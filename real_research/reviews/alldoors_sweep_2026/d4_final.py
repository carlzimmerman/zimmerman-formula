#!/usr/bin/env python3
"""
D4 FINAL: framework nu(y)=sqrt(1+1/y) Cassini Q2, robust integrator (VALIDATED on
Hees+2016 nu_alpha family to ~1-2%), correct eta->e_N deconvolution, both footings.

Machinery: Park+2026 (2602.17884) Eq(9a)-(9b) == Hees+2016 (1510.01369) Eq(12).
Observed: Q2 = (1.6 +/- 1.8)e-27 s^-2 (Park+2026, 1 sigma).

Framework nu is a SIMPLE-type (power-law-tail) IF: nu-1 ~ 1/(2y) as y->inf.
Hees/Park: the Simple IF (n=1) is EXACTLY the case excluded by Cassini because its
phantom density is 'cuspy'/divergent -> large residual Q2. So we expect the
framework nu to land HIGH. This confirms/quantifies the inherited MG-realization wall.
"""
import numpy as np
from scipy import integrate, optimize

G, Msun = 6.674e-11, 1.989e30
GMsun = G*Msun
Q2_OBS, Q2_ERR = 1.6e-27, 1.8e-27

def nu_framework(y):
    y = np.maximum(y, 1e-300)
    return np.sqrt(1.0 + 1.0/y)

def nu_alpha(y, a):                 # Hees Eq 5a (validated) -- reference only
    y = np.maximum(y, 1e-300)
    return ((1.0 + (1.0 + 4.0*y**(-a))**0.5)/2.0)**(1.0/a)

def eN_from_eta(eta, nu_func):      # eta=g_e/a0 = e_N*nu(e_N); solve for e_N
    return optimize.brentq(lambda eN: eN*nu_func(eN)-eta, 1e-10, eta,
                           xtol=1e-16, rtol=1e-14)

def q_of_eN(eN, nu_func):
    def integrand(xi, t):
        v = t/(1.0-t); jac = 1.0/(1.0-t)**2
        arg = np.sqrt(eN**2 + v**4 + 2.0*eN*v**2*xi)
        return (nu_func(arg)-1.0)*(eN*(3*xi-5*xi**3)+v**2*(1-3*xi**2))*jac
    val, _ = integrate.dblquad(integrand, 0.0, 1.0-1e-12,
                               lambda t:-1.0, lambda t:1.0,
                               epsabs=1e-13, epsrel=1e-12)
    return 1.5*val

def Q2_from_q(q, a0):
    return -(3.0*a0**1.5/(2.0*np.sqrt(GMsun)))*q

# footings and fields
A0 = {"canonical_9.36e-11": 9.36e-11, "alt_1.13e-10": 1.13e-10}
V0, R0 = 233e3, 8.2*3.086e19
GE = {"Hees_min_1.9e-10":1.9e-10, "Hees_max_2.4e-10":2.4e-10,
      "modern_233/8.2kpc":V0**2/R0}

print("="*90)
print("DOOR D4 FINAL: framework nu=sqrt(1+1/y) Cassini Q2 (Park+2026 machinery)")
print(f"Observed Q2 = (1.6 +/- 1.8)e-27 s^-2   1-sig[{Q2_OBS-Q2_ERR:+.2e},{Q2_OBS+Q2_ERR:+.2e}]"
      f"  95%[{Q2_OBS-1.96*Q2_ERR:+.2e},{Q2_OBS+1.96*Q2_ERR:+.2e}]")
print("Integrator VALIDATED on Hees nu_alpha=2 (-q=0.1008 vs 0.100) and nu_alpha=3")
print("="*90)
print(f"\n{'a0 footing':20s} {'g_e field':18s} {'e_N':>6s} {'-q':>8s} "
      f"{'Q2[s^-2]':>12s} {'sigma':>7s} {'in95%?':>7s}")
print("-"*90)
allres = {}
for a0l, a0 in A0.items():
    allres[a0l]=[]
    for gel, ge in GE.items():
        eta = ge/a0
        eN = eN_from_eta(eta, nu_framework)
        q = q_of_eN(eN, nu_framework)
        Q2 = Q2_from_q(q, a0)
        sig = (Q2-Q2_OBS)/Q2_ERR
        in95 = abs(Q2-Q2_OBS) <= 1.96*Q2_ERR
        allres[a0l].append(Q2)
        print(f"{a0l:20s} {gel:18s} {eN:6.3f} {-q:8.4f} {Q2:+12.3e} "
              f"{sig:+7.1f} {str(in95):>7s}")

print("\n" + "="*90)
print("VERDICT SUMMARY")
print("="*90)
for a0l in A0:
    lo, hi = min(allres[a0l]), max(allres[a0l])
    slo, shi = (lo-Q2_OBS)/Q2_ERR, (hi-Q2_OBS)/Q2_ERR
    print(f"  {a0l}: Q2 in [{lo:+.2e}, {hi:+.2e}] s^-2  = [{slo:+.1f}, {shi:+.1f}] sigma high")
print(f"\n  Obs 95% upper bound: {Q2_OBS+1.96*Q2_ERR:+.2e} s^-2")
print(f"  Framework MINIMUM (canonical, min field): {min(allres['canonical_9.36e-11']):+.2e} s^-2")
ratio = min(allres['canonical_9.36e-11'])/(Q2_OBS+1.96*Q2_ERR)
print(f"  -> framework floor is {ratio:.0f}x above the 95% upper bound")

# reference: where nu_alpha=2 (a MOND family Cassini already disfavors) sits, same footing
print("\n  Reference (same footing, canonical a0, modern field):")
for name, nf in [("framework sqrt(1+1/y)", nu_framework),
                 ("nu_alpha=2 (Standard)", lambda y:nu_alpha(y,2)),
                 ("nu_alpha=4", lambda y:nu_alpha(y,4)),
                 ("nu_alpha=8", lambda y:nu_alpha(y,8))]:
    ge = GE["modern_233/8.2kpc"]; a0=9.36e-11
    eN = eN_from_eta(ge/a0, nf); Q2 = Q2_from_q(q_of_eN(eN,nf), a0)
    print(f"     {name:24s}: Q2={Q2:+.2e}  ({(Q2-Q2_OBS)/Q2_ERR:+.1f} sigma)")
print("  (higher alpha = sharper transition = smaller Q2; framework is a SLOW/simple IF -> large Q2)")
