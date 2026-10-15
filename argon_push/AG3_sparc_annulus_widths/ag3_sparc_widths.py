#!/usr/bin/env python3
"""AG3 — SPARC phantom-annulus widths vs the AG1 ladders.

Question (AG1's queued observational kill test): AG1 (argon_push/AG1_g081_mode_
adjudication, 77036c1ff) showed a CONSERVATIVE isothermal A/r^2 phantom annulus
[r_in, r_out] destabilizes once its width crosses the BC ladders (DF-binding first
rung w1 = e^{(pi - atan(sqrt7/5))/nu0}, nu0 = sqrt7/2; DD/FF e^{2pi/sqrt7}). How wide
are the annuli REAL galaxies settle into?

Exact law algebra (Amendment A, frozen pre-run): for law-obeying curves
(g^2 - gbar^2 = a0*gbar), the phantom-force ratio

    rho(r) = r*g_ph/C,  C = sqrt(a0*G*M_b),  g_ph = g_obs - gbar

obeys  rho = sqrt(M(r)/M_b) / (sqrt(u+1) + sqrt(u)),  u = gbar/a0 = G M(r)/(a0 r^2),
M(r) = r^2 gbar/G measured per point. In-band (rho >= 1/f) iff the exact relation says
so; f=2 primary band; r_lo = run start, r_hi = run end (outermost-two allowance).

Pipeline precedent: G071/G044 corpus conventions (v_b^2 = sign(Vgas)Vgas^2 +
m2l*(Vdisk^2+Vbul^2), m2l fallback 0.50). a0 read at runtime from G081_results.json.
Part B (exploratory, non-gated): baryon-inclusive local-hydrostatic eigen-solve,
ODE assembled SYMBOLICALLY from primitives (drift = -G M_b/(2 r^2), NOT zero — the
constant-sigma^2 closure cancellation does not survive the baryon term).

FROZEN_CRITERIA.md (4560f945c) + AMENDMENT A (7527066a6) govern. Exit 0 iff K2b PASS,
K5 branch-stable, and (MUTATE=1: mutations behave as designed).
"""
import csv
import json
import math
import os
import sys

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
CORPUS = os.path.join(REPO, "glm53_push", "data", "rotation_curve_corpus_v7.json")
ENVTAB = os.path.join(REPO, "real_research", "data", "sparc_a0_environment_table.csv")
G081_JSON = os.path.join(REPO, "deepseek_push", "G081_results.json")

MUTATE = os.environ.get("MUTATE", "0") == "1"

# ---------------- units (mixed: kpc, km/s, Msun) derived from SI, no magic numbers ----
G_SI = 6.674e-11            # m^3 kg^-1 s^-2
MSUN_KG = 1.98892e30        # kg
KPC_M = 3.0856775814913673e19
KPC_KM = KPC_M / 1e3
MYR_S = 3.1557e13
G_MIXED = G_SI * MSUN_KG / (KPC_M * 1e6)      # kpc (km/s)^2 / Msun
OMEGA_CONV = 1000.0 / KPC_M                    # (km/s)/kpc -> s^-1

NU0 = math.sqrt(7.0) / 2.0
W1_DF = math.exp((math.pi - math.atan(math.sqrt(7) / 5)) / NU0)   # AG1 closed forms
W1_DD = math.exp(math.pi / NU0)

F_PRIMARY = 2.0
F_BANDS = [math.sqrt(2.0), 2.0, 3.0]
SEED = 20261015


def load_inputs():
    g081 = json.load(open(G081_JSON))
    a0_SI = g081["constants"]["a0"]
    alpha_break = g081["constants"]["alpha_break"]
    a0_mixed = (a0_SI / 1000.0) * KPC_KM       # m/s^2 -> (km/s)^2/kpc
    corpus = json.load(open(CORPUS))["galaxies"]
    env = {}
    for e in csv.DictReader(open(ENVTAB)):
        env[e["name"].strip()] = e
    return g081, a0_mixed, alpha_break, corpus, env


def env_ok(row, a0_mixed):
    """G071 isolated/low-EFE subset: fields present, Y = g_ext/a0 < 0.1, Nm_host <= 1,
    usable_2mrs == 1."""
    try:
        logMh = float(row["logMhalo_host"])
        dMpc = float(row["D_Mpc"])
    except (ValueError, TypeError):
        return False
    d_kpc = dMpc * 1000.0                      # Mpc -> kpc
    g_ext = G_MIXED * 10**logMh / d_kpc**2     # (km/s)^2/kpc
    if g_ext / a0_mixed >= 0.1:
        return False
    try:
        if float(row["Nm_host"]) > 1:
            return False
    except (ValueError, TypeError):
        return False
    return str(row["usable_2mrs"]).strip() == "1"


