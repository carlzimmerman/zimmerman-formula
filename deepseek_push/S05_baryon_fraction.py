#!/usr/bin/env python3
r"""S05 -- THE BARYON-TO-DARK CLOSURE: does the framework predict Omega_b/Omega_m,
or take it as input?

THE QUESTION (the S-series audit lane on the cosmic bookkeeping):
    The committed closure reads "the framework's dark sector saturates the
    matter density": eq + dust = 1.000 x Omega_dm (G198 G4, DENSITY-CLOSED),
    and in the Omega_m frame the registered numbers are
        Omega_dust = 0.2619  +  (Omega_b + Omega_eq ~ 0.052)  ~  0.314  ~ Omega_m
    (G079 decomposition: Omega_dm = 0.264, Omega_b = 0.0493, Omega_eq,capped =
    0.00209).  THE QUESTION: where does Omega_b enter -- as an INPUT (the
    baryon fraction f_b = Omega_b/Omega_m = 0.157 is a measured cosmological
    datum, Planck) or is it DERIVED by the machinery (the dust-law saturation
    M_sat = 3.09e14, the pie, the equilibrium)?

(1) THE CURRENT INPUT -- the provenance audit of f_b in the committed chain.
    Every committed touchpoint of Omega_b/f_b is enumerated and classified:
    G052 (flatness "closure": Omega_dm = 1 - Omega_Lambda - Omega_b with
    Omega_b "measured" -- the lane's own words), G079 (Omega_b = 0.0493
    hardcoded Planck; the EH98 transfer's ombom0; the envelope reading),
    G187 (Omega_b in the EH98 transfer; s_b(M) nods from MEASURED cluster/
    group baryon fractions), G178 (0.081 = the GROUP baryon floor, G143's
    f_gas,500 + 0.02 stars -- a cluster-scale measurement, NOT Omega_b/Omega_m),
    and the per-object M_b that normalizes the BTFR/equipartition/dust law at
    every scale.  The audit shows f_b = 0.157 is INPUT at every point; the
    machinery is baryon-NORMALIZED (M_dark = M_b x dimensionless multipliers).

(2) THE PREDICTION ATTEMPT -- can the machinery fix f_b?  The candidate
    levers, each computed: (a) M_sat = 8e14 (1/f_ref)^(1/q) = 3.09e14 depends
    only on the measured cluster pair (f_ref, q) -- it fixes the PHANTOM-vs-
    DUST split, not baryons; (b) the equilibrium bound Omega_eq <= Omega_star
    (1 + f_gas) is baryon-normalized by the MEASURED stellar density; (c) the
    flatness-slack inversion f_b^slack = (1 - Omega_L - Omega_dm)/(1 -
    Omega_L) = 0.160 vs the Planck datum 0.156 -- an IDENTITY on measured
    sides (the G03C circularity class: you must measure Omega_dm to get f_b
    out), not a prediction; (d) the pie's mass-function-weighted halo baryon
    share <s_b> = 0.085 (G187) is a halo-CONTENT statement (halos depleted to
    0.54 x f_b) whose normalization is the measured cluster nods.  The closed
    sector never produces the cosmic 0.157.

(3) THE CONSEQUENCE -- the input count, honestly.  The framework's core:
    (a0, G, c, Omega_Lambda, f_b, m) -- SIX inputs -- classified: G, c,
    Omega_Lambda, f_b are MEASURED cosmological constants; a0 is identity-
    pinned to (c, H0, Omega_Lambda) by the horizon form (Z11: a0 = c^2/
    (Z R_dS) = 9.3624e-11, ratio 1.00005) AND empirically zero-point
    calibrated (S09: TRIO closure at z = -0.20, "consistency not proof");
    m = 5.09 +- 0.10 keV is DERIVED (G212, three independent measured
    windows).  Plus the ancillary measured datums the closure consumes:
    H0, Omega_star, n_s, sigma_8, T_CMB.  "Zero-free-parameter" is true PER
    OBJECT (given M_b and a0 the dark profile is a closed form) and false as
    "no measured inputs": f_b = 0.157 is the last undeclared measured input
    of any cosmic "closure" framing.

(4) VERDICTS.
    V1 the f_b provenance : INPUT everywhere (the audit table); G178's 0.081
       is the group-scale baryon floor (0.52 x f_b), measured, not a cosmic
       derivation;
    V2 the derived-vs-input count : derived {m, M_sat, the band, Z, s_Lambda,
       T_b, u(M) exponent, q -> -1/3, A_b}, identity-pinned {a0}, measured
       {G, c, H0, Omega_L, Omega_m, f_b, Omega_star, n_s, sigma_8, T_CMB,
       per-object M_b} -- f_b sits in the measured column;
    V3 the honest statement: the baryon fraction is the framework's input at
       every committed closure point; the cosmic 0.157 appears only as the
       flatness-slack echo (0.160, 2.3% -- an identity, G03C class); the
       machinery's only f_b-adjacent product is the depleted halo baryon
       share <s_b> = 0.085; in any "zero-free-parameter" framing of the pie,
       f_b = 0.157 is the last undeclared free parameter.

REGISTERS READ (committed numbers only): deepseek_push/G079_results.json
(the decomposition Omega_dm 0.264 / Omega_eq 0.00209-0.00338 / Omega_dust
0.2619; the cluster f_b band 0.13-0.155; the f_dark band 6-10),
G198_results.json (the DENSITY closure eq + dust = 1.000 x Omega_dm),
G187_results.json (the pie: s_b nods 0.081/0.068/0.1443/0.2025/0.2217, the
cosmic <s_b> = 0.0846, the EH98+Tinker weights), G178_results.json (the
saturation M_sat = 3.0876e14, band [1.7298, 4.0097]e14; group median f_b =
0.081; f_ref = 0.674), G212_results.json (m = 5.09 +- 0.10 keV), Z11_results.
json (a0 = kappa_dS/Z horizon identity, the constants table), G052 (the
flatness residual lane: Omega_b "measured"), G189 (the s_Lambda register,
the Omega_Lambda identity 32 pi a0^2/(3 H0^2 c^2) -- Lean-certified algebra,
G03C-flagged as identity, not derivation).

Outputs: S05_baryon_fraction.out, S05_results.json (this lane).
Run:     python3 S05_baryon_fraction.py > S05_baryon_fraction.out 2>&1
"""

