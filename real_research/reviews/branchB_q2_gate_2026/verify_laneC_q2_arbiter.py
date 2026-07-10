#!/usr/bin/env python3
"""
ADVERSARIAL ARBITER for Lane C's load-bearing number: the scalar-class Q2.
===========================================================================
Lane C (and the committed baseline aest_cassini_quadrupole_full.py) use the transcribed
Milgrom-2009/Desmond-2024 quadrupole integral:
    q = (3/2) Int dv Int dxi (nu(Y)-1) [eN(3xi-5xi^3)+v^2(1-3xi^2)] / sqrt(D),
    D = eN^2+v^4+2 eN v^2 xi, Y=sqrt(D).
A from-scratch integration-by-parts derivation of the QUMOND phantom-density quadrupole
(this file, method B) gives the SAME integrand WITHOUT the 1/sqrt(D) factor.
Arbiter (method C): direct finite-difference divergence of the phantom flux on a 2D
(log r, theta) grid, no integration by parts, no closed form -- compute
rho_ph = -div[(nu-1) g_N]/(4piG) and its interior l=2 moment directly.
Analytic kill-test (method D): for CONSTANT nu-1=eps the phantom density is exactly
eps*M*delta^3 (pure monopole), so the true q MUST be 0. Check all three forms.
Then recompute the downstream numbers (x ceiling, sigma, w_max) with whichever form wins.
numpy/scipy only; exit 0.
"""
import numpy as np
from scipy import integrate

G    = 6.674e-11
Msun = 1.989e30
A0_CANON = 9.36e-11
A0_ALT   = 1.13e-10
Q2_C, Q2_S = 1.6e-27, 1.8e-27
Q2_CEIL = Q2_C + 2*Q2_S

def nu_fw(y):     return np.sqrt(1.0 + 1.0/y)
def nu_simple(y): return 0.5 + np.sqrt(0.25 + 1.0/y)

def solve_eN(etilde, nu):
    from scipy.optimize import brentq
    return brentq(lambda x: x*nu(x) - etilde, 1e-9, 1e4)

# ---------------- method A: the transcribed (lane/committed) form, WITH 1/sqrt(D)
def q_lane(etilde, numo, nu_for_eN, vmax=60.0):
    eN = solve_eN(etilde, nu_for_eN)
    def ig(xi, v):
        D = eN*eN + v**4 + 2*eN*v*v*xi
        if D <= 0: return 0.0
        return numo(np.sqrt(D))*(eN*(3*xi-5*xi**3) + v*v*(1-3*xi*xi))/np.sqrt(D)
    val,_ = integrate.dblquad(ig, 0.0, vmax, lambda v:-1.0, lambda v:1.0,
                              epsabs=1e-11, epsrel=1e-9)
    return 1.5*val, eN

# ---------------- method B: from-scratch parts derivation, NO 1/sqrt(D)
# rho_ph = -div[(nu-1) g_N]/(4piG); Q2 = 3G Int rho_ph P2(c)/r^3 d3x
#        = (3/(4pi)) Int (nu-1) g_N . grad[P2(c)/r^3] d3x   (boundary terms vanish)
# nondimensionalized (r_M = sqrt(GM/a0)), v = r_M/r, xi = -cos(theta):
def q_parts(etilde, numo, nu_for_eN, vmax=60.0):
    eN = solve_eN(etilde, nu_for_eN)
    def ig(xi, v):
        D = eN*eN + v**4 + 2*eN*v*v*xi
        if D <= 0: return 0.0
        return numo(np.sqrt(D))*(eN*(3*xi-5*xi**3) + v*v*(1-3*xi*xi))
    val,_ = integrate.dblquad(ig, 0.0, vmax, lambda v:-1.0, lambda v:1.0,
                              epsabs=1e-11, epsrel=1e-9)
    return 1.5*val, eN

# ---------------- method C: DIRECT finite-difference arbiter (no parts, no closed form)
def q_direct(etilde, numo, nu_for_eN, umin=3e-4, umax=3e4, Nx=3000, Nt=800):
    """
    Dimensionless (G=M=a0=1, lengths in r_M): g_N = eN zhat - rhat/u^2.
    F = m(|g_N|) g_N,  m = numo(|g_N|).  rho_ph = -div F/(4pi).
    Q2_dimless = 3 Int rho_ph P2(c)/u^3 d3u  -> q = -(2/3) Q2_dimless.
    Divergence in spherical axisymmetric coords on (x=ln u, theta) grid, central FD.
    """
    eN = solve_eN(etilde, nu_for_eN)
    x  = np.linspace(np.log(umin), np.log(umax), Nx)
    th = np.linspace(1e-6, np.pi-1e-6, Nt)
    u  = np.exp(x)[:,None]; T = th[None,:]
    c, s = np.cos(T), np.sin(T)
    gr = eN*c - 1.0/u**2          # radial component of g_N
    gt = -eN*s                    # theta component
    gm = np.sqrt(gr*gr + gt*gt)
    m  = numo(gm)
    Fr, Ft = m*gr, m*gt
    # div F = (1/u^2) d(u^2 Fr)/du + (1/(u s)) d(s Ft)/dth ; d/du = (1/u) d/dx
    A = (u**2)*Fr
    dA_dx = np.gradient(A, x, axis=0)
    div1 = dA_dx/(u**3)
    B = s*Ft
    dB_dth = np.gradient(B, th, axis=1)
    div2 = dB_dth/(u*s)
    div = div1 + div2
    P2 = 0.5*(3*c*c - 1.0)
    # Q2_dimless = -(3/2) Int div(F) P2 sin(th) dx dth   [d3u = 2pi u^3 s dx dth; psi=P2/u^3]
    integrand = div*P2*s
    trap = getattr(np, 'trapezoid', np.trapz)
    Q2_dim = -(1.5)*trap(trap(integrand, th, axis=1), x)
    return -(2.0/3.0)*Q2_dim, eN

