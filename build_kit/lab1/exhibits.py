"""All numbers shown in the Lab 1 deck, pack and key, computed once from the two locked cohorts -> exhibits.json"""
import pandas as pd, numpy as np, json, itertools, os
HERE = os.path.dirname(os.path.abspath(__file__))
def auc(x, y):
    d = pd.DataFrame({'x': x, 'y': y}).dropna(); pos = d.x[d.y == 1].values; neg = d.x[d.y == 0].values
    return float(sum((p > neg).sum() + .5*(p == neg).sum() for p in pos) / (len(pos)*len(neg)))
def load(nm):
    A = pd.read_csv(f'{HERE}/cohort_{nm}_full.csv'); A['np_'] = 1 - A.passed; A['fail'] = ((A.noshow == 0) & (A.passed == 0)).astype(int)
    A['insuf'] = A.pES_w4.isna().astype(int); return A
RULES = {  # pre-set cut-offs printed in the pack
 'R1': ('Συνδέσεις στο eclass, εβδ. 1–4', '≤ 8', lambda A: A.logins_w4 <= 8),
 'R2': ('Πλήθος υποβολών κώδικα, εβδ. 1–4', '≤ 15', lambda A: A.nsub_w4 <= 15),
 'R3': ('P(E→S), εβδ. 1–4', '< 0,35', lambda A: A.pES_w4 < .35),
 'R4': ('Φύλλα ασκήσεων εμπρόθεσμα, εβδ. 1–4', '≤ 2 από 4', lambda A: A.labs_w4 <= 2),
 'R5': ('Φύλλα ασκήσεων, όλο το εξάμηνο', '≤ 6 από 12', lambda A: A.labs_sem <= 6),
 'R6': ('Βαθμός προόδου (εβδ. 8)', '< 5 ή απουσία', lambda A: (A.midterm < 5) | A.midterm.isna()),
}
def perf(A, f):
    f = f.astype(bool); n = len(A); tp = int((f & (A.np_ == 1)).sum()); fp = int((f & (A.np_ == 0)).sum()); fn = int((~f & (A.np_ == 1)).sum()); tn = n - tp - fp - fn
    return dict(n=n, flagged=int(f.sum()), flagged_p=f.mean(), tp=tp, fp=fp, fn=fn, tn=tn, recall=tp/max(tp+fn, 1), precision=tp/max(tp+fp, 1), acc=(tp+tn)/n)
def band(A, col, edges, labels):
    o = []
    for (a, b), l in zip(edges, labels):
        g = A[(A[col] >= a) & (A[col] <= b)]; o.append(dict(label=l, n=int(len(g)), pass_p=float(g.passed.mean()) if len(g) else None))
    return o
