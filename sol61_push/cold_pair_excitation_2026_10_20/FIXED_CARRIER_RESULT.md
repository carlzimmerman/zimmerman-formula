# Fixed carrier-phase sensitivity of the actual pair coordinates

The consistently propagated carrier phase changes the fitted coordinate rates modestly; it **does not explain their full difference from the stationary linear-mode frequencies**. It changes coordinate magnitudes and fit coherence enough that the original independently fitted phase was a material analysis choice. Neither analysis establishes a nonlinear eigenfrequency or an accepted weak-mode energy.

The fresh `fixed_carrier_run_001` completed 152/152 declared numerical/provenance controls with a valid v2 manifest, measured RSS 134,676,480 bytes, and extraction runtime 3.80 seconds. It read existing snapshots only: no field, BVP, eigenvalue or outgoing solve was performed. All prior code and results remain unchanged. A first launch was rejected before execution because explicit runner input flags were missing; that rejection is retained in `fixed_carrier_launch_attempt_001.json`. The corrected invocation pins all 29 predeclared inputs and changes no scientific criteria.

## Controlled frame comparison

For each of the in-phase, half-time-step and finer-space runs, and each Q136000/Q140000 reference, the old analysis supplies the phase at t=120. The new frame is

    theta(t)=theta(120)+omega_reference (t-120).

The same omega_reference is subtracted from the lab velocities, with charge-two transformation for X. Thus phase propagation and canonical velocity transformation now describe one consistent frozen carrier frame. The six t=120 anchors reproduce the old complex coordinates within the declared 1e-10 relative tolerance. The old exploratory fits are independently reproduced from their saved coordinates. Both variants use the same seven snapshots t=120,140,...,240 and the same constant + positive fundamental + positive second-harmonic search, at 701 rates between 0.04 and 0.075.

| Case | Reference Q | Old independently fitted phase: rate | Propagated phase: rate | Old / propagated fit residual |
|---|---:|---:|---:|---:|
| In phase | 136000 | 0.04910 | 0.04975 | 0.02866 / 0.09983 |
| In phase | 140000 | 0.04915 | 0.05020 | 0.02918 / 0.10281 |
| Half time step | 136000 | 0.04910 | 0.04975 | 0.02867 / 0.09984 |
| Half time step | 140000 | 0.04910 | 0.05020 | 0.02920 / 0.10282 |
| Finer space | 136000 | 0.04965 | 0.05040 | 0.03471 / 0.11354 |
| Finer space | 140000 | 0.04970 | 0.05080 | 0.03509 / 0.11754 |

The stationary linear frequencies are 0.060387406 and 0.059587045. Even the propagated-phase rates remain approximately 14.7–17.6% below the corresponding references. Gauge choice accounts for a part of the difference, not all of it, within this bounded comparison. This does not distinguish a nonlinear shape oscillation from multimode/transient/reference effects. About one reference cycle, seven samples, a searched rate and a flexible complex basis do not determine a physical eigenfrequency or its uncertainty.

The independently fitted phase differs from the propagated phase by up to about 0.29 radians during the window. Instantaneous coordinate squared changes by up to 21.4–23.1%. Its propagated-phase in-phase ranges are about 374–667 at Q136000 and 385–672 at Q140000; the finer-space ranges are about 345–627 and 357–633. These are conditional coordinates, not a newly accepted energy budget. The fixed-frame fit has a larger residual and the weak-reference interpretation remains unresolved. The contract's finite-coordinate, anchor, frame and accounting checks do not impose physical mode-acceptance thresholds.

## Core-only reference mismatch

To exclude the possibility that the earlier full-sphere mismatch came entirely from outer radiation, the same interpolated snapshots were integrated within spherical r<12 and r<15. The field-only positive norm is

    mismatch^2 = integral_core [2|Psi_rot-f|^2+2|X_rot-b|^2+(chi-h)^2]
                 / integral_core [2 f^2+2 b^2+h^2].

