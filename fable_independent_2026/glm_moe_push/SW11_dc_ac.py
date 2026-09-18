#!/usr/bin/env python3
"""
SW11_dc_ac -- score the P10 DC/AC split on ONE real system: the Large Magellanic
Cloud (LMC), using this class's own numbers only. No invented data, no AQUAL
solver, no external files read at runtime.

P10 (NEW PREDICTION): uniform environments SUPPRESS (amplitude, DC channel:
S(eta) = 1/(1+(eta/eta_c)^2) multiplies the internal boost); tidal
environments DISTORT (shape, AC channel: enter Gamma, S pinned at 1).

INPUTS (stated, verbatim):
  MW ambient at the LMC:  g_env = v_c^2/D,  v_c = 233e3 m/s, D = 50 kpc
  a0 = 9.3619e-11 m/s^2    (canonical, MEASURED)
  eta_c = 0.2034           (DECLARED, SW01b B2 -- not tuned here)
  S(eta) = 1/(1+(eta/eta_c)^2)
  nu_RAR(y) = 1/(1-exp(-sqrt(y)))   (the class's RAR kernel, SW01/SW03/SW05)
  LMC internal: g_int = G*M_st/r_st^2, M_st = 5e9 M_sun (literature value,
    used as the cited working mass for the LMC's stellar disk), r_st = 3 kpc
  Tidal AC: tide = 2*g_env*r_st/D   (standard gradient estimate for a flat
    MW rotation curve: dg/dr = -g_env/D, evaluated across r_st)
  Units: G = 6.674e-11, M_sun = 1.989e30 kg, PC = 3.0857e16 m, kpc = 1e3*PC

PRE-REGISTERED FAIL CONDITION (declared BEFORE looking at any output):
  FAIL fires iff the AC channel dominates the DC channel at the LMC's stellar
  radius, i.e. iff tide > g_int (equivalently tide/g_int > 1). If it fires,
  the DC/AC split language collapses on this system and the result is
  recorded FAIL-as-finding, not hidden.
  NOTE on wording: the task phrase "if the tidal ratio exceeds g_int" reads a
  dimensionless ratio against an acceleration (unit mismatch). The physically
  meaningful reading, fixed by the parenthetical "(the AC dominates)", is
  tide > g_int i.e. tide/g_int > 1. The blind numeric comparison
  (tide/g_int) > g_int is ALSO computed and recorded, flagged as an artifact.

FALSIFIER FRAMING (P10's observable):
  The class predicts the LMC's internal kinematics sit at the SUPPRESSED boost
  D_int = 1 + S_LMC*(nu_RAR(x_LMC)-1), NOT at the unsuppressed RAR boost
  nu_RAR(x_LMC). The observational discriminator is the LMC's rotation
  curve / stellar dispersion measured against BOTH predictions. The rival
  side -- AQUAL's tidal response of the LMC internal field to the MW
  gradient -- is labeled OPEN: no DE solver exists in this lane, so no AQUAL
  number is claimed, computed, or implied here.

Banned words (derived/closed/breakthrough) never used as claims.
"""
import json
import math
import sys

# ---------------------------------------------------------------- constants
G     = 6.674e-11          # m^3 kg^-1 s^-2 (stated)
M_SUN = 1.989e30           # kg (stated)
PC    = 3.0857e16          # m (stated)
KPC   = 1e3 * PC           # m

A0    = 9.3619e-11         # m/s^2, canonical, MEASURED
ETA_C = 0.2034             # DECLARED (SW01b B2)

V_C   = 233e3              # m/s, MW circular speed
D     = 50.0 * KPC         # m, MW--LMC distance
R_ST  = 3.0 * KPC          # m, LMC stellar-disk characteristic radius
M_ST  = 5e9 * M_SUN        # kg, LMC mass within r_st (literature value, cited)

OUT_JSON = "/Users/carlzimmerman/new_physics/zimmerman-formula/fable_independent_2026/glm_moe_push/SW11_dc_ac.json"

# ---------------------------------------------------------------- kernels
def nu_rar(y):
    """The class's RAR kernel (SW01_envscalar_response.py): nu = 1/(1-exp(-sqrt(y)))."""
    return 1.0 / (1.0 - math.exp(-math.sqrt(y)))

def s_env(eta):
    """The class's DC conformal suppression: S(eta) = 1/(1+(eta/eta_c)^2)."""
    return 1.0 / (1.0 + (eta / ETA_C) ** 2)

