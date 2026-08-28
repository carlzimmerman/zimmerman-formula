"""
### ⚠️ SUPERSEDED — CONTAINS A CATEGORY ERROR. Use fc_cassini_CORRECTED_2026.py. ###
### This script fed the internal AeST FIELD function tanh(y/2) into q_direct2D as if it were the
### OBSERVABLE boost nu. The Cassini quadrupole is sourced by the OBSERVABLE mu_obs=1-e^-y (bridge
### line 13), NOT the field function. Correct FC q = 3.76x ceiling (= plain exponential), NOT 6.09x.
### Kept for the record (RETRACTIONS.md 2026-08-28). Everything below is the ERRONEOUS calculation. ###

FC-AeST Cassini gate: the EFE quadrupole strength q for the exact-exponential FC kernel
mu_FC(x) = tanh(x/2), evaluated with the EXACT committed DHF quadrupole integral
(route1B_monotone_escape_2026.py, q_direct2D). This is the ONE solar-system gate Carl's
c_s^2 / r_C squeeze did NOT touch -- and it is the gate that killed mu = 1-e^{-y}.

q = 1.5 * INT INT (nu-1) N N  (DHF24 Eq.10 external-field phantom quadrupole).
Ceiling: Q2 = q * 1.5 a0^1.5/sqrt(GM) must clear 5.2e-27 s^-2 (Park+2026 2-sigma)
=> q must be BELOW ~0.066 at the solar-circle external field.

Reproduces the committed anchors (RouteA/MS08 -> q(2)=0.221; mu_exp fails; mu_n pass) as a
guard, then reports FC. NOT a new pipeline -- the same integral, one new kernel.
"""
import math, numpy as np
from scipy import integrate
from scipy.optimize import brentq

GM_SUN = 6.6743e-11 * 1.98892e30
A0 = 9.3619e-11
GEXT = 2.32e-10                    # Gaia EDR3 solar-circle external field (DHF24 sec 3.3)
Q2_CEIL = 5.2e-27                  # Park+2026 2-sigma
PREF = lambda a0: 1.5 * a0**1.5 / math.sqrt(GM_SUN)   # DHF24 Eq.(10)
Q_PASS = Q2_CEIL / PREF(A0)        # max q that clears the ceiling

# ---- committed kernels (verbatim form from route1B) ----
def nu_routeA(y):                                   # MS08 alpha=1/2 completion, EXPONENTIAL class
    y = np.asarray(y, float); s = np.sqrt(y)
    out = np.where(s < 1e-8, 1.0/np.maximum(s,1e-300), 1.0/(1.0-np.exp(-np.minimum(s,700.0))))
    return np.where(s > 40.0, 1.0+np.exp(-np.minimum(s,700.0)), out)
def nu_muexp(y):                                    # mu(x)=1-e^{-x}, EXPONENTIAL class (the killed one)
    y = np.atleast_1d(np.asarray(y, float)); out = np.empty_like(y)
    for i, yy in enumerate(y):
        if yy > 200: out[i] = 1.0 + math.exp(-yy)
        else:
            g = lambda x: x*(1.0-math.exp(-x)) - yy
            xr = brentq(g, 1e-12, yy+50.0, xtol=1e-14); out[i] = xr/yy
    return out if out.size > 1 else out[0]
def nu_mun(n):                                      # BN11 mu_n, SHARP class (the Cassini-safe escape)
    def f(y):
        y = np.atleast_1d(np.asarray(y, float)); out = np.empty_like(y)
        for i, yy in enumerate(y):
            g = lambda x: x*(x/(1.0+x**n)**(1.0/n)) - yy
            out[i] = brentq(g, 1e-12, yy+50.0, xtol=1e-14)/yy
        return out if out.size > 1 else out[0]
    return f

# ---- FC EXACT-EXPONENTIAL kernel: mu_FC(x) = tanh(x/2), x = g/a0 (physical) ----
# Newtonian y_N = x * mu_FC(x) = x*tanh(x/2); nu_FC(y_N) = x/y_N. Same inversion pattern as mu_exp.
def nu_FC(y):
    y = np.atleast_1d(np.asarray(y, float)); out = np.empty_like(y)
    for i, yy in enumerate(y):
        if yy > 200: out[i] = 1.0 + 2.0*math.exp(-yy)     # 1-tanh(x/2) ~ 2e^{-x}
        else:
            g = lambda x: x*math.tanh(x/2.0) - yy
            xr = brentq(g, 1e-12, yy+80.0, xtol=1e-14); out[i] = xr/yy
    return out if out.size > 1 else out[0]

# ---- committed DHF quadrupole integral (q_direct2D, verbatim) ----
def solve_eN(nu, etilde):
    return brentq(lambda x: x*float(np.asarray(nu(x)).ravel()[0]) - etilde, 1e-12, 1e10,
                  xtol=1e-15, rtol=8.9e-16)
def q_direct2D(nu, etilde, vmax=400.0):
    eN = solve_eN(nu, etilde)
    def ig(mu, v):
        D = eN*eN + v**4 + 2.0*eN*v*v*mu
        if D <= 0: return 0.0
        nv = float(np.asarray(nu(math.sqrt(D))).ravel()[0])
        return (nv-1.0)*(eN*(3*mu-5*mu**3) + v*v*(1-3*mu*mu))
    val, _ = integrate.dblquad(ig, 0.0, vmax, lambda v: -1.0, lambda v: 1.0,
                               epsabs=1e-12, epsrel=1e-10)
    return abs(1.5*val)

eta_anchor = 2.0                        # DHF published anchor point
eta_solar  = GEXT / A0                  # actual solar-circle external field ~2.48

print(f"Cassini pass requires q < {Q_PASS:.4f}  (ceiling {Q2_CEIL:.1e}, prefactor {PREF(A0):.3e})")
print(f"solar-circle external field eta = GEXT/a0 = {eta_solar:.3f}\n")
print(f"{'kernel':<22}{'class':<14}{'q(eta=2)':>10}{'q(solar)':>10}{'Q2/ceil(solar)':>16}{'verdict':>9}")
rows = [("RouteA/MS08", nu_routeA, "exp"), ("mu=1-e^-y", nu_muexp, "exp"),
        ("FC tanh(y/2)", nu_FC, "exp"), ("mu5", nu_mun(5), "sharp"), ("mu10", nu_mun(10), "sharp")]
for nm, nu, cls in rows:
    q2 = q_direct2D(nu, eta_anchor); qs = q_direct2D(nu, eta_solar)
    ratio = qs * PREF(A0) / Q2_CEIL
    verdict = "PASS" if qs < Q_PASS else "FAIL"
    print(f"{nm:<22}{cls:<14}{q2:>10.4f}{qs:>10.4f}{ratio:>16.2f}{verdict:>9}")

# guard: reproduce the committed RouteA anchor q(2)=0.221
qa = q_direct2D(nu_routeA, 2.0)
print(f"\n[guard] RouteA q(eta=2) = {qa:.4f}  (committed anchor 0.221; match={abs(qa/0.221-1)<0.02})")
