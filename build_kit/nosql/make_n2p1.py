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
# numbers the speaker notes quote, read from the same run
titles = lambda key: O[key][0].count('title:')
PY = one('vars', 3)                                   # countDocuments({ categories: "Python" })
assert int(PY) == titles('proj1') == titles('proj2')
assert int(N['in']) == int(PY) + titles('perl')       # $in Python/Perl: no book has both
assert titles('or') == int(PY) + titles('gt') and max(int(x) for x in re.findall(r'pageCount: (\d+)', O['proj1'][0])) <= 1000
assert titles('pytitles') == 2 and int(REGEX[0]) == int(PY) - 1 + titles('pytitles') and 'Hello World!' in O['proj1'][0] and "categories: []" in O['pytitles'][0]
assert int(CHRIS) - int(CHRIS_NOT_CB) == int(N['dotall']) and int(N['dotall']) - titles('dot') == 1
assert "'Hibernate in Action (Chinese Edition)'" in O['dot'][0] and "authors: [ 'Christian Bauer'" in O['book23'][1]
AND_FILTER = CMDS['counts'][2].split('(', 1)[1][:-1]  # { status: "MEAP", pageCount: 0 }: the comma is AND
assert AND_FILTER == '{ status: "MEAP", pageCount: 0 }'
FULL_PATH = '"C:\\Program Files\\MongoDB\\Tools\\100\\bin\\mongoimport.exe"' + IMPORT[len('mongoimport'):]
_file = [json.loads(l)['title'] for l in open(os.path.join(H, '..', 'sources_nosql', 'books.json'), encoding='utf8') if l.strip()]
_gt = re.findall(r"title: '([^']*)'", O['gt'][0])
assert _gt == sorted(_gt, key=_file.index)          # slide 14 note: without sort the books came out in books.json order
assert int(ZERO) <= int(N['not'])        # 0 is not > 500: the zero-page books are among the $not count
assert 'Peter Armstrong' in O['ex2find'][0] and all(a.startswith('Peter ') for a in re.findall(r"'(Peter[^']*)'", O['ex2find'][0]))

add(type='title', mins=1, title='Μη σχεσιακές βάσεις δεδομένων', subtitle='Ερωτήματα, ενημέρωση και συνάθροιση στη MongoDB',
    author='Αθανάσιος Χριστόπουλος, Ph.D.',
    affil='Αν. Καθηγητής, Τμήμα Φυσικών Επιστημών. Κέντρο Μαθησιακής Αναλυτικής, Πανεπιστήμιο του Τούρκου, Φινλανδία',
    email='atchri@utu.fi',
    notes=['**Μη σχεσιακές βάσεις δεδομένων**: Ξεκινήστε ακριβώς στην ώρα, με μία πρόταση σύνδεσης: «Στη Βραδιά 1 εγκαταστήσατε τη MongoDB και γράψατε '
           'τα πρώτα σας έγγραφα· απόψε κάνουμε ερωτήματα σε μια συλλογή %s βιβλίων.»' % N['total'],
           '**Ερωτήματα, ενημέρωση και συνάθροιση στη MongoDB**: Αντιστοιχεί στις ενότητες 4 έως 11 της Εργασίας 2. Οι ενότητες 1 έως 3 και 12 καλύφθηκαν στη Βραδιά 1.'])

add(type='plan', mins=1, title='Το πλάνο της βραδιάς',
    rows=[{'label': 'Μέρος 1', 'text': 'Ερωτήματα στη συλλογή books', 'now': True},
          {'label': 'Μέρος 2', 'text': 'Ομαδική άσκηση σε αίθουσες του Zoom'},
          {'label': 'Μέρος 3', 'text': 'Ενημέρωση, συνάθροιση, SQL και MongoDB'}],
    notes=['**Ερωτήματα στη συλλογή books**: Μία φράση ανά μέρος, όχι περισσότερο. Το Μέρος 1 ξεκινά με δύο λήψεις, στην επόμενη διαφάνεια.',
           '**Ομαδική άσκηση σε αίθουσες του Zoom**: Ο καθένας δουλεύει στο δικό του mongosh, με τη συλλογή books που εισάγουμε στο Μέρος 1.',
           '**Ενημέρωση, συνάθροιση, SQL και MongoDB**: Στο τέλος του Μέρους 3, η Εργασία 2 ενότητα προς ενότητα και τι παραδίδετε.'])

add(type='table', mins=1, title='Δύο λήψεις, τώρα', compact=True,
    rows=[{'h': 'MongoDB Database Tools', 't': '[mongodb.com/try/download/database-tools](https://www.mongodb.com/try/download/database-tools): Windows x86_64, πακέτο msi.'},
          {'h': 'books.json', 't': '[Λήψη του books.json](https://raw.githubusercontent.com/ozlerhakan/mongodb-json-files/master/datasets/books.json): στη σελίδα που ανοίγει, Ctrl+S και αποθήκευση ως books.json.'},
          {'h': 'macOS ή Linux', 't': '[Οδηγίες εγκατάστασης ανά σύστημα](https://www.mongodb.com/docs/database-tools/installation/).'}],
    foot='Ξεκινήστε τώρα και τις δύο λήψεις.',
    src='books.json: αποθετήριο ozlerhakan/mongodb-json-files, άδεια CC0.',
    notes=['**mongodb.com/try/download/database-tools**: Στείλτε τους τρεις συνδέσμους και στο chat του Zoom (δεξί κλικ, αντιγραφή)· στην οθόνη σας οι φοιτητές '
           'δεν μπορούν να τους πατήσουν. Στη σελίδα επιλέγουν Windows x86_64 και πακέτο msi.',
           '**Λήψη του books.json**: Το αρχείο αποθηκεύεται με το όνομα books.json, γιατί με αυτό το όνομα το ζητά η εντολή της διαφάνειας [[s_install]].',
           '**Οδηγίες εγκατάστασης ανά σύστημα**: Για όσους έχουν macOS ή Linux· τα βήματα της διαφάνειας [[s_install]] είναι για Windows.',
           'Αν ρωτήσουν: κι αν η λήψη από το GitHub δεν γίνεται; Το books.json είναι και στο υλικό της βραδιάς για την πλατφόρμα του μαθήματος.'])

