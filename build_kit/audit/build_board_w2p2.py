import json, os, sys, html
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from outline_w2p2 import OUTLINE, TITLE
ST = json.load(open(os.path.join(HERE, '..', 'lab1', 'locked_stats.json'))); A = ST['last']; B = ST['this']
pc = lambda v: f'{round(100*v)}%'
def bars(vals, labels, title, color='#0D47A1', w=300, h=150, hi=None):
    n = len(vals); bw = (w-20)/n; o = [f'<svg viewBox="0 0 {w} {h+44}" width="{w}" role="img" aria-label="{html.escape(title)}"><text x="0" y="13" class="ct">{html.escape(title)}</text>']
    for i, v in enumerate(vals):
        bh = v*(h-30); x = 10+i*bw; c = (hi[i] if hi else color)
        o.append(f'<rect x="{x+4:.1f}" y="{h-bh+10:.1f}" width="{bw-8:.1f}" height="{bh:.1f}" rx="4" fill="{c}"/><text x="{x+bw/2:.1f}" y="{h-bh+4:.1f}" class="cv">{pc(v)}</text><text x="{x+bw/2:.1f}" y="{h+26:.1f}" class="cl">{html.escape(labels[i])}</text>')
    o.append(f'<line x1="6" y1="{h+10}" x2="{w-6}" y2="{h+10}" stroke="#9AA9BD"/></svg>'); return ''.join(o)
R = A['rules']; Rb = B['rules']
feat = [
 ('1', 'Availability check', 'Midterm grade (week 8)', 'Looks like the best predictor, but it does not exist at the end of week 4. First filter; an easy win for computer scientists who know target leakage.',
  bars([A['mid'][k][0] for k in ['absent','<5','5-6.5','>=7']], ['απών','<5','5–6,5','≥7'], 'Pass rate by midterm band'), 'Τεκμήριο 1–2'),
 ('2', 'Confounded proxy', 'eclass logins, weeks 1–4', f"Few logins: {pc(A['log_low'])} pass, against {pc(A['log_high'])}. Among first-time students the gap almost disappears ({pc(A['log_low_first'])} against {pc(A['log_high_first'])}). Logins mostly tell you who is re-registered for a failed course, which the registry already knows: the registry alone classifies {pc(R['repeat']['acc'])} correctly, the logins rule {pc(R['logins<=8']['acc'])}. In the process, logins depend on enrolment status and personal habit only.",
  bars([A['log_low'],A['log_high'],A['log_low_first'],A['log_high_first']], ['λίγες','πολλές','λίγες (1η εγγρ.)','πολλές (1η εγγρ.)'], 'Pass rate by logins: pooled, then first-time only', hi=['#D8433B','#0D47A1','#F2A413','#F2A413'], w=340), 'Τεκμήριο 3'),
 ('3', 'Reverse-causality trap (Course Signals pattern)', 'Lab sheets handed in over the whole semester', f"A dramatic dose-response ({pc(A['ls_0_3'])} / {pc(A['ls_4_8'])} / {pc(A['ls_9_12'])}) and a tempting proposal on the page: «να γίνουν οι ασκήσεις υποχρεωτικές». But students who leave stop handing in, so the count is a consequence of persisting. The same indicator on weeks 1–4 only is far weaker ({pc(A['l4_0_1'])} to {pc(A['l4_4'])}).",
  bars([A['ls_0_3'],A['ls_4_8'],A['ls_9_12']], ['0–3','4–8','9–12'], 'Pass rate by lab sheets, whole semester'), 'Τεκμήριο 4'),
 ('4', 'Frequency against sequence (your 7.3 argument)', 'Number of submissions, weeks 1–4', f"Inverted U: very few submissions means disengaged, very many means struggling. P(E→S) from the same submissions is monotonic ({pc(A['pes_lt25'])} / {pc(A['pes_25_40'])} / {pc(A['pes_40_55'])} / {pc(A['pes_ge55'])}).",
  bars([A['ns_0_15'],A['ns_16_40'],A['ns_41_80'],A['ns_81']], ['0–15','16–40','41–80','81+'], 'Pass rate by number of submissions', color='#55657C'), 'Τεκμήριο 5'),
 ('5', 'Valid indicator', 'P(E→S), weeks 1–4', f"Computed exactly as on Part 1 slides 23–24. Rule P(E→S) < 0,35: {pc(R['pES<.35']['prec'])} of the flagged students did not pass. Together with lab sheets on time: {pc(R['pES<.35|labs_w4<=2']['acc'])} correct last year and {pc(Rb['pES<.35|labs_w4<=2']['acc'])} on this year's cohort, close to the 70% that Veerasamy et al. report for week 4.",
  bars([A['pes_lt25'],A['pes_25_40'],A['pes_40_55'],A['pes_ge55']], ['<0,25','0,25–0,40','0,40–0,55','≥0,55'], 'Pass rate by P(E→S)', color='#2E9E5B'), 'Τεκμήριο 5'),
 ('6', 'Subgroup that is measured worse', 'Working students (22%)', f"They hand in half of their lab sheets after the weekly cut. P(E→S) cannot be computed for {pc(A['miss_work'])} of them ({pc(A['miss_nowork'])} of the rest), and «ασκήσεις εμπρόθεσμα ≤ 2» flags {pc(A['flag_l4_work'])} of them ({pc(A['flag_l4_nowork'])} of the rest), although they pass as often ({pc(A['pass_work'])} against {pc(A['pass_nowork'])}). This is the bridge to the fairness debrief of Week 3.",
  bars([A['flag_l4_nowork'],A['flag_l4_work'],1-A['pass_nowork'],1-A['pass_work']], ['σήμανση: λοιποί','σήμανση: εργαζ.','απέτυχαν: λοιποί','απέτυχαν: εργαζ.'], 'Flagged by the on-time rule, against who really did not pass', hi=['#0D47A1','#D8433B','#9AA9BD','#9AA9BD'], w=340), 'Τεκμήριο 6'),
]
cal = [('Students who sit the final exam', '65%', pc(A['attend']), 'Veerasamy, Laakso & D\'Souza (2022)'),
       ('Pass rate among those who sit it', '77%', pc(A['pass_sit']), 'same'),
       ('Did not pass (failed or did not attend)', '50%', pc(1-A['pass']), 'same, Table 3'),
       ('Rule accuracy at week 4', '70%', f"{pc(R['pES<.35']['acc'])} to {pc(R['pES<.35|labs_w4<=2']['acc'])}", 'same, Table 5'),
       ('Submissions that end in an error', '52% to 59%', pc(A['E_share']), 'Lokkila, Christopoulos & Laakso (2023), JISE, Table 3'),
       ('Activity count against grade, pooled', 'r = 0,28 with a prediction interval that crosses zero', f"r = {A['r_logins_pooled']:.2f} pooled, {A['r_logins_first']:.2f} among first-time students".replace('.',','), 'Saqr, Jovanović, Viberg & Gašević (2022), Table 2')]
