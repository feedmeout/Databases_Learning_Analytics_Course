// Usage: node build_pptx.js content/w1p1.json out/W1P1.pptx
const fs = require('fs');
const pptxgen = require('pptxgenjs');
const [,, inPath, outPath] = process.argv;
const C = JSON.parse(fs.readFileSync(inPath, 'utf8'));
const N = C.slides.length;

const K = { ink: '12233F', paper: 'FFFFFF', mist: 'EEF3FA', blue: '1565C0', deep: '0D47A1', muted: '55657C',
  green: '2E9E5B', amber: 'F2A413', amberInk: '8A5A00', amberBg: 'FFF4DA', red: 'D8433B', redInk: 'A92C25', redBg: 'FCE9E7',
  ice: 'DCE7F7', fog: 'AFC3E2', keep: '1C3358', body: '33445E' };
const FONT = 'Calibri';
const pres = new pptxgen();
pres.layout = 'LAYOUT_16x9'; // 10 x 5.625 in
pres.title = C.meta.deckTitle; pres.author = 'Αθανάσιος Χριστόπουλος'; pres.lang = 'el-GR';

// ---- clock ----
const [sh, sm] = C.meta.start.split(':').map(Number); const start = sh * 60 + sm;
const hm = m => String(Math.floor(m / 60)).padStart(2, '0') + ':' + String(m % 60).padStart(2, '0');
const offs = []; { let a = 0; C.slides.forEach(s => { offs.push(a); a += s.mins; }); }

// ---- helpers ----
const T = (sl, text, o) => sl.addText(text, Object.assign({ fontFace: FONT, color: K.ink, margin: 0, isTextBox: true, valign: 'top', lang: 'el-GR' }, o));
const box = (sl, x, y, w, h, fill, extra) => sl.addShape(pres.shapes.ROUNDED_RECTANGLE, Object.assign({ x, y, w, h, fill: { color: fill }, line: { color: fill, width: 0 }, rectRadius: 0.09 }, extra || {}));
const dot = (sl, x, y, d, color) => sl.addShape(pres.shapes.OVAL, { x, y, w: d, h: d, fill: { color }, line: { color, width: 0 } });
// *x* -> blue bold, _x_ -> amber bold
function runs(str, base, onDark) {
  const out = []; const re = /\*([^*]+)\*|_([^_]+)_/g; let last = 0, m;
  while ((m = re.exec(str))) {
    if (m.index > last) out.push({ text: str.slice(last, m.index), options: Object.assign({}, base) });
    out.push({ text: m[1] || m[2], options: Object.assign({}, base, { bold: true, color: onDark ? 'FFFFFF' : (m[1] ? K.deep : K.amberInk) }) });
    last = re.lastIndex;
  }
  if (last < str.length) out.push({ text: str.slice(last), options: Object.assign({}, base) });
  return out;
}
function title(sl, s, o = {}) {
  const long = s.title.length > 44;
  T(sl, s.title, { x: 0.6, y: o.y || 0.42, w: 8.8, h: long ? 0.98 : 0.6, fontSize: o.size || (long ? 27 : 30), bold: true, valign: 'top', fit: 'shrink' });
  return (o.y || 0.42) + (long ? 1.08 : 0.78);
}
function kicker(sl, tone, text) { dot(sl, 0.6, 0.3, 0.15, K[tone]); T(sl, text, { x: 0.85, y: 0.26, w: 5, h: 0.24, fontSize: 13, bold: true }); }
function rail(sl, i, dark) {
  T(sl, C.meta.block, { x: 0.6, y: 5.27, w: 4, h: 0.2, fontSize: 9.5, color: dark ? '9FB2CE' : K.muted });
  T(sl, `${i + 1} / ${N}`, { x: 7.4, y: 5.27, w: 2, h: 0.2, fontSize: 9.5, color: dark ? '9FB2CE' : K.muted, align: 'right' });
}
const source = (sl, s) => s.src && T(sl, s.src, { x: 0.6, y: 4.98, w: 8.2, h: 0.22, fontSize: 9, color: K.muted });
function timerBadge(sl, sec, y) {
  box(sl, 7.05, y, 2.35, 1.75, K.amberBg);
  T(sl, sec + '″', { x: 7.05, y: y + 0.25, w: 2.35, h: 0.85, fontSize: 54, bold: true, align: 'center', valign: 'mid' });
  T(sl, 'χρονόμετρο', { x: 7.05, y: y + 1.15, w: 2.35, h: 0.3, fontSize: 12, color: K.amberInk, bold: true, align: 'center' });
}
function steps(sl, arr, y, w) {
  arr.forEach((t, k) => {
    dot(sl, 0.6, y + k * 0.72 + 0.02, 0.34, K.ink);
    T(sl, String(k + 1), { x: 0.6, y: y + k * 0.72 + 0.02, w: 0.34, h: 0.34, fontSize: 12, bold: true, color: 'FFFFFF', align: 'center', valign: 'mid' });
    T(sl, t, { x: 1.12, y: y + k * 0.72, w, h: 0.66, fontSize: 17.5, valign: 'top' });
  });
  return y + arr.length * 0.72;
}