def Q2_SI(a0, q):
    return -(3.0*a0**1.5)/(2.0*np.sqrt(G*Msun))*q

print("="*100)
print(" ARBITER: which q-integral is right? (lane/committed WITH 1/sqrt(D) vs parts-derived WITHOUT)")
print("="*100)

# ---------------- method D: constant nu-1 kill test (true answer EXACTLY 0: rho_ph = eps M delta^3)
print("\n(D) constant nu-1 = 0.1 (phantom = pure monopole => true q MUST be 0):")
const = lambda y: 0.1*np.ones_like(np.asarray(y, dtype=float))
nu_const = lambda y: 1.1
for name, fn in [("lane form (with 1/sqrt(D))", q_lane),
                 ("parts form (no 1/sqrt(D)) ", q_parts)]:
    qv, eN = fn(2.0, const, nu_const)
    print(f"    {name}: q = {qv:+.6e}   {'PASS (=0)' if abs(qv)<1e-6 else 'FAIL (nonzero for pure monopole!)'}")
qv, eN = q_direct(2.0, lambda y: 0.1*np.ones_like(y), nu_const)
print(f"    direct FD arbiter          : q = {qv:+.6e}   (grid noise scale)")

# ---------------- head-to-head on the physical nu's
print("\nhead-to-head q at the physical operating points:")
print(f"  {'case':<38}{'eN':>7}{'q_lane':>10}{'q_parts':>10}{'q_direct':>10}")
cases = [("simple nu, etilde=1.933 (baseline val)", nu_simple, lambda y: nu_simple(y)-1, 1.933),
         ("framework nu, etilde=2.479 (canonical)", nu_fw,     lambda y: nu_fw(y)-1,     2.32e-10/A0_CANON),
         ("framework nu, etilde=2.053 (alt)      ", nu_fw,     lambda y: nu_fw(y)-1,     2.32e-10/A0_ALT)]
res = {}
for name, nu, numo, et in cases:
    qa,_ = q_lane(et, numo, nu)
    qb,_ = q_parts(et, numo, nu)
    qc,eN = q_direct(et, numo, nu)
    res[name] = (qa, qb, qc, et)
    print(f"  {name:<38}{eN:>7.3f}{qa:>10.4f}{qb:>10.4f}{qc:>10.4f}")

# convergence check on the FD arbiter (canonical framework case)
name, nu, numo, et = cases[1]
print("\nFD arbiter convergence (framework nu, canonical):")
for Nx, Nt in [(1500,400),(3000,800),(4500,1200)]:
    qc,_ = q_direct(et, numo, nu, Nx=Nx, Nt=Nt)
    print(f"    Nx={Nx:>5} Nt={Nt:>5}: q_direct = {qc:+.5f}")

# ---------------- downstream: recompute the load-bearing numbers with the WINNING form
print("\n" + "="*100)
print(" DOWNSTREAM NUMBERS with each form (framework nu, g_ext=1.9-2.4e-10, both footings)")
print("="*100)
GEXT = [1.9e-10, 2.32e-10, 2.4e-10]
for tag, a0 in [("canonical", A0_CANON), ("alt", A0_ALT)]:
    for g in GEXT:
        et = g/a0
        qa,_ = q_lane(et, lambda y: nu_fw(y)-1, nu_fw)
        qb,_ = q_parts(et, lambda y: nu_fw(y)-1, nu_fw)
        Qa, Qb = abs(Q2_SI(a0,qa)), abs(Q2_SI(a0,qb))
        print(f"  {tag:<10} g_ext={g:.2e}: lane Q2={Qa:.2e} ({Qa/Q2_CEIL:.2f}x ceil, {(Qa-Q2_C)/Q2_S:.1f} sig, w_max={Q2_CEIL/Qa:.3f})"
              f" | parts Q2={Qb:.2e} ({Qb/Q2_CEIL:.2f}x, {(Qb-Q2_C)/Q2_S:.1f} sig, w_max={Q2_CEIL/Qb:.3f})")
print("\nEXIT 0")
