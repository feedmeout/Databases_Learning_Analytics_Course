# Week 2, Part 1 outline (v1, awaiting approval). One entry per slide: (minutes, flag, Greek title, what is on it, source)
# flag: '' | 'SKIP' (skippable) | 'POLL' (the one timed question, 60 s) | 'FIG' (your own figure reused)
TITLE = 'Μέθοδοι με βάση το ερώτημα'
OUTLINE = [
('Άνοιγμα', [
 (1,'','Μέθοδοι με βάση το ερώτημα','Title slide, name and affiliation as on your decks.',''),
 (1,'','Το πλάνο της βραδιάς','Three parts with clock times. The only place the part structure appears; no footline.',''),
 (1,'','Πού βρισκόμαστε: δεδομένα → δείκτης → ανάλυση → δράση','The thread from the Week 1 roadmap with «ανάλυση» lit. Week 1 gave data and indicators; tonight is what is done with them.',''),
 (2,'','Από το ερώτημα στην οικογένεια μεθόδων','Four rows: educational question → family → what comes out. Πρόβλεψη, Εύρεση Δομών και Προτύπων, Εξόρυξη σχέσεων, Ακολουθίες. One line points to Part 3 for visualisation. The algorithms are known to this cohort; the question is what is new. Survivor of your 2.6 and of posters 9.6 and 9.8.','Baker & Inventado (2014), reference model · Romero & Ventura (2020)'),
]),
('Πρόβλεψη (your 3.24)', [
 (1,'','Πρόβλεψη (Prediction)','Your definition and your two questions verbatim («Ποιοι μαθητές βαριούνται;», «Ποιοι μαθητές θα αποτύχουν στην τάξη;») and your line «Συμπεραίνουμε κάτι που έχει σημασία, ώστε να κάνουμε κάτι για αυτό!».','Baker & Inventado (2014)'),
 (1,'','Ανατομία μιας πρόβλεψης: η προηγούμενη κοόρτη','Build 1 of 2. Last year\'s cohort: traces up to the prediction point, known outcome, model.',''),
 (1,'','Ανατομία μιας πρόβλεψης: η τρέχουσα κοόρτη','Build 2 of 2. This year\'s cohort at the same point: risk estimate, then intervention. The earlier the prediction, the fewer the data. This is the frame of Lab 1.',''),
 (2,'','Μελέτη: ποιοι κινδυνεύουν να αποτύχουν στην εξέταση προγραμματισμού;','Programming course at the University of Turku on ViLLE: ongoing formative-assessment scores, a classification tree the instructor can read, students at risk of failing the final exam. Numbers taken from the open-access full text at build.','Veerasamy, Laakso & D\'Souza (2022), Informatics in Education 21(2)'),
 (2,'','Προσοχή: τέσσερις ερωτήσεις προς κάθε μελέτη πρόβλεψης','Πότε γίνεται η πρόβλεψη; Με ποια δεδομένα; Σε ποια κοόρτη ελέγχθηκε; Ποιο είναι το βασικό ποσοστό αποτυχίας; A reading checklist (no empirical claim), reused in the assignment and in Lab 1.',''),
 (1,'','Προσοχή: ένα μοντέλο δεν μεταφέρεται αυτούσιο σε άλλο μάθημα','15 courses, 50 course offerings, mixed-effects models: behaviour indicators explain a low share of the variance in grades and differ little from each other; a large share sits with the student.','Jovanović, Saqr, Joksimović & Gašević (2021), Computers & Education 172'),
]),
('Εύρεση Δομών και Προτύπων (your 3.23)', [
 (1,'','Εύρεση Δομών και Προτύπων (Structure Discovery)','Your definition («Δεν υπάρχει συγκεκριμένη μεταβλητή στόχου ή πρόβλεψης») and your three questions verbatim. English term corrected from "Pattern Recognition" to the taxonomy\'s "Structure Discovery".','Baker & Inventado (2014)'),
 (2,'','Μελέτη: καταστάσεις εμπλοκής σε ένα πλήρες πρόγραμμα σπουδών','99 φοιτητές, 4 έτη, 15 μαθήματα, 1.383 εγγραφές σε μαθήματα. Latent Class Analysis on every course enrolment gives engagement states; nobody labelled the students in advance (University of Eastern Finland).','Saqr & López-Pernas (2021), EC-TEL 2021, LNCS 12884'),
 (1,'','Τι έδειξαν οι τροχιές','Early disengagement (not engaged in at least one first-term course) goes with higher dropout, lower grades and lower graduation rates; early engagement is relatively stable. Second line from the follow-up: engagement at a single time point is not a consistent indicator of high achievement. Both feed Lab 1.','Saqr & López-Pernas (2021) · Saqr, López-Pernas, Helske & Hrastinski (2023), Computers & Education 199'),
 (1,'','Προσοχή: ο αλγόριθμος επιστρέφει πάντοτε ομάδες','Three checks: internal cohesion (silhouette), stability, an external variable. Naming a cluster is interpretation. Your own study runs all three, which the next block shows.',''),
]),
('Εξόρυξη σχέσεων (your 3.25)', [
 (1,'','Εξόρυξη σχέσεων (Relationship Mining)','Your definition and your two questions verbatim. Four forms in one line: κανόνες συσχέτισης, συσχετίσεις, ακολουθιακά πρότυπα, αιτιακή εξόρυξη. English term corrected from "Relationship extraction".','Baker & Inventado (2014)'),
 (2,'','Μελέτη: ποιες συσχετίσεις αναπαράγονται από μάθημα σε μάθημα;','The same indicator-grade correlations computed course by course and pooled with meta-analysis, within one discipline and one pedagogical model: moderate variability within and across courses, few indicators hold. Numbers from the full text at build.','Saqr, Jovanović, Viberg & Gašević (2022), Studies in Higher Education 47(12)'),
 (2,'','Προσοχή: τρεις εξηγήσεις για κάθε συσχέτιση','Συγχυτικός παράγοντας, αντίστροφη αιτιότητα, επιλογή. Generic wording, no case named: it arms the students for Lab 1 without giving the planted features away.',''),
]),
('Ακολουθίες: η μελέτη των αρχάριων προγραμματιστών (your 7.2-7.11)', [
 (1,'','Εκπαιδευτική αξιολόγηση: τι δείχνει ο βαθμός','Your table, step 1: students A-F with total grade (100, 98, 94, 50, 41, 30). «Καλύτεροι; Χειρότεροι;»','Your slide 7.3'),
 (1,'','Μαθησιακή Αναλυτική: το περιεχόμενο των υποβολών έχει σημασία','Step 2: the attempts column appears (1500, 348, 200, 410, 100, 1100). Your sentence verbatim.','Your slide 7.3'),
 (1,'','Από την υποβολή στην ακολουθία','E: compilation error, S: no compilation error. Μαθητής Α: EEEEEE, Μαθητής Β: ESSSSS, pairs of consecutive submissions.','Your slide 7.4'),
 (1,'SKIP','Αλυσίδες Markov: υπενθύμιση','Your rain / sun chain (25%, 75%, 0%, 100%), rebuilt natively.','Your slide 7.5'),
 (1,'','Τέσσερις μεταβάσεις','(E,S), (E,E), (S,E), (S,S) with the question marks still on the arrows.','Your slide 7.6'),
 (1,'','Παράδειγμα υπολογισμού: καταμέτρηση μεταβάσεων','WORKED EXAMPLE, step 1: one short sequence of a hypothetical student (E E S E E E S S S), pairs counted into a 2x2 table.',''),
 (1,'','Παράδειγμα υπολογισμού: ο πίνακας μεταβάσεων','WORKED EXAMPLE, step 2: divide each row by its sum; the question marks of slide 22 are replaced by the four probabilities.',''),
 (2,'POLL','Ερώτημα: ίδια συχνότητα, διαφορετική αλληλουχία','Two students with the same share of successful submissions, Α: E E E S S S and Β: E S E S E S. In which is the E→S probability higher? Three options (Α, Β, ίση). 60-second timer; the next slide does not depend on the result. The answer (Β) is in the notes.',''),
 (1,'','Στάδια μεταβάσεων: η πλήρης μηχανή καταστάσεων','The eight published states (Met success, Met error, Repeated error, Repeated success, Runtime error, Unmodified error submission, Unmodified success submission, Completion on first attempt), rebuilt natively.','Lokkila, Christopoulos & Laakso (2023), Informatics in Education 22(2), Fig. 1'),
 (1,'','Πίνακας μεταβάσεων: ένας για κάθε φοιτητή','Collate, Aggregate, Normalize, Finalize; the result is 29 variables per student.','Lokkila, Christopoulos & Laakso (2023), Informatics in Education'),
 (1,'','Τα δεδομένα της μελέτης','665 φοιτητές, 376.475 υποβολές, 192 ασκήσεις κώδικα· Java (2017) και Python (2021), Πανεπιστήμιο του Τούρκου, ViLLE.','Lokkila, Christopoulos & Laakso (2023), Informatics in Education, Table 2'),
 (1,'FIG','Από τον πίνακα στις ομάδες: k-means Clustering','k = 3, chosen from inertia and silhouette. Your scatter plot (7.11) shown large.','Lokkila, Christopoulos & Laakso (2023) · your slide 7.11'),
 (1,'','Επικύρωση των ομάδων','The three clusters differ in self-reported prior programming experience in weeks 1-5 and not after; Syntactic Score: ρ = −0,68 with number of submissions, ρ = −0,72 with error rate; week-to-week cluster stability about 40% (Python) and 30% (Java). Perceived difficulty by cluster from the ITiCSE paper.','Lokkila, Christopoulos & Laakso (2023) · (2022), ITiCSE \'22'),
 (2,'SKIP','Java ή Python; Η ίδια μέθοδος σε άλλο ερώτημα','Error rate of submissions about 59% (Java) against about 52% (Python); a model trained on the Java courses places only 9 of the 365 Python students in the weakest group. Your t-SNE figure (7.9) with your caption.','Lokkila, Christopoulos & Laakso (2023), Journal of Information Systems Education 34(1), Tables 3 and 8 · your slide 7.9'),
 (1,'','Προβληματισμοί','Your two questions from 7.11 («Προβλήματα να γράψουν κώδικα;», «Προβλήματα στην επίλυση προβλημάτων;») and the limitations the paper itself states: one university, one clustering algorithm, self-reported experience.','Lokkila, Christopoulos & Laakso (2023)'),
]),
('Κλείσιμο', [
 (1,'','Σύνοψη: ερώτημα, μέθοδος, έλεγχος','The table of slide 4 with a third column: what to check before trusting the result (cohort and base rate; cluster validation; rival explanations; what the states mean).',''),
 (1,'','Τρία σημεία από το Μέρος 1','«Να θυμάστε»: three lines.',''),
 (3,'','Διάλειμμα','«Επιστρέφουμε σε 15′» with the 15:00 countdown. One line: after the break, Εργαστήριο 1 in groups. The 3 minutes are the slack.',''),
]),
]
# What I opened, and what still rests on my own knowledge
SOURCES = [
('Lokkila, Christopoulos & Laakso (2023). Automatically detecting previous programming knowledge from novice programmer code compilation history. Informatics in Education, 22(2), 277-294. doi:10.15388/infedu.2023.15','Full text opened (ERIC copy)','All numbers on slides 26-30 and 32 come from it.'),
('Lokkila, Christopoulos & Laakso (2023). A data-driven approach to compare the syntactic difficulty of programming languages. Journal of Information Systems Education, 34(1), 84-93','Full text opened (jise.org)','Slide 31. Note: the running text says "9 students out of 356", but Tables 1, 6 and 8 all give 365 Python students (92 + 273); the slide uses 365.'),
('Lokkila, Christopoulos & Laakso (2022). A clustering method to detect disengaged students from their code submission history. ITiCSE \'22, Vol. 1, 228-234','University of Turku research-portal record and abstract opened','Only the abstract-level claim (clusters differ in perceived difficulty) is used.'),
('Veerasamy, Laakso & D\'Souza (2022). Formative assessment tasks as indicators of student engagement for predicting at-risk students in programming courses. Informatics in Education, 21(2), 375-393. doi:10.15388/infedu.2022.15','Journal record and abstract opened; open access','Full text to be opened at build for cohort size and accuracy figures.'),
('Jovanović, Saqr, Joksimović & Gašević (2021). Students matter the most in learning analytics. Computers & Education, 172, 104251','Abstract opened (Monash research record)','The three claims on slide 10 are in the abstract.'),
('Saqr, Jovanović, Viberg & Gašević (2022). Is there order in the mess? Studies in Higher Education, 47(12), 2370-2391. doi:10.1080/03075079.2022.2061450','Publisher page and repository copy opened (abstract, introduction)','Number of courses and the list of indicators that replicate: from the full text at build.'),
('Saqr & López-Pernas (2021). The dire cost of early disengagement: a four-year learning analytics study over a full program. EC-TEL 2021, LNCS 12884. doi:10.1007/978-3-030-86436-1_10','Abstract opened (Springer)','Every number on slides 12-13 is in the abstract. Its journal-length companion (Computers & Education 175, 104325) I have seen only as a bibliographic record, so nothing is taken from it.'),
('Saqr, López-Pernas, Helske & Hrastinski (2023). The longitudinal association between engagement and achievement varies by time, students\' profiles, and achievement state. Computers & Education, 199, 104787','Abstract opened (University of Turku repository); open access, CC BY','One sentence on slide 13. One co-author is at the University of Turku.'),
('Baker & Inventado (2014). Educational data mining and learning analytics. In Larusson & White (Eds.), Learning Analytics: From Research to Practice, 61-75. doi:10.1007/978-1-4614-3305-7_4','Author\'s draft and repository record opened','Reference model (allowed exception to the 2020+ rule). Your definitions on 3.23-3.25 translate its wording.'),
('Romero & Ventura (2020), WIREs Data Mining and Knowledge Discovery','Verified in Week 1 (already on Week 1, Part 1); not re-opened today',''),
]
