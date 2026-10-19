#!/usr/bin/env python3
"""Independent reconstruction from V(t), without importing archive code."""
import argparse
import hashlib
import json
from pathlib import Path
import sympy as sp

parser = argparse.ArgumentParser()
parser.add_argument('--output', required=True)
args = parser.parse_args()

# Work in u=log(t), a global real coordinate on t>0. This avoids branch choices.
u, A = sp.symbols('u A', real=True)
B = sp.symbols('B', real=True, nonzero=True)
p, M = sp.symbols('p M', positive=True)
Vu = M**4 * sp.exp(p*u)*(A+B*u)
stationary_factor = sp.simplify(sp.diff(Vu, u)/(M**4*sp.exp(p*u)))
ustar = sp.solve(stationary_factor, u)[0]
Vstar = sp.simplify(Vu.subs(u, ustar))
# d/dt = exp(-u) d/du
Vtt = sp.exp(-u)*sp.diff(sp.exp(-u)*sp.diff(Vu, u), u)
Vttstar = sp.simplify(Vtt.subs(u, ustar))
log_alpha_star = 2*ustar-2*sp.log(sp.pi)
Atarget = sp.solve(stationary_factor, A)[0]
uplift = sp.symbols('uplift', real=True)
checks = {
    'unique_stationary_u': sp.simplify(ustar+A/B+1/p) == 0,
    'positive_t_parameterization': sp.exp(ustar).is_positive is True,
    'second_derivative_formula': sp.simplify(Vttstar/(M**4*p*B*sp.exp((p-2)*ustar))) == 1,
    'vacuum_energy_formula': sp.simplify(Vstar/(-(B/p)*M**4*sp.exp(p*ustar))) == 1,
    'coupling_A_sensitivity': sp.simplify(sp.diff(log_alpha_star,A)+2/B) == 0,
    'arbitrary_target_A': sp.simplify(Atarget+B*u+B/p) == 0,
    'constant_uplift_stationarity_unchanged': sp.simplify(sp.diff(Vu+uplift,u)-sp.diff(Vu,u)) == 0,
}
report = Path('fine_structure_puzzle/archive_audit/REPORT.md')
result = {
    'claim_id': 'FSP-S-INDEPENDENT-LIFTING-001',
    'reviewed_report': str(report),
    'reviewed_report_sha256': hashlib.sha256(report.read_bytes()).hexdigest(),
    'conventions': 't=exp(u)>0; dimensionless t,A,B,p; M>0,p>0,B real nonzero; A real; derivative sensitivity holds B,p,M fixed',
    'derivation': {'V_in_u': str(Vu), 'stationarity_factor': str(stationary_factor),
                   'u_star': str(ustar), 'V_star': str(Vstar),
                   'Vtt_star': str(Vttstar), 'A_for_target_u': str(Atarget)},
    'checks': checks, 'passed': all(checks.values()),
    'non_claims': ['This hypothetical potential is not derived from Q3',
                   'No quantum stability of other fields established',
                   'Physical stability in t assumes positive scalar kinetic metric',
                   'No alpha(0) identification'],
}
out=Path(args.output)
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps({'passed': result['passed'], 'checks': checks,
                  'reviewed_report_sha256':result['reviewed_report_sha256']}))
raise SystemExit(0 if result['passed'] else 1)
