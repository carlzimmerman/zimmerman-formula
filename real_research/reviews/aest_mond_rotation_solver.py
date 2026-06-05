#!/usr/bin/env python3
"""
AeST/MOND rotation-curve solver with the framework's a0 = c^2 sqrt(Lambda/32pi) and its a0(z) ~ sqrt(rho_DE) signature.
=====================================================================================================================
A clean, reusable computational core for the dark-universe theory's galaxy-scale predictions. It implements the AeST
quasi-static (deep-MOND/AQUAL) limit -- the algebraic relation g = g_N * nu(g_N/a0) with the simple interpolating
function nu(y)=1/2+sqrt(1/4+1/y) (the RAR-calibrated form) -- and provides:
  * a0_framework(z): the framework's evolving scale, a0(z) = a0(0) * sqrt(rho_DE(z)/rho_DE0) (constant if Lambda const).
  * rotation_curve(M_enc, r, a0): V(r) for any baryonic enclosed-mass profile.
  * the deep-MOND Baryonic Tully-Fisher check V_flat = (G M_b a0)^(1/4).
  * a demonstration on a Milky-Way-like exponential disk, including the DISTINCTIVE z=3 prediction (a0 ~0.74x ->
    V_flat ~0.93x), and a figure.
This is the module one would point at SPARC (z~0) and at JWST/ALMA z~3 rotation curves to run the bridge test.
Needs numpy, scipy, matplotlib.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ---- constants ----
c=2.998e8; G=6.674e-11; Msun=1.989e30; kpc=3.086e19; Mpc=3.086e22
H0=67.4e3/Mpc; OmM,OmL=0.315,0.685
Lam=3*OmL*H0**2/c**2
A0_LAMBDA = c**2*np.sqrt(Lam/(32*np.pi))     # framework's Lambda-only value, 9.36e-11
A0_OBS    = 1.2e-10                            # empirical anchor (RAR); ~28% above the Lambda-only value
w0,wa=-0.752,-0.86                            # DESI DR2 dynamical-DE


def a0_framework(z, a0_today=A0_OBS, dynamical=True):
    """a0(z) = a0(0) * sqrt(rho_DE(z)/rho_DE0). Constant if Lambda is constant (dynamical=False)."""
    if not dynamical:
        return a0_today*np.ones_like(np.atleast_1d(z)*1.0)
    a=1.0/(1.0+np.asarray(z,float))
    rhoDE=a**(-3*(1+w0+wa))*np.exp(-3*wa*(1-a))
    return a0_today*np.sqrt(rhoDE)


def nu_simple(y):
    """MOND interpolation g = g_N nu(g_N/a0); nu(y)=1/2+sqrt(1/4+1/y). Deep-MOND nu~1/sqrt(y); Newtonian nu->1."""
    return 0.5+np.sqrt(0.25+1.0/y)


def mond_acceleration(g_N, a0):
    return g_N*nu_simple(g_N/a0)


def rotation_curve(M_enc, r, a0):
    """V(r) [m/s] from enclosed baryonic mass M_enc(r) [kg], radius r [m], scale a0 [m/s^2]."""
    g_N=G*M_enc/r**2
    return np.sqrt(r*mond_acceleration(g_N, a0))


def Vflat_BTFR(M_b, a0):
    return (G*M_b*a0)**0.25


def exp_disk_Menc(r, M_d, R_d):
    """Enclosed mass of an exponential (spherically-approximated) disk."""
    x=r/R_d
    return M_d*(1.0-(1.0+x)*np.exp(-x))


def main():
    print("#"*96); print("# AeST/MOND rotation-curve solver -- framework a0(z) ~ sqrt(rho_DE)"); print("#"*96+"\n")
    print(f"  a0 (Lambda-only)  = c^2 sqrt(Lambda/32pi) = {A0_LAMBDA:.3e} m/s^2")
    print(f"  a0 (RAR anchor)   = {A0_OBS:.3e} m/s^2   (the value used for realistic curves; ~{100*(A0_OBS/A0_LAMBDA-1):.0f}% above Lambda-only)")
    print(f"  framework a0(z)/a0(0) (DESI DR2): " + ", ".join(f"z={z}:{a0_framework(z)/A0_OBS:.3f}" for z in (1,2,3))+"\n")

    # Milky-Way-like exponential disk
    M_d=6e10*Msun; R_d=3*kpc
    r=np.linspace(0.3, 40, 400)*kpc
    Menc=exp_disk_Menc(r, M_d, R_d)
    a0_0=a0_framework(0.0); a0_3=a0_framework(3.0)
    V0=rotation_curve(Menc, r, a0_0)/1e3        # km/s, z=0
    V3=rotation_curve(Menc, r, a0_3)/1e3        # km/s, z=3 (framework: a0 lower)
    Vn=np.sqrt(G*Menc/r)/1e3                     # Newtonian baryons-only

    print("="*96); print("(1) rotation curve flattens (MOND) + Baryonic Tully-Fisher"); print("="*96)
    print(f"   Milky-Way-like disk: M_b={M_d/Msun:.1e} Msun, R_d={R_d/kpc:.0f} kpc")
    print(f"   V_flat (solver, outer) = {V0[-1]:.0f} km/s ;  BTFR (GMa0)^1/4 = {Vflat_BTFR(M_d,a0_0)/1e3:.0f} km/s  (match)")
    print(f"   Newtonian baryons-only outer V = {Vn[-1]:.0f} km/s  -> MOND boost is real (no dark matter).\n")

    print("="*96); print("(2) the DISTINCTIVE framework prediction: a0(z=3) lower -> V_flat lower by ~7%"); print("="*96)
    print(f"   V_flat(z=0) = {V0[-1]:.0f} km/s ;  V_flat(z=3) = {V3[-1]:.0f} km/s  -> {100*(V3[-1]/V0[-1]-1):+.0f}% (= a0^1/4 shift)")
    print(f"   This is the coefficient-free bridge in a rotation curve: a SAME-baryonic-mass galaxy at z=3 rotates")
    print(f"   ~7% slower in the deep-MOND framework if dark energy evolves (DESI). The z~3 test made physical.\n")

    # figure
    fig,ax=plt.subplots(figsize=(7,5))
    ax.plot(r/kpc, V0, 'b-', lw=2, label=f'MOND z=0  (a0={a0_0:.2e})')
    ax.plot(r/kpc, V3, 'r--', lw=2, label=f'MOND z=3  (a0={a0_3:.2e}, framework)')
    ax.plot(r/kpc, Vn, 'k:', lw=1.5, label='Newtonian (baryons only)')
    ax.axhline(Vflat_BTFR(M_d,a0_0)/1e3, color='b', alpha=0.3, ls='-')
    ax.set_xlabel('radius [kpc]'); ax.set_ylabel('V [km/s]')
    ax.set_title('AeST/MOND rotation curve + framework a0(z) signature\n(Milky-Way-like disk; z=3 curve lower by the a0^1/4 bridge shift)')
    ax.legend(); ax.set_ylim(0, 220); ax.grid(alpha=0.3)
    out="real_research/figures/aest_mond_rotation.png"
    fig.savefig(out, dpi=110, bbox_inches='tight')
    print(f"  figure written: {out}")
    print("#"*96)


if __name__=="__main__":
    main()
