# Global topology and metric response in physical QCD

FSP-006, parent FSP-005. Raw derivation, 2026-10-19. The specified geometry is the smooth closed round Euclidean S4, radius a=H^-1, volume V=Omega4 a^4, Omega4=8 pi^2/3. Charge is canonical, lambda=e^2=4 pi alpha. All derivatives follow one fixed renormalized QCD/QED parameter path. No alpha value or cosmological scale is inserted.

## 1. Finite-regulator definitions and an exact mixed observable

Use coordinates for the gauge connection in which the integer Chern number Q is metric independent. In a common regulator absorb any metric-dependent measure into S, and write

    Z(t,theta,lambda)=integral dPhi exp[-S(t,lambda)+i theta Q],
    t=log a, W=-log Z, Tcal=partial_t S, I=partial_lambda S.

The identities below require differentiation of this regulated integral, followed by a controlled renormalized limit. A lattice discretization with noninteger naive Q needs a renormalized topological definition and its explicit derivative terms; integer rounding at finite spacing is not a differentiable replacement. On a smooth closed continuum manifold the integrated Q has no metric contact variation. Local q(x) does: working with the integrated charge is what fixes those contacts.

At theta=0 and CP symmetry,

    W_theta_theta=<Q^2>, chi=<Q^2>/V,
    W_t=<Tcal>, rho=W_t/(4V).

For any observable O, partial_t<O>=<partial_t O>-Cov(O,Tcal). Consequently

    partial_t chi=-4 chi-Cov(Q^2,Tcal)/V,
    rho_theta_theta=-Cov(Q^2,Tcal)/(4V)
                   =(1-D/4)chi,                  (1)
    D=H partial_H=-partial_t.

This is a directly measurable connected QCD observable: a topology–integrated-trace covariance, including the trace's quark, gluon, measure and matching pieces. It is not a replacement of rho by chi. Its sign can be checked from a theta-dependent constant vacuum potential: chi constant gives Cov(Q^2,Tcal)=-4V chi and rho_theta_theta=chi.

If chi(H)=chi0+a_chi H+o(H), with the differentiated asymptotics controlled, then

    partial_theta^2 A_rho|0=(3/4) a_chi.           (2)

The theta-dependent local terms through curvature squared can be removed by the same P(D)=D(D-2)(D-4) as in METRIC_RESPONSE.md. Equation (2) is conditional on its stated limit, not on a flat-gap argument. It probes a different component of the generating functional from A_rho(theta=0).

## 2. The exact electromagnetic insertion that is missing

At lambda=0 integrate the canonical photon as in the coordinator's prescription:

    I=(1/2) integral J D_g J + I_ct,
    partial_lambda chi=-Cov(Q^2,I)/V.              (3)

All sea, disconnected and current-contact terms belong to this expression. The quark/strong retuning terms required by the chosen path belong to I_ct. Let kappa(A,B,C) denote the connected three-variable cumulant. Differentiate (1) at fixed topology convention; equality of mixed action derivatives gives Tcal_lambda=I_t. Then

    partial_lambda rho_theta_theta
      =[kappa(Q^2,I,Tcal)-Cov(Q^2,I_t)]/(4V).      (4)

The second term must not be dropped. I_t includes variation of the photon Green function, volume factors, currents, UV contacts and parameter counterterms. In local notation the first term contains the integrated T q q J J correlator; the second supplies its seagull/contact completion. The topological charges are integrated, so calling the missing quantity just TJJ would omit the theta probes. For the actual theta=0 vacuum EM stress, before theta differentiation, the corresponding exact expression is

    partial_lambda rho
      =[<I_t>-Cov(I,Tcal)]/(4V).                  (5)

Equations (3), (4), (5) are distinct observables. Flat chi(lambda) fixes (3). It fixes neither (4) nor (5). A source can compute the Q^2JJ insertion and leave its metric response entirely uncomputed.

## 3. What the trace anomaly and axial identities do and do not add

