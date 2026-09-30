#!/usr/bin/env python3
"""CFG192_main -- primary reproduction of CFG182's headline (independent code) and the MUTATE controls.
Run:  python3 CFG192_main.py   (needs CFG192_profiles.npz)      MUTATE=k python3 CFG192_main.py  (k=1..7)
Exit: main 0 (class printed; 2 on internal error); MUTATE: 1 iff the control BITES, else 0.
Outputs CFG192_main.out/.json  (MUTATE: CFG192_MUTATE_k.out/.json).  Frozen criteria: CFG192_FROZEN_CRITERIA.md"""
import os
import sys
import numpy as np
from scipy.stats import chi2 as chi2dist
from CFG192_common import *
import CFG192_common as CC

MUT = int(os.environ.get("MUTATE", "0"))
SEEDS = dict(simple=19201, block=19202, boot=19203, neyman=19204, mut=19211, shuf=19213)
TARGET = dict(N=149, pts=3150, la0=None, a0=1.13e-10, A=0.238, l=237.2, b=-44.2, dchi=10.3, sigA=0.201, cone68=59, cone95=115,
              p_simple=0.772, p_block=0.774, nullmed=0.34, null95=0.62, A95=0.425, fpn=0.60, fp_l=142, fp_b=55)


def inj_dir():
    v = np.random.default_rng(SEEDS["mut"]).normal(size=3)
    return v / np.linalg.norm(v)


def pathf(name):
    return os.path.join(HERE, name)


def analyse(R, d, tag, full=True, nperm=5000, nboot=2000, quiet=False):
    """the primary analysis on a profile bundle; returns a dict of results"""
    b = sub_bundle(d, d["mask"])
    cv, n, C, grid = b["cv"], b["n"], b["C"], b["grid"]
    uma = b["uma"]
    res = dict(b=b)
    F0, la0 = F0_fit(cv)
    fit = fit_dipole(cv, n, starts=5)
    res.update(F0=F0, la0=la0, fit=fit)
    A = fit["A"]
    l, bb = vec_to_lb(fit["D"])
    res.update(A=A, l=l, blat=bb, dchi=F0 - fit["F"])
    hw, best = curve_halfwidth(grid, C)
    res.update(hw=hw, best=best)
    try:
        Cf = fisher_cov(cv, n, fit)
        Cdd = Cf[1:, 1:]
        dh = fit["D"] / np.linalg.norm(fit["D"])
        res.update(Cf=Cf, fisher_along=float(math.sqrt(dh @ Cdd @ dh)), fisher_rms=float(math.sqrt(np.trace(Cdd) / 3)))
    except np.linalg.LinAlgError:
        res.update(Cf=None, fisher_along=float("nan"), fisher_rms=float("nan"))  # singular Hessian (flat curves: the Newtonian control)
    if not quiet:
        R.P(f"  [{tag}] N = {cv.N}, points = {int(b['N'].sum())}; no-dipole a0 = {10 ** la0:.4e} (log {la0:.3f}); chi2(A=0) = {F0:.2f}")
        R.P(f"  [{tag}] best dipole A = {A:.4f} toward (l, b) = ({l:.1f}, {bb:.1f}); log a0bar = {fit['la']:.3f}; Delta chi2 = {F0 - fit['F']:.2f} (3 par); |D| bound hit: {A > 0.949}")
        R.P(f"  [{tag}] Fisher sigma_A along the fitted direction {res['fisher_along']:.3f}; rms component {res['fisher_rms']:.3f}; galaxies clamped at grid edge: {cv.clamped(fit['la'] + np.log10(1 + n @ fit['D']))}")
    return res


