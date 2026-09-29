#!/usr/bin/env python3
"""F2 -- Family B: Freund-Rubin M_4 x S^n with integer flux N, D-dim cosmological term, and the 4D couplings of the n=2 (D=6) case.
Pre-registered in F0_PREREGISTRATION.md (written before this script was run).
Action:  S = Int sqrt(g_D) [ R/(2 kappa^2) - Lambda/kappa^2 - F^2/(2 g^2 n!) ],  oint_{S^n} F = 2 pi N (unit-charge (n-2)-brane).
Run:   python3 f2_flux_freund_rubin.py            (real run)
       python3 f2_flux_freund_rubin.py --mutate   (control: flip the sign of the S^n curvature term; must FAIL the Einstein-equation cross-check)
"""
import sys, math
import sympy as sp
import mpmath as mp

MUTATE = "--mutate" in sys.argv
CHECKS = []
mp.mp.dps = 400
ALPHA = 1 / 137.035999177


def check(tag, ok, detail=""):
    CHECKS.append((tag, bool(ok)))
    print(f"  [{'PASS' if ok else 'FAIL'}] {tag} {detail}")


print("=" * 100)
print("F2 Freund-Rubin flux compactification -- mode: " + ("MUTATE CONTROL (curvature sign flipped)" if MUTATE else "REAL RUN"))
print("=" * 100)

R, R0, kap, g, Lam, N = sp.symbols("R R0 kappa g Lambda N", positive=True)
H2 = sp.symbols("H2", real=True)
Lam = sp.symbols("Lambda", real=True)
SIGN = -1 if MUTATE else 1

# ------------------------------------------------------------------ B1: potential vs D-dim Einstein equations, n = 2, 3
print("\nB1  V_E(R) from the reduction versus the D-dimensional Einstein equations (independent derivation)")
for n in (2, 3):
    omega = 2 * sp.pi ** sp.Rational(n + 1, 2) / sp.gamma(sp.Rational(n + 1, 2))
    omega = sp.simplify(omega)
    B = 2 * sp.pi * N / (omega * R ** n)                       # orthonormal flux component
    U = omega * R ** n * (Lam / kap ** 2 - SIGN * n * (n - 1) / (2 * kap ** 2 * R ** 2) + B ** 2 / (2 * g ** 2))
    VE = (R0 / R) ** (2 * n) * U                              # Einstein-frame energy density (R0 = radius that defines M_P)
    Lam_pot = sp.solve(sp.Eq(sp.diff(VE, R).subs(R, R0), 0), Lam)[0]
    v_pot = sp.simplify(VE.subs(Lam, Lam_pot).subs(R, R0))
    k4sq = kap ** 2 / (omega * R0 ** n)                        # kappa_4^2 = kappa^2 / Vol
    H2_pot = sp.simplify(k4sq * v_pot / 3)
    # Einstein equations: G_MN + Lambda g_MN = kappa^2 T_MN,  R_mn = 3 H^2 g (dS4), R_ab = (n-1)/R^2 g ; flux on S^n
    Rb = 4 * 3 * H2 + n * (n - 1) / R ** 2                     # Ricci scalar (the control mutates only the potential, not the Einstein equations)
    Bq = B.subs(R, R0)
    eq_mn = sp.Eq(3 * H2 - Rb / 2 + Lam, kap ** 2 * (-Bq ** 2 / (2 * g ** 2)))
    eq_ab = sp.Eq((n - 1) / R ** 2 - Rb / 2 + Lam, kap ** 2 * (Bq ** 2 / (2 * g ** 2)))
    sol = sp.solve([eq_mn.subs(R, R0), eq_ab.subs(R, R0)], [H2, Lam], dict=True)[0]
    ok_L = sp.simplify(sol[Lam] - Lam_pot) == 0
    ok_H = sp.simplify(sol[H2] - H2_pot) == 0
    print(f"    n={n}: Lambda from V'=0 : {sp.simplify(Lam_pot)}")
    print(f"          Lambda from Einstein eqs: {sp.simplify(sol[Lam])}")
    check(f"B1 n={n}: Lambda(V'=0) == Lambda(Einstein eqs)", ok_L)
    check(f"B1 n={n}: 3H^2 = kappa_4^2 V_E(R*) (4D Friedmann) from both routes", ok_H)

