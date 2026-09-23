# Week 3, Part 2 = GROUP LAB 2 + ethics debrief (outline v1, awaiting approval). One entry per slide: (minutes, flag, Greek title, what is on it, source)
# flag: '' | 'SKIP' (skippable) | 'TIMER' (timer on the slide; the timer is the only time label) | 'REAL' (numbers from the real dataset, lab2/explore.py)
TITLE = 'Εργαστήριο 2: κατώφλι, δικαιοσύνη, παρέμβαση. Θέματα ηθικής'
OUTLINE = [
('Ενημέρωση', [
 (1,'REAL','Εργαστήριο 2: ποιοι φοιτητές θα λάβουν τι;','The case in four lines. Polytechnic Institute of Portalegre (Portugal), 4.424 students of undergraduate degrees; outcome at the end of the normal duration of the course: 2.209 graduated, 1.421 dropped out, 794 still enrolled. The data feed a deployed tool that gives the tutoring team a dropout-risk estimate. Said on the slide: real, anonymised, CC BY 4.0.','Realinho, Machado, Baptista & Martins (2022), Data 7(11), 146 · UCI dataset 697'),
 (1,'REAL','Τι είναι γνωστό και πότε','Three moments: at enrolment (academic path, demographics, socio-economic data such as scholarship, debts, tuition fees, parents\' occupation and qualification, plus macro-economic indicators), end of semester 1, end of semester 2. The same model at the three moments: AUC 0,80 → 0,89 → 0,91. Tonight the prediction is made at the end of semester 1. It is the «πότε;» of Week 2 with real data.','Own analysis of the UCI file (80/20 split, as the authors recommend)'),
 (1,'','Το ζητούμενο','Three products per room: (Α) the action you choose and the threshold that follows from it; (Β) the subgroup your rule treats worst, which kind of unfairness it is, and what you do about it; (Γ) the message to a flagged student, 60 words at most.',''),
 (1,'','Πώς δουλεύουμε','One team of about four per Zoom room (automatic assignment), a coordinator and a rapporteur, the 8-page pack (who reads what), one answer sheet per room. Page 7 of the pack repeats the three tools of Part 1: kinds of action, definitions of fairness, rules for the message.',''),
]),
('Ομάδες και αναφορές', [
 (15,'TIMER','Εργασία σε ομάδες','Timer 15:00. The three products as prompts; pack pages on the foot line. Notes: rooms open for 15′ with automatic closing; broadcast at minute 5 «Έχετε επιλέξει ενέργεια; Το κατώφλι έπεται.» and at minute 11 «Τέσσερα λεπτά: γράψτε το μήνυμα.»; visit each room once and ask, never answer.',''),
 (5,'TIMER','Δύο ομάδες παρουσιάζουν','Timer 02:30 per team. Fixed format that does not depend on what they chose: action, threshold, how many are flagged; the subgroup; the message read aloud. The other rooms note one difference from their own sheet.',''),
]),
('Τι έδειχναν τα τεκμήρια', [
 (1,'REAL','Το ίδιο κατώφλι, σε πραγματικούς αριθμούς','885 students the model had not seen, 284 of whom dropped out. Threshold 0,2: 376 flagged, 132 for nothing, 40 missed. Threshold 0,7: 180 flagged, 18 for nothing, 122 missed. The slide of Part 1, now with people who existed.','Own analysis of the UCI file'),
 (1,'REAL','Ποιοι βρίσκονται στην κορυφή της λίστας','Capacity for 100 meetings: 99 of the 100 highest risks did drop out, and 71 of them had passed no unit at all in semester 1. The model is most certain where it is already too late. Highest risk is not highest benefit; among students with at least one passed unit the model finds 61% of the dropouts.','Own analysis of the UCI file'),
 (1,'REAL','Άνισα σφάλματα, αυτή τη φορά με άνισα βασικά ποσοστά','Scholarship holders: 13% drop out against 39% of the rest, and 67% of their dropouts are missed against 21%. Tuition fees not up to date: 84% drop out, and 56% of those who stayed were flagged against 8%. This is the right-hand column of Part 1, slide 17: it cannot be repaired, only chosen. Groups of 30 (international) or 12 (special needs) cannot be audited at all.','Own analysis of the UCI file'),
 (1,'REAL','Τι βαραίνει στο μοντέλο','Largest weights: units passed in semester 1, tuition fees up to date, scholarship, age at enrolment, mother\'s occupation, the unemployment rate. The model flags whoever owes money: the fitting action is financial, not a tutorial. Two roads again, with real data.','Own analysis of the UCI file'),
 (1,'SKIP','Υπόδειγμα απάντησης','One defensible answer for those who study the PDF alone: light action with threshold 0,3; scholarship holders as the group to watch, with a second look by the tutor instead of a lower cut for all; a message that names what was observed. Other answers hold as well.',''),
]),
('Το νομικό πλαίσιο', [
 (2,'','GDPR: τέσσερις αρχές που συναντήσατε απόψε','Table, each row tied to the pack: lawful basis (for a public university the public task rather than consent) · purpose limitation (fee records were collected for billing) · data minimisation against the need to hold an attribute in order to audit fairness (the note of Part 1, slide 19), with the answer the law gives: special categories may exceptionally be processed for bias detection and correction, under strict conditions · special categories (the variable «εκπαιδευτικές ειδικές ανάγκες» is health data).','Regulation (EU) 2016/679, Articles 5, 6, 9 (at build) · AI Act, Article 10(5) (opened)'),
 (2,'','Κανονισμός για την Τεχνητή Νοημοσύνη: τι υποχρεώνει το «υψηλού κινδύνου»','Week 1 said that education is a high-risk area and that emotion inference is banned; not repeated. Tonight: what the label obliges. Data governance with examination for bias, information to the deploying institution, human oversight, accuracy, the right to an explanation of an individual decision. Whether an early-warning tool falls under Annex III is shown as an open question next to the wording of the law, not as my verdict. One line on where the law stands: the 2026 amendment postponed the application of the high-risk obligations, education included; the prohibitions and the AI-literacy duty already apply; the content of the obligations did not change. Years only, no dates.','Regulation (EU) 2024/1689, Articles 10, 14, 86 (opened); 13, 15, 26, Annex III(3) (at build) · Regulation (EU) 2026/1744 (opened through five legal notes; Official Journal text at build) · Kaliisa, Baker, Wasson & Prinsloo (2025) (at build)'),
]),
('Τα επτά ερωτήματά σας', [
 (1,'','Συγκατάθεση','Your question verbatim (4.3): «Θα πρέπει να ζητείται από τους μαθητές συγκατάθεση…;» · where you met it tonight: nobody asked these 4.424 students whether their fee status may predict their dropout · one line of law: consent is not a valid ground where there is a clear imbalance, in particular where the controller is a public authority.','Your deck 4 · GDPR, Recital 43 (opened); Article 6 (at build)'),
 (1,'','Σε ποιον ανήκουν τα δεδομένα και ποιος έχει πρόσβαση','(4.5) verbatim · tonight: who sees the risk estimate, the tutor, the teacher, the student? · the right of access, and the Illuminate breach of your slide 4.20 as one line of text, with its source.','Your deck 4 · GDPR, Articles 13-15 · The New York Times (2022) — at build'),
 (1,'','Πόσο μπορούμε να στηριχθούμε στα αποτελέσματα','(4.7) verbatim · tonight: at threshold 0,4 about one flag in five is wrong, and the outcome «ακόμη εγγεγραμμένος» is neither success nor dropout.','Your deck 4 · own analysis'),
 (1,'','Πώς μειώνεται η παρερμηνεία','(4.9) verbatim · tonight: the message you wrote; a probability read as a verdict · the duty of AI literacy for staff who use such systems.','Your deck 4 · AI Act, Article 4 (opened; the 2026 amendment touched it, final wording at build)'),
 (1,'','Ευθύνη να ενεργήσουμε','(4.11) verbatim: the central dilemma of the lab. You knew of 270 students at risk and could see 100. Knowing creates an obligation that capacity cannot honour.','Your deck 4 · Prinsloo & Slade (2017), LAK \'17 — at build'),
 (1,'','Αυτονομία των φοιτητών','(4.13) verbatim · tonight: a flag that changes the advice (the EAB case of Part 1) · the right not to be subject to a decision based solely on automated processing, including profiling, with legal or similarly significant effects; and what «solely» means when a person merely confirms a score.','Your deck 4 · GDPR, Article 22 (opened) · CJEU, C-634/21 SCHUFA (at build)'),
 (1,'','Μεσολάβηση ανθρώπου','(4.15) verbatim · tonight: the question Part 1 sent here · human oversight is an obligation for high-risk systems, and the law names automation bias as something the overseer must remain aware of.','Your deck 4 · AI Act, Article 14(4)(b) (opened)'),
 (1,'SKIP','Το ερώτημα που μένει ανοιχτό','Your closing question (4.21) verbatim: «Κατά την άποψή σας, ποιο είναι το μεγαλύτερο ηθικό πρόβλημα με τις πρακτικές μαθησιακής αναλυτικής;» No discussion time is planned for it; it is left with them.','Your deck 4'),
]),
('Κλείσιμο', [
 (1,'','Να θυμάστε: τρία σημεία από το Εργαστήριο 2','Η ενέργεια επιλέγεται πρώτη· το κατώφλι έπεται. · Όπου τα βασικά ποσοστά διαφέρουν, η ανισότητα των σφαλμάτων δεν διορθώνεται: επιλέγεται και τεκμηριώνεται. · Ό,τι αποφασίσατε απόψε ως ομάδα, το δίκαιο το απαιτεί από το ίδρυμα: σκοπός, έλεγχος μεροληψίας, εξήγηση, ανθρώπινη εποπτεία.',''),
 (3,'','Διάλειμμα','«Επιστρέφουμε σε 15′» with the countdown. Next: νέες κατευθύνσεις και το δεύτερο εργαστήριο της εργασίας. Carries the 3 minutes of slack.',''),
]),
]

