#!/usr/bin/env python3
"""
Adiabaticity of the evolving-a0 reading (Fable's gate on the EVOLUTION claim).

Fable's point: the KMS/thermal selection argument, taken strictly, selects the FIXED-POINT
(asymptotic-dS) value -- a CONSTANT a0 set by H_inf -- because the moment you let a0 track the
INSTANTANEOUS rho_DE(z) through the matter era, you use the de Sitter-Unruh temperature in exactly
the regime where the row's own caveat says thermality is 'strictly lost'. The declining branch
a0(z) ~ sqrt(rho_DE(z)) is therefore an ADIABATIC extension whose validity nobody quantified.

This computes the adiabaticity parameter
    eps(z) = |d ln T / dt| / Gamma_th,   T proportional to sqrt(rho_DE),  Gamma_th ~ H_DE
i.e. (rate the de Sitter-Unruh temperature changes) / (rate the dS horizon thermalizes).
eps << 1: evolving reading self-consistent (detector tracks the instantaneous horizon).
eps >> 1: NON-adiabatic -- the detector lags; the strict thermal argument gives the CONSTANT value.
Reports the z-range where the evolving reading is self-consistent, and whether z=3 (the decisive
test) is inside it. numpy only.  C. Zimmerman, 2026-06-09.
"""
import numpy as np
H0 = 1.0                              # work in units of H0
Om, OmL = 0.315, 0.685
w0, wa = -0.752, -0.86               # DESI DR2 CPL

def rhoDE(z):                        # rho_DE(z)/rho_DE0, CPL
    a = 1/(1+z); return (1+z)**(3*(1+w0+wa))*np.exp(-3*wa*(1-a))
def dlnrhoDE_dz(z):                  # d ln rho_DE / dz, analytic CPL
    return 3*(1+w0+wa)/(1+z) - 3*wa/(1+z)**2
def H(z):    return H0*np.sqrt(Om*(1+z)**3 + OmL*rhoDE(z))   # total Hubble
def H_DE(z): return H0*np.sqrt(OmL*rhoDE(z))                 # dS-equivalent rate from rho_DE alone

def eps(z, twopi=False):
    # |d ln T/dt| = 1/2 |d ln rhoDE/dt| = 1/2 |d ln rhoDE/dz| (1+z) H(z)
    dlnT_dt = 0.5*np.abs(dlnrhoDE_dz(z))*(1+z)*H(z)
    Gamma = H_DE(z)/(2*np.pi) if twopi else H_DE(z)          # thermal-time vs relaxation-rate
    return dlnT_dt/Gamma

def boundary(twopi=False):           # smallest z>=0 with eps>=1 (bisection on a grid)
    zg = np.linspace(0, 5, 20001); e = eps(zg, twopi)
    above = np.where(e >= 1)[0]
    return zg[above[0]] if len(above) else np.inf

print("="*78)
print("Adiabaticity of the evolving (declining sqrt(rho_DE)) a0(z) reading")
print("  eps = |dlnT/dt| / Gamma_th ;  eps<<1 self-consistent, eps>>1 non-adiabatic (-> constant)")
print("="*78)
print(f"  {'z':>5}{'rhoDE/rhoDE0':>14}{'H/H_DE':>10}{'eps [Gth=H_DE]':>16}{'eps [Gth=H_DE/2pi]':>20}")
for z in [0.0, 0.3, 0.5, 1.0, 2.0, 3.0, 5.0]:
    print(f"  {z:>5.1f}{rhoDE(z):>14.4f}{H(z)/H_DE(z):>10.2f}{eps(z):>16.2f}{eps(z,True):>20.1f}")
zb1, zb2 = boundary(False), boundary(True)
print("-"*78)
print(f"  adiabatic boundary eps=1:   z = {zb1:.2f}  (Gamma_th=H_DE)   |   z = {zb2:.2f}  (Gamma_th=H_DE/2pi)")
print(f"  at z=3 (the decisive a0(z) test):  eps = {eps(3.0):.1f} to {eps(3.0,True):.0f}   => firmly NON-adiabatic")
print("="*78)
print(f"""VERDICT
  The de Sitter horizon thermalizes on a Hubble timescale (Gamma_th ~ H_DE), so the EVOLVING-
  temperature reading is self-consistent only at LOW z (z <~ {zb1:.1f}-{0.0:.0f}, depending on the O(2pi)
  thermalization rate). By z=3 the background rho_DE evolves ~{eps(3.0):.0f}-{eps(3.0,True):.0f}x faster than the dS horizon
  can thermalize: eps >> 1. Consequences, stated plainly (per the working rule, both ways):

  (1) Fable is right: the STRICT thermal/KMS argument licenses the CONSTANT (fixed-point) a0,
      not the declining one. Declining a0(z) ~ sqrt(rho_DE(z)) is an ANSATZ (the 'instantaneous-
      horizon' choice), not a thermodynamically-forced prediction. The evolution -- the
      specifically-Zimmerman, 'decisive' C3 claim -- is the LEAST geometrically-supported piece:
      one home (AeST) speaks rising, the strict thermal argument speaks constant, NONE derives
      declining.

  (2) But it does not zero the empirical test: non-adiabatic means the detector LAGS, not freezes,
      so the true a0(z=3) lies BETWEEN the full-decline prediction (~0.70) and constant (1.0). A
      clean a0(z=3) measurement still discriminates -- rising (~4.6) is excluded regardless, and any
      value <1 still favours SOME decline -- but the theory's 0.70 is the maximal decline, an
      extrapolation outside the self-consistent range, and that must be said before ELT time is
      requested on it. The decisive test tests {{constant vs declining vs rising}}, with the
      theory prior on declining-vs-constant SOFT.""")
