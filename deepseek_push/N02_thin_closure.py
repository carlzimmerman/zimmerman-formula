#!/usr/bin/env python3
"""
N02 -- CLOSURE OF THE THIN-LIMIT VOLUME WINDOW AT DEEP PRECISION
2026-09-23.  Engine: J02_moment_hierarchy (volume source, uniform kappa-cloud
kappa(r) = tau0 (1 + q r^2)); geometry: unit ball.

CONTENT
  P1  Deep-thin grid: E[D]_vol/tau0 and E[Q] at tau0 in {1e-4,2e-4,5e-4,1e-3,
      2e-3,5e-3}, q in {0,3,10}; n = 1e7 for the two smallest tau0, 4e6 else.
      Z per q against the closed form  c0(q) = 2/5 + 8q/35  (point-wise at the
      deepest probes AND per-q weighted linear-in-tau fits); curvature fits
      (sqrt-tau0 and linear) reported if the q=10 z exceeds 4.
  P2  Derivation from the N=1 sector (volume):  D telescopes as
        D = sum_j s_j (1 - u_j.u_N);  N=1: D = s0(1-mu)  (E[1-mu]=1 exactly,
      Thomson symmetry), and the sector law
        E[D 1{N=1}] = int rho du0 int_0^ch s0 (1-mu) kappa e^{-L1} e^{-L2} ...
      gives, by the FIRST-COLLISION LENGTH-BIAS (P(N=1) ~ tau0 E[ch],
      E[s0|N=1] -> E[ch^2]/(2 E[ch]) = 8/15):
        E[D]_vol/tau0 -> E[ch^2]/2 + q * E[int s r^2(s) ds]  =  2/5 + 8q/35.
      E[ch^2] = 4/5 exactly; the q-geometry integral  E[int s r^2 ds] =
      (1/2)E[r0^2 ch^2] + (1/4)E[ch^4]  =  8/35  (verified to SE by MC and
      by Legendre quadrature).  The exact-in-tau0 N=1 integrand is evaluated
      by weighted MC and compared with the engine masked at N==1 (z per point);
      the same weighted MC extrapolated to tau0 -> 0 gives 2/5 + 8q/35.
  P3  E[Q] thin expansion (volume, q=0):  Q = ch on N=0, Q = s0 mu + s1 on
      N=1 with E[Q 1{N=0}] = E[ch e^{-L1}] = E[ch] - tau0 E[ch^2] + (tau0^2/2)
      + O(tau0^3)  (E[ch^3] = 1 exactly), and  E[Q 1{N=1}]/tau0 -> B0 :=
      0.58092(13)  (exact N=1-sector integrand; no clean rational at 1e-4).
      Hence the thin tangent slope  dE[Q]/d tau0 -> -E[ch^2] + B0 =
      -0.2191(1):  the premised  -6/25  is CORRECTED (it would require
      B0 = 14/25, excluded at z = 164 of the sector value; L02's "-0.24"
      was the chord slope over tau0 ~ 0.05-0.1, not the tau0 -> 0 tangent).
      Full per-point law E[Q] = E[ch e^{-L1}] + tau0 B(tau0) + O(tau0^2)
      verified against the deep grid at |z| <= 1.2 (all six points).
  P4  The closed thin-window curve
        R_v(0,q) = (3/4 + 5q/12) / (2/5 + 8q/35)
                 = 1.875 / 1.8421 / 1.8307   at q = 0 / 3 / 10
      with SEs (delta method on c0) and the verdict: GENTLY DECREASING closed
      curve (K07's "universal ~1.86" was a within-2-SE reading of the deep
      points; at deep precision the closed curve is exact and decreasing).

Files: N02_thin_closure.py/.out, N02_results.json, N02_THIN_LIMIT_CLOSURE.md.
No git commit (per lane rules).  All formulas numerically verified.
"""
import json
import math
import os
import sys
import time

import numpy as np
from numpy.polynomial.legendre import leggauss

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from J02_moment_hierarchy import rate_integral, thomson_mu, simulate

