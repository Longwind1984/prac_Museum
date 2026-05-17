# 全队 Backlog

> 优先级标签:**P0** 立即 / **P1** 本周 / **P2** 本月 / **P3** 暂存
> 状态:`draft` `curator-签字中` `builder-执行中` `critic-review中` `done` `blocked`
> 每条任务必须有 Curator 签字才能进 Builder inbox。

## P0 — Phase 1 启动包

### 1. PRD §3.3 重构:从单 persona 林知白 → 4 原则 + 多实例
- 来源:用户 2026-05-17 输入
- Curator 签字:**待写**(强 / PRD 章节质量 + 招聘官信号:展示用户研究的严谨性)
- 产出:更新 docs/PRD.md §3.3,引用 agents/user-voice/principles.md 与 instances.md
- 状态:`draft`

### 2. PM-Critic 开机自检:审 2025-05-16 / 17 的工作
- 来源:团队 boot 流程
- 范围:近 7 天 commit,特别是 4,466 张 Met 图下载 + RAG chunks pipeline + galleries
- 期待问题:"这些产出推进了 PRD/商业故事的哪条具体论点?哪些是 over-engineering?"
- Curator 签字:**待写**
- 状态:`draft`

### 3. Strategy-Curator 数据相关性盘点
- 任务:对 data/sources/ 下现有 15,299 条数据,逐源标注"对 PRD 哪条论点 / 哪个 KPI 有支撑"
- 产出:agents/strategy-curator/data-relevance.md
- 状态:`draft`

### 4. 展品清单 v0:山博佛风遗韵 + 上海重点馆
- 任务:列出 demo 候选展品(30 件 ±),每件标注馆 / 朝代 / 选它的理由 / 跨馆对照件候选
- 产出:agents/strategy-curator/exhibit-list.md(已建空架,待填)
- 状态:`draft`

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
