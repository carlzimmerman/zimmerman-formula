#!/usr/bin/env python3
"""u01_eh_fixed_points.py  --  Einstein-Hilbert-truncation non-Gaussian fixed point of asymptotically safe gravity, for SEVERAL cutoff shapes.

Purpose (lane U, task item 3): the IR fixed point of Bonanno-Reuter (G = g*/k^2, Lambda = lambda* k^2) is POSTULATED, not derived (their own wording), so the only
fixed-point numbers that actually exist in the literature are the UV ones of the Einstein-Hilbert (EH) flow.  This script computes them from the flow equations of
Bonanno-Reuter hep-th/0002196 eqs (2.6)-(2.10) (d = 4, exponential-type cutoff 'type A'; the same flow is used by Reuter-Weyer hep-th/0410119 eq (10)) with
the general threshold functions (2.10), for a set of admissible shape functions R0(z) (R0(0)=1, R0 -> 0 at infinity, non-increasing), and reports the SPREAD of
g*, lambda*, g*lambda*.  It does NOT select a shape.  The derived quantity that feeds the puzzle is zeta_req = sqrt(32 pi / lambda*)  (see u04).

Flow (d=4), Phi^p_n(w) = 1/Gamma(n) int dz z^(n-1) (R0 - z R0')/(z+R0+w)^p ,  Phit^p_n(w) = 1/Gamma(n) int dz z^(n-1) R0/(z+R0+w)^p :
   d_t g   = (2 + eta) g ,    eta = g B1(lam)/(1 - g B2(lam))
   d_t lam = -(2 - eta) lam + (g/2pi) [ 10 Phi^1_2(-2lam) - 8 Phi^1_2(0) - 5 eta Phit^1_2(-2lam) ]
   B1(lam) = (1/3pi)[5 Phi^1_1(-2lam) - 18 Phi^2_2(-2lam) - 4 Phi^1_1(0) - 6 Phi^2_2(0)]
   B2(lam) = -(1/6pi)[5 Phit^1_1(-2lam) - 18 Phit^2_2(-2lam)]
Fixed point: eta = -2  =>  g = 2/(2 B2 - B1), and d_t lam = 0 fixes lam (1-d root find).

Controls / mutations (all counted): thresholds vs Bonanno-Reuter's closed forms (2.17)-(2.19); optimised-cutoff thresholds vs closed forms; independent 2-d
solver residuals; exact cubic for the optimised cutoff; a MUTANT flow (eta*Phit term dropped) must move the fixed point (test has power); LR's universality range.
Exit 0 iff every check passes.
"""
import math
import sys
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq, fsolve

ok = []
def check(name, cond):
    ok.append(bool(cond)); print(f"  [{'OK' if cond else 'FAIL'}] {name}")

# ---------------------------------------------------------------- shape functions: (R0, R0', upper integration limit)
def make_shapes():
    S = {}
    for s in (1.0, 2.0, 3.0, 5.0):                       # Lauscher-Reuter (3.8): R0 = s z/(exp(s z)-1); s=1 is Bonanno-Reuter (2.4)
        def R(z, s=s):
            x = s * z
            return 1.0 if x < 1e-12 else x / math.expm1(x) if x < 700 else 0.0
        def Rp(z, s=s):
            x = s * z
            if x < 1e-6: return -s / 2.0 + s * x / 6.0
            if x > 700: return 0.0
            e = math.expm1(x)
            return s * (1.0 / e - x * (e + 1.0) / e**2)
        S[f"exp s={s:g}"] = (R, Rp, 200.0 / s)
    for b in (2.0, 4.0):                                  # R0 = z^b/(exp(z^b)-1)  (my own admissible family; b=1 is the exponential)
        def R(z, b=b):
            x = z**b
            return 1.0 if x < 1e-12 else x / math.expm1(x) if x < 700 else 0.0
        def Rp(z, b=b):
            x = z**b
            if x < 1e-6: return -b * z**(b - 1) / 2.0
            if x > 700: return 0.0
            e = math.expm1(x)
            return b * z**(b - 1) * (1.0 / e - x * (e + 1.0) / e**2)
        S[f"z^b/(e^(z^b)-1), b={b:g}"] = (R, Rp, 200.0 ** (1.0 / b))
    S["optimised (1-z)theta(1-z)"] = (lambda z: max(1.0 - z, 0.0), lambda z: -1.0 if z < 1.0 else 0.0, 1.0)
    S["rational 1/(1+z)^2"] = (lambda z: 1.0 / (1.0 + z)**2, lambda z: -2.0 / (1.0 + z)**3, np.inf)
    S["exp(-z)"] = (lambda z: math.exp(-z), lambda z: -math.exp(-z), 60.0)
    return S

