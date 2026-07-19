#!/usr/bin/env python3
"""
setup.py -- SNe-side rho_DE extraction vs the framework galaxy-side prediction.
================================================================================
GOAL: get the dark-energy DENSITY rho_DE from Type Ia supernovae (the standard
LCDM extraction), and hand it to the compute lane to test against the
framework's GALAXY-side prediction rho_DE = 4 a0^2 / (G c^2).

HONEST PHYSICS (stated, not blurred):
  * The framework does NOT modify the cosmological background. a0 = c H_Lambda/Z
    = c^2 sqrt(Lambda/32pi) modifies galaxy INERTIA, not expansion. Lambda is a
    genuine constant => H(z)=H0 sqrt(Om(1+z)^3+OL) and mu(z) are STANDARD LCDM.
    There is NO framework-native SNe formula; "rho_DE from SNe" IS the standard
    extraction. The framework contributes only the galaxy-side cross-check.

  * SNe-SIDE (standard): the Hubble diagram constrains Omega_Lambda via its SHAPE
    (deceleration q0 = Om/2 - OL). The ABSOLUTE density
        rho_DE = Omega_Lambda * rho_crit = Omega_Lambda * 3 H0^2 / (8 pi G)
    needs H0 (SNe alone are M_B - H0 degenerate). We carry H0 explicitly:
    Planck 67.4 AND SH0ES 73.0, so the shape-vs-absolute / H0 dependence is VISIBLE.
    Input: Pantheon+ (Brout+2022) SNe-only flat-LCDM Omega_m = 0.334 +/- 0.018
    (=> Omega_Lambda = 0.666 +/- 0.018).

  * GALAXY-SIDE (framework prediction): from Lambda = 32pi a0^2/c^4,
        rho_Lambda = Lambda c^2/(8 pi G) = 4 a0^2 / (G c^2).
    Footings: canonical a0=9.355e-11, alt a0=1.1305e-10, and -- the HONEST input --
    the a0 MEASURED from SPARC rotation curves (Lambda-BLIND), reused from the
    banked a0-line (prep_2026/a0_line/fire_slope_results.json):
    gas-dominated GLS a0 = 1.181e-10 +/- 1.90e-11 (16%), median variant 9.73e-11.

  * THE CIRCULARITY (the crux): canonical a0 was DEFINED as c H_Lambda/Z from a
    COSMOLOGICAL Lambda (Planck). So "canonical a0 -> rho_DE = Planck rho_Lambda"
    is ALGEBRA RUN BACKWARDS, not a test -- it can only reproduce the Planck value.
    The GENUINE test uses the MEASURED a0 (rotation-curve dynamics ALONE, no Lambda
    input) and asks whether IT inverts to the SNe rho_DE. Both are reported; the
    canonical row is flagged CIRCULAR.

Credits: Milgrom (a0 kernel); Perlmutter/Riess/Schmidt (accelerating-universe
discovery); Brout+2022 / Scolnic (Pantheon+); Sarkar (the SNe-leg critique that
makes an INDEPENDENT galaxy-side corroboration of rho_DE meaningful).

Exit 0 is NOT a verdict. No 'proves'. Both footings + the measured a0, both H0.
"""
import numpy as np, os, json

HERE = os.path.dirname(os.path.abspath(__file__))
A0DIR = "/Users/carlzimmerman/new_physics/prep_2026/a0_line"
LEDGER = "/Users/carlzimmerman/new_physics/prep_2026/concordance_ledger"

# ---- physical constants (CODATA) ------------------------------------------------
C = 2.99792458e8            # m/s
G = 6.67430e-11             # m^3 kg^-1 s^-2
MPC = 3.0856775814913673e22 # m
bar = "=" * 92


def rho_crit(H0_kms_Mpc):
    """Critical density kg/m^3 for H0 in km/s/Mpc."""
    H0 = H0_kms_Mpc * 1e3 / MPC          # s^-1
    return 3.0 * H0**2 / (8.0 * np.pi * G)


def rho_DE_from_a0(a0):
    """Framework galaxy-side dark-energy density: rho_DE = 4 a0^2 / (G c^2)."""
    return 4.0 * a0**2 / (G * C**2)


