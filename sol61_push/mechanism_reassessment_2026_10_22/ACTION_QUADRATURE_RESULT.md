# Action quadrature sharpens the candidate collective mode

Replacing phase-point samples with orbital-action quadrature places the low kinetic response peak at omega=.823 throughout the tested configurations. It is within about .6% of the independent exactly cold-fluid fundamental .827760. The matrix high-frequency sum-rule error falls from about2.05% in the4096 phase-sample calculation to .00188% in4096 action-quadrature orbits. This strengthens the mode-frequency evidence; it does not establish a damping rate or halo formation.

## Measure and occupation weighting

For a spherical radial observable in the convention mass=integral r²rho dr, integrate orientations and both signs of radial velocity. The phase-space measure becomes

    dGamma=2pi L T_r dL dE=pi T_r d(L²) dE.

The equilibrium f=FQ with Q=-E-L²/2 has

    rho=A Psi^(5/2)/(1+r²),
    F=15 A/(2^(9/2) pi).

Thus the derivative-response quadrature weight is F pi T_r d(L²)dE, and the mass weight is that quantity times Q. This removes the large1/Q importance weights incurred when drawing samples from f itself. It does not change the equilibrium or add collisions.

The occupied region has E between the circular-orbit energy at fixed L and the cutoff -L²/2. Its maximum L² follows from Q=0 on a circular orbit. Numerically Lmax²=.03609691 and the corresponding circular radius is1.40591806. The circular L² curve was checked to increase on the dense background grid. This is numerical evidence for the integration domain, not a general theorem for arbitrary backgrounds.

Use Gauss nodes in L² and energy, at32x32 and64x64 orders, with the same eight finite-A trial potentials, sixteen Fourier harmonics, and1024/2048-point orbit phase integrations. This is a different integration rule for the same susceptibility, not a newly fitted mechanism.

## Independent accuracy checks

| diagnostic | 32x32 orbits | 64x64 orbits |
|---|---:|---:|
| integrated mass | .999977481 | .999996668 |
| relative matrix sum-rule error | 1.9580e-5 | 1.8789e-5 |
| maximum absolute Fourier refinement error | 4.25e-7 | 4.47e-7 |

Each direct construction passes four stated checks. The mass and high-frequency moment provide independent normalization tests of the action measure and derivative weights. The small matrix-norm error is not a uniform bound in every weak response direction, nor does it guarantee accurate integration of arbitrarily narrow resonances. The residual sum-rule error changes little with quadrature order, so other truncation/discretization errors remain.

## Low-mode response

Scan .75–.88 in frequency steps .001. The external observable is the same dilation-potential response as in MULTISHAPE_RESULT.md. Every combination of32/64 quadrature order,4/8 field shapes, and epsilon=.03,.01,.003 peaks at the grid point .823. No sub-grid frequency uncertainty is claimed.

For eight shapes:

| epsilon | peak height,32x32 | peak height,64x64 |
|---|---:|---:|
| .03 | .846087 | .846087 |
| .01 | 2.494031 | 2.494175 |
| .003 | 8.131574 | 8.144277 |

The narrowest tested peak height changes by about .16% between quadrature orders. Four-shape heights differ more, especially at epsilon=.003 (about7.00 versus8.14), even though peak locations agree. Basis convergence of widths and residues is therefore less complete than convergence of the peak's grid location.

The period corresponding to .823 is about7.63, close to the independent cold-fluid period7.59059 and the live cold simulation's7.1–8.3 prominent spacings. This is meaningful cross-checking of a candidate collective mode, but does not validate an exact waveform: finite temperature, finite amplitude and numerical spatial errors differ between these calculations.

## What remains unresolved

The peak grows nearly inversely with numerical epsilon. It has not reached a width independent of regularization. Epsilon is not physical friction, and no fitted lifetime, decay rate, lower bound on lifetime or continuum Landau pole is reported. Narrower resonance resolution requires further quadrature and basis checks; reducing epsilon on a fixed finite grid is not sufficient.

This calculation improves the response representation enough to pursue that question credibly. It does not explain why the cold occupation A10000 is selected, show primordial formation, add an energy-carrying sector, or establish novelty. The full parent and observational scope remain separate open obligations.

## Evidence

Direct action_32/action_64 JSON and NPZ files retain the weights, orbits, basis matrices and Fourier coefficients. action_response_run audits those inputs and performs the bounded low-frequency response scan; it passes three checks and has a valid completed manifest. The original direct orbit construction is not claimed to have run inside that bounded scan. The source reuse chain is pinned. Interpretation is self-reviewed.
