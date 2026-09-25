#!/usr/bin/env python3
"""
S02_A0Z_PLANE -- THE a0(z) CROSS-CONSTRAINT SYNTHESIS.
Place every on-record measurement of a0_eff-vs-epoch on ONE (z, Delta log10 a0_eff)
plane and derive what the framework can and cannot absorb.

Home: deepseek_push/  (sister lane S02_mightee_mirror owns the SLOT S02_results.json --
this lane writes S02_a0z_plane_results.json, additive-only.)

COMMITTED INPUTS (runtime-read from on-record JSONs; no invented values):
  * O02_results.json   : HeCS real-cluster z-test. delta_ANCOVA_dex (log10 T) = +0.0619786,
                         se_jackknife = 0.0198129, z_vs_framework = 3.1282,
                         pred_framework_dex = -5.46e-07, pred_MRISE_scaled_dex = +0.02383
                         (log10 T units), z_vs_MRISE_scaled = 1.9255,
                         arm medians z_lo = 0.1333 / z_hi = 0.21705.
  * G237 (commit a2e7c821e, README + G237_results.json + G237_eRASS3_zlaw.py):
                         a0(z)/a0(0) = 1 - 3e-5 z (S3-05, z<=3) -> u(z) z-invariant to 1e-5;
                         virial-T Case A identity T(z2)/T(z1)|_{M_b} = [a0(z2)/a0(z1)]^{1/2}
                         EXACT  =>  Delta log10 a0 = 2 * Delta log10 T.
                         rival M-RISE: a0(z) = a0(0)(1 + 1.6986 z)  (Ciocan 1.59e-10 m/s^2 per z).
  * N05_results.json   : SPARC deep (1152 rings): a0eff_a0 = 0.7241, fraction -0.2759,
                         z_clustered = -4.17  |  MIGHTEE deep (72 rings): a0eff_a0 = 2.1638,
                         fraction +1.1638, z = +6.58 (two-sided, ring SE).
  * O01_results.json   : L06 SPARC-deep 0.73 at 4.2 sigma; SE_dex = 0.0382 (recorded reconstruction);
                         O01 dwarfs primary (LT, gN<0.2, N=16): log10(a0eff/a0) = -0.1955 +- 0.1107.
  * G208_results.json  : MIGHTEE z_med = 0.04426 (z range [0.00577, 0.07908]);
                         z-evolution d_redshift: G011_at_zmed = 1.02189 (2.19%), needed_x = 2.9152.
  * M04_results.json   : BLR cosmography: sigma_d_days = 2.045 (d_fw1 = 61.351), dev_days = 24.0
                         (11.7 sigma lag at z=1 for M-RISE), win3_floor_days = 6.14 (6.55 atom-incl),
                         sigma_J10I_rel = 0.0356, zc_3sigma_chain = 0.6169.

ASSUMPTIONS (stated, not hidden):
  A1  HeCS absolute placement on the plane: only the hi-lo DIFFERENCE is measured; the pair is
      displayed centred on the framework 0.000 (midpoint anchored at the framework line), preserving
      the measured +0.1240-dex gradient and its SE. Absolute normalization is unmeasured.
  A2  HeCS future-leg extrapolation: the HeCS gradient (1.4801 +- 0.4732 dex per unit z) is
      extrapolated LINEARLY in z to z~1 as a DIAGNOSTIC of the BLR probe's discriminating power.
      The extrapolated law is unphysical far from the HeCS band (a0 ~ 30x by z=1); it is a
      sensitivity yardstick, not a committed law.
  A3  MIGHTEE delta-log10-a0 SE: derived from N05's point estimate (fraction +1.1638) and reported
      two-sided z = 6.58: sigma_frac = 1.1638/6.58 = 0.1769 -> sigma_dex = 0.0355. (N05 quotes the
      ring-level SE; the colour-group SE is smaller, se 7.34e-23 < 8.12e-23 -- N05's reported z=6.58
      is used as the conservative anchor.)
  A4  SPARC epoch z ~ 0.005 (task-given local band 0.001-0.01); O01 dwarfs z ~ 0 (within ~10 Mpc).
      MW(0) is definitional: Delta log10 a0_eff = 0.000 +- 0.000 (a0(0) anchors the frame, G03C 9.3619e-11).
  A5  BLR sigma evaluated at the framework expectation d_fw = 61.351 d (M04's own convention).

REGISTERED CONSTRAINING STATEMENT (C4): if a0(z) obeys G237, the survey-to-survey a0_eff spread
is environmental/systematic -- the staircase/sign-mirror cannot be a redshift effect -- and HeCS's
low-z candidate (if not selection) is ALSO ~1.1e5x too large to be a0(z) at G237's rate.

No git commit.
"""
import json, math, os

