#!/usr/bin/env python3
"""Bounded, prospective observable/covariance audit, banked XR22 tables conditional.
No pipeline change; independent mock catalog and model population, common bootstrap
indices across all separation and overlapping anchor medians. No triples/orbit repair.
"""
import os
for k in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS']:os.environ[k]='1'
import sys,ast,json,math,time,hashlib,datetime,resource
from pathlib import Path
import numpy as np
O=Path(__file__).resolve().parent;R=O.parents[2];L=R/'real_research/cross_thread_review_2026_09_26';sys.path.insert(0,str(L));sys.dont_write_bytecode=True
import XR22_common as C
OFFSET=int(os.environ.get('XR22_AUDIT_SEED_OFFSET','0')); SUFFIX='_model1p5m'
START=time.time();STAMP=datetime.datetime.now(datetime.timezone.utc).isoformat()
P=C.load_pipeline();CI=C.chain_inputs();law=json.loads((L/'XR22_force_law_results.json').read_text());TAB=law['tables'];LIN=law['lin_tables'];floor=CI['xi_floor_pc'];BINS=np.array([2,3,5,7,10,15,20,30.]);BOOT_DATA=400;BOOT_MODEL=200
# Extract unchanged prediction functions from source; no execution of full main or its large bootstrap allocations.
tree=ast.parse((L/'XR22_prereg_statistic.py').read_text());mn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='main')
grid=TAB[f"canonical|prereg_primary|{floor['canonical']:.6g}"]
ns=dict(C=C,np=np,math=math,MUTATE=False,TAB=TAB,LIN=LIN,TH3=[0.,45.,90.],S_EXT=sorted({float(k.split('|')[1]) for k in grid}),M_EXT=sorted({float(k.split('|')[0]) for k in grid}),TH_FINE=sorted({float(k.split('|')[1]) for k in LIN['canonical|prereg_primary|0']}),key=lambda M,s,t:f'{M}|{s}|{t}')
for name in ['fine_grid','phys_boost']:
 node=next(n for n in mn.body if isinstance(n,ast.FunctionDef) and n.name==name);exec(compile(ast.Module(body=[node],type_ignores=[]),str(L/'XR22_prereg_statistic.py'),'exec'),ns)
def population(N,seed,keep=None):
 p=C.make_population_full(P,N,np.random.default_rng(seed),rng_orient=np.random.default_rng(seed+22))
 if keep:
  assert len(p['Mt'])>=keep
  ix=np.random.default_rng(seed+1).permutation(len(p['Mt']))[:keep];p={k:v[ix] for k,v in p.items()}
 return p
def boost(p,foot,xi):return ns['phys_boost'](foot,xi,sysd=dict(Mt=p['Mt'],s=p['r3d']/P['KAU'],th=np.minimum(p['psi'],np.pi-p['psi'])))
def velocity(p,B,kappa=1.):
 g=kappa*np.sqrt(B)
 return np.hypot(g*p['pmx']+p['npmx'],g*p['pmy']+p['npmy'])*4.74e3*p['d_obs']/1000/p['vc_obs']
def groups(p,foot):
 s=p['s_obs']/P['KAU'];y=np.log10(p['g_proj']/P['A0_CAN' if foot=='canonical' else 'A0_ALT'])
 return [(s>=a)&(s<b) for a,b in zip(BINS[:-1],BINS[1:])]+[(y>=.5)&(y<1.),(y>=1.)&(y<2.2)]
def summaries(v,gg,idx=None,extra=None):
 if idx is None:idx=np.arange(len(v))
 vi=v[idx];cut=vi<P['VTCAP']
 if extra is not None:cut&=extra[idx]
 vals=[vi[g[idx]&cut] for g in gg]
 return np.log([np.median(x) for x in vals]),[len(x) for x in vals]
def covariance(v,gg,nboot,seed):
 rng=np.random.default_rng(seed);z=np.empty((nboot,len(gg)));n=len(v)
 for i in range(nboot):z[i]=summaries(v,gg,rng.integers(0,n,n))[0]
 return np.cov(z,rowvar=False,ddof=1)
def information(d,h,c):
 eig=np.linalg.eigvalsh(c);assert eig[0]>0
 inv=np.linalg.inv(c);fxx=float(d@inv@d);fxh=float(d@inv@h);fhh=float(h@inv@h);pr=fxx-fxh*fxh/fhh
 assert pr>0 and pr<=fxx*(1+1e-12)
 return dict(fixed_sigma=1/math.sqrt(fxx),profiled_sigma=1/math.sqrt(pr),Fxx=fxx,Fxk=fxh,Fkk=fhh,correlation=fxh/math.sqrt(fxx*fhh),cov_min_eigenvalue=float(eig[0]),cov_condition=float(eig[-1]/eig[0]))
