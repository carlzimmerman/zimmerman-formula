#!/usr/bin/env python3
"""CFG192_attacks_AB -- attack A (clean sample and leave-out) and attack B (nuisance profiling vs simpler treatments).
Frozen: CFG192_FROZEN_CRITERIA.md section 6.  Variants use N_perm = 1000, N_boot = 500 (grid step 0.02 for rebuilds).
Needs CFG192_profiles.npz.  Exit 0 (2 on error).  Outputs CFG192_attacks_AB.out/.json"""
import os
import sys
import numpy as np
from scipy.stats import spearmanr
from CFG192_common import *
import CFG192_common as CC

SEEDS = dict(simple=19201, boot=19203)
IDX = [100]


def nxt():
    IDX[0] += 1
    return IDX[0]


def variant(R, name, d, m, out, nperm=1000, nboot=500, scale=None):
    """d: bundle; m: mask over all usable galaxies"""
    b = sub_bundle(d, m)
    o = dip_stats(b["cv"], b["n"], b["uma"], b["C"], b["grid"], nxt(), nperm, nboot)
    R.P("  " + fmt_stats(o, name))
    out[name] = {k: v for k, v in o.items() if k in ("N", "A", "lb", "dchi", "p", "fisher_rms", "sig_std", "sig_comp", "null_med")}
    return o, b


