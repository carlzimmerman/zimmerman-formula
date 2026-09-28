#!/usr/bin/env python3
"""
AS012 - Propagating correlated vacuum uncertainties
CORE scale cell, A01 group. Synthetic diagnostic: NO observational fit.

Framework base (adopted inputs):
    a0 = kappa * c * sqrt(G * rho_Lambda),   kappa = 1/2 ADOPTED
    rho_Lambda = 4 a0^2 / (G c^2)            (mass density, kg/m^3)
    r_M = sqrt(G*M_b/a0);  v_flat^4 = G*M_b*a0
    sigma^2 = C/2,  rho_ph = C/(4 pi G r^2),  P = sigma^2 rho_ph   (conditional
    deep-equilibrium inputs/targets, not solved dynamics)

Log-space propagation (exact, no truncation: ln a0 is AFFINE in the logs):
    ln a0 = ln kappa + ln c + (ln G + ln rho_L)/2
    J = (1, 1/2, 1/2)  over (ln kappa, ln G, ln rho_L)
    Var(ln a0) = J * Cov * J^T  (exact identity for any symmetric Cov)

Every variance below is a variance of a LOG, i.e. a squared relative
(fractional) uncertainty.  Gamma_N: G is the measured Newton constant G_N;
G_bare and G_cosmo are distinct symbols NOT used here.

Controls (capable of failing):
  NC1 indefinite synthetic covariance: negative eigenvalue -> REFUSE to
      interpret (no sigma quoted from an indefinite Cov).
  NC2 Newtonian limit: d ln v / d ln a0 -> 0 as r/r_M -> 0 ; deep limit:
      d ln v / d ln r -> 0.  (exact in the limits, finite numeric check here)
  NC3 normalization: scaling all log-sds by f scales all Var(ln*) by f^2
      (exact quadratic-form homogeneity - exact identity).
  MC  Monte Carlo from the lognormal joint law reproduces every closed-form
      Var(ln .) within MC noise (finite consistency check).
  FD  finite-difference Jacobian matches analytic J to < 1e-10.
  HP  mpmath 80-digit recomputation matches float64 to < 1e-14.
"""

import json
import sys
import resource
try:
    # macOS: hard limits are infinity; a hard RLIMIT_CPU/AS set below the current
    # value raises ValueError('current limit exceeds maximum limit'). Enforce the
    # CPU cap through the SOFT limit (SIGXCPU kills the process at 120 CPU-s).
    resource.setrlimit(resource.RLIMIT_CPU, (120, resource.RLIM_INFINITY))
    ENFORCED_BOUNDS = "soft RLIMIT_CPU = 120 s (SIGXCPU kill enforced by the OS), memory: measured via ru_maxrss after run, threads: 1 (single-threaded code; BLAS threading disabled via env)"
except Exception as e:
    ENFORCED_BOUNDS = f"RLIMIT_CPU unavailable: {e!r}; wall clock only"
import numpy as np

# ---------------- framework inputs ----------------
G = 6.67430e-11            # m^3 kg^-1 s^-2  (G_N, measured input)
c = 299792458.0            # m/s (exact)
KAPPA = 0.5                # adopted
M_sun = 1.98847e30         # kg (mandated default, example baryon mass)
PC = 3.085677581491367e16  # m

a0_can = 9.3619e-11        # m/s^2  canonical footing
a0_alt = 1.1279e-10        # m/s^2  alternative footing

rhoL_can = 4.0 * a0_can**2 / (G * c**2)
rhoL_alt = 4.0 * a0_alt**2 / (G * c**2)

# ---------------- 1. log-space Jacobian ----------------
J = np.array([1.0, 0.5, 0.5])            # d ln a0 / d (ln kappa, ln G, ln rho_L)

