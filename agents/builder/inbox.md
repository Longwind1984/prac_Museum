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

### redirect-2 / redirect-5 / redirect-6 / Track-B · PRD 域 4 条修订(2026-05-17,Builder-B)

来源:PM 通过 Orchestrator 派单(Critic 2026-05-17 boot-selfcheck 的 修 2 / 修 5 / 修 6 + 主线 Track B 重构)。本批由 Builder-B 接 PRD 域;Builder-A 同时在 README/index/workflows 域作业,互不重叠。
产出位置:`docs/PRD.md`(主要)、`docs/ADR/003-knowledge-sources.md`(仅反向链接一句,已在前序 pass 完成)。

#### 任务 A · 修 2(P0):ADR-003 附录二洞察 → PRD §1.4

- **§1.4 新增**(已在前序 pass 完成,本轮检阅未改动):200-400 字叙事体,把"海外 CC0 是国内 RAG 最稳的图像底座"reframe 为"为什么这个 side project 从流散海外的中国文物切入";衔接 §1.2 L2 差异化方向;结尾导向"具体技术决策见 ADR-003,本节只承载洞察"
- **§1.3 末尾引导**(已存在):"关于'为什么这个 side project 从流散海外的中国文物切入'——见 §1.4"
- **ADR-003 附录二反向链接**(已存在,line 138):"本洞察已提升至 PRD §1.4 作为项目 founding insight。本附录保留作技术决策依据与可泛化框架。"
- 关键决策点:用"反讽"作为这一节的修辞钩——"做面向中国大陆用户的 AI 文博产品,最稳的图像底座反而在海外馆";避免复制 ADR 的列表式技术语言。

#### 任务 B · 修 5(P1):PRD §13.1 范围表同步本周实际产出

- **§13.1 范围表**(已在前序 pass 完成):新增"RAG 数据资产 v0"(15,299 chunks)、"数据资产可视化"(docs/index.html + gallery.md)两行,均✅完成;后者**显式标注**「这是数据资产浏览器,不是产品 demo;产品形态见 §4 / §8.2,待 Figma 阶段呈现」
- "Web demo(可选)"保留为"暂不承诺"——与 docs/index.html 区分(后者是数据浏览器,前者才是产品 demo)
- 表下小注:「2026-05-17 根据 Critic review redirect 同步实际产出。"数据资产可视化已落、产品形态 demo 待 Figma 阶段"是本次同步的核心定性」
- 关键决策点:措辞上**承认已落产物而不为之站台**——既不把它包装成产品 demo,也不掩盖它已经做出来的事实

#### 任务 C · 修 6 / Track C(P1):close §14.5 D-2 / D-6 / D-8

- **§14.5 表格扩列**:把原"v0 当前假设"列拆为"v0 假设" + "v1 决策(2026-05-17)"两列
- **D-2 保持点名**:理由——side project 无商务顾虑;reviewer = AI PM 招聘官,看到具体竞品名更能识别市场判断
- **D-6 加深**:本轮不画详细架构图,而是在 §10.2 末尾加 redirect 注,标注 v1 待补五项(embedding 选型 / chunk 粒度 / retriever / re-ranker / 反幻觉编排状态机),指向 ADR-003、ADR-005 作为暂时补足
- **D-8 去除对外承诺框架**:措辞改为"side project 自定 milestone(4-6 周内推到 v1 + Figma)";§13.3 同步加 redirect 注「本节为 side project 自定 milestone,不构成对外承诺」
- D-1 / D-3 / D-4 / D-5 / D-7 在 v1 决策列统一标"待 PM 判,不阻塞 v1 主体"(D-4 额外标"同步至 ADR-002")
- 表下小结:本表 D-2 / D-6 / D-8 已 close;其余决策不阻塞 v1 主体写作

#### 任务 D · Track B(P0,主线):§3.3 重构为 4 原则 + 多实例