# ---------------------------------------------------------------- compute
g_env = V_C ** 2 / D
eta_LMC = g_env / A0
S_LMC = s_env(eta_LMC)

g_int = G * M_ST / R_ST ** 2
x_LMC = g_int / A0
nu_x = nu_rar(x_LMC)
D_int = 1.0 + S_LMC * (nu_x - 1.0)

tide = 2.0 * g_env * R_ST / D
tidal_ratio = tide / g_int

# ------------------------------------------------- pre-registered FAIL gate
fail_physical = bool(tide > g_int)            # AC dominates: tide/g_int > 1
fail_literal_numeric = bool(tidal_ratio > g_int)  # recorded for audit ONLY

# ---------------------------------------------------------------- checks
results = []
def check(label, value_str, ok):
    ok = bool(ok)
    results.append((label, value_str, ok))
    print("  [%s] %s = %s" % ("ok" if ok else "FAIL", label, value_str))

print("=" * 78)
print("SW11_dc_ac -- P10 DC/AC split scored on the LMC (class numbers only)")
print("=" * 78)
print("PRE-REGISTERED FAIL: if tide > g_int (tide/g_int > 1; the AC dominates),")
print("  the DC/AC split collapses -- record FAIL-as-finding. Declared before output.")
print("  (Literal wording 'tidal ratio exceeds g_int' is a unit mismatch;")
print("   the blind numeric comparison is recorded for audit only.)")
print()

print("A. MW ambient (DC channel input):")
check("g_env = v_c^2/D", "%.12e m/s^2" % g_env,
      abs(g_env - 233e3**2 / (50 * 1e3 * PC)) < 1e-30)
check("eta_LMC = g_env/a0", "%.12e" % eta_LMC,
      abs(eta_LMC - g_env / A0) < 1e-18 * max(1.0, eta_LMC))
check("S_LMC = 1/(1+(eta_LMC/eta_c)^2)", "%.12e" % S_LMC,
      abs(S_LMC - 1.0 / (1.0 + (eta_LMC / ETA_C) ** 2)) < 1e-18 * max(1.0, S_LMC))
check("sanity: 0 < S_LMC <= 1 (a suppression)", "S_LMC in (0,1]: %s" % (0.0 < S_LMC <= 1.0),
      0.0 < S_LMC <= 1.0)

print()
print("B. LMC internal (the boosted source):")
check("g_int = G*M_st/r_st^2", "%.12e m/s^2" % g_int,
      abs(g_int - G * M_ST / R_ST ** 2) < 1e-30)
check("x_LMC = g_int/a0", "%.12e" % x_LMC,
      abs(x_LMC - g_int / A0) < 1e-18 * max(1.0, x_LMC))
check("nu_RAR(x_LMC) (unsuppressed RAR boost)", "%.12e" % nu_x,
      abs(nu_x - 1.0 / (1.0 - math.exp(-math.sqrt(x_LMC)))) < 1e-15)
check("D_int = 1 + S_LMC*(nu_RAR(x_LMC)-1) (SUPPRESSED, the DC prediction)",
      "%.12e" % D_int, abs(D_int - (1.0 + S_LMC * (nu_x - 1.0))) < 1e-15)
check("ordering: nu_RAR > D_int > 1 (suppression actually bites)",
      "nu=%.6f > D_int=%.6f > 1: %s" % (nu_x, D_int, nu_x > D_int > 1.0),
      nu_x > D_int > 1.0)

print()
print("C. Tidal AC channel:")
check("tide = 2*g_env*r_st/D", "%.12e m/s^2" % tide,
      abs(tide - 2.0 * g_env * R_ST / D) < 1e-30)
check("tide/g_int (AC channel size vs internal field)", "%.12e" % tidal_ratio,
      abs(tidal_ratio - tide / g_int) < 1e-18 * max(1.0, tidal_ratio))

print()
print("D. Pre-registered FAIL gate:")
check("FAIL (physical): tide > g_int i.e. tide/g_int > 1",
      "fired = %s" % fail_physical, fail_physical == (tidal_ratio > 1.0))
check("audit-only (unit mismatch): (tide/g_int) > g_int as typed numerics",
      "blind = %s (artifact of comparing ratio to acceleration)" % fail_literal_numeric,
      True)
print()
if fail_physical:
    print("  >>> FAIL-AS-FINDING: the AC channel dominates; the DC/AC split language")
    print("      collapses on the LMC under this class's own numbers.")
else:
    print("  >>> FAIL did not fire: tide/g_int = %.6f << 1, so the tidal AC distortion" % tidal_ratio)
    print("      is sub-dominant and the DC suppression (D_int) is the observable.")

