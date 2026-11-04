"""CT6 candidate B, gate G0 (health). Symbolic checks only (sympy, single thread).

Units: c = 1, 8 pi G = 1 (M^2/2 = c0 = 1/2 in front of R). Host action (V3_FULL_PICTURE.md:23-31):
  L = (1/2)[R - 2 J(Y)] + K_BS(Q) + ...,  J = Lambda - G(Y, A),  G = 2 A [u - ln(1+u)],  u = sqrt(Y)/sqrt(A),
with candidate B's replacement A = a_geo^2 = xi * Qp,  Qp = K^2/3 + (2/3) L_n K.
"""
import sympy as sp

out = []
def p(*a):
    s = " ".join(str(x) for x in a)
    print(s); out.append(s)

# ---------------------------------------------------------------- 1. FRW identity and integration by parts
t = sp.symbols('t')
a = sp.Function('a')(t); N = sp.Function('N')(t); mu = sp.Function('mu')(t)
Lam, rho, pr = sp.symbols('Lambda rho p')
K = 3*sp.diff(a, t)/(N*a)                      # trace of extrinsic curvature of FRW leaves
LnK = sp.diff(K, t)/N
Qp = K**2/3 + sp.Rational(2, 3)*LnK
H, Hd = sp.symbols('H Hdot')
Qp_N1 = sp.simplify(Qp.subs(N, 1).doit())
Qp_H = sp.simplify(Qp_N1.subs(sp.diff(a, t, 2), (Hd + H**2)*a).subs(sp.diff(a, t), H*a))
p("1a Qp on FRW (N=1) =", Qp_H, "  [expect 3H^2 + 2Hdot]")
# Friedmann (8piG=1): 3H^2 = rho + Lambda, 2Hdot = -(rho + p)
p("1b with Friedmann: Qp =", sp.simplify(Qp_H.subs({H**2: (rho+Lam)/3}).subs(Hd, -(rho+pr)/2)), "  [expect Lambda - p: dust cancels]")
# sqrt(-g) mu L_nK = d/dt(a^3 mu K) - sqrt(-g)[K L_n mu + mu K^2]
lhs = sp.diff(a**3*mu*K, t)
rhs = N*a**3*(mu*LnK + K*sp.diff(mu, t)/N + mu*K**2)
p("1c IBP identity residual:", sp.simplify(lhs - rhs), "  => mu*Qp = -(mu/3)K^2 - (2/3)K L_n mu + total derivative")

# ---------------------------------------------------------------- 2. MOND-sector function and its A-derivatives
Y, A, s, uu, xi = sp.symbols('Y A s u xi', positive=True)
G = 2*sp.sqrt(A)*s - 2*A*sp.log(1 + s/sp.sqrt(A))      # s = sqrt(Y)
G_A = sp.simplify(sp.diff(G, A))
G_AA = sp.simplify(sp.diff(G, A, 2))
G_A_u = sp.simplify(G_A.subs(s, uu*sp.sqrt(A)))
G_AA_u = sp.simplify((G_AA*A).subs(s, uu*sp.sqrt(A)))
f_u = 2*uu - 4*sp.log(1+uu) + 2*uu/(1+uu)
p("2a dG/dA =", G_A_u, "; equals f(u)/2 with f = 2u - 4ln(1+u) + 2u/(1+u):", sp.simplify(G_A_u - f_u/2) == 0)
p("2b f'(u) =", sp.simplify(sp.diff(f_u, uu)), " >= 0 and f(0) = 0  => dG/dA > 0 for u > 0")
p("2c A*d2G/dA2 =", G_AA_u, "  [expect -u^3/(2(1+u)^2) < 0]")
ser = sp.series(G.subs(s, sp.sqrt(Y)), Y, 0, 3).removeO()
p("2d small-Y expansion G =", sp.simplify(sp.expand(ser)), "  => A-dependence starts at Y^(3/2); dG/dY|_{Y=0} =",
  sp.limit(sp.diff(G.subs(s, sp.sqrt(Y)), Y), Y, 0))
p("2e deep-MOND scale invariance: the Y^(3/2) term carries A^(-1/2) = (xi Qp)^(-1/2): nonlinear in Qp, so no choice keeps the")
p("   law and makes the action linear in L_n K (linear-in-Qp would be needed for degeneracy).")
p("2f static leaves (K = 0, L_nK = 0 => Qp = 0): dG/dA at fixed s as A->0:", sp.limit(G_A, A, 0, '+'), " (diverges like s/sqrt(A))")

# P-form of v3s (X15 FROZEN_CRITERIA.md:31-32): W = (A/Kc)[-w/sqrt(A) - ln(1 - w/sqrt(A))], w = Kc|P|
w, Kc = sp.symbols('w K_c', positive=True)
W = (A/Kc)*(-w/sp.sqrt(A) - sp.log(1 - w/sp.sqrt(A)))
p("2g P-form W small-w series:", sp.series(W, w, 0, 4).removeO(), " => A enters first at w^3 here too")

# ---------------------------------------------------------------- 3. minisuperspace Ostrogradsky Hessian
add = sp.symbols('addot')
ad, aa, NN = sp.symbols('adot a N', positive=True)
Qp_ms = sp.simplify((Qp.subs(sp.diff(a, t, 2), add).subs(sp.diff(N, t), 0).subs(sp.diff(a, t), ad)).subs({a: aa, N: NN}))
p("3a Qp(a, adot, addot, N) =", Qp_ms)
p("3b d Qp / d addot =", sp.simplify(sp.diff(Qp_ms, add)), " ; Hessian of A(Qp) in addot = A''(Qp) * (that)^2")
p("   On FRW Y = 0 so A(Qp) = G(0, xi Qp) = 0 identically: Hessian 0, no extra DOF on FRW.")
p("   Where Y > 0: A'' = xi^2 d2G/dA2 != 0 (2c): non-degenerate, one extra scalar DOF (Ostrogradsky pair).")

