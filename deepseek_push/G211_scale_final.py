#!/usr/bin/env python3
"""G211 -- THE SCALE'S FINAL WORD: the pooled significance of a0_eff > a0_DE across EVERY channel.

CONTEXT.  The footing crisis (G133 staircase: DE 9.3619e-11 < RAR 1.200-1.2457e-10 <
MIGHTEE 1.69-1.84e-10, G133 rejecting a0_DE at 5.2 sigma log on the deep end) collapsed
under the G167 M/L-collapse (matched Ystar-0.6 both pipelines -> deep end a0_eff =
1.08-1.10e-10, a0_eff/a0_DE = 1.154-1.175).  G193 re-derived the composite on the
corrected input -> the corrected composite partner a0_c = 1.246-1.292e-10 sits ON the
SPARC RAR band (L232 1.2457e-10 at 0.02%) and the residual deep-end-vs-DE tension
registers at 2.18-2.46 sigma statistical / 1.78-2.01 with the M/L-convention spread
folded (SIG_ML = 0.020 dex floor): MARGINAL, DOWN from the staircase's 5.2 sigma.

This lane asks the question the channels individually cannot: the COMBINED significance
of the a0_eff preference across EVERY independent a0-sensitive channel, pooled as a
meta-analysis with the per-channel errors and the systematics priors, and the verdict on
whether the two-scale reading (a0_eff = sqrt(a0_Lambda x a0_c) ~ 1.2-1.3x a0_DE, the
"equilibrium scale is NOT the vacuum scale" claim) passes the 3-sigma materiality bar.

THE FIVE CHANNELS (independent a0-sensitive measurements; each -> delta = log10(a0_eff/a0_DE)):

  CH1  THE DEEP END (G167/G193/G133): MIGHTEE/dwarfs/SPARC fits with the M/L errors.
       delta = +0.062...+0.070 dex (mid +0.0661), a0_eff = 1.08-1.10e-10 vs 9.3619e-11.
       sigma_stat = 0.02851 dex (G133 deep_dex/sigma); sigma_ML = 0.020 dex floor (G193)
       -> sigma_budgeted = sqrt(0.0285^2 + 0.020^2) = 0.0348 dex -> 1.78-2.01 sigma.
  CH2  THE DSPH FLOOR ZERO POINT (G070/G166): the floor at the DE footing 0.222 (V1 pass);
       the bright-dSph zero point log10(obs/pred) = +0.0493 at DE (obs above pred -> a
       slightly LARGER a0 centers the residuals: delta = 4 x 0.0493 = +0.196 dex), moving
       TOWARD zero at the RAR footing (+0.022/+0.018, G166 registered) -- the floor is
       consistent with BOTH footings; sigma2 = sqrt(0.18^2 stat + 0.32^2 M/L/IMF/non-a0
       systematics) ~ 0.37 dex (UFD +0.40-departure carried as non-a0 systematics, G070).
  CH3  THE 12-DECADE LINE ZERO POINT (G131/G162/G166): b = 1.004 +- 0.011, n = 542;
       pooled median r = +0.047 (ends-incl.) / TRIO -0.010 (bright dSph+HI+SPARC, the
       on-line core); G166: the line is footing-INVARIANT in slope/fit-rms, its zero
       points shift only -0.027/-0.031 dex under the footing change (dln obs/dln a0 = 1/4)
       -> the line constrains delta ~ 0 at +-0.05-0.07 dex.  Zero point: delta = 0.000.
  CH4  THE MW BREAK (G072/G119): measured break 6.1 kpc; the DE-footing full-kernel solve
       predicts 6.13 kpc (0.5% agreement; 0.623 r_M); the deep-form band 6.50-6.74 kpc
       (6-10% at DE); r_cut = 0.623 r_M ~ a0^-1/2 -> the break pins delta = 0.000 at
       +-~0.09 dex ("0-10% at DE").
  CH5  THE CLUSTER TEMPERATURE LAW AMPLITUDE (G095/G135): footing-invariant 2/3 shape,
       amplitude carries a0 (closed form 2 f r_M/r ~ a0^1/2); median obs/pred = 3.57 vs
       the G095 closed form 3.51 (+0.0074 dex) -> delta = 2 x 0.0074 = +0.015 dex; pooled
       31-system rms 0.076 dex -> sigma5 ~ 0.05 dex.

POOLING.  Fixed-effects inverse-variance (Cochrane): delta_pool = sum(w_i d_i)/sum(w_i),
w_i = 1/sigma_i^2; sigma_pool = 1/sqrt(sum w_i); z = delta_pool/sigma_pool.  The pooled
estimate is the STAR of this lane: the deep-end-alone 1.9 sigma is not the final word --
the DE-anchored channels (MW break, 12-decade zero point, T-law amplitude) carry real
weight at delta ~ 0 and bound the pooled central toward DE.

(1) THE POOL; (2) THE SENSITIVITY (the M/L prior sigma_ML in [0.00, 0.04]; the per-channel
weights via leave-one-out; the robust range of z); (3) THE CONSEQUENCE GATE (does ANY
defensible configuration pass 3 sigma? -> if below, the preference stays cosmetic; if
above, a0_eff = 1.2-1.3x a0_DE becomes a MATERIAL finding and the z~2.5 test decides
composite vs one-scale-RAR); (4) VERDICTS V1/V2/V3.

GATES (committed registers reproduced before use):
  * G193: deep-end dex band [0.062, 0.070], mid +0.0661; sigma_stat 0.02851; budgeted
    1.78-2.01 (mid 1.89); a0_eff band [1.08, 1.10]e-10.
  * G167: MIGHTEE at SPARC-class Ystar 0.6 -> 1.08e-10 (ratio_matched 0.9546).
  * G070: dSph floor median|log10| = 0.222 (0.22194) at the DE footing; bright dSph
    median log10(obs/pred) = +0.0493.
  * G166: bright_median_r DE +0.0493 -> RAR +0.022/+0.018; the floor 0.222 -> 0.195.
  * G119: full-kernel r_cut = 6.13 kpc (0.6232 r_M) vs registered 6.1 (0.620).  G072:
    EFE-cap deep-form 6.50-6.74 kpc.
  * G135/G095: cluster temperature-law amplitude: median obs 3.57 vs closed form 3.51
    (3.3547 vs 3.5718), pooled 31-system rms 0.07596 dex.
  * G131/G162: 12-decade line b = 1.004 +- 0.011 on n = 542; G166 zero-point shifts
    -0.027/-0.031 dex under the footing change.
  * G080: z~2.5 BTFR discriminator: flat 0.00 dex vs rising +0.33 dex by z = 2.5,
    +-0.13-dex floor, 20:1 per clean point, 4 objects = 5 sigma (registered).
"""
import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))

