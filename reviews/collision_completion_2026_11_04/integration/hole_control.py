"""Sub-ulp Pauli-hole control and restart of the actual stiff warm checkpoint."""
import os,sys
sys.dont_write_bytecode=True
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[k]='1'
from pathlib import Path
import json,time,math,resource
import numpy as np
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'reviews/collision_completion_2026_11_04/statistics'))
sys.path.insert(0,str(ROOT/'reviews/collision_completion_2026_11_04/cascades'))
from quantum import ReactionEvents
from averaged import averaged_events
from vertices import VertexBackground
from generic_orbit import GenericOrbit,T0
from holes import QuantumState,implicit_step

def main(output):
 start=time.monotonic();toy=[]
 for small in (1e-12,1e-20,1e-24):
  ev=ReactionEvents([[0,1,1,2,2]],[[1,1,0,1,0]],[1.],[1.,1.,small],[2.,1.,1.],[-1.,1.,-1.])
  old=QuantumState(ev.measure,ev.eta,Y=np.array([.5,1e-30,0.]));new,control=implicit_step(ev,old,small*1000,tol=2e-10)
  f,av=new.arrays();eq=av[2]-f[1]/(1+f[1])
  toy.append(dict(lambda_measure=small,f=f.tolist(),availability=av.tolist(),hole_coordinate=bool(new.holes[2]),newton=control,equilibrium_hole_residual=float(eq),number_energy_delta=float(ev.energy@(new.numbers()-old.numbers()))))
 prior=json.loads((ROOT/'reviews/collision_completion_2026_11_04/integration/run_warm001/result.json').read_text())
 c=prior['case'];st=prior['state'];Y=np.array(st['Y']);q=np.array(c['q']);W=np.array(c['W']);N=st['N']
 bg=VertexBackground(ROOT/'reviews/collision_completion_2026_11_04/cascades/run_vertices001/result.json');model=GenericOrbit(bg,q,W,8);model.J0=st['J0'];model.last_x=st['xmid'];orb=model.orbit(N,Y,E=st['E']);ev=averaged_events(bg,orb['xs'],orb['weights'],T0*math.exp(-N),q,W,2)
 state=QuantumState(ev.measure,ev.eta,Y=Y);runs=[]
 for dN in (1e-7,1e-6,1e-5):
  new,control=implicit_step(ev,state,dN/model.hubble(N),tol=2e-8);f,av=new.arrays()
  C=new.rhs(ev);energy_local=sum(w*float(a.energy@np.asarray(a.S@(a.coefficient*(new.products(a)[0]-new.products(a)[1]))).ravel()) for w,a in zip(ev.phase_weights,ev.local_events))
  runs.append(dict(dN=dN,newton=control,min_f=float(min(f)),max_fermion_f=float(max(f[ev.eta<0])),minimum_fermion_availability=float(min(av[ev.eta<0])),hole_nodes=int(sum(new.holes)),number_change_L1=float(sum(abs(new.numbers()-Y))),entropy_change=new.entropy()-state.entropy(),local_collision_energy=energy_local,final_Z=new.Z.tolist(),hole_flags=new.holes.tolist()))
 checks=dict(sub_ulp_holes_retained=toy[-1]['hole_coordinate'] and 0<toy[-1]['availability'][2]<1e-18,
  toy_equilibria=all(abs(t['equilibrium_hole_residual'])<max(1e-20,t['lambda_measure']*1e-5) for t in toy),
  warm_steps_completed=len(runs)==3,physical_bounds=all(r['min_f']>=0 and r['max_fermion_f']<=1 and r['minimum_fermion_availability']>0 for r in runs),
  entropy_nondecreasing=all(r['entropy_change']>=-1e-10 for r in runs),local_energy=sum(abs(r['local_collision_energy']) for r in runs)<1e-20)
 result=dict(claim_id='CC10_STABLE_FERMION_HOLE_COORDINATES',checks={k:bool(v) for k,v in checks.items()},toy=toy,warm=runs,
  scope='Sub-ulp fermionic availability retained in mixed number/hole coordinates; actual warm checkpoint implicit collision advances only, not a coupled-history or averaging certificate.',runtime_seconds=time.monotonic()-start,peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
 Path(output).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(dict(checks=result['checks'],toy=toy,warm=[{k:v for k,v in x.items() if k not in ('final_Z','hole_flags')} for x in runs],runtime_seconds=result['runtime_seconds'],peak_rss_bytes=result['peak_rss_bytes'])));assert all(checks.values()),checks
if __name__=='__main__':main(sys.argv[1])
