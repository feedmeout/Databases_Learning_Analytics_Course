// Usage: node build_html2.js content/w1p1_v2.json out/W1P1.html
const fs = require('fs');
const [,, inPath, outPath] = process.argv;
const C = JSON.parse(fs.readFileSync(inPath, 'utf8'));
const N = C.slides.length, SH = C.shared || {};
const esc = s => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
const em = s => esc(s).replace(/\[([^\]]+)\]\((https?:\/\/[^)\s]+)\)/g, (m, l, u) => '<a class="n2a" href="' + u.replace(/\*/g, '&#42;').replace(/_/g, '&#95;') + '" target="&#95;blank" rel="noopener">' + l.replace(/\*/g, '&#42;').replace(/_/g, '&#95;') + '</a>').replace(/`([^`]+)`/g, (m, c) => '<code>' + c.replace(/\*/g, '&#42;').replace(/_/g, '&#95;') + '</code>').replace(/\*([^*]+)\*/g, '<strong class="em-blue">$1</strong>').replace(/_([^_]+)_/g, '<strong class="em-amber">$1</strong>');
const lamp = t => `<span class="lamp lamp-${t}" aria-hidden="true"></span>`;
const kickOf = s => s.kicker ? `<p class="kicker">${lamp(s.kickerTone || 'amber')}${esc(s.kicker)}</p>` : '';
const head = (s, kick) => `<header class="head">${kick === undefined ? kickOf(s) : kick}<h2 class="${s.title.length > 58 ? 'long' : ''}">${em(s.title)}</h2></header>`;
const body = (h, cls = '') => `<div class="body ${cls}">${h}</div>`;
const fmt = sec => String(Math.floor(sec / 60)).padStart(2, '0') + ':' + String(sec % 60).padStart(2, '0');
const timer = sec => `<div class="timer" data-sec="${sec}"><div class="timer-read">${fmt(sec)}</div><div class="timer-btns"><button type="button" class="t-start">Έναρξη χρονομέτρου</button><button type="button" class="t-reset">Μηδενισμός</button></div></div>`;
const MIME = { jpg: 'image/jpeg', png: 'image/png', gif: 'image/gif' };
const IMG = f => `data:${MIME[f.split('.').pop()]};base64,` + fs.readFileSync(require('path').resolve(__dirname, C.meta.imgDir || '.', f)).toString('base64');
const ARW = (id, col) => `<marker id="${id}" markerUnits="userSpaceOnUse" markerWidth="26" markerHeight="26" refX="22" refY="13" orient="auto"><path d="M0,0 L26,13 L0,26 z" fill="${col}"/></marker>`;

function loop(upto, opts = {}) {            // upto: 2..5 ; 5 = loop closed
  const n = SH.cycleNodes, on = k => upto >= k;
  const node = (k, cls) => `<div class="node n${k} ${on(k) ? (k === upto && upto < 5 ? 'cur' : 'on') : 'ghost'} ${cls || ''}">${opts.numbers ? `<i>${k}</i>` : ''}${esc(n[k - 1])}</div>`;
  const ln = (k, x1, y1, x2, y2, extra = '') => `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" class="arw ${on(k) ? '' : 'ghost'} ${extra}" marker-end="url(#${extra.includes('weak') ? 'ahr' : (on(k) ? 'ah' : 'ahg')})"/>`;
  const weak = opts.weak ? 'weak' : '';
  return `<div class="loop" role="img" aria-label="Κύκλος: ${esc(n.join(', '))}"><svg viewBox="0 0 760 520" aria-hidden="true">
    ${ln(2, 288, 75, 472, 75)}${ln(3, 620, 158, 620, 362)}${ln(4, 472, 445, 288, 445)}${ln(5, 140, 362, 140, 158, weak)}</svg>
    ${node(1)}${node(2)}${node(3)}${node(4, opts.weak ? 'weaknode' : '')}${opts.weak ? `<p class="weaklabel">${esc(opts.weak)}</p>` : ''}</div>`;
}
function stairs(upto, full) {
  return `<div class="stairs ${full ? 'full' : ''}">` + SH.stairs.map((st, k) => {
    const state = full ? 'on' : (k + 1 === upto ? 'cur' : (k + 1 < upto ? 'on' : 'ghost'));
    const showQ = full || k + 1 === upto;
    return `<div class="step s${k + 1} ${state}"><h3>${esc(st.h)}</h3>${state !== 'ghost' ? `<p class="tool">${esc(st.tool)}</p>` : ''}${showQ ? `<p class="sq">${st.q.map(q => `«${esc(q)}»`).join('<br>')}</p>` : ''}</div>`;
  }).join('') + `</div>`;
}

