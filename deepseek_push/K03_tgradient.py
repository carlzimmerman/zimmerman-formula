#!/usr/bin/env python3
"""
K03 -- TEMPERATURE-GRADIENT PROVISOS: EVERY EXACT RELATION UNDER T(r) = 1 + h r^2
================================================================================
2026-09-23.  Continuation of J01/J02 on the JWST_EQUATION_TARGET moment channel.
Robustness/proviso test: the frozen band theorems and the new moment laws were
derived at constant temperature T = 1; the observer sees a temperature
GRADIENT.  Engine: deepseek_push/J02_moment_hierarchy.py::simulate (exact
optical-depth bisection; central or volume source) with collision kicks
drawn at T(r) = 1 + h r^2 (J02.simulate gained an h parameter; h = 0 is
isothermal = original J02 scope).

Theory pinned to the checks (each claim must survive arbitrary h):
  (1) E[D] = tau0(1/2 + q/4)   -- geometric/opacity statement; trajectory
      sampling never consults T (the kick draws happen after the flight
      length and only rescale velocities, not paths) => EXACTLY h-free.
  (2) E[v^2] = 2E[ang], E[D v^2] = 2E[D ang] -- conditional Gaussianity of
      kicks: per-kick Var[e.(u'-u)] = 2 T(r)(1-mu), T only rescales; ang is
      DEFINED as Sum T(r)(1-mu).  Identities hold at every h, including the
      full hierarchy E[D v^{2m}] = (2m-1)!! 2^m E[D ang^m], m = 1..3, and
      E[v^{2m}] = (2m-1)!! 2^m E[ang^m], m = 1,2.
  (3) Atom law: P(no collision) = exp(-tau0(1+q/3)) (central: tau-to-wall
      from the origin is direction-independent) -- atoms never sample T.
  (4) J05 bound E[D^2] >= 3 E[D v^2]^2 / E[v^4] -- hierarchy (2) + Cauchy-
      Schwarz on D vs ang give E[D^2] >= E[D ang]^2/E[ang^2] exactly.
  (5) Kurtosis law: kurt(v|D) = 3 E[ang^2|D]/E[ang|D]^2 in continuous-part
      (N>=1) D-bins -- the per-bin instance of (2) at m = 1,2.
KILL CONDITION / honest finding: any check failing beyond 4 SE under h > 0
means the law is h-dependent => NEW FALSIFIER, reported as such.

Protocol: (tau0,q,h) in {(1,0,1),(1,0,2),(1,3,1),(1,10,1),(2,3,2)}; central
n = 1,000,000 for all five, volume-source n = 800,000 for three configs (>= two
volume).  Every h>0 run is twinned with its h=0 run at the SAME seed: the RNG
stream is h-independent (same uniform/Thomson/isotropic draws; only the kick
*scale* differs), so h-independence of trajectory functionals (E[D], atom
fraction) is testable at machine precision.
"""
import importlib.util
import json
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location(
    "j02_moment_hierarchy", os.path.join(HERE, "J02_moment_hierarchy.py"))
j02 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(j02)
simulate = j02.simulate

N_C = 1_000_000            # central per config (>= 600000)
N_V = 800_000              # volume per config (>= 600000)
CONFIGS = [(1.0, 0.0, 1.0), (1.0, 0.0, 2.0), (1.0, 3.0, 1.0),
           (1.0, 10.0, 1.0), (2.0, 3.0, 2.0)]
VOL_CONFIGS = [(1.0, 0.0, 1.0), (1.0, 3.0, 1.0), (2.0, 3.0, 2.0)]
NBIN_C, NBIN_V = 16, 12
NSE = 4.0                  # kill threshold: failure beyond 4 SE


def se(x):
    return float(np.std(x, ddof=1) / np.sqrt(len(x)))


def int_r_kappa(tau0, q):
    return tau0 * (0.5 + 0.25 * q)


def atom_pred(tau0, q):
    return np.exp(-tau0 * (1.0 + q / 3.0))


