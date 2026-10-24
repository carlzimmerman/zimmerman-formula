# X23_late_heating_graded: X22's late-heating window, graded on clusters and hosted dwarfs

Criteria: `FROZEN_CRITERIA.md` (6ec6b89807, committed alone). `AMENDMENT_A1.md` (post-result): one check-code fix and a
reported-only label reading. κ = ½ FITTED. Footings never pooled. Field mass, not a particle. Not "theory closed". Nothing here
says the data favour the framework. All numbers are in `x23_late_heating_graded.out` / `_results.json`.

## Verdict

**Frozen rule: UNDECIDED (footings disagree).** Both footings return **LATE HEATING FAILS**. They differ only on SPARC small
(Z_res −1.71 / −2.60), and that is a defect of the frozen rule, explained in A1.

**What the failure is, on both footings:**

| row | late heating predicts | observed (B_iso) | grade |
|---|---|---|---|
| hosted dwarfs: MW ultra-faints, bright M31, M31 others | E_pred ≤ 8e-4 dex (median 6e-6 per system) | +0.21 to +0.64, Z 2.1–5.6 | **UNDER**, all three |
| Clusters T2 / T3 | +1.01 / +1.18 (canonical), CAPTURED | +0.27 / +0.26 | **OVER**, Z_res −8.5 / −22 |
| Clusters T1 | +0.85, CAPTURED | +0.04 ± 0.13 | OVER (predicts EXTRA, X19 NONE) |
| Groups, LG field | ≈ 0.02 / 0 | consistent | reproduced |
| SPARC, MW disc, UMa, TDGs, DF2/DF4, Crater II | ≈ 0 | below the law (E < 0) | the law's own residual (A1) |

A1 label reading, identical on both footings. The mismatches are Clusters T1 (predicted EXTRA, X19 NONE) and the three
hosted-dwarf classes (predicted NONE, X19 EXTRA).

**Checks 4/4** (K0 after A1; K1 β → 0 limit to 1e-10 and c_s → 0 all captured; K2 X22's C4; K3 0.06 GB). `--mutate`
(c_s × 2) fails K0, exit 1.

## Reading

- **Hosted dwarfs are the wall.** With c_s ≈ 190–200 km/s and σ = 2–10 km/s, β ≈ 1e-3. The heated component sits at the
  cosmic mean inside a dwarf, a 1e-6 fraction of the baryons. Any universal late heating that clears the forest and SPARC
  (X22) empties these systems, and these are exactly the systems that need the most extra. X20_hosted_dwarf_requirement
  found the need rising toward low M★ / small r_half, which is where heating removes it most completely. That is a sign
  conflict, not a tuning problem. X20_hosted_dwarf_disequilibrium has already ruled out tides and binaries as the source.
- **Clusters get too much.** At σ = 450–630 km/s the well captures the component (β 10–22, beyond the hydrostatic cap
  2.9). Under X22's cap convention the whole share piles inside 0.55 Mpc: ×7–15 the need. The cap is X22's convention, not
  physics. A capture that behaves like dust instead gives ZT2B's numbers (profile-limited, needs concentration ×8). Either
  way, no cluster row is reproduced, and T1 is predicted to carry the extra it does not show.
- **Consequence for verdict 8.** Universal late heating is the one window X22 left that gravity allows. It is not the
  missing piece by itself: it cannot leave extra in hosted dwarfs, and in clusters it is either too much (cap) or
  profile-limited (dust-like). A collapse key on δ_b is X19's ρ_b variable, which X19 already fails (6 offenders).
- Not graded here: low-z lensing under late heating.

## Files

`FROZEN_CRITERIA.md`, `AMENDMENT_A1.md`, `x23_late_heating_graded.py`, `.out` / `_results.json`, `_RUN1` (before A1) and
`_MUTATE` outputs.

    OMP_NUM_THREADS=1 python3 x23_late_heating_graded.py            # exit 0, 4/4
    OMP_NUM_THREADS=1 python3 x23_late_heating_graded.py --mutate   # exit 1, K0 fails
