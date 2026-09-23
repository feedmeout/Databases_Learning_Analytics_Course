"""python3 build_board_w3p2.py [out.html] -> review board for Week 3, Part 2 (+ content/w3p2_outline.md)"""
import os, sys, html
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from outline_w3p2 import OUTLINE, TITLE, AUDIT, PACK, SOURCES
e = html.escape; OUTF = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, '..', 'out', 'W3P2_review_board.html')
nS = sum(len(b[1]) for b in OUTLINE); nM = sum(s[0] for b in OUTLINE for s in b[1]); assert nM == 45, nM
COL = ['#12233F', '#2E9E5B', '#0D47A1', '#7A3FB0', '#B5541A', '#C9D4E3']
H = [f'''<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title>Week 3, Part 2: review board</title><style>
body{{font:16px/1.5 "Segoe UI",Arial,sans-serif;color:#12233F;max-width:1180px;margin:28px auto;padding:0 22px}}h1{{font-size:28px;margin:0 0 4px}}h2{{font-size:20px;margin:34px 0 10px;border-bottom:3px solid #F2A413;padding-bottom:4px}}
.sub{{color:#55657C}}table{{border-collapse:collapse;width:100%;margin:8px 0}}td,th{{border-bottom:1px solid #D3DDEB;padding:7px 9px;text-align:left;vertical-align:top;font-size:15px}}th{{background:#EEF3FA}}
.run{{display:flex;height:44px;border-radius:10px;overflow:hidden;margin:10px 0}}.run div{{display:grid;place-items:center;color:#fff;font-weight:700;font-size:13px;text-align:center;line-height:1.1}}
.box{{background:#FFF4DA;border-radius:12px;padding:12px 18px;margin:12px 0}}.k{{background:#EEF3FA;border-radius:12px;padding:12px 18px;margin:12px 0}}
.skip,.tm,.l1{{border-radius:999px;padding:0 8px;font-size:12px;font-weight:700;white-space:nowrap}}.skip{{background:#F2A413}}.tm{{background:#2E9E5B;color:#fff}}.l1{{background:#0D47A1;color:#fff}}
.a{{display:inline-block;border-radius:999px;padding:0 9px;font-size:12px;font-weight:700;color:#fff}}.CUT{{background:#D8433B}}.KEEP,.USE,.OPENED{{background:#2E9E5B}}.UPDATE{{background:#0D47A1}}.TODO{{background:#B5541A}}
.sec td{{background:#12233F;color:#fff;font-weight:700}}.n{{color:#55657C;width:34px}}.m{{width:44px;font-weight:700}}</style></head><body>
<h1>Week 3, Part 2 · review board</h1><p class="sub">{e(TITLE)} · 19:15–20:00 · {nS} slides · {nM} minutes (42 + 3 of slack on the break slide). Audit and outline only; nothing is built. Awaiting your approval.</p>
<div class="box"><b>Where Week 3 stands.</b> Part 1: FINAL and delivered. Part 2: this plan, waiting for your approval; nothing built. Part 3: not started. <b>I need no file from you for Part 2.</b> The real dataset is public and I have already downloaded and analysed it; the text of your seven ethics questions is in the kit.</div>
<h2>1 · Source material for this part</h2><table><tr><th style="width:26%">Item</th><th style="width:7%">Decision</th><th>What I found</th><th style="width:30%">What happens</th></tr>''']
for it, act, found, fate in AUDIT: H.append(f'<tr><td><b>{e(it)}</b></td><td><span class="a {act}">{act}</span></td><td>{e(found)}</td><td>{e(fate)}</td></tr>')
H.append('</table><h2>2 · The 45 minutes</h2><div class="run">')
for i, (sec, sl) in enumerate(OUTLINE):
    m = sum(s[0] for s in sl); H.append(f'<div style="flex:{m};background:{COL[i]};{"color:#12233F" if i == len(OUTLINE) - 1 else ""}">{e(sec)}<br>{m}′</div>')
H.append('</div><p class="sub">Same set-up as Lab 1: one team of about four per Zoom room, one product per room, a student pack with ready-made exhibits (no coding), a teacher key, timers on the slides, two broadcast messages, report-backs that do not depend on the answers, an optional Colab notebook for after class. Skippable: 11 and 21. No new slide type is needed: the seven questions use the existing definition layout (your question large, two boxes under it).</p>')
H.append('<h2>3 · Outline, one line per slide</h2><table><tr><th class="n">#</th><th class="m">min</th><th style="width:24%">Title on the slide</th><th>What is on it</th><th style="width:22%">Source</th></tr>')
i = 0; md = [f'# Week 3, Part 2 outline (v1): {TITLE}', '']
for sec, sl in OUTLINE:
    H.append(f'<tr class="sec"><td colspan="5">{e(sec)} · {sum(s[0] for s in sl)}′</td></tr>'); md.append(f'\n## {sec}')
    for mins, flag, title, what, src in sl:
        i += 1; tag = {'SKIP': ' <span class="skip">skippable</span>', 'TIMER': ' <span class="tm">timer</span>', 'REAL': ' <span class="l1">real data</span>'}.get(flag, '')
        H.append(f'<tr><td class="n">{i}</td><td class="m">{mins}′</td><td><b>{e(title)}</b>{tag}</td><td>{e(what)}</td><td class="sub">{e(src)}</td></tr>')
        md.append(f'{i}. ({mins}′{", " + flag if flag else ""}) **{title}**: {what}' + (f' _[{src}]_' if src else ''))
H.append('</table><h2>4 · The student pack (PDF, 8 pages), with numbers already computed from the real file</h2><table><tr><th style="width:5%">p.</th><th style="width:27%">Page</th><th>Content</th></tr>')
for p, t, c in PACK: H.append(f'<tr><td>{p}</td><td><b>{e(t)}</b></td><td>{e(c)}</td></tr>')
H.append('</table><p class="sub">Model: logistic regression on the variables known at the end of semester 1, trained on 80% of the students and judged on the other 20% (885 students, 284 dropouts), the split the authors recommend. Outcome for the lab: dropped out against did not. Script: <code>lab2/explore.py</code>. The numbers are final only after the build pipeline regenerates them from one locked file, as in Lab 1.</p>')
H.append('<h2>5 · Sources</h2><table><tr><th style="width:42%">Source</th><th style="width:9%">Status</th><th>What I actually read</th></tr>')
for s, what, st in SOURCES: H.append(f'<tr><td>{e(s)}</td><td><span class="a {st}">{"opened" if st == "OPENED" else "at build"}</span></td><td>{e(what)}</td></tr>')
H.append('''</table><div class="k"><b>What you get when this part is built:</b> the HTML deck, the student PDF of the deck, the student pack (PDF), the teacher key (PDF) with the two broadcast messages and the two data cautions, the data folder and the optional Colab notebooks (student and teacher), and the updated build kit.</div></body></html>''')
os.makedirs(os.path.dirname(OUTF), exist_ok=True); open(OUTF, 'w', encoding='utf8').write('\n'.join(H))
open(os.path.join(HERE, '..', 'content', 'w3p2_outline.md'), 'w', encoding='utf8').write('\n'.join(md) + '\n')
print('slides', nS, 'minutes', nM, '| skippable', [k + 1 for k, s in enumerate(s for b in OUTLINE for s in b[1]) if s[1] == 'SKIP'], '| timers', [k + 1 for k, s in enumerate(s for b in OUTLINE for s in b[1]) if s[1] == 'TIMER'])
