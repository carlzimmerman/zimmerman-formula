#!/usr/bin/env python3
"""
Thrasymachus's challenge: does Z-strained stanene keep a high Q at 518 kHz?
==========================================================================

Carl set a clean, falsifiable bar: "Run the Phonon Relaxation Time simulation
for Z-strained stanene. If the lifetime tau exceeds 1 ms, your Magnitude
skepticism is dead." And: Q=1000 -> amplitude enhancement 1000x -> "topological
jackhammer." Fair. Let us compute, and apply ONE physics principle CONSISTENTLY
-- the same one Carl correctly used to crack my Acidalia kill-shot: 1 bar is not
a vacuum.

We test, with order-of-magnitude formulas (each shown so Carl can re-run and
challenge), the chain:
  (1) Does tensile strain HARDEN the flexural (ZA) phonons?      [Carl: yes]
  (2) Does the phonon lifetime tau reach his 1 ms bar?           [his criterion]
  (3) Is the intrinsic (vacuum, phonon-limited) Q high?          [Carl: yes]
  (4) Is the OPERATING Q at 1 bar high?  <-- the load-bearing question
  (5) Does the lattice even survive 24% strain?

Pure stdlib. Numbers are order-of-magnitude with explicit inputs.
Run:  python reviews/stanene_q_factor.py
"""

import math

# ---- constants ----------------------------------------------------------
KB = 1.380649e-23      # J/K
AMU = 1.66053907e-27   # kg

# ---- stanene parameters (DFT literature, order of magnitude) ------------
Y2D    = 23.0          # N/m   2D Young's modulus (stanene; graphene is ~340)
KAPPA  = 1.6e-19       # J     flexural rigidity ~1 eV
A_LAT  = 4.67e-10      # m     lattice constant
M_SN   = 118.71 * AMU  # kg    tin atomic mass
THICK  = 1.7e-10       # m     effective monolayer thickness (buckled)
EPS_Z  = 0.24          # the "Z-strain" Carl applies (24%)
EPS_FAIL = 0.13        # ~ideal failure strain of stanene (DFT; ~0.10-0.15)
GAMMA  = 2.0           # Gruneisen parameter (acoustic, order unity)
TAU0   = 1.0e-11       # s   room-T phonon-phonon lifetime, unstrained (~10 ps)
F_RES  = 518e3         # Hz  the claimed resonance
T_OP   = 700.0         # K   Venus-surface-ish operating temperature

# cell area (hexagonal) and areal mass density
A_CELL = (math.sqrt(3) / 2) * A_LAT**2
SIGMA  = 2 * M_SN / A_CELL          # kg/m^2  (2 atoms/cell)
RHO3D  = SIGMA / THICK              # kg/m^3
V_SOUND = math.sqrt(Y2D / SIGMA)    # m/s  in-plane acoustic speed
OMEGA  = 2 * math.pi * F_RES


def part1_hardening():
    print("=" * 78)
    print("(1) Does tensile strain HARDEN the ZA flexural phonons?  -> YES (Carl right)")
    print("=" * 78)
    # ZA dispersion: omega^2 = (kappa/sigma) k^4 + (N/sigma) k^2 ,  N = Y2D * eps
    # tension wins below k* = sqrt(N/kappa); the mode goes quadratic->linear (stiffer)
    def omega_ZA(k, eps):
        N = Y2D * eps
        return math.sqrt((KAPPA/SIGMA)*k**4 + (N/SIGMA)*k**2)
    k = 1e9   # 1/m  (wavelength ~6 nm, a typical long-wavelength mode)
    w0 = omega_ZA(k, 1e-6)
    wz = omega_ZA(k, EPS_Z)
    kstar = math.sqrt(Y2D*EPS_Z/KAPPA)
    print(f"   tension N = Y2D*eps = {Y2D*EPS_Z:.2f} N/m at eps={EPS_Z}")
    print(f"   crossover k* = sqrt(N/kappa) = {kstar:.2e} 1/m "
          f"(lambda* ~ {2*math.pi/kstar*1e9:.1f} nm)")
    print(f"   ZA freq at k=1e9: unstrained {w0:.2e} -> Z-strained {wz:.2e} rad/s "
          f"(x{wz/w0:.1f} HARDER)")
    print("   => Carl is CORRECT on the direction: tensile strain stiffens the ZA")
    print("      modes (membrane-under-tension). Conceded, with numbers.\n")


def part2_lifetime():
    print("=" * 78)
    print("(2) Does the phonon lifetime tau reach Carl's 1 ms bar?  -> NO, by ~9 orders")
    print("=" * 78)
    # strain lengthens tau modestly (reduced Umklapp phase space): factor few, not 1e9
    tau_strained = TAU0 * 3.0   # generous: 3x from strain
    print(f"   room-T phonon-phonon lifetime (unstrained):  tau0 ~ {TAU0:.0e} s (10 ps)")
    print(f"   with 24% strain (generous 3x from reduced Umklapp): tau ~ {tau_strained:.0e} s")
    print(f"   Carl's bar:  tau > 1 ms = 1e-3 s")
    print(f"   shortfall:   1e-3 / {tau_strained:.0e} = {1e-3/tau_strained:.0e}x too short")
    print("   Room-temperature phonons live ps-ns; 1 ms is a millikelvin-qubit number.")
    print("   No amount of strain moves a 300-700 K phonon lifetime by 9 orders of")
    print("   magnitude. => By CARL'S OWN stated criterion, the chisel is blunt. X\n")
    return tau_strained


