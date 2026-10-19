# FSP-003: calculating the QCD route without a target fit

**The requested physical ratio and a value of alpha remain uncalculated.** This phase obtained explicit QCD+QED infrared responses, a relation in which their leading unknown electromagnetic constants cancel, a direct four-dimensional pion-vacuum calculation, and a complete static spherical fluctuation determinant in a declared semiclassical comparison. It also found a normalization error in the particular Schwinger-model argument used to support an inverse-size vacuum effect. These results narrow the physical calculation; they do not establish or refute every possible QCD cosmological response.

All calculations and source reviews are under this folder. No observed alpha, dark-energy density or chosen numerical matching coefficient was used to tune the results below. The frozen framework and earlier scientific artifacts are unchanged. The original [target](../TARGET.md) remains open.

## 1. The ratio that still needs to be calculated

In natural units, define a specified, subtracted gravitating vacuum response by

\[
\rho(H)-\rho(0)=A_\rho H+o(H),\qquad
A_\rho=c_H\Lambda^3,\qquad m_p=C_p\Lambda.
\]

The desired dimensionless quantity is

\[
R(\alpha)=\frac{A_\rho(\alpha)}{m_p(\alpha)^3}
=\frac{c_H(\alpha)}{C_p(\alpha)^3}.
\]

This definition requires a state, geometry, regulator, subtraction, quark/charge matching and controlled small-H limit. Existence of a nonzero linear term is a hypothesis to test. The proposed cosmological branch would obey \(\bar H=(8\pi G/3)A_\rho\). Substituting the measured cosmic scale to assign \(A_\rho\) and then calling the resulting equation a prediction would fit the missing coefficient.

We did not evaluate the four-dimensional generating functional needed for \(A_\rho\), nor calculate a complete matched individual-proton response. Thus no numerical curve \(R(\alpha)\), slope on the fixed-proton-mass path, or isolated alpha root has been obtained.

## 2. A constructive result: an unfitted infrared response relation

The same charged-pion electromagnetic parameter enters two different physical sectors. Let \(M\) be the positive pion mass coordinate of the zero-charge two-flavour reference theory. Hold the strong reference theory, strange mass and light-quark mass ratio fixed in a chirally regular mass-independent matching prescription. Take the charge derivative at \(e^2=0\) first, where \(e^2=4\pi\alpha\).

Define

\[
V(M)=\left.\partial_{e^2}\log\chi_{\rm top}(M,e^2)\right|_0,
\qquad B_p(M)=\left.\partial_{e^2}m_p(M,e^2)\right|_0.
\]

The calculated leading terms are

\[
V=K_\chi^r-\frac{Z_0}{8\pi^2}
 [1+\log(M^2/\mu_\chi^2)]+\cdots,
\qquad
B_p=L_p-\frac{3g_0^2Z_0M}{16\pi}+\cdots.
\]

Here \(K_\chi^r\) and \(L_p\) are independent unknown local matching constants; \(Z_0\) is the charged-pion mass-shift constant and \(g_0\) the chiral-limit axial nucleon coupling. Differentiating the mass shapes removes both local constants:

\[
D_\chi=\partial_{\log M^2}V=-\frac{Z_0}{8\pi^2}+\cdots,
\qquad D_p=\partial_M B_p=-\frac{3g_0^2Z_0}{16\pi}+\cdots.
\]

Consequently, for nonzero \(Z_0g_0\),

\[
\boxed{\lim_{M\to0^+}\frac{D_p}{D_\chi}
=\frac{3\pi}{2}g_0^2.}
\]

This is a genuine leading infrared prediction with no fitted electromagnetic constant. It connects the electromagnetic mass dependence of vacuum topological susceptibility to that of an individual nucleon. The limit assumes the ordinary termwise differentiable chiral expansion, with the other integrated-out hadrons retaining nonzero gaps; it is not an all-orders nonperturbative theorem. It follows from the stated chiral theory; novelty is not claimed. Replacing the susceptibility normalization by its exact zero-charge value changes only higher chiral orders.

An improved version uses \(L=M^2\partial_{M^2}\), \(D_\chi^{\rm imp}=L(1-L)V\) and \(D_p^{\rm imp}=(\partial_M-M\partial_M^2)B_p\). These retain the leading loop terms and also annihilate the next local analytic \(M^2\) terms. Higher-order logarithms remain; this is not an exact finite-mass identity. The charge derivative must precede the chiral limit. At fixed nonzero charge even the retained loop ratio acquires \(\sqrt{1+2e^2F_0^2Z_0/M^2}\), illustrating the noncommuting limits.

