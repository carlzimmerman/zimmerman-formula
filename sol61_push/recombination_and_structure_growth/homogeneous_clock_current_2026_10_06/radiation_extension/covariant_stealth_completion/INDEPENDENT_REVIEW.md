# Independent covariant stealth-completion audit

**Primary verdict: proved conditional on the declared original quadratic action and chosen monotone-clock background.** The added first-derivative scalar operator preserves that exact dust+radiation history while making its reduced clock kinetic coefficient strictly positive at every finite epoch in the stated branch. It removes the original finite-time coefficient pole. This is a changed theory with history-dependent functions; it is not an independently motivated completion, a galaxy matching theorem or a vacuum selector.

Observed HEAD: `30b858d2d7d4b1eff9916a06fcf2e3e8d70842c2`. Exact inspected source hashes are listed below. The proof reconstructs the operator variations and constrained coefficient; author check counts do not establish the conclusion.

## Normalized claim and hypotheses

Use the retained four-dimensional logKGB plus detuned acceleration response, Einstein coefficient M/2, M>0, H*>0, `0<eta<1`, `kappa>0`, and the exact homogeneous dust+radiation trajectory with `h=H/H*>1`, `q=phidot>0`, finite positive scale factor, positive finite fluid densities and `Theta=M H*(h−eta)≠0`. Work at finite epochs and nonzero Fourier k. The original full lapse/shift-constrained coefficient is

`K_c=3M eta(1+eta−h)/(h−eta)²+kappa M p_phys²/[H*²(h−eta)²]`.

Monotonic phi follows from q>0; X itself need not be monotone. Define `B(phi)=Xbar(t(phi))` on this trajectory and a smooth extension to a neighborhood. Add

`Delta L=Z(phi)[X−B(phi)]²/2`,

`Z(phi)=2M H*²/qbar(phi)^4 {lambda[hbar(phi)−eta]²+3eta[hbar(phi)−1−eta]}`,

`lambda=1+3eta²/(1−eta)²`.

These are fixed functions of the scalar in the new action, not time-dependent external coefficients after variation. Their construction encodes one specified background history and its parameters/initial charge. No independence of that history choice is asserted.

## Value and all first variations

Let `F=X−B(phi)`. The derivatives are

`Delta L_X=ZF`,

`Delta L_phi=Z_phi F²/2−ZF B_phi`.

Along the chosen history F vanishes identically, hence the Lagrangian, these derivatives and stress tensor all vanish. The scalar Euler term is `Delta L_phi+div(Delta L_X grad phi)` in the X=−(grad phi)²/2 convention; it also vanishes, since Delta L_X is identically zero as a spacetime function on the history. Merely checking its value at one instant would not justify this last step. Metric, scalar and minimally coupled matter background equations therefore remain satisfied, including the Friedmann/Raychaudhuri cancellations used in the retained perturbation action.

This is not a global shift symmetry: phi appears explicitly in B,Z. The original charge happens to obey its old background identity on the preserved trajectory because the added scalar equation vanishes there. It is not a conserved Noether charge of the modified theory for arbitrary off-trajectory solutions.

## Actual invariant quadratic term and constraints

Expansion about F=0 gives exactly

`Delta S_2=integral a_FRW³ (Zbar/2)(delta X−B_phi delta phi)²`.

Along the history `B_phi=Xdot/q`. Under a time gauge transformation, delta X and delta phi transform by their respective background time derivatives; therefore

`delta F=delta X−(Xdot/q)delta phi`

is the gauge-invariant clock-norm perturbation already used in the original crossing theorem. In unitary clock gauge `delta phi=0`, `X=q²/(2N²)` implies `delta F=−q² nu`. Thus

`Delta L_2/a_FRW³=Zbar q⁴ nu²/2`, `Delta Sigma=Zbar q⁴/2`.

There is no quadratic spatial gradient of delta phi here: the background scalar is homogeneous, so the spatial-gradient contribution to X begins at second order and multiplies the zero first derivative. Neither perturbations of Z nor the measure contribute at quadratic order because F² already starts at that order. This confirms the factor of two and excludes an omitted quadratic tadpole.

The operator depends only on phi and its first derivatives. It adds no independent field or additional temporal-derivative order. In unitary ADM variables it adds a lapse square, with no lapse or shift temporal derivative; the original nonzero-Theta shift constraint stays

`nu=(M/Theta)zetadot+rho_d v_d/(2Theta)+R_r v_r/(2Theta)`.

The lapse equation still solves the scalar shift with coefficient −2Theta. Replacing Sigma by Sigma+Delta Sigma in the full same-action dust+radiation system preserves the number of constrained scalar pairs. This statement is local to the retained admissible clock slicing; it is not a general nonlinear degree-of-freedom classification of every possible extension of the original acceleration operator.

## Positive coefficient and finite-time regularity

Set `f(h)=lambda(h−eta)²+3eta(h−1−eta)`. At h=1,

`f(1)=lambda(1−eta)²−3eta²=(1−eta)²>0`.

For h>1, `f'(h)=2lambda(h−eta)+3eta>0`; hence Z>0 at every finite epoch. The constrained kinetic shift is

`Delta K_c=(M/Theta)² Delta Sigma=M lambda+3M eta(h−1−eta)/(h−eta)²`.

More generally every constant lambda>3eta²/(1−eta)² gives the same strict Z-positivity argument and a positive constant kinetic remainder. The displayed choice is sufficient, not selected by this argument. It cancels the old momentum-independent term exactly:

`K_c,new=lambda M+kappa M p_phys²/[H*²(h−eta)²]>0`.

