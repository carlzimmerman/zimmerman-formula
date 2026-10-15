# Oblique finite-interface search and its numerical limits

The continuum proofs are in [PROOF.md](PROOF.md). This file records an attempted extension, including adverse results. These finite runs are not continuum certificates.

## Implemented object

Perturb all six metric entries on a periodic z interval, with transverse dependence exp(iqx). Planar rotational symmetry makes x a representative transverse direction. Use the odd-N Fourier differentiation matrix, nodal coefficient quadrature, and complex binary64 arithmetic. The constitutive profiles are h=1 for |z|≤3, smoothly zero by 5; θ=1 up to 7, smoothly zero by 11; κ=κstrength θ; s²=1/2. Set the acceleration coefficient A=0 for this variant. A=0 is deliberate, not an omission of a term present in the tested action.

Lapse entries with h≤1e−12 are retained as multipliers. The positive lapse block is eliminated. The shift Hessian is diagonalized; eigenvalues above the recorded relative threshold (with an absolute floor) are inverted, while the discarded directions impose velocity constraints. Those constraints are integrated with zero constants for the position space. This is the nonzero-frequency perturbation sector, not arbitrary nonzero integration charges. All ranks, null couplings and thresholds are in the raw records. There is no gyroscopic mixing in this stationary flat b=0 calculation.

The matrices come from the full flat action, not the already diagonal homogeneous dispersion relations. A periodic calculation is a different mathematical domain from the decaying R-line planar proof. Coefficient quadrature also has aliasing, and a finite spectral basis does not resolve all local vacuum constraints exactly.

## Controls

[Oblique v5](oblique_run_v5/calculation/results.json) checks two independent benchmarks at N=31,q=0.5:

- Uniform h=θ=1, κ=4: all six generalized squared frequencies match their exact A=0 formulas with max error 1.42×10^−13.
- Globally h=0 with compact θ,κ: the reduced kinetic form matches an independently constructed Fourier TT-projection energy from the R³ cap theorem, max entry error 1.04×10^−13. No negative eigenvalue below −10^−8 occurs in that finite control.

The second comparison is an orthogonal implementation of the energy identity, not just a sign check. Both benchmarks pass. They do not validate every singular finite-profile reduction.

## The weak staged candidate is not certified

At κstrength=4, [oblique v2](oblique_run_v2/calculation/results.json) finds sizeable negative kinetic eigenvalues, with nonnegative restoring matrices to rounding tolerance. At N=61,q=0.5, period 32, the minimum is −0.0210594; at q=1 it is −0.0392707. These are adverse evidence against extrapolating the simple staged construction to arbitrary transverse disturbances. They are not a proved continuum counterexample.

[Oblique v6](oblique_run_v6/calculation/results.json) tests images and numerical constraints. At q=0.5, increasing period from 32 to 48 while keeping approximate z spacing fixed changes the minimum from −0.0210594 (N=61) to −0.0131120 (N=91). Multiplying by the period to remove the quadrature normalization gives approximately −0.674 and −0.629. Thus the large negative signal is not removed by this increase of vacuum separation.

At N=61, period 32, varying the shift relative inversion threshold from 10^−8 to 10^−12 leaves a sizeable negative minimum, ranging from −0.02014 to −0.02348, but changes the number of negative directions and the retained constraint rank. That sensitivity prevents a reliable exact mode count or threshold claim. Periodic q=0 results are not counterexamples to the decaying planar theorem: exterior constant/harmonic modes and discrete constraints have different admissibility conditions.

## Stronger derivative elasticity is a candidate, not a proof

With κstrength=40 or 400 the large negative directions disappear in the v5 tested cases, although near-zero eigenvalues remain slightly negative. V6 uses κstrength=64 at q=0.5:

| N | Period | Minimum kinetic eigenvalue | Count below −10^−8 |
|---|---:|---:|---:|
| 61 | 32 | −2.00×10^−9 | 0 |
| 91 | 48 | −3.78×10^−9 | 0 |

These are finite results in a problem with gauge/constraint null directions and very small positive eigenvalues. A fixed absolute tolerance cannot distinguish an exact zero from a small genuine negative eigenvalue. They justify examining a stronger-κ construction; they do not certify positivity, causality, all transverse momenta, or a spherical wall. Increasing κ also changes the model and its resource/coupling estimates.

## Exact next discriminator

For fixed h,θ, multiplier constraints and spatial window w=θ, the reduced kinetic form is affine in the elasticity amplitude K:

\[
T_K(u)=T_0(u)+{M^2K\over8}\int w|u|^2.
\]

The shift minimization is independent of K in this flat model. A continuum sufficient threshold would follow from a finite bound

\[
\mathcal C_* =\sup_{\text{admissible }u,\ \int w|u|^2>0}
{[-8T_0(u)/M^2]_+\over\int w|u|^2}<\infty,
\]

together with nonnegativity on zero-denominator directions. Then K≥C* gives nonnegative kinetic energy. The finite matrices suggest testing that weighted constraint estimate; they do not prove that the supremum is finite. Static positivity must also be controlled. This is a precise mathematical obligation for the stronger candidate, rather than an instruction to accumulate more passing grids.

## Preserved failures

- Oblique v1 correctly stopped when a discarded shift direction still coupled to physical velocity. V2 retained those directions as multipliers instead of silently inverting or dropping them.
- Oblique v3 stopped in SciPy's empty-constraint nullspace call for the uniform benchmark. V4 explicitly uses the full identity basis when no constraint rows exist.
- V2, v4, v5 and v6 completed. Their successful execution does not mean their tested staged constructions have positive energy; the negative eigenvalues remain part of the evidence.
