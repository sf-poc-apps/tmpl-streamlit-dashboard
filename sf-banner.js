/* SF-POC-BANNER. Required on every page. Do not remove or restyle. */
(function () {
  var cfg = window.SF || {};
  var expires = cfg.expires ? new Date(cfg.expires).toLocaleDateString() : "soon";
  var bar = document.createElement("div");
  bar.id = "sf-banner";
  bar.setAttribute("role", "note");
  bar.style.cssText = "position:sticky;top:0;z-index:2147483647;background:#4b1f7a;color:#fff;font:600 13px/1.4 system-ui,sans-serif;padding:6px 12px;text-align:center";
  bar.textContent = "POC built by an AI software factory" + (cfg.env === "staging" ? " (staging)" : "") +
    " - expires on " + expires + ". Do not enter personal or confidential data.";
  document.addEventListener("DOMContentLoaded", function () { document.body.prepend(bar); });
  // A page without an icon makes the browser ask for /favicon.ico and log a 404.
  if (document.head && !document.querySelector('link[rel~="icon"]')) {
    var icon = document.createElement("link");
    icon.rel = "icon";
    icon.href = "data:image/svg+xml," + encodeURIComponent(
      '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect width="32" height="32" rx="7" fill="#4b1f7a"/>' +
      '<path d="M9 21l5-10 4 7 2-3 3 6z" fill="#fff"/></svg>');
    document.head.appendChild(icon);
  }
})();
