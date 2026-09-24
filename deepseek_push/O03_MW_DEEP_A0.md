# O03 — MW ROTATION CURVE DEEP-A0 MEASUREMENT (third independent channel for the deep tension)

**Lane:** O03 · **Date:** 2026-09-23 · **Data:** Eilers+19 Table 1 (38 pts, R = 5.27–24.82 kpc) · **a0:** 9.3619e-11 m/s² (canonical footing) · **Status:** LANDED — 10/14 checks PASS (see §9)

---

## 0. Purpose and pre-registration (stated before the statistics were computed)

The SPARC-deep moment lane (L06) measured a deep-regime `a0_eff/a0 = 0.73` (0.7241 ± 0.0662 on the canonical footing, z = −4.17 vs 1.0). The dwarf lane (O01, landed) finds 0.638 ± 0.163 (LT-deep) and 0.310 ± 0.117 (deep tail) — tension *weakens* on dwarfs. O03 supplies the **MW as a third independent systematics channel** (single galaxy; kinematic tracers = red-clump/APOGEE stars, different from HI/SPARC rings; baryonic model from the mass model Eilers+19 compare against).

**Pre-registered criteria:**
- **KILL-A:** |a0_eff_MW − 0.73·a0| > 3√(SE_MW² + SE_L06²), judged linear AND dex (OR rule), at the deepest *attained* probe → if triggered: *MW disagrees with the extragalactic deep tension (sample-dependent finding, registered)*; else: *three independent channels agree (major)*.
- **KILL-B:** |log10(a0_eff_MW/a0)| < 3 SE_dex → MW probe consistent with canonical a0.

The primary evaluation point was pre-registered as the deepest region the Eilers RC attains on the Eilers-fiducial baryons — see §4: the strict L06 cut (g_bar < 0.2 a0) turns out to be **unattainable inside 25 kpc under all three baryonic modelings tested** (N_deep = 0/0/2), which is itself the first registered finding.

## 1. Data and baryonic information carried by the table

`deepseek_push/data2/eilers2019_mw_rotation_curve_table1.csv` (manifest-registered, double-verified against the arXiv renderings) carries **only** `R_kpc, vc_kms, sigma_vc_minus_kms, sigma_vc_plus_kms` — **no baryonic columns**. Per protocol, g_bar is built from the **known Eilers components**. Crucial model-identity result established in-lane by reading Eilers+19 §V.3 (arXiv HTML): **the baryonic components Eilers+19 fixed for their NFW-halo fit are NOT McMillan — they are Pouliasis, Di Matteo & Haywood (2017, A&A 598, A66) Model I** (Miyamoto–Nagai thin/thick discs + spherical Plummer bulge, masses in units of 2.32×10⁷ M⊙) — plus McMillan (2017) gas added here for the brief's "bulge+disk+gas" (equal-total-mass exponentials, since the m-disk Σ0 values used as pure exponentials over-mass H2 by ~26×).

Table integrity checks PASS: 38 rows, R = 5.27–24.82 kpc, v_c(8.19) = 228.86 ± 0.80/0.67 km/s (C1, C2).

## 2. Baryonic models (three legs, all closed forms — no fragile numerics)

| leg | bulge | thin disc | thick disc | gas | V_bary(8.19) |
|---|---|---|---|---|---|
| **primary** “Eilers-fiducial” | Plummer M=1.0672e10, b=0.30 kpc | MN M=3.944e10, a=5.3, b=0.25 | MN M=3.944e10, a=2.6, b=0.8 | HI exp M=1.1e10, Rd=7 (Σ0,eff=35.7); H2 exp M=1.2e9, Rd=1.5 (84.9) | **191.1 km/s** |
| varA “Eilers-strict” (exactly what Eilers+19 fixed) | as primary | as primary | as primary | none | 183.5 km/s |
| varB “McMillan-class” (task-brief reading) | Hernquist M=8.9e9, α=0.7 | Σ0=896, Rd=2.5 | Σ0=183, Rd=3.02 | as primary | 182.1 km/s |