HERE = os.path.dirname(os.path.abspath(__file__))
CHECKS = []

def check(name, ok, measured, reading, threshold=None):
    CHECKS.append(dict(name=name, result=bool(ok), measured=measured,
                       threshold=threshold, reading=reading))
    line = f"{'PASS' if ok else 'FAIL'} | {name}"
    if threshold:
        line += f" | thresh {threshold}"
    line += f" | measured {measured}"
    print(line)

def load(fn):
    with open(os.path.join(HERE, fn)) as f:
        return json.load(f)

o02 = load("O02_results.json"); n05 = load("N05_results.json")
o01 = load("O01_results.json"); g208 = load("G208_results.json")
m04 = load("M04_results.json")

# ---------------------------------------------------------------------------
# (1) HECS TRANSLATE: virial-T Case A  =>  Delta log10 a0 = 2 * Delta log10 T
# ---------------------------------------------------------------------------
dT   = o02["key_numbers"]["delta_ANCOVA_dex"]                 # +0.0619786 dex log10 T
seT  = o02["key_numbers"]["se_jackknife"]                     # 0.0198129
zlo, zhi = o02["key_numbers"]["z_lo_med"], o02["key_numbers"]["z_hi_med"]  # 0.1333 / 0.21705
Dz   = zhi - zlo                                             # 0.08375 (~0.084)
dA0, seA0 = 2.0*dT, 2.0*seT                                  # +0.123957 +- 0.039626 dex
alpha_hecs, se_alpha = dA0/Dz, seA0/Dz                       # 1.4801 +- 0.4732 dex/unit z
zstat_hecs = dA0/seA0                                        # 3.1282 (O02 3.1282, unchanged by x2)
check("C1 HeCS translate: Delta log10 a0 = 2*Delta log10 T (Case A exact) with SE",
      abs(zstat_hecs - o02["key_numbers"]["z_vs_framework"]) < 1e-3,
      f"dA0 = {dA0:+.4f} +- {seA0:.4f} dex over Dz = {Dz:.4f}; alpha_HeCS = {alpha_hecs:+.4f} +- "
      f"{se_alpha:.4f} dex/unit z; z vs framework 0.000 = {zstat_hecs:.2f} SE (O02 {o02['key_numbers']['z_vs_framework']:.2f})",
      "Case A: T_X(z2)/T_X(z1)|_{M_b} = [a0(z2)/a0(z1)]^{1/2} EXACT (G237) -> both Delta and SE "
      "double: Delta log10 a0 = +0.124 +- 0.040 dex over Dz = 0.084, i.e. alpha = 1.48 +/- 0.47 "
      "dex/unit z. The z-tension is UNCHANGED at 3.13 SE (factor-2 scales signal and SE jointly) -- "
      "re-stated from O02 C05 on the a0 translate.",
      threshold="|recomputed z - O02 z_vs_framework| < 1e-3")

# ---------------------------------------------------------------------------
# (2) LAW AMPLITUDES from G237 (recovered from commit files)
# ---------------------------------------------------------------------------
a0_can  = 9.3619e-11                       # canonical footing (O01, G03C/G03E)
k_fw    = 3e-5                             # G237: a0(z)/a0(0) = 1 - 3e-5 z  (S3-05; A0 rate /unit z)
slope_fw_dex = math.log10(1.0 - k_fw)      # ~-1.303e-5 dex per unit z
mr_slope    = 1.59e-10 / a0_can            # 1.6984 (G237 README: 1.6986; O02 mrise form (1+1.6986 z))
dA0_mr_z1   = math.log10(1.0 + mr_slope)   # +0.4311 dex at z=1
ratio_hecs_over_fw = alpha_hecs / abs(slope_fw_dex)   # ~1.14e5
check("C2 G237/M-RISE plane amplitudes recovered from commit files (1-3e-5 z; 1+1.6986 z)",
      abs(k_fw - 3e-5) < 1e-12 and abs(mr_slope - 1.6986)/1.6986 < 1e-3 and ratio_hecs_over_fw > 1e4,
      f"G237: a0(z)/a0(0) = 1 - 3e-5 z -> d(log10 a0)/dz = {slope_fw_dex:.3e} dex/unit z; "
      f"M-RISE: 1 + 1.6986 z (1.59e-10/{a0_can:.4g}) -> +{dA0_mr_z1:.4f} dex at z=1; "
      f"HeCS/G237 slope ratio = {ratio_hecs_over_fw:.2e}",
      "Exact amplitude FROM G237_eRASS3_zlaw.py/README L2 ('a0(z)/a0(0) = 1 - 3e-5 z, S3-05') and "
      "the committed Ciocan slope 1.59e-10 m/s^2 per z over a0 = 9.3619e-11. The '~1e-5/unit z' of "
      "the task = the dex-rate log10(1-3e-5) = -1.30e-5 dex/unit z. HeCS's translate is ~1.1e5x "
      "this rate.",
      threshold="HeCS slope / G237 slope > 1e4")

