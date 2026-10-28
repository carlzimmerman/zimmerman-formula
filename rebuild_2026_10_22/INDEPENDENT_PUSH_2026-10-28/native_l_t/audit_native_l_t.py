#!/usr/bin/env python3
"""Bounded cached-input audit; no old lane is executed or written."""
import argparse
import ast
import hashlib
import json
import math
import resource
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import brentq
from classy import Class


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", required=True, type=Path)
    ap.add_argument("--mutate", action="store_true")
    args = ap.parse_args()
    root = Path(__file__).resolve().parents[3]
    reb = root / "rebuild_2026_10_22"
    args.output.mkdir(parents=True, exist_ok=True)
    inputs = {
        "A2": reb / "X48_native_cf_zoom/x48_analyze_results_ng48_A2.json",
        "measure": reb / "X48_native_cf_zoom/x48_analyze.py",
        "NL1": reb / "NL1_native_level_L/nl1_native_level.py",
        "CL2": reb / "CL2_native_cf_slope/cl2_native_slope_results.json",
        "CL3": reb / "CL3_one_number/cl3_one_number_results.json",
        "CL3_source": reb / "CL3_one_number/cl3_one_number.py",
        "LEE1_source": reb / "LEE1_look_elsewhere/lee1.py",
        "X43": reb / "X43_collapse_core_floor/x43_collapse_core_results.json",
        "equations": reb / "THEORY_EQUATIONS_2026-10-28.md",
        "F3": reb / "F3_growth_audit/f3_growth_audit_results.json",
    }
    sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
    hashes = {str(p.relative_to(root)): sha(p) for p in inputs.values()}
    a2 = json.loads(inputs["A2"].read_text())
    cl2 = json.loads(inputs["CL2"].read_text())
    cl3 = json.loads(inputs["CL3"].read_text())
    x43 = json.loads(inputs["X43"].read_text())
    result = {"mutate": args.mutate, "input_sha256": hashes, "checks": {}}

    def check(k, ok, detail):
        result["checks"][k] = {"pass": bool(ok), "detail": detail}
        print(k, "PASS" if ok else "FAIL", json.dumps(detail, sort_keys=True))

    rng = np.random.default_rng(20261028)
    medians = {}
    boot = {}
    for mass in (1e12, 1e13, 1e14):
        key = f"{mass:.0e}"
        rows = [r for r in a2["runs"].values()
                if r.get("flag") == "ok" and r.get("ng") == 48 and r.get("M") == mass]
        values = np.array([r["cf"] for r in rows])
        med = float(np.median(values))
        medians[key] = med
        b = [float(np.median(rng.choice(values, len(values)))) for _ in range(2000)]
        lo, hi = [float(v) for v in np.percentile(b, [16, 84])]
        boot[key] = {"n": len(rows), "seeds": sorted(r["seed"] for r in rows),
                     "median": med, "boot68": [lo, hi],
                     "nfw_median_reported": float(np.median([r["c_nfw_fit"] for r in rows]))}
    ref = {k: v * (1.1 if args.mutate and k == "1e+12" else 1) for k, v in a2["cf_by_mass"].items()}
    check("K1_cached_medians", all(len(boot[k]["seeds"]) == 9 and abs(medians[k] - ref[k]) < 1e-12 for k in medians),
          {"computed": medians, "cached_reference": ref})
    result["ng48_reference_bootstrap"] = {"generator": "numpy PCG64", "seed": 20261028,
        "n_resamples": 2000, "order": ["1e+12", "1e+13", "1e+14"], "masses": boot,
        "denominator_only_L_multiplier68": [11.63 / boot["1e+12"]["boot68"][1],
                                             11.63 / boot["1e+12"]["boot68"][0]],
        "interpretation": "Diagnostic only: conditional inverse of the reference median bootstrap endpoints; not a confidence interval for unobserved ng64 convergence."}

    # Documented NL1/X48 benchmark, compiled without import bytecode writes.
    xa = {"__file__": str(inputs["measure"]), "__name__": "x48_measure_readonly"}
    exec(compile(inputs["measure"].read_text(), str(inputs["measure"]), "exec"), xa)
    n = 12000
    x = xa["synthetic_nfw"](4.0, n, 1)
    syn = xa["measure"](x, 1 / n, 1 / (4 / 3 * math.pi) / (18 * math.pi ** 2), 1e-4)
    check("K2_documented_synthetic", syn.get("flag") == "ok" and abs(syn["cf"] / 4 - 1) < .15, syn)

    # Evaluate only the documented scalar interpolation, never top-level NL1.
    ns = {"round": round}
    tree = ast.parse(inputs["NL1"].read_text())
    fun = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "cl3_T")
    exec(compile(ast.Module(body=[fun], type_ignores=[]), "nl1_scalar_only", "exec"), ns)
    roots = []
    shape = [medians[k] for k in ("1e+12", "1e+13", "1e+14")]
    b1 = 3 * math.log(2) - math.pi / 2
    eta = lambda c: 4 / (3 * b1) * c ** 1.25
    for lev in (3.75, 3.9, 4.0):
        for foot in ("canonical", "alt"):
            exact_cached = cl3["T"][str(lev)][foot]
            interpolated = ns["cl3_T"](lev)
            cf_at_t = lev * float(np.interp(exact_cached, [12., 13., 14.], shape)) / shape[2]
            roots.append({"L": lev, "footing": foot, "CL3_cached_logT": exact_cached,
                "NL1_cl3_T": interpolated, "NL1_minus_CL3_dex": interpolated - exact_cached,
                "S9_cf_at_cached_T": cf_at_t, "S9_eta_over_eta_L": eta(cf_at_t) / eta(lev)})
    result["crossover_audit"] = roots
    result["eta_mass_scaling"] = {str(int(lm)): (cf / shape[2]) ** 1.25
                                  for lm, cf in zip((12., 13., 14.), shape)}
    check("K3_crossover_records", all(np.isfinite(r["CL3_cached_logT"]) for r in roots) and len(roots) == 6,
          {"max_canonical_interpolation_error_dex": max(abs(r["NL1_minus_CL3_dex"]) for r in roots if r["footing"] == "canonical"),
           "min_alt_threshold_error_dex": min(abs(r["NL1_minus_CL3_dex"]) for r in roots if r["footing"] == "alt")})

    g = 6.67430e-11
    pc = 3.0856775814913673e16
    ms = 1.98847e30
    sig = x43["sigma_coll_table"]["1e12"][0]
    branch = []
    for lev in (3.75, 3.9, 4.):
        cf = lev * shape[0] / shape[2]
        for foot, a0 in (("canonical", 9.3603e-11), ("alt", 1.1312e-10)):
            floor = a0 / (2 * math.pi * g) * pc ** 2 / ms
            branch.append({"L": lev, "footing": foot, "logM": 12., "floor_Msun_pc2": floor,
                "eta_L_sigma_over_floor": eta(lev) * sig / floor,
                "eta_S9_cf_sigma_over_floor": eta(cf) * sig / floor,
                "CL3_switch_halo": 12. > cl3["T"][str(lev)][foot]})
    result["branch_at_1e12"] = branch

    # Independent implementation of the specified CLASS/EPS scalar calculation.
    params = json.loads(inputs["F3"].read_text())["K2"]["A_c2b_refit"]["params"]
    cc = Class()
    class_params = {"omega_b": params["omega_b"], "omega_cdm": params["omega_cdm"],
        "h": params["h"], "ln10^{10}A_s": params["lnAs"], "n_s": params["n_s"],
        "tau_reio": params["tau"], "N_ur": 3.044, "output": "mPk",
        "P_k_max_h/Mpc": 200., "z_max_pk": 10.}
    cc.set(class_params)
    cc.compute()
    h = params["h"]
    rhom = float(cc.Omega_m()) * 2.775e11 * h ** 2
    k = np.logspace(-4., math.log10(150.), 3000)
    power = np.array([cc.pk_lin(float(v * h), 0.) for v in k]) * h ** 3
    lgmass = np.linspace(7., 16.5, 191)
    sigma2 = []
    for lm in lgmass:
        rad = (3 * 10 ** lm / (4 * math.pi * rhom)) ** (1 / 3) * h
        kr = k * rad
        window = 3 * (np.sin(kr) - kr * np.cos(kr)) / kr ** 3
        sigma2.append(float(np.trapz(k ** 3 * power * window ** 2 / (2 * math.pi ** 2), np.log(k))))
    z = np.linspace(0., 30., 3001)
    growth = np.array([cc.scale_independent_growth_factor(float(v)) for v in z])
    growth /= growth[0]

    def collapse_sigma(lm):
        s2half = float(np.interp(lm - math.log10(2), lgmass, sigma2))
        s2full = float(np.interp(lm, lgmass, sigma2))
        dform = 1.686 / (1.686 + .974 * math.sqrt(max(s2half - s2full, 0.)))
        zform = float(np.interp(-dform, -growth, z)) if dform < 1 else 0.
        rho = 18 * math.pi ** 2 * rhom * (1 + zform) ** 3
        rad = (3 * (10 ** lm / 2) / (4 * math.pi * rho)) ** (1 / 3)
        return rho * rad / 1e12

    fresh = []
    for lev in (3.75, 3.9, 4., 7.31):
        for foot, a0 in (("canonical", 9.3603e-11), ("alt", 1.1312e-10)):
            floor = a0 / (2 * math.pi * g) * pc ** 2 / ms
            values = {}
            for mode in ("constant_L", "S9_mass_dependent"):
                def residual(lm):
                    cf = lev if mode == "constant_L" else lev * float(np.interp(lm, [12., 13., 14.], shape)) / shape[2]
                    return math.log(eta(cf) * collapse_sigma(lm) / floor)
                grid = np.linspace(9., 16., 300)
                brackets = [(float(a), float(b)) for a, b in zip(grid[:-1], grid[1:])
                            if np.sign(residual(a)) != np.sign(residual(b))]
                values[mode] = {"logT": brentq(residual, *brackets[0], xtol=1e-7) if brackets else None,
                                "n_sign_change_brackets": len(brackets)}
            cached = cl3["T"].get(str(lev), {}).get(foot)
            fresh.append({"L": lev, "footing": foot, **values,
                "cached_constant_logT": cached,
                "fresh_minus_cached_dex": None if cached is None else values["constant_L"]["logT"] - cached,
                "NL1_linear_minus_fresh_dex": ns["cl3_T"](lev) - values["constant_L"]["logT"]})
    result["fresh_CLASS_EPS_roots"] = {"class_params": class_params, "rhom0_Msun_Mpc3": rhom,
        "scope": "Independent scalar implementation of CL3's discretized formulas; not validation of EPS physics.", "roots": fresh}
    check("K8_CLASS_EPS_scalar_reproduction", all(abs(r["fresh_minus_cached_dex"]) < .002 for r in fresh if r["cached_constant_logT"] is not None),
          {"max_fresh_minus_cached_dex": max(abs(r["fresh_minus_cached_dex"]) for r in fresh if r["cached_constant_logT"] is not None)})
    check("K9_unique_grid_crossings", all(r[m]["n_sign_change_brackets"] == 1 for r in fresh for m in ("constant_L", "S9_mass_dependent")),
          "One sign-change bracket per function on the fixed 300-point [9,16] grid; this does not prove global uniqueness.")
    cc.struct_cleanup()
    cc.empty()

    # Concrete cached counterexample to treating primary success as derived-T success.
    primary = cl2["S9_L4"]["grade"]["canonical"]
    derived = cl3["L4"]["grade"]["canonical"]
    example = {"L": 4., "primary_logT": 12.3, "primary_fails": primary["fails"],
               "CL3_logT": cl3["T"]["4.0"]["canonical"], "CL3_fails": derived["fails"],
               "CL3_lensing_dchi2": derived["lensing"]["d_LF_L"]}
    result["primary_vs_derived_T_counterexample"] = example
    check("K4_cached_implication_counterexample", not primary["fails"] and bool(derived["fails"]), example)
    source = inputs["NL1"].read_text()
    check("K5_verdict_source", 'G["PRIMARY"] = grade_cfg(12.3, Lnat' in source and
          'pc = G["PRIMARY"]["fails_canonical"]' in source and
          'G["CL3_T"] = grade_cfg(cl3_T(Lnat), Lnat' in source,
          "NL1 uses fixed T=12.3 for PRIMARY; success verdict reads PRIMARY only; canonical-derived T is a separate report.")
    lee = inputs["LEE1_source"].read_text()
    check("K6_formula_source", 'ETAF = (lambda M, tab=tab:' in lee and
          'float(np.interp(math.log10(M), [12.0, 13.0, 14.0], tab)) ** 1.25' in lee and
          'η(L) Σ_coll(M)' in inputs["equations"].read_text(),
          "LEE1/CL3 cores use eta of the mass-dependent S9 concentration; the equation page writes eta(L).")
    check("K7_stable_inputs", hashes == {str(p.relative_to(root)): sha(p) for p in inputs.values()}, "All declared scientific input hashes stable during execution.")
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1e9 if sys.platform == "darwin" else 1e6)
    check("K10_RSS", rss < 1., "Peak RSS below 1 GB; exact resource measurement is in runner stdout only.")
    print("RESOURCE peak_RSS_GB", rss)
    result["outcome"] = "Cached finite steps reproduced; primary-to-derived-T inference and equation-to-code equivalence fail. Native ng64 L remains pending."
    dest = args.output / "results.json"
    dest.write_text(json.dumps(result, indent=2, sort_keys=True, allow_nan=False) + "\n")
    passed = sum(v["pass"] for v in result["checks"].values())
    print(f"NATIVE_L_T COMPLETE: {passed}/{len(result['checks'])} checks PASS.")
    return 0 if passed == len(result["checks"]) else 1


if __name__ == "__main__":
    raise SystemExit(main())
