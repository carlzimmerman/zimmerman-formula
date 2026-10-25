# X39_baryonic_contraction: contraction does not rescue the heavy cluster cores, and it breaks SPARC

Criteria: `FROZEN_CRITERIA.md` (b75acfc767, committed alone). `AMENDMENT_A1.md` (post-result, check code only: K1's
point-mass test range and grid; every graded line is identical to RUN1). κ = ½ FITTED. Footings never pooled. Route E,
Newtonian, cold dark energy not matter. Not "theory closed". Nothing here says the data favour the framework.

**Question.** X38's a₀-cored halos (ρ₀r₀ = a₀/2πG) pass SPARC and the cluster outskirts but under-predict the heaviest
cores. Does adiabatic contraction by the baryons (gravity only) close that gap? The BCG comes from CFG922; Blumenthal is
primary, Gnedin reported.

## Verdict: **SD + AC FAILS** (both footings)

| | X38 (no contraction) | X39 (Blumenthal) | needed |
|---|---|---|---|
| SPARC rms / median Υ, canonical | 0.0795 / 0.77 PASS | 0.0618 / **0.39** FAIL | Υ ≥ 0.50 |
| SPARC rms / median Υ, alt | 0.0729 / 0.60 PASS | 0.0636 / **0.32** FAIL | |
| MID T3 (canonical) | 1.05 (Z +4.3) | 1.13 (Z +3.9) | 2.13 |
| MID KT slope | −0.04 (Z +3.1) | +0.16 (Z +2.8) | +2.24 |
| MGAS T3 OUTER | 0.82 (Z +5.4) | 0.87 (Z +4.8) | 1.37 |
| OUTER all-KT | 0.70 (Z +0.1) | 0.73 (Z −0.1) | 0.72 ✓ |

- **Clusters:** contraction moves the heavy cores by only +0.08 in A, against the +1.0 needed.
  - The BCG (median 6e10 M☉) is negligible at 0.3–1 Mpc: with no BCG, a = 5 kpc and a = 20 kpc the results are identical.
  - The gas is too extended to contract a 0.3–0.4 Mpc core.
  - Gnedin gives the same result.
- **SPARC:** the same physics shrinks galaxy cores. The baryons dominate inside a few kpc, so contraction rebuilds the
  cusp that X38's cores had removed. Υ falls back to 0.32–0.39, which is EM1's cusp failure again. Gnedin fails too
  (Υ 0.35–0.42).
- The coordinator's warning (point 2) is borne out: **any process that makes cluster cores denser through baryons makes
  galaxy cores denser first.**

**Checks 4/4** (K0 X38 reproduced with contraction off; K1 Blumenthal limits, point-mass + SIS closed form to 1.3e-8;
K2 CFG922 BCG matches 190 = X21; K3 0.61 GB). `--mutate` ((1 − F)) fails K1 at 0.47, exit 1.

## Reading

- X38's lead stands as **SD without contraction**. Its failure is specific: the heaviest clusters need about twice the
  0.3–1 Mpc mass that a fixed a₀-surface-density core gives, and baryonic contraction cannot supply it without breaking
  galaxies.
- So the surface density cannot be universal. Cold dark energy cores must be denser in massive systems, by roughly a
  factor 2 at cluster masses, while staying at a₀/(2πG) in galaxies. Equivalently, the cold-dark-energy core radius must
  grow more slowly with mass than a fixed Σ allows.
- That is the precise remaining requirement. It is a scaling of the cold sector's own core physics with halo mass, not
  something baryons can do.

## Files

`FROZEN_CRITERIA.md`, `AMENDMENT_A1.md`, `x39_contraction.py`, `.out` / `_results.json`, `_RUN1` (before A1), `_MUTATE`,
`x39_x30_machinery*.log`.

    PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x39_contraction.py            # exit 0, 4/4
    PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x39_contraction.py --mutate   # exit 1, K1 fails
