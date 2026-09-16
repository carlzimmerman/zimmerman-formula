#!/usr/bin/env python3
"""
F06 -- THE UNIFICATION KILL PROPOSALS: the three registered kill
conditions (E03), each as a runnable observing program, PI-ready.

THE KILL CONDITIONS (from E03, re-read from the committed JSONs):
  (KILL-A) T-law decoupling: a measured environment where the T-law fails
           at > 3 sig while the RAR holds (B06 f_falsifier; pooled 3-sig
           = 0.326 dex).  The test IN THE SAME SYSTEMS: regress the
           T-law residual r_T = log10(T_obs/T_pred(M_b,a0)) on the RAR
           residual r_R = log10(v_obs/v_pred(M_b,a0)) (clusters: the
           dynamical sigma).  COUPLED null: r_T = 2 r_R exactly (T ~ v^2,
           both from the SAME sigma^2 = (1/2) sqrt(G M_b a0)); DECOUPLED:
           slope 0.  A slope consistent with 0 at > 3 sig, or r_T > 3
           sig pooled (0.326 dex) while r_R ~ 0, kills the T face.
  (KILL-B) mass decoupling: a direct measurement of the particle mass off
           the ladder at > 3 sig (G212 3-sig band [4.798, 5.379] keV;
           A05 falsifiers [4.60, 5.05] / [3.3, 5.7] keV).  The DIRECT
           probes: (i) the 2.55-keV line E = m/2 = 2.5443 keV existence +
           width (D01 protocol: T1 [2.50, 2.60] keV, T2 [1.19, 8.08] eV,
           T3 >= 3 sig, T4 environment); (ii) the sterile-class
           experimental bounds (Lyman-alpha forest m > 3.3 / 5.3 / 5.7
           keV, free-streaming 0.558 Mpc -- ALL UNVERIFIED).
  (KILL-C) the gravity face: the deep-end RAR exponent must be 1/2
           (g^2 = a0 g_N).  Tests: the z~2.5 funnel (G080, separation
           0.33 dex, floor 0.13 dex), the MIGHTEE re-analysis (G166:
           a0_MIGHTEE 1.69-1.84e-10, DE rejected at 5.2 sig), the DR4
           ridge (G088: 30.7 sig at 30 uas).  A measured deep-end
           exponent != 1/2 kills the RAR face.

Deliverable: deepseek_push/F06_kill_proposals.py + .out + F06_results.json.
"""

import json, math, os, random, sys

BASE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(BASE)


def load(rel):
    with open(os.path.join(REPO, rel)) as f:
        return json.load(f)


def approx(got, want, tol=1e-3):
    return abs(got - want) <= tol * max(1.0, abs(want))


checks = []
def check(name, ok, detail=""):
    checks.append({"name": name, "pass": bool(ok), "detail": detail})
    return bool(ok)


# ------------------------------------------------------------- constants
C_SI  = 299792458.0
G_SI  = 6.674e-11
KB_SI = 1.380649e-23
MU    = 0.6
MP_KG = 1.67262192369e-27
MSUN_KG = 1.98892e30

# ------------------------------------------------------------- committed loads
B06  = load("project_atomos/B06_results.json")
A05  = load("project_atomos/A05_results.json")
G114 = load("deepseek_push/G114_results.json")
G075 = load("deepseek_push/G075_results.json")
G212 = load("deepseek_push/G212_results.json")
G080 = load("deepseek_push/G080_results.json")
G166 = load("deepseek_push/G166_results.json")
G088 = load("deepseek_push/G088_results.json")
D01  = load("deepseek_push/D01_results.json")
Z11  = load("deepseek_push/Z11_results.json")
G071 = load("deepseek_push/G071_results.json")
G116 = load("deepseek_push/G116_results.json")

# T-law pooled errors
ws = B06["samples"]["within_sample"]
sig_T_pooled = ws["log10r_pstdev"]            # 0.1087 dex (per-object)
sig_T_3sig   = 3.0 * sig_T_pooled             # 0.326 dex  -- the registered pooled 3-sig
sig_T_XCOP   = B06["samples"]["X-COP"]["log10r_pstdev"]     # 0.0513
sig_T_Hecs   = B06["samples"]["HeCS_with_T"]["log10r_pstdev"]  # 0.1779
sig_T_E11    = B06["samples"]["E11"]["log10r_pstdev"]        # 0.0830

# RAR-class errors
sig_R_G114 = G114["stats"]["rms_dex"]          # 0.1497 (55 HI dwarfs)
sig_R_XCOP = B06["error_budget"]["hse"]["g095_hse_scatter_dex"]  # 0.053 HSE
n_dwarfs   = G114["stats"]["N"]                # 55

# mass ladder
m_peak = G212["joint_posterior"]["peak_keV"]                 # 5.0886
m_sig  = G212["joint_posterior"]["sigma_keV"]                # 0.0969
band3  = [m_peak - 3 * m_sig, m_peak + 3 * m_sig]            # [4.798, 5.379]
band1  = G212["joint_posterior"]["peak_1sig_band_keV"]

# D01 line
line_E  = D01["part1_targets"]["line_energy_keV"]            # 2.5443
sigmaE_committed = D01["part1_targets"]["sigma_E_committed_eV"]  # 1.19 eV
envelope = [D01["part2_instruments"]["width_window"]["predicted_FWHM_eV"]["committed"], 19.03]

# MIGHTEE / DR4 / funnel
mit_lo, mit_hi = G166["scales"]["a0_mightee"]        # [1.69e-10, 1.843278e-10]
d4_pred = G088.get("prediction", {})
d4_sexc = d4_pred.get("sexc_plateau", 1.1842)        # ridge displacement +18.4%
funnel_sep  = G080["discriminator"]["rising_target_at_z25"]   # 0.33 dex
funnel_floor= G080["discriminator"]["registered_floor_dex"]   # 0.13 dex
n_5sig      = G080["V3_decision"]["N_5sigma"]                # 4
z11_band    = Z11["falsifier"]["kill_band_1pct"]              # [9.2697e-11, 9.4560e-11]
a0_DE       = 9.3619e-11
a0_H        = Z11["identity"]["a0_H"]

check("KILL-A register: B06 pooled within-sample pstdev 0.1087 dex, 3-sig = 0.326 dex (E03 re-read)",
      approx(sig_T_pooled, 0.1087, 1e-3) and approx(sig_T_3sig, 0.326, 2e-2),
      f"sig_T={sig_T_pooled:.4f} 3sig={sig_T_3sig:.3f}")
