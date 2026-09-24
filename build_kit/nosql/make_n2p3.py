# NoSQL, Evening 2, Part 3: "Ενημέρωση, διαγραφή και συνάθροιση" -> ../content/n2p3.json
# Follows the colleague's Part B slides 19-26 (updateOne/$set, $unset, $group total population, the aggregation pipeline, the persons
# example from Practical MongoDB Aggregations, deleteOne), updated. Commands: e2p3_cmds.py; outputs: e2p3_outputs.json (run_e2p3.py, real run).
import json, os, re
from e2p3_cmds import PANES
H = os.path.dirname(os.path.abspath(__file__))
O = json.load(open(os.path.join(H, 'e2p3_outputs.json'), encoding='utf8'))
P = dict(PANES)
S = []
def add(**k):
    assert 2 <= len(k.get('notes', [])) <= 4, (k['title'], len(k.get('notes', [])))
    S.append(k)
cmd = lambda key, idx=None: '\n'.join(P[key] if idx is None else [P[key][i] for i in idx])
out = lambda key, idx=None: '\n'.join(x for x in (O[key] if idx is None else [O[key][i] for i in idx]) if x != '')
num = lambda s: re.findall(r'(\w+Count): (\d+)', s)
gr = lambda n: f'{int(n):,}'.replace(',', '.')
TOTAL = re.search(r'totalPopulation: (\d+)', O['agg_total'][0]).group(1)
ZEROS = O['upd_many_books'][2]
assert dict(num(O['upd_many_founder'][0]))['matchedCount'] == '2' and O['count_first'][0] == '1' and 'requires atomic operators' in O['poll'][0]
POLL_ERR = [l for l in O['poll'][0].split('\n') if 'Error' in l][0].strip()
HAVING_N = len(re.findall(r"_id: '", O['agg_having'][0]))
# numbers and names quoted in the speaker notes, read from the outputs and commands
POLL_SEC, END_MINS = 60, 5
POLL_MSG = POLL_ERR.split(': ', 1)[1]
POLL_POP = re.search(r'population: (\d+)', P['poll'][0]).group(1)
FOUNDER_ONE = O['upd_one_first'][1]
STATUS = dict(re.findall(r"_id: '(\w+)', books: (\d+)", O['agg_status'][1]))
JAVA = {m[0]: m[1:] for m in re.findall(r"_id: '(\w+)',\s*books: (\d+),\s*avgPages: ([\d.]+),\s*maxPages: (\d+)", O['agg_java'][0])}
JAVA_N = sum(int(v[0]) for v in JAVA.values())
UNWIND = re.findall(r"_id: '([^']+)', books: (\d+)", O['agg_unwind'][0])
HAVING_MIN = re.search(r'\$gte: (\d+)', P['agg_having'][0]).group(1)
TIES = [c for c, n in re.findall(r"_id: '([^']+)', books: (\d+)", O['agg_having'][0]) if n == HAVING_MIN]
AVG_R = dict(re.findall(r"status: '(\w+)', avgPages: (\d+)", O['agg_project'][0]))
VOC = re.findall(r"_id: '(\w+)',\s*people: (\d+)", O['persons_group'][0])
ENGINEERS = dict(VOC)['ENGINEER']
VOC_TIE = [v for v, n in VOC if n == '1']
assert FOUNDER_ONE == '1' and set(STATUS) == {'PUBLISH', 'MEAP'} and set(JAVA) == {'PUBLISH', 'MEAP'} and UNWIND[0] == ('Java', str(JAVA_N))
assert len(TIES) == 2 and len(VOC) == 3 and len(VOC_TIE) == 2 and 'PUBLISH' in AVG_R
assert JAVA['MEAP'][0] == '1' and JAVA['MEAP'][1] == JAVA['MEAP'][2]  # slide 17 note: one MEAP book, so average = maximum
# slide numbers of Evening 1 Part 3 and Evening 2 Part 1, read from their content files (Εργασία 2 map)
def where(part, pred):
    D = json.load(open(os.path.join(H, '..', 'content', part + '.json'), encoding='utf8'))
    hits = [i + 1 for i, s in enumerate(D['slides']) if pred(s['title'])]
    assert hits, (part, pred)
    return hits
rng = lambda h: str(h[0]) if len(h) == 1 else f'{h[0]}–{h[-1]}'
E1 = lambda *ts: where('n1p3', lambda t: any(t.startswith(x) for x in ts))
E2 = lambda *ts: where('n2p1', lambda t: any(t.startswith(x) for x in ts))
where('n2p2', lambda t: t.startswith('Java: %d' % JAVA_N))  # slide 18 note: "όσα μέτρησε και το Μέρος 2"

add(type='listslide', mins=1, title='Τι περιέχει το Μέρος 3',
    items=['Ενημέρωση εγγράφων: updateOne, updateMany, upsert.', 'Διαγραφή: deleteOne, deleteMany.',
           'Συνάθροιση: ροή σταδίων, στις συλλογές country, books και persons.',
           'Αντιστοίχιση SQL και MongoDB, και η Εργασία 2 ενότητα προς ενότητα.'],
    foot='Οι ενημερώσεις γίνονται στη συλλογή country της Βραδιάς 1: Ελλάδα, Γαλλία, Γερμανία.',
    notes=['**Ενημέρωση εγγράφων**: Στα Μέρη 1 και 2 τα ερωτήματα μόνο διάβαζαν δεδομένα. Τώρα τα αλλάζουμε.',
           '**Συνάθροιση**: Υπολογισμοί ανά ομάδα εγγράφων: πλήθος, άθροισμα, μέσος όρος. Η συλλογή persons φορτώνεται από αρχείο, στη διαφάνεια [[s_load]].',
           '**η Εργασία 2 ενότητα προς ενότητα**: Ένας πίνακας δείχνει πού διδάχθηκε κάθε ενότητα της εκφώνησης (διαφάνεια [[s_map]]).',
           '**συλλογή country της Βραδιάς 1**: Όποιος την έχει στον υπολογιστή του, εκτελεί τις εντολές των διαφανειών «Δοκιμάστε»· '
           'οι υπόλοιποι παρακολουθούν την έξοδο στη διαφάνεια.'])

