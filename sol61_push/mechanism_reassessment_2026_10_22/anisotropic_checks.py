import sympy as s
from scipy.integrate import quad
import numpy as np,json,sys
r,a,C,v,K,a0,rM=s.symbols('r a C v K a0 rM',positive=True)
u=a0*2/(1+s.sqrt(1+4*(r/rM)**2))
rho=s.diff(r*r*u,r)/(K*r*r)
expected=a0*rM/(K*r*s.sqrt(r*r+rM*rM/4))
checks={'native_density':s.simplify(rho-expected)==0,'native_law':s.simplify(u*u/(a0-u)-a0*rM*rM/(r*r))==0}
S=s.sqrt(r*r+a*a);rh=C/(r*S)
sr=v*v*S/(S+a);st=v*v*a/(S+a)
if "--mutate" in sys.argv: st=s.Integer(0)
checks['jeans_balance']=s.simplify(s.diff(rh*sr,r)+rh*(2*sr-st)/r)==0
checks['speed_sum']=s.simplify(sr+st-v*v)==0
checks['anisotropy']=s.simplify(1-st/(2*sr)-(1-a/(2*S)))==0
rows=[]
for rr in [.01,.1,1,10,100]:
 aa=.5;vv=1.;cc=1.
 # b=r sin(theta); integrate without the integrable endpoint singularity.
 pref=cc*aa/(2*np.pi**2*vv**2)
 moment=lambda weight:4*np.pi*vv**2/rr*quad(lambda th:pref/(rr*rr*np.sin(th)**2+aa*aa)*weight(th),0,np.pi/2,epsabs=1e-12,epsrel=1e-12)[0]
 dens=moment(lambda t:1.);pr=moment(lambda t:vv*vv*np.cos(t)**2);pt=moment(lambda t:vv*vv*np.sin(t)**2)
 SS=np.sqrt(rr*rr+aa*aa);ex=cc/(rr*SS)
 errors=[abs(dens/ex-1),abs(pr/(ex*SS/(SS+aa))-1),abs(pt/(ex*aa/(SS+aa))-1)]
 rows.append(dict(radius=rr,density=dens,sigma_r2=pr/dens,sigma_t_total2=pt/dens,max_relative_error=max(errors)))
checks['quadrature']=all(x['max_relative_error']<1e-9 for x in rows)
checks['positive_moments']=all(x['density']>0 and x['sigma_r2']>0 and x['sigma_t_total2']>0 for x in rows)
mass=4*s.pi*C*(s.sqrt(r*r+a*a)-a)
checks['virial_boundary']=s.simplify(4*s.pi*r**3*rh*sr-v*v*mass)==0
checks['mass_integral']=s.simplify(s.diff(mass,r)-4*s.pi*r*r*rh)==0
checks['infinite_mass']=s.limit(mass/r,r,s.oo)==4*s.pi*C
checks={k:bool(x) for k,x in checks.items()}
out=dict(checks=checks,all_pass=all(checks.values()),rows=rows,scope='constructed collisionless equilibrium in force-free algebraic identity branch; infinite isolated profile, no formation or finite stiffness')
with open(sys.argv[1],'w') as f:json.dump(out,f,indent=2)
print(json.dumps(out,indent=2));sys.exit(0 if out['all_pass'] else 1)
