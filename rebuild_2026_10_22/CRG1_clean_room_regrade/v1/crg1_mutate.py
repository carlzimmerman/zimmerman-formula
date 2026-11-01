"""MUTATE: nu=1 in the law, line S for C4 must fail. Excess sign flip result copied in. Separate outputs."""
from crg1_core import *
import shutil, sys
assert MUT_NU1
import crg1_sparc as SP
G = SP.load_gal(); out = {}
for foot in A0:
    r = SP.fit(G, SP.m_law(A0[foot]))
    out[foot] = dict(rms=r["rms"], Y_med=r["Y_med"], S_passed=SP.line_S([r, r]))
flip = json.load(open(os.path.join(HERE, "partials", "k1_shear_FLIP.json")))
res = dict(mutation_nu_is_1=dict(C4_S=out, must_fail=True, ok=not out["canonical"]["S_passed"]),
           mutation_excess_sign_flip=dict(result=flip, must_fail_exit_1=True, ok=not flip["passed"]))
write_atomic(os.path.join(HERE, "crg1_results_MUTATE.json"), dumps(res) + "\n")
log(str({k: v["ok"] for k, v in res.items()}))
sys.exit(0 if all(v["ok"] for v in res.values()) else 1)
