# CFG595: the measured cold supply. It is LARGER than the assumed (1 − f_b) M_ta, and the gravitating excess PERSISTS

Criteria were frozen first and committed alone (`FROZEN_CRITERIA.md`, commit 0bd1e4a93). Date: 2026-10-10. All numbers come from `cfg595_results.json` (printed in `cfg595_analysis.out`).

**Question (CFG594 item L05, the #1 inherited driver).** Every host is assumed to settle (1 − f_b) M_ta, the cold share of the ΛCDM turnaround ball. This lane replaces that with the cold mass that actually reaches each host in the framework's own PM, and recomputes the gravitating P(k). No ΛCDM template, halo model or standard-MOND shortcut is used.

## Verdict (per footing; never pooled)

| | canonical | alt |
|---|---|---|
| Q = Σ S / Σ (1 − f_b) M_ta, L100 N256, z = 0 | **2.26 → LARGER** | **2.12 → LARGER** |
| Q at z = 1 / 0.5 / 0 | 3.59 / 3.19 / 2.26 | 3.53 / 3.21 / 2.12 |
| Q at L100 N128 / N256 / N512 (z = 0) | 1.87 / 2.26 / 3.16 → **NOT CONVERGED** (it grows with N) | 1.84 / 2.12 / 3.09 → **NOT CONVERGED** |
| S / (cold the PM's turnaround-ball cover actually holds) | 1.03 | 1.03 |
| gravitating max\|r − 1\|, k ≤ 1: assumed → measured supply (dynamic L100 N256 re-run) | 0.661 → **0.292** | 0.634 → **0.321** |
| mean r, 1 < k ≤ 2: assumed → measured | 1.290 → 1.133 | 1.337 → 1.152 |
| σ8 ratio: assumed → measured | 1.083 → 1.096 | 1.075 → 1.105 |
| excess with the measured supply | **EXCESS PERSISTS** (about half removed: 0.56 at k ≤ 1, 0.54 at k 1–2) | **EXCESS PERSISTS** (0.49 / 0.55 removed) |

**The measured supply is not smaller in any state.** Q lies between 1.48 and 3.59 across all 20 measured states (two boxes, three meshes, three redshifts at L100 N128/N256, both footings). Every mass bin with at least 10 systems has a median ρ between 1.17 and 2.78.

**Why it is larger.** The cold that sits in each host's bound region is close to the cold the PM's own turnaround-ball cover holds (S / A_PM = 0.95–1.21 over the 20 states). The nominal (1 − f_b) M_ta undercounts that content by 1.4–3.7×, for two reasons:
- M_ta = (4π/3) r_ON³ Δ_ta ρ̄ is a lower bound on a 14-radius grid;
- systems with several distinct peaks are counted at their largest single host.

So the assumed supply does not inflate the halos. Measured from the framework's own sims, the cold that reaches the hosts is at least as large.

**Why the excess still falls by about half.** It is not because less cold arrives. Under the measured rule:
- the edges grow, so 46–48% of hosts reach the x ≤ 1 cap;
- the conservation region is now the bound region, not the turnaround cover;
- the q ≤ 1 availability cap binds for 78% of the catchment mass at z = 0 and removes 84% of the phantom demand. In the assumed-supply runs it binds for 18–21% of the mass and removes 12–15%. These are engine diagnostics (`cap_mass_frac`, `cap_e_removed_frac`) in the run JSONs.

The settled source per system is therefore set by the cold left in the bound region outside the edge, not by the supply total. The settled source assigned on the assumed-supply states is E / A_nom = 0.46 / 0.47 at L100 N256 z = 0, i.e. about 20% of the measured supply (E / S = 0.21 / 0.22).

**The persistence is robust.** The excess stays above 0.10 at L100 N256 under the dynamic re-run, and the static estimate at L100 N512 gives 0.33 / 0.38. The cap is the mechanism that lowers the excess under this rule. A rule that removed less demand would leave more excess, not less.

## The framework-native supply rule (L100 N256; Σ S / Σ A_nom by log M_sys bin; * = fewer than 5 systems)

| z | 12–12.5 | 12.5–13 | 13–13.5 | 13.5–14 | 14–14.5 | 14.5–16 |
|---|---|---|---|---|---|---|
| 1 (can / alt) | 1.68 / 1.68 | 1.97 / 1.97 | 2.76 / 2.81 | 3.73 / 3.67 | 15.2* / 15.3* | 12.2* / 11.2* |
| 0.5 | 1.67 / 1.66 | 1.80 / 1.82 | 2.10 / 2.13 | 3.08 / 3.16 | 2.26 / 2.24 | 9.7* / 9.6* |
| 0 | 1.67 / 1.68 | 1.73 / 1.73 | 1.71 / 1.71 | 2.18 / 2.07 | 2.60 / 2.52 | 3.14 / 2.53 |

Medians at z = 0 are 1.53–3.02 (canonical) and 1.54–2.57 (alt). The ratio rises with host mass and with redshift. At high z and high mass it is dominated by systems that link several peaks.

## Method

- **Bound region B** (framework-native, replacing the Δ_ta-ball finder): B is the raw candidate-B switch support λ₂ > τ − ε, i.e. f_sw > 0 before the edge mask, split into periodic 6-connected components. τ = (Δ_ta − 1)/3 still uses the shell ODE, which CFG594 L03 classes as the framework's own pre-turnaround collapse.
- **Measured supply.** S = (1 − f_b) × the mass of the B components that hold a system's peaks. A component shared between systems is split in proportion to the catchment cold.
- **Systems.** Peaks are grouped by the engine's catchment component, and A_nom = (1 − f_b) M_ta of the system's largest peak.
- **States.** CFG530's runs, re-run with this lane's engine copy `cfg595_pm.py` in mode ASSUMED so that the z = 1 and 0.5 states are also dumped (MU1 proves these are identical to CFG530). CFG530's saved z = 0 states supply L100 N512 and L200 N128/256/512.
- **Step 3.** The engine's MEAS mode measures S in-run at the edge-cache cadence. The edge is set by x = min(r_M / ln(1 + M_b/S) / R, 1). The settled cold is conserved per B component and drawn from B minus the edge. Everything else is unchanged.
- **Gravitating field.** δ_grav = −k²φ/(1.5 Ω_m), the CFG555 capture. Ratios are taken against CFG530's same-pipeline S0 at the same (L, N).
- **Static estimate.** The MEAS forces are applied to the frozen assumed-supply particle state. This is a declared approximation and is reported only. At N256 it overestimates the dynamic excess by 0.055 / 0.058.

## Controls (all PASS)

- **MU1, assumed supply reinserted.** The L100 N128/N256 runs, both footings, are bit-identical to CFG530's run JSONs: particle P and σ8 at z = 1, 0.5 and 0 agree to relative difference 0. The gravitating max\|r − 1\| reproduces CFG555 to ≤ 2.7e-8 (0.6613 / 0.6336 at N256).
- **MU2, supply zero.** Bit-identical to S0_L100_N128 at every snapshot. The captured source is ≤ 1.6e-7 of the peak.
- **C1.** The measurement equals the engine's own e_sum to ≤ 4.1e-6 (20 states), and n_catch matches exactly.
- **C2.** Bookkeeping closes to ≤ 6.5e-16.
- **C3 (reported).** For single-peak, single-component systems the median S_in / A_PM is 0.85 at N128 and 0.97 at N256. Near the spherical limit, F03's switch region and the turnaround ball hold the same cold.
- **MUTATE** (`CFG595_MUTATE=1`): with S := A_nom the verdict is SIMILAR; with MEAS P := ASSUMED P it is EXCESS PERSISTS with 0 removed. Both teeth bite (exit 1).

## Disclosures (dated 2026-10-10)

1. The decomposition (S / A_PM, A_PM / A_nom, E / S, single-peak Q) and the cap diagnostics come from post-freeze inspection. They are reported to explain the mechanism and play no verdict role.
2. As frozen, the MEAS edge combines the measured S with the inherited nominal M_b = f_ret f_b M_ta. Because S is about 2× A_nom, M_b/S halves and the edges grow, so the q ≤ 1 cap binds for most of the catchment mass. The "about half removed" result therefore belongs to this rule. Changing it would be a new lane. One candidate is M_b from the measured mass, i.e. the census f_ret applied to the region's own baryons.
3. B percolates. At L100 N256/N512 its largest component holds 69–84% of the bound cold, so a per-system S is a split share of a connected network (the frozen split rule). In aggregate, S matches the turnaround cover's content.
4. Convergence fails mainly through Σ S / Σ A_nom in the top bins and multi-peak systems. Bin medians move 1.41→1.53→1.76 (lowest bin, N128→N256→N512). The direction (LARGER) holds at every N and box; the amount does not converge.
5. No CFG530 same-pipeline S0 exists at L200 N512, so P(k) is not scored there (supply only). L200 N128 is scored but is coarse.
6. In the ZERO rows, the printed "in-run S/A_nom" is the S measured before the ×0.
7. The census f_ret, M_b, the x ≤ 1 cap, ε, the global QUMOND phantom, the ICs and the background stay inherited. S0 is a same-pipeline reference only: no verdict against data is drawn.

κ = ½ is FITTED. The footings are never pooled. The cold energy's MASS is still required, and no particle species is added. Not "theory closed".

## Reproduce

```
cd campaign_fresh_gravity/CFG595_measured_cold_supply
nice -n 10 python3 run_595.py one ASSUMED_can_L100_N256     # also ASSUMED/MEAS {can,alt} L100 N128/N256, ZERO {can,alt} L100 N128 (~2.5 min N128, ~18 min N256 at 4 threads)
nice -n 10 python3 cfg595_measure.py run MEAS_can_L100_N256  # per run; 'static ASSUMED_*_N256'; 'saved530 LR{can,alt}_L{100,200}_N{128,256,512}' (512^3 one at a time, ~4 min)
python3 cfg595_analysis.py ; CFG595_MUTATE=1 python3 cfg595_analysis.py
```
Outputs go to `../_external_data/cfg595_work/` (not committed). `cfg595_measure.out` is the measure-queue log.
