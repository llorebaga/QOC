/* QOC — open problems: filter the server-rendered list by status, topic and keyword (kept in the URL query). */
(function () {
  "use strict";

  const root = document.querySelector("[data-problems]");
  if (!root) return;

  const buttons = [...root.querySelectorAll("[data-status]")].filter((el) => el.tagName === "BUTTON");
  const select = root.querySelector("select[name=topic]");
  const input = root.querySelector("input[name=q]");
  const status = root.querySelector("[data-problems-status]");
  const cards = [...root.querySelectorAll("[data-problems-list] > li")];
  const fold = (s) => s.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase();
  const haystacks = new Map(cards.map((c) => [c, fold(c.textContent)]));
  const LABELS = { open: "open", partial: "with partial progress", solved: "solved" };

  const params = new URLSearchParams(location.search);
  let state = params.get("status") || "";
  if (!(state in LABELS)) state = "";
  if (select && [...select.options].some((o) => o.value === params.get("topic"))) select.value = params.get("topic");
  if (input && params.get("q")) input.value = params.get("q");

  function apply() {
    const topic = select ? select.value : "";
    const rawQ = input ? input.value.trim() : "";
    const terms = rawQ ? fold(rawQ).split(/\s+/).filter(Boolean) : [];
    let shown = 0;
    for (const card of cards) {
      const hay = haystacks.get(card);
      const ok = (!state || card.dataset.status === state) &&
                 (!topic || card.dataset.topics.split(" ").includes(topic)) &&
                 terms.every((t) => hay.includes(t));
      card.hidden = !ok;
      if (ok) shown++;
    }
    for (const b of buttons) b.setAttribute("aria-pressed", String(b.dataset.status === state));
    const what = shown === 1 ? "problem" : "problems";
    const topicName = topic ? select.options[select.selectedIndex].text.replace(/\s*\(\d+\)$/, "") : "";
    status.textContent = `${shown} ${what}${state ? " " + LABELS[state] : ""}${topicName ? " on " + topicName : ""}${rawQ ? ` matching “${rawQ}”` : ""}.`;

    const q = new URLSearchParams();
    if (state) q.set("status", state);
    if (topic) q.set("topic", topic);
    if (rawQ) q.set("q", rawQ);
    history.replaceState(null, "", q.toString() ? `?${q}` : location.pathname);
  }

  for (const b of buttons) b.addEventListener("click", () => { state = b.dataset.status; apply(); });
  if (select) select.addEventListener("change", apply);
  if (input) input.addEventListener("input", apply);
  root.querySelector("[data-problems-form]").addEventListener("submit", (e) => e.preventDefault());
  apply();
})();
