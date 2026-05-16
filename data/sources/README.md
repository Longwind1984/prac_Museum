# data/sources/

**博物馆 RAG 语料库 — 中国艺术专题**

15,299 条 CC0 / Public Domain 文物元数据,跨 3 家海外馆,统一 schema,
全部带原始图像 URL,配套自动化下载管线(GitHub Actions)。这是「一起看」
RAG 主语料,也是 ADR-003 附录二「可泛化数据源框架」的样例落地。

## 数据规模

| 源 | 馆 | 条数 | 带图 URL | 许可 | 文件 |
|---|---|---:|---:|---|---|
| `cma` | Cleveland Museum of Art (CMA) | 2,548 | 2,451 | CC0 | [`cma.json`](./cma.json) (4.0 MB) |
| `met` | The Metropolitan Museum of Art | 11,132 | 11,132 | Public Domain | [`met.json`](./met.json) (11 MB) |
| `smithsonian_fsg` | Freer Gallery + Arthur M. Sackler Gallery | 1,619 | 1,614 | CC0 | [`smithsonian_fsg.json`](./smithsonian_fsg.json) (3.0 MB) |
| **合计 (主语料)** |  | **15,299** | **15,197** | CC0 / PD | 18 MB |
| `va` | Victoria and Albert Museum | 8 | 0 | Unknown | [`va.json`](./va.json) — placeholder |
| `dunhuang_open` | 数字敦煌·开放素材库 | 8 | 0 | DunhuangFreeForResearch | [`dunhuang_open.json`](./dunhuang_open.json) — cave-level |
| `tianlongshan_uchicago` | 芝大天龙山项目 | 9 | 0 | ProjectInternal | [`tianlongshan_uchicago.json`](./tianlongshan_uchicago.json) — cave-level |

每个 `.json` 是数组,第 0 个元素是 `_meta`(端点、方法、统计),后续是 schema 化记录。

## 朝代覆盖矩阵(主语料)

| 朝代 | CMA | Met | Smithsonian FSG | 合计 |
|---|---:|---:|---:|---:|
| 新石器时代 (Neolithic) | 14 | 72 | 173 | **259** |
| 商 (Shang, -1600 to -1046) | 34 | 136 | 84 | **254** |
| 周 (Zhou, -1046 to -256) | 50 | 194 | 163 | **407** |
| 战国 (Warring States, -475 to -221) | 48 | 81 | 80 | **209** |
| 汉 (Han, -206 to 220) | 141 | 413 | 265 | **819** |
| 北魏 (Northern Wei, 386-534) | 18 | 55 | 18 | **91** |
| 东魏 (Eastern Wei, 534-550) | 1 | 5 | 11 | **17** |
| 北齐 (Northern Qi, 550-577) | 13 | 21 | 20 | **54** |
| 北周 (Northern Zhou, 557-581) | 2 | 1 | 11 | **14** |
| 六朝 (Six Dynasties, 220-589) | 15 | 37 | 0 | **52** |
| 隋 (Sui, 581-618) | 9 | 36 | 19 | **64** |
| 唐 (Tang, 618-907) | 139 | 418 | 38 | **595** |
| 五代 (Five Dynasties, 907-960) | 17 | 13 | 2 | **32** |
| 辽 (Liao, 916-1125) | 18 | 29 | 0 | **47** |
| 宋 (Song, 960-1279) | 306 | 464 | 28 | **798** |
| 金 (Jin, 1115-1234) | 30 | 66 | 0 | **96** |
| 元 (Yuan, 1271-1368) | 140 | 304 | 56 | **500** |
| 明 (Ming, 1368-1644) | 323 | 1,510 | 478 | **2,311** |
| 清 (Qing, 1644-1912) | 1,138 | 6,043 | 112 | **7,293** |
| 朝代未识别 | 92 | 1,234 | 61 | **1,387** |

> 北朝(北魏 91 + 东魏 17 + 北齐 54 + 北周 14)合计 **176 件**,加上六朝 52
> 件、隋 64 件,**北朝—初唐窗口共 ~292 件可作对照**。山西博物院"佛风遗韵"
> 常设展实物约 30-40 件,海外 CC0 对照件足够覆盖每件实物 5-7 个对照角度。

## 字段(unified schema)

完整 JSON Schema 见 [`_schema.json`](./_schema.json)。核心字段:

