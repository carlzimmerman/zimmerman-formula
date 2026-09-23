#!/usr/bin/env python3
"""
K02 -- THIRD-MOTOR verification engine for the JWST moment-channel headliners.
================================================================================
Unit sphere, c = k_B T0/m_e = 1, isothermal T = 1 (h = 0), opacity
    kappa(r) = tau0 (1 + q r^2)
per unit path length.  Photons are followed continuously (no diffusion
approximation), all escape, no absorption.

ALGORITHMIC INDEPENDENCE from the two existing engines
    engine 1: deepseek_push/J02_moment_hierarchy.py   (exact optical depth,
              FIXED 60-ROUND full-bisection root from [0, wall]; angle by
              acceptance-rejection on mu ~ U(-1,1); direction = normalised 3D
              normal; Gram-Schmidt transverse basis)
    engine 2: real_research/reviews/bhstar_scattering_clock_2026_09_21/
              transport.py   (NULL-COLLISION thinning: exponential proposal
              flights at kappa_max = tau0(1+q), keep with prob kappa/kappa_max;
              same rejection angle sampler)
THIS ENGINE (3) shares NO code path with either:
    * flight sampling: exact optical-depth CDF inversion,
          P(ell > s) = exp(-tau(s)),  tau(s) = tau0 [s + q (r2 s + pd s^2 +
          s^3/3)]  ->  solve tau(s) = w := -ln U  by HYBRID NEWTON-BISECTION
          (analytic dtau/ds; Newton step kept inside the analytic bracket
          [w/(tau0(1+q)), min(w/tau0, wall)], bisection fallback on
          overshoot) -- not fixed-iteration bisection, not thinning.
    * scattering angle: CLOSED-FORM INVERSE-CDF of the azimuth-averaged
          Thomson kernel P(mu) = (3/8)(1+mu^2):
              mu^3 + 3 mu = 8U - 4  =>  Cardano radicals, single formula.
          No rejection, no loop.
    * directions: spherical-angle sampling cos theta = 2U - 1, phi = 2 pi U,
          not normalised normals.
    * transverse frame: deterministic cross products (u x z, fallback u x x)
          + explicit azimuth phi; engine 1/2 draw a random-normal transverse
          vector and Gram-Schmidt.
    * RNG: dedicated seed stream (K02_* seeds) unrelated to engines 1/2.
    * delay arithmetic: D accumulated per photon as  tau - sum_j ell_j (u_j .
          u_final)  on a separate accumulator array AND cross-checked against
          the direct (x_final - x0) . u_final form of engines 1/2.

PHYSICS (faithfully identical to engines 1/2, which is the point):
    per collision:  mu ~ Thomson kernel;  u' = mu u + sqrt(1-mu^2)
                    (cos phi t1 + sin phi t2);
                    kick k ~ N(0, T=1)^3,   v += k . (u' - u);
                    ang += T (1 - mu) = (1 - mu);  N += 1
    escape:        tau(wall) <= w
    delay:         D = tau - (x_final - x0) . u_final   (>= 0 per photon)
    volume face:   Q = (x_final - x0) . u_final,  D = tau - Q per photon.

LAWS UNDER TEST (frozen results to reproduce independently):
    Thm 1   E[D]_central = int_0^1 r kappa dr = tau0 (1/2 + q/4)   [EXACT]
    J01     E[D v^2] = 2 E[D ang]  (per-photon conditional Gaussian kicks)
    atom    A = P(N=0)_central = exp(-tau0 (1 + q/3))              [EXACT]
    window  4/3 <= -ln A / E[D] <= 2  with q-dependence (1+q/3)/(1/2+q/4)
    J02B    E[D]_vol = E[tau] - E[Q],  Q = (x-x0).u_final,  E[Q] ~ 0.597
            at tau0=1, q=0 (volume source differs from central).

Deliverables beside this file: K02_engine3.out (stdout), K02_results.json,
K02_ENGINE3_VERDICT.md.  python3 + numpy only.  No git commit.
"""
import json
import math
import sys

import numpy as np


