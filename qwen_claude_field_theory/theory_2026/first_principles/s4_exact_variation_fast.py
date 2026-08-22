#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
s4_exact_variation_fast.py -- program section 4 (task parts b, c, d)
=====================================================================
Piecewise Euler-Lagrange verification (each Lagrangian term against its
display-form contribution; rational cancellation instead of general
simplify; elimination/background checks run on the verified display
forms).  This is the CANONICAL section-4 script; a monolithic variant
was retired because its final simplify step did not terminate in
reasonable time.  The two heavy identities ([4d] and [8]) are
independently corroborated at random rational points to 60 digits in
s4_numeric_spotcheck.py.

Reduction of the FULL frozen action to the static weak-field Lagrangian
L[Phi, Psi] and its EXACT variation with respect to Phi and Psi separately.

Bookkeeping (standard MOND weak-field limit): Phi/c^2, Psi/c^2 = O(eps_wf) << 1
but x = |grad Phi|/a0 arbitrary.  Kept: EH quadratic (coefficients DERIVED
below), eta_K a_i a^i quadratic, F(X,Y) with leading X(Phi), Y(Psi)
(relative corrections O(Phi/c^2); see s2_weakfield_geometry.py), matter -rho Phi
(ASSUMED per task: static dust couples through N only).

Normalisation (IMPORTED, repo anchor): F-term = -(a0^2/8 pi G) F per unit
dt d^3x  =>  M_Pl^2 c^3/2 = c^4/(16 pi G).

Static => K_ij = 0 exactly => lam_K and the K-terms DROP OUT (DERIVED, trivial).

