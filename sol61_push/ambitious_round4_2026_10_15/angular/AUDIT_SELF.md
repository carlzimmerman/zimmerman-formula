# Adversarial self-review of the new angular Hessian

Primary verdict: **proved as written at the static configuration-energy
scope, subject to the declared frozen hybrid model**. This is self-review;
an independent audit of the new shape terms is still requested. The
independent audits copied in `inputs/` cover the older radial result, not
this extension. The proof under review is SHA256
`0b9f3fdb54c22303084a43cf39354de15709995f20e2371fdd4691985e88583d`.

Claim card: the actual frozen positive-density, two-fluid, critically
charged, counted area-wall equilibrium at R=1; all smooth separately
mass-preserving physical tangents with common boundary normal displacement;
real normalized harmonic sectors; Q is the full second derivative. For
l>=2, Q >=0.01 times the sum of interior density L2 norms squared plus
0.25(l-1)(l+2) times the common shape amplitude squared. For l=1 the
corresponding positive norm uses eta_a+h rho_a', with translations and
material relabelings retained as nulls. Arbitrary solenoidal electric
remainders and static magnetic fields have nonnegative extra energy.

Dependencies and obligations:

| Obligation | Status | Evidence |
|---|---|---|
| Actual common spherical equilibrium, two hydrostatic equations, tension root | passed as pinned input | CRITICAL_PROOF plus two frozen audits |
| Independent fluids and common moving finite-density edge | passed | distribution (2), explicit flux in DERIVATION_APPENDIX |
| Gauss jump includes moving charged edge | passed | (3); radial fixed-charge trace check |
| Phase Hessian has its shape/field cross term | passed by reconstruction | differentiate phi pairing and phase jump; (4) |
| Uniform exterior-field control | passed | harmonic Maxwell energy and exact square (5) |
| Gravity includes both fluid source perturbations | passed | full multipole distribution kernel (6) |
| Wall mass varies with area; wall/fluid gravity | passed by direct material kernel differentiation | (9)-(10) and appendix; trace choice checked |
| Wall self-gravity | passed | explicit surface kernel expansion; all-l Legendre recurrence in appendix |
| Radial and translation limits | passed | l=0 reproduces radial load; l=1 shell factors vanish after equilibrium load |
| Full l>=2 and mixed relative/shape control | passed | Schur/Young bounds (12)-(16), exact rational constants |
| l=1 translation null and remaining positive quotient | passed | energy symmetry, (17)-(18), fixed-boundary gravity bound |
| Material vortical/relabeling nulls | passed and retained | weighted divergence-free tangent domain |
| Bounded implementation | passed in stated range | 219 checks, validated run_exact/manifest.json |
| Dynamic electromagnetic/interface spectrum or hyperbolicity | out of scope | static reduction cannot establish it |
| Einstein metric, shell junction, production or empirical viability | out of scope | frozen model is Newtonian hybrid |

Decisive adversarial checks:

1. Keeping only the positive electric Hessian fails: a moving phase has the
   cross term Delta h(d_++d_-). It is retained and controlled by the exterior
   Maxwell square, rather than discarded.
2. Freezing either source would change (6). Both eta_b and eta_c are free;
   the estimate bounds their sum only after retaining their separate positive
   pressure norms. Relative density motions are included.
3. Treating wall area mass as conserved gives different shell coefficients.
   The exact l=0 check against -8pi^2Gs^2R^3 and l=1 cancellation distinguish
   that wrong model.
4. An inconsistent interior/exterior trace in the wall/fluid calculation
   produces an extra -4piGs rho_Rh^2 and violates translation invariance.
   The direct material-kernel derivation and exterior-potential calculation
   agree on (10), and this spurious term is absent.
5. Claiming strict positivity in displacement norm is false. The result
   explicitly uses the physical density/shape quotient; relabeling nulls and
   translations remain, with no asserted positive angular frequency gap.
6. The finite l checks do not establish unbounded angular control. The
   analytic ratios and Legendre recurrence cover all l; finite tests only
   cross-check their implementations.

The proof has no external literature leaf. Its nontrivial input theorem is
the precisely pinned older joined radial construction. The new elementary
kernel/Legendre steps are derived locally rather than cited from memory.

Remaining implication: an independently reconstructed audit of equations
(4), (7) and (10), followed by a separate dynamical boundary analysis if one
wants evolution or spectral conclusions. That latter problem includes the
velocity/magnetic frame coupling and Maxwell radiation, which static
coercivity by itself does not control.
