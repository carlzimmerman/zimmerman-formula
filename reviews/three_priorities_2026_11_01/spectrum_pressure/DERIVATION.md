# Complete rigid spectrum and conditional pressure, TP01

## Claim and scope

For the specified canonical-K, rigid renormalizable SU(5) action, the
complete *tree* spectrum determines a nonconstant full one-loop threshold
potential along its classical flat valley. At fixed couplings satisfying
g^2=29lambda^2/200, that potential has a universal dimensionless shape.
In the stipulated relative-motion portal, its positive-source radial
matter branch loses positive compressibility well before radial stability.
This is a fixed-order statement, not a complete physical vacuum or halo
exclusion. No coupling is selected by this calculation.

The input action, not a radial RG surrogate, is

    K=|X|^2+Tr(A^dagger A)+Tr(B^dagger B),
    W=fX+(h/2)X Tr A^2+(lambda/2)Tr A^2 B,
    A=i a D, B=bD, D=diag(2,2,2,-3,-3),
    a^2=2fh/(30h^2+lambda^2), b=hX/lambda,
    Vtree=f^2 lambda^2/(30h^2+lambda^2).

All f,h,lambda are positive; X is real nonnegative on the radial slice.
Primary convention/valley checks are recorded by the coordinator in
`../SOURCE_CHECKS.md`. Sources do not supply the matter portal or gravity.

## Full mass assembly and independent controls

Use 24 Hermitian basis matrices Ta with Tr(Ta Tb)=delta_ab; gauge
generators are ta=Ta/sqrt(2). The 49 chiral coordinates are (X,Aa,Ba).
The completely symmetric cubic tensor is

    Y_X,Aa,Ab=h delta_ab,
    Y_Aa,Ab,Bc=lambda Tr[{Ta,Tb}Tc]/2,

with all permutations. With F_i=W_i and M_ij=W_ij, let

    A_H=M^dagger M, B_H,ij=sum_k conjugate(F_k)Y_kij.

In delta z=(q+i p)/sqrt(2), the F Hessian blocks are

    Hqq=Re(A_H+B_H), Hpp=Re(A_H-B_H),
    Hqp=-Im(A_H+B_H), Hpq=Im(A_H-B_H).

For adjoint representation matrices Ra, put w_a=Ra z. On this D-flat
valley the additional D Hessian is L^T L, where
L_a=sqrt(2)g(Re w_a,Im w_a). The 24 vector mass matrix is
2g^2 Re(w_a^dagger w_b). Its spectrum is twelve zeros and twelve equal
25g^2(a^2+b^2). This was checked independently through off-block root
commutators, not inferred from a supertrace.

The full 73-Weyl symmetric mass matrix is

    MF=[[W_ij, J^T],[J,0]], J_ai=sqrt(2)g(z^dagger Ra)_i.

A gaugino phase change does not change its singular masses. Singular
values squared, not eigenvalues of MF itself, are the Weyl mass squares.
The 98-real-scalar Hessian includes twelve null gauge Goldstone directions;
their zero contribution to the potential is retained. Quotienting leaves
86 physical scalar coordinates. Twelve massive plus twelve massless gauge
vectors contribute 60 physical polarizations, matching 146 Weyl degrees.

At X>0 there are fourteen scalar zero eigenvalues (twelve gauge directions
and the complex flat direction) and thirteen zero Weyl eigenvalues
(twelve unbroken gauginos and the Goldstino). At X=0 additional chiral
fermion zeros appear; the diagnostic records 25, rather than silently
applying the generic count there. These light fields have not been
integrated out or given invented masses.

## Exact representation blocks

Let c=f h lambda^2/(30h^2+lambda^2). For the SU(3) adjoint take r=2,
multiplicity8; for SU(2) r=-3,multiplicity3; for the broken root sector
r=-1/2,multiplicity12. In each sector define

    m=(1+r)hX, q=r lambda a, beta=(1+r)c,
    M_chiral=[[m,iq],[iq,0]], B_chiral=diag(beta,0).

