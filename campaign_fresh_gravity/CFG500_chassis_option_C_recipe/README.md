# CFG500: chassis option C as a full track. Candidate B as a recipe is C VIABLE WITH CONFLICTS (frozen rule)

Criteria frozen first: [FROZEN_CRITERIA.md](FROZEN_CRITERIA.md), commit 21b1db999, committed alone before any script.
The owner's instruction (2026-10-08) was "try both A and C". This lane does C; CFG499 does A, and nothing was shared
with it. This is a specification plus a scored audit of committed results. No physics is computed and nothing is
downloaded. Every file is read at HEAD with `git show`.

| run | outputs | controls | exit code |
|---|---|---|---|
| main | `cfg500_recipe_scoring.out`, `cfg500_results.json` | 6/7: K1 (literal "33 tiles") fails, see Disclosure 1 | 1 |
| MUTATE (`CFG500_MUTATE=1`: per-catchment mass conservation removed) | `cfg500_recipe_scoring_MUTATE.out`, `cfg500_results_MUTATE.json` | 6/7 (same K1) | 1, by design; TEETH DETECTED |

    python3 campaign_fresh_gravity/CFG500_chassis_option_C_recipe/cfg500_recipe_scoring.py
    CFG500_MUTATE=1 python3 campaign_fresh_gravity/CFG500_chassis_option_C_recipe/cfg500_recipe_scoring.py

Both runs take a few seconds. The specification and the one-page plain-language summary are in [RECIPE.md](RECIPE.md).

## Bottom line
- **Verdict (frozen §5): C VIABLE WITH CONFLICTS.**
  - No status-board tile fails under C beyond the board's two known FAILs. Both of those belong to the retired ungated
    chassis and become MOOT, which is not the same as passed.
  - There is one real conflict, C1, the lensing-edge clash. It is resolved on the record only by a hand-set support, and
    otherwise it is PENDING on CFG498.
  - The second conflict, C2, applies only if the optional settling clock is used as the support.
