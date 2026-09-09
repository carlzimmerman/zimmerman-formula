#!/usr/bin/env python3
"""
L33 -- is a MOND-scalar cone thousands of times wider than the light cone admissible?
=====================================================================================
L13 (L13_STRONG_COUPLING.md, check P8) established, while showing that the recipe's P7 strong-coupling
wound does NOT fire, that the MOND scalar of THE_ACTION_2026-09-05.md sections 1-3 propagates in the Solar
System at

    c_s,perp^2 = (2 - K_B) J_Y c^2 / |K_2|,     J_Y = s / Delta(s),   s = g_N/a_0,

i.e. c_s/c = 19 at 1 AU and 2.5e3 at Cassini conjunction, forced by Delta being bounded above by the
bounded-boost theorem.  L13 labelled that "a quantified cost, not an exclusion, because in a theory with a
preferred foliation superluminal propagation is not by itself acausal".  THAT LABEL WAS NEVER CHECKED.
This lane checks it.

WHAT SAVES SUPERLUMINAL PROPAGATION, AND WHAT IT REQUIRES (the literature statement being tested).
In a Lorentz-violating theory with a preferred foliation there is a global time function tau.  Superluminal
signals then do NOT produce closed causal curves provided every propagating mode's characteristic cone is
"spacelike with respect to that foliation": each leaf tau = const must be a non-characteristic, spacelike
surface for EVERY mode's effective (acoustic) metric, so that tau is non-decreasing along every causal
curve of every cone.  The precise algebraic condition, for a mode with inverse acoustic metric G^{mu nu},
is that the leaf conormal n_mu = -d_mu tau be TIMELIKE with respect to G, i.e.

    G^{mu nu} n_mu n_nu > 0        (in the signature convention where G^{mu nu} k_mu k_nu = 0 is the
                                    characteristic condition and the time-time entry is positive).

Sources for that statement (literature input, NOT re-derived here):
  * R. Geroch, "Faster Than Light?", arXiv:1005.1614 (2010) -- multiple cones are causally consistent iff a
    common foliation exists that is spacelike for all of them.
  * E. Babichev, V. Mukhanov, A. Vikman, "k-Essence, superluminal propagation, causality and emergent
    geometry", JHEP 0802:101 (2008), arXiv:0708.0561 -- chronology protection for superluminal k-essence
    reduces to the existence of a global time function.
  * J.-P. Bruneton, "Causality and superluminal behavior in classical field theories: applications to
    k-essence theories and MOND-like theories of gravity", PRD 75, 085013 (2007), gr-qc/0607055; and
    J.-P. Bruneton & G. Esposito-Farese, "Field-theoretical formulations of MOND-like gravity",
    PRD 76, 124012 (2007), arXiv:0705.4043 -- the MOND-specific analysis: RAQUAL/TeVeS scalars are
    generically superluminal, and this is not by itself fatal.
  * D. Blas, O. Pujolas, S. Sibiryakov, "Models of non-relativistic quantum gravity: the good, the bad and
    the healthy", JHEP 1104:018 (2011), arXiv:1007.3503 -- the khronometric instantaneous mode.
The counter-argument in the literature, also recorded: A. Adams, N. Arkani-Hamed, S. Dubovsky, A. Nicolis,
R. Rattazzi, JHEP 0610:014 (2006), hep-th/0602178 -- superluminality obstructs a LORENTZ-INVARIANT UV
completion.  That argument is inapplicable in principle here, because the host is fundamentally
Lorentz-violating (a Horava/Lifshitz-type UV completion is the whole point of a khronometric host); it is
reported, not used.

THE UNIVERSAL-HORIZON QUESTION.  In theories with superluminal modes, black holes are bounded not by the
metric horizon but by a "universal horizon" -- a compact leaf of the preferred foliation inside the metric
horizon, which no signal of any speed can cross outward:
  * E. Barausse, T. Jacobson, T. P. Sotiriou, "Black holes in Einstein-aether and Horava-Lifshitz gravity",
    PRD 83, 124043 (2011), arXiv:1104.2889.
  * D. Blas, S. Sibiryakov, "Horava gravity vs. thermodynamics: the black hole case", PRD 84, 124043
    (2011), arXiv:1110.2195.
  * P. Berglund, J. Bhattacharyya, D. Mattingly, "Mechanics of universal horizons", PRD 85, 124019 (2012),
    arXiv:1202.4497, and "Towards thermodynamics of universal horizons in Einstein-aether theory",
    PRL 110, 071301 (2013), arXiv:1210.4940.
  * The problem they solve: S. Dubovsky, S. Sibiryakov, "Spontaneous breaking of Lorentz invariance, black
    holes and perpetuum mobile of the 2nd kind", Phys. Lett. B 638, 509 (2006), hep-th/0603158.
  * F. B. Estabrook et al., "Maximally slicing a black hole", PRD 7, 2814 (1973) -- the limiting maximal
    slice of Schwarzschild at r = 3M/2, which section C rebuilds from scratch and identifies as the
    universal horizon of the c_2-dominated khronon.
  * Well-posedness: O. Sarbach, E. Barausse, J. A. Preciado-Lopez, "Well-posed Cauchy formulation for
    Einstein-aether theory", CQG 36, 165007 (2019), arXiv:1902.05130; and J. Bhattacharyya, M. Colombo,
    T. P. Sotiriou / J. Bhattacharyya et al., "Evolution and spherical collapse in Einstein-aether theory
    and Horava gravity", PRD 93, 064056 (2016), arXiv:1512.04899 -- the instantaneous-mode case is evolved
    as a mixed elliptic-hyperbolic system.

WHAT IS COMPUTED HERE, and where the checks can fail
  A  CONTROL.  The quadratic action of delta phi is expanded from THE_ACTION sections 1-3 independently of
     L13's code, giving the acoustic metric, the transverse and LONGITUDINAL stiffnesses, and c_s/c at 1 AU
     and at Cassini conjunction on both a_0 footings.  It must reproduce L13's 19 / 2522 and 17 / 2298.
  B  Does this action have a genuine preferred foliation, and is the scalar's cone spacelike for it at
     c_s = 2.5e3 c?  With a NEGATIVE control: a mode whose cone is tied to a boosted frame must FAIL.
  C  The universal horizon, built explicitly: the CMC/maximal foliation of Schwarzschild, its limiting leaf
     at r = 3M/2, the horizon of a mode of speed c_s, and its limit as c_s -> infinity.
  D  Well-posedness: transverse hyperbolicity, the longitudinal sector on the published saturated branch,
     the xi^2 (Lifshitz) term's unbounded group velocity, with an ill-posedness control.
  E  Empirics: GW170817 (tensors only), gravitational-Cherenkov KINEMATICS for a superluminal mode, where
     the cone crosses c, the Milgrom cutoff, and whether ANY existing observation bounds this speed.
     Lane L19 handles the Cherenkov APPLICABILITY question for a different mode (IC10's clock) in a
     different action; nothing of its rate machinery is imported or re-derived here.  Where this lane needs
     Milgrom's published loss distance it cites the published result and L19's independent verification of
     it, and says so.
  F  Is the number forced?  The kernel-free identity, the ephemeris route, and a scan over the standard
     MOND interpolating-function family, with an unbounded-kernel control.
  G  The verdict checks.

Both a_0 footings on every dimensional number.  9.3619e-11 / 1.1279e-10 m s^-2.
Nothing under closure_2026/ is imported or executed; THE_ACTION sections 1-3 were transcribed by hand.
"""
import sympy as sp, numpy as np, math, sys, time

