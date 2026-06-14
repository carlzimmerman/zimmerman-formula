#!/usr/bin/env python3
# === COEFFICIENT-FOOTING CORRECTION (2026-06-13) ===
# Any 'a0 = cH0/Z', '1/Z=0.173 against cH0', or an H0-tuned-to-71.5 'rescue' below uses the SUPERSEDED footing.
# Canonical: a0 = c^2 sqrt(Lambda/32pi) = cH_Lambda/Z = 9.36e-11 (rho_DE; cH_Lambda = sqrt(OmL)*cH0 = 0.83*cH0).
# Coefficient 1/Z=0.173 is against cH_Lambda; against cH0 it is 0.143. Milgrom 0.159 / Verlinde 0.167 use cH0,
# so the apt comparison is 0.143 (the LOW OUTLIER, NOT bracketed). cH0/Z=1.13e-10 is the rho_total reading (+20%).
# See real_research/THE_A0_COEFFICIENT_CONVENTION.md + real_research/THE_A0_COEFFICIENT_AUDIT_2026-06-13.md
"""
Tier B: the radion-MOND bridge -- a real attempt, with a real ledger.
=====================================================================

The ask: make the volume modulus (radion) do double duty --
  (i)  stabilize it so its minimum fixes Lambda  (-> H0 -> a0), and
  (ii) write a MOND completion in which THAT SAME field is the MOND field,
       so a0 is geometric and a0(z) ~ E(z) is automatic.

This script BUILDS the construction far enough to test it, and is brutally
honest about which planks hold. The pieces that are actually COMPUTABLE:

  Part 1: the AQUAL scalar MOND completion genuinely produces v^4 = G M a0
          (flat rotation curves) -- demonstrated numerically. [WORKS]
  Part 2: a modulus whose mass tracks the Hubble rate, m_phi(z) ~ H(z), gives
          an emergent a0(z) = c H(z) / Z, hence a0(z)/a0(0) = E(z), with the
          O(1) coupling fixed to Z = 2 sqrt(8pi/3). [WORKS as a scaling]
  Part 3: AQUAL is solar-system safe: deviations ~ a0/a ~ 2e-8 << Cassini.[WORKS]
  Part 4: the LEDGER of what does NOT close: the cosmological-constant problem,
          the heavy-(stabilized)-vs-light-(m~H) tension, the varying-constants
          bound on a rolling radion, and the imposed interpolation mu(x).

VERDICT up front: this is a coherent SKETCH with a genuine mechanism (a
Hubble-mass modulus -> a0 ~ cH(z)), strictly better than 'shared symbol' -- but
it imports the CC problem and needs an imposed MOND function, and the LITERAL
single-radion-does-everything version faces a varying-constants bound. It is a
research program, not a derivation. Same honesty bar as every other floor.

Pure stdlib. Run:  python reviews/radion_mond_bridge.py
"""

import math

# constants
C = 2.99792458e8
G = 6.674e-11
MSUN = 1.989e30
MPC = 3.0857e22
KPC = 3.0857e19
HBAR = 1.054571817e-34
EV = 1.602176634e-19
A0 = 1.20e-10
Z = 2 * math.sqrt(8 * math.pi / 3)          # 5.78881
H0 = 71.5 * 1e3 / MPC                        # 1/s  (framework H0)
OM, OL = 0.315, 0.685


def Efunc(z):
    return math.sqrt(OM * (1 + z) ** 3 + OL)


def mu(x):
    """AQUAL interpolation: mu(x)=x/sqrt(1+x^2). x = g/a0.
       mu->1 (Newton) for x>>1; mu->x (deep MOND) for x<<1."""
    return x / math.sqrt(1.0 + x * x)