The renormalized trace is an operator combination of the gluon beta-function operator, mass operators with anomalous dimensions, the electromagnetic beta-function operator when present, and gravitational/identity terms. Its precise Euclidean signs follow the stress convention above. This identity determines the operator to put in (1), (4), (5); it does not evaluate its curved-space expectation or its mixed correlations. In particular a flat-space gluon condensate, a proton trace matrix element and a theta susceptibility are not those vacuum metric derivatives.

The connected covariances in (1) and (4) remove an additive c-number identity in the trace. That is advantageous for measuring theta-dependent stress, but proves that they cannot recover a theta-independent vacuum term. Makino–Suzuki, arXiv:1403.4772v5, equation (2.11) and its master formula (4.73), explicitly subtract the flat vacuum expectation. Importing such a subtraction separately at each H would discard the desired response. A common flat subtraction with metric derivatives retained is required. Their master formula is established for separated operator insertions, as stated in Section 1; its equation-of-motion simplification also assumes no coincident operator. The integrated products here therefore need their own contact prescription, conveniently defined by regulated action/source derivatives. The flat master formula alone is not a ready-made evaluation of (1) or (4), and its extension to curved space requires matching.

As an exact structural check in pure QCD, if one quark is strictly massless an anomalous axial change of variables removes theta. On S4 the gravitational Pontryagin number is zero, so it introduces no residual gravitational theta dependence here. Thus all theta cumulants and (1) vanish. This does not make the theta-independent QCD stress vanish. This limiting argument is not a physical-point approximation or proof of nonzero A_rho; it refutes an inference that the axial identity alone makes topology data exhaustive of stress.

## 4. A new sector-conditioned trace diagnostic

Write P_Q=Z_Q/Z(theta=0) for the actual probability of sector Q. Exactly,

    rho_Q-rho=-(1/(4V)) partial_t log P_Q.         (6)

This is the difference between the integrated trace in a constrained sector and in the theta ensemble. It removes the same identity normalization on both sides. The normalized Fourier saddle of Aoki–Fukaya–Hashimoto–Onogi (AFHO), for fixed integer Q, X=chi V large, and bounded higher theta cumulants, gives

    log P_Q=-(1/2)log(2 pi chi V)-Q^2/(2 chi V)
            -c4/(8 chi^2 V)+O(V^-2),             (7)
    c4=partial_theta^4 f|0=-<Q^4>_c/V.

Equation (7) is the fixed-Q expansion; its omitted coefficients depend on Q and higher cumulants. Applying it at each sphere radius is a Fourier saddle, not a claim that AFHO simulated S4. Uniform remainder and derivative control must be established along the radius sequence. Under those conditions,

    rho_Q-rho=(4-D log chi)/(8V)[1-Q^2/(chi V)]
               +O(V^-2)                         (8)

where the O(V^-2) includes c4 and its radius derivative. At fixed chi,c4, the more explicit fixed-Q result is

    rho_Q-rho=H^4/(2 Omega4)
       -[Q^2/(2 chi)+c4/(8 chi^2)]H^8/Omega4^2
       +O(H^12).                                (9)

These are ordinary fixed-topology artifacts. The leading H^4 is a constraint entropy effect, not a linear-H energy. Summing sectors returns the theta ensemble; adding that H^4 term to its vacuum would double count the constraint.

For Q=0 there is a concrete amplified measurement:

    X_top(H)={8V[rho_Q=0-rho]-4}/H
            =-D log chi/H+O(H^3).               (10)

If chi0>0 and chi=chi0+a_chi H+O(H^2 log H), with the same saddle/differentiation control,

    lim X_top=-a_chi/chi0,
    A_rho,theta_theta=-(3 chi0/4) lim X_top.       (11)

Thus a topology-dependent H effect appears as an H^5 correction to the constrained-sector stress difference, against a universal H^4 baseline. A regular H^2 curvature term in chi first appears as H^6 here; non-Gaussian fixed-topology contamination in (10) starts at H^3 after amplification. This diagnostic is falsifiable and can be computed from sector-conditioned trace measurements without an absolute partition-function normalization. It is demanding statistically; no such numerical QCD measurement is performed here.

