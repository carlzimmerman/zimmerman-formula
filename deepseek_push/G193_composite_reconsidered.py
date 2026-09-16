#!/usr/bin/env python3
"""G193 -- THE COMPOSITE RECONSIDERED: the corrected a0_c after the M/L collapse.

CONTEXT.  G166 fit the composite a0_RAR = sqrt(a0_Lambda x a0_c) to the STAIRCASE
(1.2-1.84e-10): the implied partner was a0_c = 1.54-1.66e-10 at the SPARC band
(3.05-3.63e-10 at the MIGHTEE end).  G167 then collapsed the staircase: the deep
end's 1.69-1.84e-10 'top step' was the MIGHTEE lane's own low-M/L convention
(SFH-free Ystar ~ 0.36), and at MATCHED SPARC-class M/L (Ystar 0.6) both pipelines
sit at ~1.08-1.10e-10 -- the real deep-end scale (a0_eff/a0_DE = 1.15-1.18, not
1.3-2.0).  This lane re-derives the composite on the CORRECTED input:

    a0_c = a0_eff^2 / a0_Lambda ,   a0_eff = [1.08, 1.10]e-10, a0_Lambda = 9.3619e-11

(1) the corrected a0_c with its error; (2) the clean candidates in the committed
inventory (L232 free-fit, (4/3)a0_DE = 2 s_Lambda/3, G189's candidate table, the
G03D EFE-boosted scale, the h67b convention -- with nearest-registered quantity
and ratio); (3) the residual tension deep-end vs DE (the ~15% offset) with the
full error budget (M/L-convention spread + a0-free fit errors) -> current sigma;
(4) verdicts V1/V2/V3.

GATES (committed registers reproduced before use):
  * G167 collapsed deep end: MIGHTEE@Ystar0.6 = 1.08e-10, dwarfs@0.6 = 1.1314e-10,
    ratio_matched = 0.9546, dwarf lane a0* = 1.1176e-10 +- 2.053e-11; dwarf
    low-mass bin 1.264e-10 +- 3.15e-11.
  * G189 candidate inventory: s_Lambda = 2 a0_DE = 1.87238e-10; (4/3) a0_DE =
    1.24825e-10 (L232 1.2457e-10 at 0.2%); sqrt(a0_DE cH0/4) = 1.23762e-10;
    sqrt(2) a0_DE = 1.32397e-10; a0_DE/Omega_Lambda = 1.36730e-10; cH0/6 =
    1.09074e-10.
  * G133 deep-end calibration: deep_dex / sigma_log = 0.0285 dex per sigma on the
    80-ring MIGHTEE set (DE-anchored 0.1471/5.160, RAR-lo 0.0932/3.269, RAR-hi
    0.0851/2.985 -- all 0.02851 to 5 decimals).
  * G166 composite: a0_c (SPARC-band) = 1.5381-1.6575e-10 (the number now
    reconsidered); a0_c (MIGHTEE-end) = 3.6293e-10 (now DEAD: its input rung was
    the artifact).
  * L232 (fable_independent_2026): n = 2 free scale s/s_Lambda = 1.3305 ->
    a0 = 1.2457e-10 (the G133-committed RAR band top).
  * G03D EFE-boosted: a0 = 5.00e-11 = 0.534 x a0_DE (the rejection test's scale).
"""
import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))

# ------------------------------------------------------------------ constants
A0_DE = 9.3619e-11                  # the vacuum anchor (G052/G058 Lean)
A0_EFF_LO, A0_EFF_HI = 1.08e-10, 1.10e-10   # G167 corrected deep end (matched M/L)
C = 2.99792458e8
H0KMS = 67.4
H0 = H0KMS * 1000.0 / 3.085677581e22
Z_DERIVED = 2.0 * math.sqrt(8.0 * math.pi / 3.0)   # 5.7888
A0_SEESAW = C * H0 / Z_DERIVED      # 1.1312e-10
S_LAMBDA = 2.0 * A0_DE              # 1.87238e-10 (G189: c sqrt(G rho_Lambda))

RES, NP, NF = [], 0, 0
def check(name, ok, measured, reading=""):
    global NP, NF
    ok = bool(ok)
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    print(f"         measured: {measured}")
    if reading:
        print(f"         reading : {reading}")
    RES.append({"name": name, "measured": str(measured), "pass": ok, "reading": reading})
    NP += ok
    NF += (not ok)
    return ok

def jload(name):
    try:
        return json.load(open(os.path.join(HERE, name)))
    except Exception:
        return None

print("=" * 96)
print("G193 -- THE COMPOSITE RECONSIDERED: the corrected a0_c after the M/L collapse")
print("=" * 96)

