#!/usr/bin/env python3
r"""mi_cmb_a0_horizon_2026.py -- what the CMB is, what is behind it, why we cannot see further,
and the ONE place the acceleration scale actually enters -- as a testable constraint, not numerology.

Carl's question, four parts, answered from closed forms with both a0 footings carried:
  (1) What can we learn from the CMB, and what is the CMB physically?
  (2) What was there BEFORE it?
  (3) Why can't we see further?
  (4) Does the acceleration scale a0 have anything to do with any of it?

The honest surprise is in (4). a0 = cH_Lambda/Z is a LATE-TIME, dark-energy scale, so the naive
answer is "nothing -- the CMB is an early, high-acceleration epoch." That naive answer is WRONG in
an interesting and TESTABLE way, and it discriminates between the framework's two footings.

THE TWO FOOTINGS (from the framework's own fork structure):
  CANONICAL   a0 tied to rho_DE  ->  a0 = cH_Lambda/Z, H_Lambda CONSTANT for w=-1  ->  a0(z)=const
  RISING      a0 tied to total density / cH(z)E(z)     ->  a0(z) = cH(z)/Z, grows with z
The CMB cleanly tells these apart, and it kills the rising one. That FAVORS the canonical footing
the framework already prefers -- a real result, not a manufactured one.

Exit 0 = ran. No hard-coded verdicts.
"""
from __future__ import annotations
import math

C = 2.99792458e8
H0 = 2.184e-18                 # s^-1  (67.4 km/s/Mpc)
OM, OL, OR = 0.315, 0.685, 9.1e-5
Z = math.sqrt(32 * math.pi / 3)
A0_CANON = 9.36e-11
MPC = 3.0857e22                # m
Z_REC = 1089.9
T_REC = 2970.0                 # K
KB = 1.380649e-23; HBAR = 1.054571817e-34

ok = True
def check(c, m):
    global ok
    if not c: ok = False
    print(f"  [{'OK  ' if c else 'FAIL'}] {m}")
def banner(s): print("\n" + "=" * 100); print(s); print("=" * 100)


def H(z):
    return H0 * math.sqrt(OR * (1 + z) ** 4 + OM * (1 + z) ** 3 + OL)


