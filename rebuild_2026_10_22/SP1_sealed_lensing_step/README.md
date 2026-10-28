# SP1_sealed_lensing_step: a sealed prediction for isolated-galaxy weak lensing

## Provenance

- **Criteria:** `FROZEN_CRITERIA.md` (1048b648fa), committed alone before any number.
- **Seal:** `SEAL.md` (the sha256 of `sp1_predictions.json`, byte-reproducible).
- **Machinery:** X53's committed lens code. The law branch is computed as X62's LF_M, and it reproduces X53's law-only χ²
  exactly (160.70 / 127.60). The halo branch is X53's `mass_H` with CL2's c_f(M).

**Run conventions.** κ = ½ FITTED. Footings are never pooled. Cold dark energy is a gravitating w ≈ 0 field component, not
a particle. Not "theory closed". This is a prediction for future data, not a claim about it.

## The prediction (frozen CL2 picture: switch M200 = 10^12.3, L = 4, native S9 slope)

**Where the switch sits.** Isolated central galaxies switch from the law-only branch to the cold dark energy halo branch
at **log M★ ≈ 11.21**, on both footings (M200 = 10^12.3 through EM1's relation).

**What the lensing does above the switch.** The outer lensing signal *drops*. The law's extended phantom field keeps ΔΣ
high out to megaparsecs, while route E's halo is truncated at R200.

| log M★ | branch | ΔΣ / ΔΣ_law at 0.1 / 0.5 / 1.0 Mpc (canonical) |
|---|---|---|
| 10.3–11.1 | law | 1.00 / 1.00 / 1.00 |
| 11.3 | halo | 1.04 / 0.46 / 0.23 |
| 11.7 | halo | 1.06 / 0.65 / 0.33 |

**The sealed step statistic.**
- S_step (R = 0.5 Mpc, 0.2 dex bins either side of the switch) = **0.47 canonical, 0.43 alt**.
- With 0.15 dex scatter in mass it is **0.76 / 0.73**.

**Falsifier (frozen).** The prediction fails if a future isolated-lens stack (KiDS-Legacy, Euclid DR1, or DESI × KiDS/HSC)
shows either of these:
- **no drop,** meaning S_step is above 1 + 0.5 (S_pred − 1) at 3σ;
- **a misplaced step,** with the step more than 0.3 dex in M★ from 11.21.

A smooth halo–mass relation predicts S_step ≥ 1.

## Checks

- **K1:** the switch off gives Q ≡ 1, by construction.
- **K2:** the law-only stack reproduces X53's committed χ² on both footings.
- **K3:** under 1 GB.
- **Rerun:** byte-identical predictions hash.
- **MUTATE twin:** the switch at 10^13.3 moves M★,sw off the grid (> 11.7, at least 0.49 dex higher), as required.

## Files

- `sp1_predict.py`
- `sp1_predictions.json` (sealed)
- `SEAL.md`
- `sp1_predict.out`
- `*_MUTATE.*`
