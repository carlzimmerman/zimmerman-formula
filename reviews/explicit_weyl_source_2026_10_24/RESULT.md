# Explicit symmetry on metric, extra fields and matter: full-source Weyl test

## Result and advance over the previous Weyl test

An explicit local symmetry can be constructed that transforms the metric, unit vector, compensator, MOND scalar and matter, while retaining the previously established scalar source through gravitational mixing. However, its exact Ward identity allows the vacuum, linear-gradient, quadratic-gradient and cubic-gradient operators separately. It therefore neither protects the two vanished coefficients nor selects the vacuum/force ratio. This is a failed candidate with an explicit action-level reason, not the requested successful microscopic mechanism.

The older integrable-Weyl audit encountered a direct scalar-source problem. The present construction addresses that particular gap by keeping an independent physical scalar and the covariant metric-vector source mixing. It also makes the nominal MOND scalar transform nontrivially under the local symmetry. The resulting invariant physical scalar remains real and sourced; the failure here is coefficient freedom, not merely a vanished source.

Base 69f1f60587; frozen criteria 2b29534c88. Kappa=1/2 remains FITTED. CFG493 kappa_Lambda=0.417 +/- 0.095 and kappa_crit=0.345 +/- 0.078 are distinct and unused. Dark-energy footing; c=hbar=1. No numerical selection, fit, scan, second parameter-free prediction or microscopic hbar cancellation is asserted.

## 1. The complete transformation

In D spacetime dimensions, work on sigma>0 with a fixed positive reference normalization f. For arbitrary smooth omega(x), set

    g_mu nu -> exp(2 omega) g_mu nu,
    sigma -> exp(-omega) sigma,
    U^mu -> exp(-omega) U^mu,
    theta -> theta + omega,
    psi -> exp[-(D-1)omega/2] psi.

The Dirac adjoint has the same weight as psi. The unit condition g_mu nu U^mu U^nu=-1 is invariant. Define

    ghat_mu nu = (sigma/f)^2 g_mu nu,
    Uhat^mu = (f/sigma) U^mu,
    chi = theta + log(sigma/f),
    psihat = (f/sigma)^[(D-1)/2] psi.

All four hatted/physical variables are invariant pointwise. In particular partial_mu chi is invariant despite the spacetime-dependent theta transformation: the derivative of omega from theta cancels the derivative from log sigma.

A full covariant action S0[ghat,Uhat,chi,psihat] therefore defines an exactly invariant classical action when expressed in the original fields. Choose its gravitational sector to be the source-mixing action from reviews/mixed_source_ward_2026_10_24/RESULT.md, now entirely in hatted variables, including the unit-vector constraint and temporal sector. This supplies a concrete family of full transformations and sourced actions, not just an invariance of the quadratic static terms.

## 2. Matter really is included

For a massive effective Dirac species in D=4, take

    S_m = integral sqrt(-ghat) [i psihat_bar gammahat^mu Dhat_mu psihat
                                - y f psihat_bar psihat].

This is invariant by construction. In unhatted variables the mass density is sqrt(-g) y sigma psi_bar psi. The massless Dirac kinetic term has its standard compensating vierbein and spin-connection factors. Equivalently a massive point-particle action is

    S_particle = -y f integral ds_ghat = -y integral sigma ds_g.

Thus a mass source is included consistently, not treated as a fixed external object that violates the transformation. These are effective matter descriptions; no anomaly-free microscopic Standard Model or baryonic QCD matching has been constructed. The y values remain ordinary independent mass couplings.

Matter couples universally to ghat. In the aligned weak-field regime the gravitational mixing gives physical potential Phi=Phi_hat+(B/A)chi, so the scalar source coupling is g=B/A exactly as in the parent audit. The compensator itself supplies no extra trace force. Universal metric coupling does not by itself fix B/A, the cubic amplitude, or the vacuum coefficient.

## 3. Four separately invariant operators

Let

    P^mu nu = g^mu nu + U^mu U^nu,
    Y = P^mu nu partial_mu chi partial_nu chi >= 0.

The projector has Weyl weight -2 and Y transforms as exp(-2 omega)Y. For any p, the density

    I_p = sqrt(-g) sigma^(D-p) Y^(p/2)

is separately invariant: its weights add to D-(D-p)-p=0. For D=4 the relevant local energy densities, divided by sqrt(-g), are

| Operator | Coefficient | Role after sigma=f |
|---|---|---|
| sigma^4 | c_0 | vacuum V=c_0 f^4 |
| sigma^3 sqrt(Y) | c_1 | unwanted linear-gradient term alpha=c_1 f^3 |
| sigma^2 Y/2 | c_2 | independent quadratic-gradient contribution c_2 f^2 |
| sigma Y^(3/2)/3 | c_3 | cubic coefficient gamma=c_3 f |

The quadratic entry can shift the full Schur stiffness C-B^2/A. It need not equal that stiffness before the other gravitational coefficients are included. The p=1 operator is nonanalytic at zero gradient; the symmetry allows it on the response branch but does not establish that a regular vacuum effective action contains it. Restricting to an effective energy analytic in gradient components would also exclude the desired p=3 term, as established in the preceding audit.