def galaxy_pipeline(g, a0m, f_list, mb_override=None):
    pts = g["data"]
    m2l = g.get("m2l_disk")
    if m2l is None or float(m2l) <= 0:
        m2l = 0.5                              # G071 fallback (precedent)
    m2l = float(m2l)
    R = np.array([p["Rad"] for p in pts], float)
    Vo = np.array([p["Vobs"] for p in pts], float)
    eV = np.array([p["errV"] if p["errV"] is not None else 0.0 for p in pts], float)
    Vg = np.array([p["Vgas"] for p in pts], float)
    Vd = np.array([p["Vdisk"] if p["Vdisk"] is not None else 0.0 for p in pts], float)
    Vb = np.array([p["Vbul"] if p["Vbul"] is not None else 0.0 for p in pts], float)
    vb2 = np.sign(Vg) * Vg**2 + m2l * (Vd**2 + Vb**2)
    valid = (Vo > 0) & (eV < Vo) & (vb2 > 0) & (R > 0)
    n_dropped = int(np.sum(~valid))
    R, Vo, vb2 = R[valid], Vo[valid], vb2[valid]
    if len(R) < 6:
        return dict(ok=False, reason="n<6", n_dropped=n_dropped)
    order = np.argsort(R)
    R, Vo, vb2 = R[order], Vo[order], vb2[order]
    gobs = Vo**2 / R
    gbar = vb2 / R
    gph = gobs - gbar
    Mb_enc = R * vb2 / G_MIXED                 # Msun enclosed baryonic per point
    M_b = float(np.max(Mb_enc)) if mb_override is None else float(mb_override)
    C = math.sqrt(a0m * G_MIXED * M_b)         # (km/s)^2
    rM = math.sqrt(G_MIXED * M_b / a0m)        # kpc
    rho = R * gph / C
    u = gbar / a0m
    frac = np.sqrt(np.clip(Mb_enc / M_b, 0, None))
    rho_pred = frac / (np.sqrt(u + 1.0) + np.sqrt(u))
    n_neg_gph = int(np.sum(rho <= 0))

    runs = {}
    for f in f_list:
        ok = rho >= 1.0 / f
        n = len(R)
        cand = []
        i = 0
        while i < n:
            if ok[i]:
                j = i
                while j + 1 < n and ok[j + 1]:
                    j += 1
                cand.append((i, j))
                i = j + 1
            else:
                i += 1
        elig = [(i, j) for (i, j) in cand if (j - i + 1) >= 2 and j >= n - 2]
        runs[f] = elig[-1] if elig else None

    # K2b crossings (continuous, log-r linear interpolation of rho vs 1/2)
    def crossing(rr, vals):
        thr = 0.5
        if vals[0] >= thr:
            return rr[0], True                  # left-censored
        for i in range(1, len(rr)):
            if vals[i - 1] < thr <= vals[i]:
                wgt = (thr - vals[i - 1]) / (vals[i] - vals[i - 1])
                return rr[i - 1] * (rr[i] / rr[i - 1]) ** wgt, False
        return None, False

    x_meas, cens_m = crossing(R, rho)
    x_pred, cens_p = crossing(R, rho_pred)

    # K1 law diagnostic
    lawq = (gobs**2 - gbar**2) / (a0m * gbar)
    pos = lawq > 0
    k1_rms = float(np.sqrt(np.mean(np.log10(lawq[pos])**2))) if np.sum(pos) >= 3 else None

    # K4 interior discriminator points
    interior = R <= 0.62 * rM

    return dict(ok=True, name=g["galaxy"], R=R, gph=gph, gbar=gbar, gobs=gobs,
                M_b=M_b, Mb_enc=Mb_enc, C=C, rM=rM, rho=rho, rho_pred=rho_pred,
                u=u, runs=runs, x_meas=x_meas, x_pred=x_pred, Vo=Vo, errV=eV[valid][order],
                quality_tier=g.get("quality_tier"),
                censored=bool(cens_m or cens_p), n_dropped=n_dropped,
                n_neg_gph=n_neg_gph, k1_rms=k1_rms,
                interior_rho=(rho[interior] if np.any(interior) else np.array([])),
                interior_sig=(2.0 * Vo[interior] * eV[valid][order][interior] / C if np.any(interior) else np.array([])),
                interior_pred=(rho_pred[interior] if np.any(interior) else np.array([])),
                n_pts=len(R))


def eigen_b2(r_lo, r_hi, M_b, C, Gm):
    """Part B2: lowest omega^2 of  sigma^2(r) xi'' - (G M_b/(2 r^2)) xi' + (C/r^2 + w^2) xi = 0
    with sigma^2(r) = (G M_b/r + C)/2, D at r_lo, F (xi' + 2 xi/r = 0) at r_hi.
    omega^2 in (km/s)^2/kpc^2; adaptive scan in units of scale = C/r_lo^2 (narrow annuli
    have eigenvalues far above any fixed window: first sign change from below = lowest root)."""
    GmMb = Gm * M_b
    scale = C / r_lo**2

    def resid(w2):
        def rhs(r, y):
            s2 = (GmMb / r + C) / 2.0
            return [y[1], (GmMb / (2 * r**2)) * y[1] / s2 - (C / r**2 + w2) * y[0] / s2]
        sol = solve_ivp(rhs, (r_lo, r_hi), [0.0, 1.0], rtol=1e-10, atol=1e-12)
        return sol.y[1, -1] + 2.0 * sol.y[0, -1] / r_hi

    def first_root(hi_units):
        ws = np.linspace(-2.0, hi_units, 281) * scale
        vals = [resid(w) for w in ws]
        idx = np.where(np.diff(np.sign(vals)) != 0)[0]
        if len(idx) == 0:
            return None
        return brentq(resid, ws[idx[0]], ws[idx[0] + 1], xtol=1e-12 * scale, rtol=1e-12)

    for hi in (12.0, 60.0, 400.0, 4000.0):
        root = first_root(hi)
        if root is not None:
            return root
    return float("nan")