def perms_and_boot(R, res, tag, nperm, nboot, hemi=False, scheme_list=("simple", "block")):
    b = res["b"]
    cv, n, C, grid, uma = b["cv"], b["n"], b["C"], b["grid"], b["uma"]
    la0, fit, F0 = res["la0"], res["fit"], res["F0"]
    out = {}
    for sch in scheme_list:
        A, F, D, H = run_perms(cv, n, uma, C, grid, la0, sch, SEEDS[sch], 0, nperm, hemi=hemi and sch == "simple")
        out[sch] = dict(A=A, F=F, D=D, H=H)
        pA = pval(A, fit["A"])
        pL = pval(F0 - F, res["F0"] - fit["F"])
        R.P(f"  [{tag}] permutation ({sch}, N = {nperm}): p_A = {pA:.4f}; null A-hat median {np.median(A):.3f}, 68% {np.quantile(A, .68):.3f}, 95% {np.quantile(A, .95):.3f}; p(Delta chi2) = {pL:.4f}")
        out[sch]["p"] = pA
        out[sch]["pL"] = pL
    res["perm"] = out
    if nboot:
        Db, Ab = run_boot(cv, n, la0, np.arange(cv.N), SEEDS["boot"], 0, nboot, extra=fit["u"])
        res["boot"] = dict(D=Db, A=Ab)
        Cb = np.cov(Db.T)
        res["sigA_std"] = float(np.std(Ab, ddof=1))
        res["sigA_comp"] = float(math.sqrt(np.trace(Cb) / 3))
        dirs = Db / np.linalg.norm(Db, axis=1, keepdims=True)
        res["cone68"] = cone(dirs, fit["D"], 0.68)
        res["cone95"] = cone(dirs, fit["D"], 0.95)
        R.P(f"  [{tag}] bootstrap ({nboot}): std(A-hat) = {res['sigA_std']:.3f}; rms component sigma = {res['sigA_comp']:.3f}; mean A-hat = {Ab.mean():.3f}; cones 68% {res['cone68']:.0f} deg, 95% {res['cone95']:.0f} deg")
        res["Cboot"] = Cb
    return res