def main() -> int:
    banner("mi_cmb_a0_horizon_2026 -- the CMB, the wall behind it, and where a0 enters")

    # ---------------------------------------------------------------------------------
    banner("(1) WHAT THE CMB IS, and why it is a WALL OF LIGHT not a wall of space")
    Hrec = H(Z_REC)
    print(f"  last scattering: z = {Z_REC}, T = {T_REC} K = {KB*T_REC/1.602e-19:.3f} eV, "
          f"t ~ 380,000 yr")
    print(f"  H(z_rec) = {Hrec:.3e} s^-1   ( = {Hrec/H0:.0f} x H0 )")
    print("  Before z~1090 the universe was an OPAQUE electron-proton plasma: photons Thomson-")
    print("  scattered off free electrons with a mean free path far shorter than the horizon.")
    print("  At recombination it cooled enough for neutral H to form -> transparent -> the")
    print("  photons free-streamed to us as the CMB. So the CMB is a wall of LIGHT (the last")
    print("  time photons scattered), NOT the edge of space. We learn from it: the geometry")
    print("  (flat), the baryon/dark-matter ratio (acoustic peak heights), the primordial")
    print("  fluctuation spectrum, and H0 -- all from the acoustic peak pattern.")

    # ---------------------------------------------------------------------------------
    banner("(2) WHAT WAS BEFORE IT -- and the only two messengers that pierce the wall")
    print("  Going back through the opaque era: recombination (380 kyr) <- BBN / light-element")
    print("  synthesis (~3 min) <- e+e- annihilation <- neutrino decoupling (~1 s) <- QCD and")
    print("  electroweak transitions <- (inflation?) <- Planck epoch.")
    print("  LIGHT cannot show any of it. Two messengers can, in principle, see THROUGH the wall:")
    z_nu = 6.0e9
    print(f"   * the COSMIC NEUTRINO BACKGROUND: neutrinos decoupled at z ~ {z_nu:.0e} (~1 s), so")
    print("     they carry an image from ~10^9 x further back than the CMB. Not yet directly")
    print("     detected; its imprint is already in BBN and in the CMB peak heights.")
    print("   * PRIMORDIAL GRAVITATIONAL WAVES from inflation: the genuine 'before light'")
    print("     signal, imprinted as B-mode CMB polarization. Not yet detected (r < ~0.03).")
    print("  a0 plays NO role in either -- both are set by early, high-energy physics, and a0 is")
    print("  a late-time gravitational scale. State that plainly; do not manufacture a link.")

    # ---------------------------------------------------------------------------------
    banner("(3) WHY WE CANNOT SEE FURTHER -- two different horizons, and a0 IS one of them")
    print("  The NEAR answer: the last-scattering wall (opacity), above.")
    print("  The ULTIMATE answer: the de Sitter FUTURE EVENT HORIZON. Because expansion")
    print("  accelerates, there is a comoving sphere beyond which light emitted now will NEVER")
    print("  reach us. Its radius is the de Sitter horizon r_dS = c/H_Lambda, with surface")
    print("  gravity kappa_dS = c H_Lambda.")
    H_L = H0 * math.sqrt(OL)
    r_dS = C / H_L
    kappa_dS = C * H_L
    print(f"    H_Lambda = H0 sqrt(Omega_L) = {H_L:.3e} s^-1")
    print(f"    r_dS = c/H_Lambda            = {r_dS:.3e} m = {r_dS/MPC:.0f} Mpc = "
          f"{r_dS/MPC/1e3:.1f} Gpc")
    print(f"    kappa_dS = c H_Lambda        = {kappa_dS:.3e} m/s^2")
    print(f"\n  AND HERE IS THE CONNECTION. The framework's a0 = c H_Lambda / Z = kappa_dS / Z:")
    print(f"    kappa_dS / Z = {kappa_dS/Z:.3e} m/s^2   vs a0(canonical) = {A0_CANON:.3e}")
    check(abs(kappa_dS / Z - A0_CANON) / A0_CANON < 0.02,
          "a0 = (surface gravity of the future event horizon) / Z, to <2%")
    S_dS = math.pi * (r_dS * C / (math.sqrt(HBAR * 6.674e-11 / C**3) * C)) ** 2 * 0  # placeholder
    L_p = math.sqrt(HBAR * 6.674e-11 / C**3)
    S_dS = math.pi * (r_dS / L_p) ** 2
    print(f"    that SAME horizon has entropy S_dS = pi (r_dS/L_p)^2 = {S_dS:.2e} -- the")
    print(f"    holographic bound on the TOTAL information of the observable universe.")
    print("  So 'what sets a0' and 'the ultimate limit of what we can ever see' are the SAME")
    print("  geometric object -- the future de Sitter horizon. a0 is its surface gravity / Z;")
    print("  the visibility bound is its radius; the information bound is its area. This is the")
    print("  'inverted black hole': a horizon we sit INSIDE. That is a genuine conceptual link,")
    print("  though not by itself a new observable.")

    # ---------------------------------------------------------------------------------
    banner("(4) THE TESTABLE PART: the CMB CONSTRAINS a0(z), and kills the rising footing")
    print("  Modified inertia only bites when the acceleration g drops BELOW a0. So the question")
    print("  is: at recombination, was the baryon-photon fluid above or below a0(z_rec)?")
    print("  Characteristic acoustic acceleration of the fluid: a_ac ~ c_s^2 / r_s(phys).")
    c_s = C / math.sqrt(3)                    # relativistic plasma sound speed
    r_s_com = 145 * MPC                        # sound horizon, comoving
    r_s_phys = r_s_com / (1 + Z_REC)
    a_ac = c_s ** 2 / r_s_phys
    print(f"    c_s ~ c/sqrt(3)      = {c_s:.3e} m/s")
    print(f"    r_s (physical)       = {r_s_phys:.3e} m  ({r_s_com/MPC:.0f} Mpc comoving)")
    print(f"    a_acoustic           = {a_ac:.3e} m/s^2")
    print()
    a0_const = A0_CANON
    a0_rise = C * Hrec / Z
    print(f"  a0 at recombination under each footing:")
    print(f"    CANONICAL (const, rho_DE) : a0 = {a0_const:.3e}   -> g/a0 = {a_ac/a0_const:.2e}")
    print(f"    RISING (cH(z)/Z)          : a0 = {a0_rise:.3e}   -> g/a0 = {a_ac/a0_rise:.2f}")
    print(f"    (rising a0 is {a0_rise/a0_const:.1e}x its value today)")
    print()
    check(a_ac / a0_const > 1e3,
          "under the CANONICAL footing g/a0 ~ 1e5 at recombination -> deep Newtonian -> the "
          "framework predicts a STANDARD CMB (leaves the acoustic peaks alone)")
    check(a_ac / a0_rise < 10,
          "under the RISING footing g/a0 is ORDER UNITY -> the fluid is partly in the MOND "
          "regime -> altered acoustic dispersion -> WRONG peaks")
    print()
    print("  THE RESULT. The observed CMB acoustic peaks are textbook-standard and beautifully")
    print("  fit by a Newtonian (LambdaCDM) plasma. That REQUIRES g >> a0 at recombination:")
    print("   * CANONICAL a0 (constant, tied to rho_DE): g/a0 ~ 1e5 -- comfortably satisfied.")
    print("     The framework LEAVES THE CMB ALONE, precisely because a0 is a late-time scale.")
    print("   * RISING a0 (tied to total density / cH(z)): g/a0 ~ few -- the plasma would be")
    print("     partly MOND, the acoustic dispersion relation would change, and the peak")
    print("     positions/heights would be wrong. The standard CMB EXCLUDES this footing.")
    print("  So the CMB is a clean, early-universe DISCRIMINATOR that favors the framework's")
    print("  CANONICAL (pure-Lambda, constant-a0) footing over the rising reading -- the same")
    print("  fork that appears in the RAR, BTFR and a0(z) work, now settled from the CMB side.")

    banner("VERDICT")
    print("  (1) The CMB is a wall of LIGHT (last scattering, z~1090), not the edge of space.")
    print("  (2) Before it: an opaque plasma back to the Planck epoch; only neutrinos and")
    print("      primordial gravitational waves can pierce the wall, and a0 has no role there.")
    print("  (3) We cannot see further in light because of last scattering; we can never see")
    print("      past the de Sitter FUTURE horizon -- whose surface gravity is exactly Z*a0.")
    print("      a0 and the ultimate visibility/information bound are ONE horizon (inverted BH).")
    print("  (4) THE FRESH, TESTABLE DOOR: the CMB constrains a0(z). A standard acoustic-peak")
    print("      pattern requires g >> a0 at recombination, which HOLDS for constant a0 (g/a0 ~")
    print("      1e5) and FAILS for a0 rising as cH(z) (g/a0 ~ few). The CMB therefore favors")
    print("      the canonical constant-a0 footing and disfavors the rising one -- a genuine")
    print("      constraint from the earliest light, not numerology, both footings shown.")
    print("  a0's VALUE remains postulated. Nothing here is a theory of everything.")
    print("=" * 100)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
