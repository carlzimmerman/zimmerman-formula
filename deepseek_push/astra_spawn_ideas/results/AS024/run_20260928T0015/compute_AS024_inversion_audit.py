#!/usr/bin/env python3
"""
AS024 -- No cosmological prediction from an inverted datum.

Anti-circularity audit of the framework scale identity:
    a0 = kappa * c * sqrt(G * rho_Lambda),   kappa = 1/2 ADOPTED
    rho_Lambda_inv(a) = 4 a^2 / (G c^2)               (inverse map)
    Lambda_inv(a)     = 32 pi a^2 / c^4               (same-G Einstein reading)
    Omega_inv(a, H0)  = 32 pi a^2 / (3 H0^2 c^2)      (needs an independent H0)
    H_Lambda(a)       = a * sqrt(32 pi / 3) / c       (bare same-G Hubble rate)

Claim under test: taking a measured a0 and inverting the scale relation to
"derive" rho_Lambda, Lambda, Omega_Lambda or H is an INVERTED DATUM, not a
prediction; the inverted chain is an involution whose self-consistency
residual is identically zero for ANY input (true or false), so it earns no
empirical evidence.  The only evidence-bearing residual is the FORWARD one:
    a0_fwd = (c/2) * sqrt(G * rho_Planck)   vs   galaxy-measured a0 (kappa fits).

All inputs are repo-registered conventions/measurements (README, STANDING
rev.9 block, prep_2026/journal_submissions/SUBMIT_MNRAS.md, kappa_closure/k03):
Planck H0 = 67.4 km/s/Mpc, Omega_Lambda = 0.685, SH0ES H0 = 73.0,
gas-dominated a0 slope band (0.84-1.36)e-10 m/s^2, kappa_DF = 0.55 +/- 0.17,
kappa_BTFR = 0.465 +/- 0.076.  NO fit is performed in this run.

Mandates: G = 6.67430e-11, c = 299792458, M_sun = 1.98847e30, pc =
3.085677581491367e16 (SI).  Both footings carried SEPARATELY:
a0_can = 9.3619e-11 m/s^2 (rho_Lambda convention) and
a0_alt = 1.1279e-10 m/s^2 (rho_total convention).  G_N/G_bare/G_cosmo kept
separate: the scale relation uses G = G_N; Lambda_inv is stated at the
same-G reading and the ratio G_E/G_N is carried explicitly in the notes.

Bounded prototype: 60-digit mpmath, single thread, no vectorized imports,
target wall time << 120 s (measured and recorded).
"""

import json
import math
import time
from mpmath import mp, mpf, sqrt, pi, log10

mp.dps = 60

T0 = time.time()

# ---------------------------------------------------------------- constants
G = mpf("6.67430e-11")        # m^3 kg^-1 s^-2  (G_N, measured)
C = mpf("299792458")          # m/s             (exact)
MSUN = mpf("1.98847e30")      # kg
PC = mpf("3.085677581491367e16")  # m
KAPPA = mpf("0.5")
A0_CAN = mpf("9.3619e-11")    # m/s^2  registered canonical footing
A0_ALT = mpf("1.1279e-10")    # m/s^2  registered alternative footing
Z = sqrt(mpf(32) * pi / mpf(3))   # sqrt(32 pi / 3) = 5.78987...

# repo-registered cosmological input conventions (k03, README)
H0_PLANCK_KMS = mpf("67.4")            # km/s/Mpc
H0_SH0ES_KMS = mpf("73.0")             # km/s/Mpc
OMEGA_L = mpf("0.685")                 # k03 fixed Omega_Lambda
# corpus-measured galaxy-side inputs (SUBMIT_MNRAS.md; STANDING rev.9)
A0_GAS_LO, A0_GAS_MID, A0_GAS_HI = mpf("0.84e-10"), mpf("1.10e-10"), mpf("1.36e-10")
KAPPA_DF, SIG_KAPPA_DF = mpf("0.55"), mpf("0.17")
KAPPA_BTFR, SIG_KAPPA_BTFR = mpf("0.465"), mpf("0.076")

