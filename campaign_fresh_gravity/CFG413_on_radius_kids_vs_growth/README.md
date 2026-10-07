# CFG413: how far out must the law be ON for KiDS (two-halo modelled), and how much growth excess lies beyond? DOOR OPEN on the frozen criteria (x = 0.3; x = 0.4 if judged against the best-fitting x), heavily conditional

Criteria: `FROZEN_CRITERIA.md`, committed alone first (d468d555b). Scripts: `cfg413_kids.py`, `cfg413_growth.py` (both rc 0, all checks pass).
MUTATE (`CFG413_MUTATE=1`, outputs `*_MUTATE.*`): x = 0.05 fails KiDS by Δχ² +39.8 / +51.1. DETECTED.
Light CPU: one thread, nice 15, about 1.5 min + 20 s. No PM run, no download.

## Verdict
**DOOR OPEN by the frozen rule.** At x = 0.3 both legs pass on both footings:
- KiDS Δχ² vs x = 1 is −11.5 (canonical) / −6.6 (alt).
- It stays ≤ 4 in all 15 drop-one-bin variants (worst +0.24 / +3.39).
- S(0.3), the share of the excess beyond 0.3 r_ta, is 0.92 / 0.91.

x = 0.23 passes on the full stack but fails the drop-one-bin test (worst +4.05 / +8.47).

Two things weaken this "open". Both are stated in full under "What this does and does not say":
1. x = 1 is not the best fit. Judged against the best grid x (0.5), the smallest x within Δχ² ≤ 4 is **0.4**, where S = 0.83 / 0.81. This reference was reported only, not frozen.
2. KiDS's preference for x comes entirely from bins outside the range Brouwer+21 trust, and through a free two-halo template. Inside 0.3/h Mpc, KiDS cannot tell any x in the grid apart.

The door is open on the frozen criteria. It is not a demonstrated cure for the growth excess.

### Answer to "CFG352's +169: was the two-halo term free?"
**No.** CFG352 scored KiDS with FP1's `kfit(..., W0, Amax = 0.0)`, so its two-halo amplitude was fixed at zero. This lane's A = 0 column reproduces that pattern: x = 0.23 vs x = 1 gives +203 / +199. With a free amplitude, that penalty disappears. CFG352's reading, "the isolated-lens signal needs the law out to about r_ta", follows from the missing two-halo term, not from the data.

## (1) KiDS leg
Model: CFG377's BARE law (CFG100 ν_mono phantom, shell projector, M_d frozen beyond r_on), with r_on = x · r_ta (cfg100 `r_ta_law` per lens group), plus CFG377's free R^−0.8 two-halo amplitude, profiled. Data: CFG377's primary stack (181,477 lenses, 15 bins, 50-patch jackknife, Hartlap 0.67). Typical r_ta is 1.09 Mpc (canonical) / 1.14 Mpc (alt), so x = 0.3 means r_on ≈ 0.33 Mpc.

| x | χ² free 2h (can / alt) | Δχ² vs x = 1 | Δχ² vs best x (reported) | χ² with A = 0 (CFG352-like) |
|---|---|---|---|---|
| 0.23 | 16.88 / 22.52 | −7.62 / −0.92 | +7.94 / +12.75 | 444 / 379 |
| 0.30 | 13.01 / 16.87 | −11.50 / −6.58 | +4.06 / +7.10 | 379 / 315 |
| 0.40 | 9.73 / 11.93 | −14.77 / −11.51 | +0.79 / +2.16 | 325 / 261 |
| 0.50 | **8.95 / 9.77** | −15.56 / −13.67 | 0 / 0 | 290 / 226 |
| 0.70 | 12.65 / 11.92 | −11.85 / −11.52 | +3.71 / +2.15 | 257 / 196 |
| 1.00 | 24.50 / 23.44 | 0 / 0 | +15.56 / +13.67 | 241 / 181 |

- x_min (frozen, vs x = 1) is **0.23 / 0.23**. In the drop-one-bin test the largest x_min is **0.3 / 0.3**.
- With A ≥ 0 enforced, nothing changes: every fitted A is positive.
- **Can KiDS distinguish x? Only weakly, and only through the two-halo model.**
  - In the 9 bins Brouwer+21 trust (R ≤ 0.3/h = 0.445 Mpc), |Δχ²| ≤ 1.1 for every x. The data cannot tell x apart there.
  - The whole preference comes from the 6 outer bins (0.58–2.17 Mpc), where the free template carries 43–88% of the model.
  - Even at x = 1 the template carries 40% / 34% of the model at 0.44 Mpc.
  - The R^−0.8 amplitude has no external prior. A smaller r_on is traded against a larger "two-halo" amplitude: A rises from 1.12 to 1.57 (canonical).
  - Pinning x needs a two-halo/environment model for isolated lenses that is fixed independently, for example from the isolation criterion and mocks.
- f30 strict isolation (reported only) gives the same ordering: Δχ² vs x = 1 is −22 to −26 for x = 0.23–0.5.
- K1 / K2: x = 0.4 reproduces CFG377's 9.733 / 11.935 with the free two-halo term and 325.49 / 261.19 with none, to 0.0000.

## (2) Growth leg
Input: CFG410's BASE z0 snapshots, with CFG412's machinery. There are 4,252 (canonical) / 4,277 (alt) resolved peaks (r_ta,c ≥ 2 cells); median r_ta,c is 1.91 Mpc/h. S(x) is the T1-weighted RES excess source lying beyond x · r_ta,c of every resolved peak.

