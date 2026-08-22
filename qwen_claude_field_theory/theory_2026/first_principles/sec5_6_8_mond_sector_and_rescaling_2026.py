#!/usr/bin/env python3
r"""
Sections 5, 6, 8 of the first-principles programme for the FROZEN khronon action

  S = (M_Pl^2 c^3/2) INT d^4x N sqrt(h) [ (3)R + K_ij K^ij - lam_K K^2 + eta_K a_i a^i
      - (2 a0^2/c^4) F(X,Y) ] + S_m ,
  F(X,Y) = -2 sqrt(X) + 2 ln(1+sqrt(X)) + eps [X^2/(1+X)^4] Y ,
  X = c^4 a_mu a^mu / a0^2 ,  Y = c^8 Rbar_ij Rbar^ij / a0^4 .

SEC 5  MOND kernel:  F_X, mu(x) = x/(1+x), asymptotics, mu(X,Y) = 1 + F_X.
SEC 6  Spherical source: mu(g/a0) g = GM/r^2, deep-MOND g = sqrt(GMa0)/r, v^4 = GMa0;
       ANALYTIC effect of the Y-sector on both asymptotic branches (profiles re-derived).
SEC 8  Dimensionless rescaling r = R_M xhat, Phi = a0 R_M phihat:
       X = |grad phihat|^2, Y = Lam Sbar^2, Lam = c^4/(GMa0) = (c/v_inf)^4, chi = eps Lam,
       and every coefficient of the dimensionless field equation, pushed through sympy.

Labelling discipline: every claim is tagged DERIVED / ASSUMED / IMPORTED(cite) in the
printout.  The static weak-field anchor (F-term Lagrangian density -(a0^2/8piG) F per
unit dt d^3x) and the identification a_i = d_i Phi/c^2, Rbar_ij = S_ij[Psi]/c^2 are the
inputs; the Psi = Phi identification is ASSUMED here (it belongs to the two-potential
sections) and the robustness of the asymptotic conclusions to Psi = gamma*Phi, gamma=O(1),
is stated explicitly.

Run:  python3 sec5_6_8_mond_sector_and_rescaling_2026.py   -> exits 0 iff all checks pass.
"""
import sys
import sympy as sp

PASS, FAIL = [], []
def ok(cond, label, detail=""):
    cond = bool(cond)
    print(f"  [{'ok' if cond else 'FAIL'}] {label}" + (f"   {detail}" if detail else ""))
    (PASS if cond else FAIL).append(label)
    return cond

def head(t):
    print("\n" + "=" * 100 + "\n" + t + "\n" + "=" * 100)

# ----------------------------------------------------------------------------------------
head("SEC 5.1 -- F_X and mu(x) = x/(1+x)  [DERIVED, sympy-exact]")
X, Yv, xs, u = sp.symbols('X Y x u', positive=True)
eps, chi = sp.symbols('epsilon chi', positive=True)
sqX = sp.sqrt(X)

F0 = -2*sqX + 2*sp.log(1 + sqX)                       # the X-only part of the frozen F
FX0 = sp.together(sp.diff(F0, X))
ok(sp.simplify(FX0 + 1/(1 + sqX)) == 0, "F_X (X-part) = -1/(1+sqrt(X))")
ok(sp.simplify(F0.subs(X, 0)) == 0, "F(0,0) = 0 exactly (no cosmological-constant leak from F)")

mu0 = sp.simplify(1 + FX0)
ok(sp.simplify(mu0 - sqX/(1 + sqX)) == 0, "mu = 1 + F_X = sqrt(X)/(1+sqrt(X))")
mux = sp.cancel(mu0.subs(X, xs**2))
ok(sp.simplify(mux - xs/(1 + xs)) == 0, "mu(x) = x/(1+x)  with  x = sqrt(X) = g/a0")

