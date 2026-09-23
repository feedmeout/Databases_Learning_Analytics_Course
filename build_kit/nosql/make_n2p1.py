# NoSQL, Evening 2, Part 1: "Ερωτήματα στη συλλογή books" -> ../content/n2p1.json
# Commands: e2p1_cmds.py. Outputs: e2p1_outputs.json, written by run_e2p1.py from a real run
# (MongoDB Community 8.0.32, mongosh 2.12.0, Database Tools 100.19.0). Nothing below types an output by hand.
# Follows the colleague's NoSQL Part B: find and projection, printjson, variables, comparison, logical, limit and sort,
# Database Tools and mongoimport, Άσκηση 1 and Άσκηση 2 with their solutions. Arrays, regex, dot notation and skip come
# from the approved plan; his optional exercises (B36-39) and his group task (B35) are kept for Part 2.
import json, os
from e2p1_cmds import CMDS, IMPORT
H = os.path.dirname(os.path.abspath(__file__))
O = json.load(open(os.path.join(H, 'e2p1_outputs.json'), encoding='utf8'))
S = []

def add(**k):
    assert 2 <= len(k.get('notes', [])) <= 4, (k['title'], len(k.get('notes', [])))
    S.append(k)

def cmd(key, idx=None):
    st = CMDS[key]
    return '\n'.join(st if idx is None else [st[i] for i in idx])

def out(key, idx=None):
    o = O[key]
    return '\n'.join(x for x in (o if idx is None else [o[i] for i in idx]) if x != '')

def one(key, i=0):
    return O[key][i]

# the numbers quoted in text, read from the real run
N = {k: one(k) for k in ['total', 'in', 'not', 'lt400', 'all', 'dotall', 'escape', 'piter']}
MEAP, ZERO, MEAP0, INTERNET, INTERNET_LC = O['counts']
EX1, EX1FIX = one('ex1', 1), one('ex1fix')
EXACT_ALL, EXACT_ONLY = O['exact']
CHRIS, CHRIS_NOT_CB = O['elem']
PETER, PETER_SIMPLE = O['ex2']
SAME_WRONG, SAME_RIGHT, SAME_AND = O['samefield']
REGEX = O['regex']
THE, EDITION = one('symbols', 0), one('symbols', 1)
INT_IDS, OID_IDS = O['idtypes']
assert N['total'] == '431' and SAME_RIGHT == SAME_AND and N['lt400'] == SAME_WRONG and PETER == PETER_SIMPLE and N['piter'] == '0'
assert int(EXACT_ALL) - int(EXACT_ONLY) == 20 and int(EX1FIX) == int(EX1) + 1
IMPORT_OUT = O['import']
IMPORT_OK = IMPORT_OUT.split('\n')[-1].split('\t', 1)[1].split('. ')[0]
assert IMPORT_OUT.endswith('%s document(s) imported successfully. 0 document(s) failed to import.' % N['total'])
import re
_p = re.findall(r'pageCount: (\d+)', O['zerosfix'][0])
assert len(_p) == 3
PAGES3 = '%s, %s και %s' % tuple(_p)
SYNTAX_ERR = [l for l in O['import_in_mongosh'].split('\n') if l.startswith('SyntaxError')][0]
PROJ_ERR = [l for l in O['projerr'][0].split('\n') if 'MongoServerError' in l][0]
PROJ_ERR_MSG = PROJ_ERR.split(': ', 1)[1]
AGAIN_LAST = O['import_again_last'].split('\t', 1)[1]
assert AGAIN_LAST.startswith('0 document(s) imported successfully. 431 document(s) failed')

add(type='title', mins=1, title='Μη σχεσιακές βάσεις δεδομένων', subtitle='Ερωτήματα, ενημέρωση και συνάθροιση στη MongoDB',
    author='Αθανάσιος Χριστόπουλος, Ph.D.',
    affil='Αν. Καθηγητής, Τμήμα Φυσικών Επιστημών. Κέντρο Μαθησιακής Αναλυτικής, Πανεπιστήμιο του Τούρκου, Φινλανδία',
    email='atchri@utu.fi',
    notes=['Σύνδεση με την προηγούμενη βραδιά σε μία πρόταση: «Εγκαταστήσατε τη MongoDB και γράψατε τα πρώτα σας έγγραφα. Απόψε: ερωτήματα σε μια πραγματική συλλογή %s βιβλίων.»' % N['total'],
           'Απόψε καλύπτονται οι ενότητες 4 έως 11 της Εργασίας 2· οι ενότητες 1 έως 3 και 12 καλύφθηκαν στη Βραδιά 1.',
           'Ξεκινήστε ακριβώς στην ώρα: μετά το πλάνο, οι φοιτητές ξεκινούν δύο λήψεις.'])

add(type='plan', mins=1, title='Το πλάνο της βραδιάς',
    rows=[{'label': 'Μέρος 1', 'text': 'Ερωτήματα στη συλλογή books', 'now': True},
          {'label': 'Μέρος 2', 'text': 'Ομαδική άσκηση σε αίθουσες του Zoom'},
          {'label': 'Μέρος 3', 'text': 'Ενημέρωση, συνάθροιση, SQL και MongoDB'}],
    notes=['Μία φράση ανά μέρος, όχι περισσότερο.',
           'Το Μέρος 2 γίνεται στο mongosh του καθενός, με τη συλλογή που εισάγεται τώρα, στο Μέρος 1.'])

