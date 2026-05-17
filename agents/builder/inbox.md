# Builder · Inbox

> 只有 Curator 签过字的任务才能进这里。Builder 自顶向下执行。
> 完成后挪到本文件底部的「完成」区。

## 待执行

(空 — 等待 Curator 完成 backlog #1, #2, #3 三条 P0 任务的签字后填入)

## 完成

### redirect-1 · 冻结图像下载工作流(P0)
- **来源**:pm-critic/reviews/2026-05-17-boot-selfcheck.md · 必须修 1
- **Curator 签字**:(本批为 Critic redirect 直接派单,无 Curator 二次签字;遵循 review 文末「必须修」)
- **产出位置**:`.github/workflows/download-images.yml`
- **完成定义(DoD)**:
  - [x] workflow 顶部加 FROZEN 注释块(说明冻结时间 / 双签 / 重启前提)
  - [x] push 触发整段注释掉(代码保留以便日后重启)
  - [x] workflow_dispatch.inputs.limit 默认值从 5000 改为 200
  - [x] 增加 Compute args 步骤的硬上限检查(limit > 200 直接 fail with explicit error)
  - [x] 引用 review 文档路径 + 撤回 4e81375 意图
- **关键决策**:保留 `workflow_dispatch` + dynasty / source 输入,因为后续「30 件展品对照件清单」驱动的定向跑需要这两个 filter;硬 cap 写在 step 里,即便有人改 default 也跑不出去
- **review request 路径**:待 Orchestrator commit 后建

### redirect-3 · README 顶部重排(P0)
- **来源**:pm-critic/reviews/2026-05-17-boot-selfcheck.md · 必须修 3
- **Curator 签字**:同上
- **产出位置**:`README.md`(根目录)
- **完成定义(DoD)**:
  - [x] 顶部加 v0.2 (2026-05-17) 小标 + 指向 Critic review 的链接(诚实标注 redirect 事实)
  - [x] 顶部 selling point 改为 **PRD §1 三条核心论点压缩**(L1 / L2 / L3),并紧跟 ADR-003 附录二 founding insight 一段
  - [x] 显式说明「web + RAG 已落资产是数据资产,不是产品 demo」
  - [x] "15,299 / 4,466 / 3 馆"下沉为「数据资产(底层素材层,非产品本身)」二级章节
  - [x] "3 馆"全部改为「3 家海外馆(Cleveland / Smithsonian Freer-Sackler / Met)」
  - [x] search.py 的 framing 改为 "baseline / sanity-check 检索工具"
  - [x] docs/index.html 链接旁注「非产品 demo,见首屏 disclaimer」
- **关键决策点**:顶部 framing **同时**用了 PRD §1 三条论点(L1/L2/L3)**和** ADR-003 founding insight。理由:三条论点是产品自身价值主张,founding insight 是"为什么选这个切片"的商业判断,两者在 README 顶部回答的是不同问题——招聘官看价值主张,投资人看商业判断。任务说"二选一",我选了"主+辅":三论点为主叙事,founding insight 以 quote block 紧跟作为补充。如果 Critic 觉得太长,可以二轮再砍 founding insight quote。
- **review request 路径**:待 Orchestrator commit 后建

### redirect-4 · docs/index.html 加 disclaimer(P0)
- **来源**:pm-critic/reviews/2026-05-17-boot-selfcheck.md · 必须修 4
- **Curator 签字**:同上
- **产出位置**:`docs/index.html` + `README.md`(链接旁批注)
- **完成定义(DoD)**:
  - [x] `<header>` 内 h1 下方、filters 上方插入 `<div class="disclaimer">`
  - [x] 强调粗体首句「这是数据资产浏览器,不是产品 demo。」
  - [x] 链向 PRD §4 与 §8.2(github.com 绝对链接,因为 GitHub Pages 默认不渲染 .md)
  - [x] CSS:背景 `#1c1c24` 比 panel 略浅 + 左侧 3px accent 色 border + padding 12px 14px + border-radius 4px + font-size 13px + 显眼但不刺眼
  - [x] README 中 docs/index.html 链接旁加批注
- **关键决策点**:disclaimer 内嵌在 `<header>` 内而非另起 section,这样在 sticky filters 滚下来之后,disclaimer 会随 header 一起滚出视野——首屏命中,二屏让位给数据。如果 Critic 觉得应该 sticky,二轮再改。
- **review request 路径**:待 Orchestrator commit 后建

### redirect-7 · 去除「无 LLM」selling point 措辞(P1)
- **来源**:pm-critic/reviews/2026-05-17-boot-selfcheck.md · 必须修 7
- **Curator 签字**:同上
- **产出位置**:`data/sources/scripts/search.py` · `data/sources/scripts/build_rag_chunks.py` · `data/sources/README.md`
- **完成定义(DoD)**:
  - [x] search.py 顶部 docstring 改为 "Baseline / sanity-check retrieval. ... a vector retriever + LLM sits on top. This script exists *below* that — it validates ... BEFORE we plug in embeddings and an LLM."
  - [x] build_rag_chunks.py docstring 已无「无 LLM」措辞(原本也未自我标榜无 LLM,主要 framing 集中在 search.py 与 data/sources/README.md)
  - [x] data/sources/README.md 中「无 LLM CLI 检索」改写为「baseline / sanity-check 检索工具」段落
  - [x] 全仓 grep 「无 LLM / no-LLM / without LLM」只剩 Critic review 自己 — 通过
  - [x] 代码逻辑完全未动,仅改文字
- **关键决策点**:search.py docstring 改写后明确写出"this script exists *below* the LLM layer"——这把 baseline 工具的位置感讲清楚了,既不否认它能独立跑,也不把它伪装成产品。
- **review request 路径**:待 Orchestrator commit 后建

---

## 自评:这一轮 Critic 可能还会标的点

1. **README 顶部「Founding insight」quote 是否过长?** 我把它做成 quote block 跟在三论点后。Critic 可能会说「招聘官 5 分钟读 README,quote block 会被跳过」——但我判断招聘官读完 L1/L2/L3 后,quote 这一行是把"商业判断在哪"的钉子钉下去。若被 redirect,下移到 demo 切片表的脚注即可。

2. **docs/index.html disclaimer 在移动端的换行**。我 mobile breakpoint 没单独加 disclaimer 样式,小屏会读起来有点挤(220px 网格下文字会贴边)。如果 Critic 拿手机打开发现挤,二轮加一条 `@media (max-width: 600px) { .disclaimer { padding: 10px 12px; font-size: 12px; } }` 即可。

3. **download-images.yml 的「重启时改回 push 触发」注释**。我注释掉了 push 块但留下了原 paths 配置,日后重启时要改两处(取消注释 + 确认 paths 仍准确)。如果 Critic 觉得这给未来留了「忘改 paths」的坑,二轮可以加一条 TODO 标记。

4. **没动的事**(任务边界外,提示 Orchestrator 注意):
   - PRD / ADR 未动(Builder-B 域)
   - 修 2(把 founding insight 上推到 PRD §1)未动 — 这是 PRD 域
   - 修 5 / 修 6(PRD §13.1 同步、PRD §14.5 close 决策)未动 — PRD 域
   - sync-log.md 未动 — 留给 Orchestrator commit 时统一写

5. **诚实度风险**:README 顶部新加的「PRD v0 (14 章,60-70% 完成度,v1 推进中)」这个 60-70% 是从 review 引用的;若 Builder-B 在并行改 PRD 时数字变了,需要对齐。我没动这个数字。

---

## 任务条目模板

```
### {任务编号} · {标题}
- **来源**:backlog.md #{n}
- **Curator 签字**:推进 {KPI}; 强度 {强/中/弱}; 合理性 {30字}
- **产出位置**:{文件路径}
- **完成定义(DoD)**:
  - [ ] ...
  - [ ] ...
- **review request 路径**:pm-critic/reviews/{date}-{slug}.md
```
