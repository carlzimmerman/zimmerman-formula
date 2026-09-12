# L194: a reproducible frozen ODE, not yet an action-derived tracking state

2026-09-12. Independent bounded audit of commit `9212f4498`, source
`fable_independent_2026/L194_tracking_dynamics.py`. Only the original
`coeffs`, `cs2`, `epoch`, `track`, `fixed_point` and `multi` function definitions
are loaded through AST extraction. The original top-level checks and JSON
writes are not executed; no old result or action source was modified.

**Verdict:** the tested finite-mode ODE attraction reproduces. Its equilibrium
has negative signed proxy sound speed, is invadable by an added higher mode,
and has not been derived as a statistical solution of the unchanged covariant
action. Neither the forest gate nor full-action stability follows from these
ODE checks. This does not disprove every possible nonlinear statistical
variance state, and the earlier localized-tail theorem does not exclude a
different nonzero statistical asymptotic state.

## Exact statements within the L194 ODE

The implemented equation is

\[
\frac{d\log Y_i}{dN}=-2+2\kappa_i\sqrt{\max(-c^2(Y),0)},
\qquad Y=\sum_iY_i.
\]

For a nonzero surviving mode at \(\kappa_{\max}>0\), stationarity requires
\(\kappa_{\max}\sqrt{-c^2}=1\), hence
\(c^2=-1/\kappa_{\max}^2\). Source line 15 displays the opposite sign;
the actual root solve at lines 54–61 correctly targets the negative value.
The scan at lines 72–76 and JSON output store its absolute magnitude. A small
negative number is not a real positive scalar characteristic speed.

At this finite-mode balance, an infinitesimal newly seeded mode obeys

\[
\frac{d\log Y_{\rm new}}{dN}
=2\left(\frac{\kappa_{\rm new}}{\kappa_{\max}}-1\right).
\]

Thus a mode at twice the old maximum has growth exponent 2, while a lower
mode decays. An exactly absent mode remains absent in this deterministic ODE;
the statement concerns invasion after positive seeding. The finite list's
equilibrium is not stable under extending its allowed mode set upward. This
does not posit a physical cutoff or establish whether additional action-level
physics regulates that extension.

## Original-function probe and two-mode experiment

At source epoch `a=0.5627048688069557`, `kappa=1000`:

- original fixed point `Yeq=0.00039947445288493564`;
- original signed `c²=-9.999999999875596e-7`;
- original `track`, starting at `0.01 Yt` and evolving eight frozen e-folds,
  ends at `Y/Yeq=1.0000000000000044` (313 function evaluations).

Seeding a mode at `kappa=2000` with variance `1e-6 Yeq`, while retaining the
old mode at `Yeq`, gives initial logarithmic rates approximately
`[-0.0036402, 1.9927196]`. The infinitesimal-seed limit is exactly 2 for the
new mode; the finite seed slightly changes the total variance and rate.
After twelve frozen e-folds the new mode carries `0.99387526` of the variance,
and `c²=-2.5153836619235863e-7`, close to the new balance `-1/2000²`.
The total variance equation and source proxy are unchanged during this test;
only the admitted mode set and its small seed differ.

Three signed source balances (`kappa=100,1000,10000`), one original track,
and this seeded two-mode experiment are archived. Five tests additionally
check a lower-mode non-invasion control and the source's explicit no-root
case at `kappa=1`. The scientific output is distinct from solver success.

## Why the claimed approximation needs another calculation

At the proposed balance, the assumed amplitude growth rate is
`k sqrt(-c²)=H`, even for large `k/H`. Therefore Hubble friction and
coefficient-rate effects are not parametrically negligible in the balance
itself. The large-k limit at fixed nonzero sound speed is not uniform in the
simultaneous `c²~-(H/k)²` limit being used here.

A separate exact sensitivity control illustrates the issue, without replacing
the action. In

\[
\sigma_{NN}+\nu\sigma_N-\kappa^2u^2\sigma=0,
\]

constant physical gradient variance requires amplitude `sigma~exp(N)`;
substitution gives `kappa²u²=1+nu`, rather than 1. Choosing `nu=3` gives 4.
This is not a determination of the actual action's friction coefficient. It
shows why the coefficient of the claimed balance cannot be inferred solely
from the dropped-friction approximation.

More fundamentally, source lines 9–21 and 45–52 impose the variance closure.
The exact local clock-frame identity is

\[
n\nabla Y=2D\chi\cdot(DQ+Qa)-2K_{ij}D_i\chi D_j\chi.
\]

Averaging it requires gradient/velocity/curvature correlations and a specified
averaging measure; replacing those terms by one common `c²(<Y>)` is an
additional approximation, not this identity. Nonlinear constitutive averages
also do not in general equal the constitutive function of the average.
The ODE freezes its background coefficients and `kappa` for eight or twelve
e-folds. It does not follow changing physical `k/(aH)` or the original
background across those e-folds.

The function `coeffs` at lines 34–35 uses the coefficient reference `qbar`,
not the evolved physical Q. Its `cs2` at lines 36–42 is the earlier scalar
proxy; it does not evaluate the full anisotropic cubic/Hessian/Einstein
principal operator or solve its statistical averaging problem. The source's
forest conversion at lines 77–85 is consequently not a demonstrated
full-action empirical pass. No external forest bound or physical cutoff was
authenticated in this bounded algebra/code audit.

## Evidence and next gate

`run_001` records source/input hashes, actual command, software, bounded
execution and result hash. `run_bounded.py` is its reproduction command and
preserves existing runs by requiring a fresh output directory. Run tests with
`python3 -B -m unittest discover -s` followed by this directory and
`-p test_tracking_audit.py -v`.

The next missing implication is an action-derived, constraint-compatible
equation for the claimed variance state, with its correlations, actual
principal operator, expansion-scale terms and admitted-mode domain controlled.
Neither another finite mode list nor an assumed UV cutoff supplies it.

Used proof-audit and computation-audit; mathematical self-review found no
additional mathematical-token correction in this new report.
