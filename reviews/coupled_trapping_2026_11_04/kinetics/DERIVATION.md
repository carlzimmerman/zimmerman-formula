# CT09 coupled limiting networks: derivation and scope

Base checkpoint: Git `285353a57bc1c21662c5565830bbc97ac5b0f7f9`, with exact
read-only TP06/TK08 input hashes pinned in each v2 manifest. This package owns
only this `kinetics/` directory. The numerical state is conditional on the
prescribed initial massless frozen FD distribution, xi=.02, e=h=lambda=.003,
and g=sqrt(29/200)e. It does not derive reheating or initial thermalization.

## Momentum-resolved scalar inverse-decay sink

Let g=24 count all spin/particle/antiparticle charged light-fermion degrees.
The physical energy is E(p,x)=sqrt(p^2+m(x)^2), where m is the actual middle
signed eigenbranch of the recorded broken 3x3 fermion mass matrix. Initial
f(q)=1/(exp(q)+1), q=p/Tc; Tc=Tc0 exp(-N), N=log a. The same f enters both
rho and the force; no undepleted force is retained after f changes.

For a real parent S with M>2m and its actual inclusive partial width Gamma
into these fermions, beta=sqrt(1-4m^2/M^2). The prior isotropic parent integral
can be transformed exactly into

    gamma = Gamma M/(2 pi^2 beta) int dE1 dE2 f(p1) f(p2) Theta,
    Theta = 1 if |E1 E2-(M^2-2m^2)/2| <= p1 p2, else 0.

Use dE1 dE2 = (p1/E1)(p2/E2) dp1 dp2. Integrating over both labelled daughter
energies counts the full ordered pair domain. The normalization is fixed by
recovering the independent parent-momentum integral and the MB detailed-balance
limit already tested in TK08. This is an unblocked forward inverse reaction,
with initially empty parent occupation; it is a partial-channel absorption
limit, not the actual collision operator after a parent decays back.

For momentum cells i with physical number measure

    wi = g Tc^3/(2 pi^2) (qhi^3-qlo^3)/3,
    ni=wi fi,

construct a symmetric positive matrix Kij approximating the allowed area in
(E1,E2) cell i,j. The integration over E2 uses its exact allowed interval;
4-node Gauss integration over E1 and explicit symmetrization give the matrix.
Then

    dfi/dtau = -[2 Gamma M/(g beta Tc^3 Wi)] fi sum_j Kij fj,
    tau = mu t_physical, Wi=(qhi^3-qlo^3)/3.

Sum all open parents; equivalent degenerate parents are grouped by adding
partial widths. This guarantees the discrete number identity

    sum_i wi dfi/dtau = -2 gamma_discrete.

Cell representative energies define the radiation energy source
Q=-sum_i wi Ei dfi/dtau. The same removed energy is subtracted from particles
and added once to radiation. The quadrature error in the representative
energies, cell-constant occupation, width interpolation and orbit averaging
must be tested separately; this algebraic identity alone does not verify the
continuum collision integral. Symmetric pair removal preserves zero signed
U1 charge; it does not assert pair-number conservation.

## Field energy and slow action

The field kinetic energy in mu units is 31 (dx/dtau)^2; its mass parameter is
Mrad=62. The instantaneous conservative potential is

    U(x;f,N) = V0(x) + sum_i wi(N) fi Ei(x,N).

V0 is the recorded global tree gravity plus rigid CW potential relative to
its origin value. The physical particle energy is retained in U. At fixed f,
redshifting the momenta and cell volume gives

    partial_N rho |_f,x = -3(rho+P).

The action is J=(1/(2pi)) integral p_x dx around the bounded positive-X orbit.
For turning points xL,xR,

    J = sqrt(2 Mrad)/pi int_xL^xR sqrt(Etotal-U) dx,
    Torb = sqrt(2 Mrad) int_xL^xR dx/sqrt(Etotal-U).

Angle-mapped Gauss quadrature regularizes the turning endpoints. Solving the
action equation determines the orbit energy for the changing distribution.
The occupation f evolves by its time average over this same orbit. If
Ci=dfi/dtau and H=Hphysical/mu, the consistent averaged action equation is

    dJ/dN = -3 J + Torb/(2pi H) sum_i wi
              [ <Ei Ci> - <Ei><Ci> ].

The covariance term is necessary: scalar resonance losses depend on orbital
phase. Simply assigning J proportional to a^-3 would discard their correlated
energy removal. The coordinator independently derived the same identity.

The mean energy equation implied by this system is

    dEtotal/dN = -3 <62 xdot^2 + rho+P> - <Q>/H,
    drho_rad/dN = -4 rho_rad + <Q>/H.

