#!/usr/bin/env python3
"""CFG192_attacks_E -- attack E: what the two published claims would look like in this pipeline (repo files only; the papers'
methods are unknown to this lane).  Frozen: CFG192_FROZEN_CRITERIA.md section 6E.  Needs CFG192_profiles.npz.
Exit 0 (2 on error).  Outputs CFG192_attacks_E.out/.json.  Seeds: perms 19201, boot 19203, injections 19205/19214."""
import os
import sys
import numpy as np
from CFG192_common import *
import CFG192_common as CC

S_P, S_B, S_INJ, S_DIR = 19201, 19203, 19205, 19214
CHANG, ZHOU = DIRS["Chang"], DIRS["Zhou"]


def fixed_fisher(cv, n, dvec, la0):
    """Fisher sigma of the fixed-direction amplitude (la marginalised), chi2 units"""
    cf = fit_fixed(cv, n, dvec, la0=la0)

    def g(p):
        F, gr = CC._obj_raw(np.concatenate([[p[0]], p[1] * dvec]), cv, n, "mult", None)
        return np.array([gr[0], gr[1:] @ dvec])
    q0 = np.array([cf["la"], cf["s"]])
    H = np.zeros((2, 2))
    for k in range(2):
        e = np.zeros(2)
        e[k] = 1e-5
        H[:, k] = (g(q0 + e) - g(q0 - e)) / 2e-5
    H = 0.5 * (H + H.T)
    return float(math.sqrt(2.0 * np.linalg.inv(H)[1, 1]))


def _w_e4(a):
    ss, nm, Ainj, dvec = a
    rng = np.random.default_rng(ss)
    cv, n, uma, la0, C, grid = (CC._W[k] for k in ("cv", "n", "uma", "la0", "C", "grid"))
    out = np.empty((nm, 3))
    for k in range(nm):
        npos = perm_positions(rng, n, uma, "simple")
        sh = np.log10(1.0 + npos @ (Ainj * dvec))
        l0 = la0 + float(sh.mean())
        r = fit_dipole(cv, npos, starts=1, shift=sh, la0=l0)
        rf = fit_fixed(cv, npos, dvec, shift=sh, la0=l0)
        Csh = np.array([np.interp(grid - sh[i], grid, C[i]) for i in range(len(C))])
        out[k] = (r["A"], rf["s"], hemi_H_axis(Csh, grid, npos, dvec))
    return out