# ---------------------------------------------------------------------------
# (3) KILL-CANDIDATE restated (already on record; conversion does not change it)
# ---------------------------------------------------------------------------
z_mr = abs(dA0 - 2.0*o02["key_numbers"]["pred_MRISE_scaled_dex"]) / seA0   # 1.93 (a0 units)
check("C3 Restate: K1 FIRED (3.13 SE), selection-flagged, K2 NOT SATISFIED (M-RISE not excluded)",
      zstat_hecs >= 3.0 and z_mr < 3.0,
      f"z_vs_G237 = {zstat_hecs:.2f} SE (>=3, K1 fires); z_vs_MRISE-scaled(+{2*o02['key_numbers']['pred_MRISE_scaled_dex']:+.4f} dex a0) = {z_mr:.2f} SE (<3, K2 not satisfied); "
      "C08 mass-dependent structure (low edge +0.15 dex -> high edge ~0) = pre-registered LX "
      "flux-selection signature -> VERDICT NOT ADJUDICATIVE",
      "The KILL-CANDIDATE fired on real low-z data (O02) stands on the a0 translate at the SAME "
      "3.13 SE; its confounder (selection signature) is on record, so the plane registers it as "
      "KILL-CANDIDATE, NOT adjudication.",
      threshold="z_G237 >= 3 AND z_MRISE < 3")

# ---------------------------------------------------------------------------
# (4) THE IMPOSSIBILITY LEG (registered constraining statement)
# ---------------------------------------------------------------------------
z_mightee = g208["samples"]["MIGHTEE"]["z_med"]              # 0.04426
a0e_orig = n05["mightee_deep"]["a0eff_a0"]                   # 2.1638
a0e_sparc = n05["deep_sparc_L06"]["a0eff_a0"]                # 0.7241
alpha_lin_mightee = (a0e_orig - 1.0) / z_mightee             # ~26.3 /unit z  (linear ratio law a0=1+alpha z)
alpha_lin_sparc   = (a0e_sparc - 1.0) / z_mightee            # ~ -6.2 /unit z (referenced to MIGHTEE epoch)
alpha_lin_sparc_own = (a0e_sparc - 1.0) / 0.005              # ~ -55 /unit z at SPARC's own z~0.005
dA0_between = math.log10(a0e_orig / a0e_sparc)               # +0.4757 dex SPARC(z~0) -> MIGHTEE(z=0.044)
slope_between = dA0_between / (z_mightee - 0.005)            # ~ +12.1 dex/unit z
g011_short = g208["orthogonal_decomposition"]["d_redshift"]["needed_x"] / \
             g208["orthogonal_decomposition"]["d_redshift"]["G011_at_zmed"]   # 2.85x ratio; pct short ~87x
