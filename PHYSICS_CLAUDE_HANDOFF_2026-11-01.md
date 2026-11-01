# Claude handoff: finite SU(5) matching, conditional photino, gravity/production

Owner request: commit and push the current work for Claude. This is a research
checkpoint, not a claim that the vacuum/gravity/production program is complete.
The owner interrupted TP05 to request this handoff. Do not continue another
numerical lane merely because an earlier roadmap lists it. The simulation
queue and unrelated active work were left untouched.

## Read in this order

1. [TP04 current result](reviews/radial_ir_cold_2026_11_01/README.md): actual
   radial dynamics, radiative gaugino masses, charge loss, and the conditional
   cold photino example. Its [handoff](reviews/radial_ir_cold_2026_11_01/HANDOFF.md)
   lists the remaining physical assumptions.
2. [TP05 contract](reviews/gravity_vacuum_production_2026_11_01/CONTRACT.md)
   and [gravity/DE dictionary](reviews/gravity_vacuum_production_2026_11_01/GRAVITY_LINK_DICTIONARY.md).
   This is the current unfinished program. Read the subroute status files
   saved alongside the derivations before interpreting any preliminary number.
3. [TP03](reviews/finite_matching_2026_11_01/README.md): all ten finite two-loop
   vacuum classes and the finite angular current, with heavy response once.
4. [TP02](reviews/quantum_matching_2026_11_01/README.md): full running/CS and
   actual matter couplings. [TP01](reviews/three_priorities_2026_11_01/README.md)
   contains spin/contraction, full tree spectrum and law/certificate correction.

## Established finite results

The canonical-K rigid model is

    W=fX+(h/2)X Tr A^2+(lambda/2)Tr A^2 B,
    A=i a diag(2,2,2,-3,-3), B=b diag(2,2,2,-3,-3),
    a^2=2fh/(30h^2+lambda^2), b=hX/lambda,
    T=sqrt(30h^2+lambda^2)X/lambda.

The full tree spectrum has 98 real scalars, 73 Weyl fermions and 24 vectors.
Use the actual canonical T, not a fictitious constant kinetic coefficient
for s=ln X. Couplings, scale and state remain physical inputs. kappa=1/2 is
fitted in the repository; no step here derives it or closes the V3 theory.

- All ten finite two-loop vacuum diagram classes are implemented and pass
  SUSY cancellation, basis/scaling and reduced CS checks. Scalar/vector
  derivative mixing is included in the finite phase current. Landau component
  anomalous dimensions differ from chiral-superfield ones; the heavy pullback
  closes that distinction in the reduced current identity.
- Finite radial matching and the known real/imaginary heavy derivative
  completion do not rescue the rotating phase. At X/Xmin=1.3 its spatial
  instability grows at about .33--.36 times omega. Coherent radial oscillations
  are a separate candidate with actual phase decay and Floquet production;
  a tiny spontaneous width is not a universal coherent-state lifetime.
- All 12 tree-massless unbroken gauginos get finite leading one-loop masses.
  The neutral residual-U(1) photino obeys

      m_chi=1.1164161506e-4 mu e^(5/2), mu=sqrt(f),
      e=h=lambda, g=sqrt(29/200)e.

  The residual photon is not identified with observed EM. The Goldstino and
  light gauge/phase sectors require the stated IR treatment. A rolling phase
  has a T=0 anomaly-driven photon-helicity instability; its growth exponent
  is not by itself a fractional charge lifetime.
- At the *conditional rigid* point e=.003, m_chi=1 MeV, mu=1.81707e7 GeV
  and v=2.44405e9 GeV, a named leading vacuum/NR loss set is bounded. The
  [preferred combined record](reviews/radial_ir_cold_2026_11_01/run_loss_v2/result.json)
  gives lifetime >=1.15116e20 s and >=.996224 survival over 13.8 Gyr. It uses
  a conservative hard box/seagull majorant, Ward/current soft completion,
  physical thresholds and interference-safe collision bounds. This is not
  an all-orders inclusive or early thermal-history theorem.
- A stipulated unpolarized FD relic at that point is cold (travel distance
  103.75 pc, independent bound <120 pc). It was **not produced** by TP04.
  Its raw vacuum is 1.396e74 times the DE benchmark. Fixing raw F energy to
  DE instead makes the photino far too light and defeats the tested density
  construction. An independent vacuum offset cannot be silently assumed.

## TP05: exact starting point for continuation

Canonical supergravity with W_raw+W0 is a new calculation, not an arbitrary
constant added to the rigid potential. To leading order the canonical
linear term is

    delta V=-4 f W0 Re X/Mp^2=-4 F_eff W0 Re T/Mp^2.

