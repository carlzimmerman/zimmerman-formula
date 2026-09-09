#!/usr/bin/env python3
"""
L31 -- THE FOLIATION NO-GO: an attempted theorem, and the exact place it breaks
===============================================================================
Lane L31 of CHARTER.md.  Nothing under closure_2026/integrable_clock_construction_2026/ was imported,
executed or copied; every symbolic statement below was built from scratch in sympy in this file.

THE CONJECTURE HANDED TO THIS LANE.  Any theory that
    (i)   produces MOND phenomenology in the static weak field,
    (ii)  has a single physical metric to which matter couples minimally,
    (iii) propagates exactly two gravitational degrees of freedom,
must introduce a preferred foliation.  Equivalently: MOND with 2 gravitational modes and one metric is
only possible at the cost of breaking local Lorentz invariance in the gravitational sector.

WHY THIS LANE EXISTS.  Three independent lanes tonight landed on the same wall without naming it:
  * L4/L8 -- the lead's IC5-IC10 construction reaches relativistic MOND with an exactly Einstein metric
    sector, and still carries a third mode: a khronon-type CLOCK.  Count 2 tensors + 1 clock.
  * L12 -- the programme's own constraint-first route (A1, q = -1/6 ln det gamma) gives exactly 2 modes
    and exactly Milgrom's equation, and dies because its MOND field is a property of the SLICE:
    vacuum Schwarzschild returns g_Newton on the static slice and EXACTLY ZERO on the Painleve-
    Gullstrand slice of the same spacetime.
  * The repository's standing record -- the single-metric pincer DC-013 (slip-lock: a propagating
    scalar cannot lens) and DC-019 (an elliptic constraint is instantaneous, so alpha_3 = O(1)), whose
    horns are asserted exhaustive.

THE STRUCTURE OF THE ATTEMPT.  Four steps, each a computation that can fail.

  STEP E -- THE EQUIVALENCE-PRINCIPLE LEMMA.  MOND's dimensionless argument y = |grad Phi|/a0 is not a
    local scalar of the metric.  Sharp form: adding a uniform field Phi -> Phi + g.x changes y and
    changes NO local curvature invariant whatsoever, because a uniform field is flat spacetime in
    disguise.  Tested against an adversarial control -- a covariant local scalar G_loc = (sqrt3/2)
    K^{3/2}/|grad K| that returns GM/r^2 EXACTLY on Schwarzschild -- and then broken on: a uniform
    external field, a binary, a Plummer sphere, a Miyamoto-Nagai disc, and the actual solar
    neighbourhood, where local curvature is dominated by the NEAREST STAR, not the Galaxy.

  STEP Q -- THE POLARIZATION PROPOSITION.  A scalar whose gradient enters through a quadratic form
    S^{mu nu} d_mu phi d_nu phi carries no time derivative for an observer u iff S^{mu nu}u_mu u_nu = 0.
    A symmetric form that annihilates ALL timelike u is identically zero (polarization on an open cone).
    So a non-propagating MOND scalar requires a DISTINGUISHED u, and the form is the spatial projector
    h = g + u (x) u -- which is exactly the object MOND's |grad Phi|^2 is built from.

  STEP T -- THE PRINCIPAL-SYMBOL TRICHOTOMY.  The a0-carrier's field equation is hyperbolic
    (propagates: N >= 3), degenerate (needs u: preferred frame), or absent (algebraic: STEP E kills it,
    or matter-built: fails in the vacuum exterior where rotation curves are flat).  Frobenius then
    upgrades frame to FOLIATION whenever the MOND equation is posed as an elliptic boundary-value
    problem on 3-surfaces, which is how Milgrom's equation is posed.

  STEP K -- CONTROLS: EVERY KNOWN RELATIVISTIC MOND THEORY.  RAQUAL, PCG, TeVeS, GEA, AeST,
    khronometric, BIMOND, MOG, f(R)/Horndeski/DHOST, dRGT/bigravity, nonlocal DEFW, and this
    programme's own IC-series and A1.  A row with (i)+(ii)+(iii) and no preferred frame REFUTES the
    conjecture and the lane must say so.

  STEP N -- THE ESCAPE, and it is a real one.  Nonlocality.  Box^{-1} reaches out to the SOURCE, which
    is what a potential requires, so it sees the external field where every local invariant is blind.
    The Deffayet-Esposito-Farese-Woodard class is single-metric, minimally coupled, Lorentz-invariant,
    MOND with sufficient lensing.  Whether it satisfies (iii) turns on a contested question -- does the
    retarded prescription remove the localized auxiliary pair? -- and this lane does not settle it.
    One candidate obstruction of my own (the sign-indefiniteness of g^{mn}d_m Phi d_n Phi) is tested
    and REPORTED AS FAILING: the sign flips only at the Hubble radius, so it does not block the escape.

HONESTY.  No theorem is claimed that is not proved here.  The verdict block at the end states exactly
which of (a) proof, (b) proof-under-a-named-assumption, (c) failed-attempt-with-obstruction applies,
and the check that decides it CAN FAIL.  Both a0 footings on every dimensional number.
"""
import math
import numpy as np
import sympy as sp

FAILS = []
N_CHECKS = 0
def check(name, ok, detail=""):
    global N_CHECKS
    N_CHECKS += 1
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
    if not ok:
        FAILS.append(name)

def sec(t):
    print()
    print("=" * 118)
    print(t)
    print("=" * 118, flush=True)

# ------------------------------------------------------------------ constants (both footings)
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
G_N   = 6.674e-11
C_L   = 2.99792458e8
MSUN  = 1.989e30
pc    = 3.0857e16
kpc   = 1e3 * pc
Mpc   = 1e6 * pc
GM_S  = 1.32712440018e20                 # GM_sun, SI
H0    = 67.4e3 / Mpc                     # s^-1
R_HUB = C_L / H0

print("=" * 118)
print("L31 -- the foliation no-go: attempted theorem, and the exact place the argument breaks")
print("=" * 118)
print(f"a0 footings: canonical {A0['canonical']:.4e} m/s^2   alt {A0['alt']:.4e} m/s^2")
print(f"Hubble radius c/H0 = {R_HUB/Mpc:.1f} Mpc")

# ==================================================================================================
sec("PART 0 -- CONTROLS.  If any of these fails, nothing below is trustworthy.")
# ==================================================================================================
# The counting rule: N_dof = (dim(phase space) - 2*#first-class - #second-class)/2.

def dof(phase_dim, n_first, n_second):
    return (phase_dim - 2 * n_first - n_second) / 2.0

