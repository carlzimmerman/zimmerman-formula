# CFG786: CFG779's FRB exclusion under its own assumptions

**Label: WEAKENED (as frozen).**
- Every systematic variant keeps the Croker-like baryon-eating case excluded at ≥ 5.1σ. That includes the worst
  combination of all four individually varied assumptions: B = 0.927 [0.880, 0.976], Z = 5.12.
- The declared stellar-channel escape route lowers it to 2.5σ, for a condensed budget of 0.24 (Croker's ×2 SFRD).
- K1 PASS: V0 reproduces CFG779's ln B = +0.062.

- **Criteria:** `FROZEN_CRITERIA.md` (7ca119528). Run 2026-10-15 right after T1x. Output in `cfg786.out` / `cfg786_results.json`.

| variant | ln B (68%) | Z (P2, s_b = 0.70) |
|---|---|---|
| V0 baseline | +0.062 (+0.010, +0.115) | 7.78 |
| h = 0.67 / 0.73 | +0.018 / +0.104 | 6.96 / 8.59 |
| Salpeter f_d | +0.093 | 8.50 |
| wide host box | +0.057 | 8.04 |
| Ω_b h² +2σ / −2σ | −0.032 / +0.167 | 6.00 / 9.83 |
| strict sample | +0.014 | 6.61 |
| **V6 worst combined** (h 0.67, Chabrier, authors' host box, Ω_b h² +2σ) | −0.076 (−0.128, −0.024) | **5.12** |
| escape, fc 0.12 / 0.24 | — | 5.33 / **2.48** |

**Disclosures.**
- V6 was chosen from each variant's direction, as the criteria intend. The frozen file's parenthetical named the
  opposite ends; the script used the true worst directions.
- The escape route assumes the converted baryons come entirely from the stellar channel. That is the remaining
  loophole, reported in PAPER50 (DOI 10.5281/zenodo.23396865).
- Limits on the inputs are those of CFG779/CFG632.
- κ fitted; not theory closed.
