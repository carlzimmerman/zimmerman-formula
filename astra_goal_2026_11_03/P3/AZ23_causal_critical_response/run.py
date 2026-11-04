"""Exact finite symbolic audit, not a physical kappa certificate."""
import hashlib
import json
import platform
import subprocess
from pathlib import Path
import sympy as s

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
inputs = [HERE / 'CRITERIA.md', HERE / 'run.py', HERE / 'Certificate.lean', HERE / 'Mutate.lean',
          ROOT / 'why_4_puzzle/W4_08_positive_mond_amplitudes/formal/unified_invariant/SINGLE_FUNCTION.md',
          ROOT / 'why_4_puzzle/W4_08_positive_mond_amplitudes/formal/critical_endpoint/RESULT.md']
def hashes():
    return {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs}
before = hashes()
checks = {}
def zero(name, expr):
    checks[name] = bool(s.simplify(expr) == 0)

y, ys, H, B, Q = s.symbols('y ys H B Q', positive=True)
n, z, zd, r = s.symbols('n z zd r', real=True)
X = H**2*y**2
C = 6
D = C*H**2+2*X
K = 6*y**2/(3+y**2)
V = 12*H**2*y**4/(3+y**2)**2
dt = lambda f: -H*y*s.diff(f, y)
friction = s.simplify(3*H+dt(K)/K)
omega2 = s.simplify(V/K)
op = lambda f: s.simplify(dt(dt(f))+friction*dt(f)+omega2*f)
# Action density divided by a^3, after eliminating shift but before lapse.
L = B/2*(C*(zd-H*n)**2 + X*(2*z*z+4*n*z+2*n*n))-r*n
nsol = (C*H*zd-2*X*z+r/B)/D
zero('original_lapse_constraint', s.diff(L,n).subs(n,nsol))
reduced = s.expand(L.subs(n,nsol))
Jd = s.simplify(s.diff(s.diff(reduced,r),zd)*r)
J = s.simplify(s.diff(s.diff(reduced,r),z)*r)
rho = B*H**2*Q*y**3
forcing = s.simplify((J.subs(r,rho)-dt(Jd.subs(r,rho))-3*H*Jd.subs(r,rho))/(B*K))
zero('forcing_from_action', forcing-rho/(6*B)*(y*y+9)/(y*y+3))
zero('friction', friction-H*(1+2*y*y/(y*y+3)))
zero('frequency', omega2-2*H**2*y*y/(y*y+3))
u, v = y, y*y-3
zero('mode_one',op(u))
zero('mode_two',op(v))
W = s.simplify(u*dt(v)-dt(u)*v)
zero('wronskian',W+H*y*(y*y+3))
checks['wronskian_nonzero_positive_domain'] = bool((-W).is_positive)
green = (ys*(y*y-3)-(ys*ys-3)*y)/(-H*ys*(ys*ys+3))
zero('green_homogeneous',op(green))
zero('green_zero_initial_value',green.subs(y,ys))
zero('green_unit_derivative',dt(green).subs(y,ys)-1)
particular = Q*y**3/12
zero('conserved_source_particular',op(particular)-forcing)
np = nsol.subs({z:particular,zd:dt(particular),r:rho})
zero('particular_lapse',np+particular)
zero('mass_homogeneity',s.diff(particular,Q,2))
for root in [-H,-2*H]:
    zero('known_subhorizon_root_'+str(root),root**2+3*H*root+2*H**2)
mutated = dt(dt(u))+3*H*dt(u)+omega2*u
checks['mutate_frozen_X_rejected'] = bool(s.simplify(mutated) != 0)
for name, expected in [('Certificate',0),('Mutate',1)]:
    p = subprocess.run(['/opt/homebrew/bin/lean',str(HERE/(name+'.lean'))],capture_output=True,text=True)
    (HERE/(name+'.log')).write_text((p.stdout+p.stderr).replace(str(ROOT),'.'))
    checks['lean_'+name] = p.returncode == expected and (name!='Mutate' or 'false' in (p.stdout+p.stderr).lower())
after = hashes()
checks['inputs_unchanged'] = before == after
result = {
 'label':'κ = ½ FITTED; not theory closed',
 'assertion_tested':'Exact residual identities for inherited linear de Sitter scalar operator and conserved comoving probe; two finite Lean witnesses.',
 'verdicts':{f:{'exact_response':'PASS' if all(checks.values()) else 'FAIL',
                   'linear_causal_MOND_selection':'FAIL','nonlinear_mechanism':'NO VERDICT','physical_kappa':'NOT EVALUABLE',
                   'whole_requirement_rows_held':0,'whole_RQ3_rows_held':0} for f in ['canonical','alt']},
 'checks':checks,'checks_passed':sum(checks.values()),'checks_total':len(checks),
 'exact_expressions':{k:str(s.simplify(e)) for k,e in {'friction':friction,'omega_squared':omega2,'wronskian':W,'retarded_green_t_ge_s':green,'forcing':forcing,'particular_zeta':particular,'mutated_mode_residual':mutated}.items()},
 'inputs_before':before,'inputs_after':after,
 'versions':{'python':platform.python_version(),'sympy':s.__version__,'lean':subprocess.check_output(['/opt/homebrew/bin/lean','--version'],text=True).strip()},
 'command':'python3 astra_goal_2026_11_03/P3/AZ23_causal_critical_response/run.py',
 'run_status':'completed' if all(checks.values()) else 'failed',
 'limitations':['Conditional inherited quadratic action; zero sound-speed cutoff unresolved.','No nonlinear evolution, stationary galaxy, source-force fit or vacuum normalization derived.','Lean certifies finite rational checks only.']}
(HERE/'results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'checks_passed':result['checks_passed'],'checks_total':len(checks),'failed':[k for k,v in checks.items() if not v],'expressions':result['exact_expressions']},indent=2))
raise SystemExit(0 if all(checks.values()) else 1)
