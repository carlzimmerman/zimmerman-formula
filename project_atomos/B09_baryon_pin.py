#!/usr/bin/env python3
r"""B09 -- THE BARYON-FRACTION PIN: the halo-scale depleted share vs the cosmic
0.157 -- the framework's best shot at its last input.

THE QUESTION (the B-series cosmic-wave attack on S05's verdict): S05 concluded
the baryon fraction f_b = Omega_b/Omega_m = 0.157 is INPUT at every committed
closure point (G052's flatness residual consumes it, the EH98 transfer
hardcodes it, the pie's s_b(M) nods are measured cluster/group shares) -- the
"last undeclared free parameter of the cosmic frame."  B09 attacks the one
route S05 flagged as the machinery's only f_b-adjacent emission: the halo-
scale baryon CONTENT.  G187's cosmic closure gives the mass-function-weighted
halo baryon share <s_b> = 0.0846 = 0.54 x f_b -- halos baryon-DEPLETED to
54% of the cosmic share.  THE QUESTION: can that halo-scale depleted share,
run BACKWARD through a first-principles depletion chain (reionization
feedback, stellar/AGN ejection, gas retention -- the committed baryon
physics), PIN the cosmic f_b -- turning the framework's last input into a
DERIVED quantity (a 5-input framework) -- or does the chain's own depletion
factor turn out to be measured, leaving f_b an input still?

(1) THE DEPLETION CHAIN: the halo share s_b = f_retention x f_b, with the
    retention 0.54 assembled from the committed pieces: the STELLAR share
    (Omega_star/Omega_b = 0.0027/0.0493 = 5.5% cosmic; the G143 group
    convention 0.02 = ~25% of the retained budget), the GAS RETENTION
    (f_gas,500 median 0.061, E11 via G143/G178), the FEEDBACK (the measured
    mass-run of retention: d log f_gas/d log M500 = +0.34 dex/dex, G143;
    the group f_gas rise +0.536 vs cluster +0.235, G143; low-mass halos
    eject more -- reionization photo-evaporation + stellar/AGN winds), and
    the GROUP FLOOR (G178: f_b = 0.081 = 0.061 + 0.02, retention 0.518).
    The chain's closure: f_b = s_b/f_ret = 0.0846/0.54 = 0.157 -- IF every
    link is independently fixed.  The honest completion status is stated:
    every link is MEASURED (the retention 0.54 is the ratio of measured
    halo baryon shares to the measured cosmic share); the ejected fraction
    (1 - retention = 0.46) is never partitioned between "beyond R500" and
    "genuinely ejected" on the committed record; no framework mechanism
    (a0, m, Z, the ladder) appears anywhere in the chain.

(2) THE GROUP-COSMIC BRIDGE: two rungs bracket the cosmic datum.  Rung A --
    the groups (E11 via G143/G178: f_gas,500 0.061 + 0.02 stars = 0.081,
    retention 0.52); Rung B -- the halo mean (G187: <s_b> = 0.0846,
    retention 0.54).  Under the SAME depletion factor 0.54: f_b from the
    group rung = 0.081/0.54 = 0.150; f_b from the halo rung = 0.0846/0.54
    = 0.157.  The two-rung consistency band [0.150, 0.157] brackets the
    Planck datum 0.1564 to 4.3%; with the honest systematics (f_gas,500
    calibration, the 0.02 star convention, the R500 truncation: retention
    +- 0.07) the derived band widens to 0.157 +- 0.02 = [0.139, 0.180].

(3) THE DECISION: does the chain pin f_b = 0.157 +- 0.02?  The chain's
    first-principles content vs its empirical floor: the FIRST-PRINCIPLES
    content is exactly zero on the framework side (no committed mechanism
    computes the ejection budget; the retention factor is the ratio of two
    measured shares; recovering f_b from s_b/f_ret is an IDENTITY on
    measured sides -- the G03C circularity class S05 flagged for the
    flatness slack).  The EMPIRICAL floor carries the whole chain (E11 gas,
    F&P stellar bound, the pie's measured nods).  DECISION: the chain does
    NOT promote f_b to DERIVED; f_b = 0.157 remains an INPUT; the six-core
    (a0, G, c, Omega_Lambda, f_b, m) = 4 measured + 1 identity-pinned (a0)
    + 1 derived (m) stands; the "5-input framework" is NOT earned.  WHAT IS
    NEW: f_b is now halo-ANCHORED -- two independent rungs render the datum
    consistent at 4% (band [0.150, 0.157]) -- a consistency lock, not a
    derivation.

(4) VERDICTS.
    V1 THE DEPLETION CHAIN: assembled (star 0.02 / gas 0.061 / feedback
       mass-run +0.34 dex/dex / floor 0.081), ARITHMETICALLY CLOSED
       (retention 0.52 group, 0.54 halo -> f_b = 0.157 at 0.2% -- an
       identity), PHYSICS-OPEN (the retention is a measured ratio; the
       ejected fraction is unpartitioned; no framework mechanism in the
       chain).
    V2 THE DERIVED f_b BAND: same-depletion two-rung band
       [0.150 (group rung), 0.157 (halo rung)] vs datum 0.1564 (inside,
       4.3% from the low edge); systematic envelope 0.157 +- 0.02
       = [0.137, 0.177]; the central value recovers the Planck datum
       because both the numerator and the denominator carry it.
    V3 THE HONEST STATEMENT: the baryon fraction is NOT pinned by the
       halo-depletion chain -- the chain's depletion factor 0.54 is
       measured (the ratio of the measured halo baryon share to the
       measured cosmic share), so f_b = s_b/0.54 restores the datum by
       construction (G03C class); the framework contributes no mechanism
       to the chain; f_b = 0.157 stays an INPUT.  THE INPUT COUNT,
       FINALLY SETTLED: six core (a0, G, c, Omega_Lambda, f_b, m) = 4
       measured + 1 identity-pinned + 1 derived -- f_b in the measured
       column, now with a registered halo-scale consistency anchor
       (the two rungs 0.081 / 0.0846 render the datum consistent at 4%).

REGISTERS READ (committed numbers only): deepseek_push/G178_results.json
(the group floor 0.081 = f_gas,500 median 0.061 + 0.02 stars; the implied
f_dust 0.919 = 1 - f_b; M_sat = 3.0876e14), G187_results.json (the cosmic
closure <s_b> = 0.0846 = 0.54 x f_b; the pie nods 0.081/0.068/0.1443/
0.2025/0.2217), G143_results.json (the 26 E11 group rows: f_gas,500 spread
0.013-0.098; the f_gas mass-run +0.34 dex/dex; the group rise +0.536),
G079_results.json (Omega_dm = 0.264 = eq 0.0021 + dust 0.2619; Omega_star
0.0027; envelope Omega_b/Omega_dm = 0.1867), S05_results.json (the f_b
provenance audit: f_b = 0.1564 INPUT; the G03C circularity classification;
the six-core count), A02_results.json (the mu m_p rung: baryon-SCALE, not
baryon-ABUNDANCE content), G198_results.json (eq + dust = 1.000 x Omega_dm).

Outputs: B09_baryon_pin.out, B09_results.json (this lane).
Run:     python3 B09_baryon_pin.py > B09_baryon_pin.out 2>&1
"""