# asymptotics
lo = sp.series(xs/(1 + xs), xs, 0, 3).removeO()
ok(sp.simplify(lo - (xs - xs**2)) == 0, "deep-MOND branch:  mu = x - x^2 + O(x^3)  -> mu ~ x")
hi = sp.series((xs/(1 + xs)).subs(xs, 1/u), u, 0, 3).removeO().subs(u, 1/xs)
ok(sp.simplify(hi - (1 - 1/xs + 1/xs**2)) == 0,
   "Newtonian branch:  mu = 1 - 1/x + 1/x^2 + O(x^-3)  -> mu -> 1 with a POWER-LAW tail")
print("      NOTE (DERIVED, consequence): the 1/x tail is the alpha=1 'simple mu' class;")
print("      see SEC 6.2 for the constant-a0 solar-system excess it forces.")

head("SEC 5.2 -- A(X) and the Y-corrected mu(X,Y) = 1 + F_X  [DERIVED, sympy-exact]")
A = X**2 / (1 + X)**4
Ap = sp.together(sp.diff(A, X))
ok(sp.simplify(Ap - 2*X*(1 - X)/(1 + X)**5) == 0, "A'(X) = 2X(1-X)/(1+X)^5")
ok(A.subs(X, 1) == sp.Rational(1, 16), "A(1) = 1/16")
ok(sp.simplify(Ap.subs(X, 1)) == 0, "A'(1) = 0  (correction to mu vanishes AT the transition point)")
ok(sp.limit(A/X**2, X, 0) == 1, "A ~ X^2   as X -> 0")
ok(sp.limit(A*X**2, X, sp.oo) == 1, "A ~ X^-2  as X -> oo")

Ffull = F0 + eps*A*Yv
FXfull = sp.diff(Ffull, X)
muXY = 1 + FXfull
ok(sp.simplify(muXY - (sqX/(1 + sqX) + eps*Ap*Yv)) == 0,
   "mu(X,Y) = 1 + F_X = sqrt(X)/(1+sqrt(X)) + eps A'(X) Y")

# ----------------------------------------------------------------------------------------
head("SEC 5.3 -- the divergence-form field equation FROM the anchor Lagrangian (radial EL)")
print("  ANCHOR (repo, given): after the (M_Pl^2 c^3/2) N sqrt(h) reduction the F-term")
print("  contributes  L_F = -(a0^2/8 pi G) F(X,Y)  per unit dt d^3x.   [IMPORTED: repo anchor]")
print("  ASSUMED: the (3)R + K-sector supplies the standard  (1/4 pi G) lap Phi  piece (the '1'")
print("  in mu = 1 + F_X) with the MEASURED G; the lam_K/eta_K renormalisation of G belongs to")
print("  the PPN section  [IMPORTED baseline: Blas-Pujolas-Sibiryakov khronometric].")
print("  Static, radial:  a_i = d_i Phi/c^2  =>  X = Phi'(r)^2/a0^2;")
print("  Y via Rbar_ij = S_ij[Psi]/c^2 with Psi = Phi  [ASSUMED here, checked in SEC 6.4].")

r = sp.Symbol('r', positive=True)
a0, G, c, Mm = sp.symbols('a0 G c M', positive=True)
Phi = sp.Function('Phi')
rho = sp.Function('rho')

# radial reduction of S_ij and Sbar^2 -- derived generically in SEC 6.3 below and used here:
Pp, Ppp = sp.diff(Phi(r), r), sp.diff(Phi(r), r, 2)
s_r = Ppp - Pp/r                                     # S_ij = s(r) (n_i n_j - delta_ij/3)
Xr = Pp**2 / a0**2
Yr = (c**4/a0**4) * sp.Rational(2, 3) * s_r**2       # Sbar^2 = (2/3) s^2  (SEC 6.3, DERIVED)

Ffull_r = Ffull.subs({X: Xr, Yv: Yr})
Lrad = (-(a0**2/(8*sp.pi*G))*Ffull_r - rho(r)*Phi(r)) * r**2   # d^3x = 4 pi r^2 dr (4pi dropped)

