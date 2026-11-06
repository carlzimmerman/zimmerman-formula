#!/usr/bin/env python3
"""QX11: FG1's C4 (law alone) gate set regraded on the action's exact AQUAL field. Criteria: FROZEN_CRITERIA.md
(610ce3a4ef). Reuses QX8's loader, fitter and solved parts read-only. kappa = 1/2 FITTED; not theory closed.
Footings never pooled.

Run from the repo root:
  OMP_NUM_THREADS=1 nice -n 15 python3 closure_2026_11_06/QX11_fg1_tilt_exact/qx11.py           -> qx11.out / qx11.json
  OMP_NUM_THREADS=1 nice -n 15 python3 closure_2026_11_06/QX11_fg1_tilt_exact/qx11.py --mutate  -> qx11_MUTATE.out / .json
"""
import os, sys, json, math, pickle
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(REPO, "closure_2026_11_06", "QX8_sparc_exact_field"))
import qx8 as Q8                                                   # noqa: E402  (read-only import)

MUTATE = "--mutate" in sys.argv
tag = "_MUTATE" if MUTATE else ""
A0 = dict(canonical=9.3603e-11, alt=1.1312e-10)                    # FG1's law-tail values
UPS, NODES = Q8.UPS, Q8.NODES
lU, lN = np.log(UPS), np.log(NODES)
NBOOT, SEED = 4000, 20261106
OUT = []
P = lambda s="": (print(s, flush=True), OUT.append(str(s)))

FG1 = json.load(open(os.path.join(REPO, "rebuild_2026_10_22", "FG1_final_grade", "fg1law_RUN_results.json")))
Q8J = json.load(open(os.path.join(REPO, "closure_2026_11_06", "QX8_sparc_exact_field", "qx8.json")))
Q9J = json.load(open(os.path.join(REPO, "closure_2026_11_06", "QX9_vflat_tilt", "qx9.json")))
SL1 = pickle.load(open(os.path.join(REPO, "rebuild_2026_10_22", "SL1_symbolic_law_search", "cache", "sl1_cache.pkl"), "rb"))
BIN = ((20, 60), (60, 100), (100, 150), (150, 200), (200, 250), (250, 400))

# FG1's C4 cells that the exact field cannot move (spherical / point models, or already a full AQUAL row); README literals.
CARRIED = {
    "canonical": dict(G="PASS Z +0.31 [FG1 NR2]",
                      K="FAIL 9 of 15; worst G-MID-T3 +4.46 [FG1 NR2]",
                      X="NOT GRADED (CS2 law on record -0.151, 0.205) [FG1]",
                      Ln="PASS ENV2H-L2H +0.0, ENV2H-H2H -463.6 [FG1 NR2]",
                      Dw="FAIL MW ultra-faint +5.22; bright M31 +2.20; M31 others +2.29; MW classical +1.69 [FG1 NR2]",
                      MW="FAIL feasible only in wide priors; K_z +4.7 to +6.6 sigma [FG1 READ X5, already AQUAL]",
                      DM="NOT GRADED [FG1]",
                      IC="FAIL E -0.593 (Z -7.9) [FG1 READ ND1, RF2; carried by argument]"),
    "alt": dict(G="PASS Z -0.31 [FG1 NR2]",
                K="FAIL (10 keys over 2 in either h); worst G-MID-T3 +4.11 [FG1 NR2]",
                X="NOT GRADED (CS2 law on record -0.151, 0.205) [FG1]",
                Ln="PASS ENV2H-L2H +0.0, ENV2H-H2H -492.9 [FG1 NR2]",
                Dw="FAIL MW ultra-faint +4.87; M31 others +2.12 [FG1 NR2]",
                MW="FAIL feasible only in wide priors [FG1 READ X5, already AQUAL]",
                DM="NOT GRADED [FG1]",
                IC="FAIL E -0.593 (Z -7.9) [FG1 READ ND1, RF2; carried by argument]"),
}


def nu(gN, a0):
    return 0.5 + np.sqrt(0.25 + a0 / np.maximum(gN, 1e-300))


