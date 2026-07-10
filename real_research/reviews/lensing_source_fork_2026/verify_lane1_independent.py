#!/usr/bin/env python3
"""Independent re-derivation of the lane-1 (dS-Unruh bath energetics) decisive ratio.

Written from scratch: scalar arithmetic, exact analytic rho_eff for a point
source (no numerical gradient), both footings, plus the required-temperature
inversion and a maximal-generosity stack (g* species, g_obs in T, photon+graviton).
"""
import math

G, c = 6.674e-11, 2.998e8
hbar, kB = 1.0546e-34, 1.3807e-23
sigma_SB = 5.670374e-8            # W m^-2 K^-4
a_rad = 4*sigma_SB/c              # J m^-3 K^-4  (independent derivation)
Msun, kpc = 1.989e30, 3.0857e19
Z = 5.79
rho_L = 6.0e-27
M = 1.0e11*Msun

def analytic_rho_eff(r, a0):
    """rho_eff = (1/4 pi r^2) d/dr [ M (nu(y)-1) ], exact derivative for point mass.
    y = GM/(a0 r^2); nu = sqrt(1+1/y); d(nu)/dr via chain rule."""
    y = G*M/(a0*r*r)
    nu = math.sqrt(1.0 + 1.0/y)
    dy_dr = -2.0*G*M/(a0*r**3)
    dnu_dy = (-1.0/(y*y))/(2.0*nu)
    dMeff_dr = M*dnu_dy*dy_dr
    return dMeff_dr/(4.0*math.pi*r*r), y, nu

print(f"a_rad independent = {a_rad:.4e} (script used 7.5657e-16)")
for label, a0 in [("canonical", 9.36e-11), ("alt", 1.13e-10)]:
    cH = Z*a0
    Tc = hbar/(2*math.pi*kB*c)
    Tfloor = Tc*cH
    print(f"\n--- {label}: a0={a0:.3e}, cH={cH:.3e}, T_floor={Tfloor:.3e} K ---")
    for rk in (10, 100):
        r = rk*kpc
        rho_eff, y, nu_v = analytic_rho_eff(r, a0)
        g_bar = G*M/r/r
        g_obs = math.sqrt(g_bar*g_bar + g_bar*a0)
        T = Tc*math.sqrt(g_obs**2 + cH**2)
        rho_bath = a_rad*T**4/c**2
        rho_exc = a_rad*(T**4 - Tfloor**4)/c**2
        orders_full = math.log10(rho_eff/rho_bath)
        orders_exc = math.log10(rho_eff/rho_exc)
        # generosity stack: g* = 106.75 relativistic species (SM), x2 gravitons
        rho_max = rho_bath*106.75*2
        orders_max = math.log10(rho_eff/rho_max)
        # required temperature to match rho_eff via SB
        T_req = (rho_eff*c**2/a_rad)**0.25
        print(f"  r={rk:>3} kpc: y={y:.3f}  rho_eff={rho_eff:.3e}  "
              f"rho_bath={rho_bath:.3e}  short(full)={orders_full:.1f} orders  "
              f"short(excess)={orders_exc:.1f}  short(g*-stacked)={orders_max:.1f}")
        print(f"             T_bath={T:.3e} K, T_required={T_req:.3e} K, "
              f"ratio={T_req/T:.2e};  conc needed vs rho_L: {rho_eff/rho_L:.2e}")
print("\nexit 0")
