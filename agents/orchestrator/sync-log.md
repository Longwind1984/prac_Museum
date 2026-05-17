# Daily Sync Log

> 每天 3-5 行。给 PM(=你)做日常对接。新条目放顶部。
> 格式:日期 · 谁做了什么 · 谁 review · 状态

---

## 2026-05-17

- **PM 项目级 pivot**:核心 demo 之一 = 用 AI agent 拼出市面上不存在的中国文博 RAG 知识库。锁定 4 馆(山博佛风遗韵 + 上博本馆 + 上博东馆 + 震旦)= 30 件,5 类源 / 件。Researcher 样本可行性测试 3 件 in-flight。ADR-006 草稿待 Researcher 反馈后启动。
- **Researcher Track 1/2/3** 全部完成(commits 928a6ca / ed0b43d / 143ddce):大陆 7 馆 = 「有展示·无接入」;UChicago 是 demo 隐藏中心(AIC 馆藏 + 天龙山 + 响堂山,响堂山是单点最大新发现);BMFEA + 山西大学云冈学知识库等是反向金矿。3 灰区已被 pivot 解决(灰 1 作废 / 灰 3 升级为 discovery pipeline 目标 / 灰 4 降级)。
- **PM-Critic** 完成开机自检(backlog #2):review 文件 `agents/pm-critic/reviews/2026-05-17-boot-selfcheck.md`。判定 **REDIRECT**,招聘官层 2.7/5、投资人层 2.2/5。7 条「必须修」,核心 = 4,466 张图利用率 1.97%、PRD §14.5 八决策 0 close、商业故事 0 推进、docs/index.html 形态学问题。不触发 T2/T3/T4。
- **Strategy-Curator** 完成数据相关性首次盘点(backlog #3):产出 `agents/strategy-curator/data-relevance.md`;dashboard 数据完整性 KPI 首测 = **强支撑 2.1% / 无支撑 62.8%**;**结论:禁止再扩 Met + 明清 + 占位源,定向补北朝—初唐图像,大陆馆方 0 条是最大缺口**。同步更新 exhibit-list.md「现有数据覆盖」初评列。
- **Orchestrator** 与 PM 完成团队架构对齐:5 角色 + 4 用户原则 + 3 升级触发(T2/T3/T4)
- **Orchestrator** 提交 agents/ 目录骨架:13 文件,涵盖宪法、backlog、dashboard、user-voice 原则与实例
- **下一步**:启动 PM-Critic 开机自检(backlog #2)+ PRD §3.3 重构准备(backlog #1)
- 升级:无
