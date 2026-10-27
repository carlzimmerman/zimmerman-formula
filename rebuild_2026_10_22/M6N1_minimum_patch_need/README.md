# M6N1_minimum_patch_need: how many baryons must M6's patches hold, and does the forest-side budget matter?

## Provenance

- **Criteria:** `FROZEN_CRITERIA.md` (3a2f5ca3a0), committed alone before any script or number.
- **One code-only guard after the first twin run:** the twin's x_min = 0 divided by zero after its required failures.
  The main output is identical before and after the guard, apart from the K4 RSS line.

**Run conventions.** κ = ½ FITTED. Footings are never pooled. Cold dark energy is a gravitating w ≈ 0 field component, not
a particle. Not "theory closed". Nothing here says the data favour the framework.

## The derived piece: the minimum patch-born fraction

- **The constraint.** Outside material arrives with the fair cold share, and there is no exchange (X54). A galaxy can then
  stay under X22's cold cap f_max only if a fraction **x_min = (1 − f_max)/(1 − f_max/(1 + δ_b,in))** of its baryons began
  in depleted patches.
- **Values.** x_min = **0.835** canonical (f_max 0.196) and **0.977** alt (f_max 0.027). Almost every baryon in such a
  galaxy must be patch-born.

## Verdict (frozen rule, both footings): **BUDGET BINDS AT RECORD RETENTION**

The required patch baryon fraction is F_need = x_min · q · F_inv / ε. It is compared with X57's provisional budget,
F_allowed = 0.0613 canonical / 0.0490 alt.

| quantity | canonical | alt |
|---|---|---|
| F_need at full retention (ε = 1), as a multiple of the budget | 0.19–0.56 × | 0.28–0.83 × |
| F_need at the record's own Lagrangian retention, as a multiple of the budget | **1.00–2.95 ×** | **1.73–5.06 ×** |
| record retention ε_ref = 1/(1 + δ_b) | 0.191 | 0.163 |
| retention needed to stay within budget, ε_crit | **0.19–0.56** | **0.28–0.83** |

- **Full retention fits.** M6 fits within the budget only if most of each patch's baryons end up in the galaxy.
- **Record retention does not.** X22 assigns each galaxy the Lagrangian volume of its law mass, and at that retention M6
  needs more baryons in patches than the budget allows, on every corner.
- **One corner is knife-edge.** Canonical, ungrouped share q 0.30, stellar-only inventory: 1.00 × (0.0616 against
  0.0613).
- **The range** spans the q bracket (0.30 ungrouped to 0.69 for 1e9–1e11 M☉) and the inventory (stars only, or stars plus
  cold gas).

## What this means

- **The forest-side budget matters.** M6 survives only if the galaxies that need it retain at least 19–56 %
  (canonical) or 28–83 % (alt) of their initial patch baryons. Under the record's own mapping, retention is 19 % / 16 %.
- **That budget is provisional.** F_allowed is X57's 20 %-of-adiabatic-variance line, not a measured forest limit.
  P1D1–P1D3 are all NOT DIAGNOSTIC, and P1D2 indicates that FGPA saturation hides M6's patches at z 4–5. So the decisive
  numbers are two:
  1. a calibrated limit on the patch fraction;
  2. a measured q with the isolation selection M6 actually needs.
- **This lane uses the closure program's population inputs** (`closure_program_2026_10_27/population`, uncommitted; sha256
  pinned) and adds the derived x_min. It is an accounting bound, not a dynamical formation model.

## Checks

- **Main: 5/5 PASS, exit 0.**
  - S0: sha256 and inputs reproduced.
  - K1: x_min matches brute force to 6.8e-8.
  - K2: accounting identity.
  - K3: limits.
  - K4: 0.31 GB.
- **Rerun.** Identical apart from the RSS line.
- **MUTATE (`M6N1_MUTATE=1`): exit 1.** It fails S0 (m2) and K1 (m1: wrong cap, x_min = 0), as required. The twin's
  verdict flips to DOES NOT BIND, so the cap is the load-bearing piece.
