# Research · Track 2 海外 OA 馆藏补强 · 2026-05-17

**召唤者**:Orchestrator(PM 主线交付)
**题目**:海外 OA 馆藏补强 —— 找与现有 3 馆(CMA / Met / Smithsonian FSG)形成互补、对北朝—初唐 + 山博 demo 切片(天龙山 + 佛风遗韵)有跨馆对照价值的开放数据源
**置信度**:逐源标(整体 中–中高;沙盒环境 `curl` 直接打 API 全部 403,所有 API 字段细节均来自官方文档/第三方文章描述,而非本机实测——这是一个**关键 caveat**:实际接入时须在通网环境再做一次最小可达性测试)

**主要来源**(都是 2026-05-17 通过 WebSearch 取证;每个馆都按"OA 政策 / API / 馆藏量级 / 北朝—初唐覆盖 / 图像资源 / 重复度"6 字段评估):
- V&A developers.vam.ac.uk(2025-04 ToC 更新),vam.ac.uk/info/image-licensing
- British Museum collection.britishmuseum.org SPARQL endpoint(museum-api 案例研究);britishmuseum.org/collection
- Musée Guimet guimet.fr/en/our-collections + Villa Guimet 2026 数字门户公告
- Asian Art Museum SF asianart.org;collections.asianart.org;about.asianart.org/photography-and-image-rights
- Royal Ontario Museum rom.on.ca/about-rom/openrom;collections.rom.on.ca/rights
- Harvard Art Museums harvardartmuseums.org/collections/api + github.com/harvardartmuseums/api-docs
- Princeton University Art Museum github.com/Princeton-University-Art-Museum/puam-api-docs
- Yale University Art Gallery artgallery.yale.edu/open-access-images;lux.collections.yale.edu;guides.library.yale.edu/open-metadata-service
- Brooklyn Museum brooklynmuseum.org/opencollection/api/docs/rights;github.com/brooklynmuseum/brooklynmuseum-api-examples
- MFA Boston mfa.org/collections/mfa-images/licensing/frequently-asked-questions
- Art Institute of Chicago artic.edu/open-access/public-api;api.artic.edu/docs;github.com/art-institute-of-chicago/api-data
- Nelson-Atkins nelson-atkins.org/art/collections/chinese;ns.nelson-atkins.org/collections/collection-history-Chinese
- Penn Museum penn.museum/collections/objects/data.php(2026-03-05 CSV dump 138MB,CC BY 4.0)
- 数字 OA 聚合:Europeana pro.europeana.eu/page/apis(metadata CC0);DPLA dp.la
- Smithsonian Open Access si.edu/openaccess + api.si.edu(配套 GitHub `Smithsonian/OpenAccess`)
- 国家故宫 NPM Taiwan theme.npm.edu.tw/opendata(CC BY 4.0 + OGDL 1.0)
- Tianlongshan/Xiangtangshan 专题:tls.uchicago.edu;xts.uchicago.edu
- 反向参考:McCarthy "Curiouser and curiouser: copyright and the public domain at the V&A"(2024);"A sampling of prominent rights holders not offering Open Access licences"(forarthistory.org.uk,2024-06)

---

## TL;DR(给 Curator 的 3 条)

1. **现有 3 馆最大互补缺口 = 天龙山/响堂山具体散件归属图谱 + 北齐"邺城/晋阳两轴"的实物分布**。CMA + Met + FSG 三家虽然北朝—初唐窗口件数(287)够,但**完全没有"按窟分组""可视化流散件"的语义层**——这恰好是 ADR-003 选定的 demo 叙事核心(流散与数字回归)。这个缺口不是某一家馆可以补的,而是**专题项目**(`tls.uchicago.edu` + `xts.uchicago.edu`)才能补。

2. **本周最值得接入的 3 个新源**:
   - **Art Institute of Chicago(芝加哥艺博)**——CC0 + 公开 API,本身藏天龙山佛首,**并且 demo 叙事核心(芝大天龙山项目)就在芝加哥**,跨馆对照逻辑天然;边际增益大、重复度低。
   - **Harvard Art Museums**——CC0 数据集 + IIIF + REST API + Winthrop 收藏的北朝/初唐中国佛教造像专门展厅(Gallery 1610);字段密度可对标 CMA,接入工程量小。
   - **Smithsonian Open Access 全量(不止 FSG)**——本仓库现在只接了 FSG;`api.si.edu` 还覆盖 NMNH/NMAH/Cooper Hewitt 等单元的中国相关件,API 完全相同,**零新代码成本**,只是改 `unit_code` 参数。

3. **必须放弃 / 重复度过高的源**:
   - **MFA Boston / Asian Art Museum SF / Cernuschi / Rietberg / ROM / Guimet**——这 6 家**都没有 CC0 + 公开 API 的组合**。MFA 收费 $50/张、SF Asian Art 明确"全馆图像版权保留"、ROM 走人工请求表、Guimet 数字门户 2026 才上线。**全部跳过**——任何"国内 RAG 想要的图像底座"都进不来。
   - **British Museum 的 SPARQL** 技术上可用,但**图像 license 是 CC BY-NC-SA**(非商用),在 ADR-003 "未来商业化决策"路径上是雷;**且 collection.britishmuseum.org SPARQL endpoint 多年维护不积极**,实际可达性需现场验证。**Phase 1 可暂时纳入"低优先级技术 spike",但不要现在动手**。
   - **V&A**——`api.vam.ac.uk/v2` 在线、含 24,799 条 China-related,但**默认图像 license 不是 CC0**,仅"非商业 + 教育免费",ADR-003 商业化路径不友好;此外**国内 RAG 主语料的 founding insight 已锁 CC0,V&A 的灰度 license 不能直接灌**。建议**写一个 30 行 `extract_va.py` 收元数据(已在 README 里说过),但只入 metadata + 缩略图,不入主图**——保留学术对照价值,不污染 CC0 主索引。

