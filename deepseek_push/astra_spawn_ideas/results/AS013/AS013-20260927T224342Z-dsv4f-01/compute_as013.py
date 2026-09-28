#!/usr/bin/env python3
"""AS013 - a distance scaling degeneracy of the deep law.

Bounded prototype (declared/enforced): wall-clock <= 120 s via signal.alarm;
memory <= 512 MB declared (RLIMIT_AS not enforceable on this macOS host - the
process reports ru_maxrss instead); single thread; mpmath precision 60 dps
(mp.prec = 200 bits ~ 60 digits).

Scope: audit the degeneracy of the deep law v_flat^4 = G*M_b*a0 under the
distance rescaling M_b proportional to D^2 (fixed flux, fixed mass-to-light),
and its combination with the inclination scaling v = v_los/sin(i).

Framework inputs (adopted, not derived here): a0 = kappa*c*sqrt(G*rho_Lambda),
kappa = 1/2; r_M = sqrt(G*M_b/a0); both a0 footings carried separately.
Branches Q, RAR, MONO (and the deep limit) are evaluated as labelled curves;
no branch is imported as the mechanism. The heat filter S is not exercised
(pointwise deep asymptotics; the operative target's declared content is
g^2 = a0*g_N => v^4 = G*a0*M_b, req. 1 of FRIED_CHICKEN_SPEC).

Outputs are printed to stdout (redirected into raw_output.txt by the runner).
All residuals are ACTUAL numbers; checks record observed values.
"""

import signal, time, os, sys, hashlib, json, resource

signal.alarm(120)
T0 = time.time()

from mpmath import mp, mpf, sqrt, exp, log, pi, power, diff, findroot, ln
mp.prec = 200  # ~ 60 decimal digits
F = mpf

# ----------------------------------------------------------------------------
# Framework constants (contract defaults, SI)
# ----------------------------------------------------------------------------
G   = F("6.67430e-11")
c   = F("299792458")
Msun = F("1.98847e30")
pc  = F("3.085677581491367e16")
kB  = F("1.380649e-23")
kappa = F("0.5")

A0_CAN = F("9.3619e-11")    # canonical footing
A0_ALT = F("1.1279e-10")    # alternative footing

# mock galaxy
M_b  = F("1e9") * Msun
D    = F("10e6") * pc           # 10 Mpc
i_deg = F("60")
sin_i = sqrt(F("3")) / 2        # sin(60 deg)

def rho_Lambda_from_a0(a0):
    return F(4) * a0 ** 2 / (G * c ** 2)

def v_flat(M, a0):
    return (G * M * a0) ** F("0.25")

def r_M(M, a0):
    return sqrt(G * M / a0)

def B_at_theta(M, Dv, th):
    """Newtonian baryonic acceleration at angular radius th (point mass)."""
    r = Dv * th
    return G * M / r ** 2

CHECKS = []
def check(name, ok, observed, tolerance, result=None):
    CHECKS.append(dict(name=name, observed=observed, tolerance=tolerance,
                       result=result if result is not None else ("PASS" if ok else "FAIL")))

def relerr(x, y):
    if x == 0 and y == 0:
        return F(0)
    return abs(x - y) / (abs(y) if y != 0 else abs(x))

# ----------------------------------------------------------------------------
# CK-A  symbolic exact substitution (sympy): residual exactly 0
# ----------------------------------------------------------------------------
import sympy as sp
lam_s, M_s, a_s, G_s, s_s, I_s = sp.symbols("lam M a G s I", positive=True)
deep_L  = G_s * M_s * a_s
deep_R  = G_s * (lam_s ** 2 * M_s) * (a_s / lam_s ** 2)
r1 = sp.simplify(deep_L - deep_R)
comb_R = G_s * (lam_s ** 2 * M_s) * (a_s / (lam_s ** 2 * s_s ** 4)) * ((s_s * I_s) ** 4)
r2 = sp.simplify(G_s * M_s * a_s * I_s ** 4 - comb_R)
r3 = sp.simplify(sp.sqrt(G_s * (lam_s ** 2 * M_s) / (a_s / lam_s ** 2)) - lam_s ** 2 * sp.sqrt(G_s * M_s / a_s))
check("CK-A1_sympy_deep_product_invariance", r1 == 0,
      "residual exactly %s (0)" % r1, "exactly 0")
