# X23_late_heated_cold: late-heated cold energy (LHC) on the KT-keyed cluster test, and one c_s against five constraints

Criteria: `FROZEN_CRITERIA.md` (b8d81770bb, committed alone). `AMENDMENT_A1.md` (df896db507, coordinator request, before any
run): the overdetermination scan. `AMENDMENT_A2.md` (8b21926ce6, check definition only; RUN1 was killed during the first cell
build, before any graded number). κ = ½ FITTED. Footings never pooled. Cold energy is field mass, never a particle. c_s is read
from X22's JSON, never fitted. Not "theory closed". Nothing here says the data favour the framework. Every number is in
`x23_late_heated_cold.out` / `_results.json`.

**ID collision.** Two X23 lanes exist: this one and `rebuild_2026_10_22/X23_late_heating_graded` (criteria 6ec6b89807,
result 9c54fae62e). That peer lane already grades X22's window on every X19 class with X22's flat-well profile. I re-ran its
committed script read-only from a scratch copy, with only its input root changed. Its `.out` matched line for line, and its
JSON matched apart from timing. So this lane does not re-grade those rows; it quotes them. It adds:
1. the KT-keyed cluster test in the real C\* potential;
2. the one-c_s overdetermination scan (A1);
3. the forest/σ₈/CMB, energy and action lines.

## Verdict (frozen classes): **WRONG AMPLITUDE**, all 4 cells, both footings

The amplitude factor is F = (A_pred − 1)/(A_meas − 1) over the 106 KT clusters: **12.3 / 10.7** (canonical, h 0.672 / 0.686)
and **14.9 / 12.7** (alt).

**A1: no single c_s ≥ c_s,need fits all the constraints. INTERSECTION EMPTY on both footings.**

| sub-test | grade |
|---|---|
| KT terciles (X21) | FAIL in every cell, Z_t from −17 to −36 (over-predicted) |
| KT slope (X21) | FAIL, Z −5.8 to −6.5 (predicted slope ≈ 3× too steep) |
| clusters by MGAS500 (X7 terciles; A1 at c_s,need) | FAIL in all three terciles: T1 is predicted A 6.6, but measured 1.10 |
| SPARC (X22 d2 line) | PASS by construction at c_s,need (X22) |
| groups (peer lane) | REPRODUCED: E_pred +0.022 / +0.021 against +0.020 ± 0.065 / −0.021 ± 0.065 |
| MW disc (peer lane) | E_pred +0.0006 / +0.0003 dex, so K_z rises by ≈ 0.1 %: negligible. The law's own residual (−0.14 / −0.16) is unchanged |
| forest / σ₈ (X22, p 3–6) | p 3: forest UNDECIDED, R_σ₈ 0.995. p 4 and p 6: PASS, R_σ₈ ≥ 0.997. p 5 lies between them |
| CMB | unaffected: c_s(z = 1100) ≤ 5e-6 km/s, k_J ≥ 4e8 h/Mpc |
| hosted dwarfs | **CONFLICT with a measured requirement** (see below) |

## Step 0 (K0, K1 PASS)

- **X7 and X21 reproduced.** X7's MGAS500 tercile A_CAL, X21's KT tercile A and X21's KT slope b all match, max |dev|
  8.9e-16 over 28 numbers. Canonical h 0.672: KT terciles 1.10 / 1.65 / 2.13, b +2.24.
- **X22 read.** c_s,need is 190.014 / 201.315 km/s. The p-scan is read from X22's JSON.

## Step 1: clusters keyed on KT (c_s = c_s,need)

**Model.** For each cluster:
- the cold fluid is isothermal and in hydrostatic equilibrium in the C\* potential (law + baryons + EFE):
  ρ_c ∝ exp[∫_r^{r_ta} g dr′/c_s²];
- it holds the mass-conserving fair share, M_c(<r_ta) = 5.364 M_b;
- it sources AQUAL with the baryons and lenses.

**Predicted against measured A_MID** (measured values from X21):

| cell | A_meas by KT tercile | A_pred (LHC) | b_meas | b_pred | F |
|---|---|---|---|---|---|
| canonical h 0.672 | 1.10±0.38 / 1.65±0.32 / 2.13±0.25 | 7.85 / 8.65 / 10.70 | +2.24±0.74 | +6.88 | 12.3 |
| canonical h 0.686 | 1.16±0.39 / 1.76±0.32 / 2.22±0.26 | 7.71 / 8.52 / 10.53 | +2.38±0.76 | +6.80 | 10.7 |
| alt h 0.672 | 1.00±0.34 / 1.51±0.29 / 1.96±0.23 | 7.62 / 8.37 / 10.29 | +2.07±0.68 | +6.46 | 14.9 |
| alt h 0.686 | 1.06±0.35 / 1.61±0.30 / 2.04±0.24 | 7.48 / 8.25 / 10.14 | +2.20±0.70 | +6.39 | 12.7 |

**Why.** At c_s ≈ 190 km/s and σ ≈ 450–630 km/s, the cluster captures the whole component.
- **The fair share is 24 × M_gas,500**, and 60–62 % of it sits inside 0.15 Mpc (99.7–99.8 % inside 0.5 Mpc).
- **Normalising at the cosmic mean at r_ta instead would give 10^19–10^20 × the fair share.** The cap binds in 320 of 326
  clusters.
- **The cold mass's own pull at R500 is 3.0–3.3 × the baryons' pull.** So leaving self-gravity out understates the
  concentration.

This agrees with the peer lane's flat-well result (T2/T3 +1.0 / +1.2 dex against +0.27). The real potential and the
mass-conserving normalisation do not rescue it.