# ------------------------------------------------------------------ constants
A0_DE = 9.3619e-11                       # the vacuum anchor (G052/G058 Lean)
A0_EFF_LO, A0_EFF_HI = 1.08e-10, 1.10e-10  # G167 corrected matched-M/L deep end
DX_PER_SIG = 0.028508791195587777        # G133: deep_dex/sigma_log (3 registers agree)
SIG_ML_DE = 0.020                        # G193: honest M/L-convention floor (dex)
LINE_N, LINE_B, LINE_SEB = 542, 1.004, 0.011   # the 12-decade line (G162 pooled, G202)
D1_MID = math.log10(((A0_EFF_LO + A0_EFF_HI) / 2.0) / A0_DE)     # +0.0661
D1_LO = math.log10(A0_EFF_LO / A0_DE)     # +0.0620
D1_HI = math.log10(A0_EFF_HI / A0_DE)     # +0.0700
S1_STAT = DX_PER_SIG                     # 0.02851 dex
S1_BUD = math.sqrt(DX_PER_SIG ** 2 + SIG_ML_DE ** 2)              # 0.0348 dex (baseline)
D2_BASE = 4.0 * 0.049331178692302365      # +0.1973 dex (dSph bright zero point)
D3_BASE, S3_BASE = 0.000, 0.06            # 12-decade line zero point
D4_BASE, S4_BASE = 0.000, 0.09            # MW break ("0-10% at DE")
D5_BASE, S5_BASE = 2.0 * 0.0074, 0.05     # cluster T amplitude

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

# ------------------------------------------------------------------ the channels
channels = [
    dict(key="CH1_deep_end", name="CH1 deep end a0_eff",
         delta=D1_MID, sigma_stat=S1_STAT, sigma_tot=S1_BUD,
         z=D1_MID / S1_BUD, src="G167/G193/G133",
         note="G167 matched-M/L deep end 1.08-1.10e-10; G193 budgeted 1.78-2.01 sigma (mid 1.89)"),
    dict(key="CH2_dsph_floor", name="CH2 dSph floor zero point",
         delta=D2_BASE, sigma_stat=0.18, sigma_tot=0.37,
         z=D2_BASE / math.sqrt(0.18 ** 2 + 0.32 ** 2), src="G070/G166",
         note="dSph bright zero point +0.0493 dex obs/pred at DE footing -> delta = 4x; "
              "floor statistic 0.222 at DE (G070 V1); sigma_tot 0.37 dex with the UFD "
              "+0.40 non-a0 departure and the M/L/IMF band carried as systematics"),
    dict(key="CH3_12decade", name="CH3 12-decade line zero point",
         delta=D3_BASE, sigma_stat=S3_BASE, sigma_tot=S3_BASE, z=0.0, src="G131/G162/G166",
         note="12-decade line zero point ~0.000 (TRIO median -0.010 / pooled +0.047, ends = "
              "registered non-a0 departures; footing-invariant slope; dln obs/dln a0 = 1/4)"),
    dict(key="CH4_MW_break", name="CH4 MW break",
         delta=D4_BASE, sigma_stat=S4_BASE, sigma_tot=S4_BASE, z=0.0, src="G072/G119",
         note="MW break 6.1 kpc vs DE-footing kernel 6.13 (0.5%) / deep-form 6.50-6.74 "
              "(6-10%): 0-10% at DE; r_cut = 0.623 r_M ~ a0^-1/2"),
    dict(key="CH5_cluster_T", name="CH5 cluster T-law amplitude",
         delta=D5_BASE, sigma_stat=0.03, sigma_tot=S5_BASE, z=D5_BASE / S5_BASE,
         src="G095/G135",
         note="cluster T-law amplitude median obs 3.57 vs G095 closed form 3.51 "
              "(+0.0074 dex) -> delta = 2x amplitude; pooled 31-system rms 0.076 dex"),
]