| x | S(x) can / alt | S_fil | Xhat = X_CFG410 · S_fil (**estimate**) | T1-ON mass beyond | volume IN |
|---|---|---|---|---|---|
| 0.23 | 0.959 / 0.952 | 0.986 / 0.983 | 0.88 / 0.85 | 0.80 | 0.06% |
| 0.30 | **0.922 / 0.911** | 0.951 / 0.946 | 0.85 / 0.81 | 0.70 | 0.12% |
| 0.40 | 0.825 / 0.811 | 0.853 / 0.844 | 0.76 / 0.73 | 0.57 | 0.28% |
| 0.50 | 0.650 / 0.635 | 0.678 / 0.668 | 0.60 / 0.57 | 0.41 | 0.62% |
| 0.70 | 0.437 / 0.428 | 0.433 / 0.427 | 0.39 / 0.37 | 0.31 | 1.3% |
| 1.00 | 0.201 / 0.196 | 0.163 / 0.159 | 0.15 / 0.14 | 0.21 | 3.6% |

- The x = 1 row reproduces CFG412's ceiling: K3 gives 0.8051 / 0.8110 inside, against D2's 0.805 / 0.811.
- **Most of the excess source sits in the 0.5–1 r_ta infall shells of resolved hosts.** About 45% of it lies between 0.5 and 1 r_ta. Those shells are exactly what KiDS, with a free two-halo term, does not require to be ON.
- Sensitivity (reported only): with resolved ≥ 1 cell, S(0.3) is 0.90 / 0.89. With ≥ 3 cells it is 0.94 / 0.93.

## Pre-declared verdict table
| x | KiDS Δχ² ≤ 4 (both) | robust to drop-one-bin | S ≥ 0.60 (both) | |
|---|---|---|---|---|
| 0.23 | yes | **no** | yes | — |
| **0.30** | yes | yes | yes (0.92 / 0.91) | **OPEN** |
| 0.40 | yes | yes | yes (0.83 / 0.81) | OPEN (also passes vs best x) |
| 0.50 | yes | yes | yes (0.65 / 0.64) | OPEN (best fit; marginal S) |
| 0.70, 1.0 | yes | yes | no | — |

## Confirming PM run (specified, NOT run)
- **Run.** CFG410 engine `cfg410_pm.py RES FLAT {canonical,alt} N 3.0 MIXA` with one change. Each step, the switch f is multiplied by IN(x):
  - IN(x) is the union of the balls |cell − c| ≤ x · r_ta,c around every resolved peak c;
  - the peaks and radii come from CFG412's first-crossing turnaround machinery, recomputed from the CIC density each step.
  - Primary x = 0.4, which passes against both references. Secondaries are x = 0.3 and 0.5.
- **Resolution requirement.** At 256³, x = 0.4 of the median resolved host is 0.98 cells, so IN is just the peak cell.
  - The run must therefore be done at **512³** (CFG411b's convergence setting) at minimum, where 0.4 r_ta is about 2 cells.
  - A sub-mesh, particle-level IN assignment is an alternative.
- **Gates.**
  - CFG361 GROWTH OK on both footings: |σ₈ ratio − 1| ≤ 5% and max_{k ≤ 1} |P − 1| ≤ 10%.
  - A MUTATE run at x = 1 must reproduce BASE's TENSION.
  - The KiDS leg of this lane must be re-scored with the same x.

## What this does and does not say (caveats)
- **The two-halo degeneracy is the whole result.**
  - KiDS allows a small ON radius only because a free R^−0.8 term with no prior absorbs the outer signal.
  - At x = 0.3 that term carries 44% / 39% of the model at 0.44 Mpc and 65% / 60% at 1 Mpc.
  - Whether a real two-halo term for isolated lenses is that large has not been tested here. If it is smaller, x is pushed back toward 1 (A = 0 gives +138 at x = 0.3).
- **x is a new declared constant.** CFG412's B1 cover at x = 1 has 0 new constants. Any x ≠ 1 adds one, against the zero-knob standard. It is also not derived, and the peak-anchored IN(x) has no written smooth action (legality CONDITIONAL, as B1).
- **Resolution.**
  - KiDS lenses (r_ta ≈ 1 Mpc) are below the 0.78 Mpc/h mesh, and resolved peaks are group/cluster hosts.
  - S(x) is an upper bound: unresolved galaxy hosts in BEYOND cells would also need the law ON.
  - For x ≤ 0.4 the balls are at most one cell for typical hosts. So S(0.23–0.4) is set by the mesh: at x = 0.05 (MUTATE), S is still 0.97.
  - The ON fraction of r_ta is assumed independent of mass, from galaxies to groups.
- **Xhat is a linear-response estimate, not a PM result.** It uses one 256³ snapshot per footing at z = 0, and CFG411b shows the excess grows with resolution.
- **Standing rules.** κ = ½ is fitted. The footings are 9.3603e-11 and 1.1312e-10, never pooled. The cold mass is still required, and no particle species is added. Nothing here says the data favour the framework, and no front is closed.

## Run
```
nice -n 15 python3 campaign_fresh_gravity/CFG413_on_radius_kids_vs_growth/cfg413_kids.py                     # rc 0, ~90 s
nice -n 15 python3 campaign_fresh_gravity/CFG413_on_radius_kids_vs_growth/cfg413_growth.py                   # rc 0, ~20 s
CFG413_MUTATE=1 nice -n 15 python3 campaign_fresh_gravity/CFG413_on_radius_kids_vs_growth/cfg413_kids.py     # rc 0, DETECTED
CFG413_MUTATE=1 nice -n 15 python3 campaign_fresh_gravity/CFG413_on_radius_kids_vs_growth/cfg413_growth.py   # x = 0.05 reported
```
Inputs (read-only): `real_research/data/lensing_rar/` (CFG377's files), `../_external_data/cfg410_work/cfg410_RES_Rc3_MIXA_FLAT_{canonical,alt}_N256_z0.npz`.