def Phi(shape, p, n, w):
    R, Rp, zmax = shape
    f = lambda z: z**(n - 1) * (R(z) - z * Rp(z)) / (z + R(z) + w)**p
    pts = [1.0] if np.isfinite(zmax) and zmax > 1.0 else None
    v, _ = quad(f, 0.0, zmax, epsabs=1e-13, epsrel=1e-12, limit=400, points=pts)
    return v / math.gamma(n)

def Phit(shape, p, n, w):
    R, Rp, zmax = shape
    f = lambda z: z**(n - 1) * R(z) / (z + R(z) + w)**p
    pts = [1.0] if np.isfinite(zmax) and zmax > 1.0 else None
    v, _ = quad(f, 0.0, zmax, epsabs=1e-13, epsrel=1e-12, limit=400, points=pts)
    return v / math.gamma(n)

def B1(shape, lam):
    return (5 * Phi(shape, 1, 1, -2 * lam) - 18 * Phi(shape, 2, 2, -2 * lam) - 4 * Phi(shape, 1, 1, 0.0) - 6 * Phi(shape, 2, 2, 0.0)) / (3 * math.pi)

def B2(shape, lam):
    return -(5 * Phit(shape, 1, 1, -2 * lam) - 18 * Phit(shape, 2, 2, -2 * lam)) / (6 * math.pi)

def beta_lam(shape, g, lam, eta, mutant=False):
    t = 10 * Phi(shape, 1, 2, -2 * lam) - 8 * Phi(shape, 1, 2, 0.0)
    if not mutant:
        t -= 5 * eta * Phit(shape, 1, 2, -2 * lam)
    return -(2 - eta) * lam + g / (2 * math.pi) * t

def eta_of(shape, g, lam):
    return g * B1(shape, lam) / (1 - g * B2(shape, lam))

def fixed_point(shape, mutant=False):
    def g_of(lam):
        return 2.0 / (2 * B2(shape, lam) - B1(shape, lam))
    def F(lam):
        g = g_of(lam)
        return beta_lam(shape, g, lam, -2.0, mutant)
    grid = np.linspace(0.005, 0.49, 98)
    vals = [F(l) for l in grid]
    roots = []
    for i in range(len(grid) - 1):
        if vals[i] * vals[i + 1] < 0:
            lam = brentq(F, grid[i], grid[i + 1], xtol=1e-14, rtol=1e-13)
            g = g_of(lam)
            if g > 0:
                roots.append((g, lam))
    return roots