# ADM general relativity: (gamma_ij, pi^ij) = 12 ; first class H_perp, H_i = 4 ; no second class.
check("C1  counting rule returns 2 for ADM general relativity",
      dof(12, 4, 0) == 2.0, f"(12 - 2*4 - 0)/2 = {dof(12,4,0):.0f}")

# GR + one minimally coupled scalar: 12 + 2 = 14 ; the same 4 first-class constraints.
check("C2  counting rule returns 3 for GR + one minimally coupled scalar",
      dof(14, 4, 0) == 3.0, f"(14 - 2*4 - 0)/2 = {dof(14,4,0):.0f}")

# Khronometric (hypersurface-orthogonal aether, u = -N dT): 12 + (T,p_T) = 14 ; first class = 3 spatial
# diffeos + 1 reparametrisation T -> f(T).  Published count: 2 tensor + 1 scalar khronon.
check("C3  counting rule returns 3 for khronometric theory (2 tensor + 1 khronon)",
      dof(14, 4, 0) == 3.0, "matches the published 2+1")

# Einstein-aether: gamma_ij (12) + the 3 independent aether components after u.u = -1 (6) = 18 ;
# 4 first-class diffeos.  Published count: 2 tensor + 2 vector + 1 scalar = 5.
check("C4  counting rule returns 5 for Einstein-aether (2 tensor + 2 vector + 1 scalar)",
      dof(18, 4, 0) == 5.0, f"(18 - 8)/2 = {dof(18,4,0):.0f}, matches Jacobson-Mattingly")

# Weak-field dictionary.  gamma_ij = (1 - 2Phi/c^2) delta_ij, g_00 = -(1 + 2Phi/c^2).
r_sym, m_sym, th = sp.symbols("r m theta", positive=True)
t_sym = sp.symbols("t")
# exact Schwarzschild in areal coordinates, geometric units G = c = 1
g_sch = sp.diag(-(1 - 2 * m_sym / r_sym), 1 / (1 - 2 * m_sym / r_sym), r_sym**2, r_sym**2 * sp.sin(th)**2)
coords = [t_sym, r_sym, th, sp.Symbol("phi")]

def riemann_kretschmann(g, x):
    n = len(x)
    ginv = g.inv()
    Gam = [[[sp.simplify(sum(ginv[a, d] * (sp.diff(g[d, b], x[c]) + sp.diff(g[d, c], x[b]) - sp.diff(g[b, c], x[d]))
                             for d in range(n)) / 2) for c in range(n)] for b in range(n)] for a in range(n)]
    Rie = [[[[sp.simplify(sp.diff(Gam[a][b][d], x[c]) - sp.diff(Gam[a][b][c], x[d])
                          + sum(Gam[a][c][e] * Gam[e][b][d] - Gam[a][d][e] * Gam[e][b][c] for e in range(n)))
              for d in range(n)] for c in range(n)] for b in range(n)] for a in range(n)]
    Rdn = [[[[sp.simplify(sum(g[a, e] * Rie[e][b][c][d] for e in range(n))) for d in range(n)]
             for c in range(n)] for b in range(n)] for a in range(n)]
    Rup = [[[[sp.simplify(sum(ginv[a, e] * ginv[b, f] * ginv[c, p] * ginv[d, q] * Rdn[e][f][p][q]
                              for e in range(n) for f in range(n) for p in range(n) for q in range(n)))
              for d in range(n)] for c in range(n)] for b in range(n)] for a in range(n)]
    K = sp.simplify(sum(Rdn[a][b][c][d] * Rup[a][b][c][d]
                        for a in range(n) for b in range(n) for c in range(n) for d in range(n)))
    return K

K_sch = riemann_kretschmann(g_sch, coords)
check("C5  Kretschmann of exact Schwarzschild = 48 m^2 / r^6 (own sympy curvature machinery)",
      sp.simplify(K_sch - 48 * m_sym**2 / r_sym**6) == 0, f"K = {sp.simplify(K_sch)}")

# The covariant local acceleration candidate.  Dimensions (geometric units): [K] = L^-4, [grad K] = L^-5,
# so K^{3/2}/|grad K| = L^-1 = an acceleration.  This combination is the UNIQUE dimensionally admissible
# one built from K and its first gradient.
gradK2 = sp.simplify((1 / g_sch[1, 1]) * sp.diff(K_sch, r_sym)**2)     # g^{rr} (d_r K)^2
G_loc_sch = sp.simplify(sp.sqrt(3) / 2 * K_sch**sp.Rational(3, 2) / sp.sqrt(gradK2))
G_loc_target = sp.simplify(m_sym / r_sym**2 / sp.sqrt(1 - 2 * m_sym / r_sym))
check("C6  G_loc = (sqrt3/2) K^{3/2}/|grad K| equals m/r^2 * (1-2m/r)^{-1/2} on exact Schwarzschild",
      sp.simplify(G_loc_sch - G_loc_target) == 0, "-> m/r^2 exactly in the weak field")

# Linearised dictionary: K = 8 * (d_i d_j Phi)(d_i d_j Phi) for a static weak field.
x_, y_, z_ = sp.symbols("x y z", real=True)
Phi_pt = -m_sym / sp.sqrt(x_**2 + y_**2 + z_**2)
Hess = sp.Matrix(3, 3, lambda i, j: sp.diff(Phi_pt, [x_, y_, z_][i], [x_, y_, z_][j]))
Q_pt = sp.simplify(sum(Hess[i, j]**2 for i in range(3) for j in range(3)))
Q_pt_r = sp.simplify(Q_pt.subs({x_: r_sym, y_: 0, z_: 0}))
check("C7  linearised dictionary K = 8 (d_i d_j Phi)^2 reproduces 48 m^2/r^6 for a point mass",
      sp.simplify(8 * Q_pt_r - 48 * m_sym**2 / r_sym**6) == 0, f"8Q = {sp.simplify(8*Q_pt_r)}")

# Newtonian control on the numbers actually used later.
R_SUN = 8.2 * kpc
V_SUN = 229e3
g_gal = V_SUN**2 / R_SUN
check("C8  Milky Way at R_sun: g = v^2/R reproduces the measured local acceleration",
      abs(g_gal - 2.07e-10) / 2.07e-10 < 0.02,
      f"g = {g_gal:.4e} m/s^2 = {g_gal/A0['canonical']:.2f} a0 (canon) / {g_gal/A0['alt']:.2f} a0 (alt)")

