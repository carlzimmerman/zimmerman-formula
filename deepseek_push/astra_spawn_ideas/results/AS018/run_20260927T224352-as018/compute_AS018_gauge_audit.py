#!/usr/bin/env python3
"""AS018 - Reference potential and gauge-independent force: bounded audit.

Bounds enforced INSIDE the process before any work: RLIMIT_CPU=120s,
RLIMIT_AS=512MB (best-effort on macOS), single-threaded (NO_*_NUM_THREADS=1,
no BLAS work above N=64 matrices), 60-digit mpmath for identity checks,
float64 for the radial-grid independent check.

Sections
  A. symbolic identities (sympy): log-potential derivative, r_ref shift,
     gauge shift, MONO deep series coefficients (Bernoulli structure).
  B. footing constants (both a0 footings separately).
  C. high-precision identity residuals (mpmath mp.diff): gauge invariance of
     g, exactness of d/dr[C ln(r/r_ref)] = C/r, re-reference = constant.
  D. deep-limit expansion of the RAR/MONO force with the ACTUAL leading
     remainder (y^3/30240; odd coefficients vanish) and log-log slope 3.
  E. MONO construction: y_p (peak of h_RAR), h_p, y* (splice), C1 join,
     max |log10(nu_mono/nu_RAR)| <= 0.0104 dex.
  F. radial-grid independent check (float64): spherical shell source,
     g_N from Green (erf) representation, Phi by quadrature and
     differentiated back (gauge & gradient-residual cross check), energy
     shift E[K]-E[0] = K*M_b, phantom-mass identity, deep/Newtonian regime
     checks with leading-term bands, v_flat approach.
  G. S operator + adjoint S* on grids: periodic (S*1=1, zero-mode),
     Dirichlet (constant NOT preserved), lapse-weighted measure
     (S*_N = N^{-1} S^T N != S; adjoint identity checked).
  H. NEGATIVE CONTROL: "potential zero = measured extra vacuum density"
     rejected: gauge scan K -> observables inert, naive density estimator
     linear in K (any alleged density 'explained' by some K), framework
     rho_Lambda K-invariant.
  I. JSON residuals dump.
"""
import os, sys, json, time, warnings
import resource
_t0 = time.time()
resource.setrlimit(resource.RLIMIT_CPU, (120, 120))
_rlim_as_note = ""
try:
    resource.setrlimit(resource.RLIMIT_AS, (512 * 1024 * 1024, 512 * 1024 * 1024))
    _rlim_as_note = "RLIMIT_AS 512MB set"
except (ValueError, OSError) as e:
    _rlim_as_note = f"RLIMIT_AS not enforceable here: {e}"
for _k in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
           "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ[_k] = "1"
warnings.filterwarnings("ignore")

import numpy as np
import sympy as sp
import mpmath as mp

mp.mp.dps = 60
G = mp.mpf("6.67430e-11")
c = mp.mpf("299792458")
M_SUN = mp.mpf("1.98847e30")
A0_CAN = mp.mpf("9.3619e-11")
A0_ALT = mp.mpf("1.1279e-10")
DELTA_MONO = mp.mpf("0.05")

OUT = []
def log(*a):
    s = " ".join(str(x) for x in a)
    OUT.append(s)
    print(s, flush=True)

log("== AS018 bounded audit; bounds: CPU<=120s (RLIMIT_CPU), AS<=512MB (%s), 1 thread ==" % _rlim_as_note)
log("mpmath dps = %d | numpy %s | sympy %s" % (mp.mp.dps, np.__version__, sp.__version__))
RES = {}

