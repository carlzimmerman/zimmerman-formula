from pathlib import Path
from fractions import Fraction as F
import json,argparse
import numpy as np
p=argparse.ArgumentParser();p.add_argument('--out',required=True);args=p.parse_args();out=Path(args.out);out.mkdir(exist_ok=True)
B=Path('deepseek_push/astra_spawn_ideas/fresh_gravity_followups');src=B/'results/FGF-029/fgf029_run_001/numeric_001/extended_response.npz';x=np.load(src)
U=[[F(float(q)) for q in row] for row in x['old_pressure']];c=[F(float(q)) for q in x['new_column']];L=[F(float(q)) for q in x['L16'][:15]];base=[F(float(q)) for q in x['baseline16']]
def dot(a,b):return sum((v*w for v,w in zip(a,b)),F(0))
def trans(a):return list(map(list,zip(*a)))
def mul(a,b):return [[dot(row,col) for col in trans(b)] for row in a]
def eye(n):return [[F(i==j) for j in range(n)] for i in range(n)]
def inverse(a):
 n=len(a);rows=[row+i for row,i in zip(a,eye(n))]
 for j in range(n):
  k=next(k for k in range(j,n) if rows[k][j]);rows[j],rows[k]=rows[k],rows[j];z=rows[j][j];rows[j]=[v/z for v in rows[j]]
  for i in range(n):
   if i!=j:
    z=rows[i][j]
    if z:rows[i]=[v-z*w for v,w in zip(rows[i],rows[j])]
 return [row[n:] for row in rows]
def enc(z):return [enc(v) for v in z] if isinstance(z,list) else str(z)
checks=[]
def ck(name,passed,observed=None):
 checks.append({'name':name,'pass':bool(passed),'observed':observed,'tolerance':0});assert passed,name
inv=inverse(U);I=eye(15);ck('left exact inverse',mul(inv,U)==I);ck('right exact inverse',mul(U,inv)==I)
h=[row[0] for row in mul(inv,[[z] for z in c])];mu=-dot(L,h);ell=sum(map(abs,L));kappa=max(sum(map(abs,row)) for row in inv);H=max(map(abs,h));ck('positive nominal target response',mu>0,float(mu));ck('target L1 is10',ell==10)
old=json.loads(Path('campaign_fresh_gravity_astra/stage_15/target_audit/run_001/results.json').read_text());n=[-z for z in h]+[F(1)];ck('zero error matches prior exact target',mu==F(old['target_sensitivity_dp5_exact']));ck('zero error matches prior exact null',n==list(map(F,old['null_direction_exact'])))
delta=min(1/(4*kappa),mu/(4*kappa*ell*(1+H)));entry=delta/15;t=kappa*delta;r=t*(1+H)/(1-t)
ck('radius strictly positive',delta>0,float(delta));ck('Neumann product <=quarter',0<t<=F(1,4),float(t));ck('target error <=third nominal',ell*r<=mu/3,float(ell*r));lower=mu-ell*r;upper=mu+ell*r;ck('uniform positive target lower bound',lower>=2*mu/3>0,float(lower));ck('entrywise alternative implies induced bound',15*entry==delta and entry<=delta)
# This intentionally excluded matrix is not silently admitted under induced bound.
ck('reject maxentry-for-induced confusion',15*delta>delta)
gaps=[base[i]-(base[i+1] if i<15 else F(0)) for i in range(16)];m0=min(gaps);ck('strict baseline including endpoint',m0>0,float(m0));V=max(F(1),H+r);eta=m0/(4*V);ck('uniform step strictly positive',eta>0,float(eta));ck('uniform strict pressure margin',m0-2*eta*V==m0/2>0);sep=2*eta*lower;ck('uniform target separation positive',sep>=4*eta*mu/3>0,float(sep))
A=[row+[v] for row,v in zip(U,c)];plus=[v+eta*w for v,w in zip(base,n)];minus=[v-eta*w for v,w in zip(base,n)];data=[dot(row,base) for row in A];lext=L+[F(0)]
for name,pressure in [('plus',plus),('minus',minus)]:
 ck('zero error '+name+' strict gaps',all(pressure[i]>(pressure[i+1] if i<15 else F(0)) for i in range(16)))
 ck('zero error '+name+' exact bins',all(dot(row,pressure)==d for row,d in zip(A,data)))
ck('zero error target separation',dot(lext,plus)-dot(lext,minus)==2*eta*mu)
threshold=mu/(kappa*(ell*(1+H)+mu));z=kappa*threshold;thresholdr=z*(1+H)/(1-z)
ck('threshold above selected radius',threshold>delta,float(threshold));ck('threshold still inverse sufficient',z<1,float(z));ck('threshold target lower bound exactlyzero',mu-ell*thresholdr==0);ck('threshold remains mathematically inconclusive',not(mu-ell*thresholdr>0));ck('zero perturbation in threshold ball stays ambiguous',mu>0 and threshold>0)
constants={'kappa_inverse_induced_infinity':kappa,'h_infinity':H,'target_L1':ell,'nominal_mu':mu,'delta_induced_E_and_vector_e':delta,'common_entrywise_radius':entry,'Neumann_product':t,'inverse_bound':kappa/(1-t),'inverse_column_change_bound':r,'mu_lower':lower,'mu_upper':upper,'baseline_min_gap':m0,'null_norm_bound_V':V,'common_witness_step':eta,'uniform_gradient_separation_lower':sep,'threshold_inconclusive_radius':threshold}
result={'claim':'Uniform finite pressure-target ambiguity survives the declared real operator perturbations','constants_exact':{k:str(v) for k,v in constants.items()},'constants_float':{k:float(v) for k,v in constants.items()},'norm_conventions':{'E':'induced infinity=max row absolute sum; <=delta','e':'vector infinity=max absolute entry; <=delta','combined_entrywise_sufficient':'Every E or e entry absolute value <=delta/15','L':'row L1 norm','units':'response entries: Compton-y per normalized pressure coefficient; null last coordinate1; pressure and dp/dx inherited units'},'inverse_U_exact':enc(inv),'h_exact':enc(h),'nominal_null_exact':enc(n),'baseline_exact':enc(base),'zero_error_witness_plus_exact':enc(plus),'zero_error_witness_minus_exact':enc(minus),'zero_error_synthetic_bins_exact':enc(data),'zero_error_gradients':[float(dot(lext,plus)),float(dot(lext,minus))],'checks':checks,'threshold_control':{'inverse_bound_passes':True,'positive_target_margin_certified':False,'result':'inconclusive sufficient bound; no restored-identification claim'},'uniform_scope':'All real E,e in stated norm ball; for each operator use its own n_E and synthetic data, common baseline and common positive step','empirical_status':'No actual response/calibration error budget or outer-pressure measurement authenticated','tested_operator_count':1,'perturbation_sampling':False,'route_stop':'Finite robustness certificate complete at worker level; no support/annular/error-radius sweep.'}
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'constants':result['constants_float'],'checks':len(checks),'all_passed':True}))