const R = {
  title(s) {
    let bars = '', seed = 7; const rnd = () => (seed = (seed * 16807) % 2147483647) / 2147483647;
    for (let i = 0; i < 54; i++) { const h = 14 + Math.round(rnd() * 70 * (0.45 + 0.55 * Math.sin((i / 54) * Math.PI))); bars += `<rect x="${i * 22}" y="${100 - h}" width="12" height="${h}" rx="3"/>`; }
    return `<div class="title-wrap"><p class="course">${esc(C.meta.course)}</p><h1>${esc(s.title)}</h1><p class="subtitle">${esc(s.subtitle)}</p>
      <svg class="trace" viewBox="0 0 1400 100" aria-hidden="true"><g class="bars">${bars}</g><circle cx="1240" cy="68" r="26" class="l-g"/><circle cx="1308" cy="68" r="26" class="l-a"/><circle cx="1372" cy="68" r="26" class="l-r"/></svg>
      <div class="who"><p class="author">${esc(s.author)}</p><p>${esc(s.affil)}</p><p>${esc(s.email)}</p></div></div>`;
  },
  plan(s) {
    return head(s) + body(`<ol class="plan">` + s.rows.map((r, k) => `<li class="${r.now ? 'now' : ''}"><span class="plabel">${esc(r.label)}</span><span>${em(r.text)}</span></li>`).join('') + `</ol>${s.foot ? `<p class="footline muted">${em(s.foot)}</p>` : ''}`);
  },
  objectives(s) {
    return head(s) + body(`<p class="lead muted">${em(s.lead)}</p><ol class="numlist">${s.items.map(x => `<li><span>${em(x)}</span></li>`).join('')}</ol><p class="footline">${em(s.foot)}</p>`);
  },
  bignum(s) {
    return head(s) + body(`<div class="bigs">${s.stats.map(x => `<div><span class="num xl">${esc(x.n)}</span><p>${em(x.t)}</p></div>`).join('')}</div><p class="keyline">${em(s.line)}</p>`);
  },
  definition(s) {
    return head(s) + body(`<blockquote class="defq">${em(s.quote)}<cite>${esc(s.cite)}</cite></blockquote><div class="callouts">${s.callouts.map(c => `<div class="callout c-${c.tone}"><h3>${esc(c.h)}</h3>${c.items ? `<ul class="il">${c.items.map(i => `<li>${em(i)}</li>`).join('')}</ul>` : `<p>${em(c.t)}</p>`}</div>`).join('')}</div>`);
  },
  cards3(s) {
    return head(s) + body(`<div class="three">${s.items.map(x => `<div class="item"><h3>${esc(x.h)}</h3><p>${em(x.t)}</p></div>`).join('')}</div><p class="footline">${em(s.foot)}</p>`);
  },
  quad(s) {
    const tiles = SH.quadTiles.map((t, k) => `<div class="tile ${k === s.active ? 'cur' : (k < s.active ? 'on' : 'ghost')}"><span class="qq">${esc(t.q)}</span><span class="ql">${esc(t.label)}</span></div>`).join('');
    const many = s.groups.length === 1 && s.groups[0].items.length > 4;
    const det = s.groups.map(g => `<div class="grp"><h3>${esc(g.h)}</h3><ul class="${many ? 'cols2' : ''}">${g.items.map(i => `<li>${em(i)}</li>`).join('')}</ul></div>`).join('');
    return head(s) + body(`<div class="quadb"><div class="tiles">${tiles}</div><div class="detail">${det}${s.detailFoot ? `<p class="dfoot">${em(s.detailFoot)}</p>` : ''}</div></div>`);
  },
  quadfull(s) {
    return head(s) + body(`<div class="quadf">${SH.quadTiles.map((t, k) => `<div class="qf"><span class="qq">${esc(t.q)}</span><div><h3>${esc(t.label)}</h3><p>${em(s.texts[k])}</p></div></div>`).join('')}</div><p class="footline">${em(s.foot)}</p>`);
  },
  cycle(s) {
    return head(s) + body(`<div class="cyc">${loop(s.upto, { weak: s.weak })}<div class="cyc-side"><p class="step-text">${em(s.text)}</p></div></div>`);
  },
  cycleai(s) {
    return head(s) + body(`<div class="cyc">${loop(5, { numbers: true })}<ol class="airows">${s.rows.map((r, k) => `<li><span class="k">${k + 1}</span><div><h3>${esc(SH.cycleNodes[k])}</h3><p>${em(r)}</p></div></li>`).join('')}</ol></div>`);
  },
  stairs(s) { return head(s) + body(stairs(s.upto, false), 'bottom'); },
  stairsfull(s) {
    return head(s) + body(`${stairs(4, true)}<div class="axes"><span class="past">Παρελθόν</span><span class="future">Μέλλον</span></div>
      <p class="axis"><svg viewBox="0 0 400 20" aria-hidden="true"><line x1="0" y1="10" x2="386" y2="10" stroke="#55657C" stroke-width="3"/><path d="M400,10 L384,2 L384,18 z" fill="#55657C"/></svg>Αξία και πολυπλοκότητα αυξάνονται μαζί</p><p class="footline sm">${em(s.foot)}</p>`, 'bottom');
  },
  fact(s) {
    const text = /[^\d.,+\s]/.test(s.big);
    return head(s) + body(`<div class="fact"><div class="fbig"><span class="num ${text ? 'word' : 'xl'}">${esc(s.big)}</span><p>${em(s.bigLabel)}</p></div><div class="fmain"><p class="statement">${em(s.statement)}</p><ul class="points">${s.points.map(p => `<li>${em(p)}</li>`).join('')}</ul></div></div>`);
  },
  verdicts(s) {
    return head(s) + body(`<div class="fact"><div class="fbig"><span class="num xl">${esc(s.big)}</span><p>${em(s.bigLabel)}</p></div><div class="fmain"><div class="vrows">${s.rows.map(r => `<div class="vrow"><span class="vh">${esc(r.h)}</span><span class="vv v-${r.tone}">${lamp(r.tone)}${esc(r.v)}</span></div>`).join('')}</div><p class="vnote">${em(s.note)}</p></div></div>`);
  },
  poll(s) {
    return head(s, `<p class="kicker">${lamp('amber')}${esc(s.kicker)}</p>`) + body(`<div class="act"><div>${s.context ? `<p class="context">${em(s.context)}</p>` : ''}${s.code ? `<pre class="n2pq">${esc(s.code)}</pre>` : ''}${s.seqs ? `<div class="pseqs">${s.seqs.map(q => `<div class="pseq"><span class="sfl">${esc(q.label)}</span>${chips(q.seq)}</div>`).join('')}</div>` : ''}<ol class="opts">${s.options.map((o, k) => `<li><b class="ob">${'ΑΒΓΔ'[k]}</b><span>${em(o)}</span></li>`).join('')}</ol></div>${timer(s.timerSec)}</div>`);
  },
  compare(s) {
    return head(s) + body(`<div class="cmp${s.left ? ' left' : ''}">${s.cols.map(c => `<div class="cc c-${c.tone}"><h3>${lamp(c.tone)}${esc(c.h)}</h3><ul>${c.items.map(i => `<li>${em(i)}</li>`).join('')}</ul></div>`).join('')}</div><p class="lesson">${em(s.lesson)}</p>`);
  },
  reveal(s) {
    const arrow = `<svg viewBox="0 0 70 20" aria-hidden="true"><line x1="0" y1="10" x2="56" y2="10" stroke="currentColor" stroke-width="4"/><path d="M70,10 L52,1 L52,19 z" fill="currentColor"/></svg>`;
    return head(s) + body(`<blockquote class="claim">${em(s.claim)}</blockquote><div class="models">${s.models.map(m => `<div class="model m-${m.tone}"><span class="mlabel">${esc(m.label)}</span><span class="mbox">${esc(m.a)}</span>${arrow}<span class="mbox">${esc(m.b)}</span></div>`).join('')}</div><p class="lesson">${em(s.lesson)}</p>`);
  },
  challenge(s) {
    const labels = ['Αλγοριθμική μεροληψία', 'Παραγωγική ΤΝ και ίχνη', 'Κανονιστικό πλαίσιο'];
    return head(s) + body(`<div class="chal"><ol class="chidx">${labels.map((l, k) => `<li class="${k === s.idx ? 'cur' : ''}">${esc(l)}</li>`).join('')}</ol><div><p class="statement">${em(s.statement)}</p><ul class="points">${s.points.map(p => `<li>${em(p)}</li>`).join('')}</ul></div></div>`);
  },
  listslide(s) {
    return head(s, s.kicker ? `<p class="kicker">${lamp(s.kickerTone || 'amber')}${esc(s.kicker)}</p>` : '') + body(`<ol class="numlist ${s.big ? 'big ink' : (s.compact ? 'compact' : 'roomy')}">${s.items.map(x => `<li><span>${em(x)}</span></li>`).join('')}</ol>${s.foot ? `<p class="footline">${em(s.foot)}</p>` : ''}`);
  },
  cardsL(s) {
    return head(s) + body(`<div class="three">${s.items.map(x => `<div class="item ${x.focus ? 'focus' : ''}"><h3>${esc(x.h)}</h3><ul class="il">${x.items.map(i => `<li>${em(i)}</li>`).join('')}</ul></div>`).join('')}</div>${s.foot ? `<p class="footline">${em(s.foot)}</p>` : ''}`);
  },
  table(s) {
    return head(s) + body(`<div class="trows ${s.rows.some(r => r.tag) ? 'tagged' : ''} ${s.compact || s.rows.length > 5 ? 'compact' : ''}${s.wideTag ? ' wtag' : ''}">${s.rows.map(r => `<div class="trow"><span class="trh">${esc(r.h)}</span><span class="trt">${em(r.t)}</span>${r.tag ? `<span class="ttag ${r.tagTone || ''}">${esc(r.tag)}</span>` : ''}</div>`).join('')}</div>${s.foot ? `<p class="footline">${em(s.foot)}</p>` : ''}`);
  },
  cols5(s) {
    return head(s) + body(`<div class="cols5">${s.cols.map((c, k) => `<div class="c5"><span class="c5n">${k + 1}</span><h3>${esc(c.h)}</h3><ul class="il">${c.items.map(i => `<li>${esc(i)}</li>`).join('')}</ul></div>`).join('')}</div>${s.foot ? `<p class="footline">${em(s.foot)}</p>` : ''}`);
  },
  stack(s) {
    return head(s) + body(`<div class="stackrow">${s.stages.map(st => `<div class="stg"><h3>${esc(st.h)}</h3><p>${esc(st.t)}</p></div>`).join('<i class="sarr" aria-hidden="true">→</i>')}</div>
      <div class="stack2"><div><p class="codelabel">${esc(s.codeLabel)}</p><pre class="code">${esc(s.code)}</pre></div><p class="dfoot">${em(s.foot)}</p></div>`);
  },
  datacycle(s) {
    const L = SH.cycle7, cx = 380, cy = 268, rx = 286, ry = 206, w = 200, h = 78; let nodes = '', chev = '';
    L.forEach((t, k) => {
      const a = (-90 + k * 360 / 7) * Math.PI / 180, x = cx + rx * Math.cos(a) - w / 2, y = cy + ry * Math.sin(a) - h / 2;
      const st = s.cur.includes(k) ? 'cur' : (k < s.upto ? 'on' : 'ghost');
      nodes += `<div class="dnode ${st}" style="left:${x.toFixed(0)}px;top:${y.toFixed(0)}px">${esc(t)}</div>`;
      const m = (-90 + (k + 0.5) * 360 / 7) * Math.PI / 180, mx = cx + rx * Math.cos(m), my = cy + ry * Math.sin(m), rot = Math.atan2(ry * Math.cos(m), -rx * Math.sin(m)) * 180 / Math.PI;
      const lit = k + 1 < s.upto || (s.upto === 7 && k === 6);
      chev += `<path d="M-11,-10 L11,0 L-11,10 z" transform="translate(${mx.toFixed(1)} ${my.toFixed(1)}) rotate(${rot.toFixed(1)})" fill="${lit ? '#0D47A1' : '#C9D4E3'}"/>`;
    });
    const det = s.groups.map(g => `<div class="grp"><h3>${esc(g.h)}</h3><ul>${g.items.map(i => `<li>${em(i)}</li>`).join('')}</ul></div>`).join('');
    return head(s) + body(`<div class="cyc"><div class="ring" role="img" aria-label="Κύκλος δεδομένων: ${esc(L.join(', '))}"><svg viewBox="0 0 760 540" aria-hidden="true">${chev}</svg>${nodes}<div class="ringc">Κύκλος δεδομένων</div></div><div class="detail">${det}${s.dfoot ? `<p class="dfoot">${em(s.dfoot)}</p>` : ''}</div></div>`);
  },
  chain(s) {
    const parts = s.boxes.map((b, k) => `<div class="cbox c${k}"><span class="ck">${esc(b.k)}</span><span class="ct">${esc(b.t)}</span></div>`);
    const link = t => `<div class="clink"><span>${esc(t)}</span><svg viewBox="0 0 120 20" aria-hidden="true"><line x1="0" y1="10" x2="104" y2="10" stroke="#12233F" stroke-width="4"/><path d="M120,10 L100,1 L100,19 z" fill="#12233F"/></svg></div>`;
    return head(s) + body(`<div class="chainrow">${parts[0]}${link(s.links[0])}${parts[1]}${link(s.links[1])}${parts[2]}</div><p class="statement wide">${em(s.statement)}</p>`);
  },
  levels(s) {
    const tiles = SH.levelTiles.map((t, k) => `<div class="ltile ${s.active.includes(k) ? 'cur' : (k < Math.min(...s.active) ? 'on' : 'ghost')}">${esc(t)}</div>`).join('');
    const det = s.groups.map(g => `<div class="grp"><h3>${esc(g.h)}</h3><ul class="plain">${g.items.map(i => `<li>${em(i)}</li>`).join('')}</ul></div>`).join('');
    return head(s) + body(`<div class="levb"><div class="ltiles">${tiles}</div><div class="detail">${det}</div></div>`);
  },
  pipeline(s) {
    const chips = SH.pipe.map((t, k) => `<div class="pchip ${k < s.upto ? (k >= (s.upto === 2 ? 0 : s.upto === 4 ? 2 : 4) ? 'cur' : 'on') : 'ghost'}">${esc(t)}</div>`).join('<i class="sarr" aria-hidden="true">→</i>');
    const det = s.groups.map(g => `<div class="grp"><h3>${esc(g.h)}</h3><ul>${g.items.map(i => `<li>${em(i)}</li>`).join('')}</ul></div>`).join('');
    return head(s) + body(`<div class="pipe">${chips}</div>${s.upto === 7 ? '<div class="pback"><span>οι ενέργειες επιστρέφουν ως νέα δεδομένα</span></div>' : '<div class="pback ghostb"></div>'}<div class="pdet">${det}</div>${s.dfoot ? `<p class="dfoot">${em(s.dfoot)}</p>` : ''}`);
  },
  shot(s) {
    return head(s, s.tag ? `<p class="kicker">${lamp('green')}${esc(s.tag)}</p>` : '') + body(`<div class="shot ${s.natural ? 'natural' : ''}"><div class="im"><img class="${s.printImg ? 'scr' : ''}" src="${IMG(s.img)}" alt="${esc(s.title)}">${s.printImg ? `<img class="pr" src="${IMG(s.printImg)}" alt="">` : ''}</div><p class="caption">${em(s.caption)}</p></div>`, 'fill');
  },
  shotside(s) {
    const im = `<img src="${IMG(s.img)}" alt="${esc(s.title)}">`;
    return head(s) + body(`<div class="shotside${s.caption ? ' capd' : ''}">${s.caption ? `<figure class="ssfig">${im}<figcaption class="caption">${em(s.caption)}</figcaption></figure>` : im}<ul class="points">${s.points.map(p => `<li>${em(p)}</li>`).join('')}</ul></div>`);
  },
  schema(s) {
    const tb = t => `<div class="tb"><span class="tn">${esc(t.n)}</span><span class="tk">${esc(t.k)}</span>${t.c ? `<span class="tc">${esc(t.c)}</span>` : ''}</div>`;
    return head(s) + body(`<div class="schema"><div class="scol"><h3>Μαθήματα</h3>${s.left.map(tb).join('')}</div><div class="scol stu"><h3>Φοιτητές</h3>${s.right.map(tb).join('')}</div></div><p class="footline">${em(s.foot)}</p>`);
  },
  flow(s) {
    const chips = s.chips.map((t, k) => `<div class="pchip ${s.cur.includes(k) ? 'cur' : 'on'}"><b class="fn">${k + 1}</b>${esc(t)}</div>`).join('<i class="sarr" aria-hidden="true">→</i>');
    const det = (s.groups || []).map(g => `<div class="grp"><h3>${esc(g.h)}</h3><ul>${g.items.map(i => `<li>${em(i)}</li>`).join('')}</ul></div>`).join('');
    return head(s) + body(`<div class="pipe flowp">${chips}</div><div class="pdet">${det}</div>`);
  },
  grid(s) {
    return head(s) + body(`<div class="gridn${s.tall ? ' tall' : ''}" style="grid-template-columns:repeat(${s.colsN},1fr)">${s.items.map(x => `<div class="gcard"><h3>${esc(x.h)}</h3><p>${em(x.t)}</p></div>`).join('')}</div>${s.foot ? `<p class="footline">${em(s.foot)}</p>` : ''}`);
  },
  codeslide(s) {
    return head(s) + body(`<div class="codes"><pre class="code big">${esc(s.code)}</pre><ul class="points">${s.points.map(p => `<li>${em(p)}</li>`).join('')}</ul></div>`);
  },
  htable(s) {
    return head(s) + body(`<table class="ht${s.compact ? ' compact' : ''}"><thead><tr>${s.head.map(h => `<th>${esc(h)}</th>`).join('')}</tr></thead><tbody>${s.rows.map(r => `<tr>${r.map(c => `<td>${em(c)}</td>`).join('')}</tr>`).join('')}</tbody></table>${s.foot ? `<p class="footline">${em(s.foot)}</p>` : ''}`);
  },
  prisma(s) {
    const n = v => s.filled ? ` <b class="pn2">n = ${v}</b>` : '';
    const sub = t => s.filled ? `<span class="psub">${esc(t)}</span>` : '';
    const row = (ph, main, side, last) => `<div class="pph">${ph ? esc(ph) : ''}</div><div class="pm ${last ? 'last' : ''}">${main}</div><div class="parr">${side ? '→' : ''}</div>${side ? `<div class="ps">${side}</div>` : '<div></div>'}`;
    return head(s) + body(`<div class="prisma">
      ${row('Εντοπισμός', `Εγγραφές από βάσεις δεδομένων${n(412)}${sub('Scopus 230, ERIC 96, IEEE Xplore 52, ACM DL 34')}`, `Αφαιρέθηκαν πριν από τον έλεγχο: διπλοεγγραφές${n(97)}`)}
      ${row('Έλεγχος', `Εγγραφές που ελέγχθηκαν με βάση τίτλο και περίληψη${n(315)}`, `Αποκλείστηκαν${n(251)}`)}
      ${row('', `Πλήρη κείμενα που αναζητήθηκαν${n(64)}`, `Δεν ανακτήθηκαν${n(5)}`)}
      ${row('', `Πλήρη κείμενα που αξιολογήθηκαν${n(59)}`, `Αποκλείστηκαν με αιτιολογία${n(36)}${sub('μη εμπειρικές 14, εκτός ανώτατης εκπαίδευσης 9, χωρίς μέτρηση αυτορρύθμισης 13')}`)}
      ${row('Ένταξη', `Μελέτες που εντάχθηκαν στην ανασκόπηση${n(23)}`, '', true)}
    </div>`);
  },
  rubric(s) {
    return head(s) + body(`<div class="rbar">${s.parts.map(p => `<div class="rseg ${p.hot ? 'hot' : ''}" style="flex:${p.p}"><b>${p.p}%</b></div>`).join('')}</div>
      <div class="rleg">${s.parts.map(p => `<div class="rl ${p.hot ? 'hot' : ''}"><i></i><span>${esc(p.h)}</span><b>${p.p}%</b></div>`).join('')}</div><p class="footline">${em(s.foot)}</p>`);
  },
  endslide(s) { return `<div class="teaser"><h2>${esc(s.title)}</h2><p>${em(s.line)}</p></div>`; },
  teaser(s) { return `<div class="teaser"><h2>${esc(s.title)}</h2><p>${em(s.line)}</p></div>`; },
  roadmap(s) {
    return head(s) + body(`<p class="thread">${s.thread.map(t => `<span>${esc(t)}</span>`).join('<i aria-hidden="true">→</i>')}</p><div class="map">${s.weeks.map((w, wi) => `<div class="wk">${esc(w.w)}</div>` + w.parts.map((p, pi) => `<div class="cell ${wi === 0 && pi === 0 ? 'here' : ''} ${/Εργαστήριο/.test(p) ? 'lab' : ''}">${esc(p)}</div>`).join('')).join('')}</div><p class="footline sm">${em(s.foot)}</p>`);
  },
  remember(s) {
    return head(s, `<p class="kicker">${lamp('green')}${esc(s.kicker)}</p>`) + body(`<ol class="numlist big">${s.items.map(x => `<li><span>${em(x)}</span></li>`).join('')}</ol>`);
  },
  break(s) {
    const m = C.meta.breakMin || 15;
    return `<div class="brk"><h2>${esc(s.title)}</h2><p class="back">Επιστρέφουμε σε <span>${m}′</span></p><p class="count" data-break="${m}">${String(m).padStart(2, '0')}:00</p><p class="next">${em(s.next)}</p></div>`;
  }
};