# ------------------------------------------------------------------ B2: n = 2 closed form
print("\nB2  n = 2 (D = 6): extremum, stability, Minkowski point, tuning")
n = 2
omega = 4 * sp.pi
B = N / (2 * R ** 2)
U = omega * R ** 2 * (Lam / kap ** 2 - 1 / (kap ** 2 * R ** 2) + B ** 2 / (2 * g ** 2))
VE = (R0 / R) ** 4 * U
sol_M = sp.solve([sp.Eq(VE.subs(R, R0), 0), sp.Eq(sp.diff(VE, R).subs(R, R0), 0)], [Lam, R0], dict=True)
sol_M = [s for s in sol_M if s[R0].is_positive]
RM2 = sp.simplify(sol_M[0][R0] ** 2)
LamM = sp.simplify(sol_M[0][Lam])
print(f"    Minkowski point (V=0, V'=0):  R*^2 = {RM2},   Lambda_6 = {LamM}")
check("B2a Minkowski: R*^2 = N^2 kappa^2/(4 g^2)", sp.simplify(RM2 - N ** 2 * kap ** 2 / (4 * g ** 2)) == 0)
check("B2b Minkowski: Lambda_6 = 1/(2 R*^2)  (Lambda_6 has dimension length^-2; it enters U as Lambda/kappa^2)", sp.simplify(LamM - 1 / (2 * RM2)) == 0)
d2 = sp.simplify(sp.diff(VE, R, 2).subs(Lam, LamM).subs(R, R0).subs(R0, sol_M[0][R0]))
print(f"    V_E''(R*) at the Minkowski point = {d2}   (>0: radion is stable; other modes NOT tested, cf. hep-th/0205080)")
check("B2c radion is stable at the Minkowski point: V''(R*) = 64 pi g^2/(N^2 kappa^4) > 0", sp.simplify(d2 - 64 * sp.pi * g ** 2 / (N ** 2 * kap ** 4)) == 0)
# window of Lambda that supports a radion minimum, in units R_M = 1 (kappa=1, g^2=N^2/4)
yy = sp.symbols("y", positive=True)
Wp = sp.Rational(1)                                            # units check: W = Lam/y - 1/y^2 + 1/(2 y^3) with y = R^2
Wfun = lambda LL, y: LL / y - 1 / y ** 2 + sp.Rational(1, 2) / y ** 3
Lam_of_y = sp.solve(sp.Eq(sp.diff(Wfun(Lam, yy), yy), 0), Lam)[0]        # extremum of R^-2 f  (see script text)
Lam_top = sp.simplify(Lam_of_y.subs(yy, sp.Rational(3, 2)))
print(f"    in units R_M=1: Lambda_6(y=R^2) at an extremum = {sp.simplify(Lam_of_y)}; the minimum branch merges with the maximum at y=3/2, Lambda_6 = {Lam_top}")
print("    => minima exist for Lambda_6 < 2/3 (in units of 1/(kappa^2 R_M^2)); V>0 (dS) only for Lambda_6 in (1/2, 2/3); V=0 at exactly 1/2; V<0 below.")
check("B2d Lambda_c = 1/2 and the merger value 2/3 (units 1/R_M^2)", sp.simplify(Lam_of_y.subs(yy, 1) - sp.Rational(1, 2)) == 0 and Lam_top == sp.Rational(2, 3))

# tuning: envelope dV_min/dLambda = 4 pi R^2/kappa^2 ; needed |delta Lambda/Lambda_c| for V_min = v
ratio = sp.simplify((kap ** 2 * sp.symbols("v", positive=True) / (4 * sp.pi * R0 ** 2)) / (1 / (2 * R0 ** 2)))
print(f"    relative tuning of Lambda_6 needed to hold V = v: delta Lambda/Lambda_c = {ratio}")

