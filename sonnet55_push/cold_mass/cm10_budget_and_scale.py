"""cm10: conservation budget + the step scale for the two-level retention (cm08/cm09): galaxy-scale hosts keep r_gal ~ 0.13, group/cluster hosts r_grp ~ 0.6
of their cold share. LCDM halo mass function (colossus, planck18, Tinker+08, M200m, z = 0) gives where the cold mass would sit; the two-level rule keeps
B(M_step) = r_gal f(1e9 < M < M_step) + r_grp f(M > M_step) bound in halos; the rest of the cold mass must be diffuse (conservation: Omega_c fixed).
(1) budget: bound and diffuse fractions vs LCDM's own halo-bound fraction, for M_step = 1e12 .. 1e14.
(2) scale: the step location from data (cm08/cm09: hosts of the 23 galaxy-level ETGs vs the 9 centrals; MW 1e12 at 0.14; Lovisari groups M500 >= ~1e13);
    reported as the bracket where the levels change, converted to sigma_v, T_vir and R200m.
Retentions are aperture quantities (5 Re / R500) applied to whole halos: an approximation, stated. Nothing here derives 0.13 or 0.6.
Run: python3 cm10_budget_and_scale.py | MUTATE=1 sets r_gal = r_grp = 1 (bound must equal LCDM's, check B fails)
"""
import os, sys, math, numpy as np
from colossus.cosmology import cosmology
from colossus.lss import mass_function
MUTATE = os.environ.get("MUTATE") == "1"
res = []
def check(n, ok): res.append(bool(ok)); print(("PASS  " if ok else "FAIL  ") + n)
cosmo = cosmology.setCosmology("planck18")
h = cosmo.H0 / 100; rho_m = cosmo.rho_m(0) * 1e9   # Msun h^2 / Mpc^3
lM = np.linspace(6, 16, 2001); M = 10**lM          # Msun/h
dndlnM = mass_function.massFunction(M, 0.0, mdef="200m", model="tinker08", q_out="dndlnM")
dens = M * dndlnM                                   # mass per ln M per volume
def frac(lo, hi):
    m = (M >= lo * h) & (M < hi * h); return float(np.trapz(dens[m], np.log(M[m])) / rho_m)
rg, rG = (1.0, 1.0) if MUTATE else (0.13, 0.60)
fL = frac(1e9, 1e16)
print(f"   LCDM (Tinker08, z = 0): fraction of matter in halos > 1e9 Msun = {fL:.3f}; >1e12 {frac(1e12,1e16):.3f}; >1e13 {frac(1e13,1e16):.3f}; >1e14 {frac(1e14,1e16):.3f}")
B = {}
for ls in (12.0, 12.5, 13.0, 13.5, 14.0):
    Ms = 10**ls; b = rg * frac(1e9, Ms) + rG * frac(Ms, 1e16); B[ls] = b
    print(f"   M_step = 1e{ls:.1f}: bound cold = {b:.3f} of all cold mass (LCDM {fL:.3f}); diffuse = {1-b:.3f}; bound / LCDM-bound = {b/fL:.2f}")
check("B the two-level rule binds < 90% of the cold mass LCDM halos would (MUTATE r = 1 must fail; v1 used a 1e-6 margin that the grid split defeated)", B[13.0] < 0.9 * fL)
# scale
G = 4.30091e-9   # Mpc km^2 s^-2 Msun^-1
def props(Mv):
    R = (3 * Mv / (4 * math.pi * 200 * cosmo.rho_m(0) * 1e9 * h**2))**(1 / 3)   # Mpc
    V = math.sqrt(G * Mv / R); T = 0.5 * 0.6 * 1.6726e-27 * (V * 1e3)**2 / 1.380649e-23
    return R, V, T
print("   step scale bracket from the data: highest galaxy-level host ~ Milky Way 1e12 (0.14); lowest group-level hosts: Lovisari groups M500 >= ~1e13 and the")
print("   low-sigma centrals NGC 4636/1316/5846 (group halos ~1e13). Bracket M200m ~ 1e12 .. 1e13 Msun:")
for Mv in (1e12, 3e12, 1e13):
    R, V, T = props(Mv); print(f"      M200m {Mv:.0e}: R200m {R*1e3:.0f} kpc, V200 {V:.0f} km/s, T_vir {T:.2e} K")
print("   compare: the Rees-Ostriker/Silk cooling mass ~1e12 Msun, T ~ 1e6 K (atomic cooling vs dynamical time)")
print(f"\n{sum(res)}/{len(res)} pass" + ("  (MUTATE)" if MUTATE else ""))
sys.exit(0 if all(res) else 1)