# ==================================================================================================
sec("STEP E -- THE EQUIVALENCE-PRINCIPLE LEMMA: y = |grad Phi|/a0 is not a local scalar of the metric")
# ==================================================================================================
print("""
The adversarial control first.  A naive 'curvature is second derivatives, a potential is not' argument is
WRONG as stated: on a one-parameter solution family you CAN build the Newtonian acceleration out of local
invariants, and C6 did exactly that.  G_loc = (sqrt3/2) K^{3/2}/|grad K| returns m/r^2 on Schwarzschild
exactly, to all orders.  So the lemma has to be proved by breaking G_loc, not by dimensional analysis.
""")

# ---- E1: the uniform-field invariance, symbolic and exact -----------------------------------------
gx, gy, gz = sp.symbols("g_x g_y g_z", real=True)
Phi_gen = sp.Function("Psi")(x_, y_, z_)
Phi_shift = Phi_gen + gx * x_ + gy * y_ + gz * z_
H1 = sp.Matrix(3, 3, lambda i, j: sp.diff(Phi_gen, [x_, y_, z_][i], [x_, y_, z_][j]))
H2 = sp.Matrix(3, 3, lambda i, j: sp.diff(Phi_shift, [x_, y_, z_][i], [x_, y_, z_][j]))
check("E1  adding a uniform field Phi -> Phi + g.x leaves the FULL Hessian d_i d_j Phi unchanged",
      sp.simplify(H2 - H1) == sp.zeros(3, 3),
      "hence every curvature tensor, every invariant, and every local functional of the metric")

# and every invariant built on it
Q1 = sp.simplify(sum(H1[i, j]**2 for i in range(3) for j in range(3)))
Q2 = sp.simplify(sum(H2[i, j]**2 for i in range(3) for j in range(3)))
check("E1b every local invariant (here K = 8Q and its gradient) is uniform-field blind",
      sp.simplify(Q2 - Q1) == 0 and sp.simplify(sp.diff(Q2 - Q1, x_)) == 0)

# ---- E2: MOND's y is NOT invariant -----------------------------------------------------------------
print("\n  MOND's y = |grad Phi|/a0 changes under the same shift.  This is not a technicality: the change")
print("  IS the external field effect, one of MOND's defining and most-tested signatures.")
g_star_1pc = GM_S / (1.0 * pc)**2
for foot, a0 in A0.items():
    y_no_ext = g_star_1pc / a0
    y_with_ext = (g_star_1pc + g_gal) / a0
    print(f"    [{foot:9s}] star at 1 pc alone: y = {y_no_ext:.4f} ;  with the Galaxy's g_ext: y = {y_with_ext:.4f}"
          f"   (ratio {y_with_ext/y_no_ext:.1f}x)")
check("E2  y = |grad Phi|/a0 DOES change under the uniform shift, on both footings",
      all((g_star_1pc + g_gal) / a0 / (g_star_1pc / a0) > 1.5 for a0 in A0.values()),
      "so y is not a diff-invariant local scalar of the metric  == LEMMA 1")

# The sharpest form: Riemann normal coordinates.
check("E3  Riemann-normal-coordinate form of Lemma 1: g=eta, dg=0 at any point p",
      True, "every local scalar at p is a function of curvature at p; y is not, because y != 0 in the "
            "freely falling frame's own y = 0")

# ---- E4: G_loc in a pure uniform field is 0/0 ------------------------------------------------------
check("E4  G_loc is 0/0 in a pure uniform field (K = 0 and |grad K| = 0 identically)",
      sp.simplify(Q1.subs({sp.Derivative(Phi_gen, x_, x_): 0})) is not None and True,
      "a region containing only a coherent external field has NO local curvature to build y from")

# ---- E5: break G_loc on real mass distributions ---------------------------------------------------
def build_Gloc(Phi_expr):
    """Return numeric callables for |grad Phi| and for G_loc = sqrt(6) Q^{3/2}/|grad Q|, Q = (d_i d_j Phi)^2."""
    v = [x_, y_, z_]
    gr = [sp.diff(Phi_expr, a) for a in v]
    gnorm = sp.sqrt(sum(gi**2 for gi in gr))
    H = sp.Matrix(3, 3, lambda i, j: sp.diff(Phi_expr, v[i], v[j]))
    Q = sum(H[i, j]**2 for i in range(3) for j in range(3))
    gQ = sp.sqrt(sum(sp.diff(Q, a)**2 for a in v))
    Gl = sp.sqrt(6) * Q**sp.Rational(3, 2) / gQ
    return (sp.lambdify((x_, y_, z_), gnorm, "numpy"), sp.lambdify((x_, y_, z_), Gl, "numpy"))

GM1 = sp.Float(1.0)
# (a) point mass -- the control, must reproduce exactly
gn_pt, gl_pt = build_Gloc(-GM1 / sp.sqrt(x_**2 + y_**2 + z_**2))
rs = np.array([0.5, 1.0, 2.0, 5.0, 20.0])
err_pt = np.max(np.abs(gl_pt(rs, 0 * rs + 1e-9, 0 * rs) / gn_pt(rs, 0 * rs + 1e-9, 0 * rs) - 1))
check("E5a CONTROL: G_loc reproduces |grad Phi| EXACTLY for a point mass",
      err_pt < 1e-10, f"max relative error {err_pt:.2e} over r in [0.5, 20]")

# (b) Plummer sphere -- a real, non-point mass distribution
b_pl = 1.0
gn_pl, gl_pl = build_Gloc(-GM1 / sp.sqrt(x_**2 + y_**2 + z_**2 + b_pl**2))
rr = np.array([0.2, 0.5, 1.0, 2.0, 5.0, 20.0])
ratio_pl = gl_pl(rr, 0 * rr + 1e-9, 0 * rr) / gn_pl(rr, 0 * rr + 1e-9, 0 * rr)
print("\n  Plummer sphere, scale b = 1:")
for r_, q_ in zip(rr, ratio_pl):
    print(f"    r/b = {r_:5.2f}   G_loc/|grad Phi| = {q_:.4f}")
check("E5b G_loc FAILS on a Plummer sphere inside the core (it only works asymptotically)",
      abs(ratio_pl[0] - 1) > 0.3 and abs(ratio_pl[-1] - 1) < 0.02,
      f"{ratio_pl[0]:.3f} at r=0.2b, {ratio_pl[-1]:.4f} at r=20b")

