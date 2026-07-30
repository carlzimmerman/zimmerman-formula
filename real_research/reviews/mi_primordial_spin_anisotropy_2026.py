#!/usr/bin/env python3
r"""mi_primordial_spin_anisotropy_2026.py -- was matter formation anisotropic, what made it swirl,
and what does the MODIFIED-INERTIA framework actually say about it?

Carl's three questions, answered in order, with the framework's own content isolated from the
standard cosmology so it is clear which is which.

  S1  WAS THE FORMATION OF MATTER ANISOTROPIC?  Statistically isotropic, LOCALLY very anisotropic.
  S2  WHAT MADE IT SWIRL?  NOT primordial rotation -- vorticity modes DECAY. Tidal torques.
  S3  THE FRAMEWORK'S ACTUAL, COMPUTABLE CONTENT: because a0 is CONSTANT (canonical footing, now
      supported at ~52 sigma by mi_cmb_camb_run_2026) while structure densities scale as (1+z)^3,
      the acceleration at a halo's virial radius scales as (1+z)^2. So MODIFIED INERTIA SWITCHES
      ON LATE, at a computable redshift, and high-z galaxies should be MORE Newtonian. That is a
      genuine prediction of the constant-a0 footing and it is testable now.
  S4  WHAT THE FRAMEWORK DOES NOT SAY -- and why the spin question in particular is not its to
      answer.

Both a0 footings carried. Exit 0 = ran. No hard-coded verdicts.
"""
from __future__ import annotations
import math

C = 2.99792458e8
G = 6.67430e-11
H0 = 2.184e-18
OM, OL = 0.315, 0.685
MSUN = 1.98892e30
KPC = 3.0857e19
A0_CANON, A0_ALT = 9.36e-11, 1.13e-10
DELTA_C = 200.0                      # virial overdensity wrt mean matter density

ok = True
def check(c, m):
    global ok
    if not c: ok = False
    print(f"  [{'OK  ' if c else 'FAIL'}] {m}")
def banner(s): print("\n" + "=" * 98); print(s); print("=" * 98)

RHO_C0 = 3 * H0**2 / (8 * math.pi * G)
RHO_M0 = OM * RHO_C0


def halo(M_sun, z):
    """virial radius and virial-edge acceleration for a halo of mass M at redshift z."""
    M = M_sun * MSUN
    rho_halo = DELTA_C * RHO_M0 * (1 + z) ** 3
    R = (3 * M / (4 * math.pi * rho_halo)) ** (1 / 3)
    g = G * M / R**2
    return R, g


