# MUTATE — A63: does the check set bite on the *medium*?

The lane's identification is "the medium is the one-sided single-occupancy (Langmuir) gate". The
mutation must therefore change **the medium**, not the algebra of the two laws. Two modes are
implemented, both in `a63_checks.py`, both selected at the `isotherm()` switch:

| flag | identified medium | what it represents |
|---|---|---|
| *(none)* | `θ = x/(1+x)`, `A = a₀θ` | the Langmuir lattice (the lane's claim) |
| `--mutate` | `A = a₀ tanh(g/a₀)` | the centrosymmetric saturating dielectric (candidate (a)) |
| `--mutate-n2` | `4x(1−θ) = θ(2−θ)`, `A = (a₀/2)θ` | the self-depleting n=2 element |

Baseline: `A63 COMPLETE: 31/31 checks PASS.`, exit 0 (`a63.out`).

## Mode 1 — `--mutate` (tanh dielectric): 24/31, exit 1

```
K18 FAIL  0.15196818077536986   1e-06
K19 FAIL  0.5493061443340548    1e-10
K20 FAIL  0.07755886258626891   1e-12
K23 FAIL  inf                   1e-12
K27 FAIL  0.8364200567129756    1e-08
K28 FAIL  0.7615941559557649    1e-12
K31 FAIL  12.959809080009897    1e-04
```

Read the values, not just the failures:

- **K28** — `θ(a₀) = 0.7616` instead of `1/2`. The tanh saturated dielectric is **not half occupied
  at `g = a₀`**: its half-occupancy drive is `atanh(1/2) = 0.5493 a₀`. This is the single cleanest
  statement of what the mutation does: it moves the affinity away from `a₀`.
- **K19** — the skew's zero moves to `g = 0.5493 a₀` instead of `1.000 a₀`.
- **K18** — the skew at `g = a₀/2` becomes `+0.152` instead of `+0.7071`: same sign, wrong size,
  because `θ(1/2)` is wrong by 39 %.
- **K23** — `R = c₃c₁/c₂² = ∞`: `c₂ = 0` for any odd isotherm, so the ratio diverges. The
  fingerprint is well defined only for a rectifying medium.
- **K27** — the medium reproduces neither the law (relative deviation `1.0`) nor `K W′(u) = g`
  (`0.84`). This is the check the whole lane rests on.

**Why 24 survive, and why that is correct.** K1–K17, K21, K22, K24–K26, K29, K30
are statements about *the two laws and the candidate class*, not about which medium is installed:
identities (K1), the integral of the Langmuir isotherm (K2–K4), the two potentials' series (K5),
the tanh/Langevin coefficients and the biased-tanh family (K6, K7, K9), the admissibility theorem
(K8), Born–Infeld (K10, K11), mass action (K12, K13), the capacity bookkeeping
(K14), the multi-occupancy and Fermi exclusions (K15, K16), the analytic structure (K17), the
rotation-curve and wide-binary numbers (K21, K22), homogeneity (K24), the capacities (K25), the
adsorption exponent (K26), n=2's violation of `C = −c₂a₀` (K29) and the sample sizes (K30). A
mutation must not break those; if it did, the checks would be measuring the switch rather than the
physics.

## Mode 2 — `--mutate-n2`: 23/31, exit 1

```
K11 FAIL  0.9999995000003749   1e-05
K18 FAIL -0.34831069974900664  1e-06
K19 FAIL  0.375                1e-10
K20 FAIL  0.07755886258626891  1e-12
K23 FAIL  0.0                  1e-12
K27 FAIL  9999998.999999998    1e-08
K28 FAIL  0.7639320225002103   1e-12
K31 FAIL  1.8739948907337003   1e-04
```

This is the strong mutation, and the numbers are the point: with the n=2 element installed, the
checks return **exactly the n=2 predictions derived in the report** —

- **K18** returns `−0.34831`, which is the `−0.348327` that K18's own note says n=2 should give;
- **K19** returns `0.375 = 3/8`, exactly the n=2 flip location;
- **K23** returns `0` — the n=2 third-order fingerprint;
- **K28** returns `θ(a₀) = 0.7639 = 3 − √5`, the n=2 occupancy at `g = a₀` from
  `4(1−θ) = θ(2−θ)` — its capacity is half, so `θ = 2A/a₀` is already `0.764` at `g = a₀`;
- **K11** fails because the mutated theory saturates at `a₀/2`, so "the theory caps `A` at `a₀`" is
  no longer true. K11 is a statement about the *capacity*, so the n=2 mutation is entitled to break
  it — and it is the one check that distinguishes the two mutations.

So the two mutations are not equivalent: the tanh mutation moves the medium *off* the admissible
class (wrong `c₂`), while the n=2 mutation keeps `c₂` and halves the capacity. The check set
separates them by exactly one check (K11), which is the capacity statement, and by nothing else —
which is the correct discrimination, because `c₂` is shared and the capacity is not.

## What would *not* be a legitimate mutation

- Changing `a₀` (a footing change, not a medium change): it rescales every number but leaves every
  pass/fail pattern unchanged, since all the shape statements are in units of `a₀`. That is the
  sense in which the discriminator is normalisation-free, and it is worth stating that no check can
  see a footing change — by design.
- Changing the *noise model* (e.g. Poisson instead of binomial occupancy): that is a different
  claim, not a mutation of this one; K18 would then be testing the wrong formula.
- Truncating the series (using `A = g − g²/a₀ + g³/a₀²` instead of the closed form): K27's grid
  extends to `g/a₀ = 10³`, where the truncated series diverges, so the failure would be a numerical
  artefact, not a medium change.
