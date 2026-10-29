"""Original-input analytic nonlinear membership gate; no observational regrade."""
import os
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[k]='1'
from pathlib import Path
import argparse,hashlib,json,math,time
import numpy as np
from mpmath import iv
p=Path(__file__).resolve().parent;r=p.parents[1];reb=p.parent;ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);out=Path(ap.parse_args().output);out.mkdir(parents=True,exist_ok=True);iv.dps=50;t0=time.monotonic()
paths=[Path(__file__),p/'NONLINEAR_001_CRITERIA.md',p/'nonlinear_contract.json',p/'projection_anchor_001/x53_on_shpS9_L3.75_corrected_own/x62_x53copy_1.executed.py',reb/'EM1_emergent_dust_law/em1_emergent_results.json',reb/'F3_growth_audit/f3_growth_audit_results.json',reb/'X43_collapse_core_floor/x43_collapse_core_results.json',reb/'X48_native_cf_zoom/x48_analyze_results_ng48_A2.json',reb/'CL3_one_number/cl3_one_number.py',reb/'F2_outer_lensing/f2_outer_lensing.py',p/'interval_001/results.json',p/'native_matrix_001/native_matrices.npz',p/'mass_enclosure_001/outward_mass_vectors.npz',p/'projection_anchor_001/projection_primitive_enclosures.npz',p/'signed_dot_002_cached/signed_map_evidence.npz']
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest();hashes={str(f.relative_to(r)):sha(f) for f in paths};read=lambda i:json.loads(paths[i].read_text());em=read(4)['rows']['A_c2b_refit']['R1'];bg=read(5)['K2']['A_c2b_refit']['params'];collapse=read(6)['sigma_coll_table'];shape=[read(7)['cf_by_mass'][k] for k in ['1e+12','1e+13','1e+14']];old=read(10);nat=dict(np.load(paths[11]));mass=dict(np.load(paths[12]));proj=dict(np.load(paths[13]));signed=dict(np.load(paths[14]));checks={};ck=lambda k,v:checks.update({k:bool(v)});J=lambda x:iv.mpf(float(x));log10=lambda x:iv.log(x)/iv.log(10);power10=lambda x:iv.exp(x*iv.log(10));B=lambda x:iv.log(1+x*x)+2*iv.log(1+x)-2*iv.atan2(x,iv.mpf(1));pack=lambda x:str(x);nodes=old['nodes'];active=np.flatnonzero(np.any(nat['weights']>0,axis=0));ck('inventory',len(nodes)==127 and np.array_equal(active,np.array([n['i'] for n in nodes])));src=paths[3].read_text();ck('source_formulas',all(v in src for v in ['lM200 = bg["a"] + bg["b"] * (logMbrel - 10.0)','M200 / (4 * math.pi * 200 * rhoc)','sc = eta_of(M200, cfg_h["cf"]) * sigma_coll(M200)','return LENS_RECORD(','LF_M(Mb, Mh, RGRID_PC','"linear" if (halo and LAST["law"]) else "const"']));ck('shape_source',all(v in paths[8].read_text() for v in ['return [L * v / c[2] for v in c]','_A2["cf_by_mass"][k]']));ck('constants_source',all(v in paths[9].read_text() for v in ['9.3603e-11','4.30091e-3','3.0857e16 / 1e6']))
# Tables rebuilt from original raw columns, not saved SC_LM/SC_LS outputs.
ct=sorted((float(k),float(v[0])) for k,v in collapse.items());cx=[log10(J(x)) for x,y in ct];cy=[log10(J(y)) for x,y in ct];sx=[J(12),J(13),J(14)];B1=3*iv.log(2)-iv.pi/2;floor=J(9.3603e-11)*J(3.0857e16)/J(1e6)/(2*iv.pi*J(4.30091e-3));rhoc=J(2.775e11)*J(bg['h'])**2/J(1e18);rows=[];roots=[];uncertain=[];coeff=[];point_errors=[];branch_events=[];mutation=False

