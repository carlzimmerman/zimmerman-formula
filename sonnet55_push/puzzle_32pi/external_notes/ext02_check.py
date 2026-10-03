"""EXT02 check: do the six pasted "derivations" of a0 = c^2 sqrt(Lambda/(32 pi)) work?
(see EXT02_pasted_32pi_derivations_2026-10-02.md and README.md here)

Each section re-runs the paste's own arithmetic and then tests what it claims to establish.
Convention: PASS = the statement written in the check name is true. Several of those statements are
"the paste's claim FAILS" (e.g. "balance gives Lambda/(32 pi^2), not Lambda/(32 pi)"); the check name
says which way it reads.

Run:            python3 ext02_check.py            (exit 0 iff all checks pass)
Mutation run:   MUTATE=1 python3 ext02_check.py   (the de Sitter radius formula is corrupted; the run MUST fail)
"""
import os
import sys

import sympy as sp

MUTATE = os.environ.get("MUTATE") == "1"
results = []


def check(name, ok):
    results.append((name, bool(ok)))
    print(("PASS  " if ok else "FAIL  ") + name)


pi = sp.pi
Lam, a0, A, S, s = sp.symbols("Lambda a0 A S s", positive=True)

# ======================================================================================
# Pastes 1-2: Rindler disk x Chern-Gauss-Bonnet, GHY, heat-kernel boundary density
# ======================================================================================
# the E4 integral and the CGB numerology are right
L = sp.symbols("L", positive=True)
E4 = sp.Rational(24) / L**4                                     # Riem^2 - 4 Ric^2 + R^2 on S^4 radius L
check("1a int_{S^4} E4 dV = 64 pi^2 (the paste's number is right)",
      sp.simplify(E4 * 8 * pi**2 * L**4 / 3 - 64 * pi**2) == 0)
check("1b 32 pi^2 = 2 (4 pi)^2 (arithmetic true; the 'CGB constant = 2 Area(S^2)^2' reading is numerology)",
      32 * pi**2 == 2 * (4 * pi) ** 2)
# what pi/a0^2 is: the area of the Euclidean (tau, rho) disc, rho <= 1/a0, tau period 2 pi/a0 -- NOT a horizon cross-section
tau, rho = sp.symbols("tau rho", positive=True)
disc = sp.integrate(sp.integrate(a0 * rho, (rho, 0, 1 / a0)), (tau, 0, 2 * pi / a0))
check("1c pi/a0^2 is the area of the Euclidean (tau,rho) disc up to rho=1/a0 (the horizon cross-section is the infinite transverse plane)",
      sp.simplify(disc - pi / a0**2) == 0)
# the postulate A*Lambda = C gives a0^2 = pi Lambda / C for ANY C: nothing selects 32 pi^2
C = sp.symbols("C", positive=True)
sol_C = sp.solve(sp.Eq(pi / a0**2 * Lam, C), a0**2)[0]
check("1d postulate A*Lambda = C gives a0^2 = pi Lambda/C; C = 32 pi^2 -> Lambda/(32 pi), C = 16 pi^2 -> Lambda/(16 pi)",
      sp.simplify(sol_C - pi * Lam / C) == 0 and sp.simplify(sol_C.subs(C, 32 * pi**2) - Lam / (32 * pi)) == 0
      and sp.simplify(sol_C.subs(C, 16 * pi**2) - Lam / (16 * pi)) == 0)
check("1e GHY term a0 A/(4 pi) = 1/(4 a0) is arithmetic (and is never used in the matching)",
      sp.simplify(a0 * (pi / a0**2) / (4 * pi) - 1 / (4 * a0)) == 0)


def Bdens(Kd):                                                  # paste 2 density on S^1 x S^2, S^2 radius 1/a0
    Km = sp.diag(*Kd)
    Ric = sp.diag(0, a0**2, a0**2)
    K, R = Km.trace(), Ric.trace()
    return sp.simplify(sp.Rational(1, 3) * K * R - (Km * Ric).trace()
                       + sp.Rational(1, 3) * (K**3 - 3 * K * (Km * Km).trace() + 2 * (Km**3).trace()))


vals = [Bdens((0, a0, a0)), Bdens((2 * a0, 0, 0)), Bdens((2 * a0 / 3,) * 3)]
check("1f the paste's own boundary density gives -2/3, 4/3, 16/27 a0^3 for natural K_ij, never the claimed 4 a0^3",
      vals == [-2 * a0**3 / 3, 4 * a0**3 / 3, 16 * a0**3 / 27] and all(sp.simplify(v - 4 * a0**3) != 0 for v in vals))
