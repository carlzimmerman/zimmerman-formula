# PN28-RES: the reservoir pressure changes the closure problem

Checkpoint PN28, base `66c45c5082f651dd54e171f98c11acd9cb3d9086`.
Owner: `/root`. Inputs are pinned in `../INPUTS.json`. This route changes only
new files in its assigned directory. No claim of literature novelty is made.

## Target and hypotheses

Test whether the energy reservoir needed to maintain the MC27 logarithmic
kinetic pressure can select its amplitude, and whether a local vacuum
reservoir supplies a healthy completion. The first discriminator is the exact
reciprocal energy equation including the reservoir's own pressure.

Let rho>0 be a conserved nonrelativistic rest-mass density, D the derivative
along its bulk velocity, and theta the velocity divergence. Consider an
isotropic random stress with kinetic energy density K=3p/2 and impose

    D rho = -rho theta,
    p = A log(rho/rho_ref),       A>0, rho_ref>0 fixed,
    D K + (K+p) theta = Q.                                      (1)

Physical kinetic states are restricted to p>=0, hence rho>=rho_ref. The
algebraic reservoir ODE also exists outside that interval, but negative p is
not an admitted isotropic kinetic stress. This route assumes zero spatial
random-energy flux and an exact material log
closure, rather than merely a log profile in equilibrium. Q is positive for
energy supplied to the random kinetic sector, per volume per time. The
reciprocal local reservoir has energy density e and pressure p_R=w e, with
constant w and the same material derivative:

    D e + (1+w)e theta = -Q.                                   (2)

For w=-1 there is no vacuum four-velocity; D refers to the matter frame used
to project its stress tensor. Equations (1)-(2) are energy equations only.
Momentum transfer must also be included, as below. They are not a microscopic
action, a proof of local thermalization, or a kinetic existence theorem.

## 1. All constant-w reservoir solutions

Set z=log(rho/rho_ref)=p/A and b=1+w. Since Dz=-theta, equation (1) gives

    Q = A(5z-3) theta/2 = (5p-3A) theta/2.                    (3)

On a material family, (2) consequently requires

    d e/dz - b e = A(5z-3)/2.                                (4)

This is a state relation required to hold during arbitrary compression and
expansion; dividing a single static trajectory by theta=0 would not derive
it. Direct integration gives, for b nonzero,

    e(z) = C exp(bz) - A[5z/(2b) + 5/(2b^2) - 3/(2b)].        (5)

For b=0 the separate, regular family is

    e_V(z) = C + A(5z^2/4 - 3z/2)
           = C + 5p^2/(4A) - 3p/2.                           (6)

C is fixed along the chosen material trajectory, not selected by conservation.
For any compact z interval, any A>0, and any fixed finite w, C can be made large
enough that e>0 throughout that interval. For a prescribed positive reservoir
energy at one reference state, continuity likewise leaves an open family of
positive states and A values nearby. Conservation has not selected A, its
ratio to a separately gravitating vacuum, or the interval's endpoints.

Two useful cases of (5) are

    w=0:   e=C(rho/rho_ref) - 5p/2 - A,
    w=1/3: e=C(rho/rho_ref)^(4/3) - 15p/8 - 9A/32.            (7)

These expressions enforce the desired log closure by construction. They do
not derive it. A constant vacuum e_V is incompatible with (3) during a
nonzero compression except instantaneously at p=3A/5. The MC27 exact-log
interval has p/A>=2/3, so that exception is absent there.

## 2. Include the reservoir pressure and momentum

Use the effective perfect-fluid completion

    epsilon = rho c^2 + 3p/2 + e,
    P = p+w e,
    epsilon+P = rho c^2 + 5p/2 + (1+w)e.                     (8)

Its nonrelativistic internal relation K=3p/2 is only appropriate to cold
particles with p much less than rho c^2; no exact relativistic particle EOS
is asserted. Equations (1)-(2) imply

    D epsilon + (epsilon+P) theta = 0.                       (9)

For material perturbations holding C,A,rho_ref fixed, differentiation gives

    rho dP/drho = A + w[(1+w)e+(5p-3A)/2],
    rho d epsilon/drho = rho c^2+5p/2+(1+w)e.                 (10)

At states with epsilon+P nonzero, in a locally uniform rest frame, linearizing conservation of this total
perfect-fluid stress gives the adiabatic acoustic characteristic

    c_s^2/c^2 = [A+w((1+w)e+(5p-3A)/2)]
                /[rho c^2+5p/2+(1+w)e].                     (11)

