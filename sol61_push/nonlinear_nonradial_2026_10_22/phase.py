import numpy as np,json,argparse
from pathlib import Path
from scipy.optimize import minimize
from field import Field
pa=argparse.ArgumentParser();pa.add_argument('--output');args=pa.parse_args();rows=[];checks=[];mstar=.08408132497418408
for n,box,b,R,lam in [(32,8,b,R,lam) for b in [1,4] for R in [.3,.6] for lam in [1,100]]+[(64,16,4,.6,100)]:
 f=Field(n,box);a=1/(2*lam);d=a/.2**2
 rho=np.exp(-sum((x/(R*s))**2 for x,s in zip(f.x,[1.2,.8,1]))/2);rho*=b*mstar/(f.vol*rho.sum())
 inv=lambda z:np.fft.ifftn(np.fft.fftn(z)/(a+d*f.k2)).real
 def fg(y):
  h=y.reshape(rho.shape);g=f.grad(h);s=np.sqrt(np.sum(g*g,axis=0));q=g/(1+s);z=inv(h*h);val=np.sum(.5*h*h+s-np.log1p(s)-rho*h+.125*h*h*z)
  return val,(h+.5*h*z-f.div(q)-rho).ravel()
 h0=np.fft.ifftn(np.fft.fftn(rho)/(1+f.k2)).real
 opt=minimize(fg,h0.ravel(),jac=True,method='L-BFGS-B',options={'ftol':1e-14,'gtol':1e-8,'maxiter':2000,'maxcor':10});h=opt.x.reshape(rho.shape);val,res=fg(opt.x);chi=1+.5*inv(h*h);g=f.grad(h);s=np.sqrt(np.sum(g*g,axis=0))
 r=dict(n=n,box=box,b=b,R=R,lam=lam,max_chi=float(chi.max()),max_w=float(np.max(s/(1+s))),relative_residual=float(np.linalg.norm(res)/np.linalg.norm(rho)),polarization_phase_energy=float(-f.vol*val),iterations=int(opt.nit),success=bool(opt.success));rows.append(r);print(r,flush=True)
 if n==32 and b==4 and R==.6 and lam==100:
  v=np.sin(np.arange(h.size));v/=np.linalg.norm(v);eps=1e-5;fd=(fg(opt.x+eps*v)[0]-fg(opt.x-eps*v)[0])/(2*eps);an=np.dot(res,v);checks.append(dict(name='nonlocal_quartic_gradient',passed=bool(abs(fd-an)<1e-7),value=float(abs(fd-an))))
 Path(args.output).write_text(json.dumps(dict(rows=rows,checks=checks),indent=2)+'\n')