# ------------------------------------------------------------------ A. sympy
log("\n[A] symbolic identities (sympy, exact algebra)")
r, Cm, r1, r2, K = sp.symbols("r C r_ref1 r_ref2 K", positive=True, real=True)
Phi = Cm * sp.log(r / r1)
aS = {
 "d_dr_Phi_minus_C_over_r": sp.simplify(sp.diff(Phi, r) - Cm / r) == 0,
 "r_ref_shift_is_constant": sp.simplify(sp.simplify(Cm * sp.log(r / r2) - Phi) - Cm * sp.log(r1 / r2)) == 0,
 "gauge_shift_derivative_invariant": sp.simplify(sp.diff(Phi + K, r) - sp.diff(Phi, r)) == 0,
 "gauge_shift_force_still_C_over_r": sp.simplify(sp.diff(Phi + K, r) - Cm / r) == 0,
}
for k, v in aS.items():
    log("   symbolic: %-38s %s" % (k, v))
RES["A_symbolic"] = aS

# deep series f(z) = z/(1-e^{-z}) (z = sqrt y); Bernoulli structure: odd terms z^3,z^5 vanish
z = sp.symbols("z")
f_ser = sp.series(z / (1 - sp.exp(-z)), z, 0, 11).removeO()
fzP = sp.Poly(sp.expand(f_ser), z)
coefs = {int(n): sp.Rational(fzP.coeff_monomial(z**n)) for n in range(1, 9)}
aS["f_series_z8"] = str(f_ser)
aS["f_series_odd_coefs_vanish"] = bool(all(coefs[n] == 0 for n in (3, 5, 7)))
aS["coef_z4_minus_1_over_720"] = bool(coefs[4] == sp.Rational(-1, 720))
aS["coef_z6_1_over_30240"] = bool(coefs[6] == sp.Rational(1, 30240))
aS["coef_z2_1_over_12"] = bool(coefs[2] == sp.Rational(1, 12))
log("   f(z)=z/(1-e^{-z}) = %s" % f_ser)
log("   odd coefficients z^3,z^5,z^7 vanish (Bernoulli): %s ; coef(z^4)=-1/720: %s ; coef(z^6)=1/30240: %s"
    % (aS["f_series_odd_coefs_vanish"], aS["coef_z4_minus_1_over_720"], aS["coef_z6_1_over_30240"]))
RES["A_deep_series"] = {k: str(v) for k, v in aS.items() if k.startswith(("f_series", "coef"))}

# ------------------------------------------------------------- B. footings
log("\n[B] footing constants (both a0 footings, separately; M_b = M_sun)")
def foot(a0l):
    d = {"a0": a0l,
         "rho_Lambda": 4 * a0l**2 / (G * c**2),
         "C": mp.sqrt(G * M_SUN * a0l),
         "r_M": mp.sqrt(G * M_SUN / a0l),
         "v_flat": mp.sqrt(mp.sqrt(G * M_SUN * a0l))}
    d["C2_minus_v4"] = d["C"]**2 - d["v_flat"]**4
    d["rM2_minus"] = d["r_M"]**2 - G * M_SUN / a0l
    return d
foot_can, foot_alt = foot(A0_CAN), foot(A0_ALT)
for f, tag in ((foot_can, "canonical"), (foot_alt, "alternative")):
    log("   %-11s a0=% .6e rho_L=%.10e kg/m^3 C=%.10e m^2/s^2 r_M=%.10e m v_flat=%.6f m/s"
        % (tag, f["a0"], f["rho_Lambda"], f["C"], f["r_M"], f["v_flat"]))
    log("       v_flat^4 - G M a0 = % .3e ; r_M^2 - G M/a0 = % .3e" % (f["C2_minus_v4"], f["rM2_minus"]))
RES["B_footings"] = {"canonical": {k: mp.nstr(v, 16) for k, v in foot_can.items()},
                     "alternative": {k: mp.nstr(v, 16) for k, v in foot_alt.items()}}

