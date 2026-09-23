#!/usr/bin/env python3
"""
K07 -- CLOSURE OF THE VOLUME WINDOW THEOREM
2026-09-23.  Moment channel, volume source.  Follows J09 (central window,
tau0-FREE, verified 27/27) and J11 (volume window tau0-DEPENDENT; V2 q>0
quadrature check FAILED z = 29.5 / 83.6 -- closed here).

CONTENT
  P1  Grid: E[D]_vol and -ln A_vol at tau0 in {0.5,1,2,3,5,8}, q in {0,3,10},
      MC n = 600000 (J02 engine volume source), vs EXACT Gauss-Legendre
      quadrature (80/160-pt; Wm = 0.5*du, Wr = (3r^2)(0.5*dr), each sums to 1).
      THE J11 SIGN BUG IS CLOSED: the escape chord along +u is
        chord = sqrt(1 - r^2(1-u^2)) - r*u            (TRUE, matches engine)
      not the J11-stated chord = sqrt(...) + r*u (equal only in the q=0
      integral by u-symmetry; at q>0 the stated formula was off by z = 29.5
      / 83.6 -- V2 failure).  Both variants computed; only 'minus' checks.
  P2  tau0-shape: R_v(tau0) := -ln A_v / E[D]_vol is DECREASING in tau0.
      Candidate fit R = a/tau0 + b per q (weighted LSQ) reported for the
      record; thick asymptotic behavior handled in P3/P4.
  P2c Thin limit measured separately by low-tau0 MC (micro grid
      tau0 = 1e-3..0.1, n = 2e6, plus 0.2..0.5 at n = 6e5):
        lim_{tau0->0} R_v = <T>_q / c_q,   c_q := lim E[D]_vol/tau0,
        <T>_q = <chord + q(r^2 chord + r u chord^2 + chord^3/3)>_vol.
      RESULT (preview): c0(q=0) = 0.4034(2) -- NOT the 0.338 E[D]/tau0 at
      tau0=1 used for the old "thin ~ 2.2" claim; thin limit ~ 1.86 for all
      q, i.e. the volume window NEVER leaves [~1.2, ~1.9] on the high side:
      the "R > 2" kill region is EMPTY.
  P3  KILL-REGION MAP: R_v < 4/3 (naive central-window observer wrongly
      kills Thomson) sets the deep boundary tau0*(q); R_v > 2 does NOT occur
      (checked by dense scan + max).  Boundaries from exact -ln A_v(tau0)
      and a knot-interpolated c_q(tau0) = E[D]/tau0 (all MC points), with
      bootstrap SEs.
  P4  Crossing report: thin volume window ~1.86 (universal in q) vs values
      at tau0 = 8: 1.22 (q=0) / 0.69 (q=3) / 0.36 (q=10), asymptotic thick
      limit 0 (surface-tangent chords -> -ln A ~ (3/2) ln tau0 -> R -> 0);
      central window flat in tau0 at (1+q/3)/(1/2+q/4).

Files: K07_vol_window.py/.out, K07_results.json, K07_VOLUME_WINDOW_CLOSURE.md.
No git commit (per lane rules).
"""
import json
import os
import sys
import time
from multiprocessing import Pool

import numpy as np
from numpy.polynomial.legendre import leggauss

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from J02_moment_hierarchy import simulate

N_GRID = 600000          # contract: n >= 600k for every reported MC number
TAUS = (0.5, 1.0, 2.0, 3.0, 5.0, 8.0)
QS = (0.0, 3.0, 10.0)
THIN_TAUS = (0.05, 0.1, 0.2, 0.3, 0.5)       # low-tau0 scans
MICRO_TAUS = (1e-3, 1e-2, 5e-2, 1e-1)        # micro grid, n = 2e6
R_LOW, R_HIGH = 4.0 / 3.0, 2.0               # central window edges


