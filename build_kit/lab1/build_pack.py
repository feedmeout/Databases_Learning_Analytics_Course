"""Student pack for Lab 1 (8 A4 pages, Greek) -> out/Lab1_pack.html ; every number comes from exhibits.json"""
import json, os, html, pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__)); X = json.load(open(f'{HERE}/exhibits.json', encoding='utf8')); L = X['last']; T = X['this']
MID = json.load(open(f'{HERE}/midterm_bands.json', encoding='utf8')); A = pd.read_csv(f'{HERE}/cohort_last_full.csv')
pc = lambda v: f'{round(100*v)}%'; e = html.escape
gr = lambda v, d=2: f'{v:.{d}f}'.replace('.', ',')
def bars(items, unit='%', H=120, tone='blue', dense=False, vmax=None):
    mx = (vmax or 1) if unit == '%' else max(i['v'] for i in items)
    o = [f'<div class="barrow{" dense" if dense else ""}">']
    for i in items:
        h = max(2, round(i['v'] / mx * H)); val = pc(i['v']) if unit == '%' else str(i['v'])
        o.append(f'<div class="bar"><span class="bv">{val}</span><i class="t-{i.get("tone", tone)}" style="height:{h}px"></i><span class="bl">{e(i["l"])}</span>' + (f'<span class="bn">n = {i["n"]}</span>' if 'n' in i else '') + '</div>')
    return ''.join(o) + '</div>'
def band(bs, tone=None): return [dict(l=b['label'], v=b['pass_p'], n=b['n'], **({'tone': tone} if tone else {})) for b in bs]
def fig(title, inner, note=''): return f'<div class="fig"><h3>{e(title)}</h3>{inner}' + (f'<p class="fnote">{note}</p>' if note else '') + '</div>'
def page(n, kicker, title, body, foot='Προσομοιωμένα δεδομένα · περσινή κοόρτη, ' + str(L['n']) + ' φοιτητές'):
    return f'<section class="page"><header><span class="kick">{e(kicker)}</span><h1>{e(title)}</h1></header><div class="content">{body}</div><footer><span>{e(foot)}</span><span>Εργαστήριο 1 · σελίδα {n} από 8</span></footer></section>'
