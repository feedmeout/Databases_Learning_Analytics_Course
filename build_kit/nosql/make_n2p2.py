# NoSQL, Evening 2, Part 2: group exercise "Από την SQL στη MongoDB" -> ../content/n2p2.json
# The colleague's line (Part B, slides 35-39): study the manual's SQL-to-MongoDB page, solve in groups, present to the plenary; his optional
# exercises become the one-page sheet (e2p2_cmds.SHEET). Every number and output comes from e2p2_outputs.json (run_e2p2.py, real run).
import json, os
from e2p2_cmds import SHEET, CMDS
H = os.path.dirname(os.path.abspath(__file__))
O = json.load(open(os.path.join(H, 'e2p2_outputs.json'), encoding='utf8'))
S = []
def add(**k):
    assert 2 <= len(k.get('notes', [])) <= 3, (k['title'], len(k.get('notes', [])))
    S.append(k)
cmd = lambda key: '\n'.join(CMDS[key])
out = lambda key: '\n'.join(x for x in O[key] if x != '')
C = {q['n']: (O['q%d_count' % q['n']][0] if q['count'] else None) for q in SHEET}
JAVA, JAVA_EXACT, JAVA_LC, JAVA_IN = O['java']
AND_, OR_, PUB, JAVA_MEAP = O['andor']
RX_ALL, RX_WORD, RX_START, RX_START_WORD = O['regex']
ZJ = O['zeros_java'][0]
assert C[4] == JAVA and C[5] == AND_ and C[6] == OR_ and int(OR_) == int(PUB) + int(JAVA_MEAP) and C[11] == RX_ALL and C[12] == RX_START
assert int(RX_START) - int(RX_START_WORD) == O['javascript'][0].count("title:")
N_ITEMS = len(SHEET)

add(type='listslide', mins=1, title='Ομαδική άσκηση: από την SQL στη MongoDB',
    items=['Μελετήστε τη σελίδα του εγχειριδίου που αντιστοιχίζει εντολές της SQL σε εντολές της MongoDB.',
           'Σε ομάδες, λύστε τα %d ζητούμενα του φύλλου στη συλλογή books.' % N_ITEMS,
           'Παρουσιάστε τα αποτελέσματα στην ολομέλεια.'],
    foot='Όλες οι αίθουσες έχουν την ίδια άσκηση· ο καθένας δουλεύει στο δικό του mongosh.',
    notes=['Η ομαδική άσκηση του παλαιότερου υλικού, όπως ήταν: μελέτη της σελίδας σύγκρισης SQL και MongoDB, ομάδες, παρουσίαση στην ολομέλεια. Οι προαιρετικές του ασκήσεις είναι τώρα τα %d ζητούμενα του φύλλου.' % N_ITEMS,
           'Αναρτήστε τώρα το φύλλο στην πλατφόρμα του μαθήματος ή μοιραστείτε το στο chat του Zoom, μαζί με τον σύνδεσμο της σελίδας της επόμενης διαφάνειας.'])

add(type='htable', mins=2, compact=True, title='Η σελίδα: SQL to MongoDB Mapping Chart',
    head=['SQL, πίνακας people', 'MongoDB, συλλογή people'],
    rows=[["`WHERE status = 'A' AND age = 50`", '`{ status: "A", age: 50 }`'],
          ["`WHERE status = 'A' OR age = 50`", '`{ $or: [ { status: "A" }, { age: 50 } ] }`'],
          ['`WHERE age > 25 AND age <= 50`', '`{ age: { $gt: 25, $lte: 50 } }`'],
          ["`WHERE user_id LIKE 'bc%'`", '`{ user_id: /^bc/ }`'],
          ['`SELECT user_id, status`', '`{ user_id: 1, status: 1, _id: 0 }`, δεύτερο όρισμα του find'],
          ['`ORDER BY user_id DESC`', '`.sort({ user_id: -1 })`'],
          ['`LIMIT 5 SKIP 10`', '`.limit(5).skip(10)`'],
          ['`SELECT COUNT(*) FROM people`', '`db.people.countDocuments()`']],
    foot='[Η σελίδα στο εγχειρίδιο](https://www.mongodb.com/docs/manual/reference/sql-comparison/). Όπου γράφει `count()`, γράψτε `countDocuments()`.',
    src='MongoDB Manual: SQL to MongoDB Mapping Chart (mongodb.com/docs/manual/reference/sql-comparison).',
    notes=['Παραδείγματα της ίδιας της σελίδας, με τον πίνακα people που χρησιμοποιεί. Στην SQL εδώ τα κείμενα γράφονται με απλά εισαγωγικά, όπως στο πρότυπο.',
           'Η σελίδα γράφει ακόμη db.people.count() για το SELECT COUNT(*): στο σημερινό mongosh εμφανίζεται προειδοποίηση απόσυρσης.',
           'Το παλαιότερο υλικό έδινε τη διεύθυνση docs.mongodb.com· η σημερινή είναι mongodb.com/docs.'])

