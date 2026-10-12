# CFG636 FROZEN CRITERIA: the framework-native 1024³ shear test of the condensed-baryon source (H-CB)

Committed alone, before the CFG636 validation runs and before any CFG636 production run. Date: 2026-10-12.

## 0. Disclosure: what was seen before this file was written

- **CFG596's canonical RESULT was seen** (commit 41efda383; `CFG596_lean_pm_1024/README.md`, RESULT section): candidate B
  (phantom sourced by all retained baryons) is EXCLUDED on raw KiDS-1000 (Δχ² +68.7, robustness minimum +43.9, T-OWN pass,
  NZ1 bites); DES Y3 Δχ² +22.4 is NOT DIAGNOSTIC (T-OWN fails, χ²_min 2.4); own boost B(z = 0) 1.19 / 1.25 / 1.21 at
  k 0.3 / 0.5 / 1 h/Mpc. CFG596's alt footing (P2) was still running when this file was frozen.
- **CFG634's results were seen** (criteria 1fea20013; `CFG634_condensed_baryon_source/README.md`): H-CB is NOT DECIDED
  (reservoir-limited) on the static gates; in CFG634's halo model (context only, ΛCDM-inherited ingredients, no verdict weight)
  H-CB turned CFG556's +72–89% excess at k = 1 into a 32–41% deficit, with R(k = 1) spanning 0.24–0.97 across variants.
- **This test is therefore chosen after seeing that candidate B fails the shear side and that H-CB moves the halo-model power
  down.** That is why the growth gate below fails a deficit exactly like an excess: the test cannot be passed by overshooting.
- **Settings:** κ = ½ is FITTED. The footings (9.3603e-11 / 1.1312e-10) are never pooled. "Cold energy" throughout; its MASS is
  still required; no particle species. Not "theory closed". Nothing here may say the data favour the framework. No ΛCDM or
  standard-MOND yardstick enters any verdict.

## 1. Hypothesis and engine

- **H-CB (CFG634):** the law's phantom is sourced only by condensed baryons (stars + HI/H2), not by hot X-ray gas.
- **Engine:** `cfg636_pm.py` = `CFG596_lean_pm_1024/cfg596_pm.py` at its production freeze (commit 6323b630f) with ONLY the two
  changes CFG634's spec names:
  1. in `cover_balls(..., want_fret=True)` the per-catchment source weight becomes the condensed retention
     **f_c = min(fret_of(lM), 0.10)** instead of fret_of(lM);
  2. in `x_supply` the census edge uses that same f_c: r_M from f_c f_b M_ta and ln(1 + f_c f_b/(1 − f_b)).
- **The rule used, confirmed against CFG634:** CFG634's FROZEN_CRITERIA (T5, HC-1) defines condensed = max(M*, 0.10 f_b M_ta)
  capped at the retained baryons, 0.10 being the census floor (stars + cold gas). The PM carries no stellar-mass model, so its
  HC-1 form is the cap alone, `min(fret_of(lM), 0.10)`, exactly as CFG634's README spec writes it. Because fret_of ≥ 0.10 for
  every mass, f_c = 0.10 in every catchment.
- **Unchanged:** particles, ICs, the switch (RES), R5, the supply, the step grid, the mask rules other than the edge's f_c, the
  table entry 0 = 1.0 for cells outside every catchment (the spec changes only the per-catchment weight), all output definitions.
- **Selector:** `CFG636_SOURCE` = `hcb` (production), `b` (old weight; must equal cfg596_pm.py bit for bit), `none` (control only).

## 2. Runs

- **Production:** C1 = H-CB RES canonical, then C2 = H-CB RES alt. L = 100 Mpc/h, N = 1024, NSEED 1024, seed 359,
  RMIN 0.78125, lean mode, spill on, 14 threads, nice 10, same 150-step grid and snapshots (z = 1, 0.5, 0 and the two
  measurement-only extras) as CFG596. Canonical first, alt later; alt is PENDING until C2 finishes.
- **S0 is shared:** CFG596 P0 (`_external_data/cfg596_work/P0`), read only. Same seed and box, so H-CB vs S0 is a same-pipeline pair.
- **Machine rule:** a production job runs alone, after every `cfg596_pm.py` process has ended and free + inactive memory is
  ≥ 42 GB (queued by a waiter; nothing is killed). Abort rule unchanged from CFG596: RSS > 50 GB or swap growth > 4 GB.
- **Optional MUTATE production run CM** (`CFG636_SOURCE=b`, canonical): must reproduce CFG596 P1's spectra; run only if machine
  time allows; it has no verdict role.

## 3. Validation gates (before production; 256³, one process ≤ 4 GB, nice 10)