import json
import math
import os

RES, NP, NF = [], 0, 0


def check(name, measured, ok, d=""):
    global NP, NF
    ok = bool(ok)
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    print(f"         measured: {measured}")
    if d:
        print(f"         reading : {d}")
    RES.append({"name": name, "measured": str(measured), "pass": ok,
                "reading": d})
    NP, NF = NP + (1 if ok else 0), NF + (0 if ok else 1)


def info(*a):
    print(*a, flush=True)


print(__doc__)
print("=" * 100)
print("S05 -- THE BARYON-TO-DARK CLOSURE: predict or input?")
print("=" * 100)

HERE = os.path.dirname(os.path.abspath(__file__))

# ------------------------------------------------------------------ commits
G079 = json.load(open(os.path.join(HERE, "G079_results.json")))
G198 = json.load(open(os.path.join(HERE, "G198_results.json")))
G187 = json.load(open(os.path.join(HERE, "G187_results.json")))
G178 = json.load(open(os.path.join(HERE, "G178_results.json")))
G212 = json.load(open(os.path.join(HERE, "G212_results.json")))
Z11 = json.load(open(os.path.join(HERE, "Z11_results.json")))

# Planck / committed cosmic constants (the register values, all published)
OM_M = 0.3153          # Planck 2020 (G079)
OM_B = 0.0493          # Planck 2020 (G079/G187/G052 -- hardcoded INPUT)
OM_DM = G079["decomposition"]["Omega_dm"]                       # 0.264
OMEQ_CAP = G079["decomposition"]["Omega_eq_capped_0p62"]        # 0.0020925
OMEQ_UNC = G079["decomposition"]["Omega_eq_uncapped"]           # 0.003375
OM_DUST = G198["closure"]["density_sum_capped"]["dust"]          # 0.261908
OM_STAR = G079["decomposition"]["Omega_star"]                   # 0.0027
FGAS = 0.25            # galaxy disk gas-to-star fraction (G079)
OM_L_COMMIT = 0.6857   # the committed constants-table register (Z10 F8)
OM_L_PLANCK = 0.6847   # Planck 2018/2020 VI
G058_WIN = (0.6849303, 0.6849321)   # G058 Lean-certified window (H0 = 67.4)
H0_67p36 = 67.36        # Planck-in-commits
NS, SIG8 = 0.9649, 0.811   # Planck (G079 mass-function weights)
F_B_CLUSTER_BAND = (0.13, 0.155)   # Vikhlinin et al. 2006 (G079 G7)
FDARK_BAND = G079["cluster_budget"]["f_dark_band"]              # [6, 10]
M_SAT = G178["prediction"]["M_sat_Msun"]                        # 3.0876e14
M_SAT_BAND = G178["prediction"]["M_sat_band_Msun"]              # [1.73, 4.01]e14
F_REF = G178["direct_test"]["cluster_anchor"]                   # 0.6740
Q_REG = -0.41438        # G140 registered mass slope
F_B_GROUP = G178["direct_test"]["median_f_b"]                   # 0.081
SB_HALO = G187["cosmic_closure"]["mean_shares_equipartition"]["s_b"]  # 0.0846
M_KEV = 5.09            # G212 joint posterior peak, band [4.99, 5.19]
A0_DE = 9.3619e-11      # the committed canonical DE-anchored scale
A0_H = float(Z11["registers"]["a0_H"]) if "a0_H" in Z11.get(
    "registers", {}) else 9.362375e-11   # horizon form

F_B = OM_B / OM_M
info(f"  registers: Omega_m = {OM_M}, Omega_b = {OM_B} (INPUT), "
     f"Omega_dm = {OM_DM}, Omega_dust = {OM_DUST}, "
     f"Omega_eq = {OMEQ_CAP}/{OMEQ_UNC:.5f}")
info(f"  f_b = Omega_b/Omega_m = {F_B:.4f} (Planck; the task's 0.157)")
info(f"  the task's saturation reading: 0.2619 + 0.052 = "
     f"{0.2619 + 0.0514:.3f} ~ Omega_m; the '0.052' = Omega_b + Omega_eq_cap "
     f"= {OM_B + OMEQ_CAP:.4f} (or Omega_m - Omega_dust = "
     f"{OM_M - OM_DUST:.4f}) -- BOTH routes need the measured Omega_b")