check("1g its stated balance 8 pi a0^2 A = (Lambda/4pi) A gives a0^2 = Lambda/(32 pi^2), not Lambda/(32 pi)",
      sp.solve(sp.Eq(8 * pi * a0**2 * A, Lam / (4 * pi) * A), a0**2)[0] == Lam / (32 * pi**2))
check("1h with A = pi/a0^2 the 'boundary anomaly' 8 pi a0^2 A is the pure number 8 pi^2 (no a0)",
      sp.simplify(8 * pi * a0**2 * (pi / a0**2) - 8 * pi**2) == 0)
check("1i K_ij = a0 h_ij on a 3-dim boundary has trace 3 a0, not the 2 a0 the paste uses",
      sp.diag(a0, a0, a0).trace() == 3 * a0 and sp.diag(a0, a0, a0).trace() != 2 * a0)

# ======================================================================================
# Pastes 3-4: spin sum rule 7 N0 - 28 N1/2 + 86 N1 = 720
# ======================================================================================
sol_S = sp.solve(sp.Eq(8 * pi * a0**2 * A / (5760 * pi**2) * S, Lam / (4 * pi) * A), a0**2)[0]
check("2a prefactor 360 (4 pi)^2 = 5760 pi^2", sp.expand(360 * (4 * pi) ** 2) == 5760 * pi**2)
check("2b its balance gives a0^2 = 180 Lambda/S; at S = 720 that is Lambda/4, not Lambda/(32 pi)",
      sp.simplify(sol_S - 180 * Lam / S) == 0 and sp.simplify(sol_S.subs(S, 720) - Lam / 4) == 0)
need = sp.solve(sp.Eq(sol_S, Lam / (32 * pi)), S)[0]
check("2c Lambda/(32 pi) would need S = 5760 pi, irrational: no integer field content can satisfy it",
      sp.simplify(need - 5760 * pi) == 0 and not need.is_rational)


def Ssum(n0, nh, n1, n32=0, n2=0):
    return 7 * n0 - 28 * nh + 86 * n1 - 224 * n32 + 712 * n2


check("2d N=4 SYM as the paste counts (6,1,1) = 100, but 4 Majorana = 2 Dirac gives (6,2,1) = 72",
      Ssum(6, 1, 1) == 100 and Ssum(6, 2, 1) == 72)
check("2e Standard Model (4, 22.5, 12) = 430 and N=8 supergravity (70,28,28,8,1) = 1034; neither is 720",
      Ssum(4, sp.Rational(45, 2), 12) == 430 and Ssum(70, 28, 28, 8, 1) == 1034)
check("2f 'exact integer solution' (8,1,8) = 716, not 720; adding a scalar by the paste's own weight 7 gives 723, not +4",
      Ssum(8, 1, 8) == 716 and Ssum(9, 1, 8) == 723)
sols = [(n0, nh, n1) for n1 in range(0, 12) for nh in range(0, 30) for n0 in range(0, 120) if Ssum(n0, nh, n1) == 720]
check("2g integer solutions of the sum rule exist (e.g. (0,5,10); 39 found in a small box): the rule is a Diophantine knob",
      (0, 5, 10) in sols and len(sols) == 39)

# ======================================================================================
# Paste 5: d-dimensional "uniqueness of d = 4"
# ======================================================================================
def a0sq(d, Lv):
    """paste 5: a0^2 = pi/(d Vol(S^d)) * (2 Lambda/((d-1)(d-2)))^((d-2)/2); MUTATE corrupts R_dS^2."""
    volSd = 2 * pi ** sp.Rational(d + 1, 2) / sp.gamma(sp.Rational(d + 1, 2))
    fac = (d - 1) * (d - 1) if MUTATE else (d - 1) * (d - 2)
    return pi / (d * volSd) * (2 * Lv / fac) ** sp.Rational(d - 2, 2)


check("3a d = 4 reproduces a0^2 = Lambda/(32 pi)", sp.simplify(a0sq(4, Lam) - Lam / (32 * pi)) == 0)
check("3b paste's printed values: d=3 Lambda^{1/2}/(6 pi), d=5 sqrt(6) Lambda^{3/2}/(180 pi^2), d=6 Lambda^2/(640 pi^2)",
      sp.simplify(a0sq(3, Lam) - sp.sqrt(Lam) / (6 * pi)) == 0
      and sp.simplify(a0sq(5, Lam) - sp.sqrt(6) * Lam ** sp.Rational(3, 2) / (180 * pi**2)) == 0
      and sp.simplify(a0sq(6, Lam) - Lam**2 / (640 * pi**2)) == 0)
# dimensional weight: lengths L -> s L means Lambda -> Lambda/s^2 and a0^2 -> a0^2/s^2
weights = {d: sp.simplify(a0sq(d, Lam / s**2) * s**2 / a0sq(d, Lam)) for d in range(3, 9)}
check("3c under L -> s L the paste's a0^2 scales as s^(4-d) relative to a0^2: dimensionally consistent ONLY at d = 4",
      all(sp.simplify(w - s ** (4 - d)) == 0 for d, w in weights.items()) and weights[4] == 1
      and all(w != 1 for d, w in weights.items() if d != 4))
