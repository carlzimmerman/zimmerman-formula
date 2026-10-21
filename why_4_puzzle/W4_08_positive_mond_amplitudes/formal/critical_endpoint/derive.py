#!/usr/bin/env python3
"""W4-08 critical endpoint -- symbolic part (M1, M2, M3, M5, M7 of FROZEN_CRITERIA.md, committed alone 582bbb7ad).

Action: S = (B/2) int sqrt(-g)[R + m^2 F(I)] + S_m,  I = (c2 K^2 - c1 a.a)/m^2, hypersurface-orthogonal clock.
Light: sympy only, one core, seconds. Run from the repo root:
    python3 why_4_puzzle/W4_08_positive_mond_amplitudes/formal/critical_endpoint/derive.py > .../derive.out
kappa = 1/2 FITTED. Not theory closed.
"""
import json, os, re, sys
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
OUT, checks, res = [], [], {}


def P(s=""):
    print(s); OUT.append(str(s))


def check(name, detail, ok):
    checks.append({"name": name, "detail": str(detail), "pass": bool(ok)})
    P(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}")


# ---------------------------------------------------------------- M1 exact kinematics
P("M1  exact kinematics of a stationary radial clock flow on ds^2 = -A dt^2 + Br dr^2 + r^2 dOmega^2")
t, r, th, ph = sp.symbols("t r theta phi", real=True)
X = [t, r, th, ph]
A, Br, v = sp.Function("A")(r), sp.Function("B_r")(r), sp.Function("v")(r)
g = sp.diag(-A, Br, r ** 2, r ** 2 * sp.sin(th) ** 2)
ginv = g.inv()


def christoffel(g, ginv):
    G = [[[0] * 4 for _ in range(4)] for _ in range(4)]
    for l in range(4):
        for m in range(4):
            for n in range(4):
                G[l][m][n] = sp.simplify(sum(ginv[l, k] * (sp.diff(g[k, m], X[n]) + sp.diff(g[k, n], X[m]) - sp.diff(g[m, n], X[k]))
                                             for k in range(4)) / 2)
    return G


Gam = christoffel(g, ginv)
ut = sp.sqrt((1 + Br * v ** 2) / A)                     # unit normalisation: -A ut^2 + Br v^2 = -1
uU = [ut, v, 0, 0]
uL = [sum(g[i, j] * uU[j] for j in range(4)) for i in range(4)]
sqrtg = sp.sqrt(A * Br) * r ** 2                          # angular factor sin(theta) cancels in the divergence
K_exact = sp.simplify(sp.diff(sqrtg * v, r) / sqrtg)
a_r = sp.simplify(sum(uU[n] * (sp.diff(uL[1], X[n]) - sum(Gam[l][n][1] * uL[l] for l in range(4))) for n in range(4)))
a_t = sp.simplify(sum(uU[n] * (sp.diff(uL[0], X[n]) - sum(Gam[l][n][0] * uL[l] for l in range(4))) for n in range(4)))
P(f"  K   = {K_exact}")
P(f"  a_r = {a_r}")
# hypersurface orthogonality is automatic for a radial flow; a.u = 0 check
adotu = sp.simplify(sum(ginv[i, j] * [a_t, a_r, 0, 0][i] * uL[j] for i in range(4) for j in range(4)))
H, M = sp.symbols("H M", positive=True)
dS = {A: 1 - H ** 2 * r ** 2, Br: 1 / (1 - H ** 2 * r ** 2), v: H * r}
PG = {A: 1 - 2 * M / r, Br: 1 / (1 - 2 * M / r), v: -sp.sqrt(2 * M / r)}


def on(expr, sub):
    e = expr
    for f, val in sub.items():
        e = e.subs(f, val)
    return sp.simplify(e.doit())


K_dS, a_dS = on(K_exact, dS), on(a_r, dS)
K_PG, a_PG = on(K_exact, PG), on(a_r, PG)
P(f"  de Sitter flat slicing (A = 1 - H^2 r^2, v = H r): K = {K_dS}, a_r = {a_dS}")
P(f"  Painleve-Gullstrand Schwarzschild (v = -sqrt(2M/r)): K = {K_PG}, a_r = {a_PG}")
check("K1 exact identities: a.u = 0; dS flat slicing K = 3H, a = 0; PG a = 0", f"a.u {adotu}; {K_dS}, {a_dS}; {a_PG}",
      adotu == 0 and sp.simplify(K_dS - 3 * H) == 0 and a_dS == 0 and a_PG == 0)

