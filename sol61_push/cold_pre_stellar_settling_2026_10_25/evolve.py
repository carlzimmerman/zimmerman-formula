"""Cold-first adaptive formation; star birth chosen by dynamics, not data score."""
import argparse,json,time,resource,hashlib,subprocess,sys,platform
from pathlib import Path
import numpy as np
from kernel import Solver
from stars_v2 import Background,Cold,Cohort
P=Path(__file__).resolve().parent;ROOT=P.parents[1];META=P.parent/'cold_full_envelope_data_2026_10_25/fit_002/result.json'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--galaxy',required=True);ap.add_argument('--ne',type=int,required=True);ap.add_argument('--tol',type=float,required=True);ap.add_argument('--T',type=float,default=8);ap.add_argument('--wall',type=float,default=480);ap.add_argument('--out',required=True);a=ap.parse_args();out=Path(a.out);out.mkdir(parents=True,exist_ok=True);assert not(out/'result.json').exists();start=time.monotonic();rev=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip();paths=[P/f for f in ['evolve.py','kernel.py','CONTRACT.md','test_kernel.py']]+[P.parent/'cold_formation_data_2026_10_25'/f for f in ['radial_v4.py','radial_v2.py','stars_v2.py']]+[META];before={str(f.relative_to(ROOT)):sha(f) for f in paths}
 data=json.loads(META.read_text())['datasets'][a.galaxy];G=.00430091;a0=9.3603e-11*3.085677581491367e10;M=.5*data['supply_Msun'];R=np.sqrt(G*M/(.1*a0));V=np.sqrt(G*M/R);tu=.97779222168*R/V;aa=np.array(data['tracer_scales_pc'])/R;q=data['stellar_mass_Msun']/M;pb=lambda r:sum(-q/len(aa)/np.sqrt(r*r+b*b) for b in aa);s=Solver(a.ne,eta=1500/(R*V),vin=10/V,alpha=10,pb=pb);u=s.gaussian();phi=s.phi(u);M0=float(np.vdot(u,u).real);E0=s.energy(u,phi);escale=s.kinetic(u)+abs(.5*np.sum(abs(u)**2*phi))+abs(np.sum(abs(u)**2*s.pb));ref=data['observed_rhalf_pc']/R;cdfgrid=np.geomspace(.05,10,100);bg=Background(q,aa,a0*R/V**2);cohorts=[];birth_controls=[];birth_failures=[];birth_time=None;history=[];savedt=[];savedu=[];savedphi=[];t=0.;h=.000625;nextdiag=.05;status='finished';accepted=0;rejected=0;consecutive=0;its=0;dtmin=float('inf');dtmax=0.;maxerr=0.;maxsolver=0.;accepted_solver=0.;maxima=dict(mass=0.,energy=0.,phase=0.,boundary=0.);settling_records=[];numerical_exception=None
 def snapshot():
  if savedt and abs(savedt[-1]-t)<1e-10:return
  savedt.append(t);savedu.append(u.copy());savedphi.append(phi.copy())
 def diagnostic(valid=True):
  m=abs(u)**2;cdf=np.cumsum(m);row=dict(t=t,time_Myr=t*tu,mass=float(m.sum()),energy=s.energy(u,phi),cold_Mref=float(m[s.r<ref].sum()),r50=float(np.interp(.5*M0,cdf,s.r)),cdf=np.interp(cdfgrid,s.r,cdf).tolist(),numerically_valid=valid,cohorts=[c.diag(t,Cold(s.r,m)) for c in cohorts]);history.append(row);return row
 def settling():
  if t<2:return False
  window=[x for x in history if t-1-1e-9<=x['t']<=t]
  if len(window)<20 or not all(x['numerically_valid'] for x in window):return False
  cc=np.array([x['cdf'] for x in window]);mm=np.array([x['cold_Mref'] for x in window]);rr=np.array([x['r50'] for x in window]);cd=float(np.max(np.ptp(cc,axis=0))/M0);md=float(np.ptp(mm)/max(mm.mean(),1e-12));rd=float(np.ptp(rr)/rr.mean());ok=cd<=.01 and md<=.05 and rd<=.05;settling_records.append(dict(t=t,CDF_range=cd,reference_mass_relative_range=md,r50_relative_range=rd,qualifies=ok));return ok
 def birth():
  nonlocal birth_time
  birth_time=t
  for j,b in enumerate(aa):
   try:
    c=Cohort(s.r,abs(u)**2,bg,b,1024,1025+j,t)
    if not np.all(np.isfinite(c.x)) or not np.all(np.isfinite(c.v)) or not all(np.isfinite(v) for k,v in c.controls.items() if isinstance(v,(float,int))) or c.controls['cdf_max_decrease']>1e-6 or c.controls['moment_control_relative_error']>.01:raise ValueError('birth DF controls '+str(c.controls))
    birth_controls.append(dict(t=t,population=j,**c.controls));cohorts.append(c)
   except ValueError as ex:birth_failures.append(dict(t=t,population=j,error=str(ex)))
 diagnostic();snapshot()
 while t<a.T-1e-12:
  if time.monotonic()-start>a.wall:status='wall stop';break
  if resource.getrusage(resource.RUSAGE_SELF).ru_maxrss>750000000:status='memory stop';break
  hh=min(h,a.T-t,nextdiag-t);old_u=u;old_phi=phi
  try:un,pn,error,info=s.doubled(u,phi,hh)
  except (np.linalg.LinAlgError,ValueError,FloatingPointError) as ex:numerical_exception=repr(ex);status='solver exception stop';break
  its+=info['iterations'];maxsolver=max(maxsolver,info['residual'])
  if not info['converged'] or not np.isfinite(error) or error>a.tol:
   rejected+=1;consecutive+=1;factor=.5 if not np.isfinite(error) else max(.2,min(.8,.8*(a.tol/max(error,1e-300))**.2));h=hh*factor
   if h<1e-8 or consecutive>60:status='time/solver resolution stop';break
   continue
  consecutive=0;accepted+=1;accepted_solver=max(accepted_solver,info['residual']);dtmin=min(dtmin,hh);dtmax=max(dtmax,hh);maxerr=max(maxerr,error);u,phi=un,pn;t+=hh;m=abs(u)**2
  if cohorts:
   cold0=Cold(s.r,abs(old_u)**2);cold1=Cold(s.r,m)
   for c in cohorts:c.advance(cold0,cold1,hh)
  maxima['mass']=max(maxima['mass'],abs(m.sum()/M0-1));maxima['energy']=max(maxima['energy'],abs(s.energy(u,phi)-E0)/escale);maxima['phase']=max(maxima['phase'],s.phase_bad(u));maxima['boundary']=max(maxima['boundary'],float(m[s.r>.85*s.R].sum()));valid=np.all(np.isfinite(u)) and np.all(np.isfinite(phi)) and np.isfinite(s.energy(u,phi)) and maxima['mass']<=1e-8 and maxima['energy']<=1e-4 and maxima['phase']<=.05 and maxima['boundary']<=1e-4
  if not valid:status='spatial/invariant/boundary stop';diagnostic(False);break
  if abs(t-nextdiag)<1e-9:
   t=nextdiag;diagnostic()
   if birth_time is None and settling():birth();snapshot()
   if abs(t*2-round(t*2))<1e-7:
    snapshot();print(json.dumps(dict(progress_t=t,accepted=accepted,rejected=rejected,birth_time=birth_time)),flush=True)
   nextdiag=round(nextdiag+.05,10)
  if birth_time is not None and t>=birth_time+2-1e-12:status='completed post-birth interval';break
  h=min(.005,hh*min(1.8,max(.5,.85*(a.tol/max(error,1e-300))**.2)))
 diagnostic(status not in ['spatial/invariant/boundary stop']);snapshot();np.savez_compressed(out/'field.npz',r=s.r,w=s.w,p=s.p,t=savedt,u=savedu,phi=savedphi);st={}
 for j,c in enumerate(cohorts):st.update({str(j)+'_x':c.x,str(j)+'_v':c.v,str(j)+'_xc':c.xc,str(j)+'_vc':c.vc,str(j)+'_work':c.work})
 np.savez_compressed(out/'stars.npz',**st);cold=Cold(s.r,abs(u)**2);source=[]
 for c in cohorts:
  rr=np.geomspace(c.a*.1,c.a*10,100);emp=np.searchsorted(np.sort(np.linalg.norm(c.x,axis=1)),rr)/len(c.x);target=rr**3/(rr*rr+c.a*c.a)**1.5;delta=q/len(aa)*abs(emp-target)/rr**2;source.append(dict(birth=c.birth,max_delta_baryon_Newton_force_over_cold=float(np.max(delta/np.maximum(cold.g(rr),1e-30))),max_stellar_CDF_change=float(np.max(abs(emp-target)))))
 stellar_valid=None if birth_time is None else (not birth_failures and all(c.max_ledger<=.01 and c.max_frozen_drift<=.01 and not c.substep_cap_exceeded for c in cohorts))
 result=dict(scope='CCT spherical cold-first finite branch; fixed supported baryon source/passive later stars; not action or permanent settlement',galaxy=a.galaxy,status=status,numerical_exception=numerical_exception,t=t,T=a.T,ne=a.ne,alpha=10,local_tolerance=a.tol,accepted=accepted,rejected=rejected,total_solver_iterations=its,accepted_dt_range=[None if accepted==0 else dtmin,dtmax],accepted_local_error_max=maxerr,accepted_solver_residual_max=accepted_solver,all_attempts_solver_residual_max=maxsolver,maxima=maxima,units=dict(M_Msun=M,R_pc=R,V_kms=V,t_Myr=tu,eta_code=s.eta,vin_code=10/V,q=q),initial=dict(mass=M0,energy=E0,energy_scale=float(escale)),birth_time=birth_time,birth_controls=birth_controls,birth_failures=birth_failures,stellar_numerics_valid=stellar_valid,source_backreaction_omitted_estimates=source,settling=settling_records,history=history,seconds=time.monotonic()-start,peak_RSS_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,raw_sha256={f:sha(out/f) for f in ['field.npz','stars.npz']},inputs_before=before,inputs_after={str(f.relative_to(ROOT)):sha(f) for f in paths},revision_before=rev,revision_after=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),software=dict(python=sys.version,numpy=np.__version__,platform=platform.platform()));(out/'result.json').write_text(json.dumps(result,indent=2));print(json.dumps({k:result[k] for k in ['galaxy','status','t','accepted','rejected','maxima','birth_time','stellar_numerics_valid','seconds','peak_RSS_bytes']}),flush=True)
if __name__=='__main__':main()