check("3d so its postulate A_dS/A_R = (pure number) equates length^(d-4) to a number: 'd = 4 is unique' is dimensional analysis of its own input",
      all(sp.simplify(sp.limit(weights[d], s, 2) - 2 ** (4 - d)) == 0 for d in (3, 5, 6)))
# in d = 4 the postulate is the p08 identity A_a0 = (4/3) Lambda Vol(S^4_L)
R2 = 3 / Lam
A_dS = 4 * pi * R2
A_R = pi / (Lam / (32 * pi))
volS4 = 8 * pi**2 * R2**2 / 3
check("3e d = 4: A_dS/A_R = 3/(8 pi) and A_R = (4/3) Lambda Vol(S^4_L) = 32 pi^2/Lambda (the identity already in p08)",
      sp.simplify(A_dS / A_R - 3 / (8 * pi)) == 0 and sp.simplify(A_R - sp.Rational(4, 3) * Lam * volS4) == 0
      and sp.simplify(A_R - 32 * pi**2 / Lam) == 0)
check("3f '32 pi = 12 x 8 pi/3' is arithmetic (12 pi/Lambda = A_dS, 8 pi/3 = Vol(S^4_1)/pi), not a '3D horizon volume'", 12 * (8 * pi / 3) == 32 * pi)

# ======================================================================================
# Paste 6: volume partition Vol(D2 x S2)/Vol(S4) = Lambda/(2 a0^2) := 16 pi
# ======================================================================================
VolS4 = 8 * pi**2 / 3 * (3 / Lam) ** 2
VolProd = (pi / a0**2) * (4 * pi * 3 / Lam)
ratio = sp.simplify(VolProd / VolS4)
check("4a the paste's 'exact' steps are right: Vol(S^4) = 24 pi^2/Lambda^2, Vol(D2 x S2) = 12 pi^2/(a0^2 Lambda), ratio Lambda/(2 a0^2)",
      sp.simplify(VolS4 - 24 * pi**2 / Lam**2) == 0 and sp.simplify(VolProd - 12 * pi**2 / (a0**2 * Lam)) == 0
      and sp.simplify(ratio - Lam / (2 * a0**2)) == 0)
Z = sp.sqrt(32 * pi / 3)                                         # 1/a0 in units of R_dS at a0^2 = Lambda/(32 pi)
check("4b at the target a0 the 'volume fraction' is 16 pi = 50.3 > 1: a fraction of S^4 cannot exceed 1",
      sp.simplify(ratio.subs(a0, sp.sqrt(Lam / (32 * pi))) - 16 * pi) == 0 and float(16 * pi) > 1)
check("4c the disc radius 1/a0 = 5.79 R_dS exceeds the largest geodesic distance pi R_dS on S^4: D2 does not fit in S^4 (cf. p06)",
      float(Z) > float(pi) and abs(float(Z) - 5.7886) < 1e-3)
check("4d 'set the ratio equal to 16 pi' is a free choice: ratio = C gives a0^2 = Lambda/(2C); C = 16 pi is the target by construction",
      sp.solve(sp.Eq(Lam / (2 * a0**2), C), a0**2)[0] == Lam / (2 * C)
      and sp.simplify(sp.solve(sp.Eq(Lam / (2 * a0**2), 16 * pi), a0**2)[0] - Lam / (32 * pi)) == 0)
check("4e the 16 pi 'coupling' is unit-dependent: S_EH = (1/(16 pi G)) int R, but in 8 pi G = 1 units the prefactor is 1/2",
      sp.simplify(1 / (16 * pi * sp.Symbol("G")) - sp.Rational(1, 2) / (8 * pi * sp.Symbol("G"))) == 0)
check("4f F1<->F2<->F3 are rearrangements of one equation: a0^2 = Lambda/(32 pi) <=> A Lambda = 32 pi^2 <=> Lambda/(2 a0^2) = 16 pi",
      sp.simplify(sp.solve(sp.Eq((pi / a0**2) * Lam, 32 * pi**2), a0**2)[0] - Lam / (32 * pi)) == 0
      and sp.simplify(sp.solve(sp.Eq(Lam / (2 * a0**2), 16 * pi), a0**2)[0] - Lam / (32 * pi)) == 0)

n_ok = sum(ok for _, ok in results)
print(f"\n{n_ok}/{len(results)} checks pass" + ("  [MUTATE=1: a failure is REQUIRED]" if MUTATE else ""))
sys.exit(0 if n_ok == len(results) else 1)
