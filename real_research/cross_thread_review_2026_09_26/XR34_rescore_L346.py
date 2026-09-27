#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
XR34_rescore_L346 -- L346's forest gate (matter power) re-scored with ONLY the MOND kernel's argument corrected.

L346 AS COMMITTED.  L342's constant-threshold switch (matter reading, x = 1.5 Omega_m(a) delta_mesh) in L176's PM (50 Mpc/h,
128^3 mesh, 96^3 particles, CLASS to 20 h/Mpc, seed 7).  F2: P_switch/P_LCDM in the forest band (k = 1-4 h/Mpc, z = 3 and
2) at x_c = 5 must lie in [0.8, 1.2] for both footings: worst |P/P_LCDM - 1| = 0.36 -> FAILS.  C3: MOND everywhere
overshoots (3.5-4.6).  F1 (diagnostic): the switched-on mass fraction and its median |g_N|/a0.  F3: 0.8 Mpc/h smoothing
gives less excess.  Its kernel line is gN = -grad phi / a^2 = (1+z) g_N,phys; the F1 median reads the same gN.

METHOD.  L346's committed source executed read-only with that ONE line changed to gN = -grad phi / a (XR34_common).
The same line feeds F1's median |g_N|/a0, which after the change is the physical one.  Runs:
  'fix'  (after):   sw5_canon, sw5_alt, sw4_canon, sw7_canon, sw5_smooth08, sw5_phantomx, no_switch
  'none' (control): sw5_canon, sw5_alt; LCDM re-run
PRE-DECLARED (before any XR34 run; XR34_README 'Hypotheses')
  H-L346: F2's FAIL does NOT flip (the excess grows).
CHECKS
  K1 [load-bearing] L346's own accel() with the corrected line reproduces the analytic single-halo QUMOND profile (2%).
  C1 [load-bearing] the committed line re-run reproduces L346's committed P(k) arrays and F1 diagnostics (sw5_canon,
     sw5_alt) to 1e-12.
  C2 [load-bearing] MOND off: the LCDM re-run equals L346's committed LCDM P(k) to 1e-12.
  R1 (reported) F2 per cell before / after, C3, F1, F3.
  H1 (reported) whether H-L346 held.
MUTATE=1: 'double' stands in for the corrected line in K1 -> K1 FAILS (rc = 1); no PM run.

Run from the repository root (MUTATE=1 first):  python3 real_research/cross_thread_review_2026_09_26/XR34_rescore_L346.py
"""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import XR34_common as X                                                 # noqa: E402
import numpy as np                                                      # noqa: E402

MUTATE = os.environ.get("MUTATE", "0") == "1"
FIX = "double" if MUTATE else "fix"
LANE = "L346"
LN = X.Lane("XR34_rescore_L346", MUTATE)
P = LN.P
INF = float("inf")
CFG = {"no_switch": ("switch", "canonical", 0, 0.0, False), "sw5_canon": ("switch", "canonical", 5.0, 0.0, False),
       "sw5_alt": ("switch", "alt", 5.0, 0.0, False), "sw4_canon": ("switch", "canonical", 4.0, 0.0, False),
       "sw7_canon": ("switch", "canonical", 7.0, 0.0, False), "sw5_smooth08": ("switch", "canonical", 5.0, 0.8, False),
       "sw5_phantomx": ("switch", "canonical", 5.0, 0.0, True)}
NONE = ("sw5_canon", "sw5_alt")
ZZ = ("3.0", "2.0")


def score(runs, lcdm):
    """L346's F2/C3/F3 arithmetic, line for line."""
    ref = {z: np.array(lcdm["pk"][z]) for z in ZZ}
    kk = ref["3.0"][:, 0]; forest = (kk >= 1.0) & (kk <= 4.0)
    ratio = lambda n, z: np.array(runs[n]["pk"][z])[:, 1] / ref[z][:, 1]
    gate = {f"{n}_{z}": (float(ratio(n, z)[forest].min()), float(ratio(n, z)[forest].max())) for n in CFG for z in ZZ}
    passes = all(0.8 <= gate[f"{n}_{z}"][0] and gate[f"{n}_{z}"][1] <= 1.2 for n in ("sw5_canon", "sw5_alt") for z in ZZ)
    worst = max(max(abs(gate[f"{n}_{z}"][0] - 1), abs(gate[f"{n}_{z}"][1] - 1)) for n in ("sw5_canon", "sw5_alt") for z in ZZ)
    ex = {n: float(np.mean(np.abs(ratio(n, "3.0")[forest] - 1))) for n in ("sw5_smooth08", "sw5_canon", "sw5_phantomx")}
    return dict(gate=gate, passes=passes, worst=worst, C3_min_z3=gate["no_switch_3.0"][0], F3=ex,
                F3_ok=ex["sw5_smooth08"] <= ex["sw5_canon"], forest_k=kk[forest].tolist())


