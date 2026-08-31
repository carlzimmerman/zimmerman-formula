#!/usr/bin/env python3
"""
LEG C - FRAME/CONGRUENCE FUNCTIONALS: close-or-break calculation.

Trichotomy question (Layer C frontier): can a scalar functional q[g] built from
a designated congruence/foliation (apparent horizon R_A = c/H, expansion theta
of a flow, CMB frame) deliver an evolving a0(z) ~ H(z) INSIDE a bound system,
with (i) no new propagating DOF, (ii) no independent Cauchy data, (iii) no
conserved dark charge?

Everything load-bearing below is COMPUTED (sympy), not scaled. Parts:

  C1. H IS FOLIATION DATA, NOT A SPACETIME SCALAR. Exact de Sitter in two
      charts covering the same events: the flat-slicing comoving congruence
      has theta = 3H; the static-chart Killing congruence through the SAME
      event has theta = 0. Both metrics verified Einstein: G_ab + Lambda g_ab
      = 0 with Lambda = 3H^2. So "H" = theta/3 of a CHOSen congruence; the
      metric alone assigns no H to an event.

  C2. EVEN WITHIN ONE SLICING, BOOST CHANGES H: a tilted (radially boosted,
      constant v) congruence in flat FLRW has theta = 3*gamma*H, not 3H.
      Measured expansion is (event, congruence)-dependent, period.

  C3. BOUND VACUUM REGION: THE CONGRUENCE IS FREE DATA CARRYING ARBITRARY H.
      Schwarzschild-de Sitter (verified R_ab = Lambda g_ab, R = 4*Lambda,
      Weyl type D with only Psi2 = -m/r^3). The type-D principal structure
      fixes only the (t,r) TIMELIKE PLANE; the residual boost chi(r) is one
      free function. Computed: theta[chi] = (1/r^2) d/dr(r^2 sqrt(f) sinh chi)
      -- chi = 0 (Killing) gives theta = 0; and for ANY externally chosen
      H0 the choice sinh chi = (H0 r^3 + C)/(r^2 sqrt(f)) gives theta = 3*H0
      EXACTLY (verified). The vacuum metric supports congruences with EVERY
      expansion; H0 enters as INPUT (the boost profile = velocity Cauchy
      data), never as output. "The frame that knows H must be told H."

  C4. NO CANONICAL DATA-FREE CONGRUENCE FROM THE METRIC:
      (a) Weyl principal directions: type D fixes a plane not a vector (C3's
          boost function remains free); on conformally flat FLRW C_abcd = 0
          (verified for flat dS) so the construction is DEGENERATE exactly on
          the cosmology it is supposed to read.
      (b) Gradient-of-invariant flows: in SdS every algebraic invariant is a
          function of r alone; computed |grad K|^2 = f(r) K'(r)^2 > 0 in the
          static region => SPACELIKE => not a congruence 4-velocity at all.
          In exact dS the gradients vanish identically (degenerate). Where
          such a flow IS timelike it is a LOCAL curvature functional, so its
          theta is a local invariant and the construction collapses to Leg A
          (t-independent in the stationary bound region; legA script).

  C5. MAKING THE FOLIATION DYNAMICAL = THE DARK STATE, WITH A CONSERVED
      CHARGE. u_mu = -d_mu T/sqrt(X) (khronon). Minisuperspace L = a^3 P(X):
      the T Euler-Lagrange equation is verified to be EXACTLY
      d/dt[a^3 P'(X) Tdot] = 0 => conserved shift charge Q = a^3 P_X Tdot.
      This is the SAME conserved-advected-charge obstruction as the nbody/DW
      results. T needs an initial slice + velocity => Cauchy data (violates
      ii); Q is the dark charge (violates iii); the propagating khronon mode
      is the new DOF (violates i) -- and this territory is already KILLED
      for MOND (FC-KH: c^2_par < 0 on a0 < a < 38 a0, committed).

  C6 (stated identity, standard, NOT sympy here): if instead u is a FIXED
      background structure (non-dynamical foliation), diffeo invariance is
      broken and the Noether identity reads
        2 grad_a E^{ab} = -(delta S/delta u_a) grad^b u^a + grad_a[(dS/du_a) u^b]-type source != 0
      unless delta S/delta u = 0 is IMPOSED -- i.e. unless u is given
      dynamics, returning to C5. So: fixed frame => conservation trade;
      dynamical frame => Cauchy data + charge + DOF.

PARTITION ARGUMENT (closes the leg): a congruence functional u[g] is either
  POINTWISE-LOCAL (u from g and finitely many derivatives at the point) =>
    theta_u is a local curvature invariant => Leg A collapse (and the named
    candidates each fail concretely per C3/C4); or
  NONLOCAL => u must be transported/selected globally: initial-slice transport
    = Cauchy data (khronon, C5; killed), global elliptic selection (CMC/York
    slicing: elliptic => instantaneous response = Leg B's alpha_3/pulsar
    exposure; in-house York/CMC audit already FAILED gates E and F), physical
    -fluid frame (CMB/matter: fails in vacuum, environment-dependent, PPN
    preferred-frame exposure, and IS a dark-medium coupling = McVittie
    mechanism = Leg A's forced-medium result), or teleological (Leg B).
No fifth option: pointwise vs non-pointwise is exhaustive.

Units: geometric c = G = 1 in symbolic parts.
"""

