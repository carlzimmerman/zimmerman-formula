# CM2_gas_rich_past: FROZEN CRITERIA (committed before any script or number)

**Question.** CM1 found gravity-only outflows insufficient at today's gas mass (R 0.932, needed 0.817). Galaxies were
gas-richer in the past. Does a gas history tied to the stars actually formed, and capped by the supernova energy those
stars release, reach the target?

**Fixed from CM1 (read-only):** `cm1_setup.json`, `cm1_ics.npz`, dynamics, dt, estimator, a*, gas ramps (5 Myr out to
8a*, 200 Myr back), `e_lift`, STATIC run as reference, threshold R ≤ 0.817, canonical representative galaxy.

**Gas history (no free parameter).** Closed box over 10 Gyr with N equal bursts, constant star formation:
- gas before burst k (k = 0..N−1): M_gas,k = M_gas,today + M★,today (1 − k/N), so it starts at M_b and ends at M_gas,today + M★/N;
- gas that does not move, and stars, sit static at a*, so total baryons at a* are always M_b and conversion does no work;
- the supernova energy for burst k is E_SN/N;
- the moved mass is M_f,k = the largest mass ≤ M_gas,k with e_lift(M_f,k) ≤ ε_c E_SN/N.

**Coupling.** ε_c = 1: all supernova energy goes into lifting gas. All gas is also taken to start at the stellar scale.
Both are deliberate ceilings, so a miss is strong and a reach only shows existence. Reported: ε_used = Σ e_lift / E_SN.

**Runs.**
- **C40:** N = 40, period 250 Myr (CM1's cadence). PRIMARY.
- **C10:** N = 10, period 1 Gyr. Declared bracket, chosen after seeing CM1: heating is second order in moved mass, so at
  fixed energy burstier should heat more. It is the channel's best declared chance, not a scan. No other cadence may be
  added to this lane.
- **MUTATE:** C10 with the energy cap × 0.01.

**Statistic.** R = η(run)/η(CM1 STATIC) at the same time, marks every 1250 Myr (gas is back at a* at every mark), graded
at 10 Gyr.

**Verdicts (canonical; alt not run, its SPARC line fails at every c_f per X78).**
- **REACHED AT BOTH CADENCES:** C40 and C10 have R ≤ 0.817.
- **CADENCE-DEPENDENT:** only one reaches it. This is not a pass: cadence is then an undetermined input.
- **NOT REACHED AT CEILING:** neither reaches it.
- **NOT DECIDED:** a check fails.

**Checks.**
- **K1:** the new code with M_f fixed at M_gas,today and CM1's cadence reproduces CM1 PRIMARY's η at the 1250 Myr mark exactly.
- **K2:** work balance < 1% in every run.
- **K3:** Σ e_lift ≤ ε_c E_SN in every run, and M_f,k ≤ M_gas,k for every k.
- **MUTATE:** |1 − R| must be below half of C10's |1 − R|, and the moved mass must fall by the cap's effect.

**Scope.** Same galaxy, seed and spherical geometry as CM1. The halo is taken as formed at t = 0, and gas histories are
prescribed. Clusters untested. κ = ½ FITTED. Not theory closed. Cold dark energy is a gravitating field component, never
a particle.