def cohort(nm):
    A = load(nm); S = pd.read_csv(f'{HERE}/subs_{nm}.csv'); q = ''.join(S.seq); o = {}
    o['n'] = int(len(A)); o['n_sub'] = int(len(q)); o['E_share'] = q.count('E')/len(q)
    o['base'] = dict(passed=int(A.passed.sum()), failed=int(A.fail.sum()), noshow=int(A.noshow.sum()), pass_p=A.passed.mean(), np_p=A.np_.mean(), attend_p=1-A.noshow.mean(), pass_sit_p=A[A.noshow == 0].passed.mean())
    o['status'] = {k: dict(n=int(len(g)), pass_p=g.passed.mean(), noshow_p=g.noshow.mean()) for k, g in A.groupby('repeat')}
    o['rules'] = {k: perf(A, v[2](A)) for k, v in RULES.items()}
    o['registry_only'] = perf(A, A.repeat == 1); o['flag_all_acc'] = float(A.np_.mean())
    o['auc'] = {k: auc(-(A[c] if c != 'midterm' else A.midterm.fillna(-1)), A.np_) for k, c in [('R1','logins_w4'),('R2','nsub_w4'),('R3','pES_w4'),('R4','labs_w4'),('R5','labs_sem'),('R6','midterm')]}
    # exhibit 3: logins, pooled and by enrolment status
    o['logins3'] = band(A, 'logins_w4', [(0, 8), (9, 13), (14, 999)], ['0–8', '9–13', '14+'])
    o['logins_by_status'] = {str(k): band(g, 'logins_w4', [(0, 8), (9, 999)], ['0–8', '9+']) for k, g in A.groupby('repeat')}
    o['logins_mean_by_status'] = {str(k): float(g.logins_w4.mean()) for k, g in A.groupby('repeat')}
    o['logins_r'] = dict(pooled=float(np.corrcoef(A.logins_w4, A.passed)[0, 1]), **{('first' if k == 0 else 'repeat'): float(np.corrcoef(g.logins_w4, g.passed)[0, 1]) for k, g in A.groupby('repeat')})
    # exhibit 4: lab sheets, two windows + week of last activity of those who did not attend
    o['labs_sem'] = band(A, 'labs_sem', [(0, 3), (4, 8), (9, 12)], ['0–3', '4–8', '9–12']); o['labs_w4'] = band(A, 'labs_w4', [(0, 1), (2, 2), (3, 3), (4, 4)], ['0–1', '2', '3', '4'])
    ns = A[A.noshow == 1]; o['last_week_noshow'] = [int((ns.last_week == w).sum()) for w in range(1, 14)]; o['noshow_left_by_w4'] = float((ns.last_week <= 4).mean()); o['noshow_active_to_end'] = float((ns.last_week == 13).mean())
    o['labs_sem_mean'] = dict(passed=float(A[A.passed == 1].labs_sem.mean()), failed=float(A[A.fail == 1].labs_sem.mean()), noshow=float(ns.labs_sem.mean()))
    # exhibit 5: frequency against sequence
    o['nsub'] = band(A, 'nsub_w4', [(0, 15), (16, 40), (41, 80), (81, 10**6)], ['0–15', '16–40', '41–80', '81+'])
    o['pes'] = band(A, 'pES_w4', [(0, .2499), (.25, .3999), (.40, .5499), (.55, 1)], ['< 0,25', '0,25–0,40', '0,40–0,55', '≥ 0,55'])
    g = A[A.insuf == 1]; o['pes_insuf'] = dict(n=int(len(g)), pass_p=float(g.passed.mean()))
    tm = {}
    for key, g in (('passed', A[A.passed == 1]), ('failed', A[A.fail == 1]), ('noshow', A[A.noshow == 1])):
        c = g[['EE', 'ES', 'SE', 'SS']].sum(); e = c.EE + c.ES; s_ = c.SE + c.SS
        tm[key] = dict(n=int(len(g)), EE=c.EE/e, ES=c.ES/e, SE=c.SE/s_, SS=c.SS/s_, nsub_median=float(g.nsub_w4.median()))
    o['tmat'] = tm
    # exhibit 6: working students
    sg = {}
    for k, g in A.groupby('work'):
        r3 = perf(g, RULES['R3'][2](g)); r4 = perf(g, RULES['R4'][2](g)); r34 = perf(g, RULES['R3'][2](g) | RULES['R4'][2](g)); r3m = perf(g, RULES['R3'][2](g) | (g.insuf == 1))
        sg[str(k)] = dict(n=int(len(g)), np_p=float(g.np_.mean()), pass_p=float(g.passed.mean()), insuf_p=float(g.insuf.mean()), nsub_median=float(g.nsub_w4.median()), labs_w4_mean=float(g.labs_w4.mean()), labs_sem_mean=float(g.labs_sem.mean()), R3=r3, R4=r4, R3orR4=r34, R3m=r3m)
    o['work'] = sg
    # two roads
    sit = A[A.noshow == 0]; nw = A[A.work == 0]; sitnw = sit[sit.work == 0]
    o['roads'] = dict(pes_fail=auc(-sit.pES_w4, sit.fail), pes_noshow=auc(-A.pES_w4, A.noshow), labs_fail=auc(-sit.labs_w4, sit.fail), labs_noshow=auc(-A.labs_w4, A.noshow))
    f3 = RULES['R3'][2](A); f4 = RULES['R4'][2](A)
    o['roads_flag'] = dict(R3_among_failed=float(f3[A.fail == 1].mean()), R3_among_noshow=float(f3[A.noshow == 1].mean()), R4_among_failed=float(f4[A.fail == 1].mean()), R4_among_noshow=float(f4[A.noshow == 1].mean()), R3_among_passed=float(f3[A.passed == 1].mean()), R4_among_passed=float(f4[A.passed == 1].mean()))
    # lookup for the key: every rule a group can propose from the week-4 menu
    avail = ['R1', 'R2', 'R3', 'R4']; F = {k: RULES[k][2](A) for k in avail}; F['R3m'] = F['R3'] | (A.insuf == 1); look = {}
    for k in avail + ['R3m']: look[k] = perf(A, F[k])
    for a, b in itertools.combinations(avail, 2):
        look[f'{a} ή {b}'] = perf(A, F[a] | F[b]); look[f'{a} και {b}'] = perf(A, F[a] & F[b])
    look['R3m ή R4'] = perf(A, F['R3m'] | F['R4']); look['R5'] = perf(A, RULES['R5'][2](A)); look['R6'] = perf(A, RULES['R6'][2](A))
    o['lookup'] = look
    return o
