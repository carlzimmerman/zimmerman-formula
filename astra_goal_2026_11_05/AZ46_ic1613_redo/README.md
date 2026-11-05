# IN PROGRESS — diagnosis complete; beam-aware cube redo frozen

Kappa=1/2 FITTED; not theory closed. DIAGNOSIS.md records the preliminary
investigation committed in a8f468e93c. It reproduces both old discrepancies
and identifies beam/weighting and derivative/velocity-field comparison
issues without changing FN4a's verdict. The full table-to-map mass origin
remains unidentified; missing reference products are in NEEDS_OWNER.

Criteria e3d557204a now freeze the independent cube redo: each weighting's
own beam/mask/noise, both a0 footings,2x2/4x4 numerical pairs, original
model families and mass/thickness brackets, mock controls, shuffled-
channel mutation, optimizer checks and preemptible heavy-queue execution.

No new preparation or production cube fit has yet run. The implementation,
small pilot/footprint/resume contract, queue submission and final physical
labels remain required. External benchmark NOT EVALUABLE is distinct
from any future conditional local-cube verdict. This is not a completed
lane12 result.

## New beam and raw-reader checks: partial numerical failure retained

The new io_beam.py reads each cube's own CLEAN header and integrates its
Gaussian over pixel boxes once. It does not carry FN4a's natural beam into
the robust cube, nor add another Gaussian box variance before subpixel
integration. check_beam.py applies the already-frozen2% second-moment line
at3/6arcsec pixels and5/9 subpixel quadrature. It passes16/18 checks.
Natural weighting and the3arcsec robust grid pass; the6arcsec robust grid
fails the minor-axis moment at both quadratures: relative errors6.3024%
and5.3341%, versus the2% line. Increasing quadrature from5 to9 changes
that moment1.0229%; the continuous Gaussian-plus-box moment is still not
recovered on this coarse sampled grid. No tolerance was changed, and no
moment-matching adjustment was made to obtain a pass. This is an open
numerical obstruction to the robust coarse/fine cube verdict, not a
physical rejection of the galaxy or action.

MUTATE substitutes the natural beam for the robust beam. The correct
robust CLEAN-header anchor passes in main and fails in the separate
mutate/beam_checks.json. This specific changed check establishes that the
control bites, independently of the main run's existing moment failures.
Both a0 footings share these geometric checks; no field fit is graded.

check_io.py passes4/4: independent Astropy-section agreement at32/64 row
chunks, row-sum convergence1e-10, and exact recovery of the rounded
262.8614460793164Jy km/s parser anchor. This remains a parser test, not an
observational flux acceptance. All three scientific JSONs are byte-identical
on fresh repeats, including the beam failures. Commands in the installed
conda environment:

    python -W error astra_goal_2026_11_05/AZ46_ic1613_redo/check_io.py
    python -W error astra_goal_2026_11_05/AZ46_ic1613_redo/check_beam.py

The first exits0; the second deliberately exits1 for the two failed main
checks. Full cube preparation, interrupted/resumed pilot, physical footprint,
queued fits and local-cube grading remain pending. The external published
benchmark remains NOT EVALUABLE for the separately documented missing data.