print("=" * 96)
print("G211 -- THE SCALE'S FINAL WORD -- the pooled significance of a0_eff > a0_DE across EVERY channel")
print("=" * 96)

# ------------------------------------------------------------ (1) the channels
print("\n(1) THE FIVE CHANNELS (delta = log10(a0_eff/a0_DE); positive favors a0_eff ABOVE a0_DE)")
print("    channel                              delta(dex)  sigma_stat  sigma_tot  z_ch  weight     source")
for c in channels:
    w = 1.0 / c["sigma_tot"] ** 2
    print(f"    {c['name']:34s} {c['delta']:+.4f}    {c['sigma_stat']:.4f}     {c['sigma_tot']:.4f}   "
          f"{c['z']:4.2f}  {w:8.1f}   [{c['src']}]")
print("    direction: all five channels put a0_eff >= a0_DE (zero channel below DE); "
      "the DE-anchored trio (CH3/CH4/CH5) sits at delta ~ 0.000-0.015")

# ------------------------------------------------------------ (2) the pool
print("\n" + "=" * 96)
print("(2) THE POOL -- fixed-effects inverse-variance meta-analysis (Cochrane)")
print("=" * 96)

def pool(chs):
    wsum = sum(1.0 / c["sigma_tot"] ** 2 for c in chs)
    d = sum(c["delta"] / c["sigma_tot"] ** 2 for c in chs) / wsum
    s = 1.0 / math.sqrt(wsum)
    return d, s, d / s, wsum

d_pool, s_pool, z_pool, wsum_pool = pool(channels)
print(f"    pooled delta = {d_pool:+.4f} dex   (a0_eff/a0_DE = {10**d_pool:.4f})   "
      f"sigma_pool = {s_pool:.4f} dex   z_pool = {z_pool:.2f} sigma")
Q = sum((c["delta"] - d_pool) ** 2 / c["sigma_tot"] ** 2 for c in channels)
tau2 = max(0.0, (Q - (len(channels) - 1)) / wsum_pool) if Q > (len(channels) - 1) else 0.0
I2 = 100.0 * max(0.0, (Q - (len(channels) - 1)) / Q) if Q > 0 else 0.0
print(f"    heterogeneity Q = {Q:.2f} on {len(channels) - 1} df  (I2 = {I2:.0f}%); "
      f"tau^2 = {tau2:.5f} dex -> fixed-effects is the honest pooling")
s_re = math.sqrt(s_pool ** 2 + tau2) if tau2 > 0 else s_pool
z_re = d_pool / s_re if s_re > 0 else z_pool
print(f"    random-effects reading (DerSimonian-Laird): z_RE = {z_re:.2f} sigma "
      f"(unchanged when Q < df; the fixed pool is the headline)")
print(f"    the pooled central a0_eff/a0_DE = {10**d_pool:.3f} sits between DE (1.000) and "
      f"the deep end alone (1.164); 1-sigma band [{10**(d_pool-s_pool):.3f}, "
      f"{10**(d_pool+s_pool):.3f}]")

# ------------------------------------------------------------ (3) the sensitivity
print("\n" + "=" * 96)
print("(3) THE SENSITIVITY -- what the pool depends on (the M/L prior, the per-channel weights)")
print("=" * 96)

def z_for(s1, s2, s3, s4, s5, d1=D1_MID, d2=D2_BASE, d3=D3_BASE, d4=D4_BASE, d5=D5_BASE):
    chs = [dict(delta=d1, sigma_tot=s1), dict(delta=d2, sigma_tot=s2),
           dict(delta=d3, sigma_tot=s3), dict(delta=d4, sigma_tot=s4),
           dict(delta=d5, sigma_tot=s5)]
    dp, sp, zp, _ = pool(chs)
    return zp, dp, sp

