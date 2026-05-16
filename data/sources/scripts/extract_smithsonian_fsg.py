#!/usr/bin/env python3
"""
Extract Chinese-art CC0 records from the Freer Gallery + Arthur M. Sackler
Gallery (FSG, Smithsonian) Open Access dataset.

Source:
  AWS S3 bucket: smithsonian-open-access (us-west-2)
  Index:  https://smithsonian-open-access.s3-us-west-2.amazonaws.com/metadata/edan/fsg/index.txt
  Files:  256 shards (00.txt .. ff.txt), line-delimited JSON, ~4,700 records total.

Filter:
  content.freetext.place.content contains "China"
  AND record has online_media with usage.access = "CC0"  (essentially all FSG records).

Output:
  data/sources/smithsonian_fsg.json — JSON array, [_meta, ...records]
"""
from __future__ import annotations
import datetime as _dt
import json
import re
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
OUT_PATH = REPO_ROOT / "data" / "sources" / "smithsonian_fsg.json"
INDEX_URL = "https://smithsonian-open-access.s3-us-west-2.amazonaws.com/metadata/edan/fsg/index.txt"
CACHE_DIR = Path("/tmp/fsg")

DYNASTY_MAP = {
    "northern wei": ("北魏", "Northern Wei"),
    "eastern wei": ("东魏", "Eastern Wei"),
    "western wei": ("西魏", "Western Wei"),
    "northern qi": ("北齐", "Northern Qi"),
    "northern zhou": ("北周", "Northern Zhou"),
    "six dynasties": ("六朝", "Six Dynasties"),
    "sui": ("隋", "Sui"),
    "tang": ("唐", "Tang"),
    "five dynasties": ("五代", "Five Dynasties"),
    "liao": ("辽", "Liao"),
    "song": ("宋", "Song"),
    "jin": ("金", "Jin"),
    "yuan": ("元", "Yuan"),
    "ming": ("明", "Ming"),
    "qing": ("清", "Qing"),
    "han": ("汉", "Han"),
    "warring states": ("战国", "Warring States"),
    "zhou": ("周", "Zhou"),
    "shang": ("商", "Shang"),
    "neolithic": ("新石器时代", "Neolithic"),
}