def interp(x,xs,ys,clamp):
 # For a strict single segment, interval coefficients contain the exact map.
 if x.b<xs[0].a:
  return ys[0] if clamp else ys[0]+(ys[1]-ys[0])/(xs[1]-xs[0])*(x-xs[0])
 if x.a>xs[-1].b:
  return ys[-1] if clamp else ys[-1]+(ys[-1]-ys[-2])/(xs[-1]-xs[-2])*(x-xs[-1])
 for j in range(len(xs)-1):
  if x.a>=xs[j].b and x.b<=xs[j+1].a:return ys[j]+(ys[j+1]-ys[j])/(xs[j+1]-xs[j])*(x-xs[j])
 # Exact knots handled by a hull of adjacent full interval expressions.
 candidates=[]
 for j in range(len(xs)-1):
  if x.b>=xs[j].a and x.a<=xs[j+1].b:candidates.append(ys[j]+(ys[j+1]-ys[j])/(xs[j+1]-xs[j])*(x-xs[j]))
 assert candidates;return iv.mpf([min(v.a for v in candidates),max(v.b for v in candidates)])

for ni,node in enumerate(nodes):
 idx=node['i'];lm=J(nat['LMG'][idx]);Ms=power10(lm);Mc=power10(lm+J(-.69)*(lm-2*log10(J(.70)/J(.679)))+J(6.63));M=power10(J(em['a'])+J(em['b'])*(log10(Ms+Mc)-10));R=(3*M/(4*iv.pi*200*rhoc))**(iv.mpf(1)/3);lgM=log10(M);coll=power10(interp(lgM,cx,cy,False));sy=[J(3.75)*J(v)/J(shape[2]) for v in shape];cf=interp(lgM,sx,sy,True);columns=[]
 for L in (J(3.75),J(3.751)):
  sy=[L*J(v)/J(shape[2]) for v in shape];cf=interp(lgM,sx,sy,True);columns.append(4/(3*B1)*cf**(iv.mpf(5)/4)*coll)
 if columns[0].a>floor.b:halo=True
 elif columns[1].b<=floor.a:halo=False
 else:halo=None;branch_events.append(idx)
 ck(f'branch_matches_{idx}',halo==node['halo']);rows.append(dict(node=idx,M=pack(M),R=pack(R),Ms=pack(Ms),Mc=pack(Mc),column0=pack(columns[0]),column1=pack(columns[1]),floor=pack(floor),halo=halo,branch_gap_lower=pack(columns[0]-floor),branch_gap_upper=pack(columns[1]-floor)));coeff.append((Ms,Mc,M,R,columns,halo))
 # Original binary64 construction control, distinct from analytic enclosure.
 lmf=nat['LMG'][idx];ms=10**lmf;mc=10**(lmf+(-.69*(lmf-2*np.log10(.70/.679))+6.63));mf=10**(em['a']+em['b']*(math.log10(ms+mc)-10));rf=(3*mf/(4*math.pi*200*(2.775e11*bg['h']**2/1e18)))**(1/3);xx=math.log10(mf);cxx=np.array([math.log10(x) for x,y in ct]);cyy=np.array([math.log10(y) for x,y in ct]);j=int(np.clip(np.searchsorted(cxx,xx)-1,0,len(cxx)-2));sc=10**(cyy[j]+(cyy[j+1]-cyy[j])/(cxx[j+1]-cxx[j])*(xx-cxx[j]));cf=float(np.interp(xx,[12.,13.,14.],[3.75*v/shape[2] for v in shape]));col=4/(3*(3*math.log(2)-math.pi/2))*cf**1.25*sc;fl=9.3603e-11*3.0857e16/1e6/(2*math.pi*4.30091e-3);point_errors.extend([abs(mf/node['M']-1),abs(col/node['column']-1),abs(fl/node['floor']-1)])
 if halo:
  ri=sum(1 for n in nodes[:ni] if n['halo'])
  for e in (0,1):
   br=old['root_brackets'][2*ri+e];rl,rh=J(br['r0_lower']),J(br['r0_upper']);sg=columns[e];lo=iv.pi*sg*rl**2*B(R/rl)-M;hi=iv.pi*sg*rh**2*B(R/rh)-M;compact=4*(R/rh)**3/((1+R/rh)*(1+(R/rh)**2)*B(R/rh));ok=bool(lo.b<0 and hi.a>0 and compact.b<2 and compact.a>0);roots.append(dict(node=idx,endpoint=e,lower_residual=pack(lo),upper_residual=pack(hi),compact_h=pack(compact),signs_pass=ok))
   if not ok:uncertain.append(dict(node=idx,endpoint=e))
   if not mutation:mutation=bool((iv.pi*sg*J(1.01)*rl**2*B(R/rl)-M).a>0)
