#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
A59 -- IS THE THEORY ACTUALLY EXCLUDED BY alpha_1?
==================================================

The question.  A36 (verified, 13/13) computes the galactic-regime preferred-frame
coefficient

        alpha_1(k,g) = 4 u' / (D - u'),   u' = a0^2/(g+a0)^2,
        D = 1 + (k L*)^2 u'/2,

and finds alpha_1 = 0.046 ... 5.19 for r = 1 ... 30 kpc.  It then compares that
number with the PPN bound |alpha_1| < 1e-4 (LLR) and declares the theory EXCLUDED
by 2.66 ... 4.72 decades.

The objection this lane tests: alpha_1 is a COEFFICIENT.  Its physical effect on
any observable is alpha_1 x (v/c)^2, where v is a velocity relative to the
preferred frame (systemic, w, or internal, v_orb).  The 1e-4 bound is measured in
environments where the local acceleration is enormous (Earth-Moon: g ~ 3e7 a0;
binary pulsars: g ~ 1e11 a0), and in exactly those environments the theory's own
formula gives alpha_1 ~ 1e-14 ... 1e-24.  So the bound may be satisfied precisely
where it is measured, while the galactic value is O(1).

What this script proves.

  PART 0 (K1-K2): A36's numbers are reproduced exactly (they are the input, and
      they are correct -- the disagreement is about scope, not arithmetic).

  PART 1 (K3-K9): the observable signature of alpha_1.
      K3  the k -> 0, k -> infinity and u' -> 0 limits of A36's formula.
      K4  where alpha_1 = 1 and where alpha_1 = 1e-4 (in g/a0).
      K5  the alpha_1(g) ladder: monotone, 44 decades wide.
      K6  the crossover LOCUS alpha_1 = 1e-4: g* = 199 a0 for any source larger
          than ~1 pc (96 a0 at 20 kAU), and unreachable below 17.5 kAU, where the
          maximum is 8(r_s/L*)^2.
      K7  BILINEARITY.  The PPN alpha_1 Lagrangian (Shao & Wex 2012, eq. 7) is
          L_a1 = -alpha_1 (G m1 m2 / r) (v1.v2)/(2c^2) with v1, v2 ABSOLUTE
          velocities.  Expanding v1.v2 in the barycentric velocity V and the
          relative velocity u gives exactly three pieces -- V^2, V.u, u^2 --
          and NO velocity-independent piece.  Therefore every alpha_1 observable
          is alpha_1 x (velocity/c)^2, with velocity in {V, u}.  This is the
          structural fact the whole lane rests on.
      K8  the preferred-frame acceleration: Euler-Lagrange of that Lagrangian
          gives a = (alpha_1/2)(GM/c^2)[V rdot - (V^2 + V.u) rhat]/r^2 exactly
          (symbolic residual 0): a uniform (V/c)^2 rescaling of g (absorbable
          into G) plus a velocity-dependent (V.v/c^2) piece (not absorbable).
      K9  the rotation-curve decomposition: |w+v|^2 -> monopole (degenerate with
          M/L), dipole (m=1, aligned with the CMB dipole), and v^2 (a radial
          shape correction).  The monopole piece is exactly degenerate with the
          mass: a G-rescaling is a mass-rescaling.

  PART 2 (K10-K15): the environment table -- six systems with real bounds, plus
      the two "no-test" environments the task names.
      For each: g/a0, u', alpha_1(theory), the alpha_1-induced amplitude of the
      observable, the published precision, the implied bound on alpha_1, and the
      margin in decades.

  PART 3 (K16-K20): the decision.
      K16 the scan: is there ANY environment with alpha_1 >= 0.1 AND a test
          sensitive to the alpha_1 signature?  (count must be 0)
      K17 the published bounds are themselves alpha_1 x (v/c)^2 measurements:
          LLR's 9e-5 maps to 5.3 cm at lunar distance (2 cm ranging); the
          pulsar 3.5e-5 maps to its quoted xdot precision.  Both within a
          factor 3 -- so the bounds are bounds on the COEFFICIENT, measured at
          (v/c)^2 of their own environment.
      K18 A36 erratum: its K11 uses factor 2 while its headline formula is
          factor 4 (5.44e-14 vs 1.09e-13).  Not load-bearing.
      K19 A36's own section 8 already states the (v/c)^2 suppression; check it.
      K20 the verdict logic: coefficient O(1) in galaxies (true) AND bound
          satisfied wherever measured (true) AND no O(1) environment with a
          test (true) => "EXCLUDED" is false; "alpha_1 = 0 claim refuted" is true.

Conventions: c = 2.99792458e8 m/s, G = 6.67430e-11, a0 = 9.36e-11 m/s^2
(canonical footing), L* = 24 pc, lambda = L*/sqrt2, K = 4 pi G (round-2 action,
as in A22/A36).  K = 8 pi G in BRIEF sec.1 is a bookkeeping difference that
cancels in every formula used here (all of them are ratios); A36's numbers are
reproduced bit-for-bit, which fixes the convention.