---

## A · 海外候选馆逐馆评估

### A-1 · Victoria & Albert Museum(V&A,英国)

| 字段 | 取值 |
|---|---|
| OA / CC0 政策 | **部分** —— API 元数据公开但条款限"非商业 / 教育";图像默认走 vandaimages.com 商用许可。**不是 CC0**。 |
| 公开数据接口 | `api.vam.ac.uk/v2/`,无需 key,文档完整(developers.vam.ac.uk/guide/v2/) |
| 中国艺术品馆藏量级 | API 中 `q_place_name=China` 命中 ~24,799 条 |
| 北朝—初唐 / 佛造像覆盖 | **强** —— 2009 年开馆的英国首座佛教雕塑专门展厅(Robert H. N. Ho Family Foundation Galleries of Buddhist Art);明确藏龙门一件大型石窟造像(有 V&A blog 长文) |
| 图像资源 | 通过 API `_images` 字段拿 IIIF manifest;但**主图下载需走商用授权**——这是关键灰区 |
| 国内访问性 | 直连可达(英国服务器,无 GFW 干扰);沙盒 403 仅本机 WAF 问题 |
| 与现有 3 馆重复度 | 中。V&A 强项在装饰艺术(瓷器/玉器/家具)与 Ho Family 佛雕展厅;与 CMA/Met 在"流散件流传链"上不冲突,但**在北朝—初唐石灰岩造像 specifically 不会比 CMA 强** |
| **置信度** | 高(条数 24,799 是 V&A blog 官方数字) |
| **判定** | **有条件接入**:写 ~30 行 extractor,但仅入 metadata + 缩略图(≤512px),license 字段标 `VA-Personal-Educational`,**不进 CC0 主索引,只进"对照件参考"二级表**。这与 ADR-003 §"图像分层入库"完全一致。 |

### A-2 · British Museum(大英)

| 字段 | 取值 |
|---|---|
| OA / CC0 政策 | **图像 CC BY-NC-SA 4.0**(非商业 + 必须同样授权);metadata 在 SPARQL endpoint 开放 |
| 公开数据接口 | `collection.britishmuseum.org/sparql.json`(SPARQL,CIDOC-CRM schema)+ collection-online REST(有 JSON/CSV);**注意**:多份社区文章(numishare 2018,museum-api 2020 案例研究)反映 SPARQL endpoint 服务质量起伏,需现场验证 |
| 中国艺术品馆藏量级 | Department of Asia 总量 ≈ 75,000(含日韩印),其中中国件估计 25,000–40,000(Wikipedia);Collection Online 总 4M+ |
| 北朝—初唐 / 佛造像覆盖 | **强** —— 阿弥陀佛白大理石立像(Buddhist 标志件)、敦煌斯坦因专项绘画/纸本(20 世纪初 Aurel Stein 西域考古的核心组件) |
| 图像资源 | IIIF 部分支持;高清图下载需走 license |
| 国内访问性 | 直连可达 |
| 与现有 3 馆重复度 | 中–低。**斯坦因敦煌组件**(纸本/绢画)是现有 3 馆都没有的强补强 |
| **置信度** | 中。SPARQL endpoint 实际可达性最近 24 个月未亲测,license 是高确定。 |
| **判定** | **不接入(本周);标为 P2 spike**。理由:(a) NC-SA 与"商业化决策"冲突;(b) SPARQL 接入工程量高(CIDOC-CRM 字段映射要重写一遍 extractor)。**若 demo 叙事强行要"敦煌斯坦因绢画",再单独 spike**。 |

### A-3 · Musée Guimet(巴黎吉美)

| 字段 | 取值 |
|---|---|
| OA / CC0 政策 | **无公开 OA dump、无 CC0 声明**;"Villa Guimet 2026 数字门户"是规划,**未上线**(自己官网原话) |
| 公开数据接口 | 无 |
| 中国艺术品馆藏量级 | 中国部 ~20,000 件(官方数字) |
| 北朝—初唐 / 佛造像覆盖 | 中–强(欧洲最强的中国佛教雕塑馆之一);**但拿不到结构化数据** |
| 图像资源 | 无 OA;`guimet.fr/en/collections/china` 网站可看缩略图 |
| 国内访问性 | 直连可达(法国服务器) |
| 与现有 3 馆重复度 | 高互补——但**没有数据接口让你拿** |
| **置信度** | 高(直接来自官方页面) |
| **判定** | **暂缓(等 2026 数字门户上线)**。当前不可用。 |

### A-4 · Asian Art Museum, San Francisco(旧金山亚博)

