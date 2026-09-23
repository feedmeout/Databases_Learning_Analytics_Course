// Usage: node build_html.js content/w1p1.json out/W1P1.html
const fs = require('fs');
const [,, inPath, outPath] = process.argv;
const C = JSON.parse(fs.readFileSync(inPath, 'utf8'));
const N = C.slides.length;

const esc = s => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
const em = s => esc(s)
  .replace(/\*([^*]+)\*/g, '<strong class="em-blue">$1</strong>')
  .replace(/_([^_]+)_/g, '<strong class="em-amber">$1</strong>');
const lamp = tone => `<span class="lamp lamp-${tone}" aria-hidden="true"></span>`;
const src = s => s.src ? `<p class="src">${esc(s.src)}</p>` : '';
const foot = s => s.foot ? `<p class="footline">${em(s.foot)}</p>` : '';
const head = (s, extra = '') => `<header class="head">${extra}<h2>${em(s.title)}</h2></header>`;

function timerPanel(sec) {
  const mm = String(Math.floor(sec / 60)).padStart(2, '0'), ss = String(sec % 60).padStart(2, '0');
  return `<div class="timer" data-sec="${sec}">
    <div class="timer-read" aria-live="off">${mm}:${ss}</div>
    <div class="timer-btns">
      <button type="button" class="t-start">Έναρξη χρονομέτρου</button>
      <button type="button" class="t-reset" aria-label="Μηδενισμός χρονομέτρου">Μηδενισμός</button>
    </div></div>`;
}

