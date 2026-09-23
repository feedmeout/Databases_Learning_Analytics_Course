# One-page teacher guide for nosql/NoSQL_Evening1_demo.js -> ../out/NoSQL_Evening1_demo_instructions.html (+ PDF with lab1/topdf.py)
import os, re, html
H = os.path.dirname(os.path.abspath(__file__)); K = os.path.join(H, '..'); e = html.escape
CSS = re.search(r"CSS = '''(.*?)'''", open(f'{K}/lab1/build_pack.py', encoding='utf8').read(), re.S).group(1)
CSS += '''
.page{padding:10mm 14mm 8mm}.content{gap:1.1mm}header{margin-bottom:3mm;padding-bottom:2mm}h1{font-size:17pt}
h2{font-size:11pt;color:var(--deep);margin:1.5mm 0 .3mm}p.lead{font-size:9.1pt;line-height:1.32;text-align:justify;margin:0}
ol.st,ul.st{margin:0 0 0 5mm;padding:0}ol.st li,ul.st li{font-size:9pt;line-height:1.3;margin:.45mm 0;text-align:justify}
code{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:8.6pt;background:var(--mist);padding:.15mm 1mm;border-radius:1mm;white-space:nowrap}
table.fx{width:100%;border-collapse:collapse;font-size:8.5pt;line-height:1.26}table.fx code{white-space:normal}table.fx th{background:var(--ink);color:#fff;text-align:left;padding:1.3mm 2mm;font-size:8.4pt}
table.fx td{padding:1mm 2mm;border-bottom:.6pt solid var(--line);vertical-align:top;text-align:left}table.fx td:first-child{width:36%}
.note{background:var(--mist);border-radius:2mm;padding:1.6mm 3mm;font-size:8.9pt;line-height:1.3;text-align:justify}
'''
c = lambda t: f'<code>{e(t)}</code>'
body = f'''
<p class="lead">Το αρχείο {c("NoSQL_Evening1_demo.js")} δεν εκτελείται μόνο του. Είναι σημειωματάριο με τις εντολές της επίδειξης, με τη σειρά των διαφανειών 15 έως 28 του Μέρους 3. Το ανοίγετε, αντιγράφετε μία εντολή, την επικολλάτε στο mongosh και πατάτε Enter. Οι διαφάνειες δείχνουν ήδη κάθε εντολή με την πραγματική της έξοδο· αν κάτι δεν λειτουργήσει την ώρα του μαθήματος, συνεχίζετε απλώς από τις διαφάνειες.</p>
<h2>1. Μία φορά, πριν από το μάθημα (περίπου 15 λεπτά)</h2>
<ol class="st">
<li><b>Διακομιστής:</b> {c("mongodb.com/try/download/community")}, πλατφόρμα Windows, πακέτο msi. Στον οδηγό εγκατάστασης: Complete και «Install MongoD as a Service». Ο διακομιστής ξεκινά μόνος του, και σε κάθε εκκίνηση του υπολογιστή.</li>
<li><b>Κέλυφος:</b> {c("mongodb.com/try/download/shell")}, πακέτο msi. Το mongosh δεν περιλαμβάνεται στην εγκατάσταση του διακομιστή.</li>
<li><b>Έλεγχος:</b> σε τερματικό (Command Prompt, PowerShell ή Windows Terminal) γράψτε {c("mongosh")} και Enter. Αν εμφανιστεί η προτροπή {c("test>")}, όλα λειτουργούν. Έξοδος με {c("exit")}.</li>
<li><b>Κενή βάση:</b> αν δοκιμάσατε εντολές, γράψτε στο mongosh {c("use world")} και μετά {c("db.dropDatabase()")}, ώστε η επίδειξη να ξεκινήσει από την αρχή.</li>
</ol>
<h2>2. Πώς ανοίγετε το αρχείο</h2>
<p class="lead">Δεξί κλικ στο αρχείο, «Άνοιγμα με», Σημειωματάριο (Notepad) ή VS Code. <b>Όχι διπλό κλικ:</b> τα Windows θεωρούν τα αρχεία .js σενάρια, θα επιχειρήσουν να το εκτελέσουν και θα εμφανίσουν μήνυμα σφάλματος.</p>
<h2>3. Κατά τη διάρκεια του Μέρους 3</h2>
<ul class="st">
<li>Ανοιχτά δύο παράθυρα: το τερματικό με το mongosh και το αρχείο. Μεγαλώστε τα γράμματα του τερματικού (στο Windows Terminal: Ctrl και ροδέλα του ποντικιού), ώστε να διαβάζονται στο Zoom.</li>
<li>Στο Zoom μοιραστείτε ολόκληρη την οθόνη: περνάτε από τις διαφάνειες στο τερματικό χωρίς νέα κοινή χρήση.</li>
<li>Στο αρχείο, κάθε γραμμή {c("// Διαφάνεια …")} δείχνει ποιες εντολές ανήκουν σε ποια διαφάνεια. Για κάθε διαφάνεια από την 15 έως την 28: αντιγραφή μίας εντολής, επικόλληση στο mongosh (Ctrl+V ή δεξί κλικ), Enter, και επιστροφή στη διαφάνεια για τα σημεία της.</li>
<li>Η εντολή {c("insertMany")} (διαφάνεια 19) πιάνει έξι γραμμές: αντιγράψτε τις έξι μαζί. Όσο η εντολή δεν έχει κλείσει, το mongosh δείχνει {c("...")}· με την τελευταία γραμμή εκτελείται.</li>
<li>Διαφάνεια 21: μετά το παράδειγμα με την Ιταλία, εκτελέστε και τη γραμμή {c("deleteOne")} που ακολουθεί, για να καθαρίσει η συλλογή.</li>
<li>Διαφάνεια 27 (δημοσκόπηση): μην εκτελέσετε τίποτε. Οι δύο εντολές της διαφάνειας 28 εκτελούνται μετά την ψηφοφορία.</li>
<li>Τα ObjectId που θα δείτε διαφέρουν από εκείνα των διαφανειών, γιατί περιέχουν τη στιγμή δημιουργίας. Είναι αναμενόμενο.</li>
</ul>
<h2>4. Αν κάτι δεν πάει καλά</h2>
<table class="fx"><tr><th>Τι βλέπετε</th><th>Τι κάνετε</th></tr>
<tr><td>Το mongosh δεν αναγνωρίζεται ως εντολή</td><td>Κλείστε και ανοίξτε ξανά το τερματικό. Αν επιμένει, προσθέστε στη μεταβλητή PATH τον φάκελο εγκατάστασης του mongosh.</td></tr>
<tr><td>{c("MongoNetworkError: connect ECONNREFUSED 127.0.0.1:27017")}</td><td>Ο διακομιστής δεν τρέχει: Υπηρεσίες των Windows ({c("services.msc")}), MongoDB Server, Έναρξη.</td></tr>
<tr><td>{c("E11000 duplicate key error")} στη διαφάνεια 18</td><td>Η επίδειξη έχει ήδη τρέξει μία φορά: {c("use world")}, {c("db.dropDatabase()")} και ξανά από τη διαφάνεια 17.</td></tr>
<tr><td>Το mongosh μένει σε {c("...")}</td><td>Η εντολή δεν ολοκληρώθηκε. Ctrl+C μία φορά καθαρίζει την ημιτελή εντολή (δεύτερο Ctrl+C κλείνει το mongosh)· μετά, επικόλληση ξανά.</td></tr>
</table>
<p class="note">Στο τέλος της επίδειξης η συλλογή country έχει τρία έγγραφα: Ελλάδα, Γαλλία, Γερμανία. Δεν χρειάζεται να τα διαγράψετε· αν θέλετε να επαναλάβετε την επίδειξη, ξεκινήστε από το βήμα 4 της ενότητας 1.</p>
'''
page = (f'<section class="page"><header><span class="kick">Μη σχεσιακές βάσεις · Βραδιά 1 · Μέρος 3</span><h1>Η επίδειξη στο mongosh: οδηγίες</h1></header>'
        f'<div class="content">{body}</div><footer><span>Οδηγός διδάσκοντος · δεν διανέμεται στους φοιτητές</span><span>σελίδα 1 από 1</span></footer></section>')
out = os.path.join(K, 'out', 'NoSQL_Evening1_demo_instructions.html')
open(out, 'w', encoding='utf8').write(f'<!DOCTYPE html><html lang="el"><head><meta charset="UTF-8"><title>Η επίδειξη στο mongosh: οδηγίες</title>'
    f'<link href="https://fonts.googleapis.com/css2?family=Commissioner:wght@400;500;700;800&display=swap" rel="stylesheet"><style>{CSS}</style></head><body>{page}</body></html>')
print('wrote', out)