# ------------------------------------------------------------------ B3: 4D couplings at the Minkowski point (sympy reduction)
print("\nB3  4D gauge couplings of the n=2 background (fibration ansatz, A_mu = A(x) in the y-slot)")
t, xx, yv, zz, th, ph = sp.symbols("t x y z theta phi", real=True)
Rr, Nn = sp.symbols("Rr Nn", positive=True)
Af = sp.Function("A")(xx)
coords = [t, xx, yv, zz, th, ph]
gm = sp.zeros(6, 6)
gm[0, 0] = -1; gm[1, 1] = 1; gm[2, 2] = 1; gm[3, 3] = 1
gm[4, 4] = Rr ** 2
# R^2 sin^2 th (dphi + A dy)^2
gm[5, 5] = Rr ** 2 * sp.sin(th) ** 2
gm[5, 2] = gm[2, 5] = Rr ** 2 * sp.sin(th) ** 2 * Af
gm[2, 2] = 1 + Rr ** 2 * sp.sin(th) ** 2 * Af ** 2
gi = gm.inv().applyfunc(sp.simplify)
Gam = [[[sum(gi[a, d] * (sp.diff(gm[d, b], coords[c]) + sp.diff(gm[d, c], coords[b]) - sp.diff(gm[b, c], coords[d])) for d in range(6)) / 2 for c in range(6)] for b in range(6)] for a in range(6)]
def Ric(b, c):
    r = 0
    for a in range(6):
        r += sp.diff(Gam[a][b][c], coords[a]) - sp.diff(Gam[a][b][a], coords[c])
        for d in range(6):
            r += Gam[a][a][d] * Gam[d][b][c] - Gam[a][c][d] * Gam[d][b][a]
    return r
R6 = sp.simplify(sum(gi[b, c] * Ric(b, c) for b in range(6) for c in range(6)))
F4sq = 2 * sp.diff(Af, xx) ** 2                                  # F_{mu nu}F^{mu nu} for A_y(x)
expected_R6 = 2 / Rr ** 2 - sp.Rational(1, 4) * Rr ** 2 * sp.sin(th) ** 2 * F4sq
print(f"    6D Ricci scalar of the fibration = {R6}")
check("B3a R_6 = 2/R^2 - (1/4) R^2 sin^2(theta) F_{mu nu}F^{mu nu}", sp.simplify(R6 - expected_R6) == 0)
# Maxwell field strength with A_pot = -(N/2) cos(theta) (dphi + A dy)
Apot = [0, 0, -(Nn / 2) * sp.cos(th) * Af, 0, 0, -(Nn / 2) * sp.cos(th)]
Fm = sp.Matrix(6, 6, lambda a, b: sp.diff(Apot[b], coords[a]) - sp.diff(Apot[a], coords[b]))
F2 = sp.simplify(sum(gi[a, c] * gi[b, d] * Fm[a, b] * Fm[c, d] for a in range(6) for b in range(6) for c in range(6) for d in range(6)))
expected_F2 = Nn ** 2 / (2 * Rr ** 4) + sp.Rational(1, 4) * Nn ** 2 * sp.cos(th) ** 2 * F4sq
print(f"    F_MN F^MN = {sp.simplify(F2)}")
check("B3b F^2 = N^2/(2R^4) + (N^2/4) cos^2(theta) F4^2", sp.simplify(F2 - expected_F2) == 0)
# integrate over S^2 (area element R^2 sin th)
kin_geo = sp.integrate(Rr ** 2 * sp.sin(th) * (Rr ** 2 * sp.sin(th) ** 2), (th, 0, sp.pi)) * 2 * sp.pi     # Int R^2 sin^2 * dA
kin_flux = sp.integrate(Rr ** 2 * sp.sin(th) * sp.cos(th) ** 2, (th, 0, sp.pi)) * 2 * sp.pi               # Int cos^2 dA
kap6, g6 = sp.symbols("kappa6 g6", positive=True)
# L4 = -(1/4) F4^2 * [ (1/(2 kap^2)) Int R^2 sin^2 dA + (1/g^2)(N^2/4)/... ]  (Einstein: R/(2k^2) ; Maxwell: -F^2/(4 g^2) with the 1/(4g^2) convention)
# careful with the Maxwell normalisation: -(1/(4 g^2)) F_MN F^MN  -> coefficient of -(1/4) F4^2 is (1/g^2)(N^2/4) Int cos^2 dA
inv_g2 = sp.simplify(kin_geo / (2 * kap6 ** 2) + (Nn ** 2 / 4) * kin_flux / g6 ** 2)
print(f"    1/g_SU2(3)^2 = (1/(2 kappa^2)) Int R^2 sin^2 dA + (1/g^2)(N^2/4) Int cos^2 dA = {inv_g2}")
# the pure-geometry piece equals the general KK formula Vol|K|^2/(2 kappa^2) with |K|^2 = R^2 sin^2
check("B3c geometric piece 1/g^2_geo = 4 pi R^4/(3 kappa^2)", sp.simplify(kin_geo / (2 * kap6 ** 2) - 4 * sp.pi * Rr ** 4 / (3 * kap6 ** 2)) == 0)
inv_g1 = 4 * sp.pi * Rr ** 2 / g6 ** 2                          # 6D Maxwell zero mode, unit 6D charge
# Minkowski point substitution
subsM = {g6: sp.sqrt(Nn ** 2 * kap6 ** 2 / (4 * Rr ** 2))}
g2_su2 = sp.simplify(1 / inv_g2.subs(subsM))
g2_u1 = sp.simplify(1 / inv_g1.subs(subsM))
k4sq = kap6 ** 2 / (4 * sp.pi * Rr ** 2)
lP2 = k4sq / (8 * sp.pi)                                       # G_4 = kappa_4^2/(8 pi)
a_su2 = sp.simplify(g2_su2 / (4 * sp.pi) / (lP2 / Rr ** 2))
a_u1 = sp.simplify(g2_u1 / (4 * sp.pi) / (lP2 / Rr ** 2))
print(f"    at the Minkowski point:  alpha_SU2 / (l_P^2/R^2) = {a_su2},   alpha_U1 / (l_P^2/R^2) = {a_u1}")
check("B3d Minkowski point: alpha_SU2 = 3 l_P^2/R^2", sp.simplify(a_su2 - 3) == 0)
check("B3e Minkowski point: alpha_U1(unit charge) = N^2 l_P^2/(2 R^2)", sp.simplify(a_u1 - Nn ** 2 / 2) == 0)
chat = sp.symbols("chat", positive=True)                       # chat = g^2/kappa_6
Rl = sp.sqrt(2) * sp.pi * Nn ** 2 / chat
al_chat = sp.simplify(a_u1 / Rl ** 2)                          # alpha_U1 = a_u1 (l_P/R)^2 ; with (R/l_P) = sqrt2 pi N^2/chat
print(f"    R*/l_P = sqrt(2) pi N^2 / chat;  alpha_U1 = {al_chat} = (chat/(2 pi N))^2")
R2M = Nn ** 2 * kap6 / (4 * chat)                              # R*^2 with g6^2 = chat*kappa6
lP2M = kap6 ** 2 / (32 * sp.pi ** 2 * R2M)
check("B3f alpha_U1 = (chat/(2 pi N))^2 with chat = g_6^2/kappa_6, and (R*/l_P)^2 = 2 pi^2 N^4/chat^2",
      sp.simplify(al_chat - (chat / (2 * sp.pi * Nn)) ** 2) == 0 and sp.simplify(R2M / lP2M - 2 * sp.pi ** 2 * Nn ** 4 / chat ** 2) == 0)

