"""Conditional Newtonian warm-tether feasibility; no formation or data fit."""
import json
import sys
from pathlib import Path
import sympy as s

r, q = s.symbols('r q', positive=True)
pi = s.pi
checks = []

def check(name, condition):
    passed = bool(condition)
    checks.append(dict(name=name, passed=passed))
    if not passed:
        raise AssertionError(name)

def identity(name, expression):
    check(name, s.simplify(expression) == 0)

# G=a0=M_cond=1. q is one-dimensional carrier velocity dispersion squared.
# These are candidate equilibria under the identified-carrier force dictionary,
# not the independent auxiliary-P zero-kinetic Euler equation.
D = s.sqrt(1 + 4*r*r)
Mt = (D - 1)/2
u = 2/(1 + D)
rho_t = 1/(2*pi*r*D)
R = u*u/(1-u)
gb = 1/r**2
gx = q*(1/r + 4*r/(1 + 4*r*r))
Mx = r*r*gx
rho_x = q*(1 + 20*r*r + 32*r**4)/(4*pi*r*r*(1 + 4*r*r)**2)
Phi_x = q*(s.log(r) + s.log(1+4*r*r)/2)
gtotal = gb + u + gx
afull = -gtotal + u + R

identity('tether mass flux', Mt-r*r*u)
identity('positive tether density from mass derivative', s.diff(Mt,r)-4*pi*r*r*rho_t)
identity('exact saturating law on condensed point mass', R-gb)
identity('all material sources included in total gravity', gtotal-(1+Mt+Mx)/r**2)
identity('full gravity and full tether leave extra-source attraction', afull+gx)
identity('extra-source density from Poisson', s.diff(Mx,r)-4*pi*r*r*rho_x)
identity('effective potential derivative', s.diff(Phi_x,r)-gx)
identity('isotropic Jeans equation', s.diff(q*rho_t,r)+rho_t*gx)
identity('Maxwell spatial factor supplies target density', s.exp(-Phi_x/q)-2*pi*rho_t)
identity('rationalized positive tether mass', Mt-2*r*r/(D+1))
check('tether mass positive for r>0', s.ask(s.Q.positive(2*r*r/(D+1))) is True)
check('tether density positive for r>0', s.ask(s.Q.positive(rho_t)) is True)
check('extra-source density positive for r,q>0', s.ask(s.Q.positive(rho_x)) is True)
identity('rationalized positive wall margin', 1-u-4*r*r/(D+1)**2)
check('positive saturation margin for r>0', s.ask(s.Q.positive(4*r*r/(D+1)**2)) is True)

# Direct stationary Vlasov test in Cartesian variables. H_eff=v^2/2+Phi_x.
# f=rho_t/(2*pi*q)^(3/2)*exp(-v^2/(2q)), normalized by the Gaussian integral.
v, ctheta = s.symbols('v ctheta', real=True)
identity('stationary Vlasov transport cancels along every velocity direction',
         v*ctheta*s.diff(s.log(rho_t),r)+(-gx*ctheta)*(-v/q))
z = s.symbols('z', real=True)
identity('Gaussian density normalization',
         s.integrate(s.exp(-z*z/(2*q)), (z,-s.oo,s.oo))**3/(2*pi*q)**s.Rational(3,2)-1)
identity('Gaussian pressure moment',
         s.integrate(z*z*s.exp(-z*z/(2*q)), (z,-s.oo,s.oo))/s.sqrt(2*pi*q)-q)

# A second stationary witness uses random-phase circular orbits on an annulus.
# Unlike the Maxwell local solution, these orbits do not cross annular edges.
vc2 = r*gx
L2 = r**3*gx
kappa2 = s.diff(gx,r) + 3*gx/r
kappa_expected = 2*q*(1+16*r*r+32*r**4)/(r*r*(1+4*r*r)**2)
identity('circular carrier force balance', vc2/r-gx)
identity('frozen-potential epicyclic frequency', kappa2-kappa_expected)
identity('angular momentum slope independent epicyclic check', s.diff(L2,r)/r**3-kappa2)
check('circular frozen-potential radial stability', s.ask(s.Q.positive(kappa_expected)) is True)
identity('zero extra source reduces pressure to zero', (q*rho_t).subs(q,0))

# Directly canceling only the extra-source pull has a different reciprocal cost.
# U_total=U_gravity+U_comp=-(1-alpha)G mt mx/d. At alpha=1 both cross forces vanish.
mt,mx,d,G = s.symbols('mt mx d G', positive=True)
alpha = s.symbols('alpha', real=True)
U = -(1-alpha)*G*mt*mx/d
Ft = -s.diff(U,d)
identity('pair-force cancellation is reciprocal at alpha=1', Ft.subs(alpha,1))
identity('same action leaves no extra-species pull from tether at alpha=1',
         (Ft/mx).subs(alpha,1))

