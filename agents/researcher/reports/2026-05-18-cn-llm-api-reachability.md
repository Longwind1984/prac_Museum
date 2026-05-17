# Research · 国内 LLM API 可达性 mini 实测 · 2026-05-18

**召唤者**:Orchestrator(PM 当面授权直接跑)
**题目**:5 家国内 LLM API(+Kimi)从海外沙箱可达性、注册门槛、联网搜索工具
**时间盒**:30 min(用时约 25 min)
**置信度**:逐项标注(沙箱 curl 实测 = 已验证;官网/二手源 = 基于文档,未自验)
**主要来源**(访问日期均为 2026-05-17):
- DeepSeek 定价/Function Calling 文档:https://api-docs.deepseek.com/quick_start/pricing / https://api-docs.deepseek.com/guides/function_calling
- DeepSeek +86 限制公告(2025-01):https://www.163.com/dy/article/JMUTS3040511A6N9.html
- 智谱 BigModel web_search 文档:https://docs.bigmodel.cn/cn/guide/tools/web-search (返回 403,信息来自搜索摘要)
- 智谱 GLM-4-Flash 永久免费:https://docs.bigmodel.cn/cn/guide/models/free/glm-4.7-flash
- 阿里百炼新人额度 + 地域限制:https://help.aliyun.com/zh/model-studio/new-free-quota
- 阿里百炼 web_search 工具:https://help.aliyun.com/zh/model-studio/web-search
- 阿里云国际版手机绑定限制:https://developer.aliyun.com/ask/164094
- 百度千帆 web_search 参数:https://cloud.baidu.com/doc/qianfan-docs/s/Wm8r4sw29
- 火山方舟 Web Search 插件:https://www.volcengine.com/docs/82379/1756990
- 火山方舟 50 万 tokens 免费额度:https://next.ithome.com/archiver/774/730.htm
- Kimi web_search 工具 + 海外端点 api.moonshot.ai:https://platform.moonshot.cn/docs/guide/use-web-search / https://platform.moonshot.ai/

## 重要前置发现(curl 实测,已验证)

**沙箱出口对所有外网都返回 `HTTP/2 403` + `x-deny-reason: host_not_allowed` + 21 字节 body `Host not in allowlist`** —— 含 OpenAI、Anthropic、Google、故宫、上博。这是**沙箱 egress proxy 的统一拦截行为**,不能用 curl 证伪"中国侧拦截海外 IP"。

DNS 解析能成功(已验证):
- `api.deepseek.com` → **3.173.21.63 (CloudFront)** — 唯一一家走海外 CDN
- `open.bigmodel.cn` → 122.10/129.227/156.59 (globalconnect 跨境加速,香港/中国)
- `dashscope.aliyuncs.com` → 8.140.x.x / 47.236.x.x (阿里云华东 / 国际)
- `qianfan.baidubce.com` → 全 IPv6 中国电信/联通段(240e:/2408:/2409:)
- `ark.cn-beijing.volces.com` → 101.126.7.76 (Volces 北京)
- `api.moonshot.cn` → 8.147.223.37 (Aliyun DDoS 高防)

**结论**:沙箱内 curl 测可达性等于零信号。下表"endpoint 海外可达"列基于 (a) 该域名是否解析到海外 CDN、(b) 二手源里海外用户能否调通的报告。

## TL;DR(3 条,给 PM)

1. **真海外可达只有 DeepSeek 一家**(走 CloudFront)。其余 5 家域名都解析回中国大陆/香港,海外 latency 高且可能被对端 IP 风控,但 API 协议本身没做地域阻断 —— 走代理/在国内服务器跑就行。
2. **自带"开箱即用联网搜索"的有 5 家**:智谱(全套,接 Bing/搜狗/夸克/Jina)、阿里百炼(`enable_search=True` 或 `web_search` 工具,MCP 端点每月 2000 次免费)、百度千帆(`web_search` 参数)、火山方舟(Web Search 插件)、Kimi(`$web_search` 工具)。**DeepSeek 是唯一一家不自带联网搜索**,需要你自己接 SerpApi/Google。
3. **零摩擦门槛最低的是 Kimi 海外站 `api.moonshot.ai`** —— 域名在海外、自带联网搜索;但是否能用非中国手机号注册没有公开文档明证。**如果接受 +86 手机号 + 身份证实名**,智谱 BigModel 性价比最高:2000 万 token 新人额度 + GLM-4-Flash 永久免费 + 完整搜索栈。

