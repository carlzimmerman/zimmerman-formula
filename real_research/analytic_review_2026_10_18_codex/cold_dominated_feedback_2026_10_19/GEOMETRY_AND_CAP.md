# Actual cold-dominated members and cap resonance geometry

Checkpoint ZAR-2026-10-19-11-CX. Analytic derivation by `/root`.
The sources are the exact smooth inverse, the exact finite-halo profile, and
`../actual_feedback_2026_10_19/GEOMETRY_AND_SCALING.md`, especially its exact
epicyclic twist identity. This file makes no assumption that susceptibility is
small. Quantities below are dimensionless unless physical units are displayed.

## 1. A nonempty family in the requested mass regime

Put `r_M=sqrt(G M_b/a_0)`, choose `f=1/64`, and set

    ell=D r_M,   (r_0,r_1,r_2,R)=ell(1,2,3,4),
    M(ell x)=A ell p(x),   A=M_b/r_M.

Here `p` is exactly the original profile: `p=x S(x-1)` on `(1,2)`,
`p=x` on `[2,3]`, and `p=3+integral_3^x[1-S(u-3)]du` on `[3,4]`.
Inside the hollow core it is zero and outside the halo it is constant.
Thus `M/M_b=D x` throughout the law annulus. The cold-to-baryon mass ratio
there can be arbitrarily large. The deep-cubic and circular-core conditions
hold for sufficiently large `D`: their dimensionless small ratios are
`f/D` and `2f^2/((1-f)D)`.

