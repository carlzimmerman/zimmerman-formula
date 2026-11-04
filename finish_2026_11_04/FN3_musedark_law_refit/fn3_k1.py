"""FN3 stage 0: K0 (hashes), the frozen sample and z-thirds, and K1 (engine against the survey's released curves).

Criteria: FROZEN_CRITERIA.md (c6640225c2) sections 4 and 8. K1 uses the survey's own conventions (Planck15 kpc per
arcsec, h, E(z), Delta_vir from each run file) so the only thing tested is the mass-model engine. The convention list
(sgas k, drift form, MGE thickness) is the criteria's; every variant's score is written out.
kappa = 1/2 FITTED; not theory closed.
"""
import json
import math
import os
import sys

import numpy as np

import fn3_common as C

OUT = os.path.join(C.HERE, "fn3_k1")
LOG = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LOG.append(s)


def components(g, k, q, mge_cache):
    """survey-convention circular-speed components at the slit radii (kpc)."""
    p = g["par"]
    rot = g["rot"]
    kpc = g["kpc"]
    Re = p["radius"] * g["pixscale"] * kpc
    n = p["sersic_n"]
    r = np.abs(rot["dx_arcsec"]) * kpc
    v2dm, info = C.dc14_vc2(r, p["virial_velocity"], p["concentration"], p["log_X"], g["h"], g["Ez"], g["DeltaVir"])
    Mdisk = 10 ** p["log_X"] * info["Mvir"]
    key = round(n, 4)
    if key not in mge_cache:
        mge_cache[key] = C.sersic_mge(n)
    sig, frac, _ = mge_cache[key]
    v2disk = C.mge_vc2(r, sig * Re, frac, Mdisk, q)
    v2gas = C.sgas_vc2(r, p["gas_density"], k)
    # v22: the circular speed at 2.2 R_e / 1.678
    r22 = np.array([2.2 * Re / 1.678])
    v2dm22, _ = C.dc14_vc2(r22, p["virial_velocity"], p["concentration"], p["log_X"], g["h"], g["Ez"], g["DeltaVir"])
    vc22 = math.sqrt(float(v2dm22[0] + C.mge_vc2(r22, sig * Re, frac, Mdisk, q)[0] + C.sgas_vc2(r22, p["gas_density"], k)[0]))
    return r, Re, n, v2dm + v2disk + v2gas, vc22


def sigma_profile(g, r):
    """the model's total dispersion at the slit radii, and dln(sigma^2)/dlnR by finite differences in |R|."""
    s = np.asarray(g["rot"]["sig_kms"], float)
    o = np.argsort(r)
    rs, ss = r[o], s[o]
    lr = np.log(np.maximum(rs, 1e-4))
    d = np.gradient(np.log(ss ** 2), lr)
    out = np.empty_like(d)
    out[o] = d
    return s, out


