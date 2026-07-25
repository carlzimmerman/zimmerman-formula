#!/usr/bin/env python3
r"""
WHAT IS THE GATE GATING?  THE KERNEL'S TWO AXES, AND WHETHER omega_c IS REDUNDANT
=================================================================================
de Sitter-Unruh MODIFIED-INERTIA framework (Carl Zimmerman).  Judged on ITS OWN terms:
no McGaugh nu, no standard-MOND lens, no covariant PDE work -- closed form + numerics only.

THE ACTION UNDER TEST (MI_FIELD_THEORY_RESULTS_2026.md Sec. 2.1):
    S_matter = -(1/2) INT sqrt(-g) rho_m [ s u^mu K(Box_u/a0^2) u_mu ],
    K(z) = (sqrt(1+4z)-1)/(2 sqrt z),   Box_u f = u^a nabla_a(u^b nabla_b f),   s = -1 (postulate).

THE PAPER MAKES TWO STATEMENTS THAT LOOK INCOMPATIBLE:
  (i) Sec. 3.1: "the literal frequency-domain evaluation gives |K(-omega^2 + i0)| = 1 (pure phase, no
      amplitude MOND) at every orbital frequency.  MOND lives entirely in the DC/secular sector."
 (ii) Sec. 5.2 + the committed window scripts: the phenomenological gate G(omega) = 1/(1 + i omega/omega_c)
      is evaluated AT THE ORBITAL FREQUENCY for BOTH window edges (omega_gal = V/r below,
      omega_planet = 2pi/T above).  reviews/mi_cassini_q2_omegac_2026.py labels this [ADOPTED #1],
      "the single load-bearing assumption of the whole calculation".

ASSIGNED ROLE, three parts:
  (1) Are (i) and (ii) consistent?  If MOND amplitude is DC-only, what is the gate gating?
  (2) REDUNDANCY TEST: does K's OWN frequency structure suppress the planetary anomaly by the required
      10^3-10^4x while leaving the galactic RAR intact?  If yes, omega_c (the free fifth constant)
      disappears and both the naturalness gap and the window-closure problem dissolve.
  (3) Both the galactic RAR and the sunward a0/2 planetary tail live in the SAME non-oscillating sector.
      Can a purely FREQUENCY-dependent gate separate them at all?  Does the action supply an
      ACCELERATION-dependent crossover instead?

AND THE CENTRAL TECHNICAL LEAD HANDED IN (to verify or refute, not assume):
      Box_u acts on the VECTOR u_mu.  On a circular orbit the jerk is -Omega^2 v, so Box_u may have
      EIGENVALUE -Omega^2 on u.  If so the galactic TANGENTIAL coefficient is set by arg K on the
      vector channel, NOT by the gate's |Im G| = 0.300 -- and those could differ by orders.

CALIBRATION HELD (Carl's standing rule; manufacture NEITHER a kill NOR a rescue):
  * Every load-bearing number on BOTH a0 footings (canon 9.355e-11 = cH_Lambda/Z; alt 1.13e-10 = cH0/Z).
  * The lead is TESTED, including its dimensions -- a wrong-dimension reading flips the answer by 4 orders
    and is shown explicitly (Sec. 2), then rejected against the paper's OWN forced corner a0/2c.
  * Where the kernel RESCUES a prong (galactic survival), the rescue is verified as hard as a kill would
    be, and the price is named.  Where it does NOT, the shortfall is quantified per planet.
  * No verdict string is hard-coded: every OPEN/EMPTY/PASS/FAIL below is computed from the numbers.
  * Bears on the GATE ONLY.  The MOND premise, a0 = cH_Lambda/Z, and the galactic RAR are UNTOUCHED.
  * No TOE language.  Never "theory closed".  sympy + numpy + scipy.  Exits 0.
"""
import numpy as np
import sympy as sp

RULE = "=" * 104
def head(s): print("\n" + RULE + "\n" + s + "\n" + RULE)

# ----------------------------------------------------------------------------------------------------
# 0. CONSTANTS, AND THE DIMENSIONAL AUDIT THAT FIXES THE KERNEL'S FREQUENCY ARGUMENT
# ----------------------------------------------------------------------------------------------------
C_LIGHT  = 2.99792458e8
A0_CANON = 9.355e-11          # a0 = c H_Lambda / Z   (rho_DE)   -- canonical
A0_ALT   = 1.13e-10           # a0 = c H_0 / Z        (rho_total) -- alternate
FOOTINGS = (("canon", A0_CANON), ("alt", A0_ALT))
YR, GYR  = 365.25 * 86400.0, 365.25 * 86400.0 * 1e9
KPC      = 3.0857e19
AU       = 1.495978707e11
GM_SUN   = 1.32712440018e20

# the binding galactic orbit -- the one that SETS the window's lower edge (paper Sec. 5.2)
OMEGA_GAL = 5.9414e-15        # UGC05721 innermost: V/r
R_GAL, V_GAL = 0.09 * KPC, 16.5e3
# the paper's committed window and its two edge conditions
OMEGA_C_LO   = 1.7824e-14     # 3 x OMEGA_GAL, from Re G >= 0.90 (footing-independent)
OMEGA_C_HI_C = 2.2113e-14     # LLR Gdot/G ceiling, canon
OMEGA_C_HI_A = 1.8306e-14     # LLR Gdot/G ceiling, alt
GATE_KEEP    = 0.90
# Fienga & Minazzoli 2024 per-planet delta_g bounds, and orbital elements
PLANETS = {  # name: (semi-major axis [m], period [d], eccentricity, delta_g bound [m/s^2])
    "Mercury": (5.7909e10, 87.9691,  0.20563, 4.6e-14),
    "Earth":   (1.4960e11, 365.256,  0.01671, 8.7e-15),
    "Mars":    (2.2794e11, 686.980,  0.09341, 1.4e-15),
    "Saturn":  (1.43353e12, 10759.22, 0.05648, 7.0e-15),
}

head("0.  DIMENSIONAL AUDIT -- what IS the kernel's argument at a frequency?  (load-bearing)")
print(f"""
  K's argument is z = Box_u/a0^2, and Box_u f = u^a nabla_a(u^b nabla_b f) = d^2 f/dtau^2.
  In geometrized (c = 1, tau in LENGTH) units d/dtau has 1/length and a0 -> a0/c^2 has 1/length, so
  z is dimensionless.  Converting an SI angular frequency omega [rad/s] into that variable:

        d^2/dtau_geo^2  ->  -(omega/c)^2        and      a0_geo^2 = (a0/c^2)^2
        =>   z(omega) = -(omega/c)^2 / (a0/c^2)^2 = -(omega c / a0)^2  ==  -Y,   Y = (omega c/a0)^2

  So the kernel's OWN frequency scale is omega_* = a0/c, and its BRANCH POINT z = -1/4 sits at
        omega_branch = a0/(2c) = {A0_CANON/(2*C_LIGHT):.4e} rad/s (canon) / {A0_ALT/(2*C_LIGHT):.4e} (alt).

  INDEPENDENT CONFIRMATION FROM THE PAPER ITSELF (this is not my choice of units):  Sec. 5.3 states
  "the action's OWN forced memory corner is omega_c = a0/2c = 1.56e-19 rad/s (tau_mem = 2c/a0)".
  That is EXACTLY the z = -1/4 branch point computed above ({A0_CANON/(2*C_LIGHT):.3e} vs the paper's 1.56e-19).
  The paper's own kernel-derived corner therefore pins the map omega -> z = -(omega c/a0)^2.

  WHY THIS MATTERS, stated before any physics:  the handed-in lead wrote the vector-channel argument as
  "-Omega^2/a0^2".  Read literally (SI omega over SI a0) that is -(5.94e-15/9.355e-11)^2 = -4.0e-9,
  i.e. |z| << 1/4 -- INSIDE the cut region, where (Sec. 1) K is PURE IMAGINARY, arg K = 90 deg exactly.
  Read with the correct c-factors it is -(omega c/a0)^2 = -3.6e+08, i.e. |z| >> 1/4 -- DEEP on the
  negative axis, where |K| = 1 and arg K ~ 1/(2 sqrt Y) is TINY.  The two readings differ by ~10^4 in the
  tangential coefficient.  The paper's own a0/2c corner settles it: the c-factors are there.
""")
assert abs(A0_CANON / (2 * C_LIGHT) / 1.56e-19 - 1) < 0.01, "a0/2c does not match the paper's stated corner"

def z_of_omega(omega, a0):     return -(omega * C_LIGHT / a0) ** 2
def Y_of_omega(omega, a0):     return (omega * C_LIGHT / a0) ** 2

# ----------------------------------------------------------------------------------------------------
# 1. THE KERNEL'S TWO AXES -- exact, symbolic.  This is the whole reconciliation in one table.
# ----------------------------------------------------------------------------------------------------
head("1.  K ON ITS TWO AXES:  the POSITIVE (acceleration) axis vs the NEGATIVE (frequency) axis")
zs, Xs, Ys, eps = sp.symbols("z X Y epsilon", positive=True)
Kf = lambda zz: (sp.sqrt(1 + 4 * zz) - 1) / (2 * sp.sqrt(zz))

