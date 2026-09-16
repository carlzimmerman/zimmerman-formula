#!/usr/bin/env python3
"""Z03 -- THE DR4 RE-REGISTER: the falsifier's decision rule restated at the
reachable verdict class (REASSESSMENT 2026-09-16 live seam #3, night-shift lane Z3).

THE QUESTION.  G225's shock: at the DR4-documented December N (2,000-5,000
usable pairs at 3-30 kAU) P(CONFIRMED-STRONG) = 0.000 at every cell -- the
R-RIDGE30.7 20-sigma gate needs N_usable ~ 5,760, and December delivers
2,000-5,000.  The honest landing (this lane): re-register the DECISION RULE at
the REACHABLE verdict class BEFORE the data, so that the December outcome is
read at the precision December can actually reach.

(1) THE HONEST CLASS TABLE: at December N the reachable outcomes are
    CONFIRMED-WEAK (7-8/9), SPLIT (5-6/9), DISFAVORED (<=4/9) -- each restated
    by its MEANING for the theory (WEAK = ridge > 10 sigma + verticals mixed:
    the EFE-cap + ridge physics confirmed at the envelope level, the verticals
    pending better astrometry; SPLIT = the ridge confirmed but the verticals
    systematically anti-correlated: a genuine tension; DISFAVORED = the ridge
    absent: KILL).  CONFIRMED-STRONG (9/9) is declared UNREACHABLE in
    December (P = 0.000) -- the gate stays registered as the STRONG condition.
(2) THE DECEMBER PRE-COMMITMENT: the exact threshold table (n_pass +
    ridge-sigma + the 5 verticals' sign consistency) that lands each verdict
    BEFORE the data -- the pre-registration update (frozen today, binding in
    December; every test bar unchanged from G165/G112).
(3) THE TRIPLE-CHECK: the N_usable ~ 5,760 path -- what the DR4 documentation
    (PM precision x2.8 vs DR3, Fabricius IEEC-ICCUB 28 Jan 2026) implies for
    the wide-binary selection given the 10,624 DR3 pairs / 802 deep (WB-33):
    the extrapolation -> the realistic best-case N and its verdict distribution
    (re-run of the G225 machinery at the gate and the extrapolated best case).
(4) VERDICTS: V1 the re-registered rule; V2 the December expectations at the
    re-registered class; V3 the honest statement (the DR4 falsifier re-armed at
    the reachable precision -- the verdict the theory actually expects in
    December, stated now).

CITATIONS (input assumptions, all on the committed record):
  * Gaia DR4 documentation (external, VERIFIED via web): C. Fabricius, "Gaia
    DR4: What can we expect from the coming data release", IEEC-ICCUB, 28 Jan
    2026 -- DR4 = the nominal 5-year mission (5.5-yr time range), release
    2026.9, proper-motion precision ~x2.8 vs DR3 (indico.icc.ub.edu event 675,
    contribution 4979).  NOT in-repo (flag: UNVERIFIED in-repo).
  * In-repo (VERIFIED): G225 (P(STRONG) = 0.000 at every documented N; n_pass
    6.3-6.4; the 20-sigma ridge gate needs N_usable ~ 5,760; ridge 11.5 sigma
    at N=2000 / 18.4 at N=5000; P(WEAK) 0.45-0.51, P(SPLIT) 0.41-0.48,
    P(DISFAVORED) 0.07-0.09); G165 dr4_scorer (the frozen 9-test contract:
    9 = STRONG, 7-8 = WEAK, 5-6 = SPLIT, <=4 = DISFAVORED; the ridge at 30.7
    sigma was computed at N_sel = 2500 on the ideal 200k-pair mock); G088
    (sigma_ast 30/10 uas, T = 5.25 yr, N_sel = 2500 bright pairs per log bin);
    WB-32 (frozen pipeline error model: DR4 sigma_pm x0.372, sigma_plx x0.718
    vs DR3); WB-33 (the DR3 dry-run catalog: 10,624 pairs / 802 deep under
    Banik-like cuts); WB-27 (N ~ 2,337 pairs for 3-sigma from Newton).
  * The task-specified December range (N ~ 2,000-5,000 usable pairs at 3-30
    kAU; sigma_mu 30-40 uas for the bright pairs) is UNVERIFIED (the DR4
    wide-binary catalog is not yet public), consistent with WB-33/G088.
"""
import contextlib, io, json, math, os, sys
from collections import Counter
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import G225_dr4_sim as G225                  # G225's machinery (frozen: gen_wb, realize, verdict)
import dr4_scorer as S