add(type='work', mins=6, timerSec=360, title='Εγκατάσταση και εισαγωγή τώρα',
    context='Στα Windows:',
    items=['Εκτελέστε το msi των Database Tools, με τις προεπιλογές.',
           {'t': 'Ρυθμίσεις συστήματος για προχωρημένους → Μεταβλητές περιβάλλοντος → Path → Επεξεργασία. Νέα γραμμή:', 'code': 'C:\\Program Files\\MongoDB\\Tools\\100\\bin'},
           {'t': 'Νέο τερματικό, στον φάκελο του books.json:', 'code': IMPORT},
           'Στο chat: «ΟΚ», ή το μήνυμα λάθους.'],
    foot='Όποιος δεν τελειώσει, συνεχίζει παράλληλα με το μάθημα.',
    src='MongoDB Database Tools: Installation, Windows (msi, PATH).',
    # timer note first on purpose: students start step 1 while steps 2-3 are explained (check_notes order warning = timer in the right column)
    notes=['**06:00**: Ξεκινήστε το χρονόμετρο με το πλήκτρο T. Όσο τρέχει, απαντάτε στα μηνύματα του chat· τα συνηθισμένα λάθη και η λύση τους '
           'είναι στη διαφάνεια [[s_errors]].',
           '**`C:\\Program Files\\MongoDB\\Tools\\100\\bin`**: Εδώ εγκαθιστά τα εργαλεία το msi με τις προεπιλογές του βήματος 1. '
           'Η γραμμή μπαίνει στο Path, για να βρίσκει το τερματικό το mongoimport.',
           '**Νέο τερματικό, στον φάκελο του books.json**: Νέο, γιατί ένα τερματικό που ήταν ήδη ανοιχτό δεν βλέπει το νέο Path. '
           'Στον φάκελο μπαίνουμε με `cd`, για παράδειγμα `cd Downloads`.',
           'Αν ρωτήσουν: και χωρίς αλλαγή στο Path; Δουλεύει η πλήρης διαδρομή: `%s`.' % FULL_PATH])

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
    notes=['**Μέσα στο mongosh**: Όποιος γράψει την εντολή μετά την προτροπή `test>` παίρνει αυτό το σφάλμα. Βγαίνει από το mongosh με `exit` '
           'και τη γράφει στο τερματικό.',
           '**Δεύτερη εισαγωγή**: Στο τέλος το τερματικό γράφει `%s` Δεν χρειάζεται διόρθωση: η συλλογή έχει ήδη τα %s βιβλία.' % (AGAIN_LAST, N['total']),
           '**«Δεν αναγνωρίζεται»**: Το ακριβές μήνυμα διαφέρει ανάλογα με το τερματικό (Γραμμή εντολών ή PowerShell) και τη γλώσσα των Windows. '
           'Αν ούτε νέο τερματικό βοηθά, ελέγξτε τη γραμμή του Path στη διαφάνεια [[s_install]].',
           'Αν ρωτήσουν: τι σημαίνει «error connecting to host»; Ο διακομιστής δεν τρέχει: Υπηρεσίες των Windows, MongoDB Server, Έναρξη, όπως στη Βραδιά 1.'])

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
    notes=['**`{ categories: "Python" }`**: Το πρώτο όρισμα είναι το φίλτρο: τα %s βιβλία της κατηγορίας Python.' % PY,
           '**`{ title: 1, pageCount: 1 }`**: Το δεύτερο όρισμα, η προβολή: από κάθε βιβλίο μόνο ο τίτλος και οι σελίδες. '
           'Στην SQL είναι η λίστα στηλών μετά το SELECT.',
           '**Το `_id` εμφανίζεται πάντα**: Φαίνεται σε κάθε βιβλίο του αποτελέσματος, αν και η προβολή δεν το ζητά.',
           '**Εργασία 2, ενότητα 4**: «Απλά ερωτήματα προβολής συγκεκριμένων πεδίων»: αυτό είναι ένα τέτοιο ερώτημα.'])

add(type='shell', mins=1, title='Χωρίς `_id`, και εξαίρεση πεδίων', dense=True,
    cmd=cmd('proj2'), out=out('proj2'),
    points=['`_id: 0`: το μόνο πεδίο που αποκλείεται μέσα σε προβολή με 1.',
            'Εξαίρεση: `{ longDescription: 0 }` δείχνει όλα τα πεδία εκτός από αυτό.',
            '1 και 0 μαζί δεν επιτρέπονται: «%s».' % PROJ_ERR_MSG],
    src='MongoDB Manual: Project Fields to Return from Query.',
    notes=['**`_id: 0`**: Το ίδιο ερώτημα με την προηγούμενη διαφάνεια, χωρίς το `_id`. Είναι το μόνο πεδίο που δέχεται 0 δίπλα σε πεδία με 1.',
           '**`{ longDescription: 0 }`**: Προβολή μόνο με 0: εμφανίζονται όλα τα πεδία του βιβλίου εκτός από την περιγραφή longDescription.',
           '**1 και 0 μαζί δεν επιτρέπονται**: Το μήνυμα το δίνει η εντολή `%s`. Στα ελληνικά: δεν γίνεται εξαίρεση πεδίου σε προβολή που επιλέγει πεδία.' % cmd('projerr')])

