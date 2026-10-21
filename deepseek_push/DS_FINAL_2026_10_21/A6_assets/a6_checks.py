#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
A6_assets -- verify and weaponise the four distinctive assets of the framework.

  (1) THE SADDLE NO-GO.  Solve the exact static law for two equal point masses,
      g = g_N + u with u^2 = g_N (a0 - u)  <=>  g_N = g^2/(g+a0),
      on the axis and in the pancake, and compute the cold-energy density
          rho_cold = -div(g - g_N)/(4 pi G)      [convention: div g = -4 pi G rho]
      in units of the cosmic mean cold density rho_bar_c = Omega_c rho_crit.
      Then the column through the saddle, its negative part and its net, in
      Msun/pc^2, and the survey size needed.

  (2) THE EXACT LAW IDENTITY.  sympy: the law <=> nu = 1/2 + sqrt(4a0+g_N)/(2 sqrt g_N);
      within mu = x/(1+x)^p the exact Newtonian limit forces p = 1 (unique);
      the "smallest constant anomaly" selection is shown to be empty.

  (3) THE TWO FOOTINGS.  a0_alt/a0_can = 1.2073 stated, 1.2093 = 1/sqrt(Omega_L)
      from the defining relation; both footings are the same formula with
      rho = rho_Lambda or rho = rho_crit.  Nothing internal picks one.

  (4) THE CAPACITY.  lim_{g_N->inf} (g - g_N) = a0 (canonical) and a0/2 (n=2);
      max fractional circular-speed difference at fixed (M_b, r) is
      sqrt(2/sqrt3) - 1 = 7.457%, attained at g_N = a0/2.

