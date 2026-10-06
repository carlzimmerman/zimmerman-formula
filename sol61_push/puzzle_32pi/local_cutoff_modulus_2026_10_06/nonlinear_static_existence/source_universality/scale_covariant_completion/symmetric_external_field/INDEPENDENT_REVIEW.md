# Independent symmetric external-field audit

Primary verdict: **proved as written for the declared admitted NR constant-external-field branch and its linear Green operator**. No blocking mathematical correction found. The interpretation is conditional on that branch and, for a nonlinear body's far-zone monopole, on existence of its matched inner solution. This does not prove a global covariant vacuum/source theory, body likelihood, Cassini quadrupole, kinetic health, or coefficient selection.

## Exact objects and dependency scope
Reviewed REPORT.md SHA256 ad34e20ad62b9a0e2b30ebddf14a5f6025a69053e98915d86bde5486cb2adc94 and checks.py SHA256 80e2242971676ff353082be69e0d77ac5b6bd1d1386c07f1068065f16161f930, without editing or executing the author's script. Parent repaired radial-only covariant dictionary is pinned at66e0b0104c2064a942387a10552d649e371105dfb1fc857b4ebe0422e6de8ef2. The action uses the averaged inverse-metric invariant, not the unsymmetrized primary action. Its NR equations, auxiliary stationarity and admitted local inverse are hypotheses/parent dependencies; the tensor vacuum extension remains unresolved elsewhere.

The proof chain here is: actual sum/star source equations → eliminate the auxiliary on its admitted finite positive branch → differentiate the total constitutive flux → anisotropic elliptic Green operator and source charge → physical half-sum observable → analytic small-y stationarity expansion → angular coefficient → audited scaled moment inequality. None of these arrows identifies the nonspherical constitutive coordinate y with an independently observed external Newton acceleration.

## Raw source and total auxiliary variation reconstructed
The two NR metric-potential equations add to Δ(φ+hatφ)=ΩGnρ and subtract to div[μ(x)∇φ*]=ΩGnρ. With decaying perturbation boundary conditions the sum perturbation is the ordinary Newton Green potential, so δφ=(δφ*+δΦN)/2. An external sum gradient can remain an independently supplied boundary datum.

On the stationary branch x=y(1+2e), μ=y/x and q_T=λT. Differentiating q_T/T=4∫_0^y t³b(t)/(T²+t²)² dt=λ gives exactly

T_y=y³b(y)/[4T(T²+y²)² I3],
I3=∫_0^y t³b(t)/(T²+t²)³dt,
E_T≡yT_y/T=y⁴b(y)/[4T²(T²+y²)² I3].

Thus, with δ=(y/T)²,
D=d[y(1+e)]/dy
 =1+[b+yb_y]/(1+δ)−2bδ(1−E_T)/(1+δ)².
The author's numerical E_T is this expression after t=yv, T=U y^(7/8). Its denominator factors and powers agree. Holding T fixed would remove the E_T term and is a changed operator, not the fully eliminated response.

At a supplied finite constant star gradient, linearization gives A_ij=μδ_ij+xμ_x n_i n_j. Because x_y=2D−1, its longitudinal eigenvalue is d(μx)/dx=dy/dx=1/(2D−1), while transverse eigenvalues are μ. Hence h=1+L=1/[μ(2D−1)] and the stated admitted branch is elliptic. This is a static source-operator statement, not a relativistic kinetic-energy verdict.

## General-n Green normalization and physical force
For n≥3 let rtilde²=R²+z²/h. The map z=sqrt(h) ztilde makes A_ij∂i∂j=μΔtilde and transforms the source delta by1/sqrt(h). Since Δtilde rtilde^(2−n)=−(n−2)Ω delta, the unique decaying point Green function is

δφ*=−Gn m/[(n−2)μsqrt(h)] rtilde^(2−n).

This verifies both the n−2 coefficient and the determinant/Jacobian factor. Flux across an ellipsoidal Gaussian surface is ΩGn m; omitting sqrt(h) would change source charge. A distributional point Green function is not an exact nonlinear point-body solution. At a nonlinear body's far-zone it is the leading mass monopole only if the inner/global solution and external-dominated matching exist.