# weak-field reduction: A = 1 + 2 eps Phi, Br = 1 - 2 eps Psi, v = sqrt(eps) V (v^2 ~ Phi ordering)
eps = sp.symbols("epsilon", positive=True)
Phi, Psi, V = sp.Function("Phi")(r), sp.Function("Psi")(r), sp.Function("V")(r)
wf = {A: 1 + 2 * eps * Phi, Br: 1 - 2 * eps * Psi, v: sp.sqrt(eps) * V}
K_wf = sp.series(on(K_exact, wf) / sp.sqrt(eps), eps, 0, 1).removeO()
a_wf = sp.series(on(a_r, wf) / eps, eps, 0, 1).removeO()
P(f"  weak field, leading order: K = sqrt(eps) * [{sp.simplify(K_wf)}];  a_r = eps * [{sp.simplify(a_wf)}]")
res["K_leading"] = str(sp.simplify(K_wf)); res["a_leading"] = str(sp.simplify(a_wf))
check("M1 leading forms K = (r^2 v)'/r^2, a_r = Phi' + v v'",
      f"{sp.simplify(K_wf - sp.diff(r ** 2 * V, r) / r ** 2)}, {sp.simplify(a_wf - sp.diff(Phi, r) - V * sp.diff(V, r))}",
      sp.simplify(K_wf - sp.diff(r ** 2 * V, r) / r ** 2) == 0 and sp.simplify(a_wf - sp.diff(Phi, r) - V * sp.diff(V, r)) == 0)

# ---------------------------------------------------------------- M2 reduced field equations
P("\nM2  Newtonian-limit reduced Lagrangian per (B/2) 4 pi dr:  L = r^2[2 Psi'^2 - 4 Phi' Psi' + m^2 F(I)] - (2/B) rho r^2 Phi")
c1, c2, m, Bc = sp.symbols("c1 c2 m B", real=True)
F = sp.Function("F")
rho = sp.Function("rho")(r)
Kx = sp.diff(r ** 2 * V, r) / r ** 2
ax = sp.diff(Phi, r) + V * sp.diff(V, r)
Ix = (c2 * Kx ** 2 - c1 * ax ** 2) / m ** 2
L = r ** 2 * (2 * sp.diff(Psi, r) ** 2 - 4 * sp.diff(Phi, r) * sp.diff(Psi, r) + m ** 2 * F(Ix)) - 2 / Bc * rho * r ** 2 * Phi
EL = {f: sp.euler_equations(L, [f], r)[0].lhs for f in (Phi, Psi, V)}
Fp = sp.simplify(sp.diff(F(Ix), r) / sp.diff(Ix, r))     # F'(I) in the same Subs form sympy uses
# claimed forms: Psi: (r^2(4Psi' - 4Phi'))' = 0;  Phi: (r^2(4Psi' - 2 alpha_I a))' = (2/B) rho r^2;  khronon: r^2 (c2 F' K)' + V (r^2 alpha_I a)' = 0
alphaI = -c1 * Fp
claim_Psi = sp.diff(r ** 2 * (4 * sp.diff(Psi, r) - 4 * sp.diff(Phi, r)), r)
claim_Phi = sp.diff(r ** 2 * (4 * sp.diff(Psi, r) - 2 * alphaI * ax), r) - 2 / Bc * rho * r ** 2
claim_V = r ** 2 * sp.diff(c2 * Fp * Kx, r) + V * sp.diff(r ** 2 * alphaI * ax, r)
dPsi = sp.simplify(EL[Psi] + claim_Psi)
dPhi = sp.simplify(sp.expand(EL[Phi] - claim_Phi))
ratio_V = sp.simplify(sp.expand(EL[V]) / sp.expand(claim_V))
P(f"  Psi equation  == -(r^2(4Psi' - 4Phi'))'                 residual {dPsi}")
P(f"  Phi equation  == (r^2(4Psi' - 2 alpha_I a))' - (2/B) rho r^2      residual {dPhi}")
P(f"  khronon (V)   == {ratio_V} x [r^2 (c2 F'(I) K)' + V (r^2 alpha_I a)']")
check("M2 Euler-Lagrange equations have the stated forms", f"Psi {dPsi}, Phi {dPhi}, V ratio {ratio_V}",
      dPsi == 0 and dPhi == 0 and sp.simplify(ratio_V + 2) == 0)

