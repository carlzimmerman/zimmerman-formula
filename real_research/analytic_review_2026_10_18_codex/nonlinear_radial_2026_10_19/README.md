# Nonlinear radial stability and the limits of confinement

19 October 2026. Checkpoint ZAR-2026-10-19-05, continuing [the exact smooth halo](../smooth_exact_2026_10_18/README.md). The base equilibrium, density law, population fraction, radial temperature family and finite hollow profile are unchanged.

**The smooth halo is nonlinearly stable against sufficiently small radial perturbations with angular momentum bounded away from zero and a fixed height bound. The entire spatial support cannot be uniformly confined for all time in this open perturbation class.** An explicit arbitrarily small smooth canonical perturbation preserves the initial density and centered dispersion but sends a tiny positive mass to infinity. Stability controls the bulk, not the outermost particle.

The nonlinear theorem uses

\[
X(f-F)=\sum_i\int(1+v_r^2+L/r^2)|f_i-F_i|d\Gamma.
\]

For every desired tolerance epsilon, a sufficiently small initial X distance gives sup_(t>=0) X(f(t)-F) < epsilon. Initial data are smooth, compact, radial and nonnegative, with L in a fixed positive bounded interval containing the equilibrium supports and a uniform L-infinity height bound. Their Casimirs need not equal those of the equilibrium. The theorem includes radial canonical perturbations and nearby invariant leaves.

The proof first establishes an actual nonlinear energy minimum on a weakly closed class of angular-momentum rearrangements. Its normalized weak tangent lies in the previously controlled accessible space; compact mass fields and the exact cubic remainder transfer the positive quadratic into nonlinear coercivity. A conserved-entropy first-exit argument then handles general nearby radial data. No assumption that evolving canonical maps stay small is used.

| Quantity | What the nonlinear result controls |
|---|---|
| Equilibrium density and force law | Exactly the original law and finite profile |
| Perturbed enclosed-mass and force law | Uniformly close for all time; equality is not dynamically preserved |
| Radial pressure | Integrated raw and centered radial pressure remain uniformly close |
| Pointwise radial dispersion | Positive at each annulus radius and finite time for connected positive-support data, including canonical images; no universal positive lower constant |
| Bulk spatial confinement | Mass beyond the original R is uniformly smaller than the selected tolerance |
| Particle radii and speeds | A positive inner bound and finite velocity bound for all time; compact spatial support at each finite time |
| One outer radius containing every particle for all time | False for the open small-distribution perturbation class; a positive-mass escape counterexample is given |

The escape perturbations can approach the equilibrium in X, energy and every fixed Ck norm, while retaining exact initial density, centered dispersion, total masses and fixed-L Casimirs. They do not retain a uniform negative individual particle-energy gap. Uniform outer confinement for a narrower class that retains such an initial gap is not established here; an initial gap is not itself a conserved quantity.

[NONLINEAR_COERCIVITY.md](NONLINEAR_COERCIVITY.md) proves the nonlinear local minimum. [NONLINEAR_FLOW.md](NONLINEAR_FLOW.md) proves global classical evolution and the stability theorem. [LAW_DISPERSION_BOUNDARY.md](LAW_DISPERSION_BOUNDARY.md) gives the observable estimates and counterexamples. [AUDIT_AND_HANDOFF.md](AUDIT_AND_HANDOFF.md) and [CHECKPOINT.json](CHECKPOINT.json) record the checked proof dependencies and exact revisions.

The scope is the existing spherical deep-cubic model with its positive point baryon mass, chosen parameters and positive angular-momentum gap. This is not a nonspherical or covariant completion, temperature-selection mechanism, observation fit or claim of global mathematical novelty. Only this new checkpoint directory was written. No scientific scripts, simulations, numerical calculations or process operations were performed; Claude's calculations and all prior research artifacts were left untouched.