def sample(phot, fit, gals):
    rows = []
    for gid, g in gals.items():
        ph = phot.get(gid, {})
        fs = fit.get(gid, {})
        p = g["par"]
        logm = ph.get("Mstar", float("nan"))
        z = ph.get("z", float("nan"))
        incl = ph.get("incl", float("nan"))
        v22 = g["der"].get("v22", float("nan"))
        s0 = p.get("velocity_dispersion", float("nan"))
        logz = fs.get("log_Z_DC14", float("nan"))
        cut = dict(mass=bool(np.isfinite(logm) and logm > 8.8), z=bool(np.isfinite(z) and 0.33 < z < 1.44),
                   incl=bool(np.isfinite(incl) and incl > 30), vsig=bool(np.isfinite(v22) and s0 > 0 and v22 / s0 > 1),
                   logz=bool(np.isfinite(logz) and logz < 15000), disc=not g["bulge"])
        rows.append(dict(gid=gid, z=z, logm=logm, incl=incl, v22=v22, sig0=s0, logZ=logz, cut=cut,
                         primary=all(cut.values()), secondary=all(v for k, v in cut.items() if k != "logz")))
    prim = sorted([r for r in rows if r["primary"]], key=lambda r: (r["z"], r["gid"]))
    N = len(prim)
    edges = [prim[0]["z"], prim[N // 3]["z"], prim[2 * N // 3]["z"], prim[-1]["z"]] if N >= 3 else []
    for i, r in enumerate(prim):
        r["third"] = 0 if i < N // 3 else (1 if i < 2 * N // 3 else 2)
    return rows, prim, edges


def main():
    n, fails = C.verify_hashes()
    P(f"K0: {n} files hashed, {len(fails)} failures -> {'PASS' if not fails else 'FAIL'}")
    if fails:
        P("K0 FAIL: stop", fails[:10])
        sys.exit(1)
    phot, fit = C.load_catalogue()
    gals = {gid: C.load_galaxy(gid) for gid in C.galaxy_ids()}
    rows, prim, edges = sample(phot, fit, gals)
    sec = [r for r in rows if r["secondary"]]
    P(f"sample: {len(rows)} runs; primary {len(prim)}; secondary (no log Z cut) {len(sec)}")
    for k in ("mass", "z", "incl", "vsig", "logz", "disc"):
        P(f"  cut {k}: {sum(r['cut'][k] for r in rows)} pass")
    thirds = [[r for r in prim if r["third"] == t] for t in range(3)]
    for t in range(3):
        zz = [r["z"] for r in thirds[t]]
        P(f"  third {t}: N {len(zz)}, z {min(zz):.3f}-{max(zz):.3f}, median {np.median(zz):.3f}")
    json.dump(dict(criteria="c6640225c2", primary=[r["gid"] for r in prim], secondary=[r["gid"] for r in sec],
                   thirds={str(t): [r["gid"] for r in thirds[t]] for t in range(3)},
                   rows=[{k: v for k, v in r.items()} for r in rows]),
              open(os.path.join(C.HERE, "fn3_sample.json"), "w"), indent=1, default=float)

    disc = [gid for gid, g in gals.items() if not g["bulge"]]
    variants = [(kn, k, d, qn, q) for kn, k in (("pi", math.pi), ("2pi", 2 * math.pi)) for d in ("D1", "D2", "D3")
                for qn, q in (("q0.15", 0.15), ("thin", 1e-3), ("sphere", 1.0))]
    res = {}
    pset = set(r["gid"] for r in prim)
    for kn, k, d, qn, q in variants:
        tag = f"{kn}|{d}|{qn}"
        cache = {}
        per = {}
        for gid in disc:
            g = gals[gid]
            r, Re, n_, v2c, vc22 = components(g, k, q, cache)
            s, dls2 = sigma_profile(g, r)
            v2ad = C.drift_v2(d, r, Re, n_, s, g["par"]["velocity_dispersion"], dls2)
            vperp = np.sqrt(np.maximum(v2c - v2ad, 0.0))
            vobs = np.abs(np.asarray(g["rot"]["v_kms"], float))
            rr = np.abs(np.asarray(g["rot"]["rad_Re"], float))
            m = (rr >= 0.5) & (rr <= 2.5) & (vobs > 0)
            rms = float(np.sqrt(np.mean((vperp[m] / vobs[m] - 1) ** 2))) if m.sum() else float("nan")
            dv22 = vc22 / g["der"]["v22"] - 1
            per[gid] = dict(rms=rms, dv22=dv22, npts=int(m.sum()))
        P_ = [per[g]["rms"] for g in per if g in pset and np.isfinite(per[g]["rms"])]
        V_ = [per[g]["dv22"] for g in per if g in pset]
        f_rms = float(np.mean(np.array(P_) <= 0.03)) if P_ else float("nan")
        f_v22 = float(np.mean(np.abs(np.array(V_)) <= 0.03)) if V_ else float("nan")
        res[tag] = dict(per=per, frac_rms_le_3pct=f_rms, frac_v22_le_3pct=f_v22, median_rms=float(np.median(P_)),
                        median_dv22=float(np.median(V_)), passes=bool(f_rms >= 0.9 and f_v22 >= 0.9))
        P(f"K1 {tag:20s} primary: rms<=3% {f_rms:.3f}  v22<=3% {f_v22:.3f}  median rms {np.median(P_):.4f}  "
          f"median dv22 {np.median(V_):+.4f}  -> {'PASS' if res[tag]['passes'] else 'fail'}")
    passing = [t for t in res if res[t]["passes"]]
    if passing:
        best = min(passing, key=lambda t: res[t]["median_rms"])
        P(f"K1 PASS: {len(passing)} of {len(res)} conventions pass; pinned (lowest median rms among passing): {best}")
    else:
        best = None
        P("K1 FAIL as frozen: no listed convention passes both lines. Stage 0 forecast reads NOT EVALUABLE.")
    json.dump(dict(criteria="c6640225c2", pinned=best, passing=passing,
                   scores={t: {k: v for k, v in r.items() if k != "per"} for t, r in res.items()},
                   per_galaxy={t: r["per"] for t, r in res.items()}),
              open(OUT + ".json", "w"), indent=1, default=float)
    open(OUT + ".out", "w").write("\n".join(LOG) + "\nkappa = 1/2 FITTED; not theory closed.\n")


if __name__ == "__main__":
    main()
