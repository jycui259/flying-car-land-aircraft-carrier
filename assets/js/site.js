/* Site behaviour: reading progress, TOC scrollspy, market-model calculator.
   Vanilla JS, no dependencies. Degrades gracefully without JS. */
(function () {
  "use strict";

  /* ---------- reading progress ---------- */
  var bar = document.querySelector(".progress");
  if (bar) {
    var update = function () {
      var doc = document.documentElement;
      var max = doc.scrollHeight - doc.clientHeight;
      var p = max > 0 ? (doc.scrollTop || document.body.scrollTop) / max : 0;
      bar.style.width = Math.min(100, Math.max(0, p * 100)) + "%";
    };
    window.addEventListener("scroll", update, { passive: true });
    window.addEventListener("resize", update);
    update();
  }

  /* ---------- TOC scrollspy ---------- */
  var tocLinks = Array.prototype.slice.call(document.querySelectorAll(".toc a[href^='#']"));
  if (tocLinks.length && "IntersectionObserver" in window) {
    var byId = {};
    var targets = [];
    tocLinks.forEach(function (a) {
      var id = a.getAttribute("href").slice(1);
      var el = document.getElementById(id);
      if (el) { byId[id] = a; targets.push(el); }
    });
    var visible = new Set();
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { visible.add(e.target.id); } else { visible.delete(e.target.id); }
      });
      var current = null;
      targets.forEach(function (t) { if (!current && visible.has(t.id)) { current = t.id; } });
      if (!current) {
        var top = window.scrollY + 120;
        targets.forEach(function (t) { if (t.offsetTop <= top) { current = t.id; } });
      }
      tocLinks.forEach(function (a) { a.classList.remove("active"); a.removeAttribute("aria-current"); });
      if (current && byId[current]) {
        byId[current].classList.add("active");
        byId[current].setAttribute("aria-current", "true");
      }
    }, { rootMargin: "-12% 0px -70% 0px", threshold: [0, 1] });
    targets.forEach(function (t) { io.observe(t); });
  }

  /* ---------- market model calculator ---------- */
  var calc = document.querySelector("[data-calc]");
  if (!calc) { return; }

  var money = function (v) {
    if (!isFinite(v)) { return "—"; }
    if (Math.abs(v) >= 100) { return v.toFixed(0) + " 亿元"; }
    if (Math.abs(v) >= 1) { return v.toFixed(1) + " 亿元"; }
    return (v * 10000).toFixed(0) + " 万元";
  };

  var read = function (id) {
    var el = document.getElementById(id);
    return el ? parseFloat(el.value) : 0;
  };

  var label = function (inputId, outId, suffix) {
    var el = document.getElementById(inputId);
    var out = document.getElementById(outId);
    if (el && out) { out.textContent = el.value + suffix; }
  };

  var run = function () {
    label("c-price", "v-price", " 万元");
    label("c-units", "v-units", " 台");
    label("c-conv", "v-conv", "%");
    label("c-cost", "v-cost", "%");
    var price = read("c-price");      // 万元 / 台
    var units = read("c-units");      // 年产销量 / 台
    var conv  = read("c-conv");       // 订单转化率 %
    var cost  = read("c-cost");       // 单位成本占售价比 %

    var sold = units * conv / 100;
    var revenue = price * sold / 10000;                 // 亿元
    var unitMargin = price * (1 - cost / 100);          // 万元 / 台
    var margin = revenue * (1 - cost / 100);            // 亿元
    var perFlight = 0; // filled below if present

    var set = function (id, text) {
      var el = document.getElementById(id);
      if (el) { el.textContent = text; }
    };
    set("o-rev", money(revenue));
    set("o-sold", sold.toFixed(0) + " 台");
    set("o-margin", money(margin));
    set("o-unit", unitMargin.toFixed(0) + " 万元/台");

    // optional: 5 flights per charge, 2 charges/day scenario
    var flightsPerDay = read("c-flights");
    if (flightsPerDay) {
      perFlight = price * 10000 / (flightsPerDay * 365 * 5); // 5-year straight-line, CNY per flight
      set("o-dep", (perFlight / 10000).toFixed(2) + " 万元/架次");
    }
  };

  calc.addEventListener("input", run);
  calc.addEventListener("change", run);
  run();
})();

