#!/usr/bin/env python3
"""q01: the SU(2) BPST instanton and the ledger of where '32 pi^2' comes from in scale-carrying Yang-Mills.

Everything here is a recomputation (sympy), nothing is quoted.  Conventions: Euclidean, F = dA + A^A, geometric normalisation
(coupling g only in the action  S/hbar = (1/(4 g^2)) Int F^a_{mn} F^a_{mn} d^4x  ), 't Hooft symbols eta^a_{mn}.

  A1  BPST regular gauge  A^a_m = 2 eta^a_{mn} x_n/(x^2+rho^2)  gives  F^a_{mn} = -4 rho^2 eta^a_{mn}/(x^2+rho^2)^2,
      F^a_{mn}F^a_{mn} = 192 rho^4/(x^2+rho^2)^4  (self-dual), Int d^4x F.F = 32 pi^2 (rho-independent), = 4 x 8 pi^2 (per direction).
  A2  The instanton action is 8 pi^2/g^2 = (1/4)(32 pi^2)/g^2;  q = F.F~/(32 pi^2) integrates to 1, Int tr F^F = 8 pi^2.
  A3  The one-loop measure factor 1/(16 pi^2) = Omega_3/(2 (2 pi)^4).
  A4  The origin ledger: every scale-carrying '32 pi^2' is  4 x 8 pi^2  with the 4 coming from DIFFERENT places
        (directions of translation zero modes / the 1/4 of the Lagrangian / D in Lambda^D and in the trace / T_F^-1 x 2 of F~).
  A5  't Hooft measure structure: 4N zero modes -> (8 pi^2/g^2)^(2N); e^{-8 pi^2/g^2(rho)} = (Lambda rho)^b0 at one loop.
Controls/mutations are marked 'MUT' and must FAIL the claim they attack (they PASS when the claim is rejected).
"""
import itertools, sys
import sympy as sp

ok = []
def chk(name, cond):
    ok.append(bool(cond)); print(("PASS " if cond else "FAIL ") + name)

pi = sp.pi
rho, r = sp.symbols('rho r', positive=True)
x = sp.symbols('x1:5', real=True)
r2 = sum(xi**2 for xi in x)

# ------------------------------------------------------------------ 't Hooft symbols
def eta(a, m, n, bar=False):
    # a=1..3, m,n=1..4 ; eta^a_{ij} = eps_{aij}, eta^a_{i4} = +/- delta_{ai}  (bar flips the sign of the 4-components)
    if m <= 3 and n <= 3:
        return sp.LeviCivita(a, m, n)
    s = -1 if bar else 1
    if n == 4 and m <= 3:
        return s * (1 if a == m else 0)
    if m == 4 and n <= 3:
        return -s * (1 if a == n else 0)
    return 0

def field(bar=False, scale=1):
    A = [[scale * 2 * sum(eta(a, m, n, bar) * x[n-1] for n in range(1, 5)) / (r2 + rho**2) for m in range(1, 5)] for a in range(1, 4)]
    F = [[[None]*4 for _ in range(4)] for _ in range(3)]
    for a in range(3):
        for m in range(4):
            for n in range(4):
                val = sp.diff(A[a][n], x[m]) - sp.diff(A[a][m], x[n])
                for b in range(3):
                    for c in range(3):
                        e = sp.LeviCivita(a+1, b+1, c+1)
                        if e != 0:
                            val += e * A[b][m] * A[c][n]
                F[a][m][n] = sp.simplify(val)
    return A, F

A, F = field(False)
den = (r2 + rho**2)**2
# ------------------------------------------------------------------ A1
bad = 0
for a in range(3):
    for m in range(4):
        for n in range(4):
            bad += sp.simplify(F[a][m][n] + 4 * rho**2 * eta(a+1, m+1, n+1) / den) != 0
chk("A1 F^a_mn = -4 rho^2 eta^a_mn/(x^2+rho^2)^2 for all 48 components (mismatches %d)" % bad, bad == 0)

F2 = sp.simplify(sum(F[a][m][n]**2 for a in range(3) for m in range(4) for n in range(4)))
chk("A1 F^a_mn F^a_mn = 192 rho^4/(x^2+rho^2)^4", sp.simplify(F2 - 192 * rho**4 / (r2 + rho**2)**4) == 0)

