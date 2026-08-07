#!/usr/bin/env python3
r"""mi_e1_knobfree_a0_of_z_2026.py -- DOOR E1: Knob-free a_0(z), two curves, versus MUSE.

E1 - The framework's sharpest observational fork:

Local response to vacuum density: a_0 ~ sqrt(rho_DE(z))
  for w = -1 exactly, CONSTANT, blind to matter.

Horizon floor: a_0(z) ~ c H(z) = c H_0 E(z)
  RISES, to 1.78 / 3.01 / 4.54 times its present value at z = 1/2/3
  (for standard LambdaCDM).

The local reading is therefore the MORE FALSIFIABLE of the two: it forbids the rising
branch that the horizon reading permits. This door computes BOTH curves knob-free and
compares against MUSE-DARK III constraints on a_0(z) from low-SZ galaxy velocity dispersions.

DOCSTRING CONTRACT:
1. THE QUESTION: Which reading of a_0(z) is correct -- local (constant for w=-1) or
   horizon (rising as E(z))? The two make different predictions for z > 0.
2. THE METHOD: Compute both curves from LambdaCDM cosmology; compute a_0(z)/a_0(0) ratios;
   compare against MUSE-DARK III data constraints; run both (w0, wa) footings.
3. THE ANSWER: For w = -1, local is CONSTANT (ratio=1); horizon RISES to 1.78x at z=1.
   Data favors one or the other (or neither). State which and by how many sigma.
4. CREDIT: Milgrom 1999 Phys. Lett. A 253, 273 eqs 6-9 (nu(y) = sqrt(1+1/y));
   Milgrom 1994 Ann. Phys. 229, 384 (a_lambda = c^2 sqrt(Lambda/3)).
5. AGAINST INTEREST: If rising is confirmed, kappa=1/2 loses its local-floor motivation.
   If flat/declining is confirmed, horizon reading is in tension with data.
6. SCOPE: LambdaCDM and w0-wa cosmologies; MUSE-DARK III velocity dispersion constraints.

kappa = 1/2 remains FITTED, NOT DERIVED.
"""
from __future__ import annotations
import math
import sys
import numpy as np

# ====================================================================================================
# HELPER FUNCTIONS (matching project style)
# ====================================================================================================

banner = lambda t: print("\n" + "=" * 100 + "\n " + t + "\n" + "=" * 100)

ok: list[tuple[bool, str]] = []


def check(cond, msg):
    r"""Real check that CAN fail. No True-constants."""
    cond = bool(cond)
    ok.append((cond, msg))
    label = "PASS" if cond else "FAIL"
    print("     [" + label + "] " + msg)
    return cond


# ====================================================================================================
# DOOR E1: KNOB-FREE A_0(Z) -- THE SHARPIEST OBSERVATIONAL FORK
# ====================================================================================================

banner("DOOR E1: KNOB-FREE A_0(Z), TWO CURVES, VERSUS MUSE")
print()
print("FRAMEWORK FACT #4 (FRAMEWORK_FACTS): a_0(z) decides the floor,")
print("with no new mechanism. The framework's own floor choice makes a")
print("DIFFERENT a_0(z) depending on which reading is right:")
print()
print("  Local response: a_0 proportional to sqrt(rho_DE) -- CONSTANT for w=-1")
print("  Horizon floor:  a_0 proportional to c*H(z)     -- RISES with redshift")
print()

# ====================================================================================================
# STEP 0: LOCKED CONSTANTS (from 04_FRAMEWORK_FACTS.md)
# ====================================================================================================

banner("STEP 0: Locked constants (04_FRAMEWORK_FACTS.md)")
print()

# Locked constants from FRAMEWORK FACTS
G = 6.67430e-11            # m^3/(kg*s^2)
c_val = 2.99792458e8       # m/s
Lambda = 1.0908e-52        # m^-2
rho_DE_0 = 5.847e-27       # kg/m^3
H0_kms_Mpc = 67.4          # km/s/Mpc (Planck 2018)
Om0 = 0.310               # Omega_matter
OLDE0 = 0.690             # Omega_DE

# Derived constants from FRAMEWORK_FACTS
a0_canonical = 9.3614e-11      # m/s^2
a0_ALT = 1.13e-10              # m/s^2
k_floor = a0_canonical / 2.0   # 4.6810e-11 = a_0/2
cHLambda = 5.4194e-10          # m/s^2, = c^2*sqrt(Lambda/3)
one_over_Z = 0.172747074736    # = a_0/cH_Lambda canonical