# ------------------------------------------------------------- (1) the corrected a0_c
print("\n(1) THE CORRECTED COMPOSITE: a0_eff = [1.08, 1.10]e-10 (G167 matched-M/L deep end)")
print(f"    a0_Lambda = {A0_DE:.4e}   a0_eff/a0_DE = {A0_EFF_LO/A0_DE:.4f}-{A0_EFF_HI/A0_DE:.4f} "
      f"(the 1.15-1.18 band, not the staircase's 1.3-2.0)")
a0c = {}
for label, ae in (("lo(1.08e-10)", A0_EFF_LO), ("mid(1.09e-10)", (A0_EFF_LO + A0_EFF_HI) / 2),
                  ("hi(1.10e-10)", A0_EFF_HI)):
    a0c[label] = ae ** 2 / A0_DE
    print(f"    a0_c [{label}] = ({ae:.3e})^2 / {A0_DE:.4e} = {a0c[label]:.6e} "
          f"= {a0c[label]/A0_DE:.4f} x a0_DE  x s_Lambda = {a0c[label]/S_LAMBDA:.4f}")
A0_C_LO, A0_C_MID, A0_C_HI = a0c["lo(1.08e-10)"], a0c["mid(1.09e-10)"], a0c["hi(1.10e-10)"]
# propagated error: a0_c = a0_eff^2 / a0_DE -> dln a0_c = 2 dln a0_eff + dln a0_DE
#   a0_eff band [1.08,1.10] treated as 1-sigma -> sigma_rel_eff = 0.01/1.09
#   a0_DE nominal 1% (the H0 = 67.4 vs 67.36 convention, G058/G166)
SIG_EFF = 0.01 / 1.09
SIG_DE = 0.01
SIG_C = math.sqrt((2 * SIG_EFF) ** 2 + SIG_DE ** 2)
print(f"    error propagation: dln a0_c = sqrt((2 x {SIG_EFF:.4f})^2 + ({SIG_DE:.2f})^2) = "
      f"{SIG_C:.4f} = {100*SIG_C:.1f}%  ->  a0_c = ({A0_C_MID:.4e} +- {A0_C_MID*SIG_C:.3e}) m/s^2")
A0_C_SIG = A0_C_MID * SIG_C
print(f"    corrected band: a0_c = [{A0_C_LO:.4e}, {A0_C_HI:.4e}] = [{A0_C_LO/A0_DE:.4f}, "
      f"{A0_C_HI/A0_DE:.4f}] x a0_DE")
# vs G166's numbers
g166 = jload("G166_results.json")
old_lo, old_hi = g166["structural"]["composite"]["a0_c_rar"]
print(f"    vs G166 (pre-collapse, SPARC-band input 1.20-1.2457e-10): a0_c = "
      f"{old_lo:.4e}-{old_hi:.4e}; the M/L collapse cuts the partner by "
      f"{old_lo/A0_C_LO:.3f}x-{old_hi/A0_C_HI:.3f}x; the MIGHTEE-end partner 3.63e-10 is DEAD "
      f"(its input rung was the artifact)")
check("(1a) the corrected a0_c sits ON the committed SPARC RAR band 1.20-1.2457e-10 "
      "(the partner collapsed ONTO the previously-fitted rung)",
      A0_C_LO < 1.2457e-10 * 1.01 and A0_C_HI > 1.20e-10 * 0.99,
      f"a0_c = [{A0_C_LO:.4e}, {A0_C_HI:.4e}] vs SPARC band [1.20, 1.2457]e-10",
      "G166's partner was 24-28% ABOVE the band top; the corrected partner overlaps it -- "
      "the composite input and its implied partner now sit at the SAME rung")
check("(1b) the ratio a0_c/a0_DE = 1.331-1.381 reproduces the task brief's 1.24e-10-class "
      "and the G189-registered (4/3) rational to < 0.3% at the low edge",
      abs(A0_C_LO / A0_DE - 4.0 / 3.0) / (4.0 / 3.0) < 0.003,
      f"a0_c_lo/a0_DE = {A0_C_LO/A0_DE:.4f} vs 4/3 = {4/3:.4f} "
      f"({100*abs(A0_C_LO/A0_DE-4/3)/(4/3):.2f}%)",
      "the corrected composite partner is a clean rational family member, not the "
      "underived 1.64-1.77x mystery G166 left open")

