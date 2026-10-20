# W4-12: can one stellar-mass or gas-mass correction reconcile the four κ facts? NO SINGLE CORRECTION

**Bottom line.** No universal stellar-mass factor k or gas-mass factor f makes the record's four κ facts agree.
- **The red/blue lens split (F4) cannot close under any universal correction.** C3 fails in all 289 cells for both stellar-share
  brackets, because a universal factor rescales red and blue lenses alike. That split needs **type-dependent** physics: an IMF
  that varies with galaxy type (CFG926 R5), or cold energy that tracks stellar populations.
- **The within-galaxy gas/star gap (F3) and the rotation-curve/lens agreement (F2 vs F1) can be met together, but only off
  the plausible M/L and gas range.** The nearest such cell is Υ_d 0.71 with gas masses × 0.71, i.e. 29% less gas than SPARC, beyond
  CFG493's ±11.5% gas-scale band. Holding the gas scale, it needs Υ_d ≥ 1.

So the evidence is better described by baryon-type-dependent physics than by one wrong normalisation. **κ = ½ is FITTED.**
Not theory closed.

## The four facts (committed)

- **F1:** gas-dominated rotation curves (p64 B E2): κ 0.557.
- **F2:** blue lenses (W4-06): 0.520.
- **F3:** within-galaxy Δ_g (p64 A): −0.408 ± 0.085 dex at Υ_d 0.5.
- **F4:** red lenses 1.293 vs blue 0.520 (W4-10).

## Results (`w4_12.out`)

- **Grid:** log k ∈ [−0.2, 0.6] and log f ∈ [−0.6, 0.2], step 0.05. The lens stellar share S is bracketed at 1.0 and 0.7.
- **C1** (the gap closes) passes on a diagonal band: higher k or lower f. Inside the plausible region (k 0.8–1.6, f 0.85–1.15)
  it never passes.
- **C2** (rotation curves = blue lenses) passes over a broad region with f ≳ 0.6.
- **C3** (the type split closes) passes **nowhere**.
- **Best C1 ∧ C2 cell** (frozen report; reading: closest to k = f = 1): k 1.41 (Υ_d 0.71), f 0.71. κ_F1 there is 0.702, with
  ½ inside 2σ (0.40–1.23); blue lenses 0.46–0.48.

## Checks and controls

- **K1:** the copied p64 functions reproduce p64's Δ_g (−0.408) and E2 (−9.9816). The vectorised lens fit reproduces blue 0.520
  and red 1.293.
- **MUTATE** (`w4_12_MUTATE.out`, exit 1 by design):
  - **M1**, a mock early-type IMF (red g_bar × 10^0.4), makes C3 passable.
  - **M2**, a mock radial M/L (star-dominated points × 10^0.43), closes C1 at k = f = 1.
  - With both mocks, ONE CORRECTION FITS ALL appears in the plausible region. The method can find a solution when one exists.

## Disclosure: first run

The first normal run (`w4_12_firstrun_nobestcell.out`, kept) omitted the frozen best-C1∧C2-cell report: κ_F1 there and ½
within 2σ. It was added with the reading stated above, and the normal run was redone. No other number changed.

## Files

`FROZEN_CRITERIA.md` (fb52868b4), `w4_12.py` (numpy, 3.6 s, 98 MB), `w4_12.out` / `_results.json`, `w4_12_MUTATE.out` /
`_results_MUTATE.json`, `w4_12_firstrun_nobestcell.out`.

    OMP_NUM_THREADS=1 nice -n 10 python3 why_4_puzzle/W4_12_one_correction/w4_12.py > why_4_puzzle/W4_12_one_correction/w4_12.out