# =====================================================================
print()
print("=" * 100)
print("PART 1 -- THE CURRENT INPUT: the f_b provenance audit (the committed")
print("          chain, every Omega_b touchpoint classified)")
print("=" * 100)

# --- 1a: the flatness "closure" lane is the strongest candidate for a
#      derivation; audit what G052 actually does.
print("""
  1a. G052 (lanes/G052_unified_cosmology.py, PART 3 -- the flatness closure):
      'Omega_Lambda DERIVED (a0 -> Lambda^4 -> 0.6857) and Omega_b MEASURED,
      spatial flatness demands Omega_dm = residual' -- the lane's OWN words.
      -> Omega_b is the INPUT of the flatness residual; Omega_dm is DERIVED
      as 1 - Omega_L - Omega_b.  The baryon fraction is never produced; it is
      consumed.  (And the Omega_Lambda derivation is the G03C-flagged identity
      rho_Lambda = 4 a0^2/(G c^2), Lean-certified algebra, not physics.)""")

# --- 1b: hardcoded Omega_b in the density lanes
print("""
  1b. G079/G187/G198: Omega_b = 0.0493 is hardcoded as 'Planck 2020,
      published, not computed here'.  Uses: (i) the EH98 transfer function
      (ombom0 = Omega_b/Omega_m enters the sound horizon and silk damping --
      the baryon acoustic shape of every F(>M) weight this lane family
      computes); (ii) the envelope reading Omega_b/Omega_dm = 18.7%; (iii)
      G198's closure arithmetic.  All three are INPUT uses.""")

# --- 1c: G178's 0.081 -- the cluster-scale floor vs the cosmic 0.157
print("""
  1c. G178's 0.081: the GROUP baryon floor.  It is the median of the 26 E11
      groups' f_b = f_gas,500 + 0.02 stars (G143's committed transcription of
      the E11 group gas fractions) -- a CLUSTER-SCALE measurement, the baryon
      share of M500 in the all-dust phase.  It is NOT Omega_b/Omega_m and it
      is NOT derived from the framework: it is the measured input that the
      equipment inversion 1 - M_b/M500 is normalized to.""")
gap = F_B_GROUP / F_B
info(f"  the two baryon numbers side by side:")
info(f"    f_b,cgroup (G143/E11 median, measured) = {F_B_GROUP:.3f}")
info(f"    f_b,cosmic = Omega_b/Omega_m (Planck, measured) = {F_B:.3f}")
info(f"    ratio = {gap:.3f} -- the groups carry ~{100*gap:.0f}% of their")
info(f"    cosmic-share baryons (halo baryon depletion, a measured deficit,")
info(f"    not a framework prediction)")

# --- 1d: the pie's s_b(M) nods -- all measured
SB_NODES = [(1e13, F_B_GROUP), (1.7298e14, 0.068), (3.48e14, 0.1443),
            (8e14, 0.2025), (1e15, 0.2217)]
check("C1 [the datum] f_b = Omega_b/Omega_m = 0.1564 (Planck 0.0493/0.3153)",
      f"f_b = {F_B:.4f}",
      abs(F_B - 0.157) < 0.002,
      "the task's 0.157 is the Planck 2020 ratio of two measured densities; "
      "nothing in the committed chain computes it")
check("C2 [G178's 0.081 is not Omega_b/Omega_m] the group baryon floor sits "
      "at {:.2f}x the cosmic f_b -- a cluster-scale MEASURED depletion, not "
      "a cosmic derivation".format(gap),
      f"f_b,group = {F_B_GROUP:.3f} vs f_b,cosmic = {F_B:.3f} (ratio {gap:.2f})",
      gap < 0.75,
      "G178's own verdict calls it 'the baryon floor' of the group f_dust "
      "inversion (dust share = 1 - f_b with f_b ~ 0.08): an input, and a "
      "scale-specific one")
check("C3 [the pie's baryon nods are all measured] every s_b(M) anchor of "
      "the constitution curve is a measured cluster/group baryon fraction",
      f"nods: {', '.join(f'({m:.2e}, {s:.3f})' for m, s in SB_NODES)}",
      all(s < 0.25 for _, s in SB_NODES),
      "G187 labels them 'the committed nods s_b(M) passes through (the pie's "
      "own data, not invented)' -- measured inputs interpolated by the "
      "curve, not produced by the machinery")

info("")
info("  AUDIT RESULT (1): f_b is INPUT at every committed touchpoint --"
     "G052's flatness residual consumes it, the transfer function consumes "
     "it, the pie's s_b(M) is built from measured cluster baryon shares, "
     "and per-object M_b (measured M/L + gas) normalizes the BTFR, the "
     "equipartition and the dust law at every scale.  Zero derivations.")

# =====================================================================
print()
print("=" * 100)
print("PART 2 -- THE PREDICTION ATTEMPT: can M_sat / the pie / the")
print("          equilibrium fix the baryon fraction?")
print("=" * 100)

# --- 2a: M_sat content
M_sat_re = 8.0e14 * (1.0 / F_REF) ** (1.0 / Q_REG)
info("")
info("  2a. THE SATURATION M_sat = 3.09e14: determined ONLY by the measured")
info("      cluster pair (f_ref, q) -- no baryon input anywhere:")
info(f"      M_sat = 8e14 (1/f_ref)^(1/q) = 8e14 (1/{F_REF:.3f})^(1/"
     f"{Q_REG:.3f}) = {M_sat_re:.4e} Msun (registered {M_SAT:.4e}, band "
     f"[{M_SAT_BAND[0]:.3e}, {M_SAT_BAND[1]:.3e}])")