## 6 家对照表

| 厂商 | endpoint 海外可达性 | 注册门槛 | 免费额度 | 联网搜索工具 | 推荐度 |
|---|---|---|---|---|---|
| **DeepSeek** | **真海外 CDN(CloudFront)**,可达性最好 | **2025-01 起仅 +86 手机号**,身份证实名后才能充值 | 10 元试用(部分时段);新用户曾有 50 万-500 万 tokens,文档口径不一 | **无内置联网搜索**,需自己接 SerpApi | ★★ |
| **智谱 GLM-4** | 中国/香港 IP,无海外 CDN | +86 + 身份证实名(海外手机号无文档支持) | **GLM-4-Flash 永久免费** + 新人 2000 万 tokens / 3 个月 | **完整搜索栈**:Web Search API / Web Search in Chat / Search Agent,后端可选 Bing/搜狗/夸克/Jina | ★★★★★ |
| **通义千问(百炼)** | 中国华东/新加坡 IP | +86 + 个人实名;**国际版要非大陆手机号**且**无免费额度** | 内地版每模型 100 万 tokens,总额 7000 万+,90 天 | `enable_search=True` 或 `tools: web_search`;MCP WebSearch 端点 2000 次/月免费 | ★★★ |
| **百度文心(千帆)** | 全 IPv6 中国电信/联通 | +86 + 身份证实名 | 部分模型免费 / 千万 token 资源包(活动制) | `web_search` 请求参数,绑百度搜索结果 | ★★ |
| **字节豆包(火山方舟)** | Volces 北京 IP | +86 + 实名(个人/企业均可) | 全模型 50 万 tokens/天 + 邀请活动 3625 万 tokens | Web Search 联网内容插件 + Function Calling | ★★★ |
| **Moonshot Kimi** | `api.moonshot.cn`(中国) **+ `api.moonshot.ai`(海外端点存在)** | 国内版要实名;海外版门槛未公开明证 | 注册赠送 + 按量付费 | **`$web_search` 工具内置**,触发不完成只收 ¥0.03 工具费 | ★★★★ |

## 每家具体发现

### DeepSeek(★★ —— 可达性最好但搜索能力为零)
**唯一一家域名解析到海外 CDN**(CloudFront `3.173.21.63`),理论上海外调用延迟最低。但 (a) 2025-01 起官方限制为仅 +86 手机号注册(攻击应对),(b) **API 不自带联网搜索**,Function Calling 是 OpenAI 兼容形式但执行函数要你自己实现 —— 这恰恰违背我们用国内 AI 抓大陆页面的初衷。不适合 X2 路径。

### 智谱 BigModel(★★★★★ —— 综合最优)
2025 年发布"全系列 AI 搜索工具",分三层:Web Search API(基础检索)、Web Search in Chat(问答增强,直接塞 Completions)、Search Agent(智能体)。**后端可切 Bing/搜狗/夸克/Jina.ai** —— 这是 5 家里唯一公开多搜索引擎切换的。GLM-4-Flash 永久免费 + 新人 2000 万 token,价格 GLM-4.6 为 5 元/百万 token。门槛是 +86 实名。返回是 snippet 还是正文未在二手源中找到明确描述(WebFetch 官方文档被 403,需要进一步自验)。

### 通义千问 / 阿里百炼(★★★ —— 干净但有地域坑)
`enable_search=True` 一键启用,或用 `tools` 加 `web_search`;还提供 MCP WebSearch 端点 `https://dashscope.aliyuncs.com/api/v1/mcps/WebSearch/mcp`,免费 2000 次/月。**陷阱**:免费额度只覆盖"中国内地版"和"新加坡版"模型,国际版本身无免费;阿里云国际站要求非大陆手机号 —— 与国内站手机号要求互相排斥,**两边只能选一**。

