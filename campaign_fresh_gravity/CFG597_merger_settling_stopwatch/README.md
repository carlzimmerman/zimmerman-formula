# CFG597: cluster mergers as a stopwatch for cold-energy settling — VOID as frozen (control C4 failed)

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (ae49ff4d7), 2026-10-10. Frozen text is never edited. Every change
  after the freeze is a dated disclosure below.
- **Status: VOID.** Control C4 (isolated progenitor) failed: 16.96 kpc against the 15 kpc limit (`cfg597_results.json` → `C4`).
  Under §5 every simulation verdict depends on the centroids C4 checks, so **V1–V5 are VOID**. No α range is reported as a verdict.
  The as-run numbers below are a reading only.
- Settings: κ = ½ is FITTED. Both footings (9.3603e-11 / 1.1312e-10) are reported and never pooled. Kernel ν(y) = 1/(1 − e^(−√y)),
  the exponential form written in THEORY_v1 A1 (not FP1's monotone-repaired variant). Candidate B, G9, no EFE. The cold energy's
  mass is still required (an input). No particle species. Yardsticks are raw data only: no ΛCDM halo or baseline, no MOND force
  law. Nothing here says the data favour the framework. This is not "theory closed".

## What was built

- A 3-D merger: adiabatic grid hydro gas (MUSCL/Rusanov), collisionless galaxies, and cold energy as particles. The cold energy
  feels the CFG541 class-A drift toward the round-rule phantom of the CURRENT baryons of each progenitor, plus CFG544's FIX-2 OU
  velocity relaxation. Mobility region: the whole box. Grid: 128×64×64 at 50 kpc.
- Cases: L (law-filled, primary) and U (record census with an unsettled NFW part). Rules: 2S (primary) and 1S.
- α ∈ {0, 0.1, 0.3, 1, 3, 10, ∞}. Footings: both for the 10:1 runs; canonical only for 4:1.
- Data: the Bullet via the record's Clowe+06 Table 2 script, read-only. Offsets 194.1 kpc (sub) and 209.4 kpc (main); BCG–BCG
  721.5 kpc; f_obs 0.045, σ_f 0.125 (PROVISIONAL). Harvey+15: β = −0.04 ± 0.07. D3 systems at sign level only. Nothing was
  downloaded.

## Files

| file | what |
|---|---|
| `cfg597_lib.py`, `cfg597_sim.py` | grid, hydro, PM, round phantom, drift + OU, diagnostics |
| `cfg597_controls.py` → `cfg597_controls.out`, `_results.json` | C1 Poisson (2.83% ≤ 3%), C2 Sod (1.12%), C3 phantom (0.13%), C5 conservation: PASS |
| `cfg597_main.py` → `cfg597.out`, `cfg597_results.json` | calibration, C4, 53-run grid, scores, frozen verdict code |
| `CFG597_MUTATE=1 cfg597_main.py` → `cfg597_MUTATE.out`, `cfg597_results_MUTATE.json` | M1–M3 |
| `cfg597_supp.py` → `cfg597_supp.out`, `_results.json` | S1, post-freeze, reported only (D-3) |
| `cfg597_c4_diag.py` → `cfg597_c4_diag.out`, `_results.json` | C4 diagnosis (D-5) |
| `runs/` | per-run time series (JSON). `runs_discarded_pericentre_target/` holds the first, infeasible calibration (D-1) |

All runs used `nice -n 10` and 4 processes of 1 thread. Total wall time was about 6 h on a loaded machine.

## Controls and MUTATE (as frozen)

- C1, C2, C3, C5: PASS. C3b, the painted phantom from sampled baryons, was off by 5.7% at 300 kpc. It is reported, not a frozen control.
- **C4: FAIL.** The largest gas/lensing–galaxy offset was 16.96 kpc, against a 15 kpc limit. M(<300 kpc) drifted −0.13%.
- M1 PASS: at α = ∞, f150 = 0.656, so lensing sits on the gas.
- **M2 FAIL:** the pure-collisionless β̄ is 0.125, above the frozen 0.10. Its f150 = 0.063 is within the limit.
- M3 PASS: with the roles swapped, f150 = 0.072, so the offsets flip.

## As-run reading (NOT a verdict; VOID by C4)

10:1, L, 2S. Each cell gives max(|Z_B|, |Z_H|), canonical / alt:

| α | 0 | 0.1 | 0.3 | 1 | 3 | 10 | ∞ |
|---|---|---|---|---|---|---|---|
| max\|Z\| | 1.60 / 1.56 | 2.34 / 2.46 | 3.54 / 3.67 | 4.19 / 4.21 | 2.20 / 2.21 | 1.92 / 1.93 | 2.02 / 2.04 |

- **The full passing set is {0, 10} on both footings.** The nodes α = 0.1, 0.3, 1 and 3 fail, and α = ∞ misses by 0.02–0.04.
- The α = 10 pass is not a physical window. At high α the 100 and 150 kpc lensing apertures disagree (f150 0.655 against
  f100 0.269), and the frozen σ_num = |f100 − f150| inflates the error. The same inflation keeps α = ∞ at Z_B 1.72. On the obs
  error alone, f150 = 0.656 would be 4.9σ.
- The other cells:
  - L-1S passes no node.
  - 4:1 L passes only {0}.
  - U-2S passes most nodes, but only because its 150 kpc aperture is unstable at every α (f150 ≈ 0.9 against f100 ≈ 0.02), so it is
    not diagnostic. U's main-progenitor unsettled fraction is 0.73, outside CFG515's 0.37–0.63.
- The pattern in the primary cell is monotone, with no noise-flattering: settled cold energy that relaxes toward the phantom of
  the current, gas-dominated baryons pulls the lensing toward the stripped gas. The shift is about 200 kpc at α = 0.1 and the full
  shift by α ≈ 1. It only says something about α once the controls and estimators pass.

## Dated disclosures (2026-10-10)

- **D-1 Calibration target changed.**
  - The frozen M-6 asked for v_peri = 2700 ± 200 km/s. That is infeasible: from rest, the cores meet at 3600–7100 km/s.
  - SF07's 2700 km/s is the bullet's speed at the observed epoch. So v0 was calibrated on the galaxy speed at the 720-kpc
    post-pericentre epoch, with v0 ≥ 0. The first runs are kept in `runs_discarded_pericentre_target/`.
- **D-2 Calibration misses.**
  - **10:1 L landed at 3021 km/s**, outside 2700 ± 200. The response is non-monotonic (1867, 3048, 2323, 3021 km/s), and the
    last iterate was used.
  - 4:1 U landed at 3305 km/s; v0 = 0 gives 2362 km/s.
  - 10:1 U (2825) and 4:1 L (2551) are within tolerance.
- **D-3 Gas geometry.**
  - The frozen gas model strips the sub's gas wholesale before pericentre. At the 720-kpc epoch d_SG is 770–950 kpc, against the
    Bullet's 194 kpc, so the comparison is not like-for-like.
  - S1 (post-freeze, reported only) used a compact sub core, r_c = 0.03 r200. It is still stripped (d_SG about 840 kpc) and shows
    the same trend: f150 0.047 / 0.178 / 0.453 / 0.629 / 0.721 at α = 0 / 0.1 / 0.3 / 1 / ∞.
  - At 50 kpc cells with no cooling, the model cannot hold a bullet cool core.
- **D-4 alpha_max is mis-defined.**
  - `alpha_max()` takes the FIRST Z = 2 crossing and places α = 0 at 0.03 (an endpoint substitution). For a disconnected passing
    set such as {0, 10}, the printed "α_max 0.058 / 0.054" is therefore meaningless.
  - The `Gamma_tobs_at_alpha_max` number in the JSON inherits the same defect. A local Γ is also not a halo recentring rate.
    Do not cite either.
  - The frozen V4 line reports "VARIANT-DEPENDENT" only because of a wording difference (1S has no α = 0 node). That is not a
    physical difference.
- **D-5 C4 diagnosis** (`cfg597_c4_diag.py`).
  - On the exactly symmetric t = 0 state, whose true gas centre is (0, 0), the frozen gas-centroid estimator returns
    (−9.35, −9.35), 13.2 kpc off. That happens before any dynamics.
  - The cause: the estimator starts at the argmax pixel of a map made by block-repeating the 50-kpc gas cells, and it stalls at a
    block-edge fixed point. Galaxy shot noise (±4–9 kpc from 40,000 star particles) adds to it.
  - Started from the mass-weighted centroid, the same estimator returns (0.00, 0.00).
  - The lensing centroid stayed within 10.6 kpc, and M(<300) drifted −0.13%. So C4 failed on a gas-ESTIMATOR offset, not on an
    OU or drift drift of the halo. It is still a frozen fail.
- **D-6 Review.** An independent review (`REVIEW_openai_astra_2026-10-10.md`, 306426335) found the same C4, alpha_max, M2 and
  calibration points. All were verified here against the JSON.
- **Not claimed:** that galaxy settling (α ≳ 0.5) is incompatible with mergers, any allowed α range, and that instant
  re-settling is excluded.

## What a valid rerun needs (new frozen criteria first)

1. A gas centroid that passes C4. Use a mass-conserving (CIC or trilinear) projection, start from the tracer mass-weighted
   centroid, and use more star particles. Re-test C4 before any merger number.
2. A passing-set rule fixed in advance: report every grid node, with no first-crossing α_max and no endpoint substitution.
3. A lensing-peak estimator that is aperture-stable at high α, such as a smoothed-map peak or a fixed-aperture fit, in place of
   the σ_num = |f100 − f150| inflation.
4. A Harvey statistic whose collisionless baseline passes M2. For example, exclude ±0.1 Gyr around pericentre, where the
   apertures capture the main peak.
5. A bracketed (bisection) v0 calibration that lands inside ±200 km/s.
6. A gas model that keeps a bullet core (finer cells near the sub, or a declared cool core with cooling), so that d_SG is near 194 kpc.
7. Optionally, the review's unit test: compare the drift's initial slope against an analytic smooth-equilibrium response.

Until then CFG597 supports no statement about α beyond "not established".
