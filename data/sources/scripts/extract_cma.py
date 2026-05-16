#!/usr/bin/env python3
"""
Extract all Chinese-Art CC0 records from the Cleveland Museum of Art
open-access dump (cma.json at the repo root).

Source:
  Live API https://openaccess-api.clevelandart.org/api/artworks
  Full dump https://openaccess-api.clevelandart.org/artworks/  (single JSON)
  Re-fetch from any host with normal egress; the sandbox where this script
  was first authored could not reach the CDN.

Filter:
  department == "Chinese Art"  AND  share_license_status starts with "CC0"

Output:
  data/sources/cma.json       — JSON array, [_meta, ...records]
"""
from __future__ import annotations
import datetime as _dt
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
SOURCE_DUMP = REPO_ROOT / "cma.json"
OUT_PATH = REPO_ROOT / "data" / "sources" / "cma.json"

DYNASTY_MAP_EN = {
    "northern wei": ("北魏", "Northern Wei", 386, 534),
    "eastern wei": ("东魏", "Eastern Wei", 534, 550),
    "western wei": ("西魏", "Western Wei", 535, 557),
    "northern qi": ("北齐", "Northern Qi", 550, 577),
    "northern zhou": ("北周", "Northern Zhou", 557, 581),
    "six dynasties": ("六朝", "Six Dynasties", 220, 589),
    "sui": ("隋", "Sui", 581, 618),
    "tang": ("唐", "Tang", 618, 907),
    "five dynasties": ("五代", "Five Dynasties", 907, 960),
    "liao": ("辽", "Liao", 916, 1125),
    "song": ("宋", "Song", 960, 1279),
    "jin": ("金", "Jin", 1115, 1234),
    "yuan": ("元", "Yuan", 1271, 1368),
    "ming": ("明", "Ming", 1368, 1644),
    "qing": ("清", "Qing", 1644, 1912),
    "han": ("汉", "Han", -206, 220),
    "warring states": ("战国", "Warring States", -475, -221),
    "zhou": ("周", "Zhou", -1046, -256),
    "shang": ("商", "Shang", -1600, -1046),
    "neolithic": ("新石器时代", "Neolithic", -10000, -2000),
}


def is_relevant(rec: dict) -> bool:
    if (rec.get("department") or "").strip() != "Chinese Art":
        return False
    return "CC0" in (rec.get("share_license_status") or "").upper()


def derive_dynasty(rec: dict) -> tuple[str | None, str | None]:
    parts: list[str] = []
    for key in ("creation_date", "culture", "tombstone"):
        v = rec.get(key)
        if isinstance(v, list):
            parts.extend(str(x) for x in v)
        elif v:
            parts.append(str(v))
    blob = " ".join(parts).lower()
    # Longest-first so "northern wei" beats "wei" etc.
    for key in sorted(DYNASTY_MAP_EN, key=len, reverse=True):
        if key in blob:
            zh, en, _s, _e = DYNASTY_MAP_EN[key]
            return zh, en
    return None, None


def derive_dates(rec: dict) -> tuple[int | None, int | None]:
    def _i(x):
        try:
            return int(x) if x is not None else None
        except (ValueError, TypeError):
            return None
    return _i(rec.get("creation_date_earliest")), _i(rec.get("creation_date_latest"))


def derive_materials(rec: dict) -> list[str]:
    mats: list[str] = []
    tech = rec.get("technique")
    if tech:
        mats.append(tech)
    support = rec.get("support_materials") or []
    if isinstance(support, list):
        mats.extend(s for s in support if isinstance(s, str))
    elif isinstance(support, str):
        mats.append(support)
    seen, out = set(), []
    for m in mats:
        m = m.strip()
        if m and m.lower() not in seen:
            seen.add(m.lower())
            out.append(m)
    return out