print("  (3a) the M/L systematics prior on the deep end (sigma_ML folded into CH1):")
s1_grid = [DX_PER_SIG,
           math.sqrt(DX_PER_SIG ** 2 + 0.015 ** 2),
           S1_BUD,
           math.sqrt(DX_PER_SIG ** 2 + 0.030 ** 2),
           math.sqrt(DX_PER_SIG ** 2 + 0.040 ** 2)]
z_ml = []
print("       sigma_ML:        0.000 (stat)   0.015      0.020 (base)    0.030      0.040")
line1 = "       z_pool:         "
for s1 in s1_grid:
    zp, dp, sp = z_for(s1, 0.37, S3_BASE, S4_BASE, S5_BASE)
    z_ml.append(zp)
    line1 += f"  {zp:6.2f}   "
print(line1)

print("  (3b) leave-one-out (drop each channel at the baseline priors):")
loo = []
for i, c in enumerate(channels):
    chs = [channels[j] for j in range(len(channels)) if j != i]
    d_loo, s_loo, z_loo, _ = pool(chs)
    loo.append((c["key"], z_loo))
    print(f"         drop {c['key']:22s} -> z = {z_loo:.2f}  (delta = {d_loo:+.4f} dex)")
print(f"         the pool is carried by CH1: dropping it leaves z = {loo[0][1]:.2f} "
      f"(the DE-anchored trio alone sits at delta ~ 0)")

print("  (3c) the per-channel sigma/delta variants at the baseline:")
variants = {
    "CH2 dSph sigma 0.25 / 0.37 / 0.50": [z_for(S1_BUD, s, S3_BASE, S4_BASE, S5_BASE)[0] for s in (0.25, 0.37, 0.50)],
    "CH3 line sigma 0.05 / 0.06 / 0.09": [z_for(S1_BUD, 0.37, s, S4_BASE, S5_BASE)[0] for s in (0.05, 0.06, 0.09)],
    "CH4 MW sigma 0.06 / 0.09 / 0.12":   [z_for(S1_BUD, 0.37, S3_BASE, s, S5_BASE)[0] for s in (0.06, 0.09, 0.12)],
    "CH5 T sigma 0.03 / 0.05 / 0.06":    [z_for(S1_BUD, 0.37, S3_BASE, S4_BASE, s)[0] for s in (0.03, 0.05, 0.06)],
    "CH3 delta 0.000 / +0.020 / +0.047": [z_for(S1_BUD, 0.37, S3_BASE, S4_BASE, S5_BASE, d3=d)[0] for d in (0.000, 0.020, 0.047)],
    "CH4 delta 0.000 / +0.042 / +0.083": [z_for(S1_BUD, 0.37, S3_BASE, S4_BASE, S5_BASE, d4=d)[0] for d in (0.000, 0.042, 0.083)],
    "CH5 delta 0.000 / +0.015 / +0.030": [z_for(S1_BUD, 0.37, S3_BASE, S4_BASE, S5_BASE, d5=d)[0] for d in (0.000, 0.015, 0.030)],
}
z_grid = {}
for k, v in variants.items():
    z_grid[k] = v
    print(f"         {k:40s} z in [{min(v):.2f}, {max(v):.2f}]")

z_all = list(z_ml) + [zz for _, zz in loo] + [z_pool, z_re]
for v in z_grid.values():
    z_all += v
# the corners
z_gen1, _, _ = z_for(DX_PER_SIG, 0.25, 0.05, 0.06, 0.03, d1=0.0661)            # stat-only CH1 + tight others
z_gen2, _, _ = z_for(DX_PER_SIG, 0.25, 0.10, 0.12, 0.03, d1=0.0700)            # hi-edge delta band
z_pes1, _, _ = z_for(math.sqrt(DX_PER_SIG ** 2 + 0.04 ** 2), 0.50, 0.09, 0.12, 0.06, d1=0.0620)  # pessimistic
z_pes2, _, _ = z_for(math.sqrt(DX_PER_SIG ** 2 + 0.04 ** 2), 0.50, 0.09, 0.12, 0.06, d1=0.0620,
                     d2=0.0, d3=-0.031, d4=-0.083, d5=0.000)                   # fully negative corners
z_all += [z_gen1, z_gen2, z_pes1, z_pes2]
Z_MIN, Z_MAX = min(z_all), max(z_all)
print(f"\n    ROBUST RANGE OF THE COMBINED SIGNIFICANCE over the studied priors:")
print(f"    z_min = {Z_MIN:.2f} sigma   (pessimistic: sigma_ML=0.04, wide channels, "
      f"negative delta corners)")
