# FSP-010: hard proton matching and an unconditioned interacting vacuum

**The full physical proton derivative M_u, curved-vacuum A_rho, R(alpha)=A_rho/M_p^3, finite-alpha dependence and alpha remain uncalculated.** This continuation changes the two missing physical steps: it specifies a finite quark matching coefficient and an all-scale reconstruction of the hard mass, then computes actual absolute non-Abelian and charged-sea vacuum coefficients in explicitly defined closed lattice models. These partial values are not added into a purported complete QCD prediction. No numerical alpha or cosmological target is used.

## Finite hard quark matching and newer proton data

The [hard-proton calculation](hard_proton/REPORT.md) closes a finite coefficient left unspecified by the earlier scalar OPE/log cancellation. For a sharp O(4) photon cutoff and fixed MSbar quark parameters, its leading strong-order local conversion is

    M_u,ct^q=sum_f Q_f^2 sigma_f^p
                [3 log(mu^2/Lambda^2)+5/2]/(16pi^2),
    sigma_f^p=m_f partial M_p/partial m_f, u=e^2.

The finite 5/2 is the difference between the complete sharp-loop constant 3/2 and the dimensionally regulated/MSbar constant 4, including the evanescent numerator. Matching uses an external elementary quark; a scalar Feynman–Hellmann insertion transfers that local operator to the proton. It does not model the proton's full two-current tensor as an elementary particle. The formal leading quark Wilson tail remains finite at mu=Q0, but it is useful only above all retained active masses and QCD scales, with higher-order/power control.

Source-calibrated scalar matrix elements give sum Q_f^2 sigma_f=52.0711466667 MeV and finite conversion 0.8243609709 MeV per e^2 at mu=Lambda. The quoted linearized marginal-error ceiling is 0.2729073064 MeV per e^2, conditional on the cross-source parameter identification; it is no total theoretical error. These inputs include lattice fits, scalar sea terms, empirical scale/quark-mass calibrations and continuum/model averages. This is not a parameter-free proton prediction.

A newer June 2026 source supplies three finite-spacing light-current form-factor tables. Its continuum curves use fitted parametrizations, and strange/charm electromagnetic insertions are not part of those tables. The declared full-Born nodal functional on 0.56<=Q^2<=0.88 GeV^2, at explicit reference mass 0.9389 GeV, gives M_u,B/m_ref per e^2:

| Ensemble | Nodal functional |
|---|---:|
| B64 | -0.0003343715368 |
| C80 | -0.0004164176385 |
| D96 | -0.0004332606994 |

The calculation applies no new fit or endpoint extrapolation. The source's correlator fits and calibrations remain inputs. This finite nodal object is not a controlled continuum-band quadrature or a complete hard mass. Its light disconnected elastic changes are smaller than the covariance-agnostic linear error ceilings and establish no physical sign. A negative full-Born value is allowed because the regular Dirac subtraction is included. No value from this table is added to the local conversion as if omitted momenta, non-Born terms and finite matching were known.

## Recovering the constant requires all scales and its UV endpoint

The [reconstruction package](hard_bridge/REPORT.md) changes the previous infrared method: integrate derivatives over all photon masses rather than taking only a soft limit. For s=lambda_gamma^2 and h_n=(-1)^n s^(n-1)f^(n)/(n-1)!, the exact finite-endpoint identity is

    f(0)=integral_0^L h_n(s)ds
         +sum_(k=0)^(n-1)(-L)^k f^(k)(L)/k!.

The stated endpoint derivative limits and integrability are essential. A function bound O(s^1/2) alone does not establish them; the independent review's stronger restriction governs the theorem. For a controlled single logarithm f=-a log(s/S0)+B+r,

    f(0)=B+a H_(n-1)+integral_0^infinity[h_n-a/(s+S0)]ds.

Thus all-scale data can recover the hard constant, given the matched UV boundary. A canonical mass-independent scheme fixes B; it is not a new free coupling. In the complete Dirac benchmark at M=mu=1, B=5/(32pi^2) and f(0)=1/(4pi^2). Independent radial/Feynman-parameter calculations recover it. Pointwise heavy-photon decay at separated currents does not justify removing the coincident-current matching term. QCD running requires a matched running endpoint rather than the elementary single-log ansatz. Full QCD data across the intermediate photon scales remain missing.

## The finite gluon coefficient recovered from two-loop matching

A further [source-first matching calculation](gluon_matching/DERIVATION.md) reconstructs the conserved-vector limit of established Standard Model decoupling results. Sequential matching must remove both the top-QED threshold and its induced mass threshold before taking the six-light-quark limit. Keeping only a beta-function logarithm would miss the finite term. With k=1/(16pi^2), L=log(s/mu^2), and S_Q=sum Q_f^2, the derived local matching is

    (g_s,EFT-g_s,full)/u = k^2 g_s^3 S_Q [L-3/4],
    (m_f,EFT-m_f)/(u m_f)
       =k Q_f^2[-3L+5/2]
        +k^2 g_s^2 C_F Q_f^2[-3L+17/4]+higher orders.