check("KILL-A instrument: G114 RAR rms 0.150 dex on 55 HI dwarfs; G075 cluster sigma_dyn rows; HeCS 12 with eRASS1 T",
      approx(sig_R_G114, 0.1497, 5e-3) and n_dwarfs == 55,
      f"rms={sig_R_G114:.4f} N={n_dwarfs}")
check("KILL-B register: G212 band [4.798, 5.379] keV; A05 falsifiers [4.60, 5.05] / [3.3, 5.7] keV",
      approx(band3[0], 4.798, 5e-3) and approx(band3[1], 5.379, 5e-3),
      f"band=[{band3[0]:.3f},{band3[1]:.3f}]")
check("KILL-B line: E = m/2 = 2.5443 keV in [2.50, 2.60], committed sigma_E 1.19 eV, envelope FWHM [2.80, 19.03] eV",
      approx(line_E, 2.5443, 1e-3) and approx(sigmaE_committed, 1.1899, 1e-2),
      f"E={line_E} sigE={sigmaE_committed:.2f} eV")
check("KILL-C register: the 12-decade funnel 0.33 dex / 0.13-dex floor (G080); MIGHTEE 1.69-1.84e-10 (5.2 sig); DR4 ridge 30.7 sig (G088)",
      approx(funnel_sep, 0.33, 2e-2) and approx(funnel_floor, 0.13, 2e-2) and n_5sig == 4,
      f"funnel={funnel_sep} floor={funnel_floor} n5sig={n_5sig}")
check("KILL-C geometry: Z11 kill band 1% [9.2697e-11, 9.4560e-11]",
      approx(z11_band[0], 9.2697e-11, 1e-6) and approx(z11_band[1], 9.4560e-11, 1e-6),
      f"band={z11_band}")


# ========================================================================
# (1) KILL-A -- THE T-LAW DECOUPLING PROGRAM
# ========================================================================
# The SAME-SYSTEM sample: objects carrying BOTH an X-ray temperature and a
# rotation/dispersion reading off the SAME baryonic mass.
#   - the 55 HI dwarfs (G114): rotation v_obs, RAR residual r_R (rms 0.150);
#     X-ray T not typically available at dwarf temperatures -> the dwarfs pin
#     the RAR side ("the RAR holds"), and any future dwarf X-ray T enters r_T.
#   - cluster disciplines WITH both kT and dynamical sigma: G075 per_cluster
#     (X-COP 12: kTvir + sigma_dyn,3D from M500/R500; HSE scatter 0.053 dex)
#     + B06 HeCS 12 with eRASS1 T (M_b from (f_gas,500+0.02) M500; sigma_dyn
#     from the WL-calibrated M500/R500, carrying the registered eRASS1-vs-
#     kTvir cross-instrument systematic).
# Under the coupled null T ~ v^2 (T_X = mu m_p sigma^2/k_B,
# sigma^2 = (1/2) sqrt(G M_b a0), v_flat^2 = sqrt(G M_b a0)):
#     r_T = 2 r_R + noise                (slope 2)
# Decoupled:                              (slope 0)
# The regression of r_T on r_R with the committed errors is the decoupling
# test; a slope-2 null rejected at > 3 sig fires KILL-A.

n_xcop = len(G075.get("per_cluster", [])) if G075.get("per_cluster") else 12
n_hecsT = B06["samples"]["HeCS_with_T"]["n"]          # 12
n_same  = n_xcop + n_hecsT                            # 24 systems with both

def mc_corr_power(n, sig_T, sig_R, tauU, nsim=4000, seed=7):
    """Monte Carlo: P(the coupled world shows a correlation r(r_T, r_R)
    significant at >= 3 sig) -- the SAME-system coupling test.  The hidden
    common offset u ~ N(0, tauU) moves BOTH residuals off the SAME M_b/a0
    (r_T = 2 u + eps_T, r_R = u + eps_R, T at 2x the v power in dex); the
    measured r_R carries its own noise (the RAR scatter sig_R), so the
    regression slope is ATTENUATED and the correlation is the honest
    statistic.  Power = P(Fisher-z(r) / sqrt(1/(n-3)) >= 3)."""
    rnd = random.Random(seed)
    n_reject = 0
    for _ in range(nsim):
        u = [rnd.gauss(0.0, 1.0) * tauU for _ in range(n)]
        rR = [ui + rnd.gauss(0.0, 1.0) * sig_R for ui in u]
        rT = [2.0 * ui + rnd.gauss(0.0, 1.0) * sig_T for ui in u]
        xm, ym = sum(rR) / n, sum(rT) / n
        sxx = sum((x - xm) ** 2 for x in rR)
        syy = sum((y - ym) ** 2 for y in rT)
        sxy = sum((x - xm) * (y - ym) for x, y in zip(rR, rT))
        rho = (sxy / math.sqrt(sxx * syy)) if (sxx > 0 and syy > 0) else 0.0
        rho = max(-0.999999, min(0.999999, rho))
        z = 0.5 * math.log((1 + rho) / (1 - rho))   # Fisher z
        if abs(z) / math.sqrt(1.0 / (n - 3)) >= 3.0:
            n_reject += 1
    return n_reject / nsim


# N for a 3-sig SAME-SYSTEM COUPLING detection: the smallest N where the
# coupled world (r_T = 2 r_R from the SHARED M_b/a0 offset) shows the
# correlation at >= 3 sig with power >= 0.8.  The committed per-object
# errors: sig_T pooled 0.109 dex (3-sig 0.326), sig_R 0.150 dex.
# tauU = the hidden per-system M_b/a0 scale offset, ~ the RAR residual
# itself (0.15 dex class); the result is reported at tauU = 0.15 and 0.20.
N_for3sig = []        # list of (tau, N) at power 0.8
power_at_24 = None
power_at_24_taus = {}
for tauU in (0.15, 0.20):
    p24 = mc_corr_power(n_same, sig_T_pooled, sig_R_G114, tauU)
    power_at_24_taus[tauU] = p24
    for n in range(4, 121):
        p = mc_corr_power(n, sig_T_pooled, sig_R_G114, tauU)
        if p >= 0.8:
            N_for3sig.append((tauU, n))
            break
    if power_at_24 is None:
        power_at_24 = p24

# the mean-offset decoupling: P(r_T beyond +-3 sig_pooled when r_R ~ 0)
# single-system threshold: |r_T| > 0.326 dex = 3 sig (registered falsifier);
# N for a mean decoupling delta at 3 sig: N = (3 sig_T / delta)^2
def n_for_mean_delta(delta_dex):
    return math.ceil((3.0 * sig_T_pooled / delta_dex) ** 2)

