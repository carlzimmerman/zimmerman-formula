# Scoped analytic and source review

2026-10-20. Reviewer: critical_gauge_current. No Lean edits, compilation or
git commits were performed in this review.

**Primary verdict: proved as written for the reviewed scoped analytic
claims.** The report explicitly leaves the coupled weak-gravity continuation
conditional on a regular constraint/gauge reduction and a valid cutoff; this
review does not turn that condition into a completed full-gravity theorem.
No healthy microscopic normalization or end-to-end physical proof is claimed.

## Exact artifacts and provenance

- RESULT.md SHA-256:
  `b20f279bf75f3ad4ffa192cf41c5f92409a5e9346f2e369c57d9320c3878236e`.
- SOURCES.md SHA-256:
  `2ade5450142277792316742a7b801997c6443a8d54c6c106dfbfcbef3c70fe3f`.
- GravitySelection.lean source/type-scope review SHA-256:
  `fd0145d1e60ff5cc020a15700f7a6378c0d33d5e465eba2962549b6aebcaf6c4`.

The pure-BM de Sitter packet and nine initial Lean declarations were authored
by this reviewer. Their integration review is therefore self-review, not a
new independent confirmation. The vector_completion_audit agent separately
reconstructed the raw de Sitter action, both constraints and redshift boundary
from the specified action. The rational-model Bianchi-I, finite-k and
conformal-source calculations were supplied by gap_selection_physics; this
review reconstructed those equations from the written action before accepting
their conclusions. All agents share a model family; this provenance is not a
claim of methodologically independent experimental evidence.

## Claim and dependency graph

The claim reviewed is the conjunction of the following restricted arrows:

1. Specified bosonic rational action and regular selected auxiliary branch
   -> Bianchi-I stress/lapse equation and frozen finite-k determinant.
2. Additional regular weak-gravity reduction and EFT validity assumptions
   -> conditional persistence of the separated negative root.
3. Universal conformal matter action and the stated local weak-field UV
   limit -> source charge, tensor/scalar Newton couplings, physical potentials,
   PPN coefficient and normalization cube.
4. Specified BM action on its exact de Sitter vacuum, nonzero k and H>0
   -> lapse/shift reduction, redshift boundary and positive kinetic with no
   quadratic restoring term.
5. BM stationary weak-field metric/source reduction and the explicit
   f_delta deformation -> actual static amplitudes and nonselection by the
   homogeneous quadratic test.

Leaves include the authenticated component/action dictionaries, the selected
finite-gradient branch, stated boundary/domain restrictions and the explicitly
uncomputed full metric continuation. None of these arrows derives a quantum
completion, selects a coupling, or identifies the rigid scalar-only ratio with
the actual tensor-plus-scalar prediction.

## Obligation matrix and decisive checks

| Obligation | Verdict | Reconstructed evidence and scope |
|---|---|---|
| Rational Bianchi-I stress and lapse | Passed | The reduced kinetic terms are -3(M_Pl^2+M/2) alpha_dot^2 +3(M_Pl^2-M) beta_dot^2. Lapse variation reproduces the displayed constraint. The gradient stress has p_parallel=-E+h^2 E_X and p_perp=-E. This is a local consistent background, not a global halo solution. |
| Finite-k real mode | Passed | Eliminating the regular auxiliary affects b, while the frozen determinant is exactly (K w-b k^2)[M(w-k^2)+jH^2]-j^2H^2 w. Its negative constant term for 0<k^2<m_b^2 gives a simple negative root. The point E/V0=283/252 and both displayed mass ratios were independently recomputed. |
| Coupled metric continuation | Conditional | The report retains the regular finite-k constraint/gauge reduction, compatible data and validity window as hypotheses. The complete mixing matrix, finite-coupling threshold, microscopic cutoff and strong-coupling control are not computed. A fixed-metric negative root alone would not prove arbitrary-coupling gravity instability. |
| Conformal source and force signs | Passed | -m exp(q phi) ds gives the same q for the source and test body. The final report explicitly chooses q>0 by scalar orientation and m>0; q=0 is excluded from a scalar MOND force. |
| Tensor and scalar UV calibration | Passed | Static aligned clock variation gives Gt=1/[8pi(M_Pl^2-M/2)], not bare G. The spatial metric variation still gives psi=-n. Scalar energy is consistently higher weak-potential order in this local calculation. |
| Physical potentials and cube | Passed | Phi_phys=Phi_E+q phi and Psi_phys=Psi_E-q phi give gamma_UV=(Gt-Gs)/(Gt+Gs)=1-2f. Matching the leading IR scalar force to Guv gives a_IR=f a_s, hence xi_V0=xi_scalar f^3. This is an unscreened local UV coefficient, not a global PPN calculation about the MOND vacuum. |
| Density footing | Passed | Gcos=1/[8pi(M_Pl^2+M/2)] gives epsilon_inf/V0=(1-r)(1-f)/(1+r). The inferred xi therefore multiplies xi_V0 by Guv/Gcos. The two target counterfactuals are correctly kept distinct. |
| Pure-BM de Sitter constraints | Passed; self-review | Shift U=0 gives n=zeta_dot/H at nonzero k. Lapse fixes B=X_k zeta/H+(eta X_k+2mu^2)zeta_dot/(2H^2), rather than imposing another scalar constraint. The singular flat lambda=1 corner is not obtained by dividing by lambda-1. |
| Redshift boundary | Passed; self-review | Wdot=3HW and X_kdot=-2HX_k give d(2WX_k zeta^2/H)/dt=2WX_k zeta^2+4WX_k zeta zeta_dot/H. Holding X_k fixed would spoil the required cancellation. H is constant on this de Sitter background. |
| Retained scalar interpretation | Passed; self-review | For pure BM and finite nonzero k, the coefficient W eta X_k/H^2 is positive. Its equation gives zeta=C1+C2 exp(-Ht). There is no quadratic restoring term; this is not gauge removal or full nonlinear health. k=0 and H->0 are excluded from this reduction. |
| Optional KT term | Passed; self-review | At its exact Q=1 condensate, K=mu^2(Q-1)^2 adds +2mu^2 n^2 and zero background energy. It changes the reduced kinetic coefficient but adds no restoring term at that vacuum. Other cosmological states are outside this statement. |
| BM static amplitudes | Passed; self-review | Source -rho Phi and the actual high/low acceleration limits give C2_B=1/(8piG), C3_B=1/(12piG a0), epsilon_B=f_B0/(8piG), and R_B=4f_B0/(9a0^2), in c=1 units. |
| f_delta nonselection test | Passed; self-review | The added term begins at a^3 and decays at infinity. It preserves f_B0, f_B''(0), the high-acceleration constant, the homogeneous vacuum and all its quadratic terms. It rescales C3_B by 1+delta and R_B by (1+delta)^2 near zero. No all-background health of the deformed family is inferred. |

