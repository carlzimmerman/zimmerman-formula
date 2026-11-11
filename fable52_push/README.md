# fable52_push: one swing at completion (2026-11-09)

Adopts nothing. kappa = 1/2 FITTED; not theory closed. Nothing here is registered in the closure record.
Paper: PAPER71 v1.1, deposited 2026-11-09, DOI 10.5281/zenodo.24095262 (v1.0: DOI 10.5281/zenodo.24094860; v1.1 adds one
disclosure sentence)
(`qwen_claude_field_theory/papers_2026/PAPER71_switch_theorems_kids_outer_points_2026.pdf`; each deposit's supplement zip
holds this folder at the commit its manifest names).

## Answer first

**No completion.** I could not build a theory that passes every gate, and I do not think one exists inside the gates as
they are frozen.

**What this folder does close: one whole class of completion.** Every switch on the law that comes from an action (the
"two-phase" reading: law inside cleared regions around galaxies, cold component elsewhere) now has a failing verdict on
each of its exits. Seven lanes carry it: SWT1 (theorems), EMV1 and GAL1 (the lensing allowance, checked twice), KO1 with
its blind regrade KO1R (KiDS's outer points), SNP1 (clearing dynamics), and HE1 (the one static construction the theorems
left room for). The Lean files hold 92 theorems, standard axioms only, each file with a twin of false statements that
fails.

**Owner decision, 2026-11-09 (21:33): the record closes on form B**, the a0 law with cold dark energy counted once (the
law is how the component sits around galaxies, not a second force). It is chosen as a form, not as a pass, and changes no
label here. The decision, its gate table and its eight open items are in
`closure_2026_11_09/OWNER_DECISION_2026-11-09_FINAL_FORM_B.md`. What this folder adds to it:

