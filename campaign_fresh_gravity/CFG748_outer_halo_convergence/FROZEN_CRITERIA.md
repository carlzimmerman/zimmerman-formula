# CFG748 — does the outer halo converge onto the law, given time and mass? (frozen criteria, committed alone)

Block CFG740–749. Written before any CFG748 number. κ = ½ fitted; the cold energy's mass is required; no particle species; not
theory closed.

## Why
CFG747: collisionless cold energy (self-gravity cancelled by the critical tether, cubic push u²/a₀) lands on the law at
r ≤ 5 r_M from every start. It falls short at 10–20 r_M (0.62–0.96). That run could not separate "not enough time" from "not
enough mass" (some was ejected, R₀ = 50).

## Runs (CFG747's code and dynamics unchanged except as listed)
- **R₀ = 200, t_end = 10000**, N = 4000, dt = 0.005, r_min = 0.5, core 0.5, radial shells.
- Initial states, at rest:
  - **(i)** the law on [0.5, 200] (control);
  - **(ii)** a uniform sphere of the same mass (cold infall);
  - **(iii)** 0.5 × the law (mass-starved).
- Record m(<r)/r at r = 2, 5, 10, 20, 50, time-averaged over five windows: [1000, 2000], [3000, 4000], [5000, 6000],
  [7000, 8000], [9000, 10000].

## Tests
- **C1. Convergence.** For (ii) and (iii), in the last window, |m/r − 1| ≤ 0.10 at all five radii. PASS / FAIL.
- **C2. Trend** (reported, decides the reading if C1 fails). For each radius, the change of m/r between the first and last
  windows. **CONVERGING** if every outer radius (10, 20, 50) moves toward 1 by at least half its first-window gap; **STALLED**
  otherwise.
- **Controls:**
  - K2: energy conserved to 1e-3;
  - the control stays within 1% at all radii in every window.

## Reading rule (frozen)
- **C1 PASS:** collisionless relaxation reaches the law out to 50 r_M; the CFG747 deficit was time/mass.
- **C1 FAIL + CONVERGING:** the outer halo is still settling; its present-day state depends on age, and the deficit is
  transient.
- **C1 FAIL + STALLED:** collisionless cold energy settles to a *different* outer profile than the law. The law then holds
  only in inner halos for this mechanism. That is a prediction (outer deficit), and it conflicts with SPARC's flat outer curves
  if r ≳ 10 r_M is reached there.

## MUTATE (`CFG748_MUTATE=1`, exit 1 iff it bites)
State (ii) with no cold-energy force must collapse: m(2)/2 > 1.5 in the last window.
