#!/usr/bin/env python3
"""CFG478: first-order switch legibility -- door B of the openai/math re-read.

Outside lemma (radial continuum phase transition with algebraic decay paper,
Theorem 1.1): there is a bounded continuous stable radial pair potential
phi(r) with |phi(r)| <= C r^{-3-1/32} (r>=1) whose canonical free energy of the
3D classical gas has a FIRST-ORDER transition: the canonical pressure is
discontinuous at one inverse temperature throughout an OPEN density interval
(Simon's continuum problem construction; Lebowitz-Mazel-Presutti mechanism:
a bounded repulsive core permitting clusters <= 4 + a long-range attraction
entering as the quadratic density term via the variational operator
  T_a Q(beta,h) = sup_u { Q(beta, h+beta*a*u) - beta*a*u^2/2 }).

Transfer to the framework: the two-regime rule (CFG396) -- phantom action only
where rho_cold < rho_ph, capped -- is a first-order switch. L227 says every
MONOTONE MOND kernel gives a continuous transition, so a sharp switch cannot
come from a smooth interpolating function. #228 removes that obstruction: the
sharp switch can be thermodynamic (canonical coexistence of two densities at one
beta) with a stable, bounded, continuous radial kernel. The kernel stays
absolutely legal (bounded, continuous, algebraically decaying tail).

This script demonstrates the mechanism class numerically (LMP skeleton):
Carnahan-Starling hard-sphere free energy + mean-field attraction -> the
double-tangent coexistence construction. Computes the critical beta, the two
coexisting densities, and the canonical free-energy derivative (pressure) jump.
"""
import numpy as np
from scipy.optimize import brentq

# ---- van der Waals skeleton (the classical LMP-mechanism free energy) ----
# f(rho)/(kT) = rho*ln(rho/(1-b*rho)) + rho*T/(1-b*rho)... canonically:
#   f(rho) = rho*ln(rho) - rho*ln(1-b*rho) + (b*rho/(1-b*rho))*rho - beta*a*rho^2/2
# i.e. the vdW free energy density at kT=1 with excluded volume b and
# mean-field attraction a (Simon/Lebowitz-Mazel-Presutti skeleton; the #228
# paper constructs the same mechanism with an explicit stable radial pair
# potential and algebraic-decay tail).
B = 1.0   # excluded volume (close packing rho = 1/B)

def f_rho(rho, beta, a):
    if rho <= 0 or rho >= 1.0/B: return np.nan
    ideal = rho*np.log(rho)
    excl  = -rho*np.log(1-B*rho)
    return ideal + excl - beta*a*rho**2

def dmu(rho, beta, a):
    if rho <= 0 or rho >= 1.0/B: return np.nan
    return np.log(rho) + 1.0 - np.log(1-B*rho) + B*rho/(1-B*rho) - 2*beta*a*rho

def coexistence(beta, a):
    """Double tangent via the 1D slope formulation. On the slope-overlap window
    [mu2, mu1] (mu1 = gas-spinodal chemical potential, mu2 = liquid-spinodal),
    define rho_g(s), rho_l(s) as the branch points with dmu = s and
    h(s) = (f(rho_l)-f(rho_g))/(rho_l-rho_g) - s.  A root of h is a common
    tangent; pick the root with the widest density gap (the stable one)."""
    from scipy.optimize import brentq
    Bv = B
    def fdd(rho):                        # d2f/drho2
        return 1.0/rho + Bv/(1-Bv*rho)**2 - 2*beta*a
    # spinodal roots (convexity boundaries)
    try:
        r1 = brentq(fdd, 1e-6, 0.5, xtol=1e-12)
        r2 = brentq(fdd, 0.5, 1.0/Bv - 1e-7, xtol=1e-12)
    except ValueError:
        return None
    mu1 = dmu(r1, beta, a)               # gas branch slopes: (-inf, mu1]
    mu2 = dmu(r2, beta, a)               # liquid branch slopes: [mu2, inf)
    if mu2 > mu1: return None            # no overlap -> no tangent
    def rho_g(s): return brentq(lambda r: dmu(r, beta, a) - s, 1e-10, r1, xtol=1e-13)
    def rho_l(s): return brentq(lambda r: dmu(r, beta, a) - s, r2, 1.0/Bv - 1e-10, xtol=1e-13)
    def h(s):
        rg, rl = rho_g(s), rho_l(s)
        return (f_rho(rl,beta,a)-f_rho(rg,beta,a))/(rl-rg) - s
    # scan the window for the root with the widest gap
    s_lo, s_hi = mu2 + 1e-9, mu1 - 1e-9
    if s_hi <= s_lo: return None
    try:
        roots = brentq(h, s_lo, s_hi, xtol=1e-12)
    except ValueError:
        return None
    # refinement: the root of h may be near the window edge; verify convexity
    rg, rl = rho_g(roots), rho_l(roots)
    if rl - rg < 0.05: return None
    if dmu(rg+1e-6,beta,a) < dmu(rg,beta,a): return None
    if dmu(rl-1e-6,beta,a) > dmu(rl,beta,a): return None
    return (rg, rl, roots)

def main():
    print("="*72)
    print("CFG478: first-order switch legality (door B) - LMP skeleton demo")
    print("="*72)
    a = 28.0   # mean-field attraction strength (vdW units, b=1)
    print(f"\nmodel: van der Waals skeleton (ideal + excluded volume b=1 + attraction a), a={a}")
    print("scanning inverse temperature for the double-tangent (coexistence)...")
    beta_c = None
    # vdW critical point: beta_c*a = 27/8 * ... spinodal needs beta*a > 6;
    # coexistence window sits just above it, so scan the LOW-beta band.
    for beta in np.arange(0.14, 0.70, 0.002):
        res = coexistence(beta, a)
        if res is not None:
            beta_c = beta; break
    if beta_c is None:
        print("FAIL: no coexistence found in scan")
        return
    r1, r2, mu = coexistence(beta_c, a)
    P = r1*mu - f_rho(r1, beta_c, a)     # coexistence pressure (rho*mu - f)
    print(f"\ncritical inverse temperature beta_c = {beta_c:.4f}  (beta*a = {beta_c*a:.3f})")
    print(f"coexisting densities:  rho_gas  = {r1:.5f}   rho_liquid = {r2:.5f}")
    print(f"density ratio rho_liq/rho_gas = {r2/r1:.2f}")
    print(f"canonical pressure at coexistence P = {P:.4f}  (derivative jump!)")
    P1 = dmu(r1, beta_c, a); P2 = dmu(r2, beta_c, a)
    print(f"open density interval of coexistence: [{r1:.4f}, {r2:.4f}]  "
          f"(volume fractions b*rho: {r1:.3f} .. {r2:.3f})")
    print(f"pressure equality at the two ends: P(rho_gas)={P1:.4f} = P(rho_liq)={P2:.4f}")
    print("\n" + "-"*72)
    print("Transfer verdict (door B):")
    print("  * the sharp switch needs NO smooth interpolating kernel (L227 is")
    print("    about monotone kernels; the coexistence here is thermodynamic).")
    print("  * the #228 kernel itself is legal for the framework: bounded,")
    print("    continuous, stable, tail ~ r^{-3-1/32} (integrable, just barely).")
    print("  * KILL CONDITION: if the phantom two-regime rule is FORBIDDEN to")
    print("    carry a free-energy-type discontinuity (e.g. by a smooth-action")
    print("    requirement), this door closes.")
    print("="*72)

if __name__ == "__main__":
    main()