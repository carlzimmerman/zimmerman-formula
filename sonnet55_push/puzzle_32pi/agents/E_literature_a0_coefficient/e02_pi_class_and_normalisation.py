#!/usr/bin/env python3
"""e02_pi_class_and_normalisation.py -- what KIND of number each published coefficient is, and what the missing step would have to be.

Definitions (c = G = hbar = 1):  H = H_Lambda = sqrt(Lambda/3) = sqrt(8 pi rho_L / 3);  a0 = c H / Z  (Z as in the record);  kappa = a0 / sqrt(G rho_L)
=> kappa = sqrt(8 pi / 3) / Z.   The framework:  kappa = 1/2  <=>  Z^2 = 32 pi / 3.
PART A  'pi-class' table: for every published/derived coefficient, is Z, kappa^2, or a0^2 A_dS rational?   Only the framework (and the record's forced kernel kappa = 1)
        has kappa^2 in Q.  Every COMPUTED route has Z in Q (or Z in pi Q by fitting 2 pi).  Lemma B: integer powers of pi (the T = H/2pi, 4 pi r^2, 8 pi G bookkeeping
        of horizon thermodynamics) can never give kappa^2 in Q; it needs a half-integer power, i.e. a0^2 (not a0) linear in an area or a density.
PART C  Milgrom's 'naturalness' route (arXiv:2001.09729 sec III.A) and Xu's rho_DE = A0 a^2/G are the SAME object: kappa = 1/sqrt(|F0|) = 1/sqrt(A0).  The puzzle is |F0| = 4.
PART D  the window: which computed Z lie between sqrt(32 pi/3) and 2 pi;  Verlinde's 6 vs the framework: equal iff pi = 27/8.
PART E  the dS/conformal-group route (Milgrom 0810.4065, 1404.7661; Singh 2601.04290): the deep-MOND symmetry is blind to a0 (A0 scales out), so the group cannot fix xi.
Exit 0 = the algebra holds and the controls behave.
"""
import sys
import mpmath as mp
import sympy as sp

ok = []
def check(name, cond):
    ok.append(bool(cond)); print(f"  [{'OK' if cond else 'FAIL'}] {name}")

pi = sp.pi
Zfw = sp.sqrt(32 * pi / 3)
Zforced = sp.sqrt(8 * pi / 3)
def kappa2(Z): return sp.simplify(8 * pi / (3 * Z**2))
def a02A_over_c4(Z): return sp.simplify(4 * pi / Z**2)          # a0^2 * A_dS with A_dS = 4 pi L^2, L = 1/H  =>  4 pi / Z^2
def is_Q(x): return sp.simplify(x).is_rational is True
def cls(x):
    x = sp.simplify(x)
    if is_Q(x): return "Q"
    if is_Q(x / pi): return "pi Q"
    if is_Q(x * pi): return "Q/pi"
    if is_Q(x / pi**2): return "pi^2 Q"
    if is_Q(x * pi**2): return "Q/pi^2"
    return "mixed"

cands = [
    ("Verlinde 1611.02269 (a0/6)",                    sp.Integer(6),                   "computed"),
    ("Milgrom 1999 / Smolin / K-K / Pikhitsa (T-T_L)", sp.Rational(1, 2),              "computed"),
    ("Milgrom 1999 alt functional a dT/da",           sp.Integer(1),                   "computed"),
    ("Milgrom brane, n = 2  (a0 = n c^2/l0)",         sp.Rational(1, 2),               "computed"),
    ("Milgrom brane, n = 3",                          sp.Rational(1, 3),               "computed"),
    ("van Putten 1411.2665 (2/(1+2 pi sqrt2))",       (1 + 2 * pi * sp.sqrt(2)) / 2,   "computed"),
    ("Milgrom empirical 2 pi (2001.09729 eq 3)",      2 * pi,                          "empirical"),
    ("HMN 1005.3537 a_c = a_L/2pi (beta = 1/pi)",     2 * pi,                          "inserted"),
    ("Kiselev-Timofeev N_G (eq 28)",                  2 * pi,                          "inserted"),
    ("record forced kernel kappa = 1",                Zforced,                         "record"),
    ("framework kappa = 1/2",                         Zfw,                             "record (FITTED)"),
]
print("PART A  which variable is rational?   (Z = c H_Lambda / a0)")
print(f"  {'candidate':<46}{'Z':>9}  {'origin':<16}{'Z class':<9}{'kappa^2':<9}{'a0^2 A_dS':<10}")
res = {}
for nm, Z, org in cands:
    k2 = kappa2(Z); a2A = a02A_over_c4(Z)
    res[nm] = (cls(Z**2), cls(k2), cls(a2A))
    print(f"  {nm:<46}{float(Z):>9.4f}  {org:<16}{cls(Z**2):<9}{cls(k2):<9}{cls(a2A):<10}")
