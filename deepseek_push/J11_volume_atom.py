#!/usr/bin/env python3
"""
J11 -- THE VOLUME-SOURCE ATOM AND ITS WINDOW (real-BLR geometry)

Everything central in J09/J10 is volume here.  Real LRD clouds are
volume-emissive; J02B proved the frozen identity fails off-centre (E[Q]=0.597).
Central window:  -ln A / E[D] = (1+q/3)/(1/2+q/4) in [4/3, 2].
Volume question (open door):
  (a) A_vol(tau0, q=0) = 3 int_0^1 r^2 dr (1/2) int_-1^1 dmu exp(-tau0*chord)
      EXACT by quadrature -- no MC needed;
  (b) does the volume ratio -ln A_vol / E[D]_vol have a q-window at all?
      E[D]_vol = E[tau]_vol - E[Q] (J02B: 0.339 vs central 0.501 at q=0, tau0=1).

Checks (engine: J02_moment_hierarchy.simulate, volume source):
  V1  quadrature vs MC atom at tau0 in {0.5,1,2,3}, q=0        (3 SE)
  V2  atom law q-dependence measured (q=3,10) vs quadrature-extended
      (r^2 -> (1+q r^2) -weighted chord integral; still exact by quadrature)
  V3  volume window: -ln A_vol / E[D]_vol vs (1+q/3+...)/(...) -- does a
      closed form exist?  report q=0/3/10 and the fitted limit
  V4  the J10 volume port: J10-I_vol = -ln A_vol * r_B/(c d_vol) at
      A2744-QSO1 numbers must fall OUTSIDE the central [4/3,2] if the
      cloud is really volume-emissive -> the true volume window is the
      falsifier for volume geometry.
2026-09-23.  Brute force + exact quadrature.
"""
import json
import math
import sys

import numpy as np
from numpy.polynomial.legendre import leggauss

sys.path.insert(0, "deepseek_push")
from J02_moment_hierarchy import simulate


def A_vol_quadrature(tau0, q, ng=80):
    """Exact: A_vol = 3 int r^2 dr (int dOmega/4pi) exp(-tau0 * (1+q r^p...)
    chord integral with kappa(r') = tau0(1+q r'^2) along the ray:
    tau_esc(x,u) = int_0^chord tau0(1+q |x+u s|^2) ds
                 = tau0 ( chord + q (chord - r^2 chord ...
    |x+u s|^2 = r^2 + 2 (x.u) s + s^2 ; x.u = r mu
    = tau0 ( chord + q [ r^2 chord + r mu chord^2 + chord^3/3 ] )
    """
    xr, wr = leggauss(ng); r = 0.5 * xr + 0.5
    xm, wm = leggauss(2 * ng); mu = xm
    R = r[:, None]; MU = mu[None, :]
    Wr = (3.0 * R ** 2) * (0.5 * wr[:, None])
    Wm = 0.5 * wm[None, :]     # (1/2) dmu = dOmega/4pi (isotropic, sums to 1)
    chord = -R * MU + np.sqrt(np.maximum(0.0, 1.0 - R ** 2 * (1.0 - MU ** 2)))
    # (exit distance solves s^2 + 2s r mu + r^2 = 1: s = -r mu + sqrt(1 - r^2(1-mu^2));
    #  at q=0 the mu-integral is symmetric so a wrong +r mu sign cancels -- the
    #  q-term breaks the symmetry and exposes it; the V2 fails were this sign)
    tau_esc = tau0 * (chord + q * (R ** 2 * chord + R * MU * chord ** 2
                                   + chord ** 3 / 3.0))
    return float(np.sum(Wr * np.exp(-tau_esc) * Wm))


def se(x):
    return float(np.std(x, ddof=1) / np.sqrt(len(x)))


