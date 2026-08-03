#!/usr/bin/env python3
r"""mi_route_a_wb_gamma_v_2026.py -- THE WIDE-BINARY gamma_v TARGET UNDER ROUTE A. The frozen DR4 number moves
from 1.0310 to 1.1582, and that is a FIVE-FOLD BIGGER SIGNAL -- which is good for Newton-vs-MI and BAD for
everything else on this axis.

WHY THIS RUNS. Route A (2026-08-02) replaced the framework's power-law approach to Newton with an EXPONENTIAL
one, nu(y) = 1/(1 - e^-sqrt(y)). The wide-binary gamma_v prediction is a TRANSITION-REGIME number (the binary
sits at y_ext ~ 1-2), so it is maximally kernel-sensitive and must be RE-SOLVED, not rescaled. It also has a
frozen, hash-stamped pre-registration downstream (PREREGISTRATION_DR4.md, Amendments 1-7), so precision matters
more than usual. NOTHING in prep_2026/ is edited by this file; it only computes.

WHAT IS RE-SOLVED, exactly the way Amendment 4(d) computed 1.0310 (verified in V1 to 1e-5):
  the framework's MI law a = nu(|g_N|/a0) g_N is applied to each star's TOTAL Newtonian field. Linearising in
  the internal field gives an ANISOTROPIC response tensor with eigenvalues
      gamma^2_par  = dx/dy |_(y_extN)      (separation ALONG g_ext)      x = nu(y) y
      gamma^2_perp = nu(y_extN)            (separation PERPENDICULAR)
  and y_extN is the CLOSURE INVERSION of the OBSERVED g_ext,obs/a0 under the kernel in force -- Amendment 4(b)'s
  correction, which is what makes this re-solve kernel-dependent twice over (the inversion moves AND nu moves).
  The orientation average is the isotropic average of the RADIAL force boost, (gamma^2_par + 2 gamma^2_perp)/3,
  square-rooted; V1 proves that convention is the one that returns 1.030988.

  ROUTE A CANONICAL / PRIMARY g_ext:  y_extN 1.6809 -> 1.28903,  gamma_v 1.0310 -> 1.15820
  FULL RANGE over both a0 footings x both g_ext conventions:     1.0218-1.0472 -> 1.13107-1.19640

THE FOUR ANSWERS, and two of them cut against the front:
  (a) V2/V3  the substitutable target: 1.1582, range 1.1311-1.1964 (dynamical asymptote, no dilution -- the
      same footing that produced 1.0310 and 1.0218-1.0472).
  (b) V4  YES, a Newtonian 2-30 kAU result is still evidence AGAINST, and MUCH more strongly: 4.74 sigma_tot at
      the worst corner instead of 0.79, on the frozen error model at N = 30,000.
  (c) V5  the sigma_sys = 0.02 cap RISES from 1.55 sigma to 6.55-9.82 sigma if sigma_sys is absolute, or to a
      kernel-INVARIANT 4.50 sigma if it scales with the signal. Either way 3 sigma becomes reachable and
      section 1.5's "expected DECIDABLE" is RESTORABLE at N ~ 4,597-10,321. Checked three ways, because this
      corpus has already had to withdraw an "expected DECIDABLE" once.
  (d) V6  the hybrid S x L gate branch SURVIVES -- still < 0.1 sigma_tot from Newton at 10 kAU -- so the trap
      count stays 2. But the same 5x amplitude makes the gated branch's own cubic rise reach 1.56 sigma_fit by
      30 kAU, so it stops being Newtonian-indistinguishable at the OUTER edge of the frozen window.

AND THE COSTS, stated as plainly as the gains:
  * 1.1582 lands INSIDE the frozen decision band "1.145-1.20 -> MG-side; MI disfavored per z". The framework's
    own prediction would be scored as evidence against itself by the frozen table (V4).
  * the range 1.1311-1.1964 STRADDLES the frozen MG target 1.137, so a scorer running the frozen table cannot
    tell the framework's own prediction from the row the document forbids calling the framework's. Stated
    against my own headline: when BOTH rows are recomputed on Route A the physical MI-vs-MG separation
    actually IMPROVES, 1.16 -> 2.01 sigma_tot -- still under 3, so "likely UNDECIDABLE" stands unchanged (V4).
  * the worst corner 1.1964 is 0.0036 below the frozen ">1.20 contamination-guard zone, NO hypothesis verdict
    permitted" edge. On the alt footing a true framework detection is unscoreable by the frozen rule (V4).
  * gamma_par flips from SUB-Newtonian (0.9636) to SUPER-Newtonian (1.0380) on all 4/4 corners, so Amendment
    4(e)(ii) is Route-A-FALSE. The pre-declared PERPENDICULAR > PARALLEL sign survives (V2).
  * the frozen pipeline hard-codes the alpha=1 transition scale y_extN in its estimator shape and is
    hash-stamped shut. V5 prices that shape mismatch as a new, kernel-caused systematic.

Exit 0 = ran and every internal check held. No check(True), no hard-coded verdict: every PASS/FAIL below is a
numeric comparison that can fail, and the alpha=2 and alpha=1 reproductions in V1 are the controls that would
catch a wrong convention.
"""
from __future__ import annotations

import math
import pathlib
import sys

import numpy as np
import sympy as sp

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from mi_route_a_kernel import A0_ALT, A0_CANON, dmu_dx, mu, nu, u_of_x  # noqa: E402

ok: list[tuple[bool, str]] = []


def check(cond, msg):
    cond = bool(cond)
    ok.append((cond, msg))
    print(f"  [{'OK' if cond else 'FAIL'}] {msg}")
    return cond


def banner(t):
    print("\n" + "=" * 118)
    print(f"  {t}")
    print("=" * 118)


# ======================================================================================= FROZEN INPUTS
# every value below is quoted from PREREGISTRATION_DR4.md / its amendments, or from the frozen pipeline.
G_EXT_PRIMARY = 1.778e-10          # sec 1.1, "primary g_ext,obs"
G_EXT_ALTCONV = 2.078e-10          # sec 1.1, "Alt convention g_ext = Vc^2/R0"
GEXTS = (("primary g_ext,obs", G_EXT_PRIMARY), ("alt Vc^2/R0", G_EXT_ALTCONV))
FOOTINGS = (("canonical", A0_CANON), ("alt", A0_ALT))

A0_PREREG = 9.36e-11               # the rounded a0 the frozen document itself uses
A4D_POINT = 1.0310                 # Amendment 4(d), IN FORCE before Route A
A4D_RANGE = (1.0218, 1.0472)       # Amendment 4(d), IN FORCE before Route A
A4D_PAR, A4D_PERP = 0.9636, 1.0631  # Amendment 4(d)
A4C_YEXTN = {"canonical": 1.6809, "alt": 1.3280}   # Amendment 4(c), alpha=2 inversions
A3_RETIRED = 1.0246                # Amendment 3, retired by 4(d): the OBSERVED-argument value
A1_YEXTN_DOC = 1.4647              # sec 1.1, the alpha=1 inversion the FROZEN pipeline still hard-codes
BANKED_ASY_MAG = 1.1015            # sec 1.1 "dynamical asymptote 1.1015" (alpha=1, magnitude convention)
BANKED_DILUTED = 1.0508            # sec 1.1 "observable-diluted edge 1.0508"
FROZEN_MG = 1.137                  # the modified-GRAVITY row, never the MI target
FROZEN_MOND = 1.33
FROZEN_BAND = (1.05, 1.10)         # the original frozen MI band
DECISION_EDGES = (1.007, 1.083, 1.145, 1.20)   # sec 1.5 pre-declared band edges at sigma_tot = 0.028
SIG_FIT_30K = 0.0191               # sec 1.7 spread check, 8 catalogs @ 1.09
SIG_SYS = 0.02                     # sec 1.5, IRREDUCIBLE
SIG_ECC = 0.0150                   # sec 1.5/1.7, measured at INJECTED gamma = 1.09
SIG_FOOT_ALLOW = 0.005             # sec 1.5, estimator-side footing allowance
GATE_INJ_SIGNAL = 0.09             # the excess at which SIG_ECC was measured (inject 1.09)
GATE_FOOT_SPREAD = 1.0950 - 1.0925  # sec 1.7, canonical vs alt RECOVERED at inject 1.09
N_REF = 30000
A15_N_3SIG = 12200                 # sec 1.5's statistical-only claim
A7_CEILING = 1.55                  # Amendment 7's alpha=2 infinite-N ceiling, 1.09-2.36 corners
A7_CORNERS = (1.09, 2.36)
OMC = {"lo": 1.782e-14, "hi": 2.211e-14}   # Amendment 1's committed omega_c window, rad/s
A2_CUBIC_AMP = 0.0651              # Amendment 7 V1b, alpha=2 cubic prefactor 1/2[nu(y_extN)-1]
A1_GATED = (1.0004, 1.0006)        # Amendment 1's registered gated row
A2_GATED = (1.00012, 1.00020)      # Amendment 4(h)(i), the alpha=2 restatement

G_N, MSUN, AU, KAU = 6.674e-11, 1.989e30, 1.496e11, 1.496e14
M_WB = 1.5 * MSUN                  # the banked reference pair mass


# ======================================================================================= THE THREE KERNELS
def x_of_y_routeA(y):
    """observed x = nu(y) y under Route A."""
    y = np.asarray(y, float)
    return y * nu(y)


def y_of_x_routeA(x):
    """closure inversion under Route A: y = u(x)^2, exact via the module's validated inverter."""
    u = u_of_x(x)
    return u * u


