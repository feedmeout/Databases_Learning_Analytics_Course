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
    assert 2 <= len(k.get('notes', [])) <= 3, (k['title'], len(k.get('notes', [])))
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
# slide numbers of Evening 1 Part 3 and Evening 2 Part 1, read from their content files (Εργασία 2 map)
def where(part, pred):
    D = json.load(open(os.path.join(H, '..', 'content', part + '.json'), encoding='utf8'))
    hits = [i + 1 for i, s in enumerate(D['slides']) if pred(s['title'])]
    assert hits, (part, pred)
    return hits
rng = lambda h: str(h[0]) if len(h) == 1 else f'{h[0]}–{h[-1]}'
E1 = lambda *ts: where('n1p3', lambda t: any(t.startswith(x) for x in ts))
E2 = lambda *ts: where('n2p1', lambda t: any(t.startswith(x) for x in ts))

add(type='listslide', mins=1, title='Τι περιέχει το Μέρος 3',
    items=['Ενημέρωση εγγράφων: updateOne, updateMany, upsert.', 'Διαγραφή: deleteOne, deleteMany.',
           'Συνάθροιση: ροή σταδίων, στις συλλογές country, books και persons.',
           'Αντιστοίχιση SQL και MongoDB, και η Εργασία 2 ενότητα προς ενότητα.'],
    foot='Οι ενημερώσεις γίνονται στη συλλογή country της Βραδιάς 1: Ελλάδα, Γαλλία, Γερμανία.',
    notes=['Ακολουθεί το παλαιότερο υλικό (Μέρος Β, διαφάνειες 19 έως 26): ενημέρωση, $unset, συνάθροιση, το παράδειγμα persons, διαγραφή.',
           'Στις διαφάνειες «Δοκιμάστε» οι εντολές εκτελούνται από όποιον έχει τη συλλογή country της Βραδιάς 1· οι υπόλοιποι παρακολουθούν την έξοδο στη διαφάνεια.'])

add(type='shell', mins=2, dense=True, kicker='Δοκιμάστε', kickerTone='green', title='updateOne και $set',
    cmd=cmd('upd_set'), cmdLabel='Εντολές', out=out('upd_set'), outLabel='Αποτελέσματα',
    points=['Πρώτο όρισμα: το φίλτρο. Δεύτερο: η αλλαγή, με τελεστή.',
            '`$set` προσθέτει το πεδίο capital· αν υπήρχε, θα άλλαζε την τιμή του.',
            'Εργασία 2, ενότητα 11.'],
    src='MongoDB Manual: db.collection.updateOne().',
    notes=['Η Ελλάδα αποκτά εμφωλευμένο έγγραφο πρωτεύουσας, όπως η Γαλλία και η Γερμανία στη Βραδιά 1.',
           'Το παλαιότερο υλικό όριζε εδώ το yearOfIndipendence: 1821. Το πεδίο αφαιρέθηκε στη Βραδιά 1, γιατί είχε λάθος ορθογραφία και τιμές χωρίς νόημα για τις άλλες χώρες.'])

add(type='shell', mins=1, dense=True, title='matchedCount και modifiedCount',
    cmd=cmd('upd_again'), cmdLabel='Η ίδια εντολή, δεύτερη φορά', out=out('upd_again'),
    points=['Βρέθηκε ένα έγγραφο (`matchedCount: 1`), αλλά δεν άλλαξε (`modifiedCount: 0`): η τιμή ήταν ήδη αυτή.',
            'Με `matchedCount: 0`, το φίλτρο δεν βρήκε τίποτε: π.χ. "greece" με πεζό.'],
    notes=['Το αποτέλεσμα κάθε ενημέρωσης είναι ο πρώτος έλεγχος ότι έγινε αυτό που θέλαμε.',
           'Στην Εργασία 2, το στιγμιότυπο του αποτελέσματος δείχνει ακριβώς αυτούς τους αριθμούς.'])

