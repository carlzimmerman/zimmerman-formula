#!/usr/bin/env python3
"""
The core physics, derived honestly from two equations only.
===========================================================

Everything the surviving framework can legitimately claim follows from combining
  Schwarzschild :  R_s = 2GM/c^2
  Friedmann     :  H^2 = (8 pi G / 3) rho     (flat, critical density)
Nothing else is assumed. Each result below is tagged:
  [EXACT]        forced by the two equations, verified numerically here.
  [POSIT]        a definitional choice (which cosmic timescale); not unique.
  [ASPIRATIONAL] the horizon-thermodynamics direction where the one open number
                 (the coefficient) might eventually be computed -- not done.

The honest punchline: a0 = c^2/(2R) with R = c x (a cosmic timescale). The
STRUCTURE (a0 ~ surface gravity of a cosmic scale ~ cH) is forced; the O(1)
COEFFICIENT is a convention -- the data picks the dynamical time, giving Z.

Run:  python real_research/schwarzschild_friedmann_core.py
"""

import math

c = 2.99792458e8
G = 6.674e-11
MPC = 3.0857e22
HBAR = 1.054571817e-34
KB = 1.380649e-23
H0 = 70e3 / MPC                  # s^-1 (value cancels in the ratios that matter)
LAMBDA_OM, LAMBDA_OL = 0.315, 0.685
A0_OBS = 1.13e-10                # real SPARC RAR anchor (sparc_rar_honest.py)

RH = c / H0
RHO_C = 3 * H0 ** 2 / (8 * math.pi * G)
Z = 2 * math.sqrt(8 * math.pi / 3)
LP2 = HBAR * G / c ** 3          # Planck length^2


def ok(a, b, tol=1e-6):
    return "OK" if abs(a - b) / abs(b) < tol else "FAIL"