def dxdy_routeA(y):
    """d(nu(y) y)/dy in closed form: (1/D)[1 - s e^-s/(2D)], s = sqrt(y), D = 1 - e^-s. V1 cross-checks it
    against sympy AND against the mu-side identity dx/dy = 1/(mu + x dmu/dx)."""
    y = np.asarray(y, float)
    s = np.sqrt(y)
    e = np.exp(-s)
    D = -np.expm1(-s)
    return (1.0 / D) * (1.0 - s * e / (2.0 * D))


def x_of_y_a2(y):
    y = np.asarray(y, float)
    return np.sqrt((y * y + y * np.sqrt(y * y + 4.0)) / 2.0)


def y_of_x_a2(x):
    x = np.asarray(x, float)
    return x * x / np.sqrt(1.0 + x * x)


def dxdy_a2(y):
    """dx/dy = 1/(dy/dx) with y = x^2/sqrt(1+x^2) => dy/dx = x(2+x^2)/(1+x^2)^{3/2}."""
    x = x_of_y_a2(y)
    return (1.0 + x * x) ** 1.5 / (x * (2.0 + x * x))


def x_of_y_a1(y):
    y = np.asarray(y, float)
    return np.sqrt(y * y + y)


def y_of_x_a1(x):
    x = np.asarray(x, float)
    return 0.5 * (-1.0 + np.sqrt(1.0 + 4.0 * x * x))


def dxdy_a1(y):
    y = np.asarray(y, float)
    return (2.0 * y + 1.0) / (2.0 * np.sqrt(y * y + y))


KERNELS = {
    "routeA": (x_of_y_routeA, y_of_x_routeA, dxdy_routeA),
    "alpha2": (x_of_y_a2, y_of_x_a2, dxdy_a2),
    "alpha1": (x_of_y_a1, y_of_x_a1, dxdy_a1),
}


# ======================================================================================= THE EFE OBSERVABLE
def efe_gammas(kern, gext, a0):
    """Amendment 4(d)'s construction, kernel-generic.

    returns dict with the closure-inverted Newtonian argument, the two response eigenvalues, and gamma_v in
    BOTH orientation-average conventions:
       'radial' : sqrt of the isotropic average of the RADIAL force boost = sqrt((g2par + 2 g2perp)/3)
                  -- the convention that returns Amendment 4(d)'s 1.030988 (proved in V1)
       'magnit' : sqrt of the isotropic average of |a_rel|/g_N -- the convention the banked
                  wb_dr4_prereg_framework_curve.py used for its 1.1015 (also proved in V1)
    """
    xf, yf, df = KERNELS[kern]
    x_ext = gext / a0
    yN = float(yf(x_ext))
    g2perp = float(xf(yN)) / yN            # = nu(y_extN); identically x_ext/y_extN
    g2par = float(df(yN))
    gv_rad = math.sqrt((g2par + 2.0 * g2perp) / 3.0)
    c = np.linspace(0.0, 1.0, 200001)      # isotropic: cos(theta) uniform on [0,1]
    gv_mag = math.sqrt(float(np.mean(np.sqrt(g2perp**2 + (g2par**2 - g2perp**2) * c * c))))
    return dict(x_ext=x_ext, yN=yN, g2par=g2par, g2perp=g2perp,
                gpar=math.sqrt(g2par), gperp=math.sqrt(g2perp), rad=gv_rad, mag=gv_mag)


def efe_grid(kern, a0_canon=A0_CANON):
    """the 4 combinations Amendment 4(d)'s range runs over: both a0 footings x both g_ext conventions."""
    out = {}
    for fl, a0 in (("canonical", a0_canon), ("alt", A0_ALT)):
        for gl, ge in GEXTS:
            out[(fl, gl)] = efe_gammas(kern, ge, a0)
    return out


# ---- the per-star nonlinear curve (the banked construction, kernel-generic) -------------------------
_COS = np.linspace(-1.0, 1.0, 4001)
_SIN = np.sqrt(np.clip(1.0 - _COS**2, 0.0, None))


def boost_perstar(y_rel, yN, kern):
    """framework-MI per-star law at FULL nonlinearity (no small-h expansion), equal masses.

    returns (radial-projection boost, magnitude boost). y_rel = G M_tot/(s^2 a0); each star's field from its
    companion is y_rel/2. e_ext = z, separation axis at angle theta.
    """
    xf, _, _ = KERNELS[kern]
    ys = 0.5 * y_rel
    y1z, y1x = yN + ys * _COS, ys * _SIN
    y2z, y2x = yN - ys * _COS, -ys * _SIN
    m1, m2 = np.hypot(y1z, y1x), np.hypot(y2z, y2x)
    n1, n2 = xf(m1) / m1, xf(m2) / m2
    az, ax = n1 * y1z - n2 * y2z, n1 * y1x - n2 * y2x
    rad = (az * _COS + ax * _SIN) / y_rel
    return float(np.mean(rad)), float(np.mean(np.hypot(az, ax) / y_rel))


def gamma_curve(y_rel, yN, kern, conv="mag"):
    r, m = boost_perstar(y_rel, yN, kern)
    return math.sqrt(m if conv == "mag" else r)


# ======================================================================================================
banner("V1  MACHINERY VALIDATION -- reproduce the COMMITTED alpha=2 and alpha=1 numbers, then a mutation "
       "control")

print("  Before Route A touches anything, the construction above must return the numbers already in the "
      "frozen document.\n")
print(f"  {'quantity':<52}{'committed':>12}{'this file':>12}{'dev':>11}")
print("  " + "-" * 88)
a2 = efe_grid("alpha2", a0_canon=A0_PREREG)
a2_cp = a2[("canonical", "primary g_ext,obs")]
a2_all_rad = [v["rad"] for v in a2.values()]
rows_v1 = [("Amendment 4(c) y_extN canonical (alpha=2)", A4C_YEXTN["canonical"], a2_cp["yN"]),
           ("Amendment 4(c) y_extN alt footing (alpha=2)", A4C_YEXTN["alt"],
            efe_gammas("alpha2", G_EXT_PRIMARY, A0_ALT)["yN"]),
           ("Amendment 4(d) gamma_par", A4D_PAR, a2_cp["gpar"]),
           ("Amendment 4(d) gamma_perp", A4D_PERP, a2_cp["gperp"]),
           ("Amendment 4(d) orientation-averaged gamma_v", A4D_POINT, a2_cp["rad"]),
           ("Amendment 4(d) range LOW corner", A4D_RANGE[0], min(a2_all_rad)),
           ("Amendment 4(d) range HIGH corner", A4D_RANGE[1], max(a2_all_rad))]
for nm, com, mine in rows_v1:
    print(f"  {nm:<52}{com:>12.4f}{mine:>12.6f}{abs(mine-com):>11.2e}")
worst_v1 = max(abs(m - c) for _, c, m in rows_v1)
check(worst_v1 < 1.2e-3,
      f"V1a the alpha=2 construction reproduces EVERY committed Amendment 4(c)/(d) number to a worst "
      f"deviation of {worst_v1:.2e} -- so the convention used below (closure-inverted Newtonian argument; "
      f"eigenvalues dx/dy and nu; isotropic average of the RADIAL boost) is demonstrably the one that "
      f"produced the in-force 1.0310, not a re-invention of it")
check(abs(a2_cp["rad"] - 1.030988) < 3e-5,
      f"V1b and it lands on the six-figure value the independent consolidation script reported "
      f"({a2_cp['rad']:.6f} vs 1.030988), which pins the orientation-average convention to 3e-5")

# alpha=1: the banked target script's two numbers, in the OTHER convention
a1 = efe_gammas("alpha1", G_EXT_PRIMARY, A0_PREREG)
print(f"\n  {'alpha=1 (the banked wb_dr4_prereg_framework_curve.py)':<52}{'committed':>12}{'this file':>12}"
      f"{'dev':>11}")
print("  " + "-" * 88)
for nm, com, mine in (("sec 1.1 y_extN", A1_YEXTN_DOC, a1["yN"]),
                      ("sec 1.1 dynamical asymptote (MAGNITUDE conv)", BANKED_ASY_MAG, a1["mag"])):
    print(f"  {nm:<52}{com:>12.4f}{mine:>12.6f}{abs(mine-com):>11.2e}")
check(abs(a1["yN"] - A1_YEXTN_DOC) < 2e-3 and abs(a1["mag"] - BANKED_ASY_MAG) < 2e-3,
      f"V1c the SECOND convention is validated too: the banked 'dynamical asymptote 1.1015' is the MAGNITUDE "
      f"average ({a1['mag']:.4f}), while the radial average gives {a1['rad']:.4f}. Both are carried below and "
      f"their spread is reported -- this is Amendment 4(h)(ii)'s mismatched-convention wrinkle, {abs(a1['mag']-a1['rad']):.4f} "
      f"at alpha=1, and it is not swept under the rug")

# MUTATION CONTROL: feed the OBSERVED ratio instead of the closure inversion. Must return Amendment 3's
# RETIRED value. If it does not, the diagnosis in Amendment 4(b) is not what I think it is.
xo = G_EXT_PRIMARY / A0_PREREG
g2p_bad, g2q_bad = float(dxdy_a2(xo)), float(x_of_y_a2(xo)) / xo
bad = math.sqrt((g2p_bad + 2 * g2q_bad) / 3.0)
print(f"\n  MUTATION CONTROL -- feed nu the OBSERVED ratio {xo:.4f} instead of y_extN {a2_cp['yN']:.4f}:")
print(f"      gamma_v = {bad:.6f}   vs Amendment 3's RETIRED {A3_RETIRED}  (dev {abs(bad-A3_RETIRED):.2e})")
print(f"      gamma_v = {a2_cp['rad']:.6f}   vs Amendment 4(d)'s IN-FORCE {A4D_POINT}  "
      f"(dev {abs(a2_cp['rad']-A4D_POINT):.2e})")
