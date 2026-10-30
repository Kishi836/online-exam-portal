// FR-028: tell the server each time the examination window loses focus. The request carries no time;
// the server stamps it (UT_067). Loaded by the attempt page with data-focus-url set on <body>.
(() => {
  const url = document.body.dataset.focusUrl;
  if (!url) {
    return;
  }
  const csrf = document.querySelector("input[name=csrfmiddlewaretoken]");

  // TODO(Kartik):
  // 1. A function report() that POSTs to `url` with the CSRF token in a FormData body (like paper.html does),
  //    using fetch(url, { method: "POST", body, keepalive: true }) so it is still sent while the tab hides.
  // 2. One tab switch fires BOTH "blur" and "visibilitychange" -- it must create ONE event (UT_064).
  //    Keep a flag `away`: on loss (document.hidden, or window blur) report only if !away, then set away = true;
  //    on return (visible again, or window focus) set away = false. Three switches -> three events (UT_065).
  // 3. Clicking inside the page (radio buttons, palette links) must never report (UT_066):
  //    in-page clicks do not blur the window, so do NOT listen to element-level blur/focusout.
})();