The two real scalar 2x2 blocks are

    Hplus=[[m^2+q^2+beta,-mq],[-mq,q^2]],
    Hminus=[[m^2+q^2-beta,mq],[mq,q^2]].

Only for the broken sector add vv^T to Hplus, v=(5ga,-5gb).
That sector's Weyl masses are squares of the eigenvalues of the real
symmetric matrix

    [[m,q,5ga],[q,0,5gb],[5ga,5gb,0]],

obtained by unitary congruence from the complex mass matrix. It has one
massive vector with mass square25g^2(a^2+b^2) per root. The remaining
singlets have four real scalar masses2fh, two scalar zeros, two Weyl
masses2fh and one Weyl zero; their CW contribution cancels exactly.
The twelve unbroken vector multiplets are massless at this tree order.

These independently assembled small blocks match every dense eigenvalue
at X={0,.1,1,3,10}, h=lambda=.6. Maximum absolute discrepancy1.43e-13;
50-digit slow and analytic-block eigensystems agree to better than1e-35.

There is also a direct tree-positivity argument. In the unbroken sectors,
the scalar determinants are q^2(q^2+beta) and q^2(q^2-beta), with positive
traces. For r=2 the factors q^2+beta,q^2-beta are 11c,5c; for r=-3 they
are 16c,20c. Both scalar blocks are positive definite at every finite X.
In the broken sector beta=q^2 and mL+qR=0, with L=5ga,R=5gb. Hminus
has determinant zero and positive trace; Hplus has positive trace and

    det(Hplus)=2q^4+q^2 L^2+(m^2+4q^2)R^2>0.

Thus all physical transverse scalar modes of this rigid tree valley are
positive for finite X and positive f,h,lambda. The flat singlet directions
and gauge Goldstones remain zero, as already counted. This exact tree
statement does not establish loop-corrected transverse stability.

## Complete one-loop potential and exact cancellation

In the stipulated Landau-gauge supersymmetric DR-bar-prime convention,

    CW=[sum_s H(ms^2)-2sum_f H(mf^2)+3sum_v H(mv^2)]/(64pi^2),
    H(x)=x^2[ln(x/Q^2)-3/2], Q=1 in the numerical units.

Massless modes contribute zero; negative physical scalar masses would
invalidate a real stable CW interpretation. No resolved negative masses
occur in the frozen finite grid. The exact block traces give

    STr M^2=0,
    STr M^4=6 f^2 h^2 lambda^2(29lambda^2-200g^2)
                                  /(30h^2+lambda^2)^2.

Both are independent of X. At g^2=29lambda^2/200 the second supertrace
vanishes. Thus the one-loop explicit Q dependence cancels along this
valley; the *finite threshold potential does not vanish*. This is neither
all-order protection nor a statement that individual sectors cancel.

At that critical coupling set z=hX/sqrt(c). Every noncanceling sector
mass square is c times a universal dimensionless function of z:
q^2/c=2r^2, m/sqrt(c)=(1+r)z,
(5ga)^2/c=29/4 and (5gb)^2/c=29z^2/8 in the broken block.
STr M^4=0 also cancels the log c term. Therefore

    CW=c^2 F(z).

The numerical dimensionless minimum is z_min=7.367143721278508... .
No claim of an exhaustive global minimum proof or exact transcendental
root certificate is made. The universality of the shape is algebraic;
the reported root is numerical.

The relation g^2=29lambda^2/200 is an inherited comparator from MV28.
It is not newly selected by minimizing the full threshold potential.
At finite thresholds a stationary X and its running/matching data must
be solved together, not assumed to fix g by the leading-log equation.

## Canonical field dictionary and radiative shape

The microscopic flat coordinate is the complex canonical
T=sqrt(30h^2+lambda^2)X/lambda. If s=ln(X/v), then on the fixed-phase
slice its kinetic term is

    |T_v|^2 exp(2s)(partial s)^2.

It is not the constant-kinetic canonical-s toy used in VR28's isolated
scalar-loop test. That test's exp(6s) counterterm cannot be imported as
a compulsory microscopic operator. Here the complete one-loop divergent
supertrace is X-independent and zero at the comparator, while the finite
full threshold shape is computed explicitly. This rules out that particular
one-loop import, not all higher-loop operators or unknown Kahler effects.