# (a) POSITIVE axis z = +X : real, monotone 0 -> 1.  This is where the first-moment closure lives.
K_pos = sp.simplify(Kf(Xs))
K_pos_0 = sp.limit(K_pos, Xs, 0, "+")            # K(0) as the limit (0/0 at the point itself)
K_pos_inf = sp.limit(K_pos, Xs, sp.oo)
K_pos_UV = sp.series(K_pos, Xs, sp.oo, 3).removeO()
tail_abs = sp.simplify(sp.sqrt(Xs) * (1 - K_pos))            # (g/a0)*(1-K) = absolute anomaly / a0
tail_lim = sp.limit(tail_abs, Xs, sp.oo)

# (b) NEGATIVE axis beyond the branch point, z = -Y with Y > 1/4 : |K| = 1 exactly, pure phase.
K_neg = sp.simplify(Kf(-Ys).rewrite(sp.sqrt))
ReK = sp.sqrt(4 * Ys - 1) / (2 * sp.sqrt(Ys))
ImK = 1 / (2 * sp.sqrt(Ys))
mod2 = sp.simplify(ReK ** 2 + ImK ** 2)
argK = sp.atan(ImK / ReK)

# (c) the cut region -1/4 < z < 0 : K pure imaginary, arg = pi/2, |K| < 1.
K_cut_mod = sp.simplify((1 - sp.sqrt(1 - 4 * eps)) / (2 * sp.sqrt(eps)))

print(f"""
  (a) POSITIVE axis, z = +X  (X = |a|^2/a0^2, an ACCELERATION -- no frequency in it):
        K(X) real, K(0+) = {K_pos_0},  K(inf) = {K_pos_inf},  monotone, K ~ sqrt(X) near 0.
        UV expansion:  K(X) = {K_pos_UV}   =>  K - 1 = -1/(2 sqrt X) = -a0/(2g)
        ABSOLUTE anomaly  g(1 - K) = a0 * sqrt(X)(1-K(X)) -> a0 * {tail_lim}  =  a0/2, EXACTLY CONSTANT.
        <== THIS IS WHERE MOND LIVES.  It is the first-moment closure K(<Box_u>) = K(+|a|^2/a0^2).

  (b) NEGATIVE axis, z = -Y with Y > 1/4  (Y = (omega c/a0)^2, a FREQUENCY):
        Re K = {ReK} ,   Im K = {ImK}
        |K|^2 = {mod2}      <== UNIT MODULUS, EXACTLY, for EVERY Y > 1/4.  No amplitude, at any frequency.
        arg K = arctan(1/sqrt(4Y-1)) -> 1/(2 sqrt Y) = a0/(2 c omega)   for Y >> 1/4.
        <== THIS IS WHERE EVERY ORBITAL FREQUENCY LIVES (verified numerically in Sec. 4-5).

  (c) THE CUT REGION, -1/4 < z < 0  (frequencies BELOW a0/2c = 1.56e-19 rad/s):
        K pure imaginary, arg K = pi/2 exactly, |K| = {K_cut_mod} -> sqrt(eps), i.e. < 1 and -> 0.
        Nothing physical lands here: the lowest frequency in the problem (the binding galactic orbit)
        is {OMEGA_GAL/(A0_CANON/(2*C_LIGHT)):.2e} x ABOVE the branch point.

  ==> RECONCILIATION OF THE PAPER'S TWO STATEMENTS.  Both are TRUE, and they are true for ONE reason:
      the MOND amplitude and the orbital frequencies live on OPPOSITE SIDES OF THE KERNEL'S BRANCH CUT.
        * MOND amplitude  -> POSITIVE z (argument X = (g/a0)^2).  K real, 0 -> 1, carries the a0/2 tail
          and the RAR.  There is NO frequency variable on this axis at all.
        * orbital response -> NEGATIVE z (argument -(omega c/a0)^2).  |K| = 1 identically: the kernel
          returns a PHASE and nothing else.  There is no amplitude here to suppress.
      "MOND lives entirely in the DC/secular sector" is thus more precisely: MOND lives on the
      POSITIVE-z / moment-closure axis, which is FREQUENCY-FREE.  And |K| = 1 is not a coincidence of
      the orbital regime -- it is an identity on the whole axis where any frequency can appear.
""")
assert sp.simplify(mod2 - 1) == 0, "|K|^2 = 1 on the negative axis failed"
assert K_pos_0 == 0 and K_pos_inf == 1, "K(0+)=0 / K(inf)=1 failed"
assert sp.simplify(tail_lim - sp.Rational(1, 2)) == 0, "absolute a0/2 tail limit failed"
# BRANCH CHECK: the (ReK, ImK) pair above must BE K(-Y + i0), not a guess.  Numerical, retarded (+i0).
for Yv in (0.30, 1.0, 7.5, 1e3, 3.6252e8):
    zc = complex(-Yv, 1e-18)
    Kc = (np.emath.sqrt(1 + 4 * zc) - 1) / (2 * np.emath.sqrt(zc))
    Kp = np.sqrt(4 * Yv - 1) / (2 * np.sqrt(Yv)) + 1j / (2 * np.sqrt(Yv))
    assert abs(Kc - Kp) < 1e-10, f"branch mismatch at Y={Yv}: {Kc} vs {Kp}"
    assert abs(abs(Kc) - 1) < 1e-12, f"|K(-Y+i0)| != 1 at Y={Yv}"
# and INSIDE the cut region K must be pure imaginary with |K| < 1
for ev in (1e-9, 0.01, 0.2):
    zc = complex(-ev, 1e-24)
    Kc = (np.emath.sqrt(1 + 4 * zc) - 1) / (2 * np.emath.sqrt(zc))
    assert abs(Kc.real) < 1e-9 and 0 < abs(Kc) < 1, f"cut-region structure failed at eps={ev}"
# the modulus on the negative axis must be 1 at the two physical frequencies, both footings
for _, a0 in FOOTINGS:
    for wv in (OMEGA_GAL, 2 * np.pi / (PLANETS["Saturn"][1] * 86400.0)):
        Yv = Y_of_omega(wv, a0)
        assert abs(np.hypot(np.sqrt(4 * Yv - 1) / (2 * np.sqrt(Yv)), 1 / (2 * np.sqrt(Yv))) - 1) < 1e-12
        assert Yv > 0.25, "a physical orbital frequency landed inside the cut region"

# ----------------------------------------------------------------------------------------------------
# 2. THE HANDED-IN LEAD, TESTED: is Box_u really an EIGENVALUE operator on u?  (exact relativistic helix)
# ----------------------------------------------------------------------------------------------------
head("2.  THE LEAD TESTED EXACTLY -- Box_u on the VECTOR u for an exact circular (helical) worldline")
tau, Om, R, bet = sp.symbols("tau Omega R beta", positive=True)
gam = 1 / sp.sqrt(1 - R ** 2 * Om ** 2)
phi = gam * Om * tau
u = sp.Matrix([gam, -gam * R * Om * sp.sin(phi), gam * R * Om * sp.cos(phi), 0])   # exact 4-velocity
eta = sp.diag(-1, 1, 1, 1)
def dd(v):  return sp.simplify(sp.diff(v, tau))
u_dot  = dd(u)                       # = a^mu
u_ddot = dd(u_dot)                   # = Box_u u^mu  (flat space, u^a nabla_a = d/dtau)
norm   = sp.simplify((u.T * eta * u)[0, 0])
a2     = sp.simplify((u_dot.T * eta * u_dot)[0, 0])
first  = sp.simplify((u.T * eta * u_ddot)[0, 0])
# the eigenvalue claim: Box_u u = -(gamma Omega)^2 * (AC part of u), zero on the timelike DC part
u_DC = sp.Matrix([gam, 0, 0, 0])
u_AC = sp.simplify(u - u_DC)
resid_eig = sp.simplify(u_ddot - (-(gam * Om) ** 2) * u_AC)
n_AC = sp.simplify((u_AC.T * eta * u_AC)[0, 0])
print(f"""
  Exact flat-space helix (no slow-motion approximation): u^mu = gamma(1, -beta sin phi, beta cos phi, 0),
  beta = R Omega, gamma = 1/sqrt(1-beta^2), phi = gamma Omega tau (PROPER-time phase).

    u.u                      = {norm}          (unit norm, exact)
    |a|^2 = a.a              = {sp.simplify(a2)}
    u_mu Box_u u^mu          = {sp.simplify(first)}
    u_mu Box_u u^mu + |a|^2  = {sp.simplify(first + a2)}     <== the FIRST-MOMENT IDENTITY, exact

  THE EIGENVALUE STRUCTURE (the lead's claim), tested componentwise:
    split u = u_DC + u_AC,  u_DC = (gamma,0,0,0) [timelike, constant],  u_AC = spatial, rotating at
    proper frequency gamma*Omega.  Then
        Box_u u^mu  -  ( -(gamma Omega)^2 ) u_AC^mu  =  {sp.simplify(resid_eig.T)}   (must be all zeros)
    i.e.  Box_u u_DC = 0   and   Box_u u_AC = -(gamma Omega)^2 u_AC.   TWO eigenvalues: 0 and -(gam Om)^2.

  ==> THE LEAD IS VERIFIED, WITH ITS DIMENSIONS CORRECTED.  Box_u IS diagonal on u with eigenvalue
      -(gamma Omega)^2 on the direction-carrying (AC) part -- exactly the jerk = -Omega^2 v statement.
      In K's dimensionless variable that is  z = -(gamma Omega c/a0)^2, NOT -(Omega/a0)^2 (Sec. 0).

  AND THE SAME DECOMPOSITION EXPLAINS THE FIRST MOMENT, which is the reconciliation's mechanism:
      u.u    = {norm}   is carried ALMOST ENTIRELY by the DC (timelike) part;
      u_AC.u_AC = {sp.simplify(n_AC)} = (gamma beta)^2 is the AC share of the norm.
      So  u_mu Box_u u^mu = -(gamma Omega)^2 * (gamma beta)^2 = -|a|^2, and the normalized first moment
      <Box_u>_u = (u Box_u u)/(u.u) = +|a|^2 is POSITIVE only because u.u = -1 is NEGATIVE.
      The first moment is a RAYLEIGH QUOTIENT, not an eigenvalue: +|a|^2 is NOT in the spectrum of
      Box_u (which is {{0, -(gamma Omega)^2}}, both <= 0).  It is smaller than the AC eigenvalue by the
      norm share (gamma beta)^2, and it has the OPPOSITE SIGN.  THAT is how one operator produces both
      an acceleration-axis (MOND) argument and a frequency-axis (phase) argument.
""")
assert sp.simplify(first + a2) == 0, "first-moment identity failed on the exact helix"
assert all(sp.simplify(c) == 0 for c in resid_eig), "Box_u is NOT diagonal on (u_DC, u_AC)"

