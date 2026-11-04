"""Self-control for an explicit-availability physical-number backend."""
import os,sys
sys.dont_write_bytecode=True
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS'):os.environ[k]='1'
from pathlib import Path
import json,time,resource
import numpy as np
from scipy.sparse import csr_matrix
from protocol_holes import QuantumState,implicit_step
ROOT=Path(__file__).resolve().parents[3]

class ToyNumberBackend:
 def __init__(self,measure):self.measure=np.asarray(measure,float);self.eta=np.array([-1.,1.,-1.]);self.energy=np.array([2.,1.,1.]);self.s=np.array([-1.,1.,1.])
 def products(self,f,a):return f[0]*a[1]*a[2],a[0]*f[1]*f[2]
 def number_rhs(self,f,availability=None):
  a=1+self.eta*f if availability is None else availability;F,R=self.products(f,a);return self.s*(F-R)
 def number_gross(self,f,availability=None):
  a=1+self.eta*f if availability is None else availability;F,R=self.products(f,a);return abs(self.s)*(F+R)
 def number_jacobian(self,f,availability=None):
  a=1+self.eta*f if availability is None else availability;derivative=np.array([a[1]*a[2]+f[1]*f[2],f[0]*a[2]-a[0]*f[2],-f[0]*a[1]-a[0]*f[1]])/self.measure
  return csr_matrix(self.s[:,None]*derivative[None,:])

def main(out):
 start=time.monotonic();reference=json.loads((ROOT/'reviews/collision_completion_2026_11_04/integration_solver/run_toy001/result.json').read_text())['toy'];rows=[]
 for m in [1e-12,1e-20,1e-24]:
  ev=ToyNumberBackend([1.,1.,m]);old=QuantumState(ev.measure,ev.eta,Y=np.array([.5,1e-30,0.]));new,diag=implicit_step(ev,old,1.,tol=2e-10);f,a=new.arrays();ref=next(t for t in reference if t['lambda_measure']==m and t['dt']==1.);relative=abs(a[2]/float(ref['reference_hole'])-1);rows.append(dict(measure=m,availability=a.tolist(),f=f.tolist(),relative_reference_hole_error=float(relative),newton=diag,copy_class_preserved=isinstance(new.copy(),QuantumState),collision_energy_rate=float(ev.energy@new.rhs(ev))))
 ev=ToyNumberBackend([2.,3.,.1]);old=QuantumState(ev.measure,ev.eta,Y=ev.measure*np.array([.3,.2,.7]));exact=old.jacobian(ev).toarray();numerical=np.zeros_like(exact)
 for j in range(3):
  d=1e-6*old.Z[j];left=old.copy();right=old.copy();left.Z[j]-=d;right.Z[j]+=d;sign=np.where(old.holes,-1.,1.);numerical[:,j]=sign*(right.rhs(ev)-left.rhs(ev))/(2*d)
 error=float(np.max(abs(exact-numerical))/max(np.max(abs(exact)),1e-300));checks=dict(subulp_availability=rows[-1]['availability'][2]>0 and rows[-1]['availability'][2]<1e-18,highprecision_reference=max(r['relative_reference_hole_error'] for r in rows)<1e-7,number_jacobian_protocol=error<1e-7,copy_preserves_adapter=all(r['copy_class_preserved'] for r in rows),physical_bounds=all(min(r['f'])>=0 and max(np.array(r['f'])[[0,2]])<=1 for r in rows),local_energy=max(abs(r['collision_energy_rate']) for r in rows)<1e-20)
 result=dict(claim_id='CC10_EXPLICIT_AVAILABILITY_PROTOCOL_CONTROL',checks=checks,toy=rows,Jacobian_relative_error=error,exact_coordinate_jacobian=exact.tolist(),finite_difference_coordinate_jacobian=numerical.tolist(),runtime_seconds=time.monotonic()-start,peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,scope='Ownexactnumberbackend testsadapterchainrule,explicitavailabilityandcopytype; actualAngularExactwarmcontroldeferreduntilitsfrozen sourceavailable.')
 Path(out).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result));assert all(checks.values())
if __name__=='__main__':main(sys.argv[1])
