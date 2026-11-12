#!/usr/bin/env python3
"""PIK2 row 0 (criteria 95edd35e0b): certified variation of the gated dust term L_K = F(Q) S(Pi/Pi_c), F = mu^2 (Q-1)^2/(2K).
  C0a : second-order gate action about FRW in unitary gauge, 3 space dims, general S (Taylor s1, s2, s3), integrated exactly
        over a 3-torus (constant term of a Laurent polynomial in X = e^{ix}, Y = e^{iy}, Z = e^{iz}), against the hand form
        Int a^3 [ -(s1/Pi_c)(F/Q)'(Qb) P^i d_i dQ + (s2/(2 Pi_c^2)) (F/Q)(Qb) (d_i P^i)^2 ].
  C0a': the identity Int sqrt(gamma)(F/Q) Pi = -Int sqrt(gamma) P^i d_i(F/Q), orders eps^1..eps^3 (KA3).
  C0b : static weak-field Euler-Lagrange equations of the gate term (lapse N, generic S, 3D) against the hand forms.
  C2  : energy density -d[N F(1/N)]/dN = (mu^2/2K)(Q^2 - 1).   C3: Pi independent of N at fixed P^i.
  KA4 : Newtonian sub-horizon reduction (row 2's machinery): no P sector -> n = 1 polytrope; with P and S = 1 -> beta = 1;
        general gate -> M = mu^2 + beta k^2, beta = (1+e1)^2/(1 - e2 k^2/K).
  python3 pik2_row0.py            -> pik2_row0.out / .json
  python3 pik2_row0.py --mutate   -> pik2_row0_MUTATE.out / .json  (M-ID: sqrt(gamma) dropped from Pi; M-S2 in the reduction)
kappa = 1/2 FITTED; not theory closed. Adopts nothing."""
import os, sys, json, time
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
MUT = "--mutate" in sys.argv
TAG = "pik2_row0_MUTATE" if MUT else "pik2_row0"
OUT = []; T0 = time.time()
def P(s=""): print(s, flush=True); OUT.append(str(s))
RES = dict(lane="PIK2", file=TAG, criteria="95edd35e0b", checks={})

# ------------------------------------------------------------------ C0a: torus, unitary gauge
X, Y, Z = sp.symbols("X Y Z")            # e^{ix}, e^{iy}, e^{iz}
eps, a, Qb, mu, K, Pc, s1, s2, s3 = sp.symbols("epsilon a Qbar mu K Pi_c s1 s2 s3", positive=True)
I = sp.I
def cosf(v): return (v + 1 / v) / 2
def sinf(v): return (v - 1 / v) / (2 * I)
VARS = (X, Y, Z)
def D(f, i): return sp.expand(I * VARS[i] * sp.diff(f, VARS[i]))     # d/dx_i on Laurent polynomials
def const_term(expr):
    e = sp.expand(expr)
    tot = 0
    for t in sp.Add.make_args(e):
        pw = t.as_powers_dict()
        if all(sp.simplify(pw.get(v, 0)) == 0 for v in VARS):
            tot += t
    return sp.simplify(tot)

# perturbations (real trigonometric fields, rational amplitudes)
nf = cosf(X) + sinf(Y * Z) / 2                                     # lapse: N = (1 + eps nf)/Qb
h = sp.Matrix([[sinf(X * Y) / 3, cosf(Y) / 2, sinf(Z * X) / 5],
               [cosf(Y) / 2, cosf(Z) + cosf(X) / 2, sp.Rational(0)],   # cos(x)/2 added after the first M-ID run (see RESULT)
               [sinf(Z * X) / 5, sp.Rational(0), cosf(X * Z) / 4]])
pv = [sinf(X) + cosf(Y) / 2, cosf(X * Z), sinf(Y) / 3]                # P^i = eps pv_i (upper, coordinate)

def series2(expr, order):
    """Taylor coefficients of expr in eps up to 'order' (list)."""
    out = []
    for n in range(order + 1):
        out.append(sp.expand(sp.diff(expr, eps, n).subs(eps, 0) / sp.factorial(n)))
    return out

