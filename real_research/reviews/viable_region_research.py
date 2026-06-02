#!/usr/bin/env python3
"""
Research into the viable region: z>4 extended galaxies -- what is ACTUALLY distinctive?
======================================================================================

The parameter-space review located the only testable corner: z>4, extended (deep-MOND)
galaxies, cross-channel coherence + RAR tightness. Before designing the test, honest
research has to ask the hard question first:

   Is the cross-channel COHERENCE actually distinctive from LCDM, or does LCDM forge it too?

The answer (Part 1) is uncomfortable, and it sends us to look for something that survives
(Parts 2-4). One genuinely distinctive prediction emerges -- the REDSHIFT EVOLUTION OF THE
EXTERNAL FIELD EFFECT -- which the round-2 red-team missed by conflating it with a withdrawn
(div B) claim. Run: python <thisfile>   (needs numpy)
"""
import numpy as np

OM, OL = 0.315, 0.685
E = lambda z: np.sqrt(OM * (1 + z) ** 3 + OL)
ZS = [0.0, 2.3, 4.0, 6.0, 10.0]


def part1_coherence_is_degenerate():
    print("=" * 82)
    print("PART 1 -- is the cross-channel coherence distinctive? (No.)")
    print("=" * 82)
    print("   The channels all derive from the deep-MOND relation M_dyn/M_bar=sqrt(a0/g_bar):")
    print("     M_dyn/M* ~ sqrt(a0) ~ sqrt(E);  v,sigma ~ a0^1/4 ~ E^1/4;  BTFR0 ~ -log a0 ~ -log E.")
    print("   These powers follow from ONE thing: the RAR knee sitting at a0(z).")
    print("   But Magneticum shows LCDM's APPARENT a0 also rises ~ E(z) (x3 by z=2.3 = E(2.3)=3.46).")
    print("   So in LCDM's RAR, the SAME deep-MOND algebra gives the SAME powers off apparent-a0(z):")
    print(f"   {'z':>5}{'E(z)':>8}{'framework powers':>22}{'LCDM (apparent a0~E)':>24}")
    for z in ZS:
        e = E(z)
        fw = f"sqrtE={np.sqrt(e):.2f},E^.25={e**.25:.2f}"
        print(f"   {z:>5}{e:>8.2f}{fw:>22}{'SAME (a0_app~E)':>24}")
    print("   => the COHERENCE (all channels off one E(z)) is NOT distinctive: LCDM, with apparent")
    print("      a0 ~ E(z), reproduces every channel power. The signature I claimed is degenerate.")
    print("      What is left must live in (a) SCATTER, (b) the high-z AMPLITUDE, (c) the EFE.\n")


def part2_scatter():
    print("=" * 82)
    print("PART 2 -- RAR intrinsic scatter: a clean discriminator, but the trend leans LCDM")
    print("=" * 82)
    print("   Universal a0(z) (framework) => intrinsic RAR scatter ~ 0 at every z (one a0 for all).")
    print("   LCDM (halo-to-halo variation) => scatter GROWS with z. Observed (to z~0.9):")
    print("     0.13 dex (low z) -> 0.19 dex (z~0.9), i.e. RISING -- the LCDM expectation.")
    print("   Naive linear extrapolation of that trend:")
    slope = (0.19 - 0.13) / 0.9
    for z in (2.3, 4.0, 6.0):
        print(f"     z={z}: scatter ~ {0.13 + slope*z:.2f} dex (if the trend holds)")
    print("   To VINDICATE the framework, the z>4 intrinsic scatter must be SMALL (<~0.1 dex)")
    print("   against this rising trend. Current data point the other way. [clean test; leans LCDM]\n")


