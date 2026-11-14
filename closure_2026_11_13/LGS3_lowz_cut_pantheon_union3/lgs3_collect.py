"""LGS3 collector: applies the frozen rules of FROZEN_CRITERIA.md to the outputs of lgs3_run.py. Reads JSON only.
kappa = 1/2 FITTED; not theory closed."""
import json
import os

import numpy as np
from scipy.interpolate import CubicSpline

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, "..", ".."))
X54C = os.path.join(REPO, "rebuild_2026_10_22", "X54_cold_de_exchange", "x54_cold_de_exchange_results.json")
C689 = os.path.join(REPO, "campaign_fresh_gravity", "CFG689_native_ruler_bao")
FOOT = ("canonical", "alt")
SAMPLES = {"PP": ("full", "zcut", "legacy_surveys", "rand"), "U3": ("full", "zcut", "node055")}
CONTROL = {"PP": "rand", "U3": "node055"}
TOL = {"C": {"chi2": 0.1, "xi": 1e-4}, "D": {"chi2": 0.1, "xi": 5e-3}}
ZS = ["1.0", "1.2", "1.5", "2.33"]
out = {"lane": "LGS3"}


def load(name):
    p = os.path.join(HERE, name)
    return json.load(open(p)) if os.path.exists(p) else None


def category(cls):
    for c in ("EXCHANGE PREFERRED (DE -> cold)", "EXCHANGE PREFERRED (cold -> DE)", "EXCHANGE ALLOWED", "EXCHANGE EXCLUDED BEYOND", "UNDECIDED"):
        if cls.startswith(c):
            return c
    return "?" + cls


def conv_points(prof):
    return {float(k): v["chi2"]["total"] for k, v in prof.items() if "chi2" in v and v.get("converged")}


def interval(pts, level):
    xs = np.array(sorted(pts))
    cs = np.array([pts[x] for x in xs])
    fine = np.linspace(xs[0], xs[-1], 20001)
    cf = CubicSpline(xs, cs)(fine)
    i = int(np.argmin(cf))
    inside = cf - cf[i] <= level
    return float(fine[i]), float(fine[inside][0]), float(fine[inside][-1])


def checks_ok(r):
    return all(v["pass"] == (v["required"] == "PASS") for v in r["checks"].values()) and len(r["checks"]) == 7


def summ(r, key):
    an = r["analysis"][key]
    pts = conv_points(r["profiles"][key])
    x68 = interval(pts, 1.0)
    return {"class": an["class"], "category": category(an["class"]), "xi_hat": an["xi_hat"], "int95": an["int95"], "closed": an["closed"],
            "dchi2_xi0": an["dchi2_xi0"], "int68": [x68[1], x68[2]], "a0_grade": an["secondary"], "band": an["band_flat_theta"],
            "sqrtX_2.33_best": an["report"]["best"]["sqrtX_2.33"], "sqrtX_range_95": an["sqrtX_range_95"], "reaches_0909": an["reaches_0909"],
            "a0_2.33_best": an["report"]["best"]["a0_2.33"], "F_made": [an["report"][k]["F_made"] for k in ("best", "lo95", "hi95")],
            "S8": [an["report"][k]["S8"] for k in ("xi0", "best", "lo95", "hi95")], "H0_xi0": an["report"]["xi0"]["H0"],
            "Omega_m_xi0": an["report"]["xi0"]["Omega_m"], "chi2_xi0": pts.get(0.0), "points": pts,
            "cpl_best": [an["report"]["best"]["w"]["cpl_w0"], an["report"]["best"]["w"]["cpl_wa"]]}


