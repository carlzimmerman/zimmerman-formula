# What a decelerating supernova result would mean for this framework

Checked 2026-09-08. This is an assumption audit and a reproduced algebraic
consistency condition, not a new supernova fit or a proof against either side.

## Source question

Sah, Rameez and Sarkar, *Pantheon+ supernovae corrected for progenitor age
indicate the universe is decelerating*, MNRAS 549, stag844 (2026),
[published paper](https://doi.org/10.1093/mnras/stag844),
[arXiv:2606.09650](https://arxiv.org/abs/2606.09650), report a positive
deceleration monopole after applying an age-dependent luminosity correction.
Their equation (6) subtracts `0.030 mag/Gyr` times a redshift-dependent
relative-age curve; their equation (5) separately models a decaying directional
contribution to q0. Those modeling choices are substantive, not equivalent
to refitting an isotropic distance curve with the unchanged release magnitudes.

Wiseman et al., *Still accelerating: type Ia supernova cosmology is robust
to host galaxy age evolution*, MNRAS 549, stag797 (2026),
[published paper](https://doi.org/10.1093/mnras/stag797), examine the age-bias
premises used by Son et al. They argue that standard host-mass and selection
corrections remove the significant residual age trend, and distinguish host
stellar age from supernova progenitor age. This is a relevant counteranalysis,
not a numerical reproduction of every Sah et al. directional fit.

Source scope: primary published methods/results were checked, not the complete
author likelihoods or their data-processing pipelines. No consensus vote or
paper title is used as a proof. The accompanying [full-covariance baseline](REPORT.md)
uses the published corrected Pantheon+ data. It **does not test or refute**
Sarkar's alternative age, frame or directional analysis. A fair comparison
requires both correction models and their nuisance uncertainties, avoiding
double-counted environmental corrections and verifying sky-coordinate frames.

## A direct consistency consequence, derived rather than assigned

The earlier supernova bridge assumes flat GR, pressureless matter, negligible
radiation at the epoch, and the proposed density relation. In those assumptions,

    H² = (8 pi G/3)(rho_m+rho_DE),
    addot/a = -(4 pi G/3)[rho_m+(1+3w_DE)rho_DE],
    a0² = c² G rho_DE/4.

Eliminate both densities before specializing the dark-energy equation of state:

    q0 = 1/2 + 16 pi w_DE [a0/(c H0)]².

For constant Lambda (`w_DE=-1`), this becomes

    q0 = 1/2 - 16 pi [a0/(c H0)]²,
    q0 >= 0  requires  a0 <= c H0/sqrt(32 pi).

At the illustrative input `a0=9.4e-11 m/s²`, the derived q0 is -0.535775
for H0=67.4 km/s/Mpc and -0.382957 for H0=73.0 km/s/Mpc. The corresponding
largest a0 values permitting deceleration are 6.53101e-11 and 7.07364e-11
m/s². These are conditional calculations, not new measurements of q0 or H0.

Thus a confirmed decelerating q0 would also challenge this **combination** of
the proposed scale relation, those numerical inputs and the inherited flat-GR
constant-Lambda background. It would not by itself prove the MOND framework
right. Conversely, a different action-derived expansion law or DE pressure
changes the condition; the current IC constructions have not supplied a
realistic background, so this is not a no-go for every IC completion.

## Reproduction

    python3 -B qwen_claude_field_theory/closure_2026/supernova_reaudit_2026/q0_consistency.py
    python3 -B -m unittest discover -s qwen_claude_field_theory/closure_2026/supernova_reaudit_2026 -p 'test_q0_consistency.py' -v

The three tests were first run with the implementation absent (exit 1), then
passed after implementation (exit 0). SymPy eliminates the densities and
solves the zero-deceleration boundary. The general-w check prevents assuming
the constant-Lambda result for other fluids. No PPN parameter or theory-closure
flag is supplied by this calculation.