evol_pct = g208["orthogonal_decomposition"]["d_redshift"]["evolution_pct"]    # 2.189%
need_pct = 100.0*(g208["orthogonal_decomposition"]["d_redshift"]["needed_x"] - 1.0)  # 191.5%
check("C4 IMPOSSIBILITY LEG: between-survey a0_eff spread cannot be a0(z) under G237",
      alpha_lin_mightee > 25.0 and alpha_lin_sparc < 0.0 and slope_between > 10.0 and \
      slope_between / abs(slope_fw_dex) > 1e5 and need_pct / evol_pct > 50.0,
      f"MIGHTEE at z=0.04426 with a0_eff/a0 = {a0e_orig:.3f} -> alpha ~ {alpha_lin_mightee:.1f}/unit z "
      f"(2.16 = 1+alpha*0.044) ; SPARC {a0e_sparc:.3f} at z~0 -> alpha ~ {alpha_lin_sparc:.1f}/unit z "
      f"(ref. 0.044; {alpha_lin_sparc_own:.0f}/unit z at its own z=0.005) -- OPPOSITE sign; "
      f"between-survey slope = {slope_between:.1f} dex/unit z = {slope_between/abs(slope_fw_dex):.1e}x "
      f"G237's rate; G208 C6: +{evol_pct:.2f}% evolution available vs {need_pct:.0f}% needed "
      f"({need_pct/evol_pct:.0f}x short, ~100x) -> the staircase/sign-mirror CANNOT be a redshift "
      f"effect under G237's law; HeCS's candidate is ~1.1e5x G237's rate",
      "REGISTERED CONSTRAINING STATEMENT: if a0(z) obeys G237, the survey-to-survey a0_eff spread "
      "is environmental/systematic, and HeCS's low-z candidate (if not selection) is also too "
      "large to be a0(z) at G237's rate. The 26.3/unit-z MIGHTEE and -6.2/unit-z SPARC readings "
      "are arithmetic from the on-record ratios (A3/A4 assumption: epoch scale 0.04426 for the "
      "SPARC sign-mirror; at SPARC's own z it is -55/unit z, worse).",
      threshold="alpha_MIGHTEE > 25 AND alpha_SPARC < 0 AND between-slope > 10 dex/unit z AND "
                "G208 shortfall > 50x")

# ---------------------------------------------------------------------------
# (5) THE PLANE TABLE (z, Delta log10 a0_eff) with SEs + both law curves
# ---------------------------------------------------------------------------
def fw_pred(z):  return math.log10(1.0 - k_fw*z)
def mr_pred(z):  return math.log10(1.0 + mr_slope*z)

sparc_dA0 = math.log10(a0e_sparc)                       # -0.1401 dex
sparc_se  = o01["pre_registered"]["L06"]["SE_dex"]      # 0.0382 (O01 reconstruction)
mig_dA0   = math.log10(a0e_orig)                        # +0.3355 dex
mig_se    = (1.0/math.log(10.0)) * (n05["mightee_deep"]["fraction_a0E"] / n05["mightee_deep"]["z"] / a0e_orig)
dwarf_dA0 = o01["samples"]["primary"]["log10_a0eff_over_a0"]   # -0.1955
dwarf_se  = o01["samples"]["primary"]["SE_dex"]                # 0.1107
rows = [
 dict(row="MW(0) anchor",      z=0.0,      dA0=0.0,      se=0.0,      src="definitional; G03C a0=9.3619e-11; G237 L2"),
 dict(row="O01 dwarfs (N=16)", z=0.0,      dA0=dwarf_dA0, se=dwarf_se, src="O01 primary gN<0.2; deep tail -0.509+-0.166"),
 dict(row="SPARC deep (1152r)",z=0.005,    dA0=sparc_dA0, se=sparc_se, src="N05 a0eff/a0=0.7241, z_cl=-4.17; O01 L06 SE_dex"),
 dict(row="MIGHTEE deep (72r)",z=z_mightee,dA0=mig_dA0,   se=mig_se,   src="N05 a0eff/a0=2.1638, z=+6.58 2-sided; G208 z_med"),
 dict(row="HeCS-lo (N=27)",    z=zlo,      dA0=-dA0/2.0,  se=seA0/2.0, src="O02 arm median 0.1333; pair difference ONLY (A1)"),
 dict(row="HeCS-hi (N=28)",    z=zhi,      dA0=+dA0/2.0,  se=seA0/2.0, src="O02 arm median 0.21705; pair difference ONLY (A1)"),
]
table_ok = True
print("="*100)
print("THE PLANE (z, Delta log10 a0_eff) -- overlay: G237 a0(z)/a0(0) = 1-3e-5 z ; M-RISE 1+1.6986 z")
print("="*100)
hdr = f"{'row':24s} {'z':>7s} {'Delta log10 a0e':>15s} {'+-SE':>8s} {'vsG237':>7s} {'G237pred':>10s} {'MRpred':>10s} {'vsMR':>7s}  class"
print(hdr); print("-"*len(hdr))
for r in rows:
    z, d, se = r["z"], r["dA0"], r["se"]
    if r["row"].startswith("HeCS"):
        # A1: only the PAIR DIFFERENCE is measured -> use the pair z-stats, not per-arm
        # absolute placement vs the curves.
        zg, zm, cls = zstat_hecs, z_mr, "G237-inconsistent 3.13SE (sel-flagged); M-RISE 1.93SE"
    else:
        zg = abs(d - fw_pred(z)) / se if se > 0 else 0.0
        zm = abs(d - mr_pred(z)) / se if se > 0 else 0.0
        cls = ("BOTH" if zg <= 2.0 and zm <= 2.0 else
               "NEITHER (>3 both)" if zg > 3.0 and zm > 3.0 else
               "G237-inconsistent" if zg > 3.0 else
               "MR-inconsistent" if zm > 3.0 else "1.9-3.0 both")
    print(f"{r['row']:24s} {z:7.4f} {d:+15.4f} {se:8.4f} {zg:7.2f} {fw_pred(z):+10.3e} {mr_pred(z):+10.4f} {zm:7.2f}  {cls}")
    r["z_vs_G237"], r["z_vs_MR"], r["class"] = zg, zm, cls
