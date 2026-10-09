# CFG515: does the census edge dissolve the growth-vs-lensing clash? PARTLY. Two things stay broken: KiDS on the alt footing, and the Milky Way timing (which now fails the other way)

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (2bbe75602).
- **Scripts:**
  - `cfg515_lib.py` holds the census f_ret and the edge.
  - `cfg515_kids.py` runs (a). About 9 min with 4 workers on a loaded machine.
  - `cfg515_levels.py` runs (b), `cfg515_sparc.py` runs (c) and `cfg515_mw.py` runs (d).
  - `cfg515_verdict.py` runs (e), does the growth bookkeeping and applies the frozen verdict.
  - All of them exit 0 and every control passes.
- **MUTATE:** `CFG515_MUTATE=1` writes the `*_MUTATE.*` outputs. All teeth pass.
- **Settings:** κ = ½ is FITTED. The footings (9.3603e-11 / 1.1312e-10) are never pooled, and a0 is flat. The data are on disk; nothing was downloaded. The cold energy's MASS is still required (no particle). This is not "theory closed", and nothing here says the data favour the framework.

## The question

The PAPER45 edge is r_edge = r_M(M_b,now) / ln(1 + f_ret f_b/(1 − f_b)).
- The PM growth runs never remove baryons, so f_ret = 1 is the self-consistent value inside them.
- CFG485, CFG487 and CFG513 used f_ret = 1 for real galaxies, and they failed.
- This lane scores the consistent picture instead. Each real object gets the census f_ret, and nothing is fitted.

## Census f_ret, fixed before scoring

- **Primary:** CFG416's declared `fret_of(M_ta)`, solved self-consistently against each object's present baryons. It gives 0.10 for KiDS lenses (10–90%: 0.100–0.103), 0.10 for the Milky Way, 0.136 for M31, 0.10–0.23 for SPARC, and 0.86–0.90 for clusters.
- **Bracket:** constant f_ret = 0.07 and 0.18, the "7–18% in the census" spread from PAPER45 v1.0.

## Verdicts (primary census; both footings each)

| test | census result | verdict | bracket 0.07 / 0.18 |
|---|---|---|---|
| (a1) KiDS, CFG413 harness (free two-halo), χ² − best | +3.20 (can) / **+8.84 (alt)**; drop-one-bin +1.75..+4.40 / +7.2..+10.4 | **FAIL** (alt) | PASS (+1.27 / +2.50) / FAIL (+12.2 / +22.0): bracket-sensitive |
| (a2) KiDS, CFG503 environment, inner 9 bins, minus the best frozen model (F_DD 5.24 / 5.66) | inner-9 58.5 / 36.9, so +53.3 / +31.2 | **FAIL** | FAIL / FAIL |
| (b) early-type lensing levels (CFG485 R8), χ² − B1 | 2.50 vs 2.55 / 2.74 vs 2.87, so −0.05 / −0.12 | **PASS** | PASS / PASS |
| (c) SPARC (CFG346 S clauses) | A3 1.00 / 1.00; Δrms 0; no R_HI lies beyond the edge | **PASS** | PASS / PASS |
| (d) MW: LG timing \|z\| ≤ 3 and CFG433 D ≤ 3 | timing v = −168.7 km/s, **z = +13.5**; D +2.89 / +2.52; 2 of 39 satellites unbound | **FAIL** (timing) | FAIL (z +30.7) / FAIL (z +3.1) |
| (e) cluster unsettled fraction u | 0.433–0.628 / 0.368–0.584, exactly the record range | PASS (structurally blind, as declared) | PASS / PASS |

**Frozen verdict: PARTLY** (b and c pass; a and d fail).

## What it means

1. **The census edge repairs most of what f_ret = 1 broke.**
   - Early-type lensing levels go from +27.9 / +35.3 (f_ret = 1) to −0.05 / −0.12. The late types also come back to B1 (−0.08 / −0.21, reported).
   - SPARC alt dwarfs go from A3 0.864 to 1.00.
   - KiDS on the canonical footing goes from +60.5 to +3.2.
   - The MW satellites go from D 4.06 (24 of 39 unbound) to D 2.89 (2 unbound).
   - So most of the record's "clash" on real galaxies came from the f_ret = 1 edge, as hypothesised.
