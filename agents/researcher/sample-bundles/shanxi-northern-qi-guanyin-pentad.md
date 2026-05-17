# Sample Bundle · 北齐观音菩萨五尊像 · 山西博物院

**目的**:测试 Open Discovery Pipeline 在该展品上能拼到什么。
**Phase**:样本/可行性,不是最终 bundle。
**调研日期**:2026-05-18
**调研者**:Researcher
**沙箱环境提示**:本机 IP 对所有大陆馆方域名 + 多数大陆媒体域名(thepaper.cn、qq.com、sina.com、163.com)以及 archive.org 全部 403(WAF host_not_allowed)。所有"直链验证"实际是 WebSearch 摘要;**未实测站点字段密度**。

---

## 0. 展品识别

| 字段 | 内容 |
|---|---|
| 名称 | 观音菩萨五尊像(贴金彩绘砂石五尊像) |
| 馆 / 厅 | 山西博物院 · 历史展线"佛风遗韵" · "北朝风貌"单元 |
| 朝代 / 公元年范围 | 北齐(550–577) |
| 材质 / 尺寸 | 砂石 + 贴金彩绘;高 60cm,长 41cm,宽 17cm(基于二手报道,未官方核对) |
| 已知 accession / 编号 | **未找到馆藏号**(山博官网藏品详情页 `shanximuseum.com/sx/collection/detail/id/{N}` 在本环境 403,无法枚举核对) |
| 出土 | **1954 年 太原 华塔村(花塔村)** 寺院遗址 |
| 关键关键词(检索用) | 山西博物院 / 北齐 / 观音菩萨五尊像 / 双树背光 / 龙树背龛 / 贴金彩绘 / 华塔村 / 太原 / 邺城模式 / 晋阳 |

**为什么选它(选品论证)**:这是山博"佛风遗韵"展厅"北朝风貌"单元被多家媒体反复提到的"标志重器"之一(腾讯展馆分享、新浪博客、知乎《我眼中的那些馆藏珍宝》同时点名);**与海外馆已知北齐"龙树背龛"式造像窗口高度可比**(详见来源 B);**出土于晋阳(北齐别都),正是邺城—晋阳两轴中"晋阳轴"的核心实物证据**,对原则 D"知识结构网络"是天然抓手。

---

## 1. 来源 A · 馆方一手页面

**目标**:拿到山博对该件的官方描述、说明牌文字、策展声明。

**尝试**:
- `https://www.shanximuseum.com/sx/collection/detail/id/{N}` —— **沙箱 curl HTTP 403**(WAF host_not_allowed);WebFetch 同上;**未在本机直链验证**
- `https://www.shanximuseum.com/sx/exhibition/exhibition/id/4079`(佛风遗韵展览页)—— 同上 403
- `https://sxwwszbwg.chwhyun.cn/`(省级数字博物馆,可能也覆盖此件)—— 同上 403
- Wayback Machine `web.archive.org` —— WebFetch "Claude Code is unable to fetch from web.archive.org",**整个 wayback 在本环境不可用**
- WebSearch 拼 site:shanximuseum.com —— 命中山博官网藏品 ID 索引(如 8210),证实 URL pattern 可枚举,但**单件具体内容未拿到**

**到手内容**:
- 二手摘要(腾讯展馆分享 2023-09-07、新浪《佛风遗韵展厅》系列博客)统一描述:"砂石质贴金彩绘 / 透雕双树背光 / 高浮雕伎乐飞天及二龙奉塔 / 主尊观音菩萨头戴华冠身佩璆珞 / 北齐菩萨造像精品"
- **馆方原始策展声明(展览前言、单元导语、说明牌文字 OCR、馆方策展人长文)→ 在本环境 0 条获取**

**置信度**:**低-中**(基于多家二手报道一致,**不是基于馆方一手文字**)。这正是 Track 3 §D1 已记录的"山博的策展立场只能通过二手报道反推,馆方没有公开的策展声明文档"的具体落地证据。

