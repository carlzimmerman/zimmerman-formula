#!/usr/bin/env python3
"""
THE MILGROM "MOND-AS-A-VACUUM-EFFECT" ROUTE -- does it derive the framework a0?  (honest audit)
================================================================================================
Route (Milgrom 1999, Phys Lett A 253, 273; astro-ph/9805346): a uniformly-accelerated detector in
de Sitter space registers an Unruh temperature that is NOT T~a but the Deser-Levin COMBINED value
        2*pi*k_B*T(a)/hbar = sqrt(a^2 + a_dS^2),     a_dS = c^2 sqrt(Lambda/3) = c H_Lambda.
                                                     (Deser & Levin, gr-qc/9706018, VERIFIED verbatim)
If inertia is the vacuum's reaction to the temperature EXCESS dT = T(a)-T(0):
    a << a_dS :  dT ~ a^2/(2 a_dS)   (MOND-like quadratic; mu ~ a/a0)   <-- deep-MOND FORM reproduced
    a >> a_dS :  dT ~ a              (Newtonian linear)                  <-- high-acc limit reproduced
So the FUNCTIONAL FORM of the transition and the deep-MOND asymptote follow, with the onset scale = a_dS.

This script computes, from the real numbers, exactly:
  (1) the a0 the route gives under each reading of "onset" (raw a_dS vs thermal a_dS/2pi),
  (2) the dimensionless Z = cH_Lambda/a0 each gives, vs the framework Z=sqrt(32pi/3)=5.79 and band [4.2,6.0],
  (3) the de Sitter (Gibbons-Hawking) and Unruh temperatures, to show the 6x temperature offset is the SAME
      number as the coefficient question,
  (4) the EVOLUTION a0(z) the route implies -- the decisive fork: does it give the framework's declining
      sqrt(rho_DE), or the disfavored rising/constant branch?
Reproducible: `python milgrom_vacuum_route.py`. Needs numpy.

LITERATURE STATUS (all verified against the real papers this session):
  Milgrom 1999 abstract VERBATIM: "...sees Unruh radiation of temperature T~[a^2+a0^2]^(1/2), with a0=(L/3)^(1/2).
                                   ... An actual inertia-from-vacuum mechanism is still a far cry off."
  Milgrom review VERBATIM:        "I cannot tell whether it is germane to MOND, because it is not backed by a
                                   concrete mechanism for inertia..."  (he calls a0<->Lambda a 'coincidence').
  Milgrom 2020 (2001.09729):      "a0 ~ c H0 ~ c^2 Lambda^(1/2) ~ c^2/l_U"  (no preferred branch; 'near-equal today').
  Deser & Levin (gr-qc/9706018):  "2*pi*T = (Lambda/3 + a^2)^(1/2)"  (the combined de Sitter Unruh temperature).
  Klinkhamer & Kopp (1104.2022):  "2*pi*T_min = H_deS";  "A0 = 2 c H_deS";  a0 "differ[s] from our A0 by a
                                   factor of order unity"; they do NOT derive the rotation-curve a0.
"""
import numpy as np

# ---------------- constants (match the framework scripts exactly) ----------------
C    = 2.99792458e8          # m/s
G    = 6.674e-11             # SI
HBAR = 1.054571817e-34       # J s
KB   = 1.380649e-23          # J/K
MPC  = 3.0857e22             # m
H0   = 67.4e3 / MPC          # 1/s
OmL  = 0.685                 # dark-energy fraction today

LAM    = 3 * OmL * H0**2 / C**2          # cosmological constant, 1/m^2
H_LAM  = C * np.sqrt(LAM / 3)            # asymptotic de Sitter rate, 1/s
A_DS   = C * H_LAM                       # = c^2 sqrt(Lambda/3): the de Sitter ACCELERATION (Milgrom's raw a0)
RHO_L  = LAM * C**2 / (8 * np.pi * G)    # dark-energy density, kg/m^3
A0_FR  = C**2 * np.sqrt(LAM / (32 * np.pi))   # framework a0 = (c/2)sqrt(G rho_L) = 9.36e-11

