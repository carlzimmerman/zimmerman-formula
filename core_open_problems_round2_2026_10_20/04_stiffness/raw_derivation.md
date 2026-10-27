# Raw candidate derivations for independent review

Base `8aa3f7046a7ae14a99f3515fd42df5bf061fb1db`. Definitions: `K=4piG`, `gamma=KLstar^2/2`; the canonical static spatial energy is `gamma/2 integral |grad P|^2`. We retain its supplied local potential and gravitational coupling. These claims concern matching a spatial operator and selecting its coefficient, not a full origin of S2.

## A. Ordinary stress-free elastic displacement

Assume a homogeneous isotropic solid without prestress, a physical displacement `xi`, frame-indifferent energy to quadratic order, and constant density `rho0>0`. With infinitesimal strain `e_ij=(partial_i xi_j+partial_j xi_i)/2`, let

`F_el = integral [lambda/2 (tr e)^2 + mu e_ij e_ij]`, `P=-rho0 xi`.

For a Fourier plane wave the Hessian acting on P is

`D_el(k)=rho0^-2 [mu k^2 I + (lambda+mu) k k^T]`.

Matching both canonical sectors requires `mu=gamma rho0^2` and `lambda+2mu=gamma rho0^2`, hence `lambda=-mu`. The bulk modulus is `B=lambda+2mu/3=-mu/3<0` when gamma>0. In uniform affine compression `xi=alpha x`, `e=alpha I`, the local energy density is `(9lambda/2+3mu)alpha^2=-3mu alpha^2/2<0`.

The latter strain is not periodic/decaying. Under such restricted boundaries, integration by parts gives `F_el=mu/2 integral |grad xi|^2 +(lambda+mu)/2 integral (div xi)^2`, so the matched plane-wave operator is positive even though a free homogeneous solid has negative bulk modulus. Thus this does NOT prove an instability of canonical S2 or every fixed-boundary model. It excludes a mechanically stable stress-free ordinary solid with positive bulk and shear moduli from supplying the complete operator in this displacement dictionary. Pinning, prestress, independent rotational elasticity, and internal vector coordinates are outside the statement.

## B. Vector alignment lattice

Take a cubic lattice of spacing b. At each cell R an internal three-component coordinate p_R has kinetic energy `M/2 |dot p_R|^2`. Give each positive-axis bond energy `J/2 |p_(R+b e_alpha)-p_R|^2`, with J>0, counting each bond once. The coordinate p has the physical normalization of P; local potential per cell is `b^3 Wrem(K|p|)`. This local potential and gravitational coupling are assumed inputs.

The bond Hessian per physical volume is

`D_bond(k) = (4J/b^3) sum_alpha sin^2(k_alpha b/2) I_3`.

At small kb it equals `(J/b) k^2 I_3 + O(J b k^4)`, so `gamma=J/b`, `I_eff=M/b^3`, `c_ac^2=J b^2/M`, and `Lstar^2=2J/(Kb)`. All three internal components receive the same spatial coefficient for every wave-vector direction, though the exact dispersion has cubic anisotropy.

For a literal internal displacement d with ordinary inertial mass m_cell and bond spring constant j, let `P=zeta d`. Then `M=m_cell/zeta^2`, `J=j/zeta^2`, and `gamma=j/(zeta^2 b)`. Thus the above generalized M is not automatically a particle mass; the polarization normalization zeta must be independently supplied. The ordinary density-displacement dictionary would set zeta=rho0, but the optical coordinate discussed below does not satisfy that dictionary for total mass.

For fixed b and a prescribed speed v, the transformation `(J,M)->(aJ,aM)` with any a>0 preserves the lattice frequencies of the pure bond system, c_ac and its dimensionless derivative errors, while multiplying gamma and Lstar^2 by a. This does not preserve background restoring frequencies from Wrem, nor claim those are measured. The supplied local potential and gravitational coupling are unchanged. Stability, the full tensor matching, and a speed bound alone cannot select the amplitude J/b. P's gravitational normalization forbids absorbing this freedom into a harmless P rescaling.

The scalar bond tensor is a constitutive assumption. Independent rotations of the internal coordinate would protect it in the isolated bond system, but the gravitational coupling P.grad Phi leaves only simultaneous spatial/vector rotations. These permit separate `(div P)^2` and `|curl P|^2` coefficients. No quantum/radiative protection of their equality is established here.

For a two-constituent cell with positive masses m1,m2 and internal separation d at fixed cell center of mass, the mass dipole is `m1 delta x1 + m2 delta x2=0` because `delta x1=m2 d/(m1+m2)`, `delta x2=-m1 d/(m1+m2)`. Its total density Fourier amplitude has no term linear in k.d; the first internal perturbation is quadratic. Therefore this optical coordinate cannot be identified with a linear TOTAL mass polarization satisfying delta rho=div P. A relative/species polarization or an external anchor may exist, but it is a new mapping hypothesis. This statement does not exclude a separate center-of-mass displacement mode.

## C. Local mediator continuation

Introduce an internal vector q and, for each static eigenmode h>=0 of the inherited gravitational-plus-local Hessian, use

`L2=I/2 dot p^2 + Jq/2 dot q^2 - h/2 p^2 - C/2(q-p)^2 - D/2 |grad q|^2`,

with I,Jq,C,D>0. D can be the J/b coefficient of the alignment model; it is not claimed predicted by the continuum action. The spatial-gradient structure is identical for all three components before the inherited h is added.

Static elimination gives `q=C p/(C+D k^2)` and

`H_eff(k)=h+C D k^2/(C+D k^2)=h+D k^2/[1+ell^2 k^2]`, `ell^2=D/C`.

Thus gamma=D, `Lstar^2=2D/K`, and the relative error of the local derivative term against its exact mediator contribution is `(k ell)^2`. It is not a local k^2 operator beyond this range.

At angular frequency omega the inverse response is

`H_eff(omega,k)=h+C-I omega^2-C^2/(C+D k^2-Jq omega^2)`.

Expanding for `|D k^2-Jq omega^2|<<C` gives `h+D k^2-(I+Jq)omega^2-(D k^2-Jq omega^2)^2/C+...`. The exact generalized eigenproblem has polynomial

`I Jq omega^4-[Jq(h+C)+I(C+D k^2)]omega^2+(h+C)(C+D k^2)-C^2=0`.

Positive kinetic and potential quadratic forms imply nonnegative omega^2 for h,k>=0; the sole zero mode occurs for h=k=0. At h=0,k=0 the gapped mode has `Omega^2=C(I+Jq)/(I Jq)`. The gapless branch has small-k speed `sqrt(D/(I+Jq))`. The material PDE principal part has one propagating characteristic speed `sqrt(D/Jq)` and local p oscillators. A condition `D/Jq<=c^2` controls this material sector; it is not a proof of a relativistically causal gravitational completion because Phi is still Newtonian.

For fixed ell and front speed v, `(D,C,Jq,I)->a(D,C,Jq,I)` keeps ell, front speed, the h=0 branch frequencies and gap unchanged, yet changes gamma and Lstar^2 by a. At fixed independently known inertia the speed constraint gives an inequality rather than a selected gamma. This is a scoped nonidentifiability result, not a claim that no UV theory can determine the constants.