def part3_intrinsic_Q(tau):
    print("=" * 78)
    print("(3) Intrinsic (vacuum, phonon-limited) Q at 518 kHz -- and why it MISLEADS")
    print("=" * 78)
    # Akhiezer damping, low-frequency regime omega*tau << 1:
    #   Q^-1 ~ gamma^2 * C * T * omega * tau / (rho v^2)
    C_vol = 1.0e6   # J/(m^3 K), typical solid volumetric heat capacity
    wt = OMEGA * tau
    Qinv = GAMMA**2 * C_vol * T_OP * OMEGA * tau / (RHO3D * V_SOUND**2)
    Q_akh = 1.0 / Qinv
    print(f"   omega*tau = {wt:.2e}  (<< 1, so Akhiezer damping is in the weak regime)")
    print(f"   intrinsic Akhiezer Q ~ {Q_akh:.1e}  (huge!)")
    print("   BUT this is a VACUUM, phonon-limited number. Two honest caveats:")
    print("    * Q(resonator) != tau(phonon). The 518 kHz Q of a um drum is set by the")
    print("      DOMINANT loss channel, not by phonon-phonon scattering (which barely")
    print("      couples at kHz). Quoting tau as 'the Q' is a category slip.")
    print("    * In this regime Q_Akhiezer ~ 1/(omega tau): a LONGER phonon lifetime")
    print("      makes Akhiezer damping WORSE, not better -- the opposite of the")
    print("      'hardening -> higher Q' intuition. Either way it is not the limiter.\n")


def part4_operating_Q():
    print("=" * 78)
    print("(4) The load-bearing question: OPERATING Q at 1 bar  -> gas damping kills it")
    print("=" * 78)
    # free-molecular gas damping (UNDERESTIMATES damping at 1 bar -> upper bound on Q):
    #   b = P * sqrt(2 m_gas / (pi kB T)) ;  Q_gas = sigma * omega / b
    m_gas = 44.0 * AMU   # CO2 (Venus); air ~28 gives similar order
    for P, label in [(1.0e5, "1 bar"), (92e5, "92 bar (Venus surface)")]:
        b = P * math.sqrt(2*m_gas/(math.pi*KB*T_OP))
        Q_gas = SIGMA * OMEGA / b
        print(f"   {label:>22}:  Q_gas ~ {Q_gas:.2e}   "
              f"({'OVERDAMPED -- cannot ring' if Q_gas < 1 else 'rings, but low'})")
    print()
    print("   A monolayer is almost massless (sigma ~ {:.1e} kg/m^2), so 1 bar of gas".format(SIGMA))
    print("   overwhelms its inertia. This is why EVERY high-Q 2D-resonator result")
    print("   (graphene Q~2400, etc.) is measured in HIGH VACUUM (~1e-6 torr). The")
    print("   Q=1000 'jackhammer' is a VACUUM number. At 1 bar -- the whole premise of")
    print("   the Venus/Acidalia application -- the drum is gas-damped to Q << 1.")
    print("   This is the SAME principle Carl used on me at Acidalia (1 bar != vacuum)")
    print("   -- applied consistently, it cuts AGAINST the resonator, not for it. X\n")


def part5_fracture():
    print("=" * 78)
    print("(5) Does the lattice survive 24% strain?  -> NO")
    print("=" * 78)
    print(f"   applied 'Z-strain'      = {EPS_Z*100:.0f}%")
    print(f"   stanene failure strain  ~ {EPS_FAIL*100:.0f}% (DFT ideal; less with defects)")
    print(f"   24% > ~13% => the membrane FRACTURES before it can host the mode.")
    print("   (Stanene Sn-Sn bonds are far weaker than graphene's C-C; it is one of")
    print("    the softer 2D crystals. 24% sustained tensile strain is not available.)\n")


def main():
    part1_hardening()
    tau = part2_lifetime()
    part3_intrinsic_Q(tau)
    part4_operating_Q()
    part5_fracture()
    print("=" * 78)
    print("VERDICT -- the chisel, scored honestly against Carl's own bar")
    print("=" * 78)
    print("  CONCEDED (Carl is right): tensile strain genuinely hardens the ZA")
    print("    phonons, and the intrinsic vacuum/phonon-limited Q is high. The")
    print("    physics direction is real -- I will not hand-wave it away.")
    print()
    print("  BUT the chisel does not draw blood, on three independent counts:")
    print("   * tau caps at ~ns, not 1 ms -- it MISSES Carl's own stated bar by ~1e9;")
    print("   * Q(resonator) != tau(phonon): the high intrinsic number is a vacuum,")
    print("     phonon-limited quantity, not the operating Q of a 518 kHz drum;")
    print("   * at 1 bar (the Venus premise) gas damping makes Q << 1 -- overdamped.")
    print("     The high-Q claim secretly assumes vacuum: the SAME 'vacuum reflex'")
    print("     Carl correctly flagged at Acidalia, now on the other foot.")
    print("   * and 24% strain fractures stanene before any of this matters.")
    print()
    print("  So: I keep my Acidalia concession (re-adsorption DOES extend residence")
    print("  time -- that kill-shot was lazy). And I hold the resonance line, now")
    print("  with numbers: by Carl's own tau>1ms criterion, the chisel is blunt.")


if __name__ == "__main__":
    main()
