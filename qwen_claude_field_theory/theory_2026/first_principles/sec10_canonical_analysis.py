#!/usr/bin/env python3
"""
Section 10: canonical (ADM) analysis of the FROZEN action, unitary gauge T = t.

    S = (M_Pl^2 c^3/2) INT d^4x N sqrt(h) [ (3)R + K_ij K^ij - lam_K K^2 + eta_K a_i a^i
        - (2 a0^2/c^4) F(X,Y) ] + S_m
    F(X,Y) = -2 sqrt(X) + 2 ln(1+sqrt(X)) + eps [X^2/(1+X)^4] Y
    X = c^4 a_i a^i / a0^2  (a_i = D_i ln N in unitary gauge; no time derivatives)
    Y = c^8 Rbar_ij Rbar^ij / a0^4  (trace-free SPATIAL Ricci; no time derivatives)

Units in the symbolic work: c = a0 = 1, so lengths are in units of ell = c^2/a0 and
the overall positive prefactor (M_Pl^2 c^3/2) is dropped (it cannot change any sign).

CHECKS (all derivations, no imports of stability results):
  1  F(X) is C^1 at X=0 but NON-ANALYTIC at order X^(3/2):
       F = -X + (2/3) X^(3/2) - X^2/2 + (2/5) X^(5/2) + ...,  F_X = -1/(1+sqrt X),
       F_XX = 1/(2 sqrt X (1+sqrt X)^2) -> +infinity as X -> 0.
     => the QUADRATIC action around Minkowski exists (leading term -X is analytic,
        the sqrt(X) pieces cancel between -2 sqrt X and 2 ln(1+sqrt X)), and the
        F-sector acts at X=0 exactly like a khronometric a_i a^i term with
        alpha_eff = eta_K + 2; the breakdown is at CUBIC order (|delta a|^3).
  2  Hessian of the a-sector at background X0 = s^2 > 0:
       (1/2) d^2/da_i da_j [eta_K a^2 - 2F] has eigenvalues
       alpha_par (a || direction)  = eta_K + 2/(1+s)^2   [= eta + (mu-hat + 2X mu-hat')]
       alpha_perp (2x)             = eta_K + 2/(1+s)
  3  The F-sector contains NO time derivatives and NO shift:
       => pi^ij = dL/d hdot_ij is exactly the (lam_K-)GR one, momentum constraints
       H_i are exactly the (lam_K-)GR ones, pi_N = pi_i = 0 primaries.
       Higher SPATIAL derivatives (Rbar^2) add k^4 gradients, not new momenta.
  4  Quadratic action, scalar sector around flat space, unitary gauge, E=0 spatial
     gauge: fields phi (lapse), B (shift potential), psi (conformal). Fourier-average,
     eliminate the non-dynamical phi and B, obtain the single khronon branch
     D(omega,k) = U omega^2 - V k^2 - W k^4.  Verify:
       - the phi row has NO omega^2: the lapse equation is ELLIPTIC (determines N),
         not a propagating equation and not a first-class constraint;
       - U sign  => no-ghost condition on (alpha, lam_K);
       - c_s^2 = V/U;  W ~ eps A(X0) => sign condition on eps.
  5  Tensor sector: standard graviton + k^4 correction from the Y-term
       omega_T^2 = k^2 + (coef) eps A(X0) k^4   (k in units a0/c^2 = 1/ell)
     => eps >= 0 for high-k tensor stability AND a GW170817 dispersion bound.
  6  Stability window at finite X0 (eikonal): with the DERIVED c_s^2(alpha, lam):
       alpha_par(s), alpha_perp(s) must lie in (0, 2).
       eta_K = 0 puts BOTH in (0,2) for ALL s>0 (boundaries only asymptotic);
       eta_K > 0: alpha_par > 2 for s < s_c  => deep-MOND gradient instability
                  (the Blanchet-Skordis-type low-k instability, derived here);
       eta_K < 0: alpha_par < 0 for s > s*  => ghost in the Newtonian regime.
  7  Numbers: strong-coupling length sqrt(l_Pl * ell) ~ 0.1 mm; GW170817 bound on eps
     vs the eps needed for the Y-term to matter in galaxies.
"""
import sympy as sp

