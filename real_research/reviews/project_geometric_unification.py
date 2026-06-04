#!/usr/bin/env python3
"""
Deep geometry II: the UV/IR geometric-mean unification, a0 as the cosmological curvature, and the two-horizon
question that the data (not geometry) must decide.
============================================================================================================
Pushing the deep geometry further. Three structural results and one sharpened tension:

A. THE GEOMETRIC-MEAN THEME RUNS AT TWO LEVELS (not one):
     SCALE:  r_M = sqrt(GM/a0) = (8pi/3)^{1/4} sqrt(r_s R_H)   -- geometric mean of the UV length r_s and IR length R_H
     LAW:    g_obs = sqrt(g_N * a0)  (deep-MOND)               -- geometric mean of the LOCAL accel g_N and COSMIC accel a0
   MOND is a UV/IR geometric-mean structure in BOTH its scale and its dynamics. The deep-MOND law is itself a
   geometric mean, and it is coefficient-clean -- Z enters ONLY through a0 = cH/Z.

B. a0 IS THE COSMOLOGICAL CURVATURE (the a0-Lambda identity):
     a0/c^2 = 1/(Z R_H) is an inverse length -- a curvature. In the event-horizon reading,
        a0 = c^2 sqrt(Lambda / 32pi)   <=>   Lambda = 32pi (a0/c^2)^2 ,
   so the MOND acceleration is the de Sitter curvature scale sqrt(Lambda) expressed as an acceleration. The
   galactic-dynamics scale and the cosmological constant are ONE geometric quantity.

C. THE LEGITIMATE HOME OF Z^2 = 32pi/3:
     the a0-Lambda conversion factor is 32pi = 3 Z^2, with Z^2 = (2 sqrt(8pi/3))^2 = 32pi/3. So the project's
   number Z^2 = 32pi/3 -- once (wrongly) used to "derive the Standard Model" (numerology) -- has a REAL home:
   it is the geometric conversion between the cosmological constant and the MOND acceleration. Reclaimed.

THE SHARPENED TENSION (the deep-geometry payoff, honestly unresolved):
   There are TWO horizons, and they give two a0's that DIVERGE into the past and CONVERGE in the de Sitter future:
     EVENT  horizon (global / de Sitter / DSSYK):  a0 = c^2 sqrt(Lambda/32pi) = 0.93e-10, CONSTANT -- the cleanest identity.
     APPARENT horizon (local / Hubble / Padmanabhan): a0 = cH(z)/Z, today 1.12e-10, RISING -- what MUSE favors.
   The high-z a0(z) measurement is exactly where they diverge, so it DISCRIMINATES them -- and MUSE picks the
   APPARENT (local) horizon. So geometry offers the more elegant identity (a0 = the cosmological curvature,
   constant), but the DATA select the local apparent horizon (a0 tracks the evolving H). Consequence: the
   framework should ground itself in LOCAL apparent-horizon emergent gravity (Padmanabhan/Jacobson), and the
   DSSYK *event*-horizon derivation -- though microscopically more rigorous -- is the data-disfavored branch.
   Geometry sharpens the question; only the a0(z) data answer it. Needs numpy.
"""
import numpy as np

c = 2.998e8; G = 6.674e-11; H0 = 67e3/3.086e22; OL = 0.685
Msun = 1.989e30; AU = 1.496e11
Z = 2*np.sqrt(8*np.pi/3); a0_app = c*H0/Z; HL = H0*np.sqrt(OL)


def main():
    print("#"*92)
    print("# Deep geometry II: UV/IR geometric-mean unification, a0 = cosmological curvature, the two-horizon question")
    print("#"*92 + "\n")

    print("="*92); print("A. THE GEOMETRIC-MEAN THEME AT TWO LEVELS"); print("="*92)
    rs = 2*G*Msun/c**2; RH = c/H0; rM = np.sqrt(G*Msun/(1.2e-10))
    print(f"  SCALE: r_M = (8pi/3)^1/4 sqrt(r_s R_H);  check r_M/sqrt(r_s R_H) = {rM/np.sqrt(rs*RH):.4f} = {(8*np.pi/3)**0.25:.4f}")
    print(f"  LAW:   g_obs = sqrt(g_N a0)  (deep-MOND) -- observed gravity = geometric mean of local g_N and cosmic a0")
    print(f"  => MOND is a UV/IR geometric mean at BOTH scale and dynamics; the deep-MOND LAW is coefficient-clean.\n")

    print("="*92); print("B. a0 AS THE COSMOLOGICAL CURVATURE (the a0-Lambda identity)"); print("="*92)
    Lam = 3*HL**2/c**2
    a0_evt = c**2*np.sqrt(Lam/(32*np.pi))
    print(f"  Lambda = 3H_L^2/c^2 = {Lam:.3e} m^-2;  a0/c^2 = 1/(Z R_H) = {a0_app/c**2:.3e} m^-1 (an inverse length = curvature)")
    print(f"  a0 = c^2 sqrt(Lambda/32pi) = {a0_evt/1e-10:.3f}e-10  <=>  Lambda = 32pi (a0/c^2)^2")
    print(f"  => a0 is the de Sitter curvature scale sqrt(Lambda) as an acceleration: MOND scale = IR curvature.\n")

    print("="*92); print("C. THE LEGITIMATE HOME OF Z^2 = 32pi/3"); print("="*92)
    print(f"  a0-Lambda conversion = 32pi = 3 Z^2;  Z^2 = 32pi/3 = {32*np.pi/3:.3f}.")
    print(f"  Z^2 = 32pi/3 is NOT an SM-deriving number (that was numerology) -- it is the geometric conversion")
    print(f"  between the cosmological constant and the MOND acceleration: Lambda = 3 Z^2 (a0/c^2)^2. Reclaimed.\n")

    print("="*92); print("THE SHARPENED TWO-HORIZON TENSION (data decides, not geometry)"); print("="*92)
    print(f"  EVENT   (global/de Sitter/DSSYK): a0 = c^2 sqrt(Lambda/32pi) = {a0_evt/1e-10:.2f}e-10, CONSTANT  [cleanest identity]")
    print(f"  APPARENT(local/Hubble/Padmanabhan): a0 = cH(z)/Z, today {a0_app/1e-10:.2f}e-10, RISING            [MUSE favors]")
    print(f"  the two diverge into the past (high-z a0(z) discriminates) and converge in the de Sitter future.")
    print(f"  MUSE -> APPARENT. So the elegant identity (a0 = cosmological curvature, constant) is data-disfavored;")
    print(f"  the framework should ground in LOCAL apparent-horizon emergent gravity, and the DSSYK event-horizon")
    print(f"  derivation -- more rigorous but tied to the constant/Lambda branch -- is the one the data argue against.")
    print("="*92)


if __name__ == "__main__":
    main()
