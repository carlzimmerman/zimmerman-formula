#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
sf42_flrw_expansion_hessian_2026.py -- the EXPANSION (theta != 0) attack on the single-invariant no-go.

CONTEXT
-------
sf40 + sf41 (committed) proved: for the York/CMC gravity sector plus a single local carrier
a0^2 F(A^2/a0^2), A_mu = u^nu nabla_nu u_mu the khronon acceleration, the scalar-sector velocity
Hessian is
      Z_ij = F'(s) delta_ij + (2 F''(s)/a0^2) abar_i abar_j ,   s = A^2/a0^2 = (g/a0)^2,
with eigenvalues  Z_perp = F' = 2(1-mu)  (x2, transverse)  and  Z_par = F' + 2 s F''  (longitudinal).
Z_perp = 2(1-mu) > 0 wherever MOND is on (mu<1)  =>  the khronon PROPAGATES  =>  no 2+0 removal.

THE STATED WEAK POINT (sf40/sf41 SCOPE): every background used had the khronon congruence expansion
theta = K = 0 and shear sigma = 0 (static/Minkowski).  A GENERIC background has theta != 0
(FLRW: theta = 3H).  ATTACK: does the a(t) time-dependence feed a theta-dependent piece into the
khronon-fluctuation acceleration a_mu[phi] that makes an eigenvalue of Z_ij vanish while mu < 1?

THIS SCRIPT recomputes the velocity Hessian in the Stuckelberg frame phi = t + eps*chi on
      g = diag(-N(x)^2, a(t)^2, a(t)^2, a(t)^2),
which has  theta = 3 adot/(aN) != 0,  sigma = 0,  and (with N=N(x))  abar_x = d_x ln N != 0 : a MOND
region embedded in an expanding universe.  a_mu is built FULLY COVARIANTLY (Christoffels carry adot,
e.g. Gamma^0_{ij} = a adot delta_ij/N^2, Gamma^i_{0j} = (adot/a) delta^i_j), so any theta-piece is
captured.  A^2 = a_mu a^mu is expanded to O(chi^2), the carrier quadratic action formed, and the
coefficient of (d_i chidot)(d_j chidot) read off.

Cross-checks: covariant a_mu == projector -h_mu^nu d_nu lnX (adot-free route); sqrt/log expansion
self-consistency; a NUMERIC finite-difference match of exact-vs-truncated A^2 on de Sitter.

VERDICT: SURVIVES on FLRW.  adot enters neither a_mu nor A^2; Z_perp = F' = 2(1-mu) unchanged.
Reason (geometric): nabla_mu u_nu = -u_mu a_nu + K_mu nu (+shear+vorticity); a_mu is the u-directed
part, K_ij (carrying theta) the transverse-symmetric part -- orthogonal decomposition, so the
acceleration scalar A^2 is theta-blind.  Expansion is a genuinely NEW invariant, not a piece of F(A^2).

