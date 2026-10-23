import sys,json
from pathlib import Path
import numpy as np
from scipy.special import roots_legendre
from scipy.optimize import brentq
p=Path(__file__).parent;order=int(sys.argv[2])
source=(p/'basis16_orbits.py').read_text().split('cdf=cumulative')[0]
ns={'__file__':str(p/'basis16_orbits.py'),'__name__':'basis_only'};exec(source,ns)
r=ns['r'];rho=ns['rho'];sol=ns['sol'];phi=ns['phi'];R=ns['R'];S=ns['Ssym'];moment=ns['moment'];fun=ns['ns']['fun'];A=ns['ns']['A'];r0=ns['r0']
def psi(x):return sol.sol(x)[1]
def dp(x):return fun(x,sol.sol(x))[1]
def lc(x):return -x**3*dp(x)
def qc(x):return psi(x)+(x+x**3)*dp(x)/2
rcmax=brentq(qc,r0,R);umax=lc(rcmax);gx,gw=roots_legendre(order);us=(gx+1)*umax/2;uw=gw*umax/2
coeff=[];frequencies=[];derweights=[];qs=[];errs=[]
for u,wu in zip(us,uw):
 rc=brentq(lambda x:lc(x)-u,r0,rcmax);emin=-psi(rc)+u/(2*rc*rc);emax=-u/2
 for e,we in zip(emin+(gx+1)*(emax-emin)/2,gw*(emax-emin)/2):
  def v2(x):return 2*(e+psi(x))-u/x**2
  rp=brentq(v2,r0,rc,xtol=1e-13);ra=brentq(v2,rc,R,xtol=1e-13)
  cc=[];periods=[]
  for count in [1024,2048]:
   theta=(np.arange(count)+.5)*np.pi/(2*count);xx=rp+(ra-rp)*np.sin(theta)**2;weights=(ra-rp)*np.sin(2*theta)/np.sqrt(v2(xx));phase=np.pi*(np.cumsum(weights)-weights/2)/weights.sum()
   potentials=np.array([np.interp(xx,r,f) for f in phi]);cos=np.cos(np.arange(1,33)[:,None]*phase);cc.append((cos*weights)@potentials.T/weights.sum());periods.append(2*weights.sum()*np.pi/(2*count))
  T=periods[-1];F=15*A/(2**4.5*np.pi);derweights.append(F*np.pi*T*wu*we);qs.append(-e-u/2);frequencies.append(2*np.pi/T);coeff.append(cc[-1]);errs.append(float(np.max(abs(cc[-1]-cc[0]))))
C=np.array(coeff);o=np.array(frequencies);dw=np.array(derweights);Q=np.array(qs);freq=o[:,None]*np.arange(1,33);weights=2*dw[:,None]*freq**2;measured=np.einsum('nh,nhi,nhj->ij',weights,C,C)
mass=float(dw@Q);matrixerr=float(np.linalg.norm(measured-moment)/np.linalg.norm(moment));checks=dict(mass=abs(mass-1)<1e-3,sum_rule=matrixerr<.01,fourier=max(errs)<1e-4,positive_weights=bool(min(dw)>0 and min(Q)>0))
np.savez_compressed(sys.argv[1]+'.npz',S=S,moment=moment,measured_moment=measured,coeff=C,omega=o,derivative_weights=dw,Q=Q)
out=dict(checks=checks,all_pass=all(checks.values()),order=order,orbits=len(Q),mass=mass,matrix_sum_rule_error=matrixerr,max_fourier_error=max(errs),max_L2=float(umax),max_circular_radius=float(rcmax),scope='Gauss quadrature in angular momentum squared and energy; finite Fourier truncation and broadening remain')
Path(sys.argv[1]+'.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2));sys.exit(0 if out['all_pass'] else 1)
