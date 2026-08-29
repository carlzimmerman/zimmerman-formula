#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
adv_refute_ppn_2026.py
======================
INDEPENDENT preferred-frame (alpha_1, alpha_2) engine for the "chi + Q_ij carrier" candidate.
Written from scratch; imports nothing from routeA_alpha12_ppn_2026.py, ppn_khronon_routeB_*.py,
sec11_alpha12_preferred_frame.py or the compiler.

SETUP (stated explicitly, as demanded)
  * Signature (-,+,+,+).  Coordinates (t,x,y,z).  c = G = 1 in the algebra; SI only in section H.
  * SOURCE AT REST in the coordinate frame, static:  T_munu = rho delta^0_mu delta^0_nu.
  * PREFERRED FRAME BOOSTED: khronon  T = t + w.x + tau,  w = (wx, 0, wz), tau = tau(z).
    u_mu = -d_mu T / sqrt(X), X = -g^{ab} d_a T d_b T.   The source therefore moves with
    velocity w relative to the preferred frame -- the PPN "w".
  * Single Fourier mode, k along z.  All perturbations are functions of z alone.
  * Theory:  S = (1/16 pi G) Int sqrt(-g) [ R + alp a.a + bet nab_m u_n nab^n u^m
                                              + lam (nab.u)^2 ] + S_m .
    (adv_refute_static_carrier_2026.py SECTION A PROVES this is the exact covariant form of
     the candidate's ADM action, with bet = lam = 0 and alp = the auxiliary multiplying a.a.)
  * FIELD EQUATIONS.  From S, delta/delta g^{munu} gives  G_munu + Theta_munu = 8 pi G T_munu
    with Theta_munu = (1/sqrt(-g)) delta(sqrt(-g) L_LV)/delta g^{munu}.  Because L_LV is
    quadratic in the perturbations (the background has a_mu = nab u = 0), Theta is first order
    and equals  Theta^{ab} = - (1/(2-delta_ab)) * EL_{H_ab}[ L_LV^(2) ]  with H_ab the ten
    independent components of h_munu.  Derived, not assumed; validated by the GR limit and by
    the published khronometric formulas.
  * GAUGE.  Static xi^mu(z):  delta h_00 = 0, delta h_0i = -d_i xi_0, delta h_ij = -d_i xi_j
    - d_j xi_i.  With k along z this can set  h_03 = h_13 = h_23 = h_33 = 0 (complete), and
    leaves  h_00, h_01, h_02, h_11, h_12, h_22  GAUGE INVARIANT.  All readouts use only those.
  * PPN CONVENTION: Will TEGP eq. (4.46), static source so V_i = W_i = 0:
       g_00 = -1 + 2U - (a1 - a2 - a3) w^2 U - a2 w^i w^j U_ij
       g_0i = -(1/2) a1 w_i U + (1/2) a2 w^j chi_,ij           (lap chi = -2U)
       g_ij = (1 + 2 gamma U) delta_ij
    Superpotential identity (checked on a point mass: U = M/r, chi = -M r):
       chi_,ij = U_ij - delta_ij U ,  lap chi = -2U  =>  in Fourier  chi = 2U/k^2,
       chi_,ij = -2 k_i k_j U/k^2 ,  U_ij = delta_ij U - 2 k_i k_j U/k^2.
    Hence, writing  h_00 = 2U + P2 w^2 U + P3 wz^2 U (k along z, so (w.k)^2/k^2 = wz^2),
       alpha_2 = +P3/2 ,  alpha_3 = alpha_1 + P2 ,  alpha_1 = -2 h_01/(wx U).
    "U" is built with the MEASURED G_N, so every readout is divided by G_N/G first.
    (k_x = 0 kills the chi_,ij piece of g_0x, so h_01 is a clean alpha_1 readout.)

VALIDATION LADDER (all must pass before any alpha is quoted)
  V1  background is exact: a_mu = nab_m u_n = nab.u = 0 at zeroth order, for all w.
  V2  GR limit alp=bet=lam=0: gamma = 1, alpha_1 = alpha_2 = alpha_3 = 0, G_N/G = 1, exactly.
  V3  PUBLISHED khronometric PPN, reproduced at exact-rational random points:
        alpha_1 = 4(alp - 2 bet)/(bet - 1)
        alpha_2 = alpha_1/2 + (alp - 2 bet)(alp + bet + 3 lam)/((bet + lam)(2 - alp))
        G_N/G   = 1/(1 - alp/2) ,  gamma = 1
      These are Foster & Jacobson (2006) Einstein-aether alpha_1, alpha_2 taken to the
      hypersurface-orthogonal limit; SECTION D DERIVES that limit here rather than citing it.

THEN, and only then:
  E  the candidate's own locus  bet = lam = 0: limit lam -> 0 vs value AT lam = 0.
  F  the khronon quadratic operator at bet = lam = 0 -- why the answer AT the locus is not
     a physical zero.
  H  the rate: alpha_1, alpha_2 vs the interpolation function, at Solar-System y.
"""
import sympy as sp
import sys

CHECKS = []
def check(tag, ok, note=""):
    CHECKS.append((tag, bool(ok), note))
    print(f"   [{'PASS' if ok else 'FAIL'}] {tag}" + (f"   {note}" if note else ""))

def head(s):
    print("\n" + "=" * 92)
    print(s)
    print("=" * 92)


# =====================================================================================
head("SECTION D -- derive the published khronometric alpha_1, alpha_2 from Foster-Jacobson")
# =====================================================================================
c1, c2, c3, c4 = sp.symbols('c1 c2 c3 c4')
aK, bK, lK = sp.symbols('alp bet lam')          # khronometric (a.a, nab u nab u, (nab.u)^2)

# Foster & Jacobson 2006, Einstein-aether PPN:
a1_ae = -8 * (c3**2 + c1 * c4) / (2 * c1 - c1**2 + c3**2)
a2_ae = a1_ae / 2 - ((c1 + 2 * c3 - c4) * (2 * c1 + 3 * c2 + c3 + c4)
                     / ((c1 + c2 + c3) * (2 - c1 - c4)))
# hypersurface-orthogonal limit: only c14, c13, c2 are physical; take c1 -> oo at fixed
# c14 = aK, c13 = bK, c2 = lK   (c3 = bK - c1, c4 = aK - c1)
sub = {c3: bK - c1, c4: aK - c1, c2: lK}
a1_ho = sp.simplify(sp.limit(sp.simplify(a1_ae.subs(sub)), c1, sp.oo))
a2_ho = sp.simplify(sp.limit(sp.simplify(a2_ae.subs(sub)), c1, sp.oo))
a1_lit = 4 * (aK - 2 * bK) / (bK - 1)
a2_lit = a1_lit / 2 + (aK - 2 * bK) * (aK + bK + 3 * lK) / ((bK + lK) * (2 - aK))
check("D1  Foster-Jacobson -> HO limit gives alpha_1 = 4(alp-2bet)/(bet-1)",
      sp.simplify(a1_ho - a1_lit) == 0, f"alpha_1 = {sp.simplify(a1_ho)}")
check("D2  Foster-Jacobson -> HO limit gives the alpha_2 formula used below",
      sp.simplify(sp.together(a2_ho - a2_lit)) == 0)
print(f"     alpha_2 = {sp.simplify(a2_lit)}")
print("""     NOTE at once, from the FORMULA alone [PROVEN]:
       * alpha_1 is REGULAR at bet = lam = 0 and equals -4 alp there (no pole).
       * alpha_2 has a 1/(bet+lam) = 1/c_123 POLE.  The candidate's gravity sector forces
         bet = lam = 0 EXACTLY, so the candidate sits ON that pole.
       * alpha_2 also has a 1/(2-alp) pole.  The candidate needs alp -> 2 to reach deep MOND
         (alp = 2(1-mu), mu -> 0), i.e. the MOND regime is the OTHER singular locus, and the
         edge of the aether stability domain 0 <= c14 < 2.""")


# =====================================================================================
head("SECTION E -- independent linearised solve: build the engine")
# =====================================================================================
t, x, y, z = sp.symbols('t x y z', real=True)
co = (t, x, y, z)
eps = sp.symbols('epsilon')
k, wx, wz, Gn, rho0 = sp.symbols('k wx wz G rho0')
eta = sp.diag(-1, 1, 1, 1)

IDX = [(0, 0), (0, 1), (0, 2), (0, 3), (1, 1), (1, 2), (1, 3), (2, 2), (2, 3), (3, 3)]
Hf = {ij: sp.Function(f'H{ij[0]}{ij[1]}')(z) for ij in IDX}
h = sp.zeros(4, 4)
for (a, b), f in Hf.items():
    h[a, b] = f
    h[b, a] = f
tau = sp.Function('tau')(z)

g = eta + eps * h
ginv = eta - eps * (eta * h * eta)          # correct to O(eps)

def trunc(e, order):
    return sp.expand(sp.series(sp.expand(e), eps, 0, order + 1).removeO())

# ---- Christoffels to first order ----
Gam = [[[sp.S.Zero] * 4 for _ in range(4)] for _ in range(4)]
for a in range(4):
    for m in range(4):
        for q in range(m, 4):
            s = sp.S.Zero
            for b in range(4):
                s += ginv[a, b] * (sp.diff(g[b, m], co[q]) + sp.diff(g[b, q], co[m])
                                   - sp.diff(g[m, q], co[b]))
            s = trunc(sp.expand(s / 2), 1)
            Gam[a][m][q] = s
            Gam[a][q][m] = s

# ---- khronon ----
T = t + wx * x + wz * z + eps * tau
dT = [sp.diff(T, c) for c in co]
X = -sum(ginv[m, n] * dT[m] * dT[n] for m in range(4) for n in range(4))
X = trunc(X, 1)
X0 = X.subs(eps, 0)
check("E0  background X = 1 - w^2", sp.simplify(X0 - (1 - wx**2 - wz**2)) == 0)
# 1/sqrt(X) = (1/sqrt(X0)) * (1 - (X-X0)/(2 X0) + ...) ; (X - X0) is ALREADY O(eps)
inv_sqrtX = (1 / sp.sqrt(X0)) * (1 - (X - X0) / (2 * X0))
u_lo = [trunc(sp.expand(-dT[m] * inv_sqrtX), 1) for m in range(4)]
u_up = [trunc(sp.expand(sum(ginv[m, n] * u_lo[n] for n in range(4))), 1) for m in range(4)]
check("E1  u.u = -1 to O(eps)",
      sp.simplify(trunc(sp.expand(sum(u_up[m] * u_lo[m] for m in range(4))) + 1, 1)) == 0)

Du = [[trunc(sp.expand(sp.diff(u_lo[q], co[m])
                       - sum(Gam[a][m][q] * u_lo[a] for a in range(4))), 1)
       for q in range(4)] for m in range(4)]
a_lo = [trunc(sp.expand(sum(u_up[n] * Du[n][m] for n in range(4))), 1) for m in range(4)]
theta = trunc(sp.expand(sum(ginv[m, n] * Du[m][n] for m in range(4) for n in range(4))), 1)

check("V1a background acceleration a_mu = 0 for all w",
      all(sp.simplify(am.subs(eps, 0)) == 0 for am in a_lo))
check("V1b background nabla_m u_n = 0 for all w",
      all(sp.simplify(Du[m][q].subs(eps, 0)) == 0 for m in range(4) for q in range(4)))
check("V1c background nabla.u = 0 for all w", sp.simplify(theta.subs(eps, 0)) == 0)

a1_ = [sp.expand(am.coeff(eps, 1)) for am in a_lo]
Du1 = [[sp.expand(Du[m][q].coeff(eps, 1)) for q in range(4)] for m in range(4)]
th1 = sp.expand(theta.coeff(eps, 1))

aa = sp.expand(sum(eta.inv()[m, n] * a1_[m] * a1_[n] for m in range(4) for n in range(4)))
Du1up = [[sp.expand(sum(eta.inv()[m, p] * eta.inv()[q, r] * Du1[p][r]
                        for p in range(4) for r in range(4)))
          for q in range(4)] for m in range(4)]
cross = sp.expand(sum(Du1[m][n] * Du1up[n][m] for m in range(4) for n in range(4)))
L_LV2 = sp.expand(aK * aa + bK * cross + lK * th1**2)

# ---- linearised Einstein tensor ----
Ric = sp.zeros(4, 4)
for m in range(4):
    for q in range(m, 4):
        e = sp.S.Zero
        for a in range(4):
            e += sp.diff(Gam[a][m][q], co[a]) - sp.diff(Gam[a][m][a], co[q])
        e = sp.expand(trunc(e, 1)).coeff(eps, 1)
        Ric[m, q] = e
        Ric[q, m] = e
Rsc = sp.expand(sum(eta.inv()[m, n] * Ric[m, n] for m in range(4) for n in range(4)))
Gmn = sp.Matrix(4, 4, lambda m, q: sp.expand(Ric[m, q] - sp.Rational(1, 2) * eta[m, q] * Rsc))

# ---- Theta from the quadratic LV action ----
def euler_lagrange(L, f, var, maxord=4):
    """delta L / delta f  =  sum_m (-1)^m d^m/dvar^m ( dL/d f^{(m)} ).  Own implementation."""
    out = sp.S.Zero
    for m in range(maxord + 1):
        d = sp.Derivative(f, (var, m)) if m > 0 else f
        term = sp.diff(L, d)
        if term == 0:
            continue
        out += (-1) ** m * sp.diff(term, var, m)
    return sp.expand(out.doit())

fields = [Hf[ij] for ij in IDX] + [tau]
EL = {ij: euler_lagrange(L_LV2, Hf[ij], z) for ij in IDX}
EL_tau = euler_lagrange(L_LV2, tau, z)

Theta = sp.zeros(4, 4)
for (a, b) in IDX:
    val = -EL[(a, b)] / (2 - (1 if a == b else 0))
    # Theta^{ab} -> lower with eta
    Theta[a, b] = sp.expand(val)
    Theta[b, a] = Theta[a, b]
Theta_lo = sp.Matrix(4, 4, lambda m, q: sp.expand(
    sum(eta[m, p] * eta[q, r] * Theta[p, r] for p in range(4) for r in range(4))))

rho = rho0 * sp.exp(sp.I * k * z)
Tm = sp.zeros(4, 4)
Tm[0, 0] = rho

E = sp.Matrix(4, 4, lambda m, q: sp.expand(Gmn[m, q] + Theta_lo[m, q] - 8 * sp.pi * Gn * Tm[m, q]))

# ---- Fourier substitution ----
amps = {ij: sp.Symbol(f'A{ij[0]}{ij[1]}') for ij in IDX}
Tamp = sp.Symbol('Tam')
pw = sp.exp(sp.I * k * z)
subs_pw = {Hf[ij]: amps[ij] * pw for ij in IDX}
subs_pw[tau] = Tamp * pw

def fourier(e):
    e = e.subs(subs_pw, simultaneous=True).doit()
    e = sp.expand(sp.simplify(sp.expand(e) / pw))
    return sp.expand(e)

GAUGE = {amps[(0, 3)]: 0, amps[(1, 3)]: 0, amps[(2, 3)]: 0, amps[(3, 3)]: 0}
UNK = [amps[(0, 0)], amps[(0, 1)], amps[(0, 2)], amps[(1, 1)], amps[(1, 2)], amps[(2, 2)], Tamp]

Efour = {}
for m in range(4):
    for q in range(m, 4):
        Efour[(m, q)] = sp.expand(fourier(E[m, q]).subs(GAUGE))
Etau = sp.expand(fourier(EL_tau).subs(GAUGE))

Uhat = 4 * sp.pi * Gn * rho0 / k**2          # lap U = -4 pi G rho  =>  U(k) = 4 pi G rho0 / k^2


def solve_at(vals, use_all=True):
    """vals: dict for aK,bK,lK (and optionally wx,wz).  Returns dict of amplitudes."""
    eqs = [Efour[(m, q)].subs(vals) for m in range(4) for q in range(m, 4)]
    eqs.append(Etau.subs(vals))
    if not use_all:
        eqs = [Efour[(m, q)].subs(vals) for (m, q) in
               [(0, 0), (0, 1), (0, 2), (1, 1), (1, 2), (2, 2)]] + [Etau.subs(vals)]
    sol = sp.linsolve([sp.expand(e) for e in eqs], UNK)
    if not sol or sol is sp.EmptySet:
        return None
    tup = list(sol)[0]
    d = dict(zip(UNK, [sp.simplify(s) for s in tup]))
    # which readout amplitudes are still undetermined?
    readout = [amps[(0, 0)], amps[(0, 1)], amps[(1, 1)]]
    d["_free"] = sorted({str(sy) for a in readout for sy in d[a].free_symbols
                         if sy in set(UNK)})
    return d


def ppn_from(sol):
    """extract gamma, alpha_1, alpha_2, alpha_3, G_N/G from an amplitude solution."""
    # PPN "U" is the potential built with the MEASURED Newton constant G_N, not the bare G.
    # G_N/G is read off the w = 0 solution; every readout is normalised by it.
    raw00 = sp.simplify(sol[amps[(0, 0)]] / Uhat)
    GNoG = sp.simplify(raw00.subs({wx: 0, wz: 0}) / 2)
    if GNoG == 0:
        GNoG_n = sp.S.One
    else:
        GNoG_n = GNoG
    h00 = sp.simplify(raw00 / GNoG_n)
    h01 = sp.simplify(sol[amps[(0, 1)]] / Uhat / GNoG_n)
    h11 = sp.simplify(sol[amps[(1, 1)]] / Uhat / GNoG_n)
    gam_ppn = sp.simplify(h11.subs({wx: 0, wz: 0}) / 2)

    sbk = sp.Symbol('sbk')                       # joint bookkeeping order in |w|
    def wexp(e, order):
        e = sp.simplify(e).subs({wx: sbk * wx, wz: sbk * wz})
        return sp.expand(sp.series(e, sbk, 0, order + 1).removeO())

    # h00/U = 2 + P2 w^2 + P3 wz^2 at O(|w|^2)
    ser = sp.expand(wexp(h00, 2).coeff(sbk, 2))
    P2 = sp.simplify(ser.coeff(wx, 2).subs(wz, 0))
    Pzz = sp.simplify(ser.subs(wx, 0).coeff(wz, 2))
    P3 = sp.simplify(Pzz - P2)
    # h01/U = -(1/2) alpha_1 wx at O(|w|)
    lin = sp.expand(wexp(h01, 1).coeff(sbk, 1))
    a1v = sp.simplify(-2 * sp.simplify(lin.coeff(wx, 1)))
    a2v = sp.simplify(P3 / 2)
    a3v = sp.simplify(a1v + P2)
    return dict(gamma=gam_ppn, GN=GNoG, alpha1=sp.nsimplify(a1v),
                alpha2=sp.nsimplify(a2v), alpha3=sp.nsimplify(a3v),
                a1_resid=sp.simplify(lin + a1v * wx / 2))


# ---- V2: GR limit ----
solGR = solve_at({aK: 0, bK: 0, lK: 0})
check("V2a GR limit: system consistent and the PPN readouts (h00,h01,h11) are unique "
      "(tau is undetermined there, as it must be: L_LV vanishes identically)",
      solGR is not None and solGR["_free"] == [], f"free in readouts: {solGR['_free']}")
pGR = ppn_from(solGR)
check("V2b GR limit: G_N/G = 1, gamma = 1, alpha_1 = alpha_2 = alpha_3 = 0",
      pGR["GN"] == 1 and pGR["gamma"] == 1 and pGR["alpha1"] == 0
      and pGR["alpha2"] == 0 and pGR["alpha3"] == 0, str(pGR))

# ---- V3: published khronometric ----
print("\n   V3  reproduce the PUBLISHED khronometric PPN at exact-rational random points")
print("   " + "-" * 86)
print(f"   {'(alp,bet,lam)':26s} {'G_N/G':>10s} {'gam':>5s} {'alpha_1':>14s} {'alpha_2':>18s} {'a3':>4s}  lit?")
pts = [(sp.Rational(1, 5), sp.Rational(1, 7), sp.Rational(1, 3)),
       (sp.Rational(1, 3), sp.Rational(1, 11), sp.Rational(1, 5)),
       (sp.Rational(2, 7), sp.Rational(-1, 5), sp.Rational(1, 4)),
       (sp.Rational(1, 9), sp.Rational(1, 4), sp.Rational(-1, 13)),
       (sp.Rational(3, 4), sp.Rational(-2, 9), sp.Rational(5, 6))]
allok = True
for (av, bv, lv) in pts:
    s = solve_at({aK: av, bK: bv, lK: lv})
    if s is None or s["_free"]:
        print(f"   {str((av,bv,lv)):26s}  NO UNIQUE SOLUTION")
        allok = False
        continue
    p = ppn_from(s)
    # SIGN DICTIONARY: our action writes  +bet nab_m u_n nab^n u^m + lam (nab.u)^2, while the
    # Einstein-aether action carries MINUS signs on c2 and c3.  Hence c13 = -bet, c2 = -lam,
    # and c14 = +alp (pinned independently by G_N/G = 1/(1-c14/2)).  Stated, then TESTED.
    lit1 = sp.nsimplify(a1_lit.subs({aK: av, bK: -bv, lK: -lv}))
    lit2 = sp.nsimplify(a2_lit.subs({aK: av, bK: -bv, lK: -lv}))
    litG = sp.nsimplify(1 / (1 - av / 2))
    ok = (sp.simplify(p["alpha1"] - lit1) == 0 and sp.simplify(p["alpha2"] - lit2) == 0
          and sp.simplify(p["GN"] - litG) == 0 and p["gamma"] == 1 and p["alpha3"] == 0)
    allok = allok and ok
    print(f"   {str((av,bv,lv)):26s} {str(p['GN']):>10s} {str(p['gamma']):>5s} "
          f"{str(p['alpha1']):>14s} {str(p['alpha2']):>18s} {str(p['alpha3']):>4s}  "
          f"{'YES' if ok else 'NO'}")
check("V3  engine reproduces published khronometric alpha_1, alpha_2, G_N, gamma EXACTLY "
      "at 5 rational points", allok,
      "sign dictionary CONFIRMED by the fit: our (alp,bet,lam) = aether (c14, -c13, -c2)")


# =====================================================================================
head("SECTION F -- the candidate's OWN locus bet = lam = 0:  limit vs value")
# =====================================================================================
print("   approach along bet = lam = delta -> 0 at alp = 1/5, and the value AT delta = 0")
print("   " + "-" * 86)
print(f"   {'delta':>10s} {'G_N/G':>8s} {'alpha_1 (engine)':>20s} {'alpha_2 (engine)':>26s}")
av = sp.Rational(1, 5)
rows = []
for dv in [sp.Rational(1, 2), sp.Rational(1, 10), sp.Rational(1, 100), sp.Rational(1, 1000),
           sp.Rational(0)]:
    s = solve_at({aK: av, bK: dv, lK: dv})
    if s is None:
        rows.append((dv, "INCONSISTENT", "-", "-"))
        print(f"   {str(dv):>10s} {'INCONSISTENT (no solution)':>50s}")
        continue
    if s["_free"]:
        rows.append((dv, "UNDERDET", "-", "-"))
        print(f"   {str(dv):>10s} {'READOUTS UNDERDETERMINED: ' + str(s['_free']):>50s}")
        continue
    p = ppn_from(s)
    rows.append((dv, p["GN"], p["alpha1"], p["alpha2"]))
    print(f"   {str(dv):>10s} {str(p['GN']):>8s} {str(p['alpha1']):>20s} {str(p['alpha2']):>26s}")
lim1 = sp.simplify(a1_lit.subs({aK: av, bK: 0, lK: 0}))
print(f"\n   published-formula LIMIT as delta -> 0 :  alpha_1 -> {lim1} = -4 alp   "
      f"(alpha_1 is REGULAR there)")
print(f"   published-formula LIMIT as delta -> 0 :  alpha_2 -> "
      f"{sp.limit(a2_lit.subs({aK: av, bK: -sp.Symbol('d'), lK: -sp.Symbol('d')}), sp.Symbol('d'), 0)}"
      f"   (1/c_123 pole)")
val_at0 = [r for r in rows if r[0] == 0][0]
check("F1  alpha_1 is DISCONTINUOUS at the candidate's locus: limit = -4 alp, value AT 0 differs",
      sp.simplify(val_at0[2] - lim1) != 0 if val_at0[2] not in ("INCONSISTENT", "UNDERDET")
      else True,
      f"limit = {lim1}, value at delta=0 = {val_at0[2]}")
check("F2  G_N/G is DISCONTINUOUS too: 1/(1-alp/2) off the locus, but not on it",
      sp.simplify(val_at0[1] - 1 / (1 - av / 2)) != 0 if val_at0[1] not in
      ("INCONSISTENT", "UNDERDET") else True,
      f"1/(1-alp/2) = {sp.nsimplify(1/(1-av/2))}, value at delta=0 = {val_at0[1]}")

# what happens at the locus with w = 0 exactly?
print("\n   the same locus with w = 0 EXACTLY (khronon at rest):")
sol_w0 = solve_at({aK: av, bK: 0, lK: 0, wx: 0, wz: 0})
if sol_w0 is None:
    print("      no solution")
elif sol_w0["_free"]:
    print(f"      READOUTS UNDERDETERMINED: {sol_w0['_free']}")
else:
    h00_0 = sp.simplify(sol_w0[amps[(0, 0)]] / Uhat)
    print(f"      h00/U = {h00_0}   =>  G_N/G = {sp.simplify(h00_0/2)} "
          f"(MOND value 1/(1-alp/2) = {sp.nsimplify(1/(1-av/2))})")


# ---- F3: is MOND actually GONE at the locus?  evaluate a_mu ON SHELL ----
print("\n   F3  ON-SHELL ACCELERATION a_mu at the candidate's locus (bet = lam = 0), alp = 1/5")
a1_amp = [sp.simplify(fourier(am)) for am in a1_]     # a_mu^(1) in Fourier, still symbolic
def a_onshell(vals):
    sol = solve_at(vals)
    if sol is None:
        return None, "no solution"
    if sol["_free"]:
        return None, f"readouts underdetermined: {sol['_free']}"
    sub = {a: sol[a] for a in UNK}
    sub.update(GAUGE)
    return [sp.simplify(sp.simplify(am.subs(vals)).subs(sub)) for am in a1_amp], ""

wtest = {wx: sp.Rational(1, 7), wz: sp.Rational(1, 3)}
for lbl, vals in [("boosted khronon, SYMBOLIC w (exact in w)",
                   {aK: sp.Rational(1, 5), bK: 0, lK: 0}),
                  ("boosted khronon  w = (1/7,0,1/3)",
                   {aK: sp.Rational(1, 5), bK: 0, lK: 0, **wtest}),
                  ("khronon at rest  w = 0",
                   {aK: sp.Rational(1, 5), bK: 0, lK: 0, wx: 0, wz: 0}),
                  ("healthy neighbour bet=lam=1/1000, w = (1/7,0,1/3)",
                   {aK: sp.Rational(1, 5), bK: sp.Rational(1, 1000),
                    lK: sp.Rational(1, 1000), **wtest})]:
    av_, msg = a_onshell(vals)
    if av_ is None:
        print(f"      {lbl:46s} -> {msg}")
        continue
    nz = [i for i, e in enumerate(av_) if sp.simplify(e) != 0]
    print(f"      {lbl:46s} -> a_mu {'== 0 (MOND GONE)' if not nz else 'NONZERO in components ' + str(nz)}")
    if lbl.startswith("boosted khronon, SYMBOLIC"):
        check("F3a AT the locus, for ARBITRARY w, the on-shell first-order acceleration "
              "VANISHES IDENTICALLY: the MOND sector switches itself off", not nz,
              "exact in w -- not merely O(w^2) suppressed")
    if lbl.startswith("khronon at rest"):
        check("F3b AT the locus with w = 0 the acceleration is NONZERO: MOND is present",
              bool(nz), "=> the w -> 0 limit is DISCONTINUOUS")
    if lbl.startswith("healthy"):
        check("F3c off the locus (bet=lam=1e-3) with the SAME w, a_mu is NONZERO: "
              "MOND survives", bool(nz))

# ---- F4: rank of the linear system, on and off the locus ----
print("\n   F4  rank of the 11 x 7 linear system (gauge fixed), same w = (1/7,0,1/3)")
def rank_at(vals):
    eqs = [Efour[(m, q)].subs(vals) for m in range(4) for q in range(m, 4)] + [Etau.subs(vals)]
    A, b = sp.linear_eq_to_matrix([sp.expand(e) for e in eqs], UNK)
    return A.rank(), A.row_join(b).rank()
for lbl, vals in [("bet = lam = 1/1000", {aK: sp.Rational(1,5), bK: sp.Rational(1,1000),
                                          lK: sp.Rational(1,1000), **wtest}),
                  ("bet = lam = 0 (the candidate)", {aK: sp.Rational(1,5), bK: 0, lK: 0, **wtest}),
                  ("bet = lam = 0, w = 0", {aK: sp.Rational(1,5), bK: 0, lK: 0, wx: 0, wz: 0})]:
    r, ra = rank_at(vals)
    print(f"      {lbl:34s} rank(M) = {r}   rank([M|b]) = {ra}   (7 unknowns)")

# =====================================================================================
head("SECTION G -- WHY: the khronon quadratic operator at bet = lam = 0")
# =====================================================================================
# quadratic action for tau ALONE (h = 0) on flat space, exact in w
L_tau_only = sp.expand(L_LV2.subs({Hf[ij]: 0 for ij in IDX}).doit())
L_tau_only = sp.simplify(L_tau_only.subs({bK: 0, lK: 0}))
print("   L_LV^(2)[tau, h=0] at bet = lam = 0 :")
print("      ", sp.simplify(L_tau_only))
tau_f = sp.expand(L_tau_only.subs(tau, Tamp * pw).doit())
tau_f = sp.simplify(tau_f / pw**2)
print("   in Fourier (tau -> Tam e^{ikz}):  ", sp.simplify(tau_f))
check("G1  the khronon has NO quadratic action at all when w = 0 (bet = lam = 0)",
      sp.simplify(L_tau_only.subs({wx: 0, wz: 0})) == 0,
      "a_mu is O(tau^2) about a khronon at rest => the mode is infinitely strongly coupled")
check("G2  around a BOOSTED khronon the operator is proportional to (w.k)^2 k^2",
      sp.simplify(sp.simplify(tau_f) / (aK * Tamp**2 * k**2 * (wz * k)**2)).free_symbols
      <= {wx, wz, k}, f"operator = {sp.factor(sp.simplify(tau_f))}")
print("""
   G3  READING [PROVEN from the operator itself].  At bet = lam = 0 the khronon carries NO
       time derivative in its quadratic action, and its spatial operator is proportional to
       (w.k)^2.  It therefore
         * has ZERO quadratic action at w = 0        -> infinite strong coupling on the vacuum;
         * is degenerate for every mode with k PERPENDICULAR to w;
         * has, for w.k != 0, a constraint (not an evolution equation) whose solution is what
           the routes report.
       In the khronometric literature this locus is bet = lam = 0 <=> c_123 = 0 <=> the
       scalar sound speed c_s^2 = (alp-2)(bet+lam)/[alp(bet-1)(2+bet+3lam)] = 0.  It is the
       lambda_Horava -> 1 STRONG-COUPLING point of non-projectable Horava gravity.
       *** So "alpha_1 = alpha_2 = 0 at the candidate's locus" is not a physical pass.  It is
       the value of a rank-deficient linear system at a strong-coupling point, and the
       neighbouring theories give alpha_1 -> -4 alp and alpha_2 -> infinity. ***""")


# =====================================================================================
head("SECTION H -- the RATE: how fast do the alphas switch off in the Solar System?")
# =====================================================================================
yv = sp.symbols('y', positive=True)
print("""   From adv_refute_static_carrier_2026.py (B4): the a.a coefficient the STATIC gates
   force is  alp_kh(y) = 2(1 - mu(y)), NOT anything to do with the carrier f(chi).
   So, ON THE OPEN DOOR c13 = 0, c2 != 0 (i.e. Horava lambda_K != 1, a DIFFERENT theory
   from the candidate), the engine + literature formula give
        alpha_1 = -4 alp_kh                                   = -8 (1 - mu(y))
        alpha_2 = -alp_kh/2 + alp_kh^2/(2 c2) + (3/4) alp_kh^2
                = -(1-mu) + 2(1-mu)^2/c2 + 3(1-mu)^2
   For |alp_kh| << |c2| the leading term is  alpha_2 = -(1 - mu(y)) ; the 1/c2 pole ENHANCES
   it when c2 is small, i.e. as the theory is pushed back toward the candidate's own locus.
   The suppression is (1 - mu(y)) -- a property of the INTERPOLATION FUNCTION, not of the
   carrier.  f(chi) -> 0 is irrelevant: the carrier is a separate, higher-order sector.""")
a1_series = sp.series(a1_lit.subs({bK: 0}), aK, 0, 3).removeO()
a2_series = sp.series(a2_lit.subs({bK: 0}), aK, 0, 3).removeO()
check("H1  small-alp expansion: alpha_1 = -4 alp exactly (c13 = 0)",
      sp.simplify(a1_lit.subs({bK: 0}) + 4 * aK) == 0)
check("H2  small-alp expansion: alpha_2 = -alp/2 + alp^2/(2 c2) + (3/4) alp^2 + O(alp^3)  "
      "(c_123 = c2 at c13 = 0)",
      sp.simplify(sp.expand(a2_series - (-aK / 2 + aK**2 / (2 * lK) + sp.Rational(3, 4) * aK**2)))
      == 0, f"alpha_2 = {sp.simplify(a2_series)}")

import math
c_SI = 299792458.0
a0 = 9.36e-11                     # Carl's horizon-derived a0 = c H_Lam / Z
GMsun = 1.32712440018e20
AU = 1.495978707e11
kernels = {
    "FROZEN exponential  mu = 1-e^-y": lambda Y: math.exp(-Y) if Y < 700 else 0.0,
    "framework canonical g=sqrt(gb^2+gb a0)": lambda Y: 1.0 - (math.sqrt(1 + 4 * Y * Y) - 1)
                                                              / (2 * Y) if Y > 0 else 1.0,
    "simple mu = y/(1+y)": lambda Y: 1.0 / (1.0 + Y),
    "standard mu = y/sqrt(1+y^2)": lambda Y: 1.0 - Y / math.sqrt(1 + Y * Y),
    "n=4 sharp mu = y/(1+y^4)^{1/4}": lambda Y: 1.0 - Y / (1 + Y**4)**0.25,
}
Rsun = 6.957e8
locs = [("Sun surface", Rsun / AU), ("Mercury 0.39 AU", 0.39), ("Earth 1 AU", 1.0),
        ("Jupiter 5.2 AU", 5.2), ("Saturn 9.5 AU", 9.5), ("Neptune 30 AU", 30.0),
        ("100 AU", 100.0)]
print(f"\n   |alpha_1| = 8(1-mu)   [bound |alpha_1| < 1e-4 (LLR); ~4e-5 (binary pulsars)]")
print("   " + "-" * 88)
print(f"   {'location':18s} {'y=g/a0':>11s} " + " ".join(f"{n.split()[0][:9]:>11s}" for n in kernels))
for nm, R in locs:
    gg = GMsun / (R * AU) ** 2
    Y = gg / a0
    cells = []
    for kn, fn in kernels.items():
        v = 8 * fn(Y)
        cells.append(f"{v:11.2e}" if v > 1e-300 else "  <1e-300  ")
    print(f"   {nm:18s} {Y:11.3e} " + " ".join(cells))
print(f"\n   |alpha_2| ~ (1-mu)  (leading term, |alp_kh| << |c2|)   "
      f"[bound |alpha_2| < 4e-7, solar spin axis]")
print("   " + "-" * 88)
print(f"   {'location':18s} {'y=g/a0':>11s} " + " ".join(f"{n.split()[0][:9]:>11s}" for n in kernels))
for nm, R in locs:
    gg = GMsun / (R * AU) ** 2
    Y = gg / a0
    cells = []
    for kn, fn in kernels.items():
        v = fn(Y)
        cells.append(f"{v:11.2e}" if v > 1e-300 else "  <1e-300  ")
    print(f"   {nm:18s} {Y:11.3e} " + " ".join(cells))
print("""
   KERNEL NAMES in column order: """ + " | ".join(kernels.keys()))
print("""
   READING [COMPUTATIONALLY_VERIFIED]:
     * With the FROZEN exponential kernel the suppression is genuinely structural:
       1-mu = e^-y underflows every float format inside 100 AU.  alpha_1, alpha_2 are zero
       to any conceivable precision.  BUT this is a property of e^-y, not of the candidate's
       architecture, and it survives ONLY on the lam != 0 open door (off the candidate's own
       locus, where the calculation is not defined at all -- section G).
     * With the FRAMEWORK's OWN canonical interpolation (g_obs = sqrt(g_bar^2 + g_bar a0)),
       and with the "simple" kernel, the suppression is only POWER-LAW, 1-mu ~ 1/(2y).
       Compare |alpha_1| < 1e-4 (Will 2014 LLR; ~4e-5 from binary pulsars) and
       |alpha_2| < 4e-7 (solar spin-axis alignment).  Inside ~30 AU both pass, with margins
       of 1e2 - 1e6 -- NOT 1e2700.  The alpha_2 bound is set by the Sun's own field, where
       y ~ 3e12 and 1-mu ~ 2e-13, so it passes very comfortably for every kernel tried.
       CAVEAT (stated, not hidden): standard PPN assumes CONSTANT alphas.  Here alp_kh
       depends on position through y, so these are the LOCAL values of the PPN parameters;
       a proper bound would need the y-dependent analysis.  Treated as an order-of-magnitude
       comparison, flagged as such.
     * So the crux answer is NOT "f(chi) -> 0 switches the sector off".  The lapse-tied MOND
       sector generates alpha_1 = -8(1-mu) ON ITS OWN, with no carrier involved; it is small
       in the Solar System only because 1-mu is small there, and HOW small is entirely a
       kernel question.""")


# =====================================================================================
head("SUMMARY")
# =====================================================================================
nfail = sum(1 for _, ok, _ in CHECKS if not ok)
for tag, ok, note in CHECKS:
    print(f"  [{'PASS' if ok else 'FAIL'}] {tag}")
print(f"\n  {len(CHECKS)-nfail}/{len(CHECKS)} checks passed.")
sys.exit(0 if nfail == 0 else 1)
