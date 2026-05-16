// "一起看" CC0/PD gallery — vanilla JS, no build step.
// Loads rag_chunks.ndjson, paginates, filters, modal detail view.
// Designed to be deployable to GitHub Pages from /docs.

const CHUNKS_URL = "../data/sources/rag_chunks.ndjson";
const IMAGES_BASE = "../data/sources/images/";
const PAGE_SIZE = 60;

const DYNASTY_ORDER = [
  "Neolithic","Shang","Zhou","Warring States","Han","Six Dynasties",
  "Northern Wei","Eastern Wei","Northern Qi","Northern Zhou",
  "Sui","Tang","Five Dynasties","Liao","Song","Jin","Yuan","Ming","Qing"
];

const DYNASTY_ZH = {
  Neolithic:"新石器", Shang:"商", Zhou:"周", "Warring States":"战国",
  Han:"汉", "Six Dynasties":"六朝",
  "Northern Wei":"北魏", "Eastern Wei":"东魏",
  "Northern Qi":"北齐", "Northern Zhou":"北周",
  Sui:"隋", Tang:"唐", "Five Dynasties":"五代",
  Liao:"辽", Song:"宋", Jin:"金", Yuan:"元", Ming:"明", Qing:"清"
};

const SOURCE_LABEL = {
  cma: "Cleveland Museum of Art",
  met: "The Metropolitan Museum of Art",
  smithsonian_fsg: "Freer + Sackler (Smithsonian)"
};

const state = {
  all: [],         // all chunks
  filtered: [],    // current filter result
  page: 0,
  q: "",
  source: "",
  dynasty: "",
  material: "",
  imgOnly: true,
};

async function loadChunks() {
  const r = await fetch(CHUNKS_URL);
  if (!r.ok) throw new Error("Failed to load chunks: " + r.status);
  const text = await r.text();
  // Use \n split (NDJSON spec); avoid splitlines-style splits on U+2028 etc.
  return text.split("\n").filter(l => l.length).map(l => JSON.parse(l));
}

function applyFilters() {
  const q = state.q.toLowerCase();
  state.filtered = state.all.filter(c => {
    const m = c.metadata;
    if (state.source && m.source !== state.source) return false;
    if (state.dynasty && m.dynasty_en !== state.dynasty) return false;
    if (state.material) {
      const mats = (m.materials || []).join(" ").toLowerCase();
      if (!mats.includes(state.material.toLowerCase())) return false;
    }
    if (state.imgOnly && !m.has_image_local) return false;
    if (q) {
      const text = c.text.toLowerCase();
      // All space-separated terms must match
      for (const t of q.split(/\s+/)) {
        if (!t) continue;
        if (!text.includes(t)) return false;
      }
    }
    return true;
  });
  state.page = 0;
  render();
}

function render() {
  const grid = document.getElementById("grid");
  const start = state.page * PAGE_SIZE;
  const end = Math.min(start + PAGE_SIZE, state.filtered.length);
  const slice = state.filtered.slice(start, end);
  if (slice.length === 0) {
    grid.innerHTML = '<div class="loading">无匹配结果。</div>';
  } else {
    grid.innerHTML = slice.map(cardHTML).join("");
    // Attach click handlers
    [...grid.querySelectorAll(".card")].forEach((el, i) => {
      el.addEventListener("click", () => openModal(slice[i]));
    });
  }
  // Update stats / pager
  document.getElementById("stats").textContent =
    `${state.filtered.length} 条匹配 / 共 ${state.all.length} 条`;
  document.getElementById("page-info").textContent =
    state.filtered.length === 0 ? "—" :
    `${start+1}–${end} / ${state.filtered.length}`;
  document.getElementById("prev").disabled = state.page === 0;
  document.getElementById("next").disabled = end >= state.filtered.length;
}

