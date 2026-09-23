# NoSQL, Evening 2, Part 2: group exercise "Από την SQL στη MongoDB" -> ../content/n2p2.json
# The colleague's line (Part B, slides 35-39): study the manual's SQL-to-MongoDB page, solve in groups, present to the plenary; his optional
# exercises become the one-page sheet (e2p2_cmds.SHEET). Every number and output comes from e2p2_outputs.json (run_e2p2.py, real run).
import json, os, re
from e2p2_cmds import SHEET, CMDS
H = os.path.dirname(os.path.abspath(__file__))
O = json.load(open(os.path.join(H, 'e2p2_outputs.json'), encoding='utf8'))
S = []
def add(**k):
    assert 2 <= len(k.get('notes', [])) <= 4, (k['title'], len(k.get('notes', [])))
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
assert int(JAVA) - int(AND_) == int(JAVA_MEAP) == 1  # the one Java book not published is the Java book in MEAP (notes of slide 8)
N_ITEMS = len(SHEET)
ONE_MEAP = 'ένα' if JAVA_MEAP == '1' else JAVA_MEAP
JAVA_LC_TITLES = re.findall(r"title: '([^']*)'", O['java_lc'][0])
assert len(JAVA_LC_TITLES) == int(JAVA_LC) and "categories: [ 'java' ]" in O['java_lc'][0]
JAVASCRIPT_TITLES = re.findall(r"title: '([^']*)'", O['javascript'][0])
ROOM_MIN, ROOM_SEC, PRES_SEC, BREAK_MIN = 22, 1200, 180, 15
fmt = lambda sec: '%02d:%02d' % divmod(sec, 60)
# slide number of the install slide of Evening 2 Part 1, read from its content file (notes of slides 3 and 12)
P1 = [i + 1 for i, s in enumerate(json.load(open(os.path.join(H, '..', 'content', 'n2p1.json'), encoding='utf8'))['slides'])
      if s['title'] == 'Εγκατάσταση και εισαγωγή τώρα']
assert len(P1) == 1, P1

add(type='listslide', mins=1, title='Ομαδική άσκηση: από την SQL στη MongoDB',
    items=['Μελετήστε τη σελίδα του εγχειριδίου που αντιστοιχίζει εντολές της SQL σε εντολές της MongoDB.',
           'Σε ομάδες, λύστε τα %d ζητούμενα του φύλλου στη συλλογή books.' % N_ITEMS,
           'Παρουσιάστε τα αποτελέσματα στην ολομέλεια.'],
    foot='Όλες οι αίθουσες έχουν την ίδια άσκηση· ο καθένας δουλεύει στο δικό του mongosh.',
    notes=['**Μελετήστε τη σελίδα του εγχειριδίου**: Τη βλέπουμε στην επόμενη διαφάνεια. Κάθε ζητούμενο του φύλλου δίνεται και σε SQL· η σελίδα δείχνει πώς γράφεται ως ερώτημα της MongoDB.',
           '**λύστε τα %d ζητούμενα του φύλλου**: Αναρτήστε τώρα το φύλλο στην πλατφόρμα του μαθήματος ή στο chat του Zoom, μαζί με τον σύνδεσμο της σελίδας.' % N_ITEMS,
           '**Παρουσιάστε τα αποτελέσματα στην ολομέλεια**: Γίνεται όταν κλείσουν οι αίθουσες, πριν από τις λύσεις.',
           '**ο καθένας δουλεύει στο δικό του mongosh**: Με τη συλλογή books που εισήγαγε στο Μέρος 1.'])

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
    notes=['**SQL, πίνακας people**: Τα παραδείγματα είναι της ίδιας της σελίδας, με τον δικό της πίνακα people. Στις δύο πρώτες γραμμές, το AND γίνεται κόμμα και το OR γίνεται `$or`.',
           '**`{ age: { $gt: 25, $lte: 50 } }`**: Δύο συνθήκες στο ίδιο πεδίο: οι δύο τελεστές μπαίνουν στο ίδιο έγγραφο, όπως στο Μέρος 1.',
           '**`{ user_id: /^bc/ }`**: Το LIKE γίνεται κανονική έκφραση: το `/^bc/` σημαίνει «αρχίζει από bc», όπως το `\'bc%\'`.',
           '**Όπου γράφει `count()`, γράψτε `countDocuments()`**: Η σελίδα γράφει `db.people.count()`, που στο mongosh δίνει προειδοποίηση απόσυρσης.'])

