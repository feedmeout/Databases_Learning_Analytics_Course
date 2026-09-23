"""Lab 1 designed case: simulated first-year programming course (Greek university).
Data-generating process with KNOWN ground truth. Deterministic: same seed -> same files.
Two cohorts: 'last' (outcomes known, used in the student pack) and 'this' (week-4 view for students, outcomes only in the key)."""
import numpy as np, pandas as pd, json, sys
L = lambda x: 1/(1+np.exp(-x))
P = dict(p_repeat=.30, p_work=.22, n_labs=12, ex_per_lab=5, cut_week=4, mid_week=8, min_E_trans=4)

def one_exercise(rng, pE0, pES, pSE, qc, g, cap=30):
    seq = []; state = 'E' if rng.random() < pE0 else 'S'
    while True:
        seq.append(state)
        if len(seq) >= cap: break
        if state == 'S':
            if rng.random() < qc: break                      # tests pass: exercise completed
            state = 'E' if rng.random() < pSE else 'S'
        else:
            if rng.random() < g: break                       # gives up after an error
            state = 'S' if rng.random() < pES else 'E'
    return ''.join(seq)

def simulate(n, seed):
    rng = np.random.default_rng(seed); rows = []; subs = []; logs = []
    for i in range(n):
        rep = rng.random() < P['p_repeat']; work = rng.random() < P['p_work']
        th = rng.normal(0, 1) - (.3 if rep else 0)            # skill
        c = rng.normal(0, 1) - (1.3 if rep else 0)            # commitment
        noshow = rng.random() < L(-1.45 - 1.25*c - .30*th)
        grade = float(np.clip(round((5.95 + 1.75*th + .35*c + rng.normal(0, 1.2))*2)/2, 0, 10))
        passed = (not noshow) and grade >= 5
        if noshow and rng.random() > .22:                     # most no-shows leave during the semester, a fifth stay active to the end
            last = int(rng.choice(np.arange(1, 13), p=np.array([1,2,3,7,10,13,15,16,13,10,6,4])/100))
        else: last = 13
        lam = np.exp(1.30) * (.38 if rep else 1.0) * float(np.exp(rng.normal(0, .25)))   # logins depend on enrolment status and personal habit only
        wk = [int(rng.poisson(lam)) if w <= last else 0 for w in range(1, 14)]
        pE0, pES, pSE, qc, g = L(.0 - .7*th), L(-.2 + .9*th), L(-.95 - .5*th), L(-.1 + .6*th), L(-2.3 - .9*c)
        a_lab = L(1.7 + 1.1*c)
        seq_w4 = []; labs_w4 = 0; labs_sem = 0; nsub_sem = 0
        for k in range(1, P['n_labs'] + 1):
            week = k
            if week > last or rng.random() > a_lab * (1 if week <= 6 else L(1.2 + .9*th)): continue
            late = work and rng.random() < .50                # working students hand in half of their labs after the weekly cut
            labs_sem += 1; ontime4 = (week <= P['cut_week']) and not late
            if ontime4: labs_w4 += 1
            for e in range(P['ex_per_lab']):
                if rng.random() > .92: continue
                s = one_exercise(rng, pE0, pES, pSE, qc, g); nsub_sem += len(s)
                subs.append((i + 1, k, e + 1, week, int(late), s))
                if ontime4: seq_w4.append(s)
        tr = {'EE':0,'ES':0,'SE':0,'SS':0}
        for s in seq_w4:
            for a, b in zip(s, s[1:]): tr[a+b] += 1
        nE = tr['EE'] + tr['ES']; nsub4 = sum(map(len, seq_w4))
        pes = tr['ES']/nE if nE >= P['min_E_trans'] else np.nan
        mid = np.nan
        if last >= P['mid_week'] and rng.random() < L(2.6 + .9*c):
            mid = float(np.clip(round((5.1 + 1.7*th + .3*c + rng.normal(0, 1.0))*2)/2, 0, 10))
        rows.append(dict(id=i+1, repeat=int(rep), work=int(work), logins_w4=sum(wk[:4]), logins_sem=sum(wk), nsub_w4=nsub4, nE_trans_w4=nE,
                         pES_w4=pes, EE=tr['EE'], ES=tr['ES'], SE=tr['SE'], SS=tr['SS'], labs_w4=labs_w4, labs_sem=labs_sem, midterm=mid,
                         last_week=last, noshow=int(noshow), exam=(np.nan if noshow else grade), passed=int(passed), theta=th, commit=c))
        logs.append([i+1] + wk)
    return pd.DataFrame(rows), pd.DataFrame(subs, columns=['id','lab','exercise','week','late','seq']), pd.DataFrame(logs, columns=['id']+[f'w{w}' for w in range(1,14)])

if __name__ == '__main__':
    seedA, seedB = 36, 71        # chosen among seeds 1-80 as the cohorts closest to the large-sample values of the process (see population_values.json)
    A, subA, logA = simulate(312, seedA); B, subB, logB = simulate(298, seedB)
    for nm, D in (('last', A), ('this', B)):
        D.to_csv(f'cohort_{nm}_full.csv', index=False)
    subA.to_csv('subs_last.csv', index=False); subB.to_csv('subs_this.csv', index=False); logA.to_csv('logins_last.csv', index=False); logB.to_csv('logins_this.csv', index=False)
    print('written', len(A), len(B))
