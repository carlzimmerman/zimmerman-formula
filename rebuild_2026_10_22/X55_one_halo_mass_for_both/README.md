# X55_one_halo_mass_for_both: no single route-E halo-mass relation fits both SPARC and the KiDS isolated lenses (CONTRADICTION, 4.6σ / 4.3σ)

Criteria and ledger: `FROZEN_CRITERIA.md`, `ASSUMPTION_LEDGER.md` (32f994b55e, committed alone; they include the
coordinator's informativeness condition and saturation counts). No amendment. κ = ½ FITTED. Footings never pooled. Route
E's halos are cold dark energy, not matter. No dark-matter particle. Not "theory closed". Nothing here says the data favour
the framework.

**Question.** X53 found that KiDS lenses want route-E halos about 0.35–0.5 dex heavier than EM1's SPARC relation. Is there
one relation log M200 = a + b (log M_b − 10.5) that fits both data sets?
- **SPARC:** a₀/(2πG) Burkert floor, X38's machinery, Υ free per galaxy, X38's line; uncertainty by galaxy bootstrap.
- **KiDS:** B21 isolated lenses, exactly X53's (H2H): X43 core rule with c_f = 4, R200 truncation, CFG805 two-halo term.
  The regions are Birge-scaled, which widens them and so favours finding one relation.
- Masses are framework-native: (a, b) are fitted, with no abundance matching and no c(M).

## Verdict (frozen rule): **CONTRADICTION**, both footings

**This test finds that route E's SPARC halos and its lensing halos cannot share one mass relation.** The relation that
fits the rotation curves sits about 0.4 dex below the one the lenses want, at the same baryonic masses.

| | canonical | alt |
|---|---|---|
| SPARC best (a, b) | 11.70, 0.90 (rms 0.0790, Υ 0.76) | 11.66, 0.92 (rms 0.0728, Υ 0.60) |
| SPARC bootstrap sd a / b (corr) | 0.035 / 0.046 (+0.26) | 0.043 / 0.051 (+0.47) |
| SPARC 2σ box: a / b | 11.62–11.78 / 0.80–1.00 | 11.56–11.76 / 0.80–1.04 |
| KiDS best (a, b), all radii | 12.12, 0.92 (χ² 242.0 / 54, s_K 4.48) | 12.10, 0.98 (χ² 254.0 / 54, s_K 4.70) |
| KiDS 2σ box: a / b (Birge) | 11.96–12.24 / 0.56–1.36 | 11.94–12.24 / 0.60–1.42 |
| KiDS 2σ box, unscaled | 12.06–12.18 / 0.74–1.10 | 12.04–12.16 / 0.80–1.16 |
| **n_sep (line-passing nodes)** | **4.55σ** | **4.26σ** |
| n_sep with KiDS unscaled | 6.72σ | 6.15σ |

- In EM1's convention (pivot 10), SPARC's floor-Burkert fit is a = 11.25, b 0.90. EM1's NFW + Bullock value is 11.18.
- The rows above are the ranges of the elliptical 2σ regions, not the regions themselves. The full regions are in
  `x55_one_halo_results.json`.

**log M200 at the four lens-bin mean M_b** (10.19 / 10.60 / 10.80 / 10.96):

| | bin 1 | bin 2 | bin 3 | bin 4 |
|---|---|---|---|---|
| SPARC, canonical (bootstrap median; 68 % width) | 11.42 (0.07) | 11.78 (0.08) | 11.96 (0.07) | 12.11 (0.09) |
| KiDS, canonical (best; 68 % Birge range) | 11.83 (11.73–11.92) | 12.21 (12.16–12.25) | 12.39 (12.35–12.43) | 12.55 (12.50–12.59) |
| SPARC, alt | 11.37 (0.08) | 11.74 (0.09) | 11.93 (0.10) | 12.08 (0.12) |
| KiDS, alt | 11.80 (11.70–11.90) | 12.19 (12.14–12.24) | 12.39 (12.35–12.43) | 12.56 (12.50–12.60) |

- **Informativeness (frozen, coordinator):** SPARC's 68 % width at the lens masses is 0.07–0.12 dex in every bin, well
  under 0.30. So SPARC does pin M200 there; the disagreement is not "SPARC can't tell".
- **There is no joint relation.** The closest line-passing compromise is reported, not endorsed:
  - Canonical: (11.86, 1.02). SPARC rms 0.0821, Υ 0.77, 4.46σ from SPARC's best; KiDS χ² 350.7, 4.55σ.
  - Alt: (11.86, 1.04). SPARC rms 0.0782, Υ 0.60; KiDS χ² 352.9.
  - The law, for comparison: SPARC rms 0.0541 / 0.0537; KiDS L2H all radii χ² 154.3 / 125.1 (L 160.7 / 127.6).
- **Read X38's line with care.** At the KiDS best relation, SPARC still passes X38's coarse line: rms 0.0918 / 0.0906,
  Υ 0.78 / 0.61. That relation is only excluded statistically, at 12.2σ / 10.8σ by bootstrap. In the other direction,
  KiDS at SPARC's best relation is 7.6σ (Birge-scaled).
- **Saturation (coordinator):** none.
  - SPARC: 0 galaxies saturated at the SPARC best fit, the KiDS best fit or the compromise.
  - KiDS: 0 lens weight in any bin.
  - No node inside either 2σ region saturates.
  - The floor-only SPARC halos saturate only above log M200 14.65 (canonical) / 14.9 (alt), reached on 4162 / 2953 of
    30351 grid nodes, all far from both regions. With the X43 rule, the KiDS halo table never saturates on 8–15.

## Reported variants (not graded)

| variant | n_sep canonical | n_sep alt |
|---|---|---|
| lens M★ −0.15 dex | 6.29 CONTRADICTION | 5.83 CONTRADICTION |
| lens M★ +0.15 dex | 2.72 TENSION | 2.57 TENSION |
| KiDS R ≤ 0.31 Mpc only (leakage test i; one-halo) | 3.63 | 3.14 |
| outer data × 0.64 (F2 GAMA/KiDS; leakage test ii) | 4.97 | 4.51 |
| untruncated halos (100 R200) | 4.85 | 4.43 |
| SPARC with the X43 rule (c_f 4) | 2.91 | 4.07 |

- **Lens stellar masses.** Only heavier lens M★ (+0.15 dex) brings the separation down, and only to TENSION. A further
  shift would be needed to reach 2σ.
  - The mass definitions differ (ledger A2/A3). SPARC's relation variable uses Υ = 0.5, while the fitted median Υ is
    0.76 canonical.
  - Putting SPARC on its fitted Υ would raise its M_b, and so move SPARC's M200 at fixed M_b lower still. That widens
    the gap.
- **Isolation leakage does not close the gap.** Neither test removes it:
  - Inner radii only: the separation falls to 3.6σ / 3.1σ.
  - Scaling the outer signal down to GAMA's spectroscopic level: 5.0σ / 4.5σ.
- **Restricted overlap.**
  - The lenses' 5–95 % range is log M_b 10.14–11.02, which holds 39 SPARC galaxies. Refitting SPARC on those alone gives
    (11.70, 0.82) canonical and (11.68, 0.78) alt, with b poorly fixed (bootstrap sd 0.37 / 0.46).
  - Against KiDS on all radii: n_sep 3.07 (CONTRADICTION) / 2.67 (TENSION).
  - Against KiDS on R ≤ 0.31 Mpc only: 2.27 / **1.87**. This is the one reported combination that reaches the 2σ
    overlap, on alt only.
  - The subset's M200 at the lens-bin masses stays 0.37–0.55 dex below KiDS's best in every bin.

## Systematics and limits

- **KiDS errors.** (H2H) fits badly in absolute terms (χ²/dof ≈ 4.5), so the Birge scaling makes the KiDS regions about
  2× wider. Without it, the separation grows to 6.2–6.7σ.
- **SPARC errors.** SPARC's errors come from the galaxy bootstrap, a Gaussian approximation. No bootstrap fit landed at
  the grid edge. The relation has no intrinsic-scatter term (ledger A1).
- **Inherited from ΛCDM.** The two-halo template uses ΛCDM-inherited initial conditions (CFG805; b_eff absorbs its
  amplitude). Nothing ΛCDM-derived sets the halo masses. EM1's reference (11.18, 0.90) used Bullock c(M); here it serves
  only as step 0.
- **Mass definitions.** M200 is taken at 200 ρ_crit,0 with background A's h for both data sets. The lenses sit at
  z ≈ 0.2–0.3; X53's variant at ρ_c(z_eff) moved Δχ² by about 10.

## What it means

- Route E with a₀-floor Burkert halos needs lens halos about 0.4 dex heavier than SPARC halos at the same M_b. The SPARC
  side is now measured to ±0.04 dex, so this is an internal contradiction between route E's dynamics and its lensing.
  It is not an artefact of EM1's borrowed relation.
- This test strengthens X53's reading: its normalisation gap cannot be removed by re-choosing the relation. The profiled
  A1 numbers are what route E gets only if it is allowed a lensing-only mass relation.
- The ways out still open:
  - lens M★ systematically about 0.2+ dex heavier than LePhare + 0.15;
  - a mass-dependent environment or selection effect on the "isolated" lenses beyond F2's leakage proxy;
  - halo physics that differs between SPARC discs and KiDS lenses.

## Checks and MUTATE

- **Step 0: PASS.**
  1. X53's L / H / L2H / H2H χ² match the committed values within 0.05 (both ranges and footings).
  2. A1's common shifts (+0.35 / +0.50) and their χ² (56.95 / 242.15 canonical, 67.25 / 254.92 alt) are reproduced with
     the halo table.
  3. EM1 rerun unchanged in a scratch copy gives (11.18, 0.90) bg A and (11.20, 0.90) bg B, rms 0.06557 / 0.06546
     (`x55_step0_em1.py`).
  4. X38's SPARC row is reproduced: 0.0795 / 0.77 and 0.0729 / 0.60, 0 saturated.
- **Main run: 10/10 PASS.** K0_X53, K0_EM1, K0_A1, K0_X38 (×2), K_NNLS (vectorised b_eff ≥ 0 fit = X53's `fit` to 1e-6),
  K_TAB (×2; table vs X53 `stack_H` within 0.006), K_BOOT, and K_R (0.98 GB).
  - A first run exceeded 1 GB and failed K_R; its physics numbers were identical.
  - The SPARC node tables were then built in galaxy chunks. No number changed.
- **MUTATE** (`X55_MUTATE=1`, lens M★ +1 dex): K0_X53 and K0_A1 FAIL (A1's best shift goes to the grid edge −0.30,
  χ² 1428–1609). The class becomes UNDECIDED (step 0 failed), and the run exits 1.
- **Resources.** One thread, nice 15, about 65 s per run plus 64 s for the EM1 rerun. Nothing downloaded, and nothing
  written outside this folder except the removed scratch copy.

## Files

- `x55_step0_em1.py`, `.out`, `_results.json` (step 0 item 3)
- `x55_one_halo.py`, `.out`, `_results.json`, plus the `_MUTATE` outputs

        PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x55_step0_em1.py
        PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x55_one_halo.py               # exit 0, 10/10
        X55_MUTATE=1 PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x55_one_halo.py  # exit 1
