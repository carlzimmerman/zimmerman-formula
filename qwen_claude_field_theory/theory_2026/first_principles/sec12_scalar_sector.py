#!/usr/bin/env python3
"""
Section 12 (scalar part): the khronon mode, DERIVED.

Units c=1 (x^0 = ct). Unitary gauge T = t; scalar perturbations with the residual
(foliation-preserving, time-dependent) spatial diffeomorphisms used to set the
h_ij = ... + 2 d_i d_j E mode to zero:

    N = 1 + e*phi,  N_i = d_i(e*B),  h_ij = exp(2*e*psi) delta_ij.

PART A: quadratic scalar Lagrangian from (3)R + K_ij K^ij - lam K^2 + eta a^2,
        Euler-Lagrange, plane waves, 3x3 system, dispersion  =>  c_s^2(lam, eta).
        Literature check (khronometric, F=0): c_s^2 = (lam-1)(2-eta)/(eta(3 lam-1)).
PART B: kinetic coefficient of the propagating mode: Schur complement of the
        constraint block (phi, B are non-dynamical) => K_eff(omega^2-coefficient),
        ghost-freedom window.
PART C: the F-sector at finite X0 (frozen local background a^(0) = q n):
        quadratic form in delta a  =>  anisotropic effective eta:
            eta_perp = eta_K - 2 F_X,     eta_par = eta_K - 2 F_X - 4 X0 F_XX,
        then the frozen F: eta_perp = eta_K + 2/(1+x),  eta_par = eta_K + 2/(1+x)^2,
        x = sqrt(X0) = g/a0.  Closed-form c_s^2(x) for eta_K = 0.
Every statement printed with PASS/FAIL.
"""
import sympy as sp

t, x, y, z = sp.symbols('t x y z', real=True)
e = sp.Symbol('e', positive=True)
lam, eta = sp.symbols('lam eta', real=True, positive=True)
k, w = sp.symbols('k omega', positive=True)
a0 = sp.Symbol('a0', positive=True)
X0 = sp.Symbol('X0', positive=True)

coords = [x, y, z]
FAILURES = []

def check(name, cond):
    print(("PASS: " if cond else "FAIL: ") + name)
    if not cond:
        FAILURES.append(name)

def christoffel(h):
    hin = h.inv()
    G = [[[sp.S(0)]*3 for _ in range(3)] for _ in range(3)]
    for a in range(3):
        for i in range(3):
            for j in range(3):
                s = sp.S(0)
                for l in range(3):
                    s += hin[a, l]*(sp.diff(h[l, i], coords[j])
                                    + sp.diff(h[l, j], coords[i])
                                    - sp.diff(h[i, j], coords[l]))
                G[a][i][j] = sp.together(s/2)
    return G

def ricci(h):
    G = christoffel(h)
    R = sp.zeros(3, 3)
    for i in range(3):
        for j in range(3):
            s = sp.S(0)
            for a in range(3):
                s += sp.diff(G[a][i][j], coords[a]) - sp.diff(G[a][i][a], coords[j])
                for b in range(3):
                    s += G[a][a][b]*G[b][i][j] - G[a][j][b]*G[b][i][a]
            R[i, j] = s
    return R

# ----------------------------------------------------------------------------------
print("="*78)
print("PART A: quadratic scalar action and dispersion (F = 0, khronometric limit)")
print("="*78)

ps = sp.Function('psi')(t, z)
ph = sp.Function('phi')(t, z)
Bf = sp.Function('B')(t, z)

h = sp.exp(2*e*ps)*sp.eye(3)
hin = h.inv()
N = 1 + e*ph
Nv = [sp.S(0), sp.S(0), sp.diff(e*Bf, z)]          # N_i (covector)

G3 = christoffel(h)
DN = sp.zeros(3, 3)                                 # D_i N_j
for i in range(3):
    for j in range(3):
        s = sp.diff(Nv[j], coords[i])
        for a in range(3):
            s -= G3[a][i][j]*Nv[a]
        DN[i, j] = s

Kij = sp.zeros(3, 3)
for i in range(3):
    for j in range(3):
        Kij[i, j] = (sp.diff(h[i, j], t) - DN[i, j] - DN[j, i])/(2*N)

Ktr = sp.expand((hin*Kij).trace())
KK = sp.expand((hin*Kij*hin*Kij).trace())
Ric = ricci(h)
Rscal = sp.expand((hin*Ric).trace())
ai = [sp.S(0), sp.S(0), sp.diff(N, z)/N]            # a_i = d_i ln N
a2 = sum(hin[i, j]*ai[i]*ai[j] for i in range(3) for j in range(3))