# -------------------------------------------------------- C. identity evals
log("\n[C] high-precision identity residuals (mpmath mp.diff, 60 digits)")
rng = [mp.mpf("1e11"), mp.mpf("1e14"), foot_can["r_M"], mp.mpf("1e16"), mp.mpf("1e17")]
rrefs = [mp.mpf("1"), foot_can["r_M"] / 2, mp.mpf("1e17")]
worst = mp.mpf(0); worst_g = mp.mpf(0); wrc = mp.mpf(0)
KANY = mp.mpf("12345.678")
for rr in rng:
    for rf in rrefs:
        PhiC = lambda s, rf=rf: foot_can["C"] * mp.log(s / rf)            # noqa: E731
        PhiG = lambda s, rf=rf: foot_can["C"] * mp.log(s / rf) + KANY      # noqa: E731
        g_fd = mp.diff(PhiC, rr, 1)
        g_gd = mp.diff(PhiG, rr, 1)
        worst = max(worst, abs(g_fd - foot_can["C"] / rr) / (foot_can["C"] / rr))
        worst_g = max(worst_g, abs(g_gd - foot_can["C"] / rr) / (foot_can["C"] / rr))
        diffc = PhiC(rr) - foot_can["C"] * mp.log(rr / rrefs[0]) - foot_can["C"] * mp.log(rrefs[0] / rf)
        wrc = max(wrc, abs(diffc) / max(abs(diffc), foot_can["C"]))
log("   max rel residual  d/dr[C ln(r/r_ref)] vs C/r : % .3e" % worst)
log("   max rel residual  gauge shift Phi->Phi+K (force unchanged) : % .3e" % worst_g)
log("   max rel residual  re-reference Phi(.;r_ref)-Phi(.;r_ref0) = C ln(r_ref0/r_ref) : % .3e" % wrc)
RES["C_identity_residuals"] = {"grad_log_pot": mp.nstr(worst, 20),
                               "gauge_shift_g": mp.nstr(worst_g, 20),
                               "rereference_const": mp.nstr(wrc, 20), "dps": 60}

# ----------------------------------------------------------- D. deep limit
log("\n[D] deep expansion: g = (C/r)[1 + z/2 + y/12 - y^2/720 + y^3/30240 + O(y^5)], z=sqrt y = r_M/r")
def nu_RAR(y):
    return 1 / (1 - mp.e**(-mp.sqrt(y)))
ys = [mp.mpf(10)**(-k) for k in (1, 2, 3, 4, 5, 6, 7, 8)]
rows = []
for y in ys:
    z = mp.sqrt(y)
    q = nu_RAR(y) * z - 1
    pred = z / 2 + y / 12 - y**2 / 720
    rows.append((y, q, pred, q - pred))
log("   y          exact q=g*r/C-1      pred(q)           remainder")
for y, q, pred, rem in rows:
    log("   % .1e   % .6e   % .6e   % .3e" % (y, q, pred, rem))
xs = [float(mp.log10(y)) for y, *_ in rows[-4:]]
rl = [float(mp.log10(abs(r))) for *_, r in rows[-4:]]
sl = float(np.polyfit(xs, rl, 1)[0])
rem_small = abs(rows[-1][3]) / (rows[-1][0]**3)
log("   log-log slope of |remainder| vs y = %.4f  (expect 3.0: leading remainder y^3/30240)" % sl)
log("   remainder/y^3 at y=1e-8 = %.6e  (expect 1/30240 = 3.3069e-5)" % rem_small)
RES["D_deep_series"] = {"slope_remainder": sl,
                        "rem_over_y3_at_1e-8": mp.nstr(rem_small, 16),
                        "expected_1_over_30240": mp.nstr(1 / mp.mpf(30240), 16),
                        "series": "g = (C/r)[1 + z/2 + y/12 - y^2/720 + y^3/30240 + O(y^5)], z=sqrt(y)=r_M/r"}

# --------------------------------------------------------------- E. MONO
log("\n[E] MONO construction (framework def): h_RAR(y)=y(nu_RAR(y)-1), peak y_p, h_p, splice y*, delta=0.05")
yS = sp.symbols("y", positive=True)
nuS = 1 / (1 - sp.exp(-sp.sqrt(yS)))
hS = yS * (nuS - 1)
hpS = sp.simplify(sp.diff(hS, yS))
f_hp = sp.lambdify(yS, hpS, "mpmath")
def h_RAR_mp(yv):
    return yv * (1 / (1 - mp.e**(-mp.sqrt(yv))) - 1)
