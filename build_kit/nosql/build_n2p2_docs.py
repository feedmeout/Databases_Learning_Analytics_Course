"""NoSQL Evening 2, Part 2: out/N2P2_sheet.html (one A4 page, for the rooms) and out/N2P2_answers.html (two A4 pages, lecturer only).
Every query and result comes from nosql/e2p2_cmds.py and nosql/e2p2_outputs.json (run_e2p2.py, real run). PDF: python3 lab1/topdf.py <html> <pdf>."""
import json, os, re, html, sys
HERE = os.path.dirname(os.path.abspath(__file__)); K = os.path.join(HERE, '..'); e = html.escape
sys.path.insert(0, HERE)
from e2p2_cmds import SHEET, CMDS
O = json.load(open(f'{HERE}/e2p2_outputs.json', encoding='utf8'))
CSS = re.search(r"CSS = '''(.*?)'''", open(f'{K}/lab1/build_pack.py', encoding='utf8').read(), re.S).group(1)
CSS += '''
body{font-size:9.2pt;line-height:1.35}.page{padding:11mm 14mm 9mm}.content{gap:2mm}header{margin-bottom:3mm;padding-bottom:2mm}h1{font-size:15.5pt}h2{font-size:10.8pt;margin:1.6mm 0 .8mm}
code,.mono{font-family:ui-monospace,Menlo,Consolas,monospace}code{font-size:7.9pt;background:var(--mist);padding:.15mm 1mm;border-radius:1mm}
p.lead{font-size:9.4pt;line-height:1.35;text-align:justify;margin:0}.note{background:var(--mist);border-radius:2mm;padding:1.8mm 2.8mm;font-size:8.5pt;line-height:1.3;text-align:justify}
.t td{font-size:8.4pt;padding:1mm 1.6mm;line-height:1.26}.t th{padding:1.1mm 1.6mm;font-size:8.2pt}
.t.ns td{height:13.6mm;vertical-align:middle}.t.ns td:first-child{width:5%;font-weight:800;color:var(--deep);text-align:center}.t.ns td:nth-child(2){width:27%}.t.ns td:nth-child(3){width:30%}
.t.ns td:nth-child(3) .mono{font-size:7.7pt;line-height:1.25}.t.ns td:nth-child(4){width:29%}.t.ns td:nth-child(5){width:9%}.t.ns td:nth-child(4),.t.ns td:nth-child(5){border-left:.6pt solid var(--line)}
.t.na td{padding:.9mm 1.4mm;font-size:8pt;line-height:1.24;vertical-align:top}.t.na td:first-child{width:4%;font-weight:800;color:var(--deep);text-align:center}.t.na td:nth-child(2){width:41%}
.t.na td:nth-child(2) .mono{font-size:7.3pt;line-height:1.22;white-space:pre-wrap;word-break:break-word}.t.na td:nth-child(3){width:26%}.t.na td:nth-child(4){width:29%;color:var(--body)}
.t.run td{font-size:8.3pt;padding:.9mm 1.5mm}.t.run td:first-child{width:11%;font-weight:700;white-space:nowrap}.t.run td:nth-child(2){width:11%}
ul.chg{margin-left:4mm}ul.chg li{margin-bottom:.8mm;font-size:8.5pt;line-height:1.3;text-align:justify}.srcl{font-size:7.6pt;line-height:1.26;color:var(--muted);text-align:justify}
footer{font-size:7.7pt;white-space:nowrap}
'''
COURSE = 'Βάσεις Δεδομένων & Ανάλυση Δεδομένων Μάθησης'
def doc(title, pages): return f'<!DOCTYPE html><html lang="el"><head><meta charset="UTF-8"><title>{e(title)}</title><link href="https://fonts.googleapis.com/css2?family=Commissioner:wght@400;500;700;800&display=swap" rel="stylesheet"><style>{CSS}</style></head><body>{"".join(pages)}</body></html>'
def page(kick, title, body, left, right): return f'<section class="page"><header><span class="kick">{e(kick)}</span><h1>{e(title)}</h1></header><div class="content">{body}</div><footer><span>{e(left)}</span><span>{e(right)}</span></footer></section>'
def tbl(cls, head, rows): return f'<table class="t {cls}"><tr>' + ''.join(f'<th>{h}</th>' for h in head) + '</tr>' + ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in r) + '</tr>' for r in rows) + '</table>'
titles = lambda s: re.findall(r"title: '([^']*)'", s)
pages_ = lambda s: re.findall(r'pageCount: (\d+)', s)
N = len(SHEET)
C = {q['n']: (O['q%d_count' % q['n']][0] if q['count'] else None) for q in SHEET}

