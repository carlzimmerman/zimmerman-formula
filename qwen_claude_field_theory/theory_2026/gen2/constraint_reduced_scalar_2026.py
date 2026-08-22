#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
constraint_reduced_scalar_2026.py
=================================
THE EXACT CONSTRAINT-REDUCED QUADRATIC SCALAR ACTION FOR GEN-2.

Carl's ruling: "The right next calculation is the exact constraint-reduced quadratic
action for Gen-2.  That determines whether the promising k^2, rather than k^4, tensor
behavior survives the full ADM constraints and whether the scalar sector is actually
healthy."

THE FROZEN GEN-2 ACTION (not modified anywhere below)
-----------------------------------------------------
  u_mu = -grad_mu T / sqrt(-grad T . grad T)      (unitary gauge T = t)
  h_munu = g_munu + u_mu u_nu ,  a_mu = u^a grad_a u_mu ,  K_munu = h^a_mu h^b_nu grad_a u_b
  T_munu = (1/2)(D_mu a_nu + D_nu a_mu) - (1/3) h_munu D_alpha a^alpha    [sym trace-free]
  X   = (c^4/a0^2) a_mu a^mu ,      Y_a = (c^8/a0^4) T_munu T^munu
  S = (M_Pl^2 c^3/2) INT d^4x N sqrt(h) [ (3)R + K_ij K^ij - lam_K K^2 + eta_K a_i a^i
      - (2 a0^2/c^4) F(X, Y_a) ] + S_m
  F = -2 sqrt(X) + 2 ln(1+sqrt(X)) + eps [X^2/(1+X)^4] Y_a
  a0 = 9.3619e-11 m/s^2  (INPUT, not derived).   lam_K, eta_K, eps free.

UNITS used in all symbolic work:  c = a0 = 1.  Lengths are in units of
ell = c^2/a0 = 9.598e26 m.  The overall positive prefactor (M_Pl^2 c^3/2) is dropped
(it is positive and cannot flip any sign).  In these units:
  X = a_i a^i ,  Y_a = T_ij T^ij ,  and the action bracket is
      (3)R + K_ij K^ij - lam_K K^2 + Gcal(X) - 2 eps A(X) Y_a
  with  Gcal(X) = eta_K X - 2 F_mu(X),   F_mu(X) = -2 sqrt X + 2 ln(1+sqrt X),
        A(X) = X^2/(1+X)^4.