add(type='table', mins=1, compact=True, title='Πώς δουλεύουμε',
    rows=[{'h': 'Ομάδες', 't': 'Περίπου τέσσερα άτομα σε κάθε αίθουσα του Zoom· όλες οι αίθουσες έχουν το ίδιο φύλλο.'},
          {'h': 'Εργαλείο', 't': 'Ο καθένας στο δικό του mongosh, στη βάση library: `use library`.'},
          {'h': 'Τι γράφετε', 't': 'Για κάθε ζητούμενο, το ερώτημα της MongoDB και το πλήθος των εγγράφων που επιστρέφει.'},
          {'h': 'Χρόνος', 't': '20 λεπτά στην αίθουσα· μετά δύο ομάδες παρουσιάζουν, 3 λεπτά η καθεμία.'},
          {'h': 'Χωρίς τη συλλογή', 't': 'Όποιος δεν ολοκλήρωσε την εισαγωγή, δουλεύει με την οθόνη ενός μέλους της ομάδας.'}],
    notes=['Οι ίδιοι χρόνοι είναι γραμμένοι και στο φύλλο, ώστε κάθε αίθουσα να ξέρει τι κάνει χωρίς τις διαφάνειες.',
           'Μία αίθουσα ανά ομάδα, όπως στα εργαστήρια της Μαθησιακής Αναλυτικής.'])

add(type='shell', mins=2, dense=True, title='Ένα λυμένο παράδειγμα',
    sql="SELECT title, pageCount FROM books\nWHERE status = 'MEAP' AND pageCount > 0\nORDER BY pageCount DESC\nLIMIT 3", sqlLabel='SQL',
    cmd=cmd('example'), cmdLabel='MongoDB', out=out('example'), outLabel='Αποτέλεσμα',
    points=['`WHERE` γίνεται φίλτρο: το `AND` είναι το κόμμα.',
            '`SELECT title, pageCount` γίνεται προβολή.',
            '`ORDER BY … DESC` γίνεται `sort` με -1· το `LIMIT` γίνεται `limit`.'],
    notes=['Ένα ερώτημα που δεν υπάρχει στο φύλλο: βιβλία σε MEAP με γνωστό αριθμό σελίδων, τα τρία μεγαλύτερα.',
           'Η σειρά μέσα στο mongosh: find(φίλτρο, προβολή), μετά sort, μετά limit. Η σειρά γραφής των sort και limit δεν αλλάζει το αποτέλεσμα.'])

add(type='work', mins=22, timerSec=1200, title='Στις αίθουσες',
    context='Σε κάθε αίθουσα, με το φύλλο της άσκησης:',
    items=['Ο καθένας στο δικό του mongosh: `use library`.',
           'Για κάθε ζητούμενο, το ερώτημα της MongoDB και το πλήθος, με `countDocuments` και το ίδιο φίλτρο.',
           'Ένα μέλος κρατά τις απαντήσεις της ομάδας.'],
    foot='Βοήθημα: [SQL to MongoDB Mapping Chart](https://www.mongodb.com/docs/manual/reference/sql-comparison/), στο εγχειρίδιο της MongoDB.',
    notes=['Ανοίξτε τις αίθουσες (ομάδες των τεσσάρων περίπου) και ξεκινήστε το χρονόμετρο (πλήκτρο T) μόλις μπουν όλοι. Τα 22 λεπτά της διαφάνειας περιλαμβάνουν το άνοιγμα και το κλείσιμο των αιθουσών.',
           'Μηνύματα προς όλες τις αίθουσες: στο 10ό λεπτό «Όποιος τελείωσε έως το 10, συνεχίζει στα 11 έως 13»· στο 18ο «Δύο λεπτά· σημειώστε τα πλήθη».',
           'Οι απαντήσεις είναι στο αρχείο απαντήσεων (N2P2_answers).'])

