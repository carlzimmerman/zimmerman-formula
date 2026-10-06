# Independent audit: shift-symmetric dust-density completion

**Primary verdict: proved conditional on the declared covariant current action and retained parent quadratic action.** At any finite smooth epoch with M>0, kappa>0, Z>0, rho_d>0, b=B_rho≠0, q>0, Theta≠0 and positive finite radiation coefficients, the fully constrained formal principal system has

`omega_d²/p² -> −rho_d Z b² <0`.

This is a classical short-wavelength instability of the pure positive density square. The conclusion is not inferred from a negative kinetic diagonal alone and does not assert an admitted unstable mode below an unknown EFT cutoff. No blocking mathematical error was found in the REPORT or raw determinant implementation.

Observed HEAD: `36b9957612c8b422e900874fb053c6baa22456e4`; requested base prefix `36b995761`. Exact inspected inputs are pinned below. No author script or frozen input was edited or executed by this reviewer.

## Definitions, source action and conservation

The new interaction is `Delta L=Z(rho_d)[X−B(rho_d)]²/2`, with `rho_d=mn`, X=−(grad phi)²/2 and no explicit phi. The covariant dust action is

`−sqrt(−g)mn+J^mu partial_mu ell+sqrt(−g)Delta L`.

From `n=sqrt(−g_mu_nu J^mu J^nu)/sqrt(−g)`, differentiation at fixed metric gives `n_Jmu=−u_mu/sqrt(−g)`. Thus the current equation is precisely

`partial_mu ell=−(m−Delta L_n)u_mu`,

while the potential equation is `partial_mu J^mu=0`. Scalar shift symmetry also remains. These are particle-number/current conservations; they do not imply separate minimal dust stress conservation in this interacting theory. At fixed X the interaction changes the effective fluid energy to `e(n)=mn−Delta L`, so its pressure contribution is `Delta L−n Delta L_n`. Linearizing on Y=X−B=0 gives `delta p=rho_d Z b delta Y`. Holding the clock norm fixed yields `delta p=−rho_d Z b² delta rho_d`, the suspected negative compressibility. The constrained calculation below establishes that clock mixing cannot remove it.

