"""One-page student sheets (rework of 20 Sept 2026) -> out/Lab1_sheet.html, out/Lab2_sheet.html, out/Search_sheet.html, out/Submission_checklist.html
CSS: the Lab 1 pack stylesheet (lab1/build_pack.py), so all four sit in the same visual family as the decks and the old packs.
Lab sheets: content and layout of _handover/Lab1_one_page.html and Lab2_one_page.html (approved by the lecturer); numbers untouched.
Search sheet: workshop1/eric_counts.json is the single source of the ERIC counts.  PDF: python3 lab1/topdf.py <html> <pdf> (must say 'pages overflowing: none')."""
import json, os, re, html
HERE = os.path.dirname(os.path.abspath(__file__)); K = os.path.join(HERE, '..'); e = html.escape
CSS = re.search(r"CSS = '''(.*?)'''", open(f'{K}/lab1/build_pack.py', encoding='utf8').read(), re.S).group(1)
CSS += '''
.page{padding:10mm 14mm 8mm}.content{gap:1.3mm}header{margin-bottom:3mm;padding-bottom:2mm}h1{font-size:16.5pt}h2{font-size:11.2pt;margin:1.8mm 0 .8mm}
p.lead{font-size:9.5pt;line-height:1.33;margin-bottom:0}
table.data{width:100%;border-collapse:collapse;font-size:8.5pt;line-height:1.22}table.data th{background:var(--ink);color:#fff;font-weight:700;padding:1.3mm 1.4mm;text-align:center;vertical-align:bottom;font-size:7.9pt;line-height:1.15}
table.data th.l{text-align:left}table.data td{padding:1mm 1.4mm;border-bottom:.6pt solid var(--line);text-align:center;vertical-align:middle}table.data td.l{text-align:left}
table.data td .nm{white-space:nowrap}table.data td .rule{color:var(--muted);font-size:7.9pt}table.data td.acc{font-weight:800;color:var(--deep)}table.data tr.base td{border-bottom:none;color:var(--muted);font-size:8.3pt;padding-top:1.3mm}
.note{background:var(--mist);border-radius:2mm;padding:1.7mm 2.6mm;font-size:8.1pt;line-height:1.27;color:var(--body);text-align:justify}
table.charts{width:100%;border-collapse:collapse}table.charts td{vertical-align:top;padding:0;text-align:center}table.charts svg{height:30mm;width:auto}
.ctitle{font-size:8.6pt;font-weight:700;color:var(--deep);text-align:center;margin-bottom:.2mm}.facts{font-size:8.6pt;line-height:1.28;text-align:justify;color:var(--body)}
.qbox{border:1.2pt solid var(--ink);border-radius:3mm;padding:2.2mm 3.6mm 1.8mm;background:var(--mist);margin-top:.6mm}.qbox .qt{font-weight:800;color:var(--deep);font-size:10.2pt;margin-bottom:.6mm}
table.q{width:100%;border-collapse:collapse}table.q td{vertical-align:top;padding:.35mm 0;text-align:justify;font-size:9.1pt;line-height:1.28}table.q td.n{width:6mm;font-weight:800;color:var(--deep)}
.how{font-size:8.5pt;line-height:1.28;text-align:justify;margin-top:.4mm;color:var(--body)}.how b{color:var(--ink)}
table.cols{width:100%;border-collapse:collapse;table-layout:fixed}table.cols td{vertical-align:top;padding:0}table.cols td+td{padding-left:4mm}table.cols svg{width:100%;height:auto}
footer{font-size:7.7pt;white-space:nowrap}.src{font-size:7.8pt;line-height:1.25;color:var(--muted);text-align:justify}.tab{font-size:8.4pt;color:var(--amber-ink);font-weight:700;background:var(--amber-bg);border-radius:999px;padding:.5mm 3mm;float:right;margin-top:1.2mm}
'''
def doc(title, body): return f'<!DOCTYPE html><html lang="el"><head><meta charset="UTF-8"><title>{e(title)}</title><link href="https://fonts.googleapis.com/css2?family=Commissioner:wght@400;500;700;800&display=swap" rel="stylesheet"><style>{CSS}</style></head><body>{body}</body></html>'
def page(kick, title, body, left, right, tag=None):
    t = f'<span class="tab">{e(tag)}</span>' if tag else ''
    return f'<section class="page"><header>{t}<span class="kick">{e(kick)}</span><h1>{e(title)}</h1></header><div class="content">{body}</div><footer><span>{e(left)}</span><span>{e(right)}</span></footer></section>'