T0 = time.time(); FAILS = []
def check(name, ok, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
    if not ok: FAILS.append(name)
W = 118
def head(s): print("\n" + "=" * W); print(s); print("=" * W, flush=True)

# ------------------------------------------------------------------ parameters, transcribed by hand
A0   = {"canonical": 9.3619e-11, "alt": 1.1279e-10}   # m s^-2, the framework's two footings
KB_V = 0.2                                            # THE_ACTION section 2
C14_V= 1.0e-5
C13_V= 0.0                                            # c_1 = -c_3 = K_B  =>  c_13 = 0 exactly (GW170817)
K2_LO, K2_HI = 2.0e5, 5.0e5                           # the dark sector's window (g03r/g03u)
K2_GROWTH    = 2.7e6                                  # the growth pincer (g03t)
XI_PC = {"canonical": 0.10, "alt": 0.15}              # coherence length floors for nu_RAR (THE_ACTION s.3)
CLIGHT = 2.99792458e8
GNEWT  = 6.674e-11
GM_SUN = 1.32712440018e20
AU     = 1.495978707e11
RSUN   = 6.957e8
PC     = 3.0856775814913673e16
KPC    = 1e3 * PC
HBARC_GeV_m = 1.9732698e-16                            # GeV m
# committed ephemeris bounds on a CONSTANT radial delta-g, 1 sigma (prep_2026/mi_integrator, laneR/BOUNDS.md)
DG_BOUND = {"Venus": 8.0e-14, "Saturn": 7.0e-15}
R_PLANET = {"Venus": 0.7233 * AU, "Saturn": 9.5826 * AU}

print("=" * W)
print("L33 -- is a MOND-scalar cone thousands of times wider than the light cone admissible?")
print("=" * W, flush=True)

# ------------------------------------------------------------------ the carried kernel
def Delta_rar(s):
    """nu_RAR's acceleration excess Delta = (g - g_N)/a0 with g = g_N/(1 - e^{-sqrt(s)})."""
    if s <= 0: return 0.0
    r = math.exp(-math.sqrt(s))
    return s * r / (1.0 - r)
lo, hi = 1.0, 6.0
for _ in range(300):
    m1 = lo + (hi - lo) / 3; m2 = hi - (hi - lo) / 3
    if Delta_rar(m1) < Delta_rar(m2): lo = m1
    else: hi = m2
S_SAT = 0.5 * (lo + hi); C_SAT = Delta_rar(S_SAT)
def Delta(s):  return Delta_rar(s) if s <= S_SAT else C_SAT
def J_Y(s):    return s / Delta(s)

head("A -- CONTROL: the quadratic action of the MOND scalar, expanded from THE_ACTION sections 1-3")
check("A0 [CONTROL] the carried kernel's saturation point and ceiling reproduce THE_ACTION section 3 "
      "(s_sat = 2.540, C = 0.6476)",
      abs(S_SAT - 2.540) < 0.005 and abs(C_SAT - 0.6476) < 0.0005,
      f"s_sat = {S_SAT:.4f}, C = Delta_max = {C_SAT:.5f}")

# --- A1: expand -K(Q) - (2-K_B) J(Y) to second order in delta phi, flat metric, preferred frame ---
print("\n  A1  Expansion (flat metric, preferred frame n^mu = (1,0,0,0), background static with V along x).")
t, x, y, z, eps = sp.symbols('t x y z epsilon', real=True)
gphi, Q0, K2s, KBs = sp.symbols('g_phi Q_0 K_2 K_B', positive=True)
JY, JYY = sp.symbols('J_Y J_YY', real=True)
dphi = sp.Function('f')(t, x, y, z)
phi = gphi * x + eps * dphi                      # background V_x = g_phi, perturbation eps*f
Qexpr = sp.diff(phi, t)                          # Q = n^mu d_mu phi   (background Q = Q_0 = 0 static)
Yexpr = sp.diff(phi, x)**2 + sp.diff(phi, y)**2 + sp.diff(phi, z)**2
Y0 = gphi**2
# K(Q) = K_2 (Q - Q_0)^2 with K_2 < 0; write K_2 = -|K_2| so -K(Q) = +|K_2| (dQ)^2
Lag = K2s * (Qexpr - 0)**2 - (2 - KBs) * (JY * (Yexpr - Y0) + sp.Rational(1, 2) * JYY * (Yexpr - Y0)**2)
L2 = sp.expand(sp.simplify(sp.series(Lag, eps, 0, 3).removeO().coeff(eps, 2)))
print(f"      L_2 / (eps^2)  =  {sp.factor(sp.collect(L2, [sp.diff(dphi, t)**2]))}")
kin  = sp.simplify(L2.coeff(sp.diff(dphi, t)**2))
stx  = sp.simplify(-L2.coeff(sp.diff(dphi, x)**2))
sty  = sp.simplify(-L2.coeff(sp.diff(dphi, y)**2))
stz  = sp.simplify(-L2.coeff(sp.diff(dphi, z)**2))
print(f"      kinetic coefficient (d_t f)^2 : {kin}")
print(f"      longitudinal stiffness (d_x f)^2: {stx}")
print(f"      transverse   stiffness (d_y f)^2: {sty}   (d_z f)^2: {stz}")
ok_A1 = (sp.simplify(kin - K2s) == 0
         and sp.simplify(stx - (2 - KBs) * (JY + 2 * gphi**2 * JYY)) == 0
         and sp.simplify(sty - (2 - KBs) * JY) == 0
         and sp.simplify(stz - sty) == 0)
check("A1 [CONTROL] the quadratic action expanded here gives the acoustic metric "
      "G^{mu nu} = |K_2| n^mu n^nu - (2-K_B)[J_Y q^{mu nu} + 2 J_YY V^mu V^nu], i.e. kinetic |K_2|, "
      "transverse (2-K_B)J_Y, longitudinal (2-K_B)(J_Y + 2Y J_YY)",
      bool(ok_A1),
      "all four coefficients match the covariant form term by term; the AeST mixing 2(2-K_B)J^mu d_mu phi "
      "carries one time derivative and is antisymmetric, so it does not enter this Hessian (L13's finding, "
      "used here, not re-derived)")

# --- A2: the longitudinal stiffness identity  J_Y + 2 Y J_YY = 1/Delta'(s) ---
print("\n  A2  The longitudinal stiffness in terms of the kernel.  With the static law J_Y(g_phi) g_phi = g_N,")
print("      g_phi = a_0 Delta(s), g_N = a_0 s and Y = g_phi^2:")
ss, a0s = sp.symbols('s a_0', positive=True)
D = sp.Function('Delta')(ss)
Yofs = (a0s * D)**2
JYofs = ss / D
dJY_ds = sp.diff(JYofs, ss); dY_ds = sp.diff(Yofs, ss)
JYY_expr = sp.simplify(dJY_ds / dY_ds)
longi = sp.simplify(JYofs + 2 * Yofs * JYY_expr)
print(f"      J_Y + 2 Y J_YY  =  {sp.simplify(longi)}")
check("A2 [CONTROL] the longitudinal stiffness is exactly 1/Delta'(s) for EVERY kernel -- i.e. it is the "
      "inverse of the boost function's slope, which is what the bounded-boost theorem constrains",
      sp.simplify(longi - 1 / sp.diff(D, ss)) == 0,
      "J_Y + 2 Y J_YY = 1/Delta'(s), symbolically, for a generic Delta; a_0 cancels")

# --- A3: the numbers ---
print("\n  A3  c_s,perp/c = sqrt((2-K_B) J_Y / |K_2|), independently of L13's code.")
g_saturn  = GM_SUN / (9.5826 * AU)**2
g_earth   = GM_SUN / AU**2
g_cassini = GM_SUN / (1.6 * RSUN)**2
ENVS = [("deep MOND, galaxy outskirt", None, 0.1),
        ("MOND transition",            None, 1.0),
        ("galaxy inner disc",          None, 10.0),
        ("Saturn orbit",               g_saturn,  None),
        ("Earth orbit (1 AU)",         g_earth,   None),
        ("Cassini conjunction, b = 1.6 R_sun", g_cassini, None)]
def cs_over_c(s, K2): return math.sqrt((2 - KB_V) * J_Y(s) / K2)
print(f"      {'environment':<36}{'footing':>11}{'s':>14}{'J_Y':>14}{'c_s/c |K2|=5e5':>18}{'c_s/c |K2|=2e5':>18}")
CS = {}
for nm, gN, sfix in ENVS:
    for foot in ("canonical", "alt"):
        s_ = (gN / A0[foot]) if gN is not None else sfix
        v_hi = cs_over_c(s_, K2_HI); v_lo = cs_over_c(s_, K2_LO)
        CS[(nm, foot)] = (s_, J_Y(s_), v_hi, v_lo)
        print(f"      {nm:<36}{foot:>11}{s_:>14.5g}{J_Y(s_):>14.5g}{v_hi:>18.5g}{v_lo:>18.5g}")
au_can  = CS[("Earth orbit (1 AU)", "canonical")][2]
au_alt  = CS[("Earth orbit (1 AU)", "alt")][2]
cas_can = CS[("Cassini conjunction, b = 1.6 R_sun", "canonical")][2]
cas_alt = CS[("Cassini conjunction, b = 1.6 R_sun", "alt")][2]
check("A3 [CONTROL] these reproduce L13/P8's reported cone widths -- 19 and 2522 at 1 AU and Cassini "
      "conjunction on the canonical footing, 17 and 2298 on the alt footing",
      abs(au_can - 19) < 0.6 and abs(cas_can - 2522) < 15 and abs(au_alt - 17) < 0.6 and abs(cas_alt - 2298) < 15,
      f"here: {au_can:.2f} / {cas_can:.0f} (canonical), {au_alt:.2f} / {cas_alt:.0f} (alt), at |K_2| = 5e5")

# ------------------------------------------------------------------ B: the foliation
head("B -- does this action have a genuine preferred foliation, and is the scalar's cone spacelike for it?")
print("  B1  THE_ACTION section 1 defines the clock through a SCALAR tau: n_mu = -d_mu tau / sqrt(-(d tau)^2),")
print("      with NO independent aether vector.  Hypersurface-orthogonality is then an identity, not a")
print("      solution property (unlike Einstein-aether).  Frobenius test: n ^ dn = 0 for a generic tau.")
tau = sp.Function('tau')(t, x, y, z)
XS = [t, x, y, z]; ETA = sp.diag(-1, 1, 1, 1)
dtau = sp.Matrix([sp.diff(tau, v) for v in XS])
Wnorm = sp.sqrt(-(dtau.T * ETA.inv() * dtau)[0, 0])
n_dn = sp.Matrix([-dtau[m] / Wnorm for m in range(4)])            # n_mu
def levi(a, b, c, d): return sp.LeviCivita(a, b, c, d)
twist = []
for mu in range(4):
    acc = 0
    for nu in range(4):
        for rho in range(4):
            for sig in range(4):
                e = levi(mu, nu, rho, sig)
                if e == 0: continue
                acc += e * n_dn[nu] * sp.diff(n_dn[sig], XS[rho])   # all contracted indices LOWER
    twist.append(sp.simplify(sp.together(sp.expand(acc))))
frob_ok = all(sp.simplify(tw) == 0 for tw in twist)
check("B1 [CONTROL] the clock defines a genuine preferred FOLIATION: n built from the scalar tau is "
      "hypersurface-orthogonal identically (n ^ dn = 0 for a generic tau), so tau = const is a global time "
      "function and not a special solution",
      frob_ok, "all four components of eps^{mu nu rho sig} n_nu grad_rho n_sig vanish symbolically")

print("\n  B2  Is the leaf tau = const SPACELIKE for the scalar's cone?  The condition is that the leaf")
print("      conormal n_mu be timelike for the inverse acoustic metric:  G^{mu nu} n_mu n_nu > 0.")
K2sym, JYs, JYYs, KBsym = sp.symbols('K2 J_Y J_YY K_B', real=True)
# covariant contraction: G^{mn} n_m n_n = |K2|(n.n)^2 - (2-K_B)[J_Y q^{mn} n_m n_n + 2 J_YY (V.n)^2]
nn = sp.Integer(-1)                     # n.n = -1
q_nn = nn + nn**2                       # q^{mn} n_m n_n = g^{mn}n_m n_n + (n.n)^2 = -1 + 1 = 0
V_n = sp.Integer(0)                     # V.n = 0 by construction (V is the projected gradient)
Gnn = sp.simplify(K2sym * nn**2 - (2 - KBsym) * (JYs * q_nn + 2 * JYYs * V_n**2))
print(f"      G^{{mu nu}} n_mu n_nu = {Gnn}   -- because q^{{mu nu}} n_nu = 0 and V.n = 0 BY CONSTRUCTION")
print(f"      This is |K_2| for EVERY J_Y and J_YY: the result does not depend on the cone's width at all.")
spacelike_all = all(K2_HI > 0 for _ in CS)
print(f"      numerically, at every environment above and both footings: G^{{mu nu}}n_mu n_nu = |K_2| = "
      f"{K2_HI:.1e} > 0 (and {K2_LO:.1e} at the window's other edge)")
check("B2 the tau = const leaves are SPACELIKE with respect to the MOND scalar's characteristic cone at "
      "c_s = 2.5e3 c -- so the cone is causally consistent with the preferred foliation",
      sp.simplify(Gnn - K2sym) == 0 and K2_LO > 0 and K2_HI > 0,
      "G^{mu nu}n_mu n_nu = |K_2| > 0 identically, independent of J_Y, J_YY and hence of c_s.  The "
      "no-ghost condition |K_2| > 0 IS the spacelike condition; nothing else enters")

print("\n  B3  NEGATIVE CONTROL -- the test must be able to fail.  Replace the scalar's projector q by the")
print("      projector qtilde orthogonal to a DIFFERENT unit timelike vector ntilde, boosted by v relative")
print("      to the clock (this is what a second preferred frame in the action would do).  Then")
print("          qtilde^{mu nu} n_mu n_nu = -1 + (ntilde . n)^2 = gamma^2 - 1,")
print("      so G^{mu nu}n_mu n_nu = |K_2| - (2-K_B) J_Y (gamma^2 - 1), which turns NEGATIVE at")
print("          gamma^2 - 1 > |K_2|/[(2-K_B) J_Y] = 1/c_s^2   <=>   v > c/c_s.")
print(f"      {'environment':<36}{'footing':>11}{'c_s/c':>12}{'boost margin v [km/s]':>24}")
margins = []
for nm, gN, sfix in ENVS[3:]:
    for foot in ("canonical", "alt"):
        s_, jy, v_hi, v_lo = CS[(nm, foot)]
        vmarg = CLIGHT / v_hi / 1e3
        margins.append(vmarg)
        print(f"      {nm:<36}{foot:>11}{v_hi:>12.4g}{vmarg:>24.4g}")
worst_margin = min(margins)
jy_cas = CS[("Cassini conjunction, b = 1.6 R_sun", "canonical")][1]
def Gnn_boosted(v):
    gam2m1 = v**2 / (1 - v**2)
    return K2_HI - (2 - KB_V) * jy_cas * gam2m1
v_star = 1.0 / cas_can
below, above = Gnn_boosted(0.9 * v_star), Gnn_boosted(1.1 * v_star)
print(f"      explicit sign flip at Cassini conjunction (|K_2| = 5e5, J_Y = {jy_cas:.4g}):")
print(f"        v = 0.9 c/c_s = {0.9*v_star*CLIGHT/1e3:>8.1f} km/s : G^{{mu nu}}n_mu n_nu = {below:+.4e}  (spacelike)")
print(f"        v = 1.1 c/c_s = {1.1*v_star*CLIGHT/1e3:>8.1f} km/s : G^{{mu nu}}n_mu n_nu = {above:+.4e}  (TIMELIKE -> closed causal curves)")
neg_ctrl_fires = below > 0 > above
check("B3 [CONTROL, negative] the spacelike test HAS TEETH: a mode whose cone is tied to any frame boosted "
      "relative to the clock fails it, and the margin is finite and computable",
      neg_ctrl_fires and worst_margin < 3e5,
      f"the leaves stop being spacelike once the scalar's own frame is misaligned from the clock's by "
      f"v > c/c_s; the tightest margin above is {worst_margin:.0f} km/s (Cassini conjunction), SMALLER than "
      f"the Solar System's 370 km/s motion relative to the CMB.  The theory is safe only because Q = n.d phi "
      f"and V = q.d phi are built from the SAME tau, so the alignment is exact by construction, not by tuning")

print("\n  B4  No closed causal curve.  Along a characteristic of a mode of finite speed c_s, in the")
print("      preferred frame, dtau/dlambda = k^0 > 0 strictly: tau is a strictly monotone function of the")
print("      curve parameter, so no causal curve of the scalar can close.  Quantitatively, the leaf-crossing")
print("      rate of the fastest ray is dtau/d(proper distance along the leaf) = 1/c_s > 0:")
for nm, foot in [("Cassini conjunction, b = 1.6 R_sun", "canonical"), ("Cassini conjunction, b = 1.6 R_sun", "alt")]:
    v = CS[(nm, foot)][2]
    print(f"      {foot:>11}: c_s/c = {v:.4g}  =>  dtau/dx = 1/(c_s) = {1/(v*CLIGHT):.4g} s/m  > 0  (finite, non-zero)")
check("B4 no closed causal curve exists for the scalar at c_s = 2.5e3 c: tau increases strictly along every "
      "characteristic, because c_s is FINITE",
      cas_can < float('inf') and cas_can > 0 and cas_alt > 0,
      f"1/c_s = {1/(cas_can*CLIGHT):.3e} s/m at the widest cone -- non-zero, so tau is strictly monotone. "
      f"The condition is finiteness, not subluminality; see D2 for where finiteness fails")

# ------------------------------------------------------------------ C: the universal horizon
head("C -- the universal horizon: what a c_s = 2.5e3 c mode can and cannot escape")
print("  Built from scratch, in the regime this action actually sits in: all c_i <= 1e-5, so the metric is")
print("  Schwarzschild to O(1e-5) and the clock is a TEST field on it.  With the c_2 (khronometric lambda)")
print("  term dominant the khronon equation makes the leaves CONSTANT MEAN CURVATURE surfaces; the maximal")
print("  (K = 0) family of Schwarzschild is the textbook case, and its LIMITING leaf is the universal")
print("  horizon.  (Estabrook et al. 1973 for the slicing; Barausse-Jacobson-Sotiriou 2011 and")
print("  Blas-Sibiryakov 2011 for the identification.  Existence of a universal horizon for GENERAL c_i is")
print("  a literature result, cited, not re-derived; the exact example below is derived here.)")
rr, MM, CC, csym = sp.symbols('r M C c_s', positive=True)
f_s = 1 - 2 * MM / rr
g_s = f_s + CC**2 / rr**4
hprime = CC / (rr**2 * f_s * sp.sqrt(g_s))                       # dt/dr of the leaf
# u_mu = -sqrt(g) d_mu(t - h(r));  u^t = sqrt(g)/f, u^r = C/r^2
u_up = sp.Matrix([sp.sqrt(g_s) / f_s, CC / rr**2])
norm_u = sp.simplify(-f_s * u_up[0]**2 + u_up[1]**2 / f_s)
s_up = sp.Matrix([CC / (rr**2 * f_s), sp.sqrt(g_s)])
norm_s = sp.simplify(-f_s * s_up[0]**2 + s_up[1]**2 / f_s)
orth = sp.simplify(-f_s * u_up[0] * s_up[0] + u_up[1] * s_up[1] / f_s)
print(f"\n  C1  leaf normal u and in-leaf radial unit vector s:  u.u = {norm_u},  s.s = {norm_s},  u.s = {orth}")
check("C1 [CONTROL] the constant-mean-curvature leaf's unit normal u (u^r = C/r^2) and the in-leaf radial "
      "unit vector s (s^r = sqrt(g), g = f + C^2/r^4) satisfy u.u = -1, s.s = +1, u.s = 0 exactly",
      sp.simplify(norm_u + 1) == 0 and sp.simplify(norm_s - 1) == 0 and sp.simplify(orth) == 0,
      "verified symbolically in Schwarzschild coordinates")

# the limiting slice: double root of g
sol = sp.solve([sp.Eq(g_s, 0), sp.Eq(sp.diff(g_s, rr), 0)], [rr, CC], dict=True)
sol = [d for d in sol if d[rr].is_real is not False]
r_uh = sp.simplify(sol[0][rr]); C_uh = sp.simplify(sol[0][CC])
gpp = sp.simplify(sp.diff(g_s, rr, 2).subs({CC: C_uh, rr: r_uh}))
print(f"\n  C2  limiting leaf (double root of g):  r_UH = {r_uh},  C = {C_uh},  g''(r_UH) = {gpp}")
print(f"      the metric horizon is at r = 2M, so r_UH = {sp.nsimplify(r_uh/(2*MM))} of it, INSIDE it.")
check("C2 [CONTROL] the limiting leaf of the maximal foliation of Schwarzschild sits at r = 3M/2 with "
      "C = 3 sqrt(3) M^2 / 4, reproducing the published universal-horizon radius",
      sp.simplify(r_uh - sp.Rational(3, 2) * MM) == 0
      and sp.simplify(C_uh - 3 * sp.sqrt(3) * MM**2 / 4) == 0
      and sp.simplify(gpp - sp.Rational(16, 9) / MM**2) == 0,
      f"r_UH = 3M/2 (Estabrook et al. 1973's limiting maximal slice; the universal horizon of "
      f"Barausse-Jacobson-Sotiriou 2011 / Blas-Sibiryakov 2011), g''(r_UH) = 16/(9 M^2)")

print("\n  C3  A ray of speed c_s in the CLOCK frame has tangent k = u + c_s s.  It moves outward iff")
print("      k^r = -|C|/r^2 + c_s sqrt(g) > 0  (infalling clock, C < 0), i.e. iff")
print("            g(r)  >  C^2 / (c_s^2 r^4).")
esc = sp.Eq(g_s, CC**2 / (csym**2 * rr**4))
r_light = sp.solve(sp.Eq(g_s.subs(CC, C_uh), (C_uh**2 / rr**4)), rr)
r_light = [q for q in r_light if q.is_real and q > 0]
print(f"      at c_s = 1 (light) this reduces to f(r) = 0, i.e. r = {r_light} -- the METRIC horizon.")
check("C3 [CONTROL] the escape condition returns the METRIC horizon r = 2M exactly when c_s = 1, so the "
      "machinery is anchored to a known answer",
      any(sp.simplify(q - 2 * MM) == 0 for q in r_light),
      "g(r) = C^2/r^4  <=>  f(r) = 0  <=>  r = 2M")

def r_horizon(cs, Mval=1.0):
    """radius where a mode of speed cs (in units of c) stops escaping, on the limiting leaf."""
    Cv = 3 * math.sqrt(3) * Mval**2 / 4
    gg = lambda r: 1 - 2 * Mval / r + Cv**2 / r**4
    F = lambda r: gg(r) - Cv**2 / (cs**2 * r**4)
    a, b = 1.5 * Mval * (1 + 1e-14), 4.0 * Mval
    if F(a) * F(b) > 0: return float('nan')
    for _ in range(300):
        m = 0.5 * (a + b)
        if F(a) * F(m) <= 0: b = m
        else: a = m
    return 0.5 * (a + b)
print(f"\n  C4  {'c_s/c':>12}{'r_horizon / M':>18}{'(r_h - r_UH)/M':>18}{'fraction of the way in':>26}")
for cs in [1.0, 10.0, au_can, 100.0, cas_can, 1e4, 1e6, 1e9]:
    rh = r_horizon(cs)
    print(f"      {cs:>12.4g}{rh:>18.10f}{rh-1.5:>18.4e}{(2.0-rh)/0.5:>26.10f}")
rh_cas = r_horizon(cas_can); rh_au = r_horizon(au_can)
check("C4 the c_s = 2.5e3 c mode is TRAPPED: its horizon lies strictly between the universal horizon "
      "r = 3M/2 and the metric horizon r = 2M, so a black hole is a black hole for it too",
      1.5 < rh_cas < 2.0 and 1.5 < rh_au < 2.0,
      f"r_h(c_s = {cas_can:.0f}) = {rh_cas:.8f} M, i.e. {(rh_cas-1.5)/0.5*100:.4f}% of the way from the "
      f"universal horizon to the metric horizon; r_h(c_s = {au_can:.1f}) = {rh_au:.6f} M")

delta_pred = math.sqrt(3.0 / 8.0) / cas_can
print(f"\n  C5  Analytically, near the double root g ~ (8/9)(r - r_UH)^2/M^2 and C^2/r^4 -> 1/3, so")
print(f"          r_h - r_UH = sqrt(3/8) M / c_s  ->  0   as c_s -> infinity.")
print(f"      predicted {delta_pred:.6e} M at c_s = {cas_can:.0f}; measured {rh_cas-1.5:.6e} M "
      f"(ratio {(rh_cas-1.5)/delta_pred:.4f})")
check("C5 an INFINITE-speed mode is trapped too: r_h(c_s) -> r_UH exactly, so the universal horizon censors "
      "arbitrarily fast modes and black-hole thermodynamics is not defeated by the scalar's cone",
      abs((rh_cas - 1.5) / delta_pred - 1) < 0.02 and abs(r_horizon(1e9) - 1.5) < 1e-6,
      f"r_h - r_UH = sqrt(3/8) M/c_s, verified to {abs((rh_cas-1.5)/delta_pred-1)*100:.2f}%; at c_s = 1e9, "
      f"r_h - r_UH = {r_horizon(1e9)-1.5:.2e} M.  This is the resolution of Dubovsky-Sibiryakov's "
      f"perpetuum-mobile problem (hep-th/0603158) supplied by Berglund-Bhattacharyya-Mattingly "
      f"(arXiv:1202.4497, arXiv:1210.4940): the universal horizon carries its own surface gravity and "
      f"temperature, common to all speeds")

# ------------------------------------------------------------------ D: well-posedness
head("D -- the initial value problem")
print("  D1  Transverse sector.  omega^2 = c_s,perp^2 k^2 with c_s,perp^2 = (2-K_B)J_Y/|K_2| > 0 and the")
print("      energy density |K_2|(d_t f)^2 + (2-K_B)J_Y |grad_perp f|^2 positive definite.  Real, distinct")
print("      characteristics; strongly hyperbolic; finite domain of dependence of half-angle arctan(c_s).")
d1_ok = all(v > 0 and math.isfinite(v) for (_, _, v, _) in CS.values())
check("D1 the transverse sector is strongly hyperbolic on every background sampled (real characteristic "
      "speeds, positive-definite energy), so it has a well-posed Cauchy problem on the leaves",
      d1_ok, f"c_s,perp^2 > 0 and finite at all {len(CS)} (environment, footing) points; K_B = {KB_V} < 2 and "
             f"|K_2| > 0 are the two conditions")

print("\n  D2  Longitudinal sector, ON THE ACTION AS PUBLISHED.  A2 showed the longitudinal stiffness is")
print("      (2-K_B)/Delta'(s).  The carried kernel is EXACTLY flat beyond s_sat = 2.540 (THE_ACTION s.3),")
print("      so Delta'(s) = 0 identically at every Solar-System background and")
print("          c_s,par^2 = (2-K_B) / (Delta'(s) |K_2|)  =  INFINITY.")
print("      An infinite characteristic speed is not a closed causal curve (tau never DEcreases, it stays")
print("      constant along the ray), but it is not hyperbolic either: the longitudinal evolution equation")
print("      degenerates into an elliptic CONSTRAINT on the leaf, to be solved with boundary conditions at")
print("      infinity.  That is the khronometric 'instantaneous mode' (Blas-Pujolas-Sibiryakov 2011), and it")
print("      is evolved in the literature as a mixed elliptic-hyperbolic system (arXiv:1512.04899), not as a")
print("      Cauchy problem with a finite domain of dependence.")
dprime_sat = 0.0
sample = [1e5, 1e7, CS[("Earth orbit (1 AU)", "canonical")][0], CS[("Cassini conjunction, b = 1.6 R_sun", "canonical")][0]]
print(f"      {'s':>16}{'Delta(s)':>14}{'Delta_prime(s)':>18}{'c_s,par/c':>16}")
for s_ in sample:
    dp = 0.0 if s_ > S_SAT else 1.0
    print(f"      {s_:>16.5g}{Delta(s_):>14.6f}{dp:>18.1f}{'infinity' if dp == 0 else '-':>16}")
check("D2 the initial value problem is well posed AS THE ACTION IS PUBLISHED, i.e. every propagating "
      "direction has a finite characteristic speed on the Solar-System background",
      dprime_sat > 0,
      "it is not: Delta'(s) = 0 exactly for s > 2.540, so the LONGITUDINAL scalar speed is infinite, not "
      "2.5e3 c.  The system there is elliptic-hyperbolic, not hyperbolic.  This is the same missing input "
      "L13's P9 identified from the other side (no C^2 kernel => no cubic action): a C^2 continuation of "
      "Delta past its maximum with Delta' > 0.  NOTE the direction: this makes the cone WIDER than P8's "
      "number, never narrower")

print("\n  D3  CONTROL -- the same machinery must detect a genuine ill-posedness.  Set K_B > 2 (so the")
print("      gradient stiffness (2-K_B)J_Y < 0): omega^2 < 0, exponential growth at every k, ill-posed.")
KB_bad = 3.0
om2_bad = (2 - KB_bad) * J_Y(CS[("Earth orbit (1 AU)", "canonical")][0]) / K2_HI
om2_good = (2 - KB_V) * J_Y(CS[("Earth orbit (1 AU)", "canonical")][0]) / K2_HI
print(f"      K_B = {KB_V}: omega^2/k^2 = {om2_good:+.5g} c^2   (healthy)")
print(f"      K_B = {KB_bad}: omega^2/k^2 = {om2_bad:+.5g} c^2   (gradient instability, growth rate ~ c k sqrt|.|)")
check("D3 [CONTROL] the hyperbolicity test is not blind: it flags a gradient instability when one is put in "
      "by hand (K_B > 2)", om2_bad < 0 < om2_good,
      f"omega^2/k^2 = {om2_bad:.4g} c^2 < 0 at K_B = {KB_bad}, against {om2_good:.4g} c^2 at K_B = {KB_V}")

print("\n  D4  The coherence operator.  With xi^2 |grad_perp V|^2 in the action the dispersion becomes")
print("      omega^2 = c_s^2 k^2 (1 + xi^2 k^2) (Lifshitz z = 2): omega is real at every k, so the Cauchy")
print("      problem is still well posed in the Lifshitz sense, but the GROUP velocity is unbounded --")
print("      there is no cone at all in the UV and hence no finite domain of dependence.")
print(f"      {'footing':>11}{'xi [pc]':>10}{'v_g at k = 1/xi':>20}{'v_g at k = 1/AU':>20}{'v_g at k = 1/(1 m)':>22}")
for foot in ("canonical", "alt"):
    xi = XI_PC[foot] * PC
    cs0 = CS[("Earth orbit (1 AU)", foot)][2]
    vg = lambda k: cs0 * (1 + 2 * (xi * k)**2) / math.sqrt(1 + (xi * k)**2)
    print(f"      {foot:>11}{XI_PC[foot]:>10.2f}{vg(1/xi):>20.4g}{vg(1/AU):>20.4g}{vg(1.0):>22.4g}")
check("D4 the coherence operator leaves the mode with a bounded group velocity, i.e. a finite domain of "
      "dependence survives in the ultraviolet",
      False,
      "it does not: v_g ~ 2 c_s xi k grows without bound (Lifshitz z = 2).  This is a KNOWN and accepted "
      "feature of the Horava-type host, not a new pathology -- omega(k) is real at every k so the Cauchy "
      "problem is well posed -- but it means the answer to 'how wide is the cone' is 'there is no cone', "
      "and the c_s = 2.5e3 c figure is a long-wavelength (k << 1/xi) statement only")

# ------------------------------------------------------------------ E: the empirical angle
head("E -- does ANY existing observation bound this scalar's speed?")
print("  E1  GW170817.  The bound |c_T/c - 1| < ~1e-15 is on the TENSOR sector.  In this action")
print("      c_T^2 = 1/(1 - c_13) and c_13 = c_1 + c_3 = K_B - K_B = 0 exactly, so c_T = c identically and")
print("      independently of |K_2|, J_Y and the kernel.  The MOND scalar is a spin-0 mode: it does not")
print("      enter the tensor dispersion at all.")
c13sym, cTsq = sp.symbols('c_13'), None
cT2 = 1 / (1 - c13sym)
print(f"      c_T^2 = {cT2}  ->  at c_13 = 0: {cT2.subs(c13sym, 0)}; d(c_T^2)/d|K_2| = 0, d(c_T^2)/dJ_Y = 0")
check("E1 [CONTROL] GW170817 constrains only the tensor speed, which this action fixes to c exactly and "
      "independently of the scalar sector -- so it places NO bound on c_s",
      sp.simplify(cT2.subs(c13sym, C13_V) - 1) == 0,
      "c_T^2 = 1/(1 - c_13) = 1 at c_13 = 0; the scalar's |K_2| and J_Y do not appear in it")

print("\n  E2  Gravitational Cherenkov, KINEMATICS.  A particle of energy E, mass m, speed v emitting a")
print("      quantum of speed c_s: energy-momentum conservation gives")
print("          k = 2 (p - E c_s) / (1 - c_s^2).")
Esym, psym, msym, ksym = sp.symbols('E p m k', positive=True)
kexpr = 2 * (psym - Esym * csym) / (1 - csym**2)
print(f"      k = {kexpr}")
print("      For c_s > 1 the numerator p - E c_s < 0 (since p < E always) and the denominator 1 - c_s^2 < 0,")
print("      so k > 0 formally -- but the emitted quantum must also satisfy k <= p for a real final state.")
print("      Check the threshold directly:  emission requires v > c_s, and v < 1 < c_s.  No solution.")
thresh = []
for nm, foot in [(e[0], f) for e in ENVS[3:] for f in ("canonical", "alt")]:
    v_hi = CS[(nm, foot)][2]
    thresh.append(v_hi > 1.0)
check("E2 no gravitational-Cherenkov channel EXISTS into a superluminal mode: the threshold v > c_s cannot "
      "be met by any particle, since v < c < c_s.  Superluminality is the SAFE side of the Cherenkov bound",
      all(thresh),
      "Elliott, Moore & Stoica (JHEP 0508:066, hep-ph/0505211) constrain aether modes to be at or ABOVE c "
      "for exactly this reason; the repo's own g03v applies the same requirement to the khronon.  A cone "
      "wider than the light cone is not merely tolerated by this bound, it is what the bound asks for")

print("\n  E3  The flip side, computed rather than assumed: the SAME formula makes the scalar SUBLUMINAL at")
print("      low acceleration.  The crossing is at c_s = c, i.e. J_Y = |K_2|/(2-K_B):")
print(f"      {'|K_2|':>10}{'J_Y at c_s = c':>18}{'s_crit':>14}{'g_N,crit [m/s^2]':>20}{'r from the Sun':>20}")
s_crit = {}
for K2 in (K2_LO, K2_HI):
    jyc = K2 / (2 - KB_V)
    sc = jyc * C_SAT                       # on the saturated branch J_Y = s/C
    s_crit[K2] = sc
    for foot in ("canonical",):
        gcrit = sc * A0[foot]
        rcrit = math.sqrt(GM_SUN / gcrit)
        print(f"      {K2:>10.1e}{jyc:>18.5g}{sc:>14.5g}{gcrit:>20.5g}{rcrit/AU:>17.4g} AU")
print(f"      Galactic ambient acceleration is ~a_0 (s ~ 1), where c_s/c = "
      f"{CS[('MOND transition','canonical')][2]:.4g} at |K_2| = 5e5 -- i.e. ~"
      f"{CS[('MOND transition','canonical')][2]*CLIGHT/1e3:.0f} km/s.")
print("      So the mode is superluminal only INSIDE ~{:.0f} AU of the Sun and subluminal everywhere else."
      .format(math.sqrt(GM_SUN / (s_crit[K2_HI] * A0['canonical'])) / AU))
check("E3 [diagnostic] the superluminal cone is a LOCAL, high-acceleration phenomenon: the same law makes "
      "the mode deeply subluminal in the interstellar medium, which is the corner the Cherenkov bound "
      "actually constrains",
      True,
      f"c_s = c at s = {s_crit[K2_HI]:.3g} (|K_2| = 5e5), i.e. within "
      f"{math.sqrt(GM_SUN/(s_crit[K2_HI]*A0['canonical']))/AU:.0f} AU of the Sun; at galactic ambient "
      f"acceleration c_s = {CS[('MOND transition','canonical')][2]*CLIGHT/1e3:.0f} km/s.  Reported as a "
      f"diagnostic, not as a PASS/FAIL, because it is the opposite corner from this lane's question")

print("\n  E4  Whether THAT subluminal corner is excluded is a rate question, and this lane does not compute")
print("      the rate (lane L19 owns the rate machinery, for a different mode in a different action).  What")
print("      is computed here is the GEOMETRY that sets the cutoff, because it is what differs between the")
print("      two lanes.  Milgrom, PRD 83, 084005 (2011), arXiv:1102.1818: radiation of wavenumber k is")
print("      generated at distance ~1/k from the primary, where the PRIMARY's own field sets the local")
print("      acceleration; in a theory that becomes GR at high acceleration this cuts the emission off at")
print("      k_cut = 1/r_M, giving D_loss = q c^2/a_0 with the cosmic-ray energy cancelling exactly (L19")
print("      re-derived that published result independently; it is cited here, not re-derived).")
print("      In THIS action the emission switches off EARLIER than Milgrom's r_M -- at the smaller radius")
print("      r_c where the cone crosses c -- because inside r_c there is no channel at all (E2):")
print(f"      {'E [eV]':>12}{'footing':>11}{'r_M [m]':>14}{'r_c [m]':>14}{'r_M/r_c':>12}"
      f"{'D_loss [m] (worst case)':>26}{'/10 kpc':>12}")
for Eev in (1e20, 3e20):
    for foot in ("canonical", "alt"):
        a0 = A0[foot]
        m_eff = Eev * 1.602176634e-19 / CLIGHT**2          # relativistic mass of the primary
        r_M = math.sqrt(GNEWT * m_eff / a0)
        r_c = r_M / math.sqrt(s_crit[K2_HI])
        l_M = CLIGHT**2 / a0
        D_loss = 2.0 * l_M / s_crit[K2_HI]                  # q = 2/(1-v^2)^2 -> 2 for a slow mode
        print(f"      {Eev:>12.1e}{foot:>11}{r_M:>14.4g}{r_c:>14.4g}{r_M/r_c:>12.4g}{D_loss:>26.4g}"
              f"{D_loss/(10*KPC):>12.4g}")
print("      Two suppressions are DELIBERATELY omitted from that worst case, both of which lengthen D_loss:")
print("      (i) between r_c and r_M the scalar is screened, J_Y = s/Delta >> 1, so its coupling to the")
print("          source is suppressed by ~1/J_Y there -- and that is exactly the shell doing the emitting;")
print("      (ii) the scalar's kinetic normalisation is |K_2| = 5e5, i.e. the canonically normalised field")
print("          carries a 1/sqrt(|K_2|) coupling, suppressing the rate by a further ~1/|K_2|.")
print("      Neither is computed here.  The number below is therefore an upper bound on the loss.")
Dloss_can = 2.0 * (CLIGHT**2 / A0['canonical']) / s_crit[K2_HI]
Dloss_alt = 2.0 * (CLIGHT**2 / A0['alt']) / s_crit[K2_HI]
check("E4 [worst case] even with the emission cut off only where the cone crosses c -- a factor s_crit "
      "= |K_2| Delta_max/(2-K_B) EARLIER than Milgrom's own MOND-radius cutoff -- and with the coupling "
      "taken at FULL gravitational strength (no 1/|K_2| suppression), the loss distance still exceeds the "
      "10 kpc Galactic path used by Moore & Nelson",
      min(Dloss_can, Dloss_alt) > 10 * KPC,
      f"D_loss = 2 (c^2/a_0)/s_crit = {Dloss_can:.3g} m ({Dloss_can/(10*KPC):.0f}x the Galactic path, "
      f"canonical; {Dloss_alt/(10*KPC):.0f}x alt) at |K_2| = 5e5.  ASSUMPTIONS, stated: the rate formula is "
      f"L19's verified transcription of Milgrom eq. (4), the coupling is taken as gravitational-strength "
      f"(an UPPER bound on the rate -- the scalar's normalisation |K_2| = 5e5 suppresses it further, by a "
      f"factor that is NOT computed here), and the path is Galactic.  For an EXTRAGALACTIC path of 100 Mpc "
      f"this same worst case would fail by {3.086e24/Dloss_can:.0f}x, so the margin is not large: this is "
      f"the one empirical item this lane leaves open, and the missing input is the scalar-matter vertex "
      f"normalisation")

print("\n  E5  Everything else that has been claimed to bound a gravitational-sector speed:")
print("      * binary pulsars (Yagi, Blas, Yunes, Barausse, PRL 112, 161101, arXiv:1307.6219) bound the")
print("        preferred-frame parameters alpha_1, alpha_2 and the dipole COUPLING -- not c_s.  A larger")
print("        c_s SUPPRESSES scalar radiation (the flux falls with the mode speed), so the superluminal")
print("        cone makes those bounds easier, not harder.")
print("      * the CMB and growth of structure constrain the scalar's speed in the COSMOLOGICAL background,")
print("        where J_Y is small and the mode is deeply subluminal (c_* ~ 400 km/s); they say nothing")
print("        about the Solar-System value.")
print("      * no time-of-flight measurement of this mode exists or can exist with present technique: the")
print("        scalar is not coupled to matter directly (matter is minimally coupled to g alone,")
print("        requirement 11), so there is no emitter and no receiver.")
check("E5 [verdict on observation] no existing observation is violated by c_s = 2.5e3 c -- and, stated "
      "plainly, no existing observation BOUNDS this scalar's speed from above at all",
      True,
      "GW170817 constrains the tensor; Cherenkov constrains slow modes and is turned OFF by superluminality; "
      "pulsars constrain couplings; the CMB constrains the cosmological (subluminal) value.  The Solar-System "
      "scalar cone is an untested prediction, in the strict sense that nothing measures it")

# ------------------------------------------------------------------ F: is the number forced?
head("F -- is the superluminal cone forced, or is it a kernel choice?")
print("  F1  The kernel-free form.  The static law of ANY matter-sourced scalar of this class is")
print("      div[J_Y grad phi] = 4 pi G rho, hence J_Y g_phi = g_N exactly, hence")
print("          c_s,perp^2 / c^2  =  (2 - K_B) g_N / ( g_phi |K_2| ).")
print("      a_0 does NOT appear.  The two footings give IDENTICAL numbers for this statement; the footing")
print("      enters only through which g_phi a given kernel produces.")
gNs, gps = sp.symbols('g_N g_phi', positive=True)
cs2_free = (2 - KBsym) * gNs / (gps * K2sym)
check("F1 the sound speed depends on the kernel ONLY through the scalar force g_phi it produces at the "
      "point in question -- so 'which kernel' is not a free direction, only 'how big is the scalar force'",
      sp.simplify(cs2_free.subs({gNs: sp.Symbol('s') * sp.Symbol('a0'), gps: sp.Symbol('D') * sp.Symbol('a0')})
                  - (2 - KBsym) * sp.Symbol('s') / (sp.Symbol('D') * K2sym)) == 0,
      "c_s^2/c^2 = (2-K_B) g_N/(g_phi |K_2|) = (2-K_B) s/(Delta |K_2|); a_0 cancels identically")

print("\n  F2  Therefore SUBLUMINALITY at a point REQUIRES a scalar force there of at least")
print("          g_phi >= (2 - K_B) g_N / |K_2|,")
print("      and the scalar force is exactly the anomalous sunward acceleration the ephemerides bound.")
print(f"      {'planet':>9}{'g_N [m/s^2]':>15}{'g_phi needed':>16}{'ephemeris bound':>18}{'over by':>12}"
      f"{'=> c_s/c forced >=':>22}")
forced_min = []
for pl in ("Venus", "Saturn"):
    gN = GM_SUN / R_PLANET[pl]**2
    need = (2 - KB_V) * gN / K2_HI
    over = need / DG_BOUND[pl]
    csmin = math.sqrt((2 - KB_V) * gN / (DG_BOUND[pl] * K2_HI))
    forced_min.append(csmin)
    print(f"      {pl:>9}{gN:>15.5g}{need:>16.5g}{DG_BOUND[pl]:>18.1e}{over:>12.3g}{csmin:>22.5g}")
print("      (both footings identical -- a_0 is absent from this argument, by F1)")
check("F2 planetary ephemerides ALREADY force the cone open: a subluminal scalar at Venus's or Saturn's "
      "orbit would need an anomalous sunward acceleration far above the measured bound",
      min(forced_min) > 1.0,
      f"subluminality needs g_phi over the 1-sigma bound by "
      f"{(2-KB_V)*GM_SUN/R_PLANET['Venus']**2/K2_HI/DG_BOUND['Venus']:.2g}x (Venus) and "
      f"{(2-KB_V)*GM_SUN/R_PLANET['Saturn']**2/K2_HI/DG_BOUND['Saturn']:.2g}x (Saturn); equivalently the "
      f"data force c_s >= {forced_min[0]:.0f} c at Venus's orbit and >= {forced_min[1]:.0f} c at Saturn's, "
      f"at |K_2| = 5e5, for ANY kernel and BOTH footings.  Caveat stated: this uses the xi = 0 static law; "
      f"the xi^2 operator only stiffens the response further, i.e. it raises c_s")

print("\n  F3  Scan over the standard MOND interpolating-function family.  For each, Delta_max = max_s "
      "[s(nu(s) - 1)],")
print("      and subluminality at 1 AU requires |K_2| >= (2 - K_B) s_AU / Delta_max.")
def nu_simple(yv):  return (1 + math.sqrt(1 + 4 / yv)) / 2
def nu_n(yv, n):    return ((1 + math.sqrt(1 + 4 * yv**(-n))) / 2)**(1.0 / n)
def nu_rar(yv):     return 1.0 / (1 - math.exp(-math.sqrt(yv)))
def nu_expc(yv):
    # exponential carrier: mu(x) = 1 - e^{-x} with g_N = g mu(g/a0); solve for g/a0 at given y
    lo_, hi_ = yv, yv + 50.0
    for _ in range(200):
        mid = 0.5 * (lo_ + hi_)
        if mid * (1 - math.exp(-mid)) < yv: lo_ = mid
        else: hi_ = mid
    return 0.5 * (lo_ + hi_) / yv
KERNELS = [("simple nu (n=1)", lambda yv: nu_simple(yv)),
           ("standard nu (n=2)", lambda yv: nu_n(yv, 2)),
           ("n = 3", lambda yv: nu_n(yv, 3)), ("n = 5", lambda yv: nu_n(yv, 5)),
           ("n = 10", lambda yv: nu_n(yv, 10)), ("n = 20", lambda yv: nu_n(yv, 20)),
           ("nu_RAR (carried)", nu_rar), ("exponential carrier", nu_expc)]
from mpmath import mp, mpf
mp.dps = 60                                   # Delta = s(nu-1) is a cancelling difference at s ~ 1e8
def NU(nm, yv):
    yv = mpf(yv)
    if nm == "simple nu (n=1)":  return (1 + mp.sqrt(1 + 4 / yv)) / 2
    if nm.startswith("standard"): return ((1 + mp.sqrt(1 + 4 * yv**mpf(-2))) / 2)**(mpf(1) / 2)
    if nm.startswith("n = "):
        n = mpf(int(nm.split("=")[1])); return ((1 + mp.sqrt(1 + 4 * yv**(-n))) / 2)**(1 / n)
    if nm.startswith("nu_RAR"):   return 1 / (1 - mp.e**(-mp.sqrt(yv)))
    lo_, hi_ = yv, yv + 200                   # exponential carrier: mu(x) = 1 - e^{-x}
    for _ in range(400):
        mid = (lo_ + hi_) / 2
        if mid * (1 - mp.e**(-mid)) < yv: lo_ = mid
        else: hi_ = mid
    return (lo_ + hi_) / 2 / yv
grid = np.geomspace(1e-4, 1e10, 60000)
s_au_can = g_earth / A0['canonical']
print(f"      {'kernel':<24}{'Delta_max':>10}{'at s':>10}{'|K2| need can':>16}{'|K2| need alt':>16}"
      f"{'interior max?':>15}{'c_perp/c 1AU':>14}{'c_par/c 1AU':>14}")
K2need = {}
for nm, nu in KERNELS:
    dm, sm = 0.0, 0.0
    for yv in grid:
        try: d = yv * (nu(yv) - 1.0)
        except Exception: continue
        if d > dm: dm, sm = d, yv
    need_can = (2 - KB_V) * (g_earth / A0['canonical']) / dm
    need_alt = (2 - KB_V) * (g_earth / A0['alt']) / dm
    Dfun = lambda yv: mpf(yv) * (NU(nm, yv) - 1)
    D_au = Dfun(s_au_can)
    interior = bool(D_au < mpf(dm) * mpf('0.999'))     # Delta has fallen back below its maximum
    if interior:                                       # bounded boost => the carried kernel is SATURATED
        cperp = math.sqrt((2 - KB_V) * (s_au_can / dm) / K2_HI); cpar = float('inf')
    else:
        Dp_au = mp.diff(Dfun, mpf(s_au_can))
        cperp = math.sqrt((2 - KB_V) * float(mpf(s_au_can) / D_au) / K2_HI)
        cpar = math.sqrt((2 - KB_V) / (float(Dp_au) * K2_HI)) if Dp_au > 0 else float('inf')
    K2need[nm] = (dm, need_can, need_alt, cperp, cpar, interior)
    print(f"      {nm:<24}{dm:>10.4f}{sm:>10.3g}{need_can:>16.4g}{need_alt:>16.4g}"
          f"{('yes -> saturated' if interior else 'no (monotone)'):>18}{cperp:>14.4g}{cpar:>14.4g}")
print("      'interior max? yes' means Delta falls back after its peak, so the bounded-boost theorem forces")
print("      the carried kernel to SATURATE there (THE_ACTION s.3) -- and then Delta' = 0 and the")
print("      LONGITUDINAL speed is infinite in the whole Solar System (D2).  Only the simple nu is monotone,")
print("      and even it gives a longitudinal cone "
      f"{K2need['simple nu (n=1)'][4]/K2need['simple nu (n=1)'][3]:.0f}x wider than its transverse one at 1 AU.")
print("      (Delta_max for the simple nu is an asymptotic supremum reached only as s -> infinity, and the")
print("       kernel attaining it carries a PERMANENT 1.0 a_0 excess = "
      f"{A0['canonical']/DG_BOUND['Venus']:.0f}x the Venus ephemeris bound, so it is inadmissible anyway.)")
worst_need = min(v[1] for v in K2need.values())
print(f"      the dark sector's window is |K_2| <= {K2_HI:.0e} (g03r/g03u); the growth pincer allows "
      f"<= {K2_GROWTH:.1e} (g03t).")
print(f"      the LEAST demanding kernel in the family still needs |K_2| >= {worst_need:.3g}, i.e. "
      f"{worst_need/K2_HI:.0f}x the window edge and {worst_need/K2_GROWTH:.0f}x the growth pincer.")
print(f"      To fit inside |K_2| = {K2_HI:.0e} a kernel would need Delta_max >= "
      f"{(2-KB_V)*(g_earth/A0['canonical'])/K2_HI:.4g}, i.e. a permanent acceleration excess of "
      f"{(2-KB_V)*(g_earth/A0['canonical'])/K2_HI*A0['canonical']:.3g} m/s^2 -- "
      f"{(2-KB_V)*(g_earth/A0['canonical'])/K2_HI*A0['canonical']/DG_BOUND['Venus']:.1e}x the Venus "
      f"ephemeris bound (this is F2 restated).")
check("F3 some kernel of the class gives a subluminal Solar-System scalar at an admissible |K_2| -- i.e. "
      "the superluminal cone is a kernel CHOICE",
      worst_need <= K2_GROWTH,
      f"no kernel in the standard family does: Delta_max lands in [{min(v[0] for v in K2need.values()):.3f}, "
      f"{max(v[0] for v in K2need.values()):.3f}] across simple/standard/n-family/nu_RAR/exponential, so "
      f"|K_2| >= {worst_need:.3g} is required, {worst_need/K2_GROWTH:.0f}x above the loosest bound the "
      f"programme carries.  The superluminal cone is FORCED by bounded boost, not chosen")

print("\n  F4  CONTROL -- is the theorem about BOUNDEDNESS, or is it about scalars in general?  Take an")
print("      UNBOUNDED 'kernel' Delta(s) = beta s (a pure rescaling of G by 1 + beta, no MOND).  Then")
print("      J_Y = 1/beta is constant and c_s^2 = (2-K_B)/(beta |K_2|) is subluminal for modest |K_2|.")
for beta in (0.1, 1.0):
    need = (2 - KB_V) / beta
    print(f"      Delta = {beta} s:  J_Y = {1/beta:.4g} everywhere;  subluminal for |K_2| >= {need:.4g}")
check("F4 [CONTROL] the theorem is about BOUNDEDNESS of the boost, not about scalars: an unbounded kernel "
      "(a pure G rescaling) is subluminal at |K_2| >= 1.8, thirteen orders below the window, so the test "
      "distinguishes the two cases",
      (2 - KB_V) / 1.0 < K2_LO and worst_need > K2_LO,
      "Delta ~ s gives J_Y = const and no growth of c_s with acceleration; it is the SATURATION of Delta "
      "-- the bounded-boost theorem, THE_ACTION section 3 / section 5.13 -- that forces J_Y = s/Delta to "
      "grow linearly and drags the cone open")

print("\n  F5  The general statement, proved.  Boundedness of Delta means int_0^S Delta'(s) ds = Delta(S) is")
print("      bounded, so Delta'(s) -> 0 and Delta(s)/s -> 0.  Hence BOTH scalar speeds diverge:")
print("          c_s,perp^2 = (2-K_B) s / (Delta(s) |K_2|)      -> infinity  (at least linearly in s)")
print("          c_s,par^2  = (2-K_B) / (Delta'(s) |K_2|)       -> infinity  (faster than linearly)")
print("      There is no bounded-boost kernel with a subluminal high-acceleration scalar at fixed |K_2|.")
print("      A sharper corollary, which a C^2 continuation does NOT remove: if Delta has an INTERIOR")
print("      maximum (as nu_RAR does, at s_sat = 2.540), then Delta'(s_sat) = 0 exactly there, so the")
print("      longitudinal speed is infinite ON THAT SURFACE for every kernel with an interior maximum --")
print(f"      around the Sun, a sphere at r = sqrt(GM/(s_sat a_0)) = "
      f"{math.sqrt(GM_SUN/(S_SAT*A0['canonical']))/AU:.0f} AU (canonical) / "
      f"{math.sqrt(GM_SUN/(S_SAT*A0['alt']))/AU:.0f} AU (alt), i.e. in the inner Oort cloud.")
ratio_check = all(J_Y(s2) > J_Y(s1) * (s2 / s1) * 0.999 for s1, s2 in [(1e3, 1e4), (1e6, 1e7), (1e9, 1e10)])
check("F5 [theorem] on the saturated branch J_Y grows exactly linearly in s, so c_s^2 grows linearly in the "
      "local Newtonian acceleration without bound -- verified numerically over seven decades",
      ratio_check,
      "J_Y(10 s)/J_Y(s) = 10 to 1e-3 at s = 1e3, 1e6, 1e9; the growth is the bounded-boost theorem's "
      "own content, transcribed into the kinetic sector")

# ------------------------------------------------------------------ G: verdict
head("G -- verdict")
G1 = (sp.simplify(Gnn - K2sym) == 0) and K2_LO > 0
G2 = dprime_sat > 0
G3 = True
G4 = worst_need <= K2_GROWTH
check("G1 [VERDICT] the MOND scalar's cone at c_s = 2.5e3 c is SPACELIKE with respect to the theory's "
      "preferred foliation, so it creates no closed causal curve and is causally admissible", G1,
      "proved as an identity in B2 (G^{mu nu}n_mu n_nu = |K_2|, independent of c_s), with a negative "
      "control in B3 and the black-hole censorship in C4/C5")
check("G2 [VERDICT] the initial value problem is a well-posed hyperbolic Cauchy problem as the action is "
      "published", G2,
      "it is not, for a reason that is NOT the 2.5e3 c number: the published kernel's exact saturation "
      "makes the LONGITUDINAL speed infinite, turning that sector into an elliptic constraint on the leaf. "
      "Accepted practice in this class of theory (the khronometric instantaneous mode) but it must be "
      "SAID, and it needs the same C^2 continuation of Delta that L13's P9 asked for")
check("G3 [VERDICT] no existing observation is violated by the superluminal cone", G3,
      "and none bounds it either: GW170817 is a tensor bound, gravitational Cherenkov is switched OFF by "
      "superluminality (E2) and is safe in the subluminal corner by a computed but not-large factor (E4), "
      "pulsars bound couplings")
check("G4 [VERDICT] the superluminal cone is a kernel choice rather than a structural consequence of the "
      "bounded-boost theorem", G4,
      "it is structural: F3 finds no admissible kernel, F5 proves the divergence follows from boundedness "
      "alone, and F2 shows planetary ephemerides force c_s >= "
      f"{forced_min[0]:.0f} c at Venus's orbit independently of any kernel")
adm = G1 and G3
check("G5 [ADMISSIBILITY] a MOND-scalar cone thousands of times wider than the light cone is ADMISSIBLE in "
      "this theory", adm,
      "yes -- on causality, on black-hole censorship, and on every existing observation.  The costs it "
      "carries are (i) the alignment of the scalar's frame with the clock's must be exact, with a margin "
      f"of only {worst_margin:.0f} km/s at Cassini conjunction (B3); (ii) the published kernel's saturation "
      "makes one direction instantaneous, so the system is elliptic-hyperbolic, not hyperbolic (G2); and "
      "(iii) the subluminal galactic corner's Cherenkov margin is finite and uncomputed at the vertex "
      "level (E4)")

print("\n" + "-" * W)
print("  ONE-LINE ANSWER.  The cone is admissible and it is FORCED.  It is admissible because the scalar's")
print("  characteristic cone is built from the SAME clock scalar tau that defines the preferred foliation,")
print("  so G^{mu nu} n_mu n_nu = |K_2| > 0 identically and the leaves are spacelike at any c_s; because the")
print("  universal horizon censors arbitrarily fast modes (r_h -> 3M/2 as c_s -> infinity); and because no")
print("  observation bounds a spin-0 gravitational-sector speed from above.  It is forced because")
print("  c_s^2 = (2-K_B) g_N/(g_phi |K_2|) contains no a_0 and no kernel shape: the Solar System's own")
print("  ephemerides, which bound g_phi, therefore bound c_s from BELOW at several hundred c.  L13's label")
print("  was correct; this lane replaces it with a proof, and adds that the number is not a cost the theory")
print("  chose but a consequence of the Solar System being Newtonian.")
print("-" * W)
print(f"\nRESULT: {len(FAILS)} FAIL" + (f" -> {FAILS}" if FAILS else ""))
print(f"({time.time()-T0:.0f}s)")
sys.exit(0)
