#!/usr/bin/env python3
"""CFG192_attacks_CD -- attack C (footprint response and injection on mock skies) and attack D (the 95% upper limit).
Frozen: CFG192_FROZEN_CRITERIA.md section 6.  Needs CFG192_profiles.npz.  Exit 0 (2 on error).
Outputs CFG192_attacks_CD.out/.json.  Seeds: injection mocks 19205, synthetic 19206, directions 19214, Neyman 19204 (+0,1,2)."""
import os
import sys
import numpy as np
from scipy.stats import ncx2
from scipy.optimize import brentq
from CFG192_common import *
import CFG192_common as CC

S_INJ, S_SYN, S_DIR, S_NEY = 19205, 19206, 19214, 19204
AINJ = (0.1, 0.2, 0.3, 0.5)


def dirs_for(ia, n):
    return rand_dirs(np.random.default_rng(np.random.SeedSequence([S_DIR, ia])), n)


# ----------------------------------------------------------------------------------------------- workers (module level)
def _w_nested(a):
    ss, dirs, Ainj, nperm = a
    rng = np.random.default_rng(ss)
    cv, n, uma, la0 = CC._W["cv"], CC._W["n"], CC._W["uma"], CC._W["la0"]
    pv = np.empty(len(dirs))
    Am = np.empty(len(dirs))
    for k in range(len(dirs)):
        npos = perm_positions(rng, n, uma, "simple")
        sh = np.log10(1.0 + npos @ (Ainj * dirs[k]))          # injection attached to each galaxy's curve
        r = fit_dipole(cv, npos, starts=1, shift=sh, la0=la0 + float(sh.mean()))
        Am[k] = r["A"]
        cnt = 0
        for _ in range(nperm):
            n2 = npos[rng.permutation(len(npos))]
            r2 = fit_dipole(cv, n2, starts=1, shift=sh, la0=la0 + float(sh.mean()))
            cnt += r2["A"] >= r["A"]
        pv[k] = (1 + cnt) / (1 + nperm)
    return Am, pv


def _w_syn2(a):
    ss, Ainj, ntr = a
    rng = np.random.default_rng(ss)
    n, hw, la, tau, grid = CC._W["n"], CC._W["hw"], CC._W["la_true"], CC._W["tau"], CC._W["grid"]
    N = len(n)
    out = np.empty((ntr, 4))
    for k in range(ntr):
        npos = n[rng.integers(0, N, N)]
        d = rand_dirs(rng, 1)[0]
        x = la + np.log10(1 + npos @ (Ainj * d)) + rng.normal(0, hw) + rng.normal(0, tau, N)
        cq = Curves.quad(grid, x, hw)
        r = fit_dipole(cq, npos, starts=1, la0=la)
        out[k, :3] = r["D"]
        out[k, 3] = float(r["D"] @ d)
    return out


def _w_injfix(a):
    ss, dirs, Ainj, dfix = a
    rng = np.random.default_rng(ss)
    cv, n, uma, la0 = CC._W["cv"], CC._W["n"], CC._W["uma"], CC._W["la0"]
    out = np.empty(len(dirs))
    for k in range(len(dirs)):
        npos = perm_positions(rng, n, uma, "simple")
        sh = np.log10(1.0 + npos @ (Ainj * dfix))
        out[k] = fit_fixed(cv, npos, dfix, shift=sh, la0=la0 + float(sh.mean()))["s"]
    return out


def _w_ney2(a):
    ss, Ainj, ntr = a
    rng = np.random.default_rng(ss)
    cv, n, uma, la0 = CC._W["cv"], CC._W["n"], CC._W["uma"], CC._W["la0"]
    out = np.empty((ntr, 2))
    for k in range(ntr):
        d = rand_dirs(rng, 1)[0]
        npos = perm_positions(rng, n, uma, "simple")
        sh = np.log10(1.0 + npos @ (Ainj * d))
        r = fit_dipole(cv, npos, starts=1, shift=sh, la0=la0 + float(sh.mean()))
        F0 = F0_fit(cv, sh)[0]
        out[k] = (r["A"], F0 - r["F"])
    return out


