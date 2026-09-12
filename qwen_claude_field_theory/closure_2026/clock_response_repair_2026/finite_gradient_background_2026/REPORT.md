# Finite homogeneous gradient: the momentum constraint requires zero scalar shift charge

**Precise obstruction:** the inherited nonzero-charge branch cannot be an exactly homogeneous diagonal-Bianchi-I solution with a nonzero constant comoving scalar gradient, homogeneous clock, and comoving baryons/radiation. Including the fixed cubic term does not remove that obstruction: cancellation of its momentum flux requires the distinct zero-shift-charge branch. This calculation neither constructs nor excludes all such zero-charge backgrounds.

The result follows from two quantities derived independently from the action and geometry:

    G0x = 0,
    T0x = b Jchi,
    Jchi = 2 PX Q - 2 gamma theta Q^2 + 2 gamma Hx Y.

Here Q=Cdot, Y=b^2/ax^2 and theta=Hx+Hy+Hz. Consequently b!=0 and zero ordinary-matter flux force Jchi=0. The scalar equation conserves ax*ay*az*Jchi per unit coordinate volume. The archived physical history instead carries approximately0.0971724238633, reproduced directly from the fixed action without changing its coefficients.

## Ansatz, action and direct derivation

Use proper time and

    ds^2 = -dt^2 + ax(t)^2 dx^2 + ay(t)^2 dy^2 + az(t)^2 dz^2,
    tau=tau(t),  chi=C(t)+b*x,  b=constant,
    Hi=ai_dot/ai,  volume=ax*ay*az,
    L=P(X,tau)-V(tau)+s W(Y,tau)+gamma X Box chi,

with constant gamma and signature(-+++). The functions P,V,W are the same frozen coefficient functions; they contain no explicit chi. Ordinary matter is minimally coupled and comoving with these slices.

SymPy constructs the Christoffel symbols and Ricci tensor from this metric. It obtains all three G0i=0 and

    G00 = Hx*Hy + Hx*Hz + Hy*Hz.

The stress of a generic comoving perfect fluid also gives T0i=0. The cosmological-constant term has no0i component. Thus the Einstein momentum equation imposes T0x(clock+chi)=0 without using any background evolution equation.

For a time-dependent symmetric inverse-metric variation delta g^{0x}=epsilon(t), before imposing the shift-free background,

    delta X = -2 Q b epsilon,
    delta s = 0,
    delta Y = 0,
    delta sqrt(-g) = 0,
    Box chi = -Qdot-theta Q,
    delta(Box chi) = b(epsilon_dot+theta epsilon).

The two off-diagonal metric entries vary together, so delta S=-integral volume*T0x*epsilon dt. The ordinary scalar variation immediately gives

    T0x(gamma0) = 2 PX Q b.

For PX>0, Q>0 and b!=0, this cannot satisfy the momentum constraint. Neither the potential nor the projected-gradient clock term supplies compensating flux under the specified ansatz.

For the cubic action, retain the derivative of the metric variation:

    delta S3 = gamma integral volume*b*
        [2Q(Qdot+theta Q)epsilon + X(epsilon_dot+theta epsilon)] dt.

After integration by parts with compactly supported variations and using Ydot=-2 Hx Y, the Qdot terms cancel. The result is

    T0x(cubic) = 2 gamma b(Hx Y-theta Q^2),
    T0x(total) = 2b[PX Q-gamma theta Q^2+gamma Hx Y].

The exact cancellation condition is therefore

    PX Q = gamma(theta Q^2-Hx Y).

This is derived from the untruncated cubic action, not inferred from its homogeneous energy expression. An independent inverse-g00 variation gives

    T00(cubic) = 2 gamma Q(Hx Y-theta Q^2).

Its Y=0 isotropic limit is -6 gamma H Q^3, agreeing with the existing action convention.

## Why cubic cancellation requires a different charge branch

Independently reduce the homogeneous scalar action while retaining Qdot. Because C itself does not appear, its generalized momentum is

    Jchi = (1/volume) [partial Lred/partial Q
                      - d/dt(partial Lred/partial Qdot)].

Direct differentiation gives exactly the Jchi in the opening equations. Its Euler equation is

    d/dt(volume Jchi)=0.

The equality T0x=b Jchi was checked symbolically against the independent metric variation. It is valid with the cubic term and arbitrary frozen coefficient functions of tau, under the stated homogeneous ansatz. It does not rely on a small-gamma expansion or on an assumed zero sound speed.

