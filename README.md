# 一起看 · AI 原生博物馆伴游

> 不是给你讲文物，是和你一起看文物。

一个面向**文博中度爱好者**的 AI 原生伴游产品。它不把博物馆当作权威讲者、把用户当作被讲对象——它把用户当作智识同侪，先听用户怎么看，再给出自己的观点。

它有学养、有立场、有跨次记忆，**但默认沉默**。它知道自己是站在文物旁的工具，不是要把人拉回手机屏幕的应用。

这是一份 **AI PM side project**，非商业化产品。当前阶段的产出是定位文档与产品需求文档（PRD），后续会推进到 Figma 高保真原型。

## 项目文档

PRD 与 Agent 体验设计三件套**平级**——前者回答"是什么产品"，后者三份合起来回答"AI agent 怎么主导这场对话"。

**产品定义层**

- [PRD v1](./docs/PRD.md) — 产品定义：定位 / reject list / 一日剧本 / 状态机 / 真实场景边界 / 平台约束
- [v0 评审团报告](./docs/review-v0.md) — 5 角色独立 review + 主席综合 Executive Summary
- [ADR-001: 形态决策](./docs/ADR/001-form-factor.md) — 为什么选屏为主而非语音

**Agent 体验设计三件套**

- [Agent 体验设计 v0](./docs/agent-experience.md) — 编排层主文档：8 个交互模式 + 双视图 flow + harness spec + **8 个模式全部深抠到完整 prompt + few-shot + 验证器 + 失败兜底**
- [状态机形式化](./docs/state-machine.md) — XState 风格定义：spatial + audio + fatigue + memory 四并行状态机，可直接喂给 stately.ai/viz 渲染
- [横向 vs 纵向 Agent Harness](./docs/harness-comparison.md) — 独立短文：为什么"纵向 harness 才是真正的 PM 工作"。适合放进简历/作品集首页

**第一次真实体验交付**

- [`prototype/index.html`](./prototype/index.html) — 为 2026-05-19 首博「玉米/黄金/美洲豹 · 玛雅与安第斯古代文明大展」设计的完整可交互 HTML 体验原型。覆盖 8 个模式（M-01 锁屏 / M-02 双卡 / M-03 拒讲完 / M-04 跨次记忆 wow / M-05 合上手机 30 秒 / M-06 四卡对照 / M-07 学界争议 / M-08 今日记忆卡），4 件深度内容文物（翡翠面具 / 长纪年石碑 / 安第斯纺织 / 黄金 tumi），全程黑底克制式视觉。直接在浏览器打开 `prototype/index.html` 即可体验。这是第一个真实的 user story，将作为后续产品设计的 ground-truth。

## 项目阶段

- [x] 定位与背景 v2
- [x] PRD 章节大纲
- [x] PRD v0
- [x] v0 评审团 review（作品集 8.5 / 产品深度 7.5 / 落地可行性 6.0）
- [x] PRD v1（P0/P1 共 5 项必改全部落地）
- [x] Agent 体验设计 v0（8 个交互模式 + agent loop + harness spec；M-04 / M-06 深抠）
- [x] 8 个模式全部抠到完整 prompt（M-01–M-08，含 few-shot 与验证器）
- [x] 状态机形式化（XState 风格，可视化-ready）
- [x] Harness 哲学短文（横向 vs 纵向，独立可引用）
- [x] **第一次真实体验交付 v0**（HTML 可交互原型：8 个模式 × 4 件玛雅/安第斯文物 × 克制式视觉，为 5/19 首博访馆准备）
- [ ] 5/19 实地访馆 → 校准 PRD 设计假设
- [ ] PRD v2（根据实地体验修订）
- [ ] Figma 信息架构 / 高保真原型

## demo 切片

| 维度 | 锁定 |
| --- | --- |
| 品类 | 中国古代佛教造像 |
| 场馆 | 上海博物馆东馆 |
| 形态 | 屏为主，语音为辅 |
| 人格 | 同行的资深爱好者（不是导览员） |