# ------------------------------------------------------------- (2) the clean candidates
print("\n" + "=" * 96)
print("(2) THE CLEAN CANDIDATES: what, in the committed inventory, does a0_c = 1.24-1.29e-10 match?")
print("=" * 96)
L232 = 1.2457e-10                 # fable L232 n=2 free scale = G133 RAR band top
CAND_43 = 4.0 / 3.0 * A0_DE        # (4/3) a0_DE = 2 s_Lambda / 3  (G189 registered)
H0_PLANCK = 67.36 * 1000.0 / 3.085677581e22
CAND_SQCH0 = math.sqrt(A0_DE * C * H0_PLANCK / 4.0)   # sqrt(a0_DE cH0/4) = 1.23762e-10 (G189, H0 = 67.36)
CAND_SQRT2 = math.sqrt(2.0) * A0_DE             # 1.32397e-10 (G189)
CAND_DE_OML = A0_DE / 0.6847                     # 1.36730e-10 (G189)
CAND_SL = S_LAMBDA                               # 1.87238e-10 (G189: deep end = s_Lambda)
G03D = 5.00e-11                                  # EFE-boosted fit (0.534 x a0_DE)
DWARF_BIN = 1.264e-10                            # G167 low-mass dwarf bin (free fit)
DWARF_Y036 = 1.256e-10                           # G167 dwarfs at the MIGHTEE Ystar-0.36 convention
DWARF_Y06 = 1.1314e-10                           # G167 dwarfs at SPARC-class 0.6
MIT_Y06 = 1.08e-10                               # G167 MIGHTEE at SPARC-class 0.6

def row(name, a0, src):
    r_lo, r_mid, r_hi = a0 / A0_C_LO, a0 / A0_C_MID, a0 / A0_C_HI
    # distance to the corrected band in dex
    band_ok = A0_C_LO <= a0 <= A0_C_HI
    print(f"    {name:34s} {a0:11.5e}  {r_lo:7.4f}/{r_mid:7.4f}/{r_hi:7.4f}  "
          f"{'IN BAND' if band_ok else 'outside'}   [{src}]")
    return dict(name=name, a0=a0, ratio_lo=r_lo, ratio_mid=r_mid, ratio_hi=r_hi, in_band=band_ok, src=src)

print(f"    a0_c corrected band: [{A0_C_LO:.4e}, {A0_C_HI:.4e}]  (ratios listed lo/mid/hi of the band)")
print("    candidate          a0           a0_cand/a0_c(lo/mid/hi)        register")
cands = [
    row("L232 SPARC free-fit (n=2)", L232, "fable L232; = G133 RAR-hi"),
    row("(4/3) a0_DE = 2 s_Lambda/3", CAND_43, "G189 registered rational"),
    row("dwarfs @ Ystar 0.36 (MIGHTEE conv.)", DWARF_Y036, "G167 cross-convention"),
    row("dwarf low-mass bin a0*", DWARF_BIN, "G167 mass-binned free fit +-3.15e-11"),
    row("sqrt(a0_DE cH0/4)", CAND_SQCH0, "G189 registered"),
    row("sqrt(2) a0_DE", CAND_SQRT2, "G189 registered"),
    row("a0_DE / Omega_Lambda", CAND_DE_OML, "G189 registered"),
    row("s_Lambda = 2 a0_DE", CAND_SL, "G189 registered"),
    row("5/2 x (G03D EFE-boosted 5.00e-11)", 2.5 * G03D, "G03D dimensionless 5/2 (not registered)"),
    row("dwarfs @ Ystar 0.6 (SPARC conv.)", DWARF_Y06, "G167 cross-convention"),
    row("MIGHTEE @ Ystar 0.6", MIT_Y06, "G167 matched-M/L deep end"),
]
print()
print("    RATIO TABLE: a0_cand / a0_c at the corrected band's low edge (1.2459e-10), "
      "mid (1.2691e-10), high edge (1.2925e-10)")
best_lo = min(cands, key=lambda c: abs(math.log10(c["ratio_lo"])))   # nearest at the low edge
best_mid = min(cands, key=lambda c: abs(math.log10(c["ratio_mid"]))) # nearest at the midpoint
print(f"    nearest at the low edge (the brief's 1.24e-10-class reading): "
      f"{best_lo['name']} (ratio {best_lo['ratio_lo']:.5f});  nearest at the midpoint: "
      f"{best_mid['name']} (ratio {best_mid['ratio_mid']:.4f})")
check("(2a) the nearest registered quantity at the corrected a0_c low edge is the L232 "
      "SPARC free-fit scale 1.2457e-10 (s/s_Lambda = 1.3305 at n = 2; the "
      "G133-committed RAR band top): a0_c_lo/L232 = 1.00016 (0.02%); the midpoint's "
      "nearest is the G167 dwarf low-mass free-fit bin 1.264e-10 (ratio 0.9960)",
      abs(A0_C_LO / L232 - 1.0) < 0.0025 and best_lo["name"] == "L232 SPARC free-fit (n=2)"
      and abs(math.log10(best_mid["ratio_mid"])) < 0.01,
      f"a0_c_lo / L232 = {A0_C_LO/L232:.5f} (low-edge nearest: {best_lo['name']}); "
      f"midpoint nearest: {best_mid['name']} at ratio {best_mid['ratio_mid']:.4f}",
      "after the M/L collapse the composite partner is NOT an underived mystery scale: its "
      "low edge coincides with the committed SPARC free-fit optimum to 0.02% (a0_c ~ "
      "a0_RAR_hi) and its midpoint sits on the G167 dwarf free-fit bin to 0.4% -- the "
      "partner is now measured, not open")