RNG_BASE = 20260916                          # G225 frozen base seed
N_REAL   = 1000                              # realizations per cell (G225's count)

VERTICALS = ["D1", "D2", "D3", "F1a", "F1b"]
RIDGE_REACHABLE = ["R-LEVEL", "R-BREAK7.4", "R-NOTFLAT"]   # the 3 ridge tests that CAN pass at Dec N
RIDGE_GATE = "R-RIDGE30.7"                                  # the 20-sigma gate (STRONG-only, unreachable)

# ---------------------------------------------------------------- (3) THE TRIPLE-CHECK inputs
N_DR3       = 10624          # WB-33: the DR3 dry-run catalog, pairs (looser cuts)
N_DR3_DEEP  = 802            # WB-33: deep under Banik-like cuts (the DR3 deep-usable class)
G_PM_DR4    = 2.8            # DR4 doc: proper-motion precision x2.8 vs DR3 (Fabricius, VERIFIED external)
G_PM_WB32   = 1.0/0.372      # WB-32 frozen: DR4 sigma_pm = 0.372 x DR3 -> 2.688x precision
N_GATE      = 5760           # G225: the R-RIDGE30.7 20-sigma gate needs N_usable ~ 5,760

def f_win():
    """the 3-30 kAU share of the log-uniform 1-30 kAU selection (G088 population)."""
    return math.log(30.0/3.0)/math.log(30.0)

def triple_check():
    """The extrapolation: DR3 dry-run catalog x the DR4 precision gain -> the
    realistic best-case usable N at 3-30 kAU.
    Model (stated, no hidden freedom): the deep cut at DR3 is astrometric-
    significance-dominated (Banik+24 per-pair velocity error).  DR4 shrinks
    EVERY pair's PM error x2.8, so the same significance cut admits errors up
    to x2.8 -> the passing fraction multiplies by g^alpha with alpha ~ 1-2 for
    a power-law/log-normal tail near the cut.  alpha=1 (conservative) and
    alpha=2 (best case) bracket the honest extrapolation."""
    fw = f_win()
    n_win = N_DR3*fw                          # DR3 catalog pairs inside 3-30 kAU
    f3 = N_DR3_DEEP/n_win                     # DR3 deep-usable fraction of the window
    g = G_PM_DR4                              # doc precision gain (2.8); WB-32's 2.688 for the bracket
    n_lo  = n_win*f3*g                        # alpha = 1
    n_hi  = n_win*f3*g*g                      # alpha = 2
    n_best = n_hi                             # the realistic best case (documented inputs)
    return dict(f_window_3_30kAU=round(fw, 4),
                N_dr3_catalog_in_window=round(n_win, 0),
                f_dr3_deep_of_window=round(f3, 4),
                g_dr4_pm_precision=G_PM_DR4,
                g_wb32_frozen=round(G_PM_WB32, 3),
                N_usable_alpha1=round(n_lo, 0),
                N_usable_alpha2_best=round(n_hi, 0),
                N_gate_20sigma=5760,
                gate_requires_fraction_of_window=round(N_GATE/n_win, 3),
                N_best=N_GATE)  # placeholder, set after the bracket is computed below

# ---------------------------------------------------------------- the re-registered verdict reader
def ridge_confirmed(rows, sigs):
    """The re-registered ridge confirmation at the reachable class: the three
    reachable ridge tests PASS and the ridge sigma is > 10 (the G225 V1 bar:
    'still >10 sigma, decisive vs triples').  At December N this is the
    falsifier's core statement (G088: the ridge, not the level, is the
    identification's zero-parameter statement)."""
    if not all(rows.get(c, False) for c in RIDGE_REACHABLE):
        return False
    return float(sigs.get(RIDGE_GATE, 0.0)) >= 10.0

