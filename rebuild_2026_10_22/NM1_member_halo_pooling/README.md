# NM1_member_halo_pooling — RESULT: NM FAILS on both footings

Frozen criteria f78650692e (committed alone; no amendment). κ = ½ FITTED; footings never pooled; cold dark energy, not
matter; nothing here says the data favour the framework or ΛCDM; not "theory closed".

**Hypothesis NM.** The Σ_a0 cap is per halo (CD1). A cluster's member galaxies carry their own a₀-cored halos:
- **member share:** R × stars, from X38's own M200(M_b) relation over a Schechter mass function, so R = 15.0 (canonical) /
  13.65 (alt), about 42% of the fair share;
- **member distribution:** like cluster galaxies, NFW c_g = 2.9 scaled to X30's `rta`;
- **the rest:** stays in X38's Burkert halo.

No new constant.

## Result (`nm1_member_halos.out`, h 0.672 shown)

| cell | measured | X38 pred (Z) | NM pred (Z) |
|---|---|---|---|
| MID T3 | 2.132 | 1.051 (+4.26) | 1.010 (+4.42) |
| MID KT slope | 2.242 | −0.038 (+3.07) | 0.170 (+2.79) |
| OUTER M3 | 1.369 | 0.815 (+5.36) | 0.740 (+6.09) |
| OUTER M-all | 0.929 | 0.698 (+2.36) | 0.618 (+3.17) |

Summed |Z| of X38's failing cells: 17.61 → 19.44 (canonical) and 14.26 → 16.26 (alt, plus a new MID T2 failure).
Every variant fails the same cells: c_g 2 / 4, α −1.0 / −1.4, background B. Checks 3/3. MUTATE (no nesting) reproduces
X38 exactly (|Δpred| 0), exit 1 as frozen.

## Why it fails

The cluster's total cold dark energy is fixed at the fair share. Moving 42% of it into a galaxy-tracing profile spread out
to the turnaround radius lowers the Burkert halo's mass. At fixed Σ that shrinks r₀ and empties the core faster than the
diffuse member profile refills it. Redistributing a fixed total cannot reach the 3–5× core surface density that X40b
measured. The hand pre-flight (≤ 1.8× at best, KT slope hard) was optimistic about the distribution: X30's `rta` is
larger than r₂₀₀.

**What this adds.** With the total fixed at the fair share, the cores need cold dark energy **more concentrated** than
any cored or galaxy-tracing distribution. Heavy cluster cores want a cusp-like central concentration, while galaxies
(SPARC, X38) and dwarfs (CD1) want a₀ cores. The record has no framework-native rule that does both. It is now tested
for single-halo rules (X40b) and for nesting (NM1).