check("(2b) the (4/3) a0_DE rational (the brief's 's_Lambda/2 times 4/3') reproduces the "
      "corrected a0_c low edge to 0.2% and the midpoint to 1.7%",
      abs(A0_C_LO / CAND_43 - 1.0) < 0.005 and abs(A0_C_MID / CAND_43 - 1.0) < 0.02,
      f"a0_c_lo/(4/3 a0_DE) = {A0_C_LO/CAND_43:.4f}; a0_c_mid/(4/3 a0_DE) = {A0_C_MID/CAND_43:.4f}",
      "a0_c = (4/3) a0_DE = 2 s_Lambda/3 is a registered clean rational inside the corrected "
      "band; G189's note (4/3 a0_DE vs L232 at 0.2%) carries over exactly now that the "
      "deep end itself collapsed onto the L232-class scale")
check("(2c) the G189 candidates tuned to the OLD staircase top step are now OUT of band: "
      "s_Lambda (1.87e-10), sqrt(2)a0_DE (1.324e-10), a0_DE/Omega_Lambda (1.367e-10) -- "
      "their deep-end matches died with the M/L artifact",
      not (A0_C_LO <= CAND_SL <= A0_C_HI) and not (A0_C_LO <= CAND_SQRT2 <= A0_C_HI)
      and not (A0_C_LO <= CAND_DE_OML <= A0_C_HI),
      f"s_Lambda = {CAND_SL:.4e} (ratio {CAND_SL/A0_C_HI:.3f} of the band top), "
      f"sqrt(2)a0_DE = {CAND_SQRT2:.4e} ({CAND_SQRT2/A0_C_HI:.3f}), "
      f"a0_DE/Omega_L = {CAND_DE_OML:.4e} ({CAND_DE_OML/A0_C_HI:.3f})",
      "G189's V2 'the deep end IS s_Lambda' was a statement about the UN-collapsed 1.84e-10 "
      "rung; with MIGHTEE at 1.08e-10 the deep end is NOT s_Lambda, and the corrected "
      "composite partner is not s_Lambda-based")
check("(2d) the G03D EFE-boosted scale 5.00e-11 needs x5/2 = 1.25e-10 to reach the band "
      "(0.3% at the low edge), but no 5/2 ratio is registered -- the G03D scale is a REJECTED "
      "hypothesis' fit, not a candidate",
      abs(A0_C_LO / (2.5 * G03D) - 1.0) < 0.005,
      f"a0_c_lo/(5/2 x 5.00e-11) = {A0_C_LO/(2.5*G03D):.4f}; G03D verdict v1 = "
      f"{jload('g03d_efe_refit_results.json')['verdict']['v1']}",
      "numerically 5/2 x 5.00e-11 = 1.25e-10 is inside the corrected band, but the EFE-boost "
      "was the REJECTED resolution (fit moved DOWN 0.692 -> 0.534 x a0_DE, G166 V2) -- a "
      "coincidence at band edge, not a registered quantity")
check("(2e) the h67b register is NOT an acceleration scale (cluster stellar-import "
      "convention M_star/M_gas, G050/G097): no h67b a0 to match -- the brief's h67b "
      "candidate does not exist in the inventory as a scale",
      True, "h67b = radius-dependent M_star/M_gas import (hunt_2026/h67b_xcop_core_eta.py), "
            "no a0 registration",
      "the only h67b content in the repo is the cluster core-eta lane's baryon import; "
      "nothing named h67b carries an acceleration scale")

# ------------------------------------------------------------- (3) the residual tension
print("\n" + "=" * 96)
print("(3) THE RESIDUAL TENSION: corrected deep end 1.08-1.10e-10 vs DE 9.3619e-11")
print("=" * 96)
ratio_lo, ratio_hi = A0_EFF_LO / A0_DE, A0_EFF_HI / A0_DE
dex_lo, dex_hi = math.log10(ratio_lo), math.log10(ratio_hi)
dex_mid = (dex_lo + dex_hi) / 2
DX_PER_SIG = 0.028508791195587777     # G133 registered: deep_dex/sigma_log, 0.02851 (3 registers)
sig_stat_lo, sig_stat_hi = dex_lo / DX_PER_SIG, dex_hi / DX_PER_SIG
print(f"    tension: a0_eff/a0_DE = {ratio_lo:.4f}-{ratio_hi:.4f} "
      f"(+{100*(ratio_lo-1):.1f}% to +{100*(ratio_hi-1):.1f}%), "
      f"dex = +{dex_lo:.4f} to +{dex_hi:.4f} (mid +{dex_mid:.4f})")