t, z, x, y = sp.symbols('t z x y')
epsp = sp.Symbol('varepsilon')                 # perturbation bookkeeping parameter
lam, eta, al = sp.symbols('lambda_K eta_K alpha', real=True)
epsA = sp.Symbol('epsA', real=True)            # = eps * A(X0)  (>=0 to be determined)
w, k = sp.symbols('omega k', real=True)
s = sp.Symbol('s', positive=True)              # s = sqrt(X0) = g/a0 on the background

coords = (x, y, z)
results = []
def report(name, ok, extra=""):
    print(("PASS  " if ok else "FAIL  ") + name + (("   " + extra) if extra else ""))
    results.append(ok)

# ---------- geometry helpers (3D, spatial derivatives only) ----------
def christoffel(h):
    hinv = h.inv()
    return [[[sp.together(sum(hinv[a, l]*(sp.diff(h[l, i], coords[j])
                                          + sp.diff(h[l, j], coords[i])
                                          - sp.diff(h[i, j], coords[l]))
                              for l in range(3))/2)
              for j in range(3)] for i in range(3)] for a in range(3)]

def ricci(h):
    G = christoffel(h)
    R = sp.zeros(3, 3)
    for i in range(3):
        for j in range(3):
            R[i, j] = (sum(sp.diff(G[a][i][j], coords[a]) for a in range(3))
                       - sum(sp.diff(G[a][i][a], coords[j]) for a in range(3))
                       + sum(G[a][a][b]*G[b][i][j] for a in range(3) for b in range(3))
                       - sum(G[a][i][b]*G[b][a][j] for a in range(3) for b in range(3)))
    return R

# =====================================================================
print("="*78)
print("CHECK 1: analytic structure of F(X) at X=0   [DERIVED]")
X = sp.Symbol('X', positive=True)
u = sp.Symbol('u', positive=True)              # u = sqrt(X)
F = -2*sp.sqrt(X) + 2*sp.log(1 + sp.sqrt(X))
FX = sp.simplify(sp.diff(F, X))
report("F_X = -1/(1+sqrt X)", sp.simplify(FX + 1/(1 + sp.sqrt(X))) == 0)
Fu = -2*u + 2*sp.log(1 + u)
ser = sp.expand(sp.series(Fu, u, 0, 6).removeO())
target = -u**2 + sp.Rational(2, 3)*u**3 - u**4/2 + sp.Rational(2, 5)*u**5
report("F = -X + (2/3)X^{3/2} - X^2/2 + (2/5)X^{5/2}+... (sqrt-X cancels; C^1 at 0)",
       sp.simplify(ser - target) == 0)
FXX = sp.simplify(sp.diff(F, X, 2))
report("F_XX = 1/(2 sqrt X (1+sqrt X)^2) > 0, DIVERGES as X->0",
       sp.simplify(FXX - 1/(2*sp.sqrt(X)*(1 + sp.sqrt(X))**2)) == 0
       and sp.limit(FXX, X, 0, '+') == sp.oo)
A = X**2/(1 + X)**4
report("A(1)=1/16, A'(1)=0, A~X^2 (X<<1), A~X^-2 (X>>1)",
       A.subs(X, 1) == sp.Rational(1, 16)
       and sp.simplify(sp.diff(A, X).subs(X, 1)) == 0
       and sp.limit(A/X**2, X, 0) == 1 and sp.limit(A*X**2, X, sp.oo) == 1)

