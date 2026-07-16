# FROZEN CUTS — Jeanneau+26 (MUSE-DARK II) low-acceleration bTFR refit (Lane D/E)

**FROZEN 2026-07-16, BEFORE any per-galaxy number from Jeanneau+26 was read.**
This file defines the selection, the zero-point estimator, and the error model. It is written
first so the acceleration cut and the estimator cannot be tuned to the answer. Parent context:
`prep_2026/highz_tfr_fork/{DATA_LEDGER.md,FORK_RESULTS.md,fork_confrontation.py}` (Lane C/D found
the full-sample z≈1 bTFR is UNDERPOWERED: 0.00±0.27 honest band vs a diluted fork separation
≤0.14 dex; the one in-hand lever is this low-acceleration-third refit).

## 0. Footings (both run, each with ITS OWN a0)
- **CANONICAL**: `a0_canon = cH_Λ/Z = 9.36e-11 m/s²` (from ρ_DE). `a0(z)/a0(0) = sqrt(f_DE(z))`;
  EXACTLY constant under pure Λ (w=−1); mildly declining under DESI DR2 CPL (w0=−0.752, wa=−0.86).
- **ALT**: `a0_alt = 1.13e-10 m/s²` (ρ_total/cH0 branch). `a0(z)/a0(0) = E(z)`, RISING.
Machinery identical to `prep_2026/highz_tfr_fork/fork_confrontation.py` (E(z), f_DE, ν, size term
all re-imported/re-asserted against the banked anchors before any refit number is printed).

## 1. Acceleration cut (THE selection — frozen)
- **Estimator.** For each galaxy compute the observed (total) acceleration at the outermost
  GalPaK3D velocity point:
  `g_obs = v_c(R_out)^2 / R_out`, with `v_c` the inclination-corrected circular velocity Jeanneau
  report at their velocity radius and `R_out` the radius at which that velocity is quoted
  (Jeanneau quote v_c at ~1.8–2 R_e; **R_out = the radius of the quoted velocity = 2·R_e using the
  GalPaK3D fitted disc scale R_e**; if the table gives v_c already at a stated radius, use that
  radius verbatim). Then invert the framework's OWN interpolation
  `g_obs = sqrt(g_bar² + g_bar·a0)`  →  `g_bar = 0.5(−a0 + sqrt(a0² + 4 g_obs²))`,
  evaluated with `a0 = a0_canon = 9.36e-11` (the cut is defined on the canonical footing so the
  SAME galaxies are selected regardless of which footing is later tested — the cut must not depend
  on the hypothesis under test).
- **Justification of v²/R over G·M_bar/R².** The cut uses only the two cleanest measured quantities
  (v_c, R_e); it does NOT use the model-mediated baryonic mass (Tacconi+20 molecular + NUM HI, 0.8
  dex scatter), which would inject that scatter into the selection itself. g_obs=v²/R is the
  rotation-supported total acceleration; inverting through ν gives the baryonic g_bar the fork
  cares about. (Secondary cross-check only, NOT the selection: direct g_bar = G·M_bar/R_e² — report
  the overlap, do not re-select on it.)
- **THE CUT:** keep galaxy iff `g_bar < 0.5 · a0_canon = 4.68e-11 m/s²`.
  (Equivalently g_obs < sqrt(0.25 + 0.5)·a0 = 0.866·a0_canon = 8.11e-11 m/s².)
- **Deep-regime rationale (why 0.5 a0).** At g_bar < 0.5 a0 the framework's linearized dilution
  x/(2+x) with x=a0/g_bar > 2 exceeds 0.5 (→ >50% of the deep-MOND a0-lever survives); the size
  term (M=v²R/G, Newtonian) cancels because the regime is deep-MOND (M=v⁴/(G a0), R-independent).
  At this cut the exact per-galaxy ALT prediction is ≈ −0.15…−0.20 dex while canonical stays ≈0.

## 2. Secondary cuts (Jeanneau's OWN quality flags ONLY — no new cuts invented)
Apply, in this order, ONLY the quality flags Jeanneau+26 themselves define for their fiducial bTFR
sample (whatever the machine-readable table exposes — to be recorded verbatim in DATA.md):
- their rotation-dominated / disc flag (v/σ or "regular rotator" flag) as used for their fiducial
  bTFR fit;
- their inclination validity range (drop face-on/edge-on beyond their stated i limits);
- their lens-model / magnification quality flag if one is tabulated;
- their bTFR-sample membership flag (galaxies they themselves include in the 0.00±0.06 fit).
NO acceleration-independent mass, redshift, or size cut beyond the above is added by us.

## 3. Zero-point estimator (frozen)
Observable = `Δb` = bTFR offset along the MASS axis at fixed velocity vs the local reference, dex
(same convention as the parent ledger). Local reference = **Lelli+19 bTFR, slope 3.14**
(log M_bar = 3.14·log V_c + A_L19; the exact intercept Jeanneau adopt is read from their paper and
recorded in DATA.md — the SAME reference they use for their full-sample 0.00±0.06).
- **PRIMARY:** fixed-slope-3.14 median offset.
  `Δb = median_i [ log10 M_bar,i − (3.14·log10 V_c,i + A_L19) ]` over the low-acceleration subsample.
  Median (not mean) for outlier robustness; report N, MAD, and bootstrap CI.
