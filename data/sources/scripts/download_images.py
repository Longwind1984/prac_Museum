#!/usr/bin/env python3
"""
Download CC0/PD thumbnails from museum CDNs for records in data/sources/*.json.

Per-source behavior:
  cma             — image_urls already point to openaccess-cdn.clevelandart.org.
                    Pick the `_web` variant (≤ ~300 KB) and save.
  smithsonian_fsg — image_urls point to https://ids.si.edu/ids/download?id=...
                    Pick the `_screen` variant (~700-1500 px JPEG) and save.
  met             — image_urls[0] is the Met API endpoint
                    (collectionapi.metmuseum.org/.../objects/{id});
                    fetch JSON, take `primaryImageSmall`, save.

Skip if file already exists (idempotent).
Honor a configurable per-host rate limit (default 0.5s, --rate-limit).
Cap with --limit-per-source N to avoid downloading 11k images in one run.

Output: data/sources/images/{source}/{accession-or-id}.jpg
Manifest: data/sources/images/_manifest.json (URL → local path mapping)

Usage:
  python data/sources/scripts/download_images.py --limit-per-source 200
  python data/sources/scripts/download_images.py --source cma --limit-per-source 500
  python data/sources/scripts/download_images.py --dry-run
"""
from __future__ import annotations
import argparse
import json
import random
import sys
import threading
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
SOURCES_DIR = REPO_ROOT / "data" / "sources"
IMG_DIR = SOURCES_DIR / "images"
MANIFEST_PATH = IMG_DIR / "_manifest.json"

UA = "Mozilla/5.0 (compatible; museum-rag-extractor/1.0.1; +https://github.com/Longwind1984/prac_museum)"


def http_get(url: str, timeout: int = 30) -> bytes | None:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.read()
    except urllib.error.HTTPError as e:
        print(f"  HTTP {e.code} {url}", file=sys.stderr)
    except Exception as e:
        print(f"  ERR {type(e).__name__} {url} :: {e}", file=sys.stderr)
    return None


def slugify(s: str) -> str:
    return "".join(c if c.isalnum() or c in "-_." else "_" for c in s)[:80]


def out_path(source: str, rec: dict) -> Path:
    key = rec.get("accession_number") or rec.get("source_id") or "unknown"
    return IMG_DIR / source / f"{slugify(str(key))}.jpg"


def best_image_url(source: str, rec: dict) -> str | None:
    urls = rec.get("image_urls") or []
    if not urls:
        return None
    if source == "cma":
        # Prefer the `_web` variant (smaller, fits in a repo)
        for u in urls:
            if "_web.jpg" in u:
                return u
        for u in urls:
            if u.lower().endswith(".jpg"):
                return u
        return urls[0]
    if source == "smithsonian_fsg":
        for u in urls:
            if "_screen" in u or u.endswith("_screen"):
                return u
        for u in urls:
            if u.endswith(".jpg"):
                return u
        return urls[0]
    if source == "met":
        # Resolve API → primaryImageSmall
        api_url = urls[0]
        if "collectionapi.metmuseum.org" not in api_url:
            return api_url
        payload = http_get(api_url, timeout=15)
        if not payload:
            return None
        try:
            j = json.loads(payload)
        except json.JSONDecodeError:
            return None
        return j.get("primaryImageSmall") or j.get("primaryImage") or None
    # Generic fallback
    return urls[0]


def load_records(source: str) -> list[dict]:
    p = SOURCES_DIR / f"{source}.json"
    if not p.exists():
        return []
    data = json.loads(p.read_text(encoding="utf-8"))
    return [r for r in data if isinstance(r, dict) and r.get("source") == source]


def load_manifest() -> dict:
    if MANIFEST_PATH.exists():
        try:
            return json.loads(MANIFEST_PATH.read_text())
        except json.JSONDecodeError:
            return {}
    return {}


def save_manifest(m: dict) -> None:
    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST_PATH.write_text(json.dumps(m, ensure_ascii=False, indent=2, sort_keys=True))


_lock = threading.Lock()