# Audit of the source material for this part: (item, action, what I found, what happens)
AUDIT = [
 ('Deck 4, your seven questions (4.3, 4.5, 4.7, 4.9, 4.11, 4.13, 4.15)', 'KEEP', 'Their full text is in the kit, so nothing is needed from you. They are good questions and they are yours.', 'Kept verbatim, one slide each (14-20), each tied to a decision the teams have just taken and to one line of law or literature.'),
 ('Deck 4, slide 4.2: two recommendations of a 2014 EU report', 'CUT', 'Older than the GDPR and the AI Act.', 'Replaced by slides 12 and 13.'),
 ('Deck 4, slide 4.20: New York Times on the Illuminate breach (2022)', 'UPDATE', 'A 9 MB animation of a newspaper page: third-party image.', 'One line of text with its source on slide 15. No image, so the PowerPoint is not needed.'),
 ('Deck 4, slides 4.16-4.17: teacher quote «…να αγνοώ τους μαθητές μου και να επικεντρώνομαι στα δεδομένα»', 'CUT', 'The slide names a person but no publication, and I cannot trace the quote.', 'Left out, unless you tell me where it comes from.'),
 ('Deck 4, cartoons (4.4, 4.6, 4.8, 4.10, 4.12, 4.14, 4.18)', 'CUT', 'Third-party images, no credit on the slides, several at low resolution.', 'Left out. A lab part with two timers has no room for them anyway.'),
 ('Deck 4, 4.19 and 4.21', 'KEEP', '4.19 was used as the teaser of Week 1. 4.21 is your closing question.', '4.21 becomes slide 21 (skippable).'),
 ('Old E3 practical (both datasets)', 'CUT', 'Already decided in Part 1\'s audit: noise and a leaking label.', 'Its FORMAT is the format of this lab.'),
 ('Realinho dataset, UCI 697', 'USE', 'Verified today at the source: 4.424 students, 36 features plus the outcome, no missing values, outcome Graduate 2.209 / Dropout 1.421 / Enrolled 794, licence CC BY 4.0 (stated in the data descriptor). I downloaded the file and ran the analysis below.', 'The lab stands on it. Two cautions go into the teacher key: 180 rows have zero enrolled units in semester 1 and 75 of those students graduated (zeros that are not zeros); the Zenodo copy is restricted, the UCI copy is open.'),
]

