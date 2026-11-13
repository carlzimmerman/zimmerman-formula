# Closure statement for the fable52 push (2026-11-10)

> **Corrections, 2026-11-12:** this historical closure map predates the corrected
> quadratic variation and retention audit. Read [PIK1's correction](PIK1_pi_gated_dust/CORRECTION_2026_11_12.md)
> and [FRM1's correction](FRM1_formation_theory/CORRECTION_2026_11_12.md).
> The density gate has no established universal NO VALUE verdict, and FRM1's
> channel ceiling does not bound all conserved formation/transport histories.
> These corrections establish neither a working carrier nor theory closure.

Adopts nothing. kappa = 1/2 FITTED; not theory closed. Not registered. This file states where the push ends. Every line
points at a lane; the lanes' RESULT.md files are the record, and where this file and a lane differ the lane is right.

## In one paragraph

The owner's chosen form (form B: the a0 law with cold dark energy counted once) is real inside the adopted action: the
law's halo is the clock sector's own gravitating density, on one conserved charge, in force balance, and linearly
stable. **The action as written cannot be completed.** Its two regimes, the free-falling clock (dust, the CMB) and the
static clock (the law, galaxies), do not join: not in space, not with one constant, not in time. What is missing is one
thing, and it is not in the action: what the clock does when it folds.

## What is closed, with the lane that closes it

| Statement | Verdict | Lanes |
|---|---|---|
| Keep the cold component out of galaxies by any action-based switch | closed on every exit | SWT1, EMV1, GAL1, KO1, KO1R, SNP1, HE1 |
| Hold the galaxy's share outside a wall, statically | FAILS / FAILS | HE1 |
| The two-phase action is a consistent set of equations | yes; its health flaw was a planar artefact | TPA1, SCS1 |
| One dust constant for the CMB, clusters and galaxies (quadratic term) | NO VALUE / NO VALUE | MK1 |
| A clock that starts as dust settles into the law's halo | BREAKS DOWN / BREAKS DOWN (a fold at the centre in 0.06 to 0.15 Gyr) | COL1 |

## What stands

| Statement | Verdict | Lanes |
|---|---|---|
| In the action the law's halo is real, gravitating and conserved | certified | QX17; FB1 note |
| The static state holds the law's shape (force balance) | checked in any geometry | FB1 note |
| The static state is stable with gravity coupled | STABLE around point masses and isolated discs | SCS1, SCS2 |
| Form B on host-free KiDS lenses | PASSES at the widest veto; so does the law with no end | ONE1 |
| Form B on groups, clusters, the Bullet | not falsified (one-sided), never a pass | RB1 (another session) |

## What fails or has no verdict under form B

- Hosted dwarfs: the Milky Way's ultra-faints and M31's bright dwarfs sit high (RB2, another session).
- A disc in an external field: reads slowly unstable in places; NO VERDICT (SCS2).
- Lensing by galaxy type: NO VERDICT (KO2, another session).

## The one missing ingredient

Three independent lanes fail at the same joint.

1. **In space.** A wall between a law region and a dust region cannot be held (the switch class; HE1).
2. **In the constant.** The clock offset is about 1e-6 both in the expanding background at z 3400 and in a galaxy well
   today. The dust term must be stiff in the first and inert in the second, so it cannot depend on the offset alone
   (MK1). The same argument rules out any other one-variable dust term, including the exponential one in the DT1 note
   (being graded as MK2).
3. **In time.** With the law on, the clock falls onto baryons like test particles, nothing removes its infall energy,
   and it folds. The equations give no answer after the fold (COL1; X14 said the same from a different side).

So a completion has to say what the clock is behind a fold. The static state is the only state in which the action
holds the law, it is stable once reached, and the action offers no way to reach it. Any completion must do two things at
once: make the clock static behind the fold, and make the dust inert there.

## What would test a completion before anyone writes one

- **Does the folded region cover where the law is seen?** COL1's shells first cross outside 10 kpc at z 4 to 6 and
  outside 100 kpc at z 2.3 to 2.8. If a completion puts the law behind the fold, the law's reach at each epoch is the
  fold's reach. That is a necessary condition and can be graded now against KiDS and against rotation curves at high
  redshift (lane FLD1, queued).
- **The amount.** Only about one baryon mass of clock charge turns around by z 0, 1 to 4 % of the law's halo (COL1's
  diagnostic, no label). A completion in which the halo is advected dust is short by 25 to 100. One in which the halo is
  the polarization of a static clock needs no advected dust; whether the action's leafwise flux can supply it has not
  been computed.

## Added the same day: both tests ran, and the nearest repair failed

- **FLD1** (`FLD1_fold_reach/RESULT.md`, origin bce6d61451): DOES NOT / DOES NOT. The folded region covers every SPARC
  last radius (175 of 175) and every high-redshift rotation curve on disk (100 of 100), and stops 1.3 to 2.3 times short
  of KiDS's inner window and 3.1 to 5.4 times short of its middle window; form B's own cap lies 1.1 to 4.2 times beyond
  it. So a completion that puts the law only behind the fold cannot give the law where lensing sees it. FLD1 also says
  COL1's side numbers on the charge that arrives (the "1 to 4 %" quoted above) came from a wall-reflection artefact;
  read FLD1 for the corrected ones. COL1's label does not rest on them.
- **REL1** (`REL1_relative_acceleration/RESULT.md`, origin 6db345c60e): NOT WELL-DEFINED on both footings. Letting the
  law respond to the clock's acceleration relative to the baryons puts the baryons' own acceleration inside a convex
  Lagrangian, which makes matter's equation of motion fourth order and unstable (e-folding about 10 minutes for a
  free-falling rock). Its argument is general: by the equivalence principle a free-falling clock can only carry a law
  through the baryons' acceleration. Its later steps were not graded.