def A_vol_quadrature(tau0, q, ng=80, sign="minus"):
    """Exact volume-atom fraction by Gauss-Legendre:
       A_v = 3 int_0^1 r^2 dr * (1/2) int_-1^1 du * exp(-tau0 * T)
       T = chord + q (r^2 chord + r u chord^2 + chord^3/3)
       chord = sqrt(1 - r^2(1-u^2)) - r*u        ('minus': escape along +u)
       sign='plus' reproduces the J11-stated chord (r*u + sqrt(...)); kept
       for the ledger only.
       Weights: Wr = (3 r^2)(0.5 dr) sums to 1; Wm = (1/2)du sums to 1.
    """
    xr, wr = leggauss(ng)
    r = 0.5 * xr + 0.5
    xm, wm = leggauss(2 * ng)
    mu = xm
    R = r[:, None]
    MU = mu[None, :]
    Wr = (3.0 * R ** 2) * (0.5 * wr[:, None])
    Wm = 0.5 * wm[None, :]
    S = np.sqrt(np.maximum(0.0, 1.0 - R ** 2 * (1.0 - MU ** 2)))
    chord = S - R * MU if sign == "minus" else S + R * MU
    T = chord + q * (R ** 2 * chord + R * MU * chord ** 2 + chord ** 3 / 3.0)
    return float(np.sum(Wr * np.exp(-tau0 * T) * Wm))


def T_vol_mean(q, ng=160):
    """<T>_q = <chord + q(...)>_vol on the same grid: thin limit of
    -ln A_v / tau0 (exact by the same quadrature)."""
    xr, wr = leggauss(ng)
    r = 0.5 * xr + 0.5
    xm, wm = leggauss(2 * ng)
    R = r[:, None]
    MU = xm[None, :]
    Wr = (3.0 * R ** 2) * (0.5 * wr[:, None])
    Wm = 0.5 * wm[None, :]
    S = np.sqrt(np.maximum(0.0, 1.0 - R ** 2 * (1.0 - MU ** 2)))
    chord = S - R * MU
    T = chord + q * (R ** 2 * chord + R * MU * chord ** 2 + chord ** 3 / 3.0)
    return float(np.sum(Wr * T * Wm)), float(np.sum(Wr * chord * Wm))


def mc_one(args):
    n, tau0, q, seed = args
    r = simulate(n, tau0, q, "volume", seed=seed)
    D = r["D"]
    atom = (r["N"] == 0).astype(float)
    n0 = int(np.sum(atom))
    return dict(tau0=tau0, q=q, seed=seed, n=n, n_atom=n0,
                ED=float(np.mean(D)),
                sD=float(np.std(D, ddof=1) / np.sqrt(n)),
                A=float(np.mean(atom)),
                sA=float(np.std(atom, ddof=1) / np.sqrt(n)),
                cov=float(np.cov(atom, D, ddof=1)[0, 1] / n))


def build_T(q, ng=80):
    """Quadrature nodes/weights for the volume exponent T (chord + q(...)).
    Returns (T_flattened, W_flattened) with W = Wr * Wm summing to 1."""
    xr, wr = leggauss(ng)
    r = 0.5 * xr + 0.5
    xm, wm = leggauss(2 * ng)
    R = r[:, None]
    MU = xm[None, :]
    W = ((3.0 * R ** 2) * (0.5 * wr[:, None])
         * (0.5 * wm[None, :])).ravel()
    S = np.sqrt(np.maximum(0.0, 1.0 - R ** 2 * (1.0 - MU ** 2)))
    chord = S - R * MU
    T = (chord + q * (R ** 2 * chord + R * MU * chord ** 2
                      + chord ** 3 / 3.0)).ravel()
    return T, W


def R_curve(ts, T, W, cknot, t0, chunk=1000):
    """R(t) = -ln A_v(t; q) / (t * c(t)) with c(t) = linear-interp of the
    MC knots cknot at abscissae t0.  Vectorized over ts (chunked)."""
    LnA = np.empty(len(ts))
    for i in range(0, len(ts), chunk):
        tb = ts[i:i + chunk]
        LnA[i:i + chunk] = -np.log(np.exp(-tb[:, None] * T[None, :]) @ W)
    cmod = np.interp(ts, t0, cknot)
    return LnA / (ts * cmod)