add(type='shell', mins=1, dense=True, title='$inc και $push',
    cmd=cmd('upd_incpush'), cmdLabel='Εντολές', out=out('upd_incpush'), outLabel='Αποτελέσματα',
    points=['`$inc`: αυξάνει έναν αριθμό· αν το πεδίο λείπει, το δημιουργεί.',
            '`$push`: προσθέτει στοιχείο σε λίστα· αν η λίστα λείπει, τη δημιουργεί.',
            'Δύο τελεστές στην ίδια ενημέρωση.'],
    src='MongoDB Manual: Field and Array Update Operators.',
    notes=['Το visits είναι ένας μετρητής για το παράδειγμα· αφαιρείται στην επόμενη διαφάνεια.',
           'Το findOne με { _id: 0 } δείχνει όλο το έγγραφο χωρίς το _id.'])

add(type='shell', mins=1, title='$unset: αφαίρεση πεδίου',
    cmd=cmd('upd_unset'), out=out('upd_unset'),
    points=['Το πεδίο visits αφαιρείται· η τιμή μετά το όνομα δεν έχει σημασία, συνήθως "".',
            'Με updateMany, το ίδιο πεδίο αφαιρείται από όλα τα έγγραφα που ταιριάζουν (διαφάνεια [[s_many]]).'],
    notes=['Στο παλαιότερο υλικό: updateOne({ name: "Greece" }, { $unset: { yearOfIndipendence2: "" } }).',
           'Στον πίνακα αντιστοίχισης της SQL, το $unset σε όλα τα έγγραφα αντιστοιχεί στο ALTER TABLE … DROP COLUMN.'])

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
    notes=['Οι τελεστές που χρειάζονται για την ενότητα 11 της Εργασίας 2· το εγχειρίδιο έχει και άλλους ($min, $max, $mul, $currentDate).',
           'Όλοι δουλεύουν το ίδιο με updateOne και updateMany.'])

add(type='shell', mins=1, dense=True, kicker='Προσοχή', title='updateOne: μόνο το πρώτο έγγραφο',
    cmd=cmd('upd_one_first') + '\n' + cmd('upd_many_founder'), cmdLabel='Εντολές', out=out('upd_one_first') + '\n' + out('upd_many_founder'), outLabel='Αποτελέσματα',
    points=['Γαλλία και Γερμανία έχουν euSince 1958· το updateOne άλλαξε μόνο την πρώτη.',
            'Το updateMany βρήκε και τις δύο (`matchedCount: 2`) και άλλαξε όποια δεν είχε ήδη την τιμή (`modifiedCount: 1`).'],
    notes=['founder: true σημαίνει ιδρυτικό μέλος της ΕΟΚ (1958).',
           'Αν ένα φίλτρο μπορεί να ταιριάξει σε πολλά έγγραφα, το updateOne αλλάζει ένα από αυτά, χωρίς προειδοποίηση.'])

add(type='shell', mins=1, dense=True, title='updateMany: από «0 σελίδες» σε «άγνωστο»',
    cmd=cmd('upd_many_books'), cmdLabel='Εντολές', out=out('upd_many_books'), outLabel='Αποτελέσματα',
    points=['Ένα φίλτρο, πολλά έγγραφα: και τα %s βιβλία με 0 σελίδες.' % ZEROS,
            'Τώρα το «άγνωστο» είναι πεδίο που λείπει, όχι ψεύτικο 0: δεν μετρά στους μέσους όρους.',
            'Επαναφορά του αρχείου: `mongoimport … --drop`.'],
    notes=['Καθαρισμός δεδομένων με μία εντολή: το ζήτημα των μηδενικών του Μέρους 1.',
           'Το $exists: false βρίσκει τα έγγραφα που δεν έχουν το πεδίο.'])

add(type='shell', mins=2, dense=True, kicker='Δοκιμάστε', kickerTone='green', title='upsert: η Κύπρος επιστρέφει',
    cmd=cmd('upsert'), cmdLabel='Εντολές', out=out('upsert'), outLabel='Αποτελέσματα',
    points=['Κανένα έγγραφο δεν ταίριαξε: με `upsert: true` δημιουργείται νέο.',
            'Το νέο έγγραφο παίρνει το name από το φίλτρο και το population από το `$set`.'],
    src='MongoDB Manual: db.collection.updateOne() (upsert).',
    notes=['Η Κύπρος είχε διαγραφεί στη Βραδιά 1. Το upsert είναι «ενημέρωσε αν υπάρχει, αλλιώς δημιούργησε».',
           'Χρήσιμο όταν δεν ξέρουμε αν το έγγραφο υπάρχει ήδη, π.χ. σε επαναλαμβανόμενες εισαγωγές.'])

