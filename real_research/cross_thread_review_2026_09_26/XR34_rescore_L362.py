#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
XR34_rescore_L362 -- L362's forest convergence verdict re-scored with ONLY the MOND kernel's argument corrected.

L362 AS COMMITTED.  L342's constant-threshold switch at the KiDS-accepted x_c = 3 (matter reading, all matter feels the
phantom), L347's machinery generalised to (box L, mesh NG, particles NP), CLASS to 60 h/Mpc, seed 7:
  A (50, 128, 128), B (25, 128, 128), C (25, 256, 192); control ctrl_x5 (50, 128, 96) at x_c = 5.
F1: worst |P1D/P1D_LCDM - 1| (k_par 0.2-2, z = 3 and 2, both footings) = A 0.104, B 0.157, C 0.191 -> the forest side of
the KiDS-forest pincer is RESOLUTION-ROBUST (B and C > 0.10).  Its kernel line reads |grad phi|/a^2 = (1+z) g_N,phys.

METHOD.  L362's committed source executed read-only with that ONE line changed to |grad phi|/a (XR34_common).  Runs:
  'fix'  (after):   A, B, C at x_c = 3, both footings; ctrl_x5
  'none' (control): A_x3_alt, B_x3_alt, ctrl_x5 (compared with L362's committed P1D arrays)
  LCDM:             A_lcdm and ctrl_lcdm re-run (compared with the committed arrays); every ratio uses L362's committed
                    LCDM P1D (B_lcdm's exactness: XR34_rescore_DE11b C2; C_lcdm is not re-run)
The committed-line C runs are not re-run (256^3 mesh, ~6.5 GB and ~1 h each on the shared machine): L362's committed C
arrays are the 'before', and XR34_rescore_DE11b's C1 re-runs a C cell of the same Sim to 1e-9.
PRE-DECLARED (before any XR34 run; XR34_README 'Hypotheses')
  H-L362: 'resolution-robust' does NOT flip (B and C stay > 0.10 and grow).
CHECKS
  K1 [load-bearing] L362's own accel() with the corrected line reproduces the analytic single-halo QUMOND profile (2%).
  C1 [load-bearing] the committed line re-run reproduces L362's committed P1D arrays (A_x3_alt, B_x3_alt, ctrl_x5) to 1e-12.
  C2 [load-bearing] MOND off: A_lcdm and ctrl_lcdm re-runs equal L362's committed LCDM P1D to 1e-12.
  R1 (reported) before / after per box and footing; L362's F1 rule re-scored.
  H1 (reported) whether H-L362 held.
MUTATE=1: 'double' stands in for the corrected line in K1 -> K1 FAILS (rc = 1); no PM run.

Run from the repository root (MUTATE=1 first):  python3 real_research/cross_thread_review_2026_09_26/XR34_rescore_L362.py
"""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import XR34_common as X                                                 # noqa: E402
import numpy as np                                                      # noqa: E402

MUTATE = os.environ.get("MUTATE", "0") == "1"
FIX = "double" if MUTATE else "fix"
LANE = "L362"
LN = X.Lane("XR34_rescore_L362", MUTATE)
P = LN.P
BOX = {"A": (50.0, 128, 128), "B": (25.0, 128, 128), "C": (25.0, 256, 192)}
CFG = {f"{t}_x3_{f}": b + ("switch", f, 3.0) for t, b in BOX.items() for f in ("canonical", "alt")}
CFG["ctrl_x5"] = (50.0, 128, 96, "switch", "canonical", 5.0)
LCDM = {"A_lcdm": (50.0, 128, 128, "lcdm", "canonical", 0), "ctrl_lcdm": (50.0, 128, 96, "lcdm", "canonical", 0)}
NONE = ("A_x3_alt", "B_x3_alt", "ctrl_x5")

if __name__ == "__main__":
    P(__doc__.split("PRE-DECLARED")[0].strip())
    if MUTATE:
        P("\n  *** MUTATE=1: 'double' stands in for the corrected line; K1 must FAIL; no PM run ***")
    R62 = json.load(open(os.path.join(X.G03, "L362_forest_pincer_convergence_results.json")))["numbers"]

    LN.banner("K1  THE ARGUMENT: L362's own accel() on the analytic single halo")
    sf, sn = X.k1_tables(LANE, FIX)                                   # in a child holding one Budget token
    k1 = max(v["ratio"] for v in sf.values())
    for zk in sf:
        P(f"    {zk:13s} y {sf[zk]['y_min']:.3f}-{sf[zk]['y_max']:.3f}: kick/a over nu g_N  '{FIX}' {sf[zk]['ratio_min']:.3f}-"
          f"{sf[zk]['ratio_max']:.3f}   committed {sn[zk]['ratio_min']:.3f}-{sn[zk]['ratio_max']:.3f}")
    LN.out["numbers"]["K1"] = {"fix_or_mutant": sf, "committed": sn}
    LN.check("K1 L362's accel() with the corrected line reproduces nu_mono(g_N/a0) g_N on the analytic halo (2%, z = 3, 2, 0, "
             "both footings)", f"'{FIX}': max |ratio - 1| = {k1:.4f}; committed line: z = 3 {max(sn['z3/canonical']['ratio'], sn['z3/alt']['ratio']):.3f}, "
             f"z = 2 {max(sn['z2/canonical']['ratio'], sn['z2/alt']['ratio']):.3f}, z = 0 {max(sn['z0/canonical']['ratio'], sn['z0/alt']['ratio']):.3f}",
             k1 <= 0.02, "the 'after' runs below use the physical argument")
    if MUTATE:
        sys.exit(LN.finish())

    LN.banner("THE RUNS (L362's run(), one line patched; wall time and peak memory per run)")
    jobs = ([(LANE, "fix", ("C_x3_alt",) + CFG["C_x3_alt"])]
            + [(LANE, "fix", (k,) + CFG[k]) for k in ("B_x3_alt", "B_x3_canonical", "A_x3_alt", "A_x3_canonical", "ctrl_x5")]
            + [(LANE, "none", (k,) + v) for k, v in LCDM.items()] + [(LANE, "none", (k,) + CFG[k]) for k in NONE]
            + [(LANE, "fix", ("C_x3_canonical",) + CFG["C_x3_canonical"])])
    res = X.run_jobs(jobs, heavy=lambda j: j[2][2] >= 256, log=P)
    runs = {f"{p_}/{n_}": r["out"] for (l_, p_, n_), r in res.items()}
    LN.out["numbers"]["runs"] = runs
    LN.out["numbers"]["run_times"] = {f"{p_}/{n_}": dict(wall_s=round(r["wall_s"]), peak_rss_gb=round(r["peak_rss_gb"], 2))
                                      for (l_, p_, n_), r in res.items()}
    C = R62["runs"]                                                      # committed arrays (before, and the LCDM references)

    LN.banner("C1 C2  CONTROLS: the committed line reproduces L362; MOND off reproduces the LCDM box")
    c1 = max(X.max_abs_diff_p1d(runs[f"none/{k}"], C[k]) for k in NONE)
    LN.check("C1 the committed line re-run reproduces L362's committed P1D arrays (A_x3_alt, B_x3_alt, ctrl_x5; 1e-12)",
             f"max |P1D ratio - 1| = {c1:.1e}", c1 <= 1e-12, "the harness is L362 exactly; only the kernel line differs in 'fix'")
    c2 = max(X.max_abs_diff_p1d(runs[f"none/{k}"], C[k]) for k in LCDM)
    LN.check("C2 MOND off: A_lcdm and ctrl_lcdm re-runs equal L362's committed LCDM P1D (1e-12)", f"max |P1D ratio - 1| = {c2:.1e}",
             c2 <= 1e-12)

    LN.banner("R1  BEFORE / AFTER: worst |P1D/P1D_LCDM - 1| over k_par 0.2-2 h/Mpc, z = 3 and 2 (L362's statistic)")
    ref = {"A": C["A_lcdm"], "B": C["B_lcdm"], "C": C["C_lcdm"], "ctrl": C["ctrl_lcdm"]}
    before, after = {}, {}
    for k in CFG:
        t = k.split("_")[0]
        before[k] = X.worst_p1d(C[k], ref[t]); after[k] = X.worst_p1d(runs[f"fix/{k}"], ref[t])
        P(f"    {k:16s} before {before[k]:.4f}   after {after[k]:.4f}   x{after[k] / before[k]:.2f}   (after z = 3 / 2: "
          f"{X.worst_p1d(runs[f'fix/{k}'], ref[t], zs=('3.0',)):.4f} / {X.worst_p1d(runs[f'fix/{k}'], ref[t], zs=('2.0',)):.4f})")
    Wb = {t: max(before[f"{t}_x3_{f}"] for f in ("canonical", "alt")) for t in BOX}
    Wa = {t: max(after[f"{t}_x3_{f}"] for f in ("canonical", "alt")) for t in BOX}
    dcom = max(abs(Wb[t] - R62["worst_x3"][t]) for t in BOX)
    rob_b = Wb["B"] > 0.10 and Wb["C"] > 0.10
    rob_a = Wa["B"] > 0.10 and Wa["C"] > 0.10
    P(f"    worst per box (max over footings): " + "; ".join(f"{t} {Wb[t]:.3f} -> {Wa[t]:.3f}" for t in BOX)
      + f"   (before recomputed from the committed arrays equals L362's committed worst_x3 to {dcom:.0e})")
    LN.out["numbers"]["R1"] = dict(before=before, after=after, worst_before=Wb, worst_after=Wa,
                                   F1_before="RESOLUTION-ROBUST" if rob_b else "NOT robust", F1_after="RESOLUTION-ROBUST" if rob_a else "NOT robust")
    LN.check("R1 (reported) L362's F1 rule (robust iff B and C exceed 0.10 at x_c = 3) with the corrected argument",
             "; ".join(f"{t} {Wb[t]:.3f} -> {Wa[t]:.3f}" for t in BOX) + f"; ctrl_x5 {before['ctrl_x5']:.3f} -> {after['ctrl_x5']:.3f}"
             f" -> {'RESOLUTION-ROBUST' if rob_a else 'NOT robust'} (before: {'RESOLUTION-ROBUST' if rob_b else 'NOT robust'})",
             True, load_bearing=False)
    LN.check("H1 (reported) the pre-declared hypothesis H-L362: 'resolution-robust' does not flip", f"B {Wa['B']:.3f}, C {Wa['C']:.3f}",
             rob_a, "a failed hypothesis is kept as run", load_bearing=False)

    LN.banner("VERDICT")
    P(f"""  With ONLY the kernel argument corrected, L362's worst forest deviation at x_c = 3 is A {Wb['A']:.3f} -> {Wa['A']:.3f},
  B {Wb['B']:.3f} -> {Wa['B']:.3f}, C {Wb['C']:.3f} -> {Wa['C']:.3f}: the forest side of the KiDS-forest pincer is
  {'still RESOLUTION-ROBUST (no flip); the constant-threshold switch fails the forest by more' if rob_a else 'NO LONGER robust (FLIP)'}.
  Controls: committed line reproduces L362 to {c1:.0e} (C1); MOND off reproduces the LCDM boxes to {c2:.0e} (C2).""")
    sys.exit(LN.finish())