add(type='table', mins=1, title='Δύο λήψεις, τώρα', compact=True,
    rows=[{'h': 'MongoDB Database Tools', 't': '[mongodb.com/try/download/database-tools](https://www.mongodb.com/try/download/database-tools): Windows x86_64, πακέτο msi.'},
          {'h': 'books.json', 't': '[Λήψη του books.json](https://raw.githubusercontent.com/ozlerhakan/mongodb-json-files/master/datasets/books.json): στη σελίδα που ανοίγει, Ctrl+S και αποθήκευση ως books.json.'},
          {'h': 'macOS ή Linux', 't': '[Οδηγίες εγκατάστασης ανά σύστημα](https://www.mongodb.com/docs/database-tools/installation/).'}],
    foot='Ξεκινήστε τώρα και τις δύο λήψεις.',
    src='books.json: αποθετήριο ozlerhakan/mongodb-json-files, άδεια CC0.',
    notes=[           'Το books.json είναι σύνολο δεδομένων εξάσκησης από το δημόσιο αποθετήριο ozlerhakan/mongodb-json-files (άδεια CC0). Το αντίγραφο του μαθήματος έχει τα ίδια %s έγγραφα, με αλλαγές γραμμής των Windows.' % N['total'],
           'Στείλτε τους δύο συνδέσμους και στο chat του Zoom (δεξί κλικ στον σύνδεσμο, αντιγραφή): οι φοιτητές βλέπουν την οθόνη, δεν μπορούν να πατήσουν τον σύνδεσμο. Το ίδιο books.json είναι και στο υλικό της βραδιάς, για την πλατφόρμα.'])

add(type='work', mins=6, timerSec=360, title='Εγκατάσταση και εισαγωγή τώρα',
    context='Στα Windows:',
    items=['Εκτελέστε το msi των Database Tools, με τις προεπιλογές.',
           {'t': 'Ρυθμίσεις συστήματος για προχωρημένους → Μεταβλητές περιβάλλοντος → Path → Επεξεργασία. Νέα γραμμή:', 'code': 'C:\\Program Files\\MongoDB\\Tools\\100\\bin'},
           {'t': 'Νέο τερματικό, στον φάκελο του books.json:', 'code': IMPORT},
           'Στο chat: «ΟΚ», ή το μήνυμα λάθους.'],
    foot='Όποιος δεν τελειώσει, συνεχίζει παράλληλα με το μάθημα.',
    src='MongoDB Database Tools: Installation, Windows (msi, PATH).',
    notes=['Ξεκινήστε το χρονόμετρο (πλήκτρο T) και απαντάτε στο chat όσο διαρκεί. Τα συνηθισμένα λάθη και η λύση τους είναι στη διαφάνεια [[s_errors]].',
           'Στον φάκελο του αρχείου μπαίνουμε με cd, π.χ. cd Downloads. Η διαδρομή του Path είναι η προεπιλογή του msi· χωρίς αλλαγή στο Path δουλεύει και η πλήρης διαδρομή: "C:\\Program Files\\MongoDB\\Tools\\100\\bin\\mongoimport.exe" books.json -d library -c books --drop',
           'Όπως στο παλαιότερο υλικό: εγκατάσταση των εργαλείων, δήλωση της διαδρομής στο Path, εισαγωγή του books.json με το mongoimport.'])

add(type='shell', mins=1, title='Η εντολή mongoimport', dense=True,
    cmd=IMPORT, cmdLabel='Εντολή, στο τερματικό', out=IMPORT_OUT, outLabel='Αποτέλεσμα',
    points=['`-d library`: η βάση. `-c books`: η συλλογή. Δημιουργούνται με την εισαγωγή.',
            '`--drop`: αδειάζει πρώτα τη συλλογή, ώστε μια δεύτερη εισαγωγή να μη βρει διπλά.',
            'Εκτελείται στο τερματικό του συστήματος, όχι μέσα στο mongosh.'],
    stack=True,
    src='MongoDB Database Tools: mongoimport.',
    notes=['**`%s`**: Η εντολή της διαφάνειας [[s_install]]. Γράφεται στο τερματικό του συστήματος, όχι στο mongosh.' % IMPORT,
           '**`%s`**: Αυτό πρέπει να δει ο καθένας στο τερματικό του. Η ώρα στην αρχή κάθε γραμμής θα είναι διαφορετική.' % IMPORT_OK,
           '**`-d library`**, **`-c books`**: Η εισαγωγή δημιουργεί τη βάση library και τη συλλογή books. Με αυτά τα ονόματα τις βρίσκουμε στο mongosh.',
           '**`--drop`**: Αν κάποιος εκτελέσει την εντολή δεύτερη φορά, η συλλογή αδειάζει πρώτα και τα %s βιβλία φορτώνονται ξανά.' % N['total']])