add(type='shell', mins=1, title='Ευανάγνωστο JSON: printjson', dense=True,
    cmd=cmd('printjson'), out=out('printjson'),
    points=['`forEach(printjson)`: τυπώνει κάθε έγγραφο χωριστά, ένα πεδίο ανά γραμμή.',
            'Η Εργασία 2 το ζητά σε κάποια ερωτήματα: σημειώστε στην αναφορά πού το χρησιμοποιήσατε.',
            'Το `forEach(printjson)` μπαίνει στο τέλος, μετά το `sort` ή το `limit`.'],
    src='mongosh: Native Methods (print, printjson).',
    notes=['**`.forEach(printjson)`**: Το αποτέλεσμα δεν είναι πια μία λίστα σε αγκύλες: κάθε έγγραφο τυπώνεται χωριστά, με ένα πεδίο ανά γραμμή.',
           '**Η Εργασία 2 το ζητά σε κάποια ερωτήματα**: Το printjson αντιστοιχεί στη φράση της εκφώνησης «προβολή σε ευανάγνωστη μορφή JSON» και αρκεί γι’ αυτήν.',
           '**μπαίνει στο τέλος, μετά το `sort` ή το `limit`**: Πρώτα το ερώτημα με ταξινόμηση και όριο, στο τέλος η εκτύπωση. '
           'Τα sort και limit έρχονται στη διαφάνεια [[s_sort]].',
           'Αν ρωτήσουν: και το `.pretty()` των παλαιών οδηγών; Λειτουργεί ακόμη· η έξοδος του mongosh όμως είναι ήδη μορφοποιημένη.'])

add(type='shell', mins=1, title='Μεταβλητές',
    cmd=cmd('vars'), out=out('vars'), outLabel='Αποτελέσματα των δύο τελευταίων εντολών',
    points=['Η μεταβλητή κρατά ένα φίλτρο, μια προβολή ή ένα αποτέλεσμα, και ξαναχρησιμοποιείται.',
            'Ισχύει μόνο όσο είναι ανοιχτό το mongosh.',
            'Η Εργασία 2 ζητά μεταβλητές σε κάποια ερωτήματα: σημειώστε το στην αναφορά.'],
    notes=['**`var python = { categories: "Python" }`**: Η μεταβλητή python κρατά το φίλτρο και η fields την προβολή. '
           'Οι δηλώσεις δεν τυπώνουν τίποτε· γι’ αυτό φαίνονται μόνο τα αποτελέσματα των δύο τελευταίων εντολών.',
           '**`db.books.countDocuments(python)`**: Το ίδιο φίλτρο ξαναχρησιμοποιείται χωρίς να ξαναγραφτεί: %s βιβλία, όσοι και οι τίτλοι του find.' % PY,
           '**Ισχύει μόνο όσο είναι ανοιχτό το mongosh**: Σε νέο παράθυρο του mongosh, οι δηλώσεις var γράφονται ξανά πριν από τα ερωτήματα.',
           '**Η Εργασία 2 ζητά μεταβλητές σε κάποια ερωτήματα**: Είναι στην ίδια πρόταση της εκφώνησης με το ευανάγνωστο JSON της προηγούμενης διαφάνειας. '
           'Και τα δύο τα επισημαίνετε με σχετικό κείμενο στην αναφορά.'])

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
    notes=['**`$ne`**: Επιλέγει και τα έγγραφα που δεν έχουν καθόλου το πεδίο. Το ίδιο κάνει και το `$nin`.',
           '**`$in`**: Για παράδειγμα, το `%s` δίνει %s: τα βιβλία Python και τα βιβλία Perl μαζί.' % (cmd('in'), N['in']),
           '**`{ πεδίο: { $τελεστής: τιμή } }`**: Ο τελεστής και η τιμή του γράφονται μαζί σε ένα έγγραφο, εκεί όπου αλλιώς θα έμπαινε μόνο η τιμή. '
           'Εργασία 2, ενότητα 6: «Ερωτήματα προβολής δεδομένων με τελεστές σύγκρισης».'])

add(type='shell', mins=1, title='Σύγκριση στην πράξη: `$gt`', dense=True,
    cmd=cmd('gt'), out=out('gt'),
    points=['Βιβλία με περισσότερες από 1.000 σελίδες: τρία.',
            'Στη θέση της τιμής μπαίνει ένα έγγραφο με τον τελεστή.',
            'SQL: `pageCount > 1000` στο WHERE.'],
    notes=['**`{ $gt: 1000 }`**: «Μεγαλύτερο από 1.000»: ένα βιβλίο με ακριβώς 1.000 σελίδες δεν μετρά. Για «1.000 και πάνω» γράφουμε `$gte`.',
           '**`pageCount: 1101`**: Το αποτέλεσμα δεν είναι ταξινομημένο κατά σελίδες: χωρίς sort, η σειρά δεν είναι εγγυημένη· '
           'εδώ τα βιβλία βγήκαν με τη σειρά του books.json. '
           'Την ταξινόμηση την ορίζει το sort, στη διαφάνεια [[s_sort]].',
           '**SQL: `pageCount > 1000` στο WHERE**: Η προβολή `{ title: 1, pageCount: 1, _id: 0 }` αντιστοιχεί στο `SELECT title, pageCount`.'])

