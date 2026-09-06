#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""g03n -- captured fractions of the scalar dust in galaxies and clusters, as a function of |K_2| (the one free normalisation of its sound speed).
Improves g03m in two ways: (1) the Jeans criterion uses the MEAN enclosed effective density of the well (MOND phantom-enhanced mass), not the local
density at the outskirts; (2) the fraction is estimated with the filtering-mass formula f = [1 + (2^{1/3} - 1) M_J/M]^{-3} (Gnedin 2000, derived for
baryons whose Jeans mass exceeds part of the halo mass; applied here by analogy and labelled an estimate).  Sound speed: c_s^2 = 0.42 J_Y(y_loc)/|K_2| (c = 1),
J_Y from the completed kernel (g03j).  Representative systems (assumptions, stated): galaxy M_b = 5e10 Msun at R = 100 kpc (KiDS), cluster M_b = 1e14 Msun
at R500 = 1 Mpc with y_N = 0.4 (the repository's R500 = 0.33-0.58 a0).  Targets from the repository: KiDS <= 14% CDM-like halo around galaxies, clusters need
32-46%.  Question: is there a |K_2| with f_gal <= 0.14 and f_cl >= 0.32?  Checks can fail."""
import math, numpy as np, sys
from scipy.optimize import brentq
FAILS = []
def check(name, ok, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
    if not ok: FAILS.append(name)
G, c, kpc, MSUN, a0 = 6.6743e-11, 2.998e8, 3.0857e19, 1.98892e30, 9.3619e-11
Y1 = 1 - 1/math.e
def ytot_of(yN): return brentq(lambda t: t*(1 - math.exp(-t)) - yN, 1e-12, yN + 60)
def JY(yN):
    yt = ytot_of(yN); return yN/(yt*math.exp(-yt)) if yt <= 1 else yN/(1/math.e)
def nu_exp(yN): return ytot_of(yN)/yN
SYS = {"galaxy (KiDS, 100 kpc)": dict(Mb=5e10*MSUN, R=100*kpc), "galaxy inner (10 kpc)": dict(Mb=4e10*MSUN, R=10*kpc), "cluster (R500 = 1 Mpc)": dict(Mb=1e14*MSUN, R=1000*kpc)}
print("=" * 100); print("g03n -- captured dust fractions vs |K_2| (filtering-mass estimate, MOND effective wells)"); print("=" * 100)
props = {}
for nm, d in SYS.items():
    yN = G*d["Mb"]/(d["R"]**2*a0); Meff = d["Mb"]*nu_exp(yN); rho = Meff/(4*math.pi/3*d["R"]**3); jy = JY(yN)
    props[nm] = dict(yN=yN, Meff=Meff, rho=rho, JY=jy)
    print(f"  {nm:24s}: y_N = {yN:.3f} (y_tot = {ytot_of(yN):.3f}), MOND effective mass {Meff/MSUN:.2e} Msun, mean density {rho:.2e} kg/m^3, J_Y = {jy:.3f}")
def frac(nm, K2abs):
    p = props[nm]; cs = c*math.sqrt(0.42*p["JY"]/K2abs); lamJ = cs*math.sqrt(math.pi/(G*p["rho"])); MJ = 4*math.pi/3*p["rho"]*(lamJ/2)**3
    return (1 + (2**(1/3) - 1)*MJ/p["Meff"])**-3, lamJ, MJ
K2s = np.logspace(3, 13, 201)
fg = np.array([frac("galaxy (KiDS, 100 kpc)", k)[0] for k in K2s]); fc = np.array([frac("cluster (R500 = 1 Mpc)", k)[0] for k in K2s]); fi = np.array([frac("galaxy inner (10 kpc)", k)[0] for k in K2s])
print(f"\n  {'|K_2|':>8s} {'f_gal':>7s} {'f_inner':>7s} {'f_cl':>7s}    (KiDS needs f_gal <= 0.14; clusters need f_cl >= 0.32-0.46; the inner galaxy must stay near 0 for the RAR)")
for k in (1e3, 1e4, 3e4, 1e5, 2e5, 3e5, 1e6, 1e7, 1e8, 1e10):
    i = np.argmin(np.abs(np.log10(K2s) - math.log10(k))); print(f"  {K2s[i]:8.1e} {fg[i]:7.3f} {fi[i]:7.3f} {fc[i]:7.3f}")
ok = (fg <= 0.14) & (fc >= 0.32); ok46 = (fg <= 0.14) & (fc >= 0.46)
if ok.any(): print(f"\n  WINDOW (f_gal <= 0.14 and f_cl >= 0.32): |K_2| in [{K2s[ok].min():.2e}, {K2s[ok].max():.2e}] (factor {K2s[ok].max()/K2s[ok].min():.1f}); with f_cl >= 0.46: " + (f"[{K2s[ok46].min():.2e}, {K2s[ok46].max():.2e}]" if ok46.any() else "none"))
else:
    i = np.argmax(fc - fg); print(f"\n  NO WINDOW: the best separation is at |K_2| = {K2s[i]:.1e} with f_gal = {fg[i]:.3f}, f_cl = {fc[i]:.3f}")
ratio_R = (props["cluster (R500 = 1 Mpc)"]["Meff"]/props["galaxy (KiDS, 100 kpc)"]["Meff"])
print(f"  the cluster's effective mass exceeds the galaxy's by {ratio_R:.0f}x while its Jeans mass exceeds the galaxy's by {frac('cluster (R500 = 1 Mpc)', 1e8)[2]/frac('galaxy (KiDS, 100 kpc)', 1e8)[2]:.1f}x: the ratio M_J/M that sets the fraction is {frac('galaxy (KiDS, 100 kpc)', 1e8)[2]/props['galaxy (KiDS, 100 kpc)']['Meff'] / (frac('cluster (R500 = 1 Mpc)', 1e8)[2]/props['cluster (R500 = 1 Mpc)']['Meff']):.0f}x larger for the galaxy at any |K_2|")
check("F1 with the mean effective density the ordering survives: at every |K_2| the cluster's captured fraction exceeds the galaxy's", np.all(fc >= fg))
check("F2 there is a |K_2| range in which f_gal <= 0.14 (KiDS) and f_cl >= 0.32 (the cluster residual's lower requirement), i.e. the fractions, not only the Jeans ordering, admit the pincer's escape at this level of estimate", ok.any(),
      f"window {K2s[ok].min():.1e}-{K2s[ok].max():.1e}" if ok.any() else "none")
check("F3 the same range reaches f_cl >= 0.46 (the residual's upper requirement) somewhere", ok46.any(), f"{K2s[ok46].min():.1e}-{K2s[ok46].max():.1e}" if ok46.any() else "none")
check("F4 inside the window the inner galaxy (10 kpc, the rotation-curve regime) captures under 2% of its share, so the RAR is untouched", bool(ok.any()) and np.all(fi[ok] < 0.02), f"max f_inner in the window {fi[ok].max():.4f}" if ok.any() else "n/a")
check("F5 the window is narrow: under a factor 10 in |K_2| (a tuning, recorded as such)", ok.any() and K2s[ok].max()/K2s[ok].min() < 10, f"factor {K2s[ok].max()/K2s[ok].min():.1f}" if ok.any() else "n/a")
print("\n  caveats, stated: filtering-mass formula by analogy (no accretion history, no dust self-gravity, spherical, one representative system each); the numbers are an estimate of the escape's existence, not the fractions to compare with data. The Coma UDG kill and the residual's radial profile are not addressed.")
print(f"\nRESULT: {len(FAILS)} FAIL -> {FAILS}" if FAILS else "\nRESULT: 0 FAIL"); sys.exit(1 if FAILS else 0)
