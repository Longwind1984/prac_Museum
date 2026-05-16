#!/usr/bin/env python3
"""
Extract Chinese-art Public-Domain records from the Met Open Access dataset.

Source CSV:
  https://media.githubusercontent.com/media/metmuseum/openaccess/master/MetObjects.csv
  (~317 MB, 480k records, Public Domain)

Filter:
  Department == "Asian Art" AND
  (Culture contains "China" or Country contains "China") AND
  Is Public Domain == True

Image URLs:
  The CSV does not carry direct image URLs. The Met Object Page (`Link Resource`)
  exposes them but requires fetching the API endpoint
  https://collectionapi.metmuseum.org/public/collection/v1/objects/{objectID}
  to retrieve `primaryImage` / `primaryImageSmall` / `additionalImages`.
  We record the API URL in image_urls[0] and the canonical web page in source_url;
  the actual binary download happens in download_images.py, which calls the API
  per record to resolve the image URL. This keeps this extractor pure-CSV
  (no network) so the heavy filter step is reproducible offline.

Output:
  data/sources/met.json   — JSON array, [_meta, ...records]
"""
from __future__ import annotations
import csv
import datetime as _dt
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_CSV = Path("/tmp/MetObjects.csv")
OUT_PATH = REPO_ROOT / "data" / "sources" / "met.json"

DYNASTY_MAP = {
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


def derive_dynasty(*texts: str) -> tuple[str | None, str | None]:
    blob = " ".join(t for t in texts if t).lower()
    for key in sorted(DYNASTY_MAP, key=len, reverse=True):
        if key in blob:
            zh, en, _s, _e = DYNASTY_MAP[key]
            return zh, en
    return None, None


def parse_year(s: str | None) -> int | None:
    if not s:
        return None
    s = str(s).strip()
    try:
        return int(s)
    except ValueError:
        m = re.match(r"^-?\d+", s)
        return int(m.group()) if m else None


def truncate(text: str | None, n: int = 500) -> str | None:
    if not text:
        return None
    text = re.sub(r"\s+", " ", str(text)).strip()
    return text if len(text) <= n else text[: n - 1] + "…"


def split_bilingual_title(raw: str) -> tuple[str | None, str | None]:
    """Met titles for Asian Art often look like:
        '北齊 青釉陶瓶|Jar'
        '清乾隆 仿青銅器銅胎掐絲琺瑯犧尊一對|Pair of zoomorphic vessels'
    The Chinese half (mostly CJK) is left of '|', English right of it. If no '|',
    detect CJK ratio: ≥50% CJK → Chinese; else English."""
    raw = (raw or "").strip()
    if not raw:
        return None, None
    if "|" in raw:
        left, _, right = raw.partition("|")
        return left.strip() or None, right.strip() or None
    cjk = sum(1 for c in raw if "一" <= c <= "鿿" or "㐀" <= c <= "䶿")
    if cjk and cjk / max(len(raw), 1) > 0.4:
        return raw, None
    return None, raw


def normalize(row: dict) -> dict:
    object_id = row.get("Object ID", "").strip()
    culture = row.get("Culture", "").strip()
    period = row.get("Period", "").strip()
    dynasty = row.get("Dynasty", "").strip()
    object_date = row.get("Object Date", "").strip()
    object_name = row.get("Object Name", "").strip()
    title_raw = row.get("Title", "").strip()
    title_zh, title_en = split_bilingual_title(title_raw)
    if not title_en and object_name:
        title_en = object_name

    zh, en = derive_dynasty(period, dynasty, culture, object_date)

    materials = []
    for fld in ("Medium",):
        v = row.get(fld, "").strip()
        if v:
            materials.append(v)

    tags = sorted({t for t in (
        row.get("Object Name", "").strip(),
        row.get("Classification", "").strip(),
        row.get("Department", "").strip(),
        row.get("Culture", "").strip(),
        row.get("Period", "").strip(),
        row.get("Dynasty", "").strip(),
    ) if t})

    # Canonical Met API URL — used by download_images.py.
    api_url = f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{object_id}"
    return {
        "source": "met",
        "source_id": object_id,
        "title_zh": title_zh,
        "title_en": title_en,
        "period": zh,
        "dynasty_en": en or (dynasty or None),
        "date_raw": object_date or None,
        "date_start": parse_year(row.get("Object Begin Date")),
        "date_end": parse_year(row.get("Object End Date")),
        "materials": materials,
        "dimensions": row.get("Dimensions", "").strip() or None,
        "provenance_or_findsite": row.get("Geography Type", "").strip() + " " + row.get("Region", "").strip()
            if (row.get("Region") or "").strip() else (row.get("Country") or "").strip() or None,
        "current_location": "The Metropolitan Museum of Art, New York",
        "accession_number": row.get("Object Number", "").strip() or None,
        "license": "PublicDomain",
        "image_urls": [api_url],  # resolved to actual JPEG by download_images.py
        "thumbnail_url": None,
        "description": truncate(row.get("Title")) or None,
        "source_url": row.get("Link Resource", "").strip() or f"https://www.metmuseum.org/art/collection/search/{object_id}",
        "tags": tags,
        "extracted_at": _dt.datetime.now(_dt.timezone.utc).isoformat(timespec="seconds"),
    }


def main() -> int:
    csv_path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_CSV
    if not csv_path.exists():
        print(f"ERROR: CSV not found at {csv_path}", file=sys.stderr)
        print("Fetch with: curl -o /tmp/MetObjects.csv "
              "https://media.githubusercontent.com/media/metmuseum/openaccess/master/MetObjects.csv",
              file=sys.stderr)
        return 2
    csv.field_size_limit(sys.maxsize)
    out: list[dict] = []
    with csv_path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get("Department", "").strip() != "Asian Art":
                continue
            if row.get("Is Public Domain", "").lower() != "true":
                continue
            blob = (row.get("Culture", "") + " " + row.get("Country", "") +
                    " " + row.get("Period", "")).lower()
            if "china" not in blob and "chinese" not in blob:
                continue
            out.append(normalize(row))

    meta = {"_meta": {
        "source": "met",
        "endpoint": "https://collectionapi.metmuseum.org/public/collection/v1/objects/{id}",
        "csv_dump": "https://media.githubusercontent.com/media/metmuseum/openaccess/master/MetObjects.csv",
        "method": "filter CSV by Department=Asian Art AND Culture/Country contains China AND PublicDomain",
        "actual_count": len(out),
        "with_image_urls": "image_urls hold the API endpoint; resolve via download_images.py",
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