computed = [nm for nm, Z, org in cands if org == "computed"]
check("A1  every COMPUTED route has Z^2 in Q (Z rational) or is mixed (van Putten); none has kappa^2 in Q",
      all(res[nm][1] != "Q" for nm in computed))
check("A2  the only candidates with kappa^2 rational AND a0^2*A_dS rational are the record's two (forced kernel and framework)",
      [nm for nm in res if res[nm][1] == "Q" and res[nm][2] == "Q"] == ["record forced kernel kappa = 1", "framework kappa = 1/2"])
check("A3  framework: a0^2 A_dS / c^4 = 3/8 exactly (no pi);   Verlinde: pi/9;   T-T_L family: 16 pi;   Milgrom 2pi: 1/pi",
      sp.simplify(a02A_over_c4(Zfw) - sp.Rational(3, 8)) == 0 and sp.simplify(a02A_over_c4(sp.Integer(6)) - pi / 9) == 0
      and sp.simplify(a02A_over_c4(sp.Rational(1, 2)) - 16 * pi) == 0 and sp.simplify(a02A_over_c4(2 * pi) - 1 / pi) == 0)

# ------------------------------------------------------------------------------ Lemma B (pi parity)
print("\nPART B  pi-parity lemma:  a0 = q (2 pi)^j c H_Lambda, q algebraic, j integer  =>  kappa^2 = (8 pi/3) q^2 (2 pi)^(2j) is transcendental")
mp.mp.dps = 60
def alg_deg(val, maxdeg=6, maxcoeff=1000):
    p = mp.findpoly(val, maxdeg, maxcoeff=maxcoeff, tol=mp.mpf(10)**-40)
    return None if p is None else len(p) - 1
rows = []
for j2 in (-4, -3, -2, -1, 0, 1, 2, 3):                         # j = j2/2 : integer j for even j2, half-integer for odd
    j = mp.mpf(j2) / 2
    k2 = (8 * mp.pi / 3) * (2 * mp.pi)**(2 * j)                 # q = 1
    deg = alg_deg(k2)
    rows.append((j2, deg))
    print(f"      j = {float(j):>5.1f}   kappa^2 = (8 pi/3)(2 pi)^{float(2*j):.0f}  ->  algebraic of degree {deg if deg else 'none found (deg<=6, coeff<=1000)'}")
check("B1  for every INTEGER j (even j2) no integer relation of degree <= 6 (coefficients <= 1000) exists for kappa^2 (as Lindemann demands: pi is transcendental)",
      all(deg is None for j2, deg in rows if j2 % 2 == 0))
check("B2  the relation exists exactly when the power of pi in kappa^2 vanishes, i.e. j = -1/2 (a0^2 proportional to 1/(2 pi), i.e. to 1/A or to G rho): j2 = -1 -> degree 1",
      dict(rows)[-1] == 1 and all(deg is None for j2, deg in rows if j2 != -1))
check("B3  the framework is that case:  a0 = (sqrt3/4)(2 pi)^(-1/2) c H_Lambda  (q = sqrt3/4, j = -1/2)  gives kappa = 1/2 exactly",
      sp.simplify(sp.sqrt(8 * pi / 3) / (1 / ((sp.sqrt(3) / 4) / sp.sqrt(2 * pi))) - sp.Rational(1, 2)) == 0)

