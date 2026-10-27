# FSP-009: non-Born proton and unconditioned QCD vacuum

**The full physical A_rho, R(alpha)=A_rho/m_p^3 and alpha remain uncalculated.** This continuation computes a full finite non-Born photon band in a controlled pion–nucleon sector, obtains an infrared filter and coordinate-moment formula for its soft coefficient, and derives a contact-complete estimator for the unconditioned vacuum coefficient. No alpha value, target ratio or cosmological coefficient is fitted.

## A complete non-Born band in a declared low-energy sector

The [proton calculation](nonborn_proton/REPORT.md) goes beyond the parent's elastic functional and the earlier isolated sea/subtraction moment. For a stable proton at positive QCD pion mass, let a=alpha_E/u and b=beta_M/u at u=e^2=0. With the complete on-shell Born graphs removed, both Compton amplitudes give the exact soft-ball reduction

    (M_u^NB/M)(0<Q<Lambda)=3 Lambda^4(a-b)/(32pi M)+O(Lambda^6).

The dispersive part contains a+b; its independent subtraction contains b. Both are required. The source-normalization dictionary is checked against both Born amplitudes and the Euclidean polarizability interaction. A magnetic subtraction alone would not give this coefficient. Full-QCD a,b include every contraction class, but their numerical physical values are not supplied by this reduction.

An authenticated primary ancillary notebook permits a separate no-alpha calculation of the covariant pi-N-loop polarizability difference. Its fitted magnetic contact, empirical Baldin normalization, Delta-transition calibration and numerical alpha cell are excluded. At the source's printed strong parameters, the isolated covariant soft coefficient is 0.0395567 GeV^-4; the strict leading heavy-baryon coefficient is 0.0513256 GeV^-4. Their difference is a comparison of approximations, not an uncertainty estimate or two additive contributions.

The ancillary was enumerated and contains static polarizabilities and slopes, not the needed two-variable amplitudes. The work therefore continued into a different primary source: Nevado–Pineda0712.1294v2. Its complete leading-HB pi-N non-Born functions, including the contact missed by a purely dispersive reconstruction, support an actual [finite-band integration](nonborn_proton/FINITE_BAND_DERIVATION.md):

    (M_u^NB/M)(0<Q<m_pi/2)=1.19846564e-6,
    (M_u^NB/M)(m_pi/4<Q<m_pi/2)=1.12269133e-6.

These are coefficients per e^2, before the full-theory mass/strong matching insertions. No numerical alpha enters. The full first band is 0.98456143 times its strict soft-polynomial limit; the run uses the full functions rather than assuming that ratio. The result is complete at the specified leading-HB pi-N order over that finite Euclidean band, not the full physical proton or the covariant all-momentum answer. Its flat photon cutoff is not sphere curvature H.

Numerical units use the source's printed M=0.93827, m_pi=0.13957, f_pi=0.09221 GeV and g_A=1.27. These are imported calibrations, not ab initio predictions. In particular the charged-pion benchmark is not an independently calculated pure-QCD pion mass on the physical fixed-MSbar matching path. Higher-order polarizability operators, recoil, Delta/heavy states, remaining momenta and finite QCD matching remain independent physical inputs. Numerical quadrature convergence does not bound those omissions. The covariant static coefficient is not multiplied by the HB band shape as if that produced a full covariant result.

## A no-fit infrared coefficient and full-trace moment