- **MK2** (`MK2_exponential_dust_term/RESULT.md`, origin 6bbfd8697b): NO VALUE / NO VALUE (as frozen NO VALUE / NO
  VERDICT: one known answer failed on alt by 0.0026 and was fixed post hoc). The exponential dust term of the DT1 note
  has no sound speed that passes all graded rows. Clusters and groups have none at all: above about 1000 km/s the dust
  does not pool and X-COP stays +0.45 / +0.42 dex short; below it each cluster's static state stops existing, with the
  dust at 24 to 79 % of the baryons at its last state. What the term does do: above about 300 km/s it leaves SPARC,
  KiDS and the Solar System untouched, and above about 500 km/s the clock around a galaxy is static out to form B's
  cap (a static and timescale argument, not an evolution run), so COL1's and FLD1's failures do not apply to it there.
  It cannot carry CMB lensing, growth or the forest. MK2 also corrects three statements in the DT1 note; the note
  carries the corrections.

So the statement above tightens: in this family of actions the law exists only where the clock is static, the clock is
not static where lensing sees the law, and the one change that would lift that requirement is not a consistent theory.
Neither lane's long runs were re-run by the lead; the labels are quoted from their RESULT.md files.

## Added 2026-11-10 night: four derivation attempts and the lead's two own lanes

- **SHAPE_search** (notes, origin aaab11ddf2): four independent attempts to derive why the cold component's pull is
  a0 g / (g + a0). None is a derivation and none fixes kappa. One statement worth keeping: for one conserved scalar
  medium coupled by gravity only, the unique Lagrangian that gives the law is the Newtonian limit of action (A).
