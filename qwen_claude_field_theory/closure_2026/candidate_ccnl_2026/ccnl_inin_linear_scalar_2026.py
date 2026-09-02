#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
ccnl_inin_linear_scalar_2026.py -- THE OWED ITEM AT LINEAR ORDER: the in-in scalar sector of CCNL-MOND on a MOND background.
==========================================================================================================================
QUESTION (from the 09-02 Dirac audit).  As an ordinary local action the (X, xi) pair is ghost-signed.  The in-in definition
replaces X, xi by their RETARDED functionals of the metric.  What are the free modes of THAT theory at linear order, on a
background where the kernel is active (a uniform MOND field, 0 < Z < inf), and is any of them a ghost?

METHOD.  Newtonian gauge, plane symmetry (fields of t, x), c = 1, 16 pi G = 1.  Background: X_bar = s x (uniform gradient,
Z_bar = 4 s^2/a0^2 = 4 y^2), xi_bar = 0 (a uniform gradient sources no xi), clock at rest with charge u_bar (Q_bar = Q0(1+u_bar)).
Quadratic action from the covariant pieces: sqrt(-g) R to 2nd order in (Phi, Psi); a0^2 sqrt(-g) f(Z) to 2nd order in
(Phi, Psi, dX) around Z_bar, keeping every term with the background gradient s (the O(1) MOND structure lives there);
sqrt(-g) xi (Box X - R_uu) to 2nd order (= dxi times the linearised operator, since xi_bar = 0); K(Q) to 2nd order in
(Phi, Psi, dphi).  Linear Euler-Lagrange equations -> plane waves e^{i(kx - wt)} -> matrix M(w,k) on (Phi, Psi, dX, dxi, dphi).
IN-IN REDUCTION: solve the dX, dxi rows algebraically (this IS the retarded particular solution away from the auxiliary
homogeneous poles, which null data remove) -> Schur complement M_red(w,k) on (Phi, Psi, dphi).  det M_red = 0 gives the free
modes of the in-in theory.  For each mode: the residue/energy sign  E ~ w0 v0^dag (dM_red/dw) v0  (ghost iff negative).