add(type='shell', mins=2, dense=True, kicker='Δοκιμάστε', kickerTone='green', title='updateOne και $set',
    cmd=cmd('upd_set'), cmdLabel='Εντολές', out=out('upd_set'), outLabel='Αποτελέσματα',
    points=['Πρώτο όρισμα: το φίλτρο. Δεύτερο: η αλλαγή, με τελεστή.',
            '`$set` προσθέτει το πεδίο capital· αν υπήρχε, θα άλλαζε την τιμή του.',
            'Εργασία 2, ενότητα 11.'],
    src='MongoDB Manual: db.collection.updateOne().',
    notes=['**`use world`**: Η βάση της Βραδιάς 1. Το mongosh απαντά `switched to db world`.',
           '**`$set`**: Η Ελλάδα αποκτά εμφωλευμένο έγγραφο πρωτεύουσας, όπως η Γαλλία και η Γερμανία στη Βραδιά 1.',
           '**`matchedCount: 1`**: Το φίλτρο βρήκε ένα έγγραφο, και το `modifiedCount: 1` δείχνει ότι άλλαξε.',
           '**Εργασία 2, ενότητα 11**: Η ενότητα ζητά ενημέρωση ενός εγγράφου: ένα updateOne σαν αυτό, στα δικά σας δεδομένα.'])

add(type='shell', mins=1, dense=True, title='matchedCount και modifiedCount',
    cmd=cmd('upd_again'), cmdLabel='Η ίδια εντολή, δεύτερη φορά', out=out('upd_again'),
    points=['Βρέθηκε ένα έγγραφο (`matchedCount: 1`), αλλά δεν άλλαξε (`modifiedCount: 0`): η τιμή ήταν ήδη αυτή.',
            'Με `matchedCount: 0`, το φίλτρο δεν βρήκε τίποτε: π.χ. "greece" με πεζό.'],
    notes=['**Η ίδια εντολή, δεύτερη φορά**: Ίδιο φίλτρο και ίδια τιμή με την προηγούμενη διαφάνεια.',
           '**`modifiedCount: 0`**: Η Ελλάδα βρέθηκε, αλλά είχε ήδη αυτή την πρωτεύουσα, άρα δεν άλλαξε. '
           'Δεν εμφανίζεται σφάλμα· μόνο οι δύο αριθμοί δείχνουν τι έγινε.',
           '**`matchedCount: 0`**: Με "greece" το φίλτρο δεν βρίσκει την Ελλάδα: η σύγκριση ξεχωρίζει κεφαλαία από πεζά, όπως με το «Internet» στο Μέρος 1.'])

add(type='shell', mins=1, dense=True, title='$inc και $push',
    cmd=cmd('upd_incpush'), cmdLabel='Εντολές', out=out('upd_incpush'), outLabel='Αποτελέσματα',
    points=['`$inc`: αυξάνει έναν αριθμό· αν το πεδίο λείπει, το δημιουργεί.',
            '`$push`: προσθέτει στοιχείο σε λίστα· αν η λίστα λείπει, τη δημιουργεί.',
            'Δύο τελεστές στην ίδια ενημέρωση.'],
    src='MongoDB Manual: Field and Array Update Operators.',
    notes=['**`$inc: { visits: 1 }`**: Το visits είναι ένας μετρητής για το παράδειγμα. Η Ελλάδα δεν τον είχε, άρα δημιουργείται με τιμή 1.',
           '**`$push: { languages: "Greek" }`**: Ούτε η λίστα languages υπήρχε· δημιουργείται με ένα στοιχείο.',
           '**`{ _id: 0 }`**: Το findOne δείχνει όλο το έγγραφο χωρίς το _id. Τα δύο νέα πεδία είναι στο τέλος.',
           '**Δύο τελεστές στην ίδια ενημέρωση**: Μία εντολή, ένα `modifiedCount: 1`, δύο αλλαγές στο ίδιο έγγραφο.'])

add(type='shell', mins=1, title='$unset: αφαίρεση πεδίου',
    cmd=cmd('upd_unset'), out=out('upd_unset'),
    points=['Το πεδίο visits αφαιρείται· η τιμή μετά το όνομα δεν έχει σημασία, συνήθως "".',
            'Με updateMany, το ίδιο πεδίο αφαιρείται από όλα τα έγγραφα που ταιριάζουν (διαφάνεια [[s_many]]).'],
    notes=['**`$unset: { visits: "" }`**: Αφαιρεί τον μετρητή που προσθέσαμε στην προηγούμενη διαφάνεια.',
           '**δεν έχει σημασία, συνήθως ""**: Το πεδίο δεν παίρνει την τιμή "": φεύγει ολόκληρο από το έγγραφο.',
           '**Με updateMany**: Με κενό φίλτρο `{}`, για όλη τη συλλογή, αντιστοιχεί στο ALTER TABLE … DROP COLUMN της SQL (διαφάνεια [[s_sqlcmd]]).'])

add(type='htable', mins=1, compact=True, title='Οι τελεστές ενημέρωσης',
    head=['Τελεστής', 'Τι κάνει'],
    rows=[['`$set`', 'ορίζει την τιμή ενός πεδίου· το δημιουργεί αν λείπει'],
          ['`$unset`', 'αφαιρεί ένα πεδίο'],
          ['`$inc`', 'αυξάνει έναν αριθμό κατά μια τιμή'],
          ['`$rename`', 'μετονομάζει ένα πεδίο'],
          ['`$push`', 'προσθέτει στοιχείο σε λίστα'],
          ['`$addToSet`', 'προσθέτει στοιχείο σε λίστα, μόνο αν δεν υπάρχει ήδη'],
          ['`$pull`', 'αφαιρεί από λίστα όσα στοιχεία ταιριάζουν σε μια συνθήκη']],
    foot='Πολλοί τελεστές στην ίδια ενημέρωση: `{ $set: { … }, $inc: { … } }`.',
    src='MongoDB Manual: Field Update Operators· Array Update Operators.',
    notes=['**`$set`**: Αυτός και οι `$unset`, `$inc`, `$push` είναι όσοι είδαμε στις διαφάνειες [[s_set]] έως [[s_unset]]. '
           'Νέοι είναι οι `$rename`, `$addToSet` και `$pull`.',
           '**`$addToSet`**: Διαφέρει από το `$push` μόνο στα διπλά. Ένα δεύτερο `$push` του "Greek" θα το έγραφε δύο φορές στη λίστα· το `$addToSet` όχι.',
           '**Πολλοί τελεστές στην ίδια ενημέρωση**: Όπως το `$inc` με το `$push` στη διαφάνεια [[s_incpush]]. '
           'Όλοι λειτουργούν το ίδιο με updateOne και updateMany.',
           'Αν ρωτήσουν: υπάρχουν κι άλλοι τελεστές; Ναι, π.χ. `$min`, `$max`, `$mul`, `$currentDate`. '
           'Για την ενότητα 11 της Εργασίας 2 αρκούν όσοι είναι στον πίνακα.'])