add(type='poll', mins=2, timerSec=60, kicker='Ερώτημα', title='Τι κάνει αυτή η εντολή;',
    context='Η Ελλάδα έχει ήδη πέντε πεδία.',
    code=cmd('poll'),
    options=['Αλλάζει μόνο τον πληθυσμό', 'Αντικαθιστά όλο το έγγραφο', 'Εμφανίζει σφάλμα', 'Δεν κάνει τίποτε, χωρίς μήνυμα'],
    notes=['Δημοσκόπηση Zoom, μία επιλογή. Ξεκινήστε το χρονόμετρο (πλήκτρο T). Τα πέντε πεδία: name, euSince, population, capital, languages.',
           'Η απάντηση είναι στην επόμενη διαφάνεια.'])

add(type='shell', mins=1, title='Η απάντηση: σφάλμα',
    cmd=cmd('poll'), out=POLL_ERR,
    points=['Το updateOne θέλει τελεστή: `$set`, `$inc`, `$unset`…',
            'Για αντικατάσταση ολόκληρου του εγγράφου υπάρχει το `replaceOne`.',
            'Προσοχή σε παλιούς οδηγούς: το `update()` χωρίς τελεστή αντικαθιστούσε όλο το έγγραφο.'],
    src='MongoDB Manual: db.collection.updateOne()· db.collection.replaceOne()· db.collection.update().',
    notes=['Κανένα έγγραφο δεν αλλάζει: το σφάλμα εμφανίζεται πριν σταλεί η εντολή.',
           'Με το replaceOne θα έμενε μόνο το population (και το _id): χάνονται τα υπόλοιπα πεδία.'])

add(type='shell', mins=1, skippable=True, kicker='Προσοχή', title='Πριν από κάθε μαζική διαγραφή: μέτρηση',
    cmd=cmd('count_first'), out=out('count_first'),
    points=['Πρώτα `countDocuments` με το φίλτρο της διαγραφής: 1, η Κύπρος.',
            '`deleteMany({})` και `updateMany({}, …)` αφορούν όλη τη συλλογή, χωρίς επιβεβαίωση και χωρίς αναίρεση.'],
    notes=['Αν ο αριθμός δεν είναι ο αναμενόμενος, το φίλτρο διορθώνεται πριν από τη διαγραφή.',
           'Αν ο χρόνος πιέζει, η διαφάνεια παραλείπεται· ο κανόνας είναι στο «Να θυμάστε».'])

add(type='shell', mins=1, title='deleteMany και deleteOne',
    cmd=cmd('delmany'), out=out('delmany'),
    points=['`deleteMany`: όλα όσα ταιριάζουν· εδώ ένα, η Κύπρος.',
            '`deleteOne`: μόνο το πρώτο, όπως στη Βραδιά 1.',
            'Εργασία 2, ενότητα 12.'],
    src='MongoDB Manual: db.collection.deleteMany().',
    notes=['Στο παλαιότερο υλικό: deleteOne({ name: "Greece" }).',
           'Η συλλογή country είναι πάλι όπως στο τέλος της Βραδιάς 1, με τις ενημερώσεις της Ελλάδας και των ιδρυτικών μελών.'])