The inferred-target bound uses 0<r<1/2 and 0<f<1. If f<=1/4, then
f^3/(1-f)<=1/48 and (1+r)/(1-r)<3. Together with pi<4 this excludes
xi_inf=1/4. Thus f>1/4 and gamma_UV<1/2 follow only as downstream
counterfactuals. They do not select q and are not the unique-gamma prediction
on the actual-V0 footing. The scope of the Cassini comparison is correctly
conditional on this local unscreened UV metric applying to that experiment;
no measured value enters the action or bound.

## Primary-source checks

The following exact versions were read online in this work; no source was
downloaded. Their hypotheses and translations agree with the report:

- Foster--Jacobson, gr-qc/0509083v2, 8 February 2006: the pure-aether action,
  Newton/cosmological coupling dictionaries, gamma=1 and tensor speed. The
  pure-aether PPN result is not imported as a hybrid conformal-matter theorem.
- Pujolas--Sibiryakov, 1109.4495v1, 21 September 2011: the real global
  super-aether derivative sector and its gravitational limitations. Its flat
  c2+c3 relation does not uniquely choose the report's covariant c1-only model.
- Marakulin--Sibiryakov, 1610.07805v3, 25 October 2021: a linearized
  supergravity construction exists. It is not a nonlinear completion or a
  finite-gradient health result for this rational model.
- Nitta--Sasaki, 1406.7647v3, 4 November 2014: the saturated chiral component
  normalization and algebraic bosonic auxiliary equation; not the selected
  rational branch's microscopic normalization.
- Blanchet--Marsat, 1107.5264v1, 26 July 2011: ADM action, lapse acceleration
  and stationary MOND source. Its thermal example is not a microscopic
  selection principle. HTML and PDF equation-number conventions are separated.
- Flanagan, 2302.14846v3, 24 September 2023: stationary low-acceleration
  stability has the named symmetry, density/sign and conventional-MOND
  stability hypotheses. It is not an all-background result for the hybrid
  model or an arbitrary f_delta deformation.
- Blanchet--Skordis, 2507.00912v1, 1 July 2025, and the full
  2404.06584v2, 27 November 2024: the KT term and retained flat scalar are
  correctly scoped. The nonlinear AeST implication cited by the full paper
  has not been independently verified here and is not used as health evidence.

SOURCES.md G8 records the report author's direct authentication of the Cassini
original abstract. This reviewer checked the stated downstream transfer scope,
but did not independently repeat that experimental-source retrieval. No new
likelihood, confidence conversion or observational exclusion of every clock
theory is asserted.

## Formal scope and remaining gap

The final Lean source contains fourteen declarations and fourteen axiom-print
commands. Source/type inspection confirms that the de Sitter reduction is
conditional algebra, the lapse increment is a polynomial certificate, actual
pi is not formalized, the tensor/scalar cube assumes its source calibration,
and the band statements prove polynomial signs rather than the existence or
physical interpretation of a constrained mode. Root performed the compilation
and controls; this review did not rerun or independently validate those logs.

Three forced local clarifications found during review were integrated before
the pinned freeze: q>0 and m>0 in the scalar bridge, nonzero k in the de Sitter
shift inference, and removal of an imaginary-clock sector absent from the
declared real-vector action. No remaining substantive correction was found.

The strongest safe outcome is the report's stated one: a conditional
finite-gradient instability discriminator, an independently testable static
source/PPN bridge, and a pure-BM lapse/shift loophole with a retained degenerate
scalar. Full constrained finite-coupling dynamics, a controlled microscopic
cutoff/quantum completion and an independent vacuum/cubic selection equation
remain missing. No reviewed result completes the original why-4 goal.