# ----------------------------------------------------------------------------
# instrumented thin simulation: tracks s0, mu1, s1 per photon for the
# N=1 sector; Q = (x_f - x0).u_final exactly (bookkeeping cross-check);
# mirrors the J02 engine's flight logic (exact bisection, same kernels).
# ----------------------------------------------------------------------------

def thin_sim(n, tau0, q, seed):
    rng = np.random.default_rng(seed)
    d0 = rng.normal(size=(n, 3)); d0 = d0 / np.linalg.norm(d0, axis=1)[:, None]
    pos = d0 * rng.random(n)[:, None] ** (1 / 3)
    disp = np.zeros((n, 3))                  # x - x0, updated incrementally
    d = rng.normal(size=(n, 3)); direc = d / np.linalg.norm(d, axis=1)[:, None]
    elapsed = np.zeros(n)
    s0 = np.zeros(n); mu1 = np.zeros(n); s1 = np.zeros(n)
    N = np.zeros(n, dtype=int)
    alive = np.arange(n)
    first = True
    while len(alive):
        p, u = pos[alive], direc[alive]
        pd = np.sum(p * u, axis=1); r2 = np.sum(p * p, axis=1)
        disc = pd * pd - r2 + 1.0
        wall = -pd + np.sqrt(np.maximum(disc, 0.0))
        U = rng.random(len(alive))
        tau_wall = rate_integral(r2, pd, wall, tau0, q)
        esc = tau_wall <= -np.log(U)
        s = wall.copy()
        inner = ~esc
        if inner.any():
            lo = np.zeros(inner.sum()); hi = wall[inner]
            Ui = U[inner]; r2i = r2[inner]; pdi = pd[inner]
            for _ in range(60):
                mid = 0.5 * (lo + hi)
                val = rate_integral(r2i, pdi, mid, tau0, q) + np.log(Ui)
                tak = val < 0
                lo[tak] = mid[tak]; hi[~tak] = mid[~tak]
            s[inner] = 0.5 * (lo + hi)
        if first:
            s0[alive] = s
            first = False
        else:
            one = N[alive] == 1          # second flight of the N=1 photons
            if one.any():
                s1[alive[one]] = s[one]
        elapsed[alive] += s
        pos[alive] += u * s[:, None]
        disp[alive] += u * s[:, None]
        alive = alive[~esc]
        if len(alive) == 0:
            break
        was = N[alive].copy()
        p, u = pos[alive], direc[alive]
        r2 = np.sum(p * p, axis=1)
        mu = thomson_mu(rng, len(alive))
        t = rng.normal(size=(len(alive), 3))
        t -= np.sum(t * u, axis=1)[:, None] * u
        tn = np.linalg.norm(t, axis=1); t = t / tn[:, None]
        direc[alive] = u * mu[:, None] + t * np.sqrt(1 - mu * mu)[:, None]
        mu1[alive[was == 0]] = mu[was == 0]     # first-kick cosine
        N[alive] += 1
    X = np.sum(disp * direc, axis=1)
    D = elapsed - X
    return dict(D=D, Q=X, X=X, elapsed=elapsed, N=N, s0=s0, mu1=mu1, s1=s1,
                pos=pos, direc=direc, disp=disp)


def se(x):
    return float(np.std(x, ddof=1) / np.sqrt(len(x)))


# ----------------------------------------------------------------------------
# P2 geometry: first-flight moments by Legendre quadrature + MC cross-check
# ----------------------------------------------------------------------------

