# IC15: dust response and a separate pure-source auxiliary repair

2026-09-08. **Constructive root repair on the two pure-source axes; full
theory OPEN.** This continues IC14's retained-clock construction, motivated
by Carl's retained-clock hypothesis. It does not replace IC14's action or
attribute the following new potential to Carl.

## Dust and radiation must be varied with their actual couplings

For `g=z gtilde`, a massive particle has action

    -m integral ds_g = -m integral sqrt(z) ds_gtilde.

Let a conserved particle current define the Einstein-frame proper number
density `ntilde`. The physical number density is `n_g=z^(-3/2) ntilde`.
Since `sqrt(-g)=z² sqrt(-gtilde)`, a dust-current action, including its
current-conservation constraints, has the Einstein-frame matter term

    Ldust=-b sqrt(z),    b=m ntilde.

For comoving homogeneous dust, `b a_tilde³` is conserved. It is held fixed
when varying the auxiliary field at fixed Einstein metric and number
current; it is not a canonical scalar kinetic argument. Setting the on-shell
physical dust pressure to zero before varying would erase this coupling.

For conformally invariant radiation the corresponding density scales as
`rho_g proportional to n_g^(4/3)`. Thus `z² rho_g` is independent of z.
Equivalently, the Einstein-frame Hamiltonian of a massless particle is
`sqrt(h_tilde^{ij}p_i p_j)`, whereas for a massive particle it is
`sqrt(h_tilde^{ij}p_i p_j+m²z)`. Radiation has no algebraic auxiliary source
in this restriction; it still gravitates. Radiation cosmology and activation
are not computed in this note.

## The IC14 square potential has a dust continuation fold

Write `q(X)=z0(X)` and retain the IC14 functions F and q. For

    L=F-(z-q)²/(2t)-b sqrt(z),    t=1/10,

the algebraic equation and its curvature are

    L_z=-(z-q)/t-b/(2sqrt(z))=0,
    L_zz=-1/t+b/(4z^(3/2)).

The original vacuum branch has `z=q`. The positive dust-root fold is

    zfold=q/3,    bcrit=4 q^(3/2)/(3sqrt(3)t).

This follows either by solving both equations or by maximizing
`b(z)=2sqrt(z)(q-z)/t` for `0<z<q`. The third z derivative of L is
nonzero there. No such positive root remains for `b>bcrit` in this
fixed-X square-potential continuation.

This is not automatically a canonical constraint-rank failure. For the
clock velocity `v=sqrt(2X)`, and a resting dust current, define

    M=L_X+2X L_XX,    c=sqrt(2X)L_Xz,
    Acan,z=L_zz-c²/M.

Resting particles have no mixed auxiliary/particle-velocity derivative,
so their momenta add no correction to this expression on this background.
If canonical scalar matter is present as well, the code includes its bare
kinetic entry z and mixed derivative `sqrt(2Y)` in the same Schur complement.
The computed auxiliary Poisson-bracket block is `[[0,A],[-A,0]]`.

At `S=.1`, the square fold has

| Quantity | Value |
| --- | ---: |
| zfold | .3116204544571602 |
| bcrit | 6.958232342963977 |
| bare clock M | -1.678618789245093 |
| clock gradient L_X | -2.072686566496437 |
| Acan,z | 21.49945725790790 |

The auxiliary block has computed rank two, while the reduced clock momentum
Hessian vanishes at the fold. The clock is already unhealthy here. Moreover,
the inherited chart requires `exp(-S)<z<1`; at `S=.1` it ends on the square
dust branch at `b=.571193204855`, well before this fold. These are formal
continuation controls, not evidence for a physical fold inside that chart.

More generally, if M is positive and c is nonzero at a raw velocity fold,
then `Acan,z=-c²/M<0`, so a healthy bare clock keeps this auxiliary block
nondegenerate. A divergent velocity-eliminated kinetic coefficient must not
be reported as a loss of canonical rank.

## A rational potential repairs both pure-source root problems

The separate proposal is

    V(z,q)=(z²/2+q³/z-3q²/2)/(3t),
    L=F-V(z,q)+zY-b sqrt(z),    z>0.

It uses the same constant t and obeys

    V(q,q)=0,    V_z(q,q)=0,    V_zz(q,q)=1/t.

Thus it preserves the original vacuum root, pressure, eliminated clock
derivatives, and the IC14 vacuum auxiliary curvature. It adds a barrier as
z approaches zero and grows quadratically as z becomes large.

The sufficient conditions can be derived directly. Pure scalar matter
requires `Y=V_z`; a strictly increasing V_z with range containing every
nonnegative Y gives a unique positive root. Pure dust requires
`b(z)=-2sqrt(z)V_z`, whose derivative is

    b_z=-(V_z+2z V_zz)/sqrt(z).

Therefore a positive `V_z+2zV_zz` on the dust branch gives monotonicity;
the endpoint limits determine whether its range includes every b. For the
proposed potential,

    V_z=(z-q³/z²)/(3t),
    V_zz=(1+2q³/z³)/(3t)>0,
    V_z+2z V_zz=(z+q³/z²)/t>0.