add(type='table', mins=1, skippable=True, kicker='Προσοχή', title='Τρία συνηθισμένα λάθη', compact=True,
    rows=[{'h': 'Μέσα στο mongosh', 't': 'Σφάλμα `%s`: το mongoimport γράφεται στο τερματικό, όχι στο mongosh.' % SYNTAX_ERR.split('.')[0]},
          {'h': 'Δεύτερη εισαγωγή', 't': 'Χωρίς `--drop`, όλα απορρίπτονται ως διπλά (`E11000 duplicate key error`). Η συλλογή μένει σωστή, με %s έγγραφα.' % N['total']},
          {'h': '«Δεν αναγνωρίζεται»', 't': 'Το τερματικό δεν βρίσκει το mongoimport: η διαδρομή δεν μπήκε στο Path, ή το τερματικό ήταν ήδη ανοιχτό. Ανοίξτε νέο.'}],
    notes=['Αν ο χρόνος πιέζει, η διαφάνεια παραλείπεται: τα ίδια λάθη εμφανίζονται στο chat κατά την εγκατάσταση.',
           'Το τρίτο μήνυμα διαφέρει ανάλογα με το τερματικό (Γραμμή εντολών ή PowerShell) και τη γλώσσα των Windows.',
           'Τέταρτο πιθανό λάθος: «error connecting to host» σημαίνει ότι ο διακομιστής δεν τρέχει (Υπηρεσίες των Windows, MongoDB Server, Έναρξη), όπως στη Βραδιά 1.'])

add(type='shell', mins=1, title='Ένα βιβλίο της συλλογής',
    cmd=cmd('book23'), cmdLabel='Εντολές, στο mongosh', out=out('book23'), outLabel='Αποτελέσματα',
    foot='Κείμενα, αριθμοί, μια ημερομηνία (Date) και δύο λίστες, authors και categories. Άλλα βιβλία έχουν και isbn, shortDescription, longDescription.',
    notes=['**`use library`**: Περνάμε στη βάση που δημιούργησε το mongoimport. Το mongosh απαντά `switched to db library`.',
           '**`db.books.findOne({ _id: 23 })`**: Φέρνει ένα μόνο έγγραφο, το βιβλίο με `_id` 23.',
           '**Κείμενα, αριθμοί, μια ημερομηνία (Date) και δύο λίστες**: Για παράδειγμα `title`, `pageCount`, `publishedDate`, `authors` και `categories`. '
           'Τα βιβλία της ίδιας συλλογής δεν έχουν όλα τα ίδια πεδία.',
           'Αν ρωτήσουν: γιατί το `_id` είναι αριθμός; Το ορίζει το ίδιο το books.json: ακέραιο σε %s βιβλία, ObjectId στα %s.' % (INT_IDS, OID_IDS)])

add(type='shell', mins=1, title='Πριν από τα ερωτήματα: μετρήσεις',
    cmd=cmd('counts'), cmdLabel='Εντολές', out=out('counts'), outLabel='Αποτελέσματα',
    points=['%s βιβλία είναι σε MEAP: γράφονται ακόμη και δεν έχουν κυκλοφορήσει.' % MEAP,
            '%s βιβλία έχουν 0 σελίδες: ο αριθμός είναι άγνωστος. Τα %s είναι βιβλία MEAP.' % (ZERO, MEAP0),
            'Η κατηγορία «Internet» έχει %s βιβλία· με πεζά, «internet», υπάρχει ακόμη %s.' % (INTERNET, 'ένα' if INTERNET_LC == '1' else INTERNET_LC)],
    notes=['**`countDocuments`**: Μετρά τα έγγραφα χωρίς να τα εμφανίζει, όπως στη Βραδιά 1. Κάθε αριθμός στα Αποτελέσματα αντιστοιχεί σε μία εντολή, με τη σειρά.',
           '**%s βιβλία είναι σε MEAP**: Τα %s από αυτά έχουν ακόμη 0 σελίδες, όπως δείχνει η επόμενη γραμμή.' % (MEAP, MEAP0),
           '**%s βιβλία έχουν 0 σελίδες**: Εδώ το 0 σημαίνει «άγνωστο». Θα το ξαναβρούμε στην ταξινόμηση, στη διαφάνεια [[s_zeros]].' % ZERO,
           '**Η κατηγορία «Internet» έχει %s βιβλία**: Η σύγκριση ξεχωρίζει κεφαλαία από πεζά, άρα το «internet» είναι άλλη τιμή.' % INTERNET])

add(type='shell', mins=1, title='Προβολή: ποια πεδία εμφανίζονται', dense=True,
    cmd=cmd('proj1'), out=out('proj1'),
    points=['Δεύτερο όρισμα του find: η προβολή. Με 1 εμφανίζεται ένα πεδίο.',
            'Το `_id` εμφανίζεται πάντα, εκτός αν το αποκλείσουμε.',
            'Εργασία 2, ενότητα 4.'],
    src='MongoDB Manual: Project Fields to Return from Query.',
    notes=['Όπως στο παλαιότερο υλικό, με τη συλλογή country: find({ name: "Greece" }, { name: 1, population: 1 }). Εδώ με φίλτρο: τα 6 βιβλία της κατηγορίας Python.',
           'Στην SQL, η προβολή είναι η λίστα στηλών μετά το SELECT.'])

