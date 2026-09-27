#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
XR9_gate_table.py -- THE SMALL-REGION DOOR: every gate for every cell, the all-pass cells (if any), the pinch, and the
pre-declared hypothesis scored.  Bookkeeping only: it reads the three XR9 results files (no physics is computed here).

THE GATES per cell (p in {1, 1.5}, x_c0 in {2.5, 3.5, 5, 7, 10, 14, 20}; w = 0.25; MS5's kappa cap; both footings in every
gate), as defined in the three scripts before their scans:
  1 KiDS      XR9_kids_flagship: fs = 1 (the carrier's own post-trigger halo), 2-halo amplitude A <= 2, v_k = 600 and 650,
              Delta chi^2 <= +4 against the unswitched model;
  2 flagship  XR9_kids_flagship: z = 2.5, M_b = 1e10-1e11.5, MS2's door at r_F with the kappa cap AND DE9's smooth shift
              >= -0.05 dex;
  3 LG        XR9_environment: R_0 within +-0.10 dex of 0.96 Mpc for the model's own carrier history, some M_b;
  4 EFE-C     XR9_environment: every operator-A (kappa) variant's slope within 2 sigma, no new failure ('central' beside);
  4 EFE-D     XR9_environment: statistic C within 2 sigma for host baryons x1-x2;
  5 UDG       XR9_environment: Coma UDGs below 2 sigma for every gap and kappa reading;
  6 shear     XR9_cosmic_shear: with the kappa cap, R(k) within 20% of LCDM at k = 0.1-1 h/Mpc, 0.8 <= R <= 1.2 (the gate
              as MS3 states it, "within 20%"; MS3/MS4's code checks only the upper side, R <= 1.2, shown beside it -- the two
              differ only where the kicked carrier's missing small-scale power is no longer masked by the phantom);
  7 RC        XR9_environment: every SPARC galaxy's fully-on radius >= 3 R_last;
  + forest    by monotonicity from DE11 (not a computed column).
PRE-DECLARED HYPOTHESIS H (XR9_kids_flagship's docstring): some cell above the switch-only KiDS cap passes KiDS with the
carrier AND at that cell the LG and the cluster-infall EFE slope are in their bands.  Scored here, reported either way.
CHECKS
  T0 [load-bearing] the three results files are present, cover all 14 cells, and none has a load-bearing failure.
  T1 [load-bearing; MUTATE must fail] the KiDS column carries the carrier: at every cell the gated Delta chi^2 differs
     from the switch-only one by > 1 (read from the KiDS results; MUTATE reads XR9_kids_flagship_results_MUTATE.json,
     whose gated column IS the switch-only one).
  H (reported) the pre-declared hypothesis; A (reported) the all-pass cells; PINCH (reported) which gates exclude each other.
MUTATE=1: the table is built from the KiDS MUTATE run (the carrier's lensing off): the switch-only table, T1 FAILS (rc = 1).

Run from the repository root:  python3 real_research/cross_thread_review_2026_09_26/XR9_gate_table.py   (MUTATE=1)
"""
import os, sys, json, itertools

HERE = os.path.dirname(os.path.abspath(__file__))
MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "XR9_gate_table"
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "XR9 gate table", "mutate": MUTATE, "checks": {}, "numbers": {}}
PS = (1.0, 1.5)
XC0S = (2.5, 3.5, 5.0, 7.0, 10.0, 14.0, 20.0)
KEYS = [f"p{p:g}_x{x0:g}" for p in PS for x0 in XC0S]
SO_CAP = 4.347265625000002


def check(name, measured, ok, load_bearing=True):
    ok = bool(ok); CH.append((name, ok, load_bearing))
    OUT["checks"][name.split()[0]] = {"pass": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}]{'' if load_bearing else ' (reported)'} {name}\n         measured: {measured}")


if __name__ == "__main__":
    P(__doc__.split("CHECKS")[0].strip())
    if MUTATE: P("\n  *** MUTATE=1: the KiDS column is read from the carrier-off run; T1 must FAIL ***")
    fk = os.path.join(HERE, "XR9_kids_flagship_results" + ("_MUTATE" if MUTATE else "") + ".json")
    files = {"kids": fk, "shear": os.path.join(HERE, "XR9_cosmic_shear_results.json"),
             "env": os.path.join(HERE, "XR9_environment_results.json")}
    R = {k_: json.load(open(v_)) for k_, v_ in files.items() if os.path.exists(v_)}
    ok0 = len(R) == 3
    if ok0:
        ok0 = (all(k_ in R["kids"]["numbers"]["kids"] and k_ in R["kids"]["numbers"]["flagship"] for k_ in KEYS)
               and all(k_ in R["shear"]["numbers"]["table"] for k_ in KEYS)
               and all(k_ in R["env"]["numbers"][s_] for k_ in KEYS for s_ in ("LG", "clusters", "dwarfs", "udg", "rotation_curves"))
               and R["shear"]["n_fail_load_bearing"] == 0 and R["env"]["n_fail_load_bearing"] == 0
               and (R["kids"]["n_fail_load_bearing"] == 0 or MUTATE))
    check("T0 the three XR9 results files are present, cover all 14 cells, and have no load-bearing failure (the KiDS MUTATE run "
          "fails M1 by design)", {k_: os.path.basename(v_) for k_, v_ in files.items()}, ok0)
    if not ok0:
        sys.exit(1)
    K, FL, SH = R["kids"]["numbers"]["kids"], R["kids"]["numbers"]["flagship"], R["shear"]["numbers"]["table"]
    LG, CL, DW, UD, RC = (R["env"]["numbers"][s_] for s_ in ("LG", "clusters", "dwarfs", "udg", "rotation_curves"))
    FEET = ("canonical", "alt")
    T = {}
    for k_ in KEYS:
        kd = K[k_]["kids"]
        worst_k = max(kd[f"w0.25/v{v}/{f}"]["gate"]["dchi2"] for v in (600, 650) for f in FEET)
        worst_so = max(kd[f"w0.25/v600/{f}"]["switch_only_A2"]["dchi2"] for f in FEET)
        diff_min = min(abs(kd[f"w0.25/v600/{f}"]["gate"]["dchi2"] - kd[f"w0.25/v600/{f}"]["switch_only_A2"]["dchi2"]) for f in FEET)
        T[k_] = {
            "xce_025": K[k_]["xce_025"],
            "KiDS": K[k_]["pass"], "KiDS_worst": worst_k, "KiDS_switch_only_worst": worst_so, "KiDS_carrier_shift_min": diff_min,
            "KiDS_A20": K[k_]["pass_A20"], "KiDS_hard": K[k_]["pass_hard"],
            "flagship": FL[k_]["pass_"], "flagship_to_1e11": FL[k_]["pass_upto_1e11"], "flagship_lost": FL[k_]["masses_lost"],
            "LG": LG[k_]["pass_"], "LG_dex_decay": [min(LG[k_]["dex_decay"].values()), max(LG[k_]["dex_decay"].values())],
            "EFE_clusters": CL[k_]["pass_"], "EFE_clusters_central": CL[k_]["pass_central"], "EFE_clusters_sigma": CL[k_]["sigma_range"],
            "EFE_new_failures": CL[k_]["new_failures"],
            "EFE_dwarfs": DW[k_]["pass_"], "EFE_dwarfs_sigma": DW[k_]["sigma_range"],
            "UDG": UD[k_]["pass_"], "UDG_sigma": UD[k_]["sigma_range"],
            "shear": SH[k_]["two_sided_capped"], "shear_one_sided": SH[k_]["pass_capped"], "shear_worst": max(SH[k_]["capped"].values()),
            "shear_min": min(SH[k_]["capped_min"].values()), "shear_uncapped": SH[k_]["pass_uncapped"],
            "RC": RC[k_]["pass_"], "RC_min_ratio": RC[k_]["min_ratio"],
            "forest": True,
        }
    GATES = ("KiDS", "flagship", "LG", "EFE_clusters", "EFE_dwarfs", "UDG", "shear", "RC", "forest")
    P("\n  cell       x(0.25) | KiDS (worst)   | flag | LG (decay dex)   | EFE-C (sigma)    | EFE-D (sigma) | UDG (sigma)  | shear (R min-max)  | RC")
    for k_ in KEYS:
        t = T[k_]; y = lambda b: "PASS" if b else "fail"
        P(f"  {k_:9s} {t['xce_025']:6.2f}  | {y(t['KiDS'])} {t['KiDS_worst']:+6.1f} | {y(t['flagship'])} | {y(t['LG'])} "
          f"{t['LG_dex_decay'][0]:+.2f}..{t['LG_dex_decay'][1]:+.2f} | {y(t['EFE_clusters'])} {t['EFE_clusters_sigma'][0]:.1f}-"
          f"{t['EFE_clusters_sigma'][1]:.1f}{'' if t['EFE_new_failures'] == 0 else ' NF'}   | {y(t['EFE_dwarfs'])} "
          f"{t['EFE_dwarfs_sigma'][0]:.1f}-{t['EFE_dwarfs_sigma'][1]:.1f}  | {y(t['UDG'])} {t['UDG_sigma'][0]:.1f}-{t['UDG_sigma'][1]:.1f} "
          f"| {y(t['shear'])} {t['shear_min']:.2f}-{t['shear_worst']:.2f}{'' if t['shear_one_sided'] else ' (>1.2)'} | {y(t['RC'])} {t['RC_min_ratio']:.1f}")
    OUT["numbers"]["table"] = T
    shift = min(t["KiDS_carrier_shift_min"] for t in T.values())
    check("T1 THE KiDS COLUMN CARRIES THE CARRIER: at every cell the gated Delta chi^2 differs from the switch-only one by > 1 "
          "(MUTATE, the carrier-off run, must fail this)", f"smallest difference {shift:.2f}", shift > 1.0)
    kc = R["kids"]["numbers"].get("kids_cap_with_carrier", {})
    P("\n  the KiDS cap itself (w = 0.25, A <= 2, both kicks and footings): " + "; ".join(
        f"{k_}: x_c,eff(0.25) <= {v_['cap']:.4f} (x_c0 <= {v_['x_c0_max_p1']:.3f} at p = 1, {v_['x_c0_max_p15']:.3f} at p = 1.5)"
        if v_.get("cap") else f"{k_}: no crossing" for k_, v_ in kc.items()) + f"; switch only (DE9): {SO_CAP:.4f}")
    OUT["numbers"]["kids_cap_with_carrier"] = kc
    allpass = [k_ for k_ in KEYS if all(T[k_][g] for g in GATES)]
    passing = {g: [k_ for k_ in KEYS if T[k_][g]] for g in GATES}
    hyp = [k_ for k_ in KEYS if T[k_]["xce_025"] > SO_CAP and T[k_]["KiDS"] and T[k_]["LG"] and T[k_]["EFE_clusters"]]
    hyp_c = [k_ for k_ in KEYS if T[k_]["xce_025"] > SO_CAP and T[k_]["KiDS"] and T[k_]["LG"] and T[k_]["EFE_clusters_central"]]
    check("H (pre-declared, reported) some cell above the switch-only KiDS cap passes KiDS with the carrier AND puts the LG's R_0 and "
          "the cluster-infall EFE slope in their bands", f"cells: {hyp or 'none'} (with the EFE gate at its central systematics only: "
          f"{hyp_c or 'none'})", len(hyp) > 0, load_bearing=False)
    check("A (reported) the cells that pass all seven gates (+ the forest) on both footings", allpass or "none", True, load_bearing=False)
    pinch = []
    for g1, g2 in itertools.combinations(GATES, 2):
        if passing[g1] and passing[g2] and not set(passing[g1]) & set(passing[g2]):
            pinch.append(f"{g1} x {g2}")
    never = [g for g in GATES if not passing[g]]
    check("PINCH (reported) the gates passing at no cell, and the pairs whose passing sets are disjoint",
          f"never passing: {never or 'none'}; disjoint pairs: {pinch or 'none'}; passing sets: {passing}", True, load_bearing=False)
    OUT["numbers"].update(all_pass=allpass, passing_by_gate=passing, hypothesis_cells=hyp, hypothesis_cells_central=hyp_c,
                          never_passing=never, disjoint_pairs=pinch)
    nlb = sum(1 for _, ok, lb in CH if lb and not ok)
    OUT["n_checks"], OUT["n_fail_load_bearing"] = len(CH), nlb
    fn = os.path.join(HERE, SLUG + ("_results_MUTATE.json" if MUTATE else "_results.json"))
    json.dump(OUT, open(fn, "w"), indent=1, default=str)
    P(f"\n  {sum(ok for _, ok, _ in CH)}/{len(CH)} checks pass; load-bearing failures: {nlb}; wrote {os.path.basename(fn)}")
    sys.exit(1 if nlb else 0)
