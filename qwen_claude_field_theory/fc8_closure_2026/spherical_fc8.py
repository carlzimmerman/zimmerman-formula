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

# --- Gate F IR: r_C from the committed MNRAS 531,272 formula; freeze mu^-1 fiducial by r_C requirement ---
# r_C = (1/3)[ 18 r_M mu^-2 / (1+3|Delta|) ]^(1/3),  r_M = sqrt(G M_b / a0)   (MNRAS 531,272 eq.)
import math
G_, MSUN, KPC, MPC = 6.6743e-11, 1.98892e30, 3.0857e19, 3.0857e22
Mb, a0 = 6.0e10*MSUN, 1.2e-10                     # MW-like baryonic mass; canonical a0
r_M_m = math.sqrt(G_*Mb/a0); r_M_kpc = r_M_m/KPC  # r_M
def r_C_kpc(mu_inv_Mpc, Delta=0.0):
    mu_inv_m = mu_inv_Mpc*MPC
    return (1.0/3.0)*(18.0*r_M_m*mu_inv_m**2/(1+3*abs(Delta)))**(1.0/3.0)/KPC
P(f"  r_M = sqrt(G M_b/a0) = {r_M_kpc:.2f} kpc  (M_b=6e10 Msun, a0=1.2e-10)  [Carl: 8.35 kpc, match={abs(r_M_kpc/8.35-1)<0.02}]")
P("  r_C = (1/3)[18 r_M mu^-2/(1+3|Delta|)]^(1/3)  (Delta=0):")
for muinv in [1.0, 3.0, 13.4]:
    rc = r_C_kpc(muinv)
    P(f"         mu^-1 = {muinv:>5} Mpc -> r_C = {rc:8.1f} kpc = {rc/1000:5.3f} Mpc")
# invert for r_C = 1 Mpc:  1000 kpc = (1/3)(18 r_M mu^-2)^(1/3)  =>  mu^-1 = sqrt( (3*1000)^3 / (18 r_M[kpc]) )
mu_for_1Mpc = math.sqrt((3*1000.0)**3/(18*r_M_kpc))/1000.0   # Mpc
P(f"\n  [VERIFIED] r_C >= 1 Mpc requires mu^-1 >= {mu_for_1Mpc:.1f} Mpc (NOT 2.1 Mpc -- Carl's intermediate")
P(f"             formula mu^-1=[2/3 r_M (1 Mpc)^3]^(1/2) is dimensionally length^2, an arithmetic slip).")
P(f"  [FIDUCIAL] mu^-1 = 3 Mpc (Carl's frozen exploratory value) gives r_C = {r_C_kpc(3.0):.0f} kpc ~ 0.37 Mpc:")
P(f"             beyond the disk (~30 kpc) but NOT beyond ~1 Mpc. Honest: 3 Mpc pushes the IR onset past the")
P(f"             rotation-curve domain; the conservative r_C>=1 Mpc target needs mu^-1~{mu_for_1Mpc:.0f} Mpc.")
P("  This is a FALSIFIABLE PARAMETER CONSTRAINT, NOT 'take mu small'. Inherited AeST feature (MNRAS 531,272);")
P("  the J10 interpolation does not set it.")

P("\n  [OPEN] The full nonlinear spherical solution is NOT done here:")
for s in ["Solve the coupled ODE system {Phi(r),Lambda(r),A_t(r),A_r(r),phi(r)} from the FC-FINAL eqs",
          "  (no sigma; a0 constant) WITHOUT assuming the vector vanishes (the m_x scale, PRD 110.024062).",
          "Verify g_N = g^2/(g^10+a0^10)^(1/10) emerges from the SOLUTION incl. metric/aether backreaction",
          "  (not just the constitutive algebra).",
          "Verify Phi=Psi comes out of the solution rather than being assumed.",
          "Confirm the three-regime structure Newtonian -> MOND -> oscillatory-IR and locate the onset radius.",
          "Report where the solution deviates from pure MOND (AeST weak-lensing tension, 2301.03499)."]:
    P(f"         - {s}")
P("\n"+"="*94); P("G4 STATUS: PARTIAL — IR crossover estimate derivable (mu^-1>~Mpc); full nonlinear BVP OPEN.")
