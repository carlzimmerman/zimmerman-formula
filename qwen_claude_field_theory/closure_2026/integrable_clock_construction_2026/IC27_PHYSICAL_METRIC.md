# IC27: physical potentials and the tensor-coupling slip identity

Base: b2a5cc4ec32122984c19e5749e29a15b191ae716 plus the hashed IC26
construction in this working tree. Full theory **OPEN**.
Carl Zimmerman's exponential constitutive law, vacuum-scale relation and
primordial-clock proposal motivate this continued construction. No new
observational fit, novelty priority, or complete gravity theory is claimed.

## Decision and scope

Keep the selected IC26 action, M_*=-.03, and its three S-only coefficient
functions unchanged. Do not tune another action to suppress its observables.
Recover the physical metric from the momentum and auxiliary constraints,
check its coordinate transformation directly, and identify what sources slip.
This is a bounded extension of the existing quadratic calculation, not a new
covariant ansatz. The previous goal reply clarified vacuum density but did not
advance field-theory closure; this calculation addresses the missing physical
interpretation directly.

The active pin fixes w=wc. Work at k!=0, on the expanding flat background.
The existing IC23/26 quadratic action is the input; this work does not
independently re-vary every covariant term in IC20. All background functions
and their time derivatives are from that SAME IC26 construction.

## 1. Recover lapse and shift separately

The phase basis is (zeta,delta sigma_r,delta sigma_m,delta q,s_r,s_m),
with s_i=delta P_i/V. Define k² using the barred spatial metric.
With the tracefree momentum parameterized by

    delta pi_TF/V=(k_i k_j/k²-delta_ij/3) s_TF,

the linear momentum constraint and preservation of the scalar spatial gauge
give, respectively,

    2s_TF+delta q-(3/2)sum j_i delta sigma_i=0,
    2t s_TF-2k² chi=0.

Here N^i=bar h^{ij} partial_j chi. Thus

    chi=-t[delta q-(3/2)sum j_i delta sigma_i]/(2k²).

Variation of the lapse auxiliary gives

    delta S=-[C delta q+sum u_i s_i+
              (4e k²-3sum(1+w_i)h_i)zeta]/[M_*-2Bk²].

No metric potential is assigned from the other.

For each minimally coupled matter scalar the reconstructed metric obeys

    delta sigma_i dot=u_i[delta S+w_i(s_i/j_i-3zeta)],
    s_i dot+3Qdot s_i=-j_i k² chi-exp(2S)j_i k² delta sigma_i/u_i.

These equations are checked against the full coupled Hamiltonian generator,
not imposed as replacement equations.

## 2. Physical metric and coordinate-invariant potentials

Let N0=exp(S+wc), d tau=N0 dT and A_phys=exp(Q+wc).
The physical unitary-gauge metric has

    phi=delta S, psi=-zeta, g_tau_i=partial_i b,
    b=exp(wc-S)chi.

For a general scalar spatial perturbation E, define shear b-A_phys² E_tau.
The script computes minus the Lie derivative of the background metric under
an arbitrary Fourier time shift and scalar spatial shift. The derived shear
changes by the time shift, while phi and psi change by minus its proper-time
derivative and plus H_phys times it. The following combinations therefore
annihilate a pure coordinate perturbation:

    Phi=delta S+exp(-2S)(chi dot-Sdot chi),
    Psi=-zeta-exp(-2S)Qdot chi,
    delta_i^B=(1+w_i)[s_i/j_i+3Psi],
    delta T^B=exp(-2S)chi.

Here dots denote T derivatives, not proper-time derivatives. Density and
clock invariance are checked by transforming their background scalars.
These are cosmological physical-metric potentials, not galactic PPN
parameters. A numerical Psi/Phi ratio on an evolving mode is NOT gamma_PPN.

## 3. Exact quadratic slip reduction

Write R_p=delta q-(3/2)sum j_i delta sigma_i. Differentiating the actual
unreduced quadratic Hamiltonian gives

    R_p dot=-3Qdot R_p-2d k² delta q
             +(2v k²-8H_RR k^4)zeta-2e k² delta S.

