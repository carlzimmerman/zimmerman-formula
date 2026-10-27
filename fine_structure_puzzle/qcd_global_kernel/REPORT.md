# FSP-008: full kernels and global vacuum response

**The physical ratio R(alpha)=A_rho(alpha)/m_p(alpha)^3 and alpha remain uncalculated.** No value of alpha, cosmological coefficient or target mass ratio was fitted. This phase calculates additional complete sectors and supplies an exact estimator for the missing sea contractions. These sectors have declared theories and regimes; their numerical results are not added together as if they were a full QCD answer.

## What changed at the missing proton kernel

The [proton calculation](proton_kernel/REPORT.md) derives the full elastic/Born tensor and its photon angular integral, including T1, T2 and the non-pole Born subtraction. A subtraction-function moment alone is insufficient. Omitting the Born subtraction creates a spurious first recoil term in the small-photon-momentum kernel.

For a unit-charge physical proton, conditional on massive-QCD low-energy analyticity and the stated current/state conventions, it obtains the universal finite soft-band coefficient

lim_(epsilon->0) M_u(0<Q<epsilon m)/(epsilon m)=1/(4pi^2), u=e^2.

This fixes an actual endpoint of the physical kernel. The full photon integral still needs the finite-momentum elastic/non-Born tensor, all sea contractions and finite mass/strong matching. The soft Q cutoff is an integration prescription in a flat mass calculation, not the sphere curvature H.

In the separate, exactly specified point-Dirac reference theory, the entire all-momentum integral with a doubly Pauli-Villars photon is calculated. The [finite-matching supplement](proton_kernel/DIRAC_MSBAR_MATCHING.md) also evaluates its dimensional Feynman-parameter integral and regulator conversion, including the evanescent numerator. It gives M_u/m=[4+3log(mu^2/m^2)]/(16pi^2), with no measured alpha or fitted form factor. The elementary matching coefficient cannot be substituted for a QCD counterterm.