print('creating modest model and independent mock populations',flush=True)
model=population(1500000,20261216);data=population(81000,2026092813+OFFSET,30000)
controls={'newton_velocity_equals_frozen':bool(np.allclose(velocity(data,np.ones(len(data['Mt']))),P['vtilde_of'](data,1.,P['A0_CAN']),rtol=1e-14,atol=1e-14))}
rows=[]
for f in ['canonical','alt']:
 gm,gd=groups(model,f),groups(data,f)
 for case,(xi,xj) in enumerate([(floor[f],.03),(.05,.07),(.1,.15)]):
  t=time.time();Bm=boost(model,f,xi);Bd=boost(data,f,xi);v=velocity(model,Bm);vd=velocity(data,Bd);v0=velocity(model,np.ones(len(Bm)))
  base,counts=summaries(v,gm);next_=summaries(velocity(model,boost(model,f,xj)),gm)[0];dx=(next_-base)/math.log(xj/xi)
  eps=.005;plus=summaries(velocity(model,Bm,math.exp(eps)),gm)[0];minus=summaries(velocity(model,Bm,math.exp(-eps)),gm)[0];dk=(plus-minus)/(2*eps)
  cdata=covariance(vd,gd,BOOT_DATA,2026092913+OFFSET+case)
  cmc=covariance(v,gm,BOOT_MODEL,2026093013+OFFSET+case)
  cov=cdata+cmc
  result=information(dx,dk,cov);unanchored=information(dx[:7],dk[:7],cov[:7,:7]);diag=information(dx[:7],dk[:7],np.diag(np.diag(cov[:7,:7])))
  # Paired joint covariance retains correlations with both overlapping anchor bins.
  norm=np.sqrt(np.outer(np.diag(cov),np.diag(cov)));cor=cov/norm
  oldg=summaries(v,gm,extra=v0<P['VTCAP'])[0];oldn=summaries(v0,gm,extra=v<P['VTCAP'])[0];newn=summaries(v0,gm)[0]
  oldratio=np.exp(oldg-oldn)-1;newratio=np.exp(base-newn)-1
  banked=json.loads((L/'XR22_prereg_statistic_results.json').read_text())['numbers']['sepbins'][f'{f}|{xi:.6g}']; banked_ratios=np.array([z['ratio'] for z in banked]); ratio_delta=float(np.max(abs(newratio[:7]-banked_ratios))); assert ratio_delta<1e-12
  mutd=(summaries(velocity(model,boost(model,f,xi)),gm)[0]-base)/math.log(xj/xi);mutinfo=float(mutd@np.linalg.solve(cov,mutd));assert mutinfo==0
  # Mean old/new cut differences often exactly zero in a clean sample; test actual tails rather than assume an effect.
  row=dict(footing=f,xi_pc=xi,next_knot_pc=xj,model_N=len(Bm),mock_N=len(Bd),model_counts=counts,data_counts=summaries(vd,gd)[1],cut_removed_model=int((v>=P['VTCAP']).sum()),cut_removed_newton=int((v0>=P['VTCAP']).sum()),cut_disagreement=int(np.count_nonzero((v<P['VTCAP'])!=(v0<P['VTCAP']))),old_intersection_ratio=oldratio[:7].tolist(),corrected_symmetric_ratio=newratio[:7].tolist(),banked_ratio_max_abs_difference=ratio_delta,maximum_cut_ratio_change=float(np.max(abs(oldratio[:7]-newratio[:7]))),derivative_lnxi=dx.tolist(),derivative_lnkappa=dk.tolist(),joint_covariance=cov.tolist(),data_covariance=cdata.tolist(),model_covariance=cmc.tolist(),max_sep_anchor_correlation=float(np.max(abs(cor[:7,7:]))),joint_anchor=result,seven_bins_profiled=unanchored,seven_bins_diagonal=diag,xi_independent_mutation_information=mutinfo,seconds=time.time()-t)
  rows.append(row);print(f,xi,'joint',result['profiled_sigma'],'noanchor',unanchored['profiled_sigma'],'cut change',row['maximum_cut_ratio_change'],'seconds',row['seconds'],flush=True)
  out=dict(status='partial' if len(rows)<6 else 'complete',started_utc=STAMP,runtime_seconds=time.time()-START,peak_rss_bytes_macos=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,rows=rows,controls=controls,settings=dict(model_draws=1500000,model_seed=20261216,mock_draws=81000,mock_seed=2026092813+OFFSET,mock_keep=30000,bootstrap_data=BOOT_DATA,bootstrap_model=BOOT_MODEL,cap=6.,kappa_log_step=eps,finite_difference='adjacent xi knot',proposal_not_frozen=True),limitations=['Uses banked force tables conditionally while full force rerun is active.','No contamination, self-consistent orbit, real Galactic-direction or mass-ratio force correction.','Fisher forecast only; no frequentist coverage or detection calibration.','κ derivative is local at κ_cal=1; window [.95,1.05] not imposed as a stochastic prior.','Sample objects have no shared-star graph; whole-pair resampling suffices only for this independent mock.','Limited model population and bootstrap draws cause Monte Carlo forecast variability.'],input_hashes={str(q.relative_to(R)):hashlib.sha256(q.read_bytes()).hexdigest() for q in [L/'XR22_common.py',L/'XR22_prereg_statistic.py',L/'XR22_force_law_results.json',L/'XR22_prereg_statistic_results.json',R/'prep_2026/gaia_dr4_prep/wide_binary_pipeline.py',Path(__file__)]})
  (O/('corrected_statistic_results'+SUFFIX+'.json')).write_text(json.dumps(out,indent=2))
assert controls['newton_velocity_equals_frozen']; print('completed',time.time()-START,flush=True)
