# Independent audit of the cold-dominated geometry and energy-mode bootstrap

19 October 2026. Auditor `/root/audit_cold_checkpoint`, independently dispatched from raw claim/proof files. Analytic audit only. This report is the auditor's only write. No scientific scripts, numerical calculations, discretized arrays, or process inspection/control were used. Source text and metadata were read with `cat`, `sed`, `rg`, and `shasum`; the proof-audit skill and its general-logic checklist were applied.

## Normalized claim and primary verdict

**Primary verdict: proved as written for the selected cold-dominated family, with the bootstrap's explicit finite resonant-chart contract retained.** The resulting claim is a family-existence and mode-regularity checkpoint. It proves neither existence nor absence of a self-consistent mode with a nonzero fundamental circular force trace, and it proves no frequency-dependent reduced inverse.

More precisely, fix the exact hollow profile, the exact two-species shell kernels, `f=1/64`, `ell=D r_M`, and the four dimensionless radii `(1,2,3,4)`. There are arbitrarily large, nonexceptional `D` such that both circular epicyclic frequencies have finitely many simple stationary points. For each such fixed member one can choose a sufficiently small **positive fixed** warmth `delta`, with all the exact-inverse requirements retained. On the resulting occupied action domains:

* the full frequency gradient never vanishes;
* eccentric cap receivers are reached by interior regular resonance curves, and actual energy modes have bounded receiving detuning quotients there;
* physical radial endpoint accumulation creates no additional modal-work divergence;
* every actual finite-energy eigenmode has a `C^(1,1)` radial field under the finite-chart contract; this also resolves an eccentric definite-Morse quotient whenever such a chart occurs in the more general contract;
* at a simple circular extremum, higher harmonics have bounded modal quotients, while the fundamental quotient is bounded exactly when the mode's own species force satisfies `phi_j'(s_c)=0`.

The construction quantifies as “for a suitable fixed `D`, choose `delta>0` sufficiently small.” It does not provide one warmth valid uniformly as `D` tends to infinity and does not certify an unspecified numerical halo.

There is one precision point outside the concrete cold-family application. The bootstrap's Section 1 item 4 only states that an otherwise unspecified boundary source is bounded. That is enough for qualitative `C^(1,1)` membership. The proof's displayed quantitative estimate with one constant `C_nu` additionally uses a boundary source bound controlled linearly by `||h||_Q`; that control is not explicitly included in the abstract wording of item 4. The concrete cap and endpoint arguments audited here do supply it. Thus the abstract quantitative estimate should retain that quantitative boundary input unless supplied separately; no stronger arbitrary-boundary estimate is being certified by this report.

## Claim card and model

The coefficient domain is complex, allowing one mode `exp(-i nu t)`, with real `nu !=0`; a real perturbation is recovered by the conjugate pair. Species order is `(t,f)`. The angular momentum variable `L` is squared specific angular momentum, `J>=0` is ordinary radial action, and `L=L_c(s)` with `L_c'>0`. The physical and action measures are

`dGamma=C_Gamma dr dv dL`, `dm=2*pi*C_Gamma dJ dL`.

The exact susceptibility is `w_j=-F_(j,E)>0` in the open occupied set, smooth with compact physical support and flat physical edges. An actual mode is a nonzero accessible energy-space eigenvector satisfying both the kinetic equation and `phi=P h`; it is not merely a prescribed numerator divided by a detuning. Weighted energy finiteness gives `sum integral |h|^2/w dGamma<infinity`. The mode equation is

`h_(j,k)=-w_j k Omega_j phi_(j,k)/(k Omega_j-nu)`.

The physical kernels are exactly

`P_ff=P_ft=P_tf=-G/max(r,r')`,

`P_tt=2(G^2/a_0) integral_(max(r,r'))^infinity M_t(s)s^-4 ds`.

The exact smooth inverse is a source theorem used for existence and smooth compact support of the chosen equilibria; this audit checked its hypotheses against the new parameter choice. A full re-audit of every Fourier/Sobolev estimate in that inverse is outside this focused assignment. Likewise, no external theorem or literature attribution is being verified here.

