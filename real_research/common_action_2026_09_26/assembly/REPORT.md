# Assembly checks: density, zero mode, energy and convex activation

These checks connect the independently developed action and transport lanes.
They establish the displayed identities; they do not turn a fixed-background
or finite-dimensional calculation into a global theorem for gravity.

## 1. Use an independent field when varying the carrier coupling

For real canonical fields phi, put

    Ld = exp(z) K - exp(-z) W,
    K = sum[(n.phi)^2]/2,
    W = sum[|D phi|^2]/2 + V(phi).

At fixed spatial geometry and fixed independent z, variation of the physical
lapse gives the same density as variation with respect to z:

    rho_d = exp(z) K + exp(-z) W = partial Ld/partial z.

The principal time and spatial coefficients are positive for every finite z.
The characteristic speed relative to the physical foliation is exp(-z).
Uniform bounds additionally require a bound on z. This exponential completion
repairs the linear coupling's coefficients 1+z and 1-z, which lose positivity
outside |z|<1. It also supplies the actual lapse density, rather than the
uncoupled density used by a first-order subtraction.

Substitution before variation is a different theory. The bounded example

    z(K)=1/[2(1+(K-1)^2)], K=v^2/2, L=exp(z(K)) K

has L_vv=-exp(1/2) at K=1. A bounded gate is therefore not enough to prevent
a ghost if it is composed with a velocity-dependent density. The negative
control is an exact symbolic check in `energy_check.py`.

## 2. The spatial zero mode must be repaired explicitly

An unprojected, purely spatial Z equation of the form

    spatial divergence + N rho_d = 0

on a compact boundaryless leaf cannot have everywhere positive rho_d and
positive N: integrating the equation gives an immediate contradiction.
This is a missing homogeneous equation, not a small-gradient approximation.

The main candidate uses the proper-volume projection

    barZ = integral(sqrt(h) Z)/integral(sqrt(h)), z=Z-barZ,
    Abar = <N rho_d>_h.

It gives the exact Z source rho_d-Abar/N, whose N-weighted integral vanishes.
It preserves the physical lapse density because the mean uses sqrt(h), not
N sqrt(h). It also produces real geometric terms. At fixed N and fields the
projector contributes the isotropic stress

    Delta T^ij = -(Abar/N) z h^ij.

The action report supplies the corresponding foliation variation; neither
this pressure term nor that variation may be silently dropped. Homogeneous
z=0 admits positive homogeneous carrier density. The projection is invariant
under Z -> Z+c(tau); its global shift is not a new local propagating field.

`projection_check.py` performs the exact weighted three-cell analogue of all
three variations (Z, lapse, volume), integrated-source cancellation and shift
invariance. All 17 identities vanish exactly. The continuum conclusions use
the explicitly displayed weighted-integral differentiation and the assumed
compact-leaf boundary conditions, not a claim that three cells prove a PDE.

## 3. Convex activation needs an energy primitive

Let J(p) be the convex nu_mono primitive in the action normalization, so its
Hessian eigenvalues are 4C_T and 4C_L. At fixed N,h both Delta_h S U and
Delta_N S U are linear in U. Thus

    G[J(D S U)+ell Delta S U-theta]

is convex when G is convex and nondecreasing. Its second variation is

    G' Hess(J)[D S v,D S v]
      + G'' [DJ.D S v+ell Delta S v]^2 >= 0.

Together with 2|DU-a|^2 this is strongly convex modulo constants. A fixed
linear compensator in U does not alter that conclusion. This is a property
of the auxiliary solve at fixed geometry and lapse. The weighted-Laplacian
version nevertheless fails a separate transition lapse test; see the
evolution report and the compensated unweighted repair. Convexity in U does
not by itself prove the health of lapse/metric dynamics.

The C4 ramp used here, with r=X/delta in (0,1), is

    G' = 35r^4-84r^5+70r^6-20r^7,
    G  = delta[7r^5-14r^6+10r^7-(5/2)r^8].

Extend it by G=0 for X<=0 and G=X-delta/2 for X>=delta.
Then 0<=G'<=1 and max G''=35/(16 delta). Its positive second variation,
endpoint matching and the failure of a multiplicative alternative are
checked exactly. A separate 96-site periodic deep-MOND illustration verifies
the strong Jensen inequality for 64 deterministic random pairs. This finite
illustration uses the deep power law; the analytic composition proof uses
the actual convex nu_mono primitive without replacing its empirical kernel.

The active bulk contains a constant -theta-delta/2 in its Lagrangian. It is
part of the varied energy and stress. The lapse-weighted Laplacian integrates
to a boundary term only with its exact measure; replacing it with Delta_h
requires the compensator recorded by the final action. No old observational
gate pass transfers to the new activation function without a new calculation.

## 4. Exact energy exchange and a genuinely bounded control

On a fixed flat slice, epsilon=exp(z)K+exp(-z)W satisfies on the carrier
equations

    partial_t epsilon - div[exp(-z) sum(phi_t D phi)] = -z_t epsilon.

The field energy is exchanged with the variable coupling. A time-dependent
carrier gate cannot be treated as supplying free energy. For the separate
control with canonical z action M^2[z_t^2-c_z^2|Dz|^2-omega^2 z^2]/2,
its equation supplies the opposite term, so total energy is conserved.
This canonical z control is **not** the spatial auxiliary Z of the common
gravity action; it is an independent verification of the exchange law.

Its homogeneous Hamiltonian is

    H=p_z^2/(2M^2)+M^2 omega^2 z^2/2+exp(-z) H_D,
    H_D=sum(p_phi^2)/2+V(phi).

H_D itself is conserved: a spatially uniform exponential coupling changes
the carrier's time parameter without changing its intrinsic orbit. For
positive masses and a coercive positive quartic potential the energy shell
is compact. In particular |z|<=sqrt(2H)/(M omega); H_D bounds every carrier
coordinate and momentum. Smooth finite-dimensional Hamiltonian continuation
then gives all-time homogeneous solutions for this control. This observation
prevents an incorrect claim that uniform z alone changes a density-transition
threshold in the intrinsic carrier dynamics.

The quartic used for that control is

    V4=lambda(R^4+s^4)/4-eta R^2 s^2/2
      =(lambda-eta)(R^4+s^4)/4+eta(R^2-s^2)^2/4,
    lambda>eta>=0.

Two deterministic integrations on 0<=t<=40 (seed 0 and .01) keep energy,
intrinsic energy and charge to relative errors below 1.5e-10. The zero seed
stays zero. The seeded real field grows, but that is not a charge-evacuation
theorem; the transport lane preserves the subsequent negative spatial test
and replaces this trial with a charge-converting, five-real-field potential.

## 5. Evidence and formal scope

- `run1/manifest.json`: 15 exact energy/source/current identities and two ODE controls.
- `gate_run1/manifest.json`: 22 exact convex-gate checks and 64 numerical Jensen controls.
- `projection_run1/manifest.json`: 17 exact projected-variation identities.
- `AssemblyBridge20260926.lean`: six compiled algebraic statements covering
  the zero-mode contradiction, projected-source cancellation, quartic
  decomposition/positivity, homogeneous energy bound and convex composition.

The accepted Lean compilation is recorded in `lean_attempt2_record.json` and
`lean_attempt2.log`. Its declarations use only propext, Classical.choice and
Quot.sound. The first failed source and log remain preserved. The Lean file
does not formalize continuum integration, full constraint algebra, a global
PDE theorem, or an empirical fit. Those scopes are not inferred from exit 0.