add(type='shell', mins=1, title='Χωρίς `_id`, και εξαίρεση πεδίων', dense=True,
    cmd=cmd('proj2'), out=out('proj2'),
    points=['`_id: 0`: το μόνο πεδίο που αποκλείεται μέσα σε προβολή με 1.',
            'Εξαίρεση: `{ longDescription: 0 }` δείχνει όλα τα πεδία εκτός από αυτό.',
            '1 και 0 μαζί δεν επιτρέπονται: «%s».' % PROJ_ERR_MSG],
    src='MongoDB Manual: Project Fields to Return from Query.',
    notes=['Το σφάλμα εμφανίζεται με: %s' % cmd('projerr'),
           'Στο παλαιότερο υλικό: find({ name: "Cyprus" }, { population: 0 }), δηλαδή εξαίρεση πεδίου.'])

add(type='shell', mins=1, title='Ευανάγνωστο JSON: printjson', dense=True,
    cmd=cmd('printjson'), out=out('printjson'),
    points=['`forEach(printjson)`: τυπώνει κάθε έγγραφο χωριστά, ένα πεδίο ανά γραμμή.',
            'Η Εργασία 2 το ζητά σε κάποια ερωτήματα: σημειώστε στην αναφορά πού το χρησιμοποιήσατε.',
            'Το `forEach(printjson)` μπαίνει στο τέλος, μετά το `sort` ή το `limit`.'],
    src='mongosh: Native Methods (print, printjson).',
    notes=['Για αυστηρό JSON, π.χ. για άλλο πρόγραμμα: EJSON.stringify(έγγραφο, null, 2). Για την Εργασία 2 αρκεί το printjson.',
           'Στο στιγμιότυπο του παλαιότερου υλικού το _id εμφανιζόταν ως {}· στο σημερινό mongosh εμφανίζεται ο κωδικός του, π.χ. ObjectId(\'53c2ae8528d75d572c06ad9d\').',
           'Το .pretty() των παλαιών οδηγών λειτουργεί ακόμη· η έξοδος του mongosh όμως είναι ήδη μορφοποιημένη.'])

add(type='shell', mins=1, title='Μεταβλητές',
    cmd=cmd('vars'), out=out('vars'), outLabel='Αποτελέσματα των δύο τελευταίων εντολών',
    points=['Η μεταβλητή κρατά ένα φίλτρο, μια προβολή ή ένα αποτέλεσμα, και ξαναχρησιμοποιείται.',
            'Ισχύει μόνο όσο είναι ανοιχτό το mongosh.',
            'Η Εργασία 2 ζητά μεταβλητές σε κάποια ερωτήματα: σημειώστε το στην αναφορά.'],
    notes=['Το παλαιότερο υλικό έβαζε σε μεταβλητή μια λίστα εγγράφων και την εισήγαγε με insert(). Σήμερα: var countries = [ … ]; db.country.insertMany(countries). Το insert() λειτουργεί με προειδοποίηση απόσυρσης.',
           'Εκτός από var δουλεύουν και let και const. Στο mongosh μια δήλωση μπορεί να επαναληφθεί χωρίς σφάλμα.'])

add(type='htable', mins=1, title='Τελεστές σύγκρισης', compact=True,
    head=['Τελεστής', 'Επιλέγει τιμές', 'SQL'],
    rows=[['`$eq`', 'ίσες με μια τιμή', '`=`'],
          ['`$ne`', 'διαφορετικές από μια τιμή', '`<>`'],
          ['`$gt`', 'μεγαλύτερες', '`>`'],
          ['`$gte`', 'μεγαλύτερες ή ίσες', '`>=`'],
          ['`$lt`', 'μικρότερες', '`<`'],
          ['`$lte`', 'μικρότερες ή ίσες', '`<=`'],
          ['`$in`', 'ίσες με μία από τις τιμές μιας λίστας', '`IN`'],
          ['`$nin`', 'διαφορετικές από όλες τις τιμές μιας λίστας', '`NOT IN`']],
    foot='Σύνταξη: `{ πεδίο: { $τελεστής: τιμή } }`. Εργασία 2, ενότητα 6.',
    src='MongoDB Manual: Comparison Query Predicate Operators· SQL to MongoDB Mapping Chart.',
    notes=['Ο πίνακας του παλαιότερου υλικού, στα ελληνικά, με την αντίστοιχη SQL.',
           'Τα $ne και $nin επιλέγουν και έγγραφα που δεν έχουν καν το πεδίο.',
           '$in στην πράξη: %s επιστρέφει %s.' % (cmd('in'), N['in'])])

add(type='shell', mins=1, title='Σύγκριση στην πράξη: `$gt`', dense=True,
    cmd=cmd('gt'), out=out('gt'),
    points=['Βιβλία με περισσότερες από 1.000 σελίδες: τρία.',
            'Στη θέση της τιμής μπαίνει ένα έγγραφο με τον τελεστή.',
            'SQL: `pageCount > 1000` στο WHERE.'],
    notes=['Όπως στο παλαιότερο υλικό: find({ population: { $gt: 70000000 } }).',
           'Η σειρά της εξόδου είναι η σειρά αποθήκευσης· την ταξινόμηση την ορίζει το sort, στη διαφάνεια [[s_sort]].'])

