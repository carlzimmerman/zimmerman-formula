"""Exact compact stiffness-supported halo and polynomial source certificate."""
import json,sys,math
from pathlib import Path
import sympy as s
r=s.symbols('r',nonnegative=True)
checks=[]
def exact(name,expr):
    z=s.factor(expr)
    assert z==0,(name,z)
    checks.append(name)
rho0=s.Rational(105,776)/s.pi
rho=rho0*(1-r*r/10-s.Rational(9,10)*r**4)
k=s.Rational(101,50958); gamma=k/rho0
m=r*(350-21*r*r-135*r**4)/1940*r*r
u=m/(r*r)
gb=u*u/(1-u)+k*(r/5+s.Rational(18,5)*r**3)
mb=r*r*gb
exact('Gauss and cold mass',s.diff(m,r)-4*s.pi*r*r*rho)
exact('regular density form',rho-rho0*(1-r*r)*(1+s.Rational(9,10)*r*r))
exact('gradient chemical force',gamma*s.diff(rho,r)-(u*u/(1-u)-gb))
exact('total cold mass',m.subs(r,1)-s.Rational(1,10))
exact('total baryon mass',mb.subs(r,1)-s.Rational(25,1341))
exact('assigned inventory ratio',m.subs(r,1)/mb.subs(r,1)-s.Rational(1341,250))
exact('source regular center',s.limit(mb/r**3,r,0)-k/5)
exact('zero density boundary',rho.subs(r,1))
exact('positive pressure-gradient load',s.diff(rho,r)+rho0*(r/5+s.Rational(18,5)*r**3))
exact('pole avoidance bound decomposition',s.Rational(35,194)*r-u-r**3*(21+135*r*r)/1940)
# Positive Bernstein coefficients certify the polynomial at every real r in [0,1].
q=s.cancel(s.diff(mb,r)*(1-u)**2/r**2)
assert s.denom(q)==1 or s.denom(q).is_Integer
poly=s.Poly(q,r)
def bernstein_coefficients(expr,a,b):
    z=s.symbols('z')
    pp=s.Poly(s.expand(expr.subs(r,a+(b-a)*z)),z)
    degree=pp.degree()
    aa=[pp.nth(i) for i in range(degree+1)]
    return [s.factor(sum(aa[j]*s.Rational(math.comb(i,j),math.comb(degree,j)) for j in range(i+1))) for i in range(degree+1)]
cert=[]
def certify(a,b,depth=0):
    coeff=bernstein_coefficients(q,a,b)
    if all(v>0 for v in coeff):
        cert.append({'left':str(a),'right':str(b),'coefficients':[str(v) for v in coeff],'minimum':str(min(coeff))})
        return
    assert depth<12,(a,b,min(coeff))
    mid=(a+b)/2
    certify(a,mid,depth+1);certify(mid,b,depth+1)
certify(s.Integer(0),s.Integer(1))
# Vacuum particle potential inequality: r² Fout is strictly decreasing from a negative value.
M=s.Rational(1,10); Mb=s.Rational(25,1341)
Fout=(M/r**2)**2/(1-M/r**2)-Mb/r**2
exact('outside chemical force',r*r*Fout-(M*M/(r*r-M)-Mb))
exact('outside decreasing force envelope',s.diff(r*r*Fout,r)+2*M*M*r/(r*r-M)**2)
assert Fout.subs(r,1)<0
# Hodge radial integration identity, including its boundary derivative.
mm=s.Function('m')(r)
raw=r*r*(s.diff(mm/r**2,r)**2+2*(mm/r**2)**2/r**2)
exact('radial Hodge integration identity',raw-s.diff(mm,r)**2/r**2+2*s.diff(mm*mm/r**3,r))
x=s.symbols('x',positive=True)
W=(-x-x*x/2-s.log(1-x))/(4*s.pi)
exact('frozen W derivative',4*s.pi*s.diff(W,x)-x*x/(1-x))
exact('positive radial Hessian formula',4*s.pi*s.diff(W,x,2)-x*(2-x)/(1-x)**2)
exact('positive transverse Hessian formula',4*s.pi*s.diff(W,x)/x-x/(1-x))
result={'claim_id':'VC3-SH-001','exact_identity_count':len(checks),'identities':checks,
'positive_source_polynomial':str(q),'bernstein_partition':cert,
'constants':{'rho0':str(rho0),'gamma':str(gamma),'Lstar_squared_over_R_squared':str(gamma/(2*s.pi)),'Mc':str(M),'Mb':str(Mb),'inventory_ratio':'1341/250','outside_force_at_edge':str(Fout.subs(r,1))},
'scope':'Exact fixed-baryon NR electrostatic/stiffness candidate with chosen source/scale; no relativistic vacuum or formation theorem.'}
Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n')
print(f'PASS: {len(checks)} exact identities; {len(cert)} Bernstein intervals certify positive baryon source on [0,1].')