The [independent derivation](electromagnetic/mixed_chiral/INDEPENDENT_DERIVATION.md) and [coordinator derivation](coordinator/MIXED_CHIRAL_RAW.md) were saved separately before comparison. The extension includes symbolic checks and a separate scheme/limit audit. Its purpose is an unfitted QCD+QED benchmark for a future calculation. It is a different ratio from \(R\): it neither supplies \(A_\rho\) nor selects alpha, since the overall charge response cancels.

## 3. Actual alpha-dependent loop functions, and what remains independent

The [electromagnetic calculation](electromagnetic/REPORT.md) derives the charged-pion determinant and checks the baryon invariant operators. With \(\Delta=2e^2F^2Z\), the retained, unexpanded one-loop functions include

\[
\left(\frac{\delta\chi}{\chi_0}\right)_{\rm loop}
=-\frac{(M^2+\Delta)\log[(M^2+\Delta)/\mu_\chi^2]
-M^2\log(M^2/\mu_\chi^2)}{16\pi^2F^2},
\]
\[
\delta m_{p,\rm loop}
=-\frac{g_A^2}{16\pi F^2}
 [(M^2+\Delta)^{3/2}-M^3].
\]

These are calculated functions of the charge, rather than assigned linear sensitivities. They are only particular low-energy contributions. The full susceptibility includes meson counterterms; the individual proton includes \(-e^2F^2(f_1+f_3+f_2)/2\) in the stated invariant convention. Proton-minus-neutron data remove the shared pion term and isoscalar constant, so that splitting cannot determine the individual mass response.

The [fresh source and derivation review](reviews/chiral_fresh/REVIEW.md) confirms these restrictions and a printed sign/dimension inconsistency in the baryon source; our expression follows its invariant Lagrangian. The numerical values of the unknown constants were not guessed or fitted. Independent QCD matching can in principle calculate them.

## 4. A supporting inverse-size argument fails its own spectral test

For the exact metric and periods printed in Sachs–Wipf, hep-th/9508142v1, the zero Fourier slice of the massive scalar Green function is

\[
\frac{1}{2mL|\tau|}
\coth\!\left(\frac{mL\tau_0}{2|\tau|}\right).
\]

Their equation (119) instead has \(\tau_0\) in the prefactor. The two differ on a tilted torus. This is a spectral normalization error, independently reconstructed from the metric before the fresh reviewer read the disputed formula. The later Urban–Zhitnitsky 0906.2165v2 inverse-L argument inherits this discrepancy, in addition to separate printed sign/addition issues.

With the corrected scalar coefficient and the source's stated massless-Schwinger global measure, the condensate ratio is

\[
\frac{\Sigma_L}{\Sigma_\infty}
=\exp\!\left[-\sum_{w\ne0}K_0(m\ell_w)\right].
\]

At fixed nondegenerate torus shape its corrections are exponentially small, and the claimed intrinsic inverse-L term is absent. The [exact derivation](coordinator/SCHWINGER_CLAIM.md), numerical spectral checks and [fresh primary-source audit](reviews/schwinger_fresh/REVIEW.md) agree. This conclusion concerns these exact source versions, observable, geometry and massless-condensate approximation. It is not a four-dimensional QCD no-go theorem or a literature-wide novelty claim.

## 5. Going beyond zero modes: real determinant calculations

The [geometry lane](vacuum_geometry/REPORT.md) reproduces the finite-ball BPS zero-mode factor, but finds that neither the strong-coupling extrapolation nor the total physical vacuum coefficient is controlled by it. Hyperbolic boundary effects and metric variations also require separate treatment.

We then calculated omitted fluctuations rather than stopping at that objection. For a framed Dirichlet ghost channel, \(x=m_WR\), the exact static relative determinant is

\[
D_0=\frac{3(x\coth x-1)}{x^2},\qquad
\log D_0=\log(3/x)-\frac1x+O(x^{-2}).
\]

For the actual coupled spherical gauge-amplitude/\(A_4\) Hessian, an exact one-dimensional integral gives

\[
D_{\rm real}=\frac3{4x^2}
 [1+2/x+7/(2x^2)+\cdots].
\]

These use explicitly defined auxiliary comparison operators, not a completed physical-vacuum determinant. Independent eigenvalue-product and matrix-ODE checks support the formulas; the matrix comparison's maximum observed relative discrepancy was \(2.32\times10^{-13}\). The [ghost report](vacuum_geometry/determinant_followup/REPORT.md) and [coupled-vector derivation](vacuum_geometry/determinant_followup/VECTOR_BLOCK.md) specify the domains.

The calculated nonzero-mode contributions are of the same inverse-radius order as the earlier zero-mode estimate. A formal operator pairing changes Dirichlet into Robin data; it cannot justify cancellation while silently keeping both domains Dirichlet. The old global rotation mode is outside the framed ghost domain. Those initial separate scalar comparisons did not determine a complete coefficient, and cannot be added to the earlier zero-mode number to produce one.