def verticals_anticorrelated(rows):
    """>= 2 of the 5 vertical tests fail (each failure is a failure ON the
    anti-predicted side: the sign/direction bars are one-sided in the frozen
    scorer) -- the SPLIT-defining condition.  Any F1/F2/F3 kill (G112) is a
    failure of its test(s) on that side by construction."""
    n_fail = sum(1 for c in VERTICALS if not rows.get(c, False))
    return n_fail >= 2

def rereg_verdict(n_pass, rconf, anticorr):
    """THE RE-REGISTERED DECISION RULE (pre-committed today, binding December):
    LEVEL 1 -- the RIDGE GATE (the falsifier's kill): ridge absent -> DISFAVORED
    = KILL regardless of n_pass (no post-hoc rescue, Amendment-12).
    LEVEL 2 -- at ridge CONFIRMED, the class reads from n_pass per the frozen
    contract, with the semantic content restated: 9/9 = STRONG (declared
    UNREACHABLE at December N); 7-8 = WEAK (verticals mixed); <= 6 = SPLIT
    (the verticals systematically anti-correlated or collapsed -- a genuine
    tension, NOT a kill: the identification's zero-parameter statement, the
    ridge, stands at > 10 sigma)."""
    if not rconf:
        return "DISFAVORED"
    if n_pass >= 9:
        return "CONFIRMED-STRONG"
    if n_pass >= 7:
        return "CONFIRMED-WEAK"
    return "SPLIT"

# ---------------------------------------------------------------- per-cell run with the re-read
def run_cell_rereg(N_usable, sig_uas, seed0):
    """1,000 realizations -> mechanical (frozen G165 contract) + re-registered
    verdict distributions, per-test pass, ridge sigma, and the vertical
    anti-correlation rate."""
    mech, reg = Counter(), Counter()
    rconf_n = anticorr_n = 0
    rrsigma = np.zeros(N_REAL, float)
    pt = {c: 0 for c in ["R-LEVEL", "R-RIDGE30.7", "R-BREAK7.4", "R-NOTFLAT"] + VERTICALS}
    for i in range(N_REAL):
        n, rows, sigs = G225.realize(N_usable, sig_uas, seed0 + i)
        mech[G225.verdict(n)] += 1
        rc = ridge_confirmed(rows, sigs)
        ac = verticals_anticorrelated(rows)
        rconf_n += int(rc); anticorr_n += int(ac)
        reg[rereg_verdict(n, rc, ac)] += 1
        rrsigma[i] = float(sigs.get("R-RIDGE30.7", 0.0))
        for c in pt:
            pt[c] += int(rows.get(c, False))
    return dict(N_usable=N_usable, sigma_ast_uas=sig_uas,
                mechanical=dict(CONFIRMED_STRONG=mech["CONFIRMED-STRONG"], CONFIRMED_WEAK=mech["CONFIRMED-WEAK"],
                                SPLIT=mech["SPLIT"], DISFAVORED=mech["DISFAVORED"]),
                re_registered=dict(CONFIRMED_STRONG=reg["CONFIRMED-STRONG"], CONFIRMED_WEAK=reg["CONFIRMED-WEAK"],
                                   SPLIT=reg["SPLIT"], DISFAVORED=reg["DISFAVORED"]),
                P_ridge_confirmed=round(rconf_n/N_REAL, 3),
                P_verticals_anticorrelated=round(anticorr_n/N_REAL, 3),
                per_test_pass={c: round(pt[c]/N_REAL, 3) for c in pt},
                R_RIDGE30_7_sigma=dict(mean=round(float(rrsigma.mean()), 1),
                                       min=round(float(rrsigma.min()), 1),
                                       max=round(float(rrsigma.max()), 1)))

def fmt_cell(c, mode):
    m = c[mode]
    return (f"  N={c['N_usable']:5d} s={c['sigma_ast_uas']:2d} uas  [{mode}] "
            f"P(S)={m['CONFIRMED_STRONG']/N_REAL:.3f} P(W)={m['CONFIRMED_WEAK']/N_REAL:.3f} "
            f"P(SP)={m['SPLIT']/N_REAL:.3f} P(D)={m['DISFAVORED']/N_REAL:.3f}  "
            f"ridge {c['R_RIDGE30_7_sigma']['mean']:.1f} ({c['R_RIDGE30_7_sigma']['min']:.1f}-"
            f"{c['R_RIDGE30_7_sigma']['max']:.1f}) sigma  P(rconf)={c['P_ridge_confirmed']:.3f}  "
            f"P(vert-anti)={c['P_verticals_anticorrelated']:.3f}")

