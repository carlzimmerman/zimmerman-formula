#!/usr/bin/env python3
"""
M05 -- GEOMETRIC ANCHORS OF THE VOLUME WINDOW: exact first-flight moments.
Hypothesis from K07's thin limits (<T>_q = 0.75 / 2.0 / 4.9167 at q=0/3/10):
  <T>_q = E_{x uniform in ball, u isotropic}[ int_0^{chord} (1 + q r^2(s)) ds ]
        = <chord> + q * E[int r^2 ds] = 3/4 + q * (5/12)   (conjectured 5/12)
i.e. E[int_0^{chord} r^2(s) ds] = 5/12 EXACTLY, and <T>_q is LINEAR in q.
Consequence: the volume atom's thin limit -ln A_v ~ tau0 * <T>_q is a CLOSED
FORM per q, and if c0(q) = lim E[D]_vol/tau0 is also linear, the thin window
limit R_v(0,q) = <T>_q/c0(q) is a closed-form curve.
2026-09-23.  Quadrature exact (Legendre 256-pt); MC thin legs for c0.
"""
import json
import math
import sys

import numpy as np
from numpy.polynomial.legendre import leggauss

sys.path.insert(0, "deepseek_push")
from J02_moment_hierarchy import simulate


def first_flight_moments(ng=256):
    """E over (r_birth uniform in ball, mu isotropic) of:
    ch, I1 = int r^2 ds, I2 = int r^4 ds, I3 = int r^6 ds along first flight."""
    xr, wr = leggauss(ng); r = 0.5 * xr + 0.5
    xm, wm = leggauss(2 * ng); mu = xm
    R = r[:, None]; MU = mu[None, :]
    Wr = (3.0 * R ** 2) * (0.5 * wr[:, None])
    Wm = 0.5 * wm[None, :]
    cord = -R * MU + np.sqrt(np.maximum(0.0, 1.0 - R ** 2 * (1.0 - MU ** 2)))
    # along the ray: r2(s) = R^2 + 2 R MU s + s^2
    I1 = R ** 2 * cord + R * MU * cord ** 2 + cord ** 3 / 3.0   # int r^2 ds
    I2 = (R ** 4 * cord + 2 * R ** 3 * MU * cord ** 2
          + (2 * R ** 2 * MU ** 2 + R ** 2) * cord ** 3 / 3.0
          + R * MU * cord ** 4 / 2.0 + cord ** 5 / 5.0)          # int r^4 ds
    ch = float(np.sum(Wr * cord * Wm))
    a1 = float(np.sum(Wr * I1 * Wm))
    a2 = float(np.sum(Wr * I2 * Wm))
    # I3 = int r^6 ds = int (r2)^3 ds;  expand (R^2 + 2RMU s + s^2)^3:
    # (x + y + z)^3 with x=R^2, y=2RMU s, z=s^2:
    # x^3: R^6; 3x^2 y: 3 R^4 * 2RMU s = 6 R^5 MU s; 3 x^2 z: 3 R^4 s^2
    # 3 x y^2: 3 R^2 * 4 R^2 MU^2 s^2 = 12 R^4 MU^2 s^2; 6 x y z: 6*R^2*2RMU s*s^2
    #   = 12 R^3 MU s^3; 3 x z^2: 3 R^2 s^4
    # y^3: 8 R^3 MU^3 s^3; 3 y^2 z: 3*4R^2 MU^2 s^2*s = 12 R^2 MU^2 s^3
    # 3 y z^2: 3*2RMU s*s^4 = 6 R MU s^5; z^3: s^6
    I3 = (R ** 6 * cord + 6 * R ** 5 * MU * cord ** 2 / 2.0
          + 3 * R ** 4 * cord ** 3 / 3.0
          + 12 * R ** 4 * MU ** 2 * cord ** 3 / 3.0
          + 12 * R ** 3 * MU * cord ** 4 / 4.0
          + 3 * R ** 2 * cord ** 5 / 5.0
          + 8 * R ** 3 * MU ** 3 * cord ** 4 / 4.0
          + 12 * R ** 2 * MU ** 2 * cord ** 5 / 5.0
          + 6 * R * MU * cord ** 6 / 6.0
          + cord ** 7 / 7.0)
    a3 = float(np.sum(Wr * I3 * Wm))
    return ch, a1, a2, a3