# ------------------------------------------------------------------------------ PART C
print("\nPART C  Milgrom's naturalness route and Xu's rho_DE = A0 a^2/G  are the framework's relation with an unfixed constant")
F0, Lam = sp.symbols('F0 Lambda', real=True)
a0s, A0 = sp.symbols('a0 A0', positive=True)
# action (c = G = 1):  S = (1/16 pi) int sqrt(-g) [R - 2 Lambda] + int sqrt(-g) F0 a0^2 ...  (F normalised as in Milgrom's eq 16, prefactor c^4/G, EH term carrying 1/16 pi)
Lam_from_F0 = sp.solve(sp.Eq(-2 * Lam / (16 * pi), F0 * a0s**2), Lam)[0]
check("C1  a constant F0 in Milgrom's l^-2 F(l^2 Q) (with a0 = c^2/l, EH term R/16 pi G) acts as Lambda = -8 pi F0 a0^2", sp.simplify(Lam_from_F0 + 8 * pi * F0 * a0s**2) == 0)
f = sp.Symbol('f', positive=True)
rho_F = (Lam_from_F0 / (8 * pi)).subs(F0, -f)                    # rho_Lambda = f a0^2
kappa_F = sp.simplify(a0s / sp.sqrt(rho_F))
check("C2  kappa = a0/sqrt(G rho_Lambda) = 1/sqrt(|F0|):  |F0| = 1 is the record's forced kernel (kappa = 1);  kappa = 1/2 is |F0| = 4 = 2^2", sp.simplify(kappa_F - 1 / sp.sqrt(f)) == 0 and sp.simplify((1 / sp.sqrt(f)).subs(f, 4) - sp.Rational(1, 2)) == 0)
rho_Xu = A0 * a0s**2
check("C3  Xu (2203.05606 eq 38) rho_DE = A0 a^2/G: same statement with A0 = |F0|;  A0 ~ 'unity' leaves kappa = 1/sqrt(A0) free;  the puzzle is A0 = 4",
      sp.simplify(a0s / sp.sqrt(rho_Xu) - 1 / sp.sqrt(A0)) == 0)
print("      |F0| = Lambda/(8 pi a0^2) = 3 Z^2/(8 pi) for each candidate (EH normalised as R/16 pi; if F rides with the 1/16 pi the number is 16 pi times larger):")
for nm, Z, org in cands:
    F0v = sp.simplify(3 * Z**2 / (8 * pi))
    print(f"        {nm:<46}|F0| = {float(F0v):>8.4f}")
check("C4  framework |F0| = 4 exactly;  Verlinde 6: 27/(2 pi) = 4.297;  Milgrom 2 pi: 3 pi/2 = 4.712;  T-T_L family: 3/(32 pi) = 0.0298",
      sp.simplify(3 * Zfw**2 / (8 * pi) - 4) == 0 and sp.simplify(3 * 36 / (8 * pi) - 27 / (2 * pi)) == 0
      and sp.simplify(3 * (2 * pi)**2 / (8 * pi) - 3 * pi / 2) == 0 and sp.simplify(3 * sp.Rational(1, 4) / (8 * pi) - 3 / (32 * pi)) == 0)
Zlo, Zhi = 4.5, 6.3
check("C5  the data-preferred range Z in [%.1f, %.1f] (footing-dependent, record p03) corresponds to |F0| in [%.2f, %.2f]: O(1) in this normalisation, so 'naturalness' is consistent with the data at O(1) but cannot select 4"
      % (Zlo, Zhi, 3 * Zlo**2 / (8 * float(pi)), 3 * Zhi**2 / (8 * float(pi))), 2.0 < 3 * Zlo**2 / (8 * float(pi)) and 3 * Zhi**2 / (8 * float(pi)) < 5.0)
check("C6  CONTROL: the T-T_L family (Z = 1/2) would need |F0| = 0.03, ~100x below the data band [2.4, 4.7]: its coefficient is not a near-miss",
      3 * 0.25 / (8 * float(pi)) < 0.05)