add(type='stack', mins=1, title='Συνάθροιση: ροή σταδίων',
    stages=[{'h': '$match', 't': 'Φιλτράρει έγγραφα, όπως το φίλτρο του find.'},
            {'h': '$group', 't': 'Ομαδοποιεί και υπολογίζει ανά ομάδα: πλήθος, άθροισμα, μέσο όρο, ελάχιστο, μέγιστο.'},
            {'h': '$sort, $limit, $project', 't': 'Ταξινομούν, περιορίζουν και διαμορφώνουν την έξοδο.'}],
    codeLabel='Σύνταξη', code='db.συλλογή.aggregate([\n  { στάδιο 1 },\n  { στάδιο 2 },\n  …\n])',
    foot='Η έξοδος κάθε σταδίου είναι η είσοδος του επόμενου.',
    src='MongoDB Manual: Aggregation Pipeline.',
    notes=['Η διαφάνεια 23 του παλαιότερου υλικού σε τρία σημεία: στάδια, κάθε στάδιο μία λειτουργία, αποτελέσματα ανά ομάδα.',
           'Το find απαντά «ποια έγγραφα»· η συνάθροιση απαντά «πόσα, πόσο, κατά μέσο όρο, ανά τι».'])

add(type='shell', mins=2, dense=True, title='$group: ο συνολικός πληθυσμός',
    cmd=cmd('agg_total'), out=out('agg_total'),
    points=['`_id: null`: μία μόνο ομάδα, όλα τα έγγραφα μαζί.',
            '`"$population"`: η τιμή του πεδίου· το $ μπροστά από το όνομα.',
            'Ελλάδα, Γαλλία και Γερμανία: %s.' % gr(TOTAL)],
    src='MongoDB Manual: $group (aggregation).',
    notes=['Το παράδειγμα της διαφάνειας 22 του παλαιότερου υλικού, με τους πληθυσμούς της Eurostat που μπήκαν στη Βραδιά 1.',
           'Στην SQL: SELECT SUM(population) FROM country.'])

add(type='shell', mins=1, title='$group ανά πεδίο: βιβλία ανά κατάσταση',
    cmd=cmd('agg_status'), cmdLabel='Εντολές', out=out('agg_status'), outLabel='Αποτελέσματα',
    points=['`_id: "$status"`: μία ομάδα για κάθε τιμή του status.',
            '`$sum: 1`: μετρά τα έγγραφα κάθε ομάδας, όπως το COUNT(*) με GROUP BY.',
            'Εργασία 2, ενότητα 10.'],
    notes=['Η σειρά των ομάδων στην έξοδο δεν είναι εγγυημένη· για σταθερή σειρά χρειάζεται $sort.',
           'Στην SQL: SELECT status, COUNT(*) FROM books GROUP BY status.'])

add(type='shell', mins=1, dense=True, title='$match και συσσωρευτές',
    cmd=cmd('agg_java'), out=out('agg_java'),
    points=['`$match` πρώτο: μόνο τα βιβλία Java, όπως το WHERE.',
            '`$avg` και `$max`: μέσος όρος και μέγιστο ανά ομάδα.',
            'Το `$avg` αγνοεί τα βιβλία που δεν έχουν πλέον pageCount (διαφάνεια [[s_many]]).'],
    src='MongoDB Manual: $avg (aggregation).',
    notes=['Μόνο ένα βιβλίο Java σε MEAP έχει γνωστό αριθμό σελίδων· γι’ αυτό ο μέσος όρος και το μέγιστο συμπίπτουν.',
           'Ο μέσος όρος έχει πολλά δεκαδικά: η στρογγυλοποίηση γίνεται με $project, στη διαφάνεια [[s_project]].'])

add(type='shell', mins=2, dense=True, title='$unwind: ένα έγγραφο ανά κατηγορία',
    cmd=cmd('agg_unwind'), out=out('agg_unwind'),
    points=['`$unwind`: ένα έγγραφο για κάθε κατηγορία κάθε βιβλίου.',
            'Μετά: ομάδα ανά κατηγορία, ταξινόμηση, τα πέντε πρώτα.',
            'Βιβλία χωρίς κατηγορία δεν περνούν από το `$unwind`.'],
    src='MongoDB Manual: $unwind (aggregation).',
    notes=['Χωρίς $unwind, το $group θα έφτιαχνε ομάδες ανά ολόκληρη λίστα κατηγοριών, όχι ανά κατηγορία.',
           'Στην SQL, το ίδιο θα απαιτούσε πίνακα κατηγοριών και JOIN.'])

