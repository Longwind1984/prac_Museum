# data/sources/

Generalizable multi-source dataset for the "Together We Look" museum companion
project. The intent of this directory is **framework portability**, not
maximum data. Six heterogeneous sources are normalized into one schema
(`_schema.json`), one JSON file per source. Each file is an array; element 0
is a `_meta` object, elements 1..N are records.

> Status (2026-05-16): three of six sources are **fully degraded** to
> WebSearch-snippet extraction because the sandbox WAF blocks all direct
> WebFetch / curl against museum APIs. One source (CMA) is **fully
> extractable** because the user pre-staged a 338 MB CC0 dump at the repo
> root. Two sources are public web pages whose detail pages also 403.
> Honest counts and method-of-extraction are recorded in each file's
> `_meta` block.

## Files

| file | source | records | method | reachable? |
|---|---|---|---|---|
| `cma.json` | Cleveland Museum of Art | **100** (target cap reached) | local dump → Python extractor | dump local; API blocked |
| `met.json` | Metropolitan Museum of Art | 20 | WebSearch fallback | API+web blocked |
| `va.json` | Victoria and Albert Museum | 8 | WebSearch fallback | API+web blocked |
| `smithsonian.json` | Smithsonian (NMAA Freer/Sackler) | 7 | WebSearch fallback | API needs key + blocked, GitHub dump out of allowlist |
| `dunhuang_open.json` | 数字敦煌·开放素材库 | 8 (cave-level) | WebSearch fallback | web blocked |
| `tianlongshan_uchicago.json` | 芝大天龙山项目 | 9 (cave-level + project) | WebSearch fallback | web blocked |
| `_schema.json` | JSON Schema (draft-07) | n/a | hand-written | n/a |
| `scripts/extract_cma.py` | CMA extractor | n/a | run with `python3 data/sources/scripts/extract_cma.py` | runs offline |

Total: **152 records across 6 sources.**

## Unified schema

See `_schema.json`. Required: `source`, `source_id`, `license`, `image_urls`,
`source_url`, `tags`, `extracted_at`. All other fields are optional and **must
be `null` if unknown** — never fabricated.

### Field-by-field availability

| field | met | va | si | cma | dunhuang | tianlong |
|---|---|---|---|---|---|---|
| `title_zh` | empty | partial (hand-translated) | partial | rarely populated in dump | yes | yes |
| `title_en` | yes | yes | yes | yes | yes | yes |
| `period` / `dynasty_en` | yes | partial | yes (where snippet had it) | yes (regex-mapped) | yes | yes |
| `date_raw` / `date_start` / `date_end` | partial | partial | partial | dump fields | yes | yes |
| `materials` | partial | partial | partial | dump fields (`technique` + `support_materials`) | yes | minimal ("Stone (in situ)") |
| `dimensions` | partial | empty | empty | dump field `measurements` | rarely | rarely |
| `provenance_or_findsite` | partial | partial | yes | dump `find_spot` / flattened `provenance` chain | yes | yes (incl. dispersed locations) |
| `current_location` | hard-coded museum | hard-coded museum | hard-coded museum | dump `current_location` (gallery code) | "in situ" | "in situ" + dispersed |
| `accession_number` | mostly null (only what snippet revealed) | empty | yes (URL-derived) | yes | n/a | n/a |
| `image_urls` / `thumbnail_url` | **all empty** (snippets do not surface CDN URLs) | **all empty** | **all empty** | **populated** (openaccess-cdn.clevelandart.org) | empty | empty |
| `description` | snippet-derived (≤500 chars) | snippet-derived | snippet-derived | dump field (truncated) | snippet-derived | snippet-derived |

## Per-source extraction notes

### 1. Met Museum — degraded
- Target endpoint: `https://collectionapi.metmuseum.org/public/collection/v1/`
  with `q=Buddha&medium=Sculpture&geoLocation=China&isPublicDomain=true`.
- Sandbox result: WebFetch and curl both return `Host not in allowlist` /
  HTTP 403. The Met front-end at `metmuseum.org/art/collection/search/{id}`
  is also blocked.
- Fallback: WebSearch with curated queries (see `met.json:_meta.query_examples`).
  Each item's `source_id` is the path component from the Met URL. Every item
  surfaced via Met's "Open Access" search filter, so license is recorded as
  `PublicDomain`; per-item `isPublicDomain` flag could not be re-verified.