- **KDE1** (`KDE1_clock_is_dark_energy/RESULT.md`, origin c26db8802f): ALREADY IN THE RECORD AS AC2s on both footings.
  Making the law's clock a stiff dark-energy field was the record's AC2 family of 2026-11-05. The record also answers
  the hope behind it: such a clock does not stay cosmological around a galaxy. The law's term gives it an inertia that
  swamps its stiffness below the Hubble scale, so it falls in with the baryons and folds at the same time as the
  dust-carrying clock (the record's AC10). The lead's premise for the lane was wrong.
- **GRW1** (`GRW1_late_growth_baryons_and_law/RESULT.md`, origin b54941f573): baryons under the law do not build late
  structure when the cold component is warm. Under the action's own linear theory every graded line falls short at
  every sound speed in MK2's band (S8 at 0.59 of the required value, the forest at 1e-4), and a bound on that treatment
  is still short. With the static law and the total field as external field, large scales overshoot by about 300 in
  CMB-lensing amplitude and the forest is still short. As frozen the lane is NO VERDICT, because two of its
  known-answer checks were written wrong and were fixed post hoc; the labels are under that amendment.

Together with DT1's trade-off (a dust term that keeps galaxies empty is warm at late times) GRW1 closes the family of
completions with a warm cold component: galaxies stay clean, and nothing then builds late structure. Neither lane was
re-run by the lead; the labels are quoted from their RESULT.md files.

## Added 2026-11-10 late: three lanes from another session, one of which corrects a line above

Quoted from their RESULT.md headers; that session re-ran each; the lead did not.

- **LFS1** (`closure_2026_11_10/LFS1_leafwise_flux_supply/RESULT.md`, origin 0168c8c040): ILL-POSED on both footings.
  **It answers, with no, the question this file left open under "The amount"** ("whether the action's leafwise flux
  can supply it has not been computed"). In action (A) the leafwise flux is the normal equation's own bookkeeping and
  adds no charge: the polarization flux through a sphere is carried with the clock's flow, and for a static clock it is
  frozen. The halo's charge changes only by a fraction of order |Phi| / c^2, about 1e-6; everything else it holds is
  charge the clock carried in. So a static halo cannot grow, and the reading in which the halo is polarization that
  needs no advected dust is closed.
- **CLS1** (`closure_2026_11_10/CLS1_cluster_state_in_action/RESULT.md`, origin 0dba08ca7f): at form B's own mu_K (at
  least 198 per Mpc) NO STATE / NO STATE, proven on all seven X-COP clusters: the clock's own pressure is too weak by a
  factor of 396 to 2,192. As frozen the label is STATE EXISTS-PARTIAL, which the lane says means only that a window in
  mu_K is not excluded; no state was built in it.
- **DCN1** (`DCN1_disc_centre_null/RESULT.md`): SCS3's unbounded rate at a disc-centre null reads ARTEFACT only under
  the last of six post hoc readings, two of them written after the outcome was seen; every earlier reading is NO
  VERDICT. So that item has no verdict.

## Added 2026-11-10 night: asking the data directly

- **DD1** (`DD1_deduce_from_data/RESULT.md`, origin 91c159b746): NO RULE AMONG THE CANDIDATES on both footings. One
  frozen table of 16 classes and 626 systems, the statistic X = g_obs / g_bar - 1, candidate variables fixed before any
  fit, held-out and leave-one-class-out scoring, no theory assumed. No candidate holds even the two half-splits; every
  candidate that covers all classes fails at least 11 of them; six classes fail every candidate. Under the law itself
  SPARC passes (offsets 0.00 to +0.02 dex), KiDS is within its errors, groups sit +0.16 high, X-COP and CLASH clusters
  +0.5 to +0.6 at 15 to 24 standard errors, the Milky Way's ultra-faints +0.5 to +0.6, and tidal dwarfs and DF2 / DF4
  0.6 to 0.9 low. The best candidate, a function of g_bar and the system's depth, has held-out scatter 0.219 dex and
  still fails 12 classes. The conservation reading (a fixed total at the last measured point) is the worst. Not re-run
  by the lead; no blind regrade.

So the data, asked without a theory, return the law for rotation curves and no single rule beyond them. The classes that
break every rule break it in both directions.

- **HIS1** (`HIS1_history_reading/RESULT.md`, origin c4f8cd2bb3): on DD1's frozen table, the reading "the non-baryonic
  mass is real and conserved, its amount set by the law when a system formed" HOLDS EXCEPT H3 (fails), H5 (no power),
  on both footings. Four of its five frozen statements are met: the tidal dwarfs sit at Newton (0.6 standard errors
  from none, 6 below the law); no system of 626 reads below zero non-baryonic mass beyond its errors; X-COP's edge
  holds 4.94 [4.30, 6.11] against 5.41 with groups on the other side; hosted and gas-poor classes sit at or above the
  law. It fails on one class: the isolated faint gas-rich rotators sit about 0.3 dex below the law (3.5 / 3.9 standard
  errors; 2.3 / 2.7 if every distance were 20 % smaller). Inside a class nothing tracks a measured sign of history
  (no power). **The reading "the law is a force that every system obeys now" scores 1 of 5 on the same tests.** One
  mutation arm did not bite as frozen (disclosed); the early types' hold rests on a Chabrier-like mass-to-light ratio.
  Not re-run by the lead. It tests consistency with a history, not a mechanism.
- **HIS1R** (`HIS1R_history_regrade/`, origin fefd1d3437, 882d9fa389, 88d306d2b1): a regrade from the frozen criteria
  and the frozen table with its own code, label committed before HIS1's result was opened. Same label on both footings;
  all five test outcomes and the force score agree; 145 of 148 compared numbers agree to 5e-12; the three that differ
  (one standard error and one control count) move no label. It discloses that it was not fully blind: HIS1's commit
  subjects were in its session context from the start, so the agreement is of arithmetic from separate code, not an
  independent judgement.

## Added 2026-11-10 late night: a0 as a contact strength, tested and killed

- **NBC1** (`NBC1_neutral_baryon_contact/RESULT.md`, origin criteria 472bc26182, result 31a392831d): the lead's own
  hypothesis, worked through its kill tests on the owner's go. Reading a0 as an opacity G/a0 (7.13 / 5.90 cm^2/g)
  between cold dark energy and neutral gas is KILLED (K2 PROVISIONAL) on both footings. In the law's own halo
  rho_c r = a0 / (2 pi G sqrt(1 + 4 x^2)), so gas on a circular orbit gives its angular momentum to a non-rotating halo
  in 0.58 / k orbits at every radius inside r_M and for every baryon mass; the largest coupling that lets a gas disc
  live 50 orbits is 0.0115 G/a0. A halo that turns with the gas escapes that, and then settles into a layer of 65 to 85
  Msun/pc^2 at the Sun where the budget is 21 +- 5 (local inputs from memory). At recombination the neutral-only
  coupling is 0.2 to 0.7 of the expansion rate (not decided by hand) and above 1 at the largest value tried.
  The coincidence that started it (the law's column times G/a0 is 1/(2 pi)) is the law's own column restated.
  With MEDIUM_DESIGN's table and its section 3 (`closure_2026_11_10/`), every medium class the record can name now has
  a failing verdict; this lane closes the neutral-contact one. It is not a statement about a field-mediated force.

## Added 2026-11-10 late night: three parent-action lanes from other sessions

Quoted from each lane's own RESULT.md (headers read by the lead, not re-run by the lead; the sending session re-ran
PAR1 and SMF1). All three are under `closure_2026_11_10/`.

- **PAR1** (`PAR1_parent_action_spec/`, origin 6be0bf30d1): NO VERDICT / NO VERDICT as frozen and under both of its
  post hoc amendments, because two branches stay open and no member of them was graded there. Its answer: "No parent
  action built from one single-valued carrier exists" (branch B-Ts, EMPTY under its post hoc A1; with B0 and B-L that
  closes every parent whose cold dark energy is a single-valued field). Left open: a multi-valued (wave) carrier with
  the law keyed on the wave's own phase frame (wave mass 4.2e-24 to 1.84e-23 eV canonical, to 1.93e-23 alt), or with
  the law on a separate smooth frame.
