# Self-review of the candidate mechanism

Primary verdict: **incomplete, with the smallest missing implication being a
physical conversion interaction that selects the required populations while
preserving the disk acceleration relation.** The executable prototype exists;
the proposed explanation of real dwarfs and clusters is not established.

This is a self-review, not independent peer review. The claims reviewed are
the explicit restricted statements in DERIVATION.md, and the code/input hashes
in the current run manifests. The original paper and prior repository reports
were used to identify constraints, not treated as independently validated data.

## Dependency and obligation check

| Obligation | Evidence | Verdict |
|---|---|---|
| Positive T/F rest mass, no extra P mass | Density definitions and summed continuity equations | Passed in the spherical definition |
| State conversion compatible with P | Conversion source term in partial_t P is explicit | Passed as Newtonian radial bookkeeping |
| Gravitational and tether signs | Variation of shell energy; numerical finite-difference gradient checks | Passed in stated spherical domain |
| Baryonic law at F=0 | Analytic inversion and root-solver cross-check | Passed conditional on enough T and negligible stiffness |
| F can be added without changing disk source | Coexistence equation depends on g_b+g_F | Failed; source change is compulsory |
| Conversion conserves energy | Finite field-energy difference booked to receiver | Conditional: receiver coupling not derived |
| Conversion conserves momentum | Spherical balanced export assumed, no microscopic recoil calculation | Not addressed beyond symmetry assumption |
| Cold bound remnant exists after imposed conversion | Softened live-shell finite-time experiments | Numerical evidence only; resolution limits reported |
| Binding diagnostic is an eternal bound fraction | Time-dependent potential can exchange orbital energy | Not established |
| Profile force excess is an observed mass/dispersion excess | No tracer equilibrium, observational likelihood, or lensing theory | Not established |
| Common binding gap and common bath select dwarf/cluster versus disks | Frozen-profile chemical potential inequality | Failed for declared q targets and profiles |
| Positive density in general geometries | Spherical nonnegative mass only | Out of scope; saddle issue unresolved |
| Cosmological, relativistic, stiffness and satellite consistency | Omitted | Not addressed |

## Adversarial reconstruction

1. Keeping F gravitating but removing it from the tether source contradicts
   the shell energy variation. The model does not use that shortcut.
2. Keeping partial_t P=-j_T after conversions contradicts T continuity.
   The added integral source is essential and is explicitly documented.
3. Turning W off at fixed kinetic energy without a receiver loses energy.
   The ledger exposes the missing channel; it does not invent a physical one.
4. Baryon removal performs external work. The energy-error tests apply only
   after the impulse, with the baryon potential fixed.
5. Chemical stationarity at a frozen density is not dynamical equilibrium.
   Its selector failure is not a universal no-go for all two-state media.
6. The all-F retention runs must use ordinary gravity, not the coexisting
   equilibrium amplification. The acceleration diagnostic uses ordinary
   gravity with the declared softened kernel.
7. The initial mass ratio refers to initial baryons. Following 90% loss it is
   not legitimate to say the final system has the same cosmic ratio.
8. The finite reservoir already runs out before the original toy dwarf's
   0.3 kpc test radius. This prevents claiming the initial toy model realizes
   the full baryonic law at that radius. Chemical tests are restricted to
   existing T material, and the supply flag is retained in the JSON.
9. The 17.72 Gyr cluster simulation is a mathematical duration, not a valid
   age-matched cluster inference. Earlier snapshots can be inspected, but a
   formation history and age-consistent inference remain absent.
10. A unit-conversion error was detected by the SI benchmark; rejected static
    output and its source are retained. The current manifests are separate.

## Proofreading self-review

Reviewed the newly written derivation and claim restrictions, including
dimensions, state labels, radial signs, source terms and zero-field limit.
No mathematical-token changes were made as proofreading. Substantive limits
remain as listed above; they are not typography errors.
