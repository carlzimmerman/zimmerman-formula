"""Exact auxiliary action, normalization and independent controls.

Run via the recorded bounded runner. No original research source is executed
or modified. All expectations below are identities, limits, or exact examples;
none is an observation fit or numerical stability claim.
"""
from pathlib import Path
import ast
import json
import subprocess
import sys
import sympy as S

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
OUT = Path(sys.argv[1]).resolve()
assert OUT.is_relative_to(HERE)
checks = []

def zero(name, expr):
    residual = S.simplify(S.expand_log(expr, force=True))
    assert residual == 0, (name, residual)
    checks.append({'name': name, 'residual': str(residual)})

y, lam, q1, q2 = S.symbols('y lambda q1 q2', positive=True)
U = lambda q: q*q/2-2*q+S.log(q)+S.Rational(3,2)
W = y*y*(1-q1*q2)+(U(q1)+U(q2))/lam**2
q = 1/(1+lam*y)
stationary = {q1:q,q2:q}
reduced = y*y-2/lam**2*(S.log(1+lam*y)+1/(1+lam*y)-1)
mu = 1-(1+lam*y)**-2
p = lam*y/(1+lam*y)
zero('auxiliary_vacuum_value',U(S.Integer(1)))
zero('first_auxiliary_EL',lam**2*q1*S.diff(W,q1)-((1-q1)**2-lam**2*y*y*q1*q2))
zero('second_auxiliary_EL',lam**2*q2*S.diff(W,q2)-((1-q2)**2-lam**2*y*y*q1*q2))
zero('stationary_first_residual',S.diff(W,q1).subs(stationary))
zero('stationary_second_residual',S.diff(W,q2).subs(stationary))
zero('exact_reduced_action',W.subs(stationary)-reduced)
zero('partial_envelope_flux',S.diff(W,y).subs(stationary)/(2*y)-mu)
zero('total_reduced_flux',S.diff(reduced,y)/(2*y)-mu)
zero('two_channel_factorization',mu-(1-(1-p)**2))
zero('engagement_origin',p.subs(y,0))
zero('engagement_slope',S.diff(p,y).subs(y,0)-lam)
zero('response_slope',S.diff(mu,y).subs(y,0)-2*lam)
zero('newtonian_normalization',S.limit(mu,y,S.oo)-1)
zero('action_vacuum_value',reduced.subs(y,0))
zero('action_first_origin_derivative',S.diff(reduced,y).subs(y,0))
zero('action_second_origin_derivative',S.diff(reduced,y,2).subs(y,0))
zero('action_cubic_coefficient',S.limit(reduced/y**3,y,0)-4*lam/3)
zero('newtonian_action_coefficient',S.limit(reduced/y**2,y,S.oo)-1)
H=S.hessian(W,(q1,q2)).subs(stationary)
zero('symmetric_auxiliary_eigenvalue',H[0,0]+H[0,1]+2*y*(1+lam*y)/lam)
zero('antisymmetric_auxiliary_eigenvalue',H[0,0]-H[0,1]+2*y/lam)
zero('transverse_static_eigenvalue',mu-(lam*y)*(lam*y+2)/(1+lam*y)**2)
zero('longitudinal_static_eigenvalue',mu+y*S.diff(mu,y)-(lam*y)*((lam*y)**2+3*lam*y+4)/(1+lam*y)**3)

# Independent branch controls: positivity alone does not select q<=1.
other=1/(1-lam*y)
zero('excluded_equal_branch',S.diff(W,q1).subs({q1:other,q2:other}))
t=lam*y
plus=1+t/S.sqrt(1+t*t)
minus=1-t/S.sqrt(1+t*t)
zero('excluded_asymmetric_branch_1',S.diff(W,q1).subs({q1:plus,q2:minus}))
zero('excluded_asymmetric_branch_2',S.diff(W,q2).subs({q1:plus,q2:minus}))
assert plus.subs({lam:1,y:1})>1