Exit 0 iff every declared check passes.  --mutate freeze  : alpha_1 is frozen at
its 8 kpc value in every environment (A36's implicit assumption).
--mutate nolstar : the (k L*)^2 u'/2 term in D is dropped.
"""

import sys
import json
import math

import sympy as sp

LANE = "A59_alpha1_observable"
MUTATE = "freeze" if "--mutate" in sys.argv and "freeze" in sys.argv else (
    "nolstar" if "--mutate" in sys.argv and "nolstar" in sys.argv else None)

FAIL = []
NCHK = [0]
ROWS = []


def check(cond, cid, value, threshold, note=""):
    NCHK[0] += 1
    ok = bool(cond)
    print(f"{cid} {'PASS' if ok else 'FAIL'}  value={value}  threshold={threshold}"
          + (f"   [{note}]" if note else ""))
    if not ok:
        FAIL.append(cid)
    ROWS.append({"id": cid, "pass": ok, "value": str(value),
                 "threshold": str(threshold), "note": note})
    return ok


def info(msg):
    print(f"    .  {msg}")


# ----------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------
CLIGHT = 2.99792458e8
G_N = 6.67430e-11
MSUN = 1.98892e30
AU = 1.495978707e11
PC = 3.0856775814913673e16
KPC = 1.0e3 * PC
MPC = 1.0e6 * PC
A0 = 9.36e-11
LSTAR = 24.0 * PC
LAM = LSTAR / math.sqrt(2.0)
W_CMB = 369.82e3                     # Planck dipole, m/s
WC2 = (W_CMB / CLIGHT) ** 2
ALPHA1_BOUND = 1.0e-4                # task's PPN bound (LLR class)
LLR_ALPHA1_1SIG = 9.0e-5             # Müller et al. 2005: (-7 +- 9)e-5  [DOOR11]
PULSAR_ALPHA1 = 3.5e-5               # Shao & Wex 2012 95%: -3.5e-5 .. +3.3e-5
PULSAR_ALPHA1_LIU = 2.1e-5           # Liu et al. 2020, PSR J1909-3744

print("=" * 78)
print("A59 -- is the theory actually excluded by alpha_1?")
print("=" * 78)
print(f"a0 = {A0:.3e} m/s^2   L* = {LSTAR/PC:.1f} pc   lambda = {LAM/PC:.3f} pc")
print(f"w_CMB = {W_CMB/1e3:.1f} km/s  ->  (w/c)^2 = {WC2:.4e}")
print(f"declared PPN bound |alpha_1| < {ALPHA1_BOUND:.1e}; LLR 1-sigma {LLR_ALPHA1_1SIG:.1e};"
      f" pulsar 95% {PULSAR_ALPHA1:.1e}")
if MUTATE == "freeze":
    print("*** MUTATION freeze: alpha_1 is FROZEN at its 8 kpc value in every environment ***")
if MUTATE == "nolstar":
    print("*** MUTATION nolstar: the (k L*)^2 u'/2 term in D is DROPPED ***")
print()

# ============================================================================
# PART 0 -- A36 as input
# ============================================================================
print("-" * 78)
print("PART 0 -- A36's numbers (input; must reproduce exactly)")
print("-" * 78)


def gN_of_r(r, Mbar=6.0e10, a_h=3.0 * KPC):
    m_encl = Mbar * MSUN * r ** 2 / (r + a_h) ** 2
    return G_N * m_encl / r ** 2


def g_of_gN(gN):
    return 0.5 * gN * (1.0 + math.sqrt(1.0 + 4.0 * A0 / gN))


def uprime(g):
    return A0 ** 2 / (g + A0) ** 2


def alpha1(g, r, factor=4.0, drop_D=False):
    """A36 eq. (2.5): alpha_1 = factor * u'/(D - u'), D = 1 + (kL*)^2 u'/2, k = 1/r."""
    up = uprime(g)
    D = 1.0 if drop_D else 1.0 + (LSTAR / r) ** 2 * up / 2.0
    return factor * up / (D - up), up, D


A36_R = [1.0, 2.0, 3.0, 5.0, 8.0, 12.0, 20.0, 30.0]
A36_A = [0.073, 0.143, 0.235, 0.475, 0.928, 1.628, 3.169, 5.194]
A36_B = [0.537, 0.742, 0.942, 1.303, 1.736, 2.151, 2.659, 3.007]
A36_C = [0.046, 0.068, 0.091, 0.142, 0.219, 0.316, 0.477, 0.629]

tab36 = []
for r_kpc in A36_R:
    r = r_kpc * KPC
    gN = gN_of_r(r)
    g = g_of_gN(gN)
    a1, up, D = alpha1(g, r)
    fph = (g - gN) / g
    tab36.append(dict(r_kpc=r_kpc, g=g, gN=gN, up=up, D=D, a1=a1,
                      a1b=4.0 * fph, fph=fph))

rel_a = max(abs(t["a1"] - a) / a for t, a in zip(tab36, A36_A))
rel_b = max(abs(t["a1b"] - b) / b for t, b in zip(tab36, A36_B))
check(rel_a < 1e-2 and rel_b < 1e-2, "K1",
      f"max rel diff route(a) = {rel_a:.2e}, route(b) = {rel_b:.2e}", "< 1e-2 both",
      "A36's galactic alpha_1 tables reproduced from its own formula (A36 quotes 3 dp, "
      "so 1e-2 is the rounding floor)")


def alpha1_route_c(r_target, n=4000):
    num = den = 0.0
    prev = 0.0
    for i in range(1, n + 1):
        rb = i * r_target / n
        ra = prev
        ga = g_of_gN(gN_of_r(ra)) if ra > 0 else g_of_gN(gN_of_r(rb))
        gb = g_of_gN(gN_of_r(rb))
        ua, ub = uprime(ga), uprime(gb)
        num += 0.5 * (ga * ua + gb * ub) * (rb - ra)
        den += 0.5 * (ga + gb) * (rb - ra)
        prev = rb
    return 4.0 * num / den


rel_c = max(abs(alpha1_route_c(t["r_kpc"] * KPC) - c) / c for t, c in zip(tab36, A36_C))
check(rel_c < 3e-2, "K2", f"max rel diff route(c) = {rel_c:.2e}", "< 3e-2",
      "A36's independent 'galaxy as its own source' route reproduced (0.5% quadrature)")

a1_1kpc = tab36[0]["a1"]
a1_8kpc = tab36[4]["a1"]
a1_30kpc = tab36[7]["a1"]
info(f"alpha_1 ladder from A36: {a1_1kpc:.3f} (1 kpc) ... {a1_8kpc:.3f} (8 kpc) ... "
     f"{a1_30kpc:.3f} (30 kpc)")

# ============================================================================
# PART 1 -- the observable signature of alpha_1
# ============================================================================
print()
print("-" * 78)
print("PART 1 -- what alpha_1 DOES: the signature algebra")
print("-" * 78)