y_scan = [mp.mpf(10) ** (t / 50.0) for t in range(0, 60)]
hvals = [h_RAR_mp(yy) for yy in y_scan]
imax = int(np.argmax([float(h) for h in hvals]))
ylo, yhi = y_scan[imax - 1], y_scan[imax + 1]
y_p = mp.findroot(lambda yy: f_hp(yy), (ylo, yhi))
h_p = h_RAR_mp(y_p)
def cross(yv):
    return f_hp(yv) - DELTA_MONO * h_p / (yv + y_p)
y_star = mp.findroot(cross, (mp.mpf("2.0"), mp.mpf("2.45")))
log("   y_p    = %.8f   (landmark 2.5396; h_p = %.6f ; README saturation 's=2.540, Delta=0.6476' = same object)"
    % (y_p, h_p))
log("   y*     = %.8f   (landmark 2.3374)" % y_star)
h_lo = h_RAR_mp(y_star)
def h_mono_mp(yv):
    if yv <= y_star:
        return h_RAR_mp(yv)
    return h_lo + DELTA_MONO * h_p * mp.log((yv + y_p) / (y_star + y_p))
cont = abs(h_mono_mp(y_star + 1e-14) - h_mono_mp(y_star))
c1 = abs(f_hp(y_star) - DELTA_MONO * h_p / (y_star + y_p))
log("   h continuity at y* : % .3e ;  C^1 (|h'_RAR(y*) - floor(y*)|) : % .3e" % (cont, c1))
def nu_mono_mp(yv):
    return 1 + h_mono_mp(yv) / yv
ygr = [mp.mpf(10) ** (t / 20.0) for t in range(-20, 181)]
mxd = mp.mpf(0); mxy = None
for yv in ygr:
    ddex = abs(mp.log10(nu_mono_mp(yv) / nu_RAR(yv)))
    if ddex > mxd:
        mxd = ddex; mxy = yv
log("   max |log10(nu_mono/nu_RAR)| = %.6f dex at y=%.4f (spec bound 0.0104)" % (mxd, mxy))
RES["E_mono"] = {"y_p": mp.nstr(y_p, 16), "h_p": mp.nstr(h_p, 16),
                 "y_star": mp.nstr(y_star, 16),
                 "landmark_yp_err": mp.nstr(abs(y_p - mp.mpf("2.5396")), 8),
                 "landmark_ystar_err": mp.nstr(abs(y_star - mp.mpf("2.3374")), 8),
                 "h_cont_at_star": mp.nstr(cont, 8), "C1_at_star": mp.nstr(c1, 8),
                 "max_dex_vs_RAR": mp.nstr(mxd, 12), "max_dex_at_y": mp.nstr(mxy, 8)}

# ------------------------------------------------------------- F. grid check
log("\n[F] radial-grid independent check (float64): shell source, Green(erf) g_N, "
    "Phi by quadrature, gauge & energy checks, phantom mass, regimes")
M_b = 1.0
a0f = float(A0_CAN)
Gf = float(G)
cf = float(c)
r_Mu = float(mp.sqrt(G / a0f))
r_s = 0.1 * r_Mu
sig = 0.02 * r_Mu
N = 65536
rmin, rmax = 0.01 * r_Mu, 2000.0 * r_Mu
rg = np.geomspace(rmin, rmax, N)
from math import erf as _erf
erfv = np.vectorize(_erf)
Gauss = np.exp(-((rg - r_s) ** 2) / (2 * sig ** 2)) / (sig * np.sqrt(2 * np.pi))
M_enc = M_b * 0.5 * (1 + erfv((rg - r_s) / (sig * np.sqrt(2.0))))
gN = Gf * M_enc / rg**2
y = gN / a0f
def h_RAR_np(yv):
    w = np.sqrt(yv)
    return yv * np.exp(-w) / (1 - np.exp(-w))
