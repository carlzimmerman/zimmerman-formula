#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
XR34_rescore_DE11 -- DE11's forest verdict re-scored with ONLY the MOND kernel's argument corrected.

DE11 AS COMMITTED.  The converged model's MOND-sector switch (x_MS = 1.5 Omega_m(a)[f_b delta + delta_ph], the phantom
lagged one step; threshold 2.5 E(z)^2; smoothTransition width w = 0.25 and 0.02) in L347's PM (128^3 mesh, 96^3
particles, 50 and 25 Mpc/h, CLASS to 40 h/Mpc, seed 7).  F1: worst |P1D/P1D_LCDM - 1| = 0.0041 (L25 alt) against 0.10 ->
PASS.  Its kernel line reads |grad phi|/a^2 = (1+z) g_N,phys (XR34_kernel_argument).

METHOD.  DE11's committed source executed read-only with that ONE line changed to |grad phi|/a (XR34_common).  Runs:
  'fix'  (after):   all eight MOND cells (2 boxes x 2 footings x 2 widths)
  'none' (control): L25_alt_w0.02 and L25_alt_w0.25 (the cells that set DE11's worst) and L50_alt_w0.25
  LCDM:             L50_lcdm and L25_lcdm re-run (DE11's own run(); compared with L347's committed LCDM P1D)
PRE-DECLARED (before any XR34 run; XR34_README 'Hypotheses')
  H-DE11: the pass does NOT flip (worst <= 0.10 after the correction).
CHECKS
  K1 [load-bearing] DE11's own accel() with the corrected line reproduces the analytic single-halo QUMOND profile to 2%
     (z = 3, 2, 0; both footings); the committed line misses it at z = 3, 2 (reported in the same row).
  C1 [load-bearing] the committed line re-run reproduces DE11's committed per-cell deviations (both z) to 1e-9.
  C2 [load-bearing] MOND off: DE11's L50_lcdm and L25_lcdm equal L347's committed LCDM P1D to 1e-12.
  R1 (reported) before / after per cell and z; the gate's reach (A1: active mesh fraction, largest phantom density);
     DE11's F1 rule re-scored.
  H1 (reported) whether H-DE11 held.
MUTATE=1: 'double' stands in for the corrected line in K1 -> K1 FAILS (rc = 1); no PM run.

Run from the repository root (MUTATE=1 first):  python3 real_research/cross_thread_review_2026_09_26/XR34_rescore_DE11.py
"""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import XR34_common as X                                                 # noqa: E402
import numpy as np                                                      # noqa: E402

MUTATE = os.environ.get("MUTATE", "0") == "1"
FIX = "double" if MUTATE else "fix"
LANE = "DE11"
LN = X.Lane("XR34_rescore_DE11", MUTATE)
P = LN.P
CELLS = {f"L{int(L)}_{f}_w{w}": (L, "mond", f, 2.5, w) for L in (50.0, 25.0) for f in ("canonical", "alt") for w in (0.25, 0.02)}
LCDM = {"L50_lcdm": (50.0, "lcdm", "canonical", 0, 0), "L25_lcdm": (25.0, "lcdm", "canonical", 0, 0)}
NONE = ("L25_alt_w0.02", "L25_alt_w0.25", "L50_alt_w0.25")
ZZ = ("3.0", "2.0")

if __name__ == "__main__":
    P(__doc__.split("PRE-DECLARED")[0].strip())
    if MUTATE:
        P("\n  *** MUTATE=1: 'double' stands in for the corrected line; K1 must FAIL; no PM run ***")
    D11 = json.load(open(os.path.join(X.DEN, "DE11_forest_converged_model_results.json")))["numbers"]
    R347 = json.load(open(os.path.join(X.G03, "L347_switch_forest_flux_power_results.json")))["numbers"]["runs"]

    LN.banner("K1  THE ARGUMENT: DE11's own accel() on the analytic single halo")
    sf, sn = X.halo_summary(X.halo_table(LANE, FIX)), X.halo_summary(X.halo_table(LANE, "none"))
    k1 = max(v["ratio"] for v in sf.values())
    for zk in sf:
        P(f"    {zk:13s} y {sf[zk]['y_min']:.3f}-{sf[zk]['y_max']:.3f}: kick/a over nu g_N  '{FIX}' {sf[zk]['ratio_min']:.3f}-"
          f"{sf[zk]['ratio_max']:.3f}   committed {sn[zk]['ratio_min']:.3f}-{sn[zk]['ratio_max']:.3f}")
    LN.out["numbers"]["K1"] = {"fix_or_mutant": sf, "committed": sn}
    LN.check("K1 DE11's accel() with the corrected line reproduces nu_mono(g_N/a0) g_N on the analytic halo (2%, z = 3, 2, 0, "
             "both footings)", f"'{FIX}': max |ratio - 1| = {k1:.4f}; committed line: z = 3 {max(sn['z3/canonical']['ratio'], sn['z3/alt']['ratio']):.3f}, "
             f"z = 2 {max(sn['z2/canonical']['ratio'], sn['z2/alt']['ratio']):.3f}, z = 0 {max(sn['z0/canonical']['ratio'], sn['z0/alt']['ratio']):.3f}",
             k1 <= 0.02, "the 'after' runs below use the physical argument")
    if MUTATE:
        sys.exit(LN.finish())

    LN.banner("THE RUNS (DE11's run(), one line patched; wall time and peak memory per run)")
    jobs = ([(LANE, "fix", (k,) + CELLS[k]) for k in ("L25_alt_w0.02", "L25_alt_w0.25", "L25_canonical_w0.02", "L25_canonical_w0.25",
                                                      "L50_alt_w0.02", "L50_alt_w0.25", "L50_canonical_w0.02", "L50_canonical_w0.25")]
            + [(LANE, "none", (k,) + v) for k, v in LCDM.items()] + [(LANE, "none", (k,) + CELLS[k]) for k in NONE])
    res = X.run_jobs(jobs, log=P)
    runs = {f"{p_}/{n_}": r["out"] for (l_, p_, n_), r in res.items()}
    LN.out["numbers"]["runs"] = runs
    LN.out["numbers"]["run_times"] = {f"{p_}/{n_}": dict(wall_s=round(r["wall_s"]), peak_rss_gb=round(r["peak_rss_gb"], 2))
                                      for (l_, p_, n_), r in res.items()}
    ref = {"L50": runs["none/L50_lcdm"], "L25": runs["none/L25_lcdm"]}

    LN.banner("C1 C2  CONTROLS: the committed line reproduces DE11; MOND off reproduces the LCDM box")
    before = D11["F1"]["cells"]
    c1 = 0.0
    for k in NONE:
        for z in ZZ:
            v = X.worst_p1d(runs[f"none/{k}"], ref[k.split("_")[0]], zs=(z,))
            d = abs(v - before[f"{k}/z{z}"]); c1 = max(c1, d)
            P(f"    {k:15s} z = {z}: committed {before[f'{k}/z{z}']:.12f}   re-run (committed line) {v:.12f}   |diff| {d:.1e}")
    LN.check("C1 the committed line re-run reproduces DE11's committed per-cell deviations (three cells, both z; 1e-9)",
             f"max |diff| = {c1:.1e}", c1 <= 1e-9, "the harness is DE11 exactly; only the kernel line differs in 'fix'")
    c2 = max(X.max_abs_diff_p1d(runs[f"none/{t}_lcdm"], R347[f"{t}_lcdm"]) for t in ("L50", "L25"))
    LN.check("C2 MOND off: DE11's L50_lcdm and L25_lcdm re-runs equal L347's committed LCDM P1D (1e-12)", f"max |P1D ratio - 1| = {c2:.1e}",
             c2 <= 1e-12)

    LN.banner("R1  BEFORE / AFTER: worst |P1D/P1D_LCDM - 1| over k_par 0.2-2 h/Mpc, per z (DE11's statistic)")
    after = {f"{k}/z{z}": X.worst_p1d(runs[f"fix/{k}"], ref[k.split("_")[0]], zs=(z,)) for k in CELLS for z in ZZ}
    A1b = D11["A1"]
    P(f"    {'cell':22s} {'before':>9s} {'after':>9s} {'x':>6s}    active z=2 before -> after   largest phantom density z=2 before -> after")
    for k in CELLS:
        for z in ZZ:
            kk = f"{k}/z{z}"
            extra = ""
            if z == "2.0":
                extra = (f"    {A1b[k]['2.0']['active']:.2e} -> {runs['fix/' + k]['2.0']['active']:.2e}     "
                         f"{A1b[k]['2.0']['dph_max']:.0f} -> {runs['fix/' + k]['2.0']['dph_max']:.0f} rho_bar_m")
            P(f"    {kk:22s} {before[kk]:9.4f} {after[kk]:9.4f} {after[kk] / max(before[kk], 1e-30):6.2f}{extra}")
    wb, wa = max(before.values()), max(after.values())
    ok_after = wa <= 0.10
    LN.out["numbers"]["R1"] = dict(before=before, after=after, worst_before=wb, worst_after=wa,
                                   F1_before="PASS" if wb <= 0.10 else "FAIL", F1_after="PASS" if ok_after else "FAIL",
                                   A1_after={k: {z: {q: runs["fix/" + k][z][q] for q in ("active", "f_mean", "dph_max")} for z in ZZ}
                                             for k in CELLS})
    LN.check("R1 (reported) DE11's F1 rule (worst <= 0.10, both boxes, footings, widths) with the corrected argument",
             f"before {wb:.4f} ({'PASS' if wb <= 0.10 else 'FAIL'}) -> after {wa:.4f} ({'PASS' if ok_after else 'FAIL'})", True,
             load_bearing=False)
    LN.check("H1 (reported) the pre-declared hypothesis H-DE11: the pass does not flip", f"verdict {'PASS' if ok_after else 'FAIL'} after "
             f"(worst {wa:.4f})", ok_after, "a failed hypothesis is kept as run", load_bearing=False)

    LN.banner("VERDICT")
    P(f"""  With ONLY the kernel argument corrected, DE11's worst forest deviation goes {wb:.4f} -> {wa:.4f} (x{wa / wb:.1f}) against
  0.10: the verdict {'does NOT flip (PASS)' if ok_after else 'FLIPS to FAIL'}.  Controls: the committed line reproduces DE11 to {c1:.0e} (C1);
  MOND off reproduces L347's LCDM boxes to {c2:.0e} (C2).  DE11's own limits stand (FGPA, one phase per box, all-matter kernel).""")
    sys.exit(LN.finish())
