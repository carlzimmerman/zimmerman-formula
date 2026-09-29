#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CFG167 referee re-derivation of CFG161 (KURVS - KROSS differential under P4), frozen criteria CFG167_FROZEN_CRITERIA.md.
Main:    ZF_REPO=<repo> python3 CFG167_referee_diff_p4.py            -> CFG167_main.out / CFG167_main_results.json  (rc 0; rc 2 if a control fails; rc 1 if H1 fails)
MUTATE:  MUTATE=k python3 CFG167_referee_diff_p4.py   (k = 1..5)    -> rc 1 = the control BITES (H1 fails or class != main class), rc 0 = does not bite
Imports (shared, NOT independent): CFG165_referee_kurvs_p4 as M (loaders, per_object, pool, anchor_pool, cell, SP, alpha_K, E_of_z, nu_mono via CFG4_common).
Written fresh: D, sigma_D, D_H, the 4-class rule, R0-R3, controls, MUTATEs."""
import os
import sys
import json
import math
sys.dont_write_bytecode = True
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "2")
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))


def _find_repo():
    r = os.environ.get("ZF_REPO")
    if r and os.path.isdir(os.path.join(r, "data_assembly")):
        return r
    d = HERE
    for _ in range(8):
        if os.path.isdir(os.path.join(d, "data_assembly")) and os.path.isdir(os.path.join(d, "campaign_fresh_gravity")):
            return d
        d = os.path.dirname(d)
    raise SystemExit("set ZF_REPO")


REPO = _find_repo()
os.environ["ZF_REPO"] = REPO
sys.path.insert(0, os.path.join(REPO, "campaign_fresh_gravity", "CFG165_kurvs_referee"))
_mut = os.environ.pop("MUTATE", None)
import CFG165_referee_kurvs_p4 as M   # noqa: E402  (read-only shared element)
if _mut is not None:
    os.environ["MUTATE"] = _mut
MODE = _mut if _mut is not None else "0"

LN10 = math.log(10.0)
P4 = M.SP["P4"]
FOOT = "canonical"
MU = 0.67


def copy_sample(S):
    import copy
    return copy.deepcopy(S)


def pooled(S, sp, mu, delta=0.0):
    po = M.per_object(S, sp, mu, delta, FOOT)
    f = M.pool(po["d_flat"], po["e_flat"])
    h = M.pool(po["d_H"], po["e_H"])
    return dict(f=f[0], fe=f[1], h=h[0], he=h[1], po=po)


def diff(SK, SR, spK, spR, muK=MU, muR=MU, dK=0.0, dR=0.0):
    k = pooled(SK, spK, muK, dK)
    r = pooled(SR, spR, muR, dR)
    D = k["f"] - r["f"]
    sD = math.hypot(k["fe"], r["fe"])
    DH = (k["f"] - k["h"]) - (r["f"] - r["h"])
    return dict(D=D, sD=sD, DH=DH, zf=D / sD, zh=(D - DH) / sD, kf=k["f"], ke=k["fe"], kh=k["h"], rf=r["f"], re=r["fe"], rh=r["h"],
                kpo=k["po"], rpo=r["po"])


def classify_D(D, DH, sD, swap=False):
    """frozen CFG161 rule at 2 sigma_D. swap=True attaches the number D_H to the label 'flat' and 0 to 'rival' (M3)."""
    pf, ph = (DH, 0.0) if swap else (0.0, DH)
    nf, nh = abs(D - pf) <= 2 * sD, abs(D - ph) <= 2 * sD
    if nf and nh:
        return "consistent with both"
    if nf:
        return "lands on flat"
    if nh:
        return "lands on the rival"
    return "manufactures evolution"


def load_all(inc_col="inc_star_deg"):
    SK = M.load_kurvs(inc_col=inc_col)
    SR = M.load_kross()
    AS = M.load_sparc_anchor()
    return SK, SR, AS


def sigma0_variant(SK):
    S = copy_sample(SK)
    S.sig = S.sig0.copy()
    S.esig = S.esig0.copy()
    return S


TARGETS = {  # CFG161 README table, targets READ (not blind)
    "P0": (0.017, 0.058, 0.069, "consistent with both"), "P1": (0.273, 0.070, 0.078, "manufactures evolution"),
    "P2": (0.265, 0.065, 0.077, "manufactures evolution"), "P3": (0.218, 0.070, 0.074, "manufactures evolution"),
    "P4": (0.148, 0.044, 0.072, "lands on the rival"), "P4 a0.6": (0.110, 0.045, 0.071, "lands on the rival"),
    "P4 a1.4": (0.175, 0.046, 0.073, "manufactures evolution"), "P4 KU s0": (0.126, 0.050, 0.074, "lands on the rival"),
}


def rows(SK, SR):
    out = {}
    SP = M.SP
    out["P0"] = diff(SK, SR, SP["P0"], SP["P0"])
    out["P1"] = diff(SK, SR, SP["P1"], SP["P1"])
    out["P2"] = diff(SK, SR, SP["P2"], SP["P2"])
    out["P3"] = diff(SK, SR, SP["P3"], SP["P3"])
    out["P4"] = diff(SK, SR, P4, P4)
    s06, s14 = M.spec("P4", scale=0.6), M.spec("P4", scale=1.4)
    out["P4 a0.6"] = diff(SK, SR, s06, s06)
    out["P4 a1.4"] = diff(SK, SR, s14, s14)
    out["P4 KU s0"] = diff(sigma0_variant(SK), SR, P4, P4)
    out["P4 a0.6 KURVS-only"] = diff(SK, SR, s06, P4)          # option B, reported
    out["P4 a1.4 KURVS-only"] = diff(SK, SR, s14, P4)
    return out


def main():
    res = dict(mode=MODE, checks={}, numbers={})
    P = lambda *a: print(*a, flush=True)
    P("=" * 100)
    P(f"CFG167 referee re-derivation of CFG161.  MODE={MODE}  repo=<repo>  (inc column: inc_star_deg primary)")
    P("=" * 100)
    checks = []

    def check(name, ok, meas):
        checks.append((name, bool(ok)))
        res["checks"][name] = dict(ok=bool(ok), measured=str(meas))
        P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {meas}")

    SK, SR, AS = load_all("inc_star_deg")
    SK_sfr = M.load_kurvs(inc_col="inc_sfr_deg")
    SK0, SR0 = copy_sample(SK), copy_sample(SR)          # unmutated copies for the controls
    spK, spR = P4, P4
    muK, muR = MU, MU
    swap = False
    note = ""
    if MODE == "1":
        SK.V = SK.V * 10 ** 0.3; SK.eV = SK.eV * 10 ** 0.3; note = "KURVS v_last x 10^0.3 (g_obs x ~4)"
    elif MODE == "2":
        spR = M.spec("alpha", fn=lambda S_, a: 0.0 * S_.V); note = "KROSS pressure correction removed (alpha = 0 for KROSS only)"
    elif MODE == "3":
        swap = True; note = "verdict labels swapped (D_H attached to 'flat', 0 to 'rival')"
    elif MODE == "4":
        muK = 4.0; note = "KURVS gas mu = 4, KROSS mu = 0.67"
    elif MODE == "5":
        rng = np.random.default_rng(167)
        p = rng.permutation(len(SK.sig))
        SK.sig, SK.esig, SK.grad2 = SK.sig[p], SK.esig[p], SK.grad2[p]; note = "KURVS sigma_out permuted across galaxies (seed 167)"
    if note:
        P("MUTATION:", note)

    # ---------------- controls (always on the unmutated samples)
    P("\n-- controls")
    check("C3 alpha(0)=1.475, alpha(1)=2.533, alpha(4)=3.955", abs(M.alpha_K(0) - 1.475) < 1e-9 and abs(M.alpha_K(1) - 2.533) < 1e-9 and abs(M.alpha_K(4) - 3.955) < 1e-9,
          (float(M.alpha_K(0)), float(M.alpha_K(1)), float(M.alpha_K(4))))
    r1 = float(M.nu_mono(1e-12) * 1e-12 / math.sqrt(1e-12) - 1)
    r2 = float(M.nu_mono(1e12) - 1)
    check("C5 kernel limits < 1e-5", abs(r1) < 1e-5 and abs(r2) < 1e-5, (r1, r2))
    check("C4a sample sizes KURVS 10, KROSS 390", len(SK0.ids) == 10 and len(SR0.ids) == 390, (len(SK0.ids), len(SR0.ids)))
    P(f"      median z: KURVS {np.median(SK0.z):.3f}, KROSS {np.median(SR0.z):.3f};  KROSS x = R/Reff-1 in [{(SR0.R/SR0.Reff-1).min():.3f},{(SR0.R/SR0.Reff-1).max():.3f}] alpha {float(M.alpha_K(1.0)):.3f}")
    R0 = rows(SK0, SR0)
    d0, d1 = R0["P0"], R0["P1"]
    check("C1 P0 differential +0.017+-0.058 (3-dec print)", abs(round(d0["D"], 3) - 0.017) <= 0.0015 and abs(round(d0["sD"], 3) - 0.058) <= 0.0015, f"{d0['D']:+.4f}+-{d0['sD']:.4f}")
    check("C1 P1 differential +0.273+-0.070 (3-dec print)", abs(round(d1["D"], 3) - 0.273) <= 0.0015 and abs(round(d1["sD"], 3) - 0.070) <= 0.0015, f"{d1['D']:+.4f}+-{d1['sD']:.4f}")
    c = M.cell(SK0, AS, P4, MU, 0.0, FOOT)
    check("C2 decision cell Dflat' +0.1441, DH' -0.0060 within 0.001", abs(c["flat"]["dprime"] - 0.1441) <= 0.001 and abs(c["H"]["dprime"] + 0.0060) <= 0.001,
          f"{c['flat']['dprime']:+.4f} {c['H']['dprime']:+.4f}")
    res["numbers"]["decision_cell"] = dict(flat=c["flat"]["dprime"], H=c["H"]["dprime"], sig_f=c["flat"]["sigma"], sig_h=c["H"]["sigma"])

    # ---------------- R0 power (before D)
    r = diff(SK, SR, spK, spR, muK, muR)
    P("\n-- R0 power (printed before D): sigma_D, D_H, |D_H|/sigma_D")
    ZK, ZR = np.median(SK0.z), np.median(SR0.z)
    deep = 0.5 * math.log10(float(M.E_of_z(ZK) / M.E_of_z(ZR)))
    P(f"   sigma_D = {r['sD']:.4f}   D_H (exact, pipeline) = {r['DH']:+.4f}   |D_H|/sigma_D = {abs(r['DH'])/r['sD']:.2f}   deep-regime 0.5*log10[E(z_K)/E(z_R)] = {deep:+.4f}")
    res["numbers"]["R0"] = dict(sigma_D=r["sD"], DH=r["DH"], ratio=abs(r["DH"]) / r["sD"], deep=deep)

    # ---------------- R1 table
    P("\n-- R1: D = Delta_flat(KURVS) - Delta_flat(KROSS), raw pooled, mu=0.67 both, canonical, delta=0  [README target in brackets]")
    if MODE == "0":
        R = R0
    else:
        R = None
    tab = {}
    if MODE == "0":
        for nm, x in R.items():
            cl = classify_D(x["D"], x["DH"], x["sD"])
            tab[nm] = dict(D=x["D"], sD=x["sD"], DH=x["DH"], zf=x["zf"], zh=x["zh"], cls=cl, kf=x["kf"], ke=x["ke"], rf=x["rf"], re=x["re"])
            t = TARGETS.get(nm)
            tg = f"  [+{t[0]:.3f} +-{t[1]:.3f}, D_H {t[2]:+.3f}, {t[3]}]" if t else ""
            P(f"   {nm:19s} D {x['D']:+.4f} +- {x['sD']:.4f}  D_H {x['DH']:+.4f}  z_flat {x['zf']:+.2f}  z_riv {x['zh']:+.2f}  -> {cl}{tg}")
        res["numbers"]["R1"] = tab
        # inc_sfr variant (CFG165 default column)
        Rs = rows(SK_sfr, SR0)
        res["numbers"]["R1_inc_sfr"] = {nm: dict(D=x["D"], sD=x["sD"], DH=x["DH"]) for nm, x in Rs.items()}
        P("   (inclination column variant inc_sfr_deg, reported):  " + "; ".join(f"{nm} {x['D']:+.3f}+-{x['sD']:.3f}" for nm, x in Rs.items() if nm in ("P0", "P1", "P2", "P3", "P4")))
        # pass lines
        P("\n-- pass lines vs README targets (section 4 of the frozen criteria)")
        ok3 = True
        okp5 = True
        edges = []
        for nm, t in TARGETS.items():
            x = tab[nm]
            a = abs(x["D"] - t[0]) <= 0.005 and abs(x["DH"] - t[2]) <= 0.005 and abs(x["sD"] - t[1]) <= 0.005
            ok3 &= a
            eq = x["cls"] == t[3]
            if not eq:
                # EDGE rule: P3 row |D-D_H|/sD within 2+-0.1; a1.4 row within 2+-0.25
                zz = abs(x["D"] - x["DH"]) / x["sD"]
                edge = (nm == "P3" and abs(zz - 2) <= 0.1) or (nm == "P4 a1.4" and abs(zz - 2) <= 0.25)
                if edge and a:
                    edges.append(nm)
                else:
                    okp5 = False
            P(f"   {nm:10s} numbers within 0.005: {'yes' if a else 'NO '}  (dD {x['D']-t[0]:+.4f}, dD_H {x['DH']-t[2]:+.4f}, dsig {x['sD']-t[1]:+.4f});  class {'= README' if eq else 'DIFFERS: mine ' + x['cls'] + ' vs README ' + t[3]}")
        P4r = tab["P4"]
        z_ok = abs(P4r["zf"] - 3.3) <= 0.10 and abs(P4r["zh"] - 1.7) <= 0.10
        check("P3 all 8 rows D, D_H, sigma_D within 0.005", ok3, "")
        check("P4 z vs flat / rival within 0.10 of 3.3 / 1.7", z_ok, f"{P4r['zf']:.2f} / {P4r['zh']:.2f}")
        check("P5 class labels (EDGE-DIFFERS allowed): " + (("edge rows: " + ",".join(edges)) if edges else "no edge"), okp5, "")
        check("P6 R0 sigma_D 0.044, D_H 0.072, ratio 1.6, deep +0.083", abs(r["sD"] - 0.044) <= 0.005 and abs(r["DH"] - 0.072) <= 0.005 and abs(abs(r["DH"]) / r["sD"] - 1.6) <= 0.1 and abs(deep - 0.083) <= 0.001,
              f"{r['sD']:.4f} {r['DH']:+.4f} {abs(r['DH'])/r['sD']:.2f} {deep:+.4f}")
    # ---------------- R3 absolute anchored levels
    P("\n-- R3: anchored absolute levels under P4 (mu=0.67, same anchor): [README targets: KURVS +0.144+-0.044 / -0.006; KROSS -0.004+-0.020 (-0.2s) / -0.082 (-4.1s)]")
    ap = M.anchor_pool(P4, 0.0, FOOT, AS)["flat"]
    kk = diff(SK, SR, spK, spR, muK, muR)
    k_sig = math.hypot(kk["ke"], ap[1]); r_sig = math.hypot(kk["re"], ap[1])
    R3 = dict(kurvs_f=kk["kf"] - ap[0], kurvs_h=kk["kh"] - ap[0], kurvs_sig=k_sig, kross_f=kk["rf"] - ap[0], kross_h=kk["rh"] - ap[0], kross_sig=r_sig, anchor=ap[0], anchor_err=ap[1])
    P(f"   anchor P4 = {ap[0]:+.4f} +- {ap[1]:.4f}")
    P(f"   KURVS: flat {R3['kurvs_f']:+.4f} +- {k_sig:.4f} ({R3['kurvs_f']/k_sig:+.2f}s)   rival {R3['kurvs_h']:+.4f} ({R3['kurvs_h']/k_sig:+.2f}s)")
    P(f"   KROSS: flat {R3['kross_f']:+.4f} +- {r_sig:.4f} ({R3['kross_f']/r_sig:+.2f}s)   rival {R3['kross_h']:+.4f} ({R3['kross_h']/r_sig:+.2f}s)")
    res["numbers"]["R3"] = R3
    if MODE == "0":
        check("P7 R3 within 0.005 (values), KROSS sigma within 0.003, z within 0.15",
              abs(R3["kurvs_f"] - 0.144) <= 0.005 and abs(R3["kurvs_h"] + 0.006) <= 0.005 and abs(R3["kross_f"] + 0.004) <= 0.005 and abs(R3["kross_h"] + 0.082) <= 0.005
              and abs(r_sig - 0.020) <= 0.003 and abs(R3["kross_f"] / r_sig + 0.2) <= 0.15 and abs(R3["kross_h"] / r_sig + 4.1) <= 0.15, "")

    # ---------------- decision
    cls = classify_D(kk["D"], kk["DH"], kk["sD"], swap=swap)
    P("\n-- DECISION (P4 primary)" + (f"  [MUTATED: {note}]" if MODE != "0" else ""))
    P(f"   D = {kk['D']:+.4f} +- {kk['sD']:.4f};  D_H = {kk['DH']:+.4f};  z_flat = {kk['zf']:+.2f}, z_rival = {kk['zh']:+.2f};  class = {cls}")
    within = (abs(kk["D"]) <= 2 * kk["sD"]) or (abs(kk["D"] - kk["DH"]) <= 2 * kk["sD"])
    h1 = within
    if swap:
        h1 = within   # label swap does not change the set of two predictions
    P(f"   H1 (D within 2 sigma_D of at least one prediction): {'PASS' if h1 else 'FAIL'}")
    bounds = dict(flat_lo=-2 * kk["sD"], flat_hi=2 * kk["sD"], rival_lo=kk["DH"] - 2 * kk["sD"], rival_hi=kk["DH"] + 2 * kk["sD"])
    P(f"   class map in D: consistent with both [{max(bounds['flat_lo'], bounds['rival_lo']):+.3f}, {min(bounds['flat_hi'], bounds['rival_hi']):+.3f}]; lands on rival ({bounds['flat_hi']:+.3f}, {bounds['rival_hi']:+.3f}]; "
      f"lands on flat [{bounds['flat_lo']:+.3f}, {bounds['rival_lo']:+.3f}); manufactures D > {bounds['rival_hi']:+.3f} or D < {bounds['flat_lo']:+.3f}. Observed distance to the manufactures edge: {bounds['rival_hi']-kk['D']:+.3f} ({(bounds['rival_hi']-kk['D'])/kk['sD']:.2f} sigma_D)")
    res["numbers"]["decision"] = dict(D=kk["D"], sD=kk["sD"], DH=kk["DH"], zf=kk["zf"], zh=kk["zh"], cls=cls, h1=bool(h1), bounds=bounds)
    outname = "CFG167_main" if MODE == "0" else f"CFG167_MUTATE_{MODE}"
    if MODE == "0":
        fails = [n for n, ok in checks if not ok]
        P(f"\n   controls/pass lines: {len(checks)-len(fails)}/{len(checks)} PASS" + (f"; FAIL: {fails}" if fails else ""))
        res["exit_reason"] = "controls" if fails else ("H1" if not h1 else "ok")
        rc = 2 if fails else (0 if h1 else 1)
    else:
        bite = (not h1) or (cls != "lands on the rival")
        P(f"\n   MUTATE bite = (H1 fails) or (class != 'lands on the rival') -> {'BITES' if bite else 'DOES NOT BITE'}")
        res["bite"] = bool(bite)
        rc = 1 if bite else 0
    res["rc"] = rc
    json.dump(res, open(os.path.join(HERE, outname + "_results.json"), "w"), indent=1, default=float)
    P(f"exit {rc}")
    return rc


if __name__ == "__main__":
    sys.exit(main())