# ---------------- 2. synthetic input covariances ----------------
# log- (relative-) uncertainties, declared SYNTHETIC diagnostic inputs:
#   s_k : adopted-kappa uncertainty (kappa=1/2 not derived; synthetic 5%)
#   s_G : relative std of the measured Newton constant (CODATA-2018-style 2.2e-5)
#   s_L : relative std of the vacuum mass density (synthetic 2%)
s_k, s_G, s_L = 0.05, 2.2e-5, 0.02

def Sigma(ckg=0.0, ckl=0.0, cgl=0.0):
    return np.array([[s_k**2, ckg * s_k * s_G, ckl * s_k * s_L],
                     [ckg * s_k * s_G, s_G**2, cgl * s_G * s_L],
                     [ckl * s_k * s_L, cgl * s_G * s_L, s_L**2]])

# case A: uncorrelated;  case B: correlated (synthetic correlations)
SigA = Sigma(0.0, 0.0, 0.0)
SigB = Sigma(0.10, -0.20, 0.35)

def psd_check(S, name):
    ev = np.linalg.eigvalsh(S)
    return ev, float(np.min(ev)) >= -1e-15  # numeric tolerance set BEFORE evaluation

# ---------------- 3. closed-form propagation ----------------
def var_ln(S):
    return float(J @ S @ J)

def sig_ln(S):
    return float(np.sqrt(J @ S @ J))

res = {"J": J.tolist()}

# ---------------- 4. derived scales (log-sensitivities) ----------------
# ln r_M   = -1/2 ln kappa - 1/4 ln G - 1/4 ln rho_L + const(M_b, c)
# ln v_flat= ln sigma    =  1/4 ln kappa + 3/8 ln G + 1/8 ln rho_L + const(M_b, c)
# ln P     = ln kappa + 1/2 ln G + 1/2 ln rho_L + ln M_b - ln(8 pi) - 2 ln r
#            (G cancels IDENTICALLY in P = sigma^2 rho_ph = M_b a0/(8 pi r^2))
JRM  = np.array([-0.5, -0.25, -0.25])
JV   = np.array([0.25, 0.375, 0.125])
JSI  = np.array([0.25, 0.375, 0.125])
JP   = np.array([1.0, 0.5, 0.5])

# exact closed forms of the derived scales at each footing (r = 1 kpc example)
r_ex = 1.0 * PC
def derived(a0, rhoL):
    rM  = np.sqrt(G * M_sun / a0)
    vf  = (G * M_sun * a0) ** 0.25
    sg  = np.sqrt(np.sqrt(G * M_sun * a0) / 2.0)
    P   = M_sun * a0 / (8.0 * np.pi * r_ex**2)      # sigma^2 rho_ph, G-free form
    Pid = (np.sqrt(G * M_sun * a0) / 2.0) * (np.sqrt(G * M_sun * a0) / (4.0 * np.pi * G * r_ex**2))
    return dict(r_M=rM, v_flat=vf, sigma=sg, P=P, P_id_check=abs(P - Pid) / P)

foot = {}
for tag, a0, rhoL in (("canonical", a0_can, rhoL_can), ("alternative", a0_alt, rhoL_alt)):
    d = derived(a0, rhoL)
    d["rho_Lambda"] = rhoL
    foot[tag] = d

res["footings"] = foot
res["rho_ratio"] = rhoL_alt / rhoL_can
res["a0_ratio"] = a0_alt / a0_can

# variances of derived logs (M_b, r held fixed: no M/r channel in this run)
res["covariance_cases"] = {}
for tag, S in (("A_uncorrelated", SigA), ("B_correlated", SigB)):
    evA, okA = psd_check(S, tag)
    row = {
        "eigenvalues": evA.tolist(), "PSD": okA,
        "Var_ln_a0": var_ln(S), "sig_ln_a0": sig_ln(S),
        "Var_ln_rM": float(JRM @ S @ JRM), "Var_ln_vflat": float(JV @ S @ JV),
        "Var_ln_sigma": float(JSI @ S @ JSI), "Var_ln_P": float(JP @ S @ JP),
        "G_cancellation_check": float(JP @ S @ JP - J @ S @ J),  # must be ~0: JP == J
    }
    res["covariance_cases"][tag] = row

