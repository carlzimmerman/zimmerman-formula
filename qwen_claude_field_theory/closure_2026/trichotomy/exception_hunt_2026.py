#!/usr/bin/env python3
"""
TRICHOTOMY EXCEPTION HUNT — adversarial construction pass (2026-08-31).

QUESTION (Layer C): can a scalar functional q[g] of the metric ALONE give a0(z) ~ H(z)
inside bound systems with (i) no new propagating DOF, (ii) no independent Cauchy data,
(iii) no conserved dark charge?

This script sympy-verifies the load-bearing curvature facts behind five candidate
constructions and one genuine near-escape:

  CHECK 1  (Leg A, local invariants): Schwarzschild-de Sitter — R = 4*Lambda exactly,
           R_mn R^mn = 4*Lambda^2; the ONLY invariant carrying M is Weyl-type
           (Kretschmann ~ 48 M^2/r^6). H(z) appears in NO local invariant. Combined
           with the Einstein-Straus vacuole (interior EXACTLY SdS at all orders), Leg A
           closes EXACTLY, not approximately: even the infinite jet is H-blind.

  CHECK 2  (McVittie resolution): McVittie DOES have R reading H at every radius — but
           the computation shows WHY it is not a counterexample: G_munu forces a fluid
           with homogeneous rho = 3H^2/8piG filling the bound region and an
           r-DEPENDENT pressure p(r,t) ~ -(3H^2 + 2*Hdot*(1+mu)/(1-mu))/8pi that
           diverges at the lapse zero. The H-signal in local curvature is carried
           point-by-point by T_munu != 0: a cosmological medium penetrating the bound
           system = the dark-fluid leg in disguise. (Also: R = 12H^2 + 6*Hdot*(1+mu)/(1-mu),
           NOT 12H^2+6Hdot at every radius — the naive claim is corrected here.)

  CHECK 3  (Leg C, foliation-dependence of K, adversarial vs the CMC escape): the SAME
           de Sitter spacetime carries K = 0 (static slicing) and K = 3H (flat FLRW
           slicing) — BOTH constant-mean-curvature. So in the Lambda-dominated regime
           CMC foliations are NON-UNIQUE (the classical CMC-uniqueness theorems assume
           the timelike convergence condition R_mn t^m t^n >= 0, violated when Lambda
           dominates). The 'CMC-K reads H with no Cauchy data' escape therefore still
           carries a global foliation-SELECTION datum precisely in the DE era.

  CHECK 4  (Global averages / sequestering): <R> = int sqrt(-g) R / int sqrt(-g) over
           ALL of a LCDM history converges to 4*Lambda (future dS volume dominates).
           A global average is ONE number for the whole spacetime: it is constant BY
           CONSTRUCTION — Layer A at best, and teleological (future-dominated) anyway.
           Truncating the average at 'now' requires a slice (Leg C) or the past
           lightcone (Leg B, in-in localization -> field).

  CHECK 5  (small causal diamonds): any functional of a causal diamond of size ell
           reduces, as ell -> 0, to the metric jet at its center (Riemann-normal
           expansion) = Leg A; verified here at leading order via the geodesic-ball
           volume deficit coefficient (Vol = V_flat*(1 - R*ell^2/(...)) on a static
           slice reads LOCAL R). A Hubble-sized diamond anchored in a bound system
           extends across the vacuole = Legs B/C by support.

VERDICT PRINTED AT END. No claim here is a scaling estimate; every equation is
computed by sympy or by explicit quadrature.
"""

import sympy as sp

t, r, th, M, L, H0 = sp.symbols('t r theta M Lambda H_0', positive=True)
results = []

def check(name, cond):
    ok = bool(cond)
    results.append((name, ok))
    print(('PASS' if ok else 'FAIL') + '  ' + name)
    return ok

# ---------- curvature machinery (diagonal-friendly, general) ----------
def christoffel(g, x):
    n = len(x); ginv = g.inv()
    Gam = [[[0]*n for _ in range(n)] for _ in range(n)]
    for l in range(n):
        for i in range(n):
            for j in range(i, n):
                expr = sum(ginv[l, s]*(sp.diff(g[s, i], x[j]) + sp.diff(g[s, j], x[i])
                                       - sp.diff(g[i, j], x[s])) for s in range(n))/2
                expr = sp.together(expr)
                Gam[l][i][j] = expr; Gam[l][j][i] = expr
    return Gam

def ricci_tensor(g, x):
    n = len(x); Gam = christoffel(g, x)
    Ric = sp.zeros(n, n)
    for i in range(n):
        for j in range(i, n):
            e = 0
            for l in range(n):
                e += sp.diff(Gam[l][i][j], x[l]) - sp.diff(Gam[l][i][l], x[j])
                for s in range(n):
                    e += Gam[l][l][s]*Gam[s][i][j] - Gam[l][j][s]*Gam[s][i][l]
            e = sp.simplify(sp.together(e))
            Ric[i, j] = e; Ric[j, i] = e
    return Ric

