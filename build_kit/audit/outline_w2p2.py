# Week 2, Part 2 = GROUP LAB 1 (outline v1, awaiting approval). One entry per slide: (minutes, flag, Greek title, what is on it)
# flag: '' | 'SKIP' (skippable) | 'TIMER' (timer on the slide; label = timer)
TITLE = 'Εργαστήριο 1: δείκτες έγκαιρης προειδοποίησης'
OUTLINE = [
('Ενημέρωση (5′)', [
 (1,'','Εργαστήριο 1: ποιους φοιτητές ειδοποιούμε την εβδομάδα 4;','The case in four lines: introductory programming course, about 300 registered students, roughly half do not pass, the teaching team wants to contact students at the end of week 4. States on the slide that the data are simulated.'),
 (1,'','Τι καταγράφηκε και πότε','The Part 1 "anatomy" timeline reused: registry and week-1 questionnaire, weekly eclass logins, weekly lab submissions as E/S sequences, midterm in week 8, January exam. Prediction point: end of week 4. Last year\'s cohort (outcome known) and this year\'s (week 4 only).'),
 (1,'','Έξι υποψήφιοι δείκτες','Table: indicator, source, time window. Logins wk 1-4; number of submissions wk 1-4; P(E→S) wk 1-4; lab sheets handed in on time wk 1-4; lab sheets over the whole semester; midterm grade.'),
 (1,'','Το ζητούμενο','Three things per group: up to two indicators you recommend; one you reject, with the reason; one group of students your rule may treat unfairly, and what you would do about it.'),
 (1,'','Πώς δουλεύουμε','Zoom rooms of 3-5, a coordinator and a rapporteur, the 8-page pack (who reads what), and the two checklists from Part 1 (four questions; three rival explanations).'),
]),
('Ομάδες (17′) και αναφορές (9′)', [
 (17,'TIMER','Εργασία σε ομάδες','17:00 timer. The three prompts stay on screen. Two broadcast messages for the rooms are in the notes (minute 6, minute 12).'),
 (9,'TIMER','Αναφορά ομάδων','03:00 timer, restarted for each group. Three rooms = 9′. With four rooms the two skippable slides go and one minute comes from the slack.'),
]),
('Αποκάλυψη: πώς κατασκευάστηκαν τα δεδομένα (10′)', [
 (1,'','Πώς κατασκευάστηκαν τα δεδομένα','Build 1 of the process diagram: two hidden traits (δεξιότητα, δέσμευση) and two roads to not passing (αποτυχία στην εξέταση, μη προσέλευση).'),
 (1,'','Τι μετρά κάθε ίχνος','Build 2: each trace attached to its real cause. P(E→S) ← skill; lab sheets on time ← commitment; logins ← enrolment status; number of submissions ← both, with opposite signs.'),
 (1,'','Πρόοδος: ο ισχυρότερος δείκτης δεν υπάρχει την εβδομάδα 4','Availability. Pass rate by midterm band 22% / 26% / 67% / 91%, and the midterm takes place in week 8.'),
 (1,'','Συνδέσεις στο eclass: συγχυτικός παράγοντας','Pooled: 32% pass with few logins against 54%. Among first-time students: 50% against 56%. The registry alone classifies 61% correctly, the logins rule 59%.'),
 (1,'','Ασκήσεις όλου του εξαμήνου: αντίστροφη αιτιότητα','Pass rate 6% / 35% / 78% by lab sheets over the semester, against 30% to 69% for the week 1-4 window. Whoever leaves the course stops handing in: the Course Signals pattern.'),
 (1,'','Πλήθος υποβολών: η συχνότητα δεν αρκεί','Inverted U: 32% / 57% / 52% / 36% pass by number of submissions, against a monotonic 16% / 40% / 65% / 71% by P(E→S). Your 7.3 argument, in data.'),
 (1,'','P(E→S): έγκυρος δείκτης, άνιση μέτρηση','Working students: P(E→S) cannot be computed for 42% of them (20% for the rest), and "lab sheets on time" flags 80% of them (31% of the rest), although both groups pass equally often (45% and 47%).'),
 (1,'SKIP','Οι κανόνες στη φετινή κοόρτη','Every candidate rule on last year\'s and on this year\'s cohort. Best combination: 71% correct last year, 70% this year.'),
 (1,'','Δύο δρόμοι, δύο δείκτες','P(E→S) separates those who fail the exam; lab sheets on time separate those who never sit it. Two reasons, two interventions: the bridge to Week 3.'),
 (1,'SKIP','Υπόδειγμα απάντησης','A model three-part answer, so the PDF works for self-study.'),
]),
('Κλείσιμο', [
 (1,'','Να θυμάστε','Three points.'),
 (3,'','Διάλειμμα','«Επιστρέφουμε σε 15′», countdown. Next: Part 3.'),
]),
]
if __name__ == '__main__':
    n = sum(len(b[1]) for b in OUTLINE); m = sum(s[0] for b in OUTLINE for s in b[1]); print(n, 'slides', m, 'minutes')