- **SECONDARY (check only):** free-slope orthogonal fit to the subsample; report slope and the
  intercept-at-pivot offset. If the free slope differs from 3.14 by >2σ, flag it (the ZP-vs-slope
  covariance is a known high-z systematic) but the PRIMARY fixed-slope number is the headline.
- **Velocity definition:** V_c = the same GalPaK3D circular velocity Jeanneau use in their fiducial
  bTFR (pressure-support / Dalcanton-Stilp corrected as they apply it). Do not re-derive it.

## 4. Error model (frozen — added in quadrature unless stated)
Per-subsample honest band on Δb:
- **stat**: bootstrap the median offset over the subsample galaxies (resample with replacement,
  10⁴ draws) → 68% CI. This carries the small-N penalty of the deep cut automatically.
- **gas-model systematic**: **±0.20 dex** flat (Tacconi+20 molecular scaling + NeutralUniverseMachine
  HI, 0.8 dex per-galaxy scatter → the SAMPLE-MEDIAN systematic band the parent ledger carries; the
  0.8 dex per-galaxy is NOT divided by √N because it is a coherent scaling-relation offset, not
  independent noise — frozen as ±0.20 on the median, matching the parent's Jeanneau row budget).
- **local-reference ZP**: **±0.16 dex** (Lelli+19 bTFR intercept uncertainty).
- **velocity-convention**: **±0.06 dex** (Jeanneau's own robustness-scan spread over velocity
  definition / v-σ cut / slope).
- **magnification (per-galaxy, deep-third-specific)**: propagate each galaxy's lensing-magnification
  uncertainty σ_μ into a mass error δlogM = δμ/(μ ln10) (M ∝ 1/μ), then into the median via the
  bootstrap (include per-galaxy logM magnification error in the resampled offsets). The faint
  low-mass third is the most magnification-sensitive; if σ_μ is not tabulated per galaxy, use
  Jeanneau's stated global magnification-error prescription and record that fallback in DATA.md.
- **HONEST BAND** = sqrt(stat² + 0.20² + 0.16² + 0.06²) with magnification folded into stat.

## 5. Decision rule (frozen — verdict is mechanical, not chosen after seeing the number)
Let S = |Δb_subsample|, B = honest band (§4), and the diluted fork separation at the subsample's
median redshift/acceleration be Δ_canon(≈0) vs Δ_ALT (exact per-galaxy, framework ν, each footing's
own a0; typically −0.15…−0.20 at this cut). Then:
- **ALT-side constraint** iff the subsample is consistent with canonical (|Δb − 0| < B) AND
  inconsistent with ALT at ≥1σ (|Δb − Δ_ALT| > B): report "first published-data constraint on ALT,
  N.Nσ" with the exact σ.
- **ALT-side lean (not a constraint)** iff |Δb−0| and |Δb−Δ_ALT| are BOTH < B but Δb sits closer to
  canonical: report lean + σ, explicitly UNDERPOWERED.
- **ALT-favored** iff Δb sits at/below Δ_ALT within B and away from 0: report straight (a manufactured
  ALT-kill is as bad as a manufactured save — if the deep third leans ALT, SAY SO).
- **STILL-UNDERPOWERED** iff B > |Δ_ALT| (the honest band exceeds the fork separation): report that
  the deep cut did not deliver the forecast power — the test remains a wash. **This is a live
  outcome; the gas-model ±0.20 alone nearly equals the fork separation, so underpowered is likely.**
- If deep-cut N is much smaller than ~⅓·95 (say N≲8): flag the test as weaker than forecast
  regardless of central value; bootstrap CI is the arbiter.

## 6. ΛCDM-degeneracy (mandatory — what the deep cut CAN and CANNOT say)
The parent found the fork is footing-INTERNAL only (canonical vs ALT), NOT an MI-vs-ΛCDM
discriminator, because ALT's −log10 E(z) tracks the standard halo-scaling drift
−log10[E(z)·sqrt(Δc(z)/Δc(0))] to <0.12 dex. **Check whether the deep cut changes that.** The size
term cancels in deep-MOND, but the ΛCDM halo-scaling drift does NOT cancel (it is a mass-assembly /
gas-fraction effect, not a size effect). Compute the ΛCDM halo term at the subsample median z and
compare to Δ_ALT: if they still track, the deep cut constrains ALT-vs-canonical INTERNALLY but
remains ΛCDM-degenerate — state that explicitly. The deep cut buys fork power (canonical vs ALT),
NOT MI-vs-ΛCDM discrimination.

## 7. Frozen constants
```
a0_canon = 9.36e-11 m/s^2   ;  a0_alt = 1.13e-10 m/s^2
cut: g_bar < 0.5*a0_canon = 4.68e-11 (g_bar from inverting g_obs=v^2/R through framework nu)
slope = 3.14 (Lelli+19 bTFR)   ;  size alpha = 0.75 (van der Wel+14, only for the cross-check)
Om,OL = 0.315,0.685  ;  CPL w0,wa = -0.752,-0.86 (DESI DR2)
gas-model sys = 0.20 ; local-ref sys = 0.16 ; convention sys = 0.06 (dex, quadrature)
bootstrap draws = 1e4
```
END FROZEN CUTS.
