"""Workshop 1 student handout (3 A4 pages, Greek) and teacher sheet (2 A4 pages, Greek) -> out/*.html ; counts from eric_counts.json"""
import json, os, html
HERE = os.path.dirname(os.path.abspath(__file__)); K = os.path.join(HERE, '..')
src = open(f'{K}/lab1/build_pack.py', encoding='utf8').read(); i = src.index("CSS = '''") + 9; CSS = src[i:src.index("'''", i)]
E = json.load(open(f'{HERE}/eric_counts.json', encoding='utf8')); Q = {k: v['n'] for k, v in E['queries'].items()}; d = E['retrieved']; DATE = f'{d[8:10]}/{d[5:7]}/{d[0:4]}'
e = html.escape; gr = lambda n: f'{n:,}'.replace(',', '.')
XCSS = CSS + '''body{font-size:9.9pt;line-height:1.36}h2{margin:3.2mm 0 1.2mm;font-size:12pt}.content{gap:2.6mm}.t td{font-size:9.3pt;padding:1.5mm 2.2mm}.t th{padding:1.6mm 2.2mm}.note,.sim{padding:2.6mm 3.6mm;font-size:9.3pt}.page{padding:13mm 15mm 11mm}header{margin-bottom:3.5mm;padding-bottom:2.2mm}h1{font-size:17.5pt}
code,.mono{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:8.8pt;background:var(--mist);padding:.2mm 1.2mm;border-radius:1mm}
.steps{list-style:none;counter-reset:s;display:grid;gap:2.4mm}.steps li{counter-increment:s;display:grid;grid-template-columns:9mm 1fr;text-align:justify}.steps li::before{content:counter(s);width:6.2mm;height:6.2mm;border-radius:50%;background:var(--deep);color:#fff;font-size:9.5pt;font-weight:800;display:grid;place-items:center}
.roles{display:grid;grid-template-columns:repeat(4,1fr);gap:3mm}.roles div{background:var(--mist);border-radius:2.5mm;padding:2.6mm 3mm;font-size:9.4pt;line-height:1.35}.roles b{display:block;color:var(--deep);font-size:10.2pt;margin-bottom:.8mm}
.chk4{border:1.2pt solid var(--ink);border-radius:3mm;padding:3.5mm 4.5mm}.chk4 h3{color:var(--deep)}.chk4 ol{margin-left:5mm;display:grid;gap:1.2mm}.chk4 li{text-align:justify}
.t.syn td,.t.syn th{font-size:8.3pt;padding:1.3mm 1.7mm;line-height:1.3}.t.syn td:first-child{width:17%;font-weight:700}.t.syn th:not(:first-child){width:20.75%}
.t.fn td:nth-child(2),.t.fn th:nth-child(2),.t.fn td:nth-child(3),.t.fn th:nth-child(3){text-align:right;width:17%}.t.fn td:first-child{width:auto}.t td code{white-space:normal;word-break:break-word}
.t.traps td:first-child{width:47%}.t.traps td:nth-child(2),.t.traps th:nth-child(2){width:13%;text-align:right;font-weight:800}.t.traps td:nth-child(3){width:40%}.srcl{font-size:8.2pt;color:var(--muted);line-height:1.35;text-align:left}.t.err td:first-child{width:36%}.t.err td{font-size:9.2pt}.t.run td:first-child{width:14%}.t.run td:nth-child(2){width:13%}'''
def page(n, N, kicker, title, body, foot): return f'<section class="page"><header><span class="kick">{e(kicker)}</span><h1>{e(title)}</h1></header><div class="content">{body}</div><footer><span>{e(foot)}</span><span>σελίδα {n} από {N}</span></footer></section>'
def doc(title, pages): return f'<!DOCTYPE html><html lang="el"><head><meta charset="UTF-8"><title>{e(title)}</title><link href="https://fonts.googleapis.com/css2?family=Commissioner:wght@400;500;700;800&display=swap" rel="stylesheet"><style>{XCSS}</style></head><body>{"".join(pages)}</body></html>'
B1 = '("learning analytics")'; B2 = 'AND (dashboard* OR "visual analytics")'; B3 = 'AND ("self-regulated learning" OR self-regulation OR SRL)'; B4 = 'AND ("higher education" OR universit* OR undergraduate*)'
FOOT = 'Βάσεις Δεδομένων & Ανάλυση Δεδομένων Μάθησης · Εβδομάδα 2, Μέρος 3 · Εργαστήριο αναζήτησης'
# ---------------------------------------------------------------- student handout
H = []
H.append(page(1, 3, 'Εργαστήριο αναζήτησης βιβλιογραφίας · Φυλλάδιο', 'Μία συμβολοσειρά, δύο καταγεγραμμένες εκτελέσεις, μία απόφαση', f'''
<div class="sim"><b>Η εργασία σας παραμένει ατομική ή σε δυάδα.</b> Απόψε η αίθουσα δουλεύει ως μία ομάδα, πάνω στο θέμα ανασκόπησης ενός μέλους της. Κατόπιν ο καθένας επαναλαμβάνει τα ίδια βήματα για τη δική του ανασκόπηση, με το ίδιο φύλλο και αυτό το φυλλάδιο.</div>
<h2>Ρόλοι</h2><div class="roles"><div><b>Οθόνη</b>Μοιράζεται το φύλλο 0_Συμβολοσειρά και γράφει τους όρους που αποφασίζει η ομάδα.</div><div><b>Βάση δεδομένων</b>Εκτελεί τη συμβολοσειρά στη Scopus ή, χωρίς πρόσβαση από το σπίτι, στο ERIC.</div><div><b>Ημερολόγιο</b>Καταγράφει κάθε εκτέλεση στο φύλλο 1_Αναζήτηση, όπως ακριβώς έγινε.</div><div><b>Έλεγχος</b>Εφαρμόζει τους τέσσερις ελέγχους πριν από κάθε εκτέλεση.</div></div>
<h2>Βήματα</h2><ol class="steps">
<li><span><b>Θέμα.</b> Διαλέγετε το θέμα του μέλους του οποίου η δοκιμαστική αναζήτηση έδωσε το πιο προβληματικό πλήθος. Γράφετε το ερώτημα με PCC ή PICO, όπως στην Εβδομάδα 1.</span></li>
<li><span><b>Έννοιες.</b> Μία στήλη ανά έννοια στο φύλλο <b>0_Συμβολοσειρά</b>. Δύο έως τέσσερις έννοιες συνήθως αρκούν· το αποτέλεσμα (outcome) συχνά δεν χρειάζεται να μπει στη συμβολοσειρά.</span></li>
<li><span><b>Συνώνυμα,</b> ένα ανά κελί. Τρεις πηγές: οι λέξεις-κλειδιά των άρθρων που βρήκατε στη δοκιμαστική αναζήτηση· ο θησαυρός του ERIC (Thesaurus)· ορθογραφικές παραλλαγές και συντομογραφίες, όπως <code>analys*</code> και <code>analyz*</code>, <code>behaviour</code> και <code>behavior</code>, <code>SRL</code>.</span></li>
<li><span><b>Πρώτη εκτέλεση.</b> Αντιγράφετε τη συμβολοσειρά από το φύλλο στη βάση και εκτελείτε. Καταγράφετε αμέσως στο φύλλο <b>1_Αναζήτηση</b>: βάση, ημερομηνία, συμβολοσειρά όπως εκτελέστηκε, φίλτρα, πλήθος αποτελεσμάτων.</span></li>
<li><span><b>Έλεγχος και δεύτερη εκτέλεση.</b> Εφαρμόζετε τους τέσσερις ελέγχους. Αλλάζετε <b>ένα</b> πράγμα, εκτελείτε ξανά και καταγράφετε ξανά, σε νέα γραμμή. Η πρώτη γραμμή δεν σβήνεται.</span></li>
<li><span><b>Απόφαση.</b> Πάνω από 500 αποτελέσματα: στενεύετε, με μία ακόμη έννοια ή με περιορισμό σε τίτλο και περίληψη. Κάτω από 40: διευρύνετε, με περισσότερα συνώνυμα, με αφαίρεση της λιγότερο ουσιώδους έννοιας ή με ευρύτερο χρονικό διάστημα. Ελέγχετε επίσης αν η συμβολοσειρά βρίσκει τα δύο άρθρα που ήδη γνωρίζετε ότι ανήκουν στο θέμα.</span></li></ol>
<div class="chk4"><h3>Οι τέσσερις έλεγχοι</h3><ol><li>Ταιριάζει η συμβολοσειρά με το ερώτημα; Λείπει ή περισσεύει κάποια έννοια;</li><li>OR μέσα στο μπλοκ, AND ανάμεσα στα μπλοκ, παρενθέσεις παντού;</li><li>Ορθογραφία, αστερίσκοι, ευθέα εισαγωγικά;</li><li>Είναι τα φίλτρα αιτιολογημένα και το πλήθος εύλογο;</li></ol></div>
<p class="srcl">Οι έλεγχοι είναι προσαρμογή του PRESS 2015: McGowan, Sampson, Salzwedel, Cogo, Foerster &amp; Lefebvre (2016), Journal of Clinical Epidemiology, 75, 40–46. Τι καταγράφεται για κάθε αναζήτηση: PRISMA-S, Rethlefsen et al. (2021), Systematic Reviews, 10, 39.</p>''', FOOT))
syn = [('Πρόσβαση', 'HEAL-Link: από το δίκτυο του Πανεπιστημίου ή με VPN.', 'Ελεύθερη, χωρίς σύνδεση: eric.ed.gov', 'Η αναζήτηση και οι περιλήψεις είναι ελεύθερες.', 'Η αναζήτηση και οι περιλήψεις είναι ελεύθερες.'),
       ('Πού αναζητά', '<code>TITLE-ABS-KEY( … )</code>: τίτλος, περίληψη, λέξεις-κλειδιά.', 'Προεπιλογή: τίτλος, συγγραφέας, πηγή, περίληψη, περιγραφείς. Πεδία: <code>title:</code> <code>abstract:</code> <code>descriptor:</code>', 'Command Search. Προεπιλογή «All Metadata»· πεδία όπως <code>"Document Title":</code> και <code>"Abstract":</code>', 'Advanced Search, «Search Within»: Title, Abstract. Για ευρύτερη κάλυψη: «The ACM Guide to Computing Literature».'),
       ('Τελεστές', 'AND, OR, AND NOT. Το OR εκτελείται πριν από το AND· το AND NOT μπαίνει στο τέλος.', 'AND, OR, πάντοτε με παρενθέσεις: χωρίς αυτές, η ανάμειξή τους δεν επιστρέφει αποτελέσματα.', 'AND, OR, NOT, με κεφαλαία. Εγγύτητα: NEAR, ONEAR.', 'AND, OR, NOT, με κεφαλαία.'),
       ('Φράσεις', '<code>"…"</code> χαλαρή φράση: δέχεται πληθυντικούς και αστερίσκο. <code>{…}</code> ακριβής φράση. Μόνο ευθέα εισαγωγικά.', '<code>"…"</code> ακριβής φράση. Με καμπύλα εισαγωγικά οι λέξεις αναζητούνται χωριστά.', '<code>"…"</code> ακριβής φράση· ο αστερίσκος επιτρέπεται και μέσα της.', '<code>"…"</code> ακριβής φράση.'),
       ('Αστερίσκος', '<code>*</code> για πολλούς χαρακτήρες, <code>?</code> για έναν.', '<code>*</code> μόνο σε μεμονωμένη λέξη: όχι μέσα σε φράση, όχι μετά από ενωτικό. Οι πληθυντικοί βρίσκονται αυτόματα.', '<code>*</code> και <code>?</code>. Τουλάχιστον 3 χαρακτήρες πριν από τον αστερίσκο· έως 10 ανά αναζήτηση. Έως 25 όροι ανά παρένθεση.', 'Ελέγξτε τη βοήθεια της βάσης πριν τον χρησιμοποιήσετε.'),
       ('Χρονολογία', '<code>AND PUBYEAR &gt; 2018</code>', '<code>pubyearmin:2019</code> στο τέλος της συμβολοσειράς.', 'Φίλτρο «Year» στη σελίδα των αποτελεσμάτων.', 'Φίλτρο ημερομηνίας στη σελίδα των αποτελεσμάτων.')]
