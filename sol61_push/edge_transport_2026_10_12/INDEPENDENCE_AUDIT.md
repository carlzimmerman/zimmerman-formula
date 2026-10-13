# Assumption audit: independence from ΛCDM is not independence from modelling

12 October 2026. Audit checkpoint `c29c554931ebca0e8c02874aa06bd3cd03846a34`. Requested by the owner after the edge-transport calculation. This is adversarial self-review, not an independent external review. The previous [report](REPORT.md), numerical inputs and recorded outcomes remain preserved.

**Primary verdict: conditional on a named input.** The sharp-edge profiles and Brownian escape formula are conditional on the imposed drift A=d/2, diffusion D=d(q+q0), constant radial period, and specified boundary treatment. They are not derived dynamics of a detected cold component. The inspected calculation does not use ΛCDM background expansion, Planck parameter values, an NFW halo, a cosmological cold/baryon ratio or a ΛCDM-trained mass relation. That independence does not establish its physical applicability.

## 1. Dependency audit

| Step | Mathematical or physical input | Audit status |
|---|---|---|
| Orbital transport | Newtonian Hamiltonian, static spherical mean potential, fixed L | Conditional physical approximation, not a consequence of ΛCDM |
| Noise spectrum | Weak stationary finite-variance forcing independent of initial phase | Conditional; actual baryonic or collective noise not derived |
| Diffusion description | Markov/Ito reduction with separated scales | Conditional; no general memory or separatrix result |
| Drift and variance | A=d/2; D=d(q+q0) | Chosen constitutive model; not fixed by conservation or data |
| Orbit weights to density | Constant radial period at fixed L | Restricted approximation; general period factors not tested |
| Outer boundary | Reflecting benchmark or killed/absorbing population | Chosen boundary models; apocentre crossing is not automatically permanent escape |
| Stationary-current algebra | J=(A-D')n-Dn' | Conditional exact mathematics, with Lean certificates |
| Brownian survival | Square-root transformation and reflection principle | Correct for the chosen drift and ideal killed half-line; not a measured halo lifetime |
| Full cold-energy mechanism | Microscopic forcing, backreaction, supply, metric coupling, abundance and a0 | Incomplete; these leaves are not supplied by the certificates |

The earlier phrase “halo rearrangement, escape, and replenishment must be explained together” should be read as a requirement for the tested open transport construction. It is not a theorem that every possible cold component has that diffusion law, loses particles through that boundary, or needs steady external replenishment.

## 2. Remove the imposed half-drift

Keep the same diffusion for a controlled comparison, but replace the drift by

\[
A=\alpha d,\qquad D=d(q+q_0),\qquad d>0.
\]

Here alpha is a free transport coefficient, not the cosmological kappa. Zero current implies

\[
0=d(\alpha-1)n-d(q+q_0)n',
\qquad
\frac{n'}n=\frac{\alpha-1}{q+q_0}.
\]

For positive n, integrating this first-order equation gives

\[
\boxed{n(q)=C(q+q_0)^{\alpha-1}.}
\]

The inverse-square-root profile occurs at alpha=1/2. Alpha=1 gives a locally constant density; alpha=2 gives a linearly increasing density. These alternatives obey the same local conservative Fokker–Planck form. No conservation condition used in the original calculation selects alpha=1/2. Normalizability, end conditions and backreaction remain additional constraints; these are local counterexamples to uniqueness, not completed physical halo models.

The conservative Fokker–Planck form concerns probability or particle number, with its boundary flux included. It does not by itself conserve the combined energy of baryons, cold matter and a receiver. That requires additional dynamical equations and is still missing here.

With x=sqrt(q+q0), Ito's rule instead gives

\[
\boxed{dx=\frac{d(2\alpha-1)}{4x}\,dt+\sqrt{d/2}\,dW_t.}
\]

For nonzero d and x, the transformed drift vanishes **if and only if alpha=1/2**. Therefore the earlier erf survival formula cannot be transferred unchanged to this family. A physical microscopic calculation of drift is needed before using it to infer a halo lifetime.

This is the decisive audit result: removing an imposed coefficient changes the profile and the escape dynamics without introducing any ΛCDM ingredients. The main uncertainty in this calculation is its own closure, not a hidden cosmological background.

## 3. What survives without that particular coefficient

- The finite-harmonic result that subtracting an orbital-phase-independent scalar changes only the zero harmonic, under the stated weak-noise assumptions.
- The conditional current and probability-conservation bookkeeping.
- For a nondegenerate diffusion at an absorbing boundary, the need to solve a boundary/injection problem; the old drift-specific formula is not a universal solution.
- The earlier Lean proofs as implications of their original premises. They do not validate those premises and are not revoked by changing the model.

`DriftAudit.lean` independently expresses the more general current, its required stationary slope, an explicit alternative, the transformed drift, and the exact condition for its cancellation. These five algebraic theorems do not formalize stochastic calculus or solve the physical selection problem.

Verification: [five theorems compiled](drift_run/main.log) without warnings, admitted proofs or extra axioms; [three damaged proofs were rejected](drift_run/results.json). The [manifest](drift_run/manifest.json) was validated against the current inputs and recorded outputs. This is a second formulation checked by the same author and compiler, not independent human replication.

## 4. Independence requirements for the wider architecture

The broader repository contains model-conditioned inputs that this small calculation does not use. They cannot be silently relabelled as direct observations:

- The numerical cold/baryon ratio 5.364 is an inferred parameter under a cosmological framework, not an assumption-free instrument reading.
- A fitted kappa or galaxy interpolation kernel is an empirical model ingredient, not a microscopic derivation.
- A ΛCDM initial power spectrum, background, halo-mass relation or concentration law remains an inherited input even if the subsequent force solver is new.
- Inferring additional mass from motion or lensing presupposes a gravitational mapping. A gravity-independent observation is not already a dark-mass measurement.

For this programme, the empirical target should be observables such as resolved line-of-sight velocities, angular light/gas distributions, shear and redshifts, with distance, inclination, stellar populations, gas conversion, selection and calibration uncertainties exposed. These are not all assumption-free; the aim is explicit dependencies and sensitivity tests.

The candidate must predict those observables through its own forward equations. A ΛCDM model may be a separately labelled competitor, never the definition of a passing result. A model is not supported merely because a competitor fails. Parameters selected on one sample must be frozen before a genuinely withheld test, with shared systematics and covariance retained.

No new observational test was performed in this audit. No result here proves ΛCDM false or identifies a replacement theory. The concrete next missing input is a microscopic or independently measured drift–diffusion relation, followed by its own boundary and backreaction calculation. Choosing that relation to recover the desired profile would again assume the result.