def bound_gap_batches(D, v2, v4, nb=12):
    """E[D^2] - 3 E[D v^2]^2 / E[v^4] with a batched SE of the gap."""
    idx = np.array_split(np.arange(len(D)), nb)
    gaps = np.array([np.mean(D[i] * D[i])
                     - 3.0 * np.mean(D[i] * v2[i]) ** 2 / np.mean(v4[i])
                     for i in idx])
    return float(gaps.mean()), float(np.std(gaps, ddof=1) / np.sqrt(nb))


def kurt_bin(v2b, v4b, angb):
    """Per-bin kurt(v|D) vs 3E[ang^2|D]/E[ang|D]^2 with delta-method SEs."""
    Ev2 = float(np.mean(v2b)); Ev4 = float(np.mean(v4b))
    Ea = float(np.mean(angb)); Ea2 = float(np.mean(angb * angb))
    K = Ev4 / Ev2 ** 2
    sK = K * np.hypot(se(v4b) / Ev4, 2 * se(v2b) / Ev2)
    R = 3.0 * Ea2 / Ea ** 2
    sR = R * np.hypot(se(angb * angb) / Ea2, 2 * se(angb) / Ea)
    return K, sK, R, sR


# --------------------------------------------------------------------------
CHECKS = []    # one dict per check: id, cfg, desc, meas, pred, tol, passed
FAILURES = []  # failed checks (id + cfg + numbers)
MEAS = {}      # per-config measurements


def add_check(cid, cfg, desc, meas, pred, tol, passed, note=""):
    ok = bool(passed)
    CHECKS.append(dict(id=cid, cfg=list(cfg), desc=desc, meas=float(meas),
                       pred=float(pred), tol=float(tol), passed=ok, note=note))
    if not ok:
        FAILURES.append(dict(id=cid, cfg=list(cfg), desc=desc,
                             meas=float(meas), pred=float(pred),
                             tol=float(tol)))
    print("%s K03%-3s cfg=%-14s %s\n      meas=% .7g  pred=% .7g  tol=% .7g%s"
          % ("PASS" if ok else "FAIL", cid, str(tuple(cfg)), desc,
             float(meas), float(pred), float(tol),
             ("  | " + note if note else "")))


