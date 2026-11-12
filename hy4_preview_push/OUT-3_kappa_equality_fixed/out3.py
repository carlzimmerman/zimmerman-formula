#!/usr/bin/env python3
"""
LANE OUT-3 (EQUALITY-FIXED): does the tau-reparametrization / leaf-volume degeneracy,
with the clock's rest rate fixed by the vacuum, OUTPUT kappa = 1/2?

This script is the SYMPY/NUM leg. It:
  1. derives the exact cold-charge profile of the framework's own halo (law S),
  2. defines the settle-down radius r_sd (where the halo's cold density returns to the
     vacuum's own cold-charge density, which the new normalization fixes to rho_Lambda),
  3. computes  K := (halo's enclosed cold charge) / (cosmic share)  at r_sd,
  4. reports the number, and whether it is 1/2.

Nothing here is fitted. Law S, g_N = g^2/(g+a0), is the framework's own static limit
(CLOSURE.md 2026-11-05 s1; V3_FULL_PICTURE s2).

kappa = 1/2 FITTED; not theory closed. Footings never pooled. Cold dark energy is a
gravitating field component, never a particle.
"""
import json
import sympy as sp

# ----------------------------------------------------------------------
# 0. symbols
# ----------------------------------------------------------------------
x, u, a0, G, Mb, r, rhoL = sp.symbols(
    'x u a0 G M_b r rho_L', positive=True)

# ----------------------------------------------------------------------
# 1. Law S in dimensionless form.
#    x := g/a0 (observed), u := g_N/a0 (Newtonian).  Spherical AQUAL with
#    mu(s) = s/(1+s) integrates exactly to  u = x^2/(1+x).
# ----------------------------------------------------------------------
u_of_x = x**2 / (1 + x)
# cold (excess) pull g_c = g - g_N, in units of a0:
gc_of_x = sp.simplify(x - u_of_x)          # = x/(1+x)
print("u(x)      =", sp.simplify(u_of_x))
print("g_c/a0(x) =", sp.simplify(gc_of_x))
assert sp.simplify(gc_of_x - x/(1+x)) == 0

# ----------------------------------------------------------------------
# 2. Enclosed cold charge  M_c(r) = r^2 g_c / G.
#    With r^2 = G M_b / (a0 u)  (definition of u), show  M_c = M_b / x.
# ----------------------------------------------------------------------
r2_of_x = G*Mb/(a0*u_of_x)
Mc = sp.simplify(r2_of_x * (a0*gc_of_x) / G)
print("M_c(x)    =", sp.simplify(Mc))
assert sp.simplify(Mc - Mb/x) == 0, "M_c = M_b/x failed"
MC_OF_X = Mb/x

# ----------------------------------------------------------------------
# 3. Cold density  rho_c = (1/(4 pi r^2)) dM_c/dr.
#    Do it properly: r -> x map, chain rule.
# ----------------------------------------------------------------------
# u = G Mb/(a0 r^2)  =>  du/dr = -2u/r ;  du/dx = x(2+x)/(1+x)^2
du_dx = sp.simplify(sp.diff(u_of_x, x))
du_dr = sp.simplify(du_dx * sp.Symbol('dxdr'))
dxdr = sp.symbols('dxdr', positive=False)
dxdr_val = sp.simplify((-2*u_of_x/r) / du_dx)
print("dx/dr     =", sp.simplify(dxdr_val))

rho_c = sp.simplify((1/(4*sp.pi*r**2)) * sp.diff(MC_OF_X, x) * dxdr_val)
rho_c = sp.simplify(sp.powsimp(rho_c, force=True))
print("rho_c     =", sp.simplify(rho_c))
# expected closed form:
rho_c_expected = Mb*(1+x)/(2*sp.pi*r**3*x*(2+x))
print("rho_c (closed form) =", sp.simplify(rho_c_expected))
assert sp.simplify(rho_c - rho_c_expected) == 0, "rho_c closed form failed"

# ----------------------------------------------------------------------
# 4. Settle-down radius r_sd :  rho_c(r_sd) = rho_Lambda.
#    (The new normalization fixes the vacuum's cold-charge density to rho_Lambda;
#     the halo is a redistribution of it, so its outer boundary is where its own
#     density returns to the vacuum value.)
# ----------------------------------------------------------------------
Xi = sp.symbols('Xi', positive=True)   # Xi := rho_L G^{3/2} Mb^{1/2} / a0^{3/2}
# substitute r^3 = [G Mb (1+x)/(a0 x^2)]^{3/2} into rho_c = rhoL
r3 = (G*Mb*(1+x)/(a0*x**2))**sp.Rational(3, 2)
eq = sp.simplify(Mb*(1+x)/(2*sp.pi*x*(2+x)) / r3 - rhoL)
eq_s = sp.simplify(sp.powsimp(eq, force=True))
print("\nsettle-down equation (rho_c = rho_L):", sp.simplify(eq_s))

