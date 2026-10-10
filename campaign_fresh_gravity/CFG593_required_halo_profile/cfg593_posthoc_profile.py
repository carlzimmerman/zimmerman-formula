#!/usr/bin/env python3
"""CFG593 POST-HOC (dated 2026-10-10; NOT a verdict input): the post-hoc overlap of cfg593_posthoc.py D4 (SHMR-LCDM-normalised KiDS family
intersected with the frozen shear-allowed set) described as a profile: closest-to-both point per footing, its halo-model M/M_L(<r) and drained-shell
depth, side constraints (frozen side scan), and the ranges of the overlap.
  nice -n 10 python3 cfg593_posthoc_profile.py -> cfg593_posthoc_profile.out, cfg593_posthoc_profile_results.json
kappa = 1/2 FITTED; footings never pooled; cold energy mass required; not theory closed."""
import os, sys, json
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np
from scipy import stats
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import cfg593_lib as FL
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
J4 = json.load(open(os.path.join(HERE, "cfg593_posthoc_results.json")))["D4"]
JC = json.load(open(os.path.join(HERE, "cfg593_side_results.json")))
X2C = float(stats.chi2.isf(0.01, 15))
H = FL.H556()
P("CFG593 POST-HOC profile of the D4 overlap (NOT a verdict input; data-driven, NOT a framework derivation).")
res = dict(lane="CFG593", script="cfg593_posthoc_profile", date="2026-10-10", note="POST-HOC, not a verdict input", footings={})
for ft in ("canonical", "alt"):
    pts = J4[ft]["points"]; ov = J4[ft]["overlap"]
    if not ov:
        P(f"[{ft}] no D4 overlap"); continue
    d = {k: max(pts[k]["shear_Zmax"] / 2, max(pts[k]["chi2_A"], pts[k]["chi2_B"]) / X2C) for k in ov}
    kb = min(d, key=d.get); b = pts[kb]
    side = [k for k in ov if JC["scan"][f"{ft}|total|{k}"]["allowed"]]
    rng = dict(xe=[min(pts[k]["xe"] for k in ov), max(pts[k]["xe"] for k in ov)], f=[min(pts[k]["f"] for k in ov), max(pts[k]["f"] for k in ov)],
               y=sorted({pts[k]["y"] for k in ov}), contains_f1=any(pts[k]["f"] == 1.0 for k in ov), contains_f0=any(pts[k]["f"] == 0.0 for k in ov))
    P(f"[{ft}] D4 overlap {len(ov)} points: x_e {rng['xe']}, f {rng['f']}, y {rng['y']}; f = 1 inside: {rng['contains_f1']}; with frozen side constraints (c): {len(side)}")
    P(f"[{ft}] closest-to-both point x_e {b['xe']} f {b['f']} y {b['y']}: shear Zmax {b['shear_Zmax']:.2f}; KiDS chi2 A {b['chi2_A']:.2f} B {b['chi2_B']:.2f}; "
      f"groups Z {JC['scan'][f'{ft}|total|{kb}']['groups_Z']:+.2f}, MW pass {JC['scan'][f'{ft}|total|{kb}']['mw_pass']}")
    prof = {}
    for lt in (12, 13, 14, 15):
        hb = H["halo_basics"](10 ** np.interp(lt, np.log10(H["MTA"]), H["LM"]))
        r, M, inf = FL.hm_profile(hb, ft, b["xe"], b["f"], b["y"])
        rat = {str(x): float(np.interp(x * hb["rta"], r, M) / H["M_L"](hb, x * hb["rta"])) for x in (0.05, 0.1, 0.2, 0.3, 0.5)}
        prof[str(lt)] = dict(ratios=rat, q=inf["q"], re_over_rta=inf["re_over_rta"], rin_over_rta=inf["rin"] / hb["rta"], r200m_over_rta=hb["r200"] / hb["rta"],
                             capped_supply=bool(inf.get("capped_supply", False)))
        P(f"    log M_ta {lt}: M/M_L at 0.05/0.1/0.2/0.3/0.5 r_ta = " + " ".join(f"{v:.2f}" for v in rat.values())
          + f"; r_e/r_ta {inf['re_over_rta']:.3f} (r200m/r_ta {hb['r200'] / hb['rta']:.3f}); drained-shell depth q {inf['q']:+.3f}; supply-capped {prof[str(lt)]['capped_supply']}")
    res["footings"][ft] = dict(n_overlap=len(ov), ranges=rng, n_with_side=len(side), closest=dict(key=kb, **b), profiles=prof)
json.dump(res, open(os.path.join(HERE, "cfg593_posthoc_profile_results.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, "cfg593_posthoc_profile.out"), "w").write("\n".join(OUT) + "\n")
