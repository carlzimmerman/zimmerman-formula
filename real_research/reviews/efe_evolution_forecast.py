#!/usr/bin/env python3
"""
Rigorous feasibility forecast for the EFE-evolution test (the one distinctive card).
====================================================================================

The framework's single distinctive, falsifiable prediction (viable_region_research.py): the
MOND External Field Effect weakens with redshift, eta = g_ext/a0(z) ~ 1/E(z), because a0(z)
rises. Concretely, for a galaxy of fixed baryonic acceleration g_bar in a fixed external
environment g_ext, the EFE SUPPRESSION of its mass discrepancy shrinks as z grows.

This file forecasts whether that is measurable. It (1) solves the MOND EFE numerically, (2)
computes the SIGNAL (the z-evolution of the embedded-vs-isolated offset), (3) builds an honest
per-galaxy error budget, (4) derives the SAMPLE SIZE for a 3-sigma detection that also separates
the framework from LCDM (no EFE) and constant-a0 MOND (non-evolving EFE), and (5) judges
feasibility against real JWST/ELT capability. No number is rigged.

MOND EFE model (standard scalar/algebraic AQUAL, simple interpolation mu(x)=x/(1+x)):
   solve   mu((g_obs + g_ext)/a0) * g_obs = g_bar   for g_obs.
   g_ext=0 -> isolated MOND;  g_ext>>g_obs -> g_obs = g_bar/mu(g_ext/a0) (EFE-dominated).

Run: python <thisfile>   (needs numpy)
"""
import numpy as np

OM, OL = 0.315, 0.685
E = lambda z: np.sqrt(OM * (1 + z) ** 3 + OL)
A0 = 1.2e-10                      # a0(0) [m/s^2]
mu = lambda x: x / (1.0 + x)


def g_obs(g_bar, g_ext, a0):
    """Solve mu((g_obs+g_ext)/a0)*g_obs = g_bar by bisection. All in SI."""
    f = lambda go: mu((go + g_ext) / a0) * go - g_bar
    lo, hi = 1e-18, 1e-6
    for _ in range(200):
        mid = np.sqrt(lo * hi)            # log-bisection (positive, spans many decades)
        if f(mid) < 0:
            lo = mid
        else:
            hi = mid
    return np.sqrt(lo * hi)


def offset_dex(g_bar0, g_ext0, z):
    """log10 of (boost_embedded / boost_isolated) at redshift z, for FIXED physical
    g_bar0, g_ext0 (in units of a0(0)). The EFE suppression (negative = suppressed)."""
    a0z = A0 * E(z)
    gb, ge = g_bar0 * A0, g_ext0 * A0          # fixed physical accelerations
    B_iso = g_obs(gb, 0.0, a0z) / gb
    B_emb = g_obs(gb, ge, a0z) / gb
    return np.log10(B_emb / B_iso)


# ===========================================================================
def part1_signal():
    print("=" * 80)
    print("PART 1 -- the SIGNAL: EFE suppression vs z (it must SHRINK toward 0)")
    print("=" * 80)
    print("   fixed deep-MOND galaxy g_bar=0.1 a0(0); three environments g_ext/a0(0):")
    print(f"   {'z':>5}{'E(z)':>7}", end="")
    envs = [0.3, 0.5, 1.0]
    for e in envs:
        print(f"{'gext='+str(e):>12}", end="")
    print()
    sig = {}
    for z in (0.0, 1.0, 2.0, 4.0, 6.0):
        print(f"   {z:>5}{E(z):>7.2f}", end="")
        for e in envs:
            off = offset_dex(0.1, e, z)
            sig.setdefault(e, {})[z] = off
            print(f"{off:>12.3f}", end="")
        print()
    print("   (each entry = log10[boost_embedded/boost_isolated]; 0 = no EFE)")
    print()
    print("   SIGNAL = offset(z=0) - offset(z=6)  [how much the EFE weakening moves the obs]:")
    for e in envs:
        s = sig[e][0.0] - sig[e][6.0]
        print(f"     g_ext={e} a0: signal = {abs(s):.3f} dex over z=0->6")
    print("   => the distinctive signal is ~0.1-0.15 dex. Stronger environments give more, but")
    print("      the galaxy must stay deep-MOND (g_bar<a0(z)) and g_ext<a0(z). [SMALL signal]\n")
    return max(abs(sig[e][0.0] - sig[e][6.0]) for e in envs)


def part2_error_budget():
    print("=" * 80)
    print("PART 2 -- honest per-galaxy error budget on log(M_dyn/M_bar) at z>4")
    print("=" * 80)
    terms = [
        ("M_dyn (sigma or v_rot + size)", 0.20, "NIRSpec kinematics, ~10-30 km/s; size; incl."),
        ("M_* (SED fit: IMF, SFH, dust)", 0.25, "stellar mass systematics at z>4"),
        ("M_gas (rarely measured at z>4)", 0.20, "gas can dominate baryons; ~unconstrained"),
        ("intrinsic RAR scatter (floor)",  0.15, "the irreducible astrophysical scatter"),
    ]
    var = 0.0
    print(f"   {'term':34}{'sigma[dex]':>11}   note")
    for name, s, note in terms:
        print(f"   {name:34}{s:>11.2f}   {note}")
        var += s * s
    sig_gal = np.sqrt(var)
    print(f"   ---> per-galaxy sigma(log M_dyn/M_bar) = sqrt(sum) = {sig_gal:.2f} dex")
    print("   (optimistic floor if gas measured + tight SED: ~0.25 dex). [LARGE vs the signal]\n")
    return sig_gal


