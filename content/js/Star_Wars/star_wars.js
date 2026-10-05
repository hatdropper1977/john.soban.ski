/* Star Wars etymology visuals for john.soban.ski
   Three interactive figures built from window.SW_DATA (see sw_data.js):
     1. Leaflet map      where the trilogy's vocabulary comes from
     2. D3 timeline      when those words entered English, with a year slider
     3. Cytoscape graph  how speakers, words, etymons and languages connect
   Libraries are loaded from cdnjs by the article; this file only wires them up. */
(function () {
  'use strict';
  var D = window.SW_DATA;
  if (!D) { return; }
  var LANG = D.languages;
  var FAMILY_COLORS = {
    'English': '#3b82f6', 'Germanic': '#22c55e', 'Latin': '#ef4444', 'French': '#f97316',
    'Romance': '#fb7185', 'Greek': '#a855f7', 'Celtic': '#14b8a6', 'Semitic': '#eab308',
    'Iranian & Indic': '#b45309', 'Slavic & Baltic': '#94a3b8', 'Asian & Pacific': '#ec4899',
    'Americas': '#84cc16', 'African': '#f59e0b', 'Proto-Indo-European': '#78716c',
    'Coined': '#fde047', 'Unknown': '#9ca3af', 'Other': '#a3a3a3'
  };
  var FAMILY_ORDER = ['English', 'Germanic', 'Latin', 'French', 'Romance', 'Greek', 'Celtic', 'Semitic',
    'Iranian & Indic', 'Slavic & Baltic', 'Asian & Pacific', 'Americas', 'African', 'Coined', 'Unknown', 'Other'];
  var ENGLISH = { en: 1, enm: 1, 'enm-nor': 1, ang: 1, sco: 1 };
  var FILM_NAME = { IV: 'A New Hope', V: 'The Empire Strikes Back', VI: 'Return of the Jedi' };
  var SPEAKER_NAME = { HAN: 'Han Solo', LUKE: 'Luke Skywalker', LEIA: 'Princess Leia', VADER: 'Darth Vader',
    BEN: 'Obi-Wan Kenobi', THREEPIO: 'C-3PO', YODA: 'Yoda', LANDO: 'Lando Calrissian', EMPEROR: 'The Emperor',
    TARKIN: 'Grand Moff Tarkin', BIGGS: 'Biggs Darklighter', JABBA: 'Jabba the Hutt', PIETT: 'Admiral Piett' };

  var byLemma = {};
  D.words.forEach(function (w) { byLemma[w.w] = w; });

  function isProto(c) { return (LANG[c] && LANG[c].proto) || /-pro$/.test(c || ''); }
  function langName(c) { return (LANG[c] && LANG[c].name) || c; }
  function famColor(f) { return FAMILY_COLORS[f] || FAMILY_COLORS.Other; }
  function speakerName(s) { return SPEAKER_NAME[s] || (s ? s.charAt(0) + s.slice(1).toLowerCase() : ''); }
  function fmtYear(y) { return y == null ? 'undated' : y < 0 ? (-y) + ' BCE' : y + ' CE'; }
  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function el(html) { var t = document.createElement('template'); t.innerHTML = html.trim(); return t.content.firstChild; }
  function debounce(fn, ms) { var t; return function () { clearTimeout(t); t = setTimeout(fn, ms); }; }

  /* The lineage runs from English down to the first reconstructed proto-language. */
  function lineage(w) {
    var out = [];
    for (var i = 0; i < w.chain.length; i++) {
      if (isProto(w.chain[i].lang)) { break; }
      out.push(w.chain[i]);
    }
    if (!out.length) { out = w.chain.filter(function (h) { return !isProto(h.lang); }); }
    return out;
  }
  function deepest(w) {
    if (w.root) { return w.root.lang; }
    return w.chain.length ? w.chain[w.chain.length - 1].lang : w.origin;
  }
  function originFor(w, mode) {
    if (mode === 'donor') { return w.donor || null; }
    if (mode === 'deepest') { return deepest(w) || w.origin; }
    return w.origin;
  }
  /* Ordered language codes from the deepest attested source up to English, only those with coordinates. */
  function pathFor(w) {
    var codes = [], lin = lineage(w);
    for (var i = lin.length - 1; i >= 0; i--) {
      var c = lin[i].lang;
      if (codes.indexOf(c) < 0 && LANG[c] && LANG[c].lat != null) { codes.push(c); }
    }
    if (codes.indexOf('en') < 0) { codes.push('en'); }
    return codes;
  }
  function chainText(w) {
    var parts = [];
    w.chain.forEach(function (h) { parts.push(langName(h.lang) + (h.term ? ' <i>' + esc(h.term) + '</i>' : '')); });
    if (w.root && !(w.chain.length && w.chain[w.chain.length - 1].lang === w.root.lang)) {
      parts.push(langName(w.root.lang) + ' root <i>' + esc(w.root.term) + '</i>');
    }
    var s = parts.length ? '<b>' + esc(w.w) + '</b> &larr; ' + parts.join(' &larr; ') : '<b>' + esc(w.w) + '</b>';
    if (w.parts && w.parts.length) { s += (parts.length ? '; ' : ': ') + 'built from ' + w.parts.map(function (p) { return '<i>' + esc(p) + '</i>'; }).join(' + '); }
    return s;
  }
  function dateText(w) {
    if (w.year == null) { return 'no date could be inferred'; }
    var k = w.kind === 'attested' ? 'first attested' : w.kind === 'coined' ? 'coined' : 'placed in';
    var era = w.kind === 'inferred' ? (w.year < 1150 ? 'the Old English period' : w.year < 1500 ? 'the Middle English period'
      : w.year < 1700 ? 'Early Modern English' : w.year < 1900 ? 'Modern English' : 'the 20th century') : fmtYear(w.year);
    return k + ' ' + era + (w.note ? ' (' + esc(w.note) + ')' : '');
  }
  function wiktLink(w) {
    var t = w.wikt || w.w;
    return '<a href="https://en.wiktionary.org/wiki/' + encodeURIComponent(t) + '#English" target="_blank" rel="noopener">Wiktionary</a>';
  }
  function wordCard(w) {
    var ex = w.example || {};
    var spk = Object.keys(w.speakers || {}).map(function (s) { return speakerName(s) + ' (' + w.speakers[s] + ')'; }).join(', ');
    return '<h4>' + esc(w.w) + ' <small>&middot; spoken ' + w.n + ' time' + (w.n === 1 ? '' : 's') + '</small></h4>' +
      '<p class="sw-chain">' + chainText(w) + '</p>' +
      '<p>' + dateText(w) + '. Origin family: <b>' + esc(w.family) + '</b>. ' + wiktLink(w) + '</p>' +
      (spk ? '<p>Said by ' + esc(spk) + '.</p>' : '') +
      (ex.line ? '<p class="sw-quote">&ldquo;' + esc(ex.line) + '&rdquo; (' + esc(speakerName(ex.speaker)) + ', ' + esc(FILM_NAME[ex.film] || '') + ')</p>' : '');
  }
  function legendHTML(families) {
    return families.map(function (f) { return '<span style="--c:' + famColor(f) + '">' + esc(f) + '</span>'; }).join('');
  }

  /* ------------------------------------------------------------------ 1. MAP */
  function buildMap() {
    var root = document.getElementById('sw-map-app');
    if (!root || !window.L) { return; }
    root.className = 'sw-viz';
    root.innerHTML =
      '<div class="sw-controls">' +
      '<label>Origin depth <select id="sw-map-mode">' +
      '<option value="attested" selected>deepest attested language</option>' +
      '<option value="donor">language English borrowed from</option>' +
      '<option value="deepest">deepest root, reconstructed languages included</option></select></label>' +
      '<label>Color <select id="sw-map-color"><option value="era" selected>when the words entered English</option><option value="family">language family</option></select></label>' +
      '<label><input type="checkbox" id="sw-map-routes" checked> routes</label>' +
      '<input id="sw-map-search" list="sw-map-words" placeholder="trace a word, e.g. admiral" size="22">' +
      '<datalist id="sw-map-words"></datalist>' +
      '</div>' +
      '<div id="sw-map" class="sw-canvas"></div>' +
      '<div class="sw-legend" id="sw-map-legend"></div>' +
      '<div class="sw-info" id="sw-map-info">Circle size shows how often the characters say the words that trace back to a place. Click a circle to list them, or type a word to draw its route.</div>';

    var dl = root.querySelector('#sw-map-words');
    D.words.forEach(function (w) { var o = document.createElement('option'); o.value = w.w; dl.appendChild(o); });

    var map = L.map('sw-map', { worldCopyJump: true, minZoom: 1, maxZoom: 7, zoomSnap: 0.5, scrollWheelZoom: false });
    map.setView([40, 30], root.clientWidth < 600 ? 2 : 2.5);
    L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Dark_Gray_Base/MapServer/tile/{z}/{y}/{x}', {
      maxZoom: 16,
      attribution: 'Tiles &copy; <a href="https://www.esri.com/">Esri</a>, HERE, Garmin, OpenStreetMap contributors &middot; etymologies: Wiktionary'
    }).addTo(map);
    var circles = L.layerGroup().addTo(map), routes = L.layerGroup().addTo(map), traced = L.layerGroup().addTo(map);
    var eraColor = d3.scaleSequential(d3.interpolateViridis).domain([600, 1980]);

    function arc(a, b, k) {
      var pts = [], mx = (a[0] + b[0]) / 2, my = (a[1] + b[1]) / 2, dx = b[0] - a[0], dy = b[1] - a[1];
      var cx = mx - dy * k, cy = my + dx * k;
      for (var t = 0; t <= 1.0001; t += 1 / 24) {
        pts.push([(1 - t) * (1 - t) * a[0] + 2 * (1 - t) * t * cx + t * t * b[0],
                  (1 - t) * (1 - t) * a[1] + 2 * (1 - t) * t * cy + t * t * b[1]]);
      }
      return pts;
    }
    function routeFor(w, style, group) {
      var codes = pathFor(w);
      if (codes.length < 2) { return null; }
      var lines = [];
      for (var i = 0; i < codes.length - 1; i++) {
        var a = LANG[codes[i]], b = LANG[codes[i + 1]];
        lines.push(arc([a.lat, a.lon], [b.lat, b.lon], 0.18));
      }
      var pl = L.polyline(lines, style).addTo(group);
      pl.bindTooltip('<b>' + esc(w.w) + '</b>: ' + codes.map(langName).join(' &rarr; '), { sticky: true });
      pl.on('click', function () { showWord(w); });
      return pl;
    }
    /* Languages that share a homeland (Latin and Late Latin at Rome, Old French and French at
       Paris) merge into one circle so they do not stack on top of each other. */
    function groupsFor(mode) {
      var g = {};
      D.words.forEach(function (w) {
        var c = originFor(w, mode);
        if (!c || !LANG[c] || LANG[c].lat == null) { return; }
        var key = LANG[c].lat + ',' + LANG[c].lon;
        if (!g[key]) { g[key] = { code: c, codes: {}, n: 0, words: [] }; }
        g[key].codes[c] = (g[key].codes[c] || 0) + w.n;
        g[key].n += w.n; g[key].words.push(w);
      });
      Object.keys(g).forEach(function (k) {
        var grp = g[k];
        var ranked = Object.keys(grp.codes).sort(function (a, b) { return grp.codes[b] - grp.codes[a]; });
        grp.code = ranked[0];
        grp.also = ranked.slice(1).map(langName);
        var ws = grp.words.filter(function (w) { return w.year != null; }).sort(function (a, b) { return a.year - b.year; });
        var half = ws.reduce(function (s, w) { return s + w.n; }, 0) / 2, acc = 0, med = null;
        for (var i = 0; i < ws.length; i++) { acc += ws[i].n; if (acc >= half) { med = ws[i].year; break; } }
        grp.medYear = med;
        grp.words.sort(function (a, b) { return b.n - a.n; });
      });
      return g;
    }
    function render() {
      var mode = root.querySelector('#sw-map-mode').value, colorMode = root.querySelector('#sw-map-color').value;
      var groups = groupsFor(mode), list = Object.keys(groups).map(function (k) { return groups[k]; }).sort(function (a, b) { return b.n - a.n; });
      circles.clearLayers(); routes.clearLayers();
      var maxN = d3.max(list, function (g) { return g.n; }) || 1;
      var r = d3.scaleSqrt().domain([1, maxN]).range([4, 44]);
      list.forEach(function (g) {
        var Lg = LANG[g.code];
        var color = colorMode === 'era' ? eraColor(g.medYear || 1600) : famColor(Lg.family);
        var m = L.circleMarker([Lg.lat, Lg.lon], { radius: r(g.n), color: color, weight: 1.5, fillColor: color, fillOpacity: 0.55 }).addTo(circles);
        m.bindTooltip('<b>' + esc(Lg.name) + '</b>' + (g.also.length ? ' <small>with ' + esc(g.also.join(', ')) + '</small>' : '') +
          '<br>' + g.words.length + ' words, spoken ' + g.n + ' times' +
          (g.medYear ? '<br>typical arrival in English: ' + fmtYear(g.medYear) : ''));
        m.on('click', function () { showGroup(g, mode); });
      });
      if (root.querySelector('#sw-map-routes').checked) {
        D.words.filter(function (w) { return pathFor(w).length >= 3; }).sort(function (a, b) { return b.n - a.n; }).slice(0, 40)
          .forEach(function (w) { routeFor(w, { color: famColor(w.family), weight: 1.2, opacity: 0.5, dashArray: '4 5' }, routes); });
      }
      var lg = root.querySelector('#sw-map-legend');
      if (colorMode === 'era') {
        lg.innerHTML = '<span style="--c:' + eraColor(700) + '">entered English early (Old English)</span>' +
          '<i class="sw-ramp" style="background:linear-gradient(90deg,' + [600, 900, 1200, 1500, 1800, 1980].map(eraColor).join(',') + ')"></i>' +
          '<span style="--c:' + eraColor(1950) + '">recent (20th century)</span>';
      } else {
        var fams = {}; list.forEach(function (g) { fams[LANG[g.code].family] = 1; });
        lg.innerHTML = legendHTML(FAMILY_ORDER.filter(function (f) { return fams[f]; }));
      }
    }
    function showGroup(g, mode) {
      var Lg = LANG[g.code];
      var era = Lg.era ? ' Spoken roughly ' + fmtYear(Lg.era[0]) + ' to ' + fmtYear(Lg.era[1]) + '.' : '';
      var what = mode === 'donor' ? 'borrowed straight from' : mode === 'deepest' ? 'ultimately rooted in' : 'traced back to';
      var info = root.querySelector('#sw-map-info');
      var label = Lg.name + (g.also.length ? ' (with ' + g.also.join(', ') + ')' : '');
      info.innerHTML = '<h4>' + esc(label) + ' <small>&middot; ' + esc(Lg.family) + '</small></h4>' +
        '<p>' + g.words.length + ' Star Wars words ' + what + ' ' + esc(label) + ', spoken ' + g.n + ' times in the trilogy.' + era + '</p>' +
        '<div class="sw-wordlist">' + g.words.slice(0, 40).map(function (w) {
          return '<button data-w="' + esc(w.w) + '">' + esc(w.w) + ' <small>' + w.n + '</small></button>'; }).join('') +
        (g.words.length > 40 ? '<small>and ' + (g.words.length - 40) + ' more</small>' : '') + '</div>';
      info.querySelectorAll('button').forEach(function (b) { b.addEventListener('click', function () { showWord(byLemma[b.getAttribute('data-w')]); }); });
    }
    function showWord(w) {
      if (!w) { return; }
      traced.clearLayers();
      var codes = pathFor(w);
      var pl = routeFor(w, { color: '#fde047', weight: 3.5, opacity: 0.95 }, traced);
      codes.forEach(function (c, i) {
        var Lg = LANG[c];
        L.circleMarker([Lg.lat, Lg.lon], { radius: 6, color: '#fde047', weight: 2, fillColor: '#0f172a', fillOpacity: 1 }).addTo(traced)
          .bindTooltip('<b>' + esc(Lg.name) + '</b>' + (i === 0 && codes.length > 1 ? ' (origin)' : ''), { permanent: i === 0 && codes.length > 1, direction: 'top' });
      });
      if (pl) { map.fitBounds(pl.getBounds().pad(0.35)); }
      root.querySelector('#sw-map-info').innerHTML = wordCard(w) +
        (codes.length > 1 ? '<p>Route: ' + codes.map(langName).join(' &rarr; ') + '</p>' : '<p>This word never left England: no route to draw.</p>');
    }
    ['#sw-map-mode', '#sw-map-color', '#sw-map-routes'].forEach(function (id) { root.querySelector(id).addEventListener('change', render); });
    var search = root.querySelector('#sw-map-search');
    function doSearch() { var w = byLemma[search.value.trim().toLowerCase()] || byLemma[search.value.trim()]; if (w) { showWord(w); } }
    search.addEventListener('change', doSearch);
    search.addEventListener('keydown', function (e) { if (e.key === 'Enter') { doSearch(); } });
    render();
    window.addEventListener('resize', debounce(function () { map.invalidateSize(); }, 200));
  }

  /* ------------------------------------------------------------- 2. TIMELINE */
  function buildTimeline() {
    var root = document.getElementById('sw-timeline-app');
    if (!root || !window.d3) { return; }
    root.className = 'sw-viz';
    var Y0 = 450, Y1 = 1985, BIN = 50;
    var ERAS = [
      ['Old English', 450, 1150, '#3b82f6'], ['Old Norse', 700, 1350, '#22c55e'], ['Old French & Anglo-Norman', 842, 1400, '#f97316'],
      ['Middle English', 1150, 1500, '#60a5fa'], ['Early Modern English', 1500, 1700, '#93c5fd'], ['Modern English', 1700, 1985, '#bfdbfe']
    ];
    var PRESETS = [[1066, 'Norman conquest'], [1200, '1200'], [1400, 'Chaucer'], [1616, 'Shakespeare'], [1776, '1776'], [1900, '1900'], [1977, 'A New Hope']];
    root.innerHTML =
      '<div class="sw-controls">' +
      '<label>Count <select id="sw-tl-unit"><option value="lemmas" selected>distinct words</option><option value="tokens">every word spoken</option></select></label>' +
      '<label>Film <select id="sw-tl-film"><option value="all" selected>whole trilogy</option><option value="IV">A New Hope</option><option value="V">The Empire Strikes Back</option><option value="VI">Return of the Jedi</option></select></label>' +
      '<label><input type="checkbox" id="sw-tl-attested"> only words with a recorded date</label>' +
      '</div>' +
      '<svg class="sw-timeline-svg" id="sw-tl-svg"></svg>' +
      '<div class="sw-legend" id="sw-tl-legend"></div>' +
      '<div class="sw-slider-row"><span class="sw-year" id="sw-tl-year"></span>' +
      '<input type="range" id="sw-tl-slider" min="' + Y0 + '" max="' + Y1 + '" step="1" value="' + Y1 + '">' +
      '<div class="sw-presets" id="sw-tl-presets"></div></div>' +
      '<div class="sw-stats" id="sw-tl-stats"></div>' +
      '<div class="sw-quote-box"><div class="sw-controls"><label>Line <select id="sw-tl-quote"></select></label></div>' +
      '<div class="sw-quote-text" id="sw-tl-quote-text"></div><div class="sw-quote-who" id="sw-tl-quote-who"></div>' +
      '<div class="sw-quote-explain" id="sw-tl-quote-explain">Hover a word to see when it entered English. Drag the slider back in time and words that did not yet exist fade out.</div></div>';

    var presets = root.querySelector('#sw-tl-presets');
    PRESETS.forEach(function (p) {
      var b = el('<button>' + esc(p[1]) + '</button>');
      b.addEventListener('click', function () { slider.value = p[0]; update(); });
      presets.appendChild(b);
    });
    var qsel = root.querySelector('#sw-tl-quote');
    D.quotes.forEach(function (q, i) {
      var o = document.createElement('option'); o.value = i;
      o.textContent = speakerName(q.speaker) + ': ' + (q.text.length > 48 ? q.text.slice(0, 45) + '...' : q.text);
      qsel.appendChild(o);
    });
    var slider = root.querySelector('#sw-tl-slider');
    var svg = d3.select(root.querySelector('#sw-tl-svg'));
    var tip = null;

    function filtered() {
      var film = root.querySelector('#sw-tl-film').value, onlyAtt = root.querySelector('#sw-tl-attested').checked;
      return D.words.filter(function (w) {
        if (film !== 'all' && !w.films[film]) { return false; }
        if (onlyAtt && w.kind === 'inferred') { return false; }
        return true;
      }).map(function (w) { return { w: w, n: film === 'all' ? w.n : w.films[film] }; });
    }
    function draw() {
      var unit = root.querySelector('#sw-tl-unit').value;
      var rows = filtered();
      var W = Math.max(320, root.clientWidth), H = 340, m = { t: 8, r: 12, b: 34, l: 44 }, eraH = 13, eraTop = m.t, chartTop = eraTop + ERAS.length * eraH + 14;
      svg.attr('viewBox', '0 0 ' + W + ' ' + H).attr('width', W).attr('height', H);
      svg.selectAll('*').remove();
      var x = d3.scaleLinear().domain([Y0, Y1]).range([m.l, W - m.r]);
      // era bands
      ERAS.forEach(function (e, i) {
        var y = eraTop + i * eraH;
        svg.append('rect').attr('x', x(e[1])).attr('y', y).attr('width', x(Math.min(e[2], Y1)) - x(e[1])).attr('height', eraH - 2).attr('rx', 2).attr('fill', e[3]).attr('opacity', 0.75);
        svg.append('text').attr('x', x(e[1]) + 4).attr('y', y + eraH - 4).attr('font-size', 9.5).attr('fill', '#0f172a').text(e[0]);
      });
      // bins
      var nb = Math.ceil((Y1 - Y0) / BIN), bins = [];
      for (var i = 0; i < nb; i++) { bins.push({ y0: Y0 + i * BIN, fams: {}, total: 0 }); }
      rows.forEach(function (r) {
        var w = r.w; if (w.year == null) { return; }
        var y = Math.min(Math.max(w.year, Y0), Y1 - 1), b = bins[Math.floor((y - Y0) / BIN)];
        var f = w.family || 'Unknown', k = w.kind === 'inferred' ? 'inf' : 'att', v = unit === 'tokens' ? r.n : 1;
        b.fams[f] = b.fams[f] || { att: 0, inf: 0 }; b.fams[f][k] += v; b.total += v;
      });
      var maxT = d3.max(bins, function (b) { return b.total; }) || 1;
      var yS = d3.scaleSqrt().domain([0, maxT]).range([H - m.b, chartTop]);
      var fams = FAMILY_ORDER.filter(function (f) { return bins.some(function (b) { return b.fams[f]; }); });
      bins.forEach(function (b) {
        var acc = 0, bx = x(b.y0) + 1, bw = Math.max(1, x(b.y0 + BIN) - x(b.y0) - 2);
        fams.forEach(function (f) {
          var v = b.fams[f]; if (!v) { return; }
          ['inf', 'att'].forEach(function (k) {
            if (!v[k]) { return; }
            var y1 = yS(acc), y2 = yS(acc + v[k]);
            svg.append('rect').attr('class', 'sw-bin').attr('data-y', b.y0).attr('x', bx).attr('y', y2).attr('width', bw).attr('height', Math.max(0, y1 - y2))
              .attr('fill', famColor(f)).attr('opacity', k === 'inf' ? 0.45 : 0.95)
              .append('title').text(b.y0 + '-' + (b.y0 + BIN) + ': ' + v[k] + ' ' + (unit === 'tokens' ? 'spoken words' : 'words') + ' of ' + f + ' origin' + (k === 'inf' ? ' (era estimated from the etymology)' : ' (dated on Wiktionary or by hand)'));
            acc += v[k];
          });
        });
      });
      svg.append('g').attr('transform', 'translate(0,' + (H - m.b) + ')').call(d3.axisBottom(x).ticks(W < 500 ? 6 : 12).tickFormat(d3.format('d'))).attr('font-size', 10);
      svg.append('g').attr('transform', 'translate(' + m.l + ',0)').call(d3.axisLeft(yS).ticks(5).tickFormat(d3.format('~s'))).attr('font-size', 10);
      svg.append('text').attr('x', m.l + 4).attr('y', chartTop - 3).attr('font-size', 10).attr('fill', '#475569').text((unit === 'tokens' ? 'words spoken' : 'distinct words') + ' entering English per 50 years (square-root scale)');
      svg.append('rect').attr('id', 'sw-tl-shade').attr('y', chartTop - 6).attr('height', H - m.b - chartTop + 6).attr('fill', '#0f172a').attr('opacity', 0.08);
      svg.append('line').attr('id', 'sw-tl-cursor').attr('y1', eraTop).attr('y2', H - m.b).attr('stroke', '#0f172a').attr('stroke-width', 2);
      root.querySelector('#sw-tl-legend').innerHTML = legendHTML(fams) + '<span style="--c:#cbd5e1">paler bars: era estimated from the etymology chain</span>';
      draw.x = x; draw.W = W;
      update();
    }
    function update() {
      var Y = +slider.value, x = draw.x;
      root.querySelector('#sw-tl-year').textContent = Y + ' CE';
      svg.select('#sw-tl-cursor').attr('x1', x(Y)).attr('x2', x(Y));
      svg.select('#sw-tl-shade').attr('x', x(Y)).attr('width', Math.max(0, x(Y1) - x(Y)));
      svg.selectAll('.sw-bin').attr('stroke', function () { return +this.getAttribute('data-y') >= Y ? '#fff' : 'none'; });
      var rows = filtered(), lemAll = 0, lemOk = 0, tokAll = 0, tokOk = 0, undated = 0;
      rows.forEach(function (r) {
        lemAll++; tokAll += r.n;
        if (r.w.year == null) { undated++; return; }
        if (r.w.year <= Y) { lemOk++; tokOk += r.n; }
      });
      var film = root.querySelector('#sw-tl-film').value;
      var scope = film === 'all' ? 'the trilogy' : FILM_NAME[film];
      var pct = function (a, b) { return b ? (100 * a / b).toFixed(1) + '%' : '-'; };
      root.querySelector('#sw-tl-stats').innerHTML =
        '<div class="sw-stat"><b>' + pct(lemOk, lemAll) + '</b><span>of the distinct words in ' + esc(scope) + ' existed in English by ' + Y + '</span></div>' +
        '<div class="sw-stat"><b>' + pct(tokOk, tokAll) + '</b><span>of every word actually spoken</span></div>' +
        '<div class="sw-stat"><b>' + lemOk.toLocaleString() + ' / ' + lemAll.toLocaleString() + '</b><span>words in, words total' + (undated ? ' (' + undated + ' undated)' : '') + '</span></div>';
      renderQuote(Y);
    }
    function renderQuote(Y) {
      var q = D.quotes[+qsel.value] || D.quotes[0];
      var box = root.querySelector('#sw-tl-quote-text');
      box.innerHTML = q.tokens.map(function (t) {
        if (!t.w) { return /[A-Za-z]/.test(t.t) ? '<span class="sw-tok sw-name" title="a name, or a word with no traceable history">' + esc(t.t) + '</span>' : esc(t.t); }
        var w = byLemma[t.w]; if (!w) { return esc(t.t); }
        var gone = w.year != null && w.year > Y;
        return '<span class="sw-tok' + (gone ? ' sw-gone' : '') + '" data-w="' + esc(w.w) + '" style="color:' + famColor(w.family) + '">' + esc(t.t) + '</span>';
      }).join('');
      root.querySelector('#sw-tl-quote-who').textContent = speakerName(q.speaker) + ', ' + FILM_NAME[q.film];
      var ex = root.querySelector('#sw-tl-quote-explain');
      box.querySelectorAll('.sw-tok[data-w]').forEach(function (s) {
        s.addEventListener('mouseenter', function () {
          var w = byLemma[s.getAttribute('data-w')];
          ex.innerHTML = '<b>' + esc(w.w) + '</b>: ' + dateText(w) + '. ' + chainText(w) + '.';
        });
      });
      var missing = box.querySelectorAll('.sw-gone').length;
      if (missing && !ex.dataset.hover) {
        ex.innerHTML = 'In ' + Y + ', ' + missing + ' of the words in this line did not yet exist in English. Hover a word for its story.';
      }
    }
    slider.addEventListener('input', update);
    qsel.addEventListener('change', update);
    ['#sw-tl-unit', '#sw-tl-film', '#sw-tl-attested'].forEach(function (id) { root.querySelector(id).addEventListener('change', draw); });
    draw();
    window.addEventListener('resize', debounce(draw, 250));
  }

  /* ---------------------------------------------------------------- 3. GRAPH */
  function buildGraph() {
    var root = document.getElementById('sw-graph-app');
    if (!root || !window.cytoscape) { return; }
    root.className = 'sw-viz';
    root.innerHTML =
      '<div class="sw-controls">' +
      '<span class="sw-graph-search"><input id="sw-g-search" list="sw-g-words" placeholder="add a word, e.g. galaxy" size="22"><button id="sw-g-add">Add</button></span>' +
      '<datalist id="sw-g-words"></datalist>' +
      '<button id="sw-g-reset">Reset</button><button id="sw-g-layout">Re-run layout</button>' +
      '<label><input type="checkbox" id="sw-g-speakers" checked> speakers</label>' +
      '</div>' +
      '<div id="sw-cy" class="sw-canvas"></div>' +
      '<div class="sw-legend" id="sw-g-legend"></div>' +
      '<div class="sw-info" id="sw-g-info">Tap a word for its story, a language to see every Star Wars word that descends from it, or a speaker to light up their vocabulary. Drag nodes, scroll to zoom.</div>';
    var dl = root.querySelector('#sw-g-words');
    D.words.forEach(function (w) { var o = document.createElement('option'); o.value = w.w; dl.appendChild(o); });

    var SPEAKERS = (D.speakers || []).slice(0, 6);
    var inGraph = {};
    function hopsFor(w) {
      var out = [], lastProto = null;
      w.chain.forEach(function (h) {
        if (isProto(h.lang)) { lastProto = h; return; }
        if (ENGLISH[h.lang] && h.lang !== 'ang') { return; }      // Middle English spellings are noise here
        out.push(h);
      });
      if (w.root) { lastProto = w.root; }
      if (lastProto) { out.push(lastProto); }
      return out;
    }
    function langNode(c) {
      var Lg = LANG[c] || { name: c, family: 'Other' };
      return { group: 'nodes', data: { id: 'l:' + c, type: 'lang', label: Lg.name, code: c, color: famColor(Lg.family), family: Lg.family } };
    }
    function elementsFor(w) {
      var els = [], hops = hopsFor(w), wid = 'w:' + w.w;
      els.push({ group: 'nodes', data: { id: wid, type: 'word', label: w.w, w: w.w, n: w.n, size: 16 + 6 * Math.log(w.n + 1), color: famColor(w.family), family: w.family } });
      var prev = wid;
      hops.forEach(function (h, i) {
        var Lg = LANG[h.lang] || { family: 'Other' };
        var hid = h.term ? 'e:' + h.lang + ':' + h.term : 'l:' + h.lang;
        if (h.term) {
          els.push({ group: 'nodes', data: { id: hid, type: 'etymon', label: h.term, lang: h.lang, color: famColor(Lg.family), family: Lg.family } });
          els.push(langNode(h.lang));
          els.push({ group: 'edges', data: { id: 'x:' + hid, source: hid, target: 'l:' + h.lang, type: 'lang' } });
        } else {
          els.push(langNode(h.lang));
        }
        els.push({ group: 'edges', data: { id: 'c:' + prev + '>' + hid, source: prev, target: hid, type: 'chain' } });
        prev = hid;
      });
      if (!hops.length && w.origin) {
        els.push(langNode(w.origin));
        els.push({ group: 'edges', data: { id: 'c:' + wid + '>l:' + w.origin, source: wid, target: 'l:' + w.origin, type: 'chain' } });
      }
      (w.parts || []).forEach(function (p) {
        var base = p.replace(/^-|-$/g, ''), pw = byLemma[base];
        if (pw && pw.w !== w.w && inGraph[pw.w]) {
          els.push({ group: 'edges', data: { id: 'p:' + wid + '>w:' + pw.w, source: wid, target: 'w:' + pw.w, type: 'part' } });
        }
      });
      if (root.querySelector('#sw-g-speakers').checked) {
        SPEAKERS.forEach(function (s) {
          if (w.speakers && w.speakers[s]) {
            els.push({ group: 'nodes', data: { id: 's:' + s, type: 'speaker', label: speakerName(s), speaker: s, color: '#fde047' } });
            els.push({ group: 'edges', data: { id: 's:' + s + '>' + wid, source: 's:' + s, target: wid, type: 'speaker' } });
          }
        });
      }
      return els;
    }
    var cy = cytoscape({
      container: root.querySelector('#sw-cy'),
      wheelSensitivity: 0.2,
      style: [
        { selector: 'node', style: { 'label': 'data(label)', 'color': '#e2e8f0', 'font-size': 10, 'text-valign': 'bottom', 'text-margin-y': 3, 'text-outline-color': '#0f172a', 'text-outline-width': 2, 'background-color': 'data(color)' } },
        { selector: 'node[type="word"]', style: { 'width': 'data(size)', 'height': 'data(size)', 'font-size': 13, 'font-weight': 'bold', 'border-width': 1.5, 'border-color': '#f8fafc' } },
        { selector: 'node[type="etymon"]', style: { 'width': 9, 'height': 9, 'font-size': 9, 'font-style': 'italic', 'opacity': 0.9, 'min-zoomed-font-size': 6 } },
        { selector: 'node[type="lang"]', style: { 'shape': 'round-rectangle', 'width': function (n) { return n.data('label').length * 7 + 14; }, 'height': 22, 'font-size': 12, 'font-weight': 'bold', 'text-valign': 'center', 'text-margin-y': 0, 'color': '#0f172a', 'text-outline-width': 0, 'border-width': 2, 'border-color': '#f8fafc' } },
        { selector: 'node[type="speaker"]', style: { 'shape': 'diamond', 'width': 30, 'height': 30, 'font-size': 11, 'font-weight': 'bold', 'color': '#fde047' } },
        { selector: 'edge', style: { 'width': 1.4, 'line-color': '#64748b', 'curve-style': 'bezier', 'target-arrow-shape': 'triangle', 'target-arrow-color': '#64748b', 'arrow-scale': 0.7, 'opacity': 0.8 } },
        { selector: 'edge[type="lang"]', style: { 'width': 0.8, 'line-style': 'dotted', 'target-arrow-shape': 'none', 'opacity': 0.5 } },
        { selector: 'edge[type="speaker"]', style: { 'line-color': '#fde047', 'target-arrow-color': '#fde047', 'line-style': 'dashed', 'opacity': 0.55, 'width': 1 } },
        { selector: 'edge[type="part"]', style: { 'line-color': '#38bdf8', 'target-arrow-color': '#38bdf8', 'line-style': 'dashed' } },
        { selector: '.sw-dim', style: { 'opacity': 0.12 } },
        { selector: '.sw-hl', style: { 'border-color': '#fde047', 'border-width': 3, 'line-color': '#fde047', 'target-arrow-color': '#fde047', 'opacity': 1, 'z-index': 9 } }
      ]
    });
    function runLayout() {
      cy.layout({ name: 'cose', animate: false, randomize: false, fit: true, padding: 20, componentSpacing: 60, nodeRepulsion: function () { return 9000; },
        idealEdgeLength: function (e) { return e.data('type') === 'speaker' ? 110 : 55; }, edgeElasticity: function () { return 120; }, gravity: 0.5, numIter: 800, nodeOverlap: 8 }).run();
    }
    function addWords(list, relayout) {
      var els = [];
      list.forEach(function (w) { if (w && !inGraph[w.w]) { inGraph[w.w] = 1; els = els.concat(elementsFor(w)); } });
      // part edges to words that arrived later in the same batch
      list.forEach(function (w) {
        (w.parts || []).forEach(function (p) {
          var pw = byLemma[p.replace(/^-|-$/g, '')];
          if (pw && pw.w !== w.w && inGraph[pw.w]) { els.push({ group: 'edges', data: { id: 'p:w:' + w.w + '>w:' + pw.w, source: 'w:' + w.w, target: 'w:' + pw.w, type: 'part' } }); }
        });
      });
      var fresh = els.filter(function (e) { return !cy.getElementById(e.data.id).length; });
      var seen = {}; fresh = fresh.filter(function (e) { if (seen[e.data.id]) { return false; } seen[e.data.id] = 1; return true; });
      cy.add(fresh);
      if (relayout) { runLayout(); }
      var fams = {}; cy.nodes('[type="word"]').forEach(function (n) { fams[n.data('family')] = 1; });
      root.querySelector('#sw-g-legend').innerHTML = legendHTML(FAMILY_ORDER.filter(function (f) { return fams[f]; })) +
        '<span style="--c:#fde047">speakers</span><span style="--c:#64748b">etymon &rarr; language</span>';
    }
    function reset() {
      cy.elements().remove(); inGraph = {};
      addWords(D.hero.map(function (h) { return byLemma[h]; }), true);
    }
    var info = root.querySelector('#sw-g-info');
    function clearHl() { cy.elements().removeClass('sw-dim sw-hl'); }
    function highlight(nodes) {
      clearHl();
      var keep = nodes.union(nodes.connectedEdges()).union(nodes.neighborhood());
      cy.elements().difference(keep).addClass('sw-dim');
      nodes.addClass('sw-hl');
    }
    cy.on('tap', 'node[type="word"]', function (e) {
      var w = byLemma[e.target.data('w')];
      var path = e.target.successors().filter('node[type!="lang"]').union(e.target.successors('node[type="lang"]'));
      highlight(e.target.union(path));
      info.innerHTML = wordCard(w);
    });
    cy.on('tap', 'node[type="lang"]', function (e) {
      var code = e.target.data('code');
      var all = D.words.filter(function (w) { return w.chain.some(function (h) { return h.lang === code; }) || w.origin === code || (w.root && w.root.lang === code); })
        .sort(function (a, b) { return b.n - a.n; });
      var present = cy.nodes('[type="word"]').filter(function (n) { var w = byLemma[n.data('w')]; return all.indexOf(w) >= 0; });
      highlight(present.union(e.target));
      var Lg = LANG[code] || { name: code, family: 'Other' };
      var spoken = all.reduce(function (s, w) { return s + w.n; }, 0);
      var missing = all.filter(function (w) { return !inGraph[w.w]; });
      info.innerHTML = '<h4>' + esc(Lg.name) + ' <small>&middot; ' + esc(Lg.family) + '</small></h4>' +
        '<p>' + all.length + ' Star Wars words have ' + esc(Lg.name) + ' somewhere in their ancestry, spoken ' + spoken + ' times. ' + present.length + ' are in the graph now.</p>' +
        (missing.length ? '<p><button id="sw-g-expand">Add ' + Math.min(missing.length, 40) + ' more ' + esc(Lg.name) + ' words</button></p>' : '') +
        '<div class="sw-wordlist">' + all.slice(0, 60).map(function (w) { return '<button data-w="' + esc(w.w) + '">' + esc(w.w) + ' <small>' + w.n + '</small></button>'; }).join('') +
        (all.length > 60 ? '<small>and ' + (all.length - 60) + ' more</small>' : '') + '</div>';
      var ex = info.querySelector('#sw-g-expand');
      if (ex) { ex.addEventListener('click', function () { addWords(missing.slice(0, 40), true); e.target.emit('tap'); }); }
      info.querySelectorAll('.sw-wordlist button').forEach(function (b) {
        b.addEventListener('click', function () { var w = byLemma[b.getAttribute('data-w')]; addWords([w], true); cy.getElementById('w:' + w.w).emit('tap'); });
      });
    });
    cy.on('tap', 'node[type="speaker"]', function (e) {
      var s = e.target.data('speaker');
      var words = cy.nodes('[type="word"]').filter(function (n) { var w = byLemma[n.data('w')]; return w.speakers && w.speakers[s]; });
      highlight(words.union(e.target));
      var all = D.words.filter(function (w) { return w.speakers && w.speakers[s]; });
      var fams = {}; all.forEach(function (w) { fams[w.family] = (fams[w.family] || 0) + w.speakers[s]; });
      var tot = Object.keys(fams).reduce(function (a, k) { return a + fams[k]; }, 0);
      info.innerHTML = '<h4>' + esc(speakerName(s)) + '</h4><p>Origin of the words this speaker uses most (counted among their top three speakers per word): ' +
        Object.keys(fams).sort(function (a, b) { return fams[b] - fams[a]; }).slice(0, 5).map(function (k) { return esc(k) + ' ' + (100 * fams[k] / tot).toFixed(0) + '%'; }).join(', ') + '.</p>';
    });
    cy.on('tap', 'node[type="etymon"]', function (e) {
      highlight(e.target.union(e.target.predecessors()).union(e.target.successors()));
      info.innerHTML = '<h4><i>' + esc(e.target.data('label')) + '</i> <small>&middot; ' + esc(langName(e.target.data('lang'))) + '</small></h4><p>Words in the graph that pass through this form: ' +
        e.target.predecessors('node[type="word"]').map(function (n) { return esc(n.data('label')); }).join(', ') + '</p>';
    });
    cy.on('tap', function (e) { if (e.target === cy) { clearHl(); } });
    root.querySelector('#sw-g-reset').addEventListener('click', reset);
    root.querySelector('#sw-g-layout').addEventListener('click', runLayout);
    root.querySelector('#sw-g-speakers').addEventListener('change', reset);
    var search = root.querySelector('#sw-g-search');
    function addSearched() {
      var w = byLemma[search.value.trim().toLowerCase()] || byLemma[search.value.trim()];
      if (!w) { info.innerHTML = '<p>No etymology for &ldquo;' + esc(search.value) + '&rdquo; in the trilogy data.</p>'; return; }
      addWords([w], true); cy.getElementById('w:' + w.w).emit('tap'); search.value = '';
    }
    root.querySelector('#sw-g-add').addEventListener('click', addSearched);
    search.addEventListener('keydown', function (e) { if (e.key === 'Enter') { addSearched(); } });
    reset();
    window.addEventListener('resize', debounce(function () { cy.resize(); cy.fit(undefined, 20); }, 250));
  }

  function init() {
    try { buildMap(); } catch (e) { console.error('map', e); }
    try { buildTimeline(); } catch (e) { console.error('timeline', e); }
    try { buildGraph(); } catch (e) { console.error('graph', e); }
  }
  if (document.readyState === 'loading') { document.addEventListener('DOMContentLoaded', init); } else { init(); }
})();
