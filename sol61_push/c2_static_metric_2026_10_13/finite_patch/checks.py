"""Finite prescribed-lapse C2 weak matching; no gravitational solution."""
from pathlib import Path
import json,math
import sympy as s
from scipy.integrate import quad

HERE=Path(__file__).resolve().parent
checks=[]
def z(name,value):
    residual=s.simplify(value);assert residual==0,(name,str(residual))
    checks.append({'name':name,'passed':True})
def yes(name,value):
    assert value,name
    checks.append({'name':name,'passed':True})
a,X0,rho0,h=s.symbols('a X0 rho0 h',positive=True)
r=s.symbols('r',positive=True)
Phi=-h*(1-r*r)**2;N=s.exp(Phi);omega=s.sqrt(2*X0)
d=X0*(1/N**2-1);Xi=X0+d
p=-rho0+a*d*d/2;rho=rho0+2*a*X0*d+3*a*d*d/2
psi2=2*X0*(1/N**2-1)
Xout=(omega*omega/N**2-psi2)/2
z('vacuum exterior phase invariant',Xout-X0)
z('vacuum exterior radial current',a*(Xout-X0))
z('charged core hydrostatic stress equation',s.diff(p,r)+(rho+p)*s.diff(N,r)/N)
z('lapse maximum derivative',s.diff(N,r).subs(r,1))
z('regular center lapse derivative',s.diff(N,r).subs(r,0))
z('phase invariant continuous at edge',d.subs(r,1))
z('phase invariant derivative continuous at edge',s.diff(d,r).subs(r,1))
z('pressure matches vacuum at edge',p.subs(r,1)+rho0)
z('pressure derivative continuous',s.diff(p,r).subs(r,1))
z('density matches vacuum at edge',rho.subs(r,1)-rho0)
z('density derivative continuous',s.diff(rho,r).subs(r,1))
slicecharge=a*d*omega/N
z('slice charge matches zero at edge',slicecharge.subs(r,1))
z('slice charge derivative continuous',s.diff(slicecharge,r).subs(r,1))
psiprime=s.sqrt(psi2)
z('radial phase gradient continuous at edge',s.limit(psiprime,r,1,dir='+'))
z('radial phase exterior slope',s.limit(psiprime/(r-1),r,1,dir='+')-4*s.sqrt(h*X0))
yes('phase is not generally C2 at edge',(4*s.sqrt(h*X0)).is_positive)
z('toy effective Newtonian source',s.diff(Phi,r,2)+2*s.diff(Phi,r)/r-(12*h-20*h*r*r))
yes('toy peak needs negative effective source',(12*h-20*h).is_negative)
yes('omitting exterior phase gradient leaves nonzero charged state',d.subs(r,2).is_positive)
z('wrong exterior phase-gradient sign mutation residual',(omega*omega/N**2+psi2)/2-X0-psi2)
yes('wrong sign does not leave vacuum',psi2.subs(r,2).is_positive)

# Fixed finite patch, prepared nonzero charge, no density or metric fit.
hh=.001;u=math.sqrt(2)
def lapse(x):return math.exp(-hh*(1-x*x)**2)
def delta(x):return 1/lapse(x)**2-1
Q=4*math.pi*quad(lambda x:x*x*delta(x)*u/lapse(x),0,1,epsabs=1e-12,epsrel=1e-12)[0]
E=4*math.pi*quad(lambda x:x*x*(2*delta(x)+1.5*delta(x)**2),0,1,epsabs=1e-12,epsrel=1e-12)[0]
Qlead=64*math.pi*math.sqrt(2)*hh/105;Elead=128*math.pi*hh/105
yes('finite prepared charge and buffer energy positive',Q>0 and E>0)
samples=[]
for x in [.5,1,1.5,2]:
    Nn=lapse(x);gradient=0 if x<=1 else math.sqrt(2*delta(x))
    X=(u*u/Nn**2-gradient*gradient)/2
    dd=X-1
    if x<1:assert dd>0
    else:assert abs(dd)<1e-12
    samples.append({'r':x,'d_over_X0':dd,'radial_phase_gradient':gradient,'radial_charge_current':-dd*gradient})
yes('sampled exterior current remains zero',max(abs(x['radial_charge_current']) for x in samples)<1e-12)
result={'checks':checks,'passed':len(checks),'failures':0,'prepared_core':{'Q':Q,'proper_excess_energy':E,
        'leading_small_h_Q':Qlead,'leading_small_h_energy':Elead,'Q_relative_difference':Q/Qlead-1,'energy_relative_difference':E/Elead-1},
        'samples':samples,'scope':'Distributional stationary P-only matter on prescribed finite peaked-lapse metric. Phase C1 not C2; no S_g, self-gravity, uniform health, formation, physical outer boundary or selector.'}
(HERE/'run/results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
