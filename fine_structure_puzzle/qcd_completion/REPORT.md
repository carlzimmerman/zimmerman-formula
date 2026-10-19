# QCD completion: closed ensembles, contact sector and further gauge modes

FSP-004, continued at the user's request. **Physical R(alpha)=A_rho/mp³ and alpha(0) remain uncalculated.** The new calculations address the missing neutral ensemble, anomalous contact sector, nonspherical gauge modes and physical monopole matching. No target value was fitted. The previous phase's scientific files remain frozen.

## A charged insertion is not the neutral vacuum

The [screened exterior calculation](vacuum_matching/REPORT.md) specifies a monopole with nonzero magnetic flux in a ball. Screening removes the scalar tail's algebraic wall response, while the charged magnetic insertion retains delta log w=2pi kappa_h/R plus exponential terms, kappa_h=L/g_h². Its conditional leading core-cloud correction 2pi kappa_h m_h agrees, after normalization translation, with the known small-Higgs-mass monopole expansion. Neither expression is a vacuum metric response.

The [closed-ensemble calculation](closed_dual_qcd/REPORT.md) instead sums both signed monopole species on S3_R x S1_L, with L small and fixed. Compact integration enforces exact magnetic neutrality and integer total topological charge. It derives the tree vacuum term and complete leading dual-photon Gaussian determinant, including the canonically normalized constant eigenfunction. At fixed matched fugacity and kinetic coefficient, with mR>1,

    Delta tau_s = m³/(12pi L)
      [1-sqrt(1-(mR)^(-2)) coth(pi sqrt((mR)²-1))]
      = m/(24pi L R²)+O(R^-4).

Here tau_s=(1/L) partial_V W, V=2pi²R³, is a spatial Euclidean metric response. It is not W/(LV), which has a different leading coefficient, or an automatically specified Lorentzian cosmological energy. The retained tree plus Gaussian ensemble has zero 1/R spatial-stress coefficient. Local gravitational matching can change the R^-2 coefficient.

An exact [S3 Coulomb-kernel calculation](closed_dual_qcd/CLOSED_GREEN.md) checks the microscopic cancellation: its regular self term and every pair kernel contain the same -3/(8pi²R). In the complete action their 1/R term is proportional to (sum q)² and vanishes for a neutral finite configuration. Keeping only self energies would miss it. Fixed-separation expansion is not uniform in a thermodynamic sum; the full massive determinant supplies the separate leading screening calculation. Geometry-dependent hard/core matching and any remaining global metric functional remain uncalculated.

The [fresh normalization audit](normalization_bridge/REPORT.md) resolves a factor two in that source-to-microscopic bridge. Starting from tr(TaTb)=delta_ab/2, the specified Yang–Mills action and monopole flux 4pi force kappa_dual=g²/(16pi²L). The checked earlier source instead prints g²/(8pi²L), while retaining the same core action 4pi²/g². The invariant kappa_dual S0 is then inconsistent by a factor two; a global coupling rescaling cannot repair both equations. A second primary paper independently confirms the microscopic normalization. The frozen closed calculation correctly solves its declared scalar action, but its source-derived coupling identification is superseded by this qualification. All its formulas at fixed independently matched u,kappa or mR survive; substituting physical g requires the corrected dictionary and common fugacity matching. No previous executed input was rewritten.

## The anomalous contact sector is now included explicitly

The [compact three-form calculation](anomaly_contact/REPORT.md) on closed S4 retains the nonpropagating flux sector, the entire ghosts-for-ghosts hierarchy and its harmonic gauge volume. For V=8pi²/(3H^4) and fixed chi_g>0,

    Ztop=(2pi chi_g V)^(-1/2) sum_Q exp[-Q²/(2chi_g V)+iQtheta]
         =sum_k exp[-V chi_g(theta+2pi k)²/2].

