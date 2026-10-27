"""Enclosed-mass acceleration resolved into every Hamiltonian force."""
import argparse,json
from pathlib import Path
import numpy as np
from dynamics import model,load,field
p=argparse.ArgumentParser();p.add_argument('--output',required=True);args=p.parse_args();m=model();rows=[]
for name,path,t in [('quiet_initial','infall_pump_2026_10_25/run_smooth_prepare/state.npz',0.),('first_pulse','infall_pump_2026_10_25/run_smooth_infall/state.npz',5.7),('continued','sustained_transport_2026_10_26/run_continue/state.npz',None)]:
 z=load(path);a,x,cp,c,v=z;mt=abs(a[0])**2;mf=abs(a[1])**2;mass=mt+mf;rho=mt/m.vol;cm=m.true_chi_m(c);vm=m.true_chi_m(v);mu=m.pot(a,x,True)[1];u=m.enclosed(mt);gd=m.enclosed(mass);omega=cp/m.Z(a);extra,S,b,conv,U,G=m.transfer(a,x,c)
 muG=-m.transpose(m.vol*(gd+m.gb))-np.sum(mass)/m.R-1/np.sqrt(m.R**2+m.b**2);muR=mu[0]-muG+m.eps
 def local(ut,uf):return np.array([ut*a[0],uf*a[1]])
 kin=m.kd*a.copy();kin[0,:-1]+=m.ko*U*a[0,1:];kin[0,1:]+=m.ko*np.conj(U)*a[0,:-1];kin[1,:-1]+=m.ko*a[1,1:];kin[1,1:]+=m.ko*a[1,:-1]
 Hin={'gravity':local(muG,muG),'response':local(muR,0),'F_pressure':local(0,mu[1]-muG),'binding':local(-m.eps,0),'covariant_gradient':kin,'alignment':m.J*m.alignment(a,x,c),'carrier_density_inertia':local(-(2/np.pi)**2*m.ell2/m.c**2*m.transpose(.5*m.vol*omega**2*m.f(u)[3]),0),'current_density_companions':local(extra,0)}
 ads={k:-1j*H/m.sigma for k,H in Hin.items()};ff=field(m,z);ad=sum(ads.values());assert np.max(abs(ad-ff[0]))<1e-9
 psi=a/np.sqrt(m.vol);D=np.conj(psi[0,:-1])*U*psi[0,1:];D_F=np.conj(psi[1,:-1])*psi[1,1:]
 def jdot(ad,cv):
  md=2*np.real(np.conj(a)*ad);rd=md[0]/m.vol;psid=ad/np.sqrt(m.vol);cmv=m.true_chi_m(cv)
  bd=m.g2/m.sigma*(2*rd[1:]*cm[1:]+2*rho[1:]*cmv[1:]-2*rd[:-1]*cm[:-1]-2*rho[:-1]*cmv[:-1]-.5*(rd[1:]+rd[:-1])*np.diff(cm)-.5*(rho[1:]+rho[:-1])*np.diff(cmv))
  dt=np.conj(psid[0,:-1])*U*psi[0,1:]+np.conj(psi[0,:-1])*U*psid[0,1:]+1j*bd*D
  df=np.conj(psid[1,:-1])*psi[1,1:]+np.conj(psi[1,:-1])*psid[1,1:]
  return m.k/m.sigma*m.w*np.imag(dt+df)
 budget={k:jdot(aa,np.zeros_like(v)) for k,aa in ads.items()};budget['scalar_phase_backreaction']=jdot(np.zeros_like(a),v)
 J=m.k/m.sigma*m.w*np.imag(D+D_F);JD=sum(budget.values());cases=[]
 for R in [10,25,50]:
  rr=m.r*m.rm;i=np.searchsorted(rr,R)-1;f=(R-rr[i])/(rr[i+1]-rr[i]);w=np.zeros(m.n);w[:i]=1;w[i]=.5+.5*f;w[i+1]=.5*f;dw=np.diff(w)
  acc={k:float(dw@jd/m.tdyn**2) for k,jd in budget.items()};rate=float(dw@J/m.tdyn);mdot=float(w@np.sum(2*np.real(np.conj(a)*ff[0]),axis=0)/m.tdyn)
  direct=[]
  for eps in [1e-7,3e-8,1e-8]:
   vals=[]
   for sign in [1,-1]:
    zz=tuple(y+sign*eps*dy for y,dy in zip(z,ff));aa,xx,pp,cc,vv=zz;UU=m.geometry(aa,cc)[3];ps=aa/np.sqrt(m.vol);jj=m.k/m.sigma*m.w*np.imag(np.conj(ps[0,:-1])*UU*ps[0,1:]+np.conj(ps[1,:-1])*ps[1,1:]);vals.append(float(dw@jj))
   direct.append({'epsilon':eps,'acceleration_Mb_Myr2':(vals[0]-vals[1])/(2*eps*m.tdyn**2)})
  assert abs(rate-mdot)<1e-11
  cases.append({'radius_kpc':R,'enclosed_mass_Mb':float(w@mass),'inward_mass_rate_Mb_Myr':rate,'force_acceleration_components_Mb_Myr2':acc,'net_acceleration_Mb_Myr2':sum(acc.values()),'finite_difference_acceleration_checks':direct,'continuity_error':rate-mdot})
 if t is None:t=json.loads(Path(path).with_name('results.json').read_text())['completed_time_Myr']
 rows.append({'state':name,'time_Myr':t,'source_integral':float(np.sum(S)),'bulk_integral':float(np.sum(b)),'conversion_integral':float(np.sum(conv)),'full_force_reconstruction_error':float(np.max(abs(ad-ff[0]))),'radii':cases})
res={'cases':rows,'derivation':'Exact edge current differentiated with all material Hamiltonian forces plus rho-dot and chi-dot covariant-phase companions. Conversion cancels from total-mass continuity. Components depend on canonical representation; only their sum is physical.','non_claim':'An instantaneous acceleration is not a constant-acceleration forecast or a long-time formation proof.'};Path(args.output).write_text(json.dumps(res,indent=2)+'\n');print([{ 'state':r['state'],'time':r['time_Myr'],'R50':r['radii'][-1]} for r in rows])
