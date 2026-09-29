# POST-HOC repair of control C3a (disclosed): the frozen C3a returned 'inf' (numerical fault of the control, not a physics result). Same formula, looser quad tolerance.
import numpy as np, warnings
from scipy.special import i0,i1,k0,k1,ellipk
from scipy.integrate import quad
warnings.filterwarnings("ignore")
def phi(r):
    f=lambda a: -2*np.pi*a*(1/(2*np.pi))*np.exp(-a)*(2/(np.pi*(a+r)))*ellipk(4*a*r/(a+r)**2)
    return quad(f,0,r,limit=800,epsabs=1e-13,epsrel=1e-10)[0]+quad(f,r,60,limit=800,epsabs=1e-13,epsrel=1e-10)[0]
for x in (0.5,1,2.15,5,10):
    h=1e-3*x; g=(phi(x+h)-phi(x-h))/(2*h)
    # Richardson with h/2
    h2=h/2; g2=(phi(x+h2)-phi(x-h2))/(2*h2); gr=(4*g2-g)/3
    y=x/2; cf=2*y**2*(i0(y)*k0(y)-i1(y)*k1(y))/x
    print(x, g, gr, cf, abs(gr/cf-1))
