import json, base64, io, glob, os, html, sys
from PIL import Image
sys.path.insert(0,'.'); from decisions import D
inv = json.load(open('/home/claude/src/inventory.json', encoding='utf8'))
DECKS = {1:'1. Επισκόπηση',2:'2. Εισαγωγή',3:'3. Δεδομένα',4:'4. Θέματα Ηθικής',5:'5. Συστηματική Ανασκόπηση'}
VERDICT = {
1:'Administrative deck. The introductions round is the biggest hidden time cost of the evening. The assignment slide disagrees with the brief on grading and team size.',
2:'Nine slides of stock infographics carrying taxonomies. The definition and the five facets are good and stay; the algorithm list and the 2007-era tool list go.',
3:'The core deck, and the clearest picture of the density problem: 28 of 51 slides have under 12 words, 8 have over 70, median 4. Three slides are screenshots of text. The nine-slide tools tour goes. The ViLLE section (3.40-3.49) is your strongest material and is kept almost untouched.',
4:'Seven good questions spread over 21 slides by alternating each with a cartoon. The legal anchor is a 2014 report that predates GDPR and the AI Act. One 9.2 MB animation is 80% of the file.',
5:'Correct but abstract: two slides over 119 words, a PRISMA 2009 diagram, no worked example, no scope limits, no timeline. This is why the assignment does not feel doable.'}
def thumb(d, n):
    for pat in (f'/home/claude/src/r{d}/s-{n}.jpg', f'/home/claude/src/r{d}/s-{n:02d}.jpg', f'/home/claude/src/r{d}/s-{n:03d}.jpg'):
        if os.path.exists(pat):
            im = Image.open(pat).convert('RGB'); im.thumbnail((340, 200)); b = io.BytesIO(); im.save(b, 'JPEG', quality=58)
            return 'data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode()
    return ''