add(type='work', mins=3, timerSec=180, title='Άσκηση 1',
    context='Στο mongosh, στη βάση library:',
    items=['Εμφανίστε τα βιβλία της κατηγορίας Internet με 400 έως 500 σελίδες, χωρίς το πεδίο longDescription.',
           'Μετρήστε τα με `countDocuments` και το ίδιο φίλτρο.'],
    notes=['**Στο mongosh, στη βάση library**: Όσοι δεν έχουν ακόμη τη συλλογή, παρακολουθούν τη λύση στην επόμενη διαφάνεια.',
           '**Μετρήστε τα με `countDocuments` και το ίδιο φίλτρο**: Ο αριθμός ελέγχει το find: πρέπει να είναι όσα και τα βιβλία που εμφανίστηκαν.',
           '**03:00**: Ξεκινήστε το χρονόμετρο με το πλήκτρο T.',
           'Αν ρωτήσουν: μετρούν και τα βιβλία με 400 και με 500 σελίδες; Ναι, και τα δύο όρια περιλαμβάνονται.'])

add(type='shell', mins=1, title='Άσκηση 1: η λύση', dense=True,
    cmd=cmd('ex1'), cmdLabel='Η λύση και ο έλεγχος', out=out('ex1', [1]), outLabel='Αποτέλεσμα του countDocuments',
    points=['`categories: "Internet"`: αρκεί η κατηγορία να υπάρχει στη λίστα.',
            '`$gte` και `$lte` μέσα στο ίδιο έγγραφο: δύο όρια για το ίδιο πεδίο.',
            'Το «WebWork in Action» (400 σελίδες) έχει κατηγορία «internet», με πεζά, και λείπει. Με `$in: ["Internet", "internet"]` βρίσκονται %s.' % EX1FIX],
    notes=['**`categories: "Internet"`**: Το categories είναι λίστα· το φίλτρο ταιριάζει όταν ένα από τα στοιχεία της είναι «Internet».',
           '**Αποτέλεσμα του countDocuments**: Το find τυπώνει τα βιβλία με όλα τα άλλα πεδία τους, που δεν χωρούν εδώ· το countDocuments δίνει το πλήθος τους, %s.' % EX1,
           '**`$gte` και `$lte` μέσα στο ίδιο έγγραφο**: Περιλαμβάνονται και τα δύο όρια, όπως ζητά το «400 έως 500».',
           '**«WebWork in Action»**: Το «internet» με πεζά είναι άλλη τιμή, όπως στη διαφάνεια [[s_counts]]. '
           'Με το `$in` και των δύο γραφών, το πλήθος γίνεται %s.' % EX1FIX])

add(type='htable', mins=1, title='Λογικοί τελεστές', compact=True,
    head=['Τελεστής', 'Επιλέγει έγγραφα που', 'SQL'],
    rows=[['`$and`', 'ικανοποιούν όλες τις συνθήκες', '`AND`'],
          ['`$or`', 'ικανοποιούν τουλάχιστον μία συνθήκη', '`OR`'],
          ['`$nor`', 'δεν ικανοποιούν καμία συνθήκη', '`NOT (… OR …)`'],
          ['`$not`', 'δεν ικανοποιούν τη συνθήκη ενός τελεστή', '`NOT`']],
    foot='Το κόμμα ανάμεσα σε συνθήκες είναι ήδη AND, όπως στη διαφάνεια [[s_counts]]. Εργασία 2, ενότητα 5.',
    src='MongoDB Manual: Logical Query Predicate Operators.',
    notes=['**`$and`**: Τα `$and`, `$or` και `$nor` παίρνουν λίστα συνθηκών: `{ $or: [ {…}, {…} ] }`. Το `$or` στην πράξη είναι στην επόμενη διαφάνεια.',
           '**`$not`**: Μπαίνει μέσα σε ένα πεδίο και περιέχει άλλον τελεστή: το `%s` δίνει %s, μαζί με τα %s βιβλία των 0 σελίδων. '
           'Όπως τα `$ne` και `$nin`, επιλέγει και έγγραφα χωρίς το πεδίο.' % (cmd('not'), N['not'], ZERO),
           '**Το κόμμα ανάμεσα σε συνθήκες είναι ήδη AND**: Στη διαφάνεια [[s_counts]], το `%s` βρήκε τα %s βιβλία που ικανοποιούν και τις δύο συνθήκες.' % (AND_FILTER, MEAP0)])

add(type='shell', mins=1, title='`$or`: τουλάχιστον μία συνθήκη', dense=True,
    cmd=cmd('or'), out=out('or'),
    points=['Βιβλία της κατηγορίας Python, ή βιβλία με περισσότερες από 1.000 σελίδες: 6 και 3.',
            'Λογικός τελεστής και τελεστής σύγκρισης στο ίδιο ερώτημα: σύνθετο ερώτημα.',
            'Εργασία 2, ενότητα 8: τουλάχιστον δύο τέτοια ερωτήματα.'],
    notes=['**`$or`**: Κάθε στοιχείο της λίστας είναι ένα πλήρες φίλτρο: `{ categories: "Python" }` και `{ pageCount: { $gt: 1000 } }`.',
           '**%s και %s**: Κανένα βιβλίο Python δεν ξεπερνά τις 1.000 σελίδες, γι’ αυτό το αποτέλεσμα έχει %s + %s = %d τίτλους.'
           % (PY, titles('gt'), PY, titles('gt'), titles('or')),
           '**Εργασία 2, ενότητα 8**: «Τουλάχιστον δύο σύνθετα ερωτήματα με λογικούς τελεστές και τελεστές σύγκρισης ταυτόχρονα»· αυτό είναι ένα τέτοιο ερώτημα.'])