add(type='work', mins=6, timerSec=180, title='Δύο ομάδες παρουσιάζουν',
    context='Δύο ομάδες, τρία λεπτά η καθεμία:',
    items=['Η πρώτη ομάδα: τα ζητούμενα 4 έως 8, με το ερώτημα και το πλήθος.',
           'Η δεύτερη ομάδα: τα ζητούμενα 9 έως 13, με τον ίδιο τρόπο.',
           'Οι υπόλοιπες ομάδες συγκρίνουν με τα δικά τους πλήθη.'],
    notes=['Επιλέξτε δύο αίθουσες. Για τη δεύτερη ομάδα: μηδενισμός και νέα έναρξη του χρονομέτρου.',
           'Αν τα πλήθη διαφέρουν, η εξήγηση βρίσκεται σχεδόν πάντα σε μία από τις επόμενες τέσσερις διαφάνειες.'])

add(type='shell', mins=2, title='Java: %s, όχι %s ούτε %s' % (JAVA, JAVA_EXACT, JAVA_IN), dense=True,
    cmd=cmd('java'), cmdLabel='Εντολές', out=out('java'), outLabel='Αποτελέσματα',
    points=['Ζητούμενο 4 (πρώτη εντολή): %s βιβλία.' % JAVA,
            'Με αγκύλες, %s: μόνο όσα έχουν ως μοναδική κατηγορία τη Java.' % JAVA_EXACT,
            'Ένα βιβλίο έχει «java» με πεζά. Αν το θέλουμε κι αυτό, `$in` και τα δύο: %s.' % JAVA_IN],
    notes=['Στην SQL του φύλλου, με μία κατηγορία ανά βιβλίο, το category = \'Java\' είναι ακριβής ταύτιση· εδώ το categories είναι λίστα και η ισότητα σημαίνει «περιέχει».',
           'Οι λύσεις του παλαιότερου υλικού για τα ζητούμενα 4 και 5 είχαν τυπογραφικά εισαγωγικά (“Java”): το mongosh απαντά %s' % O['curly'],
           'Το db.books.count() του ζητούμενου 1 λειτουργεί με προειδοποίηση απόσυρσης· σωστά db.books.countDocuments().'])

add(type='shell', mins=2, title='AND ή OR', dense=True,
    cmd=cmd('andor'), cmdLabel='Εντολές', out=out('andor'), outLabel='Αποτελέσματα',
    points=['Ζητούμενο 5, AND: %s βιβλία Java που κυκλοφόρησαν.' % AND_,
            'Ζητούμενο 6, OR: %s, δηλαδή τα %s που κυκλοφόρησαν και %s βιβλίο Java σε MEAP.' % (OR_, PUB, 'ένα' if JAVA_MEAP == '1' else JAVA_MEAP),
            'Το «είτε… είτε» της εκφώνησης είναι OR: αρκεί μία από τις δύο συνθήκες.'],
    notes=['Αν μια ομάδα βρήκε %s στο ζητούμενο 6, έγραψε AND αντί για OR.' % AND_,
           'Στην SQL: WHERE category = \'Java\' OR status = \'PUBLISH\'.'])

add(type='shell', mins=2, skippable=True, title='Ταξινόμηση κειμένου: τα πεζά στο τέλος', dense=True,
    cmd=cmd('sortcase'), cmdLabel='Εντολές', out=out('sortcase'), outLabel='Αποτελέσματα',
    points=['Η MongoDB συγκρίνει τα κείμενα χαρακτήρα προς χαρακτήρα: όλα τα κεφαλαία πριν από τα πεζά. Το «jQuery» έρχεται μετά το «XML».',
            'Με `collation` και `locale: "en"`, η σειρά γίνεται αλφαβητική, ανεξάρτητα από πεζά και κεφαλαία.',
            'Ζητούμενο 9: στο τέλος της λίστας είναι τα %s βιβλία Java με 0 σελίδες.' % ZJ],
    src='MongoDB Manual: Comparison/Sort Order (Collation).',
    notes=['Οι δύο εντολές ταξινομούν φθίνουσα (-1), ώστε να φαίνεται το τέλος της αύξουσας λίστας του ζητούμενου 8.',
           'Στην SQL, η σειρά εξαρτάται από τη συρραφή (collation) της βάσης· γι’ αυτό το ίδιο ORDER BY μπορεί να δώσει άλλη σειρά από τη MongoDB.'])

