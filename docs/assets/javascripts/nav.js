// Pages other than Home open scrolled so the rounded navigation bar sits at
// the top of the window, just under Material's header. Scrolling up reveals
// the banner. Links with a #fragment and restored scroll positions are left alone.
document$.subscribe(() => {
  const pill = document.querySelector(".st-pill");
  if (!pill || pill.dataset.home === "true") return;
  if (location.hash || window.scrollY > 0) return;
  const header = document.querySelector(".md-header");
  const offset = (header ? header.offsetHeight : 0) + 8;
  const top = pill.getBoundingClientRect().top + window.scrollY - offset;
  window.scrollTo({ top: Math.max(0, top), behavior: "instant" });
});