def ask(items): return '<div class="ask"><h3>Ερωτήματα για την ομάδα</h3><ul>' + ''.join(f'<li>{i}</li>' for i in items) + '</ul></div>'
base = L['base']; R = L['rules']; W0 = L['work']['0']; W1 = L['work']['1']; first = L['logins_by_status']['0']; rep = L['logins_by_status']['1']; tm = L['tmat']
P = []
# ---------- page 1
P.append(f'''<section class="page cover"><p class="course">Βάσεις Δεδομένων &amp; Ανάλυση Δεδομένων Μάθησης · Εβδομάδα 2, Μέρος 2</p>
<p class="kick">Εργαστήριο 1 · Πακέτο τεκμηρίων</p><h1 class="big">Ποιους φοιτητές ειδοποιούμε την εβδομάδα 4;</h1>
<div class="sim"><b>Τα δεδομένα αυτού του πακέτου είναι προσομοιωμένα.</b> Το μάθημα, οι φοιτητές και οι αριθμοί δεν αντιστοιχούν σε πραγματικά πρόσωπα ούτε σε πραγματικό ίδρυμα. Οι σχέσεις μεταξύ των μεταβλητών έχουν σχεδιαστεί ώστε να μοιάζουν με όσες αναφέρει η βιβλιογραφία για εισαγωγικά μαθήματα προγραμματισμού.</div>
<h2>Η υπόθεση</h2><p>Σε ένα ελληνικό πανεπιστήμιο, το εισαγωγικό μάθημα προγραμματισμού του πρώτου εξαμήνου έχει περίπου 300 εγγεγραμμένους φοιτητές. Πέρυσι πέρασαν οι {base["passed"]} από τους {L["n"]}. Η διδακτική ομάδα θέλει φέτος, στο <b>τέλος της εβδομάδας 4</b>, να επικοινωνήσει με όσους κινδυνεύουν να μην περάσουν, όσο υπάρχει ακόμη χρόνος. Σας ζητά να της πείτε ποιους δείκτες να εμπιστευθεί. Για να απαντήσετε έχετε τα δεδομένα της περσινής κοόρτης, της οποίας η έκβαση είναι γνωστή.</p>
<h2>Το ζητούμενο</h2><ol class="num"><li><span><b>Έως δύο δείκτες</b> που προτείνετε, με μία πρόταση αιτιολόγησης για τον καθένα.</span></li><li><span><b>Έναν δείκτη που απορρίπτετε</b>, και τον λόγο: διαθεσιμότητα, συγχυτικός παράγοντας, αντίστροφη αιτιότητα ή ποιότητα μέτρησης.</span></li><li><span><b>Μία ομάδα φοιτητών</b> την οποία ο κανόνας σας ενδέχεται να αδικεί, και τι θα κάνατε γι' αυτό.</span></li></ol>
<h2>Πώς δουλεύετε</h2><p>Ορίζετε συντονιστή, που κρατά τον χρόνο, και εισηγητή, που θα κάνει την αναφορά των 3′. Όλοι διαβάζουν τα Τεκμήρια 1 και 2. Τα Τεκμήρια 3 έως 6 μοιράζονται, ένα ή δύο ανά άτομο. Κατόπιν συζητάτε και συμπληρώνετε το φύλλο απάντησης. Δεν γράφετε κώδικα και δεν αλλάζετε τα κατώφλια των κανόνων: επιλέγετε δείκτες.</p>
<h2>Περιεχόμενα</h2><table class="toc"><tr><td>Τεκμήριο 1</td><td>Τα δεδομένα: τι καταγράφεται και πότε</td><td>σελ. 2</td></tr><tr><td>Τεκμήριο 2</td><td>Πόσο καλά ξεχωρίζει κάθε δείκτης όσους δεν πέρασαν</td><td>σελ. 3</td></tr><tr><td>Τεκμήριο 3</td><td>Συνδέσεις στο eclass</td><td>σελ. 4</td></tr><tr><td>Τεκμήριο 4</td><td>Φύλλα εργαστηριακών ασκήσεων</td><td>σελ. 5</td></tr><tr><td>Τεκμήριο 5</td><td>Πλήθος και αλληλουχία υποβολών</td><td>σελ. 6</td></tr><tr><td>Τεκμήριο 6</td><td>Οι κανόνες ανά ομάδα φοιτητών</td><td>σελ. 7</td></tr><tr><td></td><td>Φύλλο απάντησης</td><td>σελ. 8</td></tr></table>
<footer><span>Προσομοιωμένα δεδομένα</span><span>Εργαστήριο 1 · σελίδα 1 από 8</span></footer></section>''')
# ---------- page 2
rows = [('Κατάσταση εγγραφής', 'μητρώο', 'εβδομάδα 1', f"πρώτη εγγραφή {L['status']['0']['n']}, επανεγγραφή {L['status']['1']['n']}"),
        ('Εργασία παράλληλα με τις σπουδές', 'ερωτηματολόγιο', 'εβδομάδα 1', f"όχι {W0['n']}, ναι {W1['n']}"),
        ('Συνδέσεις στο eclass', 'αρχεία καταγραφής του eclass', 'κάθε εβδομάδα', 'όλοι οι φοιτητές'),
        ('Υποβολές κώδικα, E ή S', 'πλατφόρμα αυτόματης αξιολόγησης', 'κάθε εβδομάδα, φύλλα 1 έως 12', f"{L['n_sub']:,} υποβολές στο εξάμηνο".replace(',', '.')),
        ('Φύλλα ασκήσεων εμπρόθεσμα', 'πλατφόρμα αυτόματης αξιολόγησης', 'κάθε εβδομάδα', 'όλοι οι φοιτητές'),
        ('P(E→S)', 'υπολογίζεται από τις υποβολές', 'όταν υπάρχουν 4 τουλάχιστον μεταβάσεις με αφετηρία E', f"την εβδομάδα 4: {int(A.pES_w4.notna().sum())} από {L['n']}"),
        ('Βαθμός προόδου', 'βαθμολόγιο', 'εβδομάδα 8', f"προσήλθαν {int(A.midterm.notna().sum())}"),
        ('Βαθμός τελικής εξέτασης', 'βαθμολόγιο', 'Ιανουάριος', f"προσήλθαν {base['passed'] + base['failed']}")]