# =================================================================================
# (1) SNe-SIDE EXTRACTION  (standard flat-LCDM; Pantheon+ SNe-only)
# =================================================================================
Om, Om_err = 0.334, 0.018                 # Brout+2022, SNe-only flat-LCDM
OL, OL_err = 1.0 - Om, Om_err             # flat: Omega_Lambda = 1 - Omega_m
q0 = Om / 2.0 - OL                        # deceleration parameter (the SHAPE quantity)

print(bar); print("(1) SNe-SIDE:  rho_DE = Omega_Lambda * 3 H0^2 / (8 pi G)   [standard LCDM]"); print(bar)
print(f"  Pantheon+ (Brout+2022) SNe-only flat-LCDM:  Omega_m = {Om:.3f} +/- {Om_err:.3f}")
print(f"     => Omega_Lambda = {OL:.3f} +/- {OL_err:.3f}   (SHAPE); q0 = {q0:+.3f} (accelerating)")
print( "  SNe constrain the SHAPE (Omega_Lambda); the ABSOLUTE rho_DE needs H0 "
       "(M_B-H0 degeneracy).")
sne = {}
for H0 in (67.4, 73.0):
    rc = rho_crit(H0)
    rDE = OL * rc
    rDE_err = OL_err * rc                  # error from Omega_Lambda at fixed H0
    sne[H0] = dict(rho_crit=rc, rho_DE=rDE, rho_DE_err=rDE_err)
    tag = "Planck" if H0 < 70 else "SH0ES"
    print(f"\n  H0 = {H0:.1f} km/s/Mpc ({tag}):  rho_crit = {rc:.3e} kg/m^3")
    print(f"     rho_DE(SNe) = {rDE:.3e} +/- {rDE_err:.2e} kg/m^3   "
          f"(sigma from Omega_L only; the H0 choice is a SEPARATE axis)")
print(f"\n  H0 lever: rho_DE(73.0)/rho_DE(67.4) = {sne[73.0]['rho_DE']/sne[67.4]['rho_DE']:.3f} "
      f"(= (73.0/67.4)^2).  The absolute density is only known to this H0 band.")

# =================================================================================
# (2) GALAXY-SIDE PREDICTION  rho_DE = 4 a0^2 / (G c^2)   [framework]
# =================================================================================
anchor = json.load(open(os.path.join(LEDGER, "anchor_values.json")))
a0_canon, a0_alt = anchor["a0_canon"], anchor["a0_alt"]
slope = json.load(open(os.path.join(A0DIR, "fire_slope_results.json")))
bg = slope["budget_gas"]
a0_meas, a0_med, a0_err = bg["a0hat"], bg["a0med"], bg["tot"]   # GLS / median / tot sigma

print("\n" + bar); print("(2) GALAXY-SIDE:  rho_DE = 4 a0^2 / (G c^2)   [Lambda = 32pi a0^2/c^4]"); print(bar)
gal = {}
rows = [
    ("canonical a0 = cH_Lambda/Z  [CIRCULAR: a0 DEFINED from Planck Lambda]", a0_canon, None),
    ("alt a0 (rho_total/cH0)                                              ", a0_alt,   None),
    ("MEASURED a0  GLS gas-dom  [Lambda-BLIND: the GENUINE test]          ", a0_meas,  a0_err),
    ("MEASURED a0  median variant                                        ", a0_med,   None),
]
for lab, a0v, err in rows:
    r = rho_DE_from_a0(a0v)
    entry = dict(a0=a0v, rho_DE=r)
    if err is not None:
        # sigma_ln(rho) = 2 * sigma_ln(a0)   (rho ~ a0^2)
        s_ln = 2.0 * err / a0v
        entry["rho_DE_err"] = r * s_ln
        entry["s_ln"] = s_ln
        print(f"  {lab}\n     a0 = {a0v:.3e} +/- {err:.2e} ({100*err/a0v:.1f}%)  "
              f"=> rho_DE = {r:.3e} +/- {r*s_ln:.2e} kg/m^3 (sigma_ln = {s_ln:.3f})")
    else:
        print(f"  {lab}\n     a0 = {a0v:.3e}                     "
              f"=> rho_DE = {r:.3e} kg/m^3")
    gal[lab.split()[0] + "_" + lab.split()[1]] = entry

