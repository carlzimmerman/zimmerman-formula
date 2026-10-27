import json,math,sys
from pathlib import Path
import sympy as s
r,mr,mt,u,beta=s.symbols('r mr mt u beta',positive=True)
rho=mr/(4*s.pi*r*r);j=-mt/(4*s.pi*r*r)
checks=[]
def check(name,cond,detail=''):
 checks.append(dict(name=name,passed=bool(cond),detail=detail))
 if not cond:raise AssertionError(name)
check('radial kinetic energy density',s.simplify(4*s.pi*r*r*j*j/(2*rho)-mt*mt/(2*mr))==0)
R=u*u/(1-u);Rp=s.diff(R,u)
check('residual curvature',s.simplify(Rp-u*(2-u)/(1-u)**2)==0)
eta,k,omega=s.symbols('eta k omega',real=True)
mass=1/mr;stiff=Rp/r**2+beta*k*k/r**2
check('identified carrier frozen dispersion',s.simplify(stiff/mass-mr*(Rp+beta*k*k)/r**2)==0)
m0=(s.sqrt(1+4*r*r)-1)/2
mp=s.diff(m0,r);u0=m0/r**2
check('pointlaw density slope',s.simplify(mp-2*r/(2*m0+1))==0)
gap=s.simplify(mp*Rp.subs(u,u0)/r**2)
check('deep radial oscillator scaling',s.limit(gap*r**3,r,s.oo)==2)
cs2=beta*mp/r**2
check('deep wave speed scaling',s.limit(cs2*r*r/beta,r,s.oo)==1)
check('independent coefficient cannot equal all carrier inertia',s.diff(1/mp,r)!=0)
G=6.67430e-11;MS=1.98847e30;pc=3.0856775814913673e16
ls=5.754*pc;rows=[]
for footing,a0 in [('canonical',9.3603e-11),('alt',1.1312e-10)]:
 for mb in [1e9,1e10,1e11,1e12]:
  rm=math.sqrt(G*mb*MS/a0);vf=(G*mb*MS*a0)**.25
  bd=ls*ls/(2*rm*rm)
  for y in [.1,.01]:
   x=1/math.sqrt(y);mass0=(math.sqrt(1+4*x*x)-1)/2
   upr=mass0/(x*x);mprime=2*x/(2*mass0+1)
   curv=upr*(2-upr)/(1-upr)**2
   gap_si=vf/rm*math.sqrt(mprime*curv/(x*x))
   cs=vf*math.sqrt(bd*mprime/(x*x));orbit=2*vf/(rm*x)
   check('source above local carrier gap %s %g %g'%(footing,mb,y),orbit>gap_si)
   wavelength=2*math.pi*cs/math.sqrt(orbit*orbit-gap_si*gap_si)
   check('speed positive %s %g %g'%(footing,mb,y),cs>0)
   # Independent dimensional principal relation cs^2=gamma rho,
   # gamma=K Lstar^2/2 and rho=Mb mprime/(4pi rm^3 x^2).
   density=mb*MS*mprime/(4*math.pi*rm**3*x*x)
   gamma=(4*math.pi*G)*ls*ls/2
   check('physical density stiffness dictionary %s %g %g'%(footing,mb,y),
         abs(cs*cs-gamma*density)<1e-12*max(1.,cs*cs))
   rows.append(dict(footing=footing,baryon_mass_Msun=mb,y=y,r_kpc=rm*x/(1e3*pc),
    carrier_cs_m_s=cs,carrier_gap_s_inv=gap_si,source_frequency_s_inv=orbit,
    source_over_local_gap=orbit/gap_si,local_propagating_wavelength_pc=wavelength/pc))
out=dict(checks=checks,physical_controls=rows,scope='Interior positive-density locally frozen radial carrier dispersion; prescribed current/energy; not global emission, relaxation, nonlinear stability or covariant parent.')
Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(dict(checks=len(checks),speed_m_s_range=[min(z['carrier_cs_m_s'] for z in rows),max(z['carrier_cs_m_s'] for z in rows)],wavelength_pc_range=[min(z['local_propagating_wavelength_pc'] for z in rows),max(z['local_propagating_wavelength_pc'] for z in rows)]),indent=2))
