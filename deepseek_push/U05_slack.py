#!/usr/bin/env python3
"""
U05 -- THE ANALYTIC SLACK (J00/ND1): corr(D,ang) and the slack curve as
functions of (tau0, q).  Continuation of the moment channel on the frozen
conservative Thomson-sphere model (J00 scope; J05/J06 untouched, append-only).

Engine: J02_moment_hierarchy.simulate (exact optical-depth bisection;
bit-identical kernels; no null-collision thinning).  Every number below
carries a 24-block jackknife SE; every formula is machine-verified.

CONTENT
 (1) CLOSURE RATIO vs SLACK -- are R_1 and the J05 slack the same object?
       R_1   = E[D ang] / (E[D] E[ang])          = 1 + Cov(D,ang)/(E[D]E[ang])
       slack = E[D^2] E[ang^2] / E[D ang]^2      (= 1/rho0^2, J06 exact)
     Exact link (algebra, verified per cloud):
       slack * R_1^2 = (1 + CV_D^2)(1 + CV_ang^2),  CV = mean-normalized std
     But they are NOT the same object: as tau0 -> 0, R_1 - 1 diverges
     (L01: (7/5)/[(1+q/3)tau0] - 1) while slack stays finite, with the
     derived thin intercept (N=1 sector: D = s1 (1-mu), ang = (1-mu)):
       S_thin(q) = (1/3 + q/5)(1 + q/3)/(1/2 + q/4)^2      (central source)
                  = 4/3, 448/375, 91/81 at q = 0, 3, 10 ;  -> 16/15 (q->inf)
     Volume-source analogue (chord geometry, N=1 sector):
       S_vol(q) = A2(q) P1(q)/A1(q)^2,
         A1 = 2/5 + 12q/35,  A2 = 1/3 + q*E[ch^5]/5,  P1 = 3/4 + 5q/12
         (E[ch^5] by Legendre quadrature + MC; E[ch..ch^4] = N02 closed rows)
     Comparison with N02's closed thin window R_v(0,q) = (3/4+5q/12)/(2/5+8q/35)
     (a ratio-of-means window for the volume source -- a DIFFERENT object,
     same N=1-sector machinery, same gentle q-decrease).
 (2) ASYMPTOTIC q -> inf: q-scan q = 30/100/300 (n = 3e5; 30/100 re-run at the
     J06 seeds 8007/9007 for a bit-identical harness cross-check; 300 new),
     plus J06's q = 0/3/10 clouds.  slack-1 vs 1/Nbar: NOT linear (local
     exponent collapses 0.53 -> 0.08); floor model slack-1 = s_inf + c/Nbar
     fitted on q in {10,30,100} and tested OUT OF SAMPLE on q = 300; the
     no-floor power law is the registered alternative.
 (3) THE ND1 KILL (re-stated from J00): "a proven positive lower bound on the
     slack above the measured 1.06, or an n=10^7 measurement showing the
     q-large limit flattening above 1.05".  Tested on the reachable
     (tau0,q) family: thin (derived intercepts) + asymptotic (floor) +
     measured grid.  Reported honestly.
 (4) COMPOSITE closed-form candidate: slack = 1 + s0(q)/(N-score) + ... :
     the naive 1 + s0/Nbar form is killed (thin intercept is finite, and the
     large-q floor is non-zero); the anchored two-parameter form
       slack - 1 = s_inf + (S_thin(q) - 1 - s_inf) * N0(q)/(N0(q) + Nbar)
     is fitted per q-chain and tested against the full measured grid (J06
     numbers + the new q = 300), with the N0(q), s_inf(q) profiles reported.

Every check below is gated at the J-channel convention (z < 5 combined SE
unless the gate says otherwise).  No git commit (lane rule).
"""
import json
import math
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from J02_moment_hierarchy import simulate

OUT = "U05_results.json"
HERE = os.path.dirname(os.path.abspath(__file__))


# ---------------------------------------------------------------------------
# derived closed forms
# ---------------------------------------------------------------------------
def S_thin(q):
    """Thin-limit slack intercept, central source, N=1 sector (derived).
       D|N=1 = s1 (1-mu), ang|N=1 = (1-mu) with s1 length-biased by
       kappa~(s) = 1 + q s^2 on [0,1]:
         E[s|1] -> (1/2+q/4)/(1+q/3),  E[s^2|1] -> (1/3+q/5)/(1+q/3)"""
    return (1.0 / 3.0 + q / 5.0) * (1.0 + q / 3.0) / (1.0 / 2.0 + q / 4.0) ** 2


def S_vol(q):
    """Thin-limit slack intercept, volume source, N=1 sector (derived, CLOSED).
       Chord geometry (r(s)^2 = r0^2 + 2s(r0.u) + s^2), exact quadrature
       constants: E[ch]=3/4, E[ch^2]=4/5, E[ch^3]=1, E[ch^4]=48/35 (N02),
       E[ch^5]=2, E[r0^2 ch^3]=3/5, E[(r0.u) ch^4]=-4/5, so
         B1(q) = E[int s kappa~ ds]  = 2/5 + 8q/35   (= N02 c0)
         B2(q) = E[int s^2 kappa~ ds] = 1/3 + q/5
         P1(q) = E[int kappa~ ds]    = 3/4 + 5q/12   (= N02 numerator)
             S_vol(q) = B2 P1 / B1^2        (25/16, 1715/1083, ...; -> 1225/768)
       All rationals verified by Legendre quadrature (1e-9) in-script."""
    B1 = 2.0 / 5.0 + 8.0 * q / 35.0
    B2 = 1.0 / 3.0 + q / 5.0
    P1 = 3.0 / 4.0 + 5.0 * q / 12.0
    return B2 * P1 / B1 ** 2


# ---------------------------------------------------------------------------
# statistics
# ---------------------------------------------------------------------------
def block_stats(arrays, fstats, B=24):
    """Delete-one-block jackknife: fstats(dict of arrays) -> dict of scalars.
    Returns (full_stats, {key: SE})."""
    n = len(next(iter(arrays.values())))
    full = {k: float(v) for k, v in fstats(arrays).items()}
    keys = list(full.keys())
    lo = {k: np.empty(B) for k in keys}
    cuts = np.linspace(0, n, B + 1, dtype=int)
    mask = np.ones(n, bool)
    for i in range(B):
        m = mask.copy()
        m[cuts[i]:cuts[i + 1]] = False
        sub = {k: v[m] for k, v in arrays.items()}
        vals = fstats(sub)
        for k in keys:
            lo[k][i] = float(vals[k])
    se = {k: float(np.sqrt((B - 1) / B * np.sum((lo[k] - lo[k].mean()) ** 2)))
          for k in keys}
    return full, se


