# X59_formation_epoch_switch: deciding retention at the collapse epoch does not give the non-monotone pattern. Dwarfs collapse too late on EPS, and L* galaxies inherit their progenitors' cold dark energy

Criteria and ledger: `FROZEN_CRITERIA.md` + `ASSUMPTION_LEDGER.md` (6c7210abf1, committed alone).
- A1 (19ca1d6368) is an implementation fix, made before any graded number: the Monte Carlo uses the continuity
  correction for a barrier that is checked only at discrete steps.
- A2 (8a9a12b286) is the coordinator's band gate. It arrived after the first graded numbers and is reported post-hoc.

κ = ½ FITTED. Footings never pooled. Cold dark energy is not matter. Not "theory closed". Nothing here says the data favour
the framework.

**Hypothesis FE.** An object keeps cold dark energy only if ηΣ_coll(M, z_c) > a₀(z_c)/(2πG) at its own EPS collapse
epoch z_c. Here a₀(z) = a₀·F(z), with F the M-DEC curve (primary) or flat (variant). An object that is not retained does
not take its cold dark energy into the collapse: the component is not heated and not converted, it stays at background
density, and the object follows the law on its baryons. Retained content stays bound through mergers. This is the
frozen "sticky" reading, because FE supplies no unbinding energy.

## Verdicts

- **Frozen §2** (primary: X48 3-seed ng 48 c_f, with M-DEC): **FE FAILS BY EARLY CAPTURE (galaxy progenitors keep too
  much)**, on both footings. R1 passes. The pattern also misses on SPARC and on all five dwarf classes.
- **A2 band gate** (c_f = 4, with M-DEC; post-hoc): **FE BAND GATE FAILS (dwarfs, L\*)**, on both footings. It also
  fails in every variant: c_f 4 with flat F, X48 3-seed, and X48 A2 nine-seed, each with M-DEC and with flat F.

## The non-monotone question (dwarfs retain, L* excluded, clusters retain)

A2 band gate. The mass grid runs at z_obs = 0 in 0.05 dex steps. The ratio is ηΣ_coll / Σ_a₀(z_c).

| footing, c_f / F | dwarfs 10⁸–10¹⁰ retained (ratio) | same at z_c = 8 | L* 10^11.35–12.05: self-retained / f_EC (f_max) | ≥10¹³ retained |
|---|---|---|---|---|
| canonical, **4 / M-DEC** | **0.00** (0.09–0.31) | 1.00 (1.87–8.67) | **0.00** / **0.81–0.97** (0.196) | 1.00 (1.63–4.65) |
| canonical, 4 / flat | 0.00 | 0.95 | 0.00 / 0.72–0.97 | 1.00 |
| canonical, X48 3-seed / M-DEC | 0.00 | 1.00 | 1.00 / 1.00 | 1.00 |
| canonical, X48 A2 nine-seed / M-DEC | 0.15 (0.35–1.17) | 1.00 | 1.00 (2.53–3.65) / 1.00 | 1.00 |
| alt, **4 / M-DEC** | **0.00** (0.08–0.25) | 1.00 (1.55–7.18) | **0.00** / **0.71–0.90** (0.027) | 1.00 (1.35–3.85) |
| alt, 4 / flat | 0.00 | 0.83 | 0.00 / 0.58–0.86 | 1.00 |
| alt, X48 3-seed / M-DEC | 0.00 | 1.00 | 1.00 / 1.00 | 1.00 |
| alt, X48 A2 nine-seed / M-DEC | 0.00 (0.29–0.97) | 1.00 | 1.00 (2.09–3.02) / 1.00 | 1.00 |

What the table shows:
- **Groups and clusters retain** in every case.
- **Dwarfs fail the gate.** On the record's own EPS, a 10⁸–10¹⁰ M☉ halo has its median half-mass formation at only
  z_c ≈ 1.3–1.7. The EPS σ(M) is too flat at low mass for dwarfs to collapse early. So Σ_coll is 3–10 × below the
  threshold at c_f 4.
  - Dwarfs would retain only if their collapse epoch is X51's cooling epoch, z_c = 8 (the reported variant).
  - Even then it holds only with M-DEC F(8) ≈ 0.48, or with the native c_f.
  - With c_f 4 and flat F the ratio at z_c = 8 is 0.94 / 0.78, so the lightest dwarfs fall back under the threshold.
- **L* galaxies themselves are excluded at c_f 4.** Their ratio is 0.55–0.98, so the re-keyed reading would pass this
  band.
- **But L* galaxies assembled 58–97 % of their mass through progenitors that did satisfy FE when those progenitors
  collapsed.** This is EPS merger-history Monte Carlo, 20 000 walks per host. Under FE's own terms (no heating, no
  conversion) that content stays bound. The amount is 4–5 × X22's Υ-window tolerance on canonical and 20–35 × on alt.
- **The native c_f (either X48 table) does not exclude L* galaxies at all.** At those concentrations the galaxies
  themselves sit above the threshold, with ratio 1.1–3.7.