**这件事在 pipeline 里的工程意义**:
- 在沙箱环境,馆方一手页面对大陆馆是 **完全堵死的路**(本次三件展品中所有大陆馆方源都重现 Track 1 §C9 的 403)
- ADR-006 必须把"大陆馆方页面抓取"定义为 **「人在回路(PM 国内 IP 执行)」**,不是 agent 自动化任务
- 给 PM 留一个明确的 scraping plan:**国内 IP 下** `curl https://www.shanximuseum.com/robots.txt` 先核合规;然后枚举 `/sx/collection/detail/id/{N}` 或在展览页 id=4079 抓取展品列表 → 落 30 件 anchor metadata。**爬虫脚本本身 agent 可写**,但**执行必须移交国内 IP**。

---

## 2. 来源 B · 跨馆对照件(海外 OA)

**目标**:在 CMA / Met / FSG / V&A / Cleveland / 计划接入的 AIC + Harvard + Cernuschi 中找北齐"龙树背龛"或同窗口造像。

**搜索路径**:
- `python3` grep 现有 `data/sources/{cma,met,smithsonian_fsg,va}.json`,过滤 `dynasty_en` 含 "Northern Qi" + 标题含 "Buddha/Bodhisattva/Buddhist"
- WebSearch "Cernuschi museum Northern Qi white marble Buddha standing limestone Paris collection" → Cernuschi 4 件 inv 号确认
- WebSearch 反向参考(Met *Wisdom Embodied* 2010 Denise Leidy 编)

**到手内容(候选对照件清单)**:

| 馆 | source_id / accession | title | 朝代 | 与本件相似性 |
|---|---|---|---|---|
| CMA | 156948 | Stele with Shakyamuni and Maitreya | c. 570s 北齐 | **强**:石灰岩 + 浮雕菩提树背屏,造像组群构图同窗口 |
| CMA | 137218 | Bodhisattva Guanyin | late 500s–early 600s | **强**:同名观音造像 + 砂石 + 残存彩绘,**单件版的本件主尊** |
| CMA | 105881 | Head of Buddha | c. 570 | 同 city/同窗口的造像头部对照 |
| Met | 42718 | Bodhisattva, probably Avalokiteshvara (Guanyin) | ca. 550–560 | 砂石 + 彩绘,北齐观音单件 |
| Met | 39757 | Votive stele with Buddha and bodhisattvas | mid-6th c | 石灰岩 + 彩绘 + 贴金,与本件构图原型最接近 |
| FSG | ld1-...191186-0 | Gathering of Buddhas and bodhisattvas | 550–577 | 大型石灰岩多尊像构图同窗口 |
| FSG | ld1-...191198-0 | Buddha draped in robes portraying the Realms of Desire | 550–577 | 北齐石灰岩立像(无观音,但是"邺城模式"代表) |
| V&A | O129249 | Buddha head | 550–577 | **极强**:probably **Xiangtangshan**,Hebei,出土区与本件"晋阳—邺城"风格圈直接相连 |
| Cernuschi(待接入) | inv. 1.0267 / 1.0147 / 1.0078 / 1.0080 | Standing Buddha / Bodhisattva | 北齐 | **关键互补**:巴黎,**非英语世界对照**,inv.1.0078 被馆方描述为"青州式" |

**置信度**:**高**(现有 5 馆数据中 6 件北齐佛教造像直接命中,Cernuschi 4 件 inv 号在馆方页面摘要中已锁定;但 **Cernuschi 实际数据可达性未实测**,Track 2 §A3 标 Guimet/法国系"暂缓")。

**给 ADR-006 的工程笔记**:
- 现有 `rag_chunks.ndjson` 数据已**够支撑跨馆对照**;Pipeline 在"来源 B"步只需要做 **类目 query** (`dynasty_en=Northern Qi AND tags ⊇ Buddhist`),**纯本地查询,可 100% agent 自动化**,**这是 pipeline 中唯一证明可全自动跑通的一环**
- 单一展品的"对照件候选"产出应是 **agent 输出 top-N 列表 + 相似性论证**;最终入 bundle 的"对照件"由 Curator 决策(那一步保留人在回路)
- Cernuschi 是缺口,值得加入 ADR-006 P1 (Track 2 §D 已写过)

---

## 3. 来源 C · 学术论文 / 学者文章

**目标**:任何讨论"花塔村 1954 出土"、北齐观音五尊像、晋阳—邺城关系的学术文章。