add(type='shell', mins=1, dense=True, title='$match μετά το $group: το HAVING',
    cmd=cmd('agg_having'), out=out('agg_having'),
    points=['`$match` μετά το `$group` φιλτράρει ομάδες, όπως το HAVING της SQL.',
            'Κατηγορίες με τουλάχιστον 12 βιβλία: %s.' % {7: 'επτά'}.get(HAVING_N, HAVING_N),
            '`_id: 1` στο `$sort`: σταθερή σειρά στις ισοπαλίες.'],
    notes=['Η σειρά των σταδίων μετρά: το ίδιο $match πριν από το $group θα έψαχνε πεδίο books στα βιβλία, και δεν θα έβρισκε τίποτε.',
           'Business και Programming έχουν από 12 βιβλία· χωρίς το _id: 1 η σειρά τους μπορεί να αλλάζει.'])

add(type='shell', mins=1, dense=True, title='$project: το σχήμα της εξόδου',
    cmd=cmd('agg_project'), out=out('agg_project'),
    points=['`$project`: ποια πεδία βγαίνουν και με ποιο όνομα· το `_id` γίνεται status.',
            '`$round`: στρογγυλοποίηση του μέσου όρου.',
            'Ό,τι είναι το SELECT για την SQL.'],
    src='MongoDB Manual: $project· $round (aggregation).',
    notes=['Το books: 1 κρατά το πεδίο όπως είναι· το status: "$_id" δημιουργεί νέο πεδίο από υπάρχουσα τιμή.',
           'Η σειρά των πεδίων στην έξοδο ακολουθεί τη σειρά του εισερχόμενου εγγράφου για όσα κρατούνται.'])

add(type='shell', mins=1, dense=True, title='Το persons.txt στο mongosh',
    cmd='db = db.getSiblingDB("book-filtered-top-subset");\ndb.dropDatabase();\ndb.persons.createIndex({"vocation": 1, "dateofbirth": 1});\ndb.persons.insertMany([ … έξι άτομα … ]);',
    cmdLabel='Το αρχείο persons.txt', out=out('persons_load'), outLabel='Αποτέλεσμα της τελευταίας εντολής',
    points=['Ανοίξτε το αρχείο, αντιγράψτε όλο το περιεχόμενο και επικολλήστε το στο mongosh.',
            'Νέα βάση με έξι άτομα· η διεύθυνση είναι εμφωλευμένο έγγραφο.',
            'Εναλλακτικά: `load("persons.txt")`, με το mongosh ανοιγμένο στον φάκελο του αρχείου.'],
    notes=['Όπως στο παλαιότερο υλικό: «Εισάγετε τα περιεχόμενα του αρχείου persons.txt».',
           'Η πρώτη γραμμή του αρχείου άλλαξε: με το use book-filtered-top-subset; το επικόλλημα λειτουργούσε, αλλά το load() άφηνε το mongosh σε βάση με ερωτηματικό στο όνομα, χωρίς τα άτομα. Με το db.getSiblingDB λειτουργούν και οι δύο τρόποι.'])

add(type='shell', mins=2, dense=True, side=True, title='Οι τρεις νεότεροι μηχανικοί',
    cmd=cmd('persons_pipeline', [1, 2]), cmdLabel='Εντολές', out=out('persons_pipeline', [2]),
    foot='Φιλτράρει τους μηχανικούς, ταξινομεί από τον νεότερο, κρατά τρεις και αφαιρεί τρία πεδία.',
    src='Paul Done, Practical MongoDB Aggregations: «Filtered Top Subset».',
    notes=['Οι διαφάνειες 24 και 25 του παλαιότερου υλικού, χωρίς τα αγγλικά σχόλια του πρωτοτύπου.',
           'Η μεταβλητή pipeline κρατά τη λίστα των σταδίων: η Εργασία 2 ζητά μεταβλητές σε κάποια ερωτήματα.'])

