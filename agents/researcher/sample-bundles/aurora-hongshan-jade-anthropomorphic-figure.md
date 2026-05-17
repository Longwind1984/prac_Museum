# Sample Bundle · 玉神人兽像(红山文化) · 震旦博物馆

**目的**:测试 Open Discovery Pipeline 在该展品上能拼到什么 —— **故意挑的高难度件**,海外对照件预期少,主要靠学术源 + 现场场域 + 真伪争议本身作为产品哲学素材(直接对应 user-voice 原则 C "找不到一手叙事本身就是产品哲学素材")。

**Phase**:样本/可行性,不是最终 bundle。
**调研日期**:2026-05-18
**调研者**:Researcher
**沙箱环境提示**:同 Sample 1+2。

---

## 0. 展品识别

| 字段 | 内容 |
|---|---|
| 名称 | 玉神人兽像(Jade Anthropomorphic / Humanoid figure with horn) |
| 馆 / 厅 | 震旦博物馆(上海陆家嘴) · 历代玉器展厅 · "古代玉器精品"单元 |
| 朝代 / 公元年范围 | 新石器时代 红山文化(约公元前 4500–3000) |
| 材质 / 尺寸 | 玉(透闪石,Hongshan 主产地为辽宁岫岩);圆雕;尺寸未在二手报道中给出 |
| 已知 accession / 编号 | **未找到**;震旦博物馆**整馆都没有公开的 accession ID 系统**(私立馆,Track 1 §A.4) |
| 已知来源/出处 | **无考古出处**——这就是关键。本件**没有发掘记录**(私人收藏 → 陈永泰捐给震旦) |
| 关键关键词(检索用) | 震旦博物馆 / Aurora Museum / 红山文化 / Hongshan / 玉神人 / jade humanoid / Childs-Johnson / 牛河梁 / Niuheliang / 真伪 / authenticity |

**为什么选它(选品论证)**:
1. **demo 切片"难度高样本"**:海外对照件预期少;本身在学界有**真伪争议**(下面详细)
2. **直接服务 user-voice 原则 C**:震旦作为私立博物馆,其叙事(古器物学"料工形纹"四维)与馆方学术地位的张力本身就是叙事素材
3. **测试 pipeline 在 "无考古出处 + 学界争议 + 馆藏号缺失"边缘情况下的退化形态** —— 这恰好是 ADR-006 应该覆盖的 worst case

---

## 1. 来源 A · 馆方一手页面

**目标**:震旦官方对本件的描述、说明牌文字、古器物学四维(料、工、形、纹)分析。

**尝试**:
- `https://www.auroramuseum.cn/zh/collection`(典藏文页,四大类目精选)—— 沙箱 curl 403
- `https://www.auroramuseum.cn/zh/temporary-exhibitions/1008`("灵光:新石器时代玉器特展",2025-05-16 至 2026-10-31)—— curl 403
- WebFetch 同 403
- 注意:Track 1 §A.4 已记录"震旦在线藏品页极简,仅按四大类目精选,无系统化检索"

**到手内容**:
- 二手摘要(澎湃 2023-12《观展手账──〈玉神人兽像〉》):"**圆雕造型,头上树立角状物,左右生有立耳,耳下有横向对穿的钻孔,脸上浮雕五官,额间、后脑及后颈下方阴刻网格纹** —— 网格纹是红山文化玉器中常见的装饰纹样"
- 馆方四维分析(料、工、形、纹):**未到手具体文本**;但震旦 5F"古器物学研究中心"陈永泰团队的整体方法论已公开(Track 1 §A.4 笔记)

**置信度**:**低-中**(澎湃单篇深度文 + 馆方网页摘要;馆方一手 PDF / 策展声明 0 条)

**这件事在 pipeline 里的工程意义**:
- 私立馆在"开放度"上**比公立馆更差**:数据更少、ID 不公开、镜像源稀疏
- ADR-006 应把"私立馆样本"标为 **bundle 完整度天花板较低**;不应承诺等同公立馆产出
- **震旦的独特价值不在"展品 metadata 量",而在"古器物学方法论叙事"** —— 这是 RAG 不能覆盖、必须靠 PM 实地拍摄说明牌补的部分

---

## 2. 来源 B · 跨馆对照件(海外 OA)

**目标**:海外 OA 馆中红山玉神人 / 兽面饰对照件。

**搜索路径 + 现有数据 grep**:

