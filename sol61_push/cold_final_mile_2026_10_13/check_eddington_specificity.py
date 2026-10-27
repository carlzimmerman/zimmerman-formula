"""CE-FM-070: exact ideal posterior and mass-rescale/rebin specificity audit."""
from pathlib import Path
import json,math,sys
import numpy as np
from scipy.integrate import quad
import sympy as sp
b=Path('sol61_push/cold_final_mile_2026_10_13');inp=b/'eddington_inputs';sdir=Path('campaign_fresh_gravity/CFG816_erass1_eddington');saved=json.loads((sdir/'cfg816_results.json').read_text());raw=np.load(b/'outskirt_stack_inputs/cfg687_percluster.npz',allow_pickle=False);ER=np.load(b/'outskirt_stack_inputs/erass_P.npy',allow_pickle=True)
checks=[]
def ck(n,v):
 checks.append({'name':n,'pass':bool(v)})
 if not v:raise AssertionError(n)
rows=[]
for line in (inp/'erass1_main.tsv').read_text().splitlines():
 r=line.split('\t')
 try:v=tuple(float(r[j]) for j in [1,2,3,5,6,7])
 except (ValueError,IndexError):continue
 if all(v[j]>0 for j in [3,4,5]):rows.append(v)
cat=np.array(rows);lm=np.log(cat[(cat[:,2]>=.05)&(cat[:,2]<=.5),3]*1e11);h,e=np.histogram(lm,bins=40);center=(e[:-1]+e[1:])/2;use=(np.arange(40)>np.argmax(h))&(h>=5);alpha=float(-np.polyfit(center[use],np.log(h[use]),1)[0]);ck('current catalogue alpha reproduces saved',abs(alpha-saved['alpha'])<1e-12)
sig=[];dist=[];inside=[]
for ra,de in zip(raw['ra'],raw['dec']):
 sep=((cat[:,0]-ra)*np.cos(np.radians(de)))**2+(cat[:,1]-de)**2;i=np.argmin(sep);dist.append(3600*np.sqrt(sep[i]));sig.append(.5*np.log(cat[i,5]/cat[i,4]));inside.append(cat[i,4]<=cat[i,3]<=cat[i,5])
sig=np.array(sig);ck('matched catalogue bounds ordered',all(inside));ck('all318 matches within one arcsec',max(dist)<1)
Pm=np.array([o['s|canonical|EX']['base']+o['s|canonical|EX']['res'] for o in ER]);W=np.where(raw['E']>0,1/raw['E']**2,0);numer=(W[:,3:6]*raw['D'][:,3:6]).sum(1);denom=(W[:,3:6]*Pm[:,3:6]).sum(1)
patch=np.empty(318,int);patch[np.argsort(raw['ra'])]=np.arange(318)*30//318
ck('positive model denominators',np.all(denom>0))
def terc(m):
 q=np.quantile(m,[1/3,2/3]);return [m<=q[0],(m>q[0])&(m<=q[1]),m>q[1]]
def amplitudes(groups,scale):
 den=denom*scale;ans=[]
 for g in groups:
  a=numer[g].sum()/den[g].sum();rep=np.array([numer[g&(patch!=i)].sum()/den[g&(patch!=i)].sum() for i in range(30)]);err=np.sqrt(29/30*np.sum((rep-rep.mean())**2));ans.append([float(a),float(err)])
 return ans
def mono(v):
 return all(v[j+1][0]-v[j][0]>=-np.hypot(v[j+1][1],v[j][1]) for j in range(2)) or all(v[j+1][0]-v[j][0]<=np.hypot(v[j+1][1],v[j][1]) for j in range(2))
g0=terc(raw['mg']);corr=np.exp(-alpha*sig**2);g1=terc(raw['mg']*corr);slope=.47
ab={}
for label,groups,scale in [('neither',g0,np.ones(318)),('rescale_only',g0,corr**slope),('rebin_only',g1,np.ones(318)),('both',g1,corr**slope)]:
 v=amplitudes(groups,scale);ab[label]={'tercile_A_sigma':v,'frozen_monotonicity_diagnostic':mono(v)}
