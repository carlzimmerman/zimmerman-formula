# CFG486 FROZEN CRITERIA: CFG352's caustic edge re-scored with a FREE two-halo amplitude

(committed alone, before any script is written or run; on-disk data only; no downloads; light CPU, one thread, nice 15)

## Why
CFG352 killed the "second-caustic edge" reading of the switch (edge at 0.232 r_ta, CFG351) on KiDS lensing:
Δχ² +169.28 / +163.46 against the untruncated law. Its KiDS scorer was FP1's L355 machinery,
`kfit(..., W0, Amax = 0.0)`, so the two-halo amplitude was FIXED AT ZERO. CFG413 later showed, on CFG377's stack,
that with a FREE two-halo amplitude the penalty for small ON radii disappears. CFG413 scored a grid
x ∈ {0.23, ..., 1.0}, not CFG352's edge itself. This lane re-scores CFG352's edge model on CFG413's free-two-halo floor.

## A declared deviation from the brief (stated before running)
The brief asks for "the same stack: CFG377 primary" AND for an `Amax = 0` control that reproduces CFG352's committed χ².
These are two different stacks:
- **CFG352's scorer (stack F):** FP1/L355 machinery, Brouwer+21 Fig-3 lensing rotation curves, 4 stellar-mass bins,
  the published covariance, M_b profiled per mass bin on a grid, linear-theory two-halo template with A ∈ [0, Amax]
  per mass bin. Law χ² 162.6053 / 154.7582.
- **CFG413's floor (stack P):** CFG377's primary stack, 181,477 lenses, 15 g_bar bins, 50-patch leave-one-out
  jackknife, Hartlap; free R^-0.8 two-halo amplitude, profiled analytically, sign unconstrained.

With A = 0, stack P cannot reproduce CFG352's numbers (CFG413's own A = 0 column gives +203 / +199 at x = 0.23,
not +169 / +163). So:
- the **verdict** is scored on stack P, as the brief specifies;
- the **Amax = 0 reproduction control** is run on stack F, CFG352's own scorer;
- stack F is also re-scored with the two-halo amplitude freed. That row is reported, with the same rule stated.

## The model (identical to CFG352 except where stated)
- Law: the BARE law. CFG100 ν_mono phantom, M_d(r) = M_gal (ν_mono(y) − 1). The kernel is identical to FP1's
  `C4.nu_mono` (checked).
- Footings: a0 = 9.3603e-11 and 1.1312e-10, scored separately, never pooled. κ = ½ is FITTED. The cold mass is
  still required, and no particle species is added.
- Edge: a sharp step. The phantom mass is frozen beyond r_on = x · r_ta (CFG352's `smear_mass` sharp path is the
  same thing: M = M_law(min(r, a))).
- r_ta: on stack P, cfg100's `r_ta_law(M_gal, a0, z_lens)` per lens group (CFG413's floor). On stack F,
  CFG352's `r_bound` (Δ = DTA_025 relative to ρ_m at z_l = 0.25).

## Rows
- **x = 0.232:** CFG352's edge (CFG351 second caustic). PRIMARY.
- **x = 0.359:** first caustic. Reported.
- **x = 1.0:** the reference, "law-to-r_ta".
- **x = 0.23:** control. It must reproduce CFG413's committed row.

## Decision quantity
Δχ²_edge = χ²(x = 0.232) − χ²(x = 1.0) on stack P, free two-halo amplitude. Each fit has its own A, profiled.

**A plausibility range.** It is read from CFG413's committed `cfg413_kids_results.json` (free A over its grid
x = 0.23–1.0), per footing, as [min A / 1.5, 1.5 · max A]:
- canonical: CFG413 range 1.120–1.572, giving **[0.746, 2.358]**;
- alt: CFG413 range 0.953–1.436, giving **[0.635, 2.155]**.

## Verdict (declared now; stack P)
- **REVIVED:** Δχ²_edge ≤ 4 on BOTH footings, AND the fitted A of both the x = 0.232 fit and the x = 1.0 fit lies
  inside the range above on both footings.
- **STILL KILLED:** Δχ²_edge > 9 on EITHER footing.
- **MARGINAL:** otherwise. This includes Δχ² ≤ 4 with an A outside the range.

## Controls (can fail; a failure is kept and reported)
- **C1 (the brief's reproduction control, stack F).** With Amax = 0, the script reproduces CFG352's committed
  numbers to 0.01: the law χ² (162.6053 / 154.7582) and the Δχ² of rows 1.0, 0.359 and 0.232 against the law
  (`cfg352_caustic_edge_results.json`). In the MUTATE run it also reproduces the 0.05 row (707.77 / 703.76).
- **C2 (stack P is CFG413's floor).** Rows x = 0.23 and x = 1.0 reproduce CFG413's committed χ², free-A and
  A = 0, to 0.01.
- **C3.** The stack has 181,477 lenses and 15 bins.

## MUTATE (`CFG486_MUTATE=1`; outputs `*_MUTATE.*`)
An edge at x = 0.05 r_ta is added on stack P, with free A. It must be STILL KILLED by the rule above: Δχ² vs
x = 1.0 > 9 on at least one footing. If it is not, MUTATE is NOT DETECTED and the lane cannot discriminate.

## Reported only (no verdict weight)
- **R1. The 9 bins Brouwer+21 trust** (pair-weighted mean R ≤ 0.3/h = 0.445 Mpc): Δχ²_edge and A on the
  sub-covariance, with Hartlap for 9 bins. The rule's outcome on these bins is stated.
- **R2. Other two-halo modes on stack P:** A ≥ 0, and A = 0.
- **R3. Drop-one-bin:** the range of Δχ²_edge over the 15 drops (free A). CFG413 found x = 0.23 fragile here.
- **R4. Stack F (CFG352's own scorer)** with the two-halo amplitude freed:
  - Amax = 2, the record's bias-like ceiling (L355);
  - Amax = ∞ (A ≥ 0, free).
  Reported: Δχ²_edge (0.232 vs 1.0), Δχ² vs the untruncated law, and A per mass bin. The same rule is applied and
  stated. **If stack F with Amax = ∞ lands in a different category from stack P, the README headline says the result
  is stack-dependent.**
- **R5. r_ta definition.** CFG352's own r_ta (`r_bound`, fixed z_l = 0.25) applied on stack P for x = 0.232 and
  1.0, plus the median ratio r_bound / r_ta_law.
- **R6. Is A physically plausible?** An effective bias, b_eff = A · (stacked R^-0.8 template) / (stacked linear
  two-halo ESD), per bin. The linear two-halo ESD is FP1's (bias 1, z_l = 0.25, Planck), stacked through the same
  g_bar nodes. Any b_eff > 2 (L355's bias-like ceiling) is flagged as implausibly large. This is approximate: one
  lens redshift and linear theory.

## Standing rules
- Never "theory closed".
- Never "the data favour the framework".
- CFG352 is not edited. This lane qualifies or supersedes it in its own README.