rows=[]
for rv in [s.Rational(1,2),s.Integer(1),s.Integer(2),s.Integer(10),s.Integer(50)]:
    for qv in [s.Rational(1,100),s.Rational(1,10),s.Integer(1)]:
        sub={r:rv,q:qv}
        vals={key: float(expr.subs(sub)) for key,expr in
              dict(u=u,rho_t=rho_t,rho_x=rho_x,g_extra=gx,
                   pressure=q*rho_t,circular_v2=vc2,epicyclic_w2=kappa2).items()}
        check('positive admissible finite control r=%s q=%s'%(rv,qv),
              0 < vals['u'] < 1 and all(vals[k]>0 for k in vals if k!='u'))
        rows.append(dict(r=str(rv),sigma2=str(qv),**vals))

# Fixed ordinary source profiles, not inverse-designed from carrier pressure.
# Isotropic density inversion is verified by its Abel convolution coefficient.
# rho(psi)=4*pi*sqrt(2)*int_0^psi f(E)*sqrt(psi-E) dE.
# f(E)=1/(sqrt(8)*pi^2)*int_0^E rho''(psi)/sqrt(E-psi) dpsi,
# with rho(0)=rho'(0)=0. Fubini's inner beta integral reconstructs rho.
H,b = s.symbols('H b',positive=True)
B = s.symbols('B',nonnegative=True)
t = s.symbols('t',positive=True)
beta_integral=s.integrate(s.sqrt(1-t)/s.sqrt(t),(t,0,1))
identity('Abel density reconstruction beta integral', beta_integral-pi/2)
identity('Abel density reconstruction normalization',
         4*pi*s.sqrt(2)*beta_integral/(s.sqrt(8)*pi*pi)-1)
fixed_sources=[]
for name,psi,Mextra in [
    ('Hernquist',H/(r+b),H*r*r/(r+b)**2),
    ('Plummer',H/s.sqrt(r*r+b*b),H*r**3/(r*r+b*b)**s.Rational(3,2))]:
    h=-s.diff(psi,r)
    d1=s.diff(rho_t,r)/s.diff(psi,r)
    d2=s.factor(s.diff(d1,r)/s.diff(psi,r))
    identity(name+' positive source Poisson flux',h-Mextra/r**2)
    check(name+' source density positive',s.ask(s.Q.positive(s.factor(s.diff(Mextra,r)))) is True)
    identity(name+' carrier density vanishes at relative-potential zero',s.limit(rho_t,r,s.oo))
    identity(name+' carrier first derivative vanishes at relative-potential zero',s.limit(d1,r,s.oo))
    if name=='Hernquist':
        N=b+16*r**5+r*r*(48*b*(r-1/(48*b))**2+10*b-1/(48*b))
        expected=(b+r)**3*N/(pi*H*H*r**3*(1+4*r*r)**s.Rational(5,2))
        identity(name+' explicit positive second-derivative numerator',d2-expected)
        # b=B+1/2: 10b-1/(48b)=[480b^2-1]/48b >0.
        identity(name+' completed-square residual coefficient',
                 10*b-1/(48*b)-(480*b*b-1)/(48*b))
        check(name+' residual coefficient positive for b>=1/2',
              s.ask(s.Q.positive(s.expand(480*(B+s.Rational(1,2))**2-1))) is True)
    else:
        N=3*b*b+32*b*b*r*r+(128*b*b-4)*r**4+32*r**6
        expected=(b*b+r*r)**2*N/(2*pi*H*H*r**5*(1+4*r*r)**s.Rational(5,2))
        identity(name+' explicit positive second-derivative numerator',d2-expected)
        check(name+' residual coefficient positive for b>=1/2',
              s.ask(s.Q.positive(s.expand(128*(B+s.Rational(1,2))**2-4))) is True)
    for rv in [s.Rational(1,10),s.Integer(1),s.Integer(10)]:
        for bv in [s.Rational(1,2),s.Integer(1),s.Integer(2)]:
            val=d2.subs({r:rv,b:bv,H:s.Integer(1)})
            check(name+' finite positive isotropic inversion integrand r=%s b=%s'%(rv,bv),
                  s.ask(s.Q.positive(val)) is True)
            fixed_sources.append(dict(source=name,r=str(rv),scale_b=str(bv),
                                      density_second_derivative=float(val)))

out=dict(verdict='conditional exact local/annular warm-tether feasibility',
         checks=checks,controls=rows,fixed_source_controls=fixed_sources,
         assumptions=['identified-carrier Newtonian force dictionary',
                      'spherical point condensed source; G=a0=M_cond=1',
                      'zero stiffness; prescribed positive extra gravitating density',
                      'q>0 supplied in Maxwell construction, not dynamically selected',
                      'fixed Hernquist/Plummer source H>0,b>=1/2 in isotropic inversion'],
         non_claims=['no formation, cooling, source-phase selection or basin anchor',
                     'no global finite-mass solution or coupled stability',
                     'no independent auxiliary-P action or relativistic completion',
                     'no empirical fit or observational exclusion'])
Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(dict(checks=len(checks),all_passed=all(x['passed'] for x in checks),
                     verdict=out['verdict']),indent=2))
