#!/usr/bin/env python3
"""
ROUTE B: FULL nonlinear AeST Y-Q coupled solution in deep cluster cores.

Question: the banked undershoot (~4.4x core-avg) used the MOND phantom (g_obs)
as a proxy. Does the FULL coupled AeST field equation -- the modified-Helmholtz
single-field PDE (Durakovic-Skordis 2312.00889 Eq.2.40) with the mu^2*Phi
mass term (the Q-sector / ghost-condensate dust) and the J(Y) MOND sector --
source EXTRA central mass beyond the naive phantom? Durakovic-Skordis FIND a
RAR PEAK above MOND + "more compressed gas" -- is that enhancement in the CORE
(closes the ~2.3e14 Msun target) or only the OUTSKIRTS?

We solve the AeST two-component system (their Eqs. 2.43-2.44) in spherical
symmetry for a realistic cluster gas + BCG, scan {1/mu screening length, chi_inf
boundary shift, lambda_s}, and compute M_AeST(<420 kpc) vs the eRASS1/CLASH core
target. Then we read off WHAT 1/mu the core-enhancement needs and whether it
survives.

Framework footing: a0 = 9.36e-11 m/s^2 (NOT asserted derived). Both-ways.

Units: SI internally for masses; accelerations in m/s^2; radii in meters.
"""
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

# ---- constants (SI) ----
G    = 6.674e-11
Msun = 1.989e30
kpc  = 3.086e19
Mpc  = 1000.0*kpc
a0   = 9.36e-11           # framework a0 (quarantine: NOT derived)

# ================================================================
#  AeST single-field equation, Durakovic-Skordis 2312.00889
#  Eq.(2.40):  (1/r^2) d/dr [ r^2 M(x) dPhi/dr ] + mu^2 Phi = 4 pi G_N rho_b
#  with x = |Phi'|/a0, and (simple interp, lambda_s=inf) Eq.(2.39):
#     M(x) = (-1 + sqrt(1+4x)) / (1 + sqrt(1+4x))
#  Two-component Hamiltonian form (Eqs 2.43-2.44 / 3.18-3.19) is what we evolve
#  to avoid the |Phi'|=0 apparent singularity:
#     P_Phi = r^2 M(x) Phi'   (canonical momentum)
#     dP_Phi/dr = -r^2 mu^2 Phi + 4 pi G_N r^2 rho_b   [matter-sourced form]
#     dPhi/dr   = Phi'(P_Phi, r)   inverted from P_Phi = r^2 M(x) Phi'
#  mu^2 is the AeST weak-field mass parameter (Q-sector); 1/mu = screening length.
# ================================================================

def Mfun(x):
    """AeST interpolation M(x), simple function, lambda_s=inf (Eq.2.39).
       x = |Phi'|/a0.  M->x (deep MOND) as x->0; M->1 (Newton) as x->inf."""
    x = np.abs(x)
    s = np.sqrt(1.0 + 4.0*x)
    return (-1.0 + s) / (1.0 + s)

def invert_Phiprime(PPhi, r):
    """Given canonical momentum P_Phi = r^2 M(x) Phi' and Phi'=a0*x*sign,
       solve P_Phi/r^2 = a0 * x * M(x) * sign for x>=0.  z_tilde = |P_Phi|/(a0 r^2)."""
    if r <= 0:
        return 0.0
    zt = abs(PPhi) / (a0 * r*r)        # = x*M(x), monotone increasing in x
    if zt <= 0:
        return 0.0
    # x*M(x) = x*(-1+sqrt(1+4x))/(1+sqrt(1+4x)).  Solve x*M(x)=zt.
    f = lambda x: x*Mfun(x) - zt
    # bracket: x*M(x) ~ x^2 for small x (deep MOND), ~ x for large x
    hi = max(2.0*zt, np.sqrt(zt)*2.0, 1e-6)
    while f(hi) < 0:
        hi *= 2.0
    x = brentq(f, 0.0, hi, xtol=1e-14, rtol=1e-12)
    return np.sign(PPhi) * a0 * x      # returns Phi' (signed)