check(abs(bad - A3_RETIRED) < 1e-3 and abs(bad - A4D_POINT) > 5e-3,
      f"V1d the mutation control DISCRIMINATES: the observed-argument reading returns Amendment 3's retired "
      f"{A3_RETIRED} to {abs(bad-A3_RETIRED):.1e} while sitting {abs(bad-A4D_POINT):.1e} from the in-force "
      f"value. So this file is using the CORRECTED argument, and a silent reversion to the retired one would "
      f"have shown up here as a failure")

# derivative cross-checks: closed form vs sympy vs the mu-side identity
ys_ = sp.symbols("ys", positive=True)
x_sym = ys_ / (1 - sp.exp(-sp.sqrt(ys_)))
dx_sym = sp.lambdify(ys_, sp.diff(x_sym, ys_), "math")
tests = [0.3, 0.99240, 1.28903, 1.59095, 5.0]
d_sym = np.array([dx_sym(t) for t in tests])
d_cls = np.array([float(dxdy_routeA(t)) for t in tests])
xs_ = np.array([float(x_of_y_routeA(t)) for t in tests])
d_mu = 1.0 / (np.asarray(mu(xs_), float) + xs_ * np.asarray(dmu_dx(xs_), float))
print(f"\n  {'y':>10}{'dx/dy sympy':>14}{'dx/dy closed':>14}{'1/(mu + x mu_x)':>18}")
for t, a, b, c_ in zip(tests, d_sym, d_cls, d_mu):
    print(f"  {t:>10.5f}{a:>14.9f}{b:>14.9f}{c_:>18.9f}")
check(float(np.max(np.abs(d_cls / d_sym - 1))) < 1e-12 and float(np.max(np.abs(d_mu / d_sym - 1))) < 1e-9,
      f"V1e the Route A longitudinal eigenvalue is computed three independent ways -- closed form, sympy "
      f"differentiation, and the AQUAL-side identity dx/dy = 1/(mu + x dmu/dx) using the kernel module's own "
      f"dmu_dx -- agreeing to {float(np.max(np.abs(d_cls/d_sym-1))):.1e} and "
      f"{float(np.max(np.abs(d_mu/d_sym-1))):.1e}. The nu-form and mu-form of Route A are consistent in "
      f"spherical symmetry, which is the only place they must be")


# ======================================================================================================
banner("V2  (a) THE ROUTE A TARGET -- all four corners, both conventions, both a0 footings carried")

rA = efe_grid("routeA")
print(f"  {'footing':<11}{'g_ext convention':<20}{'x_ext':>9}{'y_extN':>10}{'nu(y_extN)':>12}"
      f"{'gamma_par':>11}{'gamma_perp':>12}{'gamma_v rad':>13}{'gamma_v mag':>13}")
print("  " + "-" * 111)
for k in sorted(rA, key=lambda t: (t[0], t[1])):
    v = rA[k]
    print(f"  {k[0]:<11}{k[1]:<20}{v['x_ext']:>9.5f}{v['yN']:>10.5f}{v['g2perp']:>12.5f}"
          f"{v['gpar']:>11.5f}{v['gperp']:>12.5f}{v['rad']:>13.5f}{v['mag']:>13.5f}")
rA_cp = rA[("canonical", "primary g_ext,obs")]
rA_rad = [v["rad"] for v in rA.values()]
RA_POINT, RA_LO, RA_HI = rA_cp["rad"], min(rA_rad), max(rA_rad)
print(f"\n  *** ROUTE A, SUBSTITUTABLE INTO AMENDMENT 4(d)'s SLOT ***")
print(f"      orientation-averaged, primary g_ext / canonical a0 :  {A4D_POINT}  ->  {RA_POINT:.4f}")
print(f"      full range over both footings x both g_ext          :  {A4D_RANGE[0]}-{A4D_RANGE[1]}  ->  "
      f"{RA_LO:.4f}-{RA_HI:.4f}")
print(f"      gamma_par (primary/canonical)                       :  {A4D_PAR}  ->  {rA_cp['gpar']:.4f}")
print(f"      gamma_perp (primary/canonical)                      :  {A4D_PERP}  ->  {rA_cp['gperp']:.4f}")
print(f"      y_extN fed to nu (canonical / alt)                  :  "
      f"{A4C_YEXTN['canonical']}/{A4C_YEXTN['alt']}  ->  {rA_cp['yN']:.4f}/"
      f"{rA[('alt','primary g_ext,obs')]['yN']:.4f}")
print(f"      convention spread (radial vs magnitude), worst corner: "
      f"{max(abs(v['mag']-v['rad']) for v in rA.values()):.4f}")

check(RA_LO > A4D_RANGE[1],
      f"V2a *** THE TARGET MOVES UP BY A FACTOR {(RA_POINT-1)/(A4D_POINT-1):.2f} IN THE OBSERVABLE. *** Route "
      f"A's ENTIRE range {RA_LO:.4f}-{RA_HI:.4f} sits above the whole in-force alpha=2 range "
      f"{A4D_RANGE[0]}-{A4D_RANGE[1]}: the two do not overlap, so this is an amendment-grade move, not a "
      f"rounding drift. gamma_v - 1 goes {A4D_POINT-1:.4f} -> {RA_POINT-1:.4f}")
check(all(v["gperp"] > v["gpar"] for v in rA.values()),
      f"V2b THE PRE-DECLARED ANISOTROPY SIGN SURVIVES on all 4/4 corners: PERPENDICULAR pairs still show the "
      f"larger boost (worst margin {min(v['gperp']-v['gpar'] for v in rA.values()):.4f}). Amendment 2(f)/3(c)'s "
      f"pre-registered falsifier -- an opposite-sense anisotropy at >3 sigma -- is intact and is in fact "
      f"STRONGER under Route A (spread {rA_cp['gperp']-rA_cp['gpar']:.4f} vs alpha=2's "
      f"{a2_cp['gperp']-a2_cp['gpar']:.4f})")
npar_super = sum(1 for v in rA.values() if v["gpar"] > 1.0)
check(npar_super == 4,
      f"V2c *** AGAINST THE COMMITTED RECORD: gamma_par is SUPER-Newtonian on {npar_super}/4 corners under "
      f"Route A ({min(v['gpar'] for v in rA.values()):.4f}-{max(v['gpar'] for v in rA.values()):.4f}), so "
      f"Amendment 4(e)(ii)'s 'gamma_v || stays sub-Newtonian on all 4/4 (0.9592-0.9688)' is ROUTE-A-FALSE. *** "
      f"That claim was alpha=2-specific (alpha=1 also gave super-Newtonian, {a1['gpar']:.4f}), and it must be "
      f"withdrawn rather than quietly re-scoped. Note this does NOT touch V2b: the SIGN of the anisotropy is "
      f"perpendicular-larger in all three kernels; only the absolute level of the parallel eigenvalue moves "
      f"across 1")


# ======================================================================================================
banner("V3  THE FULL NONLINEAR CURVE -- is the asymptote actually the right target for a 2-30 kAU sample?")

print("  The linear-response eigenvalues assume the internal field is a PERTURBATION on g_ext. In 2-30 kAU it")
print("  is not: at 2 kAU a 1.5 Msun pair's internal field is ~24 a0, twelve times g_ext. So the asymptote is")
print("  only the right target if the estimator's DEEP bins carry the fit -- which they do, the frozen")
print("  pipeline's deep cut being y < 0.3. This section prices that, kernel by kernel.\n")
yN_rA = rA_cp["yN"]
yN_a2 = a2_cp["yN"]
print(f"  {'s [kAU]':>9}{'y_int/a0':>10}{'| alpha=2 rad':>14}{'alpha=2 mag':>13}{'| routeA rad':>14}"
      f"{'routeA mag':>12}{'routeA diluted':>16}")
print("  " + "-" * 90)
curve = {}
for s_kau in (2., 3., 5., 10., 15., 18., 20., 30., 60., 200.):
    yr = G_N * M_WB / (s_kau * KAU) ** 2 / A0_CANON
    r2, m2 = boost_perstar(yr, yN_a2, "alpha2")
    rr, mr = boost_perstar(yr, yN_rA, "routeA")
    curve[s_kau] = (yr, math.sqrt(r2), math.sqrt(m2), math.sqrt(rr), math.sqrt(mr))
    dil = 1.0 + 0.5 * (math.sqrt(mr) - 1.0)
    print(f"  {s_kau:>9.0f}{yr:>10.4f}{math.sqrt(r2):>14.4f}{math.sqrt(m2):>13.4f}"
          f"{math.sqrt(rr):>14.4f}{math.sqrt(mr):>12.4f}{dil:>16.4f}")

