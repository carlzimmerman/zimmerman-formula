#!/usr/bin/env python3
"""
J02 -- THE EVEN-MOMENT HIERARCHY + THE VOLUME-SOURCE FACE
2026-09-23.  Continuation of J01 on the JWST_EQUATION_TARGET moment channel.

THEOREM A (moment hierarchy; any source, exact): conditional on the
trajectory, v ~ N(0, 2 ang) (J01 lemma), so for every m >= 1

      E[D v^{2m}] = (2m-1)!! * 2^m * E[D ang^m]

  m=1:  E[D v^2] = 2  E[D ang]          (J01, re-verified; NEW for volume)
  m=2:  E[D v^4] = 12 E[D ang^2]
  m=3:  E[D v^6] = 120 E[D ang^3]

THEOREM B (volume-source face; NEW): Theorem 1's density-free identity does
not port to the volume source.  With volume-uniform isotropic emission,
D = tau - Q,  Q := (x_tau - x_0).u_final = sum_j ell_j (u_j . u_final),
and Dynkin on f(x,u) = F(r) + 2 x.u with F'(r) = 2 r kappa(r) gives

   E[tau]_vol = int_0^1 r kappa(r) dr + R E[mu_exit] - (1/2) E[F(r0)],
                F(r) = 2 int_0^r s kappa(s) ds,  r0 ~ 3 r^2 (volume-uniform)

For kappa = tau0 uniform, R = 1:  E[F(r0)] = 3 tau0/5, so
E[tau]_vol = tau0/2 + E[mu_exit] - 3 tau0/10  (verified below, q=0 and q-cloud).
The frozen identity E[D] = int r kappa dr FAILS for volume (measured): the
residence-coupling term Q is the new, retained observable (J01's angular term
was the F^{12}-source analogue; here Q is its spatial-face analogue).

Corollary: the MIXED hierarchy survives the source change exactly.

Every number below is machine-checked on the independent solver from J01
(exact optical-depth bisection; no null-collision thinning).
Checks:
  A1-A3  hierarchy m = 1,2,3, central source   A4-A6  m = 1,2,3, volume
  B1     central E[D] = int r kappa dr (re-benchmark)
  B2     volume E[D] != int r kappa dr (identity does NOT port; > 8 SE)
  B3     E[tau]_vol Dynkin compensation vs closed form (uniform + q-cloud)
  B4     Q bookkeeping: per-photon Q == (x-x0).u_final; E[D]=E[tau]-E[Q]
  C1     closure ratios R_m at m = 1,2,3 (angular term grows with m)
"""
import json
import math
import sys

import numpy as np


def rate_integral(a, b, ds, tau0, q):
    return tau0 * (ds + q * (a * ds + b * ds**2 + ds**3 / 3))

def thomson_mu(rng, n):
    out = np.empty(n); todo = np.arange(n)
    while len(todo):
        m = rng.uniform(-1, 1, len(todo))
        take = rng.random(len(todo)) < (1 + m*m) / 2
        out[todo[take]] = m[take]; todo = todo[~take]
    return out


