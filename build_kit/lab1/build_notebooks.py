"""Optional Colab notebooks for Lab 1 (student and teacher versions), data embedded so that no hosting is needed."""
import nbformat as nbf, base64, gzip, os, json
HERE = os.path.dirname(os.path.abspath(__file__)); D = f'{HERE}/data'
def emb(path): return base64.b64encode(gzip.compress(open(path, 'rb').read(), 9)).decode()
def chunk(s, n=100): return '(\n' + '\n'.join(f'    "{s[i:i+n]}"' for i in range(0, len(s), n)) + '\n)'
md = lambda t: nbf.v4.new_markdown_cell(t); code = lambda t: nbf.v4.new_code_cell(t)
def loader(files):
    L = ['import base64, gzip, io', 'import numpy as np, pandas as pd, matplotlib.pyplot as plt', '', '# Τα δεδομένα είναι ενσωματωμένα στο σημειωματάριο (CSV, συμπιεσμένα). Δεν χρειάζεται κανένα εξωτερικό αρχείο.', 'def _load(b64): return pd.read_csv(io.BytesIO(gzip.decompress(base64.b64decode(b64))))', '']
    for var, path in files: L.append(f'_{var} = {chunk(emb(path))}'); L.append(f'{var} = _load(_{var})')
    L.append(''); L.append("print({k: v.shape for k, v in dict(" + ', '.join(f'{v}={v}' for v, _ in files) + ").items()})")
    return '\n'.join(L)
INTRO = '''# Εργαστήριο 1: δείκτες έγκαιρης προειδοποίησης την εβδομάδα 4
**Βάσεις Δεδομένων & Ανάλυση Δεδομένων Μάθησης · Εβδομάδα 2, Μέρος 2 · προαιρετικό σημειωματάριο**

> **Τα δεδομένα είναι προσομοιωμένα.** Το μάθημα, οι φοιτητές και οι αριθμοί δεν αντιστοιχούν σε πραγματικά πρόσωπα ούτε σε πραγματικό ίδρυμα.

Το σημειωματάριο αυτό δεν χρειάζεται για το εργαστήριο. Απευθύνεται σε όσους θέλουν, μετά τη συνεδρία, να αναπαραγάγουν τα τεκμήρια του πακέτου και να δοκιμάσουν δικούς τους κανόνες.

- Περσινή κοόρτη: όλα τα δεδομένα του εξαμήνου, με γνωστή έκβαση.
- Φετινή κοόρτη: μόνο όσα υπάρχουν στο τέλος της εβδομάδας 4, χωρίς έκβαση.

Εκτελέστε τα κελιά με τη σειρά (Runtime → Run all).'''
DICT = '''## Τα δεδομένα

| Πίνακας | Μία γραμμή ανά | Στήλες |
|---|---|---|
| `students_last` | φοιτητή της περσινής κοόρτης | `enrolment` (first, repeat), `works`, `logins_w1_4`, `submissions_w1_4`, `EE`, `ES`, `SE`, `SS`, `p_ES_w1_4`, `sheets_on_time_w1_4` (0 έως 4), `sheets_semester` (0 έως 12), `midterm`, `exam`, `no_show`, `passed`, `last_active_week` |
| `students_this` | φοιτητή της φετινής κοόρτης | μόνο οι στήλες που υπάρχουν στο τέλος της εβδομάδας 4 |
| `submissions_last`, `submissions_this` | άσκηση που επιχειρήθηκε | `sheet`, `exercise`, `week`, `late`, `sequence` (π.χ. `EESS`) |
| `logins_last` | φοιτητή | συνδέσεις στο eclass ανά εβδομάδα, `w1` έως `w13` |

`E`: σφάλμα μεταγλώττισης. `S`: υποβολή χωρίς σφάλμα. `p_ES_w1_4`: P(E→S) από τις εμπρόθεσμες υποβολές των εβδομάδων 1 έως 4· κενό όταν υπάρχουν λιγότερες από τέσσερις μεταβάσεις με αφετηρία E («ανεπαρκή δεδομένα»).'''
LOOK = '''L = students_last.copy(); L["not_passed"] = 1 - L["passed"]
print("Φοιτητές:", len(L))
print("Πέρασαν:", int(L.passed.sum()), "| απέτυχαν στην εξέταση:", int(((L.no_show == 0) & (L.passed == 0)).sum()), "| δεν προσήλθαν:", int(L.no_show.sum()))
print("Βασικό ποσοστό (δεν πέρασαν):", round(L.not_passed.mean(), 3))
L.head()'''
TM_MD = '''## Από την ακολουθία στον πίνακα μεταβάσεων
Τα τρία βήματα του Μέρους 1: **Collate** (οι υποβολές κάθε άσκησης σε χρονολογική σειρά και τα διαδοχικά ζεύγη τους), **Aggregate** (καταμέτρηση των ζευγών), **Normalize** (κάθε γραμμή διαιρείται με το άθροισμά της).'''
TM = '''def transition_counts(sequences):
    """Μετρά τις μεταβάσεις EE, ES, SE, SS σε μια λίστα ακολουθιών (μία ακολουθία ανά άσκηση)."""
    c = dict(EE=0, ES=0, SE=0, SS=0)
    for q in sequences:
        for a, b in zip(q, q[1:]):
            c[a + b] += 1
    return c

def transition_matrix(c):
    e, s = c["EE"] + c["ES"], c["SE"] + c["SS"]
    return pd.DataFrame([[c["EE"] / e if e else np.nan, c["ES"] / e if e else np.nan],
                         [c["SE"] / s if s else np.nan, c["SS"] / s if s else np.nan]], index=["από E", "από S"], columns=["προς E", "προς S"]).round(2)

# Το παράδειγμα του Μέρους 1
c = transition_counts(["EESEEESSS"]); print(c); display(transition_matrix(c))

# Έλεγχος: το P(E→S) της εβδομάδας 4 υπολογίζεται ξανά από τις υποβολές και συγκρίνεται με τη στήλη p_ES_w1_4
s4 = submissions_last[(submissions_last.week <= 4) & (submissions_last.late == 0)]
def p_es(seqs, min_transitions=4):
    c = transition_counts(seqs); e = c["EE"] + c["ES"]
    return c["ES"] / e if e >= min_transitions else np.nan
recomputed = s4.groupby("student_id")["sequence"].apply(list).apply(p_es)
check = L.set_index("student_id")["p_ES_w1_4"]
print("Ίδιες τιμές με τη στήλη του πίνακα:", bool(np.allclose(recomputed.reindex(check.index).fillna(-1), check.fillna(-1), atol=1e-3)))'''
HELP = '''def pass_rate(df, col, edges, labels):
    """Ποσοστό επιτυχίας ανά ζώνη τιμών της στήλης col."""
    b = pd.cut(df[col], edges, labels=labels, include_lowest=True)
    return df.groupby(b, observed=True)["passed"].agg(ποσοστό="mean", n="size").round(2)

def bar(ax, t, title, color="#0D47A1"):
    ax.bar(t.index.astype(str), t["ποσοστό"], color=color); ax.set_ylim(0, 1); ax.set_title(title, fontsize=10)
    for i, v in enumerate(t["ποσοστό"]): ax.text(i, v + .02, f"{v:.0%}", ha="center", fontsize=9)'''