def main():
    R = Run("CFG192_attacks_AB")
    R.banner("CFG192 attacks A and B   repo=<repo>")
    d = load_bundle(os.path.join(HERE, "CFG192_profiles.npz"))
    allm = np.ones(len(d["N"]), bool)
    Q, Inc, fD, N = d["Q"], d["Inc"], d["fD"], d["N"]
    lat = np.array([x[1] for x in d["lb"]])
    hasb = d["has_bul"]
    prim = (Q <= 2) & (Inc >= 30)
    res = {}
    # ------------------------------------------------------------------------------------- A1
    R.banner("A1. sample ladder (Birge scaling, LML profiles as primary; N_perm 1000, N_boot 500)")
    ladder = {
        "primary Q<=2, Inc>=30": prim,
        "Q=1 only, Inc>=30": (Q <= 1) & (Inc >= 30),
        "Q<=2, Inc>=45": (Q <= 2) & (Inc >= 45),
        "Q<=2, Inc>=60": (Q <= 2) & (Inc >= 60),
        "Q<=2, no Inc cut": (Q <= 2),
        "Q<=3, no Inc cut (all usable)": allm,
        "primary, >= 10 points": prim & (N >= 10),
        "primary, drop UMa": prim & (fD != 4),
        "primary, drop Hubble-flow": prim & (fD != 1),
        "primary, drop TRGB/Ceph/SNIa": prim & ~np.isin(fD, (2, 3, 5)),
        "primary, drop bulge galaxies": prim & ~hasb,
        "primary, |b| > 10": prim & (np.abs(lat) > 10),
    }
    A1 = {}
    for nm, m in ladder.items():
        variant(R, nm, d, m, A1)
    res["A1"] = A1
    min_p = min(v["p"] for v in A1.values())
    R.P(f"  smallest p_perm over the {len(A1)} sample cells: {min_p:.3f}; largest A-hat {max(v['A'] for v in A1.values()):.3f}")
    R.P(f"  A1 verdict: {'SAMPLE-DEPENDENT (a cell has p < 0.01; look-elsewhere count %d)' % len(A1) if min_p < 0.01 else 'NULL ROBUST across the ladder (no cell p < 0.01)'}")
    # ------------------------------------------------------------------------------------- A2 jackknife
    R.banner("A2. leave-one-galaxy-out jackknife and pull-based removal")
    b = sub_bundle(d, prim)
    cv, n = b["cv"], b["n"]
    F0, la0 = F0_fit(cv)
    fit = fit_dipole(cv, n, starts=5)
    setW(cv=cv, n=n, la0=la0)
    jk = []
    for i in range(cv.N):
        keep = np.delete(np.arange(cv.N), i)
        r = fit_dipole(cv.sub(keep), n[keep], starts=3, la0=la0)
        jk.append(r["D"] - fit["D"])
    jk = np.array(jk)
    shift = np.linalg.norm(jk, axis=1)
    order = np.argsort(-shift)
    R.P(f"  largest single-galaxy shifts of D-hat: " + ", ".join(f"{b['names'][i]} {shift[i]:.3f}" for i in order[:5]))
    R.P(f"  max shift {shift.max():.3f}; median {np.median(shift):.4f}")
    hw, best = curve_halfwidth(b["grid"], b["C"])
    xmod = fit["la"] + np.log10(1 + n @ fit["D"])
    pull = (best - xmod) / hw
    tau_pull = np.abs(pull)
    R.P(f"  |pull| (curve-only widths) > 3: {int((tau_pull > 3).sum())} of {cv.N}; > 2: {int((tau_pull > 2).sum())}")
    keep10 = np.setdiff1d(np.arange(cv.N), order[:10])
    o1 = dip_stats(cv.sub(keep10), n[keep10], b["uma"][keep10], b["C"][keep10], b["grid"], nxt(), 1000, 500)
    R.P("  " + fmt_stats(o1, "drop 10 most influential"))
    keepP = np.setdiff1d(np.arange(cv.N), np.argsort(-tau_pull)[:10])
    o2 = dip_stats(cv.sub(keepP), n[keepP], b["uma"][keepP], b["C"][keepP], b["grid"], nxt(), 1000, 500)
    R.P("  " + fmt_stats(o2, "drop 10 largest |pull|"))
    res["A2"] = dict(max_shift=float(shift.max()), top5=[(str(b["names"][i]), float(shift[i])) for i in order[:5]], drop_infl=dict(A=o1["A"], p=o1["p"]),
                     drop_pull=dict(A=o2["A"], p=o2["p"]), npull3=int((tau_pull > 3).sum()))
    # ------------------------------------------------------------------------------------- A3 sky sectors
    R.banner("A3. remove each of 12 equal-area sky sectors (nearest of 12 Fibonacci centres)")
    cen = fib_sphere(12)
    lab = np.argmax(np.einsum('gk,ak->ga', n, cen), axis=1)
    A3 = []
    for s in range(12):
        m = lab != s
        if m.sum() == cv.N or m.sum() < 20:
            continue
        ix = np.where(m)[0]
        o = dip_stats(cv.sub(ix), n[ix], b["uma"][ix], b["C"][ix], b["grid"], nxt(), 500, 0, fisher=False)
        A3.append((s, int((~m).sum()), o["A"], o["lb"], o["p"]))
        R.P(f"  remove sector {s:2d} ({(~m).sum():3d} galaxies): A = {o['A']:.3f} toward ({o['lb'][0]:.0f}, {o['lb'][1]:+.0f}); p = {o['p']:.3f}")
    dirsA3 = np.array([lb_to_vec(*x[3]) for x in A3])
    R.P(f"  A-hat range {min(x[2] for x in A3):.3f}-{max(x[2] for x in A3):.3f}; max angle between sector-removed directions {max(ang(a, c) for a in dirsA3 for c in dirsA3):.0f} deg; min p {min(x[4] for x in A3):.3f}")
    res["A3"] = [(x[0], x[1], x[2], x[4]) for x in A3]
    # ------------------------------------------------------------------------------------- B: rebuilds at step 0.02
    R.banner("B. nuisance treatments (each rebuilt at grid step 0.02 for the 149 primary galaxies)")
    G = load_all()
    Pall = {g["name"]: prep(g) for g in G}
    names = list(d["names"][prim])
    P = [Pall[str(nm)] for nm in names]
    idxP = np.where(prim)[0]
    B = {}
    cfgs = {
        "P02 primary, step 0.02": make_cfg(step=0.02),
        "B1 fixed nuisances": make_cfg(step=0.02, prof=()),
        "B2 profile Y only": make_cfg(step=0.02, prof=("Yd", "Yb")),
        "B3 profile D and Inc only": make_cfg(step=0.02, prof=("D", "i")),
        "B4a Y sigma 0.2 dex": make_cfg(step=0.02, sY=0.2),
        "B4b Y sigma 0.3 dex": make_cfg(step=0.02, sY=0.3),
        "B4c D, Inc sigma x2": make_cfg(step=0.02, mD=2.0, mI=2.0),
        "B4d all looser (Y 0.2, D/Inc x2)": make_cfg(step=0.02, sY=0.2, mD=2.0, mI=2.0),
        "B4e Y sigma 0.05 dex (tighter)": make_cfg(step=0.02, sY=0.05),
        "B7e e_V x sin(i)/sin(i')": make_cfg(step=0.02, evsin=True),
    }
    prof_cache = {}
    for nm, cfg in cfgs.items():
        pr = build_profiles(P, cfg)
        R.T(nm)
        prof_cache[nm] = pr
        sc = birge(pr["chi"], pr["N"])
        C = pr["chi"] / sc[:, None]
        cvx = Curves(pr["grid"], C)
        nx = np.array([p["n"] for p in P])
        umax = np.array([p["fD"] == 4 for p in P])
        o = dip_stats(cvx, nx, umax, C, pr["grid"], nxt(), 1000, 500)
        hwx, _ = curve_halfwidth(pr["grid"], C)
        R.P("  " + fmt_stats(o, nm) + f" hw_med={np.median(hwx):.3f} birge_med={np.median(sc):.2f}")
        B[nm] = dict(A=o["A"], lb=o["lb"], p=o["p"], fisher=o.get("fisher_rms"), sig_std=o["sig_std"], sig_comp=o["sig_comp"], hw=float(np.median(hwx)),
                     birge=float(np.median(sc)), null_med=o["null_med"])
    pr1 = prof_cache["B1 fixed nuisances"]
    # Birge variants on the fixed-nuisance and on the primary (0.01) curves
    R.banner("B1/B7 Birge variants (fixed-nuisance step-0.02 curves and primary step-0.01 curves)")
    for lab_, prx in (("fixed", pr1), ("primary", dict(grid=d["grid"], chi=d["chi"][prim], chiv=d["chiv"][prim], N=d["N"][prim]))):
        for mode, cap in (("none", None), ("vel", None), ("dofN", None), ("primary", 3.0)):
            sc = birge(prx["chi"], prx["N"], mode, prx["chiv"], cap)
            C = prx["chi"] / sc[:, None]
            cvx = Curves(prx["grid"], C)
            nx = np.array([p["n"] for p in P])
            umax = np.array([p["fD"] == 4 for p in P])
            o = dip_stats(cvx, nx, umax, C, prx["grid"], nxt(), 1000, 500)
            nm = f"{lab_} Birge {mode}{' cap3' if cap else ''}"
            R.P("  " + fmt_stats(o, nm))
            B[nm] = dict(A=o["A"], lb=o["lb"], p=o["p"], fisher=o.get("fisher_rms"), sig_std=o["sig_std"], sig_comp=o["sig_comp"], null_med=o["null_med"])
    # ------------------------------------------------------------------------------------- B5
    R.banner("B5. simple per-galaxy a0 fit (fixed nuisances) + regression of log a0_i on log10(1 + D.n_i)")
    d01 = make_cfg(step=0.01, prof=())
    pr01 = build_profiles(P, d01)
    sc = birge(pr01["chi"], pr01["N"])
    hw5, best5 = curve_halfwidth(pr01["grid"], pr01["chi"] / sc[:, None])
    hw5 = np.maximum(hw5, 0.01)
    nx = np.array([p["n"] for p in P])
    umax = np.array([p["fD"] == 4 for p in P])
    grid5 = np.arange(-12.5, -8.0001, 0.01)
    for lab_, sig in (("weighted (1/hw^2)", hw5), ("unweighted", np.ones(len(P)))):
        cvq = Curves.quad(grid5, best5, sig)
        Cq = None
        F0q, la0q = F0_fit(cvq)
        fq = fit_dipole(cvq, nx, starts=5)
        Cf = fisher_cov(cvq, nx, fq)
        A_, F_, D_, _ = run_perms(cvq, nx, umax, None, None, la0q, "simple", SEEDS["simple"], nxt(), 1000, chunk=50)
        Db, Ab = run_boot(cvq, nx, la0q, np.arange(len(P)), SEEDS["boot"], nxt(), 500, chunk=50, extra=fq["u"])
        sc_ = float(np.sqrt(np.trace(Cf[1:, 1:]) / 3))
        # for the weighted case chi2 units are Delta chi2 = 1 <-> 1 sigma; for the unweighted regression the Fisher is in units of sigma_i = 1 dex: rescale by the residual scatter
        resid = best5 - (fq["la"] + np.log10(1 + nx @ fq["D"]))
        if lab_ == "unweighted":
            sc_ *= float(np.std(resid))
        R.P(f"  {lab_:20s}: A = {fq['A']:.3f} toward ({vec_to_lb(fq['D'])[0]:.0f}, {vec_to_lb(fq['D'])[1]:+.0f}); Fisher rms sigma {sc_:.3f}; bootstrap std/comp {np.std(Ab, ddof=1):.3f}/{np.sqrt(np.trace(np.cov(Db.T)) / 3):.3f}; permutation p = {pval(A_, fq['A']):.3f}; scatter of residuals {np.std(resid):.3f} dex")
        B["B5 " + lab_] = dict(A=fq["A"], lb=vec_to_lb(fq["D"]), p=pval(A_, fq["A"]), fisher=sc_, sig_std=float(np.std(Ab, ddof=1)), sig_comp=float(np.sqrt(np.trace(np.cov(Db.T)) / 3)))
    # ------------------------------------------------------------------------------------- B6 random effects
    R.banner("B6. random-effects likelihood on the primary Birge-scaled curves (fitted tau)")
    b = sub_bundle(d, prim)
    Cs, g = b["C"], b["grid"]
    cmin = Cs.min(1)
    Wl = np.exp(-(Cs - cmin[:, None]) / 2.0)
    h = g[1] - g[0]
    nb = b["n"]

    def nll(q, nx_, D_fixed=None):
        la, tau = q[0], q[-1]
        D = q[1:4] if D_fixed is None else D_fixed
        x0 = la + np.log10(np.maximum(1 + nx_ @ D, 1e-3))
        K = np.exp(-0.5 * ((g[None, :] - x0[:, None]) / tau) ** 2) / (tau * math.sqrt(2 * math.pi))
        L = (Wl * K).sum(1) * h
        return float(np.sum(cmin - 2 * np.log(np.maximum(L, 1e-300))))

    def fit_re(nx_, nstart=3):
        best = None
        for s in [np.zeros(3), 0.2 * np.array([1, 1, 1.]), 0.2 * np.array([-1, 1, -1.])][:nstart]:
            q0 = np.concatenate([[-9.95], s, [0.3]])
            r = minimize(nll, q0, args=(nx_,), method="L-BFGS-B", bounds=[(-11, -9), (-.95, .95), (-.95, .95), (-.95, .95), (0.03, 1.5)],
                         options=dict(ftol=1e-13, gtol=1e-8))
            if best is None or r.fun < best.fun:
                best = r
        return best

    def fit_re0():
        r = minimize(lambda q: nll(np.array([q[0], 0, 0, 0, q[1]]), nb, D_fixed=np.zeros(3)), [-9.95, 0.3], method="L-BFGS-B",
                     bounds=[(-11, -9), (0.03, 1.5)], options=dict(ftol=1e-13, gtol=1e-8))
        return r
    r0 = fit_re0()
    r1 = fit_re(nb, 3)
    Dre = r1.x[1:4]
    LR = r0.fun - r1.fun
    R.P(f"  A = 0: tau = {r0.x[1]:.3f} dex, log a0 = {r0.x[0]:.3f}; with dipole: A = {np.linalg.norm(Dre):.3f} toward ({vec_to_lb(Dre)[0]:.0f}, {vec_to_lb(Dre)[1]:+.0f}); tau = {r1.x[4]:.3f}; LR = {LR:.2f}")

    def re_worker(a):
        seedss, nper = a
        rng = np.random.default_rng(seedss)
        out = []
        for _ in range(nper):
            npos = nb[rng.permutation(len(nb))]
            r = fit_re(npos, 2)
            out.append((np.linalg.norm(r.x[1:4]), r0.fun - r.fun))
        return out
    ss = np.random.SeedSequence([SEEDS["simple"], 777]).spawn(20)
    outp = pmap_local(re_worker, [(s, 15) for s in ss])
    outp = np.array([x for chunk in outp for x in chunk])
    pRE = pval(outp[:, 1], LR)
    pREA = pval(outp[:, 0], np.linalg.norm(Dre))
    R.P(f"  permutation (N = 300): p(LR) = {pRE:.3f}; p(A-hat) = {pREA:.3f}; null A-hat median {np.median(outp[:, 0]):.3f}")
    B["B6 random effects"] = dict(A=float(np.linalg.norm(Dre)), lb=vec_to_lb(Dre), tau=float(r1.x[4]), tau0=float(r0.x[1]), LR=float(LR), p=float(pRE), pA=float(pREA))
    # ------------------------------------------------------------------------------------- B8 diagnostics
    R.banner("B8. degeneracy diagnostics on the primary (step-0.01) profile")
    ixP = np.where(prim)[0]
    kmin = np.argmin(d["chi"][ixP], axis=1)
    th = d["theta"][ixP][np.arange(len(ixP)), kmin]  # lYd, lYb, Dp, ip at the per-galaxy minimum
    Dcat, eD, Inc_, eInc = d["D"][ixP], d["eD"][ixP], d["Inc"][ixP], d["eInc"][ixP]
    hw8, best8 = curve_halfwidth(d["grid"], d["chi"][ixP] / d["s"][ixP][:, None])
    pY = (th[:, 0] - np.log10(0.5)) / 0.1
    pDn = (th[:, 2] - Dcat) / eD
    pI = (th[:, 3] - Inc_) / eInc
    sp = lambda a, c: spearmanr(a, c)
    R.P(f"  Spearman(best log a0, log D) = {sp(best8, np.log10(Dcat))[0]:+.2f} (p {sp(best8, np.log10(Dcat))[1]:.3f}); with Inc = {sp(best8, Inc_)[0]:+.2f} (p {sp(best8, Inc_)[1]:.3f}); with Y_d pull = {sp(best8, pY)[0]:+.2f}; D pull = {sp(best8, pDn)[0]:+.2f}; i pull = {sp(best8, pI)[0]:+.2f}")
    lb_ = dict(lYd=(np.log10(0.05), np.log10(3.0)), Dp=(0.2 * Dcat, 3 * Dcat), ip=(5.0, 90.0))
    atY = np.mean((th[:, 0] <= np.log10(0.05) + 1e-3) | (th[:, 0] >= np.log10(3.0) - 1e-3))
    atD = np.mean((th[:, 2] <= 0.2 * Dcat + 1e-3) | (th[:, 2] >= 3 * Dcat - 1e-3))
    atI = np.mean((th[:, 3] <= 5.0 + 1e-3) | (th[:, 3] >= 90.0 - 1e-3))
    R.P(f"  fraction of galaxies with a nuisance at its bound at the minimum: Y_d {atY:.2f}, D {atD:.2f}, i {atI:.2f}")
    R.P(f"  median |pull|: Y_d {np.median(np.abs(pY)):.2f}, D {np.median(np.abs(pDn)):.2f}, i {np.median(np.abs(pI)):.2f}; fraction with |pull| > 2: {np.mean(np.abs(pY) > 2):.2f}, {np.mean(np.abs(pDn) > 2):.2f}, {np.mean(np.abs(pI) > 2):.2f}")
    # slope of ln D' with log a0 across the grid near the minimum (the a0-distance degeneracy)
    sl = []
    for j, i in enumerate(ixP):
        k = kmin[j]
        if 2 <= k < len(d["grid"]) - 2:
            sl.append((np.log(d["theta"][i, k + 2, 2]) - np.log(d["theta"][i, k - 2, 2])) / (d["grid"][k + 2] - d["grid"][k - 2]))
    R.P(f"  median d ln D' / d log10 a0 along the profile near the minimum = {np.median(sl):+.3f} (a0 <-> D degeneracy: at fixed data the deep-regime law V^2 ∝ a0^(1/2) D' gives a0 ∝ D'^-2, i.e. -1.15 for full degeneracy; the prior on D' pulls the profile away from it)")
    res["B8"] = dict(atY=float(atY), atD=float(atD), atI=float(atI), slope_lnD=float(np.median(sl)))
    res["B"] = B
    # ------------------------------------------------------------------------------------- verdicts
    R.banner("Verdicts (frozen meaning)")
    psB = {k: v["p"] for k, v in B.items() if "p" in v and isinstance(v["p"], float)}
    R.P("  B p-values (permutation): " + "; ".join(f"{k}: {v:.3f}" for k, v in psB.items()))
    surv = all(v > 0.05 for v in psB.values())
    dep = any(v < 0.01 for v in psB.values())
    R.P(f"  NULL SURVIVES iff p > 0.05 in all B cells: {surv}; NUISANCE-DEPENDENT (any p < 0.01): {dep}; smallest p {min(psB.values()):.3f} ({min(psB, key=psB.get)})")
    fx = B["B1 fixed nuisances"]["fisher"]
    prim_boot = B["P02 primary, step 0.02"]["sig_comp"]
    b5w = B["B5 weighted (1/hw^2)"]["fisher"]
    fxb = B["B1 fixed nuisances"]["sig_comp"]
    R.P(f"  like-for-like (bootstrap vs bootstrap, rms component): fixed nuisances {fxb:.3f} vs profiled {prim_boot:.3f} (ratio {prim_boot / fxb:.2f}): the bootstrap error does NOT shrink when the nuisances are fixed; the frozen literal rule below compares a fixed-nuisance FISHER error with a profiled BOOTSTRAP error and so overstates it")
    R.P(f"  '5x errors' claim (frozen literal rule): fixed-nuisance Fisher sigma {fx:.3f} vs profiled bootstrap sigma {prim_boot:.3f} (ratio {prim_boot / fx:.1f}); B5 weighted Fisher {b5w:.3f}; published-size (<= 0.08) reachable: {b5w <= 0.08}; confirmed iff ratio >= 2 and reachable: {prim_boot / fx >= 2 and b5w <= 0.08}")
    R.num("results", res)
    return R.finish(0)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        import traceback
        traceback.print_exc()
        sys.exit(2)