As a separate sign and boundary-term check, the reduced cubic density obeys

    volume gamma X(-Qdot-theta Q)
      = volume gamma[-(2/3)theta Q^3+2 Q Hx Y]
        + d/dt[volume gamma(-Q^3/3+QY)].

The full energy also satisfies the exact identity

    rho_clock = Q Jchi-P+V.

Thus a putative allowed zero-charge background must obey rho_clock=V-P as well as the remaining Einstein, clock and scalar equations. Setting only the momentum numerator to zero is not a completed solution.

The constant-b ansatz additionally enforces Ydot=-2HxY. With Hx>0 it redshifts the gradient; it supplies no homogeneous mechanism for growing b. This is a kinematic restriction of the ansatz, not a proof about inhomogeneous gradient growth.

## Bounded test of the inherited history

Use the physical Q and H from radiation_002, gamma=1e-6, the original frozen qbar reference inside P, and the five unchanged positive L192 transverse-root values. The full P_X includes its existing gamma-dependent completion; it was not replaced by its gamma0 limit for the cubic comparison.

At a=1:

    Q = 0.9078321505772312, H = 0.5191118192004086,
    Y = 0.00025242369831450766,
    PX(full) = 0.053361759909897416,
    T0x(P part) = 0.001539326556607332,
    T0x(cubic) = -0.00000004077969820609554,
    T0x(total) = 0.0015392857769091258,
    Jchi = 0.09688447579251618.

The cubic contribution cancels only2.65e-5 of the ordinary scalar flux. The zero-gradient current at the same archived point reproduces the recorded conserved charge0.09717242386329555 exactly.

| Epoch a | Cubic/P flux | Total/P flux | Isotropic H required for cancellation / inherited H |
| --- | ---: | ---: | ---: |
| 1.000000 | -2.6492e-5 | 0.99997351 | 37747 |
| 0.750137 | -1.2808e-5 | 0.99998719 | 78075 |
| 0.562705 | -6.6922e-6 | 0.99999331 | 149427 |
| 0.422105 | -3.8730e-6 | 0.99999613 | 258198 |
| 0.316637 | -2.4188e-6 | 0.99999758 | 413428 |

The required isotropic rate is the algebraic diagnostic

    H_required = PX Q/[gamma(3Q^2-Y)].

At a=1 it is19595.1 in the source's dimensionless units. Merely replacing H by this value while holding the field/matter values fixed would give3H_required^2=1.15190e9, whereas the zero-charge Hamiltonian right side V-P+rho_b+rho_r+Lambda is0.720228 (M2=1). It therefore fails that constraint by a factor1.60e9. An anisotropic zero-charge branch has additional freedom and is not excluded by this isotropic diagnostic.

These five finite-gradient points are not claimed to form one trajectory: each point uses its own inherited local Y and physical Q. Their purpose is to test whether the published coefficient/history data automatically supply momentum cancellation. They do not.

## Scope and remaining work

PAPER19 explicitly starts from a locally uniform WKB gradient. Such a local jet is not itself a global homogeneous Einstein solution. This audit obstructs its promotion to the specific charged homogeneous background above; it does not exclude a local WKB region embedded in inhomogeneous geometry.

A consistent completion must either solve a separate zero-shift-charge branch, admit compensating ordinary-matter momentum/tilt, change the clock alignment, or include spatial dependence in the fields and metric so that the Einstein momentum equation changes. No new matter species or coefficient functions are introduced here, and none of these alternatives is established to work.

In particular, the gamma0 positive-PX/Q obstruction is exact for this ansatz. With nonzero gamma, the algebra permits cancellation, but only at zero current; the same nonzero-charge history cannot use that option. This is a constrained-background result, not a universal no-go or a new empirical law.

## Verification and provenance

Six unit tests passed. Three geometry/matter identities and ten action/current/boundary identities were derived and checked exactly. The numerical current reproduces every selected archived charge with absolute discrepancy zero at the recorded precision. No coefficient or initial charge was fitted.

The bounded run and exact commands are recorded in COMMANDS.md and run_001/manifest.json. The child and runner exited0; current-input/output-hash validation also exited0. The manifest pins the action sources, coefficient evaluator, original history, L192 roots, PAPER19 source, numerical helper, and both new scripts. No Git mutation or changes outside this audit directory were made.

Used computation-audit and verification-before-completion workflows. SymPy's differential identities and a finite archive check support this restricted obstruction; no Lean theorem was added merely to repackage its final elementary zero-product consequence.
