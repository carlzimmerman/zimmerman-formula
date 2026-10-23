# Quantum-correlation continuation: executed work and current limit

**The requested calculation is not complete.** No thermalization time, surviving cold abundance, or bound-core initial condition was obtained. In particular, the new absorption/inverse reaction has not yet been integrated into a nonlinear quantum time-evolution solver. The earlier conditional abundance is not upgraded by this work.

Checkpoint ancestry: repository HEAD `142d9d8ccd50aceb78e9bd4fa20c120116029738`, with local uncommitted research evidence. Exact input contents are pinned by the four run manifests below. Work continues from `BATH_FORMATION_REACTION_RESULT.md`, not from a new assumed bath.

## Target and route decisions

Target: evolve the existing high-H source from its quantum initial conditions under the original complex action, retain the correlations responsible for production and conversion, include absorption and inverse processes without double counting, establish approximate thermalization dynamically if it happens, and compute the later cold distribution and yield. An early-time covariance, a thermal-rate table, or a fitted energy temperature is partial progress only.

Three routes were assessed:

1. A Gaussian/Hartree closure is inexpensive and retains squeezing, but does not provide the scattering and higher connected correlations needed for the requested chemistry. It cannot be used as the complete answer.
2. A kinetic particle solver initialized at a chosen late time repeats the unresolved matching assumption. It was not used to generate another abundance.
3. A renormalized closed-time-path correlation evolution can retain both coherence and nonlocal scattering, but requires a new nonlinear solver and consistent initial-state specification. The executed work below constructs and tests prerequisites for this route; it does not claim that solver exists yet.

## 1. Quantum initial-state audit and nonzero-mode completion

The previous classical lattice initializes 364 nonzero spatial modes per real field with Hankel covariances. The other represented modes have zero stochastic field and momentum variance. That is a valid stated classical truncation, but it cannot be read as a quantum covariance for all the active lattice modes: a quantum vacuum has nonzero uncertainty.

In the source's conformal variables, the canonical commutator per orthonormal real mode has effective hbar=lambda=0.00881292. For mode covariance F=<q²>, P=<v²>, C=<{q,v}>/2,

\[
FP-C^2\ge\lambda^2/4=1.94168897316\times10^{-5}.
\]

The retained Hankel modes saturate this relation. Assigning F=P=C=0 to an additional quantum mode violates it. This is a statement about the initial covariance prescription, not an attempt to estimate a quantum ensemble from one saved classical realization.

`quantum_initial_state_audit.py` reconstructs the retained covariances exactly and extends the **same constant-background Hankel ansatz** to all nonzero finite-box modes. It stores compact shell-degenerate covariance and stable Cholesky data in three NPZ files for grids 32,64,96, all at box size L=32. Wronskian error is below 4.5e-13; uncertainty saturation and the original retained variances pass.

This supplies candidate nonzero-mode input, not a complete interacting initial quantum state. The quantum zero mode/coarse patch density matrix, missing larger-volume infrared information and renormalized interacting initial correlations remain unresolved. No new nonminimal curvature coupling or vacuum renormalization prescription was silently chosen.

At 96 cubed, 884371 of 884735 nonzero spatial modes were outside the original band. **Mode-count fraction is not an energy or particle-abundance fraction.** Completing them with unsubtracted Hankel covariances changes the bare longitudinal Hartree curvature by 0.073781 in the conformal units, versus 0.014339 at grid 32. The strong cutoff dependence demonstrates why merely adding random vacuum noise to the classical nonlinear code would not yield a controlled quantum prediction.

## 2. Actual pre-backreaction correlation evolution

`linear_quantum_correlations.py` propagates complex mode functions U and V=U' from those Hankel covariances, including their phase correlation. The mean and velocity come directly from the saved high-H initial Cauchy state. In the early leading conformal quartic sector,

\[
q''+q^3=0,\qquad
U_L''+(k^2+3q^2)U_L=0,\qquad
U_T''+(k^2+q^2)U_T=0.
\]

The original cubic coupling to the frozen X background is negligible **over this computed interval**: its classical curvature contribution relative to the quartic oscillation scale is bounded by 1.44e-13 at the endpoint. This does not justify neglecting X or its reactions at late times. This early evolution is conditional on the same prescribed inflationary source and representative patch as the earlier calculation; that source was not selected by the flat-space action alone.

The solver retains F=|U|², P=|V|² and C=Re(U*V). Instantaneous particle occupancy and anomalous correlation can be reconstructed as

\[
n+\tfrac12=\frac{P+\omega^2F}{2\lambda\omega},\qquad
\kappa=\frac{\omega^2F-P}{2\lambda\omega}+i\frac C\lambda.
\]

The nonzero kappa is not discarded to manufacture a bath. The Wronskian and pure Gaussian mode-pair covariance remain preserved. Global purity alone would not exclude local thermal behavior in an interacting system; no such broad claim is made here.

A finite-cutoff, zeroth-adiabatic-order-subtracted tadpole diagnostic measures when the prescribed-background linear expansion ceases to be small:

\[
C_s^{\rm sub}=L^{-3}\sum_k d_k\left(|U_s|^2-\frac{\lambda}{2\omega_s}\right),
\qquad B=\frac{|3C_L^{\rm sub}+C_T^{\rm sub}|}{q_{\rm amplitude}^2}.
\]

This is not full renormalization. The run stops at the first sampled B>=0.1, a declared approximation-control threshold, **not a physical bath-formation criterion**.

All four runs (32 cubed at dt=.01 and .005; 48 cubed at .01; 64 cubed at .005) cross at sampled conformal time z=3.0, corresponding to a=8.50605 and H/M=9.28954e10. B ranges 0.10068–0.10112; output time spacing is 0.2, so the exact crossing time is not resolved more precisely. Modes outside the old retained band contribute about 10.7–11.1% of this signed diagnostic at that point. This is not a statement about cold material or an integrated scattering fraction.

The timestep check gives background energy error below 5.1e-6 at dt=.005 and Wronskian error below 4.6e-13. The calculation establishes that extrapolating a linear quantum source to late conversion is not controlled. It does **not** evolve through the nonlinear bath-formation stage.

## 3. Interaction orders required for the new reaction

`quantum_diagram_inventory.py` enumerates exact Wick contractions of selected unshifted complex-action vertex sets, records connected graphs and tests two-particle irreducibility by edge removal. It checks contraction totals and elementary double-bubble, cubic-sunset and quartic-basketball combinatorial weights. These are positive combinatorial weights only; contour signs and self-energy derivatives have not been supplied.

Squaring the full absorption amplitude gives orders g²lambda², g⁴lambda, g⁶. For the corresponding connected vacuum diagrams, closing the external X self-energy legs gives four loops. The leading contact Phi 4-to-2 loss at order lambda⁴ corresponds to five-loop vacuum diagrams. The inventory explicitly finds irreducible graphs at these orders.

This is **not** permission to add every squared tree as a separate term to an already dressed correlation solver. Some perturbative diagrams are generated by iterating lower self-energies. For example, the selected g⁴ unshifted, normal-propagator vacuum set has no new two-particle-irreducible skeleton although it has connected diagrams. Dressing and cuts must be reconciled before combining terms. Coherent backgrounds introduce shifted vertices and anomalous propagators outside this inventory.

Thus neither a Gaussian closure nor a low-order scattering model with an independently appended absorption rate has yet been shown to realize the requested conserving quantum dynamics. Both contour directions must be retained to obtain the reaction and its inverse; the previously computed Bose gain–loss factor provides a dilute-limit check, not the missing nonlocal solver.

## Correlation equations to be implemented

With canonical conformal real fields, define the statistical matrix F and spectral matrix rho=i<[chi,chi]>. A closed-time-path calculation has the schematic causal structure

\[
[\partial_\eta^2+k^2+\mathcal M^2(\eta)]F(\eta,\eta';k)
=-\int_{\eta_0}^{\eta}ds\,\Sigma_\rho(\eta,s;k)F(s,\eta';k)
+\int_{\eta_0}^{\eta'}ds\,\Sigma_F(\eta,s;k)\rho(s,\eta';k),
\]

\[
[\partial_\eta^2+k^2+\mathcal M^2(\eta)]\rho(\eta,\eta';k)
=-\int_{\eta'}^{\eta}ds\,\Sigma_\rho(\eta,s;k)\rho(s,\eta';k).
\]

Field indices are contracted; a non-Gaussian initial state requires additional initial-correlation terms. Consistent mean-field equations, renormalized local terms and nonlocal self-energies are jointly necessary. Their specific nonlinear implementation for this model remains open. The general framework is reviewed by [Berges, Introduction to Nonequilibrium Quantum Field Theory](https://arxiv.org/abs/hep-ph/0409233); it is not a ready-made solution or a controlled-error guarantee for this model.

## Evidence and status

All four bounded runs completed with their stated checks passing:

- `quantum_initial_state_audit_run/manifest.json` and `results.json`; nonzero-mode covariance NPZ files.
- `linear_quantum_correlations_run/manifest.json` and `results.json`; four time histories and final complex mode functions.
- `quantum_diagram_inventory_run/manifest.json` and `results.json`; exact graph inventory.
- `audit_linear_quantum_correlations_run/manifest.json` and `results.json`; an independent adaptive DOP853 integration of 31 shells in both polarizations. The fine-step mode error is 2.35e-5, and halving the symplectic timestep reduces both mode and mean-field errors by a factor of approximately four.

These files record command lines and input hashes. The old action, source evidence and thermal runs were not modified.

**Open route:** implement and validate the nonlinear renormalized correlation evolution, including the source's initial correlations and all required cuts without double counting. Thermalization must then be tested from the evolved distributions/correlations, followed by late cooling and loss evolution. A numerical surviving abundance at present would still require an unsupported closure or matching assumption. No such number is reported.