# =====================================================================
print("="*78)
print("CHECK 2: a-sector Hessian at X0 = s^2 > 0   [DERIVED]")
a1, a2, a3 = sp.symbols('a1 a2 a3', real=True)
asq = a1**2 + a2**2 + a3**2
Lq = eta*asq - 2*(-2*sp.sqrt(asq) + 2*sp.log(1 + sp.sqrt(asq)))
H = sp.hessian(Lq, (a1, a2, a3)).subs({a1: s, a2: 0, a3: 0})
alpha_par = sp.simplify(H[0, 0]/2)
alpha_perp = sp.simplify(H[1, 1]/2)
report("alpha_par  = eta_K + 2/(1+s)^2",
       sp.simplify(alpha_par - (eta + 2/(1 + s)**2)) == 0)
report("alpha_perp = eta_K + 2/(1+s)",
       sp.simplify(alpha_perp - (eta + 2/(1 + s))) == 0)
report("Hessian diagonal in (par,perp) basis",
       all(sp.simplify(H[i, j]) == 0 for i in range(3) for j in range(3) if i != j))
# AQUAL-type combination: mu-hat = -2 F_X = 2/(1+s);  mu-hat + 2X mu-hat' = 2/(1+s)^2
muh = 2/(1 + u)
report("alpha_par - eta = mu-hat + 2X d(mu-hat)/dX  (AQUAL combination, positive)",
       sp.simplify((muh + 2*u**2*sp.diff(muh, u)/(2*u)).subs(u, s)
                   - (alpha_par - eta)) == 0)

# =====================================================================
print("="*78)
print("CHECK 3/4: scalar sector quadratic action around flat slicing   [DERIVED]")
phi = sp.Function('phi')(t, z)     # N = 1 + eps*phi        (lapse perturbation)
B   = sp.Function('B')(t, z)       # N_i = eps * d_i B      (shift potential)
psi = sp.Function('psi')(t, z)     # h_ij = (1-2 eps psi) delta_ij (E=0 spatial gauge)
f = 1 - 2*epsp*psi
h3 = sp.diag(f, f, f)
hinv = h3.inv()
sqh = sp.sqrt(h3.det())
N = 1 + epsp*phi
Ni = sp.Matrix([0, 0, epsp*sp.diff(B, z)])   # lower-index shift
G3 = christoffel(h3)
DN = sp.zeros(3, 3)
for i in range(3):
    for j in range(3):
        DN[i, j] = sp.diff(Ni[j], coords[i]) - sum(G3[a][i][j]*Ni[a] for a in range(3))
K = sp.zeros(3, 3)
for i in range(3):
    for j in range(3):
        K[i, j] = (sp.diff(h3[i, j], t) - DN[i, j] - DN[j, i])/(2*N)
Ktr = sum(hinv[i, j]*K[i, j] for i in range(3) for j in range(3))
KK = sum(hinv[i, a]*hinv[j, b]*K[i, j]*K[a, b]
         for i in range(3) for j in range(3) for a in range(3) for b in range(3))
R3m = ricci(h3)
R3 = sp.together(sum(hinv[i, j]*R3m[i, j] for i in range(3) for j in range(3)))
Rbar = R3m - h3*R3/3
Ybar = sum(hinv[i, a]*hinv[j, b]*Rbar[i, j]*Rbar[a, b]
           for i in range(3) for j in range(3) for a in range(3) for b in range(3))
aln = [sp.diff(sp.log(N), c) for c in coords]
asqf = sum(hinv[i, j]*aln[i]*aln[j] for i in range(3) for j in range(3))

# --- canonical-structure assertions on the F-sector building blocks ---
def has_t_derivative(expr):
    return any(any(v == t for v, c in d.variable_count)
               for d in expr.atoms(sp.Derivative))
report("X-building block a_i a^i: NO time derivatives (pi^ij untouched)",
       not has_t_derivative(asqf))
report("Y-building block Rbar_ij Rbar^ij: NO time derivatives (pi^ij untouched)",
       not has_t_derivative(Ybar))
