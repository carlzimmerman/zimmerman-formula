#!/usr/bin/env python3
"""
Is the 8pi -> 32pi factor-4 FORCED by a normalization principle, or is it a CONVENTION?
=======================================================================================
C. Zimmerman, June 2026. Worked with real math, every factor of 2 / pi / 3 carried explicitly.

THE SETUP (from ANHARMONIC_AND_32PI.md). MOND is an ANHARMONIC effect: Newton's field Lagrangian is
HARMONIC (quadratic), L_N = -(1/8piG)|grad phi|^2 -> linear Poisson; deep-MOND (Bekenstein-Milgrom
AQUAL) is ANHARMONIC (cubic), L_M = -(1/8piG)(2/3)|grad phi|^3/a0 -> the sqrt-law. a0 is the
gravitational anharmonic coefficient. Blanchet's dipolar-dark-matter internal energy is
    W(Pi) = Lambda/8pi  +  2pi Pi^2  +  (16pi^2/3a0) Pi^3 + ...
            ^floor          ^harmonic     ^anharmonic (MOND, a0 in the cubic coeff)
The FLOOR coefficient is 8pi (the Einstein coupling). The framework's number, written as
a0 = c^2 sqrt(Lambda/32pi) <=> 32pi = Lambda c^4 / a0^2, uses 32pi = 4 x 8pi.

THE QUESTION. Is the factor 4 = 2^2 (i.e. 8pi -> 32pi) FORCED by a normalization principle -- namely,
is it EXACTLY the conversion between "Lambda as a potential/energy-floor coefficient (8pi)" and "a0 as a
free-fall acceleration coefficient (32pi)" via the de Sitter surface gravity kappa = c^2/(2R) (the 1/2,
squared)? Or is the "2" a convention (could equally be 1, collapsing 32pi -> 8pi)?

WHAT THIS SCRIPT SHOWS (verdict up front, all four sections verify it numerically):
  -- 8pi IS forced: it is the Einstein coupling, entering through rho_Lambda = Lambda c^2/(8 pi G).
  -- The 4 = 2^2 is NOT forced: it is entirely the numeric PREFACTOR (1 vs 1/2) on the de Sitter
     acceleration a = (prefactor) x c x sqrt(G rho_Lambda). prefactor=1 -> 8pi; prefactor=1/2 -> 32pi.
  -- There is NO convention-free de Sitter quantity that selects 1/2 over 1. Worse: the Gibbons-Hawking
     surface gravity kappa = c^2/(2R) (which DOES carry a 1/2) does NOT even land on 32pi -- it gives 12,
     not 8pi or 32pi. So the framework's 1/2 is a THIRD, separate modeling choice, not the kappa 1/2.
  VERDICT: the 8pi->32pi factor-4 is CONVENTION, not forced. Default (and correct) answer.

Needs numpy.
"""
import numpy as np

# ---- constants & cosmology (same values as the sibling review scripts) ----
pi = np.pi
c = 2.998e8                       # m/s
G = 6.674e-11                     # m^3 kg^-1 s^-2
Mpc = 3.086e22                    # m
H0 = 67.4e3 / Mpc                 # Hubble constant, 1/s (Planck)
OmL = 0.685                       # Omega_Lambda
Lam = 3 * OmL * H0**2 / c**2      # cosmological constant, 1/m^2  (Lambda = 3 Omega_L H0^2 / c^2)
H = H0 * np.sqrt(OmL)             # de Sitter (pure-Lambda) Hubble rate, 1/s
R = c / H                         # de Sitter horizon radius, m  ( = sqrt(3/Lam) )
rhoL = Lam * c**2 / (8 * pi * G)  # mass density of Lambda, kg/m^3  ( rho = Lam c^2 / 8 pi G ) <- the 8pi enters HERE

a0_obs = 1.2e-10                  # observed MOND scale, m/s^2


def ratio(a):
    """The dimensionless Lambda c^4 / a^2 -- this is '32pi' (or whatever number) for a given accel a."""
    return Lam * c**4 / a**2