asy_rA_rad = gamma_curve(1e-6, yN_rA, "routeA", "rad")
asy_rA_mag = gamma_curve(1e-6, yN_rA, "routeA", "mag")
print(f"\n  s -> inf asymptote, Route A:  radial {asy_rA_rad:.5f}   magnitude {asy_rA_mag:.5f}")
print(f"  linear-response prediction:   radial {rA_cp['rad']:.5f}   magnitude {rA_cp['mag']:.5f}")
check(abs(asy_rA_rad - rA_cp["rad"]) < 2e-3 and abs(asy_rA_mag - rA_cp["mag"]) < 2e-3,
      f"V3a the FULL NONLINEAR per-star solve reproduces the linear-response tensor result to "
      f"{max(abs(asy_rA_rad-rA_cp['rad']), abs(asy_rA_mag-rA_cp['mag'])):.1e} in gamma_v -- so the eigenvalue "
      f"expansion is valid for Route A too, and V2's table is not an artefact of linearising a more strongly "
      f"curved kernel")

# fraction of the asymptotic excess realised at the frozen deep-cut boundary y = 0.3
s_deep = math.sqrt(G_N * M_WB / (0.3 * A0_CANON)) / KAU
f_rA = (gamma_curve(0.3, yN_rA, "routeA", "mag") - 1) / (asy_rA_mag - 1)
f_a2 = (gamma_curve(0.3, yN_a2, "alpha2", "mag") - 1) / (gamma_curve(1e-6, yN_a2, "alpha2", "mag") - 1)
print(f"\n  frozen deep cut y < 0.3 corresponds to s > {s_deep:.1f} kAU for 1.5 Msun.")
print(f"  fraction of the ASYMPTOTIC excess already realised AT y = 0.3:  Route A {100*f_rA:.1f}%   "
      f"alpha=2 {100*f_a2:.1f}%")
check(f_rA > 0.55 and f_rA / f_a2 > 0.90,
      f"V3b the asymptote remains the right target: {100*f_rA:.0f}% of the excess is already present at the "
      f"deep-cut boundary under Route A, versus {100*f_a2:.0f}% under alpha=2 -- a ratio of "
      f"{f_rA/f_a2:.3f}, i.e. Route A's transition is NOT materially slower. Had this come out below ~0.9 the "
      f"asymptotic target would have been the wrong number to hand a 2-30 kAU pipeline")

dil_pt = 1.0 + 0.5 * (asy_rA_mag - 1.0)
dil_lo = 1.0 + 0.5 * (min(v["mag"] for v in rA.values()) - 1.0)
dil_hi = 1.0 + 0.5 * (max(v["mag"] for v in rA.values()) - 1.0)
print(f"\n  FOR THE RECORD, the banked observable-dilution row (factor 0.5 on the velocity excess, the")
print(f"  crude Banik-style marginalisation that produced sec 1.1's 'observable-diluted edge {BANKED_DILUTED}'):")
print(f"      Route A diluted point {dil_pt:.4f}, diluted range {dil_lo:.4f}-{dil_hi:.4f}")
check(FROZEN_BAND[0] < dil_lo and dil_hi < FROZEN_BAND[1] + 0.01,
      f"V3c reported because it is uncomfortable rather than because it helps: Route A's DILUTED range "
      f"{dil_lo:.4f}-{dil_hi:.4f} falls almost exactly inside the ORIGINAL frozen band {FROZEN_BAND} that "
      f"alpha=1 produced. That is a coincidence of two compensating factor-of-~5 and factor-of-2 moves and it "
      f"must NOT be used to claim 'the frozen band survives' -- Amendment 4(d)'s undiluted footing is the one "
      f"in force, and on that footing the target moves by {RA_POINT-A4D_POINT:+.4f}")


# ======================================================================================================
banner("V4  (b) WOULD A NEWTONIAN 2-30 kAU RESULT STILL BE EVIDENCE AGAINST? -- and where 1.1582 lands in "
       "the FROZEN decision table")

sig_tot_30k = math.hypot(SIG_FIT_30K, SIG_SYS)
print(f"  frozen error model: sigma_tot = sqrt(sigma_fit^2 + {SIG_SYS}^2), sigma_fit = {SIG_FIT_30K} at "
      f"N = {N_REF:,} -> sigma_tot = {sig_tot_30k:.5f}\n")
print(f"  {'hypothesis / corner':<40}{'gamma_v':>10}{'gamma_v-1':>11}{'z @ N=30k':>12}{'z @ N=inf':>12}")
print("  " + "-" * 85)
zrows = [("alpha=2 in force (Amendment 4d point)", A4D_POINT),
         ("alpha=2 worst corner", A4D_RANGE[0]),
         ("ROUTE A point (canonical/primary)", RA_POINT),
         ("ROUTE A worst corner (lowest)", RA_LO),
         ("ROUTE A best corner (highest)", RA_HI)]
for nm, g in zrows:
    print(f"  {nm:<40}{g:>10.4f}{g-1:>11.4f}{(g-1)/sig_tot_30k:>12.2f}{(g-1)/SIG_SYS:>12.2f}")
z30_lo, z30_hi = (RA_LO - 1) / sig_tot_30k, (RA_HI - 1) / sig_tot_30k
z30_a2 = (A4D_RANGE[0] - 1) / sig_tot_30k
check(z30_lo > 3.0,
      f"V4a *** YES, AND MUCH MORE STRONGLY. *** A measured gamma_hat = 1.000 sits {z30_lo:.2f}-{z30_hi:.2f} "
      f"sigma_tot from the Route A target at the frozen N = 30,000 -- above 3 even at the WORST corner, where "
      f"alpha=2 gave only {z30_a2:.2f}. Amendment 6's un-hedged rule (a Newtonian 2-30 kAU result is evidence "
      f"AGAINST, and must not be re-hedged after DR4) therefore becomes ENFORCEABLE under Route A instead of "
      f"merely declared")
check((RA_POINT - 1) / sig_tot_30k > 2.0 * (A4D_POINT - 1) / sig_tot_30k,
      f"V4b the improvement is a factor {(RA_POINT-1)/(A4D_POINT-1):.2f} in the observable and therefore in "
      f"every z on this axis: {(A4D_POINT-1)/sig_tot_30k:.2f} -> {(RA_POINT-1)/sig_tot_30k:.2f} sigma_tot at "
      f"the point value. This is the one unambiguously GOOD consequence of Route A for the wide-binary front")

print(f"\n  NOW THE COST. Section 1.5's pre-declared decision bands, and where Route A's own prediction lands:")
edges = [(-1e9, DECISION_EDGES[0], "supports Newtonian over framework-MI (MI disfavored > 3 sigma)"),
         (DECISION_EDGES[0], DECISION_EDGES[1], "no hypothesis separation -- undecided"),
         (DECISION_EDGES[1], DECISION_EDGES[2], "non-Newtonian >=3 sigma AND framework-MI-compatible"),
         (DECISION_EDGES[2], DECISION_EDGES[3], "MG-side; MI DISFAVORED per z"),
         (DECISION_EDGES[3], 1e9, "contamination-guard: NO hypothesis verdict permitted")]


def band_of(g):
    for lo, hi, nm in edges:
        if lo <= g < hi:
            return nm
    return "?"


for nm, g in (("alpha=2 in force", A4D_POINT), ("ROUTE A point", RA_POINT),
              ("ROUTE A worst corner", RA_LO), ("ROUTE A best corner", RA_HI),
              ("frozen MG row", FROZEN_MG), ("DR3 dry run", 1.205)):
    print(f"      {nm:<24}{g:7.4f}  ->  {band_of(g)}")
check(band_of(RA_POINT) == "MG-side; MI DISFAVORED per z",
      f"V4c *** THE FRAMEWORK'S OWN ROUTE A PREDICTION LANDS IN THE BIN PRE-DECLARED 'MG-side; MI DISFAVORED "
      f"per z'. *** {RA_POINT:.4f} falls in [{DECISION_EDGES[2]}, {DECISION_EDGES[3]}). A scorer executing the "
      f"frozen table on a measurement AT the framework's own prediction would record the framework as "
      f"disfavored. This is the SAME class of scoring defect Amendment 1 fixed and Amendment 7 V3c re-found, "
      f"and it is the single most important thing the Route A amendment has to repair")
# the as-MG row is itself kernel-dependent and Amendment 4(i) explicitly left it uncorrected. Recompute it
# like-for-like: the banked MG asymptote <nu(y_tot)> -> nu(y_extN), i.e. gamma_v = sqrt(nu) = the PERP
# eigenvalue exactly (equivalently 1/sqrt(mu(x_ext)) -- the same number, since mu = 1/nu in this closure).
mg = {k: v["gperp"] for k, v in rA.items()}
mg_a1 = a1["gperp"]
MG_RA, MG_LO, MG_HI = mg[("canonical", "primary g_ext,obs")], min(mg.values()), max(mg.values())
print(f"\n  AND THE 'framework-as-MG' ROW IS ITSELF STALE -- Amendment 4(i) left it uncorrected on purpose.")
print(f"  Like-for-like (the banked MG asymptote <nu(y_tot)> -> nu(y_extN), so gamma_v = sqrt(nu) = the perp")
print(f"  eigenvalue): alpha=1 gives {mg_a1:.4f} (the frozen {FROZEN_MG}, 'computed 1.1389'), alpha=2 gives "
      f"{a2_cp['gperp']:.4f},")
print(f"  Route A gives {MG_RA:.4f} (range {MG_LO:.4f}-{MG_HI:.4f}). So comparing Route A's MI row against the")
print(f"  FROZEN {FROZEN_MG} is comparing two different kernels. Both comparisons matter and they say "
      f"different things:")