H.append(page(2, 3, 'Σύνταξη ανά βάση δεδομένων', 'Η ίδια συμβολοσειρά δεν τρέχει παντού', f'''

<table class="t syn"><tr><th></th><th>Scopus</th><th>ERIC</th><th>IEEE Xplore</th><th>ACM Digital Library</th></tr>{''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in r) + '</tr>' for r in syn)}</table>
<h2>Τρεις παγίδες, με πραγματικούς αριθμούς</h2>
<table class="t traps"><tr><th>Τι πληκτρολογήθηκε</th><th>Αποτελέσματα</th><th>Σύγκριση</th></tr>
<tr><td><code>"learning analytics" AND "self-regulat*"</code><br>Αστερίσκος μέσα σε φράση ή μετά από ενωτικό.</td><td>{Q['q_wild_in_quotes']}</td><td>{Q['q_phrase']} με <code>"self-regulated learning"</code></td></tr>
<tr><td><code>“learning analytics” AND dashboard*</code><br>Καμπύλα εισαγωγικά, από το Word.</td><td>{Q['q_curly']}</td><td>{Q['q_straight']} με ευθέα εισαγωγικά</td></tr>
<tr><td><code>dashboard* OR widget* AND "learning analytics"</code><br>Χωρίς παρενθέσεις.</td><td>{Q['p_none']}</td><td>{Q['p_or_first']} με <code>(dashboard* OR widget*) AND …</code><br>{Q['p_and_first']} με <code>dashboard* OR (widget* AND …)</code></td></tr></table>
<p class="srcl"><b>Πηγές.</b> Elsevier, Scopus Support Center· ERIC, Advanced Search Tips, και αναζητήσεις στο eric.ed.gov στις {DATE}· IEEE Xplore Help (Command Search, Search engine)· ACM Digital Library, Advanced Search. Οι βάσεις αλλάζουν: σε περίπτωση αμφιβολίας ισχύει η βοήθεια της ίδιας της βάσης.</p>''', FOOT))
H.append(page(3, 3, 'Παράδειγμα', 'Το ερώτημα της Εβδομάδας 1 στο ERIC, μπλοκ προς μπλοκ', f'''
<p>Πίνακες πληροφοριών μαθησιακής αναλυτικής και αυτορρύθμιση στην ανώτατη εκπαίδευση. Κάθε γραμμή προσθέτει ένα μπλοκ στην προηγούμενη. Αναζητήσεις στο eric.ed.gov στις {DATE}.</p>
<table class="t fn"><tr><th>Συμβολοσειρά</th><th>Όλα τα έτη</th><th>Από το 2019</th></tr>
<tr><td><code>{e(B1)}</code></td><td>{gr(Q['n1'])}</td><td></td></tr><tr><td><code>{e(B2)}</code></td><td>{gr(Q['n2'])}</td><td>{gr(Q['n2_2019'])}</td></tr>
<tr><td><code>{e(B3)}</code></td><td>{gr(Q['n3'])}</td><td>{gr(Q['n3_2019'])}</td></tr><tr><td><code>{e(B4)}</code></td><td>{gr(Q['n4'])}</td><td>{gr(Q['n4_2019'])}</td></tr></table>
<div class="note"><b>Πώς διαβάζεται.</b> Με ένα μπλοκ τα αποτελέσματα είναι πάρα πολλά· με δύο, το πλήθος είναι εφικτό· με τρία πέφτει κάτω από το όριο των 40 και με τέσσερα σχεδόν μηδενίζεται. Για μια μικρή, εξειδικευμένη βάση όπως το ERIC τα τέσσερα μπλοκ είναι υπερβολικά· η ίδια συμβολοσειρά στη Scopus δίνει πολύ περισσότερα. Η βαθμονόμηση γίνεται ξεχωριστά για κάθε βάση.</div>
<h2>Το ημερολόγιό σας, μετά από δύο εκτελέσεις</h2>
<table class="t"><tr><th>Βάση</th><th>Ημερομηνία</th><th>Συμβολοσειρά, όπως εκτελέστηκε</th><th>Φίλτρα</th><th>n</th><th>Σημειώσεις</th></tr>
<tr><td>ERIC</td><td>{DATE}</td><td><code>{e(B1 + ' ' + B2 + ' ' + B3 + ' ' + B4)} pubyearmin:2019</code></td><td>από το 2019</td><td>{Q['n4_2019']}</td><td>Πολύ στενό. Αφαιρούμε το μπλοκ της ανώτατης εκπαίδευσης· το επίπεδο θα γίνει κριτήριο ένταξης.</td></tr>
<tr><td>ERIC</td><td>{DATE}</td><td><code>{e(B1 + ' ' + B2 + ' ' + B3)} pubyearmin:2019</code></td><td>από το 2019</td><td>{Q['n3_2019']}</td><td>Ακόμη κάτω από 40. Επόμενο βήμα: περισσότερα συνώνυμα στο τρίτο μπλοκ, και εκτέλεση στη Scopus.</td></tr></table>
<div class="note"><b>Έως το επόμενο μάθημα.</b> Επαναλαμβάνετε τα αποψινά βήματα για τη δική σας ανασκόπηση. Εκτελείτε την τελική συμβολοσειρά σε δύο έως τρεις βάσεις, με την εκδοχή της καθεμιάς, και καταγράφετε κάθε εκτέλεση. Εξάγετε στο Zotero, αφαιρείτε τις διπλοεγγραφές και ολοκληρώνετε το Στάδιο 1 στο φύλλο 2_Επιλογή. Στο Μέρος 3 της Εβδομάδας 3 δουλεύουμε με τις μελέτες που θα έχετε επιλέξει.</div>''', FOOT))
open(f'{K}/out/Workshop1_handout.html', 'w', encoding='utf8').write(doc('Εργαστήριο αναζήτησης: φυλλάδιο', H))
# ---------------------------------------------------------------- teacher sheet
TF = 'Οδηγός διδάσκοντος · δεν διανέμεται στους φοιτητές'
T = []
T.append(page(1, 3, 'Οδηγός διδάσκοντος · Εβδομάδα 2, Μέρος 3', 'Πίνακες πληροφοριών και εργαστήριο αναζήτησης', f'''
<div class="sim"><b>Δύο μονάδες που δεν πρέπει να μπερδευτούν.</b> Η <b>εργασία</b> είναι ατομική ή σε δυάδα και γίνεται στο σπίτι. Το <b>εργαστήριο</b> γίνεται σε αίθουσες των τεσσάρων περίπου ατόμων, μία ομάδα ανά αίθουσα, όπως στο Εργαστήριο 1. Κάθε αίθουσα παράγει μία συμβολοσειρά, για το θέμα ενός μέλους της. Οι υπόλοιποι επαναλαμβάνουν τα βήματα για το δικό τους θέμα έως την Εβδομάδα 3, όπως ήδη προβλέπει το χρονοδιάγραμμα της Εβδομάδας 1.</div>
<h2>Ροή των 45 λεπτών</h2><table class="t run"><tr><th>Λεπτά</th><th>Διαφάνειες</th><th>Τι γίνεται</th><th>Zoom</th></tr>
<tr><td><b>0 έως 15</b></td><td>1 έως 15</td><td>Πίνακες πληροφοριών, ένα λεπτό ανά διαφάνεια. Χρονομετρημένο ερώτημα στη διαφάνεια 5 (01:00, πλήκτρο T). Παραλείψιμες: 8 και 13.</td><td>Οι απαντήσεις στο ερώτημα γράφονται στη συνομιλία. Δεν σχολιάζονται μία προς μία.</td></tr>
<tr><td><b>15 έως 21</b></td><td>16 έως 21</td><td>Ενημέρωση για το εργαστήριο: τι παράγουν, το υπόδειγμα, το φύλλο, οι παγίδες, η βαθμονόμηση, οι ρόλοι.</td><td>Βεβαιωθείτε ότι όλοι έχουν ανοιχτό το αρχείο προτύπων (έκδοση 2) και το φυλλάδιο.</td></tr>
<tr><td><b>21 έως 35</b></td><td>22</td><td>Εργασία στις αίθουσες, 14:00.</td><td>Αυτόματη κατανομή, περίπου τέσσερα άτομα ανά αίθουσα, διάρκεια 14′, αυτόματο κλείσιμο με αντίστροφη μέτρηση 60″.</td></tr>
<tr><td><b>35 έως 40</b></td><td>23</td><td>Δύο ομάδες παρουσιάζουν, 02:30 η καθεμία. «Μηδενισμός» και T πριν από τη δεύτερη.</td><td>Ο εισηγητής μοιράζεται την οθόνη με το φύλλο 1_Αναζήτηση. Οι παρατηρήσεις των υπολοίπων στη συνομιλία.</td></tr>
<tr><td><b>40 έως 45</b></td><td>24 έως 26</td><td>Τι οφείλουν έως την Εβδομάδα 3, «Να θυμάστε», ερωτήσεις. Τα τελευταία 3′ είναι το περιθώριο της βραδιάς.</td><td></td></tr></table>
<div class="two"><div class="note"><b>Μηνύματα προς όλες τις αίθουσες.</b><br>5ο λεπτό: «Έχετε εκτελέσει την πρώτη αναζήτηση; Καταγράψτε την πριν αλλάξετε οτιδήποτε.»<br>10ο λεπτό: «Τέσσερα λεπτά ακόμη: δεύτερη εκτέλεση και απόφαση.»</div>
<div class="note"><b>Ποιες ομάδες παρουσιάζουν.</b> Μία με πάρα πολλά αποτελέσματα και μία με πολύ λίγα, αν υπάρχουν: οι δύο διορθώσεις είναι αντίθετες και το μάθημα φαίνεται καθαρά. Στις αίθουσες ρωτάτε μόνο: «Ποιο μπλοκ δίνει τα περισσότερα αποτελέσματα, και γιατί;»</div></div>
<div class="note"><b>Αν η Scopus δεν ανοίγει για κανέναν,</b> όλο το εργαστήριο γίνεται στο ERIC. Τίποτε στις διαφάνειες δεν προϋποθέτει τη Scopus: το παράδειγμα της βαθμονόμησης και οι τρεις παγίδες είναι ήδη από το ERIC.</div>''', TF))
errs = [('Όλες οι έννοιες σε μία παρένθεση, με OR.', 'Χιλιάδες αποτελέσματα. «OR μόνο ανάμεσα σε συνώνυμα της ίδιας έννοιας.»'),
        ('AND ανάμεσα σε συνώνυμα.', 'Σχεδόν μηδέν αποτελέσματα. «Πρέπει το άρθρο να περιέχει και τις δύο λέξεις;»'),
        ('Ανάμειξη OR και AND χωρίς παρενθέσεις.', f"Στο ERIC: {Q['p_none']} αποτελέσματα. Στη Scopus εκτελείται πρώτα το OR. Το φύλλο βάζει τις παρενθέσεις μόνο του· το λάθος εμφανίζεται όταν γράφουν με το χέρι."),
        ('Καμπύλα εισαγωγικά από Word ή PDF.', f"Στο ERIC οι λέξεις αναζητούνται χωριστά ({Q['q_curly']} αντί για {Q['q_straight']}). Η Scopus ζητά ευθέα εισαγωγικά. Το φύλλο τα μετατρέπει."),
        ('Αστερίσκος μέσα σε φράση ή μετά από ενωτικό, στο ERIC.', f"<code>\"self-regulat*\"</code>: {Q['q_wild_in_quotes']} αποτελέσματα. Γράφουν τις παραλλαγές ολόκληρες. Το φύλλο προειδοποιεί."),
        ('Αστερίσκος πολύ νωρίς στη λέξη, όπως <code>stud*</code>.', 'Θόρυβος: study, studio, student. Η ρίζα να είναι αρκετά μακριά ώστε να ορίζει την έννοια.'),
        ('Πέμπτη έννοια «επειδή υπάρχει στο PICO».', 'Υπερβολικά στενό. Το αποτέλεσμα (outcome) και το επίπεδο εκπαίδευσης γίνονται συχνά κριτήρια ένταξης, όχι μπλοκ της συμβολοσειράς.'),
        ('NOT για να «καθαρίσουν» τα αποτελέσματα.', 'Χάνονται σχετικές μελέτες που απλώς αναφέρουν τον αποκλεισμένο όρο. Το PRESS το επισημαίνει ρητά.'),
        ('Φίλτρα χωρίς αιτιολόγηση, όπως «μόνο ανοιχτής πρόσβασης».', 'Μεροληψία στην επιλογή. Το PRISMA-S ζητά αιτιολόγηση για κάθε περιορισμό.'),
        ('Καταγράφουν μόνο την «καλή» εκτέλεση.', 'Το ημερολόγιο είναι ιστορικό: κάθε εκτέλεση, με την ημερομηνία της, όπως ακριβώς έγινε.')]