The minimal current definitions and potential sign were independently checked against the primary [arXiv:1609.03599v2](https://arxiv.org/pdf/1609.03599v2), equations III.1–III.9, on 2026-10-06. Its potential is minus ell here. That source does not prove this interacting model's dispersion; the added interaction and its sign are derived in this audit.

## Actual density variation and auxiliaries

ADM current normalization gives

`n=(J0/sqrt(gamma))sqrt[1−gamma_ij(Ji/J0+Ni)(Jj/J0+Nj)/N²]`.

At a comoving background Ji=Ni=0, the second factor starts at quadratic order. Therefore

`delta rho_d=pi−3rho_d zeta`, `pi=m delta J0/a³`,

with no first-order lapse, shift or matter spatial-current contribution. Because the new Lagrangian and its density first derivative vanish on the trajectory, second-order pieces of n cannot enter its quadratic action. In particular the original spatial-current auxiliary elimination remains legitimate at this order. With unitary clock gauge `delta X=−q²nu`, the actual new quadratic term is

`Z[q²nu+b(pi−3rho_d zeta)]²/2`.

It contains no scalar shift variable t. The exact momentum constraint remains

`nu=d zetadot+e_d v_d+e_r v_r`,

`d=M/Theta`, `e_d=rho_d/(2Theta)`, `e_r=R_r/(2Theta)`.

The lapse equation still solves t through −2Theta, rather than imposing a new restriction on the retained three scalar pairs. Dust pi has the invertible algebraic equation

`pi=3rho_d zeta−(v_d_dot−nu)/(Zb²)−q²nu/b`.

Completion of the square, including the parent `3rho_d zeta nu` tadpole, yields exactly

`3rho_d zeta v_d_dot−(v_d_dot−nu)²/(2Zb²)`

`−(q²/b)nu(v_d_dot−nu)−rho_d p²v_d²/2`.

This verifies the report's density elimination and its factor/sign without assuming an effective dust sound speed. Positive Z and nonzero b are essential to this elimination; taking Z or b to zero is singular in this representation and lies outside the theorem.

## Independent leading determinant by a frequency-dependent triangular reduction

The author's exact symbolic determinant can be checked independently without reproducing its long expansion. Freeze finite coefficients and use `exp(−i omega t)`, `omega=p x`, near any nonzero x. In the reduced coordinates `u=(zeta,v_d,v_r)`, put

`zeta=tilde_zeta−i(e_d v_d+e_r v_r)/(d omega)`.

This is an invertible unit-determinant triangular transformation for nonzero omega and d, not the omission of a constraint. It makes the lapse exactly `nu=−i d omega tilde_zeta`. Transform the Euler matrix by `T(−omega)^T E(omega) T(omega)`; both triangular determinants are one, so its characteristic determinant is unchanged.

The acceleration term then supplies the unique leading clock diagonal

`E_clock=−2kappa M d² p⁴ x²+O(p²)`.

Terms proportional to `p² zeta²` and `p²nu zeta` create only O(p²) clock–matter mixing after the transformation; frozen `zetadot zeta` self terms are boundaries. All finite q²/b, Sigma, H and parent time-normalization terms are likewise lower order. Matter–matter contributions from replacing zeta by its O(1/p) piece are below their O(p²) diagonal terms. Consequently the leading matter diagonals are independently

`E_dust=p²[x²/(Zb²)+rho_d]+lower orders`,

`E_radiation=p²[R_r−2C_r x²]+lower orders`.

Clock–matter off-diagonal elements are at most O(p²); their Schur reaction through the O(p⁴) clock diagonal is only O(1), not O(p²). Thus they cannot cancel the principal matter sign. Taking the determinant gives

`det E=p⁸ [2kappa M³/(Theta²Zb²)]`

` *x²(2C_r x²−R_r)(x²+rho_d Zb²)+O(p⁶)`.

The remainder has even powers in the frozen calculation: K,V depend on p², and the antisymmetric one-derivative matrix implies `E(−p)=E(p)^T` at fixed x, so det E is even in p. This independently reconstructs the complete leading coefficient, including its sign, the factor two and the uncancelled dust factor. It does not rely on a matter-free scalar Schur coefficient. The x=0 clock branch is outside this nonzero-x triangular argument but is irrelevant to the nonzero dust roots being audited.

## Genuine dust mode and scope of the limit

For `gamma=rho_d Zb²>0`, the two roots `x=±i sqrt(gamma)` are simple: x is nonzero, the radiation factor cannot vanish there, and the derivative of x²+gamma is nonzero. Coefficients of the rescaled frozen characteristic are analytic in 1/p near these roots, so the implicit-function theorem supplies actual frozen roots converging to them. Smooth time dependence contributes lower WKB orders for sufficiently large admitted p relative to all finite background rates. Hence the stated principal limit holds, rather than just a suggestive canonical sign.

For this branch the transformed clock equation gives `tilde_zeta=O(p^(−2))` relative to the matter amplitude, thus `nu=O(p^(−1))` and `zeta=O(p^(−1))`. The density equation gives `pi≈−v_d_dot/(Zb²)`, while current conservation gives `pi_dot≈−rho_d p²v_d`. Combining yields

`pi_ddot≈rho_d Zb² p²pi`.

The mode carries nonzero physical dust density; after normalizing that density, the clock-norm and metric pieces are suppressed. Moreover `delta Y=delta X−b delta rho_d` is gauge invariant because `Xdot=b rhodot` on the trajectory. Its leading density contribution does not disappear under a smooth gauge change. This is not the earlier superhorizon negative-kinetic diagnosis which could be reframed as a Jeans potential: the growth rate scales linearly with arbitrarily large formal p.

The formal p→infinity result assumes applicability of the specified operator there. A physical EFT must exhibit a window above background rates and below its cutoff before a concrete unstable cosmological mode is claimed. No cutoff, observed growth rate or fitted cosmological coefficient sample is supplied. The report explicitly keeps this limitation. Additional pressure, operators, b=0, Z=0, kappa=0 or Theta=0 are not covered.

## Claim scope, evidence and remaining implication

The action-family scaling is correct when B and Z change with the parameter rho_v as declared. It is not fixed-coupling self-adjustment to an independently changed matter vacuum. Particle number and scalar shift current are preserved, but the matter force/pressure and off-trajectory source equations change. This result excludes the pure positive dust-density square as an arbitrarily-short-wavelength stable repair; it does not exclude every shift-symmetric completion or establish a 32pi selector.

The inspected checks.py correctly constructs the new density square, preserves matter momenta in the shift constraint, eliminates pi, and uses `E=−omega²K−iomega G−V` with the stated antisymmetric G. The numerical frozen examples are explicitly algebra controls, not on-background fits. This independent analytic reduction validates the principal coefficient universally under the stated finite-coefficient hypotheses; finite assertion counts do not supply that proof. Author runner provenance and controls remain separate execution evidence.

- `sol61_push/recombination_and_structure_growth/homogeneous_clock_current_2026_10_06/radiation_extension/shift_symmetric_matter_completion/REPORT.md`: `16eadd7ed2dca331f2d203de15773d151c12fd0e1b8fb75e302d9808e1501f36`.
- `sol61_push/recombination_and_structure_growth/homogeneous_clock_current_2026_10_06/radiation_extension/shift_symmetric_matter_completion/checks.py`: `dfc0d9b3496ad986ad7ccdfa9e9f47c5f8206b3fb0a7589beb16a336e250d6cf`.
- `sol61_push/recombination_and_structure_growth/homogeneous_clock_current_2026_10_06/radiation_extension/shift_symmetric_matter_completion/sources.json`: `711c5467ed226a35b5aad959ea64fcf9351069cbaad20be135e5eb1424c34819`.
- `sol61_push/recombination_and_structure_growth/homogeneous_clock_current_2026_10_06/radiation_extension/shift_symmetric_matter_completion/provenance.json`: `5046dfdafad45f00c1e591810f60e2311a25e0bf2e771b853d293ebc00e97015`.
- `sol61_push/recombination_and_structure_growth/homogeneous_clock_current_2026_10_06/radiation_extension/perturbations/REPORT.md`: `c5fdf8222e9ea93d13a59255c212a00b39b9911b091495ef4919d96f8d966a15`.