e = html.escape
rows = {d: [] for d in DECKS}
for k, (act, dest, note) in D.items():
    d, n = map(int, k.split('.')); a = inv[k]
    ttl = (a['texts'][0] if a['texts'] else '(image only)').replace('\x0b', ' ')[:70]
    meta = f"{a['words']} words, {len(a['pics'])} image{'s' if len(a['pics'])!=1 else ''}"
    rows[d].append(f'''<tr class="a-{act}"><td class="th"><img loading="lazy" src="{thumb(d,n)}" alt="Slide {k}"></td>
<td><b>{k}</b> <span class="ttl">{e(ttl)}</span><div class="meta">{meta}</div></td>
<td><span class="badge b-{act}">{act}</span>{f'<div class="dest">{e(dest)}</div>' if dest else ''}</td><td class="note">{e(note)}</td></tr>''')
import collections
cnt = collections.Counter(v[0] for v in D.values())
VOCAB = [('learning analytics','Μαθησιακή Αναλυτική'),('stakeholders','ενδιαφερόμενα μέρη'),('context / purpose','πλαίσιο / σκοπός'),('dashboards','Πίνακες Πληροφοριών (Dashboards)'),
('big educational data','μεγάλα εκπαιδευτικά δεδομένα'),('digital traces','ψηφιακά δεδομένα και ίχνη'),('descriptive / diagnostic','Περιγραφική / Διαγνωστική Αναλυτική'),('predictive / prescriptive','Προγνωστική / Καθοδηγητική Αναλυτική'),
('structure discovery','Εύρεση Δομών και Προτύπων'),('prediction','Πρόβλεψη'),('relationship mining','Εξόρυξη σχέσεων'),('misconceptions','λανθασμένες αντιλήψεις'),('automatic grading','αυτόματη βαθμολόγηση'),
('study habits','συνήθειες μελέτης'),('gamified exercises','παιχνιδοποιημένες ασκήσεις'),('inclusion / exclusion criteria','κριτήρια ένταξης / αποκλεισμού'),('systematic review','συστηματική βιβλιογραφική ανασκόπηση'),('intervention','παρέμβαση')]
LABELS = [('Takeaway','Να θυμάστε'),('Closing questions','Προβληματισμοί'),('Wrap-up','Σύνοψη / Συμπεράσματα'),('Short overview','Εν συντομία'),('Examples','Παραδείγματα'),('Challenges','Προκλήσεις'),('Timed question (replaces "Η σειρά σας")','Ερώτημα'),('Caution','Προσοχή'),('Objectives','Μαθησιακοί στόχοι')]
OUT = [
('Άνοιγμα',[('Μαθησιακή Αναλυτική: από τα ίχνη στις αποφάσεις','Title. Name and affiliation exactly as on your decks.',''),('Το πλάνο της βραδιάς','Three parts with clock times and breaks. The only place the part structure appears.',''),('Μαθησιακοί στόχοι','Your 1.4, rewritten to four lines for the new backbone.','')]),
('Γιατί τώρα; Τι είναι;',[('Κάθε κλικ καταγράφεται','One open dataset: 32.593 φοιτητές, ~10,6 εκατ. εγγραφές αλληλεπίδρασης. The same dataset returns in Weeks 2-3.','Kuzilek, Hlosta & Zdrahal (2017)'),('Ορισμός','Your translation, with the four verbs and the two purposes highlighted.','SoLAR (2011)'),('Συγγενικά πεδία: LA, EDM, Academic Analytics','One line each. Skippable.','Romero & Ventura (2020)')]),
('Τέσσερις ερωτήσεις (your 2.2 + 3.6)',[('Τι; Δεδομένα και περιβάλλοντα','Your Πλαίσιο: παραδοσιακή αίθουσα, διαδικτυακά, μικτά περιβάλλοντα.','Chatti et al. (2012), reference model'),('Ποιος; Ενδιαφερόμενα μέρη','Your list: φοιτητές, εκπαιδευτικοί, σχεδιαστές, ερευνητές, γονείς.',''),('Γιατί; Στόχοι','Your six goals from 3.6, rebuilt as text.',''),('Πώς; Μέθοδοι','One line only; the detail is Week 2.',''),('Ο πλήρης χάρτης','All four together. Returns in Part 3 as the reading grid for the assignment.','')]),
('Ο κύκλος (your 3.8, built step by step)',[('Εκπαιδευόμενοι → Δεδομένα','',''),('→ Μετρικές και αναλύσεις','',''),('→ Παρεμβάσεις','',''),('Ο κύκλος κλείνει, ή δεν κλείνει','Without the last arrow it is statistics, not LA.','Clow (2012)'),('Ο ίδιος κύκλος το 2024: πού μπαίνει η Παραγωγική ΤΝ','GenAI mapped onto each step of the same cycle.','Yan, Martinez-Maldonado & Gašević (2024), LAK \'24')]),
('Τύποι αναλυτικής (your 3.20-3.21)',[('Περιγραφική: «Τι πήγε στραβά; Τι πήγε καλά;»','Your guiding questions, verbatim.',''),('Διαγνωστική: «Γιατί συνέβη αυτό;»','',''),('Προγνωστική: «Τι να περιμένετε στο μέλλον;»','',''),('Καθοδηγητική: «Ποια είναι η επόμενη καλύτερη ενέργεια;»','',''),('Αξία και πολυπλοκότητα: η πλήρης εικόνα','Your figure, rebuilt sharp.','')]),
('Λειτουργεί; Τι δείχνουν τα δεδομένα',[('Η υπόσχεση: έγκαιρη προειδοποίηση σε κλίμακα','OU Analyse at the Open University: the same institution as our dataset.','Herodotou et al. (2019; 2020)'),('Πίνακες πληροφοριών: 38 μελέτες, περιορισμένες ενδείξεις','Best paper at LAK \'24; two of the authors are at UEF.','Kaliisa, Misiejuk, López-Pernas, Khalil & Saqr (2024)'),('Ερώτημα, 60″: ίδιο σύστημα, 11 πανεπιστήμια. Τι περιμένετε;','Zoom poll, three options. The next slide does not depend on the answers.',''),('MAAPS: τυχαιοποιημένη δοκιμή, 10.037 φοιτητές, έξι έτη','No significant effect on graduation or persistence overall.','Ithaka S+R, final MAAPS report'),('…εκτός από ένα: Georgia State, +7 ποσοστιαίες μονάδες','The only site that ran the intervention for all six years.','Ithaka S+R'),('Η υλοποίηση, όχι ο αλγόριθμος','What differed was people and follow-through. This is the argument of the whole course.','Ithaka S+R implementation study'),('Υποσημείωση: Purdue Course Signals και η αντίστροφη αιτιότητα','One slide, skippable. The single historical case in this part.','Caulfield (2013); Essa (2013)')]),
('Προκλήσεις σήμερα (update of your 2.8)',[('Αλγοριθμική μεροληψία','','Baker & Hawn (2022)'),('Η Παραγωγική ΤΝ αλλάζει τι σημαίνει ένα ίχνος: επίδοση ≠ μάθηση','','Yan, Greiff, Lodge & Gašević (2025); Misiejuk et al. (2025)'),('Κανονιστικό πλαίσιο: GDPR και Κανονισμός ΤΝ της ΕΕ','Education as a high-risk domain. Detail in Week 3.','Regulation (EU) 2024/1689; Kaliisa, Baker, Wasson & Prinsloo (2025)'),('«Μαθησιακή Αναλυτική» ή «Παρακολούθηση Μαθητών»;','Your 4.19 as a teaser for Week 3.','')]),
('Κλείσιμο',[('Ο χάρτης των τριών εβδομάδων','Replaces your 1.3.',''),('Να θυμάστε','Three lines.',''),('Διάλειμμα: επιστρέφουμε στις 19:15','Live countdown.','')]),
]
n=0; outl=''
for sec, items in OUT:
    outl += f'<tr class="sec"><td colspan="4">{e(sec)}</td></tr>'
    for t, d, s in items:
        n+=1; outl += f'<tr><td class="n">{n}</td><td class="gt">{e(t)}</td><td>{e(d)}</td><td class="s">{e(s)}</td></tr>'
