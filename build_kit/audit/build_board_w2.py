import json, base64, io, os, html, sys, collections
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from decisions_w2 import D2 as D
from outline_w2p1 import OUTLINE, SOURCES, TITLE
SRC = sys.argv[1] if len(sys.argv) > 1 else '/home/claude/src'          # folder with r/d6-01.jpg ... renders
OUTF = sys.argv[2] if len(sys.argv) > 2 else '/home/claude/kit/out/W2_review_board.html'
inv = json.load(open(os.path.join(HERE, 'inventory_w2.json'), encoding='utf8'))
DECKS = {6:'6. Τεχνολογίες Εμβύθισης', 7:'7. Ενδεικτικά Παραδείγματα', 8:'8. Πρακτικές Ασκήσεις', 9:'9. Βοηθητικό Υλικό'}
VERDICT = {
6:'Your immersive-technology framework, and the whole deck belongs to Week 3, Part 3 (frontiers), as the backbone says. The content is yours and publishable as it stands; the problems are layout (text boxes that overlap or run off the slide on 6.4 and 6.6) and three opening slides that tell a Week 3 audience what Learning Analytics is. Eight of ten slides survive, six of them rebuilt.',
7:'Two studies in one deck. Slides 2-11 are the novice-programmer work and they are the spine of Week 2, Part 1: the two-table device on 7.3 is the best motivating slide in the four decks. They need three things: the state names brought in line with what you published, citations on the slides, and a worked example between 7.6 and 7.7, because the deck jumps from four transitions to an 8x8 matrix in one step. Slides 12-15 are the VR robotics study; it is the applied example of deck 6 and travels with it to Week 3.',
8:'The live-coding practical on Kaggle with OULAD: the source of feedback point 6. All six slides go. Nothing here is needed for Lab 1, which has no accounts, no setup and no code during the session.',
9:'Ten third-party posters (Google Cloud sketchnotes, R / SQL / MLlib cheat sheets, the Azure algorithm chooser, a chart chooser), each stretched over a full slide at 78-100 px per inch, with no text and no notes. None can be read on Zoom and none can be studied alone. Two ideas survive as native slides: "question first, method second" (9.6, 9.8) in Part 1 and "question first, chart second" (9.10) in Part 3. If you want the posters available to students, the honest form is a one-page list of links in the Week 2 pack; say so and I will verify each link.'}
def thumb(d, n):
    for pat in (f'{SRC}/r/d{d}-{n:02d}.jpg', f'{SRC}/r/d{d}-{n}.jpg'):
        if os.path.exists(pat):
            im = Image.open(pat).convert('RGB'); im.thumbnail((340, 200)); b = io.BytesIO(); im.save(b, 'JPEG', quality=58)
            return 'data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode()
    return ''
e = html.escape
TITLES = {'7.7':'ΣΤΑΔΙΑ ΜΕΤΑΒΑΣΕΩΝ','7.8':'ΠΙΝΑΚΑΣ ΜΕΤΑΒΑΣΕΩΝ','7.13':'Data collection stages / Analytics (VR robotics study)','7.14':'Results (VR robotics study)','7.15':'Visualisations (VR robotics study)','8.2':'Πληροφορίες (OULAD, Kaggle)','8.3':'Βήμα #1: λογαριασμός στο Kaggle'}
rows = {d: [] for d in DECKS}
for k, (act, dest, note) in D.items():
    d, n = map(int, k.split('.')); a = inv[k]
    ttl = TITLES.get(k) or (a['texts'][0] if a['texts'] else '(image only)').replace('\x0b', ' ')[:70]
    meta = f"{a['words']} words, {len(a['pics'])} image{'s' if len(a['pics'])!=1 else ''}" + (', SmartArt' if a['smartart'] else '') + (', table' if a['tables'] else '')
    rows[d].append(f'''<tr class="a-{act}"><td class="th"><img loading="lazy" src="{thumb(d,n)}" alt="Slide {k}"></td>
<td><b>{k}</b> <span class="ttl">{e(ttl)}</span><div class="meta">{meta}</div></td>
<td><span class="badge b-{act}">{act}</span>{f'<div class="dest">{e(dest)}</div>' if dest else ''}</td><td class="note">{e(note)}</td></tr>''')
cnt = collections.Counter(v[0] for v in D.values())
assert len(D) == len(inv) == 42, (len(D), len(inv))
# outline table
orow, n, total = [], 0, 0
FLAG = {'SKIP':'<span class="badge b-UPDATE">skippable</span> ', 'POLL':'<span class="badge b-MERGE">60″ poll</span> ', 'FIG':'<span class="badge b-KEEP">your figure</span> ', '':''}
for sec, items in OUTLINE:
    orow.append(f'<tr class="sec"><td colspan="5">{e(sec)} ({len(items)} slides, {sum(i[0] for i in items)}′)</td></tr>')
    for mins, flag, t, what, src in items:
        n += 1; total += mins
        orow.append(f'<tr><td class="n">{n}</td><td class="n">{mins}′</td><td class="gt">{e(t)}</td><td>{FLAG[flag]}{e(what)}</td><td class="s">{e(src)}</td></tr>')