pack = [('1','Εξώφυλλο','Scenario, task, time plan, and in the first lines: «Τα δεδομένα είναι προσομοιωμένα».'),
        ('2','Τεκμήριο 1: τα δεδομένα','Data dictionary: variable, source, the week in which it becomes available, coverage. Cohort sizes and base rates.'),
        ('3','Τεκμήριο 2: πόσο καλά ξεχωρίζει κάθε δείκτης','All six candidates ranked on last year\'s cohort. The naive reading puts the midterm and the semester lab count on top.'),
        ('4','Τεκμήριο 3: συνδέσεις στο eclass','Pass rate by logins, pooled and by enrolment status (πρώτη εγγραφή, επανεγγραφή).'),
        ('5','Τεκμήριο 4: εργαστηριακές ασκήσεις','Whole semester against weeks 1–4, the week of last activity of those who did not pass, and the «υποχρεωτικές ασκήσεις» proposal to judge.'),
        ('6','Τεκμήριο 5: πλήθος και αλληλουχία υποβολών','Pass rate by number of submissions and by P(E→S); average transition matrices for passed, failed, did not attend.'),
        ('7','Τεκμήριο 6: ο κανόνας ανά υποομάδα','Working and non-working students: coverage of P(E→S), share flagged by each rule, share that really did not pass.'),
        ('8','Φύλλο απάντησης','The three prompts and the 3′ report template.')]
