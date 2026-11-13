"""LGS2 collector: applies the frozen rules of FROZEN_CRITERIA.md to the outputs of lgs2_run.py. Reads JSON only.
kappa = 1/2 FITTED; not theory closed."""
import json
import os

import numpy as np
from scipy.interpolate import CubicSpline

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, "..", ".."))
X54C = os.path.join(REPO, "rebuild_2026_10_22", "X54_cold_de_exchange", "x54_cold_de_exchange_results.json")
RF5C = os.path.join(REPO, "rebuild_2026_10_22", "RF5_growth_native_yardstick", "rf5_results.json")
LGS1 = os.path.join(REPO, "closure_2026_11_13", "LGS1_legacy_sn_dropped", "lgs1_results.json")
FOOT = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
out = {"lane": "LGS2"}


def load(name):
    p = os.path.join(HERE, name)
    return json.load(open(p)) if os.path.exists(p) else None


def category(cls):
    for c in ("EXCHANGE PREFERRED (DE -> cold)", "EXCHANGE PREFERRED (cold -> DE)", "EXCHANGE ALLOWED", "EXCHANGE EXCLUDED BEYOND", "UNDECIDED"):
        if cls.startswith(c):
            return c
    return "?" + cls


def conv_points(prof):
    """converged grid points {xi: chi2_total} of one profile block (as X54's analyse(): converged points only)"""
    return {float(k): v["chi2"]["total"] for k, v in prof.items() if "chi2" in v and v.get("converged")}


def interval(pts, level):
    """X54's own spline construction (analyse()), at a chosen delta chi2 level: (xi_hat, lo, hi)"""
    xs = np.array(sorted(pts))
    cs = np.array([pts[x] for x in xs])
    fine = np.linspace(xs[0], xs[-1], 20001)
    cf = CubicSpline(xs, cs)(fine)
    i = int(np.argmin(cf))
    inside = cf - cf[i] <= level
    return float(fine[i]), float(fine[inside][0]), float(fine[inside][-1])


def checks_ok(r):
    return all(v["pass"] == (v["required"] == "PASS") for v in r["checks"].values()) and len(r["checks"]) == 7


# =============================================================== part A: X54
com = json.load(open(X54C))
runs = {s: load(f"lgs2_x54_{s}.json") for s in ("full", "des_only", "rand197")}
lgs1 = json.load(open(LGS1))
BAND_LGS1 = lgs1["B_cfg689"]["TD5F"]["z"]["2.33"]["des_only_68"]          # TD5F 68 % band at z 2.33 without the legacy set
TOL = {"C": {"chi2": 0.1, "xi": 1e-4}, "D": {"chi2": 0.1, "xi": 5e-3}}
A = {"band_lgs1_TD5F_des_only_2.33": BAND_LGS1}


def summ(r, key):
    an = r["analysis"][key]
    pts = conv_points(r["profiles"][key])
    x68 = interval(pts, 1.0)
    return {"class": an["class"], "category": category(an["class"]), "xi_hat": an["xi_hat"], "int95": an["int95"], "closed": an["closed"],
            "dchi2_xi0": an["dchi2_xi0"], "int68": [x68[1], x68[2]], "xi_hat_68calc": x68[0], "a0_grade": an["secondary"],
            "sqrtX_2.33_best": an["report"]["best"]["sqrtX_2.33"], "sqrtX_range_95": an["sqrtX_range_95"],
            "a0_2.33_best": an["report"]["best"]["a0_2.33"], "F_made": [an["report"][k]["F_made"] for k in ("best", "lo95", "hi95")],
            "S8": [an["report"][k]["S8"] for k in ("xi0", "best", "lo95", "hi95")], "H0_xi0": an["report"]["xi0"]["H0"],
            "Omega_m_xi0": an["report"]["xi0"]["Omega_m"], "chi2_xi0": pts.get(0.0), "points": pts,
            "cpl_best": [an["report"]["best"]["w"]["cpl_w0"], an["report"]["best"]["w"]["cpl_wa"]],
            "matched_band_grade": "CONSISTENT" if BAND_LGS1[0] <= an["report"]["best"]["sqrtX_2.33"] <= BAND_LGS1[1] else "TENSION"}


