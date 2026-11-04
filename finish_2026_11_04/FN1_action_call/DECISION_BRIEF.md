# FN1: the action call for PAPER67's requirement 12

A decision brief for the owner, item 1 of the finish push. Criteria `FROZEN_CRITERIA.md` (72f9d70fd6). κ = ½ FITTED.
Footings canonical a0 = 9.3603e-11 and alt 1.1312e-10 m/s², never pooled. The theory is not closed. Nothing here says
the data favour the framework. This brief adopts nothing: the choice is the owner's. V3W (the v3s weak-spot tests) is
still running and is not cited.

## Bottom line

PAPER67's requirement 12 asks for an action for the law g_N = g²/(g + a0). No action on record gives that law and
passes the Solar System without a screening length. Every class whose static limit is AQUAL or QUMOND with the law's
interpolation fails Cassini's Q2 by 1.69–5.18× Hees (AX1).
**(a)** v3s is the one action on record that passes AX1's G1–G4 on both footings, and its Solar-System gate is a clean
PASS (C6P). It also fails as gravity plus cosmology, as the 2026-10-24 verdict records, and it carries its own dust term.
**(b)** No smoothed-QUMOND action exists. Its static limit with one universal length was graded here (FN1b):
Cassini and the planets pass at every length from 0.024 to 2 kpc, but no length passes all five static gates on either
footing. The Milky Way passes only at 2 kpc, where the dwarfs read 6/24 and SPARC fails. The dwarfs pass only up to
0.1 kpc, where no Milky Way cell passes.
**(c)** Selecting nothing keeps requirement 12 open, which is what the PAPER67 v1.1 draft already says. Of the two
options that select an action, (a) leaves the fewest ungraded doors. In every option a0 is put in by hand.

## At a glance

| | (a) v3s as it stands | (b) smoothed QUMOND, one fixed length | (c) no action selected |
|---|---|---|---|
| an action on record | yes, frozen on 2026-10-24 | no | no |
| its static limit gives the law | yes ("This is law S") | yes, as the length goes to zero | the law itself |
| Solar System | clean PASS on both footings (C6P) | static PASS at every length (FN1b) | the unscreened law fails (PAPER58) |
| galaxies at one setting | SPARC rms 0.054 / 0.054 dex | no length passes all five static gates (FN1b) | the law's own record |
| a0 from the action (G5) | by hand | by hand | by hand |
| clusters, growth and CMB, radiation era, hosted dwarfs, Milky Way disc | graded, all FAIL | ungraded | open, as now |
| what the owner would decide | adopt v3s with its failures stated | pursue an action that does not exist yet; its one-length static limit already fails | state requirement 12 as open |

## (a) v3s as it stands

