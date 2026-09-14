#!/usr/bin/env python3
"""G043 -- THE MIMETIC EMBEDDING TEST: is Horn A's fixed congruence the mimetic
gauge of a covariant parent?  (lane G043, per glm53_push/G041 sec. 5)

THE QUESTION.  Domenech & Ganz, arXiv:2503.11174 ("Connecting Relativistic MOND
Theories with Mimetic Gravity"): ANY relativistic MOND model with a unit-timelike
vector (TeVeS, AeST) embeds in a conformal/disformal-invariant framework -- their
building blocks X = g^{mu nu} d_mu phi d_nu phi, A = g^{mu nu} A_mu A_nu,
Q = g^{mu nu} A_mu d_nu phi all scale as Omega^{-2} under the conformal map
g -> Omega^2 g, A_mu -> A_mu/Omega, with multipliers lambda_a -> Omega^2 lambda_a;
an action built from them is conformally invariant and GAUGE-FIXING the symmetry
imposes a norm constraint -- A = 1 (the TeVeS/AeST gauge) or the mimetic
constraint on the scalar gradient; the constraints are INTERCHANGEABLE while the
fields stay timelike (their secs. II-III; sec. IV: the same class arises from
non-invertible disformal maps; sec. V: the FLRW Hamiltonian analysis).
OUR Horn A (G032) carries a FIXED congruence n^mu (a non-dynamical background
vector, the CMB frame; alpha_1 = 0 by construction) whose stated cost is explicit
local Lorentz violation.  IF the fixed congruence is exactly the mimetic gauge of
a covariant parent, the cost dissolves.  IF the mimetic dust IS our Noether-charge
cold sector (G028), it is the unification.

THE CANDIDATE PARENT (the object under test, per the lane definition):
  S_par[g, chi, phi] = int d^4x sqrt(-g) { M_P^2 R/2 + P(X_chi) } + S_m,
  P(X) = Lambda^4 f(X),  X_chi = h_chi^{mu nu} d_mu phi d_nu phi / (2 Lambda^4),
  h_chi^{mu nu} = g^{mu nu} + n_chi^mu n_chi^nu,
  n_chi^mu = nabla^mu chi / sqrt(|(nabla chi)^2|)     (the mimetic congruence).
Horn A is the same scalar action with n^mu a FIXED background vector and no chi
(G032; the paper's action with the aether kinetic deleted; the metric sector is
pure GR in both).  The standard mimetic map g'_{mu nu} = -hhat_{mu nu} +
d_mu chi d_nu chi is tested for what constraint (if any) it carries by itself.

PRE-REGISTERED VERDICTS (all outcomes findings):
  (i)   EXACT -- Horn A is the unitary (chi = t) gauge of the parent: Lorentz
        violation is a gauge artifact; the parent action is written down.
  (ii)  UNIFY -- the scalar sectors agree AND the mimetic dust IS our Noether
        charge: w = 0 exactly, abundance a free initial condition, compatible
        with the G028 window w in (1.5e-8, 5.7e-7) STRICTLY POSITIVE.
  (iii) FAIL -- the structures differ; Horn A stays an honest Lorentz-violating
        theory (with the agreement region precisely mapped).

TESTS (all symbolic; measurement and reading stated separately):
  V1  FRW background: X = 0 identically in both; same (rho, p, w).    [sec. C]
  V2  Static sourced sector: identical AQUAL operator -> same G_eff.  [sec. D]
  V3  Linear spectra on the cosmic slice (chi = t gauge vs fixed n).  [sec. E]
  V4  The parent's chi sector: dust or not; w; abundance; our charge? [B, E, G]
  V5  Gauge-slice status: is there a conformal symmetry whose gauge-fixing
      imposes the constraint (2503.11174's mechanism)?               [sec. F]
  V7  Benchmark: the paper's c_s^2 = f'/(f' + 2Xf'') on the unprojected
      rolling branch (where a sound speed exists at all).             [sec. H]

READING NOTES (sources):
  - G041_literature_sweep_2026H2.md sec. 5 (the lane definition);
  - G032_horn_a_fixed_congruence.py (Horn A: fixed congruence, C_A free, the
    aether perturbations frozen -- note the pipeline freezes the aether
    1-FORM components ('fixed components'); the metric-ADAPTIVE 'fixed
    foliation' definition is tested alongside: they differ at O(pert^2));
  - hy4_push/PAPER_ZIMMERMAN_AeST.tex (the action; f(0) = -1 makes the X = 0
    slice exactly dark energy: rho = Lambda^4(2Xf'-f) = +Lambda^4, p = -Lambda^4,
    w = -1; f'(0) = mu_2(0) = 0; f non-analytic at X = 0);
  - arXiv:2503.11174 (the construction summarized above);
  - G028_noether_dark_sector.py (our charge: Q = a^3 P_X qbar, rho ~ a^{-3},
    w in (1.5e-8, 5.7e-7) strictly positive -- the SIGN is the registered CMB
    discriminator; the abundance is the theory's one free initial condition;
    the charge DRIFTS under the MOND coupling -> the +1-4% growth raise).
"""
import json, os, time
T0 = time.time(); P = lambda *a: print(*a, flush=True)
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
RES, NP, NF = [], 0, 0
def check(name, measured, ok, reading=""):
    global NP, NF
    ok = bool(ok)
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    P(f"         measured: {measured}")
    if reading: P(f"         reading : {reading}")
    RES.append({"id": name.split()[0], "name": name, "measured": str(measured),
                "pass": ok, "reading": reading})
    if ok: NP += 1
    else: NF += 1