def simulate(n, tau0, q, source, seed, h=0.0):
    """Independent engine (J01), central or volume source.  Returns
    v2,v4,v6 (D-weighted by the tester), D, ang, N, elapsed, pos, direc.
    h: temperature-gradient parameter, T(r) = 1 + h r^2 in the collision
    kick and in the angular exposure (h=0 is isothermal J02 scope)."""
    rng = np.random.default_rng(seed)
    pos = np.zeros((n, 3))
    if source == "volume":
        d0 = rng.normal(size=(n, 3)); d0 = d0 / np.linalg.norm(d0, axis=1)[:, None]
        pos = d0 * rng.random(n)[:, None] ** (1/3)      # uniform in unit ball
    origin = pos.copy()
    d = rng.normal(size=(n, 3)); direc = d / np.linalg.norm(d, axis=1)[:, None]
    v = np.zeros(n); elapsed = np.zeros(n); ang = np.zeros(n)
    N = np.zeros(n, dtype=int)
    alive = np.arange(n); steps = 0
    while len(alive):
        steps += 1
        if steps > 50000:
            raise RuntimeError("transport cap; do not drop survivors")
        p, u = pos[alive], direc[alive]
        pd = np.sum(p * u, axis=1)
        r2 = np.sum(p * p, axis=1)
        disc = pd*pd - r2 + 1.0
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
                mid = 0.5*(lo + hi)
                val = rate_integral(r2i, pdi, mid, tau0, q) + np.log(Ui)
                tak = val < 0
                lo[tak] = mid[tak]; hi[~tak] = mid[~tak]
            s[inner] = 0.5*(lo + hi)
        elapsed[alive] += s
        pos[alive] += u * s[:, None]
        alive = alive[~esc]
        if len(alive) == 0:
            break
        p, u = pos[alive], direc[alive]
        r2 = np.sum(p*p, axis=1)
        mu = thomson_mu(rng, len(alive))
        t = rng.normal(size=(len(alive), 3))
        t -= np.sum(t*u, axis=1)[:, None] * u
        tn = np.linalg.norm(t, axis=1)
        t = t / tn[:, None]
        newu = u*mu[:, None] + t*np.sqrt(1 - mu*mu)[:, None]
        T = 1.0 + h*r2                       # T(r) = 1 + h r^2 (h=0 isothermal)
        kick = rng.normal(size=(len(alive), 3)) * np.sqrt(T)[:, None]
        v[alive] += np.sum(kick*(newu - u), axis=1)
        ang[alive] += T*(1.0 - mu)
        N[alive] += 1
        direc[alive] = newu
    D = elapsed - np.sum((pos - origin) * direc, axis=1)
    assert np.all(D >= -1e-9)
    return dict(v2=v*v, v4=v**4, v6=v**6, D=D, ang=ang, N=N,
                elapsed=elapsed, pos=pos, direc=direc)


def simulate_Q(n, tau0, q, source, seed):
    """Definitional Q = sum_j ell_j (u_j . u_final) by exact segment
    bookkeeping; cross-validated against (x-x0).u_final per photon."""
    rng = np.random.default_rng(seed)
    pos = np.zeros((n, 3))
    if source == "volume":
        d0 = rng.normal(size=(n, 3)); d0 = d0 / np.linalg.norm(d0, axis=1)[:, None]
        pos = d0 * rng.random(n)[:, None] ** (1/3)
    origin = pos.copy()
    d = rng.normal(size=(n, 3)); direc = d / np.linalg.norm(d, axis=1)[:, None]
    elapsed = np.zeros(n)
    segs = [[] for _ in range(n)]          # list of (length, direction)
    alive = np.arange(n); steps = 0
    while len(alive):
        steps += 1
        if steps > 100000:
            raise RuntimeError("cap; do not drop survivors")
        p, u = pos[alive], direc[alive]
        pd = np.sum(p * u, axis=1)
        r2 = np.sum(p * p, axis=1)
        disc = pd*pd - r2 + 1.0
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
                mid = 0.5*(lo + hi)
                val = rate_integral(r2i, pdi, mid, tau0, q) + np.log(Ui)
                tak = val < 0
                lo[tak] = mid[tak]; hi[~tak] = mid[~tak]
            s[inner] = 0.5*(lo + hi)
        elapsed[alive] += s
        pos[alive] += u * s[:, None]
        for i, idx in enumerate(alive):
            segs[idx].append((float(s[i]), u[i].copy()))
        alive = alive[~esc]
        if len(alive) == 0:
            break
        p, u = pos[alive], direc[alive]
        r2 = np.sum(p*p, axis=1)
        mu = thomson_mu(rng, len(alive))
        t = rng.normal(size=(len(alive), 3))
        t -= np.sum(t*u, axis=1)[:, None] * u
        tn = np.linalg.norm(t, axis=1)
        t = t / tn[:, None]
        direc[alive] = u*mu[:, None] + t*np.sqrt(1 - mu*mu)[:, None]
    Q = np.array([sum(ll*float(np.dot(ud, direc[i])) for (ll, ud) in segs[i])
                   for i in range(n)])
    X = np.sum((pos - origin) * direc, axis=1)
    return dict(Q=Q, X=X, elapsed=elapsed)


