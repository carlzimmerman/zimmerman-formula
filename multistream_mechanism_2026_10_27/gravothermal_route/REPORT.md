# Multistream gravothermal route: energy moves, but gravity alone does not select the core

Date: 2026-10-27. Base requested: `e6d278b74755885d9f62106becef5d7b753c512c`.
Independent subagent calculation, with live repository changes hashed by the two run manifests.
All writes are confined to this directory. No galaxy or cosmological fit was run.

**Result.** Multistreaming provides an activation condition and a reservoir of orbital energy. It does not by itself provide a dissipative operator, the right feedback sign, or the required surface-density scale. The claim that ordinary collisionless mixing or Fourier-like core/envelope heat transfer must settle at the prescribed core density is refuted under the assumptions below. A distinct pressure-bearing phase can evade this obstruction. The root agent's proposed logarithmic-pressure core has a numerically verified stable radial branch under a moving, fixed-external-pressure boundary. Its microscopic origin, phase boundary, and vacuum coefficient remain missing.

## 1. Exact transfer identity and a multistream counterexample

For collisionless transport in a potential,

\[
\partial_t f+v\cdot\nabla_x f-\nabla\Phi\cdot\nabla_v f=0,
\qquad {d\over dt}\left({v^2\over2}+\Phi\right)=\partial_t\Phi.
\]

Time-dependent gravitational potentials can redistribute orbital energy between streams. Once the potential is stationary, every orbit conserves its energy. The velocity covariance can remain nonzero while this transfer vanishes. For example, a spatially homogeneous pair of counterstreams in a periodic background-subtracted problem has nonzero dispersion and zero energy transfer forever. A stationary self-consistent distribution `f=F(E,L)` is the bound analogue: being multistream does not imply heating.

Fine-grained phase-space volume and the Vlasov Casimirs are conserved; mixing can change coarse-grained moments without supplying a unique final temperature or density. A coarse-graining prescription is not a collision operator or an energy receiver.

**Scope:** these statements concern Hamiltonian collisionless transport. They do not exclude an explicitly specified interaction or radiative channel. The older finite kinetic-current calculation actually supplies such an interaction response, but explicitly has no spatial gradients or streaming and does not derive a halo conductivity: `sol61_push/cold_production_2026_10_11/KINETIC_HEAT_CURRENT.md:106–117`. Conservative tagged transport likewise fixes bookkeeping, not core selection: `sol61_push/cold_conservative_phase_2026_10_24/TRANSPORT_DERIVATION.md:15–23`.

