# EUC13 AMENDMENT A1 (post hoc; disclosed; committed alone, before the script it describes is run)

2026-11-12. Written after the frozen run's numbers were seen. Changes no word, no member, no interval.

The frozen word stands: **EUC13-P NO VERDICT / NO VERDICT** (canonical / alt); f25 statistic CEILING BROKEN / CEILING
BROKEN.

## What changes

Criteria §2 M3.5 asked for two readings bounding the cross-section approximation: the full-form lensing weight with
the lens boost fixed at b = 0 and at b = 0.5, **with the μ-marginal n(z)**. The μ-marginal setting failed validation
(V1) and was dropped by the frozen rule, so `euc13.py` skipped those readings. A1 computes them with the one
surviving setting, **μ = 10**, otherwise exactly as written (catalogued values, 50 draws, seed 20261112, point
estimates only), in a separate script `euc13_posthoc.py` that imports `euc13.py` and changes none of its numbers.

These are readings, not part of the M3 envelope and not the gate. They are post hoc because the setting was chosen
after the validation result was seen (it is the only one left, so there was nothing to choose between).

Adopts nothing. κ = ½ FITTED; not theory closed.