report("F-sector contains NO shift (momentum constraint H_i untouched)",
       (B.func not in [a.func for a in asqf.atoms(sp.Function)])
       and (B.func not in [a.func for a in Ybar.atoms(sp.Function)]))
LF = N*sqh*(al*asqf - 2*epsA*Ybar)
report("d(F-sector Lagrangian)/d(psi-dot) == 0 identically",
       sp.simplify(sp.diff(LF, sp.Derivative(psi, t))) == 0)

# --- quadratic Lagrangian (alpha stands for eta_K + 2 at X=0, or alpha_par/perp at X0) ---
Lfull = N*sqh*(R3 + KK - lam*Ktr**2 + al*asqf - 2*epsA*Ybar)
Lser = sp.expand(sp.series(Lfull, epsp, 0, 3).removeO())
L2 = sp.expand(Lser.coeff(epsp, 2))
L0 = sp.simplify(Lser.coeff(epsp, 0))
report("background (eps^0) Lagrangian vanishes on flat slicing", L0 == 0)

# --- Fourier average:  f -> A E + Ac/E,  E = exp(i(k z - w t)) ---
Aph, Aphc, AB, ABc, Aps, Apsc = sp.symbols('A_phi A_phi_c A_B A_B_c A_psi A_psi_c')
fmap = {phi.func: (Aph, Aphc), B.func: (AB, ABc), psi.func: (Aps, Apsc)}
E = sp.Symbol('E_')
def fourier_avg(L):
    def drepl(e):
        base = e.expr.func
        Af, Afc = fmap[base]
        m = n = 0
        for v, c in e.variable_count:
            if v == t: m = c
            elif v == z: n = c
            else: raise ValueError("unexpected derivative variable")
        return (Af*(-sp.I*w)**m*(sp.I*k)**n*E
                + Afc*(sp.I*w)**m*(-sp.I*k)**n/E)
    expr = L.replace(lambda e: isinstance(e, sp.Derivative)
                     and getattr(e.expr, 'func', None) in fmap, drepl)
    for base, (Af, Afc) in fmap.items():
        expr = expr.subs(base(t, z), Af*E + Afc/E)
    p = sp.Poly(sp.expand(expr*E**6), E)
    return sp.expand(p.coeff_monomial(E**6))

Lavg = fourier_avg(L2)

# --- the lapse row: elliptic, no omega^2 ---
eq_phi = sp.expand(sp.diff(Lavg, Aphc))
report("lapse (phi) equation contains NO omega at all: N is DETERMINED (elliptic), "
       "not propagating", sp.degree(sp.Poly(eq_phi, w), w) == 0)
eq_B = sp.expand(sp.diff(Lavg, ABc))

# --- eliminate the non-dynamical phi and B ---
sol = sp.solve([eq_phi, eq_B], [Aph, AB], dict=True)
assert len(sol) == 1, "auxiliary elimination not unique"
Leff = sp.simplify(sp.expand(Lavg.subs(sol[0])))
D = sp.cancel(Leff/(Aps*Apsc))
report("reduced action is a single khronon branch  D(omega,k) |A_psi|^2",
       not any(sym in D.free_symbols for sym in (Aph, Aphc, AB, ABc, Aps, Apsc)))
Dn, Dd = sp.fraction(sp.cancel(sp.together(D)))
Dn = sp.expand(Dn); Dd = sp.expand(Dd)
print("   D numerator  :", Dn)
print("   D denominator:", Dd)
# kinetic (ghost) coefficient and dispersion
U = sp.simplify(sp.diff(D, w, 2)/2)
print("   U (omega^2 coefficient of D)      :", U)
disp = sp.solve(sp.Eq(Dn, 0), w**2)
assert len(disp) == 1
w2 = sp.simplify(disp[0])
print("   dispersion  omega^2 =", sp.factor(w2))
csq_derived = sp.simplify(w2.subs(epsA, 0)/k**2)
cand = (lam - 1)*(2 - al)/(al*(3*lam - 1))
report("c_s^2 = (lam_K-1)(2-alpha)/(alpha(3 lam_K-1))   [DERIVED, matches khronometric form]",
       sp.simplify(csq_derived - cand) == 0)
