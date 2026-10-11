# CFG625 FROZEN CRITERIA: merger baryon-input sensitivity (CFG623 rerun with data-based progenitor baryons)

Date: 2026-10-11. Written and committed ALONE, before any CFG625 run, any CFG625 static profile number and any CFG625 scoring.
Nothing below may be edited after this commit; later changes go in dated disclosures in the README.

κ = ½ is fitted. The cold energy's mass is still required (an input). No dark-matter particle is added. The theory is not closed.
Yardsticks are raw data only: no ΛCDM halo or baseline, no MOND force law. Nothing here will be phrased as "the data favour the
framework". Both footings (9.36e-11 canonical, 1.13e-10 alt) are kept and never pooled.

## 0. What has already been seen (stated before any choice below)

- CFG621's, CFG622's and CFG623's criteria, results, README tables and disclosures (CFG623 c7669aef1: VALID; allowed {0} on both
  footings; α 0.1, 0.3, ∞ EXCLUDED; α 0.03, 1, 3, 10 UNSCORABLE; V-1 EXCLUDED, V-2 ALLOWED, V-3 INCOMPATIBLE (literal), V-4
  "collisionless component that re-settles slowly"; α = 0 Bullet stable at the minimum 3/4 majority; α = 0 Harvey pass depends on
  the d_SG ≥ 200 kpc window).
- CFG623's step-1 mechanism test (1539fd142): the early α = 0 lensing–gas offset is mostly the cool-core cloud acting on a FLAT
  cold-energy core; a cuspier cold-energy core (NFW c = 10) removed it. This is why the baryon inputs, which set the cold-energy
  (phantom) core shape, are the question of this lane.
- The orchestrator's static t = 0 numbers for CFG623's progenitors (case L): projected M(<250 kpc) main 8.3e13 (can) / 8.9e13
  (alt), sub 3.2e13 / 3.5e13, versus the Paraficz+16 strong-lensing 2.5e14 / 2.0e14 quoted in CFG597 D1 (recalled, PROVISIONAL).
- The record's hunt item 57 (`hunt_2026/h57_bullet_peaks.py` / `.out`): with Famaey (2026) Plummer baryons the kernel gives
  2.6–3.1× the projected baryons at the galaxy peaks while the lensing (Rihtarsic+26 via Famaey) needs 8.3–9.8× (shortfall
  factor 3.17 / 3.15, canonical).
No α-dependent CFG625 number exists. The variants below are fixed from published measurements as the record transcribes them and
from declared brackets; none is chosen by which α it would favour.

## 1. Measured baryon inputs (sources on disk; nothing downloaded)

- **[F26] Famaey (2026), arXiv:2605.10022, Table 1**, as transcribed in `hunt_2026/h57_bullet_peaks.py` (lines 45–48; the record
  says it was read from the paper's HTML and checked: the transcription reproduces the paper's projected baryons at BCG1/BCG3 to
  −8.6% / −3.7%). Plummer components (mass M, scale a, position relative to BCG1, kpc), today's configuration:
  - galaxies: main 1.196e13 M☉, a = 470 kpc at BCG1; sub 4.0e12 M☉, a = 245 kpc at BCG3 (820, 220);
  - gas: main 2.0e14, a = 565 at (190, 90); 1.5e13, a = 505 at (525, 120); bullet 1.5e13, a = 90 minus 6.8e12, a = 70, both
    at (670, 170) (net 8.2e12, a cored cloud; the difference density is positive at every r because a = 90 > 70 and the centre is
    positive).
- **[C06] Clowe et al. 2006 Table 2** (`opus_48_extended_research/reviews/bullet/bullet_data_table.py`, verbatim): 100-kpc aperture
  stellar masses at the BCGs, main 0.54 ± 0.08e12, sub 0.58 ± 0.09e12; plasma 5.5 / 2.7e12 (BCG apertures), 6.6 / 5.8e12 (plasma
  apertures).
- **[P16] Paraficz et al. 2016** strong-lensing M(<250 kpc) main 2.5 ± 0.1e14, sub 2.0 ± 0.2e14 (as quoted in the record;
  recalled, PROVISIONAL). **[R26] Rihtarsic+26 via F26 via h57**: projected M(<300 kpc) BCG1 3.5e14, BCG3 2.3e14 (PROVISIONAL).
  These lensing numbers are used only for the M-RAW mass report (§4), never in an α verdict.
