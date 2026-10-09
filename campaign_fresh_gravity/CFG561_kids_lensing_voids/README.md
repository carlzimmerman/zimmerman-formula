# CFG561: do isolated KiDS lenses inside cosmic voids lens differently from matched lenses outside? NON-DISCRIMINATING (underpowered; the void-tracer control FAILED)

**Ledger line:** CFG561 KiDS-N isolated lenses inside BOSS DR12 voids (Mao+2017) vs (M*, z, colour)-matched outside:
outer bins 0–7 Δ = −0.033 ± 0.071 dex (−0.46σ), K1 −0.003 ± 0.105 → NON-DISCRIMINATING (purity-corrected 2σ bounds
0.52 / 0.58 dex, far above the 0.1 dex NULL bar; power to see a true 0.1 dex outer offset at 3σ ≈ 1%); the frozen positive
control C3 (void lenses have fewer KiDS neighbours) FAILED (+0.011 ± 0.028 dex), so the photo-z void flag is not shown to
select emptier surroundings; main run exits 1 on that failure; κ fitted; cold mass still required; not theory closed.

- **Criteria:** `FROZEN_CRITERIA.md` (4a5cebaa2), committed alone before any script or void number.
- **Script:** `cfg561_voids.py` (~60 s). Main run: 4/5 checks, 1 load-bearing failure (C3) → exit 1. MUTATE run: C3 fails → exit 1
  (but see "MUTATE" below: it is not informative while C3 also fails on the real flags).
- **Data:** per-lens sums `real_research/data/lensing_rar/cfg110_perlens.npz` + CFG446's lens/bright-sample files (read only);
  Mao et al. 2017 BOSS DR12 void catalogue from CDS (`data/`, `FETCH_LOG.md`). Pure data: the a₀ footings (9.3603e-11 /
  1.1312e-10) do not enter.

## Verdict table

| row | N_void | purity p̄_V | Δ outer (bins 0–7), dex | Δ K1 (bins 8–14), dex | verdict |
|---|---|---|---|---|---|
| **headline** p ≥ 0.25 vs p < 0.02, matched | 10,472 (vs 50,872 outside, eff. 33,572) | 0.398 | **−0.033 ± 0.071 (−0.46σ)**; corrected −0.09 ± 0.21 | −0.003 ± 0.105 (−0.03σ); corrected −0.01 ± 0.29 | **NON-DISCRIMINATING** (both) |
| deep cores R = 0.5 R_eff (reported) | 579 | 0.32 | −0.06 ± 0.49 | +0.35 ± 0.16 (+2.1σ) | — |
| p ≥ 0.5 (reported) | 1,940 | 0.62 | −0.11 ± 0.14 | +0.22 ± 0.13 (+1.7σ) | — |
| p-weighted (reported) | 25,170 | 0.35 | −0.032 ± 0.066 | +0.050 ± 0.070 | — |
| early only (reported) | 5,172 | 0.40 | −0.145 ± 0.090 (−1.6σ) | −0.04 ± 0.12 | — |
| late only (reported) | 5,300 | 0.40 | +0.19 ± 0.13 (+1.4σ) | +0.10 ± 0.18 | — |

Frozen map (outer bins headline): SETTLING-SIGN Δ < 0 at > 3σ; FORCE-SIGN Δ > 0 at > 3σ; NULL |Δ| < 2σ and purity-corrected
2σ bound < 0.1 dex; else NON-DISCRIMINATING. No row reaches 3σ in either direction; the null cannot be bounded at 0.1 dex.

## Power (printed before any void number)

From 100 random analysis-set subsets of the void size, matched the same way: expected σ_Δ = 0.080 dex (outer), 0.073 (K1);
the null z-spread 1.03 / 0.93 (C5, pass). Membership purity p̄_V − p̄_O = 0.40 (photo-z σ 0.02(1+z) ≈ 70 Mpc/h comoving vs
void radii ~40 Mpc/h), so a true 0.1 dex outer offset is diluted to ~0.04 dex: **P(3σ detection) ≈ 0.01**; the expected
purity-corrected 2σ bound is 0.42 dex. The lane could not reach any of the three pictures' separations; this is a power
limit of photo-z void membership on KiDS-N × BOSS North (76,061 analysis-set lenses, 25 populated jackknife patches),
not a statement about the physics.