# k^4 piece from the Y-term
Wk4 = sp.simplify((w2 - w2.subs(epsA, 0)))
print("   Y-term contribution to omega^2 :", sp.factor(Wk4))
Wcoef = sp.simplify(Wk4/(epsA*k**4))
report("scalar k^4 term  omega^2 += (coef) * epsA * k^4  with coef > 0 for no-ghost params",
       sp.simplify(sp.diff(Wk4, epsA)).has(k) and
       sp.simplify(Wcoef.subs({lam: 2, al: 1})) > 0)
print("   scalar k^4 coefficient / epsA  :", Wcoef)
# no-ghost condition: sign of U.  DERIVED RESULT: U = 4(3 lam_K - 1)/(lam_K - 1),
# INDEPENDENT of alpha.  In unitary gauge the alpha-window is NOT a ghost condition:
# alpha outside (0,2) shows up as omega^2 < 0 (an instability at every k), while the
# ghost condition is purely lam_K > 1 or lam_K < 1/3.  (In the Stueckelberg frame the
# same pathology is redistributed into the khronon kinetic term; the frame-invariant
# statement is: healthy <=> U > 0 AND omega^2 > 0.)
report("U = 4(3 lam_K-1)/(lam_K-1), alpha-INDEPENDENT: no-ghost <=> lam_K>1 or lam_K<1/3",
       sp.simplify(U - 4*(3*lam - 1)/(lam - 1)) == 0
       and U.subs(lam, 2) > 0 and U.subs(lam, sp.Rational(1, 5)) > 0
       and U.subs(lam, sp.Rational(1, 2)) < 0)
report("alpha-window is the GRADIENT condition: given no-ghost, omega^2>0 <=> 0<alpha<2 "
       "(spot checks lam_K=2: alpha=1 stable, alpha=-1 and alpha=3 unstable)",
       csq_derived.subs({lam: 2, al: 1}) > 0
       and csq_derived.subs({lam: 2, al: -1}) < 0
       and csq_derived.subs({lam: 2, al: 3}) < 0)

# =====================================================================
print("="*78)
print("CHECK 5: tensor sector + Y-term k^4   [DERIVED]")
Ht = sp.Function('H')(t, z)
hT = sp.Matrix([[1, epsp*Ht, 0], [epsp*Ht, 1, 0], [0, 0, 1]])
hTinv = hT.inv(); sqhT = sp.sqrt(hT.det())
GT = christoffel(hT)
KT = sp.zeros(3, 3)
for i in range(3):
    for j in range(3):
        KT[i, j] = sp.diff(hT[i, j], t)/2          # N=1, N_i=0
KtrT = sum(hTinv[i, j]*KT[i, j] for i in range(3) for j in range(3))
KKT = sum(hTinv[i, a]*hTinv[j, b]*KT[i, j]*KT[a, b]
          for i in range(3) for j in range(3) for a in range(3) for b in range(3))
RTm = ricci(hT)
RT = sum(hTinv[i, j]*RTm[i, j] for i in range(3) for j in range(3))
RbarT = RTm - hT*RT/3
YbarT = sum(hTinv[i, a]*hTinv[j, b]*RbarT[i, j]*RbarT[a, b]
            for i in range(3) for j in range(3) for a in range(3) for b in range(3))
LT = sqhT*(RT + KKT - lam*KtrT**2 - 2*epsA*YbarT)
LT2 = sp.expand(sp.expand(sp.series(LT, epsp, 0, 3).removeO()).coeff(epsp, 2))
AH, AHc = sp.symbols('A_H A_H_c')
fmap = {Ht.func: (AH, AHc)}
LTavg = fourier_avg(LT2)
DT = sp.cancel(sp.simplify(LTavg/(AH*AHc)))
print("   tensor quadratic form  D_T =", sp.expand(DT))
UT = sp.simplify(sp.diff(DT, w, 2)/2)
report("tensor kinetic coefficient positive (never a ghost; lam_K drops out)",
       UT.is_positive is True or sp.simplify(UT) > 0)
