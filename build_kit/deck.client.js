(function () {
  var D = window.DECK, S = D.slides, N = S.length;
  var stage = document.getElementById('stage');
  var slides = [].slice.call(document.querySelectorAll('.slide'));
  var cur = 0, pres = null;

  // ---- clock times: everything derives from one start time (?start=HH:MM overrides) ----
  var q = new URLSearchParams(location.search).get('start');
  var st = (q && /^\d{1,2}:\d{2}$/.test(q) ? q : D.meta.start).split(':').map(Number);
  var start = st[0] * 60 + st[1];
  function hm(m) { m = ((m % 1440) + 1440) % 1440; return ('0' + Math.floor(m / 60)).slice(-2) + ':' + ('0' + (m % 60)).slice(-2); }
  var offs = [], acc = 0; S.forEach(function (s) { offs.push(acc); acc += s.mins; });
  var times = { back: hm(start + 60) };
  for (var k = 0; k < 3; k++) { times['p' + k + 's'] = hm(start + 60 * k); times['p' + k + 'e'] = hm(start + 60 * k + 45); }
  [].forEach.call(document.querySelectorAll('[data-time]'), function (el) { el.textContent = times[el.getAttribute('data-time')] || ''; });

  // ---- fit the 1600x900 stage to the window ----
  function fit() {
    var s = Math.min(innerWidth / 1600, innerHeight / 900);
    stage.style.transform = 'translate(' + (innerWidth - 1600 * s) / 2 + 'px,' + (innerHeight - 900 * s) / 2 + 'px) scale(' + s + ')';
  }
  addEventListener('resize', fit); fit();

  // ---- navigation ----
  function go(i) {
    cur = Math.max(0, Math.min(N - 1, i));
    slides.forEach(function (el, j) { el.classList.toggle('on', j === cur); });
    document.querySelector('#progress i').style.width = (100 * (cur + 1) / N) + '%';
    history.replaceState(null, '', location.pathname + location.search + '#' + (cur + 1));
    sync();
  }
  document.getElementById('bPrev').onclick = function () { go(cur - 1); };
  document.getElementById('bNext').onclick = function () { go(cur + 1); };
  document.getElementById('bNotes').onclick = openPresenter;
  var help = document.getElementById('help');
  document.getElementById('bHelp').onclick = function () { help.hidden = !help.hidden; };
  help.onclick = function () { help.hidden = true; };

  addEventListener('keydown', function (e) {
    if (e.target.tagName === 'INPUT') return;
    var k = e.key;
    if (k === 'ArrowRight' || k === 'PageDown' || k === ' ') { e.preventDefault(); go(cur + 1); }
    else if (k === 'ArrowLeft' || k === 'PageUp') { e.preventDefault(); go(cur - 1); }
    else if (k === 'Home') go(0); else if (k === 'End') go(N - 1);
    else if (/^[nν]$/i.test(k)) openPresenter();
    else if (/^[tτ]$/i.test(k)) toggleTimer();
    else if (/^[hη]$/i.test(k)) showHint();
    else if (/^[fφ]$/i.test(k)) { document.fullscreenElement ? document.exitFullscreen() : document.documentElement.requestFullscreen(); }
    else if (/^[pπ]$/i.test(k)) print();
    else if (k === '?' || k === 'Escape') help.hidden = k === 'Escape' ? true : !help.hidden;
  });
  // ---- mouse wheel / trackpad: one notch, one slide ----
  var wAcc = 0, wLock = 0;
  addEventListener('wheel', function (e) {
    if (!help.hidden) return;                                   // the help overlay scrolls on its own
    for (var el = e.target; el && el !== document.body; el = el.parentElement) {
      if (el.scrollHeight - el.clientHeight > 4 && getComputedStyle(el).overflowY !== 'visible') return;
    }
    var now = Date.now();
    if (now - wLock < 400) { e.preventDefault(); return; }      // one slide per gesture, not per event
    wAcc += e.deltaY + e.deltaX;
    if (Math.abs(wAcc) < 24) return;
    e.preventDefault(); wLock = now; go(cur + (wAcc > 0 ? 1 : -1)); wAcc = 0;
  }, { passive: false });

  var tx = null;
  addEventListener('touchstart', function (e) { tx = e.touches[0].clientX; }, { passive: true });
  addEventListener('touchend', function (e) { if (tx === null) return; var dx = e.changedTouches[0].clientX - tx; if (Math.abs(dx) > 60) go(cur + (dx < 0 ? 1 : -1)); tx = null; });

  // ---- activity timers ----
  var ticking = null;
  function fmt(s) { return ('0' + Math.floor(s / 60)).slice(-2) + ':' + ('0' + (s % 60)).slice(-2); }
  [].forEach.call(document.querySelectorAll('.timer'), function (t) {
    var total = +t.getAttribute('data-sec'), left = total, read = t.querySelector('.timer-read'), b = t.querySelector('.t-start');
    t._toggle = function () {
      if (t._id) { clearInterval(t._id); t._id = null; b.textContent = 'Συνέχεια'; return; }
      if (left <= 0) { left = total; t.classList.remove('done'); }
      b.textContent = 'Παύση';
      var end = Date.now() + left * 1000;
      t._id = setInterval(function () {
        left = Math.max(0, Math.round((end - Date.now()) / 1000)); read.textContent = fmt(left);
        if (left === 0) { clearInterval(t._id); t._id = null; t.classList.add('done'); b.textContent = 'Ξανά'; }
      }, 250);
    };
    b.onclick = t._toggle;
    t.querySelector('.t-reset').onclick = function () { clearInterval(t._id); t._id = null; left = total; read.textContent = fmt(left); t.classList.remove('done'); b.textContent = 'Έναρξη χρονομέτρου'; };
  });
  function toggleTimer() { var t = slides[cur].querySelector('.timer'); if (t) t._toggle(); else if (brkEl()) brkStart = Date.now(); }
  function showHint() { var h = slides[cur].querySelector('.hint[hidden]'); if (h) { h.hidden = false; var b = slides[cur].querySelector('.hint-btn'); if (b) b.remove(); } }
  [].forEach.call(document.querySelectorAll('.hint-btn'), function (b) { b.onclick = showHint; });

  // ---- break countdown: runs from the full break length, starting when the break slide is first shown ----
  var brkStart = null;
  function brkEl() { return slides[cur].querySelector('[data-break]'); }
  setInterval(function () {
    var el = brkEl(); if (!el) return;
    if (brkStart === null) brkStart = Date.now();
    var left = Math.max(0, Math.round(+el.getAttribute('data-break') * 60 - (Date.now() - brkStart) / 1000));
    el.textContent = left > 0 ? fmt(left) : 'Ξεκινάμε.';
  }, 500);

  // ---- presenter window: notes, clock, pace, run sheet ----
  function openPresenter() {
    if (pres && !pres.closed) { pres.focus(); return; }
    pres = window.open('', 'presenterNotes', 'width=980,height=760');
    if (!pres) { alert('Ο browser μπλόκαρε το παράθυρο σημειώσεων. Επιτρέψτε τα αναδυόμενα παράθυρα για αυτή τη σελίδα.'); return; }
    pres.document.write('<!DOCTYPE html><html lang="el"><head><meta charset="UTF-8"><title>Σημειώσεις ομιλητή</title><style>' +
      'body{margin:0;font:18px/1.5 "Segoe UI","Helvetica Neue",Arial,sans-serif;background:#0B1628;color:#E8EEF8;display:grid;grid-template-columns:1fr 330px;height:100vh}' +
      'main{padding:26px 30px;overflow:auto}aside{background:#12233F;padding:18px;overflow:auto;border-left:1px solid #2A436C}' +
      '.bar{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-bottom:20px}.box{background:#1C3358;border-radius:12px;padding:12px 16px}' +
      '.box small{display:block;color:#9FB2CE;font-size:13px}.box b{font-size:34px;font-variant-numeric:tabular-nums}' +
      '.pace.late{background:#A92C25}.pace.ok{background:#1F7A45}' +
      'h1{font-size:26px;line-height:1.2;margin:4px 0 6px}.meta{color:#9FB2CE;font-size:15px;margin-bottom:14px}' +
      '.skip{display:inline-block;background:#F2A413;color:#12233F;font-weight:700;border-radius:999px;padding:2px 12px;font-size:14px;margin-left:8px}' +
      'ul{padding-left:22px}li{margin:0 0 12px;font-size:21px;line-height:1.42}' +
      '.nxt{margin-top:22px;color:#9FB2CE;font-size:16px}.btns{margin-top:18px;display:flex;gap:10px}' +
      'button{font:700 17px inherit;padding:12px 22px;border-radius:10px;border:0;background:#F2A413;color:#12233F;cursor:pointer}button.sec{background:#2A436C;color:#fff}' +
      'ol{list-style:none;margin:0;padding:0}ol li{font-size:14px;line-height:1.3;margin:0;padding:7px 8px;border-radius:8px;display:grid;grid-template-columns:48px 1fr;gap:6px;cursor:pointer;color:#C9D7EC}' +
      'ol li.cur{background:#F2A413;color:#12233F;font-weight:700}ol li .t{font-variant-numeric:tabular-nums}aside h2{font-size:14px;color:#9FB2CE;margin:0 0 8px;font-weight:600}' +
      '</style></head><body><main><div class="bar"><div class="box"><small>Ώρα</small><b id="now"></b></div>' +
      '<div class="box"><small>Πλάνο για αυτή τη διαφάνεια</small><b id="plan"></b></div><div class="box pace" id="paceBox"><small>Ρυθμός</small><b id="pace"></b></div></div>' +
      '<h1 id="ttl"></h1><div class="meta" id="meta"></div><ul id="notes"></ul><div class="nxt" id="nxt"></div>' +
      '<div class="btns"><button class="sec" id="pv">‹ Προηγούμενη</button><button id="nx">Επόμενη ›</button></div></main>' +
      '<aside><h2>Πλάνο ' + hm(start) + '–' + hm(start + D.meta.lengthMin) + '</h2><ol id="sheet"></ol></aside></body></html>');
    pres.document.close();
    var pd = pres.document;
    pd.getElementById('pv').onclick = function () { go(cur - 1); };
    pd.getElementById('nx').onclick = function () { go(cur + 1); };
    pres.addEventListener('keydown', function (e) { if (e.key === 'ArrowRight' || e.key === ' ') go(cur + 1); if (e.key === 'ArrowLeft') go(cur - 1); });
    var ol = pd.getElementById('sheet');
    S.forEach(function (s, i) { var li = pd.createElement('li'); li.innerHTML = '<span class="t">' + hm(start + offs[i]) + '</span><span></span>'; li.lastChild.textContent = (i + 1) + '. ' + s.title + (s.skippable ? ' (παραλείπεται)' : ''); li.onclick = function () { go(i); }; ol.appendChild(li); });
    sync();
  }
  function sync() {
    if (!pres || pres.closed) return;
    var pd = pres.document, s = S[cur];
    pd.getElementById('ttl').textContent = (cur + 1) + '. ' + s.title;
    pd.getElementById('meta').innerHTML = hm(start + offs[cur]) + ' → ' + hm(start + offs[cur] + s.mins) + ' (' + s.mins + '′)' + (s.skippable ? '<span class="skip">Αν είστε πίσω, παραλείπεται</span>' : '');
    pd.getElementById('plan').textContent = hm(start + offs[cur]);
    var ul = pd.getElementById('notes'); ul.innerHTML = '';
    s.notes.forEach(function (n) { var li = pd.createElement('li'); li.textContent = n; ul.appendChild(li); });
    pd.getElementById('nxt').textContent = cur < N - 1 ? 'Επόμενη: ' + S[cur + 1].title : 'Τέλος μέρους.';
    [].forEach.call(pd.querySelectorAll('#sheet li'), function (li, i) { li.className = i === cur ? 'cur' : ''; if (i === cur) li.scrollIntoView({ block: 'nearest' }); });
  }
  setInterval(function () {
    if (!pres || pres.closed) return;
    var pd = pres.document, now = new Date(), nowMin = now.getHours() * 60 + now.getMinutes() + now.getSeconds() / 60;
    pd.getElementById('now').textContent = hm(Math.floor(nowMin));
    var late = Math.round(nowMin - (start + offs[cur] + S[cur].mins)), box = pd.getElementById('paceBox'), p = pd.getElementById('pace');
    if (Math.abs(nowMin - start) > 180) { p.textContent = 'εκτός ώρας'; box.className = 'box pace'; }
    else if (late > 0) { p.textContent = late + '′ πίσω'; box.className = 'box pace late'; }
    else { p.textContent = 'εντός χρόνου'; box.className = 'box pace ok'; }
  }, 1000);

  // hide the controls while presenting from the keyboard; any mouse movement brings them back
  var idleT; function wake() { document.body.classList.remove('idle'); clearTimeout(idleT); idleT = setTimeout(function () { document.body.classList.add('idle'); }, 2500); }
  addEventListener('mousemove', wake); wake();

  go(Math.max(0, (parseInt(location.hash.slice(1), 10) || 1) - 1));
})();
