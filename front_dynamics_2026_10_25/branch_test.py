"""Actual minimum-front branch: geometry, transport and slow radiation.

No time history or cosine potential is inserted. Conservative infall speed is
derived from the actual branch energy, starting from rest at lambda=1/16.
Its monopole radiation is a perturbative diagnostic of slow tracking only.
"""
import argparse,json,sys
from pathlib import Path
import numpy as np
from scipy.interpolate import PchipInterpolator,CubicSpline
from scipy.optimize import minimize_scalar
from scipy.integrate import simpson
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'physical_completion_2026_10_25'))
from free_formation import FreeVacuum
from joint import T

class Branch:
 def __init__(self,order=24):
  self.m=m=FreeVacuum();self.ini=json.loads(Path('physical_completion_2026_10_25/run_free_formation/all_F.json').read_text());self.fin=json.loads(Path('physical_completion_2026_10_25/run_free_finish/formed.json').read_text())
  self.m0=np.array(self.ini['mass']);self.m1=np.array(self.fin['mass']);self.dm=self.m1-self.m0;self.rad=m.r.numpy();self.vol=m.vol.numpy();self.Rf=self.fin['scaled_boundary_kpc']/m.rm
  self.xf=np.array(self.fin['v'][m.n:]);self.profile=PchipInterpolator(self.rad,self.xf,extrapolate=False)
  self.edges=np.r_[0,np.cumsum(np.zeros(m.n))]
  for i,r in enumerate(self.rad):self.edges[i+1]=2*r-self.edges[i]
  nd,wt=np.polynomial.legendre.leggauss(order);self.rr=(self.edges[1:,None]+self.edges[:-1,None])/2+np.diff(self.edges)[:,None]*nd/2;self.ww=np.diff(self.edges)[:,None]*wt/2
  self.rho0=self.m0/self.vol;self.drho=self.dm/self.vol
  self.Q=np.r_[0,np.cumsum(self.dm)][:-1,None]+self.drho[:,None]*(self.rr**3-self.edges[:-1,None]**3)/3
  self.k=(m.material_length/m.rm)**2;self.J=30.
  kpc=3.085677581491367e19;Myr=365.25*86400*1e6;v=np.sqrt(9.3603e-11*m.rm*kpc)
  self.tdyn=m.rm*kpc/v/Myr;self.c=299792458/v
  # Same physical coupling as the preceding binding prototype (Dnorm=.25).
  si=json.loads(Path('selective_stress_2026_10_25/run_spinor_inertia/results.json').read_text());Mt=si['converted_mass_Mb'];D=si['cases'][0]['conversion_potential_Eunit']
  radius=json.loads(Path('physical_completion_2026_10_25/run_two_field/J_30.0.json').read_text())['scaled_boundary_kpc']/m.rm
  self.g=np.sqrt(D/.25)*3*radius**1.5/Mt
 def phase(self,r,R):
  z=r+self.Rf-R;inside=(z>=self.rad[0])&(z<=self.rad[-1]);x=np.where(z<self.rad[0],1.,0.);dx=np.zeros_like(z)
  x[inside]=self.profile(z[inside]);dx[inside]=self.profile(z[inside],1)
  return x,dx
 def potential(self,L,R,grad=False):
  mass=self.m0+L*self.dm;x,dx=self.phase(self.rad,R)
  if not grad:return float(self.m.energy(T(np.log(mass)),T(x)))
  E,gg=self.m.fg(np.r_[np.log(mass),x]);return E,np.array([gg[:self.m.n]@(self.dm/mass),-gg[self.m.n:]@dx])
 def tensors(self,L,R):
  rho=(self.rho0+L*self.drho)[:,None];vel=-self.Q/(self.rr**2*rho);x,xr=self.phase(self.rr,R);theta_r=np.pi*xr/2;qr=np.pi/2*np.sin(np.pi*x)*xr;dv=self.ww*self.rr**2
  coeff=np.stack([-self.Q*qr/self.rr**2,-rho*qr],axis=-1);w=2*self.k*rho*theta_r**2/self.J
  vv=np.stack([vel,-np.ones_like(vel)],axis=-1);G=np.einsum('ij,ija,ijb->ab',dv*w,vv,vv);G[0,0]+=np.sum(self.ww*self.Q**2/(self.rr**2*rho))
  f=(coeff*dv[...,None]).reshape(-1,2);prev=np.cumsum(f,axis=0)-f;rinv=1/self.rr.ravel()
  D=np.einsum('i,ia,ib->ab',rinv,f,f)+np.einsum('i,ia,ib->ab',rinv,f,prev)+np.einsum('i,ia,ib->ab',rinv,prev,f)
  Gwave=self.g**2/self.c**2*D
  return dict(G=G+Gwave,Gbare=G,Gwave=Gwave,coeff=coeff,dv=dv,rho=rho,qr=qr,vel=vel,MT=float(np.sum(dv*rho*np.sin(np.pi*x/2)**2)))
 def continuous_mass(self,L,R):return self.tensors(L,R)['MT']
 def audit(self):
  L=.5;R=self.Rf-.05;t=self.tensors(L,R);h=1e-5
  fd=np.array([(self.continuous_mass(L+h,R)-self.continuous_mass(L-h,R))/(2*h),(self.continuous_mass(L,R+h)-self.continuous_mass(L,R-h))/(2*h)])
  integ=np.sum(t['dv'][...,None]*t['coeff'],axis=(0,1))
  E,grad=self.potential(L,R,True);d=np.array([.3,-.7]);fdE=(self.potential(L+h*d[0],R+h*d[1])-self.potential(L-h*d[0],R-h*d[1]))/(2*h)
  return {'mass_error':float(max(abs(sum(self.m0)-sum(self.m1)),abs(sum(self.m0)-5.364))),'integrated_source':integ.tolist(),'MT_gradient_finite_difference':fd.tolist(),'source_identity_relative_error':float(np.linalg.norm(integ-fd)/np.linalg.norm(fd)),'energy_chain_rule_relative_error':float(abs(fdE-grad@d)/max(abs(fdE),1e-12)),'metric_eigenvalues':np.linalg.eigvalsh(t['G']).tolist(),'scalar_added_metric_eigenvalues':np.linalg.eigvalsh(t['Gwave']).tolist(),'endpoint_energy_errors':[self.potential(0,-20/self.m.rm)-self.ini['energy'],self.potential(1,self.Rf)-self.fin['energy']]}
 def run(self,n):
  # Resolve both the early front adjustment and the approach to final density.
  L=np.unique(np.r_[np.linspace(1/16,.9,n),1-np.geomspace(.1,.0001,n//2)])
  rows=[]
  for l in L:
   opt=minimize_scalar(lambda R:self.potential(l,R),bounds=(45/self.m.rm,65/self.m.rm),method='bounded',options={'xatol':1e-11})
   R=opt.x;E,gr=self.potential(l,R,True);hh=1e-4
   H=np.column_stack([(self.potential(l+hh,R,True)[1]-self.potential(l-hh,R,True)[1])/(2*hh),(self.potential(l,R+hh,True)[1]-self.potential(l,R-hh,True)[1])/(2*hh)])
   slope=-H[1,0]/H[1,1];t=self.tensors(l,R);v=np.array([1.,slope]);G=float(v@t['G']@v)
   # All density diagnostics are genuine for this restricted profile, and
   # positivity is guaranteed by interpolation, not by an evolution solver.
   mass=self.m0+l*self.dm;gb=self.rad/(self.rad**2+self.m.b**2)**1.5;gt=gb+self.m.B.numpy()@mass/self.rad**2;law=(gb+np.sqrt(gb*gb+4*gb))/2;err=np.log10(gt/law);rr=self.rad*self.m.rm;sel=(rr>=1.5)&(rr<=50);bound=(10**max(max(abs(err[sel])),max(abs(np.interp([1.5,50],rr,err))))-1)*100
   PR=float(t['G'][1]@v);dRG=(self.tensors(l,R+hh)['G']-self.tensors(l,R-hh)['G'])/(2*hh);dRpath=float(v@dRG@v)
   rows.append([l,R,E,gr[0],gr[1],H[1,1],slope,G,t['MT'],bound,float(t['Gbare'][1,1]),float(min(.9997-self.m.A.numpy()@(mass*np.sin(np.pi*self.phase(self.rad,R)[0]/2)**2))),float(t['G'][1,1]),PR,dRpath])
  a=np.array(rows);ls=a[:,0];R=a[:,1];E=a[:,2];Gp=CubicSpline(ls,a[:,7]);Ms=CubicSpline(ls,a[:,8]);Vp=CubicSpline(ls,E);drop=E[0]-E
  speed=np.sqrt(np.maximum(2*drop/a[:,7],0));acc=(-a[:,3]-.5*Gp(ls,1)*speed**2)/a[:,7];gamma=Ms(ls,1)*speed;gammadot=Ms(ls,2)*speed**2+Ms(ls,1)*acc
  # Singular 1/sqrt(lambda-lambda0) time integral: use lambda=lambda0+s².
  ss=np.linspace(0,np.sqrt(ls[-1]-ls[0]),4*n+1);ll=ls[0]+ss**2;dd=Vp(ls[0])-Vp(ll);vv=np.sqrt(np.maximum(2*dd/Gp(ll),0));integrand=np.divide(2*ss,vv,out=np.zeros_like(ss),where=vv>0);integrand[0]=np.sqrt(2*a[0,7]/(-a[0,3]));times=np.r_[0,np.cumsum((integrand[1:]+integrand[:-1])*np.diff(ss)/2)]*self.tdyn
  # Lowest-order outgoing monopole power in the radial dV=r²dr convention.
  aa=(-Vp(ll,1)-.5*Gp(ll,1)*vv**2)/Gp(ll);gd=Ms(ll,2)*vv**2+Ms(ll,1)*aa
  power=self.g**2/self.c**3*gd**2;Erad=float(simpson(power*integrand,x=ss));omega=np.sqrt(a[:,5]/a[:,10]);omegadressed=np.sqrt(a[:,5]/a[:,12])
  PRs=CubicSpline(ls,a[:,13]);forcing=a[:,13]*acc+(PRs(ls,1)-.5*a[:,14])*speed**2;offset=-forcing/a[:,5]
  return {'grid_size':n,'columns':['lambda','R_dimensionless','V','V_lambda','V_R','V_RR','Rprime_lambda','G_along_branch','MT_continuous','law_bound_percent','G_RR_bare','cap_slack','G_RR_dressed','G_R_along_branch','partial_R_G_along_branch'],'rows':rows,'release_after_start':float(drop[-1]),'infall_time_Myr':float(times[-1]),'slow_monopole_radiated_energy_Eunit':Erad,'slow_radiation_over_release':Erad/drop[-1],'minimum_bare_front_inverse_frequency_Myr':float(min(self.tdyn/omega)),'maximum_bare_front_inverse_frequency_Myr':float(max(self.tdyn/omega)),'min_dressed_front_inverse_frequency_Myr':float(min(self.tdyn/omegadressed)),'max_dressed_front_inverse_frequency_Myr':float(max(self.tdyn/omegadressed)),'maximum_inertial_tracking_offset_kpc':float(max(abs(offset))*self.m.rm),'maximum_quadratic_offset_energy_Eunit':float(max(.5*a[:,5]*offset**2)),'max_speed_lambda_per_Myr':float(max(speed)/self.tdyn),'max_R_tracking_speed_kpc_per_Myr':float(max(abs(a[:,6]*speed))*self.m.rm/self.tdyn),'max_boundary_force_residual':float(max(abs(a[:,4]))),'min_boundary_curvature':float(min(a[:,5])),'lambda_to_1percent_law':float(ls[np.where(a[:,9]<=1)[0][0]]) if np.any(a[:,9]<=1) else None,'time_grid_Myr':times.tolist(),'lambda_time_grid':ll.tolist(),'max_abs_integrated_conversion_rate_per_Myr':float(max(abs(gamma))/self.tdyn),'coupling_original_units':self.g,'c_original_units':self.c,'tdyn_Myr':self.tdyn,'leading_monopole_note':'Perturbative slow tracking source only; no artificial temporal cutoff radiation is counted. Initial slow acceleration specified by actual potential and rest data. Does not count initial nucleus/front transient or nonlinear fast excitation.'}

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();b=Branch();audit=b.audit();assert audit['mass_error']<1e-10;assert max(abs(np.array(audit['endpoint_energy_errors'])))<1e-9;assert audit['energy_chain_rule_relative_error']<1e-5
 out={'audit':audit,'runs':[],'non_claims':['Adiabatic minimum-front branch, not integrated two-coordinate evolution','Positive density and final law on this restricted manifold do not prove unconstrained formation','Radiation is leading slow monopole perturbation; no fast front pump or nonlinear outer-reservoir stability tested','Minimum branch search restricted to 45--65 kpc and lambda>=1/16','Canonical internal inertia assumes alignment J=30 while static energy uses locked profiles']}
 for n in [81,161]:
  r=b.run(n);out['runs'].append(r);Path(a.output).write_text(json.dumps(out,indent=2)+'\n');print({k:v for k,v in r.items() if k not in ['rows','time_grid_Myr','lambda_time_grid']},flush=True)
