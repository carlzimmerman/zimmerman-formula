# CFG500 FROZEN CRITERIA: chassis option C as a full track. Candidate B stated as an explicit recipe, its constants recounted, scored against every status-board tile, and checked for internal consistency

Written 2026-10-08. Committed alone, before any CFG500 script exists and before any CFG500 number is computed.
Nothing below may change after a result is seen. Any later departure goes in the README as a disclosed deviation.

**Owner instruction (2026-10-08):** "try both A and C". This lane does option C. CFG499 does option A in parallel.
Nothing is read from or written to CFG499.

**Standing.** κ = ½ is FITTED. Kernel ν_mono by default. Both footings (a0 = 9.3603e-11 and 1.1312e-10 m/s²) are
reported separately and never pooled. a0 tracks ρ_DE(z): it is flat only if w = −1. "Cold energy" = the cold clumping
component (was "cold fluid"). Its MASS is still required. No dark-matter particle species is added. Untested is not
passed. Never "theory closed". Never "the data favour the framework".

**On-disk and committed only.** No downloads. No new physics computation: this lane is a specification plus a scored
audit of committed results. Every number it uses is read from a file committed at HEAD (read with `git show HEAD:path`,
so uncommitted outputs, such as CFG498's working files, cannot enter). CFG498 (criteria d9c739010) has no committed
result: it is referenced as PENDING and scores nothing.

**Not blind (disclosed).** Before writing this file I read CFG469's README (option C, the 15-input table, the 16
untested gates), the status board script `closure_map/status_picture_2026_10_03.py` (33 tiles), the board explainer
(10-08), GATES.md, RECIPE_GATE_AUDIT_2026-10-03, STANDING's 10-08 block, the 10-06 working model, the failure ledger
10-08, and the READMEs/results of CFG373, 381, 413, 414, 416, 424, 425, 427, 439, 460, 461, 462, 464, 465, 466, 467, 483
(.out), 484, 485, 487, 488, 489, 490, 491, 493, 494, 497. Expected outcome (a judgement, not a rule): **C VIABLE WITH
CONFLICTS**, the conflict being the lensing-edge clash (the 5.85 r_M edge vs the KiDS edge), resolvable on the record
only with the hand-set x = 0.4 r_ta (CFG413 + CFG414), which the owner's 10-07 rule forbids, or by CFG498 (pending).

## 1. Deliverables

1. `RECIPE.md`: candidate B as a self-contained specification (foundation-style). For each item: statement, status
   (FITTED / DATA / DECLARED FUNCTION / DECLARED CONSTANT / DECLARED RULE / DECLARED DISCRETE CHOICE / NUISANCE /
   DERIVED-given-inputs), and the committed lanes that test it. Items required: the law (a0 = κ c √(G ρ_DE), κ fitted,
   footings); the kernel (ν_mono; CFG493: kernel choice moves κ; CFG468 has frozen criteria and no committed result);
   the bound-only switch; ownership; the cold energy's amount (input); the supply postulate (input; six failed
   derivations CFG461 / 462 / 488 / 490 / 494 / 497); the zero-knob edge and per-catchment mass conservation
   (CFG424–460); the settling clock (CFG487), optional; a0(z) tracking ρ_DE. Ends with a one-page plain-language
   summary for the foundation programme.
2. `cfg500_recipe_scoring.py`: encodes the recipe, the 33 board tiles, the scoring rule and the consistency checks;
   reads committed numbers; prints the scorecard, the constant count, the conflicts and the verdict.
3. Outputs: `cfg500_recipe_scoring.out`, `cfg500_results.json`; MUTATE: `cfg500_recipe_scoring_MUTATE.out`,
   `cfg500_results_MUTATE.json` (separate files, named by mode).
4. `README.md`.

## 2. Constant count (rule)

- Count every item a user of the recipe must supply that is not ordinary measured physics (G, c, ħ are not counted;
  the law's functional form is the hypothesis itself and is not counted, as in CFG469).
- Categories: FITTED, DATA, DECLARED FUNCTION, DECLARED CONSTANT, DECLARED RULE, DECLARED DISCRETE CHOICE, NUISANCE.
  An item that follows from other listed items with no further choice is DERIVED-given-inputs and is not counted.
- Settings inherited by a test engine are reported separately. They are counted as recipe constants only if no
  committed lane shows the result insensitive to them.
- Reconcile line by line with CFG469's 15 (2 fitted, 2 data, 1 declared function, 9 declared rules or constants,
  1 nuisance): every difference is named, with its reason.

## 3. Scoring rule (each status-board tile)

The tile list is parsed from `closure_map/status_picture_2026_10_03.py` at HEAD. Control K1: every parsed tile is
scored exactly once, and no tile is invented.

For each tile the script records its board status, the recipe items it depends on, whether it depends on a
chassis-only ingredient (the khronon, α_c, c_2, the heat filter / ξ, the leaf average, the C-H term, the lapse), and the
committed evidence. Status under C:

- **UNTESTED**: the tile's pass, condition or fail is a property of the relativistic chassis, and the recipe makes no
  statement on it. This holds whatever the board colour was. Untested is not passed.
- **MOOT**: the board FAIL belongs to an object the recipe retires (the ungated chassis). Moot is not passed.
- **PARTIAL**: a tile that bundles a chassis-only part with a recipe part; each part is scored separately.
- **DECLARED (question retired)**: a "deep why" tile whose question becomes a declared rule under C. It is not passed.
- **otherwise the board status carries over** (PASS / COND / UNDEC / OPEN / FAIL), with any committed 10-08 update
  attached as a note. The status may NOT be raised by this lane.