| 字段 | 类型 | 说明 |
|---|---|---|
| `source` | str enum | `met` / `cma` / `smithsonian_fsg` / `va` / `dunhuang_open` / `tianlongshan_uchicago` |
| `source_id` | str | 原 ID(Met=objectID, CMA=id, FSG=edanmdm hash) |
| `title_zh` | str\|null | 中文题名(Met 双语题名拆分后) |
| `title_en` | str\|null | 英文题名 |
| `period` | str\|null | 中文断代(`北齐`/`盛唐`/`明嘉靖` 等) |
| `dynasty_en` | str\|null | 英文断代(`Northern Qi`/`Tang` 等) |
| `date_raw` | str\|null | 源站原文,**不规范化** |
| `date_start` / `date_end` | int\|null | 公元年(负数=BCE) |
| `materials` | str[] | 材质,源站原文,顺序保留 |
| `dimensions` | str\|null | 尺寸,源站原文 |
| `provenance_or_findsite` | str\|null | 流传/出土,源站原文 |
| `current_location` | str\|null | 现藏馆/展厅 |
| `accession_number` | str\|null | 馆藏号(如 CMA `1914.567`) |
| `license` | str enum | `CC0` / `PublicDomain` / `CC-BY` / `Restricted` / `Unknown` / `DunhuangFreeForResearch` / `ProjectInternal` |
| `image_urls` | str[] | 全分辨率/缩略图 URL 数组。Met 是 API 端点,需 `download_images.py` 解析;CMA/FSG 是直链 |
| `thumbnail_url` | str\|null | 推荐缩略图 |
| `description` | str\|null | 源站描述,**≤500 字、逐字截断、不改写** |
| `source_url` | str | 源站物件页 |
| `tags` | str[] | 源站分类/标签 |
| `extracted_at` | ISO datetime | 提取时间 |

**真实性硬约束**:字段缺失填 `null`,**禁止编造**。

## 图像下载机制

### 为什么不直接 commit 图片

这个仓库的原始开发环境(沙盒)WAF 阻塞所有博物馆 CDN
(`images.metmuseum.org` / `ids.si.edu` / `openaccess-cdn.clevelandart.org`
全部 403)。因此本地无法下载图像;但 GitHub Actions runner 走的是普通
egress,可以下载。**图像由 Actions 异步落到仓库**,不阻塞元数据交付。

### 自动管线(2 个 workflow)

#### 1. `.github/workflows/download-images.yml`

- 触发:`workflow_dispatch`(手动)+ 主语料 JSON 改动时自动跑
- 默认每源 200 张(可调),共 600 张,~25–60 MB
- 输出:`data/sources/images/{source}/{accession}.jpg`
- 清单:`data/sources/images/_manifest.json`(URL → 本地路径)
- 自动 commit 回当前分支(commit message 带 `[skip-images]` 避免循环)

手动触发可传参:
- `limit`:每源条数(默认 200)
- `source`:只跑 `cma` / `smithsonian_fsg` / `met` 之一
- `dynasty`:按 `dynasty_en` 过滤,如 `Northern Qi`

#### 2. `.github/workflows/refresh-extractors.yml`

- 触发:手动 + 每月 1 号自动
- 拉 CMA dump(~325 MB) + Met CSV(~317 MB) + Smithsonian S3 全量
- 重跑 3 个 extractor
- 自动 commit JSON 文件

## 重跑方法(本地,需通网环境)

```bash
# 1. 拉数据源
curl -L -o cma.json "https://openaccess-api.clevelandart.org/artworks/"
curl -L -o /tmp/MetObjects.csv \
  "https://media.githubusercontent.com/media/metmuseum/openaccess/master/MetObjects.csv"

# 2. 跑 extractor
python data/sources/scripts/extract_cma.py
python data/sources/scripts/extract_met.py /tmp/MetObjects.csv
python data/sources/scripts/extract_smithsonian_fsg.py   # 自动从 S3 拉

# 3. 下载图片(默认每源 200 张)
python data/sources/scripts/download_images.py --limit-per-source 200

# 4. (可选)单源 / 单朝代下载
python data/sources/scripts/download_images.py \
  --source cma --dynasty "Northern Qi" --limit-per-source 50
```

只需 Python 3.11 stdlib。`requirements.txt` 只列了可选依赖。

## 字段可用矩阵(主语料)

| 字段 | cma | met | smithsonian_fsg |
|---|---|---|---|
| `title_zh` | 偶有 (`title_in_original_language`) | **3,105 件**(双语题名拆分) | 暂无 |
| `title_en` | **全有** | **全有** | **全有** |
| `period` / `dynasty_en` | 朝代正则映射,北朝精确 | 朝代正则映射,北朝精确 | 朝代正则映射,北朝精确 |
| `date_start` / `date_end` | dump 字段 `creation_date_earliest/latest` | CSV 字段 `Object Begin/End Date` | 解析 `date` 文本 |
| `materials` | dump `technique` + `support_materials` | CSV `Medium` | `physicalDescription` |
| `dimensions` | dump `measurements` | CSV `Dimensions` | `measurements` |
| `provenance_or_findsite` | dump `provenance` 链(扁平化) | CSV `Geography Type + Region` | `notes` 中 label=Provenance(前 3 条) |
| `accession_number` | dump `accession_number` | CSV `Object Number` | `identifier` 中 label=Accession Number |
| `image_urls` | 直链 (3 档:web/print/full) | API 端点(`download_images.py` 解析) | 直链(thumb/screen/jpg/tif 多档,最多 10 URL) |
| `description` | `description` 或 `tombstone`,≤500 字截断 | CSV `Title`(简短) | `notes` 第一条 |
| `license` | 直接读 `share_license_status` | CSV `Is Public Domain` | 读 `usage.access` |

