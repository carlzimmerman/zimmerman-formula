# A2 audit: the medium and the joint (HY4 preview batch, 2026-11-11/12)

Independent auditor. Re-ran every lane script I could in a temporary sibling folder (one thread, `nice -n 19`),
compared it with the committed outputs, then deleted the copy. Checked each derived, identified or closed claim
myself with sympy. Lean files were not compiled. Footings were kept separate.

## Table

| lane | label claimed | order ok? | re-run reproduces? | grade | reason |
|---|---|---|---|---|---|
| FINAL-1 THEORY_ASSEMBLY | THEORY WRITTEN / same | **NO**: criteria, script and outputs land together in c5d897706f (a FINAL4-titled sweep). RESULT's "committed alone" is not supported by git | YES, main + mutate byte-identical | OVERSTATED | Numbers sound. But the Sigma_f "assembly rule" is called an initial condition. It is not: it constrains a hypersurface in mid-evolution (see below) |
| FINAL-7 what_it_is | NO MEDIUM, CLOSED AT (ii) / same | YES: criteria 6d3324113e comes before the script in 01b3baca9e | **NO**: fin7.py was deleted in f639380e36. The last committed version reproduces M1-M3 and M5 but not fin7.out or M4. Committed DB1(i) reads PASSES; the script on record gives FAILS, and Arm N also differs | SOUND WITH LIMITS | NO MEDIUM follows from M5 plus the tension fact. K3's "no conserved cold rest mass" rests on the 5.41 cap, which was withdrawn 11-12. The final outputs cannot be traced to any committed code |
| FINAL7F formation reading | NOT A FUNCTION OF ANY TESTED VARIABLE (history-like) / same | YES: aa235e9fb2 holds the criteria alone | YES: json identical apart from runtime | OVERSTATED | The frozen rule gives NO STRUCTURE. Post hoc A1 raises it to "history-like". A null across 16 class medians has little power and is not a signature |
| ELA1 elastic_medium | ELASTIC SOLID FAILS AT S0 (+S2, B1) / same | YES: criteria f140ffc0cf alone, then A1 alone (post hoc, disclosed), then the script | YES: main + 5 arms identical | SOUND | I confirm sigma = -Pi myself: div sigma/(rho_c g) = 1 exactly in the deep field. The lane keeps M5's hypotheses and fails, consistent with M5 |
| OUT5 bootstrap_carrier | BOOTSTRAP KILLED (FRW/HALO + PAYMENT) / same | **NO**: criteria, out5_sym.py and outputs land together in 41307730e1 | YES: sym/num/grade, main + 5 arms identical | SOUND WITH LIMITS | It "evades T4/LFS1" by dropping charge conservation: a new pinned scalar with no kinetic term. That drop is then tested (payment, mu_K) and the carrier dies. G1 identity confirmed, residual 0. Its Lean "flat direction" claim is already withdrawn by the record |
| OUT3 scale_free_boundary | NOT DERIVED (FITTED) | **NO**: PREREGISTER, script and outputs land together in 41307730e1. A1 post hoc | YES: main + mutate identical | SOUND WITH LIMITS | kappa stays FITTED. Its ontology sentence ("in vacuum it is the cold dark energy, w = -1") contradicts form B, where the component is dust on FRW at 5.41 x baryons |
| CLOSE-1 DT2 | FOLDS / FOLDS | **NO**: criteria land with dt2_static/linear scripts and outputs in 0e2b0a5489 | PARTLY: static identical; linear identical except two band-edge n' values. reach/run not re-run (> 2 min) | SOUND WITH LIMITS | The FOLDS kill matches COL1/FLD1. K1 PASS and R_set(0) = 0 are already withdrawn by the 11-12 correction (corrected K1 = 0.4908, FAIL) |
| FINAL5 measurement | the decisive observation is runnable on archival data | YES: criteria 6d3324113e before the script f7674e4d03 | YES: committed main + mutate identical (working tree now holds an uncommitted wrapper) | OVERSTATED | See the FINAL5 section below |
| FINAL-15 formation | 14/16 (can.), 13/16 (alt) band hits, p 0.005 | YES: 639e7f3b12 holds the criteria alone | YES: main + mutate identical (a trailer line was added by hand) | OVERSTATED | Not blind (its own honesty flag says so). Channel and F_b were chosen per class after the residuals were printed, so the shuffle p tests nothing. It scores KiDS as "settled", yet FLD1 puts KiDS's windows 1.3-2.3x beyond the fold, where Sigma_f does not exist |
| CLOSE-2 par1_branch_union | NO VERDICT as frozen; CLOSED (member sense) under post hoc amendments | YES: criteria b8acc6c3bc alone, A1 one minute later, result after | YES, except R8's repo-scan count (18 to 21, because the record grew) | SOUND WITH LIMITS | Honest. "Closed" holds only under post hoc amendments, and only in the member sense, not as a class theorem |
| CRUX / CLOSURE / EXITS / ANALYSIS / README | notes (no label) | n/a (CRUX, CLOSURE, EXITS, ANALYSIS were swept into c5d897706f) | crux Kill 1 CONFIRMED | OVERSTATED | "The charge does not exist" relies on a universal 5.41 cap, withdrawn 11-12 (Mc/Mb = 5.41 Fc/Fb needs equal retention). Only CRUX and CLOSURE carry the correction; EXITS, ANALYSIS and README do not. README's lane table is stale ("running") |

## Hits checked myself

