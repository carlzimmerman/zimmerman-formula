# CFG586: is CFG585's old-vs-young early-type difference environment? No — AGE SIGNAL SURVIVES as frozen

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (8124cb1a4). (owner chat, "run the neighbour check")
- **Script:** `cfg586_env.py` → `cfg586_env.out`, `cfg586_results.json`; MUTATE `CFG586_MUTATE=1` (OLD leakage ×3) → `_MUTATE`.
- **Executed unedited (heads only, no outputs written):** `cfg585_age.py` (masks, CFG531 estimator), `cfg509_counts.py` (companion counts).
- K9 is primary because that is where CFG585's hint sits (a follow-up of a post-hoc band choice); K-in reported.
- κ = ½ fitted; footings never pooled; cold energy's mass still required; not theory closed.

## Step 1 — companion counts (no lensing; CFG509's method)
| group | N | companion excess | leakage scale λ | f_leak |
|---|---|---|---|---|
| f30 all | 57,265 | 0.1295 | 0.436 ± 0.017 | 0.074 |
| f30 early | 26,572 | 0.1420 | 0.602 ± 0.030 | 0.095 |
| OLD | 8,843 | 0.1418 | 0.602 ± 0.053 | 0.094 |
| YOUNG | 8,850 | 0.1389 | 0.590 ± 0.050 | 0.092 |

λ_old − λ_young = +0.013 ± 0.066 (Z +0.19). Old and young early types have the same environment at fixed mass.

## Step 2 — lensing re-score with each group's own leakage
| cell | K9 D_raw (Z) | K9 D_env (Z) | ε_old / ε_young (env) | K-in D_env (Z) |
|---|---|---|---|---|
| A canonical | +0.941 (+2.66) | +0.968 (+2.69) | +1.168 / +0.200 | +0.648 (+1.51) |
| A alt | +0.862 (+2.66) | +0.886 (+2.69) | +0.984 / +0.098 | +0.594 (+1.51) |
| B canonical | +0.938 (+2.65) | +0.964 (+2.69) | +1.166 / +0.201 | +0.648 (+1.51) |
| B alt | +0.859 (+2.65) | +0.883 (+2.69) | +0.982 / +0.099 | +0.593 (+1.51) |

- **Verdict as frozen: AGE SIGNAL SURVIVES** (Z ≥ 2 and ≥ half of D kept, all four cells, K9).
- Controls 3/3: C1 CFG509 0.8454; C2 early λ 1.0572; C3 scale 1 reproduces CFG585's D exactly.
- MUTATE: tripling OLD's leakage lowers D(K9) in every cell (to +0.72–0.79, still Z ≈ 2.1): environment would need far more
  than 3× its measured contamination to remove the signal.

## Reading (not a verdict)
- At fixed stellar mass and the same environment, older early types carry ≈ +1.0–1.2 excess (K9) and younger ones ≈ +0.1–0.2:
  the law's shortfall tracks FORMATION HISTORY, not present-day baryons or neighbours.
- The law predicts lensing from present baryons alone, so it cannot produce a colour/age dependence at fixed M_b. Whatever
  supplies the extra mass remembers when the galaxy formed. In ΛCDM language this is the known halo-assembly dependence
  (earlier-forming systems sit in more massive / concentrated halos at fixed M*); in the framework it would mean the cold
  energy accumulates or settles with time (owner's idea) — no mechanism exists in the record yet.
- Remaining confounds: a colour-dependent stellar-mass error would need ≈ 0.5 dex between groups 0.25 mag apart (implausible);
  dust and metallicity also redden. The K9 band choice followed CFG585's post-hoc look; the primary-band (K-in) result stays
  Z ≈ 1.5. Treat as the strongest lead in the record, not an established result.
