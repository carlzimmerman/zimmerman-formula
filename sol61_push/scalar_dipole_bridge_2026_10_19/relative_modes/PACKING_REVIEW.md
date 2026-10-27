# Independent review: packing and the homogeneous shared reservoir

Reviewer: `self_gravity_dipoles`, assigned independently by `/root`.
Reviewed artifact:
`sol61_push/scalar_dipole_bridge_2026_10_19/sum_rules/PACKING_AND_SHARED_RESERVOIR.md`.
Final SHA-256: `5d5e4edd583814cb614fe54b5371a48a856e25b26515432849ec1ef506086537`.
Date: 19 October 2026. The reviewer did not edit the reviewed artifact.
The antecedent relative-mode note is frozen at SHA-256
`9a726b50fb9b2d6b077cf4ad06613ebf3e4fe25385846c587980f7015976eb2f`.

**Primary verdict: proved as written**, with the explicit restrictions in the
final artifact: separated independently counted diffuse hosts, a local
self-averaging constitutive medium on probe scale `1/k`, and the standard
mean-subtracted/local Jeans two-fluid linearization through nonzero modes.
The single-host form-factor plateau remains valid; neither a formal sparse
ensemble average nor an inhomogeneous dense shared state is excluded.

## Claim card and dependence

The first claim is a scale incompatibility: separated diffuse hosts with
finite nonoverlap filling cannot both be resolved on a form-factor plateau
`k R_b >> 1` and supply many independent mode centers in each probe volume.
The second claim is that two homogeneous separately conserved barotropic
positive-mass fluids coupled only by attractive Newtonian gravity have no
positive gravity-generated relative optical gap as `k→0` in the stated Jeans
linearization.

The first follows from geometry and the declared homogenization criterion.
The second follows from separate continuity equations, Euler equations,
linear Poisson and a two-by-two symmetric matrix. The microscopic validity
of the fluid state, its production and any inhomogeneous continuation are
assumptions or open obligations, not leaves silently proved by this argument.

| Obligation | Assessment |
|---|---|
| Mean host-center count and filling factors | Passed |
| Scale conflict in the separated-host plateau limit | Passed under local self-averaging criterion |
| Sparse Fourier ensemble average distinguished from local medium | Passed by the final scope restrictions |
| Background equilibrium for Jeans calculation | Passed after explicit mean-subtraction/local approximation qualification |
| Continuity/Euler/Poisson signs and density normalization | Passed by independent derivation |
| Symmetric matrix, determinant and positivity threshold | Passed analytically |
| Exact zero density mode distinguished from nonzero-k limit | Passed by the final fixed-mass qualification |
| General shared inhomogeneous-state exclusion | Out of scope and not claimed |

## Packing reconstruction

For a stationary population of center density `nu`, the mean count in a
ball of radius `1/k` is `(4pi/3)nu/k^3`. If the complete diffuse-host spheres
are separated, `f=(4pi/3)nu R_b^3<=1`. Eliminating `nu` gives exactly

\[
 \langle N_{\rm probe}\rangle={f\over(kR_b)^3}.
\]

Thus the deep plateau limit `kR_b→infinity` sends the mean independent-center
count to zero. It cannot simultaneously approach the many-center limit
needed to self-average a local constitutive response on that same probe
scale. Replacing the probe radius by `2pi/k` changes only a fixed multiplier.
For Gaussian profiles with `R_b=C sigma_b` and a fixed effective-radius
constant, the same parametric conclusion follows. A narrowly tuned zero of a
particular oscillatory form factor would not supply this broad scale-separated
plateau limit; the addendum's conclusion concerns the latter.

This is a restriction on local homogenization, not a theorem that an averaged
linear scattering response ceases to exist in a sparse population. Sharing or
overlapping a reservoir removes the packing premise, but removes the ability
to attach its entire mass and recoil inertia independently to every carrier.
Counting that reservoir repeatedly would invalidate the single-host oscillator
strength used to normalize the proposed medium.