The program integrates the Hubble-work ledger alongside the occupations and
action, and compares Etotal+rho_rad+integrated work with its initial value.
The visible radiation bath determines H at explicit xi=.02; the conditional
hidden source is a small addition to that dominant bath, not its temperature.
The averaging approximation requires H and all relevant reaction rates small
compared with the orbital frequency. A number-averaged rate check is necessary
but does not bound rare-cell local rates; those are a residual concern.

## Scope of the compared closures

1. Absorption: each produced neutral scalar disappears into a radiation ledger.
   This maximizes the instantaneous sink for the included parent channels at
   a specified f,x,T. Its self-consistent history is not an upper bound on all
   possible histories, because depletion changes the restoring force and orbit.
2. Zero collisions: all occupations are conserved in comoving cells. This is
   a collisionless number-preserving limit. It is not the actual carrier-
   conserving cascade: conversion between scalars and fermions and gaugino
   radiation can preserve carrier number while changing energy and force.
3. FD-amplitude: force and source use A(N) times the initial FD shape. This is
   a diagnostic closure. Scalar resonances select momenta; comparing it with
   the cell evolution directly tests the error of preserving the shape.

The actual tree cascade returns charged carriers at small x; at larger x its
neutral terminal products can be massive and exert their own forces. The
lightest charged ordering changes, opening S->F+gaugino below the crossing and
F->S+gaugino above it. Repeated conversion can radiate more than one gaugino per
initial carrier. These processes cannot be inferred from a zero-loss switch.
The full charged scalar/fermion/neutral daughter distribution network remains
a distinct required leaf. No reduced network here is the complete DE/DM history.

## Two charged distributions and actual conversion vertices

`two_species.py` advances separate fermion and scalar occupations instead of
forcing an instantaneous minimum-mass branch. The latter artificial envelope
creates a cusp at the mass crossing and an extra inner-well separatrix; its
failed runs are retained as a closure failure, not a physical escape result.
The actual conversion widths are much slower than a field oscillation, even
where they greatly exceed H.

The lowest physical charged scalar has exactly

    mS(x) = (e/2) sqrt(x^2+2/(31e)).

Its twelve real physical degrees differ from the fermion's 24 spin degrees.
For bookkeeping both distributions use the same g=24 carrier-number measure,
so the actual scalar occupation is fC=2 fS. This preserves the carrier count
while changing statistics and phase-space density. Consequently the scalar
pair inverse production integral is four times the same-form integral in
fS, using the actual inclusive parent partial width to the twelve scalars.
The scalar threshold factor Gamma proportional to beta is removed before
interpolating Gamma/beta; this resolves the constant singlet threshold at
x=25.4000254000381 without extrapolating a width through a closed channel.

The two-species potential is smooth:

    U=V0+rhoF[fF]+rhoS[fS].

The actual projected vacuum widths from the independent photino packet are
used for F->S+gaugino and S->F+gaugino, summed over U1, SU2 and SU3. The
neutral gaugino mass is retained in those input widths. Its tiny mass is
neglected only in the daughter boost and subsequent radiation ledger. These
are conditional empty-final-state vacuum rates. The photino package shows
that Pauli factors and inverse reactions cannot generally remain negligible;
no completed reduced run here removes that obligation.

For a parent A of momentum p and daughter B, the isotropic rest-frame
kinematics at massless neutral boost order is

    E*B=(mA^2+mB^2)/(2 mA), p*=(mA^2-mB^2)/(2 mA),
    EB=(EA E*B+p p* cos theta)/mA,
    decay rate per parent=GammaA mA/EA.

Eight angular nodes deposit the charged daughter into adjacent energy cells
with positive linear weights. Within the represented energy range this
preserves both number and daughter energy. Finite endpoints clamp the
negligible initial FD tail and are tracked as a grid-overflow diagnostic.
An independent control checks generator column sums, positivity, and the exact
isotropic energy moment

    mean emitted energy per unit tau per parent
      = GammaA (mA^2-mB^2)/(2 mA),

which is independent of the parent momentum after the time-dilation factor.
The seven benchmark moment errors are below 5.2e-8 relative; this does not
uniformly certify all later distributions at finite grid endpoints.

In comoving number-cell coordinates uF,uS, the conversion matrix has
nonnegative off-diagonal entries and zero column sum. Scalar-parent absorption
adds a negative diagonal depending on the current distributions. At each
orbit the full generator, its energy moment, and the two-species force are
averaged together. A positive matrix exponential handles the stiffness in
Gamma/H; predictor/corrector comparisons adapt the step. The action covariance
uses both species and all momentum transfers. The particle energy lost to
conversion is added once to the gaugino energy ledger, while an absorbing
scalar-parent event adds its full removed particle energy to that same
auxiliary ledger. Decays preserve one signed carrier; pair absorption removes
opposite charges symmetrically.