add(type='shell', mins=1, dense=True, kicker='Προσοχή', title='updateOne: μόνο το πρώτο έγγραφο',
    cmd=cmd('upd_one_first') + '\n' + cmd('upd_many_founder'), cmdLabel='Εντολές', out=out('upd_one_first') + '\n' + out('upd_many_founder'), outLabel='Αποτελέσματα',
    points=['Γαλλία και Γερμανία έχουν euSince 1958· το updateOne άλλαξε μόνο την πρώτη.',
            'Το updateMany βρήκε και τις δύο (`matchedCount: 2`) και άλλαξε όποια δεν είχε ήδη την τιμή (`modifiedCount: 1`).'],
    notes=['**`founder: true`**: Ιδρυτικό μέλος της ΕΟΚ (1958). Το φίλτρο `euSince: 1958` ταιριάζει σε δύο χώρες.',
           '**`countDocuments({ founder: true })`**: Μετά το updateOne, μόνο ένα έγγραφο έχει το πεδίο: το %s στα Αποτελέσματα.' % FOUNDER_ONE,
           '**το updateOne άλλαξε μόνο την πρώτη**: Όταν το φίλτρο ταιριάζει σε πολλά έγγραφα, το updateOne αλλάζει ένα από αυτά, χωρίς προειδοποίηση.',
           '**`modifiedCount: 1`**: Η χώρα που άλλαξε το updateOne είχε ήδη την τιμή, όπως στη διαφάνεια [[s_again]]· άλλαξε μόνο η άλλη.'])

add(type='shell', mins=1, dense=True, title='updateMany: από «0 σελίδες» σε «άγνωστο»',
    cmd=cmd('upd_many_books'), cmdLabel='Εντολές', out=out('upd_many_books'), outLabel='Αποτελέσματα',
    points=['Ένα φίλτρο, πολλά έγγραφα: και τα %s βιβλία με 0 σελίδες.' % ZEROS,
            'Τώρα το «άγνωστο» είναι πεδίο που λείπει, όχι ψεύτικο 0: δεν μετρά στους μέσους όρους.',
            'Επαναφορά του αρχείου: `mongoimport … --drop`.'],
    notes=['**`{ pageCount: 0 }`**: Τα βιβλία με 0 σελίδες του Μέρους 1, όπου το 0 σήμαινε «άγνωστο». Το `$unset` αφαιρεί το πεδίο από όλα μαζί.',
           '**`$exists: false`**: Μετρά τα έγγραφα που δεν έχουν καθόλου το πεδίο: %s, όσα άλλαξε το updateMany.' % ZEROS,
           '**δεν μετρά στους μέσους όρους**: Ένα 0 κατεβάζει τον μέσο όρο· ένα πεδίο που λείπει δεν μετρά. Το δείχνει η διαφάνεια [[s_avg]].',
           '**`mongoimport … --drop`**: Όποιος θέλει ξανά τα βιβλία με τα μηδενικά, εκτελεί πάλι την εισαγωγή του Μέρους 1.'])

add(type='shell', mins=2, dense=True, kicker='Δοκιμάστε', kickerTone='green', title='upsert: η Κύπρος επιστρέφει',
    cmd=cmd('upsert'), cmdLabel='Εντολές', out=out('upsert'), outLabel='Αποτελέσματα',
    points=['Κανένα έγγραφο δεν ταίριαξε: με `upsert: true` δημιουργείται νέο.',
            'Το νέο έγγραφο παίρνει το name από το φίλτρο και το population από το `$set`.'],
    src='MongoDB Manual: db.collection.updateOne() (upsert).',
    notes=['**`use world`**: Πίσω στη βάση world, μετά τα βιβλία της προηγούμενης διαφάνειας.',
           '**`{ name: "Cyprus" }`**: Η Κύπρος διαγράφηκε στη Βραδιά 1, άρα το φίλτρο δεν βρίσκει τίποτε: `matchedCount: 0`.',
           '**`upsertedCount: 1`**: Δημιουργήθηκε νέο έγγραφο, με δικό του ObjectId. Το upsert είναι «ενημέρωσε αν υπάρχει, αλλιώς δημιούργησε».',
           '**Το νέο έγγραφο παίρνει το name από το φίλτρο**: Το findOne δείχνει μόνο αυτά τα δύο πεδία. '
           'Χρήσιμο όταν δεν ξέρουμε αν το έγγραφο υπάρχει ήδη, όπως σε επαναλαμβανόμενες εισαγωγές.'])

add(type='poll', mins=2, timerSec=POLL_SEC, kicker='Ερώτημα', title='Τι κάνει αυτή η εντολή;',
    context='Η Ελλάδα έχει ήδη πέντε πεδία.',
    code=cmd('poll'),
    options=['Αλλάζει μόνο τον πληθυσμό', 'Αντικαθιστά όλο το έγγραφο', 'Εμφανίζει σφάλμα', 'Δεν κάνει τίποτε, χωρίς μήνυμα'],
    notes=['**Η Ελλάδα έχει ήδη πέντε πεδία**: Τα name, euSince και population της Βραδιάς 1, και τα capital και languages των διαφανειών [[s_set]] και [[s_incpush]].',
           '**%02d:%02d**: Δημοσκόπηση Zoom, μία επιλογή· ξεκινήστε το χρονόμετρο με το πλήκτρο T. Η απάντηση είναι στην επόμενη διαφάνεια.' % divmod(POLL_SEC, 60)])

add(type='shell', mins=1, title='Η απάντηση: σφάλμα',
    cmd=cmd('poll'), out=POLL_ERR,
    points=['Το updateOne θέλει τελεστή: `$set`, `$inc`, `$unset`…',
            'Για αντικατάσταση ολόκληρου του εγγράφου υπάρχει το `replaceOne`.',
            'Προσοχή σε παλιούς οδηγούς: το `update()` χωρίς τελεστή αντικαθιστούσε όλο το έγγραφο.'],
    src='MongoDB Manual: db.collection.updateOne()· db.collection.replaceOne()· db.collection.update().',
    notes=['**`%s`**: Η σωστή απάντηση είναι το Γ. Κανένα έγγραφο δεν αλλάζει: το σφάλμα εμφανίζεται πριν σταλεί η εντολή.' % POLL_MSG,
           '**Το updateOne θέλει τελεστή**: Με `{ $set: { population: %s } }` θα άλλαζε μόνο ο πληθυσμός, όπως λέει η επιλογή Α.' % POLL_POP,
           '**`replaceOne`**: Θα κρατούσε μόνο το population και το _id· τα υπόλοιπα πεδία θα χάνονταν.',
           '**Προσοχή σε παλιούς οδηγούς**: Με το ίδιο δεύτερο όρισμα, το παλιό `update()` έκανε ό,τι λέει η επιλογή Β: αντικαθιστούσε όλο το έγγραφο.'])

