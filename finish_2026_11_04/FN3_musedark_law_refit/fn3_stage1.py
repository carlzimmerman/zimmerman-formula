"""FN3 Stage 1 driver (criteria s5-s8, amendments A1, A2). Written before any cutout exists; runs only on cutouts that
fn3_fetch.py --approved wrote after the owner's yes.

Per galaxy (cutout ID<gid>.npz: DATA, STAT boxes 81 x 25 x 25, lam0, dlam, PSF):
  continuum subtracted per spaxel outside +-12 channels of the expected [OII] position; fit window 25 channels.
  K3 (first 10 primary galaxies): the survey's DC14 model refitted; v_c(2.2 R_e/1.678) against the released v22 (5 %),
      inclination against the released one (3 deg).
  law fits: footing x reading (R0-R7); context laws on R0; free a0 (M* at SED + H2) on R0; MUTATE a0 x 2 on R0.
Checkpoints per galaxy and fit to fn3_stage1.jsonl. SIGTERM exits cleanly (75). Single thread.
  python3 fn3_stage1.py RUN <cutout_dir>
  python3 fn3_stage1.py SELFTEST <scratch_dir>    plumbing test on 3 synthetic cutouts made by the engine
kappa = 1/2 FITTED; not theory closed.
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
from fn3_cutout import continuum_subtract

OUTJ = os.path.join(C.HERE, "fn3_stage1.jsonl")
STOP = False
READINGS = {"R0": dict(drift=1.0), "R1": dict(drift=0.5), "R2": dict(drift=0.0), "R3": dict(sighi=0.0),
            "R4": dict(sighi=15.0), "R5": dict(mu=0.5), "R6": dict(mu=2.0), "R7": dict(dms=False)}


def _term(*_):
    global STOP
    STOP = True


signal.signal(signal.SIGTERM, _term)


class PaperLaw(F.LawMass):
    pass


def prepare(gid, cut, N, P15, phot):
    g = C.load_galaxy(gid)
    ph = phot[gid]
    z = ph["z"]
    kpc = N.kpc_per_arcsec(z)
    dl2 = (float(N.DL(z)) / P15.luminosity_distance(z).value) ** 2
    logm = ph["Mstar"] + math.log10(dl2)
    logsfr = math.log10(ph["SFR"]) + math.log10(dl2) if ph.get("SFR", 0) > 0 else None
    t = N.age_gyr(z)
    lam_all = cut["lam0"] + cut["dlam"] * np.arange(cut["DATA"].shape[0])
    jc = float((F.L1 + F.L2) / 2 * (1 + z) - cut["lam0"]) / cut["dlam"]
    cs = continuum_subtract(cut["DATA"], cut["STAT"], jc, 12)
    j0 = int(round(jc)) - 12
    data = cs[j0:j0 + 25]
    var = cut["STAT"][j0:j0 + 25].astype(float)
    lam = lam_all[j0:j0 + 25]
    cm = F.CubeModel(25, 25, lam, 0.2, kpc, float(cut["psf_fwhm"]), float(cut["psf_beta"]))
    p = g["par"]
    incl_phot = ph.get("incl", p["inclination"])
    geo0 = dict(x0=12.0, y0=12.0, lc=(F.L1 * (1 + z) - lam[0]) / cut["dlam"],
                flux=float(np.nansum(np.where(np.isfinite(data), data, 0.0))) * 1.0, rhalf=max(p["radius"] * 0.2, 0.15),
                n=float(np.clip(p["sersic_n"], 0.5, 4.0)), inc=float(np.clip(incl_phot, 20, 80)), pa=float(p["pa"] % 360),
                rline=float(p.get("line_ratio", 0.7)) if np.isfinite(p.get("line_ratio", 0.7)) else 0.7,
                sig0=float(max(p["velocity_dispersion"], 5.0)))
    return dict(g=g, z=z, kpc=kpc, logm=logm, logsfr=logsfr, t=t, data=data, var=var, cm=cm, geo0=geo0)


def law_fit(P, a0, mu_scale=1.0, drift=1.0, sighi=None, dms=True, start=None, lo_ext=0.0):
    mu = C.mu_mol_t20(P["z"], P["logm"], P["logsfr"], P["t"], use_dms=dms) * mu_scale
    mass = F.LawMass(mu * 10 ** P["logm"], a0)
    fit = F.Fitter(P["cm"], P["data"], P["var"], mass, "law", drift_scale=drift, sighi_fixed=sighi)
    geo = P["geo0"]
    lo = [geo["x0"] - 3, geo["y0"] - 3, geo["lc"] - 3, max(geo["flux"], 1e-30) * 0.05, geo["rhalf"] * 0.3, 0.5,
          max(geo["inc"] - 5, 10), geo["pa"] - 45, 0.3, 0.0, P["logm"] - 2.0 - lo_ext]
    hi = [geo["x0"] + 3, geo["y0"] + 3, geo["lc"] + 3, max(geo["flux"], 1e-30) * 20, geo["rhalf"] * 3.0, 4.0,
          min(geo["inc"] + 5, 85), geo["pa"] + 45, 1.5, 150.0, P["logm"] + 2.0]
    th0 = [geo[k] for k in F.GEO] + [geo["sig0"], P["logm"]]
    if sighi is None:
        lo.append(0.0)
        hi.append(15.0)
        th0.append(7.5)
    if start is not None:
        th0 = list(start)
    r = fit.fit(np.array(th0), np.array(lo), np.array(hi))
    return r, mu


def dc14_fit(P):
    g = P["g"]
    p = g["par"]
    mass = F.DC14Mass(g["h"], g["Ez"], g["DeltaVir"])
    fit = F.Fitter(P["cm"], P["data"], P["var"], mass, "dc14", drift_scale=1.0)
    geo = P["geo0"]
    lo = [geo["x0"] - 3, geo["y0"] - 3, geo["lc"] - 3, max(geo["flux"], 1e-30) * 0.05, geo["rhalf"] * 0.3, 0.5,
          max(geo["inc"] - 5, 10), geo["pa"] - 45, 0.3, 0.0, 15.0, 5.0, -3.0, 0.0]
    hi = [geo["x0"] + 3, geo["y0"] + 3, geo["lc"] + 3, max(geo["flux"], 1e-30) * 20, geo["rhalf"] * 3.0, 4.0,
          min(geo["inc"] + 5, 85), geo["pa"] + 45, 1.5, 150.0, 300.0, 25.0, -1.2, 15.0]
    th0 = [geo[k] for k in F.GEO] + [geo["sig0"], float(np.clip(p["virial_velocity"], 16, 299)),
                                     float(np.clip(p["concentration"], 5.5, 24.5)), float(np.clip(p["log_X"], -2.9, -1.3)), 7.5]
    r = fit.fit(np.array(th0), np.array(lo), np.array(hi))
    d = dict(zip(r["names"], r["x"]))
    Re = d["rhalf"] * P["cm"].kpc
    R22 = np.array([2.2 * Re / 1.678])
    vc22 = float(np.sqrt(mass.vc2(R22, Re, d["n"], d["Vvir"], d["c2"], d["X"], d["SigHI"]))[0])
    return dict(vc22=vc22, v22_survey=g["der"]["v22"], inc=d["inc"], inc_survey=p["inclination"], chi2_red=r["chi2_red"])


def run(cutdir, gids, k3_ids, N, P15, phot, third, quick=False):
    done = set()
    if os.path.exists(OUTJ):
        for ln in open(OUTJ):
            d = json.loads(ln)
            done.add((d["gid"], d["fit"]))

    def emit(rec):
        with open(OUTJ, "a") as fh:
            fh.write(json.dumps(rec) + "\n")
        done.add((rec["gid"], rec["fit"]))

    for gid in gids:
        if STOP:
            print("SIGTERM: stopping cleanly")
            sys.exit(75)
        f = os.path.join(cutdir, f"ID{gid:04d}.npz")
        if not os.path.exists(f):
            continue
        cut = dict(np.load(f))
        P = prepare(gid, cut, N, P15, phot)
        base = dict(gid=gid, z=P["z"], third=third.get(gid, -1), logm_sed=P["logm"])
        if gid in k3_ids and (gid, "K3") not in done:
            emit(dict(base, fit="K3", **dc14_fit(P)))
        for foot, af in (C.A_FOOT.items() if not quick else [("canonical", C.A_FOOT["canonical"])]):
            a0 = af * float(N.band_ratio(P["z"]))
            for rd, kw in (READINGS.items() if not quick else [("R0", READINGS["R0"])]):
                key = f"law|{foot}|{rd}"
                if (gid, key) in done:
                    continue
                r, mu = law_fit(P, a0, mu_scale=kw.get("mu", 1.0), drift=kw.get("drift", 1.0), sighi=kw.get("sighi"),
                                dms=kw.get("dms", True))
                rec = dict(base, fit=key, footing=foot, reading=rd, d_fit=float(r["x"][10] - P["logm"]),
                           d_err=float(r["err"][10]), chi2_red=r["chi2_red"], mu=mu, valid=bool(r["status"] > 0))
                emit(rec)
                if rd == "R0" and foot == "canonical" and (gid, "mutate") not in done:
                    rM, _ = law_fit(P, 2 * a0, start=r["x"], lo_ext=0.5)
                    emit(dict(base, fit="mutate", d_fit=float(rM["x"][10] - P["logm"]), d_ref=rec["d_fit"]))
        if quick:
            continue
        for name, a0 in (("paper_law", (1.00 + 1.59 * P["z"]) * 1e-10), ("rival_Hz", C.A_FOOT["canonical"] * float(N.E(P["z"])))):
            key = f"context|{name}"
            if (gid, key) not in done:
                r, mu = law_fit(P, a0)
                emit(dict(base, fit=key, d_fit=float(r["x"][10] - P["logm"]), chi2_red=r["chi2_red"]))
        print(f"ID{gid} done", flush=True)


def selftest(scratch):
    """three synthetic cutouts from the engine, wrapped as Stage 1 would read them; checks the plumbing only."""
    N, P15 = C.Native(), C.planck15()
    phot, _ = C.load_catalogue()
    s = json.load(open(os.path.join(C.HERE, "fn3_sample.json")))
    gids = s["primary"][:3]
    cutdir = os.path.join(scratch, "fn3_stage1_selftest")
    os.makedirs(cutdir, exist_ok=True)
    from fn3_k2 import setup
    for gid in gids:
        g, z, kpc, logm_sed, mu, cm25, geo = setup(gid, N, P15, phot)
        lam0 = (F.L1 + F.L2) / 2 * (1 + z) - 40 * 1.25
        lam = lam0 + 1.25 * np.arange(81)
        cm = F.CubeModel(25, 25, lam, 0.2, kpc, g["psf"]["fwhm"], g["psf"]["beta"])
        a0 = C.A_FOOT["canonical"] * float(N.band_ratio(z))
        fit = F.Fitter(cm, None, np.ones((81, 25, 25)), F.LawMass(mu * 10 ** logm_sed, a0), "law")
        th = [geo[k] for k in F.GEO] + [geo["sig0"], logm_sed, 5.0]
        th[2] = (F.L1 * (1 + z) - lam0) / 1.25
        m = fit.model(np.array(th))
        sig = math.sqrt(float(np.sum(m ** 2))) / 30.0
        rng = np.random.default_rng(99 + gid)
        cont = (1.0 + 0.01 * np.arange(81))[:, None, None] * sig
        np.savez(os.path.join(cutdir, f"ID{gid:04d}.npz"), DATA=(m + cont + rng.normal(0, sig, m.shape)).astype(np.float32),
                 STAT=np.full(m.shape, sig * sig, np.float32), lam0=lam0, dlam=1.25,
                 psf_fwhm=g["psf"]["fwhm"], psf_beta=g["psf"]["beta"])
    global OUTJ
    OUTJ = os.path.join(scratch, "fn3_stage1_selftest.jsonl")
    if os.path.exists(OUTJ):
        os.remove(OUTJ)
    third = {gid: 0 for gid in gids}
    run(cutdir, gids, set(gids[:1]), N, P15, phot, third, quick=True)
    recs = [json.loads(l) for l in open(OUTJ)]
    law = [r for r in recs if r["fit"].startswith("law")]
    ok = len(law) == 3 and all(abs(r["d_fit"]) < 0.6 for r in law) and any(r["fit"] == "K3" for r in recs)
    lines = [f"stage 1 plumbing selftest: {len(recs)} records; law Delta (planted 0): " +
             ", ".join(f"{r['d_fit']:+.3f}" for r in law) + f" -> {'PASS' if ok else 'FAIL'}",
             "kappa = 1/2 FITTED; not theory closed."]
    print("\n".join(lines))
    open(os.path.join(C.HERE, "fn3_stage1_selftest.out"), "w").write("\n".join(lines) + "\n")
    return ok


def main():
    if len(sys.argv) > 2 and sys.argv[1] == "SELFTEST":
        sys.exit(0 if selftest(sys.argv[2]) else 1)
    if len(sys.argv) > 2 and sys.argv[1] == "RUN":
        N, P15 = C.Native(), C.planck15()
        phot, _ = C.load_catalogue()
        s = json.load(open(os.path.join(C.HERE, "fn3_sample.json")))
        third = {gid: int(t) for t, gl in s["thirds"].items() for gid in gl}
        gids = sorted(set(s["primary"]) | set(s["secondary"]))
        run(sys.argv[2], gids, set(s["primary"][:10]), N, P15, phot, third)
        return
    print(__doc__)


if __name__ == "__main__":
    main()