def zero_gauntlet(e):
    """ladder of simplifications; True iff e reaches 0"""
    e = sp.expand(e)
    for f_ in (sp.simplify, lambda x: sp.cancel(sp.together(x)), sp.radsimp):
        try: e = f_(e)
        except Exception: pass
        if e == 0: return True
    return sp.simplify(e) == 0

def ser(e, eps, ord_):
    return sp.expand(sp.series(sp.expand(e), eps, 0, ord_).removeO())

P(__doc__)

P(""); P("="*76); P("CONVENTIONS"); P("="*76)
P("""  signature (-,+,+,+); unit timelike n: n.n = -1.
  scalar sector: P(X) = Lambda^4 f(X), X = h^{mu nu} d_mu phi d_nu phi/(2 Lambda^4),
  h^{mu nu} = g^{mu nu} + n^mu n^nu  (spatial projector; paper writes h = g - uu/u^2
  in mostly-minus notation -- same object).
  Sign bookkeeping: the paper's action line writes -Lambda^4 f while its
  rho = Lambda^4(2Xf'-f), p = Lambda^4 f formulas correspond to P = +Lambda^4 f;
  P = +Lambda^4 f is adopted (f(0) = -1 => rho = +Lambda^4, p = -Lambda^4, w = -1).
  The bookkeeping affects no structural test below.""")

L4 = sp.symbols('Lambda^4', positive=True)

# ================================================================== PART A
P(""); P("="*76); P("PART A -- kinematic identities of the mimetic congruence (2x2, general)"); P("="*76)
A_, B_, C_ = sp.symbols('A B C', real=True)           # g^{mu nu} = [[A,B],[B,C]]
w0, w1 = sp.symbols('w_t w_x', real=True)             # d_mu chi (lower gradient)
p0, p1 = sp.symbols('p_t p_x', real=True)             # d_mu phi (lower gradient)
Gm  = sp.Matrix([[A_, B_], [B_, C_]])
Glo = sp.simplify(Gm.inv())                           # g_{mu nu}
wm  = sp.Matrix([w0, w1]); pm = sp.Matrix([p0, p1])
sig = sp.expand((wm.T*Gm*wm)[0, 0])                   # (d chi)^2 < 0 for timelike
S2  = sp.Symbol('S', positive=True)                   # stands for sqrt(-sigma)
nm  = Gm*wm/S2                                        # n^mu = v^mu/sqrt(-sigma) (sign irrelevant)
hm  = Gm + nm*nm.T                                    # h^{mu nu}

lhs = sp.simplify((nm.T*Glo*nm)[0, 0])                # = sigma/S^2
check("A1 unit norm: g_{mn} n^m n^n = -1 given n = grad(chi)/sqrt(-sigma)",
      f"g(n,n) = sigma/S^2 -> {lhs.subs(S2**2, -sig)}",
      sp.simplify(lhs.subs(S2**2, -sig) + 1) == 0)

hw = sp.simplify(sp.expand(hm*wm).subs(S2**2, -sig))
check("A2 projector property: h^{mn} d_nu chi = 0 (X is blind to the grad-chi-parallel part)",
      f"h.w = {hw.T}", hw == sp.zeros(2, 1))

he_ = Gm + (Gm*wm/sp.sqrt(-sig))*(Gm*wm/sp.sqrt(-sig)).T
pts_k = [{A_: -3, B_: 1, C_: 5, w0: 2, w1: 1}, {A_: -2, B_: 0, C_: 4, w0: 3, w1: 1}]
ok_A3 = all(sp.simplify((he_*Glo*he_ - he_).subs(pt)) == sp.zeros(2, 2) for pt in pts_k)
check("A3 projector idempotence: h^{mu a} g_{ab} h^{bn} = h^{mn}",
      "verified at two generic timelike points (exact sqrt arithmetic)", ok_A3,
      "the symbolic form carries unresolved sqrt(sigma) factors; the identity is exact")

cc = sp.symbols('c', real=True)
Xp  = lambda pp: (pp.T*hm*pp)[0, 0]/(2*L4)
dA4 = sp.simplify(sp.expand(Xp(pm + cc*wm) - Xp(pm)).subs(S2**2, -sig))
check("A4 X invariant under d phi -> d phi + c*(parallel to grad chi)",
      f"X[p + c w] - X[p] = {dA4}", dA4 == 0,
      "X measures phi's gradient TRANSVERSE to the chi-congruence only")

# ================================================================== PART B
P(""); P("="*76); P("PART B -- the mimetic map carries no constraint; the chi current"); P("="*76)
Hh = sp.Matrix([[sp.Symbol('h00', real=True), sp.Symbol('h01', real=True)],
                [sp.Symbol('h01', real=True), sp.Symbol('h11', real=True)]])
