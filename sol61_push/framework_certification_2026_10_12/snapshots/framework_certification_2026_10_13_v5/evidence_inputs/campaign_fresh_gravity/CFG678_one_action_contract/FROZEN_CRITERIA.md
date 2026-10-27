# CFG678 — the one-action contract (frozen criteria, committed alone)

Block CFG670–679. Step 1 of the closure path in `fable_independent_2026/lean_2026/TOE_BEST_ATTEMPT_2026_10_12.lean`:
one covariant action that produces the law. This file freezes the gates that any candidate action must pass,
taken from the record's own failures. It is written before any candidate is scored against it.

## Rules
- **No new thresholds.** Each gate's PASS line is its source lane's own frozen line. A gate with no frozen line
  on record is marked DECLARED (stated, not scored).
- **An action, not a recipe.** A gate counts only if the behaviour follows from varying one action. A prescribed
  mask, a hand-placed edge or a by-hand tie scores UNTESTED, never PASS.
- **Both footings** (9.36e-11, 1.13e-10 m/s²), never pooled. A gate passes only if it passes on both.
- **Statuses:** PASS / FAIL / CONDITIONAL (passes under a stated, unproved premise) / UNTESTED (no action to
  test) / DECLARED.
- κ = ½ is fitted. The cold energy's mass is still required. No dark-matter particle may be added. Not theory closed.

## Gates

### A. Structure (the action as a field theory)
| id | gate | PASS line (source) |
|---|---|---|
| A1 | no ghost; second-order field equations | CFG329 G0 test |
| A2 | strongly hyperbolic at high frequency | CFG292: α_c > 0 and β = 0 |
| A3 | nonlinear local well-posedness | CFG294; A1–A5 proved, not assumed |
| A4 | strong-coupling scale above the energies it is used at | XC1/XC3, including XC6 part 2 |
| A5 | gravitational waves at c; no cold-energy GW messenger that is excluded | c_T² = 1/(1−β) = 1; CFG665 Lean no-go |
| A6 | black-hole exteriors match GR to observable precision | CFG318/319 |
| A7 | radiative stability | DECLARED (CFG320: depends on the unknown UV completion) |

### B. The three gaps (must come from the variation)
| id | gate | PASS line (source) |
|---|---|---|
| B1 | the bound-only switch is a varied action term, not a prescribed mask, and introduces no ghost | Gap 1 (CFG48; N14/N15) |
| B2 | the a₀–Λ tie comes from the action with no new local degree of freedom | CFG43/CFG103 Dirac count; the tie function not postulated |
| B3 | the cold energy is a well-posed sector of the action, with the lensing response it must have | CFG660–665 (ill-posed; CFG663 non-lensing response excluded; isotropic form excluded on SPARC) |

### C. Weak field and galaxies
| id | gate | PASS line (source) |
|---|---|---|
| C1 | Solar System: Cassini | G01/G02 (strict AQUAL fails 3.8–5.5×; filtered T-B survives statically) |
| C2 | SPARC RAR | CFG4_galaxy_law frozen line (rms 0.1003 / 0.0991 dex) |
| C3 | massive early types at 50–100 kpc, raw KiDS isolated lenses | CFG529 frozen census-edge line |
| C4 | cluster lensing beyond the baryons, 8–40′ | CFG680 A3 (κ < 0.0026 at 2σ) |

### D. Cosmology
| id | gate | PASS line (source) |
|---|---|---|
| D1 | zero-field nonlinear dependence | CFG358 frozen line |
| D2 | structure growth against raw KiDS / DES | CFG596 frozen line |
| D3 | a₀(z): flat, not ∝ H(z) | CFG570/571 sealed predictions (U4_27928 release 2026-11-06, GS4_24110 release 2026-11-28) |

### E. Beyond the law (required for a theory of everything, not for the law)
| id | gate | PASS line |
|---|---|---|
| E1 | κ = ½ output by the action, not fitted | DECLARED; Lean `Z_sq_not_a_count`: the factor π must come from geometry |
| E2 | a quantum completion | DECLARED |
| E3 | Standard-Model structure forced, not input | DECLARED; walled unless E1–E2 force new structure |

## Candidates to score (from committed lanes only, no new runs)
1. the ungated filtered C-H/K khronon ("chassis");
2. candidate B (the law with the bound-only switch, plus cold energy);
3. the CFG660 cold energy as a field-stress medium.

## Output
`SCORECARD.md`: one row per gate per candidate, with status and lane citation, plus the list of gates no
candidate passes. That list is the specification for the next action.

## MUTATE
Score a deliberately wrong candidate (plain GR + Λ, no MOND sector). It must FAIL C2, which shows the scorecard
can fail something.