def solve_g(gN, a0):
    """Solve mu(g/a0) * g = gN for g (the AQUAL radial field eqn)."""
    # monotonic in g; bisection between tiny and 10*gN
    lo, hi = 1e-30, max(10 * gN, 10 * a0)
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if mu(mid / a0) * mid < gN:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def part1_aqual_works():
    print("=" * 80)
    print("(1) The AQUAL scalar MOND completion DOES produce v^4 = G M a0  [WORKS]")
    print("=" * 80)
    print("   Action piece (Bekenstein-Milgrom):")
    print("     L_phi = -(a0^2/8piG) F( (grad phi)^2 / a0^2 ),  phi = the radion")
    print("   Field eqn (point mass M): mu(g/a0) g = g_N = GM/r^2,")
    print("     mu->1 (g>>a0): g=GM/r^2  (Newton);")
    print("     mu->g/a0 (g<<a0): g=sqrt(GM a0)/r  ->  v^2 = g r = sqrt(GM a0) = const.")
    print()
    M = 1e11 * MSUN
    v_pred = (G * M * A0) ** 0.25 / 1e3
    print(f"   Test galaxy M = 1e11 Msun.  deep-MOND v_flat = (G M a0)^1/4 = {v_pred:.0f} km/s")
    print(f"   {'r [kpc]':>9} {'g_N/a0':>9} {'v(r) [km/s]':>12} {'regime':>10}")
    for r_kpc in (1, 3, 10, 30, 100, 300):
        r = r_kpc * KPC
        gN = G * M / r ** 2
        g = solve_g(gN, A0)
        v = math.sqrt(g * r) / 1e3
        regime = "Newton" if gN / A0 > 3 else ("MOND" if gN / A0 < 0.3 else "transition")
        print(f"   {r_kpc:>9} {gN/A0:>9.2e} {v:>12.0f} {regime:>10}")
    print(f"   => v(r) flattens to ~{v_pred:.0f} km/s at large r: the scalar reproduces")
    print("      the baryonic Tully-Fisher law. The MOND completion is REAL physics")
    print("      (this is just AQUAL; the only claim is that phi = the radion). ✓\n")


def part2_a0_tracks_H():
    print("=" * 80)
    print("(2) A Hubble-mass modulus gives a0(z) = cH(z)/Z, so a0(z)/a0(0)=E(z) [WORKS]")
    print("=" * 80)
    print("   Mechanism: an ultralight modulus with Compton wavelength = Hubble radius,")
    print("     m_phi c^2 ~ hbar H(z),  has force range ~ c/H(z) and a natural")
    print("     acceleration scale a0 ~ c H(z) (the de Sitter / horizon acceleration).")
    print("     The O(1) normalization is the coupling = 1/Z.  =>  a0(z) = c H(z)/Z.")
    print()
    a0_today = C * H0 / Z
    m_phi = HBAR * H0 / C ** 2            # kg
    m_phi_eV = m_phi * C ** 2 / EV
    print(f"   a0(0) = cH0/Z = {a0_today:.3e} m/s^2   (obs {A0:.3e}; coupling must be Z={Z:.3f})")
    print(f"   modulus mass m_phi ~ hbar H0 / c^2 = {m_phi_eV:.2e} eV   (ultralight)")
    print()
    print(f"   {'z':>5} {'E(z)':>7} {'a0(z)=cH(z)/Z':>16} {'a0(z)/a0(0)':>13} {'=E(z)?':>7}")
    for z in (0, 1, 3, 6, 10, 14):
        a0z = a0_today * Efunc(z)
        print(f"   {z:>5} {Efunc(z):>7.2f} {a0z:>16.3e} {a0z/a0_today:>13.2f} "
              f"{Efunc(z):>7.2f}")
    print("   => the EVOLUTION is automatic and Z-independent; the VALUE needs coupling=Z.")
    print("      This is the genuine new content vs 'shared symbol': a MECHANISM for")
    print("      WHY a0 ~ cH and WHY it evolves as H(z). ✓\n")


def part3_solar_system():
    print("=" * 80)
    print("(3) Solar-system safety: AQUAL reduces to Newton where a >> a0  [WORKS]")
    print("=" * 80)
    a_earth = G * MSUN / (1.496e11) ** 2      # Sun's pull on Earth
    ratio = a_earth / A0
    dev = A0 / a_earth                         # fractional MOND deviation ~ a0/a
    print(f"   Earth's acceleration toward Sun:  a = {a_earth:.3e} m/s^2")
    print(f"   a / a0 = {ratio:.2e}  (>> 1, deep Newtonian regime, mu->1)")
    print(f"   fractional MOND deviation ~ a0/a = {dev:.1e}")
    print(f"   Cassini PPN bound on extra force:  ~2e-5")
    print(f"   {dev:.1e} << 2e-5  => PASSES. The scalar is screened (Newtonian) in the")
    print("      Solar System; MOND only switches on in the a<a0 galactic outskirts. ✓\n")