add(type='shell', mins=1, kicker='Προσοχή', title='Το ίδιο πεδίο δύο φορές',
    cmd=cmd('samefield'), cmdLabel='Εντολές', out=out('samefield'), outLabel='Αποτελέσματα',
    points=['Στο πρώτο, το δεύτερο `pageCount` αντικαθιστά σιωπηλά το πρώτο: μένει μόνο το `$lt: 400`, και μετρώνται και τα %s βιβλία με 0 σελίδες.' % ZERO,
            'Σωστά: οι δύο τελεστές στο ίδιο έγγραφο, ή ρητό `$and`.'],
    src='MongoDB Manual: $and.',
    notes=['**%s**: Το πλήθος της πρώτης εντολής, χωρίς κανένα σφάλμα. Η JavaScript κρατά την τελευταία τιμή ενός διπλού κλειδιού, '
           'πριν σταλεί το ερώτημα στον διακομιστή.' % SAME_WRONG,
           '**%s**: Η δεύτερη και η τρίτη εντολή δίνουν το ίδιο, σωστό πλήθος: βιβλία με περισσότερες από 300 και λιγότερες από 400 σελίδες.' % SAME_RIGHT,
           '**μένει μόνο το `$lt: 400`**: Το ίδιο %s δίνει και η εντολή `%s`.' % (N['lt400'], cmd('lt400')),
           '**Σωστά: οι δύο τελεστές στο ίδιο έγγραφο**: Έτσι γράφτηκε και η λύση της Άσκησης 1, με `$gte` και `$lte`, στη διαφάνεια [[s_ex1sol]].'])

add(type='shell', mins=1, title='Πεδία-λίστες: αρκεί ένα στοιχείο', dense=True,
    cmd=cmd('perl'), out=out('perl'),
    points=['`{ categories: "Perl" }` ταιριάζει όταν η λίστα περιέχει το «Perl», σε οποιαδήποτε θέση.',
            'Δύο από τα έξι βιβλία έχουν και δεύτερη κατηγορία.'],
    src='MongoDB Manual: Query an Array.',
    notes=['**`{ categories: "Perl" }`**: Γράφεται όπως για ένα απλό πεδίο κειμένου· σε πεδίο-λίστα ταιριάζει όταν ένα στοιχείο της είναι «Perl». '
           'Έτσι βρέθηκαν και τα βιβλία Internet της Άσκησης 1.',
           '**Δύο από τα έξι βιβλία έχουν και δεύτερη κατηγορία**: Στο «Graphics Programming with Perl» το «Perl» είναι δεύτερο στη λίστα, και το βιβλίο βρίσκεται κι αυτό.',
           'Αν ρωτήσουν: ισχύει και με τελεστές; Ναι: το `{ categories: { $in: ["Python", "Perl"] } }` ελέγχει κάθε στοιχείο της λίστας.'])

add(type='poll', mins=2, timerSec=60, kicker='Ερώτημα', title='Πόσα βιβλία επιστρέφει;',
    context='Το πρώτο φίλτρο βρίσκει %s βιβλία. Πόσα βρίσκει το δεύτερο;' % EXACT_ALL,
    code='{ categories: "Internet" }\n{ categories: ["Internet"] }',
    options=['%s, τον ίδιο αριθμό' % EXACT_ALL, 'Λιγότερα από %s' % EXACT_ALL, 'Περισσότερα από %s' % EXACT_ALL, 'Σφάλμα σύνταξης'],
    notes=['**Πόσα βρίσκει το δεύτερο**: Ανοίξτε δημοσκόπηση στο Zoom, μία επιλογή, με τις απαντήσεις Α έως Δ.',
           '**`{ categories: ["Internet"] }`**: Η μόνη διαφορά από το πρώτο φίλτρο είναι οι αγκύλες. Η σημασία τους εξηγείται στην απάντηση, όχι πριν.',
           '**01:00**: Ξεκινήστε το χρονόμετρο με το πλήκτρο T. Στο τέλος, κλείστε τη δημοσκόπηση και δείξτε τα αποτελέσματα πριν από την επόμενη διαφάνεια.'])

add(type='shell', mins=1, title='Η απάντηση: λιγότερα, %s' % EXACT_ONLY, dense=True,
    cmd=cmd('exact') + '\n' + cmd('all'), cmdLabel='Εντολές', out=out('exact') + '\n' + out('all'), outLabel='Αποτελέσματα',
    points=['Με αγκύλες, το φίλτρο ζητά ακριβώς την ίδια λίστα, με την ίδια σειρά: μόνο «Internet».',
            '%d από τα %s βιβλία έχουν και άλλη κατηγορία.' % (int(EXACT_ALL) - int(EXACT_ONLY), EXACT_ALL),
            '`$all` (τρίτη εντολή): και οι δύο κατηγορίες, σε οποιαδήποτε θέση· %s βιβλία.' % N['all']],
    src='MongoDB Manual: Query an Array.',
    notes=['**λιγότερα, %s**: Σωστή είναι η επιλογή Β, «Λιγότερα από %s».' % (EXACT_ONLY, EXACT_ALL),
           '**Με αγκύλες, το φίλτρο ζητά ακριβώς την ίδια λίστα**: Τα %s βιβλία έχουν μόνη κατηγορία το «Internet». '
           'Χωρίς αγκύλες αρκεί ένα στοιχείο, όπως στη διαφάνεια [[s_perl]].' % EXACT_ONLY,
           '**%d από τα %s βιβλία έχουν και άλλη κατηγορία**: Αυτά χάνονται όταν οι αγκύλες μπουν κατά λάθος. '
           'Δεν εμφανίζεται σφάλμα, και το λάθος περνά απαρατήρητο.' % (int(EXACT_ALL) - int(EXACT_ONLY), EXACT_ALL),
           '**`$all`**: Οι αγκύλες εδώ είναι η λίστα του τελεστή, όχι ακριβής λίστα: αρκεί να υπάρχουν και οι δύο κατηγορίες, με οποιαδήποτε σειρά.'])