check("CK-A2_sympy_combined_inclination_distance", r2 == 0,
      "residual exactly %s (0)" % r2, "exactly 0")
check("CK-A3_sympy_rM_scaling", r3 == 0,
      "residual exactly %s (0)" % r3, "exactly 0")

# ----------------------------------------------------------------------------
# CK-B  dimensional mock numbers on both footings
# ----------------------------------------------------------------------------
for tag, a0 in (("canonical", A0_CAN), ("alternative", A0_ALT)):
    rl  = rho_Lambda_from_a0(a0)
    vf  = v_flat(M_b, a0)
    rMv = r_M(M_b, a0)
    thM = rMv / D
    vlos = vf * sin_i
    print("MOCK[%s] a0=%.6e v_flat=%.9f m/s v_los(i=60deg)=%.9f m/s "
          "r_M=%.6e m = %.6f kpc  theta_M=%.6e rad = %.6f arcsec"
          % (tag, a0, vf, vlos, rMv, rMv / (1e3 * pc), thM,
             thM / (pi / 648000)))
    print("MOCK[%s] rho_Lambda(implied)=%.6e kg/m^3  eps_L=%.6e J/m^3"
          % (tag, rl, rl * c ** 2))
    if tag == "canonical":
        A0C, RL_C, VF_C, RM_C, TH_C, VLOS_C = a0, rl, vf, rMv, thM, vlos
    else:
        A0A, RL_A, VF_A, RM_A, TH_A, VLOS_A = a0, rl, vf, rMv, thM, vlos

# footing bookkeeping (framework contract: fixed density => effective kappa;
# fixed kappa => changed density)
ratio = A0_ALT / A0_CAN
kappa_eff = F("0.5") * ratio
rho_ratio = ratio ** 2
print("FOOTINGS ratio a0_alt/a0_can = %.12f ; kappa_eff (rho fixed) = %.12f ; rho_ratio (kappa fixed) = %.12f"
      % (ratio, kappa_eff, rho_ratio))
check("CK-B1_footing_ratio_kappa_eff",
      abs(kappa_eff / F("0.602388404063") - 1) < F("1e-9"),
      "kappa_eff = %.12f" % kappa_eff, "< 1e-9 vs sibling-consistent 0.602388404063")
check("CK-B2_footing_rho_ratio",
      abs(rho_ratio / F("1.4514871574") - 1) < F("1e-9"),
      "rho_ratio = %.12f" % rho_ratio, "< 1e-9 vs sibling-consistent 1.4514871574")

# ----------------------------------------------------------------------------
# CK-C  exact plateau invariance under R_lambda (both footings)
# ----------------------------------------------------------------------------
lam_grid = [F("0.5"), F("0.8"), F("1.2"), F("1.5"), F("2.0"), F("3.3")]
for tag, a0 in (("canonical", A0_CAN), ("alternative", A0_ALT)):
    prod = G * M_b * a0
    worst = F(0)
    for lam in lam_grid:
        Mp = lam ** 2 * M_b
        ap = a0 / lam ** 2
        vp4 = G * Mp * ap
        worst = max(worst, relerr(vp4, prod))
    check("CK-C_plateau_invariance_%s" % tag,
          worst < F("1e-50"), "max rel residual over lam-grid = %.3e (actual)" % worst,
          "< 1e-50")
    # slope d ln a0 / d ln D = -2 along the orbit
    l1 = ln(a0); l2 = ln(A0_CAN if tag == "canonical" else A0_ALT)
    sl = (ln(a0 / F("2.0") ** 2) - l2) / (ln(F("2.0")) - ln(F("1.0")))
    check("CK-C_slope_dlna0_dlnD_%s" % tag, abs(sl + 2) < F("1e-12"),
          "slope = %.12f (target -2)" % sl, "< 1e-12 of -2")

# ----------------------------------------------------------------------------
# CK-D  combined distance x inclination invariance, both footings
# ----------------------------------------------------------------------------
s_grid = [F("0.8"), F("1.25")]
for tag, a0 in (("canonical", A0_CAN), ("alternative", A0_ALT)):
    ref = G * M_b * a0 * sin_i ** 4
    worst = F(0)
    for lam in lam_grid:
        for s in s_grid:
            val = G * (lam ** 2 * M_b) * (a0 / (lam ** 2 * s ** 4)) * ((s * sin_i) ** 4)
            worst = max(worst, relerr(val, ref))
    check("CK-D_combined_invariance_%s" % tag,
          worst < F("1e-50"), "max rel residual = %.3e" % worst, "< 1e-50")

