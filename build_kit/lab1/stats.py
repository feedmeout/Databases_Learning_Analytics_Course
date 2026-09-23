import numpy as np, pandas as pd
def keystats(A):
    A=A.copy(); A['np_']=1-A.passed; o={}
    o['pass']=A.passed.mean(); o['noshow']=A.noshow.mean(); o['repeat']=A.repeat.mean(); o['work']=A.work.mean()
    o['pass_first']=A[A.repeat==0].passed.mean(); o['pass_rep']=A[A.repeat==1].passed.mean()
    o['pass_work']=A[A.work==1].passed.mean(); o['pass_nowork']=A[A.work==0].passed.mean()
    lo=A.logins_w4<=8; o['log_low']=A[lo].passed.mean(); o['log_high']=A[~lo].passed.mean()
    f=A[A.repeat==0]; o['log_low_first']=f[f.logins_w4<=8].passed.mean(); o['log_high_first']=f[f.logins_w4>8].passed.mean()
    r=A[A.repeat==1]; o['log_low_rep']=r[r.logins_w4<=8].passed.mean()
    for lab,(a,b) in {'ls_0_3':(0,3),'ls_4_8':(4,8),'ls_9_12':(9,12)}.items(): o[lab]=A[(A.labs_sem>=a)&(A.labs_sem<=b)].passed.mean()
    for lab,(a,b) in {'l4_0_1':(0,1),'l4_2':(2,2),'l4_3':(3,3),'l4_4':(4,4)}.items(): o[lab]=A[(A.labs_w4>=a)&(A.labs_w4<=b)].passed.mean()
    for lab,(a,b) in {'ns_0_15':(0,15),'ns_16_40':(16,40),'ns_41_80':(41,80),'ns_81':(81,10**6)}.items(): o[lab]=A[(A.nsub_w4>=a)&(A.nsub_w4<=b)].passed.mean()
    for lab,(a,b) in {'pes_lt25':(-1,.25),'pes_25_40':(.25,.40),'pes_40_55':(.40,.55),'pes_ge55':(.55,1.01)}.items(): o[lab]=A[(A.pES_w4>=a)&(A.pES_w4<b)].passed.mean()
    o['pes_missing_pass']=A[A.pES_w4.isna()].passed.mean()
    o['miss_nowork']=A[A.work==0].pES_w4.isna().mean(); o['miss_work']=A[A.work==1].pES_w4.isna().mean()
    o['flag_l4_nowork']=(A[A.work==0].labs_w4<=2).mean(); o['flag_l4_work']=(A[A.work==1].labs_w4<=2).mean()
    return o