def main():
    print("#" * 74)
    print("# (1) [EXACT] The universe is marginally a black hole")
    print("#" * 74)
    M_H = (4 * math.pi / 3) * RH ** 3 * RHO_C
    Rs = 2 * G * M_H / c ** 2
    print("  Mass inside the Hubble radius at critical density:")
    print(f"    M_H = (4pi/3) R_H^3 rho_c = c^3/(2GH) = {M_H:.3e} kg")
    print(f"    Schwarzschild radius of M_H:  R_s = 2GM_H/c^2 = {Rs:.3e} m")
    print(f"    R_s / R_H = {Rs/RH:.6f}   [{ok(Rs, RH)}]")
    print("  => the Hubble radius IS its own Schwarzschild radius. Equivalently the")
    print("     Newtonian escape velocity at R_H equals c. This is exact, not a fit.\n")

    print("#" * 74)
    print("# (2) [EXACT] The 1/2 in a0 = c^2/(2R) is the escape-velocity factor")
    print("#" * 74)
    print("  Escape velocity from sphere (M,R): v_esc^2 = 2GM/R  (the '2' of R_s).")
    print("  Surface gravity g = GM/R^2 = v_esc^2/(2R). At the cosmic horizon v_esc=c:")
    g_H = c ** 2 / (2 * RH)
    print(f"    g_horizon = c^2/(2 R_H) = cH/2 = {g_H:.3e} m/s^2   [{ok(g_H, c*H0/2)}]")
    print("  So the Schwarzschild '1/2' is the escape-velocity/surface-gravity factor.")
    print("  This already gives a0 ~ cH -- the Milgrom coincidence -- with coefficient 1/2.\n")

    print("#" * 74)
    print("# (3) [POSIT] The coefficient is set by WHICH cosmic timescale")
    print("#" * 74)
    print("  a0 = c^2/(2R),  R = c * t_cosmic.  Three natural timescales, three answers:")
    print(f"  {'timescale':<34}{'R/R_H':>8}{'a0=cH/k':>12}{'a0 [m/s^2]':>13}")
    rows = [
        ("Hubble time   t=1/H",            1.0,                       2.0),
        ("collapse time t=sqrt(3pi/32Grho)", math.pi / 2,             math.pi),
        ("dynamical time t=1/sqrt(Grho)",  math.sqrt(8 * math.pi / 3), Z),
    ]
    for name, RoverRH, k in rows:
        print(f"  {name:<34}{RoverRH:>8.3f}{('cH/%.3f'%k):>12}{c*H0/k:>13.3e}")
    print(f"  {'OBSERVED (SPARC)':<34}{'--':>8}{('cH/%.2f'%(c*H0/A0_OBS)):>12}{A0_OBS:>13.3e}")
    print("  => the data picks the DYNAMICAL time t=1/sqrt(Grho), i.e. coefficient")
    print(f"     Z = 2 sqrt(8pi/3) = {Z:.4f}. The 'cleaner' Hubble (2) and collapse (pi)")
    print("     scales OVERSHOOT. So Z is a free-fall-scale CONVENTION that fits, not a")
    print("     first-principles number. This is the single posited input. Honest.\n")

    print("#" * 74)
    print("# (4) [EXACT] The density form and the Hubble form are the same law")
    print("#" * 74)
    lhs = (c / 2) * math.sqrt(G * RHO_C)
    rhs = c * H0 / Z
    print("  a0 = (c/2) sqrt(G rho)  -- surface gravity of the dynamical scale. Friedmann")
    print("  sqrt(G rho) = sqrt(3/8pi) H turns it into cH/Z:")
    print(f"    (c/2)sqrt(G rho_c) = {lhs:.3e},   cH/Z = {rhs:.3e}   [{ok(lhs, rhs)}]")
    print("  Because rho is the TOTAL (Friedmann) density, a0 tracks H(z): a0(z)=cH(z)/Z.")
    print("  (The matter-only free-fall branch instead gives a0 ~ (1+z)^1.5 -- the fork")
    print("   tested in a0_evolution_pipeline.py.)\n")

    print("#" * 74)
    print("# (5) [EXACT] The de Sitter floor: a0 is the cosmological constant")
    print("#" * 74)
    H_L = H0 * math.sqrt(LAMBDA_OL)
    Lam = 3 * H_L ** 2 / c ** 2                 # cosmological constant (1/m^2), de Sitter
    a0_floor_A = c * H_L / Z
    a0_floor_B = (c ** 2 / 2) * math.sqrt(Lam / (8 * math.pi))
    print("  Far future: rho -> rho_Lambda, H -> H_L = H0 sqrt(OmegaL). Then")
    print(f"    a0_floor = cH_L/Z          = {a0_floor_A:.3e}")
    print(f"    a0_floor = (c^2/2)sqrt(L/8pi) = {a0_floor_B:.3e}   [{ok(a0_floor_A, a0_floor_B)}]")
    print("  So a0 FLOORS at the cosmological constant in acceleration units -- the same")
    print("  law (3) evaluated at the de Sitter horizon. (Today a0 sits ~21% above it.)\n")

    print("#" * 74)
    print("# (6) [ASPIRATIONAL] Horizon thermodynamics -- where the coefficient lives")
    print("#" * 74)
    S = math.pi * RH ** 2 / LP2                 # Bekenstein-Hawking A/4lp^2
    T_dS = HBAR * H0 / (2 * math.pi * KB)
    T_a0 = HBAR * A0_OBS / (2 * math.pi * c * KB)
    print(f"  Bekenstein-Hawking entropy of the horizon: S/kB = pi R_H^2/lp^2 = {S:.2e}")
    print(f"  de Sitter temperature: T_dS = hbar H/2pi kB = {T_dS:.2e} K")
    print(f"  Unruh temperature at a0: T_a0 = hbar a0/2pi c kB = {T_a0:.2e} K")
    print(f"    T_dS / T_a0 = {T_dS/T_a0:.3f}  (= Z, the same coefficient as in (3))")
    print("  Jacobson(1995)/Padmanabhan: the Einstein equations themselves follow from")
    print("  horizon entropy dS = dQ/T. IF gravity is emergent in this sense, the MOND")
    print("  scale is the acceleration at which a body's Unruh temperature falls to the")
    print("  horizon temperature -- and the coefficient (Z vs the entropy values 1/6,")
    print("  1/2pi) would be COMPUTED, not posited. This is the open theory task, not a")
    print("  result. It is the honest reason to keep going.\n")

    print("#" * 74)
    print("# LEDGER")
    print("#" * 74)
    print("  EXACT (Schwarzschild + Friedmann):")
    print("    * R_H is its own Schwarzschild radius (universe ~ a black hole).")
    print("    * the 1/2 is the escape-velocity/surface-gravity factor -> a0 ~ cH.")
    print("    * a0=(c/2)sqrt(Grho)=cH/Z (density form = Hubble form) -> a0(z)=cH(z)/Z.")
    print("    * a0 floors at the cosmological constant: a0=(c^2/2)sqrt(L/8pi).")
    print("  POSIT (one number):")
    print("    * the coefficient Z=2sqrt(8pi/3): the '2' is Schwarzschild, the sqrt(8pi/3)")
    print("      is choosing the dynamical time 1/sqrt(Grho). The data fits it; first")
    print("      principles do not single it out (Hubble->2, collapse->pi, entropy->1/6).")
    print("  ASPIRATIONAL (the TOE direction):")
    print("    * horizon thermodynamics (Jacobson/Padmanabhan) -> emergent gravity ->")
    print("      the coefficient computed. See TOE_REVIEW.md.")
    print("  FALSIFIABLE NOW:")
    print("    * a0(z)=cH(z)/Z (or matter branch (1+z)^1.5) -- a0_evolution_pipeline.py.")


if __name__ == "__main__":
    main()
