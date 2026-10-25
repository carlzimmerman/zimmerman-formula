"""Finite overlap with sampled occupied CCT-008 radial subspaces, not entropy creation."""
import pathlib,json,hashlib
import numpy as np
from scipy.linalg import eigh_tridiagonal
P=pathlib.Path(__file__).resolve().parent;ROOT=P.parents[1];T=ROOT/'sol61_push/cold_envelope_spectrum_2026_10_24';models=json.loads((ROOT/'sol61_push/cold_survey_capture_2026_10_24/capture_results.json').read_text())['models'];model={m['name']:m for m in models};tjson=json.loads((T/'eta1500_refine.json').read_text());targets={q['name']:q for q in tjson['results']};G=.00430091
# Saved states only; newly finishing jobs do not change this explicit assay list.
tags=['draco_L12_long','draco_escape_long','sextans_L24_long','sextans_escape','sextans_escape_long'];files=[pathlib.Path(__file__),T/'eta1500_refine.json',ROOT/'sol61_push/cold_survey_capture_2026_10_24/capture_results.json']
for tag in tags:
 q=json.loads((P/'runs'/f'{tag}.json').read_text());name=q['parameters']['galaxy'];files.extend([P/'runs'/f'{tag}.json',P/'runs'/f'{tag}_fields.npz',T/f'eta1500_refine_{name.replace(" ","")}.npz'])
def hashes():return {str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest() for f in files}
before=hashes();rows=[]
for tag in tags:
 q=json.loads((P/'runs'/f'{tag}.json').read_text());name=q['parameters']['galaxy'];m=model[name];tp=targets[name];target=np.load(T/f'eta1500_refine_{name.replace(" ","")}.npz');x=target['x'];h=x[1]-x[0];eta=tp['eta_code'];n=len(x);off=np.full(n-1,-eta*eta/(2*h*h));diag=np.full(n,eta*eta/h**2)+target['target_potential'];occ=target['occupation'];ids=target['mode_ids'];f=np.load(P/'runs'/f'{tag}_fields.npz');r=f['r'];w=f['w'];lm=f['lm'];u=q['physical'];source_x=r*u['Runit_pc']/m['cold_scale_pc'];states={'initial':f['initial'],'final':f['final']};projected={k:0. for k in states};ranks=[];covered_target=0;angular_target=0
 for l in sorted(set(lm[:,0])):
  chosen=np.where((ids[:,0]==l)&(occ>1e-7))[0]
  if not len(chosen):continue
  ns=ids[chosen,1];covered_target+=sum(occ[chosen]);modes=np.where(lm[:,0]==l)[0];angular_target+=sum(occ[chosen])*len(modes)/(2*l+1)
  ev,U=eigh_tridiagonal(diag+eta*eta*l*(l+1)/(2*x*x),off,select='i',select_range=(0,int(max(ns))))
  # Sample the target eigenfunctions into the source weighted radial Hilbert space.
  B=np.array([np.interp(source_x,np.r_[0,x,20],np.r_[0,U[:,j],0],left=0,right=0) for j in ns]).T
  B*=np.sqrt(w*u['Runit_pc']/(m['cold_scale_pc']*h))[:,None]
  Q,sv,_=np.linalg.svd(B,full_matrices=False);rank=int(sum(sv>sv[0]*1e-8));Q=Q[:,:rank]
  assert np.max(abs(Q.conj().T@Q-np.eye(rank)))<1e-12
  for stage,v in states.items():projected[stage]+=u['Munit_Msun']*float(np.sum(abs(Q.conj().T@v[:,modes])**2))
  ranks.append({'l':int(l),'radial_columns':len(ns),'retained_rank':rank,'condition':float(sv[0]/max(sv[-1],1e-300))})
 for stage,v in states.items():assert projected[stage]<=u['Munit_Msun']*float(np.sum(abs(v)**2))*(1+1e-10)
 row={'tag':tag,'scope':'orthogonal finite-grid overlap with sampled occupied TARGET radial eigenfunction spans; not a bound-state certificate for actual nonlinear H','initial_supported_span_mass_Msun':projected['initial'],'final_supported_span_mass_Msun':projected['final'],'growth_ratio':projected['final']/max(projected['initial'],1e-100),'fraction_of_reference_radial_occupation_under_L_cutoff':covered_target/sum(occ),'fraction_of_reference_full_mixture_under_L_and_m_geometry':angular_target/sum(occ),'radial_rank_checks':ranks};rows.append(row);print(tag,projected,'growth',row['growth_ratio'],flush=True)
after=hashes();assert before==after
(P/'supported_projection.json').write_text(json.dumps({'scope':'subspace assay; target has nonunique occupations and cold pure-state coherences are retained; no stationary statistical envelope formed by a projector','inputs_before':before,'inputs_after':after,'results':rows},indent=2)+'\n')