sep_ra = abs(MG_RA - RA_POINT) / sig_tot_30k
sep_a2 = abs(a2_cp["gperp"] - A4D_POINT) / sig_tot_30k
print(f"      MI vs the FROZEN MG row 1.137        : {abs(RA_POINT-FROZEN_MG):.4f} = "
      f"{abs(RA_POINT-FROZEN_MG)/sig_tot_30k:.2f} sigma_tot   (alpha=2: "
      f"{abs(A4D_POINT-FROZEN_MG)/sig_tot_30k:.2f})")
print(f"      MI vs the RECOMPUTED MG row, same kernel: {abs(MG_RA-RA_POINT):.4f} = {sep_ra:.2f} sigma_tot   "
      f"(alpha=2: {sep_a2:.2f})")
check(RA_LO < FROZEN_MG < RA_HI and sep_ra > sep_a2 and sep_ra < 3.0,
      f"V4d TWO FINDINGS THAT PULL IN OPPOSITE DIRECTIONS, and both must be registered. (i) A SCORING "
      f"degeneracy: the frozen MG target {FROZEN_MG} now lies INSIDE Route A's framework-MI range "
      f"{RA_LO:.4f}-{RA_HI:.4f}, only {abs(RA_POINT-FROZEN_MG)/sig_tot_30k:.2f} sigma_tot from the MI point "
      f"value, so a scorer executing the frozen table cannot tell the framework's own prediction from the row "
      f"the document forbids presenting as the framework's. (ii) But the PHYSICAL MI-vs-MG separation actually "
      f"IMPROVES when both rows are recomputed on the same kernel: {sep_a2:.2f} -> {sep_ra:.2f} sigma_tot. It "
      f"is still below the frozen 3-sigma requirement, so section 1.5's 'MI vs MG likely UNDECIDABLE' STANDS "
      f"-- it is not superseded and it must not be upgraded. I am recording (ii) explicitly because (i) alone "
      f"reads as a bigger disaster than the arithmetic supports")
gap_guard = DECISION_EDGES[3] - RA_HI
check(0.0 < gap_guard < 0.02,
      f"V4e *** AND THE WORST CORNER IS {gap_guard:.4f} BELOW THE CONTAMINATION-GUARD EDGE {DECISION_EDGES[3]}. *** "
      f"On the alt a0 footing with the primary g_ext, Route A predicts {RA_HI:.4f}; the frozen rule says any "
      f"gamma_hat > {DECISION_EDGES[3]} permits NO hypothesis verdict at all. So on that corner a genuine "
      f"framework detection would be pre-declared UNSCOREABLE. Related and equally uncomfortable: the DR3 dry "
      f"run's 1.205 -- correctly dismissed as contamination-dominated because three triple screens were not "
      f"implementable -- is now only {abs(1.205-RA_HI):.4f} from the framework's own worst-corner prediction. "
      f"That does not make 1.205 evidence FOR anything (it remains evidence for nothing), but the framework "
      f"can no longer treat '>1.20 = contamination' as automatic")
# the frozen a0-DEGENERACY flag, re-priced. It must not be quietly loosened by a bigger signal.
A0_MILGROM = 1.2e-10
deg = {}
for kn, lab in (("alpha1", "alpha=1 (the banked check)"), ("alpha2", "alpha=2"), ("routeA", "ROUTE A")):
    f_ = efe_gammas(kn, G_EXT_PRIMARY, A0_CANON)
    m_ = efe_gammas(kn, G_EXT_PRIMARY, A0_MILGROM)
    deg[kn] = (f_["rad"], m_["rad"])
print(f"\n  THE FROZEN a0-DEGENERACY FLAG, RE-PRICED (same PHYSICAL g_ext, a0 {A0_CANON:.3e} -> Milgrom "
      f"{A0_MILGROM:.1e}, {100*(A0_MILGROM/A0_CANON-1):+.0f}%):")
print(f"  {'kernel':<28}{'gamma_v @ framework a0':>24}{'@ Milgrom a0':>15}{'d gamma_v':>11}"
      f"{'/sigma_tot':>12}{'d(gamma-1)/(gamma-1)':>22}")
print("  " + "-" * 112)
for kn, lab in (("alpha1", "alpha=1 (the banked check)"), ("alpha2", "alpha=2"), ("routeA", "ROUTE A")):
    f_, m_ = deg[kn]
    print(f"  {lab:<28}{f_:>24.4f}{m_:>15.4f}{m_-f_:>11.4f}{(m_-f_)/sig_tot_30k:>12.2f}"
          f"{(m_-1)/(f_-1)-1:>21.1%}")
d_rA = (deg["routeA"][1] - deg["routeA"][0]) / sig_tot_30k
d_a1 = (deg["alpha1"][1] - deg["alpha1"][0]) / sig_tot_30k
a0_effect = deg["routeA"][1] - deg["routeA"][0]
check(d_rA > d_a1 and (RA_HI - RA_LO) > a0_effect,
      f"V4f THE a0-DEGENERACY FLAG SURVIVES AND MUST NOT BE LOOSENED, but its price changes. In RELATIVE terms "
      f"the sensitivity is nearly kernel-invariant (a {100*(A0_MILGROM/A0_CANON-1):.0f}% a0 change moves "
      f"(gamma_v - 1) by {100*((deg['routeA'][1]-1)/(deg['routeA'][0]-1)-1):.0f}% under Route A vs "
      f"{100*((deg['alpha1'][1]-1)/(deg['alpha1'][0]-1)-1):.0f}% at alpha=1). In ABSOLUTE, measurable terms it "
      f"grows from {d_a1:.2f} to {d_rA:.2f} sigma_tot, so a DR4 measurement is more a0-sensitive than before. "
      f"That is still NOT permission to report a DR4 gamma_v as measuring a0, and here is the decisive "
      f"arithmetic: the framework's OWN internal footing x g_ext fork already spans {RA_HI-RA_LO:.4f} in "
      f"gamma_v, which is LARGER than the {a0_effect:.4f} that a {100*(A0_MILGROM/A0_CANON-1):.0f}% change in "
      f"a0 produces. The framework cannot resolve a0 against an ambiguity bigger than the signal it is trying "
      f"to read. The frozen flag stands verbatim; only the number attached to it moves")

print(f"\n  For orientation, NOT as a claim: Chae et al. 2026's force gamma 1.600 (+0.171/-0.141) is velocity")
print(f"  gamma_v ~ 1.26 (sec 1.1's own conversion). Route A's {RA_LO:.3f}-{RA_HI:.3f} is nearer that than")
print(f"  alpha=2's {A4D_RANGE[0]}-{A4D_RANGE[1]} was, which cuts against the banked note that matching Chae")
print(f"  needed a0 ~ 1.9x canonical. It is not a confirmation of anything: the two published analyses of the")
print(f"  same catalogue differ by 0.174 in gamma_v, which is larger than this entire discussion.")


# ======================================================================================================
banner("V5  (c) RE-DERIVING THE sigma_sys = 0.02 CAP UNDER ROUTE A -- checked three ways, because an "
       "'expected DECIDABLE' has already had to be withdrawn once")

print(f"  Amendment 7's cap: as N -> inf, sigma_fit -> 0 and sigma_tot -> sigma_sys = {SIG_SYS} irreducibly, so")
print(f"  Newton-vs-MI ceilings at (gamma_v - 1)/sigma_sys. At alpha=2 that was {A7_CEILING} "
      f"({A7_CORNERS[0]}-{A7_CORNERS[1]} across corners) and 3 sigma was unreachable at ANY N.\n")
print(f"  READING 1 -- sigma_sys is ABSOLUTE (the frozen document's literal reading: a fixed 0.02 allowance)")
cap_pt, cap_lo, cap_hi = (RA_POINT - 1) / SIG_SYS, (RA_LO - 1) / SIG_SYS, (RA_HI - 1) / SIG_SYS
print(f"      ceiling = {cap_pt:.2f} sigma at the point value, {cap_lo:.2f}-{cap_hi:.2f} across corners "
      f"(alpha=2: {A7_CEILING} / {A7_CORNERS[0]}-{A7_CORNERS[1]})")
check(cap_lo > 3.0,
      f"V5a *** THE CAP RISES ABOVE 3 SIGMA ON THE FROZEN DOCUMENT'S OWN LITERAL ERROR MODEL: "
      f"{cap_lo:.2f}-{cap_hi:.2f} sigma versus alpha=2's {A7_CORNERS[0]}-{A7_CORNERS[1]}. *** Newton-vs-MI "
      f"becomes decidable at infinite N even at the worst corner, which is the improvement Amendment 7 said "
      f"the alpha=2 signal could not deliver")

print(f"\n  READING 2 -- sigma_sys SCALES WITH THE SIGNAL. This is the hostile reading and it must be run,")
print(f"      because the frozen sigma_sys was CALIBRATED at an injected excess of {GATE_INJ_SIGNAL} "
      f"(sec 1.7: inject 1.09,")
print(f"      flat-e truth under a thermal-e model shifts gamma by -{SIG_ECC}). If that eccentricity bias is a")
print(f"      fractional mis-scaling of the BOOST rather than an additive offset, it grows with the signal.")
sig_sys_prop_pt = SIG_SYS * (RA_POINT - 1) / GATE_INJ_SIGNAL
sig_sys_prop_lo = SIG_SYS * (RA_LO - 1) / GATE_INJ_SIGNAL
print(f"      sigma_sys(prop) = {SIG_SYS} x (gamma_v-1)/{GATE_INJ_SIGNAL} = {sig_sys_prop_pt:.4f} at the point "
      f"value, {sig_sys_prop_lo:.4f} at the worst corner")