All cubic W terms cancel by Euler homogeneity. There is no heavy-a,b tadpole
at this linear order. For W0 approximately F_eff Mp/sqrt(3), the old MeV
point's force is too large for the shallow CW minimum. The completed
*preliminary one-loop shape plus leading tilt* run finds:

    R/R_rigid at phase-pair closure =1.13196225,
    fold R/R_rigid =1.26673987,
    at e=.003: mu_fold=600578 GeV, m_chi_fold=26.1319 keV,
    old MeV benchmark force / maximum CW restoring force =30.2553.

These are not a completed finite SUGRA vacuum or a universal photino exclusion.
Read canonical_gravity/run_shape scope and any later saved partial status.
The exact next issue is the full displaced stationary point, spectrum and
vacuum tuning, including heavy-normal and higher-order gravity corrections.

The R-breaking phase mass matters for production. For a canonical potential
U(R)-J R cos(theta), at its aligned stationary point,

    J R=U_s, m_sigma^2=(U_ss-U_s)/(2A), m_a^2=U_s/(2F).

For A=F=R^2, phase-pair closure is U_ss<=5U_s, while the radial fold is
U_ss=U_s. The actual cubic is (m_sigma^2-m_a^2)/(sqrt(2)R), so

    Gamma_sigma->aa=m_sigma^3/(64pi R^2)
        (1-m_a^2/m_sigma^2)^2 sqrt(1-4m_a^2/m_sigma^2).

Using only the massless width times a phase-space factor is wrong. These
identities have exact symbolic checks in TP05/run_structures.

The protected-gravity route is unfinished. Exact no-scale cancels its own
W0 contribution but does not automatically cancel matter F energy; modulus
stabilization and physical neutral fermions are mandatory. An almost-no-scale
construction was proposed to suppress the tadpole, but it adds modulus
breaking and must rederive the Goldstino/current normalization. Do not adopt
its preliminary verbal estimates as a verified spectrum. Added status/code
files in protected_gravity/ record what was actually persisted at interruption.

Production has not yet delivered a solved abundance. The concrete first
source is the existing radial mother. The rigid phase-open estimate has
tiny direct photino branching (~8e-6), whereas phase closure can make the
U1 branching roughly .29. A massive phase can itself decay into gauginos:
sigma->aa->gauginos must be tracked, not counted as permanent dark radiation.
The first unresolved calculation is the coupled decay/entropy/momentum
history using a genuinely surviving gravity vacuum. Warm injection and
nonabelian companions may defeat a naive yield fit. No reheating portal or
temperature ratio has been derived or silently introduced.

## Meaning of keeping the dark-energy link

Keep separate: (a) raw model F energy sets DE; (b) an explicitly tuned net
SUGRA residual equals DE and is inserted in the existing a0 relation. The
second does not derive the first or kappa. W0 cancellation at the MeV point
requires roughly 74 decimal orders of residual tuning. A concrete Einstein-
frame particle embedding also does not supersymmetrize the V3 khronon/P action
or derive J(Y). These distinctions are contractual, not optional terminology.

## Verification and portability

Each phase has exact input hashes, independent audits, bounded v2 manifests,
failed histories and handoffs. The preferred TP04 record is run_loss_v2;
older rate-sum and charged-Goldstone diagnostics are superseded by explicit
addenda, not deleted. TP05 has only the completed records listed in the
handoff verification inventory; unexecuted scripts/proposals remain labelled.

The fresh provenance check validates all 58 completed numerical manifests,
parses 80 current Python sources and rechecks all 205 TP04 artifact pins.
Thirteen failed/launch-failed histories remain. Nine of those reference
subsequently changed source files; the report identifies exact archived
versions where available. Four early TP01 failed/launch-failed records lack
an exact preserved source version. They are diagnostic history, not reusable
completed evidence. No numerical experiment was rerun for this checkpoint.

The remote checkpoint intentionally excludes unrelated dirty work and raw
local N-body snapshots/cache files. The companion HANDOFF_VERIFICATION.json
lists all current external input paths and hashes, tracked/untracked status
and missing dependencies. Forward SU(5) calculations use the committed TP01
spectrum modules. Reproducing the older spin experiment additionally needs
its original local snapshots. Do not claim a fresh clone reproduces data it
does not contain.

The frozen verdict document had unrelated pre-existing edits. Only our dated
law erratum is committed there; its exact reviewed full working copy is saved
as an evidence snapshot. The working file and unrelated edits are preserved.

Run the manifest validator from the installed mathbox computation-audit skill
against the source workspace. Recorded commands use original fresh output
directories: choose new ones for a rerun. All numerical jobs use one thread,
minute-scale caps and measured RSS. No production job, queue mutation, package
installation or new simulation is part of this handoff. Commit/push was
explicitly requested by the owner; it changes the prior no-Git action status
only for this final handoff.