# --- K3: limits of A36's formula --------------------------------------------
up, Ls, k2 = sp.symbols("up Ls k2", positive=True)
D = 1 + k2 * Ls ** 2 * up / 2
a1_sym = 4 * up / (D - up)
lim_k0 = sp.simplify(sp.limit(a1_sym, k2, 0))
lim_kinf = sp.simplify(sp.limit(a1_sym, k2, sp.oo))
lim_up0 = sp.simplify(sp.limit(a1_sym, up, 0))
# the k -> infinity asymptote is 8/(kL*)^2 (u' cancels)
asym = sp.simplify(sp.series(a1_sym, k2, sp.oo, 2).removeO())
info(f"k->0: {lim_k0}   k->inf: {lim_kinf}   u'->0: {lim_up0}   asymptote: {asym}")
check(sp.simplify(lim_k0 - 4 * up / (1 - up)) == 0 and lim_kinf == 0 and lim_up0 == 0
      and sp.simplify(asym - 8 / (k2 * Ls ** 2)) == 0,
      "K3", f"{sp.simplify(lim_k0)}, {lim_kinf}, {lim_up0}, {asym}", "4u'/(1-u'), 0, 0, 8/(kL*)^2",
      "alpha_1 is screened BOTH by high acceleration (u'->0) and by a source small "
      "compared with L* (kL*>>1); it is O(1) only for g~a0 AND r_s >> L*")


# --- K4: where alpha_1 = 1 and 1e-4 -----------------------------------------
def alpha1_of_g(g, r):
    return alpha1(g, r)[0]


def solve_g(target, r):
    lo, hi = 1e-16, 1e4
    for _ in range(200):
        mid = math.sqrt(lo * hi)
        if alpha1_of_g(mid, r) > target:
            lo = mid
        else:
            hi = mid
    return math.sqrt(lo * hi)


g_at_1 = solve_g(1.0, 1.0 * MPC)          # r_s >> L*, so the pure u' branch
g_at_1em4 = solve_g(1e-4, 1.0 * MPC)
info(f"alpha_1 = 1    at g/a0 = {g_at_1/A0:.3f}   (analytic 1/sqrt(0.2)-1 = {1/math.sqrt(0.2)-1:.3f})")
info(f"alpha_1 = 1e-4 at g/a0 = {g_at_1em4/A0:.2f}  (analytic 1/sqrt(2.5e-5)-1 = {1/math.sqrt(2.5e-5)-1:.2f})")
check(abs(g_at_1 / A0 - (1 / math.sqrt(0.2) - 1)) < 1e-3
      and abs(g_at_1em4 / A0 - (1 / math.sqrt(2.5e-5) - 1)) < 0.05,
      "K4", f"{g_at_1/A0:.3f}, {g_at_1em4/A0:.2f} a0", "1.236, 199.0 a0",
      "alpha_1 = 4u'/(1-u'): unity at 1.24 a0, the PPN line 1e-4 at 199 a0")

# --- K5: the ladder ---------------------------------------------------------
ladder = []
for expo in range(22, -3, -1):
    g = A0 * 10.0 ** expo
    ladder.append((expo, alpha1_of_g(g, 1.0 * MPC)))
# g decreases down the list, so alpha_1 must INCREASE
mono = all(ladder[i][1] < ladder[i + 1][1] for i in range(len(ladder) - 1))
span = math.log10(ladder[-1][1] / ladder[0][1])
info("alpha_1(g), r_s >> L*: " + ", ".join(f"1e{e}a0:{a:.1e}" for e, a in ladder[:5]) + " ...  "
     f"1e{ladder[-1][0]}a0:{ladder[-1][1]:.2e}")
check(mono and span > 40, "K5", f"monotone={mono}, span={span:.1f} decades", "monotone, > 40",
      "alpha_1 spans 46 decades between a neutron-star surface and a galaxy: it is not a "
      "PPN parameter, it is a response function")

# --- K6: the crossover locus ------------------------------------------------
# alpha_1 = 1e-4 is a LOCUS in (g, r_s), not a single acceleration:
#   (i) for a source with r_s >~ 17.5 kAU the crossing is at g* = 96-199 a0
#       (199 a0 once r_s >~ 1 pc, because then D -> 1 and alpha_1 = 4u'/(1-u'));
#   (ii) for r_s < 17.5 kAU alpha_1 never reaches 1e-4: its maximum over g is
#        alpha_1(g->0) = 8 (r_s/L*)^2 < 1e-4.
r_x = LSTAR * math.sqrt(1e-4 / 8.0)          # = 17.5 kAU
g_star = solve_g(1e-4, LSTAR)
g_star_pc = solve_g(1e-4, 1.0 * PC)
g_star_8k = solve_g(1e-4, 8.0 * KPC)
g_star_20k = solve_g(1e-4, 20e3 * AU)
a1max_20k = alpha1_of_g(1e-20, 20e3 * AU)
a1max_18au = alpha1_of_g(1e-20, 18.0 * AU)
info(f"crossing at r_s = L*: g* = {g_star/A0:.1f} a0 = {g_star:.3e} m/s^2")
info(f"crossing at r_s = 1 pc: {g_star_pc/A0:.1f} a0; at 8 kpc: {g_star_8k/A0:.1f} a0; "
     f"at 20 kAU: {g_star_20k/A0:.1f} a0")
info(f"max over g: 20 kAU -> {a1max_20k:.2e} (= 8(r/L*)^2 = {8*(20e3*AU/LSTAR)**2:.2e}); "
     f"18 AU -> {a1max_18au:.1e}")
check(abs(g_star / A0 - 199.0) < 1.0 and abs(g_star_pc / g_star - 1) < 0.02
      and abs(8 * (r_x / LSTAR) ** 2 / 1e-4 - 1) < 1e-6
      and a1max_20k > 1e-4 and a1max_18au < 1e-6,
      "K6", f"{g_star/A0:.1f} a0, {g_star_pc/A0:.1f} a0, r_x={r_x/AU:.0f} AU, "
            f"max(20kAU)={a1max_20k:.1e}, max(18AU)={a1max_18au:.1e}",
      "199 a0, 199 a0, 17502 AU, >1e-4, <1e-6",
      "the 1e-4 line is a LOCUS: 199 a0 for any source larger than ~1 pc, 96 a0 at 20 kAU, "
      "and unreachable (max 8(r_s/L*)^2) below 17.5 kAU")

