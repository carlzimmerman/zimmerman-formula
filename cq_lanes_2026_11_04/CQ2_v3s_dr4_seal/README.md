# CQ2_v3s_dr4_seal: NEWTONIAN (SCREENED). v3s predicts Newtonian Gaia DR4 wide binaries: the frozen pipeline returns Newton's γ_inf (1.0019 / 1.0100), NOT SEPARABLE from Newton, SEPARABLE from plain QUMOND (1.1494 / 1.2081). SEALED, SHA-256 1d65509dbf

κ = ½ FITTED; not theory closed. Footings 9.3603e-11 / 1.1312e-10 m/s², never pooled. No particle, no separate cold
sector. A prediction, not a result; nothing here says the data favour the framework. Status: **complete** (criteria
532e0dc567; scripts, runs, seal and this README in the next commit).

## Question

What does v3s (the khronon plus the switched stiffness −(γ_L/2)[max(D·P, 0)]², L★ ≥ 21.682 / 22.849 pc) predict for
Gaia DR4 wide binaries, pushed through the frozen DR4 pipeline and sealed before DR4 (due about 2026-12-02)?

## Why v3s binaries are screened (derived, not assumed)

1. **The switch is on the stiff side.** v3s equals v3 wherever D·P ≥ 0 (Lean `switched_agrees_where_screened`). From
   X3's D2 rows: the Galactic phantom is ≥ +0.0055 / +0.0062 M☉/pc³ over R 7.2–9.2 kpc, |z| ≤ 1 kpc, and a point mass's
   own negative lobes sit at 33–226 pc and are at most 3.1e-7 M☉/pc³ deep per M☉. For M_tot 2.5 M☉ the margin is
   ≥ **7.06e3** (line 10); the near zone is positive (+0.0449). So every DR4 binary sits where v3s's binary is v3's.
2. **The Galactic field does not lift the screening.** Linearising the static equation about the uniform Galactic
   background (x_e = g/a₀ ≈ 1.6–2.5), the binary's own Newtonian field is cancelled inside χ = Φ + (L★²/2)∇·p by the
   stiffness; what is left is the hedgehog GM/L★² r̂, so the expansion parameter is ε = (GM/L★²)/(a₀x_e/(1+x_e)) ≤
   **1.2e-5** at 2.5 M☉, not g_N/g_e. The kernel χ = m/(1 − m + (kL★)²m/2) → 2/(kL★)² for kL★ ≫ 1 + x_e, independent
   of the field: g ≈ 2a₀ changes only F at the 1 % level.
3. **Two bodies.** The kernel is even in k̂, so no self-force; each star feels the other's monopole response, so the
   relative anomalous acceleration is G M_tot F(r/L★)/L★² and γ_r − 1 = (r/L★)² F, independent of mass.
4. **Motion.** At β = 0 (v3s) a binary moving through the khronon frame carries no hedgehog (X15): γ_r ≡ 1. Either way
   the binary is Newtonian.

## Numbers (primary field 1.9e-10 m/s², L★ floor)

| | canonical | alt |
|---|---|---|
| γ_r − 1 at 1 / 10 / 30 kAU (any M_tot 0.5–2.5) | 5.0e-8 / 5.0e-6 / 4.45e-5 | 4.5e-8 / 4.5e-6 / 4.01e-5 |
| analytic (s/L★)² at 30 kAU | 4.50e-5 | 4.05e-5 |
| F on the sealed grid (all three fields) | 0.9876–0.9996 | 0.9894–0.9997 |
| DR3 Q_pred V3S (z) | −0.001018 (+0.08, CONSISTENT) | −0.003007 (+0.15, CONSISTENT) |
| Q(V3S) − Q(Newton) | +2.5e-7 | +4.8e-9 |
| pipeline γ_inf V3S (spread) | 1.0019 (0.0200) | 1.0100 (0.0068) |
| paired γ_inf V3S − Newton, 4 realisations | 0, 0, 0, 0 | 0, 0, 0, 0 |
| V3S vs plain (dQ/0.020, dγ/0.028) | 2.62, 5.27 → SEPARABLE | 2.86, 7.08 → SEPARABLE |
| V3S vs Newton | 0.0000, 0.0000 → NOT SEPARABLE | 0.0000, 0.0000 → NOT SEPARABLE |

