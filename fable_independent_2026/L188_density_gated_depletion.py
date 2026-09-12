#!/usr/bin/env python3
"""L188 -- THE DENSITY-GATED DEPLETION FAMILY (the loop's C002 class, done analytically). Any mechanism whose per-particle depletion
rate is a function of the LOCAL density, Gamma = eps (G rho)^(alpha/2) (alpha = 1: a fixed fraction per free-fall time), switched on at
z_c <= 2.2 (so the forest is untouched by construction), applied to NFW halos (Dutton-Maccio c(M)); mass REMOVED (converted). Gates:
(1) the ledger (spiral 0.105 at 3R_d, MW 0.14 at 30 kpc, cluster 0.576 at R500) fit with (eps*Dt, alpha); (2) G7 KiDS: the retained
CDM-like halo mass of a 1e12 halo in the 0.1-1 Mpc shell must be <= 0.14 -- but the shell is LESS dense than the cluster anchor over
most of its mass, so any rate monotone in density retains there at least what it retains in clusters (Lean: density_gate_monotone_bound);
(3) G8: the global removed fraction of dark matter (Sheth-Tormen mass function, halos 1e9-1e16 Msun) vs the 3% late-time Omega_m budget.
Both a0 footings are irrelevant here (no kernel enters); the family is tested on its own terms. No literal-True checks."""
import sys, os, numpy as np
from scipy.optimize import brentq
CH = []
def check(n, ok, d=""):
    CH.append(bool(ok)); print(f"  [{'PASS' if ok else 'FAIL'}] {n}" + (f"\n           ({d})" if d else ""), flush=True)
print("=" * 118 + "\nL188 DENSITY-GATED DEPLETION: ledger fit, KiDS monotonicity kill, Omega_m budget\n" + "=" * 118)
G = 6.674e-8; Msun = 1.989e33; Mpc = 3.086e24; Gyr = 3.156e16; h = 0.6736
rho_c = 2.775e11*h**2*Msun/Mpc**3                                     # g/cm^3
m = lambda x: np.log(1 + x) - x/(1 + x)
cDM = lambda M: 10**(0.905 - 0.101*np.log10(M*h/1e12))
def nfw(M):
    R200 = (3*M*Msun/(4*np.pi*200*rho_c))**(1/3); c = cDM(M); rs = R200/c; rho_s = 200*rho_c*c**3/(3*m(c)); return R200, rs, rho_s
def rho_of(r, M):
    R200, rs, rho_s = nfw(M); x = r/rs; return rho_s/(x*(1 + x)**2)
def retained(M, r1, r2, epsDt, alpha):                                  # retained mass fraction in shell [r1, r2], rate eps (G rho)^(alpha/2), removal
    r = np.geomspace(max(r1, 1e-4*Mpc), r2, 4000); rho = rho_of(r, M); w = rho*r**2
    keep = np.exp(-epsDt*(G*rho)**(alpha/2)); return np.trapz(w*keep, r)/np.trapz(w, r)
anchors = [("spiral 1.2e10 Mb (M200 3e11) inside 3R_d = 7.5 kpc", 3e11, 7.5e-3*Mpc, 0.105), ("Milky Way (1e12) inside 30 kpc", 1e12, 0.030*Mpc, 0.14),
           ("X-COP cluster (1e15) inside R500 = 1.38 Mpc", 1e15, 1.38*Mpc, 0.576)]
print("    local densities [g/cm^3]: " + "; ".join(f"{n.split(' (')[0]} at anchor {rho_of(r, M):.1e}" for n, M, r, _ in anchors) + f"; 1e12 halo at 0.1 / 0.3 / 1 Mpc: {rho_of(0.1*Mpc, 1e12):.1e} / {rho_of(0.3*Mpc, 1e12):.1e} / {rho_of(1*Mpc, 1e12):.1e}")
best = None
for alpha in (0.5, 1.0, 1.5, 2.0):
    # eps*Dt in units where (G rho)^(alpha/2) is in s^-alpha: scan log-uniformly
    grid = np.geomspace(1e-30, 1e40, 400)
    costs = [sum((np.log(retained(M, 0, r, e, alpha)) - np.log(t))**2 for _, M, r, t in anchors) for e in grid]
    e = grid[int(np.argmin(costs))]; fs = [retained(M, 0, r, e, alpha) for _, M, r, _ in anchors]
    print(f"    alpha = {alpha:.1f}: best eps*Dt -> f = " + " / ".join(f"{x:.3f}" for x in fs) + f"  (targets 0.105 / 0.14 / 0.576), max |ln(f/target)| = {max(abs(np.log(x/t)) for x, (_, _, _, t) in zip(fs, anchors)):.2f}")
    if best is None or min(costs) < best[0]: best = (min(costs), alpha, e, fs)
