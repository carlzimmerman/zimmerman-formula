"""CE-FM-063: fixed-mass aperture checks and Msun/h retention dictionary."""
import ast,json,math,sys
from pathlib import Path
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq
from scipy.special import ellipk
from scipy.stats import chi2
base=Path('campaign_fresh_gravity'); p=base/'CFG804_catchment_supply_derived'; p805=base/'CFG805_two_halo_t1x'
s=5.364; fb=1/(1+s);h=.6736
# Source pure functions only: no module-level fits, imports, profiles or writes.
ns={'math':math,'MUT':False,'FB':fb}
tree=ast.parse((p/'cfg804.py').read_text())
exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in ['fret_of','N_of']],type_ignores=[]),'cfg804_defs','exec'),ns)
checks=[]
def ck(name,v):
 checks.append({'name':name,'pass':bool(v)})
 if not v:raise AssertionError(name)
def f(lm):
 return .1+.45*np.clip(lm-12.5,0,1)+.30*np.clip(lm-13.5,0,7/6)
def root(lmb,unit_h):
 # q = log10(Mta physical/Msun); rule input = log10(h Mta/Msun).
 q=brentq(lambda q:10**(q-lmb)*fb*f(q+math.log10(unit_h))-1,lmb,lmb+3,xtol=1e-13)
 return 1/float(f(q+math.log10(unit_h))),q
for lm in [10.,10.5,10.8,11.,11.5,12.,13.]:
 N,q=root(lm,1);NN,qq=ns['N_of'](lm)
 ck('source root dictionary h=1 '+str(lm),abs(N-NN)<1e-8 and abs(q-qq)<1e-9)
 Nr,qr=root(lm,h)
 ck('unit-translated budget identity '+str(lm),abs(10**(qr-lm)*fb/Nr-1)<1e-12)
 ck('unit shift cannot reduce supply '+str(lm),Nr>=N-1e-10)
ck('plateau control logMb10.5 unchanged',root(10.5,h)[0]==10. and root(10.5,1)[0]==10.)
d=Path('real_research/data/lensing_rar/brouwer2021_rar')
raw=[np.loadtxt(d/f'Fig-3_Lensing-rotation-curves_Massbin-{i}.txt') for i in range(1,5)]
R=np.array([z[:,0] for z in raw]);Y=np.concatenate([z[:,1]/z[:,4] for z in raw])
c=np.loadtxt(d/'Fig-3_Lensing-rotation-curves_Massbins_covmatrix.txt');keys=sorted(set(c[:,0]));C=np.zeros((60,60))
for row in c:
 i=keys.index(row[0])*15+int(np.argmin(abs(R[0]-row[2])));j=keys.index(row[1])*15+int(np.argmin(abs(R[0]-row[3])))
 C[i,j]=row[4]/row[6]
ck('covariance positive definite',np.linalg.eigvalsh(C).min()>0)
M=lambda x:(math.sqrt(1+4*x*x)-1)/2
Mp=lambda x:2*x/math.sqrt(1+4*x*x)
rho=lambda x:1/(2*math.pi*x*math.sqrt(1+4*x*x))
edge=lambda N:math.sqrt(s*N*(1+s*N))
# Direct shell aperture; source instead computes cumulative gridded Sigma.
def esd(x,N):
 if N is not None and x>=edge(N):return (1+s*N)/(math.pi*x*x)
 top=edge(N) if N is not None else np.inf
 sig=2*quad(lambda z:rho(math.hypot(x,z)),0,math.sqrt(top*top-x*x),epsabs=1e-11)[0] if N is not None else ellipk(1/(1+4*x*x))/(math.pi*math.sqrt(1+4*x*x))
 mc=M(x)+quad(lambda r:Mp(r)*(x/r)**2/(1+math.sqrt(max(0,1-(x/r)**2))),x,top,epsabs=1e-11)[0]
 return (1+mc)/(math.pi*x*x)-sig