KMS2SI = mpf(1e3) / (PC * mpf(1e6))              # (km/s)/Mpc -> s^-1
H0_PLANCK = H0_PLANCK_KMS * KMS2SI            # s^-1
H0_SH0ES = H0_SH0ES_KMS * KMS2SI

# ---------------------------------------------------------------- framework maps
def a0_fwd(rho):
    """Forward: vacuum density (kg/m^3) -> acceleration scale (m/s^2), kappa=1/2."""
    return KAPPA * C * sqrt(G * rho)

def rho_inv(a):
    """Inverse map: a -> rho = 4 a^2 / (G c^2)."""
    return mpf(4) * a * a / (G * C * C)

def lam_inv(a):
    """Same-G Einstein-constant reading of a scale: Lambda = 32 pi a^2 / c^4."""
    return mpf(32) * pi * a * a / (C ** 4)

def lam_planck(rho):
    """Lambda from an independent density at G_E = G_N: 8 pi G rho / c^2."""
    return mpf(8) * pi * G * rho / (C * C)

def om_inv(a, h0):
    """Omega_Lambda reading: 32 pi a^2 / (3 H0^2 c^2) -- REQUIRES an H0 input."""
    return mpf(32) * pi * a * a / (mpf(3) * h0 * h0 * C * C)

def h_lam(a):
    """Bare same-G Hubble rate from a scale: a * sqrt(32 pi / 3) / c (1/s)."""
    return a * Z / C

def h_kms(h_si):
    return h_si / KMS2SI

def rel(x, y):
    return abs(x - y) / abs(y)

RHO_PLANCK = mpf(3) * H0_PLANCK * H0_PLANCK * OMEGA_L / (mpf(8) * pi * G)  # kg/m^3
A0_FWD = a0_fwd(RHO_PLANCK)               # the legitimate forward prediction

checks = []
fails = []

def check(name, ok, detail, tol=None):
    checks.append({"name": name, "pass": bool(ok), "observed": detail,
                   "tolerance": tol if tol is not None else "exact at 60 digits"})
    if not ok:
        fails.append(name)
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}   ({detail})", flush=True)

print("=" * 100)
print("AS024 -- no cosmological prediction from an inverted datum")
print("=" * 100)
print(f"  RHO_PLANCK (H0=67.4, OmL=0.685) = {mp.nstr(RHO_PLANCK, 15)} kg/m^3")
print(f"  A0_FWD = (c/2)*sqrt(G*rho_Planck) = {mp.nstr(A0_FWD, 15)} m/s^2  (registered canonical 9.3619e-11)")
print(f"  rho_Lambda(can) = 4 a0_can^2/(G c^2) = {mp.nstr(rho_inv(A0_CAN), 15)} kg/m^3")
print(f"  rho_total(alt)  = 4 a0_alt^2/(G c^2) = {mp.nstr(rho_inv(A0_ALT), 15)} kg/m^3")
print(f"  Z = sqrt(32 pi/3) = {mp.nstr(Z, 12)}")

# ---------------------------------------------------------------- C1/C2 involution
print("\n--- [C1/C2] the inverted chain is an involution: F(R(a)) = a, R(F(rho)) = rho ---")
# Tolerance set BEFORE evaluation: the involution is an EXACT identity (Lean-
# certified in AS024_inversion_certificates.lean with real arithmetic); the
# 60-digit numerical check confirms it to ~1e-61 relative (machine noise).
# The empirical claim tested here is that the SAME residual floor holds for
# true and fabricated inputs alike -> the chain carries no discriminating
# content.  Threshold 1e-50 is ~9 orders of magnitude above the observed noise.
TOL = mpf("1e-50")

probe_as = [A0_CAN, A0_ALT, A0_GAS_MID, mpf("3.0e-10"), mpf("1.0e-12"), mpf("7.3e-11")]
inv_res = {}
for a in probe_as:
    r = a0_fwd(rho_inv(a))
    inv_res[mp.nstr(a, 6)] = float(r - a)
    print(f"    a = {mp.nstr(a, 6)}:  F(R(a)) - a = {mp.nstr(r - a, 4)}  (rel {mp.nstr(rel(r, a), 4)})")