# Explicit one-dimensional source variation, with g=Phi'>0 on the tested chart.
# Overall action is -(s² W/8piG + rho Phi); this verifies the flux normalization.
g,scale,G=S.symbols('g s G',positive=True)
E=scale**2*reduced.subs(y,g/scale)/(8*S.pi*G)
zero('source_action_flux_normalization',S.diff(E,g)-g*mu.subs(y,g/scale)/(4*S.pi*G))

# Holding s fixed still changes a0: actual parameter points, not a fit.
matching_a0=scale/(2*lam)
zero('deep_flux_matching',(2*lam/scale)*matching_a0-1)
zero('unit_weight_half',matching_a0.subs(lam,1)/scale-S.Rational(1,2))
zero('different_weight_quarter',matching_a0.subs(lam,2)/scale-S.Rational(1,4))

# Homogeneous perturbation control: the leading |eps|³ term has zero first
# and second derivatives at zero from BOTH signs; it is not a cubic polynomial.
eps=S.symbols('eps',real=True)
for sign in [-1,1]:
    signed=(4*lam/3)*sign*eps**3
    for order in [0,1,2]:
        zero('zero_background_jet_sign_%s_order_%s'%(sign,order),S.limit(S.diff(signed,eps,order),eps,0,dir='+' if sign==1 else '-'))

# Fixed-vacuum four-form comparison from ACTION_ROUTE, including response ratio.
D,b,beta,C,Z,a=S.symbols('D b beta C Z a',positive=True)
Zfamily=2*D-2*b*beta**2
zero('fixed_vacuum_coefficient',Zfamily/2+b*beta**2-D)
qflux=C/(2*D)
zero('flux_stationarity',2*D*qflux-C)
zero('vacuum_energy',D*qflux**2-C**2/(4*D))
zero('canonical_ratio', (Z/a**2)/(beta/a)**2-Z/beta**2)
zero('half_requires_ratio',(beta**2/(Z/2+b*beta**2)).subs(Z,(8-2*b)*beta**2)-S.Rational(1,4))

# Independent particle-free spectral realization: no species or mass parameter.
nu=S.symbols('nu',positive=True)
density=lam*S.exp(-lam*nu)
zero('spectral_density_normalization',S.integrate(density,(nu,0,S.oo))-1)
zero('spectral_response_integral',S.integrate(density*S.exp(-nu/y),(nu,0,S.oo))-p)
zero('spectral_infrared_weight',density.subs(nu,0)-lam)

# PD08's operation is inspected as syntax, never run for its success flags.
pd08=ROOT/'deepseek_push/PD08_particle_free_derivation.py'
tree=ast.parse(pd08.read_text())
p_assignments=[ast.unparse(n.value) for n in ast.walk(tree) if isinstance(n,ast.Assign)
               and any(isinstance(t,ast.Name) and t.id=='p' for t in n.targets)]
assert 'Y + c2 * Y ** 2' in p_assignments
c2=S.symbols('c2',real=True)
zero('correct_PD08_second_order_coefficient',S.expand(1-(1-(y+c2*y*y))**2).coeff(y,2)-(2*c2-1))

run=subprocess.run(['lake','env','lean',str(HERE/'UnitResponse.lean')],
                   cwd=ROOT/'fable_independent_2026/lean_2026',capture_output=True,text=True)
(OUT/'lean.txt').write_text(run.stdout+run.stderr)
assert run.returncode==0,run.stdout+run.stderr
assert 'sorryAx' not in run.stdout and 'warning:' not in run.stdout
assert run.stdout.count('depends on axioms:')==14
result={'exact_checks':checks,'exact_check_count':len(checks),
        'lean_theorems':14,'lean_exit_code':run.returncode,
        'pd08_p_assignments':p_assignments,
        'requested_unconditional_unit_normalization':'NOT ESTABLISHED',
        'verified_result':'Explicit equal-weight particle-free auxiliary action implies unit response and kappa=1/2; the variable-weight action implies kappa=1/(2 lambda).',
        'non_claims':['No independent selection of equal weights','No covariant dynamics or observation fit','No dark particle premise or particle nonexistence theorem','No global novelty claim']}
(OUT/'result.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='exact_checks'},indent=2))
