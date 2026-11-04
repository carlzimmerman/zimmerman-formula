# LAM5: BOSS fibres as spin labels for a lensing split (stage 0)

Criteria `a5617b4742` (frozen first). kappa = 1/2 FITTED; not theory closed.

**LABEL: NOT FEASIBLE.** F1 needs 42,000 gas-poor BOSS galaxies with S/N >= 20 and fibre coverage c >= 0.5.

| BOSS galaxies, 0.15 <= z <= 0.55, zWarning 0, velDisp >= 100, err < 10 % | N |
|---|---|
| all | 230,144 |
| S/N >= 10 | 84,198 |
| S/N >= 20 (LAM2's K2-backed cut) | **7,790** |

**Disclosure: the gas-poor join failed.** No BOSS row matched `emissionLinesPort` in this query, so every gas-poor
count prints 0. That is a query failure, not a physical result, and it is not fixed after the fact. The verdict
does not rest on it: S/N >= 20 alone leaves 7,790 galaxies before any gas or coverage cut, 5.4x short of F1.
Every gas or coverage definition can only lower that number.

## Reading
BOSS spectra of massive galaxies at z 0.15-0.55 are too noisy to measure h4 galaxy by galaxy at the S/N where
LAM2 K2 measured it (rms 0.027 at S/N >= 20). Even S/N >= 10, below any tested h4 recovery, gives 84,198 before
cuts. So spin labels for a spin-split lensing sample cannot come from BOSS fibres one galaxy at a time, and
LAM1's question stays unanswerable on public data. LAM4 stands as an estimator result for IFU-summed spectra.

Files: `lam5_stage0.py`, `lam5_stage0.out`, `lam5_stage0.json`.