add(type='codeslide', mins=1, title='$unset ως στάδιο',
    code='// με $unset\n{ $unset: ["_id", "vocation", "address"] }\n\n// με $project\n{ $project: {\n    _id: 0, vocation: 0, address: 0 } }',
    points=['Και τα δύο δίνουν τους ίδιους τρεις μηχανικούς.',
            '`$unset`: γράφει μόνο όσα αφαιρούνται.',
            '`$project`: και για προσθήκη ή μετονομασία πεδίων (διαφάνεια [[s_project]]).'],
    src='MongoDB Manual: $unset (aggregation).',
    notes=['Το εγχειρίδιο: το στάδιο $unset είναι ψευδώνυμο του $project που αφαιρεί πεδία.',
           'Στην Εργασία 2, οποιοδήποτε από τα δύο είναι σωστό.'])

add(type='shell', mins=1, dense=True, side=True, skippable=True, title='Το ίδιο με find',
    cmd=cmd('persons_find'), out=out('persons_find'),
    foot='Χωρίς ομαδοποίηση, το find αρκεί· η συνάθροιση χρειάζεται όταν υπολογίζουμε ανά ομάδα.',
    notes=['Κατά το βιβλίο από όπου προέρχεται, είναι το μόνο του παράδειγμα που γίνεται και χωρίς συνάθροιση.',
           'Αν ο χρόνος πιέζει, η διαφάνεια παραλείπεται.'])

add(type='definition', mins=1, kicker='Προσοχή', title='Η ενότητα 10 ζητά ομαδοποίηση',
    quote='Ερώτημα με pipeline που παρουσιάζει συγκεντρωτικά, ομαδοποιημένα αποτελέσματα.',
    cite='Εργασία 2, ενότητα 10',
    callouts=[{'tone': 'amber', 'h': 'Το παράδειγμα του persons', 't': '$match, $sort, $limit, $unset: φιλτράρει και ταξινομεί, αλλά δεν ομαδοποιεί.'},
              {'tone': 'blue', 'h': 'Για την Εργασία 2', 't': 'Τουλάχιστον ένα $group, με τα δικά σας δεδομένα, όπως στις διαφάνειες [[s_group_first]] έως [[s_project]].'}],
    notes=['Μόνο το παράδειγμα του persons, όπως ήταν στο παλαιότερο υλικό, δεν καλύπτει την ενότητα 10.',
           'Η επόμενη διαφάνεια προσθέτει ομαδοποίηση στην ίδια συλλογή.'])

add(type='shell', mins=1, dense=True, side=True, title='Ομαδοποίηση στο persons: άτομα ανά επάγγελμα',
    cmd=cmd('persons_group'), out=out('persons_group'),
    foot='Μία ομάδα ανά επάγγελμα: πόσα άτομα, και η παλαιότερη ημερομηνία γέννησης (`$min`).',
    notes=['Με $sort κατά πλήθος και, στις ισοπαλίες, κατά όνομα επαγγέλματος.',
           'Στην SQL: SELECT vocation, COUNT(*), MIN(dateofbirth) FROM persons GROUP BY vocation.'])

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
    notes=['Ο πίνακας συνοψίζει τη σελίδα που χρησιμοποίησε η ομαδική άσκηση του Μέρους 2.',
           'Η σελίδα γράφει ακόμη count() για το SELECT COUNT(*): στο σημερινό mongosh, countDocuments().'])

add(type='htable', mins=2, compact=True, title='SQL και MongoDB: συνάθροιση',
    head=['SQL', 'Συνάθροιση στη MongoDB'],
    rows=[['`WHERE`', '`$match`'], ['`GROUP BY`', '`$group`'], ['`HAVING`', '`$match` μετά το `$group`'],
          ['`SELECT`', '`$project`'], ['`ORDER BY`', '`$sort`'], ['`LIMIT`', '`$limit`'],
          ['`SUM()`, `COUNT()`', '`$sum`, με `$sum: 1` για το πλήθος'], ['`JOIN`', '`$lookup`']],
    foot='Το `$lookup` συνδέει δύο συλλογές, όπως το JOIN. Η Εργασία 2 δεν το ζητά.',
    src='MongoDB Manual: SQL to Aggregation Mapping Chart.',
    notes=['Ο πίνακας του εγχειριδίου, με τις γραμμές που χρησιμοποιήθηκαν απόψε.',
           'Στο εγχειρίδιο, για το COUNT() αναφέρονται το $sum και το $sortByCount.'])

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
    notes=['«Μέρος» χωρίς βραδιά σημαίνει τη σημερινή, Βραδιά 2.',
           'Η ενότητα 8 δεν έχει δική της διαφάνεια: συνδυάζει τους τελεστές των ενοτήτων 5 και 6.'])