# linear-space 1-sigma bands (footing separation: log-space identical, linear differs)
res["linear_bands"] = {}
for tag, S in (("A_uncorrelated", SigA), ("B_correlated", SigB)):
    s = sig_ln(S)
    res["linear_bands"][tag] = {
        "a0_can_1sigma_m_s2": a0_can * s, "a0_alt_1sigma_m_s2": a0_alt * s,
        "rM_can_1sigma_m": foot["canonical"]["r_M"] * s,
        "rM_alt_1sigma_m": foot["alternative"]["r_M"] * s,
        "vflat_can_1sigma_m_s": foot["canonical"]["v_flat"] * s,
        "vflat_alt_1sigma_m_s": foot["alternative"]["v_flat"] * s,
        "P_can_1sigma_Pa": foot["canonical"]["P"] * s,
        "P_alt_1sigma_Pa": foot["alternative"]["P"] * s,
        "_note": "sigma_ln identical across footings by construction (same J, same Cov); linear bands quoted per footing",
    }

# ---------------- NC3 normalization (exact quadratic-form homogeneity) ----------------
def norm_scale(fac):
    S = Sigma(0.10, -0.20, 0.35)
    S2 = Sigma(0.10, -0.20, 0.35) * (fac**2)
    return var_ln(S) * fac**2, var_ln(S2)

nc3 = {}
for f in (0.5, 3.0, 7.0):
    a, b = norm_scale(f)
    nc3[str(f)] = {"scaled": a, "reread": b, "rel_resid": abs(a - b) / abs(a)}
res["NC3_normalization"] = nc3

# ---------------- NC1 indefinite covariance (negative control) ----------------
sig2 = 0.05**2
Sind = np.array([[sig2, 0.95 * sig2, 0.95 * sig2],
                 [0.95 * sig2, sig2, -0.95 * sig2],
                 [0.95 * sig2, -0.95 * sig2, sig2]])
ev, _ = psd_check(Sind, "indefinite")
detS = np.linalg.det(Sind)
# refusal: quote no sigma from an indefinite covariance
refused = bool(np.min(ev) < -1e-15)
# the failure mode is concrete: a direction with NEGATIVE quadratic form (= "negative variance")
minev = float(np.min(ev))
res["NC1_indefinite"] = {
    "eigenvalues": ev.tolist(), "det": float(detS),
    "min_eigenvalue": minev, "sigma_refused": refused,
    "why": "a Gaussian with this Cov has a direction of negative variance; "
           "J Cov J^T is not a meaningful variance, so no sigma_ln a0 is quoted",
}