WHAT IS DERIVED HERE vs ASSUMED vs IMPORTED -- stated at every step in the output.
Nothing is imported from Gen-1: eta_K = 0 is RE-DERIVED (part 7), the khronometric
c_s^2 formula is RE-DERIVED (part 5) and only then compared to the literature.
"""
import sympy as sp

# ----------------------------------------------------------------------------------
FAIL = []
def head(s):
    print("\n" + "=" * 96 + "\n" + s + "\n" + "=" * 96)
def rep(label, cond, extra=""):
    print(("  [ok]   " if cond else "  [FAIL] ") + label + (("\n         " + extra) if extra else ""))
    if not cond:
        FAIL.append(label)
    return cond
def note(tag, s):
    print(f"  [{tag}] {s}")

t, x, y, z = sp.symbols('t x y z', real=True)
coords = [x, y, z]
e = sp.Symbol('e')                                    # perturbation bookkeeping
lam = sp.Symbol('lambda_K', real=True)
eta = sp.Symbol('eta_K', real=True)
q = sp.Symbol('q', positive=True)                     # |a^(0)|  -> X0 = q^2
EA = sp.Symbol('EA', real=True)                       # = eps * A(X0)
G0, G1, G2 = sp.symbols('G0 G1 G2', real=True)        # Gcal(X0), Gcal'(X0), Gcal''(X0)
w, k = sp.symbols('omega k', positive=True)
X0s = sp.Symbol('X0', positive=True)
s_sym = sp.Symbol('s', positive=True)                 # s = sqrt(X0) = g/a0

# ------------------------------- 3-geometry helpers -------------------------------
def christoffel(h):
    hin = h.inv()
    return [[[sp.together(sum(hin[a, l] * (sp.diff(h[l, i], coords[j])
                                           + sp.diff(h[l, j], coords[i])
                                           - sp.diff(h[i, j], coords[l]))
                              for l in range(3)) / 2)
              for j in range(3)] for i in range(3)] for a in range(3)]

def ricci(h):
    G = christoffel(h)
    R = sp.zeros(3, 3)
    for i in range(3):
        for j in range(3):
            R[i, j] = (sum(sp.diff(G[a][i][j], coords[a]) for a in range(3))
                       - sum(sp.diff(G[a][i][a], coords[j]) for a in range(3))
                       + sum(G[a][a][b] * G[b][i][j] for a in range(3) for b in range(3))
                       - sum(G[a][i][b] * G[b][a][j] for a in range(3) for b in range(3)))
    return R


# ==================================================================================
head("PART 0 -- GAUGE FIXING, BACKGROUND, AND THE APPROXIMATION SCHEME (stated, not hidden)")
note("SETUP", "Unitary gauge T = t.  This uses up the time reparametrisation completely; "
              "the khronon is eaten and there is no Stueckelberg field left.")
note("SETUP", "Residual symmetry after T = t: time-dependent spatial diffeomorphisms "
              "x^i -> x^i + xi^i(t,x).  Scalar part xi^i = d^i xi.")
note("SETUP", "General scalar spatial metric h_ij = e^{2psi} delta_ij + 2 d_i d_j E.  Under "
              "the residual scalar diffeo, (traceless part of) E shifts by -2 xi, so E can "
              "be set to ZERO.  GAUGE FIXED: h_ij = e^{2 psi} delta_ij.")
note("SETUP", "Leftover residual freedom: xi with d_i d_j xi - (1/3) delta_ij d^2 xi = 0, "
              "i.e. xi linear in x -- global translations/dilatation-free rigid maps.  These "
              "act trivially on a plane wave of finite k.  So (phi, B, psi) with "
              "N = e^{phi}, N_i = d_i B, h_ij = e^{2 psi} delta_ij is a COMPLETE and "
              "NON-REDUNDANT scalar parametrisation.  [DERIVED from the transformation law]")
note("SETUP", "phi is DEFINED as delta ln N (not delta N).  a_i = D_i ln N is then EXACT and "
              "linear in phi, which removes a spurious quadratic tadpole term.")
note("BG",   "Background: flat spatial slice, N^(0) with a^(0)_i = q n_i = q zhat CONSTANT.")
note("BG",   "Then D_i a^(0)_j = d_i a^(0)_j - Gamma^k_ij a^(0)_k = 0 - 0 = 0, so "
              "T^(0)_ij = 0 EXACTLY and Y_a^(0) = 0.  [DERIVED]")
note("ASSUMED", "FROZEN-BACKGROUND / EIKONAL SCHEME.  ln N^(0) = q z means N^(0) = e^{qz}: "
              "an envelope.  Different terms of the ADM Lagrangian carry different powers of "
              "N^(0), so we evaluate the quadratic form at the point z = 0 (N^(0) -> 1) while "
              "keeping a^(0)_i = q exactly.  No derivative ever acts on the envelope in the "
              "terms that matter: a_i = d_i ln N is envelope-exact, and D_i D_j (q z) = 0 "
              "identically.  The dropped corrections are relative O(q/k) = O(sqrt(X0) a0/(k c^2)).")
note("ASSUMED", "TADPOLE.  The uniform-acceleration background is not a vacuum solution; it is "
              "sourced.  Terms proportional to the background field equations are k-INDEPENDENT "
              "(they multiply the O(e^2) parts of the fields with no derivatives), so they can "
              "only contaminate the k^0 sector.  We therefore quote the omega^2, k^2 and k^4 "
              "coefficients, which are tadpole-free, and DO NOT quote k^1 or k^0 coefficients.")
note("SCHEME", "Accuracy: EXACT in X0 and in (lam_K, eta_K, eps); leading order in q/k.  "
              "Kept: {omega^2, k^2, eps k^4}.  Dropped: everything relative O(q/k).")


# ==================================================================================
# builder
# ==================================================================================
def build_L2(prop_coord, extra_vector=False):
    """Return (L2, fields, prop_coord). prop_coord = z (k || a^(0)) or x (k perp a^(0))."""
    sc = prop_coord
    phi = sp.Function('phi')(t, sc)
    Bf = sp.Function('B')(t, sc)
    psi = sp.Function('psi')(t, sc)
    fields = [phi, Bf, psi]

    h = sp.exp(2 * e * psi) * sp.eye(3)
    if extra_vector:
        # one vector-sector partner to test scalar-vector mixing in the perp case:
        chi = sp.Function('chi')(t, sc)     # h_xz = h_zx = e*chi
        Vf = sp.Function('V')(t, sc)        # N_z = e*V
        fields = [phi, Bf, psi, chi, Vf]
        h = h + e * sp.Matrix([[0, 0, chi], [0, 0, 0], [chi, 0, 0]])

    N = sp.exp(e * phi)                     # envelope set to 1 (eikonal, see PART 0)
    Ni = sp.Matrix([sp.diff(e * Bf, c) for c in coords])
    if extra_vector:
        Ni[2] = Ni[2] + e * Vf

    hin = h.inv()
    sqh = sp.sqrt(h.det())
    G3 = christoffel(h)

    DN = sp.zeros(3, 3)                     # D_i N_j
    for i in range(3):
        for j in range(3):
            DN[i, j] = sp.diff(Ni[j], coords[i]) - sum(G3[a][i][j] * Ni[a] for a in range(3))

    K = sp.zeros(3, 3)
    for i in range(3):
        for j in range(3):
            K[i, j] = (sp.diff(h[i, j], t) - DN[i, j] - DN[j, i]) / (2 * N)
    Ktr = sum(hin[i, j] * K[i, j] for i in range(3) for j in range(3))
    KK = sum(hin[i, a] * hin[j, b] * K[i, j] * K[a, b]
             for i in range(3) for j in range(3) for a in range(3) for b in range(3))
    Ric = ricci(h)
    R3 = sum(hin[i, j] * Ric[i, j] for i in range(3) for j in range(3))

    # a_i = D_i ln N = q n_i + e d_i phi     (EXACT; n = zhat)
    a_low = [sp.S(0), sp.S(0), q]
    for i in range(3):
        a_low[i] = a_low[i] + sp.diff(e * phi, coords[i])
    a_low = sp.Matrix(a_low)

    Xfull = sum(hin[i, j] * a_low[i] * a_low[j] for i in range(3) for j in range(3))

    Da = sp.zeros(3, 3)                     # D_i a_j
    for i in range(3):
        for j in range(3):
            Da[i, j] = sp.diff(a_low[j], coords[i]) - sum(G3[a][i][j] * a_low[a] for a in range(3))
    Dasym = (Da + Da.T) / 2
    trDa = sum(hin[i, j] * Da[i, j] for i in range(3) for j in range(3))
    Tij = Dasym - h * trDa / 3
    Ya = sum(hin[i, a] * hin[j, b] * Tij[i, j] * Tij[a, b]
             for i in range(3) for j in range(3) for a in range(3) for b in range(3))

    # ---- Taylor in e ----
    def coef(expr, n):
        return sp.simplify(sp.diff(expr, e, n).subs(e, 0) / sp.factorial(n))

    X_0 = sp.simplify(Xfull.subs(e, 0))
    X_1 = coef(Xfull, 1)
    X_2 = coef(Xfull, 2)

    meas = N * sqh
    m0, m1, m2 = coef(meas, 0), coef(meas, 1), coef(meas, 2)

    # geometric/kinetic block
    LG = sp.expand(N * sqh * (R3 + KK - lam * Ktr ** 2))
    LG2 = coef(LG, 2)

    # a-sector:  N sqrt(h) * Gcal(X),  Gcal(X0+dX) = G0 + G1 dX + (1/2) G2 dX^2
    Gser = G0 + G1 * (e * X_1 + e ** 2 * X_2) + sp.Rational(1, 2) * G2 * (e * X_1) ** 2
    LGcal = sp.expand((m0 + e * m1 + e ** 2 * m2) * Gser)
    LGcal2 = sp.expand(sp.Poly(LGcal, e).coeff_monomial(e ** 2)) if LGcal.has(e) else sp.S(0)

    # Y-sector:  N sqrt(h) * (-2 eps A(X) Y_a).  Y_a = O(e^2) since T^(0)=0, and
    # dA/dX * dX * Y_a is O(e^3).  So only -2 EA * Y_a^(2) survives at O(e^2).
    Y_2 = coef(Ya, 2)
    Y_0 = sp.simplify(Ya.subs(e, 0))
    Y_1 = coef(Ya, 1)
    LY2 = -2 * EA * Y_2

    L2 = sp.expand(LG2 + LGcal2 + LY2)
    return dict(L2=L2, fields=fields, sc=sc, X0=X_0, X1=X_1, X2=X_2,
                Y0=Y_0, Y1=Y_1, Y2=Y_2, Tij=Tij, m1=m1, m2=m2)


def fourier_avg(L, fields, sc):
    Amap = {}
    for f in fields:
        nm = f.func.__name__
        Amap[f.func] = (sp.Symbol('A_' + nm), sp.Symbol('Ac_' + nm))
    E = sp.Symbol('E_')

    def drepl(d):
        base = d.expr.func
        Af, Afc = Amap[base]
        m = n = 0
        for v, c in d.variable_count:
            if v == t:
                m = c
            elif v == sc:
                n = c
            else:
                raise ValueError("unexpected derivative variable " + str(v))
        return (Af * (-sp.I * w) ** m * (sp.I * k) ** n * E
                + Afc * (sp.I * w) ** m * (-sp.I * k) ** n / E)

    expr = L.replace(lambda ex: isinstance(ex, sp.Derivative)
                     and getattr(ex.expr, 'func', None) in Amap, drepl)
    for base, (Af, Afc) in Amap.items():
        expr = expr.subs(base(t, sc), Af * E + Afc / E)
    p = sp.Poly(sp.expand(expr * E ** 8), E)
    return sp.expand(p.coeff_monomial(E ** 8)), Amap


# ==================================================================================
head("PART 1 -- BACKGROUND AND THE FIRST-ORDER TIDAL TENSOR (k || a^(0), the clean case)")
P = build_L2(z)
rep("X^(0) = q^2 = X0 exactly", sp.simplify(P['X0'] - q ** 2) == 0)
rep("Y_a^(0) = 0 exactly  (T^(0)_ij = 0 on a uniform-acceleration, flat-slice background)",
    sp.simplify(P['Y0']) == 0)
rep("Y_a^(1) = 0 exactly  (Y_a is quadratic in delta T; no linear-order Y term at all)",
    sp.simplify(P['Y1']) == 0,
    "=> the ENTIRE quadratic Y-contribution is -2 eps A(X0) delta T_ij delta T^ij, with "
    "A evaluated on the background.  No F_XY cross term at this order.")

# hand-derived cross-check of delta T and Y^(2), parallel case
phi = sp.Function('phi')(t, z); psi = sp.Function('psi')(t, z)
u_hand = sp.diff(phi, z, 2) - 2 * q * sp.diff(psi, z)
rep("delta T_ij = u (n_i n_j - delta_ij/3) with u = phi'' - 2 q psi'   [independent hand check]",
    sp.simplify(sp.expand(P['Y2'] - sp.Rational(2, 3) * u_hand ** 2)) == 0,
    "hence  Y_a^(2) = (2/3)(phi'' - 2 q psi')^2 .  The phi'' piece is the FOURTH-derivative "
    "hazard: it is second spatial derivatives of the LAPSE, squared.")
note("DERIVED", "In Fourier (k || zhat):  u -> -(k^2 A_phi + 2 i q k A_psi), so")
note("DERIVED", "  Y^(2) -> (2/3)[ k^4 |phi|^2 + 4 q^2 k^2 |psi|^2 + O(q k^3) cross ].")
note("DERIVED", "  * k^4 |phi|^2 : the lapse hazard.        * 4 q^2 k^2 |psi|^2 : an O(eps A X0) "
                "shift of the scalar gradient term -- the exact scalar analogue of the tensor "
                "sector's dc_T^2/c^2 = 2 eps A X0.")


# ==================================================================================
head("PART 2 -- CANONICAL STRUCTURE: WHAT IS NON-DYNAMICAL")
def has_t(expr):
    return any(any(v == t for v, c in d.variable_count) for d in expr.atoms(sp.Derivative))
rep("Y_a contains NO time derivatives (pi^ij is exactly the (lam_K-)GR momentum)",
    not has_t(sp.expand(P['Y2'])))
rep("X contains NO time derivatives", not has_t(sp.expand(P['X1'] + P['X2'])))
Bf = sp.Function('B')(t, z)
rep("Y_a contains NO shift B (momentum constraint H_i is exactly the (lam_K-)GR one)",
    Bf.func not in [a.func for a in sp.expand(P['Y2']).atoms(sp.Function)])
rep("d(Y-sector)/d(psi-dot) = 0 identically (no new momentum from the tidal term)",
    sp.simplify(sp.diff(P['Y2'], sp.Derivative(psi, t))) == 0)
note("DERIVED", "So the Gen-2 tidal operator adds only SPATIAL derivatives.  phi and B remain "
                "non-dynamical; the phase-space count is unchanged from Gen-1: "
                "(20 - 12 - 2)/2 = 3 = 2 tensor + 1 khronon.  No Ostrogradsky partner appears "
                "from the (d^2 phi)^2 term because phi carries no time derivative at all.")


# ==================================================================================
head("PART 3 -- THE LAPSE EQUATION: PRINCIPAL SYMBOL AND ELLIPTICITY  (the Gen-2 hazard)")
Lavg, Amap = fourier_avg(P['L2'], P['fields'], z)
Aphi, Acphi = Amap[sp.Function('phi')]
AB, AcB = Amap[sp.Function('B')]
Apsi, Acpsi = Amap[sp.Function('psi')]

eq_phi = sp.expand(sp.diff(Lavg, Acphi))
eq_B = sp.expand(sp.diff(Lavg, AcB))
eq_psi = sp.expand(sp.diff(Lavg, Acpsi))

rep("lapse (phi) equation contains NO omega: N is DETERMINED by an elliptic-type equation, "
    "it is not propagating and not a first-class constraint",
    sp.degree(sp.Poly(eq_phi, w), w) == 0)
rep("shift (B) equation contains no omega^2 (momentum constraint, first order in time)",
    sp.degree(sp.Poly(eq_B, w), w) <= 1)

Sigma = sp.simplify(sp.expand(eq_phi).coeff(Aphi))          # the phi-phi symbol
Sigma = sp.factor(sp.simplify(Sigma))
print("\n  phi-phi symbol  Sigma(k) = d(eq_phi)/d(A_phi) =")
sp.pprint(Sigma)
alpha_par_sym = G1 + 2 * q ** 2 * G2
Sig_target = 2 * k ** 2 * (alpha_par_sym) - sp.Rational(8, 3) * EA * k ** 4
lead = sp.simplify(sp.expand(Sigma) - sp.expand(Sig_target))
lead = sp.simplify(lead)
print("  Sigma - [2 alpha_par k^2 - (8/3) EA k^4] =", sp.simplify(sp.expand(lead)))
rep("Sigma(k) = 2 alpha_par k^2 - (8/3) eps A(X0) k^4  + (k-independent tadpole/mass terms), "
    "with alpha_par = Gcal'(X0) + 2 X0 Gcal''(X0)",
    sp.degree(sp.Poly(sp.expand(lead), k), k) <= 0,
    "the residue is k^0 -- exactly the tadpole sector we declared unreliable.  The k^2 and "
    "k^4 coefficients are clean.")

note("DERIVED", "PRINCIPAL SYMBOL of the lapse equation = -(8/3) eps A(X0) k^4.")
note("DERIVED", "It is non-degenerate iff eps != 0 -- so at eps != 0 the lapse equation is a "
                "FOURTH-order elliptic equation for phi, not second order.  That by itself is "
                "fine: phi is still algebraically determined mode by mode.")
note("DERIVED", "THE REAL CONDITION IS NOT THE PRINCIPAL SYMBOL, IT IS THE FULL SYMBOL.  "
                "Eliminating phi divides by Sigma(k).  Sigma(k) = 2k^2[alpha_par - (4/3) eps A k^2] "
                "has a REAL ZERO at")
note("DERIVED", "        k_deg^2 = 3 alpha_par / (4 eps A(X0))")
note("DERIVED", "which is a real positive wavenumber iff  eps * alpha_par > 0.  At that k the "
                "lapse is undetermined, the reduced action is singular, and the Cauchy problem "
                "for the constrained system fails.  Since gradient stability requires "
                "alpha_par > 0 (part 5/7), SOLVABILITY OF THE LAPSE EQUATION AT ALL k REQUIRES")
note("DERIVED", "        eps < 0        [Gen-2 condition; note this is OPPOSITE to Gen-1, where "
                "tensor high-k stability forced eps >= 0]")


# ==================================================================================
head("PART 4 -- ELIMINATE phi AND B EXACTLY; THE REDUCED SCALAR ACTION")
sol = sp.solve([eq_phi, eq_B], [Aphi, AB], dict=True)
assert len(sol) == 1, "auxiliary elimination not unique"
Leff = sp.together(sp.expand(Lavg.subs(sol[0])))
D = sp.cancel(sp.simplify(Leff / (Apsi * Acpsi)))
rep("reduced action is a single scalar branch  D(omega,k) |psi|^2 "
    "(phi and B eliminated exactly, no residue)",
    not any(sym in sp.simplify(D).free_symbols
            for sym in (Aphi, Acphi, AB, AcB, Apsi, Acpsi)))

# eikonal truncation: keep leading k at each structure -> set the tadpole G0 -> 0 and
# drop the O(q/k) odd-k terms by taking the large-k leading behaviour at fixed omega/k.
Dn, Dd = sp.fraction(sp.cancel(sp.together(D)))
Dn = sp.expand(Dn)
Dd = sp.expand(Dd)

# substitute alpha for the a-sector Hessian eigenvalue in the parallel direction
al = sp.Symbol('alpha', real=True)
sub_alpha = {G2: (al - G1) / (2 * q ** 2)}
Dn_a = sp.expand(sp.simplify(Dn.subs(sub_alpha)))
Dd_a = sp.expand(sp.simplify(Dd.subs(sub_alpha)))

# ---- the clean statement: dispersion relation ----
disp = sp.solve(sp.Eq(Dn_a, 0), w ** 2)
print("\n  number of omega^2 branches:", len(disp))
w2 = sp.simplify(disp[0])
# eikonal: drop tadpole G0 and the O(q/k) pieces by keeping leading k at fixed structure
w2_eik = sp.simplify(w2.subs(G0, 0))
w2_eik = sp.simplify(sp.expand(w2_eik))
print("\n  omega^2(k) [G0 -> 0, exact in alpha, lam_K, EA, q] =")
sp.pprint(sp.factor(sp.simplify(w2_eik)))

# strip the O(q/k) odd-power-of-k terms: substitute q -> 0 ONLY where it multiplies an odd
# power of k relative to the leading structure.  Cleanest honest way: series in 1/k.
kappa = sp.Symbol('kap', positive=True)     # k -> kappa, then large-kappa handled explicitly
w2_poly = sp.simplify(sp.cancel(w2_eik))
print("\n  (the O(q k) terms below are the declared O(q/k) sector and are not quoted)")

# ---- K_S, G_S, W_S by matching D = K_S omega^2 - G_S k^2 - W_S k^4 ----
KS = sp.simplify(sp.diff(sp.expand(D.subs(sub_alpha).subs(G0, 0)), w, 2) / 2)
KS = sp.factor(sp.simplify(KS))
print("\n  K_S  (coefficient of omega^2 in the reduced quadratic form) =")
sp.pprint(KS)
rep("K_S = 4(3 lam_K - 1)/(lam_K - 1):  INDEPENDENT of alpha, of eps and of X0 "
    "=> the Gen-2 tidal term does NOT change the no-ghost condition",
    sp.simplify(KS - 4 * (3 * lam - 1) / (lam - 1)) == 0,
    "NO-GHOST  <=>  K_S > 0  <=>  lam_K > 1  or  lam_K < 1/3.  Unchanged from Gen-1. [DERIVED]")

Dstat = sp.simplify(sp.expand(D.subs(sub_alpha).subs(G0, 0)).subs(w, 0))
Dstat = sp.cancel(sp.together(Dstat))
print("\n  -[G_S k^2 + W_S k^4] = D(omega=0,k) =")
sp.pprint(sp.factor(sp.simplify(Dstat)))
Gtot = sp.simplify(-Dstat)                    # = G_S k^2 + W_S k^4 (+ O(q/k) and k^0)
c_s2_exact = sp.simplify(sp.cancel(Gtot / (KS * k ** 2)))
print("\n  c_s^2(k) = G_total/(K_S k^2) =")
sp.pprint(sp.factor(sp.simplify(c_s2_exact)))


# ==================================================================================
head("PART 4b -- ADVERSARIAL CROSS-CHECK 1: THE DETERMINANT ROUTE (no Schur complement)")
Mmat = sp.zeros(3, 3)
rows = [eq_phi, eq_B, eq_psi]
cols = [Aphi, AB, Apsi]
for r, ex in enumerate(rows):
    exx = sp.expand(ex)
    for c_, a_ in enumerate(cols):
        Mmat[r, c_] = sp.simplify(exx.coeff(a_))
    resid = sp.simplify(exx - sum(Mmat[r, cc] * cols[cc] for cc in range(3)))
    assert resid == 0, ("nonlinear residue in row", r, resid)
detM = sp.factor(sp.simplify(Mmat.det()))
det_a = sp.expand(sp.simplify(detM.subs(sub_alpha).subs(G0, 0)))
roots_det = sp.solve(sp.Eq(det_a, 0), w ** 2)
rep("determinant route gives exactly ONE omega^2 branch (one propagating scalar; "
    "the (d^2 phi)^2 term creates NO Ostrogradsky partner)", len(roots_det) == 1)
rep("*** determinant route and Schur-complement route give the IDENTICAL dispersion "
    "relation -- the reduction is verified by two independent computations ***",
    sp.simplify(sp.cancel(roots_det[0] - w2_eik)) == 0)
rep("Hermiticity: the 3x3 quadratic form is self-adjoint (M = M^dagger with k -> -k on "
    "the conjugate index), a necessary consistency condition on the Fourier average",
    all(sp.simplify(Mmat[i, j] - Mmat[j, i].subs(k, -k).subs(w, -w)) == 0
        for i in range(3) for j in range(3)))


# ==================================================================================
head("PART 4c -- ADVERSARIAL CROSS-CHECK 2: DOES A TT MODE SOURCE THE CONSTRAINTS?")
note("TEST", "PART 11 claims delta N = delta N^i = 0 at linear TT order.  In ya_tensor_exact_2026.py "
             "that was SET BY HAND.  Here it is COMPUTED: add a genuine TT polarisation to the "
             "same setup and look for linear-in-gamma terms in the phi and B rows.")
gam = sp.Function('gamma')(t, z)          # h_xy = h_yx = e*gamma : TT for k || zhat
phiT = sp.Function('phi')(t, z); BT = sp.Function('B')(t, z); psiT = sp.Function('psi')(t, z)
hT = sp.exp(2 * e * psiT) * sp.eye(3) + e * sp.Matrix([[0, gam, 0], [gam, 0, 0], [0, 0, 0]])
rep("the added mode is transverse and traceless for k || zhat "
    "(delta^ij gamma_ij = 0 and k^i gamma_ij = 0)",
    sp.simplify(sp.Matrix([[0, gam, 0], [gam, 0, 0], [0, 0, 0]]).trace()) == 0
    and all(sp.simplify(sp.diff(sp.Matrix([[0, gam, 0], [gam, 0, 0], [0, 0, 0]])[2, j], z)) == 0
            for j in range(3)))
NT = sp.exp(e * phiT)
NiT = sp.Matrix([sp.diff(e * BT, c) for c in coords])
hinT = hT.inv(); sqhT = sp.sqrt(hT.det()); G3T = christoffel(hT)
DNT = sp.zeros(3, 3)
for i in range(3):
    for j in range(3):
        DNT[i, j] = sp.diff(NiT[j], coords[i]) - sum(G3T[a][i][j] * NiT[a] for a in range(3))
KT = sp.zeros(3, 3)
for i in range(3):
    for j in range(3):
        KT[i, j] = (sp.diff(hT[i, j], t) - DNT[i, j] - DNT[j, i]) / (2 * NT)
KtrT = sum(hinT[i, j] * KT[i, j] for i in range(3) for j in range(3))
KKT = sum(hinT[i, a] * hinT[j, b] * KT[i, j] * KT[a, b]
          for i in range(3) for j in range(3) for a in range(3) for b in range(3))
RicT = ricci(hT); R3T = sum(hinT[i, j] * RicT[i, j] for i in range(3) for j in range(3))
aT = sp.Matrix([sp.diff(e * phiT, c) for c in coords]); aT[2] = aT[2] + q
XT = sum(hinT[i, j] * aT[i] * aT[j] for i in range(3) for j in range(3))
DaT = sp.zeros(3, 3)
for i in range(3):
    for j in range(3):
        DaT[i, j] = sp.diff(aT[j], coords[i]) - sum(G3T[a][i][j] * aT[a] for a in range(3))
TijT = (DaT + DaT.T) / 2 - hT * sum(hinT[i, j] * DaT[i, j] for i in range(3) for j in range(3)) / 3
YaT = sum(hinT[i, a] * hinT[j, b] * TijT[i, j] * TijT[a, b]
          for i in range(3) for j in range(3) for a in range(3) for b in range(3))
cf = lambda ex, n: sp.simplify(sp.diff(ex, e, n).subs(e, 0) / sp.factorial(n))
X1T, X2T = cf(XT, 1), cf(XT, 2)
measT = NT * sqhT
m0T, m1T, m2T = cf(measT, 0), cf(measT, 1), cf(measT, 2)
LG2T = cf(sp.expand(NT * sqhT * (R3T + KKT - lam * KtrT ** 2)), 2)
GserT = G0 + G1 * (e * X1T + e ** 2 * X2T) + sp.Rational(1, 2) * G2 * (e * X1T) ** 2
LGc2T = sp.expand(sp.Poly(sp.expand((m0T + e * m1T + e ** 2 * m2T) * GserT), e).coeff_monomial(e ** 2))
L2T = sp.expand(LG2T + LGc2T - 2 * EA * cf(YaT, 2))
LavT, AmT = fourier_avg(L2T, [phiT, BT, psiT, gam], z)
Agam = AmT[sp.Function('gamma')][0]
eqphiT = sp.expand(sp.diff(LavT, AmT[sp.Function('phi')][1]))
eqBT = sp.expand(sp.diff(LavT, AmT[sp.Function('B')][1]))
eqpsiT = sp.expand(sp.diff(LavT, AmT[sp.Function('psi')][1]))
eqgamT = sp.expand(sp.diff(LavT, AmT[sp.Function('gamma')][1]))
rep("*** the LAPSE equation has NO linear-in-gamma source: d(eq_phi)/d(A_gamma) = 0 ***",
    sp.simplify(eqphiT.coeff(Agam)) == 0)
rep("*** the SHIFT equation has NO linear-in-gamma source: d(eq_B)/d(A_gamma) = 0 ***",
    sp.simplify(eqBT.coeff(Agam)) == 0)
rep("the psi equation likewise has no linear-in-gamma source (scalar/tensor fully decouple "
    "at quadratic order, even at a^(0) != 0)",
    sp.simplify(eqpsiT.coeff(Agam)) == 0)
rep("conversely the gamma equation receives nothing from phi, B or psi",
    all(sp.simplify(eqgamT.coeff(AmT[f][0])) == 0
        for f in (sp.Function('phi'), sp.Function('B'), sp.Function('psi'))))
note("DERIVED", "=> delta N = delta N^i = 0 at linear TT order is now a COMPUTED RESULT of the "
                "Gen-2 constraints, not an assumption.  The item ya_tensor_exact_2026.py listed "
                "as NOT ESTABLISHED is hereby closed.")
w2T_full = sp.solve(sp.Eq(sp.simplify(sp.cancel(sp.expand(LavT.coeff(Agam).coeff(
    AmT[sp.Function('gamma')][1])) if False else
    sp.expand(eqgamT.coeff(Agam)))), 0), w ** 2)
print("\n  tensor dispersion from the SAME constraint-reduced computation: omega_T^2 =",
      sp.factor(sp.simplify(w2T_full[0])) if w2T_full else "(degenerate)")
if w2T_full:
    cT2 = sp.simplify(sp.cancel(w2T_full[0].subs(G0, 0) / k ** 2))
    print("  c_T^2 =", sp.factor(sp.simplify(cT2)), "   (G0 = the declared tadpole sector, "
          "the only term dropped; it is k-independent and cancels against the matter "
          "second variation)")
    rep("*** c_T^2 = 1 + 2 eps A(X0) X0 EXACTLY, with NO k-dependence -- "
        "ya_tensor_exact_2026.py REPRODUCED by a fully independent route, now WITH the ADM "
        "constraints solved rather than delta N = delta N^i = 0 imposed by hand ***",
        sp.simplify(sp.expand(cT2 - (1 + 2 * EA * q ** 2))) == 0,
        "so the promising k^2 tensor behaviour SURVIVES the constraints.  That question is "
        "answered YES.  It is simply no longer the question that decides the theory.")


# ==================================================================================
head("PART 5 -- THE STRUCTURE OF THE ANSWER: alpha -> alpha_eff(k)")
# isolate the q-independent (isotropic) core by dropping the O(q k) cross terms:
# these are the terms odd in q. Split c_s^2 into even/odd in q.
c_even = sp.simplify((c_s2_exact + c_s2_exact.subs(q, -q)) / 2)
c_odd = sp.simplify((c_s2_exact - c_s2_exact.subs(q, -q)) / 2)
rep("c_s^2 is EVEN in q: no O(q k^3) cross term survives into the dispersion "
    "(the q-odd pieces of the Lagrangian are pure imaginary and cancel in the Hermitian form)",
    sp.simplify(c_odd) == 0, "q-odd part = " + str(sp.simplify(sp.factor(c_odd))))

alpha_eff = sp.Symbol('alpha_eff', real=True)
cand = (lam - 1) * (2 - alpha_eff) / (alpha_eff * (3 * lam - 1))
# test the substitution alpha_eff = alpha - (4/3) EA k^2
sub_ae = {alpha_eff: al - sp.Rational(4, 3) * EA * k ** 2}
test = sp.simplify(sp.expand(sp.cancel(c_even - cand.subs(sub_ae))))
print("\n  c_s^2(k)_even  -  [ (lam-1)(2 - alpha_eff)/(alpha_eff(3 lam - 1)) ]_{alpha_eff = alpha - (4/3) EA k^2}")
print("  = ", sp.simplify(sp.factor(test)))
rep("*** THE WHOLE eps-DEPENDENCE OF THE SCALAR SECTOR IS THE SINGLE SUBSTITUTION "
    "alpha -> alpha_eff(k) = alpha - (4/3) eps A(X0) k^2, EXACTLY, at q = 0 ***",
    sp.simplify(sp.factor(test)).subs(q, 0) == 0)
# split the q^2 residue into (i) the genuine O(eps A X0) gradient shift and
# (ii) the O(q^2/k^2) mass-sector terms that the eikonal scheme discards.
res = sp.cancel(sp.together(test))
res_noEA = sp.simplify(sp.expand(res).subs(EA, 0))
res_EA1 = sp.simplify(sp.diff(res, EA).subs(EA, 0))          # O(eps) coefficient
lead_EA = sp.simplify(sp.limit(sp.cancel(res_EA1), k, sp.oo))
print("\n  residue split (valid below the pathology scale, eps A k^2 << alpha):")
print("    (i)  O(eps) coefficient, k -> inf         = ", sp.simplify(sp.factor(lead_EA)))
print("    (ii) eps-independent part                 = ", sp.simplify(sp.factor(res_noEA)))
rep("residue part (ii) is O(q^2/k^2): a MASS term, inside the declared O(q/k)^2 error of "
    "the scheme, NOT quoted",
    sp.simplify(sp.limit(sp.simplify(res_noEA), k, sp.oo)) == 0)
shift_closed = (2 * q ** 2 * (lam - 1)
                * (4 * G1 ** 2 + 4 * G1 * al - 4 * G1 + al ** 2)
                / (3 * al ** 2 * (3 * lam - 1)))
rep("residue part (i) is a k-INDEPENDENT gradient shift, DERIVED as\n"
    "         delta c_s^2 = eps A(X0) X0 * 2(lam_K-1)(4 a_perp^2 + 4 a_perp a_par - 4 a_perp "
    "+ a_par^2) / (3 a_par^2 (3 lam_K - 1))\n"
    "         [G1 = alpha_perp, alpha = alpha_par in the k || a^(0) run]",
    sp.simplify(sp.expand(lead_EA - shift_closed)) == 0)
_num = float(shift_closed.subs({q: 1, lam: 2, G1: 1, al: sp.Rational(1, 2)}))
rep(f"magnitude check at X0 = 1, eta_K = 0, lam_K = 2:  delta c_s^2 = {_num:.3f} * eps A X0 "
    "-- the SAME order as the tensor sector's dc_T^2/c^2 = 2 eps A X0, as it must be",
    0.1 < _num < 10.0,
    "being k-INDEPENDENT this shift CANNOT be the pathology: the pathology is the "
    "alpha -> alpha_eff(k) running, a different, k-GROWING effect.")

note("DERIVED", "c_s^2(k) = (lam_K - 1)(2 - alpha_eff(k)) / [ alpha_eff(k) (3 lam_K - 1) ]  "
                "+ O(eps A X0),   alpha_eff(k) = alpha - (4/3) eps A(X0) k^2 .")
note("DERIVED", "At eps = 0 this REPRODUCES the khronometric form "
                "c_s^2 = (lam-1)(2-alpha)/(alpha(3 lam-1)) -- re-derived here, not imported; "
                "only now compared with Blas-Pujolas-Sibiryakov (xi=1, beta=0).")
rep("eps -> 0 limit reproduces the khronometric scalar speed [re-derived, then compared]",
    sp.simplify(sp.factor(c_even.subs(EA, 0).subs(q, 0)
                          - (lam - 1) * (2 - al) / (al * (3 * lam - 1)))) == 0)


# ==================================================================================
head("PART 6 -- HEALTH: THE PINCER")
note("DERIVED", "Given no-ghost (K_S > 0), stability requires  0 < alpha_eff(k) < 2  for EVERY k "
                "up to the EFT cutoff (this is the alpha-window re-derived above, now k-dependent).")
note("DERIVED", "alpha_eff(k) = alpha - (4/3) eps A(X0) k^2 is MONOTONIC in k^2.  Therefore:")
print("""
    eps > 0 :  alpha_eff DECREASES.  It reaches 0 at   k_deg^2 = 3 alpha /(4 eps A).
               At k_deg the lapse equation degenerates (PART 3) and c_s^2 has a POLE;
               for k > k_deg, alpha_eff < 0 => c_s^2 = (lam-1)(2-alpha_eff)/(alpha_eff(3lam-1)) < 0
               (numerator > 0, denominator < 0 for lam_K > 1).  GRADIENT INSTABILITY.

    eps < 0 :  alpha_eff INCREASES.  The lapse equation is elliptic at every k (good),
               but alpha_eff crosses 2 at k_inst^2 = 3(2 - alpha)/(4 |eps| A),
               and for k > k_inst, c_s^2 < 0.  GRADIENT INSTABILITY.
               As k -> infinity, c_s^2 -> -(lam_K - 1)/(3 lam_K - 1) : an O(1) NEGATIVE
               limit, i.e. growth rate |omega| ~ |c_s| k, unbounded with k.

    eps = 0 :  healthy (khronometric with the mu-sector), but the tidal operator is switched
               off entirely and Gen-2 collapses to eta_K = 0 khronometric MOND.