At theta=0 the stress is exponentially small, even though the infinite-volume contact susceptibility is chi_g. A missing canonical volume factor would create a spurious H^4 response. The compact singlet with periodic mass potential is finite in its zero-quark-mass model limit and screens theta. At fixed positive pinning parameter B its exact constant-mode stress begins at B/[8(chi_g+B)²V²], of order H^8. The optional massive Gaussian singlet contribution begins at H^6 in the preceding phase's specified subtraction; its constant eigenfunction is replaced exactly once.

The [fresh independent review](reviews/contact/REVIEW.md) derives these formulas before reading the target and finds no blocking defect within the defined model. The source/hand proof of the gauge-volume factor is distinct from the normalized numerical identity checks. The compact quadratic contact model does not fix the unknown full QCD function K(F), curved hard matching or a theta-independent metric normalization. It is not a full-QCD no-go.

## Actual next angular ghost and vector work

The [next angular calculation](angular_modes/REPORT.md) derives the nonspherical adjoint ghost operator directly from Cartesian covariant derivatives. Its entire static J=1 determinant is exact, relative to the declared K=1,h=0 auxiliary comparison:

    det M1/det M1_ref = (D_RE D_M)^3,
    log(det M1/det M1_ref)
       =6x-18log x+3log(15/8)+O(x²exp(-2x)).

There is no algebraic inverse-radius term in this ghost comparison. This does not settle the gauge-vector contribution. Framed ghost eigenfunctions pair exactly with three longitudinal vector channels under the relative mixed wall conditions. Seven transverse combinations remain. The Dirichlet spherical factorization instead induces matrix Robin data with an exact partner kernel; cancellation by the bulk operator identity alone is invalid.

The intensified [full-vector calculation](angular_modes/transverse_followup/REPORT.md) derives the actual ten-channel Cartesian operator, its smooth origins and seven Dirichlet/three Robin wall conditions. It splits into two invariant five-channel systems. Its full mixed-wall vector determinant is evaluated at nine radii through x=24. Two numerical setups differ by about 4e-8 through x=16, with larger uncertainty near x=24; those finite checks are not interval bounds.

The [kernel/rank proof](reviews/kernel_rank/RAW_DERIVATION_v1.md), exact outer-mode algebra and [remainder control](angular_modes/transverse_followup/REMAINDER_CONTROL.md) now establish in the fixed auxiliary model

    log Z_J1=-3x+15log x+C+3/x+O(x^-2),  x=m_W R.

This is the complete static J1 vector-plus-ghost Gaussian, retaining the positive lifted translation state. The coefficient is derived from the operator, boundary conditions and zero-mode ranks, not fitted to the finite table. The neutral threshold and charged-induced neutral tails are controlled explicitly; a bulk pairing alone would not establish this result. The [independent finite review](reviews/vector/REPORT.md) verifies the operator and wall; a separate asymptotic review checks the tail calculation.

Even this partial-wave coefficient depends on the comparison path. [Direct substitution](reviews/BOUNDARY_PATH_CHECK.md) changes 3/(m_W R) to 18/(bR) when the wall Higgs value b=m_W h(m_W R) is fixed in the same dimensionless comparison. A physical dimensionful measure and reference transport still require matching.

The [higher-angular calculation](higher_angular/REPORT.md) now derives every fixed J>=2 from the actual quaternion angular algebra, twelve-channel Hessian and relative mixed wall:

    log Z_J=(2J+1)[-2x+(2J+3)log x+c_J
                         +(J(J+1)-1)/x+O_J(x^-2)].

Here c_J is an x-independent connection constant. The inverse coefficient through a finite cutoff N is exactly [(N+1)^4-3(N+1)^2]/2-2, which diverges quartically. The [uniform exterior proof](higher_angular/UNIFORM_EXTERIOR_v1.md) goes further than a fixed-J series: it resums the exact charged exterior polynomials through J of order sqrt(x), controls the actual charged Robin wall, and bounds their summed remainder. The logarithm stays controlled at that scale even though an unresummed solution series fails. Quantitative uniform bounds for the full regular-origin connection and neutral Schur complement remain missing. A chosen angular heat regulator's finite part is not a renormalized physical prediction.

