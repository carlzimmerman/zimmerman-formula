"""Homogeneous scalar-GB + canonical inflaton + phenomenological reheating fluid.
Reduced Planck mass=1; all dimensional quantities use a supplied initial H unit.
No external H(t), effective-vacuum replacement, or observational fit.
"""
import numpy as np
from scipy.integrate import solve_ivp
MI=np.sqrt(6)/15
GAMMA=.05*MI

def coupling(phi,eta,scale=None):
 if scale is None:return eta*phi,eta
 y=(phi/scale)**2;e=np.exp(-y)
 return eta*phi*e,eta*e*(1-2*y)

def detail(y,lam=1.,eta=.1,scale=None,damping=0.):
 p,v,c,w,r,h,n=y;fp,fpp=coupling(p,eta,scale);up=.01*p+lam*p**3
 A=24*fp*h*h;B=24*h**3*fp-v;C=6*h+72*h*h*fp*v
 b=-(3*h+damping)*v-up+24*fp*h**4
 d=up*v-3*h*w*w-4*h*r+damping*v*v-24*h**3*fpp*v*v
 determinant=C+B*A
 hd=(d-B*b)/determinant;acc=b+A*hd
 QT=1+8*h*fp*v;FT=1+8*(fpp*v*v+fp*acc)
 return acc,hd,QT,FT,determinant

def rhs(t,y,lam=1.,eta=.1,scale=None,damping=0.):
 p,v,c,w,r,h,n=y;acc,hd,qt,ft,det=detail(y,lam,eta,scale,damping)
 return [v,acc,w,-(3*h+GAMMA)*w-MI*MI*c,-4*h*r+GAMMA*w*w+damping*v*v,hd,h]

def initial(phi=1e-6,inflaton=15.,lam=1.):
 rho=.005*phi**2+lam*phi**4/4+.5*MI**2*inflaton**2
 return np.array([phi,0.,inflaton,0.,0.,np.sqrt(rho/3),0.])

def evolve(lam=1.,eta=.1,scale=None,phi=1e-6,inflaton=15.,end=5000.,rtol=1e-9,atol=1e-12,damping=0.):
 def fun(t,y):return rhs(t,y,lam,eta,scale,damping)
 def kinetic(t,y):return detail(y,lam,eta,scale,damping)[2]
 def gradient(t,y):return detail(y,lam,eta,scale,damping)[3]
 def amplitude(t,y):return 100-abs(y[0])
 def hubble(t,y):return 10-y[5]
 events=[kinetic,gradient,amplitude,hubble]
 for e in events:e.terminal=True;e.direction=-1
 y0=initial(phi,inflaton,lam)
 # A negative coefficient at the starting point is already an invalid trajectory.
 if min(detail(y0,lam,eta,scale,damping)[2:4])<=0:return None,{'termination':'initial tensor screen fails'}
 sol=solve_ivp(fun,[0,end],y0,method='DOP853',rtol=rtol,atol=atol,max_step=4,events=events,dense_output=True)
 labels=['tensor kinetic zero','tensor gradient zero','field amplitude guard100','Hubble guard10']
 termination='end time' if sol.t[-1]==end else next((labels[i] for i,t in enumerate(sol.t_events) if len(t)),'integrator failure')
 # Resample independently of the internal step endpoints for diagnostics.
 ts=np.unique(np.concatenate([sol.t,np.linspace(0,sol.t[-1],4001)]));ys=sol.sol(ts)
 vals=np.array([detail(y,lam,eta,scale,damping) for y in ys.T]);p,v,c,w,r,h,N=ys
 fp=np.array([coupling(a,eta,scale)[0] for a in p]);rp=.5*v*v+.005*p*p+lam*p**4/4
 ri=.5*w*w+.5*MI**2*c*c;rgb=-24*h**3*fp*v
 residual=(3*h*h-rp-ri-r-rgb)/(3*h*h)
 row={'lam':lam,'eta':eta,'damping':damping,'scale':scale,'initial_phi':phi,'initial_inflaton':inflaton,'end_time':float(sol.t[-1]),'termination':termination,'success':sol.success,'nfev':sol.nfev,'N':float(N[-1]),'max_abs_phi':float(max(abs(p))),'min_QT':float(min(vals[:,2])),'min_FT':float(min(vals[:,3])),'max_Friedmann_relative_residual':float(max(abs(residual))),'end_phi_canonical_fraction':float(rp[-1]/(3*h[-1]**2)),'end_GB_fraction':float(rgb[-1]/(3*h[-1]**2)),'end_radiation_fraction':float(r[-1]/(3*h[-1]**2)),'end_H':float(h[-1]),'end_phi':float(p[-1]),'end_velocity':float(v[-1])}
 return sol,row