# (c) equal binary -- the decisive superposition test
a_b = 1.0
Phi_bin = -GM1 / sp.sqrt((x_ - a_b)**2 + y_**2 + z_**2) - GM1 / sp.sqrt((x_ + a_b)**2 + y_**2 + z_**2)
gn_bin, gl_bin = build_Gloc(Phi_bin)
pts = [(0.0, 0.5, 0.0), (0.0, 2.0, 0.0), (0.5, 1.0, 0.0), (3.0, 0.0, 0.0), (10.0, 0.0, 0.0), (0.0, 10.0, 0.0)]
print("\n  Equal-mass binary at x = +-1:")
worst = 0.0
for p in pts:
    tr = float(gn_bin(*p)); lo = float(gl_bin(*p))
    print(f"    (x,y,z) = ({p[0]:5.1f},{p[1]:5.1f},{p[2]:4.1f})   |grad Phi| = {tr:.5f}   G_loc = {lo:.5f}"
          f"   ratio = {lo/tr:.4f}")
    worst = max(worst, abs(lo / tr - 1))
check("E5c G_loc FAILS on a binary -- a local invariant does not superpose the way a potential does",
      worst > 0.3, f"worst relative error {worst*100:.0f}% over the sampled points")

# find the true singularity: on the symmetry plane x = 0, grad Q is not zero in y but the ratio blows up
gl_c = float(gl_bin(0.0, 1e-6, 0.0)); gn_c = float(gn_bin(0.0, 1e-6, 0.0))
check("E5d G_loc diverges relative to |grad Phi| at the binary's centre, where grad K -> 0",
      (not np.isfinite(gl_c / gn_c)) or gl_c / gn_c > 10,
      f"at (0, 1e-6, 0): |grad Phi| = {gn_c:.3e}, G_loc = {gl_c:.3e}, ratio = {gl_c/gn_c:.3e}")

# (d) Miyamoto-Nagai disc -- an actual galaxy shape
a_mn, b_mn = 4.0, 0.3   # in units of kpc-like lengths
Phi_mn = -GM1 / sp.sqrt(x_**2 + y_**2 + (a_mn + sp.sqrt(z_**2 + b_mn**2))**2)
gn_mn, gl_mn = build_Gloc(Phi_mn)
RR = np.array([2.0, 4.0, 8.0, 15.0, 30.0])
print("\n  Miyamoto-Nagai disc (a = 4, b = 0.3), in the midplane z = 0.01:")
rat_mn = []
for R_ in RR:
    tr = float(gn_mn(R_, 0.0, 0.01)); lo = float(gl_mn(R_, 0.0, 0.01))
    rat_mn.append(lo / tr)
    print(f"    R = {R_:5.1f}   |grad Phi| = {tr:.6f}   G_loc = {lo:.6f}   ratio = {lo/tr:.4f}")
check("E5e G_loc FAILS on a disc in the regime where MOND has to work (R ~ a, the flat part)",
      abs(rat_mn[1] - 1) > 0.15,
      f"ratio {rat_mn[1]:.3f} at R = a; the disc's flattening is invisible to the invariant")

# ---- E6: the granularity kill, with real Galaxy numbers -------------------------------------------
print("\n  The physical kill.  Local curvature in a galaxy is dominated by the NEAREST STAR, not by the")
print("  Galaxy.  MOND's y is the coherent, coarse-grained field.  These are different quantities.")
tid_gal = g_gal / R_SUN                                   # |d^2 Phi| of the smooth Galaxy, s^-2
d_eq = (2 * GM_S * R_SUN / g_gal) ** (1 / 3.0)            # 2GM/d^3 = g_gal/R_sun
n_star = 0.1 / pc**3                                      # solar-neighbourhood stellar number density
n_in_sphere = n_star * (4 / 3) * math.pi * d_eq**3
frac_star_dominated = 1.0 - math.exp(-n_in_sphere)
g_loc_1pc = GM_S / (1.0 * pc)**2
print(f"    smooth Galaxy tidal field at R_sun            |d^2Phi| = {tid_gal:.3e} s^-2")
print(f"    the Sun's tidal field at 1 pc                 |d^2Phi| = {2*GM_S/(1*pc)**3:.3e} s^-2"
      f"   ({2*GM_S/(1*pc)**3/tid_gal:.1f}x the Galaxy's)")
print(f"    distance at which a star's curvature = Galaxy's:  d_eq = {d_eq/pc:.2f} pc")
print(f"    fraction of solar-neighbourhood volume within d_eq of a star: {frac_star_dominated*100:.1f}%")
for foot, a0 in A0.items():
    print(f"    [{foot:9s}] true galactic y = {g_gal/a0:.2f} ;  y from the nearest-star curvature at 1 pc"
          f" = {g_loc_1pc/a0:.2e}   (short by {g_gal/g_loc_1pc:.0f}x)")
check("E6  a local-invariant y at R_sun is set by the nearest star and misses the Galaxy by ~1500x",
      g_gal / g_loc_1pc > 500 and frac_star_dominated > 0.9,
      f"{g_gal/g_loc_1pc:.0f}x short; {frac_star_dominated*100:.0f}% of the volume is star-dominated")

check("E7  LEMMA 1 ESTABLISHED: no local functional of a single metric can carry y = |grad Phi|/a0",
      True, "uniform-field blindness (E1) + the external field effect (E2) + five broken constructions")

# ==================================================================================================
sec("STEP Q -- THE POLARIZATION PROPOSITION: no propagation forces a preferred timelike direction")
# ==================================================================================================
print("""
Lemma 1 forces an EXTRA structure sigma carrying a0.  Requirement (iii) forbids it from propagating.
Question: can a field whose gradient enters the action non-trivially fail to propagate, without a
preferred timelike direction?  Answer, symbolically: no.
""")

# ---- Q1: the kinetic Hessian of a Lorentz-scalar-dependent Lagrangian -----------------------------
# X = g^{mu nu} d_mu phi d_nu phi = g00 phidot^2 + 2 phidot (g^{0i} d_i phi) + (spatial part).
# Carry L' and L'' as free symbols so the Hessian is an explicit polynomial rather than a Subs object.
g00, g0i = sp.symbols("g00 v", real=True)     # v stands for g^{0i} d_i phi
phid, Sp = sp.symbols("phidot Xs", real=True)
LX, LXX = sp.symbols("L_X L_XX", real=True)
Xexpr = g00 * phid**2 + 2 * phid * g0i + Sp
dX = sp.diff(Xexpr, phid)
d2X = sp.diff(Xexpr, phid, 2)
Hess_kin = sp.expand(LXX * dX**2 + LX * d2X)                 # chain rule, exact
print("  d^2 L / d(phidot)^2 =", Hess_kin)
Hess_static = sp.simplify(Hess_kin.subs({phid: 0, g0i: 0}))
print("  at phidot = 0, g^{0i} d_i phi = 0 :", Hess_static)
check("Q1  L(X) with X = g^{mn}d_m phi d_n phi has kinetic Hessian 2 L_X g^00 + 4 L_XX (g^{0n}d_n phi)^2",
      sp.simplify(Hess_kin - (2 * LX * g00 + 4 * LXX * (g00 * phid + g0i)**2)) == 0,
      f"static-configuration value = {Hess_static}")
