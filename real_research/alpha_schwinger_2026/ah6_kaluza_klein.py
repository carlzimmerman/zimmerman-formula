#!/usr/bin/env python3
"""AH6 -- the Kaluza-Klein route to alpha.  Pre-registered in AH6_PREREGISTRATION.md (written before this script was run).

Units hbar = c = 1, Heaviside-Lorentz (alpha = e^2/(4 pi)).  kg_ below is the KK gauge parameter (NOT the framework's kappa = 1/2).
Run:   python3 ah6_kaluza_klein.py            (real run)
       python3 ah6_kaluza_klein.py --mutate   (control: a wrong reduction coefficient must FAIL K1)
"""
import sys
import math
import sympy as sp

MUTATE = "--mutate" in sys.argv
CHECKS = []
PI = math.pi
ALPHA = 1.0 / 137.035999177


def check(tag, ok, detail=""):
    CHECKS.append((tag, bool(ok)))
    print(f"  [{'PASS' if ok else 'FAIL'}] {tag} {detail}")


print("=" * 100)
print("AH6 Kaluza-Klein route to alpha -- mode: " + ("MUTATE CONTROL (wrong reduction coefficient)" if MUTATE else "REAL RUN"))
print("=" * 100)

# ------------------------------------------------------------------ K1: 5D Ricci scalar of the KK ansatz
t, x, y, z, w = sp.symbols("t x y z w", real=True)
kg = sp.symbols("kg", positive=True)
A = sp.Function("A")(x)                                       # nontrivial background: A_y(x)
X = [t, x, y, z, w]
# ds^2 = -dt^2 + dx^2 + dy^2 + dz^2 + (dw + kg A(x) dy)^2
g = sp.Matrix([[-1, 0, 0, 0, 0],
               [0, 1, 0, 0, 0],
               [0, 0, 1 + kg ** 2 * A ** 2, 0, kg * A],
               [0, 0, 0, 1, 0],
               [0, 0, kg * A, 0, 1]])
gi = sp.simplify(g.inv())
n = 5
Gam = [[[sum(gi[a, d] * (sp.diff(g[d, b], X[c]) + sp.diff(g[d, c], X[b]) - sp.diff(g[b, c], X[d])) for d in range(n)) / 2
         for c in range(n)] for b in range(n)] for a in range(n)]


def ricci(b, c):
    return sum(sp.diff(Gam[a][b][c], X[a]) - sp.diff(Gam[a][b][a], X[c])
               + sum(Gam[a][a][d] * Gam[d][b][c] - Gam[a][c][d] * Gam[d][b][a] for d in range(n)) for a in range(n))


R5 = sp.simplify(sum(gi[b, c] * ricci(b, c) for b in range(n) for c in range(n)))
Ap = sp.diff(A, x)
F2 = 2 * Ap ** 2                                              # F_{xy} = A', F_{mu nu}F^{mu nu} = 2 A'^2 (flat 4D)
coeff = sp.simplify(R5 / (kg ** 2 * F2))
print("\nK1  5D Ricci scalar of ds^2 = eta + (dw + kg A dy)^2 with A = A_y(x):")
print(f"     R_5 = {R5}")
print(f"     R_5 / (kg^2 F_{{mu nu}}F^{{mu nu}}) = {coeff}     (expected -1/4)")
expected = sp.Rational(-1, 2) if MUTATE else sp.Rational(-1, 4)
k1_ok = sp.simplify(coeff - expected) == 0
check("K1 R_5 = R_4 - (kg^2/4) F^2 (coefficient -1/4)", k1_ok, f"(tested against {expected})")

if MUTATE:
    print("\nMUTATE CONTROL: the tested coefficient was -1/2 instead of -1/4.")
    print(f"  K1 {'FAILED as required -- the control works' if not k1_ok else 'DID NOT FAIL -- the check has no power'}")
    sys.exit(0 if not k1_ok else 1)

# ------------------------------------------------------------------ K2: the mode operator / charge coupling
pt, px, py, pz, pw = sp.symbols("pt px py pz pw", real=True)
p = sp.Matrix([pt, px, py, pz, pw])
quad = sp.simplify((p.T * gi * p)[0, 0])
target = -pt ** 2 + px ** 2 + (py - kg * A * pw) ** 2 + pz ** 2 + pw ** 2
print("\nK2  g^{MN} p_M p_N for the ansatz:")
print(f"     = {quad}")
check("K2 g^{MN}p_M p_N = eta^{mu nu}(p_mu - kg A_mu p_w)(p_nu - kg A_nu p_w) + p_w^2 (charge coupling kg n/R)",
      sp.simplify(quad - target) == 0)

