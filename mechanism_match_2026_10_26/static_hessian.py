"""Final active constrained static Hessian and density-relaxed boundary stiffness."""
import argparse,json,sys
from pathlib import Path
import numpy as np,torch
from scipy.linalg import null_space
from matched import Matched
sys.path.insert(0,'nonlinear_transfer_2026_10_25')
from exact_equilibrium import Exact
from joint import T,RESERVOIR
torch.set_num_threads(1)

class Static(Exact):
 def __init__(self):
  super().__init__(J=30);self.obj=Matched(length_kpc=.0001);m=self.obj.m
  self.L2=(m.c/self.obj.M)**2;self.track=self.obj.M**2*self.obj.lam**2;self.weights=T(m.w)
  B=np.diag(np.r_[m.w[0],m.w[:-1]+m.w[1:],m.w[-1]])-np.diag(m.w,1)-np.diag(m.w,-1)
  self.chol=torch.linalg.cholesky(T(np.diag(m.vol)+self.L2*B))
 def energy(self,z,p):
  E=super().energy(z,p);mass=RESERVOIR*torch.softmax(z,dim=0)
  rho=mass*torch.sin(torch.pi*p[self.n:]/2)**2/self.vol
  t=torch.cholesky_solve((self.vol*rho)[:,None],self.chol)[:,0]
  return E+.5*self.track*(self.L2*torch.sum(self.weights*torch.diff(t)**2)+torch.sum(self.vol*(t-rho)**2))

ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args()
model=Static();m=model.obj.m;n=m.n;s=np.load('mechanism_match_2026_10_26/run_newton/state_0.0001.npz')
mass=np.sum(abs(s['a'])**2,axis=0);th=np.arctan2(abs(s['a'][0]),abs(s['a'][1]))*2/np.pi
v=np.r_[mass,s['alpha']*2/np.pi,th];y=np.r_[np.sqrt(mass),v[n:]]
def E(t):return model.energy(torch.log(t[:n]**2),t[n:])
_,phys=model.direct(v);lam=np.median(phys[:n][mass>1e-7]);im=np.where((mass>4e-12)|(phys[:n]<lam-1e-8))[0]
gx=phys[n:];ix=np.where(((y[n:]>1e-12)|(gx<0))&((y[n:]<1-1e-12)|(gx>0)))[0]+n
N=null_space(y[im][None,:]);Z0=np.zeros((3*n,N.shape[1]));Z0[im]=N;Z=np.c_[Z0,np.eye(3*n)[:,ix]]
ty=T(y).requires_grad_(True);H=torch.autograd.functional.hessian(E,ty).detach().numpy();HH=Z.T@H@Z
scale=1/np.sqrt(np.maximum(abs(np.diag(HH)),1e-8));HS=scale[:,None]*HH*scale[None,:]
eig=np.linalg.eigvalsh(HS);assert eig[0]>0
q=np.sin(np.pi*th/2)**2;cross=np.flatnonzero((q[:-1]-.5)*(q[1:]-.5)<0);assert len(cross)==1;i=cross[0]
dr=(m.r[i+1]-m.r[i])*m.rm;dq=q[i+1]-q[i];b=np.zeros(3*n)
b[2*n+i]=dr*(.5-q[i+1])/dq**2*np.pi/2*np.sin(np.pi*th[i])
b[2*n+i+1]=-dr*(.5-q[i])/dq**2*np.pi/2*np.sin(np.pi*th[i+1])
bp=Z.T@b;sol=scale*np.linalg.solve(HS,scale*bp);stiff=1/float(bp@sol);assert stiff>0
direction=Z@sol/(bp@sol)
def radius(yy):
 qq=np.sin(np.pi*yy[2*n:]/2)**2
 return (m.r[i]+(.5-qq[i])*(m.r[i+1]-m.r[i])/(qq[i+1]-qq[i]))*m.rm
fd=(radius(y+1e-5*direction)-radius(y-1e-5*direction))/(2e-5)
assert abs(fd-1)<1e-6
out={'mediator_range_pc':.1,'active_dimension':len(eig),'min_scaled_Hessian_eigenvalue':float(eig[0]),
     'max_scaled_Hessian_eigenvalue':float(eig[-1]),'Hessian_asymmetry_max':float(np.max(abs(H-H.T))),
     'relaxed_boundary_stiffness_Eunit_per_kpc_squared':stiff,'radius_derivative_control':fd,
     'scope':'Final active constrained real-density/composition/carrier static tangent on inherited grid, mediator relaxed. Not live moving-boundary or arbitrary 3D stability.'}
Path(args.output).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