w2T = sp.solve(sp.Eq(sp.expand(DT), 0), w**2)[0]
print("   tensor dispersion  omega_T^2 =", sp.factor(w2T))
cT2 = sp.simplify(w2T.subs(epsA, 0)/k**2)
report("c_T = 1 at k->0 (GW speed exact at leading order)", sp.simplify(cT2 - 1) == 0)
WT = sp.simplify((w2T - w2T.subs(epsA, 0))/(epsA*k**4))
print("   tensor k^4 coefficient / epsA :", WT)
report("tensor high-k stability  <=>  eps >= 0  (omega_T^2 = k^2 + WT*epsA*k^4, WT>0)",
       sp.simplify(WT) > 0)

# =====================================================================
print("="*78)
print("CHECK 6: stability window at finite X0 (eikonal)   [DERIVED]")
csq = csq_derived            # trust the derivation, not memory
c_par = sp.simplify(csq.subs(al, eta + 2/(1 + s)**2))
c_perp = sp.simplify(csq.subs(al, eta + 2/(1 + s)))
c_par_eta0 = sp.simplify(c_par.subs(eta, 0))
c_perp_eta0 = sp.simplify(c_perp.subs(eta, 0))
report("eta_K=0:  c_par^2  = s(s+2)(lam_K-1)/(3 lam_K-1)",
       sp.simplify(c_par_eta0 - s*(s + 2)*(lam - 1)/(3*lam - 1)) == 0)
report("eta_K=0:  c_perp^2 = s(lam_K-1)/(3 lam_K-1)",
       sp.simplify(c_perp_eta0 - s*(lam - 1)/(3*lam - 1)) == 0)
# eta_K = 0 keeps 0 < alpha < 2 for every s > 0: algebraic proof
ap0 = 2/(1 + s)**2; at0 = 2/(1 + s)
gap_par = sp.factor(2 - ap0)    # = 2 s (s+2)/(1+s)^2 > 0 for s > 0
gap_perp = sp.factor(2 - at0)   # = 2 s/(1+s) > 0 for s > 0
report("eta_K=0: 0 < alpha_par, alpha_perp < 2 for ALL s>0 (window boundaries only asymptotic)",
       sp.simplify(gap_par - 2*s*(s + 2)/(1 + s)**2) == 0
       and sp.simplify(gap_perp - 2*s/(1 + s)) == 0
       and ap0.subs(s, 1) > 0 and at0.subs(s, 1) > 0
       and bool((2*s*(s + 2)/(1 + s)**2).is_positive) in (True,)
       or (gap_par.is_positive is True and gap_perp.is_positive is True))
# eta_K > 0: alpha_par > 2 for s < s_c  (deep-MOND gradient instability, BS-type)
sc_formula = lambda e: (2/(2 - e))**0.5 - 1
ok_sc = True
for ev in (0.5, 1.0, 1.5):
    scn = [complex(r) for r in sp.solve(sp.Eq(ev + 2/(1 + s)**2, 2), s)]
    scn = [r.real for r in scn if abs(r.imag) < 1e-12 and r.real > 0]
    ok_sc &= len(scn) == 1 and abs(scn[0] - sc_formula(ev)) < 1e-12
    # verify instability inside, stability outside
    ok_sc &= (ev + 2/(1 + 0.5*scn[0])**2) > 2 and (ev + 2/(1 + 2*scn[0])**2) < 2
report("eta_K>0: alpha_par crosses 2 at s_c = sqrt(2/(2-eta_K)) - 1  => c_par^2 < 0 for "
       "s < s_c  (LOW-k gradient instability in the deep-MOND regime, Blanchet-Skordis "
       "structure DERIVED here)", bool(ok_sc))