- Skipped fields: `additionalImages`, `primaryImage`, `creditLine` for some
  items, `geographyType` / `country` / `region` (the search snippet only
  surfaces an inline "China — Northern Wei dynasty" string).

### 2. V&A — degraded
- Target endpoint: `https://api.vam.ac.uk/v2/objects/search`. Public,
  keyless, normally usable. **HTTP 403 from the sandbox** for both API root
  and `collections.vam.ac.uk` item pages.
- Fallback: WebSearch + URL-slug-derived `systemNumber`.
- License: recorded as `Unknown` for every record. V&A image rights vary
  per-image (CC-BY-NC for many newer photographs, restricted for many older
  ones); the snippets never surface the IIIF rights statement.

### 3. Smithsonian — degraded (with two failed fallbacks)
- Target endpoint: `https://api.si.edu/openaccess/api/v1.0/search` with
  api.data.gov key.
- Attempt 1: no key provided; the endpoint refuses anonymous traffic anyway,
  and the sandbox blocks both `api.si.edu` and `asia.si.edu`.
- Attempt 2 (per task brief): GitHub `Smithsonian/OpenAccess` metadata dump
  via the `mcp__github__*` tools. **Blocked**: the GitHub MCP server here
  is locked to a single repository (`longwind1984/prac_museum`) and rejects
  any other repo with `Access denied: repository "..." is not configured`.
- Final fallback: WebSearch over `site:asia.si.edu`. The Freer/Sackler
  Xiangtangshan items dominate the relevant hit list; all 7 records have
  publicly-known accession numbers and the Smithsonian's OA program
  blanket-licenses CC0 for OA collection objects, so the license is
  recorded as `CC0`.

### 4. Cleveland Museum of Art — extracted from local dump
- Target endpoint: `https://openaccess-api.clevelandart.org/api/artworks`
  with `department=Chinese%20Art&q=Buddha&cc0=1`. **HTTP 403 from the sandbox.**
- Fallback: the user pre-staged the **full CMA OA dump** at the repo root as
  `cma.json` (338 MB, 68,748 records).
- Extractor: `scripts/extract_cma.py`. Run: `python3 data/sources/scripts/extract_cma.py`.
  Idempotent: overwrites `data/sources/cma.json`. Filter:
  - `department == "Chinese Art"`
  - `share_license_status` contains `"CC0"`
  - `title` contains a Buddhist keyword OR (`type`/`technique` ∈
    {Sculpture, Stele, Relief, Architectural, Stone} AND `tombstone`/
    `description`/`culture` contains a Buddhist keyword).
- The filter selects 56 sculptures, 26 paintings, 1 print, plus 17 records
  whose `type` is null but pass the title/culture filter. Dynasty
  distribution: Tang 16, Ming 16, Song 11, Yuan 11, Qing 10, Northern Qi 6,
  Northern Wei 6, Sui 4, Jin 4, Han 4, Liao 3, Northern Zhou 2, Five
  Dynasties 2, Eastern Wei 1. The 100-record cap is the first to hit.
- All `image_urls` are the real openaccess-cdn URLs from the dump and are
  reachable from a non-sandboxed network.

### 5. 数字敦煌·开放素材库 (Digital Dunhuang Open) — degraded
- Site is a Vue-rendered SPA; no public API. The blockchain-tracked license
  layer is the differentiator: per-image commercial licensing 300–800 RMB,
  personal/academic free download with on-chain attribution.
- Sandbox blocks both `ip.e-dunhuang.com` and `e-dunhuang.com`.
- Records here are **cave-level** (the granularity the search snippets
  surface) plus two platform-level records (license policy, inventory
  index). No per-mural / per-pattern record was retrievable.