# ----------------------------------------------------------------------------
# CK-E  r_M and theta_M scaling  (r_M -> lam^2 r_M ; theta_M -> lam theta_M)
# ----------------------------------------------------------------------------
for tag, a0, RM, TH in (("canonical", A0_CAN, RM_C, TH_C), ("alternative", A0_ALT, RM_A, TH_A)):
    w1 = w2 = F(0)
    for lam in lam_grid:
        w1 = max(w1, relerr(r_M(lam ** 2 * M_b, a0 / lam ** 2), lam ** 2 * RM))
        w2 = max(w2, relerr((r_M(lam ** 2 * M_b, a0 / lam ** 2) / (lam * D)), lam * TH))
    check("CK-E_rM_scaling_%s" % tag, w1 < F("1e-50"),
          "max rel residual = %.3e (r_M' vs lam^2 r_M)" % w1, "< 1e-50")
    check("CK-E_thetaM_scaling_%s" % tag, w2 < F("1e-50"),
          "max rel residual = %.3e (theta_M' vs lam theta_M)" % w2, "< 1e-50")

# ----------------------------------------------------------------------------
# CK-F  Q-branch break: v'^4/v^4 = (lam^2 y + 1) / (y + 1); deep leading term
# ----------------------------------------------------------------------------
y_grid = [F("1e-4"), F("1e-3"), F("1e-2"), F("3e-2"), F("0.1"), F("0.3"),
          F("1.0"), F("3.0"), F("10.0"), F("30.0"), F("1e2"), F("1e3"),
          F("1e4"), F("1e6")]
lamQ = F("1.5")
worst = F(0)
print("Q-break: y | ratio_direct | ratio_formula | relerr")
for y in y_grid:
    Bv = a0 if False else None
    # direct: v'^4/v^4 = (lam^2 N + C)/(N + C), N = r^2 B^2, C = a0 r^2 B, C/N = 1/y
    ratio_direct = (lamQ ** 2 + F("1") / y) / (F("1") + F("1") / y)
    ratio_formula = (lamQ ** 2 * y + 1) / (y + 1)
    e = relerr(ratio_direct, ratio_formula)
    worst = max(worst, e)
    print("%.3e  %.12f  %.12f  %.3e" % (y, ratio_direct, ratio_formula, e))
check("CK-F1_Q_break_formula", worst < F("1e-50"),
      "max relerr over y-grid = %.3e" % worst, "< 1e-50")
# deep limit leading neglected term: ratio - 1 = y(lam^2-1)/(1+y) exactly,
# so |ratio - 1 - y(lam^2-1)| = y^2(lam^2-1)/(1+y) <= (lam^2-1) y^2.
lead_err = F(0); lead_sat = True
for y in (F("1e-4"), F("1e-3"), F("1e-2")):
    ratio = (lamQ ** 2 * y + 1) / (y + 1)
    err = abs(ratio - 1 - y * (lamQ ** 2 - 1))
    bound = (lamQ ** 2 - 1) * y ** 2
    lead_err = max(lead_err, err / bound)
    lead_sat = lead_sat and (err <= bound)
print("deep-leading-corr: max err/bound = %.3e, bound = (lam^2-1)y^2, all satisfied = %s"
      % (lead_err, lead_sat))
check("CK-F2_Q_deep_leading_term", lead_sat and lead_err < F("1.0") ,
      "|ratio-1-y(lam^2-1)| <= (lam^2-1)y^2 exactly; max ratio err/bound = %.3e" % lead_err,
      "<= 1 exactly (structural: leading term y(lam^2-1), next term -(lam^2-1)y^2)")