y_starf, y_pf, h_pf = float(y_star), float(y_p), float(h_p)
deltaf = float(DELTA_MONO)
h_lo_f = float(h_lo)
def h_mono_np(yv):
    yv = np.asarray(yv, dtype=float)
    return np.where(yv <= y_starf, h_RAR_np(yv),
                    h_lo_f + deltaf * h_pf * np.log((yv + y_pf) / (y_starf + y_pf)))
g = gN * (1 + h_mono_np(y) / y)
C_u = float(mp.sqrt(G * a0f))
chk = {}
sel = y <= 1e-6
if sel.any():
    rdeep, ydeep = float(rg[sel][-1]), float(y[sel][-1])
    ratio = float(g[sel][-1] * rdeep / C_u)
    lead = 0.5 * np.sqrt(ydeep)
    chk["deep_g_times_r_over_C"] = ratio
    chk["deep_leading_correction_pred_1_plus"] = 1 + lead
    chk["deep_in_band"] = bool(abs(ratio - (1 + lead)) < 0.011 * lead)
seln = y >= 1e5
if seln.any():
    yn = float(y[seln][0])
    dev_formula = float(h_mono_np(np.array([yn]))[0] / yn)
    dev_direct = float(g[seln][0] / gN[seln][0] - 1.0)
    chk["newt_dev_formula"] = dev_formula
    chk["newt_dev_direct"] = dev_direct
    chk["newt_formula_matches_direct"] = bool(abs(dev_formula - dev_direct) < 1e-12 * max(1.0, abs(dev_formula)))
    chk["newt_dev_lt_1e-3"] = bool(abs(dev_direct) < 1e-3)
idx0 = int(np.argmin(np.abs(rg - r_Mu)))
dr = np.diff(rg)
cumu = np.concatenate([[0.0], np.cumsum(0.5 * (g[:-1] + g[1:]) * dr)])
Phivec = np.zeros_like(rg)
Phivec[idx0:] = -(cumu[idx0:] - cumu[idx0])
Phivec[:idx0] = (cumu[idx0] - cumu[:idx0])
K0 = 3.14159e4
K0s = 1e-9                       # gauge constant comparable to |Phi| scale (~1e-10)
PhiK = Phivec + K0
PhiKs = Phivec + K0s
grad0 = -np.gradient(Phivec, rg)
gradK = -np.gradient(PhiK, rg)
gradKs = -np.gradient(PhiKs, rg)
relg = np.abs(grad0 - g) / np.maximum(np.abs(g), 1e-30)
chk["grad_of_Phi_vs_g_max_rel"] = float(relg[2:-2].max())
# gauge invariance: mathematical identity grad(Phi) = grad(Phi + K) for every K;
# float64 test at comparable-magnitude K (rounding-free) and at gigantic K (rounding bound)
chk["gauge_grad_diff_smallK_max_abs"] = float(np.max(np.abs(grad0 - gradKs)))
dxmin = float(np.min(np.diff(rg)))
rounding_bound = 4.0 * np.finfo(float).eps * K0 / dxmin   # ~4 ulp of K0 per difference, /dx
chk["gauge_grad_diff_hugeK_max_abs"] = float(np.max(np.abs(grad0 - gradK)))
chk["hugeK_rounding_bound_pred"] = float(rounding_bound)
chk["hugeK_diff_within_rounding_bound"] = bool(chk["gauge_grad_diff_hugeK_max_abs"] <= 1.6 * rounding_bound)
dM = M_b * Gauss
E0 = float(np.trapz(dM * Phivec, rg))
EK = float(np.trapz(dM * PhiK, rg))
M_by_quad = float(np.trapz(dM, rg))
chk["E0_J"] = E0
chk["E_K_J"] = EK
chk["dE_over_dK"] = (EK - E0) / K0
chk["M_b_by_quad"] = M_by_quad
chk["energy_shift_identity_rel_err"] = abs((EK - E0) - K0 * M_by_quad) / abs(EK - E0)
chk["mass_quad_vs_exact"] = abs(M_by_quad - M_b)
Mph_formula = (a0f / Gf) * rg**2 * h_mono_np(y)
Mph_dir = (1.0 / Gf) * rg**2 * (g - gN)
relm = np.abs(Mph_formula - Mph_dir) / np.maximum(np.abs(Mph_formula), 1e-30)
chk["Mph_identity_max_rel"] = float(relm[np.isfinite(relm) & (Mph_formula != 0)].max())
if sel.any():
    v2 = float(rg[sel][-1] * g[sel][-1])
    chk["v2_minus_C_relative"] = (v2 - C_u) / C_u
    chk["v2_lead_pred_relative"] = 0.5 * np.sqrt(ydeep)