It is decisive for a mechanism only when that mechanism predicts the theta dependence of A_rho. For example a specified A_rho(theta)=A0 v(theta), v(0)=1, v''(0) nonzero, predicts A_rho,theta_theta=A0 v''(0). Neither AFHO nor the anomaly fixes v. A failure of (11) to show a linear response would not exclude a theta-independent A0.

## 5. An exact information obstruction, not a new counterterm

For any theta-independent C[g,lambda], multiplying all Z_Q by exp[-C] leaves P_Q, every theta cumulant, and Z(theta)/Z(0) unchanged. It shifts W by C. A hypothetical C=V c(lambda)H shifts the target stress by (3/4)c H while leaving (1), (4), (6) unchanged. This is an inverse-data counterfamily: it proves that normalized topology measurements alone do not determine that target. It is NOT permission to add a nonlocal C to a fixed microscopic QCD theory, and NOT a demonstration that QCD generates it. Locality and the actual globally normalized path integral could rule it out or fix it. Those are additional inputs.

This distinction is visible in AFHO's exact source: before the saddle derivation it sets Z(0)=1, E(0)=0 in equation (1). That is harmless for normalized theta observables and removes the stress normalization in question. Likewise a reconstructed thermal Z(theta)/Z(0) gives only f(theta)-f(0), even if arbitrarily many sectors have been measured.

## 6. Relation to actual primary QCD results

The already-used Gorghetto–Villadoro calculation, arXiv:1812.01008v2, Appendix A.1 equations (34),(36), supplies the flat chiral matching for (3):

    (partial_lambda chi)/chi_LO = K_chi
        -Z/(8 pi^2)[1+log(M^2/mubar^2)]+
        higher chiral terms,
    K_chi=(20/9)(k5+k6)+(4/9)(1+3 Delta)k7,
    M^2=B(mu+md), Delta=(md-mu)/(md+mu).

This is the same adjacent result used in the earlier EM lane, not a newly evaluated physical slope. Its independent LECs remain. The source's main-text equation (10) is instead expressed using the neutral pion mass and a pure-QCD pion decay input. Subtracting its pion mass correction, equation (31), from equation (36) produces equation (10). The bounded check verifies that change of variables exactly. Holding the pion mass fixed changes the charge-switching path. No numerical LEC, Z, measured alpha, susceptibility, or hadron mass is inserted here. In particular the source's EM-calibrated percentage is not repurposed as an unfitted slope.

Kotov–Lombardo–Trunin, arXiv:2502.15407v2, is an actual recent continuum-extrapolated thermal QCD topology calculation with physical pion tuning. Its sector reconstruction in Section 6.4 concerns the normalized Z(theta)/Z(0) on a thermal cylinder. It does not supply the S4 radius derivative in (1), the mixed insertion (4), or the common factor in Section 5. Its scale is calibrated with f_pi and its quark masses are tuned; it is not a parameter-free QCD prediction. No reported numerical point is used in the present calculation.

Yamamoto's arXiv:1405.6665v2 remains an adjacent quenched curved-background current calculation as already established in the frozen lattice-bridge report. A bounded primary search did not find an actual continuum S4 QCD evaluation of (1), (4), (5) or (10). This is a search limitation, not a nonexistence or novelty theorem.

The recent-looking CERN copy of Zhitnitsky's magnetic-field/holonomy paper is the 2019 publication, matched by arXiv:1902.07737v2 dated 2019-05-08. Its coefficient is still left for a QCD lattice calculation; its weakly coupled support and dominant H ansatz do not evaluate the required physical metric functional. No new 2026 computation was found in that copy.

## 7. Cheapest discriminating physical continuation

Use one renormalized sphere ensemble at positive quark masses, measure joint integer Q and the correctly normalized integrated trace, and check (1) by independent radius differences of chi. This tests operator contacts and the global derivative before extrapolating. Then use a radius sequence at common physical inputs to measure (10), with higher-cumulant and fixed-sector derivative errors controlled. At order e^2 additionally measure I, I_t and the connected cumulant in (4) in the same regulator, or introduce electromagnetic reweighting with the complete matching path. This directly tests a topology-dependent linear-H mechanism. Determining the theta-independent A_rho still requires the unconditioned stress (5) or an absolute matched free-energy comparison; the parent coordinator develops that complementary test.