# ---------------------------------------------------------------------------
# closed-form inverse CDF of the azimuth-averaged Thomson kernel
# ---------------------------------------------------------------------------
def thomson_mu_invCDF(U):
    """mu with density (3/8)(1+mu^2) on [-1,1], from uniform U in (0,1).

    F(mu) = (3/8)(mu + mu^3/3 + 4/3)  =>  mu^3 + 3 mu = 8U - 4 =: c.
    Cardano (p = 3):  mu = cbrt(c/2 + s) + cbrt(c/2 - s),  s = sqrt(c^2/4 + 1).
    """
    c = 8.0 * U - 4.0
    s = np.sqrt(0.25 * c * c + 1.0)
    return np.cbrt(0.5 * c + s) + np.cbrt(0.5 * c - s)


# ---------------------------------------------------------------------------
# hybrid Newton-bisection root of the exact segment optical depth
# ---------------------------------------------------------------------------
def flight_root(r2, pd, wall, w, tau0, q):
    """Root s* in [0, wall] of  tau(s) = tau0 [s + q (r2 s + pd s^2 + s^3/3)]
    = w, by Newton safeguarded inside the analytic bracket
        [w/(tau0(1+q)), min(w/tau0, wall)].
    Invariant:  tau(lo) <= w <= tau(hi);  tau strictly increasing on the
    segment (dtau/ds = tau0 [1 + q (r2 + 2 pd s + 3 s^2)] >= tau0 > 0)."""
    lo = w / (tau0 * (1.0 + q))
    hi = np.minimum(w / tau0, wall)
    s = 0.5 * (lo + hi)
    for _ in range(60):
        s2 = s * s
        tau = tau0 * (s + q * (r2 * s + pd * s2 + s2 * s / 3.0))
        dtau = tau0 * (1.0 + q * (r2 + 2.0 * pd * s + 3.0 * s2))
        cand = s - (tau - w) / dtau
        bad = ~np.isfinite(cand) | (cand <= lo) | (cand >= hi)
        cand = np.where(bad, 0.5 * (lo + hi), cand)
        c2 = cand * cand
        left = tau0 * (cand + q * (r2 * cand + pd * c2 + c2 * cand / 3.0)) <= w
        lo = np.where(left, cand, lo)
        hi = np.where(left, hi, cand)
        s = 0.5 * (lo + hi)
        if np.all((hi - lo) <= 4.0 * np.finfo(float).eps *
                  np.maximum(1.0, np.abs(hi))):
            break
    return 0.5 * (lo + hi)