def lt_law(a0):
    C = SL1["const"]; E = []
    for r_ in SL1["lt"]:
        R_ = r_["R"] * C["MPCE"] / 1e3; gN = C["GE"] * 10 ** r_["logMb"] * C["MSUNE"] / R_ ** 2
        E.append(math.log10((r_["V"] * 1e3) ** 2 / R_) - math.log10(gN * float(nu(np.array(gN), a0))))
    return float(np.median(E))


def tilt(rows, uk):
    lo = np.array([p[uk] for p in rows if p["good"] and 0 < p["Vflat"] < 100])
    hi = np.array([p[uk] for p in rows if p["good"] and p["Vflat"] > 150])
    return float(np.median(lo) - np.median(hi)), lo, hi


def boot(lo, hi, rng):
    t = np.array([np.median(lo[rng.integers(0, len(lo), len(lo))]) - np.median(hi[rng.integers(0, len(hi), len(hi))])
                  for _ in range(NBOOT)])
    return float(np.std(t)), t


def main():
    GALS = Q8.load_sparc(); n = len(GALS)
    rng = np.random.default_rng(SEED)
    P(f"QX11 FG1 C4 gate set on the exact field{' -- MUTATE (g_obs x1.5 at 0<Vflat<100)' if MUTATE else ''}. "
      f"kappa = 1/2 FITTED; not theory closed. n galaxies {n}.")
    RES = dict(lane="QX11", criteria="610ce3a4ef", mutate=MUTATE, footings={})
    ka_ok = True; tl_fail_mut = []
    for foot, a0 in A0.items():
        parts = [dict(np.load(os.path.join(Q8.PARTS, foot, f"{i:03d}.npz"), allow_pickle=False)) for i in range(n)]
        rows = []; fl, fe = [], []
        for q, pt in zip(GALS, parts):
            m = q["meta"]
            if MUTATE and 0 < m["Vflat"] < 100:
                q = dict(q, GO=q["GO"] * 1.5)
            lgl = np.log10(np.maximum(nu(q["GB"], a0) * q["GB"], 1e-300))
            Tf = np.array([np.interp(lU, lN, pt["T"][:, j]) for j in range(pt["T"].shape[1])])
            lge = lgl + Tf
            rl = Q8.fit_one(q, lgl); re_ = Q8.fit_one(q, lge); fl.append(rl); fe.append(re_)
            rows.append(dict(name=q["name"], Vflat=m["Vflat"], good=bool(m["Q"] <= 2 and m["Inc"] >= 30),
                             U_law=float(UPS[rl[2]]), U_ex=float(UPS[re_[2]])))
        Sl, Se = Q8.pooled(fl), Q8.pooled(fe)
        tl, lol, hil = tilt(rows, "U_law"); te, loe, hie = tilt(rows, "U_ex")
        sd_e, bs_e = boot(loe, hie, rng); sd_l, _ = boot(lol, hil, rng)
        bins = {f"{l}-{h}": float(np.median([p["U_ex"] for p in rows if p["good"] and l <= p["Vflat"] < h])) for l, h in BIN}
        ltl = lt_law(a0)
        F = dict(S_law=Sl, S_exact=Se, S_exact_line=Q8.line(Se), tilt_law=tl, tilt_exact=te, tilt_exact_boot_sd=sd_e,
                 tilt_law_boot_sd=sd_l, frac_boot_over_line=float(np.mean(np.abs(bs_e) > 0.15)),
                 n_lo=int(len(loe)), n_hi=int(len(hie)), medU_lo_exact=float(np.median(loe)), medU_hi_exact=float(np.median(hie)),
                 bins_exact=bins, LT_law=ltl, LT_exact=ltl, Tl_label="PASS" if abs(te) <= 0.15 else "FAIL")
        P(f"\n[{foot}] a0 {a0:.4e}")
        P(f"  S  law   rms {Sl['rms']:.4f} U {Sl['U_median']:.2f} line {Q8.line(Sl)}")
        P(f"  S  exact rms {Se['rms']:.4f} U {Se['U_median']:.2f} line {Q8.line(Se)} -> {'PASS' if Q8.line(Se) else 'FAIL'}")
        P(f"  Tl law   {tl:+.3f} (boot sd {sd_l:.3f})")
        P(f"  Tl exact {te:+.3f} (boot sd {sd_e:.3f}; {100*F['frac_boot_over_line']:.1f}% of draws |t|>0.15); "
          f"median U lo {F['medU_lo_exact']:.3f} (n {len(loe)}), hi {F['medU_hi_exact']:.3f} (n {len(hie)}) -> {F['Tl_label']}")
        P(f"  Tl bins exact (median U): " + ", ".join(f"{k} {v:.3f}" for k, v in bins.items()))
        P(f"  LT law {ltl:+.4f}; exact = law (point-mass statistic, spherical identity) -> {'PASS' if abs(ltl) <= 0.10 else 'FAIL'}")
        if not MUTATE:
            ref = FG1[foot]["A_c2b_refit"]
            ka1 = abs(tl - ref["tilt"]) <= 1e-9 and abs(Sl["U_median"] - ref["U"]) <= 1e-9
            ka2 = abs(ltl - ref["lt"]) <= 1e-4
            ka3 = abs(Se["rms"] - Q8J["footings"][foot]["exact"]["rms"]) <= 1e-9 and abs(Se["U_median"] - Q8J["footings"][foot]["exact"]["U_median"]) <= 1e-9
            ka4 = abs(te - Q9J["footings"][foot]["FG1_U_tilt_ex"]) <= 1e-9
            F["KA"] = dict(KA1=ka1, KA2=ka2, KA3=ka3, KA4=ka4)
            P(f"  KA1 law tilt/U vs FG1 {ref['tilt']:+.3f}/{ref['U']:.2f}: {'PASS' if ka1 else 'FAIL'}")
            P(f"  KA2 law LT vs FG1 {ref['lt']:+.5f}: {'PASS' if ka2 else 'FAIL'} (|d| {abs(ltl-ref['lt']):.1e})")
            P(f"  KA3 exact S vs QX8: {'PASS' if ka3 else 'FAIL'}")
            P(f"  KA4 exact tilt vs QX9 {Q9J['footings'][foot]['FG1_U_tilt_ex']:+.3f}: {'PASS' if ka4 else 'FAIL'}")
            ka_ok &= ka1 and ka2 and ka3 and ka4
            fails = [k for k, ok in (("S", Q8.line(Se)), ("Tl", abs(te) <= 0.15), ("LT", abs(ltl) <= 0.10)) if not ok]
            fails += [k for k, v in CARRIED[foot].items() if v.startswith("FAIL")]
            ng = [k for k, v in CARRIED[foot].items() if v.startswith("NOT GRADED")]
            F["C4_exact"] = dict(label="PASSES EVERY GRADED LINE" if not fails else "FAILS", failed=fails, not_graded=ng, carried=CARRIED[foot])
            P(f"  carried (exact = law or already AQUAL): " + "; ".join(f"{k}: {v}" for k, v in CARRIED[foot].items()))
            P(f"  C4 on the exact field [{foot}]: {F['C4_exact']['label']}, failed {fails}, NOT GRADED {ng}")
        else:
            if abs(te) <= 0.15:
                tl_fail_mut.append(foot)
        RES["footings"][foot] = F
    if MUTATE:
        bites = not tl_fail_mut
        P(f"\nMUTATE: planted trend {'caught (Tl > 0.15) on both footings: BITES' if bites else 'NOT caught on ' + str(tl_fail_mut) + ': NO POWER'}")
        RES["mutate_bites"] = bites
    else:
        RES["known_answers_ok"] = ka_ok
        c = RES["footings"]["canonical"]["Tl_label"]
        P(f"\nKnown answers: {'all PASS' if ka_ok else 'FAILED -> NO VERDICT'}")
        if ka_ok and c == "FAIL":
            P("Plainly: the a0 law as an algebraic law passes FG1's tilt row; the action's exact AQUAL solution FAILS it on the canonical footing.")
    P("kappa = 1/2 FITTED; not theory closed.")
    json.dump(RES, open(os.path.join(HERE, f"qx11{tag}.json"), "w"), indent=1, default=float)
    open(os.path.join(HERE, f"qx11{tag}.out"), "w").write("\n".join(OUT) + "\n")
    if MUTATE and not RES["mutate_bites"]:
        sys.exit(0)
    if MUTATE:
        sys.exit(1)
    sys.exit(0 if ka_ok else 2)


if __name__ == "__main__":
    main()
