# Frequency is stable; intrinsic linewidth is unresolved

The low-mode frequency remains near .8228 under narrower broadening and a128x128 action grid, but the small excess half-width does not converge. At epsilon=.0001 it changes by a factor about2.10 from64x64 to128x128, and by about16 across32x32 to128x128. No physical damping rate or lifetime is established.

## Experiment

Retain the eight-shape A10000 kinetic response and sixteen orbital harmonics. Add a128x128 Gauss action grid (16384 orbit integrations). Its mass is .9999988711, matrix high-frequency sum-rule error1.8747e-5 relatively, and maximum Fourier integration difference4.51e-7. All four direct construction checks pass. This confirms global moments and orbit integrations; it does not guarantee resolution of narrow resonance surfaces.

For each action-grid order32,64,128 and epsilon=.003,.001,.0003,.0001, maximize the absorptive response within .818–.828 and find both half-height crossings within .79–.85. No Lorentzian damping fit is imposed. Report half-width at half maximum (HWHM), subtracting epsilon only as a numerical diagnostic. A non-Lorentzian background or asymmetry can make that subtraction physically misleading.

## Measured excess half-width HWHM-epsilon

| epsilon | 32x32 | 64x64 | 128x128 |
|---|---:|---:|---:|
| .003 | 7.193e-5 | 6.505e-5 | 6.881e-5 |
| .001 | 7.126e-5 | 5.574e-5 | 7.208e-5 |
| .0003 | 4.531e-5 | 6.156e-5 | 7.631e-5 |
| .0001 | 5.888e-6 | 4.504e-5 | 9.457e-5 |

At epsilon=.003 the two finest grids agree in this diagnostic to about5.8%, but the excess is only about2.3% of the imposed width. Agreement at that broad setting does not establish a zero-width limit. At narrower epsilon the grid dependence increases. At epsilon=.0001 the128-grid peak is noticeably asymmetric: the difference between right and left half-widths is9.47e-5, comparable to the reported excess. Interpreting it as a single damping pole would be unjustified.

The128-grid peak frequencies are .82279797,.82279760,.82280190,.82275919 as epsilon decreases. Their variation is small relative to the collective frequency, while the tiny width remains sensitive. This separates the robust candidate frequency evidence from the unresolved decay question.

## Interpretation

This is an unresolved resonance-integration problem, not evidence for zero damping and not a measurement of nonzero damping. Finite action grids replace a continuum of orbital resonances with discrete frequencies. Narrowing epsilon eventually resolves that discreteness, and subtracting epsilon can amplify quadrature error. A passing mass/sum-rule test cannot certify a narrow linewidth.

The next useful calculation is integration along the resonant curves n Omega_r(E,L)=omega, with an appropriate principal-value calculation for the real response. That targets the continuum imaginary part without treating arbitrary Lorentzian broadening as physical friction. Multiple roots, tangent resonances and endpoint contributions need explicit handling. Further basis and harmonic checks remain necessary even after quadrature improves.

The cold collective response therefore remains a plausible long-lived kinetic mode, but no lifetime, cooling efficiency, cosmological formation route or cold-occupation selector follows. The full parent and novelty obligations remain open.

## Evidence

The direct128-grid orbit construction is preserved in action_128.json/.npz. linewidth_run performs the bounded peak/crossing calculation using all three pinned action grids, passes its two numerical-operation checks and has a valid completed manifest. Those checks confirm optimizer success and positive measured widths; they do NOT certify convergence, which the table above fails to demonstrate. Interpretation is self-reviewed.