The matter momentum and homogeneous mass terms cancel using the same
matter equations, rather than by discarding matter perturbations.
With v=v0+z², v0=exp(S+2wc)/2, t=exp(2S)/v, this implies

    Phi-Psi=(1+e/v)delta S+(d/v)delta q
             +(4H_RR/v)k²zeta
             +exp(-2S)(tdot/t-Sdot)chi.

The SAME auxiliary elimination gives

    d=2z h_qz/h_zz,
    e=-v0+2z h_Sz/h_zz,
    H_RR=-4z²/h_zz,
    delta z=-(h_Sz delta S+h_qz delta q-8zk²zeta)/h_zz.

Substitution, checked exactly in SymPy and against raw varied numerical
coefficients, yields the constructive identity

    Phi-Psi=-(z²/v) D_B,
    D_B=2delta z/z-delta S
           +(2zdot/z-Sdot)exp(-2S)chi.

D_B is the gauge-invariant perturbation of ln(z² exp(-S)) on this
regular z!=0 branch. No claim extends this logarithm to z=0.

There is a physical interpretation using the actual tensor action. Its
coordinate-time kinetic term V gamma_dot_ij²/(4t), converted to proper time
and physical volume, is A_phys³ M_T² gamma_tau_ij²/8, where

    M_T²=2exp(S-2wc)/t=1+2z²exp(-S-2wc).

Consequently the same identity reads

    Phi-Psi=-delta ln(M_T²)|_B.

This M_T² is in the normalized action units. It is NOT an independently
derived measured Newton constant. The wave speed can equal light speed while
this normalization fluctuates; c_T=1 alone does not guarantee no slip.
No assertion that this general type of relation is new in scalar-tensor
gravity is made. What is established here is its reduction for this action.

## 4. Attack preservation, not just initial no-slip data

Let ell(T,k) be the actual row mapping the six phase coordinates to Phi-Psi
and let G_H be their time-dependent Hamiltonian generator. Evolution gives

    (Phi-Psi)dot=(ell dot+ell G_H)phase.

Thus a nonzero ell's zero-slip subspace is invariant exactly when the latter
row is proportional to ell. This is a finite-dimensional linear-algebra
statement at each nonzero Fourier mode, not nonlinear Dirac closure.
The script differentiates the actual background row including k²dot=-2Qdot k².
It computes singular values of the two separately normalized rows in initial
kinetic coordinates and reports the rank at a declared threshold.

It also constructs an explicit unit-kinetic phase direction with zero initial
slip, using the component of the preservation row perpendicular to ell.
Its initial slip derivative is computed, not assigned. Direct differentiation
of the independently reconstructed metric tests this derivative.
If it is nonzero, initial equality alone is not a dynamical no-slip solution.

## 5. Bounded evidence and unavoidable continuation

The report samples Q=0,1 and k²=.001,.01,.1,1,10,100 at 50 digits,
using the IC26 double-precision background interpolation. It retains all six
Euler roots and reports the physical potentials of the fastest instantaneous
mode. Such a mode is not a finite-time growth history; no CMB transfer spectrum
or statistical prediction is manufactured.

k=0 remains separate: a homogeneous shift gradient vanishes, so the inverse
Laplacian used here cannot determine its shear. IC26 homogeneous constraints
remain applicable; the present reconstruction explicitly rejects k=0.
The static pin-off and zero-field sectors are not covered.

The most direct constructive obligation is now precise: show that the relevant
galactic branch has delta ln(M_T²)|_B=0 by its field equations and boundary
conditions, while preserving the exponential constitutive law, constraint
count, minimal matter coupling and expanding cosmology. Adding this equation
by hand would change the theory. Cosmological slip alone does not disprove
the separately specified galactic no-slip requirement.

Still unproved: global coefficient extension, same functions for changed
matter backgrounds, nonlinear constraint closure, physical elliptic-channel
causality, strong-coupling scales, static Phi/Psi and all PPN parameters,
measured G, and real galaxy/cluster/recombination data. Lean/lake were not on
PATH when checked; these are SymPy identities and numerical tests, not Lean
certificates. Mathematical proofreading is self-review, not peer review.