_, alpha, e, fs = best
check("V1 [ledger] the two-parameter density-gated rate reproduces all three ledger anchors within a factor 1.4 at its best (alpha, eps*Dt)",
      all(abs(np.log(x/t)) < np.log(1.4) for x, (_, _, _, t) in zip(fs, anchors)), f"alpha = {alpha}, f = " + " / ".join(f"{x:.3f}" for x in fs))
# G7 KiDS: 1e12 halo, shell 0.1-1 Mpc, at the best fit; and the monotonicity bound
fK = retained(1e12, 0.1*Mpc, 1.0*Mpc, e, alpha)
rho_cl = rho_of(1.38*Mpc, 1e15); f_cl_local = np.exp(-e*(G*rho_cl)**(alpha/2))
r = np.geomspace(0.1*Mpc, 1.0*Mpc, 4000); w = rho_of(r, 1e12)*r**2; frac_less_dense = np.trapz(w*(rho_of(r, 1e12) <= rho_cl), r)/np.trapz(w, r)
check("V2 [G7 KiDS, DEFICIT verified] at the ledger-fitting rate the 1e12 halo keeps far more than 14% of its CDM-like mass in the 0.1-1 Mpc lensing shell",
      fK > 0.14, f"retained in shell = {fK:.2f} (>= {frac_less_dense:.2f} of the shell mass is less dense than the cluster anchor, where retention >= {f_cl_local:.2f})")
check("V3 [structure, Lean density_gate_monotone_bound] the kill is generic: for ANY rate monotone in local density, retention in the part of the shell less dense than the cluster anchor is >= the cluster anchor's local retention; that part carries > 70% of the shell mass and the cluster anchor retains ~0.58 at any fit, so the shell cannot fall to 0.14",
      frac_less_dense > 0.70 and frac_less_dense*f_cl_local > 0.14, f"mass fraction less dense = {frac_less_dense:.2f}, cluster-anchor local retention = {f_cl_local:.2f}, product {frac_less_dense*f_cl_local:.2f} > 0.14")
# G8: global removed fraction (Sheth-Tormen), halos 1e9-1e16
sys.path.insert(0, os.path.abspath("L183_class_mond_kernel/site"))
from classy import Class
cl = Class(); cl.set({"h": h, "omega_b": 0.02237, "omega_cdm": 0.12, "A_s": 2.1e-9, "n_s": 0.9649, "output": "mPk", "P_k_max_h/Mpc": 200, "z_max_pk": 1}); cl.compute()
Om = cl.Omega_m(); rho_m = Om*rho_c
def sigma(M): R = (3*M*Msun/(4*np.pi*rho_m))**(1/3)/Mpc; return cl.sigma(R, 0.0)
Ms = np.geomspace(1e9, 1e16, 120); sig = np.array([sigma(M) for M in Ms]); lnsig = np.log(sig); dlnsdlnM = np.gradient(lnsig, np.log(Ms))
nu = 1.686/sig; A, a, p = 0.3222, 0.707, 0.3
fST = A*np.sqrt(2*a/np.pi)*nu*(1 + (a*nu**2)**(-p))*np.exp(-a*nu**2/2)          # nu f(nu) form: dn/dlnM = rho_m/M * f * |dlnsig/dlnM|
dndlnM = rho_m/(Ms*Msun)*fST*np.abs(dlnsdlnM)
frac_in_halos = np.trapz(dndlnM*Ms*Msun, np.log(Ms))/rho_m
removed = np.trapz(dndlnM*Ms*Msun*np.array([1 - retained(M, 0, nfw(M)[0], e, alpha) for M in Ms]), np.log(Ms))/rho_m
check("V4 [G8 Omega_m budget, DEFICIT verified] the removal variant deletes more than 3% of all dark matter by today (mass-weighted over the Sheth-Tormen halo population; unbound matter untouched)",
      removed > 0.03, f"removed fraction of all DM = {removed:.3f} (fraction of DM in halos > 1e9: {frac_in_halos:.2f}); redistribution instead of removal keeps Omega_m but raises the shell retention further")
print("    LIMITS: NFW + Dutton-Maccio, anchors as in L187, removal bookkeeping, z_c <= 2.2 so the forest is untouched by construction, no time-dependence beyond eps*Dt,\n"
      "    Sheth-Tormen at z = 0; the KiDS shell criterion is the repository's '<= 14% CDM-like halo at 0.1-1 Mpc'.")
import json; json.dump(dict(alpha=float(alpha), epsDt=float(e), f=[float(x) for x in fs], f_kids=float(fK), frac_less_dense=float(frac_less_dense), removed=float(removed)), open("L188_results.json", "w"), indent=1)
print(f"\nL188 COMPLETE: {sum(CH)}/{len(CH)} checks PASS.")
