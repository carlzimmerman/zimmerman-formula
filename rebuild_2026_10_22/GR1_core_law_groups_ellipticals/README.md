# GR1_core_law_groups_ellipticals — RESULT: GR1 PREDICTS GROUPS, ELLIPTICALS SHORT (both footings agree)

Frozen criteria + assumption ledger fc3df5bac5 (committed alone; no amendment). κ = ½ FITTED. Footings are graded
separately and never pooled. Cold dark energy, not matter. Nothing here says the data favour the framework or ΛCDM. Not
"theory closed".

**Question.** OS1's core law is X38's route-E Burkert halos with Σ_i = Σ_a0 (σ_i/70.5 km/s)^q. With q fixed once on
SPARC (q_f = 0.892 / 0.748, read from OS1's JSON, **no refit**), does it predict two classes it never saw? The σ convention
is X19's V2, σ_LOS.

## Result (`gr1_groups_ellipticals.out`)

| | canonical (q_f 0.892) | alt (q_f 0.748) |
|---|---|---|
| **groups (63, P4 T3 estimator)**: X38 q = 0 | +0.0973 dex, Z +2.48, ABOVE LAW | +0.0907, Z +2.29, ABOVE LAW |
| groups at q_f | **+0.0767, Z +1.94, CONSISTENT → PASS** | **+0.0740, Z +1.85, CONSISTENT → PASS** |
| **SLUGGS centrals (4, CFG528b tracers, route E)**: q = 0 | mean +0.197, Zc +9.6, 0/4 cleared | +0.182, Zc +8.9, 1/4 |
| SLUGGS at q_f | **+0.127, Zc +6.2, 1/4 cleared → FAILS** (−36 %, the bar is −50 %) | **+0.127, Zc +6.2, 1/4 → FAILS** (−30 %) |
| red KiDS lenses | NOT GRADED (no σ_LOS per lens under V2; criteria §1c) | NOT GRADED |
| **lane class** | **GR1 PREDICTS GROUPS, ELLIPTICALS SHORT** | **GR1 PREDICTS GROUPS, ELLIPTICALS SHORT** |

SLUGGS per galaxy at q_f (offset dex, Z), in the order M87 / NGC 4365 / NGC 4374 / NGC 5846:
- both footings: +0.164 (+9.4), +0.132 (+5.7), +0.071 (+1.0), +0.143 (+6.4).
- the route-E JAM analogue puts M★ at 0.74–0.89 M_JAM. Σ_i/Σ_a0 is 2.9–4.0 (canonical) and 2.4–3.2 (alt).

**Checks 10/10** (exit 0, 31 s, peak RSS 0.71 GB, one thread):
- K0a: SPARC at q = 0 equals X38 to 1e-9.
- K0b: groups at q = 0 equal X40b's X38 row (mean to 1e-6, Z to 1e-4) on both footings.
- K0c: the SLUGGS Jeans machinery reproduces CFG528b row M K0 exactly (0.0 dex).
- K0d: the no-halo groups match P4's integrator.
- K1: SPARC at q_f equals OS1 to 1e-6.
- K2: the JAM-analogue root residual is 6e-14.

**MUTATE** (q → −q_f, `_MUTATE.*`). The groups go to +0.132 / +0.115 (Z +3.39 / +2.92) and SLUGGS to +0.291 / +0.260. Both
shifts are opposite in sign to the real run on both footings, so the tooth bites (exit 1, as frozen).

## Reported only (no class weight)

- **The groups' pass is narrow and comes from the σ level, not the ordering.**
  - Z +1.94 sits against a line of 2.
  - In the self-consistent σ reading (predicted σ fed back into Σ), canonical is Z +2.04, ABOVE LAW. Alt stays at +1.94,
    CONSISTENT.
  - q_f ± 0.05 stays CONSISTENT on both footings (Z 1.83–1.96).
  - Permuting σ across the 63 groups at q_f gives the same Z, +1.94 / +1.86.

  So the groups test only that their *typical* σ (≈ 140 km/s, about 2 σ_ref) earns a Σ about 1.8× higher. The 63 groups
  span too little in σ for the within-class ordering to carry weight. Unlike OS1's SPARC MUTATE, this is not evidence that
  the per-system σ dependence is right.
- **SLUGGS, mass-side readings.**
  - Hot gas added ('bar'): +0.059 / +0.058, 2/4 cleared. M87 and NGC 4374 clear, NGC 4365 (Z +4.7) and NGC 5846 (+9.9)
    do not.
  - Salpeter M★ instead of the JAM analogue: +0.093, 1/4.
  - Self-consistent σ: +0.138 / +0.136.

  No reading reaches PASS.
- **SLUGGS route-E baseline.** Route E at q = 0 (X38 halos, never graded on SLUGGS before) sits at +0.18 to +0.20 dex. That
  is about the same as the law-based record (CFG528b row M K0, +0.18 / +0.17). The core law removes about a third of it.

## What it means

1. **Second out-of-sample class passes.** With one constant fixed on SPARC galaxies, the core law takes the groups from
   ABOVE LAW (Z +2.48 / +2.29) to CONSISTENT on both footings. X38, X40b, X42, X43 and IC1 all failed this line; X43's
   η-floor reached Z +2.05. The margin is thin (Z 1.94), and one reported reading (canonical, self-consistent σ) sits just
   above the line.
2. **Massive ellipticals stay short.** The four SLUGGS centrals have σ_GC ≈ 250–400 km/s, so Σ_i rises 2.4–4×. That is the
   right direction, but only a third of the +0.2 dex excess goes away. The outer GC dispersions want more mass at 30–100
   kpc than an M200(M★)-sized Burkert core at Σ ∝ σ^0.8 supplies.
   - The two strongest misses, M87 and NGC 5846, are host centres. Their Virgo / group halos are omitted by design (the
     isolated reading, disclosed before the run). The hot-gas reading clears M87 but not NGC 5846.
   - So this class is FAILS as frozen. The record cannot yet tell "law short" apart from "host halo missing".
3. **Red KiDS lenses** need a σ convention for lenses and a route-E ΔΣ forward model, and neither exists in the record.
   This is a follow-up, not a result.

## What this does not include or show

- No host halo for M87 or NGC 5846, and no M200 relation calibrated above log M_b ≈ 11.5. The groups and SLUGGS rows are
  extrapolations, as in P4 / X40b / X43.
- The groups' external field is not on disk (P4 caveat). Route E has no EFE, so that caveat does not enter here.
- The SLUGGS σ errors are statistical only (CFG466's bootstrap).

## Run

```
PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 rebuild_2026_10_22/GR1_core_law_groups_ellipticals/gr1_groups_ellipticals.py            # ~30 s, exit 0
PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 rebuild_2026_10_22/GR1_core_law_groups_ellipticals/gr1_groups_ellipticals.py --mutate   # ~30 s, exit 1
```

**Inputs.** All are read only:
- Tian+2026 groups, from `../_external_data/vizier2026/`;
- the CFG528b tracer sources, from `../_external_data/cfg528_work/src/`.

Both sit outside git. Nothing was downloaded. X30's machinery log is redirected to `gr1_x30_machinery*.log`.