On the pure scalar axis `b=0`, V_z increases from zero at q to infinity.
For every finite `Y>=0` there is exactly one root `z>=q`, satisfying
`z³-3tY z²-q³=0`, with `L_zz=-V_zz<0`.

On the pure dust axis `Y=0`, b(z) decreases continuously from infinity
at zero to zero at q. Every finite `b>=0` has exactly one root `0<z<=q`.
An explicit formula, written to avoid numerical cancellation, is

    d=3tb/4,
    r=q³/(sqrt(q³+d²)+d),
    z=r^(2/3).

At that root,

    L_zz=-(V_z+2z V_zz)/(2z)<0.

These are exact pure-axis root-existence, uniqueness, and regularity
statements for the local potential at fixed X. They do not extend the
inherited auxiliary chart or prove all-density clock health.

## Actual clock response of the new proposal

At fixed z, the clock jets are

    L_X=F_X+(q-q²/z)q_X/t,
    L_XX=F_XX+[(1-2q/z)q_X²+(q-q²/z)q_XX]/t,
    L_Xz=q² q_X/(tz²).

The code derives K from the raw velocity Hessian and its auxiliary Schur
complement, and derives the fixed-momentum coefficient separately. For
`S=.1,b=.01,Y=0`, it gives

| Quantity | Value |
| --- | ---: |
| z | .9343443804009033 |
| L_zz | -10.00830425729295 |
| bare clock M | 5.499409804501756 |
| eliminated clock K | 9.113342087506329 |
| clock gradient L_X | 2.061733398747673 |
| clock probe speed squared | .2262324160501060 |
| Acan,z | -16.58525253708022 |

This sample is within the inherited z chart. At S=.1,b=.1 the same local
clock signs remain healthy and the chart still holds. At b=1 the clock
probe remains healthy but the inherited chart has been left. At b=100 the
root is regular while M, K and L_X are all negative. In fact for positive
q_X, `L_X` eventually becomes negative as dust drives z to zero. This
specific repair therefore does not give an all-density healthy-clock theory.

On the pure scalar axis, z>=q makes both L_X and the raw L_XX no smaller
than their respective raw vacuum values `F_X` and `F_XX-q_X²/t` whenever
q_X,q_XX>=0. If also
`F_X>0` and `tF_XX-q_X²>0`, the same pressure-Hessian argument as IC14
gives causal aligned scalar cones for every Y at that X. Again this is
conditional on the coefficient inequalities and does not certify the
physical chart for arbitrarily large Y.

The original chart bounds for the repaired axes can be written explicitly:

    b < 2[q³-exp(-3S)]/[3t exp(-3S/2)]    (pure dust),
    Y < [1-q³]/(3t)                      (pure scalar).

Activation has not been checked here. The reported clock probe is not the
full coupled dust velocity/density characteristic system or a dust Dirac
analysis; those remain separate obligations.

## Why simultaneous mixtures require a separate design step

There is a narrow exact obstruction to uniform raw-root regularity for
this class of potentials. Suppose a smooth V has `V_z(q)=0` and positive
finite `kappa=V_zz(q)`, with the exact matter terms `zY-b sqrt(z)`.
For the simultaneous nonnegative sources

    b*=4 q^(3/2) kappa,    Y*=2q kappa,

the auxiliary equation holds at z=q and `L_zz=0`. Hence no member of this
restricted smooth-potential class can have a nonzero fixed-X raw auxiliary
derivative for every pair `(b,Y)>=0`. This conclusion concerns that raw
regularity condition only. It is not a universal obstruction to a modified
matter/auxiliary action, to local mixed-source solutions, or to canonical
constraint regularity.

For the proposed rational potential at S=.1 the witness is
`b*=36.15603584665`, `Y*=18.69722726743`. The raw constraint and curvature
residuals are below `5e-50`, whereas `Acan,z=-46.55054885350` and the
computed auxiliary block still has rank two. The raw third derivative is
`L_zzz=1/(2tq)>0`, so this is a nondegenerate raw-root fold. Activation for
this large simultaneous source has not been evaluated.

## Verification and remaining work

From this directory:

    PYTHONDONTWRITEBYTECODE=1 python3 -m unittest test_ic15_dust_response -v
    PYTHONDONTWRITEBYTECODE=1 python3 ic15_dust_response.py

The original seven tests were written first, observed failing for the missing
module, then passed after implementation. They check both original fold equations,
compute the canonical block instead of entering a rank, compare the actual
raw velocity Hessian against the derived clock K, check vacuum preservation,
test pure-source roots at densities through one million, preserve the
large-dust instability as a negative control, and verify the narrow mixed
source statement. Eight symbolic identities check the matter scaling,
fold, and potential formulas. An eighth test, also observed failing before its
implementation, checks that a false exact identity produces exit 1 while
documented physical negative controls remain valid report results. With all
identities passing, normal mode exits 0 and `--require-full-closure` exits 2.

The finite root tests are not the proof of the all-density pure-axis
statements; the monotonicity and endpoint arguments above supply that proof.
No extension of the implicit clock chart, continuous coefficient certificate,
activation transition, full dust perturbations, sourced weak fields, or
phenomenological closure is claimed.