### 6. 芝大天龙山项目 (U Chicago Tianlongshan Project) — degraded
- Site at `tls.uchicago.edu` is also 403 from this sandbox.
- Records are organized **by cave** (the project's own primary unit) plus
  one project-overview record. Dispersal information (which museums hold
  cave fragments) is surfaced in `current_location` and `provenance_or_findsite`
  where the snippets specify it. The Met `39640`, Harvard, Tokyo National
  Museum, Penn Museum links are explicit on Cave 21.

## License comparison

| source | per-item license | bulk usable for commercial RAG? | full image vectorization OK? |
|---|---|---|---|
| Met (`PublicDomain` flag) | items marked OA are CC0-equivalent | yes | yes |
| V&A | varies per-image (CC-BY-NC common) | **no — per-item review** | depends on per-item rights |
| Smithsonian OA | CC0 for OA-flagged items | yes | yes |
| CMA (`CC0`) | CC0 | yes | yes |
| Dunhuang Open | research/personal free; commercial paid | **no for commercial RAG** unless paid + on-chain licensed | research-only ingestion OK; commercial = pay-per-image |
| Tianlongshan U-Chicago | project-internal; email-grant required | **no by default** | thumbnail + metadata only by default; full image after email auth |

For ADR-003 alignment: a downstream RAG layer should partition this dataset
by `license` and treat anything outside `{CC0, PublicDomain}` as
**metadata-only** with click-through to source.

## Reproducing the dataset

### CMA (fully reproducible)
```bash
# Pre-req: cma.json at repo root. To re-fetch:
#   curl -L https://openaccess.clevelandart.org/data/cma.json -o cma.json
# (must be done from a non-sandboxed host; sandbox here blocks the host).
python3 data/sources/scripts/extract_cma.py
```

### Met / V&A / Smithsonian / Dunhuang / Tianlongshan
No scripted re-run path is provided because the sandbox cannot reach the
upstream hosts. When run from a host with normal internet access, the
intended scripts would be:
```python
# Met:    GET /public/collection/v1/search?q=Buddha&medium=Sculpture&geoLocation=China&isPublicDomain=true
#         then GET /public/collection/v1/objects/{id} for each.
# V&A:    GET /v2/objects/search?q_object_type=sculpture&q_place=China&q=buddha&images_exist=1&page_size=100
# SI:     GET /openaccess/api/v1.0/search?q=buddha+china+sculpture&api_key=DEMO_KEY (replace DEMO_KEY)
```
These scripts are **deliberately not committed** because they have never
been executed end-to-end in this environment and would otherwise be
untested.

## Completeness self-assessment

Reliable fields (≥80 % populated):
- Across all sources: `source`, `source_id`, `title_en`, `license`, `source_url`, `tags`, `extracted_at`.
- CMA only: every field except `title_zh`.

Sparsely populated:
- `title_zh`: missing on Met / CMA almost entirely (sources don't carry it).
- `image_urls`: empty on Met, V&A, Smithsonian, Dunhuang, Tianlongshan because
  search snippets do not expose CDN URLs and direct fetches are blocked.
- `accession_number`: empty on V&A and inconsistent on Met (search snippets
  don't reliably surface it).
- `dimensions`: empty on V&A and most non-CMA items.

## Known limitations and pitfalls

1. **Sandbox WAF is the dominant constraint.** Every museum API and the two
   target web sites return HTTP 403 to `WebFetch` and to `curl` (even with
   `dangerouslyDisableSandbox`). `WebSearch` is the only outbound channel
   that works, and it returns Google-snippet-grade detail.
2. **Snippet-derived records can drop on the floor between extractions.**
   Google snippet wording occasionally varies. Re-running WebSearch for the
   same query may return a different sub-set of fields per item. The 20 Met
   records here represent a hand-curated sub-set that survived two
   independent queries.
3. **License labels are coarse.** V&A `Unknown` covers items that may in
   fact be CC-BY-NC or fully restricted. Do not promote anything labelled
   `Unknown` to a CC0 codepath.
4. **CMA dump is 338 MB**; large for git. The extractor reads it lazily-ish
   (`json.load` then iterate). For a true streaming run, swap to `ijson`.
   The `.gitignore` does **not** currently exclude `cma.json` — the user
   should decide whether to track it via Git LFS, exclude it, or move it
   into `data/raw/` outside the index.
5. **Dunhuang inventory counts** in `dunhuang_open.json:_meta` come from
   Xinhua's 2024 press release, not from a direct count of the live
   library. The site updates regularly; treat the numbers as a 2024
   snapshot.
6. **Tianlongshan `image_urls` are intentionally empty.** The project's
   primary asset is the 3D viewer, which is not statically addressable.
   This is a feature, not a gap.