// ---------- Week 2 additions (new slide types; Week 1 types are untouched) ----------
const gr = v => String(v).replace('.', ',');                                   // Greek decimal comma
const TONE = { E: 'e', S: 's' };
function chips(seq, map) { return `<span class="sqrow">${[...seq].map(ch => `<span class="sq ${(map && map[ch]) || TONE[ch] || 'a'}">${esc(ch)}</span>`).join('')}</span>`; }
function chainSvg(a, b, p) {                                                   // two-state Markov chain
  const lab = (x, y, t) => `<text class="p" x="${x}" y="${y}">${esc(t)}</text>`;
  return `<svg class="chsvg" viewBox="0 0 840 420" role="img" aria-label="Αλυσίδα δύο καταστάσεων: ${esc(a.name)}, ${esc(b.name)}">
    <path class="ar" d="M 305,157 Q 420,70 535,157" marker-end="url(#ah)"/><path class="ar" d="M 535,263 Q 420,350 305,263" marker-end="url(#ah)"/>
    <path class="ar" d="M 147,171 C 30,110 30,310 147,249" marker-end="url(#ah)"/><path class="ar" d="M 693,171 C 810,110 810,310 693,249" marker-end="url(#ah)"/>
    <circle class="st t-${a.tone}" cx="230" cy="210" r="86"/><circle class="st t-${b.tone}" cx="610" cy="210" r="86"/>
    <text class="k ${a.tone}" x="230" y="200">${esc(a.k)}</text><text class="nm ${a.tone}" x="230" y="254">${esc(a.name)}</text>
    <text class="k ${b.tone}" x="610" y="200">${esc(b.k)}</text><text class="nm ${b.tone}" x="610" y="254">${esc(b.name)}</text>
    ${lab(420, 100, p.ab)}${lab(420, 346, p.ba)}${lab(60, 222, p.aa)}${lab(780, 222, p.bb)}</svg>`;
}
Object.assign(R, {
  gradetab(s) {
    const th = s.head.map((h, k) => `<th class="${k === s.hiCol ? 'hi' : ''}">${esc(h)}</th>`).join('');
    const tr = s.rows.map(r => `<tr>${r.map((c, k) => `<td class="${k === s.hiCol ? 'hi' : ''}">${esc(c)}</td>`).join('')}</tr>`).join('');
    const arrow = s.arrow ? `<div class="garrow"><span>${esc(s.arrow.top)}</span><i class="gline" aria-hidden="true"></i><span>${esc(s.arrow.bottom)}</span></div>` : '';
    const side = s.side ? `<div class="gside"><h3>${esc(s.side.h)}</h3><ol class="exlist">${s.side.items.map((x, k) => `<li><b>${esc(s.side.prefix)}${k + 1}</b> ${esc(x)}</li>`).join('')}</ol></div>` : '';
    const quote = s.quote ? `<div class="gside"><p class="gquote">${em(s.quote)}</p>${(s.notesOn || []).map(t => `<p class="gnote">${em(t)}</p>`).join('')}</div>` : '';
    return head(s) + body(`<div class="gt ${s.hiCol !== undefined ? 'wide' : ''}"><div class="gtl"><p class="gcap">${esc(s.tableTitle)}</p><div class="gtw"><table class="gtab"><thead><tr>${th}</tr></thead><tbody>${tr}</tbody></table>${arrow}</div></div>${side}${quote}</div>`);
  },
  seqflow(s) {
    const pairsOf = q => [...q].slice(1).map((c, i) => `(${q[i]}<sub>${i + 1}</sub>,&nbsp;${c}<sub>${i + 2}</sub>)`).join(' ');
    const arr = t => `<div class="sfarr"><span>${esc(t)}</span><svg viewBox="0 0 150 20" aria-hidden="true"><line x1="0" y1="10" x2="134" y2="10" stroke="#12233F" stroke-width="4"/><path d="M150,10 L130,1 L130,19 z" fill="#12233F"/></svg></div>`;
    return head(s) + body(`<div class="sfpipe"><div class="sfbox">${esc(s.pipe.from)}</div>${arr(s.pipe.a1)}<div class="sfbox mid">${s.pipe.mid.map(m => `<span><b>${esc(m[0])}</b> ${esc(m[1])}</span>`).join('')}</div>${arr(s.pipe.a2)}<div class="sfbox">${esc(s.pipe.to)}</div><div class="sfloop"><span>${esc(s.pipe.loop)}</span></div></div>
      <div class="sfh"><span></span><span>${esc(s.cols[0])}</span><span>${esc(s.cols[1])}</span><span></span></div>
      <div class="sfrows">${s.students.map(u => `<div class="sfrow"><span class="sfl">${esc(u.label)}</span>${chips(u.seq)}<span class="pairs">${pairsOf(u.seq)}</span>${u.tag ? `<span class="sftag">${esc(u.tag)}</span>` : '<span></span>'}</div>`).join('')}</div>${s.foot ? `<p class="footline">${em(s.foot)}</p>` : ''}`);
  },
  chain2(s) {
    const side = `<div class="ch2side">${s.seq ? `<div class="blk"><h3>${esc(s.seqLabel)}</h3>${chips(s.seq, s.seqMap)}</div>` : ''}${s.statement ? `<p class="statement">${em(s.statement)}</p>` : ''}${s.legend ? `<ul class="legend">${s.legend.map(l => `<li><b>${esc(l[0])}</b><span>${esc(l[1])}</span></li>`).join('')}</ul>` : ''}${s.points ? `<ul class="points">${s.points.map(x => `<li>${em(x)}</li>`).join('')}</ul>` : ''}</div>`;
    return head(s) + body(`<div class="ch2">${chainSvg(s.a, s.b, s.p)}${side}</div>${s.foot ? `<p class="footline">${em(s.foot)}</p>` : ''}`);
  },
  tmatrix(s) {                                                                 // counts and probabilities are computed from s.seq, never typed by hand
    const q = [...s.seq], pairs = q.slice(1).map((c, i) => q[i] + c), cnt = { EE: 0, ES: 0, SE: 0, SS: 0 };
    pairs.forEach(x => cnt[x]++);
    const sumE = cnt.EE + cnt.ES, sumS = cnt.SE + cnt.SS, pr = (n, d) => gr((n / d).toFixed(2));
    const cell = (k, d) => s.step === 1 ? `<td>${cnt[k]}</td>` : `<td class="pr">${pr(cnt[k], d)}<small>${cnt[k]} / ${d}</small></td>`;
    const tab = `<table class="ctab"><thead><tr><th></th><th>προς E</th><th>προς S</th><th>Σύνολο</th></tr></thead><tbody>
      <tr><th>από E</th>${cell('EE', sumE)}${cell('ES', sumE)}<td class="sum">${s.step === 1 ? sumE : '1,00'}</td></tr>
      <tr><th>από S</th>${cell('SE', sumS)}${cell('SS', sumS)}<td class="sum">${s.step === 1 ? sumS : '1,00'}</td></tr></tbody></table>`;
    const left = s.step === 1
      ? `<div class="blk"><h3>${esc(s.seqLabel)}</h3>${chips(s.seq)}</div><div class="blk"><h3>${esc(s.pairLabel)}: ${pairs.length}</h3><div class="pairchips">${pairs.map(x => `<span class="pc">${chips(x)}</span>`).join('')}</div></div>`
      : chainSvg({ k: 'E', name: 'Error', tone: 'red' }, { k: 'S', name: 'Success', tone: 'green' }, { aa: pr(cnt.EE, sumE), ab: pr(cnt.ES, sumE), ba: pr(cnt.SE, sumS), bb: pr(cnt.SS, sumS) });
    return head(s) + body(`<div class="tmx step${s.step}"><div class="tml">${left}</div><div class="tmr"><h3>${esc(s.tabLabel)}</h3>${tab}</div></div>${s.foot ? `<p class="footline">${em(s.foot)}</p>` : ''}`);
  },
  adjmatrix(s) {
    const st = s.states, to = { S: [2, 4, 5, 7], E: [1, 3, 5, 6] };                // Lokkila, Christopoulos & Laakso (2023), Table 1
    const hd = st.map(x => `<th><span class="k${x.k}">${x.n}</span></th>`).join('');
    const rows = st.map(r => `<tr><th>${esc(r.name)} <span class="k${r.k}">${r.n}</span></th>${st.map(c => to[r.k].includes(c.n) ? `<td class="to${c.k}">${r.k}${c.k}</td>` : '<td></td>').join('')}</tr>`).join('');
    return head(s) + body(`<div class="adj"><div><table class="amx"><thead><tr><th class="corner">${esc(s.corner)}</th>${hd}</tr></thead><tbody>${rows}</tbody></table><p class="amnote">${em(s.matrixNote)}</p></div><ol class="asteps">${s.steps.map(x => `<li><div><h3>${esc(x.h)}</h3><p>${em(x.t)}</p></div></li>`).join('')}</ol></div>${s.foot ? `<p class="footline">${em(s.foot)}</p>` : ''}`);
  },
  anatomy(s) {
    const W = s.weeks, cut = s.cut, g = s.upto < 2 ? 'ghosted' : '';
    const track = fut => `<div class="track" style="grid-template-columns:repeat(${W},1fr)"><span class="ppoint" style="left:calc(${cut} * (100% + 6px) / ${W} - 3px)">${esc(s.pointLabel)}</span>${Array.from({ length: W }, (_, k) => `<span class="wkc ${k < cut ? 'feat' : (fut ? 'fut' : 'rest')}">${k + 1}</span>`).join('')}</div>`;
    const flow = a => `<div class="midflow">${a.map(x => x === '>' ? '<i class="sarr" aria-hidden="true">→</i>' : `<span class="mchip ${x.cls || ''}">${esc(x.t)}</span>`).join('')}</div>`;
    const L = s.lanes;
    return head(s) + body(`<div class="ana">
      <div class="lane"><div class="lh">${esc(L[0].h)}<small>${esc(L[0].sub)}</small></div>${track(false)}<div class="endb known">${esc(L[0].end)}</div></div>
      <div class="lane mid"><div></div>${flow(s.train)}<div></div></div>
      <div class="lane ${g}"><div class="lh">${esc(L[1].h)}<small>${esc(L[1].sub)}</small></div>${track(true)}<div class="endb unk">${esc(L[1].end)}</div></div>
      <div class="lane mid ${g}"><div></div>${flow(s.apply)}<div></div></div></div><p class="footline">${em(s.foot)}</p>`);
  }
});