## 每源数据出处

### Cleveland Museum of Art(cma)
- 端点(主):<https://openaccess-api.clevelandart.org/artworks/>(单一巨型 JSON dump,~325 MB)
- 端点(分页):<https://openaccess-api.clevelandart.org/api/artworks?cc0=1>
- 许可:CC0 (`share_license_status` 字段值 = `CC0`)
- 字段密度极高:多档图像、完整流传链、当前展厅号(`current_location`)
- 注:本仓库 `.gitignore` 排除了原 325 MB dump;extract_cma.py 期望 `/cma.json`

### The Met(met)
- 端点(批量):<https://media.githubusercontent.com/media/metmuseum/openaccess/master/MetObjects.csv>(317 MB,Git LFS)
- 端点(单件,带图):<https://collectionapi.metmuseum.org/public/collection/v1/objects/{id}>
- 许可:Public Domain (`Is Public Domain == "True"`)
- CSV 不带图像 URL — `download_images.py` 调单件 API 解出 `primaryImageSmall`
- 双语题名 (`北齊 青釉陶瓶|Jar`) 已拆 `title_zh` / `title_en`

### Smithsonian Freer + Sackler(smithsonian_fsg)
- 端点:`s3://smithsonian-open-access/metadata/edan/fsg/*.txt`(256 分片,line-delimited JSON,~27 MB)
- 索引:<https://smithsonian-open-access.s3-us-west-2.amazonaws.com/metadata/edan/fsg/index.txt>
- 许可:CC0(`usage.access == "CC0"`,FSG 几乎全部覆盖)
- 单件最多带 10 个图像 URL(tif/jpg/screen/thumb 多档)
- 现位置硬编码 = "Freer Gallery of Art / Arthur M. Sackler Gallery, Smithsonian"

## 占位源(等待重跑)

以下 3 个文件保留为占位,源 API 在原沙盒不可达且无 GitHub/AWS 镜像可绕,
待通网环境补完。**这些文件目前数据稀薄(WebSearch 片段级),不可作 RAG 主源**。

| 源 | 待解决方案 |
|---|---|
| `va.json` | V&A `api.vam.ac.uk/v2/objects/search`,无需 key,通网环境下可写一个 ~30 行的 `extract_va.py` |
| `dunhuang_open.json` | 数字敦煌·开放素材库 (`ip.e-dunhuang.com`),需付费授权(300–800 元/张),不入本仓库 |
| `tianlongshan_uchicago.json` | 芝大天龙山项目 (`tls.uchicago.edu`),需邮件申请,3D 数据不公开下载 |

## 已知限制 / 坑

1. **图像 URL 不等于图像文件**——主语料 15,299 条只是元数据 + URL,实际图片需要 `download_images.py` 落盘
2. **Met CSV 不带图像 URL**——必须调单件 API 解;11k 条全量解析 ~3 小时(0.5s/req 限速),建议分批
3. **朝代正则映射的局限**——CSV 中只有 `Object Date` 而无明确 `Dynasty` 字段的记录(尤其 Qing 内的细分如"乾隆"),目前只能落到顶层朝代
4. **CMA dump 是 CC0-only 过滤后的结果**——`share_license_status` 含 `Copyrighted` 的记录被过滤掉,所以实际记录可能少于馆方公布总数
5. **Smithsonian FSG `place=China` 过滤可能误伤**——少量记录用 "East Asia" 而非 "China" 标注,目前漏掉
6. **图片下载脚本无并发**——单线程 + 限速,200 张约 100 秒;如改成 ThreadPool 注意各 CDN 的 rate-limit 政策

## 数据更新策略

- 主语料三个源每月 1 号自动重跑(workflow `refresh-extractors`)
- 图像按需触发(`download-images` 手动 dispatch)
- `_meta.extracted_at` 字段记录每条 extraction 时间,可做增量 diff

## 相关 ADR

- [ADR-003:一期切片调整与知识源使用许可](../../docs/ADR/003-knowledge-sources.md)——本数据集落地的决策依据
- [ADR-005:展品发现自动化(三层管道)](../../docs/ADR/005-exhibit-discovery.md)——下一步:把"哪件在哪个展厅"加进来
