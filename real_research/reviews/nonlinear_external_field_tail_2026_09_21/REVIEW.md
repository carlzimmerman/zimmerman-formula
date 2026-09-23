# Self-audit of the nonlinear external-field coefficient

Primary verdict: **conditional on a named input** — the differentiable far-field
multipole expansion stated in PROOF.md. Within that class, the quadratic
coefficient and its filtered orbital relation follow from the displayed PDE.
This is a self-review, not an independent-agent or external referee report.

## Dependencies and obligations

`chosen static PDE + smooth response + positive background ellipticity`
`-> quadratic flux Hessian -> forced odd exterior solution`
`+ differentiable multipole expansion -> universal odd axial coefficient`
`-> opposite-side and radial subtractions -> nonlinear statistic`
`+ isolated spherical flux + ordinary circular motion -> orbital relation`.

| Obligation | Status | Evidence or boundary |
| --- | --- | --- |
| Vector flux Hessian, including longitudinal coefficient | Passed | All 27 components differentiated from mu(norm(v))*v |
| Minus sign in AQUAL's quadratic inversion | Passed | Full symbolic cylindrical PDE identity; direct nonlinear residual scaling |
| Positive stretch and source normalization | Passed | Gamma=1+L>0; volume Jacobian sqrt(Gamma); flux 4 pi G M_b |
| Odd angular inversion and absence of resonance | Passed | Only ell=1,3 forced; eigenvalues 4,-6; ell=2 homogeneous mode even |
| mu second derivative cancels on the axis | Passed | Both direct substitution and independent harmonic coefficient sum |
| Dipole cannot be discarded | Passed | Global second-order source integral; induced dipole depends on positive energy-like integral |
| Unknown source quadrupole cannot contaminate odd degree -3 | Passed under expansion | Spatial inversion parity and radial order |
| Two-radius subtraction and its normalization | Passed | Exact algebra and Lean; arbitrary d retained |
| Three-radius subtraction removes next odd homogeneous power | Passed | Exact algebra, Lean and compact-source Green integrals |
| QUMOND uses Newtonian input gradient, no AQUAL stretch | Passed | Separately differentiated flux and Poisson identity |
| Physical external acceleration and axial amplitude in QUMOND | Passed | g_e=nu_e n_e; K=G M_b nu_e; coefficient -k_nu |
| Full nonlinear QUMOND example | Computationally verified in stated range | Positive compact spherical sources; finite angular modes, radial/angular convergence checks |
| General nonlinear AQUAL global solution and expansion existence | Not addressed | Explicit premise; second-order global examples do not prove this |
| Observational construction, tides and error budget | Not addressed | No data fit or projected-velocity claim |
| Literature priority | Conditional/bounded | Relevant primary sources read; exact combined relation not located in stated search |

## Adversarial checks

1. **Point-source singularity:** no assumption of weak internal gravity all the
   way into a point source. The universal calculation is exterior only. Global
   second-order examples have regular compact sources. Their source-radius
   limit need not commute with the perturbation expansion.
2. **Source-shape pollution:** degree -2 odd terms survive and must be removed;
   degree -3 homogeneous terms are even. The radial combination addresses the
   former, and the opposite-side difference addresses the latter. The more
   general QUMOND linear images of Newtonian multipoles preserve these parity
   and radial-order properties.
3. **Coordinate/sign reversal:** z follows the external potential gradient.
   Swapping the physical axis while retaining old labels reverses D, so the
   convention must be fixed in any experiment. A fixed origin translation
   changes d but not the coefficient selected here.
4. **Background-subtraction error:** an unremoved constant acceleration changes
   D and is not eliminated by the dipole filter. The uniform background is
   assumed known and subtracted. A freely falling reference convention must be
   reconciled explicitly before importing old solver outputs or real data.
5. **Response normalization:** the coefficients are dimensionless. Rescaling a0
   moves the acceleration at which a given beta occurs but cannot change the
   relation at physically matched acceleration for one fixed response.
6. **Degenerate cases:** mu_e=0, g_e=0 or Gamma<=0 are excluded. L=0 yields a
   zero axial coefficient, even if M is nonzero and an off-axis quadratic
   response remains. The Newtonian response L=M=0 removes the whole correction.
7. **Detection size:** N=1 versus 1/2 is a coefficient difference. The physical
   term is of order internal-force-squared/background-force and falls as r^-4.
   The radial subtractions amplify noise; no practical sensitivity is claimed.
8. **Finite evidence:** exact symbolic checks certify identities of the stated
   expressions; residual scaling does not construct a global AQUAL solution.
   Lean certifies eight algebraic implications and does not certify the PDE.

## Numerical issues encountered and resolved

The initial generic SymPy Hessian contained unevaluated `Subs(Derivative(...))`
objects. Evaluating those substitutions before replacing derivative symbols
resolved the mismatch; no mathematical coefficient was changed.

The initial compact-source Green check used an absolute quadrature tolerance
of 1e-13. Its small ell=3 outer integral at stretched radius 64 had a relative
error about 2.8e-4; the radial extraction magnified it. Comparing that integral
with its independently known exterior power-law integral identified the cause.
At absolute tolerance 1e-24, the same tail comparison was at about 1e-16 relative
error. The final benchmark uses this tolerance and independently compares the
dipole source integral with the integration-by-parts expression.

The first nonlinear QUMOND integration attempted adaptive integration of tiny
high angular projections; roundoff warnings prevented the requested accuracy.
It was replaced by deterministic Gauss–Legendre quadrature with logarithmic
interior-tail coordinates and a finite-interval inverse-radius outer integral.
Three angular/radial resolutions and angular truncations are compared. The
source uses cancellation-safe differences of powers, evaluated with log1p and
expm1. No warning is suppressed and no failed output is promoted to evidence.

## Mathematical proofreading

Scope: README.md, PROOF.md, LITERATURE.md, this review and TailAlgebra.lean.
Checked symbol definitions, opposite-side signs, powers, physical versus
stretched radii, field versus force conventions, source-mass versus response
second-derivative notation, source links, and the theorem/computation boundary.
No unresolved local typographical issue was identified. The remaining analytic
and observational gaps above are substantive, not typographical.

## Next executable handoff

Use the fixed conditional coefficient as a target for a nonlinear AQUAL solver,
with compact sources of multiple shapes. The outer boundary must include or
fit the unknown dipole; imposing only the linear monopole can bias precisely
the quantity under test. Compare spatial resolution and boundary distance
separately, and report the coefficient's convergence with extraction radius.
This is additional validation, not a replacement for a general asymptotic
existence theorem. No background job remains running for this package.
