import numpy as np
from scipy.integrate import quad
from field import Field
class Isolated(Field):
 def evaluate(self,M,axes):
  r,acc,fg,h=self.solve(M,1,shape=axes)
  positive=np.exp(-sum((x/a)**2 for x,a in zip(self.x,axes))/2);positive*=M/(self.vol*positive.sum());rho=positive-positive.mean()
  rk=np.fft.fftn(rho);phi=np.fft.ifftn(-rk/self.safe).real;phi-=phi.mean()
  # Exact isolated Gaussian gravitational energy and shape derivatives.
  aa=np.array(axes)**2
  base=lambda t:1/np.sqrt(np.prod(t+aa))
  U=-M*M/(4*np.sqrt(np.pi))*quad(base,0,np.inf,epsabs=1e-9)[0]
  der=[]
  for i in range(3):
   z=(self.x[i]/axes[i])**2;dr=positive*(z-np.sum(positive*z)/np.sum(positive))
   grav=M*M/(4*np.sqrt(np.pi))*quad(lambda t:base(t)*aa[i]/(t+aa[i]),0,np.inf,epsabs=1e-9)[0]
   der.append(self.vol*np.sum(h*dr)+grav)
  # Restore constant h mode removed from the periodic source; exact at fixed chi.
  E=r['energy']-r['gravity']+U+2*np.pi*M*M/self.box**3
  r.update(energy=float(E),gravity=float(U),axis_log_derivatives=[float(x) for x in der],axes=list(axes))
  return r