**So the formation-epoch key does not reproduce the non-monotone pattern under any c_f or F.** Two things would be needed
together:
1. a collapse epoch for dwarfs earlier than EPS gives (the cooling epoch, z_c ≈ 8);
2. a way to strip early-captured cold dark energy from L* galaxies.

Item 2 is exactly the late non-gravitational energy source that X22 found is missing. FE's own "no heating" rule forbids
it.

## Frozen §2 detail (primary: X48 3-seed c_f, M-DEC)

| | canonical | alt |
|---|---|---|
| SPARC retained | 97/175 (0.55) | 74/175 (0.42) |
| groups | 63/63 | 63/63 |
| cluster cells | 652/652 | 652/652 |
| dwarfs, all 5 X51 classes (EPS z_c ≈ 1.6–1.7) | 0 / 82 | 0 / 82 |
| dwarfs at z_c = 8 (UFD / bright M31 / M31 others / MW classical / LG field) | 1.00 / 0.76 / 1.00 / 0.62 / 0.38 | same |
| **R1 forest, M_hm 4.89e9 at z 2 / 2.5 / 3** (ratio) | retained (2.06 / 2.71 / 3.48): PASS | retained (1.70 / 2.24 / 2.88): PASS |
| m_FE(z_obs = 0 / 1 / 2 / 3) | 10^10.79 / 9.56 / 8.61 / 7.88 | 10^11.12 / 9.86 / 8.90 / 8.15 |
| **f_EC, median SPARC galaxy** (log M200 10.88) | **1.000** (the galaxy itself retains) | **0.941** |
| f_EC, MW (log M200 11.88) | 1.000 | 1.000 |
| X22 f_max | 0.196 | 0.027 |

**c_f 4 variant (§2 classes).**
- **R1 fails at z = 2.**
  - M-DEC: ratio 0.99 canonical, 0.82 alt.
  - Flat: R1 fails at z 2 and 2.5 on canonical, and at all three redshifts on alt.
- **Early capture still fails.** The median SPARC galaxy's f_EC is 0.687 / 0.527 (canonical, M-DEC / flat) and
  0.585 / 0.390 (alt). Galaxies are retained at 0.11 (canonical) and 0.01 (alt).
- **The tension.** A c_f that lets the forest-scale cold dark energy survive at z 2–3 also sends most of a galaxy's
  progenitors through capture. A c_f that excludes the galaxies breaks R1 at z ≈ 2. No c_f does both.

**Contradiction quantified, question (b).**
- Early-captured cold dark energy in galaxy progenitors is 0.39–1.00 of the fair share for the median SPARC galaxy,
  across every variant.
- The MW's progenitors capture 0.79–1.00.
- X22's tolerance is 0.196 (canonical) and 0.027 (alt).

## Checks and MUTATE

**Normal run: 8/8, exit 0.**
- **K0:** X41 table exact; η 14.83.
- **K1:** FE with flat F at z_obs 0 equals X43's flag in 3888/3888 cases.
- **K1b:** crossover 10^12.093 / 10^12.429. The X48 3-seed crossover is 10^10.835 / 10^11.157, matching X58.
- **K2:** M-DEC equals CPL to 2e-16.
- **K3:** EPS at z_obs 0 equals X41's.
- **K4:** Monte Carlo vs analytic: 0.7393 / 0.7375, 0.5968 / 0.5922, 0.8071 / 0.8071 (after A1).
- **K5:** X51's M200 reproduced to 1e-15.
- **K6:** peak RSS 0.84 GB.

The first A1 run failed K6 at 1.21 GB. A2 re-blocked the Monte Carlo (the random stream is identical, and every graded
line is unchanged by diff).

**MUTATE runs.**
- `X59_MUTATE=reverse`: K1 fails (3888 mismatches), exit 1.
- `X59_MUTATE=a0x10`: K1 fails (3028 mismatches) and K1b fails (no crossover), exit 1.

## Caveats (ledger)

- **η below 10¹² M☉ is an extrapolation** under either X48 table (held flat).
- **The EPS formation epoch is a median.** Early-forming dwarfs in the tail are not modelled.
- **EPS merger fractions are accurate only to tens of %.** The early-capture excess is 2–35 ×, far larger than that.
- **EM1's M200 relation carries a ΛCDM concentration** (A8).
- **Growth uses background A, while a₀(z) uses M-DEC** (A7).

## Files

`FROZEN_CRITERIA.md`, `ASSUMPTION_LEDGER.md`, `AMENDMENT_A1.md`, `AMENDMENT_A2.md`, `x59_fe_switch.py`, `.out` /
`_results.json`, `_MUTATE_reverse`, `_MUTATE_a0x10`, `x59_x30_machinery*.log`.

    PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x59_fe_switch.py                      # exit 0, 8/8
    X59_MUTATE=reverse PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x59_fe_switch.py   # exit 1, K1 fails
    X59_MUTATE=a0x10   PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x59_fe_switch.py   # exit 1, K1 + K1b fail
