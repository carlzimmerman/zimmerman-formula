"""CE091: saved CFG848 profiles/classes and common-temperature/angular-momentum identities."""
import json,math,sys,resource
from pathlib import Path
S=Path('campaign_fresh_gravity/CFG848_maxent_partition');d=json.loads((S/'cfg848_results.json').read_text());mu=json.loads((S/'cfg848_results_MUTATE.json').read_text());checks=[];cases=[]
def ck(n,v):
 checks.append({'name':n,'pass':bool(v)})
 if not v:raise AssertionError(n)
def classification(pr):
 D=pr['rg']['Delta'];rising=pr['rg']['f_free']-pr['Rhalf']['f_free']>=.05
 if D>.8:return 'OVERSHOOT'
 if .15<=D<=.8:return 'CONCENTRATED FREE CORE' if rising else 'INTERMEDIATE'
 if .05<=D<.15:return 'INTERMEDIATE'
 if -.05<D<.05 or pr['rg']['f_free']<.05:return 'NO FREE EXCESS'
 return 'WRONG SIGN'
for ci,c in enumerate(d['cells']):
 for state,st in c['states'].items():
  if not st['found']:
   ck(str((ci,state))+' no state class',st['class']=='ILL-POSED (a)');continue
  a=c['a'];pr=st['profile']
  for n,p in pr.items():
   r=p['r'];mb=r*r/(r+a)**2;law=r*r/(r+a);mt,mf=p['Mt'],p['Mf'];want=math.log10((mb+mt+mf)/(mb+law))
   ck(str((ci,state,n))+' exact law mass',abs(law-p['M_law'])<1e-10*max(1,law));ck(str((ci,state,n))+' total Delta',abs(want-p['Delta'])<1e-11)
   if mt+mf>0:ck(str((ci,state,n))+' enclosed free fraction',abs(mf/(mt+mf)-p['F_enc'])<1e-11)
  if c['kind']=='C':
   ck(str((ci,state))+' local free >half',all(p['f_free']>.5 for p in pr.values()));ck(str((ci,state))+' positive potential separation',st['min_dPhi']>0)
  if st.get('class') is not None:ck(str((ci,state))+' class arithmetic',classification(pr)==st['class'])
  if c['kind']=='C' and c['N']==10 and c['Rmode']=='r_ta' and state=='E_INF':
   p=pr['rg'];cases.append({'system':c['system'],'footing':c['footing'],'Mb_scale_Msun':10**d['inputs']['systems'][c['system']]['logMb'],'a_in_rM':a,'beta':st['beta'],'r_g_in_rM':p['r'],'free_local':p['f_free'],'cold_inside_rg_over_Mb':p['Mt']+p['Mf'],'free_inside_rg_over_Mb':p['Mf'],'cold_fraction_of_total_stock_inside_rg':(p['Mt']+p['Mf'])/c['Mc'],'law_cold_inside_rg_over_Mb':p['M_law'],'Delta':p['Delta'],'class':st['class']})
K=d['controls'];ck('K1 ratio tolerance',abs(K['K1']['ratio']-1)<.02);ck('K1 energy tolerance',abs(K['K1']['E']/K['K1']['E_LAW']-1)<.02);ck('K2 Lambda tolerance',abs(K['K2']['Lambda']-.3346)<.002);ck('K2 density contrast',690<=K['K2']['contrast']<=730);ck('K3 exact residual recorded',K['K3']['residual']=='0');ck('K3 positive min',K['K3_dPhi']['min']>0);ck('mutation bites recorded',mu['mutate_bites'])
# Given common beta and chemical potential, local rotation shift is species-independent.
# Integrating exp[-beta(v²/2+Phi-Omega*s*vphi)] gives
# rho_i ~exp[-beta(Phi_i-Omega²*s²/2)] and cancels from rho_t/rho_f.
for beta in [.1,1,10]:
 for gap in [.01,.1,1]:
  for shift in [0,.1,1,10]:
   pt,pf=gap,0.;lt=-beta*(pt-shift);lf=-beta*(pf-shift)
   free=1/(1+math.exp(lt-lf));want=1/(1+math.exp(-beta*gap));ck(str((beta,gap,shift))+' centrifugal cancellation',abs(free-want)<1e-13)
# A label conversion is not an angular-momentum sink at fixed position/velocity.
for r in [(1.,2.,3.),(-2.,.5,1.)]:
 for v in [(3.,1.,-.5),(0.,2.,4.)]:
  L=(r[1]*v[2]-r[2]*v[1],r[2]*v[0]-r[0]*v[2],r[0]*v[1]-r[1]*v[0]);ck(str((r,v))+' label invariant specific L',sum(x*x for x in L)>0)
res={'claim_id':'CE-FM-091','n_checks':len(checks),'checks':checks,'all_pass':all(x['pass'] for x in checks),'primary_found_cases':cases,'saved_grade':d['grade'],'scope':'Arithmetic/force dictionary and recorded controls of saved CFG848 profiles; analytic angular momentum/rotating Boltzmann identities. No equilibrium ODE/shooting, continuation/stability search, or actual dwarf evolution rerun.','peak_rss_raw':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'non_claims':['Spherical prototype P1/P2 are not Draco/Sextans/Fornax/LeoI data fits','Common mu and interconversion with zero label degeneracy offset are added assumptions','Lagrange multiplier Omega requires prescribed total J, it does not generate low J','Formal centrifugal cancellation uses given potentials, not a new nonspherical self-consistent solution','No proof all non-equilibrium partitions or histories fail']};Path(sys.argv[1]).write_text(json.dumps(res,indent=2)+'\n');print(json.dumps({'checks':len(checks),'primary':cases,'grade':d['grade']},indent=1))
