#!/usr/bin/env python3
"""
Does the cosmic-Weinberg coincidence connect to the MOND scaling? Tested rigorously.
===================================================================================

Carl asked: the relation 2 sin^2(theta_W) = Omega_m/Omega_Lambda (good to ~0.5% today) --
does it have a real connection to the novel scaling-MOND result a0(z) = a0(0) E(z)? This
engages the question with the SAME tool that validates the scaling (z-invariance), applied
fairly. Short answer: no mechanistic connection -- and the reason is sharp and decisive, not
a hand-wave. But there IS a shared, honest observation, stated at the end.

Run:  python real_research/weinberg_mond_connection_test.py
"""

import math

c = 2.99792458e8
MPC = 3.0857e22
Z = 2 * math.sqrt(8 * math.pi / 3)
OM, OL = 0.315, 0.685
SIN2_MZ = 0.23122      # sin^2 theta_W (MS-bar, M_Z); on-shell 0.2231-0.2312, ~constant
SIN2_LOW = 0.2381      # low-energy (Q->0) -- the FULL range of its energy running


def E(z):
    return math.sqrt(OM * (1 + z) ** 3 + OL)


def Om_over_OL(z):
    # Omega_Lambda has constant density; Omega_m density ~ (1+z)^3
    return (OM / OL) * (1 + z) ** 3


def main():
    print("=" * 78)
    print("(1) The coincidence today -- it is real and good")
    print("=" * 78)
    lhs = 2 * SIN2_MZ
    rhs = Om_over_OL(0)
    print(f"   2 sin^2(theta_W)   = {lhs:.4f}")
    print(f"   Omega_m/Omega_L    = {rhs:.4f}")
    print(f"   agreement today    = {abs(lhs-rhs)/rhs*100:.1f}%   (genuinely close, worth recording)")
    print()

    print("=" * 78)
    print("(2) THE TEST -- apply z-invariance (the tool that validates the MOND scaling)")
    print("=" * 78)
    print("   A real edge off a cosmic law is z-INVARIANT. Compare the two ratios vs z:")
    print(f"   {'z':>5}{'a0/cH = 1/Z':>16}{'2sin2W / (Om/OL)(z)':>24}")
    for z in (0, 0.5, 1, 2, 5):
        edge = 1 / Z                                   # constant by construction
        coin = (2 * SIN2_MZ) / Om_over_OL(z)           # the Weinberg 'relation'
        print(f"   {z:>5}{edge:>16.4f}{coin:>24.4f}")
    print("   => a0/cH = 1/Z is FLAT (real edge). The Weinberg ratio drifts as ~(1+z)^-3:")
    print("      off by 8x at z=1, 27x at z=2. It holds ONLY at z~0. FAILS z-invariance ->")
    print("      it is a single-epoch coincidence, the SAME verdict the discriminator gives")
    print("      a0<->T_CMB and a0<->particle scales. The scaling passes; this does not.")
    print()

    print("=" * 78)
    print("(3) The only escape -- 'sin^2 co-evolves with Om/OL' -- is killed by data")
    print("=" * 78)
    print("   For 2 sin^2 = Om/OL to be a LAW (not a now-snapshot), sin^2(theta_W) would have")
    print("   to track Om/OL across cosmic time. But the weak mixing angle is ~constant:")
    print(f"     sin^2 runs only LOG with ENERGY: {SIN2_MZ:.4f} (M_Z) -> {SIN2_LOW:.4f} (Q->0), ~3% total.")
    print("     Across cosmic TIME at fixed energy it is constant (BBN z~1e9, CMB z~1100, lab")
    print("     z=0 all agree). Om/OL spans ~1e27 over that range. A near-constant cannot track")
    print("     a quantity that moves by 27 orders of magnitude. The co-evolution escape fails.")
    print()

    print("=" * 78)
    print("(4) What IS shared (the honest, non-zero part)")
    print("=" * 78)
    print("   The relation holds at z~0 -- which is ALSO when Omega_m ~ Omega_Lambda (the cosmic-")
    print("   coincidence problem) AND when a0 sits ~21% above its Lambda floor. These are the")
    print("   SAME 'now': we live near the matter->Lambda transition. So 2sin^2 = Om/OL is the")
    print("   cosmic-coincidence problem wearing sin^2(theta_W) -- a real why-now puzzle, but NOT")
    print("   a new mechanism, and it does not single out the weak angle (any O(0.46) constant")
    print("   would 'match' now). The MOND scaling does not predict it and is not predicted by it.")
    print()

    print("=" * 78)
    print("   VERDICT")
    print("=" * 78)
    print("   NO genuine connection to the scaling-MOND result. The Weinberg relation FAILS the")
    print("   z-invariance test the scaling PASSES (it drifts as (1+z)^-3; sin^2 cannot co-evolve).")
    print("   It is a single-epoch why-now coincidence in the cosmic-coincidence family -- worth")
    print("   RECORDING, not banking, and NOT to be tiered with the falsifiable a0(z) ~ E(z) trend.")
    print("   Reassuringly, our own discriminator -- built for the scaling -- draws the line cleanly.")


if __name__ == "__main__":
    main()