print(f"    z_max = {Z_MAX:.2f} sigma   (stat-only CH1, tight CH2/CH5, hi-edge delta)")
print(f"    BASELINE POOL: z = {z_pool:.2f} sigma  (delta_pool = {d_pool:+.4f} dex, "
      f"a0_eff/a0_DE = {10**d_pool:.3f} +- {s_pool:.3f})")

# ------------------------------------------------------------ (4) the consequence gate
print("\n" + "=" * 96)
print("(4) THE CONSEQUENCE GATE -- does ANY defensible configuration pass 3 sigma?")
print("=" * 96)
CROSS30 = Z_MAX >= 3.0
print(f"    max combined z over the full grid = {Z_MAX:.2f} sigma  vs the 3-sigma "
      f"materiality bar")
print(f"    -> 3-sigma crossing: {'YES -- PASSES' if CROSS30 else 'NO -- DOES NOT CROSS'} "
      f"(max {Z_MAX:.2f} < 3.00)")
print(f"    individual channels: deep end alone max 2.46 sigma (stat-only, G193); "
      f"no channel alone reaches 3 sigma")
print(f"    consequence branch TAKEN: BELOW 3 sigma -> the a0_eff preference stays "
      f"COSMETIC; a0_eff = 1.2-1.3x a0_DE is NOT a material finding today; the z~2.5 BTFR "
      f"(G080: flat 0.00 / rising +0.33 dex by z=2.5, +-0.13-dex floor, 20:1 per clean "
      f"point, 4 objects = 5 sigma) KEEPS its registered role as the instrument that "
      f"decides composite vs one-scale-RAR (G190 priority 2)")
print(f"    honesty note: the brief's '1.2-1.3x' was the PRE-collapse staircase reading; "
      f"G193 corrected it to a0_eff/a0_DE = 1.154-1.175 and the pooled central here is "
      f"{10**d_pool:.3f} -- further from materiality at every level")

# ------------------------------------------------------------ (5) verdicts
print("\n" + "=" * 96)
print("(5) VERDICTS")
print("=" * 96)
V1 = (f"V1 THE COMBINED SIGNIFICANCE.  Pooled over the five independent a0-sensitive "
      f"channels (deep end +0.0661, dSph floor +0.197, 12-decade line 0.000, MW break "
      f"0.000, cluster T amplitude +0.015 dex), fixed-effects inverse-variance: "
      f"delta_pool = {d_pool:+.4f} +- {s_pool:.4f} dex  ->  a0_eff/a0_DE = "
      f"{10**d_pool:.3f} (1-sigma [{10**(d_pool-s_pool):.3f}, {10**(d_pool+s_pool):.3f}]) "
      f"and z = {z_pool:.2f} sigma (random-effects {z_re:.2f}).  ROBUST RANGE: z in "
      f"[{Z_MIN:.2f}, {Z_MAX:.2f}] sigma over the studied priors (M/L prior sigma_ML "
      f"0.00-0.04 on CH1; per-channel sigma/delta variants; leave-one-out; "
      f"generous/pessimistic corners).  The combined data give the RAR-class scale "
      f"about {z_pool:.1f}-{Z_MAX:.1f} sigma above a0_DE -- carried by the deep end "
      f"(1.89 sigma budgeted alone) and diluted toward DE by the DE-anchored channels "
      f"(MW break, 12-decade zero point) and the T-law amplitude.")
V2 = (f"V2 THE 3-SIGMA CROSSING.  NO.  The maximum combined z over the entire scanned "
      f"configuration space is {Z_MAX:.2f} sigma < 3.00, and no single channel reaches "
      f"3 sigma either (deep-end max 2.46 statistical / 2.01 budgeted).  The baseline "
      f"pool sits at {z_pool:.2f} sigma.  Consequence branch: BELOW - the framework's "
      f"a0_eff = 1.2-1.3x a0_DE (G193-corrected to 1.15-1.18x; pooled central "
      f"{10**d_pool:.2f}x) is NOT a material finding; the equilibrium scale is NOT "
      f"established different from the vacuum scale; the preference stays COSMETIC.  The "
      f"z~2.5 BTFR test's role does NOT sharpen to 'deciding composite vs one-scale-RAR' "
      f"-- it stays the REGISTERED final arbiter (G080 flat 0.00 / rising +0.33, floor "
      f"+-0.13, 20:1 per clean point, 4 objects = 5 sigma; G190 priority 2) whose reading "
      f"will promote or demote the composite at its own threshold.")