The remaining spherical phase/radial-gauge block was calculated with an independent action/domain review. The [completed static spherical calculation](vacuum_geometry/determinant_followup/phase_block/REPORT.md) imposes tangential Dirichlet, normal divergence-zero and framed ghost data. In a common unbroken auxiliary reference its phase-plus-ghost factor is exactly \(\sqrt{\sinh x/x}\), with no residual algebraic inverse-radius terms. Combining the real block gives

\[
\mathcal Z_{J=0,n=0}^{(0)}
=\left[\frac{x\sinh^2x}{9I(x)}\right]^{1/2},\quad
\log\mathcal Z=\log(2/3)+\frac32\log x-\frac1{2x}+O(x^{-2}),
\]

where \(I\) is the explicit integral in the coupled-vector report. Independent mixed-boundary matrix integration agrees within \(8.49\times10^{-13}\). A positive near-zero eigenvalue is retained; it cannot also be replaced by an infinite-space collective-coordinate factor. All-vector Dirichlet would break the stated ghost pairing. The [independent boundary review](electromagnetic/gauge_block_review/REVIEW.md) checks the gauge complex and its limitations.

Even this completed static spherical coefficient depends on what is held fixed at the wall. Holding its physical Higgs value \(b=m_Wh(m_WR)\) fixed instead of the asymptotic \(m_W\) gives \(m_WR=bR+1+\) exponentially small terms. The residual inverse-radius coefficient then becomes \(+1/(bR)\), rather than \(-1/(2m_WR)\); the classical inverse-radius term also cancels on that path. The [explicit path derivation](vacuum_geometry/determinant_followup/phase_block/FIXED_BOUNDARY_PATH.md) separates dimensionless determinants from still-unmatched dimensionful measure factors. A universal bulk QCD coefficient cannot be assigned from either boundary path. Angular/Fourier sums, matter, physical vacuum matching and strong-coupling transport remain missing.

The coupling in this pure SU(2) semiclassical gauge problem is its Yang–Mills coupling, not the electromagnetic e. The calculation includes no electromagnetically charged quark/photon sector. Its gauge-coupling dependence cannot be relabelled as the requested physical alpha dependence. The Maxwell control's coupling is likewise explicitly a model parameter.

## 6. Controlled topology and the correct vacuum observable

An [exact compact-Maxwell calculation](controlled_model/REPORT.md) supplies a useful control. In two dimensions, topological susceptibility is nonzero but the closed-sphere vacuum energy has an exponentially small large-radius response and zero linear-curvature-scale coefficient. In four dimensions a defined flux-sector comparison on a rectangular torus is also exactly calculable; it is not the full photon vacuum or QCD. Topological sectors alone do not guarantee the proposed cosmic response.

There are two further independent requirements:

- A susceptibility measures theta curvature. Even a known geometric susceptibility coefficient determines \(A_f''(0,\alpha)\), not \(A_f(0,\alpha)\). A theta-independent contribution is invisible to that inference. This is missing information, not freedom to change a fixed microscopic theory arbitrarily. See [the explicit counterexample](coordinator/SUSCEPTIBILITY_TO_VACUUM.md).
- Effective-action density is not automatically gravitating stress. On a specified round S4, \(f=-\log Z/V\) gives \(\rho=f-(H/4)\partial_Hf\). A linear term changes by a factor 3/4. A different geometry needs its own metric variation. See [the stress derivation](coordinator/METRIC_RESPONSE.md).

The latter note provides a subtraction-free *formal definition*, not an evaluation: with \(D=H\partial_H\), \(P(D)=D(D-2)(D-4)\), a controlled differentiated asymptotic expansion gives \(A_\rho=\lim P(D)\rho/(3H)\). This removes local constant, curvature and curvature-squared subtraction terms. The electromagnetic derivative requires the corresponding curved-space current-current insertion and metric variation. No present run evaluates that nonperturbative four-dimensional observable.

A [bounded check of the existing lattice citation](vacuum_geometry/lattice_bridge_review/REPORT_v2.md) also does not close the gap. Yamamoto1405.6665v2 calculates a fermion-current response at imaginary expansion rate on a finite quenched Euclidean lattice. Its numerical coefficient is a current fit, not a vacuum-stress measurement; it supplies no electromagnetic derivative or proton matching. The citation from the newer cosmological proposal is indirect through1505.05151v2. Even a continuation of that current would not turn it into the required metric observable. This statement concerns the checked citation chain, not every later lattice calculation.

## 7. Direct four-dimensional calculation of the ordinary pion vacuum

The [curved-pion calculation](coordinator/curved_pion/REPORT.md) evaluates a genuine four-dimensional QCD infrared contribution on a closed round S4, using its exact scalar spectrum. After subtracting the constant, H² and H4 local terms, one real minimal pion gives