# dimensionless reduction:  x^2 / ((2+x) sqrt(1+x)) = 2 pi Xi
Xi_expr = rhoL*G**sp.Rational(3, 2)*sp.sqrt(Mb)/a0**sp.Rational(3, 2)
lhs = x**2/((2+x)*sp.sqrt(1+x))
# verify the reduction symbolically
sub_eq = sp.simplify(
    (Mb*(1+x)/(2*sp.pi*x*(2+x)) / r3 / rhoL) * (2*sp.pi*Xi_expr) - lhs/Xi_expr*Xi_expr
)
# do it cleanly: rho_c/rhoL expressed with Xi
rc_over_rhoL = sp.simplify(
    sp.powsimp((Mb*(1+x)/(2*sp.pi*x*(2+x))) / r3 / rhoL, force=True))
print("rho_c/rho_L =", sp.simplify(rc_over_rhoL))
print("2 pi Xi     =", sp.simplify(2*sp.pi*Xi_expr))
# rho_c/rho_L  should equal  lhs / (2 pi Xi)   with  lhs = x^2/((2+x) sqrt(1+x))
target = lhs / (2*sp.pi*Xi_expr)
print("check reduction (rho_c/rho_L - lhs/(2 pi Xi)):",
      sp.simplify(rc_over_rhoL - target))
assert sp.simplify(rc_over_rhoL - target) == 0, "Xi reduction failed"
# so the settle-down condition rho_c = rho_L is exactly  lhs = 2 pi Xi
print("settle-down condition:  x^2/((2+x) sqrt(1+x)) = 2 pi Xi,"
      "  Xi = rho_L G^(3/2) sqrt(M_b)/a0^(3/2)")

# ----------------------------------------------------------------------
# 5. K(x) := M_c(r_sd) / M_Lambda(r_sd)
# ----------------------------------------------------------------------
ML = sp.Rational(4, 3)*sp.pi*rhoL*r**3
K = sp.simplify((MC_OF_X / ML).subs(r**3, r3))
# at the match point rho_c = rhoL, so r3 is pinned; eliminate rhoL using the match
K_of_x = sp.simplify(
    sp.Rational(3, 2)*(2+x)/(1+x))
# verify: use rho_c = rhoL  =>  rhoL = Mb(1+x)/(2 pi r^3 x (2+x))
rhoL_at = Mb*(1+x)/(2*sp.pi*r**3*x*(2+x))
K_check = sp.simplify(MC_OF_X/(sp.Rational(4, 3)*sp.pi*rhoL_at*r**3))
print("\nK(x)       =", sp.simplify(K_check))
assert sp.simplify(K_check - K_of_x) == 0, "K(x) formula failed"

print("K(x -> 0)  =", sp.limit(K_of_x, x, 0, '+'))
print("K(x -> oo) =", sp.limit(K_of_x, x, sp.oo))
K_lo = sp.limit(K_of_x, x, sp.oo)     # saturated branch
K_hi = sp.limit(K_of_x, x, 0, '+')    # isothermal branch
print("K range    = [%s, %s]" % (K_lo, K_hi))

# is 1/2 in the range?
in_range = sp.simplify(sp.Rational(1, 2) - K_lo)
print("1/2 - K_min =", in_range, " -> 1/2 in range?", sp.simplify(in_range) >= 0)
assert sp.simplify(K_lo - sp.Rational(3, 2)) == 0
assert sp.simplify(K_hi - 3) == 0

# small-x expansion: K = 3 - (3/2) x + O(x^2)
ser = sp.series(K_of_x, x, 0, 3).removeO()
print("K small-x  =", sp.expand(ser))

# ----------------------------------------------------------------------
# 6. Branch profiles (the load-bearing "n" of rho ~ r^-n).
# ----------------------------------------------------------------------
A, rr = sp.symbols('A r', positive=True)
# saturated: g_c -> a0  =>  M_c = a0 r^2/G  =>  rho_c = a0/(2 pi G r)   (n = 1)
Mc_sat = a0*rr**2/G
rho_sat = sp.simplify(sp.diff(Mc_sat, rr)/(4*sp.pi*rr**2))
print("\nsaturated  rho_c =", rho_sat, " (n = 1)")
assert sp.simplify(rho_sat - a0/(2*sp.pi*G*rr)) == 0
# isothermal: M_c = sqrt(G Mb a0) r / G  => rho_c = sqrt(G Mb a0)/(4 pi G r^2)  (n = 2)
Mc_iso = sp.sqrt(G*Mb*a0)*rr/G
rho_iso = sp.simplify(sp.diff(Mc_iso, rr)/(4*sp.pi*rr**2))
print("isothermal rho_c =", rho_iso, " (n = 2)")

# generic n: rho = A/r^n, match A/r^n = rhoL  =>  K = 3/(3-n)
n = sp.symbols('n')
Mn = sp.integrate(4*sp.pi*rr**2 * A/rr**n, (rr, 0, rr))
MLn = sp.Rational(4, 3)*sp.pi*rhoL*rr**3
Kn = sp.simplify(Mn/MLn)
Kn = sp.simplify(Kn.subs(rhoL, A/rr**n))
print("generic n  K     =", sp.simplify(Kn), " -> K(n=1)=%s K(n=2)=%s"
      % (sp.simplify(Kn.subs(n, 1)), sp.simplify(Kn.subs(n, 2))))

