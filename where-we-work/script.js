(function () {
  "use strict";

  /** Active markets — GeoJSON `ADM0_A3` (Jordan, Saudi Arabia, UAE only in brand fill). */
  const activeAdm0A3 = { JOR: true, SAU: true, ARE: true };

  const currencyByAdm0 = {
    JOR: "JOD",
    SAU: "SAR",
    ARE: "AED",
  };

  const i18n = window.WHERE_WE_WORK_I18N || {};

  const BRAND = "#0d3b6e";
  const BRAND_HOVER = "#1a5494";
  const BRAND_SEL = "#164a82";
  const MUTED = "#c8ccd0";

  function adm0A3(feature) {
    const p = feature.properties || {};
    return p.ADM0_A3 || "";
  }

  function isActive(feature) {
    return !!activeAdm0A3[adm0A3(feature)];
  }

  function currencyFor(feature) {
    return currencyByAdm0[adm0A3(feature)] || null;
  }

  /** Natural Earth label point (LABEL_X = lon, LABEL_Y = lat), else polygon centroid. */
  function currencyLabelLatLng(feature) {
    const p = feature.properties || {};
    if (typeof p.LABEL_Y === "number" && typeof p.LABEL_X === "number") {
      return L.latLng(p.LABEL_Y, p.LABEL_X);
    }
    try {
      return L.geoJSON(feature).getBounds().getCenter();
    } catch (e) {
      return null;
    }
  }

  function addFloatingCurrencyLabels(mapInstance, features) {
    var paneName = "wmCurrencyPane";
    if (!mapInstance.getPane(paneName)) {
      mapInstance.createPane(paneName);
      mapInstance.getPane(paneName).style.zIndex = "650";
    }
    for (var i = 0; i < features.length; i++) {
      var feat = features[i];
      var code = currencyFor(feat);
      if (!code) continue;
      var ll = currencyLabelLatLng(feat);
      if (!ll) continue;
      var icon = L.divIcon({
        className: "wm-currency-marker",
        html: '<span class="wm-currency-float">' + code + "</span>",
        iconSize: [56, 34],
        iconAnchor: [28, 17],
      });
      L.marker(ll, { icon: icon, pane: paneName, interactive: false, keyboard: false }).addTo(mapInstance);
    }
  }

  function baseStyle(feature, selected) {
    if (isActive(feature)) {
      return {
        color: selected ? BRAND_SEL : BRAND,
        weight: 0,
        opacity: 0,
        fillColor: selected ? BRAND_SEL : BRAND,
        fillOpacity: selected ? 0.98 : 0.92,
      };
    }
    return {
      color: MUTED,
      weight: 0,
      opacity: 0,
      fillColor: MUTED,
      fillOpacity: selected ? 0.72 : 0.58,
    };
  }

  function hoverStyle(feature) {
    if (!isActive(feature)) {
      return {};
    }
    return {
      color: BRAND_HOVER,
      weight: 0,
      opacity: 0,
      fillColor: BRAND_HOVER,
      fillOpacity: 0.96,
    };
  }

  let selectedLayer = null;
  let selectedFeature = null;

  function applyLayerStyle(layer, feature, mode) {
    if (!layer || !feature) return;
    if (mode === "hover") {
      const selected = layer === selectedLayer;
      layer.setStyle(Object.assign({}, baseStyle(feature, selected), hoverStyle(feature)));
    } else if (mode === "selected") {
      layer.setStyle(baseStyle(feature, true));
    } else {
      layer.setStyle(baseStyle(feature, false));
    }
  }

  const mapEl = document.getElementById("wm-map");
  const shell = document.querySelector(".wm-map-shell");
  const mapError = document.getElementById("wm-map-error");

  if (!mapEl) return;

  function showMapError(title, detail) {
    if (!mapError) return;
    mapError.textContent = [title, detail].filter(Boolean).join(" ");
    mapError.hidden = false;
  }

  function hideMapError() {
    if (!mapError) return;
    mapError.textContent = "";
    mapError.hidden = true;
  }

  const map = L.map(mapEl, {
    scrollWheelZoom: true,
    zoomControl: true,
    attributionControl: false,
    maxBoundsViscosity: 0.85,
  }).setView([24, 47], 5);

  window.addEventListener("load", function () {
    map.invalidateSize();
  });

  function clearSelectionVisual() {
    if (selectedLayer && selectedFeature) {
      applyLayerStyle(selectedLayer, selectedFeature, "base");
    }
    selectedLayer = null;
    selectedFeature = null;
  }

  function onEachActiveFeature(feature, layer) {
    layer.on("mouseover", function () {
      applyLayerStyle(layer, feature, "hover");
    });

    layer.on("mouseout", function () {
      applyLayerStyle(layer, feature, layer === selectedLayer ? "selected" : "base");
    });

    layer.on("click", function (e) {
      if (e.originalEvent) L.DomEvent.stopPropagation(e.originalEvent);
      L.DomEvent.stopPropagation(e);
      if (selectedLayer && selectedLayer !== layer && selectedFeature) {
        applyLayerStyle(selectedLayer, selectedFeature, "base");
      }
      selectedLayer = layer;
      selectedFeature = feature;
      applyLayerStyle(layer, feature, "selected");
      layer.bringToFront();
    });
  }

  function addInactiveLayer(geojson) {
    return L.geoJSON(geojson, {
      interactive: false,
      style: function (feature) {
        return baseStyle(feature, false);
      },
    }).addTo(map);
  }

  function addActiveLayer(geojson) {
    return L.geoJSON(geojson, {
      style: function (feature) {
        return baseStyle(feature, false);
      },
      onEachFeature: onEachActiveFeature,
    }).addTo(map);
  }

  hideMapError();

  const data = window.WHERE_WE_WORK_REGION_GEOJSON;
  if (!data || !data.features || !data.features.length) {
    showMapError(
      i18n.errorTitle || "Map unavailable",
      i18n.loadError || "Regional map data is missing. Please ensure region-data.js is loaded before this script."
    );
    if (shell) shell.classList.add("is-visible");
    return;
  }

  const feats = (data.features || []).slice();
  feats.sort(function (a, b) {
    return (isActive(a) ? 1 : 0) - (isActive(b) ? 1 : 0);
  });

  const inactive = {
    type: "FeatureCollection",
    features: feats.filter(function (f) {
      return !isActive(f);
    }),
  };
  const active = {
    type: "FeatureCollection",
    features: feats.filter(function (f) {
      return isActive(f);
    }),
  };

  addInactiveLayer(inactive);
  const activeGroup = addActiveLayer(active);
  activeGroup.bringToFront();

  const activeFeats = active.features || [];
  addFloatingCurrencyLabels(map, activeFeats);

  var focusBounds = null;
  if (activeFeats.length) {
    focusBounds = L.geoJSON({ type: "FeatureCollection", features: activeFeats }).getBounds();
  }
  if (!focusBounds || !focusBounds.isValid()) {
    focusBounds = L.geoJSON(data).getBounds();
  }
  if (focusBounds.isValid()) {
    map.fitBounds(focusBounds, { padding: [36, 36], maxZoom: 6, animate: false });
    map.setMaxBounds(focusBounds.pad(0.22));
  }

  map.on("click", function (e) {
    var t = e.originalEvent && e.originalEvent.target;
    if (t && typeof t.closest === "function" && t.closest(".leaflet-interactive")) {
      return;
    }
    clearSelectionVisual();
  });

  if (shell) {
    requestAnimationFrame(function () {
      shell.classList.add("is-visible");
    });
  }
})();