# What the pack will contain (student PDF, 8 pages), with the numbers already computed
PACK = [
 ('1', 'Η περίπτωση και τα δεδομένα', 'Real data, source, licence, the three outcomes, what is known when, the list of variables by kind (academic, demographic, socio-economic, macro-economic).'),
 ('2', 'Τεκμήριο 1: πότε προβλέπουμε', 'The same model at enrolment, after semester 1, after semester 2: AUC 0,80 / 0,89 / 0,91; accuracy 79% / 85% / 86%.'),
 ('3', 'Τεκμήριο 2: το κατώφλι', 'Six thresholds on 885 unseen students: flagged 376 / 317 / 270 / 231 / 208 / 180; for nothing 132 / 91 / 59 / 39 / 29 / 18; missed 40 / 58 / 73 / 92 / 105 / 122.'),
 ('4', 'Τεκμήριο 3: η δυναμικότητα', 'The 50 and the 100 highest risks: 49 of 50 and 99 of 100 dropped out; 71 of the 100 had passed no unit in semester 1.'),
 ('5', 'Τεκμήριο 4: οι υποομάδες', 'Per group: base rate, share flagged, flagged for nothing, missed. Gender, scholarship, debtor, tuition fees, displaced, age band, and two groups too small to judge (international n = 30, special needs n = 12).'),
 ('6', 'Τεκμήριο 5: τι βαραίνει στο μοντέλο', 'The ten largest standardised weights, in words.'),
 ('7', 'Υπενθύμιση από το Μέρος 1', 'Three kinds of action, three definitions of fairness, four rules for the message.'),
 ('8', 'Φύλλο απάντησης', 'Α, Β, Γ: one per room.'),
]

