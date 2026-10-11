/* Render LaTeX with KaTeX (loaded before this file via deferred scripts). */
(function () {
  "use strict";
  if (typeof window.renderMathInElement !== "function") return;
  window.renderMathInElement(document.body, {
    delimiters: [
      { left: "$$", right: "$$", display: true },
      { left: "\\(", right: "\\)", display: false },
    ],
    ignoredTags: ["script", "noscript", "style", "textarea", "pre", "code"],
    throwOnError: false,
  });
})();
