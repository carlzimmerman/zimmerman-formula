#!/usr/bin/env python3
"""CFG715 (criteria of this dir): third probe. CFG714's extra isothermal component (1 + q = 10^Delta_pred) predicts the SLUGGS outer
GC dispersion excess over the bare law: Delta log sigma = 0.5 log10(1 + q) = 0.5 Delta_pred. Data: CFG38 committed results (SLUGGS's
own stellar masses; CFG55 dynamical-mass variant as context). kappa = 1/2 FITTED; not theory closed."""
import os, sys, json, math
HERE = os.path.dirname(os.path.abspath(__file__)); L = os.path.dirname(HERE)
MUT = os.environ.get("CFG715_MUTATE", "0") == "1"; TAG = "_MUTATE" if MUT else ""
c714 = json.load(open(os.path.join(L, "CFG714_inner_outer_excess", "cfg714_results.json")))
c38 = json.load(open(os.path.join(L, "CFG38_sluggs_massive_passive_results.json")))["numbers"]["RES"]
c55 = json.load(open(os.path.join(L, "CFG55_sluggs_dynamical_masses_results.json")))["numbers"]["RES"]
OUT, RES = [], {"lane": "CFG715"}
P = lambda x: (print(x), OUT.append(x))
for foot in ("canonical", "alt"):
    obs, eo = c38[foot]["law_mean"], c38[foot]["law_err"]
    obs55, eo55 = c55[foot]["law"]["mean"], c55[foot]["law"]["err"]
    RES[foot] = {}
    for lab, d, s in (("primary", c714[foot]["delta_pred"], c714[foot]["boot"]), ("all43", c714[foot]["delta_pred_variant"], c714[foot]["boot_variant"])):
        d = 0.0 if MUT else d
        pred, sp = 0.5 * d, 0.5 * s
        for dlab, o, e in (("SLUGGS_masses", obs, eo), ("dynamical_masses", obs55, eo55)):
            z = (pred - o) / math.hypot(sp, e); v = "CONSISTENT" if abs(z) <= 2 else ("INCONSISTENT" if abs(z) > 3 else "TENSION")
            RES[foot][f"{lab}_{dlab}"] = dict(pred=pred, pred_err=sp, obs=o, obs_err=e, z=z, verdict=v)
            P(f"{foot} {lab:7s} vs {dlab:16s}: predicted {pred:+.4f} +- {sp:.4f}, observed {o:+.4f} +- {e:.4f}, z {z:+.2f} -> {v}")
code = 0
if MUT:
    bite = all(abs(v["pred"]) < 1e-12 for f in ("canonical", "alt") for v in RES[f].values()); P(f"MUTATE q->0: {'BITES' if bite else 'NO'}"); code = 1 if bite else 0
json.dump(RES, open(os.path.join(HERE, f"cfg715_results{TAG}.json"), "w"), indent=1)
open(os.path.join(HERE, f"cfg715{TAG}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(code)
