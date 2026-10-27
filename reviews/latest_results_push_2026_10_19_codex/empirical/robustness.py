import json,pathlib,math,numpy as np
P=pathlib.Path(__file__).resolve().parent
D=json.loads((P/'run/result.json').read_text())

def golden(f,hi):
 lo=0.;t=(math.sqrt(5)-1)/2;c=hi-t*(hi-lo);d=lo+t*(hi-lo);fc=f(c);fd=f(d)
 for _ in range(80):
  if fc<fd: hi,d,fd=d,c,fc;c=hi-t*(hi-lo);fc=f(c)
  else: lo,c,fc=c,d,fd;d=lo+t*(hi-lo);fd=f(d)
 x=(lo+hi)/2;return 0. if f(0.)<=f(x) else x

def fit(t):
 sl2=np.array([r['sl2'] for r in t]);yo=np.log10([r['so'] for r in t])
 f=lambda a:float(np.mean((yo-.5*np.log10(sl2+a))**2))
 return golden(f,10*max(float(max(r['so']**2 for r in t)),1.)),max(1.,10**float(np.mean(2*yo-np.log10(sl2))))

def score(mw,m31):
 e1=[];e2=[]
 for tr,te in ((mw,m31),(m31,mw)):
  a,q=fit(tr);sl2=np.array([r['sl2'] for r in te]);yo=np.log10([r['so'] for r in te])
  e1.extend((yo-.5*np.log10(sl2+a)).tolist());e2.extend((yo-.5*np.log10(q*sl2)).tolist())
 return np.sqrt(np.mean(np.array(e1)**2)),np.sqrt(np.mean(np.array(e2)**2))

O={}
for foot in ('canonical','alt'):
 rows=D['footings'][foot]['rows'];s=[r for r in rows if r['delta']>.05]
 mw=[r for r in rows if r['host']=='mw'and r['lgbar']<-11.9];m31=[r for r in rows if r['host']=='m_031'and r['lgbar']<-11.9]
 base=score(mw,m31);jack=[]
 for name in [r['name'] for r in mw+m31]:
  z=score([r for r in mw if r['name']!=name],[r for r in m31 if r['name']!=name]);jack.append({'excluded':name,'additive_rmse':float(z[0]),'multiplicative_rmse':float(z[1]),'difference':float(z[0]-z[1])})
 rng=np.random.default_rng(20261019);bs=[];mean_bs=[]
 s1=[r for r in s if r['host']=='mw'];s2=[r for r in s if r['host']=='m_031']
 for _ in range(1000):
  t1=[mw[i] for i in rng.integers(0,len(mw),len(mw))];t2=[m31[i] for i in rng.integers(0,len(m31),len(m31))];z=score(t1,t2);bs.append(z[0]-z[1])
  t1=[s1[i] for i in rng.integers(0,len(s1),len(s1))];t2=[s2[i] for i in rng.integers(0,len(s2),len(s2))]
  mean_bs.append([np.mean([r[k] for r in t2])-np.mean([r[k] for r in t1]) for k in ('lVx','lVl','normalized')])
 x=np.array([r['logM'] for r in s]);mass_slopes={k:float(np.polyfit(x,[r[k] for r in s],1)[0]) for k in ('lVx','lVl','normalized')}
 O[foot]={'low_g_cross_host_difference_additive_minus_multiplicative':float(base[0]-base[1]),'bootstrap':{'draws':1000,'seed':20261019,'median':float(np.median(bs)),'p025':float(np.quantile(bs,.025)),'p975':float(np.quantile(bs,.975)),'fraction_positive':float(np.mean(np.array(bs)>0)),'interpretation':'Descriptive stratified resampling with refits, not a calibrated new-data significance test.'},'jackknife':jack,'selected_M31_minus_MW_gap_bootstrap_se':dict(zip(('lVx','lVl','normalized'),np.std(mean_bs,axis=0).tolist())),'pooled_logM_slope_decomposition':mass_slopes}
(P/'robustness_run/result.json').write_text(json.dumps(O,indent=2)+'\n');print(json.dumps(O,indent=2))