def main():
    res = {"checks": {}, "measurements": {}}
    ok = True
    ch, a1, a2, a3 = first_flight_moments()
    res["measurements"]["chord_mean"] = ch
    res["measurements"]["E_int_r2"] = a1
    res["measurements"]["E_int_r4"] = a2
    res["measurements"]["E_int_r6"] = a3
    res["checks"]["chord_three_quarters"] = bool(abs(ch - 0.75) < 1e-9)
    res["checks"]["E_int_r2_five_twelfths"] = bool(abs(a1 - 5.0/12.0) < 1e-9)
    res["checks"]["E_int_r4_quarter"] = bool(abs(a2 - 0.25) < 1e-9)
    ok &= res["checks"]["chord_three_quarters"]
    ok &= res["checks"]["E_int_r2_five_twelfths"]
    ok &= res["checks"]["E_int_r4_quarter"]
    print(f"<chord>     = {ch:.12f}   (3/4 = {3/4:.12f})")
    print(f"E[int r^2]  = {a1:.12f}   (5/12 = {5/12:.12f})")
    print(f"E[int r^4]  = {a2:.12f}   (1/4  = {0.25:.12f})  <-- NEW closed form")
    print(f"E[int r^6]  = {a3:.12f}   (candidates: 7/36 = {7/36:.12f}, 1/6 = {1/6:.12f}, 3/20 = {3/20:.12f})")
    # pattern check: 3/4, 5/12, 3/12(=1/4), ... -> (k+2)/(2k+4)?  k=2: 4/8=1/2 no.
    # moment sequence: 0.75, 0.416667, 0.25 -> ratios 5/9, 3/5.  Try a3 = 7/36? 
    for cand, name in ((7/36, "7/36"), (1/6, "1/6"), (7/40, "7/40"), (0.175, "0.175")):
        print(f"    E[int r^6] vs {name}: diff {abs(a3-cand):+.2e}")

    # <T>_q = ch + q*a1 linearity check at several q
    print("\n<T>_q = 3/4 + 5q/12  vs  ch + q*a1 :")
    for q in (0.0, 1.0, 3.0, 10.0, 20.0):
        Tq = ch + q * a1
        pred = 0.75 + q * 5.0/12.0
        res["measurements"][f"T_q{int(q)}"] = Tq
        res["checks"][f"Tlinear_q{int(q)}"] = bool(abs(Tq - pred) < 1e-8)
        ok &= res["checks"][f"Tlinear_q{int(q)}"]
        print(f"  q={q:5.1f}: {Tq:.12f} vs {pred:.12f} (diff {Tq-pred:+.1e})")

    # thin-limit atom: -ln A_v ~ tau0 <T>_q  ->  verify A_v vs quadrature at tau0=0.05
    # with the exact tau_esc = tau0*(chord + q*I1) integrated form.
    ng = 192
    xr, wr = leggauss(ng); r = 0.5 * xr + 0.5
    xm, wm = leggauss(2 * ng); mu = xm
    R = r[:, None]; MU = mu[None, :]
    Wr = (3.0 * R ** 2) * (0.5 * wr[:, None]); Wm = 0.5 * wm[None, :]
    cord = -R * MU + np.sqrt(np.maximum(0.0, 1.0 - R ** 2 * (1.0 - MU ** 2)))
    I1 = R ** 2 * cord + R * MU * cord ** 2 + cord ** 3 / 3.0
    for q in (0.0, 3.0, 10.0):
        t0 = 0.005          # limit law: remainder is O((tau0<T>)^2) ~ 3e-4
        A_quad = float(np.sum(Wr * np.exp(-t0 * (cord + q * I1)) * Wm))
        thin = np.exp(-t0 * (0.75 + q * 5.0/12.0))
        res["measurements"][f"thinA_q{int(q)}"] = dict(A_quad=A_quad, closed=thin)
        res["checks"][f"thinA_q{int(q)}"] = bool(abs(A_quad - thin) < 2e-3)
        ok &= res["checks"][f"thinA_q{int(q)}"]
        print(f"  thin atom q={q:5.1f}: quadrature {A_quad:.6f} vs exp(-<T>t0) {thin:.6f}")

    # c0(q) = lim E[D]_vol/tau0 from thin MC (n=3e6, tau0=1e-3)
    print("\nc0(q) = lim E[D]_vol/tau0, thin MC (tau0 = 1e-3, n = 3e6):")
    cs = {}
    for q in (0.0, 3.0, 10.0):
        r = simulate(3_000_000, 1e-3, q, "volume", seed=555 + int(q))
        D = r["D"]
        c0 = float(np.mean(D)) / 1e-3
        s = float(np.std(D, ddof=1) / np.sqrt(len(D))) / 1e-3
        cs[q] = (c0, s)
        res["measurements"][f"c0_q{int(q)}"] = dict(c=c0, s=s)
        print(f"  q={q:5.1f}: c0 = {c0:.4f} +- {s:.4f}")
    # linearity: does c0(q) = a + b q? fit q=0,3,10
    if all(cs[q][1] < 0.02 for q in cs):
        b = (cs[10.0][0] - cs[0.0][0]) / 10.0
        a = cs[0.0][0]
        pred3 = a + 3 * b
        z = abs(pred3 - cs[3.0][0]) / math.hypot(cs[3.0][1], 3 * (cs[10.0][1] + cs[0.0][1]) / 10.0)
        res["measurements"]["c0_linear_fit"] = dict(a=a, b=b, pred_q3=pred3, z_q3=z)
        res["checks"]["c0_linear"] = bool(z < 3.0)
        ok &= res["checks"]["c0_linear"]
        print(f"  c0(q) ~ {a:.4f} + {b:.4f} q ;  q=3 prediction {pred3:.4f} vs measured {cs[3.0][0]:.4f} (z={z:.2f})")

    res["total_checks"] = len(res["checks"])
    res["passed"] = sum(1 for v in res["checks"].values() if v)
    res["ALL_PASSED"] = bool(ok)
    print(json.dumps(res, indent=1))
    print("ALL M05 CHECKS PASSED" if ok else "M05 CHECK FAILURE")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())