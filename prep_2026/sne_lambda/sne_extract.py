#!/usr/bin/env python3
"""
sne_extract.py -- Dark-energy density from Type Ia supernovae vs. the
de Sitter-Unruh MODIFIED-INERTIA framework's galaxy-side prediction.

Carl Zimmerman's framework. HONEST BOTH WAYS.

Physics (stated, not blurred):
  * The framework DOES NOT modify the cosmological background. a0 = c^2 sqrt(Lambda/32pi)
    = cH_Lambda/Z (Z=sqrt(32pi/3)=5.789) modifies galaxy INERTIA, not expansion.
    Lambda is a genuine constant, so H(z)=H0 sqrt(Om(1+z)^3+OL) and mu(z) are
    STANDARD LCDM. There is NO framework-native SNe formula. "rho_DE from SNe" IS
    the standard extraction; the framework contributes the galaxy-side PREDICTION.

  * SNe-SIDE (standard extraction): SNe constrain Omega_Lambda via the SHAPE of the
    Hubble diagram (deceleration q0 = Om/2 - OL). The ABSOLUTE density
    rho_DE = OL * 3 H0^2/(8 pi G) needs H0 (SNe alone are M_B - H0 degenerate).
    Input: Pantheon+ Brout+2022 (ApJ 938:110) SNe-only flat-LCDM Om = 0.334 +/- 0.018.

  * GALAXY-SIDE (framework prediction): rho_DE = 4 a0^2/(G c^2), since
    Lambda = 32 pi a0^2 / c^4  and  rho_Lambda = Lambda c^2 / (8 pi G).

  * THE CIRCULARITY: canonical a0 = cH_Lambda/Z was DEFINED from a cosmological
    (Planck) Lambda, so canonical-a0 -> rho_DE is Planck rho_Lambda by construction.
    Its match to SNe is algebra run backwards, NOT a test. The GENUINE cross-check
    uses the a0 MEASURED FROM SPARC rotation curves (Lambda-BLIND) and asks whether
    it inverts to the SNe-measured rho_DE.

Credits: Milgrom (interpolation kernel), Brout+2022 / Scolnic (Pantheon+),
Perlmutter / Riess / Schmidt (accelerating-universe discovery),
Sarkar (the SNe-leg critique this cross-check is relevant to).

Exit 0. numpy/scipy only. Frozen a0_line repo READ-ONLY (values hard-banked below).
"""
import json
import os
import numpy as np

# ---------------------------------------------------------------- constants
c   = 2.99792458e8      # m/s
G   = 6.67430e-11       # m^3 kg^-1 s^-2
MPC = 3.0856776e22      # m
KM  = 1.0e3

# ---------------------------------------------------------------- SNe-SIDE input
# Pantheon+ Brout+2022 (ApJ 938:110), 1701 light curves / 1550 SNe Ia,
# SNe-only flat-LCDM posterior:
OM_SNE    = 0.334
OM_SNE_SD = 0.018
OL_SNE    = 1.0 - OM_SNE        # flat  => Omega_Lambda
OL_SNE_SD = OM_SNE_SD           # flat  => sigma(OL) = sigma(Om)
Q0_SNE    = OM_SNE/2.0 - OL_SNE  # deceleration parameter (shape observable)

# Two H0 footings carried explicitly (SNe alone cannot fix H0).
H0_CASES = {
    "Planck_67.4": 67.4,   # km/s/Mpc
    "SH0ES_73.0": 73.0,
}

def rho_crit(H0_kms_mpc):
    """Critical density [kg/m^3] for H0 in km/s/Mpc."""
    H0 = H0_kms_mpc * KM / MPC   # s^-1
    return 3.0 * H0**2 / (8.0 * np.pi * G)

def rho_de_from_sne(H0_kms_mpc):
    """(rho_DE, sigma_rho_DE) [kg/m^3] from SNe Omega_Lambda x rho_crit(H0).
       Error is Omega_Lambda-only; H0 is a SEPARATE axis (reported, not folded)."""
    rc = rho_crit(H0_kms_mpc)
    return OL_SNE * rc, OL_SNE_SD * rc, rc

# ---------------------------------------------------------------- GALAXY-SIDE input
# Framework: rho_DE = 4 a0^2 / (G c^2).
def rho_de_from_a0(a0):
    return 4.0 * a0**2 / (G * c**2)

# a0 footings (banked from prep_2026/a0_line/fire_slope_results.json, READ-ONLY):
A0_CANON = 9.354769736111044e-11   # cH_Lambda/Z from Planck Lambda  [CIRCULAR]
A0_ALT   = 1.1305322040279838e-10  # alt footing

