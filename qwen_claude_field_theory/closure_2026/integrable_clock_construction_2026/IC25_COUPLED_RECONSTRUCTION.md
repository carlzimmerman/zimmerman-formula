# IC25: jointly reconstruct clock coupling and potential

Base commit `14d7dd714699bba048a4191d512834a4a1e4cfb2`, 2026-09-09.
Full theory **OPEN**. This is a construction from Carl Zimmerman's
exponential-kernel / primordial-clock framework, not a new empirical fit or
a claimed priority result. The original thirteen requirements remain intact.

## 1. Same action, two coefficient functions

Use the IC20 covariant first-order action with the simultaneous, minimally
coupled IC23 radiation and positive-pressure matter actions. Replace ONLY
A(S),D(S) in the gravitational density by the following locally defined
functions. E4(S), the constitutive terms, physical metric and matter
couplings remain unchanged. The relevant pinned density is

    h=-exp(2S)q²/(6v)-A(S)qz-exp(S)P0(S)-D(S)z²-E4(S)z⁴,
    v=exp(S+2wc)/2+z².

The full tensor/spatial terms are those of IC20, not this homogeneous
restriction alone. This reconstruction defines action functions over the
traversed S interval; a global/static extension is NOT provided here.

Let Q=ln(barred scale factor), rhoH=sum h_i, pH=sum w_i h_i and
E0=exp(3Q)(h+rhoH). Initial data are the actual IC23 mixed constraint solution
with q=-3,Q=0,Mr=Mm=10^-6,wm=10^-8. Those fluid idealizations do not model
photon-baryon collisions, recombination, or observed transfer functions.

We study two distinct action constructions:

    linear: S(Q)=S0+kappa Q;
    charge: S(Q)=S0+kappa(1-exp(-3Q))/3,  kappa=.01.

Their wave-diagonal design target is c_g²=.3. Both numbers are engineering
choices, not observations or predictions. A construction history is NOT a
new constraint imposed on the dynamical lapse. The frozen reconstructed
action must yield that history upon variation; this is checked.

## 2. Derivative equation and actual lapse preservation

At fixed S,q,z,Q,A write alpha=A'. Solve h_z=0 for D and h_S+rhoH=0 for D'.
The first-derivative raw jets have the form

    h_Sq=L-z alpha,   h_Sz=U+q alpha,

where L,U, p=h_qz, h_zz and the scalar UV momentum coefficient
a=-p²/(2h_zz) are independent of alpha on that auxiliary shell. Set
Sdot=S_Q Qdot, Qdot=h_q/2 and qdot=-3(h-pH)/2. The z preservation equation
gives zdot=-(h_Sz Sdot+p qdot)/h_zz. With

    Z=-v0+2z h_Sq/p,   rho_mix=-4z/p,
    c_g²=(-2av+4a Z²/B)/exp(2S)
          -2a(rho_mix_dot+Qdot rho_mix)/exp(2S),

the response is exactly quadratic in alpha. In particular

    partial_alpha³ c_g²=0,
    coefficient(alpha²)=-8z⁴/[B exp(2S) h_zz] > 0

on B>0,h_zz<0. These identities are checked symbolically, and the numeric
quadratic predicts a slope not used to construct its coefficients. The
smaller real root is followed continuously on the sampled nondegenerate
branch. Linear and fully degenerate equations have explicit handling; no
real discriminant means that root prescription cannot be used there.

Compute the required lapse Schur coefficient from preservation:

    C=h_Sq-h_Sz p/h_zz,
    M=(-C qdot+3Qdot(rhoH+pH))/Sdot.

Choose the D'' jet so the raw partial variation produces this M, then
recalculate the multipliers with the actual two-by-two auxiliary matrix.
The script does not assign its multiplier, auxiliary rank, determinant,
coupled eigenvalues, PPN parameters or DOF counts as certification outputs.
The active pin is checked explicitly; pin-off states cannot silently use
the pinned reduction.

## 3. Two-function integrability

Evolve q,z and A_Q=alpha S_Q, using the varied background flow. Differentiate
the selected root along that flow to obtain

    A''=alpha_dot/Sdot.

Reinsert A'' into the raw action and recompute D''. Altering A'' shifts D''
by -q A''/z; hence the raw h_SS change cancels:

    -qz A''-z²(-q A''/z)=0.