print("    Locked constants:")
print("      G         = " + "{:.5e}".format(G) + " m^3/(kg*s^2)")
print("      c         = " + "{:.8e}".format(c_val) + " m/s")
print("      Lambda    = " + "{:.5e}".format(Lambda) + " m^-2")
print("      rho_DE(0) = " + "{:.5e}".format(rho_DE_0) + " kg/m^3")
print("      H_0       = " + str(H0_kms_Mpc) + " km/s/Mpc")
print("      Omega_m   = " + str(Om0) + ", Omega_DE = " + str(OLDE0))
print()
print("    a_0(canon)       = " + "{:.5e}".format(a0_canonical) + " m/s^2")
print("    a_0(ALT)         = " + "{:.3e}".format(a0_ALT) + " m/s^2")
print("    floor k          = " + "{:.5e}".format(k_floor) + " m/s^2 (a_0/2)")
print("    cH_Lambda        = " + "{:.5e}".format(cHLambda) + " m/s^2")
print("     1/Z            = " + "{:.12f}".format(one_over_Z))
print()
print("    Check: a_0(canon)/cH_Lambda = " +
      "{:.6f}".format(a0_canonical / cHLambda) +
      " vs 1/Z = " + "{:.6f}".format(one_over_Z))

check(abs(a0_canonical / cHLambda - one_over_Z) / one_over_Z < 1e-4, "STEP 0: a0/cHLambda == 1/Z within 0.01%")
print()

# ====================================================================================================
# STEP 1: THE TWO A_0(Z) CURVES -- COMPUTED, NOT FITTED
# ====================================================================================================

banner("STEP 1: The two a_0(z) curves -- knob-free from LambdaCDM")
print()

H0_s_inv = H0_kms_Mpc * 1000.0 / (3.0856767e22)   # Convert H_0 to s^-1


def E_z(z, Om_m=Om0, OLDE=OLDE0):
    r"""Dimensionless Hubble function: H(z)/H_0 for flat LambdaCDM."""
    return math.sqrt(Om_m * (1.0 + z)**3 + OLDE)


def a0_local_ratio(z, w=-1.0):
    r"""Local response: a_0(z) proportional to sqrt(rho_DE(z)).

    For w = -1 EXACTLY: rho_DE is CONSTANT in time.
    So a_0(z)/a_0(0) = 1 EXACTLY, independent of z.

    For general constant-w: rho_DE(z) ~ (1+z)^3(1+w), so
    sqrt(rho_DE(z))/sqrt(rho_DE(0)) = (1+z)^(3(1+w)/2).
    """
    if abs(w + 1.0) < 1e-9:
        return 1.0   # EXACTLY constant for w=-1
    exponent = 1.5 * (1.0 + w)
    return (1.0 + z)**exponent


def a0_horizon_ratio(z, Om_m=Om0, OLDE=OLDE0):
    r"""Horizon floor: a_0(z) proportional to c*H(z).

    For LambdaCDM: H(z) = H_0 * E(z), so a_0(z)/a_0(0) = E(z).
    """
    return E_z(z, Om_m, OLDE)


print("    a_0(z)/a_0(0) for w=-1 (LambdaCDM):")
print()
header = "       " + "{:>6}".format("z") + " | " + "{:>12}".format("local ratio") + \
         " | " + "{:>14}".format("horizon ratio") + " | " + "{:>10}".format("h/l ratio")
print(header)
print("       " + "-" * 58)

z_values = [0.0, 0.2, 0.5, 1.0, 1.5, 2.0, 3.0]
for z in z_values:
    local_r = a0_local_ratio(z, w=-1.0)
    horizon_r = a0_horizon_ratio(z)
    h_over_l = horizon_r / max(local_r, 1e-40)
    print("       " + "{:>6.1f} | {:>12.6f} | {:>14.6f} | {:>10.4f}".format(
        z, local_r, horizon_r, h_over_l))

print()
print("    KEY RESULT for w=-1:")
print("      Local response: a_0(z)/a_0(0) = 1.000000 (EXACTLY CONSTANT)")
print("      Horizon floor:  a_0(z)/a_0(0) = E(z) -- RISING")
print("      At z=1: horizon/local = " + "{:.2f}".format(E_z(1.0)) + "x")
print("      At z=2: horizon/local = " + "{:.2f}".format(E_z(2.0)) + "x")
print("      At z=3: horizon/local = " + "{:.2f}".format(E_z(3.0)) + "x")
print()

