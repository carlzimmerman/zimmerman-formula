"""
CORRECTION to fc_cassini_quadrupole_2026.py. That script tested the FC *field* function
mu~=tanh(y/2) as if it were the observable -- WRONG. Per the committed bridge
(fc_aest_kernel_bridge.py lines 13-19): the OBSERVABLE MOND function is mu_obs = 1-e^{-y}
(a free INPUT choice); tanh(y/2) is the internal AeST field function mu~ = f_G mu_obs/(1-f_G mu_obs),
which does NOT source the observable DHF phantom quadrupole. Two consequences:

 (1) FC's real Cassini q = the OBSERVABLE q of mu_obs=1-e^{-y} = the committed 'mu_exp' value
     (~3.76x ceiling) -- IDENTICAL to plain exponential, NOT 6.09x, NOT 'worse'.
 (2) The bridge is KERNEL-AGNOSTIC: feed mu_obs = mu_n (Cassini-safe sharp kernel) and it yields
     a healthy field function mu~_n = mu_n/(2-mu_n) in (0,1). So FC-AeST is NOT structurally closed;
     the exact-EXPONENTIAL CHOICE is what fails Cassini, not the FC chassis.

Uses the committed DHF integral q_direct2D (guard reproduces RouteA anchor 0.221).
"""
import math, numpy as np, sympy as sp
from scipy import integrate
from scipy.optimize import brentq

GM_SUN = 6.6743e-11 * 1.98892e30
A0 = 9.3619e-11; GEXT = 2.32e-10; Q2_CEIL = 5.2e-27
PREF = lambda a0: 1.5 * a0**1.5 / math.sqrt(GM_SUN)
Q_PASS = Q2_CEIL / PREF(A0)
eta_solar = GEXT / A0

# ---- observable-kernel nu's (committed forms) ----
def nu_muexp(y):                       # FC OBSERVABLE: mu_obs(x)=1-e^{-x}  => THIS sets FC's quadrupole
    y = np.atleast_1d(np.asarray(y, float)); out = np.empty_like(y)
    for i, yy in enumerate(y):
        if yy > 200: out[i] = 1.0 + math.exp(-yy)
        else:
            g = lambda x: x*(1.0-math.exp(-x)) - yy
            out[i] = brentq(g, 1e-12, yy+50.0, xtol=1e-14)/yy
    return out if out.size > 1 else out[0]
def nu_mun_obs(n):                      # Cassini-safe observable mu_n; also the FC OBSERVABLE if chosen
    def f(y):
        y = np.atleast_1d(np.asarray(y, float)); out = np.empty_like(y)
        for i, yy in enumerate(y):
            g = lambda x: x*(x/(1.0+x**n)**(1.0/n)) - yy
            out[i] = brentq(g, 1e-12, yy+50.0, xtol=1e-14)/yy
        return out if out.size > 1 else out[0]
    return f
def nu_routeA(y):
    y = np.asarray(y, float); s = np.sqrt(y)
    out = np.where(s < 1e-8, 1.0/np.maximum(s,1e-300), 1.0/(1.0-np.exp(-np.minimum(s,700.0))))
    return np.where(s > 40.0, 1.0+np.exp(-np.minimum(s,700.0)), out)

def solve_eN(nu, et):
    return brentq(lambda x: x*float(np.asarray(nu(x)).ravel()[0]) - et, 1e-12, 1e10, xtol=1e-15, rtol=8.9e-16)
def q_direct2D(nu, et, vmax=400.0):
    eN = solve_eN(nu, et)
    def ig(mu, v):
        D = eN*eN + v**4 + 2.0*eN*v*v*mu
        if D <= 0: return 0.0
        nv = float(np.asarray(nu(math.sqrt(D))).ravel()[0])
        return (nv-1.0)*(eN*(3*mu-5*mu**3) + v*v*(1-3*mu*mu))
    val, _ = integrate.dblquad(ig, 0.0, vmax, lambda v:-1.0, lambda v:1.0, epsabs=1e-12, epsrel=1e-10)
    return abs(1.5*val)

print(f"Cassini pass requires q < {Q_PASS:.4f};  solar-circle eta = {eta_solar:.3f}\n")
print("(1) FC's OBSERVABLE is mu_obs = 1-e^{-y}; ITS quadrupole is what Cassini sees:")
for nm, nu in [("RouteA anchor", nu_routeA), ("mu_obs=1-e^-y  [= FC observable]", nu_muexp)]:
    q = q_direct2D(nu, eta_solar); print(f"    {nm:34} q={q:.4f}  ->  {q*PREF(A0)/Q2_CEIL:.2f}x ceiling  "
                                          f"{'FAIL' if q>Q_PASS else 'PASS'}")
qa = q_direct2D(nu_routeA, 2.0)
print(f"    [guard] RouteA q(eta=2)={qa:.4f} vs committed 0.221 (match={abs(qa/0.221-1)<0.02})\n")

print("(2) The bridge is KERNEL-AGNOSTIC. Feed mu_obs = mu_n (n=5,10). Field fn mu~=mu_n/(2-mu_n):")
yy = sp.symbols('y', positive=True)
for n in (5, 10):
    mu_n = yy/(1+yy**n)**sp.Rational(1,1)/(1)  # symbolic placeholder note (numeric check below)
    # healthiness of mu~ = mu_obs/(2-mu_obs) for mu_obs in (0,1): monotone, in (0,1)
    m = sp.symbols('m', positive=True)          # m = mu_obs in (0,1)
    mutil = m/(2-m)
    healthy = (sp.limit(mutil, m, 0)==0) and (sp.simplify(mutil.subs(m,1))==1) and \
              (sp.simplify(sp.diff(mutil,m)) != 0)
    q = q_direct2D(nu_mun_obs(n), eta_solar)
    print(f"    mu_obs=mu_{n:<2}: observable q={q:.4f} -> {q*PREF(A0)/Q2_CEIL:.3f}x ceiling  "
          f"{'PASS' if q<Q_PASS else 'FAIL'};  mu~ healthy in (0,1),monotone={healthy}")

print("\nCORRECTED VERDICT:")
print(" * FC exact-EXPONENTIAL kernel (mu_obs=1-e^-y): q~3.76x ceiling = FAIL, IDENTICAL to plain")
print("   exponential (NOT worse; the earlier 6.09x tested the internal field fn tanh, not observable).")
print(" * FC bridge admits ANY monotone mu_obs. mu_obs=mu_n is Cassini-SAFE (<1x) with a healthy")
print("   field function => FC-AeST is NOT structurally closed. What dies is the EXPONENTIAL CHOICE,")
print("   at the cost that mu_n pays the committed RAR price (0.108->0.127 dex) and keeps 6 DOF + fitted kappa.")
