# Independent audit: small acoustic corners

**Verdict: proved as written in the stated ordinary regular-corner class.**
The calculation is a necessary-condition exclusion; it does not prove
that a postbreak BV evolution exists or must contain such a shock.

Reviewed `pf12/SMALL_ACOUSTIC_CORNERS.md`, SHA256
`f92e205e152a2e29d471cf6a2c88df0c62a4f572f584cbf53d3a6b56ec5c2df4`.
Independent delegated audit, 2026-11-06. Also read the dynamic normal
stress bridge in `coupled/time_layer_review/MATCHING_BRIDGE.md`.

At D0=0, h=r0 and R0=u+1/u-1, so the physical high-frequency scalar
speed is c0^2=u/(1-u+u^2). An interface with speed approaching either
acoustic characteristic has proper tangential clock slope
s0=r0/sqrt(1-c0^2). Hence

    epsilon0=gamma s0^2=u(1-u+u^2)/(1-u)^2.

For fixed 0<u<=1/10, this is at most 10/81<1/3. The interface is timelike,
and in its rest frame the limiting clock velocity is the nonzero value
opposite its speed. Thus a sufficiently small neighborhood preserves
nonzero same-sign endpoint velocities, the strict switch margin, and
epsilon<1/3. This neighborhood need not remain uniform as u approaches
zero. The assertion concerns a small acoustic interface family, not an
unproved classification of every possible small discontinuity.

The normal polarization conjugate is B=s A>0: r=s sqrt(1-w^2), and its
factor C Q=Q/sqrt(1-w^2) equals s A. This B is not n beta. With the
stated common tangential traces, the exact partial normal Legendre
function, up to common constants and an affine velocity term, is

    f(w)=([B sqrt(1-w^2)-1-epsilon(1-w^2)]^2
           +epsilon(1-w^2))/(2 gamma).

Direct differentiation independently confirms the displayed identity

    f'''=(3w/gamma)[4epsilon^2+B(1-w^2)^(-5/2)
                 (1-epsilon(3-2w^2)(1-w^2))].

Python3/SymPy simplification of the derivative minus this expression
returned exactly zero. On 0<w<1, (3-2w^2)(1-w^2)<=3, so epsilon<1/3
makes the bracket strictly positive. Therefore f' is strictly convex.
For two distinct positive endpoints with equal f'=j, its graph lies
strictly below the constant chord j. The difference of their normal
Legendre stresses is the nonzero integral of j-f'. It cannot vanish.
Negative endpoints follow by reflection (or strict concavity of f' on
the negative interval). A common affine term shifts j but cancels from
this argument. Equal velocities with the common conjugate and regular
tangential data give equal normal derivatives on the on branch.

The dynamic canonical/Hilbert bridge supplies this normal stress condition
only with the regular identified outer states, native equations and no
surface stress/current assumed in the candidate. The proof does not
automatically transfer it to a rough BV interface with unidentified
currents or a diffuse defect. Nor does PF11's stress nonactivation by
itself prove all those corner regularity assumptions for every future
continuation. No entropy theorem for the constrained nonlocal system is
used or established here.