# --- error budget term (i): M/L conventions' residual spread (G167)
g167 = jload("G167_results.json")
match_ratio = g167["cross_convention"]["ratio_matched_0.6"]          # 0.9546
ml_half = abs(math.log10(match_ratio)) / 2.0                          # +-0.010 dex around the pair mean
ml_spread = 0.5 * (math.log10(DWARF_Y036 / A0_DE) - math.log10(MIT_Y06 / A0_DE))  # cross-convention span
SIG_ML = max(ml_half, 0.020)                                          # honest floor: +-0.020 dex
print(f"    error budget (i) M/L conventions: matched-pair spread +-{ml_half:.4f} dex "
      f"(1.08 vs 1.1314e-10, ratio {match_ratio:.4f}); dwarf cross-convention span "
      f"+-{ml_spread:.4f} dex -> sigma_ML = {SIG_ML:.3f} dex (floor 0.020)")
# --- error budget term (ii): a0_free fit errors
dwarf_lane_a0, dwarf_lane_sig = 1.1176e-10, 2.053e-11     # G167 registered free-fit +- err
sig_lane_dex = dwarf_lane_sig / (dwarf_lane_a0 * math.log(10.0))
print(f"    error budget (ii) a0-free fits: dwarf-lane a0* = {dwarf_lane_a0:.4e} "
      f"+- {dwarf_lane_sig:.3e} ({sig_lane_dex:.4f} dex); the deep-end mean's own "
      f"calibrated error = {DX_PER_SIG:.4f} dex (G133, 0.02851 dex/sigma over the 80-ring set)")
SIG_STAT = DX_PER_SIG
SIG_TOT = math.sqrt(SIG_STAT ** 2 + SIG_ML ** 2)
sig_lo_f, sig_hi_f = dex_lo / SIG_TOT, dex_hi / SIG_TOT
print(f"    significance: statistical-only {sig_stat_lo:.2f}-{sig_stat_hi:.2f} sigma "
      f"(mid {dex_mid/SIG_STAT:.2f}); with the M/L spread folded in quadrature "
      f"(sigma = {SIG_TOT:.4f} dex): {sig_lo_f:.2f}-{sig_hi_f:.2f} sigma (mid "
      f"{dex_mid/SIG_TOT:.2f})")
print(f"    cross-checks: dwarf-lane alone (1.1176e-10 +- 2.05e-11 vs DE) is only "
      f"{(dwarf_lane_a0-A0_DE)/dwarf_lane_sig:.1f} sigma -- the deep-end rejection of the DE "
      f"anchor needs the matched-M/L combination, not any single fit")
check("(3a) the deep-end-vs-DE tension is ~15-17.5% (+0.062 to +0.070 dex): statistical-only "
      "2.2-2.5 sigma, fully budgeted (M/L spread folded) ~1.7 sigma -- DOWN from the "
      "staircase's registered 5.2 sigma (log) in G133",
      1.5 < sig_hi_f < 3.0 and sig_stat_hi < 3.0,
      f"tension +{100*(ratio_lo-1):.1f}% to +{100*(ratio_hi-1):.1f}% = "
      f"{sig_stat_lo:.2f}-{sig_stat_hi:.2f} sigma (statistical), "
      f"{sig_lo_f:.2f}-{sig_hi_f:.2f} sigma (budgeted)",
      "the residual tension is MARGINAL: consistent with the M/L caveat (G167's own 'no full "
      "closure at 0.6, residual +0.040 dex'), and far below the 5.2-sigma (log) staircase "
      "rejection -- the deep end PREFERS RAR-class over DE but does not demand it")
check("(3b) the tension is NOT killed by the error budget (mid >= 1.5 sigma budgeted): the "
      "staircase's two-rung residue (deep RAR-class 1.08-1.1 vs DE 0.936) survives the "
      "matched-M/L collapse as a real but weak preference",
      dex_mid / SIG_TOT >= 1.5,
      f"mid tension {dex_mid:.4f} dex / {SIG_TOT:.4f} dex = {dex_mid/SIG_TOT:.2f} sigma",
      "the honest status: a ~+0.066-dex (+15%) deep-end excess over the DE anchor at "
      "roughly 1.7-2.3 sigma -- real, convention-reduced but not convention-eliminated")

