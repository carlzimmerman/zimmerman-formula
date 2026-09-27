#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
XR34_rescore_L358 -- L358's KiDS-forest pincer (forest side) re-scored with ONLY the MOND kernel's argument corrected.

L358 AS COMMITTED.  L347's run() (imported and called unchanged) at constant thresholds x_c = 2, 2.5, 3, 4, both
footings, 50 and 25 Mpc/h.  Worst |P1D/P1D_LCDM - 1|: 0.185 / 0.174 / 0.160 / 0.131.  F2: every KiDS-accepted threshold
(2, 2.5, 3) fails the 10% rule -> the pincer HOLDS; F3: carried by the 25 Mpc/h box (the 50 Mpc/h box alone gives 0.096
at x_c = 3 and would pass).  L358 has no kernel line of its own: it inherits L347's, |grad phi|/a^2 = (1+z) g_N,phys.

METHOD.  L347's committed source executed read-only with that ONE line changed to |grad phi|/a (XR34_common), called with
L358's configurations.  A PARTIAL re-score, to fit the shared machine: every threshold on the 25 Mpc/h box at both
footings (in all 32 committed L358 cells the 25 Mpc/h box carries the worst deviation), plus the 50 Mpc/h box at x_c = 3
(F3's cell).  A threshold that fails on 25 Mpc/h fails L358's rule, so the pincer's direction is decided without L50.
  'fix'  (after):   L25 x (2, 2.5, 3, 4) x 2 footings; L50 x_c = 3 x 2 footings
  'none' (control): L25_x3.0_alt; the LCDM references are L358's committed L25_lcdm and L50_lcdm (L347's run, the same
                    code; C1 reproduces a cell against them)
PRE-DECLARED (before any XR34 run; XR34_README 'Hypotheses')
  H-L358: the pincer does NOT flip (every KiDS-accepted threshold still fails; the deviations grow).
CHECKS
  K1 [load-bearing] L347's accel() with the corrected line reproduces the analytic single-halo QUMOND profile (2%).
  C1 [load-bearing] the committed line re-run reproduces L358's committed L25_x3.0_alt P1D to 1e-12.
  C2 [load-bearing] MOND off: L358's committed LCDM P1D equals L347's committed LCDM P1D (the same run() and phases) to 1e-12.
  R1 (reported) the forest-observable curve vs threshold before / after; F2 and F3 re-scored.
  H1 (reported) whether H-L358 held.
MUTATE=1: 'double' stands in for the corrected line in K1 -> K1 FAILS (rc = 1); no PM run.