ck('saved before amplitude/error reproduced',np.allclose(ab['neither']['tercile_A_sigma'],saved['CFG815 P']['before'],rtol=1e-11,atol=1e-12))
ck('saved after amplitude/error reproduced',np.allclose(ab['both']['tercile_A_sigma'],saved['CFG815 P']['after'],rtol=1e-11,atol=1e-12))
# A real zero-sigma path, rather than expression-minus-itself in source K1.
z=np.zeros(318);zc=np.exp(-alpha*z*z);zg=terc(raw['mg']*zc);zv=amplitudes(zg,zc**slope)
ck('actual zero-sigma transformation is identity',np.allclose(zv,ab['neither']['tercile_A_sigma'],rtol=1e-13))
ck('zero-sigma identity matches previous CFG815 cached terciles',np.allclose(zv,json.loads((b/'outskirt_stack_inputs/cfg815_results_P.json').read_text())['T_R']['s|canonical|EX']['terciles'][:3] and np.array(zv),rtol=1e-13)) if False else None
# Compare first two columns: CFG815 additionally stores Z.
v815=json.loads((b/'outskirt_stack_inputs/cfg815_results_P.json').read_text())['T_R']['s|canonical|EX']['terciles']
ck('zero-sigma actual matches CFG815 reference',np.allclose(zv,np.array(v815)[:,:2],rtol=1e-11))
bad=amplitudes(g0,np.full(318,.5));ck('real zero-sigma control rejects deliberately wrong half scaling',not np.allclose(bad,zv,rtol=1e-6))
# Exact conjugate posterior, with KNOWN sigma and untruncated exponential
# log-mass prior, not the actual selected catalogue generative model.
x,y,a,t=sp.symbols('x y a t',real=True);sd=sp.symbols('sd',positive=True)
ck('Gaussian completion of square',sp.simplify(-(y-x)**2/(2*sd**2)-a*x+(x-(y-a*sd**2))**2/(2*sd**2)+a*y-a*a*sd**2/2)==0)
for sigma in [.1,.79,1.2]:
 mu=-alpha*sigma*sigma;exact=math.exp(slope*mu+.5*slope*slope*sigma*sigma)
 integral=quad(lambda zz:math.exp(slope*(mu+sigma*zz))*math.exp(-zz*zz/2)/math.sqrt(2*math.pi),-10,10,epsabs=1e-12)[0]
 ck('posterior prediction moment '+str(sigma),abs(integral/exact-1)<1e-11)
mean_scale=corr**slope*np.exp(.5*slope*slope*sig**2);mean_v=amplitudes(g1,mean_scale)
# Bounded exploratory permutation specificity, NOT a calibrated causal p-value.
rng=np.random.default_rng(817);trials=[]
for i in range(99):
 perm=rng.permutation(sig);co=np.exp(-alpha*perm*perm);vv=amplitudes(terc(raw['mg']*co),co**slope);trials.append({'monotonic':mono(vv),'light_A':vv[0][0]})
mut=json.loads((sdir/'cfg816_results_MUTATE.json').read_text());ck('original mutation also same positive class',mut['cls']==saved['cls']=='SELECTION EXPLAINS PATTERN')
text=(sdir/'cfg816.py').read_text();ck('original K1 contains identical operands', 'jk(t, MODELS["CFG815 P"])[0] - jk(t, MODELS["CFG815 P"])[0]' in text)
out={'claim_id':'CE-FM-070','n_checks':len(checks),'all_pass':all(v['pass'] for v in checks),'checks':checks,'catalog_rows':len(cat),'max_catalog_match_arcsec':float(max(dist)),'alpha':alpha,'ablation':ab,'posterior_prediction_with_same_corrected_groups':mean_v,'median_extra_logscatter_prediction_factor_by_observed_tercile':[float(np.median(np.exp(.5*slope*slope*sig[g]**2))) for g in g0],'median_sigma_observed_terciles':[float(np.median(sig[g])) for g in g0],'permutation_diagnostic':{'seed':817,'trials':99,'n_same_frozen_positive_monotonic_label':sum(v['monotonic'] for v in trials),'light_A_range':[min(v['light_A'] for v in trials),float(np.median([v['light_A'] for v in trials])),max(v['light_A'] for v in trials)]},'scope':'Ideal Gaussian/power-law posterior calculation and cached ratio diagnostics; no intrinsic mass function, count-rate selection or catalog posterior calibration inferred. Source class retained; no physical corrected fit/new frozen verdict.'}
Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ['checks','scope']}))
