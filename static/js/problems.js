/* QOC — open problems: filter the server-rendered list by status and topic (kept in the URL query). */
(function () {
  "use strict";

  const root = document.querySelector("[data-problems]");
  if (!root) return;

  const buttons = [...root.querySelectorAll("[data-status]")].filter((el) => el.tagName === "BUTTON");
  const select = root.querySelector("select[name=topic]");
  const status = root.querySelector("[data-problems-status]");
  const cards = [...root.querySelectorAll("[data-problems-list] > li")];
  const LABELS = { open: "open", partial: "with partial progress", solved: "solved" };

  const params = new URLSearchParams(location.search);
  let state = params.get("status") || "";
  if (!(state in LABELS)) state = "";
  if (select && [...select.options].some((o) => o.value === params.get("topic"))) select.value = params.get("topic");

  function apply() {
    const topic = select ? select.value : "";
    let shown = 0;
    for (const card of cards) {
      const ok = (!state || card.dataset.status === state) &&
                 (!topic || card.dataset.topics.split(" ").includes(topic));
      card.hidden = !ok;
      if (ok) shown++;
    }
    for (const b of buttons) b.setAttribute("aria-pressed", String(b.dataset.status === state));
    const what = shown === 1 ? "problem" : "problems";
    const topicName = topic ? select.options[select.selectedIndex].text.replace(/\s*\(\d+\)$/, "") : "";
    status.textContent = `${shown} ${what}${state ? " " + LABELS[state] : ""}${topicName ? " on " + topicName : ""}.`;

    const q = new URLSearchParams();
    if (state) q.set("status", state);
    if (topic) q.set("topic", topic);
    history.replaceState(null, "", q.toString() ? `?${q}` : location.pathname);
  }

  for (const b of buttons) b.addEventListener("click", () => { state = b.dataset.status; apply(); });
  if (select) select.addEventListener("change", apply);
  root.querySelector("[data-problems-form]").addEventListener("submit", (e) => e.preventDefault());
  apply();
})();