const R = {
  title(s) {
    // "trace strip": a term of activity bars that resolves into three signal lamps
    let bars = '', seed = 7;
    const rnd = () => (seed = (seed * 16807) % 2147483647) / 2147483647;
    for (let i = 0; i < 54; i++) {
      const h = 14 + Math.round(rnd() * 70 * (0.45 + 0.55 * Math.sin((i / 54) * Math.PI)));
      bars += `<rect x="${i * 22}" y="${100 - h}" width="12" height="${h}" rx="3"/>`;
    }
    return `<div class="title-wrap">
      <p class="course">${esc(C.meta.course)}</p>
      <h1>${esc(s.title)}</h1>
      <p class="subtitle">${esc(s.subtitle)}</p>
      <svg class="trace" viewBox="0 0 1400 100" aria-hidden="true"><g class="bars">${bars}</g>
        <circle cx="1240" cy="68" r="26" class="l-g"/><circle cx="1308" cy="68" r="26" class="l-a"/><circle cx="1376" cy="68" r="26" class="l-r" transform="translate(-4 0)"/></svg>
      <div class="who"><p class="author">${esc(s.author)}</p><p>${esc(s.affil)}</p><p>${esc(s.email)}</p></div>
      <p class="blockline">${esc(C.meta.block)}, <span data-time="p0s"></span>–<span data-time="p0e"></span></p>
    </div>`;
  },
  plan(s) {
    return head(s) + `<ol class="plan">` + s.rows.map((r, k) => `<li class="${r.now ? 'now' : ''}">
      <span class="ptime"><span data-time="p${k}s"></span>–<span data-time="p${k}e"></span></span>
      <span class="plabel">${esc(r.label)}</span><span class="ptext">${em(r.text)}</span></li>`).join('') + `</ol>` + foot(s);
  },
  activity(s) {
    const body = s.prompt
      ? `<p class="prompt">${em(s.prompt)}</p>`
      : `${s.claim ? `<blockquote class="claim">${em(s.claim)}</blockquote>` : ''}<ol class="steps">${s.steps.map(x => `<li>${em(x)}</li>`).join('')}</ol>`;
    const hint = s.hint ? (s.hintHidden
      ? `<div class="hintbox"><button type="button" class="hint-btn">Εμφάνιση υπόδειξης</button><p class="hint" hidden>${em(s.hint)}</p></div>`
      : `<p class="hint">${em(s.hint)}</p>`) : '';
    return head(s, `<p class="kicker">${lamp('amber')}${esc(s.kicker)}, ${esc(s.duration)}</p>`) +
      `<div class="act"><div class="act-main">${body}${hint}</div>${timerPanel(s.timerSec)}</div>`;
  },
  columns(s) {
    return head(s) + `<div class="cols">` + s.cols.map(c => `<div class="col ${c.focus ? 'focus' : ''}"><h3>${esc(c.h)}</h3><p>${em(c.t)}</p></div>`).join('') + `</div>` + foot(s);
  },
  definition(s) {
    return head(s) + `<blockquote class="defq">${em(s.quote)}<cite>${esc(s.src)}</cite></blockquote>
      <div class="callouts">` + s.callouts.map(c => `<div class="callout c-${c.tone}"><h3>${esc(c.h)}</h3><p>${em(c.t)}</p></div>`).join('') + `</div>`;
  },
  cycle(s) {
    const n = s.nodes;
    return head(s) + `<div class="cyc"><div class="loop" role="img" aria-label="Κύκλος: ${esc(n.join(', '))}">
        <svg viewBox="0 0 760 520" aria-hidden="true"><defs>
          <marker id="ah" markerUnits="userSpaceOnUse" markerWidth="26" markerHeight="26" refX="22" refY="13" orient="auto"><path d="M0,0 L26,13 L0,26 z" fill="#0D47A1"/></marker>
          <marker id="ahr" markerUnits="userSpaceOnUse" markerWidth="26" markerHeight="26" refX="22" refY="13" orient="auto"><path d="M0,0 L26,13 L0,26 z" fill="#C2362F"/></marker></defs>
          <line x1="280" y1="75" x2="474" y2="75" class="arw" marker-end="url(#ah)"/>
          <line x1="620" y1="156" x2="620" y2="364" class="arw" marker-end="url(#ah)"/>
          <line x1="480" y1="445" x2="286" y2="445" class="arw" marker-end="url(#ah)"/>
          <line x1="140" y1="364" x2="140" y2="156" class="arw weak" marker-end="url(#ahr)"/></svg>
        <div class="node n1">${esc(n[0])}</div><div class="node n2">${esc(n[1])}</div>
        <div class="node n3">${esc(n[2])}</div><div class="node n4">${esc(n[3])}</div>
        <p class="weaklabel">${esc(s.weak)}</p></div>
      <div class="cyc-side"><h3>${esc(s.sideH)}</h3><p>${em(s.sideT)}</p>
        <p class="bigstat"><span class="num">${esc(s.stat)}</span><span class="numt">${em(s.statT)}</span></p></div></div>` + src(s);
  },
  quad(s) {
    return head(s) + `<div class="quad">` + s.quads.map(q => `<div class="q"><span class="qq">${esc(q.q)}</span><div><h3>${esc(q.h)}</h3><p>${em(q.t)}</p></div></div>`).join('') + `</div>` + foot(s) + src(s);
  },
  stairs(s) {
    return head(s) + `<div class="stairs">` + s.steps.map((x, k) => `<div class="step s${k + 1}"><h3>${esc(x.h)}</h3><p class="sq">${esc(x.q)}</p><p>${em(x.t)}</p></div>`).join('') + `</div>
      <p class="axis"><svg viewBox="0 0 400 20" aria-hidden="true"><line x1="0" y1="10" x2="388" y2="10" stroke="#5B6B82" stroke-width="3"/><path d="M400,10 L384,2 L384,18 z" fill="#5B6B82"/></svg>${esc(s.axis)}</p>` + `<p class="src">${esc(s.foot)}</p>`;
  },
  signals(s) {
    return head(s) + `<div class="sig"><div class="light" aria-hidden="true"><span class="b r"></span><span class="b a"></span><span class="b g"></span></div>
      <div class="sig-main"><dl>` + s.rows.map(r => `<div><dt>${esc(r.h)}</dt><dd>${em(r.t)}</dd></div>`).join('') + `</dl>
      <blockquote class="claim">${em(s.claim)}<cite>${esc(s.claimSrc)}</cite></blockquote></div></div>` + src(s);
  },
  reveal(s) {
    return head(s, `<p class="kicker">${lamp('red')}${esc(s.kicker)}</p>`) + `<div class="models">` +
      s.models.map(m => `<div class="model m-${m.tone}"><span class="mlabel">${esc(m.label)}</span><span class="mbox">${esc(m.a)}</span>
        <svg viewBox="0 0 70 20" aria-hidden="true"><line x1="0" y1="10" x2="56" y2="10" stroke="currentColor" stroke-width="4"/><path d="M70,10 L52,1 L52,19 z" fill="currentColor"/></svg>
        <span class="mbox">${esc(m.b)}</span></div>`).join('') + `</div>
      <ul class="points">${s.points.map(p => `<li>${em(p)}</li>`).join('')}</ul>
      <p class="lesson">${em(s.lesson)}</p>` + src(s);
  },
  stats(s) {
    return head(s) + `<div class="stats">` + s.stats.map(x => `<div class="stat"><span class="num">${esc(x.n)}</span><p>${em(x.t)}</p></div>`).join('') + `</div>
      <p class="keyline">${em(s.key)}</p><p class="caveat">${lamp('red')}${em(s.caveat)}</p>` + src(s);
  },
  three(s) {
    return head(s) + `<p class="lead">${em(s.lead)}</p><div class="three">` + s.items.map(x => `<div class="item"><h3>${esc(x.h)}</h3><p>${em(x.t)}</p><p class="when">${esc(x.when)}</p></div>`).join('') + `</div>`;
  },
  roadmap(s) {
    return head(s) + `<p class="thread">` + s.thread.map(t => `<span>${esc(t)}</span>`).join('<i aria-hidden="true">→</i>') + `</p>
      <div class="map">` + s.weeks.map((w, wi) => `<div class="wk">${esc(w.w)}</div>` + w.parts.map((p, pi) =>
        `<div class="cell ${wi === 0 && pi === 0 ? 'here' : ''} ${/εργαστήριο/i.test(p) ? 'lab' : ''}">${esc(p)}</div>`).join('')).join('') + `</div>` + foot(s);
  },
  break(s) {
    return `<div class="brk"><h2>${esc(s.title)}</h2>
      <p class="back">Επιστρέφουμε στις <span data-time="back"></span></p>
      <p class="count" data-countdown aria-live="off"></p>
      <div class="keep"><p class="kicker">${lamp('green')}${esc(s.keepKicker)}</p><p>${em(s.keep)}</p></div>
      <p class="next">${em(s.next)}</p></div>`;
  }
};