# ------------------------------------------------------------------ student sheet (one page)
lead = ('<p class="lead">Δουλεύετε σε ομάδες των τεσσάρων περίπου ατόμων, κάθε ομάδα στη δική της αίθουσα του Zoom, για <b>20 λεπτά</b>. '
        'Ο καθένας εκτελεί τα ερωτήματα στο δικό του mongosh, αφού πρώτα επιλέξει τη βάση library με την εντολή <code>use library</code>. '
        'Για κάθε ζητούμενο γράψτε στον πίνακα το ερώτημα της MongoDB και πόσα έγγραφα επιστρέφει· το πλήθος το βρίσκετε με την '
        '<code>countDocuments</code>, με το ίδιο φίλτρο.</p>'
        f'<p class="lead">Στο τέλος, οι ομάδες παρουσιάζουν στην ολομέλεια με τη σειρά, ένα ζητούμενο η καθεμία: η πρώτη ομάδα το 1, '
        f'η δεύτερη το 2 και ούτω καθεξής, ώσπου να παρουσιαστούν και τα {N}.</p>')
note = ('<b>Βοήθημα:</b> η σελίδα <a href="https://www.mongodb.com/docs/manual/reference/sql-comparison/">SQL to MongoDB Mapping Chart</a> '
        'του εγχειριδίου της MongoDB. Όπου η σελίδα χρησιμοποιεί την <code>count()</code>, χρησιμοποιήστε την <code>countDocuments()</code>. '
        'Η στήλη SQL γράφει κάθε ζητούμενο σαν να είχε κάθε βιβλίο μία μόνο κατηγορία (category)· στη MongoDB το πεδίο λέγεται categories και είναι λίστα.')
rows = [[str(q['n']), e(q['task']), f'<span class="mono">{e(q["sql"])}</span>', '', ''] for q in SHEET]
sheet_body = f'{lead}<div class="note">{note}</div>' + tbl('ns', ['#', 'Ζητούμενο', 'SQL', 'Ερώτημα στη MongoDB', 'Πλήθος'], rows)
open(f'{K}/out/N2P2_sheet.html', 'w', encoding='utf8').write(doc('Ομαδική άσκηση · Φύλλο', [page(
    'Μη σχεσιακές βάσεις · Βραδιά 2 · Μέρος 2 · Ομαδική άσκηση', f'Από την SQL στη MongoDB: {N} ζητούμενα στη συλλογή books',
    sheet_body, COURSE, 'NoSQL, Βραδιά 2')]))

# ------------------------------------------------------------------ answers (two pages)
def result(q):
    n = q['n']; show = O.get('q%d_show' % n, [None])[0]
    if n == 1: return f'<b>{O["q1_find"][0]}</b>'
    if n == 2: return f'<b>{C[2]}</b> έγγραφα· το mongosh δείχνει 20 τη φορά, με <code>it</code> τα επόμενα.'
    if n == 3: return f'<b>{C[3]}</b> έγγραφα· π.χ. <span class="mono">{e(" ".join(show.split(chr(10))[1].split()).rstrip(","))}</span>'
    if n in (8, 13): return f'<b>{C[n]}</b>· πρώτοι τίτλοι: ' + ' · '.join(e(t) for t in titles(show)) + ' …'
    if n == 9: return f'<b>{C[9]}</b>· πρώτα: ' + ' · '.join(f'{e(t)} ({p})' for t, p in zip(titles(show), pages_(show))) + ' …'
    if n == 10: return ' · '.join(f'{e(t)} ({p})' for t, p in zip(titles(show), pages_(show)))
    return f'<b>{C[n]}</b>'
