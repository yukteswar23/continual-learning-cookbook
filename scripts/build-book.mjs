// Builds "The Continual Learning Cookbook" from book/chapters/*.html.
//   node scripts/build-book.mjs          build dist/book/index.html (+ figures) and dist/book/artifact.html
//   node scripts/build-book.mjs --check  validate only
// Chapter files start with a JSON header comment: <!-- {"id":..., "part":..., "title":..., "dek":...} -->
// Tokens inside chapters:
//   \( ... \) inline math, \[ ... \] display math (KaTeX, rendered at build time)
//   <fig k="key"></fig>             a figure from book/figures.json (original figure from a source)
//   <cite k="src"></cite>           citation chip linking to the references chapter
import { readFileSync, writeFileSync, mkdirSync, readdirSync, copyFileSync, existsSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import katex from "katex";

const root = join(dirname(fileURLToPath(import.meta.url)), "..");
const B = (p) => join(root, "book", p);
const read = (p) => readFileSync(p, "utf8");
const errors = [];
const fail = (m) => errors.push(m);

const sources = JSON.parse(read(B("sources.json")));
const figures = JSON.parse(read(B("figures.json")));
const sizes = JSON.parse(read(B("figures/_sizes.json")));
const esc = (s) => String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");

function math(s, where) {
  // Display first, then inline. Content between delimiters is LaTeX.
  return s
    .replace(/\\\[([\s\S]+?)\\\]/g, (_, tex) => {
      try { return `<div class="eq">${katex.renderToString(tex.trim(), { displayMode: true, throwOnError: true, strict: "ignore", trust: false })}</div>`; }
      catch (e) { fail(`${where}: display math error: ${e.message.split("\n")[0]} in ${tex.trim().slice(0, 80)}`); return ""; }
    })
    .replace(/\\\(([\s\S]+?)\\\)/g, (_, tex) => {
      try { return katex.renderToString(tex.trim(), { displayMode: false, throwOnError: true, strict: "ignore" }); }
      catch (e) { fail(`${where}: inline math error: ${e.message.split("\n")[0]} in ${tex.trim().slice(0, 80)}`); return ""; }
    });
}

const usedFigs = {};
let figCounter = 0;
function figure(k, chapterN, where) {
  const f = figures[k];
  if (!f) { fail(`${where}: unknown figure "${k}"`); return ""; }
  const src = sources[f.src];
  if (!src) { fail(`figure "${k}": unknown source "${f.src}"`); return ""; }
  figCounter++;
  const n = `${chapterN}.${figCounter}`;
  (usedFigs[f.src] = usedFigs[f.src] || []).push({ k, label: f.label, n });
  const panels = f.file ? [{ file: f.file, w: 1200, h: 600 }] : sizes[k];
  if (!panels) { fail(`figure "${k}": no exported image`); return ""; }
  panels.forEach((p) => { if (!existsSync(B("figures/" + p.file))) fail(`figure "${k}": missing file ${p.file}`); });
  const layout = f.layout || (panels.length > 1 ? "row" : "single");
  const alt = `${f.label} from ${src.short}`;
  const imgs = panels.map((p, i) => `<img src="figures/${p.file}" width="${p.w}" height="${p.h}" loading="lazy" decoding="async" alt="${esc(alt)}${panels.length > 1 ? `, panel ${i + 1}` : ""}">`).join("");
  const narrow = f.maxw ? ` narrow" style="--maxw:${f.maxw}px` : "";
  return `<figure class="pfig" id="fig-${n.replace(".", "-")}"><div class="pfig-plate ${layout}${narrow}">${imgs}</div><figcaption><div class="pfig-head"><span class="pfig-n">Fig. ${n}</span><span class="pfig-src">${esc(f.label)} in <a href="#ref-${f.src}">${esc(src.short)}</a></span></div><p>${math(f.caption, "caption " + k)}</p><p class="pfig-credit">Original figure reproduced from <a href="${src.url}" target="_blank" rel="noopener">${esc(src.short)}</a> · ${esc(src.license.split(/\.\s/)[0])}</p></figcaption></figure>`;
}

function cite(k, where) {
  const s = sources[k];
  if (!s) { fail(`${where}: unknown citation "${k}"`); return ""; }
  return `<a class="cite" href="#ref-${k}" title="${esc(s.cite)}">${esc(s.short)}</a>`;
}

// ── Chapters ─────────────────────────────────────────
const files = readdirSync(B("chapters")).filter((f) => f.endsWith(".html")).sort();
const chapters = files.map((file) => {
  const raw = read(B("chapters/" + file));
  const m = raw.match(/^<!--\s*(\{[\s\S]*?\})\s*-->/);
  if (!m) { fail(`${file}: missing JSON header`); return null; }
  let meta; try { meta = JSON.parse(m[1]); } catch (e) { fail(`${file}: bad header JSON (${e.message})`); return null; }
  figCounter = 0;
  let body = raw.slice(m[0].length);
  body = body.replace(/<fig k="([\w-]+)"><\/fig>/g, (_, k) => figure(k, meta.n, file));
  body = body.replace(/<cite k="([\w-]+)"><\/cite>/g, (_, k) => cite(k, file));
  body = math(body, file);
  if (/\\\(|\\\[/.test(body.replace(/<annotation[\s\S]*?<\/annotation>/g, ""))) fail(`${file}: unmatched math delimiter`);
  (meta.sources || []).forEach((s) => { if (!sources[s]) fail(`${file}: header source "${s}" unknown`); });
  return { ...meta, file, body };
}).filter(Boolean);

const ids = new Set();
chapters.forEach((c) => { if (ids.has(c.id)) fail(`duplicate chapter id ${c.id}`); ids.add(c.id); });

// References chapter (generated)
const refsBody = `<p class="lede">Every figure in this book is an original figure from one of the works below, shown with its original caption and figure number. Equations are typeset from the papers' own definitions. Tables are transcribed from the papers. Text that is not quoted is written for this book.</p>
<ol class="refs">${Object.entries(sources).map(([k, s]) => `<li id="ref-${k}"><p class="ref-cite">${esc(s.cite)}</p><p class="ref-meta"><a href="${s.url}" target="_blank" rel="noopener">${esc(s.url.replace(/^https?:\/\//, ""))}</a>${(s.links || []).map(([l, u]) => ` · <a href="${u}" target="_blank" rel="noopener">${esc(l)}</a>`).join("")}</p><p class="ref-meta">Licence: ${esc(s.license)}</p>${s.note ? `<p class="ref-meta ref-note">${esc(s.note)}</p>` : ""}${usedFigs[k] ? `<p class="ref-meta">Figures used: ${usedFigs[k].map((u) => `<a href="#fig-${u.n.replace(".", "-")}">Fig. ${u.n}</a> (${esc(u.label)})`).join(", ")}</p>` : ""}</li>`).join("")}</ol>`;
chapters.push({ id: "references", part: "Back matter", n: "R", title: "References & credits", dek: "Every source in this book, with links and licences.", body: refsBody, kind: "back" });

// Every source should be cited somewhere
Object.keys(sources).forEach((k) => { if (!chapters.some((c) => c.body.includes(`#ref-${k}"`))) fail(`source "${k}" is never cited`); });

if (errors.length) { errors.forEach((e) => console.error("  ERROR " + e)); console.error(`\n${errors.length} error(s). Nothing built.`); process.exit(1); }
const nFigs = Object.values(usedFigs).reduce((a, b) => a + b.length, 0);
console.log(`  ok    ${chapters.length} chapters · ${nFigs} source figures · ${Object.keys(sources).length} sources`);
if (process.argv.includes("--check")) process.exit(0);

// ── Assemble ─────────────────────────────────────────
// KaTeX CSS with fonts inlined as data URIs (artifact CSP allows no external font hosts but Google Fonts).
const kdir = join(root, "node_modules/katex/dist");
let kcss = read(join(kdir, "katex.min.css"));
kcss = kcss.replace(/src:url\(fonts\/([\w-]+)\.woff2\) format\("woff2"\),url\(fonts\/[\w-]+\.woff\) format\("woff"\),url\(fonts\/[\w-]+\.ttf\) format\("truetype"\)/g,
  (_, name) => `src:url(data:font/woff2;base64,${readFileSync(join(kdir, "fonts", name + ".woff2")).toString("base64")}) format("woff2")`);
if (/url\(fonts\//.test(kcss)) { console.error("KaTeX font inlining failed"); process.exit(1); }

const parts = [];
chapters.forEach((c) => { let p = parts.find((x) => x.name === c.part); if (!p) parts.push(p = { name: c.part, items: [] }); p.items.push(c); });
const toc = parts.map((p) => `<li class="toc-part"><span>${esc(p.name)}</span><ol>${p.items.map((c) => `<li><a href="#${c.id}" data-ch="${c.id}"><span class="toc-n">${c.kind === "front" ? "" : esc(String(c.n))}</span><span class="toc-t">${esc(c.title)}</span></a></li>`).join("")}</ol></li>`).join("");

const articles = chapters.map((c, i) => {
  const prev = chapters[i - 1], next = chapters[i + 1];
  const head = c.kind === "cover" ? "" : `<header class="ch-open"><div class="ch-num">${esc(String(c.n))}</div><div class="ch-titles"><p class="ch-part">${esc(c.part)}</p><h1>${esc(c.title)}</h1>${c.dek ? `<p class="ch-dek">${esc(c.dek)}</p>` : ""}${(c.sources || []).length ? `<p class="ch-sources"><span>Cooked from</span> ${c.sources.map((s) => cite(s, c.id)).join(" ")}</p>` : ""}</div></header>`;
  const nav = `<nav class="ch-nav" aria-label="Chapter navigation">${prev ? `<a href="#${prev.id}" class="prev"><span>← Previous</span><strong>${esc(prev.title)}</strong></a>` : "<span></span>"}${next ? `<a href="#${next.id}" class="next"><span>Next →</span><strong>${esc(next.title)}</strong></a>` : "<span></span>"}</nav>`;
  return `<article class="chapter${c.kind ? " " + c.kind : ""}" id="${c.id}" data-title="${esc(c.title)}">${head}<div class="ch-body">${c.body}</div>${nav}</article>`;
}).join("\n");

const style = read(B("book.css"));
const script = read(B("book.js"));
const built = new Date().toISOString().slice(0, 10);
const page = `<title>The Continual Learning Cookbook</title>
<meta name="description" content="A cookbook for continual learning, built from the original papers, their figures and their equations.">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:ital,wdth,wght@0,62..125,400..900;1,62..125,400..700&family=Instrument+Serif:ital@0;1&family=Space+Mono:wght@400;700&display=swap">
<style>${kcss}</style>
<style>${style}</style>
<div class="progress" aria-hidden="true"><span></span></div>
<button class="toc-toggle" type="button" aria-controls="toc" aria-expanded="false">Contents</button>
<aside class="toc" id="toc" aria-label="Contents"><a class="toc-brand" href="#cover">The Continual Learning <em>Cookbook</em></a><ol>${toc}</ol><p class="toc-foot">Built ${built}</p></aside>
<main id="book">${articles}</main>
<script>${script}</script>`;

// 1) index.html at the repository root (GitHub Pages), loading images from book/figures/.
const cut = page.indexOf('<div class="progress"');
const doc = (p) => `<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n${p.slice(0, cut)}</head>\n<body>\n${p.slice(cut)}\n</body>\n</html>\n`;
writeFileSync(join(root, "index.html"), doc(page.replaceAll('src="figures/', 'src="book/figures/')));
console.log(`  built index.html (${(Buffer.byteLength(page) / 1024).toFixed(0)} KB page; images from book/figures/)`);

// 2) dist/book: a portable copy (page fragment for hosted artifacts + figures folder).
const out = join(root, "dist/book");
mkdirSync(join(out, "figures"), { recursive: true });
readdirSync(B("figures")).filter((f) => !f.startsWith("_")).forEach((f) => copyFileSync(B("figures/" + f), join(out, "figures", f)));
writeFileSync(join(out, "artifact.html"), page);
writeFileSync(join(out, "index.html"), doc(page));
console.log(`  built dist/book/ (${readdirSync(join(out, "figures")).length} figure files)`);