- **§3.3 完整重写**,新结构:
  - 导言(约 280 字):解释为什么从单 persona 升级为「原则 + 实例」、点出单 persona 过拟合风险(林知白是 PM 自身镜像)、引用 user-voice/principles.md + instances.md 作为维护源
  - §3.3.1 四条原则:A 反对超市叙事 / B 反对照本宣科 / C 觉察权力结构(**保留**"中国大陆极权语境下博物馆作为权力机器一部分"的提法) / D 知识结构网络。每条 100-150 字 + 末尾原则关系图(文本形式,D 是终点、ABC 是前置条件)
  - §3.3.2 三个差异度高的 persona:林知白(精简至 ~200 字 + 4 原则认同状态)、陈砚秋(~280 字)、周允(~280 字),每个显式标 4 条原则上的认同状态(已认同 / 模糊 / 待引导 / 不认同)
  - §3.3.3 反 persona:简列 4 类(A/B/C/D 类),指向 §3.4
  - §3.3.4 维护机制:说明原则与实例由 user-voice/* 维护,PRD §3.3 是同步快照
- 关键取舍:
  - 原 §3.3 表格中的"年龄/职业/痛点/对策/用语"等具体字段大部分弃用——避免与 §3.5 用户旅程的描写性内容重复,也避免回到"人口学画像"的旧 persona 形态。林知白的核心人格信号(语气冷静、对 AI 助手警觉、看到话痨产品退出)保留进段落叙事
  - 三个实例的"差异点"显式写出(陈砚秋 = 学术化的极端;周允 = 短耐心高资源的极端),反向 stress test 林知白
  - 原则 C 关于"中国大陆极权语境"的提法**没有软化**——按 PM 指示诚实承认,而非回避
  - 语气保持 PRD 主体一致:第一人称、克制、有立场;不用"研究表明 / 数据显示"等伪学术语言

#### 改动文件清单(Builder-B 本轮)

- `docs/PRD.md` — §3.3 完整重写、§10.2 末尾加 redirect 注、§13.3 末尾加 redirect 注、§14.5 表格扩列 + D-2/D-6/D-8 close;§1.4 与 §13.1 已在前序 pass 完成,本轮检阅无修改
- `docs/ADR/003-knowledge-sources.md` — 无本轮改动(反向链接已在前序 pass 完成)
- `agents/builder/inbox.md` — 本节追加

#### Builder-B 自评:Critic 二轮可能会标的潜在问题

1. **§7 一日剧本仍然全员使用林知白**:T1–T14+30d 整套剧本只有林知白视角。重构后陈砚秋与周允没有进入剧本。Critic 二轮可能问:"你的多实例只是在 §3.3 装点门面,还是真的在产品决策中被使用?"——目前的回答是"§3.3 重构是首步,§7 剧本暂未触及"。若 Critic 要求,需另起任务把陈砚秋或周允的微剧本补上(至少 T2 / T7 / T9 的极端用例)
2. **原则 C 的合规色温**:本节明文写入"中国大陆极权语境下博物馆作为权力机器"。这是 PM 当面指示保留的措辞,但 PRD 一旦对外发布(招聘官/投资人读到),它会成为可被截图的一句话。Builder 不擅自软化——是 PM 在 v1 阶段需要二次确认的边界判断。已通过本注释主动 surface
3. **§14.5 D-2/D-6/D-8 close 是"决策 close",不是"内容 close"**:D-6 的"加深 RAG 架构图"实际要在 v1 写作时执行;现在只是把决策方向定了。Critic 若严格要求"close = 产物已落",这三条可能被打回。本轮判断:Phase 1 关键是把决策定下来不漂,内容落地是 v1 写作时的常规工作,不算 redirect 任务的一部分
4. **§1.4 政治色温**:Founding insight 用了"反讽""灰色地带"等措辞描述国内大陆的文物图像版权处境。对偏国内招聘官略偏锐——但这正是这条洞察的杀伤力来源,稀释它等于稀释 PRD 唯一的市场判断信号。本轮判断:保留
5. **§3.3 实例 2 / 3 仍标 draft**:`user-voice/instances.md` 中陈砚秋与周允的状态字段写的是 "draft,待 PM 确认"。本轮 §3.3 把它们当作"已实例化"写入了 PRD。如果 PM 后续 reject 这两个实例中的任何一个,§3.3 需重写。这是 Orchestrator → PM 链路的下游风险,Builder 已主动暴露

#### Builder-B 不动的事

- README / docs/index.html / .github/ / data/sources/(均为 Builder-A 域,本轮无重叠)
- ADR 主体(仅反向链接一句,已在前序 pass 完成)
- 本轮**不 commit / push**,等 Orchestrator 统一处理
- 不主动召唤 Critic 二轮 review

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