# ------------------------------------------------------------------ K3: normalization -> alpha_n = 4 n^2 l_P^2 / R^2
G4, R_, nn = sp.symbols("G4 R nn", positive=True)
kg_sq = sp.symbols("kg_sq", positive=True)
# gauge kinetic term: (1/(16 pi G4)) (kg^2/4) F^2  == (1/4) F_c^2  =>  kg^2 = 16 pi G4
kg_sol = sp.solve(sp.Eq(kg_sq / (16 * sp.pi * G4), 1), kg_sq)[0]
e_n = nn * sp.sqrt(kg_sol) / R_                               # charge coupling kg n / R
alpha_n = sp.simplify(e_n ** 2 / (4 * sp.pi))
m_n = nn / R_
print("\nK3  canonical normalization:")
print(f"     kg^2 = {kg_sol};   e_n = {sp.simplify(e_n)};   alpha_n = e_n^2/(4 pi) = {alpha_n}   (l_P^2 = G4 in hbar = c = 1)")
check("K3 alpha_n = 4 n^2 G4/R^2 = 4 n^2 l_P^2/R^2", sp.simplify(alpha_n - 4 * nn ** 2 * G4 / R_ ** 2) == 0)
check("K3' e_n^2 = 16 pi G4 m_n^2 (extremal KK charge-to-mass ratio)", sp.simplify(e_n ** 2 - 16 * sp.pi * G4 * m_n ** 2) == 0)

# ------------------------------------------------------------------ 2. requirement
print("\n2. WHAT alpha = 1/137.036 REQUIRES (n = 1):")
c = 299792458.0
Gn = 6.67430e-11
hbar = 1.054571817e-34
lP = math.sqrt(Gn * hbar / c ** 3)
k_req = 2.0 / math.sqrt(ALPHA)
R_req = k_req * lP
GEV_PER_KG = c ** 2 / 1.602176634e-10                         # 1 kg c^2 in GeV
M_KK_kg = hbar / (R_req * c)
M_KK_GeV = M_KK_kg * GEV_PER_KG
m_e_kg = 9.1093837015e-31
m_e_GeV = m_e_kg * GEV_PER_KG
print(f"     R/l_P = 2/sqrt(alpha) = {k_req:.6f};  R = {R_req:.4e} m;  l_P = {lP:.4e} m")
print(f"     carrier mass M_KK = hbar/(R c) = {M_KK_GeV:.3e} GeV;  m_e = {m_e_GeV:.3e} GeV;  M_KK/m_e = {M_KK_GeV / m_e_GeV:.3e}")
check("K4 requirement computed: R/l_P about 23.4", abs(k_req - 23.41) < 0.01, f"({k_req:.4f})")

# ------------------------------------------------------------------ 3. handles
print("\n3. DECLARED HANDLES on k = R/l_P (alpha = 4/k^2; a hit is within 1e-3 of 1/137.035999177):")
Z = 2 * math.sqrt(8 * PI / 3)
handles = [("1", 1.0), ("2", 2.0), ("sqrt(8 pi/3)", math.sqrt(8 * PI / 3)), ("Z = 2 sqrt(8 pi/3)", Z),
           ("2 pi", 2 * PI), ("4 pi", 4 * PI), ("Z^2 = 32 pi/3", Z * Z)]
print("     k                    alpha       alpha^-1     miss (rel)   hit?")
any_hit = False
for name, kv in handles:
    a = 4.0 / kv ** 2
    miss = abs(a - ALPHA) / ALPHA
    hit = miss < 1e-3
    any_hit = any_hit or hit
    print(f"     {name:19s}  {a:10.5e}  {1 / a:9.3f}   {miss:10.3e}    {'YES' if hit else 'no'}")
check("K5 no declared handle hits alpha to 1e-3 (declared expectation)", not any_hit)

print("\n4. INTEGER FLUX ROUTE (R = N l_P, alpha^-1 = N^2/4):")
any_int = False
for N in (23, 24):
    a = 4.0 / N ** 2
    miss = abs(a - ALPHA) / ALPHA
    any_int = any_int or miss < 1e-3
    print(f"     N = {N}:  alpha^-1 = {N * N / 4:.3f};  miss = {miss:.3e}")
check("K6 neither neighbouring integer N hits alpha to 1e-3", not any_int)

# ------------------------------------------------------------------ 5. electron obstruction
print("\n5. THE ELECTRON OBSTRUCTION: a KK momentum mode has m >= hbar/(R c).")
ratio = m_e_kg * R_req * c / hbar
print(f"     m_e R c/hbar = m_e/M_KK = {ratio:.3e}  (needs >= 1 for the electron to carry graviphoton charge)")
check("K7 the electron obstruction is present: m_e R c/hbar << 1 (declared expectation: ~1e-21)", ratio < 1e-15, f"({ratio:.2e})")

print("\n" + "=" * 100)
passed = sum(1 for _, ok in CHECKS if ok)
print(f"CHECKS: {passed}/{len(CHECKS)} passed")
print("VERDICT (against the declared criteria):")
print("  * The KK relation is derived (K1-K3): alpha_n = 4 n^2 l_P^2/R^2, e_n^2 = 16 pi G m_n^2.  Charge quantization is real, but it TRADES alpha for the modulus R.")
print(f"  * alpha = 1/137.036 needs R = {k_req:.2f} l_P; no declared handle or integer flux number hits (K5, K6).")
print(f"  * The carrier of the charge quantum would have M_KK ~ {M_KK_GeV:.1e} GeV; the electron is {ratio:.0e} of the minimum mass a graviphoton-charged mode can have (K7).")
print("    So the electron's charge cannot be graviphoton charge; a 5D gauge field would make e a free 5D coupling.")
print("  * Not tested: radion stabilization, the 5D cosmological constant, non-abelian or higher-dimensional KK.  kappa = 1/2 stays FITTED; the SM-mass wall is unchanged.")
sys.exit(0 if passed == len(CHECKS) else 1)