In hatted variables the same densities are sqrt(-ghat) f^(D-p) Yhat^(p/2), where Yhat=(f/sigma)^2 Y. This gives an independent check of every power of f and sigma.

Every c_p is compatible with the displayed local symmetry. In particular c_0>0 and c_3>0 impose signs without fixing their product or quotient. Choosing c_1=0 and cancelling the full quadratic stiffness remain extra matching conditions. Their symmetry-allowed deformations are explicit, so an exact symmetry of this form cannot by itself provide their radiative protection.

## 4. The Ward identity contains no coefficient-selection equation

Let E denote functional Euler derivatives. With consistent left/right ordering for the fermionic contractions, the infinitesimal invariance gives the local identity

    2 g_mu nu E_g^(mu nu) - sigma E_sigma - U^mu E_U,mu + E_theta
        - [(D-1)/2](fermion Euler contractions) = 0.

This follows off shell because all arguments of S0 are invariant. It holds for each I_p separately and for the matter action separately. Hence inserting sum c_p I_p yields zero for every choice of c_p; it cannot imply c_1=0, c_2=0 or a relation between c_0 and c_3. This is an explicit check of the Ward identity's content, not merely parameter counting.

Quantum anomalies require an actual quantum definition and are not settled here. Even granting an exact anomaly-free version of this identity would not remove the separately invariant counterterms. An anomalous identity would require additional analysis and cannot be invoked as protection without deriving its effect.

## 5. Gauge fixing proves why the apparent extra symmetry does not reduce theory space

For sigma>0 choose omega=log(sigma/f). Then sigma_new=f, theta_new=chi, g_new=ghat, U_new=Uhat, and psi_new=psihat. The action becomes precisely the arbitrary starting action S0.

Thus this compensator construction is a lift of the original physical theory family, not a restriction of it. The new gauge orbit removes the new redundant variable. No physical coefficient freedom has disappeared. Conversely any action in the invariant fields admits this lift, so its existence cannot distinguish the desired MOND/vacuum relation from alternatives.

This statement is local to the sigma>0 patch. It makes no assertion about global topology, zeros of sigma, global gauge obstructions or a different microscopic gauge completion. Those require specified extra structure rather than identifying the present local redundancy as a physical selection rule.

## 6. Physical amplitude and analytic mutation controls

In D=4 after gauge fixing, let the positive temporal coefficient be K=c_K f^2, gamma=c_3 f, V=c_0 f^4, and define the operational Planck mass from the measured high-gradient Newton coupling by M_Pl^2=c_N f^2. The coefficient c_N need not equal the bare Einstein coefficient; source matching must determine it. The source coupling to the dimensionless physical scalar chi is g=B/A.

Canonical normalization then gives

    u = g sqrt(c_N/c_K),
    v = c_3 c_N/c_K^(3/2),
    e = c_0/c_N^2,

and therefore

    R = u^3/(v sqrt(e)) = g^3 c_N^(3/2)/(c_3 sqrt(c_0)),
    kappa = 2 sqrt(8 pi) R.

Both the compensator normalization f and the temporal field normalization c_K cancel. The independent physical coefficients remain. The symmetry supplies no equation selecting the right-hand side.

Analytic controls at fixed other physically matched coefficients:

- c_3 -> t c_3 with t>0 leaves the local symmetry exact and gives R -> R/t.
- c_0 -> t c_0 leaves the local symmetry exact and gives R -> R/sqrt(t).
- Adding a nonzero c_1 or an independent c_2 preserves the identity while restoring an unwanted lower-gradient response.

A cubic deformation can be restricted to the small-Yhat regime with a smooth function of the invariant ratio Yhat/f^2 to leave a specified high-gradient calibration unchanged. This demonstrates allowed functional freedom, not a proposed microscopic interpolation law. Varying c_0 changes cosmological solutions; no statement that their full stability remains unchanged is needed for the narrower allowed-operator test. Positive V alone is not a stable-vacuum certificate. In a gauge theory the compensator equation is related to the metric and matter equations; minimizing c_0 sigma^4 alone would also be an invalid vacuum analysis.

## 7. Source provenance, review and remaining route

The general possibility of a Weyl lift and homogeneous but freely specifiable invariant potentials is established background: [Bars, Steinhardt and Turok, 1307.1848v3](https://arxiv.org/html/1307.1848v3), version 2013-11-08, sections II.2 and III.1, equations (10)-(17), inspected 2026-10-24. The simultaneous transformation above, scalar-vector source retention and operator/amplitude test are derived here; the source does not claim this is a MOND completion. The attempted anisotropic source 1002.2549v2 was not retrievable in HTML and supplies no premise or result here. No source file was downloaded.

Review is analytic self-review, recorded in REVIEW.md. No numerical executable, independent verification, all-orders protection or healthy positive-vacuum selection is claimed.

What changes the search is specific: adding an explicit local symmetry through compensator variables, even one visibly acting on baryons and the MOND scalar, cannot by itself select the ratio. A genuinely restrictive new microscopic symmetry must remove at least one of the independently invariant physical deformations above, or supply additional dynamics/quantization relating their coefficients. No such relation was constructed in this test; the user's original goal remains open.