add(type='table', mins=1, title='Εργασία 2: τι παραδίδετε',
    rows=[{'h': 'Αναφορά', 't': 'Ονοματεπώνυμο, email, τίτλος· περιγραφή των τροποποιήσεων της βάσης της Εργασίας 1 και των πινάκων (τουλάχιστον 2, ο ένας εμφωλευμένος στον άλλον).'},
          {'h': 'Ενότητες 1 έως 12', 't': 'Αριθμημένες όπως στην εκφώνηση· για κάθε κώδικα, μία παράγραφος που εξηγεί τι κάνει και στιγμιότυπο οθόνης με το αποτέλεσμα.'},
          {'h': 'JSON και μεταβλητές', 't': 'Σε κάποια ερωτήματα, ευανάγνωστο JSON και μεταβλητές, με κείμενο που το επισημαίνει.'},
          {'h': 'Προθεσμία', 't': 'Στην πλατφόρμα του μαθήματος.'}],
    src='Εκφώνηση της Εργασίας 2 (MongoDB).',
    notes=['Οι απαιτήσεις είναι ακριβώς όπως στην εκφώνηση του συναδέλφου· διορθώθηκε μόνο η διατύπωση.',
           'Καμία ημερομηνία στη διαφάνεια: η προθεσμία ορίζεται στην πλατφόρμα.'])

add(type='remember', mins=1, kicker='Να θυμάστε', title='Τρία σημεία από το Μέρος 3',
    items=['Κάθε ενημέρωση έχει φίλτρο και τελεστή: το updateOne αλλάζει το πρώτο έγγραφο, το updateMany όλα, και χωρίς τελεστή εμφανίζεται σφάλμα.',
           'Η συνάθροιση είναι ροή σταδίων: το $match φιλτράρει, το $group ομαδοποιεί, τα $sort, $limit και $project διαμορφώνουν την έξοδο.',
           'Πριν από κάθε μαζική αλλαγή ή διαγραφή, countDocuments με το ίδιο φίλτρο.'],
    notes=['Διαβάστε τα τρία σημεία. Τίποτε άλλο.',
           'Ακολουθεί η τελευταία διαφάνεια, με τα λεπτά για ερωτήσεις.'])

add(type='endslide', mins=5, title='Ερωτήσεις',
    line='Εδώ κλείνουν οι μη σχεσιακές βάσεις δεδομένων. Στο επόμενο μάθημα ξεκινά η Μαθησιακή Αναλυτική.',
    notes=['Η διαφάνεια κρατά το περιθώριο της βραδιάς: περίπου 5 λεπτά για ερωτήσεις, κυρίως για την Εργασία 2.',
           'Αν δεν ρωτά κανείς: «Ποια ενότητα της Εργασίας 2 σας φαίνεται η δυσκολότερη;»'])

def n_of(pred):
    hits = [i + 1 for i, s in enumerate(S) if pred(s['title'])]
    assert len(hits) == 1, hits
    return hits[0]
REF = {'s_many': n_of(lambda t: t.startswith('updateMany')), 's_project': n_of(lambda t: t.startswith('$project')),
       's_group_first': n_of(lambda t: t.startswith('$group: ο συνολικός')), 's_pgroup': n_of(lambda t: t.startswith('Ομαδοποίηση στο persons')),
       's_upsert': n_of(lambda t: t.startswith('upsert')), 's_del': n_of(lambda t: t.startswith('deleteMany'))}
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
              'part': 'Μη σχεσιακές βάσεις, Βραδιά 2, Μέρος 3', 'start': '20:15', 'lengthMin': 45, 'breakMin': 15, 'lang': 'el'},
     'slides': S}
json.dump(D, open(os.path.join(H, '..', 'content', 'n2p3.json'), 'w', encoding='utf8'), ensure_ascii=False, indent=1)
print('slides', len(S), 'minutes', tot, 'skippable', skips, 'refs', REF)
