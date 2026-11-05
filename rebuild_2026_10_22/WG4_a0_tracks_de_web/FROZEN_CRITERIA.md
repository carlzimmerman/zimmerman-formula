# WG4_a0_tracks_de_web: FROZEN CRITERIA, committed alone before any script or number

**Not blind.** These results are known:
- **WG2** (6856666719, under its post-result A2), with **a0 flat**:
  - law off: r 0.0002-0.31;
  - QUMOND on the web: r 11-14 with the measured-style expansion, 560-660 with baryons alone in the expansion.
- **WG3** (d4d81be402): the record's bound-only switch never turns on and fails low.
- **WG3's reported T1τ0:** a uniform halving of the phantom lands at r 1.3-1.9 with the measured-style expansion. So a factor of about ½ in the web phantom would land.
- **The DESI DR2 CPL a0(z) is known**, computed with a0kit before this file:
  - 0.87 at z 2, 0.45 at z 10, 0.17 at z 50;
  - phantom ∝ √a0 in the deep regime, so the phantom is about 0.67 at z 10 and 0.41 at z 50.

κ = ½ FITTED. The cold sector stays retired. No particle and no cold component is added. Not theory closed. Nothing here says the data favour the framework. No downloads.

**Owner 2026-11-04,** on WG3's open lead (a factor of about ½ on the web that "has to come from the theory"): "okay work on this then".
- **Standing owner rule** (feedback, 10-06): a0 tracks the dark-energy density over time, a0(z) = κ c √(G ρ_DE(z)). "Flat a0" is only the w = −1 case.
- **WG2 ran only that special case.** This lane runs the framework's own law with evolving dark energy. No new parameter is introduced.

## Question
With a0(z) = a0(0) √(ρ_DE(z)/ρ_DE0), does the law alone from WG2's baryons-only start, under QUMOND on the web, give the CMB-lensing amplitude Planck PR4 measures?

## Inputs
- **ρ_DE(z):** a0kit's CPL form, `rho_de_ratio(z, w0, wa)`, with DESI DR2 (w0, wa) = (−0.838, −0.62). These are the record's values (CFG359 A0-DE, chart_a0z_one.py).
  - **Caveat:** that CPL fit is a CDM-family fit, and its use beyond z 2.33 is the CPL form extrapolated, not measured. This is stated in every label.
- **Rules (all R1: QUMOND on the peculiar field, simple ν, WG2's engine imported read only):**
  - **DE (primary):**
    - a0 = a0_foot √(ρ_DE,CPL(z)/ρ_DE0);
    - the expansion carries the same CPL dark energy;
    - backgrounds B2D (WG2's B2 with CPL in place of Λ) and B1D (WG2's B1 with CPL).
  - **DE-a0only (reported):** a0 as DE, expansion with Λ (WG2's B2). This is CFG359's convention, whose inconsistency CFG359 disclosed.
  - **NATIVE-LOW (reported bracket):** a0(z)/a0(0) at the record's native CFG689 band lower 68 % edge (1, 0.76, 0.71, 0.33 at z 0, 1, 1.5, 2.33), held at 0.33 beyond, on B2. This is the lowest a0 history the native band allows at 68 % without extrapolating a fit form.
- **Everything else is WG2's:**
  - ICs from CLASS at z_on 50; at z 50 the CPL and Λ dark energy are both under 1e-4 of the matter, so B2D uses B2's ICs and B1D uses B1's;
  - box, steps and snapshots;
  - projection with χ(z) from each run's own E(a);
  - PR4 grading and r.

## Run matrix (canonical, 128³, 200 steps, z_on 50 unless stated)
- **DE:** {B2D, B1D} × A_s {1e-9, 4e-9}. 4 runs.
- **DE-a0only:** B2 × A_s {1e-9, 4e-9}. 2 runs.
- **NATIVE-LOW:** B2 × A_s {1e-9, 4e-9}. 2 runs.
- **Checks:** DE B2D A_s 2.1e-9 at 128³ (reference) and 192³ (K5); DE B2D A_s 2.1e-9 alt footing. 3 runs.

## Labels
- **Thresholds (WG2's):** FAILS LOW if r < 0.5; FAILS HIGH if r > 2; WITHIN ×2 if 0.5 ≤ r ≤ 2. AMPLITUDE PASS also needs |r − 1| ≤ 0.056 and an unscaled χ² with p ≥ 0.001.
- **Primary label:** the DE rule on B2D over its two A_s members.
  - B2D is primary because PAPER67's law takes the measured expansion, which carries the smooth matter term.
  - The four-member label (B1D + B2D, as WG2 and WG3 used) is also reported.
- **If the primary reads WITHIN ×2,** the record line is "IN RANGE when a0 tracks DESI DR2's evolving ρ_DE (CPL extrapolated beyond z 2.33)". It counts only if:
  - K5 gives the same label;
  - all K checks pass;
  - the alt footing is reported beside it.
  - It is not a CMB pass, because the primary CMB still has no fit without dust.
- **If it FAILS,** the record line is "a0 tracking DESI's evolving dark energy does not close the gap", with the side stated.
- **DE-a0only and NATIVE-LOW** are reported with per-run labels.

## Checks (all must PASS before any label is read)
- **WG2's K1, K2** on the imported engine.
- **K3 (Limber)** and **K4b (ICs, ratio of summed power, 10 %)** on the DE B2D A_s 2.1e-9 128³ run.
- **K9, code test:**
  - (a) the DE a0 at z 2 equals a0kit `a0_of_z(2, −0.838, −0.62)/a0(0)` to 1e-9;
  - (b) B2D's E(z = 0) = 1 to 1e-9;
  - (c) with (w0, wa) = (−1, 0), B2D's E(a) equals B2's at z 0, 1, 10 and 50 to 1e-12.
- **MUTATE:** WG2's Poisson-halved K1 must FAIL. Outputs carry `_MUTATE`.

## What this lane can't say
- Everything WG2 can't say: 12.5 h⁻¹ Mpc mesh, no primary-CMB test, A_s bracketed, lensing assumed to see the dynamical potential.
- The CPL form beyond z 2.33 is an extrapolation of a fit, not a measurement. The native band ends at z 2.33.
- A pass on the primary would tie the CMB-lensing amplitude to dark-energy evolution at z > 2.33 that nothing has measured. It would be a prediction to test, not a confirmation.
- Nothing here reinstates the cold sector.

## Output
- `wg4_pm.py`: wraps WG2's engine and adds the DE and NATIVE-LOW a0 rules, the B2D/B1D backgrounds and K9.
- `wg4_run_all.py`: the 11 runs.
- `wg4_grade.py`: copies WG2's projection and grading; writes `wg4_results.json` and `wg4.out`. MUTATE writes `_MUTATE`.
- `README.md`.
