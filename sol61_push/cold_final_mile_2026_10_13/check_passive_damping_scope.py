"""CE-FM-055: corrected isothermal operator and passive-damping scope."""
import json,sys
from pathlib import Path
import sympy as s
checks=[]
def exact(name,expr):
    assert s.simplify(expr)==0,(name,expr)
    checks.append(name)
r,A,C,v,w2=s.symbols('r A C v w2',positive=True)
x=s.Function('xi')(r);rho=A/r**2
dr=-s.diff(r*r*rho*x,r)/r**2
dg=-C*x/r**2
acc=(-s.diff(v*dr,r)-dr*C/r-rho*dg)/rho
expected=v*s.diff(x,r,2)+(C-2*v)*s.diff(x,r)/r+C*x/r**2
exact('continuity reduction',dr+rho*s.diff(x,r))
exact('complete perturbed Euler acceleration',acc-expected)
exact('closure operator',expected.subs(C,2*v)-v*(s.diff(x,r,2)+2*x/r**2))
nu=s.sqrt(7)/2
for f in [s.sqrt(r)*s.sin(nu*s.log(r)),s.sqrt(r)*s.cos(nu*s.log(r))]:
    exact('zero-frequency logarithmic branch',s.diff(f,r,2)+2*f/r**2)
gam,Om=s.symbols('gamma Omega',positive=True)
root=(s.sqrt(gam**2+4*Om**2)-gam)/2
stable=2*Om**2/(s.sqrt(gam**2+4*Om**2)+gam)
exact('positive root rationalization',root-stable)
exact('damped unstable characteristic',root**2+gam*root-Om**2)
exact('large friction growth product',s.limit(gam*stable,gam,s.oo)-Om**2)
q,z=s.symbols('q qdot',real=True)
exact('saddle-energy dissipation',z*(Om**2*q-gam*z)-Om**2*q*z+gam*z**2)
L,k,t=s.symbols('L k t',positive=True)
# Log-sine trial y=sqrt(r)sin(pi log(r/a)/L), DD endpoints.
# Transform numerator to log radius; cross term integrates to zero.
kL=s.pi/L
trial=(s.sin(kL*t)/2+kL*s.cos(kL*t))**2-2*s.sin(kL*t)**2
num=s.integrate(s.expand_trig(trial),(t,0,L))
exact('DD Rayleigh numerator',num-(s.pi**2/(2*L)-7*L/8))
Lc=2*s.pi/s.sqrt(7)
exact('critical log width',num.subs(L,Lc))
M=s.diag(1,2);K=s.diag(-1,3);D=s.Matrix([[2,1],[1,2]])
lam=s.symbols('lambda',real=True)
poly=(lam**2*M+lam*D+K).det()
assert poly.subs(lam,0)<0 and poly.subs(lam,1)>0
assert M.is_positive_definite and D.is_positive_definite
assert K*D!=D*K
checks.append('noncommuting positive damping retains positive growth root')
examples=[]
for gg in [s.Integer(0),s.Rational(1,10),s.Integer(1),s.Integer(10),s.Integer(1000000)]:
    val=stable.subs({gam:gg,Om:1})
    assert val>0;checks.append('positive growth at gamma='+str(gg))
    examples.append({'gamma_over_Omega':str(gg),'growth_over_Omega':str(s.N(val,20))})
res={'claim_id':'CE-FM-055','checks_passed':len(checks),'checks':checks,'DD_critical_width':str(s.N(s.exp(Lc),16)),'noncommuting_pencil_polynomial':str(poly),'damped_growth_controls':examples,'scope':'Isothermal surrogate reconstruction; unchanged negative stiffness with linear passive damping. Not a full tether-fluid/Einstein stability theorem.'}
Path(sys.argv[1]).write_text(json.dumps(res,indent=2)+'\n')
print(json.dumps(res,indent=2))