add(type='work', mins=3, timerSec=180, title='Άσκηση 1',
    context='Στο mongosh, στη βάση library:',
    items=['Εμφανίστε τα βιβλία της κατηγορίας Internet με 400 έως 500 σελίδες, χωρίς το πεδίο longDescription.',
           'Μετρήστε τα με `countDocuments` και το ίδιο φίλτρο.'],
    notes=['Η Άσκηση 1 του παλαιότερου υλικού, όπως ήταν. Ξεκινήστε το χρονόμετρο (πλήκτρο T).',
           'Όσοι δεν έχουν ακόμη τη συλλογή παρακολουθούν τη λύση στην επόμενη διαφάνεια.'])

add(type='shell', mins=1, title='Άσκηση 1: η λύση', dense=True,
    cmd=cmd('ex1'), cmdLabel='Η λύση και ο έλεγχος', out=out('ex1', [1]), outLabel='Αποτέλεσμα του countDocuments',
    points=['`categories: "Internet"`: αρκεί η κατηγορία να υπάρχει στη λίστα.',
            '`$gte` και `$lte` μέσα στο ίδιο έγγραφο: δύο όρια για το ίδιο πεδίο.',
            'Το «WebWork in Action» (400 σελίδες) έχει κατηγορία «internet», με πεζά, και λείπει. Με `$in: ["Internet", "internet"]` βρίσκονται %s.' % EX1FIX],
    notes=['Η λύση του παλαιότερου υλικού είναι σωστή και μένει ως έχει.',
           'Η έξοδος του find δεν χωρά εδώ, γιατί κάθε βιβλίο έχει και shortDescription· το countDocuments επιβεβαιώνει ότι είναι %s.' % EX1])

add(type='htable', mins=1, title='Λογικοί τελεστές', compact=True,
    head=['Τελεστής', 'Επιλέγει έγγραφα που', 'SQL'],
    rows=[['`$and`', 'ικανοποιούν όλες τις συνθήκες', '`AND`'],
          ['`$or`', 'ικανοποιούν τουλάχιστον μία συνθήκη', '`OR`'],
          ['`$nor`', 'δεν ικανοποιούν καμία συνθήκη', '`NOT (… OR …)`'],
          ['`$not`', 'δεν ικανοποιούν τη συνθήκη ενός τελεστή', '`NOT`']],
    foot='Το κόμμα ανάμεσα σε συνθήκες είναι ήδη AND, όπως στη διαφάνεια [[s_counts]]. Εργασία 2, ενότητα 5.',
    src='MongoDB Manual: Logical Query Predicate Operators.',
    notes=['Ο πίνακας του παλαιότερου υλικού, στα ελληνικά, με την αντίστοιχη SQL.',
           'Τα $and, $or και $nor παίρνουν λίστα συνθηκών: { $or: [ {…}, {…} ] }. Το $not μπαίνει μέσα σε ένα πεδίο και επιλέγει και έγγραφα χωρίς το πεδίο: %s επιστρέφει %s, μαζί με τα βιβλία των 0 σελίδων.' % (cmd('not'), N['not'])])

add(type='shell', mins=1, title='`$or`: τουλάχιστον μία συνθήκη', dense=True,
    cmd=cmd('or'), out=out('or'),
    points=['Βιβλία της κατηγορίας Python, ή βιβλία με περισσότερες από 1.000 σελίδες: 6 και 3.',
            'Λογικός τελεστής και τελεστής σύγκρισης στο ίδιο ερώτημα: σύνθετο ερώτημα.',
            'Εργασία 2, ενότητα 8: τουλάχιστον δύο τέτοια ερωτήματα.'],
    notes=['Κάθε στοιχείο της λίστας του $or είναι ένα πλήρες φίλτρο.',
           'Κανένα βιβλίο Python δεν ξεπερνά τις 1.000 σελίδες, γι’ αυτό 6 + 3 = 9.'])

add(type='shell', mins=1, kicker='Προσοχή', title='Το ίδιο πεδίο δύο φορές',
    cmd=cmd('samefield'), cmdLabel='Εντολές', out=out('samefield'), outLabel='Αποτελέσματα',
    points=['Στο πρώτο, το δεύτερο `pageCount` αντικαθιστά σιωπηλά το πρώτο: μένει μόνο το `$lt: 400`, και μετρώνται και τα %s βιβλία με 0 σελίδες.' % ZERO,
            'Σωστά: οι δύο τελεστές στο ίδιο έγγραφο, ή ρητό `$and`.'],
    src='MongoDB Manual: $and.',
    notes=['Το παλαιότερο υλικό είχε το ίδιο θέμα από το εγχειρίδιο («AND Queries With Multiple Expressions Specifying the Same Field»).',
           'Δεν εμφανίζεται κανένα σφάλμα: η JavaScript κρατά την τελευταία τιμή ενός διπλού κλειδιού πριν καν σταλεί το ερώτημα στον διακομιστή. Το %s δίνει επίσης %s.' % (cmd('lt400'), N['lt400'])])

