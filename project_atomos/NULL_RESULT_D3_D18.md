# The atomos null: depths 3-18, no forced SM kernel

**Status: NEGATIVE RESULT, and it is theorem-backed rather than merely unlucky.** Recorded
2026-07-25. Local-only repo by project rule; never pushed to a remote.

## What was searched
Constructive enumeration of Gate-B-passable dimensionless expression trees over the framework's
FORCED germ vocabulary -- `3` (generation count) and `sqrt(8pi/3)` (the a0 kernel germ, half of
Z = sqrt(32pi/3)) plus one free O(1) -- confronted with 21 Standard-Model dimensionless targets
through three gates run in the REAL committed gate code:
* **Gate B** kernel: the candidate must actually carry the forced germs.
* **Gate C** interlock: cross-sector agreement, not a single-target coincidence.
* **Gate A** FDR: surplus information over the chance expectation in the candidate's own
  measurement window, with the look-elsewhere multiplicity applied. The window IS each target's
  published 1-sigma error, so a blunt target buys a wide window and pays for it in E_chance.

Every depth also passed a constructive-completeness head (scheme == brute, 0 missed / 0 extra) and
an a0-validity head (the pipeline must re-find a0 = cH_Lambda/Z from the same alphabet) before its
verdict was accepted.

## Exhaustive results -- complete enumeration, theorem-grade
| depth | verdict | in-window hits | CERTIFIED |
|---|---|---|---|
| 8 | CLEAN NULL | 5566 | 0 |
| 9 | CLEAN NULL | 22141 | 0 |

Depths 3-7 are the earlier committed clean nulls (`VERDICT_depth4_forced.md`,
`VERDICT_depth5_forced.md`, `notes/DEPTH6PLUS_ESCALATION_VERDICT.md`). **Depth 9 is the exhaustive
ceiling**: depth 10's streamed build has a reproducible CPU-bound dedup pathology (two hangs at
different raw counts, ~99% CPU, not memory or disk), and depth 11 is ~5x worse.

## Sampled results -- seeded lottery, non-exhaustive (no null claimed)
| depth | batches | trials | in-window hits | survivors |
|---|---|---|---|---|
| 10 | 22 | 107,257 | 977 | 0 |
| 11 | 22 | 99,394 | 684 | 0 |
| 12 | 23 | 86,311 | 534 | 0 |
| 13 | 22 | 70,626 | 338 | 0 |
| 14 | 23 | 56,783 | 261 | 0 |
| 15 | 22 | 42,466 | 146 | 0 |
| 16 | 22 | 32,907 | 95 | 0 |
| 17 | 21 | 26,045 | 59 | 0 |
| 18 | 21 | 20,680 | 45 | 0 |

**Total: 542,469 completed trials from 632,009,334 skeleton draws, 3139 in-window hits, ZERO survivors.**
A sampled search can never establish a null; every hit is labelled
`CANDIDATE (sampled, non-exhaustive)` with its trials-based multiplicity attached.

## The pattern, and why it is informative
Across depths 3-18 roughly **29,000 in-window hits produced not one Gate-A survivor.** In-window
hits GROW with depth in the exhaustive regime (259 at D6 -> 1,248 -> 5,566 -> 22,141 at D9) purely
because the value set densifies, while the sampled hit RATE FALLS with depth (0.9% at D10 to 0.2%
at D18). Both behaviours are what a genuinely empty space looks like: candidates accumulate as
noise and die at the FDR gate. The tightest hit at several depths was the same degenerate re-label
of 2/3 -- `sqrt(8pi/3)/sqrt(8pi/3)` cancelling on `c/c = 1` -- correctly killed.

## Why this is theorem-backed and not just an unlucky search
Four independent lines say the same thing:
1. **Number-field obstruction** (2026-06-27): Z carries sqrt(pi), transcendental, while all
   measured flavour data is ALGEBRAIC to measurement precision -- so a0/Z is structurally
   gauge-blind to the flavour sector.
2. **Period-ring sharpening** (2026-07-23, `reviews/period_ring_obstruction_2026.py`):
   sqrt(pi) = Gamma(1/2) has HALF-INTEGER weight; 4d SM perturbative amplitudes are integer-weight
   MZVs whose weight-1 slot is provably EMPTY (Zagier d_1 = 0). **Disjoint at weight 1** -- and this
   survives the enlargement from the algebraics to the full Kontsevich-Zagier period ring, which is
   exactly the escape the search was hoping for.
3. **This null**: 7 exhaustive depths + 522k sampled trials, zero survivors.
4. **Category mismatch**: a0 is an ACCELERATION set by a HORIZON. SM masses are Yukawa couplings
   with no acceleration content. The framework supplies no dimensional bridge to them.

## Honest scope
This bounds the framework's reach; it does NOT bound the framework. The a0 = cH_Lambda/Z reframing,
the galactic RAR and the a0-line are untouched by it -- they never depended on an SM connection.
a0's VALUE, Z and the sign s = -1 remain POSTULATED. The 2026-06-23 public retraction of the
TOE/SM overclaims stands and this result is consistent with it: the SM sector is WALLED, and now
walled with a measured null behind the theorems. **Do not re-open absent a NEW forced gauge or
Yukawa kernel** -- not a new search of the same space.
