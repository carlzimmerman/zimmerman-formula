# CFG747 — can collisionless cold energy relax onto the law's profile? (frozen criteria, committed alone)

Block CFG740–749. Written 2026-10-13, before any CFG747 script or number. κ = ½ fitted; the cold energy's mass is required; no
particle species; not theory closed.

## Why
CFG744: the polarization's own radiation cannot settle the cold energy at galaxy scales. Candidate B (cold energy *in*
galaxies, the law emerging from baryons + cold energy) then needs collisionless relaxation. It is the only channel left, and
the record has never tested it.

## Dynamics (from the action; derived in the CFG745-era D-form, restated)
- Spherical. Point baryonic mass M_b. Cold energy as N radial shells.
- With the critical tether (CFG698 J1 / CFG743) the cold energy's self-gravity cancels exactly. The cubic residual
  E = (G²/3a₀)∫m(r)³/r⁴ dr gives each shell an outward force u²/a₀, with u = G m(<r)/r².
- Units G = a₀ = M_b = 1 (r_M = 1): **r̈ = −1/r² + m(<r)²/r⁴**. The static law is m(r) = r (u = √(a₀g_N)).
  - This is derived in the script by finite differences of E, which is control K1.
- No law quantity is input: the force contains only the baryons and the cold energy's own enclosed mass.

## Runs
- N = 4000 shells; reflecting inner boundary r_min = 0.5; leapfrog, dt = 0.005; t_end = 3000 (about 10 deep circular periods at
  r = 50).
- Shells are radial (zero angular momentum), the extreme collisionless case. Disclosed as a limit.
- Initial states, all at rest:
  - **(i)** the law m = r on [0.5, 50] (control: it must stay within 1%);
  - **(ii)** a uniform-density sphere of the same total mass in R₀ = 50 (cold infall);
  - **(iii)** 1.5 × the law;
  - **(iv)** 0.5 × the law.

## Tests
- **K1.** The force from finite differences of E matches the formula to 1e-6.
- **K2.** Total energy is conserved to 1e-3 in every run.
- **R1. Relaxation.** For (ii)–(iv): the time-averaged m(<r)/r over t ∈ [2000, 3000] at r = 2, 5, 10, 20 (bound shells only;
  the escaped mass is reported).
  - **PASS iff |m/r − 1| ≤ 0.10 at all four radii for every state.** Otherwise FAIL: collisionless cold energy does not
    settle onto the law.
- **Reported.** The kinetic-energy fraction at the end (pressure support), and the sign of the deviation (excess or deficit
  relative to the law). That sign bears on C3.

## MUTATE (`CFG747_MUTATE=1`, exit 1 iff it bites)
No cold-energy force (pure baryon gravity on the shells). State (i) must then collapse: m(2)/2 > 1.5 at the end.