# MEASURED a0 from SPARC rotation curves -- Lambda-BLIND (budget_gas, GLS gas-dom):
A0_MEAS_GLS = 1.1814381247770623e-10   # a0hat (gas-dominated GLS slope estimator)
A0_MEAS_MED = 9.725607106012755e-11    # a0med (median variant)
A0_MEAS_TOT = 1.9026066078649394e-11   # total (stat+sys) 1-sigma on a0  (~16%)

# fractional error on measured a0:
FRAC_A0 = A0_MEAS_TOT / A0_MEAS_GLS
# rho_DE ~ a0^2 => sigma_ln(rho) = 2 * sigma_ln(a0):
SIGMA_LN_RHO_MEAS = 2.0 * FRAC_A0

# ---------------------------------------------------------------- compute
out = {"constants": {"c": c, "G": G, "MPC": MPC},
       "sne_input": {"source": "Pantheon+ Brout+2022 ApJ 938:110, SNe-only flat-LCDM",
                     "Omega_m": OM_SNE, "Omega_m_sd": OM_SNE_SD,
                     "Omega_Lambda": OL_SNE, "Omega_Lambda_sd": OL_SNE_SD,
                     "q0": Q0_SNE},
       "galaxy_input": {"rho_DE_formula": "4 a0^2 / (G c^2)",
                        "a0_canonical": A0_CANON, "a0_alt": A0_ALT,
                        "a0_measured_GLS": A0_MEAS_GLS, "a0_measured_med": A0_MEAS_MED,
                        "a0_measured_frac_err": FRAC_A0,
                        "sigma_ln_rho_measured": SIGMA_LN_RHO_MEAS},
       "cases": {}}

# framework rho_DE for each a0 footing:
rho_canon = rho_de_from_a0(A0_CANON)
rho_alt   = rho_de_from_a0(A0_ALT)
rho_meas_gls = rho_de_from_a0(A0_MEAS_GLS)
rho_meas_med = rho_de_from_a0(A0_MEAS_MED)
sig_meas_gls = SIGMA_LN_RHO_MEAS * rho_meas_gls   # linearized 1-sigma [kg/m^3]

out["galaxy_rho_DE"] = {
    "canonical_CIRCULAR": rho_canon,
    "alt": rho_alt,
    "measured_GLS": rho_meas_gls,
    "measured_GLS_sigma": sig_meas_gls,
    "measured_med": rho_meas_med,
}

def tension(r_fw, sln_fw, r_sne, s_sne):
    """(ratio, n_sigma) in LOG space -- the correct treatment for the ~32%
       multiplicative (lognormal) measured-a0 error, which dominates.
       sln_fw = sigma_ln of the framework rho; SNe error added in log too."""
    ratio   = r_fw / r_sne
    sln_sne = s_sne / r_sne           # small (~2.7%): OL error / rho
    denom   = np.sqrt(sln_fw**2 + sln_sne**2)
    nsig    = np.log(ratio) / denom
    return ratio, nsig

for name, H0 in H0_CASES.items():
    r_sne, s_sne, rc = rho_de_from_sne(H0)
    entry = {"H0_kms_mpc": H0, "rho_crit": rc,
             "rho_DE_SNe": r_sne, "rho_DE_SNe_sigma": s_sne,
             "footings": {}}

    # canonical -- FLAGGED CIRCULAR (a0 defined from a cosmological Lambda).
    # No measurement error on the fixed-footing a0 rows: log-tension is driven
    # by the SNe error alone (sln_fw = 0).
    ratio, nsig = tension(rho_canon, 0.0, r_sne, s_sne)
    entry["footings"]["canonical_CIRCULAR"] = {
        "rho_DE_framework": rho_canon, "ratio": ratio, "n_sigma": nsig,
        "note": "CIRCULAR: a0=cH_Lambda/Z defined from a cosmological (Planck) Lambda; "
                "this ratio only re-checks Planck-vs-SNe Lambda, NOT a framework test."}

    # alt footing (no measurement error attached):
    ratio, nsig = tension(rho_alt, 0.0, r_sne, s_sne)
    entry["footings"]["alt"] = {
        "rho_DE_framework": rho_alt, "ratio": ratio, "n_sigma": nsig}

    # MEASURED a0 -- THE GENUINE CROSS-CHECK (Lambda-blind rotation-curve dynamics):
    ratio, nsig = tension(rho_meas_gls, SIGMA_LN_RHO_MEAS, r_sne, s_sne)
    entry["footings"]["measured_GLS_GENUINE"] = {
        "rho_DE_framework": rho_meas_gls, "rho_DE_framework_sigma": sig_meas_gls,
        "ratio": ratio, "n_sigma": nsig,
        "note": "GENUINE cross-check: a0 from SPARC rotation-curve dynamics alone, "
                "no Lambda input. Sarkar-relevant independent corroboration test."}

    # measured median variant:
    ratio, nsig = tension(rho_meas_med, 0.0, r_sne, s_sne)
    entry["footings"]["measured_med"] = {
        "rho_DE_framework": rho_meas_med, "ratio": ratio, "n_sigma": nsig}

    # which footing does the SNe rho_DE sit CLOSEST to?
    cand = {"canonical": rho_canon, "alt": rho_alt,
            "measured_GLS": rho_meas_gls, "measured_med": rho_meas_med}
    closest = min(cand, key=lambda k: abs(np.log(cand[k]/r_sne)))
    entry["closest_footing"] = closest
    out["cases"][name] = entry