cap_prop = (RA_POINT - 1) / sig_sys_prop_pt
cap_prop_a2 = (A4D_POINT - 1) / (SIG_SYS * (A4D_POINT - 1) / GATE_INJ_SIGNAL)
print(f"      ceiling = {cap_prop:.2f} sigma -- and it is KERNEL-INVARIANT: the same construction gives "
      f"{cap_prop_a2:.2f} at alpha=2,")
print(f"      because a systematic proportional to the signal cancels the signal exactly. "
      f"= {GATE_INJ_SIGNAL}/{SIG_SYS} = {GATE_INJ_SIGNAL/SIG_SYS:.2f}.")
# TAUTOLOGY FIXED 2026-08-03: `cap_prop > 3.0 and abs(cap_prop - cap_prop_a2) < 1e-9` could not fail --
# cap_prop reduces algebraically to GATE_INJ_SIGNAL/SIG_SYS and cap_prop_a2 to the identical expression, so the
# second conjunct is a float identity and the first compares two frozen constants (0.09/0.02). The substantive
# and FALSIFIABLE content is that this reading gives Route A NO improvement over alpha=2, which is the
# against-interest half and is what is now asserted.
# asserting the kernel-invariance would ALSO be an identity (both sides reduce to GATE_INJ_SIGNAL/SIG_SYS).
# The falsifiable content is the COMPARISON OF TWO DIFFERENT CONSTRUCTIONS: the proportional-reading ceiling
# must come out BELOW the absolute-reading ceiling V5a claims, i.e. the hostile reading STRIPS the improvement.
cap_abs_pt = (RA_POINT - 1) / SIG_SYS
print(f"      against the ABSOLUTE-reading ceiling V5a claims at the point value: {cap_abs_pt:.2f} sigma")
check(cap_prop < cap_abs_pt,
      f"V5b under the fully-proportional reading the ceiling is {cap_prop:.2f} sigma and is EXACTLY "
      f"kernel-invariant -- ROUTE A EARNS ZERO IMPROVEMENT ON THIS READING, which is the honest statement and "
      f"is what this check now asserts (the previous form could not fail). Two consequences, one for each side "
      f"of the ledger: (i) 3 sigma is nominally reachable on this reading, but NOT because of Route A -- "
      f"alpha=2 would already have been at {cap_prop_a2:.2f}, so V5a's improvement is specific to the ABSOLUTE "
      f"reading and does not survive the proportional one; (ii) it exposes that Amendment "
      f"7's {A7_CEILING}-sigma cap was itself an artefact of treating a signal-calibrated systematic as "
      f"absolute -- if sigma_sys is even partly proportional, the alpha=2 front was never as dead as "
      f"{A7_CEILING} sigma implied. The truth is between the two readings and the frozen document does not "
      f"say which")

print(f"\n  READING 3 -- the FINITE-N requirement, which is what section 1.5 actually claims.")
print(f"  {'reading':<34}{'sigma_sys':>11}{'sigma_fit needed':>18}{'N for 3 sigma':>15}")
print("  " + "-" * 80)
ns = {}
for lab, ss, sig in (("absolute, point value", SIG_SYS, RA_POINT - 1),
                     ("absolute, worst corner", SIG_SYS, RA_LO - 1),
                     ("proportional, point value", sig_sys_prop_pt, RA_POINT - 1),
                     ("proportional, worst corner", sig_sys_prop_lo, RA_LO - 1)):
    need_tot = sig / 3.0
    v = need_tot**2 - ss**2
    if v <= 0:
        print(f"  {lab:<34}{ss:>11.4f}{'--':>18}{'UNREACHABLE':>15}")
        ns[lab] = float("inf")
        continue
    need_fit = math.sqrt(v)
    n = N_REF * (SIG_FIT_30K / need_fit) ** 2
    ns[lab] = n
    print(f"  {lab:<34}{ss:>11.4f}{need_fit:>18.4f}{n:>15,.0f}")
n_worst = max(ns.values())
check(n_worst < N_REF,
      f"V5c *** SECTION 1.5's 'expected DECIDABLE' IS RESTORABLE UNDER ROUTE A. *** 3 sigma on Newton-vs-MI "
      f"needs N ~ {min(ns.values()):,.0f}-{n_worst:,.0f} depending on the corner and the sigma_sys reading -- "
      f"below the N = {N_REF:,} the frozen document assumes, on ALL FOUR combinations. Amendment 7 withdrew "
      f"that claim as stale on the alpha=2 signal (where it was unreachable at any N); Route A makes it true "
      f"again. It should be RE-registered with the arithmetic shown, not merely un-withdrawn, and the frozen "
      f"N >~ {A15_N_3SIG:,} remains wrong as written because it was alpha=1 statistical-only")

print(f"\n  WHAT DOES *NOT* IMPROVE, and one thing that gets WORSE:")
foot_spread_target = RA_HI - RA_LO
foot_spread_a2 = A4D_RANGE[1] - A4D_RANGE[0]
print(f"   * the TARGET's footing x g_ext spread grows {foot_spread_a2:.4f} -> {foot_spread_target:.4f} "
      f"({foot_spread_target/foot_spread_a2:.2f}x). That is target-side, NOT part of sigma_sys -- sec 1.5's")
print(f"     'a0-footing spread <= {SIG_FOOT_ALLOW}' is the ESTIMATOR-side spread (sec 1.7: recovered 1.0950 "
      f"canonical vs")
print(f"     1.0925 alt at injected 1.09 = {GATE_FOOT_SPREAD:.4f}), so the correct handling is to quote the "
      f"worst corner, which V4 does.")
foot_est_prop = GATE_FOOT_SPREAD * (RA_POINT - 1) / GATE_INJ_SIGNAL
print(f"     Scaled to Route A's signal the estimator-side spread would be {foot_est_prop:.4f}, still within "
      f"the frozen {SIG_FOOT_ALLOW} allowance.")
check(foot_est_prop < SIG_FOOT_ALLOW,
      f"V5d the frozen sigma_sys line item for the a0 footing is NOT breached by Route A "
      f"({foot_est_prop:.4f} < {SIG_FOOT_ALLOW}) -- recorded explicitly so the growth of the TARGET spread to "
      f"{foot_spread_target:.4f} is not mis-sold as a systematic-budget failure. Two different objects; only "
      f"the target one moves, and the honest response to it is the worst-corner quote, not an inflated "
      f"sigma_sys")

# the genuinely NEW, kernel-caused systematic: the frozen estimator's hard-coded alpha=1 transition scale
print(f"\n   * A NEW SYSTEMATIC ROUTE A CREATES, AND IT IS UNFIXABLE BY DESIGN. The frozen, hash-stamped")
print(f"     wide_binary_pipeline.py fits gamma_inf through the declared shape")
print(f"         gamma(y) = 1 + (gamma_inf - 1) * yE/(yE + y),   yE = y_newt_from_obs(g_ext/a0)")
print(f"     and y_newt_from_obs is the ALPHA=1 closure inversion, yE = {A1_YEXTN_DOC} (canonical). Route A's")
print(f"     true transition scale is yE = {yN_rA:.4f}, {100*(yN_rA/A1_YEXTN_DOC-1):+.1f}%. The pipeline cannot "
      f"be edited.")
EDGES_LOG = np.array([-1.5, -1.1, -0.8, -0.5, -0.2, 0.1, 0.5])     # sec: the DEEP bins (log10 y < 0.5)
ycen = 10 ** (0.5 * (EDGES_LOG[:-1] + EDGES_LOG[1:]))
true_rad = np.array([gamma_curve(float(y), yN_rA, "routeA", "mag") for y in ycen])
shape = A1_YEXTN_DOC / (A1_YEXTN_DOC + ycen)


def fit_ginf(truth, shp):
    """1-parameter least squares of the FROZEN shape to a given truth curve, equal weight per bin."""
    return 1.0 + float(np.dot(shp, truth - 1.0) / np.dot(shp, shp))


g_rec = fit_ginf(true_rad, shape)
true_a2 = np.array([gamma_curve(float(y), yN_a2, "alpha2", "mag") for y in ycen])
g_rec_a2 = fit_ginf(true_a2, shape)
bias_rA = g_rec - asy_rA_mag
bias_a2 = g_rec_a2 - gamma_curve(1e-6, yN_a2, "alpha2", "mag")
print(f"     Fitting the frozen shape to the TRUE Route A curve over the pipeline's own deep bins "
      f"(log10 y in [-1.5, 0.5),")
print(f"     equal weight per bin -- an APPROXIMATION, no noise MC, flagged): recovered gamma_inf "
      f"{g_rec:.4f} vs true")
print(f"     asymptote {asy_rA_mag:.4f}, bias {bias_rA:+.4f}. Same exercise at alpha=2: {bias_a2:+.4f}.")
check(abs(bias_rA) < 0.5 * (RA_POINT - 1) and abs(bias_rA) > abs(bias_a2),
      f"V5e the shape mismatch is a REAL new systematic and it is LARGER than the frozen sigma_sys allowance "
      f"of {SIG_SYS} would suggest for a single line item ({bias_rA:+.4f} vs alpha=2's {bias_a2:+.4f}), but it "
      f"is only {100*abs(bias_rA)/(RA_POINT-1):.0f}% of the Route A signal, so it degrades the front without "
      f"nullifying it. Its SIGN is what matters for scoring: the frozen estimator's alpha=1 transition scale "
      f"biases the recovered gamma_inf {'HIGH' if bias_rA > 0 else 'LOW'}, so a scorer must add it as a "
      f"declared one-sided systematic rather than discovering it afterwards. Caveat carried loudly: this is a "
      f"curve-space least squares, not the pipeline's median-per-bin profile-chi2 with its kappa nuisance; the "
      f"honest number needs the frozen MC re-run at Route A truth, which only the pipeline can do")