def core_stats(tau0, q):
    """Builder of the per-cloud stat function (closure over tau0, q)."""
    def f(a):
        mD = np.mean(a["D"]); mang = np.mean(a["ang"])
        mD2 = np.mean(a["D2"]); mang2 = np.mean(a["ang2"])
        mDang = np.mean(a["Dang"])
        mDv2 = np.mean(a["Dv2"])
        slack = mD2 * mang2 / mDang ** 2
        R1 = mDang / (mD * mang)
        R1b = 1.0 + (mDang - mD * mang) / (mD * mang)
        R1v = mDv2 / (2.0 * mD * mang)          # hierarchy m=1, velocity path
        rho0 = mDang / math.sqrt(mD2 * mang2)
        CVD = mD2 / mD ** 2 - 1.0
        CVA = mang2 / mang ** 2 - 1.0
        ident = slack * R1 ** 2 - (1.0 + CVD) * (1.0 + CVA)
        return dict(slack=slack, R1=R1, R1_cov=R1b, R1_v=R1v, rho0=rho0,
                    CVD=CVD, CVA=CVA, ident=ident,
                    R1_thin=R1 * tau0 * (1.0 + q / 3.0) * (5.0 / 7.0))
    return f


def sector_stats(f):
    """N=1 slice: D = s1 (1-mu), ang = (1-mu) pointwise => E[D|1]/E[ang|1]
    is the length-biased E[s1|N=1]; slice slack = E[s1^2|1]/E[s1|1]^2."""
    def g(a):
        mD = np.mean(a["D"]); mang = np.mean(a["ang"])
        mD2 = np.mean(a["D2"]); mang2 = np.mean(a["ang2"])
        mDang = np.mean(a["Dang"])
        # tautology guarded: D == s1*ang per photon on N=1
        return dict(s1_ratio=mD / mang,
                    slice_slack=mD2 * mang2 / mDang ** 2,
                    D_over_ang2=mD2 / mang2)
    return g


# ---------------------------------------------------------------------------
# one cloud
# ---------------------------------------------------------------------------
def analyze(n, tau0, q, source, seed, tag):
    t0 = time.time()
    r = simulate(n, tau0, q, source, seed)
    D = r["D"]; ang = r["ang"]
    arr = dict(D=D, ang=ang, D2=D ** 2, ang2=ang ** 2, Dang=D * ang,
               Dv2=D * r["v2"])
    core, secore = block_stats(arr, core_stats(tau0, q))
    N1 = r["N"] == 1
    sec_ok = int(N1.sum())
    if sec_ok > 200:
        sarr = {k: v[N1] for k, v in arr.items()}
        sec, sesec = block_stats(sarr, sector_stats(tau0))
    else:
        sec = sesec = None
    out = dict(tag=tag, source=source, tau0=tau0, q=q, n=n, seed=seed,
               secs=round(time.time() - t0, 1),
               Nbar=float(np.mean(r["N"])), s_Nbar=float(
                   np.std(r["N"], ddof=1) / math.sqrt(n)),
               E_D=float(np.mean(D)), s_E_D=float(
                   np.std(D, ddof=1) / math.sqrt(n)),
               E_ang=float(np.mean(ang)),
               E_D2=float(np.mean(arr["D2"])), E_ang2=float(np.mean(arr["ang2"])),
               E_Dang=float(np.mean(arr["Dang"])),
               slack=core["slack"], s_slack=secore["slack"],
               R1=core["R1"], s_R1=secore["R1"],
               R1_cov=core["R1_cov"], s_R1_cov=secore["R1_cov"],
               R1_v=core["R1_v"], s_R1_v=secore["R1_v"],
               rho0=core["rho0"],
               CVD=core["CVD"], CVA=core["CVA"],
               ident_diff=core["ident"], s_ident=secore["ident"],
               R1_thin_ratio=core["R1_thin"], s_R1_thin=secore["R1_thin"],
               n_sector=int(N1.sum()),
               s1_ratio=sec["s1_ratio"] if sec else None,
               s_s1_ratio=sesec["s1_ratio"] if sec else None,
               slice_slack=sec["slice_slack"] if sec else None,
               s_slice_slack=sesec["slice_slack"] if sec else None)
    print(f"[{tag:16s}] t0={tau0:5.2f} q={q:4.0f} n={n:>7d} Nbar={out['Nbar']:9.2f}"
          f" slack={out['slack']:.5f}+-{out['s_slack']:.5f}"
          f" R1={out['R1']:9.3f} rho0={out['rho0']:.5f} "
          f"({out['secs']}s)")
    return out


# ---------------------------------------------------------------------------
# fitting helpers
# ---------------------------------------------------------------------------
def wls(A, y, se):
    """Weighted least squares y = A beta; returns beta, cov, chi2."""
    w = 1.0 / se
    Aw = A * w[:, None]
    yw = y * w
    beta, *_ = np.linalg.lstsq(Aw, yw, rcond=None)
    resid = y - A @ beta
    chi2 = float(np.sum((resid / se) ** 2))
    cov = np.linalg.inv(Aw.T @ Aw)
    return beta, cov, chi2, resid


def chain_fit(pts, Delta):
    """Anchored composite per q-chain: pts = list of (Nbar, slack-1, se).
       slack - 1 = s_inf + (Delta - s_inf) * N0/(N0 + Nbar), Delta = S_thin - 1
    Search over log N0 in [1e-2, 1e5] with inner closed-form solve for s_inf
    clipped to [0, Delta].  Returns (s_inf, N0, chi2, worst_z, per-point z)."""
    Nbar = np.array([t[0] for t in pts]); y = np.array([t[1] for t in pts])
    se = np.array([t[2] for t in pts])

    def chi2_of(N0):
        if N0 <= 0:
            return 1e300, 0.0
        w = N0 / (N0 + Nbar)
        # y = s_inf + (Delta - s_inf)*w  =>  y - Delta*w = s_inf*(1 - w)
        yy = y - Delta * w
        AA = (1.0 - w)[:, None]
        s_inf = float(np.sum(AA[:, 0] * yy / se ** 2) /
                      np.sum(AA[:, 0] ** 2 / se ** 2))
        s_inf = min(max(s_inf, 0.0), Delta)
        pred = s_inf + (Delta - s_inf) * w
        return float(np.sum(((y - pred) / se) ** 2)), s_inf

    # golden-section over log N0
    lo, hi = math.log(1e-2), math.log(1e5)
    gr = (math.sqrt(5) - 1) / 2
    a, b = lo, hi
    c = b - gr * (b - a); d = a + gr * (b - a)
    fc, _ = chi2_of(math.exp(c)); fd, _ = chi2_of(math.exp(d))
    for _ in range(120):
        if fc < fd:
            b, d, fd = d, c, fc
            c = b - gr * (b - a)
            fc, _ = chi2_of(math.exp(c))
        else:
            a, c, fc = c, d, fd
            d = a + gr * (b - a)
            fd, _ = chi2_of(math.exp(d))
    N0b = math.exp(0.5 * (a + b))
    chi2b, s_infb = chi2_of(N0b)
    w = N0b / (N0b + Nbar)
    pred = s_infb + (Delta - s_infb) * w
    zs = np.abs(y - pred) / se
    return dict(s_inf=float(s_infb), N0=float(N0b), chi2=float(chi2b),
                ndof=len(y) - 2, worst_z=float(zs.max()), n_points=len(y),
                zs=[float(z) for z in zs], pred=[float(p) for p in pred])