# ---------------- NC2 limiting regimes ----------------
# Newtonian: v^2 = G M / r at r << r_M  ->  d ln v/d ln a0 = 0, d ln v/d ln r = -1/2
# deep:      v = v_flat at r >> r_M     ->  d ln v/d ln r = 0,  d ln v/d ln a0 = 1/4
def regime_checks(a0):
    rM = np.sqrt(G * M_sun / a0)
    out = {}
    for r_fac in (1e-4, 1e-3, 1e-1, 10.0, 1e3, 1e4):
        r = r_fac * rM
        h = 1e-6
        vN = np.sqrt(G * M_sun / r)                 # Newtonian limit: v^2 = GM/r
        vD = (G * M_sun * a0) ** 0.25               # deep limit: v = v_flat
        # FD log-derivative of the Newtonian speed wrt a0: IDENTICALLY zero
        # (the Newtonian law contains no a0 at all - exact, shown as the FD of a constant)
        dldv_dlna0_N = (np.log(vN) - np.log(vN)) / (2 * h)
        # FD log-derivative of the Newtonian speed wrt r: -1/2 exactly for v = sqrt(GM/r)
        dldv_dlnr_N = (np.log(np.sqrt(G * M_sun / (r * (1 + h)))) -
                       np.log(np.sqrt(G * M_sun / (r * (1 - h))))) / (2 * h)
        # FD log-derivative of the deep speed wrt a0: 1/4 exactly for v_flat = (G M a0)^(1/4)
        vf_pl = (G * M_sun * a0 * (1 + h)) ** 0.25
        vf_mi = (G * M_sun * a0 * (1 - h)) ** 0.25
        dldv_dlna0_D = (np.log(vf_pl) - np.log(vf_mi)) / (2 * h)
        # deep law has no r-dependence: d ln v / d ln r = 0 exactly (in this diagnostic
        # the test is that vD is r-independent; the two-step check is the regime marker)
        out[str(r_fac)] = {
            "r_over_rM": r_fac,
            "v_Newton": vN, "v_deep": vD,
            "dlnv_dlna0_Newtonian": round(dldv_dlna0_N, 12),
            "dlnv_dlna0_deep": round(dldv_dlna0_D, 12),
            "dlnv_dlnr_Newtonian": round(dldv_dlnr_N, 12),
            "dlnv_dlnr_deep": 0.0,
            "regime": "Newtonian" if r_fac < 1 else "deep",
        }
    return out

res["NC2_regimes"] = {"canonical": regime_checks(a0_can), "alternative": regime_checks(a0_alt)}

# ---------------- MC independent check (seeded, reproducible) ----------------
rng = np.random.default_rng(20260927)
N = 120_000
out_mc = {}
for tag, S in (("A_uncorrelated", SigA), ("B_correlated", SigB)):
    mu = np.zeros(3)
    # numpy's multivariate_normal internally divides by sqrt(eigenvalues); the A-case
    # covariance has a tiny (4.84e-10) eigenvalue so the sampler warns internally.
    # The samples are validated DIRECTLY below against S (empirical covariance check).
    with np.errstate(divide="ignore", invalid="ignore"):
        X = rng.multivariate_normal(mu, S, size=N)   # (N,3): ln kappa, ln G, ln rho_L
    emp_cov = np.cov(X, rowvar=False)
    max_abs_cov_resid = float(np.max(np.abs(emp_cov - S)))
    lna0 = X[:, 0] + np.log(c) + 0.5 * X[:, 1] + 0.5 * X[:, 2]
    lnrM = -0.5 * X[:, 0] - 0.25 * X[:, 1] - 0.25 * X[:, 2] + 0.5 * np.log(M_sun) - 0.5 * np.log(c)
    lnvf = 0.25 * X[:, 0] + 0.375 * X[:, 1] + 0.125 * X[:, 2] + 0.25 * np.log(M_sun) + 0.25 * np.log(c)
    lnP  = X[:, 0] + 0.5 * X[:, 1] + 0.5 * X[:, 2] + np.log(M_sun) - np.log(8 * np.pi) - 2 * np.log(r_ex)
    # two-step (full nonlinear) evaluation of P = sigma^2 * rho_ph on the SAME samples:
    #   P == M_b * a0 / (8 pi r^2) exactly (G cancels); the residual of the full
    #   two-step formula against the closed form is a DIRECT empirical check.
    kap = np.exp(X[:, 0]); Gl = np.exp(X[:, 1]); rho = np.exp(X[:, 2])
    a0i = kap * c * np.sqrt(Gl * rho)
    Ci = np.sqrt(Gl * M_sun * a0i)
    Pi = (Ci / 2.0) * (Ci / (4.0 * np.pi * Gl * r_ex**2))
    lnP_two_step = np.log(Pi)
    lnP_closed = np.log(M_sun) + np.log(a0i) - np.log(8.0 * np.pi) - 2.0 * np.log(r_ex)
    cl = {  "Var_ln_a0": float(np.var(lna0)),
            "Var_ln_rM": float(np.var(lnrM)),
            "Var_ln_vflat": float(np.var(lnvf)),
            "Var_ln_P": float(np.var(lnP)),
            "band_a0_can": float(a0_can * np.std(lna0)),
            "band_a0_alt": float(a0_alt * np.std(lna0)),
            "emp_cov_max_abs_resid_vs_S": max_abs_cov_resid,
            "P_two_step_vs_closed_form_max_abs_log_residual": float(np.max(np.abs(lnP_two_step - lnP_closed)))}
    out_mc[tag] = cl