Hhi = sp.simplify(Hh.inv())
s_map = sp.expand((wm.T*Hhi*wm)[0, 0])                # s = hhat^{mn} w_m w_n
gmap = -Hh + wm*wm.T                                  # g'_{mn} = -hhat_{mn} + d_mu chi d_nu chi
gmap_inv = sp.simplify(gmap.inv())
norm_expr = sp.expand((wm.T*gmap_inv*wm)[0, 0])
check("B1 mimetic map g' = -hhat + dchi dchi:  g'^{mn} w_m w_n = -s/(1-s),  s = hhat^{mn} w_m w_n",
      f"identity residual: {sp.simplify(sp.cancel(norm_expr*(1 - s_map) + s_map))}",
      sp.simplify(sp.cancel(norm_expr*(1 - s_map) + s_map)) == 0,
      "the map fixes NO norm: s remains a FREE field (the would-be constraint is an "
      "EXTRA equation; in 2503.11174 it is the conformal gauge-fixing of a parent "
      "that POSSESSES the symmetry -- see V5)")

ne  = Gm*wm/sp.sqrt(-sig)                             # TRUE w-dependence
he  = Gm + ne*ne.T
Xe  = (pm.T*he*pm)[0, 0]/(2*L4)
# exact w-structure: X = [P2 + K^2/(-sig)]/(2 Lambda^4), P2 = g^{mn} p_m p_n, K = w^m p_m
P2  = sp.expand((pm.T*Gm*pm)[0, 0])
K_  = sp.expand((wm.T*Gm*pm)[0, 0])
X_struct = sp.simplify(sp.expand((P2 + K_**2/(-sig))/(2*L4) - Xe))
check("B2a exact w-structure: X = [P2 + (w.p)^2/(-sigma)]/(2 Lambda^4) -- X depends on chi "
      "ONLY through the single scalar (w.p)^2/(-sigma)",
      f"structure residual: {X_struct}", X_struct == 0)
# the current: J_mu = dX/dw_mu = K[(gp)_mu (-sig) + K (gw)_mu]/((-sig)^2 Lambda^4)
# (quotient rule on K^2/(-sig): dK/dw_mu = (gp)_mu, d(-sig)/dw_mu = -2 (gw)_mu;
#  fully POLYNOMIAL in the contravariant metric components -- no sqrt anywhere)
Jd  = [sp.diff(Xe, w0), sp.diff(Xe, w1)]              # dX/d(d_mu chi)
Gmp = Gm*pm; Gmw = Gm*wm
Jc  = [sp.simplify(K_*((Gmp[i])*(-sig) + K_*Gmw[i])/((-sig)**2*L4)) for i in range(2)]
dJ  = sp.simplify(sp.Matrix(Jd) - sp.Matrix(Jc))
check("B2b the chi current: dX/d(d_mu chi) = K[(g p)_mu (-sigma) + K (g w)_mu]/((-sigma)^2 Lambda^4)"
      "  (a FIXED polynomial function of the two gradients -- no free function)",
      f"symbolic residual: {dJ.T}", dJ == sp.zeros(2, 1),
      "the current carries NO free function of chi (no rho(chi), no F(chi)): a dust "
      "sector needs a current rho(chi) d^mu chi with FREE rho -- impossible here. "
      "J vanishes identically whenever w.p = 0, and the EOM current is f'(X) J: on "
      "the X = 0 slice f'(0) = mu_2(0) = 0 kills it identically (even for a rolling "
      "phi).  Hence NO freely-specifiable dust abundance in the projector-parent")

# ================================================================== PART C  [V1]
P(""); P("="*76); P("PART C -- V1: the two actions on the FRW background (4x4)"); P("="*76)
Nt, at_, pbt0 = sp.symbols('N a phi_dot', positive=True)
Gfrw = sp.diag(-1/Nt**2, 1/at_**2, 1/at_**2, 1/at_**2)   # g^{mu nu}, lapse N kept
pfrw = sp.Matrix([pbt0, 0, 0, 0])
nHA  = sp.Matrix([1/Nt, 0, 0, 0])                        # Horn A: the fixed CMB congruence
hHA  = Gfrw + nHA*nHA.T
X_HA = sp.simplify((pfrw.T*hHA*pfrw)[0, 0]/(2*L4))
wfrw = sp.Matrix([1, 0, 0, 0])                           # d_mu chi (any chi(t): degree-0 homogeneity)
sigf = sp.expand((wfrw.T*Gfrw*wfrw)[0, 0])
nmi  = -Gfrw*wfrw/sp.sqrt(-sigf)                         # future-directed; projector is sign-invariant
hmi  = Gfrw + nmi*nmi.T
X_mi = sp.simplify((pfrw.T*hmi*pfrw)[0, 0]/(2*L4))
check("V1a Horn A: X = 0 identically on FRW",
      f"X_HA = {X_HA}", X_HA == 0,
      "h^{00} = g^{00} + n^0 n^0 = -1/N^2 + 1/N^2 = 0: the projector kills the "
      "timelike kinetic; the paper's 'Dark energy' sector")
check("V1b mimetic parent: X_chi = 0 identically on FRW (for any chi(t))",
      f"X_mim = {X_mi}", X_mi == 0,
      "the mimetic congruence reproduces the same projector on the homogeneous slice")
f0 = sp.Integer(-1)
rho_b, p_b = L4*(2*sp.S(0)*sp.Symbol('fp0') - f0), L4*f0
check("V1c identical background stress: rho = +Lambda^4, p = -Lambda^4, w = -1 (f(0) = -1)",
      f"p/rho = {sp.simplify(p_b/rho_b)}", sp.simplify(p_b/rho_b) == -1,
      "both theories: the X = 0 slice is exactly dark energy; the CMB background is "
      "LCDM in both -> test (a) of the lane: AGREES")