RECOLOR = {'#1f5fa8': '#0D47A1', '#c0504d': '#D8433B', '#1b2a41': '#12233F', '#4a5a70': '#55657C', '#c9d2de': '#D3DDEB', 'Carlito, Liberation Sans, DejaVu Sans, sans-serif': 'Commissioner, Segoe UI, Arial, sans-serif'}
def port(src):
    """approved one-page HTML -> (question, inner content) in the kit's family: strip and foot tables dropped, colours mapped, numbers untouched"""
    s = open(src, encoding='utf8').read(); b = re.search(r'<body>(.*)</body>', s, re.S).group(1)
    b = re.sub(r'<table class="strip">.*?</table>', '', b, count=1, flags=re.S); b = re.sub(r'<table class="foot">.*?</table>', '', b, count=1, flags=re.S)
    b = re.sub(r'<h1>.*?</h1>\s*', '', b, count=1, flags=re.S); q = re.search(r'<div class="sub">(.*?)</div>', b, re.S).group(1).strip(); b = re.sub(r'<div class="sub">.*?</div>\s*', '', b, count=1, flags=re.S)
    b = re.sub(r'(<p>)', r'<p class="lead">', b, count=1)
    for a, c in RECOLOR.items(): b = b.replace(a, c)
    b = re.sub(r'<td class="l">(.*?)<br>', r'<td class="l"><span class="nm">\1</span><br>', b); b = b.replace('<table class="two"', '<table class="cols"'); return q, b.strip()
NUM = lambda h: re.findall(r'\d[\d.,%]*', re.sub(r'<svg.*?</svg>', '', h, flags=re.S))
COURSE = 'Βάσεις Δεδομένων & Ανάλυση Δεδομένων Μάθησης'
os.makedirs(f'{K}/out', exist_ok=True)
# ------------------------------------------------------------------ Lab 1 and Lab 2 sheets
for n, src, part, tag, right in [(1, 'Lab1_one_page.html', 'Εβδομάδα 2, Μέρος 2', 'Προσομοιωμένα δεδομένα', 'Εργαστήριο 1'),
                                 (2, 'Lab2_one_page.html', 'Εβδομάδα 3, Μέρος 2', 'Πραγματικά, ανωνυμοποιημένα δεδομένα', 'Εργαστήριο 2')]:
    q, body = port(f'{HERE}/{src}'); orig = re.search(r'<body>(.*)</body>', open(f'{HERE}/{src}', encoding='utf8').read(), re.S).group(1)
    core = re.sub(r'<table class="strip">.*?</table>|<table class="foot">.*?</table>|<h1>.*?</h1>|<div class="sub">.*?</div>', '', orig, flags=re.S)
    assert NUM(body) == NUM(core) and len(NUM(core)) > 60, 'numbers changed'   # every number of the approved sheet, in the same order
    foot_txt = re.search(r'<table class="foot">.*?<td>(.*?)</td>', orig, re.S).group(1).strip()   # the approved sheet's own attribution line
    if n == 2: body += f'<p class="src">{foot_txt}</p>'; left = f'{COURSE} · {part}'
    else: left, right = COURSE, foot_txt
    open(f'{K}/out/Lab{n}_sheet.html', 'w', encoding='utf8').write(doc(f'Εργαστήριο {n} · Φύλλο εργασίας', page(f'Εργαστήριο {n} · Φύλλο εργασίας · {part}', q, body, left, right, tag)))
    print(f'Lab{n}_sheet.html written; numbers kept:', len(NUM(body)))

