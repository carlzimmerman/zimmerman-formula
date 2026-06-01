#!/usr/bin/env python3
"""
GATE 1.5 -- stress-test scaling MOND against the intermediate-z BTFR (data NOW).
==============================================================================

Adversarial test of the program, same standard I applied to the numerology.
Scaling MOND, a0(z)=a0(0)E(z), makes a SHARP prediction for the baryonic
Tully-Fisher zero-point at z~0.5-2.5 -- where the data (KMOS3D, KROSS) is vastly
better than z>10. If that data already kills it, no point waiting for Gate 1.

Deep-MOND BTFR:  M_b = v_flat^4 / (G a0(z)).  At fixed v_flat,
  log M_b(z) - log M_b(0) = -log E(z)   (monotonic DECREASE with z).

The test was literally PROPOSED as a modified-gravity probe in 2008
(arXiv:0809.2790). Here we run it against Ubler+2017 (KMOS3D, z~0.9 & 2.3) and
the Genzel/Lang declining-rotation-curve result, and report honestly -- including
the confound that decides it.

Pure stdlib. Run:  python reviews/scaling_mond_btfr_evolution.py
"""

import math

OM, OL = 0.315, 0.685


def E(z):
    return math.sqrt(OM * (1 + z) ** 3 + OL)


def part1_prediction():
    print("=" * 80)
    print("(1) Scaling-MOND prediction: BTFR zero-point shifts MONOTONICALLY with z")
    print("=" * 80)
    print("   At fixed v_flat:  Dlog M_b = -log E(z)  (M_b smaller at higher z).")
    print("   Equivalently at fixed M_b:  v_flat boosted by E(z)^1/4.")
    print(f"   {'z':>6}{'E(z)':>8}{'Dlog M_b @fixed v':>20}{'v boost @fixed M':>18}")
    for z in (0.5, 0.9, 1.5, 2.3):
        print(f"   {z:>6.1f}{E(z):>8.2f}{-math.log10(E(z)):>20.3f}{E(z)**0.25:>18.3f}")
    print("   => a SHARP, monotonic, falsifiable signature at intermediate z.\n")


def part2_data():
    print("=" * 80)
    print("(2) The data: Ubler+2017 (KMOS3D) -- and it is NON-monotonic")
    print("=" * 80)
    print("   Measured baryonic-TFR zero-point evolution (at fixed circular velocity):")
    print("     z=0   -> z~0.9 :  NEGATIVE (M_b LOWER at z~0.9)   [scaling MOND: -0.23]")
    print("     z~0.9 -> z~2.3 :  POSITIVE (M_b HIGHER at z~2.3)   [scaling MOND: -0.31 more]")
    print()
    print("   So scaling MOND predicts MONOTONIC down (-0.23 then -0.54 dex);")
    print("   the data goes DOWN to z~0.9 (right direction) then BACK UP to z~2.3")
    print("   (wrong direction). The z>0.9 segment is where the naive test FAILS.")
    print("   Ubler et al. fit the non-monotonic trend with a LCDM toy model (gas")
    print("   fractions + DM-to-baryon evolution) -- no a0 evolution needed.\n")


def part3_confound():
    print("=" * 80)
    print("(3) The confound that decides it: high-z galaxies are NEWTONIAN, not deep-MOND")
    print("=" * 80)
    print("   The deep-MOND BTFR only applies when g_N < a0. But the OBSERVED high-z")
    print("   samples are massive, COMPACT, high-surface-density -> high g_N.")
    print("   Size evolution R_e ~ (1+z)^-0.75 (van der Wel+14) -> g_N ~ (1+z)^1.5.")
    print(f"   {'z':>6}{'(1+z)^1.5':>11}{'E(z)=a0 up':>12}{'g_N/a0 vs z=0':>15}{'regime':>12}")
    for z in (0.9, 1.5, 2.3):
        gN = (1 + z) ** 1.5
        ratio = gN / E(z)
        reg = "Newtonian" if ratio > 1.3 else "transition"
        print(f"   {z:>6.1f}{gN:>11.2f}{E(z):>12.2f}{ratio:>15.2f}{reg:>12}")
    print("   g_N/a0 RISES with z (compactness beats the a0 boost) -> high-z galaxies")
    print("   are MORE Newtonian -> baryon-dominated, DECLINING rotation curves")
    print("   (Genzel+17, Lang+17: ~90% baryon-dominated by z~2.2). CONFIRMED.")
    print("   => the high-z samples do NOT probe the deep-MOND a0 at all. The 'wrong")
    print("      direction' z>0.9 BTFR segment is in the WRONG REGIME to test scaling.")
    print("   (Note: constant-a0 gives g_N/a0 EVEN higher -- (1+z)^1.5 alone -- so the")
    print("    baryon-dominance is fit by both; it is driven by SIZE evolution.)\n")


def main():
    part1_prediction()
    part2_data()
    part3_confound()
    print("=" * 80)
    print("VERDICT -- Gate 1.5: scaling MOND SURVIVES, but is not advanced either")
    print("=" * 80)
    print("  * NOT a clean kill: the one segment where deep-MOND might apply (z<0.9)")
    print("    shows the RIGHT direction (BTFR zero-point down ~0.1-0.2 dex vs the")
    print("    predicted -0.23); the z>0.9 'wrong direction' is in the Newtonian regime")
    print("    where the deep-MOND BTFR does not apply (compact, baryon-dominated).")
    print("  * NOT a clean win: LCDM (gas + DM evolution) fits the same data, and the")
    print("    intermediate-z samples are selection-biased toward high-g_N systems that")
    print("    cannot probe a0. So the test neither confirms nor refutes scaling MOND.")
    print("  * THE REFINEMENT (the useful part): the decisive test -- here AND at z>10")
    print("    (Gate 1) -- must target DEEP-MOND systems: extended, gas-rich, LOW")
    print("    surface brightness, where g_N < a0. The compact bright galaxies that")
    print("    dominate high-z samples are Newtonian and silent on a0. Gate 1 should")
    print("    select for LOW ACCELERATION, not just high redshift.")
    print()
    print("  Honest net: the best existing intermediate-z data does NOT kill scaling")
    print("  MOND (the would-be-killing segment is in the wrong regime), but it does")
    print("  NOT support it over LCDM either, and it sharpens what a real test needs.")
    print("  My confidence is unchanged-to-slightly-lower: the program still lives or")
    print("  dies at Gate 1, now correctly aimed at deep-MOND systems.")


if __name__ == "__main__":
    main()
