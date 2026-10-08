# CFG501: draw the phantom only from UNSETTLED cold energy. NOT RECONCILED (both versions)

Criteria: `FROZEN_CRITERIA.md` (7b71dd9b5, committed alone before any script). κ = ½ is FITTED; ν_mono; both footings
(9.3603e-11 / 1.1312e-10), never pooled; a0 flat. "Cold energy" = the cold clumping component: its mass is still required,
with no particle species. Nothing here closes the clash or the theory.

**The object.** CFG498's clock taper (λ = 1, no edge) with per-catchment mass conservation, with one change: the draw takes
cold energy that has NOT yet settled. The weight goes from ρ_c to (1 − m) ρ_c, where m is the clock's settled fraction (the
same field that sets the taper). The cap now applies to the unsettled supply: q = Σe / Σ(1 − m)s_c, e → e / max(1, q),
comp = min(1, q)(1 − m)s_c. No new constant.

## Verdict (frozen rule)

| leg | V1: cold-energy clock (MS1 EXCEPTION) | V2: baryon clock (strict MS1) |
|---|---|---|
| (a) growth 256³ (can / alt) | GROWTH OK / OK: σ8 1.0053 / 1.0059, max\|P−1\| 0.024 / 0.027, P(k = 1) 1.014 / 1.014 | GROWTH OK / OK: 1.0060 / 1.0076, 0.041 / 0.053, P(k = 1) 1.034 / 1.044 |
| MUTATE-N (no compensation, no cap) | TENSION (σ8 1.068, max\|P−1\| 0.262): **detected** | (same control) |
| (b) KiDS, χ² − CFG413 best ≤ 4 (free 2h) | **FAIL: +29.45 / +25.71** (A 2.02 / 1.94) | **FAIL: +6.17 / +11.06** (unchanged from CFG498) |
| (c) SPARC, CFG346 clauses | **FAIL: A3 0% / 0%** (spirals and dwarfs), Δrms +0.099 / +0.082 | PASS |
| (d) early-type levels (reported) | "OK" (−1.03 / −1.31), but χ² without two-halo 155 / 141 vs B1's 23 / 14 | OK (−0.05 / −0.08) |
| **verdict** | **NOT RECONCILED (KiDS, SPARC)** | **NOT RECONCILED (KiDS)** |

The 512³ run was not made: no version passes (a), (b) and (c) together.

**Bottom line.**
- The unsettled draw does stop the PM from emptying halo cores, and V1's growth deficit goes away (P(k = 1) 0.826 → 1.014).
- But V1 passes growth because it loses most of its phantom, not because the draw has a better shape.
  - In a V1 catchment most of the cold energy has already settled. In the PM the unsettled share is 13% of the catchment's
    cold energy, so the cap binds on 100% of catchment mass (q_raw up to 40-46). At z = 0, Σ|e| is 15% of the PROP run's.
  - On real objects the same thing happens. q_u = D / C_u is 2.16 (median) for every KiDS lens group and 2.38 for every SPARC
    galaxy, so the cap binds on all of them. The phantom is cut to about 0.46 of the law. That fails SPARC on every galaxy
    and costs +26 to +29 in KiDS χ².
- V2's cap never binds on real objects (q_u ≤ 0.45), so its lensing and SPARC rows are CFG498's exactly. It still fails
  KiDS (+6.17 / +11.06), because the V2 clock is too compact. Its PM growth stays OK, now with a small positive offset
  (P(k = 1) +3-4%, where it was −2%).
- **The clash moves; it does not close.** The settled fraction m that gives V1 its broad lensing taper also leaves little
  unsettled cold energy to pay for the phantom. Draw from all of the cold energy (CFG498), and the cores empty and growth
  fails. Draw only from the unsettled part (this lane), and the supply is too small, so lensing and rotation fail.

## Core-emptying diagnostic (`cfg501_halo_stack.py`, reported)

Stack of the 200 largest S0 halos (σ = 1 cell smoothing, separation ≥ 8 cells; 1 cell = 0.78 Mpc/h). e, comp and src are in
units of the mean cold source.

| run | M / M_S0, r ≤ 1 / 2 / 3 / 6 cells | draw share r ≤ 2 | centre: e / comp / src | e at r = 2 |
|---|---|---|---|---|
| PROP (CFG498 weight; = CFG498 V1-CAP bit for bit) | **0.759** / 0.906 / 0.965 / 1.013 | 0.282 | 28.9 / **285.2** / −256.3 | 25.9 |
| V1-U (unsettled draw) | **1.003** / 1.017 / 1.019 / 1.018 | 0.087 | 0.40 / 4.95 / −4.56 | **4.6** |
| V2-U | 1.011 / 1.035 / 1.033 / 1.017 | 0.142 | 2.09 / 24.9 / −22.8 | 17.7 |
| MUTATE-N (no compensation) | 1.076 / 1.143 / 1.152 / 1.139 | — | 2.62 / 0 / +2.62 | 28.6 |

- **CFG498's reading is now measured, not just reasoned.** With the proportional draw, the halo centre loses 285 units of
  source against a phantom of 29 there. The innermost cell holds 24% less mass than S0. The cumulative src inside r ≤ 1
  is −56% of the S0 cold mass there.
- By the frozen rule, **"the (1 − m) draw stops emptying cores": YES.** V1-U's core mass ratio is 1.017 (PROP 0.906) and its
  draw share inside 2 cells is 0.087 (PROP 0.282).