# K2: ADM cross-check. With Psi = Phi, the Phi equation integrates (outside sources) to r^2 alpha_I a = 2 r^2 phi' - 2GM, so
# (r^2 alpha_I a)' = 2 (r^2 phi')'. With V = H r the integrated khronon equation gives
#   c2 F'K - c2 F'(I0) K0 = int_r^inf V (r^2 alpha_I a)'/r^2 = 2 H int_r^inf (s^2 phi')'/s ds = -2H (phi + r phi')  (phi -> 0 at inf)
s_, Hs = sp.symbols("s H_s", positive=True)
phi = sp.Function("phi")
Pi = -2 * Hs * (phi(r) + r * sp.diff(phi(r), r))          # claimed: c2 F'K - c2 F'(I0) K0 (phi, r phi' -> 0 at infinity)
integrand = 2 * Hs * sp.diff(r ** 2 * sp.diff(phi(r), r), r) / r   # V (r^2 alpha_I a)'/r^2 with V = H r, (r^2 alpha_I a)' = 2 (r^2 phi')'
ibp = sp.simplify(sp.diff(Pi, r) + integrand)
P(f"  covariant: d/dr[-2H(phi + r phi')] + 2H (r^2 phi')'/r = {ibp}  (so Pi(r) = int_r^inf of the khronon source)")
# ADM (SINGLE_FUNCTION sec. 4-5 variables, unitary gauge): U = zetadot - H n, with n = phi and zeta = -phi for a field static in
# physical coordinates (zetadot = H r d zeta/dr). Linearised trace: c2[F'(I) K - F'(I0) K0] = c2 Q dK = (1 - lambda) dK and the
# shift equation of SINGLE_FUNCTION sec. 5 gives dK = 3U - S U/(lambda - 1) = -2U/(lambda - 1). Hence (1 - lambda) dK = 2U.
lam, Usym = sp.symbols("lambda U")
U_adm = sp.simplify(Hs * r * sp.diff(-phi(r), r) - Hs * phi(r))
dK_adm = sp.simplify(3 * Usym - (3 * lam - 1) * Usym / (lam - 1))
lin = sp.simplify((1 - lam) * dK_adm)
P(f"  ADM (SINGLE_FUNCTION sec. 5): dK = {dK_adm};  (1 - lambda) dK = {lin};  U = {U_adm}")
cov_closed = Pi
adm_closed = sp.simplify((lin / Usym) * U_adm)
check("K2 covariant khronon equation == ADM momentum constraint (linear order, static in physical coordinates)",
      f"covariant {cov_closed}; ADM {adm_closed}; ibp residual {ibp}", sp.simplify(cov_closed - adm_closed) == 0 and ibp == 0)
check("K4 flat-static limit (H -> 0, V -> 0): Phi equation gives mu = 1 + c1 F'/2",
      sp.simplify((4 - 2 * alphaI) / 4), sp.simplify((4 - 2 * alphaI) / 4 - (1 + c1 * Fp / 2)) == 0)

# ---------------------------------------------------------------- M3 endpoint closed forms
P("\nM3  endpoint alpha(I0) = 2.  Leading sub-horizon system (back-reaction U and convective v v' dropped; kept in numerics):")
P("      khronon:  alpha_I(I) K = 2 K0           (from c2 F'(I) K = c2 F'(I0) K0 and alpha_I = -c1 F')")
P("      Phi:      (2 - alpha_I) g = 2 G M / r^2  ->  mu_eff = 1 - alpha_I/2,   x = I - I0 = [ -|c2|(K^2 - K0^2) + |c1| g^2 ]/m^2")
gg, aM, xa, K0 = sp.symbols("g a_M x_a K_0", positive=True)
C1, C2 = sp.symbols("C1 C2", positive=True)          # |c1|, |c2|
mm = sp.symbols("m", positive=True)
y = sp.symbols("y", positive=True)
# E-cusp, deep: alpha = 2(1 - p), p = y = sqrt(x/x_a); K = K0/(1-p) ~ K0(1+p); x_a = |c1| a_M^2/m^2
pdeep = sp.solve(sp.Eq(mm ** 2 * (C1 * aM ** 2 / mm ** 2) * y ** 2, C1 * gg ** 2 - 2 * C2 * K0 ** 2 * y), y)
pdeep = [s for s in pdeep if s.subs({gg: 1, aM: 1, K0: 1, C1: 1, C2: sp.Rational(1, 100)}).is_positive][0]
eta = sp.symbols("eta", positive=True)
mu_deep = sp.simplify(pdeep)
target_form = (sp.sqrt(eta ** 2 + gg ** 2) - eta) / aM
eta_def = C2 * K0 ** 2 / (C1 * aM)
P(f"  E-cusp deep regime: mu_eff = {mu_deep}")
check("M3 closed form mu_eff = (sqrt(eta^2 + g^2) - eta)/a_M with eta = |c2| K0^2/(|c1| a_M) = 9(|c2|/|c1|) H^2/a_M",
      sp.simplify(mu_deep - target_form.subs(eta, eta_def)), sp.simplify(mu_deep - target_form.subs(eta, eta_def)) == 0)