Exit 0 = every numbered check passed.
"""
import sys
import sympy as sp

FAIL, NCHK = [], [0]

def check(cond, label, detail=""):
    NCHK[0] += 1
    ok = bool(cond)
    print(f"  [{'ok' if ok else 'FAIL'}] {NCHK[0]:02d} {label}" + (f"   {detail}" if detail else ""))
    if not ok:
        FAIL.append(f"{NCHK[0]:02d} {label}")

def hdr(s):
    print("\n" + "=" * 80); print(s); print("=" * 80)

t, x, y, z = sp.symbols('t x y z', real=True)
a0 = sp.Symbol('a0', positive=True)
eps = sp.Symbol('eps')
F1, F2 = sp.symbols('F1 F2', real=True)           # F'(s0), F''(s0): INDEPENDENT (no-go must hold for any)
coords = [t, x, y, z]

def T(e):
    """truncate a polynomial in eps to O(eps^2)"""
    e = sp.expand(e)
    return e.coeff(eps, 0) + e.coeff(eps, 1) * eps + e.coeff(eps, 2) * eps ** 2

def build(Nfun, afun, chifun):
    """return dict of everything for background g=diag(-N^2,a^2,a^2,a^2), field phi=t+eps*chi."""
    N, a, chi = Nfun, afun, chifun
    adot, addot = sp.Derivative(a, t), sp.Derivative(a, t, t)
    g = sp.diag(-N**2, a**2, a**2, a**2)
    ginv = sp.diag(-1/N**2, 1/a**2, 1/a**2, 1/a**2)
    sqrtmg = N * a**3
    # Christoffels (expand only)
    G = [[[sp.Integer(0)] * 4 for _ in range(4)] for _ in range(4)]
    for l in range(4):
        for m in range(4):
            for nu in range(4):
                tot = sp.Integer(0)
                for si in range(4):
                    tot += ginv[l, si] * (sp.diff(g[si, m], coords[nu])
                                          + sp.diff(g[si, nu], coords[m])
                                          - sp.diff(g[m, nu], coords[si]))
                G[l][m][nu] = sp.expand(sp.Rational(1, 2) * tot)
    theta = sp.simplify(sum(sp.diff(sqrtmg * (ginv * sp.Matrix([-N, 0, 0, 0]))[m], coords[m])
                            for m in range(4)) / sqrtmg)
    # field, X^2, manual eps expansion of 1/X and lnX (sympy series chokes on MV Derivatives)
    phi = t + eps * chi
    dphi = [sp.diff(phi, c) for c in coords]
    X2 = sp.expand(-sum(ginv[i, i] * dphi[i]**2 for i in range(4)))    # = 1/N^2 + O(eps)
    P0 = sp.Rational(1) / N**2
    r = T((X2 - P0) * N**2)                                            # = u/P0, O(eps)
    invX = T(N * (1 - r/2 + sp.Rational(3, 8) * r**2))                 # (1+r)^{-1/2}
    lnX = T(-sp.log(N) + r/2 - r**2/4)                                # (1/2)log(P0(1+r))
    selfchk = sp.expand(T(invX**2 * X2) - 1)
    selfchk = sp.expand(selfchk.coeff(eps, 0)) + sp.expand(selfchk.coeff(eps, 1))*eps + sp.expand(selfchk.coeff(eps, 2))*eps**2
    u_dn = [T(-dphi[m] * invX) for m in range(4)]
    u_up = [T(ginv[m, m] * u_dn[m]) for m in range(4)]
    # covariant acceleration a_mu = u^nu ( d_nu u_mu - Gamma^l_{nu mu} u_l )
    a_cov = []
    for m in range(4):
        tot = sp.Integer(0)
        for nu in range(4):
            term = sp.diff(u_dn[m], coords[nu])
            for l in range(4):
                term -= G[l][nu][m] * u_dn[l]
            tot += u_up[nu] * term
        a_cov.append(T(tot))
    # projector acceleration a_mu = -h_mu^nu d_nu lnX (X=1/N bg => a_i=+d_i lnN=-d_i lnX), adot-free
    dlnX = [sp.diff(lnX, c) for c in coords]
    a_proj = []
    for m in range(4):
        tot = dlnX[m]
        for nu in range(4):
            tot += u_dn[m] * u_up[nu] * dlnX[nu]
        a_proj.append(T(-tot))
    A2 = T(sum(ginv[i, i] * a_cov[i]**2 for i in range(4)))
    return dict(N=N, a=a, chi=chi, adot=adot, addot=addot, ginv=ginv, sqrtmg=sqrtmg, theta=theta,
                G=G, selfchk=selfchk, a_cov=a_cov, a_proj=a_proj, A2=A2)

def hessian(D):
    A2, sqrtmg, ginv = D['A2'], D['sqrtmg'], D['ginv']
    A2_0, A2_1, A2_2 = (sp.expand(A2.coeff(eps, k)) for k in range(3))
    L2 = sp.expand(sqrtmg * (F1 * A2_2 + sp.Rational(1, 2) * F2 * A2_1**2 / a0**2))
    chi = D['chi']
    chi_atoms = [d for d in L2.atoms(sp.Derivative) if d.expr.func == chi.func]
    symmap = {d: sp.Symbol('D%d' % i) for i, d in enumerate(chi_atoms)}
    back = {v: k for k, v in symmap.items()}
    L2p = sp.expand(L2.xreplace(symmap))
    def Sy(*o):
        return symmap.get(sp.Derivative(chi, *o))
    def csq(s):
        if s is None:
            return sp.Integer(0)
        return sp.simplify((L2p.diff(s, 2) / 2).xreplace({sym: 0 for sym in back}))
    def cpr(s1, s2):
        if s1 is None or s2 is None:
            return sp.Integer(0)
        return sp.simplify(L2p.diff(s1).diff(s2).xreplace({sym: 0 for sym in back}))
    return dict(A2_0=A2_0, Zyy=csq(Sy(t, y)), Zzz=csq(Sy(t, z)), Zxx=csq(Sy(t, x)),
                Zxy=cpr(Sy(t, x), Sy(t, y)), Cv2=csq(Sy(t)), Cacc2=csq(Sy(t, t)))

def has_adot(e, D):
    ders = sp.sympify(e).atoms(sp.Derivative)
    return (D['adot'] in ders) or (D['addot'] in ders)


# ==================================================================================
hdr("PART A -- FLRW + static lapse N(x):  theta != 0, sigma = 0, abar_x != 0 (cosmological MOND cell)")
# ==================================================================================
N1 = sp.Function('N', positive=True)(x)
a1 = sp.Function('a', positive=True)(t)
chi1 = sp.Function('chi')(t, x, y, z)
D1 = build(N1, a1, chi1)
H1 = hessian(D1)
print("  theta =", D1['theta'], "  (= 3 adot/(aN) != 0)")
print("  Gamma^0_{yy} =", D1['G'][0][2][2], "   Gamma^y_{0y} =", D1['G'][2][0][2], "  (adot-carrying)")

check(D1['theta'] != 0, "background expansion theta != 0 (genuine FLRW, not static)",
      "theta = 3 adot/(aN)")
check(D1['selfchk'] == 0, "sqrt/log eps-expansion self-consistent (invX^2 X2 - 1 = 0 to O(eps^2))")
check(all(sp.expand(D1['a_cov'][m] - D1['a_proj'][m]) == 0 for m in range(4)),
      "INDEPENDENT ROUTE: covariant a_mu == projector -h.dlnX to O(eps^2)",
      "adot-Christoffel route and adot-free projector route agree")
check(not any(has_adot(D1['a_cov'][m], D1) for m in range(4)),
      "adot appears in NO component of the fluctuation acceleration a_mu",
      "the expansion drops out of a_mu itself (a_mu is the u-directed part, K_ij is separate)")
check(not has_adot(D1['A2'], D1),
      "adot appears NOWHERE in the scalar A^2 = a_mu a^mu (the only thing F sees)",
      "=> a0^2 F(A^2/a0^2) is theta-blind to O(chi^2)")

s0 = sp.simplify(H1['A2_0'] / a0**2)
Zperp_norm = sp.simplify(H1['Zyy'] / (D1['sqrtmg'] * D1['ginv'][2, 2]))
Zpar_norm = sp.simplify(H1['Zxx'] / (D1['sqrtmg'] * D1['ginv'][1, 1]))
print("\n  Z_perp (d_y chidot)^2 =", H1['Zyy'], "   Z_perp (d_z chidot)^2 =", H1['Zzz'])
print("  Z_par  (d_x chidot)^2 =", H1['Zxx'])
print("  normalized  Z_perp =", Zperp_norm, "   Z_par =", Zpar_norm, "   s0 =", s0)
check(sp.simplify(H1['Zyy'] - H1['Zzz']) == 0 and not has_adot(H1['Zyy'], D1),
      "the two transverse eigenvalues are equal and adot-FREE")
check(sp.simplify(Zperp_norm - F1) == 0,
      "TRANSVERSE eigenvalue Z_perp = F'(s0)  EXACTLY (= 2(1-mu)) -- identical to the static result",
      "theta introduces NO new term in Z_perp")
check(sp.simplify(Zpar_norm - (F1 + 2 * s0 * F2)) == 0,
      "LONGITUDINAL eigenvalue Z_par = F'(s0) + 2 s0 F''(s0)  EXACTLY -- identical to the static result")
check(sp.simplify(H1['Zxy']) == 0, "off-diagonal (d_x chidot)(d_y chidot) coefficient vanishes")
check(sp.simplify(H1['Cv2']) == 0,
      "the bare chidot^2 (k->0) coefficient is IDENTICALLY 0, on FLRW too (no theta-induced mass-kinetic)")
check(sp.simplify(H1['Cacc2']) == 0,
      "the chiddot^2 coefficient is IDENTICALLY 0, on FLRW too (no theta-induced Ostrogradski ghost)")


# ==================================================================================
hdr("PART B -- pure FLRW (N=1, abar=0):  theta != 0, s=0 -- isolates the pure expansion effect")
# ==================================================================================
D2 = build(sp.Integer(1), sp.Function('a', positive=True)(t), sp.Function('chi')(t, x, y, z))
H2 = hessian(D2)
print("  theta =", D2['theta'])
check(D2['theta'] != 0 and not has_adot(D2['A2'], D2),
      "pure FLRW: theta != 0 yet A^2 still adot-free",
      "confirms the abar!=0 case: expansion alone adds nothing to A^2")
check(sp.simplify(H2['Zyy'] / (D2['sqrtmg'] * D2['ginv'][2, 2]) - F1) == 0
      and sp.simplify(H2['Cv2']) == 0 and sp.simplify(H2['Cacc2']) == 0,
      "pure FLRW: Z_perp = F', chidot^2 = 0, chiddot^2 = 0 -- same structure as static")


# ==================================================================================
hdr("PART C -- NUMERIC VALIDATION: exact A^2 vs truncated O(eps^2) on de Sitter (adot = H a != 0)")
# ==================================================================================
import mpmath as mp
mp.mp.dps = 40
Nc = sp.exp(sp.Rational(3, 10) * x)          # b = 0.3
ac = sp.exp(sp.Rational(7, 10) * t)          # H = 0.7 => adot = 0.7 a != 0 (de Sitter)
chic = (sp.sin(sp.Rational(11, 10)*t + sp.Rational(7, 10)*x) * sp.cos(sp.Rational(1, 2)*y) * sp.exp(-sp.Rational(1, 5)*z)
        + sp.Rational(3, 10) * sp.cos(sp.Rational(9, 10)*t) * sp.sin(sp.Rational(6, 10)*x + sp.Rational(4, 10)*y))
ginv = sp.diag(-1/Nc**2, 1/ac**2, 1/ac**2, 1/ac**2)
gg = sp.diag(-Nc**2, ac**2, ac**2, ac**2)
Gc = [[[sp.Integer(0)] * 4 for _ in range(4)] for _ in range(4)]
for l in range(4):
    for m in range(4):
        for nu in range(4):
            tot = sp.Integer(0)
            for si in range(4):
                tot += ginv[l, si] * (sp.diff(gg[si, m], coords[nu]) + sp.diff(gg[si, nu], coords[m]) - sp.diff(gg[m, nu], coords[si]))
            Gc[l][m][nu] = sp.Rational(1, 2) * tot
phi = t + eps * chic
dphi = [sp.diff(phi, c) for c in coords]
X2c = -sum(ginv[i, i] * dphi[i]**2 for i in range(4))
Xc = sp.sqrt(X2c)
u_dn = [-dphi[m] / Xc for m in range(4)]
u_up = [ginv[m, m] * u_dn[m] for m in range(4)]
a_cov = []
for m in range(4):
    tot = sp.Integer(0)
    for nu in range(4):
        term = sp.diff(u_dn[m], coords[nu])
        for l in range(4):
            term -= Gc[l][nu][m] * u_dn[l]
        tot += u_up[nu] * term
    a_cov.append(tot)
A2c = sum(ginv[i, i] * a_cov[i]**2 for i in range(4))
pt = {t: sp.Rational(2, 10), x: sp.Rational(-3, 10), y: sp.Rational(5, 10), z: sp.Rational(1, 10)}
f = sp.lambdify(eps, A2c.subs(pt), "mpmath")
hs = mp.mpf('1e-6')
c2_exact = (f(hs) - 2 * f(0) + f(-hs)) / (2 * hs**2)          # (1/2) d^2 A^2/deps^2 at eps=0
# truncated machinery on the same concrete functions
Dc = build(Nc, ac, chic)
c2_trunc = mp.mpf(str(sp.N(sp.expand(Dc['A2'].coeff(eps, 2)).subs(pt), 30)))
print("  eps^2 coeff of A^2  exact (finite-diff) =", c2_exact)
print("  eps^2 coeff of A^2  truncated machinery =", c2_trunc)
print("  |difference| =", abs(c2_exact - c2_trunc))
check(abs(c2_exact - c2_trunc) < mp.mpf('1e-9'),
      "exact A^2 (finite-difference) matches the truncated O(eps^2) machinery",
      "the whole eps-expansion pipeline is numerically validated")


# ==================================================================================
hdr("PART D -- the no-go conclusion is unaffected: Z_perp = 2(1-mu) > 0 for mu<1, on FLRW")
# ==================================================================================
print(r"""
  With F'(s) = 2(1-mu(x)) (AQUAL master eq, sf39), the FLRW transverse eigenvalue is
        Z_perp = F'(s0) = 2(1 - mu(x)),   x = g/a0,   UNCHANGED by theta.
  A nontrivial MOND interpolation has mu(x)<1 for all finite x, so Z_perp>0 throughout the MOND
  regime on an expanding background exactly as on a static one: the khronon still propagates (2+1);
  no expansion-induced degeneracy removes it while MOND is active.