# ---------------------------------------------------------------- report
def fmt(x): return f"{x:.4e}"

print("="*72)
print("DARK-ENERGY DENSITY: Type Ia SNe  vs.  MI-framework galaxy prediction")
print("="*72)
print()
print("SNe-SIDE  (standard LCDM extraction -- NOT framework-native):")
print(f"  Pantheon+ Brout+2022 SNe-only flat-LCDM:")
print(f"    Omega_m      = {OM_SNE:.3f} +/- {OM_SNE_SD:.3f}")
print(f"    Omega_Lambda = {OL_SNE:.3f} +/- {OL_SNE_SD:.3f}  (flat)")
print(f"    q0 = Om/2 - OL = {Q0_SNE:+.3f}   (< 0 => accelerating)")
print(f"  SHAPE (q0) fixes Omega_Lambda; ABSOLUTE rho_DE needs H0 (M_B-H0 degenerate).")
print()
for name, H0 in H0_CASES.items():
    e = out["cases"][name]
    print(f"  H0 = {H0} ({name.split('_')[0]}):  rho_crit = {fmt(e['rho_crit'])}"
          f"  rho_DE(SNe) = {fmt(e['rho_DE_SNe'])} +/- {fmt(e['rho_DE_SNe_sigma'])} kg/m^3")
hi = out["cases"]["SH0ES_73.0"]["rho_DE_SNe"]; lo = out["cases"]["Planck_67.4"]["rho_DE_SNe"]
print(f"  H0 lever alone: (73.0/67.4)^2 = {(73.0/67.4)**2:.3f}x  "
      f"(rho_DE SH0ES/Planck = {hi/lo:.3f}x)")
print()
print("GALAXY-SIDE  (framework prediction  rho_DE = 4 a0^2/(G c^2)):")
print(f"  canonical  a0={fmt(A0_CANON)}  -> rho_DE={fmt(rho_canon)}  [CIRCULAR]")
print(f"  alt        a0={fmt(A0_ALT)}  -> rho_DE={fmt(rho_alt)}")
print(f"  MEASURED   a0={fmt(A0_MEAS_GLS)} +/-{FRAC_A0*100:.0f}%  -> "
      f"rho_DE={fmt(rho_meas_gls)} +/- {fmt(sig_meas_gls)}  [GENUINE, Lambda-blind]")
print(f"  meas.med   a0={fmt(A0_MEAS_MED)}  -> rho_DE={fmt(rho_meas_med)}")
print()
print("RATIO  rho_DE(framework) / rho_DE(SNe)   +   sigma-tension:")
for name, H0 in H0_CASES.items():
    e = out["cases"][name]
    print(f"  --- {name}  (rho_DE(SNe)={fmt(e['rho_DE_SNe'])}) ---")
    for foot in ["canonical_CIRCULAR", "alt", "measured_GLS_GENUINE", "measured_med"]:
        f = e["footings"][foot]
        tag = "  [CIRCULAR]" if "CIRCULAR" in foot else ("  [GENUINE]" if "GENUINE" in foot else "")
        print(f"    {foot:22s} ratio={f['ratio']:.3f}x  ({f['n_sigma']:+.2f} sigma){tag}")
    print(f"    -> SNe rho_DE sits CLOSEST to footing: {e['closest_footing']}")
print()
print("CIRCULARITY: the canonical match is algebra run backwards (a0 was DEFINED")
print("from Planck Lambda). The MEASURED-a0 row is the only genuine cross-check.")
print("="*72)

# ---------------------------------------------------------------- ZERO-FREE-PARAM
# SNe-DIAGRAM PREDICTION: predict mu(z) from the GALAXY-measured Lambda (no SNe
# shape used), compare residuals + chi2 against the best-fit LCDM Hubble diagram.
#
# Given H0 and the galaxy a0 -> Lambda -> rho_Lambda -> Omega_Lambda(H0), flatness
# fixes Omega_m. mu(z) then follows with ZERO free parameters (a0 and H0 are the
# only inputs, both fixed externally: a0 from rotation curves, H0 from the ladder).
# Best-fit reference = Pantheon+ SNe-only flat-LCDM (Om=0.334). We report delta-mu(z)
# and a chi2 using REPRESENTATIVE Pantheon+ binned errors (not the full covariance --
# this is an order-of-magnitude discriminator, not the official likelihood).
from scipy.integrate import quad

