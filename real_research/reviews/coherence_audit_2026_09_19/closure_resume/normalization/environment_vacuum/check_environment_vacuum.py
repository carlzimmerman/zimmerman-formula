#!/usr/bin/env python3
"""Exact environmental vacuum area bound and constructive counterfamily.

No fits. Positive variables unless stated. c=1. The full physical claim and
inequality proofs are in REPORT.md; this script verifies their exact algebra.
"""
import argparse
import json
from pathlib import Path
import sympy as s

ap=argparse.ArgumentParser()
ap.add_argument('--output',required=True)
args=ap.parse_args()
checks=[]
def eq(name,x,y):
    r=s.simplify(x-y)
    checks.append({'name':name,'residual':str(r),'pass':r==0})
    assert r==0,(name,r)

a,A,g,g0,B,C,D,G,a0,N,h,I=s.symbols('a A g g0 B C D G a0 N h I',positive=True)
e=s.symbols('epsilon',positive=True)
q=s.Function('alpha')(g)
eq('longitudinal_health_is_monotone_sigma',s.diff(g*q,g),q+g*s.diff(q,g))
gend=A*g0/a
Itail=s.integrate(2*g*(A*g0/g-a),(g,g0,gend))
eq('profile_independent_tail_lower_bound',Itail,g0**2*(A-a)**2/a)
Ibound=s.factor(Itail+(A-a)*g0**2)
eq('monotone_profile_sharp_area_lower_bound',Ibound,g0**2*A*(A-a)/a)

# Continuous piecewise profile with strictly positive longitudinal slope.
ge=(A-e*a)*g0/((1-e)*a)
middle=e*a+(A-e*a)*g0/g
eq('strict_constructive_profile_left_join',middle.subs(g,g0),A)
eq('strict_constructive_profile_right_join',middle.subs(g,ge),a)
eq('strict_constructive_profile_health',middle+g*s.diff(middle,g),e*a)
Ie=s.factor((A-a)*g0**2+s.integrate(2*g*(middle-a),(g,g0,ge)))
eq('strict_profile_integral',Ie,g0**2*(A-a)*(A-e*a)/((1-e)*a))
eq('sharp_infimum_limit',s.limit(Ie,e,0,dir='+'),Ibound)

# Sign and exact bare versus measured G conventions from the action lapse.
Lvac=-N*h**3*I/(16*s.pi*G)
rhov=s.simplify(-s.diff(Lvac,N)/h**3)
Lambda=s.simplify(8*s.pi*G*rhov)
eq('positive_vacuum_lapse_energy',rhov,I/(16*s.pi*G))
eq('effective_Lambda',Lambda,I/2)
kb2=s.simplify(a0**2/(G*rhov))
GN=2*G/(2-a)
km2=s.simplify(a0**2/(GN*rhov))
eq('bare_G_kappa_squared',kb2,16*s.pi*a0**2/I)
eq('measured_G_kappa_squared',km2,8*s.pi*(2-a)*a0**2/I)
eq('measured_G_half_requires_area',km2.subs(I,32*s.pi*(2-a)*a0**2),s.Rational(1,4))

# Globally smooth, decreasing finite profile, C/B=D/a>1.
alpha=a+D/(s.sqrt(1+g**2/B**2)*(1+g**2/C**2))
alphaL=s.simplify(alpha+g*s.diff(alpha,g))
positive=D/((1+g**2/B**2)**s.Rational(3,2)*(1+g**2/C**2))
negative=2*D*g**2/(C**2*s.sqrt(1+g**2/B**2)*(1+g**2/C**2)**2)
eq('smooth_profile_longitudinal_decomposition',alphaL,a+positive-negative)
t=s.symbols('t',positive=True)
H=2*t/(1+t**2)**2
eq('negative_part_envelope_derivative',s.diff(H,t),2*(1-3*t**2)/(1+t**2)**3)
eq('negative_part_envelope_maximum',H.subs(t,1/s.sqrt(3)),3*s.sqrt(3)/8)
eq('smooth_profile_origin',alpha.subs(g,0),a+D)
eq('smooth_profile_high_limit',s.limit(alpha,g,s.oo),a)
eq('smooth_profile_excess_g_cubed_limit',s.limit(g**3*(alpha-a),g,s.oo),D*B*C**2)