# --- K7: bilinearity of the alpha_1 Lagrangian ------------------------------
# Shao & Wex 2012 eq. (7):  L_a1 = -alpha_1 (G m1 m2 / r) (v1.v2)/(2 c^2),
# with v1, v2 the ABSOLUTE velocities w.r.t. the preferred frame.
m1, m2, al = sp.symbols("m1 m2 alpha1", positive=True)
Vx, Vy, Vz, ux, uy, uz = sp.symbols("Vx Vy Vz ux uy uz", real=True)
M = m1 + m2
v1 = sp.Matrix([Vx + m2 / M * ux, Vy + m2 / M * uy, Vz + m2 / M * uz])
v2 = sp.Matrix([Vx - m1 / M * ux, Vy - m1 / M * uy, Vz - m1 / M * uz])
dot = sp.expand(v1.T * v2)[0]
dot = sp.expand(dot)
V2 = Vx ** 2 + Vy ** 2 + Vz ** 2
Vu = Vx * ux + Vy * uy + Vz * uz
u2 = ux ** 2 + uy ** 2 + uz ** 2
target = V2 + (m2 - m1) / M * Vu - (m1 * m2 / M ** 2) * u2
r_b = sp.simplify(dot - target)
# is there any term with neither V nor u?  count monomials of total degree 0
poly = sp.Poly(dot, Vx, Vy, Vz, ux, uy, uz)
deg0 = sum(c for mon, c in zip(poly.monoms(), poly.coeffs()) if sum(mon) == 0)
info(f"v1.v2 = {dot}")
check(r_b == 0 and deg0 == 0, "K7", f"residual={r_b}, velocity-independent terms={deg0}", "0, 0",
      "the alpha_1 Lagrangian is BILINEAR in velocities: every alpha_1 observable carries "
      "(v/c)^2 with v in {V, u}. There is no alpha_1 effect at zeroth order in velocity.")

# --- K8: the preferred-frame acceleration from that Lagrangian --------------
# Test-body limit (m2 -> 0, m1 = M):  v1 = V, v2 = V + u, so
#   L = (1/2) m u^2 + G M m / r - (alpha_1/2)(G M m/c^2)(V^2 + V.u)/r .
# Euler-Lagrange in Cartesian components, rhat = r/|r|:
#   m a_i = d/dt(dL/du_i) - dL/dr_i
#         = (alpha_1/2)(G M m/c^2)[ V_i rdot - (V^2 + V.u) rhat_i ] / r^2 .
# Verify that identity symbolically, component by component.
Gsec, al1 = sp.symbols("Gsec alpha1", positive=True)
mm, MM, rr = sp.symbols("m M r", positive=True)
rdot = sp.symbols("rdot", real=True)
Vvec = [Vx, Vy, Vz]
uvec = [ux, uy, uz]
V2s = Vx ** 2 + Vy ** 2 + Vz ** 2
Vus = Vx * ux + Vy * uy + Vz * uz
dL = -(al1 / 2) * (Gsec * MM * mm / rr) * (V2s + Vus)
resid = 0
for i in range(3):
    # rhat_i = x_i/r ; d(1/r)/dx_i = -x_i/r^3, but with r and rhat independent we
    # differentiate w.r.t. r and multiply by rhat_i (chain rule for the radial dir)
    dL_du_i = sp.diff(dL, uvec[i])                       # = -(al/2) GMm V_i/(c^2 r)
    d_dt = sp.diff(dL_du_i, rr) * rdot                   # r-dot dependence of 1/r
    dL_dr = sp.diff(dL, rr)                              # = +(al/2) GMm (V^2+V.u)/r^2
    a_i = sp.simplify(d_dt - dL_dr - (al1 / 2) * Gsec * MM * mm
                      * (Vvec[i] * rdot - (V2s + Vus)) / rr ** 2)
    resid = sp.simplify(resid + a_i)
info(f"dL/du = {[sp.simplify(sp.diff(dL, q)) for q in uvec]}")
info(f"dL/dr  = {sp.simplify(sp.diff(dL, rr))}")
check(resid == 0, "K8", f"sum of component residuals = {resid}", "0",
      "preferred-frame acceleration: (alpha1/2)(GM/c^2)[V rdot - (V^2+V.u)rhat]/r^2 -- "
      "a V^2 piece (uniform G rescaling, absorbable) plus a V.u piece (velocity-dependent), "
      "verified in all three components")

# --- K9: rotation-curve decomposition and the monopole degeneracy -----------
# |w + v|^2 = w^2 + 2 w.v + v^2
mono = WC2
dip = 2.0 * (W_CMB / CLIGHT) * (220e3 / CLIGHT)
quad = (220e3 / CLIGHT) ** 2
info(f"at 8 kpc, v_rot = 220 km/s: monopole (w/c)^2 = {mono:.2e}, "
     f"dipole 2(w/c)(v/c) = {dip:.2e}, v^2 (v/c)^2 = {quad:.2e}")
# degeneracy: g -> g(1 + eps) is exactly M -> M(1 + eps) for a point mass
eps = sp.symbols("eps", real=True)
GM = sp.symbols("GM", positive=True)
g_pt = GM / rr ** 2
resid = sp.simplify(g_pt * (1 + eps) - (GM * (1 + eps)) / rr ** 2)
check(resid == 0, "K9", f"residual = {resid}", "0",
      "the monopole piece is exactly degenerate with the mass (a G-rescaling IS a "
      "M-rescaling): only the dipole and v^2 pieces are observable in one system")

# ============================================================================
# PART 2 -- the environment table
# ============================================================================
print()
print("-" * 78)
print("PART 2 -- alpha_1 in every environment with a bound, and its observable")
print("-" * 78)

FROZEN = a1_8kpc


def a1_env(g, r_s):
    if MUTATE == "freeze":
        return FROZEN
    return alpha1(g, r_s, drop_D=(MUTATE == "nolstar"))[0]


ENV = []

# --- environment definitions ------------------------------------------------
# Two kinds of row:
#   kind="coef" : the published bound IS a bound on alpha_1.  signature = alpha_1
#                 itself; margin = log10(bound / alpha_1).
#   kind="obs"  : the published precision is on a physical observable.  The
#                 alpha_1 signature is  s = alpha_1 (v/c)^2 c_k  (c_k = 1/2 for
#                 a mass/acceleration, 1/4 for a circular-speed), margin =
#                 log10(precision / s).

