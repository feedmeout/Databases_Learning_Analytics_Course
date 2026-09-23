"""Lab 2: every number shown anywhere (deck, pack, key, notebooks) is computed here ONCE from the real file -> numbers.json, and exported for students -> data/."""
import json, os, numpy as np, pandas as pd, warnings; warnings.filterwarnings('ignore')
from sklearn.metrics import roc_auc_score
from model import load, columns, split, fit, HERE
D = load(); C = columns(D); tr, te = split(D); out = {}
out['data'] = dict(n=int(len(D)), n_features=int(D.shape[1] - 2), missing=int(D.drop(columns='y').isna().sum().sum()), classes={k: int(v) for k, v in D.Target.value_counts().items()}, n_courses=int(D.Course.nunique()),
                   zero_enrolled=dict(n=int((D['Curricular units 1st sem (enrolled)'] == 0).sum()), **{k: int(v) for k, v in D[D['Curricular units 1st sem (enrolled)'] == 0].Target.value_counts().items()}))
P = {}
for k in ('enrol', 'sem1', 'sem2'):
    m, X = fit(D, C[k], tr); p = pd.Series(m.predict_proba(X.loc[te])[:, 1], index=te); P[k] = p
    out.setdefault('moments', {})[k] = dict(n_features=len(C[k]), auc=float(roc_auc_score(D.y.loc[te], p)), acc=float(((p >= .5) == D.y.loc[te]).mean()))
    if k == 'sem1': M1, X1 = m, X
T = D.loc[te].assign(p=P['sem1']); out['test'] = dict(n=int(len(T)), dropouts=int(T.y.sum()), train_n=int(len(tr)))
def perf(G, f):
    f = f.astype(bool); tp = int((f & (G.y == 1)).sum()); fp = int((f & (G.y == 0)).sum()); fn = int((~f & (G.y == 1)).sum()); tn = int(len(G) - tp - fp - fn)
    return dict(n=int(len(G)), pos=int(G.y.sum()), base=float(G.y.mean()), flagged=int(f.sum()), flagged_p=float(f.mean()), tp=tp, fp=fp, fn=fn, tn=tn, precision=tp / max(tp + fp, 1), recall=tp / max(tp + fn, 1), fpr=fp / max(fp + tn, 1), fnr=fn / max(fn + tp, 1))
out['sweep'] = {f'{c:.1f}': perf(T, T.p >= c) for c in (.2, .3, .4, .5, .6, .7)}
a1 = 'Curricular units 1st sem (approved)'; rk = T.p.rank(ascending=False, method='first')
out['topk'] = {str(k): dict(**perf(T, rk <= k), zero_approved=int((T[rk <= k][a1] == 0).sum())) for k in (50, 100)}
out['zero_approved_test'] = dict(n=int((T[a1] == 0).sum()), dropouts=int(T[T[a1] == 0].y.sum())); nz = T[T[a1] > 0]; out['nonzero_approved_test'] = perf(nz, nz.p >= .4)
T['age_grp'] = pd.cut(T['Age at enrollment'], [0, 20, 25, 99], labels=['έως 20', '21 έως 25', '26 και άνω']).astype(str)
GROUPS = [('Gender', {0: 'γυναίκες', 1: 'άνδρες'}), ('Scholarship holder', {0: 'χωρίς υποτροφία', 1: 'υπότροφοι'}), ('Tuition fees up to date', {1: 'δίδακτρα εξοφλημένα', 0: 'δίδακτρα σε καθυστέρηση'}), ('Debtor', {0: 'χωρίς οφειλές', 1: 'με οφειλές'}),
          ('age_grp', {'έως 20': 'έως 20 ετών', '21 έως 25': '21 έως 25 ετών', '26 και άνω': '26 ετών και άνω'}), ('Displaced', {0: 'μόνιμοι κάτοικοι', 1: 'εκτός τόπου κατοικίας'}), ('International', {0: 'ημεδαποί', 1: 'διεθνείς φοιτητές'}), ('Educational special needs', {0: 'χωρίς ειδικές ανάγκες', 1: 'με ειδικές εκπαιδευτικές ανάγκες'})]
out['groups'] = {col: {lab: perf(T[T[col] == val], T[T[col] == val].p >= .4) for val, lab in labs.items()} for col, labs in GROUPS}
co = pd.Series(M1[-1].coef_[0], index=X1.columns); top = co.reindex(co.abs().sort_values(ascending=False).index).head(10); out['weights'] = [dict(var=k, w=float(v)) for k, v in top.items()]
json.dump(out, open(f'{HERE}/numbers.json', 'w', encoding='utf8'), ensure_ascii=False, indent=1)
os.makedirs(f'{HERE}/data', exist_ok=True); D.drop(columns='y').to_csv(f'{HERE}/data/students_dropout_uci697.csv', index=False, sep=';')
T[['p', 'y', 'Target', 'Gender', 'Scholarship holder', 'Tuition fees up to date', 'Debtor', 'Age at enrollment', 'Displaced', 'International', 'Educational special needs', a1]].rename(columns={'p': 'risk', 'y': 'dropout'}).round({'risk': 4}).to_csv(f'{HERE}/data/test_set_with_risk.csv', index=False, sep=';')
g = out['groups']; s = out['sweep']
print('data', out['data']); print('moments', {k: (round(v['auc'], 3), round(v['acc'], 3)) for k, v in out['moments'].items()}); print('test', out['test'])
print('sweep', {k: (v['flagged'], v['tp'], v['fp'], v['fn'], round(v['precision'], 2), round(v['recall'], 2)) for k, v in s.items()})
print('topk', {k: (v['tp'], v['zero_approved']) for k, v in out['topk'].items()}, '| nonzero', {k: out['nonzero_approved_test'][k] for k in ('n', 'pos', 'flagged', 'recall')})
for col in g:
    print(' ', col, {lab: (r['n'], round(r['base'], 2), round(r['flagged_p'], 2), round(r['fpr'], 2), round(r['fnr'], 2)) for lab, r in g[col].items()})
print('weights', [(w['var'], round(w['w'], 2)) for w in out['weights']])
