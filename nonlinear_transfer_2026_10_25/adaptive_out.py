"""Adaptive full Hamiltonian evolution with explicit transfer-work ledger."""
import argparse,json,time
from pathlib import Path
import numpy as np
from outgoing import OutgoingFull as Full
from initial import initial

def components(m,a,x,p,chi,pi):
 mt=abs(a[0])**2;mf=abs(a[1])**2;mass=mt+mf;u=m.enclosed(mt);gd=m.enclosed(mass);W,F,_,_=m.f(u);ff=m.f((u[1:]+u[:-1])/2)[1];xx=2*x/np.pi
 response=sum(m.vol*(W+m.beta*np.sin(2*x)**2/np.pi**2*F))+sum(m.tw*m.f(sum(mt)*m.tt**2)[0]/m.tt**4);grav=-sum(m.vol*(.5*gd*gd+m.gb*gd))-.5*sum(mass)**2/m.R-sum(mass)/np.sqrt(m.R*m.R+m.b*m.b);amp=np.abs(a)/np.sqrt(m.vol)[None,:];density_grad=.5*m.k*np.sum(m.w*np.sum(np.diff(amp,axis=1)**2,axis=0));kin=float(m.kinetic(a));outer=m.r*m.rm>70
 return {'gravitational_energy':float(grav),'response_energy':float(response),'F_pressure_energy':float(1.5*m.K*sum(m.vol*(mf/m.vol)**(5/3))),'binding_energy':float(-m.eps*sum(mt)),'carrier_spatial_energy':float(.5*sum(m.w*(m.ell2*ff+m.vac)*np.diff(xx)**2)),'carrier_volume_energy':float(m.B*(m.vol@np.sin(x)**2)),'alignment_energy':float(m.J*np.real(np.sum(np.conj(a)*m.alignment(a,x,chi)))),'carrier_kinetic_energy':float(.5*sum(p*p/m.Z(a))),'amplitude_gradient_energy':float(density_grad),'material_flow_energy':float(kin-density_grad),'fixed_outer_T_fraction':float(sum(mt[outer])/sum(mass[outer])),'fixed_outer_mass':float(sum(mass[outer]))}

