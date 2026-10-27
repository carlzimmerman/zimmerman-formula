"""CE-FM-072: raw-table threshold certificate and bounded-input sensitivity."""
import json,math,sys
from pathlib import Path
import numpy as np
import sympy as s
p=Path('campaign_fresh_gravity/PARAMRED_2026-10-16/E_FREE');saved=json.loads((p/'e_free_results.json').read_text());raw=json.loads(Path('campaign_fresh_gravity/CFG317_baryon_loss_cold_mass/cfg317_baryon_loss_results.json').read_text())['numbers'];groups={'MW UFDs':'ufd','MW classicals':'cls','M31 (Collins)':'col','M31 (LVD)':'m31','LV field':'fld'};data={};pts=[]
for lab,key in groups.items():
 rows=[]
 for name,z in zip(raw['NAMES'][key],raw['EST']['-0.2|'+key]):
  if z is None:continue
  M=float(z['Ms'])+float(z.get('Mg') or 0);lr=None if z.get('lR') is None else float(z['lR']);rows.append((name,M,lr))
  if lr is not None:pts.append((math.log10(M),lr))
 data[lab]=rows
coef=np.polyfit(np.array(pts)[:,0],np.array(pts)[:,1],1);checks=[]
def ck(n,v):
 checks.append({'name':n,'pass':bool(v)})
 if not v:raise AssertionError(n)
ck('OLS source relation reproduced',np.allclose(coef,[saved['T1_relation']['slope'],saved['T1_relation']['icpt']],rtol=1e-12))
def speeds(a0):
 return {lab:sorted(((6.674e-11*1.989e30*M*10**max(0,lr if lr is not None else coef[0]*math.log10(M)+coef[1])*a0)**.25/1e3,nm) for nm,M,lr in rows) for lab,rows in data.items()}
results=[]
for foot,a0 in [('canonical',9.3603e-11),('alt',1.1312e-10)]:
 vs=speeds(a0);ufd=vs['MW UFDs'];k=math.ceil(.9*len(ufd));L=ufd[k-1][0];U=min(v[len(v)//10][0] for lab,v in vs.items() if lab!='MW UFDs');rec=saved['T1'][foot]
 ck('raw order-statistic window '+foot,abs(L-rec['L'])<1e-10 and abs(U-rec['U'])<1e-10 and L>U)
 eps=(L-U)/(L+U)
 ck('bounded uncertainty closed below radius '+foot,L*(1-(eps-1e-6))>U*(1+(eps-1e-6)))
 e=eps+1e-6;low=L*(1-e);up=U*(1+e);T=(low+up)/2
 shifted={lab:[v*((1-e) if lab=='MW UFDs' else (1+e)) for v,nm in arr] for lab,arr in vs.items()}
 ck('explicit feasible shifted data above radius '+foot,sum(v<T for v in shifted['MW UFDs'])>=k and all(sum(v<T for v in arr)<=len(arr)//10 for lab,arr in shifted.items() if lab!='MW UFDs'))
 for scale in [.5,2.,10.]:ck('common rescaling cannot open window '+foot+str(scale),scale*L>scale*U)
 results.append({'foot':foot,'L_kms':L,'U_kms':U,'threshold_setter_low':rec['L_who'],'threshold_setter_upper':rec['U_who'],'ratio_L_U':L/U,'min_symmetric_fractional_velocity_perturbation_to_touch':eps,'one_population_velocity_multiplier_to_touch':L/U,'one_population_MbRind_multiplier_to_touch':(L/U)**4,'two_population_product_multipliers_at_touch':[(1-eps)**4,(1+eps)**4],'log_velocity_radius':.5*math.log(L/U),'explicit_threshold_at_epsilon_plus1e-6':T})
ck('footing change leaves ratio invariant',abs(results[0]['ratio_L_U']-results[1]['ratio_L_U'])<1e-12)
# Unit exponents are L,M,T rows, columns G,a0,Mb and optional Sigma,c_s.
D=s.Matrix([[3,1,0],[-1,0,1],[-2,-2,0]])
ck('G a0 Mb no dimensionless invariant',len(D.nullspace())==0)
Ds=D.row_join(s.Matrix([-2,1,0]));ns=Ds.nullspace();ck('surface density admits one invariant',len(ns)==1 and Ds*s.Matrix([1,-1,0,1])==s.zeros(3,1))
Dsc=Ds.row_join(s.Matrix([1,0,-1]));ck('surface plus sound speed admits two invariants',len(Dsc.nullspace())==2 and Dsc*s.Matrix([1,1,1,0,-4])==s.zeros(3,1))
out={'claim_id':'CE-FM-072','n_checks':len(checks),'all_pass':all(z['pass'] for z in checks),'checks':checks,'raw_objects':{lab:len(rows) for lab,rows in data.items()},'threshold_results':results,'dimensionless_invariants':['G Sigma_bar / a0','G Mb a0 / c_s^4'],'scope':'Conditional deterministic selector certificate and perturbation radius; no empirical error distribution or posterior probability, new threshold fit, selector amendment, or physical free-population mechanism derived.'}
Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='checks'}))
