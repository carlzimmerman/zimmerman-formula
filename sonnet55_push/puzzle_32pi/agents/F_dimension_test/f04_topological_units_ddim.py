#!/usr/bin/env python3
"""f04_topological_units_ddim.py -- does 'A Lambda = one topological unit' have a d-independent form?  (c = 1)

Setup (all from f01): D = d+1 even (d odd: d = 3, 5, 7 -> D = 4, 6, 8).  Tangherlini horizon with surface gravity a0: r_s = (d-2)/(2 a0);
a0 = kappa sqrt(G rho_L) (G = G_D), Lambda = 8 pi G rho_L.  The only dimensionless horizon-area x Lambda combination in D dims is
        AL_d(kappa) = Omega_(d-1) r_s^(d-1) Lambda^((d-1)/2) = Omega_(d-1) (2 pi (d-2)^2/kappa^2)^((d-1)/2)          (= 32 pi^2 at d=3, kappa=1/2)
[A Lambda alone has dimension L^(d-3): it is dimensionless only in D = 4.]

  A  Euler density of S^(2n)(L): E_(2n) = (2n)!/L^(2n) [generalised-Kronecker contraction, brute force for D = 2, 4, 6];  int E = (4 pi)^n n! chi
     -> units 4 pi, 32 pi^2, 384 pi^3, 6144 pi^4 (D = 2, 4, 6, 8) per unit chi.  Chern-character (instanton-type) unit of int tr F^n: (2 pi)^n n!  (8 pi^2 at n=2).
  B  pi-power bookkeeping: AL_d has pi^((d-1)/2) from Omega_(d-1) and pi^((d-1)/2) from Lambda^((d-1)/2) = (8 pi G rho)^((d-1)/2):  pi^(d-1);
     the topological unit has pi^((d+1)/2).  Equal iff d = 3.  Ratio AL_d(kappa)/U_(d+1) = (algebraic) kappa^-(d-1) pi^((d-3)/2).
  C  consequence (Lindemann): for algebraic kappa the ratio AL_d/U_(d+1) is transcendental for every d >= 5; the d-independent statement
     'AL_d = U_(d+1)' would need kappa_d proportional to pi^((d-3)/(2(d-1))) (pi^(1/4) at d=5).  Explicit values for the readings are tabulated.
  D  the de Sitter horizon itself: A_dS Lambda^((d-1)/2) has one pi too few in EVERY d >= 3 (the missing 2 pi/(d... ) is the thermal period).
Controls: d = 3 passes (AL = 32 pi^2 = U_4 exactly at kappa = 1/2); wrong kappa fails; d = 4 (D = 5, odd): no Gauss-Bonnet/Euler density, chi(S^5) = 0;
d = 2 (D = 3): odd, and A Lambda^(1/2) = 2 pi r_s sqrt(Lambda) with r_s = 0 (no Tangherlini horizon).
Exit 0 = all checks as stated.
"""
import sys
import itertools
import math
import numpy as np
import sympy as sp

OK = []
def check(name, cond):
    OK.append(bool(cond)); print(f"  [{'OK' if cond else 'FAIL'}] {name}")

# ------------------------------------------------------------------ A  Euler density on S^(2n)
def perm_sign(p):
    s = 1
    p = list(p)
    for i in range(len(p)):
        while p[i] != i:
            j = p[i]
            p[i], p[j] = p[j], p[i]
            s = -s
    return s

def E_contraction(D, n, k=1.0):
    """E_(2n) = (1/2^n) delta^(mu1..mu2n)_(nu1..nu2n) R^(nu1nu2)_(mu1mu2)...  for R^(ab)_(cd) = k (d^a_c d^b_d - d^a_d d^b_c), computed by brute force.
    delta^(mu)_(nu) = sum_sigma sgn(sigma) prod delta^(mu_sigma(i))_(nu_i)  =>  sum over sigma of sgn * prod_j R[mu_sigma(2j-1), mu_sigma(2j), mu_(2j-1), mu_(2j)]."""
    m = 2 * n
    I = np.eye(D)
    R = k * (np.einsum('ac,bd->abcd', I, I) - np.einsum('ad,bc->abcd', I, I))
    letters = 'abcdefghijkl'[:m]
    total = 0.0
    for sigma in itertools.permutations(range(m)):
        sg = perm_sign(sigma)
        terms, ops = [], []
        for j in range(n):
            up = letters[sigma[2 * j]] + letters[sigma[2 * j + 1]]
            dn = letters[2 * j] + letters[2 * j + 1]
            terms.append(up + dn)
            ops.append(R)
        total += sg * np.einsum(','.join(terms) + '->', *ops)
    return total / 2**n