It uses the same cubic interpolation, 48-node angular quadrature and radial dr measure as the coordinate analysis. It is not energy, a charge fraction, or a fitted bound-mass measure.

For the in-phase run over t=120..240:

| Reference Q | r<12, fitted phase | r<12, propagated phase | r<15, fitted phase | r<15, propagated phase |
|---|---:|---:|---:|---:|
| 136000 | 0.246–0.367 | 0.249–0.409 | 0.263–0.423 | 0.266–0.437 |
| 140000 | 0.247–0.364 | 0.257–0.414 | 0.263–0.418 | 0.274–0.439 |

Across all three cases and both charges, the propagated-phase r<12 mismatch is about 0.232–0.414, and r<15 is 0.250–0.439. Outer waves alone therefore do not explain the reference mismatch. There is appreciable core deformation/reference difference too. These norms do not prove that no finite-amplitude mode exists; they prevent automatic identification with the previously calibrated weak stationary mode.

## Positive-Psi outlet and the soft-frequency threshold

For an actual second-harmonic positive-Psi wave about a carrier omega,

    nu=omega+2 Omega, Omega_cut=(1-omega)/2,
    v_group/c=sqrt(1-nu^(-2)),
    Q_out/K_out=1/(2 Omega),
    free_Psi_kinetic/K_out=(nu-1)/(2 Omega),
    charge_unbinding/K_out=(1-omega)/(2 Omega).

The last two fractions sum to one; K_out=E_out-omega Q_out. These are reference channel kinematics, not measurements of the collision's emitted flux or its coupling to cold galactic matter.

| Reference Q | Reference Omega | Omega_cut | nu | Group speed / c | Charge / K | Free-Psi kinetic / K |
|---|---:|---:|---:|---:|---:|---:|
| 136000 | 0.060387406 | 0.043958082 | 1.032858648 | 0.250229 | 8.279872 | 0.272065 |
| 140000 | 0.059587045 | 0.044193329 | 1.030787433 | 0.242577 | 8.391086 | 0.258340 |

For **hypothetical threshold proximity only**, inserting the old in-phase coordinate fit rates would instead give:

| Reference Q | Hypothetical fitted rate | Rate above cutoff | nu | Group speed / c | Charge / K | Free-Psi kinetic / K |
|---|---:|---:|---:|---:|---:|---:|---:|
| 136000 | 0.04910 | 0.005141918 | 1.010283836 | 0.142319 | 10.183299 | 0.104723 |
| 140000 | 0.04915 | 0.004956671 | 1.009913343 | 0.139770 | 10.172940 | 0.100848 |

Those fitted rates are not accepted physical frequencies. With the propagated-phase in-phase rates, the equally hypothetical free-kinetic fractions would be 0.116420/0.119655 and group speeds 0.150901/0.153625 c. No loss rate follows from substituting either fit into a weak-mode formula.

At fixed carrier, a genuinely softer physical mode approaches the Psi+ propagation threshold: the free-wave momentum/group speed decreases, the channel closes at the cutoff, charge exported per rotating excitation rises, and the fraction becoming free-Psi kinetic energy tends to zero while the unbinding fraction tends to one. At fixed far-wave amplitude its flux vanishes at threshold. The response amplitude can also vary or resonate, so this arithmetic alone is not a monotonicity theorem for the full nonlinear radiation coefficient. Charge-rest loss must remain in the remnant ledger; total lab radiation energy cannot all be counted as useful cold-wind kinetic energy while retaining the same core stock.

The surviving interpretation is a robust finite collision deformation with a large conditional quadrupole coordinate and a slow fitted coordinate component that is not solely an artifact of snapshot-wise carrier phase. Acceptance of a finite-amplitude mode, its physical radiation rate, capture/branching efficiency, galactic torque, and the four-dwarf mass/heating budgets remains separate. A clean finite-amplitude seed and conservative flux comparison can test that next gate without relabeling this sensitivity as closure.
