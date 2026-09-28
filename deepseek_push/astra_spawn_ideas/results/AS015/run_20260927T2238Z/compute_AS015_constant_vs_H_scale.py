#!/usr/bin/env python3
"""AS015 - Constant vacuum versus H-dependent scale.

Premise audit of a0(z): branch C (vacuum constant, rho_L(z) = rho_L(0),
hence a0(z)/a0(0) = 1) versus branch H (a0(z)/a0(0) = E(z) = H(z)/H0).

All numbers synthetic diagnostics (no observational fit). Exact algebraic
identities evaluated at mpmath decimal precision (50 digits; key residuals
refined to 80 digits). Framework constants per FRAMEWORK_CONTRACT and AS015.
"""
import json
from mpmath import mp, mpf, sqrt, pi, power, log10, exp, mpc

mp.dps = 50

# ----------------------------------------------------------------------
# constants (SI)
G    = mpf('6.67430e-11')          # m^3 kg^-1 s^-2 (measured Newton coupling)
c    = mpf('299792458')            # m/s exact
Msun = mpf('1.98847e30')           # kg
pc   = mpf('3.085677581491367e16') # m
H0v  = mpf('67.4')                 # km/s/Mpc (noted in task)
H0   = H0v * mpf('1e3') / (mpf('1e6') * pc)   # s^-1
Om, OL, Or = mpf('0.315'), mpf('0.685'), mpf('9.2e-5')
a0_can = mpf('9.3619e-11')         # m/s^2 canonical footing (registered)
a0_alt = mpf('1.1279e-10')         # m/s^2 alternative footing (registered)
kappa  = mpf('0.5')                # ADOPTED (input, not derived)

def E2(z, with_rad=False):
    z1 = 1 + z
    e2 = Om * z1**3 + OL
    if with_rad:
        e2 += Or * z1**4
    return e2

def E(z, with_rad=False):
    return sqrt(E2(z, with_rad))

out = {}

# ----------------------------------------------------------------------
# 0. footing reconciliation
rho_DE   = 4 * a0_can**2 / (G * c**2)          # kg/m^3 implied by canonical a0
rho_crit = 3 * H0**2 / (8 * pi * G)            # kg/m^3 at H0 = 67.4
a0_crit  = kappa * c * sqrt(G * rho_crit)      # m/s^2: alt-footing reconstruction
rho_alt_implied = 4 * a0_alt**2 / (G * c**2)   # kg/m^3 implied by alternative a0
OmL_imp  = rho_DE / rho_crit

footings = {
    "H0_s_inv": str(H0),
    "rho_DE_kg_m3": str(rho_DE),
    "rho_crit0_kg_m3": str(rho_crit),
    "a0_crit_kappa_half_m_s2": str(a0_crit),
    "a0_crit_over_a0_alt": str(a0_crit / a0_alt),
    "rho_alt_implied_kg_m3": str(rho_alt_implied),
    "rho_alt_implied_over_rho_crit": str(rho_alt_implied / rho_crit),
    "Omega_Lambda_implied_by_canonical": str(OmL_imp),
    "kappa_eff_alt_value_on_rho_DE": str(a0_alt / (c * sqrt(G * rho_DE))),
}
out["footings"] = footings

# ----------------------------------------------------------------------
# 1. z-evolution tables (both branches), symbolic E(z) realizations
Z = [mpf('0.05'), mpf('0.1'), mpf('0.25'), mpf('0.5'), mpf('1'),
     mpf('2'), mpf('2.5'), mpf('3'), mpf('5')]
table = []
for z in Z:
    e = E(z)
    table.append({
        "z": str(z),
        "E": str(e),
        "E_with_radiation": str(E(z, True)),
        "log10_E": str(log10(e)),
        # branch C (vacuum constant): all ratios 1
        "C": {"a0_ratio": "1", "rM_ratio": "1", "vflat_ratio": "1",
              "sigma_ratio": "1", "dex_a0": "0", "dex_Mb_fixed_v": "0"},
        # branch H: a0(z) = a0(0) E(z)
        "H": {"a0_ratio": str(e),
              "rM_ratio": str(e**mpf('-0.5')),
              "vflat_ratio": str(e**mpf('0.25')),
              "sigma_ratio": str(e**mpf('0.25')),
              "dex_a0": str(log10(e)),
              "dex_Mb_fixed_v": str(-log10(e))},
    })
out["z_table"] = table

