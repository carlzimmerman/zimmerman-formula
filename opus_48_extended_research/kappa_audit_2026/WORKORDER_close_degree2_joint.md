# WORK ORDER — close the degree-2 joint of the κ = 1/2 derivation

Status: **OPEN.** This is the one unproven, load-bearing joint in the κ = 1/2 derivation chain
(PD01/PD05/PD08/PD10/PD22). Closing it non-circularly would upgrade κ = 1/2 from
"structurally two-valued {1/2, 1}, selected empirically" to a genuine derivation. Leaving it open
is not fatal — κ = 1/(2·cp) with cp measured to 0.33% still stands — but it is the difference
between "derived" and "measured with structure."

Audit basis (reproducible): `K_AUDIT_degree2_circularity.py`, `K_AUDIT_kappa_derivation_three_premises.py`.

## The problem, exactly

PD22 T1 proves: **P1** (symmetry) + **P2** (one-channel exactness, C(p,0)=p) + **P3** (saturation,
C(1,1)=1) + **P4** (the composition is degree ≤ 2 in each channel) ⇒ C(p,q) = p+q−pq uniquely.

P4 is essential and unproven:
- **Essential.** Without P4, P1+P2+P3 admit the whole tower
  `C_k(p,q) = p+q−pq + k·p·q·(1−p)(1−q)` for every k (symmetric, one-channel-exact, saturating;
  degree 4). The OR-composition is recovered only at k=0. So the uniqueness rests entirely on P4.
- **Not justified by G084.** G084's "2" is a spatial density-falloff exponent (ρ∝r⁻²), a different
  object from the composition polynomial's degree; and G084's γ=2 is itself conditional on
  σ²=C/2 (η=1/2). The citation is a category mismatch, not a derivation.
- **Circular otherwise.** The exact form p+q−pq is what independent-channel probabilistic OR gives,
  `1−(1−p)(1−q)` — but "independent channels combining as OR" is the OR-identification the theorem
  is supposed to derive.

## What counts as closing it

Produce a principle **X** and a proof (Lean preferred) that

    P1 ∧ P2 ∧ P3 ∧ X  ⇒  C(p,q) = p + q − p·q ,

where **X** must satisfy all three:
1. **Independently motivated** — derived from the action / the linearized two-channel field
   dynamics (div(μ ∇Φ) = 4πG ρ_b with the metric's two static potentials), or from a physical
   requirement on μ (monotonicity, convexity, positivity, no-ghost/stability, deep-MOND
   asymptotics). Not a restatement of degree-2.
2. **Not equivalent to assuming independent-channel OR** — i.e., X must not be "the channels
   combine as 1−(1−p)(1−q)" or "the channels are independent Bernoulli engagements," in any
   disguise. If X implies independence, it is circular and does not close the joint.
3. **Demonstrably excludes the tower** — under X, `C_k` must FAIL for every k≠0.

## Regression check (must pass before any closure claim)

The candidate X must make the tower fail. Concretely, a valid closure must show, for
`C_k = p+q−pq + k·p·q·(1−p)(1−q)`:

    X(C_k) holds  ⟺  k = 0.

`K_AUDIT_degree2_circularity.py` already encodes the tower and confirms P1,P2,P3 hold for all k;
extend it with `X` and show `X(C_k)` fails for all k≠0. If X cannot kill the tower, it does not
close the joint.

## Candidate routes (untested — try, report both ways)

- **Dynamics-first.** Derive the two-channel composition as a theorem of the matched
  linearized→deep-MOND field equation, not a probabilistic posit. Does the field equation force
  the response to combine bilinearly? (If Poisson-source linearity caps the response degree,
  state the exact step; naive source-linearity does NOT obviously cap the response's composition
  degree — that is the thing to prove.)
- **μ-analyticity + boundedness.** If μ(Y) is analytic and bounded with the corpus's
  normalisation μ(∞)=1 and slope = channel count, does that cap the per-channel degree at 2? Check
  whether the tower violates an asymptotic or a convexity condition the OR-form satisfies.
- **Stability / no-ghost.** Does the tower (k≠0) introduce a wrong-sign kinetic term or a
  gradient instability the OR-form avoids? If a health condition kills k≠0, that is a physical X.

## Honest fallback

If no non-circular X exists, record it: κ = 1/2's composition leg is empirically anchored
(cp = 1 to 0.33%, any deviation = a second acceleration scale excluded), and the standing stays
"κ structurally two-valued {1/2, 1}; the selection to 1/2 is empirical." That is a real result —
just not a first-principles derivation. Do not paper the gap with the G084 citation.