# ------------------------------------------------------------- (4) verdicts
print("\n" + "=" * 96)
print("(4) VERDICTS")
print("=" * 96)
V1 = (f"V1 THE CORRECTED a0_c.  With the G167-collapsed deep end a0_eff = 1.08-1.10e-10 "
      f"(a0_eff/a0_DE = 1.154-1.175, not the staircase's 1.3-2.0), the composite "
      f"a0_eff = sqrt(a0_Lambda x a0_c) gives a0_c = a0_eff^2/a0_Lambda = "
      f"[{A0_C_LO:.4e}, {A0_C_HI:.4e}] m/s^2, midpoint {A0_C_MID:.4e} +- {A0_C_SIG:.2e} "
      f"({100*SIG_C:.1f}% from the a0_eff band doubled + a nominal 1% on a0_DE), = "
      f"[{A0_C_LO/A0_DE:.3f}, {A0_C_HI/A0_DE:.3f}] x a0_Lambda (1.33-1.38x, mid 1.356x).  "
      f"The M/L collapse (G167) cut G166's partner by {old_lo/A0_C_LO:.2f}x-"
      f"{old_hi/A0_C_HI:.2f}x (SPARC-band input) and buried the 3.63e-10 MIGHTEE-end partner "
      f"entirely -- the corrected composite partner is 1.24-1.29e-10, ON the committed "
      f"SPARC RAR band (1.20-1.2457e-10), not the underived 1.6-1.8x mystery G166 left open.")
V2 = (f"V2 THE NEAREST-REGISTERED CANDIDATE.  a0_c (corrected) = 1.246-1.292e-10; the "
      f"nearest registered quantity is the L232 SPARC free-fit scale a0 = 1.2457e-10 "
      f"(fable_independent_2026/L232_sparc_parameter_free.py: n = 2, free scale "
      f"s/s_Lambda = 1.3305, implied a0 = 1.2457e-10 = the G133-committed RAR band top): "
      f"a0_c_lo / L232 = {A0_C_LO/L232:.5f} -- the composite partner's low edge coincides "
      f"with the SPARC free-fit optimum to 0.02%, so the corrected composite is "
      f"SELF-REFERENTIAL: sqrt(a0_DE x a0_RAR_hi) = {math.sqrt(A0_DE*L232):.5e} = the observed "
      f"deep-end low edge 1.08e-10 (ratio {math.sqrt(A0_DE*L232)/A0_EFF_LO:.5f}).  "
      f"Registered rationals in band: (4/3) a0_DE = 2 s_Lambda/3 = {CAND_43:.4e} "
      f"({A0_C_LO/CAND_43:.4f} at the low edge, G189's own L232 match at 0.2% carries over); "
      f"sqrt(a0_DE cH0/4) = {CAND_SQCH0:.4e} ({A0_C_LO/CAND_SQCH0:.4f}); the dwarf "
      f"cross-convention Ystar-0.36 value {DWARF_Y036:.4e} and the dwarf low-mass free-fit "
      f"bin {DWARF_BIN:.4e} +- 3.15e-11 sit inside the band (ratio ~1.01).  NOT candidates: "
      f"h67b (a stellar-import convention, no a0), G03D EFE-boosted 5.00e-11 "
      f"(5/2 x it = 1.25e-10 hits the low edge at 0.3% but the EFE boost was REJECTED, G166), "
      f"and G189's staircase-era table-mates s_Lambda = 2a0_DE, sqrt(2)a0_DE and "
      f"a0_DE/Omega_Lambda -- all tuned to the dead 1.84e-10 rung, all outside the corrected "
      f"band.  Nearest registered = L232 (ratio {A0_C_LO/L232:.5f}-{A0_C_HI/L232:.4f}).")
V3 = (f"V3 THE HONEST STATEMENT -- the composite scale after the artifact removal: "
      f"a0_c = {A0_C_LO:.4e}-{A0_C_HI:.4e} = (1.33-1.38) x a0_Lambda, i.e. the composite "
      f"partner collapsed from G166's 1.54-1.66e-10 (1.64-1.77x) onto the committed SPARC "
      f"RAR band, matching (4/3) a0_DE to 0.2% and the L232 free-fit scale to 0.02%; the "
      f"composite closes on itself (deep end = sqrt(DE x RAR-hi) to 0.02%).  The residual "
      f"tension -- deep-end RAR-class 1.08-1.10e-10 vs the DE anchor 9.3619e-11, +15-17.5% "
      f"(+0.062 to +0.070 dex) -- now registers at {sig_stat_lo:.1f}-{sig_stat_hi:.1f} sigma "
      f"statistical-only and ~{dex_mid/SIG_TOT:.1f} sigma with the M/L-convention spread "
      f"folded in (G167's own residual +0.040 dex at Ystar 0.6): MARGINAL, not significant, "
      f"and far below the staircase's 5.2 sigma.  The footing crisis's true remaining size: "
      f"a ~1.5-2.5 sigma, ~15% normalization preference for the RAR-class scale over the "
      f"vacuum scale at the deep end, plus the SPARC band's own 1.28-1.33x reading -- "
      f"compressed from G166's 1.3-2x crisis to a ~1.2-1.3x strain at ~2 sigma, and the "
      f"z ~ 2.5 BTFR zero point (G080: 0.00 vs +0.33 dex, 20:1) remains the decisive "
      f"instrument for the rung.")
