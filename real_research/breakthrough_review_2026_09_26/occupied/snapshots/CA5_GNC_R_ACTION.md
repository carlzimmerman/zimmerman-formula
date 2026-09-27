# CA5-GNC-R: a reciprocal vacuum barrier

This is a new candidate action, not a retroactive pass for CA4-GNC-PQ.
Keep the complete gravity, projected clock, spatial auxiliaries, heat fields,
C4 gate and fixed compensator of
[CA4-GNC](../../common_action_2026_09_26/action/FINAL_ACTION.md).
Keep the five real classical fields and positive `Vmix` of
[the perspective action](../../common_action_2026_09_26/action/PERSPECTIVE_VARIANT.md).
Set bare `Lambda=0`. Replace the entire dark-field Lagrangian, including the
old reciprocal vacuum floor and the PQ quadratic repair, by

\[
 \boxed{\mathcal L_d=tK_d-\frac{W_{\rm exc}}{t}
  -V_0\left[1+\left(t+\frac1t-2\right)^2\right],\qquad
 t=1+Z-\langle Z\rangle_h>0.} \tag{R1}
\]

Here `Kd=(1/2) sum_A (n(field_A))^2`,
`Wexc=(1/2) sum_A |D field_A|^2+Vmix`, and `V0>0` is constant.
The five fields, positive masses and interaction constants remain those
of the previous action. No carrier particle population is introduced.
The fixed coefficient of the square is one; no new fitted coefficient.

The homogeneous vacuum energy is still an input. This construction does
not determine its magnitude, derive the MOND acceleration scale from it,
or solve radiative naturalness. It changes how the vacuum couples to the
projected spatial auxiliary, which is a distinct and testable question.

## The inverse relationship does actual work

Define `F(t)=1+(t+1/t-2)^2`. For every `t>0`,

\[
 F(t)=F(1/t)=1+\frac{(t-1)^4}{t^2}\ge1,
\quad F'(t)=\frac{2(t-1)^3(t+1)}{t^3},
\]
\[
 \boxed{F''(t)=\frac{2(t-1)^2(t^2+2t+3)}{t^4}\ge0.} \tag{R2}
\]

It diverges at both ends of `(0,infinity)` and has its unique minimum at
`t=1`. Its first, second and third derivatives vanish there; the fourth
derivative is 24. It is nonlinear confinement that starts at fourth order
about the homogeneous state. Convexity and quadratic flatness coexist.

In the class of inversion-symmetric Laurent polynomials of degree at most
two, write `a(t^2+t^-2)+b(t+t^-1)+c`. Conditions `F(1)=1` and `F''(1)=0`
give `b=-4a,c=1+6a`; therefore `F=1+a(t+1/t-2)^2`. Choosing `a=1` gives
(R1). This is uniqueness only within that small algebraic ansatz. Inversion
of `F` is not a symmetry of the whole action: `tK-W/t` and the mean-one
constraint are not invariant under `t -> 1/t`.

## Exact action variations

The local lapse density and projected-auxiliary source are

\[
 \rho_R=tK_d+W_{\rm exc}/t+V_0F(t),\qquad
 \sigma_R=K_d+W_{\rm exc}/t^2-V_0F'(t). \tag{R3}
\]

Consequently the exact Z equation is

\[
 2M_P^2c_N\operatorname{div}_N(DZ-a+DU)
 +\sigma_R-\frac{\langle N\sigma_R\rangle_h}{N}=0. \tag{R4}
\]

The lapse sees `rho_b+rho_R`. The U and heat equations, gravitational
momentum and shift constraint are unchanged. The carrier equations and
common U(1) current exchanges are unchanged, since the replacement depends
only on `t`. The vacuum part has `rho_v=V0 F`, `sigma_v=-V0 F'` and

\[
 T_v^{\mu\nu}=-V_0F g^{\mu\nu}
 -\frac{\langle N\sigma_v\rangle_h}{N}\,z h^{\mu\nu},
\quad E_{\tau,v}=\langle N\sigma_v\rangle_h B_Z
                      -\sigma_v\langle NB_Z\rangle_h,
\]