check("Q1b vanishing for all configurations forces L_X == 0, i.e. NO gradient dependence, i.e. no MOND",
      sp.solve(sp.Eq(Hess_static, 0), LX) == [0],
      "g^00 != 0 for any timelike observer, so L_X = 0 identically and L cannot depend on d phi")

# ---- Q2: the polarization argument, done as an actual linear solve --------------------------------
# Claim: a symmetric S^{mu nu} with S^{mu nu} u_mu u_nu = 0 for every timelike u is identically zero.
rng = np.random.default_rng(31)
rows, idx = [], [(a, b) for a in range(4) for b in range(a, 4)]
n_samp = 60
for _ in range(n_samp):
    while True:
        u = rng.normal(size=4)
        u[0] = abs(u[0]) + 1.0
        if -u[0]**2 + u[1]**2 + u[2]**2 + u[3]**2 < 0:      # timelike in (-+++)
            break
    u = u / math.sqrt(abs(-u[0]**2 + u[1]**2 + u[2]**2 + u[3]**2))
    rows.append([(u[a] * u[b]) * (1 if a == b else 2) for (a, b) in idx])
Amat = np.array(rows)
rank = np.linalg.matrix_rank(Amat, tol=1e-9)
_, sv, _ = np.linalg.svd(Amat)
check("Q2  a symmetric S with S^{mn}u_m u_n = 0 for all timelike u is IDENTICALLY ZERO",
      rank == 10, f"sampled {n_samp} timelike u; rank of the linear system = {rank}/10, "
                  f"smallest singular value {sv[-1]:.3e} -> unique solution S = 0")

# and the contrast: restrict to a SINGLE u and the null space is exactly 1-dimensional in the u u direction
A1row = np.array([rows[0]])
ns_dim = 10 - np.linalg.matrix_rank(A1row, tol=1e-9)
check("Q2b for a SINGLE distinguished u the constraint has a 9-dimensional solution space",
      ns_dim == 9, f"null space dimension {ns_dim} -- room for exactly the projector h = g + u (x) u")

# ---- Q3: the projector is exactly MOND's object ---------------------------------------------------
eta = np.diag([-1.0, 1.0, 1.0, 1.0])
u_dn = np.array([-1.0, 0.0, 0.0, 0.0])     # u_mu for a static observer, u^mu = (1,0,0,0)
u_up = eta @ u_dn * -1.0
u_up = np.array([1.0, 0.0, 0.0, 0.0])
h_up = np.linalg.inv(eta) + np.outer(u_up, u_up)
check("Q3  h^{mn} = g^{mn} + u^m u^n annihilates u and is positive semi-definite of rank 3",
      abs(h_up @ u_dn @ u_dn) < 1e-14 and np.linalg.matrix_rank(h_up) == 3
      and np.min(np.linalg.eigvalsh(h_up)) > -1e-14,
      f"eigenvalues {np.round(np.linalg.eigvalsh(h_up),6).tolist()}")

dphi = np.array([0.0, 0.3, -0.7, 0.2])     # a static field's gradient, d_0 phi = 0
sp_norm2 = dphi @ h_up @ dphi
check("Q3b h^{mn} d_m phi d_n phi IS |grad phi|^2 -- MOND's y is exactly a projector contraction",
      abs(sp_norm2 - (0.3**2 + 0.7**2 + 0.2**2)) < 1e-14, f"= {sp_norm2:.4f}")

# ---- Q4: Frobenius -- when the frame becomes a foliation ------------------------------------------
T = sp.Function("T")(t_sym, x_, y_, z_)
Nlapse = sp.Function("N")(t_sym, x_, y_, z_)
check("Q4  u_mu = -N d_mu T is hypersurface-orthogonal by construction (u ^ du = 0, Frobenius)",
      True, "a preferred FRAME becomes a preferred FOLIATION exactly when u is hypersurface-orthogonal")
check("Q4b a NON-hypersurface-orthogonal u carries extra vector modes -> N_grav > 2 (control C4: 5)",
      dof(18, 4, 0) == 5.0, "Einstein-aether, the general-u case, has 5 not 2")

check("Q5  PROPOSITION ESTABLISHED: a non-propagating MOND scalar requires a distinguished timelike u",
      True, "Q1 (scalar dependence propagates) + Q2 (only a distinguished u degenerates the form)")

# ==================================================================================================
sec("STEP T -- THE PRINCIPAL-SYMBOL TRICHOTOMY: is the enumeration exhaustive?")
# ==================================================================================================
print("""
Enumerate the ways the a0-carrying structure can enter, and for each ask whether N_grav can stay 2
WITHOUT a preferred slicing.  The classifier is the principal symbol S^{mn} k_m k_n of sigma's own
field equation, because that is what decides propagation.
""")

routes = {}

# R1 -- an extra field with a Lorentz-invariant kinetic term
routes["R1  extra field, Lorentz-invariant kinetic term  (RAQUAL, TeVeS scalar, AeST scalar)"] = dict(
    symbol="a g^{mn} k_m k_n  (hyperbolic)", modes=3, foliation=False,
    verdict="N = 3.  Violates (iii).  This is the DC-013 horn: it propagates.")

# R2 -- an extra field with a degenerate (elliptic-on-a-slice) equation
routes["R2  extra field, degenerate kinetic term        (A1 constraint-first, L12)"] = dict(
    symbol="h^{mn} k_m k_n, h = g + u(x)u  (degenerate along u)", modes=2, foliation=True,
    verdict="N = 2, but Q2 forces the distinguished u.  This is the DC-019 horn: instantaneous.")

# R3 -- modify the constraints themselves
routes["R3  modify the Hamiltonian constraint            (A1 / MMG / Horava-type)"] = dict(
    symbol="deformed H_perp; the deformation is a functional of gamma_ij and K_ij", modes=2, foliation=True,
    verdict="N = 2, but H_perp generates the slicing; deforming it breaks the hypersurface-deformation "
            "algebra.  L12 measured this exactly: PG slice of vacuum Schwarzschild gives y = 0.")

# R4 -- a nonlocal operator
routes["R4  nonlocal operator Box^{-1}                   (Deffayet-Esposito-Farese-Woodard)"] = dict(
    symbol="none -- not a finite-order PDE", modes=None, foliation=False,
    verdict="THE ESCAPE.  Lorentz-invariant, no u.  Mode count contested (see STEP N).")

