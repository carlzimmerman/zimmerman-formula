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
base=[r for r in p['optical_table'] if r['name'] not in excluded and r['name']!='N7331']
matched=[r for r in base if key(r['name']) in modern and not modern[key(r['name'])]['author_excluded'] and not modern[key(r['name'])]['upper_limit']]
res={'temperature_exclusions':sorted(excluded),'hotgas':{}}
for label,rr,usemodern in [('original85',p['optical_table'],False),('measured81',[r for r in p['optical_table'] if r['name'] not in excluded],False),('measured_without_N7331',base,False),('same_sample_old_BH',matched,False),('same_sample_modern_BH',matched,True)]:
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
ck('baseline reproduction',np.allclose(res['hotgas']['original85']['held_out_RMSE'],prev['leave_group_out_object_weighted_RMSE'],rtol=1e-10))
# Exact audit: the old integral is twice the integral for beta=4/3, not beta=2/3.
x=sp.symbols('x',positive=True);old=sp.atan(x)-x/(1+x*x);correct=x-sp.atan(x)
ck('old derivative',sp.simplify(sp.diff(old,x)-2*x*x/(1+x*x)**2)==0)
ck('beta two-thirds derivative',sp.simplify(sp.diff(correct,x)-x*x/(1+x*x))==0)
G=6.674e-11;MS=1.98892e30;KPC=3.0857e19;R=1380*KPC;Mg=1.2e14*MS;Mc=2e13*MS;ss=2.5396;cap=.647610
# Preserve exact old kernel including its small join mismatch.
def kernel(s):return np.where(s<ss,s/np.expm1(np.sqrt(s)),cap)
def kd(s):
 u=np.sqrt(s);e=np.expm1(u)
 return np.where(s<ss,1/e-u*np.exp(u)/(2*e*e),0.)
def I(x,b):return quad(lambda z:z*z*(1+z*z)**(-1.5*b),0,float(x),epsabs=1e-10,epsrel=1e-10)[0]
for z in [.01,.1,1,10,30]:ck('quadrature beta benchmark '+str(z),np.isclose(I(z,2/3),z-np.arctan(z),rtol=1e-8))
cl=[]
for a0 in [9.3619e-11,1.1279e-10]:
 for b in [.6,2/3,.7]:
  for f in [.08,.1,.12]:
   rc=f*R;r=np.geomspace(20*KPC,1500*KPC,120);xx=r/rc;norm=I(R/rc,b)
   m=Mg*np.array([I(z,b) for z in xx])/norm+Mc
   dm=Mg/norm/rc*xx**2*(1+xx*xx)**(-1.5*b)
   s=G*m/r**2/a0;ds=G/a0*(dm/r**2-2*m/r**3)
   rho=a0/G/(4*np.pi*r**2)*(2*r*kernel(s)+r*r*kd(s)*ds)
   win=(r>40*KPC)&(r<R)&(rho>0);slope=float(np.polyfit(np.log(r[win]),np.log(rho[win]),1)[0])
   sR=G*(Mg+Mc)/R**2/a0;boost=float(kernel(sR)/sR)
   ck('positive corrected density',np.all(rho>0))
   # Independent finite difference away from join.
   def mph(q):
    mq=Mg*I(q/rc,b)/norm+Mc;sq=G*mq/q**2/a0
    return a0*float(kernel(sq))*q*q/G
   for j in [20,60,100]:
    h=r[j]*1e-5;fd=(mph(r[j]+h)-mph(r[j]-h))/(2*h)/(4*np.pi*r[j]**2)
    ck('analytic density finite difference',np.isclose(fd,rho[j],rtol=1e-6))
   cl.append({'a0':a0,'beta':b,'core_fraction':f,'slope_40kpc_R500':slope,'Mphantom_over_Mbar_R500':boost})
oldrows=[]
for a0 in [9.3619e-11,1.1279e-10]:
 r=np.geomspace(20*KPC,1500*KPC,120);xx=r/(.1*R);m=Mg/(np.pi/2)*(np.arctan(xx)-xx/(1+xx*xx))+Mc
 s=G*m/r**2/a0;mp=a0*kernel(s)*r*r/G;rho=np.gradient(mp,r)/(4*np.pi*r*r);win=(r>40*KPC)&(r<R)&(rho>0)
 oldrows.append({'a0':a0,'slope':float(np.polyfit(np.log(r[win]),np.log(rho[win]),1)[0]),'Mgas_inside_R500_over_named_Mgas':float((np.arctan(10)-10/101)/(np.pi/2))})
res['cluster']={'old_reconstruction':oldrows,'corrected':cl,'kernel_join_jump':float(cap-ss/np.expm1(np.sqrt(ss))),'density_implied_by_old_mass':'2*rho0/(1+x^2)^2; beta=4/3, not beta=2/3; beta parameter unused in old robustness loop','observational_fit':False}
# Radius-matched single-galaxy diagnostic.
a=np.loadtxt(ROOT/'real_research/data/sparc_data/NGC7331_rotmod.dat');r,v,ev,vg,vd,vb=a[:,:6].T
q=next(r for r in p['optical_table'] if r['name']=='N7331');mbh=10**q['logMBH']*14.7/q['distance_Mpc'];bh2=G*MS*mbh/(r*KPC)/1e6
outer=r>=r.max()/2;grid=[]
for ud in [.3,.5,.7]:
 for ub in [.5,.7,.9]:
  bary=vg*np.abs(vg)+ud*vd**2+ub*vb**2;extra=v*v-bary
  take=outer&(extra>0);ratio=extra[take]/bh2[take]
  # constant central enhancement: weighted fit in velocity-squared space, approximate errors.
  sig=2*v*ev;C=max(0.,np.sum(bh2[outer]*extra[outer]/sig[outer]**2)/np.sum(bh2[outer]**2/sig[outer]**2))
  grid.append({'disk_ML':ud,'bulge_ML':ub,'positive_outer_points':int(take.sum()),'required_central_mass_multiplier_range':[float(min(ratio)),float(max(ratio))] if len(ratio) else None,'best_constant_multiplier':float(C),'chi2_v_squared':float(np.sum(((extra[outer]-C*bh2[outer])/sig[outer])**2)),'outer_points':int(outer.sum())})
nom=vg*np.abs(vg)+.5*vd**2+.7*vb**2
res['radial']={'BH_mass_conditional_Msun':mbh,'BH_provenance':'unresolved primary method; not a secure new measurement','grid':grid,'distance_Mpc':14.7,'outer_definition':'r >= 0.5 rmax','r_kpc':r.tolist(),'vobs':v.tolist(),'vbar2_nominal':nom.tolist(),'extra_g_nominal_m_s2':((v*v-nom)*1e6/(r*KPC)).tolist(),'gBH_m_s2':(bh2*1e6/(r*KPC)).tolist(),'outer_radius_kpc':[float(min(r[outer])),float(max(r[outer]))]}
ck('negative gas contribution retained',np.any(vg<0) and np.any(vg*np.abs(vg)<0))
ck('36 radial rows',len(a)==36)
res['checks_count']=len(checks);res['checks']=checks
(O/'results.json').write_text(json.dumps(res,indent=2)+'\n')
print(json.dumps({'checks':len(checks),'hotgas':{k:{x:v[x] for x in ['n','partial_r','held_out_RMSE']} for k,v in res['hotgas'].items()},'cluster_slopes':[min(t['slope_40kpc_R500'] for t in cl),max(t['slope_40kpc_R500'] for t in cl)],'radial':grid},indent=2))