ENV = []

# --- 1. neutron-star surface (strong field) --------------------------------
g_ns = G_N * 1.4 * MSUN / (12e3) ** 2
ENV.append(dict(id="NS surface", g=g_ns, rs=12e3, v=355e3, kind="coef",
                test="pulsar alpha-hat_1", prec=PULSAR_ALPHA1_LIU))

# --- 2. pulsar-WD binary J1738+0333 ---------------------------------------
P_b = 0.3547907398724 * 86400.0
m_p, m_c = 1.46 * MSUN, 0.181 * MSUN
a_orb = (G_N * (m_p + m_c) * P_b ** 2 / (4 * math.pi ** 2)) ** (1.0 / 3.0)
g_pb = G_N * m_p / a_orb ** 2
v_pb = 2 * math.pi * a_orb / P_b
ENV.append(dict(id="PSR J1738+0333", g=g_pb, rs=a_orb, v=v_pb, kind="coef",
                test="pulsar alpha-hat_1 (xdot)", prec=PULSAR_ALPHA1))

# --- 3. wide pulsar-WD binary, P_b = 100 d --------------------------------
P_w = 100 * 86400.0
a_w = (G_N * (m_p + m_c) * P_w ** 2 / (4 * math.pi ** 2)) ** (1.0 / 3.0)
g_w = G_N * m_p / a_w ** 2
v_w = 2 * math.pi * a_w / P_w
ENV.append(dict(id="wide pulsar 100 d", g=g_w, rs=a_w, v=v_w, kind="coef",
                test="none (1e-3 assumed)", prec=1e-3))

# --- 4. Earth-Moon, LLR ---------------------------------------------------
g_llr = G_N * MSUN / AU ** 2
v_moon = 1.022e3
up_hedge = AU ** 2 / (2 * LAM ** 2)
a1_hedge = 4 * up_hedge / (1 + (LSTAR / AU) ** 2 * up_hedge / 2 - up_hedge)
ENV.append(dict(id="Earth-Moon (LLR)", g=g_llr, rs=AU, v=v_moon, kind="coef",
                test="orbit polarisation", prec=LLR_ALPHA1_1SIG,
                a1_override=max(alpha1(g_llr, AU)[0], a1_hedge), up_override=up_hedge))

# --- 5. wide binary, 18.6 AU (the task's 1.8e5 a0) ------------------------
r_18 = 18.8 * AU
g_18 = G_N * MSUN / r_18 ** 2
v_18 = math.sqrt(G_N * MSUN / r_18)
ENV.append(dict(id="wide binary 18.8 AU", g=g_18, rs=r_18, v=v_18, kind="obs",
                ck=0.5, test="Gaia rel. accel.", prec=1.2e-2))

# --- 6. wide binary, 20 kAU ----------------------------------------------
r_20k = 20e3 * AU
g_20k = G_N * MSUN / r_20k ** 2
v_20k = math.sqrt(G_N * MSUN / r_20k)
ENV.append(dict(id="wide binary 20 kAU", g=g_20k, rs=r_20k, v=v_20k, kind="obs",
                ck=0.5, test="Gaia rel. accel.", prec=1.2e-2))

# --- 7. outer solar system, 7000 AU --------------------------------------
r_7k = 7000 * AU
g_7k = G_N * MSUN / r_7k ** 2
v_7k = math.sqrt(G_N * MSUN / r_7k)
ENV.append(dict(id="outer SS 7000 AU", g=g_7k, rs=r_7k, v=v_7k, kind="obs",
                ck=0.5, test="none", prec=None))

# --- 8. galactic rotation at 8 kpc ---------------------------------------
g_8 = g_of_gN(gN_of_r(8.0 * KPC))
v_8 = 220e3
ENV.append(dict(id="rotation curve 8 kpc", g=g_8, rs=8.0 * KPC, v=v_8, kind="obs",
                ck=0.25, test="rotation curve / RAR", prec=1e-2))

# --- 9. cluster (Coma-like, OBSERVED v_c and r -- no Newtonian mass assumed) --
# v_c = 1000 km/s at r = 1 Mpc  =>  g = v^2/r = 0.35 a0.  In the framework's own
# law this needs only g_N = g^2/(g+a0) = 0.089 a0, i.e. M_bar(1 Mpc) = 1.2e14
# Msun -- plausible for a cluster.  This is the largest alpha_1 of any real
# environment, because clusters sit deepest in the MOND regime.
r_cl, v_cl = 1.0 * MPC, 1000e3
g_cl = v_cl ** 2 / r_cl
ENV.append(dict(id="cluster (Coma-like)", g=g_cl, rs=r_cl, v=v_cl, kind="obs",
                ck=0.5, test="cluster mass / sigma", prec=1e-2))

print(f"{'environment':22s} {'g/a0':>10s} {'uprime':>10s} {'alpha_1':>10s} "
      f"{'signature':>10s} {'precision':>10s} {'margin/dex':>11s}")
for e in ENV:
    e["a1"] = e.get("a1_override", a1_env(e["g"], e["rs"]))
    e["up"] = e.get("up_override", uprime(e["g"]))
    e["vc2"] = (e["v"] / CLIGHT) ** 2
    e["wcvc"] = (W_CMB / CLIGHT) * (e["v"] / CLIGHT)
    if e["kind"] == "coef":
        e["sig"] = e["a1"]
        e["margin"] = math.log10(e["prec"] / e["a1"]) if e["a1"] > 0 else 99.0
    else:
        # the largest NON-DEGENERATE piece: the (w/c)^2 monopole is exactly
        # degenerate with the mass, so use max((v/c)^2/2, (w/c)(v/c))
        e["sig"] = e["a1"] * max(e["vc2"] / 2.0, e["wcvc"])
        e["margin"] = (math.log10(e["prec"] / e["sig"])
                       if (e["prec"] is not None and e["sig"] > 0) else None)
    mstr = f"{e['margin']:11.2f}" if e["margin"] is not None else "        n/a"
    print(f"{e['id']:22s} {e['g']/A0:10.2e} {e['up']:10.2e} {e['a1']:10.3e} "
          f"{e['sig']:10.2e} {str(e['prec']):>10s} {mstr}")

