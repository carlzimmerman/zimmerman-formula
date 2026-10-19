# Independent derivation before opening targets

Date: 2026-10-19. Reviewer: isolated child `curved_sea_review`.
At save time the target DERIVATION, REPORT, checks, lattice package, and prior verdicts have not been opened. The allowed source-path manifest alone was read. No project AGENTS.md was found on the path to the workspace root.

## Conventions and cut

Take covariantly normalized one-pion states and
`<pi^a(p1) pi^b(p2)|Theta(0)|0> = delta_ab (s+2 M^2)` at LO, with N real degenerate pion species, s=(p1+p2)^2. Define rho(s)=(1/pi) Im Pi_M(s+i0) for the connected trace correlator. Integrated Lorentz-invariant two-body phase space is beta/(8 pi), beta=sqrt(1-4 M^2/s). The identical-particle factor is 1/2!, and the discontinuity-to-imaginary-part factor is 1/2. Thus

`rho_LO(s) = N/(32 pi^2) sqrt(1-4 M^2/s) (s+2 M^2)^2 theta(s-4 M^2)`.

The species factor sums `delta_ab delta_ab=N`; no second independent factor of two for charged pions is added after the two real charged fields are counted.

## Euclidean subtraction and Hessian

Set z=q_E^2>=0 and use a positive Stieltjes kernel. The three-times-subtracted correlator obeys

`Pi_E(z)-Pi_E(0)-z Pi_E'(0)-z^2 Pi_E''(0)/2 = -z^3 integral ds rho(s)/[s^3(s+z)]`.

At an EFT upper cutoff Lambda^2 this defines only the displayed low-energy cut. It is not an assertion that the LO spectral function holds to infinity. For any differentiable real Euclidean source action, W=-log Z gives

`delta^2 W = <delta^2 S> - <delta S delta S>_c`.

Consequently the separated conformal-metric Hessian has sign minus Pi_E. Metric seagulls and local gravitational counterterms remain independent contact contributions. With g_mu_nu=exp(2 sigma) delta_mu_nu, R_linear(q)=6 z sigma(q), and W_quadratic=(1/2) integral sigma K sigma, the subtracted separated kernel is

`K_sub(z)=+z^3 integral ds rho(s)/[s^3(s+z)]`.

If the curvature term is written WITHOUT an overall 1/2,

`W contains integral sqrt(g) R F(-Box) R`,

then `F_cut(z)=z/72 integral ds rho(s)/[s^3(s+z)]`. If instead the action is `(1/2) R F R`, F is twice this quantity. This convention must be fixed before comparing coefficients. The coefficient of `R(-Box)R` is positive; that of `R Box R` is its negative. An arbitrary local R Box R term can shift the total analytic slope without changing this cut.

## Finite third moment and chiral singularity

Define `I3(Lambda,M)=integral_(4M^2)^(Lambda^2) ds rho_LO(s)/s^4`, assuming Lambda>2M>0. For N species and `v=sqrt(1-4M^2/Lambda^2)`, direct substitution gives

`I3 = N/(256 pi^2 M^2) [3 v^3 -(6/5) v^5 +(1/7) v^7]`.

Thus `Pi_E'''(0)=-6 I3` for the cut, and the slope in the no-1/2 curvature convention is `F_cut'(0)=I3/72`. Formally extending only this LO expression to infinity gives

`I3_infinity = N*17/(2240 pi^2 M^2)`,

`F_cut'(0)=N*17/(161280 pi^2 M^2)`.

At fixed positive Lambda, this gives the same leading 1/M^2 singularity; the omitted upper tail starts `N/(32 pi^2 Lambda^2)`. This leading infrared singularity is meaningful within the LO approximation. An exact full QCD curvature coefficient is not obtained by extending the EFT cut.

For a charged mass shift Delta=Mplus^2-M^2 with one neutral and two real charged species, the isolated mass contribution to the curvature slope is

`delta F_cut'(0) = 17/(80640 pi^2) [1/(M^2+Delta)-1/M^2] + cutoff/subleading terms`.

At fixed M>0 and |Delta|<<M^2 this is

`-17 Delta/(80640 pi^2 M^4)`.

For Delta=2e^2 C/Fpi^2=8 pi alpha C/Fpi^2, the alpha-linear coefficient is `-17 C/(10080 pi Fpi^2 M^4)`. The alpha expansion and chiral limit do not commute. This differentiation alone omits electromagnetic trace-vertex, wavefunction, photon cuts, and curvature-LEC effects.

## Geometry restriction

A flat-space scalar-curvature two-point form factor fixes a response around flat geometry at finite momentum. It is not a homogeneous S4 vacuum calculation. On S4, R is constant and R Box R vanishes. No step q=H, or replacement of the finite-momentum response by a global H-linear vacuum stress, follows from these formulas.
