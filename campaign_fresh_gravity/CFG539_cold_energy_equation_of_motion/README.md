# CFG539: the cold energy equation of motion. No class is VIABLE. The only knob-free survivors (A, overdamped settling; C, inertial response) both fail T4 growth and the T1 fill test in a two-species PM, and A's rate coefficient acts as a knob

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (12f575de1). Stage 1 committed in 6f0ddbf42.
- **Settings:** κ = ½ FITTED. Footings 9.3603e-11 / 1.1312e-10, judged separately and never pooled. a0 flat; ν_mono. Seed 359, NSEED 512 (CFG530's realization). The cold energy's MASS is still required, and no particle species is added. Not "theory closed". Nothing was downloaded.
- **Arrays and logs:** `../_external_data/cfg539_work/`.

## Bottom line

1. **The equation of motion the record needs does not exist in knob-free form.**
   - Of five classes, three die in Stage 1 because each needs a constant:
     - B, a conservative fluid, needs a per-system temperature σ⁴ = G M_b a0/4;
     - D, the T17 rate law, needs λ fitted inside [0.0152, 0.0172], while the only forced value is λ = 1, 58–66× too high;
     - E, the KL/JKO flow, needs a diffusion scale.
   - The two knob-free survivors fail Stage 2:
     - **A** (overdamped settling flow) fails T1 fill, T3, T4 and convergence. Its single O(1) coefficient changes the growth answer by 0.16–0.27 when halved or doubled, so it **acts as a knob**.
     - **C** (inertial response) fails T1 fill, T4 at 256³ and convergence.
2. **What does emerge.** A's equilibrium is analytically d = 0 (a Lyapunov function exists), and its cap emerges on its own: nothing more than the catchment holds can be drawn. The census edge (T2) does **not** emerge; it is inherited. Removing it (MUTATE-S) gives more settling and more power, so the edge is load-bearing.
3. **Post-hoc finding that matters beyond this lane** (dated 2026-10-10, not a verdict input). The bookkeeping engines' "GROWTH OK" (CFG527/530) was measured on the **particles only**. Their gravitating density, particles + (e − comp), shows the same excess as EoM A:

   | footing | bookkeeping gravitating max\|r−1\| | EoM A max\|r−1\| |
   |---|---|---|
   | canonical, L200 256³ | 0.336 | 0.347 |
   | alt, L200 256³ | 0.388 | 0.381 |

   In candidate B the settled cold energy is matter and is what lensing sees. So "the bookkeeping passes T4" does not hold on the gravitating field; EoM A only makes that visible. See `cfg539_posthoc_grav_pk.out`.

## Stage 1 (`cfg539_stage1.py`; `.out`, `_MUTATE.out`, results JSONs)

| class | equation | constants beyond κ, 5.364, f_b | G9 (matter) | T1 | T2 | verdict |
|---|---|---|---|---|---|---|
| **A** overdamped settling | v_s = −catch τ_ff ∇ψ, ∇²ψ = 4πG d, d = s·max(ρ_ph − ρ_c, 0), τ_ff = 1/√(4πGρ_m) | none (coefficient fixed by "the deficit relaxes at the local free-fall rate", λ = 1) | exact | equilibrium d = 0: dF/dt = −∫ρ_c τ\|∇ψ\|² ≤ 0 (sympy); toy u 1 → 0 | edge INHERITED; cap EMERGENT (toy: settled 0.1016 = available 0.1016) | **survives** |
| B conservative fluid / superfluid | Euler in Φ + ψ with enthalpy | per-system σ⁴ = G M_b a0/4 (sympy) | exact | only at that temperature | – | killed (knob) |
| **C** inertial response | cold energy in catchments feels −∇ψ | none | exact | not an attractor: toy u min 0.36, final 0.79 | inherited | **survives** (to be tested numerically) |
| D T17 rate law | ∂_t f = λ√(4πGρ)(1 − f) | λ fitted | needs the draw rule | – | – | killed |
| E KL/JKO | ∂_t ρ = D∇²ρ − ∇·(ρ∇ln ρ_ph) | diffusion scale D | exact | global rescaling of ρ_ph | – | killed |

**Shared by A and C, disclosed:**
- **Energy sink.** A dissipates the potential energy released by settling, and nothing on the record supplies the sink (CFG462/489).
- **Causality: COND.** The Newtonian-limit drift is parabolic, so a covariant version needs a regulator.
- **Momentum.** The drive has no reaction force.
- **T5** holds structurally: baryons feel only the Newtonian field of real mass.
- **T6** holds structurally (mobility is zero outside catchments). Numerically, P_c/P_b at k ≤ 0.2 deviates from 1 by at most 0.052 (A; 0.069 in MUTATE-S) and 0.030 (C).
- **Stage-1 MUTATE:** reversing the sign fails S2, rc 1.
- **Correction 1 (2026-10-09, toy numerics only, before any Stage-2 result).** Run 1's S2 toy had a shell supply of 0.400, smaller than the deficit of 0.407. That is a supply-limited case, outside S2's premise. The toy also leaked one cell through the catchment faces. Run 1 is kept as `_run1`. The fix: catchment 0.1–0.9, and the face velocity set to zero outside the catchment.

## Stage 2: two-species PM (`cfg539_pm.py`, `run_539.py`, `cfg539_profiles.py`, `cfg539_analysis.py` → `cfg539_analysis.out`, `cfg539_results.json`)

r = P/P_S0 is for the total particle density at z = 0. The T4 cut is k ≤ min(1, k_Nyq/4). In the "core R" and "u" columns the matched-S0 value is in brackets. The LR column is CFG530's bookkeeping run at the same (L, N); its numbers are particle-only.

| run | σ8 ratio | max\|r−1\| | T4 | r(1) | r(2) | core R | u (S0) | LR |
|---|---|---|---|---|---|---|---|---|
| A can L100 128 / 256 | 1.026 / 1.045 | 0.323 / 0.464 | TENSION / TENSION | 1.34 / 1.49 | 1.53 / 1.70 | 0.955 / 1.091 (0.852) | 0.318 (0.394) | 0.076 / 0.145 |
| A can L200 128 / 256 | 1.016 / 1.031 | 0.103 / 0.347 | TENSION / TENSION | – / 1.35 | – / 1.53 | 0.951 / 1.046 (0.849) | 0.300 (0.382) | 0.023 / 0.080 |
| A alt L100 256 | 1.048 | 0.503 | TENSION, **UNSTABLE** (r(k_Nyq/2) = 2.08) | 1.54 | 1.80 | 1.039 (0.781) | 0.316 (0.421) | 0.149 |
| A alt L200 256 | 1.033 | 0.381 | TENSION | 1.39 | 1.62 | 1.045 (0.806) | 0.330 (0.422) | 0.086 |
| C can L100 128 / 256 | 1.012 / 1.028 | 0.093 / 0.163 | OK / TENSION | 1.10 / 1.17 | 1.07 / 1.07 | 0.845 / 0.881 (0.852) | 0.373 (0.394) | 0.076 / 0.145 |
| C can L200 128 / 256 | 1.006 / 1.014 | 0.037 / 0.1001 | OK / TENSION | – / 1.10 | – / 1.08 | 0.873 / 0.894 (0.849) | 0.356 (0.382) | 0.023 / 0.080 |
| C alt L100 128 / 256 | 1.013 / 1.030 | 0.1003 / 0.179 | TENSION / TENSION | 1.10 / 1.19 | 1.06 / 1.10 | 0.856 / **0.828** (0.781) | 0.391 (0.421) | 0.083 / 0.149 |
| C alt L200 128 / 256 | 1.006 / 1.016 | 0.036 / 0.114 | OK / TENSION | – / 1.11 | – / 1.09 | 0.838 / 0.878 (0.806) | 0.395 (0.422) | 0.017 / 0.086 |
| MUTATE-S (A can, no edge) L100 / L200 256 | 1.065 / 1.051 | 0.587 / 0.547 | TENSION | 1.64 / 1.57 | 1.94 / 1.87 | 1.161 / 1.114 | – | – |
| A can mob 0.5 / 1 / 2, L200 256 | 1.017 / 1.031 / 1.053 | 0.189 / 0.347 / 0.621 | TENSION | 1.19 / 1.35 / 1.63 | – | 0.959 / 1.046 / 1.166 | 0.329 / 0.300 / 0.275 | – |

### What happened to each target

**T1.**
- (a) Law-consistent: passes everywhere except C alt L100. Note that the canonical S0 itself passes (a) (disclosed before the freeze).
- (b) Direction: passes in every run; both EoMs move core R toward 1 or above it.
- (c) Fill, u ≤ ½ u_S0: **fails in every run**. A leaves 0.30–0.33 of the law's deficit unfilled, against 0.38–0.42 in S0.
- Why A fails (c): the drift carries no momentum, so settled particles keep their orbits and leave again. 53–57% of drifted particles end outside the edge. The deficit settles at a rate-limited steady state, not at the equilibrium. That is also why the coefficient matters.

**T3 (A, 256³ canonical).**
- Of the drifted cold energy that ends inside census edges, only **0.27 (L100) / 0.26 (L200)** came from outside the edge, against a required ≥ 0.5. Almost all of that came from the shell; less than 0.001 came from outside the catchment.
- So A mostly re-concentrates cold energy that is already inside the edge. It does not draw from the surroundings.
- Mass conservation is exact (particles).

**T4.**
- A fails at every (L, N), by 0.10–0.50, and the excess grows with resolution:
  - r(k = 1): 1.34 → 1.49 at L100;
  - r(k = 0.5): 1.11 → 1.19 at L200.
- C passes at 128³ in 3 of 4 cases but fails at 256³: 0.100–0.179. Ccan L200 is 0.10008 against the 0.10 cut, a hair over, reported as TENSION by the frozen rule.

**Convergence 128 → 256.**
- A canonical FAIL: Δr = 0.147 (L100) and 0.087 (L200).
- C canonical FAIL: Δr = 0.073 at L100.
- Alt is NOT EVALUABLE by the literal rule (fewer than 10 scored halos at 128³), although its Δr items also exceed 0.05.

**Robustness (A).** Mobility ×0.5 / ×2 changes max|r−1| by 0.159 / 0.274 and log core R by 0.038 / 0.047, so **the coefficient acts as a knob**. This agrees with CFG541's analytic point 2: stationary states are α-free, but the rate goes as 1/α, and the PM is rate-limited.

**T2 / MUTATE-S.**
- Removing the census edge is distinguishable: more power (0.55–0.59) and core R 1.11–1.16, against 1.05–1.09 with the edge. By the frozen rule the edge is load-bearing.
- On CFG541's note 1: an analytic self-stop of the variational flow at r_M/ln(1 + f_ret f_b/(1 − f_b)) concerns **stationary** states. These PM runs are rate-limited, with u ≈ 0.3, so they neither test nor contradict that claim. The no-edge run does not stop at the census-edge result in the PM.

**Sub-step clipping (CFG541's note 3, confirmed).** The 32-sub-step cap bound in dense, thin-reservoir regions:

| run | clipped particle-sub-steps |
|---|---|
| A can L100 256 | 592,076 |
| A alt L100 256 | 860,841 |
| MUTATE-S L100 256 | 1,562,074 |
| mob 2 L200 256 | 159,854 |
| L200 runs at mob 1 | 679 / 1,729 |

So the L100 A runs are partly displacement-limited. This cuts the drift; it cannot add to it, so it does not rescue the verdict.

**Controls.**
- The OFF two-species path reproduces CFG530 S0 at 128³ bit for bit: |dσ8| = 0 and max|dP/P| = 0 at every snapshot.
- The statistic copy identity holds (0.97259 in both).
- Aalt L100 256 and MUTATE-S L100 256 are UNSTABLE by the frozen definition (r at k_Nyq/2 is 2.08 / 2.22). Those runs are INVALID; no verdict depends on them alone.
- 512³: not run, because no class is VIABLE.

## Verdict (frozen rules)

| class | canonical | alt |
|---|---|---|
| **A** overdamped settling flow | **NOT VIABLE**: T4 (all four), T1 fill, T3, convergence, robustness (coefficient = knob) | **NOT VIABLE**: T4, T1 fill (and L100 256 UNSTABLE) |
| **C** inertial response | **NOT VIABLE**: T4 at 256³, T1 fill, convergence | **NOT VIABLE**: T4, T1 law-consistency at L100, T1 fill |
| B, D, E | killed in Stage 1 (knob) | – |

**Plain reading.**
- A local, mass-conserving, G9-respecting equation of motion can make the law's phantom its equilibrium, with the supply cap for free. That is A in Stage 1.
- But a drift that moves cold energy without damping its orbits never reaches that equilibrium in a cosmological time. Its rate is then set by an O(1) coefficient that the framework does not fix, and the settled mass it does move over-clusters the matter field at k ≈ 1.
- An EoM that works would need to damp the cold energy's random motion as well, i.e. to supply the energy sink, and nothing on the record does (CFG461/462/489).
- The bookkeeping's T4 pass rests on measuring particles rather than the gravitating field (post-hoc above). That deserves its own lane.

## Departures and disclosures (dated)

- **2026-10-09.** The launcher parsed "NOEDGE" as a mesh size and crashed both workers after the first eight 128³ jobs. It was fixed with an exact L/N regex. Nothing physical changed, and the NOEDGE claims were re-run.
- **2026-10-10.** `cfg539_posthoc_grav_pk.py` was added after the first 256³ results. It is reported, not a verdict input.
- **Convergence rule, alt.** NOT EVALUABLE is the literal rule (fewer than 10 scored halos at 128³). It does not change the verdict, because T4 already fails.
- **Coordinator note from CFG541** (MUTATE-S as the Onsager form, mobility O(1) free, clipping in thin reservoirs). It was reported against the frozen rules above; no rule was changed.

## Run

```
python3 campaign_fresh_gravity/CFG539_cold_energy_equation_of_motion/cfg539_stage1.py ; CFG539_MUTATE=1 python3 .../cfg539_stage1.py
nohup python3 .../run_539.py -t 4 OFF_L100_N128 OFF_L200_N128 Acan_L100_N128 ... Acan_mob2_L200_N256 &   # x2 workers
python3 .../cfg539_analysis.py compute ; python3 .../cfg539_analysis.py ; python3 .../cfg539_posthoc_grav_pk.py
```
