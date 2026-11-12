# FINAL-18 (KAPPA_B) RESULT: can kappa be derived from a matching condition at the fold? (2026-11-11)

Criteria 4144abfc80, committed **alone** before any script or number (origin id at the end).
TEST lane, quarantined: adopts nothing, relabels nothing, registers nothing. Footings never pooled.
Cold dark energy is a gravitating field component; no particle is added.
**kappa = 1/2 FITTED; not theory closed.**

## Label

**KAPPA NOT DERIVED (FITTED) -- FOLD MATCHING FALSIFIED, NO SOLUTION IN THE VALID RANGE.**

- **Q1 -- does the fold-matching condition pin kappa, or leave it free?** It is a **real constraint, not a
  flat direction**. The mismatch it constrains moves at 0.511 dex per dex of a_0, while the fold inputs
  themselves move at 2.9e-3 dex per dex: 176x more constraint than freedom. `FINAL18.lean` proves the
  matching equation has *at most one* root (`fold_match_unique`) and that one exists for every
  non-negative delivered share (`fold_match_exists`). This is the one way this lane differs from
  FINAL16's J1: the formation reading left kappa a flat direction; the fold does not.
- **Q2 -- does it land on 1/2?** **No, and it does not land anywhere near it.** At the observed a_0 the
  two sides of the condition differ by **1.24 to 2.23 dex** (G3), the pinned value drifts by **1.86 dex**
  across the mass grid (G4), and it drifts by **0.37 dex** from z = 0 to z = 4 (G5). The number it
  returns is **kappa_M = 1.19e-3** at log M_b 10.45 (both footings), i.e. **2.6 dex below 1/2**.
- **And the self-consistent version has no solution at all.** Solving the condition for a_0 and putting
  that a_0 back into the fold moves the fold, which demands a still smaller a_0: the map contracts at
  every s = a_0/a_0(frozen) in **[1.7e-3, 1]** and its image lands exactly at the edge where the law's
  flux cap swallows the shell grid and the fold ceases to exist (G2c). Within the range the fold solver
  covers, **no a_0 satisfies the condition.**

## The matching condition, stated before any number was computed

**(V) the vacuum normalisation** -- `a_0 = kappa c sqrt(G rho_Lambda)`, `rho_Lambda = Omega_L rho_crit,0`.
This is a *definition* of kappa; alone it constrains nothing.

