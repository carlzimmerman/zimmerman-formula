#!/usr/bin/env python3
"""
Spherical-collapse-with-AeST: SETUP / SCAFFOLD (not the full production solve).

Encodes the formalism derived in AEST_SPHERICAL_COLLAPSE_SETUP.md so the follow-up
workflow has a concrete, validated starting point. Implements:
  (A) the static AeST field solver pieces (DS24 Eq 2.40 / M(x)) -- the per-step solve,
  (B) the onion-shell MOND collapse closed-form limits (MRH08) used to VALIDATE mu=0,
  (C) the phase diagnostic stubs (oscillation phase theta, chi_infty, eta(R500)).

QUARANTINE: a0=9.36e-11 is an INPUT (= c^2 sqrt(Lambda/32pi)); never derived here.
MEMORY rule: use the framework's OWN dS-Unruh interpolation g=sqrt(gN^2+gN a0) for the
algebraic check, a0=9.36e-11 baseline. Both-ways: this scaffold takes NO stance on
whether the phase pins; it sets up the machinery that will answer it.

Refs: Skordis-Zlosnik 2021 (2007.00082); Verwayen-Skordis-Boehm 2024 (2304.05134);
Durakovic-Skordis 2024 (2312.00889); Malekjani-Rahvar-Haghi 2008 (0811.1833).
"""
import numpy as np

# ----------------------------------------------------------------------------- constants
G    = 6.674e-11           # SI
c    = 2.998e8
Msun = 1.989e30
Mpc  = 3.086e22
kpc  = Mpc/1e3
a0   = 9.36e-11            # FRAMEWORK INPUT (quarantined), c^2 sqrt(Lambda/32pi)
mu_inv_Mpc = 1.0           # CMB / flat-RC pinned Helmholtz scale; robustness band [0.5,2]

# ============================================================ (A) AeST static field pieces
def M_interp(x):
    """DS24 Eq 2.39 MOND interpolation (totally-screened, lambda_s->inf, beta0=0).
       x = |Phi'|/a0.  M->x (small x, MOND), M->1 (large x, Newton)."""
    s = np.sqrt(1.0 + 4.0*x)
    return (s - 1.0)/(s + 1.0)

def nu_dsunruh(gN):
    """Framework's OWN dS-Unruh algebraic interpolation: g = sqrt(gN^2 + gN a0).
       Used for the mu=0 ALGEBRAIC validation only; the field solve uses M(x)+mu^2 term."""
    return np.sqrt(gN**2 + gN*a0)

def aest_static_residual(Phi, r, rho_b, mu_tilde):
    """Residual of DS24 Eq 2.40 (modified Helmholtz), spherical:
         (1/r^2) d/dr[ r^2 M(x) Phi' ] + mu_tilde^2 Phi - 4 pi G rho_b = 0,  x=|Phi'|/a0.
       Phi,r,rho_b arrays on a radial grid. Returns the residual array.
       NOTE: production solve should use the DS24/VSB24 Hamiltonian (Phi,P_Phi) recast to
       avoid the |Phi'|=0 oscillation singularity -- this 2nd-order form is the reference."""
    dr   = np.gradient(r)
    Phip = np.gradient(Phi, r)
    x    = np.abs(Phip)/a0
    flux = r**2 * M_interp(x) * Phip
    div  = np.gradient(flux, r)/r**2
    return div + mu_tilde**2 * Phi - 4.0*np.pi*G*rho_b

def mu_tilde(mu_inv_Mpc=mu_inv_Mpc, beta0=0.0):
    """mu_tilde^2 = (1+beta0) mu^2.  mu set by SZ2021 background: mu^2=(2K2/(2-KB))Q0^2,
       here parameterized by the CMB-pinned length mu^-1 (Mpc)."""
    mu = 1.0/(mu_inv_Mpc*Mpc)
    return np.sqrt(1.0+beta0)*mu

# ===================================================== (B) onion-shell MOND collapse limits
def r_crit(a, H0=70e3/Mpc, Om_b=0.05, Om_aest=0.25, Om_L=0.69):
    """MRH08 Eq 9 critical (MOND-entry) radius vs scale factor a.
       AeST: Om_aest (dust) replaces CDM in the background; here folded into the
       matter term (Om_b+Om_aest) a^-3."""
    Om_m = Om_b + Om_aest
    return 2.0*a0 / (H0**2 * abs(Om_m*a**-3 - 2.0*Om_L))

def deep_mond_turnaround(r_ent, v_ent, M_i):
    """MRH08 Eq 11: r_max = r_ent exp(alpha), alpha = v_ent^2/(2 sqrt(G M a0))."""
    alpha = v_ent**2 / (2.0*np.sqrt(G*M_i*a0))
    return r_ent*np.exp(alpha), alpha

def deep_mond_virial(r_ent, v_ent, M_i):
    """MRH08 Eq 14 (MOND branch): r_vir = r_ent exp(alpha - 1/2).  Valid when alpha>1/2."""
    _, alpha = deep_mond_turnaround(r_ent, v_ent, M_i)
    return r_ent*np.exp(alpha - 0.5), alpha

