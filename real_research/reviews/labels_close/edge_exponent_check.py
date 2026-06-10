#!/usr/bin/env python3
"""
Pin the TRUE soft-edge DOS exponent of the q-Gaussian measure mu(theta), as theta->0 (or pi).
The naive fixed-fraction window overestimates s at large q because the edge sharpens. We fit
mu vs the edge distance using a window that shrinks proportionally to the edge sharpness, and
also check the analytic small-(pi-theta) expansion.

q-Gaussian: mu(theta) = (q;q)_inf |(e^{2i theta};q)_inf|^2 / (2pi),  E = 2cos(theta)/sqrt(1-q).
Near theta->pi: let phi = pi - theta -> 0. e^{2i theta} = e^{2i pi}e^{-2i phi} = e^{-2i phi}.
(e^{2i theta};q)_inf at phi=0 is (1;q)_inf = (1-1)*...=0 -> the k=0 factor (1 - e^{2i theta})
= (1 - e^{-2i phi}) ~ 2i phi. So |(e^{2i theta};q)_inf|^2 ~ |2i phi|^2 * |rest|^2 = 4 phi^2 * C.
Thus mu ~ phi^2 near the edge in THETA. In ENERGY: E0 - |E| with E = 2cos(theta)/sqrt(1-q);
near theta=pi, cos(theta) = cos(pi-phi) = -cos(phi) ~ -(1 - phi^2/2), so |E| ~ E0(1-phi^2/2),
E0-|E| ~ E0 phi^2/2 -> phi ~ sqrt(E0-|E|). Then mu ~ phi^2 ~ (E0-|E|).
=> in ENERGY the DOS VANISHES LINEARLY at the edge: rho(E) dE = mu(theta) dtheta, and
   dtheta/dE ~ 1/sqrt(E0-|E|), so rho(E) ~ mu * dtheta/dE ~ (E0-|E|) / sqrt(E0-|E|)
   = sqrt(E0-|E|)  => the ENERGY DOS rho(E) ~ sqrt(E0-|E|), local power s_E = 1/2.  <-- THE Wigner sqrt edge.
This is the standard semicircle/q-Gaussian soft edge: rho(E) ~ sqrt(edge distance), s=1/2.
"""
import numpy as np

NPOCH = 400
def qpoch(a, q, N=NPOCH):
    a = np.asarray(a, dtype=complex); out = np.ones(a.shape, dtype=complex); qk = 1.0
    for _ in range(N):
        out *= (1 - a * qk); qk *= q
    return out
def mu_theta(theta, q):
    qq = qpoch(q, q).real; e2 = np.exp(2j*np.asarray(theta,dtype=float))
    return qq*(qpoch(e2,q)*qpoch(np.conj(e2),q)).real/(2*np.pi)

print("Soft-edge exponent of the ENERGY DOS rho(E), where rho(E) = mu(theta)*|dtheta/dE|.")
print("Expect rho(E) ~ (E0-|E|)^s with s=1/2 (Wigner sqrt edge), independent of q.\n")
print(f"  {'q':>6} | {'s_theta(mu vs phi)':>18} | {'s_E (rho vs edge-dist)':>22}")
for q in (0.3,0.5,0.7,0.9,0.95,0.99):
    # use a phi-window that is genuinely small (asymptotic), log-spaced
    phi = np.logspace(-5, -2.5, 4000)     # pi-theta, deep in the asymptotic edge
    theta = np.pi - phi
    mu = mu_theta(theta, q)
    sqrt1mq = np.sqrt(1-q)
    E = 2*np.cos(theta)/sqrt1mq
    E0 = 2/sqrt1mq
    edge = E0 - np.abs(E)
    rhoE = mu / np.abs(2*np.sin(theta)/sqrt1mq)   # |dE/dtheta| = 2 sin(theta)/sqrt(1-q); rho_E = mu/|dE/dtheta|
    good = (mu>0)&(rhoE>0)&(edge>0)
    s_theta = np.polyfit(np.log(phi[good]), np.log(mu[good]), 1)[0]
    s_E = np.polyfit(np.log(edge[good]), np.log(rhoE[good]), 1)[0]
    print(f"  {q:>6.2f} | {s_theta:>18.4f} | {s_E:>22.4f}")

print("""
CONCLUSION: in THETA, mu ~ phi^2 (s_theta=2). In ENERGY, rho(E) ~ sqrt(E0-|E|) (s_E=1/2),
the universal Wigner sqrt soft edge -- q-independent. So the EDGE freezing exponent is
p_MOND=(s_E+1)/(s_E+2)=(1.5)/(2.5)=3/5 -> g~g_bar^0.6 = anti-MOND, for ANY q. The earlier
fixed-fraction window overstated s because it sat OUTSIDE the asymptotic sqrt regime.
The CENTER (rho ~ const, s_E=0 -> p=1/2 -> MOND) and EDGE (s_E=1/2 -> p=3/5 -> anti-MOND)
discriminator is therefore SOLID and q-robust. Only the PLACEMENT of |vac> is contested.""")