add(type='shell', mins=1, title='Πεδία-λίστες: αρκεί ένα στοιχείο', dense=True,
    cmd=cmd('perl'), out=out('perl'),
    points=['`{ categories: "Perl" }` ταιριάζει όταν η λίστα περιέχει το «Perl», σε οποιαδήποτε θέση.',
            'Δύο από τα έξι βιβλία έχουν και δεύτερη κατηγορία.'],
    src='MongoDB Manual: Query an Array.',
    notes=['Έτσι λειτούργησε και η Άσκηση 1 με την κατηγορία Internet.',
           'Το ίδιο ισχύει για τους τελεστές: το { categories: { $in: [ … ] } } ελέγχει κάθε στοιχείο της λίστας.'])

add(type='poll', mins=2, timerSec=60, kicker='Ερώτημα', title='Πόσα βιβλία επιστρέφει;',
    context='Το πρώτο φίλτρο βρίσκει %s βιβλία. Πόσα βρίσκει το δεύτερο;' % EXACT_ALL,
    code='{ categories: "Internet" }\n{ categories: ["Internet"] }',
    options=['%s, τον ίδιο αριθμό' % EXACT_ALL, 'Λιγότερα από %s' % EXACT_ALL, 'Περισσότερα από %s' % EXACT_ALL, 'Σφάλμα σύνταξης'],
    notes=['Δημοσκόπηση Zoom, μία επιλογή. Ξεκινήστε το χρονόμετρο (πλήκτρο T).',
           'Η απάντηση είναι στην επόμενη διαφάνεια.'])

add(type='shell', mins=1, title='Η απάντηση: λιγότερα, %s' % EXACT_ONLY, dense=True,
    cmd=cmd('exact') + '\n' + cmd('all'), cmdLabel='Εντολές', out=out('exact') + '\n' + out('all'), outLabel='Αποτελέσματα',
    points=['Με αγκύλες, το φίλτρο ζητά ακριβώς την ίδια λίστα, με την ίδια σειρά: μόνο «Internet».',
            '%d από τα %s βιβλία έχουν και άλλη κατηγορία.' % (int(EXACT_ALL) - int(EXACT_ONLY), EXACT_ALL),
            '`$all` (τρίτη εντολή): και οι δύο κατηγορίες, σε οποιαδήποτε θέση· %s βιβλία.' % N['all']],
    src='MongoDB Manual: Query an Array.',
    notes=['Επιβεβαιώνει τη διαφάνεια [[s_perl]]: χωρίς αγκύλες, αρκεί ένα στοιχείο.',
           'Η ακριβής σύγκριση λίστας σπάνια χρειάζεται· όταν γράφεται κατά λάθος, το ερώτημα επιστρέφει κάτι και το λάθος περνά απαρατήρητο.'])

add(type='shell', mins=1, title='Σημειογραφία τελείας σε λίστα',
    cmd=cmd('dot'), out=out('dot'),
    points=['`"authors.0"`: ο πρώτος συγγραφέας. Η αρίθμηση ξεκινά από το 0.',
            'Η τελεία της Βραδιάς 1 (`"capital.name"`) λειτουργεί και με θέσεις λίστας. Το όνομα γράφεται σε εισαγωγικά.'],
    src='MongoDB Manual: Query an Array.',
    notes=['Το %s δίνει %s: βρίσκει και το βιβλίο όπου ο Christian Bauer δεν είναι πρώτος συγγραφέας.' % (cmd('dotall'), N['dotall']),
           'Εγχειρίδιο, Query an Array: «Query for an Element by the Array Index Position».'])

add(type='shell', mins=1, title='Κανονικές εκφράσεις (regex)',
    cmd=cmd('regex'), cmdLabel='Εντολές', out=out('regex'), outLabel='Αποτελέσματα',
    points=['`/Python/`: ο τίτλος περιέχει «Python» σε οποιοδήποτε σημείο, όπως το `LIKE` της SQL.',
            'Πεζά και κεφαλαία διαφέρουν: το `/python/` δεν βρίσκει τίποτε· με `i` τα βρίσκει όλα.',
            'Η τέταρτη εντολή, με `$regex`, δίνει το ίδιο. Εργασία 2, ενότητα 7.'],
    src='MongoDB Manual: $regex· SQL to MongoDB Mapping Chart.',
    notes=['Επτά τίτλοι περιέχουν «Python», ενώ η κατηγορία Python έχει έξι βιβλία: δύο τίτλοι (Geoprocessing with Python, IronPython in Action) δεν έχουν καμία κατηγορία, και το «Hello World!» είναι βιβλίο Python χωρίς τη λέξη στον τίτλο.',
           'Το παλαιότερο υλικό παρέπεμπε στη σελίδα $regex του εγχειριδίου· οι ασκήσεις του με τη λέξη Java γίνονται στο Μέρος 2.'])

add(type='shell', mins=1, title='Τα σύμβολα `^`, `$` και `.`',
    cmd=cmd('symbols'), cmdLabel='Εντολές', out=out('symbols'), outLabel='Αποτελέσματα',
    points=['`^`: στην αρχή. `/^The /`: τίτλοι που αρχίζουν από «The ».',
            '`$`: στο τέλος. `/Edition$/`: τίτλοι που τελειώνουν σε «Edition».',
            '`.`: ένας οποιοσδήποτε χαρακτήρας. `/^.#/`: C# και F#.'],
    src='MongoDB Manual: $regex.',
    notes=['Χωρίς ^ και $, η έκφραση ταιριάζει σε οποιοδήποτε σημείο του κειμένου.',
           'Όταν ζητάμε αυτούσιο ένα σύμβολο με ειδική σημασία, γράφουμε \\ μπροστά του: %s βρίσκει %s τίτλους με «.NET».' % (cmd('escape'), N['escape'])])

