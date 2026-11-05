// Filter buttons and text search for lists marked with data-filter-list.
// Each item carries data-type / data-theme / data-audience attributes and
// a data-text attribute that the search box matches against.
function setupFilters() {
  document.querySelectorAll("[data-filter-list]").forEach((root) => {
    const items = root.querySelectorAll("[data-item]");
    const count = root.querySelector("[data-count]");
    const search = root.querySelector("input[type='search']");
    const state = {};

    const apply = () => {
      const needle = search ? search.value.trim().toLowerCase() : "";
      let shown = 0;
      items.forEach((item) => {
        const ok =
          Object.entries(state).every(
            ([key, value]) => value === "all" || item.dataset[key] === value
          ) && (!needle || item.dataset.text.includes(needle));
        item.hidden = !ok;
        if (ok) shown += 1;
      });
      if (count) count.textContent = shown === 1 ? "1 entry" : `${shown} entries`;
    };

    root.querySelectorAll("button[data-key]").forEach((button) => {
      const key = button.dataset.key;
      if (!(key in state)) state[key] = "all";
      button.addEventListener("click", () => {
        state[key] = button.dataset.value;
        root
          .querySelectorAll(`button[data-key='${key}']`)
          .forEach((b) => b.setAttribute("aria-pressed", String(b === button)));
        apply();
      });
    });
    if (search) search.addEventListener("input", apply);
    apply();
  });
}

document$.subscribe(setupFilters);
