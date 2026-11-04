"""FN3 K2 and synthetic MUTATE (criteria s8): planted-law recovery on 20 synthetic cutouts.

Stated before the run: noise is white with sigma set so the matched-filter S/N of the [OII] model is 30 (survey S/N
spans ~10 to >100, Paper I). Galaxies: 20 primary galaxies evenly spaced in z, with their released geometry (r_half,
n, inclination, PA, sigma_0, line ratio, PSF) and SED mass (native D_L). Planted: the canonical band at each z,
Delta_true = 0 for even slots and +0.30 for odd, Sigma_HI 5 Msun/pc^2, H2 from Tacconi 2020 with delta_MS, drift R0.
Fit: every parameter free; inclination boxed +-5 deg around the planted value, as the survey boxed its photometric one.
K2 lines: median |Delta_fit - Delta_true| <= 0.05 dex; median(Delta_fit | +0.30) - median(Delta_fit | 0) within
0.30 +- 0.05. MUTATE: refit with a0 x 2; median shift of Delta within -0.30 +- 0.07.
Checkpoints per galaxy to fn3_k2.jsonl; SIGTERM exits cleanly. kappa = 1/2 FITTED; not theory closed.
"""
import json
import math
import os
import signal
import sys
import time

import numpy as np

import fn3_common as C
import fn3_cube as F

OUTJ = os.path.join(C.HERE, "fn3_k2.jsonl")
STOP = False


def _term(*_):
    global STOP
    STOP = True


signal.signal(signal.SIGTERM, _term)


def setup(gid, N, P15, phot):
    g = C.load_galaxy(gid)
    p = g["par"]
    ph = phot[gid]
    z = ph["z"]
    kpc = N.kpc_per_arcsec(z)
    dl2 = (float(N.DL(z)) / P15.luminosity_distance(z).value) ** 2
    logm_sed = ph["Mstar"] + math.log10(dl2)
    t = N.age_gyr(z)
    logsfr = math.log10(ph["SFR"]) + math.log10(dl2) if ph.get("SFR", 0) > 0 else None
    mu = C.mu_mol_t20(z, logm_sed, logsfr, t, use_dms=True)
    lam_mean = 0.5 * (F.L1 + F.L2) * (1 + z)
    lam = lam_mean + (np.arange(25) - 12) * 1.25
    cm = F.CubeModel(25, 25, lam, 0.2, kpc, g["psf"]["fwhm"], g["psf"]["beta"])
    rline = p.get("line_ratio", 0.7)
    rline = 0.7 if not np.isfinite(rline) else rline
    geo = dict(x0=12.0, y0=12.0, lc=(F.L1 * (1 + z) - lam[0]) / 1.25, flux=1000.0, rhalf=p["radius"] * 0.2,
               n=float(np.clip(p["sersic_n"], 0.5, 4.0)), inc=float(np.clip(p["inclination"], 20, 80)),
               pa=float(p["pa"] % 360.0), rline=float(rline), sig0=float(max(p["velocity_dispersion"], 5.0)))
    return g, z, kpc, logm_sed, mu, cm, geo


def bounds(geo, logm_sed, kind="law"):
    lo = [geo["x0"] - 2, geo["y0"] - 2, geo["lc"] - 2, geo["flux"] * 0.3, geo["rhalf"] * 0.5, 0.5,
          max(geo["inc"] - 5, 10), geo["pa"] - 30, 0.3, 0.0, logm_sed - 1.5, 0.0]
    hi = [geo["x0"] + 2, geo["y0"] + 2, geo["lc"] + 2, geo["flux"] * 3.0, geo["rhalf"] * 2.0, 4.0,
          min(geo["inc"] + 5, 85), geo["pa"] + 30, 1.5, 120.0, logm_sed + 1.5, 15.0]
    return np.array(lo), np.array(hi)


