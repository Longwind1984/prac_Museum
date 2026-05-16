# docs/ — GitHub Pages 入口

仓库的静态 web 入口。两个文件:

- `index.html` + `app.js` — vanilla JS 图鉴(无构建步骤)
- 加载 `../data/sources/rag_chunks.ndjson` 与 `../data/sources/images/...`

## 在 GitHub Pages 上启用

仓库 `Settings → Pages`,Source 选 `Deploy from a branch`,Branch 选当前分支
(`claude/install-superpower-plugin-bh2Mg`),路径选 `/docs`。等几分钟后
访问 `https://longwind1984.github.io/prac_Museum/`。

也可本地预览:

```bash
cd /path/to/repo
python -m http.server 8000
# 浏览器开 http://localhost:8000/docs/
```

## 功能

- 筛选:朝代 / 源 / 材质 / 文本 / 仅带图
- 每页 60 张缩略图,懒加载
- 点卡片 → 详情 modal(完整 metadata + 高清原图链)
- 移动端 2 列响应式
- 全静态,~50KB JS,数据走 fetch

## 已知限制

- 大数据集(15,299 chunks / 12.6 MB NDJSON)首次加载需 1–2 秒
- 无服务端,无全文索引;搜索是客户端 substring,大量文本 query 时较慢
- 没有 LLM 检索增强 — 那是 v2 工作
