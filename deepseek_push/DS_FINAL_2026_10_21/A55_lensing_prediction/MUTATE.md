# A55 mutations

Four, each run as `A55_MUTATE=<name> python3 a55_checks.py`, each writing its own
`a55_MUTATE_<name>.out` / `a55_MUTATE_<name>_results.json` and each exiting **1**.
The unmutated run exits 0 with **25/25**.

Every mutation is a *physics* change, not a tolerance tweak: it removes one leg of the argument and the checks
that depend on that leg must break.

## M1 — `newton`: the extra sector switched off

`A0_RUN = 1e-30`, so the law collapses to Newton (`g = g_N`) and the phantom disappears. The baryons are unchanged,
the data are unchanged.

| check | unmutated | mutated |
|---|---|---|
| K9 headline `R_E,pred/R_E,obs` | 0.8852 (4.9σ) | **0.7536 (10.6σ)** (FAIL) |
| K11 “the phantom closes part of the Newtonian gap” | 53 % closed | **0 % closed** (FAIL) |
| K12 footing independence | 0.866 vs 0.885 | **0.866 vs 0.754** (FAIL) |
| K13c tabulated-`M_*` route | 0.824 (7.5σ) | **0.689 (12.5σ)** (FAIL) |
| total | 25/25 | **21/25, exit 1** |

What it proves: the 0.885 is the *law's* number, not a baryon-only number. Remove the sector and the prediction drops
to 0.754 — the phantom is doing 0.13 of the 0.25 total shortfall in radius, and the residual is a pure mass
normalisation problem. It also shows that K9's tolerance band (0.85–0.93) is tight enough to catch a 0.13 change.

## M2 — `chabrier`: the headline branch switched to the light IMF

`IMF_HEAD = "Fc"`; `a₀` unchanged. This is the *same* model with the other measured stellar normalisation.

| check | unmutated | mutated |
|---|---|---|
| K9 headline | 0.8852, 4.9σ | **0.5533, 20.2σ** (FAIL) |
| K11 phantom closes part of the gap | 53 % | **−81 %** (FAIL — the "worse than Newton" branch) |
| K12 footing independence | 0.866 vs 0.885 | **0.866 vs 0.553** (FAIL) |
| total | 25/25 | **22/25, exit 1** |

What it proves: the IMF branch, not `a₀` and not the profile, is the dominant systematic — 0.26 dex in `M_*` moves
`R_E` by 0.26 dex. It also shows that the K9 band is *not* so wide that both branches pass: the two branches are
3.6σ apart in the same direction, which is why the lane must report both and cannot quote a single number.

## M3 — `noproj`: the line-of-sight projection dropped

`M2D_from_g` returns the **3D** mass `M_tot(<R)` instead of the projected cylinder mass. This is the single most
common error in this kind of calculation (using `M(<R)` where `M_2D(<R)` is required), so it gets its own mutation.

| check | unmutated | mutated |
|---|---|---|
| K4c projection identity | `−1.4×10⁻⁴` | **`−0.68`** (FAIL) |
| K9 headline | 0.8852 (N=70) | **0.5813, 16.4σ (N=69)** (FAIL) |
| K11 | 0.754 → 0.885 | **0.581 → 0.581** (FAIL) |
| K13c | 0.824 | **0.535 (19.2σ)** (FAIL) |
| K14 `a₀×100` sensitivity | 5.32 | **0.581** (FAIL — no sensitivity at all) |
| K15 `n` scan | 0.877/0.885/0.893 | **0.474/0.581/0.656** (FAIL) |
| K17 shape comparison | Δslope ≤0.14 | **NFW fit impossible** (FAIL) |
| total | 25/25 | **18/25, exit 1** |

What it proves: the projected boost is not a detail. At `R_E` the 3D boost is ~1.1 but the *projected* boost is ~1.45,
because the line of sight passes through the low-acceleration outskirts where the phantom is relatively stronger.
Dropping the projection costs 0.30 dex in `R_E` — four times the effect being tested. K4c is the check that catches it,
and it is the reason K4c exists as an independent route rather than a restatement of K4.

## M4 — `slipzero`: the `O(Ψ)` correction set to zero

`cn_ref = 0` in K7 only: the deflection is asserted to be *exactly* the dynamical one.

| check | unmutated | mutated |
|---|---|---|
| K7 correction size | `2.31×10⁻⁶` / `5.01×10⁻⁵` | **`0.00` / `0.00`** (FAIL) |
| total | 25/25 | **24/25, exit 1** |

What it proves: K7 asserts the correction is *present and of the predicted size*, not merely small. “Lensing =
dynamics at `O(ε)`” is a statement about the leading order; a code that silently drops the first correction would
still pass every observational check in this lane (the correction is 8600× below the error), so the only place the
correction can be tested is here, against the analytic `c_n`. That is why K7's band is two-sided
(`1e-6 < frac < 1e-5` for galaxies, `1e-5 < frac < 1e-4` for clusters) rather than a one-sided upper bound.

---

## What the mutation set as a whole shows

| mutation | fails | the leg it removes |
|---|---|---|
| `newton` | K9, K11, K12, K13c | the sector's contribution to the lensing mass |
| `chabrier` | K9, K11, K12 | the baryonic normalisation branch |
| `noproj` | K4c, K9, K11, K13c, K14, K15, K17 | the projection from 3D to the lens plane |
| `slipzero` | K7 | the `O(Ψ)` slip correction |

No mutation breaks a check it should not: `slipzero` leaves all 24 observational and identity checks untouched
(the slip is unobservable, by design), and `newton` leaves the Task-1 derivation untouched (K1–K7 all pass), because
the law's algebra is independent of whether the phantom is switched on in the SLACS run.

The one mutation that is *not* a physics error but a legitimate alternative — `chabrier` — still fails, and that is
deliberate: the lane's claim is “zero free parameters with a stated IMF”, and the two stated IMFs give answers 0.33 dex
apart. A check set that passed both would be hiding the dominant systematic.