add(type='shell', mins=1, skippable=True, kicker='Προσοχή', title='Πριν από κάθε μαζική διαγραφή: μέτρηση',
    cmd=cmd('count_first'), out=out('count_first'),
    points=['Πρώτα `countDocuments` με το φίλτρο της διαγραφής: 1, η Κύπρος.',
            '`deleteMany({})` και `updateMany({}, …)` αφορούν όλη τη συλλογή, χωρίς επιβεβαίωση και χωρίς αναίρεση.'],
    notes=['**`{ population: { $lt: 1000000 } }`**: Χώρες με λιγότερους από ένα εκατομμύριο κατοίκους: το φίλτρο της διαγραφής της επόμενης διαφάνειας.',
           '**1, η Κύπρος**: Η Κύπρος του upsert της διαφάνειας [[s_upsert]], η μόνη χώρα κάτω από το όριο. '
           'Αν ο αριθμός δεν είναι ο αναμενόμενος, το φίλτρο διορθώνεται πριν από τη διαγραφή.',
           '**`deleteMany({})`**: Το κενό φίλτρο `{}` ταιριάζει σε όλα τα έγγραφα, όπως το DELETE χωρίς WHERE στην SQL.'])

add(type='shell', mins=1, title='deleteMany και deleteOne',
    cmd=cmd('delmany'), out=out('delmany'),
    points=['`deleteMany`: όλα όσα ταιριάζουν· εδώ ένα, η Κύπρος.',
            '`deleteOne`: μόνο το πρώτο, όπως στη Βραδιά 1.',
            'Εργασία 2, ενότητα 12.'],
    src='MongoDB Manual: db.collection.deleteMany().',
    notes=['**`deletedCount: 1`**: Διαγράφηκε μόνο η Κύπρος. Η συλλογή country έχει πάλι τις τρεις χώρες της Βραδιάς 1, '
           'με τις ενημερώσεις της Ελλάδας και των ιδρυτικών μελών.',
           '**όπως στη Βραδιά 1**: Εκεί το deleteOne διέγραψε την Κύπρο, με φίλτρο το όνομά της.',
           '**Εργασία 2, ενότητα 12**: Η ενότητα ζητά διαγραφή ενός εγγράφου, με στιγμιότυπο του αποτελέσματος.'])

add(type='stack', mins=1, title='Συνάθροιση: ροή σταδίων',
    stages=[{'h': '$match', 't': 'Φιλτράρει έγγραφα, όπως το φίλτρο του find.'},
            {'h': '$group', 't': 'Ομαδοποιεί και υπολογίζει ανά ομάδα: πλήθος, άθροισμα, μέσο όρο, ελάχιστο, μέγιστο.'},
            {'h': '$sort, $limit, $project', 't': 'Ταξινομούν, περιορίζουν και διαμορφώνουν την έξοδο.'}],
    codeLabel='Σύνταξη', code='db.συλλογή.aggregate([\n  { στάδιο 1 },\n  { στάδιο 2 },\n  …\n])',
    foot='Η έξοδος κάθε σταδίου είναι η είσοδος του επόμενου.',
    src='MongoDB Manual: Aggregation Pipeline.',
    notes=['**$match**: Το φίλτρο του find, γραμμένο ως στάδιο: περνούν μόνο τα έγγραφα που ταιριάζουν.',
           '**$group**: Το find απαντά «ποια έγγραφα»· η συνάθροιση απαντά «πόσα, πόσο, κατά μέσο όρο, ανά τι».',
           '**`db.συλλογή.aggregate([`**: Μία εντολή, με τα στάδια σε λίστα, στη σειρά που εκτελούνται.',
           '**Η έξοδος κάθε σταδίου είναι η είσοδος του επόμενου**: Γι’ αυτό η σειρά των σταδίων μετρά· το δείχνει η διαφάνεια [[s_having]].'])

add(type='shell', mins=2, dense=True, title='$group: ο συνολικός πληθυσμός',
    cmd=cmd('agg_total'), out=out('agg_total'),
    points=['`_id: null`: μία μόνο ομάδα, όλα τα έγγραφα μαζί.',
            '`"$population"`: η τιμή του πεδίου· το $ μπροστά από το όνομα.',
            'Ελλάδα, Γαλλία και Γερμανία: %s.' % gr(TOTAL)],
    src='MongoDB Manual: $group (aggregation).',
    notes=['**`_id: null`**: Το `_id` του `$group` ορίζει τις ομάδες. Με null, όλα τα έγγραφα είναι μία ομάδα.',
           '**`totalPopulation`**: Το όνομα του αποτελέσματος το διαλέγουμε εμείς· με αυτό εμφανίζεται στην έξοδο.',
           '**`"$population"`**: Το `$sum` προσθέτει την τιμή του πεδίου population από κάθε έγγραφο της ομάδας.',
           '**Ελλάδα, Γαλλία και Γερμανία: %s**: Στην SQL: `SELECT SUM(population) FROM country`.' % gr(TOTAL)])

add(type='shell', mins=1, title='$group ανά πεδίο: βιβλία ανά κατάσταση',
    cmd=cmd('agg_status'), cmdLabel='Εντολές', out=out('agg_status'), outLabel='Αποτελέσματα',
    points=['`_id: "$status"`: μία ομάδα για κάθε τιμή του status.',
            '`$sum: 1`: μετρά τα έγγραφα κάθε ομάδας, όπως το COUNT(*) με GROUP BY.',
            'Εργασία 2, ενότητα 10.'],
    notes=['**`_id: "$status"`**: Το status έχει δύο τιμές, άρα δύο ομάδες.',
           '**`books: %s`**: Τα %s βιβλία σε MEAP του Μέρους 1· τα άλλα %s έχουν κυκλοφορήσει. Μαζί %d, όλη η συλλογή.'
           % (STATUS['MEAP'], STATUS['MEAP'], STATUS['PUBLISH'], int(STATUS['MEAP']) + int(STATUS['PUBLISH'])),
           '**`$sum: 1`**: Προσθέτει 1 για κάθε έγγραφο της ομάδας. Στην SQL: `SELECT status, COUNT(*) FROM books GROUP BY status`.',
           'Αν ρωτήσουν: γιατί πρώτα το PUBLISH; Η σειρά των ομάδων στην έξοδο δεν είναι εγγυημένη· για σταθερή σειρά χρειάζεται `$sort`.'])