The action is frozen in `covariant_push_2026_10_22/V3S_FINAL_VERDICT_2026-10-24.md` (the verdict below). Its static
limit is the law: "This is law S" (the verdict's 2026-11-01 erratum).

**Passes**

| test | result | source |
|---|---|---|
| SPARC RAR | rms 0.054 / 0.054 dex | verdict, pass table |
| Cassini Q2 | clean PASS on both footings: Q2 ≥ 4.85e7 inside Hees 9.0e-27 (canonical) and ≥ 5.70e7 (Hees) (alt) | C6P |
| planets | Mars 0.173 of bound at 24 pc | C6P |
| GW speed, binary pulsars | c_T = c; ≤ 3.2e-14 of the double pulsar's precision | verdict, pass table |
| constraint algebra | closes with 3 DOF | verdict, pass table |
| AX1 | **UNDECIDED, reading PASS** on G1–G4; C6P then cleared the one failed check | `rebuild_2026_10_22/AX1_action_for_law/README.md` |

**Fails** (the verdict's failure table)

| failure | numbers |
|---|---|
| cluster cores | 1.5–1.7 × the law in 0.3–1 Mpc |
| linear growth and CMB | σ₈/σ₈,dust 0.003–0.005 |
| radiation era | BBN needs μ_K ≥ 1.84e8 h/Mpc |
| hosted dwarfs | Antlia II 24σ, MW ultra-faints 12.6σ |
| Milky Way disc | K_z(1.1 kpc) 92–97 vs 66.4 ± 2.2 |
| caustics | STRUCTURAL GAP |

The verdict's own summary: "As a galaxy-scale law, v3s is complete and passes"; "As a theory of gravity and cosmology,
v3s fails".

**Ungraded or open**
- The Lyman-α forest after saturation is UNDECIDED under the frozen rule (X18, the verdict's caustic-completion table).
- Binary pulsars: PASS on a condition, |s₁ − s₂| < 7e-7, with the strong-field sensitivity uncomputed (X16, same table).
- L★ has a lower bound only: L★ ≥ 21.7 / 22.9 pc (D10, the verdict's frozen theory); **≥ 24.0 pc** canonical and
  ≥ 24.7 pc alt (CFG820). The classical dSphs want 5.75–22 pc, which CFG821 labels INCONSISTENT, conditional: they sit
  above even the unscreened law (Draco 9.6 vs 4.6 km/s).
- G5: a0 = c² √(Λ/32π) with κ fitted, put in by hand (the verdict's frozen theory). KF1 finds NOTHING FORCED.

**What adopting it brings**
- v3s's action carries its own dust: its inputs include "the cold-dust abundance (an initial condition)" (the
  verdict's frozen theory). The law in PAPER67 has no cold term ("It has no action and supplies no dust-like term for the CMB"), and route E's
  cold sector was retired on 2026-11-01 (`rebuild_2026_10_22/OWNER_DECISION_2026-11-01_RETIRE_COLD_SECTOR.md`).
  Whether v3s's dust term sits inside that retirement is the owner's call.
- The verdict froze v3s on 2026-10-24. The owner's 2026-11-04 lift lets test lanes reopen it, and they adopt nothing.

**What finishing it would take.** No new calculation is needed to state it: the action exists and every AX1 gate has a
verdict. It needs the owner's written decision to adopt v3s with its failures stated as failures. Closing X18 would need
a "nonlinear code started from a cap-consistent state" (the verdict, on X18).

**What PAPER67 would then say** (proposed, for the owner's go; not edited):
- Requirement 12, law column: "v3s (Khronon with switched stiffness): passes G1–G4 on both footings; fails cluster
  cores, linear growth, the radiation era, hosted dwarfs and the Milky Way disc; a0 by hand."
- The "An action" item: "v3s is taken as the law's action. Its static limit is the law, and with L★ of at least 24 pc it
  passes the Solar System on both footings (C6P). As a theory of gravity and cosmology it fails (2026-10-24 verdict). Its
  action carries a dust term whose abundance is an initial condition."

**What STANDING.md would then say** (proposed dated addendum, not edited): "Addendum (FN1, owner's decision): the galaxy
law's action is v3s as frozen on 2026-10-24. It passes AX1's G1–G4 and the Solar System on both footings; the
2026-10-24 failures stand; a0 is put in by hand; κ = ½ FITTED; the theory is not closed."

## (b) A covariant smoothed-QUMOND action with one fixed length

**What exists**
- No such action is on record. AX1 calls it "the same mechanism as L★ in another form", for which "no action for it
  exists".
- Any action whose matter couples to the phantom through a fixed kernel S has the static limit
  Φ = Φ_N[ρ] + S Φ_ph[Sρ]. The outer S makes the force on matter the gradient of one energy, so action equals
  reaction. The record's filtered rules
  (KT14–KT19) leave it out, so they are not the static limit of any action. FN1b grades both forms and labels this one
  (form R).
- The length is not v3s's L★. v3s's screened core is set by L*² = 2 r_M ℓ_γ (CFG691), so it shrinks as the mass grows.
  A smoothing length is the same for every mass. The two mechanisms share Q2's fix, not their static limits.
- The record's nearest covariant attempts:
  - a Helmholtz filter made local was closed because "localising the filter adds a propagating mode" (Theorem 8). Kept
    as a constraint, whether it survives in a covariant host was left open (the hunt's support-brief addendum);
  - a khronon plus a (D²χ)² healing-length scalar is v3's scalar pair (AS3, 6770f2d8ad): Q2 passes, margin 2.8e7, 4.0e7;
    FRW growth fails, sigma8 ratio 0.0757, 0.0817 against line 0.95.

**The static limit, graded here** (`FN1b_fixed_length_static/`, criteria e6e031a163, result 22f8e50070). Form R; canonical / alt:

| L, kpc | MW cells of 1,375 | dwarfs, E1 (line 15/24) | SPARC | Cassini Q2 / ceiling | row |
|---|---|---|---|---|---|
| 0.024 | 0 / 0 | 18 / 18 | NOT EVALUABLE (V4) | 7.41e-10 / 8.68e-10 | FAILS: T0 |
| 0.1 | 0 / 0 | 16 / 16 | SURVIVES SPARC | 1.02e-11 / 1.20e-11 | FAILS: T0 |
| 0.25 | 0 / 0 | 14 / 14 | SURVIVES SPARC | 6.55e-13 / 7.68e-13 | FAILS: T0, T2 |
| 0.5 | 0 / 0 | 12 / 13 | SURVIVES SPARC | 8.19e-14 / 9.60e-14 | FAILS: T0, T2 |
| 1.0 | 0 / 0 | 9 / 10 | HURT | 1.02e-14 / 1.20e-14 | FAILS: T0, T2, T3 |
| 2.0 | 2 [GRID-DEPENDENT] / 38 | 6 / 6 | FAILS SPARC | 1.28e-15 / 1.50e-15 | FAILS: T2, T3 |

- **Label: NO UNIVERSAL LENGTH PASSES**, on both footings. The planets pass at every length.
- The record's source-only rule, graded beside, reads UNDECIDED (NOT EVALUABLE at L = 0.024 kpc) on canonical and
  NO UNIVERSAL LENGTH PASSES on alt.
- Failed checks, reported in FN1b's README:
  - KT14's smoothing test at 24 pc reads 1.5e-02 against its 1e-3 line, so the source-only Milky Way row there is NOT
    EVALUABLE;
  - V4 fails on SPARC at 24 pc (4.7e-01): KT19's grid does not resolve that length;
  - peak RSS 1.31 GiB against a 1 GB target.

**Ungraded.** Lensing, GW speed, health and degrees of freedom, PPN beyond the static quadrupole, FRW and the CMB,
clusters and caustics. Also a Helmholtz kernel, and wide binaries.

**What finishing it would take.**
- Write the action and choose its kernel. A Gaussian is non-local; a Helmholtz kernel needs an auxiliary field kept as
  a constraint.
- Count its degrees of freedom, then grade PPN, GW speed, lensing and FRW.
- Regrade the static gates on that kernel. With a Gaussian, FN1b finds no single length that passes, so the action
  would need a second scale or a mass-dependent one, each a new input put in by hand.

**What PAPER67 would then say** (proposed): requirement 12 stays open until the action exists, and the text adds: "The
candidate is a smoothed-QUMOND action with one fixed length. None exists yet. Its static limit with one Gaussian length
fails the five static gates at every length tried (FN1b)."

**What STANDING.md would then say** (proposed dated addendum): "Addendum (FN1, owner's decision): the action to pursue is
a covariant smoothed QUMOND with one fixed length. None exists. Its static limit with a Gaussian kernel passes no length
tried: the Milky Way wants the largest length, the dwarfs the smallest (FN1b)." 

## (c) No action selected

- The PAPER67 v1.1 draft already says it: "None is selected, and the a0 sector's action stays open." Its requirement
  row reads "open; 0 of 717 in AS2's Tier A; unscreened classes fail Q2 (AX1); only v3s's screen passes the Solar
  System (C6P)".
- The 2026-11-01 retirement already says "The a₀ sector's action stays open".
- **Passes and fails.** Nothing new is claimed. The law alone keeps its record. Its unscreened Solar System fails:
  2.44–4.59× the Hees line (canonical) and 2.85–5.19× (alt) under AQUAL (PAPER58).
- **Ungraded.** Requirement 12 itself, stated as open. The owner's 2026-11-02 one-field action lane did not produce an
  action either: AN1's rerun and AN2 both read NO VERDICT.
- **What finishing it would take.** Nothing. The text already states it.
- **What PAPER67 would then say** (proposed): keep row 12 and add one sentence to the "An action" item: "No action is
  selected: unscreened classes fail Cassini (AX1), v3s fails as gravity plus cosmology, and a smoothed QUMOND with one
  Gaussian length passes no length on the static gates (FN1b)."
- **What STANDING.md would then say** (proposed dated addendum): "Addendum (FN1, owner's decision): no action is
  selected for the galaxy law; requirement 12 stays open. AX1 and FN1b are the record of why."

## Ungraded doors, counted

| door | (a) v3s | (b) one-length smoothed QUMOND | (c) none selected |
|---|---|---|---|
| G1 galaxies | PASS | static grade: no single length passes | the law's record |
| G2 Solar System | PASS (C6P) | static PASS (FN1b) | the unscreened law fails |
| G3 lensing = dynamics | PASS (AX1, a reading of the record) | ungraded | not posed |
| G4 GW speed and health | PASS (AX1, a reading of the record) | ungraded | not posed |
| G5 a0 from the action | by hand | by hand | not posed |
| clusters | FAIL | ungraded | open |
| growth and CMB | FAIL | ungraded | open |
| radiation era | FAIL | ungraded | not posed |
| hosted dwarfs | FAIL | static only (FN1b's dwarfs include the MW satellites) | open |
| Milky Way disc | FAIL | static FAIL at every length but the largest (FN1b) | open |
| caustics | STRUCTURAL GAP | ungraded | not posed |

- (a) leaves none of these ungraded. Its open items are X18, X16 and the L★ band.
- (b) leaves six ungraded.
- (c) selects no action, so these doors are not posed. Requirement 12 is the one open door, stated as open.

## Sources

| short name | file | last commit read |
|---|---|---|
| AX1 | `rebuild_2026_10_22/AX1_action_for_law/README.md` (lead table, C6P line) | 17d7b7ecdc |
| C6P | `rebuild_2026_10_22/C6P_cassini_high_precision/README.md` | 8c5703da06 |
| the verdict | `covariant_push_2026_10_22/V3S_FINAL_VERDICT_2026-10-24.md`, committed text (another session has uncommitted edits elsewhere in it) | d7e1baed56 |
| CFG820, CFG821, CFG691 | `campaign_fresh_gravity/CFG820_stiffness_from_globulars/`, `CFG821_stiffness_from_dsph/`, `CFG691_stiffness_window/` | a57fe156ef, ac7002034a, d7c9b9a252 |
| KF1 | `rebuild_2026_10_22/KF1_argon_kappa_routes/README.md` | 5abc2d1ae6 |
| AS3 | `rebuild_2026_10_22/AS3_ppn_and_khronon_scalar/README.md` | 6770f2d8ad |
| Theorem 8 | `hunt_2026/SUPPORT_BRIEF_FOR_ASTRA_2026-09-04_ADDENDUM.md` | 47c46ff7c4 |
| PAPER67 v1.1 draft | `qwen_claude_field_theory/papers_2026/PAPER67_galaxy_law_and_what_it_leaves_2026.tex` | 65f4e7b1c1 |
| PAPER58 | `qwen_claude_field_theory/papers_2026/PAPER58_doors_push_2026.tex` | 829f491862 |
| the retirement | `rebuild_2026_10_22/OWNER_DECISION_2026-11-01_RETIRE_COLD_SECTOR.md` | 1996555bf2 |
| AN1, AN2 | `rebuild_2026_10_22/AN1_aest_nonlinear_dust/README.md`, `AN2_aest_3d_fold/README.md` | f9fc20c54d, f04da07be4 |
| FN1b | `finish_2026_11_04/FN1_action_call/FN1b_fixed_length_static/` (README, `fn1b_label.out`, `fn1b_small.out`) | 22f8e50070 |

KT33 and KT34 (another session's reciprocal-filter lanes) were uncommitted when this brief was written. No number here
comes from them. FN1b uses KT33's code as an engine, copied unchanged, and reproduces its stored numbers as known answers.

## Files

- This brief; `check_brief.py`, which checks every number above against its source (`check_brief.out`; MUTATE twin
  `check_brief_MUTATE.out`); `check_brief_sources.py`, the list of checked fragments.
- `FN1b_fixed_length_static/`: criteria, scripts, outputs and README for option (b)'s static grade.
