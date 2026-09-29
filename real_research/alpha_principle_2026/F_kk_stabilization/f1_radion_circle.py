#!/usr/bin/env python3
"""F1 -- Family A: 5D on S^1, Casimir energy + 5D vacuum energy rho_5, Einstein-frame radion potential.
Pre-registered in F0_PREREGISTRATION.md (written before this script was run).
Units hbar = c = 1.  l_P^2 = G_4.  Observed vacuum energy rho_L: rho_L l_P^4 = x/(8 pi).
Run:   python3 f1_radion_circle.py            (real run)
       python3 f1_radion_circle.py --mutate   (control: drop the Einstein-frame factor; must FAIL)
"""
import sys, math
import sympy as sp
import mpmath as mp

MUTATE = "--mutate" in sys.argv
CHECKS = []
mp.mp.dps = 40
ALPHA = 1 / 137.035999177
R_NEED = 2 / math.sqrt(ALPHA)          # R/l_P needed by alpha_1 = 4 l_P^2/R^2 (AH6)


def check(tag, ok, detail=""):
    CHECKS.append((tag, bool(ok)))
    print(f"  [{'PASS' if ok else 'FAIL'}] {tag} {detail}")


print("=" * 100)
print("F1 radion potential on S^1 (Casimir + 5D vacuum energy) -- mode: " + ("MUTATE CONTROL (no Einstein-frame factor)" if MUTATE else "REAL RUN"))
print("=" * 100)

# ---------------------------------------------------------------- A1 Casimir coefficient, two independent routes
print("\nA1  Casimir energy of one periodic real dof on a circle of radius R=1 (per 4D volume, circle included)")
zeta5 = mp.zeta(5)
closed = -3 * zeta5 / (64 * mp.pi ** 6)
# route 1: zeta-regularised Coleman-Weinberg sum  E = (1/(64 pi^2 R^4)) sum_{n!=0} n^4 ln n^2 ; sum n^4 ln n = -zeta'(-4)
zp = mp.zeta(-4, derivative=1)
route1 = (1 / (64 * mp.pi ** 2)) * (-4 * zp)
print(f"    closed form -3 zeta(5)/(64 pi^6)         = {mp.nstr(closed, 15)}")
print(f"    zeta'(-4) route (mode sum, no Poisson)   = {mp.nstr(route1, 15)}")
check("A1 two routes agree", abs(route1 - closed) < mp.mpf(10) ** -30)
# twisted dof: E(a) = -3/(64 pi^6) sum_k cos(2 pi k a)/k^5 versus Hurwitz-zeta route
a = mp.mpf("0.3")
poisson = -3 / (64 * mp.pi ** 6) * mp.nsum(lambda k: mp.cos(2 * mp.pi * k * a) / k ** 5, [1, mp.inf])
hurwitz = (1 / (64 * mp.pi ** 2)) * (-2) * (mp.zeta(-4, a, 1) + mp.zeta(-4, 1 - a, 1))
print(f"    twisted a=0.3: Poisson {mp.nstr(poisson, 15)}   Hurwitz-zeta {mp.nstr(hurwitz, 15)}")
check("A1' twisted-dof formula agrees with Hurwitz-zeta mode sum", abs(poisson - hurwitz) < mp.mpf(10) ** -25)

# ---------------------------------------------------------------- A2 Einstein-frame potential
print("\nA2  Weyl rescaling to the 4D Einstein frame and the extremum")
R, R0, c = sp.symbols("R R0 c", positive=True)
rho5 = sp.symbols("rho5", real=True)
# ds5^2 = (R/R0)^(-1) g4 + R^2 dtheta^2 : sqrt(g5) R5 contains (R/R0)^(-2) * (R/R0)^(1) * (R/R0)^(1) * R4 -> R4 with unit coefficient
a_, b_ = sp.symbols("a b")
weyl = sp.simplify((4 * a_ + b_) - 2 * a_)                 # exponent of e^{sigma}: volume 4a+b, curvature -2a
sol_a = sp.solve(sp.Eq(weyl.subs(b_, -2 * a_), 0), a_)
check("A2a Einstein-frame condition 2a+b=0 is consistent (exponent of R4 coefficient vanishes for b=-2a)", sp.simplify(weyl.subs(b_, -2 * a_)) == 0)
U = 2 * sp.pi * R * rho5 - c / R ** 4           # energy per 4D volume in the 5D frame (c > 0: bosonic excess)
VE = (R0 / R) ** 2 * U if not MUTATE else U
dV = sp.diff(VE, R)
rho5_sol = sp.solve(sp.Eq(dV.subs(R, R0), 0), rho5)[0]
Vmin = sp.simplify(VE.subs(rho5, rho5_sol).subs(R, R0))
d2V = sp.simplify(sp.diff(VE, R, 2).subs(rho5, rho5_sol).subs(R, R0))
print(f"    extremum condition:  2 pi rho5 = {sp.simplify(2 * sp.pi * rho5_sol)}   (R=R0=R*)")
print(f"    V_E at the extremum = {Vmin};   V_E'' there = {d2V}")
check("A2b V_E(R*) = 5 c / R*^4", sp.simplify(Vmin - 5 * c / R0 ** 4) == 0)
check("A2c V_E''(R*) = -30 c/R*^6, i.e. sign(V'') = -sign(c)", sp.simplify(d2V + 30 * c / R0 ** 6) == 0)
print("    => c>0 (bosonic excess): rho5>0, V_min=+5c/R^4>0 (dS-type) but V''<0: a MAXIMUM (radion tachyon).")
print("       c<0 (fermionic excess): rho5<0, extremum is a MINIMUM but V=5c/R^4<0 (AdS4).  Sign theorem: no dS minimum from {rho5, Casimir}.")
theorem = (sp.simplify(Vmin - 5 * c / R0 ** 4) == 0) and (sp.simplify(d2V + 30 * c / R0 ** 6) == 0)
check("A2d sign theorem: sign(V_extremum)=sign(c) and sign(V'')=-sign(c), so V>0 <=> maximum", theorem)

