# CFG498: the clock taper with a capped, mass-conserving draw. NOT RECONCILED (both versions)

Criteria: `FROZEN_CRITERIA.md` (d9c739010, committed alone before any script). κ = ½ is FITTED; ν_mono; both footings
(9.3603e-11 / 1.1312e-10), never pooled; a0 flat. "Cold energy" = the cold clumping component: its mass is still required,
with no particle species. Nothing here closes the clash or the theory.

**The object.** V1's (or V2's) settling-clock taper m(r) supports the law out to the turnaround radius, with no edge.
CFG424's per-catchment mass conservation is kept: the excess is drawn from the same catchment's cold energy, in proportion
to its local density. The draw is capped by what the catchment holds: e → e / max(1, q_raw) and comp = min(1, q_raw) s_c.

## Verdict (frozen rule)

| leg | V1: cold-energy clock (MS1 EXCEPTION) | V2: baryon clock (strict MS1) |
|---|---|---|
| (a) growth 256³, CFG361 cuts (can / alt) | **TENSION / TENSION**: σ8 0.9972 / 0.9968, max\|P−1\| 0.174 / 0.201 (P(k = 1) 0.826 / 0.799) | GROWTH OK / OK: 1.0030 / 1.0039, 0.018 / 0.020 |
| MUTATE-N (no compensation, no cap) | TENSION (σ8 1.068, max\|P−1\| 0.262, P(k = 1) 1.226): **detected** | (same control) |
| (b) KiDS, χ² − CFG413 best ≤ 4 | PASS: +2.05 / +0.71 | **FAIL: +6.17 / +11.06** |
| (c) SPARC, CFG346 clauses | PASS (A3 1.00 / 1.00, Δrms 0, both footings) | PASS |
| (d) early-type levels (reported) | OK: Δχ² vs CFG95 law −0.08 / −0.09 (CFG485's edge model was +27.9 / +35.2) | OK: −0.05 / −0.08 |
| under original MS1 | NOT ADMISSIBLE | admissible |
| **verdict** | **NOT RECONCILED (growth)** | **NOT RECONCILED (KiDS)** |

The 512³ run was not made: no version passes (a), (b) and (c) together. (No other 512³ job was running when the
analysis ran.)

**Bottom line.**
- The cap does what it says, but it does not fix growth.
  - It binds on 26% / 52% of catchment mass in V1, and after it no catchment is overdrawn (q ≤ 1.000; comp ≤ s_c exactly).
  - Yet P(k = 1) moves from 0.8259 (cap removed) to 0.8261 (capped).
  - So the −17% / −20% small-scale deficit is NOT caused by overdraw. That is the mental-estimate risk named in the
    criteria, now confirmed.
- On real galaxies the cap is inert.
  - V1's draw is q_raw = 0.76-0.79 of the catchment's cold energy for every KiDS lens group and every SPARC galaxy.
  - So (b), (c) and (d) reproduce CFG487's "switch only" rows exactly.
- The clash survives in a sharper form.
  - The clock that lensing wants (V1, a broad taper) is the one whose support, drawn in proportion to cold density,
    removes small-scale power in the PM.
  - The clock that growth tolerates (V2, which latches on only 15% of the PM mass) is too compact for KiDS.

## What the growth runs show (256³, seed 359, against CFG359 S0)

| run | σ8 ratio | max\|P−1\| | P(0.1 / 0.3 / 1) | cap binds (catchment mass) | verdict |
|---|---|---|---|---|---|
| V1-CAP canonical | 0.9972 | 0.1739 | 1.008 / 0.991 / 0.826 | 0.263 (q_raw max 2.01) | TENSION |
| V1-CAP alt | 0.9968 | 0.2007 | 1.010 / 0.989 / 0.799 | 0.518 (q_raw max 2.30) | TENSION |
| V2-CAP canonical | 1.0030 | 0.0181 | 1.006 / 1.008 / 0.982 | 0 (q_raw max 0.68) | GROWTH OK |
| V2-CAP alt | 1.0039 | 0.0203 | 1.007 / 1.010 / 0.980 | 0 (q_raw max 0.82) | GROWTH OK |
| MUTATE-N (no comp, no cap) | 1.0679 | 0.2620 | 1.099 / 1.178 / 1.226 | n/a | TENSION (detected) |
| MUTATE-U = C1 (cap removed) | 0.9972 | 0.1741 | 1.008 / 0.991 / 0.826 | overdraw 0.263, q 2.01 | TENSION; bit-identical to CFG487 V1-CATCH |
| MUTA-CAP (FRW-firing clock, reported) | 0.9873 | 0.3510 | 1.005 / 0.963 / 0.649 | 0.915 | TENSION |

- **The compensation's shape swings the small scales.**
  - With no compensation (MUTATE-N), P(k = 1) is +23%. With proportional compensation it is −17%, capped or not.
  - The more support the switch has, the larger the deficit: V2 (latched mass 0.15) −2%; V1 (0.61) −17%; FRW-firing
    (1.00) −35%.
  - **Interpretation (not verified by a separate run):** e sits where s_ph > s_c, in catchment outskirts. The draw
    comp ∝ s_c is concentrated in cores. So mass moves outward and flattens halos. With CFG424's edge, e sits in about
    one cell at the peak, so the same rule moves mass inward and is small (q ≤ 0.30).
- **The clock history matters once there is no edge.** The FRW-firing control is much worse than V1 (−35% vs −17%).
  This is unlike CFG487's edge runs, where the MUTATE was not detected.
- **V2's growth pass is not V2's lensing object.** The PM's V2 clock reads MIX-A-filtered baryon flow and latches only in
  the largest hosts. The analytic V2 used for KiDS and SPARC reads point-mass baryons. This difference carries over from
  CFG487. Also, MUTATE-N runs with the V1 clock, so it shows the leg can see a confinement failure, not V2's clock.

## KiDS and SPARC (analytic, `cfg498_data.py`)

| row | KiDS χ² − best (can / alt) | χ² − (x = 1) | χ², 2h frozen at CFG495's A = 0.07 | SPARC |
|---|---|---|---|---|
| CFG413 best (x = 0.5) | 0 / 0 | −15.6 / −13.7 | 260.05 / 199.6 | (n/a) |
| V1 capped (= uncapped, = outer-first) | **+2.05 / +0.71** (A 1.27 / 1.11) | −13.5 / −13.0 | 258.8 / 198.2 | PASS |
| V2 capped (= uncapped) | **+6.17 / +11.06** (A 1.56 / 1.45) | −9.4 / −2.6 | 400.8 / 350.8 | PASS |
| MUTATE: FRW-firing clock, capped (m ≈ 1 to r_ta) | +21.3 / +18.9 | +5.7 / +5.3 | 315.0 / 254.7 | FAIL: dwarfs A3 0.645 / 0.491 (canonical Δrms +0.0096) |

- **The cap is inert.** Its numbers:
  - V1 q_raw: median 0.763 (KiDS), 0.790 (SPARC), max 0.792.
  - V2 q_raw ≤ 0.38.
  - The cap binds for 0 of 1,953 lens groups and 0 of 171 galaxies.
  - The consistency check M_b + M_ph,law(<r_ta) = M_ta holds to 5e-13.
- **With m ≡ 1 to r_ta, the law would overdraw on every object, by q = (1 − M_b/M_ta)/(1 − f_b) ≈ 1.18.**
  - The MUTATE row shows this: the cap binds for 100% of objects.
  - The uniform cap then cuts dwarf velocities at R_HI by up to 0.03 dex and fails SPARC.
  - So on real galaxies it is the clock's taper that keeps the lensing mass under the cold supply.
- **With the two-halo term frozen at CFG495's A_equiv = 0.07, every model fails** (χ² 198-401 for 15 bins), including
  CFG413's best.
  - The KiDS pass rests on CFG413's free R^−0.8 amplitude, A 1.1-1.3, which is inside CFG486's range.
  - CFG495's own test (in progress in another session) is where the frozen two-halo term is scored. This lane only
    reports it.
- **The (d) early-type leg is weak.**
  - K1 covers R ≤ 0.3 Mpc, where the taper is about 1. So any model without the 5.85 r_M edge matches CFG95's law there.
  - The FRW-firing MUTATE also gives "OK" (−0.30 / −0.40). So (d) shows only that dropping the edge removes CFG485's
    caveat-2 failure (30.5 / 38.1). It is not a test of the clock.

## Controls

- **C1** passes. MUTATE-U reproduces CFG487 POST-HOC V1-CATCH canonical bit for bit (σ8 0.997150, max|P−1| 0.174095;
  identical P(k) arrays).
- **C2** passes:
  - CFG413's x = 0.5 / 1.0 χ² are reproduced to 0.00000.
  - The uncapped KiDS rows equal CFG487's switch-only rows to 0.00000.
  - The SPARC rows are equal exactly.
- **C3** passes: |Σsrc| / Σ|e| ≤ 1e-8 at every snapshot of every CAP run, and min (s_c − comp)/s_c = 0.000.
- **C4** passes: CFG485's machinery reproduces its committed R8 B1 χ² exactly.
- **C5** passes: m stays in [0, 1] and never decreases on any particle, in all 7 runs.
- **MUTATE** (data, FRW-firing clock): the V1 KiDS χ² moves by +19 / +18. Detected.

## Deviations and disclosures

- **Not blind.**
  - CFG487's POST-HOC V1-CATCH result (TENSION) was known before the criteria. MUTATE-U is therefore a reproduction,
    not a blind control.
  - The criteria stated in advance that the cap was likely inert analytically and might not cure the PM deficit. Both
    happened.
- **The interpretation of the growth deficit (outward redistribution) is reasoning, not a measured profile.** No
    post-hoc run was made to test it.
- **The engine copy adds only the CAP branch.** It is CFG487's file with the cap lines, env names and the work directory
  changed. With the cap off, it is bit-identical to CFG487's CATCH (C1).
- **The in_cover peak finder still carries T1's ε = 0.077 in its peak threshold** (inherited, as in CFG424/CFG487).
- **Legality is not re-derived.** CFG487's suffix applies: V1 conversion is CONDITIONAL, V2 over-couples gas, and an
  irreversible ratchet has no fully legal ordinary action (CFG349). The catchment is bilocal.

## Compute

- 7 PM runs at 256³, each 1,457-2,018 s at 3 threads, nice 10, two at a time (6 threads). That is 11,878 run-seconds, about
  3.3 h of run time and about 2 h of wall time.
- One 64³ smoke test (27 s; output deleted).
- Data legs 113 s + MUTATE ~110 s; early-type leg 111 s + MUTATE ~110 s (1 thread each).
- Large arrays live in `../_external_data/cfg498_work/` and are not committed. Local compute only; nothing was downloaded.

## Run

```
python3 campaign_fresh_gravity/CFG498_clock_taper_capped/run_498.py 256
nice -n 10 python3 campaign_fresh_gravity/CFG498_clock_taper_capped/cfg498_data.py                    # rc 0
CFG498_MUTATE=1 nice -n 10 python3 campaign_fresh_gravity/CFG498_clock_taper_capped/cfg498_data.py
nice -n 10 python3 campaign_fresh_gravity/CFG498_clock_taper_capped/cfg498_early.py                   # rc 0
CFG498_MUTATE=1 nice -n 10 python3 campaign_fresh_gravity/CFG498_clock_taper_capped/cfg498_early.py
python3 campaign_fresh_gravity/CFG498_clock_taper_capped/cfg498_growth_analysis.py                    # rc 0
CFG498_MUTATE=1 python3 campaign_fresh_gravity/CFG498_clock_taper_capped/cfg498_growth_analysis.py    # rc 1 (MUTATE-N detected)
python3 campaign_fresh_gravity/CFG498_clock_taper_capped/cfg498_verdict.py
```

κ is fitted; the footings are never pooled; the cold energy's mass is still required. Nothing here says the data favour the
framework.
