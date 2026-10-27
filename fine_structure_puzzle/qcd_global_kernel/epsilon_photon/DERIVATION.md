# Nonconstant photons around a compact charged orientation on S4

FSP-008 continuation, 2026-10-19. This lane adds the first nonconstant
PHOTON correction to the compact LO SU(2) orientation. It preserves the
previous pion calculation and does not claim a complete NLO partition.

## 1. Scope and first principles

Use U=U0 exp(i tau.pi/F), integral sqrt(g) pi=0, U0=a0+i a.tau,
a0²+|a|²=1, Q=I/6+tau3/2, s=a1²+a2². Let u=e², V=kappa H^-4,
kappa=8pi²/3, R=12H². Epsilon counting is H~epsilon,
pi,A~epsilon, M²,u~epsilon⁴, x=F²M²V and y=uCV of order one.
The nonconstant pion kinetic operator is massless at this order. The
sources M,F,C and renormalized curvature constants are unfitted inputs.

The Euclidean gauged kinetic action is

    S=∫sqrt(g)[F²/4 Tr(DU DUdag)+1/4 Fmunu Fmunu],
    DU=∇U-i e A[Q,U].                                    (1)

Set B=[Q,U0], b.tau=U0dag B=U0dag Q U0-Q. Direct Pauli algebra gives

    |b|²=s,     Tr B Bdag=2s,
    S_quad=1/2∫sqrt(g)[(∇pi_i-eF b_i A)²]
               +1/2∫sqrt(g) A Delta1 A + S_gf.           (2)

Delta1=-∇²+Ric is the Hodge operator in transverse Maxwell gauge.
Thus the seagull and derivative mixing are respectively

    S_AA=(uF²s/2)∫sqrt(g) A²,
    S_Api=-eF b_i∫sqrt(g) A·∇pi_i.                       (3)

The field-strength action alone is meant by Delta1 on the transverse
subspace. Longitudinal dynamics in (2) is specified by gauge fixing,
not by assigning it the transverse Hodge kinetic energy.

## 2. Gauge cancellation, ghosts and the collective mode

For gauge fixing (∇·A)²/(2alpha_g), write A=A_T+∇phi. On closed S4,

    ∫sqrt(g) A_T·∇pi=-∫sqrt(g) pi ∇·A_T=0.               (4)

This is an exact integration-by-parts identity; it does not drop a
nonzero transverse mixing diagram by power counting. To check that
keeping the transverse seagull is gauge complete at this order, take
each NONCONSTANT scalar harmonic with eigenvalue lambda>0. Normalize
its longitudinal vector as ∇Y/sqrt(lambda), and rotate the pion basis
so the first pion is along b. With mA=eF sqrt(s), the longitudinal
photon/pion quadratic block is

    K=[[lambda/alpha_g+mA², -mA sqrt(lambda)],
       [-mA sqrt(lambda), lambda]],
    det K=lambda²/alpha_g.                               (5)

It is independent of mA. In perturbation theory its longitudinal
seagull +alpha_g mA²/(2lambda) is canceled by the two-mixing-insertion
term -alpha_g mA²/(2lambda). This exact Gaussian cancellation is also
valid when b=0 by continuity. In Landau gauge the longitudinal field is
constrained to zero and (4) implements the same result directly.
Mass/source insertions into the nonconstant pion propagator change this
cancellation at higher epsilon order and are not silently omitted from
an all-orders claim. Other nonlinear photon/pion vertices first enter
the source correction beyond the retained epsilon² order.

The Abelian Faddeev--Popov operator is Delta0=-∇², independent of U0.
Its constant ghost is excluded. The scalar/pi constant mode is likewise
absent from (5), because it belongs to U0. S4 has no harmonic one-form;
there is no Maxwell vector zero mode to delete or replace by a mass.