run = [('Ενημέρωση',5,'#0D47A1'),('Ομάδες',17,'#F2A413'),('Αναφορές',9,'#2E9E5B'),('Αποκάλυψη',10,'#12233F'),('',1,'#55657C'),('Περιθώριο',3,'#C9D4E3')]
nS = sum(len(b[1]) for b in OUTLINE); nM = sum(s[0] for b in OUTLINE for s in b[1])
H = [f'''<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title>Lab 1 design board</title><style>
body{{font:16px/1.5 "Segoe UI",Arial,sans-serif;color:#12233F;max-width:1180px;margin:28px auto;padding:0 22px}}h1{{font-size:28px;margin:0 0 4px}}h2{{font-size:20px;margin:34px 0 10px;border-bottom:3px solid #F2A413;padding-bottom:4px}}
.sub{{color:#55657C}}table{{border-collapse:collapse;width:100%;margin:8px 0}}td,th{{border-bottom:1px solid #D3DDEB;padding:7px 9px;text-align:left;vertical-align:top;font-size:15px}}th{{background:#EEF3FA}}
.run{{display:flex;height:44px;border-radius:10px;overflow:hidden;margin:10px 0}}.run div{{display:grid;place-items:center;color:#fff;font-weight:700;font-size:14px}}
.f{{display:grid;grid-template-columns:1fr 350px;gap:22px;border:1px solid #D3DDEB;border-radius:12px;padding:14px 18px;margin:12px 0;align-items:center}}.f h3{{margin:0 0 4px;font-size:17px}}.tag{{display:inline-block;background:#12233F;color:#fff;border-radius:999px;padding:1px 10px;font-size:13px;margin-right:8px}}
.pg{{color:#8A5A00;font-weight:700;font-size:13px}}.ct{{font:700 12px "Segoe UI",Arial}}.cv{{font:700 12px "Segoe UI",Arial;text-anchor:middle}}.cl{{font:11px "Segoe UI",Arial;text-anchor:middle;fill:#55657C}}
.box{{background:#FFF4DA;border-radius:12px;padding:12px 18px;margin:12px 0}}.k{{background:#EEF3FA;border-radius:12px;padding:12px 18px}}.skip{{background:#F2A413;border-radius:999px;padding:0 8px;font-size:12px;font-weight:700}}.tm{{background:#2E9E5B;color:#fff;border-radius:999px;padding:0 8px;font-size:12px;font-weight:700}}
code{{background:#EEF3FA;padding:1px 5px;border-radius:4px}}</style></head><body>
<h1>Week 2, Part 2 · Group Lab 1: design board</h1><p class="sub">{html.escape(TITLE)}. Awaiting your approval; nothing below is built yet except the data generator, which I had to run to be sure the design works. Every number on this page comes from the two locked cohorts (n = {int(A['n'])} and n = {int(B['n'])}; {int(A['n_sub']):,} and {int(B['n_sub']):,} simulated submissions).</p>
<h2>1. What the students do</h2><p>A first-year programming course at a Greek university, about 300 registered students, roughly half do not pass. The teaching team wants to contact students at risk at the <b>end of week 4</b>. Each Zoom room gets an 8-page pack of ready-made tables and charts (no code) on last year's cohort and must decide which week-4 indicators it trusts. The report takes 3 minutes: up to two indicators they recommend, one they reject with the reason, and one group of students their rule may treat unfairly.</p>
<div class="run">''' + ''.join(f'<div style="flex:{m};background:{c};color:{"#12233F" if c in ("#F2A413","#C9D4E3") else "#fff"}">{(html.escape(l)+' '+str(m)+'′') if l else ''}</div>' for l,m,c in run) + '''</div>
<h2>2. The designed case: what is planted and what the students will see</h2>''']
for n_, kind, ind, txt, svg, where in feat:
    H.append(f'<div class="f"><div><h3><span class="tag">{n_}</span>{html.escape(kind)}: {html.escape(ind)}</h3><p style="margin:4px 0">{html.escape(txt)}</p><span class="pg">{where}</span></div><div>{svg}</div></div>')