P.append(page(2, 'Τεκμήριο 1', 'Τα δεδομένα: τι καταγράφεται και πότε', f'''
<table class="t"><tr><th>Μεταβλητή</th><th>Πηγή</th><th>Διαθέσιμη</th><th>Κάλυψη στην περσινή κοόρτη</th></tr>{''.join(f"<tr><td><b>{e(a)}</b></td><td>{e(b)}</td><td>{e(c)}</td><td>{e(d)}</td></tr>" for a, b, c, d in rows)}</table>
<div class="two"><div><h2>Η έκβαση</h2><p>«Πέρασε»: βαθμός τελικής εξέτασης τουλάχιστον 5. «Δεν πέρασε»: αποτυχία στην εξέταση ή μη προσέλευση.</p>
{fig('Περσινή κοόρτη, ' + str(L['n']) + ' φοιτητές', bars([dict(l='πέρασαν', v=base['passed'], tone='green'), dict(l='απέτυχαν', v=base['failed'], tone='red'), dict(l='δεν προσήλθαν', v=base['noshow'], tone='amber')], unit='', H=100))}</div>
<div><h2>Οι υποβολές κώδικα</h2><p>Δώδεκα εβδομαδιαία φύλλα ασκήσεων, πέντε ασκήσεις το καθένα. Κάθε υποβολή κωδικοποιείται όπως στο Μέρος 1: <b class="E">E</b> σφάλμα μεταγλώττισης, <b class="S">S</b> υποβολή χωρίς σφάλμα. «Εμπρόθεσμο» είναι το φύλλο που υποβλήθηκε μέσα στην εβδομάδα του.</p>
<p><b>P(E→S)</b>: από όλες τις μεταβάσεις με αφετηρία σφάλμα, το ποσοστό που καταλήγει σε επιτυχία. Παράδειγμα: στην ακολουθία <span class="seq">EESEEESSS</span> οι μεταβάσεις με αφετηρία E είναι πέντε και οι δύο καταλήγουν σε S, άρα P(E→S) = 2/5 = 0,40. Με λιγότερες από τέσσερις τέτοιες μεταβάσεις ο δείκτης δεν υπολογίζεται: «ανεπαρκή δεδομένα».</p></div></div>
<div class="note"><b>Η φετινή κοόρτη</b> έχει {T['n']} φοιτητές και βρίσκεται στο τέλος της εβδομάδας 4. Για αυτήν υπάρχουν μόνο όσα καταγράφονται έως εκείνη τη στιγμή. Ό,τι προτείνετε θα εφαρμοστεί σε αυτήν.</div>'''))
# ---------- page 3
order = ['R1', 'R2', 'R3', 'R4', 'R5', 'R6']
tr = ''.join(f"<tr><td><b>{e(X['rules'][k]['name'])}</b></td><td>{e(X['rules'][k]['cut'])}</td><td>{pc(R[k]['flagged_p'])}</td><td>{pc(R[k]['precision'])}</td><td>{pc(R[k]['recall'])}</td><td><b>{pc(R[k]['acc'])}</b></td></tr>" for k in order)
short = {'R1': 'συνδέσεις', 'R2': 'πλήθος υποβολών', 'R3': 'P(E→S)', 'R4': 'φύλλα εμπρόθεσμα', 'R5': 'φύλλα, εξάμηνο', 'R6': 'πρόοδος'}
P.append(page(3, 'Τεκμήριο 2', 'Πόσο καλά ξεχωρίζει κάθε δείκτης όσους δεν πέρασαν', f'''
<p>Κάθε δείκτης συνοδεύεται από έναν έτοιμο κανόνα επισήμανσης. «Επισήμανση» σημαίνει ότι ο φοιτητής θεωρείται ότι κινδυνεύει και η διδακτική ομάδα επικοινωνεί μαζί του. Ο πίνακας δείχνει τι θα είχε συμβεί αν κάθε κανόνας είχε εφαρμοστεί στην περσινή κοόρτη.</p>
<table class="t num tight"><tr><th>Δείκτης</th><th>Επισήμανση όταν</th><th>Επισημαίνονται</th><th>Από όσους επισημαίνονται, δεν πέρασαν</th><th>Από όσους δεν πέρασαν, επισημαίνονται</th><th>Ορθή κατάταξη</th></tr>{tr}</table>
{fig('Ορθή κατάταξη ανά κανόνα', bars([dict(l=short[k], v=R[k]['acc'], tone=('grey' if k in ('R1', 'R2') else 'blue')) for k in order], H=70), f"Για σύγκριση: αν επισημανθούν όλοι οι φοιτητές, κατατάσσεται ορθά το {pc(L['flag_all_acc'])}, δηλαδή όσοι δεν πέρασαν.")}
<div class="note"><b>Πώς διαβάζονται οι στήλες.</b> «Επισημαίνονται»: ποσοστό της κοόρτης με το οποίο θα επικοινωνούσε η διδακτική ομάδα. «Από όσους επισημαίνονται, δεν πέρασαν»: πόσο συχνά η επισήμανση επιβεβαιώνεται. «Από όσους δεν πέρασαν, επισημαίνονται»: πόσους από όσους χρειάζονταν βοήθεια εντοπίζει ο κανόνας. «Ορθή κατάταξη»: ποσοστό όλων των φοιτητών για τους οποίους ο κανόνας είχε δίκιο. Στον κανόνα του P(E→S), οι φοιτητές με ανεπαρκή δεδομένα δεν επισημαίνονται.</div>
{ask(['Ποιοι δείκτες προηγούνται στην κατάταξη; Πριν τους προτείνετε, ελέγξτε στο Τεκμήριο 1 πότε γίνονται διαθέσιμοι.', 'Οι τέσσερις ερωτήσεις του Μέρους 1: πότε γίνεται η πρόβλεψη, με ποια δεδομένα, σε ποια κοόρτη ελέγχθηκε, ποιο είναι το βασικό ποσοστό.'])}'''))
# ---------- page 4
P.append(page(4, 'Τεκμήριο 3', 'Συνδέσεις στο eclass, εβδομάδες 1 έως 4', f'''
<div class="two">{fig('Όλοι οι φοιτητές: ποσοστό επιτυχίας ανά πλήθος συνδέσεων', bars(band(L['logins3']), H=140))}
{fig('Οι ίδιοι φοιτητές, ανά κατάσταση εγγραφής', '<div class="grp2"><div>' + bars(band(first, 'amber'), H=140) + '<p class="gl">πρώτη εγγραφή</p></div><div>' + bars(band(rep, 'grey'), H=140) + '<p class="gl">επανεγγραφή</p></div></div>')}</div>
<table class="t num"><tr><th></th><th>Φοιτητές</th><th>Συνδέσεις, εβδομάδες 1 έως 4 (μέσος όρος)</th><th>Πέρασαν</th><th>Δεν προσήλθαν στην εξέταση</th></tr>
<tr><td><b>Πρώτη εγγραφή</b></td><td>{L['status']['0']['n']}</td><td>{gr(L['logins_mean_by_status']['0'], 1)}</td><td>{pc(L['status']['0']['pass_p'])}</td><td>{pc(L['status']['0']['noshow_p'])}</td></tr>
<tr><td><b>Επανεγγραφή</b> (το μάθημα οφείλεται από προηγούμενο έτος)</td><td>{L['status']['1']['n']}</td><td>{gr(L['logins_mean_by_status']['1'], 1)}</td><td>{pc(L['status']['1']['pass_p'])}</td><td>{pc(L['status']['1']['noshow_p'])}</td></tr></table>
<div class="note">Κανόνας επισήμανσης: έως 8 συνδέσεις στις εβδομάδες 1 έως 4. Ορθή κατάταξη: {pc(R['R1']['acc'])}. Για σύγκριση: αν επισημανθούν απλώς όλοι οι φοιτητές με επανεγγραφή, χωρίς κανένα ίχνος από το eclass, η ορθή κατάταξη είναι {pc(L['registry_only']['acc'])}.</div>
{ask(['Τι αλλάζει στη σχέση συνδέσεων και επιτυχίας όταν οι φοιτητές χωριστούν ανά κατάσταση εγγραφής;', 'Τι γνωρίζει ήδη η γραμματεία την εβδομάδα 1, πριν καταγραφεί οποιαδήποτε σύνδεση;', 'Αν η διδακτική ομάδα συμβούλευε τους φοιτητές «να συνδέονται συχνότερα», θα άλλαζε το ποσοστό επιτυχίας;'])}'''))
# ---------- page 5
lw = L['last_week_noshow']
P.append(page(5, 'Τεκμήριο 4', 'Φύλλα εργαστηριακών ασκήσεων', f'''
<div class="two">{fig('Επιτυχία ανά πλήθος φύλλων, όλο το εξάμηνο (από 12)', bars(band(L['labs_sem']), H=130))}{fig('Επιτυχία ανά φύλλα εμπρόθεσμα, εβδομάδες 1 έως 4 (από 4)', bars(band(L['labs_w4'], 'light'), H=130))}</div>
<div class="prop"><b>Πρόταση προς τη συνέλευση του τμήματος.</b> «Όσοι υπέβαλαν 9 έως 12 φύλλα πέρασαν σε ποσοστό {pc(L['labs_sem'][2]['pass_p'])}, ενώ όσοι υπέβαλαν έως 3 φύλλα σε ποσοστό μόλις {pc(L['labs_sem'][0]['pass_p'])}. Προτείνεται τα φύλλα ασκήσεων να γίνουν υποχρεωτικά, ώστε να αυξηθεί το ποσοστό επιτυχίας.»</div>
<div class="two">{fig('Εβδομάδα τελευταίας δραστηριότητας των ' + str(base['noshow']) + ' φοιτητών που δεν προσήλθαν στην εξέταση', bars([dict(l=str(k + 1), v=v) for k, v in enumerate(lw)], unit='', H=110, tone='red', dense=True), 'Δραστηριότητα: σύνδεση στο eclass ή υποβολή κώδικα. Εβδομάδα 13: ενεργοί έως το τέλος του εξαμήνου.')}
<div><table class="t num"><tr><th>Έκβαση</th><th>Φύλλα στο εξάμηνο (μέσος όρος)</th></tr><tr><td>Πέρασαν</td><td>{gr(L['labs_sem_mean']['passed'], 1)}</td></tr><tr><td>Απέτυχαν στην εξέταση</td><td>{gr(L['labs_sem_mean']['failed'], 1)}</td></tr><tr><td>Δεν προσήλθαν</td><td>{gr(L['labs_sem_mean']['noshow'], 1)}</td></tr></table>
<p class="small">Κανόνες επισήμανσης: έως 6 φύλλα στο εξάμηνο (ορθή κατάταξη {pc(R['R5']['acc'])})· έως 2 φύλλα εμπρόθεσμα στις εβδομάδες 1 έως 4 (ορθή κατάταξη {pc(R['R4']['acc'])}).</p></div></div>
{ask(['Στηρίζουν τα διαγράμματα την πρόταση προς τη συνέλευση; Ποια εναλλακτική εξήγηση από το Μέρος 1 ταιριάζει εδώ;', 'Γιατί ο ίδιος δείκτης είναι τόσο ισχυρότερος στο σύνολο του εξαμήνου απ\' ό,τι στις εβδομάδες 1 έως 4;', 'Ποια από τις δύο εκδοχές του δείκτη μπορεί να χρησιμοποιηθεί στο τέλος της εβδομάδας 4;'])}'''))
# ---------- page 6
def mat(key, title):
    m = tm[key]; return f'<div class="mx"><h4>{e(title)} ({m["n"]})</h4><table><tr><th></th><th>προς E</th><th>προς S</th></tr><tr><th>από E</th><td>{gr(m["EE"])}</td><td class="hl">{gr(m["ES"])}</td></tr><tr><th>από S</th><td>{gr(m["SE"])}</td><td>{gr(m["SS"])}</td></tr></table><p>διάμεσος υποβολών: {m["nsub_median"]:.0f}</p></div>'