\[
f_{\rm res}=-\frac{74}{63}\frac{H^6}{32\pi^2M^2}+O(H^8/M^4),
\qquad
\rho_{\rm res}=+\frac{74}{63}\frac{H^6}{64\pi^2M^2}+O(H^8/M^4).
\]

For the charged pair with \(\Delta=2e^2F^2Z\), the calculated mass-shift contribution is

\[
\delta\rho_{\pi^\pm,\rm res}
=\frac{74}{63}\frac{H^6}{32\pi^2}
\left[\frac1{M^2+\Delta}-\frac1{M^2}\right]+O(H^8).
\]

For this specified determinant at every fixed positive mass, its linear-H coefficient and that coefficient's charge derivative are **zero**. This follows from a controlled proper-time asymptotic argument, with finite spectral and resolvent checks; it is not a polynomial fit to a few radii. A fresh independent harmonic/Hurwitz derivation and [source/physics review](electromagnetic/s4_pion_review/REVIEW.md) confirm the result.

This is a definite prediction about the calculated pion contribution. It is not \(c_H=0\) for full QCD. Higher-curvature chiral constants change the full finite-mass H6 coefficient; interacting photons, higher loops, non-pion matching and any proposed additional nonlocal/topological sector are outside the determinant. The hierarchy H much smaller than M must be respected. Thus the ordinary massive pion vacuum does not supply the required H term, even though its actual charge-dependent curvature response can be calculated.

## 8. Actual QCD topological zero modes and their charge dependence

The [finite-volume QCD calculation](controlled_model/qcd_zero_modes/REPORT.md) integrates the two-flavour chiral group mode and sums its fixed-topology sectors. It also includes the leading electromagnetic Dashen operator. With \(\mu=m\Sigma V\), \(z=2\mu\cos(\theta/2)\) and \(\eta=e^2C_{\rm EM}V\), its aligned-vacuum-subtracted group function is

\[
\widehat Z(z,\eta)=\int_0^1ds\,e^{-\eta s}
 I_0\!\left(z\sqrt{1-s}\right),\qquad
\widehat Z(z,0)=\frac{2I_1(z)}z.
\]

Its first charge response is explicitly

\[
\left.\partial_{e^2}\log\widehat Z\right|_0
=-C_{\rm EM}V\frac{2I_2(z)}{zI_1(z)}.
\]

The dimensionless shape is predicted without fitting. Conversion to a physical numerical charge response still needs the independently matched \(C_{\rm EM}\). At theta=0 and degenerate quark masses, the retained action obeys \(\chi=(m/2)\Sigma_V\), where \(\Sigma_V\) is the flavour-averaged condensate defined by the common-mass derivative, including this single electromagnetic operator. This is not an all-orders QCD+QED identity.

Two calculations of the measure agree. Normalized Haar integration alone has an apparent \(3/(2V)\) stress in its large-mass saddle. The canonical constant-pion coordinate contributes a Jacobian proportional to \(V^{3/2}\), canceling that term exactly at Gaussian order. The charged-pair partition ratio becomes \(M_\pi^2/(M_\pi^2+2e^2C_{\rm EM}/F^2)\), independent of radius at fixed masses and couplings; its leading effective-action shift therefore drops out of metric stress. This connects the QCD group integral to the constant mode already present in the four-dimensional pion determinant.

For a consistent resummation, multiply that full Gaussian object only by the exact group integral divided by its own Gaussian constant-mode saddle. Adding a second constant-mode determinant or a second canonical Jacobian would count the same degrees of freedom twice. Nonconstant-mode interactions still need the same chiral counting.

The controlled epsilon regime and fixed-positive-mass H tending to zero are different paths. A mass/theta-independent normalization \(N(V,\alpha)\) remains invisible to these mass/theta observables and still needs microscopic metric matching. The canonical cancellation fixes one measure component, not that entire function. Thus these explicit QCD and charge-response functions do not yet determine \(A_\rho\) or the cosmological ratio.

## Evidence and next discriminator

[Reproduction](REPRODUCE.md), [manifest validation](reviews/MANIFEST_VALIDATION.json), [review reconciliation](reviews/COORDINATOR_RECONCILIATION.md) and the [checkpoint](../checkpoints/FSP-003.md) distinguish hand derivations, source authentication and finite numerical tests. Passing symbolic checks does not establish a cosmological mechanism.

The direct physical next step is a common regulated QCD+QED calculation of the specified small-H stress coefficient and its charge insertion, with continuum, volume/state and mass matching controlled. The available semiclassical continuation now has a complete static spherical comparison, but needs the angular/Fourier mode sums and a physical reference; even that would still require a justified bridge to physical QCD. The mixed-chiral relation and curved-pion result are independent unfitted benchmarks. None of the missing quantities should be replaced by fitted constants to obtain an alpha value.