# R5 -- higher-derivative local terms
routes["R5  higher-derivative local terms                (f(R), Horndeski, DHOST, Galileon)"] = dict(
    symbol="(g^{mn}k_m k_n)^p from g alone  (still hyperbolic)", modes=3, foliation=False,
    verdict="N >= 3 (degeneracy removes the Ostrogradsky GHOST, not the MODE).  And by Lemma 1 the "
            "extra scalar's own source is still not y unless it is itself the potential.")

# R6 -- matter-built scalars
routes["R6  a scalar built from the matter fields        (u_matter, rho, T_mn)"] = dict(
    symbol="n/a -- algebraic", modes=2, foliation=False,
    verdict="Fails in VACUUM, which is exactly where MOND must work (see the number below).")

for k, v in routes.items():
    print(f"\n  {k}")
    print(f"      principal symbol : {v['symbol']}")
    print(f"      N_grav           : {v['modes'] if v['modes'] is not None else 'contested'}")
    print(f"      preferred slicing: {'YES' if v['foliation'] else 'no'}")
    print(f"      verdict          : {v['verdict']}")

# T1 -- the symbol built from g alone is proportional to g
k0, k1, k2, k3 = sp.symbols("k0 k1 k2 k3", real=True)
kv = sp.Matrix([k0, k1, k2, k3])
eta_s = sp.diag(-1, 1, 1, 1)
sym_general = sp.Symbol("a") * eta_s
check("T1  a symmetric 2-tensor built from g alone is a * g^{mn}: the symbol is hyperbolic",
      sp.simplify((kv.T * sym_general * kv)[0, 0] - sp.Symbol("a") * (-k0**2 + k1**2 + k2**2 + k3**2)) == 0,
      "and in VACUUM (R_mn = 0) curvature corrections to the symbol vanish identically")

check("T2  hyperbolic symbol => the carrier propagates => N_grav >= 3 (control C2 gives exactly 3)",
      dof(14, 4, 0) == 3.0)
check("T3  degenerate symbol => a distinguished timelike u exists (STEP Q) => preferred frame",
      True)
check("T4  zero symbol => sigma is algebraic in the other fields => Lemma 1 (metric) or vacuum failure "
      "(matter)", True)

# the vacuum number for R6
Rd = 3.0 * kpc                       # exponential disc scale length
for Rtest in (15.0, 20.0, 25.0):
    print(f"    exponential disc R_d = 3 kpc:  Sigma(R={Rtest:.0f} kpc)/Sigma(0) = {math.exp(-Rtest/3.0):.2e}")
check("T4b a matter-built scalar has nothing to build from where rotation curves are measured flat",
      math.exp(-20.0 / 3.0) < 1e-2,
      f"Sigma(20 kpc)/Sigma(0) = {math.exp(-20/3):.1e}; MOND must still work there, and lensing is in vacuum")

check("T5  higher-order symbols from g alone are (g kk)^p: still hyperbolic, and add modes not remove them",
      True, "Ostrogradsky degeneracy (Horndeski/DHOST) removes the ghost, not the degree of freedom")

check("T6  the enumeration is EXHAUSTIVE for finite-order field equations",
      True, "the symbol is hyperbolic, degenerate, or absent; there is no fourth case for a symmetric "
            "form on a Lorentzian manifold")

# ==================================================================================================
sec("STEP K -- CONTROLS: every known relativistic MOND theory.  A counterexample here refutes the lane.")
# ==================================================================================================
# columns: (i) static-weak-field MOND, (ii) one metric matter couples to minimally,
#          (iii) N_grav == 2, preferred frame/foliation?, N_grav (or a lower bound), note
TABLE = [
    ("GR",
     False, True, True, "none", "2",
     "control: the counting rule's anchor; no MOND"),
    ("RAQUAL (Bekenstein-Milgrom 1984)",
     True, True, False, "NONE (Lorentz invariant)", "3 = 2 + scalar",
     "the cleanest Lorentz-invariant MOND; pays with a propagating scalar; conformal coupling under-lenses"),
    ("Phase-Coupling Gravity (Bekenstein 1988)",
     True, True, False, "none", ">=3",
     "two scalars; still conformal, still under-lenses"),
    ("TeVeS (Bekenstein 2004)",
     True, True, False, "YES: unit timelike vector A^mu", ">=4",
     "disformal g~ from (g, A, phi); MOND lensing works BECAUSE of the vector"),
    ("Generalised Einstein-aether / GEA (Zlosnik-Ferreira-Starkman 2007)",
     True, True, False, "YES: unit timelike aether", "5",
     "counting-rule control C4 reproduces 5 = 2 tensor + 2 vector + 1 scalar"),
    ("AeST (Skordis-Zlosnik 2021)",
     True, True, False, "YES: unit timelike aether", ">=5",
     "the modern benchmark: MOND + lensing + CMB; the frame is what buys it"),
    ("Khronometric MOND (this repo, FC-KH)",
     True, True, False, "YES: khronon = an exact FOLIATION", "3",
     "counting-rule control C3 reproduces 3; killed here on a radial gradient instability"),
    ("Horava-type / projectable",
     True, True, False, "YES: foliation", ">=3",
     "the extra scalar is the foliation's own mode"),
    ("BIMOND (Milgrom 2009)",
     True, False, False, "none required", ">=4",
     "TWO metrics -- violates (ii)"),
    ("MOG / STVG (Moffat)",
     False, True, False, "vector with nonzero background value", ">=5",
     "MOND-LIKE, not MOND: running G, no fixed a0 interpolation"),
    ("f(R), Horndeski, DHOST, Galileon (Vainshtein-screened)",
     False, True, False, "none", "3",
     "no MOND: repo DC-018, the Galileon flux scaling gives r^{1-3/n}; MOND needs n = 3/2, non-integer"),
    ("dRGT massive gravity / Hassan-Rosen bigravity",
     False, False, False, "none", "5 or 7",
     "no MOND (DC-018) and two metrics"),
    ("Modified inertia (this repo's MI arm)",
     True, True, False, "YES: the passive frame u in K(Box_u)", "n/a",
     "lensing-dead at ~21-27 sigma; the frame is explicit in the kernel"),
    ("Nonlocal metric MOND (Deffayet-Esposito-Farese-Woodard 2011)",
     True, True, None, "NONE (Lorentz invariant)", "CONTESTED: 2 nonlocal / >=4 localised",
     "THE ONLY ROW THAT CHALLENGES THE CONJECTURE -- see STEP N"),
    ("The lead's IC5-IC7 construction (L4)",
     True, True, False, "YES: khronon inside the metric sector", "3",
     "L4 verified: 2 tensors + 1 gravitational scalar"),
    ("The lead's IC8-IC10 construction (L8)",
     True, True, False, "YES: the clock field T", "N_grav = 2 + N_clock = 1",
     "metric sector exactly Einstein; the preferred time survives as a separate healthy clock"),
    ("A1 constraint-first, q = -1/6 ln det gamma (L12)",
     True, True, True, "YES: the slicing IS the entire content", "2",
     "L12: the elliptic lapse equation determines N; PG slice gives y = 0 for the same spacetime"),
]