add(type='shell', mins=1, dense=True, title='$match και συσσωρευτές',
    cmd=cmd('agg_java'), out=out('agg_java'),
    points=['`$match` πρώτο: μόνο τα βιβλία Java, όπως το WHERE.',
            '`$avg` και `$max`: μέσος όρος και μέγιστο ανά ομάδα.',
            'Το `$avg` αγνοεί τα βιβλία που δεν έχουν πλέον pageCount (διαφάνεια [[s_many]]).'],
    src='MongoDB Manual: $avg (aggregation).',
    notes=['**`{ $match: { categories: "Java" } }`**: Πρώτο στάδιο: στο `$group` φτάνουν μόνο τα %d βιβλία Java.' % JAVA_N,
           '**`books: %s, avgPages: %s, maxPages: %s`**: Ένα μόνο βιβλίο Java είναι σε MEAP, με %s σελίδες· '
           'γι’ αυτό ο μέσος όρος και το μέγιστο συμπίπτουν.' % (JAVA['MEAP'] + (JAVA['MEAP'][2],)),
           '**`avgPages: %s`**: Ο μέσος όρος έχει πολλά δεκαδικά· η στρογγυλοποίηση γίνεται με `$project`, στη διαφάνεια [[s_project]].' % JAVA['PUBLISH'][1],
           '**αγνοεί τα βιβλία που δεν έχουν πλέον pageCount**: Χωρίς το updateMany της διαφάνειας [[s_many]], '
           'τα βιβλία Java με 0 σελίδες θα κατέβαζαν αυτόν τον μέσο όρο.'])

add(type='shell', mins=2, dense=True, title='$unwind: ένα έγγραφο ανά κατηγορία',
    cmd=cmd('agg_unwind'), out=out('agg_unwind'),
    points=['`$unwind`: ένα έγγραφο για κάθε κατηγορία κάθε βιβλίου.',
            'Μετά: ομάδα ανά κατηγορία, ταξινόμηση, τα πέντε πρώτα.',
            'Βιβλία χωρίς κατηγορία δεν περνούν από το `$unwind`.'],
    src='MongoDB Manual: $unwind (aggregation).',
    notes=['**`{ $unwind: "$categories" }`**: Ένα βιβλίο με δύο κατηγορίες γίνεται δύο έγγραφα, ένα για την καθεμία. '
           'Χωρίς αυτό, το `$group` θα έφτιαχνε ομάδες ανά ολόκληρη λίστα κατηγοριών.',
           "**`{ _id: '%s', books: %s }`**: Τα %s βιβλία Java, όσα μέτρησε και το Μέρος 2." % (UNWIND[0] + (UNWIND[0][1],)),
           '**Βιβλία χωρίς κατηγορία**: Στη συλλογή υπάρχουν βιβλία με κενή λίστα categories· δεν μετρούν σε καμία ομάδα.',
           'Αν ρωτήσουν: πώς γίνεται αυτό στην SQL; Με ξεχωριστό πίνακα κατηγοριών και JOIN.'])

add(type='shell', mins=1, dense=True, title='$match μετά το $group: το HAVING',
    cmd=cmd('agg_having'), out=out('agg_having'),
    points=['`$match` μετά το `$group` φιλτράρει ομάδες, όπως το HAVING της SQL.',
            'Κατηγορίες με τουλάχιστον 12 βιβλία: %s.' % {7: 'επτά'}.get(HAVING_N, HAVING_N),
            '`_id: 1` στο `$sort`: σταθερή σειρά στις ισοπαλίες.'],
    notes=['**`{ $match: { books: { $gte: %s } } }`**: Το books είναι το πεδίο που δημιούργησε το `$group`. '
           'Πριν από το `$group`, το ίδιο `$match` θα έψαχνε πεδίο books στα βιβλία και δεν θα έβρισκε τίποτε.' % HAVING_MIN,
           '**Κατηγορίες με τουλάχιστον %s βιβλία: %s**: Οι κατηγορίες της προηγούμενης διαφάνειας, και οι %s και %s με ακριβώς %s: '
           'το `$gte` περιλαμβάνει και το %s.' % (HAVING_MIN, {7: 'επτά'}.get(HAVING_N, HAVING_N), TIES[0], TIES[1], HAVING_MIN, HAVING_MIN),
           '**σταθερή σειρά στις ισοπαλίες**: Με το `_id: 1`, οι %s και %s μπαίνουν αλφαβητικά. Χωρίς αυτό, η σειρά τους μπορεί να αλλάζει.' % tuple(TIES)])

add(type='shell', mins=1, dense=True, title='$project: το σχήμα της εξόδου',
    cmd=cmd('agg_project'), out=out('agg_project'),
    points=['`$project`: ποια πεδία βγαίνουν και με ποιο όνομα· το `_id` γίνεται status.',
            '`$round`: στρογγυλοποίηση του μέσου όρου.',
            'Ό,τι είναι το SELECT για την SQL.'],
    src='MongoDB Manual: $project· $round (aggregation).',
    notes=['**`status: "$_id"`**: Νέο πεδίο με την τιμή του `_id` της ομάδας· το `_id: 0` κρύβει το αρχικό. Το `books: 1` κρατά το πεδίο όπως είναι.',
           '**`$round: ["$avgPages", 0]`**: Στρογγυλοποίηση σε 0 δεκαδικά: ο μέσος όρος της διαφάνειας [[s_avg]] γίνεται %s.' % AVG_R['PUBLISH'],
           'Αν ρωτήσουν: γιατί το books βγαίνει πρώτο; Όσα πεδία απλώς κρατούνται ακολουθούν τη σειρά του εισερχόμενου εγγράφου, πριν από τα νέα.'])

add(type='shell', mins=1, dense=True, title='Το persons.txt στο mongosh',
    cmd='db = db.getSiblingDB("book-filtered-top-subset");\ndb.dropDatabase();\ndb.persons.createIndex({"vocation": 1, "dateofbirth": 1});\ndb.persons.insertMany([ … έξι άτομα … ]);',
    cmdLabel='Το αρχείο persons.txt', out=out('persons_load'), outLabel='Αποτέλεσμα της τελευταίας εντολής',
    points=['Ανοίξτε το αρχείο, αντιγράψτε όλο το περιεχόμενο και επικολλήστε το στο mongosh.',
            'Νέα βάση με έξι άτομα· η διεύθυνση είναι εμφωλευμένο έγγραφο.',
            'Εναλλακτικά: `load("persons.txt")`, με το mongosh ανοιγμένο στον φάκελο του αρχείου.'],
    notes=['**`db.getSiblingDB("book-filtered-top-subset")`**: Περνά στη νέα βάση, όπως το use. '
           'Το `db.dropDatabase()` τη διαγράφει πρώτα, ώστε μια δεύτερη επικόλληση να μη διπλασιάσει τα άτομα.',
           '**`insertedIds`**: Έξι ObjectId, ένα για κάθε άτομο: το αρχείο δεν δίνει _id.',
           '**Ανοίξτε το αρχείο**: Το persons.txt είναι στο υλικό της βραδιάς, δίπλα στο books.json.',
           '**η διεύθυνση είναι εμφωλευμένο έγγραφο**: Το πεδίο address, με number, street και city. Δεν φαίνεται εδώ, γιατί τα έξι άτομα είναι συντομευμένα.'])