print("A. X54 (profile likelihood in the exchange xi; DES-SN5YR profiles; CMB + DESI DR2 BAO + SN)")
for s, r in runs.items():
    if r is None:
        print(f"   {s}: NOT RUN")
        continue
    A.setdefault("checks", {})[s] = {"all_required": checks_ok(r), "binaries": r.get("binaries"),
                                      "K2": r["checks"]["K2_xi0_equals_vanilla"]["value"], "S0-1": r["checks"]["S0-1_C7_LCDM_chi2"]["value"]}
    print(f"   {s}: Step 0 + K1-K4 all required outcomes: {checks_ok(r)}; K2 {r['checks']['K2_xi0_equals_vanilla']['value']}")
for key in ("C_DES5", "D_DES5"):
    m = key[0]
    Ak = {"committed": summ(com, key)}
    for s in ("full", "des_only", "rand197"):
        if runs[s] is not None and key in runs[s].get("analysis", {}) and checks_ok(runs[s]):   # a run failing Step 0 / K1-K4 is NOT EVALUABLE
            Ak[s] = summ(runs[s], key)
    # harness check: full vs committed
    if "full" not in Ak:
        Ak["harness"] = "NOT RUN"
    else:
        f, c = Ak["full"], Ak["committed"]
        same_pts = sorted(f["points"]) == sorted(c["points"])
        dchi = max(abs(f["points"][x] - c["points"][x]) for x in c["points"]) if same_pts else float("inf")
        dxi = max(abs(f["xi_hat"] - c["xi_hat"]), abs(f["int95"][0] - c["int95"][0]), abs(f["int95"][1] - c["int95"][1]))
        dd0 = abs(f["dchi2_xi0"] - c["dchi2_xi0"])
        ok = same_pts and dchi <= TOL[m]["chi2"] and dd0 <= TOL[m]["chi2"] and dxi <= TOL[m]["xi"] and checks_ok(runs["full"]) \
            and f["category"] == c["category"] and f["a0_grade"] == c["a0_grade"]
        Ak["harness"] = "PASS" if ok else "FAIL"
        Ak["harness_detail"] = {"same_converged_points": same_pts, "max_abs_dchi2_point": dchi, "abs_d_dchi2_xi0": dd0, "max_abs_dxi": dxi, "tol": TOL[m]}
    print(f"\n   [{key}] harness (full vs committed): {Ak['harness']}  {Ak.get('harness_detail', '')}")
    for s in ("committed", "full", "des_only", "rand197"):
        if s not in Ak:
            continue
        v = Ak[s]
        print(f"   {s:9s} xi_hat {v['xi_hat']:+.5f}  95% [{v['int95'][0]:+.5f}, {v['int95'][1]:+.5f}] (closed {v['closed']})  68% [{v['int68'][0]:+.5f}, {v['int68'][1]:+.5f}]"
              f"  dchi2(xi=0) {v['dchi2_xi0']:.3f}  class {v['category']}  sqrtX(2.33) {v['sqrtX_2.33_best']:.4f} -> a0 {v['a0_grade']}"
              f" (canonical {v['a0_2.33_best']['canonical']:.4e}, alt {v['a0_2.33_best']['alt']:.4e} m/s^2)  matched-band {v['matched_band_grade']}")
    labs = {}
    if Ak.get("harness") == "PASS":
        c = Ak["committed"]
        for s in ("des_only", "rand197"):
            if s not in Ak:
                continue
            d = Ak[s]
            L = {"L1_class": "UNCHANGED" if d["category"] == c["category"] else "CHANGED",
                 "L1_a0": {f: ("UNCHANGED" if d["a0_grade"] == c["a0_grade"] else "CHANGED") for f in FOOT},
                 "L2_95": "STABLE" if (c["int95"][0] <= d["xi_hat"] <= c["int95"][1] and d["int95"][0] <= c["xi_hat"] <= d["int95"][1]) else "SHIFTED",
                 "L2_68": "STABLE" if (c["int68"][0] <= d["xi_hat"] <= c["int68"][1] and d["int68"][0] <= c["xi_hat"] <= d["int68"][1]) else "SHIFTED",
                 "matched_band_grade": d["matched_band_grade"],
                 "shift_xi_hat": d["xi_hat"] - c["xi_hat"], "shift_lo95": d["int95"][0] - c["int95"][0], "shift_hi95": d["int95"][1] - c["int95"][1]}
            labs[s] = L
            print(f"   {s} vs committed: L1 class {L['L1_class']} ({c['category']} -> {d['category']}); L1 a0 grade {L['L1_a0']}; "
                  f"L2 (95 %) {L['L2_95']}; L2 (68 %) {L['L2_68']}; xi_hat shift {L['shift_xi_hat']:+.5f}; a0 grade on LGS1's matched band {BAND_LGS1}: {L['matched_band_grade']}")
        if "des_only" in labs and "rand197" in labs:
            rd = {}
            for lab in ("L1_class", "L2_95", "L2_68"):
                a, b = labs["des_only"][lab], labs["rand197"][lab]
                bad = ("CHANGED", "SHIFTED")
                rd[lab] = ("from the legacy set" if (a in bad and b not in bad) else
                           "not attributable to the legacy set alone (the control changes too)" if (a in bad and b in bad) else
                           "no change in des_only" + (" (the control changes)" if b in bad else ""))
            labs["control_reading"] = rd
            print(f"   control reading: {rd}")
    elif "des_only" in Ak:
        labs["note"] = "harness not PASS: this part is NOT EVALUABLE; des_only numbers above are reported only"
        print("   NOT EVALUABLE (harness not PASS); des_only numbers above are reported only")
    Ak["labels"] = labs
    A[key] = Ak
