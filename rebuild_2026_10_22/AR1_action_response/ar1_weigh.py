#!/usr/bin/env python3
"""AR1 UR3 weighing as UL1 corrected it, action response in place of Blumenthal. Reported only. UR3's, SP3's and UL1's code read only. kappa = 1/2 FITTED, unused; not theory closed."""
import json, os, sys
sys.dont_write_bytecode = True
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"): os.environ[v] = "1"
ME = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(ME); SP = os.path.join(RB, "SP3_starting_point"); sys.path.insert(0, ME); import ar1_solver as AS
s = open(os.path.join(SP, "sp3_post.py")).read(); s = s[:s.index('P("c: EM1 line')]; __file__ = os.path.join(SP, "sp3_post.py"); exec(s)
OUT.clear(); R = {}; _O = U.contract
def act(r, Mb, M0, F, gnedin=None): return AS.act_contract(r, Mb, M0, F)
def use(on):
    f = act if on else _O; U.contract = f; DN["contract"] = f; MN["contract"] = f; globals()["contract"] = f
P("AR1 weighing. r target 0.90-1.10, n >= 27; MW FEASIBLE IN PRIORS. EM1, Baryons as UR3's rows (spherical-by-hand for MW, its Mbar for DiskMass). Reported only")
for lab, kw in (("NFW c200 8.0", dict(shape="nfwc", c=8.0)), ("NFW c200 6.25", dict(shape="nfwc", c=6.25)), ("NFW c200 9.625", dict(shape="nfwc", c=9.625)), ("hand", dict(shape="hand"))):
    for on in (False, True):
        use(on); show(f"{lab} {'action' if on else 'blum'}", mode="blum", **kw); json.dump(R, open(os.path.join(ME, "ar1_weigh.json"), "w"), indent=1, default=float); open(os.path.join(ME, "ar1_weigh.out"), "w").write("\n".join(OUT) + "\n")