**搜索路径**:
- WebSearch `"花塔村" 太原 1954 北齐` → 命中"1954 年 太原市华塔村出土 北齐石雕观音菩萨像龛"(摘要)、复旦出土文献中心、社科院考古所
- WebSearch `"龙树背龛" 北齐 邺城 山西` → 命中故宫院刊路径下"东魏北齐响堂石窟与邺城造像比较研究"PDF(`dpm.org.cn/Uploads/File/2020/12/29/u5feacd4049fc4.pdf`)、"邺城遗址出土北齐石塔及相关图像的探讨"(kaogu.cssn.cn)
- WebSearch `"邺城" 北齐 白石 佛立像 曲阳 BMFEA` → 命中 BMFEA backlist (varldskulturmuseerna.se),证实 OA 全卷 PDF 在线;**但单卷内具体收录本主题论文需逐卷扫**
- 山西大学云冈学知识库 `ygx.sxu.edu.cn`(Track 3 §B4 已识别) → 命中"青州龙兴寺北齐佛教造像研究"PDF 直链
- Wisdom Embodied(Met 2010) → Internet Archive 全文 OA,**但 archive.org 在本沙箱不可达**

**到手内容**:
1. **故宫院刊半 OA PDF**: `https://www.dpm.org.cn/Uploads/File/2020/12/29/u5feacd4049fc4.pdf` —— 论文《东魏北齐响堂石窟与邺城造像比较研究》。**直链命中,但本机 WebFetch 未实测**(dpm.org.cn 在 Track 1 实测 403)
2. **社科院考古所**: "邺城地区六世纪墓葬的考古学研究" `kaogu.cssn.cn/zwb/xsyj/yjxl/qt/201707/W020180123491024828122.pdf` —— 同直链,可达性未实测
3. **BMFEA 系列**: 通过 `varldskulturmuseerna.se` 全卷可达;**对北齐造像跨地传播主题应有覆盖,但需逐卷扫描** —— 这是 Track 3 §B5 推荐的金矿,但 sample 阶段未具体定位单篇
4. **山大云冈学**: `ygx.sxu.edu.cn/db/学位/D798549.pdf`("青州龙兴寺北齐佛教造像研究"博论)

**置信度**:**中**(链接命中是高置信;具体内容是否覆盖本件 1954 出土叙事 → 未自验证)。

**给 ADR-006 的工程笔记**:
- **学术 PDF 发现**:`site:dpm.org.cn filetype:pdf 北齐` + `site:kaogu.cssn.cn filetype:pdf 邺城` + `site:ygx.sxu.edu.cn filetype:pdf 北朝` → 这三条 query 加 Google CSE,**完全可 agent 自动化**(只要 Google CSE 配额够)
- **学术 PDF 下载**:dpm.org.cn / kaogu.cssn.cn 在本沙箱 403,**实际下载必须移交 PM 国内 IP** —— 同来源 A 边界
- **PDF→ 七字段提取**(ADR-003 已规定):可 agent 化,**但前提是 PDF 已落本地**
- → ADR-006 应把"学术 PDF 源"拆为两步:**步 1 发现(URL 列表)= agent**;**步 2 下载 + 解析 = 半人在回路**(国内 IP 或 PM 离线下载后入仓库)

---

## 4. 来源 D · 现场场域(公众号 / audio guide / 媒体长文)

**目标**:山博公众号、媒体深度报道、izi.TRAVEL 等。

**尝试**(注意:**微信公众号不抓**,平台 ToS 灰区。本任务**不做实际抓取**):
- 微信公众号「山西博物院」:本身不可程序化访问,标 PM 国内手机端订阅 + 关键期手动收材料
- WebSearch "山西博物院 佛风遗韵 北齐 观音五尊像" → 命中:
  - 腾讯展馆分享《展馆分享︱走进山西博物院"佛风遗韵"展厅》(2023-09-07) `news.qq.com/rain/a/20230907A04WHD00` → **本机 WebFetch 403**
  - 新浪博客系列《自驾秋游晋北山西博物院之"佛风遗韵"展》(`blog.sina.com.cn/.../blog_4cbd72290102z5x1.html` 等多篇)→ 同 403
  - 知乎《我眼中的那些馆藏珍宝之山西博物院》`zhuanlan.zhihu.com/p/696076437` → 同 403
  - 三亚博物馆同行刊物对"晋魂"基本陈列分析(Track 3 D1 已找)`sanyamuseum.com` → 同 403
  - 太原日报 2025-12 评论 `epaper.tyrbw.com` → 同 403