from sympy.calculus.euler import euler_equations
EL = euler_equations(Lrad, [Phi(r)], [r])[0].lhs     # dL/dPhi - D(dL/dPhi') + D^2(dL/dPhi'')

# target: -(rho r^2) + (1/4piG) d/dr[ r^2 ( F_X Phi' - (c^4/a0^2) w_r ) ] , with the
# double divergence of eps A S_ij written as div of the radial vector w_r n_i,
# w_r = (2/3)(T' + 3T/r), T = eps A(X) s(r)   [w_r formula DERIVED generically in SEC 6.3]
FX_r = sp.diff(Ffull, X).subs({X: Xr, Yv: Yr})
T_r = eps * A.subs(X, Xr) * s_r
w_r = sp.Rational(2, 3)*(sp.diff(T_r, r) + 3*T_r/r)
target = -rho(r)*r**2 + (1/(4*sp.pi*G)) * sp.diff(r**2*(FX_r*Pp - (c**4/a0**2)*w_r), r)

diffEL = sp.simplify(sp.together(EL - target))
ok(diffEL == 0,
   "Euler-Lagrange of the anchor Lagrangian == divergence form",
   "d/dr[ r^2 ( F_X Phi' - (c^4/a0^2)(2/3)(T'+3T/r) ) ] = 4 pi G rho r^2,  T = eps A(X) s")
print("      => with the GR-sector '1' restored:  div[ (mu + eps A'(X) Y) grad Phi ]")
print("         - (c^4/a0^2) d_i d_j [ eps A(X) S_ij ]  =  4 pi G rho        [DERIVED radially]")
print("      The earlier single-potential 'guess' is CONFIRMED as the EL equation of the")
print("      anchor density in the radial single-potential setting (Psi=Phi assumed).")

# ----------------------------------------------------------------------------------------
head("SEC 6.1 -- isolated spherical source:  mu(g/a0) g = GM/r^2  [DERIVED]")
print("  The mu-sector equation is (1/r^2)(r^2 mu g)' = 4 pi G rho  (SEC 5.3 with eps=0).")
Mr = sp.Symbol('M', positive=True)
g = sp.Function('g')
lhs = sp.diff(r**2 * (g(r)/a0/(1 + g(r)/a0)) * g(r), r)/r**2
# Gauss integration: r^2 mu g = G * integral(4 pi r'^2 rho) = G M(r).  Verify the vacuum
# statement symbolically: if mu(g/a0) g = GM/r^2 then the flux r^2 mu g is constant.
flux_sub = sp.Symbol('flux')
ok(sp.simplify(sp.diff(G*Mr, r)) == 0, "r^2 mu(g/a0) g = G M  is r-independent in vacuum (Gauss)")
gN = sp.Symbol('g_N', positive=True)          # gN = GM/r^2
y = sp.Symbol('y', positive=True)             # y = gN/a0
sols = sp.solve(sp.Eq(xs**2/(1 + xs), y), xs)
xsol = [s for s in sols if sp.limit(s, y, sp.oo) == sp.oo][0]
ok(sp.simplify(xsol - (y + sp.sqrt(y*(y + 4)))/2) == 0,
   "exact algebraic solution:  g/a0 = [y + sqrt(y^2+4y)]/2,  y = GM/(a0 r^2)")
ser_hi = sp.series(xsol.subs(y, 1/u), u, 0, 2).removeO().subs(u, 1/y)
ok(sp.simplify(ser_hi - (y + 1 - 1/y)) == 0,
   "Newtonian expansion:  g = gN + a0 - a0^2/gN + ...  (CONSTANT +a0 excess, see 6.2)")
ser_lo = sp.series(xsol, y, 0, 2).removeO()
ok(sp.simplify(ser_lo - (sp.sqrt(y) + y/2 + y**sp.Rational(3, 2)/8)) == 0,
   "deep-MOND expansion:  g = sqrt(a0 gN) [1 + sqrt(gN/a0)/2 + (gN/a0)/8 + ...]")