JAVA, JAVA_EXACT, JAVA_LC, JAVA_IN = O['java']; AND_, OR_, PUB, JM = O['andor']; RXA, RXW, RXS, RXSW = O['regex']
warn = {1: 'Το <code>count()</code> του παλαιότερου υλικού δίνει προειδοποίηση απόσυρσης.',
        2: 'Κανένα φίλτρο: όλη η συλλογή.',
        3: 'Το <code>_id</code> εμφανίζεται και χωρίς <code>_id: 1</code>.',
        4: f'Με αγκύλες, <code>["Java"]</code>: {JAVA_EXACT}. Με πεζά, «java»: {JAVA_LC} ακόμη βιβλίο ({JAVA_IN} μαζί, με <code>$in</code>).',
        5: 'Η λύση του παλαιότερου υλικού είχε τυπογραφικά εισαγωγικά: ' + e(O['curly']) + '.',
        6: f'{OR_} = {PUB} που κυκλοφόρησαν + {JM} βιβλίο Java σε MEAP. Με AND: {AND_}.',
        7: 'Χωρίς <code>_id: 0</code> εμφανίζεται και το <code>_id</code>.',
        8: 'Τίτλοι με πεζό πρώτο γράμμα (jQuery, iText) έρχονται στο τέλος· με <code>collation({ locale: "en" })</code> αλφαβητικά.',
        9: f'Στο τέλος {O["zeros_java"][0]} βιβλία Java με 0 σελίδες (άγνωστος αριθμός).',
        10: 'Με <code>sort({ pageCount: 1 })</code> θα έβγαιναν πρώτα τα βιβλία με 0 σελίδες.',
        11: f'Περιλαμβάνει JavaScript, JavaServer, JavaFX. Μόνο η λέξη: <code>/\\bJava\\b/</code>, {RXW}.',
        12: f'Με <code>/^Java\\b/</code>: {RXSW}.',
        13: "Στην SQL το <code>_</code> του <code>LIKE '_a_a%'</code> είναι η <code>.</code> της regex."}
arows = [[str(q['n']), f'<span class="mono">{e(q["find"])}</span>', result(q), warn[q['n']]] for q in SHEET]
a1 = (''
      + tbl('na', ['#', 'Λύση', 'Αποτέλεσμα', 'Προσοχή'], arows))