add(type='shell', mins=2, dense=True, side=True, title='Οι τρεις νεότεροι μηχανικοί',
    cmd=cmd('persons_pipeline', [1, 2]), cmdLabel='Εντολές', out=out('persons_pipeline', [2]),
    foot='Φιλτράρει τους μηχανικούς, ταξινομεί από τον νεότερο, κρατά τρεις και αφαιρεί τρία πεδία.',
    src='Paul Done, Practical MongoDB Aggregations: «Filtered Top Subset».',
    notes=['**`var pipeline = [`**: Η μεταβλητή κρατά τη λίστα των σταδίων, όπως οι μεταβλητές του Μέρους 1 κρατούσαν φίλτρα. '
           'Η Εργασία 2 ζητά μεταβλητές σε κάποια ερωτήματα.',
           '**`{ $sort: { dateofbirth: -1 } }`**: Φθίνουσα ημερομηνία γέννησης: πρώτα ο νεότερος. '
           'Από τους %s μηχανικούς, το `$limit: 3` αφήνει έξω όποιον γεννήθηκε πρώτος.' % ENGINEERS,
           "**`gender: 'FEMALE'`**: Μόνο η Olive έχει πεδίο gender. Ίδια συλλογή, διαφορετικά πεδία ανά έγγραφο.",
           '**αφαιρεί τρία πεδία**: Τα _id, vocation και address, με το στάδιο `$unset`· η επόμενη διαφάνεια το συγκρίνει με το `$project`.'])

add(type='codeslide', mins=1, title='$unset ως στάδιο',
    code='// με $unset\n{ $unset: ["_id", "vocation", "address"] }\n\n// με $project\n{ $project: {\n    _id: 0, vocation: 0, address: 0 } }',
    points=['Και τα δύο δίνουν τους ίδιους τρεις μηχανικούς.',
            '`$unset`: γράφει μόνο όσα αφαιρούνται.',
            '`$project`: και για προσθήκη ή μετονομασία πεδίων (διαφάνεια [[s_project]]).'],
    src='MongoDB Manual: $unset (aggregation).',
    notes=['**`{ $unset: ["_id", "vocation", "address"] }`**: Μια λίστα με τα πεδία που φεύγουν. '
           'Είναι στάδιο συνάθροισης, όχι ο τελεστής ενημέρωσης της διαφάνειας [[s_unset]].',
           '**`_id: 0, vocation: 0, address: 0`**: Το 0 σημαίνει «χωρίς αυτό το πεδίο», όπως στην προβολή του find.',
           '**Και τα δύο δίνουν τους ίδιους τρεις μηχανικούς**: Το στάδιο `$unset` είναι άλλος τρόπος γραφής του `$project` που αφαιρεί πεδία. '
           'Στην Εργασία 2, οποιοδήποτε από τα δύο είναι σωστό.'])

add(type='shell', mins=1, dense=True, side=True, skippable=True, title='Το ίδιο με find',
    cmd=cmd('persons_find'), out=out('persons_find'),
    foot='Χωρίς ομαδοποίηση, το find αρκεί· η συνάθροιση χρειάζεται όταν υπολογίζουμε ανά ομάδα.',
    notes=['**`{ vocation: "ENGINEER" }`**: Το φίλτρο του `$match`, ως πρώτο όρισμα του find. Η προβολή με 0 αφαιρεί τα ίδια τρία πεδία με το `$unset`.',
           '**`.sort({ dateofbirth: -1 }).limit(3)`**: Τα στάδια `$sort` και `$limit` γίνονται οι μέθοδοι sort και limit του Μέρους 1.',
           '**Χωρίς ομαδοποίηση, το find αρκεί**: Οι τρεις μηχανικοί είναι ίδιοι με της διαφάνειας [[s_persons]].'])

add(type='definition', mins=1, kicker='Προσοχή', title='Η ενότητα 10 ζητά ομαδοποίηση',
    quote='Ερώτημα με pipeline που παρουσιάζει συγκεντρωτικά, ομαδοποιημένα αποτελέσματα.',
    cite='Εργασία 2, ενότητα 10',
    callouts=[{'tone': 'amber', 'h': 'Το παράδειγμα του persons', 't': '$match, $sort, $limit, $unset: φιλτράρει και ταξινομεί, αλλά δεν ομαδοποιεί.'},
              {'tone': 'blue', 'h': 'Για την Εργασία 2', 't': 'Τουλάχιστον ένα $group, με τα δικά σας δεδομένα, όπως στις διαφάνειες [[s_group_first]] έως [[s_project]].'}],
    notes=['**συγκεντρωτικά, ομαδοποιημένα αποτελέσματα**: Αποτελέσματα ανά ομάδα, π.χ. πλήθος ή μέσος όρος, όχι μια λίστα εγγράφων.',
           '**Το παράδειγμα του persons**: Το pipeline της διαφάνειας [[s_persons]] δεν έχει `$group`· μόνο του δεν καλύπτει την ενότητα 10.',
           '**Τουλάχιστον ένα $group**: Για παράδειγμα, πλήθος ανά κατηγορία, με `$sum: 1` όπως στη διαφάνεια [[s_status]]. '
           'Η επόμενη διαφάνεια προσθέτει ομαδοποίηση στη συλλογή persons.'])

add(type='shell', mins=1, dense=True, side=True, title='Ομαδοποίηση στο persons: άτομα ανά επάγγελμα',
    cmd=cmd('persons_group'), out=out('persons_group'),
    foot='Μία ομάδα ανά επάγγελμα: πόσα άτομα, και η παλαιότερη ημερομηνία γέννησης (`$min`).',
    notes=['**`_id: "$vocation"`**: Τρία επαγγέλματα, άρα τρεις ομάδες. Στην SQL: `SELECT vocation, COUNT(*), MIN(dateofbirth) FROM persons GROUP BY vocation`.',
           '**`{ $sort: { people: -1, _id: 1 } }`**: Πρώτα κατά πλήθος· στην ισοπαλία, %s πριν από %s, αλφαβητικά.' % tuple(VOC_TIE),
           '**`people: %s`**: Οι %s μηχανικοί· η διαφάνεια [[s_persons]] κράτησε τους τρεις νεότερους.' % (ENGINEERS, ENGINEERS),
           '**η παλαιότερη ημερομηνία γέννησης**: Το `$min` σε ημερομηνίες δίνει την παλαιότερη: το μεγαλύτερο σε ηλικία άτομο κάθε ομάδας.'])