out["A_x54"] = A

# =============================================================== part B: RF5
comR = json.load(open(RF5C))
rr = {s: load(f"lgs2_rf5_{s}.json") for s in ("full", "des_only")}
WIN = ["R1_1000000", "R1_300000", "R1_100000", "R1_50000", "R1_30000", "R1_20000"]
LOWC = ["R1_12000", "R1_7000"]
PARTS = ["plik", "lowTT", "lowEE", "Aprior", "bao", "sn"]
B = {}
print("\nB. RF5 (turn-on epoch z_on of the cold component; CMB + BAO + DES-SN5YR steer; shear and forest graded at each fit)")


def cellrow(R, n):
    return R["cells"].get(n, {})


if rr["full"] is None:
    B["harness"] = "NOT RUN"
else:
    F, C = rr["full"], comR
    det = {}
    ok = True
    for n in WIN:
        a, b = cellrow(F, n), cellrow(C, n)
        if a.get("status") != "OK" or b.get("status") != "OK":
            ok = False
            det[n] = "status differs or not OK"
            continue
        d = {k: abs(a[k] - b[k]) for k in PARTS}
        d["shear"] = abs(a["shear"]["chi2"] - b["shear"]["chi2"]) if ("shear" in a and "shear" in b) else float("inf")
        d["S_minus_Smin"] = abs(a.get("S_minus_Smin", np.inf) - b["S_minus_Smin"])
        det[n] = d
        ok &= max(d.values()) <= 0.2
    for n in LOWC:
        a, b = cellrow(F, n), cellrow(C, n)
        same = a.get("status") == b.get("status") == "OK" and a.get("gates") == b.get("gates") and abs(a["plik"] / b["plik"] - 1) <= 0.01
        det[n] = {"same_gates_and_plik_1pc": same, "plik": [a.get("plik"), b.get("plik")]}
        ok &= same
    kh_same = F["verdict_khronon"] == C["verdict_khronon"]
    det["khronon_labels_same"] = kh_same
    ok &= kh_same
    cutF = load(os.path.join("rf5_cells_full", "shear_scale_cut.json"))
    cutC = json.load(open(os.path.join(os.path.dirname(RF5C), "cells", "shear_scale_cut.json")))
    det["shear_cut_same"] = bool(cutF and cutF["keep"] == cutC["keep"])
    ok &= det["shear_cut_same"]
    gF, gC = F.get("G0_forest") or {}, C["G0_forest"]
    fo = cellrow(F, "R1_1000000").get("forest", {})
    det["forest_1e6"] = {"full": fo.get("chi2"), "committed": cellrow(C, "R1_1000000")["forest"]["chi2"]}
    fok = fo.get("chi2") is not None and abs(fo["chi2"] - det["forest_1e6"]["committed"]) <= 2.0 and gF.get("pass") == gC["pass"]
    det["forest_harness"] = "PASS" if fok else "FAIL"
    det["checks"] = {k: v.get("pass") for k, v in F.get("checks", {}).items() if isinstance(v, dict)}
    ok &= bool(det["checks"]) and all(v for k, v in det["checks"].items() if k != "K6_profile" and v is not None)
    B["harness"] = "PASS" if ok else "FAIL"
    B["harness_detail"] = det