if __name__ == "__main__":
    P(__doc__.split("PRE-DECLARED")[0].strip())
    if MUTATE:
        P("\n  *** MUTATE=1: 'double' stands in for the corrected line; K1 must FAIL; no PM run ***")
    R46 = json.load(open(os.path.join(X.G03, "L346_switch_forest_gate_results.json")))["numbers"]

    LN.banner("K1  THE ARGUMENT: L346's own accel() on the analytic single halo (L346's 50 Mpc/h mesh)")
    sf, sn = X.k1_tables(LANE, FIX)                                   # in a child holding one Budget token
    k1 = max(v["ratio"] for v in sf.values())
    for zk in sf:
        P(f"    {zk:13s} y {sf[zk]['y_min']:.3f}-{sf[zk]['y_max']:.3f}: kick/a over nu g_N  '{FIX}' {sf[zk]['ratio_min']:.3f}-"
          f"{sf[zk]['ratio_max']:.3f}   committed {sn[zk]['ratio_min']:.3f}-{sn[zk]['ratio_max']:.3f}")
    LN.out["numbers"]["K1"] = {"fix_or_mutant": sf, "committed": sn}
    LN.check("K1 L346's accel() with the corrected line reproduces nu_mono(g_N/a0) g_N on the analytic halo (2%, z = 3, 2, 0, "
             "both footings)", f"'{FIX}': max |ratio - 1| = {k1:.4f}; committed line: z = 3 {max(sn['z3/canonical']['ratio'], sn['z3/alt']['ratio']):.3f}, "
             f"z = 2 {max(sn['z2/canonical']['ratio'], sn['z2/alt']['ratio']):.3f}, z = 0 {max(sn['z0/canonical']['ratio'], sn['z0/alt']['ratio']):.3f}",
             k1 <= 0.02, "the 'after' runs below use the physical argument")
    if MUTATE:
        sys.exit(LN.finish())

    LN.banner("THE RUNS (L346's run(), one line patched; wall time and peak memory per run)")
    jobs = ([(LANE, "fix", (k,) + CFG[k]) for k in ("sw5_alt", "sw5_canon", "sw4_canon", "sw7_canon", "sw5_smooth08", "sw5_phantomx",
                                                   "no_switch")]
            + [(LANE, "none", ("lcdm", "lcdm", "canonical", 0, 0.0, False))] + [(LANE, "none", (k,) + CFG[k]) for k in NONE])
    res = X.run_jobs(jobs, log=P)
    runs = {f"{p_}/{n_}": r["out"] for (l_, p_, n_), r in res.items()}
    LN.out["numbers"]["runs"] = runs
    LN.out["numbers"]["run_times"] = {f"{p_}/{n_}": dict(wall_s=round(r["wall_s"]), peak_rss_gb=round(r["peak_rss_gb"], 2))
                                      for (l_, p_, n_), r in res.items()}
    C = R46["runs"]

    LN.banner("C1 C2  CONTROLS: the committed line reproduces L346; MOND off reproduces the LCDM box")
    pkd = lambda A, B: max(float(np.max(np.abs(np.array(A["pk"][z])[:, 1] / np.array(B["pk"][z])[:, 1] - 1))) for z in ("6.0", "3.0", "2.0"))
    dgd = lambda A, B: max(abs(A["diag"][z][i] - B["diag"][z][i]) / max(abs(B["diag"][z][i]), 1e-30)
                           for z in ("6.0", "3.0", "2.0") for i in (0, 1))
    c1 = max(max(pkd(runs[f"none/{k}"], C[k]), dgd(runs[f"none/{k}"], C[k])) for k in NONE)
    LN.check("C1 the committed line re-run reproduces L346's committed P(k) and F1 diagnostics (sw5_canon, sw5_alt; 1e-12)",
             f"max relative difference = {c1:.1e}", c1 <= 1e-12, "the harness is L346 exactly; only the kernel line differs in 'fix'")
    c2 = pkd(runs["none/lcdm"], C["lcdm"])
    LN.check("C2 MOND off: the LCDM re-run equals L346's committed LCDM P(k) (1e-12)", f"max |P ratio - 1| = {c2:.1e}", c2 <= 1e-12)

    LN.banner("R1  BEFORE / AFTER: P/P_LCDM in the forest band (k = 1-4 h/Mpc), L346's [0.8, 1.2] rule at x_c = 5")
    SB = score(C, C["lcdm"])
    SA = score({k: runs[f"fix/{k}"] for k in CFG}, C["lcdm"])
    dcom = max(abs(SB["gate"][k][i] - R46["F2"][k][i]) for k in R46["F2"] for i in (0, 1))
    for k in SB["gate"]:
        P(f"    {k:18s} before {SB['gate'][k][0]:.2f}-{SB['gate'][k][1]:.2f}   after {SA['gate'][k][0]:.2f}-{SA['gate'][k][1]:.2f}")
    F1a = {n: runs[f"fix/{n}"]["diag"] for n in ("sw5_canon", "sw5_phantomx", "sw5_smooth08")}
    for n in F1a:
        P(f"    F1 {n:13s} mass fraction switched on / median |g_N|/a0 there, z = 6, 3, 2: before " + ", ".join(
            f"{R46['F1'][n][z][0]:.3f}/{R46['F1'][n][z][1]:.2e}" for z in ("6.0", "3.0", "2.0")) + "   after " + ", ".join(
            f"{F1a[n][z][0]:.3f}/{F1a[n][z][1]:.2e}" for z in ("6.0", "3.0", "2.0")))
    P(f"    F3 mean |ratio - 1| at z = 3: before {SB['F3']}  after {SA['F3']}")
    P(f"    (before recomputed from the committed arrays equals L346's committed F2 to {dcom:.0e})")
    LN.out["numbers"]["R1"] = dict(before=SB, after=SA, F1_after=F1a, F2_before="PASS" if SB["passes"] else "FAIL",
                                   F2_after="PASS" if SA["passes"] else "FAIL")
    LN.check("R1 (reported) L346's F2 ([0.8, 1.2] at x_c = 5, both footings), C3, F3 with the corrected argument",
             f"F2 worst {SB['worst']:.2f} ({'PASS' if SB['passes'] else 'FAIL'}) -> {SA['worst']:.2f} ({'PASS' if SA['passes'] else 'FAIL'}); "
             f"C3 no-switch z = 3 min {SB['C3_min_z3']:.2f} -> {SA['C3_min_z3']:.2f}; F3 smooth <= mesh {SB['F3_ok']} -> {SA['F3_ok']}",
             True, load_bearing=False)
    LN.check("H1 (reported) the pre-declared hypothesis H-L346: F2's FAIL does not flip", f"F2 {'PASS' if SA['passes'] else 'FAIL'} after",
             not SA["passes"], "a failed hypothesis is kept as run", load_bearing=False)

    LN.banner("VERDICT")
    P(f"""  With ONLY the kernel argument corrected, L346's forest-band matter power at x_c = 5 fails by more: worst |P/P_LCDM - 1|
  {SB['worst']:.2f} -> {SA['worst']:.2f} ({'PASS' if SA['passes'] else 'FAIL'}).  (L347 showed the flux observable absorbs most of this excess; see
  XR34_rescore_L347.)  Controls: committed line reproduces L346 to {c1:.0e} (C1); MOND off reproduces the LCDM box to {c2:.0e} (C2).""")
    sys.exit(LN.finish())