def run(config,output):
 m=Full(wave_h_kpc=config.get('wave_h_kpc',2.),wave_R_kpc=config.get('wave_R_kpc',8000.),coupling=config.get('coupling',True));case=config['case'];dest=Path(output)
 if config.get('equilibrium'):
  old=np.load(config['equilibrium']);a=old['a'].copy();x=old['alpha'].copy();chi=np.zeros(len(m.wr));pi=chi.copy();meta={'equilibrium':config['equilibrium']}
  if case=='dilated':
   rr=m.edges*m.rm;shift=m.edges*(1+.2*np.exp(-(rr/200)**4));a=np.sqrt(np.maximum([np.diff(np.interp(m.edges,shift,np.r_[0,np.cumsum(abs(v)**2)])) for v in a],0)).astype(complex);x,_,_=m.minimize_alpha(a,chi,np.arctan2(abs(a[0]),abs(a[1])),maxit=300)
  if case.startswith('boundary_'):
   delta=(1 if case.endswith('plus') else -1)*.5/m.rm;th=np.arctan2(abs(a[0]),abs(a[1]));tn=np.interp(m.r-delta,m.r,th,left=th[0],right=th[-1]);mass=np.sum(abs(a)**2,axis=0);a=np.array([np.sqrt(mass)*np.sin(tn),np.sqrt(mass)*np.cos(tn)],complex);x,_,_=m.minimize_alpha(a,chi,np.interp(m.r-delta,m.r,x,left=x[0],right=x[-1]),maxit=300)
 else:a,x,chi,pi,meta=initial(m,case)
 p=np.zeros(m.n);E0=Eold=m.full_energy(a,x,p,chi,pi);Q0=float(m.wvol@pi+m.g*sum(abs(a[0])**2));M0=float(np.sum(abs(a)**2));wave0=m.diagnostics(a,x,chi,pi)['wave_energy'];init=m.diagnostics(a,x,chi,pi);initcomp=components(m,a,x,p,chi,pi);trace=[];sink=qs=transfer=0.;t=0.;h=config['dt_Myr'];start=time.monotonic();last_rejections=[];reject=accept=0;maxE=maxQ=maxM=maxW=0.;minh=h;status='completed';next_sample=0.;maxroot=maxfp=0.
 while t<config['duration_Myr']-1e-10:
  if time.monotonic()-start>config.get('wall_seconds',240):status='wall_limit_partial';break
  h=min(h,config['duration_Myr']-t);dt=h/m.tdyn;an,xn,pn,cn,vin,ds,dq,info=m.full_step(a,x,p,chi,pi,dt);En=m.full_energy(an,xn,pn,cn,vin);defect=En+ds-Eold;tol=max(config.get('energy_roundoff_floor',5e-13),config.get('step_energy_tolerance',1e-9)*h/config['dt_Myr']);bad=info['fixed_point_error']>1e-9 or info['carrier_root_residual']>1e-8 or abs(defect)>tol or not np.isfinite(En)
  if bad:
   last_rejections.append({'time_Myr':t,'h_Myr':h,'energy_defect':float(defect),'energy_tolerance':tol,**info});last_rejections=last_rejections[-80:];reject+=1;h*=.5
   if h<config.get('minimum_dt_Myr',1e-7):status='minimum_step_failure';break
   continue
  amid=(a+an)/2;xm=getattr(m,"last_mid_alpha",(x+xn)/2);cm=(chi+cn)/2;vm=(pi+vin)/2;rate=2*m.J/m.sigma*np.imag(np.conj(amid[0])*m.alignment(amid,xm,cm)[0]);work=-m.g*dt*sum(rate*m.chi_m(vm));transfer+=float(work);a,x,p,chi,pi=an,xn,pn,cn,vin;Eold=En;t+=h;sink+=ds;qs+=dq;accept+=1;minh=min(minh,h);maxroot=max(maxroot,info['carrier_root_residual']);maxfp=max(maxfp,info['fixed_point_error'])
  if t>=next_sample or t>=config['duration_Myr']-1e-10:
   d=m.diagnostics(a,x,chi,pi);comp=components(m,a,x,p,chi,pi);maxE=max(maxE,abs(En+sink-E0));maxQ=max(maxQ,abs(m.wvol@pi+m.g*sum(abs(a[0])**2)+qs-Q0));maxM=max(maxM,abs(d['mass']-M0));maxW=max(maxW,abs(d['wave_energy']+sink-wave0-transfer));trace.append({'time_Myr':t,'total_energy':En,'escaped_energy':sink,'net_material_to_wave_work':transfer,**d,**comp});next_sample=t+.1
   if d['cap_slack']<=0:status='physical_cap_failure';break
  if abs(defect)<tol/16 and info['iterations']<15:h=min(config['dt_Myr'],h*1.25)
 final=m.diagnostics(a,x,chi,pi);finalc=components(m,a,x,p,chi,pi);out={'config':config,'status':status,'completed_time_Myr':t,'runtime_seconds':time.monotonic()-start,'accepted_steps':accept,'rejected_steps':reject,'minimum_step_Myr':minh,'initial_meta':meta,'initial':init,'initial_components':initcomp,'initial_energy':E0,'final':final,'final_components':finalc,'escaped_energy':sink,'net_material_to_wave_work':transfer,'max_field_work_ledger_error':maxW,'max_absolute_energy_ledger_error':maxE,'max_shift_charge_ledger_error':maxQ,'max_mass_error':maxM,'max_carrier_root_residual':maxroot,'max_fixed_point_residual':maxfp,'trace':trace,'last_rejections':last_rejections,'non_claims':['Finite-carrier free density evolution; no drift assigned to escape','Adaptive local energy-defect control is numerical, not a physical loss term','Stiff-mode and spatial convergence remain mandatory','K30 barotropic F state remains a constitutive assumption','No universal galaxy-population or arbitrary initial-data conclusion']};np.savez_compressed(dest.with_name('state.npz'),a=a,alpha=x,carrier_p=p,chi=chi,pi=pi);dest.write_text(json.dumps(out,indent=2)+'\n');print({k:v for k,v in out.items() if k!='trace'},flush=True)

def main(config):
 ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();run(config,a.output)
