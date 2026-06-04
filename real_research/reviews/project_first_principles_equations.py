#!/usr/bin/env python3
"""
First-principles equation sheet: what 32pi is, and every equivalent form of a0 (one scale, sqrt(Lambda)).
=========================================================================================================
Carl: "what could the 32pi be? a cube times a sphere?" and "keep going on first-principles equations."

PART A -- decompose 32pi honestly:
  32pi = 4 * 8pi  =  (surface-gravity factor)^2  x  (Einstein coupling)
       8pi  = 2 * 4pi  =  (relativistic 2)  x  (solid angle / unit 2-sphere area)
  => 32pi = 2^3 * 4pi = 8 * 4pi : the 4pi IS a genuine sphere (solid angle / Gauss's law / horizon area);
     the 8 = 2^3 is THREE factors of 2 from the gravitational couplings (surface gravity squared x relativistic),
     "cube-like" (2^3) but physical, NOT literally cube vertices (that 8-fixed-point reading is the retired
     T^3/Z2 numerology). And Z^2 = 32pi/3 = 8 * (4pi/3): the /3 turns the sphere into the BALL (the Friedmann
     volume integral, M = rho * 4pi/3 R^3). So honestly: 32pi = coupling-8 x SPHERE(4pi); Z^2 = coupling-8 x BALL(4pi/3).
     Carl's "sphere" is real; the "cube" is 2^3 coupling factors, and the ball appears in Z^2.

PART B -- every equivalent first-principles form of a0 (ALL exact, all = 9.36e-11; facets of a0 ~ sqrt(Lambda)):
  (1) de Sitter curvature   a0 = c^2 sqrt(Lambda/32pi)
  (2) vacuum free-fall      a0 = (c/2) sqrt(G rho_Lambda)
  (3) apparent horizon      a0 = c H_dS / Z         (H_dS = c sqrt(Lambda/3))
  (4) vacuum-energy seesaw  a0 = c E_Lambda^2 / (2 hbar E_Planck)
  (5) Planck/entropy        a0 = (sqrt(pi)/Z) (c^2/lP) / sqrt(S_dS)
  (6) de Sitter temperature a0 = (2pi/Z) c (kB T_dS / hbar)
Plus the derived companions: MOND length ell_M = c^2/a0 = Z R_dS; transition radius r_M = sqrt(Z/2) sqrt(r_s R_H);
vacuum scale E_Lambda = sqrt((2/Z) E_Planck E_Hubble).

HONEST: these are EXACT identities -- the SAME relation a0 ~ sqrt(Lambda) written six ways, each exposing a
different physical pairing (curvature, density, horizon, UV/IR seesaw, entropy, temperature). The geometric
coefficient (32pi: sphere 4pi + coupling 8; Z^2: ball 4pi/3 + coupling 8) is real but REPRODUCED, not forced; and
none of it derives the VALUE of Lambda (E_Lambda/E_Planck ~ 1.8e-31 = the cosmological-constant problem, open).
Needs numpy.
"""
import numpy as np

c = 2.998e8; G = 6.674e-11; hbar = 1.055e-34; kB = 1.381e-23; eV = 1.602e-19; Mpc = 3.086e22
H0 = 67.4e3/Mpc; OmL = 0.685
Z = 2*np.sqrt(8*np.pi/3)
lP = np.sqrt(hbar*G/c**3)
Lam = 3*OmL*H0**2/c**2          # constant de Sitter Lambda (1/m^2)