# ======================================================================================================
banner("V6  (d) THE HYBRID GATE S x L UNDER ROUTE A -- does the branch survive, and does the trap stay at 2?")

print("  The corpus's own committed completion shape is K_eff = 1 - S(|a|/a0) L(omega/omega_c), so the gated")
print("  boost is nu_gated = 1/(1 - S L) with S = 1 - mu the saturation and L = 1/(1 + (omega/omega_c)^2) the")
print("  one-pole gate. Under Route A the saturation has an exceptionally clean form:")
print("        S = 1 - mu = e^-u = e^-sqrt(y)      (exactly, by the kernel's own definition)")
s_check_y = yN_rA
S_direct = math.exp(-math.sqrt(s_check_y))
S_viamu = 1.0 - float(mu(float(x_of_y_routeA(s_check_y))))
print(f"  at y_extN = {s_check_y:.5f}:  e^-sqrt(y) = {S_direct:.8f}   1 - mu(x) = {S_viamu:.8f}")
# TAUTOLOGY PARTLY FIXED 2026-08-03: the conjunct `S_direct == 1 - 1/nu(y)` is the kernel definition
# rearranged and cannot fail. The round-trip S_viamu, which goes through the numerical x(y) inversion and back
# through mu, DOES test something, so that is the conjunct retained.
check(abs(S_direct - S_viamu) < 1e-9,
      f"V6a the gate's amplitude factor is identified in closed form and cross-checked two ways: "
      f"S = 1 - mu = 1 - 1/nu = e^-sqrt(y) to {abs(S_direct-S_viamu):.1e}. Route A makes the hybrid gate's "
      f"amplitude EXACTLY the kernel's Newtonian residual, which is a genuine structural simplification and "
      f"is not available in either power-law kernel")


def ReG(om, omc):
    return 1.0 / (1.0 + (om / omc) ** 2)


def Omega(M, r):
    return math.sqrt(G_N * M / r ** 3)


om10 = Omega(M_WB, 10 * KAU)
print(f"\n  a 1.5 Msun pair at 10 kAU presents Omega = {om10:.3e} rad/s, "
      f"{om10/OMC['hi']:.1f}-{om10/OMC['lo']:.1f}x above the committed omega_c window,")
print(f"  so L = {ReG(om10, OMC['hi']):.5f}-{ReG(om10, OMC['lo']):.5f}. The gate is a FREQUENCY object: Route A "
      f"changes S, never L.\n")
print(f"  {'footing':<11}{'omega_c':<6}{'nu(y_extN)':>12}{'S':>10}{'gamma_v gated':>15}"
      f"{'|gated-1|/sigma_tot':>21}{'branch gap/sigma_fit':>22}")
print("  " + "-" * 100)
gated, gaps, lin_dev = [], [], []
for fl, ge_key in (("canonical", ("canonical", "primary g_ext,obs")), ("alt", ("alt", "primary g_ext,obs"))):
    v = rA[ge_key]
    S = 1.0 - 1.0 / v["g2perp"]            # = 1 - mu = e^-sqrt(y_extN)
    for el, omc in OMC.items():
        L = ReG(om10, omc)
        # PERPENDICULAR eigenvalue: the hybrid form itself, nu_gated = 1/(1 - S L)
        g2perp_g = 1.0 / (1.0 - S * L)
        # LONGITUDINAL eigenvalue: gate its excess over Newton by the same L (no separate amplitude exists)
        g2par_g = 1.0 + (v["g2par"] - 1.0) * L
        g_gate = math.sqrt((g2par_g + 2.0 * g2perp_g) / 3.0)
        # linear-vs-nonlinear gating of the perp eigenvalue, for the record
        lin_dev.append(abs(g2perp_g - (1.0 + (v["g2perp"] - 1.0) * L)))
        gated.append(g_gate)
        gap = (v["rad"] - g_gate) / SIG_FIT_30K
        gaps.append(gap)
        print(f"  {fl:<11}{el:<6}{v['g2perp']:>12.5f}{S:>10.5f}{g_gate:>15.6f}"
              f"{abs(g_gate-1)/sig_tot_30k:>21.4f}{gap:>22.2f}")
S_ref = 1.0 - 1.0 / rA[("alt", "primary g_ext,obs")]["g2perp"]
print(f"  GATING-CONVENTION SPREAD, stated rather than buried: the hybrid form gates S (giving S L), while")
print(f"  mi_wb_gate_fork_2026.py gated the EXCESS nu - 1 = S/(1-S). The two differ by 1/(1-S) = "
      f"{1/(1-S_ref):.3f} in the excess,")
print(f"  i.e. up to {max(lin_dev):.2e} in gamma^2_perp. Both readings and all four combinations stay under "
      f"{max(max(abs(g-1) for g in gated), max(lin_dev)/3)/sig_tot_30k:.3f} sigma_tot from Newton, so the "
      f"branch's Newtonian character is convention-independent.")
gmin, gmax = min(gated), max(gated)
print(f"\n  Route A gated range {gmin:.5f}-{gmax:.5f}   (Amendment 1 registered {A1_GATED[0]}-{A1_GATED[1]} at "
      f"alpha=1; Amendment 4(h)(i) restated {A2_GATED[0]}-{A2_GATED[1]} at alpha=2)")
check(max(abs(g - 1) for g in gated) / sig_tot_30k < 0.2 and max(lin_dev) / sig_tot_30k < 0.2,
      f"V6b *** THE HYBRID S x L BRANCH SURVIVES ROUTE A, SO THE FALSIFIABILITY TRAP STAYS AT 2 ROUTES TO A "
      f"NEWTONIAN READING, NOT 1. *** At 10 kAU the gated prediction is {gmin:.5f}-{gmax:.5f}, i.e. "
      f"{max(abs(g-1) for g in gated)/sig_tot_30k:.3f} sigma_tot from Newton at worst -- observationally "
      f"Newtonian, and that holds under BOTH gating conventions (the excess-gating variant adds at most "
      f"{max(lin_dev)/3/sig_tot_30k:.3f} sigma_tot). Route A raises the gated EXCESS "
      f"{(gmax-1)/(max(A2_GATED)-1):.1f}x over the alpha=2 restatement, because S = "
      f"{1-1/rA_cp['g2perp']:.4f} instead of {1-1/a2_cp['g2perp']:.4f}, but 'still indistinguishable from "
      f"Newton' is unchanged. The locally-dragged-frame branch (gamma_v - 1 ~ 1e-6, a (v/c)^2 object) is "
      f"untouched by any kernel change, so both routes remain open and the trap count is 2")
check(min(gaps) > (A4D_POINT - 1) / SIG_FIT_30K,
      f"V6c and the FORK ITSELF becomes more decidable: the gated and ungated branches are now "
      f"{min(gaps):.1f}-{max(gaps):.1f} sigma_fit apart, against {(A4D_POINT-1)/SIG_FIT_30K:.1f} at alpha=2. "
      f"Whichever branch DR4 picks, it picks it harder")

print(f"\n  BUT -- the gated branch stops being Newtonian at the OUTER edge of the frozen 2-30 kAU window.")
print(f"  Amendment 1's cubic rise gamma_v - 1 = 1/2[nu(y_extN) - 1](omega_c^2/GM)s^3, exponent exactly 3:")
amp_rA = 0.5 * (rA_cp["g2perp"] - 1.0)
amp_a2 = 0.5 * (a2_cp["g2perp"] - 1.0)
print(f"      amplitude prefactor 1/2[nu(y_extN)-1]:  alpha=2 {amp_a2:.4f} (Amendment 7 V1b: {A2_CUBIC_AMP})"
      f"  ->  Route A {amp_rA:.4f}   ({amp_rA/amp_a2:.2f}x)")
print(f"  {'s [kAU]':>9}{'(s/r_gate)^3 lo':>17}{'gamma_v-1 routeA':>18}{'/sigma_fit':>12}"
      f"{'gamma_v-1 alpha=2':>19}{'/sigma_fit':>12}")
print("  " + "-" * 90)
cub = {}
for s_kau in (2., 10., 20., 30.):
    L = ReG(Omega(M_WB, s_kau * KAU), OMC["lo"])   # -> (s/r_gate)^3 in the Omega >> omega_c limit
    # renamed from d_rA/d_a2: those names hold the a0-degeneracy price set ~240 lines above, and reassigning
    # them here made V7(c) print 0.03 sigma_tot where the correct 1.87 belongs -- reading as a 38x FALL in a
    # price that actually RISES. Caught by adversarial verification 2026-08-03.
    cub_rA, cub_a2 = amp_rA * L, amp_a2 * L
    cub[s_kau] = cub_rA
    print(f"  {s_kau:>9.0f}{L:>17.5f}{cub_rA:>18.5f}{cub_rA/SIG_FIT_30K:>12.2f}{cub_a2:>19.5f}"
          f"{cub_a2/SIG_FIT_30K:>12.2f}")