NGRID=np.round(np.r_[1.,np.arange(2.,10.01,.25)],2)
rows=[];scores=[]
for foot,a0si in [('canonical',9.3603e-11),('alt',1.1312e-10)]:
 rec=json.loads((p/('cfg804_results'+('_alt' if foot=='alt' else '')+'.json')).read_text());a0=a0si*3.0857e16/1e6
 for scope,idx in [('primary',np.where(R[0]<=.31)[0]),('all',np.arange(15))]:
  sel=np.concatenate([idx+15*b for b in range(4)]);Csel=C[np.ix_(sel,sel)];preds={k:[] for k in ['source_snapped','source_continuous','h_units_continuous']}
  for b,lmb in enumerate(rec[scope]['logMb']):
   mass=10**lmb;rM=math.sqrt(4.30091e-3*mass/a0)
   N,q=root(lmb,1.);Nh,qh=root(lmb,h);Nsn=float(NGRID[np.argmin(abs(NGRID-N))])
   for k,n in [('source_snapped',Nsn),('source_continuous',N),('h_units_continuous',Nh)]:preds[k].extend([mass/rM**2*esd(rr*1e6/rM,n) for rr in R[b,idx]])
   row={'foot':foot,'scope':scope,'bin':b+1,'logMb':lmb,'source_N':N,'source_N_snapped':Nsn,'translated_N':Nh,'source_logMta_physical':q,'translated_logMta_physical':qh,'translated_rule_logMta_h':qh+math.log10(h),'source_edge_kpc':edge(N)*rM/1e3,'translated_edge_kpc':edge(Nh)*rM/1e3,'source_cold_budget_Msun':s*N*mass,'translated_cold_budget_Msun':s*Nh*mass,'unretained_baryon_budget_Msun':(Nh-1)*mass}
   rows.append(row)
   ck('mass profile integrates to stock '+foot+scope+str(b),abs(M(edge(Nh))/(s*Nh)-1)<1e-12)
   ck('cold plus all catchment baryons equals Mta '+foot+scope+str(b),abs((s*Nh*mass+Nh*mass)/10**qh-1)<1e-12)
  values={}
  for key,pred in preds.items():
   r=Y[sel]-pred;values[key]=float(r@np.linalg.solve(Csel,r))
  ck('independent source fixed-mass chi2 '+foot+scope,abs(values['source_snapped']-rec[scope]['chi2_D'])<.6)
  scores.append({'foot':foot,'scope':scope,'fixed_logMb':rec[scope]['logMb'],'stored_chi2_D':rec[scope]['chi2_D'],'chi2':values,'interpretation':'Fixed original masses; source .25-N snapping isolated from unit change; no reoptimization or new gate/class.'})
# Scalar score reconciliation only, not an independent 2-halo projection/cosmology run.
r805=json.loads((p805/'cfg805_results.json').read_text());m805=json.loads((p805/'cfg805_results_MUTATE.json').read_text())
for scope,n in [('all',60),('primary',32)]:
 z=r805[scope];ck('805 saved delta '+scope,abs(z['chi2_D2h']-z['chi2_B2h']-z['dchi2'])<1e-12)
 ck('805 saved nominal p '+scope,np.isclose(chi2.sf(z['chi2_D2h'],n-8),z['p_D2h'],rtol=1e-12))
ck('805 K2 failed preserved',r805['K2'] is False)
# Snapshot's statistic is a finite-box discrete mode sum. It contains NO modes
# below k_f; reduced Pk samples discard within-bin correlations with W8^2.
j=json.loads(Path(sys.argv[2]).read_text());snap=j['snap']['x0.2562'];k=np.array(snap['k']);pk=np.array(snap['P_grav']);ok=(k>0)&np.isfinite(pk)&(pk>0);k,pk=k[ok],pk[ok]
W=lambda x:3*(np.sin(x)-x*np.cos(x))/x**3
sg=float(np.sqrt(np.trapz(k*k*pk*W(8*k)**2,k)/(2*np.pi**2)))
ck('805 sigma8 recomputation matches saved result',np.isclose(sg,r805['sigma8'],rtol=1e-12))
ck('805 mismatch above frozen2pct',abs(sg/snap['sigma8_grav']-1)>.02)
# If a template were changed by a scalar alone and b remains free, b inverse
# rescaling preserves b*T exactly. This says nothing about shape changes.
t=np.array([1.,2.,3.]);bias=.3;scale=1.07
ck('pure amplitude nuisance degeneracy',np.allclose((bias/scale)*(scale*t),bias*t))
result={'claim_id':'CE-FM-063','checks':checks,'n_checks':len(checks),'all_pass':all(z['pass'] for z in checks),'unit_dictionary_h':h,'fixed_mass_scores':scores,'stock_rows':rows,'805_saved':r805,'805_mutate_saved':m805,'sigma8':{'trapz_reduced_P':sg,'stored_discrete_mode_sum':snap['sigma8_grav'],'relative_difference':sg/snap['sigma8_grav']-1,'fundamental_k':2*np.pi/j['L'],'first_mean_k':float(k[0]),'scope':'Missing sub-fundamental modes cannot explain difference between these two same-box statistics; binning/quadrature and within-bin window weighting require comparison. No field/FFT rerun or repaired template.'},'scope':'Self-review. Census rule units reconciled against CFG416 callsite and fixed-mass lensing. No original grid fit, simulation, relativistic metric, unique catchment allocation or physical baryon phase derived.'}
Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'checks':len(checks),'all_pass':result['all_pass'],'scores':scores,'sigma8':result['sigma8']}))