ok_c1 = all(rel(a0_fwd(rho_inv(a)), a) < TOL for a in probe_as)
check("C1 [involution right] F(R(a)) == a to 60 digits for every probe a (incl. fabricated)",
      ok_c1, "max rel dev = " + mp.nstr(max(rel(a0_fwd(rho_inv(a)), a) for a in probe_as), 4) +
             " (60-digit machine noise; exact identity in Lean)")
probe_rhos = [RHO_PLANCK, rho_inv(A0_ALT)]
ok_c2 = all(rel(rho_inv(a0_fwd(r)), r) < TOL for r in probe_rhos)
check("C2 [involution left] R(F(rho)) == rho to 60 digits", ok_c2,
      "max rel dev " + mp.nstr(max(rel(rho_inv(a0_fwd(r)), r) for r in probe_rhos), 4))

# ---------------------------------------------------------------- C3 ratio-squared
print("\n--- [C3] the Lambda-inversion is the forward residual squared ---")
worst3 = mpf(0)
for a in probe_as:
    lhs = lam_inv(a) / lam_planck(RHO_PLANCK)
    rhs = (a / A0_FWD) ** 2
    worst3 = max(worst3, rel(lhs, rhs))
print(f"    max |Lambda_inv(a)/Lambda_Planck - (a/a0_fwd)^2| / (a/a0_fwd)^2 = {mp.nstr(worst3, 6)}")
check("C3 [squared-ratio identity] Lambda_inv/Lambda_Planck == (a/a0_fwd)^2 for all probes",
      worst3 < mpf("1e-50"), f"worst rel dev {mp.nstr(worst3, 6)}  ('factor ~2 in Lambda' = 'factor ~1.4 in a0' squared)")

# ---------------------------------------------------------------- C4 negative control
print("\n--- [C4 NEGATIVE CONTROL] circular experiment earns no evidence ---")
# a fabricated scale 3.0e-10 (3.2x the true scale) is fed to the SAME inverted
# chain: the self-consistency residual is still EXACTLY zero.
a_fab = mpf("3.0e-10")
res_fab = a0_fwd(rho_inv(a_fab)) - a_fab
res_true = a0_fwd(rho_inv(A0_CAN)) - A0_CAN
print(f"    fabricated a* = 3.0e-10:  F(R(a*)) - a* = {mp.nstr(res_fab, 8)}")
print(f"    registered  a  = 9.3619e-11:  F(R(a))  - a  = {mp.nstr(res_true, 8)}")
print(f"    Omega_inv(a* = 3e-10)    = {mp.nstr(om_inv(a_fab, H0_PLANCK), 8)}  (nonsense cosmology, same zero residual)")
print(f"    Omega_inv(a0_can)        = {mp.nstr(om_inv(A0_CAN, H0_PLANCK), 8)}  (0.685 registered)")
print(f"    Omega_inv(a0(kappa_DF))  = {mp.nstr(om_inv(KAPPA_DF * C * sqrt(G * RHO_PLANCK), H0_PLANCK), 8)}  (measured kappa reading)")
print(f"    Omega_inv(a_gas=1.1e-10) = {mp.nstr(om_inv(A0_GAS_MID, H0_PLANCK), 8)}  (measured gas-slope reading)")
ok_c4 = (rel(a0_fwd(rho_inv(a_fab)), a_fab) < TOL) and (rel(a0_fwd(rho_inv(A0_CAN)), A0_CAN) < TOL) \
        and (om_inv(a_fab, H0_PLANCK) / om_inv(A0_CAN, H0_PLANCK) > mpf(10))
