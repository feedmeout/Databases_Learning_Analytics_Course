import pandas as pd, numpy as np
def auc(x,y):
    d=pd.DataFrame({'x':x,'y':y}).dropna(); pos=d.x[d.y==1].values; neg=d.x[d.y==0].values
    return (sum((p>neg).sum()+.5*(p==neg).sum() for p in pos))/(len(pos)*len(neg))
if __name__=="__main__":
  for nm in ('last','this'):
      A=pd.read_csv(f'/home/claude/kit/lab1/cohort_{nm}_full.csv'); S=pd.read_csv(f'/home/claude/kit/lab1/subs_{nm}.csv'); A['np_']=1-A.passed
      print(f'== {nm}: n={len(A)} repeat={A.repeat.mean():.2f} work={A.work.mean():.2f} noshow={A.noshow.mean():.3f} pass|sit={A[A.noshow==0].passed.mean():.3f} pass={A.passed.mean():.3f}  pass by status={A.groupby("repeat").passed.mean().round(2).to_dict()} by work={A.groupby("work").passed.mean().round(2).to_dict()}')
      q=''.join(S.seq); print('   E share',round(q.count('E')/len(q),3),'| pES mean',round(A.pES_w4.mean(),3),'| pES missing: all',round(A.pES_w4.isna().mean(),3),'by work',A.groupby('work').pES_w4.apply(lambda s:round(s.isna().mean(),2)).to_dict())
      for v in ['midterm','labs_sem','pES_w4','labs_w4','logins_w4','nsub_w4']:
          a=auc(-A[v],A.np_); d=A[[v,'passed','repeat']].dropna()
          r=np.corrcoef(d[v],d.passed)[0,1]; rw=[np.corrcoef(g[v],g.passed)[0,1] for _,g in d.groupby('repeat')]
          print(f'   {v:10s} AUC(notpass)={a:.2f} r={r:+.2f} within first={rw[0]:+.2f} repeat={rw[1]:+.2f} n={len(d)}')