add(type='htable', mins=2, compact=True, title='SQL και MongoDB: εντολές',
    head=['SQL', 'MongoDB'],
    rows=[['`INSERT INTO … VALUES …`', '`insertOne`, `insertMany`'],
          ['`SELECT … FROM … WHERE …`', '`find(φίλτρο, προβολή)`'],
          ['`UPDATE … SET … WHERE …`', '`updateOne`, `updateMany` με `$set`'],
          ['`SET age = age + 3`', '`$inc: { age: 3 }`'],
          ['`DELETE FROM … WHERE …`', '`deleteOne`, `deleteMany` με φίλτρο'],
          ['`DELETE FROM people`', '`deleteMany({})`'],
          ['`ALTER TABLE … ADD …`', '`updateMany({}, { $set: … })`'],
          ['`ALTER TABLE … DROP COLUMN …`', '`updateMany({}, { $unset: … })`']],
    foot='Στη MongoDB δεν υπάρχει ALTER TABLE: η συλλογή δεν επιβάλλει δομή, και τα πεδία αλλάζουν στο επίπεδο του εγγράφου.',
    src='MongoDB Manual: SQL to MongoDB Mapping Chart.',
    notes=['**`SELECT … FROM … WHERE …`**: Ό,τι κάναμε στα Μέρη 1 και 2 με το find: το φίλτρο στη θέση του WHERE, η προβολή στη θέση των στηλών.',
           '**`DELETE FROM people`**: Χωρίς WHERE, όλος ο πίνακας· στη MongoDB, το κενό φίλτρο `{}`. Και τα δύο χωρίς επιβεβαίωση (διαφάνεια [[s_count]]).',
           '**Στη MongoDB δεν υπάρχει ALTER TABLE**: Για παράδειγμα, το pageCount έφυγε μόνο από τα %s βιβλία της διαφάνειας [[s_many]], '
           'και η Κύπρος στη Βραδιά 1 δεν είχε euSince.' % ZEROS,
           'Αν ρωτήσουν: και το SELECT COUNT(*); Στη MongoDB, `countDocuments()` με φίλτρο, όπως στο Μέρος 1.'])

add(type='htable', mins=2, compact=True, title='SQL και MongoDB: συνάθροιση',
    head=['SQL', 'Συνάθροιση στη MongoDB'],
    rows=[['`WHERE`', '`$match`'], ['`GROUP BY`', '`$group`'], ['`HAVING`', '`$match` μετά το `$group`'],
          ['`SELECT`', '`$project`'], ['`ORDER BY`', '`$sort`'], ['`LIMIT`', '`$limit`'],
          ['`SUM()`, `COUNT()`', '`$sum`, με `$sum: 1` για το πλήθος'], ['`JOIN`', '`$lookup`']],
    foot='Το `$lookup` συνδέει δύο συλλογές, όπως το JOIN. Η Εργασία 2 δεν το ζητά.',
    src='MongoDB Manual: SQL to Aggregation Mapping Chart.',
    notes=['**`WHERE`**: Όλες οι γραμμές εκτός από το JOIN εμφανίστηκαν απόψε, στις διαφάνειες [[s_flow]] έως [[s_pgroup]].',
           '**`HAVING`**: Το ίδιο `$match`, μετά το `$group`: η θέση του στη ροή κάνει τη διαφορά (διαφάνεια [[s_having]]).',
           '**`COUNT()`**: Στη συνάθροιση, πλήθος ανά ομάδα με `$sum: 1`. Για απλή μέτρηση, χωρίς ομάδες, αρκεί το countDocuments.',
           '**Η Εργασία 2 δεν το ζητά**: Στην Εργασία 2, οι δύο πίνακες της Εργασίας 1 γίνονται εμφωλευμένα έγγραφα.'])

rows_map = [['1–3. Βάση, συλλογή, έγγραφα', 'Βραδιά 1, Μέρος 3, διαφάνειες %s' % rng(E1('Πλοήγηση', 'Εισαγωγή ενός', 'Δικό μας', 'Εισαγωγή πολλών', 'Εμφωλευμένο'))],
            ['4. Προβολή πεδίων', 'Μέρος 1, διαφάνειες %s' % rng(E2('Προβολή', 'Χωρίς `_id`'))],
            ['5. Λογικοί τελεστές', 'Μέρος 1, διαφάνειες %s' % rng(E2('Λογικοί', '`$or`', 'Το ίδιο πεδίο'))],
            ['6. Τελεστές σύγκρισης', 'Μέρος 1, διαφάνειες %s' % rng(E2('Τελεστές σύγκρισης', 'Σύγκριση στην πράξη'))],
            ['7. Regex', 'Μέρος 1, διαφάνειες %s· Άσκηση 2' % rng(E2('Κανονικές', 'Τα σύμβολα'))],
            ['8. Σύνθετα ερωτήματα', 'Μέρος 1, διαφάνεια %s και Άσκηση 1· φύλλο του Μέρους 2' % rng(E2('`$or`'))],
            ['9. Ταξινόμηση και περιορισμός', 'Μέρος 1, διαφάνειες %s' % rng(E2('Ταξινόμηση', 'skip', 'Τα μηδενικά'))],
            ['10. Pipeline με ομαδοποίηση', 'Μέρος 3, διαφάνειες [[s_group_first]]–[[s_project]] και [[s_pgroup]]'],
            ['11. Ενημέρωση', 'Μέρος 3, διαφάνειες 2–[[s_upsert]]'],
            ['12. Διαγραφή', 'Βραδιά 1, Μέρος 3, διαφάνεια %s· Μέρος 3, διαφάνεια [[s_del]]' % rng(E1('Διαγραφή'))],
            ['JSON και μεταβλητές', 'Μέρος 1, διαφάνειες %s' % rng(E2('Ευανάγνωστο', 'Μεταβλητές'))]]
add(type='htable', mins=2, compact=True, title='Εργασία 2: κάθε ενότητα και πού διδάχθηκε',
    head=['Ενότητα της εκφώνησης', 'Πού διδάχθηκε'], rows=rows_map,
    notes=['**Πού διδάχθηκε**: «Μέρος» χωρίς βραδιά σημαίνει τη σημερινή, Βραδιά 2. Οι αριθμοί είναι και οι σελίδες των PDF σας, μία διαφάνεια ανά σελίδα.',
           '**1–3. Βάση, συλλογή, έγγραφα**: Η εκφώνηση ζητά τουλάχιστον 4 έγγραφα, από τα οποία τα 2 με εμφωλευμένα έγγραφα.',
           '**8. Σύνθετα ερωτήματα**: Χωρίς δική της διαφάνεια: συνδυάζει τους τελεστές των ενοτήτων 5 και 6, σε τουλάχιστον δύο ερωτήματα.',
           '**9. Ταξινόμηση και περιορισμός**: Η εκφώνηση ζητά και αύξουσα και φθίνουσα ταξινόμηση.'])