Taking the half sum with the ordinary Newton Green function gives the report's E_n(u). Homogeneity of degree2−n makes its radial-force enhancement equal its potential enhancement at fixed angle; angular force is nonzero off the axes. On the axes,
E_perp=[1+1/(μsqrt(h))]/2,
E_parallel=[1+h^((n−3)/2)/μ]/2.
Only n=3 reduces the parallel value to1+e. In general n the deep normalized angular shape is (2−u²)^−(n−2)/2; the report correctly confines its coefficient B and the quoted perpendicular/parallel ratio to n=3.

## Analytic low-field coefficient reconstructed
Set ε=y^(1/4), U=T/y^(7/8). Splitting b(yv)=sqrt(1+yv)/sqrt(yv)−1 in the exact stationarity integral gives precisely the report's rescaled integral. At ε=0 it gives λU⁴=8/7 and K=(8/(7λ))^(1/4). Differentiating the implicit equation there yields
4λK³ U'(0)=−16/(11K²),
U'(0)/K=−7/(22K²).
Since A=K^−2=sqrt(7λ/8), this is the stated U=K[1−7Aε/22+O(ε²)]. Integrals are over a finite interval with denominators bounded away from zero for U nearK; therefore the analytic implicit-function argument justifies differentiating the resulting series.

Consequently x=2sqrt(y)[1−Aε+O(ε²)], μ=sqrt(y)[1+Aε+O(ε²)]/2 and x_y=y^−1/2[1−3Aε/2+O(ε²)]. Their product gives h=2[1+Aε/2+O(ε²)]. In n=3,
E_perp/E_parallel=(μ+h^−1/2)/(μ+1)
 =2^−1/2[1−Aε/4+O(ε²)].
Thus B=A/(4sqrt2), B²=7λ/256. This is an actual differentiable expansion; merely differentiating the parent's unspecified little-o force remainder would have been insufficient.

## Moment bound and primary control
Independently reconstructed the parent scaled-moment argument: Bλ(v)<1/(2v), the stationary root wλ(v)<w0(v), and w0=J(z), v=zJ(z), J=arctan z−z/(1+z²). An integrable uniform majorant gives λC→½∫dv/[1+(v/w0)²]. The three terms after the z substitution are π²/16,−1/4,+1/4; hence0<λC<π²/16, sharply approached as λ→0. Multiplying by7/256 gives exactly0<CB²<7π²/4096 with the stated limit. No offset or λ fixing follows from this strict inequality.

The QUMOND comparison is a distinct action. Independently opened the exact primary [Milgrom, arXiv:0911.5464v2](https://arxiv.org/pdf/0911.5464v2), sections5.1–5.2, equations63,67–69 on2026-10-06. Its source operator and inverse-function notation agree with the report's translation. From that operator directly, the three-dimensional Green response is −Gn mν/r[1+(K/2)sin²θ], including the distributional monopole charge; K→−1/2 gives3/4. The symmetric candidate's1/sqrt2 cannot be replaced by that control. This source check does not authenticate or import a Cassini likelihood. No new primary-paper copy was saved.

## Computation audit and independent spot reconstruction
All four current manifests were independently validated with the installed computation-audit validate_manifest.py and --root against current bytes: main_a26/26, control_Ty_a24/26, control_QUMOND_a24/26, control_charge_a25/26. The failures are exactly the declared angular-coefficient, deep-angular-limit and source-charge assertions. Contract pins REPORT itself and no author input changed during this review.

The code's rescaled bisection stationarity equation, rescaled E_T, exact derivative and finite-difference D checks agree with the raw integrals above. Independently evaluated the original unscaled I2/I3 integrals at the stored λ=.01,y=.01,T datum (40-digit mpmath, no import of author functions): stationarity residual2.7352e−24, E_T difference2.7170e−23 and D difference1.8976e−22. The published T and response numbers are rounded to22 significant digits, consistent with these residuals. This spot audit corroborates the implementation; it is not an independent rerun or interval certification of every45-digit root. The finite assertion is seven declared branch points and exact symbolic identities; the analytic proof supplies the broader n/low-field statements.

All requested obligations pass within scope. The first missing physical implication is an actual external host/body covariant solution fixing the environmental star and sum fields and admitting a nonlinear body interior, followed by a derived observable likelihood. Static ellipticity and this local angular prediction do not repair the separately identified vacuum tensor/auxiliary regularity issues or select the target coefficient.
