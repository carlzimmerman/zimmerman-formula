"""Positive two-gap spectrum: exact moment/kinetic checks and finite force samples."""
import argparse
import json
from pathlib import Path
import sympy as s

parser = argparse.ArgumentParser()
parser.add_argument('--output', required=True)
args = parser.parse_args()
P, eps, heavy, w, beta, H, S, M, theta = s.symbols(
    'P eps heavy w beta H S M theta', positive=True)
checks = {}
def check(name, expression):
    value = s.simplify(expression)
    checks[name] = value == 0
    if not checks[name]:
        raise AssertionError((name,value))

F = (1-w)*(P**2+eps**2)**s.Rational(3,2)+w*(P**2+heavy**2)**s.Rational(3,2)
mu1 = (1-w)*eps+w*heavy
mu3 = (1-w)*eps**3+w*heavy**3
check('vacuum_moment',F.subs(P,0)-mu3)
check('quadratic_moment',s.diff(F,P,2).subs(P,0)-3*mu1)
check('cubic_capacity',s.limit(F/P**3,P,s.oo)-1)
b = beta*s.diff(F,P)/(6*H)
check('flux',b-beta*P*((1-w)*s.sqrt(P**2+eps**2)+w*s.sqrt(P**2+heavy**2))/(2*H))
check('infrared_stiffness',s.limit(b/P,P,0)-beta*mu1/(2*H))
check('moment_ratio_identity',(beta*mu1/(2*H))**3-(3*S/8)*(3*beta**2/4)*(mu1**3/mu3)*(4*beta*mu3/(9*S*H**3)))
target_mu3 = 9*S*H**3/(4*beta)
w_match = (target_mu3-eps**3)/(heavy**3-eps**3)
check('exact_two_gap_vacuum_match',mu3.subs(w,w_match)-target_mu3)
check('small_heavy_weight_limit',s.limit(w_match,heavy,s.oo))
check('small_heavy_stiffness_limit',s.limit((w_match*heavy),heavy,s.oo))
check('infrared_stiffness_decoupling',s.limit(mu1.subs(w,w_match),heavy,s.oo)-eps)
check('light_force_limit',s.limit(b.subs(w,w_match),heavy,s.oo)-beta*P*s.sqrt(P**2+eps**2)/(2*H))

# The unsubtracted vacuum operator modifies the principal trace kinetic term.
vac = -beta*M**2*mu3/theta
quadratic = s.diff(vac,theta,2).subs(theta,3*H)/2
check('vacuum_trace_quadratic',quadratic+beta*M**2*mu3/(27*H**3))
dlambda = 2*beta*mu3/(27*H**3)
check('on_vacuum_kinetic_shift',dlambda.subs(w,w_match)-S/6)
B = s.symbols('B',positive=True)
S_B = 3*B+2
Beff = B+S_B/6
Seff = S_B* s.Rational(3,2)
v, shift = s.symbols('v shift',real=True)
k = s.symbols('k',positive=True)
kinetic = -3*Seff*v**2-2*Seff*v*k**2*shift-Beff*k**4*shift**2
check('effective_clock_kinetic',kinetic.subs(shift,-Seff*v/(Beff*k**2))-2*Seff*v**2/Beff)

# Free planar Dirac filled-sea primitive, with degeneracy d.
q, cutoff, mass, coupling, speed, d = s.symbols('q cutoff mass coupling speed d',positive=True)
Delta2 = mass**2+coupling**2*P**2
primitive = (speed**2*q**2+Delta2)**s.Rational(3,2)/(3*speed**2)
check('dirac_integral_primitive',s.diff(primitive,q)-q*s.sqrt(speed**2*q**2+Delta2))
E = -d*((speed**2*cutoff**2+Delta2)**s.Rational(3,2)-Delta2**s.Rational(3,2))/(6*s.pi*speed**2)
ren = E-E.subs(P,0)+d*coupling**2*cutoff*P**2/(4*s.pi*speed)
finite = d*(Delta2**s.Rational(3,2)-mass**3)/(6*s.pi*speed**2)
check('dirac_subtracted_finite_part',s.limit(ren,cutoff,s.oo)-finite)
capacity = d*coupling**3/(6*s.pi*speed**2)
gap = mass/coupling
check('heavy_vacuum_coupling_independence',capacity*gap**3-d*mass**3/(6*s.pi*speed**2))
check('heavy_quadratic_coupling_suppression',3*capacity*gap-d*coupling**2*mass/(2*s.pi*speed**2))

samples = []
for beta_value in (2,10,20):
    # Illustrative rational choices, not fitted to 32pi or observed data.
    substitutions = {H:s.Integer(1),S:s.Integer(5),beta:s.Integer(beta_value),
                     eps:s.Rational(1,10**8),heavy:s.Integer(10**4)}
    ww = s.simplify(w_match.subs(substitutions))
    assert 0 < ww < 1
    mm1 = s.simplify(mu1.subs(w,ww).subs(substitutions))
    mm3 = s.simplify(mu3.subs(w,ww).subs(substitutions))
    assert mm3 == s.Rational(45,4*beta_value)
    a0_light = s.Rational(2,beta_value)/(1-ww)
    point_results = []
    for pp in (s.Rational(1,1000),s.Rational(3,1000),s.Rational(1,100)):
        flux = b.subs(w,ww).subs(substitutions).subs(P,pp)
        error = float(s.N(flux/(pp**2/a0_light)-1))
        assert 0 <= error < 0.000057
        point_results.append({'P':float(pp),'relative_flux_correction':error,
                              'P_over_a0_light':float(pp/a0_light)})
    samples.append({'beta':beta_value,'H':1,'lambda':2,
                    'heavy_capacity_fraction':float(ww),'mu1':float(mm1),
                    'mu3':float(mm3),'infrared_stiffness':float(beta_value*mm1/2),
                    'bare_curvature_ratio':3*beta_value**2/4,
                    'finite_window_curvature_ratio':float(3/a0_light**2),
                    'force_points':point_results})
result = {'scope':'Positive finite gap ansatz; exact moments and local principal kinetic term; reduced-force samples only',
          'checks':checks,'passed':len(checks),'samples':samples,
          'non_claims':['No microscopic derivation of inverse-expansion area density or counterterm selection',
                        'No complete source or full causal/nonlinear stability proof',
                        'No exact infrared MOND or coefficient selection']}
Path(args.output).parent.mkdir(parents=True,exist_ok=True)
Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'passed':len(checks),'samples':len(samples)}))