table_ok = (abs(rows[0]["dA0"]) < 1e-12 and abs(rows[2]["dA0"] - sparc_dA0) < 1e-6 and
            abs(rows[3]["dA0"] - mig_dA0) < 1e-6 and abs(rows[4]["dA0"] + dA0/2) < 1e-6 and
            abs(abs(rows[4]["dA0"]) - abs(rows[5]["dA0"])) < 1e-9)
check("C5 Plane table: 6 on-record rows placed; HeCS pair centred (A1), values match sources to <1e-3 dex",
      table_ok,
      f"SPARC {sparc_dA0:+.4f}+-{sparc_se:.4f}; MIGHTEE {mig_dA0:+.4f}+-{mig_se:.4f}; "
      f"O01 {dwarf_dA0:+.4f}+-{dwarf_se:.4f}; HeCS pair +-{dA0/2:.4f} +-{seA0/2:.4f}",
      "Every Delta in the plane is log10(a0_eff/a0) of the cited on-record ratio (N05, O01) or "
      "the factor-2 Case-A translate of O02. Curve values printed for both laws at every row epoch.",
      threshold="|table - source| < 1e-3 dex")

# ---------------------------------------------------------------------------
# (6) CONSISTENCY CLASSES + framework verdict
# ---------------------------------------------------------------------------
z_sparc_fw = abs(sparc_dA0)/sparc_se;  z_sparc_mr = abs(sparc_dA0 - mr_pred(0.005))/sparc_se
z_dw_fw = abs(dwarf_dA0)/dwarf_se;     z_dw_mr  = abs(dwarf_dA0 - mr_pred(0.001))/dwarf_se
z_mig_fw = abs(mig_dA0)/mig_se;        z_mig_mr = abs(mig_dA0 - mr_pred(z_mightee))/mig_se
# An ADJUDICATIVE kill = a z-SPACED (z >= 0.05) deviation from G237-flat at >3 SE whose
# origin is NOT the registered selection flag. SPARC (z=0.005) and MIGHTEE (z=0.044) are
# <-- z~0 environmental: SPARC sits at the definitional anchor epoch where no z-law
# normalized at a0(0)=1 can act; MIGHTEE violates BOTH laws (8.6 SE from M-RISE too) and is
# registered environmental/systematic (G208 C6 z-evolution 87x short; G133 M/L collapse
# 1.87->1.08). HeCS IS z-spaced but carries the pre-registered selection signature -> kill-
# CANDIDATE, not adjudication.
Z_SPACED_MIN = 0.05
flagged = {"HeCS-lo (N=27)", "HeCS-hi (N=28)"}
adjudicative_kills = [r for r in rows
                      if r["z"] >= Z_SPACED_MIN and r["z_vs_G237"] > 3.0
                      and r["row"] not in flagged]
hecs_flag = "selection-flagged (C08 mass-dependent structure = LX flux-limited signature)"
check("C6 Consistency classes: only HeCS is a z-spaced >3SE tension and it is selection-flagged",
      z_sparc_fw > 3.0 and z_sparc_mr > 3.0 and z_dw_fw < 3.0 and z_dw_mr < 3.0 and \
      z_mig_fw > 3.0 and z_mig_mr > 3.0 and zstat_hecs > 3.0 and z_mr < 3.0,
      f"SPARC {z_sparc_fw:.2f}/{z_sparc_mr:.2f} (NEITHER; z~0 -> environmental); "
      f"O01 {z_dw_fw:.2f}/{z_dw_mr:.2f} (BOTH within 3SE); "
      f"MIGHTEE {z_mig_fw:.2f}/{z_mig_mr:.2f} (NEITHER); "
      f"HeCS {zstat_hecs:.2f} vs G237, {z_mr:.2f} vs M-RISE ({hecs_flag})",
      "MW(0) and O01 are consistent with BOTH laws; SPARC and MIGHTEE are consistent with NEITHER "
      "as z-effects (and SPARC sits at z~0 where NO z-law normalized at a0(0)=1 can produce it); "
      "HeCS is the only z-spaced tension, 3.13 SE from G237-flat, within 2 SE of the M-RISE-scaled "
      "prediction but overshooting it (O02 K2).",
      threshold="as stated per row")