- **WV1** (`WV1_wave_dust_split_charge/`, origin fb421c3adb, addendum 21350b497d): the separate uncoupled frame (V2)
  STRUCTURE FAILS / STRUCTURE FAILS as frozen. The frame as the wave's phase (V1) STRUCTURE FAILS only under its post
  hoc A1 + A2; as frozen it is NO VERDICT. Its plain words: "The split cannot be made in an action", because the law
  reads the frame's acceleration, so D.P enters the frame field's own current. Its log M_b 10.7 runs were paused and
  are not part of the result.
- **SMF1** (`SMF1_smooth_frame_parent/`, origin 884ddfb854, post hoc A1 result 92a0855574): PAR1's smooth-frame branch,
  written as a full action, STRUCTURE FAILS / STRUCTURE FAILS at its first part S0. By Gauss, the frame's polarization
  charge is zero in any region whose boundary lies where the frame free-falls, for every exchange rate; and where the
  halo is counted once the exchange source is zero. Neither gate is wave-specific (post hoc A1), so a collisionless
  carrier in the same structure fails the same way. Not graded there: "a re-specified branch, with the halo as the
  image of a held edge layer of real cold charge"; its member has nothing that can hold such a layer.

So the two branches PAR1 left open each have a failing member, one of them only under post hoc readings. The one
re-specified branch SMF1 names is ungraded.

## What is not claimed

No completion exists. No lane here says the data favour the framework. The exponential dust term is a hand-level
candidate that has passed no gate. The final paper (PAPER72) is written by another session and is not deposited.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