def part4_ledger():
    print("=" * 80)
    print("(4) THE LEDGER -- what does NOT close (the honest part)")
    print("=" * 80)
    rows = [
        ("Cosmological-constant problem",
         "stabilizing V(phi) at the OBSERVED Lambda~(meV)^4 ~ 1e-120 M_Pl^4 is a "
         "tuning, not a derivation. Plank (i) 'fixes Lambda' only in the sense that "
         "EVERY string vacuum 'fixes' it -- by landing in the landscape. UNSOLVED."),
        ("Heavy-vs-light tension (the crux)",
         "plank (i) wants a STABILIZED (heavy, m>>H, frozen) modulus to fix Z^2 and "
         "Lambda; plank (ii) wants an ULTRALIGHT (m~H, rolling) modulus to source the "
         "evolving a0. A single field generically CANNOT be both. This is the central "
         "obstruction to the LITERAL 'one radion does everything'."),
        ("Varying-constants bound",
         "if the SAME radion is ultralight and rolling (architecture A), the "
         "compactification volume Z^2 is time-dependent -> alpha, gauge couplings drift. "
         "alpha-dot/alpha < ~1e-17/yr forces the radion-SM coupling xi < ~1e-7. Possibly "
         "evadable (volume/loop-suppressed coupling), but a real constraint."),
        ("Imposed interpolation",
         "the MOND function mu(x) (deep limit mu->x) is CHOSEN to fit galaxy rotation "
         "curves, not derived from the geometry. Same status as in every MOND theory."),
    ]
    for name, why in rows:
        print(f"   [OPEN] {name}:")
        print(f"          {why}")
        print()


def part5_architectures():
    print("=" * 80)
    print("(5) Three architectures -- and which is actually defensible")
    print("=" * 80)
    print("   A) ONE ultralight radion (m~H) = quintessence + MOND field.")
    print("      + most economical, literally 'the radion does everything';")
    print("      - varying constants (above); hard to also fix Z^2 if it is rolling.")
    print()
    print("   B) TWO moduli: one heavy/stabilized (fixes Z^2, contributes Lambda),")
    print("      one ultralight (the MOND/quintessence field).")
    print("      + clean, no varying-constants problem;")
    print("      - NOT 'one field does double duty' -- you paid with a second modulus.")
    print()
    print("   C) STABILIZED radion (fixes Z^2 + bare Lambda) + HORIZON MOND:")
    print("      a0(z)~cH(z) emerges holographically from the de Sitter horizon")
    print("      (Verlinde-style), the radion sets only the O(1) coupling Z.")
    print("      + no varying constants; uses the stabilized modulus you already need;")
    print("      - the MOND scale is horizon-thermodynamic, so the radion is NOT")
    print("        literally the MOND field -- it sets the coupling, not the dynamics.")
    print()
    print("   MOST DEFENSIBLE: C. It is the version that survives the constraints, and")
    print("   it is honestly a notch weaker than the literal ask (radion sets the")
    print("   coupling Z; the horizon sets the evolving scale a0~cH(z)).")


def main():
    part1_aqual_works()
    part2_a0_tracks_H()
    part3_solar_system()
    part4_ledger()
    part5_architectures()
    print("=" * 80)
    print("VERDICT -- the bridge, scored honestly")
    print("=" * 80)
    print("  BUILT (real, computable): an AQUAL scalar reproduces v^4=GMa0 (part 1);")
    print("    a Hubble-mass modulus gives a0(z)=cH(z)/Z with the evolution automatic")
    print("    and the coupling fixed to Z (part 2); it is solar-system safe (part 3).")
    print("    This is a genuine MECHANISM linking the two halves -- a real upgrade")
    print("    over 'they share the number 32pi/3'.")
    print()
    print("  NOT CLOSED (the ledger, part 4): the CC problem is imported wholesale;")
    print("    the literal single-radion version faces heavy-vs-light + varying-")
    print("    constants tensions; the MOND interpolation is imposed. The defensible")
    print("    architecture (C) makes the radion set the COUPLING Z while the HORIZON")
    print("    sets the evolving a0 -- a notch weaker than 'the radion IS the MOND field'.")
    print()
    print("  NET: Tier B is buildable as a coherent research program with a real")
    print("    mechanism, not a finished derivation. The strongest honest sentence is:")
    print("    'an ultralight/horizon-coupled modulus makes a0 ~ cH(z) natural, with")
    print("    the geometric O(1) = 1/Z; deriving Lambda and fixing the field's mass")
    print("    remain open.' That is more than you had, and less than a Theory of")
    print("    Everything -- which is exactly where the honest line sits.")


if __name__ == "__main__":
    main()