# ---------------------------------------------------------------------------
# the transport engine
# ---------------------------------------------------------------------------
def simulate(n, tau0, q, source, seed):
    """Engine 3.  source in {'central','volume'}; volume = uniform in ball.
    Returns per-photon arrays: D, v2, ang, N, elapsed, plus bookkeeping
    cross-check arrays Sx, Sq and (volume) mu_exit."""
    rng = np.random.default_rng(seed)

    # ---- initial positions ----------------------------------------------
    if source == "volume":
        ct = 2.0 * rng.random(n) - 1.0
        st = np.sqrt(np.maximum(0.0, 1.0 - ct * ct))
        ph = 2.0 * np.pi * rng.random(n)
        rad = rng.random(n) ** (1.0 / 3.0)
        pos = np.stack([rad * st * np.cos(ph), rad * st * np.sin(ph),
                        rad * ct], axis=1)
    else:
        pos = np.zeros((n, 3))
    origin = pos.copy()

    # ---- initial directions (spherical angles) ---------------------------
    ct = 2.0 * rng.random(n) - 1.0
    st = np.sqrt(np.maximum(0.0, 1.0 - ct * ct))
    ph = 2.0 * np.pi * rng.random(n)
    u = np.stack([st * np.cos(ph), st * np.sin(ph), ct], axis=1)

    elapsed = np.zeros(n)
    ang = np.zeros(n)
    N = np.zeros(n, dtype=np.int64)
    v = np.zeros(n)                # scalar speed shift: sum_j k_j . (u'-u)
    Sx = np.zeros((n, 3))          # sum_j ell_j u_j  (delay arithmetic path)
    mu_exit = np.zeros(n)          # (x_hat . u) at escape; volume face
    alive = np.ones(n, dtype=bool)
    steps = 0

    while alive.any():
        steps += 1
        if steps > 60000:
            raise RuntimeError("transport cap; survivors would be dropped")
        idx = np.flatnonzero(alive)
        p = pos[idx]
        uu = u[idx]
        r2 = np.sum(p * p, axis=1)
        pd = np.sum(p * uu, axis=1)
        wall = -pd + np.sqrt(np.maximum(pd * pd - r2 + 1.0, 0.0))
        w = -np.log(rng.random(len(idx)))
        tau_w = tau0 * (wall + q * (r2 * wall + pd * wall * wall +
                                    wall * wall * wall / 3.0))
        esc = tau_w <= w
        s = wall.copy()
        inner = ~esc
        if inner.any():
            s[inner] = flight_root(r2[inner], pd[inner], wall[inner],
                                   w[inner], tau0, q)

        elapsed[idx] += s
        Sx[idx] += uu * s[:, None]
        pos[idx] += uu * s[:, None]

        # escape readout (final segment direction u_j = u_final here)
        if esc.any():
            xe = pos[idx[esc]]
            ne = np.linalg.norm(xe, axis=1)
            ue = uu[esc]
            mu_exit[idx[esc]] = np.sum(xe * ue, axis=1) / ne
        alive[idx[esc]] = False

        # colliders: scatter
        col = idx[~esc]
        if len(col):
            uc = uu[~esc]
            mu = thomson_mu_invCDF(rng.random(len(col)))
            # deterministic transverse basis: t1 = u x z (fallback u x x)
            zvec = np.zeros((len(col), 3)); zvec[:, 2] = 1.0
            t1a = np.cross(uc, zvec)
            xvec = np.zeros((len(col), 3)); xvec[:, 0] = 1.0
            t1b = np.cross(uc, xvec)
            near_pole = np.abs(uc[:, 2]) > 0.99
            t1 = np.where(near_pole[:, None], t1b, t1a)
            t1n = np.linalg.norm(t1, axis=1)
            t1 = t1 / t1n[:, None]
            t2 = np.cross(uc, t1)                     # unit, orthogonal
            phi = 2.0 * np.pi * rng.random(len(col))
            newu = (uc * mu[:, None]
                    + np.sqrt(np.maximum(0.0, 1.0 - mu * mu))[:, None]
                    * (np.cos(phi)[:, None] * t1 + np.sin(phi)[:, None] * t2))
            du = newu - uc
            kick = rng.normal(size=(len(col), 3))     # T = 1
            v[col] += np.sum(kick * du, axis=1)
            ang[col] += (1.0 - mu)
            N[col] += 1
            u[idx[~esc]] = newu

    # ---- per-photon outputs ----------------------------------------------
    Sf = np.sum(Sx * u, axis=1)          # Q = (x_final - x0) . u_final
    D = elapsed - Sf
    D_direct = elapsed - np.sum((pos - origin) * u, axis=1)
    book_err = float(np.max(np.abs(D - D_direct)))
    v2 = v * v
    return dict(D=D, v2=v2, ang=ang, N=N, elapsed=elapsed, Q=Sf,
                mu_exit=mu_exit, book_err=book_err, steps=steps)


def se(x):
    return float(np.std(x, ddof=1) / np.sqrt(len(x)))


