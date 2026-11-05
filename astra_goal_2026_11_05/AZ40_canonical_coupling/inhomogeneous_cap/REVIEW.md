# Adversarial self-review

Scope: full action in an exact plane-symmetric, external-matter-free sector.
This is a self-audit, not an independent referee or independent PDE solver.

Checked signs: the integrated Hamiltonian polarization coupling is +v Dp;
pi_B carries both transverse directions; lambda differentiation is an envelope
identity; the scalar force from Theta_star(phi) is retained by differentiation.
Physical P is a permissible auxiliary field variable: metric-dependent field
redefinition changes metric equations only by its on-shell auxiliary equation.
The shift variation is retained as Cmom before w=0. Unitary clock gauge is not
used to discard the Hamiltonian constraint or clock physical mode.

Checked discrete constraints: the lapse null-vector construction follows by
implicit differentiation of the nonconstant Hamiltonian constraints. The
remaining mean energy is monitored, not reset. Odd grids remove the Nyquist
derivative kernel. Reflection symmetry is explicit. Discrete product rules do
not preserve the continuum momentum constraint exactly; measured residuals and
refinement are required. Grid-point polarization stationarity is insufficient,
as the independent dense interpolation audit demonstrates.

Rejected claims:
- No completed evolution through the target t=3.
- No physical singularity inferred from a failed Newton iteration, exhausted
  retry budget, truncated lapse sign, or an off-grid-invalid P interpolant.
- No statement that the cap cures the full action, or makes collapse earlier.
- No equal-physical-initial-data comparison with the cap-off control.
- No full four-dimensional curvature invariant or global existence proof.
- No transfer of the old galaxy background checks to this new action.

Conditional mathematical conclusions reviewed:
- The general volume bound assumes a lower bound on Theta_star and a smooth
  solution. On the tested positive-phi branch Theta_star>0, so v>=v0 exp(-T s)
  needs no upper bound on the target; it still does not prove smooth continuation.
- The polarization separation bound additionally needs finite R/a^2.
- Exponential lapse positivity requires nonzero F, bounded G and periodic
  compatibility. At F=0 the displayed differential equation cannot be divided.
- Q=1/N: N->0 corresponds to Q->infinity, not loss of timelikeness by Q->0.
- Expanding trace control into shear/curvature control is not justified.

Evidence limits: finite floating-point sampled checks, not rigorous enclosures.
Explicit-summation derivative checks cover selected matrix operations, not a
complete diagnosis of the numerical-library warnings. The original and
bracketed cap solvers both have recorded late trial failures; neither endpoint
is promoted to a mathematical obstruction. The postprocessor uses the robust
root and succeeds on all saved states and dense audits it reports.

The decisive remaining work is spatial/domain-preserving continuation with
constraint convergence through the steep profile. Increasing only time accuracy
has already failed to remove spatial ambiguity. Adding another cap before
resolving that ambiguity would not be justified by these runs.

Proofreading self-review: REDUCTION.md, REGULARITY.md, RESULT.md and this review.
Routine edits: list spacing and clarification of the stronger positive-target
volume bound. The latter is a substantive derivation recorded in REGULARITY.md,
not a typographical correction. No mathematical-token changes were made during
the final proofreading pass. Unresolved correctness limitations are listed above.
