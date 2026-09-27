#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
XR21_s1_lcdm_controls -- STAGE 1, TESTS 1 AND 2 (code tests): in the no-MOND, no-conversion limit the XR21 particle-mesh box
(XR21_pm_core) reproduces committed LCDM particle-mesh numbers of the record, and its forest and lensing estimators return
their committed LCDM values.  Also: the run time and memory of each box (for the production plan).

WHY.  Stage 1 of lane XR21 builds a PM box for the derivation chain's current model (FP7's AQUAL-type root + FP9's separator
H_Y in the QUMOND-type approximation; FK1's dark fluid with its own density trigger).  Before any model number is read, the
box must be the record's box when the model is switched off -- the same ICs, integrator, force, estimators -- with the new
code paths (two species, the H_Y operator, the conversion hooks) exercised in their OFF limit, not bypassed.

RUNS (every run is the record's configuration; the committed numbers are read from the record's JSON)
  R1  L362's control box: 50 Mpc/h, 128^3 mesh, 96^3 particles, Zel'dovich ICs at z = 49 from L362's CLASS (seed 7), the
      record's KDK in ln a (dlna = 0.02), one species, Newtonian.  -> flux P1D at z = 3 and 2 (L362's FGPA estimator).
  R2  R1's box with TWO species (baryons f_b + the dark fluid, co-located at t_i, L366's layout), the H_Y operator ON in the
      chain reading with the yield at infinity (every step runs the band-pass, the kernel, the divergence and the Poisson
      solve, and returns an exactly zero phantom), and FK1's conversion hook ON with an infinite threshold.  The forest is
      read from the baryon particles (L366's convention).
  R3  L346's box (L176's machinery: the same geometry, L346's own CLASS settings, P_k_max = 20, clip at 20 h/Mpc), one
      species, the H_Y operator ON in FP9's reading with the yield at infinity.  -> L346's matter-power estimator at z = 6, 3, 2,
      and the lensing estimator P(delta_m + delta_ph) through the phantom path.
  R4  L366's box (the one L388's control C1 reproduces): 100 Mpc/h, 256^3 mesh, 2 x 192^3 particles (baryons + carrier,
      co-located), L362's CLASS, seed 7, Newtonian.  -> sigma_8 at z = 0 (L366's estimator), the flux P1D at z = 3 and 2
      (L366's committed LCDM values), the carrier's mass fraction above FK1's nominal threshold on the z = 2 mesh (XR12 A2's
      committed seed-7 number), and the record's cosmic-shear bins at z = 0.5 (L367's estimator; reported).
  R5  (reported) timing probes of the H_Y chain-reading force at production sizes (1 thread; 4 threads for the FFTs and the
      particle chunks), and every run's wall time, step count and peak memory.

PRE-DECLARED (tolerances fixed before the first full run of this script; an exploratory run of R1 and R2's geometry through
the same core, uncommitted, gave 8e-15 -- the tolerances below were then set from floating-point reasoning, not tuned)
  A1  R1's P1D (z = 3, 2; every k_par) equals L362's committed ctrl_lcdm P1D to 1e-10 (relative).
  A2  R2's P1D equals the same committed P1D to 1e-10: the two-species layout, the H_Y path at infinite yield and the idle
      conversion hook change nothing; R2's phantom is identically zero and nothing converts.
  A3  R3's matter power (L346's 14 log bins, z = 6, 3, 2) equals L346's committed LCDM power to 1e-10 (relative), and R3's
      lensing power equals its matter power exactly (the phantom path returns zero at infinite yield).
  A4  R4's sigma_8(z = 0) equals L366's committed 1.0208791238487946 to 1e-8 (relative) and its P1D (z = 3, 2) L366's
      committed LCDM P1D to 1e-8 (a 16x larger, 2 x 7.1M-particle box: chaotic growth of rounding is allowed for).
  A5  R4's z = 2 carrier mass fraction above FK1's nominal threshold (delta_t0 = 5.31123858083705, XR12's E(z)) equals XR12 A2's
      committed seed-7 value 0.12804115362645455 to 1e-6 (the field rounded to float32 as XR12 read it).
  A6  (reported) R4's pk_bins at z = 0.5 (the cosmic-shear estimator's LCDM reference for stage 2); R5's timings.