assert total == 45, total
srow = ''.join(f'<tr><td>{e(a)}</td><td><b>{e(b)}</b></td><td>{e(c)}</td></tr>' for a, b, c in SOURCES)
page = f'''<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Week 2 review board</title><style>
:root{{--ink:#12233F;--mist:#EEF3FA;--line:#D3DDEB;--muted:#55657C;--deep:#0D47A1}}
*{{box-sizing:border-box}}body{{margin:0;font:16px/1.5 "Segoe UI","Helvetica Neue",Arial,sans-serif;color:var(--ink);background:#fff}}
main{{max-width:1180px;margin:0 auto;padding:36px 24px 80px}}h1{{font-size:34px;line-height:1.15;margin:0 0 8px}}h2{{font-size:24px;margin:52px 0 6px}}
p.lead{{font-size:18px;max-width:74ch;color:#33445E}}nav{{position:sticky;top:0;background:#fff;border-bottom:1px solid var(--line);padding:10px 0;margin:18px 0 0;z-index:5;display:flex;gap:18px;flex-wrap:wrap;font-weight:600}}
nav a{{color:var(--deep);text-decoration:none}}nav a:hover{{text-decoration:underline}}
.counts{{display:flex;gap:10px;flex-wrap:wrap;margin:18px 0}}.counts span{{border-radius:999px;padding:6px 14px;font-weight:700;font-size:14px}}
table{{width:100%;border-collapse:collapse;margin-top:12px}}td{{padding:10px 12px;vertical-align:top;border-bottom:1px solid var(--line)}}
td.th{{width:190px}}td.th img{{width:170px;border:1px solid var(--line);border-radius:6px;display:block}}
.ttl{{font-weight:600}}.meta{{color:var(--muted);font-size:13px;margin-top:2px}}.dest{{font-size:13px;font-weight:700;margin-top:6px;color:var(--deep)}}.note{{max-width:56ch}}
.badge{{display:inline-block;border-radius:6px;padding:3px 10px;font-size:12px;font-weight:800;letter-spacing:.02em}}
.b-KEEP{{background:#DDF3E5;color:#14532D}}.b-REBUILD{{background:#DCE8F8;color:#0D47A1}}.b-UPDATE{{background:#FFF4DA;color:#7A4F00}}
.b-MERGE{{background:#E9E4F7;color:#47308A}}.b-MOVE{{background:#E3EEF0;color:#1F5560}}.b-CUT{{background:#FCE4E2;color:#8F2019}}
tr.a-CUT img{{opacity:.45}}.verdict{{background:var(--mist);border-radius:10px;padding:14px 18px;max-width:86ch}}
.out td.n{{width:40px;color:var(--muted);font-variant-numeric:tabular-nums;white-space:nowrap}}.out td.gt{{font-weight:600;width:27%}}.out td.s{{color:var(--muted);font-size:14px;width:23%}}
.out tr.sec td{{background:var(--ink);color:#fff;font-weight:700;padding:7px 12px}}.src td{{font-size:14px}}.src td:first-child{{width:46%}}.src td:nth-child(2){{width:22%}}
ul{{padding-left:20px;max-width:90ch}}li{{margin:5px 0}}@media(max-width:800px){{td.th{{width:120px}}td.th img{{width:104px}}}}</style></head><body><main>
<h1>Week 2 review board</h1>
<p class="lead">All 42 slides from decks 6-9, each with a decision and a reason. Veto anything by slide number. Below the decks: what I found in the images, the slide-by-slide outline for Week 2, Part 1, and the list of sources with what I actually opened.</p>
<div class="counts">{''.join(f'<span class="badge b-{k}">{k} {v}</span>' for k,v in cnt.most_common())}</div>
<nav>{''.join(f'<a href="#d{d}">Deck {d}</a>' for d in DECKS)}<a href="#img">Images</a><a href="#out">Part 1 outline</a><a href="#tm">Transition matrix</a><a href="#src">Sources</a></nav>
<p style="margin-top:18px;max-width:86ch"><b>Where the 42 slides go:</b> Week 2, Part 1 takes 7.2-7.11 plus the ideas of 9.6 and 9.8; Week 2, Part 3 takes 7.15 and 9.10; Week 3, Part 3 takes deck 6 and 7.12-7.14; decks 8 and 9 otherwise disappear. Already waiting in Week 2 from the Week 1 audit: your 3.23-3.25 and 2.6 (Part 1) and 2.7, 3.26-3.28 (Part 3).</p>
{''.join(f'<h2 id="d{d}">Deck {e(t)} <span style="color:var(--muted);font-weight:400;font-size:16px">({len(rows[d])} slides)</span></h2><p class="verdict">{e(VERDICT[d])}</p><table>{"".join(rows[d])}</table>' for d,t in DECKS.items())}
<h2 id="img">Images: what I found and what I will do</h2>
<ul><li><b>Reused as they are</b> (cropped from high-resolution renders of your slides, so that what you drew on top survives, such as the two dividing lines on 7.11, which are PowerPoint shapes and not part of the picture): the t-SNE plot (7.9), the k-means scatter with your dividing lines (7.11), the VR simulator screenshot (7.12), the ViLLE chart collage (7.15) and the system-architecture figure (6.10, 2937 px wide).</li>
<li><b>Rebuilt natively:</b> the three table screenshots of 7.3, the E / S pipeline (7.4), the Markov weather chain (7.5), the four-transition diagram (7.6), the state machine (7.7), the transition matrix (7.8), the framework cycle (6.7) and the two framework tables (6.8, 6.9).</li>
<li><b>Too small to show large:</b> the perceived-difficulty boxplot on 7.10 (392 px, 96 px per inch), the closing cartoon 7.16 (49 px per inch) and all ten posters of deck 9 (78-100 px per inch).</li>
<li><b>Third-party and uncredited:</b> the cartoons on 6.1, 7.1, 7.16 and 8.1, the "Barriers to Learning to Program" figure on 7.2, both Markov images on 7.5, the "Big Data" clip-art on 6.3 and every poster in deck 9. None is carried into Week 2, Part 1, so the allowance of two credited cartoons stays unspent for Parts 2-3.</li>
<li><b>Speaker notes:</b> only deck 6 has any, and they are image-source URLs and one footnote. There is no spoken text anywhere in the four decks; every rebuilt slide gets 2-3 timed notes.</li>
<li><b>Two English terms corrected against the taxonomy you translate:</b> "Pattern Recognition" becomes Structure Discovery and "Relationship extraction" becomes Relationship Mining. Your Greek terms stay exactly as they are.</li></ul>
<h2 id="out">Week 2, Part 1: «{e(TITLE)}», outline v1 ({n} slides, {total}′)</h2>
<p class="lead">One idea per slide; build-ups count as slides. 42′ of content plus 3′ of slack on the break slide. Two skippable slides (21 and 31) give back another 3′. One timed question (slide 25). Your own wording is marked "verbatim".</p>
<table class="out">{''.join(orow)}</table>
<h2 id="tm">The transition matrix: worked example or exercise?</h2>
<ul><li><b>My proposal: worked example on slides (23-24), checked by the one 60-second poll (25); the exercise itself lives in Lab 1.</b></li>
<li>An exercise inside Part 1 costs five minutes or more on Zoom, and the slides after it would have to wait for answers, which your rules exclude.</li>
<li>Your deck currently jumps from four transitions (7.6) to the 8x8 matrix (7.8). Two build slides with one short sequence close that gap in two minutes.</li>
<li>In Lab 1 the student pack already contains error / success sequences. It will include pre-computed transition matrices for groups of students, so reading a matrix becomes a task with a purpose (choosing week-4 indicators) instead of arithmetic for its own sake.</li></ul>
<h2 id="src">Sources for Part 1: what I opened and what I did not</h2>
<table class="src">{srow}</table>
<ul><li><b>Not verified yet, because they belong to later parts:</b> the publication behind your immersive-technology framework (deck 6), the publication behind the VR robotics study (7.12-7.15) and the credit for the chart chooser (9.10). I will open each before its part is outlined.</li>
<li>Slides 9, 14 and 17 are reading checklists and carry no empirical claim, so they carry no citation.</li></ul>
</main></body></html>'''
os.makedirs(os.path.dirname(OUTF), exist_ok=True)
open(OUTF, 'w', encoding='utf8').write(page)
print('wrote', OUTF, round(len(page)/1024), 'KB |', dict(cnt), '| outline', n, 'slides', total, 'min')
# markdown copy of the outline for the kit
md = [f'# Week 2, Part 1: {TITLE} (outline v1, awaiting approval)', '', '35 slides, 45′ = 42′ content + 3′ slack on the break slide. Skippable: 21 and 31 (3′). One timed question: slide 25 (60 s). "Verbatim" = your own wording from your decks.', '']
i = 0
for sec, items in OUTLINE:
    md.append(f'## {sec}')
    for mins, flag, t, what, src in items:
        i += 1; md.append(f"{i}. [{mins}′]{' ['+flag+']' if flag else ''} **{t}**: {what}" + (f' _Source: {src}_' if src else ''))
    md.append('')
md += ['## Transition matrix: worked example or exercise?', 'Proposal: worked example on slides 23-24, checked by the 60-second poll on slide 25; the exercise itself lives in Lab 1, where the pack gives pre-computed transition matrices that the groups must read in order to choose week-4 indicators.', '', '## Sources: what was opened']
md += [f'- {a} — **{b}**' + (f' — {c}' if c else '') for a, b, c in SOURCES]
open(os.path.join(HERE, '..', 'content', 'w2p1_outline.md'), 'w', encoding='utf8').write('\n'.join(md))
