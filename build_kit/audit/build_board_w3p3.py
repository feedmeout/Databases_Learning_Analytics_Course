"""python3 build_board_w3p3.py [out.html] -> review board for Week 3, Part 3 (+ content/w3p3_outline.md)"""
import os, sys, html
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from outline_w3p3 import OUTLINE, TITLE, AUDIT, DELIVER, SOURCES
e = html.escape; OUTF = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, '..', 'out', 'W3P3_review_board.html')
nS = sum(len(b[1]) for b in OUTLINE); nM = sum(s[0] for b in OUTLINE for s in b[1]); assert nM == 45, nM
COL = ['#0D47A1', '#7A3FB0', '#12233F', '#2E9E5B', '#B5541A', '#C9D4E3']
H = [f'''<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title>Week 3, Part 3: review board</title><style>
body{{font:16px/1.5 "Segoe UI",Arial,sans-serif;color:#12233F;max-width:1180px;margin:28px auto;padding:0 22px}}h1{{font-size:28px;margin:0 0 4px}}h2{{font-size:20px;margin:34px 0 10px;border-bottom:3px solid #F2A413;padding-bottom:4px}}
.sub{{color:#55657C}}table{{border-collapse:collapse;width:100%;margin:8px 0}}td,th{{border-bottom:1px solid #D3DDEB;padding:7px 9px;text-align:left;vertical-align:top;font-size:15px}}th{{background:#EEF3FA}}
.run{{display:flex;height:44px;border-radius:10px;overflow:hidden;margin:10px 0}}.run div{{display:grid;place-items:center;color:#fff;font-weight:700;font-size:13px;text-align:center;line-height:1.1}}
.box{{background:#FFF4DA;border-radius:12px;padding:12px 18px;margin:12px 0}}.k{{background:#EEF3FA;border-radius:12px;padding:12px 18px;margin:12px 0}}
.skip,.tm,.l1{{border-radius:999px;padding:0 8px;font-size:12px;font-weight:700;white-space:nowrap}}.skip{{background:#F2A413}}.tm{{background:#2E9E5B;color:#fff}}.l1{{background:#0D47A1;color:#fff}}
.a{{display:inline-block;border-radius:999px;padding:0 9px;font-size:12px;font-weight:700;color:#fff}}.CUT{{background:#D8433B}}.KEEP,.USE,.OPENED{{background:#2E9E5B}}.UPDATE,.REBUILD,.MERGE{{background:#0D47A1}}.TODO{{background:#B5541A}}.ASK{{background:#7A3FB0}}
.sec td{{background:#12233F;color:#fff;font-weight:700}}.n{{color:#55657C;width:34px}}.m{{width:44px;font-weight:700}}</style></head><body>
<h1>Week 3, Part 3 · review board</h1><p class="sub">{e(TITLE)} · 20:15–21:00 · {nS} slides · {nM} minutes (42 + 3 of slack on the end slide). Audit and outline only; nothing is built. Awaiting your approval.</p>
<div class="box"><b>Where Week 3 stands.</b> Parts 1 and 2: FINAL and delivered (you have them as LA_Week3_package_PARTS_1_and_2.zip). Part 3: this plan, waiting for your approval; nothing built. When Part 3 is built, Week 3 is complete and you get the full LA_Week3_package.zip. <b>I need no file from you</b>: your two PowerPoints and their pictures are in the kit.</div>
<h2>1 · Source material for this part</h2><table><tr><th style="width:26%">Item</th><th style="width:7%">Decision</th><th>What I found</th><th style="width:30%">What happens</th></tr>''']
for it, act, found, fate in AUDIT: H.append(f'<tr><td><b>{e(it)}</b></td><td><span class="a {act}">{act}</span></td><td>{e(found)}</td><td>{e(fate)}</td></tr>')
H.append('</table><h2>2 · The 45 minutes</h2><div class="run">')
for i, (sec, sl) in enumerate(OUTLINE):
    m = sum(s[0] for s in sl); H.append(f'<div style="flex:{m};background:{COL[i]};{"color:#12233F" if i == len(OUTLINE) - 1 else ""}">{e(sec)}<br>{m}′</div>')
H.append('</div><p class="sub">Frontiers 15′ (slides 1-12), workshop 30′ (slides 13-25). Skippable: 6 and 21. The workshop runs like Workshop 1: one team of about four per Zoom room, one product per room, timers on the slides, two broadcast messages, a report-back that does not depend on the answers. No new slide type is planned; your architecture figure and simulator screenshot use the existing image layouts.</p>')
H.append('<h2>3 · Outline, one line per slide</h2><table><tr><th class="n">#</th><th class="m">min</th><th style="width:24%">Title on the slide</th><th>What is on it</th><th style="width:22%">Source</th></tr>')
i = 0; md = [f'# Week 3, Part 3 outline (v1): {TITLE}', '']
for sec, sl in OUTLINE:
    H.append(f'<tr class="sec"><td colspan="5">{e(sec)} · {sum(s[0] for s in sl)}′</td></tr>'); md.append(f'\n## {sec}')
    for mins, flag, title, what, src in sl:
        i += 1; tag = {'SKIP': ' <span class="skip">skippable</span>', 'TIMER': ' <span class="tm">timer</span>', 'YOURS': ' <span class="l1">your material</span>'}.get(flag, '')
        H.append(f'<tr><td class="n">{i}</td><td class="m">{mins}′</td><td><b>{e(title)}</b>{tag}</td><td>{e(what)}</td><td class="sub">{e(src)}</td></tr>')
        md.append(f'{i}. ({mins}′{", " + flag if flag else ""}) **{title}**: {what}' + (f' _[{src}]_' if src else ''))
H.append('</table><h2>4 · What you get when this part is built</h2><ul>' + ''.join(f'<li>{e(x)}</li>' for x in DELIVER) + '</ul>')
H.append('<h2>5 · Sources</h2><table><tr><th style="width:42%">Source</th><th style="width:9%">Status</th><th>What I actually read</th></tr>')
LAB = {'OPENED': 'opened', 'TODO': 'at build', 'ASK': 'your answer'}
for s, what, st in SOURCES: H.append(f'<tr><td>{e(s)}</td><td><span class="a {st}">{LAB[st]}</span></td><td>{e(what)}</td></tr>')
H.append('''</table><h2>6 · One question</h2><div class="box"><b>Which publication stands behind your VR robotics slides (7.12-7.14)?</b> My candidate is Antonelli, Christopoulos, Laakso et al. (2023), Education Sciences 13(5), 528. <b>My default:</b> I cite that paper for the laboratory (slide 8) and present the three findings (slide 10) as «αποτελέσματα της αξιολόγησης του εργαστηρίου» with the same citation only if I find them in its full text; if I do not find them there, slide 10 carries no citation and says «αδημοσίευτα αποτελέσματα του διδάσκοντος». Tell me the right paper if it is another one.</div></body></html>''')
os.makedirs(os.path.dirname(OUTF), exist_ok=True); open(OUTF, 'w', encoding='utf8').write('\n'.join(H))
open(os.path.join(HERE, '..', 'content', 'w3p3_outline.md'), 'w', encoding='utf8').write('\n'.join(md) + '\n')
print('slides', nS, 'minutes', nM, '| skippable', [k + 1 for k, s in enumerate(s for b in OUTLINE for s in b[1]) if s[1] == 'SKIP'], '| timers', [k + 1 for k, s in enumerate(s for b in OUTLINE for s in b[1]) if s[1] == 'TIMER'])