add(type='shell', mins=1, title='Σημειογραφία τελείας σε λίστα',
    cmd=cmd('dot'), out=out('dot'),
    points=['`"authors.0"`: ο πρώτος συγγραφέας. Η αρίθμηση ξεκινά από το 0.',
            'Η τελεία της Βραδιάς 1 (`"capital.name"`) λειτουργεί και με θέσεις λίστας. Το όνομα γράφεται σε εισαγωγικά.'],
    src='MongoDB Manual: Query an Array.',
    notes=['**`"authors.0"`**: Η θέση 0 είναι ο πρώτος συγγραφέας της λίστας authors· το `"authors.1"` θα ήταν ο δεύτερος.',
           '**`\'Hibernate in Action (Chinese Edition)\'`**: Το βιβλίο της διαφάνειας [[s_book23]]: ο Christian Bauer είναι πρώτος στη λίστα authors.',
           '**`"capital.name"`**: Στη Βραδιά 1, η τελεία οδηγούσε μέσα σε εμφωλευμένο έγγραφο· εδώ οδηγεί σε μια θέση της λίστας.',
           'Αν ρωτήσουν: και χωρίς το `.0`; Το `%s` δίνει %s: μετρά και το βιβλίο όπου ο Christian Bauer δεν είναι πρώτος συγγραφέας.' % (cmd('dotall'), N['dotall'])])

add(type='shell', mins=1, title='Κανονικές εκφράσεις (regex)',
    cmd=cmd('regex'), cmdLabel='Εντολές', out=out('regex'), outLabel='Αποτελέσματα',
    points=['`/Python/`: ο τίτλος περιέχει «Python» σε οποιοδήποτε σημείο, όπως το `LIKE` της SQL.',
            'Πεζά και κεφαλαία διαφέρουν: το `/python/` δεν βρίσκει τίποτε· με `i` τα βρίσκει όλα.',
            'Η τέταρτη εντολή, με `$regex`, δίνει το ίδιο. Εργασία 2, ενότητα 7.'],
    src='MongoDB Manual: $regex· SQL to MongoDB Mapping Chart.',
    notes=['**`/Python/`**: Η έκφραση γράφεται ανάμεσα σε δύο καθέτους, χωρίς εισαγωγικά. Στην SQL: `WHERE title LIKE \'%Python%\'`.',
           '**Πεζά και κεφαλαία διαφέρουν**: Το `/python/` δίνει %s, για τον ίδιο λόγο που το «internet» της διαφάνειας [[s_counts]] είναι άλλη τιμή από το «Internet». '
           'Με το `i` μετά την κάθετο, δεν γίνεται διάκριση πεζών και κεφαλαίων: %s.' % (REGEX[1], REGEX[2]),
           '**Η τέταρτη εντολή, με `$regex`**: Η ίδια έκφραση, ως κείμενο σε εισαγωγικά. Εργασία 2, ενότητα 7: αναζήτηση «με βάση το περιεχόμενο μιας συμβολοσειράς».',
           'Αν ρωτήσουν: γιατί %s τίτλοι, ενώ η κατηγορία Python έχει %s βιβλία; Δύο τίτλοι (Geoprocessing with Python, IronPython in Action) δεν έχουν καμία κατηγορία, '
           'και το «Hello World!» είναι βιβλίο Python χωρίς τη λέξη στον τίτλο.' % (REGEX[0], PY)])

add(type='shell', mins=1, title='Τα σύμβολα `^`, `$` και `.`',
    cmd=cmd('symbols'), cmdLabel='Εντολές', out=out('symbols'), outLabel='Αποτελέσματα',
    points=['`^`: στην αρχή. `/^The /`: τίτλοι που αρχίζουν από «The ».',
            '`$`: στο τέλος. `/Edition$/`: τίτλοι που τελειώνουν σε «Edition».',
            '`.`: ένας οποιοσδήποτε χαρακτήρας. `/^.#/`: C# και F#.'],
    src='MongoDB Manual: $regex.',
    notes=['**`/^The /`**: Το κενό μετά το «The» ανήκει στην έκφραση: ζητά τη λέξη The, όχι απλώς τα τρία γράμματα. Βρίσκει %s τίτλους.' % THE,
           '**`/Edition$/`**: %s τίτλοι. Το «Hibernate in Action (Chinese Edition)» της διαφάνειας [[s_book23]] δεν μετρά, γιατί τελειώνει σε παρένθεση.' % EDITION,
           '**`/^.#/`**: Η τελεία είναι ένας οποιοσδήποτε χαρακτήρας, εδώ το C ή το F, και το `^` τον θέλει πρώτο.',
           'Αν ρωτήσουν: και αν ζητάμε την ίδια την τελεία, όπως στο «.NET»; Γράφουμε `\\` μπροστά της: το `%s` βρίσκει %s τίτλους.' % (cmd('escape'), N['escape'])])

