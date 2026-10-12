/* QOC — research groups: a plain world map (Natural Earth country outlines drawn by Leaflet, no tiles)
   with clustered group markers, and filters shared with the server-rendered list. */
(function () {
  "use strict";

  const root = document.querySelector("[data-groups]");
  const dataEl = document.getElementById("groups-data");
  if (!root || !dataEl) return;

  const groups = JSON.parse(dataEl.textContent);
  const form = root.querySelector("[data-groups-form]");
  const status = root.querySelector("[data-groups-status]");
  const mapEl = document.querySelector("[data-groups-map]");
  const cards = new Map([...document.querySelectorAll("[data-group]")].map((el) => [el.dataset.group, el]));
  const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  const fold = (s) => s.normalize("NFD").replace(/[̀-ͯ]/g, "").toLowerCase();
  const css = (name) => getComputedStyle(document.documentElement).getPropertyValue(name).trim();

  /* ------------------------------------------------------------ map */
  let map = null, cluster = null, land = null;
  const markers = new Map();
  const WORLD = [[-56, -168], [76, 190]];

  function landStyle() {
    return { color: css("--bg"), weight: 0.8, fillColor: css("--line-strong"), fillOpacity: 1 };
  }

  function initMap() {
    if (!window.L || !mapEl) return;
    map = L.map(mapEl, {
      zoomSnap: 0.25, minZoom: 1, maxZoom: 9, scrollWheelZoom: false, attributionControl: true,
      maxBounds: [[-75, -220], [85, 240]], maxBoundsViscosity: 0.8, worldCopyJump: false,
    });
    map.fitBounds(WORLD);
    map.attributionControl.setPrefix(false).addAttribution('Countries: <a href="https://www.naturalearthdata.com/">Natural Earth</a>');
    map.on("click", () => map.scrollWheelZoom.enable());
    mapEl.addEventListener("mouseleave", () => map.scrollWheelZoom.disable());
    window.addEventListener("resize", () => map.invalidateSize());

    // country outlines (TopoJSON from world-atlas, verified with its SRI hash)
    if (window.topojson && mapEl.dataset.world) {
      fetch(mapEl.dataset.world, { integrity: mapEl.dataset.worldIntegrity, mode: "cors" })
        .then((r) => r.json())
        .then((topo) => {
          const geo = topojson.feature(topo, topo.objects.countries);
          // drop Antarctica; rings that cross the antimeridian (Russia, Fiji) are shifted east so they draw as one shape
          geo.features = geo.features.filter((f) => f.id !== "010");
          const fixRing = (ring) => {
            const lons = ring.map((c) => c[0]);
            return Math.max(...lons) - Math.min(...lons) > 180 ? ring.map(([x, y]) => [x < 0 ? x + 360 : x, y]) : ring;
          };
          geo.features.forEach((f) => {
            const g = f.geometry;
            if (g.type === "Polygon") g.coordinates = g.coordinates.map(fixRing);
            else if (g.type === "MultiPolygon") g.coordinates = g.coordinates.map((p) => p.map(fixRing));
          });
          land = L.geoJSON(geo, { style: landStyle, interactive: false }).addTo(map);
          land.bringToBack();
        })
        .catch(() => mapEl.classList.add("no-outlines"));
    }

    const dot = L.divIcon({ className: "group-dot", iconSize: [14, 14], iconAnchor: [7, 7], popupAnchor: [0, -6] });
    cluster = L.markerClusterGroup
      ? L.markerClusterGroup({
          showCoverageOnHover: false, maxClusterRadius: 36, spiderfyDistanceMultiplier: 1.4,
          iconCreateFunction: (c) => {
            const n = c.getChildCount();
            const size = n < 5 ? 28 : n < 15 ? 34 : 40;
            return L.divIcon({ html: `<span>${n}</span>`, className: "group-cluster", iconSize: [size, size] });
          },
        })
      : L.layerGroup();
    groups.forEach((g) => {
      const m = L.marker([g.lat, g.lon], { icon: dot, title: g.name, alt: g.name, keyboard: true });
      m.bindPopup(`<p class="map-pop-title"><a href="${g.url}">${esc(g.name)}</a></p>
        <p class="map-pop-meta">${esc(g.pis.join(", "))}<br>${esc(g.institution)}, ${esc(g.place)}</p>
        ${g.labels.length ? `<p class="map-pop-topics">${g.labels.map(esc).join(" · ")}</p>` : ""}`);
      markers.set(g.id, m);
    });
    map.addLayer(cluster);

    // follow the site's light/dark theme
    const restyle = () => land && land.setStyle(landStyle);
    document.addEventListener("qoc:theme", () => setTimeout(restyle, 0));
    window.matchMedia("(prefers-color-scheme: dark)").addEventListener("change", restyle);
  }

  /* ------------------------------------------------------------ filters */
  function apply() {
    const q = fold(form.elements.q.value.trim());
    const topic = form.elements.topic.value;
    const platform = form.elements.platform.value;
    const visible = groups.filter((g) => {
      if (topic && !g.topics.includes(topic)) return false;
      if (platform && !g.platforms.includes(platform)) return false;
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
    if (cluster.zoomToShowLayer) cluster.zoomToShowLayer(m, () => m.openPopup());
    else { map.setView(m.getLatLng(), 6); m.openPopup(); }
    mapEl.scrollIntoView({ block: "center" });
  }
})();