# --- K10: LLR --------------------------------------------------------------
llr = [e for e in ENV if e["id"].startswith("Earth-Moon")][0]
up_slaved = uprime(llr["g"])
a1_slaved = a1_env(llr["g"], 4 * AU)          # k = 1/AU (the solar field)
a1_llr = max(abs(a1_slaved), abs(a1_hedge))
dr_theory = 3.844e8 * a1_llr * WC2
dr_bound = 3.844e8 * LLR_ALPHA1_1SIG * WC2
g_em = G_N * 5.972e24 / (3.844e8) ** 2
info(f"task's 'Earth-Moon 2.4e7 a0': Earth's field at the Moon is {g_em/A0:.2e} a0, the "
     f"Sun's at 1 AU {llr['g']/A0:.2e} a0 -- both give the same conclusion")
info(f"LLR: u'(slaved)={up_slaved:.2e}  u'(hedgehog,1AU)={up_hedge:.2e}")
info(f"LLR: alpha_1(slaved)={a1_slaved:.2e}  alpha_1(hedgehog)={a1_hedge:.2e}")
info(f"LLR: predicted range amplitude {dr_theory:.2e} m; the 9e-5 bound corresponds to "
     f"{dr_bound:.2e} m (LLR ranging is 2e-2 m)")
check(dr_theory < dr_bound / 1e8 and 1e-2 < dr_bound < 1.0,
      "K10", f"dr_pred={dr_theory:.2e} m, dr_at_bound={dr_bound:.2e} m", "< 1e-8 x bound; 1-100 cm",
      "LLR: alpha_1(theory) ~ 1e-13 in the environment where the 1e-4 bound is measured; "
      "the 9e-5 bound corresponds to a 5 cm lunar-range amplitude; the theory predicts 6e-11 m")

# --- K11: pulsars ----------------------------------------------------------
pb = [e for e in ENV if e["id"].startswith("PSR")][0]
wp = [e for e in ENV if e["id"].startswith("wide pulsar")][0]
check(pb["margin"] > 15 and wp["margin"] > 8,
      "K11", f"J1738 margin {pb['margin']:.1f} dex, wide-pulsar {wp['margin']:.1f} dex", "> 15, > 8",
      "binary pulsars: g/a0 ~ 1e9-1e12, so alpha_1 ~ 1e-17-1e-24 and the 2.1e-5..3.5e-5 "
      "strong-field bounds are satisfied by 13-19 decades")

# --- K12: wide binaries ----------------------------------------------------
g_task = 1.8e5 * A0
r_task = math.sqrt(G_N * MSUN / g_task)
wb = [e for e in ENV if "20 kAU" in e["id"]][0]
a1_deep = 8.0 * (wb["rs"] / LSTAR) ** 2
info(f"task's pair (20 kAU, 1.8e5 a0) is internally inconsistent: 1.8e5 a0 occurs at "
     f"{r_task/AU:.1f} AU for a 1 Msun binary; at 20 kAU g = {wb['g']/A0:.3f} a0")
info(f"deep-MOND limit: alpha_1 = 8(r/L*)^2 = {a1_deep:.2e} at 20 kAU (formula: {wb['a1']:.2e})")
check(abs(a1_deep / wb["a1"] - 1) < 0.05 and abs(r_task / AU - 18.8) < 0.2,
      "K12", f"8(r/L*)^2/alpha_1 = {a1_deep/wb['a1']:.3f}, r(1.8e5 a0) = {r_task/AU:.1f} AU",
      "1.00 +- 5%, 18.8 AU",
      "wide binary at 20 kAU: alpha_1 = 8(r/L*)^2 = 1.3e-4, the closest any environment "
      "comes to the 1e-4 line -- and its non-degenerate alpha_1 signature is 1e-13")

# --- K13: outer solar system ----------------------------------------------
oss = [e for e in ENV if "7000" in e["id"]][0]
g_165 = G_N * MSUN / (165 * AU) ** 2
a1_165 = alpha1(g_165, 165 * AU)[0]
da_7k = oss["a1"] * oss["vc2"] * oss["g"] / 2.0
da_7k_w = oss["a1"] * WC2 * oss["g"] / 2.0
info(f"7000 AU: g = {oss['g']/A0:.2f} a0, alpha_1 = {oss['a1']:.2e}; delta a = {da_7k:.1e} m/s^2 "
     f"(with w_CMB: {da_7k_w:.1e})")
info(f"Voyager 1 at 165 AU: g = {g_165/A0:.0f} a0, alpha_1 = {a1_165:.2e}")
check(oss["a1"] < 1e-4 and da_7k_w < 1e-15 and oss["margin"] is None,
      "K13", f"alpha_1={oss['a1']:.2e}, delta_a={da_7k_w:.1e} m/s^2", "< 1e-4, < 1e-15, no test",
      "the outer solar system is where g = a0, but the source is small compared with L*, "
      "so alpha_1 = 1.6e-5 and the predicted anomaly is 1e-21 m/s^2: no test exists")

# --- K14: rotation curve ---------------------------------------------------
rc = [e for e in ENV if "rotation" in e["id"]][0]
dv_v = rc["a1"] * rc["vc2"] / 4.0
dip_v = rc["a1"] * rc["wcvc"]
info(f"8 kpc: alpha_1 = {rc['a1']:.3f}; delta v/v = (alpha_1/4)(v/c)^2 = {dv_v:.2e} "
     f"({dv_v*220e3:.1e} m/s); dipole alpha_1(w/c)(v/c) = {dip_v:.2e}")
check(dv_v < 1e-6 and rc["margin"] > 4,
      "K14", f"dv/v={dv_v:.2e}, margin={rc['margin']:.2f} dex", "< 1e-6, > 4",
      "galactic rotation: alpha_1 = 0.93 but the signature is 1.3e-7 in v (8.4e-7 in the "
      "dipole): 4.1 decades below the 1e-2 rotation-curve systematics")

# --- K15: cluster ----------------------------------------------------------
cl = [e for e in ENV if "cluster" in e["id"]][0]
dv_cl = cl["a1"] * cl["vc2"] / 4.0
info(f"cluster: g = {cl['g']/A0:.2f} a0, alpha_1 = {cl['a1']:.3f}, v_c = {cl['v']/1e3:.0f} km/s, "
     f"delta v/v = {dv_cl:.2e}, delta M/M = {2*dv_cl:.2e}")
