# A finite full-Born functional of actual lattice proton points

FSP-008 physical-data continuation, 2026-10-19. This directory preserves the earlier completed proton-kernel package unchanged. Here the input changes from an elementary Dirac benchmark to the published individual-proton Sachs form factors of Alexandrou et al., arXiv:1812.10311v2, Table VI/Appendix B, PDF page 26. These are actual lattice point estimates, not samples of a fitted Q² curve.

## 1. Authenticated data and conditional physical scope

The exact public source archive contains `table_ffs.tex`. It supplies 19 nonzero-Q² pairs GE^p,GM^p at Q²=0.057 through 0.963 GeV². The row Q²=0 has GM=NA and is excluded. No magnetic moment, dipole, z-expansion or Galster ansatz is used to fill it or extrapolate either endpoint.

The data come from the cB211.072.64 Nf=2+1+1 QCD ensemble, 64³ by 128, am_N=0.3813(19), a=0.0801(4) fm, m_pi L=3.62. The source sets the scale using the measured average proton/neutron mass m_ref=0.9389 GeV; this empirical calibration is an explicit conditional input, not a mass derived in this calculation. The source Q² labels and m_ref are used together. This functional holds both fixed; its statistical calculation does not independently vary that common scale or invent its covariance.

The current normalization is the usual GE^p(0)=1, GM in proton magnetons, so the tabulated form factors are charge-stripped and no elementary e or measured alpha is inserted. Connected current matrix elements use the lattice conserved current; light disconnected ones use the source's local current normalization ZV=0.728(1). The source includes connected u,d and light u+d disconnected matrix elements. Strange/charm are dynamical sea flavors of the QCD ensemble; their current insertions are not authenticated in these proton columns. This calculation is accordingly restricted to the source's light-current elastic sector. It is not a completeness assertion for the physical all-flavor electromagnetic current.

The published point estimates already contain ground-state/plateau extraction fits and jackknife marginal errors. Connected plateau values at the largest separation are chosen, checked against two-state and summation analyses; disconnected final values use ts/a=14, compared with 16. Those source extraction choices and current normalization are imported as published QCD evidence. Separate fits to Q² dependence, magnetic moments and radii are excluded here. No new parameter is fitted to alpha, vacuum energy or a mass target.

## 2. Full Born kernel, not just its dispersive elastic part

Use u=e²=4 pi alpha, z_i=sqrt(Q_i²)/(2m_ref), tau=z², and the standard on-shell Born convention of the frozen `proton_kernel/DERIVATION.md`. At each source point define

    F1=(GE+tau GM)/(1+tau),
    A=(GE²+tau GM²)/(1+tau),
    C=GE²-2 tau GM²,
    B(z;GE,GM)=z(3F1²-A)/2+C/(sqrt(1+z²)+z).             (1)

This is the complete tensor-angle convolution of the Born T1 and T2, including the -2F1² polynomial in T1. The independent dispersive-elastic expression is

    E(z)=3z GM²/[2(1+tau)]
        +(GE²-2tau GM²)/(1+tau)
          [(1+tau)^(3/2)-z³-3z/2],
    B(z)=E(z)-(3z/2)(GM²-F1²).                           (2)

Equation (2)'s second term is the elastic Born subtraction. Both are needed. The source's light disconnected vertex enters the *total* tabulated GE,GM, whose coherent square appears here. This does not isolate the complete disconnected two-current Cottingham contribution: the non-Born tensor has its own sea contractions.

## 3. The numerical object actually calculated

For z_1<...<z_19 define the composite trapezoid functional

    I_tab=(1/(2 pi²)) sum_(i=1)^18 (z_(i+1)-z_i)
                              [B_i+B_(i+1)]/2.           (3)

It is a declared finite functional of the 19 printed points. We calculate each B_i, the dispersive and subtraction analogues, and verify their sum. A second implementation uses nodal weights

    w_1=(z_2-z_1)/2,
    w_i=(z_(i+1)-z_(i-1))/2 for 2<=i<=18,
    w_19=(z_19-z_18)/2,
    I_tab=(1/(2 pi²)) sum_i w_i B_i.

This involves no form-factor model. It is not a rigorously error-bounded approximation to a continuum integral: the source spacing, rounding and unknown between-point shape supply no quadrature-error guarantee. The electromagnetic mass response that motivates the normalization is formally M_u^Born(window)/m, but I_tab is the source-point estimator for a restricted light-current sector, not that full continuum quantity. If used as such an estimator, its first-order mass contribution is u I_tab. The corresponding coefficient per alpha is 4 pi I_tab, with no numerical alpha chosen. Q below the first point, Q above the last point, all non-Born amplitudes, strange/charm current pieces, and QCD ultraviolet matching remain absent.

## 4. What the printed errors can support

The archive/main paper does not supply the joint GE/GM configuration samples or covariance matrix. We do not invent one or combine the marginal errors in quadrature as if independent. At fixed Q² and m_ref the linear sensitivity coefficients are

    dB/dGE = z(3F1-GE)/(1+tau)+2GE/(sqrt(1+z²)+z),
    dB/dGM = z tau(3F1-GM)/(1+tau)-4tau GM/(sqrt(1+z²)+z).

For the linearized fluctuation delta I=sum_j g_j delta X_j, Cauchy-Schwarz gives

    sd(delta I) <= sum_j |g_j| sigma_j,                    (4)

for any positive-semidefinite covariance with the given marginal variances. We report this **conditional linearized statistical ceiling**, not the true nonlinear estimator uncertainty, a confidence interval or a total theoretical error. Scale/current normalization systematics, excited states, finite a/L, heavy-current omission, source rounding and quadrature bias are excluded. The exact quadratic functional also has a covariance-dependent mean shift that cannot be inferred from the printed marginals. Its central value is simply evaluation at the printed central inputs.

## 5. Execution and interpretation

All source inputs, this derivation, code and contract are fixed before the bounded run. The computation checks source-TeX transcription, all 19 Born-kernel identities, segment/nodal quadrature equality, constant and linear trapezoid invariants, and analytic versus numerical sensitivities. Numerical arithmetic uses 60 decimal digits for reproducibility, not as a claim of precision of rounded lattice data. The mathematical result is a finite source-data functional with declared limitations. It does not determine the full proton kernel, R(alpha), or a preferred alpha.