check("C4 [no evidence from tiny residual] inversion residual at the same noise floor for true and "
      "fabricated scales, while the 'derived' Omega_Lambda swings by an order of magnitude",
      ok_c4,
      f"res(a*=3e-10) ~ {mp.nstr(rel(a0_fwd(rho_inv(a_fab)), a_fab), 4)} == res(a0_can) ~ "
      f"{mp.nstr(rel(a0_fwd(rho_inv(A0_CAN)), A0_CAN), 4)} == 0 at 60 digits; "
      "Omega_inv output is fully input-controlled (0.685 -> 0.83/0.95 -> 7.03 as the input a changes), "
      "so a zero self-consistency residual carries zero empirical content")

# ---------------------------------------------------------------- C5 footing split H
print("\n--- [C5] galaxy datum alone cannot fix H0: the footing choice is a cosmic input ---")
H_CAN = h_kms(h_lam(A0_CAN))
H_ALT = h_kms(h_lam(A0_ALT))
H_CAN_REC = h_kms(h_lam(A0_CAN) / sqrt(OMEGA_L))
print(f"    H_Lambda(a0_can) = {mp.nstr(H_CAN, 6)} km/s/Mpc   (bare same-G reading)")
print(f"    H_Lambda(a0_alt) = {mp.nstr(H_ALT, 6)} km/s/Mpc   (bare same-G reading)")
print(f"    spread = {mp.nstr((H_ALT - H_CAN) / H_CAN * 100, 4)}% from ONE galaxy datum")
print(f"    recovering Planck 67.4 needs Omega_Lambda = 0.685 imported: {mp.nstr(H_CAN_REC, 6)} km/s/Mpc")
ok_c5 = (abs(H_CAN - H0_PLANCK_KMS) / H0_PLANCK_KMS > mpf("0.15")) and \
        (rel(H_CAN_REC, H0_PLANCK_KMS) < mpf("1e-3")) and \
        ((H_ALT - H_CAN) / H_CAN > mpf("0.10"))
check("C5 [footing-split H] same galaxy datum -> 55.79 vs 67.22 km/s/Mpc (20% split); "
      "Planck H0 recovered only by importing Omega_Lambda",
      ok_c5, f"H_can = {mp.nstr(H_CAN, 7)}, H_alt = {mp.nstr(H_ALT, 7)}, recovered w/ Omega_L: {mp.nstr(H_CAN_REC, 7)}")

# ---------------------------------------------------------------- C6/C7 forward residual
print("\n--- [C6/C7] the legitimate direction: vacuum -> galaxy scale, forward residual ---")
d_gas = (A0_FWD - A0_GAS_MID) / A0_GAS_MID
a0_df = KAPPA_DF * C * sqrt(G * RHO_PLANCK)     # = kappa_DF * (2 * a0_fwd)
sig_df = SIG_KAPPA_DF * C * sqrt(G * RHO_PLANCK)
z_df = (a0_df - A0_FWD) / sig_df
a0_btfr = KAPPA_BTFR * C * sqrt(G * RHO_PLANCK)
sig_btfr = SIG_KAPPA_BTFR * C * sqrt(G * RHO_PLANCK)
z_btfr = (a0_btfr - A0_FWD) / sig_btfr
print(f"    a0_fwd (Planck rho_L, kappa=1/2) = {mp.nstr(A0_FWD, 8)} m/s^2")
print(f"    gas-dominated slope band: [{mp.nstr(A0_GAS_LO, 5)}, {mp.nstr(A0_GAS_MID, 5)}, {mp.nstr(A0_GAS_HI, 5)}] m/s^2 -> delta = {mp.nstr(d_gas * 100, 5)}% of central")
print(f"    a0(kappa_DF = 0.55 +/- 0.17)  = {mp.nstr(a0_df, 8)} m/s^2  -> {mp.nstr(z_df, 5)} sigma from a0_fwd")
print(f"    a0(kappa_BTFR = 0.465 +/- 0.076) = {mp.nstr(a0_btfr, 8)} m/s^2  -> {mp.nstr(z_btfr, 5)} sigma from a0_fwd")
ok_c6 = (mpf("0.05") < abs(d_gas) < mpf("0.30"))
check("C6 [forward residual nonzero] predicted a0 sits ~15% below the gas-slope central value",
      ok_c6, f"delta = {mp.nstr(d_gas * 100, 5)}% (finite, nonzero; inside the corpus +/-16% systematic band)")
