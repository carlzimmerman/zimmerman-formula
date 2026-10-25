# X40_fixed_core_radius: a fixed-size cold dark energy core fails both SPARC and clusters

Criteria: `FROZEN_CRITERIA.md` (b37983a0f7, committed alone). `AMENDMENT_A1.md` (post-result, check code only; graded
lines identical to RUN1). κ = ½ FITTED. Footings never pooled. Route E, Newtonian, cold dark energy not matter. Not
"theory closed". Nothing here says the data favour the framework.

**Hypothesis FC.** The halo core has one physical size r_c in every system, as a self-interacting field's Thomas–Fermi
core would. The motivation: X38's fixed surface density gives r₀ ∝ √M, too wide in big clusters. r_c is calibrated on
SPARC only, and the clusters are graded once.

## Verdict: **FC FAILS** (both footings)

- **SPARC fails the line.** The best fixed core is r_c = 9.7 kpc (7.9–10.8 within Δrms 0.002), at rms 0.119 / 0.121 with
  median Υ at the grid ceiling of 1.20. Smaller r_c recreates the cusp (Υ 0.30); larger r_c starves the massive discs. No
  single size fits SPARC's diversity. X38's fixed surface density did (rms 0.073–0.080, Υ 0.60–0.77).
- **The clusters fail high.** A 10 kpc core packs the fair share far too centrally: MID T1–T3 come out 2.8 / 3.3 / 4.5
  against 1.1 / 1.65 / 2.1 (Z −4.7 to −9.4), INNER 23 against 1.9, and OUTER 1.16 against 0.72.
- The neighbouring r_c values fail the same way.

**Checks 5/5** (X38's machinery K0 and this lane's K0, which reproduces X38's SD; K1 normalisation and closed form; K2
cusp limit; K3 0.63 GB). `--mutate` fails K1, exit 1.

## Reading: what X38 + X39 + X40 pin down together

| core rule | SPARC | cluster outskirts | heavy cluster cores |
|---|---|---|---|
| fixed surface density a₀/(2πG) (X38) | **PASS** | **PASS** | ×2 short |
| + baryonic contraction (X39) | FAIL (cusp) | pass | still short |
| fixed core size (X40) | FAIL | FAIL (over) | FAIL (×2–4 over) |

- The core surface density is the right variable: it is constant across galaxies, at a₀/(2πG), and a fixed length is
  wrong.
- Between a fixed Σ (cores too wide in clusters) and a fixed length (cores far too narrow), the heavy clusters sit in
  between. **Their core surface density is about twice a₀/(2πG).** The record's measured requirement is Σ_core ≈ a₀/(2πG)
  in galaxies, rising by about ×2 by M_b ~ 3×10¹³ M☉.
- No mechanism tested here produces that rise: not baryons (X39), not a fixed length (X40), not orbit-keyed depletion
  (X37). That is the single remaining, quantified piece.

## Files

`FROZEN_CRITERIA.md`, `AMENDMENT_A1.md`, `x40_fixed_core.py`, `.out` / `_results.json`, `_RUN1`, `_MUTATE`,
`x40_x30_machinery*.log`.
