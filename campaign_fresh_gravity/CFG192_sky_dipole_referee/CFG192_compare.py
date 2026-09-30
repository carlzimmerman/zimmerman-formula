#!/usr/bin/env python3
"""CFG192_compare -- PHASE 2 ONLY.  Runs after CFG192's own main, MUTATE 1-7 and attacks A-E were saved.  Reads CFG182's
*_results.json (read-only) and diffs every README row against CFG192's numbers; also the shared-element cross-checks
(nu_mono against the repo's copy, positions against sparc_cosmicweb_match.csv, rotmod-header distances against the master
table).  Prints <repo>; exit 0.  Outputs CFG192_compare.out/.json."""
import os
import sys
import json
import numpy as np
from CFG192_common import *
import CFG192_common as CC

S182 = os.path.join(REPO, "campaign_fresh_gravity", "CFG182_a0_sky_dipole")


def J(name):
    with open(os.path.join(HERE, name)) as fh:
        return json.load(fh)


def J182(name):
    with open(os.path.join(S182, name)) as fh:
        return json.load(fh)["numbers"]


def main():
    R = Run("CFG192_compare")
    R.banner("CFG192 compare (phase 2): CFG192 vs CFG182's README rows   repo=<repo>")
    m = J("CFG192_main.json")["numbers"]["summary"]
    AB = J("CFG192_attacks_AB.json")["numbers"]["results"]
    CD = J("CFG192_attacks_CD.json")["numbers"]["results"]
    E = J("CFG192_attacks_E.json")["numbers"]["results"]
    b182 = J182("cfg182_b_dipole_results.json")
    bm182 = J182("cfg182_b_dipole_results_MUTATE.json")
    d = load_bundle(os.path.join(HERE, "CFG192_profiles.npz"))
    b = sub_bundle(d, d["mask"])
    cv, n, uma = b["cv"], b["n"], b["uma"]
    F0, la0 = F0_fit(cv)
    fit = fit_dipole(cv, n, starts=5)
    rows = []

    def row(name, mine, theirs, tol, cls, note=""):
        ok = abs(mine - theirs) <= tol
        rows.append(dict(name=name, mine=float(mine), theirs=float(theirs), tol=tol, ok=bool(ok), cls=("-" if ok else cls), note=note))
        R.P(f"  {'OK  ' if ok else 'DIFF'} {name:58s} mine {mine:10.4f}  CFG182 {theirs:10.4f}  |d| {abs(mine - theirs):.4f} (tol {tol})  {'' if ok else '[' + cls + ']'} {note}")
    p182 = b182["primary"]
    R.banner("0. shared-element cross-checks (independence stops here)")
    # (1) nu_mono against the repo copy
    sys.path.insert(0, os.path.join(REPO, "campaign_fresh_gravity"))
    import importlib
    C4 = importlib.import_module("CFG4_common")
    y = np.logspace(-8, 4, 2001)
    rel = float(np.max(np.abs(nu_mono(y) / C4.nu_mono(y) - 1)))
    R.check("nu_mono (own implementation from the FP1 definition) vs the repo's nu_mono: max relative difference < 1e-6", f"{rel:.2e}", rel < 1e-6)
    # (2) positions vs the cosmic-web match table
    import csv
    cw = {}
    with open(os.path.join(DATA, "sparc_cosmicweb_match.csv")) as fh:
        for r in csv.DictReader(fh):
            try:
                cw[r["name"]] = (float(r["l_gal"]), float(r["b_gal"]))
            except ValueError:
                pass
    G = load_all()
    dl = []
    for g in G:
        if g["name"] in cw:
            dl.append(ang(lb_to_vec(*g["lb"]), lb_to_vec(*cw[g["name"]])))
    R.check("positions: own (l, b) vs sparc_cosmicweb_match.csv, all resolved galaxies within 0.5 deg", f"{len(dl)} galaxies, max {max(dl):.3f} deg, median {np.median(dl):.4f} deg", max(dl) < 0.5)
    # (3) rotmod header distance vs master table
    bad = []
    for g in G:
        with open(os.path.join(DATA, "sparc_data", g["name"] + "_rotmod.dat")) as fh:
            for line in fh:
                if line.startswith("# Distance"):
                    dd = float(line.split("=")[1].split()[0])
                    if abs(dd - g["meta"]["D"]) > 0.01 * g["meta"]["D"] + 0.01:
                        bad.append((g["name"], dd, g["meta"]["D"]))
                    break
    R.check("rotmod-header distance = master-table D (1%)", f"{len(bad)} mismatches: {bad[:4]}", len(bad) == 0, load_bearing=False)
    R.banner("1. README rows (primary analysis)")
    row("clean-sample N", cv.N, 149, 0, "definition")
    row("points", int(b["N"].sum()), 3150, 0, "definition")
    row("a0bar no dipole (1e-10)", 10 ** la0 / 1e-10, p182["a0_bar_nodipole"] / 1e-10, 0.005, "numerical")
    row("Birge factor median", float(np.median(b["s"])), 1.72, 0.01, "numerical")
    hw, _ = curve_halfwidth(b["grid"], b["C"])
    row("median per-galaxy Delta chi2 = 1 half-width (dex)", float(np.median(hw)), 0.264, 0.01, "definition", "CFG182 averages the two sides of the first Delta chi2 = 1 crossing and caps at 1 dex; mine is (right - left)/2 with linear crossings")
    f = n.mean(0)
    row("|<n>|", float(np.linalg.norm(f)), 0.599, 0.002, "numerical")
    row("A-hat", fit["A"], p182["A"], 0.03, "numerical")
    l_, b_ = vec_to_lb(fit["D"])
    dang = ang(fit["D"], np.array(p182["D"]))
    row("direction angle apart (deg)", dang, 0.0, 15.0, "numerical")
    row("Delta chi2 (3 params)", m["dchi"], p182["dchi2"], 0.5, "numerical", "cubic-spline vs their Catmull-Rom interpolation of the curves")
    Cf = fisher_cov(cv, n, fit)
    dh = fit["D"] / np.linalg.norm(fit["D"])
    row("Fisher sigma_A along the fitted direction", float(np.sqrt(dh @ Cf[1:, 1:] @ dh)), p182["sigA_fisher"], 0.005, "numerical")
    w, V = np.linalg.eigh(Cf[1:, 1:])
    row("Fisher best-constrained sigma", float(np.sqrt(w[0])), p182["sig_strong"], 0.003, "numerical")
    row("Fisher least-constrained sigma", float(np.sqrt(w[2])), p182["sig_weak"], 0.005, "numerical")
    row("least-constrained axis angle to CFG182's (deg)", axis_ang(V[:, 2], lb_to_vec(*p182["weak_dir_lb"])), 0.0, 10.0, "numerical")
    # bootstrap sigma along the fitted direction (CFG182's definition of sigma_A) recomputed with my seeds
    Db, Ab = run_boot(cv, n, la0, np.arange(cv.N), 19203, 0, 2000, extra=fit["u"])
    Cb = np.cov(Db.T)
    sig_along = float(np.sqrt(dh @ Cb @ dh))
    row("bootstrap sigma_A ALONG the fitted direction (CFG182's definition)", sig_along, b182["bootstrap"]["sigA"], 0.03, "numerical")
    row("bootstrap std of |D-hat| (my first-read definition)", m["sigA_std"], b182["bootstrap"]["sigA"], 0.03, "definition", "the README's 'sigma_A' is sqrt(d^T Sigma d), the component along the fitted direction, NOT the std of the amplitude")
    row("bootstrap rms component", m["sigA_comp"], b182["bootstrap"]["sigA"], 0.03, "definition")
    for k, nm in enumerate("xyz"):
        row(f"bootstrap sigma of D_{nm}", float(np.sqrt(Cb[k, k])), b182["bootstrap"]["sig_components"][k], 0.03, "numerical")
    row("cone 68% (deg)", m["cone68"], b182["bootstrap"]["cone68"], 5, "numerical")
    row("cone 95% (deg)", m["cone95"], b182["bootstrap"]["cone95"], 5, "numerical")
    pm = b182["permutation"]
    R.P(f"  (CFG182 permutation keys: {list(pm.keys())})")
    row("permutation p simple", m["ps"], 0.7716, 0.05, "numerical")
    row("permutation p block", m["pb"], 0.7742, 0.05, "definition", "CFG182 compares the block null with its own A_obs = 0.231 (UMa members collapsed to their mean position); mine compares the block null with the true-position 0.237")
    row("permutation p, larger of the two", m["pA"], 0.7742, 0.05, "numerical")
    A_, F_, D_, _ = run_perms(cv, n, uma, None, None, la0, "simple", 19201, 0, 5000)
    row("permutation null A-hat median (simple)", float(np.median(A_)), 0.339, 0.015, "numerical", "mine 2.4 sigma(MC) higher; unexplained at this level, no effect on p")
    row("permutation null A-hat 95% quantile (simple)", float(np.quantile(A_, .95)), 0.615, 0.03, "numerical")
    row("permutation null A-hat 99.7% quantile (simple)", float(np.quantile(A_, .997)), 0.849, 0.10, "numerical")
    R.banner("2. fixed directions (A_fix +/- bootstrap sigma)")
    fx182 = b182["fixed_directions"]
    R.P(f"  (CFG182 fixed_directions keys: {list(fx182.keys()) if isinstance(fx182, dict) else type(fx182)})")
    t182 = {"CMB": (-0.068, 0.155), "bulk": (0.014, 0.175), "Chang": (0.110, 0.226), "Zhou": (0.066, 0.237), "Virgo": (-0.102, 0.151), "UMa": (-0.141, 0.170)}
    for nm, (a, s) in t182.items():
        A_m, s_m = m["fixed"][nm]
        row(f"A_fix {nm}", A_m, a, 0.03, "numerical")
        row(f"sigma of A_fix {nm}", s_m, s, 0.03, "numerical", "500 vs 1000 bootstrap resamples: MC noise ~5-10%")
    R.banner("3. hemisphere, splits, PV template, distance trend, variants")
    h182 = b182["hemisphere"]
    row("H_max", m["Hmax"], h182["Hmax"], 0.02, "definition", "3072-point Fibonacci axes vs HEALPix nside 16 (declared deviation)")
    row("H at the Zhou axis", m["Hz"], h182["H_zhou_axis"], 0.05, "definition", "hemisphere of the exact axis vs the axis snapped to a HEALPix pixel (not read)")
    ds = b182["split_distance"]
    R.P(f"  (CFG182 split_distance keys: {list(ds.keys()) if isinstance(ds, dict) else type(ds)})")
    row("H vs I vectors p (S2a)", m["p_split"], 0.108, 0.06, "numerical", "bootstrap covariances of 1000 resamples each, different seeds; both above 0.05")
    row("H: along-direction z (S2b)", m["zH"], -0.76, 0.25, "numerical")
    row("I: along-direction z (S2b)", m["zI"], 1.41, 0.25, "numerical")
    row("inclination split p", m["p_inc"], 0.423, 0.06, "definition", "tie handling at Inc = 63 deg: mine puts Inc == median in the low half, CFG182 in the high half")
    row("footprint axis angle to the fit (deg)", m["axa"], b182["footprint_alignment"]["axis_angle"], 3.0, "numerical")
    row("PV template |W| (km/s)", m["Wpv"], 209, 40, "numerical", "different optimiser and bounds; both ~200-240 km/s")
    row("PV template Delta chi2", m["dchiPV"], 12.23, 1.5, "numerical")
    row("distance trend beta with the dipole", m["beta"], 0.047, 0.03, "numerical")
    vs = {k: v for k, v in AB["B"].items()}
    row("no-Birge variant A-hat", vs["primary Birge none"]["A"], 0.605, 0.05, "numerical")
    row("no-Birge variant p", vs["primary Birge none"]["p"], 0.1199, 0.05, "numerical")
    row("all-usable (171) variant A-hat", AB["A1"]["Q<=3, no Inc cut (all usable)"]["A"], 0.308, 0.03, "numerical")
    row("all-usable (171) variant p", AB["A1"]["Q<=3, no Inc cut (all usable)"]["p"], 0.5872, 0.06, "numerical")
    R.P("  kernel P2 / simple variants: NOT run in CFG192 (not in the frozen attack list); CFG182 gives A = 0.228 / 0.215, p = 0.78 / 0.84")
    R.banner("4. Neyman limit and recovery table (their B9)")
    ul = b182["upper_limit"]
    R.P(f"  (CFG182 upper_limit keys: {list(ul.keys()) if isinstance(ul, dict) else type(ul)})")
    row("A95 (larger of simple/block), 1000-trial 6-run max", max(CD["D1"]["a95"].values()), 0.425, 0.06, "numerical")
    row("A95 simple (mean of 3 seeds)", float(np.mean([v for k, v in CD["D1"]["a95"].items() if k.startswith("simple")])), 0.425, 0.06, "numerical")
    row("A95 block (mean of 3 seeds)", float(np.mean([v for k, v in CD["D1"]["a95"].items() if k.startswith("block")])), 0.375, 0.06, "numerical")
    for Ai, th in ((0.1, 0.372), (0.2, 0.391), (0.3, 0.454), (0.5, 0.590)):
        row(f"<A-hat> at A_inj = {Ai}", CD["C2"][str(Ai)]["meanA"], th, 0.03, "numerical")
    for Ai, th in ((0.2, 55), (0.3, 41), (0.5, 26)):
        row(f"median direction error at A_inj = {Ai} (deg)", CD["C2"][str(Ai)]["med_ang"], th, 6, "numerical")
    R.banner("5. MUTATE (their point-level injection A = 0.20 toward (114.6, -41.9))")
    mu = bm182["mutate"]
    R.P(f"  (CFG182 mutate keys: {list(mu.keys())})")
    # my A = 0.20 injection in THEIR direction, point-level, from their profile file? -> rebuild here (own data path)
    dj = lb_to_vec(114.6, -41.9)
    Pp = [prep(g) for g in G]
    Pp = [p for p in Pp if p["N"] >= 5]
    Pm = [inject_point(p, 0.2 * dj, a0ref=1.2e-10) for p in Pp]
    prm = build_profiles(Pm, make_cfg())
    scm = birge(prm["chi"], prm["N"])
    ix = np.where(d["mask"])[0]
    cvm = Curves(prm["grid"], prm["chi"][ix] / scm[ix][:, None])
    fm = fit_dipole(cvm, n, starts=5)
    chg = fm["D"] - fit["D"]
    R.P(f"  my point-level injection of A = 0.20 toward (114.6, -41.9) with a0ref = 1.2e-10: change vector {np.linalg.norm(chg):.3f}, {ang(chg, dj):.1f} deg from the injection (CFG182: 0.151, 22 deg)")
    row("change-vector amplitude for THEIR injection", float(np.linalg.norm(chg)), 0.151, 0.03, "numerical", "same injection recipe, own code")
    row("change-vector angle for THEIR injection (deg)", ang(chg, dj), 22.0, 6.0, "numerical")
    rats = CD["C4"]
    R.P(f"  recovery of the change vector, 4 tetrahedral directions, point level mult: {rats['point mult']:.3f} (CFG182's single direction: 0.755); curve-level real sky {CD['C3']['0.3']['ratio_change']:.3f}")
    R.banner("6. post hoc (CFG182's cfg182_e_posthoc): Hubble-flow subsample toward the CMB dipole")
    Hix = np.where(b["fD"] == 1)[0]
    cvH, nH = cv.sub(Hix), n[Hix]
    fH = fit_dipole(cvH, nH, starts=5)
    R.P(f"  CFG192: Hubble-flow-only dipole A = {fH['A']:.3f} toward ({vec_to_lb(fH['D'])[0]:.0f}, {vec_to_lb(fH['D'])[1]:.0f}); {ang(fH['D'], DIRS['CMB']):.1f} deg from the CMB dipole (CFG182 post hoc: 4 deg; A along CMB +0.47 +/- 0.23)")
    cf = fit_fixed(cvH, nH, DIRS["CMB"])
    R.P(f"  CFG192: Hubble-flow amplitude along the CMB direction: {cf['s']:+.3f}")
    ok_all = all(r["ok"] for r in rows)
    R.P(f"\n  rows compared: {len(rows)}; within tolerance: {sum(r['ok'] for r in rows)}; differing rows: {[r['name'] for r in rows if not r['ok']]}")
    R.P("  classes of the differing rows: " + str({c: sum(1 for r in rows if r['cls'] == c) for c in sorted(set(r['cls'] for r in rows if not r['ok']))}))
    R.num("rows", rows)
    R.num("post_hoc_H_CMB_angle", ang(fH["D"], DIRS["CMB"]))
    return R.finish(0)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        import traceback
        traceback.print_exc()
        sys.exit(2)