// ---------- Lab additions (Week 2, Part 2) ----------
Object.assign(R, {
  work(s) {                                                                    // group-work or report slide: prompts + the only time label = the timer
    return head(s) + body(`<div class="act work"><div><p class="context">${em(s.context)}</p><ol class="numlist wk">${s.items.map(x => `<li><span>${typeof x === 'string' ? em(x) : em(x.t) + `<code class="n2code">${esc(x.code)}</code>`}</span></li>`).join('')}</ol>${s.foot ? `<p class="footline sm">${em(s.foot)}</p>` : ''}</div>${timer(s.timerSec)}</div>`);
  },
  datagrid(s) {                                                                // what is recorded in which week, with the prediction point
    const W = s.weeks, HW = 330, XW = 120, G = 6, cw = (1424 - HW - XW - (W + 1) * G) / W, cutX = HW + G + s.cut * (cw + G) - G / 2 - 2.5;
    const cols = `grid-template-columns:${HW}px repeat(${W},1fr) ${XW}px`;
    const hdr = `<div class="dgr" style="${cols}"><span class="dgk">${esc(s.weekLabel)}</span>${Array.from({ length: W }, (_, k) => `<span class="dgw">${k + 1}</span>`).join('')}<span class="dgw">${esc(s.examLabel)}</span></div>`;
    const rows = s.rows.map(r => `<div class="dgr" style="${cols}"><span class="dgh">${esc(r.h)}<small>${esc(r.sub || '')}</small></span>${Array.from({ length: W }, (_, k) => `<span class="dgc ${(r.weeks || []).includes(k + 1) ? (k + 1 <= s.cut ? 'on' : 'late') : ''}"></span>`).join('')}<span class="dgc ${r.exam ? 'late' : ''}"></span></div>`).join('');
    return head(s) + body(`<div class="dg">${hdr}${rows}<span class="dgcut" style="left:${cutX.toFixed(1)}px"><b>${esc(s.pointLabel)}</b></span></div><p class="dgleg"><span><i class="on"></i>${esc(s.legend[0])}</span><span><i class="late"></i>${esc(s.legend[1])}</span></p>${s.foot ? `<p class="footline">${em(s.foot)}</p>` : ''}`);
  },
  bars(s) {                                                                    // native bar panels; values come from lab1/exhibits.json through the content file
    const H = s.barH || 240;
    const panel = p => {
      const all = p.groups ? p.groups.flatMap(g => g.bars) : p.bars, max = p.unit === '%' ? (p.max || 1) : Math.max(...all.map(b => b.v));
      const bar = b => `<div class="bar"${p.bw ? ` style="width:${p.bw}px"` : ''}><span class="bv">${p.unit === '%' ? Math.round(b.v * 100) + '%' : b.v}</span><i class="t-${b.tone || p.tone || 'blue'}" style="height:${Math.max(3, Math.round(b.v / max * H))}px"></i><span class="bl">${esc(b.l).replace(/\n/g, '<br>')}</span>${b.n !== undefined ? `<span class="bn">n = ${b.n}</span>` : ''}</div>`;
      const inner = p.groups ? p.groups.map(g => `<div class="bgrp"><div class="barrow">${g.bars.map(bar).join('')}</div><span class="bgl">${esc(g.h)}</span></div>`).join('') : `<div class="barrow">${p.bars.map(bar).join('')}</div>`;
      return `<div class="panel${p.dense ? ' dense' : ''}" style="flex:${p.flex || 1}"><h3>${esc(p.h)}</h3><div class="pbody">${inner}</div>${p.note ? `<p class="pnote">${em(p.note)}</p>` : ''}</div>`;
    };
    return head(s) + body(`<div class="bp${s.points ? ' withside' : ''}"><div class="panels p${s.panels.length}">${s.panels.map(panel).join('')}</div>${s.points ? `<ul class="points">${s.points.map(x => `<li>${em(x)}</li>`).join('')}</ul>` : ''}</div>${s.lesson ? `<p class="lesson">${em(s.lesson)}</p>` : ''}`);
  },
  dgp(s) {                                                                     // the data-generating process: traces <- causes -> outcomes
    const Y = [46, 172, 298, 424], on2 = s.upto >= 2;
    const box = (cls, x, w, k, o) => `<div class="dn ${cls}" style="left:${x}px;top:${Y[k] - 42}px;width:${w}px"><b>${esc(o.h)}</b>${o.tag ? `<small>${esc(o.tag)}</small>` : ''}</div>`;
    const ln = (x1, y1, x2, y2, lab, lx, ly, cls) => `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" class="da" marker-end="url(#ah)"/>${lab ? `<text x="${lx}" y="${ly}" class="dl ${cls || ''}">${esc(lab)}</text>` : ''}`;
    const tr = s.traces.map((t, k) => box(on2 ? 'trc' : 'trc ghost', 0, 392, k, on2 ? t : { h: t.h })).join('');
    const ca = s.causes.map((c, k) => box(c.hidden ? 'cause hidden' : 'cause', 546, 330, k, c)).join('');
    const ou = box('outc', 1044, 380, 2, s.outcomes[0]) + box('outc', 1044, 380, 3, s.outcomes[1]);
    const arrowsT = on2 ? ln(546, Y[0], 406, Y[0]) + ln(546, Y[1], 406, Y[1], s.labels.late, 476, Y[1] - 12, 'sm') + ln(546, Y[2] - 18, 406, Y[1] + 18) + ln(546, Y[2], 406, Y[2], '+', 476, Y[2] - 10) + ln(546, Y[3] - 18, 406, Y[2] + 18, '−', 466, Y[3] - 70) + ln(546, Y[3], 406, Y[3]) : '';
    return head(s) + body(`<div class="dgp"><svg viewBox="0 0 1424 470" aria-hidden="true">${arrowsT}${ln(876, Y[2], 1030, Y[2])}${ln(876, Y[3], 1030, Y[3])}<path d="M 876,${Y[0]} C 990,${Y[0] + 10} 990,${Y[2] - 50} 888,${Y[2] - 14}" class="da" fill="none" marker-end="url(#ah)"/></svg>
      <span class="dcol" style="left:0;width:392px">${esc(s.cols[0])}</span><span class="dcol" style="left:546px;width:330px">${esc(s.cols[1])}</span><span class="dcol" style="left:1044px;width:380px">${esc(s.cols[2])}</span>${tr}${ca}${ou}<p class="dnote" style="left:1044px;top:${Y[1] - 60}px;width:380px">${em(s.outNote)}</p></div><p class="footline">${em(s.foot)}</p>`);
  }
});

