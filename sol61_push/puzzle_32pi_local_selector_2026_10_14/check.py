"""Exact controls and assigned benchmarks; not a full field-equation solver."""
import json, math
import sympy as s
x, a, m, r, b, p, F, V, z, e, g = s.symbols('x a m r b p F V z e g', positive=True)
checks = []
def check(name, expression):
    assert s.simplify(expression) == 0, (name, expression)
    checks.append(name)
d = 2*a/(m*r)*(1+m/r+4*m*m/(3*r*r))
check('linear Schwarzschild equation', s.diff(r*r*(1-2*m/r)*s.diff(d,r),r)+48*a*m*m/r**4)
check('linear horizon value', d.subs(r,2*m)-11*a/(6*m*m))
check('charge interval integral', s.integrate(48/x**4,(x,3,4))-s.Rational(37,108))
check('tail integral', s.integrate(48/x**4,(x,x,s.oo))-16/x**3)
check('radial kernel primitive', s.diff(s.log(1-2/x)/2,x)-1/(x*(x-2)))
U=V*s.exp(p*p/F**2)
check('local force balance', p*s.diff(U,p)-2*p*p*U/F**2)
check('rate upper-bound gap', 12/e-12*(1-z)/(e+6*z)-12*z*(e+6)/(e*(e+6*z)))
c=299792458.; G=6.67430e-11; solar=1.98847e30; pc=3.085677581491367e16
mass=G*4e6*solar/c**2; phi=9.360324825e-11/c**2
H=math.sqrt(32*math.pi/3)*phi; gamma=3/(128*math.pi)
inner=1e4*pc; outer=1e5*pc; X=inner/mass; XR=outer/mass
J=(math.log1p(-2/XR)-math.log1p(-2/X))/2
I=37/108; k=math.log(3)/2
def lower(beta):
    eps=mass*phi/math.sqrt(beta)
    qmin=2*I/(math.sqrt(eps*eps+4*k*I)+eps)
    return max(0.,qmin-16/(eps*X**3))*J/eps
lo,hi=1e-20,1e-10
for _ in range(160):
    mid=math.sqrt(lo*hi)
    if lower(mid)>.1: hi=mid
    else: lo=mid
beta_limit=math.sqrt(lo*hi)
out={'exact_checks':checks,'count':len(checks),
     'scope':'Conditional static massless test-field bound; assigned isolated black-hole benchmark, not observational exclusion',
     'gamma':gamma,'fast_necessary_beta':gamma/12,
     'massless_fraction_lower_bound_at_fast_threshold':lower(gamma/12),
     'beta_at_ten_percent_bound':beta_limit,
     'rate_upper_at_ten_percent_bound':12*beta_limit/gamma,
     'H_times_outer_radius':H*outer,
     'local_equilibrium_radius_kpc':(2*mass*mass/H**4)**(1/6)/(1e3*pc),
     'small_z_local_equilibrium_phi_ratio_at_inner':math.sqrt(1+2*mass*mass/(H**4*inner**6))}
assert 5e4 < out['massless_fraction_lower_bound_at_fast_threshold'] < 6e4
assert 3e-12 < out['rate_upper_at_ten_percent_bound'] < 4e-12
print(json.dumps(out,indent=2))