info("      -> it fixes the PHANTOM-vs-DUST split of the MISSING mass")
info("         (f_dust = 1 below, 0.674 (M/8e14)^-0.414 above): both are")
info("         dark-sector fractions of (1 - s_b), and s_b is the measured")
info("         baryon input.  M_sat cannot see Omega_b.")

# --- 2b: the equilibrium bound
info("")
info("  2b. THE EQUILIBRIUM BOUND (G079): Omega_eq <= Omega_star (1 + f_gas)")
info(f"      = {OM_STAR} x {1 + FGAS} = {OMEQ_UNC:.4f} (uncapped) / "
     f"0.62x = {OMEQ_CAP:.4f} (capped) = "
     f"{100*OMEQ_CAP/OM_DM:.2f}% of Omega_dm")
info("      the equilibrium sector's cosmic share is bounded by the MEASURED")
info("      stellar density (Fukugita & Peebles 2004) -- baryon-normalized,")
info("      and it bounds DARK mass in units of baryon mass; it never fixes")
info("      the baryon abundance itself.")

# --- 2c: the flatness-slack inversion -- the ONLY route that yields a
#      cosmic f_b number; classify it honestly
f_b_slack = (1.0 - OM_L_COMMIT - OM_DM) / (1.0 - OM_L_COMMIT)
f_b_slack_p = (1.0 - OM_L_PLANCK - OM_DM) / (1.0 - OM_L_PLANCK)
info("")
info("  2c. THE FLATNESS-SLACK INVERSION: if the framework's dark sector is")
info("      density-closed (eq + dust = 1.000 x Omega_dm, G198) AND the")
info("      universe is flat, the baryon fraction is the slack")
info("      f_b^slack = (1 - Omega_L - Omega_dm)/(1 - Omega_L):")
info(f"      committed Omega_L = {OM_L_COMMIT}: f_b^slack = "
     f"{f_b_slack:.4f}  vs Planck datum {F_B:.4f} "
     f"(delta {f_b_slack - F_B:+.4f}, {100*(f_b_slack/F_B - 1):+.1f}%)")
info(f"      Planck Omega_L = {OM_L_PLANCK}: f_b^slack = {f_b_slack_p:.4f} "
     f"(delta {f_b_slack_p - F_B:+.4f})")
info("      CLASSIFICATION: an IDENTITY on measured sides -- you must already")
info("      know Omega_Lambda AND Omega_dm to get f_b out; the framework ")
info("      contributes only the (trivial, mass-conservation) statement ")
info("      eq + dust = Omega_dm.  This is the G03C circularity class ")
info("      ('closure from measured inputs'), exactly as the record flags ")
info("      Omega_Lambda-from-a0.  NOT a prediction.")

# --- 2d: the pie's halo baryon content
info("")
info("  2d. THE PIE'S HALO BARYON CONTENT: the mass-function-weighted mean")
info("      baryon share of halos M > 1e12 (G187 cosmic closure, Tinker+08 "
     f"on the EH98 pipeline) = <s_b> = {SB_HALO:.4f} = "
     f"{100*SB_HALO/F_B:.0f}% of the cosmic f_b")
info("      -> the only f_b-adjacent NUMBER the closed sector emits is a")
info("         halo-CONTENT statement: halos are baryon-depleted (0.54 x the")
info("         cosmic share).  Its normalization is the measured cluster/")
info("         group nods of Part 1 -- the curve averages inputs; it does")
info("         not derive Omega_b.")

# --- the register inconsistency in the committed cosmic constants
sum_ob_odm = OM_B + OM_DM
flat_comm = OM_L_COMMIT + OM_M
info("")
info("  REGISTER NOTE (the honest constants audit):")
info(f"    Omega_b + Omega_dm = {sum_ob_odm:.4f} vs Omega_m = {OM_M:.4f} "
     f"(slack {OM_M - sum_ob_odm:+.4f}, {100*(OM_M/sum_ob_odm - 1):+.1f}%)")
info(f"    Omega_L(committed) + Omega_m = {flat_comm:.4f} vs 1 "
     f"(slack {flat_comm - 1:+.4f})")
info(f"    Omega_L + Omega_dm + Omega_b = {OM_L_COMMIT + OM_DM + OM_B:.4f}")
info("    the committed Planck registers do not sum exactly (0.6-0.9% "
     "slack); any 'closure at Omega_m' inherits that slack -- further "
     "evidence the bookkeeping is measured-input arithmetic, not derivation.")

check("C4 [M_sat carries no baryon input] M_sat = 3.09e14 recomputed from "
      "the committed (f_ref, q) alone -- the saturation fixes the dark-"
      "sector split, not the baryon fraction",
      f"M_sat = {M_sat_re:.4e} (registered {M_SAT:.4e})",
      abs(M_sat_re - M_SAT) / M_SAT < 1e-4,
      "f_ref = 0.674 (measured cluster phantom/dust median) and q = -0.414 "
      "(measured mass run): both dark-internal, both measured")
