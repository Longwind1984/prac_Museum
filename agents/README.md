# Agents — 项目的常驻团队

这是「一起看」项目的常驻 agent 团队。**不是装饰**:每个 agent 都是一个实际会被 Orchestrator 召唤、用各自宪法约束、对项目有否决/推动权的角色。

## 为什么存在

PM(你)昨晚一个人干到下载完 4,466 张 Met 图、推完 RAG chunks pipeline、却发现自己越来越不确定"在推进什么"。诊断:**单一角色既出方案又评方案,没有制衡**。这个团队解决两件事:

1. **任何 Builder 产出在合入前必须有 Critic + Curator 双签**(质量 + 战略相关性)
2. **每次互动留痕在 git,角色之间通过文件互相留消息**——repo 就是团队大脑,你随时可以查 sync-log 看团队在干什么

## 团队成员

| 角色 | 一句话职责 | 否决权 |
|---|---|---|
| **Orchestrator**(=主会话) | 任务路由、调度 agent、给人(=你)做 sync | 无,但负责升级触发 |
| **PM-Critic** | 用招聘官+投资人双重视角审 Builder 的每一份产出 | 可 block Builder 提交 |
| **Strategy-Curator** | 维护"什么数据/功能/调研真的支撑 PRD 论点和商业故事" | 任务进 Builder inbox 前必须签字 |
| **Builder** | 实际写文档、写 ADR、写代码、做 Figma | 无(执行者) |
| **User-Voice** | 用 4 原则下的多个用户实例做旁评 | 建议性,但 Critic 必须读 |
| **Researcher** | 调研:学术、商业案例、馆方资源、技术选型 | 无(供给者) |

## 阶段权重(角色不变,KPI 换)

| 角色 | Phase 1(PRD v1 + 商业定位) | Phase 2(山博/上海 demo + 完整代码) |
|---|---|---|
| PM-Critic | PRD/ADR/positioning 是否经得起招聘官审视 | demo 是否现场跑通 / 代码是否生产级 |
| Strategy-Curator | "PRD 论点 ↔ 现有素材" 的关联表 | "山博+上海 30 件展品 × 跨馆对照件命中"清单 |
| Builder | 70% 写文档/ADR/positioning,30% 代码 | 70% 写代码/Figma/demo,30% 文档 |
| User-Voice | 旁评 PRD 章节、positioning、Tagline、Reject List | 现场使用模拟、可用性反馈 |
| Researcher | 商业案例 / 学术 / 竞品 | 上海+山西馆资源 / 技术选型 |

## 互动模式

### 标准任务流

```
backlog.md (Curator+Critic 联签) → builder/inbox.md → Builder 执行 → commit
  → pm-critic/reviews/{date}-{slug}.md (Critic 写 review)
  → approve / block / redirect
  → 合入主分支(approve) or 回 Builder(redirect) or 升级到 you(block 且僵局)
  → orchestrator/sync-log.md 留一行
```

### Curator 一票否决

任何任务进 builder/inbox.md **之前**,Curator 必须在该任务条目下写一行:

> 推进 KPI:[北极星 / 商业故事 / 30 件展品命中 / PRD 章节 X / 招聘官信号 Y]
> 推进强度:[强 / 中 / 弱]
> 不通过原因(若 reject):...

Curator 说不清推进什么 → 任务回 backlog,不进 Builder。

### User-Voice 周评

每周一次(或重大 PRD 章节变更后),Orchestrator 让 User-Voice 用 `user-voice/principles.md` + `user-voice/instances.md` 中的实例,对最近的 PRD/positioning 变更做旁评,写进 `user-voice/reviews/{date}.md`。建议性,但 PM-Critic 必须读完才能签 approval。

## 升级到 you 的三个触发点

只有这三种情况需要打断你:

- **T2 边界违反**:Builder 的产出违反了 PRD §6(AI 人格)/ §9(Reject List)/ §12(隐私/著作权/学术权威性边界)。Critic block + 标 T2,直接升级。
- **T3 外部资源**:涉及花钱、对外发邮件、联系馆方、签合同、公开承诺。任何 agent 提议都升级,不执行直到你签字。
- **T4 Critic-Builder 僵局**:同一份产出 Critic 与 Builder 来回 3 轮仍未达成一致,自动升级。Orchestrator 写一份僵局摘要附在 escalation 里。

不升级的(团队自己消化):
- 常规 commit / PR(只要 Critic approve)
- 文档修订、ADR 起草、Figma 草稿
- 数据集刷新、RAG pipeline 调优
- 角色之间的讨论、互相 review、内部分歧

## 你的接触面

日常你只需读两份文件:

- `orchestrator/sync-log.md` — 每天 3-5 行,谁做了什么、谁 review、谁 block
- `orchestrator/dashboard.md` — KPI 看板,Curator 每周更新

升级时你会被直接 ping,带一份 `orchestrator/escalations.md` 里的条目链接。

## 目录结构

```
agents/
├── README.md                            # 本文件
├── orchestrator/
│   ├── backlog.md                       # 全队待办
│   ├── dashboard.md                     # KPI 看板
│   ├── sync-log.md                      # 每日 sync(给你看)
│   └── escalations.md                   # T2/T3/T4 升级记录
├── pm-critic/
│   ├── constitution.md                  # 宪法 + reviewer 模型
│   └── reviews/                         # 每次 review 一份 .md(按需创建)
├── strategy-curator/
│   ├── constitution.md
│   └── exhibit-list.md                  # 山博+上海展品对照清单
├── builder/
│   ├── constitution.md
│   └── inbox.md                         # 等待执行的、已双签的任务
├── user-voice/
│   ├── constitution.md
│   ├── principles.md                    # 4 条用户原则(替代单一 persona)
│   ├── instances.md                     # 林知白 + 其他异质实例
│   └── reviews/                         # 每周旁评(按需创建)
└── researcher/
    └── constitution.md
```

## 一句话调用约定

Orchestrator 调 agent 时,prompt 必须包含三件事:

1. 任务描述
2. 该 agent 的 constitution.md 路径(让它先读)
3. 期待的输出格式(写到哪个文件、什么结构)

agent 完成后写文件,Orchestrator 读取,然后路由到下一站(可能是另一个 agent review,可能是回到人)。
