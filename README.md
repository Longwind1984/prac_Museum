# 一起看 · AI 原生博物馆伴游

> v0.2 (2026-05-17) · 根据 Critic boot-selfcheck review 重排顶部叙事;详见 [agents/pm-critic/reviews/2026-05-17-boot-selfcheck.md](./agents/pm-critic/reviews/2026-05-17-boot-selfcheck.md)

> 不是给你讲文物,是和你一起看文物。

一份 **AI PM side project**(非商业化产品),围绕三条核心论点展开:

1. **L1 · 范式机会** — 博物馆 → 用户的「权威单向播报」假设过时。AI 原生形态可以把博物馆对话从「讲者—听众」翻成「智识同侪—智识同侪」。
2. **L2 · 差异化方向** — vs 通用 AI(ChatGPT / Gemini),「一起看」沿 5 条护城河成立:**领域深度 · 空间时间感 · 跨次记忆 · 策展人格 · 克制**。
3. **L3 · 可被审计的产品哲学** — 克制 / 立场 / 记忆 / 对等,每条落到具体机制,在 PRD §6 / §8 / §9 / §12 可被检查。

> **Founding insight**(ADR-003 附录二):面向国内大陆的中文 RAG,**最稳的图像底座不是国内馆,而是海外馆 CC0**——这是这个 side project 选择从「流散海外的中国文物」切入的现实判断,而不是审美趣味。

当前阶段产出是**定位文档 + 产品需求文档 (PRD)**,后续推进到 Figma 高保真原型。仓库里**已落地的 web 与 RAG 资产是底层数据资产,不是产品 demo**——产品形态见 PRD §4 与 §8.2。

## 项目文档

- [PRD v0](./docs/PRD.md) — 主产品需求文档(14 章,60-70% 完成度,v1 推进中)
- [ADR-001: 形态决策](./docs/ADR/001-form-factor.md) — 为什么选屏为主而非语音
- [ADR-003: 一期切片调整与知识源使用许可](./docs/ADR/003-knowledge-sources.md) — 切到天龙山+山博,六层数据源,附录二含 founding insight
- [ADR-005: 展品发现自动化(三层管道)](./docs/ADR/005-exhibit-discovery.md) — Tier 0 爬虫+LLM / Tier 1 OCR+众包 / Tier 2 SLAM

## 项目阶段

- [x] 定位与背景 v2
- [x] PRD v0 框架就位(14 章,60-70% 完成度)
- [x] 数据源框架决策(ADR-003)
- [x] 展品发现自动化决策(ADR-005)
- [x] RAG 数据资产 v0(底层素材层,见下)
- [x] 数据资产浏览器(静态 web,**非产品 demo**)
- [ ] PRD v1(依据 Critic redirect 反馈打磨,聚焦 §1 商业论点 / §14.5 八条关键决策)
- [ ] Tier 0 展品发现原型(山博"佛风遗韵")
- [ ] Figma 信息架构 + 高保真原型(**产品形态的真实 demo**)
- [ ] (可选)Web demo 接入向量库 + Anthropic API 做 RAG 推理

## demo 切片(ADR-003 调整后)

| 维度 | 锁定 |
| --- | --- |
| 主题 | 天龙山 — 从晋阳到世界:北朝佛造像的流散与数字回归 |
| 现场锚点 | 山西博物院"佛风遗韵"常设展 |
| 对照源 | 海外馆 CC0(Met / CMA / Freer)+ 数字敦煌 + 故宫院刊 PDF |
| 形态 | 屏为主,语音为辅 |
| 人格 | 同行的资深爱好者(不是导览员) |

---

## 数据资产(底层素材层,非产品本身)

> 以下是「一起看」RAG 的**底层数据资产**——不是产品 demo,不是 selling point。
> 它的作用是:**在接入 LLM / 向量库之前,先用确定性 baseline 验证数据 schema 完整性、覆盖度、字段可用性。**

[`data/sources/`](./data/sources/) — 中国艺术 CC0/PD 文物元数据,跨 **3 家海外馆**(Cleveland Museum of Art · Smithsonian Freer-Sackler · The Metropolitan Museum of Art)。

| 源(海外馆) | 元数据 | 已下图像 | 许可 |
|---|---:|---:|---|
| Cleveland Museum of Art | 2,548 | 2,451 (96%) | CC0 |
| Freer + Sackler (Smithsonian) | 1,619 | 1,614 (99.7%) | CC0 |
| The Metropolitan Museum of Art | 11,132 | 401 (3.6%) | Public Domain |
| **合计** | **15,299** | **4,466** | CC0 / PD |

> 北朝(北魏+东魏+北齐+北周)合计 176 件,加六朝/隋 116 件 — 一期切片对照件窗口约 292 件。剩余 ~15,000 条为远期 RAG 扩展素材,**当前 demo 切片实际只需要 ~88-300 条**(详见 Critic review 主要问题 #1)。

资产入口:

- [数据集 README](./data/sources/README.md) — 字段 schema、朝代矩阵、重跑命令、字段可用矩阵
- [`scripts/search.py`](./data/sources/scripts/search.py) — baseline / sanity-check 检索工具(在接入 LLM 之前先验证数据 schema)
- [`docs/index.html`](./docs/) — 数据资产浏览器(**非产品 demo**,见首屏 disclaimer)
- [gallery.md](./data/sources/gallery.md) — 240 张缩略图按朝代直接在 GitHub 网页渲染
- [.github/workflows/](./.github/workflows/) — 图像下载 + 数据刷新两个 Action(下载 workflow 2026-05-17 起冻结,见文件头注释)

---

## 团队与流程(单人多角色)

仓库使用 PM / Curator / Builder / Critic / User-Voice 多角色协作流程,所有签字、判定、review 都在 [`agents/`](./agents/) 目录公开存档,包括失败判定。最近一次 review:[2026-05-17 boot-selfcheck (REDIRECT)](./agents/pm-critic/reviews/2026-05-17-boot-selfcheck.md)。