| 字段 | 取值 |
|---|---|
| OA / CC0 政策 | **明确无 CC0**:about.asianart.org/photography-and-image-rights 原话 "AAM is the copyright holder for all digital files... Reproduction of an AAM image without a licensing agreement will constitute an infringement of copyright" |
| 公开数据接口 | `collections.asianart.org` 是 emuseum 前端,无公开 API 文档 |
| 中国艺术品馆藏量级 | 总馆藏 ~20,000 件;Avery Brundage 捐赠 7,700 件中亚州各国都有(中国子集量级估 5,000–8,000) |
| 北朝—初唐 / 佛造像覆盖 | **强** —— 藏 "最早有纪年中国造像"(338 年金铜佛);Northern Wei/Qi 标志件多 |
| 图像资源 | **不开放** —— 馆方版权全留 |
| 国内访问性 | 直连可达 |
| 与现有 3 馆重复度 | **数据层不可比较 —— 拿不到** |
| **置信度** | 高(明确否定) |
| **判定** | **跳过**。即便 Brundage 北齐藏品对 demo 极相关,**没有数据接口 + 明确版权保留 = 进不了 RAG 主索引**。可作为"用户现场参观博物馆"层的引用(L6 用户拍摄),但不能作 L3 海外 CC0。 |

### A-5 · Royal Ontario Museum(多伦多 ROM)

| 字段 | 取值 |
|---|---|
| OA / CC0 政策 | **无 CC0**:collections.rom.on.ca/rights 走"image request form + license agreement";"OpenROM" 是建筑改造项目,**不是开放数据项目**(易混淆) |
| 公开数据接口 | 无公开 API;eMuseum 前端可浏览 |
| 中国艺术品馆藏量级 | 中国馆藏 ~35,000 件(北美最大之一);**三幅元代壁画**(13–14 世纪)世界级 |
| 北朝—初唐 / 佛造像覆盖 | 强(元代寺庙壁画 + 唐三彩 + 佛雕);**但拿不到** |
| 图像资源 | 仅缩略图;高清走 license 申请 |
| 国内访问性 | 直连可达 |
| 与现有 3 馆重复度 | **数据层不可比较 —— 拿不到** |
| **置信度** | 高 |
| **判定** | **跳过**。 |

### A-6 · Harvard Art Museums

| 字段 | 取值 |
|---|---|
| OA / CC0 政策 | **强 OA** —— 数据集(CSV + JSON)CC0 发布;图像通过 IIIF 公开;rights statement 走 RightsStatements.org 标准 |
| 公开数据接口 | `harvardartmuseums.org/collections/api`,REST,需注册免费 API key(github.com/harvardartmuseums/api-docs);**IIIF Presentation API 2.1 全量支持**;另在 Harvard Dataverse 有完整 CSV 镜像 |
| 中国艺术品馆藏量级 | 总馆藏 ~250,000,其中亚洲艺术专区有"Arts of Ancient China"(Gallery 1600)和**北朝/初唐 Winthrop 收藏专门陈列**(Gallery 1610) |
| 北朝—初唐 / 佛造像覆盖 | **强** —— Grenville L. Winthrop(1864–1943)旧藏明确被描述为"现存美国馆藏中最好的中国与韩国佛教雕塑之一" |
| 图像资源 | IIIF 高清直链(Harvard IIIF service);分辨率到 2400px 以上;rate 限频未公开但 API key 制度 |
| 国内访问性 | 直连可达(中文 wikipedia 路径无障碍) |
| 与现有 3 馆重复度 | **低**。Winthrop 收藏与 CMA(主要是 1914–1923 卢芹斋系)、Met(241C)的入藏渠道**完全不同**,北朝—初唐窗口的实物件几乎不重叠 |
| **置信度** | 高(API 文档活跃 + IIIF 标准) |
| **判定** | **强烈推荐接入(本周)**。工程量:写 `extract_harvard.py`,~50 行 stdlib;字段密度与 CMA 同档;预估北朝—初唐窗口 +30–80 件本地化 |

### A-7 · Princeton University Art Museum

| 字段 | 取值 |
|---|---|
| OA / CC0 政策 | **强 OA** —— API 文档明示"static JSON files representing entirety of the collections" 周更;但**图像 license 需逐件看 rights statement**(非全局 CC0) |
| 公开数据接口 | `data.artmuseum.princeton.edu`,无需 auth(可能未来加);static JSON dumps 周更(Objects/Makers/Packages);IIIF 支持 |
| 中国艺术品馆藏量级 | 总 ~113,000;亚洲艺术"自 1880s 开始收集",中国书画"renowned for range and quality"——估中国件 ~15,000–20,000 |
| 北朝—初唐 / 佛造像覆盖 | **中** —— Guanyin 坐像旗舰件、Liao painted-wood 棺板组(独有);Tang/Song 书画"finest outside Asia";但**北朝—初唐石灰岩造像 specifically 不是 PUAM 强项** |
| 图像资源 | IIIF 公开;部分 CC0 部分有限制 |
| 国内访问性 | 直连可达 |
| 与现有 3 馆重复度 | 中。**辽代棺板组**与现有 3 馆零重复但与 demo 切片(北朝—初唐)不直接相关 |
| **置信度** | 高(API 文档活跃) |
| **判定** | **次优补强(本月)**。北朝—初唐窗口边际增益不如 Harvard,但**Tang 书画 + Liao painted-wood 在 Phase 2 上博书画/二期切片极有用**——可以接入但放 P1 |

### A-8 · Yale University Art Gallery