# the paper's own honesty check, reproduced from the same decomposition: moments match only at n = 1
print("  THE PAPER'S OWN n-th MOMENT CHECK, reproduced from this decomposition (Sec. 3.1: 'matches only")
print("  at n = 1').  Ratio  [u_mu Box_u^n u^mu] / [(a^2)^n (u.u)]  must be 1 at n=1 and not at n>1:")
for n in (1, 2, 3):
    lhs = sp.simplify((-(gam * Om) ** 2) ** n * n_AC)
    rhs = sp.simplify(a2 ** n * norm)
    print(f"      n = {n}:  ratio = {sp.simplify(lhs/rhs)}")
assert sp.simplify(sp.simplify((-(gam*Om)**2)**1 * n_AC) / sp.simplify(a2**1 * norm) - 1) == 0
assert sp.simplify(sp.simplify((-(gam*Om)**2)**2 * n_AC) / sp.simplify(a2**2 * norm) - 1) != 0
print("  MATCHES the paper's committed statement exactly -- so this decomposition IS the paper's own\n"
      "  'literal frequency-domain evaluation', now made explicit rather than quoted.\n")

# ----------------------------------------------------------------------------------------------------
# 3. WHAT THE LITERAL SPECTRAL EVALUATION OF THE ACTION ACTUALLY GIVES (and why it is not the closure)
# ----------------------------------------------------------------------------------------------------
head("3.  THE LITERAL DRESSING  u^mu K(Box_u/a0^2) u_mu  ON A CIRCULAR ORBIT -- computed, not assumed")
print(f"""
  With Box_u diagonal on (u_DC, u_AC) [Sec. 2], the operator K acts channel by channel with NO
  approximation:
        u_mu K(Box_u/a0^2) u^mu  =  (u_DC.u_DC) K(0)  +  (u_AC.u_AC) K(-(gamma Omega c/a0)^2)
                                 =  (-gamma^2) * K(0)  +  (gamma beta)^2 * K(-Y)
  and K(0) = 0 EXACTLY (Sec. 1, and the paper's Sec. 2.1 sum rule uses K(0) = 0).  Therefore

        u K u  =  (gamma beta)^2 K(-Y)    with   |K(-Y)| = 1

  READ WHAT THAT SAYS, both ways, without softening either:
    * NO MOND.  The a0-dependence has collapsed to a phase; |u K u| = (gamma beta)^2 = (v/c)^2, a
      post-Newtonian-order number with no a0 in its modulus at all.
    * NO NEWTONIAN LIMIT EITHER.  The standard kinetic term needs u K u -> u.u = -1 (i.e. K -> 1);
      here the timelike channel that CARRIES the norm is annihilated by K(0) = 0, so the literal
      evaluation returns {(V_GAL/C_LIGHT)**2:.2e} (galaxy) / {(np.sqrt(GM_SUN/PLANETS['Saturn'][0])/C_LIGHT)**2:.2e} (Saturn) instead of -1.
  So the literal spectral reading is DEGENERATE: it is not a small correction to the closure, and the
  closure is NOT its omega -> 0 limit (that limit gives K(0) = 0, i.e. nothing).  The moment closure
  K(Box_u) -> K(<Box_u>) is a genuinely SEPARATE prescription -- which is exactly what the paper says
  it is ("--first moment-->"), and exactly why eta(beta) is listed as an irreducible constant.
""")
v_sat = np.sqrt(GM_SUN / PLANETS["Saturn"][0])
print(f"    AC norm share (gamma beta)^2:  binding galactic orbit {(V_GAL/C_LIGHT)**2:.3e},  Saturn "
      f"{(v_sat/C_LIGHT)**2:.3e}   (needed for a Newtonian limit: 1)\n"
      f"    FOOTING-INDEPENDENT by construction: (gamma beta)^2 = (v/c)^2 contains no a0, and "
      f"|K(-Y)| = 1 on both footings (Sec. 1 assertions).")

# ----------------------------------------------------------------------------------------------------
# 4. THE CENTRAL NUMBER: the galactic TANGENTIAL coefficient -- kernel phase vs the gate's |Im G| = 0.300
# ----------------------------------------------------------------------------------------------------
head("4.  THE CENTRAL NUMBER -- galactic tangential coefficient:  sin(arg K) vs the gate's |Im G| = 0.300")
def gbar_from_gobs(gobs, a0):
    """exact a0-line inversion g_obs^2 - g_bar^2 = a0 g_bar."""
    return (-a0 + np.sqrt(a0 ** 2 + 4 * gobs ** 2)) / 2.0
def argK_neg(omega, a0):
    Yv = Y_of_omega(omega, a0)
    return float(np.arctan(1.0 / np.sqrt(4 * Yv - 1.0)))

# the gate's own lower-edge coefficient, from the machine-verified one-pole identity |G|^2 = Re G
ImG_edge = float(np.sqrt(GATE_KEEP - GATE_KEEP ** 2))
print(f"""
  THE GATE'S CLAIM (Reading A, the paper's own prescription).  The one-pole identity |G|^2 = Re G makes
  the lower-edge condition Re G >= {GATE_KEEP} algebraically identical to |Im G| = sqrt(ReG - ReG^2) =
  {ImG_edge:.4f} EXACTLY.  A prograde tangential force = {ImG_edge:.1%} of the MOND anomaly at the binding orbit.

  THE KERNEL'S CLAIM (same channel, same geometry, but the coefficient taken from the ACTION).  A pure
  phase applied to a rotating radial vector IS a tangential component of relative size sin(arg K):
        sin(arg K(-(Omega c/a0)^2))  with  arg K -> a0/(2 c Omega)   for Y >> 1/4.
  Both act on the same rotating radial anomaly; they differ ONLY in the lag angle.  Compare them:
""")
print(f"  {'footing':<8}{'Omega_gal':>12}{'Y':>12}{'kernel lag [rad]':>18}{'kernel lag [deg]':>18}"
      f"{'gate lag [deg]':>16}{'ratio gate/kernel':>19}")
print("  " + "-" * 102)
tang = {}
for lab, a0 in FOOTINGS:
    ak = argK_neg(OMEGA_GAL, a0)
    coef = float(np.sin(ak))
    gate_lag = float(np.arctan(OMEGA_GAL / OMEGA_C_LO))
    tang[lab] = (coef, ak, gate_lag)
    print(f"  {lab:<8}{OMEGA_GAL:>12.4e}{Y_of_omega(OMEGA_GAL,a0):>12.4e}{ak:>18.4e}"
          f"{np.degrees(ak):>18.3e}{np.degrees(gate_lag):>16.2f}{ImG_edge/coef:>19.3e}")
print(f"""
  ==> THE LEAD'S SUSPICION IS CONFIRMED QUANTITATIVELY.  The galactic tangential coefficient implied by
      the ACTION'S OWN KERNEL is {tang['canon'][0]:.3e} (canon) / {tang['alt'][0]:.3e} (alt), NOT {ImG_edge:.3f}.
      The phenomenological gate over-states the lag by {ImG_edge/tang['canon'][0]:.2e}x (canon) / {ImG_edge/tang['alt'][0]:.2e}x (alt).
      Mechanism identical (pure phase on a rotating radial vector -> tangential force); magnitude
      different by four orders, because the kernel's lag is a0/(2 c Omega) while the gate's is
      Omega/omega_c, and omega_c = 1.78e-14 sits {OMEGA_C_LO/(A0_CANON/(2*C_LIGHT)):.2e}x above the kernel's own corner a0/2c.
""")