Checks [0]-[9] as in the docstring of s4_exact_variation.py.
"""
import sympy as sp
from sympy.calculus.euler import euler_equations

x, y, z = sp.symbols('x y z', real=True)
c, a0, G, etaK, epsl, e = sp.symbols('c a_0 G eta_K epsilon e', positive=True)
ge, gpe = sp.symbols('g_e g_ep', positive=True)
V = (x, y, z)
Phi = sp.Function('Phi')(x, y, z)
Psi = sp.Function('Psi')(x, y, z)
rho = sp.Function('rho')(x, y, z)
chi = sp.Function('chi')(x, y, z)
delta = sp.eye(3)

def grad(f):  return [sp.diff(f, v) for v in V]
def lap(f):   return sum(sp.diff(f, v, 2) for v in V)
def div(vec): return sum(sp.diff(vec[i], V[i]) for i in range(3))
def S_ij(f, i, j): return sp.diff(f, V[i], V[j]) - delta[i, j] * lap(f) / 3

results = []
def check(name, cond):
    results.append((name, bool(cond)))
    print(('PASS' if cond else 'FAIL'), '--', name, flush=True)

def is_zero(expr):
    ee = sp.expand(expr)
    if ee == 0: return True
    ee = sp.cancel(sp.together(ee))
    if ee == 0: return True
    ee = sp.simplify(ee)
    return ee == 0 or (hasattr(ee, 'equals') and ee.equals(0) is True)

def subs_fields(expr, fPhi, fPsi):
    return expr.subs([(Phi, fPhi), (Psi, fPsi)]).doit()

def EL(L, funcs):
    """Euler-Lagrange expression for each func separately; 0 if L lacks it."""
    out = []
    for f in funcs:
        if not L.has(f):
            out.append(sp.S(0))
            continue
        qs = euler_equations(L, [f], V)
        # euler_equations returns [] when the EL expression is identically 0
        out.append(qs[0].lhs - qs[0].rhs if qs else sp.S(0))
    return out

# ----------------------------------------------------------------------
# exact 3D Ricci (convention validated on the unit 3-sphere in s2 script)
def christoffel(g, coords):
    n = len(coords); ginv = g.inv()
    Gam = [[[sp.S(0)] * n for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for b in range(n):
            for d in range(b, n):
                ex = sum(ginv[a, s] * (sp.diff(g[s, b], coords[d])
                                       + sp.diff(g[s, d], coords[b])
                                       - sp.diff(g[b, d], coords[s]))
                         for s in range(n)) / 2
                ex = sp.cancel(sp.together(ex))
                Gam[a][b][d] = ex; Gam[a][d][b] = ex
    return Gam

def ricci(g, coords):
    n = len(coords); Gam = christoffel(g, coords)
    Ric = sp.zeros(n)
    for b in range(n):
        for d in range(b, n):
            expr = sp.S(0)
            for a in range(n):
                expr += sp.diff(Gam[a][b][d], coords[a]) - sp.diff(Gam[a][a][b], coords[d])
                for l in range(n):
                    expr += Gam[a][a][l] * Gam[l][b][d] - Gam[a][d][l] * Gam[l][a][b]
            Ric[b, d] = sp.cancel(sp.together(expr)); Ric[d, b] = Ric[b, d]
    return Ric

# ----------------------------------------------------------------------
# (b) EH sector: exact N sqrt(h) (3)R to second order in amplitude e
print('... computing exact N sqrt(h) (3)R and expanding', flush=True)
N  = 1 + e * Phi / c**2
W  = 1 - 2 * e * Psi / c**2
h3 = sp.diag(W, W, W)
Ric3 = ricci(h3, V)
R3   = sp.cancel(sp.together(sum(Ric3[i, i] for i in range(3)) / W))
EHdensity = N * W**sp.Rational(3, 2) * R3

def coeff_e(expr, k):
    return sp.expand(sp.diff(expr, e, k).subs(e, 0) / sp.factorial(k))

E0 = coeff_e(EHdensity, 0)
E1 = coeff_e(EHdensity, 1)
E2 = coeff_e(EHdensity, 2)
check('[0] O(e^0) of N sqrt(h) (3)R vanishes (flat background)', is_zero(E0))
check('[1] O(e^1) of N sqrt(h) (3)R is a total divergence (no tadpole)',
      all(is_zero(q) for q in EL(E1, [Phi, Psi])))

# [2] canonical quadratic form: SOLVE for alpha, beta (not quoted)
al, be = sp.symbols('alpha beta')
cand = (al * sum(gi**2 for gi in grad(Psi))
        + be * sum(grad(Phi)[i] * grad(Psi)[i] for i in range(3))) / c**4
eldiff = EL(sp.expand(E2 - cand), [Phi, Psi])
probes = [(x**2 + x*y, y**2 + z**2 + x*z), (x*y*z + x**3, x**2*y + z**3)]
lin_eqs = []
for fP, fS in probes:
    for q in eldiff:
        pol = sp.Poly(sp.expand(subs_fields(q, fP, fS)), x, y, z)
        lin_eqs.extend(pol.coeffs())
sol = sp.solve(list(set(lin_eqs)), [al, be], dict=True)
assert len(sol) == 1, 'alpha,beta not uniquely determined: %s' % sol
alv, bev = sol[0][al], sol[0][be]
print('    solved: alpha = %s, beta = %s' % (alv, bev), flush=True)
ok2 = all(is_zero(q.subs([(al, alv), (be, bev)])) for q in eldiff)
check('[2] N sqrt(h)(3)R|_e2 == (1/c^4)[%s (grad Psi)^2 + (%s) grad Phi.grad Psi]'
      ' + total div' % (alv, bev), ok2)

# ----------------------------------------------------------------------
# (b) the pieces of the full static weak-field Lagrangian (per unit dt d^3x)
pref = c**4 / (16 * sp.pi * G)          # = M_Pl^2 c^3/2, fixed by the F-anchor
gP = grad(Phi); gS = grad(Psi)
gradPhi2 = sum(gi**2 for gi in gP)
X  = gradPhi2 / a0**2
xs = sp.sqrt(X)
Fmond = -2 * xs + 2 * sp.log(1 + xs)
Afun  = X**2 / (1 + X)**4
Y  = c**4 / a0**4 * sum(S_ij(Psi, i, j)**2 for i in range(3) for j in range(3))

L_EH  = pref * (alv * sum(gi**2 for gi in gS)
                + bev * sum(gP[i] * gS[i] for i in range(3))) / c**4
L_eta = pref * etaK * gradPhi2 / c**4
L_Fm  = -(a0**2 / (8 * sp.pi * G)) * Fmond
L_Fe  = -(a0**2 / (8 * sp.pi * G)) * epsl * Afun * Y
L_m   = -rho * Phi

# [3] repo facts re-derived
Xs = sp.symbols('X_s', positive=True)
FX_sym = sp.diff(-2 * sp.sqrt(Xs) + 2 * sp.log(1 + sp.sqrt(Xs)), Xs)
ok3 = is_zero(FX_sym + 1 / (1 + sp.sqrt(Xs)))
ok3 = ok3 and is_zero(sp.diff(Xs**2 / (1 + Xs)**4, Xs)
                      - 2 * Xs * (1 - Xs) / (1 + Xs)**5)
check("[3] F_X = -1/(1+sqrt(X)) and A'(X) = 2X(1-X)/(1+X)^5", ok3)

# ----------------------------------------------------------------------
# (c) exact variation, PIECE BY PIECE against display-form contributions
FX = -1 / (1 + xs)
Ap = 2 * X * (1 - X) / (1 + X)**5

print('... varying L_EH', flush=True)
q = EL(L_EH, [Phi, Psi])
okEH = is_zero(q[0] - lap(Psi) / (4 * sp.pi * G)) \
   and is_zero(q[1] + (lap(Psi) - lap(Phi)) / (4 * sp.pi * G))
check('[4a] EL of EH part: dPhi -> (1/4piG) lap Psi ; '
      'dPsi -> -(1/4piG) lap(Psi - Phi)', okEH)

print('... varying L_eta', flush=True)
q = EL(L_eta, [Phi, Psi])
okETA = is_zero(q[0] + (etaK / (8 * sp.pi * G)) * lap(Phi)) and is_zero(q[1])
check('[4b] EL of eta_K a_i a^i part: dPhi -> -(eta_K/8piG) lap Phi ; dPsi -> 0', okETA)

print('... varying the MOND part of F', flush=True)
q = EL(L_Fm, [Phi, Psi])
okFM = is_zero(q[0] - div([FX * gP[i] for i in range(3)]) / (4 * sp.pi * G)) \
   and is_zero(q[1])
check('[4c] EL of -(a0^2/8piG)F_mond: dPhi -> (1/4piG) div(F_X grad Phi) ; dPsi -> 0',
      okFM)

print('... varying the eps A(X) Y part of F (the slow one)', flush=True)
q = EL(L_Fe, [Phi, Psi])
tidal = sum(sp.diff(Afun * S_ij(Psi, i, j), V[i], V[j])
            for i in range(3) for j in range(3))
okFE = is_zero(q[0] - (epsl / (4 * sp.pi * G)) * div([Ap * Y * gP[i] for i in range(3)])) \
   and is_zero(q[1] + (epsl * c**4 / (4 * sp.pi * G * a0**2)) * tidal)
check("[4d] EL of -(a0^2/8piG) eps A(X)Y: dPhi -> (eps/4piG) div(A'(X) Y grad Phi) ;"
      ' dPsi -> -(eps c^4/4piG a0^2) d_i d_j (A(X) S_ij[Psi])', okFE)

q = EL(L_m, [Phi, Psi])
okM = is_zero(q[0] + rho) and is_zero(q[1])
check('[4e] EL of matter -rho Phi: dPhi -> -rho ; dPsi -> 0 (dust sources ONLY '
      'the lapse equation)', okM)

# assembled display forms (now established exactly):
target_phi = (lap(Psi) + div([(FX - etaK / 2 + epsl * Ap * Y) * gP[i]
                              for i in range(3)])) / (4 * sp.pi * G) - rho
target_psi = -(lap(Psi) - lap(Phi) + (epsl * c**4 / a0**2) * tidal) / (4 * sp.pi * G)
check('[4]+[5] full Phi-equation and Psi-equation assembled from the verified pieces '
      '(linearity of EL)', okEH and okETA and okFM and okFE and okM)

# ----------------------------------------------------------------------
# [6] GR limit
check('[6] GR limit (F=0, eta_K=0): lap Psi = 4 pi G rho and lap(Psi-Phi)=0 => Phi=Psi',
      okEH and okM)

# ----------------------------------------------------------------------
# [7] derivative orders (on the verified display forms, fully expanded)
def max_order(expr, f):
    m = 0
    for d in sp.expand(expr).atoms(sp.Derivative):
        if d.expr == f:
            m = max(m, d.derivative_count)
    return m

oPsi_in_psi = max_order(target_psi, Psi); oPhi_in_psi = max_order(target_psi, Phi)
oPhi_in_phi = max_order(target_phi, Phi); oPsi_in_phi = max_order(target_phi, Psi)
print('    orders: Psi-eq: d^%d Psi, d^%d Phi | Phi-eq: d^%d Phi, d^%d Psi'
      % (oPsi_in_psi, oPhi_in_psi, oPhi_in_phi, oPsi_in_phi), flush=True)
check('[7] Psi-eq is FOURTH order in Psi (not sixth), 3rd in Phi; '
      'Phi-eq 2nd in Phi, 3rd in Psi (at order eps)',
      oPsi_in_psi == 4 and oPhi_in_psi == 3 and oPhi_in_phi == 2 and oPsi_in_phi == 3)

# ----------------------------------------------------------------------
# [8] elimination -> the single-potential schematic at O(eps)
print('... elimination check', flush=True)
elphi_sub = target_phi.subs(Psi, Phi + epsl * chi).doit()
elpsi_sub = target_psi.subs(Psi, Phi + epsl * chi).doit()

def coeff_eps(expr, k):
    return sp.expand(sp.diff(expr, epsl, k).subs(epsl, 0) / sp.factorial(k))

YPhi = c**4 / a0**4 * sum(S_ij(Phi, i, j)**2 for i in range(3) for j in range(3))
tidalPhi = sum(sp.diff(Afun * S_ij(Phi, i, j), V[i], V[j])
               for i in range(3) for j in range(3))
schematic = div([(1 - etaK / 2 + FX + epsl * Ap * YPhi) * gP[i] for i in range(3)]) \
            - (epsl * c**4 / a0**2) * tidalPhi - 4 * sp.pi * G * rho

d_expr = 4 * sp.pi * G * elphi_sub - schematic
ok8a = is_zero(coeff_eps(d_expr, 0))
mismatch = coeff_eps(d_expr, 1)
onshell  = coeff_eps(elpsi_sub, 1)   # -(1/4piG)[lap chi + (c^4/a0^2) didj(A S[Phi])]
ok8b = is_zero(mismatch + 4 * sp.pi * G * onshell)
check('[8] eliminating Psi via its own equation reproduces the single-potential '
      'schematic at O(eps), on-shell, with kernel 1 - eta_K/2 + F_X', ok8a and ok8b)

# ----------------------------------------------------------------------
# [9] uniform-gradient backgrounds: vacuum equations hold for ANY (g_e, g_e')
bg_phi = subs_fields(target_phi.subs(rho, 0), -ge * z, -gpe * z)
bg_psi = subs_fields(target_psi, -ge * z, -gpe * z)
check("[9] Phi=-g_e z, Psi=-g_e' z solve both vacuum equations for arbitrary "
      "(g_e, g_e'): background slip NOT fixed locally",
      is_zero(bg_phi) and is_zero(bg_psi))

# ----------------------------------------------------------------------
print("""
DISPLAY FORM OF THE COUPLED STATIC SYSTEM (all coefficients verified above):

  (I)  lap Psi + div[ (F_X(X) - eta_K/2 + eps A'(X) Y) grad Phi ] = 4 pi G rho
       with F_X = -1/(1+sqrt(X)), X = |grad Phi|^2/a0^2,
       Y = (c^4/a0^4) S_ij[Psi] S_ij[Psi]

  (II) lap (Psi - Phi) = - (eps c^4/a0^2) d_i d_j [ A(X) S_ij[Psi] ]
       with A = X^2/(1+X)^4,  S_ij[f] = d_i d_j f - (1/3) delta_ij lap f

  The Phi-equation (lapse sector) carries F_X; the Newtonian '1' of
  mu = 1 + F_X is delivered by lap Psi through (II).  The tidal operator
  lives in the Psi-equation and acts on S_ij[Psi], NOT S_ij[Phi].
  Slip Psi - Phi = O(eps), fourth-order operator.
""", flush=True)
n_fail = sum(1 for _, ok in results if not ok)
print('%d checks, %d failed' % (len(results), n_fail))
raise SystemExit(1 if n_fail else 0)