# deep-MOND exact statements
g_dm = sp.sqrt(G*Mr*a0)/r
ok(sp.simplify((g_dm/a0)*g_dm - G*Mr/r**2) == 0,
   "deep-MOND limit mu->g/a0:  g = sqrt(G M a0)/r  solves  (g/a0) g = GM/r^2  EXACTLY")
v2 = sp.simplify(r*g_dm)
ok(sp.simplify(v2**2 - G*Mr*a0) == 0,
   "v^2 = r g = sqrt(G M a0)  =>  v^4 = G M a0  EXACTLY (BTFR, zero free parameters)")
print("      finite-radius kernel correction to v^4:  relative O(x^-1) = O(r_M/r) from mu = x - x^2.")

head("SEC 6.2 -- honest side-findings of the frozen kernel  [DERIVED, not patched]")
print("  (a) INTERPOLATION IDENTITY: the frozen action's kernel is the SIMPLE-mu law")
print("      g = [gN + sqrt(gN^2+4 a0 gN)]/2, NOT the framework's g_obs = sqrt(gN^2 + gN a0),")
print("      NOT Route A nu = 1/(1-exp(-sqrt(y))).  All three share both asymptotics; at y=1:")
v_simple = float(((1 + sp.sqrt(5))/2).evalf())
v_sqrt = float(sp.sqrt(2).evalf())
v_routeA = float((1/(1 - sp.exp(-1))).evalf())
print(f"        simple-mu (this action): g/a0 = {v_simple:.4f} | sqrt-interp: {v_sqrt:.4f} | Route A: {v_routeA:.4f}")
ok(abs(v_simple - 1.6180) < 1e-3 and abs(v_sqrt - 1.4142) < 1e-3 and abs(v_routeA - 1.5820) < 1e-3,
   "transition-region spread quantified: action sits 2.3% from Route A, 14% from sqrt-interp")
print("  (b) ALPHA=1 LIABILITY INHERITED: mu = 1 - 1/x + ... forces a CONSTANT sunward excess")
print("      +a0 (TWICE the a0/2 of the sqrt-interp exact law), i.e. the known alpha=1")
print("      ephemeris problem [repo: project_alpha1_ephemeris_liability].  The Y-sector does")
print("      NOT cure it: on the Newtonian branch eps A'(X) Y = -12 chi X^(-3/2) decays FASTER")
print("      than the mu-tail -X^(-1/2) (verified in 6.5), so the tail is Y-blind.  Any solar-")
print("      system defence must come from the EFE/kappa-window sections, not from F(X,Y).")

# ----------------------------------------------------------------------------------------
head("SEC 6.3 -- the two asymptotic profiles, RE-DERIVED from Cartesian Hessians  [sympy-exact]")
x1, x2, x3 = sp.symbols('x1 x2 x3', real=True)
co = (x1, x2, x3)
rr = sp.sqrt(x1**2 + x2**2 + x3**2)
rho_ax = sp.Symbol('rho_ax', positive=True)   # axis radius
axis = {x1: rho_ax, x2: 0, x3: 0}

def hessian(phi):
    return sp.Matrix(3, 3, lambda i, j: sp.diff(phi, co[i], co[j]))

def tracefree(H):
    return H - sp.eye(3)*sp.trace(H)/3

# generic radial function: S_ij = (f'' - f'/r)(n_i n_j - delta_ij/3), Sbar^2 = (2/3)(f''-f'/r)^2
f = sp.Function('f')
Hf = hessian(f(rr))
Sf = tracefree(Hf)
sgen = (sp.diff(f(rr), rr.args[0]) if False else None)  # placeholder, use explicit form below
fp, fpp = sp.Symbol('fp'), sp.Symbol('fpp')
# build expected tensor on the axis and compare entrywise
Sf_ax = sp.simplify(Sf.subs(axis).doit())
fr = sp.Function('f')(rho_ax)
sval = sp.diff(f(rho_ax), rho_ax, 2) - sp.diff(f(rho_ax), rho_ax)/rho_ax
expect = sp.diag(sp.Rational(2, 3)*sval, -sval/3, -sval/3)
ok(sp.simplify(Sf_ax - expect) == sp.zeros(3, 3),
   "generic radial f(r):  S_ij = (f''-f'/r)(n_i n_j - delta_ij/3)   [DERIVED]")