add(type='shell', mins=1, title='`$elemMatch`: όλες οι συνθήκες στο ίδιο στοιχείο',
    cmd=cmd('elem'), cmdLabel='Εντολές', out=out('elem'), outLabel='Αποτελέσματα',
    points=['%s βιβλία έχουν συγγραφέα που το όνομά του αρχίζει από «Chris».' % CHRIS,
            'Με `$elemMatch`, ο ίδιος συγγραφέας ικανοποιεί και τις δύο συνθήκες: αρχίζει από «Chris» και δεν είναι ο Christian Bauer. Μένουν %s.' % CHRIS_NOT_CB,
            'Οι συνθήκες του `$elemMatch` γράφονται σε ένα έγγραφο, όπως στο φίλτρο του find.'],
    src='MongoDB Manual: Query an Array· $elemMatch.',
    notes=['Το παράδειγμα ακολουθεί το εγχειρίδιο της MongoDB, που συνδυάζει στο ίδιο στοιχείο $regex και $ne.',
           'Ετοιμάζει την Άσκηση 2, που ζητά το ίδιο εργαλείο για άλλο όνομα.'])

add(type='work', mins=3, timerSec=180, title='Άσκηση 2',
    context='Στο mongosh, στη συλλογή books:',
    items=['Βρείτε τα βιβλία όπου τουλάχιστον ένας από τους συγγραφείς έχει το όνομα «Peter».',
           'Υπόδειξη: `$elemMatch` και `$regex`.',
           'Μετρήστε τα με `countDocuments`.'],
    notes=['Η Άσκηση 2 του παλαιότερου υλικού. Η εκφώνησή του έγραφε «Piter», ενώ η λύση του έψαχνε «Peter»: με «Piter» δεν βρίσκεται κανένα βιβλίο.',
           'Ξεκινήστε το χρονόμετρο (πλήκτρο T).'])

add(type='shell', mins=1, title='Άσκηση 2: η λύση',
    cmd=cmd('ex2'), cmdLabel='Εντολές', out=out('ex2'), outLabel='Αποτελέσματα',
    points=['Τα βιβλία εμφανίζονται με `find` και το ίδιο φίλτρο: %s.' % PETER,
            'Με μία μόνο συνθήκη, το `$elemMatch` δεν χρειάζεται: η δεύτερη εντολή δίνει τα ίδια %s.' % PETER_SIMPLE,
            '`$options: "i"`: χωρίς διάκριση πεζών και κεφαλαίων.'],
    src='MongoDB Manual: $elemMatch (Single Query Condition).',
    notes=['Η λύση του παλαιότερου υλικού, όπως ήταν: db.books.find({ authors: { $elemMatch: { $regex: "^Peter", $options: "i" } } }).',
           'Με «Piter», όπως έγραφε η παλαιά εκφώνηση, το countDocuments δίνει %s.' % N['piter'],
           'Το ^Peter θα έβρισκε και ονόματα όπως «Peterson»· εδώ και τα %s είναι «Peter …».' % PETER])

add(type='shell', mins=1, title='Ταξινόμηση και περιορισμός: sort, limit', dense=True,
    cmd=cmd('sort'), out=out('sort'),
    points=['`sort`: 1 για αύξουσα, -1 για φθίνουσα σειρά. Εδώ: τα πιο πρόσφατα πρώτα.',
            '`limit(3)`: μόνο τα τρία πρώτα. Με `limit(1)`: το πιο πρόσφατο βιβλίο.',
            'Εργασία 2, ενότητα 9: και αύξουσα και φθίνουσα.'],
    src='MongoDB Manual: cursor.sort()· cursor.limit().',
    notes=['Όπως στο παλαιότερο υλικό: find().sort({ population: -1 }).limit(1), «η χώρα με τον μεγαλύτερο πληθυσμό».',
           'Στην SQL: ORDER BY publishedDate DESC LIMIT 3.'])

add(type='shell', mins=1, skippable=True, title='skip: η επόμενη σελίδα', dense=True,
    cmd=cmd('skip'), out=out('skip'),
    points=['`skip(3)`: παραλείπει τα τρία πρώτα· η δεύτερη σελίδα της προηγούμενης λίστας.',
            'Η σειρά γραφής δεν μετρά: πρώτα ταξινόμηση, μετά παράλειψη, μετά όριο.'],
    src='MongoDB Manual: cursor.skip().',
    notes=['Το εγχειρίδιο: η σειρά των skip() και limit() στην αλυσίδα δεν επηρεάζει το αποτέλεσμα.',
           'Για σταθερές σελίδες, η ταξινόμηση πρέπει να περιλαμβάνει πεδίο με μοναδικές τιμές, π.χ. sort({ publishedDate: -1, _id: 1 }).'])

