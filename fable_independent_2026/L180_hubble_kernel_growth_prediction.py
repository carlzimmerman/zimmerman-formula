#!/usr/bin/env python3
"""L180 -- THE HUBBLE-KERNEL GROWTH EQUATION. From a0 = kappa c sqrt(G rho_Lambda) and the Hubble-flow prescription for the cosmological
kernel argument: G_eff(z)/G = nu(cH(z)/a0) with cH0/a0 = (1/kappa) sqrt(8 pi / (3 Omega_Lambda)). No new parameter. Computes the
scale-independent linear growth with this G_eff (both footings via kappa, and the nu_RAR function), sigma8/S8 relative to LCDM, and
f sigma8(z) shifts at RSD redshifts. Falsifiable now at the few-percent level. No literal-True checks."""
import numpy as np
from scipy.integrate import solve_ivp
CH = []
def check(n, ok, d=""):
    CH.append(bool(ok)); print(f"  [{'PASS' if ok else 'FAIL'}] {n}" + (f"\n           ({d})" if d else ""))
h = 0.6736; Om = 0.3138; OL = 1 - Om; c = 2.998e8; H0 = 100*h*1e3/3.0857e22
A0 = {"canonical (kappa=1/2)": 9.3619e-11, "alt (kappa=0.6)": 1.1279e-10}
E = lambda a: np.sqrt(Om*a**-3 + OL)
nu = lambda x: 1.0/(1.0 - np.exp(-np.sqrt(x)))
for lab, a0 in A0.items():
    r0 = c*H0/a0; print(f"    {lab}: cH0/a0 = {r0:.2f}; G_eff/G today = {nu(r0):.4f}, z=0.5: {nu(r0*E(1/1.5)):.4f}, z=1: {nu(r0*E(0.5)):.4f}, z=3: {nu(r0*E(0.25)):.4f}")
kap = 0.5; ident = (1/kap)*np.sqrt(8*np.pi/(3*OL)); print(f"    identity check: (1/kappa) sqrt(8 pi/(3 Omega_L)) = {ident:.2f} vs cH0/a0(canonical) = {c*H0/A0['canonical (kappa=1/2)']:.2f}")
check("E1 the identity cH0/a0 = (1/kappa) sqrt(8pi/(3 Omega_Lambda)) reproduces the canonical footing's cH0/a0 to 2% (kappa = 1/2)", abs(ident/(c*H0/A0["canonical (kappa=1/2)"]) - 1) < 0.02)
def growth(geff):
    def rhs(l, y):
        a = np.exp(l); Oma = Om*a**-3/E(a)**2
        return [y[1], 1.5*Oma*geff(a)*y[0] - (2 - 1.5*Oma)*y[1]]
    ls = np.linspace(np.log(1/101), 0, 600); sol = solve_ivp(rhs, [ls[0], 0], [1.0, 1.0], t_eval=ls, rtol=1e-9, atol=1e-12)
    return np.exp(ls), sol.y[0], sol.y[1]/sol.y[0]     # a, D, f
a_, D_L, f_L = growth(lambda a: 1.0)
print(f"    {'footing':<22} {'D(0)/D_LCDM':>11} {'sigma8 ratio':>12} {'S8 (LCDM 0.834 Planck)':>22} {'d fsig8/fsig8 z=0.3':>19} {'z=0.6':>7} {'z=1.0':>7}")
res = {}
for lab, a0 in A0.items():
    r0 = c*H0/a0; a_, D, f = growth(lambda a: nu(r0*E(a)))
    ratio = D[-1]/D_L[-1]; S8 = 0.834*ratio
    fs = {z: (f[np.argmin(abs(a_ - 1/(1+z)))]*D[np.argmin(abs(a_ - 1/(1+z)))])/(f_L[np.argmin(abs(a_ - 1/(1+z)))]*D_L[np.argmin(abs(a_ - 1/(1+z)))]) - 1 for z in (0.3, 0.6, 1.0)}
    res[lab] = (ratio, S8, fs)
    print(f"    {lab:<22} {ratio:11.4f} {ratio:12.4f} {S8:22.3f} {100*fs[0.3]:18.1f}% {100*fs[0.6]:6.1f}% {100*fs[1.0]:6.1f}%")
check("E2 [PREDICTION] the equation raises sigma8 by 1-3% relative to Planck-LCDM on both footings (S8 0.84-0.86): opposite in sign to the S8 tension, so KiDS/DES/DESI can kill it",
      all(1.01 < v[0] < 1.03 for v in res.values()), ", ".join(f"{k}: S8={v[1]:.3f}" for k, v in res.items()))
check("E3 [PREDICTION] f sigma8 at z = 0.3-1.0 is raised by 1-4%, inside current RSD errors (~5%) and at DESI-Y5 reach (~1-2%)",
      all(0.005 < v[2][0.3] < 0.05 and v[2][1.0] < v[2][0.3] for v in res.values()))
print("    NOTE: this is the framework's cosmology under prescription (B), with the dark component clustering as in LCDM; the galaxy-side gates are unchanged by it.")
print(f"\nL180 COMPLETE: {sum(CH)}/{len(CH)} checks PASS.")
