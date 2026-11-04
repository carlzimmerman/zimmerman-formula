"""FN3 K2' (amendment A2): population-level recovery on a fresh synthetic set, before any Stage 1 data.

Templates: all 71 primary galaxies (released geometry, SED mass, PSF), in the real z-thirds. Seeds: noise
20261105 + id; Sigma_HI draw and start perturbations 30261105 + id (not K2's). Planted Sigma_HI ~ U[0, 15].
Scenarios on the same templates: flat (Delta = 0) and rising (Delta = 0.6 (z - median z)). Noise: matched-filter
S/N 30. Canonical band; drift R0. MUTATE: a0 x 2 refit of the flat scenario.
Lines (A2): (a) |median bias| <= 0.07 in every third (flat); (b) flat Theil-Sen slope within 0 +- 0.10 per unit z;
(c) rising slope within 0.60 +- 0.10; (d) MUTATE median shift within -0.30 +- 0.07.
kappa = 1/2 FITTED; not theory closed.
"""
import json
import math
import os
import signal
import sys
import time

import numpy as np
from scipy import stats

import fn3_common as C
import fn3_cube as F
from fn3_k2 import bounds, setup

OUTJ = os.path.join(C.HERE, "fn3_k2p.jsonl")
STOP = False


def _term(*_):
    global STOP
    STOP = True


signal.signal(signal.SIGTERM, _term)


def one(gid, scen, zmed, N, P15, phot, start=None):
    g, z, kpc, logm_sed, mu, cm, geo = setup(gid, N, P15, phot)
    a0 = C.A_FOOT["canonical"] * float(N.band_ratio(z))
    rs = np.random.default_rng(30261105 + gid)
    sighi = float(rs.uniform(0.0, 15.0))
    d_true = 0.0 if scen == "flat" else 0.6 * (z - zmed)
    MH2 = mu * 10 ** logm_sed
    mass = F.LawMass(MH2, a0)
    gen = F.Fitter(cm, None, np.ones((25, 25, 25)), mass, "law")
    th_true = np.array([geo[k] for k in F.GEO] + [geo["sig0"], logm_sed + d_true, sighi])
    m = gen.model(th_true)
    sig = math.sqrt(float(np.sum(m ** 2))) / 30.0
    data = m + np.random.default_rng(20261105 + gid).normal(0.0, sig, m.shape)
    var = np.full(m.shape, sig * sig)
    lo, hi = bounds(geo, logm_sed)
    th0 = th_true.copy()
    th0[0:3] += rs.normal(0, 0.3, 3)
    th0[3] *= 1 + rs.normal(0, 0.1)
    th0[4] *= 1 + rs.normal(0, 0.1)
    th0[6] += rs.normal(0, 2.0)
    th0[7] += rs.normal(0, 5.0)
    th0[9] = geo["sig0"] * (1 + rs.normal(0, 0.2))
    th0[10] = logm_sed
    th0[11] = 7.5
    r1 = F.Fitter(cm, data, var, mass, "law").fit(th0, lo, hi)
    rec = dict(gid=gid, scen=scen, z=z, logm_sed=logm_sed, d_true=d_true, sighi_true=sighi,
               d_fit=float(r1["x"][10] - logm_sed), sighi_fit=float(r1["x"][11]), chi2_red=r1["chi2_red"])
    if scen == "flat":
        lo2 = lo.copy()
        lo2[10] -= 0.5
        rM = F.Fitter(cm, data, var, F.LawMass(MH2, 2 * a0), "law").fit(r1["x"], lo2, hi)
        rec["d_fit_mutate"] = float(rM["x"][10] - logm_sed)
    return rec


def main():
    N = C.Native()
    P15 = C.planck15()
    phot, _ = C.load_catalogue()
    s = json.load(open(os.path.join(C.HERE, "fn3_sample.json")))
    third = {gid: int(t) for t, gl in s["thirds"].items() for gid in gl}
    prim = s["primary"]
    zmed = float(np.median([phot[g]["z"] for g in prim]))
    done = {}
    if os.path.exists(OUTJ):
        for ln in open(OUTJ):
            d = json.loads(ln)
            done[(d["gid"], d["scen"])] = d
    t0 = time.time()
    for scen in ("flat", "rising"):
        for gid in prim:
            if (gid, scen) in done:
                continue
            if STOP:
                print("SIGTERM: stopping cleanly")
                sys.exit(75)
            rec = one(gid, scen, zmed, N, P15, phot)
            rec["third"] = third[gid]
            done[(gid, scen)] = rec
            with open(OUTJ, "a") as fh:
                fh.write(json.dumps(rec) + "\n")
            print(f"{scen:6s} ID{gid:<5d} z {rec['z']:.3f} true {rec['d_true']:+.3f} fit {rec['d_fit']:+.3f} "
                  f"SigHI {rec['sighi_true']:5.2f}->{rec['sighi_fit']:5.2f} ({time.time() - t0:.0f}s)", flush=True)
    flat = [done[(g, "flat")] for g in prim]
    rise = [done[(g, "rising")] for g in prim]
    lines = [f"K2' (A2), fresh synthetics, N {len(prim)} per scenario, matched-filter S/N 30, Sigma_HI ~ U[0, 15]"]
    ok_a = True
    for t in range(3):
        e = [r["d_fit"] - r["d_true"] for r in flat if r["third"] == t]
        b = float(np.median(e))
        ok_a &= abs(b) <= 0.07
        lines.append(f"  (a) third {t}: N {len(e)}, median bias {b:+.4f} (line 0.07) -> {'PASS' if abs(b) <= 0.07 else 'FAIL'}")
    sf = stats.theilslopes([r["d_fit"] for r in flat], [r["z"] for r in flat])[0]
    sr = stats.theilslopes([r["d_fit"] for r in rise], [r["z"] for r in rise])[0]
    ok_b, ok_c = abs(sf) <= 0.10, abs(sr - 0.60) <= 0.10
    sh = float(np.median([r["d_fit_mutate"] - r["d_fit"] for r in flat]))
    ok_d = abs(sh + 0.30) <= 0.07
    lines.append(f"  (b) flat slope {sf:+.4f} (line 0 +- 0.10) -> {'PASS' if ok_b else 'FAIL'}")
    lines.append(f"  (c) rising slope {sr:+.4f} (line 0.60 +- 0.10) -> {'PASS' if ok_c else 'FAIL'}")
    lines.append(f"  (d) MUTATE a0 x 2 median shift {sh:+.4f} (line -0.30 +- 0.07) -> {'PASS (bites)' if ok_d else 'FAIL'}")
    e_all = np.array([r["d_fit"] - r["d_true"] for r in flat])
    lines.append(f"  per-galaxy scatter (flat): 16-84 % [{np.percentile(e_all, 16):+.3f}, {np.percentile(e_all, 84):+.3f}]")
    allok = bool(ok_a and ok_b and ok_c and ok_d)
    lines.append(f"K2' {'PASS: an A2 label may be issued in Stage 1' if allok else 'FAIL: no A2 label either'}")
    lines.append("kappa = 1/2 FITTED; not theory closed.")
    print("\n".join(lines))
    open(os.path.join(C.HERE, "fn3_k2p.out"), "w").write("\n".join(lines) + "\n")
    json.dump(dict(amendment="A2", pass_=allok, a=ok_a, b=ok_b, c=ok_c, d=ok_d, slope_flat=sf, slope_rising=sr,
                   mutate_shift=sh, zmed=zmed), open(os.path.join(C.HERE, "fn3_k2p.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