- But V1-U's phantom at r = 2 is 4.6, against 26-29 with PROP or no compensation. The cores are intact because the phantom
  was cut, not because a full phantom was fed from the outskirts.
- m at the halo centre is 0.99 in V1 and 0.91 in V2. V2's m falls to 0.02 by r = 6, so V2 has unsettled supply nearby, and
  its cap binds on only 2-5% of catchment mass.

## KiDS detail (analytic, `cfg501_data.py`)

| row | χ² − best, free 2h (can / alt) | 2h frozen at A = 0.07: χ² − CFG413 best x under the same treatment |
|---|---|---|
| CFG413 x = 0.5 (free-2h best) | 0 / 0 | +45.0 / +41.3 |
| CFG413 x = 1.0 (frozen-2h best) | +15.6 / +13.7 | 0 / 0 (χ² 215.0 / 158.3) |
| V1 unsettled cap (PRIMARY) | +29.45 / +25.71 | +477.8 / +484.4 |
| V2 unsettled cap (PRIMARY; cap inert) | +6.17 / +11.06 | +185.8 / +192.6 |
| V1 full-supply cap (= CFG498) | +2.05 / +0.71 | +43.8 / +39.9 |

- When the two-halo term is frozen, CFG413's best x moves to 1.0, and every model in this lane is far worse than it.
- Data MUTATE (FRW-firing clock, m ≈ 1 everywhere, so there is almost no unsettled supply; q_u ≈ 3,500): the V1 χ² goes to
  90.9. Detected (> 4 on both footings).

## Controls

- **C1** passes: the PROP run reproduces CFG498's V1-CAP canonical bit for bit (σ8 and P(k) identical at every snapshot).
  **C1b** passes: MUTATE-N reproduces CFG498's MUTATE-N bit for bit.
- **C2** passes:
  - CFG413's x = 0.5 / 1.0 rows are reproduced exactly.
  - The full-supply-cap rows equal CFG498's KiDS, SPARC and early-type rows exactly.
  - The uncapped rows equal CFG487's switch-only rows.
- **C3** passes: |Σsrc| / Σ|e| ≤ 9.1e-9, and comp ≤ (1 − m)s_c exactly (min residual 0).
- **C4** passes: CFG485's R8 B1 is reproduced exactly.
- **C5** passes: m stays in [0, 1] and never decreases, in all 6 runs.

## Deviations and disclosures

- **Not blind.** The criteria (written after reading CFG498) expected that the unsettled supply might bind analytically and
  cut the phantom. That is what happened.
- **The (d) early-type leg is weak, as in CFG498.** V1's "OK" relies on the free two-halo term (A 2.3) absorbing a
  phantom that has been cut in half: its χ² without two-halo is 155 against B1's 23. The FRW-firing MUTATE also gives "OK".
- **"Growth passes because the phantom was cut" is a reading.** It rests on Σ|e| (15% of PROP), the cap binding on 100% of
  catchment mass, and the stacked e profile. No separate run isolates it.
- **The halo stack uses the S0 halo centres, recentred within ±2 cells.** Shells are centred on integer cell distances, and
  the "≤ r" sums include shell r.
- **The analytic unsettled supply assumes the cold energy follows the law's total-mass profile**, as frozen. The in_cover
  peak finder still carries T1's ε = 0.077 (inherited).
- **Thread budget.** For about 1 minute, while the PM workers were running, the data script started as a 7th thread. It was
  killed and rerun after the PM queue had finished. No result depends on it.
- **Legality is not re-derived.** CFG487's suffix applies: V1 conversion is CONDITIONAL, V2 over-couples gas, and the ratchet
  has no fully legal ordinary action (CFG349). The catchment is bilocal.

## Compute

- 6 PM runs at 256³, at 3 threads each, nice 10, two at a time (6 threads):
  - 1,549-1,959 s each; 10,219 run-seconds in total, about 1.6 h of wall time.
- One 64³ smoke test (23 s; output deleted).
- Data legs: 142 s + MUTATE. Early-type legs: about 60 s each. Halo stack: 6 s.
- Large arrays (z = 0 fields) live in `../_external_data/cfg501_work/` and are not committed.
- Local compute only; nothing was downloaded.

## Run

```
python3 campaign_fresh_gravity/CFG501_draw_from_unsettled/run_501.py 256
python3 campaign_fresh_gravity/CFG501_draw_from_unsettled/cfg501_growth_analysis.py                  # rc 0
CFG501_MUTATE=1 python3 campaign_fresh_gravity/CFG501_draw_from_unsettled/cfg501_growth_analysis.py  # rc 1 (MUTATE-N detected)
nice -n 10 python3 campaign_fresh_gravity/CFG501_draw_from_unsettled/cfg501_data.py                  # rc 0
CFG501_MUTATE=1 nice -n 10 python3 campaign_fresh_gravity/CFG501_draw_from_unsettled/cfg501_data.py
nice -n 10 python3 campaign_fresh_gravity/CFG501_draw_from_unsettled/cfg501_early.py                 # rc 0
CFG501_MUTATE=1 nice -n 10 python3 campaign_fresh_gravity/CFG501_draw_from_unsettled/cfg501_early.py
nice -n 10 python3 campaign_fresh_gravity/CFG501_draw_from_unsettled/cfg501_halo_stack.py
python3 campaign_fresh_gravity/CFG501_draw_from_unsettled/cfg501_verdict.py
```

κ is fitted; the footings are never pooled; the cold energy's mass is still required. Nothing here says the data favour the
framework.