# eta_K < 0: alpha_par < 0 for s > s*  (Newtonian-regime instability)
etav = sp.Symbol('eta_v', positive=True)   # etav = |eta_K|
sstar = sp.solve(sp.Eq(-etav + 2/(1 + s)**2, 0), s)
sstar = [r for r in sstar if r.is_positive is not False]
report("eta_K<0: alpha_par crosses 0 at s* = sqrt(2/|eta_K|) - 1  => omega^2 < 0 at "
       "every k for s > s* (Newtonian-regime instability)",
       any(sp.simplify(r - (sp.sqrt(2/etav) - 1)) == 0 for r in sstar))

# =====================================================================
print("="*78)
print("CHECK 7: numbers   [DERIVED from the above + measured constants]")
c_si = 2.99792458e8; a0_si = 9.3619e-11
ell = c_si**2/a0_si
lPl = 1.616255e-35
l_sc = (lPl*ell)**0.5
print(f"   MOND length     ell = c^2/a0            = {ell:.3e} m")
print(f"   strong-coupling length sqrt(l_Pl*ell)   = {l_sc*1e3:.3f} mm")
report("deep-MOND strong-coupling length ~ 0.1 mm (cubic |da|^3 from the X^{3/2} term)",
       0.05e-3 < l_sc < 0.5e-3)
# GW170817: tensor dispersion  Delta v/v ~ WT * epsA * (k ell)^2, epsA = eps*A(X0) on path
WT_num = float(WT)
kgw = 2*3.141592653589793*100.0/c_si            # 100 Hz
kl2 = (kgw*ell)**2
A_MW = (4.0**2)/(1 + 4.0)**4                     # X0 ~ 4 inside the Milky Way (x~2)
fpath = 2e-4                                     # ~8 kpc of galaxy per 40 Mpc path
eps_gw = 1e-15/(WT_num*fpath*A_MW*kl2)
x_gal, r_gal = 1.0, 3.086e20                     # 10 kpc, x = 1
Y_gal = (x_gal*ell/r_gal)**2
A_gal = 1.0/16.0
eps_pheno = 1.0/(A_gal*Y_gal)                    # eps A Y ~ O(1) = "Y-term matters"
print(f"   (k ell)^2 at 100 Hz                     = {kl2:.3e}")
print(f"   GW170817 bound (galaxy-interior path)   : eps < {eps_gw:.3e}")
print(f"   eps needed for Y-term to matter (10 kpc): eps ~ {eps_pheno:.3e}")
print(f"   GAP: eps_pheno/eps_bound                = {eps_pheno/eps_gw:.3e}")
report("Y-term: any eps that matters in galaxies violates the GW170817 dispersion "
       "bound by tens of orders of magnitude", eps_pheno/eps_gw > 1e30)

# =====================================================================
print("="*78)
print("DOF LEDGER (unitary gauge; the count DERIVED from the checks above)")
print("""   Phase space: h_ij,pi^ij (12) + N,pi_N (2) + N^i,pi_i (6)      = 20
   First class: pi_i ~ 0 (3) + H_i ~ 0 (3)  [F-sector shift-free]   -> -12
   Second class: pi_N ~ 0 with C_N = dH/dN  [elliptic in N, CHECK 4] -> -2
   Residual t -> f(t): ONE global first-class constraint (zero mode, not a field DOF)
   Local field DOF = (20 - 12 - 2)/2 = 3  =  2 tensor + 1 khronon scalar   [VERIFIED:
   one scalar branch (CHECK 4) + two tensor polarisations (CHECK 5)]
   lam_K = 1/3 excluded: pi-trace = (1-3 lam_K) K sqrt(h) not invertible there.""")
n_pass = sum(1 for r in results if r)
print(f"SUMMARY: {n_pass}/{len(results)} checks passed")
if n_pass != len(results):
    raise SystemExit(1)