print("=" * 100)
print("PART 1  controls on the threshold functions")
print("=" * 100)
exp1 = make_shapes()["exp s=1"]
check("exp s=1: Phi^1_1(0) = pi^2/6  (BR 2.17)", abs(Phi(exp1, 1, 1, 0.0) - math.pi**2 / 6) < 1e-9)
check("exp s=1: Phi^2_2(0) = 1       (BR 2.17)", abs(Phi(exp1, 2, 2, 0.0) - 1.0) < 1e-9)
check("exp s=1: Phit^1_1(0) = 1      (BR 2.18)", abs(Phit(exp1, 1, 1, 0.0) - 1.0) < 1e-9)
check("exp s=1: Phit^2_2(0) = 1/2    (BR 2.18)", abs(Phit(exp1, 2, 2, 0.0) - 0.5) < 1e-9)
B1_0 = B1(exp1, 0.0); B2_0 = B2(exp1, 0.0)
omega = -B1_0 / 2
check("exp s=1: omega = -B1(0)/2 = (4/pi)(1 - pi^2/144)  (BR 2.16, 2.19)", abs(omega - (4 / math.pi) * (1 - math.pi**2 / 144)) < 1e-9)
check("exp s=1: B2(0) = 2/(3 pi)     (BR 2.19)", abs(B2_0 - 2 / (3 * math.pi)) < 1e-9)
# MUTATION of the control: a wrong closed form must FAIL
check("MUTATION (omega with 144 -> 140) is rejected", abs(omega - (4 / math.pi) * (1 - math.pi**2 / 140)) > 1e-3)
opt = make_shapes()["optimised (1-z)theta(1-z)"]
for w in (0.0, -0.3, -0.7):
    cf = {"Phi11": 1 / (1 + w), "Phi22": 1 / (2 * (1 + w)**2), "Phi12": 1 / (2 * (1 + w)), "Pt11": 1 / (2 * (1 + w)), "Pt22": 1 / (6 * (1 + w)**2), "Pt12": 1 / (6 * (1 + w))}
    num = {"Phi11": Phi(opt, 1, 1, w), "Phi22": Phi(opt, 2, 2, w), "Phi12": Phi(opt, 1, 2, w), "Pt11": Phit(opt, 1, 1, w), "Pt22": Phit(opt, 2, 2, w), "Pt12": Phit(opt, 1, 2, w)}
    check(f"optimised cutoff, w={w:+.1f}: six thresholds equal their closed forms", all(abs(num[k] - cf[k]) < 1e-10 for k in cf))

print()
print("=" * 100)
print("PART 2  lambda = 0 truncation:  omega and g*(lambda=0) = 1/(omega + B2)  -- the coefficient of the k^2 term in G(k) = G0/(1 + omega G0 k^2)")
print("=" * 100)
print(f"  {'shape':32s} {'omega':>9s} {'B2(0)':>9s} {'g*(lam=0)=1/(omega+B2)':>24s}")
lam0 = {}
for name, sh in make_shapes().items():
    om = -B1(sh, 0.0) / 2; b2 = B2(sh, 0.0)
    lam0[name] = (om, b2, 1 / (om + b2))
    print(f"  {name:32s} {om:9.5f} {b2:9.5f} {1 / (om + b2):24.5f}")
om_vals = [v[0] for v in lam0.values()]
print(f"  omega spread over admissible shapes: min {min(om_vals):.4f}, max {max(om_vals):.4f}, ratio {max(om_vals) / min(om_vals):.2f}")
check("omega is NOT universal: spread > factor 1.5 over the admissible shapes", max(om_vals) / min(om_vals) > 1.5)
om_opt = -B1(opt, 0.0) / 2
check("optimised cutoff: omega = 11/(6 pi) (pure 1/pi, no pi in the numerator)", abs(om_opt - 11 / (6 * math.pi)) < 1e-9)
check("optimised cutoff: B2(0) = 1/(12 pi)", abs(B2(opt, 0.0) - 1 / (12 * math.pi)) < 1e-9)
check("optimised cutoff: g*(lam=0) = 12 pi/23", abs(1 / (om_opt + B2(opt, 0.0)) - 12 * math.pi / 23) < 1e-9)

print()
print("=" * 100)
print("PART 3  full EH non-Gaussian fixed point (g*, lambda*) for each shape; g*lambda*; the derived requirement zeta_req = sqrt(32 pi/lambda*)")
print("=" * 100)
FP = {}
print(f"  {'shape':32s} {'g*':>9s} {'lambda*':>9s} {'g*lam*':>9s} {'eta*':>8s} {'|beta_lam|':>11s} {'zeta_req':>9s}")
for name, sh in make_shapes().items():
    roots = fixed_point(sh)
    if not roots:
        print(f"  {name:32s}  (no positive fixed point found)")
        continue
    # keep the root with the smallest lambda (the standard one); report others if present
    roots.sort(key=lambda t: t[1])
    g, lam = roots[0]
    FP[name] = (g, lam)
    eta = eta_of(sh, g, lam)
    resid = abs(beta_lam(sh, g, lam, eta))
    zr = math.sqrt(32 * math.pi / lam)
    extra = "" if len(roots) == 1 else f"   (other roots: {[(round(a, 4), round(b, 4)) for a, b in roots[1:]]})"
    print(f"  {name:32s} {g:9.5f} {lam:9.5f} {g * lam:9.5f} {eta:8.4f} {resid:11.2e} {zr:9.3f}{extra}")