H.append('<div class="box"><b>Two roads to not passing.</b> In the process, <i>skill</i> drives failing the exam and <i>commitment</i> drives not attending it. P(E→S) picks up the first road (AUC 0,85 for failing, 0,60 for not attending, large-sample values) and lab sheets on time pick up the second (0,55 and 0,73). That is why the best rule combines the two, and why the two groups need different interventions: the bridge to Week 3.</div>')
H.append('<h2>3. Calibration against the literature verified for Part 1</h2><table><tr><th>Quantity</th><th>Published</th><th>Lab 1, last year\'s cohort</th><th>Source</th></tr>' + ''.join(f'<tr><td>{html.escape(a)}</td><td>{html.escape(b)}</td><td>{html.escape(c)}</td><td>{html.escape(d)}</td></tr>' for a,b,c,d in cal) + '</table><p class="sub">The strength of the midterm and the size of the two subgroups are my design choices, not published values. The key will say so.</p>')
H.append('<h2>4. Student pack (PDF, 8 pages, Greek)</h2><table><tr><th>Page</th><th>Title</th><th>What is on it</th></tr>' + ''.join(f'<tr><td>{a}</td><td>{html.escape(b)}</td><td>{html.escape(c)}</td></tr>' for a,b,c in pack) + '</table>')
H.append(f'<h2>5. Deck outline: {nS} slides, {nM} minutes</h2><table><tr><th>#</th><th>min</th><th>Title</th><th>What is on it</th></tr>')
i = 0
for blk, slides in OUTLINE:
    H.append(f'<tr><th colspan="4">{html.escape(blk)}</th></tr>')
    for m, fl, t, d in slides:
        i += 1; badge = ' <span class="skip">skippable</span>' if fl == 'SKIP' else (' <span class="tm">timer</span>' if fl == 'TIMER' else '')
        H.append(f'<tr><td>{i}</td><td>{m}′</td><td><b>{html.escape(t)}</b>{badge}</td><td>{html.escape(d)}</td></tr>')
H.append('</table>')
H.append('''<h2>6. What you would receive</h2><div class="k"><ul>
<li><b>Deck</b> (HTML + student PDF), same engine, with a work slide (17:00 timer), a report slide (03:00 timer) and the reveal charts drawn natively from the data.</li>
<li><b>Student pack</b> (PDF, 8 pages) and the <b>answer sheet</b> as its last page.</li>
<li><b>Teacher key</b> (PDF): the process diagram with every parameter, what each exhibit is built to show, a strong answer, the usual wrong answers with one question to ask back, the performance of every possible rule on both cohorts (so you can answer whatever a group proposes), Zoom logistics and the two broadcast messages.</li>
<li><b>Data and generator</b>: CSV files for both cohorts (students see this year's cohort up to week 4 only) and <code>lab1/simulate.py</code> with fixed seeds.</li>
<li><b>Optional Colab notebook</b> (student and teacher versions) with the data embedded, so it runs without any hosting. "One click" needs a link: you put the file on your Drive or GitHub once and share that link.</li></ul></div>
<h2>7. Two points that need your decision</h2><div class="box"><ol>
<li><b>19 slides, not 30 to 35.</b> Three slides hold 29 of the 45 minutes (groups 17′, reports 9′, slack 3′). The other 16 minutes carry 16 slides at one minute each, which is your usual density.</li>
<li><b>The two subgroups.</b> Confounder: re-registered students (επανεγγραφή, 31% of the cohort, 27% pass against 55%). Worse-measured group: working students (εργαζόμενοι, 22%). Both are common in Greek first-year courses and neither is a protected characteristic. Tell me if you prefer others.</li></ol></div>
</body></html>''')
open('/mnt/user-data/outputs/W2P2_Lab1_design_board.html', 'w', encoding='utf8').write(''.join(H))
md = [f'# Week 2, Part 2: {TITLE} (outline v1, awaiting approval)', '', f'{nS} slides, {nM} minutes. Timer slides: 6 (17:00) and 7 (03:00 per group). Skippable: 15 and 17.', '']
i = 0
for blk, slides in OUTLINE:
    md.append(f'## {blk}')
    for m, fl, t, d in slides:
        i += 1; md.append(f'{i}. ({m}′{", " + fl if fl else ""}) **{t}**: {d}')
    md.append('')
open('/mnt/user-data/outputs/W2P2_outline.md', 'w', encoding='utf8').write('\n'.join(md)); open(os.path.join(HERE, '..', 'content', 'w2p2_outline.md'), 'w', encoding='utf8').write('\n'.join(md))
print('board + outline written', nS, nM)