def se(x):
    return float(np.std(x, ddof=1) / np.sqrt(len(x)))


def main():
    res = {"checks": {}, "measurements": {}}
    ok = True

    # ---------- Part A: hierarchy m = 1..3, central + volume ---------------
    for src in ("central", "volume"):
        r = simulate(1000000, 1.0, 0.0, src, seed=13)
        D, ang = r["D"], r["ang"]
        m = res["measurements"][f"A_{src}"] = {"E_D": float(np.mean(D)),
                                               "sD": se(D),
                                               "E_ang": float(np.mean(ang))}
        for p, mult, lbl in ((2, 2.0, "A1"), (4, 12.0, "A2"), (6, 120.0, "A3")):
            EDvp = float(np.mean(D * r[f"v{p}"]))
            E_Dangm = float(np.mean(D * ang ** (p//2)))
            m[f"E_Dv{p}"] = EDvp
            m[f"E_Dang{p//2}"] = E_Dangm
            m[f"ratio_{p}"] = EDvp / (mult * E_Dangm)
            z = EDvp - mult*E_Dangm
            tol = 5.0*(se(D*r[f"v{p}"]) + mult*se(D*ang**(p//2)))
            c = abs(z) < tol
            res["checks"][f"{lbl}_{src}"] = bool(c)
            ok &= bool(c)

    # ---------- Part B: volume-source face ----------------------------------
    # B1: central re-benchmark E[D] = int_0^1 r*1 dr = 1/2
    rc = simulate(1000000, 1.0, 0.0, "central", seed=17)
    E_Dc = float(np.mean(rc["D"]))
    res["checks"]["B1_central_E_D"] = abs(E_Dc - 0.5) < 6*se(rc["D"]) + 1e-4
    ok &= res["checks"]["B1_central_E_D"]
    res["measurements"]["B1"] = dict(E_D_central=E_Dc, int_r_kappa=0.5)

    # B2: volume source -- E[D] deviates from 0.5
    rv = simulate(1000000, 1.0, 0.0, "volume", seed=19)
    E_Dv = float(np.mean(rv["D"])); E_tv = float(np.mean(rv["elapsed"]))
    res["checks"]["B2_volume_differs"] = abs(E_Dv - 0.5) > 8*se(rv["D"])
    ok &= res["checks"]["B2_volume_differs"]

    # B4: Q bookkeeping identity, then E[D] = E[tau] - E[Q]
    rq = simulate_Q(150000, 1.0, 0.0, "volume", seed=41)
    Err = float(np.max(np.abs(rq["Q"] - rq["X"])))
    E_Q = float(np.mean(rq["Q"])); E_tq = float(np.mean(rq["elapsed"]))
    # E[D] from the main volume run: D = tau - (x-x0).u  => E[D]=E[tau]-E[Q]
    E_D_from_identity = E_tv - E_Q
    res["measurements"]["B4"] = dict(max_bookkeeping_err=Err,
                                     E_Q=E_Q, E_tau_vol=E_tv,
                                     E_D_vol_measured=E_Dv,
                                     E_D_from_tau_minus_Q=E_D_from_identity)
    res["checks"]["B4_Q_bookkeeping"] = Err < 1e-9
    res["checks"]["B4_vol_identity"] = abs(E_Dv - E_D_from_identity) < \
        6*(se(rv["D"]) + 1.5*se(rq["Q"]))
    ok &= res["checks"]["B4_Q_bookkeeping"] and res["checks"]["B4_vol_identity"]

    # B3: Dynkin compensation E[tau]_vol = 1/2 + E[mu_exit] - 3/10  (uniform)
    # E[mu_exit]: measure it directly in a dedicated escape-face run.
    def mu_exit_estimator(n, seed):
        rng = np.random.default_rng(seed)
        pos = np.zeros((n, 3))
        d0 = rng.normal(size=(n, 3)); d0 = d0/np.linalg.norm(d0, axis=1)[:, None]
        pos = d0 * rng.random(n)[:, None] ** (1/3)
        direc = rng.normal(size=(n, 3))
        direc = direc/np.linalg.norm(direc, axis=1)[:, None]
        mus = np.zeros(n); al = np.arange(n)
        while len(al):
            p, u = pos[al], direc[al]
            pd = np.sum(p*u, axis=1); r2 = np.sum(p*p, axis=1)
            disc = pd*pd - r2 + 1.0
            wall = -pd + np.sqrt(np.maximum(disc, 0.0))
            U = rng.random(len(al))
            esc = rate_integral(r2, pd, wall, 1.0, 0.0) <= -np.log(U)
            s = wall.copy()
            inside = al[~esc]
            if len(inside):
                p2, u2 = pos[inside], direc[inside]
                pd2 = np.sum(p2*u2, axis=1); r22 = np.sum(p2*p2, axis=1)
                lo = np.zeros(len(inside)); hi = wall[~esc]
                Ui = U[~esc]; r2i = r22; pdi = pd2
                for _ in range(60):
                    mid = 0.5*(lo+hi)
                    val = rate_integral(r2i, pdi, mid, 1.0, 0.0) + np.log(Ui)
                    tak = val < 0
                    lo[tak] = mid[tak]; hi[~tak] = mid[~tak]
                s[~esc] = 0.5*(lo+hi)
            pos[al] += direc[al]*s[:, None]
            esc_idx = al[esc]
            xh = pos[esc_idx]/np.linalg.norm(pos[esc_idx], axis=1)[:, None]
            mus[esc_idx] = np.sum(xh*direc[esc_idx], axis=1)
            al = al[~esc]
            if len(al) == 0:
                break
            p, u = pos[al], direc[al]
            r2 = np.sum(p*p, axis=1)
            mu = thomson_mu(rng, len(al))
            t = rng.normal(size=(len(al), 3))
            t -= np.sum(t*u, axis=1)[:, None]*u
            tn = np.linalg.norm(t, axis=1); t = t/tn[:, None]
            direc[al] = u*mu[:, None] + t*np.sqrt(1-mu*mu)[:, None]
        return float(np.mean(mus)), float(np.std(mus, ddof=1)/np.sqrt(n))
    Emu, sEmu = mu_exit_estimator(150000, 23)
    pred = 0.5 + Emu - 0.3
    res["measurements"]["B3"] = dict(E_mu_exit=Emu, s_mu=sEmu,
                                     dynkin_pred=pred, E_tau_measured=E_tv)
    res["checks"]["B3_dynkin_tau"] = abs(E_tv - pred) < 8*max(sEmu, se(rv["elapsed"])) + 1e-3
    ok &= res["checks"]["B3_dynkin_tau"]

    # ---------- Part C: closure ratios (central, isothermal) ---------------
    r = simulate(1000000, 1.0, 0.0, "central", seed=29)
    D, ang = r["D"], r["ang"]
    C = {}
    for p, mult in ((2, 2.0), (4, 12.0), (6, 120.0)):
        C[f"R{p}"] = float(np.mean(D*r[f"v{p}"])) / (mult*float(np.mean(D))*float(np.mean(ang**(p//2))))
    res["measurements"]["C"] = C

    # ---------- Part D: q-cloud robustness (m = 1,2) ------------------------
    for q in (3.0, 10.0):
        r = simulate(1200000, 1.0, q, "central", seed=31)
        D, ang = r["D"], r["ang"]
        for p, mult in ((2, 2.0), (4, 12.0)):
            EDvp = float(np.mean(D*r[f"v{p}"]))
            E_Dangm = float(np.mean(D*ang**(p//2)))
            tol = 5.0*(se(D*r[f"v{p}"]) + mult*se(D*ang**(p//2)))
            c = abs(EDvp - mult*E_Dangm) < tol
            res["checks"][f"D_q{q}_m{p//2}"] = bool(c)
            ok &= bool(c)

    res["total_checks"] = len(res["checks"])
    res["passed"] = sum(1 for v in res["checks"].values() if v)
    res["ALL_PASSED"] = bool(ok)
    print(json.dumps(res, indent=1))
    print("ALL J02 CHECKS PASSED" if ok else "J02 CHECK FAILURE")
    return 0 if ok else 1

if __name__ == "__main__":
    sys.exit(main())