# Radiation-density square: a conditional kinetic repair with positive UV acoustic speed

The shift-symmetric square Delta L=Z(rho_r)[X-B(rho_r)]²/2, using the scalar radiation density rho_r=3lambda Y², avoids the dust-density square's negative short-wavelength sound speed. Its full constrained nonzero high-p branch is

    omega_r²/p² -> R_r/[2(C_r+DeltaSigma b_r²)] >0,
    DeltaSigma=Zq⁴/2, b_r=4rho_r B'/q², C_r=R_r/(2c_r²), c_r²=1/3.

It can repair the clock velocity Schur coefficient only within a finite radiation capacity. A positive smooth designer Z lifts every finite-epoch mode if the strict capacity condition holds along the entire history; this condition is not automatic, and known small-radiation histories fail at intermediate epochs. Thus this is a constructive conditional quadratic door, not a completed stable cosmology or a universal cure.

## Covariant variables and exact background stealth

Retain the parent four-dimensional logKGB clock, conserved ordinary dust, irrotational radiation P(Y)=lambda Y² with lambda>0, and finite-A acceleration response kappa M a_mu a^mu-2M W(|a|;A), W=O(a³/A), kappa>0. Here X=-grad(phi)²/2=q²/2, Y=-grad(chi)²/2>0, and rho_r means the declared scalar function 3lambda Y². It is the bare radiation component's background density; after adding an interaction it must not be identified with the total interacting stress-energy density away from the trajectory.

Along the chosen FRW history rho_r decreases monotonically. Define B(rho_r) equal to X along that history. The square, Delta L_X and Delta L_Y vanish there; the background Einstein, clock and radiation equations are unchanged. Because neither scalar appears explicitly, their respective shift currents remain conserved. The added current coefficients are

    Delta L_X=Z(X-B),
    Delta L_Y=-Z(X-B)B' (6lambda Y)+O((X-B)²).

They vanish on the background and modify the coupled currents away from it. Dust remains independently minimal with conserved number/stress. Radiation and clock now interact; their bare stresses are not separately minimally conserved off the trajectory, whereas total covariant stress is conserved. The operator adds no new field or higher time derivative beyond the declared parent degrees of freedom.

As with the prior matter-square proposal, B=q_star(rho_v)² F(rho_r), Z=q_star(rho_v)^(-4)Znorm(rho_r) can preserve the algebraic action-family map phi->s phi, rho_v->rho_v-2c ln s by B->s²B, Z->s^(-4)Z. This changes explicit vacuum-parameter-dependent interaction functions. It is not automatic self-adjustment to newly added independent matter vacuum energy at fixed couplings. Designer-history and charge selection remain separate assumptions.

## Correct radiation variation and profile dictionary

Let v_r=delta chi/chidot and s_r=v_r_dot-Hv_r. The background chidot is proportional to a_FRW^-1. Hence delta Y=2Y(s_r-nu) and

    delta rho_r=4rho_r(s_r-nu),
    delta[X-B]=-q²[(1-b_r)nu+b_r s_r],
    Delta L_2=DeltaSigma[(1-b_r)nu+b_r s_r]².

The density is a scalar kinetic density, not a Schutz coordinate-density momentum. No shift perturbation or spatial radiation derivative appears at first order, so the square changes velocity/lapse terms, not the quadratic gradient potential. It has no dust pi² term. Its background-stealth first derivatives ensure second-order variations of X,Y do not contribute quadratically, and Z' is likewise absent there.

A sign and factor are loadbearing. Since q is proportional to a_FRW³(h-1), rho_r is proportional to a_FRW^-4, and X=q²/2,

    b_r=-qdot/(Hq)=-(3+h_ln_a/(h-1)).

There is no extra factor1/2. The radiation-dominated early limit has b_r->-1; the dust-dominated early limit of a small-radiation family has b_r->-3/2. Reversing the b_r convention requires reversing its definition consistently; the displayed convention gives the plus b_r u term below. The root Schur audit's initial sign/profile-factor errors were corrected in its main_c revision before the present evidence was pinned.

## Full constrained velocity form and global capacity

The square does not change the exact shift equation

    nu=d zetadot+rho_d v_d/(2Theta)+R_r v_r/(2Theta), d=M/Theta.