def run_config(cfg, source, n, seed, bin_n):
    """h>0 run twinned with an h=0 run at the same seed.  Returns the
    measurements dict; also records the bit-exactness of h-independence."""
    tau0, q, h = cfg
    r0 = simulate(n, tau0, q, source, seed, h=0.0)
    rh = simulate(n, tau0, q, source, seed, h=h)
    D = rh["D"]; v2 = rh["v2"]; v4 = rh["v4"]; v6 = rh["v6"]
    ang = rh["ang"]; N = rh["N"]
    res = dict(
        h=h, source=source, n=n,
        E_D=float(np.mean(D)), sD=se(D),
        E_D_h0=float(np.mean(r0["D"])),
        D_same_seed_diff=float(np.abs(np.mean(D) - np.mean(r0["D"]))),
        E_v2=float(np.mean(v2)), st_v2=se(v2),
        E_v2_h0=float(np.mean(r0["v2"])), st_v2_h0=se(r0["v2"]),
        E_ang=float(np.mean(ang)), st_ang=se(ang),
        E_ang2=float(np.mean(ang * ang)), st_ang2=se(ang * ang),
        E_v4=float(np.mean(v4)), st_v4=se(v4),
        E_Dv2=float(np.mean(D * v2)), st_Dv2=se(D * v2),
        E_Dang=float(np.mean(D * ang)), st_Dang=se(D * ang),
        E_Dang2=float(np.mean(D * ang * ang)), st_Dang2=se(D * ang * ang),
        E_Dv4=float(np.mean(D * v4)), st_Dv4=se(D * v4),
        E_Dang3=float(np.mean(D * ang ** 3)), st_Dang3=se(D * ang ** 3),
        E_Dv6=float(np.mean(D * v6)), st_Dv6=se(D * v6),
        E_D2=float(np.mean(D * D)))
    bg, bgse = bound_gap_batches(D, v2, v4)
    res["bound_gap"] = bg
    res["bound_gap_se"] = bgse
    res["atom"] = float(np.mean(N == 0))
    res["atom_h0"] = float(np.mean(r0["N"] == 0))
    res["atom_same_seed_diff"] = float(
        np.abs(np.mean(N == 0) - np.mean(r0["N"] == 0)))
    res["cont_frac"] = float(np.mean(N >= 1))
    # ---- kurtosis law in continuous-part D-bins (N >= 1) ----
    cont = N >= 1
    Dc, v2c, v4c, angc = D[cont], v2[cont], v4[cont], ang[cont]
    qs = np.unique(np.quantile(Dc, np.linspace(0, 1, bin_n + 1)[1:-1]))
    bnd = np.digitize(Dc, qs)
    bins = []
    worst = 0.0
    for b in range(len(qs)):
        m = bnd == b
        if int(m.sum()) < 400:
            continue
        K, sK, R, sR = kurt_bin(v2c[m], v4c[m], angc[m])
        dev = abs(K - R)
        tol = NSE * (sK + sR) + 0.05 * abs(R)
        E2 = float(np.mean(v2c[m])); sE2 = se(v2c[m])
        Ea = float(np.mean(angc[m])); sEa = se(angc[m])
        wb_dev = abs(E2 - 2 * Ea)
        wb_tol = NSE * (sE2 + 2 * sEa) + 0.02 * (2 * Ea)
        bins.append(dict(bin=int(b), n=int(m.sum()), K=float(K), sK=sK,
                         R=float(R), sR=sR, dev=float(dev), tol=float(tol),
                         wb_dev=float(wb_dev / wb_tol)))
        worst = max(worst, dev / tol)
    res["kurt_bins"] = bins
    res["kurt_bins_pass"] = int(sum(1 for k in bins if k["dev"] < k["tol"]))
    res["kurt_worst_ratio"] = float(worst)
    return res


