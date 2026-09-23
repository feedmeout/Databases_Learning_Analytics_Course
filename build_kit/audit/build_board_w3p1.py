"""python3 build_board_w3p1.py [out.html]  -> review board for Week 3, Part 1 (+ content/w3p1_outline.md). No source-deck renders are needed for this part."""
import os, sys, html, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from outline_w3p1 import OUTLINE, TITLE, OLD, PROMISES, SOURCES
e = html.escape
OUTF = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, '..', 'out', 'W3P1_review_board.html')
N = json.load(open(os.path.join(HERE, '..', 'w3p1', 'lab1_numbers.json'), encoding='utf8'))
nS = sum(len(b[1]) for b in OUTLINE); nM = sum(s[0] for b in OUTLINE for s in b[1])
assert nM == 45, nM
COL = ['#12233F', '#0D47A1', '#D8433B', '#1565C0', '#7A3FB0', '#B5541A', '#2E9E5B', '#0B7A75', '#C9D4E3']
pc = lambda x: f'{100 * x:.0f}%'
H = [f'''<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title>Week 3, Part 1: review board</title><style>
body{{font:16px/1.5 "Segoe UI",Arial,sans-serif;color:#12233F;max-width:1180px;margin:28px auto;padding:0 22px}}h1{{font-size:28px;margin:0 0 4px}}h2{{font-size:20px;margin:34px 0 10px;border-bottom:3px solid #F2A413;padding-bottom:4px}}
.sub{{color:#55657C}}table{{border-collapse:collapse;width:100%;margin:8px 0}}td,th{{border-bottom:1px solid #D3DDEB;padding:7px 9px;text-align:left;vertical-align:top;font-size:15px}}th{{background:#EEF3FA}}
.run{{display:flex;height:44px;border-radius:10px;overflow:hidden;margin:10px 0}}.run div{{display:grid;place-items:center;color:#fff;font-weight:700;font-size:13px;text-align:center;line-height:1.1}}
.box{{background:#FFF4DA;border-radius:12px;padding:12px 18px;margin:12px 0}}.k{{background:#EEF3FA;border-radius:12px;padding:12px 18px;margin:12px 0}}
.skip{{background:#F2A413;border-radius:999px;padding:0 8px;font-size:12px;font-weight:700}}.tm{{background:#2E9E5B;color:#fff;border-radius:999px;padding:0 8px;font-size:12px;font-weight:700}}.l1{{background:#0D47A1;color:#fff;border-radius:999px;padding:0 8px;font-size:12px;font-weight:700}}.skip,.tm,.l1{{white-space:nowrap}}
.a{{display:inline-block;border-radius:999px;padding:0 9px;font-size:12px;font-weight:700;color:#fff}}.CUT{{background:#D8433B}}.MOVE{{background:#0D47A1}}.OPENED{{background:#2E9E5B}}.EARLIER{{background:#55657C}}.TODO{{background:#B5541A}}
.sec td{{background:#12233F;color:#fff;font-weight:700}}.n{{color:#55657C;width:34px}}.m{{width:44px;font-weight:700}}.num td{{text-align:right}}.num td:first-child,.num th:first-child{{text-align:left}}</style></head><body>
<h1>Week 3, Part 1 · review board</h1><p class="sub">{e(TITLE)} · 18:15–19:00 · {nS} slides · {nM} minutes (42 of content + 3 of slack on the break slide). Audit and outline only; nothing is built. Awaiting your approval.</p>
<div class="box"><b>Short answer to your question.</b> You are right: the old Week 3 material is obsolete, and the earlier chats had already reached that verdict for the practical (I had checked its CSV in the first chat: random noise). Two things survive. The systematic-review revision deck is the raw material of workshop 2 (Part 3). One slide of the Learning Analytics revision deck, your three types of intervention, enters Part 1. Part 1 itself has no source deck: it is written new, on the Lab 1 numbers your students already know and on 2020+ literature.</div>
<h2>1 · Your old Week 3 material, item by item</h2><table><tr><th style="width:24%">Item</th><th style="width:7%">Decision</th><th>What I found</th><th style="width:27%">What happens to it</th></tr>''']
for it, act, found, fate in OLD:
    H.append(f'<tr><td><b>{e(it)}</b></td><td><span class="a {act}">{act}</span></td><td>{e(found)}</td><td>{e(fate)}</td></tr>')
