# CSM1 verification and interpretation

The computation corrects the internal parent-column/selector mismatch and
regrades the existing finite model. It does not close the physical theory.

## Verified evidence

1. Original CL3 L=3.75 source controls reproduce both X43 and X53 exactly:
   315 and 1964 result leaves, identical keys, zero numeric discrepancy.
   BS1 geometry, five class grades, individual field residuals, MW box and
   McMillan controls also reproduce before corrected interpretation.
2. Bounded calibration run 003 reproduces the full pilot's L=3.75 grades;
   bounded replay 004 reproduces its L=3.9 and 4.0 grades exactly. The exact
   defined challenge is run 008. No source changes to active scientific
   scripts are used to reinterpret a completed result.
3. Corrected branch decisions are logged at their actual comparison mass,
   column and floor. Independent scalar recomputation checks the native
   representations. The calibration flag mutation inverts and detects all
   8806 actual flags while leaving the pure comparator intact; its scientific
   results change. The heldout mutation likewise inverts and detects all 882
   decisions per level after unchanged baseline controls pass.
4. Heldout primary fresh runs 006/007 are byte-identical. The exact challenge
   fresh runs 011/012 are byte-identical. All grades and individual MW cells
   remain in the source JSON.
5. Coordinator reconciliation regrades source primitives rather than copying
   the combined verdict: 141/141 coverage, arithmetic, source-grade, replay,
   manifest-status and input-stability checks pass. It recomputes both lens
   differences, exact P4 group rule, all cluster cells, five class Z values,
   and V+K/all-four counts from all 175 MW cells. Its completed v2 manifest
   validates. Scientific failure is separate from these implementation passes.
6. The independent [final calibration audit](feasibility/calibration_review_002/results.json)
   passes 10/10 checks: 57,920 positive column values agree within 3.56e-15
   relative error, floors agree exactly, and actual predicates have zero
   disagreements. It separately checks 14,000 own/basin amplitude and flag
   comparisons, 12 old baseline comparisons and 164 applicable harness checks.
7. A separate [heldout final review](heldout/FINAL_REVIEW.json) checks primitive
   MW line decisions from their observable values and frozen cuts, rather than
   merely counting stored booleans. It also checks class median/sd Z arithmetic
   and MW classifications. The coordinator counts those checked decisions.

The inherited source self-tests are preserved. Some assume the old fixed
branch/floor-only halo or an earlier gas budget and are inapplicable to this
model; applicable baseline controls are tested separately. No inapplicable
self-test is represented as a scientific pass.

## Corrections retained in the record

The first challenge scalar used displayed a0 rather than X43's imported FP0
digits. This changed L by 5.32354e-6. The frozen target logM=12.3 stayed fixed;
the actual-function value 2.5090648745652686 was rerun across calibration and
heldout scorers. The approximate challenge remains development evidence.
Calibration run 007 also caught launcher-metadata provenance changing during
startup; it is excluded. Run 008 uses a new immutable launcher and validates.
Earlier environment/harness failures are retained in the owners' ledgers.

The coordinator's first preflight refused identical heldout levels replayed
inside the challenge packet. It now permits duplicates only when their
entire cell dictionaries agree exactly. The development reconciliation uses
the approximate challenge and is excluded from final science. An initial
coordinator runner invocation with Python -I could not import the runner's
sibling validator and launched no child; the runner uses its normal import
path and the scientific child remains isolated. No scientific grade or cut
changed during these harness corrections.

## Claim limits

The four levels fail the joint calibration, but do not prove that every
canonical L fails. The exact lens-support cap and necessary LG threshold
leave a canonical interval. Group scatter and mass slopes change with L;
profile branches can jump. Neither likelihood nor group-Z monotonicity was
assumed. A proposed max-speed MW lower bound was actually evaluated and is
vacuous (Lmin=0 in the forced-halo relaxation).

The alternate-footing UFD result is stronger only because source inspection
reduces that fixed class to exactly two L-independent profile states, both
failing. It is conditional on X51's cooling-floor construction, class data,
bootstrap, fixed basin and footing. It excludes changing L alone in that
construction, not arbitrary alternate-a0 models.

SPARC has SPS refits already in the inherited model, the MW box explores
existing baryonic priors, L remains an existing empirical calibration level,
kappa=1/2 remains fitted and basin selection remains a posit. None becomes a
first-principles prediction because an implementation check passes. The
corrected model uses no newly fitted T, concentration shape or other number.