def E_inv(z, Om, OL):
    return 1.0 / np.sqrt(Om*(1.0+z)**3 + OL)

def mu_of_z(zgrid, Om, OL, H0_kms_mpc):
    """Distance modulus mu(z) for a flat LCDM (Om+OL=1)."""
    H0 = H0_kms_mpc * KM / MPC
    DH = c / H0                      # Hubble distance [m]
    mu = np.empty_like(zgrid)
    for i, z in enumerate(zgrid):
        Dc = DH * quad(E_inv, 0.0, z, args=(Om, OL))[0]   # comoving [m]
        DL = (1.0+z) * Dc                                  # luminosity [m]
        DL_pc = DL / (MPC/1.0e6)                           # -> parsec
        mu[i] = 5.0*np.log10(DL_pc) - 5.0
    return mu

# Pantheon+ binned-diagram redshift range (18 representative log-spaced bins,
# 0.01 < z < 2.3) with a representative per-bin binned error (~0.05 mag typical
# of the Pantheon+ binned Hubble diagram):
zbins  = np.logspace(np.log10(0.01), np.log10(2.3), 18)
sig_mu = 0.05 * np.ones_like(zbins)   # representative binned sigma_mu [mag]

sne_diag = {"z_bins": zbins.tolist(), "sigma_mu_representative": 0.05,
            "note": "chi2 uses representative binned errors, NOT the full "
                    "Pantheon+ covariance; order-of-magnitude discriminator only.",
            "by_H0": {}}

print()
print("ZERO-FREE-PARAM SNe-DIAGRAM PREDICTION (galaxy Lambda -> mu(z)):")
for name, H0 in H0_CASES.items():
    rc = rho_crit(H0)
    # best-fit LCDM reference (SNe-only shape):
    mu_ref = mu_of_z(zbins, OM_SNE, OL_SNE, H0)
    e = {"H0": H0}
    for label, rho_fw in [("measured_GLS", rho_meas_gls),
                          ("measured_med", rho_meas_med),
                          ("canonical_CIRCULAR", rho_canon)]:
        OL_pred = rho_fw / rc                 # galaxy Lambda -> Omega_Lambda(H0)
        Om_pred = 1.0 - OL_pred               # flatness
        tag = "  [CIRCULAR]" if "CIRCULAR" in label else ""
        if Om_pred <= 0.0:
            # galaxy Lambda exceeds the critical density at this H0 -> a flat
            # universe would need Om<0: UNPHYSICAL / over-closure. Honest flag.
            e[label] = {"Omega_Lambda_pred": OL_pred, "Omega_m_pred": Om_pred,
                        "max_abs_dmu_mag": None, "chi2_vs_bestfit_LCDM": None,
                        "ndof": len(zbins),
                        "unphysical": "Om_pred<0: galaxy Lambda exceeds closure at this H0"}
            print(f"  {name:12s} {label:20s} OL_pred={OL_pred:.3f} "
                  f"Om_pred={Om_pred:+.3f}  UNPHYSICAL (exceeds closure; Om<0){tag}")
            continue
        mu_pred = mu_of_z(zbins, Om_pred, OL_pred, H0)
        dmu     = mu_pred - mu_ref
        chi2    = float(np.sum((dmu/sig_mu)**2))
        e[label] = {"Omega_Lambda_pred": OL_pred, "Omega_m_pred": Om_pred,
                    "max_abs_dmu_mag": float(np.max(np.abs(dmu))),
                    "chi2_vs_bestfit_LCDM": chi2, "ndof": len(zbins)}
        print(f"  {name:12s} {label:20s} OL_pred={OL_pred:.3f} "
              f"Om_pred={Om_pred:.3f}  max|dmu|={np.max(np.abs(dmu)):.3f} mag  "
              f"chi2/{len(zbins)}={chi2:.1f}{tag}")
    sne_diag["by_H0"][name] = e
out["sne_diagram_prediction"] = sne_diag
print("  (dmu is the galaxy-predicted offset from the SNe best-fit LCDM diagram;")
print("   small chi2 => the galaxy Lambda reproduces the SNe diagram with no SNe fit.)")

# ---------------------------------------------------------------- persist
here = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(here, "sne_extract_results.json"), "w") as fh:
    json.dump(out, fh, indent=1)
print(f"wrote {os.path.join(here, 'sne_extract_results.json')}")
