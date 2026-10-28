#!/usr/bin/env python3
"""Fixed scalar audit only. Never imports/executes observational harnesses."""
import argparse
import hashlib
import json
import math
import resource
import sys
from pathlib import Path
import numpy as np
from scipy.optimize import brentq
from classy import Class


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
REB = ROOT / "rebuild_2026_10_22"
INPUTS = [
    HERE / "FROZEN_CRITERIA.md", HERE / "scalar_feasibility.py",
    REB / "F3_growth_audit/f3_growth_audit_results.json",
    REB / "X48_native_cf_zoom/x48_analyze_results_ng48_A2.json",
    REB / "X43_collapse_core_floor/x43_collapse_core.py",
    REB / "X43_collapse_core_floor/x43_collapse_core_results.json",
    REB / "X53_outer_lensing_law_vs_halos/x53_outer_lensing.py",
    REB / "F2_outer_lensing/f2_outer_lensing.py",
    REB / "EM1_emergent_dust_law/em1_emergent.py",
    REB / "CL3_one_number/cl3_one_number.py",
    REB / "CL3_one_number/cl3_one_number_results.json",
    REB / "CL2_native_cf_slope/cl2_native_slope_results.json",
    REB / "CF2_decoupled_threshold_map/cf2_decoupled_results.json",
    REB / "INDEPENDENT_PUSH_2026-10-28/native_l_t/run_003/results.json",
]
SHA = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
READ = lambda rel: json.loads((REB / rel).read_text())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", type=Path, required=True)
    ap.add_argument("--mutate", action="store_true")
    args = ap.parse_args()
    hashes = {str(p.relative_to(ROOT)): SHA(p) for p in INPUTS}
    args.output.mkdir(parents=True, exist_ok=True)
    out = {"mutate": args.mutate, "input_sha256": hashes, "checks": {}}
    def check(k, ok, detail):
        out["checks"][k] = {"pass": bool(ok), "detail": detail}
        print(k, "PASS" if ok else "FAIL", json.dumps(detail, sort_keys=True), flush=True)

    shapej = READ("X48_native_cf_zoom/x48_analyze_results_ng48_A2.json")["cf_by_mass"]
    shape = np.array([shapej[k] for k in ("1e+12", "1e+13", "1e+14")])
    q = lambda x: float(np.interp(x, [12., 13., 14.], shape) / shape[2])
    amp = 4 / (3 * (3 * math.log(2) - math.pi / 2))
    a0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
    floors = {
        "old_CL3": {f: a / (2 * math.pi * 6.67430e-11) * 3.0856775814913673e16 ** 2 / 1.98847e30 for f, a in a0.items()},
        "X43": {f: a / (2 * math.pi * 6.67430e-11) * 3.0857e16 ** 2 / 1.98847e30 for f, a in a0.items()},
        "X53": {f: a * 3.0857e16 / 1e6 / (2 * math.pi * 4.30091e-3) for f, a in a0.items()},
    }
    pars = READ("F3_growth_audit/f3_growth_audit_results.json")["K2"]
    functions = {}
    meta = {}
    for bg in ("A_c2b_refit", "B_cfg886_bg"):
        p = pars[bg]["params"]
        cp = {"omega_b": p["omega_b"], "omega_cdm": p["omega_cdm"], "h": p["h"],
              "ln10^{10}A_s": p["lnAs"], "n_s": p["n_s"], "tau_reio": p["tau"], "N_ur": 3.044,
              "output": "mPk", "P_k_max_h/Mpc": 200., "z_max_pk": 10.}
        cc = Class(); cc.set(cp); cc.compute()
        h = p["h"]; rhom = float(cc.Omega_m()) * 2.775e11 * h ** 2
        ks = np.logspace(-4, math.log10(150), 3000)
        pk = np.array([cc.pk_lin(float(k * h), 0.) for k in ks]) * h ** 3
        lms = np.linspace(7., 16.5, 191)
        s2 = []
        for lm in lms:
            rr = (3 * 10 ** lm / (4 * math.pi * rhom)) ** (1/3) * h
            kr = ks * rr
            ww = 3 * (np.sin(kr) - kr * np.cos(kr)) / kr ** 3
            s2.append(float(np.trapz(ks ** 3 * pk * ww ** 2 / (2 * math.pi ** 2), np.log(ks))))
        zs = np.linspace(0., 30., 3001)
        ds = np.array([cc.scale_independent_growth_factor(float(z)) for z in zs]); ds /= ds[0]
        def sigma(x, rhom=rhom, s2=s2, ds=ds):
            half = float(np.interp(x - math.log10(2), lms, s2))
            full = float(np.interp(x, lms, s2))
            dform = 1.686 / (1.686 + .974 * math.sqrt(max(half - full, 0)))
            zform = float(np.interp(-dform, -ds, zs)) if dform < 1 else 0.
            rho = 18 * math.pi ** 2 * rhom * (1 + zform) ** 3
            rr = (3 * (10 ** x / 2) / (4 * math.pi * rho)) ** (1/3)
            return rho * rr / 1e12
        functions[bg] = sigma
        meta[bg] = {"class_parameters": cp, "rhom0": rhom}
        cc.struct_cleanup(); cc.empty()

    cached43 = READ("X43_collapse_core_floor/x43_collapse_core_results.json")
    points = sorted((math.log10(float(k)), math.log10(v[0])) for k, v in cached43["sigma_coll_table"].items())
    slx, sly = [p[0] for p in points], [p[1] for p in points]
    def cached_sigma(x):
        if x < slx[0]: y = sly[0] + (sly[1] - sly[0]) * (x - slx[0]) / (slx[1] - slx[0])
        elif x > slx[-1]: y = sly[-1] + (sly[-1] - sly[-2]) * (x - slx[-1]) / (slx[-1] - slx[-2])
        else: y = float(np.interp(x, slx, sly))
        return 10 ** y
    functions["X53_cached_A"] = cached_sigma
    out["inputs_numeric"] = {"S9": list(shape), "q_knots": [q(x) for x in (12., 13., 14.)], "amp": amp,
                             "floors": floors, "CLASS": meta}
    differences = [abs(functions["A_c2b_refit"](x) / 10 ** y - 1) for x, y in points]
    check("K0_X43_table_reproduction", max(differences) < 1e-10, {"max_relative_difference": max(differences)})

    def lc(x, f, sigma, floor_mode):
        return (floors[floor_mode][f] / (amp * sigma(x))) ** .8 / q(x)
    def ratio(x, lev, f, sigma, floor_mode, constant=False):
        qval = 1. if constant else q(x) / (2 if args.mutate else 1)
        return amp * (lev * qval) ** 1.25 * sigma(x) / floors[floor_mode][f]
    def crossings(lev, f, sigma, floor_mode, constant=False):
        fn = lambda x: math.log(ratio(x, lev, f, sigma, floor_mode, constant))
        grid = np.linspace(9., 16., 1001)
        vals = [fn(float(x)) for x in grid]
        brackets = [[float(a), float(b)] for a, b, va, vb in zip(grid[:-1], grid[1:], vals[:-1], vals[1:]) if va * vb < 0]
        roots = [float(brentq(fn, a, b, xtol=1e-10)) for a, b in brackets]
        return {"roots_logM": roots, "sign_change_brackets": brackets}

    cl3 = READ("CL3_one_number/cl3_one_number_results.json")
    prior = READ("INDEPENDENT_PUSH_2026-10-28/native_l_t/run_003/results.json")["fresh_CLASS_EPS_roots"]["roots"]
    rows, old_diffs, prior_diffs = [], [], []
    for lev in (3.75, 3.9, 4.):
        for f in a0:
            old = crossings(lev, f, functions["A_c2b_refit"], "old_CL3", True)
            old_diffs.append(abs(old["roots_logM"][0] - cl3["T"][str(lev)][f]))
            r = {"L": lev, "footing": f, "old_CL3_floor_constant_L": old}
            for bg, fn in functions.items():
                r[bg] = crossings(lev, f, fn, "X53" if bg == "X53_cached_A" else "X43")
            p = next(t for t in prior if t["L"] == lev and t["footing"] == f)
            pp = crossings(lev, f, functions["A_c2b_refit"], "old_CL3")
            prior_diffs.append(abs(pp["roots_logM"][0] - p["S9_mass_dependent"]["logT"]))
            rows.append(r)
    out["roots_existing_levels"] = rows
    check("K1_old_CL3_reproduction", max(old_diffs) <= .002, {"max_difference_dex": max(old_diffs)})
    markers, identities, branches = [], [], []
    for x in (12.1, 12.2, 12.3, 12.5):
        for f in a0:
            val = lc(x, f, functions["A_c2b_refit"], "X43")
            v = ratio(x, val, f, functions["A_c2b_refit"], "X43")
            identities.append(abs(v - 1))
            for eps in (-1e-6, 1e-6):
                lev = val * (1 + eps)
                branches.append((ratio(x, lev, f, functions["A_c2b_refit"], "X43") > 1) == (lev > val))
            markers.append({"logM_marker": x, "footing": f, "Lcrit_X43_A": val, "direct_ratio_at_Lcrit": v})
    out["fixed_old_threshold_markers"] = markers
    check("K2_algebraic_identity", max(identities) <= 1e-12, {"max_relative_residual": max(identities)})
    check("K3_branch_equivalence", all(branches), {"n_tested_sides": len(branches), "symbolic_equality_branch": "floor; IEEE evaluation may round across equality"})
    check("K4_prior_consistent_roots", max(prior_diffs) <= 1e-6, {"max_difference_dex": max(prior_diffs)})
    check("K5_grid_root_coverage", all(len(r[bg]["roots_logM"]) == 1 for r in rows for bg in functions), "Exactly one sign-changing bracket in each fixed finite grid; no global uniqueness theorem.")
    challenge = lc(12.3, "canonical", functions["A_c2b_refit"], "X43")
    cr = {f: {bg: crossings(challenge, f, fn, "X53" if bg == "X53_cached_A" else "X43") for bg, fn in functions.items()} for f in a0}
    out["sole_challenge"] = {"L": challenge, "definition": "Lcrit_X43_A_canonical(logM=12.3)", "roots": cr,
        "linked_core_multiplier_vs_existing_L": {str(lev): (challenge / lev) ** 1.25 for lev in (3.75, 3.9, 4.)},
        "interpretation": "Refit of the same sole L to an old empirical T midpoint. No independent free T and no blind prediction."}
    check("K6_challenge_identity", abs(cr["canonical"]["A_c2b_refit"]["roots_logM"][0] - 12.3) <= 1e-6,
          {"L": challenge, "canonical_X43_A_root": cr["canonical"]["A_c2b_refit"]["roots_logM"][0]})
    cl2 = READ("CL2_native_cf_slope/cl2_native_slope_results.json")
    cf2 = READ("CF2_decoupled_threshold_map/cf2_decoupled_results.json")
    cached = {}
    for lab, data, pred in (("CL2", cl2, lambda k: k.startswith("S9_")), ("CL3", cl3, lambda k: k.startswith("L")), ("CF2", cf2, lambda k: k.startswith("T"))):
        cached[lab] = {k: {f: {"fails": v["fails"], "groups": v["groups"], "lensing": v["lensing"],
            "G-OUT-all": v["clusters"]["G-OUT-all"]} for f, v in entry["grade"].items()}
            for k, entry in data.items() if pred(k) and isinstance(entry, dict) and "grade" in entry}
    out["cached_empirical_diagnostics"] = {"records": cached, "scope": "Old fixed-T/constant-L-switch grids only; no necessary universal corrected-model bound."}
    check("K7_inputs_stable", hashes == {str(p.relative_to(ROOT)): SHA(p) for p in INPUTS}, "All declared inputs unchanged.")
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1e9 if sys.platform == "darwin" else 1e6)
    check("K8_RSS", peak < 1., "Measured peak RSS <1GB; numeric peak only in stdout, not deterministic JSON.")
    print("PEAK_RSS_GB", peak, flush=True)
    out["outcome"] = "Conditional finite scalar tradeoff verified" if all(v["pass"] for v in out["checks"].values()) else "Audit checks failed; inspect individual controls"
    (args.output / "results.json").write_text(json.dumps(out, indent=2, sort_keys=True, allow_nan=False) + "\n")
    n = sum(v["pass"] for v in out["checks"].values())
    print(f"CSM1_SCALAR COMPLETE: {n}/{len(out['checks'])} checks PASS.")
    return 0 if n == len(out["checks"]) else 1


if __name__ == "__main__":
    raise SystemExit(main())