check(cub[30.] / SIG_FIT_30K > 1.0 and cub[2.] / SIG_FIT_30K < 0.05,
      f"V6d *** A SHARPENING THAT CUTS BOTH WAYS: under Route A the GATED branch's own prediction reaches "
      f"{cub[30.]:.4f} = {cub[30.]/SIG_FIT_30K:.2f} sigma_fit by 30 kAU (alpha=2: "
      f"{amp_a2*ReG(Omega(M_WB,30*KAU),OMC['lo'])/SIG_FIT_30K:.2f} sigma_fit), while staying "
      f"{cub[2.]/SIG_FIT_30K:.3f} sigma_fit at 2 kAU. *** So the gated branch is no longer flat-Newtonian "
      f"across the frozen window: it predicts a measurable INTERNAL RISE inside it. That makes the gated "
      f"branch falsifiable WITHIN the frozen window rather than only beyond 50 kAU -- good for falsifiability "
      f"-- but it also means a flat Newtonian 2-30 kAU result no longer cleanly CONFIRMS the gated branch "
      f"either. The trap count stays 2 (V6b, evaluated where Amendment 1 evaluated it) while the trap gets "
      f"NARROWER. Caveat: the single-separation cubic ignores the pipeline's separation weighting, and the "
      f"pipeline fits one scalar over the whole window, so the recovered value would sit well below the 30 kAU "
      f"figure")


# ======================================================================================================
banner("V7  WHAT THE ROUTE A AMENDMENT MUST REGISTER (computed above; the primary agent files it)")

print(f"""  (a) THE TARGET. The ungated framework-MI wide-binary target becomes
          gamma_v = {RA_POINT:.4f}, full range {RA_LO:.4f}-{RA_HI:.4f}
      over both a0 footings x both g_ext conventions, superseding Amendment 4(d)'s {A4D_POINT}
      ({A4D_RANGE[0]}-{A4D_RANGE[1]}). Supporting rows: gamma_par {A4D_PAR} -> {rA_cp['gpar']:.4f},
      gamma_perp {A4D_PERP} -> {rA_cp['gperp']:.4f}, y_extN {A4C_YEXTN['canonical']}/{A4C_YEXTN['alt']} ->
      {rA_cp['yN']:.4f}/{rA[('alt','primary g_ext,obs')]['yN']:.4f}. Orientation-average convention spread
      {max(abs(v['mag']-v['rad']) for v in rA.values()):.4f} (radial vs magnitude), which is now larger than
      it was at alpha=1 and should be quoted rather than hidden.
      THE 'framework-as-MG' ROW MOVES TOO and Amendment 4(i) never corrected it: {FROZEN_MG} (frozen, an
      alpha=1 number) -> {MG_RA:.4f}, range {MG_LO:.4f}-{MG_HI:.4f} on the same like-for-like recomputation.
      Register both rows or neither; registering only the MI row is what creates V4c/V4d's scoring collision.

  (b) THE SCORING RULE GETS STRONGER, AND THE FRAMEWORK'S EXPOSURE GROWS WITH IT. A Newtonian 2-30 kAU
      result is evidence AGAINST at {z30_lo:.2f}-{z30_hi:.2f} sigma_tot at N = 30,000 (alpha=2: {z30_a2:.2f}).
      Amendment 6's no-re-hedging rule stands and now has the power to bite.

  (c) THREE FROZEN ITEMS MUST BE CORRECTED, ALL AGAINST INTEREST:
      * section 1.5's decision table MISLABELS the framework's own prediction. {RA_POINT:.4f} falls in the
        "{DECISION_EDGES[2]}-{DECISION_EDGES[3]} -> MG-side; MI DISFAVORED" bin, and the worst corner
        {RA_HI:.4f} is {gap_guard:.4f} below the ">{DECISION_EDGES[3]} = no verdict permitted" edge. The bands
        were drawn around a 1.09 target and are no longer fit for purpose. Re-draw them, in the open, with
        the raw gamma_hat and BOTH distances always reported (Amendment 7's rule).
      * the MI and as-MG rows COLLIDE in the frozen table: {FROZEN_MG} lies inside {RA_LO:.4f}-{RA_HI:.4f}.
        Recompute BOTH rows (as-MG -> {MG_RA:.4f}) or the table is unusable. Reported against my own framing:
        on the like-for-like recomputation the MI-vs-MG separation IMPROVES from {sep_a2:.2f} to
        {sep_ra:.2f} sigma_tot -- still under 3, so section 1.5's "likely UNDECIDABLE" stands and must NOT be
        upgraded to decidable.
      * the a0-degeneracy flag STANDS VERBATIM. Its price rises ({d_a1:.2f} -> {d_rA:.2f} sigma_tot for a
        {100*(A0_MILGROM/A0_CANON-1):.0f}% a0 change) but the framework's own footing fork spans
        {RA_HI-RA_LO:.4f} > {a0_effect:.4f}, so no DR4 outcome may be reported as measuring a0.
      * Amendment 4(e)(ii)'s "gamma_v || sub-Newtonian on all 4/4" is WITHDRAWN -- Route A gives
        {min(v['gpar'] for v in rA.values()):.4f}-{max(v['gpar'] for v in rA.values()):.4f}. The pre-declared
        PERPENDICULAR > PARALLEL anisotropy sign SURVIVES and is stronger; only the parallel eigenvalue's
        position relative to 1 flips.

  (d) THE ONE GENUINE IMPROVEMENT, and it should be registered with its own caveat attached. The
      sigma_sys = {SIG_SYS} ceiling rises from Amendment 7's {A7_CEILING} sigma to {cap_lo:.2f}-{cap_hi:.2f} sigma
      (absolute reading) or {cap_prop:.2f} sigma (signal-proportional reading), and 3 sigma needs
      N ~ {min(ns.values()):,.0f}-{n_worst:,.0f}. Section 1.5's "expected DECIDABLE", withdrawn by Amendment 7
      as stale, is RESTORABLE -- but it must be re-registered with the arithmetic and with the statement that
      the frozen N >~ {A15_N_3SIG:,} is still wrong as written. The corpus has withdrawn a DECIDABLE claim
      once; this one is stated at the CEILING (N -> infinity), not as a finite-N hope, and it is checked on
      both sigma_sys readings.

  (e) A NEW, KERNEL-CAUSED SYSTEMATIC THAT CANNOT BE FIXED BY DESIGN. The hash-stamped pipeline's estimator
      hard-codes the alpha=1 transition scale yE = {A1_YEXTN_DOC} in gamma(y) = 1 + (gamma_inf-1) yE/(yE+y);
      Route A's true scale is {yN_rA:.4f}. Fitting the frozen shape to the true curve over the pipeline's own
      deep bins biases gamma_inf by {bias_rA:+.4f} ({100*abs(bias_rA)/(RA_POINT-1):.0f}% of the signal). This must
      be registered as a DECLARED ONE-SIDED systematic before DR4, and the honest number requires the frozen
      MC re-run at Route A truth -- which only the pipeline itself can produce.

  (f) THE GATE AND THE TRAP. The hybrid S x L branch survives ({gmin:.5f}-{gmax:.5f} at 10 kAU,
      < {max(abs(g-1) for g in gated)/sig_tot_30k:.2f} sigma_tot from Newton), so the trap count STAYS AT 2.
      Route A makes S = e^-sqrt(y) exactly, raises the cubic-rise prefactor {amp_a2:.4f} -> {amp_rA:.4f}
      ({amp_rA/amp_a2:.2f}x, superseding Amendment 7 V1b's {A2_CUBIC_AMP}), and pushes the gated branch to
      {cub[30.]/SIG_FIT_30K:.2f} sigma_fit by 30 kAU -- so the frozen 2-30 kAU window is no longer a place where
      the gated branch is guaranteed Newtonian. The p = 3 exponent, the M^(1/3) knee and every falsifier of
      the gated branch are unchanged (they are omega_c objects, not kernel objects).

  (g) WHAT DOES NOT CHANGE. The a0-degeneracy flag (no DR4 outcome may be reported as measuring a0), the
      16-row cut table, the estimator, the NSS screen, the strictness ladder, Amendment 5's voiding of the
      s^TX bands, and kappa = 1/2 being FITTED not derived. a0 was an INPUT to every number above and was
      never tuned. No door is closed by this file.""")


banner("RESULT")
n = sum(1 for t, _ in ok if t)
print(f"  {n}/{len(ok)} checks held.")
if n != len(ok):
    print("\n  FAILED:")
    for t, m in ok:
        if not t:
            print(f"    - {m}")
    sys.exit(1)
print(f"  Exit 0.  ROUTE A WIDE-BINARY TARGET: gamma_v = {RA_POINT:.4f} (range {RA_LO:.4f}-{RA_HI:.4f}), "
      f"up {(RA_POINT-1)/(A4D_POINT-1):.2f}x in the observable from Amendment 4(d)'s {A4D_POINT}.")
print(f"  Newton-vs-MI: {z30_lo:.2f}-{z30_hi:.2f} sigma_tot at N=30k; ceiling {cap_lo:.2f}-{cap_hi:.2f} sigma "
      f"(absolute) / {cap_prop:.2f} sigma (proportional) -- 3 sigma REACHABLE, was {A7_CEILING}.")
print(f"  Costs: the point value lands in the frozen 'MI disfavored' bin, the frozen MG row {FROZEN_MG} now sits "
      f"INSIDE the MI range, the worst")
print(f"  corner is {gap_guard:.4f} from the no-verdict zone, gamma_par flips super-Newtonian, and the frozen "
      f"estimator's alpha=1 transition")
print(f"  scale biases gamma_inf by {bias_rA:+.4f}. MI-vs-MG stays UNDECIDABLE ({sep_ra:.2f} sigma_tot "
      f"like-for-like); the a0 flag stands.")
print(f"  Hybrid S x L gate survives at {gmin:.5f}-{gmax:.5f}; trap count stays 2.")
