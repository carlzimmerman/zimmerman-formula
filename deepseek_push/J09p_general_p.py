#!/usr/bin/env python3
"""
J09p -- K01 F3 FIX: the atom-delay ratio for the GENERAL profile family
kappa(r) = tau0 (1 + q r^p).  K01 derived analytically:
    -ln(A) / E[D]  =  (1 + q/(p+1)) / (1/2 + q/(p+2))   ->  (p+2)/(p+1) as q->inf
For p=2 this reduces to the J09 window (1+q/3)/(1/2+q/4) in [4/3, 2].
The p=2 window is NOT universal across shapes: p=4 gives limit 6/5 < 4/3.
This probe verifies the generalized law numerically for p in {1, 2, 4} and
restores the honest scope (K01 F3: "ANY central-source geometry" was
overstated; the window is per-shape).

Standalone sampler (independent of J02's quadratic rate_integral):
same process -- unit sphere, Poisson thinning with optical-depth CDF
inversion per segment, azimuth-averaged Thomson kernel, Gaussian kicks.
2026-09-23.
"""
import json
import sys
import numpy as np

BIG = 1.0e14


def rate_integral_p(a, b, ds, tau0, q, p):
    """EXACT integral of tau0*(1 + q r^p) dr over the segment
    r2(s) = a + b s + s^2, s in [0, ds], for p in {1, 2, 4}.
      p=2: r^2 = a + bs + s^2            (polynomial)
      p=4: r^4 = (a + bs + s^2)^2        (polynomial)
      p=1: r = sqrt(a + bs + s^2)        (closed-form sqrt-quadratic)
    """
    def F1(s):
        # int sqrt(s^2 + b s + a) ds, robust in all regimes.
        # (i) origin-start: r = s  ->  s^2/2            (a = b = 0)
        # (ii) radial-aligned: r = |s + b/2|  ->  (s+b/2)|s+b/2|/2
        # (iii) generic: classic asinh antiderivative (finite D4 > 0)
        if a < 1.0e-14 and abs(b) < 1.0e-14:
            return 0.5 * s * s
        D4 = 4.0 * a - b * b
        if D4 < 1.0e-12:
            # r(s) = |s + b/2| up to O(s^3) corrections; exact for the
            # degenerate parabola (segment through the turning point)
            t = s + b / 2.0
            return 0.5 * t * abs(t)
        v = s * s + b * s + a
        return ((s + b / 2.0) * np.sqrt(v) / 2.0
                + D4 / 8.0 * np.arcsinh((2.0 * s + b) / np.sqrt(D4)))

    def F2(s):
        return a * s + b * s * s / 2.0 + s ** 3 / 3.0

    def F4(s):
        aa, bb, cc = a, b, 1.0
        return (aa * aa * s + aa * bb * s * s
                + (bb * bb + 2.0 * aa) * s ** 3 / 3.0
                + bb * s ** 4 / 2.0 + s ** 5 / 5.0)

    if p == 1:
        I = F1(ds) - F1(0.0)
    elif p == 2:
        I = F2(ds) - F2(0.0)
    elif p == 4:
        I = F4(ds) - F4(0.0)
    else:
        raise ValueError("analytic p in {1,2,4} only")
    return tau0 * (ds + q * I)