def _process_one(source: str, rec: dict, args: argparse.Namespace, manifest: dict,
                 counters: dict) -> None:
    op = out_path(source, rec)
    if op.exists() and op.stat().st_size > 1024:
        with _lock:
            counters["skip"] += 1
        return
    url = best_image_url(source, rec)
    if not url:
        with _lock:
            counters["fail"] += 1
        return
    if args.dry_run:
        with _lock:
            counters["done"] += 1
            print(f"  DRY  {url}")
        return
    # Per-host courtesy delay (jitter avoids thundering herd).
    time.sleep(args.rate_limit * (0.5 + random.random()))
    data = http_get(url, timeout=args.timeout)
    if not data or len(data) < 1024:
        with _lock:
            counters["fail"] += 1
        return
    op.parent.mkdir(parents=True, exist_ok=True)
    op.write_bytes(data)
    with _lock:
        manifest[str(op.relative_to(REPO_ROOT))] = {
            "source": source,
            "source_id": rec.get("source_id"),
            "accession": rec.get("accession_number"),
            "url": url,
            "bytes": len(data),
        }
        counters["done"] += 1
        if counters["done"] % 25 == 0:
            save_manifest(manifest)
            print(f"  [{source}] done={counters['done']} skip={counters['skip']} fail={counters['fail']}")


def process_source(source: str, args: argparse.Namespace, manifest: dict) -> tuple[int, int, int]:
    recs = load_records(source)
    if args.shuffle:
        random.Random(args.seed).shuffle(recs)
    elif args.dynasty:
        recs = [r for r in recs if (r.get("dynasty_en") or "").lower() == args.dynasty.lower()]
    if args.limit_per_source:
        recs = recs[: args.limit_per_source]
    print(f"\n[{source}] candidate records: {len(recs)}")
    counters = {"done": 0, "skip": 0, "fail": 0}
    workers = args.parallel.get(source, 4)
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futs = [pool.submit(_process_one, source, r, args, manifest, counters) for r in recs]
        for _ in as_completed(futs):
            pass
    return counters["done"], counters["skip"], counters["fail"]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", choices=["cma", "smithsonian_fsg", "met"],
                    help="Process one source (default: all three)")
    ap.add_argument("--limit-per-source", type=int, default=2000,
                    help="Cap records processed per source (default 2000)")
    ap.add_argument("--dynasty", help="Filter by dynasty_en, e.g. 'Northern Qi'")
    ap.add_argument("--shuffle", action="store_true",
                    help="Random sample (deterministic via --seed)")
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--rate-limit", type=float, default=0.3,
                    help="Base seconds between requests within each source (default 0.3, jittered)")
    ap.add_argument("--timeout", type=int, default=30)
    ap.add_argument("--dry-run", action="store_true",
                    help="List URLs without downloading")
    args = ap.parse_args()
    # Per-source worker counts. Met has 2 HTTPs per record (API+image) and a
    # tighter API rate limit, so use fewer concurrent workers there.
    args.parallel = {"cma": 6, "smithsonian_fsg": 6, "met": 4}

    sources = [args.source] if args.source else ["cma", "smithsonian_fsg", "met"]
    manifest = load_manifest()
    totals = {"done": 0, "skip": 0, "fail": 0}
    # Run sources in parallel — they hit different CDNs, no cross-contention.
    with ThreadPoolExecutor(max_workers=len(sources)) as pool:
        futs = {pool.submit(process_source, src, args, manifest): src for src in sources}
        for f in as_completed(futs):
            src = futs[f]
            d, sk, fa = f.result()
            totals["done"] += d
            totals["skip"] += sk
            totals["fail"] += fa
            print(f"[{src}] FINISHED  done={d} skip={sk} fail={fa}")
    save_manifest(manifest)
    print(f"\nTOTAL  done={totals['done']}  skip={totals['skip']}  fail={totals['fail']}")
    print(f"Manifest: {MANIFEST_PATH.relative_to(REPO_ROOT)}")
    # Always exit 0 unless we wrote literally nothing — partial download failures
    # (rate limits, individual broken URLs) are normal and should not fail CI.
    # Only "0 done AND 0 skip" indicates a real outage worth alerting on.
    if totals["done"] == 0 and totals["skip"] == 0:
        print("CRITICAL: no images downloaded and none pre-existed.", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