# =================================================================================
# (3) THE CROSS-CHECK  (galaxy vs SNe) + THE CIRCULARITY STATEMENT
# =================================================================================
print("\n" + bar); print("(3) CROSS-CHECK galaxy-side rho_DE  vs  SNe rho_DE   (both H0)"); print(bar)


def compare(a0v, err, sne_H0):
    rg = rho_DE_from_a0(a0v)
    rs = sne[sne_H0]["rho_DE"]
    s_ln_g = (2.0 * err / a0v) if err else 0.0
    s_ln_s = sne[sne_H0]["rho_DE_err"] / rs
    s_ln = np.hypot(s_ln_g, s_ln_s)
    t = np.log(rg / rs) / s_ln if s_ln > 0 else np.nan
    return rg / rs, t


print("  ratio = rho_DE(galaxy) / rho_DE(SNe);  t = ln(ratio)/sigma_ln (combined)")
print(f"  {'a0 footing':<34}{'vs H0=67.4 (Planck)':>26}{'vs H0=73.0 (SH0ES)':>26}")
for lab, a0v, err in rows:
    short = lab.split("[")[0].strip()
    r1, t1 = compare(a0v, err, 67.4)
    r2, t2 = compare(a0v, err, 73.0)
    ts1 = f"{t1:+.2f}s" if err else "  (circ/1pt)" if "canonical" in lab else "     --   "
    ts2 = f"{t2:+.2f}s" if err else "  (circ/1pt)" if "canonical" in lab else "     --   "
    print(f"  {short:<34}{r1:>10.3f}x {ts1:>13}{r2:>10.3f}x {ts2:>13}")

print("\n  --- THE CIRCULARITY (do not manufacture agreement) ---")
r_can_67 = rho_DE_from_a0(a0_canon) / sne[67.4]["rho_DE"]
print(f"  * CANONICAL a0 was DEFINED as cH_Lambda/Z from the Planck Lambda. So its")
print(f"    rho_DE = {rho_DE_from_a0(a0_canon):.3e} is the Planck rho_Lambda BY CONSTRUCTION;")
print(f"    matching it to the SNe rho_DE ({r_can_67:.2f}x at H0=67.4) only re-checks")
print(f"    Planck-vs-SNe Lambda -- it is ALGEBRA RUN BACKWARDS, NOT a framework test.")
print(f"  * MEASURED a0 (SPARC rotation curves, NO Lambda input) is the GENUINE cross-")
print(f"    check. GLS gas-dom lands ~1.4-1.6x the SNe rho_DE (within ~1-1.5 sigma);")
print(f"    the median variant lands ~0.9-1.1x (<~0.3 sigma). Report the real number.")
print(f"  * SARKAR relevance: if galaxies INDEPENDENTLY give the same rho_DE the SNe do,")
print(f"    that is a cross-corroboration of the density Sarkar's SNe-leg critique targets;")
print(f"    the honest spread (measured a0 ~1x-1.6x) is consistent, NOT a clean confirmation.")

# ---- hand-off json for the compute lane -----------------------------------------
out = dict(
    constants=dict(C=C, G=G, MPC=MPC),
    sne=dict(Om=Om, Om_err=Om_err, OL=OL, OL_err=OL_err, q0=q0,
             H0_cases={str(k): v for k, v in sne.items()}),
    galaxy=dict(a0_canon=a0_canon, a0_alt=a0_alt,
                a0_meas_gls=a0_meas, a0_med=a0_med, a0_err=a0_err,
                rho_DE_canon=rho_DE_from_a0(a0_canon),
                rho_DE_alt=rho_DE_from_a0(a0_alt),
                rho_DE_meas_gls=rho_DE_from_a0(a0_meas),
                rho_DE_meas_med=rho_DE_from_a0(a0_med),
                rho_DE_meas_gls_err=rho_DE_from_a0(a0_meas) * 2.0 * a0_err / a0_meas),
    note="rho_DE from SNe is STANDARD LCDM; framework adds galaxy cross-check only. "
         "Canonical a0 comparison is CIRCULAR; measured a0 is the genuine test.")
json.dump(out, open(os.path.join(HERE, "setup_results.json"), "w"), indent=1)
print(f"\n[setup_results.json written -> {HERE}]")
print("EXIT 0: setup computed. Exit code is not a verdict.")