def riemann_down(g, x):
    n = len(x); Gam = christoffel(g, x)
    Rup = [[[[0]*n for _ in range(n)] for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for b in range(n):
            for c in range(n):
                for d in range(n):
                    e = sp.diff(Gam[a][b][d], x[c]) - sp.diff(Gam[a][b][c], x[d])
                    for s in range(n):
                        e += Gam[a][c][s]*Gam[s][b][d] - Gam[a][d][s]*Gam[s][b][c]
                    Rup[a][b][c][d] = sp.simplify(sp.together(e))
    Rdn = [[[[0]*n for _ in range(n)] for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for b in range(n):
            for c in range(n):
                for d in range(n):
                    Rdn[a][b][c][d] = sp.simplify(sum(g[a, s]*Rup[s][b][c][d] for s in range(n)))
    return Rdn

# =====================================================================
print('=' * 76)
print('CHECK 1: Schwarzschild-de Sitter local invariants (Leg A)')
print('=' * 76)
x = [t, r, th, sp.Symbol('phi')]
f = 1 - 2*M/r - L*r**2/3
gSdS = sp.diag(-f, 1/f, r**2, r**2*sp.sin(th)**2)
Ric = ricci_tensor(gSdS, x)
ginv = gSdS.inv()
R_scalar = sp.simplify(sum(ginv[i, i]*Ric[i, i] for i in range(4)))
RmnRmn = sp.simplify(sum(ginv[i, i]*ginv[j, j]*Ric[i, j]**2 for i in range(4) for j in range(4)))
print('R          =', R_scalar)
print('R_mn R^mn  =', RmnRmn)
check('SdS: R = 4*Lambda exactly (M absent)', sp.simplify(R_scalar - 4*L) == 0)
check('SdS: R_mn R^mn = 4*Lambda^2 (M absent)', sp.simplify(RmnRmn - 4*L**2) == 0)

Rdn = riemann_down(gSdS, x)
Kret = 0
for a in range(4):
    for b in range(4):
        for c in range(4):
            for d in range(4):
                Kret += ginv[a, a]*ginv[b, b]*ginv[c, c]*ginv[d, d]*Rdn[a][b][c][d]**2
Kret = sp.simplify(Kret)
print('Kretschmann =', Kret)
check('SdS: Kretschmann = 8*L^2/3 + 48*M^2/r^6 (M only via Weyl)',
      sp.simplify(Kret - (sp.Rational(8, 3)*L**2 + 48*M**2/r**6)) == 0)
print("""
  CONSEQUENCE: inside an Einstein-Straus vacuole the metric is EXACTLY SdS, so every
  local invariant, to ALL derivative orders, is a function of (M, Lambda, r) only.
  H(z) of the exterior FLRW is not encoded at any jet order -> Leg A closes EXACTLY.
  A Ricci-only functional (construction c) is worse: Ricci = Einstein-algebraic in
  LOCAL T_munu + Lambda, so it reads either the constant Lambda (Layer A) or the local
  density (environment-dependent a0 -> SPARC environmental-fork null, 13-34 sigma
  pipeline standing).""")

# =====================================================================
print('=' * 76)
print('CHECK 2: McVittie — the H-reading is carried by a local medium (resolution)')
print('=' * 76)
a = sp.Function('a', positive=True)(t)
mu = M/(2*a*r)
A2 = ((1 - mu)/(1 + mu))**2
B2 = a**2*(1 + mu)**4
gMcV = sp.diag(-A2, B2, B2*r**2, B2*r**2*sp.sin(th)**2)
RicM = ricci_tensor(gMcV, x)
ginvM = gMcV.inv()
RM = sp.simplify(sum(ginvM[i, i]*RicM[i, i] for i in range(4)))
H = sp.diff(a, t)/a
Hdot = sp.diff(H, t)
RM_target = 12*H**2 + 6*Hdot*(1 + mu)/(1 - mu)
check('McVittie: R = 12 H^2 + 6 Hdot (1+mu)/(1-mu)  [NOT 12H^2+6Hdot at every r]',
      sp.simplify(sp.together(RM - RM_target)) == 0)

# Einstein tensor mixed components -> the forced fluid
Gmix = sp.zeros(4, 4)
for i in range(4):
    for j in range(4):
        Gmix[i, j] = sp.simplify(ginvM[i, i]*(RicM[i, j] - sp.Rational(1, 2)*gMcV[i, j]*RM))
rho = sp.simplify(-Gmix[0, 0])          # 8 pi G rho = -G^t_t
p_r = sp.simplify(Gmix[1, 1])           # 8 pi G p   =  G^r_r
flux = sp.simplify(RicM[0, 1])          # G_tr ~ R_tr here (g_tr=0)
print('8piG rho   =', rho)
print('8piG p(r)  =', sp.simplify(p_r))
check('McVittie: rho = 3H^2/8piG homogeneous (r-independent) -> medium fills the bound region',
      sp.simplify(rho - 3*H**2) == 0)
check('McVittie: pressure is r-DEPENDENT (dp/dr != 0 unless Hdot=0)',
      sp.simplify(sp.diff(sp.simplify(p_r + 3*H**2 + 2*Hdot*(1+mu)/(1-mu)), r)) == 0
      and sp.simplify(sp.diff(p_r, r)) != 0)
check('McVittie: no radial energy flux (G_tr = 0) — the medium is hand-arranged, not accreting',
      flux == 0)
print("""
  RESOLUTION: R reads H at small r ONLY because Einstein's equations FORCE
  T_munu != 0 there: a homogeneous-density fluid with a tuned inhomogeneous pressure
  penetrates the 'bound' region (and p diverges at mu->1). Remove the medium
  (Einstein-Straus: T=0 in the vacuole) and the H-reading vanishes identically.
  McVittie is the dark-fluid leg in disguise. QED.""")

# =====================================================================
print('=' * 76)
print('CHECK 3: K is foliation data — de Sitter carries TWO CMC foliations (adversarial)')
print('=' * 76)
# (a) static patch: g = diag(-(1-H^2 r^2), 1/(1-H^2 r^2), r^2, r^2 sin^2) — time-symmetric
#     zero shift, time-independent spatial metric  =>  K_ij = (1/2N) d_t g_ij = 0.
gstat_spatial_timederiv = [sp.diff(e, t) for e in
                           [1/(1 - H0**2*r**2), r**2, r**2*sp.sin(th)**2]]
check('dS static slicing: K_ij = (1/2N) dt g_ij = 0  =>  K = 0 (a CMC foliation)',
      all(e == 0 for e in gstat_spatial_timederiv))
# (b) flat slicing: g = diag(-1, e^{2Ht}, e^{2Ht}, e^{2Ht}); K = (1/2N) g^ij dt g_ij
gflat = sp.exp(2*H0*t)
Kflat = sp.simplify(3*(sp.diff(gflat, t)/gflat)/2)
check('dS flat slicing: K = 3*H0 (a different CMC foliation of the SAME spacetime)',
      sp.simplify(Kflat - 3*H0) == 0)
print("""
  ADVERSARIAL POINT vs the CMC escape: BOTH slicings are CMC (K constant on slices),
  of the SAME maximally-symmetric spacetime, with K = 0 vs K = 3H. The classical
  CMC-uniqueness theorems (Marsden-Tipler/Brill class) assume the timelike convergence
  condition R_mn t^m t^n >= 0, i.e. rho + 3p >= 0 — VIOLATED exactly when Lambda
  dominates. So 'q = K_CMC[g] is a functional of the metric alone' fails to be
  single-valued in the DE era: selecting THE cosmic CMC foliation (e.g. by asymptotic
  matching to the FLRW slicing) is a global datum. The escape trades propagating
  Cauchy data for a discrete/global foliation-selection datum + an elliptic
  (instantaneous) determination.""")

# =====================================================================
print('=' * 76)
print('CHECK 4: global average <R> over LCDM history -> 4*Lambda (constant; sequestering)')
print('=' * 76)
import math
Om, Ol = 0.3, 0.7          # H0 = 1 units;  Lambda = 3*Ol*H0^2  =>  4*Lambda = 8.4
lam4 = 12*Ol
def Hub(av): return math.sqrt(Om/av**3 + Ol)
def Rof(av):
    Hv = Hub(av); Hd = -1.5*Om/av**3   # Hdot = -(3/2) Om H0^2 a^-3 (matter only)
    return 6*(Hd + 2*Hv**2)
# integrate  num = int a^3 R dt, den = int a^3 dt  from a0=1e-4 to a=a_max
def averages(amax, n=400000):
    num = den = 0.0; a0v = 1e-4
    la0, la1 = math.log(a0v), math.log(amax); dl = (la1 - la0)/n
    for i in range(n):
        av = math.exp(la0 + (i + 0.5)*dl)
        w = av**3/(av*Hub(av))*dl*av   # dt = da/(aH), da = a dl
        num += Rof(av)*w; den += w
    return num/den
for amax in [1.0, 3.0, 10.0, 100.0]:
    print(f'  <R> up to a={amax:6.1f}:  {averages(amax):9.4f}   (4*Lambda = {lam4})')
check('<R>_spacetime -> 4*Lambda as the dS future dominates (within 1% by a=100)',
      abs(averages(100.0) - lam4)/lam4 < 0.01)
print("""
  CONSEQUENCE: sequestering-type global averages are (i) ONE number for the whole
  spacetime — z-independent BY CONSTRUCTION (Layer A at best), and (ii) dominated by
  the FUTURE dS volume — teleological. A 'running average up to now' needs a slice
  ('now' = Leg C) or a past-lightcone support (Leg B — committed in-in result:
  localizes to an AeST-like field).""")

# =====================================================================
print('=' * 76)
print('CHECK 5: small-diamond/ball functionals reduce to local jets (Leg A)')
print('=' * 76)
# Geodesic-ball volume in a static spatial slice of constant curvature R3:
# V(ell) = V_flat (1 - R3 ell^2/30 + ...). Verify the expansion coefficient on S^3.
ell, Rc = sp.symbols('ell R_c', positive=True)
# 3-sphere of radius Rc: V(ell) = 2 pi Rc^3 (2*(ell/Rc) - sin(2 ell/Rc))/2 -> use exact:
# V(ell) = 4 pi int_0^ell Rc^2 sin^2(s/Rc) ds = 2 pi Rc^2 (ell - Rc sin(ell/Rc) cos(ell/Rc))
Vball = 2*sp.pi*Rc**2*(ell - Rc*sp.sin(ell/Rc)*sp.cos(ell/Rc))
series = sp.series(Vball, ell, 0, 6).removeO()
Vflat = sp.Rational(4, 3)*sp.pi*ell**3
ratio = sp.simplify(sp.expand(series/Vflat))
# scalar curvature of S^3 radius Rc is R3 = 6/Rc^2 -> coefficient must be -R3/30 * ell^2
coeff = sp.simplify(ratio.coeff(ell, 2))
print('  V/V_flat = 1 + (', coeff, ') ell^2 + ...   with R3 = 6/Rc^2')
check('ball-volume deficit coefficient = -R3/30 (reads LOCAL curvature only)',
      sp.simplify(coeff + (6/Rc**2)/30) == 0)
print("""
  CONSEQUENCE: any thermodynamic/entropy functional of a small causal diamond or
  geodesic ball (Jacobson entanglement-equilibrium style) is, order by order in the
  diamond size, a functional of the local jet -> Leg A -> H-blind in a vacuole.
  Making the diamond Hubble-sized forces its support across the vacuole boundary:
  by causal character of the support this is Leg B (past cone) or Leg C (slice).""")

# =====================================================================
print('=' * 76)
n_pass = sum(1 for _, ok in results if ok)
print(f'{n_pass}/{len(results)} checks passed')
print("""
VERDICT (exception hunt):
  (a) global constraints/sequestering: CONSTANT + teleological -> no evolving a0. Leg A/B.
  (b) boundary functionals (ADM/scri): scri of Lambda>0 is FUTURE spacelike infinity ->
      teleological (advanced) = Leg B'; reading it 'at z' needs a cut = Leg C.
  (c) Ricci-only: Einstein-algebraic in local T + Lambda -> constant or environmental. Leg A.
  (d) local-horizon thermodynamics: small diamonds = local jets (Leg A); Hubble diamonds =
      Leg B/C by support. Whose state? the LOCAL one (SdS/vacuum), not the cosmic one.
  (e) infinite-derivative kernels: support-wide = nonlocal -> causal classification
      forces Leg B (retarded/advanced) or Leg C (spacelike support needs a slice).
  (f) THE ONE REAL CRACK — q = K of the CMC foliation (York/CMC route, already realized
      in qwen_claude_field_theory/theory_2026/york/): no propagating scalar (2+0 Dirac-
      verified), no conserved charge, a0(z) = a0 H(z)/H0 DERIVED inside bound systems.
      It evades the NAIVE Leg C wording ('frame = Cauchy data') because the foliation is
      metric-determined UP TO the CMC-selection ambiguity — but CHECK 3 shows that
      ambiguity is REAL precisely in the Lambda era (two CMC foliations of dS), and the
      determination is ELLIPTIC/instantaneous: the causality-or-conservation TRADE of
      the trichotomy's consequence clause, whose acceptability is the committed OPEN
      gate (RESULT_york_cmc_mond_and_lensing_nogo.md sec 4c: 'elliptic => acausal' is
      TOO STRONG; Horava-type foliations can be causally legitimate).
  => Trichotomy survives AS AMENDED: local / nonlocal-causal / frame, with the frame leg
     containing a metric-selected-foliation subclass that pays (at minimum) a global
     foliation-selection datum + an instantaneous elliptic sector, i.e. lands exactly on
     the 'causality/conservation trade' branch — NOT a clean counterexample, NOT closed.
""")