One can obtain (11) directly from mass conservation and
`(epsilon+P) partial_t(delta u)/c^2 + grad(delta P)=0`.
Thus the formula is not inferred from a background time derivative alone.
Other independent reservoir variables, delayed exchange, flux or anisotropic
stress change this closure and need their own characteristic calculation.

For a pressureless positive reservoir, (11) is positive. For w>=0, e>=0 and
p>=2A/3, its numerator and denominator are positive as well. These are local
sign statements, not proofs of causal propagation, global stability or a
microphysical parent. Positive energy and local compressibility still do not
fix A: the state contains C, rho_ref and an arbitrary A.

For the exact local vacuum case, the integration constant cancels and (11)
reduces to the especially restrictive equation

    c_s^2 = 5 c^2 (A-p)/(2 rho c^2+5p).                     (12)

The enthalpy is positive on the physical domain, but c_s^2<0 whenever p>A. At
p=A the acoustic coefficient vanishes; this degenerate boundary is not a
stability result. Under these hypotheses the
local acoustic modes have a gradient instability: `omega^2=c_s^2 k^2`,
within the range where this continuum closure applies. This is not a ghost
claim, a proof about arbitrarily high wave numbers, or an exclusion of all
interacting-vacuum theories.

For MC27, p/A=-log x+2/3. The threshold is

    x_T=exp(-1/3)=0.7165313106... .                            (13)

Every quarter-density core family member used in the previous bridge has
x_c<=1/4 and hence p_c/A>=log(4)+2/3>1. It therefore contains an inner region
in which (12) is negative. This threshold is the same as the kinetic
temperature extremum in the independent transport route.

With a spatially uniform C, the total pressure gradient is

    grad P = (5/2)(1-p/A) grad p.                             (14)

For the outward-decreasing MC27 kinetic pressure and p>A, this gradient
reverses sign. Consequently the old hydrostatic profile cannot be retained
unchanged after adding this reservoir. A spatially varying advected C could
alter the background gradient, but does not remove the local fixed-C
characteristic (12).

This issue is required by covariant conservation: a stress tensor
`T_V^{mu nu}=-e_V g^{mu nu}` has divergence `-grad^nu e_V`. A spatially varying
e_V necessarily transfers momentum as well as energy. Retaining its energy
exchange while suppressing its pressure-gradient force is a different,
nonconserving truncation. The general interacting-vacuum statement is known;
see SOURCES.md. The specialized polynomial (6) and acoustic equation (12)
are direct calculations under the hypotheses here.

## 3. A second escape test: local relaxation does not fix the amplitude

For an arbitrary isotropic kinetic state, define an effective logarithmic
coefficient a=p/z on a z>0 interval. Do not confuse this lowercase a with the
gravitational acceleration a0 or a cosmological scale factor. With actual
flux q and transfer Q, the exact moment equation gives

    D a = [2(Q-div q)-(5p-3a)theta]/(3z).                     (15)

Any law that makes a approach A_star by writing
`Q-div q=(5p-3a)theta/2+(3z/2)gamma(A_star-a)` with gamma>0
will have `D a=gamma(A_star-a)`. It has inserted A_star as the fixed point.
Energy conservation can be restored by an opposite reservoir source, but
this does not predict that fixed point. Equation (15) separates a derived
microscopic source from a target encoded in a source prescription.

## Outcome and continuation

The constant-w local energy equations have been solved exactly. The simplest
vacuum-reservoir completion is refuted as a stable instantaneous log fluid in
the MC27 dense core under the stated assumptions. Reservoir energy
conservation by itself leaves a continuous normalization freedom. These are
partial results, not a completed theory or a general no-go theorem.

The route to a local w=-1, zero-flux, instantaneously logotropic core is closed
under these hypotheses. Nonlocal radiative transport, finite response time,
non-vacuum mediator stress, and a changed conserved-density map remain open.
The dispersion route tests a genuine changed interaction. The transport route
quantifies required cooling. A new cosmological diffusion correspondence is
checked in SOURCES.md, but it does not supply the missing microscopic A.

Finite symbolic, quadrature and ODE checks are specified before execution in
contract.json and check_reservoir.py. Their scope is distinct from the written
proofs. Independent review will be recorded separately, not inferred from a
passed script.