**Reported bracket: c_s = σ_KT (shock-heated reading; median 517 km/s).**
- A_pred is 3.23 / 2.39 / 1.54 by KT tercile (canonical h 0.672), with slope b_pred −2.84.
- So it is too much where KT is low and falls with KT: the wrong sign of the dependence.

## Amendment A1: one c_s ≥ c_s,need against seven constraints

Grid: c_s,need × 1 … 16. A constraint counts as met only if it holds in both h cells. Allowed grid values in km/s, canonical
(alt in brackets):

| constraint | allowed c_s |
|---|---|
| C-SPARC (X22) | all ≥ 190 (≥ 201) |
| C-GRP (peer predictor) | all |
| C-T1 (≈ none) | ≥ 475 (≥ 503) |
| C-T2 | 570 only (604 only) |
| C-T3 | 760 only (805 only) |
| C-KT3 (all three KT terciles) | **none** |
| C-KTb (KT slope) | 760 only (805 only) |
| **intersection** | **EMPTY (EMPTY)** |

**Reading.**
- The cluster excess turns on sharply between c_s ≈ 3 and 4 × c_s,need: A_pred goes from 1.0 to above 10.
- T2 asks for ≈ 570–600 km/s and T3 for ≈ 760–800 km/s. No grid value satisfies both, and no value reproduces all three KT
  terciles.
- Raising c_s to ≈ 3–4 × c_s,need also leaves the galaxies with even less (SPARC's line is only a lower bound). So that
  part costs nothing. But a single isothermal temperature produces a step in well depth, not the smooth KT rise X21 measured.

## Reported only

- **Hosted dwarfs: CONFLICT with a measured requirement.**
  - The peer lane (`X23_late_heating_graded`) predicts ≤ 8e-4 dex (median 6e-6), and E_pred = +0.0000 in each class. The
    observed values are:
    - MW ultra-faints +0.625 ± 0.111 (canonical) / +0.585 ± 0.109 (alt);
    - bright M31 +0.249 / +0.211;
    - M31 others +0.644 / +0.587.
  - `X20_hosted_dwarf_requirement` measures the need: a graded rise toward low M★ and small r_half.
  - `X20_hosted_dwarf_disequilibrium` rules out tides and binaries as its source: the τ ≤ 0.1 subset gives +0.48 / +0.45 dex,
    Z 5.8 / 5.4.
  - LHC removes the component exactly where the extra is measured.
- **Bullet Cluster sign.** If the component is a single perfect fluid at c_s 190 km/s, a ~4500 km/s collision is Mach ~24.
  The fluid would shock and stay with the X-ray gas, so the lensing would follow the gas. That is the opposite of the observed
  galaxy-following offset, unless the field is collisionless (qualitative).
- **Heating energy.**
  - (3/2) ρ̄_c c_s² is 2.3e-7 / 2.6e-7 of ρ_Λc².
  - Per baryon that is 3.0 / 3.4 keV: about 8–10 × a supernova or coupled-AGN feedback scale (0.37 / 0.33 keV; PROVISIONAL,
    from memory).
- **Action status: no action.**
  - X6: no free dust coupling.
  - X19 step 2: no action-level selector.
  - CFG944 Theorem G: local θ-clock tethers carry a ghost or cannot be off in the linear universe.
  - CFG741: P-wave heating gives Q ≤ 0.50.
  - CFG643: the baryon → cold heat exchange is CLOSED.
- **Prior heated-component lanes found.** None is equivalent to this test:
  - CFG742 (constant warm σ_C 250–700 km/s; linear Jeans only, CLOSED);
  - CFG741 (P-wave heating energy);
  - CFG665 (isothermal selector, no regular solution);
  - CFG643 (heat exchange);
  - CFG580/581 (hot baryonic gas);
  - CFG745 (hot-gas selector);
  - the peer lane above.

## Checks and MUTATE

| check | main | MUTATE (`X23_MUTATE=1`: m1 c_s := σ_KT, m2 KT labels shuffled, m3 hydrostatic sign flipped) |
|---|---|---|
| K0 X7/X21 reproduction | PASS 8.9e-16 | **FAIL** 1.35 (as required) |
| K1 c_s = X22 exactly | PASS (1 value per footing) | **FAIL** (91 distinct values) |
| K2 solver (A2 lines) | PASS 5.9e-6 / 8.5e-10 | **FAIL** 2.0 (as required) |
| K3 RSS | PASS 0.46 GB | PASS |
| exit | 0 | 1 |

## What this does not show

- **Linear-order growth, isothermal statics, one temperature.** The self-gravity of the cold fluid is left out, and including
  it only deepens the capture.
- **No time dependence of cluster assembly.** The KT and MGAS500 rows are A_MID only. OUTER is not graded.
- **The SPARC, groups, MW and hosted rows are quoted** from X22 and the peer lane, not recomputed.
- **The scan is a grid,** so allowed sets are grid points, not exact intervals.

## Run

```
PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 rebuild_2026_10_22/X23_late_heated_cold/x23_late_heated_cold.py               # exit 0, ~100 s, 0.46 GB
PYTHONHASHSEED=0 X23_MUTATE=1 OMP_NUM_THREADS=1 nice -n 15 python3 rebuild_2026_10_22/X23_late_heated_cold/x23_late_heated_cold.py  # exit 1 by design
```

Read-only inputs:
- X2's source (functions exec'd, as X21 does);
- X7's npz and JSON;
- the eRASS1 FITS;
- the X19, X21, X22 and peer-lane JSONs.