# (source, what I opened, status)  status: OPENED | TODO (opened before it goes on a slide)
SOURCES = [
 ('UCI Machine Learning Repository, dataset 697, doi:10.24432/C5MC89', 'The repository\'s own record (through its API and its page) and the data file itself: 4.424 rows, 37 columns, no missing values, class counts, donated in 2021.', 'OPENED'),
 ('Realinho, Machado, Baptista & Martins (2022). Predicting Student Dropout and Academic Success. Data 7(11), 146. doi:10.3390/data7110146', 'Title page and abstract of the open-access article: data descriptor, «Dataset License: CC BY 4.0», the tool that informs the tutoring team. The number of degrees, the academic years covered, the definition of «Enrolled» and the coding of gender are read in the full text at build.', 'OPENED'),
 ('Martins, Tolledo, Machado, Baptista & Realinho (2021), WorldCIST, doi:10.1007/978-3-030-72657-7_16', 'The citation that UCI asks for; it goes on the pack next to the data descriptor.', 'OPENED'),
 ('AI Act, Regulation (EU) 2024/1689: Articles 4, 10(5), 14 and 86', 'The wording of each article on sites that reproduce the Official Journal text: AI literacy of staff (4); special categories may exceptionally be processed for bias detection and correction, six conditions (10(5)); human oversight, with automation bias named in 14(4)(b); clear and meaningful explanation of the role of the system in an individual decision (86).', 'OPENED'),
 ('Regulation (EU) 2026/1744 (the 2026 amendment of the AI Act)', 'Five independent legal notes that agree: published and in force in 2026; the high-risk obligations of Annex III, education included, now apply later than first planned; prohibitions, AI literacy and transparency keep their dates; Article 4 amended, and the bias-detection basis moved and widened. NEW since Week 1 was written; Week 1 stays correct because it gave no dates. The Official Journal text itself is opened at build.', 'OPENED'),
 ('GDPR, Regulation (EU) 2016/679: Article 22(1) and Recital 43', 'Exact wording of both.', 'OPENED'),
 ('GDPR Articles 5, 6, 9, 13-15 · AI Act Articles 13, 15, 26 and Annex III(3), and the final wording after the 2026 amendment · CJEU C-634/21 (SCHUFA)', 'Not opened yet. Each is opened before its slide is written; whatever I cannot confirm is dropped.', 'TODO'),
 ('Prinsloo & Slade (2017), the obligation to act · Kaliisa, Baker, Wasson & Prinsloo (2025) · The New York Times (2022) on Illuminate', 'Not opened yet.', 'TODO'),
]