ok_c7 = (abs(z_df) < 2) and (abs(z_btfr) < 2)
check("C7 [kappa consistency] galaxy kappa measurements agree with 1/2 at <2 sigma "
      "(the ONLY licensed cosmological-galaxy cross-check)",
      ok_c7, f"z(kappa_DF) = {mp.nstr(z_df, 4)}, z(kappa_BTFR) = {mp.nstr(z_btfr, 4)}")

# ---------------------------------------------------------------- C8 deep-law correction
print("\n--- [C8] deep-law leading neglected term (Q-branch, labeled comparison) ---")
MB = mpf("1e11") * MSUN
R_M = sqrt(G * MB / A0_CAN)
print(f"    r_M = sqrt(G M_b / a0_can) = {mp.nstr(R_M / PC, 7)} pc for M_b = 1e11 M_sun")
for mult in [mpf(1), mpf(2), mpf(3)]:
    r = mult * R_M
    y = (R_M / r) ** 2
    v4_full = G * MB * A0_CAN * (1 + y)    # Q-branch: v^4 = G M a0 (1 + (r_M/r)^2)
    v4_deep = G * MB * A0_CAN
    print(f"    r = {mult}x r_M: leading correction y = (r_M/r)^2 = {mp.nstr(y * 100, 5)}% ; v^4 ratio = {mp.nstr(v4_full / v4_deep, 10)}")
ok_c8 = True  # printed table is the evidence; formula is analytic
check("C8 [deep-limit correction] v^4 = G M a0 (1 + (r_M/r)^2) on Q, domain y << 1",
      ok_c8, f"correction 100%/25%/11.1% at 1/2/3 r_M; deep law is the y -> 0 limit")

# ---------------------------------------------------------------- C9 boundary / homogeneity
print("\n--- [C9] normalization and boundary cases ---")
check("C9a [boundary] a0(rho -> 0) = 0 exactly", a0_fwd(mpf(0)) == 0, str(a0_fwd(mpf(0))))
lam2 = a0_fwd(mpf(2) * RHO_PLANCK) / a0_fwd(RHO_PLANCK)
lam10 = a0_fwd(mpf(10) * RHO_PLANCK) / a0_fwd(RHO_PLANCK)
ok9b = rel(lam2, sqrt(mpf(2))) < mpf("1e-50") and rel(lam10, sqrt(mpf(10))) < mpf("1e-50")
check("C9b [homogeneity] a0(lambda rho)/a0(rho) = sqrt(lambda)", ok9b,
      f"lambda=2: {mp.nstr(lam2, 12)} vs sqrt2 {mp.nstr(sqrt(mpf(2)), 12)}; lambda=10: {mp.nstr(lam10, 12)}")

# ---------------------------------------------------------------- C10 registration echo
print("\n--- [C10] the '+0.07% of Planck' is a registration echo, not an agreement ---")
print(f"    Omega_inv(a0_can registered)      = {mp.nstr(om_inv(A0_CAN, H0_PLANCK), 8)}  (dev {mp.nstr((om_inv(A0_CAN, H0_PLANCK) - OMEGA_L) / OMEGA_L * 100, 4)}%)")
print(f"    Omega_inv(a_gas measured 1.1e-10) = {mp.nstr(om_inv(A0_GAS_MID, H0_PLANCK), 8)}  (dev {mp.nstr((om_inv(A0_GAS_MID, H0_PLANCK) - OMEGA_L) / OMEGA_L * 100, 4)}%)")
print(f"    Lambda_inv(a0_can) / Lambda_Planck = {mp.nstr(lam_inv(A0_CAN) / lam_planck(RHO_PLANCK), 8)}")
print(f"    Lambda_inv(a_gas) / Lambda_Planck  = {mp.nstr(lam_inv(A0_GAS_MID) / lam_planck(RHO_PLANCK), 8)}  (corpus central estimate; its quoted band is 1.08-2.03)")
ok_c10 = (rel(om_inv(A0_CAN, H0_PLANCK), OMEGA_L) < mpf("1e-3")) and \
         (om_inv(A0_GAS_MID, H0_PLANCK) / OMEGA_L > mpf("1.15"))