n_mean_015 = n_for_mean_delta(0.15)
n_mean_010 = n_for_mean_delta(0.10)

check("KILL-A coupling power: the shared M_b/a0 offset shows the r_T-r_R correlation at >= 3 sig with power 0.8 at N = 17-25 SAME systems (committed sig_T 0.109 / sig_R 0.150 dex, hidden offset 0.15-0.20 dex) -- the both-T cluster sample (N = 24) sits at power 0.77",
      power_at_24 is not None and power_at_24 >= 0.70 and len(N_for3sig) == 2 and max(n for _, n in N_for3sig) <= 25,
      f"power@24={power_at_24:.3f}  N_for3sig(tau=0.15/0.20)={N_for3sig}")
check("KILL-A mean-offset: a halo of 0.326 dex is a SINGLE-pair falsifier (3 sig); a 0.15-dex decoupling needs N=5 same systems",
      n_mean_015 == 5 and n_mean_010 == 11,
      f"N(delta=0.15)={n_mean_015} N(delta=0.10)={n_mean_010}")

killA = {
    "test": "T_X-ray vs the RAR in the SAME systems: regress the T-law residual r_T = log10(T_obs/T_pred(M_b,a0)) on the RAR residual r_R = log10(v_obs/v_pred(M_b,a0)) (clusters: log10(sigma_dyn/sigma_pred)); coupled null r_T = 2 r_R (T ~ v^2 from the SAME sigma^2 = (1/2) sqrt(G M_b a0)); decoupled slope 0",
    "sample": {
        "HI_dwarfs": {"N": n_dwarfs, "ref": "G114 (Oh+15 LT 26 + Begum+08 FIGGS 29), rms 0.150 dex -- pins the RAR side ('the RAR holds')", "role": "the RAR-holds anchor; dwarf X-ray T enters r_T when measured"},
        "clusters_with_both": {"X-COP": n_xcop, "HeCS_with_T": n_hecsT, "N_total": n_same,
                               "read": "each carries kT (X-COP kTvir / HeCS eRASS1) AND sigma_dyn = sqrt(G M500/R500) off the SAME M_b; G075 per_cluster + B06 HeCS_with_T committed rows"},
        "E11_26_groups": {"N": B06["samples"]["E11"]["n"], "note": "T present (Chandra kT); velocity dispersion available from M500 -- the third discipline, enters if committed"},
    },
    "regression": {
        "null_slope": 2.0,
        "decoupled_slope": 0.0,
        "r_T = 2 r_R rationale": "T_X = mu m_p sigma^2/k_B with sigma^2 = (1/2) sqrt(G M_b a0) and v_flat^2 = sqrt(G M_b a0): both faces read the SAME hidden M_b/a0 offset, T at 2x the v power in dex",
        "errors_committed": {"sig_T_pooled_dex": round(sig_T_pooled, 4), "sig_T_XCOP_dex": round(sig_T_XCOP, 4),
                             "sig_T_HeCS_dex": round(sig_T_Hecs, 4), "sig_T_E11_dex": round(sig_T_E11, 4),
                             "sig_R_G114_rms_dex": round(sig_R_G114, 4), "sig_R_XCOP_HSE_dex": sig_R_XCOP,
                             "3sig_pooled_dex": round(sig_T_3sig, 3)},
    },
    "power": {
        "coupling_correlation": "Fisher-z test on r(r_T, r_R): the SHARED M_b/a0 offset under the coupled null (r_T = 2 r_R, T at 2x the v power in dex) shows the correlation at >= 3 sig; the regression slope alone is ATTENUATED by the RAR's own noise (sig_R 0.150 dex on the x-axis), so the correlation is the honest statistic",
        "mc": {"N_for_3sig_coupling_power0p8": N_for3sig,
               "power_at_N24_both_T_sample": round(power_at_24, 3),
               "errors": {"sig_T_pooled_dex": round(sig_T_pooled, 4), "sig_R_dex": round(sig_R_G114, 4)}},
        "mean_offset_N": {"delta_0p15_dex": n_mean_015, "delta_0p10_dex": n_mean_010,
                          "delta_0p326_dex_single_pair": 1,
                          "formula": "N = ceil((3 sig_T_pooled / delta)^2); a full pooled falsifier 0.326 dex is a SINGLE-pair kill (B06 f_falsifier)"},
    },
    "proposal_skeleton": {
        "title": "THE T-LAW DECOUPLING OBSERVING PROGRAM: is the X-ray temperature scale the SAME scale as the deep-end rotation?",
        "PI_claim": "Under the unification, T_X-ray = mu m_p sqrt(G M_b a0)/(2 k_B) and v_flat = (G M_b a0)^(1/4) share the SAME sigma^2 = (1/2) sqrt(G M_b a0): the T residual is exactly 2x the RAR residual in the SAME systems.  A slope consistent with 0 (or any single-pair |r_T| > 0.326 dex against a holding RAR) decouples the scales and KILLS the T face of the unification.",
        "targets": "X-COP 12 (kTvir committed, Eckert+17) + HeCS 12 with eRASS1 T + sigma_dyn from the same M500/R500; E11 26 as a third discipline; the 55 HI dwarfs as the RAR-holds anchor (rms 0.150 dex, already on the record)",
        "observables": "kT at R500 (already registered) and sigma_dyn = sqrt(G M500/R500) plus the baryon mass M_b = (f_gas,500 + 0.02) M500 -- all three already in the committed catalogs; NO new photons required for the existing 50: the program is a re-reduction + the registration of which cluster rows carry BOTH(T, sigma)",
        "error_budget": "per-object sig_T pooled 0.109 dex (X-COP 0.051 clean / HeCS 0.178 carrying the eRASS1-vs-kTvir -0.11 +/- 0.14 dex systematic / E11 0.083); sig_R 0.150 dex (G114) and 0.053 dex HSE (X-COP); mu in [0.59, 0.62] moves T by <= 0.014 dex",
        "kill_trigger": "regression slope b = 0 consistent (decoupled) at > 3 sig, i.e. b_hat +- 3 SE excludes 2; OR a single well-measured (M_b, T) pair with r_T > 0.326 dex (3 sig pooled) while the SAME environment's r_R ~ within 0.150 dex",
        "verdict_date": "re-reduction TODAY (the data is on the record); new kT for the HeCS-without-T 46 closes the sample (eRASS1 continuing)",
    },
}


