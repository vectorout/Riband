/* RIBAND — minimal behavior layer: mobile menu, scroll reveal, work filter */
(function () {
  "use strict";

  /* mobile menu */
  var btn = document.querySelector(".menu-btn");
  var nav = document.querySelector(".site-nav");
  if (btn && nav) {
    btn.addEventListener("click", function () {
      var open = nav.classList.toggle("open");
      btn.setAttribute("aria-expanded", open ? "true" : "false");
      btn.textContent = open ? btn.dataset.close : btn.dataset.open;
    });
    nav.addEventListener("click", function (e) {
      if (e.target.closest("a")) {
        nav.classList.remove("open");
        btn.setAttribute("aria-expanded", "false");
        btn.textContent = btn.dataset.open;
      }
    });
  }

  /* scroll reveal */
  var revealed = document.querySelectorAll("[data-reveal]");
  if ("IntersectionObserver" in window && revealed.length) {
    var io = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (en) {
          if (en.isIntersecting) {
            en.target.classList.add("is-in");
            io.unobserve(en.target);
          }
        });
      },
      { rootMargin: "0px 0px -8% 0px", threshold: 0.05 }
    );
    revealed.forEach(function (el) { io.observe(el); });
  } else {
    revealed.forEach(function (el) { el.classList.add("is-in"); });
  }

  /* work gallery filter */
  var filterWrap = document.querySelector(".filters");
  if (filterWrap) {
    var items = document.querySelectorAll(".masonry .item");
    filterWrap.addEventListener("click", function (e) {
      var b = e.target.closest(".filter-btn");
      if (!b) return;
      filterWrap.querySelectorAll(".filter-btn").forEach(function (x) {
        x.classList.toggle("active", x === b);
      });
      var cat = b.dataset.filter;
      items.forEach(function (it) {
        it.classList.toggle("hide", cat !== "all" && it.dataset.cat !== cat);
      });
    });
  }
})();