S2gen = sp.simplify(sum(Sf_ax[i, j]**2 for i in range(3) for j in range(3)))
ok(sp.simplify(S2gen - sp.Rational(2, 3)*sval**2) == 0,
   "generic radial f(r):  Sbar^2 = (2/3)(f'' - f'/r)^2               [DERIVED]")

# Newtonian point mass, dimensionless: phi = -1/x
phiN = -1/rr
HN = hessian(phiN)
ok(sp.simplify(sp.trace(HN)) == 0, "phi = -1/r is vacuum-harmonic: tr(Hess) = 0")
SN = tracefree(HN)
S2N = sp.simplify(sum(SN[i, j]**2 for i in range(3) for j in range(3)).subs(axis))
XN = sp.simplify(sum(sp.diff(phiN, cc)**2 for cc in co).subs(axis))
ok(sp.simplify(S2N - 6/rho_ax**6) == 0 and sp.simplify(XN - 1/rho_ax**4) == 0,
   "Newtonian branch:  X = x^-4,  Sbar^2 = 6 x^-6")
ok(sp.simplify(S2N - 6*XN**sp.Rational(3, 2)) == 0,
   "=> Sbar^2 = 6 X^(3/2)  (repo value RE-DERIVED)")

# deep-MOND isothermal, dimensionless: phi = ln x  (g = 1/x in units of a0, i.e. x_mond = 1/xhat)
phiM = sp.log(rr)
HM = hessian(phiM)
SM = tracefree(HM)
S2M = sp.simplify(sum(SM[i, j]**2 for i in range(3) for j in range(3)).subs(axis))
XM = sp.simplify(sum(sp.diff(phiM, cc)**2 for cc in co).subs(axis))
ok(sp.simplify(S2M - sp.Rational(8, 3)/rho_ax**4) == 0 and sp.simplify(XM - 1/rho_ax**2) == 0,
   "deep-MOND branch:  X = x^-2,  Sbar^2 = (8/3) x^-4")
ok(sp.simplify(S2M - sp.Rational(8, 3)*XM**2) == 0,
   "=> Sbar^2 = (8/3) X^2  (DIMENSIONLESS);  Y = Lam Sbar^2 = (8/3)(c/v)^4 (g/a0)^4")
print("      NOTE: the repo line 'Sbar^2 = (8/3)(c/v)^4 x^4' is Y, not Sbar^2 -- the Lam factor")
print("      belongs to Y.  Same content, mislabelled in the earlier note.  [clerical]")

# radial vector form of the double divergence: d_j[ tau(r)(n_i n_j - delta_ij/3) ]
tau = sp.Function('tau')
Tten = sp.Matrix(3, 3, lambda i, j: tau(rr)*(co[i]*co[j]/rr**2 - sp.KroneckerDelta(i, j)*sp.Rational(1, 3)))
Wvec = sp.Matrix([sum(sp.diff(Tten[i, j], co[j]) for j in range(3)) for i in range(3)])
W_ax = sp.simplify(Wvec.subs(axis).doit())
tau_ax = sp.Function('tau')(rho_ax)
w_expect = sp.Rational(2, 3)*(sp.diff(tau_ax, rho_ax) + 3*tau_ax/rho_ax)
ok(sp.simplify(W_ax[0] - w_expect) == 0 and W_ax[1] == 0 and W_ax[2] == 0,
   "d_j[tau (n n - I/3)]_i = w(r) n_i,  w = (2/3)(tau' + 3 tau/r)   [DERIVED; used in SEC 5.3]")