add(type='shell', mins=1, title='`$elemMatch`: όλες οι συνθήκες στο ίδιο στοιχείο',
    cmd=cmd('elem'), cmdLabel='Εντολές', out=out('elem'), outLabel='Αποτελέσματα',
    points=['%s βιβλία έχουν συγγραφέα που το όνομά του αρχίζει από «Chris».' % CHRIS,
            'Με `$elemMatch`, ο ίδιος συγγραφέας ικανοποιεί και τις δύο συνθήκες: αρχίζει από «Chris» και δεν είναι ο Christian Bauer. Μένουν %s.' % CHRIS_NOT_CB,
            'Οι συνθήκες του `$elemMatch` γράφονται σε ένα έγγραφο, όπως στο φίλτρο του find.'],
    src='MongoDB Manual: Query an Array· $elemMatch.',
    notes=['**`authors: /^Chris/`**: Αρκεί ένας από τους συγγραφείς να αρχίζει από «Chris»: %s βιβλία, μαζί με όσα έχει γράψει ο Christian Bauer.' % CHRIS,
           '**`$elemMatch`**: Και οι δύο συνθήκες ελέγχονται στον ίδιο συγγραφέα. Μένουν %s: φεύγουν τα %s βιβλία του Christian Bauer.' % (CHRIS_NOT_CB, N['dotall']),
           '**Οι συνθήκες του `$elemMatch` γράφονται σε ένα έγγραφο**: Η regex γράφεται εδώ με `$regex` και εισαγωγικά, όπως στην τέταρτη εντολή '
           'της διαφάνειας [[s_regex]].'])

add(type='work', mins=3, timerSec=180, title='Άσκηση 2',
    context='Στο mongosh, στη συλλογή books:',
    items=['Βρείτε τα βιβλία όπου τουλάχιστον ένας από τους συγγραφείς έχει το όνομα «Peter».',
           'Υπόδειξη: `$elemMatch` και `$regex`.',
           'Μετρήστε τα με `countDocuments`.'],
    notes=['**Στο mongosh, στη συλλογή books**: Όσοι δεν έχουν ακόμη τη συλλογή, παρακολουθούν τη λύση στην επόμενη διαφάνεια.',
           '**Υπόδειξη: `$elemMatch` και `$regex`**: Η μορφή είναι αυτή της διαφάνειας [[s_elem]], με άλλο όνομα.',
           '**03:00**: Ξεκινήστε το χρονόμετρο με το πλήκτρο T.',
           'Αν ρωτήσουν: «όνομα» είναι το μικρό όνομα; Ναι, όπως στο «Peter Armstrong».'])

add(type='shell', mins=1, title='Άσκηση 2: η λύση',
    cmd=cmd('ex2'), cmdLabel='Εντολές', out=out('ex2'), outLabel='Αποτελέσματα',
    points=['Τα βιβλία εμφανίζονται με `find` και το ίδιο φίλτρο: %s.' % PETER,
            'Με μία μόνο συνθήκη, το `$elemMatch` δεν χρειάζεται: η δεύτερη εντολή δίνει τα ίδια %s.' % PETER_SIMPLE,
            '`$options: "i"`: χωρίς διάκριση πεζών και κεφαλαίων.'],
    src='MongoDB Manual: $elemMatch (Single Query Condition).',
    notes=['**`$regex: "^Peter"`**: Το `^` ζητά το «Peter» στην αρχή του ονόματος. Θα έβρισκε και ένα «Peterson»· εδώ και τα %s είναι «Peter …».' % PETER,
           '**`$options: "i"`**: Το ίδιο με το `i` της διαφάνειας [[s_regex]]: χωρίς διάκριση πεζών και κεφαλαίων.',
           '**Τα βιβλία εμφανίζονται με `find` και το ίδιο φίλτρο**: Αυτό ζητά το πρώτο βήμα της άσκησης· η λίστα των %s βιβλίων δεν χωρά εδώ.' % PETER,
           '**η δεύτερη εντολή δίνει τα ίδια %s**: Με μία συνθήκη αρκεί η regex πάνω στη λίστα, όπως το `authors: /^Chris/` της διαφάνειας [[s_elem]]. '
           'Το `$elemMatch` χρειάζεται όταν δύο συνθήκες αφορούν τον ίδιο συγγραφέα.' % PETER_SIMPLE])

add(type='shell', mins=1, title='Ταξινόμηση και περιορισμός: sort, limit', dense=True,
    cmd=cmd('sort'), out=out('sort'),
    points=['`sort`: 1 για αύξουσα, -1 για φθίνουσα σειρά. Εδώ: τα πιο πρόσφατα πρώτα.',
            '`limit(3)`: μόνο τα τρία πρώτα. Με `limit(1)`: το πιο πρόσφατο βιβλίο.',
            'Εργασία 2, ενότητα 9: και αύξουσα και φθίνουσα.'],
    src='MongoDB Manual: cursor.sort()· cursor.limit().',
    notes=['**`.sort({ publishedDate: -1 })`**: Ταξινόμηση κατά ημερομηνία έκδοσης· το -1 βάζει πρώτα τα πιο πρόσφατα. Στην SQL: `ORDER BY publishedDate DESC`.',
           '**`.limit(3)`**: Κρατά τα τρία πρώτα της ταξινομημένης λίστας. Στην SQL: `LIMIT 3`.',
           '**Εργασία 2, ενότητα 9**: «Ερωτήματα με ταξινόμηση (αύξουσα και φθίνουσα) και περιορισμό δεδομένων»: χρειάζονται και οι δύο κατευθύνσεις.'])