def central_checks(cfg, r):
    """Checks (1)-(5) for a central-source config."""
    tau0, q, h = cfg
    cid = "G1"
    # 1: E[D] = tau0(1/2+q/4) under the gradient
    add_check("G1", cfg, "E[D] == tau0(1/2+q/4) under h>0 (central)",
              r["E_D"], int_r_kappa(tau0, q), NSE * r["sD"] + 1e-9,
              abs(r["E_D"] - int_r_kappa(tau0, q)) < NSE * r["sD"] + 1e-9)
    # 1b: temperature never enters the spatial statement -- bit-exact twin
    add_check("G1b", cfg, "E[D] bit-identical h>0 vs h=0 (same-RNG twin)",
              r["E_D"], r["E_D_h0"], 0.0, r["D_same_seed_diff"] == 0.0,
              "trajectory stream is h-free")
    # 2: exposure identities (m = 1) and Gaussian-lemma (m = 2)
    add_check("G2", cfg, "E[v^2] = 2 E[ang]",
              r["E_v2"], 2 * r["E_ang"], NSE * (r["st_v2"] + 2 * r["st_ang"]),
              abs(r["E_v2"] - 2 * r["E_ang"]) <
              NSE * (r["st_v2"] + 2 * r["st_ang"]) + 1e-9)
    add_check("G3", cfg, "E[D v^2] = 2 E[D ang]",
              r["E_Dv2"], 2 * r["E_Dang"],
              NSE * (r["st_Dv2"] + 2 * r["st_Dang"]),
              abs(r["E_Dv2"] - 2 * r["E_Dang"]) <
              NSE * (r["st_Dv2"] + 2 * r["st_Dang"]) + 1e-9)
    add_check("G3b", cfg, "E[v^4] = 12 E[ang^2] (Gaussian lemma)",
              r["E_v4"], 12 * r["E_ang2"], NSE * (r["st_v4"] + 12 * r["st_ang2"]),
              abs(r["E_v4"] - 12 * r["E_ang2"]) <
              NSE * (r["st_v4"] + 12 * r["st_ang2"]) + 1e-9)
    add_check("G3c", cfg, "E[D v^4] = 12 E[D ang^2] (hierarchy m=2)",
              r["E_Dv4"], 12 * r["E_Dang2"],
              NSE * (r["st_Dv4"] + 12 * r["st_Dang2"]),
              abs(r["E_Dv4"] - 12 * r["E_Dang2"]) <
              NSE * (r["st_Dv4"] + 12 * r["st_Dang2"]) + 1e-9)
    add_check("G3d", cfg, "E[D v^6] = 120 E[D ang^3] (hierarchy m=3)",
              r["E_Dv6"], 120 * r["E_Dang3"],
              NSE * (r["st_Dv6"] + 120 * r["st_Dang3"]),
              abs(r["E_Dv6"] - 120 * r["E_Dang3"]) <
              NSE * (r["st_Dv6"] + 120 * r["st_Dang3"]) + 1e-9)
    # 3: atom law
    add_check("G4", cfg, "atom law A = exp(-tau0(1+q/3)) (never-collided)",
              r["atom"], atom_pred(tau0, q),
              NSE * np.sqrt(r["atom"] * (1 - r["atom"]) / r["n"]) + 1e-6,
              abs(r["atom"] - atom_pred(tau0, q)) <
              NSE * np.sqrt(r["atom"] * (1 - r["atom"]) / r["n"]) + 1e-6)
    add_check("G4b", cfg, "atom fraction bit-identical h>0 vs h=0",
              r["atom"], r["atom_h0"], 0.0, r["atom_same_seed_diff"] == 0.0,
              "atoms never sample T")
    # 4: J05 bound under gradient
    gap, gse = r["bound_gap"], r["bound_gap_se"]
    add_check("G5", cfg, "E[D^2] >= 3 E[Dv^2]^2/E[v^4] (gap>0, >4 SE)",
              gap, 0.0, 4.0 * gse, gap > 4.0 * gse,
              "gap/SE = %.1f" % (gap / gse if gse > 0 else float("inf")))
    # 5: kurtosis law in continuous-part D-bins
    add_check("G6", cfg,
              "kurt(v|D) = 3E[ang^2|D]/E[ang|D]^2 in all %d D-bins"
              % len(r["kurt_bins"]),
              r["kurt_bins_pass"], len(r["kurt_bins"]), 0.0,
              r["kurt_bins_pass"] == len(r["kurt_bins"]) and
              r["kurt_bins_pass"] > 0,
              "worst dev/tol = %.2f" % r["kurt_worst_ratio"])
    # smoke: the gradient is live (E[v2] must rise with h; guards wiring)
    add_check("G7", cfg, "gradient live: E[v^2](h>0) > E[v^2](h=0) (>10 SE)",
              r["E_v2"], r["E_v2_h0"], 10.0 * r["st_v2"],
              (r["E_v2"] - r["E_v2_h0"]) > 10.0 * r["st_v2"],
              "rise = %.3f" % (r["E_v2"] - r["E_v2_h0"]))
    return r