P(f"    limits: g >> eta: mu -> {sp.limit(target_form / gg * aM, gg, sp.oo)} * g/a_M (deep MOND);  g << eta: mu -> {sp.series(target_form, gg, 0, 3).removeO()} (quartic)")
# E-cusp exact for the declared p(y) = y/(1+y): alpha = 2/(1+y), K = K0 (1+y)
yex = sp.solve(sp.Eq(C1 * aM ** 2 * y ** 2, C1 * gg ** 2 - C2 * K0 ** 2 * ((1 + y) ** 2 - 1)), y)
yex = [s for s in yex if s.subs({gg: 1, aM: 1, K0: 1, C1: 1, C2: sp.Rational(1, 100)}).is_positive][0]
P(f"  E-cusp declared p(y) = y/(1+y): y(g) = {sp.simplify(yex)},  mu_eff = y/(1+y),  K = K0 (1 + y)")
res["E_cusp_y"] = str(sp.simplify(yex))
# E-reg: alpha = 2/(1 + x/x_a); K = K0(1 + x/x_a)
z = sp.symbols("z", positive=True)                     # z = x/x_a
zsol = sp.solve(sp.Eq(C1 * aM ** 2 * z, C1 * gg ** 2 - C2 * K0 ** 2 * ((1 + z) ** 2 - 1)), z)
zsol = [s for s in zsol if s.subs({gg: sp.Rational(1, 10), aM: 1, K0: 1, C1: 1, C2: sp.Rational(1, 100)}).is_positive][0]
mu_reg = sp.series(sp.simplify(zsol / (1 + zsol)), gg, 0, 3).removeO()
P(f"  E-reg (alpha = 2/(1 + x/x_a)): mu_eff = z/(1+z), small g: mu = {sp.simplify(mu_reg)}  (quartic; no linear-in-g term)")
check("M3 E-reg has no MOND term: d mu/dg at g = 0 vanishes", sp.diff(sp.simplify(zsol / (1 + zsol)), gg).subs(gg, 0),
      sp.simplify(sp.diff(sp.simplify(zsol / (1 + zsol)), gg).subs(gg, 0)) == 0)
# point-mass laws
GM = sp.symbols("GM", positive=True)
P(f"  point mass: deep MOND g = sqrt(GM a_M)/r for eta << g << a_M; quartic g = (2 eta a_M GM/r^2)^(1/3) for g << eta")
P(f"  crossover h_c = 2 eta = 18 (|c2|/|c1|) H^2/a_M (K0 = 3H)")

# ---------------------------------------------------------------- M5 the delta-K direction and k = 0
P("\nM5  the delta-K direction")
P("  Constraint (fixed a, U): c2 [F'(I) K - F'(I0) K0] = 2U, I = (c2 K^2 - c1 a^2)/m^2.")
P("  d/dK [F'(I) K] = F'(I) + 2 (c2 K^2/m^2) F''(I) = Q(I) at the background; the cusp gives F'' -> -inf with c2 K^2/m^2 = I0 < 0,")
P("  so Q -> +inf and lambda_eff = 1 - c2 Q -> +inf (c2 < 0): the map K -> F'(I)K is strictly monotone and the constraint")
P("  fixes delta K uniquely. Linearising: (1 - lambda) dK = 2U -> dK = -2U/(lambda - 1) -> 0 as lambda -> inf.")
lam_ = sp.symbols("lambda", positive=True)
C_red = 2 * (3 * lam_ - 1) / (lam_ - 1)
P(f"  reduced scalar coefficient C = 2S/(lambda - 1) -> {sp.limit(C_red, lam_, sp.oo)} as lambda -> inf (finite; SINGLE_FUNCTION sec. 5)")
Xs, Hh = sp.symbols("X H", positive=True)
Cv = sp.limit(C_red, lam_, sp.oo)
Kz = Cv * 2 * Xs / (Cv * Hh ** 2 + 2 * Xs)
Vz = 2 * Xs ** 2 * (Cv * 4 * Hh ** 2) / (Cv * Hh ** 2 + 2 * Xs) ** 2
P(f"  at alpha = 2: K_z = {sp.simplify(Kz)} > 0, V_z = {sp.simplify(Vz)} > 0, principal c_s^2 = 2(2 - alpha)/(C alpha) = 0;"
  f" sub-horizon Omega^2 -> {sp.limit(Vz / Kz, Xs, sp.oo)}")