def main():
    N = C.Native()
    P15 = C.planck15()
    phot, _ = C.load_catalogue()
    s = json.load(open(os.path.join(C.HERE, "fn3_sample.json")))
    prim = s["primary"]
    rows = sorted([r for r in s["rows"] if r["gid"] in set(prim)], key=lambda r: (r["z"], r["gid"]))
    idx = np.round(np.linspace(0, len(rows) - 1, 20)).astype(int)
    pick = [rows[i]["gid"] for i in idx]
    done = {}
    if os.path.exists(OUTJ):
        for ln in open(OUTJ):
            d = json.loads(ln)
            done[d["gid"]] = d
    for slot, gid in enumerate(pick):
        if gid in done:
            continue
        if STOP:
            print("SIGTERM: stopping cleanly after", len(done), "galaxies")
            sys.exit(75)
        t0 = time.time()
        g, z, kpc, logm_sed, mu, cm, geo = setup(gid, N, P15, phot)
        a0 = C.A_FOOT["canonical"] * float(N.band_ratio(z))
        d_true = 0.0 if slot % 2 == 0 else 0.30
        logM_true = logm_sed + d_true
        MH2 = mu * 10 ** logm_sed
        mass = F.LawMass(MH2, a0)
        fit = F.Fitter(cm, None, np.ones((25, 25, 25)), mass, "law", drift_scale=1.0)
        th_true = np.array([geo[k] for k in F.GEO] + [geo["sig0"], logM_true, 5.0])
        m = fit.model(th_true)
        sig = math.sqrt(float(np.sum(m ** 2))) / 30.0
        rng = np.random.default_rng(20261104 + gid)
        data = m + rng.normal(0.0, sig, m.shape)
        var = np.full(m.shape, sig * sig)
        lo, hi = bounds(geo, logm_sed)
        rng2 = np.random.default_rng(1 + gid)
        th0 = th_true.copy()
        th0[0:3] += rng2.normal(0, 0.3, 3)
        th0[3] *= 1 + rng2.normal(0, 0.1)
        th0[4] *= 1 + rng2.normal(0, 0.1)
        th0[6] += rng2.normal(0, 2.0)
        th0[7] += rng2.normal(0, 5.0)
        th0[9] = geo["sig0"] * (1 + rng2.normal(0, 0.2))
        th0[10] = logm_sed
        th0[11] = 7.5
        f1 = F.Fitter(cm, data, var, mass, "law", drift_scale=1.0)
        r1 = f1.fit(th0, lo, hi)
        massM = F.LawMass(MH2, 2 * a0)
        fM = F.Fitter(cm, data, var, massM, "law", drift_scale=1.0)
        lo2, hi2 = lo.copy(), hi.copy()
        lo2[10] -= 0.5
        rM = fM.fit(r1["x"], lo2, hi2)
        rec = dict(gid=gid, slot=slot, z=z, logm_sed=logm_sed, d_true=d_true, mu=mu,
                   d_fit=float(r1["x"][10] - logm_sed), d_err=float(r1["err"][10]), sighi_fit=float(r1["x"][11]),
                   inc_true=geo["inc"], inc_fit=float(r1["x"][6]), chi2_red=r1["chi2_red"], nfev=r1["nfev"],
                   d_fit_mutate=float(rM["x"][10] - logm_sed), chi2_red_mutate=rM["chi2_red"], secs=time.time() - t0)
        done[gid] = rec
        with open(OUTJ, "a") as fh:
            fh.write(json.dumps(rec) + "\n")
        print(f"{slot:2d} ID{gid:<5d} z {z:.3f} Delta_true {d_true:+.2f} fit {rec['d_fit']:+.3f} +- {rec['d_err']:.3f} "
              f"SigHI {rec['sighi_fit']:5.2f} inc {geo['inc']:.1f}->{rec['inc_fit']:.1f} chi2r {r1['chi2_red']:.3f} "
              f"MUTATE {rec['d_fit_mutate']:+.3f} ({rec['secs']:.0f}s)", flush=True)
    recs = [done[g] for g in pick]
    err = np.array([r["d_fit"] - r["d_true"] for r in recs])
    d0 = np.median([r["d_fit"] for r in recs if r["d_true"] == 0])
    d3 = np.median([r["d_fit"] for r in recs if r["d_true"] > 0])
    shift = np.median([r["d_fit_mutate"] - r["d_fit"] for r in recs])
    k2a = bool(np.median(np.abs(err)) <= 0.05)
    k2b = bool(abs((d3 - d0) - 0.30) <= 0.05)
    mut = bool(abs(shift + 0.30) <= 0.07)
    lines = [f"K2: N {len(recs)}; median |Delta_fit - Delta_true| {np.median(np.abs(err)):.4f} (line 0.05) -> {'PASS' if k2a else 'FAIL'}",
             f"K2: planted +0.30 recovered as {d3 - d0:+.4f} (line 0.30 +- 0.05) -> {'PASS' if k2b else 'FAIL'}",
             f"K2: median bias {np.median(err):+.4f}; 16-84 % [{np.percentile(err, 16):+.4f}, {np.percentile(err, 84):+.4f}]",
             f"MUTATE (synthetic, a0 x 2): median shift {shift:+.4f} (line -0.30 +- 0.07) -> {'PASS (bites)' if mut else 'FAIL'}",
             "noise: matched-filter S/N 30; canonical band planted; kappa = 1/2 FITTED; not theory closed."]
    print("\n".join(lines))
    open(os.path.join(C.HERE, "fn3_k2.out"), "w").write("\n".join(lines) + "\n")
    json.dump(dict(criteria="c6640225c2", amendment="A1", picked=pick, K2a=k2a, K2b=k2b, MUTATE=mut,
                   median_abs_err=float(np.median(np.abs(err))), recovered_offset=float(d3 - d0),
                   mutate_shift=float(shift), records=recs), open(os.path.join(C.HERE, "fn3_k2.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
