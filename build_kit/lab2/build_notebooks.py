"""Optional after-class notebooks for Lab 2 -> Lab2_notebook_student.ipynb, Lab2_notebook_teacher.ipynb (Greek text, Python code).
python3 build_notebooks.py          builds both and TEST-RUNS every code cell against the local CSV (env LAB2_DATA), comparing with numbers.json."""
import json, os, subprocess, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__)); N = json.load(open(f'{HERE}/numbers.json', encoding='utf8'))
URL = 'https://archive.ics.uci.edu/static/public/697/predict+students+dropout+and+academic+success.zip'
md = lambda t: {'cell_type': 'markdown', 'metadata': {}, 'source': t.strip('\n').splitlines(keepends=True)}
code = lambda t: {'cell_type': 'code', 'metadata': {}, 'execution_count': None, 'outputs': [], 'source': t.strip('\n').splitlines(keepends=True)}
C_LOAD = f'''
import os, numpy as np, pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score

URL = "{URL}"
src = os.environ.get("LAB2_DATA", URL)            # στο Colab διαβάζεται απευθείας από το UCI
D = pd.read_csv(src, sep=";", compression="zip" if src.endswith(".zip") else None)
D.columns = [c.strip() for c in D.columns]
D["y"] = (D["Target"] == "Dropout").astype(int)     # 1 = εγκατέλειψε, 0 = όλοι οι άλλοι
print(D.shape, D["Target"].value_counts().to_dict())
'''
C_MODEL = '''
CATS = ["Marital status", "Application mode", "Course", "Previous qualification", "Nacionality",
        "Mother's qualification", "Father's qualification", "Mother's occupation", "Father's occupation"]
s1 = [c for c in D.columns if "1st sem" in c]; s2 = [c for c in D.columns if "2nd sem" in c]
enrol = [c for c in D.columns if c not in s1 + s2 + ["Target", "y"]]
MOMENTS = {"κατά την εγγραφή": enrol, "τέλος 1ου εξαμήνου": enrol + s1, "τέλος 2ου εξαμήνου": enrol + s1 + s2}
tr, te = train_test_split(D.index, test_size=0.2, random_state=697, stratify=D["y"])   # 80% / 20%, όπως συνιστούν οι δημιουργοί

def fit(cols):
    X = pd.get_dummies(D[cols].astype({c: "category" for c in cols if c in CATS}), drop_first=True).astype(float)
    m = make_pipeline(StandardScaler(), LogisticRegression(max_iter=3000, C=0.3)).fit(X.loc[tr], D["y"].loc[tr])
    return m, X, pd.Series(m.predict_proba(X.loc[te])[:, 1], index=te)

rows = []
for name, cols in MOMENTS.items():
    m, X, p = fit(cols)
    rows.append({"στιγμή": name, "μεταβλητές": len(cols), "AUC": round(roc_auc_score(D["y"].loc[te], p), 3), "ορθή κατάταξη": round(((p >= 0.5) == D["y"].loc[te]).mean(), 3)})
pd.DataFrame(rows)
'''
C_SWEEP = '''
model, X1, risk = fit(MOMENTS["τέλος 1ου εξαμήνου"])
T = D.loc[te].assign(risk=risk)                      # οι 885 φοιτητές ελέγχου

def perf(G, flag):
    tp = int((flag & (G.y == 1)).sum()); fp = int((flag & (G.y == 0)).sum()); fn = int((~flag & (G.y == 1)).sum()); tn = len(G) - tp - fp - fn
    return {"φοιτητές": len(G), "εγκατέλειψαν": round(G.y.mean(), 2), "επισημαίνονται": int(flag.sum()), "ορθά": tp, "χωρίς λόγο": fp, "διαφεύγουν": fn,
            "ευστοχία": round(tp / max(tp + fp, 1), 2), "ανάκληση": round(tp / max(tp + fn, 1), 2),
            "ψευδώς θετικοί %": round(100 * fp / max(fp + tn, 1)), "ψευδώς αρνητικοί %": round(100 * fn / max(fn + tp, 1))}

def sweep(thresholds=(0.2, 0.3, 0.4, 0.5, 0.6, 0.7)):
    return pd.DataFrame({t: perf(T, T.risk >= t) for t in thresholds}).T

sweep()
'''
C_TOPK = '''
a1 = "Curricular units 1st sem (approved)"
rank = T.risk.rank(ascending=False, method="first")
for k in (50, 100):
    top = T[rank <= k]
    print(f"οι {k} πρώτοι: εγκατέλειψαν {int(top.y.sum())}, χωρίς κανένα επιτυχές μάθημα {int((top[a1] == 0).sum())}")
nz = T[T[a1] > 0]
print("με ένα τουλάχιστον επιτυχές μάθημα:", perf(nz, nz.risk >= 0.4))
'''
C_GROUP = '''
def by_group(col, threshold=0.4):
    return pd.DataFrame({val: perf(G, G.risk >= threshold) for val, G in T.groupby(col)}).T

T["ηλικιακή ομάδα"] = pd.cut(T["Age at enrollment"], [0, 20, 25, 99], labels=["έως 20", "21 έως 25", "26 και άνω"]).astype(str)
for col in ["Gender", "Scholarship holder", "Tuition fees up to date", "ηλικιακή ομάδα"]:     # Gender: 1 = άνδρας, 0 = γυναίκα
    print("\\n", col); print(by_group(col)[["φοιτητές", "εγκατέλειψαν", "επισημαίνονται", "ψευδώς θετικοί %", "ψευδώς αρνητικοί %"]])
'''
C_W = '''
w = pd.Series(model[-1].coef_[0], index=X1.columns)
w.reindex(w.abs().sort_values(ascending=False).index).head(10).round(2)
'''
C_TRY = '''
# Δοκιμάστε: αλλάξτε το κατώφλι, ή ελέγξτε άλλη υποομάδα (π.χ. "Debtor", "Displaced", "Daytime/evening attendance", "Marital status")
by_group("Debtor", threshold=0.3)
'''
C_EX = '''
# Άσκηση: το ίδιο μοντέλο ΧΩΡΙΣ τα κοινωνικοοικονομικά στοιχεία. Τι αλλάζει στην ακρίβεια; Τι αλλάζει για όσους καθυστερούν τα δίδακτρα;
SOCIO = ["Debtor", "Tuition fees up to date", "Scholarship holder", "Mother's occupation", "Father's occupation", "Mother's qualification", "Father's qualification"]
cols2 = [c for c in MOMENTS["τέλος 1ου εξαμήνου"] if c not in SOCIO]
m2, X2, risk2 = fit(cols2)
T2 = D.loc[te].assign(risk=risk2)
print("AUC με όλα:", round(roc_auc_score(T.y, T.risk), 3), "| AUC χωρίς τα κοινωνικοοικονομικά:", round(roc_auc_score(T2.y, T2.risk), 3))
for name, TT in (("με όλα", T), ("χωρίς", T2)):
    late = TT[TT["Tuition fees up to date"] == 0]; r = perf(late, late.risk >= 0.4)
    print(name, "· δίδακτρα σε καθυστέρηση: επισημαίνονται", r["επισημαίνονται"], "από", r["φοιτητές"], "· ψευδώς θετικοί", r["ψευδώς θετικοί %"], "% · ψευδώς αρνητικοί", r["ψευδώς αρνητικοί %"], "%")
'''
def build(teacher, ex=None):
    c = [md('# Εργαστήριο 2: ποιοι φοιτητές θα λάβουν τι;\n**Προαιρετικό τετράδιο, για μετά το μάθημα.** ' + ('Έκδοση διδάσκοντος, με σχολιασμό.' if teacher else 'Αναπαράγει τα τεκμήρια του πακέτου και σας αφήνει να δοκιμάσετε άλλες επιλογές.') +
               '\n\nΔεδομένα: Realinho, Machado, Baptista & Martins (2022), *Data*, 7(11), 146· UCI Machine Learning Repository, σύνολο δεδομένων 697· άδεια CC BY 4.0. Πραγματικά, ανωνυμοποιημένα δεδομένα 4.424 φοιτητών.'),
         md('## 1. Τα δεδομένα\nΤο αρχείο διαβάζεται απευθείας από το UCI. Η έκβαση έχει τρεις τιμές· εδώ προβλέπουμε το «εγκατέλειψε» έναντι όλων των άλλων.'), code(C_LOAD),
         md('## 2. Το ίδιο μοντέλο σε τρεις στιγμές (Τεκμήριο 1)'), code(C_MODEL)]
    if teacher: c.append(md(f'> **Σχολιασμός.** Αναμένονται AUC {N["moments"]["enrol"]["auc"]:.2f}, {N["moments"]["sem1"]["auc"]:.2f} και {N["moments"]["sem2"]["auc"]:.2f}. Το κέρδος ενός εξαμήνου αναμονής είναι μεγάλο· το κέρδος του δεύτερου εξαμήνου μικρό. Ο σπόρος 697 και το C = 0,3 δίνουν ακριβώς τους αριθμούς του πακέτου.'))
    c += [md('## 3. Το κατώφλι (Τεκμήριο 2)'), code(C_SWEEP)]
    if teacher: c.append(md(f'> **Σχολιασμός.** {N["test"]["n"]} φοιτητές ελέγχου, {N["test"]["dropouts"]} εγκατέλειψαν. Στο 0,4: {N["sweep"]["0.4"]["flagged"]} επισημάνσεις, {N["sweep"]["0.4"]["fp"]} χωρίς λόγο, {N["sweep"]["0.4"]["fn"]} διαφεύγουν. Ζητήστε από τους φοιτητές να δικαιολογήσουν το κατώφλι με την ενέργεια, όχι με την «ισορροπία» ευστοχίας και ανάκλησης.'))
    c += [md('## 4. Η δυναμικότητα: ποιοι βρίσκονται στην κορυφή της λίστας (Τεκμήριο 3)'), code(C_TOPK)]
    if teacher: c.append(md(f'> **Σχολιασμός.** Από τους 100 πρώτους εγκατέλειψαν οι {N["topk"]["100"]["tp"]}, και οι {N["topk"]["100"]["zero_approved"]} δεν είχαν περάσει κανένα μάθημα. Η κορυφή της λίστας είναι εκεί όπου το μοντέλο προσθέτει τα λιγότερα.'))
    c += [md('## 5. Οι υποομάδες (Τεκμήριο 4)\n`Gender`: 1 = άνδρας, 0 = γυναίκα. Στις υπόλοιπες μεταβλητές ναι/όχι: 1 = ναι.'), code(C_GROUP)]
    if teacher: c.append(md('> **Σχολιασμός.** Τα βασικά ποσοστά εγκατάλειψης διαφέρουν πολύ μεταξύ των ομάδων. Η ανισότητα των σφαλμάτων δεν οφείλεται στη μέτρηση, όπως στο Εργαστήριο 1, και δεν διορθώνεται: επιλέγεται. Ομάδες κάτω των 50 ατόμων δεν κρίνονται.'))
    c += [md('## 6. Τι βαραίνει στο μοντέλο (Τεκμήριο 5)\nΤυποποιημένοι συντελεστές: συγκρίνονται μεταξύ τους, δεν ερμηνεύονται αιτιακά.'), code(C_W), md('## 7. Δοκιμάστε'), code(C_TRY), md('## 8. Άσκηση: ελαχιστοποίηση δεδομένων\nΑφαιρέστε τα κοινωνικοοικονομικά στοιχεία και εκπαιδεύστε ξανά. Πριν τρέξετε το κελί, γράψτε τι περιμένετε.'), code(C_EX)]
    if teacher and ex: c.append(md(f'> **Σχολιασμός.** Η AUC πέφτει από {ex["auc_full"]:.3f} σε {ex["auc_red"]:.3f}. Για όσους καθυστερούν τα δίδακτρα, οι ψευδώς θετικοί πέφτουν από {ex["fpr_full"]}% σε {ex["fpr_red"]}% και οι ψευδώς αρνητικοί ανεβαίνουν από {ex["fnr_full"]}% σε {ex["fnr_red"]}%. Η ελαχιστοποίηση έχει τίμημα σε ακρίβεια και αλλάζει το ποιος αδικείται· δεν εξαφανίζει την αδικία. Αυτό είναι το σημείο της άσκησης.'))
    return {'cells': c, 'metadata': {'kernelspec': {'display_name': 'Python 3', 'language': 'python', 'name': 'python3'}, 'language_info': {'name': 'python'}}, 'nbformat': 4, 'nbformat_minor': 5}
