"""Independent70-digit scalar reconstruction; normalized compact root check."""
from pathlib import Path
import json,hashlib,bisect,math
import mpmath as m
import numpy as np
p=Path(__file__).resolve().parent;r=p.parents[1];reb=p.parent;files=[Path(__file__),p/'nonlinear_001/results.json',reb/'EM1_emergent_dust_law/em1_emergent_results.json',reb/'F3_growth_audit/f3_growth_audit_results.json',reb/'X43_collapse_core_floor/x43_collapse_core_results.json',reb/'X48_native_cf_zoom/x48_analyze_results_ng48_A2.json',p/'native_matrix_001/native_matrices.npz',p/'interval_001/results.json',p/'nonlinear_001/original_input_mass_vectors.npz',p/'mass_enclosure_001/outward_mass_vectors.npz'];sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest();hashes={str(f.relative_to(r)):sha(f) for f in files};J=lambda i:json.loads(files[i].read_text());d=J(1);em=J(2)['rows']['A_c2b_refit']['R1'];h=J(3)['K2']['A_c2b_refit']['params']['h'];raw=J(4)['sigma_coll_table'];shape=[J(5)['cf_by_mass'][k] for k in ['1e+12','1e+13','1e+14']];grid=np.load(files[6])['LMG'];old=J(7);m.mp.dps=70;M=lambda x:m.mpf(float(x));tab=sorted((m.log10(M(float(k))),m.log10(M(v[0]))) for k,v in raw.items());checks={};contained=0;rootok=[];branches=[];snap=[]
def interpolate(x,t,clamp):
 if clamp and x<=t[0][0]:return t[0][1]
 if clamp and x>=t[-1][0]:return t[-1][1]
 i=max(0,min(len(t)-2,bisect.bisect_right([q[0] for q in t],x)-1));a,b=t[i],t[i+1];return a[1]+(b[1]-a[1])*(x-a[0])/(b[0]-a[0])
def inside(x,s):
 lo,hi=map(m.mpf,s.strip('[]').split(','));return lo<=x<=hi
B=lambda x:m.log1p(x*x)+2*m.log1p(x)-2*m.atan(x);floor=M(9.3603e-11)*M(3.0857e16)/M(1e6)/(2*m.pi*M(4.30091e-3));ri=0;vectors=dict(np.load(files[8]));prior_vectors=dict(np.load(files[9]));mass_cases=0;point_misses=0;finite=0;radius_errors=[]
for row in d['rows']:
 idx=row['node'];lm=M(grid[idx]);Ms=m.power(10,lm);Mc=m.power(10,lm+M(-.69)*(lm-2*m.log10(M(.70)/M(.679)))+M(6.63));parent=m.power(10,M(em['a'])+M(em['b'])*(m.log10(Ms+Mc)-10));R=m.root(3*parent/(4*m.pi*200*(M(2.775e11)*M(h)**2/M(1e18))),3);lg=m.log10(parent);coll=m.power(10,interpolate(lg,tab,False));columns=[]
 for L in (M(3.75),M(3.751)):
  cf=interpolate(lg,[(M(i+12),L*M(v)/M(shape[2])) for i,v in enumerate(shape)],True);columns.append(4/(3*(3*m.log(2)-m.pi/2))*cf**m.mpf('1.25')*coll)
 values={'M':parent,'R':R,'Ms':Ms,'Mc':Mc,'column0':columns[0],'column1':columns[1],'floor':floor};assert all(inside(v,row[k]) for k,v in values.items());contained+=len(values);branches.append(bool(columns[0]>floor)==row['halo'] and bool(columns[1]>floor)==row['halo'])
 if row['halo']:
  rf=(3*float(parent)/(4*math.pi*200*(2.775e11*h**2/1e18)))**(1/3);radius_errors.append(abs(rf/old['root_brackets'][2*ri]['R']-1))
  for e,Sigma in enumerate(columns):
   br=old['root_brackets'][2*ri+e];target=parent/(m.pi*Sigma*R**2);xx=[R/M(br[k]) for k in ['r0_lower','r0_upper']];res=[B(x)/x**2-target for x in xx];ok=res[0]<0<res[1];rootok.append(bool(ok));assert ok==d['root_checks'][2*ri+e]['signs_pass']
  for e,Sigma in enumerate(columns):
   br=old['root_brackets'][2*ri+e];target=parent/(m.pi*Sigma*R**2);xl=R/M(br['r0_upper']);xh=R/M(br['r0_lower'])
   for _ in range(100):
    xm=(xl+xh)/2
    if B(xm)/xm**2>target:xl=xm
    else:xh=xm
   root=R/((xl+xh)/2)
   for k in (0,900,1800,2700,3600):
    radius=M(vectors['radius_pc'][k]);mb=Ms+Mc+Ms/2*min(1,(radius/M(1e5))**3);value=mb+parent*B(min(radius,R)/root)/B(R/root);lo=M(vectors['lower'][2*ri+e,k]);hi=M(vectors['upper'][2*ri+e,k]);assert lo<=value<=hi;mass_cases+=1
    if not M(prior_vectors['lower'][2*ri+e,k])<=value<=M(prior_vectors['upper'][2*ri+e,k]):point_misses+=1
  ri+=1
 if idx in (d['rows'][0]['node'],d['rows'][-1]['node']):snap.append(dict(node=idx,M=str(parent),R=str(R),column0=str(columns[0])))
for row in d['rows']:
 for k in ['M','R','Ms','Mc','column0','column1','floor','branch_gap_lower','branch_gap_upper']:
  assert all(m.isfinite(m.mpf(v)) for v in row[k].strip('[]').split(','));finite+=1
for row in d['root_checks']:
 for k in ['lower_residual','upper_residual','compact_h']:
  assert all(m.isfinite(m.mpf(v)) for v in row[k].strip('[]').split(','));finite+=1
checks['radius_point_reproduction']=len(radius_errors)==62 and max(radius_errors)<1e-12
checks['620_normalized_mass_points']=mass_cases==620;checks['all_recorded_intervals_finite']=finite==1515
checks.update(all889_coefficients_contained=contained==889,all127_branches=all(branches),all124_normalized_root_reviews=len(rootok)==124 and all(rootok),run_controls=all(d['checks'].values()),source_hashes=all(sha(r/f)==h for f,h in hashes.items()));result=dict(checks=checks,coefficient_comparisons=contained,max_radius_point_relative_error=max(radius_errors),selected_mass_comparisons=mass_cases,selected_exact_point_old_box_misses=point_misses,finite_intervals_checked=finite,normalized_root_signs_passed=sum(rootok),normalized_root_signs_total=len(rootok),selected_values=snap,input_sha256=hashes,scope='70digit scalar validation of directed analytic original-input gate; not solver/libm/continuum certification');(p/'nonlinear_review.json').write_text(json.dumps(result,indent=2)+'\n');print('checks',len(checks),all(checks.values()),'roots',sum(rootok));assert all(checks.values())