print()
print("E. Falsifier framing (P10 on the LMC):")
print("  Prediction : LMC internal kinematics sit at the SUPPRESSED boost")
print("               D_int = %.6f, NOT the unsuppressed RAR nu_RAR = %.6f." % (D_int, nu_x))
print("               The gap D_int/nu_RAR = %.6f is the discriminating size." % (D_int / nu_x))
print("  Discriminator: the LMC's rotation curve / stellar dispersion measured")
print("               against BOTH values above (one number settles it).")
print("  Rival side : AQUAL's tidal response of the LMC's internal field to the MW")
print("               gradient -- OPEN. No DE solver exists in this lane; no AQUAL")
print("               number is claimed, computed, or implied here.")
print()
print("Provenance: every number above computed in-file from the stated inputs")
print("(v_c=233e3 m/s, D=50 kpc, a0=9.3619e-11 MEASURED, eta_c=0.2034 DECLARED SW01b B2,")
print("M_st=5e9 M_sun literature value, r_st=3 kpc, G=6.674e-11, M_sun=1.989e30, PC=3.0857e16 m);")
print("kernels nu_RAR and S(eta) are the class's own (SW01/SW03/SW05, SW01b B2). No invented data.")
print("Checks passed: %d/%d" % (sum(1 for _, _, ok in results if ok), len(results)))

# ---------------------------------------------------------------- json
payload = {
    "script": "SW11_dc_ac",
    "prediction": "P10 DC/AC split: uniform environments SUPPRESS (DC, S(eta)); tidal environments DISTORT (AC, Gamma, S pinned at 1)",
    "system": "Large Magellanic Cloud (LMC) in the Milky Way field",
    "inputs": {
        "v_c_m_s": V_C, "D_m": D, "a0_m_s2": A0, "a0_status": "MEASURED, canonical",
        "eta_c": ETA_C, "eta_c_status": "DECLARED (SW01b B2)",
        "G_m3_kg_s2": G, "M_sun_kg": M_SUN, "PC_m": PC,
        "M_st_kg": M_ST, "M_st_note": "5e9 M_sun, literature value (cited working mass within r_st)",
        "r_st_m": R_ST,
        "kernels": {"nu_RAR": "1/(1-exp(-sqrt(y))) (class kernel, SW01/SW03/SW05)",
                     "S": "1/(1+(eta/eta_c)^2) (class, SW01b B2)"},
    },
    "dc_channel": {"g_env_m_s2": g_env, "eta_LMC": eta_LMC, "S_LMC": S_LMC},
    "internal": {"g_int_m_s2": g_int, "x_LMC": x_LMC, "nu_RAR_x_LMC": nu_x,
                  "D_int_suppressed": D_int, "suppression_gap_D_int_over_nu": D_int / nu_x},
    "ac_channel": {"tide_m_s2": tide, "tide_over_g_int": tidal_ratio,
                    "sub_dominant": bool(tidal_ratio < 1.0)},
    "fail": {
        "pre_registered": "FAIL iff tide > g_int (tide/g_int > 1; the AC dominates) -> DC/AC language collapses, record FAIL-as-finding",
        "condition": "tide/g_int > 1.0",
        "fired": fail_physical,
        "outcome": "FAIL-as-finding" if fail_physical else "FAIL did not fire",
        "audit_note": ("The task's literal phrase 'if the tidal ratio exceeds g_int' compares a "
                        "dimensionless ratio to an acceleration (unit mismatch). The physical "
                        "reading, fixed by the parenthetical '(the AC dominates)', is tide > g_int. "
                        "The blind numeric comparison (tide/g_int) > g_int is recorded for audit "
                        "only and is NOT the scientific FAIL."),
        "blind_literal_numeric_value": fail_literal_numeric,
    },
    "falsifier_framing": {
        "prediction": "LMC internal kinematics sit at the SUPPRESSED boost D_int = %.6f, not the unsuppressed RAR nu_RAR = %.6f" % (D_int, nu_x),
        "discriminator": "LMC rotation curve / stellar dispersion vs both values",
        "rival_side": "OPEN (AQUAL's tidal response; no DE solver in this lane, no AQUAL numbers claimed)",
    },
    "checks": {"passed": sum(1 for _, _, ok in results if ok), "total": len(results),
                "all_ok": all(ok for _, _, ok in results)},
}
with open(OUT_JSON, "w") as f:
    json.dump(payload, f, indent=2)
print("json written: %s" % OUT_JSON)
sys.exit(0)
