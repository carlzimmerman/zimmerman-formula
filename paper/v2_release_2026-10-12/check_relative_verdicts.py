"""Bounded audit of the actual classifier, with exact illustrative residuals.

No survey data are simulated or refitted. Only the standalone pure `klass`
function is extracted from the source AST; the survey module is not imported.
"""
import ast
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / 'campaign_fresh_gravity/CFG592_cosmic_shear_likelihood/cfg592_native.py'
tree = ast.parse(SRC.read_text())
fn = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'klass')
module = ast.fix_missing_locations(ast.Module(body=[fn], type_ignores=[]))
ns = {'__builtins__': {'min': min, 'max': max}}
exec(compile(module, str(SRC), 'exec'), ns)
klass = ns['klass']

# Whitened scalar data d=0 and unit covariance: chi-square = residual squared.
# Robustness variants are identical by construction. No nuisance parameters.
rows = []
for label, s, f in [('equal_bad', 100, -100), ('perfect_candidate', 100, 0),
                    ('both_close', 0, 1), ('relative_penalty', 0, 3)]:
    cs, cf = s*s, f*f
    delta = cf-cs
    rows.append(dict(case=label, control_chi2=cs, candidate_chi2=cf,
                     delta=delta, classification=klass(delta, [delta]*4, True)))
assert rows[0]['classification'] == 'CONSISTENT'
assert rows[0]['candidate_chi2'] == 10000
assert rows[1]['classification'] == 'CONSISTENT'
assert rows[2]['classification'] == 'CONSISTENT'
assert rows[3]['classification'] == 'EXCLUDED'
assert klass(0, [0]*4, False) == 'NOT DIAGNOSTIC'

# Same difference and same class at arbitrarily large absolute residual:
# N=2, covariance I; control=(M,0), candidate=(M,1); delta=1 for every M.
family = []
for m in [0, 1, 10, 100, 10**6]:
    cs, cf = m*m, m*m+1
    assert cf-cs == 1
    assert klass(cf-cs, [1]*4, True) == 'CONSISTENT'
    family.append(dict(M=m, control_chi2=cs, candidate_chi2=cf, delta=cf-cs))

# Shared-input cancellation counterexample: observed d=1, fixed modification e=1.
shared = []
for s in [0, 1]:
    r, e = s-1, 1
    difference = (s+e-1)**2-(s-1)**2
    assert difference == e*e+2*r*e
    shared.append(dict(control=s, modification=e, observed=1, delta=difference))
assert [r['delta'] for r in shared] == [-1, 1]

result = {'claim':'The classifier is relative and does not certify absolute fit; shared inputs do not cancel generally.',
          'source':str(SRC.relative_to(ROOT)), 'function_line':fn.lineno,
          'scalar_cases':rows, 'unbounded_residual_family_tested':family,
          'shared_input_counterexample':shared,
          'non_claims':['No survey likelihood rerun.', 'No evidence that either cosmology is correct.',
                        'No calibration of significance or attribution of the observed mismatch.']}
out = Path(__file__).with_name('relative_verdict_run')/'result.json'
out.write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps(result, indent=2))