The pipeline's γ_inf for Newton is 1.0019 / 1.0100, not 1, because of its 30,000-binary draws; V3S is fitted on the same
draws, its bin medians move by at most 3.4e-5, and the fit (grid step 0.0025) returns the identical value every time.
L★ = 24 / 50 / 90 pc give 3.6e-5 / 8.4e-6 / 2.6e-6 at 30 kAU. The anisotropic part is ≤ 1.7e-7 of Newton at 30 kAU.

## Checks

K1 C6's 24 wide-binary numbers reproduced exactly (0.0 rel); K2 CW1's DR3 Q_obs, σ, Newton and plain Q exactly; K3 every
pipeline realisation of CW1 (Newton, plain, and canonical LOC3/LOC1/E55/HALF) exactly; K4 margin 7.06e3; K5 ε 1.2e-5; K6
|F − 1| ≤ 0.0124; K7 doubled Route F resolution 2.3e-9 rel, table interpolation 1.5e-7. All PASS.

**MUTATE** (switch inverted, so the stiffness never acts near the binaries; stand-in = CW1's plain QUMOND curve): γ_inf
V3S 1.1631 / 1.2025, Q +0.0514 / +0.0542, SEPARABLE from Newton, NEWTONIAN lines fail, exit 1: **BITES**.

## Disclosures

- Not blind: the record already had γ_v − 1 = 8.1e-6 for 1.5 M☉ at 20 kAU (C6, v3) and "v3s is screened" (X3, the final
  verdict). This lane reproduces C6 and adds the switch margin for binaries, the floor L★, the DR3 Q and the pipeline.
- K3's frozen line asked for CW1's K6 recoveries to 1e-9; CW1 stored them only at 4 printed decimals, so they were compared
  at that precision (5e-5). Every later realisation reproduced to 0.0, which needs the replayed sequence to be exact.
- Written into the code after the criteria and before the first run: beyond r = L★ (no bound binary) the unscreened far
  value c₀ = ½∫m/(1 − m)dc is used. No DR3 orbit draw reaches it (largest r3 2,935 kAU = 14 pc, 0 of 248,400); clipping
  instead gives the same Q. Such far draws carry γ − 1 up to 0.16 (median 1.2e-6) and do not move Q.
- The pipeline separation r for V3S uses √(G M_obs/g_true); the 5 % mass noise moves γ_r − 1 by ≤ 10 % of ≤ 4.5e-5.
- Memory: macOS peak physical footprint 0.37 / 0.35 GB (main / MUTATE); `ru_maxrss` reads 1.53 / 1.56 GB, from the
  pipeline's 1e6 master draw, as in CW1 (1.20 GB there). One thread, `nice -n 10`, 32 s each.
- Nothing in `prep_2026/gaia_dr4_prep/` was edited, run as a script or hashed; its SHA-256 is quoted from CW1's json.

## Files

`FROZEN_CRITERIA.md` (532e0dc567), `cq2.py`, `cq2.out` / `cq2.json`, `cq2_MUTATE.out` / `cq2_MUTATE.json`, `cq2.time` /
`cq2_MUTATE.time`, `cq2_seal.py`, `SEALED_PREDICTION.md`, `SEALED_PREDICTION.sha256`
(`1d65509dbf277fe5884cd66a9ed8702d3d68dde85c608573d02ecdd9f4511ca8`).

Reproduce: `OMP_NUM_THREADS=1 nice -n 10 python3 -I -B cq2.py`, then `... cq2.py --mutate` (exit 1 = bites), then
`python3 -I -B cq2_seal.py`.

κ = ½ FITTED; not theory closed.