def part3_amplitude():
    print("=" * 82)
    print("PART 3 -- the high-z amplitude: a discriminator only if LCDM DEVIATES from E(z)")
    print("=" * 82)
    print("   Framework: a0(z)=a0(0)E(z), a definite, steep rise. LCDM apparent-a0 is MEASURED")
    print("   to track E(z) only to z=2.3 (Magneticum); beyond that it is UNMAPPED (no sims).")
    print(f"   {'z':>5}{'framework a0/a0_0':>18}{'LCDM apparent a0/a0_0':>24}")
    for z in ZS:
        lcdm = f"{E(z):.1f} (to z=2.3)" if z <= 2.3 else "UNMAPPED"
        print(f"   {z:>5}{E(z):>18.1f}{lcdm:>24}")
    print("   If LCDM's apparent a0 SATURATES at z>4 (plausible: halos stop densifying vs a0)")
    print("   while the framework keeps rising x10 (z6), x20 (z10), THAT amplitude gap is the")
    print("   discriminator. But it needs BOTH a z>4 LCDM benchmark AND z>4 data -- neither exists.\n")


def part4_efe_evolution():
    print("=" * 82)
    print("PART 4 -- the EFE redshift-evolution: the one GENUINELY distinctive prediction")
    print("=" * 82)
    print("   The STANDARD MOND External Field Effect (NOT the withdrawn div-B claim): a system in")
    print("   an external field g_ext has its internal deep-MOND behavior suppressed when")
    print("   g_ext > a0. The strength is eta = g_ext/a0. With a0 -> a0(z)=a0(0)E(z), the SAME")
    print("   environment gives a SMALLER eta at high z -> the EFE WEAKENS as 1/E(z):")
    print(f"   take a moderate local environment g_ext = a0(0) (eta_0 = 1):")
    print(f"   {'z':>5}{'eta(z)=1/E(z)':>16}{'EFE regime':>22}")
    for z in ZS:
        eta = 1.0 / E(z)
        reg = "strong (suppressed)" if eta > 0.5 else ("moderate" if eta > 0.15 else "weak (isolated-MOND)")
        print(f"   {z:>5}{eta:>16.3f}{reg:>22}")
    print("   PREDICTION: high-z galaxies in dense environments are LESS EFE-suppressed than local")
    print("   analogs -- they behave more like isolated deep-MOND systems. This is distinct from:")
    print("     * LCDM:           the host does NOT affect the internal RAR at all (no EFE, any z).")
    print("     * constant-a0 MOND: EFE present but SAME strength at all z.")
    print("   So measuring environment-dependence of the RAR AND its z-evolution separates all")
    print("   three. This survived the red-team (the real EFE is inherited; its 1/E(z) MODULATION")
    print("   is the framework's distinctive, falsifiable addition). [DISTINCTIVE -- the best shot]\n")


def verdict():
    print("=" * 82)
    print("RESEARCH VERDICT -- the viable region, mapped honestly")
    print("=" * 82)
    print("  DEGENERATE (drop it):  the cross-channel coherence -- LCDM's apparent a0 ~ E(z)")
    print("     reproduces every channel power. Not the signature.")
    print("  LEANS LCDM (clean but unfavorable): the RAR intrinsic scatter -- universal a0 wants")
    print("     ~0, but the observed scatter GROWS with z; z>4 must break that trend to vindicate.")
    print("  UNMAPPED (needs a benchmark): the high-z amplitude -- distinctive only if LCDM")
    print("     apparent-a0 saturates at z>4, which no simulation has computed.")
    print("  DISTINCTIVE (the real target): the EFE's 1/E(z) WEAKENING -- unique vs both LCDM")
    print("     (no EFE) and constant-a0 MOND (constant EFE). The framework's best falsifiable card.")
    print()
    print("  CONCRETE PROGRAM for the viable region (what to actually measure at z>4):")
    print("   1. environment-split RAR: isolated vs grouped EXTENDED galaxies at z~4-6, and the")
    print("      same at z~0 -- test for EFE present AND weakening (the distinctive signal).")
    print("   2. intrinsic RAR scatter at z>4 (must be <~0.1 dex to survive).")
    print("   3. apparent a0 at z~6 to ~10% on extended galaxies (vs a future LCDM z>4 benchmark).")
    print("  Honest odds: the one clean, distinctive card is the EFE evolution; the others are")
    print("  degenerate, unfavorable, or un-benchmarked. The framework is testable -- but its best")
    print("  distinctive prediction is also its hardest to measure, and it has no z>4 data.")
    print("=" * 82)


def main():
    part1_coherence_is_degenerate(); part2_scatter(); part3_amplitude()
    part4_efe_evolution(); verdict()


if __name__ == "__main__":
    main()