### 百度文心 / 千帆(★★ —— 能用但平庸)
`web_search` 作为请求 body 参数,搜索引擎默认是百度搜索 —— 百度搜索在大陆页面覆盖上和必应/搜狗/夸克差别不大,但开发体验和文档评价一般。注册门槛与其他大陆厂一致。免费额度需要看具体活动,不如智谱稳定。

### 字节豆包 / 火山方舟(★★★ —— 量大稳定)
"Web Search(联网内容插件)"独立文档项,设计成 Function Calling 调用的工具,doubao-seed-1-6 系列原生支持。**50 万 tokens/天的免费推理额度**(注意是每天)对短期 demo 非常友好。门槛 +86 实名。返回内容格式没在二手源拿到细节。

### Moonshot Kimi(★★★★ —— 海外端点是杀手锏)
关键发现:**`api.moonshot.ai` 是官方海外端点**(对比 `api.moonshot.cn` 国内端点),平台 URL `platform.moonshot.ai` 同样存在。`$web_search` 是内置工具,触发但未完成只收 ¥0.03,正常使用按 token 计费。海外端点的注册流程是否豁免大陆手机号 —— **二手源未给明证,但海外端点的存在本身就值得 PM 花 10 分钟亲自试一次**(不需要充值就能看注册页要不要中国手机号)。

## 给 PM 的具体建议

- **如果走 X2 路径(LLM 联网搜),首选智谱 BigModel**。理由:(a) 搜索栈最完整、(b) 后端可切夸克/搜狗/Bing 多个引擎、(c) GLM-4-Flash 永久免费可以无成本试跑、(d) 二手源里中文社区报告最多文档最清晰。代价:必须 +86 + 身份证实名。
- **反向发现:DeepSeek 看似海外友好实际不行**。它是唯一走 CloudFront 的(可达性最好),但**不自带联网搜索** —— 它不能解决我们"用国内 AI 抓大陆页面"的核心需求。如果只是要海外低延迟通用 LLM,DeepSeek 仍是好选择,但与本调研目标无关。
- **反向发现 2:阿里云国际版是死胡同**。手机号要求与免费额度要求互相排斥(国际版要非大陆手机、但只有内地/新加坡版有免费 token)。
- **如果你愿意接受"+86 手机号 + 身份证实名 + 充值 ≤50 元"**:走智谱 BigModel,2000 万 token 体验包够跑整个 M0+M1 demo,可能完全不用充值。
- **如果你不愿意上述任一**:
  - 先花 10 分钟亲自打开 `platform.moonshot.ai`(海外端点),看注册页是否接受海外手机号 / 邮箱。如果接受 → Kimi 海外版是唯一路径
  - 否则只能走 B(你国内时段手动)或 X1(商业 IP 代理 + 海外身份证开国内号 = 灰色)
- **沙箱限制不可绕过**:不管选谁,**这个沙箱内 curl 都返回 host_not_allowed**。最终接入需要在 PM 的本地机器、或一台没装该 egress proxy 的环境跑。这是 Builder 接 ADR-006 时必须前置解决的问题。

## 不确定 / 未自验

- 智谱 web_search 返回的是完整网页正文还是 snippet:官方文档 WebFetch 被 403,二手源没明说,**需要 PM 本地试一次**
- Kimi 海外端点 `api.moonshot.ai` 的注册是否豁免大陆手机号:**关键未知**,二手源无明证,值得 PM 10 分钟亲验
- 火山方舟 Web Search 插件返回格式未在二手源拿到
- 各家免费额度的"实名前/实名后"边界:多数二手源不区分,可能领免费 token 前就要实名 —— 这会触发 T3 红线,**注册任何账号都需先 escalate PM**
- 沙箱 egress 白名单是否可申请加入:这是 harness/平台层问题,不在 Researcher 职责内

## 与上次报告 `2026-05-18-discovery-pipeline-feasibility.md` 的衔接

上次报告认定大陆馆方/Wayback 在本沙箱 100% 403。本次确认:**国内 LLM API 在本沙箱同样 100% 403**(同一拦截层)。所以"用国内 AI 帮我们抓大陆页面"这个 X2 路径,**无论选哪家厂商,都需要先解决沙箱出口问题**,这是先决条件,不是细节。Builder 写 ADR-006 时应把这个作为 P0 风险。