# ------------------------------------------------------------------ Search sheet (Week 2): syntax per database, the three traps, the four checks, calibration, sources
E_ = json.load(open(f'{K}/workshop1/eric_counts.json', encoding='utf8')); Q = {k: v['n'] for k, v in E_['queries'].items()}; R = E_['retrieved']; DATE = f'{R[8:10]}/{R[5:7]}/{R[0:4]}'
CSS2 = '''code{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:7.5pt;background:var(--mist);padding:.15mm 1mm;border-radius:1mm}
.t td{font-size:8.2pt;padding:1mm 1.5mm;line-height:1.25}.t th{padding:1.2mm 1.5mm;font-size:8.2pt}.t.syn td{font-size:7.9pt;padding:.8mm 1.4mm;line-height:1.22}.t.syn td:first-child{width:13%;font-weight:700}.t.syn th:not(:first-child){width:21.75%}
.t.traps td:nth-child(2){text-align:center;font-weight:800;width:11%;font-size:10pt;color:var(--red)}.t.traps td:first-child{width:46%}
.grid2{display:grid;grid-template-columns:1.12fr 1fr;gap:4mm;align-items:start}.box{border:1.2pt solid var(--ink);border-radius:3mm;padding:2.4mm 3.6mm 2mm}.box h3{color:var(--deep);font-size:10.2pt;margin-bottom:1mm}
.box ol{list-style:none;counter-reset:c;display:grid;gap:1mm}.box ol li{counter-increment:c;display:grid;grid-template-columns:6mm 1fr;font-size:8.9pt;line-height:1.3;text-align:justify}.box ol li::before{content:counter(c);width:4.6mm;height:4.6mm;border-radius:50%;background:var(--deep);color:#fff;font-size:8pt;font-weight:800;display:grid;place-items:center;margin-top:.5mm}
.rule{background:var(--amber-bg);border-left:3pt solid var(--amber);border-radius:2mm;padding:2.2mm 3.4mm;font-size:8.9pt;line-height:1.32;text-align:justify}.rule b{color:var(--amber-ink)}
.t.fn td:nth-child(2),.t.fn th:nth-child(2),.t.fn td:nth-child(3),.t.fn th:nth-child(3){text-align:right;width:16%}.t.fn td:first-child code{font-size:7.7pt}
.log{font-size:8.9pt;line-height:1.32;text-align:justify}.srcl{font-size:7.6pt;line-height:1.26;color:var(--muted);text-align:justify}
.t.chk td:first-child{width:24%;font-weight:700}.t.pr td:first-child{width:50%}.t.pr td:nth-child(2){color:var(--red-ink,#A92C25)}
.two2{display:grid;grid-template-columns:1fr 1fr;gap:4mm;align-items:start}.mist{background:var(--mist);border-radius:2.5mm;padding:2.4mm 3.6mm;font-size:9pt;line-height:1.34;text-align:justify}.mist b{color:var(--deep)}
'''
CSS += CSS2
syn = [('Πρόσβαση', 'Μέσω HEAL-Link, του συνδέσμου των ελληνικών ακαδημαϊκών βιβλιοθηκών: με τον ιδρυματικό σας λογαριασμό, από το δίκτυο του ιδρύματος ή με VPN.', 'Ελεύθερη, χωρίς σύνδεση, από οποιονδήποτε υπολογιστή: eric.ed.gov', 'Η αναζήτηση και οι περιλήψεις είναι ελεύθερες.', 'Η αναζήτηση και οι περιλήψεις είναι ελεύθερες.'),
       ('Πού αναζητά', '<code>TITLE-ABS-KEY( … )</code>: τίτλος, περίληψη, λέξεις-κλειδιά.', 'Προεπιλογή: τίτλος, συγγραφέας, πηγή, περίληψη, περιγραφείς. Πεδία: <code>title:</code> <code>abstract:</code> <code>descriptor:</code>', 'Command Search. Προεπιλογή «All Metadata»· πεδία όπως <code>"Document Title":</code> και <code>"Abstract":</code>', 'Advanced Search, «Search Within»: Title, Abstract. Για ευρύτερη κάλυψη: «The ACM Guide to Computing Literature».'),
       ('Τελεστές', 'AND, OR, AND NOT. Το OR εκτελείται πριν από το AND· το AND NOT μπαίνει στο τέλος.', 'AND, OR, πάντοτε με παρενθέσεις: χωρίς αυτές, η ανάμειξή τους δεν επιστρέφει αποτελέσματα.', 'AND, OR, NOT, με κεφαλαία. Εγγύτητα: NEAR, ONEAR.', 'AND, OR, NOT, με κεφαλαία.'),
       ('Φράσεις', '<code>"…"</code> χαλαρή φράση: δέχεται πληθυντικούς και αστερίσκο. <code>{…}</code> ακριβής φράση. Μόνο ευθέα εισαγωγικά.', '<code>"…"</code> ακριβής φράση. Με καμπύλα εισαγωγικά οι λέξεις αναζητούνται χωριστά.', '<code>"…"</code> ακριβής φράση· ο αστερίσκος επιτρέπεται και μέσα της.', '<code>"…"</code> ακριβής φράση.'),
       ('Αστερίσκος', '<code>*</code> για πολλούς χαρακτήρες, <code>?</code> για έναν.', '<code>*</code> μόνο σε μεμονωμένη λέξη: όχι μέσα σε φράση, όχι μετά από ενωτικό. Οι πληθυντικοί βρίσκονται αυτόματα.', '<code>*</code> και <code>?</code>. Τουλάχιστον 3 χαρακτήρες πριν από τον αστερίσκο· έως 10 ανά αναζήτηση. Έως 25 όροι ανά παρένθεση.', 'Ελέγξτε τη βοήθεια της βάσης πριν τον χρησιμοποιήσετε.'),
       ('Χρονολογία', '<code>AND PUBYEAR &gt; 2018</code>', '<code>pubyearmin:2019</code> στο τέλος της συμβολοσειράς.', 'Φίλτρο «Year» στη σελίδα των αποτελεσμάτων.', 'Φίλτρο ημερομηνίας στη σελίδα των αποτελεσμάτων.')]
