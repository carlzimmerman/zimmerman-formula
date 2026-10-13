# Quantum-seeded Gaussian production with the protected action's quartic

2026-10-11. This is a new approximation to [CHARGED_ACTION.md](CHARGED_ACTION.md),
not a reuse of the earlier real-daughter yield. It includes the quartic
interaction required by that action's positive-square potential.

## Normalization and approximation

For the circular charged source chi=A_0 exp(-iMt), rho_source=2M^2 A_0^2
and n_s,0=rho_source/M. Choose g A_0=epsilon m^2 and
lambda=g^2/Delta, Delta=4m^2u_*^2. The chosen density, m=1e-12 eV,
epsilon=1e-7, u_*=0.001 and initial radiation background are the earlier
illustrative benchmark inputs, not an abundance prediction.

Retain positive-charge daughter particles and one homogeneous coherent
source mode. Use the rotating-wave approximation with Gaussian daughter
moments and Wick-factorized quartic expectation values. Omit antiparticle
production, vacuum renormalization, moving source modes, and non-Gaussian
scattering. These omissions remain physical qualifications.

For unordered opposite-momentum pairs retain the earlier w_j, F_j=w_j n_j,
C_j=w_j kappa_j and B normalization. The sum of particle charge fractions
is |B|^2+sum F_j. Pair-state counting is the same as for one identical boson
species: phi's positive-charge particles constitute one such species,
whereas its antiparticles are excluded from this approximation.

Let x=m epsilon t, a^2=1+2h_e x, v_j=m/omega_j,
S=sum v_j F_j, Z=sum v_j C_j. The linear detuning Delta_j is as in the
previous envelope, but G_j=v_j a^(-3/2) for this charged-source normalization.
Define

\[
 k={\lambda n_{s,0}\over m^3\epsilon}
 ={\epsilon M\over2mu_*^2},\qquad K(x)=k a^{-3}.
\]

At the benchmark k is approximately 0.10000005. The required quartic is
therefore not a negligible correction to the production-scale Hamiltonian.

## Conserving Gaussian equations

Normal ordering and Gaussian factorization give
<psi^dagger psi^dagger psi psi>=2n^2+|kappa|^2 for the zero-mean daughter.
After the field normalization phi~psi/sqrt(2omega), its dimensionless
interaction energy per initial source quantum is

\[
 E_4=K(2S^2+|Z|^2).
\]

Both the normal and anomalous terms must be retained. Define

\[
 A_j=G_jB+KZ v_j,\qquad D_j=\Delta_j+4KSv_j.
\]

The moment equations are

\[
 B'=-i\sum G_jC_j,\quad
 C_j'=-iD_jC_j-iA_j(2F_j+w_j),\quad
 F_j'=-2\operatorname{Im}(A_j^*C_j).
\]

Start B=1, C=F=0. The w_j term provides spontaneous pair production.
The direct quartic contribution to sum F_j' vanishes because it is the
imaginary part of K Z* Z. Thus |B|^2+sum F_j=1 remains exact. Each pair's
Gaussian identity F_j(F_j+w_j)-|C_j|^2=0 is also preserved algebraically.

The complete reduced energy is

\[
 E_r=\sum\Delta_j F_j+2\operatorname{Re}(B^*\sum G_jC_j)
       +K(2S^2+|Z|^2).
\]

Its derivative is its explicit background derivative. In addition to the
earlier detuning and coupling work, the code integrates

\[
 K'(2S^2+|Z|^2)+K[4S\sum v_j'F_j+
 2\operatorname{Re}(Z^*\sum v_j'C_j)].
\]

Here K'=-3h_e K/a^2 and v_j'=h_e s_j^2/(a^4 omega_j^3/m^3).
The work variable is integrated independently of the reconstructed energy.
These are internal conservation checks; they cannot validate omitted
quantum correlations or modes.

## Computation scope

[charged_envelope.py](charged_envelope.py) uses 512 and 1024 quadrature
cells on v in [-2,2], and 768 on [-3,3], to x=200. The source density fixes
physical vacuum weights instead of an arbitrary classical daughter seed.
Results and execution status are recorded in `charged_envelope_run`.
The previous real-field source and its output remain untouched.

The exact charge and classical pressure theorems do not automatically apply
to a normal-ordered, truncated Gaussian quantum state. Establishing a
controlled transition between these descriptions is a separate obligation.

## Results and numerical limits

The initial run completed with all 15 checks passing. The endpoint daughter
charge fraction at x=200 is 0.948809491896 on all three quadratures, with
agreement to approximately 1e-13 between these sampled values. At x=100,
all give approximately 0.711432743657. The maximum sampled fraction is
0.999976736 near x=196.8; reverse transfer occurs, so this maximum is not
a final yield. x=200 is about 15.24 days after the chosen starting epoch.

[The tighter run](charged_envelope_tight_run/results.json), with 512 cells
and relative tolerance 1e-10 rather than 1e-8, gives endpoint fraction
0.948809502383. The difference is 1.05e-8. Thus quadrature agreement to many
digits does not imply equivalent total accuracy. About 0.94881 is an
appropriate reported endpoint value for this reduced model.

In the tighter run the maximum charge-combination drift is 1.33e-10 and
explicit-work residual is 4.97e-10. All five checks pass. The pair covariance
relative diagnostic reaches about 1.04e-5; as in earlier runs, this subtracts
nearly equal large-occupation terms and is a diagnostic rather than a
certified quantum-state error bound. No interval-arithmetic certification
or independent implementation is claimed.

The benchmark has A_0=1.1019923137e15 eV, g=9.0744734568e-47 eV and
lambda=2.0586517129e-63. These differ materially from the earlier
one-complex-field parameters. They follow from the chosen density and the
new action, not observations selecting this model.

Original [results](charged_envelope_run/results.json),
[manifest](charged_envelope_run/manifest.json), and
[tighter manifest](charged_envelope_tight_run/manifest.json) retain both
numerical calculations. Manifests validate against their recorded sources.
The derivation was self-reviewed by checking the Wick factors, unordered-pair
counting, particle-charge invariant, and explicit energy-work identity.

**Result:** spontaneous pair production and substantial source depletion
survive the protected action's necessary quartic normal and anomalous
terms in this approximation. A fixed source, classical daughter seed, or
omission of the quartic was not needed for the reported calculation.

This closes one approximation-specific production question. It does not
close moving-source backreaction, non-Gaussian correlations, quantum/classical
matching, source preparation, cosmological abundance or galaxy-law behavior.
In particular, the classical survival theorem plus this Gaussian production
run is not yet a theorem about the complete quantum formation history.

A subsequent [3D spatial pilot](SPATIAL_CONVERSION.md), using an explicitly
classical seed, populates moving sources and shows order-one changes in
transient conversion relative to its matched uniform-source control. It
does not replace the quantum initial state, but confirms that homogeneous
source yields cannot be promoted to full nonlinear predictions.