# sqrt(gamma) = a^3 sqrt(det(1 + eps h)), truncated at eps^3 (exact series)
detM = sp.expand((sp.eye(3) + eps * h).det())
sq = sp.expand(sum(c * eps ** n for n, c in enumerate(series2(sp.sqrt(detM), 3))))
sqg = a ** 3 * sq
Qf = Qb / (1 + eps * nf)
def Ffun(Q): return mu ** 2 * (Q - 1) ** 2 / (2 * K)
FoQ = Ffun(Qf) / Qf
Svec = [eps * c for c in pv]
if MUT:
    Pi = sum(D(Svec[i], i) for i in range(3))                     # M-ID: sqrt(gamma) dropped
else:
    Pi = sum(D(sqg * Svec[i], i) for i in range(3)) / sqg
u = Pi / Pc
Sm1 = s1 * u + s2 * u ** 2 / 2 + s3 * u ** 3 / 6
Lg = sqg * FoQ * Sm1
P("C0a: expanding the gate term to eps^2 on the torus ...")
c2 = series2(Lg, 2)[2]
full2 = const_term(c2)
# hand form
dQ1 = sp.expand(sp.diff(Qf, eps).subs(eps, 0))          # first-order Q perturbation
FoQp = sp.diff(Ffun(sp.Symbol("q")) / sp.Symbol("q"), sp.Symbol("q")).subs(sp.Symbol("q"), Qb)
FoQb = Ffun(Qb) / Qb
divp = sum(D(pv[i], i) for i in range(3))
hand = a ** 3 * (-(s1 / Pc) * FoQp * sum(pv[i] * D(dQ1, i) for i in range(3)) + (s2 / (2 * Pc ** 2)) * FoQb * divp ** 2)
hand2 = const_term(hand)
diffa = sp.simplify(full2 - hand2)
s3_in = bool(full2.has(s3))
C0a = bool(diffa == 0 and not s3_in)
P(f"  torus-averaged eps^2 coefficient (x (2 pi)^-3):  full = {sp.factor(full2)}")
P(f"  hand form                                      = {sp.factor(hand2)}")
P(f"  difference = {diffa}; s3 present: {s3_in} -> C0a {'PASS' if C0a else 'FAIL'}")
RES["checks"]["C0a"] = dict(full=str(full2), hand=str(hand2), diff=str(diffa), s3_present=s3_in, ok=C0a)
# identity (C0a', KA3): Int sqrt(gamma)(F/Q) Pi + Int sqrt(gamma) P^i d_i (F/Q) = 0 at eps^1..eps^3
lhs = sqg * FoQ * Pi
rhs = -sqg * sum(Svec[i] * D(FoQ, i) for i in range(3))
idres = []
for n, (l, r) in enumerate(zip(series2(lhs, 3), series2(rhs, 3))):
    if n == 0: continue
    idres.append(str(sp.simplify(const_term(l) - const_term(r))))
C0ap = all(v == "0" for v in idres)
P(f"C0a' (KA3) identity Int sqrt(g)(F/Q)Pi = -Int sqrt(g) P.d(F/Q): residual at eps^1..3 = {idres} -> {'PASS' if C0ap else 'FAIL'}")
RES["checks"]["C0a_identity_KA3"] = dict(residuals=idres, ok=C0ap)
# reading of the result in physical terms
qb = sp.Symbol("qbar", positive=True)
rho_bar = mu ** 2 * (Qb ** 2 - 1) / (2 * K)
P(f"  (F/Q)'(Qb) = {sp.simplify(FoQp)} = rho_bar/Qb^2 with rho_bar = (mu^2/2K)(Qb^2 - 1): {sp.simplify(FoQp - rho_bar / Qb ** 2) == 0}")
RES["checks"]["FoQ_prime_is_rho_over_Q2"] = bool(sp.simplify(FoQp - rho_bar / Qb ** 2) == 0)