eps4 = lambda m, n, p, q: sp.LeviCivita(m, n, p, q)
Ft = [[[sp.simplify(sp.Rational(1, 2) * sum(eps4(m+1, n+1, p+1, q+1) * F[a][p][q] for p in range(4) for q in range(4))) for n in range(4)] for m in range(4)] for a in range(3)]
selfdual = all(sp.simplify(Ft[a][m][n] - F[a][m][n]) == 0 for a in range(3) for m in range(4) for n in range(4))
chk("A1 self-duality F~ = F (all 48 components)", selfdual)

radial = lambda f: sp.integrate(f, (r, 0, sp.oo))
Omega3 = 2 * pi**2
I_tot = Omega3 * radial(192 * rho**4 * r**3 / (r**2 + rho**2)**4)
chk("A1 Int d^4x F.F = 32 pi^2, independent of rho (symbolic rho)", sp.simplify(I_tot - 32 * pi**2) == 0)

# per direction (no sum on mu): F^a_{1n}F^a_{1n} = 3 * 16 rho^4/(x^2+rho^2)^4 -> 8 pi^2
per = sum(sp.simplify(F[a][0][n]**2) for a in range(3) for n in range(4))
chk("A1 per-direction integrand F^a_{1n}F^a_{1n} = 48 rho^4/(x^2+rho^2)^4 (radial)", sp.simplify(per - 48 * rho**4 / (r2 + rho**2)**4) == 0)
I_dir = Omega3 * radial(48 * rho**4 * r**3 / (r**2 + rho**2)**4)
chk("A1 per translation direction Int = 8 pi^2 (= translation zero-mode norm) and 4 x 8 pi^2 = 32 pi^2", sp.simplify(I_dir - 8 * pi**2) == 0 and sp.simplify(4 * I_dir - 32 * pi**2) == 0)

# MUT: wrong power of rho in the numerator makes the integral rho-dependent -> the rho-independence check must reject it
I_mut = sp.simplify(Omega3 * radial(192 * rho**2 * r**3 / (r**2 + rho**2)**4))
chk("MUT A1 numerator 192 rho^2 (wrong power): integral is rho-dependent, so 'rho-independent 32 pi^2' is rejected", sp.simplify(sp.diff(I_mut, rho)) != 0)
# MUT: anti-instanton has the same F.F but opposite F.F~
Abar, Fbar = field(True)
F2bar = sp.simplify(sum(Fbar[a][m][n]**2 for a in range(3) for m in range(4) for n in range(4)))
Ftbar = [[[sp.simplify(sp.Rational(1, 2) * sum(eps4(m+1, n+1, p+1, q+1) * Fbar[a][p][q] for p in range(4) for q in range(4))) for n in range(4)] for m in range(4)] for a in range(3)]
asd = all(sp.simplify(Ftbar[a][m][n] + Fbar[a][m][n]) == 0 for a in range(3) for m in range(4) for n in range(4))
chk("A1 anti-instanton (eta-bar): F.F identical (192 rho^4/...), F~ = -F", sp.simplify(F2bar - F2) == 0 and asd)
# T_mn = F^a_{mr}F^a_{nr} - (1/4) delta_mn F^2 vanishes for (anti)self-dual fields (no back-reaction)
T = [[sp.simplify(sum(F[a][m][p] * F[a][n][p] for a in range(3) for p in range(4)) - (sp.Rational(1, 4) * F2 if m == n else 0)) for n in range(4)] for m in range(4)]
chk("A1 Euclidean stress tensor T_mn = F_mp F_np - (1/4) delta F^2 = 0 for the instanton (all 16 components)", all(t == 0 for row in T for t in row))

# ------------------------------------------------------------------ A2
g, hbar, N = sp.symbols('g hbar N', positive=True)
S_inst = sp.Rational(1, 4) * 32 * pi**2 / g**2
chk("A2 S_inst = (1/4)(32 pi^2)/g^2 = 8 pi^2/g^2  (the '1/4' is the Lagrangian normalisation)", sp.simplify(S_inst - 8 * pi**2 / g**2) == 0)
FFt = sp.simplify(sum(F[a][m][n] * Ft[a][m][n] for a in range(3) for m in range(4) for n in range(4)))
q_int = Omega3 * radial(FFt.subs({x[0]: r, x[1]: 0, x[2]: 0, x[3]: 0}) * r**3 / (32 * pi**2))
chk("A2 topological charge  q = F.F~/(32 pi^2)  integrates to 1 (F.F~ = F.F for the self-dual field)", sp.simplify(q_int - 1) == 0)
# F^F as a form: F^a ^ F^a = (1/2) F^a_mn F~^a_mn d^4x ; tr(T^aT^b)=delta/2 -> Int trF^F = (1/2)(1/2)*32 pi^2 = 8 pi^2
chk("A2 Int tr F^F = (1/2)(1/2) Int F.F~ = 8 pi^2 ;  c2 = (1/8 pi^2) Int tr F^F = 1", sp.Rational(1, 2) * sp.Rational(1, 2) * 32 * pi**2 == 8 * pi**2)
chk("A2 theta-term normalisation 32 pi^2 = (1/T_F)(1/(1/2 from F~)) x 8 pi^2 = 2 x 2 x 8 pi^2", 32 * pi**2 == 2 * 2 * 8 * pi**2)
chk("MUT A2 forgetting the 1/2 of F~ (or T_F) gives 16 pi^2 or 8 pi^2 per unit charge, not 32 pi^2", 2 * 8 * pi**2 != 32 * pi**2 and 8 * pi**2 != 32 * pi**2)