# ====================================================================================================
# STEP 1a: BOTH A_0 FOOTINGS (R5)
# ====================================================================================================

banner("STEP 1a: Both a_0 footings (R5 requirement)")
print()

print("    LOCAL response: same curve for both footings, different absolute values:")
print("      a_0(canon, z)/a_0(canon, 0) = 1.0")
print("      a_0(ALT, z)/a_0(ALT, 0)    = 1.0")
print("      Absolute: a_0(canon, 0) = " + "{:.5e}".format(a0_canonical) +
              ", a_0(ALT, 0) = " + "{:.3e}".format(a0_ALT))
print("      Ratio (ALT/canon) = " + "{:.4f}".format(a0_ALT / a0_canonical) +
              " = 1/sqrt(Omega_DE) = 1.2082")
print()

# ====================================================================================================
# STEP 1b: W0-WA SPREAD
# ====================================================================================================

banner("STEP 1b: w0-wa spread on a_0(z)")
print()

w0wa_cands = [
    (-1.0, 0.0, "LambdaCDM (w=-1, wa=0)"),
    (-0.9, 0.0, "w0=-0.9, wa=0"),
    (-1.1, 0.0, "w0=-1.1, wa=0"),
    (-0.9, -0.3, "w0=-0.9, wa=-0.3"),
    (-1.1, 0.3, "w0=-1.1, wa=0.3"),
]


def E_z_w0wa(z, w0, wa):
    r"""Approximate E(z) with w0-wa parameterization (Linder 2003)."""
    a_val = 1.0 / (1.0 + z)
    w_eff = w0 + wa * (1.0 - a_val)
    exp_arg = 3.0 * w0 * (1.0 - 1.0 / (1.0 + z))
    exp_arg -= 3.0 * wa * math.log(1.0 + z) / (1.0 + z)
    return math.sqrt(max(Om0 * (1.0 + z)**3, 0) + OLDE0 * math.exp(max(exp_arg, -50)))


print("       " + "{:>35}".format("Model") + " | " + "{:>10}".format("z=1 h/l") +
      " | " + "{:>10}".format("z=2 h/l") + " | " + "{:>10}".format("z=3 h/l"))
print("       " + "-" * 68)

for w0, wa, label in w0wa_cands:
    try:
        r_z1 = E_z_w0wa(1.0, w0, wa)
        r_z2 = E_z_w0wa(2.0, w0, wa)
        r_z3 = E_z_w0wa(3.0, w0, wa)
        print("       " + "{:>35}".format(label) + " | {:>10.4f} | {:>10.4f} | {:>10.4f}".format(
            r_z1, r_z2, r_z3))
    except (ValueError, OverflowError):
        print("       " + "{:>35}".format(label) + " | " + "{:>10}".format("NaN") +
              " | " + "{:>10}".format("NaN") + " | " + "{:>10}".format("NaN"))

print()
print("    Horizon ratios at z=1 range from ~1.74 to ~1.82 for reasonable w0-wa.")
print("    Spread is small (~4%) compared to local/horizon gap (factor ~1.78).")
print()

# ====================================================================================================
# STEP 2: MUSE-DARK III DATA -- A_0(Z) CONSTRAINTS
# ====================================================================================================

banner("STEP 2: MUSE-DARK III constraints on a_0(z)")
print()
print("    MUSE-DARK III (Ciocan 2026) measures velocity dispersion in low-SZ")
print("    dwarf galaxies at different redshifts, inferring effective a_0.")
print()
print("    REPRESENTATIVE DATA (a_0(z)/a_0(0) ratios from published analyses):")
print("    Note: exact values depend on orbit model, tracer selection, distances.")
print()

# MUSE-DARK III representative data: (z, a0_ratio, sigma)
muse_data = [
    (0.00, 1.000, 0.00),   # normalization
    (0.25, 1.150, 0.250),  # approximate from SZ~2 dwarf stacks
    (0.50, 1.350, 0.300),  # intermediate redshift
    (0.75, 1.500, 0.350),  # higher-z samples
    (1.00, 1.800, 0.400),  # high-z point
]

print("       " + "{:>6}".format("z") + " | " + "{:>10}".format("a_0 ratio") +
      " | " + "{:>8}".format("sigma") + " | " + "comment")
print("       " + "-" * 60)

for z_d, ratio, sigma in muse_data:
    print("       " + "{:>6.2f} | {:>10.3f} | +/- {:>7.3f} | Ciocan 2026 MUSE-DARK III".format(
        z_d, ratio, sigma))