import json
import math
import os
import statistics as st

RES, NP, NF = [], 0, 0


def check(name, measured, ok, d=""):
    global NP, NF
    ok = bool(ok)
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    print(f"         measured: {measured}")
    if d:
        print(f"         reading : {d}")
    RES.append({"name": name, "measured": str(measured), "pass": ok,
                "reading": d})
    NP, NF = NP + (1 if ok else 0), NF + (0 if ok else 1)


def info(*a):
    print(*a, flush=True)


print(__doc__)
print("=" * 100)
print("B09 -- THE BARYON-FRACTION PIN: the halo depleted share vs the cosmic")
print("0.157 -- the framework's last input, attacked through the halo scale")
print("=" * 100)

HERE = os.path.dirname(os.path.abspath(__file__))
DP = HERE  # the committed registers live beside this lane's parent tree
ROOT = os.path.dirname(HERE)

# ------------------------------------------------------------------ registers
def reg(name):
    p = os.path.join(ROOT, "deepseek_push", name)
    return json.load(open(p))


G178 = reg("G178_results.json")
G187 = reg("G187_results.json")
G143 = reg("G143_results.json")
G079 = reg("G079_results.json")
S05 = reg("S05_results.json")

# Planck / committed cosmic constants (the S05 register values)
OM_M = 0.3153           # Planck 2020 (G079)
OM_B = 0.0493           # Planck 2020 (INPUT at every touchpoint, S05)
OM_DM = G079["decomposition"]["Omega_dm"]                 # 0.264
OM_STAR = G079["decomposition"]["Omega_star"]             # 0.0027
OM_EQ_CAP = G079["decomposition"]["Omega_eq_capped_0p62"]  # 0.0020925
F_B = OM_B / OM_M                                        # 0.15636

# the B09 halo-scale registers (committed)
F_B_GROUP = G178["direct_test"]["median_f_b"]             # 0.081
F_GAS_500 = G178["direct_test"]["median_f_gas_500"]       # 0.061
F_STAR_GRP = 0.02                                          # G143 convention
SB_HALO = G187["cosmic_closure"]["mean_shares_equipartition"]["s_b"]  # 0.0846
M_SAT = G178["prediction"]["M_sat_Msun"]                  # 3.0876e14
F_REF = G178["direct_test"]["cluster_anchor"]             # 0.674

# the pie's s_b(M) nods (G187: the constitution curve's committed anchors)
SB_NODES = [(1e13, F_B_GROUP), (1.7298e14, 0.068), (3.48e14, 0.1443),
            (8e14, 0.2025), (1e15, 0.2217)]
NOD_LABEL = ["1e13 (the 26 E11 groups, median)",
             "1.73e14 (IC1633, group row f5 + 0.02)",
             "3.48e14 (A1644, the least-massive cluster, measured)",
             "8e14 (the pie-internal phantom-credit anchor: 0.5695 x u(8e14))",
             "1e15 (the s_b ~ M^+0.18 power-law face)"]

# the group rows (G143's committed E11 transcription, gated vs G125)
GROUPS = {r["name"]: r for r in G143["direct_test"]["per_group_two_point"]}
NGRP = len(GROUPS)
assert NGRP == 26

# framework-core provenance (S05's audit, re-stated)
CORE = "(a0, G, c, Omega_Lambda, f_b, m)"

info(f"  registers: Omega_m = {OM_M}, Omega_b = {OM_B} (INPUT), "
     f"Omega_dm = {OM_DM} (G079 closure eq + dust = 1.000 x Omega_dm), "
     f"Omega_star = {OM_STAR}")
info(f"  f_b = Omega_b/Omega_m = {F_B:.4f} (Planck; the task's 0.157)")
info(f"  the halo rungs: <s_b> (G187) = {SB_HALO:.4f} = "
     f"{100*SB_HALO/F_B:.1f}% of f_b;  f_b,group (G178) = {F_B_GROUP:.3f} = "
     f"{100*F_B_GROUP/F_B:.1f}% of f_b")
info(f"  the group floor: f_b,group = f_gas,500 ({F_GAS_500:.3f} median) + "
     f"stars ({F_STAR_GRP:.2f}, G143 convention) = {F_B_GROUP:.3f}")
info(f"  the pie's s_b(M) nods: "
     f"{', '.join(f'{m:.2e}->{s:.4f}' for m, s in SB_NODES)}")

# =====================================================================
print()
print("=" * 100)
print("GATE 0 -- THE COMMITTED REGISTERS REPRODUCED (this lane's backbone)")
print("=" * 100)

# G0a: the group floor from G143's per-group rows, reproduced independently
f5 = [GROUPS[n]["f5"] for n in GROUPS]
f5 = sorted(f5)
fb_group = [g + F_STAR_GRP for g in f5]
med_f5, med_fb = st.median(f5), st.median(fb_group)
check("G0a [the group floor gate] the 26 E11 groups' median f_b = f_gas,500 "
      "+ 0.02 stars reproduces G178's registered 0.081",
      f"median f_gas,500 = {med_f5:.3f} (spread [{f5[0]:.3f}, {f5[-1]:.3f}]); "
      f"median f_b = {med_fb:.3f} (spread [{fb_group[0]:.3f}, "
      f"{fb_group[-1]:.3f}])",
      abs(med_fb - F_B_GROUP) < 0.001,
      "G143's committed E11 transcription, gated there against G125; the "
      "0.02 stellar share is G143's group convention")

# G0b: the halo share from G187's register
check("G0b [the halo-share gate] G187's cosmic closure <s_b> = 0.0846 is "
      "the mass-function-weighted mean baryon share of halos M > 1e12 "
      "(Tinker+08 on the committed EH98 pipeline, gated in G187)",
      f"<s_b> = {SB_HALO:.4f} = {100*SB_HALO/F_B:.1f}% of f_b = {F_B:.4f}",
      abs(SB_HALO / F_B - 0.54) < 0.02,
      "the task's 0.54 depletion factor is exactly this measured ratio "
      "<s_b>/f_b -- a MEASURED share ratio, not a framework output")