add(type='table', mins=1, compact=True, title='Πώς δουλεύουμε',
    rows=[{'h': 'Ομάδες', 't': 'Περίπου τέσσερα άτομα σε κάθε αίθουσα του Zoom· όλες οι αίθουσες έχουν το ίδιο φύλλο.'},
          {'h': 'Εργαλείο', 't': 'Ο καθένας στο δικό του mongosh, στη βάση library: `use library`.'},
          {'h': 'Τι γράφετε', 't': 'Για κάθε ζητούμενο, το ερώτημα της MongoDB και το πλήθος των εγγράφων που επιστρέφει.'},
          {'h': 'Χρόνος', 't': '20 λεπτά στην αίθουσα· μετά δύο ομάδες παρουσιάζουν, 3 λεπτά η καθεμία.'},
          {'h': 'Χωρίς τη συλλογή', 't': 'Όποιος δεν ολοκλήρωσε την εισαγωγή, δουλεύει με την οθόνη ενός μέλους της ομάδας.'}],
    notes=['**Ομάδες**: Όλες οι αίθουσες έχουν το ίδιο φύλλο, ώστε στο τέλος να συγκρίνονται τα πλήθη.',
           '**`use library`**: Η βάση που δημιούργησε το mongoimport στο Μέρος 1. Αν μια ομάδα βρίσκει παντού 0, είναι ακόμη στη βάση test.',
           '**Τι γράφετε**, **%d λεπτά στην αίθουσα**: Είναι γραμμένα και στο φύλλο, ώστε η αίθουσα να ξέρει τι κάνει χωρίς τις διαφάνειες.' % (ROOM_SEC // 60),
           '**Χωρίς τη συλλογή**: Την εισαγωγή την ολοκληρώνει στο επόμενο διάλειμμα, με τη διαφάνεια [[p1_install]] του Μέρους 1.'])

add(type='shell', mins=2, dense=True, title='Ένα λυμένο παράδειγμα',
    sql="SELECT title, pageCount FROM books\nWHERE status = 'MEAP' AND pageCount > 0\nORDER BY pageCount DESC\nLIMIT 3", sqlLabel='SQL',
    cmd=cmd('example'), cmdLabel='MongoDB', out=out('example'), outLabel='Αποτέλεσμα',
    points=['`WHERE` γίνεται φίλτρο: το `AND` είναι το κόμμα.',
            '`SELECT title, pageCount` γίνεται προβολή.',
            '`ORDER BY … DESC` γίνεται `sort` με -1· το `LIMIT` γίνεται `limit`.'],
    notes=['**`WHERE status = \'MEAP\' AND pageCount > 0`**: Ένα ερώτημα που δεν υπάρχει στο φύλλο: τα τρία βιβλία σε MEAP με τις περισσότερες σελίδες, από όσα έχουν γνωστό αριθμό σελίδων.',
           '**`WHERE` γίνεται φίλτρο**: Το φίλτρο είναι το πρώτο όρισμα του find. Το `>` γίνεται `$gt`.',
           '**`SELECT title, pageCount` γίνεται προβολή**: Το δεύτερο όρισμα του find. Χωρίς `_id: 0` θα εμφανιζόταν και το `_id`, που η SQL δεν ζητά.',
           '**`ORDER BY … DESC` γίνεται `sort` με -1**: Η σειρά στο mongosh: find, μετά sort, μετά limit. Η σειρά γραφής των sort και limit δεν αλλάζει το αποτέλεσμα.'])

add(type='work', mins=ROOM_MIN, timerSec=ROOM_SEC, title='Στις αίθουσες',
    context='Σε κάθε αίθουσα, με το φύλλο της άσκησης:',
    items=['Ο καθένας στο δικό του mongosh: `use library`.',
           'Για κάθε ζητούμενο, το ερώτημα της MongoDB και το πλήθος, με `countDocuments` και το ίδιο φίλτρο.',
           'Ένα μέλος κρατά τις απαντήσεις της ομάδας.'],
    foot='Βοήθημα: [SQL to MongoDB Mapping Chart](https://www.mongodb.com/docs/manual/reference/sql-comparison/), στο εγχειρίδιο της MongoDB.',
    notes=['**Σε κάθε αίθουσα, με το φύλλο της άσκησης**: Ανοίξτε τις αίθουσες, με τέσσερα άτομα περίπου στην καθεμία. Τα %d λεπτά της διαφάνειας περιλαμβάνουν το άνοιγμα και το κλείσιμό τους.' % ROOM_MIN,
           '**με `countDocuments` και το ίδιο φίλτρο**: Το mongosh δείχνει τα αποτελέσματα του find 20 τη φορά· το πλήθος το δίνει το `countDocuments`.',
           '**Ένα μέλος κρατά τις απαντήσεις της ομάδας**: Τις λύσεις και τα πλήθη τα έχετε στο αρχείο απαντήσεων (N2P2_answers).',
           '**%s**: Ξεκινήστε το χρονόμετρο με το πλήκτρο T μόλις μπουν όλοι. Μηνύματα προς όλες τις αίθουσες: όταν δείχνει 10:00, «Όποιος τελείωσε έως το 10, συνεχίζει στα 11 έως 13»· όταν δείχνει 02:00, «Δύο λεπτά· σημειώστε τα πλήθη».' % fmt(ROOM_SEC)])

add(type='work', mins=6, timerSec=PRES_SEC, title='Δύο ομάδες παρουσιάζουν',
    context='Δύο ομάδες, τρία λεπτά η καθεμία:',
    items=['Η πρώτη ομάδα: τα ζητούμενα 4 έως 8, με το ερώτημα και το πλήθος.',
           'Η δεύτερη ομάδα: τα ζητούμενα 9 έως 13, με τον ίδιο τρόπο.',
           'Οι υπόλοιπες ομάδες συγκρίνουν με τα δικά τους πλήθη.'],
    # the student sheet (build_n2p2_docs.py, README v13.5) has another rule: every team presents one item in turn; the notes hold under both
    notes=['**Δύο ομάδες, τρία λεπτά η καθεμία**: Το φύλλο των φοιτητών γράφει άλλη σειρά: κάθε ομάδα παρουσιάζει ένα ζητούμενο, η πρώτη το 1, η δεύτερη το 2, ώσπου να παρουσιαστούν και τα %d. Πείτε ποια σειρά ισχύει πριν ξεκινήσει η πρώτη ομάδα.' % N_ITEMS,
           '**με το ερώτημα και το πλήθος**: Τα σωστά πλήθη είναι στο αρχείο απαντήσεων· αν ένα πλήθος διαφέρει, το ερώτημα δείχνει γιατί.',
           '**Οι υπόλοιπες ομάδες συγκρίνουν**: Αν τα πλήθη διαφέρουν, η εξήγηση βρίσκεται σχεδόν πάντα σε μία από τις επόμενες τέσσερις διαφάνειες.',
           '**%s**: Το χρονόμετρο ξεκινά με το πλήκτρο T. Για την επόμενη ομάδα: «Μηδενισμός» και ξανά T.' % fmt(PRES_SEC)])

add(type='shell', mins=2, title='Java: %s, όχι %s ούτε %s' % (JAVA, JAVA_EXACT, JAVA_IN), dense=True,
    cmd=cmd('java'), cmdLabel='Εντολές', out=out('java'), outLabel='Αποτελέσματα',
    points=['Ζητούμενο 4 (πρώτη εντολή): %s βιβλία.' % JAVA,
            'Με αγκύλες, %s: μόνο όσα έχουν ως μοναδική κατηγορία τη Java.' % JAVA_EXACT,
            'Ένα βιβλίο έχει «java» με πεζά. Αν το θέλουμε κι αυτό, `$in` και τα δύο: %s.' % JAVA_IN],
    notes=['**Ζητούμενο 4 (πρώτη εντολή): %s βιβλία**: Στην SQL του φύλλου κάθε βιβλίο έχει μία κατηγορία. Εδώ το categories είναι λίστα, και το `categories: "Java"` σημαίνει «η λίστα περιέχει τη Java».' % JAVA,
           '**Με αγκύλες, %s**: Το `["Java"]` ταιριάζει μόνο με λίστα που είναι ακριβώς `["Java"]`. Μένουν έξω τα %d βιβλία Java που έχουν και άλλη κατηγορία.' % (JAVA_EXACT, int(JAVA) - int(JAVA_EXACT)),
           '**Ένα βιβλίο έχει «java» με πεζά**: Η σύγκριση ξεχωρίζει πεζά από κεφαλαία, όπως με το «Internet» στο Μέρος 1. Με το `$in` αρκεί μία από τις δύο τιμές.',
           'Αν ρωτήσουν: ποιο βιβλίο έχει «java»; Το «%s», με μοναδική κατηγορία «java».' % JAVA_LC_TITLES[0]])

add(type='shell', mins=2, title='AND ή OR', dense=True,
    cmd=cmd('andor'), cmdLabel='Εντολές', out=out('andor'), outLabel='Αποτελέσματα',
    points=['Ζητούμενο 5, AND: %s βιβλία Java που κυκλοφόρησαν.' % AND_,
            'Ζητούμενο 6, OR: %s, δηλαδή τα %s που κυκλοφόρησαν και %s βιβλίο Java σε MEAP.' % (OR_, PUB, ONE_MEAP),
            'Το «είτε… είτε» της εκφώνησης είναι OR: αρκεί μία από τις δύο συνθήκες.'],
    notes=['**Ζητούμενο 5, AND: %s**: Το κόμμα ανάμεσα στις δύο συνθήκες είναι AND, όπως στο λυμένο παράδειγμα.' % AND_,
           '**Ζητούμενο 6, OR: %s**: Στην SQL, `WHERE category = \'Java\' OR status = \'PUBLISH\'`. Στη MongoDB, `$or` με λίστα από δύο συνθήκες.' % OR_,
           '**%s βιβλίο Java σε MEAP**: Τα %s περιέχουν ήδη τα %s βιβλία Java που κυκλοφόρησαν· το OR προσθέτει μόνο το βιβλίο Java που δεν έχει κυκλοφορήσει.' % (ONE_MEAP, PUB, AND_),
           '**Το «είτε… είτε» της εκφώνησης είναι OR**: Αν μια ομάδα βρήκε %s στο ζητούμενο 6, έγραψε AND αντί για OR.' % AND_])

add(type='shell', mins=2, skippable=True, title='Ταξινόμηση κειμένου: τα πεζά στο τέλος', dense=True,
    cmd=cmd('sortcase'), cmdLabel='Εντολές', out=out('sortcase'), outLabel='Αποτελέσματα',
    points=['Η MongoDB συγκρίνει τα κείμενα χαρακτήρα προς χαρακτήρα: όλα τα κεφαλαία πριν από τα πεζά. Το «jQuery» έρχεται μετά το «XML».',
            'Με `collation` και `locale: "en"`, η σειρά γίνεται αλφαβητική, ανεξάρτητα από πεζά και κεφαλαία.',
            'Ζητούμενο 9: στο τέλος της λίστας είναι τα %s βιβλία Java με 0 σελίδες.' % ZJ],
    src='MongoDB Manual: Comparison/Sort Order (Collation).',
    notes=['**`.sort({ title: -1 }).limit(3)`**: Φθίνουσα σειρά, ώστε να φαίνεται το τέλος της αύξουσας λίστας του ζητούμενου 8.',
           '**όλα τα κεφαλαία πριν από τα πεζά**: Γι’ αυτό, στο ζητούμενο 8, τα «iText» και «jQuery» έρχονται μετά από όλους τους τίτλους που αρχίζουν με κεφαλαίο.',
           '**Με `collation` και `locale: "en"`**: Η δεύτερη εντολή· τα «jQuery» και «iText» φεύγουν από την κορυφή. Στην SQL, η σειρά εξαρτάται από τη συρραφή (collation) της βάσης.',
           '**τα %s βιβλία Java με 0 σελίδες**: Στη φθίνουσα σειρά σελίδων το 0 πηγαίνει στο τέλος. Εδώ σημαίνει «άγνωστος αριθμός», όπως στο Μέρος 1.' % ZJ])

add(type='shell', mins=2, skippable=True, title='Κείμενο: λέξη ή κομμάτι λέξης', dense=True,
    cmd=cmd('regex'), cmdLabel='Εντολές', out=out('regex'), outLabel='Αποτελέσματα',
    points=['Ζητούμενο 11: το `/Java/` βρίσκει %s τίτλους, μαζί με JavaScript, JavaServer, JavaFX. Μόνο η λέξη Java: `\\b` πριν και μετά, %s.' % (RX_ALL, RX_WORD),
            'Ζητούμενο 12: το `/^Java/` βρίσκει %s· οι %d από αυτούς αρχίζουν με JavaServer, JavaFX, JavaScript.' % (RX_START, int(RX_START) - int(RX_START_WORD)),
            'Ζητούμενο 13: `/^.a.a/`, %s τίτλοι· η `.` της regex αντιστοιχεί στο `_` του LIKE της SQL.' % C[13]],
    src='MongoDB Manual: $regex.',
    notes=['**Ζητούμενο 11: το `/Java/` βρίσκει %s τίτλους**: Αντιστοιχεί στο `LIKE \'%%Java%%\'` του φύλλου· βρίσκει τη Java και μέσα σε άλλες λέξεις.' % RX_ALL,
           '**`\\b` πριν και μετά, %s**: Το `\\b` σημαίνει «όριο λέξης»: ανάμεσα σε γράμμα και σε κενό, σημείο στίξης ή αρχή και τέλος του τίτλου.' % RX_WORD,
           '**οι %d από αυτούς**: Είναι οι %s. Με `/^Java\\b/` μένουν %s.' % (len(JAVASCRIPT_TITLES), ', '.join('«%s»' % t for t in JAVASCRIPT_TITLES[:-1]) + ' και «%s»' % JAVASCRIPT_TITLES[-1], RX_START_WORD),
           '**η `.` της regex αντιστοιχεί στο `_` του LIKE της SQL**: Στο φύλλο, `LIKE \'_a_a%\'`. Το `^` σημαίνει «στην αρχή», όπως στο `/^bc/` της διαφάνειας [[s_page]].'])

add(type='remember', mins=1, kicker='Να θυμάστε', title='Τρία σημεία από το Μέρος 2',
    items=['SQL και MongoDB λένε το ίδιο με άλλη σύνταξη: το WHERE γίνεται φίλτρο, το SELECT προβολή, το ORDER BY sort, το LIMIT limit.',
           'Όπου η SQL θα είχε μία τιμή, η MongoDB μπορεί να έχει λίστα: εκεί η ισότητα σημαίνει «περιέχει».',
           'Τα κείμενα συγκρίνονται χαρακτήρα προς χαρακτήρα: Java, java και JavaScript δίνουν τρία διαφορετικά αποτελέσματα.'],
    notes=['**Τρία σημεία από το Μέρος 2**: Διαβάστε τα τρία σημεία, χωρίς νέα ύλη. Αν απομένει χρόνος, το διάλειμμα ξεκινά νωρίτερα.',
           '**SQL και MongoDB λένε το ίδιο με άλλη σύνταξη**: Είναι οι αντιστοιχίες της σελίδας του εγχειριδίου και του λυμένου παραδείγματος.',
           '**η ισότητα σημαίνει «περιέχει»**: Γι’ αυτό το ζητούμενο 4 δίνει %s βιβλία και όχι %s.' % (JAVA, JAVA_EXACT),
           '**Java, java και JavaScript**: Το «java» με πεζά είναι άλλη τιμή, και το `/Java/` βρίσκει και το JavaScript.'])

add(type='break', mins=2, title='Διάλειμμα',
    next='Στο Μέρος 3: ενημέρωση, διαγραφή και συνάθροιση, και η Εργασία 2 ενότητα προς ενότητα.',
    notes=['**Επιστρέφουμε σε %d′**: Αφήστε τη διαφάνεια στην οθόνη σε όλο το διάλειμμα· η αντίστροφη μέτρηση ξεκινά μόνη της.' % BREAK_MIN,
           '**Στο Μέρος 3**: Χρειάζεται ξανά η συλλογή books. Όποιος δεν ολοκλήρωσε την εισαγωγή, την ολοκληρώνει τώρα, με τη διαφάνεια [[p1_install]] του Μέρους 1.',
           '**η Εργασία 2 ενότητα προς ενότητα**: Οι ερωτήσεις για την Εργασία 2 έχουν χρόνο στο τέλος του Μέρους 3.'])

skips = [i + 1 for i, s in enumerate(S) if s.get('skippable')]
# slide numbers quoted in notes
def num(pred):
    hits = [i + 1 for i, s in enumerate(S) if pred(s)]
    assert len(hits) == 1, hits
    return hits[0]
REF = {'s_page': num(lambda s: s['title'] == 'Η σελίδα: SQL to MongoDB Mapping Chart'), 'p1_install': P1[0]}
for s in S:
    for k, v in REF.items():
        s['notes'] = [n.replace('[[%s]]' % k, str(v)) for n in s['notes']]
tot = sum(s['mins'] for s in S)
assert tot == 45, tot
assert len(skips) == 2, skips
assert not any(s['type'] == 'poll' for s in S)
for s in S:
    assert '[[' not in json.dumps(s, ensure_ascii=False).replace('rows": [[', ''), s['title']
D = {'meta': {'course': 'Βάσεις Δεδομένων & Ανάλυση Δεδομένων Μάθησης', 'deckTitle': 'Ομαδική άσκηση: από την SQL στη MongoDB',
              'part': 'Μη σχεσιακές βάσεις, Βραδιά 2, Μέρος 2', 'start': '19:15', 'lengthMin': 45, 'breakMin': BREAK_MIN, 'lang': 'el',
              'notesMarkup': True},
     'slides': S}
json.dump(D, open(os.path.join(H, '..', 'content', 'n2p2.json'), 'w', encoding='utf8'), ensure_ascii=False, indent=1)
print('slides', len(S), 'minutes', tot, 'skippable', skips)