A new primary 2026 photon-factorization paper supplies a useful regulator and computational method. Its actual data are HVP, not the proton, and exclude counterterms. A subsequent [primary-data acquisition](proton_elastic_data/INPUTS.json) succeeds on a different source: [Alexandrou et al., 1812.10311v2](https://arxiv.org/abs/1812.10311v2), Table VI/Appendix B, with 19 nonzero-Q-squared proton electric/magnetic pairs. These are published lattice points with light disconnected current insertions, not a fitted dipole or z-expansion curve. Their Nf=2+1+1 sea does not mean strange/charm electromagnetic current insertions were calculated. The source's physical mass scale is an input, not a new mass prediction. Full joint covariance, continuum control, non-Born amplitudes, omitted flavors, infrared/ultraviolet ranges and finite QCD matching remain absent from this finite-data calculation. This acquisition supersedes only the earlier search limitation, not the full-tensor obligation.

The [executed finite-data functional](proton_elastic_data/REPORT.md), a composite trapezoid in z=Q/(2m_ref) over 0.057<=Q^2<=0.963 GeV^2, gives

I_tab=0.00252299 per u=e^2,
I_dispersive=0.01377245, I_Born-subtraction=-0.01124946,
4pi I_tab=0.03170486 per alpha.

No numerical alpha was inserted. This is evaluation of a declared finite source-point functional; an error-bounded continuum integration cannot be inferred from 19 rounded values. The conditional linearized statistical standard-deviation ceiling from the printed marginal errors is 0.00070001 per u at fixed Q-squared and source mass. It is not an inferred joint covariance, confidence interval, nonlinear or total physical uncertainty. Published ground-state extraction and empirical lattice scale setting remain imported inputs, so this is a data-derived partial response, not a parameter-free prediction of the complete proton. The large cancellation also explains why computing only the dispersive term would be misleading.

## Completing the sea insertion algebraically

The [flavor route](sea_flavor/REPORT.md) derives the normalized-correlator Hessian before imposing vacuum charge-conjugation symmetry. With delta=ms-ml and T_a=Tr(S_l S_s V_a), the exact 2+1 sea kernel is

C_ab^sea=Cov(B,5h_l,ab/9+h_s,ab/9)
  +delta[Cov(B_a,T_b)+Cov(B_b,T_a)]/3
  +delta^2 kappa(B,T_a,T_b)/9.

The first term is the same-loop current pair. The next two are the valence-sea and separate-loop classes absent from a same-loop moment. The resolvent identity is exact at the actual strange/light masses on a common regulator; no small-delta truncation is required. Its explicit delta and delta^2 factors do not provide a small physical-mass error bound. The method overlaps with known split-even estimators, explicitly credited to the corrected May-2026 source version.

The route gives a corresponding full leading vacuum insertion and its metric derivative, with photon-kernel, action, current and measure contacts. It also derives a [measurable residual bound](sea_flavor/RESIDUAL_BOUND.md) in terms of actual gauge variances and cumulants. No such variances have been supplied, so the bound is not assigned a numerical physical error. The exact finite-matrix determinant benchmark verifies the decomposition and noise/cumulant bookkeeping; it is not a new QCD ensemble.

Independent review isolates a [normalization restriction](reviews/kernel_flavor/NORMALIZATION_CORRECTION.md). The fixed-source normalized Hessian is exact in general. Directly convolving that Hessian with a free photon is the full integrated derivative when the one-current vacuum means vanish, as in the intended charge-conjugation-invariant QCD family. If they do not, photon integration requires the additional term G_ab C_a <L_b>. The unconditioned vacuum insertion uses the uncentered product <L_a L_b>. The frozen author files and the reviewer's preliminary generic formula are preserved with this explicit correction; no physical number is changed.

## Direct global sphere calculation

The [sphere route](sphere_chiral/REPORT.md) evaluates the full one-loop pion determinant and its fixed-parameter metric derivative on round S4, using all scalar harmonics including the massive constant mode. This extends the [FSP-003 direct determinant](../qcd_prediction/coordinator/curved_pion/DERIVATION.md), which already supplied the minimal-pion heat coefficients, leading H^6 term and zero linear-H coefficient. The new calculation supplies a closed finite-radius stress/resolvent/digamma expression, general xi dependence, isolated k15 response and direct W/metric/charge checks. It also goes beyond FSP-007's different flat two-point observable. A common decoupling subtraction removes local heat terms through R^2; there is no radius or alpha fit.

For one neutral and two charged real pion modes with M_ch^2=M^2+2uC/F^2, its leading positive-mass low-curvature stress is

rho_pi,mass=37H^6/(2016pi^2) [1/M^2+2/(M^2+2uC/F^2)]+O(H^8).

The actual finite-radius answer is an exact digamma or absolutely convergent spectral expression, not this truncated asymptotic formula. The isolated zero-charge mass and curvature-coupling slopes are

partial_u rho|mass=-37 C H^6/(504pi^2 F^2 M^4)+O(H^8),
partial_u rho|k15=29 k15^r H^6/(20pi^2 M^2)+O(H^8).

M,F,C and k15 remain explicit independent matching inputs; photon loops and additional charge responses are not removed by choosing them. The positive-mass uniformity argument includes the differentiated remainder, giving A_pi=partial_u A_pi=0 in this sector. An independent local gravity R^3 term can shift the full H^6 coefficient. The massless Gaussian zero mode is singular and does not provide the nonlinear chiral-limit answer. Neither the one-loop calculation nor its uniformity proof establishes the corresponding statement for every global QCD sector.

## A second evaluated global regime

The [coordinator calculation](coordinator/UV_SPHERE.md) uses primary global two-loop gauge-theory vacuum diagrams on a small sphere, rather than a flat momentum substitution. In the declared massless three-flavor weak-coupling SU3-plus-photon theory it obtains

rho_UV/H^4=219/(320pi^2)+(u-27g^2)/(64pi^4)+O(g^4,u^2,ug^2).

The leading electromagnetic metric-response slope is H^4/(16pi^3) per renormalized alpha at fixed g and mu. Here alpha is the source's renormalized coupling at mu, with u=4pi alpha; the physical Thomson-limit charge and massive thresholds have not been matched by this massless weak-sphere computation. Gauge-volume normalization, the signed fermion graph and UV counterterms are included. A finite coupling-dependent Euler convention changes RG bookkeeping together and contributes no fixed-parameter metric derivative on S4. The logarithmic coefficient is checked independently using the one-loop beta coefficient; no numerically reconstructed radius-independent constant enters this stress.

This high-curvature regime cannot be continued through confinement into the small-H limit by assumption. Its H^4 term and the low-energy pion H^6 term are controlled calculations in distinct regimes, not a reconstruction of the missing interpolation or nonperturbative global remainder.

The [independent global review](reviews/global_sphere/REVIEW.md) found printed inconsistencies between individual fermion equations and the total in the non-Abelian source. Its [source correction](reviews/global_sphere/SOURCE_INCONSISTENCY.md) explicitly resolves the used coefficient through the consistent total/RG identities and a separate primary QED exact Gamma expression. The individual printed equations are not counted as independent corroboration. The scoped pion and weak-sphere formulas survive this check; the source narrative must be read with that correction.

## The physical ratio still requires a global coefficient

The normalization fixes what a genuine linear-H term would mean. For V=Omega/H^4 and rho=-H partial_H W/(4V), rho=A H requires a subtracted W contribution 4Omega A/(3H^3). Neither a known flat current moment nor the evaluated sphere loop terms supplies that coefficient. Once A and its common-path charge derivative exist, the quotient obeys R_u=A_u/m^3-3A m_u/m^4. The complete sea estimator and full photon kernel identify how to calculate m_u and A_u, but are not their unevaluated expectation values.

The [global-state discriminator](global_state/REPORT.md) tests an explicit possible source of the required H^-3 action. A forced equatorial wall of tension sigma produces A=9sigma/16 in its defined partition model. Summing that positive-tension sector with the same curved no-wall background instead exponentially suppresses its population, giving zero additional A and zero differentiated charge coefficient under stated uniform bounds. An exactly evaluated critical endpoint shows how first charge differentiation and the radius limit can fail to commute. This establishes a concrete state/measure obligation for that mechanism; it neither calculates physical QCD wall tension nor excludes an unknown A already in the bulk background. The pure-area equator also has an unstable displacement mode.

The compact chiral Haar/Dashen integral and its canonical Gaussian normalization were also already evaluated in [FSP-003](../qcd_prediction/controlled_model/qcd_zero_modes/REPORT.md). The first FSP-008 dispatch into this subproblem overlapped that ancestor. Work was redirected before a redundant base-integral run: the actual continuation is its exact-over-Gaussian replacement and the first constant/nonconstant pion interaction with curvature matching. Reconstructed prior formulas are not counted as new results.

The [new matched calculation](chiral_zero_mode/DERIVATION.md) executes that continuation. For x=F^2 M^2 V, y=uCV, g=Gbar/F^2, m=<a0>, q=<s>, the nonconstant-pion contraction shifts the compact source variables and adds an essential constant factor. When a full massive Gaussian determinant is already present, the genuine additional mixed term is

delta W_extra=g[(3x/2)(m-1)-4yq].

The aligned term g(3x/2+2y) must first be subtracted because it is already in that determinant. Exact finite-charge metric derivatives include covariance and third-cumulant terms; the differential response need not have a fixed sign. This supplies an actual correction function, with no numerical alpha assigned.

The S4 nonconstant tadpole has the curvature pole R/(96pi^2 epsilon) in d=4-2epsilon. In an explicitly defined zeta prescription its finite part is H^2[log(mu^2/H^2)+2gamma-8/3]/(8pi^2). That finite constant is not a physical matching condition. Curvature-mass and curvature-electromagnetic operators occur at the same epsilon order, and the convenient tadpole scheme has not been equated to the massive determinant's decoupling scheme.

The [independent curvature-basis audit](reviews/curvature_matching/REPORT.md) identifies a further unresolved step. Reading only the constant-background potential gives different partial pion curvature residues in geodesic and plain sigma coordinates. An explicit local field redefinition accounts for their difference but also generates derivative/kinetic and metric-source partners. Neither partial potential residue is the full published k15 running. This is an incomplete common off-shell/operator-basis transfer, not an established error in the primary paper. Inserting the published beta into the partial pion formula would not establish a common renormalized NLO calculation.

## The next photon contribution

The [photon continuation](epsilon_photon/DERIVATION.md) calculates the first nonconstant photon contribution around the compact chiral orientation. For s=a1^2+a2^2 the quadratic gauged kinetic term gives m_A^2=uF^2 s. For each nonconstant scalar eigenvalue lambda, the longitudinal-photon/pion block has determinant lambda^2/xi_g, independent of m_A. Its seagull and two mixing insertions cancel exactly. On closed S4 the transverse mixing vanishes by integration by parts; the transverse determinant remains. Ghost primes, the collective pion mode and the global U1 quotient are kept explicit.

The transverse Hodge spectrum is lambda_l=H^2(l+1)(l+2), d_l=l(l+3)(2l+3)/2. Its zeta residue at one is -1 and its finite part is 2/3-2gamma. Thus the declared zeta-scheme tadpole is H^2[-log(mu^2/H^2)+2/3-2gamma]/Omega, with Omega=8pi^2/3. This gives a calculated orientation correction delta W_gamma=t q, where q=<s> in the compact distribution and t=uF^2 V T_gamma/2, supplemented by its same-scheme curvature LEC. The metric and charge derivatives include the covariances and third cumulants of that distribution; treating q as a fixed constant would miss them.

The curvature pole reproduces the photon-only beta15=1/2 in the stated dimensional convention. It does not resolve the separate pion-Z basis transfer. The orientation-independent part of that counterterm requires a source-only gravitational contact; its finite matching is not determined by the orientation loop. The free Maxwell determinant and global normalization also cancel from the orientation ratio but contribute to absolute vacuum response. These calculations therefore supply additional actual sectors and source derivatives, with no fitted alpha, while leaving the complete NLO partition and the nonperturbative global coefficient open. Strict epsilon counting does not authorize the fixed-positive-mass/charge H-to-zero limit.

Independent reviews, their exact scope and corrections are [reconciled separately](reviews/RECONCILIATION.md). Open continuations include the complete physical tensor/covariance plus finite matching, and unconditioned common-theory sphere partition/stress data with continuum/radius control. The global nonperturbative remainder is still a physical calculation, not a coefficient to fit to obtain 137.
