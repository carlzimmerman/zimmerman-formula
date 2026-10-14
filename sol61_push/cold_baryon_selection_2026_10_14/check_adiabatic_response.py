"""Does a supported tether automatically ignore added extra-source gravity?"""
import json
import math
import sys
from pathlib import Path
import sympy as s
from scipy.optimize import brentq

checks=[]
def check(name,condition):
    ok=bool(condition)
    checks.append(dict(name=name,passed=ok))
    if not ok:
        raise AssertionError(name)
def identity(name,expr):
    check(name,s.simplify(expr)==0)

# Full saturating force, G=a0=M_cond=1. Extra source h=A/r on a finite annulus.
# Label r0 sets the initial exact condensed-only tether mass and circular L.
# Conserved L and enclosed label mass give a pressure-supported cold-shell
# action-preserving response; this is not full coupled nonlinear Vlasov stability.
r,m,A,L2=s.symbols('r m A L2',positive=True)
u=m/r**2
R=u*u/(1-u)
acc=-1/r**2-A/r+R+L2/r**3
D=s.sqrt(1+4*r*r)
u0=2/(1+D)
M0=(D-1)/2
M0prime=2*r/D
sub={m:M0,L2:A*r*r}
identity('initial exact condensed-only law balances circular support',acc.subs(sub))
Fr=s.diff(acc,r).subs(sub)
Fr_expected=-2*A/r**2-2/(r**3*(1-u0))
identity('held-label held-L radial restoring derivative',Fr-Fr_expected)
drdA=-r*r*(1-u0)/(2*(1+A*r*(1-u0)))
identity('implicit adiabatic orbital-radius derivative',drdA+s.diff(acc,A).subs(sub)/Fr)
identity('wall margin positive factorization',1-u0-4*r*r/(1+D)**2)
dm_fixed_radius=-M0prime*drdA
check('response is positive by explicit factorization',
      s.ask(s.Q.positive((2*r/D)*r*r*(4*r*r/(1+D)**2)/
                         (2*(1+A*r*(4*r*r/(1+D)**2))))) is True)

def mass0(radius):
    # Stable equivalent form.
    return 2*radius*radius/(1+math.sqrt(1+4*radius*radius))
def force(radius,mass,amp,ell2):
    xx=mass/radius**2
    return -1/radius**2-amp/radius+xx*xx/(1-xx)+ell2/radius**3

rows=[]
for r0 in [1.,2.,5.,10.,50.]:
    for amp0 in [.1,1.]:
        mass=mass0(r0)
        ell2=amp0*r0*r0
        xx=mass/r0**2
        deriv=-r0*r0*(1-xx)/(2*(1+amp0*r0*(1-xx)))
        damp=amp0*1e-5
        wall=math.sqrt(mass)
        low=wall+(r0-wall)*1e-9
        root=brentq(lambda rad:force(rad,mass,amp0+damp,ell2),low,r0,
                    xtol=1e-13,rtol=1e-14)
        finite=(root-r0)/damp
        check('radius contracts for positive extra mass r=%g A=%g'%(r0,amp0),wall<root<r0)
        check('finite branch derivative matches exact adiabatic derivative r=%g A=%g'%(r0,amp0),
              math.isclose(finite,deriv,rel_tol=2e-5,abs_tol=1e-8))
        # Finite 10% source change demonstrates that holding the template fixed
        # is a different operation from preserving the circular actions.
        bigroot=brentq(lambda rad:force(rad,mass,1.1*amp0,ell2),low,r0,
                       xtol=1e-13,rtol=1e-14)
        ratio=mass/mass0(bigroot)
        check('contracted carrier exceeds baryon-only template at its new radius r=%g A=%g'%(r0,amp0),ratio>1)
        rows.append(dict(initial_radius=r0,initial_extra_source_A=amp0,
                         derivative_dr_dA=deriv,finite_derivative=finite,
                         radius_after_10percent_extra_source_growth=bigroot,
                         carrier_mass_over_condensed_only_template_at_new_radius=ratio))

out=dict(checks=checks,controls=rows,
         verdict='Exact positive first-order response: this supported carrier does not automatically omit extra-source gravity',
         conventions='Full saturating identified-carrier force; point condensed source; prescribed h=A/r on a finite annulus; fixed shell mass and angular momentum',
         structural_result='dr/dA<0 and delta Mt at fixed Eulerian radius>0 for r,A>0, under the stated slow circular branch',
         non_claims=['Not a universal no-go for pressure support, thermalization, source-sensitive interactions or other histories',
                    'No global finite-mass log-source halo; no large simulation',
                    'No formation mechanism or coupled nonspherical stability',
                    'Earlier positive equilibrium constructions remain valid as feasibility witnesses'])
Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(dict(checks=len(checks),all_passed=all(x['passed'] for x in checks),
                      largest_template_excess_for_10percent_extra_source_growth=max(r['carrier_mass_over_condensed_only_template_at_new_radius']-1 for r in rows)),indent=2))