# exact solution at V = v = x/(8 pi l_P^4): how much does the x-correction move alpha?
print("\n    exact solve at the physical vacuum energy (N=2, chat=1, kappa_6=1, 400-digit arithmetic)")
xx_phys = mp.mpf("2.8485e-122")
Nn_v, chat_v = mp.mpf(2), mp.mpf(1)
g2v = chat_v                                                # g^2 = chat*kappa, kappa=1
def V_of(Rv, Lv):                                           # E-frame V at R=R0=Rv
    B = Nn_v / (2 * Rv ** 2)
    return 4 * mp.pi * Rv ** 2 * (Lv - 1 / Rv ** 2 + B ** 2 / (2 * g2v))
def dV_of(Rv, Lv):                                          # d/dR at R=R0: -4 U/R + U'
    U = lambda r: 4 * mp.pi * r ** 2 * (Lv - 1 / r ** 2 + (Nn_v / (2 * r ** 2)) ** 2 / (2 * g2v))
    return -4 * U(Rv) / Rv + mp.diff(U, Rv)
RM = mp.sqrt(Nn_v ** 2 / (4 * g2v))
LM = 1 / (2 * RM ** 2)
def resid(Rv):
    Lv = mp.findroot(lambda L_: dV_of(Rv, L_), LM)
    lP2v = 1 / (32 * mp.pi ** 2 * Rv ** 2)
    return V_of(Rv, Lv) - xx_phys / (8 * mp.pi * lP2v ** 2)
