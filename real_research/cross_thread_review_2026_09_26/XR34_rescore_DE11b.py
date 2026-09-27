#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
XR34_rescore_DE11b -- DE11b's forest verdict re-scored with ONLY the MOND kernel's argument corrected.

DE11b AS COMMITTED.  The converged model's MOND-sector switch (vacuum-gated, p = 1, x_c0 = 2.5, w = 0.25, the phantom
lagged one step inside the switch variable) at 25 Mpc/h: ctrl (128^3 mesh, 96^3 particles), B (128^3, 128^3), C (256^3,
192^3).  Scorecard row: worst |P1D/P1D_LCDM - 1| = 0.0046 (B alt 0.00464, C alt 0.00457) against L347's 0.10 -> PASS,
converged (+10-13% per refinement).  Its kernel line reads |grad phi|/a^2 = (1+z) g_N,phys (XR34_kernel_argument).

METHOD.  DE11b's committed source is executed read-only with that ONE line changed to |grad phi|/a (XR34_common checks
that exactly one line differs).  Everything else is DE11b's: L362's machinery, the ICs (seed 7, CLASS to 60 h/Mpc), the
switch and its lagged phantom, the FGPA estimator, the score (k_par 0.2-2 h/Mpc, z = 3 and 2).  Runs (one thread each,
<= 3 at a time, <= 1 on the 256^3 mesh):
  'fix'  (after):   C_alt, B_alt, B_canonical, ctrl_canonical, ctrl_alt  -- DE11b's five MOND cells, both footings
  'none' (control): the same five cells with the committed line
  LCDM:             B_lcdm and ctrl_lcdm re-run; C's LCDM is L362's committed C_lcdm P1D (the same code path: C2 shows
                    DE11b's LCDM run equals L362's committed one exactly at B, and C1's C_alt reproduction uses it)
PRE-DECLARED (before any XR34 run; XR34_README 'Hypotheses')
  H-DE11b: the pass does NOT flip: every corrected cell stays <= 0.10 (expected growth x1.5-5).
CHECKS
  K1 [load-bearing] the argument the 'after' runs use is the physical one: DE11b's own accel() with the corrected line
     reproduces the analytic single-halo QUMOND profile to 2% (z = 3, 2, 0; both footings); the committed line misses it
     at z = 3, 2 (reported in the same row).
  C1 [load-bearing] the committed line re-run reproduces DE11b's committed worst deviation in all five cells to 1e-9.
  C2 [load-bearing] MOND off: the B_lcdm re-run equals L362's committed B_lcdm P1D to 1e-12 (ctrl_lcdm has no committed
     P1D; it is compared with L347's L25_lcdm, whose CLASS table stops at 40 h/Mpc -- reported).
  R1 (reported) before / after per cell, the active mesh fraction, DE11b's F1 rule re-scored, its G1 growth ratios.
  H1 (reported) whether H-DE11b held.
MUTATE=1: the correction applied twice ('double') stands in for the corrected line in K1 -> K1 FAILS (rc = 1).  No PM run
is made under MUTATE: K1 is what certifies the argument, and a mis-argued PM run has no other internal check to fail.

Run from the repository root (MUTATE=1 first):  python3 real_research/cross_thread_review_2026_09_26/XR34_rescore_DE11b.py
"""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import XR34_common as X                                                 # noqa: E402
import numpy as np                                                      # noqa: E402

MUTATE = os.environ.get("MUTATE", "0") == "1"
FIX = "double" if MUTATE else "fix"
LANE = "DE11b"
LN = X.Lane("XR34_rescore_DE11b", MUTATE)
P = LN.P
CELLS = {"C_alt": (25.0, 256, 192, "mond", "alt", 0.25), "B_alt": (25.0, 128, 128, "mond", "alt", 0.25),
         "B_canonical": (25.0, 128, 128, "mond", "canonical", 0.25),
         "ctrl_canonical": (25.0, 128, 96, "mond", "canonical", 0.25), "ctrl_alt": (25.0, 128, 96, "mond", "alt", 0.25)}
LCDM = {"B_lcdm": (25.0, 128, 128, "lcdm", "canonical", 0.25), "ctrl_lcdm": (25.0, 128, 96, "lcdm", "canonical", 0.25)}
TESTED = ("C_alt", "B_alt", "B_canonical")                              # DE11b's F1 set (ctrl is its control)

if __name__ == "__main__":
    P(__doc__.split("PRE-DECLARED")[0].strip())
    if MUTATE:
        P("\n  *** MUTATE=1: 'double' stands in for the corrected line; K1 must FAIL; no PM run ***")
    D11b = json.load(open(os.path.join(X.DEN, "DE11b_forest_convergence_results.json")))["numbers"]
    R362 = json.load(open(os.path.join(X.G03, "L362_forest_pincer_convergence_results.json")))["numbers"]["runs"]
    R347 = json.load(open(os.path.join(X.G03, "L347_switch_forest_flux_power_results.json")))["numbers"]["runs"]

    LN.banner("K1  THE ARGUMENT: DE11b's own accel() on the analytic single halo")
    tf, tn = X.halo_table(LANE, FIX), X.halo_table(LANE, "none")
    sf, sn = X.halo_summary(tf), X.halo_summary(tn)
    k1 = max(v["ratio"] for v in sf.values())
    for zk in sf:
        P(f"    {zk:13s} y {sf[zk]['y_min']:.3f}-{sf[zk]['y_max']:.3f}: kick/a over nu g_N  '{FIX}' {sf[zk]['ratio_min']:.3f}-"
          f"{sf[zk]['ratio_max']:.3f}   committed {sn[zk]['ratio_min']:.3f}-{sn[zk]['ratio_max']:.3f}")
    LN.out["numbers"]["K1"] = {"fix_or_mutant": sf, "committed": sn}
    LN.check(f"K1 DE11b's accel() with the corrected line reproduces nu_mono(g_N/a0) g_N on the analytic halo (2%, z = 3, 2, 0, "
             "both footings)", f"'{FIX}': max |ratio - 1| = {k1:.4f}; committed line: z = 3 {max(sn['z3/canonical']['ratio'], sn['z3/alt']['ratio']):.3f}, "
             f"z = 2 {max(sn['z2/canonical']['ratio'], sn['z2/alt']['ratio']):.3f}, z = 0 {max(sn['z0/canonical']['ratio'], sn['z0/alt']['ratio']):.3f}",
             k1 <= 0.02, "the 'after' runs below use the physical argument")
    if MUTATE:
        sys.exit(LN.finish())

    LN.banner("THE RUNS (DE11b's run(), one line patched; wall time and peak memory per run)")
    jobs = ([(LANE, "fix", (k,) + CELLS[k]) for k in ("C_alt", "B_alt", "B_canonical", "ctrl_alt", "ctrl_canonical")]
            + [(LANE, "none", (k,) + v) for k, v in LCDM.items()]
            + [(LANE, "none", (k,) + CELLS[k]) for k in ("C_alt", "B_alt", "B_canonical", "ctrl_alt", "ctrl_canonical")])
    res = X.run_jobs(jobs, heavy=lambda j: j[2][2] >= 256, log=P)
    runs = {f"{p_}/{n_}": r["out"] for (l_, p_, n_), r in res.items()}
    LN.out["numbers"]["runs"] = runs
    LN.out["numbers"]["run_times"] = {f"{p_}/{n_}": dict(wall_s=round(r["wall_s"]), peak_rss_gb=round(r["peak_rss_gb"], 2))
                                      for (l_, p_, n_), r in res.items()}
    ref = {"C": R362["C_lcdm"], "B": runs["none/B_lcdm"], "ctrl": runs["none/ctrl_lcdm"]}

    LN.banner("C1 C2  CONTROLS: the committed line reproduces DE11b; MOND off reproduces the LCDM box")
    before = {k: D11b["worst"][k] for k in CELLS}
    rerun = {k: X.worst_p1d(runs[f"none/{k}"], ref[k.split("_")[0]]) for k in CELLS}
    c1 = max(abs(rerun[k] - before[k]) for k in CELLS)
    for k in CELLS:
        P(f"    {k:15s} committed {before[k]:.12f}   re-run (committed line) {rerun[k]:.12f}   |diff| {abs(rerun[k] - before[k]):.1e}")
    LN.check("C1 the committed line re-run reproduces DE11b's committed worst deviation in all five cells (1e-9)",
             f"max |diff| = {c1:.1e}", c1 <= 1e-9, "the harness is DE11b exactly; only the kernel line differs in 'fix'")
    c2 = X.max_abs_diff_p1d(runs["none/B_lcdm"], R362["B_lcdm"])
    c2r = X.max_abs_diff_p1d(runs["none/ctrl_lcdm"], R347["L25_lcdm"])
    LN.check("C2 MOND off: DE11b's B_lcdm re-run equals L362's committed B_lcdm P1D (1e-12)",
             f"max |P1D ratio - 1| = {c2:.1e}; ctrl_lcdm vs L347's L25_lcdm (CLASS 60 vs 40 h/Mpc, reported) {c2r:.1e}", c2 <= 1e-12,
             "so L362's committed C_lcdm is the LCDM reference DE11b's own C run would give")

    LN.banner("R1  BEFORE / AFTER: worst |P1D/P1D_LCDM - 1| over k_par 0.2-2 h/Mpc, z = 3 and 2 (DE11b's statistic)")
    after = {k: X.worst_p1d(runs[f"fix/{k}"], ref[k.split("_")[0]]) for k in CELLS}
    byz = {k: {z: X.worst_p1d(runs[f"fix/{k}"], ref[k.split("_")[0]], zs=(z,)) for z in ("3.0", "2.0")} for k in CELLS}
    act = {k: {p_: {z: runs[f"{p_}/{k}"][z]["active"] for z in ("3.0", "2.0")} for p_ in ("none", "fix")} for k in CELLS}
    P(f"    {'cell':15s} {'committed':>10s} {'after':>10s} {'after/before':>13s}   after z=3 / z=2      active mesh fraction z = 2: before -> after")
    for k in CELLS:
        P(f"    {k:15s} {before[k]:10.4f} {after[k]:10.4f} {after[k] / before[k]:13.2f}   {byz[k]['3.0']:.4f} / {byz[k]['2.0']:.4f}"
          f"      {act[k]['none']['2.0']:.2e} -> {act[k]['fix']['2.0']:.2e}")
    ok_before = all(before[k] <= 0.10 for k in TESTED)
    ok_after = all(after[k] <= 0.10 for k in TESTED)
    worst_after = max(after[k] for k in TESTED)
    growth = {"B/ctrl canonical": after["B_canonical"] / after["ctrl_canonical"], "B/ctrl alt": after["B_alt"] / after["ctrl_alt"],
              "C/ctrl alt (2x mesh)": after["C_alt"] / after["ctrl_alt"]}
    LN.out["numbers"]["R1"] = dict(before=before, rerun_committed_line=rerun, after=after, after_by_z=byz, active=act,
                                   F1_before="PASS" if ok_before else "FAIL", F1_after="PASS" if ok_after else "FAIL",
                                   worst_after=worst_after, growth_after=growth, growth_before=D11b["growth"],
                                   C_lcdm_reference="L362 committed C_lcdm")
    LN.check("R1 (reported) DE11b's F1 rule (worst <= 0.10 at B and C) with the corrected argument",
             f"before {max(before[k] for k in TESTED):.4f} ({'PASS' if ok_before else 'FAIL'}) -> after {worst_after:.4f} "
             f"({'PASS' if ok_after else 'FAIL'}); growth with resolution after: " + ", ".join(f"{k} {v:.2f}" for k, v in growth.items())
             + " (before: " + ", ".join(f"{k} {v:.2f}" for k, v in D11b["growth"].items()) + ")", True, load_bearing=False)
    LN.check("H1 (reported) the pre-declared hypothesis H-DE11b: the pass does not flip", f"verdict {'PASS' if ok_after else 'FAIL'} after "
             f"(worst {worst_after:.4f})", ok_after, "a failed hypothesis is kept as run", load_bearing=False)

    LN.banner("VERDICT")
    P(f"""  With ONLY the kernel argument corrected (|grad phi|/a: MOND sqrt(1+z) stronger at z = 2-3), DE11b's worst forest deviation
  goes {max(before[k] for k in TESTED):.4f} -> {worst_after:.4f} (x{worst_after / max(before[k] for k in TESTED):.1f}) against the 0.10 gate: the verdict
  {'does NOT flip (PASS)' if ok_after else 'FLIPS to FAIL'}.  Cells: """ + "; ".join(f"{k} {before[k]:.4f} -> {after[k]:.4f}" for k in CELLS) + f""".
  Controls: the committed line reproduces DE11b to {c1:.0e} (C1); MOND off reproduces the LCDM box to {c2:.0e} (C2).
  Unchanged limits (DE11b's own): FGPA, one realisation, all-matter kernel and a single fluid (both over-state the phantom).""")
    sys.exit(LN.finish())