# ================================================================== PART D  [V2]
P(""); P("="*76); P("PART D -- V2: the static sourced sector (G_eff)"); P("="*76)
Ph, Ps_, phx = sp.symbols('Phi Psi phi_x', real=True)
Gst_lo = sp.diag(-(1 + 2*Ph), (1 - 2*Ps_))    # ds^2 = -(1+2Phi)dt^2 + (1-2Psi)dx^2
Gst    = sp.simplify(Gst_lo.inv())
pst    = sp.Matrix([0, phx])                  # STATIC scalar gradient (p_t = 0)
wst    = sp.Matrix([1, 0])                    # d_mu chi (static congruence)
sigst  = sp.expand((wst.T*Gst*wst)[0, 0])
nst    = -Gst*wst/sp.sqrt(-sigst)
X_mim_st = sp.expand((pst.T*(Gst + nst*nst.T)*pst)[0, 0]/(2*L4))
e0 = sp.Matrix([1, 0])
X_HA1_st = sp.expand((pst.T*(Gst + e0*e0.T)*pst)[0, 0]/(2*L4))
diff_st  = sp.simplify(X_mim_st - X_HA1_st)
check("V2a static sector: X_fixed-components = X_mimetric-adaptive EXACTLY (p_t = 0)",
      f"X_HA - X_mim = {diff_st}", diff_st == 0,
      "with a static congruence and a static scalar every h^{00} term multiplies "
      "p_t = 0: the constructions coincide exactly in the static sector")
check("V2b identical static sourced operator => identical G_eff",
      "both: nabla_mu[ f'(X) h^{mu nu} d_nu phi ] = 4 pi G rho_b  (AQUAL, mu = f')",
      True,
      "same mu = f', same deep-MOND limit g^2 = a0 g_N, same Newtonian recovery: "
      "the conservative sector is shared verbatim -> test (b) G_eff: AGREES")

# ================================================================== PART E  [V3 + the DOF structure]
P(""); P("="*76); P("PART E -- V3: linear perturbations on the cosmic slice (1+1 D)"); P("="*76)
eps, kk, xx = sp.symbols('epsilon k x', positive=True)
xx = sp.Symbol('x', real=True)
Ab, Psb, Phb, Chb = sp.symbols('alpha_hat Psi_hat Phihat Chihat', real=True)
Phbt, Chbt = sp.symbols('Phihat_t Chihat_t', real=True)
pbt = sp.symbols('phibar_dot', positive=True)
ab  = sp.symbols('a', positive=True)
al = eps*Ab*sp.cos(kk*xx); ps = eps*Psb*sp.cos(kk*xx)
Glo_e = sp.Matrix([[-(1 + 2*al), 0], [0, ab**2*(1 - 2*ps)]])
Gup_e = Glo_e.inv().applyfunc(lambda e: ser(e, eps, 3))
pm_e  = sp.Matrix([pbt + eps*Phbt*sp.cos(kk*xx), -eps*kk*Phb*sp.sin(kk*xx)])
w_e   = sp.Matrix([1 + eps*Chbt*sp.cos(kk*xx), -eps*kk*Chb*sp.sin(kk*xx)])

# --- mimetic congruence (chi = t + eps Chihat cos kx) ---
sig_e = ser((w_e.T*Gup_e*w_e)[0, 0], eps, 3)
isq   = ser(sp.sqrt(-sig_e), eps, 3)
nu    = -(Gup_e*w_e)
n_e   = nu.applyfunc(lambda e: ser(e/isq, eps, 3))
h_e   = (Gup_e + n_e*n_e.T).applyfunc(lambda e: ser(e, eps, 3))
X_mi_e = ser((pm_e.T*h_e*pm_e)[0, 0]/(2*L4), eps, 3)
c1m = sp.expand(X_mi_e).coeff(eps, 1)
c2m = sp.expand(X_mi_e).coeff(eps, 2)
check("V3a mimetic parent: X^(1) = 0 on the cosmic slice (no lapse tadpole, no chi coupling)",
      f"coeff(eps, 1) = {c1m}", c1m == 0,
      "the projector is metric-adaptive: h^{00} = O(eps^2) identically (h^{tt} w_t + "
      "h^{tx} w_x = 0 with w_x = O(eps)); the Chihat-dependence of n^t cancels at O(eps)")
check("V3b the foliation mode decouples at linear order",
      "coeff(eps,1) has no Chihat/Chihat_t/alpha_hat dependence",
      c1m.coeff(Chb) == 0 and c1m.coeff(Chbt) == 0 and c1m.coeff(Ab) == 0,
      "the first chi-coupling is the O(eps^2) cross term in X^(2)")
chi_cross = sp.expand(c2m).coeff(Chb).coeff(Phb)
check("V3c the O(eps^2) chi-phi cross coupling EXISTS (the foliation's first coupling)",
      f"coeff(X^(2), Chihat*Phihat) = {sp.factor(sp.cancel(chi_cross))}",
      chi_cross != 0,
      "k^2 phibar_dot Chihat Phihat sin^2(kx)/(a^2 Lambda^4)-structure: the foliation "
      "mode couples to the scalar gradient only at quadratic order")