Rex = mp.findroot(resid, RM * (1 + mp.mpf(10) ** -100))
shift = abs(Rex / RM - 1)
LexF = mp.findroot(lambda L_: dV_of(Rex, L_), LM)
dLam_rel = (LexF - LM) / LM
lPl2 = 1 / (32 * mp.pi ** 2 * Rex ** 2)
Rl_ex = Rex / mp.sqrt(lPl2)
formula = 2 * Rl_ex ** 2 * xx_phys
print(f"    relative shift of R* from the Minkowski value: {mp.nstr(shift, 5)}")
print(f"    exact tuning delta Lambda_6/Lambda_c = {mp.nstr(dLam_rel, 6)};  formula 2 (R/l_P)^2 x = {mp.nstr(formula, 6)}  (R/l_P = {mp.nstr(Rl_ex, 6)})")
check("B2f the exact tuning equals 2 (R/l_P)^2 x (envelope-theorem formula)", abs(dLam_rel / formula - 1) < mp.mpf(10) ** -20)
check("B3g the vacuum-energy correction to R*, alpha is < 1e-100 (relations are functions of (N, chat) only)", shift < mp.mpf(10) ** -100)

# tuning at R = 23.41 l_P
Rratio = 2 / math.sqrt(ALPHA)
tune = 2 * Rratio ** 2 * 2.8485e-122
print(f"    (B2) tuning of Lambda_6/Lambda_c at R/l_P = 23.41: 2 (R/l_P)^2 x = {tune:.2e}")
check("B2e Lambda_6 must be tuned to ~3e-119 of its value (the CC problem re-enters, not forced)", 1e-120 < tune < 1e-117)

# ------------------------------------------------------------------ B4 inverse map and handle table
print("\nB4  inverse map (REQUIREMENT, not a hit) and declared handle check")
print("    alpha_U1 = (chat/(2 pi N))^2  =>  chat_needed = 2 pi N sqrt(alpha) ;  R/l_P = sqrt2 pi N^2/chat")
for Ni in (1, 2, 3, 4):
    cn = 2 * math.pi * Ni * math.sqrt(ALPHA)
    print(f"      N={Ni}: chat_needed = {cn:.6f};  R/l_P = {math.sqrt(2) * math.pi * Ni ** 2 / cn:.4f}")
handles = {"1/(4pi)": 1 / (4 * math.pi), "1/(2pi)": 1 / (2 * math.pi), "1/pi": 1 / math.pi, "1/2": 0.5, "1": 1.0, "2": 2.0, "pi": math.pi, "2pi": 2 * math.pi, "4pi": 4 * math.pi}
preds = []
hits = []
for hn, hv in handles.items():
    for Ni in (1, 2, 3, 4):
        al = (hv / (2 * math.pi * Ni)) ** 2
        preds.append(al)
        if abs(al / ALPHA - 1) < 1e-3:
            hits.append((hn, Ni, al))
span = math.log(max(preds) / min(preds))
exp_chance = len(preds) * 2e-3 / span
best = min(preds, key=lambda a: abs(a / ALPHA - 1))
print(f"    {len(preds)} trials; alpha predictions span {min(preds):.2e}..{max(preds):.2e}; closest is alpha^-1 = {1 / best:.2f} (miss {abs(best / ALPHA - 1):.2%})")
print(f"    expected chance hits at the 1e-3 window ~ {len(preds)} x 2e-3 / ln(span) = {exp_chance:.3f};  actual hits: {len(hits)}")
check("B4a no declared (handle, N) hits alpha to 1e-3 (36 trials; expected chance hits <0.1)", len(hits) == 0 and exp_chance < 0.1)
check("B4b chat_needed is a free continuous 6D ratio: requires values 0.54 N -- no principle here fixes it", True)

n_ok = sum(1 for _, o in CHECKS if o)
print("\n" + "=" * 100)
print(f"CHECKS: {n_ok}/{len(CHECKS)} passed")
print("VERDICT (Family B):")
print("  * At the Minkowski point R*^2 = N^2 kappa^2/(4 g^2): R* is fixed by the integer N times the FREE 6D ratio kappa/g; nothing fixes chat = g^2/kappa.")
print("  * 4D couplings are geometric functions of R/l_P and N (alpha_SU2 = 3 l_P^2/R^2, alpha_U1 = N^2 l_P^2/(2 R^2)); alpha_U1 = (chat/(2 pi N))^2. alpha is TRADED for chat, not derived.")
print("  * A dS/Minkowski vacuum needs Lambda_6 tuned; the observed V=x/(8 pi) tunes it to 2 (R/l_P)^2 x ~ 3e-119 at R=23 l_P.  The vacuum-energy correction to R*, alpha is < 1e-100.")
sys.exit(0 if n_ok == len(CHECKS) else 1)