In frequency units `(G M_b/ell^3)^(1/2)`, write

    B=x^2 p''-x p'-3p,
    C=2(p')^2+2p p''-10p p'/x+5p^2/x^2.

Direct differentiation of the actual circular forces gives

    (kappa_f^2)'=x^-4[-3+D B],
    (kappa_t^2)'=x^-4[-3+(1-f)D B-f^2 C].                 (1)

The previous analytic derivative bounds give `C>=-2858`. Therefore
`3+f^2 C>2`. Also `B<=0` outside the inner taper, `B(1)=0`, `B(2)=-8`,
and `B(3/2)=3/2`: at the midpoint `S=1/2`, `S'=2`, `S''=0`.
Consequently every zero in (1) belongs to the open set `B>0` in `(1,2)`.

On that open set define the real analytic functions

    D_f(x)=3/B(x),
    D_t(x)=(3+f^2 C(x))/((1-f)B(x)).                      (2)

Neither is constant on an interval. Indeed an analytic identity asserting
constancy extends to the entire inner taper and contradicts the limit at
`x=1`, where `B,C` tend to zero while the numerator tends to three.
For any compact positive interval of possible `D`, the inverse images under
(2) lie in a compact subset of `(1,2)` on which `B` is bounded below by a
positive constant. The zeros of each analytic derivative there are finite.
Hence the union `E` of their critical values is locally finite in `(0,infinity)`.

For every `D` outside `E`, both circular frequencies have only finitely many
stationary points, all nondegenerate. There are arbitrarily large such `D`:
every interval `(D_0,D_0+1)` contains points outside the finite exceptional set
in its closure. This is a theorem for an explicitly described nonempty
parameter family, not a certificate for a particular unprovided numerical
halo. No exceptional value has been excluded by a numerical computation.

## 2. No full action critical points at sufficiently small fixed warmth

Use the circular radius `s` as a coordinate for squared angular momentum,
`L=L_c(s)`, and the ordinary radial action `J>=0`. Write
`Omega(0,s)=kappa(s)`. The exact twist formula at a stationary circular
frequency is

    partial_J Omega(0,s_c)=kappa''(s_c)/(4 kappa(s_c)).   (3)

Every zero of `partial_s Omega(0,s)=kappa'(s)` is simple by Section 1,
and (3) is nonzero at each such zero. Elsewhere the tangential derivative
itself is nonzero. Compactness of the closed circular interval therefore
gives `|grad_(J,s) Omega|>=c>0` on a sufficiently narrow closed tube.

The exact inverse has cap `E-E_c(s)=delta^2 kappa(s)^2 h(s)^2`, where
`h(s)=(s-r_0)^2(R-s)^2/(R-r_0)^3`. The action of that cap satisfies

    J_b(s)=delta^2 kappa(s) h(s)^2+O_Cm(delta^4)          (4)

for every fixed finite `m`. This follows by the smooth local action-energy
inverse, `J=(E-E_c)/kappa+O((E-E_c)^2)`. All coefficients extend smoothly to
the radial endpoints. Choose `delta>0` once, sufficiently small for this
geometry and for the exact density inverse and its positivity. It stays
strictly positive and is not a cold-limit assertion.

The resulting actual occupied action domains have no eccentric full-frequency
critical point. The derivative `partial_L Omega` is allowed to vanish; the
stronger monotonicity assumption in the earlier small-mass proof is unnecessary.

## 3. Eccentric cap resonances are approached from the occupied interior

Let `g_delta(s)=Omega(J_b(s),s)` be the cap frequency. From (4),
`g_delta=kappa+O_C2(delta^2)`. Its stationary points are unique small
perturbations `s_delta` of the finitely many `s_c`, and

    sign g_delta''(s_delta)
      =sign partial_J Omega(J_b(s_delta),s_delta)
      =sign kappa''(s_c).                              (5)

At a cap point with `g_delta'!=0`, the frequency level crosses the cap
transversely and enters the occupied region. At a stationary cap point use
coordinates `x=s-s_delta`, `z=J-J_b(s)<=0`. By (5),

    Omega-Omega_cap=a_delta z+(b_delta/2)x^2
                    +O(|x|^3+|x z|+z^2),
    a_delta b_delta>0.

The implicit frequency level is
`z=-(b_delta/(2a_delta))x^2+O(|x|^3)<0` for small nonzero `x`.
It too enters the occupied region. In particular a cap point is never an
isolated receiving resonance for these members.

For an actual energy eigenmode, its radial field is `C^(1,1/2)` and its
eccentric receiving coefficient is `C^1` in `(J,s)`. Weighted energy forces
that coefficient to vanish at all positive-weight regular interior resonances.
The preceding geometry extends this zero to every eccentric cap resonance.
Moreover the coefficient is locally bounded by a constant times the frequency
detuning on the occupied side. At a transverse crossing this follows from a
smooth coordinate straightening both crossing curves; at a stationary cap
point the entire nearby frequency graph just constructed lies on the occupied
side, so division along the nonzero `J` derivative gives the assertion.
Thus the modal work is bounded locally at every eccentric cap receiver.
This conclusion uses the actual geometry and eigenmode equation, rather than
the invalid inference that a flat weight itself forces a boundary trace zero.

## 4. The physical radial endpoints are also controlled for energy modes

Let `h_i` be any finite-energy accessible perturbation, and write
`chi_i(r)=C_Gamma integral w_i(r,v,L)dv dL`. The exact susceptibility is a
smooth nonnegative physical function, zero outside the hollow shell.
Its velocity integral is smooth and flat at `r_0,R`. For every integer `N`,
Cauchy--Schwarz and the zero total perturbation mass give

    |m_i(r)| <= ||h_i||_A (integral_edge^r chi_i(s)ds)^(1/2)
              <= C_N ||h_i||_A d(r)^N,                 (6)

where the integral is taken from the nearer endpoint, with the orientation
reversed at `R`, and `d(r)` is its distance. Since the actual `H(r)` is smooth
on the closed shell, `phi'=-H m` has the same bounds. Subtracting a constant
on a receiving orbit therefore bounds every nonzero field harmonic by
`C_N ||h||_A d^N` when its circular center approaches an endpoint. Its entire
radial range is within comparable endpoint distance, by the intrinsic tube
construction (`|r-s|<=C delta h(s)=O(d^2)`).

Both circular-frequency derivatives are strictly negative at the physical
endpoints by (1): their inner numerator is `-3`, and their outer numerators
are strictly negative. If `nu=k kappa(edge)`, then for receivers approaching
that endpoint

    |k Omega(J,s)-nu| >= c |s-edge|,

because `J<=J_b(s)=O(d^4)` and the circular derivative is nonzero. Equation
(6) absorbs this denominator. If `nu` is different from the endpoint frequency,
the denominator stays separated from zero. Only finitely many harmonics can
resonate for a fixed mode frequency; the nonresonant tail is summable by the
usual `C^(1,1/2)` field bound. Thus physical endpoint accumulation introduces
no additional unbounded modal work.

## 5. What remains

The cap and the physical endpoints are controlled mode by mode for the actual
cold-dominated family above. A nondegenerate circular extremum inside the shell
is a different boundary threshold. There the same-sign normal form is

    Omega-kappa(s_c)=a J+b(s-s_c)^2+higher terms,
    a b>0.

The first radial harmonic of a differentiable field starts at a constant times
`phi'(s_c) sqrt(J)`. Weighted energy allows this term although its quotient by
the detuning need not be bounded. Neither the cap proof nor Section 4 removes
this interior circular force trace. An actual inverse and this threshold
condition must be checked in the separate operator/mode proofs; no absence of
such modes is asserted here.
