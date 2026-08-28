"""
G4 — FC-8R NONLINEAR SPHERICAL + INFRARED.  Status: OPEN (BVP) + derivable IR estimate.
========================================================================================
REQUIREMENT: for ds^2 = -e^{2Phi}dt^2 + e^{2Lambda}dr^2 + r^2 dOmega^2 solve simultaneously
Phi,Lambda,A_t,A_r,phi,chi; test whether g_N = g^2/(g^10+a0^10)^(1/10) and whether Phi=Psi come out of the
SOLUTION (not the ansatz). Compute the IR crossover r_C ~ (r_M mu^-2)^(1/3) and report r_C/r_galaxy.
"""
import math
P = print
P("="*94); P("G4  FC-8R nonlinear spherical + IR"); P("="*94)

# --- derivable IR estimate: r_C ~ (r_M mu^-2)^(1/3), compare to galactic scales ---
KPC, MPC = 1.0, 1000.0        # work in kpc
r_M = 12.2                    # kpc, fiducial 1e11 Msun canonical-a0 (committed FC_AEST usage)
r_gal = 30.0                  # kpc, ~galactic/outer disk scale
P("  [derivable IR estimate] r_C ~ (r_M mu^-2)^(1/3), r_M = 12.2 kpc (fiducial 1e11 Msun):")
for mu_inv_Mpc in [0.3, 1.0, 3.0]:
    mu_inv = mu_inv_Mpc*MPC   # kpc
    r_C = (r_M * mu_inv**2)**(1.0/3.0)
    P(f"         mu^-1 = {mu_inv_Mpc:>4} Mpc -> r_C = {r_C:8.1f} kpc = {r_C/MPC:5.2f} Mpc ; r_C/r_gal = {r_C/r_gal:6.1f}")
P("  => the oscillatory-IR onset sits beyond galactic scales (r_C >> r_gal) only for mu^-1 >~ Mpc.")
P("  This is a FALSIFIABLE PARAMETER CONSTRAINT (mu^-1 >~ Mpc), NOT 'take mu small'. It is an INHERITED")
P("  AeST feature (2304.05134 / MNRAS 531,272); the MOND interpolation J10 does not set it.")

P("\n  [OPEN] The full nonlinear spherical solution is NOT done here:")
for s in ["Solve the coupled ODE system {Phi(r),Lambda(r),A_t(r),A_r(r),phi(r),chi(r)} from the FC-8R eqs.",
          "Verify g_N = g^2/(g^10+a0^10)^(1/10) emerges from the SOLUTION incl. metric/aether backreaction",
          "  (not just the constitutive algebra).",
          "Verify Phi=Psi comes out of the solution rather than being assumed.",
          "Confirm the three-regime structure Newtonian -> MOND -> oscillatory-IR and locate the onset radius.",
          "Report where the solution deviates from pure MOND (AeST weak-lensing tension, 2301.03499)."]:
    P(f"         - {s}")
P("\n"+"="*94); P("G4 STATUS: PARTIAL — IR crossover estimate derivable (mu^-1>~Mpc); full nonlinear BVP OPEN.")
