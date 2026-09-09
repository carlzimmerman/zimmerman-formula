# IC26 execution review

All four bounded jobs are terminal. None is still running.
Base b2a5cc4ec32122984c19e5749e29a15b191ae716; selected action M_*=-.03.
The exact child argv, runtimes, statuses and scoped file list are in
run_index.json. The v2 manifests additionally record input/output hashes,
dirty working state and resource caps. All four validated with exit0 against
the current inputs before subsequent checkpoint work.

- Regression child0, runner0: 371 tests in198.783s (runner199.165952s).
- Construction child2, runner1: all ten scoped checks true,152.299747s.
- Transport child2, runner1: all three scoped checks true,198.923569s.
- Precision child2, runner1: both scoped checks true,105.712105s.

The nonzero strict exits are deliberate: no full-theory closure is established.
They are not silently converted to successful execution statuses.

## Strongest supported result

Three S-only action functions are reconstructed and actually varied.
Their one-efold charge drift is4.1821e-14. The same selected action reaches
seven designed e-folds, with charge drift1.10283e-6. This is not an infinite-time
limit or an empirical cosmic expansion history.

The formerly very large k_initial²=100 amplification near2.26e5 is reduced to
5.56317737 in the specified kinetic norm. A60-digit independent integration
gives5.56315097, step-refinement relative difference1.41742e-5 and volume
identity relative error1.11548e-58. The background interpolation remains
double precision, so this is not60-digit accuracy of the entire physical model.

The SIX refined maximum singular values, at initial k²=.001,.01,.1,1,10,100,
are1.20244090,1.19562594,1.22970042,3.18613527,17.16407404,5.56317737.
In particular5.563 is NOT the maximum across the sampled wavelengths.
No observational meaning or universal stability threshold is assigned to this
coordinate/norm-dependent amplification.

The projected rational denominator was corrected before the runs to
2a(2Bp-m)(4Bap+C²-2am), matching symbolic reduction. This displayed factor2
is unrelated to the fitted a0 normalization.

## What still needs construction

Residual slow modes require physical, coordinate-invariant interpretation.
IC27_PHYSICAL_METRIC.md is the next calculation of that missing map.
The same coefficient functions must work off the designed background.
Global/static matching, complete nonlinear constraints, physical causality,
interaction scales, measured G and PPN, and actual empirical tests remain open.
No Lean proof, independent peer review or novelty certification is claimed.