- The lanes below are what closed the alternative ("law near galaxies, cold component elsewhere") on every exit.
- `ONE1_counted_once/` takes the decision's open item 4: form B on KO1's host-free KiDS lenses, with every neighbour
  carrying the same share. **KiDS host-free: PASSES / PASSES** for PD1's own share (59.5 M_b) by the frozen gate at the
  1.6 R_h veto: shape ratio 0.811 +- 0.134 against a model of 1.003 (1.1 sigma; alt 0.2 sigma). The pass does not
  separate form B from the law with no end, which gives 0.98 and also passes. At the original veto radius (reported;
  it carries the veto's edge) the model misses by 2.7 sigma (canonical). Late types sit low at every veto, and their
  error at the graded veto is too large to test them. The label covers this row only.
- The lead's pre-freeze note in that folder is superseded on three points, as ONE1's result records. It ended each halo
  at the catalogued mass, while the same lenses' inner signal asks for 2 to 3 times that mass; with the calibration
  fitted, form B reads 0.86 / 0.73 without neighbours and 1.00 / 0.85 with them, not the note's 0.525 / 0.477. Its
  "late below, early above" holds only without the calibration; the frozen type-difference line passes at every veto.
  Its "about 0.1" for the neighbours is right in size at the widest veto, not by the note's route. Its blind prediction
  for KO2 (late-type ratio at most about 0.5) is met by KO2's tied design (0.277 +- 0.183) and not by its untied one
  (1.071 +- 0.199), so it is not confirmed.
- `FB1_form_b_from_the_action/` is a note, not a lane. In the adopted action the law's halo is already the khronon
  sector's own gravitating density on one conserved current, and for a static clock the law sector's stress holds it in
  the law's shape (the action's static force balance; it holds for any law of this type, so it is not evidence for this
  one). The theory is still not complete: no single dust term serves the CMB and galaxies, the collapse to the static
  state BREAKS DOWN when computed (COL1: the infalling clock folds at the centre within 0.06 to 0.15 Gyr and the
  equations give no answer beyond), and clusters cannot be a static-clock state. MK1 confirms there is no single dust
  constant (NO VALUE: the record's CMB lines need at least 198 and 2.5e4 per Mpc; host-free KiDS allows about 1). On stability: TPA1 found the static state
  unstable with gravity frozen, in a planar background; SCS1, with gravity coupled around a point mass, finds it STABLE on
  both footings and traces TPA1's growth to the planar background. SCS2 finds it STABLE around isolated discs too: the
  law's halo density is positive in every cell of every disc solved. It goes negative only with an external field, and
  that case reads unstable in regions but is NO VERDICT (magnitudes not converged between grids).
- Form B's regrade lanes run in another session under `closure_2026_11_09/`, quoted here as their result files write
  them. RB1 (groups, X-COP, the Bullet): NOT FALSIFIED (ONE-SIDED) on both footings, never a pass. RB2 (hosted dwarfs):
  B FAILS ON THE HOSTED ROWS on both footings (Milky Way ultra-faints and bright M31 dwarfs sit high; Coma's diffuse
  galaxies and the Milky Way classical dwarfs are consistent). KO2 (own lensing field by type): NO VERDICT / NO VERDICT
  as frozen when this was written.

## 1. The class and its exits

By SWT1 T1 a law-on region shows only its baryons from outside. So outside its wall a truly isolated lens shows M_b plus
whatever share was swept there. Three choices remain.

| Exit | What grades it | Verdict | Lanes |
|---|---|---|---|
| A. Law on over KiDS's whole range | needs a filling of 0.29; CMB lensing allows 0.0231 (0.0265 / 0.0259 with external fields; 0.0197 at 2 sigma with growth); and the wall never gets there (0.43-0.63 of the range at best) | FAIL: lensing, dynamics | SWT1, EMV1, GAL1, SNP1 |
| B. Wall inside the allowance, the record's share outside | KiDS's host-free outer bins exclude it at more than 5 sigma, calibration-free, with the lens's catalogued neighbours counted (5.2 to 5.4) | FAIL: KiDS | KO1 |
| C. Wall inside the allowance, a heavy share outside | KiDS needs at least 23 / 27 M_b per galaxy (4.1 / 4.9 shares); the energetic gate clears at most 2.8 to 4.0 shares; with three shares bound, 8.6 to 19.0 M_b stay inside 200 kpc; such a shell outweighs the wall force by at least 3.8 / 4.9 | FAIL: clearing | KO1, SWT1, SNP1 |

Lighter neighbours are counted (KO1 E8): with the record's share each they add a hundredth of the law's level to a
host-free lens's outer bins. The margin of exit C against the energetic gate alone is thin at the frozen veto radius (4.1
shares needed against 3.8 cleared, canonical); against the dynamics it is not.

HE1 built the static version of exits B and C exactly: the share held outside the wall as an isothermal envelope in
pressure balance with it. The envelope exists for every mass and share in the record, is stable, leaves discs alone and
fills 0.2 % of space or less. It fails KiDS's late-type stacks. They sit near 1.5 of the law at 0.16 to 0.38 of the
measured range, so the wall would have to reach about 0.38 of the range for every lens, and any outer radius that does
that for the heavier lenses pushes the low-mass walls past the whole range and breaks the filling line (0.18 to 0.66
against 0.0354). No share at any outer radius passes the disc, filling, stability and KiDS gates together.

## 2. The lanes