check(dv_cl < 1e-4 and 2.0 < cl["margin"] < 3.5,
      "K15", f"dv/v={dv_cl:.2e}, margin={cl['margin']:.2f} dex", "< 1e-4, 2-3.5 dex",
      "clusters are the CLOSEST environment to a test: alpha_1 = 4.9 (largest in nature), "
      "signature 2.7e-5 in mass, precision 1e-2 -> 2.6 decades short")

# ============================================================================
# PART 3 -- the decision
# ============================================================================
print()
print("-" * 78)
print("PART 3 -- is there ANY environment with alpha_1 = O(1) and a test?")
print("-" * 78)

# --- K16: the scan ---------------------------------------------------------
# margin = log10(precision/signature).  A test exists when the signature reaches
# the precision, i.e. margin <= 0.  Question: is there any environment with
# alpha_1 >= 0.1 AND margin <= 0?
o1 = [e for e in ENV if e["a1"] >= 0.1 and e["margin"] is not None]
with_test = [e for e in o1 if e["margin"] <= 0.0]
info(f"environments with alpha_1 >= 0.1: {[e['id'] for e in o1]}")
info(f"of those, with a test (margin <= 0): {[e['id'] for e in with_test]}")
min_margin_o1 = min(e["margin"] for e in o1) if o1 else None
check(len(with_test) == 0 and min_margin_o1 is not None and min_margin_o1 > 2.0,
      "K16", f"count={len(with_test)}, min margin={min_margin_o1:.2f} dex", "0, > 2 dex",
      "NO environment has both alpha_1 = O(0.1-5) and a measurement sensitive to the "
      "alpha_1 signature; the best (clusters) is 2.7 decades short")

# --- K17: the published bounds ARE alpha_1 (v/c)^2 measurements -------------
# LLR: an alpha_1 of 9e-5 produces a 5.3 cm lunar range amplitude -- the ranging
# precision over 35 yr.  Pulsar: 3.5e-5 with (w/c)(v/c) ~ 1.3e-6 -> an xdot
# sensitivity of order 1e-15 s/s, the quoted precision.
ratio_llr = dr_bound / 0.02
ratio_psr = PULSAR_ALPHA1 * (W_CMB / CLIGHT) * (v_pb / CLIGHT)
info(f"LLR: 9e-5 -> {dr_bound*100:.1f} cm vs 2 cm ranging -> factor {ratio_llr:.1f}")
info(f"pulsar: 3.5e-5 x (w/c)(v/c) = {ratio_psr:.1e} (eccentricity units)")
check(1.0 < ratio_llr < 10.0, "K17", f"{ratio_llr:.1f}", "1-10",
      "the published alpha_1 bounds are (v/c)^2-suppressed measurements: 9e-5 IS a 5 cm "
      "lunar range, i.e. 1.5e-6 x alpha_1 in relative terms")

# --- K18: A36 erratum ------------------------------------------------------
a1_k11_as_written = 2 * up_hedge / (1 + (LSTAR / AU) ** 2 * up_hedge / 2 - up_hedge)
a1_k11_factor4 = 4 * up_hedge / (1 + (LSTAR / AU) ** 2 * up_hedge / 2 - up_hedge)
info(f"A36 K11 as coded: {a1_k11_as_written:.3e}; with its own headline factor 4: "
     f"{a1_k11_factor4:.3e}; ratio {a1_k11_factor4/a1_k11_as_written:.2f}")
check(abs(a1_k11_factor4 / a1_k11_as_written - 2.0) < 1e-6 and a1_k11_factor4 < ALPHA1_BOUND,
      "K18", f"ratio={a1_k11_factor4/a1_k11_as_written:.2f}, value={a1_k11_factor4:.2e}", "2.00, < 1e-4",
      "A36's solar-system number uses factor 2 while its headline formula is factor 4: "
      "5.44e-14 should read 1.09e-13. Not load-bearing (both << 1e-4).")

# --- K19: A36's own section 8 ---------------------------------------------
a36_lo = 0.046 * WC2
a36_hi = 0.629 * WC2
info(f"A36 sec.8 claims alpha_1 v^2/c^2 = 2e-7..3e-6 at v=369 km/s; recomputed from its "
     f"own conservative route: {a36_lo:.1e}..{a36_hi:.1e}")
check(a36_lo < 1e-6 and 1e-7 < a36_hi < 2e-6,
      "K19", f"{a36_lo:.1e}..{a36_hi:.1e}", "within a factor 3 of 2e-7..3e-6",
      "A36 already states that its galactic alpha_1 produces only a 1e-7..1e-6 modulation, "
      "'below any present measurement' -- which contradicts its own EXCLUDED verdict")

# --- K20: the verdict logic ------------------------------------------------
coef_is_O1 = a1_1kpc > 1e-2 and a1_8kpc > 0.5
bound_satisfied_where_measured = min(
    [e["margin"] for e in ENV if e["kind"] == "coef"]) > 8.0
no_test_where_O1 = len(with_test) == 0
info(f"(a) coefficient O(1) in galaxies: {coef_is_O1}")
info(f"(b) every measured bound satisfied: min margin "
     f"{min(e['margin'] for e in ENV if e['kind']=='coef'):.1f} dex")
info(f"(c) no O(1) environment with a test: {no_test_where_O1}")
check(coef_is_O1 and bound_satisfied_where_measured and no_test_where_O1,
      "K20", f"{coef_is_O1}, {bound_satisfied_where_measured}, {no_test_where_O1}", "True, True, True",
      "VERDICT: A36's coefficient is right, its 'EXCLUDED' is over-scoped. What is excluded "
      "is the CLAIM alpha_1 = 0; the theory is not excluded by any alpha_1 measurement.")

