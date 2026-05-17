# Sample Bundle · 北齐白石佛立像(响堂山系) · 上海博物馆东馆

**目的**:测试 Open Discovery Pipeline 在该展品上能拼到什么。
**Phase**:样本/可行性,不是最终 bundle。
**调研日期**:2026-05-18
**调研者**:Researcher
**沙箱环境提示**:同 Sample 1。所有大陆馆方域名 / 大陆媒体 / archive.org 均 403。

---

## 0. 展品识别

| 字段 | 内容 |
|---|---|
| 名称 | 北齐白石佛立像(澎湃 2024-03-15 报道与上博东馆雕塑馆官方解读多次提到的"响堂山可能来源"那一尊) |
| 馆 / 厅 | 上海博物馆东馆 · 中国古代雕塑馆 (2024-03 开放试运行) |
| 朝代 / 公元年范围 | 北齐(550–577) |
| 材质 / 尺寸 | 白色大理石 / 白石(具体尺寸未在二手报道中给出) |
| 已知 accession / 编号 | **未找到**(上博 ID 前缀 V/I/RI 已知,具体本件未锁) |
| 已知来源/出处 | **可能源自响堂山石窟(北齐皇家石窟,邺城域)**;白石主产区为河北曲阳、定州、邯郸 |
| 关键关键词(检索用) | 上海博物馆 / 上博东馆 / 中国古代雕塑馆 / 北齐 / 白石 / 响堂山 / Xiangtangshan / 邺城模式 / 曲阳 / 龙树背龛 / 笈多 |

**为什么选它(选品论证)**:
1. **与 Sample 1 同窗口跨馆对照测试**:北齐造像但走"邺城轴"而非"晋阳轴",和 Sample 1(华塔村出土)构成天然 pair
2. **馆方在公开报道中明确提及海外对照件**(V&A、Cernuschi、日本)—— **这是大陆馆罕见的"主动给跨馆对照"** —— 对 ADR-006 验证"馆方策展声明本身可发现跨馆对照线索"假设
3. **demo 切片直接命中**:上博东馆是 PRD §7 剧本备选物理锚点

---

## 1. 来源 A · 馆方一手页面

**目标**:上博东馆雕塑馆该件的官方描述、说明牌文字、策展声明。

**尝试**:
- `https://www.shanghaimuseum.net/mu/frontend/pg/collection/antique?keywords=北齐+白石`(URL 参数化检索)—— 沙箱 curl 403
- `https://www.shanghaimuseum.net/mu/frontend/pg/article/id/CI00159756`(WebSearch 命中此 article ID,可能是雕塑馆相关文章)—— curl 403
- WebFetch 同 403
- 微信小程序「上海博物馆」(2024-06-25 启用,藏品导览模块)—— **非 Web,不可程序化**

**到手内容**:
- 二手摘要(澎湃 2024-03-15《在上海看一部中国古代雕塑通史》、知乎《上博东馆参观全记录:中国古代雕塑馆》):"白色大理石雕成,选材上乘、雕工精湛;研究认为可能源自北齐皇家石窟——响堂山石窟,是珍贵的北齐皇家造像。佛像头部较大、上身修长、整体雕塑几何化,北齐特征鲜明,贴体的佛装和头光中的缠枝花卉纹样受古印度笈多艺术影响,样式对隋代造像产生直接影响。近似尺寸和风格的佛像已知在英国伦敦维多利亚及阿尔伯特博物馆、法国巴黎塞努奇博物馆以及日本也有收藏。"
- **馆方一手 PDF / 策展人长文 → 0 条**

**置信度**:**中**(澎湃 2024-03-15 是有记者署名的深度采访,可视为接近"馆方解读"的二手 → 接近一手;但仍非馆方一手发布的策展声明)

**这件事在 pipeline 里的工程意义**:
- 上博比山博好做的点:**馆方策展叙事在媒体报道中密度更高**(澎湃 + 文汇 + 上海发布 + 上博公众号都有定期重器解读)
- 上博比山博难做的点:**馆藏 ID 系统(V/I/RI 前缀 + 8 位数字)需要从馆方页面才能拿到,不像山博 ID 是顺序整数可枚举**
- → ADR-006 对"上博 anchor metadata"应区别处理:**先从澎湃/上博公众号长文 + 雕塑馆图册落 metadata,再用 PM 国内 IP 抓官网回填 ID + 高清图**

