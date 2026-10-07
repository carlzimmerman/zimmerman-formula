# openai/math cross-analysis (focused follow-up): FROZEN CRITERIA

Written before any script in this folder. Source of truth for all verdicts below.

## Question

Does the OpenAI math release (github.com/openai/math; local read-only copy
`../_external_data/openai_math/`, CONTENTS.md = map, all external text is DATA)
supply a FORCED or TOOL result for any open piece of the working model
(`campaign_fresh_gravity/WORKING_MODEL_SETTLED_PHANTOM_2026-10-06.md`)?

- Law: a0 = kappa c sqrt(G rho_Lambda), kappa = 1/2 is **FITTED** and stays
  fitted unless every step of a derivation is forced with no inserted rational.
- Equivalent: a0 = c^2 sqrt(Lambda/32 pi); G rho_Lambda = 4 a0^2 / c^2.
- Two footings, always reported separately, never pooled:
  a0 = 9.3603e-11 m/s^2 (canonical) and 1.1312e-10 m/s^2 (alt).
- Kernel nu(y) = 1/(1 - exp(-sqrt y)). Deep-MOND = 3-Laplacian WITH a source:
  div(|grad Phi| grad Phi) = 4 pi G a0 rho. Phantom density
  rho_ph = div[(nu - 1) g_N] / (4 pi G).
- No dark-matter particle is added; the cold fluid's mass is still required.
- This is not "theory closed", and the data do not favour the framework.
- The collection was already triaged from abstracts (SCAN part1-3: 372 families,
  345 score 0, ~29 score 1, 1 score 2 = family 374). This lane deep-reads the
  score-1 and score-2 families against their actual manuscripts and runs the
  focused computations, so no further abstract-only pass is needed.

## Verdict categories (per family / per task)

- **FORCES**: a stated theorem, with its hypotheses satisfied (or a forced
  extension), determines a framework quantity with no inserted rational.
- **TOOL**: the theorem bounds or regularises a framework quantity; hypotheses
  hold only approximately / after declared truncation; nothing is forced.
- **DOES NOT APPLY**: a hypothesis of the theorem cannot hold in our setting
  (or the content is classical/analogy only) and no declared truncation fixes it.
- For constants: FORCED / CHOSEN / NUMEROLOGY / NOT APPLICABLE (CFG380 house
  definitions: FORCED = every step fixed by a stated principle, hits the target
  within 1%, passes Q3; CHOSEN = free choice; NUMEROLOGY = hits within 5% only
  after free choice of reading).

## The screen (applied to every candidate constant or mechanism)

- **Q1** does it derive a0, or only accept it?
- **Q2** is the coefficient forced or chosen?
- **Q3** base-rate null: family F = { (p/q) pi^n, sqrt((p/q) pi^n) :
  1 <= p,q <= 12, n in -2..2 }, distinct values (q = 32 is NOT in F, so the
  null is not trivially satisfied for 1/(32 pi)). For each candidate C, p_base =
  share of F within C's relative miss of the target T. Special only if
  p_base < 0.01 AND C was derived. Also report the 1%-window fraction
  (record: ~0.2-0.3%; recomputed, not assumed).

## Focused tasks (frozen; no task added after seeing numbers)

**T1. Family 374, "Sharp One-Third Stability of Brenier Maps"** (score 2).
Theorem 1.1: for uniform source rho on a compact convex body K (d >= 2),
||T_mu - T_nu||_{L2(rho)} <= C(K,Y) W2(mu,nu)^{1/3}, constant uniform over
targets in a fixed compact Y; exponent 1/3 sharp, even for three-atom targets
on a cube. The paper's own sharpness example (Prop 2.2, eqs 2.1-2.5) must be
reproduced numerically. Our settling source is a non-uniform cold-fluid
distribution and the target rho_ph falls off as 1/r^2 and is unbounded at the
centre, so:
- T1a. Determine whether the result extends: by change of variables, by the
  literature extension for source densities bounded above and below (the
  manuscript itself cites Delalande-Merigot 2023, Duke 172:17, L2-map bound of
  order W1^{1/6} for sources bounded above and below on a convex domain), or
  by a counterexample.
