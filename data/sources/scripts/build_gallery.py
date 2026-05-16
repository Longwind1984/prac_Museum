#!/usr/bin/env python3
"""
Generate data/sources/gallery.md — a curated visual index of downloaded
images, grouped by 朝代 / source. Renders natively in GitHub's web view.

Selection strategy (per dynasty):
  - Take all downloaded images for that dynasty across the 3 sources
  - Cap at SAMPLES_PER_DYNASTY per dynasty (rotate sources for diversity)
  - Skip dynasties with < 2 downloaded images

Output: data/sources/gallery.md
"""
from __future__ import annotations
import json
import os
import re
from collections import defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
SRC_DIR = REPO_ROOT / "data" / "sources"
IMG_DIR = SRC_DIR / "images"
MANIFEST = IMG_DIR / "_manifest.json"
OUT = SRC_DIR / "gallery.md"

SAMPLES_PER_DYNASTY = 12
DYNASTY_ORDER = [
    "Neolithic", "Shang", "Zhou", "Warring States", "Han",
    "Six Dynasties", "Northern Wei", "Eastern Wei", "Northern Qi",
    "Northern Zhou", "Sui", "Tang", "Five Dynasties",
    "Liao", "Song", "Jin", "Yuan", "Ming", "Qing",
]
DYNASTY_ZH = {
    "Neolithic": "新石器时代", "Shang": "商", "Zhou": "周",
    "Warring States": "战国", "Han": "汉",
    "Six Dynasties": "六朝", "Northern Wei": "北魏",
    "Eastern Wei": "东魏", "Northern Qi": "北齐",
    "Northern Zhou": "北周", "Sui": "隋", "Tang": "唐",
    "Five Dynasties": "五代", "Liao": "辽", "Song": "宋",
    "Jin": "金", "Yuan": "元", "Ming": "明", "Qing": "清",
}
SOURCE_LABEL = {
    "cma": "Cleveland Museum of Art (CMA)",
    "met": "The Met",
    "smithsonian_fsg": "Freer Gallery + Arthur M. Sackler Gallery",
}


def load_records() -> dict:
    """Return {(source, accession_or_id): record}"""
    out = {}
    for src in ("cma", "met", "smithsonian_fsg"):
        p = SRC_DIR / f"{src}.json"
        if not p.exists():
            continue
        data = json.loads(p.read_text(encoding="utf-8"))
        for r in data:
            if not isinstance(r, dict) or r.get("source") != src:
                continue
            key = r.get("accession_number") or r.get("source_id")
            if key:
                out[(src, key)] = r
    return out


def load_manifest() -> dict:
    if not MANIFEST.exists():
        return {}
    return json.loads(MANIFEST.read_text())


def main() -> int:
    records = load_records()
    manifest = load_manifest()
    print(f"records: {len(records)}; manifest entries: {len(manifest)}")

    # Group downloaded images by dynasty (English).
    by_dynasty: dict[str, list[tuple[str, dict, dict]]] = defaultdict(list)
    by_source: dict[str, int] = defaultdict(int)
    by_dyn_count: dict[str, int] = defaultdict(int)
    for relpath, info in manifest.items():
        src = info.get("source")
        key = info.get("accession") or info.get("source_id")
        rec = records.get((src, key))
        if not rec:
            continue
        dy = rec.get("dynasty_en") or "Unknown"
        by_dynasty[dy].append((relpath, rec, info))
        by_source[src] += 1
        by_dyn_count[dy] += 1

    out: list[str] = []
    out.append("# Gallery — 中国艺术 CC0/PD 图像样例\n")
    out.append("自动生成。所有图像 license = `CC0` (Cleveland / Smithsonian FSG) 或 ")
    out.append("`Public Domain` (Met)。点击图片跳源站。\n\n")
    out.append("**总数:** %d 张已下载,跨 %d 个朝代,3 家海外馆。\n\n" % (
        sum(len(v) for v in by_dynasty.values()), len(by_dynasty)))

    # Per-source summary
    out.append("## 按源\n\n")
    out.append("| 源 | 已下载 |\n|---|---:|\n")
    for src in ("cma", "smithsonian_fsg", "met"):
        out.append(f"| {SOURCE_LABEL[src]} | {by_source.get(src,0)} |\n")
    out.append("\n")

    # Per-dynasty summary
    out.append("## 按朝代\n\n")
    out.append("| 朝代 | 已下载 |\n|---|---:|\n")
    for dy in DYNASTY_ORDER:
        n = by_dyn_count.get(dy, 0)
        if n:
            zh = DYNASTY_ZH.get(dy, dy)
            out.append(f"| {zh} ({dy}) | {n} |\n")
    if "Unknown" in by_dyn_count:
        out.append(f"| 未识别 | {by_dyn_count['Unknown']} |\n")
    out.append("\n---\n\n")

    # Gallery: per dynasty, sampled
    out.append("## 样例(每朝代取 ≤ %d 张)\n\n" % SAMPLES_PER_DYNASTY)

    for dy in DYNASTY_ORDER + ["Unknown"]:
        items = by_dynasty.get(dy, [])
        if len(items) < 2:
            continue
        zh = DYNASTY_ZH.get(dy, dy)
        out.append(f"### {zh}({dy}) · 已下载 {len(items)} 张\n\n")
        # Rotate across sources for diversity
        by_src_local: dict[str, list] = defaultdict(list)
        for it in items:
            by_src_local[it[1]["source"]].append(it)
        picks = []
        round_idx = 0
        while len(picks) < SAMPLES_PER_DYNASTY:
            added = False
            for src in ("cma", "smithsonian_fsg", "met"):
                bucket = by_src_local.get(src, [])
                if round_idx < len(bucket):
                    picks.append(bucket[round_idx])
                    added = True
                    if len(picks) >= SAMPLES_PER_DYNASTY:
                        break
            if not added:
                break
            round_idx += 1
        # 3-col HTML table for nice rendering
        out.append('<table>\n<tr>\n')
        for i, (relpath, rec, info) in enumerate(picks):
            if i > 0 and i % 3 == 0:
                out.append('</tr>\n<tr>\n')
            title = rec.get("title_zh") or rec.get("title_en") or "(untitled)"
            title = re.sub(r"\s+", " ", title)[:60]
            acc = rec.get("accession_number") or rec.get("source_id") or ""
            src = rec["source"]
            date = rec.get("date_raw") or ""
            url = rec.get("source_url") or "#"
            # Relative path from data/sources/gallery.md to the image.
            # relpath is like 'data/sources/images/cma/1914.567.jpg'; strip
            # the 'data/sources/' prefix to get 'images/cma/...'.
            img_url = relpath.replace("data/sources/", "", 1)
            out.append(
                f'<td width="33%" valign="top" align="center">'
                f'<a href="{url}"><img src="{img_url}" width="200"/></a><br/>'
                f'<sub><b>{title}</b><br/>{date}<br/>'
                f'<code>{acc}</code> · {src}</sub></td>\n'
            )
        # pad last row
        while (i + 1) % 3 != 0:
            i += 1
            out.append('<td width="33%"></td>\n')
        out.append('</tr>\n</table>\n\n')

    OUT.write_text("".join(out), encoding="utf-8")
    print(f"wrote {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