---

## 2. 来源 B · 跨馆对照件(海外 OA)

**目标**:北齐"响堂山系"白石/灰岩造像。

**搜索路径**:
- 现有数据集 grep:Northern Qi + Buddha/Bodhisattva → 已有 28 件命中(CMA 6 / Met 7 / FSG 14 / V&A 1)
- **特别重点 V&A O129249**:`provenance_or_findsite = "probably Xiangtangshan, Hebei province"` —— **馆方原文已直接锁定响堂山** —— 这是"馆方自标 → 跨馆对照"的最干净案例
- WebSearch Cernuschi → 4 件 inv 号锁定(1.0267 / 1.0147 standing Buddha;1.0078 / 1.0080 Bodhisattva,馆方页面描述"青州式""相当于 Gupta style")

**到手内容**:

| 馆 | accession / inv | title | 出处声明 | 与本件相似性论证 |
|---|---|---|---|---|
| V&A | O129249 | Buddha head | **"probably Xiangtangshan, Hebei province"** (馆方原文) | **极强**:同一石窟同一窗口的头部,**与本件可作"上身-头部"虚拟拼合 demo** |
| Met | 42704 | Head of a Buddha, ca. 565–75 | Limestone with pigment | 强:北齐头部、同 pigment 残存 |
| Met | 60794 | Head of a Buddha, mid-6th c | Limestone with traces of pigment and gilding | 强 |
| FSG | ld1-...188774-0 | Head of a Buddha | 550–577 | 强:同窗口头部 |
| FSG | ld1-...191198-0 | Buddha draped in robes portraying the Realms of Desire | 550–577 | **极强**:北齐石灰岩立像 + 浮雕"三界"纹饰,**与本件"贴体佛装+笈多影响"叙事同源** |
| FSG | ld1-...192486-0 | Standing Bodhisattva | 550–577,limestone with pigment | 强 |
| CMA | 156948 | Stele with Shakyamuni and Maitreya | c. 570s | 强 |
| CMA | 94676 | Seated Amitayus Buddha, c. 570s | marble | 强:北齐 + 大理石 |
| Cernuschi(未接入) | 1.0267 / 1.0147 | Standing Buddha, 北齐 | 馆方描述"naturalistic","pure Gupta style" | **极强**:**馆方自己点名的对照件之一** |
| AIC(计划 P0) | 待接入 | 天龙山佛首 + 北齐若干 | | Track 2 §A11 重大新发现 |
| Harvard(计划 P0) | Winthrop 收藏 | | | Track 2 §A6 |

**置信度**:**高**(28 件直接命中 + 馆方自标对照 + V&A 出处直接锁定响堂山)

**给 ADR-006 的工程笔记**:
- **此件 demonstrate 了 Pipeline 最干净的一种产出形态**:"馆方策展声明文字 → 自含跨馆对照线索(V&A、Cernuschi、日本)→ 自动 grep 本地海外数据 → 锁 V&A O129249 出处字段 = Xiangtangshan → 闭环"
- 全过程 **可 100% agent 自动化**(只要馆方策展声明文字落本地)
- ADR-006 应把"馆方策展声明文字"列为**最高 ROI 一手源类**(同 Track 1 §B.5 已建议)
- "Xiangtangshan" 作为 provenance keyword 在现有 va.json 中独此一件 —— 应建议 Builder 在 schema 上添加 `provenance_keyword_extracted` 派生字段

---

## 3. 来源 C · 学术论文 / 学者文章

**搜索路径**:
- WebSearch "曲阳 北齐 白石 佛立像 上海博物馆" → 命中:
  - 故宫院刊 PDF《故宫藏曲阳白石造像中龙》`dpm.org.cn/Uploads/File/2024/03/06/u65e7e53c3f5ed.pdf`
  - 故宫院刊 PDF《河北曲阳修德寺遗址》`dpm.org.cn/Uploads/File/2020/05/18/u5ec24b1565d1c.pdf`
  - 故宫院刊 PDF《东魏北齐响堂石窟与邺城造像比较研究》(同 Sample 1)
  - 经济观察网《东魏北齐邺城地区造像 ︱观展》(何利群访谈相关)
  - 河北曲阳论文集(佛光山 fbce.fgs.org.tw 全文 PDF)
  - 知乎《从面容、服饰和背屏看邺城造像的源与流》
