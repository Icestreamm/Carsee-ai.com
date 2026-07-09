/**
 * CarSee pricing: starfield, vertical billing pill, effective $/mo in headline price,
 * invoice detail in .js-billed-note. Expects vertical track #psBillingTrack.ps-billing__track--vertical
 */
(function () {
  var root = document.getElementById("psShowcase");
  if (!root) return;

  var canvas = document.getElementById("psStars");
  var track = document.getElementById("psBillingTrack");
  var pill = document.getElementById("psBillingPill");
  if (!canvas || !track || !pill) return;

  /** Invoice totals (USD) */
  var totals = {
    pro: { monthly: 6.99, quarterly: 18.99, annual: 69.99 },
    plus: { monthly: 9.99, quarterly: 24.99, annual: 89.99 },
  };

  function effectivePerMonth(plan, period) {
    var t = totals[plan][period];
    if (period === "monthly") return t;
    if (period === "quarterly") return t / 3;
    return t / 12;
  }

  function formatUsd(amount) {
    var n = Math.round(amount * 100) / 100;
    return "$" + n.toFixed(2);
  }

  function lang() {
    return document.documentElement.lang === "ar" ? "ar" : "en";
  }

  function currentPeriod() {
    var active = track.querySelector(".ps-billing__btn.active");
    return active ? active.getAttribute("data-period") : "annual";
  }

  var isVertical = function () {
    return track.classList.contains("ps-billing__track--vertical");
  };

  function movePill() {
    var active = track.querySelector(".ps-billing__btn.active");
    if (!active) return;
    if (isVertical()) {
      pill.style.width = "calc(100% - 8px)";
      pill.style.height = active.offsetHeight + "px";
      pill.style.transform = "translateY(" + active.offsetTop + "px)";
      pill.style.left = "4px";
      pill.style.top = "4px";
    } else {
      pill.style.width = active.offsetWidth + "px";
      pill.style.height = "calc(100% - 8px)";
      pill.style.transform = "translateX(" + active.offsetLeft + "px)";
      pill.style.top = "4px";
      pill.style.left = "4px";
    }
  }

  var billed = {
    en: {
      free: "No payment required.",
      pro: {
        monthly: "Billed $6.99 per month.",
        quarterly: "Billed $18.99 every 3 months (shown: monthly equivalent).",
        annual: "Billed $69.99 per year (shown: monthly equivalent).",
      },
      plus: {
        monthly: "Billed $9.99 per month.",
        quarterly: "Billed $24.99 every 3 months (shown: monthly equivalent).",
        annual: "Billed $89.99 per year (shown: monthly equivalent).",
      },
    },
    ar: {
      free: "لا دفع مطلوب.",
      pro: {
        monthly: "يتم الدفع 6.99$ شهرياً.",
        quarterly: "يتم الدفع 18.99$ كل 3 أشهر (المعروض: ما يعادله شهرياً).",
        annual: "يتم الدفع 69.99$ سنوياً (المعروض: ما يعادله شهرياً).",
      },
      plus: {
        monthly: "يتم الدفع 9.99$ شهرياً.",
        quarterly: "يتم الدفع 24.99$ كل 3 أشهر (المعروض: ما يعادله شهرياً).",
        annual: "يتم الدفع 89.99$ سنوياً (المعروض: ما يعادله شهرياً).",
      },
    },
  };

  function updatePrices() {
    var period = currentPeriod();
    var lg = lang();

    document.querySelectorAll('.price-amount[data-plan="pro"]').forEach(function (el) {
      el.textContent = formatUsd(effectivePerMonth("pro", period));
    });
    document.querySelectorAll('.price-amount[data-plan="plus"]').forEach(function (el) {
      el.textContent = formatUsd(effectivePerMonth("plus", period));
    });

    document.querySelectorAll(".ps-price-suffix").forEach(function (el) {
      el.textContent = lg === "ar" ? "/شهر" : "/mo";
    });

    document.querySelectorAll(".plan-card[data-plan]").forEach(function (card) {
      var plan = card.getAttribute("data-plan");
      var note = card.querySelector(".js-billed-note");
      if (!note) return;
      if (plan === "free") {
        note.textContent = billed[lg].free;
        return;
      }
      if (plan === "pro" || plan === "plus") {
        note.textContent = billed[lg][plan][period];
      }
    });
  }

  function fireConfetti() {
    if (typeof confetti !== "function") return;
    var active = track.querySelector('.ps-billing__btn[data-period="annual"]');
    if (!active) return;
    var rect = active.getBoundingClientRect();
    confetti({
      particleCount: 72,
      spread: 70,
      origin: {
        x: (rect.left + rect.width / 2) / window.innerWidth,
        y: (rect.top + rect.height / 2) / window.innerHeight,
      },
      colors: ["#00d4f5", "#ffffff", "#0097b2", "#f5a623"],
      ticks: 280,
      gravity: 1.1,
      decay: 0.94,
      startVelocity: 28,
    });
  }

  track.querySelectorAll(".ps-billing__btn").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var next = btn.getAttribute("data-period");
      var prev = currentPeriod();
      track.querySelectorAll(".ps-billing__btn").forEach(function (b) {
        b.classList.remove("active");
      });
      btn.classList.add("active");
      requestAnimationFrame(function () {
        movePill();
        updatePrices();
      });
      if (next === "annual" && prev !== "annual") {
        requestAnimationFrame(fireConfetti);
      }
    });
  });

  var ctx = canvas.getContext("2d");
  var stars = [];
  var i;
  for (i = 0; i < 130; i++) {
    stars.push({
      x: Math.random(),
      y: Math.random(),
      r: Math.random() * 1.4 + 0.25,
      tw: Math.random() * Math.PI * 2,
      sp: 0.4 + Math.random() * 1.6,
    });
  }

  var mx = 0.5;
  var my = 0.5;

  root.addEventListener(
    "mousemove",
    function (e) {
      var r = root.getBoundingClientRect();
      mx = (e.clientX - r.left) / Math.max(r.width, 1);
      my = (e.clientY - r.top) / Math.max(r.height, 1);
    },
    { passive: true }
  );

  root.addEventListener("mouseleave", function () {
    mx = 0.5;
    my = 0.5;
  });

  function resizeCanvas() {
    var dpr = Math.min(window.devicePixelRatio || 1, 2);
    var w = root.clientWidth;
    var h = root.clientHeight;
    canvas.width = Math.floor(w * dpr);
    canvas.height = Math.floor(h * dpr);
    canvas.style.width = w + "px";
    canvas.style.height = h + "px";
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  }

  var ro = new ResizeObserver(function () {
    resizeCanvas();
    movePill();
  });
  ro.observe(root);

  function tick(t) {
    var w = root.clientWidth;
    var h = root.clientHeight;
    if (w < 1 || h < 1) {
      requestAnimationFrame(tick);
      return;
    }
    ctx.clearRect(0, 0, w, h);
    var tsec = t * 0.001;
    var parallax = 18;
    stars.forEach(function (s) {
      var dx = (mx - 0.5) * parallax * s.sp;
      var dy = (my - 0.5) * parallax * s.sp;
      var px = s.x * w + dx;
      var py = s.y * h + dy;
      var alpha = 0.28 + 0.5 * Math.sin(tsec * s.sp + s.tw);
      ctx.fillStyle = "rgba(255,255,255," + alpha + ")";
      ctx.beginPath();
      ctx.arc(px, py, s.r, 0, Math.PI * 2);
      ctx.fill();
    });
    requestAnimationFrame(tick);
  }

  resizeCanvas();
  movePill();
  updatePrices();
  requestAnimationFrame(tick);

  window.psRefreshBilling = function () {
    movePill();
    updatePrices();
  };
})();
