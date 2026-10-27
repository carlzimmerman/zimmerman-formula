# CF1_cf_window_map: FROZEN CRITERIA (committed alone, before any script or number)

**The question this lane sharpens (owner, 2026-10-27).** "Why does condensation start at about 10^12–10^12.5?"

**The reduction, from the record.**

- **The switch.** In X62's environment-keyed rule, route E (cold dark energy halo) applies if the system is a satellite,
  or if it lies above X43's crossover.
- **The crossover.** It is the mass where η Σ_coll(M) = a₀/(2πG), with η = (4/(3B(1))) c_f^{5/4}. So the threshold mass
  is a function of the single number c_f.
- **The same c_f sets the cluster and group core rule.**
  - X44: groups need c_f ≳ 4.2.
  - X43 and GC1: G-OUT-M3 is +2.00 at c_f = 5.
  - X48: c_f = 5.6–7.2 over-fills G-IN-Mall.
  - X62: SPARC and lensing fail when the crossover drops below the galaxy scale.
- **So the question is:** is there a c_f window in which one number passes every graded line, and where does it put the
  threshold?

This is a **constraint map**: the data's requirement on c_f is stated together with the threshold it implies. No c_f is
adopted or claimed derived here. The native c_f comes from X48's zooms; the ng64 run is in progress in a peer lane.

κ = ½ FITTED. Footings 9.3603e-11 / 1.1312e-10 m/s², never pooled. Cold dark energy is a gravitating w ≈ 0 field
component, not matter and not a particle. Not "theory closed". No result here may be described as the data favouring the
framework.

## 1. Harness

X62's committed harness is used, from `x62_env_switch.py` (8c7768d26d). It applies the full graded line set:

| line | source | pass rule |
|---|---|---|
| SPARC | X43 | both backgrounds pass |
| groups | X43 | CONSISTENT |
| cluster keys | X43 | all 15 keys pass in both h cells |
| LG dwarfs | X51 | five classes, \|Z\| < 2 |
| KiDS lensing | X53 | Δχ²(ENV2H − L2H) ≤ +9 and Δχ²(ENV2H − H2H) < 0 |

**The only change.** c_f becomes a scalar parameter, set consistently in X43 (`CF`, which also moves the crossover flag)
and in X53 (`eta_of`). The background is inherited, exactly as X62 ran it. The native-normalisation swap is not mixed
in, so the map stays comparable with X62.

**Grid.** c_f ∈ {3.5, 4.0, 4.25, 4.5, 4.75, 5.0, 5.25, 5.5, 6.0}, run on both footings.

**Reported for each c_f:**
- the crossover mass M_×, per footing;
- every failing line, with its Z or Δχ²;
- the X62 verdict string.

## 2. Step 0 (stop rule)

- **S0a.** c_f = 4.0 reproduces X62's committed `reported_cf4` verdict and failing lines on both footings. Those are:
  groups (canonical) +2.02, G-OUT-M3, SPARC alt, and lensing +22.5 canonical. Numbers must match to 0.01.
- **S0b.** The crossover at c_f = 4 equals X43's 10^12.09 (canonical) / 10^12.43 (alt), within 0.01 dex.

## 3. Verdict (frozen)

- **WINDOW EXISTS [a, b]:** at least one grid c_f passes every line on **both** footings. The window is the run of
  passing grid points. The threshold range it implies, M_×(b)…M_×(a) per footing, is reported.
- **NO SINGLE c_f:** no grid point passes everything. The report then gives, for each line, the c_f range in which that
  line passes. The pair of lines whose ranges do not overlap is named; that is the binding tension.
- **Reported only:** the grid resolution (0.25 in c_f) limits the window edges, and no interpolation is claimed.

## 4. Checks and twin

- **K1.** The crossover mass decreases monotonically with c_f, as the construction requires.
- **K2.** X62's switch-property check (profile equals the flagged branch) passes at every grid point.
- **K3.** Peak RSS < 1 GB, per process.
- **MUTATE (`CF1_MUTATE=1`, separate outputs).**
  - m1: the switch flag is inverted, as in X62's twin.
  - m2: the S0a target × 1.01.
  - The twin must fail S0a and K2.

Run with `PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 -I cf1_window.py`. Amendments only in `AMENDMENTS.md`,
each committed before the run it affects.