const R = {
  title(sl, s) {
    sl.background = { color: K.ink };
    T(sl, C.meta.course, { x: 0.6, y: 0.5, w: 8.8, h: 0.3, fontSize: 13, color: K.fog });
    T(sl, s.title, { x: 0.6, y: 1.05, w: 8.8, h: 0.95, fontSize: 56, bold: true, color: 'FFFFFF', valign: 'mid' });
    T(sl, s.subtitle, { x: 0.6, y: 2.05, w: 8.8, h: 0.5, fontSize: 25, color: K.ice });
    let seed = 7; const rnd = () => (seed = (seed * 16807) % 2147483647) / 2147483647;
    for (let i = 0; i < 54; i++) {
      const h = 0.09 + rnd() * 0.44 * (0.45 + 0.55 * Math.sin((i / 54) * Math.PI));
      sl.addShape(pres.shapes.RECTANGLE, { x: 0.6 + i * 0.1375, y: 3.62 - h, w: 0.075, h, fill: { color: '3E5F94' }, line: { color: '3E5F94', width: 0 } });
    }
    [K.green, K.amber, K.red].forEach((c, k) => dot(sl, 8.2 + k * 0.42, 3.27, 0.34, c));
    T(sl, s.author, { x: 0.6, y: 4.2, w: 6, h: 0.32, fontSize: 16, bold: true, color: 'FFFFFF' });
    T(sl, s.affil, { x: 0.6, y: 4.53, w: 6.4, h: 0.26, fontSize: 12, color: 'C9D7EC' });
    T(sl, s.email, { x: 0.6, y: 4.79, w: 6, h: 0.26, fontSize: 12, color: 'C9D7EC' });
    T(sl, `${C.meta.block}, ${hm(start)}–${hm(start + 45)}`, { x: 5.4, y: 4.79, w: 4, h: 0.26, fontSize: 12, color: 'C9D7EC', align: 'right' });
  },
  plan(sl, s) {
    title(sl, s);
    s.rows.forEach((r, k) => {
      const y = 1.3 + k * 0.98, on = r.now, col = on ? 'FFFFFF' : K.ink;
      box(sl, 0.6, y, 8.8, 0.84, on ? K.deep : K.mist);
      T(sl, `${hm(start + 60 * k)}–${hm(start + 60 * k + 45)}`, { x: 0.85, y, w: 1.75, h: 0.84, fontSize: 17, bold: true, color: col, valign: 'mid' });
      T(sl, r.label, { x: 2.6, y, w: 1.05, h: 0.84, fontSize: 17, bold: true, color: col, valign: 'mid' });
      T(sl, r.text, { x: 3.65, y, w: 5.55, h: 0.84, fontSize: 16.5, color: col, valign: 'mid' });
    });
    T(sl, s.foot, { x: 0.6, y: 4.35, w: 8.8, h: 0.55, fontSize: 13, color: K.muted });
  },
  activity(sl, s) {
    kicker(sl, 'amber', `${s.kicker}, ${s.duration}`);
    let y = title(sl, s, { y: 0.62 }) + 0.1;
    if (s.prompt) {
      T(sl, s.prompt, { x: 0.6, y: y + 0.1, w: 6.1, h: 2.0, fontSize: 34, bold: true, valign: 'top' });
    } else {
      if (s.claim) { box(sl, 0.6, y, 6.15, 0.95, K.mist); T(sl, s.claim, { x: 0.8, y, w: 5.75, h: 0.95, fontSize: 15.5, valign: 'mid' }); y += 1.15; }
      y = steps(sl, s.steps, y, 5.6);
      if (s.hint && !s.hintHidden) T(sl, s.hint, { x: 0.6, y: y + 0.05, w: 6.1, h: 0.5, fontSize: 13, color: K.muted });
    }
    timerBadge(sl, s.timerSec, 1.6);
  },
  columns(sl, s) {
    const y0 = title(sl, s) + 0.05, w = (8.8 - 0.45) / 4;
    s.cols.forEach((c, k) => {
      const x = 0.6 + k * (w + 0.15), on = c.focus;
      box(sl, x, y0, w, 2.3, on ? K.deep : K.mist);
      T(sl, c.h, { x: x + 0.18, y: y0 + 0.2, w: w - 0.36, h: 0.62, fontSize: 16.5, bold: true, color: on ? 'FFFFFF' : K.ink });
      T(sl, c.t, { x: x + 0.18, y: y0 + 0.85, w: w - 0.36, h: 1.35, fontSize: 14, color: on ? K.ice : K.body });
    });
    T(sl, s.foot, { x: 0.6, y: y0 + 2.55, w: 8.8, h: 0.75, fontSize: 17, bold: false });
  },
  definition(sl, s) {
    const y0 = title(sl, s);
    T(sl, runs(s.quote, { fontSize: 22, color: K.ink, fontFace: FONT }), { x: 0.6, y: y0, w: 8.8, h: 1.75, valign: 'top', lineSpacingMultiple: 1.08 });
    T(sl, s.src, { x: 0.6, y: y0 + 1.78, w: 8.8, h: 0.25, fontSize: 11, color: K.muted });
    s.callouts.forEach((c, k) => {
      const x = 0.6 + k * 4.475, am = c.tone === 'amber';
      box(sl, x, 3.6, 4.325, 1.2, am ? K.amberBg : K.mist);
      T(sl, c.h, { x: x + 0.22, y: 3.72, w: 3.9, h: 0.3, fontSize: 15, bold: true, color: am ? K.amberInk : K.deep });
      T(sl, c.t, { x: x + 0.22, y: 4.04, w: 3.9, h: 0.7, fontSize: 13.5 });
    });
  },
  cycle(sl, s) {
    const y0 = title(sl, s) + 0.1, nw = 1.8, nh = 0.85, xL = 0.6, xR = 3.5, yT = y0, yB = y0 + 2.2;
    const node = (x, y, t, weak) => {
      sl.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w: nw, h: nh, rectRadius: 0.1, fill: { color: weak ? 'FFFFFF' : K.deep }, line: { color: weak ? K.red : K.deep, width: weak ? 2.25 : 0 } });
      T(sl, t, { x: x + 0.08, y, w: nw - 0.16, h: nh, fontSize: 14.5, bold: true, color: weak ? K.redInk : 'FFFFFF', align: 'center', valign: 'mid' });
    };
    node(xL, yT, s.nodes[0]); node(xR, yT, s.nodes[1]); node(xR, yB, s.nodes[2]); node(xL, yB, s.nodes[3], true);
    const ln = (o, red) => sl.addShape(pres.shapes.LINE, Object.assign({ line: Object.assign({ color: red ? 'C2362F' : K.deep, width: 2.5 }, red ? { dashType: 'dash' } : {}, o.arrow) }, o.geo));
    ln({ geo: { x: xL + nw + 0.06, y: yT + nh / 2, w: xR - xL - nw - 0.12, h: 0 }, arrow: { endArrowType: 'triangle' } });
    ln({ geo: { x: xR + nw / 2, y: yT + nh + 0.06, w: 0, h: yB - yT - nh - 0.12 }, arrow: { endArrowType: 'triangle' } });
    ln({ geo: { x: xL + nw + 0.06, y: yB + nh / 2, w: xR - xL - nw - 0.12, h: 0 }, arrow: { beginArrowType: 'triangle' } });
    ln({ geo: { x: xL + nw / 2, y: yT + nh + 0.06, w: 0, h: yB - yT - nh - 0.12 }, arrow: { beginArrowType: 'triangle' } }, true);
    T(sl, s.weak, { x: xL + nw / 2 + 0.15, y: yT + nh + 0.4, w: 1.75, h: 0.55, fontSize: 12.5, bold: true, color: K.redInk });
    T(sl, s.sideH, { x: 5.75, y: yT, w: 3.65, h: 0.3, fontSize: 16, bold: true });
    T(sl, s.sideT, { x: 5.75, y: yT + 0.34, w: 3.65, h: 0.95, fontSize: 14 });
    box(sl, 5.75, yT + 1.5, 3.65, 1.45, K.mist);
    T(sl, s.stat, { x: 5.9, y: yT + 1.5, w: 1.3, h: 1.45, fontSize: 40, bold: true, color: K.deep, valign: 'mid' });
    T(sl, s.statT, { x: 7.15, y: yT + 1.58, w: 2.12, h: 1.3, fontSize: 11, valign: 'mid' });
    source(sl, s);
  },
  quad(sl, s) {
    const y0 = title(sl, s) + 0.02;
    s.quads.forEach((q, k) => {
      const x = 0.6 + (k % 2) * 4.475, y = y0 + Math.floor(k / 2) * 1.33;
      box(sl, x, y, 4.325, 1.2, K.mist);
      T(sl, q.q, { x: x + 0.2, y, w: 1.35, h: 1.2, fontSize: 32, bold: true, color: K.deep, valign: 'mid' });
      T(sl, q.h, { x: x + 1.55, y: y + 0.16, w: 2.65, h: 0.3, fontSize: 14.5, bold: true });
      T(sl, q.t, { x: x + 1.55, y: y + 0.47, w: 2.65, h: 0.68, fontSize: 12 , color: K.body });
    });
    T(sl, s.foot, { x: 0.6, y: y0 + 2.68, w: 8.8, h: 0.34, fontSize: 14, bold: true });
    source(sl, s);
  },
  stairs(sl, s) {
    title(sl, s); const w = (8.8 - 0.36) / 4, base = 4.45;
    const fills = ['DCE8F8', 'B5D0F2', '2A72C9', K.deep], hs = [1.75, 2.15, 2.55, 2.95];
    s.steps.forEach((st, k) => {
      const x = 0.6 + k * (w + 0.12), y = base - hs[k], lt = k > 1 ? 'FFFFFF' : K.ink;
      sl.addShape(pres.shapes.RECTANGLE, { x, y, w, h: hs[k], fill: { color: fills[k] }, line: { color: fills[k], width: 0 } });
      T(sl, st.h, { x: x + 0.15, y: y + 0.14, w: w - 0.3, h: 0.3, fontSize: 15, bold: true, color: lt });
      T(sl, st.q, { x: x + 0.15, y: y + 0.46, w: w - 0.3, h: 0.28, fontSize: 13, bold: true, color: lt });
      T(sl, st.t, { x: x + 0.15, y: y + 0.78, w: w - 0.3, h: 0.95, fontSize: 12, color: lt });
    });
    sl.addShape(pres.shapes.LINE, { x: 0.6, y: 4.72, w: 2.6, h: 0, line: { color: K.muted, width: 1.75, endArrowType: 'triangle' } });
    T(sl, s.axis, { x: 3.35, y: 4.6, w: 5, h: 0.25, fontSize: 12, color: K.muted });
    T(sl, s.foot, { x: 0.6, y: 4.98, w: 8.2, h: 0.22, fontSize: 9, color: K.muted });
  },
  signals(sl, s) {
    const y0 = title(sl, s) + 0.08;
    sl.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 0.6, y: y0, w: 1.3, h: 3.2, rectRadius: 0.3, fill: { color: K.ink }, line: { color: K.ink, width: 0 } });
    [K.red, K.amber, K.green].forEach((c, k) => dot(sl, 0.84, y0 + 0.22 + k * 0.96, 0.82, c));
    let y = y0;
    s.rows.forEach(r => {
      const h = r.t.length > 70 ? 0.72 : 0.45;
      T(sl, r.h, { x: 2.35, y, w: 1.35, h, fontSize: 15, bold: true, color: K.deep });
      T(sl, r.t, { x: 3.7, y, w: 5.7, h, fontSize: 14.5 }); y += h + 0.1;
    });
    box(sl, 2.35, y0 + 2.12, 7.05, 1.08, K.amberBg);
    T(sl, s.claim, { x: 2.57, y: y0 + 2.2, w: 6.6, h: 0.64, fontSize: 16.5, valign: 'mid' });
    T(sl, s.claimSrc, { x: 2.57, y: y0 + 2.86, w: 6.6, h: 0.24, fontSize: 10, color: K.muted });
    source(sl, s);
  },
  reveal(sl, s) {
    kicker(sl, 'red', s.kicker);
    const y0 = title(sl, s, { y: 0.62, size: 25 }) - 0.02;
    s.models.forEach((m, k) => {
      const y = y0 + k * 0.56, mu = m.tone === 'muted', col = mu ? '7C8AA0' : K.ink;
      T(sl, m.label, { x: 0.6, y, w: 2.05, h: 0.44, fontSize: 12.5, bold: true, color: col, valign: 'mid' });
      box(sl, 2.7, y, 2.25, 0.44, mu ? 'EEF1F5' : K.redBg);
      T(sl, m.a, { x: 2.8, y, w: 2.05, h: 0.44, fontSize: 12, color: col, valign: 'mid', strike: mu ? 'sngStrike' : undefined });
      sl.addShape(pres.shapes.LINE, { x: 5.03, y: y + 0.22, w: 0.4, h: 0, line: { color: mu ? '7C8AA0' : 'C2362F', width: 2.25, endArrowType: 'triangle' } });
      box(sl, 5.5, y, 3.9, 0.44, mu ? 'EEF1F5' : K.redBg);
      T(sl, m.b, { x: 5.6, y, w: 3.7, h: 0.44, fontSize: 12, color: col, valign: 'mid', strike: mu ? 'sngStrike' : undefined });
    });
    T(sl, s.points.map((p, k) => ({ text: p, options: { bullet: true, breakLine: k < s.points.length - 1, paraSpaceAfter: 5 } })),
      { x: 0.6, y: y0 + 1.22, w: 8.8, h: 1.42, fontSize: 12.5, valign: 'top' });
    box(sl, 0.6, 4.28, 8.8, 0.56, K.ink);
    T(sl, s.lesson, { x: 0.82, y: 4.28, w: 8.4, h: 0.56, fontSize: 13.5, bold: true, color: 'FFFFFF', valign: 'mid' });
    source(sl, s);
  },
  stats(sl, s) {
    const y0 = title(sl, s);
    s.stats.forEach((st, k) => {
      const x = 0.6 + k * 3.0;
      T(sl, st.n, { x, y: y0, w: 2.9, h: 0.95, fontSize: 56, bold: true, color: K.deep, valign: 'mid' });
      T(sl, st.t, { x, y: y0 + 0.98, w: 2.7, h: 0.75, fontSize: 13 });
    });
    T(sl, s.key, { x: 0.6, y: y0 + 1.95, w: 8.8, h: 0.75, fontSize: 19, bold: true });
    dot(sl, 0.6, y0 + 2.9, 0.15, K.red);
    T(sl, s.caveat, { x: 0.85, y: y0 + 2.84, w: 8.55, h: 0.55, fontSize: 12, color: K.body });
    source(sl, s);
  },
  three(sl, s) {
    const y0 = title(sl, s);
    T(sl, s.lead, { x: 0.6, y: y0, w: 8.8, h: 0.85, fontSize: 20 });
    s.items.forEach((it, k) => {
      const w = (8.8 - 0.3) / 3, x = 0.6 + k * (w + 0.15), y = y0 + 1.05;
      box(sl, x, y, w, 2.1, K.mist);
      T(sl, it.h, { x: x + 0.22, y: y + 0.2, w: w - 0.44, h: 0.6, fontSize: 17, bold: true });
      T(sl, it.t, { x: x + 0.22, y: y + 0.82, w: w - 0.44, h: 0.8, fontSize: 15 });
      T(sl, it.when, { x: x + 0.22, y: y + 1.68, w: w - 0.44, h: 0.28, fontSize: 12, bold: true, color: K.deep });
    });
  },
  roadmap(sl, s) {
    title(sl, s);
    s.thread.forEach((t, k) => {
      const x = 0.6 + k * 1.72;
      sl.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y: 1.15, w: 1.3, h: 0.36, rectRadius: 0.18, fill: { color: K.ink }, line: { color: K.ink, width: 0 } });
      T(sl, t, { x, y: 1.15, w: 1.3, h: 0.36, fontSize: 13, bold: true, color: 'FFFFFF', align: 'center', valign: 'mid' });
      if (k < 3) T(sl, '→', { x: x + 1.3, y: 1.15, w: 0.42, h: 0.36, fontSize: 14, color: K.muted, align: 'center', valign: 'mid' });
    });
    s.weeks.forEach((wk, r) => {
      const y = 1.72 + r * 0.84;
      T(sl, wk.w, { x: 0.6, y, w: 1.35, h: 0.74, fontSize: 13, bold: true, valign: 'mid' });
      wk.parts.forEach((p, c) => {
        const x = 2.0 + c * 2.5, here = r === 0 && c === 0, lab = /εργαστήριο/i.test(p);
        box(sl, x, y, 2.4, 0.74, here ? K.deep : (lab ? K.amberBg : K.mist));
        T(sl, p, { x: x + 0.13, y, w: 2.14, h: 0.74, fontSize: 11.5, bold: here, color: here ? 'FFFFFF' : K.ink, valign: 'mid' });
      });
    });
    T(sl, s.foot, { x: 0.6, y: 4.38, w: 8.8, h: 0.5, fontSize: 12.5, color: K.body });
  },
  break(sl, s) {
    sl.background = { color: K.ink };
    T(sl, s.title, { x: 0.6, y: 0.55, w: 8.8, h: 0.9, fontSize: 50, bold: true, color: 'FFFFFF', valign: 'mid' });
    T(sl, [{ text: 'Επιστρέφουμε στις ', options: { color: K.ice } }, { text: hm(start + 60), options: { bold: true, color: 'FFFFFF' } }], { x: 0.6, y: 1.5, w: 8.8, h: 0.6, fontSize: 28 });
    box(sl, 0.6, 2.55, 8.0, 1.5, K.keep);
    dot(sl, 0.85, 2.78, 0.15, K.green);
    T(sl, s.keepKicker, { x: 1.1, y: 2.74, w: 4, h: 0.24, fontSize: 13, bold: true, color: 'FFFFFF' });
    T(sl, s.keep, { x: 0.85, y: 3.08, w: 7.5, h: 0.85, fontSize: 18.5, color: 'FFFFFF' });
    T(sl, s.next, { x: 0.6, y: 4.35, w: 8.8, h: 0.3, fontSize: 14, color: K.fog });
  }
};

