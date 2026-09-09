# IC19: normalized clock, spatial constraints, and the remaining kinetic repair

Base: `9b7d7b3db109f14a3f17d1e71efa384bd16f0690`, 2026-09-08.
**Full theory OPEN. This action improves the expanding and auxiliary sectors
but fails the scalar-energy requirement in its transition.** Keep the
successful components; the precise kinetic compatibility below is the next
construction target, not a license to announce closure.

Carl's original a0–vacuum relation and primordial-clock proposal motivate this
revision. The normalization is imposed as an action coefficient, not derived
or fitted here. No global novelty claim, empirical fit, or Lean proof is made.

## 1. One action, including the changes outside the plateau

Retain the fields, canonical map, pole domain and physical matter coupling
of [IC18](IC18_PINNED_CLOCK.md). Use its fixed wc=-1/40, Sstar=3/40,
epsilon=10^-5 and positive Lambda, but now set

    a0²=Lambda/(32 pi)   (c=1).

The former IC5 relation fixing a0 to its old expanding witness is NOT also
imposed. The new expanding solution must come from this action. Change every
activation in H18 to the same lapse-independent momentum argument

    r=-p/(3 m h0),  eta=eta_up(r),

instead of -Np/(3mh0). This is a covariant scalar made from the physical leaf
momentum and fixed constants. It equals Hphysical/h0 on the Einstein plateau,
not throughout the transition: momentum variation there contains eta_p.
As before, m=h0=1 and kappa=6 in the executable numerical convention.
The report retains controls using the former lapse-dependent argument in
this normalized, operator-cleaned family. They are not IC18's full curved
action and are not pooled with the final IC19 witnesses.

Remove the obsolete curvature/gradient operators whose coefficients were
chosen for the old IC4 witness. The COMPLETE revised phase Hamiltonian is

    H19 = H18[a0²=Lambda/(32pi), eta=eta_up(-p/(3mh0))]
           +(1-eta) p² (Fcurv Rhat+J)/(2 m a0²),
    S19 = integral sqrt(-g) [2 P:Q-H19] + Sm[g,psi].

Fcurv and J are exactly the functions named F and J in IC4/IC5, not the
new clock pressure F18. The added term cancels their residual occurrences
in H18. It and its first variation vanish at p=0, preserving the independently
varied static exponential equations under the original boundary prescription.
No whole-galaxy, no-slip, or PPN solution is inferred from this zero-jet fact.

The global open domain is the inherited regular chart intersected with
`{r²<1/2} union {0<Xtilde<Xstar}` using the NEW r. Inactive corrections are
defined before evaluating a pole. On eta>0 the varied multiplier still gives
w=wc. Eliminating this holonomic pair does not change the remaining canonical
metric variables. The w equation determines the multiplier, including spatial
terms; it is not silently thrown away.

## 2. The normalized cosmology has an invariant expanding plateau

On eta=1 both new changes reduce to the same exact pinned Einstein-clock
action, with physical Einstein coefficient m and physical vacuum density
m Lambda. All plateau equations follow from that SAME restriction, not by
borrowing a different model's lensing or mode count. With delta=1-X/Xstar,

    F18=-m Lambda exp(4wc)+epsilon(1-delta)^2/delta,
    rho_clock=m Lambda exp(4wc)
               +epsilon(1-delta)^2(delta+2)/delta²,
    Q=epsilon/Xstar (1-delta)(delta²+delta+4)/delta³ > 0,
    F_X>0,  c_clock²=delta(1+delta)/(delta²+delta+4)<1,
    Atilde³ F_X sqrt(2X)=constant.

For any nonnegative homogeneous dust and radiation densities,

    r²=Hphysical²/h0² >= Lambda/(3 h0²).

Here Lambda>3h0²: its defining IC5 expression is
`6h0² exp(-1/2)-a0_legacy² U(4/9)`, U(4/9)<0 and exp(-1/2)>1/2.
Thus the bound is strictly greater than 1, hence greater than the eta=1
threshold 3/4. Numerically the lower bound is **1.2996686626**.
This proves that an expanding homogeneous solution on the pole interior
stays in the active plateau, as long as its regular solution exists.
It does not establish a galactic spatial transition.

The charge is positive and monotone in X since its derivative is proportional
to Q>0. Future expansion drives X downward without reaching X=0 at a finite
nonzero charge and finite scale factor. The early dust-like limit and radiation
equations are unchanged. No claim of nonsingular past completion, endpoint
strong-coupling control, realistic recombination, or an empirical CMB fit follows.

## 3. Full pinned spatial Hamiltonian and actual lapse variation