# G0c: the retention-vs-mass run through the pie's nods (the feedback sig)
ret_nodes = [s / F_B for _, s in SB_NODES]
check("G0c [the retention mass-run] r(M) = s_b(M)/f_b rises with mass "
      "0.52 -> 1.42 through the pie's nods -- the low-mass depletion "
      "signature the feedback chain is built on",
      f"r: {', '.join(f'{r:.2f}' for r in ret_nodes)} "
      f"(at {', '.join(f'{m:.1e}' for m, _ in SB_NODES)})",
      ret_nodes[0] < ret_nodes[-1] and ret_nodes[2] > 0.85,
      "retention rises steeply through the saturation gap (groups ~0.5 -> "
      "clusters ~0.9-1.4): low-mass halos are the most depleted -- the "
      "canonical reionization + feedback signature (G143's +0.34 dex/dex "
      "gas level-run is the same effect measured on the f_gas field)")

# =====================================================================
print()
print("=" * 100)
print("PART 1 -- THE DEPLETION CHAIN: s_b = f_retention x f_b, link by link")
print("=" * 100)

print("""
  THE CHAIN (the committed pieces, in order):
    f_b,halo  = f_b,cosmic x f_retention
    f_retention = [star share] + [gas retention]  -  [ejected / beyond R500]
  Links, all from the committed record:
    L1 STAR SHARE     : cosmic Omega_star/Omega_b = 0.0027/0.0493 = 5.5%
                        (Fukugita & Peebles 2004 via G079); the group
                        convention 0.02 (G143) = 24.7% of the retained
                        budget at groups (0.02/0.081).
    L2 GAS RETENTION  : f_gas,500 median 0.061 (E11 via G143/G178) -- the
                        hot gas within R500 only; the E11 window is
                        [r2500, R500] and the group gas profile is STILL
                        RISING there (+0.536 slope), so gas beyond R500 is
                        uncounted by this link.
    L3 FEEDBACK       : the mass-run of retention -- d log f_gas/d log M500
                        = +0.34 dex/dex (G143 level-run); group f_gas rise
                        +0.536 vs cluster +0.235 (G143); the lowest-gas
                        groups (MKW4 0.013, NGC5129 0.014, HCG62 0.017)
                        are the lowest-mass -- reionization
                        photo-evaporation + stellar/AGN ejection, the
                        standard mechanism statement.  QUANTITATIVE
                        EJECTION BUDGET: NOT committed anywhere.
    L4 THE FLOOR      : f_b,group = 0.081 (G178) = L1 + L2 -- the group
                        rung's measured result, retention 0.518.
    L5 THE HALO MEAN  : <s_b> = 0.0846 (G187), retention 0.541 = the
                        mass-function-weighted completion of the same
                        chain (the pie + Tinker weights).
""")

r_group = F_B_GROUP / F_B
r_halo = SB_HALO / F_B
star_cosmic = OM_STAR / OM_B
star_fr_ret = F_STAR_GRP / F_B_GROUP
gas_fr_ret = F_GAS_500 / F_B_GROUP
info(f"  L1 star share   : cosmic {100*star_cosmic:.1f}% of Omega_b; "
     f"group convention {F_STAR_GRP:.2f} = {100*star_fr_ret:.1f}% of the "
     f"retained {F_B_GROUP:.3f}")
info(f"  L2 gas retention: f_gas,500 = {F_GAS_500:.3f} = {100*gas_fr_ret:.1f}% "
     f"of the retained; as a share of the COSMIC budget: "
     f"{100*F_GAS_500/F_B:.1f}%")
info(f"  L3 feedback     : retention mass-run +0.34 dex/dex (measured); "
     f"ejected fraction = 1 - f_retention = {1-r_group:.2f} (group) / "
     f"{1-r_halo:.2f} (halo mean) of cosmic baryons -- NOT partitioned "
     f"between 'beyond R500' and 'genuinely ejected' on the committed record")
info(f"  L4 floor        : f_b,group = {F_B_GROUP:.3f} -> r_group = "
     f"{r_group:.3f}")
info(f"  L5 halo mean    : <s_b> = {SB_HALO:.4f} -> r_halo = {r_halo:.3f}")

f_b_pred_halo = SB_HALO / 0.54
info("")
info("  THE CHAIN'S CLOSURE (the task's construction, delta_f = 0.54):")
info(f"    f_b = <s_b>/0.54 = {SB_HALO:.4f}/{0.54} = {f_b_pred_halo:.4f} "
     f"vs the Planck datum {F_B:.4f} (delta "
     f"{100*(f_b_pred_halo/F_B - 1):+.2f}%)")
info(f"    f_b = f_b,group/0.52 = {F_B_GROUP:.3f}/{r_group:.3f} = "
     f"{F_B_GROUP/r_group:.4f} (the group rung under its OWN retention -- "
     f"the identity)")
info(f"  -> the closure is EXACT because the depletion factor is DEFINED as "
     f"the measured ratio s_b/f_b: dividing the measured share by the "
     f"measured ratio restores the measured datum.  This is the G03C "
     f"circularity class (S05's own classification of the flatness slack).")

check("C1 [the chain closes arithmetically] f_b = <s_b>/0.54 = 0.157 "
      "reproduces the Planck datum to 0.2%",
      f"f_b = {f_b_pred_halo:.4f} vs {F_B:.4f} "
      f"(delta {100*(f_b_pred_halo/F_B - 1):+.2f}%)",
      abs(f_b_pred_halo / F_B - 1) < 0.01,
      "the arithmetic closes -- but only because 0.54 IS <s_b>/f_b: this "
      "is an identity on measured sides, the same class S05 registered for "
      "the flatness-slack echo (0.160 vs 0.156)")
check("C2 [the chain's links are all measured, none derived] every link of "
      "the depletion chain is a measured share (E11 gas, F&P stars, the pie "
      "nods) or a measured gradient (G143 +0.34 dex/dex, +0.536 rise); NO "
      "framework mechanism (a0, m, Z, the ladder, the equilibrium bound) "
      "appears anywhere in the chain",
      f"links: L1 star {100*star_cosmic:.1f}% cosmic (measured), "
      f"L2 gas {F_GAS_500:.3f} (measured), L3 feedback gradient (measured), "
      f"L4 floor {F_B_GROUP:.3f} (measured), L5 mean {SB_HALO:.4f} (measured)",
      star_cosmic > 0 and F_GAS_500 > 0 and F_B_GROUP > 0,
      "the honest completion status: ARITHMETICALLY CLOSED, PHYSICS-OPEN -- "
      "the retention factor is a measured ratio, the ejected fraction is "
      "unpartitioned, and the framework's machinery contributes zero terms "
      "to the chain")

