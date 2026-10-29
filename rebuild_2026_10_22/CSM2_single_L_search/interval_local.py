"""Conditional discrete enclosure experiment for frozen canonical [3.75,3.751]."""
import os
for v in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[v]='1'
import argparse,contextlib,io,json,hashlib,sys
from pathlib import Path
import numpy as np
from scipy.optimize import brentq
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];REB=HERE.parent
sys.path.insert(0,str(HERE))
from projection_operator import operator
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args();out=Path(args.output).resolve();out.mkdir(parents=True,exist_ok=True)
checks={};finite=0

def arr(a):
 global finite
 a=np.asarray(a,float);assert np.isfinite(a).all();finite+=1;return a

def ck(k,v):checks[k]=bool(v)
replay=REB/'CSM1_consistent_core_switch/calibration/calibrate_replay.py';ref=replay.parent/'run_003_audited/results.json'
text=replay.read_text();prefix=text[:text.index('RESULT=dict(assertion_tested=')];(out/'executed_helper_prefix.py').write_text(prefix)
savedargv=sys.argv;sys.argv=[str(replay),'--output',str(out),'--reference',str(ref),'--skip-baseline'];ns={'__file__':str(replay),'__name__':'interval_helpers'}
with contextlib.redirect_stdout(io.StringIO()):exec(compile(prefix,str(replay),'exec'),ns)
sys.argv=savedargv
capture={};old=ns['NS']['run_copy']
def wrapped(*a,**kw):
 s=old(*a,**kw);capture['source']=s;return s
ns['NS']['run_copy']=wrapped
with contextlib.redirect_stdout(io.StringIO()):raw=ns['task']('x53','on','shpS9_L3.75','corrected')
s=capture['source'];base=np.array(raw['result']['canonical']['profiles']['H']);native=np.load(HERE/'native_matrix_001/native_matrices.npz');weights=arr(native['weights']);grid=arr(native['LMG']);R=arr(native['R']);PW=arr(native['P']@native['W']);y=arr(raw['result']['canonical']['profiles']['data']).ravel();lawscore=raw['result']['canonical']['all']['L2H']['chi2'];cut=lawscore+9
ck('saved_baseline',np.max(abs(base-np.array(json.loads(ref.read_text())['levels']['3.75']['lens']['result']['canonical']['profiles']['H'])))<1e-10)
ck('native_weights',np.max(abs(weights.sum(axis=1)-1))<1e-12 and np.all(weights>=0) and int(np.any(weights>0,axis=0).sum())==127)
rg=arr(s['RGRID_PC']);B=s['B'];cfg=s['H_PRIMARY'];active=np.flatnonzero(np.any(weights>0,axis=0));eta0=s['eta_of'];L0,L1=3.75,3.751
hfun=lambda x:4*x**3/((1+x)*(1+x*x)*float(B(x)))
xpk=brentq(lambda x:hfun(x)-2,.1,10,xtol=1e-14)
# Unique maximum follows analytic decreasing h proof; xpk lies inside source bounds.
ck('peak_in_source_bounds',1e-3<xpk<1e6 and abs(hfun(xpk)-2)<1e-12)
node=[];low={};high={};source_base={};bracket_records=[];events=[];maxprojectionerror=0.

def root_box(M,R,Sig):
 F=lambda x:float(B(x))/x**2;target=M/(np.pi*Sig*R*R)
 if target>F(xpk):
  # numerical peak uncertainty covered by the prescribed later mass padding
  return R/(xpk*(1+1e-12)),R/(xpk*(1-1e-12)),True
 lo=xpk;hi=1e7;assert F(hi)<target
 while hi-lo>1e-12*lo:
  mid=(hi+lo)/2
  if F(mid)>target:lo=mid
  else:hi=mid
 assert F(lo)>=target and F(hi)<=target
 return R/hi,R/lo,False

def independent_mass(lm,M,R,Sig):
 Ms=10**lm;Mc=10**(lm+(-.69*(lm-2*np.log10(.70/.679))+6.63));mb=Ms+Mc+.5*Ms*np.minimum(1,(rg/1e5)**3)
 rlo,rhi,sat=root_box(M,R,Sig);rr=np.minimum(rg,R);ml=arr(mb+np.pi*Sig*rlo*rlo*B(rr/rhi));mu=arr(mb+np.pi*Sig*rhi*rhi*B(rr/rlo))
 bracket_records.append(dict(M=M,R=R,Sigma=Sig,r0_lower=rlo,r0_upper=rhi,saturated=sat))
 return ml,mu

for i in active:
 lm=grid[i];Ms=10**lm;Mc=10**(lm+(-.69*(lm-2*np.log10(.70/.679))+6.63));M,Rh,r0,Sig,flag=s['halo_setup']('canonical',float(np.log10(Ms+Mc)),cfg);floor=s['SIGA0']['canonical'];column=eta0(M,cfg['cf'])*s['sigma_coll'](M);threshold=L0*(floor/column)**.8
 # Event guard includes a declared relative uncertainty allowance.
 if L0-1e-10<=threshold<=L1+1e-10:events.append(dict(i=int(i),threshold=threshold))
 source,mm=s['mass_H']('canonical',float(lm),.679,cfg);source=arr(source);source_base[i]=source
 node.append(dict(i=int(i),logMs=float(lm),M=M,column=column,floor=floor,threshold=threshold,halo=flag))
 if flag:
  ml0,mu0=independent_mass(lm,M,Rh,Sig);ml1,mu1=independent_mass(lm,M,Rh,max(floor,column*(L1/L0)**1.25))
  # Exact-arithmetic monotonicity proof supplies intermediate L enclosure.
  ck(f'mass_order_{i}',np.all(mu1>=ml0));low[i]=ml0;high[i]=mu1
  ck(f'source_root_{i}',np.all(source>=ml0-(1e-8*abs(ml0)+1e-6)) and np.all(source<=mu0+(1e-8*abs(mu0)+1e-6)))
 else:low[i]=source.copy();high[i]=source.copy()
 pad=1e-8*np.maximum(abs(low[i]),abs(high[i]))+1e-6;low[i]-=pad;high[i]+=pad