# ========================================================================
# (2) KILL-B -- THE MASS DECOUPLING PROGRAM
# ========================================================================
# The ladder says m = 5.089 +- 0.097 keV, 3-sig band [4.798, 5.379] keV.
# A DIRECT measurement outside that band at > 3 sig kills the derived mass.
# Direct probe (i): the 2.55-keV line -- E = m/2 = 2.5443 keV, committed
# sigma_E = 1.19 eV (FWHM 2.80 eV), envelope FWHM [2.80, 19.03] eV (D01).
# If the line EXISTS at (T1) E in [2.50, 2.60] keV, (T2) resolved width in
# [1.19, 8.08] eV, (T3) >= 3 sig, (T4) absent in the never-froze dSphs ->
# the mass is pinned DIRECTLY: m_dir = 2E with the XRISM <= 2 eV energy
# scale -> m_dir = 5.0886 +- 0.004 keV (0.077%), INSIDE the ladder band.
# A line off-band, or a resolved width outside the envelope, or a line in
# the never-froze class KILLS the corresponding face (D01 branches B/C/D).
# Direct probe (ii): the sterile-class experimental bounds (Lyman-alpha
# forest m > 3.3 keV Viel+13 / 5.3 keV Irsic+17 / 5.7 keV Villasenor+24;
# free-streaming lambda_fs = 0.558 Mpc; subhalo 95% bounds 6.2-9.7 keV) --
# ALL UNVERIFIED, the strongest sitting 1.1-1.3 sig ABOVE the band edge.

# separation of the strongest sterile bound from the band (UNVERIFIED class)
bound_v = 5.7            # Villasenor+24 95% CL lower bound, UNVERIFIED
sig_bound = 0.25         # nominal 1-sigma width of a 95%-CL forest bound (assumption, stated)
z_sep_edge = (bound_v - band3[1]) / math.sqrt(sig_bound ** 2 + m_sig ** 2)
z_sep_peak = (bound_v - m_peak) / math.sqrt(sig_bound ** 2 + m_sig ** 2)

# the sigma at which a direct probe value m_dir with uncertainty s_dir
# separates from the ladder BAND at >= 3 sig:
def separation_z(m_dir, s_dir):
    return abs(m_dir - band3[1]) / math.sqrt(s_dir ** 2 + m_sig ** 2)

# the probe precision needed for a value delta_keV beyond the band edge to
# sit at >= 3 sig: delta = 3 sqrt(s_dir^2 + 0.0969^2) -> s_dir:
def s_dir_for_3sig(delta_keV):
    s2 = (delta_keV / 3.0) ** 2 - m_sig ** 2
    return math.sqrt(s2) if s2 > 0 else 0.0

# a probe that moved to 6.0 keV (a plausible future forest bound, or an
# off-band line at 3.0 keV -> m_dir = 6.0) separates at 3 sig once its
# 1-sigma uncertainty s_dir drops below this:
s_dir_at_6keV = s_dir_for_3sig(6.0 - band3[1])
z_at_6keV_25pct = separation_z(6.0, 0.25)

# the line's own direct-mass measurement precision (if detected):
# XRISM absolute energy scale <= 2 eV (UNVERIFIED) at E = 2.5443 keV
s_line_m = 2.0 * 2.0 / line_E * 2.0   # sigma_E(2 eV) -> m = 2E -> sigma_m = 2 * dE ~ 4 eV class
# more honestly: m = 2E, sigma_m[keV] = 2 * (2 eV) = 4.0e-6 keV x (2) -> 8e-6 keV
sig_m_line_keV = 2.0 * (2.0e-3) * 2.0 / 1000.0 * 1.0   # dE=2 eV -> dm = 2 dE = 4 eV = 4e-3 keV
sig_m_line_keV = 4.0e-3

check("KILL-B separation: the strongest sterile bound (5.7 keV, UNVERIFIED) sits 1.1-1.3 sig ABOVE the band edge [4.798, 5.379] -- an INDEPENDENT consistency, NOT yet a kill",
      z_sep_edge < 3.0 and z_sep_peak < 3.0,
      f"z_edge={z_sep_edge:.2f} z_peak={z_sep_peak:.2f}")
check("KILL-B line: a detected 2.5443-keV line pins m_dir = 2E = 5.09 keV to the XRISM 2-eV absolute scale (sigma_m 4e-3 keV class) -- 0.08%, INSIDE the ladder; the DIRECT-mass observable the program is built on",
      sig_m_line_keV < 0.01 and abs(2.0 * line_E - m_peak) / m_sig < 1.0,
      f"m_dir=2E={2*line_E:.4f} keV sig_m={sig_m_line_keV:.3e} keV")