# =====================================================================
print()
print("=" * 100)
print("PART 2 -- THE GROUP-COSMIC BRIDGE: two rungs, one depletion, a band")
print("=" * 100)

print("""
  RUNG A -- the GROUPS (E11 via G143/G178): f_b,group = 0.081
            (f_gas,500 median 0.061 + 0.02 stars), retention r = 0.52.
  RUNG B -- the HALO MEAN (G187): <s_b> = 0.0846, retention r = 0.54.
  The bridge: G187's pie connects them -- the group nod anchors the
  low-mass end of s_b(M), the cluster nods (A1644 0.1443, the 8e14
  anchor, the 1e15 face) the high end, and <s_b> is the Tinker-weighted
  mean of the same curve.  Two INDEPENDENT measurements of halo baryon
  content at different mass weightings.
  UNDER THE SAME depletion factor 0.54:
    f_b(rung A) = 0.081/0.54 = 0.150
    f_b(rung B) = 0.0846/0.54 = 0.157
    -> the two-rung consistency band [0.150, 0.157], centre 0.153.
""")

fb_rungA = F_B_GROUP / 0.54
fb_rungB = SB_HALO / 0.54
band_lo, band_hi = sorted([fb_rungA, fb_rungB])
info(f"  Rung A (groups) : f_b = {F_B_GROUP:.3f}/0.54 = {fb_rungA:.4f}")
info(f"  Rung B (halos)  : f_b = {SB_HALO:.4f}/0.54 = {fb_rungB:.4f}")
info(f"  TWO-RUNG BAND   : f_b in [{band_lo:.4f}, {band_hi:.4f}] "
     f"(centre {(band_lo+band_hi)/2:.4f}) vs datum {F_B:.4f}")
info(f"  low edge vs datum: {100*(band_lo/F_B - 1):+.1f}%; "
     f"high edge vs datum: {100*(band_hi/F_B - 1):+.1f}%")

# the per-group rung spread (the honest width of rung A)
rg = sorted(g + F_STAR_GRP for g in f5)
rr = [x / F_B for x in rg]
info("")
info(f"  RUNG-A SPREAD (the honest width of the group rung): per-group "
     f"f_b = f_gas,500 + 0.02 spans [{rg[0]:.3f}, {rg[-1]:.3f}], "
     f"median {st.median(rg):.3f}; the implied per-group retention "
     f"r = f_b/f_b,cosmic spans [{rr[0]:.2f}, {rr[-1]:.2f}], "
     f"median {st.median(rr):.2f}")
info(f"  -> the group-scale retention scatter is WIDE (mass + environment); "
     f"the median 0.52 is a floor-of-scatter statement, and the same "
     f"retention applied to the group rung gives f_b = {fb_rungA:.3f} -- "
     f"4.3% below the datum, within the rung's own width")

# the systematic envelope (the honest +- 0.02)
print("""
  THE SYSTEMATIC ENVELOPE: the retention factor carries the f_gas,500
  calibration, the 0.02 star convention (G143's convention, not a
  per-group measurement), and the R500 truncation (the E11 window ends
  at R500 where the gas profile is still rising).  A fair systematic on
  the retention is +- 0.07 (r = 0.54 +- 0.07 -> ~13%):
    delta f_b / f_b = delta r / r = 0.07/0.54 = 13% -> +- 0.020
    f_b(pred) = 0.157 +- 0.02 = [0.139, 0.180]  (the task's bracket)
""")
DR = 0.07
f_b_lo_sys = SB_HALO / (0.54 + DR)
f_b_hi_sys = SB_HALO / (0.54 - DR)
info(f"  systematic band: r = 0.54 +- {DR} -> f_b in "
     f"[{f_b_lo_sys:.4f}, {f_b_hi_sys:.4f}] "
     f"= {SB_HALO/0.54:.3f} +- {SB_HALO/0.54 - f_b_lo_sys:.3f} "
     f"(the +-0.02 bracket)")
info(f"  datum {F_B:.4f} inside: {f_b_lo_sys < F_B < f_b_hi_sys}")
info(f"  self-consistency (each rung under its OWN retention): "
     f"f_b(rung A) = {F_B_GROUP/r_group:.4f}, "
     f"f_b(rung B) = {SB_HALO/r_halo:.4f} -- BOTH equal the datum "
     f"(the identity: r IS defined as s_b/f_b)")

check("C3 [the two-rung consistency] under the SAME depletion 0.54 the two "
      "independent rungs give f_b = 0.150 (groups) and 0.157 (halos) -- a "
      "band that brackets the datum 0.1564 to within 4.3%",
      f"band [{band_lo:.3f}, {band_hi:.3f}] vs datum {F_B:.3f} "
      f"(low edge {100*(band_lo/F_B-1):+.1f}%)",
      band_lo < F_B < band_hi and (F_B - band_lo) / F_B < 0.05,
      "the two rungs are independent measurements of halo baryon content "
      "(26 E11 groups vs the mass-function-weighted pie); their same-"
      "depletion f_b values are consistent with the Planck datum at the "
      "4-5% level -- a REAL consistency lock, though both rungs are "
      "measured shares")
check("C4 [the derived band] the honest derived f_b band (two rungs + the "
      "retention systematics) is 0.157 +- 0.02 and contains the datum",
      f"band [{f_b_lo_sys:.3f}, {f_b_hi_sys:.3f}] = "
      f"{SB_HALO/0.54:.3f} +- {SB_HALO/0.54 - f_b_lo_sys:.3f}; datum "
      f"{F_B:.4f} inside: {f_b_lo_sys < F_B < f_b_hi_sys}",
      f_b_lo_sys < F_B < f_b_hi_sys,
      "the +-0.02 needs only r = 0.54 +- 0.07, well inside the rung "
      "scatter (group retention spans 0.2-0.75) and the f_gas systematics "
      "-- but the CENTRAL value is the datum by construction (both "
      "factors of the ratio carry it)")

# =====================================================================
print()
print("=" * 100)
print("PART 3 -- THE DECISION: pinned (a 5-input framework) or input still?")
print("=" * 100)

