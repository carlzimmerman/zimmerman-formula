#!/usr/bin/env python3
"""
The deep geometry of a0 = cH/Z: what a0 IS, the UV/IR self-dual principle, and whether Z is forced.
==================================================================================================
"Work on the deep geometry." Three questions, answered with computation, honestly:

(i)  WHAT a0 IS geometrically. a0 = c^2/(2R*) is the SURFACE GRAVITY (kappa = c^2/2R) of a horizon at
     R* = c/sqrt(G rho). With rho = rho_crit this is a0 = cH/Z, Z = 2sqrt(8pi/3). Per-object, the MOND radius
     r_M = sqrt(GM/a0) is the GEOMETRIC MEAN of the Schwarzschild radius r_s = 2GM/c^2 and the cosmic horizon
     R_H = c/H:   r_M = (8pi/3)^{1/4} sqrt(r_s R_H)  (exact). a0 ~ cH IS this geometric-mean statement.

(ii) THE GEOMETRIC PRINCIPLE (the conceptual result). The inversion  r -> r_s R_H / r  swaps an object's
     gravitational scale r_s <-> the cosmic horizon R_H -- a UV/IR duality. Its self-dual FIXED POINT is
     r_sd = sqrt(r_s R_H), where the acceleration is exactly cH/2. So: MOND is the regime where an object's
     gravity (UV) and the cosmic horizon (IR) are in GEOMETRIC BALANCE -- the self-dual radius. The scaling
     a0 ~ cH is FORCED by this balance; the MOND radius sits at (8pi/3)^{1/4} = 1.70x the self-dual point.

(iii) IS Z FORCED? No -- it is a geometric O(1), not uniquely fixed; conditionally forced only by DSSYK/N-V.
     - Simple horizon criteria give Z = 1 (Unruh=dS temp / dS surface gravity cH) or Z = 2 (self-dual point /
       surface gravity c^2/2R_H) -- both 2.7-5.4x TOO BIG vs the observed Z_obs ~ 5.4.
     - Matching the data needs an EXTRA factor ~2.7-2.9 on top of the self-dual point: sqrt(8pi/3)=2.894
       (framework, the Friedmann density packaging) or pi (Milgrom's 2pi). Both fit ~6-14%; NEITHER is unique.
     - DSSYK (N-V, de Sitter = spectral center) ties Z to the q-Gaussian band edge: Z = 4 rho0(q)/sqrt(1-q),
       reproduced at q* ~ 0.926. But q is a FREE coupling, so this PREDICTS the coupling given Z, it does not
       independently FORCE Z. Z is pinned decisively only by a ~6% a0 measurement (5.79 vs 6.28) or by settling
       the contested de Sitter=center identification.

This matches the independent literature review: no emergent-gravity framework derives a0's coefficient from
below -- it is reproduced, not predicted. What IS geometrically robust is the SCALING and the self-dual
structure. Needs numpy.
"""
import numpy as np

c = 2.998e8; G = 6.674e-11; H0 = 67e3/3.086e22; OL = 0.685
Msun = 1.989e30; AU = 1.496e11
a0_obs = 1.2e-10; cH = c*H0
Z = 2*np.sqrt(8*np.pi/3)


def rho0_qgauss(q, K=4000):
    qq = np.prod(1-q**np.arange(1, K)); prod = np.prod((1+q**np.arange(0, K))**2)
    return qq/(2*np.pi)*prod*np.sqrt(1-q)/2