The radiation velocity square has its positive coefficient `C_r=2rho_r`; its velocity Hessian determinant is `C_r K_c,new`. Dust keeps its first-order density/momentum pair. All original six-state reduced equations therefore have finite analytic coefficients at a finite smooth epoch: the denominator K_c,new never vanishes, Theta remains nonzero, q remains positive and C_r remains positive. The old rank-one Fuchsian residue at a simple K_c zero is absent. Smoothness of B,Z follows locally from the analytic inverse t(phi) when q is nonzero.

This establishes elimination of that specific coefficient-pole mechanism. It does not establish stable mode growth, positive gradients, acceptable transfer functions, a regular big-bang limit, nonlinear global health or a physical CMB fit. The early radiation branch has `q~a_FRW`, `h~a_FRW^(−2)`, so the designed Z generally grows as `a_FRW^(−8)` toward the excluded initial endpoint. Finite-epoch positivity is not a uniform endpoint EFT bound.

## Preservation limits and scoped rigidity

The modified action is covariant but explicitly shift breaking and history encoded. Away from F=0, the added stress and scalar equation do not vanish; consequently the old static MOND source interior, vacuum-rescaling family and off-trajectory dynamics are not automatically preserved. A galaxy/cosmology match must be rederived in this theory. The finite A remains absent from this homogeneous quadratic calculation, so it supplies no A/H* or 32pi selection.

A narrower rigidity statement does hold: with the braiding G fixed, an added pure function Delta K(X) whose value and first variation vanish on an open X interval has Delta K=Delta K_X=Delta K_XX=0 on that interval and cannot alter this quadratic kinetic coefficient. The varying radiation trajectory contains open X ranges. This does not exclude coordinated changes of shift-symmetric G and K, extra fields, other operators, or background preservation through nontrivial cancellations; no such broad no-go follows.

## Dependency and evidence audit

The external/action-dependent leaf is the original fully varied dust+radiation quadratic action and its source dictionary. Operator value/variation, gauge invariance, Delta Sigma, unchanged constraints, positivity and coefficient cancellation are direct internal algebra. No external theorem or astronomical data is needed for this repair lemma. The original action, lapse/shift and finite-epoch hypotheses must accompany every use of the conclusion. Numerical tests, if supplied by the author, corroborate these identities in their bounded contract and do not replace the proof.

- `sol61_push/recombination_and_structure_growth/homogeneous_clock_current_2026_10_06/radiation_extension/perturbations/REPORT.md`: `c5fdf8222e9ea93d13a59255c212a00b39b9911b091495ef4919d96f8d966a15`.
- `sol61_push/recombination_and_structure_growth/homogeneous_clock_current_2026_10_06/radiation_extension/perturbations/checks.py`: `8caecc5db15be26ddec433d2d1ea3dfd96038d39984300bf0be75b5e9be23f2f`.
- `sol61_push/recombination_and_structure_growth/homogeneous_clock_current_2026_10_06/radiation_extension/REPORT.md`: `61982a07d83a0a3f672d799a5f4a33b814b35e6816ea97d72414cd24ea0790db`.

## Durable author-report review

The author REPORT and finalized checks.py have now been inspected directly. The normalized trajectory integral obeys `d phibar/dt=qbar` exactly, so the phi inverse defines local functions despite nonmonotonic X. The early current gives `qbar~x`, while the integral gives `phibar−phi0~x³`, confirming the stated Z divergence and B power. The displayed source reaction `delta rho_extra=−Zbar qbar⁴ nu` follows from `2X Delta K_X−Delta K`, and the pressure has no linear extra term; background stress-stealth is therefore correctly distinguished from source-stealth. The unchanged bare gravity gradient coefficient is not asserted to imply full reduced stability.

The squared-ansatz vacuum-map obstruction is correct for the stated fixed-coupling map: comparing X² and X coefficients forces Z to have degree −4 and B degree 2 under `phi−phi0` rescaling. The reconstructed B instead has early degree 2/3. This is a scoped failure of that specified map, not a no-go for every self-adjustment branch. No blocking correction was found in the durable report.

The updated script retains mixed scalar Hessian terms and checks the nontrivial early Z limit. Its formal p=0 kinetic samples are not used to assert the actual homogeneous constraint sector. This reviewer did not run or edit author inputs; authoritative runner outcomes remain separate evidence. Exact inspected mathematical-report/check hashes (before any run-summary append) are:

- `sol61_push/recombination_and_structure_growth/homogeneous_clock_current_2026_10_06/radiation_extension/covariant_stealth_completion/REPORT.md`: `5c79090f7bdb2226a86117f03e17cec7a89227c3c3822e9701551aa897dd87b9`.

- `sol61_push/recombination_and_structure_growth/homogeneous_clock_current_2026_10_06/radiation_extension/covariant_stealth_completion/checks.py`: `388c6035c1ddacc7c9c994c3bda72f785683cee2fc7f19b8d69e5d9e807e9c9c`.

- `sol61_push/recombination_and_structure_growth/homogeneous_clock_current_2026_10_06/radiation_extension/covariant_stealth_completion/SOURCES.md`: `ba1331cf49b1709166252a69d0faa154403f9e338048fffefb1fa13e9cf1dd30`.

Final author report revision (units and validation append, same accepted mathematical construction): `d60c43972d1815ef8fa58cee1a31d30280c740ce0e8d4f5131809bc5957b1bc1`. The author reports main_a27pass and three intended controls rejecting half/profile/vacuum-power changes; their runner validation is separate from this independent proof audit.
