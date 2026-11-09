# fable52_push: one swing at completion (2026-11-09)

Adopts nothing. kappa = 1/2 FITTED; not theory closed. Nothing here is registered or folded into PAPER70.

## Answer first

**No completion.** I could not build a theory that passes every gate, and I do not think one exists inside the gates as they are
frozen. I worked the galaxy / cluster / CMB triangle from every direction I could find (single counting, two-phase media,
dipolar-type media, velocity barriers, entropy floors, sign-flipped couplings). Each one landed on a lane already graded.

What this swing does add is one lane, **SWT1**, with three exact results about every switch on the law that comes from an action.
They are certified in Lean (19 theorems, standard axioms only). They correct one statistic in the record, remove one general
reading, and reduce the whole switch class to a single conflict with numbers on it.

## 1. Why it does not close

1. The CMB needs a cold, clustering component of about 5.4 times the baryons (F1; F1A and CMB3 confirm it).
2. Galaxies exist early, so that component had small-scale power and collapsed with them (WM1 A2: the law amplifies seeds, it
   cannot make them).
3. It is conserved (SS3; the BAO + SN and S8 rows). So today it is around galaxies, or something removed it.
4. Removal has a verdict on every route: kicks (CK1), heating (CE2, KX1), conversion (SS1-SS4), switches. SWT1 adds the last
   candidate, the law's own field stress: right sign, right ordering, but only against a share that has not yet settled.
5. If it is still there, then either the law is not a second force on top of it (single counting: route E, retired on FG1; PD1
   and PD2 fail KiDS, the groups and the Bullet's amount), or it must be invisible to baryons where the law acts (BI1's class,
   failing its consistency gate today).

The frozen gates exclude both branches. A completion has to move a gate or bring physics from outside the catalog. That is the
record's own closing statement, reached again by a different road; I found no way round it.

## 2. What SWT1 adds (fable52_push/SWT1_switch_theorems, RESULT.md)

- **Compensation.** A spherical switched law shows exactly M_b outside the switch radius. WL1's stage-2 statistic counted the
  retained phantom as outside mass (0.94 / 1.08 against 0.0354). The correct large-scale statistic is the volume the law-on
  regions fill, with an allowance of **2.3 %**. WL1's graded reading still fails (0.30 / 0.36); its self-consistent reading
  passes (0.018). Label **KEY-DEPENDENT**: WL1's FAIL stands, its "any arm-(i) key" scope sentence does not.
- **Wall pressure.** The force per unit area any such switch puts on its carrier is exactly
  (a0^2 / 4 pi G) [u - ln(1 + u) - u^2 / (2 (1 + u)^2)], with u the law's field inside the wall. Around galaxies it exceeds the
  pressure of the record's cosmic share by 3-20x; in groups and clusters it falls short by 4-40x. Label **NOT A NO-GO AS
  FROZEN**. My own pre-freeze expectation was a no-go; it was wrong, and the amendment says so before any number.
- **The conflict that is left.** Keeping the law on over KiDS's full range needs a filling of 0.29. The allowance reaches 0.43 of
  that range, down to g_bar 7.5e-15 m/s^2. Bubbles sized by pressure balance against 35-52 km/s component sit right at the line
  (1.8-4.6 % filling), but the ones that pass it leave 16 of the 59 KiDS points outside the wall and cost about 200 in chi2.

## 3. The closest thing to a completion, scored

"Two-phase" reading: the cold component everywhere it has not been cleared, Newtonian there; the law only inside cleared regions
around galaxies, with its phantom compensated at the wall.

| Gate | Status | Source |
|---|---|---|
| CMB primary, forest, BAO + SN, f sigma8 | pass (the cold reference) | carried rows (PD1 P4) |
| CMB lensing | pass only if law-on regions fill <= 2.3 % | SWT1 T2 |
| SPARC, Cassini, Ursa Major | pass inside the wall (the law's rows) | carried |
| Ordering: galaxies cleared, groups and clusters not | pass, no constant added | SWT1 T3 (new) |
| KiDS, inner 43 % of the range | pass | SWT1 |
| **KiDS, outer three or four points per bin** | **fail** (about +200 in chi2 at the allowed filling) | SWT1 E3 |
| X-COP | pass with the full share and the law off (bracket) | PD1 A2 |
| **Groups** | **fail** 0 of 9 | PD1 A2 |
| **Bullet** | offset right, subcluster mass 2.6 sigma low | PD1 A2 |
| **Clearing dynamics** | **not shown**; a settled share leaves 0.7-2.0 M_b inside 200 kpc (line 0.9) | SQ1, SWT1 E2 |

Three rows fail and one is not shown. It is the best row I can assemble, and it is not a completion.

## 4. What decides it

1. **KiDS's points below g_bar 7.5e-15 m/s^2.** KiDS beyond a few hundred kpc is a failing gate in at least eight lanes of the
   last three days (PD1, PD2, SS1 H and I, SS4, WD1, PJ1, SQ1), and SWT1 shows the whole switch class turns on these points. Their per-point errors are 0.06-0.10 dex against a gate line of 0.05 dex. If that signal is the
   lens's own field, the law is a force out to 3 Mpc and no switch survives the CMB. If it is neighbours' mass, the two-phase
   reading passes both. A lane that grades those points against the data, with the measured gas and the isolation cut varied,
   would settle more than another mechanism. (My recollection is that the survey paper flags its isolated sample as less reliable
   beyond about 0.3 Mpc / h70; I have not re-read it, so treat that as unverified.)
2. **The baryon census in groups.** "Newton plus the cosmic share of the observed baryons" under-fills the groups and the Bullet's
   subcluster. Either those systems hold more baryons than are counted inside R500, or the share is not tied to the baryons.
3. **Whether a settled share can be cleared.** The energetics are marginal at a quarter of the turnaround radius. A shell
   integration with the wall force acting at the wall (not through a local density screen, as in SQ1) would decide it.

If I had to bet on which leg gives way, it is the outer galaxy leg, not the CMB and not the clusters.

## 5. What I would stop doing

Grading further switch variants one at a time. Every variational switch is compensated, its reaction is bounded by the closed
form above, and its fate is set by item 1.

## Files

- SWT1_switch_theorems/: FROZEN_CRITERIA.md (4d86f4d107; origin c892bac851), AMENDMENT_A1.md (4af87eb9c0; origin 6997214890),
  RESULT.md (origin cbf83986f3), swt1.py and outputs,
  swt1_extra.py and outputs (reported only), SWT1.lean, SWT1_MUTATE.lean, compile.txt, compile_MUTATE.txt.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
