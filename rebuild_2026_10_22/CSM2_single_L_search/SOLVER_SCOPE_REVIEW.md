# Source solver bridge: sampled agreement, uniform bridge unresolved

solver_scope_001 executes extracted original X53 arithmetic for all62 active
halo nodes at L=3.75,3.7505,3.751:186 scalar solves, with no observational
regrade. The CL3 S9 table is rebuilt from the original A2 values. Instrumented
callbacks reproduce uninstrumented outputs bit for bit. All peak optimizations
and Brent solves succeed; none saturates. All14 run and10 independent review
controls pass. The completed runner record validates; hashes and observed
binary fingerprints are unchanged. Nine90-digit normalized-root checks on
first/middle/last nodes agree with the70-digit references.

Maximum observed log-root error is2.945522e-15. All186 samples are within the
nominal mixed log-radius tolerance. Minimum sampled log separation between
root and selected peak is2.560958. These are finite observations, not uniform
bounds on intermediate L or a certified optimizer branch decision.

In147cases the callback returned exactly0 while independent analytic log-mass
residual was nonzero. This is ordinary evaluator rounding at tiny residuals;
it is not evidence of a physically large error. It does demonstrate why a
zero callback cannot itself certify the analytic root. The official Brent
implementation can stop on a zero callback before its bracket-width test.
Its tolerance governs the supplied callback. The installed bounded minimizer
also uses sqrt_eps*abs(x)+xatol/3 as its internal tolerance; the requested
xatol alone is not its full stopping criterion. A separately biased callback
passes the solver but fails independent analytic residual control, as intended.

Installed wrappers, bounded minimizer and official SciPy1.14.1 Brent C are
cached with the SciPy license and provenance. Installed binary SHA256 values
are fingerprints, not independent build authentication. No justified uniform
libm error or optimizer-decision enclosure across this continuous parameter
interval was established. The original floating-evaluator bridge therefore
remains INCONCLUSIVE; the conditional score lower is not upgraded.

The likelihood scope audit identifies another explicit distinction: the fixed
numerical law comparator is F2 stack_model across all127 positive nodes. The
previous original-input reconstruction of65 hybrid law-side nodes does not
recompute this comparator. Its exact feasible-candidate upper154.34346325076024
is valid for the fixed recorded numerical vector, not automatically for an
analytic replacement of that vector. No previous result claimed that upgrade.

Next execute ANALYTIC_COMPARATOR_ROUTE.md under a separately frozen contract.
That can resolve a concrete analytic-likelihood scope question without assuming
an unproved libm ULP bound. Retain source-solver/continuous-evaluator assumptions
separately. There is still no real-L/global obstruction or full passing witness.
Native source/copy inventory remains7of9; only4and6 are pending.