print(f"   harness (full vs committed): {B['harness']}")
if "harness_detail" in B:
    for k, v in B["harness_detail"].items():
        print(f"     {k}: {v}")


def rf5_table(R, lab):
    print(f"   {lab}: verdict {R['verdict']['canonical']}")
    print(f"     S_min {R['S_min']:.3f}; window {R['window_grid']}; abs-gates-only edge {R['window_abs_only']}; forest G0 {R.get('G0_forest')}; khronon {R['verdict_khronon']}")
    for n in WIN + LOWC:
        w = cellrow(R, n)
        if w.get("status") != "OK":
            print(f"     {n:11s} {w.get('status')}")
            continue
        sh = w.get("shear", {})
        print(f"     {n:11s} plik {w['plik']:8.2f} bao {w['bao']:6.2f} sn {w['sn']:8.2f}/{w['n_sn']} (p {w['p_sn']:.3f}) shear {sh.get('chi2', float('nan')):7.2f}"
              f" S-Smin {w.get('S_minus_Smin', float('nan')):8.2f} w0 {w['params']['w0']:+.3f} wa {w['params']['wa']:+.3f} Om {w['Omega_m']:.4f} h {w['h']:.4f}"
              f" s8 {w['sigma8']:.4f} sqrtX(2.33) {w['sqrtX'].get('2.33', float('nan')):.3f} forest {w.get('forest', {}).get('chi2', float('nan')):.1f}"
              f" gates {'Y' if w.get('window_pass') else ('a' if w.get('abs_pass') else 'n')}")


rf5_table(comR, "committed")
for s in ("full", "des_only"):
    if rr[s] is not None:
        rf5_table(rr[s], s)
    else:
        print(f"   {s}: NOT RUN")
if rr["des_only"] is not None:
    D, C = rr["des_only"], comR
    L = {}
    L["L1"] = {f: ("UNCHANGED" if (D["verdict"][f] == C["verdict"][f] and D["verdict_khronon"] == C["verdict_khronon"]) else "CHANGED") for f in ("canonical", "alt")}
    sh = {}
    for n in WIN + LOWC:
        a, b = cellrow(D, n), cellrow(C, n)
        if "S_minus_Smin" in a and "S_minus_Smin" in b:
            sh[n] = a["S_minus_Smin"] - b["S_minus_Smin"]
    L["dS_minus_Smin"] = sh
    need = {n for n in WIN + LOWC if "S_minus_Smin" in cellrow(C, n)}
    if set(sh) != need:
        L["L2"] = f"NOT EVALUABLE (des_only S missing at {sorted(need - set(sh))})"
    else:
        L["L2"] = "STABLE" if all(abs(v) <= 1.0 for v in sh.values()) else "SHIFTED"
    L["L2_cells_beyond_1"] = [n for n, v in sh.items() if abs(v) > 1.0]
    L["edge_margin_3e4"] = {"committed": 25 - cellrow(C, "R1_30000")["S_minus_Smin"], "des_only": 25 - cellrow(D, "R1_30000").get("S_minus_Smin", np.nan)}
    L["forest_G0"] = {"committed": C["G0_forest"], "des_only": D.get("G0_forest")}
    if B.get("harness") != "PASS":
        L["note"] = "harness not PASS: labels are NOT EVALUABLE; reported only"
    B["labels"] = L
    print(f"   des_only vs committed: L1 {L['L1']}; L2 {L['L2']} (|d(S - S_min)| <= 1.0 at every graded cell; beyond: {L['L2_cells_beyond_1']})"
          + ("" if B.get("harness") == "PASS" else "  [NOT EVALUABLE: harness not PASS]"))
    print(f"     d(S - S_min) per cell: { {k: round(v, 3) for k, v in sh.items()} }; margin to the 25 line at 3e4: {L['edge_margin_3e4']}")
out["B_rf5"] = B
json.dump(out, open(os.path.join(HERE, "lgs2_results.json"), "w"), indent=1, default=float)
print("\nwrote lgs2_results.json\nkappa = 1/2 FITTED; not theory closed.")