## Dependency graph

1. Exact profile and circular force laws → formulas for `L_c`, `kappa^2`, and their radial derivatives.
2. Actual cutoff derivative bounds and analyticity on the inner taper → locally finite exceptional parameter set → finitely many nondegenerate circular extrema for generic fixed `D`.
3. Positive circular well, exact oscillator expansion, and twist identity → nonzero full gradient on the circular line → by compactness, no full critical points in a sufficiently narrow occupied tube.
4. Smooth action-energy inverse → cap action and cap frequency expansions → same-sign cap normal form → interior resonance approach → actual-mode energy trace zero plus `C^1` division.
5. Smooth compact physical susceptibility plus accessible zero mass → arbitrary-order endpoint decay of cumulative perturbation mass and force → endpoint detuning absorption.
6. Initial weighted-energy field estimate + kinetic equation + finite chart geometry → bounded physical radial density → exact shell field equation → `C^(1,1)` field.
7. `C^(1,1)` field + actual circular oscillator harmonics + same-sign circular detuning → the exact fundamental force-trace criterion.
8. Exact single-mode time integration → bounded work iff the relevant receiving quotients are bounded. None of steps 1–7 asserts a global reduced spectral inverse.

The leaves in 1, 3–8 are reconstructed algebra or local analytic estimates below. Step 2 uses the elementary cutoff bounds already given in the pinned geometry source; their applicability and constants were checked. Exact equilibrium existence and the accessible energy-space formulation are inherited source inputs. There is no load-bearing computation.

## Obligation matrix

| Obligation | Result | Decisive check |
|---|---|---|
| Actual cold-dominated parameter regime | passed | `M/M_b=D x` on the law annulus; deep and core ratios tend to zero with fixed `f` |
| Generic finite simple circular extrema | passed | compact inverse images of analytic parameter maps, and exclusion of constant branches |
| Nonzero full gradient at each circular extremum | passed | `Omega_J=kappa''/(4 kappa)` |
| Fixed positive warm tube | passed | choose warmth after fixing the nonexceptional member; exact inverse hypotheses remain available |
| Cap approach and trace division | passed | the actual nearby resonant graph lies on the occupied side at a stationary cap point |
| Physical endpoint flatness | passed | Cauchy–Schwarz against integrated physical susceptibility, using zero total mass at the outer edge |
| Circular physical density estimate | passed | the singularity is integrable in the two variables `(v,L)` at fixed radius |
| Eccentric turning-point density estimate | passed | logarithm times a translated fold kernel is uniformly integrable |
| Nonresonant harmonic tail | passed | bounded first term and absolutely summable `k^-2` remainder |
| Mode field `C^(1,1)` | passed | bounded density and the exact two-species force equations |
| Abstract uniform bootstrap norm with unspecified item 4 | conditional | the unspecified bounded-source input must carry a bound linear in the mode norm |
| Definite-Morse quotient after bootstrap | passed under the stated chart contract | energy zero jets and Lipschitz gradient give quadratic domination |
| Circular fundamental “iff force zero” | passed | leading first harmonic is `rho phi'(s)/2`, with `rho~sqrt(J)` |
| Actual mode with nonzero force trace | not addressed | no homogeneous field-equation solution is constructed |
| Global cancellation of every force trace | not addressed | no spectral exclusion or cancellation identity is proved |
| Frequency-dependent reduced boundary inverse | not addressed | mode-by-mode bounds do not supply it |

## Reconstruction of the parameter and cap arguments

For the exact profile, normalized circular angular momenta are

`lambda_cf=x[1+D p]`,

`lambda_ct=x[1+(1-f)D p]-f^2 p^2/x`.

Since `kappa^2=lambda_c'/x^3`, differentiation gives exactly the claimed

`(kappa_f^2)'=x^-4[-3+D B]`,

`(kappa_t^2)'=x^-4[-3+(1-f)D B-f^2 C]`.

