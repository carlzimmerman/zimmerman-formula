# MV28 model, spectrum, and dictionaries

The microscopic trial is the known Shih O'Raifeartaigh model, with canonical
Kahler potential and

    W=fX+lambda X phi1 phi2+m1 phi1 phi3+(m2/2)phi2^2.

All displayed couplings are real positive. At phi_i=0 the tree energy is
f^2. The radial pseudomodulus X is lifted by the specified massive spectrum;
this model has a runaway elsewhere, so a local minimum is metastable.
The phase of X is an R-Goldstone mode at a nonzero minimum. No lifetime or
phase-mode coupling is calculated in this checkpoint.

## Spectrum derived from the superpotential

Set x=lambda |X|/m1, r=m2/m1, y=lambda f/(m1 m2), d=yr. In units m1,

    M=[[0,x,1],[x,r,0],[1,0,0]],
    N=[[0,1,0],[1,0,0],[0,0,0]],
    A_F=M^2,     A_+=M^2+dN,     A_-=M^2-dN.

The three Weyl fermions have squared masses eigen(A_F). The six real
massive scalars have squared masses eigen(A_+) and eigen(A_-). These
blocks follow by expanding sum_i |W_i|^2 into real and imaginary scalar
perturbations, including the off-diagonal F_X W_Xij term.

Their determinants are r^2(1-y^2-2xy) and r^2(1-y^2+2xy).
The Schur complement in the third diagonal element shows both blocks
are positive definite precisely when 0<=x<(1-y^2)/(2y) for 0<y<1.
This is a check on the entire tree transverse spectrum, not the radial
one-loop stability. The fermion determinant is det M=-r, independent of x.

With Q=m1 and h(t)=t^2[ln(t)-3/2], modified-minimal-subtraction gives

    c(x;r,y)=[Tr h(A_+)+Tr h(A_-)-2Tr h(A_F)]/(64pi^2 y^2r^2),
    U_rigid=f^2[1+lambda^2 c(x;r,y)].                         (1)

The factor two counts Weyl spin degrees of freedom. Direct matrix algebra
gives STr A^2=4y^2r^2, independent of x. Changing Q therefore shifts c by
an x-independent constant; the radial minimum/curvature do not change at
this order. The vacuum value still requires a renormalized parameter and
matching convention. A rigid calculation cannot fix a gravitational offset.

At a nonzero radial minimum x0, identify s=ln(x/x0) and *try* the
R-invariant relative-motion portal Z=(x/x0)^2. This portal is an extra
model assumption; W alone does not generate the PN28 stream action.
At fixed r,y the leading result is

    B_curv/f^2=lambda^2 x0^2 c''(x0)/9,
    B_curv/U_rigid(x0)=lambda^2 x0^2 c''(x0)
                         /[9(1+lambda^2 c(x0))].             (2)

Unlike assigning B or a scaling exponent, the function c and x0 come from
the declared spectrum. Lambda, r and y remain microscopic inputs. No
coupling is selected by comparison to the old acceleration target.
The radial kinetic coefficient is field dependent in s: for canonical
complex X it is |X0|^2 exp(2s)(grad s)^2. Its positivity is manifest, but
it is not the constant scalar kinetic term of PN28.

## A controlled gravity test, with its limitations

Use the explicitly specified N=1 supergravity *effective* model with the
same W and K, no D terms, no additional sectors, and no constant W0 at the
matching scale. With reduced Planck mass M_P,

    U_SUGRA=exp(K/M_P^2)
      [K^(i jbar) D_i W D_jbar Wbar-3|W|^2/M_P^2],
    D_i W=W_i+K_i W/M_P^2.                                  (3)

At phi=0 and W=fX, put a=|X|^2/M_P^2. The full classical potential is

    U_tree=f^2 exp(a)(1-a+a^2)
          =f^2[1+a^2/2+O(a^3)].                             (4)

Thus the specified tree vacuum energy is positive f^2 at small X/M_P;
there is no order-a mass term for exactly canonical K. Adding the flat
one-loop expression (1) is only the leading weak-gravity approximation,
not an exact supergravity loop calculation. Curvature-dependent and
Planck-suppressed loop terms have not been computed.

The declared R symmetry forbids W0 if it remains exact in the matching
theory. This assumption is stronger than internal symmetry in the earlier
ordinary scalar action: a bare cosmological term alone is not a locally
supersymmetric invariant. We do not establish an anomaly-free exact R
symmetry of quantum gravity or a microscopic gravitational UV completion.
Calling (1) the measured full cosmological vacuum energy would exceed this
calculation's scope.

For an allowed R-preserving Kahler correction
K=t+c_K t^2/(4M_P^2), t=|X|^2, the exact valley potential is

    U/f^2=exp(a+c_K a^2/4)
      [(1+a+c_K a^2/2)^2/(1+c_K a)-3a]
           =1-c_K a+O(a^2).                                 (5)

The unknown coefficient thus adds a radial mass of order f^2/M_P^2.
It is small relative to the computed radiative mass only with an explicit
hierarchy and bounded Wilson coefficients. Such bounds are additional UV
assumptions. If R symmetry is broken, W0 is allowed and changes the energy
by approximately -3|W0|^2/M_P^2, with a tadpole as well. Formula (3), not
an arbitrary constant added to (1), must be used to test that change.

## Actual pressure response of the trial portal

For K=k rho^(5/3), use W_local=K exp(-2s)+U(s). Let U_s>0 on the
matter-displaced branch. Its stationary point has E_rel=U_s/2. The radial
stability and compressibility are different conditions:

    W_ss=2U_s+U_ss,
    dP_total/dln rho=5U_s(U_ss-3U_s)/[9(2U_s+U_ss)].          (6)

This follows from P=U_s/3-U and
dln rho/ds=(3/5)(2+U_ss/U_s). On a radially stable branch the pressure
response is positive only if U_ss>3U_s. In x variables this is
x c''>2c'. The compressibility can change sign while W_ss remains
strictly positive: at the sign boundary W_ss=5U_s>0.

A potential approaching A ln x has U_s->A and U_ss->0, giving the
negative limit -5A/6 in (6). The numerical spectrum calculation will test
whether this obstruction appears before the transverse tachyon boundary
in the specified finite cases. No logarithmic halo pressure or successful
observational fit is assumed from a small vacuum stiffness alone.
