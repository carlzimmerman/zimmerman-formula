# CFG464: the zero-constant t_dyn settling rate (λ = 1) on the corrected ledger. NOT EXCLUDED; this supersedes CFG429's verdict

Criteria: `FROZEN_CRITERIA.md` (bbecbb93c, committed alone before the script). Script: `cfg464_tdyn_corrected.py`.
Outputs: `cfg464_tdyn_corrected.out`, `cfg464_results.json` (MUTATE: `*_MUTATE.*`). CFG429 itself is not edited.

**Verdict: NOT EXCLUDED (robust). This replaces CFG429's "ZERO-CONSTANT t_dyn RATE EXCLUDED".**
- On the corrected ledger, all 8 group and cluster rows keep positive cold mass at λ = 1 on both footings.
- The Milky Way 30-kpc row is the only one that can go negative. Its sign depends on the circular speed and on the MW
  baryon mass, so it cannot reverse the verdict under the frozen rule.

## What was corrected
CFG429 scored Γ = λ/t_dyn with λ = 1 on T15's rows, which had two input faults.
1. **Group and cluster deficits were in the wrong units (CFG453).** They used CFG382 definition A, x_A, in place of T15's
   own x = (M_tot − M_b)/M_b. Here x is computed per object from the X-COP and Lovisari data, exactly as CFG453 reads them.
2. **The MW row mixed two baryon masses (10-08 audit, a2).** Its x implied M_b = 1e11 while its S used M_b = 7e10. Here
   each MW row uses one M_b throughout, and both 7e10 and 1e11 are reported.

Two further points:
- The gas radius was already right. CFG450 showed the gas is read at R500.
- CFG429's a0 = 1.2e-10 is replaced by the two footings, reported separately. The 1.2e-10 rows are printed for reference
  only.

## Group and cluster rows (M_cold/M_b at λ = 1; b = 0 / b = 0.3)

| | canonical 9.3603e-11 | alt 1.1312e-10 |
|---|---|---|
| clusters, (i) T15 conventions | **+0.78** / +3.40 | **+0.30** / +2.92 |
| clusters, (ii) per-object S | +2.22 / +4.86 | +1.88 / +4.52 |
| groups, (i) | +5.47 / +10.55 | +4.89 / +9.97 |
| groups, (ii) | +4.22 / +9.44 | +3.48 / +8.70 |
| objects with negative M_cold, (ii) | 0 of 27 at either b | 0 of 27 at either b |

- CFG429 had these rows at −4.1 to −5.4.
- The binding row is clusters at b = 0 under T15's fixed-mass convention. It is thinnest on the alt footing (+0.30).
- The worst single objects are A2319 (clusters, +1.6 to +1.9) and A194 (groups, +1.3 to +2.0), both at b = 0.

## Milky Way at 30 kpc (M_cold/M_b at λ = 1; one M_b per row)

| footing | M_b | V = 188 | V = 200 | V = 230 | zero crossing V0 | label |
|---|---|---|---|---|---|---|
| canonical | 7e10 | +0.06 | +0.52 | +1.80 | 186.5 km/s | robust-positive (thin at 188) |
| canonical | 1e11 | −0.53 | −0.20 | +0.70 | 207.1 km/s | speed-dependent |
| alt | 7e10 | −0.24 | +0.23 | +1.52 | 194.2 km/s | speed-dependent |
| alt | 1e11 | −0.77 | −0.44 | +0.46 | 215.3 km/s | speed-dependent |

- **M_cold ≥ 0 requires V ≥ V0.** With M_b = 7e10, the MW is feasible at the measured 188 km/s (CFG451's value) only on
  the canonical footing, by 0.06 M_b. With M_b = 1e11, it is negative at 188 and 200 km/s on both footings.
- **CFG429's mixed row** (x at 1e11, S at 7e10) gives −1.00 / −0.68 / +0.22 (canonical) and −1.29 / −0.97 / −0.07 (alt).
  It is shown for history and not scored.
- The MW baryon mass inside 30 kpc moves V0 by about 20 km/s, more than the footing does. This row cannot decide anything
  until that mass is pinned.

## What "not excluded" means here
- **At λ = 1, settling is complete.** f = 0.99999 at R500 and 1.000000 at the MW, so the ledger reduces to
  M_cold/M_b = x − S.
- **The kernel supply S equals the law's own phantom.** Per object, S/M_b agrees with ν − 1 to within 0.0011.
- **So at λ = 1 the cold mass is simply the mass beyond the law.** It equals 5.364 x_A, the definition-A excess. The rows
  are positive because groups and clusters hold mass beyond what the law gives from their baryons. That is the known
  cluster residual, and **the cold fluid's mass is still required.**
- **The budget no longer tests λ at group or cluster scale.** Those rows give no upper bound on λ (as CFG453 found), and
  this lane does not show that λ = 1 is preferred.
- **The MW row is the only one that discriminates.** At f = 1, a negative MW row means the full law, applied to that M_b,
  over-predicts the 30-kpc rotation. That is a statement about the MW's baryon mass and speed as much as about the rate.

## Controls (all pass)
- **C1:** the x_T15 medians reproduce CFG453's committed values (to 0).
- **C2:** at λ = 0.028, CFG453's committed rows (i) and (ii) are reproduced on both footings (to 0).
- **C3:** the audit's a2 re-score is matched to 4.5e-4. a2 uses f = 1 exactly and rounded x.
- **C4:** CFG429's own inputs reproduce its committed rows to 0.003.
- **C5:** f(λ = 1) ≥ 0.999992 in every scored row.

## MUTATE (planted CFG429 misread, x := x_A)
- **M1a.** T15's conventions with λ = 0.0073 (its cluster ceiling) bring the binding row, clusters at b = 0, to +0.0019.
- **M1b.** Each footing's CFG451 ceiling (0.00854 / 0.00645) brings it to 0 within 2e-16. This is a code-consistency
  check.
- **M2.** At λ = 1, 0 of 8 group and cluster rows are feasible on either footing. The headline flips to
  MW-SPEED-DEPENDENT.
- **Declared in advance and confirmed:** on the corrected ledger λ = 0.0073 brings no row to zero; they sit at +4.7 to
  +15.5. That is why the mutation plants x_A.

## Caveats
- **T15 conventions kept:**
  - τ = 10.3 Gyr.
  - ρ_R500 = 1.55e-24 kg/m³, a ρ_crit-based (ΛCDM) convention. Even at one tenth of it, f stays 0.975, which would raise
    the rows by about 0.1–0.2 (more positive).
  - Constant hydrostatic b.
  - A placeholder group stellar mass of 0.10 M_gas.
- **Small samples:** 7 clusters and 20 groups.
- **Scope:** this is the T15 settling ledger (the B reading), not a test of candidate B's action, which does not exist.
- κ = ½ is fitted.
- **Superseded on the record:** CFG429's verdict, and its claim that "λ remains a fitted number on this ledger". On the
  corrected ledger, the group and cluster budget does not pin λ at all. The MW-floor calibration λ = 0.028 is still the
  only number tied to data.