H.append('</table><h2>2 · What Weeks 1 and 2 promised, and the slide that pays it</h2><table><tr><th>Promise</th><th style="width:34%">Slide(s) of this part</th></tr>')
for p, s in PROMISES: H.append(f'<tr><td>{e(p)}</td><td>{e(s)}</td></tr>')
H.append('</table><h2>3 · The 45 minutes</h2><div class="run">')
for i, (sec, sl) in enumerate(OUTLINE):
    m = sum(s[0] for s in sl); H.append(f'<div style="flex:{m};background:{COL[i]};{"color:#12233F" if i == len(OUTLINE) - 1 else ""}">{e(sec)}<br>{m}′</div>')
H.append('</div><p class="sub">One timed question (slide 8, 60 s). Skippable: 14 and 19. No slide depends on what students answer. New slide type needed: a four-cell «people» matrix for slide 5 (class name checked for collisions at build); everything else uses existing types.</p>')
H.append('<h2>4 · Outline, one line per slide</h2><table><tr><th class="n">#</th><th class="m">min</th><th style="width:25%">Title on the slide</th><th>What is on it</th><th style="width:23%">Source</th></tr>')
i = 0; md = [f'# Week 3, Part 1 outline (v1): {TITLE}', '']
for sec, sl in OUTLINE:
    H.append(f'<tr class="sec"><td colspan="5">{e(sec)} · {sum(s[0] for s in sl)}′</td></tr>'); md.append(f'\n## {sec}')
    for mins, flag, title, what, src in sl:
        i += 1
        tag = {'SKIP': ' <span class="skip">skippable</span>', 'POLL': ' <span class="tm">timer 01:00</span>', 'LAB1': ' <span class="l1">Lab 1 numbers</span>'}.get(flag, '')
        H.append(f'<tr><td class="n">{i}</td><td class="m">{mins}′</td><td><b>{e(title)}</b>{tag}</td><td>{e(what)}</td><td class="sub">{e(src)}</td></tr>')
        md.append(f'{i}. ({mins}′{", " + flag if flag else ""}) **{title}**: {what}' + (f' _[{src}]_' if src else ''))
c = N['combined_this']; w = N['by_work_this']; t = N['top60_pES_this']; u = N['unranked_this']
H.append(f'''</table><h2>5 · The numbers Part 1 borrows from Lab 1</h2><p class="sub">Computed today from the two locked cohorts of Week 2 (<code>w3p1/lab1_numbers.py</code> → <code>lab1_numbers.json</code>); nothing was simulated again. They agree with the teacher screen of Week 2, Part 3 (298, 192, 98, 67).</p>
<table class="num"><tr><th>This year's cohort, 298 students</th><th>flagged</th><th>rightly</th><th>for nothing</th><th>missed</th><th>precision</th><th>recall</th></tr>
<tr><td>Combined rule: P(E→S) &lt; 0,35 or at most 2 sheets on time</td><td>{c["flagged"]}</td><td>{c["tp"]}</td><td>{c["fp"]}</td><td>{c["fn"]}</td><td>{pc(c["precision"])}</td><td>{pc(c["recall"])}</td></tr>''')
for k, v in N['sweep_pES_this'].items():
    H.append(f'<tr><td>P(E→S) below {k.replace(".", ",")}</td><td>{v["flagged"]}</td><td>{v["tp"]}</td><td>{v["fp"]}</td><td>{v["fn"]}</td><td>{pc(v["precision"])}</td><td>{pc(v["recall"])}</td></tr>')