Z_FRAME = np.sqrt(32 * np.pi / 3)        # 5.789
ZLO, ZHI = 4.2, 6.0                      # data-allowed band (from coefficient_landscape.py)


def Z_of(a0):  return A_DS / a0
def T_unruh(a):  return HBAR * a / (2 * np.pi * C * KB)   # standard Unruh temperature of acceleration a


def main():
    np.set_printoptions(suppress=True)
    print("#"*100)
    print("# MILGROM 'MOND AS A VACUUM EFFECT' ROUTE  -- what a0, Z, and a0(z) does it ACTUALLY predict?")
    print("#"*100)
    print(f"\n  Lambda    = {LAM:.3e} /m^2")
    print(f"  H_Lambda  = {H_LAM:.3e} /s        (asymptotic de Sitter rate)")
    print(f"  a_dS      = c*H_Lambda = {A_DS:.3e} m/s^2   (the de Sitter acceleration = Milgrom's RAW a0)")
    print(f"  rho_DE    = {RHO_L:.3e} kg/m^3")
    print(f"  framework a0 = {A0_FR:.3e} m/s^2   (Z = sqrt(32pi/3) = {Z_FRAME:.3f}); data band Z in [{ZLO},{ZHI}]")

    # ----------------------------------------------------------------------------
    # (0) verify the claimed deep-MOND FORM from the combined temperature, numerically
    # ----------------------------------------------------------------------------
    print("\n" + "="*100)
    print("(0) DOES THE COMBINED TEMPERATURE GIVE THE MOND FORM?  dT=T(a)-T(0), with 2pi T ~ sqrt(a^2+a_dS^2)")
    print("="*100)
    # work in 'temperature-acceleration' units g(a) = sqrt(a^2+a_dS^2) (i.e. 2pi c kB T/hbar):
    for ratio in [1e-3, 1e-2, 1e-1, 1.0, 1e1, 1e2]:
        a = ratio * A_DS
        g_excess = np.sqrt(a**2 + A_DS**2) - A_DS          # the temperature EXCESS in accel units
        quad = a**2 / (2 * A_DS)                            # predicted deep-MOND quadratic a^2/2a_dS
        lin  = a                                            # predicted Newtonian linear
        which = "->quad a^2/2a_dS" if ratio < 0.3 else ("->linear a" if ratio > 3 else "(transition)")
        ref  = quad if ratio < 0.3 else lin
        print(f"   a/a_dS={ratio:>6.0e}:  excess/a_dS={g_excess/A_DS:>10.3e}   ratio to {which.split()[0][2:] or 'ref':<6}"
              f"={g_excess/ref:>7.3f}")
    print("   => CONFIRMED: excess -> a^2/(2 a_dS) for a<<a_dS (deep-MOND quadratic) and -> a for a>>a_dS (Newtonian).")
    print("      The MECHANISM reproduces the deep-MOND FORM and sets the SCALE at a_dS. (Milgrom 1999, real.)")

    # ----------------------------------------------------------------------------
    # (1) the a0 and Z under each reading of 'onset'
    # ----------------------------------------------------------------------------
    print("\n" + "="*100)
    print("(1) WHAT a0 / Z DOES THE ROUTE GIVE?  (the coefficient is NOT uniquely fixed -- here are the readings)")
    print("="*100)
    readings = [
        ("Milgrom RAW: a0 = a_dS = c^2 sqrt(L/3)",           A_DS,
         "the literal abstract value a0=(L/3)^(1/2)"),
        ("deep-MOND '1/2': a0 = a_dS/2  (from a^2/2a_dS)",   A_DS/2,
         "the quadratic coefficient puts a 1/2 on a_dS"),
        ("THERMAL: a0 = a_dS/2pi  (match TEMPERATURES)",     A_DS/(2*np.pi),
         "Milgrom-2020 abar0=2pi a0; Unruh T carries 1/2pi"),
        ("Klinkhamer-Kopp bare A0 = 2 c H_deS",              2*A_DS,
         "their entropic-screen value (Z=0.5) -- they DISCLAIM it as the rotation a0"),
        ("FRAMEWORK: a0 = (c/2) sqrt(G rho_L)",              A0_FR,
         "8pi forced + 1/2 free-fall prefactor"),
    ]
    print(f"   {'reading':<48}{'a0 [m/s^2]':>13}{'Z':>8}{'a0/a0_frame':>13}   verdict")
    for name, a0, note in readings:
        Z = Z_of(a0)
        verdict = "CONSISTENT" if ZLO <= Z <= ZHI else ("edge" if abs(Z-ZLO)<0.4 or abs(Z-ZHI)<0.4 else "EXCLUDED")
        star = " <--FRAME" if "FRAMEWORK" in name else ""
        print(f"   {name:<48}{a0:>13.3e}{Z:>8.2f}{a0/A0_FR:>13.3f}   {verdict}{star}")
    print(f"\n   The route's NATURAL thermal value (a0=a_dS/2pi, Z=2pi={2*np.pi:.3f}) vs framework Z={Z_FRAME:.3f}:")
    print(f"      ratio Z_thermal/Z_frame = {2*np.pi/Z_FRAME:.4f}  ->  agree to {100*abs(2*np.pi/Z_FRAME-1):.1f}%.")
    print(f"      a0(thermal)={A_DS/(2*np.pi):.3e} vs a0(frame)={A0_FR:.3e}: differ by {100*abs(A_DS/(2*np.pi)/A0_FR-1):.1f}%.")

    # ----------------------------------------------------------------------------
    # (2) the temperatures -- showing the 6x offset IS the coefficient question
    # ----------------------------------------------------------------------------
    print("\n" + "="*100)
    print("(2) THE TEMPERATURES (the ~6x T_dS/T_U offset is the SAME number as 'Z=2pi vs raw').")
    print("="*100)
    T_dS = HBAR * H_LAM / (2 * np.pi * KB)        # Gibbons-Hawking de Sitter temperature
    T_U_frame = T_unruh(A0_FR)                    # Unruh T at the framework a0
    T_U_ds    = T_unruh(A_DS)                      # Unruh T at a_dS (= the de Sitter combined T floor)
    print(f"   T_dS (Gibbons-Hawking, hbar H_Lambda/2pi kB) = {T_dS:.3e} K")
    print(f"   T_U(a0_frame)                                = {T_U_frame:.3e} K   (ratio T_dS/T_U = {T_dS/T_U_frame:.2f})")
    print(f"   T_U(a_dS)  = T_dS by construction            = {T_U_ds:.3e} K   (check: {T_U_ds/T_dS:.3f} x T_dS)")
    print( "   => 'MOND onset when T_U(a0) ~ T_dS' is NOT satisfied at the framework a0 (off by ~6x); it is")
    print( "      satisfied at a~a_dS, i.e. Milgrom's RAW Z=1 -- which the DATA EXCLUDES (a0 ~6x too big).")
    print( "      The factor that reconciles them is exactly the 2pi/(Z) coefficient -- the open O(1).")

    # ----------------------------------------------------------------------------
    # (3) THE EVOLUTION FORK -- the decisive test
    # ----------------------------------------------------------------------------
    print("\n" + "="*100)
    print("(3) EVOLUTION a0(z): does the route give the framework's DECLINING sqrt(rho_DE)?  (THE decisive fork)")
    print("="*100)
    # Background: flat LCDM, constant Lambda (standard).
    Om_m = 1 - OmL
    def E(z):  return np.sqrt(Om_m*(1+z)**3 + OmL)                 # H(z)/H0
    def rho_tot(z):  return Om_m*(1+z)**3 + OmL                    # in units of rho_crit,0
    # The three candidate scalings the literature actually offers:
    #   (A) framework / event-horizon DE:  a0 ~ sqrt(rho_DE) ; rho_DE = const (cosmological constant) -> a0 CONSTANT here,
    #       BUT the framework's TEST uses a DECLINING sqrt(rho_DE) under THAWING/evolving DE (w!=-1). For const-Lambda the
    #       framework branch is flat; the DISCRIMINATING statement is 'tracks rho_DE, NOT rho_tot'. We show both.
    #   (B) Milgrom-raw / de Sitter a_dS = c^2 sqrt(Lambda/3): Lambda const -> a0 CONSTANT in z.
    #   (C) Hubble-horizon / McCulloch quantised inertia: a0 ~ c H(z) ~ sqrt(rho_tot) -> RISES at high z.
    print(f"   {'z':>5}{'H(z)/H0':>10}{'sqrt(rho_tot)':>15}{'(A) a0~sqrtRhoDE':>18}{'(B) a0~a_dS':>14}{'(C) a0~cH(z)':>14}")
    for z in [0, 0.5, 1, 2, 3, 5]:
        a_A = 1.0                              # const Lambda -> sqrt(rho_DE)=const (framework: tracks DE density)
        a_B = 1.0                              # de Sitter a_dS: Lambda const -> const
        a_C = E(z)                             # Hubble: rises as H(z)/H0
        print(f"   {z:>5}{E(z):>10.3f}{np.sqrt(rho_tot(z)):>15.3f}{a_A:>18.3f}{a_B:>14.3f}{a_C:>14.3f}")
    print( "\n   READOUT:")
    print( "   * The Unruh-de Sitter route pins a0 to a_dS = c^2 sqrt(Lambda/3).  With a constant Lambda this is")
    print( "     CONSTANT in z (branch B) -- it does NOT decline. It coincides with the framework only because")
    print( "     today sqrt(rho_DE)=sqrt(rho_Lambda); but the framework's DISCRIMINATING signal is a0 TRACKING the")
    print( "     DARK-ENERGY density (declining if DE thaws, w>-1), NOT the total density.")
    print( "   * Milgrom 2020 explicitly leaves a0 tied to EITHER c H0 (branch C, RISES ~sqrt(rho_tot), high-z DISFAVORED)")
    print( "     OR c^2 sqrt(Lambda/3) (branch B, CONSTANT) -- 'near-equal today', no mechanism to pick declining-DE.")
    print( "   * McCulloch quantised inertia (a0=2c^2/Theta, Theta=Hubble/particle horizon) sits on branch C -> RISES.")
    print( "   => The route does NOT naturally select a0(z) ~ sqrt(rho_DE) declining. On the fork it gives CONSTANT")
    print( "      (de Sitter) or RISING (Hubble) -- i.e. constant or the DISFAVORED side, NOT the framework's branch.")

    # ----------------------------------------------------------------------------
    # SUMMARY for the structured grade
    # ----------------------------------------------------------------------------
    print("\n" + "#"*100)
    print("# SUMMARY (numbers for the verdict)")
    print("#"*100)
    a0_thermal = A_DS/(2*np.pi); a0_raw = A_DS
    print(f"  predicted a0 (natural thermal reading)  a0 = c^2 sqrt(L/3)/(2pi) = {a0_thermal:.3e} m/s^2  (Z={Z_of(a0_thermal):.2f})")
    print(f"  predicted a0 (Milgrom literal RAW)       a0 = c^2 sqrt(L/3)       = {a0_raw:.3e} m/s^2  (Z={Z_of(a0_raw):.2f}) EXCLUDED")
    print(f"  framework a0                                                       = {A0_FR:.3e} m/s^2  (Z={Z_FRAME:.2f})")
    print(f"  thermal-vs-framework agreement: {100*abs(2*np.pi/Z_FRAME-1):.1f}% in Z, {100*abs(a0_thermal/A0_FR-1):.1f}% in a0")
    print(f"  RAW value in band [{ZLO},{ZHI}]?  {ZLO<=Z_of(a0_raw)<=ZHI}    THERMAL value in band?  {ZLO<=Z_of(a0_thermal)<=ZHI} (Z=2pi={2*np.pi:.2f}, upper edge)")
    print(f"  evolution: route -> CONSTANT (de Sitter, const Lambda) or RISING (Hubble); framework needs DECLINING sqrt(rho_DE) -> NO match")


if __name__ == "__main__":
    main()