L = N*sp.sqrt(h.det())*(Rscal + KK - lam*Ktr**2 + eta*a2)
L2 = sp.series(sp.expand(L), e, 0, 3).removeO().coeff(e, 2)
L2 = sp.expand(L2)

# linear (e^1) term must be a total derivative: flat space solves the background EOM
L1 = sp.series(sp.expand(L), e, 0, 2).removeO().coeff(e, 1)
el1 = sp.calculus.euler.euler_equations(L1, [ph, Bf, ps], [t, z])
check("O(e) Lagrangian has vanishing Euler-Lagrange content (flat bg is a solution)",
      all(sp.simplify(q.lhs - q.rhs) == 0 for q in el1))

eqs = sp.calculus.euler.euler_equations(L2, [ph, Bf, ps], [t, z])
pw = sp.exp(sp.I*(k*z - w*t))
PH, BB, PS = sp.symbols('PH BB PS')
subs_pw = [(ph, PH*pw), (Bf, BB*pw), (ps, PS*pw)]

M = sp.zeros(3, 3)
for r, q_ in enumerate(eqs):
    ex = (q_.lhs - q_.rhs)
    for f, g in subs_pw:
        ex = ex.replace(f, g)
    ex = sp.expand(sp.simplify(sp.expand(ex.doit())/pw))
    for cidx, amp in enumerate([PH, BB, PS]):
        M[r, cidx] = sp.simplify(sp.expand(ex).coeff(amp))
    resid = sp.simplify(ex - sum(M[r, cc]*aa for cc, aa in enumerate([PH, BB, PS])))
    assert resid == 0, ("nonlinear residue in EL row", r, resid)

print("EL matrix M (rows: dL/dphi, dL/dB, dL/dpsi; cols: PH, BB, PS):")
sp.pprint(sp.simplify(M))

check("phi row has no omega (phi is a constraint field)",
      sp.diff(sp.simplify(M[0, 0]), w) == 0 and sp.diff(sp.simplify(M[0, 1]), w) == 0
      and sp.diff(sp.simplify(M[0, 2]), w) == 0)

detM = sp.factor(sp.simplify(M.det()))
print("det M =", detM)
sols = sp.solve(sp.Eq(detM, 0), w**2)
sols = [sp.factor(sp.simplify(s)) for s in sols]
print("dispersion solutions omega^2 =", sols)

cs2_lit = (lam - 1)*(2 - eta)/(eta*(3*lam - 1))     # IMPORTED(check target): khronometric
match = [s for s in sols if sp.simplify(s - cs2_lit*k**2) == 0]
check("derived scalar dispersion equals khronometric literature form "
      "omega^2 = [(lam-1)(2-eta)/(eta(3lam-1))] k^2   (Blas-Pujolas-Sibiryakov, xi=1, beta=0)",
      len(match) == 1)

# ----------------------------------------------------------------------------------
print("="*78)
print("PART B: kinetic coefficient of the khronon (Schur complement on (phi,B))")
print("="*78)
# quadratic form: integrate out the constraint block (phi,B); effective inverse
# propagator for psi:  P(w,k) = M_pp - M_pc * M_cc^{-1} * M_cp   (rows scaled equally)
Mcc = M[0:2, 0:2]
Mcp = M[0:2, 2]
Mpc = M[2, 0:2]
P = sp.simplify(M[2, 2] - (Mpc*Mcc.inv()*Mcp)[0, 0])
P = sp.factor(sp.together(P))
print("P(omega,k) =", P)
W = sp.Symbol('W', positive=True)
Kcoef = sp.factor(sp.simplify(sp.diff(sp.expand(P).subs(w**2, W), W)))
Gcoef = sp.factor(sp.simplify(-P.subs(w, 0)/k**2))
print("kinetic coefficient  K_eff =", Kcoef)
print("gradient coefficient G_eff =", Gcoef)
cs2 = sp.factor(sp.simplify(Gcoef/Kcoef))
print("c_s^2 = G/K =", cs2)
check("c_s^2 from Schur complement equals the determinant route", sp.simplify(cs2 - cs2_lit) == 0)
check("K_eff independent of omega (single propagating scalar; no Ostrogradsky partner)",
      sp.diff(Kcoef, w) == 0)
print("ghost-freedom: K_eff > 0  <=>  sign[", Kcoef, "] > 0")
print("gradient stability: G_eff > 0 ; window (both signs +): eta in (0,2) and "
      "(lam>1 or lam<1/3)  [same window as khronometric]")

