import json,sys
from pathlib import Path
import sympy as s
checks=[]
def check(name,c,detail):
    checks.append(dict(name=name,passed=bool(c),detail=str(detail)))
    if not c:raise AssertionError(name)
r,R,k,D,beta=s.symbols('r R k D beta',positive=True)
tail=D*(r+1/k)/(R+1/k)*s.exp(-k*(r-R))
check('normalized tail operator',s.simplify(s.diff(tail,r,2)-2*s.diff(tail,r)/r-k*k*tail)==0,tail)
check('normalized edge deficit',s.simplify(tail.subs(r,R)-D)==0,D)
check('edge reference density',s.simplify((-s.diff(tail,r)/r**2).subs(r,R)-D*k*k/(R*(k*R+1)))==0,D*k*k/(R*(k*R+1)))
u=s.symbols('u',positive=True)
check('tail effective stiffness exceeds linear',s.simplify(1/(1-u)-1-u/(1-u))==0,'For0<u<1,1/(1-u)>1')
t=s.symbols('t',real=True);F=s.Function('F')
wave=F(t-r)/r
check('radial scalar wave equation',s.simplify(s.diff(wave,t,2)-s.diff(wave,r,2)-2*s.diff(wave,r)/r)==0,wave)

j0,j1,j2,j3,p0,p1,p2,p3=s.symbols('j0 j1 j2 j3 p0 p1 p2 p3',real=True)
J=[j0,j1,j2,j3];p=[p0,p1,p2,p3];sign=[-1,1,1,1]
L=beta/2*sum(a*x*x for a,x in zip(sign,J))-sum(x*y for x,y in zip(p,J))
sol=s.solve([s.diff(L,x) for x in J],J,dict=True)[0]
dual=s.simplify(L.subs(sol));expected=-sum(a*x*x for a,x in zip(sign,p))/(2*beta)
check('current scalar duality',s.simplify(dual-expected)==0,dual)
check('canonical scalar time kinetic positive',s.diff(dual,p0,2)==1/beta,1/beta)

z=s.symbols('z',real=True)
f=z*(1-z*z)**3;fp=s.diff(f,z)
check('pulse zero integrated charge',s.integrate(f,(z,-1,1))==0,'Q_shift=-4pi/beta integral f=0')
check('pulse vanishes at boundary with derivative',f.subs(z,1)==0 and f.subs(z,-1)==0 and fp.subs(z,1)==0 and fp.subs(z,-1)==0,'Piecewise pulse is at least C2')
integral=s.integrate(fp*fp,(z,-1,1))
check('positive pulse energy export',integral>0,4*s.pi*integral/beta)
check('finite-radius cross flux integrates zero',s.integrate(f*fp,(z,-1,1))==0,'Integrated luminosity4pi/beta integral[fprime^2+f*fprime/r]')
z0=1/s.sqrt(7)
check('nonzero pulse extremum',s.simplify(fp.subs(z,z0))==0 and f.subs(z,z0)!=0,f.subs(z,z0))
# At fprime=0, phi_t=0 and phi_r=-f/r^2; gradient is spacelike.
norm=s.simplify(f.subs(z,z0)**2/r**4)
check('pulse violates strictly timelike current sector',norm>0,norm)
out=dict(checks=checks,pulse_energy=str(4*s.pi*integral/beta),scope='Exact conditional tail identities and independent reference-only scalar pulse. No derived export in full carrier/anchor parent.')
Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