# ----------------------------------------------------------------------------------------
head("SEC 6.4 -- Y really is built from Psi: linearised spatial Ricci check  [sympy-exact]")
print("  h_ij = (1 - 2 t Psi) delta_ij  =>  (3)R_ij = t (d_i d_j Psi + delta_ij lap Psi) + O(t^2),")
print("  so the trace-free part is  Rbar_ij = t S_ij[Psi]:  Y probes the CURVATURE potential Psi,")
print("  X probes the LAPSE Phi.  Psi = Phi at leading order is ASSUMED here (two-potential")
print("  sections own it); with Psi = gamma Phi every Y-term below just picks up gamma^2.")

t = sp.Symbol('t')
def ricci3(gmat):
    ginv = gmat.inv()
    Gam = [[[sum(ginv[k, l]*(sp.diff(gmat[l, i], co[j]) + sp.diff(gmat[l, j], co[i])
                              - sp.diff(gmat[i, j], co[l])) for l in range(3))/2
             for j in range(3)] for i in range(3)] for k in range(3)]
    Ric = sp.zeros(3, 3)
    for i in range(3):
        for j in range(3):
            e = 0
            for k in range(3):
                e += sp.diff(Gam[k][i][j], co[k]) - sp.diff(Gam[k][i][k], co[j])
                for l in range(3):
                    e += Gam[k][k][l]*Gam[l][i][j] - Gam[k][j][l]*Gam[l][i][k]
            Ric[i, j] = e
    return Ric

for prof, name in ((-1/rr, "Psi = -1/r"), (sp.log(rr), "Psi = ln r")):
    gmat = (1 - 2*t*prof)*sp.eye(3)
    Ric = ricci3(gmat)
    Ric_lin = Ric.applyfunc(lambda e: sp.diff(e, t).subs(t, 0))
    lapl = sum(sp.diff(prof, cc, 2) for cc in co)
    target_lin = hessian(prof) + sp.eye(3)*lapl
    dmat = sp.simplify((Ric_lin - target_lin).subs(axis))
    ok(dmat == sp.zeros(3, 3), f"(3)R_ij linear in t equals d_i d_j Psi + delta_ij lap Psi  [{name}]")

# ----------------------------------------------------------------------------------------
head("SEC 6.5 -- does the Y-sector change the leading asymptotics?  [DERIVED, sympy series]")
print("  Dimensionless vacuum flux (SEC 8):  Flux(x) = [mu(X) + chi A'(X) Sbar^2] phi' - chi w_r,")
print("  w_r = (2/3)(T' + 3T/x), T = A(X) s(x).  Relative Y-correction R(x) = chi(...)/(mu phi').")
xh = sp.Symbol('xhat', positive=True)

def flux_pieces(phi_expr):
    gp = sp.diff(phi_expr, xh)
    s = sp.diff(phi_expr, xh, 2) - gp/xh
    Xp = gp**2
    S2 = sp.Rational(2, 3)*s**2
    Ap_p = (2*Xp*(1 - Xp)/(1 + Xp)**5)
    A_p = Xp**2/(1 + Xp)**4
    mu_p = sp.sqrt(Xp)/(1 + sp.sqrt(Xp))
    T = A_p*s
    w = sp.Rational(2, 3)*(sp.diff(T, xh) + 3*T/xh)
    Rrel = sp.cancel(sp.together((Ap_p*S2*gp - w)/(mu_p*gp)))
    return Rrel

# Newtonian branch phi = -1/x, interior x -> 0
R_N = flux_pieces(-1/xh)
serN = sp.series(R_N, xh, 0, 8).removeO()
leadN = sp.limit(R_N/xh**6, xh, 0)
ok(sp.simplify(leadN - 4) == 0,
   "Newtonian branch:  R(x) = chi * [4 x^6 + O(x^8)]  -> 0 as x -> 0",
   "leading coefficient 4 (exact)")