def main():
    W = 92
    print("#" * W)
    print("# Is the 8pi -> 32pi factor-4 FORCED by a normalization principle, or a CONVENTION?")
    print("#" * W + "\n")

    print(f"  R_dS = c/H = {R:.4e} m   (check sqrt(3/Lam) = {np.sqrt(3/Lam):.4e} m)")
    print(f"  rho_Lambda = Lam c^2/(8 pi G) = {rhoL:.4e} kg/m^3   <- note the 8pi lives in the DENSITY\n")

    # ================================================================================================
    print("=" * W)
    print("(1) THE FACTOR-4 LOCATED: it is (prefactor)^2 on the de Sitter acceleration sqrt(G rho_L)")
    print("=" * W)
    # The de Sitter free-fall acceleration is built as a = (prefactor) x c x sqrt(G rho_Lambda).
    # sqrt(G rho_L) = H sqrt(3/8pi) is a frequency (1/s); times c gives an acceleration.
    sq = np.sqrt(G * rhoL)
    print(f"   sqrt(G rho_Lambda) = {sq:.4e} 1/s = H*sqrt(3/8pi) = {H*np.sqrt(3/(8*pi)):.4e} 1/s  (a frequency)")
    print(f"   {'acceleration a':<42}{'a (m/s^2)':>13}{'Lam c^4/a^2':>14}{'  multiple of pi':>16}")
    for pref, name in [(1.0, "a = 1 * c * sqrt(G rho_L)   [no 1/2]"),
                       (0.5, "a = (1/2) c sqrt(G rho_L)   [framework a0]")]:
        a = pref * c * sq
        r = ratio(a)
        print(f"   {name:<42}{a:>13.3e}{r:>14.4f}{r/pi:>13.3f} pi")
    print(f"\n   => prefactor 1   gives Lam c^4/a^2 = 8pi  = {8*pi:.3f}   (BLANCHET's floor coefficient)")
    print(f"      prefactor 1/2 gives Lam c^4/a^2 = 32pi = {32*pi:.3f}   (the FRAMEWORK's coefficient)")
    print(f"      The factor 4 = (1 / (1/2))^2 = 2^2 is ENTIRELY the squared prefactor. The 8pi is common to both.")
    print(f"      a0(32pi)/a0(8pi) = {(0.5*c*sq)/(1.0*c*sq):.4f} = 1/2  (one power of 2; squared in the ratio -> 4)\n")

    # ================================================================================================
    print("=" * W)
    print("(2) IS THE '2' THE de SITTER SURFACE GRAVITY kappa = c^2/(2R)? -- TESTED: NO")
    print("=" * W)
    # The framework's stated story: the 4 is the surface-gravity 1/2 (kappa = c^2/2R) inverted and squared.
    # Test it head-on: does the Gibbons-Hawking kappa, or cH, actually produce 8pi / 32pi? It does NOT.
    print(f"   {'de Sitter accel (geometry only)':<40}{'a (m/s^2)':>13}{'Lam c^4/a^2':>14}")
    for a, name in [(c**2/R,      "cH        = c^2/R   (no 1/2)"),
                    (c**2/(2*R),  "kappa     = c^2/(2R) [Hawking 1/2]"),
                    (2*c**2/R,    "2cH       = 2c^2/R  (factor 2)")]:
        print(f"   {name:<40}{a:>13.3e}{ratio(a):>14.4f}")
    print(f"\n   These geometric accelerations give Lam c^4/a^2 = 3, 12, 0.75 -- NEITHER 8pi NOR 32pi.")
    print(f"   In particular kappa = c^2/(2R) (which DOES carry the Hawking 1/2) lands on 12, not 32pi.")
    print(f"   => 8pi/32pi can ONLY be reached by routing through the DENSITY rho_L = Lam c^2/(8piG)")
    print(f"      (that is where the 8pi comes from). The surface-gravity 1/2 is a DIFFERENT factor of 2")
    print(f"      that does NOT produce the framework number. The framework conflates THREE distinct 2's:")
    print(f"        (A) Hawking kappa 1/2  ->  gives 12, not used;")
    print(f"        (B) the 1/2 in a0=(c/2)sqrt(G rho_L)  ->  the actual source of 32pi vs 8pi;")
    print(f"        (C) the 8pi itself (Einstein) -- forced, and NOT a factor of 2 at all.")
    print(f"      a0(32pi) = {0.5*c*sq:.3e} =/= kappa = {c**2/(2*R):.3e}  (they differ by sqrt(3/8pi)={np.sqrt(3/(8*pi)):.4f}).\n")

    # ================================================================================================
    print("=" * W)
    print("(3) DOES BLANCHET'S W(Pi) FORCE 32pi = Lam c^4/a0^2 by floor-vs-cubic consistency? -- NO")
    print("=" * W)
    print("   W(Pi) = Lambda/8pi + 2pi Pi^2 + (16pi^2/3a0) Pi^3 + ...   has THREE independent coefficients:")
    print("     floor (set by Lambda), harmonic mass term (2pi, fixed by Blanchet), cubic (set by a0).")
    print("   Lambda and a0 enter as SEPARATE inputs. The harmonic<->anharmonic crossover in Pi is")
    Pi_star = 3/(8*pi)
    print(f"     2pi Pi^2 = (16pi^2/3a0)Pi^3  =>  Pi_* = 3a0/(8pi) = {Pi_star:.5f}*a0 -- internal to Pi, does")
    print(f"     NOT relate Lambda to a0. So W's STRUCTURE imposes no particular value of Lam c^4/a0^2.")
    print(f"   Demonstration that 'Lam c^4/a0^2' is just whatever floor coefficient you put in (a tautology):")
    for coeff, lbl in [(8*pi, "8pi (Blanchet floor)"), (32*pi, "32pi (framework)")]:
        a0 = c**2 * np.sqrt(Lam/coeff)
        print(f"     a0 = c^2 sqrt(Lam/{lbl.split()[0]:<5}) = {a0:.3e}  ->  Lam c^4/a0^2 = {ratio(a0):.3f} = {lbl}")
    print(f"   => Dimensional/normalization consistency of the floor + cubic does NOT force the relation.")
    print(f"      (AQUAL fixes the cubic's 2/3 by requiring the point-mass sqrt-law g=sqrt(g_N a0), but a0")
    print(f"       is a FREE input there -- AQUAL/Blanchet never tie a0 to Lambda at all.)\n")

    # ================================================================================================
    print("=" * W)
    print("(4) DOES 'crossover accel = de Sitter free-fall accel (c/2)sqrt(G rho_L)' FORCE the 4? -- NO")
    print("=" * W)
    print("   This is just RE-STATING choice (B): you DEFINE a0 := (c/2)sqrt(G rho_L). The (c/2) is the same")
    print("   unforced 1/2 from section (1). Pick prefactor 1 instead and you DEFINE a0 := c sqrt(G rho_L),")
    print("   landing on 8pi. The 'principle' (set the MOND crossover to the de Sitter acceleration) is real")
    print("   and gives a0 ~ c sqrt(G rho_L) ~ c sqrt(G Lambda) up to an O(1) -- but it CANNOT fix that O(1),")
    print("   because 'the de Sitter free-fall acceleration' has no convention-free numeric prefactor.")
    print(f"     prefactor 1   -> a0 = {1.0*c*sq:.3e}, ratio {ratio(1.0*c*sq):.2f} (=8pi)")
    print(f"     prefactor 1/2 -> a0 = {0.5*c*sq:.3e}, ratio {ratio(0.5*c*sq):.2f} (=32pi)")
    print(f"   Observed a0 = {a0_obs:.2e} -> Lam c^4/a0^2 = {ratio(a0_obs):.1f}, which sits BETWEEN 8pi and 32pi")
    print(f"   and matches NEITHER cleanly -- so the data do not adjudicate the prefactor either.\n")

    # ================================================================================================
    print("=" * W)
    print("VERDICT")
    print("=" * W)
    print(f"""  (a) The 8pi -> 32pi factor-4 is **CONVENTION, NOT FORCED**.

  (b) LOAD-BEARING STEP: the numeric prefactor on the de Sitter acceleration,
        a0 := (prefactor) x c x sqrt(G rho_Lambda),   rho_Lambda = Lam c^2/(8 pi G).
      prefactor = 1   gives 32pi -> 8pi (Blanchet's floor);  prefactor = 1/2 gives 8pi -> 32pi (framework).
      The factor 4 = (1/(1/2))^2 = 2^2 is exactly this prefactor, squared when you invert to Lam c^4/a0^2.
      Nothing convention-free selects 1/2 over 1. The Gibbons-Hawking surface gravity kappa = c^2/(2R) --
      the framework's stated source of the 1/2 -- does NOT even produce 32pi (it gives 12), so the
      framework's 1/2 is a SEPARATE modeling choice, not the kappa 1/2 it is attributed to.

  (c) HONEST ONE-PARAGRAPH VERDICT. The 8pi is genuinely forced -- it is the Einstein coupling, entering
      through the Lambda mass density rho_Lambda = Lambda c^2/(8 pi G); on that Blanchet and the framework
      agree exactly. But the extra factor of 4 that turns Blanchet's floor coefficient 8pi into the
      framework's 32pi is NOT forced: it is the square of the unforced numeric prefactor (1 vs 1/2) that
      converts the de Sitter cosmic frequency sqrt(G rho_Lambda) into an acceleration. "Curvature -> free-fall
      acceleration" does NOT introduce a canonical 2^2 = 4: the only de Sitter acceleration carrying a true
      1/2 (the Hawking surface gravity kappa = c^2/2R) lands on 12, not 32pi, so the framework's 1/2 is a
      third, independent convention, not the surface-gravity 1/2 it claims. Neither Blanchet's W(Pi)
      structure (Lambda and a0 are independent inputs) nor the AQUAL cubic (which fixes 2/3 but leaves a0
      free) forces the floor-to-acceleration relation. CONCLUSION: 8pi is forced, the factor-4 is a
      surface-gravity/normalization CONVENTION, and so 32pi remains route-forced by GR but NOT uniquely
      forced -- consistent with FORCING_THE_COEFFICIENT.md already classifying the outer factor-2 as
      "convention." This is NOT an upgrade from "route-forced" to "forced".""")
    print("#" * W)


if __name__ == "__main__":
    main()
