"""Moving-minimum discriminator: artificial excitation versus physical action."""
from one_step import *
from split_energy_v2 import collision,step

def main_small(out):
 start=time.monotonic();path=ROOT/'reviews/collision_completion_2026_11_04/history/run_refine002/result.json';d,bg,model,state,N,oldJ,oldorb=load(path);J=model.J0*1e-8;orb=model.orbit(N,state.numbers(),J=J);t=T0*math.exp(-N);ev=averaged_exact_events(bg,orb['xs'],orb['weights'],t,model.q,model.W);cov,C=covariance(ev,state);slope=cov/(orb['omega']*model.hubble(N));rows=[];checks={};result=dict(claim_id='CC11_ACTION_CENTERED_SMALL_ACTION',initial_N=N,initial_J=J,original_saved_J=oldJ,initial_excitation=orb['E']-orb['minimum'],initial_omega=orb['omega'],linear_collision_action_derivative=slope,rows=rows,checks=checks)
 def save():
  result.update(runtime_seconds=time.monotonic()-start,peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss);Path(out).write_text(json.dumps(result,indent=2)+'\n')
 save()
 for h,geometry,pop in [(1e-5,'midpoint','BE'),(2.5e-6,'midpoint','BE'),(6.25e-7,'midpoint','BE')]:
  before=time.monotonic()
  try:
   ns,Jn,on,info=collision(model,bg,averaged_exact_events,N,state,orb,h,geometry,pop,max_outer=10,outer_tol=2e-5);pred=J+h*slope;row=dict(dN=h,geometry=geometry,population=pop,completed=True,runtime=time.monotonic()-before,final_J=Jn,linear_predicted_J=pred,relative_action_excess=(Jn-pred)/J,final_excitation=on['E']-on['minimum'],minimum_displacement=on['xmid']-orb['xmid'],quench_energy_estimate=.5*62*orb['omega']**2*(on['xmid']-orb['xmid'])**2,info=info)
  except RuntimeError as exc:row=dict(dN=h,geometry=geometry,population=pop,completed=False,runtime=time.monotonic()-before,failure=str(exc))
  rows.append(row);print({k:v for k,v in row.items() if k!='info'},flush=True);save()
 finest=rows[-1];checks.update(finest_midpoint_completed=finest['completed'],physical_bounds=all(r['info']['min_f']>=0 and r['info']['max_fermion_f']<=1 for r in rows if r['completed']),finite_energy=all(r['info']['collision_energy_change']==0 for r in rows if r['completed']),small_action_floor_bounded=finest['completed'] and abs(finest['relative_action_excess'])<.01);save();assert all(checks.values())
if __name__=='__main__':main_small(sys.argv[1])