where `z=t-1`, `B_Z=n(Z)+Kz`. These formulas include the h-volume projector
variation. In particular the vacuum source and its linear susceptibility
vanish at `t=1`, while its physical stress is `-V0 g`. This is covariance
of the same preferred-foliation, spatially nonlocal action, not a claim of
local Lorentz invariance or an additional propagating vacuum field.

## Which vacuum shape does infrared health require?

For a general smooth `F` with `F(1)=1`, put `f1=F'(1)`, `f2=F''(1)`.
On the actual empty de Sitter solution, `H^2=V0/(3M_P^2)`, define

\[
 x=q^2>0,\quad S=e^{-\xi^2x/2},\quad r=r_0S,\quad r_0=\ell/4,
 \quad d=\alpha_e=2-(2-\alpha)(1-r)^2.
\]

The general vacuum contribution to the lapse coefficient is

\[
 D_F=\alpha_e x-6H^2r(f_1+f_2r/2). \tag{R5}
\]

For the unchanged host, a nonzero constant `D_F(0)` gives either the
previous negative infrared stiffness, a ghost, or a lapse denominator
pole. The boundary `D_F(0)=-K_sH^2` also has divergent negative kinetic
coefficient whenever its denominator is positive. Hence simultaneous
positive kinetic and restoring coefficients for all sufficiently small
nonzero continuum momenta requires

\[
 \boxed{f_1+\frac{r_0}{2}f_2=0.} \tag{R6}
\]

This necessary condition uses the continuum `q -> 0` demand. A fixed compact
leaf has a lowest nonzero momentum; failure only below that momentum is
not automatically a negative mode on that one leaf. Expanding de Sitter
redshifts every fixed comoving mode toward zero. Condition (R6) does not
by itself suffice for all-mode stability.

PQ met it by choosing `f1=-1,f2=2/r0`. The reciprocal barrier meets it
with `f1=f2=0`, independently of `ell`. Neither choice determines `V0`.

## Vacuum scalar signs, without the old filter-to-Hubble restriction

With (R1), `D=x d`. Let `K_s=2(2+3c2)/c2` and `E=K_s H^2+xd`.
The same on-shell ADM reduction, including the time integration of the
mixed term with measure `a^3`, gives

\[
 A=\frac{K_sxd}{E},\qquad
 C_I=-\frac{2x^2}{E^2}
 [K_sH^2(2+d+2x d_x)+xd(2-d)]. \tag{R7}
\]

For `0<alpha<2`, `0<ell<=1`, `c2>0`, `H>0`, and `xi>0`, one has
`0<d<2`. Writing `u=xi^2 x/2`,

\[
 2x d_x=-4(2-\alpha)u r(1-r)\ge-4r_0,
 \qquad 2+d+2x d_x\ge2-4r_0\ge1.
\]

The bound uses `u exp(-u)<=1/2` and `2-alpha<2`. Both terms in the square
bracket of (R7) are positive. Thus `A>0,C_I<0` for every finite `q>0`.
There is no condition `3H^2 xi^2 ell/4<=0.1` for this statement and no PQ
coefficient `zeta`. As before, `A -> 0` at `q -> 0`; this does not establish
uniform coercivity, full degree counting, nonlinear health, or the occupied
gradient sector. See the independent [occupied calculation](../occupied/).

The previous homogeneous global-future argument also applies: all new
terms vanish in first variation on `t=1`, leaving the identical expanding
Einstein/five-scalar ODE with positive `V0`. Its positive-mass assumptions
and restriction to the homogeneous invariant sector remain essential.

## What this closes and what it does not

The same candidate now has a convex barrier, no vacuum-induced linear
auxiliary susceptibility, and the displayed all-mode vacuum scalar signs.
The [fixed-data theorem](BARRIER_PROOF.md) proves a unique smooth positive
Z solve; joint U/Z conclusions have their own finite-resolution scope.
No global filtered-MOND matching, full post-Newtonian/Dirac analysis,
inhomogeneous global evolution or observational closure is imported.
Calling `V0` vacuum tension is a description of its stress, not a discovery
of the physical origin or measured amount of dark energy.