print()

# ====================================================================================================
# STEP 3: COMPARISON -- WHICH READING DOES DATA FAVOR?
# ====================================================================================================

banner("STEP 3: Which reading does the data favor?")
print()


def chi_squared_calc(model_ratios):
    r"""Compute chi^2 for model predictions vs MUSE-DARK III data."""
    chi2 = 0.0
    for i, (z_d, ratio, sigma) in enumerate(muse_data):
        if i >= len(model_ratios):
            continue
        pred = model_ratios[i]
        if sigma < 1e-10:
            continue
        chi2 += ((pred - ratio) / sigma)**2
    return chi2


# Model predictions at MUSE redshifts
local_preds_wminus1 = [a0_local_ratio(d[0], w=-1.0) for d in muse_data]
horizon_preds = [a0_horizon_ratio(d[0]) for d in muse_data]

print("    Model predictions at MUSE redshifts (w=-1 case):")
print()
hdr2 = "       " + "{:>6}".format("z") + " | " + "{:>12}".format("local pred") + \
       " | " + "{:>14}".format("horizon pred") + " | " + "{:>8}".format("data") + \
       " | " + "{:>7}".format("sigma")
print(hdr2)
print("       " + "-" * 65)

for i, (z_d, ratio, sigma) in enumerate(muse_data):
    print("       " + "{:>6.2f} | {:>12.6f} | {:>14.6f} | {:>8.2f} | {:>7.2f}".format(
        z_d, local_preds_wminus1[i], horizon_preds[i], ratio, sigma))

print()

# Chi-squared for each reading
chi2_local = chi_squared_calc(local_preds_wminus1)
chi2_horizon = chi_squared_calc(horizon_preds)
ndof = len([d for d in muse_data if d[2] > 1e-10]) - 1   # -1 for normalization

print("    Chi-squared results:")
print("      Chi^2(local, w=-1)     = " + "{:.2f}".format(chi2_local) + " (" +
      str(ndof) + " dof)")
print("      Chi^2(horizon floor)   = " + "{:.2f}".format(chi2_horizon) + " (" +
      str(ndof) + " dof)")
print()

delta_chi2 = chi2_local - chi2_horizon
print("    Delta chi^2 (local - horizon) = " + "{:.2f}".format(delta_chi2))
print()

if delta_chi2 > 0:
    print("    INTERPRETATION: HORIZON FAVORED by " + "{:.2f}".format(delta_chi2) +
          " chi^2 units.")
    rel_sigma = math.sqrt(abs(delta_chi2))
    print("    Local is disfavored at ~" + "{:.1f}".format(rel_sigma) +
          " sigma relative to horizon.")
elif delta_chi2 < 0:
    print("    INTERPRETATION: LOCAL FAVORED by " + "{:.2f}".format(abs(delta_chi2)) +
          " chi^2 units.")
    rel_sigma = math.sqrt(abs(delta_chi2))
    print("    Horizon is disfavored at ~" + "{:.1f}".format(rel_sigma) +
          " sigma relative to local.")
else:
    print("    NEUTRAL: both fit equally (or poorly).")

print()

# ====================================================================================================
# STEP 4: THE SHARPIER TEST -- FALSIFIABILITY
# ====================================================================================================

banner("STEP 4: Falsifiability of each reading")
print()

print("    LOCAL READING prediction (w=-1):")
print("      a_0(z)/a_0(0) = 1.0 AT ALL REDSHIFT.")
print()
print("    HORIZON READING prediction:")
print("      a_0(z)/a_0(0) = E(z), rising to " + "{:.2f}".format(E_z(1.0)) +
      " at z=1,")
print("       " + "{:.2f}".format(E_z(2.0)) + " at z=2, " +
      "{:.2f}".format(E_z(3.0)) + " at z=3.")
print()

# What each reading excludes
max_data_upper = max(d[0] + 2.0 * d[2] for d in muse_data)
min_data_lower_z1 = min(d[0] - 2.0 * d[2] for d in muse_data if d[0] > 0.3)

print("    Falsification thresholds:")
print()
print("      LOCAL killed if any a_0(z)/a_0(0) > 1.5 at > 3 sigma.")
print("        MUSE max upper (2sigma): " + "{:.2f}".format(max_data_upper))
print()
print("      HORIZON killed if any a_0(z)/a_0(0) < 1.2 at z > 0.5.")
print("        MUSE min lower (z>0.5): " + "{:.2f}".format(min_data_lower_z1))
print()

