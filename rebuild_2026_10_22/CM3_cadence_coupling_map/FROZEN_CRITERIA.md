# CM3_cadence_coupling_map: FROZEN CRITERIA (committed before any script or number)

**Question.** CM2 was CADENCE-DEPENDENT: 40 bursts miss, 10 bursts reach the target at coupling 1. How far does that reach
survive lower coupling, and another seed and galaxy mass? The owner asked for all options to be tested. This is a declared
finite map answering "where does the channel work", not a fit: nothing here selects a preferred value.

**Machinery.** CM2's script and CM1's ICs procedure, unchanged. Threshold R ≤ 0.817. All R at 10 Gyr against a STATIC of
the same ICs.

**Map (base galaxy, seed 1), bursts N × coupling ε_c:**
| | ε_c 1 | ε_c 0.3 | ε_c 0.1 |
|---|---|---|---|
| N 10 | CM2 C10 | run | run |
| N 20 (500 Myr) | run | run | not run |
| N 40 | CM2 C40 | not run | not run |

(N 40 missed at ε_c 1, so it cannot do better lower.)

**Robustness (N 10, ε_c 1), each with its own STATIC:**
- **SEED2:** same galaxy, seed 2.
- **LO, HI:** M_b/M200 at the active sample's 16th/84th percentile; gas fraction of baryons at the median; R_d/R200 at the median; E_SN ∝ M★.

**Verdicts.**
- Robustness: **ROBUST** if SEED2, LO and HI all reach R ≤ 0.817; else **FRAGILE**.
- Map: report the reaching cells; no single-value claim.

**Checks.**
- **K1:** regenerating seed 1 ICs reproduces `cm1_ics.npz` exactly.
- **K2:** work balance < 1% in every run.
- **K3:** Σ lift ≤ ε_c E_SN in every run.
- **MUTATE (monotonic):** at N 10, R does not fall as ε_c falls, within 0.03.
- Any failure makes the affected result NOT DECIDED.

**Scope.** Cadence and coupling stay undetermined inputs here. A reaching cell is existence at that cadence and coupling,
not a derivation, and ε_c is a ceiling on what real feedback delivers. Softened halos are not put through the full grader
in this lane. κ = ½ FITTED. Not theory closed. Cold dark energy is a gravitating field component, never a particle.