**到手内容(推荐 PM 手动获取的链接清单)**:
1. 腾讯展馆分享 2023-09:北齐"观音菩萨五尊像"特写段落
2. 新浪博客《佛风遗韵·上》《佛风遗韵·下》:逐展品图文(博主级深度,但有版权,**不抓,仅 PM 阅读**)
3. 山博公众号往期文章:佛风遗韵展厅升级/重器解读专辑
4. 三亚博物馆同行刊物 2023-05 + 2025-02 对山博"晋魂"陈列升级的同行评论
5. 太原日报 2025-12 "多维度解读佛教文化的融与变"

**置信度**:**低-中**(链接已锁定,**本机 0 条内容到手**;PM 国内 IP 测试是否可达需独立验证)。

**ADR-006 工程笔记**:**这一类源在 pipeline 里的边界 = AI 找位置,人工收材料**。
- agent 自动化部分:Google + WebSearch 拼 site: 限定,产出 **URL + 标题 + 摘要 + 推荐价值**清单
- 人在回路部分:(a) 微信公众号订阅 + 手动收;(b) 大陆媒体长文 PM 国内 IP 浏览 + 拷文 + 入仓库;(c) **绝对不做**:程序化爬取微信公众号(ToS 红线)、付费墙绕过、第三方聚合站直接全量抓
- **这是 ADR-006 应该写进"人在回路"的清单第一条**

---

## 5. 来源 E · 数字人文 / 跨域 OA

**目标**:与本件相关的扩展知识——数字敦煌(同期佛传图像样式)、芝大响堂山项目(同一"邺城模式"圈)、CBETA(造像题记 → 经文)、邺城遗址博物馆(2019 国博临展资料)。

**搜索路径**:
- 现有 `data/sources/dunhuang_open.json`(205 行,小但已落地)
- WebSearch "邺城模式 北齐 响堂山 山西" → 命中 Track 3 §A2(响堂山项目)、§A8(邺城考古队何利群)
- 国博 2019《和合共生 ── 临漳邺城佛造像展》专题页 `chnmuseum.cn/portals/0/web/zt/20190806hhgs/`

**到手内容**:
1. **数字敦煌开放素材库**:北齐佛教纹样、菩萨样式跨地比对的视觉底库(Track 3 §A3,海外 IP 可达 78 国,**未实测本沙箱**)
2. **芝大响堂山项目** `xts.uchicago.edu`(Track 3 §A2):北齐邺城皇家石窟最完整 3D 调查,与本件"晋阳—邺城轴"另一端对照;**本机 WebFetch 403**
3. **国博 2019 临漳邺城佛造像展专题页**:网络版图录,Track 3 §C4 已推 P0;**未实测可达**
4. **响堂山 Smart Museum《Echoes of the Past》巡展资料**(2010–2013):与本件同窗口,Track 3 §A2 重大新发现
5. **山西大学云冈学文献知识库**:北朝佛教研究全文集(Track 3 §B4)

**置信度**:**中-中高**(源已识别,但本机均不可达;响堂山项目是 ADR-003/Curator 报表此前未提到的 Track 3 新发现,需 Curator 补)。

**ADR-006 工程笔记**:
- 这一类源 license 跨度最大(CC0:数字敦煌部分元数据;CC-BY:BMFEA、响堂山项目网页文字;ProjectInternal:芝大 3D 模型)
- **agent 自动化可行度高的**:网页文字 + metadata 抓取(WebFetch + 解析,只要可达);**agent 不可做**:3D 数据邮件申请(T3)、付费授权(数字敦煌商用)
- ADR-006 应把"跨域 OA"分为 **L3.5 海外馆 OA 学术刊物**(新增层,BMFEA + 响堂山 + 芝大 + Met *Wisdom Embodied*)和 **L4 高校仓储**(山大云冈学)两层,Track 3 §B5 已建议

---

## 6. 样本 bundle 评估

