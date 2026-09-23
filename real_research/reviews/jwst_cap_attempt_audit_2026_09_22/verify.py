"""Bounded audit of Qwen code, not a physical-discovery certificate."""
import ast
import json
from pathlib import Path
import numpy as np
import sympy as sp

ROOT = Path(__file__).resolve().parent
def functions_only(path):
    tree = ast.parse(path.read_text())
    tree.body = [n for n in tree.body if isinstance(n, (ast.Import, ast.ImportFrom, ast.FunctionDef))]
    ns = {}
    exec(compile(tree, str(path), 'exec'), ns)
    return ns

checks = {}
mu, s, z = sp.symbols('mu s z', real=True)
p = 3*(1+mu**2)/8
e2 = sp.integrate(p*mu**2, (mu,-1,1))
Kz2 = sp.expand(z**2*e2 + (s-z**2)*(1-e2)/2)
bracket = sp.expand(Kz2 + z**2)  # E[z_new]=0
checks['normalized_kernel'] = sp.integrate(p,(mu,-1,1)) == 1
checks['angular_second_moment'] = e2 == sp.Rational(2,5)
checks['actual_jump_bracket'] = bracket == 3*s/10+11*z**2/10
checks['qwen_bracket_refuted'] = sp.expand(bracket-sp.Rational(3,8)*(s+z**2)) != 0
# Exact input-constraint failures, not a calculation of actual variance.
M, claimed_d = sp.Integer(10), sp.Rational(1,2)
r0 = claimed_d/M
actual_d = M*r0**2/2
checks['step_claimed_mean_refuted'] = actual_d != claimed_d
checks['step_correct_radius'] = sp.simplify(M*sp.sqrt(2*claimed_d/M)**2/2-claimed_d) == 0
# A continuous profile <=1 with integral r*k(r)=1/2 must equal one everywhere
# except potentially r=0, where continuity fixes the value as well. Therefore
# the radial moment of any such admissible profile is exactly 1/3.
checks['saturated_cap_radial_moment'] = sp.integrate(s**2,(s,0,1)) == sp.Rational(1,3)

ns = functions_only(ROOT/'f0773c84727d48feaac1155b82ebf844.py')
# Preserve Qwen's implementation byte-for-byte. Fresh disjoint seeds; no
# change to the transport, observable, uncertainty formula, or sample retention.
N=32000
runs=[]
for j, alpha in enumerate([0.1,0.5]):
    D, ne = ns['killed_transport'](N,1.,alpha,9910001+10*j)
    weighted_mean, weighted_se, w = ns['conservative_transport'](N,1.,alpha,9910002+10*j)
    p_escape=ne/N
    escape_se=np.sqrt(p_escape*(1-p_escape)/N+np.var(w,ddof=1)/N)
    mean_z=(D.mean()-weighted_mean)/np.sqrt(np.var(D,ddof=1)/ne+weighted_se**2)
    escape_z=(p_escape-w.mean())/escape_se
    Dneg, neneg=ns['killed_transport'](N,1.,alpha/2,9910003+10*j)
    pneg=neneg/N
    negative_escape_z=(pneg-w.mean())/np.sqrt(pneg*(1-pneg)/N+np.var(w,ddof=1)/N)
    checks[f'mean_agreement_{alpha}']=bool(abs(mean_z)<4)
    checks[f'escape_agreement_{alpha}']=bool(abs(escape_z)<4)
    checks[f'negative_escape_mismatch_{alpha}']=bool(abs(negative_escape_z)>6)
    checks[f'nonnegative_delay_{alpha}']=bool(D.min()>-1e-12)
    runs.append(dict(alpha=alpha,n=N,seeds=[9910001+10*j,9910002+10*j,9910003+10*j],
      killed_mean=float(D.mean()),weighted_mean=weighted_mean,mean_z=float(mean_z),
      escape_fraction=p_escape,weighted_escape=float(w.mean()),escape_z=float(escape_z),
      ESS=float(w.sum()**2/(w*w).sum()),negative_escape_z=float(negative_escape_z)))
result={'checks':checks,'all_checks_pass':all(checks.values()),'runs':runs,
        'exact':{'Kz2':str(Kz2),'bracket':str(bracket),'step_actual_mean':str(actual_d)},
        'scope':'Independent audit harness of Qwen source; finite transport calibration only. No universal cap theorem or novelty established.'}
out=ROOT/'certified'/'result.json'
out.parent.mkdir(exist_ok=True)
out.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
raise SystemExit(0 if all(checks.values()) else 1)