# ---------------------------------------------------------------------------
def main():
    args = sys.argv[1:]
    n_main = int(args[0]) if args else 1_000_000
    n_head = 2 * n_main

    res = {"lane": "K02_engine3",
           "title": "THIRD-MOTOR re-verification of the JWST moment-channel "
                    "headline numbers (Newton CDF-inversion engine)",
           "checks": {}, "measurements": {}, "headlines": {}}
    discrepancies = []
    ok = True

    def check(name, cond, note=""):
        res["checks"][name] = bool(cond)
        nonlocal ok
        ok &= bool(cond)
        if not cond:
            discrepancies.append(f"{name}: {note}")
        res.setdefault("notes", {})[name] = note

    # ============ SELF-TESTS of the new samplers ==========================
    rng = np.random.default_rng(20260999)
    U = rng.random(2_000_000) + 1e-300
    mu = thomson_mu_invCDF(U)
    emu, s2, e1m = np.mean(mu), np.mean(mu * mu), np.mean(1.0 - mu)
    z = [emu / se(mu), (s2 - 0.4) / se(mu * mu), (e1m - 1.0) / se(1.0 - mu)]
    res["measurements"]["T1_kernel"] = dict(E_mu=emu, E_mu2=s2, E_1m=e1m,
                                            z=z)
    check("T1_kernel_moments", max(abs(t) for t in z) < 3.0,
          f"Thomson inverse-CDF moments z={z} (targets 0, 0.4, 1)")
    # q=0 flight root is closed-form: s* = w/tau0; Newton must land exactly.
    R = np.random.default_rng(20260998)
    r2t = R.random(500000); pdt = R.uniform(-1, 1, 500000); wt = R.random(500000)
    wallt = -pdt + np.sqrt(pdt * pdt - r2t + 1.0)
    wc = wt * np.minimum(1.0, wallt)
    st = flight_root(r2t, pdt, wallt, wc, 1.0, 0.0)
    err = float(np.max(np.abs(st - wc)))
    res["measurements"]["T2_solver"] = dict(max_abs_err_q0=err)
    check("T2_solver_exact_at_q0", err < 1e-12,
          f"q=0 flight root must be w/tau0 exactly; max |err|={err}")

    # ============ THE THREE CLOUDS, CENTRAL SOURCE =========================
    A_exact = {}
    E_D_exact = {}
    clouds = {}
    for q in (0.0, 3.0, 10.0):
        n = n_head if q == 0.0 else n_main
        t0 = 1.0
        r = simulate(n, t0, q, "central", seed=20260200 + int(3 * q))
        D, v2, ang, Nn = r["D"], r["v2"], r["ang"], r["N"]
        A = float(np.mean(Nn == 0))
        E_D = float(np.mean(D))
        EDv2 = float(np.mean(D * v2))
        E_Dang = float(np.mean(D * ang))
        Y = D * v2 - 2.0 * D * ang          # per-photon paired difference
        A_exact[q] = math.exp(-t0 * (1.0 + q / 3.0))
        E_D_exact[q] = t0 * (0.5 + q / 4.0)
        c = dict(n=n, seed=20260200 + int(3 * q),
                 E_D=E_D, sD=se(D),
                 E_v2=float(np.mean(v2)), s_v2=se(v2),
                 E_ang=float(np.mean(ang)), s_ang=se(ang),
                 E_N=float(np.mean(Nn)),
                 E_Dv2=EDv2, sDv2=se(D * v2),
                 E_Dang=E_Dang, sDang=se(D * ang),
                 z_mixed=float(np.mean(Y)) / se(Y),
                 atom=A, sA=math.sqrt(A * (1.0 - A) / n),
                 E_tau=float(np.mean(r["elapsed"])),
                 book_err=r["book_err"], steps=r["steps"])
        clouds[q] = c
        res["measurements"][f"C_central_q{q}"] = c

        check(f"K1_ED_q{q}",
              abs(E_D - E_D_exact[q]) < 3.0 * se(D) + 1e-12,
              f"E[D]={E_D:.6f} vs exact {E_D_exact[q]} (z="
              f"{(E_D - E_D_exact[q]) / se(D):.2f})")
        check(f"K2_mixed_q{q}",
              abs(c["z_mixed"]) < 3.0,
              f"per-photon D(v^2-2ang) z={c['z_mixed']:.2f}")
        check(f"K3_atom_q{q}",
              abs(A - A_exact[q]) < 3.0 * c["sA"] + 1e-12,
              f"A={A:.6f} vs exp(-(1+q/3))={A_exact[q]:.6f} (z="
              f"{(A - A_exact[q]) / c['sA']:.2f})")

    # ratio window  -ln A / E[D]  in [4/3, 2], q-dependence (1+q/3)/(1/2+q/4)
    for q in (0.0, 3.0, 10.0):
        c = clouds[q]
        B = -math.log(c["atom"])
        sB = c["sA"] / c["atom"]
        rq = B / c["E_D"]
        srq = rq * math.sqrt((sB / B) ** 2 + (c["sD"] / c["E_D"]) ** 2)
        target = (1.0 + q / 3.0) / (0.5 + q / 4.0)
        # window is CLOSED and contains the exact target (2.0 sits ON it at
        # q=0): test the point estimate against the window straddled by 3 se.
        inwin = (rq >= 4.0 / 3.0 - 3.0 * srq) and (rq <= 2.0 + 3.0 * srq)
        zmatch = (rq - target) / srq
        res["measurements"][f"K4_ratio_q{q}"] = dict(
            B=B, sB=sB, ratio=rq, s_ratio=srq, target=target, z=zmatch,
            in_window=bool(inwin))
        check(f"K4a_window_q{q}", inwin,
              f"-ln A/E[D]={rq:.4f}+-{3*srq:.4f} outside [4/3,2] at q={q}")
        check(f"K4b_dependence_q{q}", abs(zmatch) < 3.0,
              f"ratio z={zmatch:.2f} vs (1+q/3)/(1/2+q/4)={target:.5f}")

    # ============ HEADLINE REPRODUCTION vs engines 1/2 =====================
    c0 = clouds[0.0]
    c10 = clouds[10.0]
    rep = [
        ("E[D]@q0", c0["E_D"], c0["sD"], 0.5008),
        ("E[v^2]@q0", c0["E_v2"], c0["s_v2"], 2.8061),
        ("E[D v^2]@q0", c0["E_Dv2"], c0["sDv2"], 3.7316),
        ("atom@q0", c0["atom"], c0["sA"], 0.3679),
        ("E[D]@q10", c10["E_D"], c10["sD"], 3.003),
        ("atom@q10", c10["atom"], c10["sA"], 0.0131),
    ]
    for name, val, sv, cited in rep:
        dz = (val - cited) / sv
        res["headlines"][name] = dict(measured=val, se=sv, cited=cited,
                                      z=dz)
        check(f"H_{name}", abs(dz) < 3.0,
              f"{name}: {val:.4f}+-{sv:.4f} vs cited {cited} (z={dz:.2f})")

    # ============ VOLUME-SOURCE FACE (J02B) ================================
    nv = n_main
    rv = simulate(nv, 1.0, 0.0, "volume", seed=20260230)
    Dv, Q = rv["D"], rv["Q"]
    E_Dv, E_Q = float(np.mean(Dv)), float(np.mean(Q))
    E_tv = float(np.mean(rv["elapsed"]))
    sDv, sQ, stv = se(Dv), se(Q), se(rv["elapsed"])
    z_diff = (E_Dv - 0.5) / sDv
    z_id = (E_Dv - (E_tv - E_Q)) / math.hypot(sDv, math.hypot(sQ, stv))
    mu_e = float(np.mean(rv["mu_exit"]))
    dynkin_pred = 0.5 + mu_e - 0.3
    res["measurements"]["V_volume_q0"] = dict(
        E_D=E_Dv, sD=sDv, E_tau=E_tv, s_tau=stv, E_Q=E_Q, sQ=sQ,
        z_vs_central=z_diff, z_identity=z_id, book_err=rv["book_err"],
        E_mu_exit=mu_e, dynkin_pred_tau=dynkin_pred,
        z_dynkin=(E_tv - dynkin_pred) / stv)
    check("K5a_volume_differs", abs(z_diff) > 8.0,
          f"volume E[D]={E_Dv:.6f} vs central 0.5: z={z_diff:.1f}")
    check("K5b_D_tau_Q_identity", abs(z_id) < 3.0,
          f"E[D]={E_Dv:.6f} vs E[tau]-E[Q]={E_tv - E_Q:.6f} (z={z_id:.2f})")
    check("K5c_Q_bookkeeping", rv["book_err"] < 1e-9,
          f"Sx/pos-direct delay cross-check err={rv['book_err']:.3e}")
    check("K5d_Q_value",
          abs(E_Q - 0.5972) < 3.0 * math.hypot(sQ, 0.00064),
          f"E[Q]={E_Q:.6f}+-{sQ:.6f} vs J02B 0.5972")
    check("K5e_dynkin_tau_bonus",
          abs(E_tv - dynkin_pred) < 6.0 * math.hypot(stv, 0.00052),
          f"E[tau]_vol={E_tv:.6f} vs 1/2+E[mu_exit]-3/10={dynkin_pred:.6f}")

    # ======================================================================
    res["total_checks"] = len(res["checks"])
    res["passed"] = sum(1 for v in res["checks"].values() if v)
    res["ALL_PASSED"] = bool(ok)
    print(json.dumps(res, indent=1))
    print("ALL K02 ENGINE-3 CHECKS PASSED" if ok
          else "K02 ENGINE-3: CHECK FAILURES PRESENT")
    if discrepancies:
        print("DISCREPANCIES:")
        for d in discrepancies:
            print("  -", d)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())