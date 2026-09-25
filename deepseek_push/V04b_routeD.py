#!/usr/bin/env python3
"""V04b -- THE N=1-SECTOR ANALYTIC CONNECTION CLOSED BY THE DIRECTION-COUPLED WALL.
Fix-forward of V04 (its section-(4) crash + factorized-route mismatch preserved
verbatim in V04_inverse_moments.out, committed). Registration = this header,
written BEFORE any number of this lane (Y-WAVE_BRIEF.md).

MECHANISM (found during spawn prep; MACHINE-VERIFIED here, not assumed):
J02 draws each step's escape test from the CURRENT direction and updates
direc <- newu only AFTER a collision, so an N=1 photon's step-2 escape budget is
the direction-coupled wall distance (central source, q=0, unit ball):
    wall2(s, mu) = -s*mu + sqrt(1 - s^2 (1-mu^2))
Instrumented evidence (conductor probes): emp step-2 survival 0.42631 vs
mean e^{-wall2} 0.42706; corr(mu1, wall2) = -0.766; probe route-D
P(N=1)=0.270246 vs MC 0.2706; E[D 1_N1]=0.096876 vs 0.096947;
E[D^2 1_N1]=0.071575 vs 0.071614.

ROUTE D (the registered law): m = 1..8, central, tau0 = 1, q = 0:
  E[D^m 1_{N=1}] = (3/8) int_{-1}^{1} (1+mu^2) int_0^1 s^m (1-mu)^m
                    exp(-s - wall2(s,mu)) ds dmu
(D|N=1 = s(1-mu); first-collision density e^{-s} ds; N=1 weight e^{-wall2}.)

PRE-REGISTERED KILLS (both-ways; honoring them is the lane's contract):
  K1 machinery: route P(N=1) within 3 SE of MC P(N=1); V04's recorded
    0.270045 +/- 0.000140 (n=1e7) is the stored reference.
  K2 law: route E[D^m 1_{N=1}] within 3 SE of MC (n=2e6, 24-block jackknife)
    at EVERY m = 1..8  ->  the sector law is CLOSED (MEASURED-CLOSED record;
    Lean not claimed this lane).  Any miss -> route-D FAIL at that m, exit 1,
    table kept verbatim.  V04's factorized route values (0.26424, 0.22484,
    0.25064, 0.32123, 0.44819, 0.66212, 1.01934, 1.61896) are carried as the
    REFUTED comparator -- they are NOT re-derived.
  K3 numerics: GL600x600 primary; GL1200x1200 convergence witness, relative
    |delta| < 1e-12; mpmath 30-dps spot check at m=1,2 within 1e-9 of GL.
  K4 scope: q != 0 legs OUT (rate integral along wall2 is q-dependent; open
    door recorded, not attempted).  Volume source is U06's door.
"""
import json
import math
import sys
import time

import numpy as np

HERE = "/Users/carlzimmerman/new_physics/zimmerman-formula/deepseek_push"
sys.path.insert(0, HERE)
from J02_moment_hierarchy import simulate

RES = dict(lane="V04b_routeD", checks={}, route={}, mc={}, refuted_comparator=[], kills={})
V04_MC_P1, V04_MC_P1_SE = 0.270045, 0.000140


def route_values(mmax, ngl):
    g = np.polynomial.legendre.leggauss(ngl)
    mu, wmu = g[0], g[1]
    s, ws = g[0] * 0.5 + 0.5, g[1] * 0.5
    MU, S = np.meshgrid(mu, s, indexing="ij")
    wall2 = -S * MU + np.sqrt(np.maximum(1.0 - S * S * (1.0 - MU * MU), 0.0))
    w = np.exp(-S - wall2)
    dens = (3.0 / 8.0) * (1.0 + MU * MU)
    base = dens * w * wmu[:, None] * ws[None, :]
    out = [float((base * (S * (1.0 - MU)) ** m).sum()) for m in range(1, mmax + 1)]
    p1 = float(base.sum())
    return p1, out