r,u=s.symbols('r u',positive=True)
antiderivative=2*D*B**2*r**2/s.sqrt(r**2-1)*s.atan(u/s.sqrt(r**2-1))
eq('smooth_vacuum_integral_antiderivative',s.diff(antiderivative,u),2*D*B**2*r**2/(u**2+r**2-1))
Ismooth=2*D*B**2*r**2/s.sqrt(r**2-1)*s.atan(s.sqrt(r**2-1))
# For r>1, atan(q)+atan(1/q)=pi/2; endpoint form below verifies this by
# checking derivative plus value at q=1 instead of relying on branch guesses.
w=s.symbols('w',positive=True)
ident=s.atan(w)+s.atan(1/w)
eq('atan_complementary_derivative',s.diff(ident,w),0)
eq('atan_complementary_at_one',ident.subs(w,1),s.pi/2)
eq('smooth_area_large_scale_ratio',s.limit(Ismooth/(s.pi*D*B**2*r),r,s.oo),1)

# A compact undershoot shows why alpha>=a is essential to the area lower bound.
# w(t) is zero off [1,2]. w and w' vanish at endpoints.
bump=16*(t-1)**2*(2-t)**2
for endpoint in (1,2):
    eq('undershoot_bump_zero_'+str(endpoint),bump.subs(t,endpoint),0)
    eq('undershoot_bump_derivative_zero_'+str(endpoint),s.diff(bump,t).subs(t,endpoint),0)
eq('undershoot_bump_maximum',bump.subs(t,s.Rational(3,2)),1)
eq('undershoot_bump_derivative_factorization',s.diff(bump,t),32*(t-1)*(2-t)*(3-2*t))
J=s.integrate(2*t*bump,(t,1,2))
eq('undershoot_integrated_area',J,s.Rational(8,5))

av=s.Rational(1,10**7)
Av=s.Rational(1,2)
Dv=Av-av
rv=Dv/av
bound_kappa=s.sqrt((km2.subs(I,Ibound)).subs({a:av,A:Av,g0:a0}))
Is0=s.simplify(Ismooth.subs({a:av,D:Dv,r:rv,B:a0})/a0**2)
ks0=s.sqrt(8*s.pi*(2-av)/Is0)
bV_over_a0=(2-Av)/(2-av)
ks_bV=s.simplify(ks0/bV_over_a0)
B_for_half_over_a0=2*ks0
# Fixed eta=1/100 leaves a strict positive health margin: 1-3sqrt3/8-17eta>0.
eta=s.Rational(1,100)
health_margin=1-3*s.sqrt(3)/8-17*eta
assert health_margin>0
checks.append({'name':'undershoot_conservative_health_margin_positive','value':str(health_margin),'pass':True})
targetI=32*s.pi*(2-av)
Lratio=s.sqrt((Is0-targetI)/(s.Rational(8,5)*eta*av))

result={'status':'exact_algebra_passed','checks_passed':len(checks),'checks':checks,
 'results':{'tail_bound':str(Itail),'monotone_bound':str(Ibound),'strict_profile_area':str(Ie),
 'smooth_alpha':str(alpha),'smooth_area_in_r_C_over_B':str(Ismooth),
 'smooth_health_lower_bound_at_r_D_over_a':str(a*(1-3*s.sqrt(3)/8)),
 'bare_G_kappa_squared':str(kb2),'measured_G_kappa_squared':str(km2),
 'parameters':{'alpha_lo':str(av),'alpha_hi':str(Av),'smooth_C_over_B':str(rv)},
 'sharp_bound_kappa_for_g0_a0_and_A_half':str(s.N(bound_kappa,20)),
 'minimum_a0_over_g0_for_half':str(s.N(1/(2*bound_kappa),20)),
 'smooth_I_over_B2':str(s.N(Is0,20)),
 'smooth_kappa_if_B_a0':str(s.N(ks0,20)),
 'smooth_kappa_if_B_bV':str(s.N(ks_bV,20)),
 'B_over_a0_needed_for_half_smooth':str(s.N(B_for_half_over_a0,20)),
 'undershoot_eta':str(eta),'undershoot_health_margin_over_a':str(health_margin),
 'undershoot_area_change': '-(8/5) eta a L^2',
 'undershoot_L_over_a0_targeting_half_from_B_a0':str(s.N(Lratio,20)),
 'undershoot_relative_residual_area':str(s.N(targetI/Is0,20))},
 'non_claims':['No full-theory health proof; only alpha and alpha_L health.',
 'No physical principle fixing B/a0 or undershoot L.',
 'No empirical fit or observational model comparison.',
 'The lower bound assumes alpha>=alpha_lo, plus nonincreasing alpha for the sharpened form.']}
Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'checks_passed':len(checks),'results':result['results']},indent=2))