## Four-dimensional regulation changes the electric bulk term

The [far-field derivation](far_field/REPORT.md) obtains the static charged gauge-plus-ghost density directly from scalar bubbles and the vector spin trace. For one strictly three-dimensional frequency pair it is -11(E²+B²)/(24pi m_k) in effective-action conventions. Summing those already specialized three-dimensional coefficients with a harmonic subtraction gives a useful tower model, but initially missed a finite matching term of the four-dimensional determinant.

The [independent reviewer](reviews/far_field/ADJUDICATION.md) saved a separate raw derivation before target reads and found the missing term in both common Pauli–Villars and dimensional regularization. The author confirmed it directly, and a [fresh adjudicator](reviews/regulator_adjudication/SCOPED_VERDICT_v1.md) independently derived it before target reads. For the fully integrated-by-parts bulk representative,

    K_E-K_B=L/(24pi²),
    K_B=-11L F(nu)/(48pi²) plus common coupling subtraction,
    F(nu)=-psi(nu)-psi(1-nu)-2gamma_E, nu=Lh/(2pi).

Taking the strict three-dimensional limit before the infinite frequency sum loses a term proportional to the regulator times its ultraviolet pole. A single common coupling redefinition cannot repair this electric/magnetic difference. The [coordinator oscillator check](reviews/COORDINATOR_REGULATOR_CHECK.md) also distinguishes the diagonal heat-kernel representative from the integrated bulk density; their surface integral itself contains 1/R. Original executed raw files and runs are preserved, with the [correction recorded separately](far_field/ADDENDUM_2026-10-19_COMMON_PV.md). Their successful algebra checks did not establish the disputed four-dimensional interpretation.

In that corrected bulk convention, including the quartic periodic potential on the off-shell Coulomb profile h=v-1/r gives the loop logweight coefficient

    a_loop=L/(2pi)-11L(1+n_mag²)F(Lv/(2pi))/(12pi).

This is a coefficient of a local exterior bulk integral, not the complete finite-wall determinant. The electric correspondence with the source's additional equation-of-motion convention remains separately qualified; the magnetic digamma/beta-function match survives. With scalar screening, the electric and potential algebraic tails disappear. The remaining charged magnetic bulk tail is +2pi kappa_B^eff/R, where kappa_B^eff=L/g_H² plus its derived magnetic loop correction. Its dual stiffness is 1/(16pi² kappa_B^eff), consistent with the independent microscopic normalization bridge. Neutrality, hard matching and boundary/global contributions are still required for a vacuum-stress claim.

## All-mode benchmark and the exact missing physical arrow

The [common-holonomy caloron source translation](vacuum_matching/REPORT.md) includes its all-mode determinant and collective-coordinate measure. It cancels the determinant's inverse-core-mass terms against the Jacobian and leaves a logarithmic inverse-*separation* correction. Its constituent separation and intermediate matching cutoff cannot be relabeled as a cosmological radius. The deformed holonomy potential also forces scalar screening; an undeformed Coulomb profile is not a uniform large-distance saddle. Source typos are preserved in exact-version receipts and do not support novelty claims.

These results show where several proposed 1/R assignments fail in explicit controlled calculations. They do not produce the physical QCD numerator A_rho or its electromagnetic dependence. A successful continuation needs the complete microscopic gauge-to-effective metric matching for a declared state and geometry, full matter and charge normalization, and the independently matched proton response on the fixed-proton constraint. Pure Yang–Mills g is not electromagnetic alpha. Ordinary susceptibility or a disorder-insertion fugacity cannot supply the missing theta-independent metric functional by themselves.

The [neutral/matching review](reviews/neutral_matching/REPORT.md) independently verifies the closed determinant, Coulomb cancellation, matching sensitivities and screened-exterior mathematics, while keeping microscopic normalization separate. The phase checkpoint collects current runs and separate source/hand-proof pins. Previous failed resource launches are preserved as environment outcomes, not physics evidence. The original fine-structure goal remains open.