def http_get(url: str, dest: Path, timeout: int = 30) -> bool:
    if dest.exists() and dest.stat().st_size > 0:
        return True
    req = urllib.request.Request(url, headers={"User-Agent": "rag-extractor/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            data = r.read()
        dest.write_bytes(data)
        return True
    except Exception as e:
        print(f"  ! {url} :: {e}", file=sys.stderr)
        return False


def fetch_all(parallel: int = 12) -> list[Path]:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    index_local = CACHE_DIR / "index.txt"
    if not http_get(INDEX_URL, index_local):
        print(f"ERROR: cannot fetch FSG index", file=sys.stderr)
        sys.exit(2)
    urls = [u.strip() for u in index_local.read_text().splitlines() if u.strip()]
    shard_paths = []
    with ThreadPoolExecutor(max_workers=parallel) as pool:
        futs = []
        for u in urls:
            p = CACHE_DIR / Path(u).name
            futs.append(pool.submit(http_get, u, p))
            shard_paths.append(p)
        for f in futs:
            f.result()
    return [p for p in shard_paths if p.exists() and p.stat().st_size > 0]


def truncate(text: str | None, n: int = 500) -> str | None:
    if not text:
        return None
    text = re.sub(r"\s+", " ", str(text)).strip()
    return text if len(text) <= n else text[: n - 1] + "…"


def first_freetext(rec_content: dict, kind: str) -> str | None:
    items = rec_content.get("freetext", {}).get(kind, []) or []
    for it in items:
        c = (it.get("content") or "").strip()
        if c:
            return c
    return None


def all_freetext(rec_content: dict, kind: str, label_filter: str | None = None) -> list[str]:
    out = []
    for it in rec_content.get("freetext", {}).get(kind, []) or []:
        if label_filter and it.get("label", "").lower() != label_filter.lower():
            continue
        c = (it.get("content") or "").strip()
        if c:
            out.append(c)
    return out


def derive_dynasty(text: str) -> tuple[str | None, str | None]:
    b = (text or "").lower()
    for key in sorted(DYNASTY_MAP, key=len, reverse=True):
        if key in b:
            zh, en = DYNASTY_MAP[key]
            return zh, en
    return None, None


def parse_year_range(date_raw: str) -> tuple[int | None, int | None]:
    if not date_raw:
        return None, None
    s = date_raw.strip()
    # e.g. "618-907", "ca. 12th century", "Tang dynasty (618-907)"
    m = re.search(r"(-?\d{1,4})\s*[-–to ]+\s*(-?\d{1,4})", s)
    if m:
        try:
            return int(m.group(1)), int(m.group(2))
        except ValueError:
            pass
    m = re.match(r"^(-?\d{3,4})", s)
    if m:
        try:
            return int(m.group(1)), int(m.group(1))
        except ValueError:
            pass
    return None, None


def normalize(rec: dict) -> dict | None:
    content = rec.get("content") or {}
    place = first_freetext(content, "place") or ""
    if "china" not in place.lower():
        return None

    title = rec.get("title") or first_freetext(content, "objectType") or ""
    date_raw = first_freetext(content, "date") or ""
    period_raw = ""
    for it in content.get("freetext", {}).get("date", []) or []:
        if (it.get("label") or "").lower() == "period":
            period_raw = it.get("content", "")
            break

    zh, en = derive_dynasty(period_raw + " " + date_raw)
    ds, de = parse_year_range(date_raw)

    materials = []
    for it in content.get("freetext", {}).get("physicalDescription", []) or []:
        c = (it.get("content") or "").strip()
        if c and len(materials) < 3:
            materials.append(c)

    topic_strs = [t.get("content") for t in content.get("freetext", {}).get("topic", []) if t.get("content")]
    if not materials and topic_strs:
        materials = [t for t in topic_strs[:3]]

    dimensions = first_freetext(content, "measurements") or None

    # Provenance: concatenate first 3 provenance notes
    provenance_notes = all_freetext(content, "notes", "Provenance")
    provenance = " | ".join(provenance_notes[:3]) if provenance_notes else None

    accession = None
    for it in content.get("freetext", {}).get("identifier", []) or []:
        if (it.get("label") or "").lower() in ("accession number", "object number"):
            accession = it.get("content", "")
            break

    # Images
    image_urls = []
    thumbnail_url = None
    license_str = "Unknown"
    online = content.get("descriptiveNonRepeating", {}).get("online_media", {})
    if isinstance(online, dict):
        for m in online.get("media", []) or []:
            if (m.get("usage") or {}).get("access") == "CC0":
                license_str = "CC0"
            mc = m.get("content")
            if isinstance(mc, str):
                image_urls.append(mc)
            for r in m.get("resources", []) or []:
                u = r.get("url")
                if u:
                    if "thumb" in (r.get("label") or "").lower():
                        thumbnail_url = thumbnail_url or u
                    image_urls.append(u)

    # Dedupe image urls
    seen, dedup = set(), []
    for u in image_urls:
        if u not in seen:
            seen.add(u)
            dedup.append(u)
    image_urls = dedup
    if not thumbnail_url and image_urls:
        # Find a "thumb" or "_thumb" URL
        for u in image_urls:
            if "thumb" in u.lower():
                thumbnail_url = u
                break

    tags = sorted({t for t in [
        first_freetext(content, "objectType"),
        place,
        en,
        *(topic_strs[:5]),
    ] if t})

    page_url = rec.get("url") or ""
    if page_url and not page_url.startswith("http"):
        page_url = "https://www.si.edu/object/" + page_url

    return {
        "source": "smithsonian_fsg",
        "source_id": rec.get("id"),
        "title_zh": None,
        "title_en": title or None,
        "period": zh,
        "dynasty_en": en or (period_raw or None),
        "date_raw": date_raw or None,
        "date_start": ds,
        "date_end": de,
        "materials": materials,
        "dimensions": dimensions,
        "provenance_or_findsite": provenance,
        "current_location": "Freer Gallery of Art / Arthur M. Sackler Gallery, Smithsonian",
        "accession_number": accession,
        "license": license_str,
        "image_urls": image_urls,
        "thumbnail_url": thumbnail_url,
        "description": truncate(first_freetext(content, "notes")) or None,
        "source_url": page_url or None,
        "tags": tags,
        "extracted_at": _dt.datetime.now(_dt.timezone.utc).isoformat(timespec="seconds"),
    }


def main() -> int:
    shards = fetch_all()
    print(f"Have {len(shards)} FSG shards in {CACHE_DIR}")
    out, seen = [], set()
    total_seen = 0
    for sp in shards:
        with sp.open() as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    rec = json.loads(line)
                except json.JSONDecodeError:
                    continue
                total_seen += 1
                n = normalize(rec)
                if not n:
                    continue
                if n["source_id"] in seen:
                    continue
                seen.add(n["source_id"])
                out.append(n)

    meta = {"_meta": {
        "source": "smithsonian_fsg",
        "endpoint": "s3://smithsonian-open-access/metadata/edan/fsg/*.txt",
        "method": "download all 256 shards, filter by place=China",
        "shards_scanned": len(shards),
        "raw_records_scanned": total_seen,
        "actual_count": len(out),
        "with_image_urls": sum(1 for r in out if r["image_urls"]),
        "with_cc0": sum(1 for r in out if r["license"] == "CC0"),
        "extracted_at": _dt.datetime.now(_dt.timezone.utc).isoformat(timespec="seconds"),
    }}
    payload = [meta] + out
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUT_PATH.open("w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    print(f"wrote {len(out)} records to {OUT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