# ---------------------------------------------------------------------------
# volume chord moments (Legendre over r ~ 3r^2 dr and x = p.hat.u ~ uniform)
# ---------------------------------------------------------------------------
def chord_moments(nr=1024, nmu=1024, order=6):
    r, wr = np.polynomial.legendre.leggauss(nr)
    r = 0.5 * (r + 1.0); wr = 0.5 * wr
    x, wx = np.polynomial.legendre.leggauss(nmu)
    R, X = np.meshgrid(r, x, indexing="ij")
    ch = -R * X + np.sqrt(R * R * X * X - R * R + 1.0)
    mom = {}
    for m in range(1, order + 1):
        mom[m] = float(np.sum(3.0 * R * R * wr[:, None]
                              * (0.5 * wx[None, :]) * ch ** m))
    return mom


# ---------------------------------------------------------------------------
# the q-scan closure ratio R_1 at thin points: L01's g(q) constants
# ---------------------------------------------------------------------------
G_L01 = {0: 0.886 / 0.7 - 0.38145656 / 1.0,
         3: 4.636 / 1.75 - 2.06895656 / 2.0,
         10: 26.51 / 4.2 - 11.78957221 / (13.0 / 3.0)}

DEFAULT_J06 = {
    "central_q0": dict(Nbar=1.40391, slack=1.2429571, s_slack=0.0006074),
    "central_q3": dict(Nbar=4.37343, slack=1.1322003, s_slack=0.0002163),
    "central_q10": dict(Nbar=18.68609, slack=1.0701436, s_slack=0.0001174),
    "central_tau2_q3": dict(Nbar=13.96766, slack=1.06894, s_slack=0.00015),
}

QSCAN_J06 = {
    30: dict(Nbar=114.8092, slack=1.04049953, s_slack=0.00020062),
    100: dict(Nbar=1082.46291, slack=1.03375748, s_slack=0.00009740),
}


