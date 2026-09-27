#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
XR34_rescore_L347 -- L347's forest-observable verdict re-scored with ONLY the MOND kernel's argument corrected.

L347 AS COMMITTED.  L342's constant-threshold switch (matter reading) on the 1D flux power, 50 and 25 Mpc/h boxes
(128^3 mesh, 96^3 particles, CLASS to 40 h/Mpc, seed 7).  F2: at x_c = 5 the worst |P1D/P1D_LCDM - 1| (k_par 0.2-2,
z = 3 and 2, both footings, both boxes) = 0.108 -> FAILS the 10% rule, BORDERLINE (< 0.15); x_c = 7: 0.072 (inside).
F3: the observable absorbs most of the matter-power excess (flux < half of matter).  Its kernel line reads |grad phi|/a^2.

METHOD.  L347's committed source executed read-only with that ONE line changed to |grad phi|/a (XR34_common).  Runs:
  'fix'  (after):   both boxes x (sw5_canon, sw5_alt, sw7_canon)
  'none' (control): L25_sw5_alt (L347's worst cell) and L25_sw7_canon (its x_c = 7 cell)
  LCDM:             L25_lcdm re-run; every ratio uses L347's committed LCDM arrays (P1D and matter power)
PRE-DECLARED (before any XR34 run; XR34_README 'Hypotheses')
  H-L347: x_c = 5 still FAILS and no longer as 'borderline' (worst >= 0.15); x_c = 7 FLIPS from pass to FAIL (> 0.10).
CHECKS
  K1 [load-bearing] L347's own accel() with the corrected line reproduces the analytic single-halo QUMOND profile (2%).
  C1 [load-bearing] the committed line re-run reproduces L347's committed P1D arrays (L25_sw5_alt, L25_sw7_canon) to 1e-12.
  C2 [load-bearing] MOND off: the L25_lcdm re-run equals L347's committed LCDM P1D to 1e-12.
  R1 (reported) F2 (x_c = 5, the 10% rule and the < 0.15 'borderline' band), x_c = 7, F1/F3 (matter power, translation)
     before / after.
  H1, H2 (reported) whether H-L347's two parts held.
MUTATE=1: 'double' stands in for the corrected line in K1 -> K1 FAILS (rc = 1); no PM run.

Run from the repository root (MUTATE=1 first):  python3 real_research/cross_thread_review_2026_09_26/XR34_rescore_L347.py
"""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import XR34_common as X                                                 # noqa: E402
import numpy as np                                                      # noqa: E402

MUTATE = os.environ.get("MUTATE", "0") == "1"
FIX = "double" if MUTATE else "fix"
LANE = "L347"
LN = X.Lane("XR34_rescore_L347", MUTATE)
P = LN.P
CFG = {f"L{int(L)}_{nm}": (L, "switch", f, xc) for L in (50.0, 25.0)
       for nm, f, xc in (("sw5_canon", "canonical", 5.0), ("sw5_alt", "alt", 5.0), ("sw7_canon", "canonical", 7.0))}
NONE = ("L25_sw5_alt", "L25_sw7_canon")
ZZ = ("3.0", "2.0")


def score(runs, lcdm):
    """L347's F1/F2/F3 arithmetic, line for line, on a set of runs {name: out} with LCDM references {box: out}."""
    F2, F1 = {}, {}
    for t in ("L50", "L25"):
        for nm in ("sw5_canon", "sw5_alt", "sw7_canon"):
            for z in ZZ:
                kp = np.array(lcdm[t][z]["kpar"]); r = np.array(runs[f"{t}_{nm}"][z]["p1d"]) / np.array(lcdm[t][z]["p1d"])
                m = (kp >= 0.2) & (kp <= 2.0)
                F2[(t, nm, z)] = (float(r[m].min()), float(r[m].max()))
        for z in ZZ:
            kk3 = np.array(lcdm[t][z]["pk3"])[:, 0]
            r = np.array(runs[f"{t}_sw5_canon"][z]["pk3"])[:, 1] / np.array(lcdm[t][z]["pk3"])[:, 1]
            m = (kk3 >= 1.0) & (kk3 <= 4.0)
            F1[(t, z)] = (float(r[m].min()), float(r[m].max()))
    dev = {k_: max(abs(v[0] - 1), abs(v[1] - 1)) for k_, v in F2.items()}
    worst5 = max(dev[(t, n, z)] for t in ("L50", "L25") for n in ("sw5_canon", "sw5_alt") for z in ZZ)
    x7 = max(dev[(t, "sw7_canon", z)] for t in ("L50", "L25") for z in ZZ)
    wc = max(dev[(t, "sw5_canon", z)] for t in ("L50", "L25") for z in ZZ)
    mat5 = max(max(abs(F1[(t, z)][0] - 1), abs(F1[(t, z)][1] - 1)) for t in ("L50", "L25") for z in ZZ)
    return dict(F2={f"{t}_{n}_{z}": v for (t, n, z), v in F2.items()}, dev={f"{t}_{n}_{z}": v for (t, n, z), v in dev.items()},
                F1={f"{t}_{z}": v for (t, z), v in F1.items()}, worst5=worst5, x7=x7, worst5_canonical=wc, mat5=mat5,
                passes=worst5 <= 0.10, borderline=(worst5 > 0.10 and worst5 < 0.15), x7_passes=x7 <= 0.10,
                translation=(mat5 >= 0.2 and worst5 < 0.5 * mat5))


if __name__ == "__main__":
    P(__doc__.split("PRE-DECLARED")[0].strip())
    if MUTATE:
        P("\n  *** MUTATE=1: 'double' stands in for the corrected line; K1 must FAIL; no PM run ***")
    R47 = json.load(open(os.path.join(X.G03, "L347_switch_forest_flux_power_results.json")))["numbers"]

    LN.banner("K1  THE ARGUMENT: L347's own accel() on the analytic single halo")
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

    LN.banner("THE RUNS (L347's run(), one line patched; wall time and peak memory per run)")
    jobs = ([(LANE, "fix", (k,) + CFG[k]) for k in ("L25_sw5_alt", "L25_sw5_canon", "L25_sw7_canon", "L50_sw5_alt", "L50_sw5_canon",
                                                   "L50_sw7_canon")]
            + [(LANE, "none", ("L25_lcdm", 25.0, "lcdm", "canonical", 0))] + [(LANE, "none", (k,) + CFG[k]) for k in NONE])
    res = X.run_jobs(jobs, log=P)
    runs = {f"{p_}/{n_}": r["out"] for (l_, p_, n_), r in res.items()}
    LN.out["numbers"]["runs"] = runs
    LN.out["numbers"]["run_times"] = {f"{p_}/{n_}": dict(wall_s=round(r["wall_s"]), peak_rss_gb=round(r["peak_rss_gb"], 2))
                                      for (l_, p_, n_), r in res.items()}
    C = R47["runs"]

    LN.banner("C1 C2  CONTROLS: the committed line reproduces L347; MOND off reproduces the LCDM box")
    c1 = max(X.max_abs_diff_p1d(runs[f"none/{k}"], C[k]) for k in NONE)
    LN.check("C1 the committed line re-run reproduces L347's committed P1D arrays (L25_sw5_alt, L25_sw7_canon; 1e-12)",
             f"max |P1D ratio - 1| = {c1:.1e}", c1 <= 1e-12, "the harness is L347 exactly; only the kernel line differs in 'fix'")
    c2 = X.max_abs_diff_p1d(runs["none/L25_lcdm"], C["L25_lcdm"])
    c2m = max(float(np.max(np.abs(np.array(runs["none/L25_lcdm"][z]["pk3"])[:, 1] / np.array(C["L25_lcdm"][z]["pk3"])[:, 1] - 1))) for z in ZZ)
    LN.check("C2 MOND off: the L25_lcdm re-run equals L347's committed LCDM P1D (1e-12)", f"P1D {c2:.1e}; matter power {c2m:.1e}",
             max(c2, c2m) <= 1e-12)

    LN.banner("R1  BEFORE / AFTER: L347's F2 (10% rule at x_c = 5, 'borderline' < 0.15), x_c = 7, F1/F3")
    lcdm = {"L50": C["L50_lcdm"], "L25": C["L25_lcdm"]}
    SB = score({k: C[k] for k in CFG}, lcdm)
    SA = score({k: runs[f"fix/{k}"] for k in CFG}, lcdm)
    dcom = abs(SB["worst5"] - R47["verdict"]["worst_dev_xc5"])
    for k in SB["dev"]:
        P(f"    {k:22s} before {SB['dev'][k]:.3f} ({SB['F2'][k][0]:.3f}-{SB['F2'][k][1]:.3f})   after {SA['dev'][k]:.3f} "
          f"({SA['F2'][k][0]:.3f}-{SA['F2'][k][1]:.3f})")
    for k in SB["F1"]:
        P(f"    matter power sw5_canon {k:8s} k = 1-4 h/Mpc: before {SB['F1'][k][0]:.2f}-{SB['F1'][k][1]:.2f}   after {SA['F1'][k][0]:.2f}-{SA['F1'][k][1]:.2f}")
    P(f"    (before recomputed from the committed arrays equals L347's committed worst_dev_xc5 to {dcom:.0e})")
    lab = lambda S: "PASS" if S["passes"] else ("FAIL, borderline (< 0.15)" if S["borderline"] else "FAIL (>= 0.15)")
    LN.out["numbers"]["R1"] = dict(before=SB, after=SA, F2_before=lab(SB), F2_after=lab(SA))
    LN.check("R1 (reported) L347's F2 at x_c = 5, x_c = 7 and F3 with the corrected argument",
             f"x_c = 5 worst {SB['worst5']:.3f} ({lab(SB)}) -> {SA['worst5']:.3f} ({lab(SA)}); canonical alone {SB['worst5_canonical']:.3f} -> "
             f"{SA['worst5_canonical']:.3f}; x_c = 7 {SB['x7']:.3f} -> {SA['x7']:.3f} ({'pass' if SA['x7_passes'] else 'FAIL'}); matter power worst "
             f"{SB['mat5']:.3f} -> {SA['mat5']:.3f}; F3 translation {SB['translation']} -> {SA['translation']}", True, load_bearing=False)
    LN.check("H1 (reported) H-L347 part 1: x_c = 5 still fails and no longer as 'borderline' (worst >= 0.15)",
             f"{SA['worst5']:.3f}", (not SA["passes"]) and SA["worst5"] >= 0.15, "a failed hypothesis is kept as run", load_bearing=False)
    LN.check("H2 (reported) H-L347 part 2: x_c = 7 flips from pass to FAIL (> 0.10)", f"{SB['x7']:.3f} -> {SA['x7']:.3f}",
             SB["x7_passes"] and not SA["x7_passes"], "a failed hypothesis is kept as run", load_bearing=False)

    LN.banner("VERDICT")
    P(f"""  With ONLY the kernel argument corrected, L347's forest observable at x_c = 5 goes {SB['worst5']:.3f} -> {SA['worst5']:.3f}
  ({lab(SB)} -> {lab(SA)}); x_c = 7 goes {SB['x7']:.3f} -> {SA['x7']:.3f} ({'pass' if SB['x7_passes'] else 'FAIL'} -> {'pass' if SA['x7_passes'] else 'FAIL'}).
  Controls: committed line reproduces L347 to {c1:.0e} (C1); MOND off reproduces the LCDM box to {max(c2, c2m):.0e} (C2).""")
    sys.exit(LN.finish())