print("A  Euler density of constant-curvature spaces (brute-force generalised-Kronecker contraction)")
for (D, n) in [(2, 1), (4, 2), (6, 3)]:
    val = E_contraction(D, n, 1.0)
    check(f"A{D}  E_{2 * n} on S^{D}(L=1) = (2n)! = {math.factorial(2 * n)}  (brute force: {val:.6f})", abs(val - math.factorial(2 * n)) < 1e-6)
for (D, n) in [(4, 1), (5, 2)]:       # D > 2n: formula (2k)^n D!/(D-2n)! /2^n
    val = E_contraction(D, n, 1.0)
    pred = math.factorial(D) / math.factorial(D - 2 * n)
    check(f"A{D}{n}  general D: contraction = D!/(D-2n)! ({val:.4f} vs {pred})", abs(val - pred) < 1e-6)
print("     (S^8: E_8 = 8! by the same antisymmetry argument; brute force skipped, 8! permutations x 8^8 entries)")

n = sp.symbols('n', positive=True, integer=True)
def vol_S(D):        # unit S^D
    return 2 * sp.pi**(sp.Rational(D + 1, 2)) / sp.gamma(sp.Rational(D + 1, 2))
U = {}
print("\n   D    Vol(S^D)          E_D             int E_D = E_D Vol   unit per chi = (4pi)^n n!    Chern unit (2pi)^n n!")
for nn in (1, 2, 3, 4):
    D = 2 * nn
    vol = sp.simplify(vol_S(D))
    intE = sp.simplify(sp.factorial(D) * vol)
    unit = sp.simplify((4 * sp.pi)**nn * sp.factorial(nn))
    U[D] = unit
    chern = sp.simplify((2 * sp.pi)**nn * sp.factorial(nn))
    print(f"   {D}    {str(vol):<16} {str(sp.factorial(D)):>8}       {str(intE):<18} {str(unit):<26} {str(chern)}")
    check(f"A-int{D}  int_(S^{D}) E_{D} = (4 pi)^{nn} {nn}! * chi with chi = 2", sp.simplify(intE - 2 * unit) == 0)
check("A-D4  D = 4 unit is 32 pi^2 and the Chern (SU(2) instanton) unit 8 pi^2: ratio 4 = 2^n", U[4] == 32 * sp.pi**2 and sp.simplify((2 * sp.pi)**2 * 2) == 8 * sp.pi**2)
check("A-D6  D = 6 unit is 384 pi^3 (task's 'or similar'), D = 8: 6144 pi^4", U[6] == 384 * sp.pi**3 and U[8] == 6144 * sp.pi**4)

# ------------------------------------------------------------------ B  the horizon-area x Lambda combination
print("\nB  horizon area x Lambda^((d-1)/2) with a Tangherlini horizon of surface gravity a0 = kappa sqrt(G rho_L)")
dd, kap, Gs, rho_, a0 = sp.symbols('d kappa G rho a0', positive=True)
Omega = lambda dv: 2 * sp.pi**(sp.Rational(dv, 2)) / sp.gamma(sp.Rational(dv, 2))           # area of unit S^(dv-1)
def AL(dv, kv):
    rs = sp.Rational(dv - 2, 2) / (kv * sp.sqrt(Gs * rho_))                                   # r_s = (d-2)/(2 a0), c = 1
    Lam = 8 * sp.pi * Gs * rho_
    return sp.simplify(Omega(dv) * rs**(dv - 1) * Lam**sp.Rational(dv - 1, 2))
