# Independent audit — tensor-compensated branch

Date: 2026-09-12.  This note is an independent check of the newest branch;
it does not treat a green script as a proof of the full theory.

## What survives the executable checks

The proposed extension is

\[
 S_{TC}=S_{DDM}+\int d^4x\,\sqrt{-g}\,
 \Lambda^{\mu\nu}[D_\mu D_\nu\chi-D_\mu a_\nu]^{TF},
\]

with a spatial, trace-free multiplier.  The finite-\(k\) principal-symbol
calculation gives

\[
 \mu(y)=1-e^{-y},\qquad
 \Lambda^{TF}=-\frac{2M^2 S y^2e^{-y}}{k^2},
 \qquad \delta E_\Phi+\delta E_\Psi=0,
 \qquad c_T^2=1.
\]

The fresh scripts report 10/10 for the finite-\(k\) MOND/slip algebra, 12/12
for the generated five-component Dirac matrix, 9/9 for the FLRW background,
12/12 for the homogeneous minisuperspace chain, 11/11 for the linear tensor,
vector, and scalar diagnostic, 10/10 for the tuned \(\alpha_1,\alpha_2\) algebra,
and 4/4 for the minimally coupled matter Ward identity.  These are bounded
checks, not a closure certificate.

## Independent failure found

`anti_hardcode_audit.py` scans the executable gates rather than their JSON
outputs.  It found 16 comparisons of derived count fields with literal values
(for example `finite["constraint_rank"] == 10` and
`finite["physical_dof"] == 0`).  Therefore the current Dirac/DOF suite does
not yet satisfy the project's anti-hardcoding requirement.  The diagnostic run
exits 0 and the strict run exits 1 by design:

```text
HARD_CODED_COUNT_EXPECTATIONS_FOUND 16
```

Until those assertions are replaced by derivation-only invariants, the numbers
0, 1, 6, and 10 must be treated as reported outputs, not independently
certified results.

## Exact obstruction still open

The branch gate inserts the trace-free residual
\(R=2M^2 S y^2e^{-y}\) into a principal-symbol model; it does not yet derive
the complete nonlinear metric variation of the covariant multiplier action.
The tuned Einstein-aether PPN block also lands at \(c_{14}=0\), where the usual
spin-0 PPN denominator is singular.  Thus full covariant Dirac closure,
preferred-frame parameters (especially \(\alpha_3\)), the inhomogeneous
\(k=0\) chain, and nonlinear/loop stability remain open.

The new IR gate sharpens this: cancelling that generic trace-free residual
requires \(\Lambda_{TF}=-R/k^2\).  A regular zero-mode continuation gives
\(k^2\Lambda_{TF}\to0\) and cannot cancel a nonzero anisotropic source.  The
spherical angular-average check only handles a special \(\ell=2\) source; it
is not a generic all-\(k\) closure.  The gate and its unit test pass (exit 0)
while establishing this inverse-Laplacian singularity.

The attempted local rescue was also tested. With any quadratic regulator kernel
\(F(k^2)\), the two linear equations eliminate to
\(\Lambda=-R/k^2\) and \(\Phi-\Psi=F(k^2)R/k^4\). Thus a nonzero regulator
creates slip (and a constant regulator worsens the IR divergence), while
\(F=0\) restores no-slip only by retaining the pole. The five-check
`regulator_tradeoff_gate.py` passes (exit 0). This is a conditional no-go for
local quadratic regularizations of this derivative compensator architecture.

The tradeoff is now formalized in
`RegulatorTradeoffFormal.lean`.  The Lean runner exits 0 (with only an unused
hypothesis warning) and proves, from the two principal-symbol equations alone,
\(\Lambda=-R/k^2\) and \(d=F(k^2)R/k^4\), plus the implication that exact
no-slip with nonzero \(R\) forces \(F=0\).  This is a genuine conditional
certificate of the obstruction, not a certificate of the full gravity theory.

The remaining operator-level fork was tested as well. A Helmholtz response
\(1/(k^2+m^2)\) is IR finite but introduces a new screening scale and still
needs a covariant action embedding. Promoting it to
\(k^2+m^2-\omega^2/c^2\) gives the real pole
\(\omega^2=c^2(k^2+m^2)\), i.e. a propagating auxiliary mode. The five-check
`ir_operator_tradeoff_gate.py` passes (exit 0); this narrows the next search to
a genuinely spatial, screened covariant construction.

The shared-operator generalization is now formalized in
`LocalSelfAdjointNoGoFormal.lean`: for any derivative operator (P) with
(P(0)=0), the zero-mode equation is (R=0), contradicting a generic
trace-free source, while finite-(k) exact no-slip forces every finite local
regulator (F) to vanish. The Python gate and Lean runner both exit 0. This
closes the local self-adjoint derivative-multiplier class represented by the
current branch, subject to those explicitly stated assumptions.

The invariant-order gate strengthens this assumption audit: in the standard
clock-foliation basis `(D_i a_j)^TF`, `R^(3)_{ij}^TF`, and further spatial
derivatives, every scalar trace-free term carries a factor of `k^2`; the
conformal scalar perturbation of `q_ij` contributes no trace-free piece. Its
Python and Lean checks both exit 0. This rules out obtaining a finite `P(0)`
algebraic rescue from those local invariants alone.

**Status: OPEN.**  This is the strongest constructive lead found so far, not a
complete relativistic theory.