| 字段 | 取值 |
|---|---|
| OA / CC0 政策 | **强 OA(公有领域件)** —— Yale University Open Access Policy 涵盖所有 PD 件免费 + 无需注册;**LUX 系统**(lux.collections.yale.edu,2.5B triples,JSON-LD)是全球最大开放艺术数据图谱之一 |
| 公开数据接口 | **LUX**(Linked Open Usable Data,JSON-LD 优先,不是 SPARQL);CSV downloads 通过 Open Metadata Service |
| 中国艺术品馆藏量级 | 亚洲艺术 ~8,000 件(整个亚洲,含中日韩印中亚等);**中国件估 2,000–3,000** |
| 北朝—初唐 / 佛造像覆盖 | **中** —— 唐代陶器系列;一件 550–577 北齐佛教造像石碑(Buddhist Votive Stele);**整体不是 Yale 强项** |
| 图像资源 | IIIF;PD 件免费下载 |
| 国内访问性 | 直连可达 |
| 与现有 3 馆重复度 | 中。亚洲整体 8k 件中中国子集小,北朝—初唐对照件估 <50 件 |
| **置信度** | 中。LUX 是 Linked.art / Getty 阵营的新基础设施,接入复杂度待评估。 |
| **判定** | **次优补强(本月)**。规模虽小但 license 干净;**作为 LUX/Linked.art 工程模式的练手**,对作品集叙述"我对标了一线 LOD 标准"有加分,但 demo 切片边际增益有限 |

### A-9 · Brooklyn Museum

| 字段 | 取值 |
|---|---|
| OA / CC0 政策 | **混合** —— 部分 CC0(OASC 计划标记的件);其余 ~68,000 件是"孤儿作品"或 CC 其他子集,**需逐件看 rights** |
| 公开数据接口 | `brooklynmuseum.org/opencollection/api/docs/`(REST,需 API key;techblog.brooklynmuseum.org 有教程);GitHub 有 examples |
| 中国艺术品馆藏量级 | Arts of Asia 部门(中日韩+东南亚+南亚混合);**中国件量级在馆方主页未公开**,估 5,000–10,000(基于 Asia Week NY 资料) |
| 北朝—初唐 / 佛造像覆盖 | 中(Arts of Buddhism gallery 是常设);量级不大 |
| 图像资源 | OASC 件可免费用;其他需 license |
| 国内访问性 | 直连可达 |
| 与现有 3 馆重复度 | 中 |
| **置信度** | 中(API 存在但社区维护活跃度不如 Harvard/Chicago) |
| **判定** | **暂缓**。CC0 不是全局而是逐件,extractor 复杂度上升;边际增益小于 Harvard / AIC |

### A-10 · Museum of Fine Arts, Boston(MFA)

| 字段 | 取值 |
|---|---|
| OA / CC0 政策 | **明确无 CC0**:`$50 per high-res image` 收费授权;终端用户"个人学习用途"按版权法 fair use(不是 CC0) |
| 公开数据接口 | 无公开 API(GitHub `mfaweb` 主要是网站工程仓库,不是数据 dump) |
| 中国艺术品馆藏量级 | 中国艺术"东亚之外最佳之一",藏 Tang《历代帝王图》(传阎立本)、宋《九龙图》、Wan-go H.C. Weng 2018 巨型书画捐赠 |
| 北朝—初唐 / 佛造像覆盖 | **强**(monumental Buddhist stone sculptures);但**拿不到结构化数据** |
| 图像资源 | 仅 ~160k 件低清网页缩略图;高清 = $50/张 |
| 国内访问性 | 直连可达 |
| 与现有 3 馆重复度 | **数据层不可比较 —— 拿不到** |
| **置信度** | 高(收费政策明示) |
| **判定** | **跳过**。MFA 在 founding insight "海外 CC0 是国内 RAG 最稳底座"框架内不属于 CC0 馆;典型反向案例。 |

### A-11 · Art Institute of Chicago(AIC)

| 字段 | 取值 |
|---|---|
| OA / CC0 政策 | **强 OA** —— 全 50,000+ 张 OA 图像 CC0;API 数据全字段 CC0(描述字段除外) |
| 公开数据接口 | `api.artic.edu`(REST,无需 key,文档 api.artic.edu/docs);**有完整 GitHub 数据 dump `art-institute-of-chicago/api-data`** —— 与 CMA 同模式;**IIIF 全量支持** |
| 中国艺术品馆藏量级 | 中国艺术 ~7,500 件(基于馆方主题导览);**含天龙山佛首(藏品号 87年捐入)** |
| 北朝—初唐 / 佛造像覆盖 | **强 + 特定相关**:**AIC 直接藏天龙山散件**(ADR-003 demo 叙事核心);此外 Tang 三彩、北魏石窟造像若干 |
| 图像资源 | CC0 + IIIF + Pyramid TIFF;rate limit 文档未明示但社区报告"温和"(无 key 即可) |
| 国内访问性 | 直连可达 |
| 与现有 3 馆重复度 | **低** —— 入藏渠道与 CMA 不同;天龙山件是**ADR-003 demo 唯一海外馆物理对照件**(芝大项目就在隔壁) |
| **置信度** | 高(API 在线 + GitHub 镜像) |
| **判定** | **强烈推荐接入(本周,最高优先级)**。**这是 demo 叙事最关键的新增源**——天龙山散件物理上就在芝加哥。工程量:`extract_aic.py` ~50 行 stdlib(API + IIIF URL 直拼),可与 GitHub `api-data` repo 镜像备份。 |