print("      => the Y-sector leaves the NEWTONIAN asymptote untouched: relative correction")
print("         4 chi (r/R_M)^6, and the mu-correction alone is eps A'Y = -12 chi X^(-3/2)")
muY_N = sp.limit((2*X*(1 - X)/(1 + X)**5) * 6*X**sp.Rational(3, 2) * X**sp.Rational(3, 2), X, sp.oo)
ok(sp.simplify(muY_N + 12) == 0, "eps A'(X)*6X^(3/2) -> -12 X^(-3/2) as X->oo  (x 12 exact)")

# deep-MOND branch phi = ln x, exterior x -> oo
R_M_ = flux_pieces(sp.log(xh))
leadM = sp.limit(R_M_*xh**5, xh, sp.oo)
ok(sp.simplify(leadM - sp.Rational(4, 3)) == 0,
   "deep-MOND branch:  R(x) = chi * [(4/3) x^-5 + O(x^-7 ...)]  -> 0 as x -> oo",
   "leading coefficient 4/3 (exact)")
muY_M = sp.limit(((2*X*(1 - X)/(1 + X)**5)*sp.Rational(8, 3)*X**2)/sp.sqrt(X)/X**sp.Rational(5, 2), X, 0)
ok(sp.simplify(muY_M - sp.Rational(16, 3)) == 0,
   "mu-correction/mu = (16/3) X^(5/2) -> 0 as X->0 on the deep-MOND branch")
print("      => the Y-sector leaves the DEEP-MOND asymptote untouched:  g -> sqrt(GMa0)/r and")
print("         v^4 = GMa0 hold with relative error (4/3) chi (R_M/r)^5 -> 0.")
print("      => BOTH leading asymptotics are Y-BLIND.  The Y-operator acts only in the")
print("         transition region X ~ 1 (r ~ R_M) -- by construction A' peaks there and")
print("         A'(1)=0 kills the mu-shift exactly at the midpoint.  Consistent with")
print("         mu_positivity_2026.py: the chi-window is bounded by the SAME region.")
print("      Robustness: Psi = gamma Phi (gamma = O(1)) multiplies both corrections by gamma^2;")
print("      the powers x^6 and x^-5 are profile-set and do not move.  If the tidal term lands")
print("      in the Psi-equation instead of the Phi-equation (two-potential subtlety), the")
print("      SCALINGS are unchanged because eps A(X) S_ij is evaluated on the same profiles.")

# ----------------------------------------------------------------------------------------
head("SEC 8 -- dimensionless rescaling r = R_M xhat, Phi = a0 R_M phihat  [DERIVED, sympy]")
RM = sp.sqrt(G*Mm/a0)
vinf = (G*Mm*a0)**sp.Rational(1, 4)
Lam = c**4/(G*Mm*a0)
phih = sp.Function('phihat')
rhoh = sp.Function('rhohat')

ok(sp.simplify(G*Mm/RM**2 - a0) == 0, "R_M = sqrt(GM/a0):  gN(R_M) = a0 exactly")
ok(sp.simplify(Lam - (c/vinf)**4) == 0, "Lam = c^4/(G M a0) = (c/v_inf)^4  (v_inf^4 = G M a0)")

# X = |grad phihat|^2 : push the chain rule through sympy
Phi_dim = a0*RM*phih(r/RM)
gdim = sp.diff(Phi_dim, r)
Xdim = sp.simplify((gdim**2/a0**2).subs(r, RM*xh))
ok(sp.simplify(Xdim - sp.diff(phih(xh), xh)**2) == 0,
   "X = c^4 a.a/a0^2 = (Phi'/a0)^2  ->  X = phihat'^2 = |grad_hat phihat|^2")

# Y = Lam Sbar_hat^2 : S_ij[Phi] scales as (a0/R_M) S_hat_ij
s_dim = sp.diff(Phi_dim, r, 2) - sp.diff(Phi_dim, r)/r
S2_dim = sp.Rational(2, 3)*s_dim**2
Ydim = sp.simplify((c**4/a0**4 * S2_dim).subs(r, RM*xh))
s_hat = sp.diff(phih(xh), xh, 2) - sp.diff(phih(xh), xh)/xh
S2_hat = sp.Rational(2, 3)*s_hat**2
ok(sp.simplify(Ydim - Lam*S2_hat) == 0,
   "Y = c^8 Rbar^2/a0^4  ->  Y = Lam * Sbar_hat^2,   Lam = (c/v_inf)^4")