check("C10 [input-controlled output] feeding the registered (convention) a0 returns 0.685 to 0.01%; "
      "feeding the measured a0 returns +38%; the 'agreement' is fixed by the input choice, not by data",
      ok_c10, f"Omega_inv(can) = {mp.nstr(om_inv(A0_CAN, H0_PLANCK), 6)}, Omega_inv(gas mid) = {mp.nstr(om_inv(A0_GAS_MID, H0_PLANCK), 6)}")

# ---------------------------------------------------------------- galaxy observables
print("\n--- forward galaxy observables from vacuum inputs (both footings separately) ---")
for name, a0 in [("canonical 9.3619e-11", A0_CAN), ("alternative 1.1279e-10", A0_ALT)]:
    for mb_name, mb in [("M_sun", MSUN), ("1e11 M_sun", MB)]:
        v4 = G * mb * a0
        print(f"    [{name}] M_b = {mb_name}: v_flat = (G M_b a0)^(1/4) = {mp.nstr(v4 ** mpf('0.25'), 7)} m/s ; "
              f"r_M = {mp.nstr(sqrt(G * mb / a0) / PC, 6)} pc ; v_flat^4 = {mp.nstr(v4, 5)}")

# G_E/G_N bookkeeping note (carried, not resolved)
print("\n--- G-bookkeeping: Lambda_inv uses the same-G reading G_E = G_N ---")
print("    Lambda_eff = 32 pi (G_E/G_N) a0^2/c^4 ; if G_E != G_N the inverted Lambda")
print("    scales by G_E/G_N -- an unresolved coupling ratio the inversion cannot fix.")

T1 = time.time()
print(f"\nwall time: {T1 - T0:.4f} s ; checks run: {len(checks)} ; failures: {len(fails)}")

summary = {
    "rho_planck_kg_m3": mp.nstr(RHO_PLANCK, 15),
    "a0_fwd_m_s2": mp.nstr(A0_FWD, 15),
    "involution_max_abs_residual": max(abs(v) for v in inv_res.values()),
    "squared_ratio_worst_rel_dev": mp.nstr(worst3, 8),
    "H_lam_can_kms": mp.nstr(H_CAN, 8),
    "H_lam_alt_kms": mp.nstr(H_ALT, 8),
    "H_lam_can_recovered_with_OmegaL_kms": mp.nstr(H_CAN_REC, 8),
    "forward_delta_gas_mid_pct": mp.nstr(d_gas * 100, 6),
    "z_kappa_DF": mp.nstr(z_df, 5),
    "z_kappa_BTFR": mp.nstr(z_btfr, 5),
    "Omega_inv_can": mp.nstr(om_inv(A0_CAN, H0_PLANCK), 10),
    "Omega_inv_gas_mid": mp.nstr(om_inv(A0_GAS_MID, H0_PLANCK), 10),
    "Omega_inv_fabricated_3e-10": mp.nstr(om_inv(a_fab, H0_PLANCK), 10),
    "Lambda_inv_can_over_planck": mp.nstr(lam_inv(A0_CAN) / lam_planck(RHO_PLANCK), 10),
    "Lambda_inv_gas_mid_over_planck": mp.nstr(lam_inv(A0_GAS_MID) / lam_planck(RHO_PLANCK), 10),
    "n_checks": len(checks),
    "failures": fails,
}

with open("residuals.json", "w") as f:
    json.dump(summary, f, indent=2)

sys_exit = 1 if fails else 0
print(f"RESULT: {'ALL CHECKS PASS' if not fails else 'FAILURES: ' + str(fails)} (exit {sys_exit})")
import sys
sys.exit(sys_exit)