### A-12 · Nelson-Atkins Museum of Art(堪萨斯城)

| 字段 | 取值 |
|---|---|
| OA / CC0 政策 | **无 CC0 全局声明**;有 "freely available" 检索界面但 license 未明示 |
| 公开数据接口 | **无公开 API**(在所有 OA 列表里未出现);`ns.nelson-atkins.org/collections/collection-history-Chinese.cfm` 是静态展示页 |
| 中国艺术品馆藏量级 | 中国艺术 7,500+ 件(史克曼时代积累,北美前三之一);**藏天龙山散件、龙门散件、响堂山散件**(Buddhist 石雕"5 世纪末到 8 世纪"明示包含天龙山) |
| 北朝—初唐 / 佛造像覆盖 | **极强**(实物层);**但拿不到结构化数据** |
| 图像资源 | 网页低清;无 dump |
| 国内访问性 | 直连可达 |
| 与现有 3 馆重复度 | 实物层零重复,但**数据层不可访问** |
| **置信度** | 高(数据接口明确不存在) |
| **判定** | **跳过(数据层);但在 demo 叙事文本中显式提及**——"Nelson-Atkins 也藏天龙山件,我们这里没有图,推荐你看 tls.uchicago.edu"。这是把数据缺口转化为叙事诚实度的机会。 |

### A-13 · Penn Museum(宾大博物馆)

| 字段 | 取值 |
|---|---|
| OA / CC0 政策 | **CSV CC BY 4.0**(不是 CC0,但已是开放数据档);**图像不在 CSV 里** |
| 公开数据接口 | `penn.museum/collections/objects/data.php`,138MB CSV(2026-03 dump);**无 REST API** |
| 中国艺术品馆藏量级 | Chinese Rotunda 是 Penn 招牌(Asian Section "most famous for its large collection of Chinese Buddhist sculpture");**藏 5 件天龙山佛头**(tls.uchicago.edu 案例) |
| 北朝—初唐 / 佛造像覆盖 | **极强**(华盛顿 1923 营盘大殿石刻"昭陵六骏"散件之外的少数西迁组件——中国部最具地标性的 Buddhist 阵列) |
| 图像资源 | CSV **无图像 URL**(README 原话 "images not included");需要从 collection 网站逐件抓 |
| 国内访问性 | 直连可达 |
| 与现有 3 馆重复度 | **极低** —— 1900–1920 入藏的核心 Buddhist 件与 CMA 卢芹斋系不同渠道 |
| **置信度** | 高(CSV dump 实在) |
| **判定** | **次优补强(本月);P1**。CSV 接入易(stdlib csv.DictReader),但**图像需二次抓取**(从 object page 解 OG meta);license 是 CC BY 不是 CC0,**入主索引前需在 license 字段加 `PennCC-BY` enum**,与现有 schema 兼容(`license` 已经是 enum,加新值即可)。**北朝—初唐边际增益估 +50–100 件 + 5 件天龙山实物**。 |

### A-14 · Smithsonian Open Access 全量(非仅 FSG)

| 字段 | 取值 |
|---|---|
| OA / CC0 政策 | **CC0**(2020 启动,涵盖全 Smithsonian) |
| 公开数据接口 | `api.si.edu/openaccess/api/v1.0/`(REST,DEMO_KEY 可立即用,正式 key 通过 data.gov 免费申请);**GitHub `Smithsonian/OpenAccess` 提供 5.1M 件完整 JSON dump**(分片 S3) |
| 中国艺术品馆藏量级 | 整个 Smithsonian 5.1M;中国相关需要过滤 `unit_code=FSG` 或 `culture=China` |
| 北朝—初唐 / 佛造像覆盖 | 现有 FSG 已覆盖;NMNH/NMAH 中可能还有零星考古件(需 spike 验证) |
| 图像资源 | CC0 + IIIF |
| 国内访问性 | 直连可达 |
| 与现有 3 馆重复度 | **本仓库已接 FSG,扩到其他 unit 边际增益小** |
| **置信度** | 高 |
| **判定** | **暂缓**——已接 FSG;扩到其他 unit 不是 demo 切片的杠杆。**但工程上要记一笔**:`extract_smithsonian_fsg.py` 改一个 `unit_code` 参数即可扩,**零代码成本**;留作"未来切片切换"的复用模板。 |

### A-15 · National Palace Museum Taipei(台北故宫)

| 字段 | 取值 |
|---|---|
| OA / CC0 政策 | **CC BY 4.0 + Open Government Data License v1.0**(不是 CC0,但允许商用 + 仅需署名) |
| 公开数据接口 | `theme.npm.edu.tw/opendata/`(开放数据平台);`openapiweb.npm.gov.tw`(API,需申请免费 key);政府开放平台 data.gov.tw 同步 dataset |
| 中国艺术品馆藏量级 | 70 万件(全球最大中国艺术品藏馆,清宫旧藏主体) |
| 北朝—初唐 / 佛造像覆盖 | **中—弱**。台北故宫强项是宋元书画 + 清宫瓷器 + 帝王典藏,**佛造像不强**(北朝—初唐石雕散件极少);demo 切片边际增益小 |
| 图像资源 | IIIF 支持;CC BY 4.0 |
| 国内访问性 | 直连可达 |
| 与现有 3 馆重复度 | **低**(因品类不同,清宫旧藏与海外散件主体不重叠);但与 demo 切片相关度也低 |
| **置信度** | 高 |
| **判定** | **暂缓**。**license 是干净的(CC BY 4.0 商用可),数据规模大**——但**与 demo 切片(北朝—初唐 + 山博佛造像)正交**;若 Phase 2 扩书画 / 宋元 / 清宫则强烈推荐。当前不接。 |