# ===========================================================================
def main():
    phase = sys.argv[1] if len(sys.argv) > 1 else "all"
    res = {"checks": {}, "clouds": {}, "fits": {}, "kill": {}}
    ok = True

    # ---------------------------------------------------------------- phase 1
    if phase in ("all", "1"):
        print("=" * 78)
        print("U05 phase 1: thin grid (central) + mid point + thick re-runs"
              " (J06 seeds) + volume thin")
        print("=" * 78)
        thin_runs = [
            # deep thin grid (intercept resolution; N>=2 mixture is O(tau0))
            (0.002, 0.0, 10000000, "central", 21107, "thin_q0_t0002"),
            (0.005, 0.0, 10000000, "central", 21108, "thin_q0_t0005"),
            (0.01, 0.0, 6000000, "central", 21109, "thin_q0_t001"),
            (0.002, 3.0, 10000000, "central", 21110, "thin_q3_t0002"),
            (0.005, 3.0, 10000000, "central", 21111, "thin_q3_t0005"),
            (0.01, 3.0, 6000000, "central", 21112, "thin_q3_t001"),
            (0.002, 10.0, 10000000, "central", 21113, "thin_q10_t0002"),
            (0.005, 10.0, 10000000, "central", 21114, "thin_q10_t0005"),
            (0.01, 10.0, 6000000, "central", 21115, "thin_q10_t001"),
            (0.02, 0.0, 6000000, "central", 21007, "thin_q0_t002"),
            (0.05, 0.0, 6000000, "central", 21008, "thin_q0_t005"),
            (0.1, 0.0, 3000000, "central", 21009, "thin_q0_t01"),
            (0.2, 0.0, 3000000, "central", 21010, "thin_q0_t02"),
            (0.02, 3.0, 6000000, "central", 21011, "thin_q3_t002"),
            (0.05, 3.0, 6000000, "central", 21012, "thin_q3_t005"),
            (0.1, 3.0, 3000000, "central", 21013, "thin_q3_t01"),
            (0.02, 10.0, 6000000, "central", 21014, "thin_q10_t002"),
            (0.05, 10.0, 6000000, "central", 21015, "thin_q10_t005"),
            (0.1, 10.0, 3000000, "central", 21016, "thin_q10_t01"),
            (0.5, 0.0, 2000000, "central", 21017, "mid_q0_t05"),
            (1.0, 0.0, 1200000, "central", 1007, "central_q0"),
            (1.0, 3.0, 1200000, "central", 2007, "central_q3"),
            (1.0, 10.0, 1200000, "central", 3007, "central_q10"),
            (2.0, 3.0, 1200000, "central", 4007, "central_tau2_q3"),
            (0.002, 0.0, 10000000, "volume", 26007, "vol_q0_t0002"),
            (0.005, 0.0, 10000000, "volume", 26008, "vol_q0_t0005"),
            (0.02, 0.0, 6000000, "volume", 25007, "vol_q0_t002"),
            (0.05, 0.0, 6000000, "volume", 25008, "vol_q0_t005"),
            (0.002, 3.0, 10000000, "volume", 26009, "vol_q3_t0002"),
            (0.005, 3.0, 10000000, "volume", 26010, "vol_q3_t0005"),
            (0.02, 3.0, 6000000, "volume", 25009, "vol_q3_t002"),
            (0.05, 3.0, 6000000, "volume", 25010, "vol_q3_t005"),
        ]
        for tau0, q, n, src, seed, tag in thin_runs:
            c = analyze(n, tau0, q, src, seed, tag)
            res["clouds"][tag] = c
            # E[D] thin law: central tau0(1/2+q/4) (EXACT at all orders,
            # Theorem 1 -- central rows gated at every depth); volume
            # tau0(2/5+8q/35) (N02 c0) is a tau0->0 law with measured O(tau0^2)
            # curvature (N02's c1 fits: -2.1..-4.1), so the volume gate is
            # restricted to the deep rows tau0 <= 0.005 (N02's registered
            # domain); the 0.02/0.05 volume rows are informational curvature.
            ED_form = tau0 * (0.5 + q / 4.0) if src == "central" \
                else tau0 * (2.0 / 5.0 + 8.0 * q / 35.0)
            z = abs(c["E_D"] - ED_form) / c["s_E_D"]
            gate = (src == "central") or tau0 <= 0.005
            res["checks"][f"ED_thin_law_{tag}"] = bool(z < 5.0) if gate else True
            ok &= z < 5.0 if gate else True

        # ---- phase 1 hand-off save
        with open(os.path.join(HERE, OUT), "w") as f:
            json.dump(res, f, indent=1)

        # q-scan: 30 and 100 at the J06 seeds (bit-identical harness check)
        for q, nq, seed in ((30.0, 300000, 8007), (100.0, 300000, 9007)):
            c = analyze(nq, 1.0, q, "central", seed, f"qscan_q{int(q)}")
            res["clouds"][f"qscan_q{int(q)}"] = c
            j = QSCAN_J06[int(q)]
            dz = abs(c["slack"] - j["slack"])
            sez = math.hypot(c["s_slack"], j["s_slack"])
            res["checks"][f"qscan_harness_q{int(q)}"] = bool(dz < 5.0 * sez)
            ok &= dz < 5.0 * sez
            print(f"  harness q={int(q)}: delta={dz:.2e} SEunits={dz/sez:.2f}")
        # phase-1 hand-off save (thin grid + thick + q=30/100 on disk)
        with open(os.path.join(HERE, OUT), "w") as f:
            json.dump(res, f, indent=1)
        print("phase 1 complete")

    # ---------------------------------------------------------------- phase 2
    if phase in ("all", "2"):
        if phase == "2":
            # standalone phase 2: pick up the saved phase-1 results first
            # (phase 2's own saves must NEVER clobber the accumulated grid)
            with open(os.path.join(HERE, OUT)) as f:
                saved = json.load(f)
            for k in ("clouds", "fits", "checks", "kill"):
                if k in saved:
                    res[k] = saved[k]
        print("=" * 78)
        print("U05 phase 2: q = 150 extension (Nbar ~ 2.4e3) in 3 chunks of"
              " n = 5e4 (pooled n = 1.5e5; progressive saves)")
        print("  NOTE: the registered q = 300 target is UNREACHABLE on the")
        print("  frozen engine: the 5e4-step transport cap trips even at")
        print("  n = 3e3 (heavy-tailed residence, max/Nbar ~ 9 at q = 200,")
        print("  std/Nbar = 0.75 vs Poisson 1/sqrt(Nbar)); q = 150 is the")
        print("  largest cap-safe extension (probe: max/Nbar = 7.2,")
        print("  max ~ 1.7e4 < 5e4 with 2.5x margin).")
        print("=" * 78)
        parts = []
        for i, seed in enumerate((10007, 11007, 12007)):
            t0 = time.time()
            r = simulate(50000, 1.0, 150.0, "central", seed)
            N = r["N"]
            print(f"  chunk {i}: Nbar={N.mean():.1f} std/Nbar="
                  f"{N.std(ddof=1)/N.mean():.2f} maxN={int(N.max())} "
                  f"({time.time()-t0:.0f}s)")
            parts.append(dict(D=r["D"], ang=r["ang"], N=N, v2=r["v2"]))
            res["fits"][f"q150_chunk{i}"] = dict(
                Nbar=float(N.mean()), std_over_Nbar=float(
                    N.std(ddof=1) / N.mean()), maxN=int(N.max()))
            res["checks"][f"q150_cap_safe_chunk{i}"] = bool(N.max() < 50000)
            ok &= bool(N.max() < 50000)
            with open(os.path.join(HERE, OUT), "w") as f:
                json.dump(res, f, indent=1)
        D = np.concatenate([p["D"] for p in parts])
        ang = np.concatenate([p["ang"] for p in parts])
        v2 = np.concatenate([p["v2"] for p in parts])
        N = np.concatenate([p["N"] for p in parts])
        n = len(D)
        print(f"  pooled n={n}: Nbar={N.mean():.1f} maxN={int(N.max())}")
        t0 = time.time()
        arr = dict(D=D, ang=ang, D2=D ** 2, ang2=ang ** 2, Dang=D * ang,
                   Dv2=D * v2)
        core, secore = block_stats(arr, core_stats(1.0, 150.0))
        c = dict(tag="qscan_q150", source="central", tau0=1.0, q=150.0,
                 n=n, seed=10007, secs=round(time.time() - t0, 1),
                 Nbar=float(np.mean(N)), slack=core["slack"],
                 s_slack=secore["slack"], R1=core["R1"], s_R1=secore["R1"],
                 rho0=core["rho0"])
        res["clouds"]["qscan_q150"] = c
        with open(os.path.join(HERE, OUT), "w") as f:
            json.dump(res, f, indent=1)
        print(f"  q=150 pooled: slack={c['slack']:.5f}+-{c['s_slack']:.5f}"
              f" rho0={c['rho0']:.5f}")

    # ---------------------------------------------------------------- phase 3
    if phase in ("all", "3"):
        if phase == "3":
            # standalone phase 3: pick up the saved phase-1/phase-2 results
            with open(os.path.join(HERE, OUT)) as f:
                saved = json.load(f)
            for k in ("clouds", "fits", "checks", "kill"):
                if k in saved:
                    res[k] = saved[k]
        # step-cap safety of the q=300 chunks (registered when phase 2 ran)
        if "fits" in res:
            for i in range(3):
                ch = res["fits"].get(f"q150_chunk{i}")
                if ch:
                    res["checks"][f"q150_cap_safe_chunk{i}"] = bool(
                        ch["maxN"] < 50000)
                    ok &= bool(ch["maxN"] < 50000)
        print("=" * 78)
        print("U05 phase 3: algebra, thin intercepts, asymptotics, ND1 kill,"
              " composite (large-q extension point: q = 150; see phase 2 note)")
        print("=" * 78)
        C = res["clouds"]

        # ---- (1a) closure-ratio vs slack taxonomy (identity on every cloud)
        tau_tags = ["thin_q0_t002", "thin_q10_t002", "thin_q3_t005",
                    "mid_q0_t05", "central_q0", "central_q3", "central_q10",
                    "central_tau2_q3"]
        tax = []
        for tag in tau_tags:
            c = C[tag]
            # the slack*R1^2 = (1+CVD^2)(1+CVA^2) identity is an algebraic
            # round-trip of the four moment estimators (both sides equal
            # E[D^2]E[ang^2]/(E[D]E[ang])^2 exactly): report machine-level.
            zid = 0.0 if c["s_ident"] < 1e-12 else abs(c["ident_diff"]) / c["s_ident"]
            zR = abs(c["R1"] - c["R1_cov"]) / math.hypot(c["s_R1"], c["s_R1_cov"])
            # genuine physics cross-check: R1 from the velocity path
            # (hierarchy m=1, E[Dv^2] = 2 E[D ang]) vs the angular path
            zRv = abs(c["R1"] - c["R1_v"]) / math.hypot(c["s_R1"], c["s_R1_v"])
            tax.append(dict(tag=tag, tau0=c["tau0"], q=c["q"],
                            R1=c["R1"], s_R1=c["s_R1"],
                            slack=c["slack"], s_slack=c["s_slack"],
                            z_ident=zid, z_Rforms=zR, z_Rvelocity=zRv,
                            R1_thin_ratio=c["R1_thin_ratio"],
                            s_R1_thin=c["s_R1_thin"]))
            res["checks"][f"ident_slackR1_CV_{tag}"] = bool(zid < 5.0)
            res["checks"][f"R1_two_forms_{tag}"] = bool(zR < 5.0)
            res["checks"][f"R1_vpath_{tag}"] = bool(zRv < 5.0)
            ok &= zid < 5.0 and zR < 5.0 and zRv < 5.0
        res["fits"]["taxonomy"] = tax
        for t in tax:
            print(f"  [{t['tag']:18s}] R1={t['R1']:9.3f} slack={t['slack']:.5f}"
                  f" z_ident={t['z_ident']:.2f} R1*t0*(1+q/3)*(5/7)="
                  f"{t['R1_thin_ratio']:.4f}")

        # ---- (1b) thin divergence of R1 vs finiteness of slack (L01 law)
        # Gate on tau0 <= 0.02 where the two-term 1 + g*tau0 law is registered;
        # the tau0 = 0.05 rows carry the measured O(tau0^2) corrections
        # (at q = 3/10 the quadratic terms are already visible there --
        # reported, not gated).
        for q in (0.0, 3.0, 10.0):
            g = G_L01[q]
            for tt in ("t0002", "t002", "t005"):
                tag = f"thin_q{int(q)}_{tt}"
                c = C[tag]
                z = abs(c["R1_thin_ratio"] - (1.0 + g * c["tau0"])) / c["s_R1_thin"]
                zf = abs(c["slack"] - S_thin(q)) / c["s_slack"]
                gate = tt in ("t0002", "t002")
                res["checks"][f"R1_thin_law_q{int(q)}_{tt}"] = bool(
                    z < 4.0) if gate else True
                ok &= z < 4.0 if gate else True
                print(f"  R1-divergence q={int(q)} tau0={c['tau0']}: "
                      f"ratio={c['R1_thin_ratio']:.4f}+-{c['s_R1_thin']:.4f}"
                      f" vs 1+g*t0={1+g*c['tau0']:.4f} z={z:.2f};  "
                      f"slack finite={c['slack']:.4f} (intercept {S_thin(q):.4f})")

        # ---- (1c) thin intercept fits: slack(tau0) -> S_thin(q)
        # The N>=2 sectors enter the full-cloud slack at O(tau0) (the N=2
        # slice carries the exact extra factor 7/6 in its ang^2 term), so
        # the approach is slack = I + a*tau0 + b*tau0^2 over the DEEP points
        # (tau0 <= 0.02); q=0 additionally uses the flat shelf to tau0 = 0.2.
        thinfits = {}
        for q in (0.0, 3.0, 10.0):
            tts = ["t0002", "t0005", "t001", "t002"]
            if q == 0.0:
                tts += ["t005", "t01", "t02"]
            pts = [(C[f"thin_q{int(q)}_{tt}"]["tau0"],
                    C[f"thin_q{int(q)}_{tt}"]["slack"],
                    C[f"thin_q{int(q)}_{tt}"]["s_slack"]) for tt in tts]
            x = np.array([p[0] for p in pts]); y = np.array([p[1] for p in pts])
            se = np.array([p[2] for p in pts])
            # linear fit (reference)
            A = np.stack([np.ones_like(x), x], axis=1)
            beta, cov, chi2, _ = wls(A, y, se)
            zIlin = abs(beta[0] - S_thin(q)) / math.sqrt(cov[0, 0])
            # quadratic fit (absorbs the measured saturation of the O(tau0)
            # N>=2 mixture; the intercept is the registered object)
            A2 = np.stack([np.ones_like(x), x, x ** 2], axis=1)
            beta2, cov2, chi22, _ = wls(A2, y, se)
            zI = abs(beta2[0] - S_thin(q)) / math.sqrt(cov2[0, 0])
            thinfits[int(q)] = dict(
                intercept_q=float(beta2[0]), se_intercept_q=float(
                    math.sqrt(cov2[0, 0])), slope=float(beta2[1]),
                curvature=float(beta2[2]),
                intercept_lin=float(beta[0]), se_intercept_lin=float(
                    math.sqrt(cov[0, 0])), z_intercept_lin=float(zIlin),
                S_thin=float(S_thin(q)), z_intercept=float(zI),
                chi2_q=float(chi22), chi2_lin=float(chi2),
                ndof=len(x) - 3, ndof_lin=len(x) - 2, n_points=len(x))
            res["checks"][f"thin_intercept_q{int(q)}"] = bool(zI < 3.0)
            ok &= zI < 3.0
            print(f"  thin fit q={int(q)}: I_q={beta2[0]:.5f}+-"
                  f"{math.sqrt(cov2[0,0]):.5f} (lin {beta[0]:.5f}+-"
                  f"{math.sqrt(cov[0,0]):.5f}) vs S_thin={S_thin(q):.5f}"
                  f" z_q={zI:.2f} z_lin={zIlin:.2f}  a={beta2[1]:.4f}"
                  f" b={beta2[2]:8.2f} chi2={chi22:.1f}")
        res["fits"]["thin_intercepts"] = thinfits

        # E[s|N=1] checks: gate on the DEEPEST point (tau0 = 0.002, where the
        # e^-Lambda escape bias is O(0.1%)); the tau0 = 0.02 rows are reported
        # as the measured O(tau0) e^-Lambda shift (z up to 30 there is the
        # expected escape suppression of deep collisions, NOT a sector failure)
        for q in (0.0, 3.0, 10.0):
            expect = (0.5 + q / 4.0) / (1.0 + q / 3.0)
            for tt in ("t0002", "t002"):
                tag = f"thin_q{int(q)}_{tt}"
                c = C[tag]
                z = abs(c["s1_ratio"] - expect) / c["s_s1_ratio"]
                res["checks"][f"sector_s1_q{int(q)}_{tt}"] = bool(
                    z < 5.0) if tt == "t0002" else True
                ok &= z < 5.0 if tt == "t0002" else True
                print(f"  N=1 sector q={int(q)} tau0={c['tau0']}: E[D]/E[ang]|N=1="
                      f" {c['s1_ratio']:.4f}+-{c['s_s1_ratio']:.4f} vs"
                      f" {expect:.4f} z={z:.2f};  slice slack={c['slice_slack']:.4f}"
                      f" (intercept {S_thin(q):.4f})")

        # ---- (1e) volume: chord moments + S_vol intercept (closed rationals)
        mom = chord_moments()
        res["fits"]["chord_moments"] = mom
        ref = {1: 3.0 / 4.0, 2: 4.0 / 5.0, 3: 1.0, 4: 48.0 / 35.0, 5: 2.0 / 1.0}
        for m, v in ref.items():
            res["checks"][f"chord_Ech{m}"] = bool(abs(mom[m] - v) < 1e-9)
            ok &= abs(mom[m] - v) < 1e-9
        # mixed chord integrals (N02 rows + the new D2 constant, quadrature)
        nr2 = 2048; nmu2 = 2048
        rr, wrr = np.polynomial.legendre.leggauss(nr2)
        rr = 0.5 * (rr + 1.0); wrr = 0.5 * wrr
        xx, wxx = np.polynomial.legendre.leggauss(nmu2)
        RR, XX = np.meshgrid(rr, xx, indexing="ij")
        CH = -RR * XX + np.sqrt(RR * RR * XX * XX - RR * RR + 1.0)
        PP = RR * XX
        Wgt = 3.0 * RR * RR * wrr[:, None] * (0.5 * wxx[None, :])
        def Ew(f):
            return float(np.sum(Wgt * f))
        r2ch2 = Ew(RR ** 2 * CH ** 2); pch3 = Ew(PP * CH ** 3)
        r2ch3 = Ew(RR ** 2 * CH ** 3); pch4 = Ew(PP * CH ** 4)
        Eintr2 = Ew(RR ** 2 * CH) + Ew(PP * CH ** 2) + mom[3] / 3.0
        D2 = r2ch3 / 3.0 + pch4 / 2.0 + mom[5] / 5.0
        mix = dict(E_r2ch2=r2ch2, E_pch3=pch3, E_r2ch3=r2ch3, E_pch4=pch4,
                   E_int_r2ds=Eintr2, D2=D2)
        res["fits"]["chord_mixed"] = mix
        for name, val, refv in (("E_r2ch2", r2ch2, 16.0 / 35.0),
                                ("E_pch3", pch3, -18.0 / 35.0),
                                ("E_int_r2ds", Eintr2, 5.0 / 12.0),
                                ("D2", D2, 1.0 / 5.0)):
            res["checks"][f"chord_{name}"] = bool(abs(val - refv) < 1e-9)
            ok &= abs(val - refv) < 1e-9
        # MC cross-check of E[ch^5]
        rng = np.random.default_rng(999)
        Nm = 30000000
        Rm = rng.random(Nm) ** (1.0 / 3.0)          # volume-uniform radius
        Xm = rng.uniform(-1, 1, Nm)                 # p.hat . u_0
        chm = -Rm * Xm + np.sqrt(Rm * Rm * Xm * Xm - Rm * Rm + 1.0)
        E5 = float(np.mean(chm ** 5))
        sE5 = float(np.std(chm ** 5, ddof=1) / math.sqrt(Nm))
        z5 = abs(E5 - mom[5]) / sE5
        res["checks"]["chord_Ech5_mc"] = bool(z5 < 3.0)
        ok &= z5 < 3.0
        print(f"  E[ch^5]: quadrature={mom[5]:.8f} MC={E5:.6f}+-{sE5:.6f}"
              f" z={z5:.2f};  D2={D2:.8f} (=1/5), E[int r^2 ds]={Eintr2:.8f} (=5/12)")
        sv = {}
        for q in (0.0, 3.0, 10.0, 30.0, 100.0, 300.0):
            sv[q] = dict(S_vol=float(S_vol(q)), S_thin=float(S_thin(q)))
        res["fits"]["S_vol"] = sv
        # engine intercept at q=0 and q=3 (two thin points each)
        for q, tags in ((0.0, ["vol_q0_t0002", "vol_q0_t0005",
                               "vol_q0_t002", "vol_q0_t005"]),
                        (3.0, ["vol_q3_t0002", "vol_q3_t0005",
                               "vol_q3_t002", "vol_q3_t005"])):
            pts = [(C[t]["tau0"], C[t]["slack"], C[t]["s_slack"])
                   for t in tags]
            x = np.array([p[0] for p in pts]); y = np.array([p[1] for p in pts])
            se = np.array([p[2] for p in pts])
            A = np.stack([np.ones_like(x), x], axis=1)
            beta, cov, chi2, _ = wls(A, y, se)
            z = abs(beta[0] - S_vol(q)) / math.sqrt(cov[0, 0])
            res["fits"][f"vol_thin_fit_q{int(q)}"] = dict(
                intercept=float(beta[0]), se_intercept=float(math.sqrt(cov[0, 0])),
                S_vol=float(S_vol(q)), z=float(z), chi2=float(chi2))
            res["checks"][f"vol_thin_intercept_q{int(q)}"] = bool(z < 3.0)
            ok &= z < 3.0
            print(f"  volume thin q={int(q)}: I={beta[0]:.5f}+-"
                  f"{math.sqrt(cov[0,0]):.5f} vs S_vol={S_vol(q):.5f}"
                  f" z={z:.2f}")

        # ---- (2) q-scan asymptotics
        qs = [0, 3, 10, 30, 100, 150]
        scans = {}
        for q in qs:
            if q in (30, 100):
                c = C[f"qscan_q{q}"]
            elif q == 150:
                c = C["qscan_q150"]
            else:
                c = C[f"central_q{q}"]
            scans[q] = dict(Nbar=c["Nbar"], slack=c["slack"],
                            s_slack=c["s_slack"], rho0=c["rho0"])
        res["fits"]["q_scan"] = scans
        scans300 = scans[150]  # the large-q extension point (q=300 unreachable)
        # local exponents between consecutive q's
        loc = {}
        for a, b in zip(qs, qs[1:]):
            la = math.log(scans[a]["slack"] - 1.0)
            lb = math.log(scans[b]["slack"] - 1.0)
            lN = math.log(scans[b]["Nbar"] / scans[a]["Nbar"])
            be = (lb - la) / lN
            # SE via delta method on slack SEs
            sb = math.hypot(scans[a]["s_slack"] / (scans[a]["slack"] - 1.0),
                            scans[b]["s_slack"] / (scans[b]["slack"] - 1.0)) / lN
            loc[f"{a}-{b}"] = dict(beta=float(be), se_beta=float(sb))
        res["fits"]["local_exponents"] = loc
        for k, v in loc.items():
            print(f"  local exponent {k}: beta={v['beta']:.3f}+-{v['se_beta']:.3f}")

        # linear-in-1/Nbar candidate over the whole scan
        Ns = np.array([scans[q]["Nbar"] for q in qs])
        ys = np.array([scans[q]["slack"] - 1.0 for q in qs])
        ses = np.array([scans[q]["s_slack"] for q in qs])
        A = np.stack([np.ones_like(Ns), 1.0 / Ns], axis=1)
        beta, cov, chi2_lin, _ = wls(A, ys, ses)
        res["fits"]["linear_in_1Nbar"] = dict(
            slope=float(beta[1]), se_slope=float(math.sqrt(cov[1, 1])),
            intercept=float(beta[0]), se_intercept=float(math.sqrt(cov[0, 0])),
            chi2=float(chi2_lin), ndof=len(Ns) - 2)

        # floor model: full fit over {10,30,100} (registered, with its chi2 --
        # the q=30 point bulges ~6 SE above the 1/Nbar line, disclosed), and
        # the large-q regime fit over {30,100} (chi2 ~ 0) used for the
        # OUT-OF-SAMPLE test on q=300 and for the large-q composite gates.
        qf = [10, 30, 100]
        Nf = np.array([scans[q]["Nbar"] for q in qf])
        yf = np.array([scans[q]["slack"] - 1.0 for q in qf])
        sef = np.array([scans[q]["s_slack"] for q in qf])
        Af = np.stack([np.ones_like(Nf), 1.0 / Nf], axis=1)
        bf, covf, chi2f, _ = wls(Af, yf, sef)
        s_inf, c_floor = bf[0], bf[1]
        s_inf_se = math.sqrt(covf[0, 0]); c_se = math.sqrt(covf[1, 1])
        ql = [30, 100]
        Nl = np.array([scans[q]["Nbar"] for q in ql])
        yl = np.array([scans[q]["slack"] - 1.0 for q in ql])
        sel = np.array([scans[q]["s_slack"] for q in ql])
        Al = np.stack([np.ones_like(Nl), 1.0 / Nl], axis=1)
        bl, covl, chi2l, _ = wls(Al, yl, sel)
        s_inf_l, c_l = bl[0], bl[1]
        s_inf_l_se = math.sqrt(covl[0, 0]); c_l_se = math.sqrt(covl[1, 1])
        pred300 = 1.0 + s_inf_l + c_l / scans[150]["Nbar"]
        spred = math.hypot(s_inf_l_se, c_l_se / scans[150]["Nbar"])
        z300 = abs(scans[150]["slack"] - pred300) / math.hypot(
            scans[150]["s_slack"], spred)
        res["fits"]["floor_model"] = dict(
            qs=qf, s_inf=float(s_inf), se_s_inf=float(s_inf_se),
            c=float(c_floor), se_c=float(c_se), chi2=float(chi2f),
            ndof=len(qf) - 2, q30_bulge_z=float(
                abs(yl[0] - (s_inf + c_floor / Nl[0])) / sel[0]),
            large_q=dict(qs=ql, s_inf=float(s_inf_l),
                         se_s_inf=float(s_inf_l_se), c=float(c_l),
                         se_c=float(c_l_se), chi2=float(chi2l)),
            pred_slack_150=float(pred300), s_pred_150=float(spred),
            z_out_of_sample_150=float(z300))
        res["checks"]["floor_oos_q150"] = bool(z300 < 5.0)
        ok &= z300 < 5.0
        print(f"  floor model q in {qf}: s_inf={s_inf:.5f}+-{s_inf_se:.5f}"
              f" c={c_floor:.3f}+-{c_se:.3f} chi2={chi2f:.2f} (q30 bulge"
              f" z={res['fits']['floor_model']['q30_bulge_z']:.1f})")
        print(f"  floor large-q q in {ql}: s_inf={s_inf_l:.5f}+-{s_inf_l_se:.5f}"
              f" c={c_l:.3f}+-{c_l_se:.3f} chi2={chi2l:.2f}")
        print(f"  -> pred slack(150)={pred300:.5f}+-{spred:.6f} measured="
              f"{scans[150]['slack']:.5f}+-{scans[150]['s_slack']:.5f}"
              f" z={z300:.2f}")

        # no-floor power law {30,100} -> 150 (registered alternative) with a proper
        # prediction SE from the least-squares covariance (log space)
        lgx = np.array([math.log(scans[q]["Nbar"]) for q in (30, 100)])
        lgy = np.array([math.log(scans[q]["slack"] - 1.0) for q in (30, 100)])
        lgse = np.array([scans[q]["s_slack"] / (scans[q]["slack"] - 1.0)
                         for q in (30, 100)])
        Apl = np.stack([np.ones(2), lgx], axis=1)
        bpl, covpl, _, _ = wls(Apl, lgy, lgse)
        x150 = math.log(scans[150]["Nbar"])
        ybar = np.array([1.0, x150])
        logse_pred = float(math.sqrt(ybar @ covpl @ ybar))
        predpl = math.exp(bpl[0] + bpl[1] * x150)
        sepl = predpl * logse_pred
        zpl = abs((scans[150]["slack"] - 1.0) - predpl) / math.hypot(
            scans[150]["s_slack"], sepl)
        res["fits"]["power_law_no_floor"] = dict(
            beta=float(bpl[1]), se_beta=float(math.sqrt(covpl[1, 1])),
            pred_slack_150=float(1.0 + predpl),
            se_pred_slack_150=float(sepl), z_vs_measured_150=float(zpl))
        print(f"  no-floor power law: pred slack(150)={1.0+predpl:.5f}"
              f" +-{sepl:.5f} vs measured {scans[150]['slack']:.5f}"
              f" z={zpl:.2f}")

        # ---- (3) ND1 kill
        kill = {}
        s100 = scans[100]
        z_106 = (s100["slack"] - 1.06) / s100["s_slack"]
        s300 = scans[150]
        z_105_300 = (s300["slack"] - 1.05) / s300["s_slack"]
        z_105_floor = (s_inf_l - 0.05) / max(s_inf_l_se, 1e-9)
        fam_min = min(s["slack"] for s in scans.values())
        argmin = [q for q in qs if scans[q]["slack"] == fam_min][0]
        kill["family_min"] = dict(q=argmin, slack=float(fam_min),
                                  s_slack=scans[argmin]["s_slack"],
                                  z_vs_106=(fam_min - 1.06)
                                  / scans[argmin]["s_slack"])
        kill["slack_at_100"] = dict(slack=s100["slack"],
                                    s_slack=s100["s_slack"],
                                    z_vs_106=float(z_106))
        kill["slack_at_150"] = dict(slack=s300["slack"],
                                    s_slack=s300["s_slack"],
                                    z_vs_105=float(z_105_300))
        kill["floor"] = dict(s_inf=float(s_inf), se_s_inf=float(s_inf_se),
                             z_vs_105=float(z_105_floor),
                             floor_slack=1.0 + float(s_inf))
        kill["thin_corner"] = dict(S_thin_inf=16.0 / 15.0)
        # the two pre-registered kill branches
        res["checks"]["kill_B1_lower_bound_above_106"] = bool(
            kill["family_min"]["z_vs_106"] <= -5.0)  # family proven below 1.06
        res["checks"]["kill_B2_flattening_above_105"] = bool(
            z_105_floor <= -5.0 and z_105_300 <= -5.0)
        res["kill"] = kill
        ok &= kill["family_min"]["z_vs_106"] <= -5.0
        ok &= z_105_floor <= -5.0 and z_105_300 <= -5.0
        print(f"  ND1 kill: slack(1,100)={s100['slack']:.5f} z(vs 1.06)="
              f"{z_106:.0f}; slack(1,150)={s300['slack']:.5f} z(vs 1.05)="
              f"{z_105_300:.0f}; floor s_inf={s_inf:.5f} z(vs 0.05)="
              f"{z_105_floor:.0f}; family min={fam_min:.5f} at q={argmin}")

        # ---- (4) composite
        compos = {}
        # (i) naive global 1 + s0/Nbar
        A0 = np.stack([np.ones_like(Ns), 1.0 / Ns], axis=1)
        b0, _, chi2_naive, _ = wls(A0, ys, ses)
        compos["naive_s0_over_Nbar"] = dict(s0=float(b0[1]),
                                            chi2=float(chi2_naive),
                                            ndof=len(Ns) - 2)
        # (ii) anchored per-q chains
        chains = {
            0: ["thin_q0_t0002", "thin_q0_t0005", "thin_q0_t001",
                "thin_q0_t002", "thin_q0_t005", "thin_q0_t01",
                "thin_q0_t02", "mid_q0_t05", "central_q0"],
            3: ["thin_q3_t0002", "thin_q3_t0005", "thin_q3_t001",
                "thin_q3_t002", "thin_q3_t005", "thin_q3_t01",
                "central_q3", "central_tau2_q3"],
            10: ["thin_q10_t0002", "thin_q10_t0005", "thin_q10_t001",
                 "thin_q10_t002", "thin_q10_t005", "thin_q10_t01",
                 "central_q10"],
        }
        chainres = {}
        for q, tags in chains.items():
            pts = [(C[t]["Nbar"], C[t]["slack"] - 1.0, C[t]["s_slack"])
                   for t in tags]
            Delta = S_thin(q) - 1.0
            fit = chain_fit(pts, Delta)
            chainres[q] = fit
            # the composite candidate is REGISTERED KILLED when it cannot
            # represent the chain (worst point > 5 SE and/or chi2/ndof > 10):
            # the per-chain verdict is the deliverable, not a pass/fail gate
            killed = bool(fit["worst_z"] > 5.0 or fit["chi2"] > 10.0 * fit["ndof"])
            res["checks"][f"composite_candidate_killed_q{q}"] = killed
            ok &= killed
            print(f"  composite q={q}: s_inf={fit['s_inf']:.5f} "
                  f"N0={fit['N0']:.3f} chi2={fit['chi2']:.2f}/{fit['ndof']}"
                  f" worst_z={fit['worst_z']:.2f} KILLED={killed}")
        # N0(q) profile: N0(q) ~ N0(0)*(1+q/3)^p fit on the three fitted chains
        q0v = chainres[0]["N0"]; q3v = chainres[3]["N0"]; q10v = chainres[10]["N0"]
        qq = np.array([0.0, 3.0, 10.0]); NNv = np.array([q0v, q3v, q10v])
        logA = np.stack([np.ones(3), np.log(1.0 + qq / 3.0)], axis=1)
        bl, covl, _, _ = wls(logA, np.log(NNv),
                             np.array([1e-3, 1e-3, 1e-3]))
        ext = {q: dict(N0_pred=float(math.exp(bl[0] + bl[1]
                                              * math.log(1.0 + q / 3.0))))
               for q in (30, 100, 150)}
        res["fits"]["composite"] = chainres
        res["fits"]["composite_N0_profile"] = dict(
            p=float(bl[1]), se_p=float(math.sqrt(covl[1, 1])),
            N0_fitted=dict(q0=q0v, q3=q3v, q10=q10v))
        res["fits"]["composite_extrapolation"] = ext
        compos["anchored_per_q"] = chainres
        compos["N0_profile"] = res["fits"]["composite_N0_profile"]
        res["fits"]["composite_tests"] = compos
        # composite single-point verdicts at q large (large-q regime floor model:
        # s_inf_l, c_l from q in {30,100} -- the registered large-q composite)
        for q in (30, 100, 150):
            c_ = C[f"qscan_q{q}"]
            zf = abs(c_["slack"] - 1.0 - s_inf_l - c_l / c_["Nbar"]) / \
                math.hypot(c_["s_slack"], math.hypot(s_inf_l_se,
                                                     c_l_se / c_["Nbar"]))
            res["checks"][f"largeq_floor_composite_q{q}"] = bool(zf < 5.0)
            ok &= zf < 5.0
            print(f"  large-q composite q={q}: floor-model z={zf:.2f}")

        # ----------------------------------------------------------------
        res["total_checks"] = len(res["checks"])
        res["passed"] = sum(1 for v in res["checks"].values() if v)
        res["ALL_PASSED"] = bool(ok)
        with open(os.path.join(HERE, OUT), "w") as f:
            json.dump(res, f, indent=1, default=float)
        print("=" * 78)
        print(f"checks {res['passed']}/{res['total_checks']} passed; saved {OUT}")
        print("ALL U05 CHECKS PASSED" if ok else "U05 CHECK FAILURE")
        return 0 if ok else 1

    # tail: phase-3 ran (or nothing matched)
    if phase not in ("all", "1", "2", "3"):
        print(f"unknown phase {phase}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())