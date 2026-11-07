#!/usr/bin/env python3
"""GL3 comparison (criteria FROZEN_CRITERIA.md). Reads each lane's committed JSON (pristine origin/main copy) and the JSON
the same unchanged script wrote in three sandboxes (kernel old / new / k2), and writes gl3_compare.json:
  - KA: max relative difference over every numeric leaf, old-kernel run vs committed (must be ~0);
  - every numeric leaf that differs between old and new (the kernel's footprint), with old / new / k2 values.
Usage: python3 gl3_compare.py <sandbox base dir>   (base holds gl3sb = pristine, gl3_old, gl3_new, gl3_k2)
kappa = 1/2 FITTED; not theory closed."""
import json, os, sys, math
BASE = sys.argv[1]
HERE = os.path.dirname(os.path.abspath(__file__))
FILES = {
 "SV5_iter1": "closure_2026_11_06/SV5_growth_mechanism/iter_1_law_on_web/sv5_iter1.json",
 "SV5_iter3_t0": "closure_2026_11_06/SV5_growth_mechanism/iter_3_a0z_tied_coupling/sv5_iter3.json",
 "SV5_iter2": "closure_2026_11_06/SV5_growth_mechanism/iter_2_charge_switched_sound_speed/sv5_iter2.json",
 "QX27_growth": "closure_2026_11_06/QX27_tail_retention_sector/qx27_growth.json",
 "QX28_growth": "closure_2026_11_06/QX28_superfluid_two_phase/qx28_growth.json",
 "QX29_growth": "closure_2026_11_06/QX29_dipolar_medium/qx29_growth.json",
 "QX31": "closure_2026_11_06/QX31_growth_cmb_data_assumptions/qx31.json",
 "OQ1": "closure_2026_11_06/OQ1_one_quantity_both_walls/oq1.json",
 "OQ2_stage0": "closure_2026_11_06/OQ2_one_quantity_powered/oq2_stage0.json",
 "SV5_t0": "closure_2026_11_06/SV5_growth_mechanism/sv5_t0.json",
 "OQ2": "closure_2026_11_06/OQ2_one_quantity_powered/oq2.json",
 "WL1": "closure_2026_11_07/WL1_web_law_switch/wl1.json",
 "NA1": "closure_2026_11_07/NA1_fa1_last_doors/na1.json",
 "FA2": "closure_2026_11_07/FA2_local_action_search/fa2.json",
 "FA3": "closure_2026_11_07/FA3_nonlocal_action_search/fa3.json",
 "EW2_iter2": "closure_2026_11_07/EW2_aest_nonlinear/iter_2_web_cmb_kids/ew2_iter2.json",
}
SKIP = ("seconds", "time", "elapsed", "rss", "wall")

def flat(x, p=""):
    if isinstance(x, dict):
        for k, v in x.items(): yield from flat(v, f"{p}/{k}")
    elif isinstance(x, list):
        for i, v in enumerate(x): yield from flat(v, f"{p}[{i}]")
    elif isinstance(x, bool) or x is None:
        yield p, x
    elif isinstance(x, (int, float)):
        yield p, float(x)
    else:
        yield p, x

def load(k, f):
    p = os.path.join(BASE, k, f)
    return dict(flat(json.load(open(p)))) if os.path.exists(p) else None

def rel(a, b):
    if isinstance(a, float) and isinstance(b, float):
        if math.isnan(a) and math.isnan(b): return 0.0
        if math.isinf(a) or math.isinf(b): return 0.0 if a == b else float("inf")
        return abs(a - b) / max(abs(a), abs(b), 1e-300)
    return 0.0 if a == b else float("inf")

out = {}
for name, f in FILES.items():
    ref, old, new, k2 = (load(k, f) for k in ("gl3sb", "gl3_old", "gl3_new", "gl3_k2"))
    if ref is None or old is None:
        out[name] = {"status": "MISSING", "ref": ref is not None, "old": old is not None}; continue
    keys = [k for k in ref if not any(s in k.lower() for s in SKIP)]
    ka = [(rel(ref[k], old.get(k)), k) for k in keys]
    worst = max(ka) if ka else (0.0, "")
    diffs = {}
    if new is not None:
        for k in keys:
            if k in new and rel(old.get(k), new[k]) > 1e-9:
                diffs[k] = {"old": old.get(k), "new": new[k], "k2": (k2 or {}).get(k)}
    out[name] = {"KA_max_rel": worst[0], "KA_worst_key": worst[1], "KA_pass": bool(worst[0] <= 1e-9),
                 "n_leaves": len(keys), "n_changed_old_to_new": len(diffs), "changed": diffs}
json.dump(out, open(os.path.join(HERE, "gl3_compare.json"), "w"), indent=1, default=str)
for n, r in out.items():
    if r.get("status") == "MISSING": print(f"{n}: MISSING {r}"); continue
    print(f"{n}: KA max rel {r['KA_max_rel']:.2e} ({'PASS' if r['KA_pass'] else 'FAIL: ' + r['KA_worst_key']}); "
          f"{r['n_changed_old_to_new']} of {r['n_leaves']} leaves change old -> new")