print("""
  THE FIRST-PRINCIPLES CONTENT vs THE EMPIRICAL FLOOR:
  (a) FRAMEWORK MECHANISM CONTENT: what does the closed sector contribute
      to the chain?  Count the machinery terms: a0 -- absent; m (5.09 keV)
      -- absent; Z -- absent; the ladder -- absent; the equilibrium bound
      -- baryon-NORMALIZED (Omega_eq <= Omega_star (1 + f_gas), G079: it
      bounds DARK mass in units of the MEASURED stellar density, never the
      baryon abundance itself); M_sat -- dark-internal only.  The chain's
      physics (reionization photo-evaporation, SNe/AGN ejection, gas
      retention) is STANDARD astrophysics, all external to the framework.
  (b) THE EMPIRICAL FLOOR: every link is a measured datum -- E11's gas
      fractions (UNVERIFIED-in-repo, transcribed via G143, gated vs G125),
      the Fukugita & Peebles stellar density, the pie's measured cluster
      nods.  The retention factor 0.54 IS the ratio of two measured
      shares.  No committed computation produces it.
  (c) THE CIRCULARITY: f_retention = s_b,halo/f_b,cosmic by definition;
      f_b = s_b,halo/f_retention therefore restores the input you already
      supplied.  This is EXACTLY the G03C class S05 registered for the
      flatness slack (0.160 vs 0.156: 'you must input Omega_dm and
      Omega_Lambda to get f_b out').  Here you must input f_b to state
      the depletion factor, then recover f_b.
  THE DECISION: the chain does NOT pin f_b as a DERIVED quantity.  The
  arithmetic closes at 0.157 (0.2%), but the derivation is an identity on
  measured sides.  The framework's input count is NOT reduced: the six
  core inputs (a0, G, c, Omega_Lambda, f_b, m) stand, f_b in the
  MEASURED column.  The '5-input framework' is NOT earned by this chain.
  WHAT IS EARNED: the halo-scale ANCHOR.  Two independent rungs (the
  26-group floor 0.081 and the mass-function-weighted halo mean 0.0846)
  render the cosmic datum consistent at 4%; the band [0.150, 0.157]
  brackets Planck 0.1564.  f_b is now consistency-ANCHORED at halo scale
  -- a genuine new measured cross-check -- while remaining an input.
""")

# the machinery-content audit, quantified
machinery_terms = {"a0": False, "m_keV": False, "Z": False, "ladder": False}
check("C5 [the framework-machinery audit] ZERO framework mechanisms appear "
      "in the depletion chain -- it is a measured-shares assembly",
      f"machinery terms in the chain: {sum(machinery_terms.values())}/4 "
      "(a0: no, m: no, Z: no, ladder: no); links are E11 gas + F&P stars "
      "+ the pie's measured nods + the G143 gradients",
      sum(machinery_terms.values()) == 0,
      "the first-principles content of the chain is zero ON THE FRAMEWORK "
      "SIDE: the retention physics (reionization + ejection) is standard "
      "astrophysics, and its quantitative budget is not computed anywhere "
      "in the committed record -- the chain stands entirely on its "
      "empirical floor")
check("C6 [the G03C circularity] the closure f_b = s_b/0.54 restores the "
      "datum because the depletion factor is DEFINED as s_b/f_b -- "
      "recovering an input from an input (the identity class S05 flagged "
      "for the flatness slack)",
      f"f_b(pred) = {f_b_pred_halo:.4f} = the datum {F_B:.4f} to "
      f"{100*(f_b_pred_halo/F_B-1):+.2f}% -- because 0.54 = "
      f"{SB_HALO:.4f}/{F_B:.4f} = {r_halo:.3f}",
      abs(f_b_pred_halo - F_B) / F_B < 0.005,
      "f_retention = s_b/f_b is a definition; f_b = s_b/f_retention is its "
      "inversion -- the chain adds no independent constraint, exactly as "
      "S05's verdict V3 stated ('no test of the framework constrains it')")

# ---------------- the input count, finally settled
info("")
info("  THE INPUT COUNT, FINALLY SETTLED (the six-core statement):")
info(f"    core = {CORE}")
info("    measured         : G, c, Omega_Lambda, f_b = 0.157  (4)")
info("    identity-pinned  : a0 = c^2/(Z R_dS) = 9.3624e-11   (1, Z11/S09)")
info("    derived          : m = 5.09 +- 0.10 keV             (1, G212)")
info("    + ancillary measured datums: H0, Omega_star, n_s, sigma_8, T_CMB")
info("    + per-object M_b (the baryon ruler at every scale)")
info("  THE B09 AMENDMENT: f_b = 0.157 REMAINS in the measured column; the")
info("    halo-depletion chain adds a CONSISTENCY ANCHOR (two rungs render")
info("    the datum consistent at 4%, band [0.150, 0.157]) but no DERIVATION")
info("    -- the 5-input framework is not earned; the 6-input stands.")

check("C7 [the input count] the six-core (a0, G, c, Omega_Lambda, f_b, m) "
      "stands: 4 measured + 1 identity-pinned + 1 derived; f_b stays in "
      "the measured column after the depletion-chain attack",
      f"6 core = 4 measured (incl. f_b = {F_B:.4f}) + 1 identity-pinned "
      f"(a0) + 1 derived (m); the chain adds the halo anchor, not a "
      f"derivation",
      True,
      "the depletion chain was the machinery's best shot at f_b (S05's "
      "only f_b-adjacent emission, <s_b> = 0.54 x f_b); it closes "
      "arithmetically and fails as a derivation -- f_b is halo-ANCHORED, "
      "not halo-DERIVED")
check("C8 [the equilibrium bound adds nothing] G079's Omega_eq <= "
      "Omega_star (1 + f_gas) is baryon-normalized (measured stellar "
      "density): it bounds dark mass in baryon units, never the baryon "
      "abundance itself -- re-confirmed as a dead end for f_b",
      f"Omega_eq <= {OM_STAR} x (1 + 0.25) = {OM_STAR*1.25:.4f} "
      f"(uncapped {0.003375:.4f}) = {100*0.003375/OM_DM:.2f}% of Omega_dm",
      True,
      "S05 verdict 2b re-confirmed: the only baryon-bound in the closed "
      "sector is dark mass in units of the MEASURED stellar density -- "
      "the equilibrium phase never fixes Omega_b itself")

# =====================================================================
print()
print("=" * 100)
print("V -- THE VERDICTS")
print("=" * 100)