- **Missing-rule flag (used by MUTATE):** if a tile depends on a recipe item that is absent from the recipe, its status
  becomes the committed result for the object without that item, when the record holds one (it must be read from a
  committed JSON), else UNSUPPORTED.

Also listed, from committed sources: (i) the results LOST by dropping the chassis (CFG469's list: CFG373, CFG381,
CFG462, CFG483, the khronon κ ↔ ρ_Λ link; plus anything else found), each labelled as a mechanism lead, a fail or a
tie, never as a pass; (ii) the relativistic predictions that become unavailable (GW speed, PPN, binary pulsars, BBN,
black holes, strong field, and any further GATES §4 / §5 row).

## 4. Consistency rule (pairs of recipe items)

- **Conflict:** two recipe items R_i and R_j such that committed results show a board PASS or COND tile G_a needs R_i,
  a board PASS or COND tile G_b needs R_j, and the single object that applies R_i to G_b's data (or R_j to G_a's)
  FAILS or is in TENSION by a committed frozen rule.
- A conflict is **RESOLVED ON RECORD** if one committed rule variant passes both tiles by committed frozen rules. The
  resolution is labelled ZERO-KNOB or HAND-SET (and a hand-set resolution adds its constant to the count).
  It is **PENDING** if the only candidate resolution is a lane with committed criteria and no committed result.
- **Tension, not conflict:** a recipe item whose derivation or level prediction fails (for example a level the supply
  rule cannot set) while no board tile flips. Listed separately.
- The script must test at least: (C1) the lensing-edge clash, 5.85 r_M edge vs KiDS edge x_e = 0.4 (CFG485, CFG487,
  CFG494/497 early-type levels, CFG413, CFG414, CFG498 pending); (C2) the settling clock without the edge vs growth
  (CFG487 V1-CATCH); (C3) the V1 clock vs the bound-only switch rule MS1; (C4) the supply limit vs cluster levels
  (CFG379, CFG497 bonus); (C5) the bound-only switch vs the background rule (switch off on FRW); (C6) the kernel vs
  κ (CFG493).

## 5. Verdict (frozen)

Scored on the SPECIFICATION in RECIPE.md (the zero-knob recipe as the record holds it). Rule variants are used only to
resolve conflicts.

- **C VIABLE AS RECIPE**: no conflict, and no tile scored FAIL or TENSION under C except tiles the board already shows
  as FAIL (which become MOOT if chassis-only).
- **C VIABLE WITH CONFLICTS (list)**: at least one conflict; every conflict is RESOLVED ON RECORD (zero-knob or
  hand-set) or PENDING; and no tile scored FAIL or TENSION under C beyond the board's known fails.
- **C NOT VIABLE**: a conflict with neither a resolution on record nor a pending lane; OR a tile that is PASS / COND /
  UNDEC / OPEN on the board scores FAIL, TENSION or UNSUPPORTED under C for a reason other than a listed conflict.

Whatever the verdict, the 16-plus relativistic gates stay UNTESTED and are reported as such. A VIABLE verdict is "the
recipe is consistent with the committed record at the effective level". It is not "the theory works", not a derivation,
and not "theory closed".

## 6. MUTATE (teeth)

`CFG500_MUTATE=1` removes one declared rule: **per-catchment mass conservation** (CFG424's compensation from the
turnaround catchment). Required: the scoring flags the growth tile through the missing-rule flag, reading CFG424's
committed "MUTATE (no compensation)" row from `CFG424_turnaround_catchment/cfg424_results.json` (TENSION expected by
that file, not by this lane), and the verdict changes from the main run's. If the growth tile is not flagged, or the
verdict does not change, the teeth have failed and the script exits 1 in MUTATE mode with "TEETH NOT DETECTED". The
MUTATE run exits 1 by design when detected (the recipe is then NOT VIABLE).

## 7. Controls

- **K1** tile coverage: 33 parsed tiles, each scored once.
- **K2** provenance: every evidence quote is found verbatim in its file at HEAD (as CFG469 K7a). A missing quote fails K2.
- **K3** no upgrade: no tile's status under C is above its board status (order FAIL < TENSION < UNDEC/OPEN < COND < PASS;
  UNTESTED / MOOT / DECLARED / PARTIAL count as below PASS).
- **K4** CFG469 reproduction: the script's list of chassis-dependent tiles contains CFG469's 12 tiles, and the recount
  starts from CFG469's 15 exactly (2 / 2 / 1 / 9 / 1).
- **K5** numbers read from JSON reproduce the README-quoted values: CFG424 MUTATE max|P−1| 0.154; CFG487 KiDS E1 +60.5 /
  +70.6; CFG487 V1 no-edge +2.05 / +0.71; CFG414 alt 0.0996; CFG425 R3 0.033; CFG439 0.040 / 0.033; CFG460 0.040
  (each to the printed precision).
- **K6** pending-lane guard: no CFG498 file outside its committed FROZEN_CRITERIA.md is read.

Main run exits 0 iff K1–K6 pass. Outcome headlines do not set the exit code in the main run.

## 8. Honesty lines (printed in every output)

κ = ½ FITTED (CFG493: 0.42 ± 0.10 / 0.35 ± 0.08, consistent but not discriminating; the kernel moves it by more than
the ½ vs 1/√π gap). The cold energy's mass is required; no dark-matter particle. The supply postulate is an input. A
recipe has no action: its relativistic sector is untested, not passed. Not "theory closed".