These runs include actual charge-state conversion and momentum recoil, but
the scalar-parent absorption is still an optimistic reduced exit and the
emitted gauginos have no kinetic occupation/inverse/Pauli operator. Massive
neutral cascade daughters exert no force here. They therefore remain
conditional coupled computations, not the target physical history. A cold
turning-point interval is also not a computed cold photino distribution.

## Coherent finite-width pole and explicit hybrid continuation

The four exactly degenerate constant-mass singlets require their coherent
production/absorptive matrix, rather than four independent irreversible exits.
`finite_bw.py` consumes the separately audited rank-one API in
`../gravity_resonance/pole_api.py`. It replaces exactly those scalar NWA
parents in the local window |x-xpole|<.05. All other scalar parents retain the
previous optimistic absorption closure; no NWA singlet term is counted twice.
The fixed coefficients are a local tree-pole packet. Moving them through a
large field range, adding medium occupancy, or identifying their neutral
energy with radiation is not established.

For the physical component-averaged opposite-charge pair cross section and
n=nplus+nminus with equal densities, the isotropic bin sink is

    df_i/dtau = -fi/2 sum_j nmeasure_j fj <sigma v_Moller>ij.

Thus the effective matrix in the existing scalar inverse-decay implementation
is Kij=PREF Tc^6 Wi Wj <sigma v>ij/2. This factor was independently checked by
the fresh transport reviewer. A separate 64/128/256 radial-bin experiment
compares the finite-width sink with independent NWA production multiplied by
the neutral-exit probability obtained from a matrix Lyapunov equation. At
256 bulk cells they agree within .36%; the production Gram normalization
agrees with the actual scalar partial width within 4.2e-5. This checks the
inclusive real-scalar/particle-plus-antiparticle factors; it does not certify
a coarse evolving abundance.

The center-of-mass cross section is transformed by s/(4 Ei Ej). The angular
integration uses theta=atan((s-Mpole^2)/(Mpole Gammaref)), including its exact
Jacobian; this resolves a pole much narrower than the thermal angular range.
Twelve-node results agree with the independent split-cosine API to below
3e-7 in weighted rate and 8e-7 in matrix entries on the three tested points.
The orbital phase integration additionally splits at both the thermal
Tc^2/(2 m dm/dx) scale and the finite-width Gamma/(4 dm/dx) scale.

A first full initial-to-late BW job hit its 240-second bound with no valid
result. That is resource inconclusiveness, not a failed physical history.
`resume_bw.py` instead starts from the completed matched-leading NWA state at
Tc=1e-5 and changes to the static finite-width kernel for the late interval.
This is an explicit hybrid history, not an initial-to-final BW solution and
not a monotone upper bound on every possible physical history. It saves the
entire numeric state every twenty accepted steps, permitting a fresh bounded
continuation without losing a resource-limited checkpoint.

The local potential is shifted to zero at the cold reference, with the pinned
quartic Taylor polynomial inside |x-xpole|<.0018. The cold minimum is solved
from the force. This avoids cancellation of tiny oscillation energies against
a roughly 1e-9 constant and the bounded minimizer's sqrt(machine-epsilon)*x
position floor. The harmonic phase measure is evaluated analytically instead
of subtracting nearly equal E, V and rho. A prior corrected phase-split run
failed through precisely that subtraction; its apparent enormous period and
rate/oscillation ratio are numerical, not a physical hierarchy failure.

The numeric action code retains a floor convention: for log(J/Jinitial)<-20
it replaces dlogJ/dN by max(-3,dlogJ/dN). The independent reviewer evaluated
the unclamped derivative at the two saved final NWA states and found about
-2.9999997, so the clamp was inactive there. It has not been independently
certified inactive at every earlier accepted point. The implementation and
this limitation remain explicit; no universal action theorem is inferred.

The static coherent width eigenvalues divided by the cold field frequency
are roughly .06--.115, according to the independent audit. This is not an
instantaneously decaying-parent hierarchy. Small parent occupancy alone does
not prove a local collision kernel in a time-dependent resonance crossing;
a memory/coherence calculation is a separate missing leaf. The auxiliary
radiation ledger, omitted massive neutral forces, gaugino Pauli/inverse
terms, and this locality condition prevent promoting any completed reduced
run into the original DE/charged-relic/cold-photino success claim.