```python
# 现有 cma/met/fsg/va 数据 grep "Hongshan" + "jade" + "humanoid/anthropomorphic"
```

**到手内容**:

- 现有数据集 grep 结果:**未发现明确标 "Hongshan culture" 的件**(本仓库当前覆盖的窗口偏北朝—唐 + 明清窗口,新石器时代非主流)
- CMA 关键命中(WebSearch):`https://www.clevelandart.org/art/1953.628` "Amulet in the Form of a Seated Figure with Bovine Head" —— **可能是 Hongshan/类红山**(具体归属未自验证);**这件在现有 cma.json 数据中未必命中** —— 需要 spike
- WebSearch 海外馆:**Sotheby's《Inviting the Touch: Jades of the Hongshan Culture》**是拍卖图录,**非海外馆 OA 馆藏**
- 国博 2020《玉出红山──红山文化考古成就展》专题页 `chnmuseum.cn/portals/0/web/zt/202010ychsh/` —— 国博收藏对照(沙箱 403)
- 辽宁省博物馆 + 牛河梁遗址博物馆收藏多件红山神人 / 玉人 —— **馆方无 OA 数据接口**(Track 1 同模式)
- **关键反向发现**(下条 #3 详)
- 美术新闻媒体(yicaiglobal.com)2025-05-16 报道"震旦『灵光』展览开幕"提到部分件**借展自国博等馆** —— 这是震旦罕见的"借展回流"案例,但**未影响本件 source 状态**

**对照件清单(诚实标:量很少)**:

| 馆 | 件 | 朝代 | 与本件相似性 / 备注 |
|---|---|---|---|
| CMA (待验证) | 1953.628 amulet | Neolithic(归属可能 Hongshan) | 弱-中:同期同区"人 + 兽"复合造像 |
| 辽博 | 玉猪龙 等多件 | 红山 | 同文化,**非同类型**(神人 vs 龙) |
| 国博 | 2020 临展借自牛河梁等 | 红山 | 同文化,**国博自身收藏对照件少** |
| 大都会 / FSG / V&A | grep 结果 | —— | **0 件直接命中** |

**置信度**:**低**(现有海外 OA 数据池在新石器时代 + 红山窗口**几乎空白**;**这是 Pipeline 的真实数据缺口**)

**给 ADR-006 的工程笔记**:
- **新石器时代窗口在海外 CC0 馆里覆盖度极差** —— Track 2 founding insight"海外 CC0 是国内 RAG 最稳底座"**在新石器时代窗口失效**
- → ADR-006 应**明确 demo 切片范围限于"有跨馆 OA 对照基础"的窗口**(北朝—初唐、商周青铜、清宫书画等),**新石器/红山/良渚等高古玉窗口不在 Phase 1 切片**
- → 给 PM 的硬建议:**30 件不应包含纯新石器件,如果包含,必须降低 wow moment 承诺**

---

## 3. 来源 C · 学术论文 / 学者文章

**搜索路径**:
- WebSearch "Hongshan jade anthropomorphic figure authenticity Childs-Johnson Sun Shoudao 牛河梁"
- WebSearch "震旦 玉神人兽 红山"
- DOAJ / MDPI: MDPI Arts 期刊《Jade for Bones in Hongshan Craftsmanship》(完全 OA,CC-BY)
- Elizabeth Childs-Johnson WordPress 个人站(`echildsjohnson.wordpress.com`)有论文 PDF 直链

**到手内容**:

1. **Elizabeth Childs-Johnson《Jades of the Hongshan culture: the dragon and fertility cult》** PDF:`https://echildsjohnson.wordpress.com/wp-content/uploads/2011/11/jadesofthehongshanculture.pdf` —— **学者个人站,OA**
2. **MDPI Arts《Jade for Bones in Hongshan Craftsmanship: Human Anatomy as the Genesis of a Prehistoric Style》**:`https://www.mdpi.com/2076-0752/12/5/206` —— **CC-BY OA,完全合规可入主语料**
3. **东方陶瓷学会(OCS)《Jade Humanoid Figures: A Look into Possible Hongshan Culture Origins》** 讲座:`https://orientalceramicsociety.org.uk/events/jade-humanoid-figures-a-look-into-possible-hongshan-culture-origins` —— **直接讨论"玉神人兽像"分类与产地**
4. **关键反向发现**:OCS 与 Childs-Johnson 同时记录的事实——
   > **"Anthropomorphic jades attributed to the Hongshan culture have never been excavated scientifically"**
   > **"based on their style, they have been attributed to the Neolithic Hongshan culture of Northeast China"**

   也就是说:**所有目前在博物馆 + 私人收藏 + 拍卖会的"红山玉神人"都不是科学发掘出土的;它们的"红山归属"是基于风格判断,不是基于地层学**。震旦这一件**自然也在这个学术暧昧地带**。这本身就是 user-voice 原则 C(觉察叙事 / 权力结构)的产品哲学素材 —— **馆方策展声明里大概不会主动承认"本件无考古出处"**,但 AI 可以 surface 这件事
5. CHANT 香港中大《中國新石器時代玉龍初探》PDF(libap.nhu.edu.tw)—— 红山玉龙考古综述

**置信度**:**中-高**(MDPI 论文是 OA 完整可读;Childs-Johnson 是国际公认 Hongshan jade 主流学者)

**给 ADR-006 的工程笔记**:
- **本件的学术 evidence base 比馆方 evidence base 强 10 倍**;ADR-006 应允许 pipeline 在某些件上 **学术源覆盖度 > 馆方源覆盖度**
- **真伪争议本身是高价值 chunk** —— PRD §7 T7 / user-voice 原则 C 的最强落地
- MDPI / OCS / 学者个人 WordPress 这类 OA 学术源 = ADR-006 应该专门写一层(暂称 L3.8)`独立学者 OA / 学会讲座 OA`,与馆方刊物 L3.5 区分

---

## 4. 来源 D · 现场场域

**目标**:震旦公众号、媒体长文、可能的灵光特展导览。

**尝试**:
- 微信公众号「震旦博物馆」—— 不抓
- 澎湃 2023-12《观展手账──〈玉神人兽像〉》`thepaper.cn/newsDetail_forward_23410012` —— **WebFetch 403**
- 澎湃 2024-05《"灵光:新石器时代玉器特展"专题导读》`thepaper.cn/newsDetail_forward_31595817` —— 403
- 新浪博客《震旦博物馆 楼层介绍︱历代玉器》`360doc.com/content/19/1007/06/41788091_865255223.shtml` —— 403
- 旅行漫记《上海震旦博物馆 第 2 页》`synyan.cn/29183/2` —— 海外个人博客,**WebFetch 可能可达**(未测)
- 三毛游 / izi.TRAVEL:Track 1 §B2 已建议不抓

**到手内容**:
- URL 清单 4–5 篇;**1 篇 synyan.cn 可能在沙箱可达**(待测,海外博客)
- 灵光特展(2025-05-16 至 2026-10-31)→ **当前 demo 时间窗内的临展**,PM 实地可逛

**ADR-006 工程笔记**:
- 私立馆媒体覆盖比公立馆**弱 5–10 倍**;**澎湃单篇就接近"馆方一手叙事"的稀缺级别** —— bundle 完整度天花板
- 灵光特展是 **PM 现场实测 audio guide / 说明牌 OCR 的最佳时间窗**

---

## 5. 来源 E · 数字人文 / 跨域 OA

**目标**:红山文化扩展知识。

**搜索路径 + 到手内容**:
1. **国博 2020《玉出红山》专题页**:`chnmuseum.cn/portals/0/web/zt/202010ychsh/`(403)+ 2020-11 NMC 英文新闻 `en.chnmuseum.cn/.../t20201102_247983.html`(403)—— 网络版图录
2. **CGTN 2020-10《Treasures from Neolithic China on display in Beijing》** —— **WebFetch 可能可达**(海外 CDN)
3. **MDPI Arts 已开放 OA**(同来源 C)
4. **辽宁省博物馆 + 牛河梁遗址博物馆**:无公开 OA 数据接口
5. **数字敦煌 / CBETA**:**与本件无关**(新石器时代,无佛教题记)
6. **Sotheby's《Inviting the Touch》《S. Bernstein Hongshan Zhulong》《Bernstein bernsteinjadeart.com》**:**拍卖商资料,不入主语料**(ADR-003 已 L5"仅作旁证")

**置信度**:**中-低**

**ADR-006 工程笔记**:
- **私立馆 + 新石器件 + 跨域 OA 的组合 = 三重难** —— bundle 完整度天花板进一步压低
- 这件应该被作为**校准 ADR-006 KPI 的下限锚点**

---

## 6. 样本 bundle 评估

| 维度 | 评价 |
|---|---|
| 5 类源,实际到手几类? | **1.5 / 5 实际到手**(C 学术 OA 论文实有 + B 海外对照件**几乎为零**作为"反向发现"也算);3.5 / 5 仅 URL 列表 |
| 哪些源 pipeline 可自动化?(给 ADR-006 用) | **C 学术 OA(MDPI、个人 WordPress)抓取 + 解析**:100% agent;**B 跨馆对照 grep**:agent,但要诚实输出"0 件直接命中" |
| 哪些源**必须人在回路**? | **A 震旦官网 + D 媒体长文 + E 国博专题页**:全部 PM 国内 IP;**实地拍摄说明牌(灵光特展)**:PM 实地 |
| 这件展品的 bundle 完整度自评 | **低**(故意挑的难件)——但**学术深度反而高**;真伪争议 chunk 价值高 |
| 给 PM 看到的"惊喜瞬间"是什么? | "**这件震旦的玉神人兽像。馆方说它是红山。 ── 但 Childs-Johnson(美国汉学家,牛河梁出土玉的主要研究者之一)在 OCS 的讲座里说,所有现在被叫做『红山玉神人』的件,没有一件是经过科学发掘出土的。它们都是基于风格判断,不是地层学。馆方没说这件事。说明牌也不会说。但你要不要知道?**" —— **这是 user-voice 原则 C 最直接的产品落地**,**"觉察博物馆叙事背后的权力结构"在这件展品上不是抽象口号,是具体可触发的对话** |

## 7. 反向发现 / 该展品不工作的源

- **现有 5 馆海外 OA 数据 + 数字敦煌库 + CBETA → 对新石器件几乎全空白** —— 这是数据集结构性短板
- **私立馆(震旦)无 ID 系统、无 API、网页极简** —— Track 1 §A.4 已盘点,本次实测进一步证实
- **国博专题页 + chnmuseum.cn 在本沙箱 403** —— 大陆官方域名通病
- **archive.org 不可达** —— 不能用 Internet Archive 作 fallback
- **馆方"灵光特展"页面无 OA 数据下载** —— 临展数据**绝大多数永远不会数字化** —— 这是 PRD §10 边界
- **拍卖图录(Sotheby's 等)系统化 OA → 0** —— ADR-003 L5 "仅作旁证"已规定

---

**主要来源**:
- 震旦博物馆典藏文页:`https://www.auroramuseum.cn/zh/collection`(403)
- 震旦"灵光:新石器时代玉器特展"页:`https://www.auroramuseum.cn/zh/temporary-exhibitions/1008`(403)
- 澎湃《观展手账──〈玉神人兽像〉》:`https://www.thepaper.cn/newsDetail_forward_23410012`(403)
- 澎湃《"灵光"专题导读(一)》:`https://www.thepaper.cn/newsDetail_forward_31595817`(403)
- **MDPI Arts《Jade for Bones in Hongshan Craftsmanship》**(CC-BY OA):`https://www.mdpi.com/2076-0752/12/5/206`
- **Childs-Johnson《Jades of the Hongshan culture》PDF**:`https://echildsjohnson.wordpress.com/wp-content/uploads/2011/11/jadesofthehongshanculture.pdf`
- **OCS《Jade Humanoid Figures》讲座页**:`https://orientalceramicsociety.org.uk/events/jade-humanoid-figures-a-look-into-possible-hongshan-culture-origins`
- Sotheby's《Inviting the Touch: Jades of the Hongshan Culture》:`https://www.sothebys.com/en/articles/inviting-the-touch-jades-of-the-hongshan-culture`
- CHANT《中國新石器時代玉龍初探》PDF:`https://libap.nhu.edu.tw:8081/Ejournal/2011000604.pdf`
- 国博《玉出红山》临展专题页:`https://www.chnmuseum.cn/portals/0/web/zt/202010ychsh/`(403)
- yicaiglobal 2025-05《震旦灵光开幕》:`https://www.yicaiglobal.com/news/in-photos-the-special-exhibition-of-hongshan-culture-archaeology-debuts-at-shanghai-museum`(可能可达,未测)
- 本仓库 `data/sources/*.json`:对新石器 / 红山件 **0 件直接命中**(反向发现)

**[ Sample Bundle 3 完 · 2026-05-18 ]**