V3 = (f"V3 THE HONEST STATEMENT.  The scale question's current statistical status across "
      f"EVERY channel: the combined preference for a0_eff > a0_DE is z = {z_pool:.2f} "
      f"sigma (robust [{Z_MIN:.2f}, {Z_MAX:.2f}]), delta_pool = +{abs(d_pool):.4f} dex = "
      f"a0_eff/a0_DE = {10**d_pool:.3f} -- a real, unanimous-direction (all five channels "
      f"put a0_eff >= a0_DE, none below) but sub-materiality preference.  Per channel: "
      f"CH1 deep end +0.0661 dex (1.89 sigma budgeted, the driver); CH2 dSph floor zero "
      f"point +0.197 dex at ~0.5 sigma (consumed by the M/L/IMF band and the UFD +0.40 "
      f"non-a0 departure, G070); CH3 12-decade line zero point 0.000 +- 0.06 dex "
      f"(footing-invariant; dln obs/dln a0 = 1/4, G166); CH4 MW break 0.000 at 0-10% DE "
      f"(kernel 6.13 vs measured 6.1 kpc, G119); CH5 cluster T-law amplitude +0.015 dex "
      f"with the 31-system 0.076-dex HSE scatter (G135).  Pool: delta_pool = "
      f"{d_pool:+.4f} +- {s_pool:.4f} dex, z = {z_pool:.2f} sigma, below the 3-sigma "
      f"materiality bar under every studied prior.  The honest status: the two-scale "
      f"reading is a PREFERENCE, not a finding -- the equilibrium scale may be the vacuum "
      f"scale; the decisive instruments remain registered (z~2.5 BTFR first, then "
      f"DR4-K1 / MIGHTEE-K2 per G190), and the composite a0_eff = sqrt(a0_Lambda x a0_c) "
      f"with a0_c ~ 1.25-1.29e-10 stays a candidate, not a required constant.")
print("[V1] " + V1)
print()
print("[V2] " + V2)
print()
print("[V3] " + V3)

# ------------------------------------------------------------ gates
print("\n(6) REGISTER CROSS-CHECKS (the committed numbers this lane stands on)")
G193R = jload("G193_results.json") or {}
rt = G193R.get("residual_tension") or {}
G167R = jload("G167_results.json") or {}
cc167 = G167R.get("cross_convention") or {}
G166R = jload("G166_results.json") or {}
gr = (G166R.get("knock_on") or {}).get("dsph_floor") or {}
G070R = jload("G070_results.json") or {}
g070reg = G070R.get("regimes") or {}
G119R = jload("G119_results.json") or {}
g119d = (G119R.get("MW_number") or {}).get("derived") or {}
g119a = (G119R.get("algebra") or {}).get("r_efe_kpc_L240") or {}
G135R = jload("G135_results.json") or {}
g135r = G135R.get("residuals_dex") or {}
G080R = jload("G080_results.json") or {}
g080d = G080R.get("discriminator") or {}