# ---------------------------------------------------------------- 4. quadratic unitary-gauge action, frozen coefficients
# Flat frozen background with lapse gradient abar (Y > 0), k perpendicular to abar (cross terms abar.k vanish).
# Fields: zeta, X = K = 3 zetadot + k^2 psi (psi auxiliary <=> X auxiliary for k != 0), n (lapse, auxiliary), dmu.
# Auxiliary form of A(Qp): mu*Qp - Vt(mu), Vt'' = 1/A_QQ;  mu*Qp -> -(mu/3)K^2 - (2/3) K L_n mu.
c0 = sp.Rational(1, 2)
zd, md, z, m_, n_, X, k = sp.symbols('zd md z m n X k', real=True)
mubar, al, mK, AQQ = sp.symbols('mubar alpha m_K A_QQ', real=True)
L2 = (c0*(6*zd**2 - 4*zd*X)                 # (1/2)(K_ij K^ij - K^2)
      - (mubar/3)*X**2 - sp.Rational(2, 3)*X*md   # candidate B, auxiliary form
      + c0*(2*k**2*z**2 + 4*k**2*n_*z)       # (1/2) N sqrt(h) R3, quadratic
      + c0*2*al*k**2*n_**2                   # dG/dY (grad n)^2 ; alpha = G_Y = 1/(1+u)
      + mK*n_**2                             # K_BS(Q) lapse mass (irrelevant at high k)
      - m_**2/(2*AQQ))                       # -(1/2) Vt'' dmu^2
Xs = sp.solve(sp.diff(L2, X), X)[0]
L2 = sp.expand(L2.subs(X, Xs))
ns = sp.solve(sp.diff(L2, n_), n_)[0]
L2 = sp.simplify(L2.subs(n_, ns))
Kmat = sp.Matrix(2, 2, lambda i, j: sp.Rational(1, 2)*sp.diff(L2, [zd, md][i], [zd, md][j]))
p("4a kinetic matrix (zeta, mu):", sp.simplify(Kmat))
p("4b det =", sp.factor(Kmat.det()), " trace =", sp.simplify(Kmat.trace()), " => no ghost iff mubar > 0")
p("   mubar = dA/dQp = xi f(u)/2 > 0 for xi > 0, u > 0 (2a,2b): unlocked B is ghost-free where Y > 0 and Qp > 0.")
# dispersion
om = sp.symbols('omega2')
Vmat = sp.Matrix(2, 2, lambda i, j: -sp.Rational(1, 2)*sp.diff(L2, [z, m_][i], [z, m_][j]))
qpos = sp.symbols('q', positive=True)
disp = sp.factor((om*Kmat - Vmat).det().subs({AQQ: -qpos, al: 1/(1+uu), mK: 0}))
# disp is quadratic in omega2: c2 om^2 + c1 om + c0. Leading k behaviour of the two roots:
P = sp.Poly(sp.numer(sp.together(disp)), om)
c2_, c1_, c0_ = [sp.expand(cc) for cc in P.all_coeffs()]
fast = sp.simplify(sp.limit(-c1_/(c2_*k**2), k, sp.oo))           # sum of roots / k^2 -> fast root / k^2
slow = sp.simplify(sp.limit(-c0_/c1_, k, sp.oo))                  # product/sum -> slow root
p("4c fast root omega^2/k^2 ->", fast, " (alpha = 1/(1+u), A_QQ = -q < 0)")
p("4c slow root omega^2 ->", slow, " ; 3 mubar/(2 A_QQ) =", sp.simplify(3*mubar/(2*(-qpos))))
p("   fast mode c_s^2 = (1/alpha - 1)/3 = u/3 >= 0 with alpha = 1/(1+u): no UV gradient instability.")
p("   slow mode: dispersionless, omega^2 = 3 mubar/(2 A_QQ).")
# slow-mode rate in units of Qp: mubar = xi f/2, A_QQ = xi^2 G_AA = -xi^2 u^3/(2 A (1+u)^2), A = xi Qp
ratio = sp.simplify(3*(f_u/2)/(2*(-(uu**3)/(2*(1+uu)**2))))   # omega^2 / Qp
p("4d slow-mode omega^2 / Qp =", ratio)
for uv in [1e-3, 1e-1, 1, 10, 1e3]:
    p(f"   u = {uv:g}: omega^2/Qp = {float(ratio.subs(uu, uv)):.4f}")
p("   => tachyonic, k-independent, |omega| ~ (1.0-1.7) sqrt(Qp) ~ H: Hubble-rate, frozen coefficients cannot decide (UNDECIDED).")

# ---------------------------------------------------------------- 5. CMC-locked variant vs the VCDM theorem
p("5a CMC lock (multiplier lambda (K + phi), D_i phi = 0) sets dK = 0 at k != 0, so dQp = 0 and the extra DOF is removed.")
p("   That is the VCDM structure of FLRW_OBSTRUCTION.md with f(s) -> G(Y); premise f_s(0) = 1 <=> dG/dY|_0 =",
  sp.limit(sp.diff(G.subs(s, sp.sqrt(Y)), Y), Y, 0), "(2d). The K_BS lapse mass drops out of the k->inf limit used there.")
p("   Record result applies: negative matter kinetic coefficient, c_UV^2 = -1/(6 + 9 c_m^2) < 0 on matter FLRW. FAIL.")

open(__file__.replace('.py', '.out'), 'w').write("\n".join(out) + "\n")
