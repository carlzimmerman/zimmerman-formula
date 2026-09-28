# AS232 - derive PPN beta from the second-order static weak-field equation.  (v8)
# CA5-GNC-R, FINAL_ACTION eq (4): the curvature slot is the FULL 4D scalar curvature
# of the warped ansatz g = diag(-e^{2 Phi}, e^{2w} δ_3), w = ln(1-2 Psi)/2:
#   R4 = R3(w) - 2 (1-2 Psi)^{-1} L0 Phi - 2 (1-2 Psi)^{-1} (D0 Phi)^2
#            + 2 (1-2 Psi)^{-2} (D0 Phi)(D0 Psi)
# (verified: EXACTLY zero on Schwarzschild isotropic vacuum Phi=ln((1-x)/(1+x)),
#  w=2ln(1+x), the unique static spherically symmetric vacuum solution).
# The branch system is the AS226-validated operator family (E1: 4 cN L0(Phi-Z) = rho-side;
# shell Psi=Phi), closed at second order by the on-shell quadratic density of R4 + V_a
# (window: inactive gate, dust, heat suppression S_k -> 0; Lambda k!=0-projected; nonzero
# modes; mean normalization). The task's coordinate gauge: g00 = -e^{2 Phi}, so with
# Phi = -U_N + phi2:  beta = 1 + phi2/U_N^2.
import sympy as sp

r = sp.symbols('r', positive=True)
U = sp.Function('U')(r)
alpha, cN, Sk, ell = sp.symbols('alpha cN Sk ell', positive=True)
eps = sp.symbols('eps', positive=True)

Phi1, Psi1 = -U, -U
varphi2, psi2 = sp.Function('varphi2')(r), sp.Function('psi2')(r)
Phi = eps * Phi1 + eps**2 * varphi2
Psi = eps * Psi1 + eps**2 * psi2
Z1 = ell * Sk * Phi1 / 4
Z = eps * Z1 + eps**2 * ell * Sk * varphi2 / 4
Uaux = eps * (Phi1 - Z1) + eps**2 * (varphi2 - ell * Sk * varphi2 / 4)

def D0(f): return sp.diff(f, r)
def L0(f): return sp.diff(f, r, 2) + sp.Rational(2, 1) * sp.diff(f, r) / r

w = sp.log(1 - 2 * Psi) / 2
R3 = -4 * (1 - 2 * Psi) ** -1 * L0(w) - 2 * (1 - 2 * Psi) ** -1 * D0(w) ** 2
R4 = (R3 - 2 * (1 - 2 * Psi) ** -1 * L0(Phi) - 2 * (1 - 2 * Psi) ** -1 * D0(Phi) ** 2
      + 2 * (1 - 2 * Psi) ** -2 * D0(Phi) * D0(Psi))
R4 = sp.expand(sp.series(R4, eps, 0, 3).removeO())

inv = 1 / (1 - 2 * Psi)
Va = (alpha * inv * (D0(Phi) - D0(Z)) ** 2
      + 4 * inv * D0(Phi) * D0(Z) - 2 * inv * D0(Z) ** 2 - 4 * cN * inv * D0(Z) * D0(Uaux))
Va_2 = sp.expand(sp.series(Va, eps, 0, 3).removeO().coeff(eps, 2))

# -------- on-shell quadratic density (first-order fields) at eps^2, retained with S_k ---
R4_2 = sp.expand(R4.coeff(eps, 2))
R4_1 = sp.expand(R4.coeff(eps, 1))
# linear check of the R4-lapse entry: expected -2 L0(Phi1) - 2 (4cN?): report
print("R4 linear part:", sp.expand(R4_1))

# -------- the branch system at second order (E1-operator family) --------
# lapse:     4 cN L0(phi2 - z2) + quad = 0      (E1 operator; 'the same equations')
# spatial:   4 L0(psi2 - phi2) + quadS = 0      (shell operator; AS226 C2d family)
# quad  = [R4_2 + Va_2] evaluated on the first-order fields (no phi2/psi2 inside)
# quadS = spatial stress sourcing psi2 from the SAME density (sqrt(h) measure moments)
#         = pointwise + IBP variation of sqrt(h)(R4 + Va) at eps^2  (chi-probe, then chi->psi2)
R4_2q = sp.expand(R4_2.subs(varphi2, 0).subs(psi2, 0))
Va_2q = sp.expand(Va_2.subs(varphi2, 0).subs(psi2, 0))
quad = sp.expand(R4_2q + Va_2q)

# spatial source via probe (with explicit IBP of chi' terms)
chi = sp.Function('chi')(r)
s = sp.symbols('s')
Psip = eps * Psi1 + eps**2 * (psi2 + s * chi)
wp = sp.log(1 - 2 * Psip) / 2
R3p = -4 * (1 - 2 * Psip) ** -1 * L0(wp) - 2 * (1 - 2 * Psip) ** -1 * D0(wp) ** 2
R4p = (R3p - 2 * (1 - 2 * Psip) ** -1 * L0(Phi) - 2 * (1 - 2 * Psip) ** -1 * D0(Phi) ** 2
       + 2 * (1 - 2 * Psip) ** -2 * D0(Phi) * D0(Psip))
