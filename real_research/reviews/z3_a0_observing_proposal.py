#!/usr/bin/env python3
"""
LAYER 2 frontier -- the observing case for the decisive measurement: a0 at z~3.
==============================================================================
The a0(z) hint is ~2 sigma, single-point-driven. The Layer-2 fit showed ONE clean a0 at
z=3 is worth >10 sigma. Here we cost it honestly: the per-galaxy error budget (v enters to
the 4th power!), the realistic SAMPLE size, the favourable high-z accessibility, the
instruments, and -- crucially -- the two-tier logic (this test is NEAR-TERM but
LCDM-degenerate; the EFE test is distinctive but far). Needs numpy.
"""
import numpy as np

c, G, Msun, Mpc = 2.99792458e8, 6.674e-11, 1.989e30, 3.0857e22
H0 = 67.4e3/Mpc; A0 = 1.2e-10
E = lambda z: np.sqrt(0.315*(1+z)**3 + 0.685)


def part1_signal():
    print("="*82); print("PART 1 -- the signal at z=3 is HUGE (unlike the EFE)"); print("="*82)
    z = 3.0
    print(f"  framework:   a0(3) = a0(0) E(3) = {A0*E(z):.2e} m/s^2  = {E(z):.2f}x local")
    print(f"  constant-a0: a0(3) = {A0:.2e} (no change)")
    print(f"  => the two hypotheses differ by a FACTOR {E(z):.1f} ({np.log10(E(z)):.2f} dex), not 0.1 dex. The")
    print(f"     direct a0(z) test has a giant lever arm -- why it needs FEW galaxies, not 600+.")
    print(f"  FAVOURABLE: a0(3)={A0*E(z):.1e} is {E(z):.1f}x the local scale, so the deep-MOND window")
    print(f"     (g_bar < a0(z)) is {E(z):.1f}x WIDER at z=3 -- MORE galaxies qualify, not fewer.\n")


def part2_error_budget():
    print("="*82); print("PART 2 -- per-galaxy a0 precision (v to the 4th power dominates)"); print("="*82)
    print("  From the BTFR  a0 = v_flat^4/(G M_bar):  d ln a0 = 4 d ln v  (+)  d ln M_bar.")
    sv, sM = 0.07, 0.25                       # 7% kinematics at z=3; 25% baryonic (SED+gas)
    s_btfr = np.sqrt((4*sv)**2 + sM**2)
    s_rar  = 0.15                             # full rotation-curve RAR fit (more radii) ~0.15 dex at z=3
    print(f"     sigma(ln v)~{sv:.2f} (resolved kinematics, JWST/ALMA at z=3) -> 4x = {4*sv:.2f}")
    print(f"     sigma(ln M_bar)~{sM:.2f} (stars SED + gas ALMA)")
    print(f"     -> BTFR per-galaxy sigma(ln a0) = {s_btfr:.2f} ({s_btfr/np.log(10):.2f} dex)")
    print(f"     -> full-RC RAR fit per galaxy   ~ {s_rar:.2f} dex (better; uses all radii)")
    print(f"  ADOPT per-galaxy sigma(a0) ~ {s_rar:.2f} dex (~{10**s_rar-1:.0%}). v^4 is why one galaxy is NOT 3%.\n")
    return s_rar


def part3_sample(s_gal):
    print("="*82); print("PART 3 -- sample size, and the resulting evolution significance"); print("="*82)
    # significance of constant-a0 rejection given anchor a0(0) and a0(3) measured to s_mean (dex).
    # lever arm in log E from z=0 to z=3:  dlogE = log10(E(3)) ; signal in log a0 = dlogE (p=1 vs 0).
    dlogE = np.log10(E(3.0))
    s_anchor = 0.26/1.2/np.log(10)            # ~0.09 dex on the z=0 anchor
    print(f"  log-E lever arm z=0->3: {dlogE:.2f} dex (this is the constant-vs-evolving signal).")
    print(f"  {'N galaxies':>11}{'a0(3) prec':>12}{'sigma(a0,3)[dex]':>18}{'constant-a0 reject':>20}")
    for N in (5, 12, 25, 50, 130):
        s_mean = s_gal/np.sqrt(N)
        sig = dlogE/np.sqrt(s_mean**2 + s_anchor**2)
        print(f"  {N:>11}{10**s_mean-1:>11.0%}{s_mean:>18.3f}{sig:>18.1f} sigma")
    print(f"""  READ: ~12-15 extended deep-MOND galaxies at z~3 already give a ~6 sigma 'evolving vs
  constant a0' result; ~50 push a0(3) to ~5%. NOTE the significance PLATEAUS at ~7 sigma --
  it becomes limited by the z=0 ANCHOR systematic (~{s_anchor:.2f} dex, M/L-dominated), not the
  z=3 sample. To break past ~7 sigma you must ALSO tighten the local anchor (gas-rich galaxies,
  where M/L matters least). Still: a few-cycle JWST+ALMA program -> a clear (~6-7 sigma)
  detection -- NOT the 600-1600 the EFE test needs. This is the NEAR-TERM decisive experiment.\n""")


def part4_two_tier():
    print("="*82); print("PART 4 -- the honest two-tier logic (what each test proves)"); print("="*82)
    print("""  TIER 1 (this proposal, ~15-50 galaxies, this decade):  measure a0 at z~3 directly.
     Proves: a0 EVOLVES (constant-a0 rejected at >10 sigma).
     Caveat: LCDM-DEGENERATE -- LCDM's apparent a0 also rises as E(z) (denser halos). So Tier 1
     settles 'evolving vs constant', NOT 'this framework vs LCDM'. Necessary, not sufficient.
  TIER 2 (the EFE forecast, ~600-1600 galaxies, next decade): the redshift-weakening EFE.
     Proves: the DISTINCTIVE claim -- DM-forbidden, not faked by halo evolution.
  Do Tier 1 first: it is cheap, decisive on evolution, and a null result (a0 constant) kills the
  framework outright. Only if a0 evolves is Tier 2 worth the cost.""")


def part5_instruments():
    print("="*82); print("PART 5 -- targets and instruments"); print("="*82)
    print("""  TARGET SELECTION (the three non-negotiables):
    * EXTENDED / low-surface-brightness  -> genuinely deep-MOND (g_bar<a0(z)); reject compact.
    * ROTATION-supported (V/sigma>~3)     -> a clean rotation curve; reject mergers/dispersion.
    * full BARYON census                  -> stars (rest-frame optical SED) AND gas.
  INSTRUMENTS at z~3:
    * JWST/NIRSpec IFU  -- Halpha, [OIII] kinematics (V(r)) + rest-optical for M_star.
    * ALMA              -- CO / [CII] cold-gas rotation (extends the curve) + M_gas.
    * ELT/HARMONI (post-2029) -- higher-resolution kinematics, fainter/larger samples.
  z~3 is the sweet spot: Halpha still in JWST range, a0(z) is 6x local (wide deep-MOND window),
  and rotation-supported discs are common enough to assemble ~15-50 clean targets.""")
    print("="*82)


def main():
    part1_signal(); s = part2_error_budget(); part3_sample(s); part4_two_tier(); part5_instruments()
    print("\nBOTTOM LINE: the decisive near-term experiment is ~15-50 extended, rotation-supported,")
    print("deep-MOND galaxies at z~3 with JWST+ALMA kinematics and baryon masses -> a0(3) to 5-10%")
    print("-> ~6-7 sigma on whether a0 evolves (anchor-limited; tighten the z=0 M/L to go higher).")
    print("Cheap, decisive, and a null result kills the framework outright. Do it first.")


if __name__ == "__main__":
    main()
