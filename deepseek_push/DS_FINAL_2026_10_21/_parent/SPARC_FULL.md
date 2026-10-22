# The full-SPARC check — and a correction to my own subset claim

**2026-10-21.** Written after the subset result in `THEORY.md` §4 looked too good.

## What I did

Fixed the theory's own footing (`a₀ = 1.132e-10` from P1/P3) and computed
`V(r) = √(g r)` with `g` from the law, on **all 171 SPARC galaxies with ≥5 points**,
error model `σ² = errV² + (0.05 V_obs)²`, Υ_* = 0.5 fixed (zero free parameters) and
one Υ_* per galaxy (free).

```
P1 footing 1.132e-10   canonical  Ng=171  fixed-U chi2/dof= 6.87   free-U chi2/dof= 2.42
P1 footing 1.132e-10   n=2        Ng=171  fixed-U chi2/dof= 7.06   free-U chi2/dof= 2.31
observed-vacuum 9.36e-11 canonical Ng=171 fixed-U chi2/dof= 6.63   free-U chi2/dof= 2.21
observed-vacuum 9.36e-11 n=2       Ng=171 fixed-U chi2/dof= 7.54   free-U chi2/dof= 2.28
```

## What it means, and what I got wrong

1. **My §4 headline was a favourable subset.** The five galaxies I chose (NGC 3198, NGC 2403,
   UGC 02885, NGC 7331, UGC 01281) give 1.66 with zero parameters; the full sample gives **6.87**.
   I picked well-known, well-sampled rotators, and that is a biased selection. The 1.66 is not a
   theory result and must not be quoted as one. This is exactly the defect class A31 was built to
   catch, and I caught it one step later than I should have.
2. **Zero-parameter rotation curves do not work at Υ_* = 0.5.** χ²/dof ≈ 6.9 means the theory
   with a *fixed* stellar M/L does not describe SPARC. That is not a failure of the law — it is
   the standard statement that one Υ per galaxy is required, and the theory does not predict Υ.
3. **With one Υ per galaxy the two laws are degenerate**: 2.42 (canonical) vs 2.31 (n=2), and
   the observed-vacuum footing does better than the bare one (2.21). This reproduces A7's
   independent finding (χ²/dof = 2.27, Δχ² flips sign between footings, bootstrap z = 0.75).
   **SPARC's total χ² cannot discriminate n, and it does not much care about the footing.**
4. **Neither law fits well at 2.3/dof.** With a 5 % floor the data are systematics-dominated for
   this error model, so the discriminating power lives in the *shape* — A7's per-galaxy Δχ²
   distribution and A25's RAR-knee test (Δχ²(Q−L) = +157.96 with no free parameters, ±25
   pre-registered) — not in the total χ².

## The corrected claim for the theory document

> The theory's rotation-curve prediction requires one stellar M/L per galaxy. With that one
> parameter per galaxy, the canonical law gives χ²/dof = 2.42 on 171 SPARC galaxies and the
> rival n=2 law gives 2.31 — degenerate, consistent with A7. A zero-parameter prediction at
> fixed Υ_* = 0.5 gives 6.87 and is **not** a success. Discrimination between the two laws comes
> from the transition-region shape, not from the total χ².

That is the honest number, and it is the one that goes in the paper.

## Reproduce

```bash
cd _parent && python3 theory_prediction.py     # the 5-galaxy subset, 4/4
python3 - <<'EOF'  # the full sample (see the loop in this note)
EOF
```