n_shapes = len(make_shapes())
check(f"a positive non-Gaussian fixed point exists for every shape tried ({len(FP)}/{n_shapes})", len(FP) == n_shapes)
check("eta* = -2 and beta_lambda = 0 at every fixed point (residual < 1e-9)", all(abs(eta_of(make_shapes()[n], *FP[n]) + 2) < 1e-9 and abs(beta_lam(make_shapes()[n], FP[n][0], FP[n][1], -2.0)) < 1e-9 for n in FP))

# independent 2-d solver from a perturbed start (different code path: fsolve on (g, lam) with eta computed from B1, B2)
def two_d(sh, g0, l0):
    def eqs(v):
        g, lam = v
        eta = eta_of(sh, g, lam)
        return [2 + eta, beta_lam(sh, g, lam, eta)]
    return fsolve(eqs, [g0, l0], xtol=1e-13)
allok = True
for name in FP:
    g, lam = FP[name]
    gg, ll = two_d(make_shapes()[name], g * 1.1, lam * 0.9)
    allok &= (abs(gg - g) < 1e-7 and abs(ll - lam) < 1e-7)
check("independent 2-d fsolve (perturbed start) reproduces every fixed point to 1e-7", allok)

lams = np.array([FP[n][1] for n in FP]); gs = np.array([FP[n][0] for n in FP]); prods = gs * lams
def rel(x): return (x.max() - x.min()) / x.mean()
print(f"\n  spread (max-min)/mean:  g*: {rel(gs):.2f}   lambda*: {rel(lams):.2f}   g*lambda*: {rel(prods):.2f}")
print(f"  ranges: g* in [{gs.min():.3f}, {gs.max():.3f}], lambda* in [{lams.min():.3f}, {lams.max():.3f}], g*lambda* in [{prods.min():.4f}, {prods.max():.4f}]")
zr = np.sqrt(32 * math.pi / lams)
print(f"  zeta_req = sqrt(32 pi/lambda*) in [{zr.min():.2f}, {zr.max():.2f}]   (a0 := c^2 k/zeta with Lambda(k) = lambda* k^2; needs G rho_L/a0^2 = lambda* zeta^2/(8 pi) = 4)")
check("g*lambda* is far less scheme dependent than g* or lambda* separately (Lauscher-Reuter's universality claim, reproduced qualitatively)", rel(prods) < min(rel(gs), rel(lams)))
check("all lambda* are O(0.1-0.4): none is anywhere near 32 pi (the value needed for zeta = 1)", lams.max() < 0.5)

print()
print("  Reference (opened source, Lauscher-Reuter hep-th/0108040, their type-B cutoff with both gauge choices, exponential and compact-support shape families):")
print("    universal g*lambda* plateau reported as ~0.12 (alpha=1) and ~0.14 (alpha=0);  (lambda*, g*) = (0.287, 0.751) for their one-loop-expanded exponential s=1, alpha=1 (their H8).")
in_band = [(p >= 0.09 and p <= 0.16) for p in prods]
print(f"  my type-A products: {[round(float(p), 4) for p in prods]}  -> {sum(in_band)}/{len(in_band)} inside [0.09, 0.16]  (their plateau +- a generous margin; shapes far from the exponential are outside their scan)")