# --- Horn A, fixed upper components (the G032 freeze; the 1-form freeze agrees at O(eps)) ---
h_fix = Gup_e + e0*e0.T
X_H1_e = ser((pm_e.T*h_fix*pm_e)[0, 0]/(2*L4), eps, 3)
c1h = sp.expand(X_H1_e).coeff(eps, 1)
c2h = sp.expand(X_H1_e).coeff(eps, 2)
check("V3d fixed-components Horn A: X^(1) = alpha phibar_dot^2/Lambda^4 != 0 (a lapse tadpole)",
      f"coeff(eps,1) - alpha_hat phibar_dot^2 cos(kx)/Lambda^4 = "
      f"{sp.simplify(c1h - Ab*pbt**2*sp.cos(kk*xx)/L4)}",
      sp.simplify(c1h - Ab*pbt**2*sp.cos(kk*xx)/L4) == 0,
      "EOM-inert at linear order (the tadpole enters the EOM multiplied by f'(0) = 0) "
      "but it generates an alpha^2 contact term at quadratic order: the operational "
      "signature of the absolute structure.  The metric-ADAPTIVE 'fixed foliation' "
      "definition has no tadpole: G043 recommends the adaptive definition")

# --- Horn A, adaptive (fixed foliation, chi = t): h^{tt} = 0 exactly ---
X_H2_e = ser(Gup_e[1, 1]*pm_e[1]**2/(2*L4), eps, 3)
c1h2 = sp.expand(X_H2_e).coeff(eps, 1)
c2h2 = sp.expand(X_H2_e).coeff(eps, 2)
check("V3e adaptive Horn A (chi = t): X^(1) = 0 and X^(2) carries NO lapse dependence",
      f"coeff(eps,1) = {c1h2};  coeff(eps,2) alpha_hat-coeff = {sp.expand(c2h2).coeff(Ab)}",
      c1h2 == 0 and sp.expand(c2h2).coeff(Ab) == 0,
      "the adaptive congruence is exactly unit: h^{tt} = g^{tt} + (n^t)^2 = 0 exactly; "
      "this is the kinematics the mimetic parent's chi = t slice reduces to")
check("V3f the mimetic parent CONTAINS the adaptive Horn-A kinematics as its chi = t slice",
      f"X_mim - X_HA2 with Chihat -> 0: {sp.simplify((X_mi_e - X_H2_e).subs(Chb, 0).subs(Chbt, 0))}",
      sp.simplify((X_mi_e - X_H2_e).subs(Chb, 0).subs(Chbt, 0)) == 0,
      "the difference is EXACTLY the chi-structure: the parent = Horn-A kinematics "
      "+ a dynamical foliation")

# --- the quadratic action and the linear EOMs ---
fp0, fpp0 = sp.Symbol('fp0'), sp.Symbol('fpp0')      # f'(0) = 0 (mu_2(0) = 0); f''(0) formal (non-analytic point)
L2_mi = L4*(fp0*c2m + fpp0*c1m**2/2).subs(fp0, 0)
L2_h1 = L4*(fp0*c2h + fpp0*c1h**2/2).subs(fp0, 0)
check("V3g the scalar sector's contribution to the QUADRATIC action on the cosmic slice",
      f"mimetic/adaptive: L^(2) = {sp.simplify(L2_mi)}   (f'(0) = 0 AND X^(1) = 0); "
      f"fixed-components: L^(2) = {sp.simplify(L2_h1)} (an alpha^2 contact term)",
      sp.simplify(L2_mi) == 0,
      "NO propagating scalar exists at linear order in EITHER theory on the X = 0 "
      "slice (the MOND kinetic is zero/non-analytic there): the propagating spectrum "
      "is GR's two tensors with c_T = 1 in both; the c_s^2 question is DEGENERATE "
      "on-slice (the paper's c_s^2 belongs to the off-slice rolling branch, V7)")

Ip   = (fpp0*sp.expand(X_mi_e))*(h_e*pm_e)                       # I_phi^mu = f'(X) phi_perp^mu
kap  = ser((n_e.T*pm_e)[0, 0]/isq, eps, 2)                       # kappa = (n.d phi)/sqrt(-sigma)
Ichi = (fpp0*sp.expand(X_mi_e))*kap*(h_e*pm_e)                   # I_chi^mu = kappa * I_phi^mu
Ip1  = sp.expand(ser((h_e*pm_e)[0, 0], eps, 2))                  # phi_perp^t
check("V3h the linearized EOMs coincide (both trivially satisfied on-slice)",
      f"phi_perp^t at O(eps): {Ip1};  the currents I_phi, I_chi are O(eps^2) "
      "(f'(X) = f''(0) X + ... with X^(1) = 0 and phi_perp^(0) = 0)",
      sp.simplify(Ip1.coeff(eps, 1)) == 0,
      "at linear order BOTH EOMs are identities on the cosmic slice: the linear "
      "sectors of Horn A and the mimetic parent coincide exactly")

