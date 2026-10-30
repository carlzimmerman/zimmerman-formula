#!/usr/bin/env python3
"""X78_footing_upsilon_floor (criteria aff1af6c79, renamed 4ecd7ac9a3): where does the plain a0 law's SPARC median best-fit
Upsilon cross the 0.50 stellar-population floor?  EM1's own law fit, unchanged, read-only (up to the backgrounds section).
kappa = 1/2 FITTED; footings never pooled; not theory closed."""
import contextlib, io, json, math, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE)
SRC = os.path.join(REB, "EM1_emergent_dust_law", "em1_emergent.py"); TE = open(SRC).read()
NE = {"__file__": SRC, "__name__": "em1_ro"}; a_ = sys.argv; sys.argv = [SRC]
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(TE[:TE.index("# ---------------- backgrounds")], SRC, "exec"), NE)
sys.argv = a_
GALS, fit_one, pooled, A0, LAW = NE["GALS"], NE["fit_one"], NE["pooled"], NE["A0"], NE["LAW"]
OUT = []
def P(s): print(s, flush=True); OUT.append(s)
def law(a0):
    rows = [fit_one(q, np.log10(np.maximum((0.5 + np.sqrt(0.25 + a0 / np.maximum(q["GB"], 1e-300))) * q["GB"], 1e-300))) for q in GALS]
    return pooled([r[0] for r in rows], [r[1] for r in rows], [r[2] for r in rows])
P("X78 footing vs the SPARC Upsilon floor (plain a0 law, EM1 machinery); kappa = 1/2 FITTED; not theory closed")
k1 = all(abs(law(A0[f])["rms"] - LAW[f]["rms"]) <= 1e-4 and law(A0[f])["U_median"] == LAW[f]["U_median"] for f in ("canonical", "alt"))
P(f"K1 law at the exact footing a0 reproduces EM1 KP: canonical {LAW['canonical']['rms']:.4f}@{LAW['canonical']['U_median']:.2f}, alt {LAW['alt']['rms']:.4f}@{LAW['alt']['U_median']:.2f}: {'PASS' if k1 else 'FAIL'}")
grid = np.round(np.arange(0.80, 1.2501, 0.005), 3) * 1e-10
tab = [(float(a), law(a)) for a in grid]
for a, s in tab: P(f"  a0 {a:.3e}: rms {s['rms']:.4f}, median U {s['U_median']:.2f}")
def star(floor):
    ok = [a for a, s in tab if s["U_median"] >= floor - 1e-9]
    return max(ok) if ok else None
res = {}
for fl in (0.45, 0.50, 0.55):
    a = star(fl); res[f"{fl:.2f}"] = dict(a0_star=a, kappa_alt_star=(0.5 * a / A0["alt"]) if a else None, kappa_can_star=(0.5 * a / A0["canonical"]) if a else None)
    P(f"floor {fl:.2f}: a0* = {a:.3e} -> kappa* on alt {0.5 * a / A0['alt']:.3f}, on canonical {0.5 * a / A0['canonical']:.3f}" if a else f"floor {fl:.2f}: no grid a0 passes")
a = res["0.50"]["a0_star"]
rd = ("the Upsilon floor admits the canonical footing and excludes the alt footing at kappa = 1/2" if a and A0["canonical"] <= a < A0["alt"]
      else "other: see table")
P(f"READING (floor 0.50): a0_canonical {A0['canonical']:.4e}, a0* {a:.3e}, a0_alt {A0['alt']:.4e} -> {rd}")
P("route E at c_f 4 on alt (X73/X74): median U 0.47 (rule active 0/175), quoted, not regraded")
open(os.path.join(HERE, "x78_footing_upsilon.out"), "w").write("\n".join(OUT) + "\n")
json.dump(dict(k1=k1, A0=A0, table=[dict(a0=a_, **s) for a_, s in tab], floors=res, reading=rd), open(os.path.join(HERE, "x78_footing_upsilon_results.json"), "w"), indent=1)
sys.exit(0 if k1 else 1)