The bound `C>=-2858` and `f^2=1/4096` give `3+f^2 C>2`. Outside the inner taper, `p'>=0`, `p''<=0`, and `p>0`, hence `B<0`; at the inner edge `B=0`. Every derivative zero is therefore in the open subset `B>0` of `(1,2)`. At `x=3/2`, the exact cutoff identities give `p=3/4`, `p'=7/2`, `p''=4`, hence `B=3/2`.

For a parameter range `a<=D<=b`, `a>0`, an inverse image under `D_f=3/B` has `B>=3/b`; an inverse image under `D_t=(3+f^2 C)/((1-f)B)` has `B>=2/((1-f)b`. These inverse images stay away from both taper endpoints. Any identity `D_f=constant` or `D_t=constant` on a component cross-multiplies to an analytic identity on all `(1,2)`; its limit at `x=1` would assert `3=0`. Thus the derivatives of these parameter maps have finitely many zeros on each relevant compact set. Their critical values are locally finite. At a root, nonzero derivative of the parameter map is equivalent to nonzero second radial derivative of `kappa`; the remaining multiplicative factors are nonzero. The parameter-exception argument is therefore valid, including finiteness of the roots themselves. Removing a locally finite set leaves arbitrarily large admissible `D`.

The stated mass ratio follows without approximation from `A=M_b/r_M` and `ell=D r_M`. The exact inverse's deep and circular-core restrictions become `f/D` and `2f^2/((1-f)D)`, respectively. For each fixed sufficiently large admissible `D`, the inverse applies to the same exact forces and profile.

The twist identity can be checked without assuming monotonicity. With `K=kappa^2` and `U=Phi+L/(2r^2)`, differentiation at the circular well gives

`U_rrr=K'-3K/s`, `U_rrrr=K''-3K'/s+15K/s^2`.

The cubic/quartic oscillator expansion gives

`Omega_J=U_rrrr/(8K)-5 U_rrr^2/(24K^2)`.

At `K'=0` this reduces to `K''/(8K)=kappa''/(4 kappa)`. Hence at each simple circular stationary point the `J` derivative is nonzero; elsewhere the `s` derivative is nonzero. The closed circular interval is compact and has only finitely many such points. Its gradient has a positive minimum, so continuity supplies the narrow tube used in the proof.

The cap energy is `eta=delta^2 kappa^2 h^2`. Substitution into the smooth inverse `J=eta/kappa+O(eta^2)` gives the claimed `J_b`, including the fixed finite-order smooth parameter bounds. Therefore `g_delta=Omega(J_b(s),s)=kappa+O_C2(delta^2)`. Simple stationary points persist uniquely and no new ones arise away from their fixed neighborhoods. At each perturbed stationary cap point the `J` derivative and `g_delta''` have the same nonzero sign.

In cap coordinates `z=J-J_b(s)<=0`, the resonant level thus has `z=-(b/(2a))x^2+O(x^3)<0` for small nonzero `x`. It lies inside the occupied set on both sides of the contact. Weighted energy forces the numerator to vanish along that interior regular level; continuity supplies the cap point itself. Dividing in `J` at fixed `s` is then legitimate because the whole segment between an occupied point and its nearby resonant root stays on the occupied side. At a transverse cap crossing, the detuning and boundary coordinate form valid joint coordinates, so the same division works while keeping the boundary coordinate fixed. This checks the side-of-domain issue; flatness of `w` alone is not used to force a cap trace zero.

## Physical endpoints and the field bootstrap

For either species, compact smooth physical support makes `chi(r)=C_Gamma integral w dv dL` smooth and flat at both physical radial endpoints. For an accessible perturbation,

`|m(r)|<=||h||_A [integral_edge^r chi(s) ds]^(1/2)`.

