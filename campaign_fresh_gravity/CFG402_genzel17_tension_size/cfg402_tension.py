"""CFG402: size CFG401's possible high-z tension. Criteria: FROZEN_CRITERIA.md (1d58728ee). Reuses CFG401's shape/data code (exec'd read-only).
Run: nice python3 cfg402_tension.py ; MUTATE=1 halves the errors (the sum must ~quadruple; rc 1)."""
import os, sys, math, json, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
MUT = os.environ.get("MUTATE") == "1"
os.environ.pop("MUTATE", None)                         # CFG401's own MUTATE flag must stay off
src = open(os.path.join(HERE, "..", "CFG401_genzel17_gas_shape", "cfg401_gas_shape.py")).read()
pre = src.split('LF = np.linspace(-3, 3, 601)')[0].replace('HERE = os.path.dirname(os.path.abspath(__file__))',
      f'HERE = "{os.path.join(HERE, "..", "CFG401_genzel17_gas_shape")}"')
exec(pre)
lines_out = []
def P(s=""): print(s); lines_out.append(s)
if MUT:
    for d in data.values(): d["elog"] = d["elog"] / 2
LF = np.linspace(-4, 3, 701); SC = np.logspace(-3, 2, 251)
def chi(d, a0, stars_only=False):
    gb = gshape(d["R"], d["Rh"], d["bt"], 0.0 if stars_only else d["fgas"]); best = 1e99
    for lf in LF:
        gn = gb * 10**lf * 1e11
        nu = 1.0 if a0 == 0 else C4.nu_mono(gn / a0)
        best = min(best, float(np.sum(((np.log10(d["gobs"]) - np.log10(nu * gn)) / d["elog"]) ** 2)))
    return best
out = {}
for shape in ("gas2Rd (primary)", "stars-only (reported)"):
    so = shape.startswith("stars")
    for foot, a0f in A0.items():
        tot = {"DE": 0.0, "RIVAL": 0.0, "NEWTON": 0.0}
        P(f"\n{shape} | {foot}")
        for g, d in data.items():
            prof = [chi(d, a0f * s, so) for s in SC]; cmin = min(prof); sbest = SC[int(np.argmin(prof))]
            dDE = chi(d, a0f * de(d["z"]), so) - cmin; dRV = chi(d, a0f * E(d["z"]), so) - cmin; dNW = chi(d, 0, so) - cmin
            tot["DE"] += dDE; tot["RIVAL"] += dRV; tot["NEWTON"] += dNW
            P(f"  {g:11s} best a0 x{sbest:.3f} | Delta chi2: DE {dDE:6.2f}  RIVAL {dRV:6.2f}  Newton {dNW:6.2f}")
        rd = "TENSION REAL" if tot["DE"] >= 9 else ("WEAK" if tot["DE"] >= 4 else "NOISE")
        P(f"  SUM: DE {tot['DE']:.2f}  RIVAL {tot['RIVAL']:.2f}  Newton {tot['NEWTON']:.2f}  -> DE reading: {rd}")
        out[f"{shape}|{foot}"] = dict(tot, reading=rd)
prim = [out[f"gas2Rd (primary)|{f}"]["reading"] for f in A0]
V = prim[0] if prim[0] == prim[1] else f"{prim[0]} (canonical) / {prim[1]} (alt)"
P(f"\nVERDICT (primary shape, both footings): {V}")
json.dump({"lane": "CFG402", "mutate": MUT, "results": out, "verdict": V}, open(os.path.join(HERE, f"cfg402_results{'_MUTATE' if MUT else ''}.json"), "w"), indent=1)
open(os.path.join(HERE, f"cfg402{'_MUTATE' if MUT else ''}.out"), "w").write("\n".join(lines_out) + "\n")
sys.exit(1 if MUT else 0)