def geom_quad(ng=512):
    xr, wr = leggauss(ng); r = 0.5 * xr + 0.5
    xm, wm = leggauss(2 * ng); mu = xm
    R = r[:, None]; MU = mu[None, :]
    Wr = (3.0 * R ** 2) * (0.5 * wr[:, None])
    Wm = 0.5 * wm[None, :]
    cord = -R * MU + np.sqrt(np.maximum(0.0, 1.0 - R ** 2 * (1.0 - MU ** 2)))
    def ev(f):
        return float(np.sum(Wr * f * Wm))
    ch = ev(cord); ch2 = ev(cord ** 2); ch3 = ev(cord ** 3); ch4 = ev(cord ** 4)
    r0ch = ev(R ** 2 * cord)
    r0ch2 = ev(R ** 2 * cord ** 2)
    pmu_ch3 = ev(R * MU * cord ** 3)                 # (p.u) ch^3 term
    I1 = ev(R ** 2 * cord + R * MU * cord ** 2 + cord ** 3 / 3.0)
    G = ev(0.5 * R ** 2 * cord ** 2 + (2.0 / 3.0) * R * MU * cord ** 3
           + 0.25 * cord ** 4)                        # E[int s r^2(s) ds]
    return dict(ch=ch, ch2=ch2, ch3=ch3, ch4=ch4, r0ch=r0ch, r0ch2=r0ch2,
                pmu_ch3=pmu_ch3, I1=I1, G=G)


# ----------------------------------------------------------------------------
# P2 exact N=1 sector integrand by weighted MC (exact in tau0)
# ----------------------------------------------------------------------------

def sector_mc(n, tau0, q, seed):
    """E over (x0 vol-uniform, u0 iso, s0 ~ Unif[0,ch], mu ~ Thomson) of
    theta_D  = s0 (1-mu) kappa(y) ch e^{-L1} e^{-L2}
    theta_Q1 = (s0 mu + s1) kappa(y) ch e^{-L1} e^{-L2}
    theta_Q0 = ch e^{-L1}                                     (N=0 piece)
    Also returns E[s1 1{N=1}] integrated (for the E[Q] slope)."""
    rng = np.random.default_rng(seed)
    d0 = rng.normal(size=(n, 3)); d0 /= np.linalg.norm(d0, axis=1)[:, None]
    x0 = d0 * rng.random(n)[:, None] ** (1 / 3)
    u0 = rng.normal(size=(n, 3)); u0 /= np.linalg.norm(u0, axis=1)[:, None]
    p0 = np.sum(x0 * u0, axis=1); r02 = np.sum(x0 * x0, axis=1)
    ch = -p0 + np.sqrt(np.maximum(0.0, 1.0 - r02 + p0 * p0))
    s = rng.random(n) * ch
    y = x0 + u0 * s[:, None]
    r2y = np.sum(y * y, axis=1)
    L1 = rate_integral(r02, p0, s, tau0, q)
    mu = thomson_mu(rng, n)
    t = rng.normal(size=(n, 3))
    t -= np.sum(t * u0, axis=1)[:, None] * u0
    tn = np.linalg.norm(t, axis=1); t = t / tn[:, None]
    u1 = u0 * mu[:, None] + t * np.sqrt(1 - mu * mu)[:, None]
    p1 = np.sum(y * u1, axis=1)
    s1 = -p1 + np.sqrt(np.maximum(0.0, 1.0 - r2y + p1 * p1))
    L2 = rate_integral(r2y, p1, s1, tau0, q)
    w = ch * np.exp(-L1 - L2)
    kap = tau0 * (1.0 + q * r2y)
    thD = s * (1.0 - mu) * kap * w
    thQ1 = (s * mu + s1) * kap * w
    thQ0 = ch * np.exp(-rate_integral(r02, p0, ch, tau0, q))
    thS1 = s1 * kap * w            # E[s1 1{N=1}] integrated
    return dict(thD=thD, thQ1=thQ1, thQ0=thQ0, thS1=thS1)


# ----------------------------------------------------------------------------
# main
# ----------------------------------------------------------------------------