B1 = '("learning analytics")'; B2 = 'AND (dashboard* OR "visual analytics")'; B3 = 'AND ("self-regulated learning" OR self-regulation OR SRL)'; B4 = 'AND ("higher education" OR universit* OR undergraduate*)'
gr = lambda n: f'{n:,}'.replace(',', '.')
search_body = f'''<table class="t syn"><tr><th></th><th>Scopus</th><th>ERIC</th><th>IEEE Xplore</th><th>ACM Digital Library</th></tr>{''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in r) + '</tr>' for r in syn)}</table>
<div class="grid2"><div><h2 style="margin-top:0">Τρεις παγίδες στο ERIC</h2>
<table class="t traps"><tr><th>Τι πληκτρολογήθηκε στο ERIC</th><th>Πλήθος</th><th>Σύγκριση</th></tr>
<tr><td><code>"learning analytics" AND "self-regulat*"</code><br>Αστερίσκος μέσα σε φράση ή μετά από ενωτικό.</td><td>{Q['q_wild_in_quotes']}</td><td>{Q['q_phrase']} με <code>"self-regulated learning"</code></td></tr>
<tr><td><code>“learning analytics” AND dashboard*</code><br>Καμπύλα εισαγωγικά, από το Word.</td><td>{Q['q_curly']}</td><td>{Q['q_straight']} με ευθέα εισαγωγικά</td></tr>
<tr><td><code>dashboard* OR widget* AND "learning analytics"</code><br>Χωρίς παρενθέσεις.</td><td>{Q['p_none']}</td><td>{Q['p_or_first']} με <code>(dashboard* OR widget*) AND …</code><br>{Q['p_and_first']} με <code>dashboard* OR (widget* AND …)</code></td></tr></table>
<h2>Βαθμονόμηση: το παράδειγμα του μαθήματος στο ERIC, μπλοκ προς μπλοκ</h2>
<table class="t fn"><tr><th>Συμβολοσειρά (κάθε γραμμή προσθέτει ένα μπλοκ)</th><th>Όλα τα έτη</th><th>Από το 2019</th></tr>
<tr><td><code>{e(B1)}</code></td><td>{gr(Q['n1'])}</td><td></td></tr><tr><td><code>{e(B2)}</code></td><td>{Q['n2']}</td><td>{Q['n2_2019']}</td></tr>
<tr><td><code>{e(B3)}</code></td><td>{Q['n3']}</td><td>{Q['n3_2019']}</td></tr><tr><td><code>{e(B4)}</code></td><td>{Q['n4']}</td><td>{Q['n4_2019']}</td></tr></table></div>
<div><div class="box"><h3>Οι τέσσερις έλεγχοι, πριν από κάθε εκτέλεση</h3><ol><li>Ταιριάζει η συμβολοσειρά με το ερώτημα; Λείπει ή περισσεύει κάποια έννοια;</li><li>OR μέσα στο μπλοκ, AND ανάμεσα στα μπλοκ, παρενθέσεις παντού;</li><li>Ορθογραφία, αστερίσκοι, ευθέα εισαγωγικά;</li><li>Είναι τα φίλτρα αιτιολογημένα και το πλήθος εύλογο;</li></ol></div>
<div class="rule" style="margin-top:3mm"><b>Ο κανόνας της βαθμονόμησης.</b> Πάνω από 500 αποτελέσματα: στενεύετε, με μία ακόμη έννοια ή με περιορισμό σε τίτλο και περίληψη. Κάτω από 40: διευρύνετε, με περισσότερα συνώνυμα, με αφαίρεση της λιγότερο ουσιώδους έννοιας ή με ευρύτερο χρονικό διάστημα. Και ένας έλεγχος ακόμη: βρίσκει η συμβολοσειρά τα δύο άρθρα που ήδη γνωρίζετε ότι ανήκουν στο θέμα; Η βαθμονόμηση γίνεται ξεχωριστά για κάθε βάση: η ίδια συμβολοσειρά δίνει στη Scopus πολύ περισσότερα από ό,τι στο ERIC.</div>
<p class="log" style="margin-top:3mm"><b>Τι καταγράφετε για κάθε εκτέλεση</b>, σε νέα γραμμή του ημερολογίου σας: βάση, ημερομηνία, συμβολοσειρά όπως εκτελέστηκε, φίλτρα, πλήθος αποτελεσμάτων. Η πρώτη γραμμή δεν σβήνεται ποτέ. Από το ημερολόγιο γράφεται η στρατηγική αναζήτησης της Μεθοδολογίας.</p></div></div>
<p class="srcl"><b>Χωρίς πρόσβαση στη Scopus;</b> Όλα γίνονται και στο ERIC: η βαθμονόμηση και οι τρεις παγίδες παραπάνω είναι ήδη από εκεί. <b>Πηγές.</b> Elsevier, Scopus Support Center· ERIC, Advanced Search Tips, και αναζητήσεις του διδάσκοντος στο eric.ed.gov στις {DATE} (τα πλήθη αλλάζουν με τον χρόνο)· IEEE Xplore Help (Command Search)· ACM Digital Library, Advanced Search. Οι έλεγχοι είναι προσαρμογή του PRESS 2015: McGowan, Sampson, Salzwedel, Cogo, Foerster &amp; Lefebvre (2016), Journal of Clinical Epidemiology, 75, 40–46. Τι καταγράφεται για κάθε αναζήτηση: PRISMA-S, Rethlefsen et al. (2021), Systematic Reviews, 10, 39. Οι βάσεις αλλάζουν: σε περίπτωση αμφιβολίας ισχύει η βοήθεια της ίδιας της βάσης.</p>'''
open(f'{K}/out/Search_sheet.html', 'w', encoding='utf8').write(doc('Φύλλο αναζήτησης', page('Εργασία 3 · Υλικό υποστήριξης · Φύλλο αναζήτησης βιβλιογραφίας', 'Η ίδια συμβολοσειρά δεν τρέχει παντού', search_body, COURSE, 'Εργασία 3')))
print('Search_sheet.html written')

