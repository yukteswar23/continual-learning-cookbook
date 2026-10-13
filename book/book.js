(function () {
  "use strict";
  document.documentElement.classList.add("js");
  var chapters = Array.prototype.slice.call(document.querySelectorAll(".chapter"));
  var links = Array.prototype.slice.call(document.querySelectorAll(".toc a[data-ch]"));
  var toc = document.getElementById("toc");
  var toggle = document.querySelector(".toc-toggle");
  var bar = document.querySelector(".progress span");
  var current = null;

  function show(id, anchor) {
    var ch = document.getElementById(id);
    if (!ch || !ch.classList.contains("chapter")) ch = chapters[0];
    if (current !== ch) {
      chapters.forEach(function (c) { c.classList.toggle("on", c === ch); });
      links.forEach(function (a) { a.setAttribute("aria-current", String(a.getAttribute("data-ch") === ch.id)); });
      current = ch;
      document.title = (ch.id === "cover" ? "" : ch.getAttribute("data-title") + " · ") + "The Continual Learning Cookbook";
    }
    var target = anchor ? document.getElementById(anchor) : null;
    if (target) target.scrollIntoView({ block: "start" }); else window.scrollTo(0, 0);
    closeToc();
    onScroll();
  }

  function route() {
    var h = decodeURIComponent(location.hash.replace(/^#/, ""));
    if (!h) return show("cover");
    var el = document.getElementById(h);
    if (el && el.classList.contains("chapter")) return show(h);
    if (el) { var host = el.closest(".chapter"); if (host) return show(host.id, h); }
    show("cover");
  }

  function onScroll() {
    if (!bar || !current) return;
    var max = document.documentElement.scrollHeight - window.innerHeight;
    bar.style.width = (max > 0 ? Math.min(100, (window.scrollY / max) * 100) : 0) + "%";
  }
  function closeToc() { if (toc) toc.classList.remove("open"); if (toggle) toggle.setAttribute("aria-expanded", "false"); }

  if (toggle) toggle.addEventListener("click", function () {
    var open = !toc.classList.contains("open");
    toc.classList.toggle("open", open);
    toggle.setAttribute("aria-expanded", String(open));
  });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") closeToc();
    if (/INPUT|TEXTAREA/.test(document.activeElement.tagName)) return;
    var i = chapters.indexOf(current);
    if (e.key === "ArrowRight" && e.altKey && chapters[i + 1]) location.hash = chapters[i + 1].id;
    if (e.key === "ArrowLeft" && e.altKey && chapters[i - 1]) location.hash = chapters[i - 1].id;
  });
  window.addEventListener("hashchange", route);
  window.addEventListener("scroll", onScroll, { passive: true });
  route();
})();