for k, v in chk.items():
    log("   %-36s %s" % (k, ("% .6e" % v) if isinstance(v, float) else v))
RES["F_grid"] = {k: (v if isinstance(v, (bool, str)) else ("%.9e" % v)) for k, v in chk.items()}

# ------------------------------------------------------------------ G. S-op
log("\n[G] S = exp[(xi^2/2) Laplacian]: periodic / Dirichlet / lapse-weighted adjoint")
cnt = 64
xif = 1.0
Lp = np.zeros((cnt, cnt))
for i in range(cnt):
    Lp[i, i] = -2.0
    Lp[i, (i + 1) % cnt] = 1.0
    Lp[i, (i - 1) % cnt] = 1.0
wl, wv = np.linalg.eigh(Lp)
Sp = (wv * np.exp((xif**2 / 2.0) * wl)) @ wv.T
ones = np.ones(cnt)
chkS = {}
chkS["S_periodic_symmetric"] = float(np.max(np.abs(Sp - Sp.T)) / np.max(np.abs(Sp)))
chkS["S_periodic_ones_eigen_max_abs"] = float(np.max(np.abs(Sp @ ones - ones)))
chkS["periodic_spectrum_min_lambda"] = float(min(wl))          # -4.0 = Nyquist mode (exact for the chain)
chkS["periodic_zero_mode_dist"] = float(min(abs(wl)))          # ~1e-15: the constant mode, eigenvalue 0
LD = np.zeros((cnt, cnt))
for i in range(cnt):
    LD[i, i] = -2.0
    if i > 0: LD[i, i - 1] = 1.0
    if i < cnt - 1: LD[i, i + 1] = 1.0
wlD, wvD = np.linalg.eigh(LD)
SD = (wvD * np.exp((xif**2 / 2.0) * wlD)) @ wvD.T
chkS["S_Dirichlet_constant_not_preserved"] = float(np.max(np.abs(SD @ ones - ones)))
chkS["Dirichlet_zero_mode_dist"] = float(min(abs(wlD)))        # >0: no constant mode in the Dirichlet domain
lam = np.linspace(0.0, 2 * np.pi, cnt, endpoint=False)
Nvec = 1.0 + 0.3 * np.sin(lam)
Nm = np.diag(Nvec); Ninv = np.diag(1.0 / Nvec)
S_Nstar = Ninv @ Sp.T @ Nm
rngn = np.random.default_rng(7)
u = rngn.standard_normal(cnt); v = rngn.standard_normal(cnt)
lhs = (Sp @ u).T @ Nm @ v
rhs = u.T @ Nm @ (S_Nstar @ v)
chkS["lapse_adjoint_identity_residual"] = float(abs(lhs - rhs) / max(abs(lhs), 1e-30))
chkS["S_star_N_minus_S_norm_ratio"] = float(np.max(np.abs(S_Nstar - Sp)) / np.max(np.abs(Sp)))
chkS["S_star_N_ne_S"] = bool(chkS["S_star_N_minus_S_norm_ratio"] > 1e-10)
for k, v in chkS.items():
    log("   %-38s %s" % (k, v))
RES["G_S_operator"] = chkS