T.append(page(2, 3, 'Οδηγός διδάσκοντος', 'Πριν από τη βραδιά, και δέκα λάθη που θα δείτε', f'''
<h2>Πριν από τη βραδιά</h2><table class="t"><tr><th>Τι</th><th>Πότε</th></tr>
<tr><td>Αναρτάτε το <b>LA_review_templates_v2.xlsx</b> και το <b>Workshop1_handout.pdf</b>. Όποιος έχει αρχίσει να συμπληρώνει την έκδοση 1 αντιγράφει μόνο το φύλλο 0_Συμβολοσειρά στο αρχείο του (δεξί κλικ στην καρτέλα, «Μετακίνηση ή αντιγραφή»· στα Google Sheets, «Αντιγραφή σε υπάρχον υπολογιστικό φύλλο»).</td><td>πριν από το μάθημα</td></tr>
<tr><td>Ζητάτε να έχουν δοκιμάσει την πρόσβαση στη Scopus από το σπίτι (HEAL-Link με VPN). Όποιος δεν τα καταφέρει δουλεύει στο ERIC, που είναι ελεύθερο.</td><td>πριν από το μάθημα</td></tr>
<tr><td>Έχετε ανοιχτές δύο καρτέλες, Scopus (Advanced search) και eric.ed.gov, για την περίπτωση που χρειαστεί να δείξετε κάτι ζωντανά στην παρουσίαση των ομάδων.</td><td>στο διάλειμμα</td></tr>
<tr><td>Το <b>W2P3_student.pdf</b> μπορεί να αναρτηθεί οποτεδήποτε: δεν περιέχει λύσεις.</td><td>πριν ή μετά</td></tr></table>

<table class="t err"><tr><th>Τι θα δείτε</th><th>Τι συμβαίνει, και τι λέτε</th></tr>{''.join(f'<tr><td>{a}</td><td>{b}</td></tr>' for a, b in errs)}</table>
''', TF))
T.append(page(3, 3, 'Οδηγός διδάσκοντος', 'Από πού προέρχεται κάθε αριθμός των διαφανειών', f'''
<table class="t"><tr><th>Διαφάνεια</th><th>Αριθμοί</th><th>Πηγή</th></tr>
<tr><td>3, 10, 11, 15, 17</td><td>38 μελέτες· 78,9% πίνακες μόνο για φοιτητές· επίδοση: 14 αμελητέα, 12 μικρή, 3 μέτρια, 5 μεγάλη (34)· σχεδιασμός 57,9% / 23,7% / 15,8%· αναζήτηση: 485 + 153 + 88 + 86 = 812 εγγραφές.</td><td>Kaliisa, Misiejuk, López-Pernas, Khalil &amp; Saqr (2024), LAK '24, σσ. 295–304. Διάβασα το πλήρες κείμενο στην έκδοση arXiv 2312.15042: ενότητες 3 και 4, σχήμα 1, πίνακας 1.</td></tr>
<tr><td>9, 12</td><td>50 μελέτες από 1.968 εγγραφές· σκοπός: 33 επίγνωση, 38 ενέργεια, από τις οποίες 16 ασαφείς· 5 με θεωρητική βάση· στάδιο: 2 + 19 πρωτότυπα, 23 πιλοτικές, 6 στην τάξη· αξιολόγηση: 33, 11, 9, 11· μία πειραματική μελέτη· ιδιωτικότητα ως απαίτηση σχεδιασμού: 1.</td><td>Kaliisa, Jivet &amp; Prinsloo (2023), IJETHE, 20, 28. Πλήρες κείμενο, ανοιχτής πρόσβασης: ενότητες RQ1 έως RQ6.</td></tr>
<tr><td>13</td><td>Συχνότερο πλαίσιο αναφοράς το κοινωνικό· προτίμηση στο πλαίσιο της προόδου.</td><td>Jivet et al. (2017), από τις διαφάνειες παρουσίασης των συγγραφέων· Gallagher et al. (2024), περίληψη.</td></tr>
<tr><td>2, 7</td><td>Ορισμός· διάγραμμα επιλογής γραφήματος.</td><td>Schwendimann et al. (2017), όπως παρατίθεται, με σελίδα, στο Kaliisa et al. (2024)· Abela (2006).</td></tr>
<tr><td>19, 20</td><td>Όλα τα πλήθη του ERIC.</td><td>Αναζητήσεις στο eric.ed.gov στις {DATE}, με το σενάριο <code>workshop1/eric_counts.py</code> του πακέτου. Πριν από κάθε νέα χρονιά εκτελείται ξανά και οι διαφάνειες ενημερώνονται μόνες τους.</td></tr></table>''', TF))
open(f'{K}/out/Workshop1_teacher.html', 'w', encoding='utf8').write(doc('Εργαστήριο αναζήτησης: οδηγός διδάσκοντος', T)); print('handout + teacher html written')