if __name__ == '__main__':
    out = dict(last=cohort('last'), this=cohort('this'), rules={k: dict(name=v[0], cut=v[1]) for k, v in RULES.items()})
    json.dump(out, open(f'{HERE}/exhibits.json', 'w', encoding='utf8'), ensure_ascii=False, indent=1, default=float)
    L = out['last']; T = out['this']; pc = lambda v: f'{100*v:.0f}%'
    print('base', L['base']); print('status', L['status'])
    for k in RULES: print(k, RULES[k][0], RULES[k][1], {kk: (pc(v) if kk in ('flagged_p','recall','precision','acc') else v) for kk, v in L['rules'][k].items() if kk in ('flagged_p','recall','precision','acc')}, '| this:', pc(T['rules'][k]['acc']), '| AUC', round(L['auc'][k], 2))
    print('registry only', pc(L['registry_only']['acc']), '| flag all', pc(L['flag_all_acc']))
    print('logins3', [(b['label'], b['n'], pc(b['pass_p'])) for b in L['logins3']], '| by status', {k: [(b['label'], b['n'], pc(b['pass_p'])) for b in v] for k, v in L['logins_by_status'].items()}, L['logins_mean_by_status'])
    print('labs_sem', [(b['label'], b['n'], pc(b['pass_p'])) for b in L['labs_sem']], '| labs_w4', [(b['label'], b['n'], pc(b['pass_p'])) for b in L['labs_w4']])
    print('last week of no-shows', L['last_week_noshow'], 'left by w4', pc(L['noshow_left_by_w4']), 'active to end', pc(L['noshow_active_to_end']), '| labs_sem mean', L['labs_sem_mean'])
    print('nsub', [(b['label'], b['n'], pc(b['pass_p'])) for b in L['nsub']]); print('pes', [(b['label'], b['n'], pc(b['pass_p'])) for b in L['pes']], 'insuf', L['pes_insuf'])
    print('tmat', {k: {kk: round(vv, 2) for kk, vv in v.items()} for k, v in L['tmat'].items()})
    for k, v in L['work'].items(): print('work', k, 'n', v['n'], 'np', pc(v['np_p']), 'insuf', pc(v['insuf_p']), '| R3 flagged', pc(v['R3']['flagged_p']), 'recall', pc(v['R3']['recall']), 'prec', pc(v['R3']['precision']), '| R4 flagged', pc(v['R4']['flagged_p']), 'recall', pc(v['R4']['recall']), 'prec', pc(v['R4']['precision']), '| R3orR4 flagged', pc(v['R3orR4']['flagged_p']), 'prec', pc(v['R3orR4']['precision']), 'acc', pc(v['R3orR4']['acc']))
    print('roads', {k: round(v, 2) for k, v in L['roads'].items()}, {k: pc(v) for k, v in L['roads_flag'].items()})
    print('lookup (last | this):')
    for k in L['lookup']: a = L['lookup'][k]; b = T['lookup'][k]; print(f"  {k:12s} flagged {pc(a['flagged_p'])} recall {pc(a['recall'])} prec {pc(a['precision'])} acc {pc(a['acc'])}  |  this: flagged {pc(b['flagged_p'])} recall {pc(b['recall'])} prec {pc(b['precision'])} acc {pc(b['acc'])}")