EX3 = '''fig, ax = plt.subplots(1, 3, figsize=(13, 3.4))
bar(ax[0], pass_rate(L, "logins_w1_4", [0, 8, 13, 999], ["0–8", "9–13", "14+"]), "Όλοι οι φοιτητές")
bar(ax[1], pass_rate(L[L.enrolment == "first"], "logins_w1_4", [0, 8, 999], ["0–8", "9+"]), "Πρώτη εγγραφή", "#F2A413")
bar(ax[2], pass_rate(L[L.enrolment == "repeat"], "logins_w1_4", [0, 8, 999], ["0–8", "9+"]), "Επανεγγραφή", "#8795AA")
plt.suptitle("Ποσοστό επιτυχίας ανά πλήθος συνδέσεων στο eclass, εβδομάδες 1 έως 4", y=1.04); plt.show()
L.groupby("enrolment").agg(φοιτητές=("passed", "size"), συνδέσεις=("logins_w1_4", "mean"), πέρασαν=("passed", "mean"), δεν_προσήλθαν=("no_show", "mean")).round(2)'''
EX4 = '''fig, ax = plt.subplots(1, 3, figsize=(13, 3.4))
bar(ax[0], pass_rate(L, "sheets_semester", [0, 3, 8, 12], ["0–3", "4–8", "9–12"]), "Φύλλα ασκήσεων, όλο το εξάμηνο")
bar(ax[1], pass_rate(L, "sheets_on_time_w1_4", [0, 1, 2, 3, 4], ["0–1", "2", "3", "4"]), "Φύλλα εμπρόθεσμα, εβδομάδες 1 έως 4", "#A9C8F0")
lw = L[L.no_show == 1]["last_active_week"].value_counts().reindex(range(1, 14), fill_value=0)
ax[2].bar(lw.index.astype(str), lw.values, color="#D8433B"); ax[2].set_title("Εβδομάδα τελευταίας δραστηριότητας όσων δεν προσήλθαν", fontsize=10); plt.show()
print("Στο τέλος της εβδομάδας 4 είχε αποχωρήσει το", f"{(L[L.no_show == 1].last_active_week <= 4).mean():.0%}", "όσων τελικά δεν προσήλθαν.")'''
EX5 = '''fig, ax = plt.subplots(1, 2, figsize=(10, 3.4))
bar(ax[0], pass_rate(L, "submissions_w1_4", [0, 15, 40, 80, 10**6], ["0–15", "16–40", "41–80", "81+"]), "Ανά πλήθος υποβολών", "#8795AA")
bar(ax[1], pass_rate(L, "p_ES_w1_4", [0, .2499, .3999, .5499, 1], ["<0,25", "0,25–0,40", "0,40–0,55", "≥0,55"]), "Ανά P(E→S)", "#2E9E5B"); plt.show()
L["outcome"] = np.where(L.passed == 1, "πέρασαν", np.where(L.no_show == 1, "δεν προσήλθαν", "απέτυχαν στην εξέταση"))
for name, g in L.groupby("outcome"):
    print(name, f"({len(g)} φοιτητές, διάμεσος υποβολών {g.submissions_w1_4.median():.0f})"); display(transition_matrix(g[["EE", "ES", "SE", "SS"]].sum().to_dict()))'''