add(type='table', mins=1, title='Εργασία 2: τι παραδίδετε',
    rows=[{'h': 'Αναφορά', 't': 'Ονοματεπώνυμο, email, τίτλος· περιγραφή των τροποποιήσεων της βάσης της Εργασίας 1 και των πινάκων (τουλάχιστον 2, ο ένας εμφωλευμένος στον άλλον).'},
          {'h': 'Ενότητες 1 έως 12', 't': 'Αριθμημένες όπως στην εκφώνηση· για κάθε κώδικα, μία παράγραφος που εξηγεί τι κάνει και στιγμιότυπο οθόνης με το αποτέλεσμα.'},
          {'h': 'JSON και μεταβλητές', 't': 'Σε κάποια ερωτήματα, ευανάγνωστο JSON και μεταβλητές, με κείμενο που το επισημαίνει.'},
          {'h': 'Προθεσμία', 't': 'Στην πλατφόρμα του μαθήματος.'}],
    src='Εκφώνηση της Εργασίας 2 (MongoDB).',
    notes=['**τουλάχιστον 2, ο ένας εμφωλευμένος στον άλλον**: Από δύο πίνακες της Εργασίας 1, ο ένας γίνεται εμφωλευμένο έγγραφο μέσα στον άλλον, όπως το capital μέσα σε κάθε χώρα.',
           '**στιγμιότυπο οθόνης με το αποτέλεσμα**: Για τις ενημερώσεις, το στιγμιότυπο δείχνει τα matchedCount και modifiedCount (διαφάνεια [[s_again]]).',
           '**κείμενο που το επισημαίνει**: Αρκεί μια φράση στην αναφορά που λέει πού χρησιμοποιήθηκαν. '
           'Το printjson και οι μεταβλητές είναι στο Μέρος 1, διαφάνειες %s.' % rng(E2('Ευανάγνωστο', 'Μεταβλητές')),
           '**Στην πλατφόρμα του μαθήματος**: Εκεί ορίζεται η ημερομηνία παράδοσης.'])

add(type='remember', mins=1, kicker='Να θυμάστε', title='Τρία σημεία από το Μέρος 3',
    items=['Κάθε ενημέρωση έχει φίλτρο και τελεστή: το updateOne αλλάζει το πρώτο έγγραφο, το updateMany όλα, και χωρίς τελεστή εμφανίζεται σφάλμα.',
           'Η συνάθροιση είναι ροή σταδίων: το $match φιλτράρει, το $group ομαδοποιεί, τα $sort, $limit και $project διαμορφώνουν την έξοδο.',
           'Πριν από κάθε μαζική αλλαγή ή διαγραφή, countDocuments με το ίδιο φίλτρο.'],
    notes=['**Κάθε ενημέρωση έχει φίλτρο και τελεστή**: Διαβάστε τα τρία σημεία όπως είναι. Το πρώτο είναι και η απάντηση της δημοσκόπησης.',
           '**Η συνάθροιση είναι ροή σταδίων**: Για την ενότητα 10 της Εργασίας 2, με τουλάχιστον ένα `$group`.',
           '**countDocuments με το ίδιο φίλτρο**: Ο κανόνας της διαφάνειας [[s_count]]. Ακολουθεί η τελευταία διαφάνεια, με τα λεπτά για ερωτήσεις.'])

add(type='endslide', mins=END_MINS, title='Ερωτήσεις',
    line='Εδώ κλείνουν οι μη σχεσιακές βάσεις δεδομένων. Στο επόμενο μάθημα ξεκινά η Μαθησιακή Αναλυτική.',
    notes=['**Ερωτήσεις**: Περίπου %d λεπτά για ερωτήσεις, κυρίως για την Εργασία 2. '
           'Αν δεν ρωτά κανείς: «Ποια ενότητα της Εργασίας 2 σας φαίνεται η δυσκολότερη;»' % END_MINS,
           '**Στο επόμενο μάθημα ξεκινά η Μαθησιακή Αναλυτική**: Για την Εργασία 2, στο υλικό της βραδιάς είναι η εκφώνηση και τα PDF των διαφανειών.'])

def n_of(pred):
    hits = [i + 1 for i, s in enumerate(S) if pred(s['title'])]
    assert len(hits) == 1, hits
    return hits[0]
REF = {'s_many': n_of(lambda t: t.startswith('updateMany')), 's_project': n_of(lambda t: t.startswith('$project')),
       's_group_first': n_of(lambda t: t.startswith('$group: ο συνολικός')), 's_pgroup': n_of(lambda t: t.startswith('Ομαδοποίηση στο persons')),
       's_upsert': n_of(lambda t: t.startswith('upsert')), 's_del': n_of(lambda t: t.startswith('deleteMany')),
       's_set': n_of(lambda t: t.startswith('updateOne και')), 's_again': n_of(lambda t: t.startswith('matchedCount')),
       's_incpush': n_of(lambda t: t.startswith('$inc')), 's_unset': n_of(lambda t: t.startswith('$unset:')),
       's_count': n_of(lambda t: t.startswith('Πριν από κάθε μαζική')), 's_flow': n_of(lambda t: t.startswith('Συνάθροιση: ροή')),
       's_status': n_of(lambda t: t.startswith('$group ανά πεδίο')), 's_avg': n_of(lambda t: t.startswith('$match και')),
       's_having': n_of(lambda t: t.startswith('$match μετά')), 's_load': n_of(lambda t: t.startswith('Το persons.txt')),
       's_persons': n_of(lambda t: t.startswith('Οι τρεις νεότεροι')), 's_sqlcmd': n_of(lambda t: t.startswith('SQL και MongoDB: εντολές')),
       's_map': n_of(lambda t: t.startswith('Εργασία 2: κάθε'))}
def fill(x):
    if isinstance(x, str):
        for k, v in REF.items(): x = x.replace('[[%s]]' % k, str(v))
        return x
    if isinstance(x, list): return [fill(y) for y in x]
    if isinstance(x, dict): return {k: fill(v) for k, v in x.items()}
    return x
S = [fill(s) for s in S]
skips = [i + 1 for i, s in enumerate(S) if s.get('skippable')]
tot = sum(s['mins'] for s in S)
assert tot == 45, tot
assert len(skips) == 2, skips
assert sum(1 for s in S if s['type'] == 'poll') == 1
assert 30 <= len(S) <= 35, len(S)
for s in S:
    t = json.dumps(s, ensure_ascii=False)
    assert '[[s_' not in t, s['title']
D = {'meta': {'course': 'Βάσεις Δεδομένων & Ανάλυση Δεδομένων Μάθησης', 'deckTitle': 'Ενημέρωση, διαγραφή και συνάθροιση',
              'part': 'Μη σχεσιακές βάσεις, Βραδιά 2, Μέρος 3', 'start': '20:15', 'lengthMin': 45, 'breakMin': 15, 'lang': 'el',
              'notesMarkup': True},
     'slides': S}
json.dump(D, open(os.path.join(H, '..', 'content', 'n2p3.json'), 'w', encoding='utf8'), ensure_ascii=False, indent=1)
print('slides', len(S), 'minutes', tot, 'skippable', skips, 'refs', REF)