def part3_sample_size(signal, sig_gal):
    print("=" * 80)
    print("PART 3 -- sample size for a 3-sigma detection of the EFE WEAKENING")
    print("=" * 80)
    print("   The test compares 4 sub-sample means: {isolated,embedded} x {low-z,high-z}.")
    print("   The framework signal is the CHANGE in the embedded-isolated offset across z,")
    print("   ~Delta = {:.3f} dex. To resolve it at 3 sigma the error on that double-difference".format(signal))
    print("   must be Delta/3. With sigma_gal per galaxy and 4 equal bins of N each,")
    print("   sigma(double-diff) = sigma_gal * sqrt(4/N).")
    for label, sg in [("realistic sigma_gal=%.2f" % sig_gal, sig_gal), ("optimistic 0.25", 0.25)]:
        # 3 = signal / (sg*sqrt(4/N))  ->  N = 4 * (3*sg/signal)^2
        N = 4 * (3 * sg / signal) ** 2
        print(f"     {label} dex:  N ~ {N:.0f} per bin  ->  ~{4*N:.0f} galaxies total")
    print("   ALSO required, and not in the noise budget above:")
    print("     * ENVIRONMENT classification (isolated vs embedded) at z>4 -- needs dense")
    print("       spectroscopic group/field membership, itself a major survey;")
    print("     * MATCHED physical g_ext across z (environments evolve) -- measure g_ext per")
    print("       galaxy from local density / host; a further systematic;")
    print("     * EXTENDED (deep-MOND) targets only -- compact ones are Newtonian (no signal).\n")
    return 16 * (3 * sig_gal / signal) ** 2          # TOTAL galaxies = 4 bins x N_per_bin


def part4_discrimination():
    print("=" * 80)
    print("PART 4 -- what the measurement separates (the three hypotheses)")
    print("=" * 80)
    print("   Holding g_ext, g_bar matched across z, the embedded-isolated offset(z) predicts:")
    print("     LCDM            : offset(z) = 0 at all z      (host does not affect internal RAR)")
    print("     constant-a0 MOND: offset(z) = const  != 0     (EFE present, non-evolving)")
    print("     framework       : offset(z) -> 0 as z grows   (EFE ~1/E(z), weakening)")
    print("   So the test has TWO levels:")
    print("     (i)  offset != 0 at low z  -> MOND vs LCDM  (this is the classic EFE detection);")
    print("     (ii) d(offset)/dz < 0      -> framework vs constant-a0 MOND (the NEW, distinctive bit).")
    print("   Only (ii) is unique to this framework, and it is the smaller, harder signal.\n")


def verdict(total_real, total_opt):
    print("=" * 80)
    print("FEASIBILITY VERDICT")
    print("=" * 80)
    print(f"   signal ~0.1-0.15 dex; per-galaxy noise ~0.25-0.36 dex; required sample")
    print(f"   ~{total_opt:.0f} (optimistic) to ~{total_real:.0f} (realistic) EXTENDED, environment-")
    print("   classified, kinematically-resolved galaxies at z>4 -- with measured g_ext and")
    print("   baryonic (incl. gas) masses.")
    print("   Reality check on capability:")
    print("     * current JWST high-z kinematic samples: tens of galaxies, mostly COMPACT")
    print("       (Newtonian -> no signal), no environment split, no gas masses.")
    print("     * the required sample is ~10x larger, selected for EXTENT, with environment +")
    print("       gas -- a dedicated multi-cycle JWST+ALMA(+ELT) program, plausibly next-decade.")
    print("   HONEST VERDICT: the distinctive prediction is real and falsifiable IN PRINCIPLE, but")
    print("   its signal (~0.1 dex) sits below the per-object noise, so it needs a few-hundred-")
    print("   galaxy, environment-resolved, extended-target campaign that does NOT yet exist and")
    print("   is beyond current JWST programs. It is a next-generation test, not a this-cycle one.")
    print("   The classic EFE detection (level i) is nearer-term; the EVOLUTION (level ii, the")
    print("   distinctive part) is the hard, long-horizon measurement.")
    print("=" * 80)


def main():
    signal = part1_signal()
    sig_gal = part2_error_budget()
    total_real = part3_sample_size(signal, sig_gal)
    total_opt = 16 * (3 * 0.25 / signal) ** 2        # TOTAL galaxies (4 bins)
    part4_discrimination()
    verdict(total_real, total_opt)


if __name__ == "__main__":
    main()