page = f'''<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Week 1 review board</title><style>
:root{{--ink:#12233F;--mist:#EEF3FA;--line:#D3DDEB;--muted:#55657C;--deep:#0D47A1}}
*{{box-sizing:border-box}}body{{margin:0;font:16px/1.5 "Segoe UI","Helvetica Neue",Arial,sans-serif;color:var(--ink);background:#fff}}
main{{max-width:1180px;margin:0 auto;padding:36px 24px 80px}}h1{{font-size:34px;line-height:1.15;margin:0 0 8px}}h2{{font-size:24px;margin:52px 0 6px}}
p.lead{{font-size:18px;max-width:70ch;color:#33445E}}nav{{position:sticky;top:0;background:#fff;border-bottom:1px solid var(--line);padding:10px 0;margin:18px 0 0;z-index:5;display:flex;gap:18px;flex-wrap:wrap;font-weight:600}}
nav a{{color:var(--deep);text-decoration:none}}nav a:hover{{text-decoration:underline}}
.counts{{display:flex;gap:10px;flex-wrap:wrap;margin:18px 0}}.counts span{{border-radius:999px;padding:6px 14px;font-weight:700;font-size:14px}}
table{{width:100%;border-collapse:collapse;margin-top:12px}}td{{padding:10px 12px;vertical-align:top;border-bottom:1px solid var(--line)}}
td.th{{width:190px}}td.th img{{width:170px;border:1px solid var(--line);border-radius:6px;display:block}}
.ttl{{font-weight:600}}.meta{{color:var(--muted);font-size:13px;margin-top:2px}}.dest{{font-size:13px;font-weight:700;margin-top:6px;color:var(--deep)}}.note{{max-width:52ch}}
.badge{{display:inline-block;border-radius:6px;padding:3px 10px;font-size:12px;font-weight:800;letter-spacing:.02em}}
.b-KEEP{{background:#DDF3E5;color:#14532D}}.b-REBUILD{{background:#DCE8F8;color:#0D47A1}}.b-UPDATE{{background:#FFF4DA;color:#7A4F00}}
.b-MERGE{{background:#E9E4F7;color:#47308A}}.b-MOVE{{background:#E3EEF0;color:#1F5560}}.b-CUT{{background:#FCE4E2;color:#8F2019}}
tr.a-CUT img{{opacity:.45}}.verdict{{background:var(--mist);border-radius:10px;padding:14px 18px;max-width:80ch}}
.two{{display:grid;grid-template-columns:1fr 1fr;gap:28px}}@media(max-width:800px){{.two{{grid-template-columns:1fr}}td.th{{width:120px}}td.th img{{width:104px}}}}
.kv td{{padding:6px 10px}}.kv td:first-child{{color:var(--muted);width:46%}}
.out td.n{{width:34px;color:var(--muted);font-variant-numeric:tabular-nums}}.out td.gt{{font-weight:600;width:36%}}.out td.s{{color:var(--muted);font-size:14px;width:24%}}
.out tr.sec td{{background:var(--ink);color:#fff;font-weight:700;padding:7px 12px}}
ul{{padding-left:20px}}li{{margin:4px 0}}</style></head><body><main>
<h1>Week 1 review board</h1>
<p class="lead">All 93 slides from your five Week 1 decks, each with a decision and a reason. Veto anything by slide number. Below the decks: the wording sheet taken from your slides, and the slide-by-slide outline for Part 1.</p>
<div class="counts">{''.join(f'<span class="badge b-{k}">{k} {v}</span>' for k,v in cnt.most_common())}</div>
<nav>{''.join(f'<a href="#d{d}">Deck {d}</a>' for d in DECKS)}<a href="#img">Images</a><a href="#voc">Wording</a><a href="#out">Part 1 outline</a></nav>
{''.join(f'<h2 id="d{d}">Deck {e(t)} <span style="color:var(--muted);font-weight:400;font-size:16px">({len(rows[d])} slides)</span></h2><p class="verdict">{e(VERDICT[d])}</p><table>{"".join(rows[d])}</table>' for d,t in DECKS.items())}
<h2 id="img">Images: what I found and what I will do</h2>
<ul><li>121 placed pictures (94 PNG, 18 JPG, 6 GIF). Your decks contain no SmartArt and no native charts: every diagram is either a picture or loose shapes.</li>
<li><b>Reused as they are:</b> all ViLLE screenshots (3.40-3.49), including the 402-frame exam-analysis animation in 3.48, which plays natively in HTML.</li>
<li><b>Rebuilt natively:</b> three slides that are screenshots of Greek text (3.6, 3.7, 3.9), the analytics-types figure (3.20), the Moodle pipeline (3.39), the PRISMA diagram (5.4), and every infographic in deck 2.</li>
<li><b>Too low-resolution to show large:</b> 3.17, 3.20, 3.22, 3.26, 3.48, 4.4, 4.8 (51-71 pixels per inch). All except 3.48 are cut or rebuilt. For 3.48 I will keep the animation at its natural size.</li>
<li><b>Third-party cartoons and strips</b> (Dilbert, PhD Comics, Marketoonist, Glasbergen, timoelliott.com, the title sketch-note): I carry over only the ones you tell me to keep, with their credit line. My default is to keep at most two, in the ethics part.</li>
<li><b>No speaker notes exist in any of the five decks.</b> Everything you say is improvised on top of the slide, which is where the running over starts. The rebuild puts timed notes on every slide.</li></ul>
<h2 id="voc">Wording sheet, taken from your slides</h2>
<div class="two"><div><table class="kv">{''.join(f'<tr><td>{e(a)}</td><td><b>{e(b)}</b></td></tr>' for a,b in VOCAB)}</table></div>
<div><table class="kv">{''.join(f'<tr><td>{e(a)}</td><td><b>{e(b)}</b></td></tr>' for a,b in LABELS)}</table>
<ul><li>Formal second person plural throughout.</li><li>Your habit of bolding the key term inside a sentence is kept.</li><li>φοιτητές for higher education, μαθητές for school contexts (ViLLE), εκπαιδευόμενοι in definitions.</li>
<li>English terms stay in English where your slides keep them (dashboards, LMS, MOOCs).</li><li>No slide title or text depends on what students answer.</li></ul></div></div>
<h2 id="out">Week 1, Part 1: outline, version 2 ({n} slides)</h2>
<p class="lead">One idea per slide; diagram build-ups count as slides. Greek titles are working titles. Two slides are marked skippable. Sources dated 2020 or later unless they are a definition, a reference model or the one historical case.</p>
<table class="out">{outl}</table>
</main></body></html>'''
open('/mnt/user-data/outputs/LA_Week1_review_board.html','w',encoding='utf8').write(page)
print('slides in outline:', n, '| file KB:', round(len(page)/1024))