H.append(f'<tr><td>Capacity: the 60 lowest P(E→S)</td><td>{t["flagged"]}</td><td>{t["tp"]}</td><td>{t["fp"]}</td><td>{t["fn"]}</td><td>{pc(t["precision"])}</td><td>{pc(t["recall"])}</td></tr></table>')
H.append(f'''<table class="num"><tr><th>Combined rule by subgroup</th><th>students</th><th>flagged</th><th>passed, yet flagged</th><th>did not pass, yet missed</th></tr>
<tr><td>Working students</td><td>{w["working"]["n"]}</td><td>{pc(w["working"]["flagged"] / w["working"]["n"])}</td><td>{w["working"]["fp"]} of {w["working"]["fp"] + w["working"]["tn"]} ({pc(w["working"]["fpr"])})</td><td>{w["working"]["fn"]} of {w["working"]["fn"] + w["working"]["tp"]} ({pc(w["working"]["fnr"])})</td></tr>
<tr><td>All others</td><td>{w["others"]["n"]}</td><td>{pc(w["others"]["flagged"] / w["others"]["n"])}</td><td>{w["others"]["fp"]} of {w["others"]["fp"] + w["others"]["tn"]} ({pc(w["others"]["fpr"])})</td><td>{w["others"]["fn"]} of {w["others"]["fn"] + w["others"]["tp"]} ({pc(w["others"]["fnr"])})</td></tr></table>
<p class="sub">Cannot be ranked at all (no P(E→S) value): {u["n"]} students, {u["not_passed"]} of whom will not pass; {pc(u["insuf_among_working"])} of working students against {pc(u["insuf_among_others"])} of the others.</p>''')
H.append('<h2>6 · Sources: what I opened</h2><table><tr><th style="width:40%">Source</th><th style="width:9%">Status</th><th>What I actually read today</th></tr>')
lab = {'OPENED': 'opened', 'EARLIER': 'Weeks 1-2', 'TODO': 'at build'}
for s, what, st in SOURCES: H.append(f'<tr><td>{e(s)}</td><td><span class="a {st}">{lab[st]}</span></td><td>{e(what)}</td></tr>')
H.append('''</table><div class="k"><b>How to read the table.</b> Green: every number and finding in the outline that comes from these sources is one I read on the page named, mostly abstracts; where a slide needs a table from inside a paper, I open the full text at build and say so. Orange: two primary documents that will replace secondary ones; no statement depends on them. Statements marked «own reasoning», «own synthesis» or «design rule» in the outline make no empirical claim. Mount St. Mary's (2016) was considered as a third case and left out: I did not verify it and two cases are enough.</div>
<h2>7 · One decision</h2><div class="box"><b>Do you want a revision element in Week 3?</b> The approved plan has no minutes for one, and your old revision deck revises a course that no longer exists. <b>My default:</b> no class time; when Week 3 is finished I add a two-page revision sheet to the package (give-to-students, after), assembled from the nine «Να θυμάστε» slides of the three weeks, so it revises exactly what was taught. If you say nothing, that is what I do.</div>
<h2>8 · For later parts</h2><div class="k">Decks 4, 6 and 7 did not arrive in this chat (the uploads were the kit and the old Week 3 files). Part 1 does not need them. The kit already holds their text and my slide-by-slide decisions, but not their images: for Part 2 I need <b>deck 4</b> (the cartoon, the teacher quote, the NYT still) and for Part 3 <b>decks 6 and 7</b> (your architecture figure 6.10 and the VR robotics slides 7.12-7.14). Upload the three .pptx files when you approve this outline or when Part 2 starts.</div></body></html>''')
os.makedirs(os.path.dirname(OUTF), exist_ok=True)
open(OUTF, 'w', encoding='utf8').write('\n'.join(H))
open(os.path.join(HERE, '..', 'content', 'w3p1_outline.md'), 'w', encoding='utf8').write('\n'.join(md) + '\n')
print('slides', nS, 'minutes', nM, '| skippable', sum(1 for b in OUTLINE for s in b[1] if s[1] == 'SKIP'), '| timed questions', sum(1 for b in OUTLINE for s in b[1] if s[1] == 'POLL'), '->', OUTF)
