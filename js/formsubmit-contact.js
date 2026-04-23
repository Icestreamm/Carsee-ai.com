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