# --- K22: the LLR safety is independent of the solar-system P configuration --
# alpha_1 = 4u'/(D-u') with D = 1+(kL*)^2 u'/2 is maximised over u' in (0,1] at
# u' -> 1, where alpha_1 -> 4/(1+(kL*)^2/2) -> 8/(kL*)^2.  At 1 AU that ceiling is
# 3.3e-13, whatever the local P field is (galactic background, hedgehog, or
# anything else).  This closes A36's K12 caveat ("the solar-system P
# configuration is not established") for the alpha_1 question.
ceil_au = 8.0 / (LSTAR / AU) ** 2
ceil_20k = 8.0 / (LSTAR / (20e3 * AU)) ** 2
# verify numerically that the ceiling is attained as u' -> 1
a1_at_up1_au = 4 * 1.0 / (1 + (LSTAR / AU) ** 2 * 1.0 / 2 - 1.0)
info(f"ceiling over the P configuration: alpha_1(1 AU) <= {ceil_au:.2e} "
     f"(at u'=1: {a1_at_up1_au:.2e}); at 20 kAU <= {ceil_20k:.2e}")
check(abs(a1_at_up1_au / ceil_au - 1) < 1e-6 and ceil_au < LLR_ALPHA1_1SIG / 1e8
      and abs(ceil_20k / a1max_20k - 1) < 0.02,
      "K22", f"{ceil_au:.2e}, {ceil_20k:.2e}", "3.3e-13, 1.3e-4",
      "alpha_1 at 1 AU is bounded by 8/(kL*)^2 = 3.3e-13 for ANY P configuration: "
      "the LLR pass does not depend on the open solar-system P sector")

# --- K21: the most conservative reading of the Nordtvedt channel ------------
# In the standard PPN bookkeeping alpha_1 enters the Nordtvedt parameter linearly,
# eta_N = 4beta - gamma - 3 - (10/3)xi - alpha_1 + (2/3)alpha_2 - ...  (Will 1993).
# Even reading that WITHOUT the (v/c)^2 suppression that every alpha_1 observable
# actually carries, the theory's solar-system alpha_1 gives
eta_theory = a1_llr
eta_bound = 7.2e-5                            # MESSENGER, Genova et al. 2018 [BOUNDS.md]
info(f"eta_N channel (no velocity suppression assumed): eta = {eta_theory:.2e} vs "
     f"bound {eta_bound:.1e} -> {math.log10(eta_bound/eta_theory):.1f} dex")
check(math.log10(eta_bound / eta_theory) > 8,
      "K21", f"{math.log10(eta_bound / eta_theory):.1f} dex", "> 8 dex",
      "even the most damaging reading of the Nordtvedt channel (alpha_1 enters eta_N "
      "linearly, no (v/c)^2) is satisfied by 8.7 decades")

# ============================================================================
print()
n_fail = len(FAIL)
print(f"{LANE} COMPLETE: {NCHK[0]-n_fail}/{NCHK[0]} checks PASS.")
if n_fail:
    print("FAILED:", FAIL)

# ---- results json ----------------------------------------------------------
if not MUTATE:
    res = {
        "lane": LANE,
        "status": "SURVIVES(alpha_1) + A36-VERDICT-OVER-SCOPED",
        "claim_level": "alpha_1 = 0 is REFUTED in the galactic regime (A36's coefficient stands)",
        "checks": ROWS,
        "numbers": {
            "alpha1_formula": "4*u'/(D-u'), D = 1+(kL*)^2 u'/2, u'=a0^2/(g+a0)^2",
            "a36_route_a_8kpc": a1_8kpc,
            "a36_route_a_1kpc": a1_1kpc,
            "a36_route_a_30kpc": a1_30kpc,
            "alpha1_unity_at_g_over_a0": g_at_1 / A0,
            "alpha1_1e4_at_g_over_a0": g_at_1em4 / A0,
            "crossover_locus": "alpha_1 = 1e-4 at g* = 199 a0 (r_s >= 1 pc), 96 a0 at "
                               "20 kAU, unreachable for r_s < 17.5 kAU (max 8(r_s/L*)^2)",
            "crossover_radius_deepMOND_AU": r_x / AU,
            "llr_alpha1_theory": a1_llr,
            "llr_alpha1_slaved": a1_slaved,
            "llr_alpha1_hedgehog": a1_hedge,
            "llr_predicted_range_m": dr_theory,
            "llr_range_at_bound_m": dr_bound,
            "llr_margin_dex": math.log10(LLR_ALPHA1_1SIG / a1_llr),
            "pulsar_alpha1_theory": pb["a1"],
            "pulsar_margin_dex": pb["margin"],
            "wide_binary_20kAU_alpha1": wb["a1"],
            "wide_binary_20kAU_g_over_a0": wb["g"] / A0,
            "outer_ss_7000AU_alpha1": oss["a1"],
            "outer_ss_7000AU_delta_a_w": da_7k_w,
            "rotation_8kpc_alpha1": rc["a1"],
            "rotation_8kpc_dv_over_v": dv_v,
            "rotation_margin_dex": rc["margin"],
            "cluster_alpha1": cl["a1"],
            "cluster_dv_over_v": dv_cl,
            "cluster_margin_dex": cl["margin"],
            "wc2_cmb": WC2,
            "environments": [{k: v for k, v in e.items()} for e in ENV],
            "min_margin_over_O1_envs": min_margin_o1,
            "n_envs_alpha1_ge_0p1": len(o1),
            "n_envs_with_test": len(with_test),
        },
        "constants_used": [
            "c = 2.99792458e8 m/s", "G = 6.67430e-11",
            "a0 = 9.36e-11 m/s^2 (canonical footing)", "L* = 24 pc, lambda = L*/sqrt2",
            "w_CMB = 369.82 km/s -> (w/c)^2 = 1.5217e-6",
            "alpha_1 bounds: LLR (-7+-9)e-5 [Muller 2005, DOOR11]; pulsar -3.5e-5..+3.3e-5 "
            "[Shao & Wex 2012]; pulsar |alpha-hat_1| < 2.1e-5 [Liu 2020, DOOR11]",
            "wide-binary relative-acceleration precision 1.2e-2 [A24 band width 0.012]",
            "rotation-curve / cluster relative precision 1e-2 (optimistic systematic)",
        ],
    }
    with open("a59_results.json", "w") as fh:
        json.dump(res, fh, indent=1)
    print("wrote a59_results.json")

sys.exit(1 if FAIL else 0)