# now re-derive Section-7-of-the-pincer's galactic survival with the KERNEL coefficient
gobs = V_GAL ** 2 / R_GAL
print(f"  GALACTIC SURVIVAL RE-DERIVED (binding orbit r = 0.09 kpc, V = 16.5 km/s, g_obs = {gobs:.4e}):")
print(f"  {'footing':<8}{'A_gal = g_obs-g_bar':>21}{'coefficient':>14}{'f_t':>12}"
      f"{'dlnr/dt [/Gyr]':>17}{'e-fold time':>16}{'vs 10 Gyr':>12}{'verdict':>10}")
print("  " + "-" * 102)
surv = {}
for lab, a0 in FOOTINGS:
    A_gal = gobs - gbar_from_gobs(gobs, a0)
    for src, coef in (("GATE |ImG|", ImG_edge), ("KERNEL sin(argK)", tang[lab][0])):
        f_t = A_gal * coef
        rate = f_t / V_GAL                      # flat-RC form, same as the pincer's Sec. 7
        efold = 1.0 / rate
        surv[(lab, src)] = (rate, efold)
        unit = "Myr" if efold < 1e3 * GYR / 1e3 else "Gyr"
        val = efold / (GYR / 1e3) if unit == "Myr" else efold / GYR
        print(f"  {lab+'/'+src.split()[0]:<8}{A_gal:>21.4e}{coef:>14.4e}{f_t:>12.3e}"
              f"{rate*GYR:>17.3e}{f'{val:.1f} {unit}':>16}{efold/(10*GYR):>12.3e}"
              f"{'SURVIVES' if efold > 10*GYR else 'DESTROYED':>10}")
print(f"""
  ==> READING A'S GALACTIC-DESTRUCTION PRONG IS REFUTED BY THE ACTION'S OWN KERNEL, on both footings.
      With the gate's coefficient the binding orbit e-folds in ~{surv[('canon','GATE |ImG|')][1]/(GYR/1e3):.0f} Myr (the pincer's 42-58 Myr).
      With the kernel's coefficient it e-folds in {surv[('canon','KERNEL sin(argK)')][1]/GYR:.0f} Gyr (canon) / {surv[('alt','KERNEL sin(argK)')][1]/GYR:.0f} Gyr (alt)
      -- a margin of {surv[('canon','KERNEL sin(argK)')][1]/(10*GYR):.0f}x / {surv[('alt','KERNEL sin(argK)')][1]/(10*GYR):.0f}x against a 10 Gyr disk age.  No galactic tangential problem.
      VERIFIED AS HARD AS A KILL: the coefficient is not fitted -- it is arg K at the kernel's own
      argument, with the c-factors pinned by the paper's own a0/2c corner (Sec. 0), and its ~10^-5 size
      is forced by Omega_gal/(a0/2c) ~ {OMEGA_GAL/(A0_CANON/(2*C_LIGHT)):.1e} being large, which is footing-stable to 21%.
      THE PRICE, named: this rescue is available ONLY on the vector/frequency axis -- the same axis on
      which |K| = 1, i.e. the axis that supplies NO amplitude suppression anywhere.  Section 5 collects.
""")

# ----------------------------------------------------------------------------------------------------
# 4B. THE INTERMEDIATE READING, BOUNDED -- and the omega_c window RE-DERIVED from that bound
# ----------------------------------------------------------------------------------------------------
head("4B. INTERMEDIATE (PARTIAL-LAG) READINGS -- bound the galactic tangential coefficient, redo omega_c")
OMEGA_MOON = 2.6653e-6
R_MOON, V_MOON = 3.844e8, 2.6653e-6 * 3.844e8
LLR_ALLOW = (5.0 + 2 * 9.6) * 1e-15 / YR       # |cen| + 2 sigma, Biskupek/Mueller 2021, per second
print(f"""
  Sections 4 and 5 compare two SPECIFIC responses.  A general "partial direction lag" reading is any
  causal response W(omega) = m(omega) exp(-i * lag(omega)) applied to the rotating radial anomaly:
        RADIAL (reactive) retention   = m cos(lag)        TANGENTIAL (dissipative) = T = m sin(lag)
  Four constraints, each written as a bound on (m, T) at a measured frequency, no gate form assumed:
    (G1) galactic RAR         m(Omega_gal) cos(lag) >= {GATE_KEEP}
    (G2) galactic survival    T(Omega_gal) <= V/(A_gal * 10 Gyr)          <- derived below
    (P1) per-planet delta_g   m(Omega_p) cos(lag) <= delta_g_p/(a0/2)     <- ALL FOUR planets, min taken
         (NOTE: the binding planet is NOT the one with the tightest delta_g.  A rolloff suppresses by
          x = Omega_p/omega_r, so the SLOWEST planet is least suppressed: Mars has the tightest bound but
          Saturn, at 1/16 of Mars's orbital frequency, is the binding one.  Computed, not assumed.)
    (L1) LLR secular drift    T(Omega_Moon) <= LLR_allow * v_Moon / a0    <- derived below
""")
print(f"  {'footing':<8}{'A_gal':>12}{'T_max (G2)':>13}{'kernel T':>12}{'margin':>10}"
      f"{'gate T=0.300':>14}{'gate over by':>14}{'T_max (L1)':>13}")
print("  " + "-" * 102)
bounds = {}
for lab, a0 in FOOTINGS:
    A_gal = gobs - gbar_from_gobs(gobs, a0)
    T_gal_max = V_GAL / (A_gal * 10 * GYR)
    T_moon_max = LLR_ALLOW * V_MOON / a0
    bounds[lab] = (A_gal, T_gal_max, T_moon_max)
    print(f"  {lab:<8}{A_gal:>12.4e}{T_gal_max:>13.4e}{tang[lab][0]:>12.4e}"
          f"{T_gal_max/tang[lab][0]:>10.1f}x{ImG_edge:>14.3f}{ImG_edge/T_gal_max:>13.1f}x{T_moon_max:>13.4e}")
# regression: mapping T_gal_max back onto a SINGLE-POLE gate must reproduce the record's 4.1e-12 / 4.7e-12
print(f"\n  REGRESSION -- map the G2 bound onto a SINGLE-POLE gate (|Im G| ~ Omega/omega_c for x << 1):")
for lab, a0 in FOOTINGS:
    wc_need = OMEGA_GAL / bounds[lab][1]
    hi = OMEGA_C_HI_C if lab == "canon" else OMEGA_C_HI_A
    print(f"    {lab:<6} omega_c >= {wc_need:.3e} rad/s  = {wc_need/hi:.0f}x above the LLR edge {hi:.3e}"
          f"   (record says ~4.1e-12 / ~4.7e-12, ~186x / ~257x)")
    assert wc_need > hi, "single-pole intermediate unexpectedly opened -- recompute, do not assert"
# regression: the L1 bound must reproduce the paper's own LLR-derived upper edge
wc_from_L1 = bounds["canon"][2] * OMEGA_MOON
print(f"    L1 check: T_moon_max * Omega_Moon = {wc_from_L1:.4e} reproduces the paper's canon upper edge "
      f"{OMEGA_C_HI_C:.4e} ({abs(wc_from_L1/OMEGA_C_HI_C-1)*100:.1f}%)")
assert abs(wc_from_L1 / OMEGA_C_HI_C - 1) < 0.03, "L1 bound does not reproduce the committed upper edge"

print(f"""
  THE STRUCTURAL POINT, then the honest escape.  For any SINGLE-POLE response the one-pole identity
  |G|^2 = Re G rigidly ties m to lag, so G1 (m cos >= 0.90) FORCES T >= {ImG_edge:.3f} and G2 is violated by
  {ImG_edge/bounds['canon'][1]:.0f}x (canon) / {ImG_edge/bounds['alt'][1]:.0f}x (alt).  For the KERNEL, |K| = 1 ties them the other way: T small
  FORCES cos(lag) = sqrt(1 - T^2) >= {np.sqrt(1-bounds['canon'][1]**2):.9f}, i.e. the radial retention is 1 to within
  {1-np.sqrt(1-bounds['canon'][1]**2):.1e} -- the FULL a0/2 tail.  Neither can satisfy G1+G2+P1 together.
  So the escape, if one exists, must DECOUPLE m from lag -- which needs more than one pole.  Test the
  minimal such overlay honestly (a double pole, g(t) = omega_r^2 t exp(-omega_r t) theta(t), causal,
  positive, normalised) and see whether it opens a window:
""")
def W2(x):   return 1.0 / (1.0 + 1j * x) ** 2          # double-pole overlay, x = omega/omega_r
def m2(x):   return abs(W2(x))
def T2(x):   return abs(np.imag(W2(x)))
def Rr2(x):  return abs(np.real(W2(x)))
print(f"  {'footing':<8}{'edge G1 (RAR)':>16}{'edge G2 (survival)':>20}"
      f"{'edge P1 (planets)':>19}{'binding planet':>16}{'edge L1 (LLR)':>16}{'window':>9}")