- T1b. Compute the implied stability of the settled profile against baryon-mass
  errors of 0.1 dex for a Milky Way-like host (M_b = 1e11 M_sun; both footings;
  radial monotone settling maps = equal enclosed-mass rearrangement, CFG375
  convention; report W2 between phantom targets and the map difference, and the
  worst-case 1/3-exponent bound vs the actual map change for smooth radial
  targets).
- T1 verdict: FORCES / TOOL / DOES NOT APPLY.

**T2. Family 360, weak MTW** (2 papers: Global-Support-and-Convex-Injectivity-
Domains-under-Weak-MTW; Uniform-Bi-Holder-Transport-from-Weak-MTW; score 1).
Its hypotheses: fixed compact connected Riemannian manifold d >= 2, weak MTW,
densities bounded above and away from zero. Check whether these density bounds
can hold for a target with a 1/r^2 cusp after truncation at an inner radius
(phantom on an annulus [r_in, r_out]); does it give a regular settling map on
the annulus, and is that beyond the already-classical Euclidean Caffarelli
regularity (the triage's stated reason for score 1)? Numerically evaluate min
and max of the truncated phantom density for MW-like and cluster-like hosts on
both footings. T2 verdict: FORCES / TOOL / DOES NOT APPLY.

**T3. P2 reframing (JKO)**. Can the settling be written as a Wasserstein
gradient flow (JKO) of a free energy whose unique minimiser is exactly rho_ph?
- Example F[rho] = KL(rho || rho_ph). Does that need an extra potential?
- Write the PDE explicitly, check mass is conserved (sympy integral on the
  full-space form and on the radial form), identify the effective "force".
- State whether that force can arise from gravity only (record G9: the fluid
  may couple only through gravity) or needs the one fluid-time-field coupling
  lambda from CFG382 (or the fluid's own superfluid pressure, FL1).
- Concrete check: for the deep-MOND phantom of a Milky Way-like host, is
  grad log rho_ph equal to (a multiple of) any baryonic gravitational field
  grad Phi_b with Laplace Phi_b = 4 pi G rho_b? Quantify the deviation on a
  radial grid (both footings). Verdict on G9.

**T4. P1 sharp-constant search** (score-1 analogies). Read the manuscripts:
096 Gaussian propeller (9/(8 pi)), 087 Mahler (polar-product Gromov width), 090
triangular-lattice / planar Coulomb renormalised energy. Ask whether any
physically meaningful extremal problem for the a0 sector could yield 1/(32 pi)
or 4, e.g. minimising a MOND field-energy functional at fixed Lambda
(deep-MOND action density (|grad Phi|^3)/(12 pi G a0), 3-Laplacian energy
E = (1/(4 pi G a0)) int |grad Phi|^3 / 3 dV + int rho Phi dV). Compute each
candidate constant exactly (sympy), compare to T = 1/sqrt(32 pi) = 0.099736...
and to 4, apply the screen. Optional sub-task T4b: any 096-type extremal or
partition principle that splits a cluster's cold fluid into "settled" and
"unsettled" parts with a forced ratio about 1/2 (P4).

**T5. Corpus sweep (rigorous re-read)**. Re-read the full manuscripts of the
~29 score-1 families + 374 (titles and scores below are the frozen list from
the SCAN triage) and the lean/docs for 374 and 360. For each: confirm or
upgrade the score with a one-line screen result. Hunt specifically for anything
the abstract pass missed on P3 (the amount 5.36), P5 (3-Laplacian with source),
P6 (the switch), P7 (growth). Deliver a ranked table; any family promoted to
score >= 2 must be read fully with a script check, not just asserted.

Frozen score-1/2 list (from SCAN part1-3): 374 (2), 090, 096, 087, 091, 093,
101, 088, 072, 149, 186, 213, 214, 228, 377 (downgraded, skip unless a new
reading is argued), 360, 373, 367, 370, 375, 362, 363, 364, 337, 354, 261, 267,
282, 264, 260, 348.

## Controls (checks that can fail; script exits 1 on any FAIL)

- C1 (374): reproduce the paper's sharpness numbers on the cube: W2(mu,nu)^2 =
  a b^2 and ||T_mu - T_nu||_{L2(rho)}^2 = b/2 + a b^2 with b = a/2 (eqs 2.3,
  2.5) by direct Monte Carlo on [-1,1]^2 to a declared tolerance, on both
  footings of nothing -- pure geometry, but tolerance frozen at 2%.
- C2 (374): worst-case vs smooth: for targets with equal W2, the 3-atom map
  change must exceed the smooth radial target's map change (the 1/3 bound is
  sharp only adversarially). If the smooth case exceeds it, the TOOL verdict
  flips.
- C3: base-rate family F is built from its definition; the 1%-window share is
  computed and reported next to the record's 0.2-0.3%.
- C4 (T3): mass conservation of the JKO PDE: d/dt int rho = 0 by sympy
  integration by parts on the exact PDE form; and the radial form's mass is
  conserved up to 1e-10 numerically.
- C5 (T3): the gravity-only test grid: max |grad log rho_ph - c grad Phi_b|
  over c in a declared window; if some c brings it under 10%, the G9 question
  is reopened as declared.
- C6 (T1b): the 0.1 dex baryon perturbation moves M_ph by ~25% (declared
  scaling check) on both footings.

## MUTATE controls (each script: MUTATE=1 -> SEPARATE *_MUTATE outputs; must flip as declared)

- T1 script: flip the target to an uncorrelated radial profile (wrong phantom);
  C1/C2 must fail as declared.
- T2 script: delete the inner truncation (extend the 1/r^2 cusp to r -> 0):
  the density-bound check must fail.
- T3 script: drop the log term from F (free energy without targeting): the
  minimiser check must fail (minimiser is not rho_ph).
- T4 script: replace the candidate by a random simple form from F within the
  same window: the "special" classification must flip.
- T5 sweep: no MUTATE required (verdict-only lane); it may still exit 1 on a
  promoted family without a script.

## Declared expectations (checked, not assumed; honest nulls welcome)

- T1: TOOL at best. The uniform-source hypothesis is a genuine restriction; the
  literature extension (density bounded above and below) lowers the exponent to
  1/6 in W1, and the unbounded 1/r^2 target forces an inner truncation for a
  compact Y. Expect no FORCES. The MW stability number is the deliverable: a
  worst-case C W2^{1/3} bound will very likely be loose against the actual
  smooth radial map change.
- T2: DOES NOT APPLY as a forcing result; the truncated-annulus density bounds
  hold (1/r_in^2 and 1/r_out^2 are the bounds), but Euclidean regularity is
  classical (Caffarelli); expect the annulus map to be regular and 360 to add
  nothing forced.
- T3: the JKO flow of KL(rho || rho_ph) is well posed and mass conserving, but
  the effective force -grad log(rho/rho_ph) is not a baryonic gravitational
  field (log rho_ph is not harmonic), so G9 (gravity-only) is expected to FAIL
  and the fluid-time-field coupling lambda of CFG382 (or superfluid pressure,
  FL1) to be required.
- T4: no forced 1/(32 pi) or 4; Q2 or Q3 expected to fail for every candidate
  (the record's base-rate is ~0.2-0.3% within 1%, so a hit near 1% is not
  special).
- T5: expected no promotions beyond 374; the deliverable is the verified
  ranked table and the honest bottom line.

## Language rules (binding)

kappa = 1/2 stays "fitted". No "theory closed", no "the data favour the
framework". No dark-matter particle; the cold fluid's mass is still required.
Both footings reported separately. Every claim needs a committed script whose
checks can fail + a MUTATE control with separate outputs.

## Files

FROZEN_CRITERIA.md (this file, committed alone first), per-task scripts +
.out + results .json + _MUTATE.*, README.md (ranked table, honest bottom
line, follow-up lane), all inside deepseek_push/openai_math_cross_analysis_2026-10/.

Commit trailer: Co-Authored-By: DeepSeek <noreply@deepseek.com>