""")
for name, muf in [("a0-line", (sp.sqrt(1 + 4 * x**2) - 1) / (2 * x)),
                  ("standard x/sqrt(1+x^2)", x / sp.sqrt(1 + x**2)),
                  ("MS08 1-exp(-x)", 1 - sp.exp(-x))]:
    Zp = 2 * (1 - muf)
    v = float(Zp.subs(x, 1))
    check(v > 0 and sp.limit(Zp, x, sp.oo) == 0,
          f"{name}: Z_perp(FLRW) = 2(1-mu) > 0 for finite x (mu<1), ->0 only as x->oo",
          f"Z_perp(x=1) = {v:.3f}")

# ==================================================================================
hdr("VERDICT")
# ==================================================================================
print(r"""
  SURVIVES on FLRW.
  --------------------------------------------------------------------------------------------
  On g = diag(-N(x)^2, a(t)^2 delta) the khronon congruence has expansion theta = 3 adot/(aN) != 0
  (and shear = 0).  Building the fluctuation acceleration a_mu = u^nu nabla_nu u_mu FULLY
  COVARIANTLY -- the Christoffels Gamma^0_{ij}=a adot delta/N^2 and Gamma^i_{0j}=(adot/a)delta DO
  carry adot -- and forming A^2 = a_mu a^mu to O(chi^2):

     * adot cancels out of EVERY component of a_mu, hence out of the scalar A^2 entirely.
     * the carrier velocity Hessian is unchanged from the static result:
           Z_perp = F'(s0) = 2(1-mu)      (x2, transverse),
           Z_par  = F'(s0) + 2 s0 F''(s0) (longitudinal),
       with no theta-term anywhere;  the chidot^2 (k->0) and chiddot^2 coefficients remain 0.

  WHY (geometric): nabla_mu u_nu decomposes as  -u_mu a_nu + (theta/3) h_mu nu + sigma_mu nu +
  omega_mu nu.  The acceleration a_mu is the u-directed projection; the expansion theta lives in the
  transverse-symmetric trace K = theta.  These are ORTHOGONAL invariants.  A carrier that is a
  function of A^2 = a_mu a^mu alone therefore cannot see theta -- the expansion is a genuinely NEW
  invariant, not a hidden piece of F(A^2).  This is why sf40/sf41 explicitly scoped out
  "shear/expansion invariants": adding one means F(A^2, theta), a DIFFERENT (larger) carrier class.

  CONSEQUENCE: Z_perp = 2(1-mu) > 0 wherever MOND is on (mu<1), on an expanding background exactly as
  on a static one.  The FLRW expansion does NOT open a khronon-removing degeneracy.  The no-go stands
  against this attack.  (The still-open door is the SHEAR sector sigma != 0 -- an anisotropic/Bianchi
  background -- and multi-invariant carriers F(A^2, theta, ...); those are the sf40/sf41 scope
  boundary, untouched here.)
""")
print("=" * 80)
if FAIL:
    print(f"FAILED {len(FAIL)} of {NCHK[0]} checks:")
    for fdesc in FAIL:
        print("   -", fdesc)
    sys.exit(1)
print(f"ALL {NCHK[0]} CHECKS PASSED")
sys.exit(0)