def sample_one(rng, tau0, q, p):
    """One photon, central source, unit sphere, optical-depth CDF inversion.
    Returns (D, v, ang, N)."""
    x = np.array([0.0, 0.0, 0.0])
    u = np.array([0.0, 0.0, 1.0])
    v = 0.0
    ang = 0.0
    n = 0
    T = 1.0  # thermal scale, c = 1
    t = 0.0
    while True:
        # distance to wall
        # x + s u: |x + s u|^2 = 1  ->  s^2 + 2 (x.u) s + |x|^2 - 1 = 0
        a_seg = float(np.dot(x, x))
        b = 2.0 * float(np.dot(x, u))
        c2 = a_seg - 1.0
        disc = b * b - 4.0 * c2
        wall = (-b + np.sqrt(disc)) / 2.0
        # total optical depth to wall along this segment
        tau_wall = rate_integral_p(a_seg, b, wall, tau0, q, p)
        # sample collision: tau_exp ~ Exp(1)
        tau_exp = rng.exponential(1.0)
        if tau_exp >= tau_wall:
            # exits
            s_exit = wall
            D = t + s_exit - float(np.dot(x + s_exit * u, u))
            return D, v, ang, n
        # find collision s where tau(s) = tau_exp  (bisection on cumulative)
        lo, hi = 0.0, wall
        for _ in range(40):
            mid = 0.5 * (lo + hi)
            if rate_integral_p(a_seg, b, mid, tau0, q, p) < tau_exp:
                lo = mid
            else:
                hi = mid
        s = 0.5 * (lo + hi)
        x = x + s * u
        t += s
        # scatter: azimuth-averaged Thomson kernel, direct inverse-CDF
        mu = 1.0 - 2.0 * rng.random()
        # (kernel is symmetric in mu; sample mu then randomize sign is wrong
        #  for the full kernel -- use acceptance instead: p(mu) = 3/8 (1+mu^2))
        while True:
            mu = 2.0 * rng.random() - 1.0
            if rng.random() < 0.75 * (1.0 + mu * mu):
                break
        phi = 2.0 * np.pi * rng.random()
        sp = np.sqrt(max(0.0, 1.0 - mu * mu))
        up = np.array([sp * np.cos(phi), sp * np.sin(phi), mu])
        # kick
        e = rng.standard_normal()
        dz = up - u
        v += e * np.sqrt(T) * np.sqrt(float(np.dot(dz, dz)))
        ang += T * (1.0 - mu)
        u = up
        n += 1


def main():
    rng = np.random.default_rng(20260923)
    print("=" * 74)
    print("J09p -- GENERAL-p ATOM-DELAY RATIO (K01 F3 fix)")
    print("  -ln(A)/E[D] = (1+q/(p+1))/(1/2+q/(p+2))  ->  (p+2)/(p+1)")
    print("=" * 74)
    res = {"checks": {}, "measurements": {}}
    ok = True
    n = 400000
    for p, q in ((1, 0.0), (1, 5.0), (2, 0.0), (2, 5.0), (4, 0.0), (4, 5.0), (4, 20.0)):
        tau0 = 1.0
        Ds, Ns = [], []
        for i in range(n):
            D, v, ang, N = sample_one(rng, tau0, q, p)
            Ds.append(D)
            Ns.append(N)
        D = np.array(Ds)
        A = float(np.mean(np.array(Ns) == 0))
        dbar = float(np.mean(D))
        predA = np.exp(-tau0 * (1.0 + q / (p + 1.0)))
        exact_int_rk = tau0 * (0.5 + q / (p + 2.0))
        ratio = -np.log(A) / dbar
        exact = (1.0 + q / (p + 1.0)) / (0.5 + q / (p + 2.0))
        tag = f"p{p}_q{int(q)}"
        m = dict(A=A, dbar=dbar, pred_A=predA, int_rk=exact_int_rk,
                 ratio=ratio, exact_ratio=exact, limit=(p + 2.0) / (p + 1.0))
        res["measurements"][tag] = m
        res["checks"][f"atom_{tag}"] = bool(abs(A - predA) < 0.003)
        res["checks"][f"dbar_{tag}"] = bool(abs(dbar - exact_int_rk) < 0.01)
        res["checks"][f"ratio_{tag}"] = bool(abs(ratio - exact) < 0.05)
        ok &= res["checks"][f"atom_{tag}"] and res["checks"][f"dbar_{tag}"] \
            and res["checks"][f"ratio_{tag}"]
        print(f"  {tag:8s} A={A:.5f} (pred {predA:.5f})  E[D]={dbar:.4f} "
              f"(int r kappa {exact_int_rk:.4f})  ratio={ratio:.4f} "
              f"(exact {exact:.4f}, lim {(p+2)/(p+1):.4f})")
    res["total_checks"] = len(res["checks"])
    res["passed"] = sum(1 for v in res["checks"].values() if v)
    res["ALL_PASSED"] = bool(ok)
    print(json.dumps(res, indent=1))
    print("ALL J09P CHECKS PASSED" if ok else "J09P CHECK FAILURE")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())