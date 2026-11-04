"""Physical exact-zero daughter born through an intermediate within one BE step."""
import os,sys
sys.dont_write_bytecode=True
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS'):os.environ[k]='1'
from pathlib import Path
import numpy as np,json,time,resource
import mpmath as mp
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'reviews/collision_completion_2026_11_04/statistics'))
from quantum import ReactionEvents
from seeded_number_v2 import QuantumState,implicit_step

def main(out):
 start=time.monotonic();ev=ReactionEvents([[1,0,0,0,0],[1,2,2,2,2]],[[1,1,0,1,0],[1,1,0,1,0]],[1.,1.],[1.,1.,1.],[1.,2.,1.],[-1.,1.,1.]);old=QuantumState(ev.measure,ev.eta,Y=np.array([.5,0.,0.]));rows=[]
 for epsilon in [1e-20,1e-40,1e-60]:
  new,info=implicit_step(ev,old,1.,tol=1e-10,zero_guess_occupation=epsilon);f,a=new.arrays();res=new.numbers()-old.numbers()-new.rhs(ev);rows.append(dict(guess_occupation=epsilon,final_f=f.tolist(),final_availability=a.tolist(),newton=info,physical_BE_residual_L1=float(sum(abs(res))),energy_change=float(ev.energy@(new.numbers()-old.numbers())),entropy_gain=new.entropy()-old.entropy()))
 mp.mp.dps=90
 def equations(F,P,V):
  j1=P*(1-F)**2-(1+P)*F**2;j2=P*(1+V)**2-(1+P)*V**2
  return F-mp.mpf('.5')-2*j1,P+j1+j2,V-2*j2
 reference=mp.findroot(equations,tuple(mp.mpf(str(x)) for x in rows[1]['final_f']),tol=mp.mpf('1e-75'),maxsteps=100);err=max(float(max(abs(mp.mpf(x)-r) for x,r in zip(row['final_f'],reference))) for row in rows);difference=max(float(sum(abs(np.array(row['final_f'])-np.array(rows[1]['final_f'])))) for row in rows);checks=dict(positive=all(min(r['final_f'])>=0 and r['final_f'][0]<=1 for r in rows),within_step_daughter=all(r['final_f'][2]>0 for r in rows),reference=err<1e-8,guess_sensitivity=difference<1e-10,energy=max(abs(r['energy_change']) for r in rows)<1e-12,entropy=min(r['entropy_gain'] for r in rows)>=0);result=dict(claim_id='CC11_PHYSICAL_ZERO_NEWTON_GUESS',checks=checks,rows=rows,highprecision_reference=[str(x) for x in reference],max_reference_error=err,max_guess_difference_L1=difference,initial_physical_f=[.5,0.,0.],runtime_seconds=time.monotonic()-start,peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,scope='Exactzero physicalP,V; positiveNewtonguessonly, noinitialphysicalseed. ToyFF<->P<->VV withfullstatistics/inverses,90digitBEreference; notactualvectorratevalidation.')
 Path(out).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result));assert all(checks.values())
if __name__=='__main__':main(sys.argv[1])