# ----------------------------------------------------------------------
# 7. The Lambda-balance (turnaround) variant:  g_c = (8 pi G rhoL/3) r
#    Claim to test: is the resulting K = 2 law-content, or a tautology?
# ----------------------------------------------------------------------
Mgen = sp.symbols('M_gen', positive=True)   # ANY enclosed mass
# Gauss: g_c = G M / r^2 ; balance: G M/r^2 = (8 pi G rhoL/3) r
M_from_balance = sp.solve(sp.Eq(G*Mgen/rr**2, sp.Rational(8, 3)*sp.pi*G*rhoL*rr), Mgen)[0]
ML_bal = sp.Rational(4, 3)*sp.pi*rhoL*rr**3
print("\nturnaround: M/M_Lambda =", sp.simplify(M_from_balance/ML_bal),
      "   (independent of the law -> tautology)")

# ----------------------------------------------------------------------
# 8. NUMBERS: solve x_sd and K for a mass grid, both footings.
# ----------------------------------------------------------------------
CC = 2.99792458e8
GG = 6.67430e-11
MSUN = 1.98892e30
FOOT = {"canonical": 9.3603e-11, "alt": 1.1312e-10}   # V3_FULL_PICTURE header

def solve_x(Xi_val):
    """solve x^2/((2+x) sqrt(1+x)) = 2 pi Xi for x>0"""
    f = sp.lambdify(x, lhs, 'math')
    lo, hi = 1e-18, 1e6
    tgt = 2*3.141592653589793*Xi_val
    for _ in range(200):
        mid = (lo*hi)**0.5 if hi/lo > 1.0000001 else lo
        if f(mid) < tgt:
            lo = mid
        else:
            hi = mid
        if hi/lo < 1.0000001:
            break
    return (lo*hi)**0.5

rows = []
for footing, a0v in FOOT.items():
    # the framework's own closure ties rho_Lambda to a0 at kappa = 1/2:
    rhoL_v = 4*a0v**2/(GG*CC**2)
    for name, Mbs in [("dwarf 1e8", 1e8), ("LSB 1e9", 1e9), ("MW 6e10", 6e10),
                      ("group 1e12", 1e12), ("cluster 1e14", 1e14),
                      ("Coma 1e15", 1e15)]:
        Mbv = Mbs*MSUN
        Xi_v = rhoL_v*GG**1.5*Mbv**0.5/a0v**1.5
        xs = solve_x(Xi_v)
        Kv = 1.5*(2+xs)/(1+xs)
        rsd2 = (GG*Mbv*(1+xs)/(a0v*xs**2))
        rsd = rsd2**0.5
        rM = (GG*Mbv/a0v)**0.5
        rows.append(dict(footing=footing, name=name, M_b_Msun=Mbs,
                         Xi=Xi_v, x_sd=xs, K=Kv, kappa_from_K3=Kv/3.0,
                         r_sd_kpc=rsd/3.0857e19, r_M_kpc=rM/3.0857e19,
                         r_sd_over_rM=rsd/rM))

print("\n%-10s %-13s %10s %10s %10s %12s %12s" %
      ("footing", "system", "x_sd", "K", "K/3", "r_sd/r_M", "r_sd [kpc]"))
for R in rows:
    print("%-10s %-13s %10.4e %10.6f %10.6f %12.4g %12.4g" %
          (R["footing"], R["name"], R["x_sd"], R["K"], R["kappa_from_K3"],
           R["r_sd_over_rM"], R["r_sd_kpc"]))

Ks = [R["K"] for R in rows]
out = dict(
    lane="OUT-3 (EQUALITY-FIXED)",
    question="does the clock/leaf degeneracy + vacuum normalization of Q output kappa = 1/2?",
    K_exact_formula="K(x) = (3/2)*(2+x)/(1+x),  x = g(r_sd)/a0",
    K_saturated_limit=float(K_lo),
    K_isothermal_limit=float(K_hi),
    K_range=[float(K_lo), float(K_hi)],
    half_in_range=False,
    K_numeric_min=min(Ks), K_numeric_max=max(Ks),
    kappa_if_K_over_3=[min(Ks)/3.0, max(Ks)/3.0],
    tau_reparametrization_note="Q -> f'(tau) Q under tau -> f(tau); leaf measure fixed; "
                               "vacuum sets rho_tau(Q_vac) = rho_Lambda",
    rows=rows,
    turnaround_K=2.0,
    turnaround_is_tautology=True,
)
with open("out3.json", "w") as f:
    json.dump(out, f, indent=2)
print("\nK numeric range over 7 dex in M_b: [%.6f, %.6f]" % (min(Ks), max(Ks)))
print("K/3 range (would be kappa):        [%.6f, %.6f]" % (min(Ks)/3, max(Ks)/3))
print("1/2 in [K_min, K_max]?  NO  (K >= 3/2 always)")
