# 全队 Backlog

> 优先级标签:**P0** 立即 / **P1** 本周 / **P2** 本月 / **P3** 暂存
> 状态:`draft` `curator-签字中` `builder-执行中` `critic-review中` `done` `blocked`
> 每条任务必须有 Curator 签字才能进 Builder inbox。

## P0 — Phase 1 启动包

### 1. PRD §3.3 重构:从单 persona 林知白 → 4 原则 + 多实例 ✅
- 来源:用户 2026-05-17 输入
- Builder-B 2026-05-17 完成;Critic round2 PASS
- 状态:**done**

### 2. PM-Critic 开机自检:审 2025-05-16 / 17 的工作 ✅
- 来源:团队 boot 流程
- 输出:7 条「必须修」→ Builder-A/B 并行修复 → Critic round2 APPROVE
- 评分:招聘官 2.7→4.0,投资人 2.2→3.3
- 状态:**done**

### 3. Strategy-Curator 数据相关性盘点 ✅
- 输出:强支撑 2.1%、无支撑 62.8%、大陆馆方 0 条 = 最大缺口
- 状态:**done**

### 修复批(2026-05-17 redirect 7 条「必须修」)✅
- 修 1 冻结下载 / 修 2 §1.4 founding insight / 修 3 README 重排 / 修 4 index.html disclaimer / 修 5 §13.1 同步 / 修 6 §14.5 D-2/D-6/D-8 close / 修 7 「无 LLM」措辞清零
- 全部 PASS(Critic round2 2026-05-17)
- 状态:**done**

### 4. 展品清单 v0:山博佛风遗韵 + 上海重点馆
- 任务:列出 demo 候选展品(30 件 ±),每件标注馆 / 朝代 / 选它的理由 / 跨馆对照件候选
- 产出:agents/strategy-curator/exhibit-list.md(已建空架,待填)
- 状态:`draft`(依赖主线 #11 信息源调研结果,再启动)

## P0 — 主线任务(2026-05-17 PM 直接交付)

### 11. 信息源最佳素材调研(主线 · 第 1 步)✅
- Researcher Track 1/2/3 完成,3 份 reports 已 commit
- 状态:**done** — 输入到 #12

### 12. Open Discovery Pipeline + 30 件 RAG bundle(主线 · 第 2 步)
- 来源:PM 2026-05-17 项目级 pivot 决定
- **核心**:用 AI agent 从分散来源拼出市面上不存在的中国文博 RAG 知识库;过程本身=核心 demo
- 范围(锁定):山博佛风遗韵 15 件 + 上博本馆 5 件 + 上博东馆 5 件 + 震旦 5 件 = **30 件**
- 每件 bundle 5 类源:馆方一手 / 跨馆对照 / 学术论文 / 现场场域 / 数字人文 OA
- 时间盒:7 天 v0,先证明 pipeline,再加深;Curator/Critic 守过度工程线
- 排程:
  - 12.0 Researcher 样本 pipeline 可行性测试(3 件样本)— **in-flight**
  - 12.1 ADR-006 Open Discovery Pipeline 草稿(Builder,样本完成后启动)
  - 12.2 PRD §1.4 补"AI-driven discovery as USP"段(Builder,12.1 后)
  - 12.3 30 件批量执行(Builder × Researcher,12.1 + 12.2 完成后)
- 风险:微信公众号(ToS 灰区,不抓)/ 馆方 robots.txt / Phase 1 时间预算重排
- 状态:`researcher-in-flight`

## P1 — 本周内

### 5. PRD §1 商业论证强化(reviewer = 招聘官+投资人)
- 当前 §1.2 三条核心论点偏产品价值,缺商业闭环说明
- 任务:在 §1 或新增 §1.4,加一段"为什么这个 side project 能让招聘官识别独立建项目的能力 / 投资人识别市场判断"
- Curator 签字:**待写**
- 状态:`draft`

### 6. Reject List(PRD §9)与 4 原则的一致性 check
- User-Voice 任务:用 4 原则推演,Reject List 是否漏了什么 / 多了什么
- 状态:`draft`

### 7. ADR 索引补全
- PRD §14.3 列了 ADR 索引但未完;盘点 docs/ADR/ 现状,补缺
- 状态:`draft`

## P2 — 本月

### 8. Figma 低保真:T2/T3/T6 三个关键触点
- 等 PRD §7 剧本稳定后启动
- 状态:`draft`

### 9. RAG 最小可跑 demo
- 已有 chunks pipeline,需要一个能在浏览器/CLI 跑通的端到端 query → answer demo
- 状态:`draft`

### 10. 用户研究方法论补强(PRD §3.1 局限性)
- 当前是设计假设,缺少未来"如何升级为真用户研究"的路径
- 状态:`draft`

## P3 — 暂存

- 多语言支持设计
- 离线模式设计
- 与馆方合作的商业模式探索(T3 触发,不主动推)

## 完成档案

(空)

---

**Curator + PM-Critic 维护这个文件。Builder 只读 inbox.md,不读这里。**
