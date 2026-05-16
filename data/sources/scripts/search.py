#!/usr/bin/env python3
"""
Filter + plain-text search over the unified RAG chunks.

No LLM, no vector DB, no third-party deps. Runs anywhere with Python 3.11+.

Examples:
  python data/sources/scripts/search.py --dynasty "Northern Qi" --has-image
  python data/sources/scripts/search.py -q "bodhisattva" --limit 10
  python data/sources/scripts/search.py --material limestone --dynasty "Tang"
  python data/sources/scripts/search.py -q "曹衣出水" --json   # raw NDJSON output
  python data/sources/scripts/search.py --source met --license PublicDomain
"""
from __future__ import annotations
import argparse
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
CHUNKS = REPO_ROOT / "data" / "sources" / "rag_chunks.ndjson"


def load_chunks() -> list[dict]:
    if not CHUNKS.exists():
        sys.exit(f"missing {CHUNKS}; run build_rag_chunks.py first")
    # Use split('\n') not splitlines() — the latter also splits on U+2028/U+2029/U+0085
    # which JSON doesn't escape, breaking records that contain them in descriptions.
    return [json.loads(line) for line in CHUNKS.read_text(encoding="utf-8").split("\n") if line]


def matches(chunk: dict, args: argparse.Namespace) -> bool:
    m = chunk["metadata"]
    if args.source and m["source"] != args.source:
        return False
    if args.license and m["license"] != args.license:
        return False
    if args.dynasty and (m.get("dynasty_en") or "").lower() != args.dynasty.lower():
        return False
    if args.material:
        mats = " ".join(m.get("materials") or []).lower()
        if args.material.lower() not in mats:
            return False
    if args.has_image and not m.get("has_image_local"):
        return False
    if args.year_start is not None and m.get("date_start") is not None:
        if m["date_start"] < args.year_start:
            return False
    if args.year_end is not None and m.get("date_end") is not None:
        if m["date_end"] > args.year_end:
            return False
    if args.query:
        # Case-insensitive substring match, with CJK-aware (no normalization).
        text = chunk["text"].lower()
        for term in args.query.split():
            if term.lower() not in text:
                return False
    return True


def score(chunk: dict, query: str) -> int:
    """Tiny BM25-ish score for sorting query hits — count term occurrences in title."""
    if not query:
        return 0
    txt = chunk["text"][:200].lower()
    return sum(txt.count(t.lower()) for t in query.split())


def main() -> int:
    ap = argparse.ArgumentParser(description="Search the museum RAG chunks.")
    ap.add_argument("-q", "--query", help="Space-separated terms; all must match (case-insensitive).")
    ap.add_argument("--source", choices=["cma", "met", "smithsonian_fsg"])
    ap.add_argument("--dynasty", help="dynasty_en, e.g. Northern Qi")
    ap.add_argument("--material", help="substring in materials list")
    ap.add_argument("--license", choices=["CC0", "PublicDomain"])
    ap.add_argument("--year-start", type=int, help="≥ this year (negative for BCE)")
    ap.add_argument("--year-end", type=int)
    ap.add_argument("--has-image", action="store_true", help="only records with local image")
    ap.add_argument("--limit", type=int, default=20)
    ap.add_argument("--json", action="store_true", help="output raw NDJSON")
    args = ap.parse_args()

    chunks = load_chunks()
    hits = [c for c in chunks if matches(c, args)]
    if args.query:
        hits.sort(key=lambda c: -score(c, args.query))
    hits = hits[: args.limit]

    if args.json:
        for h in hits:
            print(json.dumps(h, ensure_ascii=False))
        return 0

    print(f"\nFound {len(hits)} match(es) (of {len(chunks)} total chunks)\n")
    for h in hits:
        m = h["metadata"]
        # First line of text is title(s)
        title_line = h["text"].split("\n", 1)[0].strip()
        img = "🖼" if m["has_image_local"] else "  "
        print(f"  {img} [{m['source']:>16}] {m.get('dynasty_en') or '?':>20}  {title_line[:60]}")
        print(f"        {h['record_id']}  →  {h['source_url']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
