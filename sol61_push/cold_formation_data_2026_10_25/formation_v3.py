"""Registered diffuse-field formation branch; no feedback from passive cohorts."""
import argparse,json,time,resource,hashlib,subprocess,sys,platform
from pathlib import Path
import numpy as np
from radial_v2 import Radial,phi_shell
from stars_v2 import Background,Cold,Cohort
P=Path(__file__).resolve().parent
META=P.parent/'cold_full_envelope_data_2026_10_25/fit_002/result.json'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--galaxy',required=True);ap.add_argument('--ne',type=int,default=1024);ap.add_argument('--dt',type=float,default=.005);ap.add_argument('--T',type=float,default=8);ap.add_argument('--wall',type=float,default=240);ap.add_argument('--out',required=True);args=ap.parse_args();out=Path(args.out);out.mkdir(parents=True,exist_ok=True);assert not (out/'result.json').exists()
 paths=[P/'CONTRACT.md',P/'radial.py',P/'stars.py',P/'formation_v3.py',P/'RESOLUTION_FOLLOWUP.md',P/'SUPPLEMENT_V2.md',P/'radial_v2.py',P/'stars_v2.py',P/'test_radial.py',P/'test_stars.py',META];before={str(p.relative_to(P.parent.parent)):digest(p) for p in paths};rev=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip();start=time.monotonic()
 d=json.loads(META.read_text())['datasets'][args.galaxy];G=.00430091;a0=9.3603e-11*3.085677581491367e10;M=.5*d['supply_Msun'];R0=np.sqrt(G*M/(.1*a0));V=np.sqrt(G*M/R0);tu=.97779222168*R0/V;aa=np.array(d['tracer_scales_pc'])/R0;q=d['stellar_mass_Msun']/M
 pb=lambda r:sum(-q/len(aa)/np.sqrt(r*r+a*a) for a in aa)
 s=Radial(args.ne,1500/(R0*V),10/V,alpha=10.,pb=pb);u=s.gaussian();phi=phi_shell(s.r,abs(u)**2);mass0=float(np.vdot(u,u).real);E0=s.energy(u,phi);scale=s.kinetic(u)+abs(float(.5*np.sum(abs(u)**2*phi)))+abs(float(np.sum(abs(u)**2*s.pb)));bg=Background(q,aa,a0*R0/V**2);cohorts=[];birth_controls=[];birth_failures=[];tag=None;tag0=None;hist=[];times=[];states=[];tags=[];potentials=[];flows=[];lastsave=-1;status='finished';t=0.;maxes=dict(mass=0.,energy=0.,phase=0.,boundary=0.,solver=0.,tag=0.);gates=[]
 def birth(t):
  for j,a in enumerate(aa):
   try:
    c=Cohort(s.r,abs(u)**2,bg,a,1024,1025+j,t)
    if c.controls['cdf_max_decrease']>1e-6 or c.controls['moment_control_relative_error']>.01:raise ValueError('birth DF control '+str(c.controls))
    birth_controls.append(dict(t=t,population=j,**c.controls));cohorts.append(c)
   except ValueError as e:birth_failures.append(dict(t=t,population=j,error=str(e)))
 def save(t,force=False):
  nonlocal lastsave
  if force or t-lastsave>=.099999:
   m=abs(u)**2;row=dict(t=t,time_Myr=t*tu,mass=float(m.sum()),energy=s.energy(u,phi),phase_bad=s.phase_bad(u),boundary_mass=float(m[s.r>.85*s.R].sum()),cold_in_reference_radius=float(m[s.r<d['observed_rhalf_pc']/R0].sum()),r50=float(np.interp(.5*mass0,np.cumsum(m),s.r)),cohorts=[c.diag(t,Cold(s.r,m)) for c in cohorts]);hist.append(row);lastsave=t
  if force or abs(t*2-round(t*2))<1e-7:
   times.append(t);states.append(u.copy());potentials.append(phi.copy());tags.append(np.zeros_like(s.r) if tag is None else tag.copy());flows.append(s.transport.copy())
 birth(0.);save(0.,True)
 for it in range(round(args.T/args.dt)):
  old=Cold(s.r,abs(u)**2);un,pn,tn,info=s.step(u,phi,args.dt,tag)
  maxes['solver']=max(maxes['solver'],info['residual'])
  if not info['converged']:status='solver stop';break
  u,phi,tag=un,pn,tn;t=(it+1)*args.dt;m=abs(u)**2;new=Cold(s.r,m)
  for c in cohorts:c.advance(old,new,args.dt)
  if abs(t-4)<args.dt*.01:
   birth(t);tag=m*(s.r<d['observed_rhalf_pc']/R0);tag0=float(tag.sum())
  maxes['mass']=max(maxes['mass'],abs(m.sum()/mass0-1));maxes['energy']=max(maxes['energy'],abs(s.energy(u,phi)-E0)/scale);maxes['phase']=max(maxes['phase'],s.phase_bad(u));maxes['boundary']=max(maxes['boundary'],float(m[s.r>.85*s.R].sum()))
  if tag is not None:maxes['tag']=max(maxes['tag'],abs(tag.sum()-tag0),float(np.max(-tag)),float(np.max(tag-m)))
  save(t)
  if maxes['mass']>1e-8 or maxes['energy']>1e-4 or maxes['phase']>.05 or maxes['boundary']>1e-4 or maxes['tag']>1e-8:status='numerical gate stop';break
  if resource.getrusage(resource.RUSAGE_SELF).ru_maxrss>750_000_000:status='memory stop';break
  if time.monotonic()-start>args.wall:status='wall stop';break
 save(t,True)
 np.savez_compressed(out/'field.npz',r=s.r,w=s.w,p=s.p,t=times,u=states,phi=potentials,tag=tags,transport=flows)
 starstates={}
 for i,c in enumerate(cohorts):
  starstates.update({str(i)+'_x':c.x,str(i)+'_v':c.v,str(i)+'_xc':c.xc,str(i)+'_vc':c.vc,str(i)+'_work':c.work})
 np.savez_compressed(out/'stars.npz',**starstates)
 # Independent passive-source warning: changes in cohort enclosed stellar mass versus fixed Plummer source.
 new=Cold(s.r,abs(u)**2)
 source_change=[]
 for c in cohorts:
  grid=np.geomspace(c.a*.1,c.a*10,100);rad=np.sort(np.linalg.norm(c.x,axis=1));emp=np.searchsorted(rad,grid)/len(rad);target=grid**3/(grid*grid+c.a*c.a)**1.5;gc=new.g(grid);delta=q/len(aa)*abs(emp-target)/grid**2
  source_change.append(dict(birth=c.birth,a_code=c.a,max_delta_baryon_Newton_force_over_cold=float(np.max(delta/np.maximum(gc,1e-30))),max_stellar_CDF_change=float(np.max(abs(emp-target)))))
 stellar_valid=not birth_failures and all(c.max_ledger<=.01 and c.max_frozen_drift<=.01 and not c.substep_cap_exceeded for c in cohorts)
 result=dict(birth_controls=birth_controls,alpha=s.alpha,stellar_numerics_valid=stellar_valid,scope='spherical zero-spin CCT proxy; fixed baryon source/passive stars; finite formation branch',galaxy=args.galaxy,status=status,t=t,requested_T=args.T,ne=args.ne,dt=args.dt,units=dict(M_Msun=M,R_pc=R0,V_kms=V,t_Myr=tu,eta_code=s.eta,vin_code=10/V,q=q,a0_code=bg.a0),initial=dict(mass=mass0,energy=E0,energy_scale=scale),maxima=maxes,birth_failures=birth_failures,source_backreaction_omitted_estimates=source_change,history=hist,seconds=time.monotonic()-start,peak_RSS_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,inputs_before=before,inputs_after={str(p.relative_to(P.parent.parent)):digest(p) for p in paths},revision_before=rev,revision_after=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),software=dict(python=sys.version,numpy=np.__version__,platform=platform.platform()))
 (out/'result.json').write_text(json.dumps(result,indent=2));print(json.dumps({k:result[k] for k in ['galaxy','status','t','maxima','seconds','peak_RSS_bytes','birth_failures']}),flush=True)
if __name__=='__main__':main()