Local Landau gauge leaves GLOBAL U(1). It rotates (a1,a2), so s and
the LO source potential are invariant. In normalized Haar coordinates,
dU=ds dphi dpsi/(4pi²); removing the global psi gauge angle with its
Faddeev--Popov Jacobian leaves the same pushforward ds dphi measure up
to a source-independent normalization. For example a2=0,a1>0 has
Jacobian |a1|, which cancels delta(a2)'s 1/|a1| on 0<s<1. It does
not produce an extra 1/sqrt(s) weight. The s=0 stabilizer needs a
coordinate patch/limiting prescription; it has zero Haar measure and
does not license deleting compact configurations. The meson-sector
period convention and the full microscopic global gauge-group choice
remain part of the normalization, not predictions of charge.

The full gauge volume is divided out ONCE. The primary sphere gauge
sources explicitly supply the missing constant-group factor and ghost
prime. In the unscaled connection convention their free Maxwell factor
is proportional to

    N_gamma=[det' Delta0]^(1/2)
             /[2pi sqrt(V) det_T(Delta1/(2pi u))^(1/2)].  (6)

This formula specifies why retaining a seagull in an arbitrary gauge
would be insufficient. Canonical A rescales the nonconstant measure;
the resulting coupling/global normalization must remain consistent
with (6). Its free-coupling logarithm is not an analytic insertion at
u=0. This lane computes the orientation-dependent ratio at the SAME
u, where (6), the ghosts and the global factor cancel. Absolute metric
or charge response also requires N_gamma, its curvature renormalization
and source-only contacts. We do not call the ratio alone that response.

## 3. The transverse tadpole is calculated

The primary vector spectrum, with the Ricci shift added, is

    lambda_l=H²(l+1)(l+2),
    d_l=l(l+3)(2l+3)/2,     l=1,2,... .                  (7)

Both independent gauge sources display the rough-vector spectrum and
Ricci shift; this agrees with Kluth--Litim Table 4. In particular the
lowest Hodge eigenvalue is 6H² with degeneracy 10. Define

    zeta_T(p)=Σ_(l>=1) d_l/[(l+1)(l+2)]^p,
    T_gamma,zeta=H²/kappa FP_(eps=0)
                        (mu²/H²)^eps zeta_T(1+eps).      (8)

T_gamma is the coincident TRACE over transverse photon components.
Its multiplicity is already in d_l; no additional factor 3 or 4 occurs.
With n=l+3/2, A=5/2, c=1/4, a=9/4, the exact continuation is

    zeta_T(p)=Σ_(k>=0) (p)_k c^k/k!
       [zeta_H(2p+2k-3,A)-a zeta_H(2p+2k-1,A)].         (9)

Only k=0,1 have a pole at p=1. Their residue is (c-a)/2=-1.
The finite regular tail combines into

    FP zeta_T(1)=zeta_H(-1,A)+c/2+psi(A-1/2)+psi(A+1/2)
                =2/3-2 EulerGamma.                      (10)

The same spectrum has the directly derived early-time heat trace

    K_T(t)=1/(2t²)-1/t+19/30-5t/63-11t²/630+... .        (11)

Thus the curvature pole and the defined zeta finite part are

    T_gamma,pole=-H²/(kappa eps)=-R/(32pi² eps),
    T_gamma,zeta=H²/kappa[-log(mu²/H²)+2/3-2gamma].       (12)

A negative renormalized coincident tadpole is compatible with positive
unsubtracted modes; the quadratic and logarithmic UV subtractions are
not positive spectral weights. Equation (12) is a specified UV scheme,
not a measured finite-volume constant. The independent heat-integral
check includes 1/Gamma(p) in continuing (8), so it retains the finite
EulerGamma term that would be missed by a pole-only argument.

## 4. A matched photon-only curvature residue

At first order in u the remaining transverse determinant is

    delta W_gamma(U0)=uF² V T_gamma s/2 = t_gamma s.      (13)

The curvature operator in the inherited explicit-e convention is
uF² k15 R Tr(Q U Q Udag)=uF² k15 R(5/9-s). Its orientation
part is -uF² k15 RV s. The tadpole divergence in (13) is

    delta W_gamma,pole=-uF² RV s/(64pi² eps).             (14)

It is canceled by delta k15=-1/(64pi² eps). In the standard bare
convention k15=k15^r+beta15 L, L_pole=1/[16pi²(d-4)],
d=4-2eps, this is EXACTLY beta15,photon=1/2. It agrees with the
photon-only constant in Kubis--Meissner (4.8), independently of the
unresolved pion-loop Z=C/F⁴ part. The factor-two dimensional convention
is explicit. This comparison concerns the invariant s residue and does
not solve the earlier off-shell/EOM-basis question for the pion piece.

In the common zeta finite prescription the renormalized orientation
coefficient, including a curvature LEC in that SAME scheme, is

    t(H,u)=uF²/(2H²) B(H),
    B=-log(mu²/H²)+2/3-2gamma-64pi² k15,zeta^r(mu).       (15)

The photon-only running mu d k15^r/dmu=-1/(32pi²) cancels the
explicit mu derivative of (15). The usual finite dimensional/MSbar
coefficient and k15,zeta require a finite scheme conversion; their
finite numerical values are NOT identified. The k15 c-number 5/9 term
also requires a pion-independent R times EM-source contact: otherwise
the same counterterm would leave an uncanceled constant pole. Its finite
part is independent matching data. Both it and the absolute Maxwell
normalization remain outside the orientation ratio. They cannot be
removed by fitting alpha or by declaring this complete NLO QCD+QED.

## 5. New compact-source and metric derivatives

Use the INHERITED compact integral Z(x,y) with weight exp(x a0-y s).
Write q=<s>, c=Cov(a0,s), v=Var(s), K_ass=<delta a0 delta s²>,
K_sss=<delta s³>. It is not re-sampled as a purported new result here.
Equations (3)--(5) give the first photon correction

    Z_compact+gamma=N_gamma * [Z(x,y)-t Z(x,y)q]+...,
    delta W_gamma=t q.                                  (16)

Equivalently this is the FIRST-ORDER y->y+t shift, with t=O(epsilon²).
It is not a permission to resum (15) to finite large charge. It adds a
new nonconstant-photon contribution to the previous nonconstant-pion
contraction. There is no double counting of a free photon determinant:
at the aligned constant U0=1, s=0 and the selected photon mass is zero.

Take D=V partial_V=-H partial_H/4 at FIXED M,F,C,u,mu,k15. Then

    Dq=x c-y v,     q_y=-v,
    tdot=Dt=t/2-uF²/(4H²),     h=t_u=t/u,
    hdot=Dh=h/2-F²/(4H²).                               (17)

The u=0 notation t/u means the analytic coefficient h, not a division
by a numerically zero input. The selected physical-source derivatives
are

    delta rho_gamma=[tdot q+t(x c-y v)]/V,
    partial_u delta rho_gamma
       =[hdot q+h(x c-y v)]/V
          -C[(tdot+t)v+t(x K_ass-y K_sss)],
    partial_alpha=4pi partial_u.                         (18)

The second terms differentiate the Haar distribution and are required.
The run checks (18) by differentiating t(V,u)q(aV,CuV) independently
as a function before translating its derivatives to cumulants. The
uncomputed source-only contact and the free N_gamma response must be
added for an absolute sphere energy. A charge difference of (16) also
does not automatically cancel a general H,u-dependent matching term.

## 6. Validity and remaining work

This contribution is controlled only at the stated epsilon order,
H<<Lambda_chi, F/H large and uF²/H² small, with x,y of order one.
There is no justified fixed-positive-physical-mass H->0 extrapolation
of the epsilon truncation. The bare compact/PION correction, photon
orientation correction, gauge normalization and all local terms still
have to be assembled in a common regulator and matching basis. The
photon beta residue is now verified; the pion-Z translation remains
unresolved and is not repaired by accepting that separate result.

The code executes exact Pauli algebra, gauge-block cancellation,
independent heat/spectral finite-part checks, tail estimates and exact
metric/source differentiation. Numerical checks are not certified
interval bounds. No old Haar grid, fitted physical LEC, empirical alpha,
proton mass or cosmic target enters. Full A_rho, R(alpha) and alpha
remain uncalculated.
