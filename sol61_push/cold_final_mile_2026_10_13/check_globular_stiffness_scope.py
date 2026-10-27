"""CE-FM-073: reproduce conditional GC criterion; test null and total boost."""
import json,math,sys
from pathlib import Path
import numpy as np
from scipy.optimize import brentq
p=Path('campaign_fresh_gravity/CFG820_stiffness_from_globulars');rec=json.loads((p/'cfg820_results.json').read_text());mut=json.loads((p/'cfg820_results_MUTATE.json').read_text());GC=json.loads(Path('campaign_fresh_gravity/CFG332_globulars_three_routes/cfg332_globulars_results.json').read_text())['clusters'];checks=[]
def ck(n,v):
 checks.append({'name':n,'pass':bool(v)})
 if not v:raise AssertionError(n)
G,ms,pc=6.674e-11,1.989e30,3.0857e16
knots=np.array([.01,.1,.3,1,3,10,100,1000]);vals=np.array([.005,.048,.134,.358,.663,.894,.990,.998999])
def screen(x):
 if x<=.01:return x/2
 if x>=1000:return 1-1/x
 return float(np.interp(np.log(x),np.log(knots),vals))
nu=lambda y:1/(-math.expm1(-math.sqrt(max(y,1e-12))))
def parts(g,a0,L,mutation=False):
 M=1.6*g['LV'];r=4/3*g['rhl']*pc;sN=math.sqrt(G*M*ms/(8*g['rhl']*pc))/1000
 yi=G*M*ms/(2*r*r*a0);ye=G*6e10*ms/((g['RGC']*1000*pc)**2*a0);B=nu(yi+ye)
 S=(1 if mutation else screen(2*(r/pc)*math.sqrt(G*M*ms/a0)/pc/L**2)) if L is not None else 0
 return sN*math.sqrt(1+S*(B-1)),sN,B,S
def chi(gcs,a0,L,mutation=False):
 return sum((math.log(g['so']/parts(g,a0,L,mutation)[0]))**2/((g['eso']/g['so'])**2+(math.log(10)*.15/2)**2) for g in gcs)
grid=np.geomspace(5.75,3000,400);rows=[]
for lab,gs in [('primary (no Pal 3)',[g for g in GC if g['name']!='Pal 3']),('all four',GC)]:
 for foot,a0 in [('canonical',9.3603e-11),('alt',1.1312e-10)]:
  v=np.array([chi(gs,a0,L) for L in grid]);cN=chi(gs,a0,None);minimum=min(v.min(),cN);idx=np.where(v-minimum<=3.84)[0];L=float(grid[idx[0]]);old=rec[lab+'|'+foot]
  ck('grid criterion '+lab+foot,np.isclose(L,old['L95'],rtol=1e-13) and np.isclose(minimum,old['chi2_min'],rtol=1e-12))
  root=brentq(lambda L:chi(gs,a0,L)-minimum-3.84,grid[idx[0]-1],L)
  vm=np.array([chi(gs,a0,L,True) for L in [5.75,24,1000,3000]])
  ck('mutation independent of L '+lab+foot,np.ptp(vm)<1e-12)
  ck('mutation saved null misminimum '+lab+foot,np.isclose(mut[lab+'|'+foot]['chi2_min'],cN) and cN<vm[0] and math.isnan(mut[lab+'|'+foot]['L95']))
  ck('correct mutation own profile flat '+lab+foot,np.max(abs(vm-vm.min()))<1e-12)
  rows.append({'sample':lab,'foot':foot,'saved_grid_L_pc':L,'continuous_crossing_same_frozen_grid_minimum_pc':root,'chi2_min':minimum,'chi2_newton':cN,'constant_mutation_chi2':float(vm[0]),'mutation_actual_profile_minimum':float(vm[0]),'mutation_all_delta_chi2_zero':True})
  for g in gs:
   got,sN,B,S=parts(g,a0,1e9);ck('all-cluster Newton limit '+lab+foot+g['name'],abs(got/sN-1)<1e-10)
L=rec['primary (no Pal 3)|canonical']['L95'];ufd=[];a0=9.3603e-11
for M in [1e3,1e4]:
 for rh in [20.,40.]:
  radius=4/3*rh;rm=math.sqrt(G*M*ms/a0)/pc;ss=2*radius*rm/L**2;S=screen(ss);B=nu(rm**2/(2*radius**2));effective=1+S*(B-1)
  ck('small S not total-boost suppression '+str(M)+str(rh),S<.31 and effective>1.5)
  ck('isolated residual bounded by unscreened '+str(M)+str(rh),1<=effective<=B)
  ufd.append({'Mb_Msun':M,'projected_rh_pc':rh,'S':S,'isolated_Blaw':B,'isolated_effective_variance_boost':effective,'isolated_sigma_over_Newton':math.sqrt(effective),'meaning':'No host EFE, same algebraic screening/estimator; not a new Jeans/PDE fit or observed UFD inference.'})
ck('source K1 explicitly bypassed in mutation','or MUT' in (p/'cfg820.py').read_text())
out={'claim_id':'CE-FM-073','n_checks':len(checks),'all_pass':all(z['pass'] for z in checks),'checks':checks,'GC_criterion_replay':rows,'UFD_boost_countercontrols':ufd,'conditional_wide_binary_envelope_at50kAU':.5*((50000/206264.806247)/L)**2,'scope':'Criterion-defined proxy likelihood replay, not calibrated95%coverage or full finite-stiffness action solution. Corrected mutation interpretation and full boost algebra; no original survey data/model generation, new fit or source change.'}
Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ['checks','scope']}))