function cardHTML(c) {
  const m = c.metadata;
  // Title is first non-empty line of c.text up to first " · " or "\n"
  const firstLine = c.text.split("\n", 1)[0].trim().slice(0, 60);
  const dy = m.dynasty_en ? `${DYNASTY_ZH[m.dynasty_en] || ""} ${m.dynasty_en}` : "";
  if (!c.image_local) {
    return `<div class="card no-img">
      <div>
        <div class="title">${escapeHTML(firstLine)}</div>
        <div class="dynasty">${escapeHTML(dy)}</div>
        <div class="nomark">(no local image)</div>
      </div></div>`;
  }
  // image_local is 'data/sources/images/...' — strip prefix
  const imgPath = IMAGES_BASE + c.image_local.replace(/^data\/sources\/images\//, "");
  return `<div class="card">
    <img loading="lazy" src="${imgPath}" alt="${escapeHTML(firstLine)}" />
    <div class="meta">
      <div class="title">${escapeHTML(firstLine)}</div>
      <div class="dynasty">${escapeHTML(dy)}</div>
      <div class="src">${escapeHTML(m.source)} · ${m.license}</div>
    </div></div>`;
}

function openModal(c) {
  const m = c.metadata;
  const inner = document.getElementById("modal-inner");
  const firstLine = c.text.split("\n", 1)[0].trim();
  // Display remaining text as paragraphs
  const remaining = c.text.split("\n").slice(1).join("\n").trim();
  const paragraphs = remaining
    .split(/\n+/).map(p => p.trim()).filter(Boolean)
    .map(p => `<p>${escapeHTML(p)}</p>`).join("");
  const imgPath = c.image_local
    ? IMAGES_BASE + c.image_local.replace(/^data\/sources\/images\//, "")
    : null;
  inner.innerHTML = `
    <span class="modal-close" id="x">×</span>
    <h2>${escapeHTML(firstLine)}</h2>
    <div class="dynasty" style="color:var(--accent);font-size:13px;">${escapeHTML(m.dynasty_en || "")} · ${escapeHTML(m.period || "")} · ${escapeHTML(c.record_id)}</div>
    <div class="row">
      <div>
        ${imgPath ? `<img src="${imgPath}" />` : '<p style="color:var(--dim);">(无本地图)</p>'}
        ${c.image_url ? `<p style="margin-top:8px;font-size:11px;"><a href="${c.image_url}" target="_blank">高清原图 ↗</a></p>` : ""}
      </div>
      <dl>
        <dt>Source</dt><dd>${escapeHTML(SOURCE_LABEL[m.source] || m.source)}</dd>
        <dt>License</dt><dd>${escapeHTML(m.license)}</dd>
        ${m.materials && m.materials.length ? `<dt>Material</dt><dd>${escapeHTML(m.materials.join("; "))}</dd>` : ""}
        ${m.date_start || m.date_end ? `<dt>Date range</dt><dd>${m.date_start || "?"} – ${m.date_end || "?"}</dd>` : ""}
        ${m.current_location ? `<dt>Current location</dt><dd>${escapeHTML(m.current_location)}</dd>` : ""}
        ${c.source_url ? `<dt>Source page</dt><dd><a href="${c.source_url}" target="_blank">${escapeHTML(c.source_url)}</a></dd>` : ""}
        <dt>Description / metadata</dt><dd>${paragraphs}</dd>
      </dl>
    </div>`;
  document.getElementById("modal").classList.add("open");
  document.getElementById("x").addEventListener("click", closeModal);
}
function closeModal() {
  document.getElementById("modal").classList.remove("open");
}

function escapeHTML(s) {
  if (s == null) return "";
  return String(s).replace(/[&<>"']/g, c =>
    ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c])
  );
}

function buildDynastyDropdown() {
  const sel = document.getElementById("f-dynasty");
  const counts = {};
  for (const c of state.all) {
    const d = c.metadata.dynasty_en;
    if (d) counts[d] = (counts[d] || 0) + 1;
  }
  for (const d of DYNASTY_ORDER) {
    if (counts[d]) {
      const opt = document.createElement("option");
      opt.value = d;
      opt.textContent = `${DYNASTY_ZH[d] || d} ${d}  (${counts[d]})`;
      sel.appendChild(opt);
    }
  }
}

function wire() {
  document.getElementById("f-dynasty").addEventListener("change", e => {
    state.dynasty = e.target.value; applyFilters();
  });
  document.getElementById("f-source").addEventListener("change", e => {
    state.source = e.target.value; applyFilters();
  });
  document.getElementById("f-material").addEventListener("input", e => {
    state.material = e.target.value; applyFilters();
  });
  document.getElementById("f-q").addEventListener("input", e => {
    state.q = e.target.value; applyFilters();
  });
  document.getElementById("f-img").addEventListener("change", e => {
    state.imgOnly = e.target.checked; applyFilters();
  });
  document.getElementById("prev").addEventListener("click", () => { state.page--; render(); window.scrollTo(0,0); });
  document.getElementById("next").addEventListener("click", () => { state.page++; render(); window.scrollTo(0,0); });
  document.getElementById("modal").addEventListener("click", e => {
    if (e.target.id === "modal") closeModal();
  });
  document.addEventListener("keydown", e => {
    if (e.key === "Escape") closeModal();
  });
}

(async () => {
  try {
    state.all = await loadChunks();
    document.getElementById("sub").textContent =
      `${state.all.length} 条 RAG chunks · ${state.all.filter(c => c.metadata.has_image_local).length} 条带本地图 · 跨 3 家海外馆`;
    buildDynastyDropdown();
    wire();
    applyFilters();
  } catch (e) {
    document.getElementById("grid").innerHTML =
      `<div class="loading" style="color:#f88;">加载失败: ${escapeHTML(e.message)}</div>`;
    console.error(e);
  }
})();
