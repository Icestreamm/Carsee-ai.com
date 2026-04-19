/**
 * Count-up animation for .sol-stats-bar metrics (runs once when the bar enters view).
 * Use data-stat-target (number), optional data-stat-suffix, data-stat-less-than for a final "<N" display.
 */
(function () {
    function easeOutCubic(t) {
        return 1 - Math.pow(1 - t, 3);
    }

    function animateStat(el, target, durationMs, delayMs, lessThan, suffix) {
        window.setTimeout(function () {
            var start = performance.now();
            function tick(now) {
                var t = Math.min(1, (now - start) / durationMs);
                var eased = easeOutCubic(t);
                var raw = eased * target;
                if (lessThan) {
                    el.textContent = t >= 1 ? "<" + String(Math.round(target)) : String(Math.round(raw));
                } else {
                    var n = t >= 1 ? Math.round(target) : Math.round(raw);
                    el.textContent = String(n) + suffix;
                }
                if (t < 1) {
                    requestAnimationFrame(tick);
                }
            }
            requestAnimationFrame(tick);
        }, delayMs);
    }

    function runBar(bar) {
        var nums = bar.querySelectorAll(".sol-stat-num[data-stat-target]");
        if (!nums.length) return;
        nums.forEach(function (el, i) {
            var target = parseFloat(el.getAttribute("data-stat-target"), 10);
            if (Number.isNaN(target)) return;
            var lessThan = el.getAttribute("data-stat-less-than") === "true";
            var suffix = el.getAttribute("data-stat-suffix") || "";
            el.setAttribute("dir", "ltr");
            el.style.fontVariantNumeric = "tabular-nums";
            el.textContent = lessThan ? "0" : "0" + suffix;
            animateStat(el, target, 1200, i * 140, lessThan, suffix);
        });
    }

    var bars = document.querySelectorAll(".sol-stats-bar");
    if (!bars.length) return;

    var io = new IntersectionObserver(
        function (entries) {
            entries.forEach(function (entry) {
                if (!entry.isIntersecting) return;
                var bar = entry.target;
                io.unobserve(bar);
                runBar(bar);
            });
        },
        { threshold: 0.2, rootMargin: "0px 0px -40px 0px" }
    );

    bars.forEach(function (bar) {
        io.observe(bar);
    });
})();