// ---------- Week 2, Part 3 additions: marked screenshot, chart chooser, method pictures, dashboard mock-up, search funnel ----------
const GLY = {   // small native chart glyphs, 120 x 80
  bars: `<rect x="10" y="40" width="18" height="34"/><rect x="36" y="22" width="18" height="52"/><rect x="62" y="50" width="18" height="24"/><rect x="88" y="12" width="18" height="62"/>`,
  line: `<polyline points="8,62 34,40 58,50 84,22 112,30" fill="none" stroke-width="6" stroke-linejoin="round" stroke-linecap="round" class="gs"/>`,
  scatter: `<circle cx="18" cy="60" r="6"/><circle cx="36" cy="46" r="6"/><circle cx="52" cy="52" r="6"/><circle cx="66" cy="34" r="6"/><circle cx="84" cy="28" r="6"/><circle cx="102" cy="14" r="6"/>`,
  bubble: `<circle cx="24" cy="54" r="12"/><circle cx="62" cy="34" r="20"/><circle cx="100" cy="56" r="8"/>`,
  hist: `<rect x="8" y="58" width="16" height="16"/><rect x="26" y="40" width="16" height="34"/><rect x="44" y="16" width="16" height="58"/><rect x="62" y="28" width="16" height="46"/><rect x="80" y="50" width="16" height="24"/><rect x="98" y="64" width="16" height="10"/>`,
  box: `<line x1="10" y1="42" x2="110" y2="42" stroke-width="5" class="gs"/><rect x="38" y="22" width="46" height="40"/><line x1="58" y1="22" x2="58" y2="62" stroke="#fff" stroke-width="5"/>`,
  stack: `<rect x="12" y="44" width="22" height="30"/><rect x="12" y="20" width="22" height="22" class="g2"/><rect x="48" y="36" width="22" height="38"/><rect x="48" y="14" width="22" height="20" class="g2"/><rect x="84" y="52" width="22" height="22"/><rect x="84" y="24" width="22" height="26" class="g2"/>`,
  area: `<path d="M8,74 L8,52 L40,36 L72,44 L112,18 L112,74 z"/><path d="M8,74 L8,64 L40,56 L72,60 L112,46 L112,74 z" class="g2"/>`,
  heat: [0, 1, 2, 3].map(r => [0, 1, 2, 3].map(c => `<rect x="${14 + c * 24}" y="${4 + r * 18}" width="22" height="16" rx="3" style="opacity:${[1, .25, .45, .15, .3, .9, .2, .5, .15, .35, 1, .3, .4, .2, .55, .85][r * 4 + c]}"/>`).join('')).join(''),
  net: `<g class="gs" stroke-width="4"><line x1="26" y1="22" x2="62" y2="40"/><line x1="62" y1="40" x2="100" y2="20"/><line x1="62" y1="40" x2="40" y2="66"/><line x1="62" y1="40" x2="92" y2="62"/><line x1="26" y1="22" x2="40" y2="66"/></g><circle cx="26" cy="22" r="9"/><circle cx="62" cy="40" r="13"/><circle cx="100" cy="20" r="8"/><circle cx="40" cy="66" r="8"/><circle cx="92" cy="62" r="8"/>`,
  clus: `<circle cx="22" cy="56" r="6"/><circle cx="34" cy="64" r="6"/><circle cx="36" cy="48" r="6"/><circle cx="76" cy="22" r="6" class="g2"/><circle cx="90" cy="30" r="6" class="g2"/><circle cx="92" cy="14" r="6" class="g2"/><circle cx="84" cy="62" r="6" class="g3"/><circle cx="100" cy="56" r="6" class="g3"/>`,
  rank: `<rect x="10" y="8" width="100" height="12" rx="3" class="g3"/><rect x="10" y="26" width="78" height="12" rx="3" class="g3"/><rect x="10" y="44" width="52" height="12" rx="3" class="g2"/><rect x="10" y="62" width="30" height="12" rx="3"/>`,
  seq: [0, 1, 2].map(r => [0, 1, 2, 3, 4, 5].map(c => `<rect x="${8 + c * 18}" y="${10 + r * 22}" width="16" height="16" rx="3" class="${'ESEESS SSESSS EEEESE'.split(' ')[r][c] === 'E' ? 'g3' : 'g4'}"/>`).join('')).join('')
};
const glyph = k => `<svg class="gly" viewBox="0 0 120 80" aria-hidden="true">${GLY[k]}</svg>`;
Object.assign(R, {
  shotmark(s) {                                                                 // the lecturer's screenshot with native numbered markers; with timerSec it becomes the timed question
    const marks = (s.marks || []).map((m, k) => (m.w ? `<span class="mkb" style="left:${m.x}%;top:${m.y}%;width:${m.w}%;height:${m.h}%"></span>` : '') + `<span class="mkn" style="left:${m.x}%;top:${m.y}%">${k + 1}</span>`).join('');
    const fig = `<div class="smkw"><img src="${IMG(s.img)}" alt="${esc(s.title)}">${marks}</div>`;
    if (s.timerSec) return head(s) + body(`<div class="smk smkq"><div class="smkl">${fig}</div><div class="qside"><p class="context">${em(s.question)}</p><ol class="numlist wk">${s.marks.map(m => `<li><span>${em(m.label)}</span></li>`).join('')}</ol>${timer(s.timerSec)}</div></div>`);
    return head(s) + body(`<div class="smk">${fig}<p class="caption">${em(s.caption)}</p></div>`);
  },
  chooser(s) {                                                                  // from the question to the chart: four purposes, each with a Learning Analytics question
    return head(s) + body(`<div class="chz">${s.items.map(x => `<div class="chq"><div><h3>${esc(x.h)}</h3><p class="chg">${em(x.q)}</p><p class="chx">${em(x.ex)}</p></div><div class="chico">${x.charts.map(c => `<figure>${glyph(c.g)}<figcaption>${esc(c.l)}</figcaption></figure>`).join('')}</div></div>`).join('')}</div>`);
  },
  methodpics(s) {                                                               // each method of Part 1 and its natural picture
    return head(s) + body(`<div class="mpics">${s.items.map(x => `<div class="mpic"><p class="mpm">${esc(x.method)}</p>${glyph(x.g)}<h3>${esc(x.h)}</h3><p>${em(x.t)}</p></div>`).join('')}</div>${s.foot ? `<p class="footline">${em(s.foot)}</p>` : ''}`);
  },
  mock(s) {                                                                     // native mock-up of a teacher screen
    return head(s) + body(`<div class="mkd"><div class="mkdh"><b>${esc(s.bar[0])}</b><span>${esc(s.bar[1])}</span></div><div class="mkt">${s.tiles.map(t => `<div class="mktile"><span class="mkv">${esc(t.v)}</span><span class="mkl">${esc(t.l)}</span></div>`).join('')}</div><div class="mklist">${s.lists.map(l => `<div class="mkli t-${l.tone}"><h3>${esc(l.h)}<em>${esc(l.n)}</em></h3><p class="mkr">${em(l.rule)}</p><p class="mka">${em(l.action)}</p></div>`).join('')}</div><p class="mkf">${em(s.strip)}</p></div>${s.foot ? `<p class="footline">${em(s.foot)}</p>` : ''}`);
  },
  funnel(s) {                                                                   // a search narrowed block by block, with the real counts
    return head(s) + body(`<div class="fnl">${s.rows.map(r => `<div class="fnr"><code>${esc(r.code)}</code><span class="fnn">${esc(r.n)}</span><span class="fnv ${r.tone || ''}">${esc(r.verdict || '')}</span></div>`).join('')}</div>${s.foot ? `<p class="footline">${em(s.foot)}</p>` : ''}`);
  }
});
// ---------- Week 3, Part 1 addition: the confusion matrix as four groups of people (class prefix ppl) ----------
Object.assign(R, {
  people(s) {                                                                   // cells in reading order: row 0 (col 0, col 1), row 1 (col 0, col 1)
    const cell = c => `<div class="pplc ppl-${c.tone}"><b class="ppln">${esc(c.n)}</b><h3>${esc(c.h)}</h3><p>${em(c.t)}</p></div>`;
    return head(s) + body(`<div class="ppl"><div class="pplg"><span></span>${s.cols.map(c => `<span class="pplh">${esc(c)}</span>`).join('')}<span class="pplr">${esc(s.rows[0])}</span>${cell(s.cells[0])}${cell(s.cells[1])}<span class="pplr">${esc(s.rows[1])}</span>${cell(s.cells[2])}${cell(s.cells[3])}</div><div class="ppls">${s.side.map(m => `<div class="pplm"><span class="pplv">${esc(m.v)}</span><span class="ppll">${em(m.l)}</span></div>`).join('')}</div></div>${s.lesson ? `<p class="lesson">${em(s.lesson)}</p>` : ''}`);
  }
});
// ---------- NoSQL additions: shell = command pane + output pane (+ points), class prefix shl ----------
Object.assign(R, {
  shell(s) {                                                                    // cmd and out are shown exactly as typed / as printed by mongosh
    const pane = (label, txt, cls) => `<div class="shlp"><p class="shll">${esc(label)}</p><pre class="shlx ${cls}">${esc(txt)}</pre></div>`;
    return head(s) + body(`<div class="shl${s.points ? '' : ' wide'}${s.dense ? ' dense' : ''}${s.stack ? ' stack' : ''}${s.side ? ' n2side' : ''}"><div class="shlc">${s.sql !== undefined ? pane(s.sqlLabel || 'SQL', s.sql, 'n2sql') : ''}${s.cmd !== undefined ? pane(s.cmdLabel || 'Εντολή', s.cmd, 'c') : ''}${s.out !== undefined ? pane(s.outLabel || 'Αποτέλεσμα', s.out, 'o') : ''}</div>${s.points ? `<ul class="points">${s.points.map(p => `<li>${em(p)}</li>`).join('')}</ul>` : ''}</div>${s.foot ? `<p class="footline sm">${em(s.foot)}</p>` : ''}`);
  }
});
const dark = t => ['title', 'break', 'teaser', 'endslide'].includes(t);
const slidesHtml = C.slides.map((s, i) => `<section class="slide t-${s.type} ${dark(s.type) ? 'dark' : ''}" data-i="${i}" aria-label="Διαφάνεια ${i + 1} από ${N}">${R[s.type](s)}
<footer class="foot"><p class="src">${s.src ? esc(s.src) : ''}</p><span class="pn">${i + 1}</span></footer></section>`).join('\n');
const notesData = C.slides.map(s => ({ title: s.title, mins: s.mins, skippable: !!s.skippable, notes: s.notes || [], type: s.type }));
const css = fs.readFileSync(__dirname + '/deck2.css', 'utf8'), js = fs.readFileSync(__dirname + '/deck.client.js', 'utf8');
fs.writeFileSync(outPath, `<!DOCTYPE html><html lang="${C.meta.lang}"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>${esc(C.meta.part)} | ${esc(C.meta.deckTitle)}</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Commissioner:wght@400;500;700;800&display=swap" rel="stylesheet"><style>${css}</style></head><body>
<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>${ARW('ah', '#0D47A1')}${ARW('ahr', '#C2362F')}${ARW('ahg', '#C9D4E3')}</defs></svg>
<div id="viewport"><div id="stage">
${slidesHtml}
</div></div>
<nav class="ctl" aria-label="Πλοήγηση διαφανειών"><button type="button" id="bPrev" aria-label="Προηγούμενη διαφάνεια">‹</button><button type="button" id="bNext" aria-label="Επόμενη διαφάνεια">›</button><button type="button" id="bNotes" title="Σημειώσεις ομιλητή (N)">Σημειώσεις</button><button type="button" id="bHelp" title="Πλήκτρα (?)">?</button></nav>
<div id="progress" aria-hidden="true"><i></i></div>
<div id="help" hidden><div><h3>Πλήκτρα</h3><dl><div><dt>← →, Space</dt><dd>προηγούμενη, επόμενη διαφάνεια</dd></div><div><dt>N</dt><dd>παράθυρο σημειώσεων ομιλητή με ρολόι, ρυθμό και πλάνο</dd></div><div><dt>T</dt><dd>έναρξη ή παύση χρονομέτρου</dd></div><div><dt>F</dt><dd>πλήρης οθόνη</dd></div><div><dt>P</dt><dd>εκτύπωση ή αποθήκευση ως PDF, μία διαφάνεια ανά σελίδα</dd></div></dl><p>Άλλη ώρα έναρξης: προσθέστε <code>?start=15:15</code> στη διεύθυνση.</p></div></div>
<script>window.DECK = ${JSON.stringify({ meta: C.meta, slides: notesData })};</script><script>${js}</script></body></html>`);
console.log('wrote', outPath);