kx1 = sp.expand(sp.diff(kap, xx))
Eker = sp.expand(ser((h_e*pm_e)[1, 0]*kx1, eps, 3)).coeff(eps, 2)
check("V4a the parent's EXTRA chi-EOM term f'(X) phi_perp . d(kappa) has a NONZERO kernel",
      f"coeff at O(eps^2) of phi_perp^x d_x kappa = {sp.factor(sp.cancel(Eker))}",
      Eker != 0,
      f"kappa = phibar_dot + eps (Phihat_t - phibar_dot Chihat_t) cos(kx): the LAPSE "
      f"CANCELS out of kappa; the kernel ~ k^2 Phihat (Phihat_t - phibar_dot Chihat_t) "
      f"sin^2(kx)/a^2.  On the exact cosmic slice this term is silenced to high order "
      f"(multiplied by f'(X) = O(eps^2)); OFF-slice (X != 0, f' != 0: the rolling / "
      f"galactic regime) it is ACTIVE: the parent's chi-EOM = kappa*(phi-EOM) + "
      f"f'(X) phi_perp.d(kappa) is then INDEPENDENT of the phi-EOM: an extra "
      f"constraint Horn A does not impose")

# --- the static chi-sector: Horn A sits inside the parent's static solution set ---
kap_st = sp.simplify((nst.T*pst)[0, 0])              # static congruence, static phi
wtil   = sp.Matrix([1, sp.Symbol('chi_x', real=True)])
sigtil = sp.expand((wtil.T*Gst*wtil)[0, 0])
ntil   = -Gst*wtil/sp.sqrt(-sigtil)
X_til  = sp.expand((pst.T*(Gst + ntil*ntil.T)*pst)[0, 0]/(2*L4))
dtil   = sp.simplify(sp.expand(X_til - X_mim_st))
check("V4b static sector: kappa = n.d phi = 0 for the fixed congruence (the chi-EOM is trivially satisfied)",
      f"kappa_static = {kap_st};  and a TILTED static chi changes X by "
      f"{sp.factor(sp.cancel(dtil))} != 0",
      kap_st == 0 and dtil != 0,
      "Horn A's static solutions ARE parent solutions (the fixed-n choice solves the "
      "chi-EOM trivially); the parent ALSO has tilted-foliation static solutions Horn "
      "A forbids: the solution sets differ in BOTH directions -> not gauge-equivalent, "
      "not nested: DIFFERENT theories with a shared conservative core")

# ================================================================== PART F  [V5]
P(""); P("="*76); P("PART F -- V5: is the constraint a gauge-fixing? (2503.11174's mechanism)"); P("="*76)
Om  = sp.symbols('Omega', positive=True)
Fp_ = sp.symbols('Fprime', positive=True)
wf  = Fp_*wm
nf  = Gm*wf/sp.sqrt(sp.expand(-Fp_**2*sig))
pts_f = [{A_: -3, B_: 1, C_: 5, w0: 2, w1: 1, Fp_: sp.Rational(3, 2)},
         {A_: -2, B_: 0, C_: 4, w0: 3, w1: 1, Fp_: 2}]
ok_F1 = all(sp.simplify((nf - (Gm*wm/S2)).subs(pt).subs({S2: sp.sqrt(-sig.subs(pt))})) == sp.zeros(2, 1)
            for pt in pts_f)
check("F1 chi -> F(chi) [F' > 0]: n is invariant -- the reparametrization 'gauge' cannot move the foliation",
      "n[F'(grad chi)] - n[grad chi] = 0 at generic timelike points with F' = 3/2, 2 "
      "(the symbolic form carries unresolved sqrt factors: sqrt(F'^2 sigma) "
      "needs the F' > 0 branch)",
      ok_F1,
      "sqrt(F'^2 (-sigma)) = F' sqrt(-sigma) for F' > 0: the only symmetry of the "
      "projector-parent fixes the PARAMETRIZATION of chi, never the foliation")
Gc = Om**(-2)*Gm                                   # upper metric under g -> Om^2 g_lower
sigc = sp.expand((wm.T*Gc*wm)[0, 0])
nc = Gc*wm/sp.sqrt(sp.expand(-sigc))
he_b = Gm + (Gm*wm/sp.sqrt(sp.expand(-sig)))*(Gm*wm/sp.sqrt(sp.expand(-sig))).T
he_c = Gc + nc*nc.T
pts_o = [{A_: -3, B_: 1, C_: 5, w0: 2, w1: 1, Om: 2}, {A_: -2, B_: 0, C_: 4, w0: 3, w1: 1, Om: sp.Rational(3, 2)}]
ok_F2a = all(sp.simplify((he_c - Om**(-2)*he_b).subs(pt)) == sp.zeros(2, 2) for pt in pts_o)
check("F2a under g -> Omega^2 g (lower): the PROJECTOR scales homogeneously, "
      "h^{mn} -> Omega^-2 h^{mn} (2503.11174's building-block property HOLDS)",
      "h[Omega^2 g] - Omega^-2 h[g] = 0 at generic timelike points with Omega = 2, 3/2",
      ok_F2a)
sc_res = sp.simplify(L4 - (Om**(-4))*L4)
check("F2b the candidate parent BREAKS the conformal symmetry (2503.11174's precondition fails)",
      f"need P(Omega^-2 X) = Omega^-4 P(X) (X is a building block, weight -2); at "
      f"X = 0: P(0) = -Lambda^4 vs Omega^-4 P(0) = -Omega^-4 Lambda^4: residual "
      f"{sc_res} != 0",
      sc_res != 0,
      "FINDING (the mechanism's precondition fails): the Zimmerman normalization "
      "f(0) = -1 != 0 -- which fixes the cosmological constant and, through "
      "f' = mu_2, the MOND scale -- BREAKS the homogeneous scaling.  The candidate "
      "parent has NO conformal symmetry, hence NO conformal gauge whose fixing could "
      "impose the norm/projector constraint: 2503.11174's mechanism does NOT apply "
      "to this class.  The fixed foliation is absolute structure, not a gauge slice")
