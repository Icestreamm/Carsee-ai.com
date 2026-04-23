(function () {
  if (!document.body.classList.contains("home")) return;

  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var nodes = document.querySelectorAll(".idx-reveal");
  if (!nodes.length) return;

  if (reduced) {
    nodes.forEach(function (el) {
      el.classList.add("idx-reveal--visible");
    });
    return;
  }

  var io = new IntersectionObserver(
    function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        entry.target.classList.add("idx-reveal--visible");
        io.unobserve(entry.target);
      });
    },
    { threshold: 0.12, rootMargin: "0px 0px -6% 0px" }
  );

  nodes.forEach(function (el) {
    io.observe(el);
  });
})();