""")
# verify the two crossing wavenumbers and the UV limit symbolically
kdeg2 = sp.solve(sp.Eq(al - sp.Rational(4, 3) * EA * k ** 2, 0), k ** 2)[0]
kins2 = sp.solve(sp.Eq(al - sp.Rational(4, 3) * EA * k ** 2, 2), k ** 2)[0]
rep("k_deg^2 = 3 alpha / (4 eps A)", sp.simplify(kdeg2 - 3 * al / (4 * EA)) == 0)
rep("k_inst^2 = 3(alpha - 2) / (4 eps A)  [= 3(2-alpha)/(4|eps|A) when eps < 0]",
    sp.simplify(kins2 - 3 * (al - 2) / (4 * EA)) == 0)
uv = sp.limit(cand.subs(sub_ae), k, sp.oo)
rep("UV limit of c_s^2 is -(lam_K-1)/(3 lam_K-1) for either sign of eps (nonzero)",
    sp.simplify(uv + (lam - 1) / (3 * lam - 1)) == 0, "c_s^2(k->inf) = " + str(sp.simplify(uv)))
uvf = -(lam - 1) / (3 * lam - 1)
tab = [(sp.Integer(2), None), (sp.Rational(11, 10), None), (sp.Rational(1, 5), None),
       (sp.Rational(1, 10), None), (sp.Rational(1, 100), None)]
print("\n   lam_K      K_S = 4(3lam-1)/(lam-1)   no-ghost?   c_s^2(k -> inf)")
allneg = True
for lv, _ in tab:
    KSv = sp.nsimplify(4 * (3 * lv - 1) / (lv - 1))
    uvv = sp.simplify(uvf.subs(lam, lv))
    allneg = allneg and (uvv < 0)
    print(f"   {str(lv):>7}   {str(KSv):>22}   {str(KSv > 0):>9}   {str(uvv):>10}")
rep("*** THE UV LIMIT c_s^2 -> -(lam_K-1)/(3 lam_K-1) IS NEGATIVE ON *BOTH* NO-GHOST "
    "BRANCHES (lam_K > 1 AND lam_K < 1/3) -- there is no branch escape ***", allneg,
    "CORRECTION TO MY OWN FIRST DRAFT: I asserted the lam_K < 1/3 branch had a POSITIVE UV "
    "limit.  It does not: at lam_K = 1/5 the limit is -2.  The sign flip of (lam-1) is "
    "cancelled by the sign flip of (3lam-1), exactly as it is in the no-ghost condition.")
rep("consequently the stability window 0 < alpha_eff < 2 is BRANCH-INDEPENDENT: given "
    "K_S > 0, c_s^2 > 0 <=> 0 < alpha_eff < 2 on either branch",
    all(sp.simplify(((lam - 1) * (2 - av) / (av * (3 * lam - 1))).subs(lam, lv)) > 0
        for lv in (sp.Integer(2), sp.Rational(1, 5)) for av in (sp.Rational(1, 2), sp.Rational(3, 2)))
    and all(sp.simplify(((lam - 1) * (2 - av) / (av * (3 * lam - 1))).subs(lam, lv)) < 0
            for lv in (sp.Integer(2), sp.Rational(1, 5)) for av in (sp.Integer(3), sp.Integer(-1))))


# ==================================================================================
head("PART 7 -- IS eta_K = 0 FORCED?  RE-DERIVED FROM SCRATCH (nothing imported)")
Xs = sp.Symbol('X', positive=True)
Fmu = -2 * sp.sqrt(Xs) + 2 * sp.log(1 + sp.sqrt(Xs))
Gcal = eta * Xs - 2 * Fmu
G1e = sp.simplify(sp.diff(Gcal, Xs))
G2e = sp.simplify(sp.diff(Gcal, Xs, 2))
alpha_perp_e = sp.simplify(G1e.subs(Xs, s_sym ** 2))
alpha_par_e = sp.simplify((G1e + 2 * Xs * G2e).subs(Xs, s_sym ** 2))
rep("alpha_perp = Gcal'(X0)            = eta_K + 2/(1+s)     [s = sqrt(X0) = g/a0]",
    sp.simplify(alpha_perp_e - (eta + 2 / (1 + s_sym))) == 0)
rep("alpha_par  = Gcal'(X0)+2X0Gcal''  = eta_K + 2/(1+s)^2",
    sp.simplify(alpha_par_e - (eta + 2 / (1 + s_sym) ** 2)) == 0)
note("DERIVED", "ROUTE 1 (gradient stability, k -> 0 limit of the Gen-2 reduced action above): "
                "need 0 < alpha_par, alpha_perp < 2 for EVERY s > 0.")
print("      s -> 0 (deep MOND):  alpha_par -> eta_K + 2,  alpha_perp -> eta_K + 2")
print("      s -> inf (Newton) :  alpha_par -> eta_K,       alpha_perp -> eta_K")
rep("eta_K > 0 => alpha > 2 in the deep-MOND corner => gradient instability there",
    sp.limit(alpha_par_e, s_sym, 0) - 2 == eta and True)
rep("eta_K < 0 => alpha < 0 in the Newtonian corner => wrong-sign (unstable) lapse sector",
    sp.limit(alpha_par_e, s_sym, sp.oo) == eta)
rep("eta_K = 0 is the UNIQUE value with 0 < alpha_par, alpha_perp < 2 at every finite s "
    "(gaps 2-alpha_par = 2s(s+2)/(1+s)^2 > 0 and 2-alpha_perp = 2s/(1+s) > 0)",
    sp.simplify(sp.factor((2 - 2 / (1 + s_sym) ** 2)) - 2 * s_sym * (s_sym + 2) / (1 + s_sym) ** 2) == 0
    and sp.simplify(sp.factor(2 - 2 / (1 + s_sym)) - 2 * s_sym / (1 + s_sym)) == 0)
note("DERIVED", "ROUTE 2 (deep-MOND limit of the STATIC lapse equation).  This is derived here "
                "from the same quadratic action by a SECOND Schur complement -- at omega = 0, "
                "eliminating psi instead of phi.  Nothing is imported.")
Pperp = build_L2(x)
Lav_s, Am_s = fourier_avg(Pperp['L2'], Pperp['fields'], x)
Aph_s, Acph_s = Am_s[sp.Function('phi')]
Aps_s, Acps_s = Am_s[sp.Function('psi')]
eqp_s = sp.expand(sp.diff(Lav_s, Acph_s)).subs(w, 0).subs(G0, 0)
eqs_s = sp.expand(sp.diff(Lav_s, Acps_s)).subs(w, 0).subs(G0, 0)
Mpp = sp.simplify(eqp_s.coeff(Aph_s))
Mps = sp.simplify(eqp_s.coeff(Aps_s))
Msp = sp.simplify(eqs_s.coeff(Aph_s))
Mss = sp.simplify(eqs_s.coeff(Aps_s))
rep("static blocks are symmetric (the quadratic form is Hermitian)", sp.simplify(Mps - Msp) == 0)
psi_of_phi = sp.simplify(-Msp / Mss)
rep("in the eikonal limit q/k -> 0 the static spatial equation gives psi = -phi, "
    "i.e. Psi = Phi -> gamma_PPN = 1 [DERIVED here, not imported]",
    sp.simplify(sp.limit(psi_of_phi.subs(EA, 0), q, 0) + 1) == 0,
    "psi/phi = " + str(sp.simplify(sp.factor(psi_of_phi))))
Sig_eff = sp.simplify(sp.cancel(Mpp - Mps * Msp / Mss))
Sig_eff_eik = sp.simplify(sp.limit(sp.cancel(Sig_eff), q, 0))
print("\n  effective STATIC lapse operator after eliminating psi (eikonal q/k -> 0):")
sp.pprint(sp.factor(Sig_eff_eik))
mu_sym = sp.Symbol('mu')
rep("*** Sigma_eff(k) = -4 k^2 [ 1 - alpha_eff(k)/2 ] , i.e. the static lapse equation is "
    "div[ mu_eff grad Phi ] = source with mu_eff(k) = 1 - alpha_eff(k)/2 ***",
    sp.simplify(sp.expand(Sig_eff_eik
                          + 4 * k ** 2 * (1 - (G1 - sp.Rational(4, 3) * EA * k ** 2) / 2))) == 0,
    "the '1' is delivered by the psi (spatial) equation through the Schur complement, NOT by "
    "an a^2 term -- so it is a genuine two-potential result.")
mu_of_s = sp.simplify((1 - alpha_perp_e / 2))
rep("at eps = 0: mu = 1 - alpha_perp/2 = 1 - eta_K/2 - 1/(1+s) = 1 - eta_K/2 + F_X, "
    "the AQUAL interpolation function",
    sp.simplify(mu_of_s - (1 - eta / 2 - 1 / (1 + s_sym))) == 0)
rep("eta_K = 0  =>  mu = s/(1+s) -> s  as s -> 0 : the DEEP-MOND limit mu = g/a0 [DERIVED]",
    sp.simplify(mu_of_s.subs(eta, 0) - s_sym / (1 + s_sym)) == 0
    and sp.simplify(sp.limit(mu_of_s.subs(eta, 0) / s_sym, s_sym, 0)) == 1)
rep("eta_K != 0  =>  mu -> -eta_K/2 != 0 as s -> 0 : a CONSTANT kernel, the deep-MOND limit "
    "is destroyed (and for eta_K > 0 the kernel is negative there)",
    sp.simplify(sp.limit(mu_of_s, s_sym, 0) + eta / 2) == 0)
note("DERIVED", "Note the two routes are now visibly THE SAME STATEMENT: mu = 1 - alpha/2, so "
                "the gradient window 0 < alpha < 2 is IDENTICALLY the requirement 0 < mu < 1 "
                "on the interpolation function.  eta_K = 0 is what puts mu in (0,1) at every s.")
note("DERIVED", "TWO INDEPENDENT ROUTES AGAIN FORCE eta_K = 0 IN GEN-2.  This is a RE-DERIVATION "
                "inside the Gen-2 constraint-reduced action, not an import: the Y-sector enters "
                "only through alpha -> alpha_eff(k), which coincides with alpha at k -> 0, and "
                "both routes are k -> 0 statements.")
note("DERIVED", "eta_K = 0 is NECESSARY but, unlike Gen-1, NO LONGER SUFFICIENT: it fixes "
                "alpha(X0) in (0,2) but says nothing about alpha_eff(k) leaving that window at "
                "finite k.  That is the new Gen-2 content.")


# ==================================================================================
head("PART 8 -- THE TWO CORNERS AND THE NUMBERS")
Aexp = Xs ** 2 / (1 + Xs) ** 4
rep("A(X) = X^2/(1+X)^4 -> X^2 as X -> 0 and -> X^-2 as X -> inf; max at X = 1, A(1) = 1/16",
    sp.limit(Aexp / Xs ** 2, Xs, 0) == 1 and sp.limit(Aexp * Xs ** 2, Xs, sp.oo) == 1
    and sp.simplify(sp.diff(Aexp, Xs).subs(Xs, 1)) == 0 and Aexp.subs(Xs, 1) == sp.Rational(1, 16))
print("""
  DEEP-MOND CORNER  X0 -> 0 (s -> 0), eta_K = 0:
     alpha_par, alpha_perp -> 2      => c_s^2 -> 0 : the scalar is MARGINAL and strongly
        coupled, exactly as in Gen-1 (unchanged; the Y-sector cannot help).
     A(X0) -> X0^2 -> 0              => the k^4 lapse term switches OFF as X0^2, so the
        instability wavenumber k_inst ~ sqrt(3(2-alpha)/(4|eps|A)) DIVERGES as 1/X0.
     => the deep-MOND corner is the SAFEST place for the Y-sector and the WORST place for
        the scalar sound speed.  The two problems are anti-correlated.

  NEWTONIAN CORNER  X0 >> 1 (s -> inf), eta_K = 0:
     alpha_par -> 2/s^2, alpha_perp -> 2/s   => c_s^2 -> (lam-1)/(3lam-1) * (2/alpha)
        ~ s^2 (par) or s (perp): SUPERLUMINAL, growing without bound.  (Allowed with a
        global time function, but the Cherenkov/PPN watch of Gen-1 carries over unchanged.)
     A(X0) -> X0^-2 -> 0             => the k^4 term switches off here too.
     => the k^4 hazard is maximal at X0 = 1, i.e. exactly at g = a0, the MOND transition.
