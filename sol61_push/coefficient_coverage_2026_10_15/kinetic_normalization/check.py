import sympy as s
import json
t=s.symbols("t", positive=True)
x=s.symbols("x", nonnegative=True)
u=s.symbols("u", positive=True)
mu=t/s.sqrt(1+t*t)
e=(t*s.sqrt(1+t*t)-s.asinh(t))/2
j=t*mu
f=s.diff(j,t)
checks={}
def check(name, value):
    z=s.simplify(value)
    assert z==0, (name,z)
    checks[name]="exact zero"
check("energy_derivative",s.diff(e,t)-j)
check("radial_stiffness",f-t*(t*t+2)/(1+t*t)**s.Rational(3,2))
check("radial_extremum",s.diff(f,t)-(2-t*t)/(1+t*t)**s.Rational(5,2))
check("maximum",f.subs(t,s.sqrt(2))-4*s.sqrt(6)/9)
check("sharp_polynomial_bound",32*(1+x)**3-27*x*(x+2)**2-(x-2)**2*(5*x+8))
check("deep_flux",s.limit(j/t**2,t,0)-1)
check("high_flux",s.limit(j/t,t,s.oo)-1)
check("vanishing_absolute_flux_deficit",s.limit(t-j,t,s.oo))
check("deficit_coefficient",s.limit(t*(t-j),t,s.oo)-s.Rational(1,2))
check("deep_energy",s.limit(e/t**3,t,0)-s.Rational(1,3))
check("high_speed_squared",s.limit(f/s.Rational(9,8),t,s.oo)-s.Rational(8,9))
y=(u*u+s.sqrt(u**4+4*u*u))/2
check("spherical_solution_squared",y*y-u*u*y-u*u)
check("spherical_high_correction",s.limit(u*(s.sqrt(y)-u),u,s.oo)-s.Rational(1,2))
check("spherical_deep_force",s.limit(s.sqrt(y/u),u,0)-1)
assert s.Rational(81,64)>s.Rational(32,27)
checks["strict_kinetic_headroom"]="exact rational inequality"
print(json.dumps({"checks":checks,"count":len(checks),"sympy":s.__version__,"scope":"symbolic identities and limits; scalar preferred-frame toy only"},indent=2))