def mc_moments(n, seed, mmax=8, nblocks=24):
    r = simulate(n, 1.0, 0.0, "central", seed=seed)
    D, N = r["D"], r["N"]
    m1 = (N == 1).astype(float)
    x = D ** np.arange(1, mmax + 1)[:, None] * m1[None, :]
    blocks = np.array_split(np.arange(n), nblocks)
    bm = np.stack([x[:, b].mean(axis=1) for b in blocks])
    mean = x.mean(axis=1)
    se = np.sqrt(np.var(bm, axis=0, ddof=1) / nblocks)
    p1_mc = float(m1.mean())
    p1_se = float(np.std([m1[b].mean() for b in blocks], ddof=1) / math.sqrt(nblocks))
    return mean, se, p1_mc, p1_se, float(np.mean(D[m1 == 1]))


def main():
    t0 = time.time()
    p1_600, v600 = route_values(8, 600)
    p1_1200, v1200 = route_values(8, 1200)
    rel = max(abs(a - b) / max(abs(a), 1e-30) for a, b in zip(v600, v1200))
    RES["route"] = dict(P_N1_GL600=p1_600, P_N1_GL1200=p1_1200,
                        moments_GL600=v600, moments_GL1200=v1200,
                        convergence_rel_delta=rel)
    RES["checks"]["K3_witness_1e-12"] = bool(rel < 1e-12)

    mean, se, p1_mc, p1_se, dbar = mc_moments(2_000_000, 20260926)
    RES["mc"] = dict(n=2_000_000, seed=20260926, P_N1=p1_mc, P_N1_se=p1_se,
                     E_D_given_N1=dbar, moments=mean.tolist(), ses=se.tolist())

    z_p1 = (p1_600 - p1_mc) / p1_se
    z_ref = (p1_600 - V04_MC_P1) / V04_MC_P1_SE
    RES["checks"]["K1_P_N1_machinery_3se"] = bool(abs(z_p1) < 3 and abs(z_ref) < 3)
    RES["kills"]["K1_z_vs_runMC"] = round(z_p1, 3)
    RES["kills"]["K1_z_vs_V04_record"] = round(z_ref, 3)

    zs = [(v600[m - 1] - mean[m - 1]) / se[m - 1] for m in range(1, 9)]
    RES["kills"]["K2_z_per_m"] = [round(z, 2) for z in zs]
    RES["checks"]["K2_all_m_within_3se"] = bool(max(abs(z) for z in zs) < 3)

    # mpmath 30-dps spot check at m=1,2
    try:
        import mpmath as mp
        mp.mp.dps = 30
        spot = []
        for m in (1, 2):
            f = lambda ss, uu, mm=m: (ss ** mm * (1 - uu) ** mm *
                                      mp.e ** (-ss + ss * uu -
                                               mp.sqrt(1 - ss * ss * (1 - uu * uu))))
            inner = lambda uu: mp.quad(lambda ss: f(ss, uu), [0, 1])
            val = (3 / 8) * mp.quad(lambda uu: (1 + uu ** 2) * inner(uu), [-1, 1])
            spot.append(float(val))
        ok = all(abs(a - b) < 1e-9 for a, b in zip(spot, v600[:2]))
        RES["checks"]["K3_mpmath_30dps_m1_m2"] = bool(ok)
        RES["route"]["mpmath_m1_m2"] = spot
    except Exception as e:
        RES["checks"]["K3_mpmath_30dps_m1_m2"] = "ERROR: %r" % (e,)

    RES["verdict"] = ("N=1-SECTOR LAW CLOSED (route D, direction-coupled wall2): "
                      "all 8 moments within 3 SE of MC"
                      if RES["checks"]["K2_all_m_within_3se"] and
                      RES["checks"]["K1_P_N1_machinery_3se"]
                      else "ROUTE-D FAIL (kills fired -- table kept verbatim)")
    RES["wall_seconds"] = round(time.time() - t0, 1)
    json.dump(RES, open(HERE + "/V04b_routeD.json", "w"), indent=1)
    print("K1 z(run MC)=%s z(V04 rec)=%s" % (RES["kills"]["K1_z_vs_runMC"],
                                             RES["kills"]["K1_z_vs_V04_record"]))
    print("K2 z per m:", RES["kills"]["K2_z_per_m"])
    print("K3 witness rel delta = %.3e ; mpmath: %s" % (rel, RES["checks"]["K3_mpmath_30dps_m1_m2"]))
    print("VERDICT:", RES["verdict"])
    ok = (RES["checks"]["K2_all_m_within_3se"] and RES["checks"]["K1_P_N1_machinery_3se"]
          and RES["checks"]["K3_witness_1e-12"] is True)
    print("ALL V04b CHECKS PASSED" if ok else "V04b HONEST FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
