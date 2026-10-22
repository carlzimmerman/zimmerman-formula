# A81 — MUTATION RECORD

Ten single-input mutations. Each changes exactly one input of `a81_checks.py`, each was run from a
clean environment (`A81_MUTATE=<name> python3 a81_checks.py`), and each **exits 1** with a named set of
checks failing. The failing sets below are copied from the `a81_MUTATE_<name>.out` files, not asserted.

```
$ python3 a81_checks.py                          -> exit 0, 27/27 PASS (29.2 s)
$ A81_MUTATE=<name> python3 a81_checks.py        -> exit 1 for every name below
```

| # | mutation | one input changed | failing checks | what that proves |
|---|---|---|---|---|
| 1 | `unprofile_B` | B is set to the lensing value `exp(-Bc/C)` and the IMF prior is **not** marginalised (the `b_marg` defect of A71) | **C12, C16, C17** | the joint fit really profiles B: with B pinned at `B_req` the optimum lands at `B = B_req` (`1.23743`), C12's "B strictly between 1 and B_req" fails, the SLACS-only width collapses to `0.294`, and σ_ap now *lowers* B instead of raising it |
| 2 | `no_boot` | the SPARC error becomes the formal Δχ² = 1 value (`1.12688%`) instead of the 200-draw bootstrap (`0.093888688`) | **C15, C23, C24** | the error model is what decides the thermal-vs-½ question: Δχ² jumps from `1.824508` to `159.0666` (LR → 1e34), σ(κ) falls to `0.11175`, and the raw/compressed ratio inverts to `0.3` |
| 3 | `thermal_off` | the thermal coefficient is `cH_Λ/π` instead of `cH_Λ/2π` — a factor-2 slip of the kind A79 found in the external package | **C5, C10b, C11, C15, C18, C19, C20, C23** | the two fixed points and every identity that uses a0 are live: κ_P3(thermal) becomes `0.761858`, `L*` halves to `12.72126 pc`, `y_t` leaves its band, and the thermal point is `+14.90 sigma` from the fit |
| 4 | `imf_prior` | Treu's prior is widened from 0.036 to 0.100 dex (the cross-method IMF spread) | **C12, C13, C14, C17** | the 2σ IMF tension is a statement about the prior's width: the pull falls to `+0.91σ`, T falls to `1.045`, and B collapses onto `B_req` (`1.23435`, 0.006 away) |
| 5 | `drop_sigma_ap` | the A85 σ_ap term is removed from `slacs_at` even when requested | **C17** | the σ_ap variant is actually in the likelihood: with it dropped the B shift is `+0.00%` instead of `+0.49%`, and C17's monotonicity (formal > honest) fails |
| 6 | `sersic_default` | the SLACS baseline is Sérsic n = 6 (A80's slope-zeroing index), a uniform `+0.0868` shift in `ln r_i` calibrated at the thermal point | **C11, C13, C16** | the n-band is a real systematic: A81's B falls to `1.0985` (`-10.41%` from A85), the IMF pull falls to `+1.03σ`, and the SLACS-only width shrinks to `0.267` |
| 7 | `vacuum_beta` | the background is evaluated on A33's `Ω_Λ,eff = 1` slice (matter dropped), i.e. the 1.462 floor that A78 corrected | **C21** | the β identity is not a tautology: `r_Λ(β=0)` becomes `1.460494`, ΔN_eff at the bound becomes `+3.44463`, and `r_Λ(β_max)` becomes `0.53819` |
| 8 | `drop_lens` | the SLACS census loses every 7th lens (70 → 60) | **C1, C6, C7, C11** | the data-integrity and model-reproduction checks are live: the census fails, the median ratio moves to `0.889986`, `B_req(½)` to `1.1699`, and B(n=4) to `-1.10%` from A85 |
| 9 | `sd_at_b1` | A80's "B profiled" column is computed at `boost = 1` — exactly A71's `SD_TAB` defect | **C8** | C8 is not two evaluations of the same model: the profiled Δ reverts to `6.3517`, i.e. the check detects the very artefact it was built to detect |
| 10 | `floor10` | the SPARC per-point floor is widened from 5% to 10% | **C2, C3, C4, C13, C15, C24** | the SPARC calibration is live: the zero-parameter χ²/dof moves off `6.8651`, the best fit moves off A51's stored `8.081465e-11`, and both the pull and the error-model ratio change |

## Coverage, stated honestly

**22 of the 27 checks are killed by at least one mutation**: C1–C8, C10b, C11–C21, C23, C24.

The five survivors are calibration and identity checks on **imported** numbers, which no dial inside
this lane can move without changing the imported value itself:

| check | why no single-input mutation can kill it |
|---|---|
| C9 | A18's anchor (`1.6863 / 3.7702 / 2.6179`) is a reproduction of A18's published numbers; the mutation would have to be inside A18's solve, which is not this lane's code |
| C10 | A85's Fisher audit compares A85's published matrix against A85's published det/cond/σ/angle — a two-route consistency check on *their* numbers |
| C22 | the rank/nullity of `γ = KL*²/2`, `σ_c² = a0L*` is exact linear algebra; every mutation that changes a0 changes both sides together |
| C25 | the ledger's completeness (9 symbols, 5 classes) is a bookkeeping identity |
| C26 | the anchor re-derivation is the same two-route structure as C10 |

These are listed rather than hidden: A81 claims 22/27 mutation coverage, not 27/27. The 22 that are
covered include every check that evaluates the likelihood, the profiling, the error model, the ledger
identities and the data census.