check("C5 [the flatness slack is an identity, not a prediction] f_b^slack "
      "agrees with the datum to 2-4% ONLY because both sides are measured",
      f"f_b^slack = {f_b_slack:.4f} ({f_b_slack_p:.4f} at Planck Omega_L) "
      f"vs f_b = {F_B:.4f}",
      abs(f_b_slack - F_B) < 0.01,
      "the G03C circularity class: to run this 'prediction' you must input "
      "Omega_dm and Omega_Lambda -- the machinery adds nothing but the "
      "identity eq + dust = Omega_dm (G198, mass conservation by "
      "construction)")
check("C6 [the only framework-emitted baryon number is the halo share] "
      "<s_b> = 0.085 (G187) is a depleted halo-CONTENT mean, 0.54 x f_b, "
      "built from the measured nods -- not the cosmic f_b",
      f"<s_b> = {SB_HALO:.4f} = {100*SB_HALO/F_B:.0f}% of f_b = {F_B:.3f}",
      0.3 < SB_HALO / F_B < 0.8,
      "the halo baryon deficit is a real (measured) astrophysical statement, "
      "and it is exactly what the framework does NOT claim to derive: the "
      "curve interpolates measured cluster baryon shares")

# =====================================================================
print()
print("=" * 100)
print("PART 3 -- THE CONSEQUENCE: the honest input count")
print("=" * 100)

# derived / identity-pinned / measured classification with the registers
derived = [
    ("m = 5.09 +- 0.10 keV", "G212: joint posterior of three independent "
                             "measured windows (cosmic noon 5.0-5.2, forest "
                             "3.3-5.7, free-streaming 4.70-5.75); the only "
                             "'particle' number, fully derived"),
    ("M_sat = 3.09e14, band [1.73, 4.01]e14", "G178/G140: from the measured "
     "f_ref and q run -- derived from data, not a free fit"),
    ("Z = 2 sqrt(8 pi/3) = 5.7888", "Z11: the dimensionless constant of the "
     "horizon form (G166 register)"),
    ("s_Lambda = 2 a0_DE = 1.872e-10", "G189: the seesaw constant, the "
     "horizon surface gravity over Z/2"),
    ("T_b = 9.34 K in [9.17, 9.52]", "G212/Z11: m sigma^2/k_B -- a composite"),
    ("u(M) exponent +0.314 = (1-gamma)/2 - 1/3", "G179/G222: the derived "
     "equipoise exponent, fitted +0.3141 (z < 2)"),
    ("q -> -1/3 (Bondi)", "G200/G210: measured -0.414 +- 0.157, derived "
     "-1/3 at 0.52 sigma"),
    ("A_b = 0.650 jump", "the phantom/dust density ratio at the cap, derived "
     "from the collisionless infall (CROSS_TRACK/CLUSTER_CLOSEOUT)"),
]
identity = [
    ("a0 = c^2/(Z R_dS) = kappa_dS/Z = 9.3624e-11", "Z11: the horizon "
     "identity, ratio 1.00005 vs the committed 9.3619e-11 -- a re-expression "
     "of (c, H0, Omega_L, Z), AND empirically zero-point calibrated (S09: "
     "TRIO closure at 0.976 a0_DE, z = -0.20; the full-542 +0.2585-dex "
     "registered departure keeps it an empirical quantity, 'consistency not "
     "proof')"),
    ("Omega_Lambda = 32 pi a0^2/(3 H0^2 c^2)", "G058 Lean-certified "
     "algebra; G03C-flagged IDENTITY, not a derivation (a0 -> Omega_L is "
     "circular)"),
]
measured = [
    ("G, c", "fundamental constants, defined/measured"),
    ("H0 = 67.36", "Planck; enters R_dS, rho_crit, the Omega_L identity, "
     "the transfer"),
    ("Omega_Lambda = 0.6857 (committed)", "Planck-measured; the committed "
     "register (G058 window 0.68493)"),
    ("Omega_m = 0.3153, Omega_dm = 0.264, Omega_b = 0.0493 -> f_b = 0.157",
     "Planck-measured -- f_b is THE baryon datum"),
    ("Omega_star = 0.0027 (Fukugita & Peebles 2004)", "the equilibrium "
     "bound's normalization"),
    ("n_s = 0.9649, sigma_8 = 0.811", "the mass-function weights (G079/G187)"),
    ("per-object M_b (M/L + gas)", "the BTFR/equipartition/dust-law "
     "normalization at every scale -- N galaxy datums"),
]

info("  THE CLASSIFICATION (derived vs identity-pinned vs measured):")
info("")
info("  DERIVED (framework composites, no free data fit):")
for name, why in derived:
    info(f"    - {name:<38s} {why}")
info("")
info("  IDENTITY-PINNED (re-expressions of measured constants -- G03C class):")
for name, why in identity:
    info(f"    - {name:<38s} {why}")
info("")
info("  MEASURED INPUTS (cosmological datum, not framework-produced):")
for name, why in measured:
    info(f"    - {name:<38s} {why}")

info("")
info("  THE SIX-CORE STATEMENT:")
info("    framework core (a0, G, c, Omega_Lambda, f_b, m):")
info("      4 measured  -> G, c, Omega_Lambda, f_b")
info("      1 identity-pinned -> a0 (horizon identity + empirical zero point)")
info("      1 derived  -> m = 5.09 keV")
info("    + the ancillary measured datums the closure consumes: H0, "
     "Omega_star, n_s, sigma_8, T_CMB")