- **V-R (reproduction control):** VBr = cfg636_pm.py with `CFG636_SOURCE=b`, lean RES canonical L100 N256 NSEED 512 RMIN 0.78125,
  must equal CFG596's VLr JSON (`cfg596_work/VLr`, the V-L reference of `cfg596_validate.py`) BIT FOR BIT: P(k), σ8, P_grav,
  σ8_grav and the diagnostics at every snapshot identical (difference exactly 0). Fail → no production.
- **V-H (smoke):** VHr = the same with `CFG636_SOURCE=hcb` must complete, and its gravitating P must differ from VBr's. Its
  P_grav/P_S0 at k 0.3 / 0.5 / 1 (S0 = CFG596 VLs) is reported as a PREVIEW, NOT a verdict (256³ resolution).

## 4. Statistic, data and verdict: identical to CFG596 (FROZEN_CRITERIA.md, f6c27d401)

- **Scorer:** `cfg636_native.py` = `cfg596_native.py` pointed at the CFG636 runs (framework) and CFG596 P0 (S0). CFG592's
  `cfg592_native.py` library part is exec'd unchanged.
- **Data:** raw KiDS-1000 and DES Y3 ξ± with their published covariances, n(z) and cuts.
- **Support cut:** a point is kept if ≥ 90% of its integrand lies in [k_lo, k_hi] (k_hi = πN/(4L) = 8.04 h/Mpc); a survey with
  N_kept < 10 is NOT DIAGNOSTIC.
- **Models:** framework = the run's MEASURED gravitating P(k, z) at z = 0, 0.5, 1 (CFG592 'F' path, B ≡ 1); S0 = P0's particle P.
- **Statistic:** Δχ² = χ²_min(H-CB) − χ²_min(S0) per survey and footing, IA marginalised; positive = framework worse.
- **Robustness set:** widen2, noIA, DESI distances, held (P_part,F(z) × B_F(z = 0)).
- **Classes:** EXCLUDED (Δχ² ≥ 9 and robustness minimum ≥ 9); TENSION (Δχ² ≥ 4); CONSISTENT (Δχ² < 4 and robustness maximum < 9);
  NOT DIAGNOSTIC otherwise, or N_kept < 10, or a failed T-OWN. The no-IA class is reported alongside.
- **T-OWN tooth (unchanged):** the S0 best-fit mock × B_foot(k) from CFG530's L100 N512 caches (z = 0, held in z, flat outside
  0.08–4.02) must give an S0 refit χ²_min ≥ 9, else that survey × footing is NOT DIAGNOSTIC.
- **NZ1 MUTATE (unchanged):** the framework path with the source set to zero must reproduce χ²_min(S0) to |Δχ²| ≤ 1e-9.
  `CFG596_MUTATE=1` writes separate `_MUTATE` outputs and is run FIRST (it supplies T-OWN to the main pass).
- **Reported only:** the interpolation check at the extra snapshots, the five-node variant, absolute χ²/N and p-values, support
  thresholds 0.8 / 0.7, NZ2.

## 5. Added gate: growth on the gravitating field (CFG555 rule)

- At z = 0: **G = max over bins with k ≤ 1 h/Mpc of |P_grav,H-CB(k) / P_S0(k) − 1|** (S0 = P0 particle P, same k bins).
- **G ≤ 0.10 is required. A deficit fails exactly like an excess.** The same quantity at z = 0.5 and z = 1, the σ8_grav ratio,
  and P_grav/P_S0 at k 0.3 / 0.5 / 1 are reported only.

## 6. Verdict per footing

- **H-CB FAILS natively** on a footing if any diagnostic survey is EXCLUDED, OR if the growth gate fails (G > 0.10).
- **H-CB PASSES the shear side** on a footing only if it is CONSISTENT on at least one diagnostic survey, no survey is EXCLUDED
  or in TENSION, and the growth gate passes. A pass of the shear side requires this on BOTH footings.
- Anything else: TENSION or NOT DIAGNOSTIC as classed, stated as is.

## 7. Inherited ΛCDM-calibrated ingredients (flagged, as in CFG596)

The PM's EH no-wiggle IC spectrum at σ8 = 0.811; the flat w = −1 background with Planck-like constants; the Δ_ta(z) shell table
from a ΛCDM shell ODE; the survey nuisance priors; massless neutrinos. There is NO HMcode, NO BAHAMAS and NO halo-model mass
function in the verdict.

## 8. Outputs

In the lane folder: `cfg636_pm.py`, `run_636.py`, `cfg636_validate.py` → `.out/.json`, `cfg636_native.py` →
`cfg636_native(_MUTATE).out/_results(_MUTATE).json`, `README.md`. Arrays and logs in `../_external_data/cfg636_work/`.
Every number quoted comes from a JSON. Dated disclosures go in the README. This file is never edited.