Run from the repository root (MUTATE=1 first):  python3 real_research/cross_thread_review_2026_09_26/XR34_rescore_L358.py
"""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import XR34_common as X                                                 # noqa: E402
import numpy as np                                                      # noqa: E402

MUTATE = os.environ.get("MUTATE", "0") == "1"
FIX = "double" if MUTATE else "fix"
LANE = "L347"
LN = X.Lane("XR34_rescore_L358", MUTATE)
P = LN.P
XCS = (2.0, 2.5, 3.0, 4.0)
KIDS_OK = (2.0, 2.5, 3.0)
ZZ = ("3.0", "2.0")

if __name__ == "__main__":
    P(__doc__.split("PRE-DECLARED")[0].strip())
    if MUTATE:
        P("\n  *** MUTATE=1: 'double' stands in for the corrected line; K1 must FAIL; no PM run ***")
    R58 = json.load(open(os.path.join(X.G03, "L358_forest_kids_pincer_observable_results.json")))["numbers"]
    R47 = json.load(open(os.path.join(X.G03, "L347_switch_forest_flux_power_results.json")))["numbers"]["runs"]

    LN.banner("K1  THE ARGUMENT: L347's accel() (the one L358 runs) on the analytic single halo")
    sf, sn = X.k1_tables(LANE, FIX)                                   # in a child holding one Budget token
    k1 = max(v["ratio"] for v in sf.values())
    for zk in sf:
        P(f"    {zk:13s} y {sf[zk]['y_min']:.3f}-{sf[zk]['y_max']:.3f}: kick/a over nu g_N  '{FIX}' {sf[zk]['ratio_min']:.3f}-"
          f"{sf[zk]['ratio_max']:.3f}   committed {sn[zk]['ratio_min']:.3f}-{sn[zk]['ratio_max']:.3f}")
    LN.out["numbers"]["K1"] = {"fix_or_mutant": sf, "committed": sn}
    LN.check("K1 L347's accel() with the corrected line reproduces nu_mono(g_N/a0) g_N on the analytic halo (2%, z = 3, 2, 0, "
             "both footings)", f"'{FIX}': max |ratio - 1| = {k1:.4f}; committed line: z = 3 {max(sn['z3/canonical']['ratio'], sn['z3/alt']['ratio']):.3f}, "
             f"z = 2 {max(sn['z2/canonical']['ratio'], sn['z2/alt']['ratio']):.3f}, z = 0 {max(sn['z0/canonical']['ratio'], sn['z0/alt']['ratio']):.3f}",
             k1 <= 0.02, "the 'after' runs below use the physical argument")
    if MUTATE:
        sys.exit(LN.finish())

    LN.banner("THE RUNS (L347's run() with L358's configurations, one line patched)")
    jobs = [(LANE, "fix", (f"L25_x{xc}_{f}", 25.0, "switch", f, xc)) for xc in XCS for f in ("alt", "canonical")]
    jobs += [(LANE, "fix", (f"L50_x3.0_{f}", 50.0, "switch", f, 3.0)) for f in ("alt", "canonical")]
    jobs += [(LANE, "none", ("L25_x3.0_alt", 25.0, "switch", "alt", 3.0))]
    res = X.run_jobs(jobs, log=P)
    runs = {f"{p_}/{n_}": r["out"] for (l_, p_, n_), r in res.items()}
    LN.out["numbers"]["runs"] = runs
    LN.out["numbers"]["run_times"] = {f"{p_}/{n_}": dict(wall_s=round(r["wall_s"]), peak_rss_gb=round(r["peak_rss_gb"], 2))
                                      for (l_, p_, n_), r in res.items()}
    C = R58["runs"]

    LN.banner("C1 C2  CONTROLS: the committed line reproduces L358; its LCDM boxes are L347's")
    c1 = X.max_abs_diff_p1d(runs["none/L25_x3.0_alt"], C["L25_x3.0_alt"])
    LN.check("C1 the committed line re-run reproduces L358's committed L25_x3.0_alt P1D (1e-12)", f"max |P1D ratio - 1| = {c1:.1e}",
             c1 <= 1e-12, "the harness is L358's L347 run() exactly; only the kernel line differs in 'fix'")
    c2 = max(X.max_abs_diff_p1d(C[f"{t}_lcdm"], R47[f"{t}_lcdm"]) for t in ("L50", "L25"))
    LN.check("C2 MOND off: L358's committed LCDM P1D equals L347's committed LCDM P1D (1e-12)", f"max |P1D ratio - 1| = {c2:.1e}",
             c2 <= 1e-12)

    LN.banner("R1  BEFORE / AFTER: the forest-observable curve vs threshold (worst |P1D/P1D_LCDM - 1|, k_par 0.2-2, z = 3 and 2)")
    ref = {"L25": C["L25_lcdm"], "L50": C["L50_lcdm"]}
    wb_all, wb25, wa25 = {}, {}, {}
    for xc in XCS:
        wb_all[xc] = R58["worst"][str(xc)]
        wb25[xc] = max(X.worst_p1d(C[f"L25_x{xc}_{f}"], ref["L25"]) for f in ("canonical", "alt"))
        cells = {f"{f}/z{z}": X.worst_p1d(runs[f"fix/L25_x{xc}_{f}"], ref["L25"], zs=(z,)) for f in ("canonical", "alt") for z in ZZ}
        wa25[xc] = max(cells.values())
        P(f"    x_c = {xc:3.1f}: before {wb_all[xc]:.3f} (L25 {wb25[xc]:.3f})   after (L25) {wa25[xc]:.3f}  x{wa25[xc] / wb25[xc]:.2f}  "
          f"-> {'PASS' if wa25[xc] <= 0.10 else 'FAIL'} the 10% rule   [" + ", ".join(f"{k} {v:.3f}" for k, v in cells.items()) + "]")
    co_b = R58["resolution_x3"]["coarse"]
    co_a = max(X.worst_p1d(runs[f"fix/L50_x3.0_{f}"], ref["L50"]) for f in ("canonical", "alt"))
    fails_b = [xc for xc in KIDS_OK if wb_all[xc] > 0.10]
    fails_a = [xc for xc in KIDS_OK if wa25[xc] > 0.10]
    holds_a = len(fails_a) == len(KIDS_OK)
    P(f"    F3 the 50 Mpc/h box alone at x_c = 3: before {co_b:.3f} ({'passes' if co_b <= 0.10 else 'fails'})   after {co_a:.3f} "
      f"({'passes' if co_a <= 0.10 else 'fails'})")
    LN.out["numbers"]["R1"] = dict(before_all=wb_all, before_L25=wb25, after_L25=wa25, coarse_x3_before=co_b, coarse_x3_after=co_a,
                                   kids_ok=KIDS_OK, failing_before=fails_b, failing_after=fails_a, pincer_after=holds_a,
                                   partial="L25 box, both footings; L50 at x_c = 3 only")
    LN.check("R1 (reported) L358's F2 (the pincer holds iff every KiDS-accepted x_c fails) and F3 with the corrected argument",
             ", ".join(f"x_c {xc}: {wb_all[xc]:.3f} -> {wa25[xc]:.3f}" for xc in XCS) + f"; pincer {'HOLDS' if holds_a else 'OPENS'}; "
             f"50 Mpc/h alone at x_c = 3: {co_b:.3f} -> {co_a:.3f}", True, load_bearing=False)
    LN.check("H1 (reported) the pre-declared hypothesis H-L358: the pincer does not flip", f"failing KiDS-accepted thresholds after: {fails_a}",
             holds_a, "a failed hypothesis is kept as run", load_bearing=False)

    LN.banner("VERDICT")
    P(f"""  With ONLY the kernel argument corrected, the forest curve at constant threshold rises: """ + ", ".join(
        f"x_c {xc}: {wb_all[xc]:.3f} -> {wa25[xc]:.3f}" for xc in XCS) + f""".  The pincer {'HOLDS (no flip)' if holds_a else 'OPENS (FLIP)'};
  the 50 Mpc/h box alone at x_c = 3 now {'fails' if co_a > 0.10 else 'passes'} ({co_a:.3f}), so the pincer is {'no longer' if co_a > 0.10 else 'still'} carried by
  the finer box alone.  Partial re-score (see METHOD).  Controls: C1 {c1:.0e}, C2 {c2:.0e}.""")
    sys.exit(LN.finish())
