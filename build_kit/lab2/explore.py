"""Lab 2 feasibility (outline stage): real data, UCI 697. Prints what the lab exhibits could show. Nothing here goes on a slide before the design is approved."""
import pandas as pd, numpy as np, warnings; warnings.filterwarnings('ignore')
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score
D = pd.read_csv('raw/data.csv', sep=';'); D.columns = [c.strip() for c in D.columns]
print('shape', D.shape, '| missing', int(D.isna().sum().sum())); print('target', D.Target.value_counts().to_dict())
print('columns:', list(D.columns))
D['y'] = (D.Target == 'Dropout').astype(int)
s1 = [c for c in D.columns if '1st sem' in c]; s2 = [c for c in D.columns if '2nd sem' in c]; macro = ['Unemployment rate', 'Inflation rate', 'GDP']
enrol = [c for c in D.columns if c not in s1 + s2 + ['Target', 'y']]
tr, te = train_test_split(D, test_size=.2, random_state=697, stratify=D.y)
def fit(cols):
    X = pd.get_dummies(D[cols].astype({c: 'category' for c in cols if c in ('Marital status', 'Application mode', 'Course', 'Previous qualification', 'Nacionality', "Mother's qualification", "Father's qualification", "Mother's occupation", "Father's occupation")}), drop_first=True).astype(float)
    m = make_pipeline(StandardScaler(), LogisticRegression(max_iter=3000, C=.3)).fit(X.loc[tr.index], tr.y); p = pd.Series(m.predict_proba(X.loc[te.index])[:, 1], index=te.index); return m, p, X
for name, cols in (('at enrolment', enrol), ('after semester 1', enrol + s1), ('after semester 2', enrol + s1 + s2)):
    m, p, X = fit(cols); print(f'{name:<17} features {len(cols):>2} | AUC {roc_auc_score(te.y, p):.3f} | acc@0.5 {((p >= .5) == te.y).mean():.3f}')
    if name == 'after semester 1': P = p
T = te.assign(p=P); n = len(T); pos = int(T.y.sum()); print('test n', n, '| dropouts', pos, f'({pos / n:.1%})')
def perf(G, f):
    tp = int((f & (G.y == 1)).sum()); fp = int((f & (G.y == 0)).sum()); fn = int((~f & (G.y == 1)).sum()); tn = len(G) - tp - fp - fn
    return dict(n=len(G), base=round(G.y.mean(), 3), flag=int(f.sum()), tp=tp, fp=fp, fn=fn, prec=round(tp / max(tp + fp, 1), 2), rec=round(tp / max(tp + fn, 1), 2), fpr=round(fp / max(fp + tn, 1), 2), fnr=round(fn / max(fn + tp, 1), 2))
print('threshold sweep (model after semester 1, test set)')
for c in (.2, .3, .4, .5, .6, .7): print(' ', c, perf(T, T.p >= c))
for k in (50, 100): print('  top', k, perf(T, T.p.rank(ascending=False, method='first') <= k))
T['age_grp'] = pd.cut(T['Age at enrollment'], [0, 20, 25, 99], labels=['<=20', '21-25', '26+'])
print('subgroups at threshold 0.4')
for col in ['Gender', 'Scholarship holder', 'Debtor', 'Tuition fees up to date', 'Displaced', 'International', 'Daytime/evening attendance', 'Educational special needs', 'age_grp']:
    for v, G in T.groupby(col):
        r = perf(G, G.p >= .4); print(f'  {col[:24]:<24} {str(v):<6}', {k: r[k] for k in ('n', 'base', 'flag', 'prec', 'fpr', 'fnr')})

# ---- who is at the top of the list, what drives the model, and the zero rows (added for the outline)
top = T[T.p.rank(ascending=False, method='first') <= 100]; a1 = 'Curricular units 1st sem (approved)'; e1 = 'Curricular units 1st sem (enrolled)'
print('top 100: zero approved units in sem 1:', int((top[a1] == 0).sum()), '| dropouts', int(top.y.sum()), '| whole test set with zero approved:', int((T[a1] == 0).sum()), 'of whom dropouts', int(T[T[a1] == 0].y.sum()))
z = D[D[e1] == 0]; print('rows with zero ENROLLED units in sem 1:', len(z), z.Target.value_counts().to_dict())
m, p, X = fit(enrol + s1); co = pd.Series(m[-1].coef_[0], index=X.columns); grp = co.groupby(lambda c: c.split('_')[0] if c.split('_')[0] in ('Course', 'Application mode', "Mother's occupation", "Father's occupation", "Mother's qualification", "Father's qualification", 'Nacionality', 'Marital status', 'Previous qualification') else c).apply(lambda v: v.abs().max())
print('largest standardised coefficients:'); print(co.reindex(co.abs().sort_values(ascending=False).index).head(10).round(2).to_string())
nz = T[T[a1] > 0]; print('students WITH at least one approved unit: n', len(nz), '| dropouts', int(nz.y.sum()), '| flagged at 0.4', int((nz.p >= .4).sum()), '| recall', round(((nz.p >= .4) & (nz.y == 1)).sum() / max(nz.y.sum(), 1), 2))