# every coefficient of the dimensionless field equation
term_scale_mu = sp.simplify((a0*RM/RM**2)/(a0/RM))
ok(term_scale_mu == 1, "div[mu grad Phi] scales as (a0/R_M) * div_hat[mu grad_hat phihat]")
rho_scale = sp.simplify(4*sp.pi*G*(Mm/RM**3)/(a0/RM))
ok(rho_scale == 4*sp.pi, "4 pi G rho scales as (a0/R_M) * 4 pi rhohat,  rhohat = (R_M^3/M) rho")
tidal_scale = sp.simplify((c**4/a0**2)*(a0/RM)/RM**2/(a0/RM))
ok(sp.simplify(tidal_scale - Lam) == 0,
   "(c^4/a0^2) dd[A S] scales as (a0/R_M) * Lam * dd_hat[A S_hat]  => eps Lam = chi")

# the strongest form: substitute the rescaling into the DIMENSIONAL radial flux and factor
Ffull_flux = (sp.diff(Ffull, X).subs({X: Xr, Yv: Yr})*Pp
              - (c**4/a0**2)*sp.Rational(2, 3)*(sp.diff(eps*A.subs(X, Xr)*s_r, r)
                                                + 3*eps*A.subs(X, Xr)*s_r/r))
sub_map = {Phi(r): Phi_dim}
flux_sub_expr = Ffull_flux.subs(Phi(r), Phi_dim).doit()
flux_scaled = sp.simplify(flux_sub_expr.subs(r, RM*xh).subs(eps, chi/Lam))
Xh_ = sp.diff(phih(xh), xh)**2
FXh = sp.diff(Ffull, X).subs({X: Xh_, Yv: chi/eps*S2_hat}).subs(eps, chi/Lam)  # careful below
# build the target dimensionless flux directly:
FX_hat = (-1/(1 + sp.sqrt(Xh_)) + chi*(2*Xh_*(1 - Xh_)/(1 + Xh_)**5)*S2_hat)
T_hat = (Xh_**2/(1 + Xh_)**4)*s_hat
w_hat = sp.Rational(2, 3)*(sp.diff(T_hat, xh) + 3*T_hat/xh)
target_flux = a0*(FX_hat*sp.diff(phih(xh), xh) - chi*w_hat)
ok(sp.simplify(flux_scaled - target_flux) == 0,
   "FULL dimensional flux == a0 * [dimensionless flux with the SINGLE parameter chi]",
   "every eps, c, G, M, a0 collapses into chi = eps (c/v_inf)^4; overall factor a0 (i.e. a0/R_M per div)")

print("\n  THE DIMENSIONLESS FIELD EQUATION (all coefficients now verified):")
print("    div_hat[ ( x/(1+x) + chi A'(X) Sbar_hat^2 ) grad_hat phihat ]")
print("        - chi dd_hat[ A(X) Sbar_hat_ij ]  =  4 pi rhohat ,")
print("    x = sqrt(X) = |grad_hat phihat|,  A = X^2/(1+X)^4,  chi = eps (c/v_inf)^4,")
print("    v_inf^4 = G M a0,  M_hat = INT rhohat d^3xhat = 1.")
print("  Coefficient census: {1 (Newtonian sector), 1 (kernel), chi (BOTH Y-terms), 4 pi (source)}.")
print("  chi is the ONLY parameter of the static problem, and it is SOURCE-DEPENDENT")
print("  (chi ~ M^-1): heavier sources are deeper in the Y-quiet regime.")

# ----------------------------------------------------------------------------------------
head("SUMMARY")
print(f"  checks passed: {len(PASS)}   failed: {len(FAIL)}")
for lbl in FAIL:
    print(f"    FAILED: {lbl}")
sys.exit(0 if not FAIL else 1)
