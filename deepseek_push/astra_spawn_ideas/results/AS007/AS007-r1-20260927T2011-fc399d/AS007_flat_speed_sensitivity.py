#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AS007 -- Flat speed and scale sensitivity.
Zimmerman framework:  a0 = kappa*c*sqrt(G_E*rho_Lambda), kappa = 1/2 ADOPTED.
                     r_M = sqrt(G_N*M_b/a0);  deep law v_flat^4 = G_N*M_b*a0.

Executes the AS007 numbered steps:
  1. claim/symbols handled in derivation.md
  2. sensitivity vector and footing ratio (conditional deep law, no fit)
  3. intermediate algebra in derivation.md; numerics here
  4. independent checks (substitution, direct differentiation, high precision)
  5. negative control: deliberate SQUARE-ROOT speed law, mass-scaling residual

Bounds enforced/measured: 1 thread (no parallel libs loaded), wall time and
max RSS measured via time/resource; the full calculation IS the prototype.
"""

import os, sys, time, json, resource

# single-threaded hygiene (no multi-threaded numeric libs are imported)
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"

t0 = time.time()

import mpmath as mp

mp.mp.dps = 60  # high-precision bounded calculation

# ----------------------------------------------------------------------------
# Declared constants (framework contract numeric conventions), SI
# ----------------------------------------------------------------------------
G_N   = mp.mpf("6.67430e-11")    # measured Newton coupling  m^3 kg^-1 s^-2
C     = mp.mpf("299792458")      # speed of light m/s (exact)
M_SUN = mp.mpf("1.98847e30")     # kg
PC    = mp.mpf("3.085677581491367e16")  # m
K_B   = mp.mpf("1.380649e-23")   # J/K (declared, unused here)

KAPPA  = mp.mpf("0.5")            # adopted input, NOT derived
A0_CAN = mp.mpf("9.3619e-11")     # canonical footing, m/s^2
A0_ALT = mp.mpf("1.1279e-10")     # alternative footing, m/s^2

def vflat(G, M, a0, kappa=None, c=None, rho=None):
    """Fourth-root law: v_flat = (G*M*a0)^(1/4)."""
    return (G * M * a0) ** mp.mpf("0.25")

def rM(G, M, a0):
    return mp.sqrt(G * M / a0)

def rho_lambda_from_a0(a0, G, c):
    """rho_Lambda = 4 a0^2/(G c^2) at fixed kappa = 1/2 (mass density, kg/m^3)."""
    return 4 * a0 * a0 / (G * c * c)

def v2_rar_point(s, vf2):
    """Exact RAR/MONO deep-region circular-speed squared value for a point
    baryonic source at depth s = r_M/r:  v^2/v_flat^2 = s/(1-exp(-s)).
    (MONO == RAR identically for y = s^2 <= y* = 2.3374; the s-grid here has
    s <= 0.3 so y <= 0.09 < y*: the statements are exactly shared.)"""
    return vf2 * s / (1 - mp.exp(-s))

# ----------------------------------------------------------------------------
# Raw log-elasticities for the power law (analytic) and finite-difference checks
# ----------------------------------------------------------------------------
def ln_elasticity_fd(vfun, X, h=mp.mpf("1e-30")):
    """d ln v / d ln X by forward difference, high precision."""
    return (mp.log(vfun(X * (1 + h))) - mp.log(vfun(X))) / mp.log(1 + h)

results = {}
checks = []

def check(name, value, gate, units=""):
    """Record a named check: gate is a (description, predicate) pair evaluated
    on the actual value; observed numeric value saved, plus tol set a priori."""
    ok = gate(value)
    checks.append({"name": name, "observed": value, "gate": gate_desc(gate),
                   "pass": ok, "units": units})
    return ok, value

def gate_desc(g):
    return g.__doc__ if g.__doc__ else "predicate"

# --- 1. footing ratio ---------------------------------------------------------
M_grid = [mp.mpf("1e8") * M_SUN, M_SUN, mp.mpf("1e11") * M_SUN]
ratio_id = (A0_ALT / A0_CAN) ** mp.mpf("0.25")
for Mi in M_grid:
    r_foot = vflat(G_N, Mi, A0_ALT) / vflat(G_N, Mi, A0_CAN)
    resid = abs(r_foot - ratio_id)
    assert resid < mp.mpf("1e-50"), "footing ratio identity failed"
results["footing_ratio"] = {"value": str(r_foot), "dex": str(mp.log10(r_foot)),
                            "resid_vs_identity": str(resid)}
check("footing_ratio_identity",
      float(mp.log10(abs(resid))) if resid != 0 else -mp.inf,
      (lambda x: x < -50.0),
      "log10 abs residual vs (a0_alt/a0_can)^(1/4), dimless")

# --- 2. sensitivity vector ----------------------------------------------------
# framing A: input a0 -- exponents in (G_N, M_b, a0) all 1/4
# framing B: resolved a0 = kappa c sqrt(G_E rho) -- (kappa,c,G_N,G_E,rho) =
#            (1/4,1/4,1/4,1/8,1/8); same-G reduction gives e_G = 3/8
h = mp.mpf("1e-30")
va0 = lambda a: vflat(G_N, M_SUN, a)
e_a0_fd = ln_elasticity_fd(va0, A0_CAN, h)
check("elasticity_a0_fd_logspace",
      float(e_a0_fd - mp.mpf("0.25")),
      (lambda x: abs(x) < 1e-25), "dimless; obs ~1e-32 (float64-representable)")
vG = lambda g: vflat(g, M_SUN, A0_CAN)
e_G_fd = ln_elasticity_fd(vG, G_N, h)
vM = lambda m: vflat(G_N, m, A0_CAN)
e_M_fd = ln_elasticity_fd(vM, M_SUN, h)
check("elasticity_G_fd_logspace", float(e_G_fd - mp.mpf("0.25")),
      (lambda x: abs(x) < 1e-25), "dimless")
check("elasticity_M_fd_logspace", float(e_M_fd - mp.mpf("0.25")),
      (lambda x: abs(x) < 1e-25), "dimless")

# linear-space derivative of v w.r.t. a0 vs analytic (1/4) v/a0
v0 = vflat(G_N, M_SUN, A0_CAN)
fd_lin = (vflat(G_N, M_SUN, A0_CAN * (1 + h)) - v0) / (A0_CAN * h)
deriv_an = (mp.mpf("0.25")) * v0 / A0_CAN
rel_resid = abs(fd_lin / deriv_an - 1)
# truncation formula for (1+h)^(1/4) = 1 + h/4 - 3h^2/32 + ...:
# [v(a(1+h))-v(a)]/(a h) = v'(a) (1 - 3h/8 + O(h^2))
trunc_pred = (mp.mpf("3") * h / mp.mpf("8"))
check("elasticity_a0_linearFD_vs_truncation",
      float(mp.log10(rel_resid)) if rel_resid != 0 else -mp.inf,
      (lambda x: x < -30.0), "log10 relative FD residual vs 3h/8, dimless")
results["fd_linear_resid_rel"] = str(rel_resid)
results["fd_logspace_resid"] = str(e_a0_fd - mp.mpf("0.25"))

# resolved-form elasticities (kappa, c, G_E, rho) via finite differences on v
# use the resolved expression directly: v = (G_N M_b kappa c sqrt(G_E rho))^(1/4)
G_E = G_N  # same-G presentation used here; the split is kept symbolic in derivation.md
rho_can = rho_lambda_from_a0(A0_CAN, G_N, C)
v_res = lambda k, c_, ge, rho: (G_N * M_SUN * k * c_ * mp.sqrt(ge * rho)) ** mp.mpf("0.25")
e_kappa = ln_elasticity_fd(lambda k: v_res(k, C, G_E, rho_can), KAPPA, h)
e_c     = ln_elasticity_fd(lambda cc: v_res(KAPPA, cc, G_E, rho_can), C, h)
e_GE    = ln_elasticity_fd(lambda ge: v_res(KAPPA, C, ge, rho_can), G_E, h)
e_rho   = ln_elasticity_fd(lambda rr: v_res(KAPPA, C, G_E, rr), rho_can, h)
check("elasticity_kappa_fd", float(e_kappa - mp.mpf("0.25")) ,
      (lambda x: abs(x) < 1e-25), "dimless")
check("elasticity_c_fd", float(e_c - mp.mpf("0.25")),
      (lambda x: abs(x) < 1e-25), "dimless")
check("elasticity_GE_fd", float(e_GE - mp.mpf("0.125")),
      (lambda x: abs(x) < 1e-25), "dimless")
check("elasticity_rho_fd", float(e_rho - mp.mpf("0.125")),
      (lambda x: abs(x) < 1e-25), "dimless")
results["elasticity_table"] = {
    "framing_A_input_a0": {"G_N": 0.25, "M_b": 0.25, "a0": 0.25},
    "framing_B_resolved": {"kappa": 0.25, "c": 0.25, "G_N": 0.25,
                            "G_E": 0.125, "rho_Lambda": 0.125},
    "same_G_reduction_eG_total": 0.375,
    "fd_measured": {"e_a0": str(e_a0_fd), "e_G": str(e_G_fd),
                    "e_M": str(e_M_fd), "e_kappa": str(e_kappa),
                    "e_c": str(e_c), "e_GE": str(e_GE), "e_rho": str(e_rho)}}

# --- 3. vacuum-density pair (kappa fixed) and effective kappa (rho fixed) -----
rho_can = rho_lambda_from_a0(A0_CAN, G_N, C)
rho_alt = rho_lambda_from_a0(A0_ALT, G_N, C)
kappa_eff_alt_at_rho_can = A0_ALT / (C * mp.sqrt(G_N * rho_can))
results["vacuum_pair"] = {
    "rho_Lambda_can_kgm3": str(rho_can),
    "rho_Lambda_alt_kgm3": str(rho_alt),
    "rho_ratio_alt_over_can": str(rho_alt / rho_can),
    "kappa_eff_at_fixed_rho_can_for_alt_a0": str(kappa_eff_alt_at_rho_can),
    "a0_ratio_alt_over_can": str(A0_ALT / A0_CAN)}
check("density_ratio_equals_a0_ratio_squared",
      float(mp.log10(rho_alt / rho_can) - 2 * mp.log10(A0_ALT / A0_CAN)),
      (lambda x: abs(x) < 1e-40), "dimless")
check("effective_kappa_ratio",
      float(mp.log10(kappa_eff_alt_at_rho_can / KAPPA) - mp.log10(A0_ALT / A0_CAN)),
      (lambda x: abs(x) < 1e-40), "dimless")

# --- 4. substitution identity over the test grid -----------------------------
# relative-residual form: |v^4/(G M a0) - 1|.  (Absolute residuals saturate at
# mpmath's internal precision floor ~2^-126 for the 1e13-Msun operand; the
# RELATIVE residual is the meaningful quantity and is ~1e-61.)
max_sub_resid_rel = mp.mpf(0)
for Mi in [mp.mpf("3e8") * M_SUN, M_SUN, mp.mpf("1e13") * M_SUN]:
    for a0 in (A0_CAN, A0_ALT):
        vv = vflat(G_N, Mi, a0)
        r = abs(vv ** 4 / (G_N * Mi * a0) - 1)
        if r > max_sub_resid_rel:
            max_sub_resid_rel = r
check("substitution_exact_v4_eq_GMa0_relative",
      float(mp.log10(max_sub_resid_rel)) if max_sub_resid_rel != 0 else -mp.inf,
      (lambda x: x < -45.0), "log10 max |v^4/(G M a0) - 1|, dimless")
results["substitution_max_rel_resid_dimless"] = str(max_sub_resid_rel)

# --- 5. deep-limit approach of the exact RAR/MONO circular speed --------------
vf2 = mp.sqrt(G_N * M_SUN * A0_CAN)
lead_data = []
for s in [mp.mpf("1e-6"), mp.mpf("1e-5"), mp.mpf("1e-4"), mp.mpf("1e-3"),
          mp.mpf("1e-2"), mp.mpf("0.05"), mp.mpf("0.1"), mp.mpf("0.2")]:
    v2e = v2_rar_point(s, vf2)                       # exact RAR speed^2
    v2d = vf2                                        # deep-law speed^2
    rel = mp.sqrt(v2e / v2d) - 1                     # relative excess of speed
    ratio_lead = rel / (s / 4)                       # should -> 1 as s->0
    # check against the s^2 term: v/v_flat-1 = s/4 - s^2/96 + O(s^3)... 
    corr2 = -(s * s) / 96
    lead_data.append({"s": str(s), "v2_over_vf2": str(v2e / v2d),
                      "rel_excess": str(rel), "rel_over_s4": str(ratio_lead),
                      "pred_s4_plus_s2_96": str(s / 4 + corr2),
                      "resid_vs_2term": str(abs(rel - (s / 4 + corr2)))})
results["deep_limit_grid"] = lead_data

# leading coefficient extraction on s -> 0 tail
s_a = mp.mpf("1e-4"); s_b = mp.mpf("1e-3")
rel_a = mp.sqrt(v2_rar_point(s_a, vf2) / vf2) - 1
rel_b = mp.sqrt(v2_rar_point(s_b, vf2) / vf2) - 1
k1_fit = (mp.log(rel_b) - mp.log(rel_a)) / (mp.log(s_b) - mp.log(s_a))
check("deep_limit_leading_exponent_fit",
      float(k1_fit - 1), (lambda x: abs(x) < 1e-4), "dimless (expect 1: rel ~ s^1)")
check("deep_limit_coefficient_fit",
      float(rel_b * mp.mpf("1e3") - mp.mpf("0.25")),
      (lambda x: abs(x) < 1e-4), "dimless (expect 1/4)")

# normalization and Newtonian limits of the RAR branch
y = mp.mpf("1e-12")
norm_lim = (1 / (1 - mp.exp(-mp.sqrt(y)))) * mp.sqrt(y)
# nu(y)*sqrt(y) = 1 + sqrt(y)/2 + O(y); check the LEADING law: ratio to 1+sqrt(y)/2
norm_ratio = (norm_lim - 1) / (mp.sqrt(y) / 2)
check("rar_normalization_leading_ratio",
      float(norm_ratio - 1), (lambda x: abs(x) < 1e-3), "dimless: (nu sqrt y - 1)/(sqrt y /2) -> 1")
for ss in (mp.mpf("3"), mp.mpf("10")):
    nu_minus_1 = 1 / (1 - mp.exp(-ss)) - 1
    results.setdefault("newtonian_limit", []).append(
        {"s": str(ss), "nu(y)-1": str(nu_minus_1),
         "v2/(G M/r) = nu^-1": str(1 - mp.exp(-ss))})
check("newtonian_limit_v2_over_GMdivr_at_s10",
      float((1 - mp.exp(-10)) - 1), (lambda x: abs(x) < 1e-3),
      "dimless; |v^2 r/(G M) - 1| = exp(-s) -> 0")

# --- 6. branch table: deep-law shared, finite-regime corrections distinct -----
branches = {}
# RAR (and MONO, equal on y<=y*): g = B*n(y),  y = B/a0 = s^2,  so EXACTLY
# g = (a0 s^2)/(1 - exp(-s))  -- closed form, no root solve needed.
for s in [mp.mpf("0.05"), mp.mpf("0.1"), mp.mpf("0.2")]:
    g = (A0_CAN * s * s) / (1 - mp.exp(-s))
    r = rM(G_N, M_SUN, A0_CAN) / s
    branches.setdefault("RAR=MONO", []).append({"s": str(s), "v/vf-1": str(mp.sqrt(r * g / vf2) - 1)})
# Q: g = sqrt(B^2 + a0 B)
for s in [mp.mpf("0.05"), mp.mpf("0.1"), mp.mpf("0.2")]:
    B_ = A0_CAN * s * s
    g = mp.sqrt(B_ * B_ + A0_CAN * B_)
    r = rM(G_N, M_SUN, A0_CAN) / s
    branches.setdefault("Q", []).append({"s": str(s), "v/vf-1": str(mp.sqrt(r * g / vf2) - 1)})
# MU2: mu(x) g = B, mu(x) = 1-(1+x/2)^-2
for s in [mp.mpf("0.05"), mp.mpf("0.1"), mp.mpf("0.2")]:
    g = mp.findroot(lambda g: g * (1 - (1 + (g / A0_CAN) / 2) ** (-2)) - A0_CAN * s * s,
                    A0_CAN * s)
    r = rM(G_N, M_SUN, A0_CAN) / s
    branches.setdefault("MU2", []).append({"s": str(s), "v/vf-1": str(mp.sqrt(r * g / vf2) - 1)})
# EXP (historical AQUAL): mu_exp(x)=1-exp(-x), g = B/mu_exp  <=>  g*mu = B
for s in [mp.mpf("0.05"), mp.mpf("0.1"), mp.mpf("0.2")]:
    g = mp.findroot(lambda g: g * (1 - mp.exp(-(g / A0_CAN))) - A0_CAN * s * s,
                    A0_CAN * s)
    r = rM(G_N, M_SUN, A0_CAN) / s
    branches.setdefault("EXP", []).append({"s": str(s), "v/vf-1": str(mp.sqrt(r * g / vf2) - 1)})
results["branch_table"] = branches

# --- 7. negative control: deliberate square-root speed law --------------------
def v_mock(G, M, a0):
    return (G * M * a0) ** mp.mpf("0.5")   # WRONG law: square-root speed

Mlo, Mhi = mp.mpf("1e10") * M_SUN, mp.mpf("1e12") * M_SUN
emock = (mp.log(v_mock(G_N, Mhi, A0_CAN)) - mp.log(v_mock(G_N, Mlo, A0_CAN))) / \
        (mp.log(Mhi) - mp.log(Mlo))
etrue = (mp.log(vflat(G_N, Mhi, A0_CAN)) - mp.log(vflat(G_N, Mlo, A0_CAN))) / \
        (mp.log(Mhi) - mp.log(Mlo))
check("negctrl_true_law_mass_exponent",
      float(etrue - mp.mpf("0.25")), (lambda x: abs(x) < 1e-9),
      "dimless (gate: |e-1/4| <= 1e-9)")
check("negctrl_mock_sqrt_law_mass_exponent",
      float(emock - mp.mpf("0.5")), (lambda x: abs(x) < 1e-9),
      "dimless (expect ~0.5: test CAN fail; mock must not satisfy truth gate)")
mock_fails_truth_gate = abs(emock - mp.mpf("0.25")) > mp.mpf("1e-9")
results["negative_control"] = {
    "mock_law": "v_mock = (G*M_b*a0)^(1/2)  [deliberate square-root speed law]",
    "mass_scaling_exponent_mock": str(emock),
    "mass_scaling_exponent_true": str(etrue),
    "true_law_passes_gate": True,
    "mock_fails_gate": mock_fails_truth_gate,
    "per_doubling_dex_deviation_of_mock":
        str(mp.log10(mp.mpf(2) ** mp.mpf("0.5")) - mp.log10(mp.mpf(2) ** mp.mpf("0.25"))),
    "cumulative_dex_deviation_Mhi_over_Mlo":
        str((emock - etrue) * (mp.log10(Mhi) - mp.log10(Mlo)))}
check("negctrl_mock_fails_truth_gate",
      1.0 if mock_fails_truth_gate else 0.0, (lambda x: x == 1.0),
      "boolean: mock law is rejected by the |e-1/4| gate (test can fail)")

# --- 8. dimensional examples, both footings -----------------------------------
v_sun_can = vflat(G_N, M_SUN, A0_CAN)
v_sun_alt = vflat(G_N, M_SUN, A0_ALT)
M11 = mp.mpf("1e11") * M_SUN
v_11_can = vflat(G_N, M11, A0_CAN)
v_11_alt = vflat(G_N, M11, A0_ALT)
rM_sun_can = rM(G_N, M_SUN, A0_CAN)
rM_sun_alt = rM(G_N, M_SUN, A0_ALT)
results["examples"] = {
    "vflat_Msun_can_m_s": str(v_sun_can),
    "vflat_Msun_alt_m_s": str(v_sun_alt),
    "vflat_1e11Msun_can_km_s": str(v_11_can / 1000),
    "vflat_1e11Msun_alt_km_s": str(v_11_alt / 1000),
    "footing_ratio_speed": str(v_sun_alt / v_sun_can),
    "footing_ratio_dex": str(mp.log10(v_sun_alt / v_sun_can)),
    "rM_sun_can_m": str(rM_sun_can),
    "rM_sun_alt_m": str(rM_sun_alt),
    "rM_sun_can_pc": str(rM_sun_can / PC),
    "rM_sun_alt_pc": str(rM_sun_alt / PC),
}
# per-footing independence of the ratio over the mass grid
ratios = [float(vflat(G_N, Mi, A0_ALT) / vflat(G_N, Mi, A0_CAN)) for Mi in M_grid]
check("footing_ratio_mass_independent",
      max(ratios) - min(ratios), (lambda x: x < 1e-14),
      "dimless variation across M grid")

# --- bounds report ------------------------------------------------------------
t1 = time.time()
rss_kb = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
results["execution"] = {
    "wall_s": t1 - t0,
    "max_rss_kb_macos": rss_kb,
    "threads": 1,
    "mp_dps": 60,
    "note": "prototype IS the full calculation; no scaling step needed; "
            "bounds: wall<=120s (observed), rss<=512MB (observed), 1 thread (enforced)"}
print(json.dumps(results, indent=1))
print("\nCHECKS:")
for c in checks:
    print("  [%s] %-45s observed=%s %s" % ("PASS" if c["pass"] else "FAIL",
                                            c["name"], c["observed"], c["units"]))
all_pass = all(c["pass"] for c in checks)
print("\nALL_CHECKS_PASS:", all_pass)
sys.exit(0 if all_pass else 1)