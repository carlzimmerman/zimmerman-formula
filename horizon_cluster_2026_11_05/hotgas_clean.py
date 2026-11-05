"""HC008/009: provenance sensitivity, corrected cluster integral, radial diagnostic.
Usage: python horizon_cluster_2026_11_05/deeper.py OUTPUT
"""
import json,sys,re
from pathlib import Path
import numpy as np
from scipy.integrate import quad
from scipy.stats import pearsonr
import sympy as sp
B=Path(__file__).resolve().parent;ROOT=B.parent;O=Path(sys.argv[1]);O.mkdir(parents=True,exist_ok=True)
checks=[];rng=np.random.default_rng(32008)
def ck(s,v):
 assert v,s
 checks.append(s)
def fit(X,y):
 b=np.linalg.lstsq(X,y,rcond=None)[0];e=y-np.sum(X*b,axis=1)
 ck('finite fit',np.isfinite(b).all() and np.isfinite(e).all())
 return b,e
p=json.loads((B/'data/gaspari.json').read_text());xr={r['name']:r for r in p['xray_table']}
prev=json.loads((B/'continuation003/results.json').read_text());groupmap={n:g for g,ns in prev['group_members'].items() for n in ns}
excluded={p['xray_table'][i-1]['name'] for i in [50,57,66,76]}
ck('inferred temperature identities',excluded=={'N1374','N5077','N7768','N6086'})
def key(s):
 s=s.replace(' ','');s=re.sub(r'^N(?=\d)','NGC',s);s=re.sub(r'^(NGC|IC)0+',r'\1',s);return s
modern={key(r['name']):r for r in json.loads((B/'data/galaxies.json').read_text())['rows']}
def env(s):return next((c for c in ['BCG','BGG','BFG'] if s.startswith(c)),'isolated' if s=='isolated' else 'satellite')
upper={r['name'] for r in json.loads((B/'data/bh_upper_limit_audit.json').read_text())['rows']}
base=[r for r in p['optical_table'] if r['name'] not in excluded and r['name'] not in upper]
matched=[r for r in base if key(r['name']) in modern and not modern[key(r['name'])]['author_excluded'] and not modern[key(r['name'])]['upper_limit']]
res={'temperature_exclusions':sorted(excluded),'hotgas':{}}
for label,rr,usemodern in [('without_16_upper_limits',[r for r in p['optical_table'] if r['name'] not in upper],False),('without_upper_limits_or_inferred_T',base,False),('same_sample_old_BH',matched,False),('same_sample_modern_BH',matched,True)]:
 X=np.array([[1,r['logSigma'],r['logLK'],r['logRe_opt_kpc'],np.log10(r['distance_Mpc'])]+[float(env(xr[r['name']]['environment'])==c) for c in ['BGG','BFG','isolated','satellite']] for r in rr])
 t=np.array([xr[r['name']]['logTx_g'] for r in rr]);y=np.array([modern[key(r['name'])]['logMBH']+np.log10(r['distance_Mpc']/modern[key(r['name'])]['distance_Mpc']) if usemodern else r['logMBH'] for r in rr]);A=np.c_[X,t]
 gg=np.array([groupmap[r['name']] for r in rr]);ug=np.unique(gg);pred=np.zeros((2,len(rr)));groupmse=[]
 for g in ug:
  test=gg==g;train=~test
  ck('fold full rank '+label+g,np.linalg.matrix_rank(A[train])==A.shape[1])
  for j,Z in enumerate([X,A]):pred[j,test]=np.sum(Z[test]*fit(Z[train],y[train])[0],axis=1)
  groupmse.append(np.mean((pred[:,test]-y[test])**2,axis=1))
 vals=[]
 for _ in range(1000):
  ii=np.concatenate([np.where(gg==g)[0] for g in rng.choice(ug,len(ug))])
  if np.linalg.matrix_rank(A[ii])==A.shape[1]:vals.append(fit(A[ii],y[ii])[0][-1])
 res['hotgas'][label]={'n':len(rr),'groups':len(ug),'names':[r['name'] for r in rr], 'partial_r':float(pearsonr(fit(X,y)[1],fit(X,t)[1]).statistic),'coefficient':float(fit(A,y)[0][-1]),'group_bootstrap_95pct':np.quantile(vals,[.025,.5,.975]).tolist(),'full_rank_draws':len(vals),'held_out_RMSE':np.sqrt(np.mean((pred-y)**2,axis=1)).tolist(),'equal_group_RMSE':np.sqrt(np.mean(groupmse,axis=0)).tolist()}
res['excluded_upper_limits']=sorted(upper)
res['checks_count']=len(checks)
(O/'results.json').write_text(json.dumps(res,indent=2)+'\n')
print(json.dumps({k:{x:v[x] for x in ['n','partial_r','held_out_RMSE','coefficient','group_bootstrap_95pct']} for k,v in res['hotgas'].items()},indent=2))
