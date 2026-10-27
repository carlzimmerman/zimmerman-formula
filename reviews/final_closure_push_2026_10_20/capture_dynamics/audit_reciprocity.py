#!/usr/bin/env python3
"""Independent algebra reconstructed from the two reciprocal-energy notes."""
from pathlib import Path
import hashlib
import json
import math
import platform
import resource
import sys
import time
from datetime import datetime, timezone

import sympy as s

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
PREFIX = "reviews/final_closure_push_2026_10_20/reciprocity/"
inputs = [PREFIX + "SOURCE_RESPONSE.md", PREFIX + "POSITIVE_WARM_COMPARISON.md",
          PREFIX + "check.py", str(Path(__file__).relative_to(ROOT))]
hashes = {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in inputs}
started = datetime.now(timezone.utc).isoformat()
start = time.monotonic()
checks = []
def zero(name, expression):
    value = s.simplify(expression)
    checks.append({"name": name, "residual": str(value), "pass": value == 0})
    assert value == 0, (name, value)

B, T, F, G, r, a0 = s.symbols("B T F G r a0", positive=True)
Ugrav = -G * ((B + T + F)**2 - T**2) / (2 * r**2)
zero("independent_t_variation", s.diff(Ugrav, T) + G * (B + F) / r**2)
zero("independent_f_variation", s.diff(Ugrav, F) + G * (B + T + F) / r**2)
zero("independent_b_variation", s.diff(Ugrav, B) + G * (B + T + F) / r**2)
mixed = s.diff(Ugrav, T, F)
zero("mixed_derivative_reconstructed", mixed + G / r**2)
zero("mixed_symmetry", mixed - s.diff(Ugrav, F, T))
shell = -G / 4 + G / 3 + G / 4 - G / 2
zero("shell_cross_coefficient_reconstructed", shell + G / 6)
u = s.symbols("u", positive=True)
R = u**2 / (a0-u)
zero("du_ds_inverse_derivative", 1 / s.diff(R, u) - (a0-u)**2 / (u*(2*a0-u)))
zero("full_simple_law_inverse", (R+u)**2 / (R+u+a0) - R)
zero("dg_ds_formula", 1 + 1/s.diff(R, u) - a0**2/(u*(2*a0-u)))

Mb, A, psi, d = s.symbols("Mb A psi d", positive=True)
Tb = Mb/2 * (s.sqrt(1 + 4*a0*r**2/(G*Mb)) - 1)
rho = a0 / (2*s.pi*G*r*s.sqrt(1+4*a0*r**2/(G*Mb)))
zero("warm_density_from_enclosed_mass", s.diff(Tb, r)/(4*s.pi*r**2)-rho)
ddef = A*s.sqrt(4*a0/(G*Mb))
Cdef = a0/(2*s.pi*G*A)
zero("warm_density_in_psi", rho.subs(r,A/psi)-Cdef*psi**2/s.sqrt(psi**2+ddef**2))
h = psi**2/s.sqrt(psi**2+d**2)
expected = psi*(psi**4+d**2*psi**2+6*d**4)/(2*(psi**2+d**2)**s.Rational(5,2))
zero("Abel_positive_bracket", s.diff(h,psi)/2+psi*s.diff(h,psi,2)-expected)
zero("small_psi_bracket_coefficient", s.limit(expected/psi,psi,0)-3/d)
zero("large_psi_bracket_limit", s.limit(expected,psi,s.oo)-s.Rational(1,2))
x = s.symbols("x", real=True)
zero("Abel_double_kernel_normalization", s.integrate(1/s.sqrt(x*(1-x)),(x,0,1))-s.pi)
zero("Abel_inverse_prefactor", 1/(2*s.sqrt(2)*s.pi**2)-1/(s.sqrt(8)*s.pi**2))

after = {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in inputs}
assert hashes == after
result = {"checks": checks, "pass": len(checks), "total": len(checks),
          "non_claims": ["No full physical action derived", "No continuum stability or finite halo claimed", "No existing experiment rerun"],
          "source_hashes": hashes}
path = OUT/"reciprocity_audit_checks.json"
path.write_text(json.dumps(result,indent=2)+"\n")
rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
rss = rss if platform.system()=="Darwin" else rss*1024
manifest = {
 "schema_version":2,"claim_id":"reciprocity-independent-algebra-audit-2026-10-20",
 "repository":{"commit":"f659e6d8e1ee4cf2b756f091aff56b018da1fb1e","dirty":True},
 "command":["env","OMP_NUM_THREADS=1","OPENBLAS_NUM_THREADS=1","MKL_NUM_THREADS=1","python3",str(Path(__file__).relative_to(ROOT))],
 "environment":{"software":[{"name":"Python","version":platform.python_version()},{"name":"SymPy","version":s.__version__}],"hardware":platform.platform()+"; peak RSS "+str(rss)+" bytes"},
 "mathematics":{"assertion_tested":"16 exact symbolic residuals for all quadratic variations, mixed derivative, shell kernel, full-remainder inverse derivative, warm density and Abel positivity/normalization.","coefficient_domain":"Exact symbolic expressions over positive real parameters; 0<u<a0 for interpreted signs","conventions":"Reconstruct derivatives directly from declared Ugrav; warm force uses fixed Kepler free source.","inputs":inputs[:2],"bounds":{"symbolic_residuals":len(checks)},"non_claims":result["non_claims"]},
 "randomness":{"used":False,"generator":"none","seed":None},
 "run":{"started_at":started,"runtime_seconds":time.monotonic()-start,"exit_status":0,"status":"completed","resource_limits":{"memory_bytes":None,"cpu_seconds":None,"max_cores":1,"max_threads":1}},
 "outputs":[{"path":str(path.relative_to(ROOT)),"sha256":hashlib.sha256(path.read_bytes()).hexdigest(),"kind":"result"}],
 "checks":checks,"result":"implementation and finite symbolic assertion verified in the stated domain",
 "residual_risks":["Algebraic identities do not establish finite stock, dynamics or stability","Same-team separate-context audit; parent context and intended claim known"],
 "input_artifacts":[{"path":p,"sha256":h,"sha256_after":after[p]} for p,h in hashes.items()],
 "declared_results":[str(path.relative_to(ROOT))]
}
(OUT/"reciprocity_audit_manifest.json").write_text(json.dumps(manifest,indent=2)+"\n")
print(json.dumps({"passed":len(checks),"total":len(checks),"runtime_seconds":manifest["run"]["runtime_seconds"],"peak_RSS_bytes":rss}))
