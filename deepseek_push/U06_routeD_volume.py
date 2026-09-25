#!/usr/bin/env python3
"""U06 -- ROUTE D ON THE VOLUME SOURCE: the N=1-sector law where the chords live.
Registration = this header, BEFORE any number (Y-WAVE_BRIEF.md). Companion to
V04b (central; same mechanism: J02 scatters before the next escape draw, so the
N=1 weight is exp(-tau_esc(along newu)) with the DIRECTION-COUPLED wall).

Geometry (unit ball, tau0=1, q=0): fix the first direction u = z_hat (isotropy).
Source x0 uniform in the ball: cylindrical coords around z_hat, rho in [0,1]
with measure prop-to rho d rho; GIVEN rho the axial offset c is UNIFORM on
[-b, b] with b = sqrt(1-rho^2) (chord half-length; U03/Kellerer i-randomness).
First collision at s in [0, 2b] from x0 along z_hat: density tau0 e^{-tau0 s} ds.
Scattered direction newu = mu z_hat + sqrt(1-mu^2)(cos(phi) x_hat + sin(phi) y_hat),
(mu, phi) ~ (3/8)(1+mu^2) dmu * dphi/(2pi).  Photon position x = (rho, 0, c+s):
    pd    = x.newu = rho*sqrt(1-mu^2)*cos(phi) + (c+s)*mu
    wall2 = -pd + sqrt(pd^2 + 1 - rho^2 - (c+s)^2)
    D|N=1 = s (1-mu)
ROUTE (registered): for m = 1..3
  E[D^m 1_{N=1}] = (3/2) int_0^1 rho d rho int_{-b}^{b} dc int_0^{2b} e^{-s} ds
      x int (3/8)(1+mu^2) dmu int_0^{2pi} dphi/(2pi)  s^m (1-mu)^m e^{-wall2}
((3/2) = uniform-ball density x the azimuth of x0; all factors per-photon.)

PRE-REGISTERED KILLS (both-ways):
  K1 machinery: route P(N=1) within 3 SE of MC P(N=1); V04's recorded volume
    value 0.241484 (n=3e6, section 1c) is the stored reference.
  K2 law: route E[D^m 1_{N=1}] within 3 SE of MC (n=2e6, 24-block jackknife)
    at m = 1, 2, 3 -> volume sector law MEASURED-CLOSED. Any miss -> honest
    FAIL, exit 1, table verbatim.
  K3 numerics: resolution witness at N=56 per axis: relative |delta| < 3e-3 on
    every reported number (5D GL; coarse tolerance registered deliberately).
  K4 scope: q != 0 out of scope; shell geometry out of scope; recorded open.
Run-1 note (fix-forward, recorded): run-1 of THIS FILE had a transposed s/mu
index in pd (z.T) that silently broadcast at equal axis sizes -- caught by the
P(N=1) machinery check tripling (0.722 vs 0.2415); fixed before any kill was
evaluated. Junk placeholder lines from run-1 removed wholesale.
"""
import json
import math
import sys
import time

import numpy as np

HERE = "/Users/carlzimmerman/new_physics/zimmerman-formula/deepseek_push"
sys.path.insert(0, HERE)
from J02_moment_hierarchy import simulate

RES = dict(lane="U06_routeD_volume", checks={}, route={}, mc={}, kills={},
           fix_forward="run-1 transposed index (z.T) in pd caught by K1 tripling; fixed pre-evaluation")
V04_MC_P1, V04_MC_P1_SE = 0.241484, 0.00025


