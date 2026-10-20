# CFG912 AMENDMENT A1 (POST HOC: written after the frozen MUTATE was run and FAILED; committed alone before MUTATE-B is run)

## What happened (the frozen MUTATE, outputs kept: `cfg912_score_MUTATE.out`, `cfg912_results_MUTATE.json`)

The frozen MUTATE injected one host of log M_b 11.325 at physical d = 0.4 Mpc around every 10th I0 red lens (8,808 hosts).
It **FAILED** all three frozen conditions:
- (i) blue unchanged exactly: P0 exactly 0 on both footings, but P1 canonical differs by 5.0e-29 m/s² (≈ 4e-16 relative).
  This is kernel-cache order: kernels are cached by log10 t rounded to 10 digits, the main run's K2 checks filled some keys
  first, and t values that agree to ~1e-12 share an entry. It is roundoff, not a pipeline difference.
- (ii) P0 red change = direct per-lens computation to ≤ 1% per bin: the two bins carrying most of the signal agree to 0.05% and
  0.4%. Two bins miss: k = 6 by 13% and k = 8 by 3.5%.
  - In k = 6 the net is a near-cancellation (per-lens kernel sums +1990 vs −2242, weight units). The miss is 0.8% of the gross.
  - In k = 8 the 183 contributing lenses (the most massive) all sit at x ≈ 1.74 inside one x bin. There the frozen
    area-uniform within-bin average is not exact for a delta-like separation distribution.
- (iii) "f_env must rise": it fell (P0 canonical +0.070 → +0.004). **The hand expectation was wrong physics.**
  - At d = 0.4 Mpc the host lies inside the window annuli for most lenses (x = d/ρ_l from 1.74 to 8.41; window X ≤ 2.34–3.11).
  - The annulus-averaged ΔΣ of a point mass in the outer ≈ 40% of an annulus is negative: the −M ring term beats 2 ln(X₂/x).
  - So the injection *lowered* the red term in the window.

The frozen MUTATE is reported as FAILED. Nothing in this amendment changes the primary analysis, its classes, brackets or
controls, or any number already produced.

## MUTATE-B (added post hoc; separate outputs `*_MUTATE_B*`)

- Same injection as the frozen MUTATE (log M_b 11.325, every 10th I0 red lens, Δχ = 0, c1w = 1, seen only by its lens),
  except **d = 0.01 Mpc**. Then x = d/ρ_l ≤ 0.31 < X₁ of every computed annulus (≥ 0.321).
- The host is interior to every annulus, so its kernel is the constant 2 ln(X₂/X₁): a pure positive red-only excess in every
  window bin, with no ring term and no within-bin averaging error.
- **Recovered** if all of the following hold:
  - (i) blue unchanged: P0 exactly 0; P1 ≤ 1e-12 relative (the cache-order roundoff above);
  - (ii) the P0 red change matches the direct per-lens computation to ≤ 1% in every computed bin;
  - (iii) f_env rises (P0 and P1, both footings).

## Diagnostics for the frozen MUTATE (reported in the MUTATE-B output; no verdict weight)

- f_env recomputed with the main P0 red vector plus the *direct* expected injection. If the pipeline transmits the injection
  faithfully, this equals the pipeline's MUTATE f_env.
- Per bin: |recovered − direct| as a fraction of the gross (Σ|per-lens terms|) injection.

κ = ½ FITTED; footings never pooled; not theory closed.