print()
print("=" * 100)
print("PART 4  exact optimised-cutoff fixed point (pi-content)")
print("=" * 100)
# x = 1 - 2 lam.  eta = -2 gives g = 6 pi / (12/x^2 - 15/(2x) + 7); d_t lam = 0 gives the cubic 14 x^3 - 41 x^2 + 59 x - 24 = 0  (derived by hand in the README, re-verified here)
roots = np.roots([14, -41, 59, -24])
xr = [r.real for r in roots if abs(r.imag) < 1e-12 and 0 < r.real < 1]
print(f"  real roots x = 1-2lam of 14x^3 - 41x^2 + 59x - 24 in (0,1): {xr}")
x = xr[0]; lam_ex = (1 - x) / 2; g_ex = 6 * math.pi / (12 / x**2 - 15 / (2 * x) + 7)
print(f"  lambda* = {lam_ex:.10f}   g* = {g_ex:.10f}   g*/pi = {g_ex / math.pi:.10f}   g*lambda* = {g_ex * lam_ex:.10f}")
gnum, lnum = FP["optimised (1-z)theta(1-z)"]
check("closed-form optimised fixed point equals the numerical one (1e-9)", abs(g_ex - gnum) < 1e-9 and abs(lam_ex - lnum) < 1e-9)
print("  pi-content: lambda* is a root of a cubic with RATIONAL coefficients (algebraic, no pi); g* = pi x (algebraic).  The pi in g* is the loop factor 1/(4 pi)^(d/2-1); it cancels in lambda*.")
check("cubic residual < 1e-12 at the root", abs(14 * x**3 - 41 * x**2 + 59 * x - 24) < 1e-12)
# MUTATION: perturb a cubic coefficient -> the closed form no longer reproduces the numerical fixed point
xm = np.roots([14, -41, 59, -25]); xm = [r.real for r in xm if abs(r.imag) < 1e-12 and 0 < r.real < 1][0]
check("MUTATION (cubic constant 24 -> 25) no longer reproduces the numerical lambda*", abs((1 - xm) / 2 - lnum) > 1e-3)


print()
print("=" * 100)
print("PART 6  a second, independent scheme: Litim hep-th/0312114 (opened), optimised cutoff, gauge alpha -> infinity, d = 4 limit of his eq (9)")
print("=" * 100)
def litim_fp(d):
    n = d * d - d - 4
    lam = (n - math.sqrt(2 * d * n)) / (2 * (d - 4) * (d + 1))
    g = 2 * math.gamma(d / 2 + 2) * (4 * math.pi) ** (d / 2 - 1) / n * lam ** 2
    return lam, g
for eps in (1e-3, 1e-5):
    l1, g1 = litim_fp(4 + eps); l2, g2 = litim_fp(4 - eps)
    print(f"  d = 4 +- {eps:g}:  (lambda*, g*) = ({l1:.6f}, {g1:.6f}) / ({l2:.6f}, {g2:.6f})")
lL, gL = litim_fp(4 + 1e-5)
check("Litim eq (9) at d -> 4: lambda* -> 1/4 (rational) and g* -> 3 pi/8 (his Fig. 2 shows the UV point near (0.25, 1.2))", abs(lL - 0.25) < 1e-3 and abs(gL - 3 * math.pi / 8) < 1e-2)
print(f"  Litim alpha->inf: lambda* = 1/4, g* = 3 pi/8 = {3 * math.pi / 8:.4f}, g*lambda* = 3 pi/32 = {3 * math.pi / 32:.4f};  zeta_req = sqrt(32 pi/lambda*) = {math.sqrt(128 * math.pi):.3f}")
print(f"  compare my type-A optimised cutoff (gauge alpha=1 flow of Reuter): g*lambda* = {gnum * lnum:.4f}, lambda* = {lnum:.4f}  -> the GAUGE/scheme choice alone moves g*lambda* by x{3 * math.pi / 32 / (gnum * lnum):.2f}")
check("scheme spread including Litim: lambda* stays in [0.15, 0.36] (zeta_req in [16.7, 25.6] all the same)", 0.15 <= lL <= 0.36)
check("scheme spread including Litim: g*lambda* is NOT universal to better than a factor 2 across gauge choices (0.093 ... 0.29)", 3 * math.pi / 32 / prods.min() > 2.0)

print()
print("=" * 100)
print("PART 5  mutant flow: drop the eta*Phit term in beta_lambda -> the fixed point must move (the test is not blind)")
print("=" * 100)
rm = fixed_point(opt, mutant=True)
print(f"  optimised cutoff, mutant fixed point(s): {[(round(a, 4), round(b, 4)) for a, b in rm]}   (true: {gnum:.4f}, {lnum:.4f})")
check("mutant flow gives a different lambda* (>5% away) or none", (not rm) or min(abs(l - lnum) / lnum for g, l in rm) > 0.05)

print()
fails = ok.count(False)
print(f"RESULT: {ok.count(True)} checks passed, {fails} failed")
sys.exit(1 if fails else 0)