# ---------------------------------------------------------------------------------------------------------- MUTATE
def mutate_main(R):
    prim = load_bundle(pathf("CFG192_profiles.npz"))
    file = {1: "CFG192_profiles_MUTATE_1.npz", 2: "CFG192_profiles_MUTATE_2.npz", 3: "CFG192_profiles_MUTATE_1.npz",
            4: "CFG192_profiles_MUTATE_4.npz", 5: "CFG192_profiles_MUTATE_1.npz", 6: "CFG192_profiles_MUTATE_6.npz", 7: "CFG192_profiles.npz"}[MUT]
    d = load_bundle(pathf(file))
    dinj = inj_dir()
    Al, Bl = vec_to_lb(dinj)
    R.P(f"injection direction (seed {SEEDS['mut']}): (l, b) = ({Al:.1f}, {Bl:.1f})")
    bites = False
    if MUT == 7:
        G = load_all()
        P = [prep(g) for g in G if prep(g)["N"] >= 5]
        mx = max(float(np.max(np.abs(inject_point(p, np.zeros(3))["Vobs"] - p["Vobs"]))) for p in P)
        R.P(f"A = 0 injection: max |Delta Vobs| over all points = {mx:.3e} km/s")
        rp = analyse(R, prim, "primary", quiet=True)
        dchg = float(np.linalg.norm(rp["fit"]["D"] - rp["fit"]["D"])) + mx
        bites = dchg > 1e-6
        R.check("M7 zero injection leaves the data untouched (bites only on a pipeline defect)", f"change {dchg:.3e}", not bites)
        R.P(f"MUTATE 7 bites: {bites} (expected False)")
        return R.finish(1 if bites else 0, "M7")
    rp = analyse(R, prim, "primary", quiet=True)
    if MUT in (3, 5):
        # positions shuffled (M3) or negated (M5) in the FIT only
        b = sub_bundle(d, d["mask"])
        bp = sub_bundle(prim, prim["mask"])
        if MUT == 3:
            perm = np.random.default_rng(SEEDS["shuf"]).permutation(b["cv"].N)
            nfit = b["n"][perm]
            R.P("M3: positions shuffled among galaxies (seed 19213) in the fit; injection used the true positions")
        else:
            nfit = -b["n"]
            R.P("M5: fit with n -> -n (sign-convention flip); injection used the true positions")
        fm = fit_dipole(b["cv"], nfit, starts=5)
        fp = fit_dipole(bp["cv"], nfit, starts=5)
        dD = fm["D"] - fp["D"]
        R.P(f"mutated fit (shuffled/negated positions): A = {fm['A']:.3f} at ({vec_to_lb(fm['D'])[0]:.1f}, {vec_to_lb(fm['D'])[1]:.1f}); primary curves, same positions: A = {fp['A']:.3f}")
        R.P(f"change vector: amplitude {np.linalg.norm(dD):.3f}; component along the injected direction {dD @ dinj:.3f}; angle to +injection {ang(dD, dinj):.1f}, to antipode {ang(dD, -dinj):.1f} deg")
        if MUT == 3:
            comp = float(dD @ dinj)
            bites = (comp < 0.10) and (abs(fm["A"] - 0.34) < 0.25)
            R.P(f"M3 bites iff component along injection < 0.10 and |A-hat - 0.34| < 0.25: comp {comp:.3f}, |A - 0.34| = {abs(fm['A'] - 0.34):.3f}")
        else:
            bites = ang(dD, -dinj) <= 25.0
            R.P(f"M5 bites iff the recovered change points within 25 deg of the ANTIPODE: {ang(dD, -dinj):.1f} deg")
        R.check("control result recorded", f"bites = {bites}", True, False)
        R.P(f"MUTATE {MUT} bites: {bites}")
        return R.finish(1 if bites else 0, f"M{MUT}")
    if MUT == 6:
        rm = None   # Newtonian curves are flat in a0: no dipole fit is meaningful (a0 runs away), only the Birge/edge statistics are used
    else:
        rm = analyse(R, d, f"MUTATE {MUT}")
    if MUT in (1, 2):
        Ainj = 0.5 if MUT == 1 else 0.2
        dD = rm["fit"]["D"] - rp["fit"]["D"]
        amp = float(np.linalg.norm(dD))
        an = ang(dD, dinj)
        R.P(f"injected A = {Ainj}; primary fit A = {rp['A']:.3f}; mutated fit A = {rm['A']:.3f}; change vector amplitude {amp:.3f} (recovery {amp / Ainj:.2f}), {an:.1f} deg from the injection; along injection {dD @ dinj:.3f}")
        if MUT == 1:
            A_, F_, D_, _ = run_perms(rm["b"]["cv"], rm["b"]["n"], rm["b"]["uma"], rm["b"]["C"], rm["b"]["grid"], rm["la0"], "simple", SEEDS["simple"], 1, 2000)
            p = pval(A_, rm["fit"]["A"])
            R.P(f"mutated permutation p (N = 2000, simple) = {p:.4f}")
            bites = (0.25 <= amp <= 0.55) and (an <= 25.0) and (p < 0.05)
            R.P(f"M1 bites iff amplitude in [0.25, 0.55] AND angle <= 25 deg AND p < 0.05: amp {amp:.3f} ({0.25 <= amp <= 0.55}), angle {an:.1f} ({an <= 25}), p {p:.4f} ({p < 0.05})")
        else:
            A_, F_, D_, _ = run_perms(rm["b"]["cv"], rm["b"]["n"], rm["b"]["uma"], rm["b"]["C"], rm["b"]["grid"], rm["la0"], "simple", SEEDS["simple"], 2, 2000)
            p = pval(A_, rm["fit"]["A"])
            R.P(f"mutated permutation p (N = 2000, simple) = {p:.4f} (reported, not required)")
            bites = (0.10 <= amp <= 0.27) and (an <= 30.0)
            R.P(f"M2 bites iff amplitude in [0.10, 0.27] AND angle <= 30 deg: amp {amp:.3f}, angle {an:.1f}")
    elif MUT == 4:
        hp = float(np.median(rp["hw"]))
        hm = float(np.median(rm["hw"]))
        Cf_ratio = rp["fisher_rms"] / rm["fisher_rms"]
        R.P(f"median half-width: primary {hp:.3f} dex, fixed nuisances {hm:.3f} dex (ratio {hp / hm:.2f}); Fisher rms sigma_A: primary {rp['fisher_rms']:.3f}, fixed {rm['fisher_rms']:.3f} (ratio {Cf_ratio:.2f})")
        A_, F_, D_, _ = run_perms(rm["b"]["cv"], rm["b"]["n"], rm["b"]["uma"], rm["b"]["C"], rm["b"]["grid"], rm["la0"], "simple", SEEDS["simple"], 4, 2000)
        R.P(f"fixed-nuisance permutation p (N = 2000, simple) = {pval(A_, rm['fit']['A']):.4f}; null A-hat median {np.median(A_):.3f}; Birge median {np.median(rm['b']['s']):.2f}")
        bites = (hp / hm >= 1.5) and (Cf_ratio >= 1.5)
        R.P(f"M4 bites iff half-width shrinks >= 1.5x AND Fisher sigma_A shrinks >= 1.5x: {hp / hm:.2f}, {Cf_ratio:.2f}")
    elif MUT == 6:
        sp = float(np.median(prim["s"][prim["mask"]]))
        sm = float(np.median(d["s"][d["mask"]]))
        kmin = np.argmin(d["chi"][d["mask"]], 1)
        edge = float(np.mean((kmin == 0) | (kmin == len(d["grid"]) - 1)))
        R.P(f"median Birge factor: primary {sp:.2f}, Newtonian {sm:.2f} (ratio {sm / sp:.2f}); fraction with best a0 at a grid edge: {edge:.2f}")
        bites = (sm > 3 * sp) or (edge >= 0.5)
        R.P(f"M6 bites iff Birge > 3x primary or >= 50% at a grid edge")
    R.check("control result recorded", f"bites = {bites}", True, False)
    R.P(f"MUTATE {MUT} bites: {bites}")
    return R.finish(1 if bites else 0, f"M{MUT}")


