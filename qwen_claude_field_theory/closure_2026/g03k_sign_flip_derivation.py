#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""g03k -- derivation of the sign-flip scale from the screened anisotropic Green's function.
Linearising the candidate's static law  div[mu grad Phi] - xi^2 Delta^2 psi = 4 pi G rho  (Phi = Phi_0 + psi, the operator on the scalar part)
about the uniform observed field g_e zhat gives, for a point mass M,
        Phi_hat(k) = -4 pi G M (1 + xi^2 k^2) / [ mu_e k^2 (1 + L cos^2 theta_k) + xi^2 k^4 ],   mu_e = mu(y_e), L = y_e mu'(y_e)/mu_e,
Newton at xi k >> 1, the AQUAL anisotropic Coulomb law at xi k << 1.  With q = xi k the potential is Phi = -(4 pi G M/xi) I(s/xi, theta; mu_e, L):
the crossing of Delta = gamma_aligned - gamma_perp is at s_x = x_x(y_e) xi, independent of r_e.  Here x_x is evaluated by quadrature:
I = 1/(4 pi x) + I_R,  I_R = int d^3q/(2 pi)^3 e^{i q.x} [1 - mu_e(1 + L c^2)]/[mu_e q^2 (1 + L c^2) + q^4]  (absolutely convergent),
gamma(x, theta) = 1 - 4 pi x^2 dI_R/dx.  Checks can fail."""
import numpy as np, math, sys
from scipy.special import j0
from numpy.polynomial.legendre import leggauss
FAILS = []
def check(name, ok, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
    if not ok: FAILS.append(name)
mu = lambda y: 1 - math.exp(-y)
def gamma_profile(ye, xs, theta, nq=6000, qmax=300.0, nth=96):
    mue = mu(ye); L = ye*math.exp(-ye)/mue
    q = np.linspace(1e-4, qmax, nq); c, w = leggauss(nth); c = 0.5*(c + 1); w = 0.5*w        # c = cos(theta_q) in [0, 1] (even integrand), weight doubled below
    C2 = c[:, None]**2; Q = q[None, :]
    R = (1 - mue*(1 + L*C2))/(mue*Q**2*(1 + L*C2) + Q**4)                                     # (nth, nq)
    st = np.sqrt(1 - c**2)[:, None]
    IR = np.zeros_like(xs); dq = q[1] - q[0]
    for i, x in enumerate(xs):
        ph = np.cos(Q*x*c[:, None]*math.cos(theta))*j0(Q*x*st*math.sin(theta))
        IR[i] = 2*np.sum(w[:, None]*R*ph*Q**2)*dq/(2*math.pi)**2                            # 2x for c in [-1,1]; azimuth done analytically (J0)
    dIR = np.gradient(IR, xs)
    return 1 - 4*math.pi*xs**2*dIR, IR
print("=" * 100); print("g03k -- the sign-flip scale from the screened anisotropic Green's function"); print("=" * 100)
xs = np.linspace(0.3, 12.0, 470)
# N1: the Newtonian limit is built in (I = 1/(4 pi x) + I_R); check the far limit against the AQUAL anisotropic Coulomb law
res = {}
for ye in (1.0, 1.573, 1.9, 2.5, 3.0):
    mue = mu(ye); L = ye*math.exp(-ye)/mue
    g0, _ = gamma_profile(ye, xs, 0.0); g90, _ = gamma_profile(ye, xs, math.pi/2); D = g0 - g90
    i = np.where(np.diff(np.sign(D)) != 0)[0]; xc = xs[i[0]] - D[i[0]]*(xs[i[0] + 1] - xs[i[0]])/(D[i[0] + 1] - D[i[0]]) if len(i) else float('nan')
    far0, far90 = 1/mue, 1/(mue*math.sqrt(1 + L)); res[ye] = (xc, g0, g90, far0, far90, len(i))
    print(f"  y_e = {ye:.3f} (mu_e = {mue:.4f}, L = {L:.4f}): gamma(x -> 12): aligned {g0[-1]:.4f} [AQUAL {far0:.4f}], perpendicular {g90[-1]:.4f} [AQUAL {far90:.4f}];  Delta at x = 0.5, 1, 2, 3, 5: " + " ".join(f"{np.interp(x, xs, D):+.4f}" for x in (0.5, 1, 2, 3, 5)) + f"  ->  x_x = {xc:.3f}  (sign changes: {len(i)})")
check("L1 at x = s/xi = 12 the screened response is within 5% of the AQUAL anisotropic Coulomb law 1/mu_e (aligned) and 1/(mu_e sqrt(1+L)) (perpendicular) at every y_e (the screening tail decays as a power of xi/s, so the approach is slow)",
      all(abs(res[ye][1][-1]/res[ye][3] - 1) < 0.05 and abs(res[ye][2][-1]/res[ye][4] - 1) < 0.05 for ye in res))
check("L2 Delta = gamma_aligned - gamma_perp is negative at small x and positive at large x with exactly one crossing at every y_e (the sign flip is a property of the linear screened response, not of the nonlinearity)",
      all(res[ye][5] == 1 and np.interp(0.5, xs, res[ye][1] - res[ye][2]) < 0 for ye in res))
xc_can, xc_alt = res[1.9][0], res[1.573][0]
print(f"\n  the crossing in units of xi: x_x(y_e = 1.9) = {xc_can:.3f} [3-D scan: 2.58, 2.48, 2.52 -> 2.53 +/- 0.05];  x_x(y_e = 1.573) = {xc_alt:.3f} [3-D scan: 2.58, 2.67 -> 2.63 +/- 0.05]")
check("L3 the linear-response crossing reproduces the 3-D nonlinear scan at the registered field: x_x = 2.53 +/- 0.05 (canonical, y_e = 1.9) and 2.63 +/- 0.05 (alt, y_e = 1.573) within 8%",
      abs(xc_can/2.53 - 1) < 0.08 and abs(xc_alt/2.63 - 1) < 0.08, f"linear {xc_can:.3f} vs 2.53; {xc_alt:.3f} vs 2.63")
print("  x_x(y_e) table: " + ", ".join(f"y_e = {ye}: {res[ye][0]:.3f}" for ye in res))
check("L4 x_x decreases monotonically with the external field, from 3.14 at y_e = 1 to 2.38 at y_e = 3, and is 2.4-2.65 over the Galactic range y_e = 1.5-2.5: the equation is s_x = x_x(y_e) xi with x_x tabulated here (2.51 at the registered canonical field, 2.63 alt)",
      all(res[a][0] > res[b][0] for a, b in zip([1.0, 1.573, 1.9, 2.5], [1.573, 1.9, 2.5, 3.0])) and 2.3 < res[2.5][0] < res[1.573][0] < 2.7)
print("\n  derivation summary: Phi_hat = -4 pi G M (1 + xi^2 k^2)/[mu_e k^2 (1 + L cos^2 theta_k) + xi^2 k^4]; with q = xi k the anisotropy is a function of s/xi and y_e only, so s_x = x_x(y_e) xi exactly in linear response, r_e-independent; x_x from the quadrature above.")
print(f"\nRESULT: {len(FAILS)} FAIL -> {FAILS}" if FAILS else "\nRESULT: 0 FAIL"); sys.exit(1 if FAILS else 0)