# ------------------------------------------------------------------ Submission checklist (Week 3): the steps of your own review, extraction rules, synthesis, PRISMA numbers, check before submission, APA 7
check_body = '''<div class="two2"><div><h2 style="margin-top:0">Τα βήματα, στις δικές σας μελέτες</h2>
<div class="box" style="border-color:var(--line)"><ol><li>Πλήρη κείμενα και Στάδιο 2 της επιλογής, με λόγο για κάθε αποκλεισμό.</li><li>Δοκιμή του πίνακα εξαγωγής σε τρεις μελέτες· αν μια στήλη μένει συχνά κενή, το πρόβλημα είναι η στήλη.</li><li>Εξαγωγή και αξιολόγηση ποιότητας για κάθε μελέτη που εντάχθηκε, με ίδιες στήλες για όλες.</li><li>Σύνθεση ανά ερευνητικό ερώτημα, και κατόπιν συγγραφή.</li></ol>
<p class="srcl" style="margin-top:1.6mm">Στο προαιρετικό αρχείο προτύπων της εργασίας, τα φύλλα 2_Επιλογή, 3_Εξαγωγή, 4_Ποιότητα και 5_Σύνθεση ακολουθούν ακριβώς αυτά τα βήματα και υπολογίζουν αυτόματα τους αριθμούς του PRISMA.</p></div>
<h2>Τρεις κανόνες για τη γραμμή εξαγωγής</h2>
<div class="box"><ol><li>Το εύρημα γράφεται με κατεύθυνση και, όπου υπάρχει, με μέγεθος. «Η μελέτη εξέτασε…» δεν είναι εύρημα.</li><li>Το δείγμα γράφεται με αριθμούς και με το ποιοι ήταν οι συμμετέχοντες.</li><li>Κενή στήλη σημαίνει «δεν αναφέρεται στη μελέτη», και γράφεται έτσι.</li></ol></div>
<h2>Σύνθεση δεν είναι παράθεση</h2>
<div class="mist">«Ο Α βρήκε… Ο Β βρήκε… Ο Γ βρήκε…» είναι τρεις περιλήψεις. Σύνθεση είναι ο ισχυρισμός που προκύπτει από τις μελέτες μαζί, με το πόσες τον στηρίζουν και πόσες όχι. Για κάθε ισχυρισμό: <b>σε ποιο ερευνητικό ερώτημα</b> απαντά· <b>μία πρόταση, χωρίς ερμηνεία</b> (η ερμηνεία ανήκει στη Συζήτηση)· <b>μελέτες υπέρ και κατά</b>· <b>ποιότητα</b> των μελετών υπέρ· <b>πλαίσια</b> όπου ισχύει· και <b>η πρόταση</b> όπως θα γραφτεί στα Αποτελέσματα, με τις παραπομπές της. Κάθε ερευνητικό ερώτημα γίνεται μία ενότητα στα Αποτελέσματα.</div>
<h2>Τέσσερα συνήθη λάθη</h2>
<div class="box" style="border-color:var(--red)"><ol><li>Στήλες που αλλάζουν από μελέτη σε μελέτη: ο πίνακας παύει να συγκρίνει.</li><li>Ευρήματα αντιγραμμένα από την περίληψη, χωρίς κατεύθυνση και μέγεθος.</li><li>Ισχυρισμοί που στηρίζονται σε μία μόνο μελέτη και γράφονται ως βεβαιότητες.</li><li>Καταμέτρηση μελετών αντί για στάθμιση: δέκα αδύναμες μελέτες δεν υπερισχύουν δύο ισχυρών.</li></ol></div></div>
<div><h2 style="margin-top:0">PRISMA 2020: τέσσερις έλεγχοι στους αριθμούς σας</h2>
<table class="t pr"><tr><th>Έλεγχος</th><th>Αν δεν ισχύει</th></tr>
<tr><td>Εγγραφές ανά βάση = σύνολο που εντοπίστηκε</td><td>λείπει αναζήτηση από το ημερολόγιο</td></tr>
<tr><td>Σύνολο − διπλοεγγραφές = εγγραφές προς διαλογή</td><td>διπλοεγγραφές που αφαιρέθηκαν χωρίς να μετρηθούν</td></tr>
<tr><td>Διαλογή − αποκλεισμοί = πλήρη κείμενα</td><td>εγγραφή χωρίς απόφαση στο Στάδιο 1</td></tr>
<tr><td>Πλήρη κείμενα − αποκλεισμοί με λόγο = μελέτες</td><td>αποκλεισμός χωρίς καταγεγραμμένο λόγο</td></tr></table>
<p class="srcl" style="margin-top:1.4mm">Page et al. (2021), The PRISMA 2020 statement, BMJ, 372, n71. Η εργασία χωρίς δομή PRISMA και χωρίς διάγραμμα ροής επιστρέφεται για επανυποβολή.</p>
<h2>Έλεγχος πριν από την υποβολή</h2>
<table class="t chk"><tr><th>Ενότητα</th><th>Τι πρέπει να υπάρχει</th></tr>
<tr><td>Μεθοδολογία</td><td>Συμβολοσειρά και ημερολόγιο αναζήτησης· κριτήρια ένταξης και αποκλεισμού· διάγραμμα PRISMA 2020 με αριθμούς που αθροίζονται.</td></tr>
<tr><td>Αποτελέσματα</td><td>Πίνακας μελετών· μία ενότητα ανά ερευνητικό ερώτημα· γραφήματα ανά έτος, πλαίσιο και μέθοδο.</td></tr>
<tr><td>Συζήτηση</td><td>Ερμηνεία· σύγκριση με προηγούμενες έρευνες· περιορισμοί της δικής σας ανασκόπησης· τι λείπει από τη βιβλιογραφία.</td></tr>
<tr><td>Μορφή</td><td>APA 7· 4.000 έως 6.000 λέξεις· δήλωση για τη χρήση Τεχνητής Νοημοσύνης στο τέλος, όπως ορίζει η εκφώνηση.</td></tr></table>
<h2>APA 7 σε τρεις γραμμές</h2>
<div class="mist"><b>Στο κείμενο:</b> (Hellings &amp; Haelermans, 2022) για δύο συγγραφείς· (Bañeres et al., 2023) για τρεις ή περισσότερους, από την πρώτη αναφορά.<br><b>Άρθρο περιοδικού:</b> Επώνυμο, Α. Α., &amp; Επώνυμο, Β. Β. (Έτος). Τίτλος άρθρου. <i>Τίτλος Περιοδικού, τόμος</i>(τεύχος), σελίδες. https://doi.org/…<br><b>Παράδειγμα:</b> Hellings, J., &amp; Haelermans, C. (2022). The effect of providing learning analytics on student behaviour and performance in programming: A randomised controlled experiment. <i>Higher Education, 83</i>(1), 1–18. https://doi.org/10.1007/s10734-020-00560-z</div>
<p class="srcl" style="margin-top:1.4mm">Η προθεσμία και ο τρόπος υποβολής ορίζονται στην πλατφόρμα του μαθήματος. Απορίες: στην πλατφόρμα, ανά πάσα στιγμή.</p></div></div>'''
open(f'{K}/out/Submission_checklist.html', 'w', encoding='utf8').write(doc('Λίστα ελέγχου', page('Εργασία 3 · Υλικό υποστήριξης · Λίστα ελέγχου έως την υποβολή', 'Για τη δική σας ανασκόπηση, από την επιλογή ως την υποβολή', check_body, COURSE, 'Εργασία 3')))
print('Submission_checklist.html written')