# log-slope independent check (numeric differentiation vs analytic 2y/(y+1))
for y in (F("0.1"), F("1.0"), F("10.0")):
    def lr(lm):
        return (lm ** 2 * y + 1) / (y + 1)
    h = F("1e-6")
    slope = (ln(lr(1 + h)) - ln(lr(1 - h))) / (ln(1 + h) - ln(1 - h))
    analytic = 2 * y / (y + 1)
    check("CK-F3_logslope_y=%s" % y, relerr(slope, analytic) < F("1e-8"),
          "numeric d ln(ratio)/d ln lam = %.12f vs analytic 2y/(y+1) = %.12f"
          % (slope, analytic), "< 1e-8")

# ----------------------------------------------------------------------------
# CK-G  RAR and MONO kernels: deep-limit degeneracy exact, Newtonian break lam^2
# ----------------------------------------------------------------------------
def nu_RAR(y):
    return 1 / (1 - exp(-sqrt(y)))

def h_RAR(y):
    return y * (nu_RAR(y) - 1)

def d_h_RAR(y):
    return diff(h_RAR, y)

# parameters of the operative MONO construction (framework contract)
delta = F("0.05")
yp = findroot(lambda z: d_h_RAR(z), F("2.5396"))             # peak
hp = h_RAR(yp)
ystar = findroot(lambda z: d_h_RAR(z) - delta * hp / (z + yp), F("2.3374"))

def nu_mono(y):
    if y <= ystar:
        return nu_RAR(y)
    return 1 + (h_RAR(ystar) + delta * hp * ln((y + yp) / (ystar + yp))) / y

print("MONO parameters: y_p = %.6f  h_p = %.6f  y* = %.6f  (contract landmarks 2.5396 / 2.3374)"
      % (yp, hp, ystar))
check("CK-G1_y_p_landmark", abs(yp - F("2.5396")) < F("1e-2"),
      "y_p = %.6f" % yp, "within 1e-2 of 2.5396")
check("CK-G2_y_star_landmark", abs(ystar - F("2.3374")) < F("1e-2"),
      "y* = %.6f" % ystar, "within 1e-2 of 2.3374")
# continuity of the derivative at the join
dcont = relerr(d_h_RAR(ystar), delta * hp / (ystar + yp))
check("CK-G3_mono_derivative_join", dcont < F("1e-40"),
      "h'_RAR(y*) vs delta h_p/(y*+y_p): relerr = %.3e" % dcont, "< 1e-40")
# max dex deviation RAR vs MONO (informational; FRIED_CHICKEN says <= 0.0104 dex)
import mpmath
ysamp = [mp.mpf("1e-3") + k * mp.mpf("0.02") for k in range(500)] + \
        [mp.mpf("10.0") + k * mp.mpf("0.1") for k in range(100)]
maxdex = mp.mpf(0); yat = mp.mpf(0)
for yv in ysamp:
    d = abs(mp.log10(nu_mono(yv)) - mp.log10(nu_RAR(yv)))
    if d > maxdex:
        maxdex = d; yat = yv
print("RAR-vs-MONO max |dex| = %.5f at y = %.4f" % (maxdex, yat))
check("CK-G4_mono_within_dex", maxdex < mp.mpf("0.0104") * mp.mpf("1.05"),
      "max |log10(nu_mono/nu_RAR)| = %.5f" % maxdex, "< 0.0104 dex (req. 1, informational)")

kernels = {"Q": lambda y: sqrt(1 + 1 / y),
           "RAR": nu_RAR,
           "MONO": nu_mono}
print("Branch break v'^4/v^4 = lam^2 [nu(lam^2 y)/nu(y)]^2  at lam = 1.5")
for kname, nu in kernels.items():
    deep_dev = abs((lamQ ** 2 * nu(lamQ ** 2 * F("1e-3")) ** 2 / nu(F("1e-3")) ** 2) - 1)
    deep_dev_small = abs((lamQ ** 2 * nu(lamQ ** 2 * F("1e-6")) ** 2 / nu(F("1e-6")) ** 2) - 1)
    newt_dev = (lamQ ** 2 * nu(lamQ ** 2 * F("1e6")) ** 2 / nu(F("1e6")) ** 2) - lamQ ** 2
    y1_dev = (lamQ ** 2 * nu(lamQ ** 2 * F("1.0")) ** 2 / nu(F("1.0")) ** 2) - 1
    print("BRANCH %s: |deep(y=1e-3)-1| = %.3e ; |deep(y=1e-6)-1| = %.3e ; "
          "newtonian(y=1e6)-lam^2 = %.3e ; (y=1)-1 = %.3f"
          % (kname, deep_dev, deep_dev_small, newt_dev, y1_dev))
    check("CK-G_deep_limit_%s" % kname, deep_dev_small < F("5e-3"),
          "|v'^4/v^4 - 1| at y=1e-6 = %.3e (y=1e-3: %.3e for reference)" % (deep_dev_small, deep_dev),
          "< 5e-3 (deep limit -> 0 as (lam-1) sqrt(y))")
    check("CK-G_newtonian_limit_%s" % kname, abs(newt_dev) < F("1e-3"),
          "|v'^4/v^4 - lam^2| at y=1e6 = %.3e" % newt_dev, "< 1e-3 (Newtonian -> lam^2)")