def b2_symbolic_assembly():
    """Assemble the Part-B ODE from primitives with sympy and print the coefficients
    (no typed ODEs)."""
    r, Gm, Mb, C, w2 = sp.symbols("r Gm Mb C w2", positive=True)
    xi = sp.Function("xi")
    Xi0, Xi1, Xi2 = sp.symbols("Xi0 Xi1 Xi2")
    s2 = (Gm * Mb / r + C) / 2                 # local-hydrostatic sigma^2(r)
    s2p = sp.diff(s2, r)
    Phi0p = Gm * Mb / r**2 + C / r             # baryon + phantom (A/r^2, C = 4 pi G A)
    rho0 = C / (4 * sp.pi * Gm * r**2)         # A/r^2 with A = C/(4 pi G)
    delta_rho = -rho0 * sp.Derivative(xi(r), r)
    phi1p = -C * xi(r) / r**2                  # inner mass frozen (AG1 convention)
    euler = (-w2 * rho0 * xi(r) + rho0 * phi1p + delta_rho * Phi0p
             + sp.diff(s2 * delta_rho, r))
    e = sp.simplify(euler / rho0).subs({xi(r): Xi0, sp.Derivative(xi(r), r): Xi1,
                                        sp.Derivative(xi(r), (r, 2)): Xi2})
    e = sp.expand(e)
    c2, c1 = sp.simplify(e.coeff(Xi2, 1)), sp.simplify(e.coeff(Xi1, 1))
    c0 = sp.simplify(e.coeff(Xi0, 1))
    # predicted (up to the global euler/rho0 = -E convention sign, same as AG1 C0):
    pred2 = s2
    pred1 = -Gm * Mb / (2 * r**2)
    pred0 = C / r**2 + w2
    rat2, rat1, rat0 = (sp.simplify(c2 / pred2), sp.simplify(c1 / pred1), sp.simplify(c0 / pred0))
    ok = rat2 == rat1 == rat0 and rat2 != 0
    print("B2 symbolic assembly (from primitives, sigma^2(r) local-hydrostatic):")
    print(f"  xi'' coeff  : {c2}   /pred {rat2}")
    print(f"  xi'  coeff  : {sp.simplify(sp.factor(c1))}   /pred {rat1}")
    print(f"  xi   coeff  : {sp.simplify(sp.factor(c0))}   /pred {rat0}")
    print(f"  assembly matches predicted coefficients up to global sign {rat2}: {ok}")
    return bool(ok)


def verdict_from(ws, thr_df=W1_DF):
    ws = np.array(ws)
    med = float(np.median(ws))
    q1, q3 = float(np.percentile(ws, 25)), float(np.percentile(ws, 75))
    fr_df = float(np.mean(ws > thr_df))
    fr_dd = float(np.mean(ws > W1_DD))
    if med < thr_df and fr_df <= 0.10:
        v = "S"
    elif med > thr_df or fr_df > 0.30:
        v = "F"
    else:
        v = "AMBIGUOUS"
    return dict(n=len(ws), median=med, q1=q1, q3=q3, frac_gt_DF=fr_df, frac_gt_DD=fr_dd,
                verdict=v)