The lapse equation still solves the shift Laplacian with nonzero -2Theta coefficient. Dust's canonical density equation remains v_d_dot=nu. Thus there are still three scalar pairs, not an extra lapse constraint eliminating a mode.

In the velocity sector put u=v_r_dot-d zetadot. The original form plus the square is exactly

    A_old zetadot²+C_r u²+DeltaSigma(d zetadot+b_r u)²,
    A_old=3M+(Sigma+kappa M p²)d².

The radiation diagonal is C_r+DeltaSigma b_r²>0. Its velocity Schur complement is

    A_new=A_old+DeltaSigma d² C_r/(C_r+DeltaSigma b_r²).

This is a Hessian Schur operation, not algebraic removal of the propagating radiation mode. Define A0=A_old(p=0) and Lcap=C_r d²+A0 b_r². Wherever A0<0, a finite positive square lifts the clock coefficient iff

    Lcap>0,
    DeltaSigma> -A0 C_r/Lcap.

At equality Lcap=0 the finite positive square cannot suffice. Where A0>=0, Lcap>0 automatically and any strictly positive square helps. Once A_new(p=0)>0, the unchanged positive kappa M p²d² term makes it positive for every finite p.

There is an explicit smooth construction conditional on Lcap>0 at every finite epoch: choose any fixed DeltaSigma0>0, put T=-A0 C_r/Lcap, and set

    DeltaSigma=(T+sqrt(T²+DeltaSigma0²))/2.

This exceeds max(0,T), so the numerator A0 C_r+DeltaSigma Lcap is positive. All quantities are smooth along a finite-epoch history and rho_r is monotone, hence this defines a smooth function of rho_r and Z=2DeltaSigma/q⁴. This proves existence of a designer kinetic lift under the global strict capacity assumption; it does not prove that assumption for all histories. Endpoint regularity at a_FRW=0 or infinity, extension of the action to Y=0, and a uniform EFT cutoff are separate obligations.

On the parent upper branch A0=-3M eta(h-1-eta)/(h-eta)², C_r=12M H_star² eta r, d²=1/[H_star²(h-eta)²]. The condition is

    4r>(h-1-eta)b_r².

The independent root radiation_schur_bound report proves that sufficiently small positive radiation fractions fail this condition at some intermediate finite epoch for every fixed eta>0. Its corrected main_c example eta=.5, r_fold=.0001, a/a_fold=.5 has capacity ratio .0030241085<1. At the same epoch r_fold=.25 gives9.6443221>1, which is only a pointwise illustration, not a global proof. The early radiation and fold limits pass while an intermediate epoch can fail; endpoint checks alone are insufficient.

## Raw quadratic action and full high-p characteristic

Start from the actual parent action per a_FRW³,

    -3M zetadot²+S nu²+6Theta nu zetadot-2Theta nu t+2M zetadot t
       +M p²zeta²+2M p²nu zeta+3rho_d zeta nu
       +pi(v_d_dot-nu)-rho_d p²v_d²/2+rho_d v_d t
       +C_r(s_r-nu)²+3R_r zeta s_r-R_r p²v_r²/2+R_r v_r t
       +DeltaSigma[(1-b_r)nu+b_r s_r]²,

where S=Sigma+kappa M p² and t=Delta beta/a_FRW². Eliminate lapse and shift with their actual equations; retain pi as a first-order canonical dust density. The Fourier Euler matrix uses coordinates (zeta,v_d,v_r,pi), including the antisymmetric single-time-derivative terms. Its determinant has six frequency roots, representing three scalar pairs.

For omega=p x, the leading full characteristic is

    det E=-[2kappa M³/Theta²] p⁸ x⁴
                            [2(C_r+DeltaSigma b_r²)x²-R_r]+O(p⁶).

The exact script extracts this coefficient from all determinant permutations of the raw reduced matrix. It does not reuse a vacuum sound-speed formula. Matter momentum in the shift and the full s_r=v_r_dot-Hv_r normalization are retained. The sole nonzero principal squared speed is

    x_r²=R_r/[2(C_r+DeltaSigma b_r²)]>0.