test0 = O.get('in_test', None)
a2 = ('<h2 style="margin-top:0">Μέρος 2, λεπτό προς λεπτό</h2>' + tbl('run', ['Λεπτά', 'Διαφάνεια', 'Τι γίνεται'], [
      ['0–1', '1', 'Ο στόχος, όπως τον έθετε το παλαιότερο υλικό. Αναρτήστε το φύλλο στην πλατφόρμα ή στο chat.'],
      ['1–3', '2', 'Η σελίδα SQL to MongoDB Mapping Chart, με τα δικά της παραδείγματα· όπου γράφει <code>count()</code>, ισχύει το <code>countDocuments()</code>.'],
      ['3–4', '3', 'Πώς δουλεύουμε: ομάδες των τεσσάρων, ίδιο φύλλο, το δικό του mongosh ο καθένας.'],
      ['4–6', '4', 'Λυμένο παράδειγμα, εκτός φύλλου: βιβλία MEAP με γνωστό αριθμό σελίδων.'],
      ['6–28', '5', 'Αίθουσες. Χρονόμετρο 20:00 μόλις μπουν όλοι. Μηνύματα: στο 10ό λεπτό «όποιος τελείωσε έως το 10, συνεχίζει στα 11 έως 13»· στο 18ο «δύο λεπτά, σημειώστε τα πλήθη».'],
      ['28–34', '6', f'Όλες οι ομάδες, με τη σειρά, ένα ζητούμενο κάθε φορά, ώσπου να παρουσιαστούν και τα {N}· ένα χρονόμετρο 06:00 για όλο τον γύρο. Οι άλλες συγκρίνουν πλήθη.'],
      ['34–42', '7–10', 'Οι λύσεις εκεί όπου γίνονται τα λάθη: Java και java, AND και OR, πεζά στην ταξινόμηση, λέξη ή κομμάτι λέξης. Οι 9 και 10 παραλείπονται αν πιέζει ο χρόνος.'],
      ['42–43', '11', 'Να θυμάστε.'],
      ['43–45', '12', 'Διάλειμμα· τα 2 λεπτά είναι το περιθώριο του μέρους.']])
      + '<h2>Αν μια ομάδα κολλήσει</h2><ul class="chg">'
      + f'<li><b>Όλα τα πλήθη 0:</b> η ομάδα είναι στη βάση test, όχι στη library· <code>use library</code>. Στη βάση test, το <code>db.books.countDocuments()</code> δίνει {O["q1_in_test"][0]}.</li>'
      + '<li><b>Κάποιος δεν έχει τη συλλογή:</b> δουλεύει με την οθόνη ενός μέλους της ομάδας και ολοκληρώνει την εισαγωγή στο επόμενο διάλειμμα (διαφάνεια 4 του Μέρους 1).</li>'
      + f'<li><b>Διαφορετικά πλήθη στα 4 έως 6:</b> αγκύλες γύρω από το "Java" ({JAVA_EXACT}), ή AND αντί για OR ({AND_}).</li></ul>'
      + '<h2>Τι άλλαξε σε σχέση με το παλαιότερο υλικό</h2><ul class="chg">'
      + '<li><code>db.books.count()</code> → <code>db.books.countDocuments()</code>: το <code>count()</code> έχει αποσυρθεί και δίνει προειδοποίηση.</li>'
      + f'<li>Οι λύσεις των ζητούμενων 4 και 5 είχαν τυπογραφικά εισαγωγικά (“Java”), και στο 4 έλειπε και το κλείσιμο: το mongosh απαντά <span class="mono">{e(O["curly"])}</span>. Εδώ με απλά εισαγωγικά.</li>'
      + '<li>«ταξινομημένα κατά φθίνουσα σειρά βιβλίων» → «κατά φθίνουσα σειρά σελίδων»: το ζητούμενο 9 ζητά τον αριθμό σελίδων.</li>'
      + '<li>Διατύπωση: «έχουν έχουν», «έχουν ξεκινούν» και «δημοσιευμένα» → «έχουν», «αρχίζουν», «έχουν κυκλοφορήσει (status PUBLISH)».</li>'
      + '<li>Κάθε ζητούμενο έχει και τη μορφή του στην SQL, ώστε η ομαδική άσκηση με τη σελίδα σύγκρισης και οι ασκήσεις να γίνονται μαζί. Η διεύθυνση docs.mongodb.com είναι σήμερα mongodb.com/docs.</li></ul>'
      + '<p class="srcl">Πηγές: MongoDB Manual, SQL to MongoDB Mapping Chart· Query an Array· $regex· Comparison/Sort Order (collation)· db.collection.count().</p>')
foot = lambda n: f'Οδηγός διδάσκοντος · δεν διανέμεται στους φοιτητές'
open(f'{K}/out/N2P2_answers.html', 'w', encoding='utf8').write(doc('Ομαδική άσκηση · Απαντήσεις', [
    page('Μη σχεσιακές βάσεις · Βραδιά 2 · Μέρος 2 · Απαντήσεις', 'Οι λύσεις του φύλλου', a1, foot(1), 'NoSQL, Βραδιά 2 · σελίδα 1 από 2'),
    page('Μη σχεσιακές βάσεις · Βραδιά 2 · Μέρος 2 · Απαντήσεις', 'Η ροή του Μέρους 2 και οι αλλαγές', a2, foot(2), 'NoSQL, Βραδιά 2 · σελίδα 2 από 2')]))
print('N2P2_sheet.html and N2P2_answers.html written')
