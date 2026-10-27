"""Equilibrate composition/carrier ONLY for initial data; density later free.

Same displaced total density and total mass. No loss during this preparation
is counted as radiation. No target galaxy density or fixed boundary imposed.
"""
import argparse,json,time
from pathlib import Path
import numpy as np
from scipy.sparse import lil_matrix,csc_matrix
from scipy.sparse.linalg import splu
from scipy.optimize._numdiff import approx_derivative,group_columns
from live_collocated import Collocated
from smooth_initial import fine_initial
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args();dest=Path(args.output)
m=Collocated(eta=.01,material_h_kpc=.125,wave_R_kpc=10000.);a,x,c,v,meta=fine_initial(m,'dilated','nonlinear_transfer_2026_10_25/run_exact_equilibrium/state.npz');n=m.n;mass=np.sum(abs(a)**2,axis=0);rootmass=np.sqrt(mass);theta=np.arctan2(abs(a[0]),abs(a[1]));ct=m.enclosed(abs(a[0])**2)*m.r**2;cts=np.maximum(ct,1e-20*m.r**2);scales=np.r_[np.ones(2*n),cts,np.ones(n)]
S=lil_matrix((4*n,4*n),dtype=int)
for i in range(n):
 inds=np.arange(max(0,i-2),min(n,i+3));cols=np.concatenate([j*n+inds for j in range(4)])
 for j in range(4):S[j*n+i,cols]=1
S=csc_matrix(S);pattern=(S,group_columns(S));calls=0
def data(y):
 z=y*scales;th=z[:n];xx=z[n:2*n];ct=z[2*n:3*n];vr=z[3*n:];aa=np.array([rootmass*np.sin(th),rootmass*np.cos(th)],complex);mt=abs(aa[0])**2;mf=abs(aa[1])**2;u=ct/m.r**2;W,F,Wp,Fp=m.f(u);ff=m.f(.5*(u[1:]+u[:-1]))[1];fp=m.f(.5*(u[1:]+u[:-1]))[3];dx=np.diff(2*xx/np.pi);resp=m.vol*(Wp+m.beta*np.sin(2*xx)**2/np.pi**2*Fp);face=.25*m.ell2*m.w*fp*dx*dx;resp[:-1]+=face;resp[1:]+=face;Mt=ct[-1]+.5*mt[-1];tail=np.sum(m.tw*m.f(Mt*m.tt**2)[2]/m.tt**2);return th,xx,ct,vr,aa,mt,mf,F,ff,resp,tail
def fun(y):
 global calls
 calls+=1;th,xx,ct,vr,aa,mt,mf,F,ff,resp,tail=data(y);mu=np.array([vr-m.eps,2.5*m.K*(mf/m.vol)**(2/3)]);H=(m.kd+mu)*aa+m.J*m.alignment(aa,xx,c);H[:,:-1]+=m.ko*aa[:,1:];H[:,1:]+=m.ko*aa[:,:-1];rtheta=(H[0].real*np.cos(th)-H[1].real*np.sin(th))/rootmass
 coeff=(2/np.pi)**2*m.w*(m.ell2*ff+m.vac);parts=(mt,mf,F,coeff,np.real(np.conj(aa[1])*aa[0]));gx,hh,off,scale=m.carrier_force(xx,parts);rx=gx/scale;rct=np.r_[ct[0]-.5*mt[0],np.diff(ct)-.5*(mt[1:]+mt[:-1])]/cts;rr=resp/m.r**2;rvr=np.r_[vr[:-1]-vr[1:]-.5*(rr[:-1]+rr[1:]),vr[-1]-.5*rr[-1]-tail];return np.r_[rtheta,rx,rct,rvr]
u=m.enclosed(abs(a[0])**2);W,F,Wp,Fp=m.f(u);fp=m.f(.5*(u[1:]+u[:-1]))[3];dx=np.diff(2*x/np.pi);resp=m.vol*(Wp+m.beta*np.sin(2*x)**2/np.pi**2*Fp);face=.25*m.ell2*m.w*fp*dx*dx;resp[:-1]+=face;resp[1:]+=face;tail=np.sum(m.tw*m.f(np.sum(abs(a[0])**2)*m.tt**2)[2]/m.tt**2);vr=m.transpose(resp)+tail;y=np.r_[theta,x,ct,vr]/scales;E0=m.full_energy(a,x,np.zeros(n),c,v);history=[];start=time.monotonic();status='iteration_limit'
for it in range(70):
 r=fun(y);err=float(np.max(abs(r)));th,xx,ct,vr,aa,*_=data(y);E=m.full_energy(aa,xx,np.zeros(n),c,v);history.append({'iteration':it,'residual':err,'energy':E});print(history[-1],flush=True)
 if err<3e-10:status='converged';break
 J=approx_derivative(fun,y,method='3-point',abs_step=1e-7,sparsity=pattern,f0=r);delta=splu(csc_matrix(J)).solve(-r);merit=np.linalg.norm(r);rate=1.
 for ls in range(24):
  trial=y+rate*delta;rt=fun(trial);at=data(trial)[4]
  if np.all(np.isfinite(rt)) and np.max(m.enclosed(abs(at[0])**2))<.9997 and np.linalg.norm(rt)<merit:break
  rate*=.5
 if ls==23:status='line_search_failure';break
 y=trial
th,x,ct,vr,a,*_=data(y);mu=m.pot(a,x,True)[1];H=(m.kd+mu)*a+m.J*m.alignment(a,x,c);H[:,:-1]+=m.ko*a[:,1:];H[:,1:]+=m.ko*a[:,:-1];common=np.real(np.sum(np.conj(a)*H,axis=0))/mass;internal_error=float(np.max(abs(H-common*a)/rootmass));ad=-1j*H/m.sigma;Gd=2*m.J/m.sigma*np.imag(np.conj(ad[0])*m.alignment(a,x,c)[0]+np.conj(a[0])*m.alignment(ad,x,c)[0]);Sconv=(m.g+2*m.g2*abs(a[0])**2/m.vol)*Gd
np.savez_compressed(dest.with_name('state.npz'),a=a,alpha=x,carrier_p=np.zeros(n),chi=c,pi=v,support_potential=-common)
out={'status':status,'residual':float(np.max(abs(fun(y)))),'initial_meta':meta,'initial_unprepared_energy':E0,'prepared_energy':m.full_energy(a,x,np.zeros(n),c,v),'preparation_energy_change_not_radiation':m.full_energy(a,x,np.zeros(n),c,v)-E0,'mass_error':float(np.sum(abs(a)**2)-np.sum(mass)),'max_total_cell_mass_change':float(np.max(abs(np.sum(abs(a)**2,axis=0)-mass))),'internal_common_phase_residual':internal_error,'conversion_initial_source_derivative_norm':float(np.sqrt(np.sum(Sconv*Sconv/m.vol))),'diagnostics':m.diagnostics(a,x,c,v),'runtime_seconds':time.monotonic()-start,'history':history,'meaning':'Only initial internal composition and carrier equilibrated at the same total density. All subsequent density/phases/carrier/scalar/boundary cells must be released. support_potential is a diagnostic counterfactual only; never added to actual infall.'};dest.write_text(json.dumps(out,indent=2)+'\n');print({k:v for k,v in out.items() if k!='history'})