The independent reviewer reconstructed these constants directly from the primary source before reading the author result. The complete source/vector/regulator qualifications are [reconciled separately](reviews/RECONCILIATION.md). These are known-source results after a nontrivial translation, not a new fundamental physics claim or a fitted number. No Standard Model parameter value or numerical alpha is inserted.

The scalar-gluon proton insertion gives f_g(s)=B_g[-L+3/4], with B_g=k^2 g_s^2 S_Q<p|[G^2]|p>/(4M^2). A separate propagator-filter moment is zero for a constant B/t ultraviolet density. Under the stated full-tensor OPE/remainder and matching hypotheses, this transfers the finite term to the specified sharp photon cutoff; it is not permission to equate arbitrary regulators. Higher logarithmic densities have nonzero moments. Thus a finite gluon coefficient left open earlier is now identified at the displayed operator order.

In the precisely massless three-flavor reference theory, the leading finite gluon subtraction at mu=Lambda reduces to -1/(288pi^2)+O(alpha_s) per e^2. This is a scheme-defined local matching piece, not a full mass or physical-QCD prediction.

Hadronic power counting is essential: the canonical gluon matrix element scales as 1/g_s^2 through the trace anomaly. Its unknown next Wilson order therefore contributes at the same hadronic order as the displayed mixed-quark correction. This is not a complete NLO proton endpoint or a controlled finite physical hard tail. Physical sigma data, flavor thresholds, running, higher operators and the full nonlocal tensor remain needed. Choosing a new matching scale for every photon mass also does not preserve the fixed-parameter differentiation path automatically.

## An actual absolute non-Abelian vacuum calculation

The [closed-vacuum package](global_qcd/REPORT.md) starts from normalized SU(3) Haar links on K_n=boundary[0,n]^5 with Z(0)=1. It integrates the full gauge measure, without conditioning on topology. On K1 the complete absolute partition series through beta9 contains a genuine collective cube contribution:

    log Z1=80 log c0(beta)+720 v_f(beta)^6+O(beta^10),
    [beta^6] collective log Z1=5/236196.

The bounded support search includes all connected candidate supports with no singly occupied edge, including possible branched SU3 junctions. It does not mean every ordinary connected plaquette set is a closed candidate. Two independent singlet algorithms and exact color-index contractions give the coefficient. At the deliberately tiny algorithmic beta=10^-6, the full rational Taylor polynomial has an explicit absolute partition/log error bound below 2.96e-48. This is not a physical bare coupling or a continuum precision claim.

The microscopic definition fixes the absolute integration constant; an arbitrary geometry normalization is not inserted. Exact coupling/mass thermodynamic integration supplies a route from that anchor. Actual ensembles and physical matching along that route have not been evaluated. The full K1 series is complete only in its declared finite range; general-n uniform remainders, light quarks and smooth round-sphere transfer remain open. The calculated local and cube sectors have no n3 term, but this is no physical all-order A=0 theorem.

## Actual charged sea response on a declared closed regulator

The [coordinator sea calculation](coordinator/sea_hodge/REPORT.md) includes a specified positive integer-flavor staggered determinant and canonical noncompact photon. It evaluates the leading charge-dependent vacuum term, retaining both current and contact contributions. The complete weighted photon flux covariance has trace rank(d1), giving

    W_u |_(beta kappa^4)=beta kappa^4(sum_f q_f^2)
                              (30n^4+20n^2-1)/6.

No photon-response fit or unknown numerical coefficient is used. Independent direct hopping-matrix derivatives and tree-gauge Gaussian inversions check the normalization; a separate reviewer uses exact rational inversions. The coefficient contains bulk and n2/constant terms and no n3 term. The model's globally defined ambient staggered phases have not been matched to physical continuum spin/taste transport. It uses heavy hopping and a finite-spacing polyhedral family, not physical light-quark QCD on a differentiable round-sphere radius path. The result is an actual unconditioned microscopic charge coefficient in that defined model, not the missing physical A_u.

## Joining the calculations without inventing a ratio

The [common UV ratio note](coordinator/COMMON_UV_RATIO.md) and its [review restriction](coordinator/COMMON_UV_RATIO_RESTRICTION.md) combine matching consistently. Under stated existence/RG/scale hypotheses, beta_s partial_g R=sum_f(1+gamma_f)m_f partial_mf R. A universal strong-scale shift cancels between A and M^3. At nonzero physical quark masses the remaining terms need mass derivatives of A as well as proton sigma terms. The conditional strictly massless limit does not supply physical QCD. Dividing by beta_s requires it to be nonzero or a separately controlled limit.

The required first-order ratio is still

    R_alpha=4pi[A_u/M^3-3 A M_u/M^4].

The missing all-current proton response and absolutely normalized unconditioned smooth-sphere QCD expectation values must be evaluated on the same fixed-physics path. Higher charge responses or justified finite-u dynamics are additionally required for finite-alpha dependence; an independent physical selection equation is needed to determine alpha. Controlled lattice Taylor coefficients, source calibrations and elementary matching benchmarks do not supply those values. See [routes](ROUTES.md), [reproduction](REPRODUCE.md) and [review reconciliation](reviews/RECONCILIATION.md) for exact evidence and resumption conditions.