def main():
    print("#"*92); print("# First-principles equation sheet: 32pi, and every form of a0"); print("#"*92 + "\n")

    print("="*92); print("PART A -- what is 32pi?"); print("="*92)
    print(f"  32pi = {32*np.pi:.4f}")
    print(f"  = 4 * 8pi      : 4 = (surface-gravity 2)^2 ; 8pi = Einstein coupling   [{4*8*np.pi:.4f}]")
    print(f"  = 2^3 * 4pi    : 8 = three 2's (surf-grav^2 x relativistic) ; 4pi = unit 2-SPHERE area [{8*4*np.pi:.4f}]")
    print(f"  Z^2 = 32pi/3 = 8 * (4pi/3) = 8 * BALL volume  [{8*4*np.pi/3:.4f} = {32*np.pi/3:.4f}]")
    print(f"  => the SPHERE (4pi) is real (solid angle); the 8 is coupling factors (2^3), NOT cube vertices")
    print(f"     (that's the retired numerology); the /3 turns sphere->BALL (Friedmann volume). Carl half-right.\n")

    print("="*92); print("PART B -- every equivalent first-principles form of a0 (all = 9.36e-11)"); print("="*92)
    H_dS = c*np.sqrt(Lam/3)
    rho_L = OmL*3*H0**2/(8*np.pi*G)
    E_L = (rho_L*c**2*(hbar*c)**3)**0.25
    E_P = np.sqrt(hbar*c**5/G); E_H = hbar*H0
    RdS = np.sqrt(3/Lam); S_dS = np.pi*RdS**2/lP**2
    T_dS = hbar*H_dS/(2*np.pi*kB)
    forms = [
        ("(1) de Sitter curvature   c^2 sqrt(Lambda/32pi)", c**2*np.sqrt(Lam/(32*np.pi))),
        ("(2) vacuum free-fall      (c/2) sqrt(G rho_Lambda)", (c/2)*np.sqrt(G*rho_L)),
        ("(3) apparent horizon      c H_dS / Z", c*H_dS/Z),
        ("(4) vacuum-energy seesaw  c E_Lambda^2/(2 hbar E_Planck)", c*E_L**2/(2*hbar*E_P)),
        ("(5) Planck / entropy      (sqrt(pi)/Z)(c^2/lP)/sqrt(S_dS)", (np.sqrt(np.pi)/Z)*(c**2/lP)/np.sqrt(S_dS)),
        ("(6) de Sitter temperature (2pi/Z) c (kB T_dS/hbar)", (2*np.pi/Z)*c*(kB*T_dS/hbar)),
    ]
    for name, val in forms:
        print(f"  {name:<52} = {val:.3e} m/s^2")
    print(f"  => all six agree (to the H0/OmL choice): ONE relation a0 ~ sqrt(Lambda), six physical faces.\n")

    print("="*92); print("PART C -- the derived companions"); print("="*92)
    print(f"  MOND length    ell_M = c^2/a0 = Z R_dS         = {c**2/(c**2*np.sqrt(Lam/(32*np.pi))):.3e} m  (= Z x {RdS:.2e})")
    print(f"  vacuum scale   E_Lambda = sqrt((2/Z) E_P E_H)  = {np.sqrt((2/Z)*E_P*E_H)/eV*1e3:.3f} meV (vs {E_L/eV*1e3:.3f})")
    print(f"  transition r_M = sqrt(Z/2) sqrt(r_s R_H): (8pi/3)^(1/4) = sqrt(Z/2) = {(8*np.pi/3)**0.25:.4f}")
    print(f"  dark sector: a0 = c^2 sqrt(Lambda/32pi) AND rho_Lambda = Lambda c^2/8piG -- ONE scale sqrt(Lambda).\n")

    print("="*92); print("VERDICT (honest)"); print("="*92)
    print(f"""  32pi = (coupling 8) x (SPHERE 4pi); Z^2 = 32pi/3 = (coupling 8) x (BALL 4pi/3). Real geometry: the sphere
  is the solid angle, the ball the Friedmann volume, the 8 is 2^3 coupling factors (not cube vertices). a0 has
  SIX exact equivalent forms -- curvature, density, horizon, UV/IR seesaw, entropy, temperature -- all the one
  relation a0 ~ sqrt(Lambda). The coefficient is geometric and traceable but REPRODUCED, not forced; and none of
  it derives WHY Lambda has its value (E_Lambda/E_Planck ~ 1.8e-31 = the cosmological-constant problem, open).""")
    print("#"*92)


if __name__ == "__main__":
    main()