print("  " + "-" * 102)
from scipy.optimize import brentq
inter = {}
for lab, a0 in FOOTINGS:
    A_gal, T_gal_max, T_moon_max = bounds[lab]
    # lower edges: larger omega_r => smaller x_gal => radial retention -> 1 and T -> 0.
    # brackets stay on the monotone branch: |Re W2| = |1-x^2|/(1+x^2)^2 falls on (0,1);
    # T2 = 2x/(1+x^2)^2 RISES on (0, 1/sqrt3 = 0.577) and falls after, so cap the galactic bracket there.
    lo_G1 = OMEGA_GAL / brentq(lambda x: Rr2(x) - GATE_KEEP, 1e-6, 0.9)
    lo_G2 = OMEGA_GAL / brentq(lambda x: T2(x) - T_gal_max, 1e-12, 0.55)
    # upper edges: smaller omega_r => larger x => more suppression.  Stay above the x=1 zero of Re W2
    # and above the T2 peak, so both are monotone decreasing on the bracket.  ALL FOUR planets.
    hi_P1, bind_p = np.inf, None
    for pname, (aP, TP, eP, dg) in PLANETS.items():
        wP = 2 * np.pi / (TP * 86400.0)
        cand = wP / brentq(lambda x: Rr2(x) - dg / (a0 / 2.0), 2.0, 1e12)
        if cand < hi_P1:
            hi_P1, bind_p = cand, pname
    hi_L1 = OMEGA_MOON / brentq(lambda x: T2(x) - T_moon_max, 2.0, 1e12)
    lo, hi = max(lo_G1, lo_G2), min(hi_P1, hi_L1)
    inter[lab] = (lo, hi, lo_G1, lo_G2, hi_P1, hi_L1, bind_p)
    print(f"  {lab:<8}{lo_G1:>16.3e}{lo_G2:>20.3e}{hi_P1:>19.3e}{bind_p:>16}{hi_L1:>16.3e}"
          f"{('x%.1f' % (hi/lo)) if hi > lo else 'EMPTY':>9}")
lo_c, hi_c_i = inter["canon"][0], inter["canon"][1]
print(f"""
  ==> AN INTERMEDIATE READING DOES EXIST, AND ITS WINDOW IS NON-EMPTY.  Reported at full strength
      because the calibration rule cuts both ways: the double-pole overlay opens
        omega_r in [{inter['canon'][0]:.3e}, {inter['canon'][1]:.3e}] rad/s (canon, width x{inter['canon'][1]/inter['canon'][0]:.0f})
        omega_r in [{inter['alt'][0]:.3e}, {inter['alt'][1]:.3e}] rad/s (alt,   width x{inter['alt'][1]/inter['alt'][0]:.0f})
      i.e. WIDER than the paper's single-pole window (x1.24 canon / x1.03 alt).  Mechanism: a double
      pole rolls the AMPLITUDE off as 1/x^2 while its stopband phase approaches 180 deg, so the
      tangential residue dies as 1/x^3.  That structurally demotes the LLR drift (edge {inter['canon'][5]:.2e}) which
      binds the single-pole window from above, and hands the upper edge to the SLOWEST planet
      ({inter['canon'][6]}, edge {inter['canon'][4]:.2e}) -- so the galactic survival edge and the planetary edge no longer
      collide.  The binding planet is {inter['canon'][6]}, NOT Mars: Mars has the tightest delta_g bound but
      {inter['canon'][6]}'s orbital frequency is ~16x lower, so a rolloff suppresses it ~250x less.

      WHAT IT COSTS, stated exactly, because this is not a free rescue:
        1. It is NOT in the action.  The kernel's response on this channel has |K| = 1 (order ZERO
           rolloff); a double pole is a second, different memory function.
        2. It adds a DISCRETE assumption (the rolloff ORDER n >= 2) on top of the continuous corner --
           so the constant count does not merely stay at five, it gains structure.
        3. The corner moves the WRONG WAY for naturalness: {lo_c/(A0_CANON/(2*C_LIGHT)):.1e}x to {hi_c_i/(A0_CANON/(2*C_LIGHT)):.1e}x the kernel's own scale
           a0/2c, versus {OMEGA_C_LO/(A0_CANON/(2*C_LIGHT)):.1e}x for the single pole.  The naturalness gap WIDENS by ~3-4 orders.
        4. It is a pure overlay: nothing in Sections 1-3 supplies it, and Section 8 shows the obvious
           way of putting a pole INSIDE the kernel is pathological.
      So the pincer is NOT a closed dichotomy -- but the escape is an amendment with a bigger price tag
      than the object it rescues, not a reading of the written action.

  AND IT IS NOT A FREE SAVE, BECAUSE IT IS FALSIFIABLE DIFFERENTLY.  A corner 3-4 orders ABOVE the
  single-pole one leaves the gate WIDE OPEN at wide-binary frequencies, where the paper's single-pole
  window deliberately closes it (Sec. 5.4: "<= 6.2% of the MOND boost at <= 20 kAU, 0.8% at 10 kAU").
  Retention at a 1 Msun binary, computed for both overlays:""")
for sep_kau in (3.0, 10.0, 20.0):
    r_wb = sep_kau * 1e3 * AU
    w_wb = np.sqrt(GM_SUN / r_wb ** 3)
    x1 = w_wb / OMEGA_C_HI_C
    x2 = w_wb / inter["canon"][1]
    print(f"    {sep_kau:>5.0f} kAU:  Omega = {w_wb:.3e} rad/s   single-pole (omega_c = {OMEGA_C_HI_C:.2e}) "
          f"Re G = {1/(1+x1**2):>8.4f}   double-pole (omega_r = {inter['canon'][1]:.2e}) |Re W| = {Rr2(x2):>8.4f}")
print(f"""
  The single-pole numbers bracket the paper's committed 0.0%-6.2% band; the double-pole escape instead
  predicts ESSENTIALLY FULL AQUAL-strength wide-binary boost.  The paper's own Sec. 5.4 falsifier is
  therefore INVERTED by the escape: "a confirmed Chae-type AQUAL-strength wide-binary boost kills the
  gated survivor outright" becomes, on the double-pole reading, a CONFIRMATION -- and a NULL wide-binary
  result kills the escape instead.  So the intermediate branch is not a hedge: Gaia DR4 discriminates
  the two overlays directly, in opposite directions.  Recorded as a live fork, not as a rescue.
""")
assert inter["canon"][1] > inter["canon"][0] and inter["alt"][1] > inter["alt"][0], \
    "double-pole window came out empty -- report THAT, do not assert it open"

# ----------------------------------------------------------------------------------------------------
# 5. THE REDUNDANCY TEST -- can K ALONE do the gate's job?  (three candidate channels, four planets)
# ----------------------------------------------------------------------------------------------------
head("5.  REDUNDANCY TEST -- does K's OWN frequency structure suppress the planets and spare the RAR?")
print(f"""
  THE TEST, stated so it can fail: omega_c is redundant iff SOME K-only frequency response R(omega)
  simultaneously satisfies
      (i)  PLANETS:  R(Omega_planet) <= delta_g_bound / (a0/2)  at EVERY planet  (10^3-10^4x suppression)
      (ii) RAR:      R(Omega_gal)    >= {GATE_KEEP}              at the binding deep-MOND orbit
  K offers exactly three candidate frequency responses on the negative axis.  All three, both footings:
      R1 = |K(-Y)|              (the amplitude channel -- the one the delta_g bounds constrain)
      R2 = sin(arg K(-Y))       (the phase/tangential channel -- Section 4)
      R3 = 1 - Re K(-Y)         (the in-phase DEFICIT, the only amplitude-like frequency dependence)
""")
def one_minus_ReK(w, a0):
    """1 - sqrt(1 - 1/(4Y)) written as x/(1+sqrt(1-x)) so it does not underflow at planetary Y ~ 1e20."""
    x = 1.0 / (4.0 * Y_of_omega(w, a0))
    return float(x / (1.0 + np.sqrt(1.0 - x)))
chan = {"R1 |K|":       lambda w, a0: 1.0,
        "R2 sin(argK)": lambda w, a0: float(np.sin(argK_neg(w, a0))),
        "R3 1-ReK":     one_minus_ReK}
assert one_minus_ReK(2 * np.pi / (PLANETS["Saturn"][1] * 86400.0), A0_CANON) > 0, "R3 underflowed"
print(f"  {'footing':<7}{'channel':<15}{'R(gal)':>12}{'RAR ok':>8}"
      f"{'worst planet':>14}{'R(planet)':>12}{'R needed':>11}{'shortfall':>12}{'planets ok':>11}{'REDUNDANT':>11}")
print("  " + "-" * 102)
redundant_any = False
for lab, a0 in FOOTINGS:
    for cname, f in chan.items():
        Rg = f(OMEGA_GAL, a0)
        rar_ok = Rg >= GATE_KEEP
        worst, worst_short, worst_R, worst_need = None, -1.0, None, None
        for pname, (aP, TP, eP, dg) in PLANETS.items():
            wP = 2 * np.pi / (TP * 86400.0)
            Rp = f(wP, a0)
            need = dg / (a0 / 2.0)
            short = Rp / need
            if short > worst_short:
                worst, worst_short, worst_R, worst_need = pname, short, Rp, need
        pl_ok = worst_short <= 1.0
        red = rar_ok and pl_ok
        redundant_any = redundant_any or red
        print(f"  {lab:<7}{cname:<15}{Rg:>12.4e}{'YES' if rar_ok else 'NO':>8}{worst:>14}"
              f"{worst_R:>12.3e}{worst_need:>11.3e}{worst_short:>12.3e}"
              f"{'YES' if pl_ok else 'NO':>11}{'YES' if red else 'NO':>11}")