# ------------------------------------------------------------------ C0b, C2, C3: static weak field
x, y, z = sp.symbols("x y z", real=True)
Nf = sp.Function("N")(x, y, z)
P1, P2, P3 = [sp.Function(f"P{i}")(x, y, z) for i in (1, 2, 3)]
Sf = sp.Function("S")
PiS = sp.diff(P1, x) + sp.diff(P2, y) + sp.diff(P3, z)        # static, flat leaves at this order (sqrt(gamma) = 1)
NF = Nf * Ffun(1 / Nf)
Lst = NF * Sf(PiS / Pc)
eqs = sp.euler_equations(Lst, [Nf, P1, P2, P3], [x, y, z])
# hand: lapse eq: d[N F(1/N)]/dN S ; P_i eq: -d_i [N F(1/N) S'(u)/Pi_c]
nsym = sp.Symbol("n", positive=True)
dNF = sp.diff(nsym * Ffun(1 / nsym), nsym).subs(nsym, Nf)
hand_N = dNF * Sf(PiS / Pc)
Sp = sp.Subs(sp.Derivative(Sf(sp.Symbol("w")), sp.Symbol("w")), sp.Symbol("w"), PiS / Pc).doit()
GmN = NF * sp.Derivative(Sf(sp.Symbol("w")), sp.Symbol("w")).subs(sp.Symbol("w"), PiS / Pc) / Pc
hand_P = [-sp.diff(GmN, v) for v in (x, y, z)]
rN = sp.simplify(eqs[0].lhs - hand_N)
rP = [sp.simplify((eqs[i + 1].lhs - hand_P[i]).doit()) for i in range(3)]
C0b = bool(rN == 0 and all(r == 0 for r in rP))
P(f"C0b static weak field: lapse-equation residual {rN}; P-equation residuals {rP} -> {'PASS' if C0b else 'FAIL'}")
RES["checks"]["C0b"] = dict(lapse=str(rN), P=[str(r) for r in rP], ok=C0b)
Qs = sp.Symbol("Q", positive=True)
e_dens = sp.simplify(-sp.diff(nsym * Ffun(1 / nsym), nsym).subs(nsym, 1 / Qs))
C2 = bool(sp.simplify(e_dens - mu ** 2 * (Qs ** 2 - 1) / (2 * K)) == 0)
P(f"C2 energy density -d[N F(1/N)]/dN = {sp.factor(e_dens)} -> {'PASS' if C2 else 'FAIL'} (so the gated term's density is S x the quadratic's)")
Phi = sp.Symbol("Phi")
lead = sp.series(e_dens.subs(Qs, 1 / (1 + Phi)), Phi, 0, 2).removeO()
P(f"   leading order with N = 1 + Phi: energy density = {sp.simplify(lead)}  (dust rho_K = -mu^2 S Phi / K, K = 4 pi G)")
C3 = bool(sp.diff(PiS, Nf) == 0)
P(f"C3 Pi independent of the lapse at fixed P^i: {C3} (Q sqrt(-g) = sqrt(gamma) has no N)")
RES["checks"]["C2"] = dict(value=str(e_dens), ok=C2); RES["checks"]["C3"] = dict(ok=C3)
# law shift in SI: c^2 Gm = mu^2 Phi^2 S'/(8 pi G rho_c)  (F with Q-1 = -Phi/c^2, K = 4 pi G/c^4, Pi_c = c^2 rho_c)
Gn, c, rc, Ph, Spr = sp.symbols("G c rho_c Phi Sprime", positive=True)
c2Gm = sp.simplify(c ** 2 * (mu ** 2 * (Ph / c ** 2) ** 2 / (2 * 4 * sp.pi * Gn / c ** 4)) * Spr / (c ** 2 * rc))
P(f"   law shift c^2 Gm = {c2Gm}  (Newtonian; c cancels)")
RES["checks"]["c2Gm_SI"] = str(c2Gm)

# ------------------------------------------------------------------ KA4 / row 2 reduction: Newtonian sub-horizon, one Fourier mode
kk, rho, om = sp.symbols("k rhobar omega", positive=True)
ph, ps, ch, v, p = sp.symbols("phi psi c v p", real=True)
e1, e2 = sp.symbols("e1 e2", real=True)
xx = sp.Symbol("x", real=True)
def avg(expr):   # average over one period of kx
    return sp.simplify(sp.integrate(sp.expand(expr), (xx, 0, 2 * sp.pi / kk)) * kk / (2 * sp.pi))