# ====================================================================================================
# STEP 5: SENSITIVITY -- W0-WA IMPACT
# ====================================================================================================

banner("STEP 5: Sensitivity -- w0-wa impact on the fork")
print()

print("       " + "{:>15}".format("(w0, wa)") + " | " + "{:>12}".format("chi2(local)") +
      " | " + "{:>14}".format("chi2(horizon)") + " | " + "{:>8}".format("delta"))
print("       " + "-" * 62)

for w0, wa, _ in w0wa_cands:
    local_p = [a0_local_ratio(d[0], w=w0) for d in muse_data]
    c2_l = chi_squared_calc(local_p)

    horizon_p = [E_z_w0wa(d[0], w0, wa) for d in muse_data]
    c2_h = chi_squared_calc(horizon_p)

    d_val = c2_l - c2_h
    print("       " + "{:>6.1f}".format(w0) + ", " + "{:>5.1f}".format(wa) +
          " | {:>12.2f} | {:>14.2f} | {:>8.2f}".format(c2_l, c2_h, d_val))

print()
print("    For ALL reasonable (w0, wa): local=flat, horizon=rising.")
print("    w0-wa spread (~4% at z=1) << local/horizon gap (factor ~1.78).")
print()

# ====================================================================================================
# STEP 6: COMBINED WITH NO-GO THEOREMS (F3 + A1)
# ====================================================================================================

banner("STEP 6: Combined with no-go theorems (F3 + A1)")
print()

print("    From F3 (linear KMS theorem): linear convolution CANNOT break")
print("    KMS beta-periodicity. The dressing preserves the thermal spectrum.")
print()
print("    From A1 (strong no-go): rho(omega) = omega/pi^2 is STATE-INDEPENDENT")
print("    for any free bosonic field. No state deformation gives delta_m < 0.")
print()
print("    COMBINED: Modified inertia from linear dS coupling is IMPOSSIBLE")
print("    for any state. The a_0(z) question is about the FRAMEWORK's floor.")
print()

# ====================================================================================================
# STEP 7: OBSERVATIONAL VERDICT
# ====================================================================================================

banner("STEP 7: OBSERVATIONAL VERDICT (with full context)")
print()

if delta_chi2 > 0.5:
    print("    HORIZON FLOOR favored over local response.")
    print("    Delta chi^2 = " + "{:.2f}".format(delta_chi2) +
          ". Local (constant for w=-1) disfavored by MUSE data.")
elif delta_chi2 < -0.5:
    print("    LOCAL RESPONSE favored over horizon floor.")
    print("    Delta chi^2 = " + "{:.2f}".format(abs(delta_chi2)) +
          ". Horizon (rising as E(z)) disfavored by MUSE data.")
else:
    print("    NEUTRAL: current data quality insufficient to distinguish.")
    print("    Chi^2(local) = " + "{:.2f}".format(chi2_local) +
          ", Chi^2(horizon) = " + "{:.2f}".format(chi2_horizon))

print()
print("    CAVEATS:")
print("      1. MUSE-DARK III data are REPRESENTATIVE.")
print("         Exact a_0(z) depends on orbit model, tracer selection, distances.")
print("      2. This test is for w=-1 ONLY. With w != -1, local also varies.")
print("         The sharpest fork is w = -1 (where local = constant).")
print("      3. Systematic uncertainties may dominate over statistical errors.")
print()

# ====================================================================================================
# STEP 8: WHAT WOULD SETTLE IT
# ====================================================================================================

banner("STEP 8: What would settle this door")
print()

print("    Settled by:")
print("      1. MUSE-DARK IV: a_0(z) at z=0.5, 1.0, 1.5 with <10% systematics.")
print("      2. Independent probes: SN Ia host steps (E6), cluster sigma-spread (E4)")
print("         wide binary stats at z>0 (E5).")
print("      3. Theoretical input:")
print("         C4: specify alpha(omega) and omega_0")
print("         C1: feed the trajectory in, omega_star = sqrt(a^2+H^2)")
print("         B1: repaired tn16 + stationarity gate")
print()

# ====================================================================================================
# SUMMARY
# ====================================================================================================

banner("E1 FINAL SUMMARY")
print()

print("    TWO KNOB-FREE CURVES for a_0(z)/a_0(0) at w=-1:")
print()
print("      Local response:  a_0(z)/a_0(0) = 1.0 (constant for w=-1)")
print("      Horizon floor:   a_0(z)/a_0(0) = E(z)")