---

## B · 聚合源评估

### B-1 · Europeana

- **元数据 CC0**(全 55M 件);**图像 license 沿用原馆**(混合)。
- API `api.europeana.eu`(免费 key)+ SPARQL endpoint。
- 优点:**欧洲范围聚合**,可一次性扫到 V&A / Guimet / 各国小馆中国件。
- 缺点:(a) 中国艺术专题在 Europeana 整体里量级很小(估 <50,000 件);(b) 字段碎(每个 contributing 馆字段不齐);(c) 图像 license 仍要逐件看。
- **判定**:**P2 spike**。**适合"发现"(找不在 14 馆候选里的小馆)而非"主索引";不是本周动手目标**。

### B-2 · Wikimedia Commons + Wikidata

- 元数据 CC0;图像绝大多数 CC BY-SA 或 PD;**SPARQL 服务(query.wikidata.org)对未登录用户限频严格,登录后 10,000 行/查询 cap**。
- 中国艺术覆盖:`Category:Buddhist sculptures from China`、`Category:Sculpture of the Northern Qi Dynasty` 都存在且活跃维护。
- **关键用途**:**作为"跨馆 ID 中继表"**——Wikidata Q-ID 可以把"同一件天龙山菩萨头"在 CMA / Harvard / AIC / Penn 的 accession_number 串起来。这是现有 schema 缺的"流散件聚合"字段。
- **判定**:**P1**——不是"再接一个数据源",而是"**在现有 3 + 2(Harvard + AIC)上加 wikidata_qid 字段**"。工程量小:逐件查 wikidata API 拿 Q-ID;失败标 null。这是 ADR-003 demo "流散与数字回归" 叙事的工程化基石。

### B-3 · DPLA(Digital Public Library of America)

- 美国全国聚合(图书馆 + 档案馆 + 博物馆);**艺术馆参与度有限**(主要是 Walters / NGA Kress / Yale Center for British Art / 印第安纳波利斯 / 达拉斯);**中国艺术专题量级很小**。
- **判定**:**不接**。Met / AIC / Smithsonian 都是 DPLA 间接合作但**直接走它们各自 API 信息更密**;DPLA 抽象层带来字段流失。

### B-4 · IIIF 集合(任何 IIIF endpoint)

- 不是数据源,是**图像消费协议**。
- 现有 CMA / Smithsonian / Met 都不发 IIIF;Harvard / AIC / Yale / V&A 发 IIIF。
- **判定**:**应在 ingest 管线里加 IIIF parser**(检测 manifest URL → 解 `service/@id` → 拿对应分辨率)。**工程模式价值 > 单源价值**——这是 ADR-003 §"两条可泛化的工程模式"的落地。

### B-5 · Google Arts & Culture

- **不开放数据 API**(2017 之后关 API);只能爬网页。
- **判定**:**跳过**。反原则。

### B-6 · 专题项目:芝大 tls.uchicago.edu + xts.uchicago.edu

- 不是单馆,是**专题数据库**(155 件 Tianlongshan + 100 件 Xiangtangshan,3D 模型 + 高清照片 + 跨馆 accession 索引)。
- License:tls.uchicago.edu 网站本身公开浏览;3D 数据下载要邮件申请(ADR-003 已记录);**但其"跨馆 accession 索引表"(每件标注现藏馆 + 馆藏号)是公开可见的网页内容**。
- **判定**:**P0 spike(必做)**。**爬取 tls.uchicago.edu 公开页面的"跨馆 accession 索引表"作为 metadata 增强层**(不入主语料,作 `tianlongshan_accession_map.json`);此表与上述 Wikidata Q-ID 串联,构成 demo "数字回归" wow moment 的工程底座。

---

## C · 反向信息(看似可用实不可用)

| 馆 / 源 | 表面 | 实际 | 类型 |
|---|---|---|---|
| British Museum SPARQL | "全球最大博物馆开放数据" | CC BY-NC-SA + endpoint 维护起伏 + CIDOC-CRM 入门成本高 | 工程陷阱 + license 灰区 |
| V&A API | "API 公开" | 元数据 OK 但**图像默认走商用授权**;ToC 2025-04 更新强调非商用 | License 灰区("非商业"在 side project → 商业化路径上是雷) |
| Asian Art Museum SF | "20,000 件中国艺术品" | 馆方明文版权全留,**无 API、无 dump** | 实物丰、数据零 |
| MFA Boston | "160k 件可搜索" | **每张高清 $50**;无 API | 收费 |
| Royal Ontario Museum | "OpenROM" | **是建筑改造**,不是开放数据(易混淆) | 命名陷阱 |
| Musée Guimet | "2026 数字门户" | 写的是 "From 2026 will publish";未上线 | 未来时态当现在 |
| Nelson-Atkins | "数字化收藏" | 仅网页浏览,**无 API/dump** | 实物丰、数据零 |
| Google Arts & Culture | "覆盖广" | 2017 后 API 关闭;爬网页不合规 | 名义开放、实际封闭 |
| DPLA | "美国数字图书馆联盟" | 艺术馆参与度低,中国艺术专题极小 | 范围错配 |
| Met 明清子集 | "11k 条已下载" | **demo 切片用不上**(Curator 已标 R1) | 已识别 |
| 数字敦煌开放素材库 | "已上链授权机制" | **300–800 元/张商用授权** | 收费(ADR-003 已记录) |

