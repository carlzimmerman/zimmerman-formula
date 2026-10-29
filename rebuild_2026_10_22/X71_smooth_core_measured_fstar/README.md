# X71_smooth_core_measured_fstar

**Question (the owner, 10-29: "stress-test it").** Does X70_smooth_core_shape's canonical full pass survive measured
stellar fractions? The pass assumed X43's f★ = 0.20 (stars = 20 % of gas, following the gas). This lane uses CFG408's
injection, applied uniformly. Criteria were frozen first (d5c36c6402).

## Verdict: BREAKS: G-OUT-M3 (UNDER), canonical h 0.672, in both measured-f★ variants

| f★ | shape | G-OUT-M3 Z (h 0.672 / 0.686) | other cluster fails | groups | SPARC |
|---|---|---|---|---|---|
| 0.20 (identity) | smooth | +1.88 / +1.56 | none | +1.94 ✓ | pass (canonical) |
| **0.0615** (X-COP-7 median) | smooth | **+2.25** / +1.92 | none | +1.94 ✓ | unchanged |
| **0.034** (CFG922 A1 central) | smooth | **+2.33** / +2.00 | none | +1.94 ✓ | unchanged |
| 0.0615 | Burkert (X43) | +2.75 / +2.40 | — | +2.05 ✗ | — |
| 0.034 | Burkert (X43) | +2.83 / +2.47 | — | +2.05 ✗ | — |
| 0.60 (MUTATE) | smooth | +0.99 / +0.70 | 5 keys OVER | — | — |

- With realistic stars the heavy-cluster outskirts are short again. The miss is narrow (Z 2.25–2.33 in the h 0.672 cell;
  the h 0.686 cell passes at 1.92–2.00).
- **Every other key still passes:** the 14 other cluster keys, G-IN-Mall (−0.9 to −1.1), the groups and SPARC.
- **The smooth core still beats Burkert at the same f★** by about 0.5 in Z on G-OUT-M3, and passes the groups that Burkert
  fails.
- **Alt footing:** the same cluster picture, plus X70's SPARC Υ failure.

**Checks:**
- K1 identity: f★ = 0.20 reproduces X70's committed cluster preds exactly, max |d| = 0, with 9/9 checks.
- **The measured-f★ runs exit 1 by construction.** Two of X43's inherited identity checks, K0 (X30's stored OUTER / MID
  amplitudes) and K0x38, are defined at f★ = 0.20. They move with the injected f★ (0.716 → 0.776) because X30's
  measured-to-baryon ratios are built on the same baryon model, as in CFG408. All other checks pass. No graded number is
  affected.
- MUTATE (f★ 0.60) raises G-OUT-M3's prediction (Z 1.88 → 0.99), so the harness is sensitive.

**Reported discrepancy:** CFG408 gave Burkert G-OUT-M3 Z +3.66 at its tercile f★ 0.034. This uniform injection gives
+2.83. CFG408's KiDS part used per-tercile values and stored-X7 error rescaling flagged APPROXIMATE (its K5), and it is
ungraded (K2). The direction agrees; the size differs.

## Reading

- **X70's full pass depends on the assumed stellar fraction.** With either measured value, the heaviest-cluster outskirts
  are under-supplied at Z ≈ 2.3 in one h cell. That is the same residual CFG406–408 kept finding: a real heavy-cluster
  outer excess, here reduced to about 2σ.
- **What still stands:** the smooth core is strictly better than Burkert on every graded key at every f★ tested. Groups
  pass and inner bands pass. The remaining tension is one key, at about 2.3σ.
- **What decides it next:** the native c_f(M) from the X48 A4 zooms. Higher c_f at cluster mass raises G-OUT-M3's
  prediction. Regrade X70's shape with native c_f AND measured f★ together.

κ = ½ FITTED; c_f EXTERNAL; not theory closed. Nothing here says the data favour the framework.

## Files and reproduction

Files: `FROZEN_CRITERIA.md`, `x71_fstar.py`, `x71_fs{0.2,0.034,0.0615,0.6}_S.out` / `_results_*.json`,
`x71_fs{0.034,0.0615}_B.*`, `x71_x30_machinery.log`.

    X71_FSTAR=0.034 X71_SHAPE=S PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x71_fstar.py   # ~60-80 s each
