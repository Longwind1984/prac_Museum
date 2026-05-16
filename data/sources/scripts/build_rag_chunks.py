#!/usr/bin/env python3
"""
Convert normalized museum records (cma.json / met.json / smithsonian_fsg.json)
into RAG-ready text chunks (NDJSON, one chunk per line) for direct embedding
and vector DB ingestion (Pinecone / pgvector / Chroma / Weaviate).

Each chunk:
  - `text`         : the natural-language string the embedder sees
  - `metadata`     : filter facets (dynasty, source, material, license …)
  - `record_id`    : back-pointer to the unified record
  - `image_local`  : path to downloaded JPEG (null if not yet downloaded)
  - `image_url`    : original CDN URL (for re-download / display)

Output: data/sources/rag_chunks.ndjson

Why one chunk per record (not split)?
  Museum records are small (≤500 chars description + a dozen short fields),
  short enough that one chunk per record yields the best recall-precision
  trade-off. If descriptions grow longer in v2 (e.g. after CNKI 短引用 enrich),
  switch to recursive splitting at 800-1200 tokens.
"""
from __future__ import annotations
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
SRC_DIR = REPO_ROOT / "data" / "sources"
IMG_DIR = SRC_DIR / "images"
MANIFEST_PATH = IMG_DIR / "_manifest.json"
OUT = SRC_DIR / "rag_chunks.ndjson"

SOURCE_LABEL = {
    "cma": "Cleveland Museum of Art",
    "met": "The Metropolitan Museum of Art",
    "smithsonian_fsg": "Freer Gallery of Art / Arthur M. Sackler Gallery (Smithsonian)",
}


def render_text(rec: dict) -> str:
    """Produce the natural-language string fed to the embedder.

    Each record becomes a single paragraph. Order matters — fields
    earlier in the text dominate sparse retrievers (BM25), so put the
    most semantically distinctive bits up front (dynasty, title, material).
    """
    parts: list[str] = []
    # Title block: Chinese first if present (Chinese-language queries
    # match better that way).
    if rec.get("title_zh"):
        parts.append(rec["title_zh"])
    if rec.get("title_en"):
        parts.append(rec["title_en"])

    # Dynasty + raw date (dates often query-able as plain numbers)
    dynasty_bits = []
    if rec.get("period"):
        dynasty_bits.append(rec["period"])
    if rec.get("dynasty_en"):
        dynasty_bits.append(rec["dynasty_en"])
    if rec.get("date_raw"):
        dynasty_bits.append(rec["date_raw"])
    if dynasty_bits:
        parts.append(" · ".join(dynasty_bits))

    # Materials
    if rec.get("materials"):
        parts.append("材质 / Material: " + "; ".join(rec["materials"]))

    if rec.get("dimensions"):
        parts.append("尺寸: " + rec["dimensions"])

    if rec.get("provenance_or_findsite"):
        parts.append("出土 / 流传: " + rec["provenance_or_findsite"])

    if rec.get("description"):
        parts.append(rec["description"])

    parts.append(f"现藏: {rec.get('current_location') or SOURCE_LABEL.get(rec['source'], rec['source'])}")
    parts.append(f"馆藏号: {rec.get('accession_number') or rec.get('source_id')}")

    return " \n\n".join(parts).strip()


def build_metadata(rec: dict) -> dict:
    """Filter facets — kept compact (most vector DBs charge per metadata byte)."""
    return {
        "source": rec["source"],
        "license": rec["license"],
        "dynasty_en": rec.get("dynasty_en"),
        "period": rec.get("period"),
        "date_start": rec.get("date_start"),
        "date_end": rec.get("date_end"),
        "materials": rec.get("materials") or [],
        "has_image_local": False,   # filled in below if manifest hit
        "current_location": rec.get("current_location"),
    }


def main() -> int:
    manifest = {}
    if MANIFEST_PATH.exists():
        manifest = json.loads(MANIFEST_PATH.read_text())
    # Build lookup: (source, accession) -> local image path
    img_lookup: dict[tuple[str, str], str] = {}
    for relpath, info in manifest.items():
        src = info.get("source")
        key = info.get("accession") or info.get("source_id")
        if src and key:
            img_lookup[(src, str(key))] = relpath

    n_total = n_with_local_img = 0
    sources_seen = []
    with OUT.open("w", encoding="utf-8") as out:
        for src in ("cma", "met", "smithsonian_fsg"):
            p = SRC_DIR / f"{src}.json"
            if not p.exists():
                continue
            data = json.loads(p.read_text(encoding="utf-8"))
            count = 0
            for rec in data:
                if not isinstance(rec, dict) or rec.get("source") != src:
                    continue
                acc = str(rec.get("accession_number") or rec.get("source_id") or "")
                img_local = img_lookup.get((src, acc))
                meta = build_metadata(rec)
                if img_local:
                    meta["has_image_local"] = True
                    n_with_local_img += 1
                chunk = {
                    "record_id": f"{src}:{acc}",
                    "text": render_text(rec),
                    "metadata": meta,
                    "image_local": img_local,
                    "image_url": rec.get("thumbnail_url") or (rec.get("image_urls") or [None])[0],
                    "source_url": rec.get("source_url"),
                }
                out.write(json.dumps(chunk, ensure_ascii=False) + "\n")
                count += 1
                n_total += 1
            sources_seen.append((src, count))
            print(f"  {src}: {count} chunks")
    print(f"\nwrote {n_total} chunks → {OUT.relative_to(REPO_ROOT)}")
    print(f"  with local image: {n_with_local_img} ({100*n_with_local_img/n_total:.1f}%)")
    print(f"  size: {OUT.stat().st_size/1024/1024:.1f} MB")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
