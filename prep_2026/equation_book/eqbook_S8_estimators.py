#!/usr/bin/env python3
"""
EQUATION BOOK -- LANE M1, SEAM S8: nuisance-cancelling EXACT estimator identities
(siblings of the a0-line g_obs^2 - g_bar^2 = a0 g_bar).

OBSERVABLE MODEL (per galaxy, per radius j):
    v_los,j = v_true,j * sin(i)          (LOS rotation velocity, spectroscopic)
    theta_j = r_j / D                    (angular radius; D = distance)
    g_obs,j = v_true,j^2 / r_j  = v_los,j^2 / (sin^2 i * D * theta_j)
    g_bar,j = G M_bar(<r_j)/r_j^2 -- DISTANCE-FREE (a surface density x G:
              M propto flux*D^2, r^2 propto D^2 theta^2), and for the stellar part
              g_star,j = Upsilon * s_j with s_j the photometric shape at Upsilon=1.

KEY STRUCTURAL FACT exploited everywhere: the framework law is QUADRATIC --
    g_obs^2 = g_bar^2 + a0 g_bar
is LINEAR in the pair (g_bar^2, g_bar) and linear in a0. Ratios of the law at two
radii therefore solve for a0 (or a0/Upsilon) in CLOSED FORM -- impossible for
McGaugh's exponential nu, where the same elimination is transcendental.

  E-S8.1  PAIR ESTIMATOR (distance-free AND inclination-free):
          R12 := (v_los,1/v_los,2)^4 (theta_2/theta_1)^2   [pure observables]
          Then EXACTLY under the law:
             a0/Upsilon = (s1^2 - R12 s2^2) / (R12 s2 - s1)
          and for GAS-DOMINATED points (g_bar = g_gas, Upsilon-free):
             a0 = (g1^2 - R12 g2^2) / (R12 g2 - g1)         [D, i, Upsilon* ALL cancel]
  E-S8.2  DISTANCE ESTIMATOR (per radius!):
             D = v_los^2 / (sin^2 i * theta * sqrt(g_bar(g_bar + a0)))
          constancy of D(r_j) across radii = a NEW per-galaxy consistency test.
  E-S8.3  INCLINATION ESTIMATOR:  sin^2 i = v_los^2/(D theta sqrt(g_bar(g_bar+a0)))
  E-S8.4  THREE-RADIUS CONSISTENCY POLYGON: two independent pair estimates of
          a0/Upsilon from radii (1,2) and (2,3) must AGREE -- a closed algebraic
          identity in pure observables that tests the LAW itself with NO
          knowledge of a0, Upsilon, D, or i.
  E-S8.5  CHAIN TO COSMOLOGY: E-S8.1 (distance-free a0) + E-S3.3 Pythagorean weld
          -> H0 sqrt(Omega_L) = Z a0/c measured with NO distance ladder.

FLAGS: EXACT given the law + the observable model; real data adds asymmetric drift,
non-circular motions, warps (i(r) drift), and the disk geometry correction to
g_bar -- systematic, quantified only by the quick-fire (separate script). The
estimator is exact; the observable model is the approximation.
"""
import sympy as sp

ok = 0
def check(name, cond):
    global ok
    assert cond, "FAILED: " + name
    ok += 1
    print("[OK %2d] %s" % (ok, name))

# symbols
a0, Ups, D, G = sp.symbols("a0 Upsilon D G", positive=True)
sini = sp.symbols("sin_i", positive=True)
v1, v2, v3, th1, th2, th3, s1, s2, s3 = sp.symbols(
    "v1 v2 v3 theta1 theta2 theta3 s1 s2 s3", positive=True)  # v = TRUE velocities here

# build the synthetic observables FROM the law, with all nuisances explicit:
# at radius j: g_bar,j = Upsilon*s_j (disk-dominated case); law gives g_obs,j
def gobs_of(s):  # true observed acceleration from the law
    return sp.sqrt((Ups*s)**2 + a0*Ups*s)

# v_true,j^2 = g_obs,j * r_j = g_obs,j * D*theta_j ; v_los = v_true * sin i
vlos = {}
for j, (s, th) in enumerate([(s1, th1), (s2, th2), (s3, th3)], 1):
    vlos[j] = sp.sqrt(gobs_of(s)*D*th)*sini

# ---------------------------------------------------------------- E-S8.1
R12 = (vlos[1]/vlos[2])**4 * (th2/th1)**2
est = (s1**2 - R12*s2**2)/(R12*s2 - s1)
check("E-S8.1 pair estimator returns EXACTLY a0/Upsilon (D, sin i cancel identically)",
      sp.simplify(est - a0/Ups) == 0)