def rec_stats(Dh, dirs, Ainj):
    Ah = np.linalg.norm(Dh, axis=1)
    comp = np.einsum("ij,ij->i", Dh, dirs)
    angs = np.degrees(np.arccos(np.clip(np.einsum("ij,ij->i", Dh / np.maximum(Ah, 1e-12)[:, None], dirs), -1, 1)))
    return dict(meanA=float(Ah.mean()), medA=float(np.median(Ah)), ratio=float(comp.mean() / Ainj) if Ainj else float("nan"),
                med_ang=float(np.median(angs)), ang68=float(np.quantile(angs, .68)), Ah=Ah)


def main():
    R = Run("CFG192_attacks_CD")
    R.banner("CFG192 attacks C and D   repo=<repo>")
    d = load_bundle(os.path.join(HERE, "CFG192_profiles.npz"))
    b = sub_bundle(d, d["mask"])
    cv, n, uma, C, grid = b["cv"], b["n"], b["uma"], b["C"], b["grid"]
    F0, la0 = F0_fit(cv)
    fit = fit_dipole(cv, n, starts=5)
    Aobs = fit["A"]
    R.P(f"primary: N = {cv.N}; A-hat = {Aobs:.4f}; no-dipole log a0 = {la0:.3f}")
    res = {}
    # =========================================================================== C1
    R.banner("C1. analytic footprint response (weights 1/half-width^2 of the Birge-scaled curves)")
    hw, best = curve_halfwidth(grid, C)
    w = 1.0 / hw ** 2
    nbar = (w[:, None] * n).sum(0) / w.sum()
    M = (w[:, None, None] * np.einsum("gi,gj->gij", n, n)).sum(0) - w.sum() * np.outer(nbar, nbar)
    ev, V = np.linalg.eigh(M)
    sig = LN10 / np.sqrt(ev)            # sigma of D along each eigen-axis, la marginalised (chi2 = sum w (x - xhat)^2)
    f = n.mean(0)
    fh = f / np.linalg.norm(f)
    lc = V[:, 0]
    R.P(f"  weighted-footprint sigma_D along the eigen-axes (analytic, curve widths only): {sig[2]:.3f} (best) / {sig[1]:.3f} / {sig[0]:.3f} (worst); ratio worst/best {sig[0] / sig[2]:.2f}")
    R.P(f"  least-constrained direction (analytic): ({vec_to_lb(lc)[0]:.0f}, {vec_to_lb(lc)[1]:+.0f}); {axis_ang(lc, fh):.0f} deg from the footprint axis (142, 54), {axis_ang(lc, fit['D']):.0f} deg from the fit")
    Cf = fisher_cov(cv, n, fit)
    wF, VF = np.linalg.eigh(Cf[1:, 1:])
    R.P(f"  numerical Fisher: sigma along eigen-axes {np.sqrt(wF[0]):.3f} / {np.sqrt(wF[1]):.3f} / {np.sqrt(wF[2]):.3f}; worst direction ({vec_to_lb(VF[:, -1])[0]:.0f}, {vec_to_lb(VF[:, -1])[1]:+.0f}), {axis_ang(VF[:, -1], fh):.0f} deg from the footprint axis")
    rho = Cf[0, 1:] @ fh / math.sqrt(Cf[0, 0] * (fh @ Cf[1:, 1:] @ fh))
    R.P(f"  |<n>| = {np.linalg.norm(f):.3f}; corr(log a0bar, D along the footprint vector) = {rho:+.3f} (Fisher); the footprint vector's own sigma = {math.sqrt(fh @ Cf[1:, 1:] @ fh):.3f} vs best axis {np.sqrt(wF[0]):.3f}")
    res["C1"] = dict(sig_ratio=float(sig[0] / sig[2]), lc_to_foot=float(axis_ang(lc, fh)), rho=float(rho))
    # =========================================================================== C2
    R.banner("C2. curve-level injection on position-permuted real curves (N = 1000 per A_inj; control N = 5000)")
    ctrl_A, _, ctrl_D, _ = run_perms(cv, n, uma, None, None, la0, "simple", S_INJ, 0, 5000)
    thr = {q: float(np.quantile(ctrl_A, q)) for q in (0.95, 0.99, 0.997)}
    R.P(f"  A_inj = 0 control (5000): A-hat median {np.median(ctrl_A):.3f}, mean {ctrl_A.mean():.3f}; 95/99/99.7% thresholds {thr[0.95]:.3f} / {thr[0.99]:.3f} / {thr[0.997]:.3f}")
    C2 = {}
    mocks = {}
    R.P("  A_inj  meanA  medA   recovery(ratio)  ang_med  ang_68   power(>95%)  power(>99%)  power(>99.7%)")
    for ia, Ai in enumerate(AINJ):
        dr = dirs_for(ia, 1000)
        Dh, Ah = run_inj(cv, n, uma, la0, "simple", S_INJ, 10 + ia, dr, Ai)
        st = rec_stats(Dh, dr, Ai)
        pw = [float(np.mean(Ah > thr[q])) for q in (0.95, 0.99, 0.997)]
        C2[Ai] = dict(**{k: v for k, v in st.items() if k != "Ah"}, power95=pw[0], power99=pw[1], power997=pw[2])
        mocks[Ai] = Ah
        R.P(f"  {Ai:4.2f}  {st['meanA']:.3f}  {st['medA']:.3f}    {st['ratio']:.3f}          {st['med_ang']:5.1f}   {st['ang68']:5.1f}     {pw[0]:.3f}        {pw[1]:.3f}        {pw[2]:.3f}")
    res["C2"] = C2
    R.T("C2 done")
    # nested check: p < 0.05 with 499 fresh permutations per mock (200 mocks)
    R.P("  nested detection power: 200 mocks x 499 permutations each, power at p < 0.05 (and at p < 0.01):")
    CC.setW(cv=cv, n=n, uma=uma, la0=la0)
    nested = {}
    for ia, Ai in enumerate(AINJ):
        dr = dirs_for(50 + ia, 200)
        ss = np.random.SeedSequence([S_INJ, 500 + ia]).spawn(20)
        out = pmap(_w_nested, [(ss[c], dr[c * 10:(c + 1) * 10], Ai, 499) for c in range(20)])
        pv = np.concatenate([o[1] for o in out])
        nested[Ai] = (float(np.mean(pv < 0.05)), float(np.mean(pv < 0.01)))
        R.P(f"    A_inj = {Ai}: power(p<0.05) = {nested[Ai][0]:.3f}; power(p<0.01) = {nested[Ai][1]:.3f}")
    res["C2_nested"] = nested
    R.T("nested done")
    # =========================================================================== C3
    R.banner("C3. curve-level injection on the REAL sky realisation (real positions, real curves), N = 1000 per A_inj")
    C3 = {}
    R.P(f"  observed D-hat = ({fit['D'][0]:+.3f}, {fit['D'][1]:+.3f}, {fit['D'][2]:+.3f}), A = {Aobs:.3f}")
    for ia, Ai in enumerate(AINJ):
        dr = dirs_for(ia, 1000)
        Dh, Ah = run_inj(cv, n, uma, la0, None, S_INJ, 60 + ia, dr, Ai)
        chg = Dh - fit["D"]
        ratio = float(np.einsum("ij,ij->i", chg, dr).mean() / Ai)
        C3[Ai] = dict(meanA=float(Ah.mean()), ratio_change=ratio, med_ang_change=float(np.median(np.degrees(np.arccos(np.clip(np.einsum("ij,ij->i", chg / np.maximum(np.linalg.norm(chg, axis=1), 1e-12)[:, None], dr), -1, 1))))))
        R.P(f"  A_inj = {Ai}: mean A-hat {Ah.mean():.3f}; recovery ratio of the CHANGE (D-hat - D_obs).d / A_inj = {ratio:.3f}; median angle of the change to d = {C3[Ai]['med_ang_change']:.1f} deg")
    res["C3"] = C3
    # =========================================================================== C4
    R.banner("C4. form attenuation (the README's explanation of the ~0.77 recovery), curve level, A_inj = 0.3, N = 1000, position-permuted base")
    C4 = {}
    dr = dirs_for(7, 1000)
    for finj, ffit, exp_ in (("mult", "mult", 1.0), ("loglin", "loglin", 1.0), ("mult", "loglin", 1 / LN10), ("loglin", "mult", LN10)):
        Dh, Ah = run_inj(cv, n, uma, la0, "simple", S_INJ, 80, dr, 0.3, form_inj=finj, form_fit=ffit)
        ratio = float(np.einsum("ij,ij->i", Dh, dr).mean() / (0.3 * exp_))
        C4[f"{finj}->{ffit}"] = ratio
        R.P(f"  inject {finj:6s} fit {ffit:6s}: recovery ratio (vs the expected small-amplitude conversion {exp_:.3f} x A_inj) = {ratio:.3f}; mean A-hat {Ah.mean():.3f}")
    # point level on the real sky, 4 tetrahedral directions, A = 0.3, both forms (grid step 0.02)
    R.P("  point level (real positions, injection into V_obs, rebuild at grid step 0.02; recovery of the change vector, 4 tetrahedral directions):")
    G = load_all()
    Pall = {g["name"]: prep(g) for g in G}
    P = [Pall[str(nm)] for nm in b["names"]]
    cfg = make_cfg(step=0.02)
    pr0 = build_profiles(P, cfg)
    sc0 = birge(pr0["chi"], pr0["N"])
    cv0 = Curves(pr0["grid"], pr0["chi"] / sc0[:, None])
    F00, la00 = F0_fit(cv0)
    f0 = fit_dipole(cv0, n, starts=5)
    tet = [np.array(v) / math.sqrt(3) for v in ((1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1))]
    for form in ("mult", "loglin"):
        rats, rats_c = [], []
        for dd in tet:
            Pm = [inject_point(p, 0.3 * dd, form=form) for p in P]
            prm = build_profiles(Pm, cfg)
            scm = birge(prm["chi"], prm["N"])
            cvm = Curves(prm["grid"], prm["chi"] / scm[:, None])
            fm = fit_dipole(cvm, n, starts=5, form=form)
            fb = fit_dipole(cv0, n, starts=5, form=form)
            rats.append(float((fm["D"] - fb["D"]) @ dd / 0.3))
            # curve level on the same data / direction / form
            sh = np.log10(1 + n @ (0.3 * dd)) if form == "mult" else n @ (0.3 * dd)
            fc = fit_dipole(cv0, n, starts=5, form=form, shift=sh)
            rats_c.append(float((fc["D"] - fb["D"]) @ dd / 0.3))
        C4[f"point {form}"] = float(np.mean(rats))
        C4[f"curve same-data {form}"] = float(np.mean(rats_c))
        R.P(f"    form {form:6s}: point-level recovery (mean of 4 dirs) {np.mean(rats):.3f} [{', '.join(f'{x:.2f}' for x in rats)}]; curve-level on the same data {np.mean(rats_c):.3f}")
    res["C4"] = C4
    R.T("C4 done")
    # =========================================================================== C5
    R.banner("C5. footprint dependence: fixed injection directions, position-permuted base, N = 500")
    fdirs = {"footprint axis": fh, "footprint antipode": -fh, "S Galactic pole": lb_to_vec(0, -90), "l=60,b=0": lb_to_vec(60, 0),
             "l=150,b=0": lb_to_vec(150, 0), "l=240,b=0": lb_to_vec(240, 0), "l=330,b=0": lb_to_vec(330, 0), "CMB dipole": DIRS["CMB"]}
    C5 = {}
    for ai, Ai in enumerate((0.3, 0.5)):
        for k, (nm, v) in enumerate(fdirs.items()):
            drs = np.tile(v, (500, 1))
            Dh, Ah = run_inj(cv, n, uma, la0, "simple", S_INJ, 200 + 20 * ai + k, drs, Ai)
            st = rec_stats(Dh, drs, Ai)
            pw = float(np.mean(Ah > thr[0.95])), float(np.mean(Ah > thr[0.997]))
            C5[f"{nm} @ {Ai}"] = dict(ratio=st["ratio"], med_ang=st["med_ang"], power95=pw[0], power997=pw[1])
            R.P(f"  A_inj = {Ai}: {nm:20s}: recovery ratio {st['ratio']:.3f}; median angle {st['med_ang']:5.1f}; power(>95% thr) {pw[0]:.3f}; power(>99.7% thr) {pw[1]:.3f}")
    res["C5"] = C5
    rat5 = [v["ratio"] for v in C5.values()]
    p5 = [v["power95"] for k, v in C5.items() if "@ 0.5" in k]
    R.P(f"  recovery ratio range across directions {min(rat5):.2f}-{max(rat5):.2f}; power(A_inj = 0.5) range {min(p5):.2f}-{max(p5):.2f}")
    # =========================================================================== C6
    R.banner("C6. synthetic mock skies (Gaussian curves with the real half-widths, tau = 0.34 dex intrinsic scatter, positions bootstrapped from the footprint), N = 2000")
    CC.setW(n=n, hw=hw, la_true=la0, tau=0.34, grid=grid)
    C6 = {}
    ctrl6 = None
    for ia, Ai in enumerate((0.0,) + AINJ):
        ss = np.random.SeedSequence([S_SYN, ia]).spawn(20)
        out = pmap(_w_syn2, [(ss[c], Ai, 100) for c in range(20)])
        out = np.concatenate(out)
        Ah = np.linalg.norm(out[:, :3], axis=1)
        if Ai == 0.0:
            ctrl6 = Ah
            t6 = float(np.quantile(Ah, .95)), float(np.quantile(Ah, .997))
            R.P(f"  A_inj = 0: A-hat median {np.median(Ah):.3f}; 95% {t6[0]:.3f}; 99.7% {t6[1]:.3f}")
            C6[0.0] = dict(med=float(np.median(Ah)), q95=t6[0], q997=t6[1])
        else:
            C6[Ai] = dict(meanA=float(Ah.mean()), power95=float(np.mean(Ah > t6[0])), power997=float(np.mean(Ah > t6[1])))
            R.P(f"  A_inj = {Ai}: mean A-hat {Ah.mean():.3f}; power(>95%) {C6[Ai]['power95']:.3f}; power(>99.7%) {C6[Ai]['power997']:.3f}")
    res["C6"] = C6
    R.T("C6 done")
    # ---------------- C verdicts
    R.banner("C verdicts (frozen meaning)")
    c2r = C2[0.3]["ratio"]
    R.P(f"  recovery ratio (C2, mean over A_inj {0.1}-{0.5}) = {np.mean([C2[a]['ratio'] for a in AINJ]):.3f}; per A_inj: " + ", ".join(f"{a}: {C2[a]['ratio']:.2f}" for a in AINJ) + f" (README ~0.77; frozen window [0.6, 0.95])")
    R.P(f"  power at p<0.05 (nested): " + ", ".join(f"{a}: {nested[a][0]:.2f}" for a in AINJ))
    pw3, pw5 = nested[0.3][0], nested[0.5][0]
    R.P(f"  'cannot see a dipole below about 40%' CONFIRMED iff power(0.3) < 0.5 and power(0.5) > 0.2: power(0.3) = {pw3:.2f}, power(0.5) = {pw5:.2f} -> {'CONFIRMED' if (pw3 < 0.5 and pw5 > 0.2) else ('TOO PESSIMISTIC' if pw3 >= 0.5 else 'OPTIMISTIC')}")
    R.P(f"  estimator FOOTPRINT-SENSITIVE iff C5 recovery ratios differ by > 0.15 or power by > 2x between best/worst direction: ratio spread {max(rat5) - min(rat5):.2f}, power ratio {max(p5) / max(min(p5), 1e-9):.2f}")
    # =========================================================================== D
    R.banner("D1. Neyman A95 (random direction): 1000 trials per cell, 3 seeds x (simple, block), grid 0-0.9 step 0.025")
    agrid = np.arange(0, 0.9001, 0.025)
    tabs = {}
    a95s = {}
    for sc_, sch in enumerate(("simple", "block")):
        for sd in range(3):
            T = neyman_table(cv, n, uma, la0, sch, S_NEY + sd, agrid, ntr=1000)
            a95, P95 = a95_from_table(T, agrid, Aobs)
            tabs[(sch, sd)] = T
            a95s[(sch, sd)] = a95
            R.P(f"  {sch:6s} seed {S_NEY + sd}: A95 = {a95:.3f}; P(A-hat >= A_obs | A_inj = 0) = {P95[0]:.3f}; monotone (within 0.03): {bool(np.all(np.diff(P95) > -0.03))}")
    vals = list(a95s.values())
    R.P(f"  A95 over 6 runs: mean {np.mean(vals):.3f}, min {min(vals):.3f}, max {max(vals):.3f}; simple mean {np.mean([v for k, v in a95s.items() if k[0] == 'simple']):.3f}, block mean {np.mean([v for k, v in a95s.items() if k[0] == 'block']):.3f}")
    ag2 = np.arange(0.3, 0.5001, 0.0125)
    Tf = neyman_table(cv, n, uma, la0, "simple", S_NEY + 10, ag2, ntr=1000)
    a95f, Pf = a95_from_table(Tf, ag2, Aobs)
    R.P(f"  finer grid (step 0.0125, 0.30-0.50, simple, new seed): A95 = {a95f:.4f}")
    res["D1"] = dict(a95={f"{k[0]}_{k[1]}": v for k, v in a95s.items()}, fine=a95f)
    # ---- D2 coverage
    R.banner("D2. does the limit procedure cover? (each mock's own A95 from the D1 table; must be >= 0.95)")
    Tref = tabs[("simple", 0)]
    Ts = np.sort(Tref, axis=1)
    ntr = Tref.shape[1]

    def a95_of(x):
        # P(T[a] >= x) for every a via searchsorted
        frac = np.array([1.0 - np.searchsorted(Ts[a], x, side="left") / ntr for a in range(len(agrid))])
        ok = np.where(frac >= 0.95)[0]
        return float(agrid[ok[0]]) if len(ok) else float(agrid[-1]) + 0.025
    cov = {}
    for Ai in AINJ:
        Ah = mocks[Ai]
        lim = np.array([a95_of(x) for x in Ah])
        cov[Ai] = float(np.mean(lim >= Ai))
        R.P(f"  random-direction ensemble, A_true = {Ai}: coverage = {cov[Ai]:.3f}; median mock A95 = {np.median(lim):.3f}")
    res["D2"] = dict(random=cov)
    covfix = {}
    for nm in ("footprint axis", "footprint antipode", "S Galactic pole", "CMB dipole"):
        for Ai in (0.3, 0.5):
            v = fdirs[nm]
            drs = np.tile(v, (500, 1))
            Dh, Ah = run_inj(cv, n, uma, la0, "simple", S_INJ, 200 + 20 * (0 if Ai == 0.3 else 1) + list(fdirs).index(nm), drs, Ai)
            lim = np.array([a95_of(x) for x in Ah])
            covfix[f"{nm} @ {Ai}"] = float(np.mean(lim >= Ai))
            R.P(f"  fixed direction {nm:18s}, A_true = {Ai}: coverage = {covfix[f'{nm} @ {Ai}']:.3f}")
    res["D2"]["fixed"] = covfix
    R.P(f"  verdict: random-direction coverage min {min(cov.values()):.3f} -> {'VALID (>= 0.93)' if min(cov.values()) >= 0.93 else 'NOT VALID (< 0.93)'}; fixed-direction ensembles below 0.90: {[k for k, v in covfix.items() if v < 0.90]}")
    # ---- D3 alternatives
    R.banner("D3. alternative limit definitions next to A95")
    CC.setW(cv=cv, n=n, uma=uma, la0=la0)
    ss = np.random.SeedSequence([S_NEY, 900]).spawn(4)
    dchi_obs = F0 - fit["F"]
    lr_lim = None
    rows = {}
    for ia, Ai in enumerate(agrid[::2]):
        out = pmap(_w_ney2, [(s, float(Ai), 250) for s in np.random.SeedSequence([S_NEY, 950 + ia]).spawn(4)])
        out = np.concatenate(out)
        rows[Ai] = out
    lr_lim = next((float(A) for A in agrid[::2] if np.mean(rows[A][:, 1] >= dchi_obs) >= 0.95), float("nan"))
    R.P(f"  (i) likelihood-ratio ordering (Delta chi2_obs = {dchi_obs:.2f}), grid step 0.05, 1000 trials: limit = {lr_lim:.3f}")
    Db, Ab = run_boot(cv, n, la0, np.arange(cv.N), 19203, 0, 500, chunk=50, extra=fit["u"])
    s_std = float(np.std(Ab, ddof=1))
    s_comp = float(math.sqrt(np.trace(np.cov(Db.T)) / 3))
    R.P(f"  (ii) bootstrap percentile one-sided: A-hat + 1.645 sigma: std definition {Aobs + 1.645 * s_std:.3f}; rms-component definition {Aobs + 1.645 * s_comp:.3f}; 95th percentile of the bootstrap A-hat {np.quantile(Ab, .95):.3f}")
    sg = float(np.median(ctrl_A) / 1.5382)
    Ax = brentq(lambda A: ncx2.sf((Aobs / sg) ** 2, 3, (A / sg) ** 2) - 0.95, 1e-4, 3.0)
    R.P(f"  (iii) Maxwell / noncentral-chi3 with sigma_comp = null-median/1.5382 = {sg:.3f}: A95 = {Ax:.3f}; the permutation null has 95% quantile {thr[0.95]:.3f} vs Maxwell {2.7955 * sg:.3f}")
    spread = max([np.mean(vals), lr_lim, Aobs + 1.645 * s_std, Ax]) - min([np.mean(vals), lr_lim, Aobs + 1.645 * s_std, Ax])
    R.P(f"  spread across (Neyman, i, ii(std), iii) = {spread:.3f} -> {'DEFINITION-DEPENDENT (> 0.15)' if spread > 0.15 else 'consistent (<= 0.15)'}")
    res["D3"] = dict(lr=lr_lim, boot_std=float(Aobs + 1.645 * s_std), boot_comp=float(Aobs + 1.645 * s_comp), maxwell=float(Ax), spread=float(spread))
    # ---- D4 fixed-direction limits and their coverage
    R.banner("D4. direction-specific intervals A_fix +/- 1.96 sigma and their coverage under injection (A_true = 0.3, N = 500; sigma fixed at the observed bootstrap value)")
    D4 = {}
    for k, nm in enumerate(("CMB", "bulk", "Chang", "Zhou", "Virgo")):
        v = DIRS[nm]
        cf = fit_fixed(cv, n, v, la0=la0)
        Dfb, Afb = run_boot(cv, n, la0, np.arange(cv.N), 19203, 300 + k, 500, chunk=50, fixdir=v)
        sgm = float(np.std(Afb, ddof=1))
        CC.setW(cv=cv, n=n, uma=uma, la0=la0)
        ss = np.random.SeedSequence([S_INJ, 700 + k]).spawn(10)
        out = np.concatenate(pmap(_w_injfix, [(s, np.zeros((50, 3)), 0.3, v) for s in ss]))
        ratio = float(out.mean() / 0.3)
        covr = float(np.mean(np.abs(out - 0.3) <= 1.96 * sgm))
        D4[nm] = dict(Afix=cf["s"], sig=sgm, upper=cf["s"] + 1.96 * sgm, recovery=ratio, coverage=covr)
        R.P(f"  {nm:6s}: A_fix = {cf['s']:+.3f} +/- {sgm:.3f}; 95% upper end {cf['s'] + 1.96 * sgm:.2f}; injected 0.3 along it: recovery {ratio:.2f}, interval coverage {covr:.3f}")
    res["D4"] = D4
    R.num("results", res)
    return R.finish(0)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        import traceback
        traceback.print_exc()
        sys.exit(2)
