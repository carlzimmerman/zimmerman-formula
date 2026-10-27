"""CE-FM-069: gas-profile aperture dictionary and ACCEPT ratio influences."""
from pathlib import Path
import json,math,sys
import numpy as np
from scipy.integrate import quad
b=Path('sol61_push/cold_final_mile_2026_10_13');d=b/'outskirt_stack_inputs';raw=np.load(d/'cfg687_percluster.npz',allow_pickle=False);cl=json.loads((d/'cfg686_results.json').read_text())['clusters'];checks=[]
def ck(n,v):
 checks.append({'name':n,'pass':bool(v)})
 if not v:raise AssertionError(n)
rc=.15*raw['R500'];rm=np.minimum(2.2*raw['R500'],2.8)
B=lambda r:r-rc*np.arctan(r/rc)
A=rm**3/(rm**2+rc**2)
newP=B(rm)+A*np.log(3/rm)
newF=B(rm)+A*np.log(np.minimum(3,2*rm)/rm)+A/(2*rm)*np.maximum(3-2*rm,0)
ratios={'P':newP/B(3.),'F':newF/B(3.)}
for prof in ['P','F']:
 ck('new profile gas3 below old beta '+prof,np.all((ratios[prof]>0)&(ratios[prof]<1)))
 for i in [0,79,159,239,317]:
  rci=float(rc[i]);rmi=float(rm[i])
  def dens_r2(r):
   if r<=rmi:return r*r/(r*r+rci*rci)
   if prof=='F' and r>2*rmi:return rmi*rmi/(2*(rmi*rmi+rci*rci))
   return rmi**3/(rmi*rmi+rci*rci)/r
  bounds=[0,rmi]+([2*rmi] if prof=='F' and 2*rmi<3 else [])+[3.]
  mass=sum(quad(dens_r2,l,h,epsabs=1e-12)[0] for l,h in zip(bounds[:-1],bounds[1:]));old=3-rci*math.atan(3/rci)
  ck('analytic mass vs direct profile quadrature '+prof+str(i),abs(mass/old-ratios[prof][i])<1e-10)
mg=raw['mg'];cut=np.quantile(mg,[1/3,2/3]);tercs=[mg<=cut[0],(mg>cut[0])&(mg<=cut[1]),mg>cut[1]]
gasrows={};stackrows=[]
Da=np.nan_to_num(np.array([v['dsig'] for v in cl]));Ea=np.array([v['err'] for v in cl]);W=np.where(np.isfinite(Ea)&(Ea>0),1/Ea**2,0);outer=[6,7];boot=np.random.default_rng(1).integers(0,8,size=(1000,8))
for prof in ['P','F']:
 rec=json.loads((d/f'cfg815_results_{prof}.json').read_text());ER=np.load(d/f'erass_{prof}.npy',allow_pickle=True);AC=np.load(d/f'accept_{prof}.npy',allow_pickle=True)
 f=np.array([o['s|canonical|EX']['meta']['fret'] for o in ER]);rel=np.median(np.abs(np.array([o['M0']['mono|canonical'] for o in ER])/raw['PL']-1),axis=0)
 ck('saved failed additional M0 '+prof,rel.max()>.01 and rec['checks']['M0 eRASS1 plain law reproduces CFG687 PL']['ok'] is False)
 ck('frozen overall FAIL retained '+prof,rec['verdict']=='FAIL')
 gasrows[prof]={'new_over_old_gas3_range':[float(ratios[prof].min()),float(np.median(ratios[prof])),float(ratios[prof].max())],'terciles':[{'n':int(t.sum()),'median_new_over_old_gas3':float(np.median(ratios[prof][t])),'n_retention_capped_at1':int(np.sum(f[t]==1)),'median_cached_fret':float(np.median(f[t]))} for t in tercs],'cached_additional_M0_relative_difference_per_band':rel.tolist()}
 for mode in ['EX','ALL']:
  key='s|canonical|'+mode;pred=np.array([o[key]['base']+o[key]['res'] for o in AC]);num=(W[:,outer]*Da[:,outer]).sum(1);den=(W[:,outer]*pred[:,outer]).sum(1)
  ck('positive model denominators '+prof+mode,np.all(den>0))
  total=float(num.sum()/den.sum());Ai=num/den;q=den/den.sum();iv=W[:,outer].sum(1)/W[:,outer].sum()
  ck('exact stacked ratio convex combination '+prof+mode,abs(total-q@Ai)<1e-13)
  std=float(np.std(num[boot].sum(1)/den[boot].sum(1)))
  ck('saved ACCEPT OUTER and bootstrap '+prof+mode,np.allclose([total,std],rec['T_A'][key]['A']['OUTER'],rtol=1e-11))
  rows=[]
  for i in range(8):
   loo=(num.sum()-num[i])/(den.sum()-den[i]);influence=q[i]*(total-Ai[i])/(1-q[i])
   ck('LOO exact influence '+prof+mode+str(i),abs(loo-total-influence)<1e-13)
   rows.append({'name':cl[i]['name'],'z':cl[i]['z'],'own_A':float(Ai[i]),'inverse_variance_fraction':float(iv[i]),'ratio_denominator_fraction_q':float(q[i]),'LOO_A':float(loo),'LOO_change':float(influence)})
  group=np.array([v['name'].startswith('2PIGG') for v in cl]);without=float(num[~group].sum()/den[~group].sum())
  stackrows.append({'profile':prof,'model':mode,'A':total,'bootstrap_sigma':std,'two_groups_inverse_variance_fraction':float(iv[group].sum()),'two_groups_denominator_fraction':float(q[group].sum()),'A_without_two_groups_posthoc':without,'clusters':rows})
out={'claim_id':'CE-FM-069','n_checks':len(checks),'all_pass':all(x['pass'] for x in checks),'checks':checks,'gas_profile_diagnostics':gasrows,'ACCEPT_ratio_influences':stackrows,'scope':'Cached score/normalization audit. Frozen rule and FAIL unchanged. Posthoc deletion not a new verdict or evidence of identified selection causality; no original model generation, eRASS full score rerun, or primary outskirt-slope authentication.'}
Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'checks':len(checks),'all_pass':out['all_pass'],'gas':gasrows,'stacks':[{k:v for k,v in z.items() if k!='clusters'} for z in stackrows]}))