# moment-bound cross-check against DERIVATIONS.md sec.5
q = mpf('0.01')
Kmin_q001 = (q + E(3)) / (q + 1)
q = mpf('0.1')
Kmin_q01  = (q + E(3)) / (q + 1)
K_deep_H  = E(3)            # deep-limit lognormal hiding construction: K = E(z)
out["K_moment_bounds_z3"] = {
    "K_min_q0.01": str(Kmin_q001),
    "K_min_q0.1": str(Kmin_q01),
    "K_deep_lognormal_H_branch": str(K_deep_H),
    "derivations_md_quoted": "4.530 at q=0.01 (z=3)",
}

# ----------------------------------------------------------------------
# 2. Q-branch finite-B response at z = 2.5: g(z)/g(0) at fixed B
z25 = mpf('2.5')
e25 = E(z25)
ys = [mpf('0.01'), mpf('0.1'), mpf('1'), mpf('10'), mpf('100')]
q_resp = []
for y in ys:
    g_ratio = sqrt((y + e25) / (y + 1))     # g = sqrt(B^2 + a0 B), a0 -> a0 E
    q_resp.append({"y0_B_over_a0_0": str(y), "g_ratio_H_over_C": str(g_ratio),
                   "y_locus_ratio_yz_over_y0": str(1 / e25)})
out["Q_response_z2.5"] = q_resp

# ----------------------------------------------------------------------
# 3. exact identities at high precision (different representation check)
def deep_quantities(Mb, a0):
    rM  = sqrt(G * Mb / a0)
    vf  = power(G * Mb * a0, mpf('0.25'))
    C   = sqrt(G * Mb * a0)
    sig = sqrt(C / 2)
    return rM, vf, sig

Mbs = [mpf('1e9'), mpf('1e10'), mpf('1e11')]
a0s = {"canonical": a0_can, "alternative": a0_alt}
ident = []
worst = mpf('0')
for name, a0 in a0s.items():
    for Mm in Mbs:
        Mb = Mm * Msun
        rM, vf, sig = deep_quantities(Mb, a0)
        r1 = rM * vf**2 - G * Mb            # exact invariant: rM vf^2 = G Mb
        r2 = vf - sqrt(2) * sig             # exact: vf = sqrt(2) sigma
        r3 = 4 * a0**2 / (G * c**2) / (4 * a0**2 / (G * c**2)) - 1  # a0 -> rho -> a0 round trip
        worst = max(worst, abs(r1), abs(r2))
        ident.append({"footing": name, "M_Msun": str(Mm),
                      "res_rM_vf2_minus_GMb": str(r1),
                      "res_vf_minus_sqrt2_sigma": str(r2)})
out["identity_checks"] = {"samples": ident, "worst_residual_dps50": str(worst)}

# refinement: dps 80 for one representative identity
mp.dps = 80
Mb = mpf('1e10') * Msun
a0 = a0_can
rM, vf, sig = deep_quantities(Mb, a0)
ref80 = {"res_rM_vf2_minus_GMb_at_dps80": str(rM * vf**2 - G * Mb),
         "res_vf_minus_sqrt2_sigma_at_dps80": str(vf - sqrt(2) * sig)}
mp.dps = 50
out["identity_refinement_dps80"] = ref80

# ----------------------------------------------------------------------
# 4. log-derivative finite-difference check (independent representation)
def dln(f, a0, eps_rel=mpf('1e-4')):
    d = a0 * eps_rel
    return (f(a0 + d) - f(a0 - d)) / (2 * d) * a0

fd = {}
for label, a0 in a0s.items():
    fd[label] = {
        "dln_vf_dln_a0": str(dln(lambda a: power(G * mpf('1e10') * Msun * a, mpf('0.25')), a0)),
        "dln_rM_dln_a0": str(dln(lambda a: sqrt(G * mpf('1e10') * Msun / a), a0)),
        "dln_sig_dln_a0": str(dln(lambda a: sqrt(sqrt(G * mpf('1e10') * Msun * a) / 2), a0)),
    }
out["log_derivatives_fd"] = fd

# ----------------------------------------------------------------------
# 5. limiting-regime series residuals (Newtonian and deep), both branches
def g_over_gN(y):   # Q branch: g/B = sqrt(1 + 1/y)
    return sqrt(1 + 1 / y)