RULE_MD = '''## Ο δικός σας κανόνας
Ένας κανόνας είναι μια συνάρτηση που δέχεται τον πίνακα των φοιτητών και επιστρέφει `True` για όσους επισημαίνονται. Χρησιμοποιήστε **μόνο στήλες που υπάρχουν στο τέλος της εβδομάδας 4**. Οι φοιτητές με ανεπαρκή δεδομένα έχουν κενό `p_ES_w1_4`: αποφασίστε ρητά τι κάνετε με αυτούς.'''
RULE = '''def evaluate(rule, df):
    f = rule(df).fillna(False).astype(bool); y = (df["passed"] == 0)
    tp, fp, fn, tn = (f & y).sum(), (f & ~y).sum(), (~f & y).sum(), (~f & ~y).sum()
    return pd.Series({"επισημαίνονται": f.mean(), "από όσους δεν πέρασαν, επισημαίνονται": tp / max(tp + fn, 1), "από όσους επισημαίνονται, δεν πέρασαν": tp / max(tp + fp, 1), "ορθή κατάταξη": (tp + tn) / len(df)}).round(2)

rules = {
    "συνδέσεις ≤ 8":                 lambda d: d.logins_w1_4 <= 8,
    "υποβολές ≤ 15":                 lambda d: d.submissions_w1_4 <= 15,
    "P(E→S) < 0,35":                 lambda d: d.p_ES_w1_4 < .35,
    "φύλλα εμπρόθεσμα ≤ 2":          lambda d: d.sheets_on_time_w1_4 <= 2,
    "P(E→S) < 0,35 ή φύλλα ≤ 2":     lambda d: (d.p_ES_w1_4 < .35) | (d.sheets_on_time_w1_4 <= 2),
    "μόνο το μητρώο: επανεγγραφή":   lambda d: d.enrolment == "repeat",
    "επισήμανση όλων":                  lambda d: pd.Series(True, index=d.index),
}
display(pd.DataFrame({k: evaluate(r, L) for k, r in rules.items()}).T)

# Ο ίδιος κανόνας ανά ομάδα φοιτητών
my_rule = rules["P(E→S) < 0,35 ή φύλλα ≤ 2"]      # αλλάξτε τον
display(pd.DataFrame({("εργάζονται" if w else "δεν εργάζονται"): evaluate(my_rule, g) for w, g in L.groupby("works")}).T)'''
THIS = '''# Η φετινή κοόρτη στο τέλος της εβδομάδας 4: ποιους θα ειδοποιούσε ο κανόνας σας;
T = students_this.copy(); flagged = my_rule(T).fillna(False)
print("Επισημαίνονται", int(flagged.sum()), "από", len(T), f"({flagged.mean():.0%})")
print(T.assign(flagged=flagged).groupby(["enrolment", "works"])["flagged"].agg(["mean", "size"]).round(2))
print("Ανεπαρκή δεδομένα για το P(E→S):", int(T.p_ES_w1_4.isna().sum()), "φοιτητές")'''
MORE = '''## Για περαιτέρω σκέψη
1. Εκπαιδεύστε μια λογιστική παλινδρόμηση με τις συνδέσεις, μία φορά χωρίς και μία φορά με την κατάσταση εγγραφής. Τι συμβαίνει στον συντελεστή των συνδέσεων;
2. Αλλάξτε το κατώφλι του P(E→S). Πώς μετακινούνται μαζί το «πόσους εντοπίζω» και το «πόσες επισημάνσεις επιβεβαιώνονται»; Το ερώτημα αυτό είναι το θέμα της Εβδομάδας 3.
3. Δοκιμάστε τρεις χειρισμούς των ανεπαρκών δεδομένων: «δεν επισημαίνεται», «επισημαίνεται», «ξεχωριστή κατηγορία». Ποιον αδικεί ο καθένας;
4. Υπολογίστε έναν κανόνα από το σύνολο του εξαμήνου (π.χ. `sheets_semester`). Γιατί δεν μπορεί να χρησιμοποιηθεί την εβδομάδα 4, όσο καλός κι αν φαίνεται;'''
def build(teacher):
    files = [('students_last', f'{D}/students_last.csv'), ('students_this', f'{D}/students_this_week4.csv'), ('submissions_last', f'{D}/submissions_last.csv'), ('submissions_this', f'{D}/submissions_this_week4.csv'), ('logins_last', f'{D}/logins_last.csv')]
    if teacher: files += [('last_full', f'{D}/teacher/students_last_full.csv'), ('this_full', f'{D}/teacher/students_this_full.csv')]
    cells = [md(INTRO + ('\n\n**Έκδοση διδάσκοντος: περιέχει τις εκβάσεις της φετινής κοόρτης και τα λανθάνοντα χαρακτηριστικά. Δεν διανέμεται.**' if teacher else '')), code(loader(files)), md(DICT), code(LOOK), md(TM_MD), code(TM), md('## Βοηθητικές συναρτήσεις'), code(HELP),
             md('## Τεκμήριο 3: συνδέσεις στο eclass'), code(EX3), md('## Τεκμήριο 4: φύλλα εργαστηριακών ασκήσεων'), code(EX4), md('## Τεκμήριο 5: πλήθος και αλληλουχία υποβολών'), code(EX5), md(RULE_MD), code(RULE), md('## Η φετινή κοόρτη'), code(THIS)]
    if teacher:
        cells += [md('## Μόνο για τον διδάσκοντα: ο κανόνας στη φετινή κοόρτη, με τις εκβάσεις'),
                  code('TF = this_full.copy()\ndisplay(pd.DataFrame({k: evaluate(r, TF) for k, r in rules.items()}).T)'),
                  md('## Μόνο για τον διδάσκοντα: τι μετρά κάθε ίχνος\nΣυσχέτιση κάθε ίχνους με τα δύο λανθάνοντα χαρακτηριστικά της διαδικασίας (περσινή κοόρτη). Ο πρώτος πίνακας αφορά όλους τους φοιτητές: εκεί οι συνδέσεις συσχετίζονται με τη δέσμευση μόνο μέσω της κατάστασης εγγραφής. Ο δεύτερος αφορά μόνο την πρώτη εγγραφή, όπου η συσχέτιση αυτή εξαφανίζεται.'),
                  code('LF = last_full.copy(); LF["repeat"] = (LF.enrolment == "repeat").astype(int)\ncols = ["logins_w1_4", "submissions_w1_4", "p_ES_w1_4", "sheets_on_time_w1_4", "sheets_semester", "midterm"]\ndisplay(LF[cols + ["skill", "commitment", "repeat", "works"]].corr().loc[cols, ["skill", "commitment", "repeat", "works"]].round(2))\nF1 = LF[LF.repeat == 0]\ndisplay(F1[cols + ["skill", "commitment", "works"]].corr().loc[cols, ["skill", "commitment", "works"]].round(2))')]
    else: cells.append(md(MORE))
    nb = nbf.v4.new_notebook(cells=cells, metadata={'kernelspec': {'display_name': 'Python 3', 'language': 'python', 'name': 'python3'}, 'language_info': {'name': 'python'}, 'colab': {'provenance': []}})
    out = f'{HERE}/Lab1_notebook_{"teacher" if teacher else "student"}.ipynb'; nbf.write(nb, out); return out
for t in (False, True):
    p = build(t); print(os.path.basename(p), round(os.path.getsize(p) / 1024), 'kB')