This explains why zero-placeholder A'' is sufficient during the background
integration but NOT during perturbation variation. `completed()` supplies
the genuine second jets. Independent directional derivatives check

    alpha_dot=A''Sdot,
    Ddot=D'Sdot,
    (D')dot=D''Sdot,
    E0dot=0.

As in the IC24 local lemma, the last two coefficient identities follow by
differentiating h_z=0 and h_S+rhoH=0 and subtracting their varied preservation
equations. Nonzero z,Sdot and regular constraints are required. Each chosen
history has Sdot>0 for finite Q on an expanding branch. This gives one pair
of S-only functions locally, not an off-shell dependence on matter, q or z.

## 4. Why scaling the clock drift helps the homogeneous constraint

The conserved charge rewrites the trace-momentum equation exactly as

    qdot=-3E0 exp(-3Q)/2+3(rhoH+pH)/2.

For constant S_Q, bounded C and nonzero limiting Qdot, dilution drives M
toward zero when the matter enthalpy disappears. The linear-history probe
reached a chosen numerical safety cutoff |M|~10^-5 near Q~6.04, not a proven
finite-time rank loss or a no-go theorem.

For S_Q=kappa exp(-3Q), the same preservation equation instead reads

    M=3C E0/(2 kappa Qdot)
      +(3-3C/(2Qdot)) exp(3Q)(rhoH+pH)/kappa.

This identity is checked exactly. With bounded C/Qdot and appropriately
diluting matter, it permits a finite nonzero asymptote instead of forcing
M to zero through the clock dilution factor. It does NOT prove the limit
exists or has the required sign for every solution. Higher jets at the
finite limiting value S_infinity=S0+kappa/3 must still be controlled.

An exploratory charge-profile integration reaches Q=7 with negative M
(about -410), positive sampled kinetic and cone margins, and expanding H.
Absolute charge drift grows to about5.3e-7 there in double-precision evolution;
this is NOT high-precision evidence for the infinite-Q limit. Refinement,
actual higher jets and all sampled roots are retained in the run report.
Seven barred-scale e-folds on a designed branch are not a calibrated
recombination cosmology. Linear and charge profiles are distinct actions;
their successes are never pooled.

## 5. Full perturbation evolution, not just frozen frequencies

The three-field quadratic Hamiltonian K,L,W is the IC23 expression evaluated
with the reconstructed action jets. All six instantaneous Euler roots use
third jets and off-shell Taylor functions of S ONLY. Merely substituting
D(S,q,z,Q) or A(S,q,z,Q) during partial variation would change the theory.

For direct nonautonomous evolution, the symplectic term is V p^T D xdot,
V=exp(3Q), D=diag(2,1,1). Thus the density-momentum Hamiltonian generator is

    G_H=[[2D^-1 L,                  2D^-1 K],
         [-2D^-1 W, -2D^-1 L^T-3Qdot I]].

Evolve F_Q=(G_H/Qdot)F with F(0)=I, and physical k²(Q)=k_initial² exp(-2Q).
For Omega=[[0,D],[-D,0]], the exact identity

    G_H^T Omega+Omega G_H=-3Qdot Omega

implies det F=exp(-3nQ) for n matter-plus-clock scalar fields (here n=3).
The complete matrix identity and trace are checked symbolically; the actual
propagator is checked numerically against the volume identity. The latter
is an independent structural check, not a stability criterion.

Transfer matrices use the explicitly stated fixed initial kinetic norm on
(x,xdot/Qdot_initial). Their singular values measure amplification in that
norm; they are not coordinate-independent stability thresholds. The output
compares 81 and161 interpolation nodes and initial k²=1,100 over Q in[0,1].
It does not establish all-wavelength, all-time or nonlinear stability.

## 6. What remains before calling this a theory

This is a substantial designer-action construction, not full closure.
Still required: controlled S_infinity and zero-field limits; smooth global
extension to the static galactic branch; SAME functions with different matter
sources; general nonlinear Dirac closure and physical elliptic-channel audit;
relative flows, vector modes, canonically normalized interaction scales;
Phi and Psi independently, measured G and full PPN; and actual plasma,
galaxy/cluster/CMB likelihoods. The original a0-Lambda normalization remains
input, not a first-principles derivation. No Lean or independent-review
certificate is claimed. Mathematical proofreading and computation self-review
cover this note and new code; exact commands/statuses are in the run index.

The next calculation should test the same reconstructed functions away from
their design trajectory and their limiting coefficient jets. Do not replace
this with another independently tuned background or label modest finite
amplification a complete stability proof.