Let V=sqrt(hbar), q=pi/V be trace barred momentum density, and let pi_TF/V
denote its trace-free part. After the pin and the operator cancellation, the
Hamiltonian density on eta>0 is exactly

    H/V = T(S) |pi_TF/V|² + f(S,q)
           -A(S) Rbar-B(S,q)|Dbar S|² + Hmatter/V,
    T(S)=2 exp(S-2wc)/m,
    A(S)=m exp(S+2wc)/2,
    B(S,q)=(1-eta) m exp(S+2wc)(1-u(S)²),
    u(S)=(S+2wc)/(S+wc),
    r=-exp(-3wc)q/(3mh0),
    f=-exp(S-2wc)q²/(3m)
      -exp(S)[(1-eta(q))P0(S,wc)+eta(q)F18(S)].

P0 is the explicitly defined IC18 pressure, now with normalized a0². The
identity `2u(S+wc)u_S+(S+wc)^2 u_S²=1-u²` is checked symbolically: it
accounts for the inherited mixed auxiliary gradients rather than deleting
them. No spatial derivative of q has been inserted into H19.

Variation at fixed canonical metric momenta gives the lapse secondary

    C_S/V = partial_S(T|pi_TF/V|²+f+Hmatter/V)
             -A_S Rbar -B_S |DS|²+2 D_i(B D^i S).

The last divergence includes derivatives of q through B. The script derives
the expression by Euler differentiation and checks its expanded local form;
it does not assign an elliptic equation. The spatial momentum constraint is
the standard canonical generator, with the clock/auxiliary primary pieces
retained before reduction. All ordinary matter remains minimally coupled to
g, so its own on-shell Ward identity is unchanged.

For an isotropic momentum and homogeneous S,q on a constant-curvature leaf,
the actual auxiliary linearization at fixed metric/momenta is

    M(k)=f_SS-A Rbar-2B k².

This is not the scalar propagating-mode kinetic coefficient. Solving it does
not by itself certify a healthy scalar. In a general inhomogeneous background
its lower-order coefficient contains background gradient terms; the present
constant-coefficient result is not claimed for arbitrary profiles.

The pure TT principal Hamiltonian after the cancellation is
`2N pi_T²/m+mN k² gamma²/8`; Hamilton's equations give
`gamma_ddot+N² k² gamma=0`. Its kinetic sign is positive. This calculation
is for the isotropic local principal sector, not a claim to have diagonalized
all possible anisotropic mixed perturbations in the transition.

## 4. Curved constraint data, k=0 versus k!=0, and preservation

At any chosen regular S,r in the transition, set

    Rbar=f_S/A.

Where this is positive it defines a closed constant-curvature leaf and solves
the lapse secondary. Isotropic momenta solve the spatial momentum constraints.
The pin supplies its auxiliary equations. This is not an off-constraint flat
background obtained by discarding its energy equation.

On S^3, `k_ell²=ell(ell+2)Rbar/6`. The residual lapse primary and secondary
have mode bracket `[[0,-M_ell],[M_ell,0]]`; its entries and ranks are computed
for ell=0..4. If M0<0 and B>0, then **every** scalar Laplacian mode has
M_ell<0, including the distinct uniform mode. That last statement follows
from the spectrum inequality, not by extrapolating five ranks. High-ell
physical scalar modes, rather than gauge-special low harmonics, are used
for the instability below. The separately eliminated pin block remains
invertible because eta>0. No inverse-Laplacian zero mode is concealed.

Continue preservation for the homogeneous background. With Qmetric=ln Bscale,
p_Q=2pi, V=exp(3Qmetric) and Rbar proportional to exp(-2Qmetric),

    {C_S,H}/V = [(3 f_S-A Rbar)f_q-(3f-A Rbar)f_Sq]/2,
    Sdot=-{C_S,H}/(V M0).

The script differentiates the full volume Hamiltonian independently to check
this bracket. When M0!=0 it fixes a finite lapse multiplier; it is not the
previous fold's incompatible preservation condition. These smooth homogeneous
equations give a local evolution on the regular constraint branch. They do
not establish a globally regular spatial evolution or a galaxy embedding.

At S=.1, r=.82 the computed same-action witness has

    eta=.9991640737586682, Rbar=3.600408912491663,
    Hphysical=.7022054224992681,
    M0=-.7033298437778007, B=.000488213942341339.

It is expanding, positively curved, and has an invertible auxiliary operator
for every Laplacian mode. The source and finite Sdot are in the raw report.

## 5. The next gate exposes negative physical scalar energy

Choose a high-frequency scalar wavevector along x. The principal spatial
momentum constraint is solved by
`delta pi=diag(0,delta q/2,delta q/2)`, giving
`|delta pi_TF|²=(delta q)²/6`. Its scalar symplectic term is
`2 delta q zeta_dot`; this is not the discarded gauge conformal momentum.
Both identities are derived from the momentum matrix in the script.