ck('point_reproduction',max(point_errors)<1e-12);ck('all_coefficients_finite',all(np.isfinite([float(v.a),float(v.b)]).all() for row in coeff for v in (*row[:4],*row[4])));ck('root_coverage',len(roots)==124);ck('wrong_column_mutation',mutation);ck('inputs_stable',all(sha(r/f)==h for f,h in hashes.items()));gate=not(branch_events or uncertain);mass_result={'attempted':False,'reason':'Original coefficient intervals fail existing root bracket gate' if uncertain else 'Branch uncertainty' if branch_events else 'Root gate passed; mass propagation required'}
if gate:
 rg=mass['radius_pc'];lower=np.empty((124,len(rg)));upper=np.empty_like(lower);halo_j=0;misses=0;max_miss=0.;law_nonzero=0;law_max=0.;outward=True
 for ni,node in enumerate(nodes):
  Ms,Mc,M,R,columns,halo=coeff[ni]
  if not halo:
   for k,radius in enumerate(rg):
    rr=J(radius);hot=iv.mpf(1) if radius>=1e5 else (rr/J(1e5))**3;mb=Ms+Mc+Ms/2*hot;y=J(4.30091e-3)*mb/rr**2/(J(9.3603e-11)*J(3.0857e16)/J(1e6));law=mb*(iv.mpf('.5')+iv.sqrt(iv.mpf('.25')+1/y));saved=J(proj['node_mass'][ni,k]);diff=law-saved
    if not diff.a<=0<=diff.b:law_nonzero+=1
    law_max=max(law_max,abs(float(diff.a)),abs(float(diff.b)))
   continue
  for endpoint in (0,1):
   j=2*halo_j+endpoint;br=old['root_brackets'][j];rl,rh=J(br['r0_lower']),J(br['r0_upper']);sg=columns[endpoint]
   for k,radius in enumerate(rg):
    rr=J(radius);hot=iv.mpf(1) if radius>=1e5 else (rr/J(1e5))**3;mb=Ms+Mc+Ms/2*hot;tt=iv.mpf([min(rr.a,R.a),min(rr.b,R.b)]);lo=mb+iv.pi*sg*rl**2*B(tt/rh);hi=mb+iv.pi*sg*rh**2*B(tt/rl);lv=float(np.nextafter(float(lo.a),-np.inf));hv=float(np.nextafter(float(hi.b),np.inf));assert np.isfinite([lv,hv]).all();lower[j,k]=lv;upper[j,k]=hv;outward &= bool(J(lv)<=lo.a and J(hv)>=hi.b)
    if J(mass['lower'][j,k])>lo.a or J(mass['upper'][j,k])<hi.b:misses+=1;max_miss=max(max_miss,float(J(mass['lower'][j,k])-lo.a),float(hi.b-J(mass['upper'][j,k])))
  halo_j+=1
 np.savez_compressed(out/'original_input_mass_vectors.npz',lower=lower,upper=upper,radius_pc=rg,node_indices=mass['node_indices']);ck('mass_outward_finite',outward and np.isfinite(lower).all() and np.isfinite(upper).all());mass_result=dict(attempted=True,coordinates=lower.size,old_endpoint_box_misses=misses,max_absolute_endpoint_miss=max_miss,law_coordinates_not_identical=law_nonzero,max_law_absolute_difference=law_max,scope='Analytic original-input endpoint vectors; signed delta membership/continuum and floating solver still unresolved')
result=dict(checks=checks,rows=rows,root_checks=roots,uncertain_roots=uncertain,branch_events=branch_events,root_signs_passed=sum(v['signs_pass'] for v in roots),root_total=len(roots),analytic_gate_passed=gate,mass_propagation=mass_result,point_max_relative_error=max(point_errors),runtime_seconds=time.monotonic()-t0,input_sha256=hashes,full_model_interval_certified=False,scope='Original-input mathematical coefficient/branch/root gate; not original binary64 libm or solver/continuum membership certificate');(out/'results.json').write_text(json.dumps(result,indent=2)+'\n');print('checks',len(checks),all(checks.values()),'root_signs',result['root_signs_passed'],'/',len(roots),'branches',branch_events,'uncertain',uncertain);assert all(checks.values())
