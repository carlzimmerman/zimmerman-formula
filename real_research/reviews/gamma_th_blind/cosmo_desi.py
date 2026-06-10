#!/usr/bin/env python3
"""
Shared cosmology module: DESI DR2 CPL dark energy.
  w(a) = w0 + wa(1-a),   w0 = -0.752, wa = -0.86,  Om = 0.315, OL = 0.685 (flat).
rho_DE(a)/rho_DE0 = exp( 3 * int_a^1 (1+w(a'))/a' da' )
                  = a^{-3(1+w0+wa)} * exp(-3 wa (1-a))    [standard CPL closed form].
H(z) = H0 sqrt( Om (1+z)^3 + OL * f_DE(z) ),  f_DE = rho_DE(z)/rho_DE0.

We work in units H0 = 1 for timescales (then restore where a number is needed). Cosmic
time t in units of 1/H0.  H0 = 100 h km/s/Mpc; use h=0.674 -> 1/H0 = 14.5 Gyr if a
physical number is wanted, but the gate ratios are H0-independent / dimensionless.
"""
import numpy as np
from scipy.integrate import quad, solve_ivp

w0, wa = -0.752, -0.86
Om, OL = 0.315, 0.685
H0 = 1.0  # work in H0 units

def f_DE(z):
    """rho_DE(z)/rho_DE(0) for CPL (closed form)."""
    a = 1.0/(1.0+z)
    return a**(-3.0*(1.0+w0+wa)) * np.exp(-3.0*wa*(1.0-a))

def rho_DE(z):
    return OL * f_DE(z)   # in units of rho_crit0

def rho_m(z):
    return Om*(1.0+z)**3

def E(z):
    """H(z)/H0."""
    return np.sqrt(Om*(1.0+z)**3 + OL*f_DE(z))

def H_of_z(z):
    return H0*E(z)

# --- the dark-energy-only Hubble-like rate used by the framework's a0(z) ---
# a0 ~ sqrt(rho_DE) => define H_DE(z) = H0 sqrt(OL f_DE(z))  (the "DE Hubble rate").
def H_DE(z):
    return H0*np.sqrt(OL*f_DE(z))

# --- temperature ansatz of the framework: T(z) ∝ sqrt(rho_DE(z)) ∝ H_DE(z) ---
def T_ansatz(z):
    """T(z) proportional to sqrt(rho_DE(z)); normalize T(0)=1 (units arbitrary)."""
    return np.sqrt(f_DE(z))   # sqrt(rho_DE(z)/rho_DE0); equals H_DE(z)/H_DE(0)

# d ln T / dt  (t in 1/H0 units).  dt = -da/(a H) ; d/dt = a H d/da... easier via z:
#   dz/dt = -(1+z) H(z).   d ln T/dt = (d ln T/dz)(dz/dt).
def dlnT_dt(z, dz=1e-5):
    lnT_p = np.log(T_ansatz(z+dz)); lnT_m = np.log(T_ansatz(z-dz))
    dlnT_dz = (lnT_p - lnT_m)/(2*dz)
    dzdt = -(1.0+z)*H_of_z(z)
    return dlnT_dz*dzdt   # in units of H0

def abs_dlnT_dt(z):
    return abs(dlnT_dt(z))

# analytic d ln T/dt:  ln T = 0.5 ln f_DE.  d ln f_DE/d ln a = 3(1+w(a)).
#   => d ln T/d ln a = 1.5 (1+w(a)).   d ln a/dt = H.
#   => d ln T/dt = 1.5 (1+w(a)) H(z).
def dlnT_dt_analytic(z):
    a = 1.0/(1.0+z)
    w = w0 + wa*(1.0-a)
    return 1.5*(1.0+w)*H_of_z(z)   # signed; positive when w>-1 and ... (a increasing)
# NOTE sign: as t increases, a increases, rho_DE for w>-1 DECREASES => T decreases =>
# d ln T/dt < 0. Let's check: d ln T/d ln a = 1.5(1+w); for w0=-0.752 (>-1) this is +,
# and d ln a/dt = +H >0, so d ln T/dt >0 ?? That says T increasing. But rho_DE for w>-1
# decreases with a. Resolve: rho_DE ∝ exp(3∫(1+w)/a da)... d ln rho/d ln a = -3(1+w)!
# (the EOS continuity eqn: dρ/dt = -3H(1+w)ρ => d ln ρ/d ln a = -3(1+w)). Fix sign:
def dlnT_dt_analytic(z):
    a = 1.0/(1.0+z)
    w = w0 + wa*(1.0-a)
    dlnT_dlna = -1.5*(1.0+w)        # since d ln rho_DE/d ln a = -3(1+w), T=sqrt(rho)
    return dlnT_dlna * H_of_z(z)    # d ln a/dt = H
def abs_dlnT_dt_analytic(z):
    return abs(dlnT_dt_analytic(z))

if __name__ == "__main__":
    print("DESI CPL cosmology checks  (w0=%.3f wa=%.3f Om=%.3f)"%(w0,wa,Om))
    print(f"{'z':>4} {'f_DE':>10} {'E(z)':>9} {'H_DE/H0':>9} {'1+w':>8} "
          f"{'|dlnT/dt|_num':>14} {'|dlnT/dt|_an':>13}")
    for z in [0,0.4,1,2,3,5,10]:
        a = 1/(1+z); w = w0+wa*(1-a)
        print(f"{z:4} {f_DE(z):10.5f} {E(z):9.4f} {H_DE(z)/H0:9.4f} {1+w:8.4f} "
              f"{abs_dlnT_dt(z):14.6f} {abs_dlnT_dt_analytic(z):13.6f}")
    # sanity: rho_DE(3)/rho_DE(0) and its sqrt (the zero-lag a0(3)/a0(0)):
    print("\nrho_DE(3)/rho_DE(0) =", f_DE(3.0))
    print("sqrt(rho_DE(3)/rho_DE(0)) = zero-lag a0(3)/a0(0) =", np.sqrt(f_DE(3.0)))
