import numpy as np
from scipy.optimize import minimize
class Field:
 def __init__(self,n=32,box=8):
  self.n=n;self.box=box;self.dx=box/n;self.vol=self.dx**3/(4*np.pi)
  a=(np.arange(n)-n/2)*self.dx;self.x=np.meshgrid(a,a,a,indexing='ij')
  kk=4*np.sin(np.pi*np.fft.fftfreq(n))**2/self.dx**2
  self.k2=kk[:,None,None]+kk[None,:,None]+kk[None,None,:];self.safe=self.k2.copy();self.safe[0,0,0]=1
 def grad(self,h):return np.array([(np.roll(h,-1,axis=i)-h)/self.dx for i in range(3)])
 def div(self,P):return sum((P[i]-np.roll(P[i],1,axis=i))/self.dx for i in range(3))
 def solve(self,M,R,shape=(1.2,.8,1),quadratic=False):
  rho=np.exp(-sum((x/(R*s))**2 for x,s in zip(self.x,shape))/2);rho*=M/(self.vol*rho.sum());rho-=rho.mean()
  rk=np.fft.fftn(rho);phi=np.fft.ifftn(-rk/self.safe).real;phi-=phi.mean()
  h0=np.fft.ifftn(rk/(1+self.k2)).real
  def fg(y):
   h=y.reshape(rho.shape);g=self.grad(h);s=np.sqrt(np.sum(g*g,axis=0))
   Q=g if quadratic else g/(1+s)
   W=.5*s*s if quadratic else s-np.log1p(s)
   val=np.sum(.5*h*h+W-rho*h)
   derivative=h-self.div(Q)-rho
   return val,derivative.ravel()
  if quadratic:h=h0;success=True;nit=0
  else:
   opt=minimize(fg,h0.ravel(),jac=True,method='L-BFGS-B',options={'ftol':1e-14,'gtol':1e-8,'maxiter':1500,'maxcor':10});h=opt.x.reshape(rho.shape);success=bool(opt.success);nit=opt.nit
  val,res=fg(h.ravel());g=self.grad(h);s=np.sqrt(np.sum(g*g,axis=0));w=s/(1+s)
  accel=-self.grad(phi+h);U=.5*self.vol*np.sum(rho*phi);E=U-self.vol*val
  # Coordinate derivative of Gaussian source at fixed mass; periodic tail renormalization included.
  derivs=[]
  positive=rho+M/(self.box**3/(4*np.pi))
  for i in range(3):
   z=(self.x[i]/(R*shape[i]))**2;dr=positive*(z-np.sum(positive*z)/np.sum(positive))
   derivs.append(float(self.vol*np.sum((phi+h)*dr)))
  return dict(mass=M,R=R,shape=shape,n=self.n,box=self.box,quadratic=quadratic,success=success,iterations=int(nit),relative_residual=float(np.linalg.norm(res)/np.linalg.norm(rho)),max_w=float(w.max()),energy=float(E),gravity=float(U),axis_log_derivatives=derivs,force_norm=float(np.linalg.norm(accel))),accel,fg,h
