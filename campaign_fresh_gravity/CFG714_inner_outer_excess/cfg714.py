#!/usr/bin/env python3
"""CFG714 (criteria 4f1e688b2): does the SLACS inner extra (CFG713) predict the KiDS outer early-type excess (CFG721)?
Outer ratio 1 + V_x^2/V_f^2, V_x^2 = G A (A from CFG713's f_x), V_f^4 = G M* a0. kappa = 1/2 FITTED; not theory closed."""
import os, sys, io, json, math, contextlib
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE)
MUT = os.environ.get("CFG714_MUTATE", "0") == "1"; TAG = "_MUTATE" if MUT else ""
P713 = os.path.join(LANES, "CFG713_slacs_required_extra", "cfg713.py")
src = open(P713).read().split("OUT, RES = [], {")[0]
g = {"__file__": P713, "__name__": "c713"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(src, P713, "exec"), g)
setup, aug, eth, C4 = g["setup"], g["aug"], g["eth"], g["C4"]
G, MSUN = C4.G_SI, C4.MSUN
R713 = json.load(open(os.path.join(LANES, "CFG713_slacs_required_extra", "cfg713_results.json")))
OBS = {"colour": (0.220, 0.030), "Sersic": (0.181, 0.029)}
OUT, RES = [], {"lane": "CFG714", "criteria": "4f1e688b2", "mutate": MUT}
P = lambda x: (print(x, flush=True), OUT.append(x))
for foot, a0 in C4.A0.items():
    prim, var = [], []
    for row in R713[foot]["rows"]:
        A_ = aug[row["name"]]; r, RE, ME, Re = setup(A_["zl"], A_["zs"], A_["ReI"], eth[row["name"]])
        fx = 0.0 if MUT else row["f_x"]
        def ratio(f, lMs):
            A = f * ME / (math.pi / 2 * RE); Vx2 = G * A; Vf2 = math.sqrt(G * 10 ** lMs * MSUN * a0)
            return math.log10(1 + Vx2 / Vf2)
        if 0 <= fx < 0.95 and row["logMstar_HX"] is not None:
            prim.append(ratio(fx, row["logMstar_HX"]))
        fc = min(max(fx, 0.0), 0.95)
        lMs_v = row["logMstar_HX"] if row["logMstar_HX"] is not None else row["logMstar_HIMF"] + math.log10(max(1 - fc, 0.05))
        var.append(ratio(fc, lMs_v))
    prim, var = np.array(prim), np.array(var)
    rng = np.random.default_rng(714)
    bs = lambda v: float(np.std([np.median(rng.choice(v, v.size)) for _ in range(4000)]))
    dp, sp = float(np.median(prim)), bs(prim); dv, sv = float(np.median(var)), bs(var)
    RES[foot] = dict(n_primary=int(prim.size), delta_pred=dp, boot=sp, n_variant=int(var.size), delta_pred_variant=dv, boot_variant=sv)
    P(f"== {foot}: primary n {prim.size}: Delta_pred = {dp:+.3f} +- {sp:.3f} dex (16-84 {np.percentile(prim,16):+.3f}..{np.percentile(prim,84):+.3f}); "
      f"variant n {var.size}: {dv:+.3f} +- {sv:.3f}")
    for split, (do, eo) in OBS.items():
        for lab, d, s in (("primary", dp, sp), ("variant", dv, sv)):
            sc = math.hypot(s, eo); z = (d - do) / sc
            v = "CONSISTENT" if abs(z) <= 2 else ("INCONSISTENT" if abs(z) > 3 else "TENSION")
            RES[foot][f"{split}_{lab}"] = dict(obs=do, z=z, verdict=v)
            P(f"   vs KiDS {split} split {do:+.3f} +- {eo:.3f}: {lab} z = {z:+.2f} -> {v}")
code = 0
if MUT:
    bite = all(abs(RES[f]["delta_pred"]) < 1e-12 for f in ("canonical", "alt")); P(f"MUTATE f_x -> 0: {'BITES' if bite else 'NO'}"); code = 1 if bite else 0
json.dump(RES, open(os.path.join(HERE, f"cfg714_results{TAG}.json"), "w"), indent=1)
open(os.path.join(HERE, f"cfg714{TAG}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(code)