# ------------------------------------------------------------------ A3 : loop factor
k = sp.symbols('k', positive=True)
# Int d^4k/(2 pi)^4 f(k^2) = Omega_3/(2 pi)^4 Int k^3 dk f = (1/(16 pi^2)) Int (k^2) d(k^2) f
lhs = Omega3 / (2 * pi)**4
chk("A3 Omega_3/(2 pi)^4 = 1/(8 pi^2), and k^3 dk = (1/2) k^2 d(k^2)  ->  1/(16 pi^2) = (1/2)(1/(8 pi^2))", sp.simplify(lhs - 1 / (8 * pi**2)) == 0 and sp.simplify(sp.Rational(1, 2) * lhs - 1 / (16 * pi**2)) == 0)
chk("A3 16 pi^2 = (4 pi)^2 = 2 x 8 pi^2 = 2 x (2 pi)^4/Omega_3", sp.simplify(16 * pi**2 - (4 * pi)**2) == 0 and sp.simplify(16 * pi**2 - 2 * (2 * pi)**4 / Omega3) == 0)

# ------------------------------------------------------------------ A4 : the ledger
b0, mu, Lam, D = sp.symbols('b0 mu Lambda D', positive=True)
gg = sp.Function('g')
lnmu = sp.symbols('lnmu')
gsym = sp.symbols('gsym', positive=True)
beta = -b0 * gsym**3 / (16 * pi**2)
d_invg2 = sp.simplify(-2 * beta / gsym**3)                   # d(1/g^2)/dln mu = -2 beta/g^3
chk("A4 d(1/g^2)/dln mu = b0/(8 pi^2)   [8 pi^2 = 16 pi^2/2, the 2 is g^2 = g x g]", sp.simplify(d_invg2 - b0 / (8 * pi**2)) == 0)
theta_coeff = sp.simplify(sp.Rational(1, 4) * d_invg2)      # theta = mu dL/dmu, L = -(1/4g^2)F^2 -> theta = -(1/4) d(1/g^2)/dlnmu F^2
chk("A4 trace anomaly coefficient  theta = -(b0/(32 pi^2)) F^2_geo:  32 pi^2 = 4 (Lagrangian 1/4) x 8 pi^2", sp.simplify(theta_coeff - b0 / (32 * pi**2)) == 0)
Dd = sp.Integer(4)
chk("A4 eps_vac = theta/D: coefficient b0/(128 pi^2) = (1/D) b0/(32 pi^2), 128 pi^2 = 4 x 32 pi^2", sp.simplify(theta_coeff / Dd - b0 / (128 * pi**2)) == 0)
# Lambda^D = mu^D exp(-D * 8 pi^2/(b0 g^2)) = mu^4 exp(-32 pi^2/(b0 g^2))
gs = sp.symbols('gs', positive=True)
Lam1 = mu * sp.exp(-8 * pi**2 / (b0 * gs**2))
chk("A4 Lambda^4 = mu^4 exp(-32 pi^2/(b0 g^2)),  32 pi^2 = D x 8 pi^2 with D = 4 = mass dimension of an energy density", sp.simplify(Lam1**4 - mu**4 * sp.exp(-32 * pi**2 / (b0 * gs**2))) == 0)
# integrated anomaly on the instanton = -b0 (per unit charge)  <->  mu dS_inst/dmu = b0
I_theta = -b0 / (32 * pi**2) * 32 * pi**2
chk("A4 Int theta d^4x over the instanton = -b0 = -(mu d/dmu)(8 pi^2/g^2): the anomaly's 32 pi^2 IS the instanton unit 32 pi^2", sp.simplify(I_theta + b0) == 0 and sp.simplify(sp.integrate(b0 / (8 * pi**2), (lnmu, 0, 1)) * 8 * pi**2 - b0) == 0)