## Conditional matter pressure and local gaps

Keep the *assumed* relative-motion portal exp(2s), waterbag K=k rho^(5/3)
and local radial elimination. Then

    W=K exp(-2s)+U, U=Vtree+CW,
    K exp(-2s)=U_s/2,
    P_total=U_s/3-U,
    dP/dlnrho=5U_s(U_ss-3U_s)/[9(2U_s+U_ss)].

Only U_s>0 admits positive K. A stationary local radial minimum also
requires W_ss=2U_s+U_ss>0; compressibility requires U_ss>3U_s.
Pressure was independently differentiated against
rho proportional to[U_s exp(2s)/2]^(3/5), retaining scalar pressure.

At h=lambda=.6,f=1 the direct60-digit derivatives give

    Xmin=1.708215547106076...,
    Xpressure=2.011081499325548...,
    Xpressure/Xmin=1.177299611124933...,
    Xradial_end/Xmin=1.853361810233188... .

At the pressure boundary W_ss=5U_s>0. This ratio repeats for all nine
coupling choices because the one-loop shape scales as above. No logotropic
dense-core continuation is supplied by this branch.

The conditional density reach can be stated without choosing a phase
level. Define the old comparison scale rho_*=(3Bcurv/(2k))^(3/5),
Bcurv=Uss(Xmin)/9, and s=ln(X/Xmin). Stationarity gives exactly

    rho/rho_*=[U_s exp(2s)/(3Bcurv)]^(3/5),
    dlnrho/ds=3(2U_s+U_ss)/(5U_s).

Hence density increases along any connected positive-source radially
stable branch. Thirty-three interior states through the pressure boundary
have positive U_s and W_ss and increasing density. The boundary value is
rho/rho_*=0.59081176620322665... . In this conditional fixed-order
dictionary, positive compressibility fails below the old comparison scale,
before a rho much larger than rho_* dense-log regime is reached. This is
not a prediction of an absolute density: k cancels from the comparison,
and Bcurv is not proved to be an asymptotic log-pressure coefficient here.

For example at X/Xmin=1.2,
U_s=1.14771977e-7, W_ss=4.97024746e-7 and
dP/dlnrho=-9.85701068e-9. The smallest positive physical tree transverse
scalar mass square is1.08075416e-3. The canonical radial matter mass square
is W_ss/(2|T|^2)=1.90782480e-9, only1.77e-6 of that gap. Five samples
in1.05..1.5 have similarly separated radial and transverse tree scales.
This supports the declared local radial approximation on slowly varying
states; it does not establish a halo-gradient bound or all-mode quantum
stability. The R phase, Goldstino and unbroken gauge fields remain light.
The phase-constant, zero angular-current ansatz is a restriction, not a
derived universal material state.

## Accuracy: the old coupling grid is not a controlled final vacuum

The fixed-coupling one-loop finite minimum and pressure obstruction are
well resolved numerically. However the earlier common-threshold leading-log
two-loop curvature divided by the new one-loop threshold curvature is

| h=lambda | ratio of old LL curvature to new threshold curvature |
|---:|---:|
| .03 | .00781984 |
| .1 | .0868871 |
| .3 | .781984 |
| .6 | 3.12794 |
| 1 | 8.68871 |

This is an omitted-order *diagnostic*, not a rigorous error bound. It
precludes calling the old .3..1 grid's fixed-order minimum a robust physical
vacuum prediction. Scaling the equal couplings down suppresses that known
correction relative to the finite threshold contribution, but no complete
two-loop calculation, uniform correction bound, running Kahler metric or
nonperturbative infrared matching has been established here.

The remaining implication is a consistently RG-improved/matched threshold
effective action and its matter coupling, including the light sectors and
quantum transverse modes. The present action still has no selected UV
couplings, no derived portal, no specified total supergravity vacuum offset
and no observational acceleration dictionary derived from those data.