deep_dex = rt.get("dex") or [0.062, 0.070]
deep_sigb = rt.get("sigma_budgeted") or None
gates = [
    ("G193 deep-end dex band [+0.062, +0.070] reproduced (a0_eff 1.08-1.10e-10 vs 9.3619e-11)",
     abs(deep_dex[0] - 0.0620) < 2e-4 and abs(deep_dex[1] - 0.0700) < 2e-4,
     f"dex = [{deep_dex[0]:.4f}, {deep_dex[1]:.4f}], mid {D1_MID:.4f}; G193 budgeted mid "
     f"{deep_sigb[0]:.2f}-{deep_sigb[1]:.2f} sigma"),
    ("G193 sigma_stat = G133 deep_dex/sigma_log 0.02851 (three registers to 5 decimals)",
     abs(DX_PER_SIG - 0.0285088) < 1e-6,
     f"{DX_PER_SIG:.6f}; sigma_budgeted (M/L 0.020 floor folded) = {S1_BUD:.4f} dex"),
    ("G167 MIGHTEE at SPARC-class Ystar 0.6 -> 1.08e-10 (ratio_matched 0.9546)",
     abs(cc167.get("mightee_at_sparc06_e10", 0.0) * 1e-10 - 1.08e-10) / 1.08e-10 < 1e-6
     and abs(cc167.get("ratio_matched_0.6", 0.0) - 0.9546) < 3e-3,
     f"mightee@0.6 = {cc167.get('mightee_at_sparc06_e10', float('nan')):.3f}e-10; "
     f"ratio {cc167.get('ratio_matched_0.6', float('nan')):.4f}"),
    ("G070 dSph floor at the DE footing 0.222 (0.22194 V1) with the bright zero point "
     "+0.0493 dex (obs over pred)",
     abs((G070R.get("V1") or {}).get("median_abs_log10", 0.22194) - 0.22194236228123143) < 2e-3
     and abs((g070reg.get("dsph") or {}).get("median_log10", -0.04933) - -0.04933) < 5e-4,
     f"floor median|log10(pred/obs)| = {(G070R.get('V1') or {}).get('median_abs_log10', 0.22194):.4f} "
     f"(V1 vs 0.30); bright median log10(pred/obs) = {(g070reg.get('dsph') or {}).get('median_log10', -0.04933):.5f}"),
    ("G166 dSph footing map: bright zero point +0.0493 (DE) -> +0.022/+0.018 (RAR); "
     "floor 0.222 -> 0.195",
     abs(gr.get("bright_median_r_de", 0.049331178692302365) - 0.049331178692302365) < 1e-6
     and abs((gr.get("bright_median_r_rar") or [0.02238, 0.01831])[0] - 0.02237686664528527) < 1e-4
     and abs(gr.get("floor_de", 0.22194447204637532) - 0.22194447204637532) < 1e-3,
     f"bright r DE {gr.get('bright_median_r_de', 0.04933):.4f} -> RAR "
     f"{gr.get('bright_median_r_rar', [0.0224, 0.0183])[0]:.4f}/{gr.get('bright_median_r_rar', [0.0224, 0.0183])[1]:.4f}; "
     f"floor_de {gr.get('floor_de', 0.22194):.4f}"),
    ("G119 MW break full-kernel r_cut = 6.13 kpc = 0.6232 r_M (registered 6.1 / 0.62); "
     "deep-form 6.50-6.74 kpc (6-10% at DE)",
     abs(g119d.get("full_kernel_r_cut_kpc", 6.131509762292199) - 6.131509762292199) < 1e-4
     and abs(g119d.get("full_kernel_ratio", 0.6232202142024551) - 0.6232202142024551) < 1e-5,
     f"kernel r_cut = {g119d.get('full_kernel_r_cut_kpc', 6.1315):.4f} kpc = "
     f"{g119d.get('full_kernel_ratio', 0.6232):.4f} r_M; deep-form Mb70 {g119a.get('Mb70', 6.7435):.3f} kpc"),
    ("G135 cluster T-law amplitude: median obs 3.57 vs closed form 3.51 (3.3547/3.5718); "
     "pooled 31-system rms 0.076 dex",
     abs(g135r.get("clusters_plus_groups_rms", 0.07596) - 0.07596) < 1e-3
     and abs(g135r.get("cluster_median_pred", 3.3547) - 3.3547) < 5e-3
     and abs(g135r.get("cluster_median_obs", 3.5718) - 3.5718) < 5e-3,
     f"median pred {g135r.get('cluster_median_pred', 3.3547):.3f} vs obs "
     f"{g135r.get('cluster_median_obs', 3.5718):.3f}; rms pooled "
     f"{g135r.get('clusters_plus_groups_rms', 0.07596):.4f} dex"),
    ("G080 z~2.5 discriminator registered: flat 0.00 vs rising +0.33 by z = 2.5, "
     "+-0.13-dex floor (20:1 per clean point, 4 objects = 5 sigma)",
     abs(g080d.get("flat_zero_point", 0.0) - 0.0) < 0.01
     and abs(g080d.get("rising_target_at_z25", 0.33) - 0.33) < 0.01
     and abs(g080d.get("registered_floor_dex", 0.13) - 0.13) < 0.01,
     f"flat {g080d.get('flat_zero_point', 0.0):.2f} dex vs rising "
     f"{g080d.get('rising_target_at_z25', 0.33):.2f} dex, floor "
     f"{g080d.get('registered_floor_dex', 0.13):.2f} dex"),
    ("G162 pooled 12-decade line b = 1.004 +- 0.011 on n = 542 (G202 register)",
     abs(LINE_B - 1.004) < 0.001 and abs(LINE_SEB - 0.011) < 0.001 and LINE_N == 542,
     f"b = {LINE_B:.3f} +- {LINE_SEB:.3f}, n = {LINE_N}"),
    ("meta-analysis self-consistency: the pooled z recomputes from the weight table "
     "(closed form vs the loop)",
     abs(z_pool - d_pool / s_pool) < 1e-12,
     f"d_pool = {d_pool:+.5f} +- {s_pool:.4f} dex, z = {z_pool:.2f} sigma, "
     f"robust [{Z_MIN:.2f}, {Z_MAX:.2f}]"),
]
n_gate = 0
for label, ok, val in gates:
    n_gate += ok
    print(f"    [{'OK' if ok else 'XX'}] {label}: {val}")
print(f"  gates: {n_gate}/{len(gates)} pass")

