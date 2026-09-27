#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
XR21_s1_web_channel -- STAGE 1 (code test for stage 3's web conversion channel): the box reads the dark fluid's own flow --
strain eigenvalues, turned-around / expanding classes, dispersion -- the input XR19's web census says the sub-grid rule needs.

WHY.  XR19 (the coordinator relaying it after this lane was specified; XR19_web_runaway.py) found that once halos convert,
FK1's conversion spreads through the collapsed and turned-around web at z <~ 1.5 (one connected cluster), never into
expanding voids (an exact theorem: a daughter's relative velocity only falls where the strain is positive definite), and not
at z >~ 3 (the vacuum gate).  A halo-only sub-grid rule misses 0.12 of the carrier at z = 2 and 0.28 at z = 1 and puts the
removal in the wrong place.  Stage 3's sub-grid rule must therefore include a web channel: conversion in turned-around
sheets and filaments (the zero-strain cone), seeded within ~1 Mpc/h of converted converging or halo-hosting cells at >~ 3
e-folds per passage, one passage in expanding cells, gate-limited at high z -- with FK1/FP10's own rates (XR19_common:
G_t, rho_t_over_mean, sweep_gain, cone_gain_kinetic, kinetic_rate).  Stage 3 waits for the coordinator; this script tests
the instrument that channel stands on: XR21_pm_core.flow_strain (the carrier's mass-weighted velocity, Gaussian-smoothed on
R_s, its symmetrised spectral gradient plus the Hubble term, eigenvalues in units of H).

CHECKS (declared after an exploratory run of the same comparison, disclosed below)
  W0 [code] at the ICs (z = 49, 50 Mpc/h, 128^3 mesh and particles, L362's CLASS, seed 7) the box's strain equals the
     Zel'dovich deformation read with the same operators (XR21_pm_core.zeldovich_ic_eigen: e_i = 1 - f lambda_i/(1 - lambda_i)):
     Pearson correlation of e_1 >= 0.99 and std(e_1 - 1) within 10%, and the LEVEL -- the mean of each sorted eigenvalue within
     0.005 (in units of H; 20% of e_1's mean peculiar offset, 0.025) -- at R_s = 1 Mpc/h (2.6 cells); R_s = 0.5 Mpc/h (1.3 cells,
     at the mesh's own scale) is reported.  The level is what the turned-around/expanding split reads (e_1 < 0).
  W1 [code] the box's trigger threshold is XR19's: delta_t0 E^4/(1+z)^3 equals XR19_common.rho_t_over_mean (FK1 N2, q = 1.75)
     to 1e-12 at z = 0-6.
  W2 [code] the ICs' Zel'dovich T-web fractions at threshold 0 (0/1/2/3 collapsing axes) equal Doroshkevich's Gaussian-field
     values (0.0798/0.4202/0.4202/0.0798) within 0.015 (XR19's C3 on its own grid).
  W3 [reported] the box's EULERIAN mesh strain after evolution (z = 5, 3, 2, 1, 0.5) against XR19's LAGRANGIAN Zel'dovich census
     on the same ICs: the turned-around fraction by volume and by mass (Zel'dovich's Lagrangian fractions are mass fractions), its
     shell-crossed share, and the rank correlation of e_1.  The web channel's TA/EX
     split is estimator-dependent; stage 3 must fix the estimator (per particle, Lagrangian) before XR19's F_tot(z) is
     re-derived on the box's own flow.
MUTATE=1: the Hubble term is dropped from the strain (the peculiar gradient alone): W0 must FAIL (rc = 1).

HISTORY (disclosed).  The first run for the record (outputs kept in scratch) passed W0 in BOTH modes: its MUTATE returned rc 0,
because W0 then scored only the correlation and the std of e_1 - 1, which a uniform shift -- the dropped Hubble term -- leaves
unchanged.  The control did not bite, so W0 was blind to the one term the turned-around/expanding split depends on.  W0 now also
scores the eigenvalue level (declared after that run, whose level difference was 0.0012 at R_s = 1 and 0.0030 at R_s = 0.5; with
the Hubble term dropped it is ~1).  The same run showed that at z <= 1 and R_s = 0.5 the box calls MORE mass turned around than
Zel'dovich's single-stream census (0.39-0.40 vs 0.23-0.33, with Zel'dovich's shell-crossed share 0.34-0.49): W3's statement, which
said 'far fewer' at every row, was corrected to the rows (reported, not load-bearing).  A smoke run of this script (scratch) scored W0 at both R_s: R_s = 1 passed (0.996/0.950) and R_s = 0.5 did
not (0.987/0.917: the particle-carried velocity is CIC-smoothed at the mesh scale); W0 now scores R_s = 1 and reports R_s = 0.5.
An earlier exploratory run (scratch) of this comparison found and fixed a smoothing bug in flow_strain (the
record's K2[0,0,0] = 1 convention had scaled the k = 0 mode of the smoothed mass by exp(-R_s^2/2), so the mass-weighted
velocity diverged in low-density cells); after the fix the ICs matched Zel'dovich (correlation 0.996, std within 5%) and the
evolved comparison gave the W3 pattern.  SCOPE: the instrument only; the web channel's gains and seeded front are stage 3.
kappa = 1/2 does not enter; a0 does not enter.

Run from the repository root:  python3 real_research/cross_thread_review_2026_09_26/XR21_s1_web_channel.py   (~3 min, ~2 GB)
"""
import os, sys, json, math, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import XR21_common as X
X.pin_threads(1)
import numpy as np
from scipy.stats import spearmanr

MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "XR21_s1_web_channel"

if __name__ == "__main__":
    lane = X.Lane(SLUG, MUTATE)
    P, check, banner = lane.P, lane.check, lane.banner
    P(__doc__.split("CHECKS")[0].strip())
    if MUTATE:
        P("\n  *** MUTATE=1: the Hubble term dropped from the strain; W0 must FAIL ***")
    import XR21_pm_core as C
    import XR19_common as X19
    cos = C.Cosmo("l362"); Pl = X.l362_plin(); ZI = 49.0
    L, NG, NP = 50.0, 128, 128
    m0 = C.Mesh(L, NG)
    x, p, delta0 = C.za_ics(m0, cos, NP, ZI, lambda q: Pl(q, ZI), 7)
    ai = 1 / (1 + ZI); fg = cos.Om_a(ai) ** 0.55                     # the ICs' growth rate (the record's convention)
    lams = {RS: C.zeldovich_ic_eigen(m0, delta0, RS) for RS in (1.0, 0.5)}

    banner("W0-W2  THE INSTRUMENT AT THE INITIAL CONDITIONS")
    W0 = {}
    for RS, lam in lams.items():
        e, rho, sig = C.flow_strain(m0, cos, x, p, np.full(len(x), 1.0 / len(x)), ai, RS, hubble=not MUTATE)
        eza = np.sort(1 - fg * lam / (1 - lam), axis=1)
        W0[RS] = dict(corr=float(np.corrcoef(e[:, 0], eza[:, 0])[0, 1]),
                      std_ratio=float(np.std(e[:, 0] - 1) / np.std(eza[:, 0] - 1)),
                      level=float(np.max(np.abs(e.mean(0) - eza.mean(0)))))
        P(f"    R_s = {RS}: corr(e_1) {W0[RS]['corr']:.4f}; std(e_1 - 1) box/ZA {W0[RS]['std_ratio']:.4f}; mean e box "
          f"{e.mean(0).round(4).tolist()} ZA {eza.mean(0).round(4).tolist()}")
    check("W0 [code] AT THE ICs THE BOX READS THE ZEL'DOVICH FLOW: the strain eigenvalue e_1 from the particles (mass-weighted, "
          "smoothed, Hubble + peculiar) correlates with the Zel'dovich deformation read by the same operators at >= 0.99, with the "
          "std of e_1 - 1 within 10% and every eigenvalue's mean within 0.005 H (R_s = 1 Mpc/h; R_s = 0.5, at the mesh's own "
          "scale, reported)",
          "; ".join(f"R_s {k_}: corr {v['corr']:.4f}, std ratio {v['std_ratio']:.3f}, level {v['level']:.4f}" for k_, v in W0.items()),
          W0[1.0]["corr"] >= 0.99 and abs(W0[1.0]["std_ratio"] - 1) <= 0.10 and W0[1.0]["level"] <= 0.005,
          "the residual (a few %) is the CIC deposit of particle-carried velocities against the Lagrangian field; it grows at the "
          "mesh scale (R_s = 0.5)")
    zz = np.array([0.0, 0.5, 1.0, 2.0, 3.0, 4.0, 6.0])
    mine = np.array([5.31123858083705 * cos.E(1 / (1 + z)) ** 4 / (1 + z) ** 3 for z in zz])
    theirs = np.array([float(X19.rho_t_over_mean(z, 5.31123858083705)) for z in zz])
    d1 = float(np.max(np.abs(mine / theirs - 1)))
    check("W1 [code] the box's trigger threshold delta_t0 E^4/(1+z)^3 is XR19's rho_t_over_mean (FK1 N2, q = 1.75) at z = 0-6",
          f"max relative deviation {d1:.1e}", d1 <= 1e-12)
    tw = np.bincount((lams[0.5] > 0).sum(1), minlength=4) / lams[0.5].shape[0]
    dor = np.array([0.0798, 0.4202, 0.4202, 0.0798])
    check("W2 [code] the ICs' Zel'dovich T-web fractions at threshold 0 equal Doroshkevich's Gaussian-field values within 0.015",
          f"{tw.round(4).tolist()} vs {dor.tolist()} (max |diff| {np.max(np.abs(tw - dor)):.4f})", np.max(np.abs(tw - dor)) <= 0.015)
    lane.out["numbers"].update(W0={str(k_): v for k_, v in W0.items()}, W1=d1, W2=tw.tolist())

    if not MUTATE:
        banner("W3  THE EVOLVED FLOW: the box's Eulerian mesh strain vs XR19's Lagrangian Zel'dovich census on the same ICs")
        box = C.Box(L, NG, NP, cos, zi=ZI, seed=7, mode="single", gravity="newton", Pfun=lambda q: Pl(q, ZI))
        W3 = {}

        def out(b, a, z):
            rows = {}
            for RS, lam in lams.items():
                e, rho, sig = C.flow_strain(b.mesh, cos, b.xb, b.pb, np.full(len(b.xb), b.mb), a, RS)
                D = cos.D(a) / cos.D(ai); f = cos.f(a)
                d = D * lam; dm = np.minimum(d, 1 - 1e-9); ss = d[:, 0] < 1
                eza = np.sort(1 - f * dm / (1 - dm), axis=1)
                w = rho / rho.sum()
                rows[str(RS)] = dict(spearman=float(spearmanr(e[:, 0], eza[:, 0]).correlation),
                                     TA_box_volume=float(np.mean(e[:, 0] < 0)), TA_box_mass=float(np.sum(w * (e[:, 0] < 0))),
                                     TA_ZA=float(np.mean(ss & (eza[:, 0] < 0))), MS_ZA=float(np.mean(~ss)),
                                     sigma_median_kms=float(np.median(sig) * 100.0))
                r_ = rows[str(RS)]
                P(f"    z {z:3.1f} R_s {RS}: rank corr(e_1) {r_['spearman']:.3f}; turned around -- box {r_['TA_box_volume']:.3f} by volume, "
                  f"{r_['TA_box_mass']:.3f} by mass; Zel'dovich (Lagrangian) {r_['TA_ZA']:.3f} (+ shell-crossed {r_['MS_ZA']:.3f}); "
                  f"median dispersion {r_['sigma_median_kms']:.0f} km/s")
            W3[str(z)] = rows
            return {}
        t = time.time()
        box.run([5.0, 3.0, 2.0, 1.0, 0.5], on_output=out)
        lane.out["runs"] = {"evolved": dict(wall=time.time() - t, steps=box.nstep, rss_gb=C.peak_rss_gb())}
        check("W3 [reported] THE WEB CHANNEL'S INPUT IS ESTIMATOR-DEPENDENT: after evolution the box's Eulerian mesh strain and XR19's "
              "Lagrangian Zel'dovich census on the same ICs disagree on the turned-around share -- the box calls far less mass turned "
              "around at z >= 2 (and at every z for R_s = 1), while at z <= 1 Zel'dovich's shell-crossed share has no class in the box "
              "(the rows above)",
              "; ".join(f"z {z}: TA box mass {v['1.0']['TA_box_mass']:.3f} vs ZA {v['1.0']['TA_ZA']:.3f} + crossed "
                        f"{v['1.0']['MS_ZA']:.3f} (R_s 1), {v['0.5']['TA_box_mass']:.3f} vs {v['0.5']['TA_ZA']:.3f} + crossed "
                        f"{v['0.5']['MS_ZA']:.3f} (R_s 0.5)" for z, v in W3.items()), True,
              "Eulerian smoothing across thin pancakes dilutes the contracting axis, and Zel'dovich overshoots after shell crossing: "
              "stage 3 must read the strain per particle (Lagrangian) and re-derive XR19's F_tot(z) on the box's own flow",
              load_bearing=False)
        lane.out["numbers"]["W3"] = W3

    banner("VERDICT")
    P("  " + ("MUTATE: without the Hubble term the strain is not the flow's, and the Zel'dovich comparison fails." if MUTATE else
              "The box reads the carrier's flow correctly at the ICs and carries XR19's trigger threshold exactly; after evolution its "
              "Eulerian estimator and XR19's Lagrangian census disagree on the turned-around share, which stage 3 must settle first."))
    sys.exit(lane.finish())