print(f"""
  ==> ANSWER TO (2):  NO.  omega_c IS NOT REDUNDANT.  No K-only channel passes both halves, and the
      failures are structural, not marginal:
        R1 (amplitude):  |K| = 1 IDENTICALLY -- the RAR half passes trivially and the planetary half
            fails by exactly the full ungated factor (Mars {(A0_CANON/2)/PLANETS['Mars'][3]:.0f}x canon / {(A0_ALT/2)/PLANETS['Mars'][3]:.0f}x alt).  K's
            frequency dependence has ZERO amplitude content, so there is nothing here to suppress with.
        R2 (phase):  DOES separate the scales, and in the RIGHT DIRECTION -- arg K falls as 1/Omega, so
            it is smallest at the planets and largest in galaxies, ratio Omega_Sat/Omega_gal = {2*np.pi/(PLANETS['Saturn'][1]*86400.0)/OMEGA_GAL:.2e},
            comfortably >= the required 10^3-10^4.  It fails on the OTHER half and on CHANNEL: its
            galactic value {tang['canon'][0]:.2e} is {GATE_KEEP/tang['canon'][0]:.1e}x below the 0.90 the RAR needs, and a phase cannot
            carry a radial reactive amplitude at all -- it is not what the delta_g bounds constrain.
            This is the tangential channel of Sec. 4, doing its own (different) job.
        R3 (in-phase deficit):  separates by (Omega_Sat/Omega_gal)^2 = {(2*np.pi/(PLANETS['Saturn'][1]*86400.0)/OMEGA_GAL)**2:.2e} -- enormous -- but its
            galactic retention is {chan['R3 1-ReK'](OMEGA_GAL, A0_CANON):.2e}, i.e. RAR-DEAD by {GATE_KEEP/chan['R3 1-ReK'](OMEGA_GAL, A0_CANON):.1e}x.  Same disease as the paper's
            own forced corner a0/2c (Sec. 5.3): it gates off the rotation curves too.
      So the free fifth constant does NOT disappear.  But the reason it does not is worse for the gate
      than a mere shortfall -- see Section 6.
""")
assert not redundant_any, "a K-only channel passed both halves -- rewrite the verdict, do not assert"

# ----------------------------------------------------------------------------------------------------
# 6. PART (3): CAN A FREQUENCY GATE SEPARATE TWO OBJECTS THAT LIVE ON THE ACCELERATION AXIS?
# ----------------------------------------------------------------------------------------------------
head("6.  FREQUENCY vs ACCELERATION AS THE SEPARATOR -- what the action does and does not supply")
gN = {p: GM_SUN / PLANETS[p][0] ** 2 for p in PLANETS}
print(f"""
  BOTH the galactic RAR and the sunward a0/2 tail are POSITIVE-z / first-moment-closure objects
  (Sec. 1a): their argument is X = (g/a0)^2, an ACCELERATION.  Neither carries a frequency.  A gate
  G(omega) is a NEGATIVE-z object.  So the gate and its targets are on opposite sides of the cut:

    * applied to the closure sector as written (its own variable is DC): omega = 0, G(0) = 1 for EVERY
      omega_c -> the gate suppresses NOTHING, at planets or galaxies.  (Prong B / Fork C of the record.)
    * applied to the vector/frequency channel where a frequency does exist: the kernel there has
      |K| = 1 (Sec. 1b), so the gate is not READING the action -- it is REPLACING the action's own
      response on that channel with a different one whose lag is {ImG_edge/tang['canon'][0]:.0e}x larger (Sec. 4).

  DOES THE ACTION SUPPLY AN ACCELERATION-DEPENDENT CROSSOVER INSTEAD?  It supplies one, and it is
  EXACTLY INSUFFICIENT -- computed, not asserted.  On the positive axis (Sec. 1a, exact):
        FRACTIONAL boost   nu - 1 = 1/(2y) + O(1/y^2),  y = g/a0   -> dies as 1/g.  SEPARATES.
        ABSOLUTE anomaly   g(1 - K) = a0/2                          -> CONSTANT.   DOES NOT SEPARATE.
  The per-planet delta_g bounds constrain the ABSOLUTE anomaly.  Numerically:
""")
print(f"  {'planet':<9}{'y = g_N/a0 (canon)':>20}{'nu-1 (fractional)':>19}{'absolute [m/s^2]':>18}"
      f"{'bound':>11}{'excl. canon':>13}{'excl. alt':>11}")
print("  " + "-" * 102)
for p, (aP, TP, eP, dg) in PLANETS.items():
    y = gN[p] / A0_CANON
    print(f"  {p:<9}{y:>20.4e}{1/(2*y):>19.4e}{A0_CANON/2:>18.4e}{dg:>11.1e}"
          f"{(A0_CANON/2)/dg:>13.0f}x{(A0_ALT/2)/dg:>10.0f}x")
# what falloff WOULD clear Mars, and what an exponential-tail kernel would give
aM, TM, eM, dgM = PLANETS["Mars"]
yM = gN["Mars"] / A0_CANON
need_frac = dgM / gN["Mars"]
print(f"""
  WHAT AN ACCELERATION SEPARATOR WOULD HAVE TO DO, and whether one is available:
      Mars needs   nu - 1 <= {need_frac:.3e}   at y = {yM:.3e};   the framework's K gives 1/(2y) = {1/(2*yM):.3e}
      shortfall = {1/(2*yM)/need_frac:.3e}x  (this IS the paper's {int(round((A0_CANON/2)/dgM))}x, re-derived on the fractional axis).
      An exponential-tail interpolation (nu - 1 ~ exp(-sqrt(y)) form) would give log10(nu-1) =
      {-np.sqrt(yM)/np.log(10):.4e} at Mars, i.e. it clears the bound by ~10^{int(round(np.log10(need_frac) + np.sqrt(yM)/np.log(10)))} orders.
      So an ACCELERATION separator is not merely adequate, it is enormously over-adequate.
      THE COST, stated exactly:  it is not available inside the written action.  K's large-X tail
      -1/(2 sqrt X) is rigid -- it is the same coefficient that produces the framework's flagship EXACT
      identity g_obs^2 - g_bar^2 = a0 g_bar (the a0-line, its sharpest measurement lever) and the exact
      circular collapse 1 + 4(y^2+y) = (2y+1)^2.  Killing the tail requires a DIFFERENT kernel, which
      forfeits the exact a0-line and re-opens the high-acceleration tail the paper already lists as
      undecided (Sec. 7.5).  That is a new assumption with a named, quantified price -- not a free move,
      and NOT a claim that the framework is closed.

  ==> ANSWER TO (3):  a purely FREQUENCY-dependent gate cannot separate the RAR from the a0/2 tail,
      because both are frequency-free closure objects.  This is fatal to the GATE CONCEPT as a reading
      of the action (not to the action, and not to the a0 reframing).  The separator would have to be
      the ACCELERATION scale; the action's own acceleration structure separates the FRACTIONAL boost
      (which no experiment bounds tightly) and provably not the ABSOLUTE anomaly (which they do).
""")

# ----------------------------------------------------------------------------------------------------
# 7. THE ONE REMAINING DOOR: eccentric orbits give the SCALAR channel AC content.  Is it enough?
# ----------------------------------------------------------------------------------------------------
head("7.  THE ECCENTRIC DOOR -- on a NON-circular orbit |a| oscillates.  Can a gate then bite?")
def kepler_abs_a(e, aP, n=200000):
    """|a| = GM/r^2 sampled uniformly in TIME over one orbit (Kepler equation, exact)."""
    M = np.linspace(0.0, 2 * np.pi, n, endpoint=False)
    E = M.copy()
    for _ in range(80):
        E = E - (E - e * np.sin(E) - M) / (1 - e * np.cos(E))
    r = aP * (1 - e * np.cos(E))
    return GM_SUN / r ** 2
print(f"""
  On a circular orbit X = |a|^2/a0^2 is strictly DC, so the gate sees omega = 0 (prong B).  With
  eccentricity, |a(t)| oscillates at harmonics of Omega and the SCALAR channel acquires AC content that
  a low-pass gate WOULD suppress.  Does that rescue the planets?  Decompose the deep-Newton dressing
  deficit  d(t) = 1 - K(X(t)) = a0/(2|a(t)|)  into DC + AC, gate ONLY the AC part (G(n Omega) -> 0 for
  omega_c << Omega, the actual planetary regime), and see what anomaly SURVIVES:

        surviving anomaly (orbit-averaged) = <d>_DC * <|a|>  =  (a0/2) * <1/|a|> * <|a|>  >=  a0/2
  by Cauchy-Schwarz.  So gating the scalar AC content does not reduce the tail -- it INCREASES it.
""")
print(f"  {'planet':<9}{'e':>8}{'<1/|a|><|a|>':>15}{'surviving/(a0/2)':>19}"
      f"{'AC share of d':>15}{'excl. canon after':>19}{'relief':>10}")