add(type='shell', mins=1, kicker='Προσοχή', title='Τα μηδενικά πρώτα',
    cmd=cmd('zeros'), out=out('zeros'),
    points=['Τα «μικρότερα» βιβλία έχουν 0 σελίδες: είναι τα %s με άγνωστο αριθμό.' % ZERO,
            'Με `$gt: 0` στο pageCount, τα τρία πρώτα έχουν %s σελίδες.' % PAGES3],
    src='MongoDB Manual: Comparison/Sort Order.',
    notes=['Ανάμεσα σε ίσες τιμές η σειρά δεν είναι εγγυημένη: τα τρία βιβλία με 0 σελίδες μπορεί να διαφέρουν σε άλλη εκτέλεση. Όπου το πεδίο λείπει, η MongoDB το ταξινομεί σαν null, πριν από κάθε αριθμό.',
           'Ο ίδιος έλεγχος χρειάζεται στην Εργασία 2: πριν από την ταξινόμηση, κοιτάξτε αν υπάρχουν μηδενικά ή κενά.'])

add(type='remember', mins=1, kicker='Να θυμάστε', title='Τρία σημεία από το Μέρος 1',
    items=['Το find παίρνει δύο έγγραφα: το φίλτρο επιλέγει έγγραφα, η προβολή επιλέγει πεδία.',
           'Σε πεδίο-λίστα αρκεί να ταιριάζει ένα στοιχείο· η λίστα σε αγκύλες ζητά ακριβώς την ίδια λίστα.',
           'Πριν από τα ερωτήματα, κοιτάξτε τα δεδομένα: 0 σελίδες σημαίνει «άγνωστο», και τα πεζά διαφέρουν από τα κεφαλαία.'],
    notes=['Διαβάστε τα τρία σημεία. Τίποτε άλλο.',
           'Αν απομένει χρόνος, δεν προστίθεται ύλη· το διάλειμμα ξεκινά νωρίτερα.'])

add(type='break', mins=3, title='Διάλειμμα',
    next='Στο Μέρος 2: ομαδική άσκηση στη συλλογή books, σε αίθουσες του Zoom. Όποιος δεν ολοκλήρωσε την εισαγωγή, την ολοκληρώνει τώρα.',
    notes=['Σταματήστε ακριβώς στην ώρα. Αν χρειαστεί χρόνος, παραλείπονται οι διαφάνειες [[skips]].',
           'Αφήστε τη διαφάνεια στην οθόνη σε όλο το διάλειμμα: η αντίστροφη μέτρηση δείχνει πότε ξεκινάμε.',
           'Το Μέρος 2 χρειάζεται τη συλλογή books στον υπολογιστή κάθε φοιτητή.'])

# slide numbers quoted in notes and feet
def num(pred):
    hits = [i + 1 for i, s in enumerate(S) if pred(s)]
    assert len(hits) == 1, hits
    return hits[0]
REF = {'s_install': num(lambda s: s['title'] == 'Εγκατάσταση και εισαγωγή τώρα'),
       's_errors': num(lambda s: s['title'] == 'Τρία συνηθισμένα λάθη'),
       's_ex1sol': num(lambda s: s['title'] == 'Άσκηση 1: η λύση'),
       's_zeros': num(lambda s: s['title'] == 'Τα μηδενικά πρώτα'),
       's_sort': num(lambda s: s['title'].startswith('Ταξινόμηση και περιορισμός')),
       's_counts': num(lambda s: s['title'].startswith('Πριν από τα ερωτήματα')),
       's_perl': num(lambda s: s['title'].startswith('Πεδία-λίστες')),
       'skips': ' και '.join(str(i + 1) for i, s in enumerate(S) if s.get('skippable'))}
def fill(x):
    for k, v in REF.items():
        x = x.replace('[[%s]]' % k, str(v))
    return x
for s in S:
    s['notes'] = [fill(n) for n in s['notes']]
    if 'foot' in s:
        s['foot'] = fill(s['foot'])

sk = [i + 1 for i, s in enumerate(S) if s.get('skippable')]
tot = sum(s['mins'] for s in S)
polls = [i + 1 for i, s in enumerate(S) if s['type'] == 'poll']
assert tot == 45, tot
assert len(sk) == 2, sk
assert len(polls) == 1 and S[polls[0] - 1]['timerSec'] == 60
assert 30 <= len(S) <= 35, len(S)
for s in S:
    t = json.dumps(s, ensure_ascii=False)
    assert '[[s_' not in t and '[[skips]]' not in t, s['title']
D = {'meta': {'course': 'Βάσεις Δεδομένων & Ανάλυση Δεδομένων Μάθησης', 'deckTitle': 'Ερωτήματα στη συλλογή books',
              'part': 'Μη σχεσιακές βάσεις, Βραδιά 2, Μέρος 1', 'start': '18:15', 'lengthMin': 45, 'breakMin': 15, 'lang': 'el',
              'notesMarkup': True},
     'slides': S}
json.dump(D, open(os.path.join(H, '..', 'content', 'n2p1.json'), 'w', encoding='utf8'), ensure_ascii=False, indent=1)
print('slides', len(S), 'minutes', tot, 'skippable', sk, 'poll', polls)