| 维度 | 评价 |
|---|---|
| 5 类源,实际到手几类? | **2 / 5 实际到手内容**(B 跨馆对照件 + E 部分元链接);**3 / 5 只到位 URL 列表**(A、C、D 因沙箱与微信封禁,**0 条一手内容**) |
| 哪些源 pipeline 可自动化?(给 ADR-006 用) | **B 跨馆对照件 grep 本地数据集**(100% agent);**A/C/D URL 发现** = WebSearch 拼 site:(85% agent,15% 校验);**学术 PDF 解析** = 仅在 PDF 已落本地时 agent 化 |
| 哪些源**必须人在回路**? | **A 馆方一手页面下载**(大陆 IP);**C 学术 PDF 下载**(dpm.org.cn 国内 IP);**D 微信公众号订阅 + 媒体长文摘录**(国内 IP + 手动) |
| 这件展品的 bundle 完整度自评 | **中**:跨馆对照件极强,但**山博一手叙事 0 条**,基本只能用二手报道反推 |
| 给 PM 看到的"惊喜瞬间"是什么? | "**1954 年从太原华塔村寺院遗址出土的这一件,与你刚刚在 Met / CMA / FSG / V&A / Cernuschi 看到的 6+4 件北齐造像,共同构成的不是『相似』,而是『同一个皇家工坊圈的流散网络』 ——晋阳是北齐别都,邺城是国都,响堂山是邺城皇家石窟,本件出土地正是这条『晋阳—邺城轴』的另一端**" —— 这是 PRD §7 T5/T7 wow moment,**完全由现有海外数据 + 1 条山博出土地信息组合而成**,不需要等 30 件全做完 |

## 7. 反向发现 / 该展品不工作的源

- **山博 / 上博 / 故宫 / 国博 / 国内媒体(thepaper / qq / sina / 163)在本沙箱 100% 不可达** —— Track 1 §C9 重现
- **Wayback Machine 在本环境完全不可用** —— "Claude Code is unable to fetch from web.archive.org",Track 1 给"绕路"留的后门**在本沙箱也走不通**;ADR-006 不能把 wayback 当 fallback
- **馆方"花塔村 / 华塔村"出土地** —— 二手报道两种写法都出现,需 PM 国内拿一手核字(说明牌)
- **馆藏号** —— 整轮调研 **0 条**;山博 ID 系统未公开;**这是大陆馆通病,ADR-006 应把"accession_number"在大陆样本上接受 null,不强制**

---

**主要来源**(每条带访问日期 2026-05-18 + 可达性):
- 山西博物院官网:`https://www.shanximuseum.com/`(本机 403,未实测)
- 山博"佛风遗韵"展览页:`/sx/exhibition/exhibition/id/4079`(同 403)
- 腾讯展馆分享 2023-09-07:`https://news.qq.com/rain/a/20230907A04WHD00`(WebFetch 403)
- 知乎《我眼中的那些馆藏珍宝之山西博物院》:`https://zhuanlan.zhihu.com/p/696076437`(WebFetch 403)
- 新浪博客《自驾秋游晋北山西博物院之"佛风遗韵"展》:`https://blog.sina.com.cn/s/blog_4cbd72290102z5x1.html`(403)
- 中国考古《东魏北齐佛教造像艺术与"邺城模式"》:`http://kaogu.cssn.cn/zwb/kgyd/kgsb/201909/t20190903_4966923.shtml`(未实测,经验性可达)
- 故宫院刊 PDF《东魏北齐响堂石窟与邺城造像比较研究》:`https://www.dpm.org.cn/Uploads/File/2020/12/29/u5feacd4049fc4.pdf`(未实测)
- 山西大学云冈学《青州龙兴寺北齐佛教造像研究》(博论):`https://ygx.sxu.edu.cn/db/学位/D798549.pdf`(未实测)
- 现有本仓库 `data/sources/cma.json` / `met.json` / `smithsonian_fsg.json` / `va.json`(已落地,100% 可读)
- 芝大响堂山项目:`https://xts.uchicago.edu/zh-hans/content/概览`(本机 WebFetch 403)
- Cernuschi 馆藏页:`https://www.cernuschi.paris.fr/`(WebSearch 摘要锁定 4 个 inv 号,未自验证)

**[ Sample Bundle 1 完 · 2026-05-18 ]**
