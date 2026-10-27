"""Fine-grid constrained stationary state; preparation only, never a time history."""
import argparse,json,time
from pathlib import Path
import numpy as np
from scipy.sparse import lil_matrix,csc_matrix
from scipy.sparse.linalg import splu
from scipy.optimize._numdiff import approx_derivative,group_columns
from retry_collocated import Collocated
from volume_initial import fine_initial
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args();dest=Path(args.output)
m=Collocated(eta=.01,material_h_kpc=.125,wave_R_kpc=10000.);a,x,c,v,meta=fine_initial(m,'formed','nonlinear_transfer_2026_10_25/run_exact_equilibrium/state.npz');n=m.n;M0=np.sum(abs(a)**2);ascale=np.maximum(np.sqrt(np.sum(abs(a)**2,axis=0)),1e-14)
ct=m.enclosed(abs(a[0])**2)*m.r**2;cg=m.enclosed(np.sum(abs(a)**2,axis=0))*m.r**2;cts=np.maximum(ct,1e-20*m.r**2);cgs=np.maximum(cg,1e-20*m.r**2)
scales=np.r_[ascale,ascale,np.ones(n),cts,cgs,np.ones(2*n),1.]
S=lil_matrix((7*n+1,7*n+1),dtype=int)
for i in range(n):
 inds=np.arange(max(0,i-1),min(n,i+2));cols=np.r_[np.concatenate([j*n+inds for j in range(7)]),7*n]
 for j in range(7):S[j*n+i,cols]=1
S[-1,[n-1,2*n-1,5*n-1]]=1
S=csc_matrix(S);pattern=(S,group_columns(S));calls=0
def calc(y,details=False):
 global calls
 calls+=1;z=y*scales;aa=np.array([z[:n],z[n:2*n]],complex);xx=z[2*n:3*n];ct=z[3*n:4*n];cg=z[4*n:5*n];vr=z[5*n:6*n];vg=z[6*n:7*n];lam=z[-1]
 mt=abs(aa[0])**2;mf=abs(aa[1])**2;u=ct/m.r**2;gd=cg/m.r**2;W,F,Wp,Fp=m.f(u);dx=np.diff(2*xx/np.pi);_,ff,_,fp=m.f(.5*(u[1:]+u[:-1]));resp=m.vol*(Wp+m.beta*np.sin(2*xx)**2/np.pi**2*Fp);face=.25*m.ell2*m.w*fp*dx**2;resp[:-1]+=face;resp[1:]+=face;gr=m.vol*(gd+m.gb);Mt=ct[-1]+.5*mt[-1];M=cg[-1]+.5*(mt[-1]+mf[-1]);tail=np.sum(m.tw*m.f(Mt*m.tt**2)[2]/m.tt**2)
 mu=np.array([vg+vr-m.eps,vg+2.5*m.K*(mf/m.vol)**(2/3)])
 Ha=(m.kd+mu-lam)*aa+m.J*m.alignment(aa,xx,c);Ha[:,:-1]+=m.ko*aa[:,1:];Ha[:,1:]+=m.ko*aa[:,:-1]
 coeff=(2/np.pi)**2*m.w*(m.ell2*ff+m.vac);parts=(mt,mf,F,coeff,np.real(np.conj(aa[1])*aa[0]));force,hh,off,scale=m.carrier_force(xx,parts)
 rct=np.r_[ct[0]-.5*mt[0],np.diff(ct)-.5*(mt[1:]+mt[:-1])]/cts
 mass=mt+mf;rcg=np.r_[cg[0]-.5*mass[0],np.diff(cg)-.5*(mass[1:]+mass[:-1])]/cgs
 rr=resp/m.r**2;gg=gr/m.r**2
 rvr=np.r_[vr[:-1]-vr[1:]-.5*(rr[:-1]+rr[1:]),vr[-1]-.5*rr[-1]-tail]
 rvg=np.r_[vg[:-1]-vg[1:]+.5*(gg[:-1]+gg[1:]),vg[-1]+.5*gg[-1]+M/m.R+1/np.sqrt(m.R**2+m.b**2)]
 residual=np.r_[Ha[0].real/ascale,Ha[1].real/ascale,force/scale,rct,rcg,rvr,rvg,(M-M0)/M0]
 if details:return aa,xx,residual,lam
 return residual
mt=abs(a[0])**2;mf=abs(a[1])**2;u=ct/m.r**2;W,F,Wp,Fp=m.f(u);dx=np.diff(2*x/np.pi);fp=m.f(.5*(u[1:]+u[:-1]))[3];resp=m.vol*(Wp+m.beta*np.sin(2*x)**2/np.pi**2*Fp);face=.25*m.ell2*m.w*fp*dx**2;resp[:-1]+=face;resp[1:]+=face;tail=np.sum(m.tw*m.f(np.sum(mt)*m.tt**2)[2]/m.tt**2);vr=m.transpose(resp)+tail;vg=-m.transpose(m.vol*(cg/m.r**2+m.gb))-M0/m.R-1/np.sqrt(m.R**2+m.b**2);mu=m.pot(a,x,True)[1];lam=float(np.sum(mu*abs(a)**2)/M0)
y=np.r_[a[0].real,a[1].real,x,ct,cg,vr,vg,lam]/scales;E0=m.full_energy(a,x,np.zeros(n),c,v);history=[];start=time.monotonic();status='iteration_limit'
for it in range(30):
 r=calc(y);err=float(np.max(abs(r)));aa,xx,_,ll=calc(y,True);E=m.full_energy(aa,xx,np.zeros(n),c,v);history.append({'iteration':it,'residual':err,'energy':E,'lambda':ll});print(history[-1],flush=True)
 if err<1e-9:status='converged';break
 J=approx_derivative(calc,y,method='3-point',abs_step=1e-6,sparsity=pattern,f0=r);delta=splu(csc_matrix(J)).solve(-r);merit=np.linalg.norm(r);rate=1.
 for ls in range(22):
  trial=y+rate*delta;at,xt,rt,lt=calc(trial,True)
  if np.all(np.isfinite(rt)) and np.max(m.enclosed(abs(at[0])**2))<.9997 and np.linalg.norm(rt)<merit:break
  rate*=.5
 if ls==21:status='line_search_failure';break
 y=trial
aa,xx,r,ll=calc(y,True);diag=m.diagnostics(aa,xx,c,v)
np.savez_compressed(dest.with_name('state.npz'),a=aa,alpha=xx,chi=c,pi=v)
dest.write_text(json.dumps({'status':status,'initial_meta':meta,'initial_energy':E0,'energy':m.full_energy(aa,xx,np.zeros(n),c,v),'residual':float(np.max(abs(r))),'lambda':ll,'mass_error':float(np.sum(abs(aa)**2)-M0),'diagnostics':diag,'runtime_seconds':time.monotonic()-start,'evaluations':calls,'colors':int(max(pattern[1])+1),'history':history,'interpretation':'Constrained static preparation only, not radiation or formation; stability is separate.'},indent=2)+'\n')