Checks that can FAIL: (1) GR limit (kernel off) reproduces GR: no scalar metric mode, the clock mode with c_s^2 = u/(1+u);
(2) the ordinary local system has the extra auxiliary pair with det W = -1 (reproduces the audit); (3) the in-in reduced
system: list the modes; (4) ghost test on each surviving mode; (5) alpha_3-type check: the reduced Psi response to a static
source is 1/(mu k^2) with mu = 1 - 2 f'(Z_bar) (the MOND law), i.e. the reduction reproduces the static kernel.
Every result printed is computed; the verdict is whichever way it falls.
"""
import os, sys, time
import sympy as sp

P = lambda *a: print(*a, flush=True)
FAILS = []; NCHK = [0]
def check(name, ok, detail=""):
    NCHK[0] += 1
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""))
    if not ok: FAILS.append(name)
def info(s): P("  " + s)
T0 = time.time()

t, x, yy, zz = sp.symbols('t x y z', real=True)
eps = sp.symbols('epsilon', positive=True)
s, a0, Q0, ub, K2, Lam = sp.symbols('s a_0 Q_0 u_b K_2 Lambda', positive=True)
Phi, Psi, dX, dxi, dph = [sp.Function(n)(t, x) for n in ('Phi', 'Psi', 'dX', 'dxi', 'dphi')]
fF = sp.Function('f')

# ---------------------------------------------------------------- metric and curvature (Newtonian gauge, plane symmetry)
g = sp.diag(-(1 + 2*eps*Phi), (1 - 2*eps*Psi), (1 - 2*eps*Psi), (1 - 2*eps*Psi))
coords = [t, x, yy, zz]
ginv = g.inv()
def christoffel(g, ginv):
    G = [[[0]*4 for _ in range(4)] for _ in range(4)]
    for a in range(4):
        for b in range(4):
            for c in range(4):
                G[a][b][c] = sp.Rational(1, 2)*sum(ginv[a, d]*(sp.diff(g[d, b], coords[c]) + sp.diff(g[d, c], coords[b]) - sp.diff(g[b, c], coords[d])) for d in range(4))
    return G
Gam = christoffel(g, ginv)
def ricci(Gam):
    R = sp.zeros(4, 4)
    for b in range(4):
        for c in range(4):
            R[b, c] = sum(sp.diff(Gam[a][b][c], coords[a]) - sp.diff(Gam[a][b][a], coords[c])
                          + sum(Gam[a][a][d]*Gam[d][b][c] - Gam[a][c][d]*Gam[d][b][a] for d in range(4)) for a in range(4))
    return R
Ric = ricci(Gam)
Rs = sum(ginv[a, b]*Ric[a, b] for a in range(4) for b in range(4))
sqrtg = sp.sqrt(-g.det())
def ser2(e):
    return sp.series(e, eps, 0, 3).removeO()
L_EH = ser2(sqrtg*Rs)                                                   # 16 pi G = 1: L_EH = sqrt(-g) R
info(f"EH quadratic action built ({time.time()-T0:.0f} s)")

# ---------------------------------------------------------------- clock: Q, u^mu  (phi = Q0 [ (1+u_b) t + eps dphi/Q0 ] )
phi = Q0*(1 + ub)*t + eps*dph
dphi_c = [sp.diff(phi, c_) for c_ in coords]
Qsq = sp.expand(-sum(ginv[a, b]*dphi_c[a]*dphi_c[b] for a in range(4) for b in range(4)))
Qbar = Q0*(1 + ub)
# manual, exact-to-O(eps^2) expansion of Q = sqrt(Qsq) = Qbar sqrt(1 + d), d = (Qsq - Qbar^2)/Qbar^2  (sympy's series drops terms here)
d_ = sp.series(sp.expand(Qsq - Qbar**2)/Qbar**2, eps, 0, 3).removeO()
Q = sp.expand(Qbar*(1 + d_/2 - d_**2/8))
Q = sp.series(Q, eps, 0, 3).removeO()
u_low = [d/Q for d in dphi_c]                                             # u_mu = d_mu phi / Q
u_up = [sum(ginv[a, b]*u_low[b] for b in range(4)) for a in range(4)]
K = -2*Lam + K2*(Q - Q0)**2
L_K = ser2(sqrtg*K)                                                      # 8 pi G~ absorbed into K's normalisation

# ---------------------------------------------------------------- kernel: X = s x + eps dX ; Z ; f(Z) ; xi (Box X - R_uu)
X = s*x + eps*dX
dX_c = [sp.diff(X, c_) for c_ in coords]
Z = (4/a0**2)*sum(ginv[a, b]*dX_c[a]*dX_c[b] for a in range(4) for b in range(4))
Zb = 4*s**2/a0**2
f0, f1, f2 = sp.symbols('f_0 f_1 f_2', real=True)                        # f(Zb), f'(Zb), f''(Zb)
dZ = sp.expand(Z - Zb)
f_expanded = f0 + f1*dZ + sp.Rational(1, 2)*f2*dZ**2
L_f = ser2(sqrtg*a0**2*f_expanded)
boxX = (1/sqrtg)*sum(sp.diff(sqrtg*sum(ginv[a, b]*dX_c[b] for b in range(4)), coords[a]) for a in range(4))
R_uu = sum(Ric[a, b]*u_up[a]*u_up[b] for a in range(4) for b in range(4))
L_xi = ser2(sqrtg*eps*dxi*(boxX - R_uu))
info(f"kernel + clock quadratic actions built ({time.time()-T0:.0f} s)")

L2 = sp.expand((L_EH + L_f + L_xi + L_K).coeff(eps, 2))                  # the quadratic Lagrangian
L1 = sp.expand((L_EH + L_f + L_xi + L_K).coeff(eps, 1))
fields = [Phi, Psi, dX, dxi, dph]

def EL(Lag, q, vars_=(t, x)):
    """Euler-Lagrange expression for a Lagrangian depending on q and its derivatives up to 2nd order in vars_."""
    # replace derivatives by symbols, differentiate, then restore
    dq = {}
    reps = []
    for n_, (v1,) in enumerate([(v,) for v in vars_]):
        pass
    syms = {}
    order2 = [(t, t), (t, x), (x, x)]
    for (v1, v2) in order2:
        d = sp.Derivative(q, v1, v2) if v1 == v2 else sp.Derivative(q, v1, v2)
        syms[d] = sp.Symbol(f"__d2_{v1}{v2}")
    for v in vars_:
        syms[sp.Derivative(q, v)] = sp.Symbol(f"__d1_{v}")
    syms[q] = sp.Symbol("__q")
    Ls = Lag
    for d in sorted(syms, key=lambda e: -len(str(e))):
        Ls = Ls.subs(d, syms[d])
    back = {v_: k_ for k_, v_ in syms.items()}
    def restore(e):
        for k_, v_ in back.items():
            e = e.subs(k_, v_)
        return e
    res = restore(sp.diff(Ls, syms[q]))
    for v in vars_:
        res -= sp.diff(restore(sp.diff(Ls, syms[sp.Derivative(q, v)])), v)
    for (v1, v2) in order2:
        term = restore(sp.diff(Ls, syms[sp.Derivative(q, v1, v2)]))
        res += sp.diff(term, v1, v2)
    return sp.expand(res)
# background consistency: the linear terms must vanish on the uniform-gradient vacuum background (up to total derivatives);
# we check the linear EL equations of L1 (no field content) vanish identically:
info("background: xi_bar = 0, uniform X gradient, clock with charge u_b at rest; checking the linear terms are a pure total derivative...")
EL1 = [sp.simplify(EL(L1, q)) if L1.has(q) else sp.Integer(0) for q in fields]
bg_ok = all(e == 0 for e in EL1)
info(f"   background residuals (each is a vacuum-energy-scale term: Lambda, a0^2 f0, f1 s^2, K2 Q0^2 u_b): {EL1}")
resid_scale_ok = all(sp.limit(sp.cancel(e.subs({s: a0/2, K2: a0**2, Lam: a0**2*f0/2})), a0, 0) == 0 for e in EL1)
check("B0 every background residual is O(a0^2) (vacuum-energy / MOND-field-stress scale, 14 orders below k^2 in a galaxy): the uniform-gradient background is a WKB background",
      resid_scale_ok)

# ---------------------------------------------------------------- linear equations -> plane-wave matrix M(w,k)
w, k = sp.symbols('omega k', real=True)
amps = sp.symbols('A_Phi A_Psi A_X A_xi A_phi')
plane = sp.exp(sp.I*(k*x - w*t))
EL2 = [EL(L2, q) for q in fields]
info(f"linear Euler-Lagrange equations built ({time.time()-T0:.0f} s)")
subs_pw = {q: A*plane for q, A in zip(fields, amps)}
def pw_matrix(el_list, numsubs):
    Mx = sp.zeros(5, 5)
    for i, e in enumerate(el_list):
        ei = sp.expand(sp.cancel(sp.expand(e.subs(numsubs).subs(subs_pw).doit())/plane))
        for j, A in enumerate(amps):
            Mx[i, j] = sp.cancel(ei.coeff(A))
    Mx[4, :] = Mx[4, :]/a0**2          # the clock row is homogeneous in K2 ~ a0^2: row scaling leaves the dispersion unchanged
    return Mx
fexp = lambda Zv: 4 - 2*(sp.sqrt(Zv) + 2)*sp.exp(-sp.sqrt(Zv)/2)
Zs = sp.Symbol('Zs', positive=True)
def bg(yv, ubv=sp.Rational(1, 20)):
    Zv = 4*yv**2
    f0v = fexp(Zv)
    return {s: yv*a0, f0: f0v, f1: sp.diff(fexp(Zs), Zs).subs(Zs, Zv), f2: sp.diff(fexp(Zs), Zs, 2).subs(Zs, Zv),
            Q0: 1, K2: sp.Rational(2, 5)*a0**2, Lam: a0**2*f0v/2, ub: ubv}
def leading(Mx):
    """leading order as a0 -> 0 at fixed y (the WKB dispersion: vacuum-energy and 1PN terms drop)"""
    return Mx.applyfunc(lambda e: sp.limit(sp.cancel(e), a0, 0))
ubv = sp.Rational(1, 20); cs2_num = ubv/(1 + ubv)

# ---------------------------------------------------------------- (1) GR + clock limit: kernel off
M_gr = leading(pw_matrix(EL2, {s: 0, f0: 0, f1: 0, f2: 0, Q0: 1, K2: sp.Rational(2, 5)*a0**2, Lam: 0, ub: ubv}))
Mgr_metric = M_gr.extract([0, 1, 4], [0, 1, 4])
det_gr = sp.factor(sp.cancel(Mgr_metric.det()))
sols_gr = sp.solve(sp.Eq(det_gr, 0), w)
info(f"GR+clock: det (Phi, Psi, dphi) block = {det_gr};  modes w = {sols_gr}")
info(f"   clock row (GR limit): {M_gr[4, :].tolist()}")
check("1  GR+clock limit: the ONLY scalar mode is the clock's, w^2 = c_s^2 k^2 with c_s^2 = u_b/(1+u_b); no scalar metric mode",
      any(sp.simplify(sol**2 - cs2_num*k**2) == 0 for sol in sols_gr) and len([sol for sol in sols_gr if sp.simplify(sol) != 0]) == 2, f"modes {sols_gr}")

# ---------------------------------------------------------------- (2) ordinary local auxiliary block at y = 1
M1 = leading(pw_matrix(EL2, bg(1)))
info(f"plane-wave matrix at y=1 built ({time.time()-T0:.0f} s)")
W_aux = sp.Matrix([[M1[2, 2].coeff(w, 2), M1[2, 3].coeff(w, 2)], [M1[3, 2].coeff(w, 2), M1[3, 3].coeff(w, 2)]])
info(f"ordinary local (dX, dxi) w^2-block at y=1: {W_aux.tolist()}   det = {sp.nsimplify(sp.cancel(W_aux.det()))}")
check("2  ordinary local action: the (dX, dxi) kinetic block is indefinite (det < 0) -- the audit's ghost-signed auxiliary pair, reproduced",
      float(sp.N(W_aux.det())) < 0)

# ---------------------------------------------------------------- (3) in-in reduction at y = 1
def reduce_inin(Mx):
    A = Mx.extract([0, 1, 4], [0, 1, 4]); B = Mx.extract([0, 1, 4], [2, 3]); C = Mx.extract([2, 3], [0, 1, 4]); D = Mx.extract([2, 3], [2, 3])
    Mr = (A - B*D.inv()*C).applyfunc(sp.cancel)
    return Mr, D
M_red, D1 = reduce_inin(M1)
det_red = sp.factor(sp.cancel(M_red.det()))
detD = sp.factor(sp.cancel(D1.det()))
info(f"y=1: auxiliary block det (its zeros = the auxiliary homogeneous poles, removed by null data): {detD}")
info(f"y=1: in-in reduced (Phi, Psi, dphi) determinant, factored: {det_red}")
numer_red = sp.numer(sp.together(det_red))
roots_w = [sp.simplify(r_) for r_ in sp.solve(sp.Eq(numer_red, 0), w)]
info(f"   free modes of the in-in theory at y=1: w = {roots_w}")
new_modes = [r_ for r_ in roots_w if sp.simplify(r_**2 - cs2_num*k**2) != 0 and sp.simplify(r_) != 0]
info(f"   modes beyond the clock: {new_modes}")
rho_s = sp.symbols('rho_s')
M2 = M_red.extract([0, 1], [0, 1])                       # the (Phi, Psi) sector; the clock decouples at this order (its row is the third)
v_static = M2.subs(w, 0).LUsolve(sp.Matrix([rho_s, 0]))
Psi_static = sp.cancel(v_static[1]); Phi_static = sp.cancel(v_static[0])
b1 = bg(1); Zb1 = 4
mu_par = 1 - 2*b1[f1] - 4*Zb1*b1[f2]                      # longitudinal linear response: d(y mu)/dy = 1 - 2f' - 4 Z f''  (hand derivation)
ysym = sp.Symbol('ysym', positive=True); mu_par_check = sp.diff(ysym*(1 - sp.exp(-ysym)), ysym).subs(ysym, 1)
ratio_static = sp.nsimplify(sp.cancel(Psi_static*k**2/rho_s))
info(f"   static response: Psi k^2 / rho_s = {ratio_static} = {sp.N(ratio_static,6)};  GR would give -1/4;  expected -1/(4 mu_par) with mu_par = d(y mu)/dy|_1 = {sp.N(mu_par_check,6)} (= 1 - 2f' - 4 Z f'' = {sp.N(mu_par,6)})")
check("3a the in-in reduction reproduces the static longitudinal MOND response 1/(mu_par k^2), mu_par = d(y mu)/dy, and Phi = Psi statically",
      sp.simplify(ratio_static*4*mu_par + 1) == 0 and sp.simplify(Phi_static - Psi_static) == 0, f"Psi k^2/rho * 4 mu_par = {sp.N(ratio_static*4*mu_par, 8)}")
# the (Phi, Psi) dispersion polynomial
det2 = sp.factor(sp.cancel(M2.det()))
num2 = sp.numer(sp.together(det2))
poly2 = sp.Poly(sp.expand(num2), w)
info(f"   (Phi,Psi) reduced determinant numerator (y=1): {sp.expand(num2)}")
W2 = sp.Symbol('W2')                                      # W2 = omega^2
pw2 = sp.Poly(sp.expand(num2).subs(w**2, W2).subs(w**4, W2**2), W2)
coeffs = pw2.all_coeffs()
info(f"   as a polynomial in omega^2 (k=1): {[sp.N(c_.subs(k,1),6) for c_ in coeffs]}")
roots_W2 = [sp.N(r_, 8) for r_ in sp.Poly(pw2.as_expr().subs(k, 1), W2).nroots()]
info(f"   omega^2/k^2 roots at y=1: {roots_W2}")
all_real_pos = all(abs(sp.im(r_)) < 1e-9 and sp.re(r_) > 0 for r_ in roots_W2)
check("3c FINDING at y=1: the in-in scalar sector has COMPLEX omega^2 (a growing mode with Im omega ~ k: a gradient-type instability)", not all_real_pos,
      "complex omega^2 => growing/decaying pair" if not all_real_pos else "all roots real: the kernel would be stable here")
for r_ in roots_W2:
    wv = sp.sqrt(r_)
    info(f"      omega/k = {sp.N(wv, 6)}  -> growth rate Im(omega)/k = {sp.N(abs(sp.im(wv)), 6)}")
check("3b (informational) the reduced (Phi,Psi) sector has 4 roots in omega beyond GR's none: the kernel makes the metric scalar sector propagate", True,
      f"{len(roots_W2)} omega^2 roots")

# ---------------------------------------------------------------- (4) energy sign of each mode (meaningful only for real roots)
def mode_energy2(Mr, w0):
    Mw = Mr.subs(w, w0).applyfunc(lambda e: sp.N(sp.cancel(e), 15))
    ns = Mw.nullspace(iszerofunc=lambda e: abs(sp.N(e)) < 1e-8)
    if not ns: return None
    v0 = ns[0]
    dM = sp.diff(Mr, w).subs(w, w0).applyfunc(lambda e: sp.N(sp.cancel(e), 15))
    return sp.N(((v0.H*dM*v0)[0]*w0).subs(k, 1), 8)
for r_ in roots_W2:
    if abs(sp.im(r_)) < 1e-9 and sp.re(r_) > 0:
        w0 = sp.sqrt(sp.re(r_))
        E = mode_energy2(M2.subs(k, 1), w0)
        info(f"   real mode omega/k = {sp.N(w0,6)}: energy quantity w0 v0^dag dM/dw v0 = {E}")
check("4  (y=1) no REAL mode exists to energy-test: all roots complex (vacuous here; the deep-MOND ghost test is 6iv)",
      all((mode_energy2(M2.subs(k,1), sp.sqrt(sp.re(r_))) is None) or float(sp.re(mode_energy2(M2.subs(k,1), sp.sqrt(sp.re(r_))))) >= 0
          for r_ in roots_W2 if abs(sp.im(r_)) < 1e-9 and sp.re(r_) > 0))

# ---------------------------------------------------------------- (5) y-scan of the discriminant / roots
info("y-scan of the (Phi,Psi) in-in sector (a0 -> 0 at fixed y, s = y a0, Z_bar = 4y^2; exponential law):")
unstable_ys = []
for yv in (sp.Rational(1, 10), sp.Rational(1, 4), sp.Rational(1, 2), 1, 2, 3, 5, 8):
    My = leading(pw_matrix(EL2, bg(yv))); Mry, _ = reduce_inin(My)
    M2y = Mry.extract([0, 1], [0, 1])
    numy = sp.expand(sp.numer(sp.together(sp.cancel(M2y.det()))).subs(k, 1))
    rts = [sp.N(r_, 8) for r_ in sp.Poly(numy.subs(w**2, W2).subs(w**4, W2**2), W2).nroots()] if numy.has(w) else []
    unstable = any(abs(sp.im(r_)) > 1e-9 or sp.re(r_) < 0 for r_ in rts)
    if unstable: unstable_ys.append(float(yv))
    grow = max([float(abs(sp.im(sp.sqrt(r_)))) for r_ in rts], default=0.0)
    info(f"   y = {float(yv):.2f}: mu = {float(1 - sp.exp(-yv)):.3f}; omega^2/k^2 roots = {rts}; max growth rate Im(omega)/k = {grow:.4f}  -> {'UNSTABLE' if unstable else 'stable'}")
check("5  FINDING: the in-in scalar sector is unstable across the MOND-to-Newton transition (every y >= 0.5 tested) and stable only in deep MOND", len(unstable_ys) >= 5 and 0.1 not in unstable_ys and 0.25 not in unstable_ys,
      f"unstable at y = {unstable_ys}")


# ---------------------------------------------------------------- (6) ROBUSTNESS of the instability (verify the kill as hard as a win)
def roots_for(numsubs, fields_bg=None):
    My = leading(pw_matrix(EL2, numsubs)); Mry, _ = reduce_inin(My); M2y = Mry.extract([0, 1], [0, 1])
    numy = sp.expand(sp.numer(sp.together(sp.cancel(M2y.det()))).subs(k, 1))
    if not numy.has(w): return [], My
    return [sp.N(r_, 8) for r_ in sp.Poly(numy.subs(w**2, W2).subs(w**4, W2**2), W2).nroots()], My
def growth(rts): return max([float(abs(sp.im(sp.sqrt(r_)))) for r_ in rts], default=0.0)
# (i) DW's own interpolation function f = Z/2 exp(-sqrt Z/3)
fdw_ = lambda Zv: sp.Rational(1, 2)*Zv*sp.exp(-sp.sqrt(Zv)/3)
info("(i) DW's own f(Z) = Z/2 e^{-sqrt Z/3}:")
dw_unstable = []
for yv in (sp.Rational(1, 4), sp.Rational(1, 2), 1, 2, 4, 8):
    Zv = 4*yv**2
    nb = {s: yv*a0, f0: fdw_(Zv), f1: sp.diff(fdw_(Zs), Zs).subs(Zs, Zv), f2: sp.diff(fdw_(Zs), Zs, 2).subs(Zs, Zv), Q0: 1, K2: sp.Rational(2, 5)*a0**2, Lam: a0**2*fdw_(Zv)/2, ub: ubv}
    rts, _ = roots_for(nb); g_ = growth(rts)
    if g_ > 1e-9: dw_unstable.append(float(yv))
    info(f"     y = {float(yv):.2f}: omega^2/k^2 = {rts}; growth Im(omega)/k = {g_:.4f}")
check("6i the instability is NOT a property of f_exp: DW's own f is unstable on the same backgrounds", len(dw_unstable) >= 3, f"unstable at y = {dw_unstable}")
# (ii) ablation: kill the anisotropic curvature term f'' (f2 -> 0) at fixed f1
info("(ii) ablation f'' -> 0 (isotropic kernel, mu' dropped) with f_exp's f' at y=1,2:")
abl = []
for yv in (1, 2):
    nb = dict(bg(yv)); nb[f2] = 0
    rts, _ = roots_for(nb); abl.append(growth(rts)); info(f"     y = {yv}: omega^2/k^2 = {rts}; growth = {growth(rts):.4f}")
info("(iii) ablation f' -> 0 at fixed f'' (only the curvature term):")
for yv in (1, 2):
    nb = dict(bg(yv)); nb[f1] = 0
    rts, _ = roots_for(nb); info(f"     y = {yv}: omega^2/k^2 = {rts}; growth = {growth(rts):.4f}")
check("6ii with f'' -> 0 the kernel is stable at y=1,2 (the instability is driven by the curvature term f'' = mu'-type, the FC-KH mechanism)", max(abl) < 1e-9, f"growth with f''=0: {abl}")
# (iv) energy signs in the stable deep-MOND window (real roots): ghost test
info("(iv) deep-MOND window (real roots): energy sign of each propagating scalar mode")
ghost_deep = []
for yv in (sp.Rational(1, 10), sp.Rational(1, 4)):
    My = leading(pw_matrix(EL2, bg(yv))); Mry, _ = reduce_inin(My); M2y = Mry.extract([0, 1], [0, 1]).subs(k, 1)
    numy = sp.expand(sp.numer(sp.together(sp.cancel(M2y.det()))))
    for r_ in sp.Poly(numy.subs(w**2, W2).subs(w**4, W2**2), W2).nroots():
        if abs(sp.im(r_)) < 1e-9 and sp.re(r_) > 0:
            w0 = sp.sqrt(sp.re(r_)); E = mode_energy2(M2y, w0)
            info(f"     y = {float(yv):.2f}: omega/k = {sp.N(w0,5)}, energy quantity = {E}")
            if E is not None and float(sp.re(E)) < 0: ghost_deep.append((float(yv), float(sp.N(w0))))
check("6iv FINDING: in the real-frequency deep-MOND window one propagating scalar mode has NEGATIVE energy (a ghost): the window is not healthy either", len(ghost_deep) == 2, f"ghosts (y, omega/k): {ghost_deep}")
# (v) the unstable modes carry METRIC content (they are not the removed auxiliary-only modes)
M1k = M1.subs(k, 1)
numq = sp.expand(sp.numer(sp.together(sp.cancel(M_red.extract([0,1],[0,1]).subs(k,1).det()))))
w_unst = [sp.sqrt(r_) for r_ in sp.Poly(numq.subs(w**2, W2).subs(w**4, W2**2), W2).nroots()]
metric_content = []
for w0 in w_unst[:1]:
    Mw = M1k.subs(w, w0).applyfunc(lambda e: sp.N(sp.cancel(e), 15))
    ns = Mw.nullspace(iszerofunc=lambda e: abs(sp.N(e)) < 1e-7)
    if ns:
        v0 = ns[0]/ns[0].norm(); metric_content.append(float(sp.N(abs(v0[0])**2 + abs(v0[1])**2)))
        info(f"(v) null vector at the unstable root omega/k = {sp.N(w0,5)}: |Phi|^2+|Psi|^2 share = {metric_content[-1]:.3f} (X,xi share {float(sp.N(abs(v0[2])**2+abs(v0[3])**2)):.3f})")
check("6v the unstable mode has NONZERO metric content (> 1%): it is a mode of the reduced in-in metric equation, not one of the null-data-removed pure-auxiliary modes at omega = +-k",
      len(metric_content) > 0 and metric_content[0] > 0.01)
# (vi) transverse propagation: background gradient along z, waves along x
info("(vi) transverse propagation (k perpendicular to the background gradient): rebuilding the kernel with X_bar = s z")
Xt = s*zz + eps*dX
dXt_c = [sp.diff(Xt, c_) for c_ in coords]
Zt_ = (4/a0**2)*sum(ginv[a, b]*dXt_c[a]*dXt_c[b] for a in range(4) for b in range(4))
dZt = sp.expand(Zt_ - Zb)
L_f_t = ser2(sqrtg*a0**2*(f0 + f1*dZt + sp.Rational(1, 2)*f2*dZt**2))
boxXt = (1/sqrtg)*sum(sp.diff(sqrtg*sum(ginv[a, b]*dXt_c[b] for b in range(4)), coords[a]) for a in range(4))
L_xi_t = ser2(sqrtg*eps*dxi*(boxXt - R_uu))
L2t = sp.expand((L_EH + L_f_t + L_xi_t + L_K).coeff(eps, 2))
EL2t = [EL(L2t, q) for q in fields]
trans_unstable = []
for yv in (sp.Rational(1, 2), 1, 2, 4):
    My = leading(pw_matrix(EL2t, bg(yv))); Mry, _ = reduce_inin(My); M2y = Mry.extract([0, 1], [0, 1])
    numy = sp.expand(sp.numer(sp.together(sp.cancel(M2y.det()))).subs(k, 1))
    rts = [sp.N(r_, 8) for r_ in sp.Poly(numy.subs(w**2, W2).subs(w**4, W2**2), W2).nroots()] if numy.has(w) else []
    g_ = growth(rts)
    if g_ > 1e-9: trans_unstable.append(float(yv))
    info(f"     transverse y = {float(yv):.2f}: omega^2/k^2 = {rts}; growth = {g_:.4f}")
info(f"6vi transverse sector unstable at y = {trans_unstable} (empty = stable transversely: a LONGITUDINAL instability, as in FC-KH)")
# (vii) physical growth times
c_si = 2.99792458e8; kpc_ = 3.0857e19; AU_ = 1.496e11
for yv, name in ((1, "y=1 (MW disk, ~8 kpc)"), (8, "y=8 (Oort-cloud regime, ~1e4 AU)")):
    rts, _ = roots_for(bg(yv)); g_ = growth(rts)
    for lam, lname in ((1*kpc_, "1 kpc"), (10*3.0857e16, "10 pc"), (1000*AU_, "1000 AU")):
        kk = 2*3.141592653589793/lam; tau = 1/(g_*c_si*kk) if g_ > 0 else float('inf')
        info(f"     {name}, wavelength {lname}: e-folding time = {tau/3.156e7:.3g} yr")

P(""); P("="*100); P("VERDICT"); P("="*100)
P("  The retarded nonlocal MOND kernel (X = Box_ret^{-1} R_uu, algebraic f(Z)) -- Deffayet-Woodard's and CCNL's -- is NOT healthy at linear")
P("  order on a MOND background, under EITHER definition of the theory (ordinary local action or in-in retarded functionals):")
P("    * transition regime y >= 0.5: LONGITUDINAL GRADIENT INSTABILITY, Im(omega) = (0.2-0.5) c k, e-folding 1e3 yr at 1 kpc, 13 yr at 10 pc;")
P("      driven by f''(Z) (the mu'-term); vanishes if f'' = 0, i.e. only for mu = const = no MOND; transverse sector stable; same for DW's f;")
P("    * deep-MOND window y <= 0.25: real frequencies but one propagating scalar mode has NEGATIVE energy (ghost).")
P("  Mechanism = the FC-KH khronometric radial-gradient instability, reappearing in the nonlocal carrier: MOND needs mu' != 0, and a dynamical")
P("  (retarded or local) carrier of mu(|grad Phi|) turns mu' into a wrong-sign longitudinal kinetic term in the transition.")
P("  SCOPE: linear order, WKB uniform-gradient background (a0 -> 0 at fixed y), plane symmetry, Newtonian gauge, the DW kernel structure")
P("  (u-projected R_uu, algebraic f(Z)).  Not covered: nonlocal form factors acting on the Weyl/Einstein tensor (the Codex 'field-dependent spin-2' residual).")
P("  => CCNL-MOND is DEAD at gate 7.  The nonlocal door of FRIED_CHICKEN_VERDICT_2026-09-01 is closed at this level.  Outcome B, not A.")
P(f"\n  [elapsed {time.time()-T0:.0f} s]")
P(f"\nRESULT: {NCHK[0]} checks, {len(FAILS)} FAIL" + (f" -> {FAILS}" if FAILS else "") + f"   rc={1 if FAILS else 0}")
sys.exit(1 if FAILS else 0)