Literature context, not an imported numerical premise: [Lynden-Bell (1967), collisionless violent relaxation](https://academic.oup.com/mnras/article/136/1/101/2602554) and [Balberg, Shapiro & Inagaki (2002), gravothermal evolution](https://arxiv.org/abs/astro-ph/0110561). The algebra below is derived independently.

## 2. Why ordinary heat exchange can have the wrong feedback sign

Assume a self-gravitating, approximately homologous core of fixed mass, negligible surface work during this reduced diagnostic, and virial equilibrium. For a uniform sphere, with `theta=sigma_1D^2`,

\[
\theta={GM_c\over5R_c},\quad E_c=-{3\over2}M_c\theta,
\quad \Sigma_c={3M_c\over4\pi R_c^2}\propto\theta^2.
\]

Its effective heat capacity in these units is negative, `C_c=-A`, `A>0`. Give the envelope a positive effective capacity `C_e=B` and a heat conductance `K>0`. With outward luminosity `L=K(theta_c-theta_e)`,

\[
C_c\dot\theta_c=-L,\quad C_e\dot\theta_e=L,
\qquad\dot\delta=-K\left({1\over C_c}+{1\over C_e}\right)\delta,
\quad\delta=\theta_c-\theta_e.
\]

This closure exactly conserves `C_c theta_c+C_e theta_e`.

- `B>A`: unstable temperature equality. A hotter core loses energy, contracts and becomes hotter. A colder core absorbs energy, expands and becomes colder. The fixed-temperature-bath limit is unstable too.
- `0<B<A`: stable temperature equality, but its temperature is `E_total/(B-A)`, so it remembers the initial energy. The rate K changes the settling time, not the equilibrium density.
- If both capacities are negative, their temperature difference is unstable in this same closure.

The bounded ODE uses `C_c=-1`, `B=2` or `0.5`, and K=1. For B=2, a 1% initial temperature contrast grows by `exp(2.5)=12.18` over five time units. The initially hot core contracts to 0.819 of its initial radius; the initially cold core expands to 1.292. For B=0.5, two stable initial conditions converge toward temperatures 1.02 and 1.22 and hence normalized surface densities 1.0404 and 1.4884. They use identical constitutive parameters. Maximum energy error is `1.12e-15`; maximum analytic-trajectory error is `1.58e-11`.

**This is a bounded counterexample, not a universal claim that all spatial halo conduction is unstable.** Pressure work, changing enclosed mass, anisotropic stress, and baryon-dominated positive-capacity regions can change the response. They must be supplied explicitly.

A more general sign requirement follows without Fourier's law. Write `E_c=-D/R_c`, D>0, and let `P_net` be the net heating power. Then

\[
\dot\Sigma_c=-{2\Sigma_cR_c\over D}P_{\rm net}(\Sigma_c).
\]

A stationary surface density is locally stable only if `P_net'(Sigma_*)>0`: denser cores must receive more net heat. A fixed-temperature Fourier bath gives the opposite derivative because `theta_c` increases with `Sigma_c`. Merely setting a transfer timescale equal to a Hubble time does not establish a fixed point or its stability.

## 3. An exact scale obstruction even when Lambda is retained

Consider Newtonian Vlasov–Poisson with fixed vacuum density,

\[
\nabla^2\Phi=4\pi G\rho-8\pi G\rho_\Lambda.
\]

If `(f,Phi)` solves the equations, then for any lambda>0

\[
f_\lambda(x,v,t)=\lambda^{-3}f(x/\lambda,v/\lambda,t),
\qquad\Phi_\lambda(x,t)=\lambda^2\Phi(x/\lambda,t)
\]

does also. Density is unchanged at corresponding locations; radius and velocity scale by lambda, mass by lambda cubed, and surface density by lambda. Time, G and rho_Lambda are unchanged. Consequently a universal surface density cannot be selected by these equations plus scale-invariant activation/closure rules. This remains true after shell crossing. Specified initial-spectrum scales, boundary lengths, relativistic propagation or a new constitutive scale can break the symmetry; they are additional physical inputs, not exceptions silently contained in this result.

The Lambda force is conservative for constant Lambda and supplies no heat. For a uniform core its force relative to self-gravity is `2 rho_Lambda/rho_core`. At the target surface density this is only `1.62e-6` at 1 kpc and `4.85e-4` at 300 kpc on the canonical footing; the corresponding alternative values are `1.95e-6` and `5.86e-4`. These are illustrative uniform-core ratios, not fits to actual halos.

The desired acceleration contains a separate relativistic speed, `a0=kappa c sqrt(G rho_Lambda)`. The Newtonian Lambda force contains only the curvature frequency `H_Lambda^2=8 pi G rho_Lambda/3`. This is the missing scale-bearing coupling; putting a0 into a transfer switch would assume the desired result.

## 4. A viable structural direction: vacuum pressure, not gravitational Lambda heating

Hydrostatic pressure has the form `P_grav ~ G Sigma^2`. A physical vacuum phase pressure difference `B=epsilon rho_Lambda c^2` would therefore supply the right dimensional surface-density scale `sqrt(B/G)`. This differs from Lambda's tidal gravity: it requires a constitutive interaction or phase boundary that can transmit stress.

For the King-core convention used in the record,

\[
\rho_0r_0^2={9\sigma^2\over4\pi G},\quad
P_0={4\pi G\over9}\Sigma_0^2.
\]

Requiring `Sigma_0=a0/(2 pi G)` would need

\[
P_0={\kappa^2\over9\pi}\rho_\Lambda c^2
 =0.00884194\,\rho_\Lambda c^2\quad(\kappa=1/2).
\]

**This coefficient is a required value, not a derivation.** A uniform constant vacuum does not provide a positive mechanical wall automatically. A pressure plateau does not itself select a stable gravitational equilibrium either. The next viable ingredient is an actual pressure-bearing phase with a stable radial branch and an energy-conserving outlet for transient excess energy. A model must derive the pressure response, not prescribe the target density and call it relaxation.

## 5. Independent review of the root's logarithmic-pressure candidate

Root supplied `P=P_ref+A ln(rho/rho_ref)`, A>0. Here A is a pressure coefficient, unrelated to the heat-capacity magnitude above. Assume the perturbation response is strictly barotropic, `Delta P=(A/rho) Delta rho`, and the boundary is a material surface that moves while its external pressure remains fixed. No rigid box is imposed.

Let `rho=rho_c/theta`, `r=a xi`, with `a^2=A/(4 pi G rho_c^2)`. Hydrostatic equilibrium becomes

\[
\theta''+{2\over\xi}\theta'={1\over\theta}.
\]

For radial displacement `delta r=r eta exp(i omega t)`, linearized mass conservation gives `Delta rho/rho=-(3eta+r eta')`. The radial pulsation equation is

\[
{d\over dr}(\Gamma_1Pr^4\eta')
 +r^3{d\over dr}[(3\Gamma_1-4)P]\eta
 +\rho r^4\omega^2\eta=0.
\]

Since `Gamma_1 P=A`, this gives exactly

\[
\eta''+{4\over\xi}\eta'
 +\left({4\theta'\over\xi\theta}+{\lambda\over\theta}\right)\eta=0,
\quad\lambda={\rho_ca^2\omega^2\over A}.
\]

The boundary condition is `Delta P=-A(3eta+xi eta')=0`, not `eta=0`. The self-adjoint quadratic form contains the positive boundary term `+3 xi_b^3 eta_b^2`. This is the appropriate movable-pressure ensemble.

I independently integrated equilibrium in variables `(theta,m)` and discretized the variational eigenproblem with linear finite elements, without shooting in lambda. At density contrast four, the lowest nodeless eigenvalues are:

| Elements | lambda_0 |
|---:|---:|
| 200 | 0.090401549 |
| 400 | 0.090397405 |
| 800 | 0.090396369 |

Root's shooting value is `0.090396023`. The independent fixed-pressure mass curve is proportional to `m/theta_b^2`. Its derivative vanishes when `theta'=1/sqrt(2)`, at contrast `5.133954659824`. The fundamental eigenvalue there tends to zero with refinement (`4.34e-7` at 800 elements). At contrast six it is negative, `-0.034536874`.

**Outcome: conditional radial stability supported by two numerical methods.** It is not a complete formation mechanism. In particular:

1. An actual halo envelope must implement the assumed boundary pressure response. This calculation cannot establish the stability of an open or dynamically coupled full halo.
2. Ending the active phase at contrast four is an imposed phase/boundary hypothesis; the stability result does not select that contrast.
3. Nonradial perturbations, anisotropic kinetic stress, baryons and mass exchange are outside the calculation.
4. A positive-energy stable normal mode may radiate its perturbation energy without contradicting the gravothermal counterexample. Such damping establishes settling near an existing equilibrium, not creation of its EOS or removal of arbitrary collapse energy.
5. The logotropic relation fixes a core surface-density scale when A is fixed; it does not alone choose a unique central density. Root's required `A/(rho_Lambda c^2)=0.00232946` remains inferred from the target, and its value differs from the King relation because the structural definitions differ.

## 6. How the new evidence changes the task

- **X55 supersedes the earlier X53 calibration loophole.** It refits the Burkert family itself on SPARC and still finds a roughly 0.4-dex lensing mass mismatch. This route therefore needs altered structure/phase or selection physics, not just reuse of another mass fit. See `X55_one_halo_mass_for_both/README.md:10–31` and `:104–110`.
- **IJ1's amplitude variant has landed.** It requires 30–80 times the original self-coupling, has 34–54% unconverged SPARC lanes, and still fails most target classes. It cannot justify scaling up a conductivity until the desired radius appears. See `IJ1_isothermal_jeans_halos/README.md:80–102`.
- **X56** forbids retaining an unconditional fundamental-law floor around every cluster: its outer signal is already too high. A core mechanism must not add a universal infinite halo tail by construction.
- **X57** leaves a phase-space activation route open but expressly has no derived action. Nonzero multistream stress can activate a new channel; it is insufficient to specify that channel or its endpoint.
- **X54** constrains its stated homogeneous exchange laws. It does not directly constrain every halo-local heat transfer; their cosmological volume-averaged exchange must be calculated rather than identified with the same xi by fiat.
- **Older transport blockers** remain applicable: local theta/3 heating vanishes after virialization; constant-vacuum heating needs a dynamical receiver; finite current damping is not yet spatial conductivity. The proposed new phase and outlet must explicitly supply those missing pieces.

## 7. Evidence and reproduction

`run/manifest.json`: bounded reservoir/scale diagnostic, status `completed`, verified with the installed computation-audit validator. `eos_review_run/manifest.json`: bounded independent pressure-boundary check, status `completed`, also validated. Both contain observed before/after source hashes, software versions, argv and actual repository revision. Contract files were written before their runs. Neither run changed a declared input.

The mathematical similarity and feedback derivations are analytic; their numeric examples are not substitutes for those arguments. Numerical radial stability is finite-resolution evidence, not interval certification.

To reproduce, run the recorded argv in the manifests into a new output directory through the bounded runner (the scripts' result path must be changed consistently). The main diagnostic currently writes to `run/result.json`; preserve that file or use a copied lane before re-executing. Do not overwrite evidence while another run is active.

**Cheapest next discriminant:** couple the active core to a dynamical finite envelope and derive its pressure impedance and energy flux from the proposed stress channel. A relaxation demonstration must keep the mass/energy ledger, perturb both sides of the candidate equilibrium, and show convergence without fixing rho_c or inserting Sigma_target into its evolution. Deriving A from the vacuum receiver is a separate indispensable obligation. The gravity-only branch supplies no such A.