- **Not on disk:** a measured BCG effective radius for either Bullet BCG, and a measured pre-collision (un-stripped) gas profile
  of the sub. Where these are needed a declared bracket is used (B2's R_e) or the F26 present-day decomposition is used as stated.

## 2. The variants (progenitor baryons only; every other model input is CFG623's)

Common rules. r200 and r_t = min(r200, 1200 kpc) keep CFG599's convention (main r_t = 1200, sub r_t ≈ 991 kpc). F26 Plummer
components are placed on the progenitor centre with their F26 central density, truncated at r_t (hard for collisionless
components, CFG599's soft (r/r_t)^−8 steepening for grid gas, 300 kpc for the cloud as in CFG599); the mass beyond r_t is dropped
(it lies outside the box), so the inner profile is the measured one. Phantom (case L) = the round-rule phantom of the
progenitor's own baryons, truncated at r_t, exactly as CFG599 computes it; gas hydrostatic in its own total potential; Jeans
velocities; particle numbers unchanged. The cool-core cloud's drag column Σ_cc = M_cc / (π a_eff²) with a_eff = the cloud's
projected half-mass radius (for CFG599's cloud a_eff = 50 kpc is kept literally).

| variant | stars (main / sub) | gas | cool-core cloud (sub) | M_b |
|---|---|---|---|---|
| BASE (reproduction only) | NFW c = 4, 0.13 M_b | β-model r_c = 0.1 r200, 0.87 M_b | 0.15 of the sub's gas, Plummer 50 kpc | M200/6.73 |
| **B1 measured stellar envelope** | F26 galaxy Plummers: 1.196e13 a = 470 / 4.0e12 a = 245 (truncated) | β-model r_c = 0.1 r200 holding M_b − M_* | as CFG599 (0.15 of gas, 50 kpc) | M200/6.73 (unchanged) |
| **B2 concentrated BCG** | B1 envelope minus the C06 100-kpc stellar mass, plus that mass (0.54e12 / 0.58e12) as a Hernquist BCG with R_e = 30 kpc (a_H = R_e/1.8153 = 16.5 kpc; DECLARED bracket, not measured) | as B1 | as B1 | as B1 |
| **B3 measured gas and stars (all F26)** | as B1 | main: F26 main gas Plummer 2.0e14 a = 565; sub: F26 1.5e13 a = 505 component (assigned to the sub: 312 kpc from BCG3 vs 539 from BCG1) | the F26 bullet gas (1.5e13 a = 90 minus 6.8e12 a = 70), cut at 300 kpc | sum of the components inside r_t (not M200/6.73) |

- B1 tests the stellar SHAPE and the measured stellar-to-gas ratio (F26 total stars/gas ≈ 0.07, vs the provisional 0.15).
- B2 tests the most concentrated stellar reading allowed by the C06 apertures (cuspiest baryon core → cuspiest phantom core).
- B3 tests the gas core and the measured baryon masses. The F26 decomposition is today's (post-collision) configuration; using it
  for the pre-collision sub is a declared approximation (the stripped component and the bullet together stand for the sub's gas).
- M3 roles swapped (MUTATE): the stellar mass and the total gas mass (grid + cloud) of each progenitor are exchanged; every shape
  and the cloud's share of the gas are kept. (For BASE this is CFG599's swap.)
- 50-kpc PM gravity limits how much of B2's 16.5-kpc cusp survives in the dynamics; this is a property of the CFG623 model, stated,
  not fixed here. The lensing maps (12.5-kpc pixels) and the phantom target (12.5-kpc radial bins) do resolve it.

## 3. Unchanged from CFG623 (FROZEN_CRITERIA.md bd135f5c2; code imported read-only)

Simulator and estimator (`cfg622_sim.py`; E-M primary and variants, edge and gas guards 75 kpc); the Bullet statistic f at the
720-kpc epoch; Harvey window t − t_peri ∈ [0.1, 0.6] Gyr AND d_SG ≥ 200 kpc (kept at 200 kpc for every variant, including B3
whose cloud differs); stability rule B-3' (≥ 3 of 4 variants within T_L = 24.90 kpc, plus both guards; T_L not re-derived);
counting rule (≥ 10 stable epochs and ≥ half the window); scores S-1 (Z_B = (f − 0.045)/0.125, Z_H = (β̄ + 0.04)/0.07, no
inflation); S-2 statuses; V-1..V-4 exactly as CFG623's code; the footing-validity rule (α = 0 run in K1 2700 ± 200 km/s and
G1 194 ± 50 kpc); calibration targets K1, G1 and η ∈ [0.1, 2.5]; MUTATE M1 (α = ∞: f ≥ 0.5), M2 (α = 0: |f| ≤ 0.25 AND β̄ ≤ 0.10),
M3 (swapped, α = ∞: f ≤ 0.25); C7 (≤ 3 kpc at t = 0); C9 (α {0, ∞} × seeds {603, 604, 605} × both footings, Bullet stable and
Harvey scorable in ≥ 2 of 3 seeds); grid seed 599. The scoring functions are imported from CFG623's `cfg623_main.py`.

## 4. Changes (only these)

1. Progenitor baryons per variant (§2), through one class `Progenitor625` that, for BASE, must reproduce CFG599's
   `Progenitor599` (gate C0).
2. **Calibration per variant:** CFG621's procedure (`calibrate()`: v0 bracketing on [0, 4000] km/s at η, then η bracketing on
   [0.03, 10] (log), up to 2 rounds, stop tolerances 100 km/s and 25 kpc) run serially at α = 0, canonical, seed 599, calib mode,
   re-tuning v0 and η only to K1/G1. A variant whose calibration misses K1 or G1, or gives η outside [0.1, 2.5], is VOID.
3. Reported-only items of CFG623 dropped for compute: M3 swapped α = 0, M4 seed 600, C8 reproduction, B-6 seed scatter (B-6 is
   still printed from the C9 runs).
4. **Added diagnostics (physics unchanged):** projected mass of the total map, of baryons (gas + cloud + stars) and of cold energy
   within 250 and 300 kpc of each galaxy peak, every epoch.
5. **M-RAW mass report (reported, not an α verdict).** For every variant and footing: (i) static t = 0 progenitor masses — baryon
   and cold-energy totals inside r_t and projected inside 250 kpc of the centre; (ii) at the Bullet epoch of the variant's α = 0
   grid run — projected M(<250) and M(<300) around each galaxy peak, by component. Compared with P16 (250 kpc) and R26 (300 kpc).
   **Anchor rule:** the anchor "lensing mass reached inside the framework" is MET iff the model's projected total within 250 kpc at
   the Bullet epoch is ≥ the P16 value − 2σ (main ≥ 2.3e14, sub ≥ 1.6e14). Inside the framework the only mass is baryons (fixed
   from the measurements above) plus the law's phantom; no mass is added by hand. If the anchor is not met, the SHORTFALL
   (P16 − model, and the ratio) is reported as a result and no anchored merger model is run. If it were met by a variant, that
   variant's α verdicts are already the anchored ones.

## 5. Gate order and run order

Shared: C1–C3, C5, C6 re-run (CFG621 control code, unchanged); C4(a), C4(b), N_B ≤ 1 re-read; C0 (BASE ≡ Progenitor599: max
relative difference ≤ 1e-12 over r, ρ_g, P, ρ_s, ρ_ph, M_ph, ρ_cc for main and sub, swap and not, both footings). A shared-gate
failure voids every variant.

Per variant (a failing gate voids that variant only, named): calibration → 12 control runs, C7, C9 → MUTATE M1, M2 (the grid's
α = ∞ and α = 0 canonical runs), M3 → grid.

Run order (machine-limited; partial coverage reported honestly): calibrations B1, B2, B3; then per variant B1, B2, B3: controls,
M3, grid nodes {0, 0.1, 1, ∞} × both footings; then nodes {0.3, 0.03, 3, 10} × both footings, variant by variant. Verdicts
V-1..V-4 are computed on the nodes run; V-3 on a 4-node grid uses α = 1 and ∞ only and is labelled "4-node".

## 6. What "robust" means (declared now)

Per variant, footing and node, the status is compared with CFG623's on the same footing:
- **FLIP:** ALLOWED ↔ EXCLUDED; or any α ≥ 1 node ALLOWED on both footings (V-3 changes); or V-1, V-2 or V-4 changes wording.
- **LOST:** a CFG623 ALLOWED or EXCLUDED status becomes UNSCORABLE.
- **NEWLY SCORED:** a CFG623 UNSCORABLE node becomes ALLOWED or EXCLUDED (this answers whether α = 1, 3, 10 become scorable).

Lane reading over the VALID variants and the nodes run:
- **VERDICTS ROBUST** iff no FLIP and no LOST anywhere: α = 0 ALLOWED, α = 0.1 and ∞ EXCLUDED (and 0.3 if run), no α ≥ 1
  ALLOWED, on both footings, in every valid variant.
- **ROBUST WITH WEAKENING** iff no FLIP but at least one LOST.
- **NOT ROBUST** iff at least one FLIP (named, with variant and footing).
A VOID variant counts as "not tested", never as robust. If fewer than all variants or nodes run, the reading is stated for the
coverage reached.

## 7. Compute and housekeeping

One process at a time, 1 thread, `nice -n 10`, RSS ≤ 3 GB. Before each run: `vm_stat`; if the unrelated 1024³ job (cfg596_pm.py)
is running and free + inactive < 6 GB, wait. That job is never signalled or starved. Run cache (JSON) in
`../_external_data/cfg625_work/runs` (outside the repo). Outputs `cfg625_*.out` and `cfg625_*_results.json`; README numbers come
from the JSON. CFG599/621/622/623 are read-only. Commit specific paths only; no push; never rewrite history.