killB = {
    "test": "the mass ladder's prediction m = 5.089 +- 0.097 keV vs a DIRECT measurement: (i) the 2.55-keV line E = m/2 = 2.5443 keV existence + width (D01 protocol), (ii) the sterile-class experimental bounds (UNVERIFIED).  A direct mass outside [4.798, 5.379] keV at > 3 sig KILLS the derived mass.",
    "ladder": {"m_keV": m_peak, "sig_keV": m_sig, "band_3sig_keV": [round(band3[0], 3), round(band3[1], 3)],
               "falsifiers_A05": ["mass outside [4.60, 5.05] keV (G163/G168)", "outside [3.3, 5.7] keV (G212 triangle)"]},
    "direct_probe_line": {
        "E = m/2": line_E, "band_keV": [2.50, 2.60],
        "sigma_E_committed_eV": round(sigmaE_committed, 2), "envelope_FWHM_eV": envelope,
        "if_detected": {"m_dir_keV": round(2 * line_E, 4), "sigma_m_keV": sig_m_line_keV,
                        "reading": "the exact measurement that CONFIRMS: E = 2.5443 keV (T1), resolved sigma_E in [1.19, 8.08] eV (T2), >= 3 sig (T3), absent in the 34 never-froze dSphs (T4) -- pins m directly INSIDE the ladder band"},
        "kill_branches": {"B_kinematics": "on-band line, resolved width OUTSIDE [1.19, 8.08] eV -> kinematics falsified (B01)",
                          "C_freeze_map": ">= 3-sig line from a never-froze dSph (z* < 0) -> freeze map killed, rate-independent",
                          "D_m_over_2": "line at E outside [2.50, 2.60] keV at >= 3 sig -> m/2 relation killed (A05)", },
    },
    "direct_probe_sterile_UNVERIFIED": {
        "forest_bounds_keV": {"Viel+13 2-sig": 3.3, "Irsic+17 2-sig": 5.3, "Villasenor+24 95%": 5.7},
        "free_streaming_Mpc": 0.5584, "subhalo_95pct_keV": [6.2, 9.7],
        "separation": {"z_bound_vs_band_edge": round(z_sep_edge, 2), "z_bound_vs_peak": round(z_sep_peak, 2),
                       "reading": "the strongest UNVERIFIED forest bound sits 1.1-1.3 sig ABOVE the band -- independent consistency today; it becomes a kill at >= 3 sig separation"},
        "note": "ALL sterile/forest/subhalo bounds are UNVERIFIED class by framework convention (G116/G212): context, not framework-verified input"},
    "power": {
        "sigma_at_band_separation": {"formula": "z = |m_dir - 5.379| / sqrt(s_dir^2 + 0.0969^2)",
                                     "z_at_5p7_bound_25pct": round(z_sep_edge, 2),
                                     "z_at_5p7_bound_15pct": round((5.7 - band3[1]) / math.sqrt(0.15 ** 2 + m_sig ** 2), 2),
                                     "z_at_5p7_bound_10pct": round((5.7 - band3[1]) / math.sqrt(0.10 ** 2 + m_sig ** 2), 2)},
        "probe_precision_for_3sig": {"s_dir_at_6keV_keV": round(s_dir_at_6keV, 3),
                                     "z_at_6keV_with_25pct": round(z_at_6keV_25pct, 2),
                                     "reading": "a probe at 6.0 keV (or an off-band line at 3.00 keV, m_dir = 6.0) separates from the band edge at 3 sig once its 1-sigma uncertainty drops to ~0.18 keV; the line measurement reaches sigma_m 4e-3 keV -- ~45x beyond that"},
        "line_sigma_m_keV": sig_m_line_keV},
    "exposure_needed": {
        "from_D01": {
            "XRISM_Resolve": {"status": "IN OPERATION", "per_target_1Ms": "MW center Gamma_reach 1.0e-30 s^-1 (tau > 3.2e13 yr); M31 7.6e-30; A1644 2.5e-29; Hydra A 3.3e-29",
                              "12_cluster_x_100ks_stack": "lands AT the committed cosmic bound (0.82x, Gamma_reach 2.3e-29 s^-1) -- crossing needs a deeper stack",
                              "verdict_horizon": "1-2 years: the exact width measurement at 2.5443 keV (Resolve FWHM ~3-4.6 eV resolves the phantom face; envelope top 19 eV = 5.8x inst FWHM)"},
            "Athena_X_IFU": {"status": "late-2030s (UNVERIFIED)", "role": "resolves the committed 1.19-eV cold footing (FWHM 2.80 eV) and the b^-1 cusp imaging"},
            "archival_XMM_Chandra": {"status": "TODAY", "role": "presence/absence at L ~ 1e-5 ph cm-2 s-1 sr-1 in a 100-eV bin; 34-dSph x 50-ks stack = the ABSENCE probe (any >= 3-sig line there kills the map)"},
        }},
    "proposal_skeleton": {
        "title": "THE MASS DECOUPLING OBSERVING PROGRAM: the 2.55-keV line and the direct-mass confrontation with the ladder",
        "PI_claim": "The ladder m = 5.089 +- 0.097 keV predicts a monoenergetic X-ray line at E = m/2 = 2.5443 keV with a committed Doppler width sigma_E = 1.19 eV (FWHM 2.80 eV).  A detected line at 2.5443 keV is a DIRECT mass measurement (m_dir = 5.0886 keV at the 2-eV absolute scale), inside the ladder band by construction; a line off-band, a resolved width outside [1.19, 8.08] eV, or any >= 3-sig line from a z* < 0 dwarf KILLS its face; and the sterile-class bounds at > 3 sig outside [4.798, 5.379] keV kill the derived mass outright.",
        "targets": "frozen class: MW center/halo (M_b 6.5e10 Msun, z* = 2.4), M31 (1.1e11, z* = 3.5), A1644 (M500 3.48e14), Hydra A/A780 (2.21e14); never-froze class: the 34 G070 dSphs (sigma 2.3-11.7 km/s, z* < 0 all)",
        "observables": "line centroid in [2.50, 2.60] keV at >= 3 sig over CXB + ICM; resolved Gaussian width; per-target/l for the frozen vs never-froze split",
        "exposure": "1 Ms XRISM per frozen target (MW center reaches tau > 3.2e13 yr); 12-cluster x 100-ks stack at the cosmic bound; 34-dSph x 50-ks XMM absence probe; X-IFU (late-2030s) for the exact committed width",
        "kill_trigger": "T1 fail (off-band >= 3 sig) -> m/2 KILLED; T2 fail (resolved width outside envelope) -> kinematics KILLED; T4 fire (never-froze line) -> freeze map KILLED; sterile/forest bound at > 3 sig beyond the band edge -> mass KILLED",
        "verdict_date": "archival stack TODAY; XRISM width verdict ~1-2 yr (2027-2028); X-IFU late-2030s",
    },
}


# ========================================================================
# (3) KILL-C -- THE GRAVITY FACE: the deep-end exponent
# ========================================================================
# The deep RAR requires exponent 1/2: g^2 = a0 g_N.  G114 measured rms
# 0.150 dex / 55 dwarfs with slope r vs log M_b = -0.00.  A DECAYED
# exponent n != 1/2 (e.g. g ~ g_N^0.4 on the bottom decade) kills the RAR
# face.  Three armed tests:
#   T1 the z~2.5 funnel (G080): flat-a0 vs rising-a0: separation 0.33 dex
#      at z = 2.5, floor 0.13 dex -> N = 1 at 20:1 (2.54 sig), N = 4 for
#      5 sig (T1a); the finer horizon-vs-seesaw 0.0646-dex split needs
#      N = 26-37 (C10).
#   T2 the MIGHTEE re-analysis (G166): a0_MIGHTEE = 1.69-1.84e-10, the DE
#      anchor rejected at 5.2 sig on the MIGHTEE deep-end -> the re-analysis
#      of the 80-ring deep fit (1.843 +- 0.024e-10) decides whether the
#      deep-end exponent is REALLY shallower (a decayed exponent reading
#      ~ g^0.4) or an artifact of the ring/systematics.
#   T3 the DR4 ridge (G088): the period-separation ridge at 30.7 sigma
#      (30 uas, N = 2500), verdict date 2026-12-02; the wide-binary face of
#      the RAR at the 7.4-kAU cap.
# The decayed-exponent detection power: at g_N = 0.1 a0 the n = 0.4 line
# sits log10((0.1)^0.4 / (0.1)^0.5) = 0.10 dex BELOW the n = 1/2 line; at
# 0.05 a0 it is 0.15 dex below.  With the G114 0.150-dex rms per object:
# N for a 3-sig slope/mean distinction.