# =============================================================== part A: X54, Pantheon+ and Union3 profiles
com = json.load(open(X54C))
A = {}
print("A. X54 (profile likelihood in the exchange xi; CMB + DESI DR2 BAO + Pantheon+ or Union3)")
for comp in ("PP", "U3"):
    runs = {s: load(f"lgs3_x54_{comp}_{s}.json") for s in SAMPLES[comp]}
    Ac = {"checks": {}}
    for s, r in runs.items():
        if r is None:
            print(f"   {comp} {s}: NOT RUN")
            continue
        Ac["checks"][s] = checks_ok(r)
        print(f"   {comp} {s}: Step 0 + K1-K4 all required outcomes: {checks_ok(r)}")
    for m in ("C", "D"):
        key = f"{m}_{comp}"
        Ak = {"committed": summ(com, key)}
        for s, r in runs.items():
            if r is not None and key in r.get("analysis", {}) and checks_ok(r):     # a run failing Step 0 / K1-K4 is NOT EVALUABLE
                Ak[s] = summ(r, key)
        if "full" not in Ak:
            Ak["harness"] = "NOT RUN"
        else:
            f, c = Ak["full"], Ak["committed"]
            same = sorted(f["points"]) == sorted(c["points"])
            dchi = max(abs(f["points"][x] - c["points"][x]) for x in c["points"]) if same else float("inf")
            dxi = max(abs(f["xi_hat"] - c["xi_hat"]), abs(f["int95"][0] - c["int95"][0]), abs(f["int95"][1] - c["int95"][1]))
            dd0 = abs(f["dchi2_xi0"] - c["dchi2_xi0"])
            ok = same and dchi <= TOL[m]["chi2"] and dd0 <= TOL[m]["chi2"] and dxi <= TOL[m]["xi"] and f["category"] == c["category"] \
                and f["a0_grade"] == c["a0_grade"]
            Ak["harness"] = "PASS" if ok else "FAIL"
            Ak["harness_detail"] = {"same_converged_points": same, "max_abs_dchi2_point": dchi, "abs_d_dchi2_xi0": dd0, "max_abs_dxi": dxi, "tol": TOL[m]}
        print(f"\n   [{key}] harness (full vs committed): {Ak['harness']}  {Ak.get('harness_detail', '')}")
        for s in ("committed",) + SAMPLES[comp]:
            if s not in Ak:
                continue
            v = Ak[s]
            print(f"   {s:15s} xi_hat {v['xi_hat']:+.5f}  95% [{v['int95'][0]:+.5f}, {v['int95'][1]:+.5f}] (closed {v['closed']})  68% [{v['int68'][0]:+.5f}, {v['int68'][1]:+.5f}]"
                  f"  dchi2(xi=0) {v['dchi2_xi0']:.3f}  class {v['category']}  sqrtX(2.33) {v['sqrtX_2.33_best']:.4f} vs {v['band']} -> a0 {v['a0_grade']}"
                  f" (canonical {v['a0_2.33_best']['canonical']:.4e}, alt {v['a0_2.33_best']['alt']:.4e} m/s^2)")
        labs = {}
        if Ak.get("harness") == "PASS":
            c = Ak["committed"]
            for s in SAMPLES[comp][1:]:
                if s not in Ak:
                    continue
                d = Ak[s]
                L = {"L1_class": "UNCHANGED" if d["category"] == c["category"] else "CHANGED",
                     "L1_a0": {f: ("UNCHANGED" if d["a0_grade"] == c["a0_grade"] else "CHANGED") for f in FOOT},
                     "L2_95": "STABLE" if (c["int95"][0] <= d["xi_hat"] <= c["int95"][1] and d["int95"][0] <= c["xi_hat"] <= d["int95"][1]) else "SHIFTED",
                     "L2_68": "STABLE" if (c["int68"][0] <= d["xi_hat"] <= c["int68"][1] and d["int68"][0] <= c["xi_hat"] <= d["int68"][1]) else "SHIFTED",
                     "shift_xi_hat": d["xi_hat"] - c["xi_hat"]}
                labs[s] = L
                print(f"   {s} vs committed: L1 class {L['L1_class']} ({c['category']} -> {d['category']}); L1 a0 {L['L1_a0']}; "
                      f"L2 (95 %) {L['L2_95']}; L2 (68 %) {L['L2_68']}; xi_hat shift {L['shift_xi_hat']:+.5f}")
            ctl = CONTROL[comp]
            if "zcut" in labs and ctl in labs:
                rd = {}
                for lab in ("L1_class", "L2_95", "L2_68"):
                    a, b = labs["zcut"][lab], labs[ctl][lab]
                    bad = ("CHANGED", "SHIFTED")
                    rd[lab] = ("from the low-redshift cut" if (a in bad and b not in bad) else
                               "not attributable to the low-redshift cut alone (the control changes too)" if (a in bad and b in bad) else
                               "no change for zcut" + (" (the control changes)" if b in bad else ""))
                labs["control_reading"] = rd
                print(f"   control reading (zcut against {ctl}): {rd}")
        elif any(s in Ak for s in SAMPLES[comp][1:]):
            labs["note"] = "harness not PASS: NOT EVALUABLE; numbers above reported only"
            print("   NOT EVALUABLE (harness not PASS); numbers above are reported only")
        Ak["labels"] = labs
        Ac[key] = Ak
    # the frozen LEAN reading (M-D's delta chi2 at xi = 0)
    D = Ac["D_" + comp]
    ctl = CONTROL[comp]
    if D.get("harness") != "PASS" or "zcut" not in D or ctl not in D:
        lean = "NOT EVALUABLE (" + ("harness " + str(D.get("harness")) if D.get("harness") != "PASS" else "zcut or control missing") + ")"
    else:
        z_, c_ = D["zcut"]["dchi2_xi0"], D[ctl]["dchi2_xi0"]
        lean = "LEAN NOT FROM LOW-Z" if z_ >= 1.0 else ("LEAN FROM LOW-Z" if c_ >= 1.0 else "UNDECIDED")
    Ac["LEAN"] = {"reading": lean, "dchi2_xi0": {s: D[s]["dchi2_xi0"] for s in ("committed",) + SAMPLES[comp] if s in D}}
    print(f"\n   LEAN reading, {comp}: {lean}; M-D dchi2(xi=0): { {k: round(v, 3) for k, v in Ac['LEAN']['dchi2_xi0'].items()} }\n")
    A[comp] = Ac