ck('no_branch_events',not events)
ops={(b,tail):arr(operator(R[b]*1e6,rg,s['AQ'].TT,tail)) for b in range(4) for tail in ('const','linear')}
stack=np.zeros((4,15));predlo=np.zeros_like(stack);predhi=np.zeros_like(stack)
for n in node:
 i=n['i'];tail='const' if n['halo'] else 'linear';lo,hi=low[i],high[i]
 for b in range(4):
  if weights[b,i]==0:continue
  A=ops[b,tail];plus=np.maximum(A,0);minus=np.minimum(A,0);expected=arr(s['AQ'].delta_sigma(R[b]*1e6,rg,source_base[i],tail));got=arr(A@source_base[i]);err=float(np.max(abs(got-expected))/max(np.max(abs(expected)),1e-300));maxprojectionerror=max(maxprojectionerror,err)
  stack[b]+=weights[b,i]*got;predlo[b]+=weights[b,i]*arr(plus@lo+minus@hi);predhi[b]+=weights[b,i]*arr(plus@hi+minus@lo)
ck('projection_source',maxprojectionerror<1e-9)
stackerr=float(np.max(abs(stack-base))/max(np.max(abs(base)),1e-300));ck('stack_baseline',stackerr<1e-8)
# Project boxes after stacking. This is conservative (may lose correlations).
pl=np.maximum(PW,0);mn=np.minimum(PW,0);rl=arr(PW@y-pl@predhi.ravel()-mn@predlo.ravel()-1e-6);ru=arr(PW@y-pl@predlo.ravel()-mn@predhi.ravel()+1e-6);ck('residual_box_order',np.all(rl<=ru));distance=np.maximum(np.maximum(rl,-ru),0);lower=max(0.,float(distance@distance)-1e-4)
source_scores=[];source_projection=[]
for L in (L0,(L0+L1)/2,L1):
 s['eta_of']=lambda M,cf,L=L:eta0(M,cf)*(L/L0)**1.25
 with contextlib.redirect_stdout(io.StringIO()):model,meta=s['stack_H']('canonical',cfg)
 model=arr(model);r=arr(PW@(y-model.ravel()));score=float(r@r);source_scores.append(dict(L=L,free_score=score));ck(f'box_contains_{L}',np.all(r>=rl-1e-8) and np.all(r<=ru+1e-8));source_projection.append(model)
ck('source_scores_above_bound',all(x['free_score']>=lower-1e-8 for x in source_scores))
# Deliberate corruption of the source baseline stack, a positive weight and a branch.
ck('matrix_mutation_detected',np.max(abs(stack*1.01-base))/np.max(abs(base))>1e-8)
ck('weight_mutation_detected',abs((weights[0]*1.01).sum()-1)>1e-12)
first=next(n for n in node if n['halo']);i=first['i'];s['eta_of']=eta0;lh,mm=s['mass_H']('canonical',float(grid[i]),.679,cfg,halo=False);mut=arr(lh*s['AQ'].nu_simple(s['Gpc']*lh/rg**2/s['a0u']('canonical')));ck('branch_mutation_detected',np.max(abs(mut-source_base[i]))/np.max(abs(source_base[i]))>1e-8)
# Hash every dynamically opened scientific source/input recorded by original audited helper.
inputs=dict(ns['INPUTS'])
for f in [Path(__file__),HERE/'INTERVAL_001_CRITERIA.md',HERE/'projection_operator.py',HERE/'native_matrix_001/native_matrices.npz',HERE/'native_matrix_001/results.json',REB/'CSM1_consistent_core_switch/heldout/MW_BURKERT_MONOTONICITY.md']:
 inputs[str(f)]=hashlib.sha256(f.read_bytes()).hexdigest()
ck('inputs_stable',all(hashlib.sha256(Path(f).read_bytes()).hexdigest()==h for f,h in inputs.items()))
result=dict(checks=checks,interval=[L0,L1],nodes=node,branch_events=events,root_brackets=bracket_records,lower_score=lower,cut=cut,source_scores=source_scores,max_projection_error=maxprojectionerror,baseline_stack_relative_error=stackerr,finite_arrays_checked=finite,input_sha256=inputs,conditional_numeric_exclusion=bool(all(checks.values()) and lower>cut),certified_exclusion=False,scope='Local floating-point enclosure experiment; root brackets and padding not outward-rounded; no covering obstruction',numerical_limitations=['Binary64 evaluations and root comparisons are not interval-certified','Positive padding is prescribed, not a proven bound on all floating-point error','If lower bound is inconclusive this does not identify a passing L'])
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n');np.savez_compressed(out/'score_boxes.npz',prediction_lower=predlo,prediction_upper=predhi,residual_lower=rl,residual_upper=ru,source_profiles=source_projection)
print(json.dumps(dict(checks=checks,lower_score=lower,cut=cut,source_scores=source_scores,conditional_numeric_exclusion=result['conditional_numeric_exclusion']),indent=2));assert all(checks.values())