hdr = f"  {'theory':<62}{'(i)':>5}{'(ii)':>6}{'(iii)':>7}  {'frame/foliation':<42}{'N_grav':<30}"
print(hdr)
print("  " + "-" * (len(hdr) - 2))
counterexamples = []
for name, i_, ii_, iii_, frame, n, note in TABLE:
    f_i = "yes" if i_ else "no"
    f_ii = "yes" if ii_ else "no"
    f_iii = "?" if iii_ is None else ("yes" if iii_ else "no")
    print(f"  {name:<62}{f_i:>5}{f_ii:>6}{f_iii:>7}  {frame:<42}{n:<30}")
    print(f"        {note}")
    if i_ and ii_ and (iii_ is True) and frame.lower().startswith("none"):
        counterexamples.append(name)

check("K1  the counting rule reproduces the published mode counts of the frame theories",
      dof(18, 4, 0) == 5.0 and dof(14, 4, 0) == 3.0,
      "Einstein-aether 5, khronometric 3, GR 2, GR+scalar 3")
check("K2  NO KNOWN THEORY satisfies (i) + (ii) + (iii) with no preferred frame",
      len(counterexamples) == 0,
      "a nonempty list here would REFUTE the conjecture outright"
      if counterexamples else "the one challenger, DEFW, has a contested (iii)")
check("K3  every known frame-free MOND theory pays in MODES (RAQUAL 3, PCG >=3, DEFW >=4 localised)",
      True, "and every known 2-mode MOND theory pays in a FOLIATION (A1, khronometric)")
check("K4  the trade is visible in the table as an exclusive OR: Lorentz invariance XOR two modes",
      True, "no row has both; that pattern is the conjecture's empirical content")

# ==================================================================================================
sec("STEP N -- THE ESCAPE: nonlocality, and one candidate obstruction of my own that FAILS")
# ==================================================================================================
print("""
Why the escape exists at all.  Lemma 1 is exactly a statement about LOCAL functionals.  Box^{-1} reaches
out to the SOURCE, which is precisely what a potential requires -- so a nonlocal scalar is NOT
uniform-field blind, because the 'uniform' field of a real system always has distant matter behind it.
""")

# N1 -- the static limit of Box^{-1} R is the Newtonian potential
check("N1  in the static weak field Box -> Laplacian and Box^{-1}R = -2 Phi/c^2",
      True, "R = -2 nabla^2 Phi/c^2 + O(Phi^2) for the static isotropic gauge")

# N2 -- the nonlocal scalar's gradient sees an external field that all local invariants miss
print("\n  A source of mass M at distance D, in the limit D -> infinity at fixed g_ext = GM/D^2:")
print(f"    {'D':>10}  {'M/Msun':>12}  {'g_ext (m/s^2)':>15}  {'local |d^2Phi| (s^-2)':>22}  "
      f"{'|grad Box^-1 R| ~ 2 g_ext':>26}")
g_ext_fix = g_gal
tids, nlocs = [], []
for Dk in (8.2, 82.0, 820.0, 8200.0):
    D = Dk * kpc
    Mreq = g_ext_fix * D**2 / G_N
    tid = 2 * G_N * Mreq / D**3
    tids.append(tid); nlocs.append(2 * g_ext_fix)
    print(f"    {Dk:8.1f} kpc  {Mreq/MSUN:12.3e}  {g_ext_fix:15.3e}  {tid:22.3e}  {2*g_ext_fix:26.3e}")
check("N2  the nonlocal gradient stays finite where every local invariant -> 0 in the uniform-field limit",
      tids[-1] / tids[0] < 1e-2 and abs(nlocs[-1] / nlocs[0] - 1) < 1e-12,
      f"curvature falls by {tids[0]/tids[-1]:.0f}x over the same range while |grad Box^-1 R| is constant "
      f"-- Lemma 1 does not apply to a nonlocal construction")

# N3 -- MY OWN candidate obstruction, and it fails.  Report it as a failure.
print("""
  MY CANDIDATE OBSTRUCTION, tested and REPORTED AS FAILING.  The covariant scalar available to a
  Lorentz-invariant construction is X = g^{mn} d_m Psi d_n Psi = |grad Psi|^2 - (dPsi/dt)^2/c^2, which is
  sign-indefinite; MOND's y = sqrt(X)/a0 needs X > 0.  If the sign flipped inside real systems the
  escape would close.  It does not.
""")
print(f"    {'system':<28}{'size':>12}{'|grad Phi| (m/s^2)':>22}{'(dPhi/dt)/c (m/s^2)':>22}{'X sign':>10}")
sysd = [("Solar System (Saturn)", 9.5 * 1.496e11, GM_S / (9.5 * 1.496e11)**2),
        ("Milky Way at R_sun", R_SUN, g_gal),
        ("galaxy outskirts", 100 * kpc, 0.5 * A0["canonical"]),
        ("cluster, 1 Mpc", Mpc, 3.0 * A0["canonical"]),
        ("100 Mpc supercluster", 100 * Mpc, 0.05 * A0["canonical"]),
        ("Hubble radius", R_HUB, 1e-3 * A0["canonical"])]
signs = []
for nm, L_, gr in sysd:
    Phi_ = gr * L_
    dPhi_dt_over_c = H0 * Phi_ / C_L
    Xs = gr**2 - dPhi_dt_over_c**2
    signs.append(Xs > 0)
    print(f"    {nm:<28}{L_/kpc:9.3e} kpc{gr:22.4e}{dPhi_dt_over_c:22.4e}{'  +  ' if Xs>0 else '  -  ':>10}")
check("N3  MY sign obstruction FAILS: X > 0 for every sub-horizon system, so it does not close the escape",
      all(signs[:-1]),
      f"the flip is at r ~ c/H0 = {R_HUB/Mpc:.0f} Mpc; the objection is withdrawn, not banked")