- **Law's stress (CONFIRMED).** With J = (a0^2/K)(u - ln(1+u)), Pi_rr = J - g^2/(K(1+u)) gives
  d(Pi_rr)/du = -u/(1+u)^2 < 0. So the stress is tension along the field at every field strength. In the deep
  field: (Pi_rr + Pi_tt)/Pi_tt = 2u/3 + O(u^2), Pi_rr/rho_c = -v_inf^2/2, and div(-Pi)/(rho_c g) = 1 exactly.
  CRUX Kill 1 holds: the Tolman correction is about sigma_t^2/c^2, roughly 1e-7, so the stress cannot pay the
  lensing.
- **ELA1 and FINAL-7 do not escape M5.** Both keep all three hypotheses (local, momentum-conserving, normally
  self-gravitating), and both fail, which is consistent with M5. FINAL-7's "surviving carrier" (P2, the sourced
  field) is not a medium. It is the record's existing reading: the halo is field stress whose polarization charge
  nets to zero, as in SMF1's Gauss result. Nothing in this batch contradicts M5, SMF1 Gauss or the tension
  theorem.
- **OUT5 drops one hypothesis: conservation of the carrier.** It adds a non-dynamical scalar pinned to a function
  of rho_b, g and grad g. G1 (the identity rho_c = [(1-mu)/mu] rho_b + mu' g d_s g/(4 pi G mu)) is CONFIRMED,
  residual 0. But that identity is only the law rewritten. The dropped hypothesis was tested (the payment gate)
  and it kills the carrier.
- **FINAL-1 and FINAL-15, the "assembly rule" on Sigma_f: NOT CONFIRMED as an initial condition.** The rule
  pins X_f = X_L(g_b,f) through a delta(Sigma_f) multiplier term. The lane's own cited current obeys
  nabla_m J^m = 0, so the charge on Sigma_f is already fixed by earlier evolution. The rule therefore does one
  of two things:
  - (a) It restates the joint as an assumption. COL1 and FLD1 say the dynamics do not deliver this value.
  - (b) It acts as a localized source that violates the conservation the lane cites. That is EXITS' exit 4
    (VCC1), and no lane tests it in this form.

  Either way the formation reading moves the joint into a boundary condition. It does not find the joint.
  FINAL-1 says plainly that it does not derive the joint, but "not a bulk term: an initial condition" hides
  this.
- **FINAL-7 K3: OVERSTATED.** It infers "no conserved cold rest mass" from the KiDS demand exceeding the 5.41
  budget. Action (A) has a conserved current (QX17 E3), and the universal cap is withdrawn.

## FINAL5

- **Proposal:** stack the ACT DR6.02 NILC Compton-y map on 17,335 KiDS host-free isolated L* lenses, using
  GO1's Part A pipeline. The target is the flat gas column Sigma_gas = a0/(pi G x_b^2) = 6.16 / 7.45 Msun/pc^2
  out to 2.6 Mpc.
- **On disk:** only a Compton-y *strip* (`strip_ComptonY.f32be`, 830 MB) plus headers and the blackbody T map
  are on disk. Whether the strip covers the KiDS lenses was not checked. The 17,335 count is quoted, not
  reproduced (the lane's own KA6 says NOT VERIFIED).
- **Detectability:** the "~100 sigma, no outcome in between" claim is superseded by the record's 11-12
  correction (projection, beam, flux units).
- **Decisive? No, and not for the joint.** It tests only the hot-gas reconciliation of the amount. GAS1's G4
  already kills that reading on the galaxy leg (with the gas in g_bar the outer points fall to 0.03-0.04 of the
  law), and FINAL5 §4 itself says both gas shapes are already excluded by data on disk.
  - A null result repeats a closed verdict.
  - A detection would break form B's own KiDS fit.
  - Gas cooler than ~0.1 keV evades y, and the proposal brackets only 0.1-0.5 keV.

  So neither outcome would tell us what the joint or the medium is.

## Hygiene

- **Absolute home paths in committed files:** FINAL5 FROZEN_CRITERIA.md, PROPOSAL.md and RESULT.md;
  CLOSE-1 DT2.out, DT2_MUTATE.out and dt2_linear.out; FINAL7F final7f.out and final7f.py; FINAL-15 compile.txt
  and compile_MUTATE.txt; CLOSE-2 close2_grade.py.
- **"cold dark matter" / "CDM-like":** no use found for the theory's component.
- **Data said to favour the framework:** none found. FINAL-1 says "His data prefer the formation reading". That
  is a reading-versus-reading comparison and names a person; it should be rephrased.

## Plain answers

- **Did this batch find the joint?** No. Every lane that touches it either fails (DT2 FOLDS, OUT5 KILLED,
  CLOSE-2 member failures) or moves it into a pinned boundary condition (FINAL-1, FINAL-15).
- **Did it identify the medium?** No. Its strongest and correct result is negative: no local medium carries the
  law. ELA1's solid fails, and FINAL-7 restates M5 together with the tension theorem (the stress is tension
  along the field, so the halo is field stress, not substance).
- **What is new and holds up?**
  - ELA1: an isotropic solid carrying the law has real, subluminal sound speeds and cures M5's S4 shear
    ill-posedness, but it fails on strain, energy and the Bullet.
  - OUT5: an exact local rewrite of the law as a pinned density, closed by its cost.
  - The CRUX Kill 1 arithmetic: the stress cannot pay the lensing.
  - CLOSE-2's honest union bookkeeping.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
