# T14 — the scatter face: completeness variance traces formation time

**The variance face of the settling law.** Error propagation of
f = 1 − e^{−Γt} through the exact T12 elasticity:

    σ(f)/f = ε(f)·σ(ln t_f),     ε(f) = (1−f)·[−ln(1−f)]/f

Completeness scatter is formation-time scatter, with a derived
coefficient — and a falsifiable fork.

## Results (6/6 checks PASS, rc 0; MUTATE flips C1–C5, rc 1)

| clock | f ± 1σ | σ(ln t_f) | reading |
|---|---|---|---|
| clusters (X-COP) | 0.43 ± 0.15 | **0.468** | t_c ∈ [4.2, 10.7] Gyr across the sample (around the 6.7-Gyr z₁₄ anchor) — the scatter IS the assembly clock's scatter |
| groups | 0.60 ± 0.15 | **0.409** | t_g ∈ [7.9, 18.0] Gyr |

- C1: the transport coefficient is numerically the exact ε(f) (finite
  differences, 40 points, < 1e-6).
- C4: universality — σ(ln t_c)/σ(ln t_g) = 1.144 ∈ [1.0, 1.3], propagated
  ranges [0.16, 0.78] vs [0.14, 0.68] overlap heavily: **clusters and
  groups scatter alike in formation time** — one halo clock.
- C5: **the falsifiable fork** — the law predicts absolute scatter
  GROWS with completeness: σ(f) = σ(ln t)·f·ε(f) ⇒ σ(0.60)/σ(0.43) =
  1.1462, vs 1.0 under the constant-scatter null. The two readings are
  15% apart; a sample with scatter statistics better than ~30% per bin
  separates them.
- C7: grounding fetched (2603.19521 — cluster formation z₁₄ ≈ 0.8 with
  its percentile spread; 1409.4820 — BCG late assembly) — the measured
  formation-time spread in halo-formation catalogs is consistent with
  σ(ln t) ~ 0.4–0.5 (registered; a catalog-quantitative extraction is
  the kill/reconfirm step).

## Corollary (S4, registered)

The settling is the heat equation (T10): completeness at fixed Δ carries
no environmental correlation once formation time is controlled. Testable
with X-COP stacking by large-scale environment at fixed assembly epoch.

## Corrections to the freeze (dated, on top)

- 2026-10-07: C5's original wording was a construction tautology;
  replaced by the σ(0.60)/σ(0.43) = 1.1462-vs-1.0 fork (operational).
- 2026-10-07: C6's MUTATE flip set verified with mode-independent
  predicates: linear branch fails exactly C1–C5.

## Algebra payload

The ε(f) closed form is already Lean-certified (T12,
`cert_epoch_elasticity.lean`: epoch_elasticity_closed, zero sorry,
axioms {propext, Classical.choice, Quot.sound}); the derivative
transport (d ln f/d ln t, variance propagation) rides in this lane per
house pattern.

## Bottom line

The completeness scatter is not noise about a mean relation — it is a
measurement of the formation-time scatter with a known coefficient
(0.468/0.409 for the two X-COP-era clocks), the same halo clock for
clusters and groups, and it carries a 15% fork separating the law from
the null interpretation. The variance face is live and killable.