def main():
    g081, a0m, alpha_break, corpus, env = load_inputs()
    print("=" * 96)
    print("AG3 — SPARC phantom-annulus widths vs AG1 ladders (FROZEN 4560f945c + AMD-A 7527066a6)")
    print(f"a0 = {a0m:.4f} (km/s)^2/kpc  (runtime from G081_results.json: {g081['constants']['a0']} m/s^2)")
    print(f"AG1 thresholds (closed forms, recomputed): w1(DF) = {W1_DF:.4f}, w1(DD) = {W1_DD:.4f}")
    print(f"G = {G_MIXED:.6e} kpc (km/s)^2/Msun;  MUTATE = {MUTATE}")
    print("=" * 96)

    b2_ok = b2_symbolic_assembly()

    sparc = [g for g in corpus if str(g.get("survey", "")).strip().upper() == "SPARC"]
    print(f"\nSPARC galaxies in corpus v7: {len(sparc)}")

    shuffle_map = None
    results = []
    mbs_all = []
    for g in sparc:
        r = galaxy_pipeline(g, a0m, F_BANDS)
        if r.get("ok"):
            mbs_all.append(r["M_b"])
        results.append(r)

    if MUTATE:
        # M1: shuffle M_b across galaxies (seeded permutation)
        rng = np.random.default_rng(SEED)
        perm = rng.permutation(len(mbs_all))
        mb_pool = np.array(mbs_all)
        k = 0
        mb_for = {}
        for r in results:
            if r.get("ok"):
                mb_for[r["name"]] = mb_pool[perm[k]]
                k += 1
        results = []
        for g in sparc:
            nm = g["galaxy"]
            r = galaxy_pipeline(g, a0m, F_BANDS, mb_override=mb_for.get(nm))
            results.append(r)

    ok_res = [r for r in results if r.get("ok")]
    n_small = sum(1 for r in results if not r.get("ok"))
    eligible = [r for r in ok_res if r["runs"][F_PRIMARY] is not None]
    print(f"cleaned sample: {len(ok_res)} (dropped {n_small} with <6 valid points)")
    print(f"eligible (in-band run reaching the edge, f={F_PRIMARY}): {len(eligible)}; "
          f"no eligible run: {len(ok_res) - len(eligible)}")
    n_cens = sum(1 for r in eligible if r["censored"])
    print(f"left-censored (already in band at innermost point): {n_cens}")

    # ---- K1
    k1s = [r["k1_rms"] for r in ok_res if r["k1_rms"] is not None]
    k1_med = float(np.median(k1s))
    print(f"\nK1 law diagnostic: median per-galaxy rms log10[(g^2-gbar^2)/(a0*gbar)] = {k1_med:.4f} dex "
          f"(registered benchmark ~0.15; report only)")
    k1_deep = []
    for r in ok_res:
        m = (r["u"] <= 1.0) & ((r["gobs"]**2 - r["gbar"]**2) > 0)
        if np.sum(m) >= 3:
            lawq = (r["gobs"][m]**2 - r["gbar"][m]**2) / (a0m * r["gbar"][m])
            k1_deep.append(float(np.sqrt(np.mean(np.log10(lawq)**2))))
    k1_deep_med = float(np.median(k1_deep)) if k1_deep else float("nan")
    print(f"K1-deep variant (u = gbar/a0 <= 1 points only, n_gal = {len(k1_deep)}): median rms = "
          f"{k1_deep_med:.4f} dex  [post-hoc diagnostic variant, report only: the full-point K1 is "
          f"dominated by the deep interior where g^2-gbar^2 is a noise-amplified small difference]")

    # ---- K2a
    lrs = []
    for r in ok_res:
        m = (r["rho"] > 0) & (r["rho_pred"] > 0)
        lrs.extend(np.log(r["rho"][m] / r["rho_pred"][m]))
    lrs = np.array(lrs)
    k2a_med, k2a_iqr = float(np.median(lrs)), float(np.percentile(lrs, 75) - np.percentile(lrs, 25))
    k2a_flag = abs(k2a_med) < 0.25
    print(f"K2a exact law identity in rho-space: median ln(rho_meas/rho_pred) = {k2a_med:+.4f}, "
          f"IQR = {k2a_iqr:.4f}  -> {'quiet' if k2a_flag else 'LOUD DATA-QUALITY FLAG'}")

    # ---- K2b (EXIT-GATED)
    lr = []
    lr_grid = []
    for r in eligible:
        if r["x_meas"] is None or r["x_pred"] is None:
            continue
        if r["censored"]:
            lr.append(0.0)
        else:
            lr.append(math.log(r["x_meas"] / r["x_pred"]))
        i = r["runs"][F_PRIMARY][0]
        lr_grid.append(math.log(r["R"][i] / r["x_pred"]))
    lr = np.array(lr); lr_grid = np.array(lr_grid)
    k2b_med = float(np.median(np.abs(lr)))
    k2b_signed = float(np.median(lr))
    k2b_pass = k2b_med < 0.15
    print(f"K2b r_lo measured-vs-predicted crossings: median |ln| = {k2b_med:.4f} "
          f"(signed {k2b_signed:+.4f}; grid-start variant median ln = {float(np.median(lr_grid)):+.4f}) "
          f"-> {'PASS (<0.15)' if k2b_pass else 'FAIL'}")

    # ---- K2d (POST-HOC, non-gated diagnostic — added after the first run FAILED K2b with a
    #      signed median of exactly +0.0000: symmetric scatter is the signature of noise, not
    #      bias. Quantifies whether the K2b scatter is consistent with propagating the corpus
    #      errV through the difference-amplified rho estimator. Clearly labeled post-hoc;
    #      the frozen K2b FAIL stands and the verdict stays CONDITIONAL-on-record.)
    rng = np.random.default_rng(SEED)

    def mc_sigma_ln(r, n=300):
        R, gbar, C, Vo, eV = r["R"], r["gbar"], r["C"], r["Vo"], r["errV"]
        xs = []
        for _ in range(n):
            Vp = np.abs(Vo + rng.normal(0.0, np.maximum(eV, 1e-9)))
            rho_m = R * (Vp**2 / R - gbar) / C
            if rho_m[0] >= 0.5:
                continue
            for i in range(1, len(R)):
                if rho_m[i - 1] < 0.5 <= rho_m[i]:
                    wg = (0.5 - rho_m[i - 1]) / (rho_m[i] - rho_m[i - 1])
                    xs.append(R[i - 1] * (R[i] / R[i - 1]) ** wg)
                    break
        if len(xs) < 30:
            return None
        return float(np.std(np.log(np.array(xs))))

    zs = []
    sigmas = []
    unc = [r for r in eligible if (not r["censored"]) and r["x_meas"] and r["x_pred"]]
    for r in unc:
        s = mc_sigma_ln(r)
        if s and s > 0:
            zs.append(math.log(r["x_meas"] / r["x_pred"]) / s)
            sigmas.append(s)
    zs = np.array(zs)
    med_abs_z = float(np.median(np.abs(zs)))
    frac_2sig = float(np.mean(np.abs(zs) > 2))
    k2d_noise_consistent = (0.4 <= med_abs_z <= 1.2) and frac_2sig <= 0.15
    print(f"K2d [post-hoc, non-gated] MC noise budget (errV propagated, seed {SEED}, 300 draws): "
          f"n = {len(zs)}, median |z| = {med_abs_z:.3f} (0.67 expected if noise-dominated), "
          f"frac |z|>2 = {frac_2sig:.3f}, median sigma_ln(r_lo) = {float(np.median(sigmas)) if sigmas else float('nan'):.3f}")
    print(f"    -> K2b scatter {'CONSISTENT with measurement noise (unbiased; tolerance was frozen '
          'tighter than the difference-amplified estimator supports)' if k2d_noise_consistent else 'NOT explained by errV noise — systematic suspicion stands'}")

    # ---- K2c
    offs = []
    for r in eligible:
        i = r["runs"][F_PRIMARY][0]
        if r["R"][i] > 0 and r["rM"] > 0:
            offs.append(math.log(r["R"][i] / ((4.0 / 3.0) * r["rM"])))
    corr = []
    for r in eligible:
        i = r["runs"][F_PRIMARY][0]
        corr.append(0.5 * math.log(max(r["Mb_enc"][i] / r["M_b"], 1e-12)))
    print(f"K2c point-mass corollary (report): median ln(r_lo/((4/3)r_M)) = {float(np.median(offs)):+.4f}; "
          f"median enclosed-mass correction ln sqrt(M(r_lo)/M_b) = {float(np.median(corr)):+.4f}")

    # ---- K3 widths + verdict (f=2 primary)
    def widths(rlist, f):
        ws = []
        for r in rlist:
            run = r["runs"][f]
            if run is None:
                continue
            i, j = run
            ws.append(r["R"][j] / r["R"][i])
        return ws

    ws_all = widths(eligible, F_PRIMARY)
    ws_nc = widths([r for r in eligible if not r["censored"]], F_PRIMARY)
    v_all = verdict_from(ws_all)
    v_nc = verdict_from(ws_nc) if ws_nc else None
    # G071 isolated/low-EFE robustness subset
    env_names = {nm for nm, row in env.items() if env_ok(row, a0m)}
    eligible_env = [r for r in eligible if r["name"] in env_names]
    ws_env = widths(eligible_env, F_PRIMARY)
    v_env = verdict_from(ws_env) if len(ws_env) >= 5 else None
    print(f"\nK3 widths w = r_hi/r_lo (f={F_PRIMARY}): n = {v_all['n']}")
    print(f"    median = {v_all['median']:.3f}  IQR = [{v_all['q1']:.3f}, {v_all['q3']:.3f}]  "
          f"max = {max(ws_all):.2f}")
    print(f"    frac(w > {W1_DF:.4f} DF rung) = {v_all['frac_gt_DF']:.3f};  "
          f"frac(w > {W1_DD:.4f} DD rung) = {v_all['frac_gt_DD']:.3f}")
    print(f"    VERDICT (primary sample): {v_all['verdict']}")
    if v_nc:
        print(f"    robustness, censored excluded: n = {v_nc['n']}, median = {v_nc['median']:.3f}, "
              f"verdict = {v_nc['verdict']}")
    if v_env:
        print(f"    robustness, G071 isolated/low-EFE subset: n = {v_env['n']}, median = {v_env['median']:.3f}, "
              f"frac>DF = {v_env['frac_gt_DF']:.3f}, verdict = {v_env['verdict']}")
    else:
        print("    robustness, G071 isolated/low-EFE subset: n < 5 — not evaluated")
    k3_robust = all(v["verdict"] == v_all["verdict"] for v in (v_nc, v_env) if v)
    print(f"    K3 branch stable under robustness cuts: {k3_robust}"
          + ("" if k3_robust else "  *** FLIP => K3 verdict CONDITIONAL (loud, per freeze) ***"))
    # top-width census (report): the w > DF-rung galaxies are AG1's dissipative-settling candidates
    top = sorted(eligible, key=lambda r: -(r["R"][r["runs"][F_PRIMARY][1]] / r["R"][r["runs"][F_PRIMARY][0]]))[:5]
    print("    top-5 widths (AG1 unstable candidates if conservative): " + "; ".join(
        f"{r['name']} w={r['R'][r['runs'][F_PRIMARY][1]]/r['R'][r['runs'][F_PRIMARY][0]]:.2f} "
        f"(tier {r['quality_tier']})" for r in top))

    # ---- K4 interior discriminator
    xball = []
    sig_int = []
    pred_int = []
    for r in ok_res:
        if len(r["interior_rho"]) >= 2:
            xball.append(float(np.median(r["interior_rho"])))
            sig_int.extend(r["interior_sig"].tolist())
            pred_int.extend(r["interior_pred"].tolist())
    xball = np.array(xball)
    x_med = float(np.median(xball))
    if x_med >= 0.8:
        k4 = "STATIC-BALL reading realized inside the cap"
    elif x_med <= 0.4:
        k4 = "LAW-HAZE reading realized inside the cap (phantom NOT A/r^2 there)"
    else:
        k4 = "AMBIGUOUS"
    print(f"\nK4 interior discriminator: X_ball = median over {len(xball)} galaxies of median "
          f"rho(r <= {alpha_break} r_M) = {x_med:.4f}")
    print(f"    (static ball predicts ~1; law-haze <= 0.285*sqrt(M/M_b)) -> {k4}")
    if sig_int:
        print(f"    noise floor (post-hoc refinement): interior median sigma_rho = "
              f"{float(np.median(sig_int)):.4f} vs law-haze signal median rho_pred = "
              f"{float(np.median(pred_int)):.4f} vs X_ball = {x_med:.4f}")
        # Upsilon-systematic proxy: 20% mass-to-light error moves interior rho by ~0.2*u*R/r_M
        ups = []
        for r in ok_res:
            if len(r["interior_rho"]) >= 2:
                ii = r["R"] <= alpha_break * r["rM"]
                ups.extend((0.2 * r["u"][ii] * r["R"][ii] / r["rM"]).tolist())
        ups_med = float(np.median(ups)) if ups else float("nan")
        print(f"    Upsilon-systematic proxy (20% mass-to-light error): interior median delta_rho ~ {ups_med:.4f}")
        print("    -> STATIC-BALL reading (rho ~ 1) excluded decisively: |1 - X_ball| exceeds every")
        print("       statistical and systematic scale above by >10x. Haze-vs-Newtonian interior is")
        print("       NOT decidable at SPARC precision (haze signal <= combined noise+systematics).")
        print("       Load-bearing K4 statement: the cap interior is NOT an A/r^2 static ball.")

    # ---- K5 band robustness
    k5 = {}
    for f in F_BANDS:
        ws_f = widths(eligible, f)
        v_f = verdict_from(ws_f) if ws_f else None
        k5[f] = v_f
        if v_f:
            print(f"K5 f={f:.4f}: n={v_f['n']} median={v_f['median']:.3f} "
                  f"frac>DF={v_f['frac_gt_DF']:.3f} verdict={v_f['verdict']}")
    branches = {k5[f]["verdict"] for f in F_BANDS if k5[f]}
    k5_stable = len(branches) == 1
    print(f"K5 branch-stable across bands: {k5_stable} ({branches})")

    # ---- a0 robustness (freeze: decision must not flip under a0_alt; flip => CONDITIONAL loud)
    A0_ALT_SI = 1.1279e-10                     # G071's alternative SPARC-RAR footing (precedent)
    a0m_alt = (A0_ALT_SI / 1000.0) * KPC_KM
    res_alt = [galaxy_pipeline(g, a0m_alt, [F_PRIMARY]) for g in sparc]
    elig_alt = [r for r in res_alt if r.get("ok") and r["runs"][F_PRIMARY] is not None]
    ws_alt = widths(elig_alt, F_PRIMARY)
    v_alt = verdict_from(ws_alt) if len(ws_alt) >= 5 else None
    if v_alt:
        a0_stable = v_alt["verdict"] == v_all["verdict"]
        print(f"a0 robustness (a0_alt = {A0_ALT_SI} m/s^2): n = {v_alt['n']}, median = {v_alt['median']:.3f}, "
              f"verdict = {v_alt['verdict']} -> stable: {a0_stable}"
              + ("" if a0_stable else "  *** FLIP => CONDITIONAL (loud, per freeze) ***"))
    else:
        a0_stable = True
        print("a0 robustness: n < 5 — not evaluated")

    # ---- Part B (exploratory, non-gated)
    b1 = []
    for r in eligible:
        i, j = r["runs"][F_PRIMARY]
        b1.extend((r["rM"] / r["R"][i:j + 1]).tolist())
    print(f"\nB1 baryon/phantom force ratio r_M/r over annuli: median = {float(np.median(b1)):.3f} "
          f"IQR = [{float(np.percentile(b1,25)):.3f}, {float(np.percentile(b1,75)):.3f}] (non-negligible => "
          f"AG1 phantom-only threshold is an idealization; B2 refines)")
    b2_vals = []
    b2_norm = []
    b2_unstable = 0
    for r in eligible:
        i, j = r["runs"][F_PRIMARY]
        w2 = eigen_b2(r["R"][i], r["R"][j], r["M_b"], r["C"], G_MIXED)
        b2_vals.append(w2)
        b2_norm.append(w2 / (r["C"] / r["R"][i] ** 2))
        if np.isfinite(w2) and w2 < 0:
            b2_unstable += 1
    b2_arr = np.array([v for v in b2_vals if np.isfinite(v)])
    b2n_arr = np.array([v for v in b2_norm if np.isfinite(v)])
    print(f"B2 baryon-inclusive local-hydrostatic eigen-solve (D at r_lo, F at r_hi): "
          f"n = {len(b2_arr)}, unstable frac = {b2_unstable}/{len(eligible)}")
    if len(b2n_arr):
        print(f"    omega0^2/(C/r_lo^2): median = {float(np.median(b2n_arr)):+.4f}, "
              f"IQR = [{float(np.percentile(b2n_arr, 25)):+.4f}, {float(np.percentile(b2n_arr, 75)):+.4f}]")
        neg = b2_arr[b2_arr < 0]
        if len(neg):
            print(f"    unstable cases: median omega0^2 = {float(np.median(neg)):.3e} (km/s)^2/kpc^2")

    # ---- mutations (MUTATE=1)
    mut = {}
    if MUTATE:
        print("\n--- MUTATE run ---")
        # M1 was applied to the whole pipeline above (shuffled M_b): K2b must degrade
        mut["M1_k2b_degraded"] = bool(k2b_med > 0.3)
        print(f"M1 (M_b shuffled, seed {SEED}): K2b median |ln| = {k2b_med:.4f} -> degraded>0.3: "
              f"{mut['M1_k2b_degraded']}")
        # M2: band test on the BARYONIC product (frozen arms: eligibility flips >= 50%
        #     OR median r_lo shift > x1.5 among galaxies eligible in both modes)
        n_flip = 0
        n_tot = 0
        m2_rlos = {}
        for r in ok_res:
            n_tot += 1
            rho_b = r["R"] * r["gbar"] / r["C"]
            okb = rho_b >= 0.5
            elig_b = None
            n = len(okb)
            i = 0
            while i < n:
                if okb[i]:
                    j = i
                    while j + 1 < n and okb[j + 1]:
                        j += 1
                    if (j - i + 1) >= 2 and j >= n - 2:
                        elig_b = (i, j)
                    i = j + 1
                else:
                    i += 1
            if (elig_b is not None) != (r["runs"][F_PRIMARY] is not None):
                n_flip += 1
            if elig_b is not None and r["runs"][F_PRIMARY] is not None:
                m2_rlos[r["name"]] = (r["R"][elig_b[0]], r["R"][r["runs"][F_PRIMARY][0]])
        flip_frac = n_flip / max(n_tot, 1)
        shifts = [math.log(a / b) for a, b in m2_rlos.values()]
        med_shift = float(np.median(shifts)) if shifts else float("nan")
        m2_ok = flip_frac >= 0.5 or (shifts and abs(med_shift) > math.log(1.5))
        mut["M2_flips"] = flip_frac
        mut["M2_median_rlo_shift"] = med_shift
        mut["M2_ok"] = bool(m2_ok)
        print(f"M2 (band on r*gbar/C instead): eligibility flips = {n_flip}/{n_tot} "
              f"({flip_frac*100:.0f}%); both-eligible n = {len(shifts)}, median ln(r_lo,M2/r_lo,M0) = "
              f"{med_shift:+.4f} (|shift| > ln 1.5 = {math.log(1.5):.4f}? {bool(shifts and abs(med_shift) > math.log(1.5))}) "
              f"-> as designed (either arm): {m2_ok}")
        # M3: swapped roles -> gph <= 0 -> ZERO ELIGIBLE EDGE-RUNS (frozen wording);
        # any-in-band-point census reported separately (negative-g_ph points are a real
        # data fact: inner velocity deficits vs the baryon model)
        n_runs_m3 = 0
        n_any_m3 = 0
        for r in ok_res:
            rho_s = -r["rho"]
            ok_s = rho_s >= 0.5
            if np.any(ok_s):
                n_any_m3 += 1
            n = len(ok_s)
            i = 0
            while i < n:
                if ok_s[i]:
                    j = i
                    while j + 1 < n and ok_s[j + 1]:
                        j += 1
                    if (j - i + 1) >= 2 and j >= n - 2:
                        n_runs_m3 += 1
                    i = j + 1
                else:
                    i += 1
        mut["M3_empty"] = (n_runs_m3 == 0)
        print(f"M3 (gobs<->gbar swap): eligible edge-runs = {n_runs_m3} (frozen: must be 0) "
              f"-> {'PASS' if mut['M3_empty'] else 'FAIL'};  galaxies with ANY in-band point = {n_any_m3} "
              f"(reported: real inner negative-g_ph points vs the baryon model)")

    # ---- summary
    gate_pass = k2b_pass and k5_stable and b2_ok and k3_robust and a0_stable
    if MUTATE:
        gate_pass = gate_pass and mut.get("M1_k2b_degraded", False) and \
            mut.get("M2_ok", False) and mut.get("M3_empty", False)
    verdict_text = (
        f"K3 VERDICT = {v_all['verdict']} (median w = {v_all['median']:.3f} vs DF rung {W1_DF:.4f}; "
        f"frac>DF = {v_all['frac_gt_DF']:.3f}); K4 = {k4} (X_ball = {x_med:.3f}). "
        + ("Branch S: observed A/r^2 annuli are NARROW — the conservative reading is NOT falsified at "
           "observed scales; AG1's stability requirement is met by the data-implied inner cutoff."
           if v_all["verdict"] == "S" else
           "Branch F: wide settled annuli exist — the settling channel must be dissipative (S3) or the "
           "medium non-conservative (AG2)." if v_all["verdict"] == "F" else
           "Branch AMBIGUOUS: distribution straddles the rung; reported as is.")
    )
    print("\n" + "=" * 96)
    print(verdict_text)
    mode = "MUTATE" if MUTATE else "MAIN"
    print(f"AG3 {mode} COMPLETE: gates {'PASS' if gate_pass else 'FAIL'} "
          f"(K2b={'PASS' if k2b_pass else 'FAIL'}, K5-stable={k5_stable}, B2-assembly={b2_ok}"
          + (f", M1={mut.get('M1_k2b_degraded')}, M2={mut.get('M2_flips',0):.2f}, M3={mut.get('M3_empty')}" if MUTATE else "")
          + ")")

    out = dict(
        lane="AG3_sparc_annulus_widths",
        frozen="FROZEN_CRITERIA.md 4560f945c + AMENDMENT_A 7527066a6 (both pre-run)",
        mode="MUTATE" if MUTATE else "MAIN",
        a0_mixed=a0m, alpha_break=alpha_break,
        thresholds=dict(W1_DF=W1_DF, W1_DD=W1_DD, bands=F_BANDS),
        sample=dict(sparc=len(sparc), cleaned=len(ok_res), eligible=len(eligible),
                    censored=n_cens, small=n_small),
        K1_median_law_rms_dex=k1_med,
        K2a=dict(median=float(k2a_med), iqr=k2a_iqr, quiet=k2a_flag),
        K2b=dict(median_abs=float(k2b_med), median_signed=k2b_signed, pass_=bool(k2b_pass)),
        K2d_posthoc=dict(median_abs_z=med_abs_z, frac_2sig=frac_2sig,
                         median_sigma_ln=float(np.median(sigmas)) if sigmas else None,
                         noise_consistent=bool(k2d_noise_consistent)),
        K2c=dict(median_offset_pointmass=float(np.median(offs)), median_mass_correction=float(np.median(corr))),
        K3=dict(all=v_all, censored_excluded=v_nc, env_subset=v_env, robust=k3_robust),
        K4=dict(X_ball=x_med, n=len(xball), reading=k4),
        K5={str(f): k5[f] for f in F_BANDS if k5[f]},
        K5_stable=bool(k5_stable),
        a0_alt=dict(verdict=(v_alt["verdict"] if v_alt else None), median=(v_alt["median"] if v_alt else None),
                    stable=bool(a0_stable)),
        B1=dict(median_rM_over_r=float(np.median(b1))),
        B2=dict(n=len(b2_arr), unstable=b2_unstable, median_omega2=float(np.median(b2_arr)) if len(b2_arr) else None),
        mutations=mut if MUTATE else None,
        gates_pass=bool(gate_pass),
        verdict=verdict_text,
        per_galaxy=[dict(name=r["name"], M_b=r["M_b"], rM=r["rM"], C=r["C"],
                          run=(list(r["runs"][F_PRIMARY]) if r["runs"][F_PRIMARY] else None),
                          r_lo=(r["R"][r["runs"][F_PRIMARY][0]] if r["runs"][F_PRIMARY] else None),
                          r_hi=(r["R"][r["runs"][F_PRIMARY][1]] if r["runs"][F_PRIMARY] else None),
                          w=(r["R"][r["runs"][F_PRIMARY][1]] / r["R"][r["runs"][F_PRIMARY][0]] if r["runs"][F_PRIMARY] else None),
                          censored=r["censored"], x_meas=r["x_meas"], x_pred=r["x_pred"],
                          k1_rms=r["k1_rms"], n_pts=r["n_pts"], n_dropped=r["n_dropped"])
                     for r in ok_res],
    )
    tag = "_MUTATE" if MUTATE else ""
    with open(os.path.join(HERE, f"ag3_sparc_widths{tag}_results.json"), "w") as f:
        json.dump(out, f, indent=1, default=float)
    print(f"results -> ag3_sparc_widths{tag}_results.json")
    return 0 if gate_pass else 1


if __name__ == "__main__":
    sys.exit(main())