def shell_eom_mond(r, M_i):
    """Deep-MOND per-shell acceleration (MRH08 Eq 10): r'' = -sqrt(G M a0)/r.
       Production AeST solve replaces this with r'' = -g_AeST(r,t) from aest_static_residual
       (i.e. includes the +mu^2 phantom term -- the piece carrying the oscillation phase)."""
    return -np.sqrt(G*M_i*a0)/r

# ============================================================ (C) phase diagnostic stubs
def fit_oscillation_phase(r, Phi, mu_tilde, r_window):
    """Fit Phi(r) ~ A cos(mu_tilde r + theta)/r over r_window=(r_lo,r_hi) on the
       oscillatory branch.  Returns (A, theta).  theta = the FREE phase the static BVP
       leaves open; PINNED <=> theta(t)->theta* converges, IC-independent.  STUB: linear
       least-squares on [cos, sin] basis."""
    sel = (r>=r_window[0]) & (r<=r_window[1])
    rr, y = r[sel], Phi[sel]*r[sel]                      # y = A cos(mu r + theta)
    Bcos, Bsin = np.cos(mu_tilde*rr), np.sin(mu_tilde*rr)
    Cc, Cs = np.linalg.lstsq(np.vstack([Bcos, Bsin]).T, y, rcond=None)[0]
    A = np.hypot(Cc, Cs); theta = np.arctan2(-Cs, Cc)
    return A, theta

def eta_R500(M_total_aest, M_baryon):
    """Phantom-mass boost (DS24 Eq 3.48-3.50): eta = M_total^AeST/M_baryon - 1 at R500.
       eta>0 boost (closes clusters), eta<0 deficit.  Static result: eta in [-3.12,+3.97]
       across phases; natural untuned gives eta=-1.54."""
    return M_total_aest/M_baryon - 1.0

# ===================================================================== VALIDATION on import
if __name__ == "__main__":
    print("=== AeST spherical-collapse SETUP scaffold: self-validation ===")
    print(f"a0 (INPUT, quarantined) = {a0:.3e} m/s^2")

    # M(x) limits
    assert abs(M_interp(1e-3)-1e-3) < 1e-5,        "M(x)->x small-x FAIL"
    assert abs(M_interp(1e6)-1.0)   < 1e-3,        "M(x)->1 large-x FAIL"
    print("M(x) limits OK:  M(0.001)=%.5f (~MOND),  M(1e6)=%.5f (~Newton)" %
          (M_interp(1e-3), M_interp(1e6)))

    # dS-Unruh deep-MOND limit
    gN=1e-12
    assert abs(nu_dsunruh(gN) - np.sqrt(gN*a0)) < 1e-2*np.sqrt(gN*a0), "dS-Unruh deep limit FAIL"
    print("dS-Unruh deep-MOND g=sqrt(gN a0) OK (framework ny, not McGaugh)")

    # cluster sits in mu-regime, galaxy protected (geometric (mu r)^2)
    mt = mu_tilde()
    print("(mu r)^2:  galaxy 10kpc = %.2e (protected),  cluster 1.5Mpc = %.3f (mu-regime)"
          % ((mt*10*kpc)**2, (mt*1.5*Mpc)**2))
    assert (mt*10*kpc)**2 < 1e-3 < (mt*1.5*Mpc)**2,  "geometric galaxy/cluster split FAIL"

    # MOND collapse closed forms (MRH08)
    M_i=1e14*Msun; r_ent=0.3*Mpc; v_ent=200e3
    rmax,al = deep_mond_turnaround(r_ent, v_ent, M_i)
    rvir,_  = deep_mond_virial(r_ent, v_ent, M_i)
    assert abs(rvir/rmax - np.exp(-0.5)) < 1e-12,    "r_vir/r_max=exp(-1/2) FAIL"
    print("MOND collapse OK:  alpha=%.3f, r_max=%.3f Mpc, r_vir=%.3f Mpc, r_vir/r_max=%.4f"
          % (al, rmax/Mpc, rvir/Mpc, rvir/rmax))

    # rM, rC: confirm cluster R500 is beyond rC (oscillatory/boundary-sensitive)
    rM = np.sqrt(G*M_i/a0); rC = (rM/mt**2)**(1/3.)
    print("rM=%.3f Mpc, rC=%.3f Mpc  -> R500~1-2 Mpc is BEYOND rC => boundary-phase-sensitive"
          % (rM/Mpc, rC/Mpc))

    # phase-fit round trip
    r = np.linspace(0.5*Mpc, 4*Mpc, 2000)
    theta_true = 0.7
    Phi = 3.0*np.cos(mt*r + theta_true)/r
    A, th = fit_oscillation_phase(r, Phi, mt, (1.0*Mpc, 3.5*Mpc))
    assert abs(th - theta_true) < 1e-2,              "phase fit round-trip FAIL"
    print("phase diagnostic OK:  recovered theta=%.4f (true %.4f)" % (th, theta_true))

    print("\nALL VALIDATION CHECKS PASSED.  Scaffold ready for the production collapse solve.")
    print("Next: (3a) quasistatic-per-step field solve w/ cosmological-chi outer BC;")
    print("      (3b) fully time-dependent field; (C2) IC ensemble = the pin/no-pin verdict.")