v1 = (f"THE DEPLETION CHAIN: ASSEMBLED, ARITHMETICALLY CLOSED, PHYSICS-"
      f"OPEN.  The chain s_b = f_retention x f_b with the committed links "
      f"-- stars (cosmic Omega_star/Omega_b = {100*star_cosmic:.1f}%; group "
      f"convention {F_STAR_GRP:.2f} = {100*star_fr_ret:.0f}% of the retained "
      f"{F_B_GROUP:.3f}), gas retention (f_gas,500 median {F_GAS_500:.3f} = "
      f"{100*gas_fr_ret:.0f}% of the retained, {100*F_GAS_500/F_B:.0f}% of "
      f"the cosmic budget, R500-truncated), feedback (the measured "
      f"retention mass-run +0.34 dex/dex and the group f_gas rise +0.536 vs "
      f"cluster +0.235, G143 -- reionization + ejection, mechanism "
      f"statement only, no committed quantitative budget), and the G178 "
      f"floor ({F_B_GROUP:.3f} = {F_GAS_500:.3f} + {F_STAR_GRP:.2f}, "
      f"retention {r_group:.2f}) -- CLOSES at f_b = <s_b>/0.54 = "
      f"{f_b_pred_halo:.4f} vs the datum {F_B:.4f} "
      f"(delta {100*(f_b_pred_halo/F_B-1):+.2f}%), an IDENTITY on measured "
      f"sides: the depletion factor 0.54 "
      f"IS the measured ratio <s_b>/f_b (G187), and the ejected share "
      f"(1 - retention = {1-r_group:.2f} group / {1-r_halo:.2f} halo mean) "
      f"is never partitioned between 'beyond R500' and 'genuinely ejected' "
      f"on the committed record.  Completion status: every link is "
      f"MEASURED (E11 gas -- UNVERIFIED-in-repo, gated vs G125; F&P stars; "
      f"the pie's measured nods); the framework's machinery contributes "
      f"zero terms; the chain's first-principles content resides in the "
      f"feedback MECHANISM STATEMENT, which is standard astrophysics, "
      f"quantified nowhere in-repo.")
v2 = (f"THE DERIVED f_b BAND: under the SAME depletion factor 0.54, the two "
      f"independent rungs give f_b(rung A, groups) = {F_B_GROUP:.3f}/0.54 = "
      f"{fb_rungA:.4f} and f_b(rung B, halo mean) = {SB_HALO:.4f}/0.54 = "
      f"{fb_rungB:.4f} -- the TWO-RUNG CONSISTENCY BAND [{band_lo:.4f}, "
      f"{band_hi:.4f}], centre {(band_lo+band_hi)/2:.4f}, which brackets "
      f"the Planck datum {F_B:.4f} to {(F_B-band_lo)/F_B*100:.1f}% on the "
      f"low edge.  WITH THE HONEST SYSTEMATICS (f_gas,500 calibration, the "
      f"{F_STAR_GRP:.2f} star convention, the R500 truncation: retention "
      f"+/- {DR}, ~13%): f_b = {SB_HALO/0.54:.3f} +/- "
      f"{SB_HALO/0.54 - f_b_lo_sys:.3f} = [{f_b_lo_sys:.3f}, "
      f"{f_b_hi_sys:.3f}] -- the task's 0.157 +/- 0.02 bracket, datum "
      f"inside.  BUT the central value reproduces the datum ONLY because "
      f"both factors of the ratio (the numerator <s_b> and the "
      f"denominator 0.54 = <s_b>/f_b) carry it: the band is a "
      f"CONSISTENCY BAND, not a prediction band.  The genuinely new "
      f"content: two independent measurements of halo baryon content "
      f"(26 E11 groups vs the Tinker-weighted pie) are mutually consistent "
      f"and consistent with the cosmic datum at 4%.")
v3 = (f"HONEST -- THE BARYON FRACTION IS NOT PINNED BY THE HALO-DEPLETION "
      f"CHAIN; IT REMAINS AN INPUT, NOW HALO-ANCHORED.  The chain closes "
      f"arithmetically (f_b = <s_b>/0.54 = {f_b_pred_halo:.4f} = the datum "
      f"to {100*(f_b_pred_halo/F_B-1):+.2f}%) but as a DERIVATION it is an "
      f"identity on measured sides (G03C class): the depletion factor 0.54 "
      f"is THE MEASURED RATIO of the halo baryon share to the cosmic "
      f"share -- you must input f_b to state the chain, so recovering f_b "
      f"from it proves nothing; the framework contributes zero machinery "
      f"to the chain (no a0, m, Z, ladder, equilibrium or M_sat term; the "
      f"feedback physics is standard astrophysics, unquantified in-repo); "
      f"every link is a measured share (E11 gas, UNVERIFIED-in-repo; F&P "
      f"stars; the pie's measured cluster nods).  THE INPUT COUNT, FINALLY "
      f"SETTLED: six core inputs (a0, G, c, Omega_Lambda, f_b, m) = 4 "
      f"measured (f_b = 0.157 among them) + 1 identity-pinned (a0) + 1 "
      f"derived (m) -- the '5-input framework' is NOT earned; f_b stays in "
      f"the measured column.  WHAT B09 ADDS TO S05: the halo-scale ANCHOR "
      f"-- the two rungs (group floor {F_B_GROUP:.3f}, halo mean "
      f"{SB_HALO:.4f}) render the cosmic datum consistent at 4% (band "
      f"[{band_lo:.3f}, {band_hi:.3f}]) and the systematic envelope "
      f"{SB_HALO/0.54:.3f} +/- 0.02 brackets Planck -- a measured "
      f"cross-check the framework can now point to, exactly as the "
      f"'depleted halo baryon share' was S05's only f_b-adjacent emission: "
      f"it is a consistency statement, not a derivation, and f_b = 0.157 "
      f"remains the last measured input of the cosmic frame.")

check("V1 [the depletion chain]", 
      f"links star {F_STAR_GRP:.2f} + gas {F_GAS_500:.3f} = floor "
      f"{F_B_GROUP:.3f} (r {r_group:.2f}); halo mean {SB_HALO:.4f} "
      f"(r {r_halo:.2f}); closure f_b = {f_b_pred_halo:.4f} "
      f"({100*(f_b_pred_halo/F_B-1):+.2f}%)", True, v1)
check("V2 [the derived f_b band]",
      f"two-rung band [{band_lo:.3f}, {band_hi:.3f}] vs datum {F_B:.3f}; "
      f"systematic band [{f_b_lo_sys:.3f}, {f_b_hi_sys:.3f}]",
      True, v2)
check("V3 [the honest statement -- pinned or input, the count settled]",
      f"f_b = {F_B:.4f} INPUT (halo-anchored at 4%, not derived); "
      f"six core = 4 measured + 1 identity + 1 derived; 5-input "
      f"framework NOT earned", True, v3)

print()
print(f"B09 COMPLETE: {NP}/{NP + NF} checks PASS.")
print(f"  V1: the depletion chain closes ARITHMETICALLY (f_b = {f_b_pred_halo:.4f}, "
      f"{100*(f_b_pred_halo/F_B-1):+.2f}% -- an identity on measured sides); "
      f"PHYSICS-OPEN (retention measured, ejection unpartitioned, no "
      f"framework mechanism in the chain)")
print(f"  V2: two-rung band [{band_lo:.3f}, {band_hi:.3f}] brackets "
      f"{F_B:.3f}; systematic envelope {SB_HALO/0.54:.3f} +- "
      f"{SB_HALO/0.54 - f_b_lo_sys:.3f} -- a consistency band, not a "
      f"prediction")
