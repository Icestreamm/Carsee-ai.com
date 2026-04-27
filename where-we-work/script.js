(function () {
  "use strict";

  /** Active markets — GeoJSON `ADM0_A3` (brand fill for listed countries). */
  const activeAdm0A3 = { JOR: true, SAU: true, ARE: true, EGY: true };

  const currencyByAdm0 = {
    JOR: "JOD",
    SAU: "SAR",
    ARE: "AED",
    EGY: "EGP",
  };

  const i18n = window.WHERE_WE_WORK_I18N || {};

  const BRAND = "#0d3b6e";
  const BRAND_HOVER = "#0d3b6e";
  const BRAND_SEL = "#0d3b6e";
  const MUTED = "#c8ccd0";

  function adm0A3(feature) {
    const p = feature.properties || {};
    return p.ADM0_A3 || p.ISO_A3 || p["ISO3166-1-Alpha-3"] || p.ISO3 || "";
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
  var homeCenter = null;
  var homeZoom = null;
  var snapBackTimer = null;
  var isSnappingBack = false;

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
    dragging: true,
    touchZoom: true,
    doubleClickZoom: true,
    boxZoom: false,
    keyboard: false,
    zoomSnap: 0.1,
    zoomControl: true,
    attributionControl: false,
    maxBoundsViscosity: 1.0,
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

  function scheduleSnapBack() {
    if (!homeCenter || typeof homeZoom !== "number" || isSnappingBack) return;
    if (snapBackTimer) {
      clearTimeout(snapBackTimer);
    }
    snapBackTimer = setTimeout(function () {
      isSnappingBack = true;
      map.flyTo(homeCenter, homeZoom, { animate: true, duration: 0.45 });
      setTimeout(function () {
        isSnappingBack = false;
      }, 520);
    }, 120);
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

  const borderCountriesWanted = {
    TCD: true, // Chad (ISO; geo-countries uses TCD, not Natural Earth CHD)
    CAF: true, // Central African Republic
    ETH: true, // Ethiopia
    ERI: true, // Eritrea
    DJI: true, // Djibouti
    SOM: true, // Somalia
    KEN: true, // Kenya
    BGR: true, // Bulgaria
    GRC: true, // Greece
    GEO: true, // Georgia
    TKM: true, // Turkmenistan
    AFG: true, // Afghanistan
    LBY: true, // Libya
    SDN: true, // Sudan
    SSD: true, // South Sudan
    SOL: true, // Somaliland
    YEM: true, // Yemen
    PAK: true, // Pakistan
    ISR: true,
    PSE: true,
    LBN: true,
    SYR: true,
    IRQ: true,
    KWT: true,
    QAT: true,
    OMN: true,
  };

  function renderMap(dataset) {
    const feats = (dataset.features || []).slice();
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

    /* Wide enough for Horn of Africa, eastern Med / Balkans, Caucasus, and Turkmenistan */
    var fixedViewBounds = L.latLngBounds([-4.8, 12.0], [45.8, 67.2]);
    var fullRegionBounds = L.geoJSON(dataset).getBounds();
    var fitBounds = fixedViewBounds;
    if ((!fitBounds || !fitBounds.isValid()) && fullRegionBounds && fullRegionBounds.isValid()) {
      fitBounds = fullRegionBounds;
    } else if ((!fitBounds || !fitBounds.isValid()) && activeFeats.length) {
      fitBounds = L.geoJSON({ type: "FeatureCollection", features: activeFeats }).getBounds();
    }
    if (fitBounds && fitBounds.isValid()) {
      var isMobile = window.matchMedia("(max-width: 900px)").matches;
      map.fitBounds(fitBounds, {
        padding: isMobile ? [16, 16] : [32, 32],
        maxZoom: isMobile ? 7 : 6,
        animate: false,
      });
      var lockedZoom = map.getZoom();
      // Extra zoom-in from current setting for a tighter default view.
      var targetZoom = lockedZoom + 1.1;
      map.setZoom(targetZoom, { animate: false });
      map.panBy([Math.round(map.getSize().x * 0.1), -Math.round(map.getSize().y * 0.1)], { animate: false }); // shift right ~10% and up ~10%
      homeCenter = map.getCenter();
      homeZoom = map.getZoom();
      map.setMinZoom(targetZoom - 0.8);
      map.setMaxZoom(targetZoom + 0.8);
      map.setMaxBounds(fitBounds.pad(0.02));
    }

    map.on("dragend", function () {
      scheduleSnapBack();
    });
    map.on("zoomend", function () {
      scheduleSnapBack();
    });

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
  }

  function ensureBorderCountries(dataset) {
    var existing = {};
    (dataset.features || []).forEach(function (f) {
      existing[adm0A3(f)] = true;
    });

    var missing = Object.keys(borderCountriesWanted).filter(function (code) {
      return !existing[code];
    });

    if (!missing.length) return Promise.resolve(dataset);

    return fetch("https://raw.githubusercontent.com/datasets/geo-countries/master/data/countries.geojson")
      .then(function (r) {
        return r.ok ? r.json() : null;
      })
      .then(function (world) {
        if (!world || !world.features) return dataset;
        var added = [];
        for (var i = 0; i < world.features.length; i++) {
          var f = world.features[i];
          var code = adm0A3(f);
          var p = f.properties || {};
          var adminName = String(p.ADMIN || p.NAME || p.NAME_LONG || "").toLowerCase();
          var isSomalilandByName = adminName.indexOf("somaliland") !== -1;
          if ((borderCountriesWanted[code] || isSomalilandByName) && !existing[code]) {
            added.push(f);
            existing[code] = true;
          }
        }
        if (!added.length) return dataset;
        return { type: "FeatureCollection", features: (dataset.features || []).concat(added) };
      })
      .catch(function () {
        return dataset;
      });
  }

  function addManualFallbackRegions(dataset) {
    var feats = (dataset && dataset.features) ? dataset.features.slice() : [];
    var hasSomaliland = feats.some(function (f) {
      var code = adm0A3(f);
      var p = f.properties || {};
      var n = String(p.ADMIN || p.NAME || p.NAME_LONG || "").toLowerCase();
      return code === "SOL" || n.indexOf("somaliland") !== -1;
    });
    if (hasSomaliland) return dataset;

    feats.push({
      type: "Feature",
      properties: {
        ADMIN: "Somaliland",
        NAME: "Somaliland",
        NAME_LONG: "Somaliland",
        ADM0_A3: "SOL",
        ISO_A3: "SOL",
      },
      geometry: {
        type: "Polygon",
        coordinates: [[
          [43.25, 11.46],
          [43.7, 11.4],
          [44.5, 11.1],
          [45.3, 11.3],
          [46.0, 11.2],
          [47.0, 11.1],
          [48.0, 11.0],
          [48.9, 10.5],
          [49.2, 10.0],
          [49.0, 9.5],
          [48.9, 9.0],
          [48.0, 8.2],
          [47.0, 8.0],
          [46.0, 7.9],
          [45.0, 8.0],
          [44.0, 8.1],
          [43.5, 8.3],
          [43.0, 9.0],
          [42.8, 9.6],
          [42.6, 10.3],
          [43.0, 10.9],
          [43.25, 11.46],
        ]],
      },
    });

    return { type: "FeatureCollection", features: feats };
  }

  ensureBorderCountries(data).then(addManualFallbackRegions).then(renderMap);

  // Subtle hover/parallax feedback on desktop.
  var hoverMaxPx = 6;
  function onShellMove(ev) {
    if (!shell) return;
    var rect = shell.getBoundingClientRect();
    var x = ((ev.clientX - rect.left) / rect.width - 0.5) * 2;
    var y = ((ev.clientY - rect.top) / rect.height - 0.5) * 2;
    var tx = Math.round(x * hoverMaxPx * 10) / 10;
    var ty = Math.round(y * hoverMaxPx * 10) / 10;
    shell.style.transform = "translate(" + tx + "px, " + ty + "px)";
  }

  if (shell && window.matchMedia("(hover: hover) and (pointer: fine)").matches) {
    shell.style.transition = "opacity 380ms ease, transform 220ms ease";
    shell.addEventListener("mousemove", onShellMove);
    shell.addEventListener("mouseleave", function () {
      shell.style.transform = "translate(0px, 0px)";
    });
  }
})();
