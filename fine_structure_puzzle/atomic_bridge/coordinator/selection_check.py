#!/usr/bin/env python3
"""FSP-I exact selector checks plus measured-input scale diagnostics."""
import argparse
import json
from pathlib import Path
import sympy as s
import mpmath as mp

p = argparse.ArgumentParser()
p.add_argument('--output', required=True)
p.add_argument('--upper-state-control', action='store_true')
args = p.parse_args()
inputs = json.loads(Path('fine_structure_puzzle/atomic_bridge/coordinator/selection_inputs.json').read_text())
checks = []


def check(label, condition):
    checks.append({'label': label, 'passed': bool(condition)})


a, me, mn, hbar, c, radius = s.symbols('alpha me mp hbar c r', positive=True)
mu = me*mn/(me+mn)
length = hbar/(mu*c*a)
binding = mu*c*c*a*a/2
trial = hbar*hbar/(2*mu*radius**2)-a*hbar*c/radius
check('hydrogen variational radius stationary for EVERY alpha', s.simplify(s.diff(trial,radius).subs(radius,length)) == 0)
check('hydrogen radius has positive curvature', s.simplify(s.diff(trial,radius,2).subs(radius,length)-mu**3*c**4*a**4/hbar**2) == 0)
check('optimized hydrogen binding energy', s.simplify(trial.subs(radius,length)+binding) == 0)
check('size-energy relation extracts alpha', s.simplify(2*binding*length/(hbar*c)-a) == 0)
check('electron radius elasticity', s.simplify(me*s.diff(s.log(length),me)+mn/(me+mn)) == 0)
check('nucleon radius elasticity', s.simplify(mn*s.diff(s.log(length),mn)+me/(me+mn)) == 0)
C, D = s.symbols('C D', positive=True)
matter = C*a-D*a*a
check('linear self-energy stationary point is a maximum', s.diff(matter,a,2) == -2*D and s.simplify(s.diff(matter,a).subs(a,C/(2*D))) == 0)
atomic_mass = me+mn-binding/c**2
elasticity = s.simplify(a*s.diff(s.log(atomic_mass),a)/4)
check('BTFR response from atomic binding mass', s.simplify(elasticity+mu*a*a/(4*atomic_mass)) == 0)

# An exact noncommuting two-state Hamiltonian: H0=[[0,1],[1,2]], V=diag(-1,2).
# The Coulomb ground-energy concavity theorem is analytic; this is a finite
# implementation/sign check, not a surrogate proof of the infinite atom.
H = s.Matrix([[-a, 1], [1, 2+2*a]])
disc = s.sqrt((2+3*a)**2+4)
lower, upper = (2+a-disc)/2, (2+a+disc)/2
check('two-state eigenvalue from exact characteristic polynomial', s.simplify((H-lower*s.eye(2)).det()) == 0)
curvature = s.diff(upper if args.upper_state_control else lower,a,2)
expected = -18/((2+3*a)**2+4)**s.Rational(3,2)
check('ground branch has concave curvature', s.simplify(curvature-expected) == 0)

mp.mp.dps=60
em=mp.mpf(inputs['m_e_kg']); pm=mp.mpf(inputs['m_p_kg'])
cv=mp.mpf(inputs['c_m_s']); hv=mp.mpf(inputs['h_J_s'])/(2*mp.pi)
av=1/mp.mpf(inputs['alpha_inverse']); muv=em*pm/(em+pm)
G=mp.mpf(inputs['G_SI']); ev=mp.mpf(inputs['elementary_charge_C'])
aH=hv/(muv*cv*av); BH=muv*cv**2*av**2/2
mass=em+pm-BH/cv**2
diag={
    'a_H_m':mp.nstr(aH,25),'binding_eV_leading':mp.nstr(BH/ev,25),
    'radius_proton_elasticity':mp.nstr(-em/(em+pm),25),
    'radius_electron_elasticity':mp.nstr(-pm/(em+pm),25),
    'electronic_binding_fraction_of_H_rest_mass':mp.nstr(BH/(mass*cv**2),25),
    'velocity_alpha_elasticity_electronic_binding_only':mp.nstr(-muv*av**2/(4*mass),25),
    'atomic_electromagnetic_acceleration_diagnostic':mp.nstr(muv*cv**3*av**3/hv,25),
    'footings':[]}
for value in inputs['framework_acceleration_footings_m_s2']:
    am=mp.mpf(value)
    rM=mp.sqrt(G*pm/am)
    diag['footings'].append({'a_M_m_s2':value,'proton_gravity_transition_radius_m':mp.nstr(rM,25),
        'a_H_over_transition_radius':mp.nstr(aH/rM,25),
        'alpha_from_UNJUSTIFIED_radius_equality':mp.nstr(hv/(muv*cv*rM),25),
        'role':'Scale diagnostic only; equality of radii is not a physical law and is not proposed as an alpha derivation.'})
check('sensitivity scales physically ordered', abs(em/(em+pm)) < mp.mpf('.001') and abs(muv*av**2/(4*mass)) < mp.mpf('1e-8'))
result={'claim_id':'FSP-I','parent':'FSP-001','check_count':len(checks),'checks':checks,'passed':all(q['passed'] for q in checks),
        'upper_state_control':args.upper_state_control,'diagnostics':diag,
        'nonclaims':['No alpha derivation','Numerical diagnostics use measured alpha and masses','No microscopic source matching or full QED completion established','No new empirical bounds']}
Path(args.output).parent.mkdir(parents=True,exist_ok=True)
Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'passed':result['passed'],'check_count':len(checks),'failed':[x['label'] for x in checks if not x['passed']],'diagnostics':diag},indent=2))
raise SystemExit(0 if result['passed'] else 1)