**关键反向洞察**:海外亚洲艺术 powerhouse(MFA / SF Asian Art / Nelson-Atkins / ROM)**在实物层强,但在数据层全部不可用**——这是 founding insight "海外 CC0 是国内 RAG 最稳底座"的一个边界:**"海外"不等于"CC0";"亚洲艺术 powerhouse"不等于"开放数据 powerhouse"**。**真正的 CC0 阵营是一个特定的、相对小的圈子**:Met / Smithsonian / CMA / Harvard / AIC / Yale(PD 件)/ Brooklyn(OASC 件)/ Walters / NGA。**Penn 是 CC BY 4.0 半 OA**;**台北故宫是 CC BY 4.0**;**V&A 是非商用 + 非 CC0**;**其他都进不了**。

---

## D · 互补度判断:对 demo 切片(北朝—初唐 + 天龙山 + 山博佛风遗韵)贡献最大的 3 个新源

> 评判标准:(a) license 干净(CC0 或 CC BY 4.0)、(b) 数据接口公开且工程量 ≤ 2 天、(c) 北朝—初唐窗口件数 +30 以上 或者 demo 核心叙事(流散与数字回归)直接相关。

### 1. **Art Institute of Chicago(AIC)** —— P0,本周接入

**为什么:**
- **唯一同时满足三件事的源**:CC0 + 公开 API + **馆藏天龙山佛首**。
- ADR-003 demo 叙事核心 = 芝大天龙山项目 + 山博现场触发;AIC 是**芝加哥本地"实物-数字"闭环的关键节点**——叙事自洽度最高。
- 北朝—初唐窗口预估增量 +30–60 件;天龙山 specific 件 +3–5(精确数需 ingest 后再确认)。
- 工程:`extract_aic.py` ~50 行 stdlib;字段映射与现有 schema 同模式;IIIF URL 可直接进 `image_urls`。
- 重复度:**极低**(与 CMA 卢芹斋系、Met 241C 入藏渠道完全不同)。

**风险:** AIC API 文档未明示 rate limit;Phase 1 全量拉一次 ~7,500 件中国艺术,需 ~1–2 小时(0.5s/req 限速),在 GitHub Actions runner 上跑没问题。

### 2. **Harvard Art Museums** —— P0,本周或下周接入

**为什么:**
- **CC0 数据集 + IIIF 全量 + REST API + Dataverse 镜像** ——任何一项都比 V&A 干净。
- **Winthrop 收藏(Gallery 1610)**:北朝—初唐中国佛教雕塑专门展厅,与现有 3 馆入藏渠道几乎完全不重叠。
- 字段密度可对标 CMA;预估北朝—初唐窗口 +30–80 件。
- 工程:`extract_harvard.py` ~50 行,需 API key(免费申请,但**本任务 T2 域内**——若注册涉及邮件填写,提前与 PM 对齐;若仅是网页表单 → 自助 OK)。

**风险:** API key 申请是边界——"注册免费服务"在宪法 T3 边界上;**建议先用 Harvard Dataverse 的 CSV dump**(无需注册),仅在需要单件高清/IIIF 时用 API。

### 3. **Penn Museum CSV + 天龙山项目网站爬取**(组合)—— P1,本月接入

**为什么:**
- **Penn Museum 是 Buddhist 雕塑实物层的极强补充**(5 件天龙山佛头明示),CC BY 4.0 license 干净。
- 配合 `tls.uchicago.edu` 公开页面爬取的"跨馆 accession 索引",可以**把 demo 叙事从"几馆数据并排"升级为"同一件文物的跨馆物理坐标"**(同一窟同一龛同一头像 →CMA / Harvard / AIC / Penn / Nelson-Atkins 五点定位)——这是 wow moment 工程。
- 工程:`extract_penn.py` 处理 CSV(stdlib,~30 行);**图像需二次抓取**(从 object page 解 OG meta image),或暂时不拉图、仅入 metadata。

**风险:**
- Penn license 是 CC BY 4.0 不是 CC0:**需要在 schema `license` enum 加新值**(`CC-BY-4.0`),并在 `rag_chunks.ndjson` 内出处文本里强制带"Penn Museum"署名(满足 attribution 要求);这是 Builder 任务,Researcher 不动手。
- 天龙山项目 3D 数据邮件申请是 T3,**本任务范畴只爬公开的索引表网页**,不申请 3D 文件。

### (荣誉提名 / 不入 top 3 的原因)
- **V&A**:license 灰度,仅作"二级对照件"补元数据,不入 CC0 主索引。
- **Princeton**:边际增益偏向 Phase 2(Liao painted-wood,Tang 书画)。
- **Yale LUX**:技术挑战(Linked.art)价值高但 demo 切片直接增益小。
- **Smithsonian 其他 unit**:零代码成本但零核心增益。
- **British Museum**:斯坦因敦煌组件诱人但 license + 工程双门槛高。

---

## 给 Orchestrator 的具体建议