Before eliminating the lapse perturbation n, the momentum-dependent quadratic
Hamiltonian is

    H2=a_UV (delta q)²+f_Sq delta q n+M(k)n²/2+...,
    a_UV=T/6+f_qq/2
        =-exp(S)(F18-P0) eta_qq/2.

The last equality is an EXACT action identity. Eliminating n gives

    a_reduced(k)=a_UV-f_Sq²/[2 M(k)].

Since B>0, M(k) tends to -2B k² and a_reduced tends to a_UV. At the
regular expanding witness above, **a_UV=-13.40362867...**. The computed
coefficient stays negative at the high-frequency controls, including
k²=10^8 and 10^12, far above the curvature scale. Curvature corrections to
the momentum-constraint principal part vanish in that limit and cannot
reverse a strictly negative leading coefficient. The unbounded high-ell
spectrum supplies such modes on the closed leaf. This is a negative-energy
physical scalar direction after the constraints, not a negative unreduced
Einstein conformal term or a mere sign of a determinant.

The code labels the finite-k Schur calculation a frozen UV diagnostic, not
the full finite-wavelength dispersion relation. No gradient-stability pass
is assigned; a ghost already violates the requested healthy-clock condition.

### Restricted structural obstruction, not a framework-wide no-go

This failure is not fixed just by the a0 normalization or a slightly different
smooth switch shape. In the fixed-Einstein-TT, lapse-independent pure-pressure
interpolation class, a_UV has the exact form above. At S=.1, F18-P0<0 can be
shown without a fitted number: U(c)<0 follows from U(0)=0 and
`U'(c)=-ln²(1-c)`. The positive canonical term in P0 is
`3 exp(-1/4)>9/4`, whereas the pole pressure is less than `21 epsilon`.
Thus `F18-P0 < 21/100000-9/4 <0`.

For the specified switch, write d=3/4-r² near its upper boundary. Its tail
obeys

    eta_rr ~ -3 exp(4-1/d)/d^4 <0.

The remaining rational asymptotic coefficient -3 is computed symbolically;
the exponentially small denominator tends to one. Since eta_qq is a positive
constant multiple of eta_rr, a_UV is negative arbitrarily close to that
boundary on its transition side. At the boundary, Hphysical=sqrt(3/4)>0,
M0=-2X exp(S)Q<0, and
`Rbar >= 2 exp(2wc)(Lambda-9/4)>0`. Continuity supplies expanding,
constraint-regular curved points with the negative UV coefficient. This is
a construction-specific obstruction with stated hypotheses, not a proof
against all MOND, all primordial clocks, or all two-tensor actions.

## 6. Constructive next target: kinetic and curvature terms must be designed together

Simply increasing the trace-free kinetic coefficient T and setting the
curvature coefficient to maintain the tensor cone is not yet a repair.
It can make the curvature coefficient momentum dependent. Let H(S,q,R)
denote that proposed local trace/curvature Hamiltonian, with B>0 and finite
positive `a=T/6+H_qq/2`. Its reduced scalar Hamiltonian has leading terms

    a (delta q)^2 +4 H_qR k² delta q zeta+8 H_RR k^4 zeta²+O(k²).

The leading energy determinant is `4(2a H_RR-H_qR²)k^4`. If H_RR=0
but H_qR!=0 it is negative. Positive energy without an uncancelled k^4
dispersion term therefore requires the compatibility equation

    (H_qq+T/3) H_RR-H_qR²=0.

This condition is derived, not a full-theory verdict. An explicit local
Hessian solution is

    H=-T q²/6+beta(q+ell R)²/2-A0 R,

with T constant with respect to q,R. It gives a=beta/2 and satisfies the
compatibility exactly. The script also checks an uncompleted control whose
leading determinant is negative. This local family is NOT inserted into
IC19 and does not automatically satisfy the tensor cone, scalar k² gradient,
static MOND matching, or cosmological equations. It identifies what the next
global action must actually realize instead of testing only its kinetic rank.

Retain: normalized pole-clock cosmology, the holonomic auxiliary repair,
ordinary matter coupling, and the independently varied exponential static
primitive. Replace: the unstable trace-momentum interpolation, with a complete
kinetic/curvature construction tested against the compatibility above and
against the actual expanding witness. All PPN parameters, Phi/Psi matching,
strong coupling, zero-field limits and empirical galaxy/cluster/cosmology
tests remain obligations of that single replacement action.

The exact programs, commands, input hashes, failed development controls and
strict refusal are recorded in `ic19_run_001/run_index.json`. The mathematical
note and computations received a scoped self-review, not an independent
full-theory audit. This checkpoint preserves progress without claiming that
passing software tests constitutes a completed gravity theory.
