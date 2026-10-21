# Alpha=1 proposal: transverse vector reduction with metric shift retained

**Independent analytic result, c=1.** On an isotropic homogeneous medium/chi background, the alpha=1 modification has a k-dependent transverse inertia. Eliminating the metric vector shift does not generally remove its negative direction. The precise reduced coefficient is derived below, including background lambda. No experiment, scalar Poisson substitution or frozen-metric mode test is used.

This is a quadratic vector-sector analysis of the displayed operator proposal, not an adopted action or a full scalar/vector/tensor stability theorem. The Fourier range must lie within the derivative action's validity. A negative vorticity kinetic direction is not by itself a computed exponential growth rate or a quantum-completion verdict.

## 1. Action, variables and gauge

Use K=4pi G, c=1 and the CFG938 action, modifying only its stiffness:

`L=R/(4K)-mn-W_full(sqrt(h^{mu nu} chi_mu chi_nu))`

`  -3 gamma [tau_munu+C sigma_munu]^2/(4K^2)`

`  +lambda [h^{mu nu} nabla_mu nabla_nu chi-Kmn]`,

where `C=u_medium^mu partial_mu chi`. The scalar invariant denoted u in CFG938 is not the medium four-velocity. Sigma is the symmetric traceless projected medium-velocity gradient. The source's tau is the projected four-dimensional Hessian's traceless part, not an intrinsic slice Hessian.

Background: comoving labels phi^I=x^I, spatial scale a(t), rho=m/a^3, chi=chibar(t), C=chidot, and homogeneous lambdabar(t). Background equations are required for a physical perturbation problem; do not silently set lambda to zero. Its constraint is `-3HC=K rho`.

For the transverse irrep choose the spatial-vector gauge E_i=0 and retain the ADM shift:

`ds^2=-dt^2+a^2 delta_ij(dx^i+S^i dt)(dx^j+S^j dt)`,

`partial_i S_i=0`, `phi^I=x^I-pi^I`, `partial_i pi_i=0`.

The shift-square in g00 is retained: N=1, not g00=-1. Define physical amplitudes

`U_i=a pidot_i`, `B_i=a S_i`, `v_i=U_i+B_i`.

V is the medium velocity relative to the hypersurface normal. These are also gauge-invariant combinations before E=0: U=a(pidot+Edot), B=a(S-Edot), so v=a(pidot+S). A static volume-preserving relabeling does not remove the physical vortical velocity pidot.

Each transverse Fourier polarization is normalized so its spatial mean squared amplitude is |v|^2; Parseval/cosine averages are included consistently in that definition. Let `k_p=k_com/a`. There is no extra cosine-average factor in the quadratic coefficients below.

## 2. Expand before eliminating anything

Scalar chi and lambda fluctuations cannot mix bilinearly with a transverse Fourier irrep on this isotropic background. Their background values do contribute. The relevant identities through second order in vectors are:

`u_medium^0=1+|v|^2/2`,

`sqrt(-g) mn=a^3 rho(1-|v|^2/2)+spatial divergence`,

`h^{mu nu} chi_mu chi_nu=C^2|v|^2`,

`h^{mu nu} nabla_mu nabla_nu chi=-3HC+(Cdot-HC)|v|^2`.

The last identity keeps the shift contributions to both the connection and the inverse metric/projector. In particular `Box chi=-Cdot-3HC` in this transverse ADM gauge, while `u^mu u^nu nabla_mu nabla_nu chi=Cdot(1+|v|^2)-HC|v|^2`. No derivative of medium velocity appears in this original Hessian constraint; its apparent acceleration terms cancel.

Since `W_full(u)=u^2/(2K)+O(u^3)`, dust, W and lambda give

`L2,algebraic=a^3 A0 |v|^2/2`,

`A0=rho(1+K lambdabar)-C^2/K+2 lambdabar(Cdot-HC)`.

Using only the homogeneous multiplier constraint, the same expression is

`A0=rho-C^2/K+2 lambdabar Cdot-5 lambdabar H C`.

Thus background lambda does not generically drop out. No lambda background equation or Einstein equation has yet been used here. The spatial Jacobian/divergence pieces integrate to zero for homogeneous lambda and periodic/decaying transverse perturbations.

For the stiffness, the linear spatial components are

`delta tau_ij=C a^2 partial_(i S_j)`,

`delta sigma_ij=a^2 partial_(i pidot_j)`,

`delta(tau+C sigma)_ij=C a^2 partial_(i(S+pidot)_(j))`.

There is no trace term for transverse vectors. Hence

`[delta(tau+C sigma)]^2 = (C^2/2) k_p^2 |v|^2`,

`L2,tidal=-3 gamma a^3 C^2 k_p^2 |v|^2/(8K^2)`.

The same operation that cancels homogeneous tensor shear has moved the stiffness into the medium's velocity gradient. This term depends on relative velocity including the shift; freezing B would miss its constrained reduction.

Einstein-Hilbert contributes the ordinary nondynamical transverse shift square. From `K_ij=a^2[H delta_ij-partial_(i S_j)]`,

`L2,EH=a^3 k_p^2 |B|^2/(8K)`.