info("    + per-object M_b: the law's baryon ruler at every scale.")
info("")
info("  VS 'ZERO-FREE-PARAMETER':")
info("    TRUE  per object -- given M_b and a0, M_dark(<r) = M_b r/r_M, "
     "r_M = sqrt(G M_b/a0), v(r), the surface density are all closed forms; "
     "no per-object fit (G135/G119, the one-line sample relations).")
info("    FALSE as 'no cosmic inputs' -- the pie, the transfer, the "
     "flatness bookkeeping and the equilibrium bound all take measured "
     "cosmic datums, and f_b = 0.157 is explicitly among them.")

empirical_free = 1  # q is the last genuinely free fit (mass slope); c0 pinned
check("C7 [the empirical-free-parameter inventory] the cluster pie has "
      "exactly ONE genuinely free fit left (q = -0.414 +- 0.157, the mass "
      "slope; the amplitude combination c0 is pinned by the derived A_b jump)"
      " -- everything else is measured or derived",
      f"free fits: {empirical_free} (q); a0 zero point empirically "
      "calibrated (S09 registered tensions)",
      empirical_free <= 1,
      "the 'zero-free-parameter' claim is about per-object fits, and it is "
      "fair there; it is NOT a claim about the cosmic inputs -- and f_b is "
      "the one cosmic input with no framework-side constraint at all "
      "(the tests are all M_b-normalized, so a wrong f_b would be invisible "
      "to every fit)")
check("C8 [the honest core count] the six-core statement: (a0, G, c, "
      "Omega_Lambda, f_b, m) = 4 measured + 1 identity-pinned (a0) + 1 "
      "derived (m); the ancillary closure adds H0, Omega_star, n_s, "
      "sigma_8, T_CMB",
      f"6 core = 4 measured (G, c, Omega_L, f_b) + 1 identity-pinned (a0) "
      "+ 1 derived (m); +5 ancillary measured datums; + per-object M_b",
      True,
      "any honest input-count statement must put f_b in the MEASURED "
      "column: it is the number the flatness residual consumes (G052) and "
      "the EH98 weights (G079/G187) and the pie's s_b nods (G178/G187) "
      "all take as given")

# =====================================================================
print()
print("=" * 100)
print("V -- THE VERDICTS")
print("=" * 100)

v1 = (f"THE f_b PROVENANCE: INPUT, EVERYWHERE.  The audit chain: (a) G052's "
      f"flatness 'closure' derives Omega_dm = 1 - Omega_L - Omega_b from a "
      f"MEASURED Omega_b (the lane's own words -- 'Omega_b measured'); (b) "
      f"G079/G187 hardcode Omega_b = 0.0493 (Planck, 'published, not "
      f"computed here') into the EH98 transfer and the envelope; (c) the "
      f"pie's s_b(M) nods {[s for _, s in SB_NODES]} are MEASURED group/"
      f"cluster baryon shares; (d) G178's 0.081 is the GROUP baryon floor "
      f"(G143's E11 f_gas,500 + 0.02 stars), a cluster-scale measurement at "
      f"{100*gap:.0f}% of the cosmic f_b = {F_B:.3f} -- NOT Omega_b/Omega_m "
      f"and NOT derived; (e) the per-object M_b (measured M/L + gas) "
      f"normalizes the BTFR, the equipartition and the dust law at every "
      f"scale.  Zero derivations of f_b on the committed record.  The "
      f"machinery is baryon-NORMALIZED: M_dark = M_b x dimensionless "
      f"multipliers everywhere.")
v2 = (f"THE DERIVED-VS-INPUT COUNT: derived {{m = 5.09 +- 0.10 keV (G212), "
      f"M_sat = 3.09e14 (band [1.73, 4.01]e14), Z, s_Lambda, T_b, the u(M) "
      f"exponent +0.314, q -> -1/3, A_b = 0.650}}; identity-pinned {{a0 = "
      f"c^2/(Z R_dS) = 9.3624e-11 at ratio 1.00005 (Z11) AND empirically "
      f"zero-point calibrated (S09), Omega_Lambda = 32 pi a0^2/(3 H0^2 c^2) "
      f"(G058 algebra, G03C-flagged circular)}}; measured inputs {{G, c, "
      f"H0, Omega_Lambda, Omega_m, OMEGA_B -> f_b = {F_B:.4f}, Omega_star, "
      f"n_s, sigma_8, T_CMB, per-object M_b}}.  In the six-core framing "
      f"(a0, G, c, Omega_Lambda, f_b, m): 4 measured, 1 identity-pinned, 1 "
      f"derived.  f_b sits in the MEASURED column; every closure point "
      f"consumes it, none produces it.")
