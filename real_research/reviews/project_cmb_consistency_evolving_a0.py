#!/usr/bin/env python3
"""
The biggest open consistency door: does a0 = cH(z)/Z survive the CMB at recombination? Worked honestly.
=====================================================================================================
This is the door I had been assuming away. At z~1100 the formula a0(z)=cH(z)/Z makes a0 ~ 2e-6 m/s^2 -- about
20000x its value today. NAIVELY that looks catastrophic: the gravitational acceleration of an acoustic-scale
perturbation is g_int ~ 4e-10 m/s^2 << a0(1100), which would put CMB perturbations DEEP in the MOND regime, with a
gravity enhancement sqrt(a0/g_int) ~ 70x -- enough to destroy the acoustic peaks measured to <1%. If that were the
real comparison, evolving a0 would be EXCLUDED by the CMB at enormous significance.

IT IS NOT THE REAL COMPARISON -- and being honest means showing why my own alarm is wrong:
  1. GRADIENT SUPPRESSION (the framework's own structure, the decisive reason). On the near-homogeneous FRW
     background, the MOND term lives in the AeST free function's Y^{3/2} piece, and Y is built from GRADIENTS of
     the field. The homogeneous background has Ybar = 0, so the MOND/a0 term enters perturbations only at O(delta^3)
     -- a0 is ABSENT from the LINEAR equations that set the CMB. (bridge1_aest_equations.md / _linear_boltzmann.py.)
  2. EFE FREEZING (the intuition, complementary). Every perturbation sits in the cosmic acceleration a_H = cH(z).
     For EVOLVING a0, a_H/a0 = cH/(cH/Z) = Z = 5.789 at EVERY epoch -- frozen by construction. So the external
     cosmic field is ALWAYS ~6x a0 (above the MOND scale): the system is EFE-quasi-Newtonian, NOT isolated deep-MOND,
     and it is no more MOND-ish at recombination than today. (For CONSTANT a0, a_H/a0 = cH(z)/a0 -> 1e5 at z=1100,
     i.e. even MORE screened -- so constant a0 is cleanly Newtonian at recombination; evolving a0 keeps a small,
     epoch-CONSTANT residual.)
  => the naive isolated-deep-MOND comparison (g_int vs a0) is the WRONG one; the cosmic field screens it.

THE RESIDUAL, AND THE HONEST LIMIT: even granting the EFE quasi-static boost, G_eff/G ~ nu(a_H/a0) = nu(Z) ~ 1.0-1.17
at recombination, epoch-FROZEN -- small, and not growing toward early times. The cleanest reason (gradient/O(delta^3)
suppression) gives exactly ZERO at linear order, but its numerical check in the repo is partly circular (it encodes
the theorem) and Y^{3/2} is non-analytic at Y=0, so a rigorous proof needs a real modified-Boltzmann (hi_class+AeST)
run. VERDICT: NOT the deep-MOND catastrophe the naive estimate suggests -- the alarm is corrected by gradient
suppression + EFE freezing -- but CMB-safety is LEANING-SAFE, not rigorously nailed. The single biggest under-
resolved consistency question. Needs numpy.
"""
import numpy as np

c = 2.998e8; G = 6.674e-11; Mpc = 3.086e22
H0 = 67.4e3/Mpc; Z = 2*np.sqrt(8*np.pi/3)
OmM, OmL = 0.315, 0.685
E = lambda z: np.sqrt(OmM*(1+z)**3 + OmL)
a0_const = 1.2e-10
z_rec = 1100.0
Phi = 2e-5; lam_c = 150*Mpc           # matter-era potential depth; acoustic comoving scale


def nu(x):                            # MOND "nu" interpolation (g_obs = nu(g_ext/a0) g_ext), simple form
    return 0.5 + np.sqrt(0.25 + 1.0/x)


def main():
    print("#"*100); print("# CMB consistency of evolving a0 = cH(z)/Z at recombination -- worked honestly"); print("#"*100 + "\n")
    aH = c*H0*E(z_rec); a0e = aH/Z; g_int = c**2*Phi*(1+z_rec)/lam_c

    print("="*100); print("(1) THE NAIVE ALARM (isolated deep-MOND) -- looks catastrophic"); print("="*100)
    print(f"   a0_evolve(z=1100) = cH(1100)/Z = {a0e:.3e} m/s^2  (~{a0e/a0_const:.0f}x a0 today)")
    print(f"   g_int (acoustic perturbation)  = {g_int:.3e} m/s^2")
    print(f"   naive g_int/a0_evolve = {g_int/a0e:.2e}  -> 'deep MOND', enhancement sqrt(a0/g_int) = {np.sqrt(a0e/g_int):.0f}x")
    print(f"   IF real, that destroys the <1%-measured acoustic peaks. But it is the WRONG comparison:\n")

    print("="*100); print("(2) WHY THE ALARM IS WRONG: the cosmic field screens it (EFE freezing)"); print("="*100)
    print(f"   external cosmic field a_H = cH(1100) = {aH:.3e} m/s^2")
    print(f"   a_H/a0_evolve = {aH/a0e:.3f} = Z  (FROZEN at every epoch by construction)  -> external field > a0")
    print(f"   a_H/a0_const  = {aH/a0_const:.2e}        -> constant a0 is ~1e5x screened (cleanly Newtonian)")
    print(f"   Both have a_H > a0, so the system is EFE-quasi-Newtonian, NOT isolated deep-MOND. g_int vs a0 is moot.\n")

    print("="*100); print("(3) THE DECISIVE REASON + the residual"); print("="*100)
    print("   GRADIENT SUPPRESSION: the MOND Y^{3/2} term is gradient-built; on FRW Ybar=0, so a0 enters only at")
    print("   O(delta^3) -> ABSENT from the LINEAR CMB equations. (Cleanest; gives exactly 0 at linear order.)")
    print(f"   Residual EFE quasi-static boost (if any): G_eff/G ~ nu(a_H/a0):")
    print(f"     evolving a0:  nu(Z={Z:.2f})      = {nu(Z):.3f}   (epoch-FROZEN, ~{100*(nu(Z)-1):.0f}% at all z)")
    print(f"     constant a0:  nu({aH/a0_const:.0e}) = {nu(aH/a0_const):.5f}   (essentially 1 -> cleanly Newtonian)")
    print(f"   So evolving a0 keeps a small, epoch-constant <~17% residual; constant a0 keeps none. Neither is 70x.\n")

    print("="*100); print("VERDICT"); print("="*100)
    print(f"""  The naive 'a0 is 20000x bigger at recombination -> deep-MOND catastrophe' is WRONG: it ignores that the cosmic
  acceleration a_H = cH(z) screens the perturbation, and for evolving a0 the ratio a_H/a0 = Z is FROZEN at every
  epoch -- the early universe is no more MOND-ish than today. The decisive structural reason is gradient/O(delta^3)
  suppression (a0 absent from the linear equations); the EFE freezing is the complementary intuition. So evolving a0
  is NOT excluded by the CMB. HONEST LIMIT: it keeps a small epoch-constant residual (G_eff/G up to ~1.17 from the
  EFE view) where constant a0 keeps essentially none, and the clean O(delta^3) cancellation is checked only semi-
  circularly (Y^{{3/2}} is non-analytic at Y=0). So: LEANING CMB-SAFE for a good structural reason, but the rigorous
  proof needs a real modified-Boltzmann (hi_class+AeST) run. This is the biggest single under-resolved consistency
  door -- survived, not slammed shut.""")
    print("#"*100)


if __name__ == "__main__":
    main()
