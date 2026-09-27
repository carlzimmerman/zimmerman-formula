#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
XR34_rescore_L359 -- L359's forest leg of the vacuum-gated window, re-scored with ONLY the kernel argument corrected.

L359 AS COMMITTED.  The vacuum-gated switch x_c,eff(z) = x_c0 E(z)^(2p) (matter reading) in L347's PM (128^3 mesh, 96^3
particles, 50 and 25 Mpc/h).  F1: a cell (p, x_c0) passes the forest if worst |P1D/P1D_LCDM - 1| <= 0.10 (k_par 0.2-2,
z = 3 and 2, both footings, both boxes).  W1, the window (growth + KiDS + forest): eight cells, forest worst 0.002-0.085;
the p = 0.5 cells are the closest to the gate (0.065-0.085), and DE2 uses (p = 0.5, x_c0 = 1.5) as its dominance anchor.
The growth (G1) and KiDS (K1) legs do not use the PM and are untouched.  L359's run_gated() carries the kernel line
|grad phi|/a^2 = (1+z) g_N,phys (XR34_kernel_argument).

METHOD.  L359's committed source executed read-only with that ONE line changed to |grad phi|/a (XR34_common).  A PARTIAL
re-score, to fit the shared machine: every window cell on the 25 Mpc/h box at both footings (in all ten committed F1
cells the 25 Mpc/h box carries the worst deviation, by 1.4-3.7x over 50 Mpc/h), plus the 50 Mpc/h box at the alt footing
for the anchor cell (p = 0.5, x_c0 = 1.5) to check that ordering after the correction.  A cell that fails on 25 Mpc/h
fails L359's rule; a cell that passes there passes it if the ordering holds (checked on the anchor cell only).
  'fix'  (after):   8 window cells x L25 x 2 footings; (0.5, 1.5) L50 alt
  'none' (control): (0.5, 1.5) L25 alt; LCDM: L25_lcdm through run_gated (L50: L347's committed L50_lcdm, the same code)
PRE-DECLARED (before any XR34 run; XR34_README 'Hypotheses')
  H-L359: the p = 0.5 cells FLIP to fail; the p = 1 and p = 2 cells stay pass (the window survives, shrunk to p >= 1).
CHECKS
  K1 [load-bearing] L359's own accel() with the corrected line reproduces the analytic single-halo QUMOND profile (2%).
  C1 [load-bearing] the committed line re-run reproduces L359's committed (0.5, 1.5) L25 alt deviations (z = 3, 2) to 1e-9.
  C2 [load-bearing] MOND off: run_gated's L25_lcdm equals L347's committed L25_lcdm P1D to 1e-12.
  R1 (reported) per window cell, before / after; the window re-scored; the anchor cell's box ordering.
  H1 (reported) whether H-L359 held.
MUTATE=1: 'double' stands in for the corrected line in K1 -> K1 FAILS (rc = 1); no PM run.

Run from the repository root (MUTATE=1 first):  python3 real_research/cross_thread_review_2026_09_26/XR34_rescore_L359.py
"""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import XR34_common as X                                                 # noqa: E402
import numpy as np                                                      # noqa: E402

MUTATE = os.environ.get("MUTATE", "0") == "1"
FIX = "double" if MUTATE else "fix"
LANE = "L359"
LN = X.Lane("XR34_rescore_L359", MUTATE)
P = LN.P
INF = float("inf")
ZZ = ("3.0", "2.0")
ANCHOR = (0.5, 1.5)

if __name__ == "__main__":
    P(__doc__.split("PRE-DECLARED")[0].strip())
    if MUTATE:
        P("\n  *** MUTATE=1: 'double' stands in for the corrected line; K1 must FAIL; no PM run ***")
    R59 = json.load(open(os.path.join(X.G03, "L359_vacuum_gated_switch_results.json")))["numbers"]
    R47 = json.load(open(os.path.join(X.G03, "L347_switch_forest_flux_power_results.json")))["numbers"]["runs"]
    WIN = [(float(c["p"]), float(c["x_c0"])) for c in R59["W1"]]

    LN.banner("K1  THE ARGUMENT: L359's own accel() (run_gated) on the analytic single halo")
    sf, sn = X.k1_tables(LANE, FIX)                                   # in a child holding one Budget token
    k1 = max(v["ratio"] for v in sf.values())
    for zk in sf:
        P(f"    {zk:13s} y {sf[zk]['y_min']:.3f}-{sf[zk]['y_max']:.3f}: kick/a over nu g_N  '{FIX}' {sf[zk]['ratio_min']:.3f}-"
          f"{sf[zk]['ratio_max']:.3f}   committed {sn[zk]['ratio_min']:.3f}-{sn[zk]['ratio_max']:.3f}")
    LN.out["numbers"]["K1"] = {"fix_or_mutant": sf, "committed": sn}
    LN.check("K1 L359's accel() with the corrected line reproduces nu_mono(g_N/a0) g_N on the analytic halo (2%, z = 3, 2, 0, "
             "both footings)", f"'{FIX}': max |ratio - 1| = {k1:.4f}; committed line: z = 3 {max(sn['z3/canonical']['ratio'], sn['z3/alt']['ratio']):.3f}, "
             f"z = 2 {max(sn['z2/canonical']['ratio'], sn['z2/alt']['ratio']):.3f}, z = 0 {max(sn['z0/canonical']['ratio'], sn['z0/alt']['ratio']):.3f}",
             k1 <= 0.02, "the 'after' runs below use the physical argument")
    if MUTATE:
        sys.exit(LN.finish())

    LN.banner(f"THE RUNS (L359's run_gated(), one line patched; window cells {WIN})")
    name = lambda tag, p_, x_, f_: f"{tag}_p{p_}_x{x_}_{f_}"
    jobs = [(LANE, "fix", (name("L25", p_, x_, f_), 25.0, "switch", f_, x_, p_)) for (p_, x_) in WIN for f_ in ("alt", "canonical")]
    jobs += [(LANE, "fix", (name("L50", ANCHOR[0], ANCHOR[1], "alt"), 50.0, "switch", "alt", ANCHOR[1], ANCHOR[0])),
             (LANE, "none", ("L25_lcdm", 25.0, "lcdm", "canonical", INF, 0.0)),
             (LANE, "none", (name("L25", ANCHOR[0], ANCHOR[1], "alt"), 25.0, "switch", "alt", ANCHOR[1], ANCHOR[0]))]
    res = X.run_jobs(jobs, log=P)
    runs = {f"{p_}/{n_}": r["out"] for (l_, p_, n_), r in res.items()}
    LN.out["numbers"]["runs"] = runs
    LN.out["numbers"]["run_times"] = {f"{p_}/{n_}": dict(wall_s=round(r["wall_s"]), peak_rss_gb=round(r["peak_rss_gb"], 2))
                                      for (l_, p_, n_), r in res.items()}
    ref = {"L25": runs["none/L25_lcdm"], "L50": R47["L50_lcdm"]}

    LN.banner("C1 C2  CONTROLS: the committed line reproduces L359; MOND off reproduces the LCDM box")
    an = name("L25", ANCHOR[0], ANCHOR[1], "alt")
    com = R59["F1"][f"{ANCHOR[0]}/{ANCHOR[1]}"]["cells"]
    c1 = max(abs(X.worst_p1d(runs[f"none/{an}"], ref["L25"], zs=(z,)) - com[f"L25/alt/{z}"]) for z in ZZ)
    LN.check("C1 the committed line re-run reproduces L359's committed (0.5, 1.5) L25 alt deviations at z = 3 and 2 (1e-9)",
             f"committed {com['L25/alt/3.0']:.10f} / {com['L25/alt/2.0']:.10f}; max |diff| = {c1:.1e}", c1 <= 1e-9,
             "the harness is L359 exactly; only the kernel line differs in 'fix'")
    c2 = X.max_abs_diff_p1d(runs["none/L25_lcdm"], R47["L25_lcdm"])
    LN.check("C2 MOND off: run_gated's L25_lcdm equals L347's committed L25_lcdm P1D (1e-12)", f"max |P1D ratio - 1| = {c2:.1e}",
             c2 <= 1e-12)

    LN.banner("R1  BEFORE / AFTER per window cell: worst |P1D/P1D_LCDM - 1|, k_par 0.2-2 h/Mpc, z = 3 and 2")
    rows, win_after = {}, []
    for (p_, x_) in WIN:
        cb = R59["F1"][f"{p_}/{x_}"]["cells"]
        b25 = max(cb[f"L25/{f}/{z}"] for f in ("canonical", "alt") for z in ZZ)
        a25 = {f"L25/{f}/{z}": X.worst_p1d(runs[f"fix/{name('L25', p_, x_, f)}"], ref["L25"], zs=(z,)) for f in ("canonical", "alt") for z in ZZ}
        wa = max(a25.values())
        rows[f"{p_}/{x_}"] = dict(before_all=R59["F1"][f"{p_}/{x_}"]["worst"], before_L25=b25, after_L25=wa, after_cells=a25,
                                  pass_after=wa <= 0.10)
        if wa <= 0.10:
            win_after.append((p_, x_))
        P(f"    p = {p_:3.1f}, x_c0 = {x_:3.1f}: before {R59['F1'][f'{p_}/{x_}']['worst']:.4f} (L25 {b25:.4f})   after (L25) {wa:.4f} "
          f"x{wa / b25:.2f}  -> {'PASS' if wa <= 0.10 else 'FAIL'}   [" + ", ".join(f"{k} {v:.3f}" for k, v in a25.items()) + "]")
    a50 = {z: X.worst_p1d(runs[f"fix/{name('L50', ANCHOR[0], ANCHOR[1], 'alt')}"], ref["L50"], zs=(z,)) for z in ZZ}
    order_ok = max(a50.values()) <= rows[f"{ANCHOR[0]}/{ANCHOR[1]}"]["after_L25"]
    P(f"    anchor (0.5, 1.5) L50 alt after: z = 3 {a50['3.0']:.4f}, z = 2 {a50['2.0']:.4f}  (before {com['L50/alt/3.0']:.4f}, "
      f"{com['L50/alt/2.0']:.4f}); L25 still the worse box: {order_ok}")
    p05 = [c for c in WIN if c[0] == 0.5]; pge1 = [c for c in WIN if c[0] >= 1.0]
    hyp = all(not rows[f"{p_}/{x_}"]["pass_after"] for (p_, x_) in p05) and all(rows[f"{p_}/{x_}"]["pass_after"] for (p_, x_) in pge1)
    LN.out["numbers"]["R1"] = dict(rows=rows, window_before=WIN, window_after=win_after, anchor_L50_alt_after=a50,
                                   anchor_box_ordering_holds=order_ok, partial="L25 box, both footings; L50 alt for (0.5, 1.5) only")
    LN.check("R1 (reported) L359's forest leg with the corrected argument (25 Mpc/h box, both footings; the window's growth and "
             "KiDS legs are untouched)", f"window cells passing the forest: before {len(WIN)} -> after {len(win_after)} "
             f"({', '.join(f'({p_:g}, {x_:g})' for p_, x_ in win_after) or 'none'}); anchor (0.5, 1.5) "
             f"{rows['0.5/1.5']['before_all']:.4f} -> {rows['0.5/1.5']['after_L25']:.4f}", True, load_bearing=False)
    LN.check("H1 (reported) the pre-declared hypothesis H-L359: the p = 0.5 cells flip to fail, the p >= 1 cells stay pass",
             ", ".join(f"({p_:g}, {x_:g}) {rows[f'{p_}/{x_}']['after_L25']:.3f}" for (p_, x_) in WIN), hyp,
             "a failed hypothesis is kept as run", load_bearing=False)

    LN.banner("VERDICT")
    P(f"""  With ONLY the kernel argument corrected, L359's forest leg (25 Mpc/h box, both footings) keeps {len(win_after)} of the {len(WIN)}
  window cells: {', '.join(f'({p_:g}, {x_:g})' for p_, x_ in win_after) or 'none'}.  The anchor (0.5, 1.5) goes {rows['0.5/1.5']['before_all']:.4f} ->
  {rows['0.5/1.5']['after_L25']:.4f}.  Partial: the 50 Mpc/h box is re-run for the anchor cell only (alt), where it stays below the
  25 Mpc/h box: {order_ok}.  Controls: committed line reproduces L359 to {c1:.0e} (C1); MOND off reproduces the box to {c2:.0e} (C2).""")
    sys.exit(LN.finish())