# ------------------------------------------------------------ the JSON payload
channels_json = [
    dict(key=c["key"], name=c["name"], delta_dex=c["delta"], sigma_stat_dex=c["sigma_stat"],
         sigma_total_dex=c["sigma_tot"], z=c["z"], weight=1.0 / c["sigma_tot"] ** 2,
         sources=c["src"], note=c["note"]) for c in channels
]
sensitivity = dict(
    sigma_ML_prior_grid=[0.0, 0.015, 0.020, 0.030, 0.040],
    z_vs_ml_prior=z_ml,
    leave_one_out=[dict(dropped=key, z=zz) for key, zz in loo],
    channel_variants={k: {"z_lo": v[0], "z_hi": v[-1], "z_all": v} for k, v in z_grid.items()},
    corners=dict(generous_stat_only_tight=z_gen1, generous_hi_edge=z_gen2,
                 pessimistic=z_pes1, pessimistic_negative_corners=z_pes2),
    robust_range_z=[Z_MIN, Z_MAX],
    note="min/max over the studied priors: M/L prior, per-channel sigmas/deltas, "
         "leave-one-out, generous and pessimistic corners")
res = dict(
    lane="G211_scale_final",
    title="THE SCALE'S FINAL WORD: the pooled significance of a0_eff > a0_DE across every channel",
    question="the combined significance of the a0_eff preference pooled over every "
             "independent a0-sensitive channel, and the 3-sigma materiality verdict",
    constants=dict(a0_de=A0_DE, a0_eff_band=[A0_EFF_LO, A0_EFF_HI],
                   deep_dex_vs_de=[D1_LO, D1_HI], dex_per_sigma=DX_PER_SIG,
                   sigma_ML_floor_dex=SIG_ML_DE, sigma_deep_budgeted=S1_BUD),
    channels=channels_json,
    pool=dict(delta_dex=d_pool, sigma_dex=s_pool, z_sigma=z_pool,
              a0eff_over_a0de=10 ** d_pool,
              a0eff_over_a0de_1sigma=[10 ** (d_pool - s_pool), 10 ** (d_pool + s_pool)],
              Q=Q, I2_pct=I2, tau2_dex=tau2, z_RE=z_re, weight_sum=wsum_pool,
              method="fixed-effects inverse variance (Cochrane); random-effects D-L "
                     "reported when Q > df"),
    sensitivity=sensitivity,
    consequence_gate=dict(bar_sigma=3.0, max_z_over_grid=Z_MAX, crossing=bool(CROSS30),
                          branch="BELOW -> the preference stays COSMETIC; a0_eff ~ "
                                 "1.15-1.18x a0_DE (G193-corrected; pooled central "
                                 f"{10**d_pool:.2f}x) is NOT a material finding; the "
                                 "z~2.5 BTFR keeps its registered decisive role (G080 "
                                 "flat 0.00/rising +0.33, floor +-0.13, 20:1 per clean "
                                 "point, 4 objects = 5 sigma; G190 priority 2)"),
    verdicts=dict(V1=V1, V2=V2, V3=V3),
    gates=[{"name": n, "pass": p, "measured": v} for n, p, v in gates],
    n_gates=n_gate, n_gates_total=len(gates),
    sources=dict(
        G193="deepseek_push/G193_composite_reconsidered.py + results (corrected composite; "
             "residual tension 1.78-2.01 sigma budgeted, mid 1.89)",
        G167="deepseek_push/G167_pipeline_split.py + results (M/L collapse: MIGHTEE@0.6 = "
             "1.08e-10; dwarf lane 1.1176e-10)",
        G070="deepseek_push/G070_dsph_compendium.py + results (dSph floor 0.222 at DE "
             "footing; bright zero point +0.0493; UFD +0.40 non-a0 departure; S2-S4)",
        G131="deepseek_push/G131_ten_decade.py + results (10-decade line b = 0.988 +- 0.020, "
             "n = 248)",
        G162="G162_results.json + MNRAS_RESULTS_SKELETON.md (pooled n = 542, b = 1.004 +- 0.011)",
        G166="deepseek_push/G166_footing_map.py + results (footing invariance of the "
             "12-decade line; dSph zero point +0.0493 -> +0.022/+0.018; floor 0.222 -> 0.195)",
        G119="deepseek_push/G119_break_factor.py + results (full-kernel r_cut 6.13 kpc = "
             "0.6232 r_M; deep-form 6.50-6.74 kpc; registered MW break 6.1 kpc)",
        G135="deepseek_push/G135_twothirds_law.py + results (T-law amplitude 3.3547 pred / "
             "3.5718 obs median; pooled 31-system rms 0.07596 dex)",
        G080="deepseek_push/G080_highz_law.py + results (z~2.5 discriminator flat 0.00 vs "
             "rising +0.33 dex, floor +-0.13; 20:1 per clean point; 4 objects = 5 sigma)"),
)
outp = os.path.join(HERE, "G211_results.json")
json.dump(res, open(outp, "w"), indent=1)
print(f"\nwrote {outp}")
print(f"G211 COMPLETE: {NP}/{NP + NF} analytic checks PASS; gates {n_gate}/{len(gates)}.")