There is no vector propagation from pure Einstein gravity. The medium's vortical displacement supplies the remaining vector coordinate.

## 3. Full shift elimination in this irrep

Combining the terms gives, per polarization and nonzero k,

`L2,V=a^3/2 { A(k)|U+B|^2+b(k)|B|^2 }`,

`A(k)=A0-d k_p^2`, `d=3 gamma C^2/(4K^2)`,

`b(k)=k_p^2/(4K)>0`.

Only now vary B. When `A+b != 0`,

`B=-A U/(A+b)`, `v=b U/(A+b)`,

`L2,V,reduced=a^3/2 [A b/(A+b)] |U|^2`.

This is the physical reduced vector kinetic coefficient for U=a pidot. The time dependence of a,A0,C remains explicit in the coefficient and U definition; using a physical displacement xi=a pi would instead give U=xidot-Hxi. No lower-order term is silently turned into a principal kinetic coefficient. At `A+b=0` the algebraic elimination fails and the constraint rank/initial-value system needs separate treatment.

## 4. Does the negative k-squared direction survive?

Write `epsilon=3 gamma C^2/K`, so `A=A0-epsilon b`. For A0>0, gamma>0 and C!=0:

- If `0<epsilon<=1`, the reduced coefficient is negative for `b>A0/epsilon`; its denominator is positive. At epsilon=1 it becomes increasingly negative with k.
- If `epsilon>1`, it is negative for `A0/epsilon<b<A0/(epsilon-1)`. The denominator vanishes at the upper endpoint. Beyond that pole the formal coefficient changes sign; calling all high-k vectors negative in this case would be incorrect.
- The first zero is A=0. These are exact conditional sign intervals, not an estimate from an auxiliary Hessian sign.

Thus there is a nonempty negative reduced-vector band for every positive finite epsilon on a branch with A0>0, provided that band is inside the EFT's actual validity domain. It is not universally a negative asymptotic high-k coefficient. Unknown cutoff physics or different background lambda can change what interval is physically accessible; neither may be inferred from this derivative action alone.

For the same lambdabar=0 dust/radiation FRW branch used in the tensor counterexample, `H^2=2K rho_tot/3` gives

`C^2/K=rho^2/(6rho_tot)`,

`A0=rho[1-f_c/6]`, `f_c=rho/rho_tot`.

Therefore A0>0 for 0<f_c<=1. Using gamma=K Lstar^2/2, the first negative-band threshold can be written without choosing numerical cosmology:

`k_p^2 Lstar^2 = 16(1-f_c/6)/f_c`.

These substitutions apply only to that specified branch. For nonzero lambdabar the general A0 above must be evaluated from a consistent full background before a sign interval is asserted.

## 5. Interpretation and remaining gate

This is stronger than the earlier fixed-metric/frozen-Poisson diagnostic: the transverse metric shift is retained and eliminated, no scalar Poisson elimination was used, and scalar irreps cannot repair this transverse quadratic block on an isotropic background. It gives an explicit reduced negative kinetic band under stated background and validity conditions. Because the perfect fluid supplies no ordinary transverse elastic gradient, this note does not claim a vector frequency proportional to ik, a measured growth rate, or a complete nonlinear/quantum instability classification.

The alpha=1 operator consequently is not established as viable by its tensor cancellation and static first-variation identity. The remaining analysis must check the complete consistent background, vector constraint-degeneracy/cutoff implications, the longitudinal scalar/metric/chi/lambda block, and total degree count. A different action or higher-gradient regulator would need new provenance and its own static, dynamical and dwarf-formation checks. This result supplies no cold-core binding or four-dwarf selector.

## 6. Other background matter is not automatically a frozen vector sector

Rho_tot in a background Friedmann substitution does not specify the perturbations of S_b. If additional minimally coupled healthy ideal fluids carry independent vortical displacements, include their terms before eliminating the shift:

`L2=a^3/2 {A|U+B|^2 + sum_j A_j|U_j+B|^2 + b|B|^2}`,

with A_j>0 under this additional ideal-fluid assumption. Eliminating B gives the multi-fluid kinetic matrix

`diag(A,A_1,...) - w w^T/(b+A+sum_j A_j)`,

`w=(A,A_1,...)^T`.

On the legitimate velocity subspace U_j=0, the medium-direction coefficient is `A Btot/(A+Btot)`, `Btot=b+sum_j A_j>0`. Thus a negative interval immediately after A crosses zero persists while the denominator stays positive; healthy extra fluids shift the pole, not that first zero. In a cyclic ideal-fluid vorticity sector one can instead consistently choose each extra fluid's conserved transverse momentum to vanish, giving U_j=-B and recovering the medium-only shift reduction after the corresponding zero-momentum Routh reduction. This is different from silently freezing its coordinate displacement.

These statements do not replace the actual S_b specification if it has anisotropic stress, nonideal vector dynamics or extra constraints. The A b/(A+b) expression is exact for the specified medium-plus-metric vector block (or the stated zero-momentum ideal-fluid restriction), not a claim to have solved every possible matter sector in S_b. The existence of the adverse reduced direction under these conditions remains an analytic gate failure for the proposed alpha=1 derivative action, not a dwarf/cosmology fit.
