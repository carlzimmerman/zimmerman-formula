# FSP-006: physical QCD/QED and proton matching

The physical R(alpha)=A_rho(alpha)/m_p(alpha)^3 and its constrained slope remain unevaluated. Alpha has not been derived or fitted. This phase moves from the previous controlled boundary models to actual QCD current data, an explicit matching artifact, and directly measurable curvature observables.

## A real QCD input, with its exact scope

The proton route uses the pure-QCD connected Compton subtraction data of Can et al., arXiv:2501.08619v2. The six middle-ensemble points give the alpha-free, native-unit trapezoidal stencil

(1/M) partial_(e^2) M_p^[sub,connected,window] = -876375/152571904 = -0.005744012999929529.

This denotes a declared finite-data estimator of one contribution, not an evaluated continuum integral or a complete mass derivative. It uses the SU(3)-symmetric m_pi approximately 410 MeV ensemble, one lattice spacing, and a momentum window approximately 1.44 to 9.38 GeV^2. The transform uses native momenta and aM, so it needs no alpha, hbar c, radius, polarizability, or absolute lattice-spacing input. The published lattice extraction itself uses statistical fits; no parameter here is fitted to alpha, vacuum energy, or the desired ratio.

Published marginal errors permit a covariance-agnostic upper ceiling 0.00218094 on the stencil's standard deviation conditional on fixed aM. It is not the uncertainty of a physical prediction: interpolation, omitted momentum regions, continuum/quark-mass corrections, sea currents and matching counterterms are not bounded. The full p response cannot be reconstructed from p-minus-n data. In particular, the charge algebra sum Q=0 removes single-current sea loops at the degenerate point, while sum Q^2=2/3 leaves a same-loop two-current sea contribution. That isoscalar contribution cancels in p-minus-n and survives in each mass.

The source conventions and transformation are in [the proton report](proton_compton/REPORT.md); the original table inputs and exact-run result are retained there. The newer physical-mass subtraction source is audited separately for experimental inputs and contraction coverage, rather than silently substituted as a prediction of this programme.

## The vacuum response has an explicit missing contact

The new vacuum derivation gives, at a common regulator, rho_theta_theta=-Cov(Q^2,Tcal)/(4V), where Tcal is the full integrated metric derivative of the action. Its charge response is [kappa(Q^2,I,Tcal)-Cov(Q^2,I_t)]/(4V). The metric derivative I_t of the current insertion is essential. A flat susceptibility or Q^2JJ calculation supplies neither this contact-completed quantity nor the unconditioned stress.

A sector-conditioned measurement supplies a concrete test of the theta-dependent coefficient. Under the stated uniform large-chi V saddle and differentiated remainders, X_top={8V[rho_Q=0-rho]-4}/H tends to -a_chi/chi0 if chi(H)=chi0+a_chi H+.... The known fixed-topology baseline is H^4/(2Omega4); the sought topology-sensitive correction begins at H^5 in that difference. The test does not determine a theta-independent A_rho. A flat flowed energy-momentum formula with its vacuum expectation already removed and validity only at separated insertions cannot be substituted without restoring the missing metric normalization and contacts. [The vacuum report](vacuum_response/REPORT.md) pins both that implementation restriction and the new diagnostic. The conditional sphere measurement has not been performed here.

The differentiated saddle condition includes the retained cumulant coefficients: with t=log a and B=c4/chi^2, B_t-4B must stay bounded for the stated O(H^3) contamination, in addition to control of the differentiated tail and susceptibility expansion. Pointwise bounded cumulants alone do not establish that error estimate. [Independent review](reviews/topology/REVIEW.md) gives the full retained-term formula.

Independent source review corrects the Makino–Suzuki locators in that frozen lane: the master formula is (4.70), vacuum subtraction is (2.10), and the separated-insertion/EOM restrictions are around (4.68) and section 5/(5.6), in exact v5. The physical restriction survives; see [the source correction](reviews/topology/SOURCE_LOCATOR_CORRECTION.md). The author's original citation record is retained rather than silently changed.

## A false linear vacuum signal from proton calibration

In QED_L on infinite time times a cubic spatial torus, the established leading proton mass correction is delta m_p=alpha c1/(2L), c1=-2.83729747948..., for unit charge. An independent Ewald evaluation checks the shape constant. This is the specified finite-volume photon prescription; it is not a curvature coefficient on S4.

Let ell=log Lambda, and hold the chosen quark-mass definitions fixed. Retuning ell(L) to hold this finite-volume proton mass fixed gives

delta ell=-alpha c1/[2L partial_ell m_p].

If vacuum stress at the retuned parameters is compared with a fixed original flat-space theory, its flat baseline alone acquires

A_art=-(alpha c1/2) (partial_ell rho_flat)/(partial_ell m_p).

Its natural dimension is alpha Lambda^3. It can therefore look precisely like the scale sought in this programme. It cancels exactly when flat space is subtracted at the same retuned parameters. The cross-theory baseline derivative also depends on independent vacuum matching; the cancellation does not require assigning it a value. A geometric projector cannot remove it after parameters have already been made radius dependent. Actual stress uses a metric variation at fixed couplings at each point; a total derivative along the retuned parameter path is a different object.

This identifies a calibration artifact to exclude. It does not disprove an intrinsic fixed-theory QCD linear response. The derivation and physical matching insertion are in [the matching report](matching_path/REPORT.md).

## A direct test of the missing vacuum coefficient

For the round S4 prescription, the exact stress combination

R_H=[rho(8H)-21rho(4H)+84rho(2H)-64rho(H)]/(28 H m_p^3)

annihilates every constant, H^2 and H^4 term at fixed microscopic parameters. If the specified small-H expansion exists with remainder o(H), it tends to R. No local polynomial fit or measured target value is used. A five-radius partition-function combination also removes the ordinary anomaly logarithm; its relation to actual stress requires a differentiated remainder bound. The matching tangent insertion supplies the alpha derivative of these finite-radius observables. This is an exact measurement prescription, not substituted QCD data.

[The derivation](coordinator/FINITE_RADIUS_DERIVATION.md) states the limits, bias, noise amplification and parameter constraints. The independent moment-system check caught a hand-arithmetic normalization error in the first draft (42 instead of 28); that failed run remains preserved. The corrected run passes 23 exact symbolic checks. Nothing is inferred about QCD merely from those algebra checks.

## What prevents the requested prediction

The proton finite window is evaluated, but the full proton response at physical quark masses is still missing. More decisively, none of these flat-space Compton data evaluates the subtracted curved-space vacuum functional. Its theta/contact projections cannot supply its theta-independent metric normalization. The vacuum route records the precise mixed trace/topological/current observable and a topology-sensitive discriminator in [its report](vacuum_response/REPORT.md).

For fixed flat m_p and specified quark masses the absolute derivative would be

dR/dalpha = [partial_alpha A_rho - (partial_alpha m_p/partial_ell m_p) partial_ell A_rho]/m_p^3,

on a regular matching branch. This form remains meaningful if A_rho=0, unlike a logarithmic sensitivity. The physical A_rho and both of its needed derivatives have not been supplied. Inserting the heavy-mass connected stencil into this physical expression would mix different theories and omit independent operators.

The next decisive physical calculation is common-input continuum QCD+QED vacuum stress or partition-function differences on controlled radii, plus its matched current insertion and full flat proton response. The present local environment contains no declared curved-QCD dataset with which to execute that nonperturbative measurement. These routes remain open; this is a research checkpoint, not a claim of a solution, a QCD no-go theorem, or global novelty.