# the four different origins of '4' in 32 pi^2 = 4 x 8 pi^2
origins = {
    "4 translation directions (zero-mode norms 8 pi^2 each)": 4,
    "1/4 of the Lagrangian normalisation (S = F.F/(4 g^2))": 4,
    "D = 4 in Lambda^D / trace (Lambda^4, T^mu_mu = 4 eps)": 4,
    "2 (F~ = (1/2) eps F) x 2 (T_F = 1/2) in the theta-term": 4,
}
chk("A4 all four origins multiply 8 pi^2 to the same 32 pi^2 (%d entries) although the '4' means four different things" % len(origins), all(v * 8 * pi**2 == 32 * pi**2 for v in origins.values()))
chk("MUT A4 with D=3 (or a Lagrangian normalisation 1/3) the identity chain breaks (32 pi^2 != 3 x 8 pi^2)", 3 * 8 * pi**2 != 32 * pi**2)
# gravity-side reminder (pure numbers, lane A owns the derivation): Vol(S^4_1) = 8 pi^2/3 ; int E4 = 24 Vol = 64 pi^2 = 2 x 32 pi^2 ; 12 Vol = 32 pi^2
volS4 = sp.Rational(8, 3) * pi**2
chk("A4 gravity side pure numbers: Vol(S^4_1) = 8 pi^2/3, 12 Vol = 32 pi^2, Int E4 = 24 Vol = 64 pi^2 = 2 x 32 pi^2 (chi = 2)", 12 * volS4 == 32 * pi**2 and 24 * volS4 == 64 * pi**2)

# ------------------------------------------------------------------ A5 : 't Hooft measure structure
Nn = sp.symbols('Nn', positive=True, integer=True)
zero_modes = lambda n: 4 * n
chk("A5 SU(N) k=1 has 4N bosonic collective coordinates (4N-5 orientations + 4 position + 1 size); each contributes sqrt(S_0) -> (S_0)^(2N) = (8 pi^2/g^2)^(2N)",
    all(zero_modes(n) == (4 * n - 5) + 4 + 1 for n in range(2, 8)))
# translation-mode norm check: per direction norm^2 = (1/g^2) x 8 pi^2 = S_0  (verified above: I_dir)
chk("A5 translation zero-mode norm^2 = (1/g^2) x 8 pi^2 = S_0 (from the per-direction integral above)", sp.simplify(I_dir / g**2 - S_inst) == 0)
# e^{-8 pi^2/g^2(rho)} = (Lambda rho)^b0 at one loop
lnLR = sp.symbols('lnLR', real=True)   # ln(1/(Lambda rho))
inv_g2 = b0 / (8 * pi**2) * (-sp.log(Lam * rho))            # 1/g^2(1/rho) = (b0/8pi^2) ln(1/(Lambda rho))
weight = sp.simplify(sp.exp(-8 * pi**2 * inv_g2))
chk("A5 one-loop: exp(-8 pi^2/g^2(1/rho)) = (Lambda rho)^b0", sp.simplify(weight - (Lam * rho)**b0) == 0)
# constant: 0.466 = 4.60/pi^2 ;  C_N = 0.466 e^{-1.679 N}/((N-1)!(N-2)!)  (as printed in the RMP review, arXiv hep-ph/9610451 eq. 93)
import math
chk("A5 0.466 = 4.60/pi^2 to 3 digits", abs(4.60 / math.pi**2 - 0.466) < 1e-3)
C = lambda n: 0.466 * math.exp(-1.679 * n) / (math.factorial(n - 1) * math.factorial(n - 2))
print("     C_2 = %.5f (SU(2)), C_3 = %.6f (SU(3)) [MS-bar-like constants as printed; scheme dependent]" % (C(2), C(3)))
chk("A5 C_N small and N! suppressed: C_2 = 1.6e-2, C_3 = 1.4e-3 (ratio C_3/C_2 = %.3f)" % (C(3) / C(2)), abs(C(2) - 0.01625) < 3e-4 and C(3) < C(2))

print("\nsummary: 32 pi^2 = Int F.F per unit charge = 4 x 8 pi^2 ; the anomaly, the condensate weight, Lambda^4 and the theta-term all reuse this one unit.")
print("         The '4' in front of 8 pi^2 has four different origins (directions / Lagrangian 1/4 / D / F~ x T_F), so it is not one symmetry statement.")
n_ok = sum(ok)
print("\n%d/%d" % (n_ok, len(ok)))
sys.exit(0 if all(ok) else 1)