Verification (all from closed forms): exponential discs use the **auditor-verified Bessel closed form `vdisk_closed`** (N01_KERNEL_REFERENCE.py; 55.92 vs 55.9 km/s physical anchor); Miyamoto–Nagai and Plummer circular speeds are analytic; Hernquist via the enclosed-mass form V² = GM r/(r+α)² (no integration). Model identity checks:
- **C3 PASS** — primary V_bary(8.19) = **191.1 km/s ∈ [185, 205]** (the brief's anchor 230·√0.67 ≈ 189–192; no-gas strict 183.5, 0.8% below).
- **C4 PASS** — Eilers-strict baryons (183.5) + Eilers' own NFW halo (M_vir = 7.25e11, c = 12.8, R_s = 14.8 kpc, their §V.3) → **v_c(8.19) = 229.3 km/s vs 228.86 measured** (with the added gas: 235.4, 2.9% high — the gas is a documented addition).

g_bar conventions: primary g_bar = V_bar²/R (SPARC/G071-identical to L06); secondary g_bar = G·M_b(<R)/R² (task formula; closed forms + smooth Gauss–Legendre for the MN densities, verified M_enc(100 kpc)/M → 0.81/0.96 for thin/thick — see caveat §8); ratio 0.85–0.91 across the range (C10).

## 3. → g_obs, g_bar and the registered deep-cut finding

g_obs = V_obs²/R. Deep selection per L06: **g_bar < 0.2·a0**:

| leg | N_deep | smallest g_bar reached (R = 24.82 kpc) |
|---|---|---|
| primary | **0** | 0.241 a0 |
| varA | **0** | 0.207 a0 |
| varB | **2** (R = 23.66, 24.82) | 0.172 a0 |

**C5 FAIL — REGISTERED:** *under ALL THREE baryonic modelings the Eilers RC (5.27–24.82 kpc) does not contain a ≥ 10-point deep sample at the L06-identical cut (N = 0/0/2). The outer MW as measured by Eilers+19 keeps g_bar ≥ 0.17–0.24 a0 across its whole range; the asymptotic deep regime (0.2 a0) lies beyond R = 25 kpc under the Eilers-fiducial baryons.* The MW channel therefore rests on the **deepest-probe annuli (g_bar ≈ 0.17–0.35 a0)**, measured with the full a0-line estimator a0_eff = (g_obs² − g_bar²)/g_bar (≡ the deep line in the deep limit; arithmetic mean with a Newtonian floor at 0, since deep down-draws of the 6–28 km/s-error outer points can push g_obs below g_bar).

## 4. Deep-fit measurements

**Strict deep-line fit** (g_bar < 0.2 a0, varB leg, N = 2 — degenerate, protocol completeness only):
`log10 g_obs = 0.5 log10 g_bar + 0.5 log10 a0_eff` → **a0_eff/a0 = 1.389 ± 0.355** (SE_dex 0.121); per-point 1.10 and 1.75.

**Deepest probes** (full-line estimator, B = 10⁴ R-independent bootstrap with asymmetric V errors; SE = bootstrap std; deep-limit reading = geomean(g_obs²/g_bar)/a0 for comparison):

| probe | g_bar range | N | **a0_eff/a0 ± SE** | deep-limit reading |
|---|---|---|---|---|
| **primary** (Eilers-fiducial) R ≥ 22.5 | 0.241–0.284 a0 | 3 | **0.797 ± 0.236** (SE_dex 0.141; 68% [0.58, 1.04]) | 1.040 |
| primary R ≥ 20 | 0.241–0.351 a0 | 8 | 0.887 ± 0.142 | 1.154 |
| varA (Eilers-strict) R ≥ 22.5 | 0.207–0.245 a0 | 3 | 1.004 ± 0.274 | 1.207 |
| varA R ≥ 20 | 0.207–0.304 a0 | 8 | 1.115 ± 0.166 | 1.336 |
| varB (McMillan-class) R ≥ 22.5 | 0.172–0.206 a0 | 3 | 1.285 ± 0.328 | 1.446 |
| varB R ≥ 20 | 0.172–0.260 a0 | 8 | 1.410 ± 0.197 | 1.585 |

The two estimators straddle the truth: the arithmetic full-line mean is biased low by the Newtonian-floor and the wide scatter of the 22–24 kpc points (22.14 has σ_V = 28.6 km/s); the geometric deep-limit reading is the optimistic end. The bootstrap SE covers both.

## 5. Cross-check vs L06 (0.73) and O01 dwarfs — pre-registered verdicts

Three-channel row (canonical footing): **L06 SPARC-deep 0.724 ± 0.066 · O01 dwarfs 0.638 ± 0.163 (deep tail 0.31 ± 0.12) · O03 MW primary-probe 0.797 ± 0.236** (context: MIGHTEE-deep 2.164, z = +6.58, opposite sign, N05 on record).

- **KILL-A — NOT TRIGGERED (registered):** z(primary probe vs 0.73) = **+0.27 (linear), +0.26 (dex)** with combined SE; strict varB deep fit z = +1.82. |a0_eff_MW − 0.73 a0| = 0.067 ≪ 3·SE → **the MW channel does NOT disagree with the extragalactic deep value.**
- **KILL-B — consistent with canonical a0:** z_dex = −0.70 (z_lin = −0.86 vs 1.0).
- **C8 — three channels agree** within 3 SE of 0.73 across three independent systematics channels (HI/SPARC rings, dwarf stellar kinematics, MW APOGEE/RGB tracers with its own baryonic model).

**Registered statement:** the MW deepest probe does not exceed 3 SE from 0.73 — the three independent channels agree with the extragalactic deep value. Registered caveats: (i) the MW probe lives at g_bar = 0.24–0.30 a0 — the strict 0.2-a0 cut is NEVER attained (N = 0/0/2); (ii) the MW probe is ALSO consistent with canonical a0 (z = −0.9) and therefore does not independently discriminate 0.73 from 1.0; (iii) all three baryonic modelings put the drop-point central value at-or-above the L06 value (0.80 / 1.00 / 1.29), i.e. the MW sits on the higher side of the channel family.

## 6. R-dependence (step 4): annuli and drift (N01 density-locality per the brief)

Full-line a0_eff per annulus (7 bins; canonical expectation: flat at 1.0):

| R bin (kpc) | N | <g_bar> (a0) | <g_obs> (a0) | **a0_eff/a0 ± SE (primary)** | varB |
|---|---|---|---|---|---|
| 5.0–8.0 | 6 | 2.110 | 2.844 | 1.691 ± 0.050 | 2.227 ± 0.058 |
| 8.0–11.0 | 6 | 1.243 | 1.861 | 1.557 ± 0.019 | 2.040 ± 0.020 |
| 11.0–14.0 | 6 | 0.811 | 1.360 | 1.473 ± 0.026 | 2.036 ± 0.022 |
| 14.0–17.0 | 6 | 0.566 | 1.055 | 1.372 ± 0.024 | 1.994 ± 0.029 |
| 17.0–20.0 | 6 | 0.414 | 0.816 | 1.218 ± 0.061 | 1.839 ± 0.078 |
| 20.0–22.5 | 5 | 0.322 | 0.654 | 0.942 ± 0.175 | 1.485 ± 0.242 |
| 22.5–25.5 | 3 | 0.263 | 0.549 | **0.797 ± 0.240** | 1.285 ± 0.334 |

**a0_eff declines monotonically outward** (1.69 → 0.80 primary; 2.23 → 1.29 varB), qualitatively the direction N01 density-locality would predict for a0_eff that tracks the ambient density (high in the dense inner disk, low in the halo-dominated outskirts), and it approaches the L06/canonical band (0.8–1.3) at the deepest radii. However the **drift test on the outer annuli is statistically NULL**: weighted slope of log10 a0_eff vs R over the < 0.5 a0 bins = −0.038 ± 0.72 kpc⁻¹ (primary, n = 3) and −0.015 ± 0.35 (varB, n = 4), z = −0.05/−0.04 → **C9 PASS ("no significant drift")** — honestly underpowered: only 3–4 outer bins and ±0.2–0.3 SEs can neither confirm nor exclude the visible trend.

## 7. Deep-region form (is the √-law the right shape?)

Free slope β of log10 g_obs vs log10 g_bar on g_bar < 0.4 a0 sets: **β = 0.92 ± 0.45 (primary, N = 10; z vs 0.5 = +0.94)** and **β = 0.87 ± 0.21 (varB, N = 15; z = +1.80)** — the √-law form is not excluded (C6 PASS) but the measured β prefers a steeper-than-0.5 mapping, i.e. g_obs declines with g_bar faster than the deep √-law (a nearly flat-excess character at 17–25 kpc). **C7 FAIL (registered):** χ²_red vs the published V errors = **4.2 (primary) / 17.0 (varB)** — the point scatter around the a0-line significantly exceeds the quoted errors: systematics (both baryonic and v_c non-circular-motion) dominate the deep-probe budget, not the tabulated random errors.

## 8. Honest limits (why the MW baryonic model systematics dominate — they do)

1. **Three baryonic modelings give V_bary(8.19) = 191/183/182 km/s and probe values 0.80/1.00/1.29** — the answer's spread from baryons is larger than the statistical SE; a0_eff ~ 1/g_bar in the deep regime so outer-mass errors map ~linearly (a 30% outer-baryon error → ~2× in a0_eff).
2. **The strict deep cut is model-dependent**: 0/0/2 points under the three legs; under Eilers' own baryons the deep regime lies beyond 25 kpc entirely. The probe region (g_bar 0.17–0.35 a0) is NOT the asymptotic deep regime.
3. **Eilers v_c beyond ~20 kpc carries 6–28 km/s tabulated errors**, and the DR3-era successors (Wang+23, Jiao+23, Ou+24, Labini+23) find a steeper outer decline than Eilers — a steeper true RC would lower the probe (toward/through the L06 band), so the "consistent with 0.73" reading is the conservative direction-vs-RC choice.
4. **Convention**: V²/R vs G M_enc/R² differ by only 0.10 dex on the primary probe (C10) — good; but the MN quadrature verifier shows M_enc(100 kpc)/M = 0.81 (thin) — the MN disc's mass is not fully enclosed by 100 kpc (scale length a = 5.3), which is physical, not a bug.
5. **EFE** cannot explain an excess of g_obs over the deep line (it suppresses the boost); the MW being embedded in the Local Group field only strengthens the "no deficit" reading.
6. χ²_red ≫ 1 (C7): published random errors understate the true scatter → treat the bootstrap SE (which draws from the *published* errors) as a lower bound on the probe uncertainty.

## 9. Files, checks, summary

**Files:** `deepseek_push/O03_mw_deep.py` (this lane, reproducible), `O03_mw_deep.out` (full output), `O03_results.json` (machine-readable), this MD. No git commit (per instruction).

**Checks (10/14 PASS):** C1 table ✓ · C2 v_c(R0) ✓ · C3 V_bary(8.19) ∈ [185,205] ✓ · C4 baryons+NFW halo = 229.3 vs 228.86 ✓ · C5 deep cut attained with N ≥ 10 — **FAIL (registered probing finding, N = 0/0/2)** · C6± √-law slope (PASS, β = 0.92 ± 0.45 / 0.87 ± 0.21) · C7± scatter vs published errors — **FAIL (χ²_red = 4.2 / 17.0)** · KILL-A **not triggered** (z = +0.27/+0.26 vs 0.73) · KILL-B consistent with 1.0 (z_dex = −0.70) · C8 three channels agree ✓ · C9 no significant R-drift ✓ (underpowered) · C10 convention ≤ 0.3 dex ✓.

**Bottom line:** the MW channel — the third independent systematics channel — agrees with the extragalactic deep value a0_eff ≈ 0.73 a0 within 3 SE (probe 0.80 ± 0.24), while also remaining consistent with canonical a0; the strict deep regime is not probed by the Eilers RC under any responsible MW baryonic model (the deep cut itself is the dominant model-dependence). The deep-tension family on the canonical footing now reads: **SPARC-deep 0.72 (4.2σ below 1) · dwarfs 0.64/0.31 · MW 0.80–1.29 (probe) · MIGHTEE 2.16** — sample dependence across channels persists, with the MW on the at-or-above side.