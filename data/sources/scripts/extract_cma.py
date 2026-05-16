#!/usr/bin/env python3
"""
Extract Chinese Buddhist sculpture records from the Cleveland Museum of Art
open-access dump (cma.json at the repo root).

Why a local file:
  The live API https://openaccess-api.clevelandart.org/api/artworks is blocked
  by the sandbox WAF in this environment (HTTP 403 on every probe). The user
  pre-staged the full CC0 dump at /home/user/prac_Museum/cma.json so we work
  off that. Re-fetching the dump: see README.md (curl from a host that can
  reach openaccess-api.clevelandart.org).

Filter:
  department == "Chinese Art"
  AND (title or culture or technique or type mentions Buddha / Buddhist /
       Bodhisattva / stele / luohan / 佛 / 菩萨)
  AND share_license_status starts with "CC0"
  AND type in {"Sculpture","Stele","Stone","Architectural Element", ...}
       or culture mentions a relevant Chinese dynasty.

Output: data/sources/cma.json (array of unified records, <=100, with _meta).

Idempotent: re-running overwrites the output file.
"""
from __future__ import annotations
import datetime as _dt
import json
import os
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
SOURCE_DUMP = REPO_ROOT / "cma.json"
OUT_PATH = REPO_ROOT / "data" / "sources" / "cma.json"

MAX_RECORDS = 100

KEYWORDS = [
    "buddha", "buddhist", "bodhisattva", "stele", "luohan", "lohan",
    "guanyin", "avalokiteshvara", "maitreya", "amitabha", "vairocana",
    "shakyamuni", "dvarapala", "lokapala", "arhat",
]

DYNASTY_MAP_EN = {
    "northern wei": ("北魏", "Northern Wei", 386, 534),
    "eastern wei": ("东魏", "Eastern Wei", 534, 550),
    "western wei": ("西魏", "Western Wei", 535, 557),
    "northern qi": ("北齐", "Northern Qi", 550, 577),
    "northern zhou": ("北周", "Northern Zhou", 557, 581),
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
    "six dynasties": ("六朝", "Six Dynasties", 220, 589),
}


def is_relevant(rec: dict) -> bool:
    if (rec.get("department") or "").strip() != "Chinese Art":
        return False
    license_ = (rec.get("share_license_status") or "").upper()
    if "CC0" not in license_:
        return False
    title = (rec.get("title") or "").lower()
    type_ = (rec.get("type") or "").lower()
    tech = (rec.get("technique") or "").lower()
    # Title-level Buddhist hit OR (Sculpture/Stele type + description-level hit).
    if any(kw in title for kw in KEYWORDS):
        return True
    sculptural = any(t in (type_ + " " + tech) for t in
                     ("sculpture", "stele", "relief", "architectural", "stone"))
    if sculptural:
        blob_parts: list[str] = []
        for key in ("tombstone", "description", "culture"):
            v = rec.get(key)
            if isinstance(v, str):
                blob_parts.append(v)
        blob = " ".join(blob_parts).lower()
        if any(kw in blob for kw in KEYWORDS):
            return True
    return False


def derive_dynasty(rec: dict) -> tuple[str | None, str | None]:
    parts: list[str] = []
    for key in ("creation_date", "culture", "tombstone"):
        v = rec.get(key)
        if isinstance(v, list):
            parts.extend(str(x) for x in v)
        elif v:
            parts.append(str(v))
    blob = " ".join(parts).lower()
    for key, (zh, en, _s, _e) in DYNASTY_MAP_EN.items():
        if key in blob:
            return zh, en
    return None, None


def derive_dates(rec: dict) -> tuple[int | None, int | None]:
    s = rec.get("creation_date_earliest")
    e = rec.get("creation_date_latest")
    try:
        s = int(s) if s is not None else None
    except (ValueError, TypeError):
        s = None
    try:
        e = int(e) if e is not None else None
    except (ValueError, TypeError):
        e = None
    return s, e


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
    # Dedupe, preserve order.
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
    # CMA images dict has keys: web, print, full, square, ...
    if isinstance(imgs, dict):
        for k in ("full", "print", "web"):
            v = imgs.get(k)
            if isinstance(v, dict) and v.get("url"):
                urls.append(v["url"])
        sq = imgs.get("web") or imgs.get("square")
        if isinstance(sq, dict):
            thumb = sq.get("url")
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
    title = rec.get("title") or ""
    tomb = rec.get("tombstone") or ""
    blob = (str(title) + " " + str(tomb)).lower()
    for kw in KEYWORDS:
        if kw in blob:
            tags.add(kw)
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
    mats = derive_materials(rec)
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
        "materials": mats,
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
        return 2
    with SOURCE_DUMP.open("r", encoding="utf-8") as f:
        data = json.load(f)
    out: list[dict] = []
    seen_ids: set[str] = set()
    for rec in data:
        if not is_relevant(rec):
            continue
        norm = normalize(rec)
        if norm["source_id"] in seen_ids:
            continue
        seen_ids.add(norm["source_id"])
        out.append(norm)
        if len(out) >= MAX_RECORDS:
            break

    meta = {
        "_meta": {
            "source": "cma",
            "endpoint": "local-dump (openaccess-api.clevelandart.org unreachable from sandbox)",
            "dump_path": str(SOURCE_DUMP.relative_to(REPO_ROOT)),
            "filter": "department=Chinese Art AND title/type/culture matches Buddhist keywords AND CC0",
            "target_count": MAX_RECORDS,
            "actual_count": len(out),
            "network_reachable": False,
            "api_key_required": False,
            "rate_limit_observed": "n/a (local file)",
            "extracted_at": _dt.datetime.now(_dt.timezone.utc).isoformat(timespec="seconds"),
        }
    }
    payload = [meta] + out
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUT_PATH.open("w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    print(f"wrote {len(out)} records to {OUT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