# ---------------------------------------------------------------------------------------------------------- main
def main():
    if MUT:
        R = Run("CFG192_MUTATE_%d" % MUT)
        R.banner(f"CFG192 MUTATE {MUT}   repo=<repo>")
        return mutate_main(R)
    R = Run("CFG192_main")
    R.banner("CFG192 main: primary reproduction of the CFG182 headline (independent code)   repo=<repo>")
    d = load_bundle(pathf("CFG192_profiles.npz"))
    m = d["mask"]
    R.banner("1. sample")
    R.P(f"usable (>= 5 points) galaxies: {len(m)}; Q <= 2 and Inc >= 30: {int(m.sum())}; points {int(d['N'][m].sum())}")
    R.P("by distance method (f_D: count): " + ", ".join(f"{k}: {int(((d['fD'] == k) & m).sum())}" for k in (1, 2, 3, 4, 5)))
    R.P("all-usable sample size (Q <= 3, no Inc cut): %d" % len(m))
    R.check("sample count = 149 (frozen line)", f"{int(m.sum())}", int(m.sum()) == 149)
    R.check("points = 3150 +/- 30", f"{int(d['N'][m].sum())}", abs(int(d["N"][m].sum()) - 3150) <= 30)
    R.check("method counts 81/37/3/2/26", str([int(((d['fD'] == k) & m).sum()) for k in (1, 2, 3, 5, 4)]), [int(((d['fD'] == k) & m).sum()) for k in (1, 2, 3, 5, 4)] == [81, 37, 3, 2, 26])
    # unit checks of the coordinate conversion
    gc = radec_to_gal(266.405, -28.936)
    ngp = radec_to_gal(192.859, 27.128)
    R.check("coordinates: Galactic centre -> (0, 0) within 0.01 deg", f"({gc[0]:.4f}, {gc[1]:.4f})", (min(gc[0], 360 - gc[0]) < 0.01) and abs(gc[1]) < 0.01)
    R.check("coordinates: NGP -> b = 90 within 0.01 deg", f"b = {ngp[1]:.4f}", abs(ngp[1] - 90) < 0.01)
    b = sub_bundle(d, m)
    f = b["n"].mean(0)
    fl, fb = vec_to_lb(f)
    R.P(f"footprint: |<n>| = {np.linalg.norm(f):.3f} toward (l, b) = ({fl:.0f}, {fb:.0f}); galaxies at b > 0: {int((b['n'][:, 2] > 0).sum())} of {len(b['n'])}")
    R.banner("2. no-dipole and dipole fit")
    res = analyse(R, d, "primary")
    fit = res["fit"]
    cv, n, uma = b["cv"], b["n"], b["uma"]
    R.P(f"Birge factor median {np.median(b['s']):.3f}; Delta chi2 = 1 half-width median {np.median(res['hw']):.3f} dex; per-galaxy best log a0 16/84%: {np.percentile(res['best'], 16):.2f} / {np.percentile(res['best'], 84):.2f}; MAD scatter {1.4826 * np.median(np.abs(res['best'] - np.median(res['best']))):.3f} dex")
    # single-start vs 5-start agreement over 100 permutations; exact recovery
    rng = np.random.default_rng(192)
    dif = 0.0
    for _ in range(100):
        npos = perm_positions(rng, n, uma, "simple")
        r5 = fit_dipole(cv, npos, starts=5)
        r1 = fit_dipole(cv, npos, starts=1, la0=res["la0"])
        dif = max(dif, abs(r5["A"] - r1["A"]))
    R.check("single-start vs 5-start agreement over 100 permutations (max |dA| < 1e-4)", f"{dif:.2e}", dif < 1e-4)
    Dt = np.array([0.15, -0.10, 0.20])
    x0 = -9.95 + np.log10(1 + n @ Dt)
    ex = Curves.quad(cv.grid, x0, np.full(cv.N, 0.2))
    fe = fit_dipole(ex, n, starts=5)
    R.check("no-residual exact recovery (Gaussian curves centred on the model return the injected D to 1e-4)", f"|dD| = {np.linalg.norm(fe['D'] - Dt):.2e}", np.linalg.norm(fe["D"] - Dt) < 1e-4)
    # gradient check
    from scipy.optimize import check_grad
    p0 = np.concatenate([[res["la0"]], [0.1, 0.2, -0.1]])
    gc_ = check_grad(lambda q: CC._obj_u(q, cv, n, "mult", None)[0], lambda q: CC._obj_u(q, cv, n, "mult", None)[1], p0)
    R.check("analytic gradient vs finite differences", f"{gc_:.2e}", gc_ < 1e-3 * max(1, abs(CC._obj_u(p0, cv, n, 'mult', None)[0])))
    R.banner("3. nulls (permutation simple + block, N = 5000) and bootstrap (2000)")
    res = perms_and_boot(R, res, "primary", 5000, 2000, hemi=True)
    R.T("perms+boot done")
    ps, pb = res["perm"]["simple"]["p"], res["perm"]["block"]["p"]
    pA = max(ps, pb)
    Asim = res["perm"]["simple"]["A"]
    R.P(f"pass-line p (larger of simple {ps:.4f} and block {pb:.4f}) = {pA:.4f}")
    # ---------------------------------------------------------------- footprint
    R.banner("4. footprint and cone-free alignment")
    fh = f / np.linalg.norm(f)
    axa = axis_ang(fit["D"], fh)
    R.P(f"angle between the fitted axis and the footprint axis: {axa:.1f} deg (95% bootstrap cone {res['cone95']:.0f} deg; 68% {res['cone68']:.0f})")
    S3_pass = axa > res["cone95"]
    Dperm = res["perm"]["simple"]["D"]
    aperm = np.array([axis_ang(x, fh) for x in Dperm])
    p_align = float((1 + np.sum(aperm <= axa)) / (1 + len(aperm)))
    R.P(f"cone-free alignment statistic: fraction of permuted fits with an axis at least as close to the footprint axis = {p_align:.3f} (median null angle {np.median(aperm):.1f} deg)")
    Cdd = res["Cf"][1:, 1:]
    w_, v_ = np.linalg.eigh(Cdd)
    lc = v_[:, -1]
    R.P(f"Fisher covariance of D: sigma along eigen-axes {np.sqrt(w_[0]):.3f} / {np.sqrt(w_[1]):.3f} / {np.sqrt(w_[2]):.3f}; least-constrained direction (l, b) = ({vec_to_lb(lc)[0]:.0f}, {vec_to_lb(lc)[1]:.0f}), {axis_ang(lc, fh):.1f} deg from the footprint axis, {axis_ang(lc, fit['D']):.1f} deg from the fit")
    Cf = res["Cf"]
    ff = np.concatenate([[0], fh])
    rho = Cf[0, 1:] @ fh / math.sqrt(Cf[0, 0] * (fh @ Cf[1:, 1:] @ fh))
    R.P(f"correlation of (log a0bar, D along the footprint vector) in the Fisher covariance: {rho:.3f}")
    # ---------------------------------------------------------------- distance split (S2)
    R.banner("5. distance-method split (S2), inclination split, fixed directions")
    fD = b["fD"]
    groups = dict(H=np.where(fD == 1)[0], I=np.where(np.isin(fD, (2, 3, 5)))[0], UMa=np.where(fD == 4)[0])
    dsplit = {}
    dfull = fit["D"] / np.linalg.norm(fit["D"])
    for gname, ix in groups.items():
        cvg = cv.sub(ix)
        ng = n[ix]
        F0g, la0g = F0_fit(cvg)
        fg = fit_dipole(cvg, ng, starts=5)
        Db, Ab = run_boot(cvg, ng, la0g, np.arange(len(ix)), SEEDS["boot"], 10 + hash(gname) % 1 + list(groups).index(gname), 1000, extra=fg["u"])
        cf = fit_fixed(cvg, ng, dfull, la0=la0g)
        Dfb, Afb = run_boot(cvg, ng, la0g, np.arange(len(ix)), SEEDS["boot"], 20 + list(groups).index(gname), 500, fixdir=dfull)
        sfix = float(np.std(Afb, ddof=1))
        dsplit[gname] = dict(N=len(ix), A=fg["A"], lb=vec_to_lb(fg["D"]), D=fg["D"], cov=np.cov(Db.T), Afix=cf["s"], sfix=sfix)
        R.P(f"  {gname}: N = {len(ix)}; A = {fg['A']:.3f} toward ({vec_to_lb(fg['D'])[0]:.0f}, {vec_to_lb(fg['D'])[1]:.0f}); along the full-sample direction A_fix = {cf['s']:+.3f} +/- {sfix:.3f} ({cf['s'] / sfix:+.2f} sigma)")
    dd = dsplit["H"]["D"] - dsplit["I"]["D"]
    chi2v = float(dd @ np.linalg.inv(dsplit["H"]["cov"] + dsplit["I"]["cov"]) @ dd)
    p_split = float(chi2dist.sf(chi2v, 3))
    R.P(f"  H vs I vectors: chi2 = {chi2v:.2f} (3 dof), p = {p_split:.3f}")
    S2a = p_split > 0.05
    zH, zI = dsplit["H"]["Afix"] / dsplit["H"]["sfix"], dsplit["I"]["Afix"] / dsplit["I"]["sfix"]
    S2b = (zH >= 1) and (zI >= 1)
    S2_pass = S2a and S2b
    Inc = b["Inc"]
    medI = float(np.median(Inc))
    lo, hi = np.where(Inc <= medI)[0], np.where(Inc > medI)[0]
    fl_, fh_ = [], []
    for ix, tg in ((lo, 30), (hi, 31)):
        cvg, ng = cv.sub(ix), n[ix]
        F0g, la0g = F0_fit(cvg)
        fg = fit_dipole(cvg, ng, starts=5)
        Db, Ab = run_boot(cvg, ng, la0g, np.arange(len(ix)), SEEDS["boot"], tg, 500, extra=fg["u"])
        fl_.append((fg["D"], np.cov(Db.T), fg["A"]))
    ddi = fl_[0][0] - fl_[1][0]
    p_inc = float(chi2dist.sf(ddi @ np.linalg.inv(fl_[0][1] + fl_[1][1]) @ ddi, 3))
    R.P(f"  inclination split at median {medI:.0f} deg: A = {fl_[0][2]:.3f} / {fl_[1][2]:.3f}; vectors differ p = {p_inc:.3f}")
    fixed = {}
    for nm, v in list(DIRS.items()) + [("UMa", (lambda x: x / np.linalg.norm(x))(b["n"][uma].mean(0)))]:
        v = np.asarray(v)
        cf = fit_fixed(cv, n, v, la0=res["la0"])
        Dfb, Afb = run_boot(cv, n, res["la0"], np.arange(cv.N), SEEDS["boot"], 40, 500, fixdir=v)
        sg = float(np.std(Afb, ddof=1))
        fixed[nm] = (cf["s"], sg)
        R.P(f"  fixed direction {nm:6s} ({vec_to_lb(v)[0]:.0f}, {vec_to_lb(v)[1]:.0f}): A_fix = {cf['s']:+.3f} +/- {sg:.3f}; 95% upper end {cf['s'] + 1.96 * sg:.2f}")
    # ---------------------------------------------------------------- hemisphere
    R.banner("6. hemisphere statistic (Zhou-style; 3072-point Fibonacci axes, not HEALPix)")
    Hs = hemi_H(b["C"], b["grid"], n)
    kH = int(np.nanargmax(Hs))
    Hmax = float(Hs[kH])
    Hz = hemi_H_axis(b["C"], b["grid"], n, DIRS["Zhou"])
    He = hemi_H_einsum(b["C"], b["grid"], n)
    R.check("hemisphere scan: matmul vs einsum agree (Accelerate warnings are spurious)", f"max |dH| = {np.nanmax(np.abs(Hs - He)):.2e}", np.nanmax(np.abs(Hs - He)) < 1e-9)
    Hn = res["perm"]["simple"]["H"]
    R.P(f"  H_max = {Hmax:.3f} toward ({vec_to_lb(AXES[kH])[0]:.0f}, {vec_to_lb(AXES[kH])[1]:.0f}); permutation (N = 5000) null median {np.nanmedian(Hn[:, 0]):.3f}, 95% {np.nanquantile(Hn[:, 0], .95):.3f}; p = {pval(Hn[~np.isnan(Hn[:, 0]), 0], Hmax):.3f}")
    Hb = []
    rngh = np.random.default_rng(SEEDS["boot"] + 7)
    for _ in range(500):
        ib = rngh.choice(cv.N, cv.N)
        Hb.append(hemi_H_axis(b["C"][ib], b["grid"], n[ib], DIRS["Zhou"]))
    R.P(f"  at the Zhou axis (175.5, -6.5): H = {Hz:+.3f} +/- {np.nanstd(Hb):.3f} (bootstrap 500); fixed-axis permutation p(H >= obs) = {pval(Hn[~np.isnan(Hn[:, 1]), 1], Hz):.3f}")
    # ---------------------------------------------------------------- PV template and distance trend
    R.banner("7. peculiar-velocity template (Hubble-flow galaxies) and distance trend")
    ixH = groups["H"]
    cvH, nH, DH = cv.sub(ixH), n[ixH], b["D"][ixH]
    H0 = 73.0

    def pv_obj(q, cvx, nx, Dx):
        la, W = q[0], q[1:]
        u = 1.0 - 2.0 * (nx @ W) / (H0 * Dx)
        u = np.maximum(u, 0.05)
        x = la + np.log10(u)
        f_, fp_ = cvx.ev(x)
        dx = (-2.0 * nx / (H0 * Dx)[:, None]) / (u * LN10)[:, None]
        return float(f_.sum()), np.concatenate([[fp_.sum()], (fp_[:, None] * dx).sum(0)])

    def pv_fit(cvx, nx, Dx, la0):
        best = None
        for s in [np.zeros(3), np.array([100., 100, 100]), np.array([-100., 100, -100]), np.array([100., -100, -100]), np.array([-100., -100, 100])]:
            r = minimize(pv_obj, np.concatenate([[la0], s]), args=(cvx, nx, Dx), jac=True, method="L-BFGS-B", options=dict(ftol=1e-15, gtol=1e-9))
            if best is None or r.fun < best.fun:
                best = r
        return best
    F0H, la0H = F0_fit(cvH)
    rp = pv_fit(cvH, nH, DH, la0H)
    Wv = rp.x[1:]
    dchiPV = F0H - rp.fun
    fitH = fit_dipole(cvH, nH, starts=5)
    R.P(f"  Hubble-flow only (N = {len(ixH)}): bulk flow W = {np.linalg.norm(Wv):.0f} km/s toward ({vec_to_lb(Wv)[0]:.0f}, {vec_to_lb(Wv)[1]:.0f}); Delta chi2 = {dchiPV:.2f}; the dipole's Delta chi2 on the same galaxies = {F0H - fitH['F']:.2f}")
    rngp = np.random.default_rng(SEEDS["simple"] + 5)
    dnull = []
    for _ in range(1000):
        nn_ = nH[rngp.permutation(len(nH))]
        rr = pv_fit(cvH, nn_, DH, la0H)
        dnull.append(F0H - rr.fun)
    R.P(f"  PV template permutation p (N = 1000, positions permuted among the Hubble-flow galaxies) = {pval(dnull, dchiPV):.3f}")
    from scipy.optimize import minimize_scalar
    tD = np.log10(b["D"] / 10.0)

    def prof_beta(beta):
        r = fit_dipole(cv, n, starts=3, shift=-beta * tD, la0=res["la0"])
        return r["F"]
    rb = minimize_scalar(prof_beta, bounds=(-1.0, 1.0), method="bounded", options=dict(xatol=1e-4))
    fb_ = fit_dipole(cv, n, starts=5, shift=-rb.x * tD)
    R.P(f"  distance trend: beta = {rb.x:+.3f} dex/dex, Delta chi2 = {fit['F'] - rb.fun:.2f}; the dipole with beta free: A = {fb_['A']:.3f} toward ({vec_to_lb(fb_['D'])[0]:.0f}, {vec_to_lb(fb_['D'])[1]:.0f})")
    # ---------------------------------------------------------------- A95
    R.banner("8. Neyman A95 (random direction), 1000 trials per cell, grid 0-0.9 step 0.025")
    agrid = np.arange(0, 0.9001, 0.025)
    a95 = {}
    for sch in ("simple", "block"):
        T = neyman_table(cv, n, uma, res["la0"], sch, SEEDS["neyman"], agrid, ntr=1000)
        a95[sch], P95 = a95_from_table(T, agrid, fit["A"])
        R.P(f"  {sch}: A95 = {a95[sch]:.3f}; P(A-hat >= {fit['A']:.3f}) at A_inj = 0: {P95[0]:.3f} (the permutation p); monotone: {bool(np.all(np.diff(P95) > -0.03))}")
    A95 = max(a95.values())
    R.T("Neyman done")
    # ---------------------------------------------------------------- class
    R.banner("9. signal lines and class line vs the CFG182 README (targets read, not blind)")
    S1_pass = pA < 0.003
    R.P(f"  S1 (p < 0.003, larger of simple/block): p = {pA:.4f} -> {'PASS' if S1_pass else 'FAIL'}")
    R.P(f"  S2 (H/I vectors agree p > 0.05 AND A_fix >= 1 sigma in both): p = {p_split:.3f}, z_H = {zH:+.2f}, z_I = {zI:+.2f} -> {'PASS' if S2_pass else 'FAIL'}")
    R.P(f"  S3 (footprint axis outside the 95% cone): axis angle {axa:.1f} vs cone {res['cone95']:.0f} -> {'PASS' if S3_pass else 'FAIL'}")
    verdict = "SIGNAL" if (S1_pass and S2_pass and S3_pass) else "NULL"
    R.P(f"  verdict: {verdict}")
    rows = []

    def row(name, mine, tgt, tol, unit=""):
        ok = abs(mine - tgt) <= tol
        rows.append((name, mine, tgt, tol, ok))
        R.P(f"  {'OK ' if ok else 'MISS'} {name}: mine {mine:.4g}  README {tgt:.4g}  (tol {tol}{unit})")
        return ok
    row("A-hat", fit["A"], 0.238, 0.03)
    dirang = ang(fit["D"], lb_to_vec(237.2, -44.2))
    rows.append(("direction angle (deg)", dirang, 0.0, 15.0, dirang <= 15.0))
    R.P(f"  {'OK ' if dirang <= 15 else 'MISS'} direction: mine ({res['l']:.1f}, {res['blat']:.1f}), README (237.2, -44.2): {dirang:.1f} deg apart (tol 15)")
    row("p_A (larger of simple, block)", pA, 0.774, 0.05)
    row("a0bar (1e-10)", 10 ** res["la0"] / 1e-10, 1.13, 0.0565)
    row("sigma_A bootstrap std(A-hat)", res["sigA_std"], 0.201, 0.03)
    row("sigma_A bootstrap rms component (alternative definition)", res["sigA_comp"], 0.201, 0.03)
    row("null median", float(np.median(Asim)), 0.34, 0.03)
    row("null 95%", float(np.quantile(Asim, .95)), 0.62, 0.05)
    row("A95", A95, 0.425, 0.06)
    row("Delta chi2 (3 par)", res["dchi"], 10.3, 1.0)
    row("cone 68%", res["cone68"], 59, 10)
    row("cone 95%", res["cone95"], 115, 15)
    R.num("summary", dict(N=int(cv.N), A=fit["A"], l=res["l"], b=res["blat"], dchi=res["dchi"], pA=pA, ps=ps, pb=pb, sigA_std=res["sigA_std"],
                          sigA_comp=res["sigA_comp"], A95=A95, a95=a95, p_split=p_split, zH=zH, zI=zI, axa=axa, cone95=res["cone95"], cone68=res["cone68"],
                          verdict=verdict, S1=S1_pass, S2=S2_pass, S3=S3_pass, p_align=p_align, fixed=fixed, Hmax=Hmax, Hz=Hz, dchiPV=dchiPV,
                          Wpv=float(np.linalg.norm(Wv)), beta=float(rb.x), p_inc=p_inc))
    sample_ok = int(m.sum()) == 149
    same_verdict = (verdict == "NULL") and (not S1_pass) and (not S2_pass) and (not S3_pass)
    classified = [r for r in rows if "alternative" not in r[0]]
    core_rows = [r for r in classified if r[0] in ("A-hat", "direction angle (deg)", "p_A (larger of simple, block)", "a0bar (1e-10)", "sigma_A bootstrap std(A-hat)", "null median", "null 95%", "A95")]
    missed = [r[0] for r in core_rows if not r[4]]
    if (not same_verdict) or abs(pA - 0.774) > 0.15 or abs(fit["A"] - 0.238) > 0.10 or abs(int(m.sum()) - 149) > 2 or abs(A95 - 0.425) > 0.15:
        cls = "DISAGREES"
    elif sample_ok and not missed:
        cls = "REPRODUCES"
    elif sample_ok and missed == ["direction angle (deg)"]:
        cls = "PARTIAL-DIRECTION"
    else:
        cls = "PARTIAL"
    R.P(f"\n  CLASS: {cls}   (misses among the core rows: {missed}; among all classified rows: {[r[0] for r in classified if not r[4]]})")
    R.num("class", cls)
    return R.finish(0, f"class {cls}")


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        import traceback
        traceback.print_exc()
        sys.exit(2)