def main():
    R = Run("CFG192_attacks_E")
    R.banner("CFG192 attack E: the published claims in this pipeline   repo=<repo>")
    d = load_bundle(os.path.join(HERE, "CFG192_profiles.npz"))
    G = load_all()
    Pall = {g["name"]: prep(g) for g in G}
    allm = np.ones(len(d["N"]), bool)
    prim = d["mask"]
    Pu = [Pall[str(nm)] for nm in d["names"]]
    R.P(f"usable galaxies {len(Pu)}; primary {int(prim.sum())}")
    # fixed-nuisance curves at step 0.01 for all usable galaxies
    prf = build_profiles(Pu, make_cfg(prof=()))
    g01 = prf["grid"]
    variants = {}
    # (a) primary
    sa = d["s"]
    variants["(a) primary: profiled, Birge, 149"] = (d["chi"] / sa[:, None], d["grid"], prim)
    # (b) fixed + Birge
    sb = birge(prf["chi"], prf["N"])
    variants["(b) fixed nuisances, Birge, 149"] = (prf["chi"] / sb[:, None], g01, prim)
    # (c) fixed, no Birge
    variants["(c) fixed nuisances, no Birge, 149"] = (prf["chi"], g01, prim)
    # (f) fixed, no Birge, all usable
    variants["(f) fixed nuisances, no Birge, all 171"] = (prf["chi"], g01, allm)
    # (d),(e) deep-point median estimator
    est, has = [], []
    for p in Pu:
        gb = gfid(p)
        gobs = p["Vobs"] ** 2 * 1e6 / (p["R"] * KPC)
        m = gb < 4e-11
        if m.sum() >= 3:
            est.append(float(np.median(2 * np.log10(gobs[m]) - np.log10(gb[m]))))
            has.append(True)
        else:
            est.append(np.nan)
            has.append(False)
    est, has = np.array(est), np.array(has)
    R.P(f"deep-point estimator (g_bar < 4e-11, >= 3 points): {int(has.sum())} of {len(Pu)} usable galaxies; {int((has & prim).sum())} of the 149; median log a0 = {np.nanmedian(est):.3f}")
    gq = np.arange(-13.0, -8.0001, 0.01)
    Cq_all = ((gq[None, :] - np.where(has, est, 0.0)[:, None]) / 1.0) ** 2
    variants["(d) deep-point median, equal weights, all usable"] = (Cq_all, gq, has)
    variants["(e) deep-point median, equal weights, primary"] = (Cq_all, gq, has & prim)
    out = {}
    nulls = {}
    R.P("\nvariant | N | free dipole A (l,b) [perm p] | A_fix(Chang) +/- boot (Fisher) | H(Zhou axis) +/- boot | p_fixed(A_fix) | p_fixed(H) | H_max, p")
    for k, (_vn, (C, g, m)) in enumerate(variants.items()):
        ix = np.where(m)[0]
        Cm = C[ix]
        cvx = Curves(g, Cm)
        nx = d["n"][ix]
        ux = d["fD"][ix] == 4
        F0, la0 = F0_fit(cvx)
        fit = fit_dipole(cvx, nx, starts=5)
        A_, F_, D_, H_ = run_perms(cvx, nx, ux, Cm, g, la0, "simple", S_P, 300 + k, 1000, chunk=50, hemi=True)
        pfree = pval(A_, fit["A"])
        cf = fit_fixed(cvx, nx, CHANG, la0=la0)
        Db, Ab = run_boot(cvx, nx, la0, np.arange(cvx.N), S_B, 320 + k, 500, chunk=50, fixdir=CHANG)
        sfix = float(np.std(Ab, ddof=1))
        sF = fixed_fisher(cvx, nx, CHANG, la0)
        # perm null of A_fix along Chang
        nul = []
        rng = np.random.default_rng(S_P + k)
        for _ in range(400):
            npos = perm_positions(rng, nx, ux, "simple")
            nul.append(fit_fixed(cvx, npos, CHANG, la0=la0)["s"])
        p_afix = pval(np.array(nul), cf["s"])
        Hz = hemi_H_axis(Cm, g, nx, ZHOU)
        Hs = hemi_H(Cm, g, nx)
        Hmax = float(np.nanmax(Hs))
        # bootstrap H at Zhou axis
        rngh = np.random.default_rng(S_B + k)
        Hb = [hemi_H_axis(Cm[ib], g, nx[ib], ZHOU) for ib in (rngh.choice(cvx.N, cvx.N) for _ in range(500))]
        sH = float(np.nanstd(Hb))
        p_hfix = pval(H_[~np.isnan(H_[:, 1]), 1], Hz)
        p_hmax = pval(H_[~np.isnan(H_[:, 0]), 0], Hmax)
        out[k] = dict(name=list(variants)[k], N=cvx.N, A=fit["A"], lb=vec_to_lb(fit["D"]), pfree=pfree, Afix=cf["s"], sfix=sfix, sFisher=sF, Hz=Hz, sH=sH,
                      p_afix=p_afix, p_hfix=p_hfix, Hmax=Hmax, p_hmax=p_hmax)
        R.P(f"({list(variants)[k]}) N={cvx.N}: A = {fit['A']:.3f} ({vec_to_lb(fit['D'])[0]:.0f},{vec_to_lb(fit['D'])[1]:+.0f}) [p {pfree:.3f}] | A_fix = {cf['s']:+.3f} +/- {sfix:.3f} (Fisher {sF:.3f}) | H = {Hz:+.3f} +/- {sH:.3f} | p_fix(A_fix) {p_afix:.3f} | p_fix(H) {p_hfix:.3f} | H_max {Hmax:.3f} p {p_hmax:.3f}")
    R.T("E1 done")
    # ---------------------------------------------------------------- E2 reachability
    R.banner("E2. reachability of the published numbers")
    for k, o in out.items():
        r1 = 0.20 <= o["Afix"] <= 0.30 and (o["sfix"] <= 0.06 or o["sFisher"] <= 0.06)
        r1b = 0.20 <= o["Afix"] <= 0.30
        r2 = 0.30 <= o["Hz"] <= 0.44 and o["sH"] <= 0.08
        R.P(f"  {o['name']}: A_fix(Chang) in [0.20, 0.30]: {r1b} (with sigma <= 0.06: bootstrap {o['sfix'] <= 0.06}, Fisher {o['sFisher'] <= 0.06}); H(Zhou) in [0.30, 0.44]: {0.30 <= o['Hz'] <= 0.44} (with sigma <= 0.08: {r2})")
    anyA = any(0.20 <= o["Afix"] <= 0.30 and o["sfix"] <= 0.06 for o in out.values())
    anyAF = any(0.20 <= o["Afix"] <= 0.30 and o["sFisher"] <= 0.06 for o in out.values())
    anyH = any(0.30 <= o["Hz"] <= 0.44 and o["sH"] <= 0.08 for o in out.values())
    R.P(f"  any variant with A_fix in [0.20, 0.30] AND bootstrap sigma <= 0.06: {anyA}; with a Fisher sigma <= 0.06: {anyAF}; any with H in [0.30, 0.44] and sigma <= 0.08: {anyH}")
    R.P(f"  smallest bootstrap sigma of A_fix over the variants: {min(o['sfix'] for o in out.values()):.3f}; smallest Fisher sigma: {min(o['sFisher'] for o in out.values()):.3f}; published +/- 0.04")
    # ---------------------------------------------------------------- E4 retro-injection (primary)
    R.banner("E4. retro-injection: could this pipeline detect a published-size dipole if it were real? (primary curves, position-permuted base, N = 500)")
    b = sub_bundle(d, prim)
    cv, n, uma, C, grid = b["cv"], b["n"], b["uma"], b["C"], b["grid"]
    F0, la0 = F0_fit(cv)
    fit = fit_dipole(cv, n, starts=5)
    ctrl_A, _, _, _ = run_perms(cv, n, uma, None, None, la0, "simple", S_INJ, 0, 5000)
    thr95, thr997 = float(np.quantile(ctrl_A, .95)), float(np.quantile(ctrl_A, .997))
    Db, Ab = run_boot(cv, n, la0, np.arange(cv.N), S_B, 400, 500, chunk=50, fixdir=CHANG)
    sfixC = float(np.std(Ab, ddof=1))
    Db, Ab = run_boot(cv, n, la0, np.arange(cv.N), S_B, 401, 500, chunk=50, fixdir=ZHOU)
    sfixZ = float(np.std(Ab, ddof=1))
    R.P(f"  thresholds of the null A-hat: 95% {thr95:.3f}; 99.7% {thr997:.3f}; observed sigma of A_fix along Chang {sfixC:.3f}, along Zhou {sfixZ:.3f}")
    E4 = {}
    for nm, dv, Ai, sg in (("Chang 0.25", CHANG, 0.25, sfixC), ("Zhou 0.37", ZHOU, 0.37, sfixZ)):
        CC.setW(cv=cv, n=n, uma=uma, la0=la0, C=C, grid=grid)
        ss = np.random.SeedSequence([S_INJ, hash(nm) % 1000 * 0 + (1 if 'Chang' in nm else 2)]).spawn(20)
        res = np.concatenate(pmap(_w_e4, [(s, 25, Ai, dv) for s in ss]))
        Ah, Af, Hh = res[:, 0], res[:, 1], res[:, 2]
        E4[nm] = dict(power95=float(np.mean(Ah > thr95)), power997=float(np.mean(Ah > thr997)), meanAfix=float(Af.mean()), det_fixed=float(np.mean(Af / sg > 1.645)), meanH=float(np.nanmean(Hh)))
        R.P(f"  injected {nm} along its axis: free-dipole power (>95% thr) {E4[nm]['power95']:.3f}, (>99.7% thr) {E4[nm]['power997']:.3f}; recovered A_fix mean {Af.mean():.3f} (std {Af.std():.3f}); fixed-direction detection (A_fix/sigma_obs > 1.645) {E4[nm]['det_fixed']:.3f}; mean H at the axis {np.nanmean(Hh):.3f}")
    # ---------------------------------------------------------------- verdict
    R.banner("E verdicts (frozen meaning)")
    prim_o = out[0]
    inC = abs(0.25 - prim_o["Afix"]) <= 1.96 * prim_o["sfix"]
    inH = abs(0.37 - prim_o["Hz"]) <= 1.96 * prim_o["sH"]
    pw = max(v["power95"] for v in E4.values())
    R.P(f"  (i) 0.25 inside the 95% interval of A_fix(Chang) = {prim_o['Afix']:+.3f} +/- {1.96 * prim_o['sfix']:.3f}: {inC}")
    R.P(f"  (ii) 0.37 inside the 95% interval of H(Zhou) = {prim_o['Hz']:+.3f} +/- {1.96 * prim_o['sH']:.3f}: {inH}")
    R.P(f"  (iii) E4 power (max over the two injections, free dipole > 95% threshold) = {pw:.3f} < 0.5: {pw < 0.5}")
    verdict = "REPRODUCES 'neither confirmed nor excluded'" if (inC and inH and pw < 0.5) else ("CONTRADICTED (0.25 or 0.37 outside the 95% interval)" if not (inC and inH) else "PARTIAL")
    R.P(f"  README verdict 'neither confirmed nor excluded': {verdict}")
    R.num("results", dict(variants=out, E4=E4, thr=[thr95, thr997]))
    return R.finish(0)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        import traceback
        traceback.print_exc()
        sys.exit(2)
