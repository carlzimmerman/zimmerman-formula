"""Prior bounded discriminator: common energy/action stage alternatives."""
import os,sys
sys.dont_write_bytecode=True
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS'):os.environ[k]='1'
from pathlib import Path
import json,math,time,resource
import numpy as np
ROOT=Path(__file__).resolve().parents[3]
for folder in ('cascades','integration','initial_solver'):sys.path.insert(0,str(ROOT/'reviews/collision_completion_2026_11_04'/folder))
from angular_fast import averaged_exact_events
from consistent_background import ConsistentVertexBackground
from precise_orbit import GenericOrbit,T0
from split_energy import QuantumState,implicit_step,covariance,expansion_work,collision,step

def load(path,phase=8):
 d=json.loads(Path(path).read_text());old=d['state'];q=np.array(d['case']['q']);W=np.array(d['case']['W']);bg=ConsistentVertexBackground(ROOT/'reviews/collision_completion_2026_11_04/cascades/run_vertices001/result.json');model=GenericOrbit(bg,q,W,phase);model.J0=old['J0'];model.last_x=old['xmid'];state=QuantumState(model.measure,model.eta,Z=old['Z'],holes=old['hole_flags']);N=old['N'];J=old.get('J',d['case']['history'][-1]['action']);orb=model.orbit(N,state.numbers(),J=J);return d,bg,model,state,N,J,orb

def old_step(bg,model,state,N,J,orb,h):
 t=T0*math.exp(-N);ev=averaged_exact_events(bg,orb['xs'],orb['weights'],t,model.q,model.W);cov,C=covariance(ev,state);k0=-3+cov/(orb['omega']*J*model.hubble(N));ns,info=implicit_step(ev,state,h/model.hubble(N+h/2),tol=2e-8,number_floor=1e-14);Jp=J*math.exp(h*k0);op=model.orbit(N+h,ns.numbers(),J=Jp);ep=averaged_exact_events(bg,op['xs'],op['weights'],t*math.exp(-h),model.q,model.W);covp,Cp=covariance(ep,ns);k1=-3+covp/(op['omega']*Jp*model.hubble(N+h));Jn=J*math.exp(h*(k0+k1)/2);on=model.orbit(N+h,ns.numbers(),J=Jn);work=h*(expansion_work(orb)+expansion_work(on))/2;return ns,Jn,on,work,dict(population_newton=info,independent_step_energy_work=float(on['E']-orb['E']+work))

def main(out):
 start=time.monotonic();path=ROOT/'reviews/collision_completion_2026_11_04/integration/run_fresh_exact002/result.json';d,bg,model,state,N,J,orb=load(path);rows=[];checks={};result=dict(claim_id='CC11_ENERGY_STAGE_DISCRIMINATOR',rows=rows,checks=checks,initial_N=N,initial_E=orb['E'],initial_J=J,initial_excitation=orb['E']-orb['minimum'])
 def save():
  result.update(runtime_seconds=time.monotonic()-start,peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss);Path(out).write_text(json.dumps(result,indent=2)+'\n')
 for h,method in [(5e-5,'old_heun'),(5e-5,'split_old_geometry'),(5e-5,'split_mid_geometry'),(2.5e-5,'split_mid_geometry')]:
  before=time.monotonic()
  try:
   if method=='old_heun':ns,Jn,on,work,info=old_step(bg,model,state,N,J,orb,h)
   else:ns,Jn,on,work,info=step(model,bg,averaged_exact_events,N,state,J,h,geometry='old' if method=='split_old_geometry' else 'midpoint',max_outer=8,outer_tol=2e-5)
   f,a=ns.arrays();delta=float(on['E']-orb['E']+work);row=dict(method=method,dN=h,completed=True,runtime=time.monotonic()-before,independent_energy_work_residual=delta,residual_over_initial_excitation=delta/(orb['E']-orb['minimum']),final_action=Jn,final_energy=on['E'],final_excitation=on['E']-on['minimum'],entropy_gain=ns.entropy()-state.entropy(),min_f=float(min(f)),max_fermion_f=float(max(f[model.eta<0])),number_L1_change=float(sum(abs(ns.numbers()-state.numbers()))),stage_info=info,final_numbers=ns.numbers().tolist())
  except RuntimeError as exc:row=dict(method=method,dN=h,completed=False,runtime=time.monotonic()-before,failure=str(exc))
  rows.append(row);print({k:v for k,v in row.items() if k not in ('final_numbers','stage_info')},flush=True);save()
 success=[r for r in rows if r['method']=='split_mid_geometry'];checks.update(midpoint_completed=all(r['completed'] for r in success),positive=all(r.get('min_f',0)>=0 and r.get('max_fermion_f',1)<=1 for r in success),entropy=all(r.get('entropy_gain',-1)>=0 for r in success),independent_energy=all(abs(r.get('residual_over_initial_excitation',1))<.01 for r in success));save();assert all(checks.values())
if __name__=='__main__':main(sys.argv[1])