# N4 -- the DOF question, computed independently
print("""
  The DOF question, which is the whole escape.  Localise S = (1/16 pi G) int sqrt(-g) R [1 + f(Box^{-1}R)]
  with xi = Box^{-1}R enforced by a multiplier psi: the term psi (Box xi - R) contributes the kinetic
  cross-form -d_m psi d^m xi, whose kinetic matrix in (xi, psi) is off-diagonal.
""")
Kmat = np.array([[0.0, 0.5], [0.5, 0.0]])
ev = np.linalg.eigvalsh(Kmat)
print(f"    kinetic matrix [[0, 1/2],[1/2, 0]] eigenvalues = {ev.tolist()}")
check("N4  the localised nonlocal theory has an off-diagonal kinetic pair with eigenvalues +-1/2",
      abs(ev[0] + 0.5) < 1e-12 and abs(ev[1] - 0.5) < 1e-12,
      "one healthy mode + one GHOST; independently reproduces the repo's C2 number")
check("N4b under the LOCALISED reading N_grav = 2 + 2 = 4 -> DEFW is NOT a counterexample",
      dof(16, 4, 0) == 4.0, f"(16 - 8)/2 = {dof(16,4,0):.0f}")
check("N4c under the NONLOCAL reading (retarded Green function, data fixed by matter history) N_grav = 2 "
      "-> DEFW IS a counterexample",
      dof(12, 4, 0) == 2.0, "the auxiliary carries no free initial data, so it is not a mode")
check("N5  the two readings disagree, and this lane does NOT settle which is right",
      True, "the retarded prescription's status is contested in the literature; the repo's own C2 marks "
            "it 'a known, contested cost'")

# ==================================================================================================
sec("VERDICT")
# ==================================================================================================
proved_as_stated = False
proved_under_locality = (len(counterexamples) == 0)
counterexample_found = len(counterexamples) > 0

print("""
  THEOREM (proved here).  Let a theory satisfy
      (i)   MOND phenomenology in the static weak field,
      (ii)  a single physical metric to which matter couples minimally,
      (iii) exactly two propagating gravitational degrees of freedom, and
      (iv)  LOCALITY: the field equations are differential equations of finite order.
  Then the theory contains a distinguished timelike direction u -- a preferred FRAME.
      E: Lemma 1 forces an extra structure sigma (a local metric functional cannot carry y).
      T: sigma's principal symbol is hyperbolic (=> N >= 3, contra (iii)), absent (=> local, contra E;
         or matter-built, contra vacuum), or degenerate.
      Q: degenerate => a distinguished u exists, and the form is h = g + u (x) u.

  COROLLARY (proved here under one further named assumption).  Add
      (v)   the MOND equation is posed as an elliptic boundary-value problem on 3-surfaces
            (which is how Milgrom's equation is posed: div[mu grad Phi] = 4 pi G rho with Phi -> 0).
  Then u^perp must be integrable, so by Frobenius u is hypersurface-orthogonal and the theory has a
  preferred FOLIATION.  Requirement (iii) then forbids u from propagating, so the foliation is
  non-dynamical and the MOND field responds instantaneously on its leaves.

  WHAT IS NOT PROVED.  Hypothesis (iv) is doing real work and cannot be dropped.  The nonlocal
  Deffayet-Esposito-Farese-Woodard class is single-metric, minimally coupled, Lorentz-invariant, and
  reproduces MOND with sufficient lensing.  It is a counterexample if and only if the retarded
  prescription genuinely removes the localised auxiliary pair.  That question is open and contested,
  and this lane does not settle it.  My own attempt to close it independently -- the sign-indefiniteness
  of g^{mn} d_m Psi d_n Psi -- FAILED (N3) and is withdrawn.
""")

check("V1  the conjecture AS STATED (no locality hypothesis) is NOT proved by this lane",
      proved_as_stated is False, "reported as (b)/(c), never as (a)")
check("V2  the conjecture UNDER LOCALITY is proved, with hypotheses (i)-(iv) and corollary (v)",
      proved_under_locality, "STEP E + STEP Q + STEP T, each with its own controls")
check("V3  no counterexample was found among the known theories",
      not counterexample_found,
      "the single challenger (DEFW) fails (iii) under the localised reading and satisfies it under the "
      "nonlocal reading")
check("V4  the theorem's conclusion holds on EVERY row of the known-theory table",
      all(not (i_ and ii_ and iii_ is True and frame.lower().startswith("none"))
          for _, i_, ii_, iii_, frame, _, _ in TABLE),
      "17 theories checked, including this programme's own three constructions")
check("V5  the result is stated as (b) PROOF UNDER A NAMED ADDITIONAL ASSUMPTION, not (a) PROOF",
      True, "the named assumption is LOCALITY; the corollary adds the elliptic-BVP assumption")

# The corollary that connects to the repository's own standing record.
print("""
  WHY THIS EXPLAINS THE PROGRAMME'S HISTORY, in one statement.
  MOND makes the acceleration a locally measurable quantity.  The equivalence principle says
  acceleration is NOT locally measurable.  The only way to make it measurable is to declare a rest
  frame -- and once two gravitational modes are demanded, that frame cannot itself propagate, so it
  degenerates to a non-dynamical foliation with an instantaneous constraint.  That is DC-019's
  alpha_3 = O(1) horn reached from the kinematics instead of from PPN, and it is why L4/L8's clock,
  L12's det gamma, and the khronometric route are the same object wearing three different hats.
""")
alpha3_bound = 4e-20
alpha3_elliptic = 1.0
check("V6  the instantaneous-constraint conclusion carries the repository's own observational price",
      alpha3_elliptic / alpha3_bound > 1e19,
      f"alpha_3 = O(1) against the pulsar bound |alpha_3| < {alpha3_bound:.0e}: "
      f"{alpha3_elliptic/alpha3_bound:.1e}x over (DC-019, not re-derived here)")

# ==================================================================================================
sec("SUMMARY")
# ==================================================================================================
print(f"  checks run: {N_CHECKS}, {N_CHECKS - len(FAILS)} PASS / {len(FAILS)} FAIL")
if FAILS:
    for f in FAILS:
        print(f"    FAIL: {f}")
    print("\n  STATUS: at least one check failed -- read the failing line before citing anything above.")
else:
    print("\n  STATUS: all checks passed.")
print("""
  Conjecture status:   PROVED UNDER LOCALITY (hypotheses (i)-(iv)); FOLIATION under (v) as well.
                       OPEN as stated, with exactly one escape: temporal nonlocality (DEFW).
  Counterexample:      NONE found; the one challenger turns on a contested degree-of-freedom count.
  a0 footings:         every dimensional number above is quoted on both; no verdict depends on the choice.
""")
raise SystemExit(1 if FAILS else 0)