import sympy as sp

LINE = "=" * 78


# ----------------------------------------------------------------------------
# curvature helpers (general symmetric metric)
# ----------------------------------------------------------------------------
def christoffel(gmat, coords):
    n = len(coords)
    ginv = gmat.inv()
    Gam = [[[sp.S(0)] * n for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for b in range(n):
            for c in range(n):
                s = sp.S(0)
                for d in range(n):
                    if ginv[a, d] == 0:
                        continue
                    s += ginv[a, d] * (sp.diff(gmat[d, b], coords[c])
                                       + sp.diff(gmat[d, c], coords[b])
                                       - sp.diff(gmat[b, c], coords[d]))
                Gam[a][b][c] = sp.together(sp.cancel(s / 2))
    return Gam


def riemann_up(gmat, coords, Gam=None):
    n = len(coords)
    if Gam is None:
        Gam = christoffel(gmat, coords)
    Riem = [[[[sp.S(0)] * n for _ in range(n)] for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for b in range(n):
            for c in range(n):
                for d in range(n):
                    e = sp.diff(Gam[a][b][d], coords[c]) - sp.diff(Gam[a][b][c], coords[d])
                    for f in range(n):
                        e += Gam[a][c][f] * Gam[f][b][d] - Gam[a][d][f] * Gam[f][b][c]
                    Riem[a][b][c][d] = sp.together(sp.cancel(e))
    return Riem, Gam


def ricci(gmat, coords):
    n = len(coords)
    Riem, Gam = riemann_up(gmat, coords)
    Ric = sp.zeros(n, n)
    for b in range(n):
        for d in range(n):
            Ric[b, d] = sp.simplify(sum(Riem[a][b][a][d] for a in range(n)))
    return Ric, Riem, Gam


def einstein(gmat, coords):
    n = len(coords)
    Ric, Riem, Gam = ricci(gmat, coords)
    ginv = gmat.inv()
    Rs = sp.simplify(sum(ginv[i, j] * Ric[i, j] for i in range(n) for j in range(n)))
    G = sp.simplify(Ric - Rs / 2 * gmat)
    return G, Ric, Rs, Riem, Gam


def divergence(gmat, coords, u_up):
    """theta = nabla_mu u^mu = (1/sqrt(-g)) d_mu( sqrt(-g) u^mu )."""
    sg = sp.sqrt(-gmat.det())
    return sp.simplify(sum(sp.diff(sg * u_up[i], coords[i]) for i in range(len(coords))) / sg)


def report(tag, ok, detail=""):
    print(("[PASS] " if ok else "[FAIL] ") + tag + ("  :: " + str(detail) if detail != "" else ""))
    return ok


all_ok = True

t, r, th, ph, x, y, z = sp.symbols("t r theta phi x y z", real=True)
H, H0, m, Lam, C, v = sp.symbols("H H0 m Lambda C v", positive=True)

# ============================================================================
print(LINE)
print("C1. de Sitter: SAME spacetime, two congruences, two different 'H'")
print(LINE)
# flat slicing
g_flat = sp.diag(-1, sp.exp(2 * H * t), sp.exp(2 * H * t), sp.exp(2 * H * t))
coords_flat = [t, x, y, z]
G1, _, _, _, _ = einstein(g_flat, coords_flat)
ein1 = sp.simplify(G1 + 3 * H**2 * g_flat)
all_ok &= report("flat-slicing dS solves G_ab + Lambda g_ab = 0 (Lambda=3H^2)",
                 ein1 == sp.zeros(4, 4))
u_com = [sp.S(1), 0, 0, 0]
theta_flat = divergence(g_flat, coords_flat, u_com)
all_ok &= report("comoving congruence: theta = 3H", sp.simplify(theta_flat - 3 * H) == 0,
                 theta_flat)

# static chart of the SAME de Sitter spacetime
f_ds = 1 - H**2 * r**2
g_stat = sp.diag(-f_ds, 1 / f_ds, r**2, r**2 * sp.sin(th)**2)
coords_stat = [t, r, th, ph]
G2, _, _, _, _ = einstein(g_stat, coords_stat)
ein2 = sp.simplify(G2 + 3 * H**2 * g_stat)
all_ok &= report("static-chart dS solves G_ab + Lambda g_ab = 0 (same Lambda)",
                 ein2 == sp.zeros(4, 4))
u_kill = [1 / sp.sqrt(f_ds), 0, 0, 0]
norm_kill = sp.simplify(sum(g_stat[i, i] * u_kill[i]**2 for i in range(4)))
theta_stat = divergence(g_stat, coords_stat, u_kill)
all_ok &= report("Killing congruence unit-timelike (u.u = -1)", norm_kill == -1)
all_ok &= report("Killing congruence through the SAME events: theta = 0",
                 sp.simplify(theta_stat) == 0)
print("  => 'H' = theta/3 is a property of (event, CONGRUENCE), not of the metric.")
print("     The apparent horizon R_A = 1/H inherits this foliation dependence.")

# ============================================================================
print()
print(LINE)
print("C2. Tilted congruence in flat FLRW: theta = 3*gamma*H (boost changes H)")
print(LINE)
a = sp.Function("a", positive=True)(t)
g_frw = sp.diag(-1, a**2, a**2, a**2)
gam = 1 / sp.sqrt(1 - v**2)
u_tilt = [gam, gam * v / a, 0, 0]
norm_tilt = sp.simplify(-gam**2 + a**2 * (gam * v / a)**2)
theta_tilt = divergence(g_frw, coords_flat, u_tilt)
Hdot_a = sp.diff(a, t) / a
all_ok &= report("tilted u unit-timelike", sp.simplify(norm_tilt + 1) == 0)
all_ok &= report("theta_tilted = 3*gamma*(adot/a), gamma = (1-v^2)^(-1/2)",
                 sp.simplify(theta_tilt - 3 * gam * Hdot_a) == 0, sp.simplify(theta_tilt))

# ============================================================================
print()
print(LINE)
print("C3. Schwarzschild-de Sitter: the congruence is FREE DATA carrying ANY H0")
print(LINE)
f_sds = 1 - 2 * m / r - Lam * r**2 / 3
g_sds = sp.diag(-f_sds, 1 / f_sds, r**2, r**2 * sp.sin(th)**2)
G3, Ric3, Rs3, Riem3, Gam3 = einstein(g_sds, coords_stat)
all_ok &= report("SdS is Einstein: R_ab = Lambda g_ab",
                 sp.simplify(Ric3 - Lam * g_sds) == sp.zeros(4, 4))
all_ok &= report("R = 4*Lambda exactly (no H(t) anywhere in local curvature)",
                 sp.simplify(Rs3 - 4 * Lam) == 0)

# residual boost in the type-D principal (t,r) plane: one free function chi(r)
chi = sp.Function("chi", real=True)(r)
u_boost = [sp.cosh(chi) / sp.sqrt(f_sds), sp.sqrt(f_sds) * sp.sinh(chi), 0, 0]
norm_boost = sp.simplify(g_sds[0, 0] * u_boost[0]**2 + g_sds[1, 1] * u_boost[1]**2)
all_ok &= report("boosted principal-plane u unit-timelike for EVERY chi(r)",
                 sp.simplify(norm_boost + 1) == 0)
theta_boost = divergence(g_sds, coords_stat, u_boost)
target = sp.simplify(sp.diff(r**2 * sp.sqrt(f_sds) * sp.sinh(chi), r) / r**2)
all_ok &= report("theta[chi] = (1/r^2) d/dr( r^2 sqrt(f) sinh(chi) )",
                 sp.simplify(theta_boost - target) == 0)
all_ok &= report("chi = 0 (Killing representative): theta = 0",
                 sp.simplify(theta_boost.subs(chi, 0)) == 0)

# dial the free function to ANY externally supplied H0:
chi_H0 = sp.asinh((H0 * r**3 + C) / (r**2 * sp.sqrt(f_sds)))
theta_H0 = sp.simplify(theta_boost.subs(chi, chi_H0).doit())
all_ok &= report("sinh(chi) = (H0 r^3 + C)/(r^2 sqrt(f))  =>  theta = 3*H0 EXACTLY",
                 sp.simplify(theta_H0 - 3 * H0) == 0, theta_H0)
print("  => In the SAME bound vacuum region there exist unit timelike congruences")
print("     with theta = 3*H0 for EVERY H0 (and C: Lemaitre-type family). H0 is")
print("     INPUT smuggled through the boost profile (= velocity Cauchy data on a")
print("     slice), not OUTPUT of the geometry. The frame that knows H was told H.")

# ============================================================================
print()
print(LINE)
print("C4. No canonical data-free congruence from the metric")
print(LINE)
# (a) Weyl degeneracy on the cosmology itself: C_abcd = 0 on conformally flat dS
n = 4
ginv_flat = g_flat.inv()
Ric1, Riem1, _ = ricci(g_flat, coords_flat)
Rs1 = sp.simplify(sum(ginv_flat[i, j] * Ric1[i, j] for i in range(n) for j in range(n)))
# lower first index of Riemann, then Weyl
Rdown = [[[[sp.S(0)] * n for _ in range(n)] for _ in range(n)] for _ in range(n)]
for a_ in range(n):
    for b_ in range(n):
        for c_ in range(n):
            for d_ in range(n):
                Rdown[a_][b_][c_][d_] = sp.simplify(
                    sum(g_flat[a_, e_] * Riem1[e_][b_][c_][d_] for e_ in range(n)))
weyl_zero = True
for a_ in range(n):
    for b_ in range(n):
        for c_ in range(n):
            for d_ in range(n):
                Cw = (Rdown[a_][b_][c_][d_]
                      - (g_flat[a_, c_] * Ric1[d_, b_] - g_flat[a_, d_] * Ric1[c_, b_]
                         + g_flat[b_, d_] * Ric1[c_, a_] - g_flat[b_, c_] * Ric1[d_, a_]) / 2
                      + Rs1 * (g_flat[a_, c_] * g_flat[d_, b_]
                               - g_flat[a_, d_] * g_flat[c_, b_]) / 6)
                if sp.simplify(Cw) != 0:
                    weyl_zero = False
all_ok &= report("Weyl tensor of (conformally flat) dS vanishes identically "
                 "=> principal-null-direction frame UNDEFINED on the cosmology",
                 weyl_zero)
print("  (and where Weyl != 0, SdS type D fixes only the (t,r) PLANE: C3 showed the")
print("   in-plane boost chi(r) stays free = exactly the H-carrying function.)")

# (b) gradient-of-invariant flows are spacelike in the bound static region
# Kretschmann K = R_abcd R^abcd; for a DIAGONAL metric,
#   K = sum g_aa g^bb g^cc g^dd (R^a_bcd)^2
ginv_sds = g_sds.inv()
Kterm = sp.S(0)
for a_ in range(n):
    for b_ in range(n):
        for c_ in range(n):
            for d_ in range(n):
                Rab = Riem3[a_][b_][c_][d_]
                if Rab == 0:
                    continue
                Kterm += (g_sds[a_, a_] * ginv_sds[b_, b_] * ginv_sds[c_, c_]
                          * ginv_sds[d_, d_] * Rab
                          * Riem3[a_][b_][c_][d_])
K_sds = sp.simplify(Kterm)
K_expected = 48 * m**2 / r**6 + sp.Rational(8, 3) * Lam**2
all_ok &= report("Kretschmann(SdS) = 48 m^2/r^6 + 8 Lambda^2/3 (function of r only)",
                 sp.simplify(K_sds - K_expected) == 0, K_sds)
gradK_norm = sp.simplify(ginv_sds[1, 1] * sp.diff(K_sds, r)**2)
all_ok &= report("|grad K|^2 = f(r) K'(r)^2 > 0 in static region => SPACELIKE, "
                 "cannot serve as a congruence 4-velocity",
                 sp.simplify(gradK_norm - f_sds * sp.diff(K_sds, r)**2) == 0,
                 gradK_norm)
gradK_dS = sp.simplify(sp.diff(K_sds.subs(m, 0), r))
all_ok &= report("pure-dS limit: grad(K) = 0 identically => gradient flow DEGENERATE "
                 "exactly on the cosmology", gradK_dS == 0)
print("  => gradient-of-local-invariant congruences: spacelike where the bound mass")
print("     dominates, vanishing on the (exact-dS) cosmology, and by construction")
print("     LOCAL => theta is a local invariant => collapses to Leg A regardless.")

# ============================================================================
print()
print(LINE)
print("C5. Dynamical foliation (khronon) = Cauchy data + conserved dark charge")
print(LINE)
T = sp.Function("T", real=True)(t)
P = sp.Function("P")
X = sp.diff(T, t)**2                      # X = -g^{mn} d_m T d_n T on FLRW
Lmini = a**3 * P(X)
EL_T = sp.simplify(sp.diff(Lmini, T) - sp.diff(sp.diff(Lmini, sp.diff(T, t)), t))
# charge Q = a^3 * P'(X) * Tdot = (1/2) dL/dTdot ; verify EL_T == -2 dQ/dt
Qcharge = sp.simplify(sp.diff(Lmini, sp.diff(T, t)) / 2)
dQdt = sp.simplify(sp.diff(Qcharge, t))
all_ok &= report("khronon EL equation is EXACTLY d/dt[a^3 P'(X) Tdot] = 0 "
                 "(EL_T + 2 dQ/dt == 0)", sp.simplify(EL_T + 2 * dQdt) == 0)
print("  conserved shift charge Q = a^3 P'(X) Tdot   [Noether of T -> T + const]")
print("  => (ii) VIOLATED: T needs an initial slice + Tdot = Cauchy data;")
print("     (iii) VIOLATED: Q is a conserved advected dark charge (the SAME")
print("     obstruction as the nbody/DW shift-charge results);")
print("     (i) VIOLATED: the varied khronon propagates (khronometric scalar) --")
print("     and that territory is KILLED for MOND (FC-KH: c^2_par < 0 on the")
print("     galaxy band a0 < a < 38 a0, committed 2026-08-31).")
# alignment remark, computed: with T = t the khronon frame is comoving, theta = 3H
u_khronon = [sp.S(1), 0, 0, 0]
theta_kh = divergence(g_frw, coords_flat, u_khronon)
all_ok &= report("T = t (data ALIGNED with cosmic slicing) => theta = 3 adot/a",
                 sp.simplify(theta_kh - 3 * Hdot_a) == 0)
print("  => the khronon reproduces cosmic H only when its Cauchy data are chosen")
print("     aligned with the FLRW slicing: H enters through the data, again.")

# ============================================================================
print()
print(LINE)
print("C6 (stated, standard -- NOT a sympy result here): FIXED background frame")
print(LINE)
print("""  If u is fixed (not varied), diffeo invariance of S[g; u] fails and the
  Noether identity gives  2 grad_a E^{ab} = source[delta S/delta u] != 0:
  matter/metric conservation is violated unless delta S/delta u = 0 is imposed
  as an equation of motion -- which is precisely making u dynamical => C5.
  (Standard Einstein-aether/khronometric result; the in-house York/CMC route
  is the concrete global-slicing attempt: CMC selection is a global ELLIPTIC
  problem = instantaneous response = Leg B's alpha_3/pulsar exposure, and the
  committed A-H audit already failed it on gates E (G_eff = 2G) and F
  (Cassini). Matter/CMB frames: fail in vacuum, environment-dependent
  [SPARC-fork null], preferred-frame PPN, and = coupling to a physical medium
  = the McVittie forced-medium mechanism of the Leg A script.)""")

print()
print(LINE)
print("ALL SYMPY CHECKS PASSED" if all_ok else "SOME CHECKS FAILED")
print(LINE)
print("""VERDICT: LEG C CLOSES (no escape found).
  Partition: u[g] pointwise-local  => theta_u is a local curvature invariant
             => Leg A collapse (constant a0 in stationary bound regions; the
             named candidates fail concretely: type-D fixes a plane not a
             vector [C3], Weyl degenerate on FLRW [C4a], invariant-gradient
             flows spacelike/degenerate [C4b]).
             u[g] nonlocal => transported (Cauchy data: khronon, C5 -- new DOF
             + charge + killed by FC-KH), globally selected (CMC/York:
             elliptic/instantaneous => Leg B trade; audit-failed), physical
             fluid (vacuum-fail + environment + PPN + dark medium), or
             teleological (Leg B).
  Consequence: an evolving a0(z) ~ H(z) inside bound systems cannot come from
  a frame/congruence functional without smuggling the frame as Cauchy data or
  a physical medium => within Leg C, a dynamical dark sector (or a causality/
  conservation trade) is REQUIRED. Layer A (constant a0 = c^2 sqrt(Lambda/32pi))
  is untouched: the Killing/static frame with theta = 0 reads Lambda only.""")