Unlike the dust-density square, no negative x² proportional to a dust compressibility appears. The x⁴ zero represents slower clock/dust modes, whose dynamics are not settled by this acoustic result. In a regular finite-epoch EFT admitting H and other coefficient rates <<p<<cutoff, this is a positive acoustic principal symbol; it does not establish all frequencies, interactions or nonlinear stability. A large square reduces the acoustic speed and changes the radiation perturbations, so it is not observationally neutral.

An exploratory attempt to expand the entire generic determinant was computationally inefficient and was interrupted. Exact coefficient convolution over the finite determinant permutations supplies the decisive bounded calculation instead. Frozen numerical coefficient controls approach the positive acoustic root; they are algebra tests, not actual cosmological transfer calculations.

## Actual slow large-p system: background derivatives are essential

Freezing background coefficients is justified for omega of order p, but not for the x=0 branches with omega of order H. In particular a_FRW³p² has logarithmic derivative H, and d varies. Dropping these derivatives can produce a spurious finite-frequency tachyon conclusion.

For bounded slow solutions scale pi=p²P and define

    Rcal=2kappa M nu+2M zeta-P.

Dividing the action by p² gives its leading slow part with volume weight a_FRW³p²:

    M kappa nu²+M zeta²+2M nu zeta-rho_d v_d²/2-R_r v_r²/2
                                                  +P(v_d_dot-nu).

The finite square and radiation time-kinetic terms are lower order in this sector. Radiation's slow velocity is algebraic, v_r=Rcal/(2Theta). The exact leading time-dependent four-state system is

    nu=(Rcal-2M zeta+P)/(2kappa M),
    zetadot=[nu-rho_d v_d/(2Theta)-R_r Rcal/(4Theta²)]/d,
    v_d_dot=nu,
    Pdot=rho_d Rcal/(2Theta)-rho_d v_d-H P,
    Rcal_dot=2M(zeta+nu)/d-(H+d_dot/d)Rcal.

Here d_dot is the first time derivative of d, not its second derivative. The action verifies each equation including the H volume terms. The radiation square does not change this leading slow operator at finite DeltaSigma. Thus it does not by itself repair any instability that this operator might have on an actual intermediate background; that requires a separate nonautonomous evolution analysis.

The following is an ordered limit: first the high-p slow-sector asymptotic system, then its late-background coefficient limit. It is not the actual late-infinity evolution of a fixed comoving k, whose physical p=k/a_FRW redshifts to zero.

As a useful exact check, the late background coefficient limit with kappa=1, rho_d,R_r->0, H->H_star, d->1/[H_star(1-eta)], 0<eta<1, has rates

    0, -H_star, -eta H_star, -(1-eta)H_star.

For arbitrary finite kappa>0 the exact late characteristic is lambda(lambda+H_star)[lambda²+H_star lambda+eta(1-eta)H_star²/kappa]; its two clock roots have negative real parts when0<eta<1. There is no positive rate in this ordered coefficient limit. The zero is the formal surviving dust-velocity coordinate; the limit does not establish a propagating physical dust degree at exactly zero background density. This is a late coefficient check, not an intermediate-epoch stability theorem or an endpoint action-regularity proof.

## Physical limits and evidence

This is a covariant two-scalar density coupling and a formal fluid radiation model, not a photon distribution, neutrino hierarchy, baryon collision term or recombination model. The source law, matched accelerated clock branch and nonlinear cosmological completion remain untested. The family-map construction does not select a0/H, C or32pi. The same finite-A acceleration response still needs a separate normalized covariant vacuum/force bridge.

checks.py verifies the correct density square and profile factor, exact constrained velocity Schur, conditional smooth threshold construction, canonical dust pair, full acoustic determinant, actual leading slow action and late rates. It reports 27 assertions and three intended negative controls (wrong square sign, missing profile factor2, or importing the dust instability into this radiation square). Bound numerical acoustic roots are not interval-certified. Universal algebra follows from the derivation, not sampled output.

Primary inputs are the previously authenticated parent logKGB/ADM/Schutz action and the independently declared P(Y)=lambda Y² model; no external theorem identifying it with actual photons is invoked. SOURCES/provenance and fresh standard manifests pin exact versions/hashes, including the corrected root capacity report. No dust-square or parent evidence was modified.