res["delta_K"] = "fixed by a strictly monotone constraint; lambda_eff -> inf; C -> 6; c_s^2 = 0 at alpha = 2"
P("  k = 0: added matter raises H^2, so I = 9 c2 H^2/m^2 moves to I < I0 (c2 < 0), the side opposite to the static sources (x >= 0).")
P("  The homogeneous matter response therefore uses the regular opposite branch: G_cos = 2 G_bare/S_left. The cusp")
P("  (x >= 0 side) is reached only by H^2 < H0^2.")

# ---------------------------------------------------------------- M7 amplitudes (no target here)
P("\nM7  operational amplitudes on the same state (E-cusp)")
Hq, aq, Bq = sp.symbols("H a_M B", positive=True)
C2op, C3op, epsop = Bq, 2 * Bq / (3 * aq), 3 * Bq * Hq ** 2
Ramp = sp.simplify(epsop * C3op ** 2 / C2op ** 3)
P(f"  C2 = B (Newton regime alpha_I -> 0), C3 = 2B/(3 a_M), eps = 3 B H^2 (actual de Sitter stress)  ->  R_amp = {Ramp}")
I0s = sp.symbols("I_0", negative=True)
c1n, c2n = sp.symbols("c1 c2", negative=True)
H2 = mm ** 2 * I0s / (9 * c2n)
aM2 = mm ** 2 * xa / (-c1n)
Ramp_par = sp.simplify(Ramp.subs(Hq, sp.sqrt(H2)).subs(aq, sp.sqrt(aM2)))
P(f"  in F's parameters (H^2 = m^2 I0/(9 c2), a_M^2 = m^2 x_a/|c1|): R_amp = {Ramp_par}")
res["R_amp"] = str(Ramp_par)
F0 = sp.solve(sp.Eq(3 * H2, mm ** 2 / 2 * (2 * I0s * (-2 / c1n) - sp.Symbol("F_I0"))), sp.Symbol("F_I0"))[0]
P(f"  tunings: T1 criticality F'(I0) = -2/c1;  T2 vacuum at the cusp: F(I0) = {sp.simplify(F0)}")
P("  P1 a kink (F' jump) at I0 can pin the Friedmann root there for an open range of F(I0) (removes T2, not T1); H then")
P("     ignores matter up to a threshold density (a plateau), and R_amp is unchanged in form.")
P("  P2 the deep static equation div(|grad phi| grad phi) ~ a_M rho is scale invariant for every a_M: exponent fixed, amplitude free.")
P("  P3 the opposite-branch deformation (I < I0, flat at I0) leaves F(I0), F'(I0), the cusp, the vacuum and the MOND law")
P("     unchanged and alters only the homogeneous matter response (G_cos): not excluded, not relevant to R_amp.")
P("     The constant shift of F is fixed by T2 (it would move the root off the cusp and destroy criticality).")
P("  Surviving parameters in R_amp: |c1|/|c2| and |I0|/x_a (with the window |c2|/|c1| << a_M h_min/(18 H^2)).")

# ---------------------------------------------------------------- TARGET COMPARISON (only place the target appears)
src = open(os.path.abspath(__file__)).read()
blk = src.split("# ---------------------------------------------------------------- M1 exact")[1].split("# ---------------------------------------------------------------- TARGET COMPARISON")[0]
bad = [p for p in (r"128\s*\*?\s*sp\.pi", r"32\s*\*\s*sp\.pi", r"5\.78", r"Rational\(\s*1\s*,\s*4\s*\)\s*#\s*xi") if re.search(p, blk)]
check("I1 no target value in the compute blocks", bad or "clean", not bad)
target = 128 * sp.pi / 9
need = sp.sqrt(3 * target / 4)
P(f"\nTARGET COMPARISON: R_amp = 128 pi/9 requires H/a_M = {sp.simplify(need)} = {float(need):.4f}; equivalently "
  f"(|c1|/|c2|)(|I0|/x_a) = {sp.nsimplify(sp.simplify(target * 27 / 4))} = {float(target * 27 / 4):.2f}. No declared principle fixes either.")
res["verdict_target"] = "NOT SELECTED"
json.dump(dict(results=res, checks=checks), open(os.path.join(HERE, "derive_results.json"), "w"), indent=1, default=str)
P(f"\nchecks: {sum(c['pass'] for c in checks)}/{len(checks)} pass")
sys.exit(0 if all(c["pass"] for c in checks) else 1)