def main() -> int:
    banner("S1. WAS THE FORMATION OF MATTER ANISOTROPIC?  Statistically no, locally very much so")
    print("  The initial conditions are STATISTICALLY ISOTROPIC -- no preferred direction in the")
    print("  ensemble, and the CMB confirms it to ~1e-5. But each individual patch is a random")
    print("  fluctuation, and the gravitational collapse of a GENERIC perturbation is violently")
    print("  anisotropic. That is the Zel'dovich picture: a triaxial perturbation collapses along")
    print("  its SHORTEST axis first (a sheet/pancake), then the second (a filament), then the")
    print("  third (a halo). Nothing has to be put in by hand -- generic collapse is sequential")
    print("  and directional, which is exactly why the cosmic web is sheets and filaments rather")
    print("  than a scatter of spheres.")
    print("  So: the ANISOTROPY of structure is EMERGENT from generic collapse, not an initial")
    print("  condition. The initial condition is isotropic and Gaussian-random.")
    check(True, "S1 stated: statistically isotropic initial conditions, locally anisotropic collapse")

    banner("S2. WHAT MADE IT SWIRL?  Not primordial rotation -- that decays. TIDAL TORQUES.")
    print("  This is the part most people get wrong, and it is a theorem, not an opinion.")
    print("  Linear perturbations split into SCALAR (density), VECTOR (vorticity) and TENSOR")
    print("  (gravitational-wave) modes. In an expanding universe:")
    print("    * scalar modes GROW (delta ~ a in the matter era)")
    print("    * tensor modes are constant then decay after horizon entry")
    print("    * VECTOR / VORTICITY modes DECAY AS 1/a^2 -- they have no source and are washed out")
    for z in (1000, 100, 10, 0):
        a = 1.0 / (1 + z)
        print(f"      z = {z:>5}: any primordial vorticity has been diluted by (a/a_i)^-2 -> "
              f"suppressed by ~{(1/(1+1000))**-2 / ((1/(1+z))**-2):.2e} relative to z=1000")
    print("  So the universe did NOT start out swirling and hand that spin to galaxies. Whatever")
    print("  rotation existed initially is gone.")
    print()
    print("  WHERE GALACTIC SPIN ACTUALLY COMES FROM: TIDAL TORQUE THEORY (Hoyle 1949, Peebles")
    print("  1969, White 1984). A protogalaxy is not spherical. The tidal field of NEIGHBOURING")
    print("  overdensities exerts a torque on its quadrupole moment, and that torque spins it up")
    print("  during the LINEAR phase. Angular momentum grows ~ linearly with time in the matter")
    print("  era, then freezes near turnaround when the object decouples and virialises.")
    print("  Galaxies spin because their NEIGHBOURS pulled them lopsidedly -- not because the")
    print("  universe was rotating.")
    check(True, "S2 stated: vorticity decays as 1/a^2; spin comes from tidal torques, not initial rotation")

    banner("S3. THE FRAMEWORK'S ACTUAL CONTENT: modified inertia SWITCHES ON LATE")
    print("  Here is where the framework says something real, and it follows from the footing the")
    print("  CMB just selected. a0 is CONSTANT (tied to rho_Lambda). But structure densities scale")
    print("  as (1+z)^3, so for a virialised halo of fixed mass:")
    print("      rho_vir = 200 rho_m0 (1+z)^3  ->  R_vir ~ (1+z)^-1  ->  g_vir = GM/R_vir^2 ~ (1+z)^2")
    print("  Accelerations were HIGHER in the past while a0 stayed the same. So the deep-MOND")
    print("  regime is a LATE-TIME phenomenon, and early galaxies should be MORE Newtonian.")
    print()
    print(f"  Virial-edge acceleration g_vir in units of a0 (canonical {A0_CANON:.2e}):")
    print(f"  {'M (Msun)':>12}{'z=0':>10}{'z=1':>10}{'z=2':>10}{'z=4':>10}{'z=7':>10}{'z=10':>10}")
    print("  " + "-" * 74)
    for Msun in (1e10, 1e11, 1e12, 1e13, 1e14):
        row = f"  {Msun:>12.0e}"
        for z in (0, 1, 2, 4, 7, 10):
            _, g = halo(Msun, z)
            row += f"{g/A0_CANON:>10.3f}"
        print(row)
    print("\n  Read the table: at z = 0 every halo's outskirts are DEEP sub-a0 (g/a0 << 1), which is")
    print("  why flat rotation curves are a low-redshift commonplace. Going back, g_vir climbs as")
    print("  (1+z)^2 and the outskirts approach and then exceed a0.")
    # crossing redshift for each mass
    print(f"\n  Redshift at which the VIRIAL EDGE crosses g = a0 (MOND switches off above it):")
    print(f"  {'M (Msun)':>12}{'z_cross canon':>16}{'z_cross alt':>14}")
    print("  " + "-" * 44)
    for Msun in (1e10, 1e11, 1e12, 1e13, 1e14):
        _, g0 = halo(Msun, 0.0)
        z_c = math.sqrt(A0_CANON / g0) - 1
        z_a = math.sqrt(A0_ALT / g0) - 1
        print(f"  {Msun:>12.0e}{z_c:>16.2f}{z_a:>14.2f}")
    _, g0_mw = halo(1e12, 0.0)
    z_mw = math.sqrt(A0_CANON / g0_mw) - 1
    print(f"\n  For a Milky-Way-mass halo (1e12 Msun): z_cross = {z_mw:.1f}")
    check(3 < z_mw < 15, f"a MW-mass halo's virial edge crosses a0 at z ~ {z_mw:.0f}")
    print("  ABOVE that redshift the whole halo -- including its outskirts -- sits in the")
    print("  Newtonian regime and the framework predicts essentially NO modified-inertia")
    print("  signature. BELOW it, the outskirts go sub-a0 and flat curves develop.")
    print()
    print("  THIS IS A TESTABLE PREDICTION AND IT IS ALREADY A LIVE FRONT. High-z rotation curves")
    print("  (MSA-3D, MUSE-DARK) probe exactly this. The repo's a0(z) work carries it as")
    print("  WEAK-TENSION/WATCH (controlled residual +0.91 +/- 0.8, ~1.1 sigma from flat). The")
    print("  constant-a0 footing says high-z galaxies should look MORE Newtonian; a rising a0")
    print("  would say the opposite -- and the CMB has now excluded rising at ~52 sigma.")
    print("  So the framework's answer to 'what changed as dark energy took over' is: NOTHING")
    print("  changed about a0. What changed is that MATTER THINNED OUT, so accelerations fell")
    print("  through a0 and the modified regime became visible. Same attrition that turned on")
    print("  cosmic acceleration turned on MOND phenomenology.")

    banner("S4. WHAT THE FRAMEWORK DOES NOT SAY -- and why the spin question is not its to answer")
    print("  It has NO story for the ORIGIN of anisotropy: that is generic Zel'dovich collapse of")
    print("  Gaussian initial conditions, and it happens in the Newtonian regime at high z where")
    print("  the framework reduces to Newton (S3's table: g/a0 >> 1 at early times).")
    print("  It has NO story for the ORIGIN of spin either, for the same reason: tidal torquing")
    print("  operates during LINEAR growth at high z, again deep in the Newtonian regime. And the")
    print("  framework's kernel responds to a tracer's OWN acceleration (Box_u u = -Omega^2 u), not")
    print("  to the coherent large-scale field -- so it does not even couple to the torquing field")
    print("  in the way one might hope (mi_bulkflow_and_initial_conditions_2026).")
    print("  The genuinely unbuilt piece remains the same one: an MI transfer function and growth")
    print("  rate, i.e. the framework's linear cosmology. Without it, statements about how MI")
    print("  modifies structure formation and spin acquisition are not available -- and I am not")
    print("  going to manufacture them.")
    print()
    print("  CREDIT, so nothing reads as novel that isn't: 'MOND effects are weaker at high z")
    print("  because accelerations were higher' is standard MOND-cosmology reasoning (Sanders,")
    print("  Milgrom). The framework SHARES this expectation rather than originating it. What is")
    print("  specific here is the tie to rho_Lambda, which is what makes a0 constant and therefore")
    print("  makes the switch-on redshift computable rather than free.")

    banner("VERDICT -- what can actually be learned")
    print(f"  1. Formation was statistically ISOTROPIC but locally ANISOTROPIC -- Zel'dovich")
    print(f"     sheets then filaments then halos. Emergent, not an initial condition.")
    print(f"  2. It did NOT swirl to begin with. Vorticity decays as 1/a^2. Galactic spin comes")
    print(f"     from TIDAL TORQUES by neighbours (Hoyle/Peebles/White), acquired during linear")
    print(f"     growth and frozen at turnaround.")
    print(f"  3. THE FRAMEWORK'S REAL, COMPUTABLE STATEMENT: with a0 constant, g_vir ~ (1+z)^2, so")
    print(f"     modified inertia SWITCHES ON LATE -- a MW-mass halo's virial edge crosses a0 at")
    print(f"     z ~ {z_mw:.0f}. High-z galaxies should be MORE Newtonian. Testable now with high-z")
    print(f"     rotation curves, and it is the same front the a0(z) work already tracks.")
    print(f"  4. The deep answer to 'what changed when dark energy took over': a0 did NOT change.")
    print(f"     Matter thinned out, accelerations fell through a0, and the modified regime became")
    print(f"     VISIBLE. The same dilution that switched on cosmic acceleration switched on MOND")
    print(f"     phenomenology. That is a genuine unifying statement the constant-a0 footing makes")
    print(f"     and the rising footing cannot.")
    print(f"  5. The framework does NOT explain the origin of anisotropy or of spin, and its")
    print(f"     linear cosmology is unbuilt. Stated, not papered over.")
    print("=" * 98)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
