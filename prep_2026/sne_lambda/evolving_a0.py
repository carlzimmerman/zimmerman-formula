#!/usr/bin/env python3
"""
Evolving-a0 SNe test (Carl's framework): fit Pantheon+ with constant-Lambda vs
CPL evolving dark energy (w0,wa), then map ANY dark-energy history into the
framework's a0(z) = a0(0)*sqrt(rho_DE(z)/rho_DE(0)) and check:
  Q1: does evolving w fit the SNe as well/better than constant-Lambda?
  Q2: where does a0(0) land, and is a0(z=3)/a0(0) in the framework's 0.6-0.75?
Both H0 (67.4 Planck / 73.0 SH0ES). SPARC-measured a0 = 1.181e-10 (Lambda-blind, GLS gas).
CPL rho_DE(z)/rho_DE0 = (1+z)^{3(1+w0+wa)} exp(-3 wa z/(1+z)).
"""
import numpy as np
from scipy import optimize

c_kms, c_ms, G, MPC = 2.99792458e5, 2.99792458e8, 6.67430e-11, 3.0856776e22
A0_MEAS, A0_MEAS_ERR = 1.181e-10, 1.90e-11          # SPARC GLS gas-dom, Lambda-blind
A0_CANON, A0_ALT     = 9.355e-11, 1.1305e-10

d = np.genfromtxt("pantheonplus_full.dat", names=True, dtype=None, encoding=None)
m = (d["IS_CALIBRATOR"] == 0) & (d["zHD"] > 0.01)
z, mb, dmb = d["zHD"][m], d["m_b_corr"][m], d["m_b_corr_err_DIAG"][m]
N = len(z)
zg = np.linspace(0, z.max()*1.02, 3000)

def ode(zz, w0, wa):                                 # rho_DE(z)/rho_DE(0), CPL
    return (1+zz)**(3*(1+w0+wa)) * np.exp(-3*wa*zz/(1+zz))
def Ez(zz, Om, w0, wa):
    return np.sqrt(Om*(1+zz)**3 + (1-Om)*ode(zz, w0, wa))
def shape(Om, w0, wa):                               # 5 log10[(1+z) * dimensionless comoving D]
    inv = 1.0/Ez(zg, Om, w0, wa)
    integ = np.concatenate([[0], np.cumsum(0.5*(inv[1:]+inv[:-1])*np.diff(zg))])
    return 5*np.log10((1+z)*np.interp(z, zg, integ))
def chi2(Om, w0, wa):                                # marginalized over the M_B/H0 offset
    if not (0 < Om < 1): return 1e12
    dd = mb - shape(Om, w0, wa); w = 1/dmb**2
    return np.sum(dd*dd*w) - np.sum(dd*w)**2/np.sum(w)

# ---- Q1: fits ----
rL = optimize.minimize(lambda p: chi2(p[0], -1., 0.), [0.33], method="Nelder-Mead")
OmL = rL.x[0]; chiL = rL.fun
rW = optimize.minimize(lambda p: chi2(p[0], p[1], p[2]), [0.33, -0.9, -0.3],
                       method="Nelder-Mead", options=dict(xatol=1e-4, fatol=1e-4, maxiter=4000))
OmW, w0W, waW = rW.x; chiW = rW.fun

print(f"Pantheon+ SNe-only fit  (N={N}, marginalized offset, diagonal errors)")
print(f"  constant-Lambda (w=-1):  Om={OmL:.3f}          chi2={chiL:.1f}")
print(f"  CPL evolving (w0,wa):    Om={OmW:.3f}  w0={w0W:+.3f}  wa={waW:+.3f}  chi2={chiW:.1f}")
print(f"  Q1  Delta-chi2 (LCDM - evolving) = {chiL-chiW:+.2f}  over 2 extra params")
print(f"      => SNe alone {'mildly prefer evolving' if chiL-chiW>2 else 'do NOT significantly prefer evolving (consistent with constant-Lambda)'}")

# ---- Q2: framework a0(z) mapping for representative dark-energy histories ----
def a0_ratio(zz, w0, wa): return np.sqrt(ode(zz, w0, wa))     # a0(z)/a0(0)
def a0_present(OmDE0, H0):                                    # a0(0) from Omega_DE(0), H0[km/s/Mpc]
    H0si = H0*1e3/MPC; rho_L = OmDE0*3*H0si**2/(8*np.pi*G)
    return (c_ms/2)*np.sqrt(G*rho_L)

cosmos = [("constant-Lambda (w=-1)", -1.0, 0.0),
          ("SNe-only best CPL",       w0W,  waW),
          ("DESI-DR1 x Pantheon+",   -0.827, -0.75),
          ("DESI-DR2-like",          -0.75, -0.90)]
print("\nQ2  framework a0(z)/a0(0) = sqrt(rho_DE(z)/rho_DE0)   [target decline a0(3)/a0(0) ~ 0.60-0.75]")
for name, w0, wa in cosmos:
    r3 = a0_ratio(3.0, w0, wa)
    tag = "IN 0.6-0.75" if 0.60 <= r3 <= 0.75 else ("rises (>1)" if r3 > 1 else "outside")
    print(f"  {name:24s} (w0={w0:+.3f},wa={wa:+.2f}):  a0(3)/a0(0)={r3:.3f}  [{tag}]")

print("\nPresent-day a0(0) implied by the SNe Omega_DE(0), vs SPARC-measured a0:")
for label, Om in [("LCDM fit  Om="+f"{OmL:.3f}", OmL), ("CPL fit  Om="+f"{OmW:.3f}", OmW)]:
    for H0 in (67.4, 73.0):
        a0p = a0_present(1-Om, H0)
        print(f"  {label:22s} H0={H0}:  a0(0)={a0p:.3e}   ratio a0_meas/a0_SNe={A0_MEAS/a0p:.3f}"
              f"  (sigma={abs(np.log(A0_MEAS/a0p))/ (2*A0_MEAS_ERR/A0_MEAS):.2f})")
print(f"\n  SPARC-measured a0 = {A0_MEAS:.3e} +/- {A0_MEAS_ERR:.2e} (16%); canonical {A0_CANON:.3e}, alt {A0_ALT:.3e}")
print("EXIT 0")