# ---- baryon model: cluster gas (beta-model) + BCG (point-ish) ----
def make_cluster(M500=1e15*Msun, fgas=0.13, M_BCG=1e12*Msun,
                 rc=120.0*kpc, beta=0.67, r500=1.4*Mpc):
    """Rich relaxed cluster. Gas as a beta-model normalized so gas mass within
       r500 = fgas*M500.  BCG as a compact Hernquist-ish core (a_BCG=15 kpc)."""
    a_BCG = 15.0*kpc
    # beta-model density shape  rho_gas ~ (1+(r/rc)^2)^(-3 beta/2)
    def shape(r): return (1.0 + (r/rc)**2)**(-1.5*beta)
    # normalize gas mass to fgas*M500 within r500
    rr = np.logspace(np.log10(0.5*kpc), np.log10(r500), 4000)
    integ = np.trapz(4*np.pi*rr**2 * shape(rr), rr)
    rho0 = (fgas*M500) / integ
    def rho_gas(r): return rho0*shape(r)
    def Mgas_enc(r):
        rr2 = np.logspace(np.log10(0.3*kpc), np.log10(max(r,0.4*kpc)), 1500)
        return np.trapz(4*np.pi*rr2**2 * rho0*shape(rr2), rr2)
    def Mbcg_enc(r): return M_BCG * r*r/(r+a_BCG)**2
    def rho_bcg(r):  # Hernquist density
        return (M_BCG*a_BCG)/(2*np.pi) / (r*(r+a_BCG)**3)
    def rho_b(r):  return rho_gas(r) + rho_bcg(r)
    def Mbar_enc(r): return Mgas_enc(r) + Mbcg_enc(r)
    return rho_b, Mbar_enc

# ---- MOND phantom proxy (the BANKED method, for reference) ----
def mond_total_mass(Mbar_enc, r):
    """Naive AQUAL-simple MOND: g_obs from g_bar via the simple nu, then
       M_tot = g_obs r^2 / G.  This is the banked ~4.4x-undershoot proxy."""
    gN = G*Mbar_enc(r)/r**2
    # simple interpolation g_obs = g_bar * (1/2 + sqrt(1/4 + a0/g_bar))
    g = gN*(0.5 + np.sqrt(0.25 + a0/gN))
    return g*r**2/G

# ---- FULL AeST: integrate the two-component Hamiltonian system inward->outward ----
def solve_aest(rho_b, Mbar_enc, inv_mu, chi_inf=0.0, lam_s=np.inf,
               r_in=2.0*kpc, r_out=8.0*Mpc, GN=None):
    """
    Integrate (Hamiltonian form):
      dPhi/dr   = invert_Phiprime(P_Phi, r)
      dP_Phi/dr = -mu^2 r^2 Phi + 4 pi G_N r^2 rho_b(r)
    mu = 1/inv_mu.  GN: rescaled Newton G (here = G; lam_s=inf => GN=G).
    chi_inf: boundary shift of the potential (Durakovic's chi_inf<0 => RAR peak).
      We implement it as a shift in the deep-IR potential normalization: the
      physically meaningful free knob is the value of Phi (or equiv. the
      integration constant of P_Phi) -- we scan an additive shift in the
      *inner* potential to probe the chi_inf<0 enhancement branch.
    Returns dict with r grid, Phi, Phi', P_Phi, and M_AeST(<r) = -r^2 Phi'/G.
    """
    GN = G if GN is None else GN
    mu2 = (1.0/inv_mu)**2

    # inner boundary: at small r the baryons dominate, AeST -> MOND/Newton.
    # Start from a small r where enclosed baryon mass sets P_Phi via deep-MOND.
    # In deep MOND, Phi' = sqrt(G Mbar a0)/r => x = Phi'/a0, P_Phi = r^2 M(x) Phi'.
    r0 = r_in
    Mb0 = Mbar_enc(r0)
    gN0 = GN*Mb0/r0**2
    # MOND-simple starting accel (inner BC, where mu^2 term is negligible)
    g0  = gN0*(0.5 + np.sqrt(0.25 + a0/gN0))
    Phip0 = g0                     # |Phi'| = g
    x0 = Phip0/a0
    PPhi0 = r0**2 * Mfun(x0) * Phip0
    Phi0  = -g0*r0 + chi_inf*np.sqrt(GN*Mbar_enc(r_out)*a0)  # IR shift knob

    def rhs(r, y):
        Phi, PPhi = y
        Phip = invert_Phiprime(PPhi, r)
        dPhi = Phip
        # canonical-momentum evolution: dP_Phi/dr = -mu^2 r^2 Phi + 4 pi GN r^2 rho_b
        dPPhi = -mu2*r**2*Phi + 4.0*np.pi*GN*r**2*rho_b(r)
        return [dPhi, dPPhi]

    rgrid = np.logspace(np.log10(r0), np.log10(r_out), 2400)
    rgrid[0] = r0; rgrid[-1] = r_out
    sol = solve_ivp(rhs, [r0, r_out], [Phi0, PPhi0], t_eval=rgrid,
                    method='LSODA', rtol=1e-7, atol=1e-30, max_step=20*kpc)
    if not sol.success:
        return None
    r = sol.t
    Phi = sol.y[0]; PPhi = sol.y[1]
    Phip = np.array([invert_Phiprime(PPhi[i], r[i]) for i in range(len(r))])
    M_aest = -r**2*Phip/G          # apparent total mass (Eq.3.48)
    return dict(r=r, Phi=Phi, Phip=Phip, PPhi=PPhi, M_aest=M_aest)

