# The a₀/Z coefficient-footing audit — H₀ vs H_Λ conflation, full fix-list (2026-06-13)

*A 61-agent exhaustive audit of the a₀/Z corpus (every file stating an a₀/cH coefficient or comparing 1/Z to
Milgrom/Verlinde), graded against the ground-truth rubric in [`THE_A0_COEFFICIENT_CONVENTION.md`](THE_A0_COEFFICIENT_CONVENTION.md).
Both-ways: this is a QUOTING/COMPARING bug, not a physics error — the canonical formula a₀=c²√(Λ/32π)=9.36e-11
is footing-independent and correct.*

## Tally (59 files audited)

| verdict | count |
|---|---|
| **CLEAN** | 20 |
| **CONFLATES** | 32 |
| **AMBIGUOUS** | 4 |
| NO-COEFFICIENT-CLAIM | 3 |

**The headline Zenodo artifact is CLEAN** — `ZIMMERMAN_THEORY_OF_GRAVITY.md/.tex` and `zimmerman_toe_map_2026.tex`
already carry the exact "Footing matters" fix (md L48; tex L305–310: "evaluating on ρ_total/cH₀ gives 1.13e-10
… the law's footing is ρ_DE/cH_Λ"). **These are the templates.** The conflation is concentrated in the
secondary v12 papers and the `reviews/*.py` scripts.

## The single root error

Writing **1/Z = 0.173 against cH₀** instead of **cH_Λ**. This does two things at once:
- **inflates** the canonical value: cH₀/Z = 1.13e-10 (the ρ_total/H₀ reading), +20% above the canonical
  9.36e-11 = cH_Λ/Z = c·√(Ω_Λ)·H₀/Z. Several scripts hide this by **tuning H₀ up to 71.5** so cH₀/Z "reaches"
  1.2e-10 — the most self-deceptive form (it silently absorbs the missing √Ω_Λ = 0.83).
- **falsifies the Milgrom/Verlinde "bracket":** Milgrom (0.159) and Verlinde (0.167) reference cH₀, so the apt
  comparison is the framework's **vs-cH₀ value 0.143** — which is the **LOW OUTLIER below both**, not bracketed
  between them. (Honest upside: the outlier position is *more* distinctive and falsifiable than "bracketed.")

## MANDATORY before any citation — the 4 PUBLISHED-PAPER-CRITICAL files

| file | type | the problem |
|---|---|---|
| `papers/v12_TOE_DONE_RIGHT.md` | C1 (L24,34,65,109) + C2 (L85-86) | **visible 20% internal contradiction:** master a₀(z)=cH(z)/Z with E(0)=1 forces a₀(0)=cH₀/Z=1.13e-10, contradicting L52's own "9.39e-11 verified exactly." A referee opens this first. |
| `papers/v12_RADION_MOND_BRIDGE.md` | C1 (L56-62, esp 61) + C2 (L123-124) | L61 writes a₀=cH₀/Z=1.20e-10 (ρ_total/H₀, +20%); L123-124 compare 1/Z=0.173 to Milgrom/Verlinde same-footing. |
| `papers/Paper1_AeST_evolving_a0_realization.md` | C1 (L17,55,123,145,231) | a₀=cH(z)/Z with θ=3H, E(0)=1 → 1/Z against cH₀ → 1.13e-10 silently canonical. |
| `papers/v12_SCALING_MOND_ACTION.md` | AMBIGUOUS / latent C3 | a₀/cH=1/Z with cH the instantaneous total-density rate; never asserts a canonical number — latent, add one clarifying clause. |

*(These are secondary/older paper drafts, NOT the main published whitepaper, which is clean.)*

## SWEEP — the H₀-tuning "rescue" scripts (fix so you don't fool yourself)

These set H₀=71.5–73 so cH₀/Z lands on ~1.2e-10 without ever naming the missing √Ω_Λ:
`reviews/a0_cH0_Z_check.py` ✓fixed, `reviews/horizon_a0_derivation.py`, `reviews/emergent_a0_apparent_horizon.py`,
`reviews/radion_mond_bridge.py`, `reviews/factor_of_two_horizon.py`, `reviews/scaling_mond_action.py`,
`reviews/a0_construction_connection.py`, `reviews/a0_evolution_consequences.py`, `reviews/geometric_origin_of_a0.py`,
`reviews/predicted_a0_rar_consistency.py`, `reviews/sparc_rar_honest.py`, `reviews/data_consistency_ledger.py`,
`reviews/aest_radial_aether_eom.py`.

## SWEEP — the Milgrom/Verlinde "bracket" sites (C2)

`reviews/Z_is_one_pure_number.py` ✓fixed, `reviews/desitter_entropy_coefficient.py`,
`reviews/freefall_clock_derivations_rigorous.py`, `reviews/parameter_space_map.py`, `reviews/the_one_quarter_target.py`,
and core docs `EQUATIONS.md`, `FRAMEWORK.md`, `NOVELTY.md`, `WEB_SYNTHESIS.md`, `ROADMAP.md`, `TOE_REVIEW.md`,
`COMPLETE_ASSESSMENT.md`, `BRIDGE_TO_UNIFICATION.md`, `FIRST_PRINCIPLES_FOUNDATION_2026-06-06.md`,
`COEFFICIENT_DEFINITIVE_VERDICT.md` (ambiguous), `FOUNDATIONS.md` (ambiguous), `ZENODO_PUBLICATION_MAP.md`.

All flagged files in this list carry a correction banner pointing here + to `THE_A0_COEFFICIENT_CONVENTION.md`.

## The both-ways net (do NOT overstate)

1. **It is a quoting bug, not a physics bug.** The canonical a₀=c²√(Λ/32π)=9.36e-11 is footing-independent and
   correct; only how the coefficient is *quoted and compared* is wrong in the flagged files.
2. **The corrected story is CLEANER, not weaker.** A value that sits *apart* from Milgrom/Verlinde (0.143 vs
   0.159/0.167) is a sharper, more falsifiable claim than one "bracketed" between them.
3. **Empirical standing is unchanged.** Per the standing SPARC rule, the data cannot select among
   0.143/0.159/0.167 at ~20% systematics anyway. This fix is about internal self-consistency and being
   referee-proof, not about the physics.

*Quarantine held: Z stated as the framework's coefficient, never asserted as derived. The clean flagship proves
the right footing is already known — this is a propagate-the-fix job, not a rethink.*