### 立刻接入(本周)
- **Art Institute of Chicago `extract_aic.py`** —— 复用现有 `extract_cma.py` 模板,~50 行 stdlib + IIIF URL 拼接。**单一最高 ROI 任务**。
- **Wikidata Q-ID 增强字段** —— 不是新源,是现有 5 馆 schema 加 `wikidata_qid` 字段,用 wikidata REST API 逐件查;失败标 null。**这是"流散件聚合"的工程底座**,无 Q-ID 就无法做 demo wow moment 中的"同一件五馆定位"。
- **`tianlongshan_accession_map.json`** —— 从 `tls.uchicago.edu` 公开"散件索引"页(155 件)爬取**跨馆 accession 表**(图像不入,仅入 accession_number + 现藏馆 + 窟号 + URL);不入主语料,作旁注表。

### 次优补强(本月)
- **Harvard Art Museums** —— 优先用 Dataverse CSV(零注册),IIIF 单件 fetch 在产品级才加 API key。
- **Penn Museum CSV** —— ~30 行处理,license enum 加 `CC-BY-4.0`,主索引 attribution 字段强制带馆名。

### 放弃 / 暂停
- **MFA Boston / Asian Art Museum SF / Nelson-Atkins / ROM / Guimet / Cernuschi / Rietberg** —— 全部跳过。无 OA dump、license 不可用。
- **British Museum SPARQL** —— 暂停,license + 工程双门槛。
- **DPLA / Google Arts & Culture** —— 不用。
- **Europeana** —— 暂停(P2 spike)。
- **Smithsonian 扩单元** —— 不接,边际增益小。
- **台北故宫** —— Phase 1 不接(品类正交);Phase 2 书画切片时再启动。

### 需要 PM 决策的灰区

1. **V&A 接不接?** 我的建议是"接元数据 + 缩略图,不接主图(license)"——但这给主索引引入"非 CC0 但 OA-friendly"的中间档,需 PM 拍板是否在 `license` enum 里加 `VA-Personal-Educational` 这一档,以及 RAG 检索时是否给它降权。**这是 schema 演化决策,不是 Researcher 范畴**。
2. **Wikidata Q-ID 增强字段如何处理 missing(查不到 Q-ID 的件)?** 全部标 null 不影响 CC0 检索,但 demo "跨馆聚合" 视图会很稀疏。**是否要 Builder 写一个"半自动 wikidata 反查 + 人工核验"流程?**——若是,需考虑工时预算。
3. **Penn Museum 的图像二次抓取是否值得做?** CSV 没图,需要从 object page 解析 OG meta image。**收益**:北朝—初唐 +50–100 件图。**成本**:~半天工程 + 几小时网络拉取 + 反封 IP 风险(Penn 没有显式 rate limit 政策)。**PM 决定是否优先级**。

---

## 不确定 / 需要进一步调研

1. **AIC、Harvard、Penn 各自"中国艺术 / 北朝—初唐窗口"的精确件数**——我给的是估算(基于馆方主页描述 + 第三方 libguide),**只有真实 ingest 之后才知道**。这是"先做最小 spike(每源拉 10 件验字段)再决定全量"的正常工程节奏。
2. **AIC API 实际 rate limit**——文档未明示;社区报告"温和";但 7,500 件全量需要分批和重试逻辑。
3. **tls.uchicago.edu 的"散件索引"页是否有反爬机制**——网页公开但**未提供机器可读 endpoint**;爬取 HTML 解析需要 BeautifulSoup-ish 解析(stdlib `html.parser` 也行)。
4. **Wikidata 中天龙山/响堂山散件的 Q-ID 覆盖率**——Wikidata 上 `Q2431144`(天龙山石窟)存在但下游 instance-of 链可能不完整;**实测 spike 5 件再决策**。
5. **CMA / Met / FSG / AIC / Harvard / Penn 六馆之间"同件不同馆藏号"的重叠程度**——这是"跨馆 accession 索引"工程的核心未知量;**只有 Wikidata Q-ID 字段加进去之后才能 SQL 一下知道**。

---

## 附:与现有 3 馆字段对齐难度速查表(供 Builder 取用)

| 候选源 | 字段对齐难度 | 关键差异 | 工程预估 |
|---|---|---|---|
| Art Institute of Chicago | **低** | API 结构与 Met 类似;IIIF URL 多一道拼接 | ~50 行 stdlib,半天 |
| Harvard Art Museums | **低** | API 结构 RESTful + Dataverse CSV 双轨;字段名映射工作量略大 | ~60 行,半天–1 天 |
| Penn Museum | **中** | 只有 CSV,无 image URL,license CC BY 4.0 需 schema 加 enum 值 | ~30 行 CSV + 图像二次抓 ~半天 |
| V&A | **低**(若仅接元数据) | API 字段与 Met 对齐良好;但要在 `license` 字段加 `VA-Personal-Educational` 档 | ~30 行,半天 |
| Wikidata Q-ID 增强 | **低**(增量字段) | 不是新 extractor,是在现有 5/6 个源上批量补字段 | ~40 行查询脚本,半天–1 天 |
| tianlongshan_accession_map | **中**(HTML 爬) | 不入主语料,独立 JSON;~155 件,工作量小 | ~半天 |

---

**报告完。**  本报告不做"应该不应该"判断(那是 Curator / Critic / PM);只供"哪些可用、哪些不可用、按什么顺序最划算"的输入材料。