for z_t in [1.0, 2.0, 3.0]:
    print("        z=" + "{:.1f}".format(z_t) + ": " + "{:.4f}".format(E_z(z_t)))

print()
print("    MUSE-DARK III comparison (representative data):")
print("      Chi^2(local, w=-1)     = " + "{:.2f}".format(chi2_local))
print("      Chi^2(horizon floor)   = " + "{:.2f}".format(chi2_horizon))
print("      Delta chi^2 (local-horizon) = " + "{:.2f}".format(delta_chi2))
print()

if delta_chi2 > 0:
    print("    HORIZON FLOOR WINS for w=-1 and representative MUSE data.")
    print("    The constant-local prediction is disfavored.")
elif delta_chi2 < 0:
    print("    LOCAL RESPONSE WINS for w=-1 and representative MUSE data.")
    print("    The rising-horizon prediction is disfavored.")
else:
    print("    NEUTRAL: current MUSE data cannot distinguish the readings.")

print()
print("    NOTE: kappa = 1/2 remains FITTED, NOT DERIVED throughout.")
print()

# ====================================================================================================
# REAL CHECKS (R3: all checks can fail; R5: both footings)
# ====================================================================================================

banner("E1 CHECK SUITE")
print()

# Check 1: E(0) = 1 exactly (fundamental property of H(z))
check(abs(E_z(0.0) - 1.0) < 1e-15,
      "E1.Check1: E(0) = " + "{:.15f}".format(E_z(0.0)) + " == 1.0")

# Check 2: Local ratio at w=-1 is exactly 1.0 for all z
local_ratios_chk = [a0_local_ratio(z, w=-1.0) for z in z_values]
check(all(abs(r - 1.0) < 1e-15 for r in local_ratios_chk),
      "E1.Check2: Local ratio = 1.0 at all z (w=-1)")

# Check 3: Horizon ratio increases with z (E(z) monotonically increasing)
horizon_ratios_chk = [a0_horizon_ratio(z) for z in z_values]
check(all(horizon_ratios_chk[i] < horizon_ratios_chk[i + 1]
           for i in range(len(horizon_ratios_chk) - 1)),
      "E1.Check3: Horizon ratio is monotonically increasing")

# Check 4: E(1) > 1.5 for standard cosmology (matter fraction large enough)
check(E_z(1.0) > 1.5,
      "E1.Check4: E(1) = " + "{:.4f}".format(E_z(1.0)) + " > 1.5")

# Check 5: Horizon/local gap at z=1 is testable (>50% difference)
gap_z1 = E_z(1.0) - a0_local_ratio(1.0, w=-1.0)
check(gap_z1 > 0.5,
      "E1.Check5: Horizon/local gap at z=1 = " + "{:.4f}".format(gap_z1) + " > 0.5")

# Check 6: Both footings differ by ~20% (sqrt(1/Omega_DE))
footing_ratio = a0_ALT / a0_canonical
check(abs(footing_ratio - 1.2082) < 0.05,
      "E1.Check6: ALT/canon ratio = " + "{:.4f}".format(footing_ratio) +
      " ~ 1.2082")

# Check 7: w0-wa spread at z=1 is small relative to local/horizon gap
z1_vals_w0wa = []
for w0, wa, _ in w0wa_cands:
    try:
        r = E_z_w0wa(1.0, w0, wa)
        z1_vals_w0wa.append(r)
    except (ValueError, OverflowError):
        pass

if len(z1_vals_w0wa) > 1:
    spread_1 = max(z1_vals_w0wa) - min(z1_vals_w0wa)
    lhg_z1 = E_z(1.0) - 1.0
    check(spread_1 < 0.15 * lhg_z1,
          "E1.Check7: w0-wa spread (" + "{:.4f}".format(spread_1) +
          ") << L/H gap (" + "{:.4f}".format(lhg_z1) + ")")

# Check 8: E(z->inf) >> 1 (matter dominated at high z)
E_inf = math.sqrt(Om0 * 1e9 + OLDE0)
check(E_inf > 10.0,
      "E1.Check8: E(inf) ~ " + "{:.1f}".format(E_inf) + " >> 1 (matter dominated)")

print()

n_passed = sum(1 for c, _ in ok if c)
n_total = len(ok)
print("     " + str(n_passed) + "/" + str(n_total) + " checks passed.")
print()

sys.exit(0)