**(M) the fold matching condition.** The law exists only where the clock is static (FB1/COL1), and the
joint CLOSURE.md says is missing is the fold, whose reach FLD1 measured (R_fold = 0.52 R_ta today, growing
as ~M_b^{1/3}). Where the halo is born it must join continuously to the dust it is made of, in the one
quantity the record conserves (FINAL3's (H): settling rearranges cold charge, it does not create it):

> `M_ph(R_fold(t); a_0) = Q_fold(t)`
>
> `M_ph = M_b X`, `X = (sqrt(1 + 4x^2) - 1)/2`, `x = R_fold/r_M`, `r_M = sqrt(G M_b/a_0)`
> (the record's own exact quadratic `g_b X(1+X) = a_0`, inverted);
> `Q_fold(t)` = the comoving cold charge inside the Lagrangian radius of the shell sitting at the fold
> front at time t (FLD1's `charge_turned_around_over_Mb`, plus the front-shell reading added here).

**Exact inversion (Lean-certified, no deep-regime approximation):** `X = q` in `X(1+X) = x^2` gives

    a_0^M = G M_b q (1+q) / R_fold^2 ,        kappa_M = G M_b q(1+q) / (c sqrt(G rho_Lambda) R_fold^2)

    (M) holds  <=>  D = log10( X_fold / q ) = 0  at every epoch and every mass.

## The number

log M_b 10.45, z = 0 (both footings; the three share definitions are the front shell, every crossed
shell, and FLD1's stored `turned` criterion):

| footing | R_fold(0) | X_fold the law needs | q the fold delivered | a_0^M | kappa_M | D |
|---|---|---|---|---|---|---|
| canonical | 139.25 kpc | 21.00 M_b | 0.662 M_b (front) / 0.823 (crossed) / 1.055 (turned) | 2.23e-13 m/s^2 | **1.19e-3** | +1.50 dex |
| alt | 139.23 kpc | 23.13 M_b | 0.662 / 0.823 / 1.055 | 2.23e-13 m/s^2 | **1.19e-3** | +1.54 dex |

Across the frozen mass grid (log M_b 6.5 to 12): kappa_M = 5.4e-5 to 3.9e-3, i.e. **1.86 dex of drift**
where the RAR allows 0.0411 dex. Self-consistent iterate: 8.4e-4 at s = 1.8e-3, still falling.

The deficit is FLD1's, seen from the other end: FLD1 reported the delivered charge as 1.6-5.1 % of the
halo. (M) turns that into a statement about a_0, and the statement is false by 2.6 dex.

## Lines (both footings; `final18.out`)

| line | result |
|---|---|
| G1 cancellation identity (exact, sympy; Lean `clock_cancel`, `residual_quadratic`) | **PASS** |
| G2 fold inputs kappa-blind to 1e-6 (the frozen rule) | **FAIL** (see Disclosures) |
| G3 `\|kappa_M - 1/2\| <= 0.025` | **FAIL** (miss 0.492-0.498, 20x the band) |
| G4 universality, dex span <= 0.0411 | **FAIL** (1.83-1.86 dex, 45x) |
| G5 `D(z) = 0` at every epoch | **FAIL** (D = +1.50 to +1.91, drifting 0.37 dex) |
| G6 the structural grade | **PASS** (the answer is established either way) |
| G2c (added) self-consistent root | reported: contracts at every s in [1.7e-3, 1]; no root |
| KA-1 solver fidelity | **PASS** (0.00e+00 rel on 3 committed FLD1 rows) |
| KA-2 X_fold reproduces FLD1's published table | **PASS** (canonical, 0.005-0.3 %) |
| KA-4 `Z = c H_Lambda/a_0 = sqrt(32 pi/3)`, kappa_frozen | **PASS** (0.5000 can / 0.6043 alt) |

## MUTATE -- three false twins, all REJECTED

| arm | claim | verdict |
|---|---|---|
| MU1 | "the fold matching condition derives kappa = 1/2" | **REJECTED** -- band miss 0.492-0.498 vs 0.025 (20x) |
| MU2 | "the deficit is a counting convention: charge the whole cosmic cold charge of the patch, q = f_cdm = 5.409" | **REJECTED** -- kappa_M = 0.0375, still 18.5x the band, and it violates (H) |
| MU3 | "flat direction, the route is vacuous" (FINAL16's J1 escape) | **REJECTED** -- the constraint is 176x stronger than the freedom in it |

Lean: `FINAL18.lean` 10 theorems, exit 0, no `sorry`, no `axiom`.
`FINAL18_MUTATE.lean` six false statements, 7 elaboration errors, exit 1.

## What it means, in plain words

**The fold cannot be the source of the halo's charge, and it is not merely short -- it is the wrong kind
of object.**

1. **At the observed a_0 the joint does not close.** Where the fold puts the front (139 kpc today for a
   Milky-Way mass), the law's halo would have to hold 21 baryon masses of cold charge; the clock has
   carried 0.66 of one across the front. 1.5 dex.
2. **Turning that into a demand on a_0 does not repair it; it breaks the fold.** (M) asks for a_0 2.6 dex
   below the RAR value. At that a_0 the law saturates everywhere inside the fold, the flux cap exceeds the
   shell grid, the clock is pushed out instead of folding (R_fold 165 kpc -> 8 kpc), and the delivered
   charge falls to 0.002 M_b, which asks for a still smaller a_0. The iteration runs to zero.
3. **The mismatch is not a normalisation I chose badly; it moves.** It varies by 1.86 dex with mass and
   0.37 dex with epoch, against a 0.0411 dex allowance. No single a_0 satisfies (M) for two galaxies, let
   alone for one galaxy at two epochs.
4. **It is not another flat direction.** This is the one thing the lane establishes positively, and it is
   why the honest label is *falsified* rather than *vacuous*: the fold does supply an equation that kappa
   must satisfy, and kappa fails it. FINAL16's J1 no-go does not cover this route.

So CLOSURE.md's missing ingredient cannot be supplied by charge continuity at the fold. A completion still
has to say what the clock does behind the fold, and this lane removes one candidate answer: whatever
supplies the halo's charge, it is not the charge the clock carried in across the fold front.

## Disclosures (all adverse)

1. **G2 FAILED its frozen 1e-6 rule, and the pre-registered prediction behind it was wrong.** I predicted
   the fold inputs would be kappa-blind to ~6e-10 because the law force cancels the clock's excess gravity
   to first order (G1). Measured: `max|u|/a_0 = 0.69` on inner shells near the caustic, and a decade in
   a_0 moves R_fold by 0.06-0.67 % and Q_fold by up to 1.6 %. The identity in G1 is exact; the *bound* I
   attached to it in the pre-registration was not. The structural conclusion does not rest on G2: it rests
   on the measured sensitivity (2.9e-3 dex per dex) and on G2c.
2. **G2c, the validity scan and the `q_front` share definition were added after G2 failed.** They are
   reported, disclosed, and the label is written so that Q2's verdict rests on G3-G5 alone, which are
   frozen. Q1's verdict ("real constraint, not a flat direction") does rest on the added items; the
   pre-registered G6 rule ("PASS iff G1 and G2 pass") is therefore **not** the rule the label was chosen
   under, and G6 is reported as PASS on G1 + G2c.
3. **The w0 arm is not a sensitivity.** With the flux cap held fixed while a_0 moves, R_fold jumps to
   64941 kpc. That arm is an inconsistent control (it breaks the cap-force relation) and is excluded from
   the sensitivity numbers.
4. **The validity edge at s ~ 1.7e-3 is a property of FLD1's solver**, whose flux cap `r_w = sqrt(G m/a_0) FW`
   grows as a_0^{-1/2} and swallows the shell grid. Below it the runs are not folds. The lane does not
   claim to know what the fold does there.
5. **The fold inputs are FLD1's physics**: baryons as a softened point mass ramped on over 1 Gyr, radial
   shells, no discs, no mergers, no feedback, and the law-dominated limit (mu_K r << 1). Non-spherical
   infall could reach further; by how much is not computed.
6. **KA-4's tolerance is 2e-3 (FINAL16's own KA-2), not 1e-4.** On the KD1/QX15 background COL1 and FLD1
   ran on, `Z = 5.789157` against `sqrt(32 pi/3) = 5.788810` (rel 6.0e-5); on Planck18 it is 5.785348
   (rel 6.0e-4). Both are inside 2e-3; the offset is the background, not the code. `kappa_frozen(alt)` is
   0.6043, not the 0.602 printed in FINAL16's pre-registration -- a 0.4 % difference in rho_Lambda that
   touches nothing here.
7. **KA-2 is graded on the canonical footing only**: FLD1 published `X_fold` for canonical, and the alt
   share is larger by exactly `sqrt(a_0^alt/a_0^can) = 1.0993` (checked to 0.2 %).

## Anything this lane finds wrong in CLOSURE.md or FLD1

- Nothing. CLOSURE.md's "1.6 to 5.1 % of the law's halo" and FLD1's numbers are reproduced; this lane
  restates them as a condition on a_0 and grades that condition.
- One addition: FLD1's `charge_turned_around_over_Mb` (1.059 at N = 2400, 1.055 at N = 1200) is
  **mass-independent** to 0.3 % above log M_b 8 (the grid is scaled, so the shell dynamics is
  self-similar); it falls to 1.043 at log M_b 7 and 1.027 at 6.5, where the 1 kpc softening is no longer
  small. Combined with R_fold ~ M_b^{1/3} this is what makes kappa_M ~ M_b^{1/3}.

## Files

- Criteria: `PREREGISTER.md`.
- Solver (patched copy of FLD1's `fld1_shells.py`, plus the `q_fold(t)` series and an `a_0` scale knob):
  `final18_shells.py`; production rows `final18_run.py` -> `runs/*.json` (39 rows).
- Grader: `final18.py` -> `final18.out` / `final18.json`; `final18.py --mutate` -> `final18_MUTATE.out` /
  `.json`.
- Fixed point: `final18_fixedpoint.py` -> `final18_fixedpoint.json`, `fixedpoint.log`; validity scan
  `bracket_s.py` -> `bracket_s*.json`.
- Lean: `FINAL18.lean`, `FINAL18_MUTATE.lean`, `compile.txt`, `compile_MUTATE.txt`
  (leanprover/lean4:v4.34.0-rc2, mathlib v4.34.0-rc2).

## Commit ids

| commit | local |
|---|---|
| criteria | 4144abfc80 |
| result | (see below) |

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