Usage:  python3 a6_checks.py [--mutate]
Exit code 0 iff every declared check passes.
"""
import sys, json, math
import numpy as np

try:
    import sympy as sp
except Exception:                                   # pragma: no cover
    sp = None

if sp is not None:
    a, y, x, p, gN = sp.symbols("a y x p gN", positive=True)
    _roots = sp.solve(sp.Eq(gN, x**2 / (x + a)), x)
    gpos = _roots[-1]                                # the branch that -> +infinity with gN


_MUTARGS = [a for a in sys.argv[1:] if a.startswith("--mutate")]
MUTATE = bool(_MUTARGS)
# MUTATION 1 (default): flip the sign convention of rho_cold -- the one silent error
# that would erase the whole no-go (it turns the negative pancake positive).
# MUTATION 2 (--mutate=nu): switch off the cold sector (nu = 1, pure Newton).
MUT_MODE = "nu" if any("nu" in a for a in _MUTARGS) else "sign"
SIGN = -1.0 if (MUTATE and MUT_MODE == "sign") else +1.0

# ----------------------------------------------------------------- constants
c      = 2.99792458e8
G      = 6.67430e-11
Msun   = 1.98892e30
pc     = 3.0856775814913673e16
kpc    = 3.0856775814913673e19
Mpc    = 3.0856775814913673e22
H0     = 2.1843e-18
Lambda = 1.0890e-52
a0_can = 9.36e-11
a0_alt = 1.13e-10
kappa  = 0.5
a0     = a0_can            # working scale for the saddle solve
Om_b_h2 = 0.02237          # Planck 2018 TT,TE,EE+lowE+lensing (external)
h_hub   = 0.674            # BRIEF H0 / 100
Om_c_over_b = 5.364        # Zenodo 23533323, stated measured ratio

rho_crit = 3.0 * H0**2 / (8.0 * math.pi * G)
rho_Lam  = Lambda * c**2 / (8.0 * math.pi * G)
Om_b     = Om_b_h2 / h_hub**2
rho_bar_c = Om_c_over_b * Om_b * rho_crit          # cosmic mean cold density
U_DENS = Msun / pc**3                              # kg/m3 per Msun/pc3
U_SIG  = Msun / pc**2                              # kg/m2 per Msun/pc2

RESULTS = {"lane": "A6_assets", "status": "", "checks": [], "numbers": {},
           "constants_used": []}
CHECKS = []


def ck(cid, ok, value, threshold, note=""):
    CHECKS.append({"id": cid, "pass": bool(ok), "value": value,
                   "threshold": threshold, "note": note})
    print("%-5s %s %-46s %s" % (cid, "PASS" if ok else "FAIL", str(value), str(threshold)))
    if note:
        print("      " + note)


def info(msg):
    print("      " + msg)


def _trap(yv, xv):
    """np.trapz, renamed np.trapezoid in numpy 2.0."""
    f = getattr(np, "trapezoid", None)
    return (f(yv, xv) if f is not None else np.trapz(yv, xv))


# ------------------------------------------------------------- interpolation
def nu(y):
    """canonical nu(y) = (1+sqrt(1+4/y))/2, y = g_N/a0 > 0."""
    if MUTATE and MUT_MODE == "nu":
        return np.ones_like(np.asarray(y, dtype=float))
    return 0.5 * (1.0 + np.sqrt(1.0 + 4.0 / y))


def dnu(y):
    if MUTATE and MUT_MODE == "nu":
        return np.zeros_like(np.asarray(y, dtype=float))
    return -1.0 / (y * y * np.sqrt(1.0 + 4.0 / y))


def rho_cold(M, d, X, Y, Z):
    """Exact QUMOND cold density of two equal point masses at (-d/2,0,0),(+d/2,0,0).

    u = (nu-1) g_N ; div g_N = 0 away from the sources, so
        div u = (nu'(y)/a0) (g_N . T . g_N)/|g_N| ,  T_ij = d_i g_N,j (traceless)
    and rho_cold = -div u /(4 pi G).  No grid, no finite differences: exact.
    """
    gx = np.zeros_like(X); gy = np.zeros_like(X); gz = np.zeros_like(X)
    Txx = np.zeros_like(X); Txy = np.zeros_like(X); Txz = np.zeros_like(X)
    Tyy = np.zeros_like(X); Tyz = np.zeros_like(X); Tzz = np.zeros_like(X)
    for xc in (-0.5 * d, 0.5 * d):
        dx = X - xc; dy = Y; dz = Z
        r2 = dx * dx + dy * dy + dz * dz
        r = np.sqrt(r2); r3 = r**3; r5 = r**5
        gx += -G * M * dx / r3; gy += -G * M * dy / r3; gz += -G * M * dz / r3
        Txx += -G * M * (1.0 / r3 - 3.0 * dx * dx / r5)
        Txy += -G * M * (-3.0 * dx * dy / r5)
        Txz += -G * M * (-3.0 * dx * dz / r5)
        Tyy += -G * M * (1.0 / r3 - 3.0 * dy * dy / r5)
        Tyz += -G * M * (-3.0 * dy * dz / r5)
        Tzz += -G * M * (1.0 / r3 - 3.0 * dz * dz / r5)
    s = np.sqrt(gx * gx + gy * gy + gz * gz)
    gTg = ((Txx * gx + Txy * gy + Txz * gz) * gx
           + (Txy * gx + Tyy * gy + Tyz * gz) * gy
           + (Txz * gx + Tyz * gy + Tzz * gz) * gz)
    return SIGN * (-1.0) * ((dnu(s / a0) / a0) * gTg / s) / (4.0 * math.pi * G), s


def uvec(M, d, X, Y, Z):
    """u = (nu(|g_N|/a0)-1) g_N , computed by finite differences from g_N only."""
    gx = np.zeros_like(X); gy = np.zeros_like(X); gz = np.zeros_like(X)
    for xc in (-0.5 * d, 0.5 * d):
        dx = X - xc; r3 = (dx * dx + Y * Y + Z * Z)**1.5
        gx += -G * M * dx / r3; gy += -G * M * Y / r3; gz += -G * M * Z / r3
    s = np.sqrt(gx * gx + gy * gy + gz * gz)
    f = nu(s / a0) - 1.0
    return f * gx, f * gy, f * gz


def rho_cold_fd(M, d, x0, y0, z0, h):
    """Independent brute-force divergence of u on a 3-point stencil, with the
    physical sign hard-coded (rho = -div u/(4 pi G)); used to validate the analytic form."""
    xs = np.array([x0 - h, x0, x0 + h])
    ys = np.array([y0 - h, y0, y0 + h])
    zs = np.array([z0 - h, z0, z0 + h])
    X, Y, Z = np.meshgrid(xs, ys, zs, indexing="ij")
    ux, uy, uz = uvec(M, d, X, Y, Z)
    div = ((ux[2, 1, 1] - ux[0, 1, 1])
           + (uy[1, 2, 1] - uy[1, 0, 1])
           + (uz[1, 1, 2] - uz[1, 1, 0])) / (2.0 * h)
    return -div / (4.0 * math.pi * G)


def column(M, d, phi=math.pi / 2, Lf=1.0, n=160001):
    """Column along a straight line through the saddle at angle phi to the pair axis,
    integrated over +-Lf*d.  Returns (net, neg, pos) in kg/m2."""
    t = np.linspace(-Lf * d, Lf * d, n) + 1e-7 * d
    X = t * math.cos(phi); Y = t * math.sin(phi)
    r, _ = rho_cold(M, d, X, Y, np.zeros_like(X))
    ok = np.isfinite(r)
    net = _trap(r[ok], t[ok])
    neg = _trap(np.minimum(r[ok], 0.0), t[ok])
    pos = _trap(np.maximum(r[ok], 0.0), t[ok])
    return net, neg, pos


def rho_at(M, d, frac, where="pancake"):
    """rho_cold at R = frac*d from the saddle, in the pancake (perp. bisector plane)
    or on the axis."""
    if where == "pancake":
        X, Y, Z = np.array([0.0]), np.array([frac * d]), np.array([0.0])
    else:
        X, Y, Z = np.array([frac * d]), np.array([0.0]), np.array([0.0])
    r, s = rho_cold(M, d, X, Y, Z)
    return float(r[0]), float(s[0])


# =========================================================== 1. SADDLE NO-GO
print("=" * 108)
print("1. THE SADDLE NO-GO -- exact static law for two equal point masses")
print("=" * 108)

MW_M, MW_D = 1.4e11 * Msun, 780.0 * kpc        # a Milky-Way-M31-like pair
CL_M, CL_D = 1.0e15 * Msun, 11.6 * Mpc         # the separation that gives the -33

# --- K1: the analytic density equals an independent finite-difference divergence
errs = []
for (xf, yf) in ((0.20, 0.0), (0.0, 0.20), (0.30, 0.10), (0.10, 0.45), (0.0, 0.70), (0.60, 0.0)):
    x0, y0 = xf * MW_D, yf * MW_D
    ra, _ = rho_cold(MW_M, MW_D, np.array([x0]), np.array([y0]), np.array([0.0]))
    rf = rho_cold_fd(MW_M, MW_D, x0, y0, 0.0, 1e-4 * MW_D)
    errs.append(abs(rf / ra[0] - 1.0) if ra[0] else float("inf"))
ck("K1", max(errs) < 1e-4,
   "max rel err %.2e" % max(errs), "< 1e-4",
   "analytic div[(nu-1)g_N] vs central-difference divergence of u at 6 points; the "
   "exact form is algebraic, so this is a validation of the algebra, not a convergence")

rho_panc, g_panc = rho_at(MW_M, MW_D, 0.2, "pancake")
rho_axis, g_axis = rho_at(MW_M, MW_D, 0.2, "axis")

# --- K2: sign structure -- negative in the pancake, positive on the axis
ck("K2", (rho_panc < 0.0 < rho_axis),
   "rho_panc/rho_axis = %+.4f" % ((rho_panc / rho_axis) if rho_axis else float("nan")), "< 0",
   "at R=0.2d: rho_panc = %+.4e kg/m3 (gN/a0=%.2e), rho_axis = %+.4e kg/m3; the "
   "negative region is the pancake through the saddle" % (rho_panc, g_panc / a0_can, rho_axis))

# --- K3: the -89 number, in units of the cosmic mean cold density
ratio_mw = rho_panc / rho_bar_c
ck("K3", abs(ratio_mw / (-89.0) - 1.0) < 0.15,
   "%.1f" % ratio_mw, "-89 +-15%",
   "MW-M31-like (M_b=1.4e11 each, d=780 kpc), rho_bar_c = %.3e kg/m3 = Omega_c rho_crit" % rho_bar_c)

# --- K4: the -33 for a cluster pair -- only at a wide separation
def ratio_at(M, d):
    return rho_at(M, d, 0.2, "pancake")[0] / rho_bar_c

lo, hi = 1.0 * Mpc, 30.0 * Mpc                     # ratio is monotone in d
for _ in range(60):
    mid = 0.5 * (lo + hi)
    if abs(ratio_at(CL_M, mid)) > 33.0:
        lo = mid
    else:
        hi = mid
d33 = 0.5 * (lo + hi)
ratio_cl = ratio_at(CL_M, d33)
ratio_cl3 = ratio_at(CL_M, 3.0 * Mpc)
ck("K4", (abs(ratio_cl / (-33.0) - 1.0) < 0.02) and (d33 > 8.0 * Mpc),
   "d(-33)=%.1f Mpc, rho(3Mpc)=%.0f" % (d33 / Mpc, ratio_cl3), "d(-33) > 8 Mpc",
   "a 1e15 Msun pair needs %.1f Mpc (unbound, supercluster scale) to give -33; the "
   "bound 3 Mpc pair gives %.0f" % (d33 / Mpc, ratio_cl3))

# --- K4b: the note's two CLUSTER numbers are jointly reproduced only by a group-mass pair
GM_M, GM_D = 4.2e12 * Msun, 3.0 * Mpc
gm_ratio = ratio_at(GM_M, GM_D)
gm_net, gm_neg, gm_pos = column(GM_M, GM_D, math.pi / 2, 1.0)
ck("K4b", abs(gm_ratio / (-33.0) - 1.0) < 0.10 and 4.6 < abs(gm_neg / U_SIG) < 5.5,
   "ratio %.1f, col_neg %.2f Msun/pc2" % (gm_ratio, gm_neg / U_SIG),
   "-33 +-10% and 4.63 - 5.5",
   "(M_b = 4.2e12 each, i.e. a 1e14 halo at f_b=0.04, d = 3 Mpc) reproduces BOTH "
   "quoted cluster numbers at once; a "
   "1e15 cluster pair cannot (it needs %.1f Mpc for the density ratio and then its "
   "column is far deeper)" % (d33 / Mpc))

# --- K5: the depth scale of the pancake column (negative part), Msun/pc2
net_mw, neg_mw, pos_mw = column(MW_M, MW_D, math.pi / 2, 1.0)
neg_mw_s = neg_mw / U_SIG
ck("K5", 1.4 < abs(neg_mw_s) < 4.2,
   "%.2f Msun/pc2" % neg_mw_s, "1.4 - 4.2 (claim 1.9-2.1)",
   "negative part of the column through the saddle, line of sight in the pancake plane, "
   "|L|<d; the exact 3D value is %.1fx the quoted 1.9-2.1" % (abs(neg_mw_s) / 2.0))

# --- K6: the net column is NEGATIVE (refutes the note's +0.016 net positive)
net_mw_s = net_mw / U_SIG
ck("K6", net_mw_s < 0.0,
   "%.2f Msun/pc2 (net/|neg| = %.2f)" % (net_mw_s, net_mw / abs(neg_mw)),
   "net < 0 (note says +0.016, ratio 0.078)",
   "the exact solution's saddle column is net negative: the law itself predicts a "
   "shallow negative convergence, it is not 'neither picture predicts one'")

info("line-of-sight dependence of the saddle column (MW pair, |L|<d), phi from the pair axis")
info("(phi=0 is the axis through the point masses: that column is source-dominated, not cold energy):")
info("   phi    net [Msun/pc2]   neg part   net/|neg|")
ANG = {}
for deg in (0, 60, 70, 75, 80, 85, 90):
    n_, g_, p_ = column(MW_M, MW_D, math.radians(deg), 1.0)
    r_ = (n_ / abs(g_)) if g_ != 0 else float("nan")
    ANG[deg] = [n_ / U_SIG, g_ / U_SIG, r_]
    info("  %3d   %+12.2f   %+10.2f   %8s" % (deg, n_ / U_SIG, g_ / U_SIG,
                                              ("%+.3f" % r_) if g_ != 0 else "   --"))
_lo, _hi = math.radians(75.0), math.radians(80.0)
for _ in range(50):
    _mid = 0.5 * (_lo + _hi)
    if column(MW_M, MW_D, _mid, 1.0)[0] > 0.0:
        _lo = _mid
    else:
        _hi = _mid
PHI0 = math.degrees(0.5 * (_lo + _hi))
_n0, _g0, _p0 = column(MW_M, MW_D, 0.5 * (_lo + _hi), 1.0)
info("  the net column passes through zero at phi = %.2f deg (net=%+.3f, neg part=%+.3f "
     "Msun/pc2)," % (PHI0, _n0 / U_SIG, _g0 / U_SIG))
info("  so the quoted -0.206/+0.016 (ratio -0.078) is a line-of-sight artefact within a "
     "degree of that zero,")
info("  not a property of the solution: at the physical phi = 90 deg the net is %.2f Msun/pc2."
     % (net_mw_s if 'net_mw_s' in dir() else -2.42))

# --- K7: r^{-1/2} cusp at the null (the engine of the no-go)
vals = []
for f in (0.002, 0.005, 0.010, 0.020):
    r, _ = rho_at(MW_M, MW_D, f, "pancake")
    vals.append(abs(r) * math.sqrt(f * MW_D))
spread = (max(vals) - min(vals)) / min(vals) if min(vals) > 0 else float("inf")
ck("K7", spread < 0.02, "spread %.3f%%" % (100 * spread), "< 2%",
   "|rho| sqrt(r) constant along the pancake: the density diverges as r^-1/2 at the "
   "null point, so no smooth positive medium can match it")

# --- K8: geometry of the negative region (solid-angle fraction, half-width)
th = np.linspace(0.0, math.pi, 3601)
R0 = 0.2 * MW_D
rr, _ = rho_cold(MW_M, MW_D, R0 * np.cos(th), R0 * np.sin(th), np.zeros_like(th))
frac = float(np.sum(np.sin(th)[rr < 0]) / np.sum(np.sin(th)))
cross = [math.degrees(th[i]) for i in range(1, len(th)) if np.sign(rr[i]) != np.sign(rr[i - 1])]
half_width = 0.5 * (cross[1] - cross[0]) if len(cross) >= 2 else float("nan")
_width = (cross[1] - cross[0]) if len(cross) >= 2 else float("nan")
ck("K8", 0.05 < frac < 0.40, "solid-angle fraction %.3f" % frac, "0.05 - 0.40",
   "negative band at R=0.2d spans %.1f deg about the perpendicular plane (=%.1f deg "
   "half-width): a thin pancake" % (_width, half_width))

# --- K9: survey size for a 3-sigma detection of the missing depth
n_src_arcmin2 = 10.0          # background sources per arcmin^2 (lensing depth, external)
sigma_eps = 0.3               # intrinsic shape noise (external)
Sigma_crit = 3000.0           # Msun/pc2 at z_lens ~ 0.3 (external)
ap_arcmin = 1.5
N_src = n_src_arcmin2 * math.pi * ap_arcmin**2
sigma_pair = sigma_eps * Sigma_crit / math.sqrt(N_src)
depth = abs(neg_mw_s)
N3 = (3.0 * sigma_pair / depth)**2
N_pub = 700.0                 # order of the close-pair stack of arXiv:1702.08485 (external)
ck("K9", 8.0 < N3 / N_pub < 18.0,
   "N(3sig)=%.2e pairs, %.1fx a %.0f-pair stack" % (N3, N3 / N_pub, N_pub),
   "multiple in 8 - 18 (claim ~12)",
   "sigma(DeltaSigma) per pair = %.0f Msun/pc2 in a %.1f arcmin aperture, against a "
   "depth of %.1f Msun/pc2" % (sigma_pair, ap_arcmin, depth))

# --- numbers for the report
NUM = {}
NUM["config_MW_Mb_each_Msun"] = MW_M / Msun
NUM["config_MW_d_kpc"] = MW_D / kpc
NUM["config_cluster_Mb_each_Msun"] = CL_M / Msun
NUM["rho_crit"] = rho_crit
NUM["rho_Lambda"] = rho_Lam
NUM["Omega_b"] = Om_b
NUM["Omega_Lambda"] = rho_Lam / rho_crit
NUM["a0_can"] = a0_can
NUM["a0_alt"] = a0_alt
NUM["rho_star_MW"] = math.sqrt(a0_can * G * MW_M) / (4 * math.pi * G * MW_D**2)
NUM["rho_bar_cold"] = rho_bar_c
NUM["rho_panc_0.2d_MW"] = rho_panc
NUM["rho_axis_0.2d_MW"] = rho_axis
NUM["ratio_panc_over_rbarc_MW"] = ratio_mw
NUM["ratio_panc_over_rbarc_cluster_3Mpc"] = ratio_cl3
NUM["ratio_panc_over_rbarc_cluster_11.6Mpc"] = ratio_cl
NUM["d_for_minus33_Mpc"] = d33 / Mpc
NUM["col_neg_MW_Msun_pc2"] = neg_mw_s
NUM["missing_depth_MW_Msun_pc2"] = abs(neg_mw_s)
NUM["pancake_solid_angle_percent"] = 100.0 * frac
NUM["kill_pairs_threshold"] = 1.0e5
NUM["col_net_MW_Msun_pc2"] = net_mw_s
NUM["col_pos_MW_Msun_pc2"] = pos_mw / U_SIG
NUM["col_neg_cluster_3Mpc"] = column(CL_M, 3.0 * Mpc, math.pi / 2, 1.0)[1] / U_SIG
NUM["col_neg_cluster_d33"] = column(CL_M, d33, math.pi / 2, 1.0)[1] / U_SIG
NUM["pancake_solid_angle_fraction"] = frac
NUM["pancake_half_width_deg"] = half_width
NUM["survey_N3"] = N3
NUM["survey_multiple"] = N3 / N_pub
NUM["survey_N3_at_depth2"] = (3.0 * sigma_pair / 2.0)**2
NUM["delta_kappa_MW"] = depth / Sigma_crit
NUM["sensitivity_Mb_each_Msun"] = [1.0e11, 1.4e11, 1.5e11]
NUM["ratio_panc_MW_M1.0e11"] = ratio_at(1.0e11 * Msun, MW_D)
NUM["ratio_panc_MW_M1.5e11"] = ratio_at(1.5e11 * Msun, MW_D)
NUM["ratio_panc_MW_d700kpc"] = ratio_at(MW_M, 700.0 * kpc)
NUM["angle_scan"] = {str(k): v for k, v in ANG.items()}
NUM["phi_zero_crossing_deg"] = PHI0
NUM["col_neg_at_phi0_Msun_pc2"] = _g0 / U_SIG
NUM["quoted_from_note"] = {"ratio_MW": -89, "ratio_cluster": -33, "col_neg_part": -0.206,
                           "col_net": 0.016, "net_over_neg": -0.078,
                           "depth_MW_Msun_pc2": [1.9, 2.1], "depth_cluster_Msun_pc2": [4.6, 5.1],
                           "survey_multiple": 12, "max_dV_percent": 7.46}
# RAR log-slope at the knee: a measurable discriminator between the two laws
def _gcan(yy):
    return 0.5 * yy * (1.0 + np.sqrt(1.0 + 4.0 / yy))
def _gn2(yy):
    return np.sqrt(yy * yy + yy)
_h = 1e-6
NUM["rar_slope_knee_canon"] = float(1.0 / _gcan(1.0) * (_gcan(1 + _h) - _gcan(1 - _h)) / (2 * _h))
NUM["rar_slope_knee_n2"] = float(1.0 / _gn2(1.0) * (_gn2(1 + _h) - _gn2(1 - _h)) / (2 * _h))
NUM["rar_slope_diff_percent"] = 100.0 * (0.75 - 0.723606797749979) / 0.723606797749979
NUM["rar_slope_knee_canon_exact"] = float((0.5 * (1 + np.sqrt(5)) - 1 / np.sqrt(5)) / (0.5 * (1 + np.sqrt(5))))

# group-mass pair that reproduces BOTH cluster numbers (values from K4b)
NUM["group_ratio"] = gm_ratio
NUM["group_col_neg_Msun_pc2"] = gm_neg / U_SIG
NUM["group_missing_depth_Msun_pc2"] = abs(gm_neg / U_SIG)
NUM["group_Mb_each_Msun"] = GM_M / Msun
NUM["group_d_Mpc"] = GM_D / Mpc

# convergence of the column with the integration length
NUM["col_neg_vs_L"] = {}
for L in (1.0, 2.0, 4.0, 8.0):
    _, g_, _ = column(MW_M, MW_D, math.pi / 2, L)
    NUM["col_neg_vs_L"]["L=%gd" % L] = g_ / U_SIG

# ====================================================== 2. THE EXACT LAW IDENTITY
print()
print("=" * 108)
print("2. THE EXACT LAW IDENTITY")
print("=" * 108)

if sp is None:
    ck("K10", False, "sympy missing", "sympy import", "")
else:
    a, y, x, p = sp.symbols("a y x p", positive=True)
    gN = sp.symbols("gN", positive=True)
    roots = sp.solve(sp.Eq(gN, x**2 / (x + a)), x)
    gpos = [r for r in roots if r.subs({a: 1.0, gN: 1.0}) > 0][0]
    nu_expr = sp.simplify(gpos / gN)
    target = sp.Rational(1, 2) + sp.sqrt(4 * a + gN) / (2 * sp.sqrt(gN))
    resid = sp.simplify(nu_expr - target)
    u_check = sp.simplify(gpos - (gN + (-gN + sp.sqrt(gN**2 + 4 * a * gN)) / 2))
    ck("K10", resid == 0 and u_check == 0,
       "residual %s / %s" % (resid, u_check), "== 0",
       "g_N = g^2/(g+a0)  <=>  nu = 1/2 + sqrt(4a0+g_N)/(2 sqrt g_N)  <=>  "
       "u^2 = g_N(a0-u), u = g-g_N")

    # exact Newtonian limit inside mu = x/(1+x)^p
    lims = {}
    for pp in (sp.Rational(1, 2), sp.Integer(1), sp.Rational(3, 2), sp.Integer(2)):
        yy = x**2 / (1 + x)**pp
        lims[str(pp)] = sp.limit(yy / x, x, sp.oo)
    gdeep = {}
    for pp in (sp.Rational(1, 2), sp.Integer(1), sp.Rational(3, 2), sp.Integer(2)):
        yy = x**2 / (1 + x)**pp
        gdeep[str(pp)] = sp.limit(yy / x**2, x, 0)
    ok_newton = (lims["1"] == 1) and (lims["3/2"] == 0) and (lims["1/2"] == sp.oo)
    ck("K11", ok_newton,
       "y/x -> {1/2:oo, 1:1, 3/2:0, 2:0}", "only p=1 gives 1",
       "exact Newtonian limit selects p=1; p<1 gives g>>g_N, p>1 gives g<<g_N, so the "
       "family has exactly one admissible member")

    ck("K12", all(v == 1 for v in gdeep.values()),
       "y/x^2 -> " + str(gdeep), "all 1",
       "the deep-MOND geometric mean holds for every p: it is not the selector, so "
       "(i)+(ii) leave p free and only (i) pins it")

    # constant strong-field anomaly
    nu_c = sp.simplify(gpos / gN)
    eps = sp.symbols("eps", positive=True)
    ser = sp.series(nu_c.subs(gN, a / eps), eps, 0, 2)
    coef = sp.limit((nu_c.subs(gN, a / eps) - 1) / eps, eps, 0)
    nu2 = sp.sqrt(1 + a / gN)
    coef2 = sp.limit((nu2 - 1) * gN / a, gN, sp.oo)
    ck("K13", coef == 1 and coef2 == sp.Rational(1, 2),
       "c_canon=%s c_n2=%s" % (coef, coef2), "1 and 1/2",
       "(nu-1)g_N -> a0 (canonical) and a0/2 (n=2): the strong-field anomaly is a "
       "CONSTANT acceleration, not a decaying one")

    # "smallest anomaly" is empty: in mu = x/(1+x^p)^(1/p) both limits hold for all p
    # p=1:  y = x^2/(1+x)      -> nu-1 ~ 1/y     -> y(nu-1) -> 1
    # p=2:  y = x^2/sqrt(1+x^2) -> nu-1 ~ 1/(2y^2) -> y(nu-1) -> 0
    yv = sp.symbols("yv", positive=True)
    nu_p1 = sp.Rational(1, 2) + sp.sqrt(4 + yv) / (2 * sp.sqrt(yv))
    nu_p2 = sp.sqrt((yv**2 + yv * sp.sqrt(yv**2 + 4)) / 2) / yv
    c1 = sp.limit(yv * (nu_p1 - 1), yv, sp.oo)
    c2 = sp.limit(yv * (nu_p2 - 1), yv, sp.oo)
    ck("K14", c1 == 1 and c2 == 0,
       "c(p=1)=%s, c(p=2)=%s" % (c1, c2), "c(1) > c(2)",
       "REFUTATION: in the wider family mu = x/(1+x^p)^(1/p), which keeps both limits "
       "for every p, the constant anomaly is a0 at p=1 and ZERO for p>1 -- the canonical "
       "law has the LARGEST constant anomaly, not the smallest")

# ========================================================== 3. THE TWO FOOTINGS
print()
print("=" * 108)
print("3. THE TWO-FOOTING STRUCTURE")
print("=" * 108)
ratio_foot = a0_alt / a0_can
ck("K15", abs(ratio_foot - 1.207) < 1e-3,
   "%.6f" % ratio_foot, "1.207 +-0.001",
   "a0_alt/a0_can from the two stated footings; the two differ by 20.7%")
Om_Lam = rho_Lam / rho_crit
cosmo_ratio = 1.0 / math.sqrt(Om_Lam)
ck("K16", abs(ratio_foot - cosmo_ratio) < 0.005,
   "1/sqrt(Omega_L) = %.5f" % cosmo_ratio, "within 0.005 of 1.207",
   "the ratio IS sqrt(rho_crit/rho_Lambda) = 1/sqrt(Omega_Lambda) = %.4f; the 0.14%% "
   "gap is the rounding of the two quoted a0 values" % cosmo_ratio)
a0_from_L = kappa * c * math.sqrt(G * rho_Lam)
a0_from_c = kappa * c * math.sqrt(G * rho_crit)
ck("K17", abs(a0_from_L / a0_can - 1) < 0.01 and abs(a0_from_c / a0_alt - 1) < 0.01,
   "%.4e / %.4e" % (a0_from_L, a0_from_c), "within 1% of 9.36e-11 / 1.13e-10",
   "both footings are a0 = (c/2)sqrt(G rho) with rho = rho_Lambda or rho_crit: one "
   "equation, two roots; no internal relation contains both densities in a way that picks one")
NUM["footing_ratio"] = ratio_foot
NUM["footing_ratio_cosmo"] = cosmo_ratio
NUM["a0_from_rho_Lambda"] = a0_from_L
NUM["a0_from_rho_crit"] = a0_from_c

# ============================================================== 4. THE CAPACITY
print()
print("=" * 108)
print("4. THE CAPACITY STATEMENT")
print("=" * 108)
if sp is not None:
    cap1 = sp.limit(gpos - gN, gN, sp.oo)
    g2 = sp.sqrt(gN**2 + a * gN)
    cap2 = sp.limit(g2 - gN, gN, sp.oo)
    ck("K18", cap1 == a and cap2 == a / 2, "a0=%s, a0/2=%s" % (cap1, cap2), "a0 and a0/2",
       "lim (g-g_N) is the saturation value of u = K|P|: the canonical medium saturates "
       "at a0, the n=2 law at a0/2 -- an exact statement about the saturation scale")

    yy = sp.symbols("yy", positive=True)
    g1y = (yy / 2) * (1 + sp.sqrt(1 + 4 / yy))
    g2y = sp.sqrt(yy**2 + yy)
    rat = sp.simplify(g1y / g2y)
    crit = sp.solve(sp.diff(rat, yy), yy)
    at = sp.simplify(rat.subs(yy, sp.Rational(1, 2)))
    vmax = float(sp.sqrt(at) - 1)
    ck("K19", (crit == [sp.Rational(1, 2)]) and abs(vmax - 0.0745699) < 1e-6,
       "max dV/V = %.6f at gN/a0=1/2" % vmax, "0.0745699 (=sqrt(2/sqrt3)-1)",
       "at fixed (M_b, r): V^2 ~ g, so dV/V = sqrt(g1/g2)-1, maximal at g_N = a0/2 "
       "with g1/g2 = 2/sqrt3 exactly")

    # it is a maximum, and it is a0-independent
    yv = np.linspace(0.05, 20, 400001)
    rr_ = np.sqrt(((yv / 2) * (1 + np.sqrt(1 + 4 / yv)) / np.sqrt(yv**2 + yv)))
    dvv = rr_ - 1.0
    imax = int(np.argmax(dvv))
    # a0-independence: rescale a0 -> the same curve in y
    ck("K20", abs(dvv[imax] - vmax) < 1e-4 and yv[imax] > 0.45 and yv[imax] < 0.55,
       "grid max %.6f at y=%.3f" % (dvv[imax], yv[imax]), "0.074569 +-1e-4 at y~0.5",
       "the maximum is a pure number: it contains no a0, so both footings give 7.457%. "
       "It is the exact size of the 20%-band's observational signature")
    NUM["capacity_canon"] = float(cap1.subs(a, 1))
    NUM["capacity_n2"] = float(cap2.subs(a, 1))
    NUM["max_dV_over_V"] = vmax
    NUM["max_dV_at_y"] = 0.5
    _yv = np.array([0.1, 0.5, 1.0, 2.0])
    _g1 = 0.5 * _yv * (1.0 + np.sqrt(1.0 + 4.0 / _yv))
    _g2 = np.sqrt(_yv * _yv + _yv)
    NUM["dV_at_y"] = {str(a): float(b - 1.0) for a, b in zip(_yv, np.sqrt(_g1 / _g2))}
    NUM["dV_percent_at_y"] = {str(a): float(100.0 * (b - 1.0)) for a, b in zip(_yv, np.sqrt(_g1 / _g2))}
else:
    NUM["max_dV_over_V"] = 0.0745699

# --------------------------------------------------------------------- output
n_pass = sum(1 for c in CHECKS if c["pass"])
n_tot = len(CHECKS)
NUM["n_checks"] = n_tot
NUM["n_pass"] = n_pass
RESULTS["checks"] = CHECKS
RESULTS["numbers"] = NUM
RESULTS["status"] = ("NO-GO(positive-mass medium) + NUMERICAL(reproduced: -89; "
                     "refuted: cluster -33/column pair, net-column sign, 'smallest anomaly')")
RESULTS["constants_used"] = [
    "c = 2.99792458e8 m/s (BRIEF)",
    "G = 6.67430e-11 (BRIEF)",
    "H0 = 2.1843e-18 s^-1 (BRIEF)",
    "Lambda = 1.0890e-52 m^-2 (BRIEF)",
    "a0_can = 9.36e-11 m/s^2 (BRIEF)",
    "a0_alt = 1.13e-10 m/s^2 (BRIEF)",
    "kappa = 1/2 (BRIEF)",
    "M_sun = 1.98892e30 kg, pc = 3.0856775814913673e16 m (BRIEF)",
    "Omega_b h^2 = 0.02237 (Planck 2018, external)",
    "h = 0.674 (BRIEF H0/100)",
    "Omega_c/Omega_b = 5.364 (Zenodo 23533323, stated measured)",
    "n_src = 10 arcmin^-2, sigma_eps = 0.3, Sigma_crit = 3000 Msun/pc^2 (survey forecast, external)",
    "N_pub = 700 pairs (order of the close-pair stack of arXiv:1702.08485, external)",
]
OUTJSON = ("a6_results_MUTATED_%s.json" % MUT_MODE) if MUTATE else "a6_results.json"
def _clean(o):
    if isinstance(o, float) and not math.isfinite(o):
        return None
    if isinstance(o, dict):
        return {k: _clean(v) for k, v in o.items()}
    if isinstance(o, list):
        return [_clean(v) for v in o]
    return o

RESULTS = _clean(RESULTS)
with open(OUTJSON, "w") as f:
    json.dump(RESULTS, f, indent=1, sort_keys=False, allow_nan=False)

if MUTATE:
    print("\n*** MUTATION ACTIVE (%s): %s ***" % (MUT_MODE, "nu = 1 (no cold sector)" if MUT_MODE == "nu" else "rho_cold sign flipped"))
print("\nA6 COMPLETE: %d/%d checks PASS." % (n_pass, n_tot))
sys.exit(0 if n_pass == n_tot else 1)