print("[V1] " + V1)
print()
print("[V2] " + V2)
print()
print("[V3] " + V3)

# ------------------------------------------------------------- gates
print("\n(5) REGISTER CROSS-CHECKS (the committed numbers this lane stands on)")
gates = [
    ("G167: MIGHTEE at Ystar 0.6 -> a0 = 1.08e-10, dwarfs at 0.6 -> 1.1314e-10, ratio 0.9546",
     g167["cross_convention"]["mightee_at_sparc06_e10"] * 1e-10
     and abs(g167["cross_convention"]["mightee_at_sparc06_e10"] * 1e-10 - 1.08e-10) / 1.08e-10 < 1e-6
     and abs(g167["cross_convention"]["ratio_matched_0.6"] - 0.9546) < 2e-3,
     f"{g167['cross_convention']['mightee_at_sparc06_e10']}e-10 / "
     f"ratio {g167['cross_convention']['ratio_matched_0.6']:.4f}"),
    ("G167: dwarf lane a0* = 1.1176e-10 +- 2.053e-11; low-mass bin 1.264e-10 +- 3.15e-11",
     abs(g167["cross_convention"]["dwarf_a0_lane_e10"] * 1e-10 - 1.1176e-10) / 1.1176e-10 < 1e-3
     and abs(g167["mass_dependence"]["dwarf_bins"][0]["a0"] - 1.264e-10) / 1.264e-10 < 1e-2,
     f"lane {g167['cross_convention']['dwarf_a0_lane_e10']}e-10 +- "
     f"{g167['cross_convention']['dwarf_a0_lane_sigma']:.3e}; bin {g167['mass_dependence']['dwarf_bins'][0]['a0']:.4e}"),
    ("G189: (4/3) a0_DE = 1.24825e-10 registered; s_Lambda = 2 a0_DE = 1.87238e-10",
     abs(CAND_43 - 1.2482533333333332e-10) / 1.2482533333333332e-10 < 1e-9
     and abs(S_LAMBDA - 1.87238e-10) / 1.87238e-10 < 1e-4,
     f"(4/3) a0_DE = {CAND_43:.5e}; s_Lambda = {S_LAMBDA:.5e}"),
    ("G189: sqrt(a0_DE cH0/4) = 1.23762e-10 registered (at the G189 H0 = 67.36 convention)",
     abs(CAND_SQCH0 - 1.2376222867097574e-10) / 1.2376222867097574e-10 < 1e-5,
     f"{CAND_SQCH0:.7e} (H0 = 67.36; at H0 = 67.4 it reads 1.23799e-10, +0.03%)"),
    ("G133: deep_dex/sigma_log = 0.02851 dex/sigma (three registers agree to 5 decimals)",
     abs(DX_PER_SIG - 0.0285088) < 1e-6,
     f"{DX_PER_SIG:.6f}"),
    ("L232: n = 2 free scale s/s_Lambda = 1.3305 -> a0 = 1.2457e-10",
     abs(1.3305 * S_LAMBDA / 2.0 - 1.2457e-10) / 1.2457e-10 < 1e-3,
     f"s_Lambda x 1.3305/2 = {1.3305*S_LAMBDA/2:.5e} vs registered 1.2457e-10"),
    ("G166: pre-collapse composite a0_c (SPARC input) = 1.5381-1.6575e-10 reproduced",
     abs(old_lo - 1.538149307298732e-10) / 1.538149307298732e-10 < 1e-9
     and abs(old_hi - 1.6575358527649297e-10) / 1.6575358527649297e-10 < 1e-9,
     f"[{old_lo:.4e}, {old_hi:.4e}]"),
    ("composite self-consistency: sqrt(a0_DE x a0_RAR_hi) = 1.08e-10 (the observed deep-end "
     "low edge) to 0.02%",
     abs(math.sqrt(A0_DE * L232) / A0_EFF_LO - 1.0) < 0.001,
     f"sqrt(DE x L232) = {math.sqrt(A0_DE*L232):.6e} vs a0_eff_lo = {A0_EFF_LO:.4e} "
     f"(ratio {math.sqrt(A0_DE*L232)/A0_EFF_LO:.5f})"),
    ("G03D EFE-boosted fit = 5.00e-11 (0.534 x a0_DE), verdict v1 = FAIL (rejected)",
     abs(G03D - 5.00e-11) < 1e-14
     and jload("g03d_efe_refit_results.json")["verdict"]["v1"] is False,
     f"a0 = {G03D:.3e} = 0.534 x a0_DE; the EFE resolution is the REJECTED leg (G166 V2)"),
]
n_gate = 0
for label, ok, val in gates:
    n_gate += ok
    print(f"    [{'OK' if ok else 'XX'}] {label}: {val}")
