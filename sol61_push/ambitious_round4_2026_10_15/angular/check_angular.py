#!/usr/bin/env python3
"""Bounded exact implementation checks; universal argument lives in PROOF.md."""
import json
from fractions import Fraction as F
from pathlib import Path
import sympy as sp

out = Path('sol61_push/ambitious_round4_2026_10_15/angular/run_exact/results.json')
checks = []
def check(name, condition, detail=None):
    ok = bool(condition)
    checks.append({'name': name, 'passed': ok, 'detail': str(detail) if detail is not None else ''})
    if not ok:
        raise AssertionError(name)

l = sp.symbols('l', integer=True, nonnegative=True)
D, delta, zrho, h, dp, dm = sp.symbols('D delta zrho h dp dm', real=True)
phase = delta*h*(dp+dm)+delta*(zrho-2*D)*h*h
check('finite_density_phase_cancellation', sp.expand(phase.subs(dm,dp-zrho*h)- (2*delta*h*dp-2*D*delta*h*h)) == 0)
check('exterior_Maxwell_square', sp.expand(dp**2/(l+1)+2*delta*h*dp-(dp/sp.sqrt(l+1)+sp.sqrt(l+1)*delta*h)**2+(l+1)*delta**2*h**2) == 0)
wallpoly = 4*l*l+2*l-9+9/(2*l+1)
check('shell_load_factorization', sp.factor(wallpoly-8*l*(l+2)*(l-1)/(2*l+1))==0)
check('radial_wall_self_coefficient', wallpoly.subs(l,0)==0)
check('translation_wall_self_coefficient', wallpoly.subs(l,1)==0)
check('quadrupole_wall_self_coefficient', wallpoly.subs(l,2)==sp.Rational(64,5))

# Independent exact polar integrals of the singular divided-difference kernel.
v=sp.symbols('v', positive=True)
legendre = []
for j in range(0,17):
    integrand = sp.cancel((1-sp.legendre(j,1-v*v/2))/(v*v))
    val=sp.integrate(integrand,(v,0,2))
    check('Legendre_divided_difference_l_'+str(j), sp.simplify(val-j)==0)
    legendre.append({'l':j,'polar_integral_over_2pi':str(val)})

G=F(1,100000000); f=F(1341,250); P0=f*(1+2*f)/100
sigmalo=(F(49,50)*P0-F(1,1000000000))/2
sigmahi=F(51,100)*P0
sm=F(1,30000); Mmax=F(38); Dmax=F(1,1000); deltamax=F(1,999000)
A=F(1,50)-F(32,5)*G-G*sm
B=F(3,10)-G*sm*Mmax-16*G*sm*sm-F(252,5)*G-F(32,7)*G*sm-F(3,4)*deltamax*deltamax-Dmax*deltamax/2
check('actual_wall_root_lower_bound', sigmalo>F(3,10), sigmalo)
check('actual_wall_root_upper_bound', sigmahi<F(1,3), sigmahi)
check('density_coercivity_exact_bound', A>F(1,100), A)
check('shape_coercivity_exact_bound', B>F(1,4), B)
check('dipole_density_bound', F(1,50)-F(16,3)*G>F(1,100))
check('pressure_gradient_sign_margin',F(99,100)>f*F(1,1000)/(1-F(1,1000)))
check('beta0_branch_entire_witness',F(1,999) < F(1,2)*(F(50000,50001)/16))

rows=[]
for j in range(2,65):
    Lj=j*(j+1)
    check('angular_shape_ratio_l_'+str(j), F(j+1,Lj-2)<=F(3,4))
    check('wall_self_ratio_l_'+str(j), F(j,2*j+1)<F(1,2))
    check('wall_fluid_cross_ratio_l_'+str(j), F(j-1,2*j+1)<F(1,2))
    rows.append({'l':j,'density_lower_fraction':str(A),'shape_per_Lminus2_lower_fraction':str(B)})

result={'claim_id':'VC4-ANGULAR-001','passed':True,'checks_count':len(checks), 'checks':checks,
        'exact_bounds':{'P0':str(P0),'sigma_lower':str(sigmalo),'sigma_upper':str(sigmahi),'A_lower':str(A),'B_lower':str(B)},
        'Legendre_exact_range':legendre,'angular_ratio_range':rows,
        'non_claims':['Finite Legendre checks do not prove all l; analytic recurrence is needed.',
                      'No numerical equilibrium profile, eigenvalue spectrum, dynamic interface, hyperbolicity, or Einstein theory is computed.',
                      'The exact rational constants support only the estimates stated in the proof.']}
out.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'passed':True,'checks_count':len(checks),'A_lower_float':float(A),'B_lower_float':float(B),'output':str(out)}))