## Controls

- **C1 PASS:** per-lens sums reproduce CFG88's full-sample K1 split to 5 × 10⁻¹⁴ and its zero-model χ² 35.0418/7.
- **C2 PASS:** all 181,477 lenses match the bright sample by exact position (pool for C3).
- **C3 FAIL (load-bearing, kept):** void lenses' pool-neighbour count within 8 Mpc/h projected, |Δz| < 0.036(1+z), vs matched
  outside: T = +0.011 ± 0.028 dex (+0.37σ); needed < 0 at > 3σ. Post hoc (added after run 1, reported only): at 20 Mpc/h,
  T20 = +0.031 ± 0.032 (p ≥ 0.25) and −0.021 ± 0.037 (p ≥ 0.5). The tracer's jackknife error (0.028) is ~10× the
  shuffled-flag error (0.003, MUTATE): the void flags are spatially coherent, so the test is limited by the ~100 voids
  (void-to-void variance), and the photo-z window (±~130 Mpc/h) dilutes a ~40 Mpc/h void. The flag's environmental meaning is
  therefore **not verified in the KiDS data**; it rests on BOSS's spectroscopic void finding alone.
- **C4 PASS (after a disclosed fix):** 20 random void catalogues → outer z mean −0.48 (std 1.03, max |z| 2.79), K1 +0.22
  (0.87, 1.58). **Departure:** the frozen spec redrew all 903 BOSS-North centres into the KiDS-N box (~5× the real void density
  there), which emptied the OUTSIDE sample and produced NaN (run 1 kept: `cfg561_voids_RUN1_C4misspecified.out/_results.json`;
  its C3 and headline numbers are identical). Fixed by redrawing only the 242 voids whose centres lie in RA 118–248°,
  Dec −1.2..+12° (those that can reach the lenses), uniformly in that box.
- **C5 PASS (reported):** null z std 1.03 (outer), 0.93 (K1).

## MUTATE

p_void shuffled among analysis-set lenses (seed 561): tracer T = −0.0001 ± 0.0030, outer Δ +0.004 ± 0.085; C3 fails → exit 1.
Because C3 also fails on the real flags, the MUTATE exit is **not** a discriminating check in this lane (disclosed). The K1 row
reads +0.117 ± 0.052 (+2.2σ) under the shuffle, inside the C4/C5 null spread at < 3σ.

## Reading

- No sign is detected in either bin set; the headline outer Δ is slightly negative (−0.46σ). Reported-only early/late rows
  point in opposite directions at < 1.7σ each; nothing is claimed from them.
- Even a future SETTLING-SIGN would not by itself separate settling from ΛCDM: ΛCDM also predicts a lower 2-halo term around
  void galaxies (frozen caveat). The FORCE-SIGN foil is not supported here, but this lane is too weak to exclude it either.
- What would make this test bite: spectroscopic lens redshifts (GAMA overlap; purity → ~1, about ×2.5 in effective Δ) and/or a
  denser void catalogue at z 0.1–0.3 (e.g. GAMA/KiDS-bright voids), plus KiDS-Legacy area.

κ = ½ fitted; no dark-matter particle (the framework's cold mass is still required, amount free); not theory closed; nothing
here says the data favour the framework over ΛCDM.

## Files

`FROZEN_CRITERIA.md`, `cfg561_voids.py`, `cfg561_voids.out` / `_results.json` (main), `cfg561_voids_MUTATE.out` / `_results.json`,
`cfg561_voids_RUN1_C4misspecified.out` / `_results.json` (first run, mis-specified C4), `data/mao2017_*` (CDS), `FETCH_LOG.md`.