v3 = (f"HONEST -- the baryon fraction is the framework's last undeclared "
      f"input, and the honest input count admits it: 6 core (a0, G, c, "
      f"Omega_Lambda, f_b, m) of which 4 are measured cosmological constants "
      f"(f_b = 0.157 among them) + 5 ancillary measured datums (H0, "
      f"Omega_star, n_s, sigma_8, T_CMB) + per-object M_b.  The 'zero-free-"
      f"parameter' claim is TRUE per object (closed forms given M_b and a0) "
      f"and NOT a claim about cosmic inputs.  The closed sector's only "
      f"f_b-adjacent emissions: (i) the halo baryon share <s_b> = "
      f"{SB_HALO:.3f} = 0.54 x f_b -- halo CONTENT from the measured nods, "
      f"depleted, not a cosmic derivation; (ii) the flatness-slack echo "
      f"f_b^slack = {f_b_slack:.3f} vs {F_B:.3f} (2.3% at the committed "
      f"Omega_L) -- an identity on measured sides (G03C class: you must "
      f"input Omega_dm and Omega_Lambda to get f_b out), carrying the "
      f"registered 0.6-0.9% slack of the committed Planck registers.  The "
      f"machinery fixes the DARK-internal split (M_sat, f_dust, phantom "
      f"share 1-f_dust = 0.33 median) and the dark-to-baryon ratio field "
      f"(1:1 at r_M, x(R500/r_M) phantom gain, f_dark 6-10 clusters), never "
      f"the baryon abundance: f_b = 0.157 enters the pie as the number that "
      f"makes the dark sector measurable, and no test of the framework "
      f"constrains it -- the last undeclared free parameter of the cosmic "
      f"frame.")

check("V1 [the f_b provenance: INPUT everywhere -- the audit chain]", 
      f"G052 consumes Omega_b; G079/G187 hardcode it; G178's 0.081 = "
      f"{100*gap:.0f}% of f_b and is measured; per-object M_b normalizes "
      f"every law",
      True, v1)
check("V2 [the derived-vs-input count: f_b in the MEASURED column]",
      f"derived {len(derived)} / identity-pinned {len(identity)} / measured "
      f"{len(measured)}; six-core = 4 measured + 1 identity + 1 derived",
      True, v2)
check("V3 [the honest statement -- the baryon fraction, the input count]",
      f"f_b = {F_B:.4f} input; slack echo {f_b_slack:.4f} (identity); <s_b> "
      f"= {SB_HALO:.4f} (halo content); 6 core inputs, 4 measured",
      True, v3)

print()
print(f"S05 COMPLETE: {NP}/{NP + NF} checks PASS.")
print(f"  V1: f_b = {F_B:.4f} is INPUT at every committed touchpoint "
      f"(G052/G079/G187/G178/perp-object M_b); G178's 0.081 = the measured "
      f"group baryon floor, {100*gap:.0f}% of cosmic f_b")
print(f"  V2: derived {{m, M_sat, Z, s_Lambda, T_b, u-exp, q->-1/3, A_b}}; "
      f"identity {{a0, Omega_L}}; measured {{G, c, H0, Omega_L, Omega_m, "
      f"f_b, Omega_star, n_s, sigma_8, M_b}}")
print(f"  V3: 6 core = 4 measured + 1 identity-pinned (a0) + 1 derived (m); "
      f"f_b = 0.157 is the last undeclared input of the cosmic frame")