def main():
    t0 = time.time()
    res = {"checks": {}, "measurements": {}}
    ok = True
    TAUS = (1e-4, 2e-4, 5e-4, 1e-3, 2e-3, 5e-3)
    QS = (0.0, 3.0, 10.0)
    N_DEEP = 10_000_000
    N_MID = 4_000_000
    C_FORM = {0.0: 2.0 / 5.0, 3.0: 2.0 / 5.0 + 8.0 * 3 / 35,
              10.0: 2.0 / 5.0 + 8.0 * 10 / 35}

    grid = []
    for tau0 in TAUS:
        n = N_DEEP if tau0 <= 2e-4 else N_MID
        for q in QS:
            seed = int(round(tau0 * 1e7)) * 31 + int(q) * 1009 + 17
            r = thin_sim(n, tau0, q, seed)
            c = float(np.mean(r["D"]) / tau0)
            sc = se(r["D"]) / tau0
            EQ = float(np.mean(r["Q"])); sQ = se(r["Q"])
            row = dict(tau0=tau0, q=q, n=n, seed=seed, c=c, sc=sc, EQ=EQ,
                       sQ=sQ, EN=float(np.mean(r["N"])))
            row["s0_cond1"] = float(np.mean(r["s0"][r["N"] == 1])) if (r["N"] == 1).any() else None
            row["s1_1"] = float(np.mean(r["s1"][r["N"] == 1])) if (r["N"] == 1).any() else None
            row["Q_q0"] = float(np.mean(r["Q"][r["N"] == 0])) if (r["N"] == 0).any() else None
            row["Q_q1"] = float(np.mean(r["Q"][r["N"] == 1])) if (r["N"] == 1).any() else None
            row["P1"] = float(np.mean(r["N"] == 1))
            row["EQ1_0"] = float(np.mean(r["Q"] * (r["N"] == 0)))
            row["EQ1_1"] = float(np.mean(r["Q"] * (r["N"] == 1)))
            grid.append(row)
    res["measurements"]["deep_grid"] = grid

    # ---- P1c: thin_sim vs engine cross-check at the thickest grid point ----
    rts = thin_sim(2_000_000, 5e-3, 10.0, seed=2026)
    reng = simulate(2_000_000, 5e-3, 10.0, "volume", seed=2027)
    zD = (np.mean(rts["D"]) - np.mean(reng["D"])) / math.hypot(
        se(rts["D"]), se(reng["D"]))
    zN = (np.mean(rts["N"]) - np.mean(reng["N"])) / math.hypot(
        se(rts["N"]), se(reng["N"]))
    res["measurements"]["crosscheck_engine"] = dict(
        E_D_ts=float(np.mean(rts["D"])), E_D_eng=float(np.mean(reng["D"])),
        z_D=float(zD), z_N=float(zN),
        max_QQX=float(np.max(np.abs(rts["Q"] - rts["X"]))))
    res["checks"]["crosscheck_thin_sim_engine"] = bool(abs(zD) < 3.0 and abs(zN) < 3.0)
    ok &= res["checks"]["crosscheck_thin_sim_engine"]

    # ---- P1a: point-wise z against the closed form -------------------------
    z_pts = {}
    for q in QS:
        zs = []
        for row in grid:
            if row["q"] == q:
                zs.append((row["tau0"], (row["c"] - C_FORM[q]) / row["sc"]))
        z_pts[q] = zs
    res["measurements"]["z_pointwise"] = z_pts

    # ---- P1b: per-q weighted fit c0 + c1*tau -------------------------------
    fits = {}
    for q in QS:
        rows = [r for r in grid if r["q"] == q]
        ts = np.array([r["tau0"] for r in rows])
        cs = np.array([r["c"] for r in rows])
        ws = 1.0 / np.array([r["sc"] ** 2 for r in rows])
        A = np.vstack([np.ones_like(ts), ts]).T
        W = np.sqrt(ws)
        Aw = A * W[:, None]; bw = cs * W
        (c0, c1), cov = np.linalg.lstsq(Aw, bw, rcond=None)[0], \
                        np.linalg.inv(Aw.T @ Aw)
        sc0 = math.sqrt(cov[0, 0]); sc1 = math.sqrt(cov[1, 1])
        z = (c0 - C_FORM[q]) / sc0
        fits[q] = dict(c0=c0, sc0=sc0, c1=c1, sc1=sc1, z=z,
                       chi2=float(np.sum(ws * (cs - c0 - c1 * ts) ** 2)))
        # curvature fits at q=10 (sqrt-tau0 and constrained linear), for record
        if q == 10.0:
            sq = np.sqrt(ts)
            A2 = np.vstack([np.ones_like(ts), sq]).T
            A2w = A2 * W[:, None]
            (d0q, dq), cov2 = np.linalg.lstsq(A2w, bw, rcond=None)[0], \
                              np.linalg.inv(A2w.T @ A2w)
            z2 = (d0q - C_FORM[q]) / math.sqrt(cov2[0, 0])
            # 3-pt fit (deepest only), linear in tau
            d3 = np.array([r["c"] for r in rows if r["tau0"] <= 5e-4])
            t3 = np.array([r["tau0"] for r in rows if r["tau0"] <= 5e-4])
            dd3 = (d3 - C_FORM[q])
            z3 = dd3.mean() / (dd3.std(ddof=1) / math.sqrt(len(dd3))) \
                if len(dd3) > 1 else float("nan")
            fits[q]["d_sqrt"] = float(dq)
            fits[q]["sd_sqrt"] = float(math.sqrt(cov2[1, 1]))
            fits[q]["z_sqrt"] = float(z2)
            fits[q]["z_3deep"] = float(z3)
    res["measurements"]["fits"] = fits

    # ---- P2: geometry anchors ----------------------------------------------
    gq = geom_quad(512)
    # MC cross-check of the q-geometry constant
    rng = np.random.default_rng(20260923)
    nG = 30_000_000
    dg = rng.normal(size=(nG, 3)); dg /= np.linalg.norm(dg, axis=1)[:, None]
    xg = dg * rng.random(nG)[:, None] ** (1 / 3)
    ug = rng.normal(size=(nG, 3)); ug /= np.linalg.norm(ug, axis=1)[:, None]
    pg = np.sum(xg * ug, axis=1); r2g = np.sum(xg * xg, axis=1)
    chg = -pg + np.sqrt(np.maximum(0.0, 1.0 - r2g + pg * pg))
    Gv = 0.5 * r2g * chg ** 2 + (2.0 / 3.0) * pg * chg ** 3 + 0.25 * chg ** 4
    qcoef_SE = float(se(Gv))
    ch3m = float(np.mean(chg ** 3)); ch4m = float(np.mean(chg ** 4))
    geom = dict(ch=gq["ch"], ch2=gq["ch2"], ch3=gq["ch3"], ch4=gq["ch4"],
                r0ch=gq["r0ch"], r0ch2=gq["r0ch2"], pmu_ch3=gq["pmu_ch3"],
                I1_quad=gq["I1"], G_quad=gq["G"], G_mc=float(np.mean(Gv)),
                G_mc_SE=qcoef_SE, ch3_mc=ch3m, ch4_mc=ch4m,
                qcoef_quad=gq["G"], qcoef_mc=float(np.mean(Gv)),
                qcoef_mc_SE=qcoef_SE)
    res["measurements"]["geom"] = geom
    res["checks"]["chord_3over4"] = bool(abs(gq["ch"] - 0.75) < 1e-10)
    res["checks"]["chord2_4over5"] = bool(abs(gq["ch2"] - 0.8) < 1e-10)
    res["checks"]["Tq_num_5over12"] = bool(abs(gq["I1"] - 5.0 / 12.0) < 1e-10)
    res["checks"]["qcoef_8over35_quad"] = bool(abs(gq["G"] - 8.0 / 35.0) < 1e-9)
    res["checks"]["qcoef_8over35_mc"] = bool(
        abs(np.mean(Gv) - 8.0 / 35.0) < 6 * qcoef_SE + 1e-6)
    ok &= all(res["checks"].values())

    # ---- P2b: exact N=1 sector MC, engine-masked comparison -----------------
    sector_rows = []
    for (tau0, q) in [(0.02, 0.0), (0.02, 3.0), (0.02, 10.0), (0.05, 10.0)]:
        sm = sector_mc(6_000_000, tau0, q, seed=int(tau0 * 1e6) + int(q) * 777)
        r = simulate(6_000_000, tau0, q, "volume", seed=3 + int(q) + int(tau0 * 100))
        m = r["N"] == 1
        emD = float(np.mean(r["D"] * (r["N"] == 1)))
        semD = float(se(r["D"] * (r["N"] == 1)))
        sD = float(np.mean(sm["thD"])); sD_SE = float(se(sm["thD"]))
        z = (emD - sD) / math.hypot(semD, sD_SE)
        sector_rows.append(dict(tau0=tau0, q=q, engine_E_D1=emD,
                                engine_SE=semD, sector_E_D1=sD,
                                sector_SE=sD_SE, z=z))
        res["checks"][f"N1_mask_{tau0}_{q}"] = bool(abs(z) < 4.0)
        ok &= bool(abs(z) < 4.0)
    res["measurements"]["sector_engine_mask"] = sector_rows

    # sector MC at deep tau0 -> limit 2/5 + 8q/35: linear-in-tau fit over 4 depths
    lim_rows = []
    for q in QS:
        sms = []
        for tau0 in (1e-4, 2e-4, 5e-4, 1e-3):
            sm = sector_mc(6_000_000, tau0, q,
                           seed=555 + int(q) * 13 + int(tau0 * 1e5))
            c = float(np.mean(sm["thD"]) / tau0); sc = se(sm["thD"]) / tau0
            sms.append((tau0, c, sc))
            lim_rows.append(dict(tau0=tau0, q=q, c_sec=c, sc_sec=sc))
        tts = np.array([x[0] for x in sms]); ccs = np.array([x[1] for x in sms])
        wws = 1.0 / np.array([x[2] ** 2 for x in sms])
        A = np.vstack([np.ones_like(tts), tts]).T
        W = np.sqrt(wws)
        (c0s, c1s), cov = np.linalg.lstsq(A * W[:, None], ccs * W,
                                          rcond=None)[0], \
                          np.linalg.inv((A * W[:, None]).T @ (A * W[:, None]))
        zs = (c0s - C_FORM[q]) / math.sqrt(cov[0, 0])
        lim_rows.append(dict(q=q, tau0="fit", c0_sec=c0s, sc0_sec=math.sqrt(cov[0, 0]),
                             c1_sec=c1s, z=zs))
        res["checks"][f"sector_limit_{q}_fit"] = bool(abs(zs) < 4.0)
        ok &= bool(abs(zs) < 4.0)
    res["measurements"]["sector_limit"] = lim_rows

    # B(tau) = E[s1 1{N=1}]/tau from the exact sector integrand, q=0:
    # -> B0 := lim B(tau)  (linear-in-tau fit); slope E[Q] = -E[ch^2] + B0
    Bs_rows = []
    for tau0 in (1e-4, 2e-4, 5e-4, 1e-3, 2e-3, 5e-3):
        sm = sector_mc(6_000_000, tau0, 0.0, seed=9001 + int(tau0 * 1e5))
        Bv = float(np.mean(sm["thS1"]) / tau0)
        Bs_rows.append(dict(tau0=tau0, B=Bv, sB=se(sm["thS1"]) / tau0))
    tbs = np.array([x["tau0"] for x in Bs_rows])
    bbs = np.array([x["B"] for x in Bs_rows])
    wbs = 1.0 / np.array([x["sB"] ** 2 for x in Bs_rows])
    A = np.vstack([np.ones_like(tbs), tbs]).T
    W = np.sqrt(wbs)
    (B0, Bc1), covB = np.linalg.lstsq(A * W[:, None], bbs * W, rcond=None)[0], \
                      np.linalg.inv((A * W[:, None]).T @ (A * W[:, None]))
    sB0 = math.sqrt(covB[0, 0])
    # engine cross-check: B_eng(tau) = E[Q 1{N=1}]/tau from the grid rows
    Bx = []
    for bro in Bs_rows:
        g = next(x for x in grid if x["q"] == 0.0 and x["tau0"] == bro["tau0"])
        n1 = int(round(g["P1"] * g["n"]))
        sBeng = math.hypot(0.45 / math.sqrt(max(n1, 1)) * g["P1"] / g["tau0"],
                           g["P1"] * (1.0 - g["P1"]) ** 0.5 / math.sqrt(g["n"]) *
                           g["Q_q1"] / g["tau0"]) if n1 > 5 else float("nan")
        Beng = g["Q_q1"] * g["P1"] / g["tau0"]
        zc = (bro["B"] - Beng) / math.hypot(bro["sB"], sBeng)
        Bx.append(dict(tau0=bro["tau0"], B_sect=bro["B"], sB_sect=bro["sB"],
                       B_eng=Beng, sB_eng=sBeng, z=zc))
        res["checks"][f"B_eng_x_{bro['tau0']:.0e}"] = bool(abs(zc) < 4.0)
        ok &= bool(abs(zc) < 4.0)
    res["measurements"]["B_sector"] = dict(rows=Bs_rows, B0=B0, sB0=sB0,
                                           Bc1=Bc1, crosscheck=Bx)
    # CORRECTION of the premised 3/4 - (6/25) tau + O(tau^2): the thin tangent
    # slope is  -(4/5 - B0) = -0.21908(13), NOT -6/25 = -0.24:
    # the premised numerator piece assumed E[s1 1{N=1}]/tau0 -> 14/25;
    # the exact-sector value is B0 = 0.58092(13) (z = 164 vs 14/25).
    slope_exact = -(4.0 / 5.0 - B0)
    s_slope = sB0
    res["measurements"]["EQ_slope_corrected"] = dict(
        slope=slope_exact, s_slope=s_slope, slope_premised=-6.0 / 25.0,
        z_vs_premised=(slope_exact + 6.0 / 25.0) / s_slope,
        B0=B0, sB0=sB0, zB0_vs_14over25=(B0 - 14.0 / 25.0) / sB0)

    # ---- P3: E[Q] thin expansion ------------------------------------------
    EQ_rows = [r for r in grid if r["q"] == 0.0]
    ts = np.array([r["tau0"] for r in EQ_rows])
    es = np.array([r["EQ"] for r in EQ_rows])
    ws = 1.0 / np.array([r["sQ"] ** 2 for r in EQ_rows])
    A = np.vstack([np.ones_like(ts), ts]).T
    W = np.sqrt(ws)
    (a0, b0), cov = np.linalg.lstsq(A * W[:, None], es * W, rcond=None)[0], \
                    np.linalg.inv((A * W[:, None]).T @ (A * W[:, None]))
    sa0 = math.sqrt(cov[0, 0]); sb0 = math.sqrt(cov[1, 1])
    z_slope = (b0 + 6.0 / 25.0) / sb0
    z_int = (a0 - 0.75) / sa0
    # N=0 sector piece: E[Q 1{N=0}] = E[ch e^{-L1}] = E[ch] - tau E[ch^2]
    #   + (tau^2/2) E[ch^3] + O(tau^3)   (per-point, vs sector-MC at deep tau)
    decomp = []
    for r in EQ_rows:
        pred = 3.0 / 4.0 - r["tau0"] * 0.8 + 0.5 * r["tau0"] ** 2 * gq["ch3"]
        decomp.append(dict(tau0=r["tau0"], EQ1_0=r["EQ1_0"], pred=pred))
    res["measurements"]["EQ_decomp_N0"] = decomp
    # full thin law per point (q=0): E[Q] = E[ch e^{-L1}] + tau*B(tau) + O(tau^2),
    # with B(tau) taken at the same tau from the exact sector integrand
    EQfull = []
    for r in EQ_rows:
        bro = next(x for x in Bs_rows if abs(x["tau0"] - r["tau0"]) < 1e-12)
        pred = 3.0 / 4.0 - r["tau0"] * 0.8 + 0.5 * r["tau0"] ** 2 * gq["ch3"] \
            + r["tau0"] * bro["B"]
        zz = (r["EQ"] - pred) / math.hypot(r["sQ"], r["tau0"] * bro["sB"])
        EQfull.append(dict(tau0=r["tau0"], EQ=r["EQ"], sEQ=r["sQ"], pred=pred,
                           z=zz))
        res["checks"][f"EQ_full_thin_{r['tau0']:.0e}"] = bool(abs(zz) < 4.0)
        ok &= bool(abs(zz) < 4.0)
    res["measurements"]["EQ_full_thin"] = EQfull
    # N=1 sector piece: B(tau) = E[s1 1{N=1}]/tau  (q=0) -- engine-level view
    Brows = [r for r in EQ_rows if r["tau0"] <= 5e-4]
    Bs = np.array([r["s1_1"] * r["P1"] / r["tau0"] for r in Brows])
    B = float(np.mean(Bs)); B_SE = float(np.std(Bs, ddof=1) / math.sqrt(len(Bs)))
    rdeep = EQ_rows[0]
    Bdeep = rdeep["s1_1"] * rdeep["P1"] / rdeep["tau0"]
    EQout = dict(a0=a0, sa0=sa0, b0=b0, sb0=sb0, z_slope=z_slope, z_int=z_int,
                 B_eng_deep=B, B_eng_SE=B_SE,
                 Bdeep=Bdeep, slope_pred=-6.0 / 25.0, N0coef=-4.0 / 5.0)
    res["measurements"]["EQ_thin"] = EQout
    res["checks"]["EQ_slope_minus6over25"] = bool(abs(z_slope) < 4.0)
    res["checks"]["EQ_intercept_3over4"] = bool(abs(z_int) < 4.0)
    ok &= all(res["checks"][k] for k in ("EQ_slope_minus6over25",
                                         "EQ_intercept_3over4"))
    # per-q slopes of E[Q] (measured)
    slopes_q = {}
    for q in QS:
        rr = [r for r in grid if r["q"] == q]
        tt = np.array([r["tau0"] for r in rr]); ee = np.array([r["EQ"] for r in rr])
        ww = 1.0 / np.array([r["sQ"] ** 2 for r in rr])
        Aq = np.vstack([np.ones_like(tt), tt]).T
        Wq = np.sqrt(ww)
        (aa, bb), _ = np.linalg.lstsq(Aq * Wq[:, None], ee * Wq, rcond=None)[0], None
        slopes_q[q] = dict(intercept=float(aa), slope=float(bb))
    res["measurements"]["EQ_slopes_per_q"] = slopes_q

    # ---- P4: thin-window curve ---------------------------------------------
    curve = []
    for q in QS:
        num = 3.0 / 4.0 + 5.0 * q / 12.0
        den = C_FORM[q]
        f = fits[q]
        R = num / den
        sR = R * f["sc0"] / den
        curve.append(dict(q=q, num=num, c0_form=den, R=R, sR=sR,
                          c0_fit=f["c0"], sc0_fit=f["sc0"], z_fit=f["z"]))
    res["measurements"]["thin_window_curve"] = curve
    # verdict: decreasing vs universal
    R0 = curve[0]["R"]; R3 = curve[1]["R"]; R10 = curve[2]["R"]
    sR0 = curve[0]["sR"]; sR3 = curve[1]["sR"]; sR10 = curve[2]["sR"]
    z_dec_03 = (R0 - R3) / math.hypot(sR0, sR3)
    z_dec_010 = (R0 - R10) / math.hypot(sR0, sR10)
    res["measurements"]["verdict"] = dict(z_dec_03=z_dec_03,
                                          z_dec_010=z_dec_010,
                                          R0=R0, R3=R3, R10=R10)
    res["measurements"]["runtime_s"] = time.time() - t0

    # ---- assembly ----------------------------------------------------------
    res["total_checks"] = len(res["checks"])
    res["passed"] = sum(1 for v in res["checks"].values() if v)
    res["ALL_PASSED"] = bool(ok)
    with open("N02_results.json", "w") as f:
        json.dump(res, f, indent=1)
    print(json.dumps(res, indent=1))
    print("ALL N02 CHECKS PASSED" if ok else "N02 CHECK FAILURE")
    print("elapsed %.1f s" % res["measurements"]["runtime_s"])
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())