def run(nb):
    src = '\n'.join(''.join(c['source']) for c in nb['cells'] if c['cell_type'] == 'code')
    src = src.replace('\nsweep()\n', '\nprint(sweep())\n').replace('w.reindex(w.abs().sort_values(ascending=False).index).head(10).round(2)', 'print(w.reindex(w.abs().sort_values(ascending=False).index).head(10).round(2))').replace('\npd.DataFrame(rows)', '\nprint(pd.DataFrame(rows))').replace('\nby_group("Debtor", threshold=0.3)', '\nprint(by_group("Debtor", threshold=0.3))')
    src += '\nimport json; late=T[T["Tuition fees up to date"]==0]; late2=T2[T2["Tuition fees up to date"]==0]; a=perf(late, late.risk>=0.4); b=perf(late2, late2.risk>=0.4)\nprint("@@"+json.dumps(dict(auc_full=float(roc_auc_score(T.y,T.risk)), auc_red=float(roc_auc_score(T2.y,T2.risk)), fpr_full=a["ψευδώς θετικοί %"], fpr_red=b["ψευδώς θετικοί %"], fnr_full=a["ψευδώς αρνητικοί %"], fnr_red=b["ψευδώς αρνητικοί %"], flagged04=int((T.risk>=0.4).sum()), top100=int(T[T.risk.rank(ascending=False, method="first")<=100].y.sum()))))'
    f = tempfile.NamedTemporaryFile('w', suffix='.py', delete=False, encoding='utf8'); f.write(src); f.close()
    r = subprocess.run([sys.executable, '-W', 'ignore', f.name], capture_output=True, text=True, env=dict(os.environ, LAB2_DATA=f'{HERE}/data/students_dropout_uci697.csv'))
    assert r.returncode == 0, r.stderr[-1500:]
    return json.loads([l for l in r.stdout.splitlines() if l.startswith('@@')][0][2:]), r.stdout
ex, out = run(build(False)); assert ex['flagged04'] == N['sweep']['0.4']['flagged'] and ex['top100'] == N['topk']['100']['tp'], ex
for teacher, name in ((False, 'Lab2_notebook_student.ipynb'), (True, 'Lab2_notebook_teacher.ipynb')):
    nb = build(teacher, ex); json.dump(nb, open(f'{HERE}/{name}', 'w', encoding='utf8'), ensure_ascii=False, indent=1); print(name, len(nb['cells']), 'cells')
ex2, _ = run(build(True, ex)); print('test run ok; notebook numbers = numbers.json:', ex2['flagged04'] == N['sweep']['0.4']['flagged'], '| exercise:', ex)