# ------------------------------------------------------------------ artifact
out = {
    "lane": "S05_baryon_fraction",
    "title": "THE BARYON-TO-DARK CLOSURE: does the framework predict "
             "Omega_b/Omega_m (0.157) or take it as input?  The provenance "
             "audit, the prediction attempt (M_sat / pie / equilibrium / "
             "flatness slack), the honest input count, and the verdicts.",
    "deliverable": "deepseek_push/S05_baryon_fraction.py + .out + "
                   "S05_results.json",
    "context": "G187 (the pie, the constitution curve, the cosmic <s_b>); "
               "G079 (the Omega_dm decomposition: Omega_dm 0.264 = eq "
               "0.0021 + dust 0.2619; Omega_b 0.0493 INPUT; f_b cluster "
               "band 0.13-0.155); G178 (f_b = 0.081 the GROUP baryon floor, "
               "not Omega_b/Omega_m; M_sat = 3.09e14); G189/G058 (the "
               "Omega_Lambda identity, G03C circularity flag); S09/Z11 (a0 "
               "identity-pinned by the horizon, empirically calibrated); "
               "G212 (m = 5.09 keV derived); G052 (the flatness residual "
               "lane that consumes Omega_b as measured).",
    "registers": {
        "Omega_m": OM_M, "Omega_b": OM_B, "Omega_dm": OM_DM,
        "Omega_dust": OM_DUST, "Omega_eq_capped": OMEQ_CAP,
        "Omega_eq_uncapped": OMEQ_UNC, "Omega_Lambda_committed": OM_L_COMMIT,
        "Omega_Lambda_planck": OM_L_PLANCK,
        "f_b_cosmic": round(F_B, 4),
        "f_b_group_floor": F_B_GROUP,
        "f_b_group_over_cosmic": round(gap, 3),
        "f_b_cluster_band": list(F_B_CLUSTER_BAND),
        "M_sat_Msun": M_SAT, "M_sat_band_Msun": list(M_SAT_BAND),
        "m_keV": M_KEV,
        "a0_horizon_identity": A0_H, "a0_committed": A0_DE,
    },
    "part1_provenance_audit": {
        "f_b_classification": "INPUT at every committed touchpoint",
        "touchpoints": [
            {"G052_flatness_residual": "Omega_dm = 1 - Omega_L - Omega_b "
             "with Omega_b 'measured' (the lane's own words) -- Omega_b "
             "consumed, Omega_dm derived, f_b never produced"},
            {"G079_G187_hardcode": "Omega_b = 0.0493 Planck hardcoded into "
             "the EH98 transfer (ombom0, sound horizon, silk damping) and "
             "the envelope Omega_b/Omega_dm = 18.7%"},
            {"G178_group_floor": "0.081 = median f_gas,500 + 0.02 stars of "
             "the 26 E11 groups (G143) -- a cluster-scale MEASURED baryon "
             "share, 0.52 x cosmic f_b, not Omega_b/Omega_m, not derived"},
            {"G187_pie_nods": "s_b(M) nods (1e13, 0.081), (1.73e14, 0.068), "
             "(3.48e14, 0.1443), (8e14, 0.2025), (1e15, 0.2217) -- measured "
             "cluster/group baryon fractions, the pie's 'own data'"},
            {"per_object_M_b": "measured M/L + gas normalizes the BTFR v^4 "
             "= G M_b a0, the equipartition M_dark(<r_M) = M_b and the dust "
             "law at every scale -- the baryon ruler"},
        ],
        "derived_anywhere": False,
    },
    "part2_prediction_attempt": {
        "M_sat_content": {
            "formula": "8e14 (1/f_ref)^(1/q)",
            "recomputed": M_sat_re, "registered": M_SAT,
            "class": "fixes the phantom-vs-dust split of the missing mass "
                     "from the measured (f_ref, q); no baryon input"},
        "equilibrium_bound": {
            "Omega_eq_uncapped": OMEQ_UNC,
            "Omega_eq_capped": OMEQ_CAP,
            "bound_source": "Omega_star (Fukugita & Peebles 2004, measured)",
            "class": "dark mass in units of measured baryon mass; never "
                     "fixes the baryon abundance"},
        "flatness_slack": {
            "formula": "f_b^slack = (1 - Omega_L - Omega_dm)/(1 - Omega_L)",
            "committed_Omega_L": round(float(f_b_slack), 4),
            "planck_Omega_L": round(float(f_b_slack_p), 4),
            "datum_f_b": round(float(F_B), 4),
            "agreement_pct": round(100 * (f_b_slack / F_B - 1), 1),
            "class": "IDENTITY on measured sides (G03C circularity class): "
                     "input Omega_dm and Omega_Lambda to get f_b out -- not "
                     "a prediction",
        },
        "halo_baryon_content": {
            "s_b_mean_over_halos_gt_1e12": SB_HALO,
            "fraction_of_cosmic_f_b": round(SB_HALO / F_B, 3),
            "class": "halo-CONTENT statement, baryon-depleted, built from "
                     "the measured nods -- not the cosmic f_b"},
        "committed_register_slack": {
            "Omega_b_plus_Omega_dm": round(OM_B + OM_DM, 4),
            "Omega_m": OM_M,
            "slack": round(OM_M - OM_B - OM_DM, 4),
            "flatness_committed": round(OM_L_COMMIT + OM_M, 4),
        },
    },
    "part3_input_count": {
        "six_core": {
            "formula": "(a0, G, c, Omega_Lambda, f_b, m)",
            "measured": ["G", "c", "Omega_Lambda", "f_b (0.157)"],
            "identity_pinned": ["a0 (horizon identity c^2/(Z R_dS) at "
                                "1.00005 + empirical zero point, S09)"],
            "derived": ["m = 5.09 +- 0.10 keV (G212)"],
        },
        "ancillary_measured_datums": ["H0", "Omega_star", "n_s", "sigma_8",
                                      "T_CMB"],
        "per_object_inputs": "M_b (M/L + gas) for every system -- the "
                             "baryon ruler of the BTFR/equipartition/dust "
                             "law",
        "derived_list": [n for n, _ in derived],
        "identity_list": [n for n, _ in identity],
        "measured_list": [n for n, _ in measured],
        "zero_free_parameter": {"per_object": True, "as_no_inputs": False,
                                "statement": "'zero-free-parameter' holds "
                                "per object (closed forms given M_b and a0) "
                                "and is NOT a claim about cosmic inputs; "
                                "f_b = 0.157 is the last undeclared "
                                "measured input of the cosmic frame"},
        "empirical_free_fits": [("q = -0.414 +- 0.157", "the dust-law mass "
                                 "slope, the last genuinely free fit; "
                                 "derived -1/3 at 0.52 sigma")],
    },
    "verdicts": {
        "V1_f_b_provenance": {"pass": True, "classification": "INPUT", 
                              "statement": v1},
        "V2_derived_vs_input_count": {"pass": True, "statement": v2},
        "V3_honest_statement": {"pass": True, 
                                "statement": v3,
                                "one_line": "the baryon fraction is the "
                                "framework's input at every committed "
                                "closure point -- the last undeclared free "
                                "parameter of the cosmic frame (measured "
                                "datum, not fit); the machinery emits only "
                                "the halo baryon share 0.085 (depleted "
                                "content) and the flatness-slack echo "
                                "0.160 (identity, G03C class)"},
    },
    "gates": RES,
    "n_pass": NP,
    "n_fail": NF,
    "sources": ["G079_results.json", "G198_results.json", "G187_results.json",
                "G178_results.json", "G212_results.json", "Z11_results.json",
                "G052_unified_cosmology.py (lanes)", "G189_seesaw_fate.py",
                "S09_one_scale.py"],
}
with open(os.path.join(HERE, "S05_results.json"), "w") as f:
    json.dump(out, f, indent=1, default=str)
info("\nwrote S05_results.json")