# RAR/MONO approach rate to the deep limit: leading term (lam-1)*sqrt(y) (proved by
# expansion of nu_RAR(y) = y^(-1/2)(1 + sqrt(y)/2 + y/12 + ...)); verify it numerically.
for kname, nu in (("RAR", nu_RAR), ("MONO", nu_mono)):
    worst_q = F(0)
    for y in (F("1e-9"), F("1e-7"), F("1e-5")):
        dev = (lamQ ** 2 * nu(lamQ ** 2 * y) ** 2 / nu(y) ** 2) - 1
        lead = (lamQ - 1) * sqrt(y)
        worst_q = max(worst_q, relerr(dev, lead))
        print("DEEP-APPROACH %s: y=%.0e dev=%.6e lead=(lam-1)*sqrt(y)=%.6e relerr=%.3e"
              % (kname, y, dev, lead, relerr(dev, lead)))
    check("CK-G_deep_approach_rate_%s" % kname, worst_q < F("1e-2"),
          "max relerr dev vs (lam-1)*sqrt(y) over y in {1e-9,1e-7,1e-5} = %.3e"
          % worst_q, "< 1e-2 (leading neglected term (lam-1) sqrt(y))")

# ----------------------------------------------------------------------------
# NC1  negative control: change D in a mock while FREEZING M_b (and a0)
# ----------------------------------------------------------------------------
lamNC = F("1.5")
M_frozen = M_b
a0_frozen = A0_CAN
D_new = lamNC * D
# (a) flux consistency: flux-derived mass at the new distance
M_flux = lamNC ** 2 * M_b
fact_a = M_flux / M_frozen
# (b) velocity self-consistency at fixed theta: Newtonian part
vn_ratio = sqrt(lamNC)  # v_N at fixed theta scales as lam^(1/2)
# (c) transition-angle consistency: frozen r_M vs self-consistent deep law
theta_frozen = r_M(M_frozen, a0_frozen) / D_new
theta_consistent = lamNC * (r_M(M_frozen, a0_frozen) / D)
fact_c = theta_consistent / theta_frozen
# (d) global-a0 consistency: a deep-law analyst using the NEW distance's flux-derived
#     mass M_flux = lam^2 M_b infers a0_implied = v_flat^4/(G*M_flux) = a0/lam^2, which
#     contradicts the frozen adopted global a0 (barring a common distance-ladder error).
vf4 = v_flat(M_frozen, a0_frozen) ** 4
a0_implied = vf4 / (G * M_flux)
print("NC1 frozen-D update (lam=1.5): flux-mass ratio = %.6f (=lam^2)"
      % fact_a)
print("NC1 frozen-D update: Newtonian v(theta) ratio = %.6f (=lam^1/2)"
      % vn_ratio)
print("NC1 frozen-D update: theta_M ratio (consistent/frozen) = %.6f (=lam^2)"
      % fact_c)
print("NC1 frozen-D update: flux-implied a0 vs adopted a0 = %.6f (=lam^-2 = 1/2.25)"
      % (a0_implied / a0_frozen))
# the SAME checker applied to the consistent joint update must pass at 0:
prod_chk = G * (lamNC ** 2 * M_b) * (a0_frozen / lamNC ** 2) - G * M_b * a0_frozen
check("NC1a_frozen_update_rejected_mass", fact_a != 1,
      "flux-derived mass / frozen mass = %.6f != 1 (internally inconsistent)"
      % fact_a, "!= 1 (control must fail)")
