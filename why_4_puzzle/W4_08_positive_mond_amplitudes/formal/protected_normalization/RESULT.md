# Protected normalization: three direct microscopic tests

2026-10-20. Base9a9ab4032; criteria-only commit2591280c8.
**The original healthy microscopic xi=1/4 goal is not achieved.**
This continuation tests what could forbid the amplitude-changing operator
left by the previous gravitational-constraint calculation. It produces
new operator/state/source obstructions, not a numerical selection or an
end-to-end Lean proof. Kappa=1/2 remains FITTED: CFG493 separately gives
kappa_Lambda=0.417+/-0.095 and kappa_crit=0.345+/-0.078; neither enters
the models. No measured acceleration, density, Hubble or PPN value is an input.

The single-mediator target is an actual IR/UV force ratio,
R=epsilon C3^2/C2^3=128pi/9. An electric cubic, scalar prepotential,
small-gradient Taylor coefficient or gamma repair is insufficient.
The complete raw derivations and primary source cards are linked below.
No source download, parameter/level scan, new numerical experiment,
new Lean module, reserved-file edit or heavy job was used.

## P1. A protected cubic, an actual radial workaround, and its failures

[PROTECTED_GAUGE.md](PROTECTED_GAUGE.md) starts with the exact
five-dimensional supersymmetric vector prepotential. Its protected cubic
multiplies sigma F^2, sigma(partial sigma)^2 and A wedge F wedge F.
For a static pure electric field, F wedge F=0. The fixed regular-modulus
response is quadratic and the constant Coulomb vacuum has zero energy.
Quantization has nontrivial charge-basis/manifold hypotheses; it does
not turn the prepotential into a static |grad Phi|^3 operator.

There is a genuine constructive workaround. After circle reduction,
add V=kappa_V sigma^3 to the critical dielectric T=C sigma.
Here [C]=mass^(-1) and [kappa_V]=mass; this potential coefficient
(called kappa in the raw gauge report) is distinct from the dimensionless
fitted law coefficient above. Locally neglecting
the retained radial gradients gives

    Lstatic=C sigma E^2/2-kappa_V sigma^3,
    sigma=sqrt(C/(6kappa_V))|E|,
    Leff=C^(3/2)|E|^3/[3sqrt(6kappa_V)].

The fixed-D Hamiltonian D^2/(2C sigma)+kappa_V sigma^3 has a unique positive
minimum for D nonzero. Its exact global-minimum factorization is already
covered by CurrentEnergy.lean after the stated substitutions, so we did
not duplicate that partial proof. This necessary energy check does not
integrate out the radial field or establish a microscopic spectrum.

The workaround has four decisive problems. Its zero-field vacuum has
sigma=0, zero vacuum energy and zero photon kinetic coefficient, with
Coulomb-branch charged thresholds becoming massless. The explicit N=1
superpotential diagnostic adds a coupling y not fixed by the CS level,
breaks the higher supersymmetry protection, and needs a global Wilson-line
completion. Ordinary positive FI uplift moves the vacuum to sigma0>0,
restoring quadratic infrared response; the cubic occurs at larger field.
Finally its healthy gauge field makes like charges repel. A universal
same-sign mass charge therefore does not supply gravitational attraction.

The FI+cubic diagnostic gives the inapplicable cross-regime number16/27
using static electric Lagrangian coefficients. The electric Hamiltonian's
cubic coefficient is twice as large and gives64/27 instead. Both use an
IR quadratic and high-field cubic, the reversed force regimes; neither
is the scalar MOND amplitude and no operational kappa is registered.
These are rigid potential energies; their positive gravitating stress in
a complete supergravity model has not been established.
Magnetic flux/circle axion terms and minimal ungauged supergravity were
also tested explicitly. A fixed Einstein/Maxwell/CS normalization in the
last example still leaves the pure-electric operator Maxwell and its
zero-field vacuum Ricci flat. General gauged/SCFT completions remain open;
the cited protected Coulomb action alone does not prove their existence
with the required force, state and normalization.

## P2. Actual invariant quantum state, including smooth nonuniform sources

[QUANTUM_STATE.md](QUANTUM_STATE.md) replaces the already failed flat
thermal gas with a scalar determinant on the actual Euclidean de Sitter
sphere. The regular two-field sigma-model coupling is
(Z+lambda_s^2 chi^2)(partial Phi)^2/2, with Z>0 and a bounded chi quartic.
It supplies a real covariant mass source and a positive classical
field-space metric, not an assumed invariant timelike vector.

For a free boson on S4, the spectrum is H^2 l(l+3)+m0^2, with the first
nonzero gap4H^2. Three local subtractions define a convergent relative
determinant. For m0^2>0 the response near h=0 is analytic in h^2.
For m0=0 the isolated free zero mode gives log(h^2), not |h|^3.
Keeping a stable quartic zero mode nonperturbatively makes its partition
function entire in the mass source and its logarithm locally analytic.
Its second response derivative is minus a positive variance.