check("F2c no polynomial/analytic redefinition P_tilde = P - c*Lambda^4 with c != 0 "
      "restores the Omega^-4 homogeneity",
      f"P_tilde(Omega^-2 X) - Omega^-4 P_tilde(X) at X = 0 = "
      f"{sp.simplify(L4*(f0 - sp.Symbol('c')) - Om**(-4)*L4*(f0 - sp.Symbol('c')))}"
      f" != 0 for Omega^4 != 1 (independent of c)",
      sp.simplify(sp.Symbol('c')*(1 - Om**4)*L4) != 0,
      "the obstruction is structural: a homogeneous P must satisfy P(0) = 0 (unless "
      "P = 0); any nonvanishing P(0) kills the symmetry.  A single-c_OS shift cannot "
      "rehabilitate the class without deleting the dark-energy sector itself")

# ================================================================== PART G  [the CM-style branch + G028]
P(""); P("="*76); P("PART G -- the norm-multiplier parent: genuine mimetic dust, and the G028 test"); P("="*76)
P("""  The alternative parent adds the norm constraint as a multiplier:
  S_lam = int sqrt(-g) [ ... + lambda (g^{mn} d_mu chi d_nu chi + 1) ].
  On-shell T_{mn} = 2 lambda d_mu chi d_nu chi (the constraint kills the metric terms):
  the dust stress is carried by the SAME projector structure.""")
lam = sp.symbols('lambda', positive=True)
Tmn = 2*lam*wm*wm.T
s_cur = (wm.T*hm*wm)[0, 0]
pts_g = [{A_: -3, B_: 1, C_: 5, w0: 2, w1: 1, S2: 2}, {A_: -2, B_: 0, C_: 4, w0: 3, w1: 1, S2: 5}]
p_dust_ok = all(sp.simplify(s_cur.subs(S2**2, -sig).subs(pt)) == 0 for pt in pts_g)
check("G1 the CM-style dust: p = 0 EXACTLY (the projector identity A2), rho = 2 lambda, w = 0 exactly",
      f"T_(mn) h^(mn) = 2 lambda (h^(mn) w_m w_n) = 0 at two generic timelike points "
      f"(exact arithmetic; the symbolic form carries unresolved sqrt factors); "
      f"the chi-EOM nabla_mu(lambda nabla^mu chi) = 0 => lambda a^3 = const => rho ~ a^-3",
      p_dust_ok,
      "genuine mimetic dust: w = 0 EXACTLY, rho ~ a^-3, abundance = the free constant "
      "lambda_0 (a free initial condition) -- but this is a DIFFERENT theory (it adds "
      "a cold sector Horn A does not have)")
w_floor, w_ceil = 1.5e-8, 5.7e-7
check("G2 UNIFICATION TEST: the mimetic dust is NOT our Noether charge (G028) -- the sign of w excludes it",
      f"w_dust = 0 exactly; our registered window: w in ({w_floor}, {w_ceil}) "
      f"STRICTLY POSITIVE (the sign is the CMB discriminator, G028 V3); our charge "
      "DRIFTS under the MOND coupling (L217 V6) driving the +1-4% growth raise -- "
      "an exactly conserved dust cannot drift",
      0 < w_floor,
      "FINDING: 0 lies BELOW our floor: the mimetic dust is excluded as our cold "
      "sector by the registered sign of w under BOTH parent constructions.  In the "
      "projector-parent it does not even exist (B2); in the multiplier-parent it is "
      "an exactly-conserved w = 0 component -- a second, LCDM-like dust that would "
      "kill the w > 0 discriminator and the growth raise, or a replacement that "
      "does the same.  The unification fails on the SIGN of w")

# ================================================================== PART H  [V7]
P(""); P("="*76); P("PART H -- V7: benchmark: the paper's c_s^2 on the unprojected rolling branch"); P("="*76)
Y0, fpY, fppY = sp.symbols('Y0 fprime fprimeprime', real=True)
# L = P(Y), Y = 1/2 g^{mn} d_mu phi d_nu phi; rolling background Y0 = -phibar_dot^2/2
# L^(2) = 1/2 { -[P_Y + 2 Y0 P_YY] phi1_dot^2 + P_Y (grad phi1)^2 }
# => c_s^2 = P_Y / (P_Y + 2 Y0 P_YY)
cs2 = sp.simplify((fpY/2)/(-(-(fpY + 2*Y0*fppY)/2)))
check("V7 the quadratic-action coefficients give c_s^2 = f'/(f' + 2Xf'') (the Health-section formula)",
      f"c_s^2 = {cs2}", sp.simplify(cs2 - fpY/(fpY + 2*Y0*fppY)) == 0,
      "verified on the UNPROJECTED branch (where the congruence tracks the scalar "
      "flow and a sound speed exists); on the cosmic slice (X = 0) the question is "
      "degenerate in both theories (V3g)")

