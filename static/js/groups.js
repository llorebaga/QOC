/* QOC — research groups: Leaflet world map (marker clusters) + filters shared with the server-rendered list. */
(function () {
  "use strict";

  const root = document.querySelector("[data-groups]");
  const dataEl = document.getElementById("groups-data");
  if (!root || !dataEl) return;

  const groups = JSON.parse(dataEl.textContent);
  const form = root.querySelector("[data-groups-form]");
  const status = root.querySelector("[data-groups-status]");
  const cards = new Map([...root.querySelectorAll("[data-group]")].map((el) => [el.dataset.group, el]));
  const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  const fold = (s) => s.normalize("NFD").replace(/[̀-ͯ]/g, "").toLowerCase();

  /* ------------------------------------------------------------ map */
  let map = null, cluster = null;
  const markers = new Map();
  const mapEl = root.querySelector("[data-groups-map]");

  function initMap() {
    if (!window.L || !mapEl) return;
    map = L.map(mapEl, { scrollWheelZoom: false, worldCopyJump: true, minZoom: 2 }).setView([35, 10], 2);
    L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
      maxZoom: 18,
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    }).addTo(map);
    cluster = L.markerClusterGroup ? L.markerClusterGroup({ showCoverageOnHover: false, maxClusterRadius: 40 }) : L.layerGroup();
    groups.forEach((g) => {
      const m = L.marker([g.lat, g.lon], { title: g.name, alt: g.name });
      m.bindPopup(`<p class="map-pop-title"><a href="${g.url}">${esc(g.name)}</a></p>
        <p class="map-pop-meta">${esc(g.pis.join(", "))}<br>${esc(g.institution)}, ${esc(g.place)}</p>
        ${g.labels.length ? `<p class="map-pop-topics">${g.labels.map(esc).join(" · ")}</p>` : ""}`);
      markers.set(g.id, m);
    });
    map.addLayer(cluster);
    map.on("click", () => map.scrollWheelZoom.enable());
    mapEl.addEventListener("mouseleave", () => map.scrollWheelZoom.disable());
  }

  /* ------------------------------------------------------------ filters */
  function apply() {
    const q = fold(form.elements.q.value.trim());
    const topic = form.elements.topic.value;
    const platform = form.elements.platform.value;
    const kind = form.elements.kind.value;
    const visible = groups.filter((g) => {
      if (topic && !g.topics.includes(topic)) return false;
      if (platform && !g.platforms.includes(platform)) return false;
      if (kind && g.kind !== kind && g.kind !== "both") return false;
      if (q && !fold([g.name, g.pis.join(" "), g.institution, g.place].join(" ")).includes(q)) return false;
      return true;
    });
    const ids = new Set(visible.map((g) => g.id));
    cards.forEach((el, id) => { el.hidden = !ids.has(id); });
    if (cluster) {
      cluster.clearLayers();
      visible.forEach((g) => cluster.addLayer(markers.get(g.id)));
    }
    status.textContent = `${visible.length} group${visible.length === 1 ? "" : "s"}` +
      (visible.length < groups.length ? ` of ${groups.length}.` : ".");
  }

  form.addEventListener("input", apply);
  form.addEventListener("submit", (e) => e.preventDefault());

  initMap();
  apply();

  // groups/#<id>: open that group's marker (link from each group page)
  const target = decodeURIComponent(window.location.hash.slice(1));
  if (target && markers.has(target) && map) {
    const m = markers.get(target);
    const show = () => { map.setView(m.getLatLng(), 7); m.openPopup(); };
    if (cluster.zoomToShowLayer) cluster.zoomToShowLayer(m, () => m.openPopup()); else show();
    mapEl.scrollIntoView({ block: "center" });
  }
})();
