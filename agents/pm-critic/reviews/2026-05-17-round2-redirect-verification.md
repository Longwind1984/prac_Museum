# Review · round2-redirect-verification · 2026-05-17

**审查对象**:Builder-A + Builder-B 完成的 7 条「必须修」+ Track B §3.3 重构
**关联首轮 review**:[2026-05-17-boot-selfcheck.md](./2026-05-17-boot-selfcheck.md)
**审查范围**:`.github/workflows/download-images.yml` · `README.md` · `docs/index.html` · `docs/PRD.md`(§1.4 / §3.3 / §10.2 / §13.1 / §13.3 / §14.5) · `docs/ADR/003-knowledge-sources.md` · `data/sources/README.md` · `data/sources/scripts/*.py`

---

## 总判定

**APPROVE**

7 条「必须修」全部 PASS,Track B §3.3 重构 PASS,Builder 自评 surface 的 3 条潜在问题均判 paranoid 或 P2 级别——**不构成阻塞下一主线任务的理由**。

---

## 7 条修复逐项判定

| # | 任务 | 判定 | 备注 |
|---|---|---|---|
| 1 | 冻结下载 workflow | **PASS** | FROZEN 注释块清晰;push 触发整段注释保留代码;default=200 且 Compute args 步骤硬 cap(>200 直接 fail with explicit error + 指引 Curator 重签);引用了 review 文档与 4e81375 撤回意图。这是教科书级别的"冻结但不锁死"实施。 |
| 2 | §1.4 founding insight 上推 | **PASS** | 200-400 字叙事体,「反讽」修辞钩到位、衔接 §1.2 L2、结尾导回 ADR-003;ADR-003 line 138 反向链接已加,措辞"保留作技术决策依据与可泛化框架"准确。**「中国大陆/灰色地带/反讽」全部锐利保留,无稀释**。 |
| 3 | README 顶部重排 | **PASS** | 三论点 L1/L2/L3 一句话压缩在顶部;founding insight 作为 blockquote 紧跟(我同意 Builder-A 自选的"主+辅"结构,见自评 #1 判定);「3 馆」改为「3 家海外馆」并具体到 Cleveland / Freer-Sackler / Met;15,299/4,466 下沉到「数据资产(底层素材层,非产品本身)」二级;search.py 已 reframe 为 baseline / sanity-check;docs/index.html 链接旁加"非产品 demo"批注。v0.2 redirect 自陈在顶部小标,诚实标注。 |
| 4 | docs/index.html disclaimer | **PASS** | `<div class="disclaimer">` 内嵌在 `<header>` 内 h1 之下、filters 之上;**强调粗体首句「这是数据资产浏览器,不是产品 demo。」**,首屏命中;链 PRD §4 与 §8.2(GitHub 绝对链,因为 Pages 不渲 .md);视觉上 `#1c1c24` 比 panel 深 + accent border + 13px,显眼不刺眼。位置选择(随 header 滚走、二屏让位)是合理的产品判断。 |
| 5 | §13.1 范围表同步 | **PASS** | 新增「RAG 数据资产 v0」「数据资产可视化」两行,均✅完成;**「数据资产可视化」行内显式标注「这是数据资产浏览器,不是产品 demo」**——这正是 redirect 要的口径一致性;「(可选)Web demo」仍标"暂不承诺",与 docs/index.html 清晰区分;表下 redirect 注承认了同步性质而非掩盖。 |
| 6 | §14.5 决策表 close 三条 | **PASS** | 表头从「v0 当前假设」拆为「v0 假设 / v1 决策(2026-05-17)」双列,结构正确。D-2 close = **保持点名**(side project 无商务顾虑+招聘官能识别)措辞精准;D-6 close = **加深**并指向 §10.2 末尾五项 redirect 注(embedding 选型 / chunk 粒度 / retriever / re-ranker / 反幻觉编排状态机),把"决策定 / 执行后置"切清楚;D-8 close = **去除对外承诺框架**并同步 §13.3 末尾"side project 自定 milestone,不构成对外承诺"。其余 D-1/D-3/D-4/D-5/D-7 统一标"待 PM 判,不阻塞 v1 主体",D-4 额外标"同步至 ADR-002"。§10.2 / §13.3 redirect 注均到位。 |
| 7 | 去除「无 LLM」措辞 | **PASS** | 全仓 grep `无 LLM / no-LLM / without LLM`,只剩 Critic 自己的 review 文件 (本次 grep 0 hits 除 review)。search.py docstring 改写为 "this script exists *below* the LLM layer ... validates ... BEFORE we plug in embeddings and an LLM"——把 baseline 工具的位置感讲清楚,不否认能独立跑、不伪装成产品;data/sources/README.md 同步;build_rag_chunks.py 原本未自我标榜,无需改。代码逻辑未动。 |

**7/7 PASS**。无 PARTIAL、无 FAIL。

---

## §3.3 重构单独审

> 范围:§3.3 由「单 persona 林知白」升级为「4 原则 + 3 实例」,这是 PM 直接交给 Builder-B 的主线任务,首轮 review 未覆盖。

### 4 原则保留度

- **原则 A · 反对超市叙事**:精炼到位,产品含义("同伴的语气不能滑向'哇这个朝代真有意思'")可被工程化。**PASS**
- **原则 B · 反对照本宣科**:承认"少数极具洞见的大咖式讲解人"例外这一句加分(不偏激);产品含义("AI 不是讲解员,开场不是'这件是 X 朝的 Y'")可在 §6 / §7 测试。**PASS**
- **原则 C · 觉察权力结构**:**「中国大陆这样极权体制下的社会视角中,博物馆作为权力机器一部分的叙事运作——这是产品必须诚实面对的边界,不是要回避的话题」——措辞未被软化,反而更明确**。"同伴**不**承担政治宣传的相反角色——它只是诚实地把叙事性、视角性、权力性这一层 surface 出来"这一句把杀伤力与安全边界都钉好。**PASS,且这是本次重构最有信号的一段**。
- **原则 D · 知识结构的网络**:四层(布展者意图/用户自我认同/结构性批判/跨展览跨馆连接)清晰,衡量标准"是否触发了原本不会有的结构性认知"对应 §11 反指标,可被审计。**PASS**
- **原则关系图**:文本形式的 ASCII 图,D 为终点,A/B/C 为前置必要条件——简洁、对。**PASS**

四原则均未过度浓缩,均未稀释。

### 实例差异度

| 实例 | 差异轴 | 是否有效拉开维度 |
|---|---|---|
| 林知白 | PM 自身镜像(基线) | 自评"风险标注:这是 PM 镜像,易过拟合"诚实承认 |
| 陈砚秋 | 学术化极端 / 对 C 已是日常语言 / 反 §6 克制压力测试 | **是**(她容易"把产品带跑到学术辩论里"是 §6 要 test 的极端用例) |
| 周允 | 短耐心高资源 / 对 C 分场域操作("大陆馆保持沉默,他懂边界") | **是**(对 §8.2 克制度提出更极端要求,是天然 stress test) |

**4 原则认同状态填充**:三个实例对 A/B/C/D 均明确标"已认同 / 模糊 / 待引导 / 不认同"+ 一句话理由;且不是全勾"已认同"(林知白 C 标**模糊**、陈砚秋 D 内部不均匀**第 2 层不自觉**、周允 C 标**分场域**)——这种细颗粒度差异化是好信号。**PASS**

### 语气

第一人称、冷静、有立场;无"研究表明 / 数据显示"伪学术语;无感叹号;关键判断("这是 PM 自己的镜像,人格相似度过高")主动 surface 而非掩盖。与 PRD 主体一致。**PASS**

### 与 §3.4 / §3.5 衔接

- §3.3.3 反 persona 简列 4 类(A/B/C/D 类)指向 §3.4——但 §3.4 表格仍是原 3 行人口学 persona(周末打卡客 / 亲子家庭 / 学术专家),**没有按 A/B/C/D 类重写**。这是**衔接的轻度断裂**,不构成 block 但值得后续 surface。
- §3.5 已精简为 5 段框架 + 一句"剧本以叙事方式覆盖了这五段"指向 §7;原"每段产品介入点"细节已删,无与 §3.3 的冗余/矛盾。**衔接 OK**

**§3.3 重构总判定:PASS**。这是本批最有"AI PM 产品判断"信号的产出——把"用户是谁"从画像题转换为价值轴题,直接呼应 4 原则的可审计性。

---

## Builder 自评的 3 条潜在问题(逐条判)

### Builder-A #1 · README 顶部 founding insight quote 是否过长?

**判:paranoid**。quote block 一行(约 80 中文字),正好钉住"商业判断在哪"。删除会让 README 顶部回到 L1/L2/L3 三论点之后"没有商业判断信号"的状态——这是首轮 review 的核心扣分项。**保留**。

### Builder-A #2 · docs/index.html disclaimer 移动端换行?

**判:同意但 P2**。当前桌面端 disclaimer 视觉合格,移动端"挤"是边缘问题(目标读者 = 招聘官,招聘官多在桌面打开 GitHub);若日后想极致,加 `@media (max-width: 600px)` 那条 6 行 CSS 即可。**不阻塞 approve,列入 backlog "可选改进"**。

### Builder-A #3 · download-images.yml 重启时忘改 paths

**判:paranoid**。当前已注释整段 push 块+留 paths 配置在注释内;重启时"取消注释 + 检查 paths"是常规操作,且 workflow 头部 FROZEN 注释块明确说"重启自动触发(cron / push)前需 Curator 重签 + Critic 复查"——双签流程本身就会触发 paths review。**不需加 TODO**。

### (Builder-B 唯一 surface 项:陈砚秋/周允 draft 状态)

**已被 PM 当面 confirm,instances.md 已同步,不再是问题**——按任务指示跳过。

### 顺带评 Builder-B 自评 #1(§7 一日剧本仍全员林知白)

**判:同意,但属下游任务,不阻塞本轮 approve**。Builder-B 自陈"§3.3 重构是首步,§7 剧本暂未触及"是诚实的范围管理。**列入下一主线任务候选**(给 §7 选 1-2 个触点跑陈砚秋/周允微剧本)。

### 顺带评 Builder-B 自评 #2(原则 C 合规色温)

**Critic 立场:保留**。Builder 在自评里正确判断"稀释它等于稀释 PRD 唯一的市场判断信号"。这是 PM 当面指示的边界,Critic 同意 — 措辞锐利是 founding insight 与原则 C 的杀伤力来源,**T2 边界违反不命中**(无 §6/§9/§12 违反、无 Reject List 命中)。

---

## 评分变化(基线 = 首轮)

- **招聘官层:2.7 → 4.0** · 理由:§3.3 4原则+多实例 + founding insight 上推到 §1.4 + README 顶部叙事重排,AI PM taste 信号从 2 跃至 4
- **投资人层:2.2 → 3.3** · 理由:founding insight 显式化、商业判断在 README 顶部可读;但商业故事仍未独立成段,只到"够格"

招聘官层首次越过 dashboard 顶层 KPI 目标(≥4);投资人层越过 ≥3 阈值。

---

## 升级标记

- [ ] T2 边界违反(原则 C 锐利措辞已被 PM 当面 confirm 保留,不构成违反)
- [ ] T3 涉外/花钱(无)
- [ ] T4 第三轮僵局(N/A,本次是二轮,且共识 = APPROVE)

---

## 结论

7 条「必须修」全部到位,§3.3 重构质量超出 redirect 要求(它是 PM 主线任务,不是 redirect 任务,但 Builder-B 的执行让招聘官层评分单独再加 0.5)。**可以直接进入下一主线任务**——按 backlog 与 Builder-B 自评,优先候选是「§7 一日剧本注入陈砚秋/周允微剧本」与「§3.4 反 persona 按 A/B/C/D 类重写以闭合 §3.3.3 衔接」。无 P0 需补修;无升级。