const dark = t => t === 'title' || t === 'break';
const slidesHtml = C.slides.map((s, i) => `<section class="slide t-${s.type} ${dark(s.type) ? 'dark' : ''}" data-i="${i}" aria-label="Διαφάνεια ${i + 1} από ${N}">
  ${R[s.type](s)}
  <footer class="rail"><span>${esc(C.meta.block)}</span><span>${i + 1} / ${N}</span></footer>
</section>`).join('\n');

const notesData = C.slides.map(s => ({ title: s.title, mins: s.mins, skippable: !!s.skippable, notes: s.notes || [], type: s.type }));

const css = fs.readFileSync(__dirname + '/deck.css', 'utf8');
const js = fs.readFileSync(__dirname + '/deck.client.js', 'utf8');

const html = `<!DOCTYPE html>
<html lang="${C.meta.lang}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${esc(C.meta.block)} | ${esc(C.meta.deckTitle)}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Commissioner:wght@400;500;700;800&display=swap" rel="stylesheet">
<style>${css}</style>
</head>
<body>
<div id="viewport"><div id="stage">
${slidesHtml}
</div></div>
<nav class="ctl" aria-label="Πλοήγηση διαφανειών">
  <button type="button" id="bPrev" aria-label="Προηγούμενη διαφάνεια">‹</button>
  <button type="button" id="bNext" aria-label="Επόμενη διαφάνεια">›</button>
  <button type="button" id="bNotes" title="Σημειώσεις ομιλητή (N)">Σημειώσεις</button>
  <button type="button" id="bHelp" title="Πλήκτρα (?)">?</button>
</nav>
<div id="progress" aria-hidden="true"><i></i></div>
<div id="help" hidden><div><h3>Πλήκτρα</h3><dl>
  <div><dt>← →, Space</dt><dd>προηγούμενη, επόμενη διαφάνεια</dd></div>
  <div><dt>N</dt><dd>παράθυρο σημειώσεων ομιλητή με ρολόι και ρυθμό</dd></div>
  <div><dt>T</dt><dd>έναρξη ή παύση χρονομέτρου δραστηριότητας</dd></div>
  <div><dt>H</dt><dd>εμφάνιση υπόδειξης</dd></div>
  <div><dt>F</dt><dd>πλήρης οθόνη</dd></div>
  <div><dt>P</dt><dd>εκτύπωση ή αποθήκευση ως PDF (μία διαφάνεια ανά σελίδα)</dd></div>
  </dl><p>Άλλη ώρα έναρξης: προσθέστε <code>?start=15:15</code> στη διεύθυνση.</p></div></div>
<script>window.DECK = ${JSON.stringify({ meta: C.meta, slides: notesData })};</script>
<script>${js}</script>
</body></html>`;
fs.writeFileSync(outPath, html);
console.log('wrote', outPath, (html.length / 1024).toFixed(0) + ' KB');