def volume_checks(cfg, r):
    """Volume source: E[D] has no closed form (J02 Theorem B), so the
    in-gradient claims are h-independence + the T-free identities."""
    tau0, q, h = cfg
    add_check("V1", cfg, "volume E[D] bit-identical h>0 vs h=0",
              r["E_D"], r["E_D_h0"], 0.0, r["D_same_seed_diff"] == 0.0,
              "spatial statement h-free for volume too")
    add_check("V2", cfg, "volume E[v^2] = 2 E[ang]",
              r["E_v2"], 2 * r["E_ang"], NSE * (r["st_v2"] + 2 * r["st_ang"]),
              abs(r["E_v2"] - 2 * r["E_ang"]) <
              NSE * (r["st_v2"] + 2 * r["st_ang"]) + 1e-9)
    add_check("V3", cfg, "volume E[D v^2] = 2 E[D ang]",
              r["E_Dv2"], 2 * r["E_Dang"],
              NSE * (r["st_Dv2"] + 2 * r["st_Dang"]),
              abs(r["E_Dv2"] - 2 * r["E_Dang"]) <
              NSE * (r["st_Dv2"] + 2 * r["st_Dang"]) + 1e-9)
    add_check("V3b", cfg, "volume E[v^4] = 12 E[ang^2]",
              r["E_v4"], 12 * r["E_ang2"], NSE * (r["st_v4"] + 12 * r["st_ang2"]),
              abs(r["E_v4"] - 12 * r["E_ang2"]) <
              NSE * (r["st_v4"] + 12 * r["st_ang2"]) + 1e-9)
    add_check("V4", cfg, "volume atom fraction bit-identical h>0 vs h=0",
              r["atom"], r["atom_h0"], 0.0, r["atom_same_seed_diff"] == 0.0,
              "no closed form asserted for volume (J02 Theorem B)")
    gap, gse = r["bound_gap"], r["bound_gap_se"]
    add_check("V5", cfg, "volume J05 bound (gap > 4 SE)",
              gap, 0.0, 4.0 * gse, gap > 4.0 * gse,
              "gap/SE = %.1f" % (gap / gse if gse > 0 else float("inf")))
    add_check("V6", cfg,
              "volume kurt(v|D) law in all %d D-bins" % len(r["kurt_bins"]),
              r["kurt_bins_pass"], len(r["kurt_bins"]), 0.0,
              r["kurt_bins_pass"] == len(r["kurt_bins"]) and
              r["kurt_bins_pass"] > 0,
              "worst dev/tol = %.2f" % r["kurt_worst_ratio"])
    return r


def main():
    t0 = time.time()
    MEAS["protocol"] = dict(engine="deepseek_push/J02_moment_hierarchy.py::simulate",
                            T="1 + h r^2", NSE=NSE,
                            n_central=N_C, n_volume=N_V,
                            central_configs=[list(c) for c in CONFIGS],
                            volume_configs=[list(c) for c in VOL_CONFIGS])

    # ---- central: all five configs ----
    for i, (tau0, q, h) in enumerate(CONFIGS):
        key = "central_%g_%g_%g" % (tau0, q, h)
        r = run_config((tau0, q, h), "central", N_C, seed=1000 + i, bin_n=NBIN_C)
        MEAS[key] = r
        central_checks((tau0, q, h), r)

    # ---- volume: three configs ----
    for i, (tau0, q, h) in enumerate(VOL_CONFIGS):
        key = "volume_%g_%g_%g" % (tau0, q, h)
        r = run_config((tau0, q, h), "volume", N_V, seed=5000 + i, bin_n=NBIN_V)
        MEAS[key] = r
        volume_checks((tau0, q, h), r)

    npass = sum(1 for c in CHECKS if c["passed"])
    ntot = len(CHECKS)
    ok = npass == ntot
    print("\nK03 COMPLETE: %d/%d checks PASS.  %s"
          % (npass, ntot, "ALL PASS" if ok else "FAILURES PRESENT"))
    print("wall time: %.1f s" % (time.time() - t0))

    # ---- results JSON (lane contract) ----
    results = dict(
        checks=[dict(id=c["id"], cfg=c["cfg"], desc=c["desc"], meas=c["meas"],
                     pred=c["pred"], tol=c["tol"], passed=c["passed"],
                     note=c["note"]) for c in CHECKS],
        measurements=MEAS,
        total_checks=ntot, passed=npass, ALL_PASSED=bool(ok),
        failures=FAILURES)
    with open(os.path.join(HERE, "K03_results.json"), "w") as f:
        json.dump(results, f, indent=1)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())