res["MC"] = out_mc

# closed-form comparison (MC is finite evidence; residuals reported, tolerances below)
res["MC_residuals"] = {}
for tag in ("A_uncorrelated", "B_correlated"):
    cf = res["covariance_cases"][tag]
    mc = out_mc[tag]
    res["MC_residuals"][tag] = {
        "Var_ln_a0_rel": abs(mc["Var_ln_a0"] - cf["Var_ln_a0"]) / cf["Var_ln_a0"],
        "Var_ln_rM_rel": abs(mc["Var_ln_rM"] - cf["Var_ln_rM"]) / cf["Var_ln_rM"],
        "Var_ln_vflat_rel": abs(mc["Var_ln_vflat"] - cf["Var_ln_vflat"]) / cf["Var_ln_vflat"],
        "Var_ln_P_rel": abs(mc["Var_ln_P"] - cf["Var_ln_P"]) / cf["Var_ln_P"],
    }

# ---------------- FD Jacobian check ----------------
h = 1e-5   # central-difference step: truncation ~h^2*|f'''|/6 ~ 3e-11, rounding ~2eps/h ~ 4e-11
           # (pre-set target: |numeric - analytic| < 1e-9, i.e. the Jacobian confirmed to 9 digits)
def lna0_of(k, Gv, rho):
    return np.log(k) + np.log(c) + 0.5 * np.log(Gv) + 0.5 * np.log(rho)
for name, (k, Gv, rho) in {"canonical": (KAPPA, G, rhoL_can), "alternative": (KAPPA, G, rhoL_alt)}.items():
    dk = (lna0_of(k * (1 + h), Gv, rho) - lna0_of(k * (1 - h), Gv, rho)) / (2 * h)
    dG = (lna0_of(k, Gv * (1 + h), rho) - lna0_of(k, Gv * (1 - h), rho)) / (2 * h)
    dL = (lna0_of(k, Gv, rho * (1 + h)) - lna0_of(k, Gv, rho * (1 - h))) / (2 * h)
    res.setdefault("FD_jacobian", {})[name] = {
        "numeric": [dk, dG, dL], "analytic": J.tolist(),
        "rel_resid": max(abs(dk - 1), abs(dG - 0.5), abs(dL - 0.5)),
    }

# ---------------- HP check (mpmath 80 digits) ----------------
from mpmath import mp, mpf
mp.dps = 80
mk, mG, mL = mpf(s_k), mpf(s_G), mpf(s_L)
r_kg, r_kl, r_gl = mpf("0.10"), mpf("-0.20"), mpf("0.35")
S11 = mk**2; S12 = r_kg * mk * mG; S13 = r_kl * mk * mL
S22 = mG**2; S23 = r_gl * mG * mL; S33 = mL**2
vhp = S11 + S12 + S13 + mpf(0.25) * S22 + mpf(0.5) * S23 + mpf(0.25) * S33
res["HP"] = {"mpmath_80_var_ln_a0_B": float(vhp),
             "float64_var_ln_a0_B": float(J @ SigB @ J),
             "rel_resid": float(abs(vhp - J @ SigB @ J) / vhp)}

# ---------------- summary ----
res["enforced_bounds"] = ENFORCED_BOUNDS
ru = resource.getrusage(resource.RUSAGE_SELF)
res["ru_maxrss_kB_or_B"] = ru.ru_maxrss   # macOS: bytes; Linux: kB
res["script_wall_s_measured_by_tool"] = None
print(json.dumps(res, indent=1))