2. **KiDS on the alt footing still fails at the census value, by +8.8.**
   - The census edge sits at x = 0.30 r_ta (alt) against 0.34 r_ta (canonical), lens-weighted median.
   - KiDS with a free two-halo term wants x ≳ 0.4 (CFG413).
   - The lower census end (0.07) passes both footings. So this test is decided by where the census actually sits, which the census spread does not pin down.
3. **The CFG503 environment fails every law-type model in the inner bins, and the edge is not the cause.**
   - The census edge does 2.1 better than the law out to r_ta (LAW_RTA) there.
   - The failure comes from CFG503's stripping of leaked satellites, which removes phantom mass the law needs at 0.1–0.4 Mpc.
   - CFG503's own validation gates (G1, G3) failed, so this environment is not a validated template. Its fail is kept as frozen.
4. **The Milky Way timing now fails the other way.**
   - At f_ret = 1 the MW and M31 carry too little mass: z = −22.8.
   - At census f_ret they carry too much: MW 3.3e12 and M31 4.9e12, an approach of −169 km/s, z = +13.5.
   - At 0.18 the miss is z = +3.1 (known in advance from CFG513 and disclosed in the criteria).
   - Post hoc, not a fit: the timing needs a common f_ret of 0.206. With the MW held at its census 0.10, M31 would need 0.43.
   - The timing alone uses only the 4.4 km/s measurement error. No timing-model systematic is included, so this is strict.
   - Plain reading: the zero-knob census edge makes Local Group galaxies' cold-energy halos too massive, by about 2×.
5. **Clusters are untouched by any f_ret ≤ 1**, as declared.
   - Reported only: with CFG416's group retention values, 14 of 20 groups (b = 0) hold more dark mass inside R500 than the cold share of their original baryons (median x_T 10.8 vs a supply of 10.4).
   - So the declared group retention is slightly too high for the groups' own measured baryon fractions.

## Growth: is f_ret = 1 in the sims consistent with f_ret < 1 for real galaxies?

**It is consistent on the amount and inconsistent on the placement. Whether growth still passes with depletion-consistent placement is OPEN.**

- **Amount (computed, an exact identity).**
  - In the PM, the phantom is sourced by the undepleted baryons M_o and stops at 5.85 r_M(M_o). The settled mass is 5.364 M_o.
  - In a consistent depleted halo, it is sourced by M_now = f_ret M_o and stops at the census edge. The settled mass is 5.364 M_now/f_ret = 5.364 M_o, the same.
  - So the sims do not get the amount of settled cold energy per halo wrong.
- **Placement (computed, `cfg515_verdict.out`).** The real edge lies 2.2× (f_ret 0.18), 2.9× (0.10) and 3.5× (0.07) farther out than the PM edge. Only 45% / 34% / 28% of the settled mass lies inside the PM edge.
- **Growth is sensitive to placement (record).**
  - CFG413: most of the excess source sits at 0.5–1 r_ta.
  - CFG423 MUTATE (f_ret = 0.01, edge ×10): TENSION, 0.139.
  - CFG414's hand-set 0.4 r_ta at 512³: 0.080 / 0.0996.
  - CFG416's census radius with undepleted, uncapped baryons (its phantom is 2.3–3.7× the supply): 0.092 / 0.101.
- **Argued bracket (not computed).**
  - The consistent case keeps CFG424's mass conservation and the same total. It spreads the mass to about 0.3–0.5 r_ta, about where CFG414 confined it by hand.
  - So max|P − 1| should land between CFG424's 0.027 and the 0.08–0.10 of CFG414/416, i.e. at or under the 10% limit. That is an argument, not a result.