# ------------------------------------------------------------------------------ PART D
print("\nPART D  the window [sqrt(32 pi/3), 2 pi]  and Verlinde vs framework")
lo, hi = float(Zfw), float(2 * pi)
inwin = [(nm, float(Z)) for nm, Z, org in cands if org in ("computed",) and lo <= float(Z) <= hi]
print(f"      window Z in [{lo:.4f}, {hi:.4f}];  computed candidates inside: {inwin}")
check("D1  the only COMPUTED coefficient inside [sqrt(32 pi/3), 2 pi] is Verlinde's Z = 6", [nm.split()[0] for nm, _ in inwin] == ["Verlinde"])
sol = sp.solve(sp.Eq(36, 32 * sp.Symbol('p') / 3), sp.Symbol('p'))[0]
check("D2  Verlinde Z^2 = 36 equals the framework's 32 pi/3 iff pi = 27/8 = %.4f  (real pi differs by %.1f%%): Z_V/Z_fw = %.4f" % (float(sol), 100 * abs(float(sol) - float(pi)) / float(pi), 6 / lo),
      sol == sp.Rational(27, 8) and abs(6 / lo - 1.0365) < 5e-4)
check("D3  kappa_Verlinde = sqrt(2 pi/27) = %.4f lies between Milgrom-empirical sqrt(2/(3 pi)) = %.4f and the framework 1/2, i.e. inside the same window in kappa" %
      (float(sp.sqrt(2 * pi / 27)), float(sp.sqrt(2 / (3 * pi)))), float(sp.sqrt(2 / (3 * pi))) < float(sp.sqrt(2 * pi / 27)) < 0.5)
dd = sp.symbols('d', positive=True)
fV = (dd - 1) * (dd - 2) / (dd - 3)
crit = sp.solve(sp.diff(fV, dd), dd)
dmin = [c for c in crit if c.is_real and c > 3][0]
fmin = sp.simplify(fV.subs(dd, dmin))
check("D4  CONTROL: Verlinde's (d-1)(d-2)/(d-3) = (d-3) + 2/(d-3) + 3 >= 3 + 2 sqrt2 = %.4f (min at d = 3 + sqrt2 = %.3f) > sqrt(32 pi/3) = %.4f: no real dimension d > 3 ever gives the framework's Z, integer d >= 4 gives 6, 6, 6.67, 7.5, ..." %
      (float(fmin), float(dmin), lo),
      sp.simplify(fmin - (3 + 2 * sp.sqrt(2))) == 0 and float(fmin) > lo and all(float(fV.subs(dd, n)) > lo for n in range(4, 12)))

# ------------------------------------------------------------------------------ PART E
print("\nPART E  the dS / conformal-group route is blind to a0")
rr, A0s = sp.symbols('r A0', positive=True)
phi = sp.Function('phi')
psi = sp.Function('psi')
# spherically symmetric deep-MOND operator  (1/r^2) d/dr( r^2 |phi'| phi' )  (phi' > 0);  substitute phi = sqrt(A0) psi
op = lambda u: sp.diff(rr**2 * sp.diff(u(rr), rr)**2, rr) / rr**2
lhs = sp.simplify(op(lambda x_: sp.sqrt(A0s) * psi(x_)) / A0s)
check("E1  substituting phi = sqrt(A0) psi turns  div(|grad phi| grad phi) = 4 pi A0 rho  into an A0-free equation: the deep-MOND symmetry group (dilatations, 10-parameter conformal group = SO(4,1)) is the same for every a0",
      sp.simplify(lhs - op(psi)) == 0)
print("      => the isomorphism 'conformal group of R^3 = isometry group of dS_4' relates two symmetry groups; it contains no relation between a0 and l_dS; xi in a0 = c^2/(xi l_dS) stays a matched O(1) number (Singh 2601.04290 sec 4).")
check("E2  CONTROL: the Newtonian operator (1/r^2) d/dr(r^2 phi') is NOT invariant under phi -> sqrt(A0) phi with A0 fixed by the source, so the A0-blindness is a property of the deep-MOND (cubic) sector, as Milgrom's scale-invariance argument says",
      sp.simplify(sp.diff(rr**2 * sp.diff(sp.sqrt(A0s) * psi(rr), rr), rr) / rr**2 / A0s - sp.diff(rr**2 * sp.diff(psi(rr), rr), rr) / rr**2) != 0)

print(f"\n  {sum(ok)}/{len(ok)} checks held.")
sys.exit(0 if all(ok) else 1)
