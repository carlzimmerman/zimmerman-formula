"""Fully relaxed boundary compliance and independent constrained energy curvature."""
import json,argparse
from pathlib import Path
import numpy as np,torch
from scipy.linalg import null_space
from scipy.optimize import minimize
from mixed_carrier import Mixed
from joint import T,RESERVOIR

def stiffness(r):
 n=r['n'];m=Mixed(n=n,domain=12,beta=r['beta'],K=r['K'],charge=0);m.ell2=(r['ell_kpc']/m.rm)**2
 v=np.r_[r['mass'],r['v'][n:]];x=v[n:];q=np.sin(np.pi*x/2)**2;rad=np.array(r['r']);i=np.where((q[:-1]-.5)*(q[1:]-.5)<0)[0][-1];dr=rad[i+1]-rad[i];R=rad[i]+dr*(.5-q[i])/(q[i+1]-q[i]);hp=np.pi/2*np.sin(np.pi*x)
 C=np.zeros(2*n);C[n+i]=dr*(.5-q[i+1])/(q[i+1]-q[i])**2*hp[i];C[n+i+1]=-dr*(.5-q[i])/(q[i+1]-q[i])**2*hp[i+1]
 a=T(v).requires_grad_(True);H=torch.autograd.functional.hessian(lambda aa:m.energy(torch.log(aa[:n]),aa[n:]),a).detach().numpy();E,g=m.direct(v)
 im=np.where(v[:n]>1e-7)[0];P0=null_space(np.ones((1,len(im))));P=np.zeros((2*n,len(im)-1));P[im,:]=P0
 results=[]
 for cut in [1e-4,1e-6,1e-8]:
  ix=np.where((x>cut)&(x<1-cut))[0]+n;X=np.eye(2*n)[:,ix];Z=np.c_[P,X];HH=Z.T@H@Z;cc=C@Z;ev=np.linalg.eigvalsh(HH);Hx=X.T@H@X;cx=C@X
  kk=float(1/(cc@np.linalg.solve(HH,cc)));kf=float(1/(cx@np.linalg.solve(Hx,cx)))
  results.append(dict(phase_cutoff=cut,tangent_H_min=float(ev[0]),density_H_min=float(np.linalg.eigvalsh(P.T@H@P)[0]),relaxed_stiffness_Eunit_per_kpc2=kk,fixed_density_stiffness_Eunit_per_kpc2=kf))
 finite=[]
 for shift in [-.2,.2]:
  target=R+shift;t=(target-rad[i])/dr;assert 0<t<1
  def wall(a):return (1-t)*np.sin(np.pi*a[n+i]/2)**2+t*np.sin(np.pi*a[n+i+1]/2)**2-.5
  def jac(a):
   gg=np.zeros(2*n);gg[n+i]=(1-t)*np.pi/2*np.sin(np.pi*a[n+i]);gg[n+i+1]=t*np.pi/2*np.sin(np.pi*a[n+i+1]);return gg
  cons=[dict(type='eq',fun=lambda a:sum(a[:n])-RESERVOIR,jac=lambda a:np.r_[np.ones(n),np.zeros(n)]),dict(type='ineq',fun=m.cap,jac=m.capjac),dict(type='eq',fun=wall,jac=jac)]
  op=minimize(m.direct,v,jac=True,method='SLSQP',bounds=[(1e-12,RESERVOIR)]*n+[(0,1)]*n,constraints=cons,options=dict(ftol=1e-14,maxiter=1000));EE,gg=m.direct(op.x);massgrad=np.r_[np.ones(n),np.zeros(n)];J=np.c_[massgrad,jac(op.x)];free=np.r_[op.x[:n]>1e-7,(op.x[n:]>1e-6)&(op.x[n:]<1-1e-6)];lam=np.linalg.lstsq(J[free],gg[free],rcond=None)[0];qq=np.sin(np.pi*op.x[n:]/2)**2;force=float(lam[1]*(qq[i+1]-qq[i])/dr)
  finite.append(dict(displacement_kpc=shift,energy_difference=EE-E,force_Eunit_per_kpc=force,wall_constraint=float(wall(op.x)),mass_constraint=float(sum(op.x[:n])-RESERVOIR),cap_slack=float(min(m.cap(op.x))),stationarity_residual=float(max(abs((gg-J@lam)[free]))),success=bool(op.success),iterations=int(op.nit)))
 return dict(n=n,R_kpc=R,curvature=results,finite=finite,central_energy_curvature_Eunit_per_kpc2=sum(row['energy_difference'] for row in finite)/.2**2,force_slope_stiffness_Eunit_per_kpc2=-(finite[1]['force_Eunit_per_kpc']-finite[0]['force_Eunit_per_kpc'])/.4,limitations='Spherical finite-grid static stability; no inertia, time evolution, nonspherical or global stability claim.')
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--input',required=True);ap.add_argument('--output',required=True);a=ap.parse_args();rows=json.loads(Path(a.input).read_text())['runs'];r=[r for r in rows if r['stage']=='base'][-1];out=stiffness(r);Path(a.output).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