At the outer endpoint the representation from that endpoint uses the separately zero total perturbation mass. Arbitrary-order flatness yields every power `d^N` after taking the square root. The exact force matrix is smooth on the positive-radius shell, so `phi'=-H m` has the same decay. An orbit centered at endpoint distance `d` has radial excursion `O(delta d^2)`, hence its entire radial range has comparable distance and every nonzero field harmonic has arbitrary-order decay. Endpoint circular derivatives are strictly negative from the explicit derivative formulas. Since `J<=J_b=O(d^4)`, an exact endpoint resonance has detuning bounded below by `c d`; otherwise the denominator stays separated from zero in a sufficiently small endpoint neighborhood. The flat numerator absorbs this factor. Only finitely many harmonics can resonate at one fixed mode frequency, and the field Fourier tail is summable. This establishes the claimed endpoint conclusion for actual modes.

The initial energy-to-field regularity itself is consistent with the exact model: Cauchy–Schwarz gives `|m(r)-m(s)|<=C ||h||_A |r-s|^(1/2)`, and `phi'=-H m` gives `C^(1,1/2)` fields. Thus the bootstrap starts with information genuinely available before division.

At an eccentric definite-Morse resonance, positive weight and energy force `N(q_c)=0`; the already available `C^1` coefficient then gives `N=O(|q-q_c|)` and `h_k=O(1/|q-q_c|)`. Near a turning radius, `partial_J r_+=Omega/U_r` is nonzero. In local action coordinates `(x,y)` with turning-radius displacement `x`, integration in `y` gives `C(1+|log|x||)`. The remaining density has the kernel `1_allowed |z-x|^-1/2`. Hölder with exponents `3` and `3/2` bounds it uniformly in `z`: the logarithm is in `L^3`, and the translated fold kernel has uniformly bounded `L^(3/2)` norm on the fixed interval. The orbit's other turning point stays separated in this eccentric chart.

At a simple circular extremum, set `x=s-s_c`, `z=r-s_c`. The positive well gives `J~v^2+(r-s)^2`, hence `J+x^2~v^2+z^2+x^2`. The initial field bound yields `|phi_k|<=C sqrt(J)` and therefore

`|h_k e^(ik theta)|<=C/sqrt(v^2+z^2+x^2)`.

At fixed radius, integration is over `(v,x)`, since `dL=L_c'(s) dx` with bounded positive Jacobian. The integral of this bound over a fixed two-dimensional disk is uniformly finite. Thus the singular action-angle behavior has not been mistaken for a bounded physical Jacobian.

Regular division charts and the concrete cold-family cap/endpoint charts give bounded physical sources controlled by the initial field or energy norm. For the high-harmonic tail,

`h_k=-w phi_k-w nu phi_k/(k Omega-nu)`.

The first sum is the bounded composed radial field minus its orbit average and a finite Fourier polynomial. Radial `C^1` regularity gives `phi_k=O(k^-1)`, and the second sum is absolutely `O(k^-2)`. There is no missing infinite resonant sum. Consequently the radial density is bounded. The exact equations

`phi_f'=G(m_t+m_f)/r^2`,

`phi_t'=-2(G^2/a_0) M_t m_t/r^4+G m_f/r^2`

then make `phi'` Lipschitz. This is a kinetic-to-density-to-field bootstrap, not use of an assumed boundary inverse. Afterward, at a definite-Morse point energy also forces the first coefficient jet to vanish. The Lipschitz gradient gives `N=O(|q-q_c|^2)`, exactly enough for the quadratic detuning quotient.

## Circular criterion and the exact remaining gap

At an interior simple circular extremum, the verified twist identity gives

`k Omega-k kappa(s_c)=a_k J+b_k x^2+O(J^2+J|x|+|x|^3)`, `a_k b_k>0`.

The absolute detuning is comparable to `J+x^2`. For the actual radial oscillator, `r=s+rho cos(theta)+O(rho^2)`, `rho=sqrt(2J/kappa(s))`. A radial `C^(1,1)` field therefore has

`phi_1=(rho/2) phi'(s)+O(rho^2)`, `phi_k=O(rho^2)` for `|k|>=2`.

