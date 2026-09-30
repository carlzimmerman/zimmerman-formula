# Conditional protection in a doubled local surface operator

This follows SURFACE_NEUTRALITY_RESULTS.md. Units c=hbar=1. Introduce a two-component copy index tau, surface spin sigma and two-component internal flavor lambda. The collocated eight-component differential operator is

H8(k,p)=tau_z tensor [v(k_x sigma_x+k_y sigma_y) tensor I + y sigma_z tensor (p_i lambda_i)].

It is first order in tangential derivatives and local as a surface operator. No embedding into the prior bulk kink or covariant gravity action is derived. Doubling an effective spectrum is not itself a physical prediction of two wall species.

Define T=(I tensor sigma_y tensor lambda_y)K, C=(tau_x tensor sigma_y tensor lambda_y)K and P=tau_x tensor I tensor I. All square to +1. For a time-even polar vector p,

T H8(k,p) T^-1=H8(-k,p),

C H8(k,p) C^-1=-H8(-k,p),

P H8(k,p) P^-1=H8(-k,-p).

P includes spatial inversion of the coordinates. C is a spectral particle-hole constraint here; a physical charge-conjugation operation and its many-body action have not been constructed. The relation C=P T between their internal maps makes the homogeneous protection transparent: if a constant Hermitian perturbation B is T-even and P-even, C transforms B to +B, while the particle-hole constraint requires -B. Hence B=0. This is an exact statement for homogeneous constants independent of k and p. It leaves the derivative terms and the p-dependent coupling above intact, because they have the required coordinate/order-parameter transformations.

The complete 64-element Hermitian Pauli-string classification corroborates this argument. With T and C only, 16 real basis directions survive; imposing internal flavor rotations leaves tau_y tensor sigma_x,y,z tensor I and tau_z tensor I tensor I. Adding P removes them all. Each symmetry map is diagonal with signs in this basis, so no cancellation among basis members hides an additional allowed linear combination.

## Total neutrality can still conceal the failure

In particular B=delta tau_z tensor I tensor I is allowed by T, C and flavor rotations. It moves the two cones in opposite energy directions. At zero global chemical potential and |m|<|delta|, the two independent copies contain opposite carrier densities

n_plus=-n_minus=2(delta^2-m^2)/(4pi v^2),

where each quartet has positive-band degeneracy two. The sign of the copy label is conventional. Their total charge is zero. Their combined grand potential, using the same vacuum subtraction as the previous audit, is

Omega_total=-|delta|^3/(3pi v^2)+|delta|m^2/(pi v^2).

It has no cubic term in this regime. At delta=0 the two copies instead give total positive-band degeneracy nu=4 and Omega=4|m|^3/(6pi v^2). Thus total charge neutrality alone does not restore the cubic. Inversion forbids this homogeneous opposite-offset term in the ideal model. An identity energy reference shift must still be distinguished from filling relative to a cone.

## Scope of the improvement

This supplies a concrete conditional surface symmetry structure rather than leaving gap and neutrality protection wholly unspecified. The 13 exact checks pass; the uniform classification is complete for the stated operator and symmetry maps. No numerical sampling or source-dependent theorem is used.

It does not prove robustness to interactions, spontaneous symmetry breaking, gradients or disorder. For example delta(x) tau_z is inversion invariant when delta(-x)=-delta(x), and preserves the other specified single-particle constraints. The homogeneous classification therefore cannot be promoted to protection in an inhomogeneous galaxy. A nonzero polar stream generally breaks time reversal and inversion unless additional state transformations or compensating species are supplied. Whether these symmetries describe the intended medium remains open.

The scalar polarization term |p|^2 and an additive vacuum energy are permitted. Critical quadratic matching and the absolute vacuum curvature remain unselected. With nu=4 the prior homogeneous coefficient would give a0=ell v^2/(8G y^3), still containing free density, speed and coupling. The factor of two from doubling is a count of chosen modes; it neither derives the half factor in a0=c^2/(2R_rho) nor selects Lambda/a0^2=32pi. Positive-tension wall stress also remains incompatible with a sole vacuum source.

Next physical discriminator: a local bulk/medium implementation of the spectral constraint and inversion, tested in the actual inhomogeneous state, together with a symmetry or dynamical mechanism selecting critical matching and a vacuum-like stress. Without those links this is a conditional response construction, not the requested unified theory.
