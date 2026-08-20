/* =========================================================
   MuleSoft Mastery — Site Scripts
   Zero dependencies. No API keys. No third-party tracking.
   Progressively enhances functionality that already works
   without JavaScript (sidebar links, <details> dropdowns).
   ========================================================= */
(function () {
  "use strict";

  /* ---------- Resolve site root regardless of page depth ---------- */
  var thisScript = document.currentScript;
  var scriptUrl = thisScript ? thisScript.src : (function () {
    var scripts = document.getElementsByTagName("script");
    for (var i = 0; i < scripts.length; i++) {
      if (/main\.js(\?|$)/.test(scripts[i].src)) return scripts[i].src;
    }
    return window.location.href;
  })();
  // main.js lives at assets/js/main.js -> root is two levels up
  var SITE_ROOT = new URL("../../", scriptUrl);
  var SEARCH_INDEX_URL = new URL("search-index.json", scriptUrl).href;

  document.addEventListener("DOMContentLoaded", function () {
    initMobileNav();
    initSidebarAccordion();
    initSearch();
    initFooterYear();
    initExternalLinks();
    initThemeToggle();
  });

  /* ---------- Light / dark mode toggle (persisted, no FOUC) ---------- */
  function initThemeToggle() {
    var btns = document.querySelectorAll("[data-theme-toggle]");
    if (!btns.length) return;
    var root = document.documentElement;

    function currentTheme() {
      return root.getAttribute("data-theme") === "dark" ? "dark" : "light";
    }
    function setTheme(theme) {
      if (theme === "dark") {
        root.setAttribute("data-theme", "dark");
      } else {
        root.removeAttribute("data-theme");
      }
      try { localStorage.setItem("theme", theme); } catch (e) {}
    }

    btns.forEach(function (btn) {
      btn.addEventListener("click", function () {
        setTheme(currentTheme() === "dark" ? "light" : "dark");
      });
    });
  }

  /* ---------- Mobile sidebar / nav toggle ---------- */
  function initMobileNav() {
    var toggles = document.querySelectorAll("[data-sidebar-toggle]");
    var sidebar = document.getElementById("sidebar");
    var backdrop = document.getElementById("sidebarBackdrop");
    if (!sidebar) return;

    function openSidebar() {
      sidebar.classList.add("open");
      if (backdrop) backdrop.classList.add("open");
      document.body.style.overflow = "hidden";
    }
    function closeSidebar() {
      sidebar.classList.remove("open");
      if (backdrop) backdrop.classList.remove("open");
      document.body.style.overflow = "";
    }

    toggles.forEach(function (btn) {
      btn.addEventListener("click", function () {
        if (sidebar.classList.contains("open")) closeSidebar();
        else openSidebar();
      });
    });
    if (backdrop) backdrop.addEventListener("click", closeSidebar);
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") closeSidebar();
    });
    // Close drawer automatically when a sidebar link is tapped (mobile)
    sidebar.addEventListener("click", function (e) {
      var link = e.target.closest("a");
      if (link && window.innerWidth <= 1024) closeSidebar();
    });
  }

  /* ---------- Sidebar accordion behaviour ---------- */
  function initSidebarAccordion() {
    var details = document.querySelectorAll(".side-cat");
    details.forEach(function (d) {
      d.addEventListener("toggle", function () {
        if (d.open) {
          details.forEach(function (other) {
            if (other !== d) other.open = false;
          });
        }
      });
    });
  }

  /* ---------- Client-side search (no API key, static JSON index) ---------- */
  function initSearch() {
    var inputs = document.querySelectorAll("[data-search-input]");
    if (!inputs.length) return;

    var indexPromise = null;
    function loadIndex() {
      if (!indexPromise) {
        // Every page embeds the full search index inline (window.__MM_SEARCH_INDEX__)
        // so search works instantly and even over file:// (no fetch/CORS needed).
        // Fall back to fetching the static JSON file only if that's missing.
        if (window.__MM_SEARCH_INDEX__ && window.__MM_SEARCH_INDEX__.length) {
          indexPromise = Promise.resolve(window.__MM_SEARCH_INDEX__);
        } else {
          indexPromise = fetch(SEARCH_INDEX_URL)
            .then(function (res) {
              if (!res.ok) throw new Error("index fetch failed");
              return res.json();
            })
            .catch(function () {
              return [];
            });
        }
      }
      return indexPromise;
    }

    inputs.forEach(function (input) {
      var wrapper = input.closest(".header-search");
      if (!wrapper) return;
      var resultsBox = wrapper.querySelector("[data-search-results]");
      if (!resultsBox) return;
      var activeIndex = -1;

      function render(items, query) {
        resultsBox.innerHTML = "";
        if (!query) {
          resultsBox.classList.remove("open");
          return;
        }
        if (!items.length) {
          var empty = document.createElement("div");
          empty.className = "sr-empty";
          empty.textContent = 'No lessons found for "' + query + '". Try a different keyword.';
          resultsBox.appendChild(empty);
          resultsBox.classList.add("open");
          return;
        }
        items.slice(0, 8).forEach(function (item) {
          var a = document.createElement("a");
          a.className = "sr-item";
          a.href = new URL(item.url, SITE_ROOT).href;
          a.innerHTML =
            '<div class="sr-cat">' + escapeHtml(item.category) + "</div>" +
            '<div class="sr-title">' + escapeHtml(item.title) + "</div>" +
            '<div class="sr-summary">' + escapeHtml(item.summary || "") + "</div>";
          resultsBox.appendChild(a);
        });
        resultsBox.classList.add("open");
        activeIndex = -1;
      }

      function search(query) {
        loadIndex().then(function (data) {
          var q = query.trim().toLowerCase();
          if (!q) { render([], ""); return; }
          var scored = data
            .map(function (item) {
              var hay = (item.title + " " + item.category + " " + (item.summary || "") + " " + (item.keywords || "")).toLowerCase();
              var score = -1;
              if (item.title.toLowerCase().indexOf(q) === 0) score = 100;
              else if (item.title.toLowerCase().indexOf(q) !== -1) score = 60;
              else if (hay.indexOf(q) !== -1) score = 20;
              return { item: item, score: score };
            })
            .filter(function (r) { return r.score > -1; })
            .sort(function (a, b) { return b.score - a.score; })
            .map(function (r) { return r.item; });
          render(scored, query);
        });
      }

      var debounceTimer;
      input.addEventListener("input", function () {
        clearTimeout(debounceTimer);
        var val = input.value;
        debounceTimer = setTimeout(function () { search(val); }, 120);
      });
      input.addEventListener("focus", function () {
        if (input.value.trim()) search(input.value);
      });
      input.addEventListener("keydown", function (e) {
        var items = resultsBox.querySelectorAll(".sr-item");
        if (!items.length) return;
        if (e.key === "ArrowDown") {
          e.preventDefault();
          activeIndex = Math.min(activeIndex + 1, items.length - 1);
          highlight(items);
        } else if (e.key === "ArrowUp") {
          e.preventDefault();
          activeIndex = Math.max(activeIndex - 1, 0);
          highlight(items);
        } else if (e.key === "Enter") {
          if (activeIndex >= 0 && items[activeIndex]) {
            window.location.href = items[activeIndex].href;
          }
        } else if (e.key === "Escape") {
          resultsBox.classList.remove("open");
          input.blur();
        }
      });

      function highlight(items) {
        items.forEach(function (el, i) {
          el.classList.toggle("sr-active", i === activeIndex);
        });
        if (items[activeIndex]) {
          items[activeIndex].scrollIntoView({ block: "nearest" });
        }
      }

      document.addEventListener("click", function (e) {
        if (!wrapper.contains(e.target)) {
          resultsBox.classList.remove("open");
        }
      });
    });
  }

  function escapeHtml(str) {
    return String(str)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  /* ---------- Footer year ---------- */
  function initFooterYear() {
    var el = document.getElementById("footerYear");
    if (el) el.textContent = new Date().getFullYear();
  }

  /* ---------- Open external links in a new tab safely ---------- */
  function initExternalLinks() {
    var links = document.querySelectorAll('a[href^="http"]');
    links.forEach(function (a) {
      if (a.hostname && a.hostname !== window.location.hostname) {
        a.setAttribute("target", "_blank");
        a.setAttribute("rel", "noopener noreferrer");
      }
    });
  }
})();