P.append(page(6, 'Τεκμήριο 5', 'Πλήθος και αλληλουχία υποβολών, εβδομάδες 1 έως 4', f'''
<div class="two">{fig('Επιτυχία ανά πλήθος υποβολών κώδικα', bars(band(L['nsub'], 'grey'), H=130))}{fig('Επιτυχία ανά P(E→S)', bars(band(L['pes'], 'green'), H=130), f"Ανεπαρκή δεδομένα: {L['pes_insuf']['n']} φοιτητές· από αυτούς πέρασε το {pc(L['pes_insuf']['pass_p'])}.")}</div>
<h2>Μέσοι πίνακες μεταβάσεων ανά έκβαση</h2><p>Υπολογίζονται όπως στο παράδειγμα του Μέρους 1: οι μεταβάσεις όλων των φοιτητών κάθε ομάδας αθροίζονται και κάθε γραμμή διαιρείται με το άθροισμά της.</p>
<div class="three">{mat('passed', 'Πέρασαν')}{mat('failed', 'Απέτυχαν στην εξέταση')}{mat('noshow', 'Δεν προσήλθαν')}</div>
<div class="note">Κανόνες επισήμανσης: έως 15 υποβολές (ορθή κατάταξη {pc(R['R2']['acc'])})· P(E→S) κάτω από 0,35 (ορθή κατάταξη {pc(R['R3']['acc'])}· από όσους επισημαίνονται δεν πέρασε το {pc(R['R3']['precision'])}).</div>
{ask(['Ποιοι φοιτητές έχουν λίγες υποβολές και ποιοι πάρα πολλές; Είναι το ίδιο είδος φοιτητή;', 'Οι δύο δείκτες προέρχονται από τις ίδιες υποβολές. Γιατί συμπεριφέρονται τόσο διαφορετικά;', 'Ποια ομάδα ξεχωρίζει το P(E→S) και ποια όχι; Συγκρίνετε τις στήλες «Απέτυχαν» και «Δεν προσήλθαν».'])}'''))
# ---------- page 7
def wrow(label, f): return f'<tr><td>{label}</td><td>{f(W0)}</td><td>{f(W1)}</td></tr>'
P.append(page(7, 'Τεκμήριο 6', 'Οι κανόνες ανά ομάδα φοιτητών', f'''
<p>Στο ερωτηματολόγιο της εβδομάδας 1, {W1['n']} από τους {L['n']} φοιτητές δήλωσαν ότι εργάζονται παράλληλα με τις σπουδές τους. Ο πίνακας συγκρίνει τις δύο ομάδες.</p>
<table class="t num"><tr><th></th><th>Δεν εργάζονται ({W0['n']})</th><th>Εργάζονται ({W1['n']})</th></tr>
{wrow('<b>Δεν πέρασαν το μάθημα</b>', lambda w: pc(w['np_p']))}
{wrow('Φύλλα εμπρόθεσμα, εβδομάδες 1 έως 4 (μέσος όρος, από 4)', lambda w: gr(w['labs_w4_mean'], 1))}
{wrow('Φύλλα στο σύνολο του εξαμήνου (μέσος όρος, από 12)', lambda w: gr(w['labs_sem_mean'], 1))}
{wrow('Υποβολές κώδικα, εβδομάδες 1 έως 4 (διάμεσος)', lambda w: f"{w['nsub_median']:.0f}")}
{wrow('<b>P(E→S): ανεπαρκή δεδομένα την εβδομάδα 4</b>', lambda w: pc(w['insuf_p']))}
{wrow('Επισημαίνονται από τον κανόνα P(E→S) κάτω από 0,35', lambda w: pc(w['R3']['flagged_p']))}
{wrow('&nbsp;&nbsp;από όσους δεν πέρασαν, επισημαίνονται', lambda w: pc(w['R3']['recall']))}
{wrow('<b>Επισημαίνονται από τον κανόνα «έως 2 φύλλα εμπρόθεσμα»</b>', lambda w: pc(w['R4']['flagged_p']))}
{wrow('&nbsp;&nbsp;από όσους επισημαίνονται, δεν πέρασαν', lambda w: pc(w['R4']['precision']))}</table>
<div class="two">{fig('Επισήμανση από τον κανόνα «έως 2 φύλλα εμπρόθεσμα»', bars([dict(l='δεν εργάζονται', v=W0['R4']['flagged_p'], tone='blue'), dict(l='εργάζονται', v=W1['R4']['flagged_p'], tone='red')], H=120))}{fig('Πράγματι δεν πέρασαν', bars([dict(l='δεν εργάζονται', v=W0['np_p'], tone='grey'), dict(l='εργάζονται', v=W1['np_p'], tone='grey')], H=120))}</div>
{ask(['Οι δύο ομάδες περνούν το μάθημα εξίσου συχνά. Γιατί ο κανόνας των φύλλων τις αντιμετωπίζει τόσο διαφορετικά; Δείτε τη δεύτερη και την τρίτη γραμμή του πίνακα.', 'Τι σημαίνει «ανεπαρκή δεδομένα» για έναν φοιτητή που εργάζεται και τι για έναν που δεν εργάζεται;', 'Τι θα προτείνατε στη διδακτική ομάδα για τους φοιτητές που ο κανόνας σας δεν «βλέπει» καλά;'])}'''))
# ---------- page 8
line = lambda n=1: ''.join('<div class="wl"></div>' for _ in range(n))
P.append(page(8, 'Φύλλο απάντησης', 'Η απάντηση της ομάδας μας', f'''
<div class="ans"><p><b>Αίθουσα / ομάδα:</b> <span class="blank"></span> &nbsp; <b>Εισηγητής:</b> <span class="blank"></span></p></div>
<div class="ans"><h2>1. Προτείνουμε (έως δύο δείκτες)</h2><p>Δείκτης: <span class="blank w"></span></p><p>Γιατί:</p>{line(2)}<p>Δείκτης: <span class="blank w"></span></p><p>Γιατί:</p>{line(2)}</div>
<div class="ans"><h2>2. Απορρίπτουμε</h2><p>Δείκτης: <span class="blank w"></span> &nbsp; Τεκμήριο στο οποίο στηριζόμαστε: <span class="blank s"></span></p>
<p class="chk"><span>☐ διαθεσιμότητα</span><span>☐ συγχυτικός παράγοντας</span><span>☐ αντίστροφη αιτιότητα</span><span>☐ ποιότητα μέτρησης</span></p><p>Σε μία πρόταση:</p>{line(2)}</div>
<div class="ans"><h2>3. Μία ομάδα φοιτητών που ο κανόνας μας ενδέχεται να αδικεί</h2><p>Ποια ομάδα και γιατί:</p>{line(2)}<p>Τι θα κάναμε:</p>{line(2)}</div>
<div class="note"><b>Η αναφορά των 3′.</b> Ο εισηγητής διαβάζει τις τρεις απαντήσεις με αυτή τη σειρά. Μία πρόταση αιτιολόγησης για καθεμία αρκεί. Οι άλλες ομάδες σημειώνουν σε τι διαφωνούν· η συζήτηση γίνεται μετά την αποκάλυψη του τρόπου με τον οποίο κατασκευάστηκαν τα δεδομένα.</div>''', foot='Προσομοιωμένα δεδομένα'))
CSS = '''@page{size:A4;margin:0}*{box-sizing:border-box;margin:0;padding:0}
:root{--ink:#12233F;--mist:#EEF3FA;--deep:#0D47A1;--muted:#55657C;--body:#33445E;--green:#2E9E5B;--amber:#F2A413;--amber-ink:#8A5A00;--amber-bg:#FFF4DA;--red:#D8433B;--red-bg:#FCE9E7;--line:#D3DDEB}
body{font-family:'Commissioner','Segoe UI',Arial,sans-serif;color:var(--ink);font-size:10.6pt;line-height:1.42;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.page{width:210mm;height:297mm;padding:15mm 16mm 13mm;display:flex;flex-direction:column;page-break-after:always;break-after:page;overflow:hidden;position:relative}
header{border-bottom:2.2pt solid var(--amber);padding-bottom:3mm;margin-bottom:5mm}.kick{font-size:10pt;font-weight:700;color:var(--amber-ink);letter-spacing:.02em}
h1{font-size:19pt;line-height:1.15;font-weight:800;letter-spacing:-.01em;margin-top:1mm}h1.big{font-size:27pt;margin:2mm 0 5mm}
h2{font-size:12.5pt;font-weight:800;margin:4.5mm 0 1.5mm;color:var(--deep)}h3{font-size:10.4pt;font-weight:700;margin-bottom:2mm}h4{font-size:10pt;font-weight:700;margin-bottom:1.5mm}
p{text-align:justify;margin-bottom:2mm}.small{font-size:9.4pt;color:var(--body);margin-top:3mm}.course{font-size:9.5pt;color:var(--muted);margin-bottom:9mm}
.content{flex:1;display:flex;flex-direction:column;gap:3.5mm}footer{display:flex;justify-content:space-between;font-size:8.4pt;color:var(--muted);border-top:.6pt solid var(--line);padding-top:2mm;margin-top:auto}
.cover footer{position:absolute;left:16mm;right:16mm;bottom:13mm}
.sim{background:var(--amber-bg);border-left:3pt solid var(--amber);border-radius:2mm;padding:4mm 5mm;text-align:justify;margin-bottom:2mm}
ol.num{list-style:none;counter-reset:n;display:grid;gap:2mm}ol.num li{counter-increment:n;display:grid;grid-template-columns:8mm 1fr;text-align:justify}ol.num li::before{content:counter(n);width:5.6mm;height:5.6mm;border-radius:50%;background:var(--ink);color:#fff;font-size:9pt;font-weight:700;display:grid;place-items:center}
table{border-collapse:collapse;width:100%}.toc td{padding:1.15mm 2mm;border-bottom:.6pt solid var(--line)}.toc td:first-child{font-weight:700;width:26mm}.toc td:last-child{text-align:right;width:16mm;color:var(--muted)}
.t th{background:var(--ink);color:#fff;font-size:9.2pt;text-align:left;padding:2mm 2.4mm;font-weight:700;line-height:1.2;vertical-align:bottom}.t td{padding:1.9mm 2.4mm;border-bottom:.6pt solid var(--line);font-size:9.8pt;vertical-align:top}.t tr:nth-child(odd) td{background:#F7F9FC}
.t td b{word-spacing:.09em}.t.tight td{padding:1.3mm 2.4mm}.t.num td:not(:first-child),.t.num th:not(:first-child){text-align:center}.t.num td:first-child{width:46%}
.two{display:grid;grid-template-columns:1fr 1fr;gap:5mm;align-items:start}.three{display:grid;grid-template-columns:repeat(3,1fr);gap:4mm}
.fig{background:var(--mist);border-radius:3mm;padding:3.5mm 4mm 3mm}.fnote{font-size:8.8pt;color:var(--body);margin:2mm 0 0;text-align:left}
.barrow{display:flex;gap:3mm;align-items:flex-end;justify-content:center;padding-top:1mm}.bar{display:flex;flex-direction:column;align-items:center;justify-content:flex-end;width:21mm}
.bar i{display:block;width:100%;border-radius:1.6mm 1.6mm 0 0}.t-blue{background:var(--deep)}.t-red{background:var(--red)}.t-green{background:var(--green)}.t-amber{background:var(--amber)}.t-grey{background:#8795AA}.t-light{background:#A9C8F0}
.bv{font-size:10pt;font-weight:800;margin-bottom:.8mm}.bl{font-size:8.6pt;font-weight:700;text-align:center;line-height:1.15;border-top:1.2pt solid var(--ink);width:calc(100% + 3mm);padding-top:1.2mm}.bl{min-height:8.4mm}.bn{font-size:7.8pt;color:var(--muted)}
.two>*{min-width:0}.two .bar{width:16mm}.two .barrow{gap:2.2mm}.two .bl{font-size:8.2pt}.barrow.dense{gap:1.4mm}.barrow.dense .bar,.two .barrow.dense .bar{width:4.4mm}.barrow.dense .bv{font-size:7.4pt}.barrow.dense .bl{font-size:7.6pt;width:calc(100% + 1.4mm);min-height:0}
.grp2{display:flex;gap:6mm;justify-content:center;align-items:flex-end}.grp2 .bar{width:14mm}.gl{text-align:center;font-size:9pt;font-weight:700;color:var(--deep);margin:1.5mm 0 0}
.note{background:var(--mist);border-radius:2.5mm;padding:3mm 4mm;font-size:9.6pt;text-align:justify}.prop{background:var(--red-bg);border-left:3pt solid var(--red);border-radius:2mm;padding:3.5mm 4.5mm;text-align:justify}
.ask{border:1.2pt solid var(--ink);border-radius:3mm;padding:3.5mm 4.5mm;margin-top:auto}.ask h3{color:var(--deep)}.ask ul{list-style:none;display:grid;gap:1.6mm}.ask li{padding-left:5mm;position:relative;text-align:justify}.ask li::before{content:"";position:absolute;left:.6mm;top:1.9mm;width:2mm;height:2mm;border-radius:50%;background:var(--ink)}
.E,.S,.seq{font-family:ui-monospace,Menlo,Consolas,monospace}.E{color:#A92C25}.S{color:#14532D}
.mx{background:var(--mist);border-radius:3mm;padding:3.5mm 4mm}.mx table{margin:1mm 0}.mx th{font-size:8.6pt;color:var(--muted);font-weight:700;padding:1mm}.mx td{background:#fff;border-radius:1.5mm;text-align:center;font-size:13pt;font-weight:800;padding:2.4mm 1mm;border:1.2mm solid var(--mist)}.mx td.hl{background:var(--deep);color:#fff}.mx p{font-size:8.8pt;color:var(--body);margin:1mm 0 0;text-align:left}
.ans{border:.8pt solid var(--line);border-radius:3mm;padding:3.5mm 4.5mm}.ans h2{margin-top:0}.blank{display:inline-block;border-bottom:.8pt solid var(--muted);width:48mm;height:4mm;vertical-align:bottom}.blank.w{width:120mm}.blank.s{width:22mm}.wl{border-bottom:.8pt solid var(--line);height:7.2mm}.chk{display:flex;gap:7mm;font-size:10pt;margin:2mm 0}'''
HTML = f'<!DOCTYPE html><html lang="el"><head><meta charset="UTF-8"><title>Εργαστήριο 1: πακέτο τεκμηρίων</title><link href="https://fonts.googleapis.com/css2?family=Commissioner:wght@400;500;700;800&display=swap" rel="stylesheet"><style>{CSS}</style></head><body>{"".join(P)}</body></html>'
os.makedirs(f'{HERE}/../out', exist_ok=True); open(f'{HERE}/../out/Lab1_pack.html', 'w', encoding='utf8').write(HTML); print('pack html written,', len(P), 'pages')
