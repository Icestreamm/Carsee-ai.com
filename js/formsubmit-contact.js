(function () {

  function wireForm(form, warn) {

    if (!form) return;



    var isFile = location.protocol === "file:";



    function showFileProtocolHelp() {

      if (!warn) return;

      warn.hidden = false;

      warn.setAttribute("tabindex", "-1");

      try {

        warn.focus({ preventScroll: true });

      } catch (e) {

        warn.focus();

      }

      warn.scrollIntoView({ behavior: "smooth", block: "nearest" });

    }



    if (isFile && warn) {

      showFileProtocolHelp();

    }



    if (isFile) {

      form.addEventListener("submit", function (e) {

        e.preventDefault();

        showFileProtocolHelp();

      });

    }



    var urlField = form.querySelector('input[name="_url"]');

    if (urlField && (location.protocol === "http:" || location.protocol === "https:")) {

      urlField.value = location.href.split("#")[0];

    }

    function isArabicPage() {
      var html = document.documentElement || {};
      var lang = (html.lang || "").toLowerCase();
      return lang.indexOf("ar") === 0 || html.dir === "rtl";
    }

    function upsertFormMessage(kind, text) {
      var id = "contactInlineStatus";
      var box = document.getElementById(id);
      if (!box) {
        box = document.createElement("div");
        box.id = id;
        box.setAttribute("role", "status");
        box.setAttribute("aria-live", "polite");
        box.style.marginTop = "14px";
        box.style.padding = "12px 14px";
        box.style.borderRadius = "8px";
        box.style.fontSize = "14px";
        box.style.lineHeight = "1.55";
        form.appendChild(box);
      }
      if (kind === "ok") {
        box.style.background = "#e8f7ee";
        box.style.border = "1px solid #28a745";
        box.style.color = "#145c2a";
      } else {
        box.style.background = "#fdecec";
        box.style.border = "1px solid #dc3545";
        box.style.color = "#7a1f27";
      }
      box.textContent = text;
    }

    // Keep contact form on same page and show inline status.
    if (form.id === "contactForm" && (location.protocol === "http:" || location.protocol === "https:")) {
      form.addEventListener("submit", function (e) {
        e.preventDefault();
        var submitBtn = form.querySelector('button[type="submit"]');
        var oldBtnText = submitBtn ? submitBtn.textContent : "";
        if (submitBtn) {
          submitBtn.disabled = true;
          submitBtn.textContent = isArabicPage() ? "جارٍ الإرسال..." : "Sending...";
        }

        fetch(form.action, {
          method: "POST",
          body: new FormData(form),
          headers: {
            Accept: "application/json",
          },
        })
          .then(function (res) {
            if (!res.ok) throw new Error("submit_failed");
            form.reset();
            upsertFormMessage(
              "ok",
              isArabicPage()
                ? "تم إرسال رسالتك بنجاح. سنقوم بالتواصل معك قريبًا."
                : "Your message has been sent successfully. We will contact you shortly."
            );
          })
          .catch(function () {
            upsertFormMessage(
              "err",
              isArabicPage()
                ? "تعذر إرسال الرسالة الآن. يرجى المحاولة مرة أخرى بعد قليل."
                : "We couldn't send your message right now. Please try again in a moment."
            );
          })
          .finally(function () {
            if (submitBtn) {
              submitBtn.disabled = false;
              submitBtn.textContent = oldBtnText;
            }
          });
      });
    }

  }



  wireForm(

    document.getElementById("contactForm"),

    document.getElementById("contactFileProtocolWarn")

  );

  wireForm(

    document.getElementById("careerGeneralInquiriesForm"),

    document.getElementById("careerFileProtocolWarn")

  );

})();