| Lane | Question | Label (canonical / alt) |
|---|---|---|
| SWT1 | exact statements for any action-based switch | CP KEY-DEPENDENT; WP NOT A NO-GO AS FROZEN |
| EMV1 | does the filling statistic survive a direct nonlinear solve with an external field? | T2 HOLDS / T2 HOLDS |
| GAL1 | what do growth and CMB lensing allow for the filling history? | ALLOWANCE CONFIRMED / ALLOWANCE CONFIRMED (0.0197; 0.0134 if on from z 6) |
| KO1 | are KiDS's outer points the lens's own field? | LAW LEVEL HOLDS / LAW LEVEL HOLDS by the frozen gate |
| KO1R | blind regrade of KO1 from its criteria alone | NOT SEPARATED / LAW LEVEL HOLDS (518 tied lenses; knife edge) |
| SNP1 | can the wall pressure clear the component and keep it out? | FAILS / FAILS |
| ONE1 | does form B fit KO1's host-free lenses, neighbours included? | KiDS host-free: PASSES / PASSES at the 1.6 R_h veto (the law with no end also passes; misses at the original veto) |
| TPA1 | what are the two-phase action's field equations, and is it healthy? | EQUATIONS COMPLETE; health UNHEALTHY (a gradient instability, no ghost, in the law-on phase of a static clock with little dust; the wall and the dust phase are healthy; decoupling limit, planar background; SCS1 finds the instability does not hold around a point mass) |
| SCS1 | is the action's static law-on state stable with gravity coupled? | STABLE / STABLE around a point mass (nothing grows at any wavenumber; JEANS-ONLY at the dust constant the CMB needs; discs not analysed) |
| SCS2 | is that state stable around discs? | Isolated discs STABLE / STABLE; discs in an external field NO VERDICT / NO VERDICT (reading: unstable in regions; e-folding 0.9 to 2.4 Gyr at 0.1 a0, 27 to 75 Gyr at 0.01 a0) |
| MK1 | is there one dust constant for the CMB, clusters and galaxies? | NO VALUE / NO VALUE (does not turn on the cap; X-COP passes at no value) |
| COL1 | does a clock that starts as infalling dust reach the static state? | BREAKS DOWN / BREAKS DOWN (a caustic at the centre; a reported diagnostic puts the charge that arrives at 1 to 4 % of the law's halo) |
| HIS1 | do the systems off the law sit only where a history allows (amount set by the law at formation, then conserved)? | HOLDS EXCEPT H3 (fails), H5 (no power) / the same; the law-as-a-force reading scores 1 of 5 on the same tests |
| DD1 | with no theory assumed, does the non-baryonic mass follow one rule across every class on disk? | NO RULE AMONG THE CANDIDATES / the same (16 classes, 626 systems; the law holds on SPARC; six classes break every candidate, in both directions) |
| KDE1 | can the law's clock be the dark-energy field itself? | ALREADY IN THE RECORD AS AC2s / the same (and the record shows such a clock still falls in and folds) |
| GRW1 | can baryons and the law build late structure if the cold component is warm? | FALLS SHORT / FALLS SHORT under the action's linear theory; FALLS SHORT AND OVERSHOOTS with the static law; as frozen NO VERDICT / NO VERDICT |
| MK2 | does an exponential dust term (one sound speed) pass MK1's rows? | NO VALUE / NO VALUE (as frozen NO VALUE / NO VERDICT; clusters and groups pass at no value; galaxies clean and the clock static there above about 500 km/s) |
| FLD1 | does the folded region reach as far as the law is seen? | DOES NOT / DOES NOT (covers every rotation curve; 1.3 to 5.4 times short of KiDS's windows) |
| REL1 | can the law respond to the clock's acceleration relative to the baryons? | NOT WELL-DEFINED / NOT WELL-DEFINED (matter's motion becomes fourth order and runs away) |
| HE1 | can the share sit outside the wall as a pressure-supported envelope? | FAILS / FAILS (KiDS late-type stacks; the clusters-and-groups gate also fails as frozen, on two clusters near R500 only, and the label does not rest on it) |

## 3. What KO1 found, in plain words

- **The frozen gate passes the law.** Lenses with no galaxy 0.3 dex more massive inside their own measured range show an
  outer amplitude of 1.10 +- 0.15 / 1.00 +- 0.14 of the law.
- **That label is weaker than it looks.** The whole stack sits 1.6 to 1.8 times above the law at inner radii too, so an
  absolute level of 1 says little. Relative to its own inner level the host-free outer signal is 0.61 +- 0.09, and
  0.81 +- 0.13 once the veto's own edge effect is moved out of the way. The law's floor is 0.98; a heavy exterior gives
  0.78 / 0.66. KiDS does not separate those two.
- **What KiDS does settle.** The record's share outside a wall (5.56 M_b) is excluded at more than 5 sigma on every
  reading. With every galaxy carrying the same share, the outer bins need 33 to 47 / 40 to 56 M_b per galaxy there
  (2 sigma: at least 23 / 27).
- **Hosts are not the story I expected.** Before the freeze I estimated that leaked hosts carry 30 to 50 % of the outer
  signal. The difference is 4.9 sigma at the frozen radius but falls to +0.31 +- 0.21 when the veto is widened, so most of
  it is the veto's edge.
- **A lead, not a result.** Host-free late types show no outer signal (-0.19 +- 0.39; 0.13 +- 0.68 with the widest veto)
  while early types sit at 1.34 +- 0.18. Seen after the freeze; shares the edge effect.
- **The gas is the open flank.** With B21's own hot-gas estimate in g_bar, its published outer points drop from 1.50 to
  0.47 of the law. Nothing on disk measures that gas.

## 4. Why the theory still does not close

1. The CMB needs a cold, clustering component of about 5.4 times the baryons (F1).
2. Galaxies exist early, so the component collapsed with them, and it is conserved.
3. Removal from galaxies has a failing verdict on every route: kicks, heating, conversion, and now every action-based
   switch as a class.
4. If it is still there, either the law is not a second force on top of it (single counting: fails KiDS, the groups and
   the Bullet's amount), or it is invisible to baryons where the law acts (fails its consistency gate).

A completion has to move a gate or bring physics from outside the catalogue.

## 5. What would move it

1. **A measured gas mass at Mpc radii around isolated galaxies.** It decides whether the law over-predicts KiDS's outer
   bins (B21's estimate says by a factor of two).
2. **A clean isolation test**: spectroscopic redshifts, a veto radius well beyond the measured range, a frozen shape gate,
   late types first. Forecast done (KO3F, no signal read): with the DESI DR1 redshifts on disk a veto test has no power.
   The late-type error at the widest veto goes from 0.68 / 0.62 to 0.57 / 0.52 of the law, and a 3 sigma call needs about
   0.47. So no veto lane was frozen. The route with power models the neighbours and keeps every lens (KO2, another
   session's lane); more shear on the DESI area would also do it (DES Y3 is 312 GB, HSC Y3 needs an account).
3. **The baryon census in groups.** Unchanged from the first version of this file.

## 6. Corrections (mine and the record's)

- My first report said the wall pressure would rule out the "galaxies repel the component" family. It does not: the wall
  wins against the record's share by 3 to 20 times. It fails for other reasons (it cannot carry what KiDS needs).
- The first version of this file bet that the outer galaxy leg gives way, meaning that KiDS's outer points would turn
  out to be neighbours' mass. KO1 does not support that bet.
- My hand estimate for SNP1 (walls swept beyond KiDS's range, filling too large) was the reverse of what the runs show.
- WL1's FAIL stands, but its "any key" scope sentence does not hold for a compensated switch. SQ1 graded the opposite sign
  to the law's own term.
- Two mutation arms did not bite as frozen; both are disclosed in their lanes and neither label uses them. SWT1's M-WP
  (pressure / 100) has no power once the gate clears, and a x100 arm was added. GAL1's M-SIGN required growth to drop in
  bins that lie before one history's switch-on, where no boost exists. PAPER71 v1.0 says each lane has a mutation twin that
  must fail and does not list these two; v1.1 carries the sentence.

## Files

- `SWT1_switch_theorems/` (origin c892bac851, 6997214890, cbf83986f3)
- `EMV1_effective_medium_validation/` (origin eeb830ace2, 0e3c23f7d5)
- `GAL1_growth_lensing_allowance/` (origin f7b534d9e4, c8c6935efc, 5d9fa6d888)
- `KO1_kids_outer_points/` (origin a8c30d93c3, b64341eb9f, 66df609b0c, 9813a4adfb)
- `KO1R_kids_outer_regrade/` (origin 990bfd5450, 859e3f99fe)
- `SNP1_snowplow_clearing/` (origin 25b134be31, 8466e3da4a, 93e2340522)
- `KO3F_spec_veto_power_forecast/` (a forecast, not a lane: no criteria, no label; origin a0b26945fa)
- `ONE1_counted_once/` (pre-freeze note origin 8f6dca9ec1; lane origin 64b5bb5336, daac8502e2, 65311c51d9, 888e2d2c3d,
  467e94427b, 34259ac803, 6536ef5cdf; re-run by the lead: the KiDS script's label and every graded number reproduce, with
  only timing lines and one status flag differing; `ONE1.lean` recompiles with exit 0, 10 theorems, and its twin fails)
- `HE1_held_out_envelope/` (origin 91d343f150, ab52b18eda, d6c99b61de, 5137d5e374; re-run by the lead: both labels and
  every number in `he1.json` reproduce, only timing lines differ)
- `FB1_form_b_from_the_action/` (a note with one check; origin 2ddd61d529, bae0096600)
- `TPA1_two_phase_action/` (origin cdb9419a00, 347967f64f, 061f52e737; re-run by the lead: the three main scripts
  reproduce with only timing and memory lines differing, `TPA1.lean` recompiles with exit 0, 14 theorems, standard axioms,
  and its twin fails with 6 errors)

- `SCS1_static_clock_coupled_stability/` (origin c9355f4d9d, c88d6cc8dc, b3b863cb75, c54811ca3f, 0bacbb61f5,
  c025eee599; re-run by the lead: route 1, the covariant WKB script, reproduces with only timing lines differing, and
  `SCS1.lean` recompiles with exit 0, 13 theorems, twin failing; route 2, the radial solve, re-run in about an hour:
  every label identical and every eigenvalue equal to better than one part in a million; the stiffness output identical)

- `SCS2_static_clock_stability_discs/` (origin 7cf3530715, 448daec699, 7d303c169b, d323cc7025, 152fb45c7a, 55e47026a4,
  72f6198ede; checked by the lead: all 88 backgrounds re-solved from scratch and the maps reproduce exactly apart from
  timing and memory entries, with zero negative cells in the 40 isolated ones; the labels re-derived from the outputs
  are the same; `SCS2.lean` recompiles with exit 0, 13 theorems, twin failing. The two stability routes themselves, about
  an hour and up to 3 GB, were not re-run by the lead)

- `MK1_one_dust_constant/` (origin 11f43f9490, b076803437, 204ef24ac1, 21a9e0ca67; checked by the lead: the rows script
  re-run gives an identical file, the label re-derived from the outputs is NO VALUE on both footings, `MK1.lean`
  recompiles with exit 0, 14 theorems, twin failing; the SPARC and KiDS rows, about 5 and 20 minutes, were not re-run.
  Its Lean files sit in `fable_independent_2026/lean_2026/`)
- `COL1_clock_collapse/` (origin d56a3a2b78, 89f3fdc101, 5dbbab085c, b9c96ff3ca, 918545cf2b, dd69892991; checked by the
  lead: the label re-derived from the run outputs is BREAKS DOWN in every row, `COL1.lean` recompiles with exit 0, 13
  theorems, twin failing; the evolution runs themselves were not re-run)
- `DT1_dust_term_design/` (a design note, not a lane, hand-level: what any dust term must do and an exponential
  candidate; origin 136f7cc8c2; graded by MK2: NO VALUE, with three of the note's statements corrected. `ACTION.md` there writes out one full candidate action: action (A)
  with the exponential dust term, the constant Lambda replaced by a field chi, and a0 = kappa sqrt(G V(chi)). It is a
  candidate only: no gate passed, equations by hand)

- `MK2_exponential_dust_term/` (origin 3f889227f0, 4f672f239e, 904ca798c6, 8c7d3f711b, e138a4b122, 6bbfd8697b,
  4b44bc62b1; checked by the lead: the result file is complete and on origin, `MK2.lean` (in the Lean folder) recompiles
  with exit 0, 10 theorems, twin failing; no row was re-run)
- `FLD1_fold_reach/` (origin bce6d61451) and `REL1_relative_acceleration/` (origin 6db345c60e): result files read by
  the lead, not re-run
- `SHAPE_search/` (origin aaab11ddf2): notes from four read-only attempts to derive the law's shape for the cold
  component. None is a derivation; none is a lane
- `KDE1_clock_is_dark_energy/` (origin edfb117414, c26db8802f, 3480d33e9a) and `GRW1_late_growth_baryons_and_law/`
  (origin 660b4a1171, 40adf2ef0e, 27173fe895, b54941f573): the lead's own two lanes; result files read by the lead, not
  re-run
- `DD1_deduce_from_data/` (origin 91c159b746, ids 45a9fafdc2) and `HIS1_history_reading/` (origin c4f8cd2bb3, ids
  353bc1852e): result files read by the lead, not re-run
- `HIS1R_history_regrade/` (origin fefd1d3437, 882d9fa389, 88d306d2b1): regrade of HIS1 with separate code; same label
  on both footings, AGREES WITH DIFFERENCES THAT DO NOT MOVE A LABEL; not fully blind (disclosed)
- `DCN1_disc_centre_null/` (run from another session; header read by the lead, not re-run): ARTEFACT / ARTEFACT only
  under the last of six post hoc readings; NO VERDICT under every reading frozen before the outcome was seen
- `EQ1_cold_dark_energy_equations/EQUATIONS.md`: a reference sheet, not a lane. Every equation the record has for the
  cold component under form B, each tagged certified, hand-checked or measured, and a table of what the equations do
  not give
- `SCS3_external_field_stability/` (run from another session; origin criteria d97f24e76a, result e6a6dc2cf2, ids
  c06145c6ad; result file's header read by the lead, not re-run): NO VERDICT / NO VERDICT on every family and reading
  (a known answer fails as frozen; under its last amendment 11 of 32 axial backgrounds do not converge). Its own summary:
  the law's halo density is negative and growth appears on every grid with an external field, a slow instability of the
  outer halo (e-folding 0.74 to 2.0 Gyr at 0.1 a0, 22 to 61 Gyr at 0.01 a0); one thick-disc background reads RATE
  UNBOUNDED at the disc-centre null. All four of its amendments are post hoc
- `SHP1_cold_component_shape/` (origin 0ec459706c, 5f5b23f92a, cb73805783; a measurement lane run from another session;
  result file read by the lead, not re-run): THE LAW'S SHAPE ON ROTATION CURVES, LENSING ABOVE; NOT ONE SHAPE. Everything
  that is not baryons follows X(x) = (sqrt(1 + 4x^2) - 1)/2 on SPARC within 0.057 / 0.021 dex in every bin; KiDS's
  published isolated lenses sit 1.40 / 1.28 times the law (below it if B21's hot gas is counted as baryons); KiDS's
  lowest-mass bin sits apart. Its `THEORY.md` is a note, not a result

Lean: the Mathlib build these files were first compiled with (in a copy of the repository) was removed from the machine
on the evening of 2026-11-09. A build has been inside the repository's own `fable_independent_2026/lean_2026` since
22:17 the same evening. The ONE1 session made it by unpacking the machine's own Mathlib cache; nothing was downloaded.
The lead re-compiled `KO1.lean` (exit 0, 12 theorems) and its twin (exit 1) with it. With TPA1's 14, ONE1's 10, SCS1's 13
and SCS2's 13 and COL1's 13 the Lean files here hold 155 theorems; MK1's 14 are in the Lean folder itself.

Each folder has FROZEN_CRITERIA.md, any amendments, the scripts with their outputs and MUTATE outputs, RESULT.md, and (except
GAL1 and KO1R) a Lean file with its compile output and a mutate twin.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