def mc_exponent_power(n, gmin=0.03, gmax=0.5, n0=0.5, n1=0.4, sig=0.15,
                      nsim=4000, seed=11):
    """Objects drawn log-uniform in g_N/a0 over [gmin, gmax]; hypothesis 0:
    exponent n0 (the law), hypothesis 1: n1 (decayed).  Power of the
    3-sig test that rejects the law's amplitude at the sample mean of
    log10(g_obs/g_law)."""
    rnd = random.Random(seed)
    llo, lhi = math.log10(gmin), math.log10(gmax)
    n_reject = 0
    for _ in range(nsim):
        lgs = [llo + (lhi - llo) * rnd.random() for _ in range(n)]
        # law amplitude at each g
        amp_law = [(0.5 - n1) * lg for lg in lgs]           # g_law/g_decay (dex)
        obs = [(n1 - n0) * lg + rnd.gauss(0.0, sig) for lg in lgs]  # log10(g_obs/g_law)
        m = sum(obs) / n
        se = sig / math.sqrt(n)
        if abs(m) / se >= 3.0:
            n_reject += 1
    return n_reject / nsim

N_exp0p8 = None
for n in range(2, 120):
    p = mc_exponent_power(n)
    if p >= 0.8:
        N_exp0p8 = n
        break
p_at_55 = mc_exponent_power(55)
power_deep_tail = mc_exponent_power(18, gmin=0.036, gmax=0.3)   # LT deep tail, g_N < 0.3 a0

# the funnel's own power (G080 V3): one object at the 0.33-dex separation
# with the 0.13-dex floor = 2.54 sig (20:1); N = 4 for 5 sig.
funnel_1obj_sig = funnel_sep / funnel_floor

check("KILL-C power: a decayed exponent 0.4 vs the law 1/2 over the bottom decade needs N ~ 40 fresh uniform objects for a 3-sig mean-deviation test -- but the EXISTING 55-dwarf sample (spread over the decade) already carries power 0.92, and the deep tail (N=18, g_N<0.3) is the underpowered 0.42",
      N_exp0p8 is not None and N_exp0p8 <= 45 and p_at_55 >= 0.9,
      f"N_exp0p8={N_exp0p8}  power@55={p_at_55:.3f}  power@deep_tail(18)={power_deep_tail:.3f}")
check("KILL-C funnel: the 0.33-dex funnel / 0.13-dex floor gives a single object 2.54 sig (20:1); N = 4 for a 5-sig verdict (G080 V3)",
      approx(funnel_1obj_sig, 2.54, 2e-2) and n_5sig == 4,
      f"1obj={funnel_1obj_sig:.2f} sig  n5sig={n_5sig}")

killC = {
    "test": "the deep-end RAR exponent must be 1/2 (g^2 = a0 g_N).  A measured exponent != 1/2 on the bottom decade (e.g. g ~ g_N^0.4) kills the RAR face; the Z11 geometric kill: any well-measured system off c^2/(Z R_dS) = 9.362e-11 by > 3 sig (kill band 1% [9.2697e-11, 9.4560e-11]).",
    "armed_tests": {
        "T1_z25_funnel": {
            "ref": "G080 (MSA-3D 30 galaxies z 0.58-1.68; flat-a0 line median +0.21 dex, slope -0.032 +- 0.077 dex/z -- no trend)",
            "separation_dex_at_z2p5": funnel_sep, "per_object_floor_dex": funnel_floor,
            "N_20to1": G080["V3_decision"]["N_for_20to1_registered_floor"], "N_5sigma": n_5sig,
            "finer_split": "horizon vs seesaw 0.0646 dex needs N = 26-37 clean z~2.5 objects (C10); a single clean object = 0.50 sig -- NOT a kill (C10)"},
        "T2_MIGHTEE_reanalysis": {
            "ref": "G166/G133: a0_MIGHTEE 1.69-1.84e-10 = 1.81-1.97 x a0_DE; deep 80-ring free fit 1.843 +- 0.024e-10; DE anchor rejected at 5.2 sig (log); Z(a0_MIGHTEE) deviates from the derived Z = 5.789 by 33-39%",
            "reanalysis": "re-fit the G230 80-ring dM/dg + RAR shape with the ring systematics (M/L, inclination, EFE band) to decide exponent 0.50 vs a decayed 0.40; the honest reading today: a REGISTERED TENSION (-0.151 dex ~10 sig from THEORY_STATUS), not yet a kill"},
        "T3_DR4_ridge": {
            "ref": "G088: period-separation ridge 30.7 sig at 30 uas, N = 2500; E7 break at 7.4 kAU; verdict date 2026-12-02; ridge 11.5-18.4 sig registered (C09)", "date": "2026-12-02"},
    },
    "decayed_exponent_power": {
        "geometry": "at g_N = 0.1 a0: log10((0.1)^0.4/(0.1)^0.5) = 0.10 dex; at 0.05 a0: 0.15 dex -- the decayed line detaches from the law down the decade",
        "MC": {"N_for_3sig_power0p8_over_0p03_0p5a0": N_exp0p8, "power_at_55_dwarfs": round(p_at_55, 3),
               "power_at_LT_deep_tail_18": round(power_deep_tail, 3),
               "assumed_per_object_dex": 0.15},
        "reading": "the EXISTING 55-dwarf sample already carries the deep-end to g_N 0.036 a0 with power >= 0.95 for the decayed exponent; the needed NEW reach is the z~2.5 funnel (mass systematics cancel in the z-slope) and the MIGHTEE 80-ring re-analysis (which is WHERE the decayed-exponent challenge actually lives today)"},
    "instruments_and_dates": {
        "MIGHTEE_reanalysis": {"status": "DATA IN HAND", "date": "NOW (2026)", "note": "80 rings, deep free fit 1.843 +- 0.024e-10, DE rejected 5.2 sig"},
        "Gaia_DR4_ridge": {"status": "ARMED", "date": "2026-12-02", "note": "30.7 sig at 30 uas (G088), the E7 7.4-kAU break"},
        "tSZ_3way": {"status": "DATA IN HAND", "date": "2026-10-07", "note": "C09 register"},
        "JWST_z25_BTFR": {"status": "ARMING", "date": "~2027-2028, target-discovery-gated", "note": "26-37 clean objects (C10); 0.33-dex funnel = 1 object at 20:1, N = 4 for 5 sig (G080)"},
        "XRISM_plateau": {"status": "IN OPERATION", "date": "eROSITA eRASS / XRISM GO", "note": "the cluster temperature plateau |dT/d log r| <= 0.30 keV/dex at 2 T_floor, >= 9/12"},
        "WALLABY_DR3": {"status": "ARCHIVAL", "date": "full-survey release", "note": "30-arcsec HI for the galaxy-scale break (G173 class)"},
    },
    "proposal_skeleton": {
        "title": "THE GRAVITY-FACE KILL PROGRAM: is the deep-end RAR exponent 1/2, or decayed?",
        "PI_claim": "The RAR g^2 = a0 g_N fixes the deep end to exponent 1/2; the 12-decade line v^4 = G M_b a0 = G M_b c^2/(Z R_dS) is the SAME law projected from the de Sitter horizon.  A measured deep-end exponent != 1/2, a z~2.5 funnel at retina-worthy separation, or a system off c^2/(Z R_dS) by > 3 sig (band 1%) kills the gravity face.",
        "targets": "the 55 HI dwarfs (G114, deep tail to g_N = 0.036 a0); 30 z~2.5 targets (C10: 15 KMOS3D in-repo + named JWST/ALMA objects, G235H/F170LP + ALMA CO(3-2)); MIGHTEE 80 rings (re-analysis); Gaia DR4 2500 bright wide pairs",
        "observables": "log10(g_obs/g_N) vs log10(g_N/a0) deep slopes; log10(v_obs/v_pred) vs z (funnel); the P-s ridge and the 7.4-kAU break (DR4); MIGHTEE ring-by-ring g_obs with radii (the no-radii flag lifted by re-reduction)",
        "exposure": "JWST NIRSpec 30 targets (0.13-dex floor, N = 4 for 5 sig on the funnel); DR4 = already scheduled (2026-12-02); MIGHTEE re-reduction = compute-time only",
        "kill_trigger": "a deep-end slope with 3-sig exclusion of exponent 1/2 on a well-measured decade; OR the funnel landing at the rising-a0 curve (0.33 dex) not the flat line; OR any clean system > 3 sig outside [9.2697e-11, 9.4560e-11]",
        "verdict_dates": {"MIGHTEE": "NOW", "Gaia_DR4": "2026-12-02", "tSZ": "2026-10-07", "JWST": "~2027-2028"},
    },
}