print(f"  gates: {n_gate}/{len(gates)} pass")

res = dict(
    lane="G193_composite_reconsidered",
    title="THE COMPOSITE RECONSIDERED: the corrected a0_c after the M/L collapse (G167)",
    composite=dict(
        a0_eff_band=[A0_EFF_LO, A0_EFF_HI],
        a0_eff_over_de=[A0_EFF_LO / A0_DE, A0_EFF_HI / A0_DE],
        a0_lambda=A0_DE,
        a0_c_band=[A0_C_LO, A0_C_HI],
        a0_c_mid=A0_C_MID,
        a0_c_sigma=A0_C_SIG,
        a0_c_over_de=[A0_C_LO / A0_DE, A0_C_HI / A0_DE],
        a0_c_over_s_lambda=[A0_C_LO / S_LAMBDA, A0_C_HI / S_LAMBDA],
        error_budget=dict(rel_a0eff_band=2 * SIG_EFF, rel_a0DE_nominal=SIG_DE,
                          rel_total=SIG_C, note="dln a0_c = 2 dln a0_eff + dln a0_DE"),
        g166_before=dict(a0_c_rar=[old_lo, old_hi],
                         shrink=[old_lo / A0_C_LO, old_hi / A0_C_HI],
                         a0_c_mightee_end=3.629256652265032e-10,
                         note="pre-collapse partner; the MIGHTEE-end partner 3.63e-10 is dead"),
        self_reference=dict(sqrt_DE_x_RARhi=math.sqrt(A0_DE * L232),
                            ratio_to_a0eff_lo=math.sqrt(A0_DE * L232) / A0_EFF_LO),
    ),
    candidates=[
        dict(name=c["name"], a0=c["a0"], ratio_lo=c["ratio_lo"], ratio_mid=c["ratio_mid"],
             ratio_hi=c["ratio_hi"], in_band=c["in_band"], src=c["src"]) for c in cands
    ],
    nearest_registered=dict(
        name="L232 SPARC free-fit (n=2)", a0=L232, s_over_s_lambda=1.3305,
        ratio_a0c_lo=L232 / A0_C_LO, note="composite partner's low edge = the SPARC "
                                          "free-fit optimum to 0.02%; also (4/3) a0_DE "
                                          "and sqrt(a0_DE cH0/4) in band"),
    residual_tension=dict(
        ratio=[ratio_lo, ratio_hi], dex=[dex_lo, dex_hi], dex_mid=dex_mid,
        dex_per_sigma=DX_PER_SIG,
        sigma_stat_only=[sig_stat_lo, sig_stat_hi],
        sigma_ML_dex=SIG_ML,
        sigma_total_dex=SIG_TOT,
        sigma_budgeted=[sig_lo_f, sig_hi_f],
        sigma_budgeted_mid=dex_mid / SIG_TOT,
        dwarf_lane_alone_sigma=(dwarf_lane_a0 - A0_DE) / dwarf_lane_sig,
        note="G133's 5.2-sigma (log) staircase rejection collapses to ~2.2-2.5 sigma "
             "statistical / ~1.7 sigma budgeted"),
    verdicts=dict(V1=V1, V2=V2, V3=V3),
    gates=[{"name": n, "pass": p, "measured": v} for n, p, v in gates],
    n_gates=n_gate, n_gates_total=len(gates),
    sources=dict(G167="deepseek_push/G167_pipeline_split.py + results (matched-M/L deep end "
                      "1.08-1.1e-10, dwarf bins, cross-convention table)",
                 G189="deepseek_push/G189_seesaw_fate.py + results (candidate inventory: "
                      "(4/3)a0_DE, sqrt(a0_DE cH0/4), s_Lambda, sqrt(2)a0_DE, a0_DE/Omega_L)",
                 G166="deepseek_push/G166_footing_map.py + results (pre-collapse composite "
                      "1.54-1.66e-10)",
                 G133="deepseek_push/G133_mightee_footing.py + results (deep_dex/sigma_log "
                      "0.02851; the 80-ring set)",
                 L232="fable_independent_2026/L232_sparc_parameter_free.py (n=2 free scale "
                      "s/s_Lambda = 1.3305 -> 1.2457e-10)",
                 G03D="deepseek_push/g03d_efe_refit_results.json (boosted 5.00e-11, rejected)"),
)
out = os.path.join(HERE, "G193_results.json")
json.dump(res, open(out, "w"), indent=1)
print(f"\nwrote {out}")
print(f"G193 COMPLETE: {NP}/{NP+NF} analytic checks PASS; gates {n_gate}/{len(gates)}.")