"""EXT03 check: independent re-derivation of the headline equations of the external 32pi handoff
(phases 05-10, 2026-10-04; see README.md here). Nothing is copied from the bundle's stored outputs.

Convention: PASS = the statement in the check name is true.
c = 1; classical sections use M_P^2 = 1/(8 pi G) factored out of the action; the anomaly section uses hbar = 1.

Run:            python3 ext03_check.py            (exit 0 iff all checks pass)
Mutation run:   MUTATE=1 python3 ext03_check.py   (the Gauss-Bonnet boundary term 8 -> 7; the run MUST fail)
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
t = sp.symbols("t")
al, H, M, r, Lb, G, aE = sp.symbols("alpha H M r Lambda_b G a_E", positive=True)
GB = 7 if MUTATE else 8

# ======================================================================================
# 1. Classical scalar-Euler action, flat FRW minisuperspace with the lapse kept until variation
#    S = int sqrt(-g)[R/2 - Lb - (d phi)^2/2 + alpha phi E4]
# ======================================================================================
N = sp.Function("N")(t)
a = sp.Function("a")(t)
ph = sp.Function("phi")(t)
# a^3 E4 = 8 d/dt(adot^3) at N = 1 (verified below); with the lapse sqrt(-g)E4 = 8 d/dt(adot^3/N^3)
ad = a.diff(t)
E4_N1 = 24 * (ad / a) ** 2 * (a.diff(t, 2) / a)                 # 24 H^2 (Hdot + H^2) = 24 H^2 addot/a
check("1a a^3 E4 = 8 d/dt(adot^3) on flat FRW (N = 1)",
      sp.simplify(a**3 * E4_N1 - 8 * sp.diff(ad**3, t)) == 0)
# after integrating alpha*phi*GB*d/dt(adot^3/N^3) by parts
L = -3 * a * ad**2 / N + a**3 * ph.diff(t) ** 2 / (2 * N) - N * a**3 * Lb - GB * al * ph.diff(t) * ad**3 / N**3


def EL(L, f):
    return sp.diff(L, f) - sp.diff(sp.diff(L, f.diff(t)), t)


q = sp.symbols("q", positive=True)
sub_dS = lambda e: (e.subs(N, 1).doit()
                    .subs({a.diff(t, 2): H**2 * sp.exp(H * t), a.diff(t): H * sp.exp(H * t), a: sp.exp(H * t)})
                    .subs({ph.diff(t, 2): 0, ph.diff(t): q}))
# scalar: d/dt(a^3 phidot - 8 alpha adot^3) = 0; the attractor (current 0) gives constant roll
p_phi = sp.diff(L, ph.diff(t)).subs(N, 1)
q_sol = sp.solve(sub_dS(p_phi), q)
check("1b constant-roll de Sitter branch: q = phidot = 8 alpha H^3 (bundle's eq)",
      len(q_sol) == 1 and sp.simplify(q_sol[0] - 8 * al * H**3) == 0)
# Hamiltonian constraint (vary N, then set N = 1)
ham = sp.simplify(sub_dS(sp.diff(L, N)) / sp.exp(3 * H * t))
Lb_sol = sp.solve(ham.subs(q, 8 * al * H**3), Lb)
check("1c Hamiltonian constraint: Lambda_b = 3 H^2 + 160 alpha^2 H^6 (bundle's boxed eq)",
      len(Lb_sol) == 1 and sp.simplify(Lb_sol[0] - (3 * H**2 + 160 * al**2 * H**6)) == 0)
check("1d hence Lambda_b > 0 strictly: no self-supported dS branch with Lambda_b = 0 (canonical scalar)",
      sp.simplify(Lb_sol[0]).is_positive)
# the a-equation must be consistent with the same branch (otherwise the background is not a solution)
ae = sp.simplify(sub_dS(EL(L, a)) / sp.exp(2 * H * t))
check("1e scale-factor equation is satisfied on that branch (background consistent)",
      sp.simplify(ae.subs({q: 8 * al * H**3, Lb: Lb_sol[0]})) == 0)

# ======================================================================================
# 2. Static star: Box phi = -alpha E4 on Schwarzschild, E4 = 48 M^2/r^6
# ======================================================================================
f = 1 - 2 * M / r
C = sp.symbols("C")
flux = C + sp.integrate(-al * 48 * M**2 / r**6 * r**2, r)         # r^2 f phi' = C - alpha int E4 r^2 dr
check("2a regular horizonless centre (C = 0): phi' = 16 alpha M^2/(r^5 (1 - 2M/r)) (bundle's eq)",
      sp.simplify(flux.subs(C, 0) / (r**2 * f) - 16 * al * M**2 / (r**5 * f)) == 0)
check("2b far field falls as r^-5, not as the MOND r^-1 (sqrt(G M a0)/r)",
      sp.limit(flux.subs(C, 0) / (r**2 * f) * r**5, r, sp.oo) == 16 * al * M**2)

# ======================================================================================
# 3. Rolling scalar on Schwarzschild-de Sitter, phi = q t + psi(r), regular on both future horizons
#    Box phi = (r^2 f psi')'/r^2 = -alpha E4,  E4 = 48 M^2/r^6 + 8 Lambda^2/3
#    future BH horizon: psi' -> +q/f ; future cosmological horizon: psi' -> -q/f
#    => q (r_b^2 + r_c^2) = J(r_b) - J(r_c);  claim: q = 8 alpha (kappa_b + kappa_c)/(r_b^2 + r_c^2)
# ======================================================================================
Mv, Lv = sp.Rational(1, 10), sp.Rational(1, 5)
fS = 1 - 2 * Mv / r - Lv * r**2 / 3
roots = sorted([sp.re(x) for x in sp.Poly(sp.numer(sp.together(fS * r)), r).nroots(n=40) if abs(sp.im(x)) < 1e-30
                and sp.re(x) > 0])
rb, rc = roots[0], roots[1]
J = lambda x: C - al * sp.integrate((48 * Mv**2 / r**6 + 8 * Lv**2 / 3) * r**2, r).subs(r, x)
q_two = sp.simplify((J(rb) - J(rc)) / (rb**2 + rc**2))
kb, kc = abs(sp.diff(fS, r).subs(r, rb)) / 2, abs(sp.diff(fS, r).subs(r, rc)) / 2
check("3a two-horizon roll q = 8 alpha (kappa_b + kappa_c)/(r_b^2 + r_c^2) (M = 0.1, Lambda = 0.2)",
      abs(sp.N((q_two - 8 * al * (kb + kc) / (rb**2 + rc**2)) / al, 30)) < 1e-25)
q_cos = 8 * al * (Lv / 3) ** sp.Rational(3, 2)
check("3b ... and it differs from the homogeneous roll 8 alpha H^3 (ratio != 1)",
      abs(sp.N(q_two / q_cos) - 1) > 1e-3)

# ======================================================================================
# 4. Type-A trace anomaly on de Sitter: <T> = -a_E E4/(16 pi^2) (Weyl = Box R = 0), T_mn = -rho g_mn
# ======================================================================================
E4dS = 24 * H**4
rho = -(-aE * E4dS / (16 * pi**2)) / 4                                # trace = -4 rho
check("4a rho_anom = 3 a_E H^4/(8 pi^2)", sp.simplify(rho - 3 * aE * H**4 / (8 * pi**2)) == 0)
H2 = sp.solve(sp.Eq(H**2, 8 * pi * G * rho / 3), H)
check("4b nonzero Friedmann branch (bare vacuum = 0): H^2 = pi/(G a_E)",
      len(H2) == 1 and sp.simplify(H2[0] ** 2 - pi / (G * aE)) == 0)
Hs2 = pi / (G * aE)
A_dS = 4 * pi / Hs2
check("4c A_dS/(4G) = a_E  and  R(S^4)^2 = 1/H^2 = G a_E/pi",
      sp.simplify(A_dS / (4 * G) - aE) == 0 and sp.simplify(1 / Hs2 - G * aE / pi) == 0)
check("4d Lambda_eff A_dS = 12 pi (not the target 32 pi^2)",
      sp.simplify(3 * Hs2 * A_dS - 12 * pi) == 0)
a0 = sp.symbols("a0", positive=True)
a0sq = sp.solve(sp.Eq(a0**2, 3 * Hs2 / (32 * pi)), a0)[0] ** 2       # target a0^2 = Lambda/(32 pi), G = 1 units of a0
check("4e target in anomaly variables: a0^2 = 3/(32 G a_E) (a restatement, not derived)",
      sp.simplify(a0sq - sp.Rational(3, 32) / (G * aE)) == 0)

# ======================================================================================
# 5. Free CFT anomaly coefficients: a = (Ns + 11 ND + 62 Nv)/360, c = (Ns + 6 ND + 12 Nv)/120
# ======================================================================================
aC = lambda s, d, v: sp.Rational(s + 11 * d + 62 * v, 360)
cC = lambda s, d, v: sp.Rational(s + 6 * d + 12 * v, 120)
check("5a 11 real scalars and 1 Dirac: same a_E (11/360)", aC(11, 0, 0) == aC(0, 1, 0) == sp.Rational(11, 360))
check("5b ... different c_E (11/120 vs 1/20): trace + background do not fix the response",
      cC(11, 0, 0) == sp.Rational(11, 120) and cC(0, 1, 0) == sp.Rational(1, 20))
# observed Lambda in Planck units (Lambda = 1.1056e-52 m^-2, l_P^2 = 2.6121e-70 m^2): a_E needed for H^2 = pi/(G a_E)
Lam_P = sp.Float("1.1056e-52") * sp.Float("2.6121e-70")
aE_need = pi / (Lam_P / 3)
check(f"5c the anomaly branch needs a_E = pi/(G H^2) = {sp.N(aE_need, 3)} for the observed Lambda (~1e122 free fields)",
      1e121 < sp.N(aE_need) < 1e124)

npass = sum(ok for _, ok in results)
print(f"\n{npass}/{len(results)} pass" + ("  (MUTATE)" if MUTATE else ""))
sys.exit(0 if npass == len(results) else 1)