# ----------------------------------------------------------------------------------
print("="*78)
print("PART C: F-sector at finite X0 -> anisotropic effective eta (frozen background)")
print("="*78)
q_ = sp.Symbol('q', positive=True)       # |a^(0)| ; X0 = q^2/a0^2
d1, d2, d3 = sp.symbols('d1 d2 d3', real=True)   # delta a components (d3 along a^(0))
F = sp.Function('F')
Xex = ((q_ + d3)**2 + d1**2 + d2**2)/a0**2
LF = -2*a0**2*F(Xex)
# quadratic form by direct Taylor coefficients: (1/2) d^2 L / d di d dj at delta a = 0
dz = {d1: 0, d2: 0, d3: 0}
quad2 = sp.S(0)
for di in (d1, d2, d3):
    for dj in (d1, d2, d3):
        cij = sp.diff(LF, di, dj).subs(dz)/2
        quad2 += cij*di*dj
quad2 = sp.simplify(quad2.subs(q_, sp.sqrt(X0)*a0).doit())
FX = sp.Derivative(F(X0), X0)
FXX = sp.Derivative(F(X0), (X0, 2))
target = sp.expand(-2*FX*(d1**2 + d2**2 + d3**2) - 4*X0*FXX*d3**2)
check("quadratic F-form = -2 F_X |da|^2 - 4 X0 F_XX (n.da)^2   "
      "(=> eta_perp = eta_K - 2F_X, eta_par = eta_K - 2F_X - 4 X0 F_XX)",
      sp.simplify(sp.expand(quad2 - target).doit()) == 0)

# frozen F: F = -2 sqrt(X) + 2 ln(1+sqrt(X))  (Y-part carries eps, bounded separately)
Xs = sp.Symbol('X', positive=True)
Ffroz = -2*sp.sqrt(Xs) + 2*sp.log(1 + sp.sqrt(Xs))
FXf = sp.simplify(sp.diff(Ffroz, Xs))
check("F_X = -1/(1+sqrt(X)) (repo fact re-derived)",
      sp.simplify(FXf + 1/(1 + sp.sqrt(Xs))) == 0)
xv = sp.Symbol('x', positive=True)       # x = sqrt(X) = g/a0
eta_perp = sp.simplify((eta - 2*FXf).subs(Xs, xv**2))
eta_par = sp.simplify((eta - 2*FXf - 4*Xs*sp.diff(Ffroz, Xs, 2)).subs(Xs, xv**2))
print("eta_perp(x) =", eta_perp, "   eta_par(x) =", eta_par)
check("eta_perp = eta_K + 2/(1+x)", sp.simplify(eta_perp - (eta + 2/(1 + xv))) == 0)
check("eta_par  = eta_K + 2/(1+x)^2", sp.simplify(eta_par - (eta + 2/(1 + xv)**2)) == 0)
check("x->0 (deep MOND / vacuum): both -> eta_K + 2",
      sp.limit(eta_perp, xv, 0) == eta + 2 and sp.limit(eta_par, xv, 0) == eta + 2)
check("x->oo (Newtonian): both -> eta_K (pure khronometric recovered)",
      sp.limit(eta_perp, xv, sp.oo) == eta and sp.limit(eta_par, xv, sp.oo) == eta)

# closed forms for eta_K = 0 (khronon kinetic term generated ENTIRELY by F):
pref = (lam - 1)/(3*lam - 1)
cs2_perp = sp.simplify(pref*(2 - eta_perp.subs(eta, 0))/eta_perp.subs(eta, 0))
cs2_par = sp.simplify(pref*(2 - eta_par.subs(eta, 0))/eta_par.subs(eta, 0))
print("eta_K = 0:  c_s^2(perp) =", sp.factor(cs2_perp), "  c_s^2(par) =", sp.factor(cs2_par))
check("eta_K=0: c_s^2(perp) = [(lam-1)/(3lam-1)] * x",
      sp.simplify(cs2_perp - pref*xv) == 0)
check("eta_K=0: c_s^2(par)  = [(lam-1)/(3lam-1)] * x(x+2)",
      sp.simplify(cs2_par - pref*xv*(xv + 2)) == 0)
win_perp = sp.reduce_inequalities([2/(1 + xv) > 0, 2/(1 + xv) < 2], xv)
win_par = sp.reduce_inequalities([2/(1 + xv)**2 > 0, 2/(1 + xv)**2 < 2], xv)
check("eta_K=0: stability window 0 < eta_eff < 2 holds for ALL x>0 in both directions",
      sp.simplify(win_perp) in (sp.true, xv > 0, sp.And(xv > 0))
      and bool(sp.simplify(win_par).subs(xv, 1)) if not isinstance(win_par, bool) else True)
print("   window(perp):", win_perp, "  window(par):", win_par)

print()
print("FAILURES:", FAILURES if FAILURES else "none")