""")

import math
c_l = 2.99792458e8
a0 = 9.3619e-11
ell = c_l ** 2 / a0
print(f"  ell = c^2/a0 = {ell:.4e} m   (the unit of length in all symbolic work)")
print(f"  {'X0':>10} {'s=g/a0':>10} {'A(X0)':>12} {'alpha_par':>10} "
      f"{'lam_deg (eps>0)':>18} {'lam_inst (eps<0)':>18}")
epsv = 1.1e-24
rows = []
for X0v in (1e-2, 1.0, 1e2, 1e4, 4e15):
    sv = math.sqrt(X0v)
    Av = X0v ** 2 / (1 + X0v) ** 4
    apar = 2.0 / (1 + sv) ** 2
    kdeg = math.sqrt(3 * apar / (4 * epsv * Av))
    kins = math.sqrt(3 * (2 - apar) / (4 * epsv * Av))
    ldeg = 2 * math.pi / kdeg * ell
    lins = 2 * math.pi / kins * ell
    rows.append((X0v, sv, Av, apar, ldeg, lins))
    print(f"  {X0v:>10.2e} {sv:>10.2e} {Av:>12.4e} {apar:>10.4f} "
          f"{ldeg:>15.3e} m {lins:>15.3e} m")
print("""
  (X0 = 4e15 is g at the Earth's surface; X0 = 1 is the MOND transition, e.g. galaxy
   outskirts and the Sun's MOND radius at ~7000 AU.)
  READ THIS TABLE AS: at eps = 1.1e-24 -- the value the Solar-System suppression window
  needs -- the Gen-2 scalar sector is sick on ALL scales below roughly 10^15 m (0.05 pc)
  at the MOND transition, and still below ~1 m at the Earth's surface.  There is no
  regime where the pathology is pushed above the EFT cutoff.
""")
# how small must eps be?
for lab, lcut in (("0.13 mm (the theory's own strong-coupling length)", 1.3e-4),
                  ("1 m", 1.0), ("1 AU", 1.496e11), ("10^4 AU (wide binaries)", 1.496e15)):
    kc = 2 * math.pi / lcut * ell
    X0v, Av, apar = 1.0, 1 / 16, 0.5
    epsmax = 3 * (2 - apar) / (4 * Av * kc ** 2)
    print(f"  stability demanded down to {lab:<48s} => |eps| < {epsmax:.3e}")
print(f"  needed for the Y-sector to do anything (Solar-System window):  eps ~ {epsv:.1e}")


# ==================================================================================
head("PART 9 -- THE ONE CRACK, PRICED HONESTLY (never say 'no open doors')")
print("""
  Escapes examined.  (a) is CLOSED by the table in PART 6; (b) and (c) are left OPEN.

  (a) CLOSED -- the lam_K < 1/3 branch.  I first guessed the UV limit flips sign there.
      It does not (PART 6 table: lam_K = 1/5 gives c_s^2 -> -2).  The window
      0 < alpha_eff < 2 is branch-independent, so no choice of lam_K escapes the pincer.

  (b) OPEN, but a needle -- lam_K -> 1 from above.  The UV growth rate is
      |omega| = |c_s| k with |c_s| -> sqrt((lam_K-1)/(3lam_K-1)) -> 0.  The instability
      survives but slows.  Demanding a growth time longer than 10 Gyr at the Earth-surface
      instability scale requires the number printed below.  lam_K -> 1 is ALSO where BBN/CMB
      push (G_cosmo = 2G/(3lam_K-1)) and where K_S = 4(3lam_K-1)/(lam_K-1) -> infinity, i.e.
      the already-flagged strongly-coupled corner.  Priced, not dismissed.

  (c) OPEN, structural -- a DIFFERENT tidal invariant.  The pincer follows from one fact
      only: T_ij carries d_i d_j (ln N), so Y_a contributes -(8/3) eps A k^4 to the LAPSE
      symbol with a definite sign, and the reduced action depends on eps solely through
      alpha_eff = alpha - (4/3) eps A k^2.  Any invariant whose lapse content is a total
      derivative, or which pairs d^2 ln N with a compensating term so that the k^4 piece
      cancels in the phi-phi block, would evade this.  Y_a as frozen does not.  I have NOT
      searched that space, and I am not asserting it is empty.
""")
k_earth = math.sqrt(2 * 3 / (4 * epsv * (4e15 ** 2 / (1 + 4e15) ** 4)))   # alpha->0, 2-alpha->2
k_earth_SI = k_earth / ell
tau = 3.156e17            # 10 Gyr in s
cs_max = 1.0 / (tau * c_l * k_earth_SI)
lam_minus_1 = cs_max ** 2 * 2 / (1 - 3 * cs_max ** 2)   # (lam-1)/(3lam-1)=cs^2 -> solve
print(f"\n  Earth-surface instability wavenumber k = {k_earth_SI:.3e} 1/m "
      f"(lambda = {2*math.pi/k_earth_SI:.3e} m)")
print(f"  growth time > 10 Gyr there requires |c_s| < {cs_max:.3e}, i.e. lam_K - 1 < {lam_minus_1:.3e}")
print("  => escape (b) needs lam_K tuned to 1 at that precision.  Recorded as OPEN, not closed.")


# ==================================================================================
head("PART 10 -- THE PERPENDICULAR DIRECTION (k perp a^(0)) AND THE MIXING CAVEAT")
Pp = build_L2(x)
rep("perp case: Y_a^(0) = Y_a^(1) = 0 (same background statement)",
    sp.simplify(Pp['Y0']) == 0 and sp.simplify(Pp['Y1']) == 0)
phix = sp.Function('phi')(t, x); psix = sp.Function('psi')(t, x)
u_perp = sp.diff(phix, x, 2)
guess = sp.Rational(2, 3) * u_perp ** 2 + sp.Rational(2, 3) * q ** 2 * sp.diff(psix, x) ** 2 * 3
print("  perp-case Y^(2) =", sp.simplify(sp.expand(Pp['Y2'])))
Lavg_p, Amap_p = fourier_avg(Pp['L2'], Pp['fields'], x)
eqphi_p = sp.expand(sp.diff(Lavg_p, Amap_p[sp.Function('phi')][1]))
Sig_p = sp.factor(sp.simplify(sp.expand(eqphi_p).coeff(Amap_p[sp.Function('phi')][0])))
alpha_perp_sym = G1
resid_p = sp.simplify(sp.expand(Sig_p - (2 * k ** 2 * alpha_perp_sym - sp.Rational(8, 3) * EA * k ** 4)))
print("  perp phi-phi symbol minus [2 alpha_perp k^2 - (8/3) EA k^4] =", sp.simplify(resid_p))
rep("perp case: SAME principal symbol -(8/3) eps A k^4, with alpha_perp = Gcal'(X0) "
    "replacing alpha_par -- the k^4 hazard is ISOTROPIC (it comes from d_i d_j phi, which "
    "never touches the background direction)",
    sp.degree(sp.Poly(sp.expand(resid_p), k), k) <= 0)
note("DERIVED", "c_s^2 both directions: same formula with alpha -> alpha_par (k || a^(0)) or "
                "alpha_perp (k perp a^(0)):")
note("DERIVED", "   alpha_par  = eta_K + 2/(1+s)^2 ,   alpha_perp = eta_K + 2/(1+s) .")
note("DERIVED", "The eps k^2 correction -(4/3) eps A(X0) k^2 is the SAME in both directions.  "
                "So the pincer of PART 6 is direction-independent; only k_deg / k_inst shift by "
                "the ratio alpha_par/alpha_perp = 1/(1+s).")

# scalar-vector mixing order check (perp case only)
Pv = build_L2(x, extra_vector=True)
Lav_v, Amap_v = fourier_avg(Pv['L2'], Pv['fields'], x)
Aph = Amap_v[sp.Function('phi')][0]; Acps = Amap_v[sp.Function('psi')][1]
Achi = Amap_v[sp.Function('chi')][0]; AV = Amap_v[sp.Function('V')][0]
mix = sp.S(0)
for Asc in (Amap_v[sp.Function('phi')][0], Amap_v[sp.Function('B')][0], Amap_v[sp.Function('psi')][0]):
    for Ave in (Amap_v[sp.Function('chi')][1], Amap_v[sp.Function('V')][1]):
        mix += sp.expand(Lav_v).coeff(Asc).coeff(Ave) * Asc * Ave
mix = sp.expand(mix)
print("\n  scalar<->vector mixing terms (perp case):")
sp.pprint(sp.simplify(sp.factor(mix)))
allmix = sp.Poly(sp.expand(mix + (0 if mix == 0 else 0)), k) if mix != 0 else None
if mix != 0:
    degs = sp.Poly(sp.expand(mix), k).monoms()
    print("  powers of k appearing in the mixing block:", sorted({d[0] for d in degs}))
rep("every scalar<->vector mixing term carries at least one power of q "
    "(mixing is generated ONLY by the background direction) and is therefore O(q/k) "
    "relative to the diagonal blocks -- inside the declared error of the scheme",
    (mix == 0) or all(sp.simplify(term.subs(q, 0)) == 0
                      for term in sp.Add.make_args(sp.expand(mix))),
    "so the pure-scalar ansatz is legitimate at the order quoted; the mixing cannot "
    "cancel the k^4 term, which is q-independent.")


# ==================================================================================
head("PART 11 -- DOES THE TENSOR k^2 RESULT SURVIVE THE CONSTRAINTS?")
note("DERIVED", "The TT sector: delta N = delta N^i = 0 is now a RESULT, not an assumption.  "
                "Reason, derived from the structure above:")
note("DERIVED", "  (i) phi and B appear in the quadratic action only in the scalar block; the "
                "lapse equation (PART 3) is d(L)/d(phi) = 0 with a SCALAR source.")
note("DERIVED", "  (ii) A TT tensor gamma_ij (transverse, traceless) cannot source a scalar "
                "equation at LINEAR order: every term in eq_phi is built from scalars, and the "
                "only linear-in-gamma scalars available are delta^ij gamma_ij = 0 and "
                "k^i k^j gamma_ij = 0.  Hence delta N = delta N^i = 0 at linear TT order.")
note("DERIVED", "  (iii) Therefore the tensor quadratic action is NOT modified by the "
                "constraint solution, and the ya_tensor_exact_2026.py result stands as a "
                "constraint-reduced statement: dc_T^2/c^2 = 2 eps A(X0) X0, k-INDEPENDENT.")
note("DERIVED", "  (iv) CONSISTENCY: the scalar sector's own eps-correction to the gradient "
                "term is the SAME O(eps A X0) size (PART 5 residue).  The two agree in "
                "magnitude, as they must.")
note("CAVEAT", "This closes the item ya_tensor_exact_2026.py listed as NOT ESTABLISHED "
              "(delta N = delta N^i = 0 for TT once the constraints are solved).  It does NOT "
              "rescue Gen-2: the theory now dies in the scalar sector instead, at the same eps.")


# ==================================================================================
head("VERDICT")
print("""
  THE WHOLE ANSWER IN ONE LINE:
      alpha  ->  alpha_eff(k) = alpha - (4/3) eps A(X0) k^2 ,
  and equivalently, in AQUAL language,
      mu     ->  mu_eff(k)    = 1 - alpha_eff(k)/2 = mu(X0) + (2/3) eps A(X0) k^2 :
  the Gen-2 tidal operator makes the MOND interpolation function SCALE-DEPENDENT.

  K_S  = 4(3 lam_K - 1)/(lam_K - 1)                    [eps-independent, X0-independent]
  G_S(k) = K_S k^2 c_s^2(k),
  c_s^2(k) = (lam_K - 1)(2 - alpha_eff(k)) / [ alpha_eff(k) (3 lam_K - 1) ]  + O(eps A X0)
  W_S (the k^4 term in the psi sector) is NOT independent: it is entirely the image of the
         lapse-sector k^4 under the Schur complement, i.e. it is generated by alpha_eff(k).
  Lapse symbol: Sigma(k) = 2 alpha k^2 - (8/3) eps A(X0) k^4 ; static reduced form
         Sigma_eff(k) = -4 k^2 mu_eff(k).

  alpha_par  = eta_K + 2/(1+s)^2 ,  alpha_perp = eta_K + 2/(1+s) ,  s = sqrt(X0) = g/a0.

  NO-GHOST      : K_S > 0  <=>  lam_K > 1 or lam_K < 1/3.  UNCHANGED by the Gen-2 tidal term.
  eta_K = 0     : STILL FORCED, twice over, re-derived inside the Gen-2 reduced action.
                  The two routes are the SAME statement: mu = 1 - alpha/2, so 0 < alpha < 2
                  IS 0 < mu < 1, and eta_K = 0 is what keeps mu in (0,1) at every s.
  GRADIENT      : requires 0 < alpha_eff(k) < 2, i.e. 0 < mu_eff(k) < 1, at every k.
                  IMPOSSIBLE for eps != 0, because mu_eff is monotonic in k^2:
                    eps > 0 -> mu_eff reaches 1 at k_deg^2 = 3 alpha/(4 eps A);
                               there the lapse symbol has a REAL ZERO -- the constraint
                               cannot be solved, c_s^2 has a pole, and c_s^2 < 0 beyond.
                    eps < 0 -> lapse elliptic everywhere, but mu_eff reaches 0 at
                               k_inst^2 = 3(2-alpha)/(4 |eps| A) and c_s^2 < 0 beyond.
                  Both crossings sit at MACROSCOPIC wavelengths for eps ~ 1e-24, on BOTH
                  no-ghost branches, in BOTH directions relative to a^(0).

  => THE GEN-1 k^4 PROBLEM DID NOT DISAPPEAR IN GEN-2.  IT MOVED FROM THE TENSOR SECTOR
     TO THE LAPSE SECTOR, EXACTLY WHERE CARL SAID THE THEORY COULD STILL DIE, AND IT IS
     WORSE THERE: in Gen-1 it was a bound on eps from GW dispersion; here it is a UV
     gradient instability / loss of ellipticity that no observational bound can soften.

  The tensor k^2 result SURVIVES the constraints (PART 11) -- it was correct and it is now
  constraint-reduced.  It is simply no longer the binding problem.
""")
print("=" * 96)
print("FAILURES:", len(FAIL))
for f in FAIL:
    print("   -", f)
print("=" * 96)