# ---------------------------------------------------------------- A3 R* from the observed vacuum energy
print("\nA3  match |V(R*)| to the observed vacuum energy: R*/l_P = (40 pi |c| / x)^(1/4)")
c_light = 299792458.0
G = 6.67430e-11
hbar = 1.054571817e-34
H0 = 67.4e3 / 3.0856775814913673e22
OmL = 0.6847
Lam = 3 * OmL * H0 ** 2 / c_light ** 2
lP2 = G * hbar / c_light ** 3
lP = math.sqrt(lP2)
x = Lam * lP2
print(f"    x = Lambda l_P^2 = {x:.4e} (AH5 construction);  l_P = {lP:.4e} m")
c1 = float(3 * zeta5 / (64 * mp.pi ** 6))
rows = []
for DN in (+5, -4, -8, -16, -100):
    cc = DN * c1
    Rstar = (40 * math.pi * abs(cc) / x) ** 0.25
    al = 4 / Rstar ** 2
    kind = "max, dS-type (unstable radion)" if DN > 0 else "MIN but AdS (V<0)"
    rows.append((DN, Rstar, al, kind))
    print(f"    DN={DN:+4d}: R*/l_P = {Rstar:.3e}  ({Rstar * lP:.3e} m)  alpha_grav = 4 l_P^2/R*^2 = {al:.3e}   [{kind}]")
hit = [r for r in rows if abs(r[1] / R_NEED - 1) < 1e-3]
check("A3a no declared DN gives R*/l_P = 23.4125 within 1e-3", len(hit) == 0)
check("A3b R* is ~1e30 l_P (tens of microns... 1e-5 m scale), i.e. the dark-dimension scale Lambda^(-1/4) rather than 23 l_P",
      all(1e29 < r[1] < 1e31 for r in rows[:4]))
# exponent: alpha_grav ~ x^p
xs = sp.symbols("xs", positive=True)
cs = sp.symbols("cs", positive=True)
Rs = (40 * sp.pi * cs / xs) ** sp.Rational(1, 4)
alpha_x = sp.simplify(4 / Rs ** 2)
p_exp = sp.simplify(sp.diff(sp.log(alpha_x), xs) * xs)
print(f"    alpha_grav(x) = {alpha_x}  ->  d ln alpha/d ln x = {p_exp}")
check("A3c alpha_grav is EXACTLY a power x^(1/2) in x (exponent 1/2)", p_exp == sp.Rational(1, 2))
p_need = math.log(ALPHA) / math.log(x)
print(f"    AH5 says a pure power alpha = x^p would need p = {p_need:.5f}; this route gives 1/2  (mismatch factor {0.5 / p_need:.1f})")
check("A3d the exponent 1/2 is not the p=0.0176 that would fix alpha", abs(0.5 - p_need) > 0.4)

print("\nA3e  what R = 23.4125 l_P would demand of the vacuum energy")
for DN in (+5, -4):
    cc = abs(DN) * c1
    Vext = 5 * cc / R_NEED ** 4                     # in l_P^-4
    ratio = Vext / (x / (8 * math.pi))
    print(f"    |DN|={abs(DN)}: extremum energy 5c/R^4 = {Vext:.3e} l_P^-4  vs observed {x / (8 * math.pi):.3e}: ratio {ratio:.2e}  (cancellation of {math.log10(ratio):.1f} decades)")
check("A3e forcing R = 23.4 l_P needs a ~1e116-fold cancellation against another term (not forced)", 1e110 < 5 * c1 / R_NEED ** 4 / (x / (8 * math.pi)) < 1e120)

n_ok = sum(1 for _, o in CHECKS if o)
print("\n" + "=" * 100)
print(f"CHECKS: {n_ok}/{len(CHECKS)} passed")
print("VERDICT (Family A):")
print("  * PASS criterion (forced R = 23.4 l_P with a dS minimum) is NOT met: dS extremum is a maximum, the minimum is AdS, R* ~ x^(-1/4) ~ 1e30 l_P, alpha_grav ~ x^(1/2) ~ 1e-61.")
print("  * Not tested: twists/Scherk-Schwarz change c by O(1) factors only (c -> c*sum cos(2 pi k a)/k^5); R* moves by the 4th root; conclusion unchanged.")
sys.exit(0 if n_ok == len(CHECKS) else 1)