add(type='shell', mins=2, skippable=True, title='Κείμενο: λέξη ή κομμάτι λέξης', dense=True,
    cmd=cmd('regex'), cmdLabel='Εντολές', out=out('regex'), outLabel='Αποτελέσματα',
    points=['Ζητούμενο 11: το `/Java/` βρίσκει %s τίτλους, μαζί με JavaScript, JavaServer, JavaFX. Μόνο η λέξη Java: `\\b` πριν και μετά, %s.' % (RX_ALL, RX_WORD),
            'Ζητούμενο 12: το `/^Java/` βρίσκει %s· οι %d από αυτούς αρχίζουν με JavaServer, JavaFX, JavaScript.' % (RX_START, int(RX_START) - int(RX_START_WORD)),
            'Ζητούμενο 13: `/^.a.a/`, %s τίτλοι· η `.` της regex αντιστοιχεί στο `_` του LIKE της SQL.' % C[13]],
    src='MongoDB Manual: $regex.',
    notes=['Στην SQL το ζητούμενο 13 γράφεται LIKE \'_a_a%\'. Το \\b σημαίνει «όριο λέξης»: ανάμεσα σε γράμμα και σε κενό, σημείο στίξης ή αρχή και τέλος του κειμένου.',
           'Οι τρεις τίτλοι που αρχίζουν από Java χωρίς να είναι η λέξη Java: %s.' % ', '.join(l.split("'")[1] for l in O['javascript'][0].split('\n') if 'title' in l)])

add(type='remember', mins=1, kicker='Να θυμάστε', title='Τρία σημεία από το Μέρος 2',
    items=['SQL και MongoDB λένε το ίδιο με άλλη σύνταξη: το WHERE γίνεται φίλτρο, το SELECT προβολή, το ORDER BY sort, το LIMIT limit.',
           'Όπου η SQL θα είχε μία τιμή, η MongoDB μπορεί να έχει λίστα: εκεί η ισότητα σημαίνει «περιέχει».',
           'Τα κείμενα συγκρίνονται χαρακτήρα προς χαρακτήρα: Java, java και JavaScript δίνουν τρία διαφορετικά αποτελέσματα.'],
    notes=['Διαβάστε τα τρία σημεία. Τίποτε άλλο.',
           'Αν απομένει χρόνος, δεν προστίθεται ύλη· το διάλειμμα ξεκινά νωρίτερα.'])

add(type='break', mins=2, title='Διάλειμμα',
    next='Στο Μέρος 3: ενημέρωση, διαγραφή και συνάθροιση, και η Εργασία 2 ενότητα προς ενότητα.',
    notes=['Σταματήστε ακριβώς στην ώρα. Αν χρειαστεί χρόνος, παραλείπονται οι διαφάνειες [[skips]].',
           'Αφήστε τη διαφάνεια στην οθόνη σε όλο το διάλειμμα: η αντίστροφη μέτρηση δείχνει πότε ξεκινάμε.'])

skips = [i + 1 for i, s in enumerate(S) if s.get('skippable')]
S[-1]['notes'][0] = S[-1]['notes'][0].replace('[[skips]]', ' και '.join(map(str, skips)))
tot = sum(s['mins'] for s in S)
assert tot == 45, tot
assert len(skips) == 2, skips
assert not any(s['type'] == 'poll' for s in S)
for s in S:
    assert '[[' not in json.dumps(s, ensure_ascii=False).replace('rows": [[', ''), s['title']
D = {'meta': {'course': 'Βάσεις Δεδομένων & Ανάλυση Δεδομένων Μάθησης', 'deckTitle': 'Ομαδική άσκηση: από την SQL στη MongoDB',
              'part': 'Μη σχεσιακές βάσεις, Βραδιά 2, Μέρος 2', 'start': '19:15', 'lengthMin': 45, 'breakMin': 15, 'lang': 'el'},
     'slides': S}
json.dump(D, open(os.path.join(H, '..', 'content', 'n2p2.json'), 'w', encoding='utf8'), ensure_ascii=False, indent=1)
print('slides', len(S), 'minutes', tot, 'skippable', skips)