def route(mmax, n):
    g = np.polynomial.legendre.leggauss(n)
    total = np.zeros(mmax)
    p1 = 0.0
    rho = g[0] * 0.5 + 0.5
    wr = g[1] * 0.5
    mu = g[0]
    wmu = g[1]
    phi = (g[0] + 1.0) * math.pi                  # phi in [0, 2pi]
    wphi = g[1] * math.pi
    MU3 = mu[:, None, None]
    COS = np.cos(phi)[None, None, :]
    WPHI = (wphi / (2.0 * math.pi))[None, None, :]
    for rv, rw in zip(rho, wr):
        b = math.sqrt(max(1.0 - rv * rv, 0.0))
        c = g[0] * b
        wc = g[1] * b
        S3 = None
        for cv, cw in zip(c, wc):
            Lc = b - cv                             # exit ahead of x0 along +z
            s = (g[0] + 1.0) * 0.5 * Lc
            ws = g[1] * 0.5 * Lc
            S3 = s[None, :, None]                  # (1, ns, 1)
            z = cv + s                              # (ns,)
            pd3 = rv * np.sqrt(1.0 - MU3 ** 2) * COS + z[None, :, None] * MU3
            r23 = rv * rv + (cv + s)[None, :, None] ** 2
            wall2 = -pd3 + np.sqrt(np.maximum(pd3 * pd3 + 1.0 - r23, 0.0))
            base = ((3.0 / 8.0) * (1.0 + mu[:, None, None] ** 2) *
                    np.exp(-wall2) * wmu[:, None, None] * WPHI)   # (nmu, ns, nphi)
            w_s = np.exp(-s)[None, :, None] * ws[None, :, None]
            cell0 = float((base * w_s).sum())
            p1 += cell0 * cw * rw * rv * 1.5
            for m in range(1, mmax + 1):
                cellm = float((base * (1.0 - MU3) ** m * (s ** m)[None, :, None] * w_s).sum())
                total[m - 1] += cellm * cw * rw * rv * 1.5
    return p1, total


def main():
    t0 = time.time()
    p1, mom = route(3, 40)
    p1b, momb = route(3, 56)
    rel = max(abs(a - b) / max(abs(a), 1e-30) for a, b in zip(mom, momb))
    RES["route"] = dict(P_N1=p1, moments=mom.tolist(), witness_P_N1=p1b,
                        witness_moments=momb.tolist(), rel_delta=rel)
    RES["checks"]["K3_witness_3e-3"] = bool(rel < 3e-3 and abs(p1 - p1b) / max(p1, 1e-30) < 3e-3)

    r = simulate(2_000_000, 1.0, 0.0, "volume", seed=20260927)
    D, N = r["D"], r["N"]
    m1 = (N == 1).astype(float)
    blocks = np.array_split(np.arange(len(D)), 24)
    mts, ses = [], []
    for m in (1, 2, 3):
        x = D ** m * m1
        bm = np.array([x[b].mean() for b in blocks])
        mts.append(float(x.mean())); ses.append(float(np.std(bm, ddof=1) / math.sqrt(24)))
    p1_mc = float(m1.mean())
    p1_se = float(np.std([m1[b].mean() for b in blocks], ddof=1) / math.sqrt(24))
    RES["mc"] = dict(n=2_000_000, seed=20260927, P_N1=p1_mc, P_N1_se=p1_se,
                     moments=mts, ses=ses)
    z1 = (p1 - p1_mc) / p1_se
    z1ref = (p1 - V04_MC_P1) / V04_MC_P1_SE
    RES["kills"]["K1_z"] = round(z1, 3); RES["kills"]["K1_z_vs_V04"] = round(z1ref, 3)
    RES["checks"]["K1_P_N1_machinery_3se"] = bool(abs(z1) < 3 and abs(z1ref) < 3)
    zs = [(mom[m - 1] - mts[m - 1]) / ses[m - 1] for m in (1, 2, 3)]
    RES["kills"]["K2_z_per_m"] = [round(z, 2) for z in zs]
    RES["checks"]["K2_all_m_within_3se"] = bool(max(abs(z) for z in zs) < 3)
    RES["verdict"] = ("VOLUME N=1-SECTOR LAW MEASURED-CLOSED (route D, 5D GL)"
                      if RES["checks"]["K2_all_m_within_3se"] and RES["checks"]["K1_P_N1_machinery_3se"]
                      else "ROUTE FAIL (kills fired; table verbatim)")
    RES["wall_seconds"] = round(time.time() - t0, 1)
    json.dump(RES, open(HERE + "/U06_routeD_volume.json", "w"), indent=1)
    print("route P(N=1)=%.6f witness=%.6f rel=%.2e" % (p1, p1b, rel))
    print("K1 z=%s z_vs_V04=%s | K2 z per m=%s" % (RES["kills"]["K1_z"],
          RES["kills"]["K1_z_vs_V04"], RES["kills"]["K2_z_per_m"]))
    print("VERDICT:", RES["verdict"])
    ok = RES["checks"]["K2_all_m_within_3se"] and RES["checks"]["K1_P_N1_machinery_3se"] and RES["checks"]["K3_witness_3e-3"]
    print("ALL U06 CHECKS PASSED" if ok else "U06 HONEST FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