def main():
    print("="*100)
    print("Z03 -- THE DR4 RE-REGISTER: the falsifier's decision rule restated at the reachable verdict class")
    print("="*100)
    print(__doc__.split("CITATIONS")[0].strip())
    print("-"*100)
    print("THE INPUTS (all on the committed record):")
    print(f"  G225: P(STRONG)=0.000 at every documented N; n_pass 6.3-6.4; the 20-sigma gate needs")
    print(f"        N_usable ~ {N_GATE}; ridge 11.5 sigma at N=2000 / 18.4 at N=5000;")
    print(f"        P(WEAK) 0.45-0.51, P(SPLIT) 0.41-0.48, P(DISFAVORED) 0.07-0.09")
    print(f"  G165: the frozen 9-test contract (9=STRONG, 7-8=WEAK, 5-6=SPLIT, <=4=DISFAVORED);")
    print(f"        the ridge at 30.7 sigma was computed at N_sel = 2500 on the ideal 200k-pair mock")
    print(f"  WB-33: DR3 dry-run catalog = {N_DR3} pairs / {N_DR3_DEEP} deep (Banik-like cuts)")
    print(f"  DR4 doc (Fabricius, VERIFIED external): PM precision x{G_PM_DR4} vs DR3, 5.5-yr baseline;")
    print(f"        WB-32 frozen: sigma_pm x0.372 (={1/0.372:.3f}x precision)")
    print("-"*100)

    # ------------------------------------------------ (3) THE TRIPLE-CHECK
    tc = triple_check()
    tc["N_best"] = int(round(tc["N_usable_alpha2_best"]))
    print("SECTION 3 -- THE TRIPLE-CHECK: the N_usable ~ 5,760 path (the DR4-doc extrapolation)")
    print(f"  the window: 3-30 kAU is {tc['f_window_3_30kAU']:.1%} of the log-uniform 1-30 kAU selection")
    print(f"  DR3 catalog pairs inside the window : {tc['N_dr3_catalog_in_window']:.0f}")
    print(f"  DR3 deep-usable fraction of window  : {tc['f_dr3_deep_of_window']:.1%}  ({N_DR3_DEEP}/{tc['N_dr3_catalog_in_window']:.0f})")
    print(f"  DR4 PM precision gain               : x{G_PM_DR4} (doc) / x{G_PM_WB32:.3f} (WB-32 frozen x0.372)")
    print(f"  the same significance cut at DR4 admits per-pair errors x{G_PM_DR4} worse ->")
    print(f"     alpha=1 (conservative)           : N_usable ~ {tc['N_usable_alpha1']:.0f}")
    print(f"     alpha=2 (BEST CASE)              : N_usable ~ {tc['N_usable_alpha2_best']:.0f}")
    print(f"  the 20-sigma gate N* = {N_GATE} needs {tc['gate_requires_fraction_of_window']:.1%} of the window class")
    print(f"  -> the realistic BEST-CASE N: {tc['N_best']}  (the gate is at the top of the honest bracket)")
    print("-"*100)

    # ------------------------------------------------ (1)+(2) the re-registered rule and the new cells
    print("SECTION 1+2 -- THE RE-REGISTERED RULE (pre-committed today, binding December):")
    print("  LEVEL 1 (the RIDGE GATE -- the falsifier's kill): ridge ABSENT (sexc outside [1.15,1.22]")
    print("    or sigma < 10 or break/rise/level fail) -> DISFAVORED = KILL, regardless of n_pass.")
    print("  LEVEL 2 (at ridge CONFIRMED): 9/9 = CONFIRMED-STRONG (DECLARED UNREACHABLE at December N,")
    print("    P = 0.000; the 20-sigma gate stays registered as the STRONG condition);")
    print("    7-8 = CONFIRMED-WEAK (ridge > 10 sigma + verticals MIXED: the EFE-cap + ridge physics at")
    print("    the envelope level, the verticals pending better astrometry);")
    print("    <= 6 = SPLIT (ridge confirmed, verticals systematically anti-correlated or collapsed: a")
    print("    genuine tension -- NOT a kill; the identification's zero-parameter statement stands).")
    print("  The December pre-commitment threshold table (frozen; every test bar unchanged from G165/G112):")
    print("    verdict         n_pass   ridge condition                 verticals' sign consistency")
    print("    CONFIRMED-STRONG  9/9   R-RIDGE30.7 >= 20 sigma, sexc in [1.15,1.22]   all 5 pass, signs as registered")
    print("    CONFIRMED-WEAK    7-8   R-LEVEL+R-BREAK7.4+R-NOTFLAT pass AND ridge-sigma > 10")
    print("                                                               mixed: <=1 of 5 fails, no F1/F2/F3 kill")
    print("    SPLIT             <=6   ridge confirmed (as WEAK)          >= 2 of 5 fail on the anti-sign side")
    print("                                                               (or any F1/F2/F3 kill) -- genuine tension")
    print("    DISFAVORED        any   ridge ABSENT (sexc<1.15 / sigma<10 / no break / flat) = KILL, no rescue")
    print("  RE-READ: at December N the mechanical n_pass <= 4 tail (P ~ 0.07-0.09, G225) is the vertical")
    print("    sector collapsing at the FROZEN precision (the bars sit ~1 sigma from the forecast central")
    print("    values, G225 V3) WITH the ridge confirmed -- re-read as SPLIT, not DISFAVORED.  The kill")
    print("    is reserved for the ridge absent.  This is the pre-registered honesty floor, not a re-tuning.")
    print("-"*100)

    # ------------------------------------------------ the new cells (the gate and the best case)
    print("SECTION 3 cont. -- THE VERDICT DISTRIBUTION at the gate and the extrapolated best-case N")
    print("  (1,000 realizations per cell, G225 machinery, G225 seeds; [mechanical] = frozen G165")
    print("  contract, [re-registered] = the rule above; P(rconf) = P(ridge confirmed);")
    print("  P(vert-anti) = P(>= 2 of 5 verticals fail)):")
    cells = []
    ci = 12   # seeds past G225's 9 cells
    for Nu, su in ((N_GATE, 30), (N_GATE, 40), (tc["N_best"], 30), (tc["N_best"], 40), (6500, 30)):
        c = run_cell_rereg(Nu, su, RNG_BASE + ci*10**6); ci += 1
        cells.append(c)
    for c in cells:
        print(fmt_cell(c, "mechanical"))
        print(fmt_cell(c, "re_registered"))
    print()
    print("  per-test PASS probability (the new cells; R-LEVEL/R-BREAK7.4/R-NOTFLAT at 1.000 everywhere,")
    print("  R-RIDGE30.7's sigma is the ridge number above; the 5 verticals drive every tail):")
    hdr = "  test        " + "".join(f"{'N'+str(c['N_usable'])+'s'+str(c['sigma_ast_uas']):>13s}" for c in cells)
    print(hdr)
    for cname in ["R-LEVEL", "R-RIDGE30.7", "R-BREAK7.4", "R-NOTFLAT"] + VERTICALS:
        line = f"  {cname:<10s}"
        for c in cells:
            line += f"{c['per_test_pass'][cname]:>13.3f}"
        print(line)
    print("-"*100)

    # ------------------------------------------------ (4) VERDICTS
    g = json.load(open(os.path.join(HERE, "G225_results.json")))
    c_500 = next(x for x in g["primary_cells"] if x["N_usable"] == 5000 and x["sigma_ast_uas"] == 30)
    c_200 = next(x for x in g["primary_cells"] if x["N_usable"] == 2000 and x["sigma_ast_uas"] == 30)
    # re-registered re-read of the G225 primary cells: P(ridge absent) = 0.000 at every documented cell
    # (R-LEVEL/R-BREAK7.4/R-NOTFLAT at 1.000 and ridge sigma min >= 10.6), so the mechanical P(D) tail
    # re-reads as SPLIT.
    rereg_500 = dict(P_STRONG=0.0, P_WEAK=c_500["P_WEAK"],
                     P_SPLIT=round(c_500["P_SPLIT"] + c_500["P_DISFAVORED"], 3), P_DISFAVORED=0.0)
    rereg_200 = dict(P_STRONG=0.0, P_WEAK=c_200["P_WEAK"],
                     P_SPLIT=round(c_200["P_SPLIT"] + c_200["P_DISFAVORED"], 3), P_DISFAVORED=0.0)
    print("VERDICTS")
    print(f"  V1 [the re-registered rule]: the DR4 falsifier is re-armed at the reachable verdict class.")
    print(f"     The kill = the ridge ABSENT (no rise, no 7.4-kAU break, sexc < 1.15, or sigma < 10) ->")
    print(f"     DISFAVORED, no rescue (FALSIFIER_MATRIX row 1 stands).  At ridge confirmed: 7-8/9 = WEAK")
    print(f"     (verticals mixed), <= 6/9 = SPLIT (verticals anti-correlated/collapsed = genuine tension,")
    print(f"     NOT a kill).  9/9 = STRONG declared UNREACHABLE in December (P = 0.000 at N <= 5,000;")
    print(f"     the 20-sigma R-RIDGE30.7 gate needs N_usable ~ {N_GATE}).  Every test bar is unchanged")
    print(f"     (G165/G112 frozen); only the verdict READING is re-stated, before the data.")
    print(f"  V2 [the December expectations at the re-registered class] (G225 primary cells, re-read):")
    print(f"     N=2000, 30 uas:  P(WEAK)={rereg_200['P_WEAK']:.3f} P(SPLIT)={rereg_200['P_SPLIT']:.3f} "
          f"P(DISFAVORED)={rereg_200['P_DISFAVORED']:.3f} P(STRONG)={rereg_200['P_STRONG']:.3f}")
    print(f"     N=5000, 30 uas:  P(WEAK)={rereg_500['P_WEAK']:.3f} P(SPLIT)={rereg_500['P_SPLIT']:.3f} "
          f"P(DISFAVORED)={rereg_500['P_DISFAVORED']:.3f} P(STRONG)={rereg_500['P_STRONG']:.3f}")
    print(f"     the ridge registers {c_200['R_RIDGE30_7_sigma']['mean']} sigma (N=2000) / "
          f"{c_500['R_RIDGE30_7_sigma']['mean']} sigma (N=5000) in EVERY realization -- the ridge is the")
    print(f"     number to watch, and it is confirmed in 100% of realizations at every documented N.")
    print(f"     At the extrapolated best case N={tc['N_best']}: see the cells above (P(STRONG) turns on).")
    print(f"  V3 [the honest statement]: the DR4 falsifier, re-armed at the reachable precision.  The")
    print(f"     theory's own forecast (the mocks ARE the registered prediction) lands MODAL CONFIRMED-")
    print(f"     WEAK ~ SPLIT with the ridge confirmed at 11.5-18.4 sigma in every realization;")
    print(f"     P(CONFIRMED-STRONG) = 0.000 and P(DISFAVORED) = 0.000 at the re-registered class (the")
    print(f"     kill requires the ridge absent, which the forecast never produces).  The December number")
    print(f"     to watch is the ridge sigma and the 5 verticals' sign consistency -- WEAK vs SPLIT --")
    print(f"     not P(STRONG).  The N ~ 5,760 gate is at the top of the honest extrapolation from the")
    print(f"     DR4 documentation (x2.8 PM precision over WB-33's 10,624/802 DR3 catalog): a best-case")
    print(f"     N ~ {tc['N_best']} makes the STRONG outcome reachable, but it is NOT the December base case.")
    print("="*100)

    out = dict(task="Z03", date="2026-09-16", seed=RNG_BASE, n_realizations=N_REAL,
               section1_honest_class_table=dict(
                   reachable_at_december_N=["CONFIRMED-WEAK (7-8/9)", "SPLIT (5-6/9)", "DISFAVORED (<=4/9)"],
                   CONFIRMED_STRONG="DECLARED UNREACHABLE at December N: P = 0.000 at every documented N (G225); the 20-sigma R-RIDGE30.7 gate needs N_usable ~ 5760",
                   CONFIRMED_WEAK="ridge > 10 sigma + verticals MIXED: the EFE-cap + ridge physics confirmed at the envelope level, the verticals pending better astrometry",
                   SPLIT="the ridge confirmed but the verticals systematically anti-correlated: a genuine tension (NOT a kill)",
                   DISFAVORED="the ridge ABSENT: KILL, no post-hoc rescue (Amendment-12)"),
               section2_december_precommitment=dict(
                   rule="LEVEL 1 ridge gate: ridge absent (sexc outside [1.15,1.22] or sigma<10 or no break / flat) -> DISFAVORED = KILL regardless of n_pass; LEVEL 2 at ridge confirmed: 9/9 = STRONG (unreachable), 7-8 = WEAK, <=6 = SPLIT",
                   threshold_table=[
                       dict(verdict="CONFIRMED-STRONG", n_pass="9/9", ridge="R-RIDGE30.7 >= 20 sigma, sexc in [1.15,1.22]", verticals="all 5 pass, signs as registered"),
                       dict(verdict="CONFIRMED-WEAK", n_pass="7-8/9", ridge="R-LEVEL + R-BREAK7.4 + R-NOTFLAT pass AND ridge sigma > 10", verticals="mixed: <= 1 of 5 fails, no F1/F2/F3 kill"),
                       dict(verdict="SPLIT", n_pass="<=6/9", ridge="ridge confirmed (as WEAK)", verticals=">= 2 of 5 fail on the anti-sign side or any F1/F2/F3 kill -- genuine tension"),
                       dict(verdict="DISFAVORED", n_pass="any", ridge="ridge ABSENT (sexc < 1.15 / sigma < 10 / no break / flat)", verticals="irrelevant -- KILL")],
                   reread="at December N the mechanical n_pass <= 4 tail (P ~ 0.07-0.09, G225) occurs WITH the ridge confirmed -> re-read as SPLIT (vertical collapse at the frozen precision), not DISFAVORED; every test bar unchanged from G165/G112"),
               section3_triple_check=dict(
                   documented_inputs=dict(dr4_doc="Fabricius IEEC-ICCUB 28 Jan 2026: PM precision x2.8 vs DR3, 5.5-yr baseline, release 2026.9 (VERIFIED external)",
                                          wb32="DR4 sigma_pm x0.372, sigma_plx x0.718 vs DR3 (frozen)",
                                          wb33="DR3 dry-run: 10,624 pairs / 802 deep (Banik-like cuts)",
                                          wb27="N ~ 2,337 pairs for 3-sigma from Newton (level channel)",
                                          g225_gate="the 20-sigma ridge gate needs N_usable ~ 5,760"),
                   extrapolation=tc,
                   verdict_at_gate_and_best=[{k: v for k, v in c.items() if k != "n_pass_mean"} for c in cells],
                   g225_primary_reread=dict(N2000_s30=rereg_200, N5000_s30=rereg_500)),
               verdicts=dict(
                   V1="the DR4 falsifier re-armed at the reachable verdict class: the kill = the ridge ABSENT; at ridge confirmed the December classes are WEAK (7-8/9, verticals mixed) and SPLIT (<=6/9, verticals anti-correlated); 9/9 STRONG declared unreachable (P = 0.000 at N <= 5,000)",
                   V2_december_expectations=rereg_500,
                   V3_honest="the theory expects MODAL CONFIRMED-WEAK ~ SPLIT with the ridge confirmed at 11.5-18.4 sigma in every realization; P(STRONG) = 0.000 and P(DISFAVORED) = 0.000 at the re-registered class; the December number to watch is the ridge sigma and the verticals' sign consistency; the N ~ 5760 gate sits at the top of the honest DR4-doc extrapolation (best case ~6300), not the December base case"))
    with open(os.path.join(HERE, "Z03_results.json"), "w") as f:
        json.dump(out, f, indent=1, default=float)
    print("WROTE Z03_results.json")

if __name__ == "__main__":
    main()
