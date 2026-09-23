"""Student-facing and teacher-only data files for Lab 1 -> lab1/data/ ; checks that P(E->S) can be recomputed from the submission files."""
import pandas as pd, numpy as np, os
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = f'{HERE}/data'; os.makedirs(f'{OUT}/teacher', exist_ok=True)
REN = dict(id='student_id', logins_w4='logins_w1_4', nsub_w4='submissions_w1_4', pES_w4='p_ES_w1_4', labs_w4='sheets_on_time_w1_4', labs_sem='sheets_semester', noshow='no_show', last_week='last_active_week', work='works')
def prep(A):
    A = A.copy(); A['enrolment'] = np.where(A.repeat == 1, 'repeat', 'first'); return A.rename(columns=REN)
W4 = ['student_id', 'enrolment', 'works', 'logins_w1_4', 'submissions_w1_4', 'EE', 'ES', 'SE', 'SS', 'p_ES_w1_4', 'sheets_on_time_w1_4']
FULL = W4 + ['sheets_semester', 'midterm', 'exam', 'no_show', 'passed', 'last_active_week']
for nm in ('last', 'this'):
    A = prep(pd.read_csv(f'{HERE}/cohort_{nm}_full.csv')); S = pd.read_csv(f'{HERE}/subs_{nm}.csv').rename(columns={'id': 'student_id', 'lab': 'sheet', 'seq': 'sequence'}); G = pd.read_csv(f'{HERE}/logins_{nm}.csv').rename(columns={'id': 'student_id'})
    A.round(4)[FULL + ['theta', 'commit']].rename(columns={'theta': 'skill', 'commit': 'commitment'}).to_csv(f'{OUT}/teacher/students_{nm}_full.csv', index=False)
    if nm == 'last':
        A.round(4)[FULL].to_csv(f'{OUT}/students_last.csv', index=False); S.to_csv(f'{OUT}/submissions_last.csv', index=False); G.to_csv(f'{OUT}/logins_last.csv', index=False)
    else:
        A.round(4)[W4].to_csv(f'{OUT}/students_this_week4.csv', index=False); S[(S.week <= 4) & (S.late == 0)].to_csv(f'{OUT}/submissions_this_week4.csv', index=False); G[['student_id', 'w1', 'w2', 'w3', 'w4']].to_csv(f'{OUT}/logins_this_week4.csv', index=False)
    # consistency: recompute the week-4 indicators from the raw files
    s4 = S[(S.week <= 4) & (S.late == 0)]; rec = {}
    for sid, g in s4.groupby('student_id'):
        ee = es = 0
        for q in g.sequence:
            for a, b in zip(q, q[1:]):
                if a == 'E': ee += (b == 'E'); es += (b == 'S')
        rec[sid] = (es / (ee + es)) if (ee + es) >= 4 else np.nan
    r = A.student_id.map(rec); ok = np.allclose(r.fillna(-1), A.p_ES_w1_4.fillna(-1), atol=1e-9)
    n4 = s4.groupby('student_id').sequence.apply(lambda x: x.str.len().sum()); ok2 = (A.student_id.map(n4).fillna(0).astype(int) == A.submissions_w1_4).all()
    ok3 = (G[['w1', 'w2', 'w3', 'w4']].sum(axis=1).values == A.logins_w1_4.values).all()
    print(nm, '| P(E->S) recomputed from submissions matches:', ok, '| submission counts match:', ok2, '| logins match:', ok3)
for f in sorted(os.listdir(OUT)):
    p = f'{OUT}/{f}'
    if os.path.isfile(p): print(f'{f:32s} {os.path.getsize(p)/1024:8.1f} kB')