This is extended beyond an impossible globally constant scalar gradient.
For any fixed smooth nonconstant real Phi_* on S4, put Phi=s Phi_*,
t=s^2 and B=lambda_s^2|grad Phi_*|^2. Then

    A_t=-Delta+m0^2+tB,
    Gamma_ren'''(t)=N Tr[(A_t^(-1/2) B A_t^(-1/2))^3]>0.

At positive m0^2, a uniformly convergent cubic relative determinant is
analytic near zero. At m0=0 the constant-mode Schur complement gives
(N/2)log t plus an analytic function. Neither contains the nonanalytic
t^(3/2) integral |grad Phi_*|^3 required by a positive local MOND term.
The trace derivative converges in general D when2k>D; k3 is safe forD4.
The full finite-cutoff interacting positive-quartic measure is also
analytic along this actual smooth profile. The continuum interacting
limit and a Lorentzian inhomogeneous force are not established here.

A further physical correction matters: the gravitating invariant vacuum
energy is epsilon=W-H partial_H W/4, not simply the effective-action
density W or flat-gas internal energy. The full covariant variation and
finite Einstein/cosmological matching terms are retained. The response
calculation fixes neither those finite matching data nor positive
absolute vacuum energy. This is a new invariant-state/profile test,
not a repetition of the inherited thermal wrong-sign result and not a
no-go for all nonlocal, fermionic or interacting states.

## P3. Repair light deflection without pretending to select the charge

[PHYSICAL_METRIC.md](PHYSICAL_METRIC.md) changes the universal matter
coupling to the same fixed gravity/rational action:

    tilde_g=A(phi)^2[g+(1-B(phi)^2)u u], A0=B0=1,
    alpha=(ln A)', beta=(ln B)', Q=alpha+beta.

The dust action is -m AB N dt. Its physical temporal potential is
n+Q delta_phi and its spatial potential is n-alpha delta_phi. Thus

    Gs=Q^2/(8pi C2), Guv=Gt+Gs, f=Gs/Guv,
    gamma_UV=1-[(2alpha+beta)/Q]f,
    xi_V0=f^3(125pi/128).

The family A=exp(-Q phi), B=exp(2Q phi) gives gamma_UV=1 for every Q>0.
It genuinely repairs the previous conformal relation. It also gives a
continuous counterfamily with varying physical Q^2/C2 and varying xi.
This changes a matter interaction, rather than rewriting the whole action.
The unit constraint, covariant Ward identity and invertibility hold for
all these Q; none selects the normalization. The primary TeVeS example
likewise retains normalization parameters despite its chosen metric shape.

With constant reference A0,B0 retained, conversion to physical rods/clocks
leaves xi_Vphys unchanged but multiplies the Friedmann-inferred xi by
B0^2. Merely normalizing the background physical metric does not erase
a tensor/matter cone ratio. The report derives all coefficients afresh;
it does not transfer the old conformal target-versus-gamma exclusion.

An added saturated cone-inclusion requirement over a two-sided scalar
neighborhood forces B'=0 at the reference state. Together with gamma=1
it removes the nonzero scalar charge for this fixed gravity action.
This is a conditional discriminator, not a consequence of invertibility
or a general causality theorem. Strict cone inclusions leave the slopes
free. The new matter metric also leaves the inherited matter-free clock
instability untouched. A gamma repair supplies neither health nor a
protected amplitude relation.

## Decision, proof status and surviving continuations

All three first uncertain implications were executed. A protected scalar
cubic does not transfer automatically to the required electric/scalar
operator; an invariant quantum state changes both its IR spectrum and
its vacuum-stress dictionary; a physical metric can repair lensing while
leaving the normalization free. The explicit radial-potential, quartic
zero-mode and disformal continuations were pursued rather than stopping
at those first failures.

These are analytic derivations with independent raw-equation cross-reviews.
No new kernel-checked theorem is claimed. The nine existing partial Lean
modules and the unverified actual-pi adapter retain their previous scopes.
Adding another algebraic certificate would not establish the missing
microscopic selector, so no duplicate proof module was added here.

The original end state still needs a healthy attractive universal source
map, positive same-state gravitating vacuum, actual MOND/UV crossover and
an independent protected equation for their amplitude. Remaining routes
are explicitly deferred: a full interacting/gauged source construction
beyond the protected Coulomb action; a Lorentzian nonlocal critical state
outside the tested finite-volume analytic class; or a complete microscopic
symmetry fixing a disformal charge and the response/vacuum relation
simultaneously. Each needs a new explicit action and a discriminating
health/normalization equation. None is declared impossible or solved by
this checkpoint. The full original goal remains active.