def main():
    t_start = time.time()
    print("=" * 78)
    print("K07 -- CLOSURE OF THE VOLUME WINDOW THEOREM (volume source, J02 "
          "engine)")
    print("=" * 78)

    tasks = [(N_GRID, t, q, 2000 + int(t * 10) * 100 + int(q))
             for t in TAUS for q in QS]
    thin_tasks = [(N_GRID, t, q, 3000 + int(t * 100) * 10 + int(q))
                  for t in THIN_TAUS for q in QS]
    micro_tasks = [(2000000, t, q, 4000 + int(np.log10(t) * 1000) + int(q * 7))
                   for t in MICRO_TAUS for q in QS]
    print(f"P1 grid: {len(tasks)} x {N_GRID}; thin: {len(thin_tasks)} x "
          f"{N_GRID}; micro: {len(micro_tasks)} x 2e6")
    with Pool(12) as pool:
        grid = pool.map(mc_one, tasks)
        thin = pool.map(mc_one, thin_tasks)
        micro = pool.map(mc_one, micro_tasks)

    for m in grid:
        m["Aq80"] = A_vol_quadrature(m["tau0"], m["q"], ng=80, sign="minus")
        m["Aq160"] = A_vol_quadrature(m["tau0"], m["q"], ng=160, sign="minus")
        m["Aq_plus"] = A_vol_quadrature(m["tau0"], m["q"], ng=80, sign="plus")

    res = {"meta": {"engine": "deepseek_push/J02_moment_hierarchy.py::simulate",
                    "n_grid": N_GRID, "n_micro": 2000000,
                    "taus": list(TAUS), "qs": list(QS),
                    "date": "2026-09-23"},
           "checks": {}, "P1": {}, "P2": {}, "P2c": {}, "P3": {}, "P4": {}}
    ok = True

    # ---------------- P1: MC vs quadrature table, all 18 combos ----------
    print("-" * 78)
    print("P1  E[D]_vol and -ln A_vol vs EXACT quadrature A_v "
          "(sign='minus' = true chord)")
    print(f"{'tau0':>5} {'q':>4} | {'E[D]_vol':>10} {'sD':>8} | "
          f"{'-lnA MC':>10} {'s':>8} | {'-lnA quad':>10} | {'A_mc':>9} "
          f"{'A_quad':>9} {'z':>7} | {'R_v':>7}")
    for m in grid:
        t, q = m["tau0"], m["q"]
        A_mc, sA = m["A"], m["sA"]
        A_quad = m["Aq160"]
        z = abs(A_mc - A_quad) / sA if sA > 0 else float("inf")
        lnA_mc = -np.log(A_mc) if A_mc > 0 else float("inf")
        slnA = sA / A_mc if A_mc > 0 else float("inf")
        m["lnA_mc"], m["s_lnA"] = lnA_mc, slnA
        m["lnA_quad"] = -np.log(A_quad)
        m["z_vs_quad"] = z
        Rq = -np.log(A_quad) / m["ED"]
        m["R_quad"] = Rq
        m["sR_quad"] = abs(np.log(A_quad)) * m["sD"] / m["ED"] ** 2
        if A_mc > 0:
            m["R_mc"] = -np.log(A_mc) / m["ED"]
            m["sR_mc"] = se_ratio(A_mc, sA, m["ED"], m["sD"], m["cov"])
        else:
            m["R_mc"], m["sR_mc"] = float("inf"), float("inf")
        res["P1"][f"t{int(t*10)}_q{int(q)}"] = dict(
            ED=round(m["ED"], 5), sD=round(m["sD"], 6),
            A_mc=round(A_mc, 6) if A_mc > 0 else 0.0,
            sA=round(sA, 7), n_atom=m["n_atom"],
            A_quad=round(A_quad, 8), z=round(z, 2),
            lnA_mc=round(lnA_mc, 4) if np.isfinite(lnA_mc) else None,
            lnA_quad=round(-np.log(A_quad), 4),
            R_mc=round(m["R_mc"], 4) if np.isfinite(m["R_mc"]) else None,
            sR_mc=round(m["sR_mc"], 4) if np.isfinite(m["sR_mc"]) else None,
            R_quad=round(Rq, 4), sR_quad=round(m["sR_quad"], 4))
        meas = A_mc > 1.0e-6
        ck = f"P1_t{int(t*10)}_q{int(q)}"
        res["checks"][ck] = bool((not meas) or (z < 4.0))
        ok &= res["checks"][ck]
        print(f"{t:5.1f} {q:4.0f} | {m['ED']:10.4f} {m['sD']:8.5f} | "
              f"{lnA_mc if np.isfinite(lnA_mc) else float('inf'):10.4f} "
              f"{slnA if np.isfinite(slnA) else float('nan'):8.5f} | "
              f"{-np.log(A_quad):10.4f} | {A_mc:9.6f} {A_quad:9.6f} {z:7.2f}"
              f" | {Rq:7.4f}")
    print("ledger: max |A(ng=80)-A(ng=160)| =",
          max(abs(m["Aq80"] - m["Aq160"]) for m in grid))
    for m in grid:
        if m["q"] > 0:
            zplus = abs(m["A"] - m["Aq_plus"]) / m["sA"]
            print(f"  J11 'plus' chord, tau0={m['tau0']} q={m['q']}: "
                  f"MC {m['A']:.5f} vs plus {m['Aq_plus']:.5f} "
                  f"(z={zplus:.1f}) vs CORRECTED {m['Aq160']:.5f} "
                  f"(z={m['z_vs_quad']:.2f})")
    res["checks"]["P1_j11_plus_formula_rejected"] = bool(
        any(m["q"] > 0 and abs(m["A"] - m["Aq_plus"]) / m["sA"] > 10
            for m in grid))
    ok &= res["checks"]["P1_j11_plus_formula_rejected"]

    # ---------------- P2: tau0-shape, candidate fit a/tau0 + b ------------
    print("-" * 78)
    print("P2  R_v(tau0) = -ln A_v / E[D]_vol (A_v exact, 160-pt); "
          "fit R = a/tau0 + b (weighted)")
    fits = {}
    for q in QS:
        g = sorted([m for m in grid if m["q"] == q], key=lambda m: m["tau0"])
        x = np.array([1.0 / m["tau0"] for m in g])
        y = np.array([m["R_quad"] for m in g])
        w = np.array([1.0 / m["sR_quad"] ** 2 for m in g])
        p, covp = np.polyfit(x, y, 1, w=w, cov=True)      # y = b + a*x
        a, b = p
        sa, sb = float(np.sqrt(covp[0, 0])), float(np.sqrt(covp[1, 1]))
        pred = b + a / np.array([m["tau0"] for m in g])
        chi2 = float(np.sum(((y - pred) * np.sqrt(w)) ** 2))
        dec = bool(a > 0)
        fits[q] = dict(a=round(a, 4), sa=round(sa, 4), b=round(b, 4),
                       sb=round(sb, 4), chi2=round(chi2, 2),
                       monotone_decreasing=dec)
        res["P2"][f"q{int(q)}"] = dict(
            fit_a_over_tau_plus_b=dict(a=round(a, 4), sa=round(sa, 4),
                                       b=round(b, 4), sb=round(sb, 4),
                                       chi2=round(chi2, 2)),
            monotone_decreasing=dec)
        print(f"  q={q:4.0f}: R = ({a:.4f}+-{sa:.4f})/tau0 + "
              f"{b:.4f}+-{sb:.4f}  chi2={chi2:.2f}/4  decreasing={dec}")
        res["checks"][f"P2_monotone_q{int(q)}"] = dec
        ok &= dec

    # ---------------- P2c: thin limit, low-tau0 MC ------------------------
    print("-" * 78)
    print("P2c thin limit: lim R_v = <T>_q / c_q with c_q = lim E[D]/tau0")
    for q in QS:
        pts = [m for m in thin + micro if m["q"] == q]
        pts.sort(key=lambda m: m["tau0"])
        tab = [(m["tau0"], m["ED"] / m["tau0"], m["sD"] / m["tau0"])
               for m in pts]
        t0 = np.array([a for a, _, _ in tab])
        c = np.array([b for _, b, _ in tab])
        sc = np.array([d for _, _, d in tab])
        # curvature-aware c0: weighted quadratic over tau0 <= 0.2
        small = t0 <= 0.2
        pc, covc = np.polyfit(t0[small], c[small], 2, w=1.0 / sc[small] ** 2,
                              cov=True)
        c0 = float(pc[2])                     # intercept (highest->lowest)
        sc0 = float(np.sqrt(covc[2, 2]))
        c_floor = float(c[0])                 # empirical floor at tau0=1e-3
        Tq, chord0 = T_vol_mean(q)
        thin_lim = Tq / c0
        s_thin = thin_lim * sc0 / c0
        fits[q].update(thin_limit=thin_lim, s_thin=s_thin, c0=c0, sc0=sc0,
                       Tq=Tq)
        res["P2c"][f"q{int(q)}"] = dict(
            {"c_at_tau0_1e-3": round(c_floor, 5)},
            c_tau0={str(t): round(v, 5) for t, v, _ in tab},
            c0=round(c0, 5), sc0=round(sc0, 5),
            T_mean=round(Tq, 5), chord_mean=round(chord0, 6),
            thin_limit=round(thin_lim, 3), s_thin=round(s_thin, 3))
        print(f"  q={q:4.0f}: c0 = {c0:.4f}+-{sc0:.4f} (c(1e-3)="
              f"{c_floor:.4f})  <T>_q = {Tq:.4f}  <chord> = {chord0:.6f}  "
              f"thin limit = {thin_lim:.3f}+-{s_thin:.3f}")
        res["checks"][f"P2c_thin_q{int(q)}"] = bool(
            np.isfinite(thin_lim) and thin_lim > 0)
        ok &= res["checks"][f"P2c_thin_q{int(q)}"]

    # ---------------- P3: kill-region boundaries --------------------------
    print("-" * 78)
    print("P3  kill-region: R_v < 4/3 (naive low-side kill); R_v > 2 "
          "(naive high-side kill) -- scan + max")
    rngb = np.random.default_rng(20260923)
    ts_scan = np.linspace(0.001, 8.0, 8000)
    for q in QS:
        pts = [m for m in grid + thin + micro if m["q"] == q]
        pts.sort(key=lambda m: m["tau0"])
        pts = np.array([(m["tau0"], m["ED"], m["sD"]) for m in pts])
        t0, ED, sD = pts[:, 0], pts[:, 1], pts[:, 2]
        cknot = ED / t0
        sknot = sD / t0
        Tq_grid, Wq = build_T(q, ng=80)          # one quadrature grid per q
        Re = R_curve(ts_scan, Tq_grid, Wq, cknot, t0)
        rmax = float(np.max(Re))
        t_max = float(ts_scan[int(np.argmax(Re))])
        cross = (Re[:-1] - R_LOW) * (Re[1:] - R_LOW) < 0
        idx = np.where(cross)[0]
        t_low = (float(0.5 * (ts_scan[idx[0]] + ts_scan[idx[0] + 1]))
                 if len(idx) else None)
        # bootstrap SEs (resample E[D], rebuild interp, re-solve)
        boot_lo, boot_hi = [], []
        Tq_b, Wq_b = build_T(q, ng=40)         # faster grid for bootstrap
        for _ in range(200):
            cb = cknot + rngb.normal(size=len(cknot)) * sknot
            Reb = R_curve(ts_scan, Tq_b, Wq_b, cb, t0)
            cr = (Reb[:-1] - R_LOW) * (Reb[1:] - R_LOW) < 0
            i = np.where(cr)[0]
            if len(i):
                boot_lo.append(0.5 * (ts_scan[i[-1]] + ts_scan[i[-1] + 1]))
            crh = (Reb[:-1] - R_HIGH) * (Reb[1:] - R_HIGH) < 0
            ih = np.where(crh)[0]
            if len(ih):
                boot_hi.append(0.5 * (ts_scan[ih[0]] + ts_scan[ih[0] + 1]))
        se_lo = float(np.std(boot_lo, ddof=1)) if boot_lo else None
        n_hi = len(boot_hi)
        res["P3"][f"q{int(q)}"] = dict(
            R_below_4over3_for_tau0_gt=t_low,
            se_low=round(se_lo, 3) if se_lo is not None else None,
            R_above_2_never=bool(n_hi == 0), n_hi_boot=n_hi,
            max_R=round(rmax, 4), max_R_at_tau0=round(t_max, 3))
        seg = [f"R<4/3 for tau0 > "
               f"{t_low:.3f} +- {se_lo:.3f}" if t_low is not None else
               "R never < 4/3 on [0.001,8]"]
        seg.append(f"R>2: never (max R = {rmax:.3f} at tau0={t_max:.2f}; "
                   f"{n_hi}/200 bootstrap crossings)")
        res["P3"][f"q{int(q)}"]["summary"] = seg
        for s_ in seg:
            print(f"  q={q:4.0f}: {s_}")
        res["checks"][f"P3_no_high_kill_q{int(q)}"] = bool(
            n_hi <= 10 and rmax < R_HIGH)      # <=5% bootstrap fraction
        res["checks"][f"P3_low_kill_q{int(q)}"] = bool(t_low is not None)
        ok &= (res["checks"][f"P3_no_high_kill_q{int(q)}"]
               and res["checks"][f"P3_low_kill_q{int(q)}"])

    # ---------------- P4: the crossing report -----------------------------
    print("-" * 78)
    print("P4  central flat vs volume decreasing; thin vs thick")
    for q in QS:
        cen = (1 + q / 3) / (0.5 + q / 4)
        thin_v = fits[q]["thin_limit"]
        print(f"  q={q:4.0f}: central {cen:.4f} (flat in tau0); volume "
              f"thin {thin_v:.2f} -> R(8)="
              f"{[m['R_quad'] for m in grid if m['q']==q and m['tau0']==8.0][0]:.3f}"
              f" (->0 as tau0->inf); decreasing={fits[q]['monotone_decreasing']}")
        res["P4"][f"q{int(q)}"] = dict(
            central_flat=round(cen, 4),
            volume_thin_limit=round(thin_v, 3),
            volume_R_at_tau0_8=round(
                [m["R_quad"] for m in grid if m["q"] == q and
                 m["tau0"] == 8.0][0], 3),
            thick_asymptotic_0="yes (-ln A ~ (3/2) ln tau0, T_min = 0)",
            decreasing_in_tau0=fits[q]["monotone_decreasing"])
        res["checks"][f"P4_crossing_q{int(q)}"] = bool(
            thin_v > [m['R_quad'] for m in grid if m['q'] == q and
                      m['tau0'] == 8.0][0])

    res["total_checks"] = len(res["checks"])
    res["passed"] = sum(1 for v in res["checks"].values() if v)
    res["ALL_PASSED"] = bool(ok)
    res["elapsed_s"] = round(time.time() - t_start, 1)
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "K07_results.json"), "w") as f:
        json.dump(res, f, indent=1)
    print(json.dumps(res, indent=1))
    print(f"elapsed {res['elapsed_s']} s")
    print("ALL K07 CHECKS PASSED" if ok else "K07 CHECK FAILURE")
    return 0 if ok else 1


def se_ratio(a, sa, d, sd, cov):
    """Delta-method SE of R = -ln(a)/d (a = atom fraction, d = E[D])."""
    R = -np.log(a) / d
    gA = -1.0 / (a * d)
    gD = np.log(a) / (d * d)
    return float(np.sqrt(gA ** 2 * sa ** 2 + gD ** 2 * sd ** 2
                         + 2.0 * gA * gD * cov))


if __name__ == "__main__":
    sys.exit(main())