Higher harmonics have bounded quotients. If `phi'(s_c)=0`, Lipschitz continuity gives `|phi_1|<=C(sqrt(J)|x|+J)<=C'(J+x^2)`. Conversely, if `phi'(s_c)!=0`, the line `s=s_c`, `J>0` is inside the occupied set for all sufficiently small `J`, and the quotient is a nonzero constant times `J^-1/2+o(J^-1/2)`. This verifies both directions of the criterion on the actual receiver domain.

The local integral `integral J/(J+x^2)^2 dx dJ` is finite: scaling `x=sqrt(J)y` gives a bound `C J^-1/2` before the final `J` integration. Thus energy membership by itself does not force the circular force trace to vanish. This is a prescribed local response check, **not an actual eigenmode counterexample**. It does not decide what the complete homogeneous field equation forces.

The exact modal-work identity is `sup_t |W_k|=2|nu| |phi_k|/|k Omega-nu|` away from resonance. Therefore the criterion concerns the supremum over nearby eccentric receivers even though all nonzero harmonic coefficients vanish on the circle itself. A nonzero force trace in an actual mode would obstruct a whole-receiver modal-work bound. No such mode has been produced here, and no theorem excludes it. The first remaining implication is precisely:

`actual homogeneous energy-mode equation at a fundamental circular threshold => phi_j'(s_c)=0`,

or, alternatively, spectral exclusion of all such modes. The reduced frequency-dependent boundary inverse remains a separate obligation even if this implication is proved. Radial force locality and endpoint field data do not supply a local uniqueness ODE because the modal source contains complete orbit integrals.

## Exact revisions and provenance

Authorial self-review labels were not used as evidence. The target formulas, domain geometry, density pushforwards, and force criterion were reconstructed independently from the raw files. Independence here means a fresh isolated audit, not an external proof certificate or a guarantee against shared model error. No repository source or ledger was changed.

SHA-256 pins at reading (repository paths relative to `/Users/carlzimmerman/new_physics/zimmerman-formula`):

* `real_research/analytic_review_2026_10_18_codex/cold_dominated_feedback_2026_10_19/GEOMETRY_AND_CAP.md`: `c40c5f63e533fe19e41b996e292d21892160bf2b4aa31ffb499313b64f54fc0d`.
* `/private/tmp/threshold_bootstrap_20261019.md`: `40304ae8d1c0495cdd7482202aa9dcdfa494f12287754b7e648dd2adf26a77b5` (matches the assigned revision).
* `real_research/analytic_review_2026_10_18_codex/actual_feedback_2026_10_19/GEOMETRY_AND_SCALING.md`: `1848347266a2254e18fc579c3c6804cd6703895ce9d298f804a69acd977558c9`.
* `real_research/analytic_review_2026_10_18_codex/actual_feedback_2026_10_19/SPECTRAL_OPERATOR.md`: `52c042ff02f04c0e6917e2591d9527fbf07952ce64b6f674b240f83e4c9fb47c`.
* `real_research/analytic_review_2026_10_18_codex/actual_feedback_2026_10_19/SINGULAR_PENCIL_AND_MODES.md`: `3c091ca4be949d0bdf3c1657897a962cb7f60b137f03657c23b8af80a25e5c94`.
* `real_research/analytic_review_2026_10_18_codex/smooth_exact_2026_10_18/EXACT_SMOOTH_INVERSE.md`: `490b137269ea5c918dae517085974752a3e1bc3d9df4f3e88b99eeccde41a55b`.
* `real_research/analytic_review_2026_10_18_codex/claude_continuation_2026_10_19/full_feedback/RESULT.md`: `a69a6cfde21ccdd1a9a2fbced2e0613ac99ba1bc6fe3571dbb377d645756d4fb`.
* `real_research/analytic_review_2026_10_18_codex/finite_halo_2026_10_18/BOUNDARY_MATCHING.md`: `eab2312cf87a23267dd639c064ee8fb39a5b07d809e27ffae0b3eedd1557b774`.

The cheapest next substantive check is the actual homogeneous circular-threshold mode equation. Rechecking flatness or local energy integrability cannot decide that remaining spectral condition.
