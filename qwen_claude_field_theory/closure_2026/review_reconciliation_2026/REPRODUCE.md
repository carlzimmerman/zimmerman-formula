# Replay the narrow disputes without changing the theory

Run from the repository root. This is a documented diagnostic, not a replacement force law, flux solver or theory-certification suite. It selects named definitions from source with Python's AST to avoid executing the original scripts' top-level scans. Missing/changed definitions raise errors; the source hashes identify what was tested.

Command:

    OPENBLAS_NUM_THREADS=1 python -B -c 'from pathlib import Path; p=Path("qwen_claude_field_theory/closure_2026/review_reconciliation_2026/REPRODUCE.md"); exec(compile(p.read_text().split("```python\n",1)[1].split("```",1)[0],str(p),"exec"))'

```python
import ast
import hashlib
import json
import math
import platform
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import scipy
from scipy.integrate import quad
from scipy.optimize import brentq, minimize_scalar

started = datetime.now(timezone.utc).isoformat()
t0 = time.monotonic()
base = Path("qwen_claude_field_theory/closure_2026")
force_path = base / "g04k_infall_3d_particles.py"
flux_path = Path("kappa_closure/k04_four_form_promotion_consistency.py")
gate_path = base / "g03x_nurar_carrier_and_cassini.py"
inverse_path = base / "g02_filtered_efe.py"
paper_path = Path("qwen_claude_field_theory/papers_2026/mnras_submission_2026/mnras_a0_lambda_coefficient.tex")
paths = [force_path, flux_path, gate_path, inverse_path, paper_path]

def select(path, functions=(), assignments=()):
    selected = []
    found = set()
    for node in ast.parse(path.read_text()).body:
        if isinstance(node, ast.FunctionDef) and node.name in functions:
            selected.append(node)
            found.add(node.name)
        elif isinstance(node, ast.Assign):
            names = {n.id for target in node.targets for n in ast.walk(target)
                     if isinstance(n, ast.Name)}
            if names.intersection(assignments):
                selected.append(node)
                found.update(names)
    required = set(functions) | set(assignments)
    if not required.issubset(found):
        raise RuntimeError(f"Missing definitions in {path}: {required - found}")
    return compile(ast.Module(body=selected, type_ignores=[]), str(path), "exec")

f = {"np": np}
exec(select(force_path, functions=("Delta",)), f)
s = np.array([1e-24, 1e-30, 1e-36, 1e-90, 0.0])
multiplier = f["Delta"](s) / np.maximum(s, 1e-30)
# Literal force-map fixture, fields in units of a0: internal=-0.0199, external=+0.02.
# This checks the map at one admissible field pair, not a particle trajectory.
g_internal, g_external = -0.0199, 0.02
s_fixture = abs(g_internal + g_external)
extra = abs(g_internal) * float(f["Delta"](s_fixture)) / max(s_fixture, 1e-30)

k = {"np": np, "math": math, "quad": quad, "minimize_scalar": minimize_scalar}
exec(select(flux_path, functions=("j_of", "Dl", "a0loc_ratio"),
            assignments=("Delta", "opt", "s_sat", "jsat")), k)
s0 = 200.0
r = k["a0loc_ratio"](s0, 1.0, 0.0)
local_s = s0/r
residual = r*(1 + (local_s*k["Dl"](local_s) - k["j_of"](local_s))/(32*math.pi))-1
x = 2.5
D, j = k["Dl"](x), k["j_of"](x)
ex = math.exp(math.sqrt(x))
Dp = ((ex-1) - math.sqrt(x)*ex/2)/(ex-1)**2
secant = 1 + (x*D-j)/(32*math.pi)
hessian = 1 + (2*x*D-j-D*D/Dp)/(32*math.pi)

# At the baseline eN_of uses y*mu_exp(y)*a0. Check that source condition,
# then compare it with the selected replacement kernel's own scalar inverse.
inverse_source = inverse_path.read_text()
gate_source = gate_path.read_text()
old_call_present = "return yv*mu_exp(yv)*a0" in inverse_source
swap_present = 'g["nu"] = nufun' in gate_source and "eN = eN_of(gobs, a0)" in gate_source
a0, gobs = 9.3619e-11, 2.32e-10
y = gobs/a0
s_old = y*(-math.expm1(-y))
s_new = brentq(lambda z: z+k["Dl"](z)-y, 1e-8, 10.0)

out = {
    "baseline_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
    "dirty": bool(subprocess.check_output(["git", "status", "--porcelain"], text=True)),
    "started_at": started,
    "runtime_seconds": time.monotonic()-t0,
    "software": {"python": platform.python_version(), "numpy": np.__version__, "scipy": scipy.__version__},
    "hardware": platform.machine(),
    "source_hashes": {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},
    "force_map": {"s": s.tolist(), "extra_multiplier": multiplier.tolist(),
                  "finite_at_test_points": bool(np.isfinite(multiplier).all()),
                  "extra_at_exact_cancellation": float(multiplier[-1]),
                  "fixture_extra_in_a0": extra, "claimed_cap_in_a0": 0.6476,
                  "literal_divergence_claim": "withdrawn"},
    "four_form": {"s0": s0, "returned_ratio": r, "normalized_flux_residual": residual,
                  "residual_within_1e-8": bool(abs(residual)<1e-8),
                  "hessian_fixture_s": x, "secant_over_Z": secant,
                  "fixed_Y_hessian_over_Z": hessian,
                  "ghost_verdict": "not determined by this check"},
    "external_input": {"old_exp_call_present": old_call_present,
                       "kernel_swap_call_present": swap_present,
                       "gobs": gobs, "a0": a0, "s_old": s_old,
                       "s_replacement": s_new, "relative_difference": s_old/s_new-1},
    "btfr_statistic": {"definition": "-log10(a0_ratio)",
                       "ratio_2_13": -math.log10(2.13), "ratio_0_82": -math.log10(.82)},
    "interpretation": "Diagnostic executed; not a theory PASS or a full-model no-go.",
    "non_claims": ["No full particle rerun", "No corrected force or flux solver",
                   "No full constrained stability calculation", "No proof all completions fail"]
}
print(json.dumps(out, indent=2, allow_nan=False))
```

The Hessian fixture assumes the differentiable unsaturated branch, fixed Y, K_B=0 and Z/beta^2=8. It is a partial-variation check, not an eigenvalue of the fully reduced physical Hamiltonian. The force fixture checks the implemented algebra, not whether the simulation realizes that configuration. The printed BTFR numbers check arithmetic under the manuscript's definition, not a generic prediction of every Lambda-CDM galaxy model.