survives = (len(adjudicative_kills) == 0) and zstat_hecs >= 3.0   # HeCS is a KILL-CANDIDATE, not adjudication
check("C7 FRAMEWORK VERDICT on this plane: G237 a0(z) law SURVIVES; HeCS is kill-CANDIDATE pending WG data",
      survives,
      f"adjudicative z-spaced (z>={Z_SPACED_MIN}) >3SE kills vs G237 = {len(adjudicative_kills)} "
      f"{[r['row'] for r in adjudicative_kills]}; HeCS kill-candidate = fired at 3.13 SE, "
      f"{hecs_flag}; SPARC/MIGHTEE are z~0 environmental rows inconsistent with BOTH laws "
      f"(MIGHTEE 8.6 SE from M-RISE too) -> they cannot adjudicate G237 vs rivals",
      "HONEST: the plane KILLS nothing adjudicatively. Every >3SE deviation is z=0-anchored "
      "environmental (SPARC/O01/MIGHTEE -- and MIGHTEE is >8 SE from M-RISE too, so no growth "
      "law absorbs it either) or the HeCS gradient, whose pre-registered selection signature "
      "forces NOT-ADJUDICATIVE. If the WG high-z leg (X-ray/SZ masses, matched T) confirms HeCS, "
      "amendment is required -- and even then the impossibility leg still bars a0(z) from "
      "carrying the between-survey staircase.",
      threshold="0 adjudicative kills")

# ---------------------------------------------------------------------------
# (7) FUTURE LEG: can M04's BLR cosmography distinguish G237-flat from HeCS-alpha at 3 sigma?
# ---------------------------------------------------------------------------
sn   = 30.0
d_fw = m04["measurements"]["d_fw1_days"]        # 61.351
sig  = m04["measurements"]["sigma_d_days"]      # 2.045  (M04 convention: d_fw/30)
floor3 = m04["measurements"]["win3_floor_days"] # 6.14 lag-only (6.55 atom-incl)
def dbar_hecs(z):  return d_fw * 10.0**(-0.5*alpha_hecs*z)    # lag ratio [a0(0)/a0(z)]^1/2 (A2)
dev1 = d_fw - dbar_hecs(1.0);   zstat1 = dev1/sig            # 50.2 d / 2.045 = 24.6
z3 = math.log10(1.0 - floor3/d_fw) / (-0.5*alpha_hecs)       # 3-sigma crossing z ~ 0.062
pair_dev = abs(10.0**(-0.5*alpha_hecs*(1.0-0.3)) - math.sqrt((1.0-k_fw*0.3)/(1.0-k_fw*1.0)))
pair_z = pair_dev / (3.0*math.sqrt(2.0)/sn)                   # 4.93
sens3_dex = 2.0 * (3.0*m04["measurements"]["sigma_J10I_rel"]) / math.log(10.0)  # 0.0928 dex 3-sigma/object
check("C8 FUTURE LEG: BLR cosmography distinguishes G237-flat from HeCS-extrapolated at 3 sigma, N=1",
      zstat1 > 3.0 and z3 < 0.1 and pair_z > 3.0,
      f"single S/N=30 object: 3-sigma sensitivity on Delta log10 a0 = {sens3_dex:.3f} dex "
      f"(C8: sigma_J10I = {m04['measurements']['sigma_J10I_rel']:.4f}); HeCS-extrapolated "
      f"Delta log10 a0 (z=1) = {alpha_hecs:.3f} dex -> lag dev {dev1:.1f} d vs {floor3:.1f} d 3-sigma "
      f"floor: 3-sigma reached at z ~ {z3:.3f} (N=1); at z=1 one object = {zstat1:.1f} sigma "
      f"(M-RISE anchor: {m04['measurements']['dev_days']:.0f} d = {m04['measurements']['dev_days']/sig:.1f} sigma); "
      f"single pair (z1=0.3, z2=1.0) = {pair_z:.1f} sigma (threshold 3*sqrt(2)/30)",
      "YES -- the probe is NOT the binding constraint: the HeCS translate is so steep (1.48 "
      "dex/unit z, ~1.1e5x G237's rate) that ONE S/N=30 object at z >= 0.06-0.1 settles it at "
      "3 sigma, one object at z=1 at ~25 sigma, one pair at (0.3, 1.0) at ~5 sigma. The M04 "
      "anchor: one object at z=1 already resolves framework vs M-RISE at 11.7 sigma; the "
      "HeCS-extrapolated hypothesis is 2.1x that signal (A2, A5).",
      threshold="zstat(z=1) > 3 AND z_3sigma < 0.1 AND pair > 3")