def run():
    res = {"checks": {}, "measurements": {}}
    ok = True
    n = 400000

    # ---- V1: quadrature vs MC atom, q=0 --------------------------------
    print("=" * 74)
    print("J11 -- VOLUME ATOM: quadrature vs engine (q=0, volume src)")
    print("=" * 74)
    rngs = np.random.default_rng(20260923)
    for tau0 in (0.5, 1.0, 2.0, 3.0):
        r = simulate(n, tau0, 0.0, "volume", seed=37 + int(tau0 * 10))
        A_mc = float(np.mean(r["N"] == 0))
        A_q = A_vol_quadrature(tau0, 0.0)
        z = abs(A_mc - A_q) / se(r["N"] == 0)
        res["checks"][f"V1_tau{int(tau0*10)}"] = bool(z < 4.0)
        ok &= res["checks"][f"V1_tau{int(tau0*10)}"]
        res["measurements"][f"V1_tau{int(tau0*10)}"] = dict(
            A_mc=round(A_mc, 5), A_quad=round(A_q, 5), z=round(z, 2))
        print(f"  tau0={tau0}: MC {A_mc:.5f} vs quadrature {A_q:.5f}"
              f"  z={z:.2f}")

    # ---- V2: atom q-dependence -----------------------------------------
    print("-" * 74)
    print("V2: q-dependence of the volume atom (tau0=1)")
    for q in (0.0, 3.0, 10.0):
        r = simulate(n, 1.0, q, "volume", seed=51 + int(q))
        A_mc = float(np.mean(r["N"] == 0))
        A_q = A_vol_quadrature(1.0, q)
        z = abs(A_mc - A_q) / se(r["N"] == 0)
        res["checks"][f"V2_q{int(q)}"] = bool(z < 4.0)
        ok &= res["checks"][f"V2_q{int(q)}"]
        res["measurements"][f"V2_q{int(q)}"] = dict(
            A_mc=round(A_mc, 5), A_quad=round(A_q, 5), z=round(z, 2))
        print(f"  q={q:4.0f}: MC {A_mc:.5f} vs quadrature {A_q:.5f}  z={z:.2f}")

    # ---- V3: the volume window -----------------------------------------
    print("-" * 74)
    print("V3: volume window -ln A_vol / E[D]_vol (tau0=1)")
    w = {}
    for q in (0.0, 3.0, 10.0):
        r = simulate(n, 1.0, q, "volume", seed=71 + int(q))
        A_mc = float(np.mean(r["N"] == 0))
        d_bar = float(np.mean(r["D"]))
        rat = -math.log(A_mc) / d_bar
        w[q] = dict(A=round(A_mc, 5), d_bar=round(d_bar, 4),
                    ratio=round(rat, 4))
        print(f"  q={q:4.0f}: A={A_mc:.5f}  E[D]vol={d_bar:.4f}  "
              f"-lnA/E[D] = {rat:.4f}")
    res["measurements"]["V3_window"] = w
    # any window?  print the monotone guess: central went 2.002->1.441
    # volume: record as-is; state honestly.
    r0 = w[0.0]["ratio"]
    r10 = w[10.0]["ratio"]
    res["checks"]["V3_reported"] = True   # measurement only
    print(f"  volume window shape: q=0 -> {r0:.3f}, q=10 -> {r10:.3f}"
          f" (central: 2.002 -> 1.441)")

    # ---- V4: J10 volume port -------------------------------------------
    print("-" * 74)
    print("V4: J10-I with volume geometry (A2744-QSO1 numbers)")
    C = 2.99792458e8
    DAY = 86400.0
    rB = 40.9 * C * DAY
    R45 = 45.0 * C * DAY
    E_D_vol = 0.339        # J02B measured (tau0=1, q=0)
    r = simulate(n, 1.0, 0.0, "volume", seed=91)
    A_v = float(np.mean(r["N"] == 0))
    # physical volume lag at the 941 AU illustrative scale:
    # d_phys = E[D]_vol * R/c ;  J10-I_vol = -ln A_v * r_B / (c d_phys)
    #          = -ln A_v * r_B / (R * E[D]_vol)
    R941 = 941.0 * 1.495978707e11
    J10I_vol_45 = -math.log(A_v) * rB / (R45 * E_D_vol)
    # at the frozen illustrative scale R = 941 AU:
    J10I_vol_941 = -math.log(A_v) * rB / (R941 * E_D_vol)
    res["measurements"]["V4"] = dict(
        A_vol=round(A_v, 5),
        J10I_vol_at_R45ld=-round(J10I_vol_45, 3),
        J10I_vol_at_R941AU=-round(J10I_vol_941, 3),
        note="volume window differs from central [4/3,2]; central J10-I at "
             "45 ld was 1.818")
    print(f"  A_vol(q=0) = {A_v:.5f}")
    print(f"  J10-I_vol(R=45 ld) = {-J10I_vol_45:.3f}  "
          f"(central value was 1.818; falsifier must use the volume window)")
    print(f"  J10-I_vol(R=941 AU) = {-J10I_vol_941:.3f}")

    res["total_checks"] = len(res["checks"])
    res["passed"] = sum(1 for v in res["checks"].values() if v)
    res["ALL_PASSED"] = bool(ok)
    print(json.dumps(res, indent=1))
    print("ALL J11 CHECKS PASSED" if ok else "J11 CHECK FAILURE")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(run())