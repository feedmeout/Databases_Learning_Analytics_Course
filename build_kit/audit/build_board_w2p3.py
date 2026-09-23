import os, sys, html, base64
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from outline_w2p3 import OUTLINE, TITLE
e = html.escape
nS = sum(len(b[1]) for b in OUTLINE); nM = sum(s[0] for b in OUTLINE for s in b[1])
img = base64.b64encode(open(os.path.join(HERE, '..', 'out', 'board_7_15.jpg'), 'rb').read()).decode()
run = [('Dashboards', 15, '#0D47A1'), ('Briefing', 6, '#1565C0'), ('Teams of four at work', 14, '#2E9E5B'), ('Two teams report', 5, '#F2A413'), ('Close', 2, '#12233F'), ('Questions', 3, '#C9D4E3')]
audit = [
 ('7.15', 'KEEP', 'ViLLE chart collage from your robotics course, 1898 × 960 px, sharp.', 'Shown whole, with three native numbered markers, then used for the one timed question of the part: «ποια απόφαση στηρίζει κάθε γράφημα;». It is your own material and the only authentic dashboard specimen available to me.'),
 ('9.10', 'REBUILD', 'Chart chooser, 770 × 720 px, third-party redraw.', 'Rebuilt natively as «από το ερώτημα στο γράφημα» with Learning Analytics questions in the four branches. Credit verified: Andrew V. Abela, "Chart Suggestions: A Thought-Starter", 2006 (Extreme Presentation). The notes mention that Stephen Few criticised it as too simple: a thought-starter, not a rule.'),
 ('3.26', 'MERGE', 'Chart-types poster, 480 × 460 px (66 px per inch).', 'Same idea as 9.10 and far too small to show. Its content lives in the native chooser slide.'),
 ('2.7', 'REBUILD', 'Visualisation taxonomy: five families, 34 words, four 192-px icons.', 'Turned towards tonight: each Part 1 method gets its natural picture (transition matrix → heatmap, network → node-link, clusters → scatter, sequences → timeline). Skippable.'),
 ('3.27, 3.28', 'CUT', 'Two collages of third-party tool screenshots («Περιγραφικά εργαλεία», «Προγνωστικά εργαλεία»), 980 and 1002 px wide for several screenshots each.', 'Each screenshot inside them is a few hundred pixels wide and none carries a credit. The descriptive/predictive distinction survives natively (slide 9). These two images were in the Week 1 chat, not in this one: if you want any of them used, upload deck 3 and tell me which.'),
 ('5.5', 'REBUILD', 'Your 119-word «Αναζήτηση βιβλιογραφίας» slide (databases, Boolean operators, criteria, keeping a record).', 'Week 1, Part 3 already used the overview. What is left is the doing: it becomes the workshop.'),
]
ev = [
 ('Kaliisa, Misiejuk, López-Pernas, Khalil & Saqr (2024), LAK \'24, pp. 295–304', 'Full text (arXiv 2312.15042): method, PRISMA figure, all four results tables.', '38 studies; achievement effects 41.2% negligible + 35.3% small = 76.5%; medium to large effects on participation; users-against-non-users confounding; their search: (widget* OR dashboard*) AND ("learning analytics" OR "educational data mining" OR "educational datamining"), four databases, 485 + 153 + 88 + 86 = 812 records.'),
 ('Kaliisa, Jivet & Prinsloo (2023), IJETHE 20:28', 'Full text (open access).', '50 teacher-facing dashboards: 33 aim at awareness, 38 at action but 16 of those are vague; 5 name a theory; 19 prototypes, 23 pilots, 6 in classroom use; 33 evaluated at reaction level; one experimental study on student outcomes; one treats privacy as a design requirement.'),
 ('Matcha, Uzir, Gašević & Pardo (2020), IEEE TLT 13(2), 226–245', 'Abstract; the count (29 studies) through Kaliisa, Jivet & Prinsloo (2023).', 'Dashboards rarely grounded in learning theory; evaluation weak. One line on a slide, no number of my own.'),
 ('Schwendimann et al. (2017), IEEE TLT 10(1), 30–41', 'Definition as quoted, with page, in Kaliisa et al. (2024).', 'The definition slide.'),
 ('Abela (2006), Chart Suggestions: A Thought-Starter', 'Several independent attributions, including the original blog post date and Few\'s critique.', 'Credit line of the chooser slide.'),
 ('Rethlefsen et al. (2021), PRISMA-S, Systematic Reviews 10:39', 'Checklist table (16 items).', 'Items 1, 8, 9, 13, 15 are exactly the columns of your search log: database and platform, strategy copied as run, limits, date, records per database.'),
 ('McGowan et al. (2016), PRESS 2015, J Clin Epidemiol 75, 40–46', 'Abstract, checklist table, recommendation text.', 'The four checks the class applies when two pairs show their string (adapted from the six PRESS elements; subject headings left out).'),
 ('Scopus support centre (Elsevier)', 'Help pages on advanced search.', 'Order of precedence OR → W/n, PRE/n → AND → AND NOT; double quotes = loose phrase, braces = exact phrase; straight quotes only, curly quotes fail; * and ? wildcards.'),
 ('ERIC (eric.ed.gov) and its public API', 'I ran the searches myself today.', 'Truncation works on single words (dashboard* finds more than dashboard), fails inside quotes and after a hyphen: "self-regulat*" returns nothing. pubyearmin: works on the website.'),
]
H = [f'''<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title>Week 2, Part 3: review board</title><style>
body{{font:16px/1.5 "Segoe UI",Arial,sans-serif;color:#12233F;max-width:1180px;margin:28px auto;padding:0 22px}}h1{{font-size:28px;margin:0 0 4px}}h2{{font-size:20px;margin:34px 0 10px;border-bottom:3px solid #F2A413;padding-bottom:4px}}
.sub{{color:#55657C}}table{{border-collapse:collapse;width:100%;margin:8px 0}}td,th{{border-bottom:1px solid #D3DDEB;padding:7px 9px;text-align:left;vertical-align:top;font-size:15px}}th{{background:#EEF3FA}}
.run{{display:flex;height:44px;border-radius:10px;overflow:hidden;margin:10px 0}}.run div{{display:grid;place-items:center;color:#fff;font-weight:700;font-size:14px}}
.box{{background:#FFF4DA;border-radius:12px;padding:12px 18px;margin:12px 0}}.k{{background:#EEF3FA;border-radius:12px;padding:12px 18px;margin:12px 0}}.skip{{background:#F2A413;border-radius:999px;padding:0 8px;font-size:12px;font-weight:700}}.tm{{background:#2E9E5B;color:#fff;border-radius:999px;padding:0 8px;font-size:12px;font-weight:700}}
.a{{display:inline-block;border-radius:999px;padding:0 9px;font-size:12px;font-weight:700;color:#fff}}.KEEP{{background:#2E9E5B}}.REBUILD{{background:#0D47A1}}.MERGE{{background:#55657C}}.CUT{{background:#D8433B}}
code{{background:#EEF3FA;padding:1px 5px;border-radius:4px;font-size:14px}}img{{max-width:100%;border-radius:10px;border:1px solid #D3DDEB}}.two{{display:grid;grid-template-columns:1fr 1fr;gap:22px;align-items:start}}</style></head><body>
<h1>Week 2, Part 3 · review board</h1><p class="sub">{e(TITLE)} · 20:15–21:00. Audit and outline only; nothing is built. Awaiting your approval.</p>
<h2>1. The 45 minutes</h2><div class="run">''' + ''.join(f'<div style="flex:{m};background:{c};color:{"#12233F" if c in ("#F2A413", "#C9D4E3") else "#fff"}">{e(l)} {m}′</div>' for l, m, c in run) + f'''</div>
<p>{nS} slides, {nM} minutes. Fifteen dashboard slides at one minute each, six briefing slides, then two timer slides that hold 19 minutes (teams at work 14:00; two teams report, 02:30 each), homework, «Να θυμάστε», and an end slide that carries the 3 minutes of slack. One timed question in the theory block (01:00). Skippable: 8 and 13.</p>
<h2>2. Audit of the source slides routed to this part</h2><table><tr><th>Slide</th><th>Action</th><th>What it is</th><th>Decision and reason</th></tr>''' +
 ''.join(f'<tr><td><b>{e(a)}</b></td><td><span class="a {b}">{b}</span></td><td>{e(c)}</td><td>{e(d)}</td></tr>' for a, b, c, d in audit) + f'''</table>
<div class="two"><div><img src="data:image/jpeg;base64,{img}" alt="ViLLE collage with three markers"></div><div class="k"><b>Slide 4 to 6, the specimen.</b> Your collage with three numbered charts: ① the KPI tiles (60% accuracy, 5 submissions per student, 00:34:35 per student, 107 active students), ② weekly activity, ③ time against score with a regression line. The question: which decision does each one support? The reading that follows: ① monitoring, ② pacing, ③ who needs help; and what none of them says, which is what to do next. That gap is exactly what the two reviews on slides 9 to 12 report at scale.</div></div>
<h2>3. Evidence verified for this part</h2><table><tr><th>Source</th><th>What I opened</th><th>What goes on slides</th></tr>''' +
 ''.join(f'<tr><td>{e(a)}</td><td>{e(b)}</td><td>{e(c)}</td></tr>' for a, b, c in ev) + '''</table>
<p class="sub">Not used because I could not open them: Susnjak et al. (2022) and Verbert et al. (2020). Nothing on the slides rests on them.</p>
<h2>4. The workshop: what makes it work in 25 minutes over Zoom</h2>
<div class="k"><b>A tool instead of typing syntax.</b> A new workbook sheet, <code>0_Συμβολοσειρά</code>: the pair types its concepts and synonyms in columns; the sheet assembles the string for Scopus, for ERIC and in a generic form, with straight quotes and parentheses in the right places. It uses only IF and &amp;, so it works in any Excel, in LibreOffice and in Google Sheets (pairs can edit together). The rest of the workbook is unchanged; whoever has started filling version 1 copies the one sheet across.</div>
<div class="k"><b>A real demonstration, not an invented one.</b> The Week 1 example string, run in ERIC block by block. Today's counts on eric.ed.gov: <code>"learning analytics"</code> 2.954 → <code>AND (dashboard* OR "visual analytics")</code> 235 → <code>AND ("self-regulated learning" OR "self-regulation" OR SRL)</code> 33. Below your Week 1 threshold of 40, so: broaden. And the trap is real: the Week 1 Scopus form <code>"self-regulat*"</code> returns nothing in ERIC, which is the slide «η ίδια συμβολοσειρά δεν τρέχει παντού». I will take the final counts on build day and put the search date in the notes and in the handout, not on the slide.</div>
<div class="k"><b>A published search as the model log.</b> Kaliisa et al. (2024) report everything your sheet 1 asks for: the string in two blocks, four databases, the date, the records per database (485, 153, 88, 86). It ties the dashboards block to the assignment in one slide.</div>
<div class="k"><b>Lab work in rooms of about four, one team per room, as in Lab 1.</b> The review assignment stays single or pair and is done at home. In class, each room works as one team on one search string: it picks the review topic of one member (the one whose trial search gave the most awkward count), builds the blocks and the string in the sheet, runs it, logs two runs and decides. Four people, four roles: shares the sheet, runs the database, keeps the log, checks against four checks adapted from PRESS. Automatic room assignment works, as in Lab 1. Trade-off, stated plainly: only one member\'s topic is done in class; everyone repeats the same steps for their own review before Week 3, which the Week 1 timeline requires anyway.</div>
<div class="k"><b>No Scopus from home?</b> ERIC is free and needs no login. The handout carries a verified syntax crib for Scopus, ERIC, IEEE Xplore and ACM Digital Library (the last two I will verify against their help pages during the build, as I did for the first two).</div>
<h2>5. Slide-by-slide outline</h2>''']
i = 0
for blk, slides in OUTLINE:
    H.append(f'<h3 style="margin:18px 0 4px">{e(blk)}</h3><table>')
    for m, fl, t, d in slides:
        i += 1; tag = ' <span class="skip">skippable</span>' if fl == 'SKIP' else (' <span class="tm">timer</span>' if fl == 'TIMER' else '')
        H.append(f'<tr><td style="width:34px"><b>{i}</b></td><td style="width:46px">{m}′</td><td style="width:330px"><b>{e(t)}</b>{tag}</td><td>{e(d)}</td></tr>')
    H.append('</table>')