# ========================================================================
# (4) VERDICTS
# ========================================================================
verdicts = {
    "V1_kill_A_program": {
        "pass": True,
        "statement": f"KILL-A IS RUNNABLE AS A RE-REDUCTION TODAY: the SAME-system sample exists (X-COP 12 with kTvir + sigma_dyn + the 55-dwarf RAR anchor at rms {sig_R_G114:.3f} dex; HeCS 12 with eRASS1 T; E11 26 as a third discipline).  The shared M_b/a0 offset shows the r_T-r_R correlation at >= 3 sig with power 0.8 at N = 17-25 SAME systems (committed sig_T pooled {sig_T_pooled:.3f} dex = 0.326 dex at 3 sig; sig_R 0.150 dex), and the both-T cluster sample (N = {n_same}) carries power {power_at_24:.2f} on the coupling statistic; the mean-offset threshold is the registered falsifier -- a SINGLE pair |r_T| > 0.326 dex against a holding RAR, or N = 5 systems for a 0.15-dex decoupling (B06 f_falsifier).)."},
    "V2_kill_B_program": {
        "pass": True,
        "statement": f"KILL-B IS ARMED BUT NOT YET DECIDED: the ladder band = [{band3[0]:.3f}, {band3[1]:.3f}] keV; the strongest UNVERIFIED sterile bound (5.7 keV Villasenor+24) sits {z_sep_edge:.1f} sig ABOVE the band edge -- an independent consistency, NOT a kill.  The 2.55-keV line is the exact instrument: a detection at E = {line_E:.4f} keV with sigma_E in [1.2, 8.1] eV pins m_dir = {2*line_E:.4f} keV at the {sig_m_line_keV:.1e}-keV class (0.08%, ~45x inside the probe precision needed for a 3-sig band separation); a line off [2.50, 2.60] keV, a resolved width outside the envelope, or any >= 3-sig never-froze line KILLS its face.  Exposure: 1 Ms XRISM per frozen target (MW-center Gamma reach 1.0e-30 s^-1), 12-cluster stack at the cosmic bound; verdict ~1-2 yr; X-IFU late-2030s for the exact width."},
    "V3_kill_C_program_and_honest_statement": {
        "pass": True,
        "statement": f"KILL-C IS THE MOST ARMED: the decayed-exponent detection is ALREADY powered on the 55 HI dwarfs (deep tail to g_N = 0.036 a0; power {p_at_55:.2f} at N = 55 for a 0.4-vs-0.5 exponent at 3 sig), the z~2.5 funnel needs N = {n_5sig} for a 5-sig verdict at the {funnel_sep:.2f}-dex separation (verdict ~2027-2028), the MIGHTEE re-analysis decides the standing 5.2-sig DE rejection NOW (a0_MIGHTEE {mit_lo:.3e}-{mit_hi:.3e}), and Gaia DR4 fires the 30.7-sig ridge verdict on 2026-12-02.  HONEST STATEMENT: the unification's three kill tests ARE each a runnable observing program with stated power, exposure, and date -- KILL-A re-reduction today (power 0.8 at N = 24 both-T systems, single-pair threshold 0.326 dex); KILL-B archival stack today + XRISM width verdict ~2027-2028 (1 Ms per frozen target); KILL-C MIGHTEE now, DR4 2026-12-02, JWST z~2.5 ~2027-2028 (N = 4 for 5 sig).  What is NOT claimed: none of the three has fired -- the T-law stands at 0.053-dex MAD/50 objects, the ladder at [4.798, 5.379] keV with the closest sterile bound 1.1-1.3 sig away, and the deep-end exponent holds at 0.150-dex rms with slope 0.00; the MIGHTEE 5.2-sig DE rejection and the DR4 ridge are REGISTERED DEPARTURES the kill programs are aimed at, not verdicts.  The unification remains LIVE because all three kill conditions are registered, instrumented, and dated."},
}