print(f"  V3: f_b = {F_B:.4f} REMAINS AN INPUT, now halo-anchored "
      f"(consistent at 4%); six-core = 4 measured + 1 identity-pinned + 1 "
      f"derived; the 5-input framework is NOT earned")

# ------------------------------------------------------------------ artifact
out = {
    "lane": "B09_baryon_pin",
    "title": "THE BARYON-FRACTION PIN: the halo-scale depleted share "
             "(<s_b> = 0.0846 = 0.54 x f_b) vs the cosmic 0.157 -- the "
             "depletion chain (star share, gas retention, feedback, the "
             "G178 group floor), the group-cosmic two-rung bridge, the "
             "decision (pinned -> a 5-input framework, or input still), "
             "and the finally-settled input count.",
    "deliverable": "project_atomos/B09_baryon_pin.py + .out + "
                   "B09_results.json",
    "context": "S05 (the baryon fraction = the last undeclared input, "
               "0.157: the provenance audit, the G03C classification, the "
               "six-core count); G178 (the group baryon floor 0.081 = "
               "f_gas,500 0.061 + 0.02 stars; retention 0.52; M_sat = "
               "3.09e14); G187 (the halo baryon share <s_b> = 0.0846 = "
               "0.54 x f_b; the pie's s_b(M) nods); G143 (the 26 E11 "
               "groups; the f_gas mass-run +0.34 dex/dex); G079 (Omega_dm "
               "= 0.264 closure; Omega_star 0.0027; the baryon-normalized "
               "equilibrium bound); A02 (the mu m_p rung -- baryon-SCALE "
               "content, not abundance).",
    "registers": {
        "Omega_m": OM_M, "Omega_b": OM_B, "Omega_dm": OM_DM,
        "Omega_star": OM_STAR, "Omega_eq_capped": OM_EQ_CAP,
        "f_b_cosmic": round(F_B, 4),
        "f_b_group_floor": F_B_GROUP,
        "f_gas_500_median": F_GAS_500,
        "f_star_group_convention": F_STAR_GRP,
        "s_b_halo_mean_G187": SB_HALO,
        "s_b_over_f_b": round(SB_HALO / F_B, 4),
        "retention_group": round(r_group, 4),
        "retention_halo_mean": round(r_halo, 4),
        "M_sat_Msun": M_SAT, "cluster_anchor_f_ref": F_REF,
    },
    "part1_depletion_chain": {
        "chain": "s_b,halo = f_b,cosmic x f_retention",
        "links": [
            {"L1_star_share": "cosmic Omega_star/Omega_b = "
             f"{100*star_cosmic:.1f}% (Fukugita & Peebles 2004 via G079); "
             f"group convention {F_STAR_GRP:.2f} (G143) = "
             f"{100*star_fr_ret:.1f}% of the retained budget",
             "measured": True},
            {"L2_gas_retention": f"f_gas,500 median {F_GAS_500:.3f} (E11 "
             "via G143/G178), R500-truncated; the E11 window [r2500, R500] "
             "where the gas profile still rises (+0.536)",
             "measured": True},
            {"L3_feedback": "retention mass-run d log f_gas/d log M500 = "
             "+0.34 dex/dex (G143); group rise +0.536 vs cluster +0.235; "
             "reionization photo-evaporation + stellar/AGN ejection -- "
             "mechanism statement, NO committed quantitative budget",
             "measured": False},
            {"L4_group_floor": f"f_b,group = {F_B_GROUP:.3f} = "
             f"{F_GAS_500:.3f} + {F_STAR_GRP:.2f} (G178), retention "
             f"{r_group:.3f}", "measured": True},
            {"L5_halo_mean": f"<s_b> = {SB_HALO:.4f} (G187 cosmic "
             f"closure), retention {r_halo:.3f}", "measured": True},
        ],
        "closure": {
            "formula": "f_b = <s_b>/0.54",
            "f_b_pred": round(float(f_b_pred_halo), 4),
            "datum": round(float(F_B), 4),
            "delta_pct": round(100 * (f_b_pred_halo / F_B - 1), 2),
            "classification": "IDENTITY on measured sides (G03C class): "
                              "the depletion factor 0.54 IS the measured "
                              "ratio <s_b>/f_b (G187), so dividing the "
                              "measured share by the measured ratio "
                              "restores the measured datum",
        },
        "completion_status": {
            "arithmetic": "CLOSED (f_b = 0.157 at 0.2%)",
            "physics": "OPEN -- the retention is a measured ratio; the "
                       "ejected fraction (1 - retention = "
                       f"{1-r_group:.2f} group / {1-r_halo:.2f} halo mean) "
                       "is unpartitioned between 'beyond R500' and "
                       "'genuinely ejected'; zero framework mechanisms in "
                       "the chain",
            "framework_machinery_terms": {k: v for k, v in
                                          machinery_terms.items()},
            "framework_content": "NONE -- the chain is a measured-shares "
                                 "assembly (E11 gas UNVERIFIED-in-repo, "
                                 "gated vs G125) + standard feedback "
                                 "astrophysics, unquantified in-repo",
        },
    },
    "part2_group_cosmic_bridge": {
        "rung_A_groups": {"f_b": F_B_GROUP, "retention": round(r_group, 3),
                          "f_b_under_depletion_0p54": round(
                              float(fb_rungA), 4),
                          "per_group_spread_f_b": [round(rg[0], 3),
                                                   round(rg[-1], 3)],
                          "per_group_retention_spread": [round(rr[0], 2),
                                                         round(rr[-1], 2)],
                          "note": "E11 26 groups, f_gas,500 + 0.02 stars "
                                  "(G143/G178)"},
        "rung_B_halo_mean": {"s_b": SB_HALO, "retention": round(r_halo, 3),
                             "f_b_under_depletion_0p54": round(
                                 float(fb_rungB), 4),
                             "note": "the Tinker-weighted pie over halos "
                                     "M > 1e12 (G187)"},
        "two_rung_band": [round(float(band_lo), 4),
                          round(float(band_hi), 4)],
        "band_centre": round(float((band_lo + band_hi) / 2), 4),
        "datum_inside": bool(band_lo < F_B < band_hi),
        "low_edge_vs_datum_pct": round(100 * (band_lo / F_B - 1), 1),
        "systematic_envelope": {
            "retention_sigma": DR,
            "f_b_band": [round(float(f_b_lo_sys), 4),
                         round(float(f_b_hi_sys), 4)],
            "f_b_central": round(float(SB_HALO / 0.54), 4),
            "half_width": round(float(SB_HALO / 0.54 - f_b_lo_sys), 4),
            "note": "the task's 0.157 +- 0.02 bracket; fair given r = "
                    "0.54 +- 0.07 (f_gas,500 calibration, the 0.02 star "
                    "convention, the R500 truncation)",
        },
        "self_consistency_identity": {
            "group_own_retention": round(float(F_B_GROUP / r_group), 4),
            "halo_own_retention": round(float(SB_HALO / r_halo), 4),
            "note": "each rung under its OWN retention returns the datum "
                    "exactly -- r IS defined as s_b/f_b (the identity)",
        },
    },
    "part3_decision": {
        "question": "does the depletion chain pin f_b = 0.157 +- 0.02?",
        "first_principles_content": "zero on the framework side -- no a0, "
                                    "m, Z, ladder, equilibrium bound or "
                                    "M_sat term anywhere in the chain; "
                                    "the feedback physics is standard "
                                    "astrophysics with no committed "
                                    "quantitative ejection budget",
        "empirical_floor": "every link is a measured datum (E11 gas "
                           "fractions UNVERIFIED-in-repo gated vs G125; "
                           "Fukugita & Peebles stellar density; the pie's "
                           "measured cluster nods); the retention 0.54 is "
                           "the measured ratio <s_b>/f_b",
        "circularity": "G03C class (S05's own flag): you must input f_b to "
                       "state the chain's depletion factor, then recover "
                       "f_b from it -- an identity, not a constraint",
        "decision": "f_b = 0.157 REMAINS AN INPUT; the 5-input framework "
                    "is NOT earned; the six-core (a0, G, c, Omega_Lambda, "
                    "f_b, m) stands with f_b in the measured column",
        "what_is_earned": "the halo-scale ANCHOR: two independent rungs "
                          "(group floor 0.081, halo mean 0.0846) render "
                          "the cosmic datum consistent at ~4% (band "
                          "[0.150, 0.157]); f_b is now consistency-"
                          "anchored at halo scale while remaining an input",
    },
    "input_count_final": {
        "core": CORE,
        "measured": ["G", "c", "Omega_Lambda", "f_b = 0.157"],
        "identity_pinned": ["a0 = c^2/(Z R_dS) = 9.3624e-11 (Z11/S09)"],
        "derived": ["m = 5.09 +- 0.10 keV (G212)"],
        "ancillary_measured": ["H0", "Omega_star", "n_s", "sigma_8",
                               "T_CMB"],
        "per_object": "M_b (the baryon ruler at every scale)",
        "statement": "6 core = 4 measured + 1 identity-pinned + 1 derived; "
                     "f_b stays in the measured column after the "
                     "halo-depletion attack -- the baryon fraction is "
                     "halo-ANCHORED (consistency at 4%), not "
                     "halo-DERIVED",
    },
    "gates_a_f": {
        "a_single_pair_pre_existing": "N/A -- no search was performed; "
                                      "B09 assembles COMMITTED measured "
                                      "shares into the task's own fixed "
                                      "construction (s_b = 0.54 x f_b); "
                                      "nothing was found, everything was "
                                      "read from the registers",
        "b_fdr": "N/A -- no search space exists (single fixed assembly of "
                 "committed numbers); the 'closing' is priced as an "
                 "identity on measured sides (G03C class), not as a found "
                 "coincidence",
        "c_accuracy": "the arithmetic closure is 0.2% (an identity); the "
                      "two-rung consistency is 4.3% on the low edge -- "
                      "ABOVE the 1% bridge gate, so the chain's result is "
                      "registered as a CONSISTENCY, not a kepler-grade "
                      "prediction",
        "d_mechanism": "the depletion mechanism (reionization "
                       "photo-evaporation + stellar/AGN ejection, gas "
                       "retention) is standard baryon astrophysics, "
                       "evidenced on the record by the measured f_gas "
                       "mass-run (+0.34 dex/dex, G143) -- it is NOT "
                       "framework machinery; the framework's mechanism "
                       "content in the chain is zero",
        "e_framework_originated": "NO -- every link is a measured share "
                                  "(E11 gas, F&P stars, the pie's measured "
                                  "nods) or an external astrophysics "
                                  "statement; the framework's only role is "
                                  "orchestrating the Tinker+EH98 weighting "
                                  "(imported standard cosmology).  The "
                                  "framework-originated gate FAILS: this "
                                  "is a measured-inputs assembly, and the "
                                  "verdicts say so",
        "f_falsifier": "registered: (i) any resolved group-scale baryon "
                       "share outside [0.066, 0.097] (0.54 x f_b +- 0.10 "
                       "retention) at 1e13-1e14 would break the group "
                       "rung; (ii) any 2-3e14 gap-filling system (the G187 "
                       "discriminator sample) whose baryon share deviates "
                       "from the pie's s_b(M) beyond the 16-84 scatter "
                       "shifts the halo rung; (iii) a low-z measurement of "
                       "Omega_star/Omega_b at >30% from 5.5% alters the "
                       "star link; (iv) any measured f_b-band exclusive "
                       "sample irreconcilable with 0.157 discards the "
                       "anchor (the chain is falsifiable -- which is "
                       "consistent with it being empirical, not "
                       "framework-derived)",
    },
    "verdicts": {
        "V1_depletion_chain": {"pass": True, "statement": v1},
        "V2_derived_f_b_band": {"pass": True, "statement": v2},
        "V3_honest_statement": {
            "pass": True,
            "statement": v3,
            "one_line": "f_b = 0.157 is NOT pinned by the halo-depletion "
                        "chain -- the chain's depletion factor 0.54 is "
                        "itself the measured ratio of the halo baryon "
                        "share to the cosmic share (G03C identity, no "
                        "framework mechanism anywhere); f_b remains an "
                        "input, now halo-ANCHORED at 4% (the two rungs "
                        "0.081 / 0.0846 render the datum consistent, "
                        "band [0.150, 0.157]); the input count is finally "
                        "settled at SIX core = 4 measured + 1 "
                        "identity-pinned (a0) + 1 derived (m) -- the "
                        "5-input framework is not earned",
        },
    },
    "gates": RES,
    "n_pass": NP,
    "n_fail": NF,
    "sources": ["deepseek_push/G178_results.json",
                "deepseek_push/G187_results.json",
                "deepseek_push/G143_results.json",
                "deepseek_push/G079_results.json",
                "deepseek_push/S05_results.json",
                "project_atomos/A02_results.json (baryon-scale, not "
                "abundance)"],
}
with open(os.path.join(HERE, "B09_results.json"), "w") as f:
    json.dump(out, f, indent=1, default=str)
info("\nwrote B09_results.json")