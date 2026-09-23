"""Week 3, Part 1: every number that Part 1 borrows from the Lab 1 case, computed once from the two LOCKED cohorts -> lab1_numbers.json (the file must NOT be called numbers.py: that name shadows a Python standard module)
Nothing is simulated again here: the cohorts are the ones the students worked with in Week 2 (lab1/cohort_*_full.csv)."""
import pandas as pd, numpy as np, json, os
HERE = os.path.dirname(os.path.abspath(__file__)); LAB = os.path.join(HERE, '..', 'lab1')
def load(nm):
    A = pd.read_csv(f'{LAB}/cohort_{nm}_full.csv'); A['np_'] = 1 - A.passed; A['insuf'] = A.pES_w4.isna().astype(int); return A
def perf(A, f):
    f = f.astype(bool); tp = int((f & (A.np_ == 1)).sum()); fp = int((f & (A.np_ == 0)).sum()); fn = int((~f & (A.np_ == 1)).sum()); tn = len(A) - tp - fp - fn
    return dict(n=int(len(A)), flagged=int(f.sum()), tp=tp, fp=fp, fn=fn, tn=tn, precision=tp / max(tp + fp, 1), recall=tp / max(tp + fn, 1), acc=(tp + tn) / len(A),
                fpr=fp / max(fp + tn, 1), fnr=fn / max(fn + tp, 1))
T = load('this'); L = load('last'); out = {}
comb = lambda A: (A.pES_w4 < .35) | (A.labs_w4 <= 2)
out['combined_this'] = perf(T, comb(T)); out['combined_last'] = perf(L, comb(L))
out['sweep_pES_this'] = {f'{c:.2f}': perf(T, T.pES_w4 < c) for c in (.25, .35, .45, .55)}
out['by_work_this'] = {('working' if k == 1 else 'others'): perf(g, comb(g)) for k, g in T.groupby('work')}
out['by_work_last'] = {('working' if k == 1 else 'others'): perf(g, comb(g)) for k, g in L.groupby('work')}
# capacity: the k students with the lowest P(E->S); students without a value cannot be ranked at all
for k in (40, 60, 80):
    r = T.pES_w4.rank(method='first'); sel = (r <= k) & T.pES_w4.notna(); p = perf(T, sel)
    p['working_share_selected'] = float(T[sel].work.mean()); p['working_share_cohort'] = float(T.work.mean()); out[f'top{k}_pES_this'] = p
out['unranked_this'] = dict(n=int(T.insuf.sum()), share=float(T.insuf.mean()), not_passed=int(T[T.insuf == 1].np_.sum()),
                            working_share=float(T[T.insuf == 1].work.mean()), insuf_among_working=float(T[T.work == 1].insuf.mean()), insuf_among_others=float(T[T.work == 0].insuf.mean()))
json.dump(out, open(os.path.join(HERE, 'lab1_numbers.json'), 'w'), indent=1)
for k, v in out.items(): print(k, {a: (round(b, 3) if isinstance(b, float) else b) for a, b in v.items()} if 'n' in v or 'share' in v else {kk: {a: (round(b, 3) if isinstance(b, float) else b) for a, b in vv.items()} for kk, vv in v.items()})