C.slides.forEach((s, i) => {
  const sl = pres.addSlide();
  const dark = s.type === 'title' || s.type === 'break';
  if (!dark) sl.background = { color: K.paper };
  R[s.type](sl, s);
  rail(sl, i, dark);
  let n = `⏱ ${hm(start + offs[i])} → ${hm(start + offs[i] + s.mins)}  (${s.mins}′)`;
  if (s.skippable) n += `\nΑΝ ΕΙΣΤΕ ΠΙΣΩ ΣΤΟΝ ΧΡΟΝΟ: αυτή η διαφάνεια παραλείπεται.`;
  n += '\n\n' + (s.notes || []).map(x => '• ' + x).join('\n');
  if (s.hintHidden && s.hint) n += `\n\n(Μόνο για εσάς, δεν φαίνεται στη διαφάνεια) ${s.hint}`;
  if (s.timerSec) n += `\n\nΧρονόμετρο ${s.timerSec}″: το PowerPoint δεν έχει ζωντανό χρονόμετρο. Χρησιμοποιήστε το κινητό ή μια εφαρμογή χρονομέτρου στο Zoom.`;
  if (i === 0) n += '\n\nΠΛΑΝΟ ΜΕΡΟΥΣ\n' + C.slides.map((x, j) => `${hm(start + offs[j])}  ${j + 1}. ${x.title}${x.skippable ? '  [παραλείπεται αν χρειαστεί]' : ''}`).join('\n');
  sl.addNotes(n);
});

pres.writeFile({ fileName: outPath }).then(f => console.log('wrote', f));