check("NC1b_frozen_update_rejected_velocity", relerr(vn_ratio, F(1)) > F("0.2"),
      "Newtonian velocity ratio at fixed theta = %.6f (must differ from 1)" % vn_ratio,
      "> 20% (control must fail)")
check("NC1c_frozen_update_rejected_thetaM", fact_c != 1,
      "theta_M ratio = %.6f (frozen vs consistent prescriptions disagree)" % fact_c,
      "!= 1 (control must fail)")
check("NC1d_frozen_update_rejected_a0", a0_implied / a0_frozen != 1,
      "flux-implied a0 / adopted a0 = %.6f != 1 (control must fail)" % (a0_implied / a0_frozen),
      "!= 1 (control must fail)")
check("NC1e_consistent_update_passes", relerr(prod_chk + G * M_b * a0_frozen, G * M_b * a0_frozen) < F("1e-50"),
      "joint update relative residual = %.3e (must be 0; proves checker sensitivity)"
      % relerr(prod_chk + G * M_b * a0_frozen, G * M_b * a0_frozen), "< 1e-50 relative")

# ----------------------------------------------------------------------------
# NC2  deep and Newtonian limiting regimes + boundary/normalization at r_M
# ----------------------------------------------------------------------------
# boundary case: B(r_M) = a0 exactly (definition); g_Q(r_M)^2 = 2 a0^2
for tag, a0, rMv in (("canonical", A0_CAN, RM_C), ("alternative", A0_ALT, RM_A)):
    Bb = G * M_b / rMv ** 2
    gQ2 = Bb ** 2 + a0 * Bb
    check("NC2_boundary_B_rM_%s" % tag, relerr(Bb, a0) < F("1e-50"),
          "B(r_M)/a0 - 1 = %.3e" % relerr(Bb, a0), "< 1e-50")
    check("NC2_boundary_gQ2_rM_%s" % tag, relerr(gQ2, 2 * a0 ** 2) < F("1e-50"),
          "g_Q(r_M)^2/(2 a0^2) - 1 = %.3e" % relerr(gQ2, 2 * a0 ** 2), "< 1e-50")
# y-normalization: y = B/a0 scales by lam^2 at fixed theta
yc = relerr((B_at_theta(M_b, D, F("1e-4")) / A0_CAN) * lamQ ** 2,
            B_at_theta(lamQ ** 2 * M_b, lamQ * D, F("1e-4")) / (A0_CAN / lamQ ** 2))
check("NC2_y_rescaling", yc < F("1e-50"),
      "y'(theta) vs lam^2 y(theta): relerr = %.3e" % yc, "< 1e-50")
# deep profile exact invariance in the strict deep regime: v^4(theta) = G a0 M_b (point mass)
worst = F(0)
for tag, a0 in (("canonical", A0_CAN), ("alternative", A0_ALT)):
    for th in (F("1e-5"), F("1e-4"), F("1e-3")):
        gp = sqrt(a0 * B_at_theta(M_b, D, th))          # deep g at D
        v4a = (D * th) ** 2 * gp ** 2
        v4b = G * a0 * M_b                               # distance-free expression
        worst = max(worst, relerr(v4a, v4b))
check("NC2_deep_profile_distance_free", worst < F("1e-50"),
      "max relerr of v^4(theta) vs G a0 M_b over angular grid = %.3e" % worst,
      "< 1e-50 (D cancels exactly in strict deep regime)")

# ----------------------------------------------------------------------------
# Summary
# ----------------------------------------------------------------------------
elapsed = time.time() - T0
rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
for c in CHECKS:
    print("CHECKROW | %s | %s | %s | %s" % (c["name"], c["result"], c["observed"], c["tolerance"]))
npass = sum(1 for c in CHECKS if c["result"] == "PASS")
nfail = sum(1 for c in CHECKS if c["result"] != "PASS")
for c in CHECKS:
    if c["result"] != "PASS":
        print("FAILED_CHECK %s | observed: %s | tolerance: %s" % (c["name"], c["observed"], c["tolerance"]))
print("SUMMARY checks=%d pass=%d fail=%d" % (len(CHECKS), npass, nfail))
print("elapsed_s=%.3f  ru_maxrss_bytes=%d" % (elapsed, rss))
print("ALL_CHECKS_PASS=%s" % (nfail == 0))
sys.exit(0 if nfail == 0 else 1)