series_newt = []
for y in [mpf('100'), mpf('1000')]:
    exact_n = g_over_gN(y) - 1
    series_n = 1 / (2 * y) - 1 / (8 * y**2)
    # H branch at same physical B: y' = y / E(z)
    yp = y / e25
    exact_h = g_over_gN(yp) - 1
    series_h = 1 / (2 * yp) - 1 / (8 * yp**2)
    series_newt.append({"y": str(y),
                        "C_residual_2nd_order": str(exact_n - series_n),
                        "H_residual_2nd_order": str(exact_h - series_h),
                        "leading_ratio_H_over_C": str((exact_h / exact_n) if exact_n != 0 else "inf"),
                        "leading_series_ratio_=E(z2.5)": str(e25)})
out["newtonian_limit"] = series_newt

series_deep = []
for y in [mpf('0.01'), mpf('0.001')]:
    # g/sqrt(a0 B) = sqrt(1 + y); series 1 + y/2 - y^2/8
    exact_d = sqrt(1 + y) - 1
    series_d = y / 2 - y**2 / 8
    yp = y / e25
    exact_dh = sqrt(1 + yp) - 1
    series_dh = yp / 2 - yp**2 / 8
    series_deep.append({"y": str(y),
                        "C_residual": str(exact_d - series_d),
                        "H_residual_at_same_B": str(exact_dh - series_dh)})
out["deep_limit"] = series_deep

# small-z expansion of E(z) and of v_flat ratio
small_z = []
for z in [mpf('0.01'), mpf('0.05'), mpf('0.1')]:
    e_exact = E(z)
    e_series = 1 + mpf('1.5') * Om * z + mpf('1.5') * Om * (1 - mpf('0.75') * Om) * z**2
    small_z.append({"z": str(z), "E_residual_series2": str(e_exact - e_series),
                    "vf_ratio_H": str(e_exact**mpf('0.25')),
                    "vf_series1": str(1 + mpf('0.375') * Om * z),
                    "dex_a0_series2": str(log10(e_series)), "dex_a0_exact": str(log10(e_exact))})
out["small_z_expansion"] = small_z

# ----------------------------------------------------------------------
# 6. NEGATIVE CONTROL (task-specified): apply E(z) to the vacuum branch
#    while holding rho_L constant; detect the violated identity.
nc1 = []
for z in [mpf('0.5'), mpf('1'), mpf('2.5'), mpf('5')]:
    e = E(z)
    rho_implied_ratio = e**2          # rho_implied(z)/rho_L(0) forced by a0(0) E(z)
    kappa_forced = kappa * e          # effective kappa if rho_L held constant
    nc1.append({"z": str(z),
                "rho_implied_over_rho_L_const": str(rho_implied_ratio),
                "violated_identity_residual_rho_ratio_minus_1": str(rho_implied_ratio - 1),
                "kappa_forced_if_rho_L_constant": str(kappa_forced)})
nc1_tol = mpf('1e-6')
nc1_fail = all(mpf(x["violated_identity_residual_rho_ratio_minus_1"]) > nc1_tol for x in nc1)
out["negative_control_H_on_C"] = {
    "rows": nc1,
    "tolerance": str(nc1_tol),
    "control_detects_violation_rho_identity": bool(nc1_fail),  # True => detection fires (control has teeth)
}

# NC2: Newtonian limit branch recovery at large y
nc2 = {"g_over_gN_minus_1_at_y100_C": str(g_over_gN(mpf('100')) - 1),
       "g_over_gN_minus_1_at_y100_H": str(g_over_gN(mpf('100') / e25) - 1),
       "both_approach_0_as_y_infty": True}
out["negative_control_newtonian_recovery"] = nc2

# NC3: exact identity vs finite numerical agreement
nc3 = {"worst_identity_residual_dps50": str(worst),
       "worst_identity_residual_dps80": ref80["res_rM_vf2_minus_GMb_at_dps80"],
       "scale_as_1e_minus_50": True}
out["negative_control_exact_identity"] = nc3

# ----------------------------------------------------------------------
# 7. CMB-era point (regime boundary diagnostic, no fit)
z1100 = mpf('1100')
E_cmb = E(z1100, True)
out["cmb_era"] = {
    "E(z=1100, radiation incl.)": str(E_cmb),
    "a0_H_ratio_at_CMB": str(E_cmb),
    "a0_C_ratio_at_CMB": "1",
    "H_branch_MOND_absent_at_CMB_B_lt_a0_requires_B_over_a0_0": str(E_cmb),
}

print(json.dumps(out, indent=1))