MUTATE=1: R1-R3 are re-run with the MODEL switched on (the H_Y operator at FP9's headline yield in place of the off limit; R1
becomes an H_Y box in FP9's reading): A1-A3 must FAIL (rc = 1).  R4 and the probes are not run under MUTATE (A4/A5 are
reported as 'not run').

SCOPE.  Code tests only.  kappa = 1/2 is FITTED (Z = 5.7888); it enters nothing here (a0 is inert in the off limit).  No
model number is claimed.  Scratch: XR21_SCRATCH (default: the system temp directory) -- nothing large is written.

Run from the repository root:  python3 real_research/cross_thread_review_2026_09_26/XR21_s1_lcdm_controls.py
(~15 min on 4 threads, peak ~6 GB; MUTATE=1 ~3 min)
"""
import os, sys, json, math, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import XR21_common as X
X.pin_threads(1)
import numpy as np
from multiprocessing import get_context

MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "XR21_s1_lcdm_controls"
INF_YIELD = 1e300
THREADS = int(os.environ.get("XR21_THREADS", "4"))


def worker(cfg):
    X.pin_threads(1)
    import XR21_pm_core as C
    name = cfg["name"]
    cos = C.Cosmo("l362")
    Pfun = (lambda q: X.l346_plin()(q, 49.0)) if cfg["ics"] == "l346" else (lambda q: X.l362_plin()(q, 49.0))
    hy = None
    if cfg["gravity"] == "hy":
        hy = C.HY(cos, **C.fp9_headline())
        if cfg.get("yield_inf"):
            hy.y_Lambda = INF_YIELD                              # y_th = oo: the phantom path runs and returns exactly zero
    conv = dict(delta_t0=float("inf"), Gamma0=50.0, picture="cap", vk=600.0) if cfg.get("conv_idle") else None
    box = C.Box(cfg["L"], cfg["NG"], cfg["NP"], cos, zi=49.0, seed=7, mode=cfg["mode"], gravity=cfg["gravity"],
                reading=cfg.get("reading", "chain"), hy=hy, Pfun=Pfun, workers=cfg.get("workers", 1),
                kmax_clip=cfg.get("clip", 60.0), conversion=conv)
    phmax = [0.0]

    def on_step(b, a):
        if b.gravity == "hy" and cfg.get("track_phantom"):
            _, dph = b.lensing_delta(a)
            phmax[0] = max(phmax[0], float(np.max(np.abs(dph))))

    def out(b, a, z):
        rec = {"a": a}
        if "p1d" in cfg["outs"] and z in (3.0, 2.0):
            kp, p1 = C.flux_p1d(b.mesh, b.c, b.xb, b.pb, a, z)
            rec.update(kpar=kp.tolist(), p1d=p1.tolist())
        if "pk346" in cfg["outs"]:
            dm, dph = b.lensing_delta(a)
            rec["pk"] = b.mesh.pk_log(dm)
            rec["pk_lens"] = b.mesh.pk_log(dm + dph)
            rec["dph_max"] = float(np.max(np.abs(dph)))
        if "s8" in cfg["outs"] and z == 0.0:
            rb, rd = b.densities(); b.cb = b.cd = None
            rec["sigma8"] = b.mesh.sigma8(rb + rd - 1.0)
        if "pkbins" in cfg["outs"] and z == 0.5:
            rb, rd = b.densities(); b.cb = b.cd = None
            rec["pk_bins"] = b.mesh.pk_bins(rb + rd - 1.0, (0.1, 0.2, 0.3, 0.5, 0.7, 1.0))
        if "thr" in cfg["outs"] and z == 2.0:
            NGm = b.mesh.NG; n = len(b.xd)
            rhoc = (b.mesh.deposit(b.xd, np.full(n, 1.0)) * NGm ** 3 / n).astype(np.float32).astype(np.float64)
            OMx = 0.3138; E = lambda zz: math.sqrt(OMx * (1 + zz) ** 3 + 1 - OMx)         # XR12's E(z)
            thr = 5.31123858083705 * E(2.0) ** 4 / 3.0 ** 3
            rec["thr"] = dict(threshold=thr, mass_frac=float(rhoc[rhoc > thr].sum() / rhoc.sum()))
        return rec
    t = time.time()
    res = box.run(cfg["zouts"], dlna=0.02, on_output=out, on_step=on_step)
    info = dict(wall=time.time() - t, steps=box.nstep, rss_gb=C.peak_rss_gb(), n_particles=len(box.xb) + len(box.xd),
                converted_events=box.log["events"], phantom_max=phmax[0], L=cfg["L"], NG=cfg["NG"], NP=cfg["NP"],
                mode=cfg["mode"], gravity=cfg["gravity"])
    return name, dict(out=res, info=info)


def probe(cfg):
    """timing of the H_Y chain-reading force at a given size (the scale factor is set to 0.5 so the operator works)."""
    X.pin_threads(cfg["workers"])
    import XR21_pm_core as C
    cos = C.Cosmo("l362"); hy = C.HY(cos, **C.fp9_headline())
    t = time.time()
    box = C.Box(cfg["L"], cfg["NG"], cfg["NP"], cos, zi=49.0, seed=7, mode="two", gravity=cfg["gravity"], reading="chain",
                hy=hy, Pfun=lambda q: X.l362_plin()(q, 49.0), workers=cfg["workers"], threads=cfg.get("threads", 1))
    t_ic = time.time() - t
    box.a = 0.5
    box.forces(box.a)
    ts = []
    for _ in range(3):
        t = time.time(); box.forces(box.a); ts.append(time.time() - t)
    return cfg["name"], dict(t_ic=t_ic, t_force=float(np.median(ts)), rss_gb=C.peak_rss_gb(), **cfg)


if __name__ == "__main__":
    lane = X.Lane(SLUG, MUTATE)
    P = lane.P
    P(__doc__.split("PRE-DECLARED")[0].strip())
    if MUTATE:
        P("\n  *** MUTATE=1: R1-R3 run with the H_Y operator ON at FP9's headline yield; A1-A3 must FAIL ***")
    small = [
        dict(name="R1", L=50.0, NG=128, NP=96, mode="single", gravity="newton", ics="l362", outs=("p1d",), zouts=[3.0, 2.0]),
        dict(name="R2", L=50.0, NG=128, NP=96, mode="two", gravity="hy", reading="chain", yield_inf=True, conv_idle=True,
             track_phantom=True, ics="l362", outs=("p1d",), zouts=[3.0, 2.0]),
        dict(name="R3", L=50.0, NG=128, NP=96, mode="single", gravity="hy", reading="fp9", yield_inf=True, ics="l346", clip=20.0,
             outs=("pk346",), zouts=[6.0, 3.0, 2.0]),
    ]
    if MUTATE:
        small[0].update(gravity="hy", reading="fp9", yield_inf=False)
        small[1].update(yield_inf=False)
        small[2].update(yield_inf=False)
    big = dict(name="R4", L=100.0, NG=256, NP=192, mode="two", gravity="newton", ics="l362", workers=THREADS,
               outs=("p1d", "s8", "pkbins", "thr"), zouts=[3.0, 2.0, 0.5, 0.0])
    ctx = get_context("spawn")
    with ctx.Pool(min(3, THREADS)) as pool:
        RES = dict(pool.map(worker, small, chunksize=1))
    P(f"\n  small runs done {lane.el()}: " + "; ".join(f"{k}: {v['info']['wall']:.0f} s, {v['info']['steps']} steps, "
                                                      f"{v['info']['rss_gb']:.2f} GB" for k, v in RES.items()))
    if not MUTATE:
        with ctx.Pool(1) as pool:
            RES.update(dict(pool.map(worker, [big])))
        P(f"  R4 done {lane.el()}: {RES['R4']['info']['wall']:.0f} s, {RES['R4']['info']['steps']} steps, "
          f"{RES['R4']['info']['rss_gb']:.2f} GB peak, {RES['R4']['info']['n_particles']} particles")
    lane.out["runs"] = {k: v["info"] for k, v in RES.items()}

    # ------------------------------------------------------------------------------------------------ committed numbers
    L362 = json.load(open(os.path.join(X.G03, "L362_forest_pincer_convergence_results.json")))["numbers"]["runs"]["ctrl_lcdm"]
    L346 = json.load(open(os.path.join(X.G03, "L346_switch_forest_gate_results.json")))["numbers"]["runs"]["lcdm"]["pk"]
    L366 = json.load(open(os.path.join(X.DSEC, "L366_triggered_carrier_cluster_retention_results.json")))["numbers"]["runs"]["lcdm"]
    XR12 = json.load(open(os.path.join(HERE, "XR12_filament_trigger_results.json")))["numbers"]["A2"]["per_box"]["7"]["FK1 5.31"]

    def p1d_dev(run, ref):
        d = 0.0
        for z in ("3.0", "2.0"):
            a = np.array(RES[run]["out"][z]["p1d"]); b = np.array(ref[z]["p1d"])
            ka = np.array(RES[run]["out"][z]["kpar"]); kb = np.array(ref[z]["kpar"])
            assert np.allclose(ka, kb, rtol=1e-12)
            d = max(d, float(np.max(np.abs(a / b - 1))))
        return d

    lane.banner("A1-A3  THE OFF LIMIT REPRODUCES THE RECORD'S LCDM BOXES (50 Mpc/h, 128^3 mesh, 96^3 particles)")
    d1 = p1d_dev("R1", L362)
    lane.check("A1 R1 (one species, Newtonian) reproduces L362's committed control LCDM flux P1D (z = 3, 2; all k_par) to 1e-10",
               f"max relative deviation {d1:.1e}", d1 <= 1e-10,
               "the record's ICs, integrator, CIC and FGPA estimator are reproduced (bincount deposits, real FFTs)")
    d2 = p1d_dev("R2", L362)
    i2 = RES["R2"]["info"]
    lane.check("A2 R2 (two species; the H_Y operator run every step at infinite yield; the conversion hook idle) reproduces the "
               "same committed P1D to 1e-10, with an identically zero phantom and no conversion",
               f"max relative deviation {d2:.1e}; max |delta_ph| over all steps {i2['phantom_max']:.1e}; conversion events "
               f"{i2['converted_events']}", d2 <= 1e-10 and i2["phantom_max"] == 0.0 and i2["converted_events"] == 0)
    d3 = 0.0; dl3 = 0.0; ph3 = 0.0
    for z in ("6.0", "3.0", "2.0"):
        mine = np.array([r[1] for r in RES["R3"]["out"][z]["pk"]]); ref = np.array([r[1] for r in L346[z]])
        lens = np.array([r[1] for r in RES["R3"]["out"][z]["pk_lens"]])
        ok = np.isfinite(ref)
        d3 = max(d3, float(np.max(np.abs(mine[ok] / ref[ok] - 1))))
        dl3 = max(dl3, float(np.max(np.abs(lens[ok] / mine[ok] - 1))))
        ph3 = max(ph3, RES["R3"]["out"][z]["dph_max"])
    lane.check("A3 R3 (L346's CLASS settings; the H_Y path in FP9's reading at infinite yield) reproduces L346's committed LCDM "
               "matter power (14 log bins, z = 6, 3, 2) to 1e-10, and the lensing estimator returns the matter power exactly",
               f"max relative deviation {d3:.1e}; lensing / matter - 1: {dl3:.1e}; max |delta_ph| {ph3:.1e}",
               d3 <= 1e-10 and dl3 == 0.0 and ph3 == 0.0)
    lane.out["numbers"]["A1_A3"] = dict(A1=d1, A2=d2, A2_phantom_max=i2["phantom_max"], A3=d3, A3_lens=dl3)

    lane.banner("A4-A6  L366'S BOX (100 Mpc/h, 256^3 mesh, 2 x 192^3 particles): sigma_8, the forest, the trigger's input")
    if MUTATE:
        lane.check("A4 R4 reproduces L366's committed sigma_8 and P1D", "not run under MUTATE", True, load_bearing=False)
        lane.check("A5 R4's z = 2 threshold statistic reproduces XR12 A2", "not run under MUTATE", True, load_bearing=False)
    else:
        r4 = RES["R4"]["out"]
        s8 = r4["0.0"]["sigma8"]; ds8 = abs(s8 / L366["0.0"]["sigma8"] - 1)
        dp4 = p1d_dev("R4", L366)
        lane.check("A4 R4 reproduces L366's committed LCDM sigma_8(z = 0) = 1.0208791238487946 and its LCDM P1D (z = 3, 2) to 1e-8",
                   f"sigma_8 {s8:.16f} (relative deviation {ds8:.1e}); P1D max relative deviation {dp4:.1e}",
                   ds8 <= 1e-8 and dp4 <= 1e-8,
                   "the two-species production layout at the record's production size (L366 = L388 C1's box)")
        th = r4["2.0"]["thr"]; d5 = abs(th["mass_frac"] / XR12["mass_frac"] - 1)
        lane.check("A5 the mesh trigger's input on R4's z = 2 carrier mesh -- the mass fraction above FK1's nominal threshold -- "
                   "reproduces XR12 A2's committed seed-7 value to 1e-6",
                   f"{th['mass_frac']:.12f} vs {XR12['mass_frac']:.12f} (threshold {th['threshold']:.9f} vs "
                   f"{XR12['threshold']:.9f}); relative deviation {d5:.1e}", d5 <= 1e-6)
        pkb = r4["0.5"]["pk_bins"]
        P("    R4 pk_bins at z = 0.5 (L367's estimator, unnormalised |FFT|^2): " + ", ".join(f"{q}: {v:.6e}" for q, v in pkb.items()))
        lane.out["numbers"]["A4_A6"] = dict(sigma8=s8, dev_sigma8=ds8, dev_p1d=dp4, thr=th, dev_thr=d5, pk_bins_z05=pkb)
        lane.check("A6 (reported) R4's cosmic-shear bins at z = 0.5 are recorded as stage 2's LCDM reference (L367 stored only "
                   "ratios, so there is no committed absolute value to compare)", "see the numbers block", True, load_bearing=False)

    lane.banner("R5  RUN TIME AND MEMORY (every run above; H_Y chain-force probes at production sizes)")
    for k, v in RES.items():
        i = v["info"]
        P(f"    {k}: L = {i['L']:.0f} Mpc/h, mesh {i['NG']}^3, {i['n_particles']} particles ({i['mode']}, {i['gravity']}): "
          f"{i['wall']:.0f} s for {i['steps']} steps = {i['wall'] / max(i['steps'], 1):.2f} s/step, peak {i['rss_gb']:.2f} GB")
    if not MUTATE:
        probes = [dict(name="hy_256_192x2_1thread", L=100.0, NG=256, NP=192, gravity="hy", workers=1, threads=1),
                  dict(name="hy_256_192x2_4threads", L=100.0, NG=256, NP=192, gravity="hy", workers=THREADS, threads=THREADS),
                  dict(name="newton_256_192x2_4threads", L=100.0, NG=256, NP=192, gravity="newton", workers=THREADS, threads=THREADS),
                  dict(name="hy_384_192x2_4threads", L=150.0, NG=384, NP=192, gravity="hy", workers=THREADS, threads=THREADS),
                  dict(name="hy_384_256x2_4threads", L=200.0, NG=384, NP=256, gravity="hy", workers=THREADS, threads=THREADS)]
        PR = {}
        for pc in probes:                                     # one at a time (memory)
            with ctx.Pool(1) as pool:
                PR.update(dict(pool.map(probe, [pc])))
            v = PR[pc["name"]]
            P(f"    probe {pc['name']}: ICs {v['t_ic']:.1f} s; one force evaluation {v['t_force']:.2f} s; peak {v['rss_gb']:.2f} GB")
        lane.out["numbers"]["probes"] = PR
        lane.check("A7 (reported) run time and memory per box size", "see the R5 block and numbers.probes", True, load_bearing=False)

    lane.banner("VERDICT")
    P("  " + ("MUTATE: the model switched on breaks the reproduction, as it must." if MUTATE else
              "In the off limit the XR21 box is the record's LCDM box: the forest estimator (L362, L366), the matter-power and "
              "lensing estimators (L346) and sigma_8 (L366/L388) are reproduced, with the H_Y path and the conversion hook "
              "exercised in their off state."))
    sys.exit(lane.finish())
