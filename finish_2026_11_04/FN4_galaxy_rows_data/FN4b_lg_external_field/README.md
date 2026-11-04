# FN4b_lg_external_field: FIELD MOVES NOTHING on both footings. No class shows an external-field-signed trend; every class leans the other way, none at p < 0.01

Criteria: `FROZEN_CRITERIA.md`, committed alone before the script. κ = ½ FITTED. Not theory closed. Nothing here says the data favour the framework. No download. Script `fn4b_field.py`; numbers in `fn4b_field.out` and `fn4b_field.json`.

This builds the estimator the law-rule ledger listed as missing: the Local Group external field from a catalogue (UNGC, 869 galaxies, M_b = 0.6 L_K + 1.33 M_HI) plus the Milky Way (7.0e10 M☉) and M31, as a Newtonian vector sum at each of X1's 89 systems.

## Labels (frozen)
| | canonical | alt |
|---|---|---|
| T2 size | **FIELD MOVES NOTHING** | **FIELD MOVES NOTHING** |
| T1 sign test, every class with n ≥ 5 | **NO TREND** | **NO TREND** |

## By class (canonical; alt within 0.1 in log y_e and the same labels; `fn4b_field.out`)
| Class | n | median Δ (iso law) | median log y_e | non-host share of the field | median shift ΔE (dex) | σ_c | Z before → after | Spearman ρ, p |
|---|---|---|---|---|---|---|---|---|
| MW ultra-faint | 31 | +0.596 | −1.69 | 0.084 | +0.013 | 0.113 | +5.25 → +5.36 | +0.20, 0.27 |
| MW classical | 8 | +0.243 | −1.91 | 0.106 | +0.009 | 0.145 | +1.67 → +1.75 | +0.69, 0.07 |
| bright M31 | 25 | +0.220 | −2.61 | 0.081 | +0.0002 | 0.103 | +2.14 → +2.14 | +0.03, 0.91 |
| M31 others | 5 | +0.777 | −2.41 | 0.059 | +0.002 | 0.327 | +2.38 → +2.39 | +1.00, 0.02 |
| LG field (incl. IC 1613) | 13 | +0.036 | −3.68 | 1.000 | +0.00001 | 0.081 | +0.44 → +0.44 | +0.44, 0.13 |
| M31 dE, MW individual | 3, 4 | | | | ≤ 0.016 | | | too few |

## Reading
- **Satellites:** the rest of the Local Group adds 4–11 % to the host's field (class medians). In CZ1's one-zone form that moves the medians by at most +0.013 dex, in the direction that makes the law shorter, against class errors of 0.10–0.33.
- **Field dwarfs:** y_e is 10^−4.1 to 10^−3.1 a0, against internal fields of about 0.01–0.03. The largest shift is 4e-4 dex (Phoenix). IC 1613's field is 4.0e-4 a0 with every UNGC galaxy, against CZ1's 3.4e-4 from the Milky Way and M31 alone.
- **Sign:** an external-field effect predicts residuals falling as the field rises (ρ < 0). Every class has ρ > 0. The strongest are M31 others (+1.00, p 0.02, n 5) and MW classical (+0.69, p 0.07; alt +0.74, p 0.047). None reaches the frozen p < 0.01. This matches UX4's host-field slope, −0.05 ± 0.20 per dex against a predicted −0.75.
- So the external-field door for the Local Group rows is closed on a catalogue estimator. IC 1613 wants less gravity and its field is negligible. The dwarfs want more and the field can only make the law shorter.

## Checks
K1 reproduces CZ1 Part D's IC 1613 field (3.3564e-4 / 2.7773e-4 a0) with relative difference 0. K2 point mass and ring PASS (≤ 1e-15). K3: 63 systems have their own UNGC row excluded, none more than one; IC 1613 excluded. K4: 89 of 89 systems matched to LVD. MUTATE (UNGC distances × 0.5): K1 fails (y_e ×3.98), exit 1. Rerun byte-identical. Two seconds, 0.08 GB.

## Limits
Point masses throughout, including the hosts. Υ_K 0.3 and 1.0 brackets are stored in the JSON (`log_ye_ups03`, `log_ye_ups10`) but not graded. The one-zone form is CZ1's approximation, not a solver. UNGC stops near 11 Mpc, so the large-scale field beyond it is missing; for the satellites the host dominates in any case.

κ = ½ FITTED. Not theory closed.
