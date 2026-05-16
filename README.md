# 一起看 · AI 原生博物馆伴游

> 不是给你讲文物，是和你一起看文物。

一个面向**文博中度爱好者**的 AI 原生伴游产品。它不把博物馆当作权威讲者、把用户当作被讲对象——它把用户当作智识同侪，先听用户怎么看，再给出自己的观点。

它有学养、有立场、有跨次记忆，**但默认沉默**。它知道自己是站在文物旁的工具，不是要把人拉回手机屏幕的应用。

这是一份 **AI PM side project**，非商业化产品。当前阶段的产出是定位文档与产品需求文档（PRD），后续会推进到 Figma 高保真原型。

## 项目文档

- [PRD v0](./docs/PRD.md) — 主产品需求文档（14 章）
- [ADR-001: 形态决策](./docs/ADR/001-form-factor.md) — 为什么选屏为主而非语音
- [ADR-003: 一期切片调整与知识源使用许可](./docs/ADR/003-knowledge-sources.md) — 切到天龙山+山博,六层数据源
- [ADR-005: 展品发现自动化(三层管道)](./docs/ADR/005-exhibit-discovery.md) — Tier 0 爬虫+LLM / Tier 1 OCR+众包 / Tier 2 SLAM

## RAG 数据集(已落地)

[`data/sources/`](./data/sources/) — **15,299 条** 中国艺术 CC0/PD 文物元数据 + **4,466 张**真图,跨 3 家海外馆。

- 📊 [数据集 README](./data/sources/README.md) — 字段 schema、朝代矩阵、重跑命令
- 📷 [gallery.md](./data/sources/gallery.md) — 240 张代表图按朝代直接在 GitHub 网页渲染
- 🔎 [search.py](./data/sources/scripts/search.py) — 无 LLM CLI 检索(例:`--dynasty "Northern Qi" --has-image`)
- 🌐 [docs/index.html](./docs/) — 交互式 web 图鉴(可部署 GitHub Pages)
- 🤖 [.github/workflows/](./.github/workflows/) — 图像下载 + 数据刷新两个 Action

### 数据规模

| 源 | 元数据 | 图像 | 许可 |
|---|---:|---:|---|
| Cleveland Museum of Art | 2,548 | 2,451 (96%) | CC0 |
| Freer + Sackler (Smithsonian) | 1,619 | 1,614 (99.7%) | CC0 |
| The Metropolitan Museum | 11,132 | 401 (3.6%) | Public Domain |
| **合计** | **15,299** | **4,466** | CC0 / PD |

> 北朝(北魏+东魏+北齐+北周)合计 176 件,加六朝/隋 116 件 — 一期切片对照件窗口约 292 件。

## 项目阶段

- [x] 定位与背景 v2
- [x] PRD v0 框架就位(14 章,60-70% 完成度)
- [x] 数据源框架决策(ADR-003)
- [x] 展品发现自动化决策(ADR-005)
- [x] RAG 数据集 v0(15,299 条 + 4,466 张图)
- [x] 静态 web 图鉴(可部署 Pages)
- [ ] PRD v1(依据 review 反馈打磨,同步 ADR-003/005)
- [ ] Tier 0 展品发现原型(山博"佛风遗韵")
- [ ] Figma 信息架构
- [ ] Figma 高保真原型
- [ ] (可选)Web demo 接入向量库 + Anthropic API 做 RAG 推理

## demo 切片(ADR-003 调整后)

| 维度 | 锁定 |
| --- | --- |
| 主题 | 天龙山 — 从晋阳到世界:北朝佛造像的流散与数字回归 |
| 现场锚点 | 山西博物院"佛风遗韵"常设展 |
| 对照源 | 海外馆 CC0(Met / CMA / Freer)+ 数字敦煌 + 故宫院刊 PDF |
| 形态 | 屏为主,语音为辅 |
| 人格 | 同行的资深爱好者(不是导览员) |