- **The essential run (specified, not run).**
  - Take the CFG424 engine (turnaround-catchment compensation). Source the phantom by f_ret(M)·(PM baryons), with f_ret from CFG416's `fret_of`, and set the edge to r_M(M_now)/ln(1 + f_ret f_b/(1 − f_b)).
  - Run at 512³ on both footings with seed 359. Gate it with CFG361's cuts.
  - MUTATE: f_ret ≡ 1 must reproduce CFG425's pass.
  - It was not run here: it is a multi-hour 512³ job, the machine was heavily loaded, and the brief said to avoid new PM jobs unless essential. It is the next decisive step.

## Controls and MUTATE (all pass)

**Controls:**
- K1: the closed-form edge matches the numeric ν_mono root to 5e-9.
- K2: `fret_of` equals CFG416's exactly, and the self-consistency residual is 7e-15.
- K3: the CFG413 x = 0.5 / 1.0 χ² are reproduced to < 0.01.
- K4: re-scoring CFG503's committed tables reproduces all five frozen models to 2e-14.
- K5: CFG485's B1 is reproduced exactly, and its C1–C5 pass.
- K6: the SPARC C3 control passes, and rms0 equals CFG39's.
- K7: CFG513's f_ret = 0.18 cells are reproduced exactly.
- K8: CFG453's x_T medians are reproduced exactly.

**MUTATE M1 (f_ret = 1 on real galaxies) reproduces the record's failures:**
- KiDS: +60.48 / +70.57 (CFG487 +60.5 / +70.6).
- CFG503 EDGE inner-9: 240.86 / 240.65.
- Early-type levels: 30.45 / 38.11.
- SPARC alt dwarfs: 0.864.
- MW timing: z −22.82.
- Verdict NOT DISSOLVED.

**MUTATE M2 (f_ret = 0.01):** it fails (a) (KiDS +15.6 / +13.7, which is the x = 1 row, since the edge is capped at r_ta) and (d) (z +42 / +47). It passes (b) and (c), because there the edge lies beyond the data.

## Caveats

- **Settling and stacking.** The phantom is taken as fully settled inside the edge. CFG485's R5 found 9–14% of late types unsettled at a census edge; that is not modelled. All lensing stacks treat the baryons as point masses with present masses.
- **The census relation.**
  - It is CFG416's declared step-and-ramp, with M_ta defined through f_ret itself. Its 0.10 floor puts nearly all KiDS lenses and the MW at the same f_ret.
  - The literature census values behind it were recalled in CFG416 and not re-verified here.
  - Mapping "baryon fraction relative to cosmic" to f_ret differs by about 8% for groups. This is reported, not corrected.
- **CFG503's environment** failed its own validation gates. The (a2) failure is not specific to the edge.
- **The MW timing** uses static spherical potentials, O-MW ownership and point-mass M31, and the measurement error only (as CFG513).
- **(e)** cannot discriminate any f_ret ≤ 1.

## Run

```
nice -n 15 python3 campaign_fresh_gravity/CFG515_census_edge_resolution/cfg515_kids.py      # 4 workers
nice -n 15 python3 campaign_fresh_gravity/CFG515_census_edge_resolution/cfg515_levels.py
nice -n 15 python3 campaign_fresh_gravity/CFG515_census_edge_resolution/cfg515_sparc.py
nice -n 15 python3 campaign_fresh_gravity/CFG515_census_edge_resolution/cfg515_mw.py
python3 campaign_fresh_gravity/CFG515_census_edge_resolution/cfg515_verdict.py
# then the same five with CFG515_MUTATE=1
```

The inputs are read-only:
- CFG377 / CFG413 / CFG487 / CFG503 KiDS files and tables (`_external_data/cfg503_work`);
- the CFG485 / CFG95 / CFG61 machinery;
- the CFG487 / CFG346 SPARC harness;
- the CFG513 script and the Fritz+18 tex (`_external_data/cfg433_work`);
- CFG453's X-COP / Lovisari objects;
- CFG416's `fret_of`.