def derive_images(rec: dict) -> tuple[list[str], str | None]:
    imgs = rec.get("images") or {}
    urls: list[str] = []
    thumb = None
    if isinstance(imgs, dict):
        for k in ("full", "print", "web"):
            v = imgs.get(k)
            if isinstance(v, dict) and v.get("url"):
                urls.append(v["url"])
        for tk in ("web", "square"):
            v = imgs.get(tk)
            if isinstance(v, dict) and v.get("url"):
                thumb = v["url"]
                break
    return urls, thumb


def derive_tags(rec: dict) -> list[str]:
    tags: set[str] = set()
    for fld in ("technique", "type", "culture", "department"):
        v = rec.get(fld)
        if isinstance(v, str) and v.strip():
            tags.add(v.strip())
        elif isinstance(v, list):
            for x in v:
                if isinstance(x, str) and x.strip():
                    tags.add(x.strip())
    return sorted(tags)


def _flatten_provenance(rec: dict) -> str | None:
    fs = rec.get("find_spot")
    if isinstance(fs, str) and fs.strip():
        return fs.strip()
    prov = rec.get("provenance")
    if isinstance(prov, str) and prov.strip():
        return prov.strip()
    if isinstance(prov, list) and prov:
        parts = []
        for p in prov:
            if isinstance(p, dict):
                desc = p.get("description")
                date = p.get("date")
                if desc:
                    parts.append(f"{desc} ({date})" if date else desc)
            elif isinstance(p, str):
                parts.append(p)
        if parts:
            return " | ".join(parts)
    return None


def truncate(text: str | None, n: int = 500) -> str | None:
    if not text:
        return None
    text = re.sub(r"\s+", " ", text).strip()
    return text if len(text) <= n else text[: n - 1] + "…"


def normalize(rec: dict) -> dict:
    zh, en = derive_dynasty(rec)
    ds, de = derive_dates(rec)
    imgs, thumb = derive_images(rec)
    return {
        "source": "cma",
        "source_id": str(rec.get("id")),
        "title_zh": rec.get("title_in_original_language"),
        "title_en": rec.get("title"),
        "period": zh,
        "dynasty_en": en,
        "date_raw": rec.get("creation_date"),
        "date_start": ds,
        "date_end": de,
        "materials": derive_materials(rec),
        "dimensions": rec.get("measurements"),
        "provenance_or_findsite": _flatten_provenance(rec),
        "current_location": rec.get("current_location") or "Cleveland Museum of Art",
        "accession_number": rec.get("accession_number"),
        "license": "CC0",
        "image_urls": imgs,
        "thumbnail_url": thumb,
        "description": truncate(rec.get("description") or rec.get("tombstone")),
        "source_url": rec.get("url") or f"https://www.clevelandart.org/art/{rec.get('accession_number','')}",
        "tags": derive_tags(rec),
        "extracted_at": _dt.datetime.now(_dt.timezone.utc).isoformat(timespec="seconds"),
    }


def main() -> int:
    if not SOURCE_DUMP.exists():
        print(f"ERROR: dump not found at {SOURCE_DUMP}", file=sys.stderr)
        print("Fetch with: curl -o cma.json https://openaccess-api.clevelandart.org/artworks/",
              file=sys.stderr)
        return 2
    with SOURCE_DUMP.open("r", encoding="utf-8") as f:
        data = json.load(f)
    out: list[dict] = []
    seen: set[str] = set()
    for rec in data:
        if not is_relevant(rec):
            continue
        norm = normalize(rec)
        if norm["source_id"] in seen:
            continue
        seen.add(norm["source_id"])
        out.append(norm)

    meta = {"_meta": {
        "source": "cma",
        "endpoint": "https://openaccess-api.clevelandart.org/api/artworks",
        "method": "local CC0 dump filtered by department=Chinese Art AND license=CC0",
        "dump_path": str(SOURCE_DUMP.relative_to(REPO_ROOT)),
        "target_count": "all matching",
        "actual_count": len(out),
        "with_image_urls": sum(1 for r in out if r["image_urls"]),
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
