# Independent normalization screen review

**Verdict: proved as written under its stated Einstein/weak-field, spherical-source and static deep-response assumptions.** I reconstructed the formulas independently while deriving the algebraic-source report, then read the screen and script. No peer script was executed and no peer output was modified.

Inputs reviewed at these hashes:

- `sol61_push/puzzle_32pi/vacuum_coupling_2026_10_06/NORMALIZATION_SCREEN.md`: `ad244092159a2cf4c7d9a16a4a302995e566b2c5269ee72ecdc5057d5d6f243b`
- `sol61_push/puzzle_32pi/vacuum_coupling_2026_10_06/normalization_checks.py`: `84294c08a9bae3ca657fa5b163bf7e34b91a0cbcf8661c134319a6d2c48e307c`

The Einstein/Gauss calibration agrees with the independent derivation: trace reversal gives `R00=kappa_E rho c²(d-3)/(d-2)` for dust, whereas weak-field geometry gives `R00=Laplace Phi/c²`. Integrating over the unit sphere fixes the Poisson factor `Omega_(d-2)`. Thus `kappa_E c⁴/G_N=(d-2)Omega/(d-3)`, with `G_N` defined by the physical acceleration `G_N M/r^(d-2)`. This agrees with differentiation of the Tangherlini mass-normalized potential. The restriction `d>=4` is necessary: spacetime three has vanishing dust `R00` coefficient and no such inverse-power calibration.

For `f=1-mu/r^(d-3)`, direct differentiation makes both displayed vacuum Ricci combinations zero. Its nonextremal horizon has `a_H=c² f'(r_H)/2=(d-3)c²/(2r_H)`. Therefore the conditional assignment `a_H=a0` and the additional invariant `J=1` give the stated `a0` and coefficient `4(d-2)Omega/(d-3)^3`. This equals `32pi` in four dimensions, `3pi²` in five, and `128pi²/81` in six. It is a correct conditional dictionary; neither a horizon-to-galaxy identification nor `J=1` follows from the vacuum metric. The screen makes that distinction explicit.

Variation of the displayed static action gives `div(|grad Phi|^(p-2)grad Phi)/(Omega G_N a0^(p-2))=rho`. Integrating the spherical source equation yields `g^(p-1)/a0^(p-2)=G_N M/r^(d-2)`, without a hidden dimension-dependent rescaling of `a0`. Hence `v²=gr` has radial exponent `1-(d-2)/(p-1)`. Both continuations in the screen follow: `p=3` retains the quadratic acceleration law; `p=d-1` retains flat speeds and gives `v^(2(d-2))=G_N M a0^(d-3)`. Their coefficients are consistent with the written action and they coincide only at spacetime four among the admitted dimensions. The Lagrangian has energy-density units for every such `p`; this is not a relativistic kinetic-health check.

The homogeneous conservation law is `rho_dot+(d-1)H(1+w)rho=0` for the separately conserved, constant-`w` component. A scale proportional to `sqrt(G_N rho)` with fixed `G_N` then has exactly the displayed exponent, including dust, radiation and vacuum special cases. It remains an instantaneous-tracking prescription; formation memory or response to a different density changes the premise.

The script implements these restricted symbolic identities and dimension examples. Its checks do not establish a microscopic selector, full covariant completion, high-acceleration limit or empirical evolution fit, and the prose does not claim those implications. The same coefficient `G_N rho` can enter dimensionally correct proposals with different `kappa`, `p`, boundary data or response histories. Dimensional consistency alone does not choose among them.