out["A_x54"] = A

# =============================================================== part B (optional): CFG689 TF and TU3F
B = {}
print("B. CFG689 flat + acoustic-angle modes (TF: Pantheon+, TU3F: Union3), full vs zcut")
for mode in ("TF", "TU3F"):
    ref = json.load(open(os.path.join(C689, f"cfg689_{mode}.json")))["BAO+SN"]
    r = {s: load(f"lgs3_cfg689_{mode}_{s}.json") for s in ("full", "zcut")}
    Bm = {}
    full = r["full"]["BAO+SN"] if r["full"] else None
    if full is None:
        Bm["harness"] = "NOT RUN"
    else:
        d = max(float(np.max(np.abs(np.array(full["P1"][z]["sqrtX_q"]) - np.array(ref["P1"][z]["sqrtX_q"])))) for z in ZS)
        Bm["harness_max_abs_diff"] = d
        Bm["harness"] = "PASS" if d <= 0.005 else "FAIL"
    print(f"   {mode} harness (full vs committed): {Bm['harness']}" + (f"  max |diff| in sqrtX quantiles {Bm['harness_max_abs_diff']:.2e}" if "harness_max_abs_diff" in Bm else ""))
    zc = r["zcut"]["BAO+SN"] if r["zcut"] else None
    if zc is None:
        print(f"   {mode} zcut: NOT RUN")
    else:
        Bm["K4_ok"] = zc["K4"]["ok"]
        Bm["P1_class"] = dict(committed=ref["P1_class"], zcut=zc["P1_class"])
        Bm["P0_class"] = dict(committed=(ref["P0"] or {}).get("P0_class"), zcut=(zc["P0"] or {}).get("P0_class"))
        Bm["P2"] = dict(committed=dict(dchi2=ref["P2"]["dchi2"], sigma=ref["P2"]["sigma_equiv"], cls=ref["P2"].get("P2_class")),
                        zcut=dict(dchi2=zc["P2"]["dchi2"], sigma=zc["P2"]["sigma_equiv"], cls=zc["P2"].get("P2_class")))
        Bm["z"] = {}
        for z in ZS:
            qa, qb = np.array(ref["P1"][z]["sqrtX_q"]), np.array(zc["P1"][z]["sqrtX_q"])
            st = (qa[1] <= qb[2] <= qa[3]) and (qb[1] <= qa[2] <= qb[3])
            Bm["z"][z] = dict(committed_68=[qa[1], qa[3]], committed_median=qa[2], zcut_68=[qb[1], qb[3]], zcut_median=qb[2], B1="STABLE" if st else "SHIFTED")
            print(f"   {mode} z*={z}: tracking sqrtX 68% committed [{qa[1]:.3f}, {qa[3]:.3f}] med {qa[2]:.3f} | zcut [{qb[1]:.3f}, {qb[3]:.3f}] med {qb[2]:.3f} -> B1 {Bm['z'][z]['B1']}")
        Bm["B2"] = "CLASS UNCHANGED" if (Bm["P1_class"]["committed"] == Bm["P1_class"]["zcut"] and Bm["P0_class"]["committed"] == Bm["P0_class"]["zcut"]) else "CLASS CHANGED"
        Bm["B3"] = "P2 UNCHANGED" if Bm["P2"]["committed"]["cls"] == Bm["P2"]["zcut"]["cls"] else "P2 CHANGED"
        print(f"   {mode}: P1 {Bm['P1_class']} -> B2 {Bm['B2']};  P2 {Bm['P2']} -> B3 {Bm['B3']};  K4 ok {Bm['K4_ok']}")
        if Bm["harness"] != "PASS" or not Bm["K4_ok"]:
            Bm["note"] = "harness not PASS or K4 failed: NOT EVALUABLE; reported only"
            print(f"   {mode}: NOT EVALUABLE (harness {Bm['harness']}, K4 {Bm['K4_ok']}); reported only")
    B[mode] = Bm
out["B_cfg689"] = B
json.dump(out, open(os.path.join(HERE, "lgs3_results.json"), "w"), indent=1, default=float)
print("\nwrote lgs3_results.json\nkappa = 1/2 FITTED; not theory closed.")