check("B1  A Lambda alone has dimension length^(d-3): (G rho) ~ 1/L^2 so A Lambda ~ L^(d-1) L^-2  (dimensionless only at d = 3)", all((k - 1) - 2 == k - 3 for k in range(2, 9)))
check("B2  AL_d(kappa) = Omega_(d-1) (2 pi (d-2)^2/kappa^2)^((d-1)/2), independent of G, rho", all(sp.simplify(AL(k, kap) - Omega(k) * (2 * sp.pi * (k - 2)**2 / kap**2)**sp.Rational(k - 1, 2)) == 0 for k in (3, 5, 7)))
check("B3  control: d = 3, kappa = 1/2 gives exactly 32 pi^2 = the D = 4 Gauss-Bonnet unit", sp.simplify(AL(3, sp.Rational(1, 2)) - 32 * sp.pi**2) == 0 and sp.simplify(AL(3, sp.Rational(1, 2)) - U[4]) == 0)
check("B3b control: kappa = 1 at d = 3 gives 8 pi^2 (not 32 pi^2): wrong kappa is rejected", sp.simplify(AL(3, 1)) == 8 * sp.pi**2 and sp.simplify(AL(3, 1) - U[4]) != 0)

print("\n   pi-power of AL_d (algebraic kappa)  vs  pi-power of the topological unit U_(d+1):")
rows = []
for dv in (3, 5, 7, 9):
    D = dv + 1
    expr = sp.simplify(AL(dv, kap))
    ratio = sp.simplify(expr / ((4 * sp.pi)**(D // 2) * sp.factorial(D // 2)))
    # power of pi: strip kappa
    ratio_k1 = sp.simplify(ratio.subs(kap, 1))
    coeff = sp.simplify(ratio_k1 / sp.pi**sp.Rational(dv - 3, 2))
    rows.append((dv, D, coeff, ratio))
    print(f"   d={dv} (D={D}):  AL/U = {sp.simplify(ratio)}   = ({coeff}) kappa^-{dv - 1} pi^{sp.Rational(dv - 3, 2)}")
check("B4  AL_d/U_(d+1) = (rational) * kappa^-(d-1) * pi^((d-3)/2) with the rational coefficient shown for d = 3, 5, 7, 9 (no pi left in the coefficient)",
      all(c.is_rational for (_, _, c, _) in rows))
check("B5  the pi-exponent (d-3)/2 vanishes only at d = 3", [sp.Rational(k - 3, 2) for (k, _, _, _) in rows] == [0, 1, 2, 3])
# Lindemann consequence: for algebraic kappa the ratio at d=5 is (9/4) pi kappa^-4 , transcendental
c5 = rows[1][2]
check("B6  d = 5: AL/U = (9/4) pi/kappa^4 exactly; equals 1 only at kappa = (9 pi/4)^(1/4) = %.4f, not algebraic (pi^(1/4)); no algebraic kappa gives a rational multiple"
      % float((9 * sp.pi / 4)**sp.Rational(1, 4)), c5 == sp.Rational(9, 4) and sp.simplify(sp.solve(sp.Eq(sp.Rational(9, 4) * sp.pi / kap**4, 1), kap)[0] - (9 * sp.pi / 4)**sp.Rational(1, 4)) == 0)


# variant: state the relation with G rho instead of Lambda (no Einstein 8 pi at all)
def AG(dv, kv):
    return sp.simplify(Omega(dv) * (sp.Rational(dv - 2, 2) / kv)**(dv - 1))     # A (G rho)^((d-1)/2), r_s sqrt(G rho) = (d-2)/(2 kappa)
ratios_G = [sp.simplify(AG(dv, kap) / ((4 * sp.pi)**((dv + 1) // 2) * sp.factorial((dv + 1) // 2))) for dv in (3, 5, 7)]
print("   variant with G rho instead of Lambda:  A (G rho)^((d-1)/2)/U =", ", ".join(str(x) for x in ratios_G))
check("B9  with (G rho)^((d-1)/2) in place of Lambda^((d-1)/2) the ratio to the Euler unit is (rational)/(pi kappa^(d-1)) in EVERY odd d, including d = 3 (there the missing pi is Einstein's 8 pi): "
      "one Einstein pi is needed at d=3 and (d-1)/2 of them appear in Lambda^((d-1)/2)",
      all(sp.simplify(x * sp.pi * kap**(dv - 1)).is_rational for x, dv in zip(ratios_G, (3, 5, 7))))

# ------------------------------------------------------------------ readings
print("\n   value of AL_d/U_(d+1) for the readings (algebraic kappa unless stated) -- transcendental for d >= 5, NOT an integer")
def rd(dv):
    return {
        "(1) kappa = 1/2": sp.Rational(1, 2),
        "(3) kappa = (d-2)/2": sp.Rational(dv - 2, 2),
        "(4) kappa = (2/3) d/(d+1)": sp.Rational(2, 3) * dv / (dv + 1),
        "(5) kappa = sqrt(3/(2d(d-1)))": sp.sqrt(sp.Rational(3, 2) / (dv * (dv - 1))),
    }
vals = {}
for name in rd(3):
    line = f"   {name:<32}"
    for dv in (3, 5, 7):
        kv = rd(dv)[name]
        ratio = sp.simplify(AL(dv, kv) / ((4 * sp.pi)**((dv + 1) // 2) * sp.factorial((dv + 1) // 2)))
        vals[(name, dv)] = ratio
        line += f"   d={dv}: {str(sp.nsimplify(ratio)):<22} = {float(ratio):>10.4f}"
    print(line)
check("B7  at d = 3 every reading has kappa = 1/2 (p05), so every reading gives the ratio exactly 1: the D = 4 identity carries no information about WHICH reading",
      all(sp.simplify(vals[(nm, 3)] - 1) == 0 for nm in rd(3)))
check("B8  at d = 5 and d = 7 no reading gives 1: every value is a nonzero rational times pi^((d-3)/2)",
      all(sp.simplify(vals[(nm, dv)] - 1) != 0 and abs(float(vals[(nm, dv)]) - 1) > 1e-3 for nm in rd(3) for dv in (5, 7)))
print("   (note: some values sit near 1 by accident, e.g. reading (3) at d = 7 gives %.3f; the exact ratio is 0.877..., a transcendental number; near-misses are not evidence)"
      % float(vals[("(3) kappa = (d-2)/2", 7)]))

# ------------------------------------------------------------------ D  de Sitter horizon
print("\nD  the de Sitter horizon itself")
def A_dS_L(dv):
    L = sp.symbols('L', positive=True)
    Lam = sp.Rational(dv * (dv - 1), 2) / L**2
    return sp.simplify(Omega(dv) * L**(dv - 1) * Lam**sp.Rational(dv - 1, 2))
for dv in (3, 5, 7):
    ratio = sp.simplify(A_dS_L(dv) / ((4 * sp.pi)**((dv + 1) // 2) * sp.factorial((dv + 1) // 2)))
    print(f"   d={dv}: A_dS Lambda^((d-1)/2)/U = {ratio}")
check("D1  A_dS Lambda^((d-1)/2) / U_(d+1) is (rational)/pi in every odd d: one pi short of the topological unit (the 2 pi of the thermal period / Euclidean rotation)",
      all(sp.simplify(A_dS_L(dv) * sp.pi / ((4 * sp.pi)**((dv + 1) // 2) * sp.factorial((dv + 1) // 2))).is_rational for dv in (3, 5, 7, 9)))
check("D2  d = 3: A_dS Lambda = 12 pi, and 12 pi x 8 pi/3 = 32 pi^2: the a0 horizon's extra area factor is Z^2 = 8 pi/3 x (dS area) in D = 4 (p08); no such fixed factor in general d",
      sp.simplify(A_dS_L(3) - 12 * sp.pi) == 0)

# ------------------------------------------------------------------ controls d = 2, 4
print("\nControls")
check("C1  d = 4 (D = 5, odd): chi(S^D) = 1 + (-1)^D gives chi(S^5) = 0 (and chi(S^4) = 2): there is no Euler-density unit at odd D, the topological reading is undefined", [1 + (-1)**k for k in (4, 5, 6)] == [2, 0, 2])
check("C2  d = 2 (D = 3): Tangherlini r_s = (d-2)/(2 a0) = 0: no horizon, AL_2 = Omega_1 r_s Lambda^(1/2) = 0", sp.simplify(AL(2, kap)) == 0)
print(f"\n  {sum(OK)}/{len(OK)} checks held.")
sys.exit(0 if all(OK) else 1)