The additional [massive-photon calculation](photon_mass/REPORT.md) changes the propagator, while holding the pure-QCD current tensor and the mass-independent matching prescription fixed. Put s=lambda_gamma^2 and f_NB(s)=M_u^NB(s)/M. For a positive QCD gap, infinite volume and the specified contact-complete Born subtraction, the soft coefficient is

    C_NB=3(a-b)/(32pi M),
    f_NB(s) contains -2 C_NB s^2 log(s),
    C_NB=-lim_(s->0) s f_NB'''(s)/4.

This is a propagator-derivative calculation, with no fitted mass curve. The derivative kernel makes the hard contribution vanish in the limit under the stated soft-density and OPE-tail bounds. The actual full HB pi-N functions were integrated at six photon masses, not replaced by their soft polynomial. At lambda_gamma/m_pi=0.002, the estimator is 0.9999413325 times the independently known C_HB. The separate exact local-ball factor is 0.9999520015; the additional shape correction is computed. These are approximation controls, not a physical QCD uncertainty estimate.

For the full charged response, a fifth-order Euler projector removes the lower analytic and half-integer powers. Its known Born logarithm depends on d=2+6kappa+3kappa^2/2; the resulting non-Born extraction still needs the independently matched pure-QCD anomalous moment. Two independent integral representations of the all-momentum elementary Dirac response agree at the six declared masses. A [six-mass annihilator](photon_mass/SIX_MASS_STENCIL.md) provides a discrete alternative, but spans a factor 32 in photon mass and amplifies noise. Its finite-grid remainder and covariance must be controlled. Crucially, both filters annihilate an arbitrary additive constant: neither calculates the full hard mass response f(0). Photon mass is not sphere curvature H.

The separate [coordinate companion](photon_mass/COORDINATE_MOMENT.md) supplies an equivalent direct observable. With H_tr^NB(x) the complete Euclidean trace of the vacuum-subtracted proton two-current correlator, spin averaged and normalized by 1/(2M),

    C_NB=-1/(512pi^2 M) integral d^4x |x|^2 H_tr^NB(x).

This uses all four currents, all sea contraction classes and the full four-dimensional second moment. The earlier spatial-current temporal sea moment is insufficient. The derivation includes the bound |r^2 K2(lambda r)-2/lambda^2|<=r^2/2; a finite absolute second moment of the regular part and correctly treated local distributions justify the limit. Derivatives of delta-function contacts contribute and cannot be discarded. Complete coordinate Born subtraction may need more form-factor information than the local kappa-only logarithmic correction. An infinite-volume photon kernel can change the practical lattice implementation, but QCD finite-volume errors, tails, current normalization and contacts still need control. No complete QCD moment dataset is evaluated here.

Massive-photon extrapolation is an established method; this is a scoped translation into the polarizability observable, without a novelty claim. Endres et al.1507.08916v3 footnote42 names a regulator EFT operator that could contribute at the same logarithmic power if it occurs at order u. The source supplies neither that u-order nor its matching coefficient. It therefore establishes neither actual contamination of this fixed microscopic tensor observable nor a new freely adjustable coupling. Generic QED_M curves require a canonical-path and regulator-matching admission check. The inspected electroquenched mass-splitting/pion/kaon source data do not supply the correlated, all-current individual-proton grid needed here. This is a bounded statement about inspected sources.

## The unconditioned vacuum observable

The [global-vacuum route](vacuum_global/DERIVATION.md) starts with the actual normalized, unconditioned regulated measure, not a fixed topological sector or orientation ratio. Put t=log(radius), V=Omega exp(4t), Omega=8pi^2/3 and W=-log Z. All measure, gravity, current and regulator terms are included in S(t,u), along the line of fixed renormalized parameters. Define X=S_t, Y=S_tt and J=S_u. Then

    E=W_tt-4W_t=<Y-4X>-Var(X)=4V rho_t.

If the target expansion and its differentiated remainder are controlled, the missing coefficient is

    A_rho=-lim_(H->0) H^3 E/(4Omega).

The exact charge response includes the two-metric/charge contact and a connected third cumulant. In a useful covariance form, with F=Y-4X-(X-<X>)^2,

    E_u=<Y_u-4X_u>-2Cov(X,X_u)-Cov(F,J).

The route derives a measurable Cauchy–Schwarz bound and a higher Weyl projector with its fourth cumulant. Constant flat density cancels exactly, analytic local gravity terms cannot imitate a constant A estimator, and an unknown common metric normalization still contributes through the contact mean. A required O(H^-3) term cannot be inferred from a variance or a normalized sector probability alone.

This is an executable estimator and conditional bound, not its physical expectation value. The finite-state algebra checks are not a QCD ensemble. Each extensive term can be O(H^-4); the required cancellation or surviving H^-3 remainder must actually be measured. A flat mass gap or finite covariance does not prove the needed uniform curved/global bound. At fixed angular lattice size, changing radius also changes the physical cutoff, so bare couplings must follow the line of fixed physics.

A newly authenticated accepted 2026 lattice study, Braguta et al.2602.20970v2, supplies real-acceleration thermal Rindler pure-SU3 data. Its patch has zero Riemann curvature and open spatial boundaries; its observables are Polyakov loops and phase structure. The source's alpha denotes acceleration. It does not give round-S4 QCD vacuum stress, electromagnetic alpha response or a proton. The stated action yields an exact contact-minus-variance acceleration Hessian. An even-acceleration partition and zero first derivative follow if both the centered clover action and its open-boundary treatment are reflection covariant. The paper specifies clover averages but not enough implementation detail to certify that boundary property. The finite control tests an explicitly symmetric realization. Its analytic neighborhood also shrinks with the domain, so it is no proof excluding an absolute-acceleration term in a nonuniform infinite-volume limit.

## Testing a proposed proton–vacuum closure

The [common-response derivation](common_response/RAW_DERIVATION.md) makes a new comparison within the same isospin-symmetric QCD theory. Exchanging up/down charges is a flavor relabeling: the complete unconditioned vacuum functional and every metric derivative are unchanged. The proton non-Born tensor instead maps to the neutron tensor. A scalar/trace Ward insertion preserves this representation distinction; it does not turn a baryon matrix element into a vacuum expectation.

A primary-source chiral calculation supplies a nonzero electric p-n non-Born logarithmic response. The full photon angular contraction again selects a-b, where the kappa_s-independent electric and magnetic logarithms cancel. The remaining soft mass-channel logarithm is proportional to the isoscalar anomalous moment kappa_s, with its zero branch explicit. The soft momentum limit is taken before the chiral limit. No empirical kappa_s or alpha is assigned.

This rules out obtaining the entire proton non-Born tensor from only the stated flavor-covariant vacuum Ward identities. It does not rule out an additional dynamical relation at the physical charge assignment, establish the full all-momentum p-n mass slope, or resolve physical isospin breaking. The old chiral mass-LNA ratio and calibration projector are inherited; neither is relabeled as this new threshold comparison.

## A new flat-vacuum source does not supply the curvature coefficient

The [coordinator source audit](coordinator/vacuum_let/REPORT.md) examines Bai–Chen2502.20241v2. Its flat condensate/bag energy and fitted thermal equation-of-state inference do not calculate A_rho. There is also a separate connected-response admission question in its low-energy-theorem bound. A configurationwise scalar/topological inequality orders raw second moments; it does not alone order connected susceptibilities. An exact positive unconditioned finite ensemble demonstrates that logical distinction, without pretending to be microscopic QCD or refuting a physical numerical bound. A QCD-specific connected/contact-compatible comparison would require an additional argument. The low-energy theorem itself is not challenged.

For any flat density E0(u), W=E0(u)V gives rho=E0(u), so that piece cancels in rho(H)-rho(0) and its charge derivative. An improved flat condensate value therefore cannot replace the missing curved/global response. No conversion factor is fitted to force that substitution.

## What remains before a physical ratio

The [ratio derivation](coordinator/RATIO_DERIVATION.md) combines the actual required observables:

    R_alpha=4pi[A_u/M^3-3A M_u/M^4].

Both A_u and M_u must be complete on the same calibration path. The new non-Born band is one controlled piece of M_u; the vacuum estimator still needs its unconditioned QCD expectation values and continuum/radius limits. Source-first reviews, exact audited revisions, numerical checks and all restrictions are [reconciled separately](reviews/RECONCILIATION.md). The original goal remains open, with concrete data/matching conditions in [the route index](ROUTES.md).

The photon/current calculations are first order in u about pure QCD. Even a complete such calculation would give an initial charge slope, rather than the whole finite-alpha function. A prediction of alpha additionally needs a physical selection equation with independent inputs and a demonstrated solution; the displayed derivative identity alone supplies none.