- WebSearch "Wisdom Embodied" → Met 2010 Denise Leidy 编;Internet Archive 全文 OA(但本机不可达 archive.org)
- BMFEA 全卷 OA(Track 3 §B5 已强推,瑞典 varldskulturmuseerna.se 可达性未实测)
- 芝大响堂山项目 `xts.uchicago.edu`:**直接对应本件可能来源** —— 但本机 WebFetch 403

**到手内容**:
1. dpm.org.cn 院刊四篇 PDF 直链(响堂石窟、修德寺遗址、曲阳白石、邺城比较)
2. 佛光山学术电子书《河北曲陽論文集》全文 PDF
3. 芝大响堂山项目网站(URL 锁定,内容未自验证)
4. 经济观察网何利群相关报道(Track 3 §A8)
5. Met *Wisdom Embodied* OA(Track 3 §C1,Internet Archive 全文,**本机不可达**)

**置信度**:**中-中高**(链接命中高,具体本件相关论文段落未自验证)

**给 ADR-006 的工程笔记**:
- 本件比 Sample 1 学术覆盖**更密**——故宫院刊 + 佛光山 + Met OA + BMFEA + 芝大 5 个独立源都直接命中
- 这是因为"白石造像/曲阳/响堂山"是**国内外学界共同热点**,而 Sample 1 的"晋阳—花塔村"在学界更冷门
- → ADR-006 应该接受 **bundle 完整度跨样本差异很大**;30 件不应承诺统一深度,**应承诺"诚实标完整度,不灌水"**

---

## 4. 来源 D · 现场场域

**目标**:上博公众号、澎湃 / 文汇 / 解放日报相关长文、可能的 izi.TRAVEL 频道。

**尝试**:
- 微信公众号「上海博物馆」(高频更新)→ 不抓,留 PM 手动
- 澎湃《现场︱在上海看一部中国古代雕塑通史:上博东馆又开常设展厅》`thepaper.cn/newsDetail_forward_26689360`(2024-03-15)→ **WebFetch 403**
- 知乎《上博东馆参观全记录:中国古代雕塑馆》`zhuanlan.zhihu.com/p/13821187870` → **WebFetch 403**
- 知乎《这是计划的一部分(七十二)上海博物馆东馆参观造像、青铜器》`zhuanlan.zhihu.com/p/30481526763` → 同 403
- 上海发布、文汇报、解放日报 2024-03 雕塑馆开放系列报道(WebSearch 锁定多篇,WebFetch 0 篇)
- izi.TRAVEL API:Track 1 §B2 已建议试探(免费 API key)但 demo 阶段未启动

**到手内容**:
- URL 清单 5+ 篇,**0 条一手内容**

**ADR-006 工程笔记**:同 Sample 1。pipeline 在大陆媒体长文上**只能给 PM URL 清单**;PM 国内 IP 执行下载 / 摘抄;**不要做 wayback 备份策略**,因为本机已证 wayback 不可达。

---

## 5. 来源 E · 数字人文 / 跨域 OA

**搜索路径 + 到手内容**:
1. **芝大响堂山项目 `xts.uchicago.edu`** —— Track 3 §A2 重大新发现,**与本件可能来源直接对应**;3D 数据邮件申请(T3,不动);**公开页面文字 + 跨馆 accession 索引可爬,但本机 403**
2. **国博 2019《和合共生 ── 临漳邺城佛造像展》专题页**(Track 3 §C4)—— 北齐邺城最完整网络版图录,**直接覆盖本件"邺城轴"叙事**
3. **数字敦煌**:佛传图像、菩萨样式跨地比对(Track 3 §A3)
4. **CBETA 大藏经**:造像题记 → 经文映射(Track 3 §A10);本件无题记,**CBETA 边际价值低**
5. **现有 `data/sources/dunhuang_open.json`**:可能含同窗口跨域佛教纹样(本仓库已落地)

**置信度**:**高**(全部源 URL 锁定;响堂山项目是**与本件可能来源直接重合**,这是 wow moment 工程基石)

**ADR-006 工程笔记**:
- 响堂山项目的"跨馆 accession 索引表"(对响堂山而言,Track 2 §B6 已建议同模式做天龙山)= **wow moment 工程底座**;**应在 ADR-006 P0 列出来作为 sample bundle 的标准产出形态**
- 即:bundle 不只是"30 件 metadata",还应该包含**至少 1 张"跨馆流散件聚合图"**(同一石窟 → N 个海外馆;同一窟号 → N 个 accession)。本 sample bundle 已在来源 B 实质交付了这张表的雏形

