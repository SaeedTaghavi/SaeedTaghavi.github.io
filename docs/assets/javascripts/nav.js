// The "top" of a page is where its rounded navigation bar sits just under
// Material's header. Home is the exception: its top is the banner itself.
//
// Pages other than Home open scrolled to that position; links with a #fragment
// and restored scroll positions are left alone. The Top button appears once the
// reader has scrolled well past it, and brings them back.
//
// .st-pill-anchor is an empty element right before the bar. The bar itself is
// sticky, so once pinned its own position no longer says where it started.

function pageTop() {
  const pill = document.querySelector(".st-pill");
  const anchor = document.querySelector(".st-pill-anchor");
  if (!pill || !anchor || pill.dataset.home === "true") return 0;
  const header = document.querySelector(".md-header");
  const offset = (header ? header.offsetHeight : 0) + 8;
  const overlap = parseFloat(getComputedStyle(pill).marginTop) || 0;
  const top = anchor.getBoundingClientRect().top + window.scrollY + overlap - offset;
  return Math.max(0, Math.round(top));
}

document$.subscribe(() => {
  const pill = document.querySelector(".st-pill");
  if (pill && pill.dataset.home !== "true" && !location.hash && window.scrollY === 0) {
    window.scrollTo({ top: pageTop(), behavior: "instant" });
  }

  const button = document.querySelector(".st-top");
  if (!button || button.dataset.ready) return;
  button.dataset.ready = "true";

  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
  let queued = false;
  const update = () => {
    queued = false;
    const visible = window.scrollY > pageTop() + window.innerHeight * 0.6;
    button.classList.toggle("is-visible", visible);
  };
  window.addEventListener(
    "scroll",
    () => {
      if (!queued) {
        queued = true;
        requestAnimationFrame(update);
      }
    },
    { passive: true }
  );
  window.addEventListener("resize", update, { passive: true });
  update();

  button.addEventListener("click", () => {
    window.scrollTo({ top: pageTop(), behavior: reduceMotion.matches ? "instant" : "smooth" });
  });
});