def enc_at(res, R):
    if res is None: return np.nan
    i = np.searchsorted(res['r'], R)
    i = min(max(i,1), len(res['r'])-1)
    return res['M_aest'][i]

# ================================================================
#  RUN
# ================================================================
if __name__ == "__main__":
    print("="*72)
    print("ROUTE B: FULL nonlinear AeST Y-Q core enhancement vs the eRASS1/CLASH target")
    print("a0 = %.3e m/s^2 (framework, NOT derived)"%a0)
    print("="*72)

    rho_b, Mbar_enc = make_cluster()
    R_core = 420.0*kpc
    Mbar_core = Mbar_enc(R_core)
    print("\nCluster (M500=1e15, fgas=0.13, M_BCG=1e12):")
    print("  M_bar(<420 kpc)   = %.3e Msun"%(Mbar_core/Msun))
    print("  M_bar(<1.4 Mpc)   = %.3e Msun"%(Mbar_enc(1.4*Mpc)/Msun))

    # --- the TARGET (banked) ---
    M_target_core = 2.30e14*Msun     # eRASS1-X-ray / CLASH-lensing core (banked)
    print("\nTARGET  M_total(<420 kpc) = %.3e Msun (eRASS1/CLASH core)"%(M_target_core/Msun))

    # --- naive MOND phantom proxy (the banked ~4.4x undershoot) ---
    M_mond_core = mond_total_mass(Mbar_enc, R_core)
    print("\nNaive MOND phantom proxy:")
    print("  M_MOND(<420 kpc)  = %.3e Msun   undershoot x%.2f"%(
        M_mond_core/Msun, M_target_core/M_mond_core))

    # --- FULL AeST scan over screening length 1/mu and boundary shift chi_inf ---
    print("\n" + "-"*72)
    print("FULL AeST single-field solution, scan {1/mu, chi_inf}:")
    print("-"*72)
    inv_mus = [0.3*Mpc, 1.0*Mpc, 3.0*Mpc, 10.0*Mpc, 30.0*Mpc]
    chis    = [0.0, -10.0, -20.0]
    print("%-12s %-10s %14s %10s %10s"%(
        "1/mu[Mpc]","chi_inf","M_AeST(<420kpc)","x_under","vs_MOND"))
    best = None
    for inv_mu in inv_mus:
        for chi in chis:
            res = solve_aest(rho_b, Mbar_enc, inv_mu, chi_inf=chi)
            Mc  = enc_at(res, R_core)
            if not np.isfinite(Mc) or Mc<=0:
                print("%-12.2f %-10.0f %14s"%(inv_mu/Mpc, chi, "  (fail)"))
                continue
            xund = M_target_core/Mc
            vsmond = Mc/M_mond_core
            print("%-12.2f %-10.0f %14.3e %10.2f %10.2f"%(
                inv_mu/Mpc, chi, Mc/Msun, xund, vsmond))
            if best is None or Mc>best[0]:
                best = (Mc, inv_mu, chi)
    if best:
        print("\nBEST core mass: M_AeST=%.3e Msun at 1/mu=%.2f Mpc, chi_inf=%.0f"%(
            best[0]/Msun, best[1]/Mpc, best[2]))
        print("  => core undershoot x%.2f  (target/best)"%(M_target_core/best[0]))