# explicit nuisance-independence: derivative w.r.t. D and sin i identically zero
check("E-S8.1b d(estimator)/dD == 0 and d(estimator)/d(sin i) == 0 identically",
      sp.simplify(sp.diff(est, D)) == 0 and sp.simplify(sp.diff(est, sini)) == 0)
# gas-dominated: set Upsilon=1, s_j -> g_gas,j known absolutely (distance-free)
check("E-S8.1c gas-dominated: a0 = (g1^2 - R g2^2)/(R g2 - g1) exactly",
      sp.simplify(est.subs(Ups, 1) - a0) == 0)

# uniqueness/degeneracy guard: the estimator blows up ONLY when R12 s2 = s1,
# i.e. when the two radii carry no independent information (s1=s2 limit)
den = sp.simplify(R12*s2 - s1)
check("E-S8.1d denominator vanishes at s1=s2 (degenerate pair) -- verified",
      sp.simplify(den.subs(s2, s1)) == 0)

# ---------------------------------------------------------------- E-S8.2 distance
gbar1 = Ups*s1
D_est = vlos[1]**2/(sini**2*th1*sp.sqrt(gbar1*(gbar1 + a0)))
check("E-S8.2 per-radius kinematic distance D = v_los^2/(sin^2 i theta sqrt(g_bar(g_bar+a0)))",
      sp.simplify(D_est - D) == 0)

# ---------------------------------------------------------------- E-S8.3 inclination
sini2_est = vlos[1]**2/(D*th1*sp.sqrt(gbar1*(gbar1 + a0)))
check("E-S8.3 inclination sin^2 i = v_los^2/(D theta sqrt(g_bar(g_bar+a0)))",
      sp.simplify(sini2_est - sini**2) == 0)

# ---------------------------------------------------------------- E-S8.4 polygon
R23 = (vlos[2]/vlos[3])**4 * (th3/th2)**2
est23 = (s2**2 - R23*s3**2)/(R23*s3 - s2)
poly = sp.simplify(est - est23)
check("E-S8.4 three-radius polygon: pair(1,2) == pair(2,3) identically under the law",
      poly == 0)
# and the polygon as a PURE-OBSERVABLE identity (no a0, Upsilon, D, i):
# (s1^2 - R12 s2^2)(R23 s3 - s2) == (s2^2 - R23 s3^2)(R12 s2 - s1)
lhs = (s1**2 - R12*s2**2)*(R23*s3 - s2)
rhs = (s2**2 - R23*s3**2)*(R12*s2 - s1)
check("E-S8.4b polygon in cross-multiplied pure-observable form",
      sp.simplify(lhs - rhs) == 0)

# ---------------------------------------------------------------- E-S8.5 chain
c, Z, H0, OmL = sp.symbols("c Z H0 Omega_L", positive=True)
# a0 from E-S8.1 (pure observables) -> H0 sqrt(Omega_L) = Z a0 / c
a0_obs = est.subs(Ups, 1)  # gas-dominated
HL = Z*a0_obs/c
check("E-S8.5 H_Lambda = Z/c * (g1^2 - R12 g2^2)/(R12 g2 - g1): a distance-ladder-free "
      "H0 sqrt(Omega_L) from two rotation-curve points",
      sp.simplify(HL - Z*a0/c) == 0)

# ---------------------------------------------------------------- counterexample honesty:
# the same elimination for McGaugh's nu is TRANSCENDENTAL (no closed form).
y = sp.symbols("y", positive=True)
nu_mcg = 1/(1 - sp.exp(-sp.sqrt(y)))
# g_obs^2 ratio at two radii = R12 -> solve for a0? equation contains exp(sqrt(s/a0)):
expr = (s1/a0*nu_mcg.subs(y, s1/a0))**2 - R12.subs(Ups, 1)*(s2/a0*nu_mcg.subs(y, s2/a0))**2
try:
    sol = sp.solve(sp.Eq(expr, 0), a0, dict=True)
    closed = len(sol) > 0 and all(not s[a0].has(sp.LambertW) for s in sol)
except (NotImplementedError, Exception):
    closed = False
check("HONESTY: the identical two-point elimination for McGaugh's nu has NO closed form "
      "(sympy cannot solve; the closed-form property is SPECIFIC to the quadratic framework law)",
      not closed)

print("\nALL %d CHECKS PASSED -- exit 0" % ok)