# ------------------------------------------------- H. negative control
log("\n[H] NEGATIVE CONTROL: 'potential zero = measured extra vacuum density' -> REJECTED")
V_box = (10.0 * r_Mu)**3
Kscan = np.linspace(-1e4, 1e4, 41)
dens_vec = np.array([(Kk * M_by_quad) / (cf**2 * V_box) for Kk in Kscan])
rho_L_can = float(4 * A0_CAN**2 / (G * c**2))
rho_L_alt = float(4 * A0_ALT**2 / (G * c**2))
K_to_match = lambda rhot: float(rhot * cf**2 * V_box / M_by_quad)   # noqa: E731
Km_can, Km_alt, Km_half = K_to_match(rho_L_can), K_to_match(rho_L_alt), K_to_match(0.5 * rho_L_can)
chkH = {
 "density_estimator_slope_drho_dK_kg_m3_per_unit": float((dens_vec[-1] - dens_vec[0]) / (Kscan[-1] - Kscan[0])),
 "density_estimator_range_kg_m3": float(dens_vec[-1] - dens_vec[0]),
 "gauge_observables_inert_max_abs": chk["gauge_grad_diff_smallK_max_abs"],
 "gauge_hugeK_diff_bounded_by_rounding": chk["hugeK_diff_within_rounding_bound"],
 "contrived_K_matches_rhoL_can": Km_can,
 "contrived_K_matches_rhoL_alt": Km_alt,
 "contrived_K_matches_rhoL_half": Km_half,
 "distinct_K_needed_for_distinct_densities": bool(Km_can != Km_half and Km_alt != Km_can),
 "rho_Lambda_canonical_kg_m3": rho_L_can,
 "rho_Lambda_alt_kg_m3": rho_L_alt,
}
log("   naive rho-estimator slope d(rho)/dK = % .4e kg/m^3 per (m^2/s^2) of gauge; range over K-scan = % .4e kg/m^3"
    % (chkH["density_estimator_slope_drho_dK_kg_m3_per_unit"], chkH["density_estimator_range_kg_m3"]))
log("   contrived K matching rho_Lambda(can) = % .4e ; rho_total(alt) = % .4e ; rho_Lambda/2 = % .4e  m^2/s^2"
    % (Km_can, Km_alt, Km_half))
log("   -> ANY alleged vacuum density is 'explained' by SOME potential-zero choice, while every force/gradient"
    " observable is K-invariant (small-K gauge gradient difference = % .3e m/s^2; huge-K difference % .3e bounded by"
    " float rounding % .3e)" % (chk["gauge_grad_diff_smallK_max_abs"], chk["gauge_grad_diff_hugeK_max_abs"],
                                chk["hugeK_rounding_bound_pred"]))
log("   framework rho_Lambda (both footings) = % .6e / % .6e kg/m^3 : K-invariant, unaffected by the gauge"
    % (rho_L_can, rho_L_alt))
RES["H_negative_control"] = chkH

# ----------------------------------------------------------------------- I.
ru = resource.getrusage(resource.RUSAGE_SELF)
_rss_mb = ru.ru_maxrss / 1048576.0     # macOS ru_maxrss is in BYTES (probed: +80MB alloc -> +83.9MB delta)
RES["meta"] = {"bounds": {"RLIMIT_CPU_s": 120, "RLIMIT_AS_MB": 512,
                          "rlimit_as_note": _rlim_as_note, "threads": 1,
                          "wall_s": round(time.time() - _t0, 4),
                          "maxrss_MB": round(_rss_mb, 3),
                          "ru_maxrss_bytes": int(ru.ru_maxrss),
                          "mpmath_dps": mp.mp.dps},
               "note": "single-threaded CPython; numpy/sympy/mpmath; largest array 65536 floats"}
log("wall time %.3f s ; maxrss %.3f MB (ru_maxrss %d bytes)" % (time.time() - _t0, _rss_mb, ru.ru_maxrss))
with open("residuals.json", "w") as fh:
    json.dump(RES, fh, indent=1, default=str)
log("residuals.json written; run completed")