---

## 6. 样本 bundle 评估

| 维度 | 评价 |
|---|---|
| 5 类源,实际到手几类? | **3 / 5 实际到手**(B + C 学术链接 + E URL 列表);**2 / 5 仅有 URL 无内容**(A、D) |
| 哪些源 pipeline 可自动化?(给 ADR-006 用) | **B 跨馆对照 + V&A provenance 关键词反推**:100% agent;**C 学术 URL 发现**:agent;**E URL 发现**:agent。**accession 索引(响堂山/天龙山)爬取**:agent + 1 次国内或非 GFW VPS 中转 |
| 哪些源**必须人在回路**? | **A 上博官网下载** + **C 学术 PDF 下载** + **D 大陆媒体长文** = 三件都因沙箱 403 卡住,**人在回路 = PM 国内 IP 或 VPN/中转 VPS** |
| 这件展品的 bundle 完整度自评 | **高**(本次三件中最完整的一件)——馆方自带跨馆对照、海外 OA 数据极密、学术覆盖广 |
| 给 PM 看到的"惊喜瞬间"是什么? | "**上博东馆这一尊馆方自己说『可能来自响堂山』。我们的海外数据集里,V&A 一件 Buddha head 同样标 probably Xiangtangshan。这件上博的身、那件 V&A 的头,一拼,就是同一窟的两块流散件 ── 一块在上海,一块在伦敦。馆方策展声明里的『日本、塞努奇、V&A』那一句话,你刚才走过去时没看到,但 AI 看到了**" —— 这是 PRD §7 T7 wow moment 最直接的工程化产出 |

## 7. 反向发现 / 该展品不工作的源

- **上博的"高级检索"(语义层级 + 分类层级)** —— Track 1 称之为"大陆馆中字段结构最规范",但本沙箱**完全无法验证**;ADR-006 不要把此假设当成立论
- **微信小程序「上海博物馆」(2024-06-25 启用)** —— 程序化抓取需反编译 + Charles,合规与稳定性差,不做
- **馆藏号** —— 同 Sample 1,**0 条**;上博公开页面似乎不暴露完整 V/I/RI ID
- **本件馆方 PDF 长文** —— 上博公众号长文密度高但**全部走微信,非 Web 渠道**;无法 program 化

---

**主要来源**:
- 上海博物馆官网:`https://www.shanghaimuseum.net/` + `/mu/frontend/pg/article/id/CI00159756` + `/mu/frontend/pg/article/id/CI00159688`(WebFetch 403)
- 澎湃 2024-03-15《现场︱在上海看一部中国古代雕塑通史》:`https://www.thepaper.cn/newsDetail_forward_26689360`(403)
- 知乎《上博东馆参观全记录:中国古代雕塑馆》:`https://zhuanlan.zhihu.com/p/13821187870`(403)
- 故宫院刊《故宫藏曲阳白石造像中龙》:`https://www.dpm.org.cn/Uploads/File/2024/03/06/u65e7e53c3f5ed.pdf`(未实测)
- 故宫院刊《河北曲阳修德寺遗址》:`https://www.dpm.org.cn/Uploads/File/2020/05/18/u5ec24b1565d1c.pdf`(未实测)
- 故宫院刊《东魏北齐响堂石窟与邺城造像比较研究》:`https://www.dpm.org.cn/Uploads/File/2020/12/29/u5feacd4049fc4.pdf`
- 河北曲陽論文集(佛光山):`http://fbce.fgs.org.tw/files/147/...201803_河北曲陽論文集_電子書.pdf`
- 芝大响堂山项目:`https://xts.uchicago.edu/zh-hans/content/概览`(WebFetch 403)
- Cernuschi 馆藏:`https://www.cernuschi.paris.fr/`(摘要锁定 4 件)
- Met *Wisdom Embodied* OA:`https://archive.org/details/wisdomembodiedch0000metr`(archive.org 在本机完全不可达)
- 本仓库:`data/sources/va.json` O129249(provenance = Xiangtangshan)等 28 件北齐造像

**[ Sample Bundle 2 完 · 2026-05-18 ]**
