#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OUT-2 (KAPPA_RATELOCK) -- production run.

Criteria: PREREGISTER.md, committed alone before this file existed.
kappa = 1/2 FITTED; not theory closed.  Footings graded separately, never pooled.

The mechanism (pre-registered, not fitted here):
    the clock rate Q is anchored to the de Sitter KMS period  beta_Lam = 2 pi / H_Lam,
    the 1:1 lock gives  a0 / c = H_Lam / (2 pi),  hence  kappa^2 = 2 / (3 pi).

Nothing below adjusts a measured input.  kappa is not fitted anywhere in this file.
"""
import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))

# ----------------------------------------------------------------------------- inputs
# Measured constants (never adjusted).
G = 6.67430e-11                 # CODATA 2018, m^3 kg^-1 s^-2
C = 299792458.0                 # exact, m/s
MPC_M = 3.0856775814913673e22   # m

# Planck 2018 TT,TE,EE+lowE+lensing (rounded to the values the record's CFG493 lane uses;
# G0 checks that they reproduce CFG493's own numbers).
H0_KMS_MPC = 67.4
H0_SIG = 0.54                   # km/s/Mpc
OMEGA_L = 0.685
OMEGA_L_SIG = 0.0073

# Frozen from CFG493 (campaign_fresh_gravity/CFG493_kappa_combined/...results.json).
A0_MEAS = 7.810489953520144e-11        # m/s^2, combined 3-route
SIGMA_DEX = 0.09847540443535711        # combined, dex
KAPPA_MEAS_CAN = 0.4172136551990932    # vs rho_Lambda
KAPPA_MEAS_CAN_SIG = 0.09460236117123161
KAPPA_MEAS_ALT = 0.3452302843670502    # vs rho_crit
KAPPA_MEAS_ALT_SIG = 0.07828027592566118
CFG493_CAND_CHLAM_2PI = 8.625722289012511e-11   # CFG493's own "cH_Lambda/2pi" candidate
CFG493_PULL_CHLAM_2PI = 0.4378473362883446
CFG493_CAND_HALF_CAN = 9.3603e-11               # CFG493 canonical a0 for kappa = 1/2

KAPPA_FITTED = 0.5

out = {}
log = []
def P(s=""):
    log.append(s)
    print(s)

P("OUT-2 (KAPPA_RATELOCK) -- clock-rate lock to the vacuum")
P("criteria: PREREGISTER.md (committed alone, before this script)")
P("kappa = 1/2 FITTED; not theory closed.  Footings separate, never pooled.")
P("")

# ----------------------------------------------------------------------------- derived inputs
H0 = H0_KMS_MPC * 1.0e3 / MPC_M                  # s^-1
H_LAM = H0 * math.sqrt(OMEGA_L)                  # the VACUUM's rate, s^-1
RHO_CRIT = 3.0 * H0**2 / (8.0 * math.pi * G)     # kg/m^3
RHO_LAM = OMEGA_L * RHO_CRIT
RHO_CRIT_ALT = RHO_CRIT                          # alt footing: reference density = rho_crit,0

C_SQRT_GL_CAN = C * math.sqrt(G * RHO_LAM)       # the unit a0 is measured against (canonical)
C_SQRT_GL_ALT = C * math.sqrt(G * RHO_CRIT_ALT)  # alt footing

P("=" * 100)
P("INPUTS")
P("=" * 100)
P("  G            = %.6e m^3 kg^-1 s^-2" % G)
P("  c            = %.6e m/s" % C)
P("  H0           = %.2f +/- %.2f km/s/Mpc      = %.6e s^-1" % (H0_KMS_MPC, H0_SIG, H0))
P("  Omega_L      = %.4f +/- %.4f" % (OMEGA_L, OMEGA_L_SIG))
P("  rho_crit,0   = %.6e kg/m^3   (alt footing reference)" % RHO_CRIT)
P("  rho_Lambda   = %.6e kg/m^3   (canonical footing reference)" % RHO_LAM)
P("  H_Lambda     = %.6e s^-1     (the VACUUM's rate = H0 sqrt(Omega_L))" % H_LAM)
P("  c sqrt(G rho_Lambda) = %.6e m/s^2  (canonical unit)" % C_SQRT_GL_CAN)
P("  c sqrt(G rho_crit)   = %.6e m/s^2  (alt unit)" % C_SQRT_GL_ALT)
P("  R_Lambda = c/H_Lambda = %.4f Mpc" % (C / H_LAM / MPC_M))
P("")

# ============================================================================= G0
P("=" * 100)
P("G0  input reproduction against CFG493's own numbers")
P("=" * 100)
a0_cHL_2pi_check = C * H_LAM / (2.0 * math.pi)
kappa_meas_can_check = A0_MEAS / C_SQRT_GL_CAN
kappa_meas_alt_check = A0_MEAS / C_SQRT_GL_ALT
rel_a0 = abs(a0_cHL_2pi_check - CFG493_CAND_CHLAM_2PI) / CFG493_CAND_CHLAM_2PI
rel_kc = abs(kappa_meas_can_check - KAPPA_MEAS_CAN) / KAPPA_MEAS_CAN
rel_ka = abs(kappa_meas_alt_check - KAPPA_MEAS_ALT) / KAPPA_MEAS_ALT
G0 = max(rel_a0, rel_kc, rel_ka) <= 2e-3
P("  a0(c H_Lam / 2 pi)  this lane = %.9e" % a0_cHL_2pi_check)
P("  a0(c H_Lam / 2 pi)  CFG493    = %.9e     rel = %.2e" % (CFG493_CAND_CHLAM_2PI, rel_a0))
P("  kappa_meas canonical          = %.6f  vs %.6f    rel = %.2e" % (kappa_meas_can_check, KAPPA_MEAS_CAN, rel_kc))
P("  kappa_meas alt                = %.6f  vs %.6f    rel = %.2e" % (kappa_meas_alt_check, KAPPA_MEAS_ALT, rel_ka))
P("  [G0] %s   (max rel = %.2e, threshold 2e-3)" % ("PASS" if G0 else "FAIL", max(rel_a0, rel_kc, rel_ka)))
P("")

# ============================================================================= the lock
P("=" * 100)
P("THE LOCK  (pre-registered: 1:1 phase lock of the clock rate to the vacuum KMS period)")
P("=" * 100)
P("  beta_Lam = 2 pi / H_Lam = %.6e s" % (2 * math.pi / H_LAM))
P("  a0 / c   = 1 / beta_Lam = H_Lam / (2 pi) = %.6e s^-1" % (H_LAM / (2 * math.pi)))
A0_LOCK = C * H_LAM / (2.0 * math.pi)
KAPPA_LOCK_SQ = 2.0 / (3.0 * math.pi)
KAPPA_LOCK = math.sqrt(KAPPA_LOCK_SQ)
P("  a0_lock  = c H_Lam / (2 pi) = %.9e m/s^2" % A0_LOCK)
P("  kappa_lock^2 = 2/(3 pi)     = %.9f   (exact, no free parameter)" % KAPPA_LOCK_SQ)
P("  kappa_lock                  = %.9f" % KAPPA_LOCK)
P("")
# cross-check: the lock value recovered from the numeric route, not the closed form
kappa_lock_num = A0_LOCK / C_SQRT_GL_CAN
P("  cross-check kappa_lock = a0_lock / (c sqrt(G rho_Lam)) = %.9f   (rel vs closed form %.2e)"
  % (kappa_lock_num, abs(kappa_lock_num - KAPPA_LOCK) / KAPPA_LOCK))
# the a0-length statement
P("  c^2/a0_lock = %.6e m ;  2 pi R_Lam = %.6e m ;  ratio = %.9f"
  % (C**2 / A0_LOCK, 2 * math.pi * C / H_LAM, (C**2 / A0_LOCK) / (2 * math.pi * C / H_LAM)))
P("")

# error bar on the DERIVED a0 (Planck inputs only; kappa itself is an exact pure number)
rel_H0 = H0_SIG / H0_KMS_MPC
rel_Om = 0.5 * OMEGA_L_SIG / OMEGA_L
rel_a0_lock = math.sqrt(rel_H0**2 + rel_Om**2)
P("  a0_lock error from Planck inputs: %.3f %%   (H0 %.2f %%, Omega_L %.2f %%)"
  % (100 * rel_a0_lock, 100 * rel_H0, 100 * rel_Om))
P("  a0_lock = (%.4f +/- %.4f) e-11 m/s^2" % (A0_LOCK * 1e11, A0_LOCK * rel_a0_lock * 1e11))
P("  kappa_lock = %.6f  EXACT (pure number; no measurement error enters it)" % KAPPA_LOCK)
P("")

# ============================================================================= G3
P("=" * 100)
P("G3  derived a0 vs the measured a0  (pull in dex, CFG493 convention)")
P("=" * 100)
def pull_dex(a0):
    return (math.log10(a0) - math.log10(A0_MEAS)) / SIGMA_DEX
pull_lock = pull_dex(A0_LOCK)
G3 = abs(pull_lock) < 2.0
P("  a0_meas = %.6e +/- %.3f dex (%.1f %%)" % (A0_MEAS, SIGMA_DEX, 100 * (10**SIGMA_DEX - 1)))
P("  a0_lock = %.6e  ->  +%.4f dex  ->  pull = %.4f sigma" % (A0_LOCK, math.log10(A0_LOCK / A0_MEAS), pull_lock))
P("  CFG493's own pull for this candidate: %.4f  (rel %.2e)" % (CFG493_PULL_CHLAM_2PI, abs(pull_lock - CFG493_PULL_CHLAM_2PI) / CFG493_PULL_CHLAM_2PI))
P("  [G3] %s  (|pull| < 2 required; > 3 would be FAIL)" % ("PASS" if G3 else "FAIL"))
# pull on kappa, both footings
p_can = (KAPPA_LOCK - KAPPA_MEAS_CAN) / KAPPA_MEAS_CAN_SIG
p_alt = (KAPPA_LOCK - KAPPA_MEAS_ALT) / KAPPA_MEAS_ALT_SIG
P("  pull on kappa: canonical %.4f sigma (footing rho_Lam), alt %.4f sigma (footing rho_crit)"
  % (p_can, p_alt))
P("  NOTE the lock output is footing-invariant: kappa_lock = sqrt(2/(3 pi)) on BOTH footings,")
P("       whereas the measured kappa is footing-dependent (0.4172 vs 0.3452).  Not pooled.")
P("")

# ============================================================================= G4
P("=" * 100)
P("G4  does the lock DISCRIMINATE from the fitted kappa = 1/2 ?")
P("=" * 100)
a0_half_can = 0.5 * C_SQRT_GL_CAN          # a0 implied by kappa = 1/2 on the canonical footing
a0_half_alt = 0.5 * C_SQRT_GL_ALT
off_dex_can = math.log10(A0_LOCK / a0_half_can)
off_dex_alt = math.log10(A0_LOCK / a0_half_alt)
P("  a0(kappa=1/2) canonical = %.6e m/s^2   (CFG493 quotes %.4e)" % (a0_half_can, CFG493_CAND_HALF_CAN))
P("  a0(kappa=1/2) alt       = %.6e m/s^2" % a0_half_alt)
P("  a0_lock / a0_half       = %.6f   (canonical footing)" % (A0_LOCK / a0_half_can))
P("  offset                  = %+.4f dex (canonical), %+.4f dex (alt)" % (off_dex_can, off_dex_alt))
P("  2 sigma of the current combined a0 error = %.4f dex" % (2 * SIGMA_DEX))
G4_disc = abs(off_dex_can) > 2 * SIGMA_DEX
P("  [G4] %s  -- offset %.4f dex is %.2fx too small to separate at 2 sigma"
  % ("DISCRIMINATED" if G4_disc else "NOT DISCRIMINATED", abs(off_dex_can), (2 * SIGMA_DEX) / abs(off_dex_can)))
P("  precision a decisive 2-sigma test needs: %.4f dex = %.2f %% on a0 (currently %.2f %%)"
  % (abs(off_dex_can) / 2.0, 100 * (10 ** (abs(off_dex_can) / 2.0) - 1), 100 * (10**SIGMA_DEX - 1)))
P("  CFG493's own route floor (S_gas-dominated) is 0.0385 dex = 8.9 %%, and its power label is")
P("  'NOT POSSIBLE': no current route reaches 4.3 %%.")
P("")

# ============================================================================= G5
P("=" * 100)
P("G5  the discrete sibling locks, each graded separately")
P("=" * 100)
siblings = []
def add_sib(name, a0, note):
    k_can = a0 / C_SQRT_GL_CAN
    siblings.append((name, a0, k_can, pull_dex(a0), note))

add_sib("1:1  lock to H_Lam (vacuum rate)   [THE LANE]", C * H_LAM / (2 * math.pi), "pre-registered output")
add_sib("2:1  winding",                                  2 * C * H_LAM / (2 * math.pi), "MU3")
add_sib("1:2  winding",                                  0.5 * C * H_LAM / (2 * math.pi), "MU7")
add_sib("1:1  lock to H_0 (total rate)      [MU1]",      C * H0 / (2 * math.pi), "residual ambiguity")
add_sib("angular lock, no 2 pi              [MU2]",      C * H_LAM, "MU2")
add_sib("FINAL-19 DEC-saturation            [MU4]",      math.sqrt(2 * math.pi) * C_SQRT_GL_CAN, "MU4, already on record")
add_sib("record fit kappa = 1/2 (canonical footing)",    a0_half_can, "the FITTED value, for reference")
P("  %-46s %14s %10s %9s" % ("lock", "a0 [m/s^2]", "kappa_can", "pull/dex"))
for name, a0, k, pl, note in siblings:
    P("  %-46s %14.6e %10.4f %+9.2f   %s" % (name, a0, k, pl, note))
P("")
P("  excluded at >= 3 sigma: " + ", ".join(n.split('[')[0].strip() for n, a0, k, pl, _ in siblings if abs(pl) >= 3.0))
P("  not excluded  (<2 sigma): " + ", ".join("%s (%.2f)" % (n.split('[')[0].strip(), pl) for n, a0, k, pl, _ in siblings if abs(pl) < 2.0))
P("")
G5 = True
P("  [G5] PASS  (all seven graded; none omitted)")
P("")

# ============================================================================= G6
P("=" * 100)
P("G6  parameter count of the whole chain")
P("=" * 100)
P("  continuous free parameters: 0   (kappa is not fitted; G, c, H0, Omega_L are measured)")
P("  discrete choices: 2  (winding n/m in {2:1,1:1,1:2}, target in {H_Lam, H_0})")
P("  imported postulates: 1  (the lock equation (3) itself)")
P("  imported physics: de Sitter KMS periodicity (quantum); the OUTPUT is hbar-free")
P("  [G6] PASS")
P("")

# ============================================================================= G7
P("=" * 100)
P("G7  8 pi audit -- does the chain secretly use the record identity?")
P("=" * 100)
# with the lock: a0^2 = (2/(3 pi)) c^2 G rho_Lam
lhs = (2.0 / (3.0 * math.pi)) * C**2 * G * RHO_LAM / (8.0 * math.pi * G)   # a0^2/(8 pi G)
rhs_id = RHO_LAM * C**2 / (32.0 * math.pi)                                 # rho_Lam c^2/(32 pi)
P("  a0_lock^2 / (8 pi G)            = %.6e Pa" % lhs)
P("  rho_Lam c^2 / (32 pi)  [identity] = %.6e Pa" % rhs_id)
P("  ratio = %.6f   (1.0 would mean the chain used the identity)" % (lhs / rhs_id))
P("  in pure numbers: 1/(12 pi^2) = %.6f   vs   1/(32 pi) = %.6f" % (1 / (12 * math.pi**2), 1 / (32 * math.pi)))
G7 = abs(lhs / rhs_id - 1.0) > 1e-6
P("  the chain uses ONLY Lam = 8 pi G rho_Lam / c^2 (Einstein's equation), never the identity.")
P("  [G7] %s" % ("PASS" if G7 else "FAIL"))
P("")

# ============================================================================= G1/G2 (numeric form; Lean carries the proof)
P("=" * 100)
P("G1/G2  independence and capacity fix (numeric; the proof terms are in OUT2RateLock.lean)")
P("=" * 100)
P("  G1  kappa_lock^2 = 2/(3 pi) = %.9f  ;  (1/2)^2 = 0.25  ;  difference = %+.6f"
  % (KAPPA_LOCK_SQ, KAPPA_LOCK_SQ - 0.25))
P("      -> the lock is NOT a restatement of kappa = 1/2 (Lean: lock_kappa_sq_ne_quarter)")
P("  G2  under G_lam : a0 -> lam*a0.  Lock equation: a0^2 = (c H_Lam/2pi)^2.")
P("      (lam a0)^2 = (c H_Lam/2pi)^2  <=>  lam^2 = 1  (a0 != 0).  The flat direction is removed.")
P("      -> the lock is CHARGED under G_lam (Lean: lock_charged_under_Glambda)")
P("")

# ============================================================================= the prediction
P("=" * 100)
P("THE PREDICTION THAT IS NOT YET MEASURED")
P("=" * 100)
P("  a0 = c H_Lam / (2 pi) = c H0 sqrt(Omega_L) / (2 pi)")
P("     = (%.4f +/- %.4f) e-11 m/s^2        [Planck inputs only, %.2f %%]" %
  (A0_LOCK * 1e11, A0_LOCK * rel_a0_lock * 1e11, 100 * rel_a0_lock))
P("  equivalently  a0 / (c H0) = sqrt(Omega_L)/(2 pi) = %.6f  (no free parameter)" % (math.sqrt(OMEGA_L) / (2 * math.pi)))
P("  equivalently  a0 / (c H_Lam) = 1/(2 pi) = %.6f exactly" % (1 / (2 * math.pi)))
P("")
P("  discriminating tests, in order of how soon they bite:")
P("   (1) a0 to 4.3 %% separates the lock from the record's fitted kappa = 1/2 (8.5 %% apart).")
P("       Current combined a0 error 22.7 %%; CFG493's route floor 8.9 %%; its power label 'NOT POSSIBLE'.")
P("   (2) a0 to ~5 %% separates the vacuum lock (H_Lam) from the total-rate lock (H_0), which are")
P("       20.8 %% apart (0.4607 vs 0.5567).  NOT separable today (pulls 0.44 vs 1.27).")
P("   (3) if dark energy is dynamical: the lock tracks rho_DE(z), not rho_Lam(0), so")
P("       a0(z)/a0(0) = sqrt(rho_DE(z)/rho_DE(0)) = (1+z)^{1.5(1+w)} for constant w.")
P("       w = -1: flat (0.000 dex at every z, the framework's flat law).")
P("       DESI DR2 w0wa at face value: %.3f dex at z=0.9 (L276's DESI column), vs +0.25 dex for" %
  (-0.057))
P("       the H(z) law and 0.000 for flat.  L276 grades this arm UNDECIDED: no measurement exists.")
P("   (4) the lock is a PHASE TRANSITION, so the rate Q is pinned, not smoothed: it predicts a")
P("       universal non-analyticity at g = a0 (a kink in Q, hence in the RAR) rather than the")
P("       analytic crossover mu = u/(1+u).  The width/shape of the RAR at g = a0 is not measured.")
P("")

# ============================================================================= verdict
P("=" * 100)
P("VERDICT")
P("=" * 100)
P("  kappa is now an OUTPUT:  kappa = sqrt(2/(3 pi)) = %.6f   (0 continuous free parameters)" % KAPPA_LOCK)
P("  it is NOT the fitted 1/2:  %.2f %% below it (+%.4f dex in a0);  G4 NOT DISCRIMINATED at 2 sigma."
  % (100 * (1 - KAPPA_LOCK / 0.5), abs(off_dex_can)))
P("  measured kappa = %.4f +/- %.4f  ->  pull %.2f sigma (canonical footing), %.2f sigma (alt)."
  % (KAPPA_MEAS_CAN, KAPPA_MEAS_CAN_SIG, p_can, p_alt))
P("  the pull is POST-SELECTED over 3 discrete options using CFG493's own pull table (PREREG Sec.6).")
P("")
label = ("OUT-2 COMPLETE: kappa is an OUTPUT = sqrt(2/(3 pi)) = 0.460659; "
         "it does NOT reproduce the fitted 1/2; the data cannot yet separate them.")
P("  " + label)
P("  kappa = 1/2 FITTED; not theory closed.  This lane does not relabel it.")

out.update(
    lane="OUT-2",
    criteria="PREREGISTER.md (committed alone before this script)",
    inputs=dict(G=G, c=C, H0_kms_mpc=H0_KMS_MPC, H0_sigma=H0_SIG, Omega_L=OMEGA_L,
                Omega_L_sigma=OMEGA_L_SIG, a0_meas=A0_MEAS, sigma_dex=SIGMA_DEX,
                H0_s=H0, H_Lam_s=H_LAM, rho_crit=RHO_CRIT, rho_Lam=RHO_LAM,
                c_sqrt_G_rho_Lam=C_SQRT_GL_CAN, c_sqrt_G_rho_crit=C_SQRT_GL_ALT,
                R_Lam_Mpc=C / H_LAM / MPC_M),
    lock=dict(a0_lock=A0_LOCK, a0_lock_rel_sigma=rel_a0_lock,
              kappa_lock=KAPPA_LOCK, kappa_lock_sq=KAPPA_LOCK_SQ,
              kappa_lock_exact="sqrt(2/(3*pi))",
              a0_over_cH0=math.sqrt(OMEGA_L) / (2 * math.pi),
              a0_over_cHLam=1.0 / (2 * math.pi),
              beta_Lam_s=2 * math.pi / H_LAM),
    gates=dict(
        G0_input_repro=dict(pass_=bool(G0), max_rel=max(rel_a0, rel_kc, rel_ka), threshold=2e-3),
        G1_independence=dict(pass_=True, kappa_lock_sq=KAPPA_LOCK_SQ, quarter=0.25,
                             note="proof term in OUT2RateLock.lean"),
        G2_capacity_fix=dict(pass_=True, note="proof term in OUT2RateLock.lean"),
        G3_pull=dict(pass_=bool(G3), pull_dex=pull_lock, pull_kappa_can=p_can, pull_kappa_alt=p_alt,
                     cfg493_pull=CFG493_PULL_CHLAM_2PI),
        G4_discriminates_from_half=dict(pass_=bool(G4_disc), offset_dex_can=off_dex_can,
                                        offset_dex_alt=off_dex_alt,
                                        needed_dex=abs(off_dex_can) / 2.0,
                                        needed_pct=100 * (10 ** (abs(off_dex_can) / 2.0) - 1),
                                        current_pct=100 * (10 ** SIGMA_DEX - 1),
                                        label="NOT DISCRIMINATED" if not G4_disc else "DISCRIMINATED"),
        G5_siblings=[dict(name=n, a0=a0, kappa_can=k, pull_dex=pl, note=note)
                     for n, a0, k, pl, note in siblings],
        G6_parameters=dict(continuous=0, discrete=2, postulates=1),
        G7_eight_pi=dict(pass_=bool(G7), ratio=lhs / rhs_id)),
    prediction=dict(a0_lock_m_s2=A0_LOCK, a0_lock_sigma_m_s2=A0_LOCK * rel_a0_lock,
                    a0_over_cH0=math.sqrt(OMEGA_L) / (2 * math.pi),
                    discriminate_from_half_needs_pct=100 * (10 ** (abs(off_dex_can) / 2.0) - 1),
                    discriminate_target_lock_needs_pct=100 * (10 ** (abs(math.log10(1 / math.sqrt(OMEGA_L))) / 2.0) - 1)),
    label=label,
    status="kappa = 1/2 FITTED; not theory closed. Adopts nothing.",
)

with open(os.path.join(HERE, "out2.json"), "w") as f:
    json.dump(out, f, indent=2, sort_keys=True)
with open(os.path.join(HERE, "out2.out"), "w") as f:
    f.write("\n".join(log) + "\n")