def main():
    print("#"*90)
    print("# The deep geometry of a0 = cH/Z: horizon surface gravity, the UV/IR self-dual MOND scale, and Z")
    print("#"*90 + "\n")

    print("="*90); print("(i) WHAT a0 IS: surface gravity of a horizon; r_M = geometric mean of r_s and R_H"); print("="*90)
    rs = 2*G*Msun/c**2; RH = c/H0; rM = np.sqrt(G*Msun/a0_obs)
    print(f"  a0 = c^2/(2R*),  R* = c/sqrt(G rho)  -> a0 is the surface gravity (kappa=c^2/2R) of a cosmic horizon.")
    print(f"  for 1 Msun: r_s = {rs/1e3:.2f} km | R_H = {RH:.2e} m | r_M = {rM/AU:.0f} AU")
    print(f"  r_M / sqrt(r_s R_H) = {rM/np.sqrt(rs*RH):.4f} = (8pi/3)^(1/4) = {(8*np.pi/3)**0.25:.4f}  (exact geometric mean)\n")

    print("="*90); print("(ii) THE PRINCIPLE: MOND is the UV/IR self-dual radius (gravity <-> horizon balance)"); print("="*90)
    rsd = np.sqrt(rs*RH); a_sd = G*Msun/rsd**2
    print(f"  inversion r -> r_s R_H / r  swaps r_s <-> R_H (UV<->IR). Fixed point r_sd = sqrt(r_s R_H) = {rsd/AU:.0f} AU,")
    print(f"  where a = cH/2 = {a_sd/1e-10:.2f}e-10. The MOND radius r_M = {rM/AU:.0f} AU = {rM/rsd:.2f}x r_sd.")
    print(f"  => MOND = the regime where an object's gravity and the cosmic horizon are in GEOMETRIC BALANCE.")
    print(f"     The scaling a0~cH is forced by the self-dual bridge; the offset is (8pi/3)^(1/4) = {(8*np.pi/3)**0.25:.3f}.\n")

    print("="*90); print("(iii) IS Z FORCED? geometric O(1), not unique; conditionally forced by DSSYK/N-V"); print("="*90)
    print(f"  observed Z_obs = cH0/a0 = {cH/a0_obs:.2f} (H0=67) .. {c*73e3/3.086e22/a0_obs:.2f} (H0=73)")
    print(f"  {'criterion':46}{'Z':>8}{'a0 e-10':>9}{'vs obs':>8}")
    for name, Zc in [("Unruh T=T_dS / dS surface gravity cH", 1.0),
                     ("self-dual point / kappa=c^2/2R_H", 2.0),
                     ("FRAMEWORK free-fall at rho_crit 2sqrt(8pi/3)", Z),
                     ("Milgrom 2pi", 2*np.pi),
                     ("event-horizon 2sqrt(8pi/3)/sqrt(OmL)", Z/np.sqrt(OL))]:
        print(f"  {name:46}{Zc:>8.3f}{cH/Zc/1e-10:>9.2f}{cH/Zc/a0_obs-1:>+7.0%}")
    qf = np.linspace(0.88, 0.96, 2000); vals = np.array([4*rho0_qgauss(q)/np.sqrt(1-q) for q in qf])
    qstar = qf[np.argmin(np.abs(vals-Z))]
    print(f"\n  simple criteria give Z=1 or 2 (2.7-5.4x too big); the data need an extra ~2.7-2.9 =")
    print(f"  sqrt(8pi/3)={np.sqrt(8*np.pi/3):.3f} (framework) or pi={np.pi:.3f} (Milgrom). DSSYK/N-V: Z=4 rho0(q)/sqrt(1-q)")
    print(f"  reproduced at q*={qstar:.4f} -- but q is FREE, so this predicts the coupling given Z, it does not force Z.\n")

    print("="*90); print("VERDICT"); print("="*90)
    print("""  The SCALING a0 ~ cH -- equivalently the geometric-mean / UV-IR self-dual structure r_M = (8pi/3)^(1/4)
  sqrt(r_s R_H) -- is geometrically robust and is the real, elegant content: MOND is the self-dual regime where
  an object's gravity and the cosmic horizon balance. The COEFFICIENT Z ~ 5.4 is a geometric O(1) that the
  simplest horizon criteria UNDER-shoot (they give 1-2); the data demand an extra Friedmann factor sqrt(8pi/3)
  (framework) or 2pi (Milgrom), neither uniquely forced. Z is pinned only by the microscopics (DSSYK/N-V ties it
  to q*~0.93, conditional on the contested de Sitter=center) or by a ~6% a0 measurement separating 5.79 from
  6.28. This is exactly the field-wide situation: emergent gravity REPRODUCES a0's scale, it does not PREDICT
  the coefficient from below. The deep geometry we CAN claim is the self-dual bridge; the coefficient is honest,
  bounded, open.""")
    print("="*90)


if __name__ == "__main__":
    main()