print("  " + "-" * 102)
ecc_relief = []
for p, (aP, TP, eP, dg) in PLANETS.items():
    absa = kepler_abs_a(eP, aP)
    d = 1.0 / absa                                  # proportional to a0/(2|a|)
    cs = float(d.mean() * absa.mean())              # <1/|a|><|a|>
    ac_share = float(d.std() / d.mean())
    surviving = cs                                  # in units of a0/2
    excl_after = surviving * (A0_CANON / 2) / dg
    ecc_relief.append(excl_after)
    print(f"  {p:<9}{eP:>8.5f}{cs:>15.6f}{surviving:>19.6f}{ac_share:>15.4f}"
          f"{excl_after:>18.0f}x{'NONE' if surviving >= 1.0 else 'some':>10}")
print(f"""
  ==> THE ECCENTRIC DOOR IS SHUT, and quantitatively so.  On every planet <1/|a|><|a|> >= 1 (Cauchy-
      Schwarz, saturated only for e = 0), so the DC part of the dressing deficit -- the part a low-pass
      gate cannot touch -- already reproduces the FULL a0/2 tail or slightly more.  Worst planet after
      gating the entire AC content: still {max(ecc_relief):.0f}x over its bound (canon).  Eccentricity supplies AC
      content in the scalar channel but the anomaly it carries is a REDISTRIBUTION, not an addition:
      the ungated DC residue is bounded BELOW by the circular answer.
""")
assert min(ecc_relief) > 1.0, "an eccentric planet fell below its bound -- recompute, do not assert"

# ----------------------------------------------------------------------------------------------------
# 8. WHERE DOES THE GATE'S POLE SIT IN THE KERNEL'S OWN VARIABLE?  (secondary, flagged)
# ----------------------------------------------------------------------------------------------------
head("8.  WHAT IF THE GATE WERE PUT INSIDE THE ACTION?  the multiplicative embedding, mapped into z")

def K_c(zz):  return (np.emath.sqrt(1 + 4 * zz) - 1) / (2 * np.emath.sqrt(zz))
def G_c(zz, zeta): return 1.0 / (1.0 + 1j * np.emath.sqrt(-zz) / zeta)
print(f"""
  Sections 1-7 treat the gate as the record does: an overlay ON the closure result.  This section asks
  the natural follow-up -- could the gate instead be put INSIDE the action, as a second factor in the
  kernel, K(z) -> K(z) G(z)?  That is the ONE embedding that keeps the gate's own quoted form.  Mapping
  G(omega) = 1/(1 + i omega/omega_c) into the kernel's variable via omega = (a0/c) sqrt(-z) (Sec. 0):

        G(z) = 1 / (1 + i sqrt(-z)/zeta),        zeta = c omega_c / a0 .

  Its denominator VANISHES at sqrt(-z) = i zeta, i.e. at  z = +zeta^2  --  on the POSITIVE REAL AXIS,
  which is precisely the acceleration axis where the first-moment closure (and hence all of MOND) lives.
  In acceleration units the divergence sits at |a| = c omega_c.  Verified numerically below, and then
  located in the solar system, because c omega_c turns out to land somewhere specific:
""")
zeta_ref = C_LIGHT * OMEGA_C_LO / A0_CANON
for d in (1e-1, 1e-3, 1e-5, 1e-7):
    zz = zeta_ref ** 2 * (1 + d)
    print(f"    |G| at z = (1+{d:.0e}) zeta^2 :  {abs(G_c(zz, zeta_ref)):.4e}"
          f"   -> diverges as 1/|z/zeta^2 - 1|, a simple pole ON the positive axis")
assert abs(G_c(zeta_ref ** 2 * (1 + 1e-7), zeta_ref)) > 1e6, "no pole found at z = +zeta^2"
print(f"\n  {'footing':<8}{'edge':<5}{'omega_c':>12}{'|a|_pole = c omega_c':>22}{'in a0':>12}"
      f"{'heliocentric r':>17}{'nearest planet':>16}")
print("  " + "-" * 102)
for lab, a0, wchi in (("canon", A0_CANON, OMEGA_C_HI_C), ("alt", A0_ALT, OMEGA_C_HI_A)):
    for edge, wcv in (("lo", OMEGA_C_LO), ("hi", wchi)):
        a_pole = C_LIGHT * wcv
        r_pole = np.sqrt(GM_SUN / a_pole)
        print(f"  {lab:<8}{edge:<5}{wcv:>12.4e}{a_pole:>22.4e}{a_pole/a0:>12.3e}"
              f"{r_pole/AU:>14.1f} AU{'Neptune (30.07 AU)':>19}")
# properly-scaled Herglotz probe: the sample MUST span the pole scale zeta^2 ~ 3e9, or it is blind
rng = np.random.default_rng(20260725)
Rr = 10.0 ** rng.uniform(-3, 13, 200000)
th = rng.uniform(1e-6, np.pi - 1e-6, 200000)
pts = Rr * np.exp(1j * th)
imK  = np.imag(K_c(pts))
imKG = np.imag(K_c(pts) * G_c(pts, zeta_ref))
imG  = np.imag(G_c(pts, zeta_ref))
fK, fKG, fG = (float((v >= -1e-12).mean()) for v in (imK, imKG, imG))
worst = int(np.argmin(imKG))
print(f"""
  UPPER-HALF-PLANE POSITIVITY PROBE (200,000 points, |z| log-uniform over 10^-3..10^13 so the sample
  actually SPANS the pole scale zeta^2 = {zeta_ref**2:.3e} -- a probe confined to |z| < 100 is blind here and
  returns a spurious clean bill of health).  A Herglotz function has Im f >= 0 throughout the UHP; that
  positivity is what makes K's spectral measure positive and the reduction ghost-free (paper 2.1/2.3):
        fraction with Im K    >= 0 :  {fK:.4f}     <- the kernel alone: clean, as the paper states
        fraction with Im G    >= 0 :  {fG:.4f}     <- the gate factor alone is ANTI-Herglotz in z
        fraction with Im K*G  >= 0 :  {fKG:.4f}     <- the product loses positivity on {1-fKG:.0%} of the UHP
        worst point |z|/zeta^2 = {abs(pts[worst])/zeta_ref**2:.3f}  (the violation is centred on the pole scale)

  READ THIS WITH ITS SCOPE.  What is computed: the MULTIPLICATIVE embedding K -> K*G is pathological --
  it puts a simple pole of the inertial dressing at a PHYSICAL acceleration |a| = c omega_c = {C_LIGHT*OMEGA_C_LO:.2e}
  m/s^2 ({C_LIGHT*OMEGA_C_LO/A0_CANON:.1e} a0), i.e. at ~30-33 AU for every corner of the paper's committed window, and it
  breaks the Herglotz positivity on which the paper's own ghost-freedom and unique-measure results rest.
  What is NOT computed, and NOT claimed: that no OTHER embedding works (an additive or resummed
  insertion could move or cancel the pole), nor any ghost claim -- that needs the full KL analysis.
  So this section says the gate cannot be made part of the action THE ONE OBVIOUS WAY, which reinforces
  Sections 1-7 (the gate is an amendment, not a reading) without being load-bearing for the verdict.
""")
assert fK > 0.999 and fKG < 0.999, "positivity probe did not discriminate K from K*G"