- **Constants: 18 counted.**
  - 2 fitted: κ and Ω_c h².
  - 2 data: ρ_DE(t) and f_b.
  - 1 declared function: ν_mono.
  - 2 declared constants: δ = 0.05 and x_e = 0.4.
  - 9 declared rules.
  - 1 discrete choice: the footing.
  - 1 nuisance: M/L.
  - Add 1 if the settling clock is used. Two inherited engine settings are not counted, because CFG427 shows the growth
    pass is insensitive to them.
  - Reconciled with CFG469's 15 as 15 + 3: δ split out (+1); the supply postulate and catchment conservation split out of
    the growth-edge row, with the edge itself derived (+1); the max rule T5 added (+1; it is in CFG7's B ledger); the
    footing added (+1); "G = measured G" retired as vacuous without α_c (−1).
- **Scorecard, 29 board tiles.**

  | status under C | tiles |
  |---|---|
  | PASS (5) | SPARC; MeerKAT; KiDS; clusters/Bullet; M31 + LV dwarfs |
  | COND (3) | globulars; MW ultra-faints; growth (B) |
  | UNDEC (4) | a₀(z); halo-free high z; CRISTAL/ALESS; SLUGGS |
  | OPEN (3) | DR4; why κ = ½; cold-energy amount |
  | DECLARED (1) | ownership: the "from an action" question is retired |
  | PARTIAL (1) | Solar System: Cassini Q2 PASS via ownership; PPN UNTESTED |
  | UNTESTED (10) | GW speed; two well-posedness tiles; lapse; pulsars; strong coupling; G9; G0; black holes; G12 |
  | MOOT (2) | zero-field FAIL; chassis-alone growth FAIL |

  On the board the same 29 tiles read: 10 PASS, 9 COND, 4 UNDEC, 4 OPEN, 2 FAIL. No tile is raised (K3).
- **Unavailable without the chassis:**
  - GW speed and polarisations;
  - full PPN;
  - binary pulsars and neutron-star sensitivities;
  - BBN and the CMB, standard by declaration rather than predicted;
  - black holes;
  - strong field and collapse;
  - Φ = Ψ as a derivation;
  - preferred-frame effects;
  - the Cauchy problem, DOF and ghost count, strong coupling and radiative stability.
- **Lost (none of these is a pass of B):**
  - CFG373's zero-constant lapse carrier;
  - CFG381's sink route (it needed +1 constant anyway);
  - CFG462, which was a FAIL;
  - CFG483's khronon-boundary derivation of σ⁴ = G M_b a₀/4 given the cosmic budget. Its edge is 4.02 r_M, its falsifier
    is UNDECIDED at 256³, and it is not on STANDING;
  - the khronon tie κ = 2√(8π)/(3β), with β = 6.684 not derived;
  - the chassis's own passes;
  - CFG467/469's α_c window, which is now moot.

## The conflicts

**C1, the lensing-edge clash.** Growth needs the supply postulate, which gives the 5.85 r_M edge, plus per-catchment
conservation (16/16 runs). On real lenses that edge fails:

| test | result with the 5.85 r_M edge | source |
|---|---|---|
| KiDS | χ² − best = +60.5 / +70.6 | CFG487 |
| SPARC alt dwarfs | A3 = 0.864 (< 0.90) | CFG487 |
| early-type levels | χ² 30.5 / 38.1 vs ≤ 12.59 | CFG485 R8, CFG494 K4, CFG497 K5 |

KiDS passes with the declared x_e = 0.4. The resolutions on record:
- **Hand-set (passes both).** One support x = 0.4 r_ta for lensing and growth.
  - KiDS +0.79 / +2.16 vs best (CFG413). Growth at 512³ 0.080 / 0.0996 (CFG414; the alt run passes by 0.0004).
  - SPARC is unaffected for x ≥ 0.16 (CFG487 E2 row). Early types pass with any extended edge (CFG494).
  - Costs: x is hand-set (the owner's 10-07 rule; CFG414 calls itself a diagnostic). CFG414 also uses the hand-set
    R_c = 3 Mpc/h (+1 constant) and has no per-catchment conservation.
- **Zero-knob clock taper, CFG487 V1.** Passes KiDS (+2.05 / +0.71) and SPARC, but growth is in TENSION (max|P−1| 0.174 /
  0.202 post hoc) and V1 is an MS1 exception.
- **CFG498,** clock taper + capped conservation: criteria d9c739010, **no committed result, PENDING**.

**C2.** The settling clock used as the support without the edge overdraws the cold supply (CFG487 V1-CATCH, TENSION).
This conflict exists only if the optional clock is adopted as the support.

**Tensions and dependencies (no board tile flips):**
- **C3.** The V1 clock reads the cold energy, against MS1. The strict MS1 version, V2, fails KiDS (+6.2 / +11.1).
- **C4.** The supply limit cannot set the cluster, group or Milky Way levels (CFG379 FAILS; CFG497 bonus: clusters off by
  0.007 / 0.008).
- **C6.** The kernel moves κ by +0.06 to +0.09 dex (CFG493). CFG468 has frozen criteria and no committed result.
- **C7.** Relaxation has no force. Mass is conserved per catchment, but energy and momentum are not tracked, and G9 is
  UNTESTED under C.

**Consistent:**
- **C5.** The switch is exactly off on FRW (CFG487), matching the background rule. CMB lensing is 1.000 and the forest
  deviation 0.00.

## MUTATE
Removing per-catchment mass conservation (E4) triggers the missing-rule flag on the growth tile. The flag reads CFG424's
committed "MUTATE (no compensation)" row from `cfg424_results.json`: σ8 1.0326, max|P−1| 0.154 > 0.10, TENSION. The
tile goes from COND to TENSION, and the verdict changes to **C NOT VIABLE**. TEETH DETECTED.

## Controls
| control | result |
|---|---|
| K1 literal (33 tiles) | **FAIL**, kept: the board has 29 tiles (Disclosure 1) |
| K1b | 29 parsed and 29 scored, none invented |
| K2 | 93/93 evidence quotes found verbatim at HEAD |
| K3 | no tile raised above its board status |
| K4 | CFG469's 12 chassis tiles reproduced; CFG469's 15 = 2 / 2 / 1 / 9 / 1 |
| K5 | ten JSON numbers reproduce the README values (CFG424, CFG487, CFG414, CFG425, CFG439, CFG460) |
| K6 | no CFG498 result was read (its working files are uncommitted) |

## Disclosures
1. **The frozen K1 said "33 parsed tiles".** The board script has 11 + 8 + 6 + 4 = 29. This was my counting error in
   the criteria. The literal check is kept and fails, and the main run exits 1 because of it. K1b scores the rule's
   intent (every tile once, none invented) and passes. No verdict depends on the number.
2. **K3 ranking reading.** The frozen order did not place MOOT relative to FAIL. The script ranks MOOT with FAIL ("moot
   is not passed"), so a retired FAIL is never counted as raised. With MOOT ranked above FAIL, K3 would have flagged the
   two moot tiles, even though the scoring rule prescribes MOOT for them.
3. **MUTATE exit code.** The frozen §6 gives exit 1 in MUTATE whether or not the teeth are detected. The printed line
   distinguishes the two cases. The "verdict changed" test compares against the main run's verdict string, hardcoded as
   "C VIABLE WITH CONFLICTS". That is the main run's printed result.
4. **Not blind.** All sources were read before freezing, and the expected verdict was written into the criteria.
5. **The scorecard is a curated reading of the board.** The tile → recipe-item dependencies and the chassis flags are
   this lane's reading of the committed record, as in CFG469. Quotes are machine-checked; the reading itself is not a
   computation.
6. **CFG483** is committed (538a910fb) but is not on STANDING and has no README. It is cited as a lost LEAD, unaudited.
7. **The hand-set resolution of C1** combines CFG413 (KiDS at x = 0.4 with a free two-halo term) and CFG414 (growth at
   x = 0.4 with the RES rule, R_c = 3 Mpc/h). It is the same x on both legs, but not one engine run of one object.

## What this lane cannot say
- A recipe has no action. Every relativistic tile is **untested, not passed**. Option C does not resolve CFG467's α_c
  tension: it removes the place where the tension lives.
- "VIABLE WITH CONFLICTS" means the recipe agrees with the committed effective-level record apart from the listed
  conflicts. It does not mean "the theory works", it is not a derivation, and it is not "theory closed".
- κ = ½ is FITTED. The cold energy's mass is required, and no dark-matter particle is added. The supply postulate is an
  input.