## Two-fluid reconstruction

For each species `a`, linear continuity and Euler are
`delta rho_dot=-rho_a div v_a` and
`v_a_dot=-(c_a^2/rho_a)grad delta rho_a-grad(delta U+U_ext)`.
Using `Delta delta U=K(delta rho_d+delta rho_b)` gives

\[
 \ddot{\delta\rho_a}+c_a^2k^2\delta\rho_a
 -K\rho_a(\delta\rho_d+\delta\rho_b)
 =-\rho_a k^2U_{\rm ext},\qquad K=4\pi G.
\]

The gravitational sign is attractive. Dividing by `sqrt(rho_a)` gives exactly
`D=diag(c_d^2 k^2,c_b^2 k^2)-Kvv^T`,
`v=(sqrt(rho_d),sqrt(rho_b))`. In the nonzero-mode limit at zero wavenumber,
`v` has eigenvalue `-K(rho_d+rho_b)`, and
`w=(sqrt(rho_b),-sqrt(rho_d))` has eigenvalue zero. The corresponding density
perturbation satisfies `delta rho_d+delta rho_b=0`. Attractive self-gravity
therefore gives an unstable Jeans mode and no positive relative restoring
eigenvalue in this limit.

At small nonzero `k`, the relative eigenvalue starts as

\[
 \Omega_{\rm rel}^2=
 {\rho_b c_d^2+\rho_d c_b^2\over\rho_d+\rho_b}k^2+O(k^4).
\]

For different sound speeds this branch mixes with the density branch at
finite wavenumber; it is still gapless, rather than an omitted positive
gravity-only optical mode. At exactly `k=0`, separately fixed masses remove
the density variation itself, which is why the final note correctly phrases
its eigenvalue statement as a limit through nonzero modes.

Direct expansion of the determinant gives

\[
 \det D=c_d^2c_b^2k^4
 -K(c_d^2\rho_b+c_b^2\rho_d)k^2
 =c_d^2c_b^2k^2\left[k^2-K\left({\rho_d\over c_d^2}
 +{\rho_b\over c_b^2}\right)\right].
\]

For `k>0` and strictly positive sound speeds, the congruence by
`A^(1/2)`, `A=diag(c_d^2k^2,c_b^2k^2)`, gives one unit eigenvalue and one
eigenvalue `1-K v^T A^(-1)v` inside the bracket. It is positive above the
quoted critical wavenumber and negative below. At equality the matrix is
positive semidefinite with one zero eigenvalue. Positive quantum-pressure
`k^4` terms do not change the zero-wavenumber rank-one gravity matrix and
cannot produce a positive nonzero relative gap there.

An infinite static homogeneous positive density with its full unsubtracted
mean Newtonian field is not a background solution with zero acceleration.
The final note now states the Jeans background subtraction/local model
explicitly. No external anchor or cosmological friction is implicitly
deduced from the original scalar action.

## Review provenance and remaining work

This review reconstructed the geometry, fluid equations and exact matrix
algebra from their definitions. No scientific numerical run or new external
theorem is needed for these statements, and no new numerical evidence is
claimed. I requested three scope clarifications in the earlier draft:
mean center count instead of an exact discrete count, self-averaging locality
instead of excluding formal sparse averages, and Jeans-background/nonzero-k
qualifications. All are present in the final hash reviewed here.

The strongest safe conclusion is that the separated independent-host
implementation cannot provide the proposed controlled local plateau medium,
and the simplest homogeneous shared reservoir cannot supply its missing
positive optical spring. The finite-profile relative source result is
unaffected. The remaining route is a stable inhomogeneous shared state with
its actual mode/source operator and consistently counted mass inventory.
Its nonlinear saturation and occupied joint gap/dipole distribution remain
separate required inputs. This is an independent sibling audit, not a formal
proof certificate or classification of all original-action phases.