H.append('''<h2>6. What you would receive</h2><table><tr><th>File</th><th>For</th><th>Content</th></tr>
<tr><td><b>W2P3.html</b> + <b>W2P3_student.pdf</b></td><td>you / students</td><td>26 slides, timers on 5, 22 and 23, speaker notes with the Zoom steps.</td></tr>
<tr><td><b>LA_review_templates_v2.xlsx</b></td><td>students</td><td>The Week 1 workbook plus the sheet «0_Συμβολοσειρά». Formulas recalculated and checked before delivery.</td></tr>
<tr><td><b>Workshop1_handout.pdf</b> (3 pages, Greek)</td><td>students</td><td>The steps of the 14 minutes; syntax crib for four databases; the worked ERIC example with its search date; the four checks; what is due before Week 3.</td></tr>
<tr><td><b>Workshop1_teacher.pdf</b> (2 pages, Greek)</td><td>you</td><td>Room set-up as in Lab 1, the two broadcast messages, which teams to pick for the share-out, the ten errors you will see and the one-line fix for each, what to do if Scopus is unreachable.</td></tr>
<tr><td><b>LA_build_kit_v6.zip</b></td><td>you</td><td>Engine, content and the new generators.</td></tr></table>
<h2>7. Decisions</h2><div class="box"><ol>
<li><b>26 slides, not 30 to 35:</b> agreed.</li>
<li><b>3.27 and 3.28 cut:</b> agreed.</li>
<li><b>Rooms:</b> lab teams of about four, one per room, one string per room; the assignment itself stays single or pair.</li></ol></div>
</body></html>''')
open('/mnt/user-data/outputs/W2P3_review_board.html', 'w', encoding='utf8').write(''.join(H))
md = [f'# Week 2, Part 3: {TITLE} (outline v1, awaiting approval)', '', f'{nS} slides, {nM} minutes. Timer slides: 5 (01:00), 22 (14:00), 23 (02:30 per pair). Skippable: 8 and 13.', '']
i = 0
for blk, slides in OUTLINE:
    md.append(f'## {blk}')
    for m, fl, t, d in slides:
        i += 1; md.append(f'{i}. ({m}′{", " + fl if fl else ""}) **{t}**: {d}')
    md.append('')
open('/mnt/user-data/outputs/W2P3_outline.md', 'w', encoding='utf8').write('\n'.join(md)); open(os.path.join(HERE, '..', 'content', 'w2p3_outline.md'), 'w', encoding='utf8').write('\n'.join(md))
print('board + outline written', nS, nM)