Phif, Psif, chif, vf, Pf = ph * sp.sin(kk * xx), ps * sp.sin(kk * xx), ch * sp.sin(kk * xx), v * sp.sin(kk * xx), p * sp.cos(kk * xx)
dQ = vf - Phif
s2sign = -1 if MUT else 1
def L2(withP=True, gate=True):
    L = (sp.diff(Psif, xx) ** 2 - 2 * sp.diff(Phif, xx) * sp.diff(Psif, xx)) / (2 * K) - rho * sp.diff(chif, xx) ** 2 / 2 + mu ** 2 * dQ ** 2 / (2 * K)
    if withP:
        g1 = e1 if gate else 0; g2 = s2sign * e2 if gate else 0
        L += -(1 + g1) * Pf * sp.diff(dQ, xx) - K * Pf ** 2 / 2 + g2 * sp.diff(Pf, xx) ** 2 / 2
    return avg(L)
def reduce_(Lavg):
    aux = [p, ph, ps] if Lavg.has(p) else [ph, ps]
    sol = sp.solve([sp.diff(Lavg, q) for q in aux], aux, dict=True)[0]
    Le = sp.simplify(Lavg.subs(sol))
    A = sp.simplify(2 * sp.diff(Le, v, 2) / 2); B = sp.simplify(-2 * sp.diff(Le, ch, 2) / 2)
    return Le, A, B, sp.simplify(B / A)
_, A0_, B0_, w2_noP = reduce_(L2(withP=False))
poly = sp.simplify(w2_noP - K * rho * (kk ** 2 / mu ** 2 - 1))
P(f"KA4 (no P sector): omega^2 = {sp.factor(w2_noP)}; minus K rho (k^2/mu^2 - 1) = {poly} -> {'PASS' if poly == 0 else 'FAIL'}")
_, A1_, B1_, w2_S1 = reduce_(L2(withP=True, gate=False))
Mexpr = mu ** 2 + kk ** 2
r1 = sp.simplify(w2_S1 - K * rho * (kk ** 2 / Mexpr - 1))
P(f"KA4 (with P, S = 1): omega^2 = {sp.factor(w2_S1)}; minus K rho (k^2/(mu^2 + k^2) - 1) = {r1} -> {'PASS' if r1 == 0 else 'FAIL'} (beta = 1)")
_, Ag, Bg, w2_g = reduce_(L2(withP=True, gate=True))
beta = (1 + e1) ** 2 / (1 - e2 * kk ** 2 / K)
rg = sp.simplify(w2_g - K * rho * (kk ** 2 / (mu ** 2 + beta * kk ** 2) - 1))
P(f"Row 2 reduction (gate): omega^2 = {sp.factor(w2_g)}; minus K rho (k^2/M - 1), M = mu^2 + beta k^2, beta = (1+e1)^2/(1 - e2 k^2/K): {rg} -> "
  f"{'PASS' if rg == 0 else 'FAIL'}")
P(f"   kinetic coefficient of v (= chi-dot) after eliminating P, Phi, Psi: {sp.factor(Ag)}")
ka4 = bool(poly == 0 and r1 == 0)
RES["checks"]["KA4"] = dict(noP=str(w2_noP), S1=str(w2_S1), ok=ka4)
RES["checks"]["row2_reduction"] = dict(omega2=str(w2_g), residual=str(rg), ok=bool(rg == 0), kinetic=str(Ag))
if MUT:
    P(f"M-S2 (sign of the s2 term flipped): the reduction residual against the unflipped hand form is {rg} (must be non-zero) -> "
      f"{'BITES' if rg != 0 else 'DOES NOT BITE'}")
    P(f"M-ID (sqrt(gamma) dropped from Pi): C0a {'PASS (DOES NOT BITE)' if C0a else 'FAIL (BITES)'}")
    RES["mutate"] = dict(M_ID_C0a_fails=not C0a, M_S2_reduction_moves=bool(rg != 0))
allok = all(RES["checks"][k]["ok"] for k in ("C0a", "C0a_identity_KA3", "C0b", "C2", "C3", "KA4", "row2_reduction"))
RES["all_pass"] = allok
P(f"\nRow 0 / KA3 / KA4: {'ALL PASS' if allok else 'NOT ALL PASS'}   runtime {time.time() - T0:.0f} s")
P("kappa = 1/2 FITTED; not theory closed. Adopts nothing.")
json.dump(RES, open(os.path.join(HERE, TAG + ".json"), "w"), indent=1)
open(os.path.join(HERE, TAG + ".out"), "w").write("\n".join(OUT) + "\n")