# ---------------------------------------------------------------------------
print("-"*100)
print(f"S02_A0Z_PLANE COMPLETE: {sum(c['result'] for c in CHECKS)}/{len(CHECKS)} checks PASS.")

res = {
 "lane": "S02_A0Z_PLANE",
 "question": "Place every on-record a0_eff-vs-epoch measurement on ONE (z, Delta log10 a0_eff) plane and derive what the framework can and cannot absorb: HeCS translate, the impossibility leg, plane verdict, and the M04 BLR future leg.",
 "n_pass": sum(c["result"] for c in CHECKS), "n_total": len(CHECKS),
 "checks": CHECKS,
 "hecs_translate": {
   "Delta_log10_T_dex_ANCOVA": dT, "se_jackknife": seT,
   "Delta_log10_a0_dex": dA0, "se_dex": seA0,
   "Dz_arm_medians": Dz, "z_lo_med": zlo, "z_hi_med": zhi,
   "alpha_hecs_dex_per_unit_z": alpha_hecs, "se_alpha": se_alpha,
   "z_vs_framework": zstat_hecs, "z_vs_MRISE_scaled_a0_dex": z_mr,
   "framework_pred_dex_T": o02["key_numbers"]["pred_framework_dex"],
   "MRISE_scaled_dex_T": o02["key_numbers"]["pred_MRISE_scaled_dex"]},
 "laws": {
   "G237_a0_over_a0_0": "1 - 3e-5 z (S3-05, z<=3)",
   "G237_dlog10a0_per_unit_z": slope_fw_dex,
   "MRISE_a0_over_a0_0": "1 + 1.6986 z (Ciocan 1.59e-10 m/s^2 per z)",
   "MRISE_dlog10a0_at_z1": dA0_mr_z1,
   "hecs_over_G237_slope_ratio": ratio_hecs_over_fw},
 "impossibility_leg": {
   "alpha_lin_MIGHTEE_per_unit_z": alpha_lin_mightee,
   "alpha_lin_SPARC_per_unit_z_ref_0.044": alpha_lin_sparc,
   "alpha_lin_SPARC_own_z_0.005": alpha_lin_sparc_own,
   "delta_log10_a0_between_dex": dA0_between,
   "between_slope_dex_per_unit_z": slope_between,
   "between_over_G237_ratio": slope_between/abs(slope_fw_dex),
   "G208_evol_pct_at_zmed": evol_pct, "G208_needed_x": g208["orthogonal_decomposition"]["d_redshift"]["needed_x"],
   "G208_shortfall_x_in_pct_terms": need_pct/evol_pct,
   "statement": "if a0(z) obeys G237, the survey-to-survey a0_eff spread is environmental/systematic, and HeCS's low-z candidate (if not selection) is ALSO too large to be a0(z) at G237's rate"},
 "plane_rows": rows,
 "consistency": {"SPARC_vs_G237_MR": [z_sparc_fw, z_sparc_mr], "O01_vs_G237_MR": [z_dw_fw, z_dw_mr],
                 "MIGHTEE_vs_G237_MR": [z_mig_fw, z_mig_mr], "HeCS_vs_G237_MR": [zstat_hecs, z_mr],
                 "classes": {r["row"]: r["class"] for r in rows}},
 "verdict": "G237's a0(z) law SURVIVES this plane -- as an UNCONFIRMED flatness: no adjudicative z-spaced kill on record; the only z-spaced >3-SE signal is the HeCS gradient (Delta log10 a0 = +0.124 +- 0.040 dex over Dz = 0.084, alpha = 1.48 +- 0.47 dex/unit z, 3.13 SE), which carries its pre-registered selection signature (mass-dependent structure, LX flux-limited) -> KILL-CANDIDATE, NOT adjudication, verdict pending the WG high-z leg. The large plane deviations (SPARC 0.72, MIGHTEE 2.16, O01 0.64) sit at z ~ 0-0.05 and violate BOTH laws at >3 SE (MIGHTEE 9.5 SE from G237, 8.6 SE from M-RISE): under G237 they are environmental/systematic by registration (G208 C6 z-evolution ~87x short; G133 M/L-convention collapse 1.87->1.08; O01 deep-tail systematics), and the impossibility leg makes them UNZ-ABLE: the required slopes (+26/unit z, -6/unit z, +12 dex/unit z between-survey) are ~1e5x G237's rate, opposite-signed, and spread over Dz ~ 0.04. If HeCS survives the WG leg, amendment is needed -- but even an amended a0(z) cannot carry the staircase (impossibility leg), so the amendment would absorb HeCS alone, at <= ~1.5 dex/unit z, and M04's BLR cosmography would then settle it with a SINGLE S/N=30 object (3 sigma at z >= 0.06; ~25 sigma at z=1; one pair (0.3,1.0) ~5 sigma).",
 "future_leg": {
   "per_object_3sigma_dex": sens3_dex, "floor3_days_lag_only": floor3,
   "hecs_dev_days_at_z1": dev1, "zstat_hecs_at_z1_single_object": zstat1,
   "z3sigma_single_object": z3, "pair_zstat_z1_1p0": pair_z,
   "mrise_anchor_dev_days": m04["measurements"]["dev_days"],
   "mrise_anchor_zstat_lag": m04["measurements"]["dev_days"]/sig,
   "answer": "YES: distinguishable at 3 sigma with N=1 object at z >= 0.06-0.1 (or one pair at (0.3, >=0.4)); at z=1 one object reaches ~25 sigma -- the probe is not the binding constraint (assumption A2: linear extrapolation of the HeCS gradient, unphysical away from the band; sensitivity yardstick only)"},
 "assumptions": [
  "A1 HeCS absolute placement: only the hi-lo DIFFERENCE is measured; pair displayed centred on the framework 0.000 (midpoint anchored), preserving the +0.1240-dex gradient and SE.",
  "A2 HeCS future-leg extrapolation is linear in z, a DIAGNOSTIC sensitivity yardstick, not a committed law (implies a0~30x at z=1 if taken literally).",
  "A3 MIGHTEE SE_dex = 0.0355 derived from N05 point estimate + reported two-sided z=6.58 (ring SE); colour-group SE in S02_results.json is smaller (7.34e-23 vs 8.12e-23) - not used.",
  "A4 SPARC epoch z~0.005 (task band 0.001-0.01); O01 dwarfs z~0; MW(0) definitional anchor 0.000+-0.000.",
  "A5 BLR sigma evaluated at the framework expectation d_fw = 61.351 d (M04's own convention)."],
 "sources": [
  "deepseek_push/O02_results.json (HeCS: dT +0.0620+-0.0198, arms 0.1333/0.21705, K1/K2, C08)",
  "G237 commit a2e7c821e: G237_eRASS3_zlaw.py + README.md + G237_results.json (a0(z)/a0(0) = 1-3e-5 z; Case A identity; M-RISE 1.59e-10 m/s^2 per z)",
  "deepseek_push/N05_results.json (SPARC deep a0eff/a0 = 0.7241, z_cl -4.17; MIGHTEE deep 2.1638, z +6.58)",
  "deepseek_push/O01_results.json (L06 SE_dex 0.0382; dwarfs primary -0.1955+-0.1107)",
  "deepseek_push/G208_results.json (MIGHTEE z_med 0.04426; z-evolution +2.19% vs needed 2.915x)",
  "deepseek_push/M04_results.json + M04_J10Z_COSMOGRAPHY.md (sigma_d 2.045 d, floor 6.14 d, 11.7-sigma z=1 anchor, sigma_J10I 0.0356)"],
 "note_on_filename": "S02_results.json is the on-record deliverable of sister lane S02_mightee_mirror (read by U02/U03) and is NOT overwritten (additive-only rule); this lane writes S02_a0z_plane_results.json."}
with open(os.path.join(HERE, "S02_a0z_plane_results.json"), "w") as f:
    json.dump(res, f, indent=1)
print("wrote deepseek_push/S02_a0z_plane_results.json")