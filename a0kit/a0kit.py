#!/usr/bin/env python3
"""
a0kit -- the de Sitter-Unruh modified-inertia acceleration-scale toolkit.

A small, dependency-light (numpy only) library implementing the formulas of the
de Sitter-Unruh MODIFIED-INERTIA framework (Zimmerman): the horizon-derived MOND
acceleration scale a0 = c H_Lambda / Z, its interpolation kernel, the a0-line
identity, the Lambda<->a0 inversion, and the redshift law a0(z) ~ sqrt(rho_DE(z)).

SCOPE / HONESTY (read this): the *value* of a0, the coefficient Z = sqrt(32pi/3), and the
sign of the inertial correction are POSITED, not derived -- this library computes the
framework's relations, it does not prove them. The interpolation nu(y)=sqrt(1+1/y) is the
functional form of Milgrom (1999, Phys. Lett. A 253, 273); the framework's distinctive
content is the cH_Lambda/Z coefficient and a modified-inertia (not modified-gravity)
completion. Both a0 footings are provided (canonical pure-dark-energy vs total-density).

References: Milgrom 1983 (ApJ 270, 365), 1999 (PLA 253, 273); framework papers on Zenodo
(concept/flagship 10.5281/zenodo.21312654 and the a0-line 10.5281/zenodo.21419735).
"""
import numpy as np

# ---- physical constants (SI) ----
C     = 2.99792458e8          # speed of light, m/s
G     = 6.67430e-11           # Newton's constant, m^3 kg^-1 s^-2
MPC   = 3.0856775814913673e22 # m
MSUN  = 1.98892e30            # kg
LAMBDA_PLANCK = 1.089e-52     # Planck 2018 cosmological constant, m^-2

Z = np.sqrt(32*np.pi/3)       # 5.78881... (POSITED coefficient)

# canonical horizon-derived a0 (pure dark energy); both footings exposed below
A0_CANONICAL = C**2*np.sqrt(LAMBDA_PLANCK/(32*np.pi))   # ~9.36e-11 m/s^2

def a0_from_lambda(Lam=LAMBDA_PLANCK):
    """Canonical horizon a0 = c^2 sqrt(Lambda / 32 pi) from the cosmological constant [1/m^2]."""
    return C**2*np.sqrt(Lam/(32*np.pi))

def a0_from_hubble(H0_kms_mpc, footing="canonical", Omega_L=0.6889):
    """a0 = c H_Lambda / Z.  footing='canonical' uses H_Lambda = H0*sqrt(Omega_L) (pure dark
    energy); footing='alt' uses the total-density rate H0 (a0 = c H0 / Z)."""
    H0 = H0_kms_mpc*1e3/MPC
    H = H0*np.sqrt(Omega_L) if footing=="canonical" else H0
    return C*H/Z

def lambda_from_a0(a0):
    """Invert to the cosmological constant: Lambda = 32 pi a0^2 / c^4  [m^-2]."""
    return 32*np.pi*a0**2/C**4

def rho_de_from_a0(a0):
    """Dark-energy mass density implied by a0:  rho_DE = 4 a0^2 / (G c^2)  [kg/m^3]."""
    return 4*a0**2/(G*C**2)

def nu(y):
    """Framework interpolation nu(y)=sqrt(1+1/y), y=g_bar/a0 (Milgrom-1999 form)."""
    return np.sqrt(1+1/y)

def g_obs(g_bar, a0=A0_CANONICAL):
    """Observed acceleration from baryonic: the a0-line, g_obs = sqrt(g_bar^2 + g_bar a0)."""
    return np.sqrt(g_bar**2 + g_bar*a0)

def a0_line(g_obs_, g_bar):
    """Invert the a0-line to read a0 off a single (g_obs, g_bar) point: a0=(g_obs^2-g_bar^2)/g_bar."""
    return (g_obs_**2 - g_bar**2)/g_bar

def rho_de_ratio(z, w0=-1.0, wa=0.0):
    """CPL rho_DE(z)/rho_DE0 = (1+z)^{3(1+w0+wa)} exp(-3 wa z/(1+z))."""
    return (1+z)**(3*(1+w0+wa))*np.exp(-3*wa*z/(1+z))

def a0_of_z(z, w0=-1.0, wa=0.0, a0_0=A0_CANONICAL):
    """Framework redshift law: a0(z) = a0(0) sqrt(rho_DE(z)/rho_DE0).  (a0(z)/a0(0) is
    Z-independent; posited adiabatic-horizon promotion of the a0~sqrt(rho_DE) relation.)"""
    return a0_0*np.sqrt(rho_de_ratio(z, w0, wa))

def btfr_vflat(M_bar_kg, a0=A0_CANONICAL):
    """Deep-MOND baryonic Tully-Fisher flat velocity: V_flat = (a0 G M_bar)^(1/4)  [m/s]."""
    return (a0*G*M_bar_kg)**0.25

def footings():
    """The two a0 footings (m/s^2): canonical (pure rho_DE) and alt (total density, c H0/Z)."""
    return {"canonical": A0_CANONICAL, "alt": a0_from_hubble(67.66, footing="alt")}

if __name__ == "__main__":
    print("a0kit self-test (de Sitter-Unruh modified-inertia toolkit)")
    a0c = a0_from_lambda(); print(f"  a0 canonical = {a0c:.4e} m/s^2  (Z={Z:.5f})")
    f = footings(); print(f"  footings: canonical {f['canonical']:.3e}, alt {f['alt']:.3e}")
    assert abs(lambda_from_a0(a0c)-LAMBDA_PLANCK)/LAMBDA_PLANCK < 1e-3, "Lambda<->a0 round-trip"
    assert abs(a0_line(g_obs(1e-11, a0c), 1e-11) - a0c)/a0c < 1e-9, "a0-line round-trip"
    print(f"  round-trips OK (Lambda<->a0, a0-line invert)")
    print(f"  a0(z=3)/a0(0) at DESI-CPL (-0.84,-0.62) = {a0_of_z(3,-0.84,-0.62)/a0c:.3f}")
    print(f"  BTFR V_flat for 1e11 Msun = {btfr_vflat(1e11*MSUN)/1e3:.1f} km/s")
    print("  EXIT 0 -- a0's VALUE + Z are POSITED, not derived; nu is Milgrom-1999's form.")
