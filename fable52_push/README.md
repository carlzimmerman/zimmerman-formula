# fable52_push: one swing at completion (2026-11-09)

Adopts nothing. kappa = 1/2 FITTED; not theory closed. Nothing here is registered in the closure record.
Paper: PAPER71 v1.0, deposited 2026-11-09, DOI 10.5281/zenodo.24094860
(`qwen_claude_field_theory/papers_2026/PAPER71_switch_theorems_kids_outer_points_2026.pdf`; the deposit's supplement zip holds
this folder at c6689541ee).

## Answer first

**No completion.** I could not build a theory that passes every gate, and I do not think one exists inside the gates as
they are frozen.

**What this folder does close: one whole class of completion.** Every switch on the law that comes from an action (the
"two-phase" reading: law inside cleared regions around galaxies, cold component elsewhere) now has a failing verdict on
each of its exits. Six lanes carry it: SWT1 (theorems), EMV1 and GAL1 (the lensing allowance, checked twice), KO1 with its
blind regrade KO1R (KiDS's outer points), and SNP1 (clearing dynamics). The Lean files hold 72 theorems, standard axioms
only, each file with a twin of false statements that fails.

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

## 2. The lanes

| Lane | Question | Label (canonical / alt) |
|---|---|---|
| SWT1 | exact statements for any action-based switch | CP KEY-DEPENDENT; WP NOT A NO-GO AS FROZEN |
| EMV1 | does the filling statistic survive a direct nonlinear solve with an external field? | T2 HOLDS / T2 HOLDS |
| GAL1 | what do growth and CMB lensing allow for the filling history? | ALLOWANCE CONFIRMED / ALLOWANCE CONFIRMED (0.0197; 0.0134 if on from z 6) |
| KO1 | are KiDS's outer points the lens's own field? | LAW LEVEL HOLDS / LAW LEVEL HOLDS by the frozen gate |
| KO1R | blind regrade of KO1 from its criteria alone | NOT SEPARATED / LAW LEVEL HOLDS (518 tied lenses; knife edge) |
| SNP1 | can the wall pressure clear the component and keep it out? | FAILS / FAILS |

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
   late types first.
3. **The baryon census in groups.** Unchanged from the first version of this file.

## 6. Corrections (mine and the record's)

- My first report said the wall pressure would rule out the "galaxies repel the component" family. It does not: the wall
  wins against the record's share by 3 to 20 times. It fails for other reasons (it cannot carry what KiDS needs).
- The first version of this file bet that the outer galaxy leg gives way, meaning that KiDS's outer points would turn
  out to be neighbours' mass. KO1 does not support that bet.
- My hand estimate for SNP1 (walls swept beyond KiDS's range, filling too large) was the reverse of what the runs show.
- WL1's FAIL stands, but its "any key" scope sentence does not hold for a compensated switch. SQ1 graded the opposite sign
  to the law's own term.

## Files

- `SWT1_switch_theorems/` (origin c892bac851, 6997214890, cbf83986f3)
- `EMV1_effective_medium_validation/` (origin eeb830ace2, 0e3c23f7d5)
- `GAL1_growth_lensing_allowance/` (origin f7b534d9e4, c8c6935efc, 5d9fa6d888)
- `KO1_kids_outer_points/` (origin a8c30d93c3, b64341eb9f, 66df609b0c, 9813a4adfb)
- `KO1R_kids_outer_regrade/` (origin 990bfd5450, 859e3f99fe)
- `SNP1_snowplow_clearing/` (origin 25b134be31, 8466e3da4a, 93e2340522)

Each folder has FROZEN_CRITERIA.md, any amendments, the scripts with their outputs and MUTATE outputs, RESULT.md, and (except
GAL1 and KO1R) a Lean file with its compile output and a mutate twin.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