hp = (1 - 2 * Psip) ** sp.Rational(3, 2)
Vap = Va.subs(psi2, psi2 + s * chi)
prob = sp.expand(sp.diff(hp * (R4p + Vap), s))
prob = sp.expand(sp.series(prob, s, 0, 2).removeO())
prob = sp.expand(sp.series(prob, eps, 0, 3).removeO())
# IBP: chi' F -> - chi D0(F) ;  chi'' F -> + chi L0(F)   (flat leaf; declared)
terms = sp.Add.make_args(sp.expand(prob))
nT, ibp = sp.S.Zero, sp.S.Zero
for t in terms:
    has2 = t.has(sp.Derivative(chi, (r, 2)))
    has1 = t.has(sp.Derivative(chi, r)) and not has2
    if has2:                                    # chi'' F  ->  +chi L0(F)  (flat IBP)
        F = sp.simplify(t / sp.Derivative(chi, (r, 2)))
        ibp += chi * sp.expand(L0(F))
    elif has1:                                  # chi' F   ->  -chi D0(F)
        F = sp.simplify(t / sp.Derivative(chi, r))
        ibp -= chi * sp.expand(D0(F))
    elif t.has(chi):                            # chi F
        nT += t
    else:                                       # chi-free background (sources stay in quadS)
        nT += t * 0
# spatial EL (density form): nT + ibp with chi -> psi2 replacements
EL_sp = sp.expand((nT + ibp).replace(chi, psi2)
                  .replace(sp.Derivative(chi, r), sp.Derivative(psi2, r))
                  .replace(sp.Derivative(chi, (r, 2)), sp.Derivative(psi2, (r, 2))))
EL_sp_2 = sp.expand(EL_sp.coeff(eps, 2))
quadS = sp.expand(EL_sp_2)

# ---------- reduction: vacuum + window + point-source ansatz ----------
UP, UPP = sp.Derivative(U, r), sp.Derivative(U, (r, 2))
L0U = sp.symbols('L0U')
def vac(f):
    f = sp.expand(f).subs(UPP, L0U - 2 * UP / r)
    f = sp.expand(f).subs(L0U, 0).subs(Sk, 0)
    return sp.expand(f)

A, B = sp.symbols('A B')
def to_poly(f):
    f = vac(f)
    if f.has(U) or f.has(UP) or f.has(UPP):
        f = f.replace(D0(U), 0).replace(sp.Derivative(U, (r, 2)), 0).replace(U, 0)
    f = f.replace(varphi2, A / r ** 2).replace(psi2, B / r ** 2)
    f = f.replace(sp.Derivative(varphi2, (r, 2)), 6 * A / r ** 4)
    f = f.replace(sp.Derivative(psi2, (r, 2)), 6 * B / r ** 4)
    f = f.replace(sp.Derivative(varphi2, r), -2 * A / r ** 3)
    f = f.replace(sp.Derivative(psi2, r), -2 * B / r ** 3)
    return sp.expand(sp.simplify(sp.expand(f * r ** 4)))

Elap = sp.expand(to_poly(sp.expand(4 * cN * L0(varphi2 - ell * Sk * varphi2 / 4)) + quad))
Espa = sp.expand(to_poly(sp.expand(4 * L0(psi2 - varphi2)) + quadS))
ElapA = sp.expand(sp.diff(Elap, A).subs(B, 0));  ElapB = sp.expand(sp.diff(Elap, B).subs(A, 0))
EspaA = sp.expand(sp.diff(Espa, A).subs(B, 0));  EspaB = sp.expand(sp.diff(Espa, B).subs(A, 0))
c_l = sp.simplify(Elap.subs({A: 0, B: 0})); c_s = sp.simplify(Espa.subs({A: 0, B: 0}))
print("quad (lapse-source, vac):", sp.simplify(vac(quad)))
print("quadS(spatial-source,vac):", sp.simplify(vac(quadS)))
print("lapse  eps2: [A,B,src] =", ElapA, ElapB, c_l)
print("spatial eps2: [A,B,src] =", EspaA, EspaB, c_s)

sol = sp.solve([ElapA * A + ElapB * B + c_l, EspaA * A + EspaB * B + c_s], [A, B], dict=True)
if sol:
    A_sol, B_sol = sp.simplify(sol[0][A]), sp.simplify(sol[0][B])
    print("phi2/U^2 =", sp.simplify(A_sol), "  psi2/U^2 =", sp.simplify(B_sol))
    print("beta = 1 + phi2/U^2 =", sp.simplify(1 + A_sol))
    bl = sp.simplify(sp.expand(ElapA * A_sol + ElapB * B_sol + c_l))
    bs = sp.simplify(sp.expand(EspaA * A_sol + EspaB * B_sol + c_s))
    print("substitution-back:", bl, bs); assert bl == 0 and bs == 0
    ctl = sp.simplify(sp.expand(EspaB * (-sp.Rational(3, 4)) + c_s))
    print("negative control (beta=1 + Einstein shell) spatial resid:", ctl)
else:
    print("degenerate;", Elap, Espa)

with open('as232_symbolic_out.txt', 'w') as f:
    f.write(f"R4_2 = {R4_2}\nVa_2 = {Va_2}\nquad = {quad}\nquadS = {quadS}\n"
            f"lapse_eq = {ElapA}*A + {ElapB}*B + {c_l}\nspatial_eq = {EspaA}*A + {EspaB}*B + {c_s}\n"
            f"sol = {sol if sol else 'degenerate'}\n")