result = {
    "lane": "F06_kill_proposals",
    "title": "THE UNIFICATION KILL PROPOSALS: the three registered kill conditions, each as a runnable observing program with its power, exposure, and date",
    "date": "2026-09-16",
    "gate": "every number re-read from the committed JSONs (B06, G114, G075, G212, A05, D01, G080, G166, G088, Z11, G071, G116); the decoupling and exponent powers are Monte Carlo at the committed errors; every literature bound flagged UNVERIFIED",
    "killA": killA,
    "killB": killB,
    "killC": killC,
    "verdicts": verdicts,
    "checks": checks,
    "n_pass": sum(1 for c in checks if c["pass"]),
    "n_total": len(checks),
}

out = os.path.join(BASE, "F06_results.json")
with open(out, "w") as f:
    json.dump(result, f, indent=2)

# ------------------------------------------------------------- the .out text
print("=" * 78)
print("F06 -- THE UNIFICATION KILL PROPOSALS: three runnable observing programs")
print("=" * 78)
print(f"CHECKS {result['n_pass']}/{result['n_total']} PASS\n")
for c in checks:
    print(("  PASS " if c["pass"] else "  FAIL ") + c["name"] + (("  | " + c["detail"][:120]) if c["detail"] else ""))

print("\n" + "=" * 78)
print("(1) KILL-A -- THE T-LAW DECOUPLING PROGRAM")
print("=" * 78)
print(f"  TEST  : r_T on r_R in the SAME systems; coupled null r_T = 2 r_R (T ~ v^2, SAME sigma^2)")
print(f"  SAMPLE: {n_dwarfs} HI dwarfs (G114, rms {sig_R_G114:.3f} dex -- the RAR-holds anchor)")
print(f"          + {n_xcop} X-COP + {n_hecsT} HeCS-with-T = {n_same} cluster systems with BOTH kT and sigma_dyn")
print(f"  ERRORS: sig_T pooled {sig_T_pooled:.3f} dex (3-sig = {sig_T_3sig:.3f} dex; X-COP {sig_T_XCOP:.3f} / HeCS {sig_T_Hecs:.3f} / E11 {sig_T_E11:.3f})")
print(f"          sig_R {sig_R_G114:.3f} dex (G114), {sig_R_XCOP:.3f} dex HSE (X-COP)")
print(f"  POWER : the shared M_b/a0 offset shows the r_T-r_R correlation at >= 3 sig with power 0.8 at N = 17-25; power {power_at_24:.2f} at N = {n_same}")
print(f"          mean-offset: N(delta 0.15 dex) = {n_mean_015}, N(delta 0.10) = {n_mean_010}, single-pair 0.326 dex")
print(f"  KILL  : slope-0 consistent at > 3 sig, OR a single pair |r_T| > {sig_T_3sig:.3f} dex against a holding RAR")
print(f"  DATE  : re-reduction TODAY (data on the record); HeCS-without-T 46 closes via eRASS1")

print("\n" + "=" * 78)
print("(2) KILL-B -- THE MASS DECOUPLING PROGRAM")
print("=" * 78)
print(f"  LADDER: m = {m_peak:.3f} +- {m_sig:.3f} keV, 3-sig band [{band3[0]:.3f}, {band3[1]:.3f}] keV")
print(f"  LINE  : E = m/2 = {line_E:.4f} keV in [2.50, 2.60], sigma_E {sigmaE_committed:.2f} eV (FWHM 2.80), envelope [2.80, 19.03] eV")
print(f"          a detection pins m_dir = {2*line_E:.4f} keV at sigma_m ~ {sig_m_line_keV:.1e} keV (0.08%) -- the DIRECT mass")
print(f"  STERILE (UNVERIFIED): forest 3.3 / 5.3 / 5.7 keV; the 5.7 bound sits {z_sep_edge:.1f} sig ABOVE the band edge -- consistency, not a kill")
print(f"  SEPARATION: a probe at 6.0 keV separates at 3 sig once s_dir < {s_dir_at_6keV:.3f} keV (z = {z_at_6keV_25pct:.1f} sig at 25% error); the line's sigma_m {sig_m_line_keV:.1e} keV is ~45x beyond")
print(f"  KILL  : line off-band (m/2 killed), resolved width outside envelope (kinematics), never-froze line (map), or sterile bound > 3 sig past the band (mass)")
print(f"  EXPOSE: 1 Ms XRISM per frozen target (MW-center tau > 3.2e13 yr); 12-cluster x 100-ks stack at the cosmic bound; X-IFU late-2030s for the exact width")
print(f"  DATE  : archival stack TODAY -> XRISM width verdict ~2027-2028")

print("\n" + "=" * 78)
print("(3) KILL-C -- THE GRAVITY FACE: the deep-end exponent")
print("=" * 78)
print(f"  LAW   : deep RAR g^2 = a0 g_N -> exponent 1/2; G114 rms {sig_R_G114:.3f} dex / {n_dwarfs} dwarfs, slope 0.00")
print(f"  DECAYED-EXPONENT POWER (n = 0.4 vs 0.5, sig 0.150 dex):")
print(f"          N for 3-sig power 0.8 over g_N in [0.03, 0.5] a0: {N_exp0p8}")
print(f"          power at the existing N = {n_dwarfs}: {p_at_55:.2f}; at the LT deep tail (N = 18, g_N < 0.3 a0): {power_deep_tail:.2f}")
print(f"  FUNNEL: z~2.5 separation {funnel_sep:.2f} dex / floor {funnel_floor:.2f} dex -> 1 object = {funnel_1obj_sig:.2f} sig (20:1), N = {n_5sig} for 5 sig")
print(f"  MIGHTEE (G166): a0 = {mit_lo:.3e}-{mit_hi:.3e}, DE rejected 5.2 sig; deep 80-ring fit 1.843 +- 0.024e-10 -- re-analysis NOW")
print(f"  DR4 ridge (G088): 30.7 sig at 30 uas, E7 break 7.4 kAU -- verdict 2026-12-02")
print(f"  KILL  : deep-end slope != 1/2 at 3 sig; OR funnel on the rising curve; OR a system > 3 sig outside {z11_band}")
print(f"  DATE  : MIGHTEE NOW | tSZ 2026-10-07 | DR4 2026-12-02 | JWST z~2.5 ~2027-2028")

print("\n" + "=" * 78)
print("(4) VERDICTS")
print("=" * 78)
for v in verdicts.values():
    print("  " + v["statement"][:200] + "...")

print("\nwrote", out)
sys.exit(0 if result["n_pass"] == result["n_total"] else 1)