# ----------------------------------------------------------------------------------------------------
# 9. VERDICT
# ----------------------------------------------------------------------------------------------------
head("9.  VERDICT")
c_can, c_alt = tang["canon"][0], tang["alt"][0]
ef_can = surv[("canon", "KERNEL sin(argK)")][1] / GYR
ef_alt = surv[("alt", "KERNEL sin(argK)")][1] / GYR
print(f"""
  (1) ARE THE PAPER'S TWO STATEMENTS CONSISTENT?  YES -- and the reason is the sharp answer to the
      pincer.  K has a BRANCH CUT, and the two statements refer to its two sides:
        POSITIVE z (= X = (g/a0)^2, an acceleration):  K real, 0 -> 1.  The RAR and the a0/2 tail live
          here.  NO FREQUENCY VARIABLE EXISTS ON THIS AXIS.
        NEGATIVE z (= -(omega c/a0)^2, a frequency):  |K| = 1 EXACTLY (sympy-verified), pure phase
          arg K -> a0/(2 c omega).  Every orbital frequency lives here.  NO AMPLITUDE EXISTS HERE.
      The first moment <Box_u>_u = +|a|^2 is a RAYLEIGH QUOTIENT (positive only because u.u = -1), not
      an eigenvalue; the eigenvalues of Box_u on u are {{0, -(gamma Omega)^2}}, both <= 0 (Sec. 2, exact
      relativistic helix, and it reproduces the paper's own "moments match only at n = 1" check).
      SO WHAT IS THE GATE GATING?  Neither sector coherently:
        - on the DC/closure sector (where the MOND AMPLITUDE is): its variable is DC, G(0) = 1, no
          suppression at any omega_c -- and if it DID bite there it would suppress the RAR itself;
        - on the vector/frequency sector (where a frequency exists): the action's own response there
          already has |K| = 1, so there is no amplitude to gate; the gate REPLACES the kernel's lag
          a0/(2 c Omega) with Omega/omega_c, {ImG_edge/c_can:.1e}x larger at the binding galactic orbit.
      PRECISE STATEMENT OF THE INCONSISTENCY: the gate is applied to a POSITIVE-AXIS (amplitude) object
      using a NEGATIVE-AXIS (frequency) argument that object does not possess.  omega_c is not only a
      free constant (paper Sec. 5.3, already conceded) -- its ARGUMENT is also supplied by hand.

  (2) IS omega_c REDUNDANT?  NO.  Tested on all three frequency channels K actually has, both footings,
      four planets (Sec. 5), with the pass criteria written to be failable:
        |K| = 1 identically      -> RAR safe, planets fail by the FULL ungated factor (Mars 33429x canon
                                    / 40357x alt).  Zero amplitude content in K's frequency dependence.
        sin(arg K)               -> separates by Omega_Sat/Omega_gal ~ 1.1e6 (>= the needed 1e3-1e4) but
                                    it is a PHASE: galactic retention {c_can:.2e} << 0.90.  Wrong channel.
        1 - Re K                 -> separates by ~1.3e12 but galactic retention {chan['R3 1-ReK'](OMEGA_GAL, A0_CANON):.2e} = RAR-dead.
      The free fifth constant does NOT disappear; the naturalness gap and the window-closure problem do
      NOT dissolve.  (Had one channel passed, the price would have been named; none did.)

  (3) FREQUENCY vs ACCELERATION SEPARATOR.  Both the RAR and the a0/2 tail are closure objects with the
      SAME (frequency-free) variable, so a purely frequency-dependent gate CANNOT separate them.  That
      is fatal to the GATE CONCEPT as a reading of the written action.  The action does supply an
      acceleration crossover, and it is provably the wrong kind: nu - 1 = 1/(2y) separates the
      FRACTIONAL boost, while the ABSOLUTE anomaly g(1-K) = a0/2 is EXACTLY CONSTANT (sympy) -- and the
      ephemeris delta_g bounds constrain the absolute one.  An exponential-tail kernel would clear Mars
      by hundreds of orders, but it forfeits the exact a0-line g_obs^2 - g_bar^2 = a0 g_bar and the
      exact circular collapse.  That is the identified cost of the only working separator.

  WHICH PRONG OF THE PINCER DOES THE ACTION IMPLY?  PRONG B, for a sharper reason than the record's.
      * READING A's galactic-destruction prong is REFUTED.  The tangential coefficient set by the
        ACTION is sin(arg K) = {c_can:.3e} (canon) / {c_alt:.3e} (alt), not the gate's {ImG_edge:.3f}: an
        over-statement of {ImG_edge/c_can:.2e}x / {ImG_edge/c_alt:.2e}x.  The binding deep-MOND orbit then e-folds in
        {ef_can:.0f} Gyr (canon) / {ef_alt:.0f} Gyr (alt), a margin of {ef_can/10:.0f}x / {ef_alt/10:.0f}x against a 10 Gyr disk age.
        The 42-58 Myr galactic catastrophe, and the ~186x/~257x window-emptiness that followed from it,
        are ARTIFACTS OF THE PHENOMENOLOGICAL GATE, not consequences of the action.  So the pincer does
        NOT close: one jaw is removed by the action's own kernel.
      * READING B is UPHELD and STRENGTHENED.  The upheld half is not "G(0) = 1" (a property of the
        chosen gate) but "|K(-omega^2 + i0)| = 1 at every orbital frequency" (an IDENTITY of the
        action's kernel, Sec. 1b): the action supplies NO amplitude suppression at ANY frequency.  The
        ungated sunward a0/2 tail therefore stands, excluded 1017x-40357x per planet (canon) /
        1228x-40357x+ (alt), and the eccentric-orbit escape is shut by Cauchy-Schwarz (Sec. 7).
        The two jaws are ONE inequality, now visible: on the kernel's channel radial retention is
        cos(lag) = sqrt(1 - T^2) exactly, so galactic survival (T <= {bounds['canon'][1]:.2e}) FORCES radial retention
        >= 1 - {1-np.sqrt(1-bounds['canon'][1]**2):.0e}.  Tangential-safe and radial-suppressed are mutually exclusive at |K| = 1.

  IS THERE AN INTERMEDIATE?  YES -- and it is reported at full strength, not buried (Sec. 4B).  Decoupling
      the lag from the modulus requires MORE THAN ONE POLE, and the minimal such overlay (a causal double
      pole, g(t) = omega_r^2 t e^(-omega_r t)) has a NON-EMPTY window, WIDER than the paper's:
        omega_r in [{inter['canon'][0]:.2e}, {inter['canon'][1]:.2e}] rad/s canon (x{inter['canon'][1]/inter['canon'][0]:.0f});  [{inter['alt'][0]:.2e}, {inter['alt'][1]:.2e}] alt (x{inter['alt'][1]/inter['alt'][0]:.0f})
      because T ~ 1/x^3 in a double-pole stopband demotes the LLR drift and hands the upper edge to the
      SLOWEST planet ({inter['canon'][6]}), computed over all four rather than assumed.  ITS PRICE: not in the
      action (|K| = 1 is order-ZERO rolloff); a DISCRETE new assumption (order n >= 2) on top of the
      corner; and the naturalness gap WIDENS to {inter['canon'][0]/(A0_CANON/(2*C_LIGHT)):.0e}-{inter['canon'][1]/(A0_CANON/(2*C_LIGHT)):.0e}x the kernel's own a0/2c (vs {OMEGA_C_LO/(A0_CANON/(2*C_LIGHT)):.0e}x).
      ITS VIRTUE: it INVERTS the paper's own Sec. 5.4 wide-binary falsifier (full AQUAL-strength boost
      at 3-20 kAU instead of 0.0-6.2%), so Gaia DR4 separates the two overlays in opposite directions.
      The pincer is therefore NOT a closed dichotomy -- but no branch of it is a reading of the ACTION.

  COULD THE GATE BE PUT INSIDE THE ACTION INSTEAD?  Not the one obvious way (Sec. 8, scoped): the
      multiplicative embedding K -> K*G maps the gate's pole onto the POSITIVE (acceleration) axis at
      |a| = c omega_c = {C_LIGHT*OMEGA_C_LO:.2e}-{C_LIGHT*OMEGA_C_HI_C:.2e} m/s^2 = {C_LIGHT*OMEGA_C_LO/A0_CANON:.1e}-{C_LIGHT*OMEGA_C_HI_C/A0_CANON:.1e} a0 -- a divergence of the inertial
      dressing at 29.9-33.3 AU (Neptune's orbit is 30.07 AU) for EVERY corner of the committed window --
      and it breaks the upper-half-plane positivity that K alone satisfies (53% of a pole-spanning
      sample).  NOT claimed: that no other embedding exists, or that this is a ghost.  Not load-bearing.

  PLAINLY, AS REQUIRED:  THE SINGLE-POLE GATE MECHANISM IS EXCLUDED AS A READING OF THE WRITTEN ACTION.
  It is not sourced by the kernel (its corner is {OMEGA_C_LO/(A0_CANON/(2*C_LIGHT)):.1e}x the kernel's own a0/2c), it acts on an axis
  where the kernel has unit modulus, and its target lives on the other axis.  Removing it is NOT a
  rescue: the planetary a0/2 tail returns at full strength, 1017x-40357x per planet.  The framework's
  solar-system problem is UNMITIGATED BY THE ACTION AS WRITTEN.  Exactly TWO mitigations survive this
  audit, and both are NEW ASSUMPTIONS with prices now named and quantified:
      (A) a MULTI-POLE frequency overlay (Sec. 4B).  Window non-empty and wider than the paper's, but
          costs a discrete rolloff order, widens the naturalness gap to ~5e7-5e8 x a0/2c, and inverts
          the wide-binary falsifier (testable against Gaia DR4 in the opposite direction).
      (B) an ACCELERATION-dependent crossover (Sec. 6).  Enormously over-adequate if adopted, but the
          action's own kernel provably does not supply one (g(1-K) = a0/2 exactly), so it costs a
          different kernel -- and with it the exact a0-line g_obs^2 - g_bar^2 = a0 g_bar.
  Neither is derived.  Which of the two (if either) is right is a live question, not a closed one.

  SCOPE, held: this bears on the GATE ONLY.  The MOND premise, the a0 = cH_Lambda/Z reframing, the
  galactic RAR (0.108 dex, Upsilon = 0.70), the a0-line, and the BTFR are untouched by every number
  above -- none of them uses omega_c.  Nothing here is a claim that the framework, or any door, is
  closed; the acceleration-crossover route is open and was not attempted.  Both footings carried
  throughout; the central coefficient is footing-stable to {abs(c_alt/c_can-1)*100:.0f}%.
""")
print(RULE)
print("mi_kernel_axis_separation_omegac_2026.py: all checks passed "
      "(|K|=1 on the negative axis symbolically; Box_u diagonal on (u_DC,u_AC) exactly; first-moment "
      "identity and the paper's n>1 mismatch both reproduced; a0/2c branch point matches the paper; "
      "no K-only channel passes the redundancy test; eccentric door shut on all four planets).")
print(RULE)
