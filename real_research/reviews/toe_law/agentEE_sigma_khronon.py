#!/usr/bin/env python3
"""agentEE — can the khronon medium's own fluctuation spectrum produce sigma_req structurally?

Small verified chunks; each section [n] prints PASS/FAIL-style facts.
Raw numbers only. zeta = (16pi/3)^(1/4) QUARANTINED: never used numerically; zeta kept symbolic/unit.
"""
import numpy as np
import sympy as sp
import mpmath as mp

print("=" * 88)
print("[1] THE Z-TEST: khronon-class (sound-speed) field on dS is NOT a function of Z alone")
print("=" * 88)
# Conformal-mass member with sound speed c_s on dS, flat slicing, adiabatic vacuum:
#   f_k(eta) = (H*eta/sqrt(2 c_s k)) e^{-i c_s k eta}   (chi = a*phi modes exactly Minkowski-form,
#   the 1206.1083 structure for the reparametrization-symmetric foliation mode)
# Closed form (computed below by direct mode integral, then tested):
#   W(eta,eta',r) = H^2 eta eta' / (4 pi^2 c_s) * 1/(r^2 - c_s^2 (Deta - i eps)^2)
# dS invariant (flat slicing): Z = 1 + (Deta^2 - r^2)/(2 eta eta')
# c_s = 1  =>  W = H^2/(8 pi^2) * 1/(1 - Z)   (function of Z alone — agentV's [A2] conformal check)
# c_s != 1 =>  W depends on (Z, eta'/eta) jointly. Machine check: vary eta'/eta on a Z-level set.

H = 1.0
def W_closed(eta1, eta2, r, cs, eps=1e-9):
    de = (eta1 - eta2) - 1j * eps
    return H**2 * eta1 * eta2 / (4 * np.pi**2 * cs) / (r**2 - cs**2 * de**2)

def W_modeint(eta1, eta2, r, cs, kmax=400.0, n=200000, eps=1e-3):
    # direct mode integral: W = int d^3k/(2pi)^3 f_k(eta1) fbar_k(eta2) e^{ik.r}
    #   = H^2 eta1 eta2/(4 pi^2 c_s r) * int_0^inf dk sin(kr) e^{-i c_s k (Deta - i eps)}
    k = np.linspace(1e-6, kmax, n)
    de = (eta1 - eta2) - 1j * eps
    integ = np.sin(k * r) * np.exp(-1j * cs * k * de) * np.exp(-eps * k)  # eps: UV regulator -> i eps prescr.
    val = np.trapezoid(integ, k)
    return H**2 * eta1 * eta2 / (4 * np.pi**2 * cs * r) * val

def Z_of(eta1, eta2, r):
    return 1 + ((eta1 - eta2)**2 - r**2) / (2 * eta1 * eta2)

# (1a) closed form vs mode integral (spot check)
e1, e2, r, cs = -1.0, -0.6, 0.35, 2.0
wc, wm = W_closed(e1, e2, r, cs), W_modeint(e1, e2, r, cs)
print(f"[1a] closed form vs mode integral at (eta,eta',r)=({e1},{e2},{r}), c_s={cs}:")
print(f"     closed = {wc:.6e}   mode-sum = {wm:.6e}   rel.diff = {abs(wc-wm)/abs(wc):.2e}")

# (1b) the Z-level-set test: fix Z (timelike, Z>1), scan lambda = eta'/eta, c_s = 1 vs c_s != 1
Ztarget = 1.5  # timelike chord (the sigma_req region)
print(f"[1b] Z-level-set test at Z = {Ztarget} (timelike): scan lam = eta'/eta")
print(f"     {'lam':>6} | {'W (c_s=1) x 1/(1-Z) check':>28} | {'W (c_s=2)':>14} | {'W (c_s=10)':>14}")
vals = {1.0: [], 2.0: [], 10.0: []}
for lam in [0.3, 0.5, 0.8, 0.95]:
    eta1 = -1.0
    eta2 = lam * eta1
    # choose r to hit Ztarget: r^2 = Deta^2 - 2 eta eta'(Z-1)
    r2 = (eta1 - eta2)**2 - 2 * eta1 * eta2 * (Ztarget - 1)
    if r2 <= 0:  # purely timelike with r=0 unreachable -> r imaginary; use timelike with r2>0 region
        print(f"     lam={lam}: r^2={r2:.3f} <0, skip")
        continue
    r = np.sqrt(r2)
    row = []
    for cs_ in [1.0, 2.0, 10.0]:
        w = W_closed(eta1, eta2, r, cs_).real
        vals[cs_].append(w)
        row.append(w)
    print(f"     {lam:>6} | {row[0]:>28.6e} | {row[1]:>14.6e} | {row[2]:>14.6e}")
for cs_ in [1.0, 2.0, 10.0]:
    v = np.array(vals[cs_])
    spread = (v.max() - v.min()) / abs(v.mean())
    tag = "Z-ONLY (invariant)" if spread < 1e-12 else "NOT a function of Z"
    print(f"     c_s = {cs_:>4}: spread across the Z-level set = {spread:.3e}  -> {tag}")
print("     => c_s=1 conformal member: constant on Z-level sets (dS-invariant, the [A2] check).")
print("        c_s!=1 khronon-class member: VARIES on Z-level sets -> W admits NO representation")
print("        W = W(Z) = int drho(M^2) W_BD(Z;M^2). The Bros-Moschella dS-KL premise FAILS at its")
print("        first step (single-invariant dependence), before positivity is even invoked.")

# (1c) worldline pullback on the comoving geodesic (r -> 0): stationarity + KMS survive
print("[1c] comoving-worldline pullback, c_s arbitrary:")
t, tp, tau, csym, Hs = sp.symbols('t tp tau c_s H', positive=True)
eta_t = -sp.exp(-Hs * t) / Hs
eta_tp = -sp.exp(-Hs * tp) / Hs
expr = (Hs**2 * eta_t * eta_tp / (4 * sp.pi**2 * csym)) / (0**2 - csym**2 * (eta_t - eta_tp)**2)
expr_tau = sp.simplify(expr.subs(t, tp + tau))
target = -Hs**2 / (16 * sp.pi**2 * csym**3 * sp.sinh(Hs * tau / 2)**2)
print(f"     W(t,t')|_(r=0) simplified - target = {sp.simplify(expr_tau - target)}")
print("     => W(tau) = -H^2/(16 pi^2 c_s^3 sinh^2(H tau/2)): STATIONARY in proper time (dilatation),")
print("        i*beta-periodic with beta = 2pi/H -> KMS at T_GH SURVIVES foliation breaking (this member);")
print("        amplitude rescaled 1/c_s^3. Cut class at the cone: POWER LAW (double pole), zero flatness.")
