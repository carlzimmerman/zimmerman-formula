# Nonlinear clock, critical force, and disformal-cone checkpoint

2026-09-12. Continued from `bba135b36`; also inspected Claude's new PAPER24
commit `96512fc6e`. **Full theory: OPEN. No all-gates certificate exists.**
This checkpoint changes no fixed action functions and performs no fits.
Carl Zimmerman's primordial-clock proposal and fixed global acceleration-scale
framework motivate the calculation; no derivation of the fitted one-half
coefficient is claimed.

## Three previously unresolved calculations now have explicit results

| Opening tested | Result actually derived | Scope / verdict |
|---|---|---|
| Nonlinear clock elimination | Regular branch has an even analytic reduced action; clock-critical branch has \(F_W\sim\operatorname{cbrt}(p)\), not \(p|p|\). At \(W_c=0\), exactly \(z=p/q\), \(Y=0\). | This local clock-only constitutive rescue fails near the specified origin. Not a full physical-force no-go. |
| Singular metric response | \(Gp+4\gamma p^2/r=2b g_N\), hence at \(G=0\), \(p^2=q^2M_{\rm enc}/(16\pi M^2r)\). | Derived minimally induced source in a controlled derivative truncation. Scalar force \(\propto r^{-1/2}\), not MOND. Full fixed-history boundary problem remains OPEN. |
| L215 disformal lensing repair | \(c_\gamma^2/c_T^2=(C-D)/C\); equal linear potential shifts plus unchanged common cones imply \(c=d=0\). | The nonzero shift-only repair fails the exact common-cone gate under the stated tensor-background assumptions, even at perfect clock alignment. |

The nonlinear clock formula is action-derived, not a fitted interpolation.
Writing \(p=\pi'\), \(z=\sigma'\),
\(\mathcal D=\ell(1-z^2)+(p-qz)^2\), the exact frozen zero-current equation is

\[
\boxed{
2d\sqrt\ell\big[(q^2-\ell)z-pq\big]\sqrt{1-z^2}
=(W_c-2d\ell)z\sqrt{\mathcal D}
}.
\]

It follows by varying \(sW\). Squared roots are filtered through this original
unsquared equation, with the timelike domain enforced. The generic critical
branch has \(z=a\operatorname{cbrt}(p)+\cdots\),
\(a^3=-2\ell/[q(q^2-\ell)]\); the exceptional case \(q^2=\ell\) admits
no nonzero-slope zero-current solution. These are mathematical results about
this specified reduction, not new empirical laws of nature.

The critical metric calculation also finds an explicit term the simpler force
estimate misses:

\[
\mathcal L_{\rm critical}^{(3)}
=-\frac{4\gamma}{3}rp^3
-\frac{\alpha}{2}(G_{0,N}+3G_0)r^2\pi p^2,
\qquad \alpha=\gamma q^2/M^2.
\]

The second term is not generically negligible merely because amplitudes are
small. Lower derivative terms from the same action can dominate the critical
quadratic source response. The report gives explicit coefficients and ordering
bounds instead of calling a partially truncated equation a complete solution.

## Where the complete-theory gates stand

No new all-background Dirac closure, CMB/FLRW solution, galaxy/cluster dust
transport, full PPN matching, or empirical fit was produced by these local
calculations. The earlier finite-mode Dirac counts are still truncation-level
results and retain a scalar canonical pair on the regular clock branch.
Matter conservation remains the Ward identity of minimally coupled matter for
the **unchanged** action; moving matter to a disformal metric is a new theory
whose physical-frame conservation and constraint equations must be rederived.
The existing tensor/common-cone pass belongs to the original minimal action
on its tested homogeneous background, not automatically to L215.

Static no-slip on the earlier aligned affine branch is not full PPN, MOND,
or arbitrary-background stability. The exact exponential law, Newtonian
calibration across regimes, controlled physical zero-field limit, acceptable
PPN, nonlinear constraints, viable cosmology and galaxy/cluster evolution
still have not been derived together from one candidate.

`PAPER24_AUDIT.md` records the action-to-claim corrections. In particular,
the clock does respond at \(W_0=0\), and the new metric coupling brings a
cone gate in addition to any clock-alignment question. This checkpoint does
not modify a public deposit or infer dishonesty from a derivation error.

## The next unavoidable calculation

For the unchanged action, derive the **on-shell**, fixed-history, sourced
lapse–spatial-metric–clock–scalar system including the displayed metric
correction, lower derivative terms, background Hessians and boundary data.
First determine whether a radial domain satisfying the explicit ordering
bounds actually exists; only then solve a source-amplitude family and extract
both physical potentials. If the goal instead is to pursue L215, it first
needs a complete covariant matter factor and a gravitational principal action
with the same physical cone, followed by a new constraint analysis. Clock
alignment alone is not that calculation. Do not reconstruct new histories
to force either route to pass.

## Verification and handoff

All 18 commands in `followup_run_001/checks/summary.json` exited 0: 14 Python
jobs and four Lean compilations. Twenty printed theorem axiom sets contain
only `propext`, `Classical.choice`, `Quot.sound`; **nine of these statements
are new**. They certify the stated conditional algebra, not the action-to-
observable chain or a law of nature. The assertion negative control exited
1 as intended. All four current Mathbox manifests validate against their
input hashes. Independent proof review checked the new cone calculation,
clock expansion and critical projection; its domain/ordering qualifications
were incorporated. Conservative mathematical proofreading fixed three
display-spacing typos without changing equations.

| Important job | Exit | Evidence |
|---|---:|---|
| Nonlinear clock | 0 | 39 symbolic checks; 28 cases at 60/90 digits |
| Critical radial | 0 | 25 exact checks, explicit omitted-term coefficients |
| Disformal cone + unit test | 0 / 0 | 34 exact controls; Maxwell variation |
| New Lean files | 0 / 0 | 5 cone + 4 critical-radial statements |
| Earlier action/response/Dirac/radial regressions | 0 each | 9 Python + 2 Lean jobs |
| Earlier tensor-cone regression | 0 | Tensor and minimal-Maxwell actions |
| Manifest validation | 0 each | Four current provenance records |

See `FOLLOWUP_FILES.md` for exact new files, `FOLLOWUP_COMMANDS.md` for the
complete runner command, and the child summary for exact executable paths,
working directories, exit codes and hashes. The research/computation-audit
skills enforced frozen inputs, independent controls, bounded evidence and
explicit nonclaims; they did not supply a physical theorem.