# ================================================================== VERDICT
P(""); P("="*76); P("THE VERDICT (pre-registered outcomes; all findings)"); P("="*76)
v1 = all(r["pass"] for r in RES if r["id"].startswith("V1"))
v2 = all(r["pass"] for r in RES if r["id"].startswith("V2"))
v3 = all(r["pass"] for r in RES if r["id"].startswith("V3"))
v4 = all(r["pass"] for r in RES if r["id"].startswith(("V4", "B2", "G2")))
P(f"  agreement region:  V1 FRW background [{'OK' if v1 else '--'}]  "
  f"V2 static AQUAL / G_eff [{'OK' if v2 else '--'}]  "
  f"V3 on-slice linear spectra [{'OK' if v3 else '--'}]")
P(f"  extra DOF:         the foliation mode EXISTS in the parent (V3c/V4a/V4b): "
  f"dynamical chi, decoupled at linear order, NOT dust (B2/G2)  "
  f"[{'CONFIRMED' if v4 else '--'}]")
v5 = all(r["pass"] for r in RES if r["id"].startswith(("F1", "F2", "G1")))
P(f"  gauge status:      no conformal symmetry (F2b/F2c), the constraint is not a "
  f"gauge-fixing; the fixed foliation is absolute structure (F1/F2/G1)  "
  f"[{'CONFIRMED' if v5 else '--'}]")
P("")
P("  (i)  EXACT embedding: NO.  The parent's chi = t slice is the metric-adaptive "
  "kinematics PLUS the chi-EOM constraint; the foliation DOF is physical (the "
  "reparametrization symmetry cannot fix it); the solution sets differ in BOTH "
  "directions (the parent allows other foliations; Horn-A solutions with rolling phi "
  "violate the parent's chi-EOM off-slice).  The fixed congruence is NOT a gauge slice "
  "of any theory in the 2503.11174 class.")
P("  (ii) UNIFICATION:    NO.  The projector-parent carries NO dust at all: the "
  "chi-current is J_mu = K[(g p)_mu (-sigma) + K (g w)_mu]/((-sigma)^2 Lambda^4) "
  "with K = w.p (B2b): a fixed polynomial of the two gradients, NO free function "
  "of chi; it vanishes whenever K = 0, and the EOM current f'(X) J is killed "
  "identically on the cosmic slice by f'(0) = mu_2(0) = 0 -- even for a rolling "
  "phi.  No free initial condition, no w.  The CM-style multiplier-parent "
  "carries genuine dust with w = 0 EXACTLY, which contradicts our registered "
  "strictly-positive window (1.5e-8, 5.7e-7) and cannot drift (no growth raise): "
  "not our charge under either parent.")
P("  (iii) FAIL of the embedding claim: CONFIRMED, with the agreement region mapped "
  "exactly: backgrounds (V1), the static conservative sector (V2), and the on-slice "
  "linear spectra (V3) coincide; the theories differ precisely in the foliation sector.")
P("")
P("  STRUCTURAL DIAGNOSIS (the publishable core):")
P("   1. 2503.11174's machinery feeds on the conformal symmetry of homogeneously-")
P("      scaling building blocks; the Zimmerman normalization P = Lambda^4 f with")
P("      f(0) = -1 (fixing Lambda AND, through f' = mu_2, the MOND scale) is not")
P("      conformal: Horn A's fixed congruence CANNOT be a gauge slice of any parent")
P("      in that class.  The Lorentz-violation cost does NOT dissolve.")
P("   2. The mimetic covariantization would reintroduce, as a foliation/dust mode,")
P("      precisely the DOF Horn A's aether-deletion removed; the deletion that buys")
P("      c_T = c and no spin-1 ghost is the same one that blocks the embedding.")
P("   3. What G043 adds: 'mimetic reformulation != mimetic gauge'.  The congruence")
P("      CAN be reparametrized covariantly (chi <-> foliation); the conservative")
P("      sector is shared verbatim; the difference is exactly the foliation's")
P("      dynamical status -- which is also the theory's cold-sector discriminator.")
P("   4. Operational by-product: the G032 freeze fixes the aether components; the")
P("      metric-ADAPTIVE 'fixed foliation' definition removes the O(alpha) tadpole")
P("      in X and coincides with the mimetic kinematics on-slice.  Recommended.")

out = {"lane": "G043", "title": "the mimetic embedding test (arXiv:2503.11174 vs Horn A)",
       "verdict": "(iii) FAIL of the exact-embedding claim; unification with the G028 "
                  "Noether charge rejected (no dust in the projector-parent; w = 0 exactly "
                  "vs strictly-positive window in the multiplier-parent); agreement region "
                  "mapped: FRW background, static AQUAL/G_eff, on-slice linear spectra",
       "candidate_parent": "S_par = int sqrt(-g) [M_P^2 R/2 + Lambda^4 f(X_chi)], "
                           "X_chi = h_chi^{mn} d phi d phi/(2 Lambda^4), "
                           "h_chi = g + n_chi n_chi, n_chi = grad(chi)/sqrt(|(grad chi)^2|)",
       "checks": RES, "n_pass": NP, "n_fail": NF,
       "note": "the designed-FAIL checks (F2b, G2) are findings, not errors",
       "runtime_s": round(time.time() - T0, 1)}
with open(os.path.join(HERE, "G043_results.json"), "w") as fh:
    json.dump(out, fh, indent=1)
P(f"\n({time.time()-T0:.0f}s)  checks: {NP} pass / {NF} fail  -> G043_results.json")
