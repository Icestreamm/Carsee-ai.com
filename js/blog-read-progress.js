(function () {
  var bar = document.getElementById("csBlogProgress");
  if (bar) {
    bar.setAttribute("role", "progressbar");
    bar.setAttribute("aria-valuemin", "0");
    bar.setAttribute("aria-valuemax", "100");
    bar.removeAttribute("aria-hidden");
    function onScroll() {
      var doc = document.documentElement;
      var h = doc.scrollHeight - doc.clientHeight;
      var pct = h > 0 ? (doc.scrollTop / h) * 100 : 0;
      bar.style.width = pct + "%";
      bar.setAttribute("aria-valuenow", String(Math.round(pct)));
    }
    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();
  }
  var sections = document.querySelectorAll(".cs-blog-root .cs-blog-section");
  if (sections.length && "IntersectionObserver" in window) {
    var io = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (e) {
          if (e.isIntersecting) {
            e.target.classList.add("visible");
            io.unobserve(e.target);
          }
        });
      },
      { threshold: 0.12 }
    );
    sections.forEach(function (s) {
      io.observe(s);
    });
  }
})();