add(type='shell', mins=1, skippable=True, title='skip: η επόμενη σελίδα αποτελεσμάτων', dense=True,
    cmd=cmd('skip'), out=out('skip'),
    points=['`skip(3)`: παραλείπει τα τρία πρώτα· η δεύτερη σελίδα της προηγούμενης λίστας.',
            'Η σειρά γραφής δεν μετρά: πρώτα ταξινόμηση, μετά παράλειψη, μετά όριο.'],
    src='MongoDB Manual: cursor.skip().',
    notes=['**`.skip(3)`**: Παραλείπει τα τρία βιβλία της προηγούμενης διαφάνειας και δείχνει τα επόμενα τρία.',
           # the swapped chain .limit(3).skip(3) is not in e2p1_cmds.py (not run); the slide's own line states that the order does not matter
           '**Η σειρά γραφής δεν μετρά**: Το `.limit(3).skip(3)` δίνει το ίδιο αποτέλεσμα.'])

add(type='shell', mins=1, kicker='Προσοχή', title='Τα μηδενικά πρώτα',
    cmd=cmd('zeros'), out=out('zeros'),
    points=['Τα «μικρότερα» βιβλία έχουν 0 σελίδες: είναι τα %s με άγνωστο αριθμό.' % ZERO,
            'Με `$gt: 0` στο pageCount, τα τρία πρώτα έχουν %s σελίδες.' % PAGES3],
    src='MongoDB Manual: Comparison/Sort Order.',
    notes=['**`.sort({ pageCount: 1 })`**: Αύξουσα σειρά σελίδων: πρώτα τα βιβλία με τις λιγότερες. Τα τρία πρώτα έχουν 0 σελίδες.',
           '**είναι τα %s με άγνωστο αριθμό**: Το 0 των μετρήσεων της διαφάνειας [[s_counts]]. Ανάμεσα σε ίσες τιμές η σειρά δεν είναι εγγυημένη· '
           'σε άλλη εκτέλεση μπορεί να εμφανιστούν άλλα τρία βιβλία με 0 σελίδες.' % ZERO,
           '**Με `$gt: 0` στο pageCount**: Το φίλτρο αφήνει έξω τα %s βιβλία με 0 σελίδες πριν από την ταξινόμηση.' % ZERO,
           'Αν ρωτήσουν: κι αν το πεδίο λείπει εντελώς; Η MongoDB το ταξινομεί σαν null, πριν από κάθε αριθμό.'])

add(type='remember', mins=1, kicker='Να θυμάστε', title='Τρία σημεία από το Μέρος 1',
    items=['Το find παίρνει δύο έγγραφα: το φίλτρο επιλέγει έγγραφα, η προβολή επιλέγει πεδία.',
           'Σε πεδίο-λίστα αρκεί να ταιριάζει ένα στοιχείο· η λίστα σε αγκύλες ζητά ακριβώς την ίδια λίστα.',
           'Πριν από τα ερωτήματα, κοιτάξτε τα δεδομένα: 0 σελίδες σημαίνει «άγνωστο», και τα πεζά διαφέρουν από τα κεφαλαία.'],
    notes=['**Το find παίρνει δύο έγγραφα**: Διαβάστε τα τρία σημεία όπως είναι. Αν περισσεύει χρόνος, δεν προστίθεται ύλη· το διάλειμμα ξεκινά νωρίτερα.',
           '**η λίστα σε αγκύλες ζητά ακριβώς την ίδια λίστα**: Το ερώτημα της διαφάνειας [[s_poll]]: %s βιβλία χωρίς αγκύλες, %s με αγκύλες.' % (EXACT_ALL, EXACT_ONLY),
           '**0 σελίδες σημαίνει «άγνωστο»**: Ο ίδιος έλεγχος χρειάζεται στα δεδομένα της Εργασίας 2: πριν από την ταξινόμηση, κοιτάξτε αν υπάρχουν μηδενικά ή κενά.'])

add(type='break', mins=3, title='Διάλειμμα',
    next='Στο Μέρος 2: ομαδική άσκηση στη συλλογή books, σε αίθουσες του Zoom. Όποιος δεν ολοκλήρωσε την εισαγωγή, την ολοκληρώνει τώρα.',
    notes=['**Διάλειμμα**: Σταματήστε ακριβώς στην ώρα. Αφήστε τη διαφάνεια στην οθόνη σε όλο το διάλειμμα.',
           '**15:00**: Η αντίστροφη μέτρηση ξεκινά μόνη της και δείχνει πότε ξεκινάμε· το πλήκτρο T την ξαναξεκινά.',
           '**Όποιος δεν ολοκλήρωσε την εισαγωγή, την ολοκληρώνει τώρα**: Στο Μέρος 2 ο καθένας δουλεύει στο δικό του mongosh, με τη συλλογή books. '
           'Τα βήματα είναι στη διαφάνεια [[s_install]].'])

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
       's_book23': num(lambda s: s['title'] == 'Ένα βιβλίο της συλλογής'),
       's_regex': num(lambda s: s['title'].startswith('Κανονικές εκφράσεις')),
       's_elem': num(lambda s: s['title'].startswith('`$elemMatch`')),
       's_poll': num(lambda s: s['type'] == 'poll'),
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
