# A rotation-dependent barrier: conditional feasibility result

We constructed and tested an effective interaction that preserves an initially
tethered phase in strongly rotating galaxy-size toy profiles and permits
conversion in weakly rotating profiles. The equations contain no galaxy-type
switch. This is a candidate effective model, not established microphysics or
an observational explanation of excess bound mass.

The interaction couples an internal strain to baryon vorticity. Eliminating
that strain produces a positive conversion barrier proportional to
`C = |curl(v)|² / (|curl(v)|² + sigma²/Lrho²)`.
An additional positive internal-phase gradient energy suppresses conversion
of a weakly protected core inside a coherent rotating system. Both terms
vanish, with their first force variations, in a uniform pure tethered phase.
Thus that phase retains the parent acceleration relation within its finite
halo and equilibrium assumptions. Mixed phases do not inherit that guarantee.

The common parameters are beta=20 and phase length=30 kpc. They were selected
for feasibility, not derived from particle physics. Every numeric profile
is crossed with the same continuous streaming inputs f; none is assigned a
physical phase by its name. The geometry is a spherical mass profile with
midplane rotation and a Jeans dispersion approximation, not a real disk.

## Results

Final tethered mass percentages at 256 cells and dimensionless time 100:

| Baryon mass (solar masses) | Scale (kpc) | Weak rotation, initially T | Strong rotation, initially T | Strong rotation, initially F |
|---|---:|---:|---:|---:|
| 300,000 | 0.3 | 0.1054% | approximately 100% | 0.000246% |
| 100 million | 1 | 0.1133% | approximately 100% | 0.000246% |
| 60 billion | 3 | 0.1275% | approximately 100% | 0.000246% |
| 100 trillion | 300 | 0.1172% | T endpoint unstable | 0.000246% |

Weak rotation uses f=.3; strong initially-T cases use both .95 and .99;
initially-F cases use .99. The unstable rotating cluster-size cases were
recorded as failed protection, not silently excluded or given a simulated
conversion fraction. A rotating small object stays tethered, whereas a
weakly rotating large galaxy-size object converts: kinematics drives the
distinction in these tests.

There are 42 integrated trajectories and six endpoint stability failures
across 64, 128 and 256 cells. The largest final fraction change from 128 to
256 cells is 2.86e-8. The maximum relative energy-plus-receiver balance error
in this main suite is 2.10e-7. All four final evidence manifests validate.
An additional nine-point parameter neighborhood preserves the tested
galaxy-size stability distinction; it does not repair the rotating cluster
counterexample. Finite perturbations reveal a finite basin: x=.9 returns
to T in protected cases, while x=.5 converts.

## What remains unsolved

1. **Formation:** uniform F is the global internal-energy minimum. This
   dissipative model cannot create T from F without an external work source.
2. **Bound mass:** density and baryon kinematics were frozen. Conversion is
   demonstrated; subsequent gravitational retention and measured excess
   acceleration are not. The earlier imposed-switch retention experiment
   in the parent folder does not establish retention for this interaction.
3. **Physical origin:** the strain coupling, phase length, dissipation and
   thermal/noise properties are assumptions. Time is not calibrated to Gyr.
4. **Scope:** equal counterrotating streams have zero mean vorticity and
   receive no protection. Real geometry, live backreaction, nearby systems,
   boundary conditions, nucleation and lensing remain untested.

## Evidence and reproduction

- [Derivation](DERIVATION.md): interaction, spatial mass accounting and receiver.
- [Self-audit](AUDIT.md): claim boundaries and rejected intermediate evidence.
- [Next obligations](HANDOFF.md): work needed for a physical explanation.
- Final data: `run_angular64`, `run_angular128`, `run_angular256`, `run_diagnostics`.
- Final implementation: `angular_gate.py`, `angular_probe.py`, `diagnostics.py`.

From this directory, using Python with NumPy and SciPy:

```sh
OPENBLAS_NUM_THREADS=1 python3 angular_probe.py --n 256 --output /tmp/angular-repeat.json
OPENBLAS_NUM_THREADS=1 python3 diagnostics.py /tmp/angular-diagnostics-repeat.json
```

Each accepted run contains its exact command, hashed inputs, contract and
results in `manifest.json`. Earlier polynomial runs are historical, not
evidence for the final bounded-angle potential. See `AMENDMENTS.md` and
`ANGULAR_CONTRACT.md` for changes. No observed galaxies were fitted.
