# CFG902: CFG804 rerun with the declared Msun/h ramp. No class changes. Primary still SUFFICES; the all-radii shortfall shrinks by about a third but still FALLS SHORT

**What was done.** CFG886 (T5) found that CFG804 solved the catchment fixed point in Msun, while CFG416 declared its
f_ret(M_ta) ramp in Msun/h. This lane reruns CFG804's own committed script with that one convention fixed. The script is
executed read-only, blob-hash checked, with the frozen replacements R1–R3.
- R1 is the convention: log M_ta[Msun/h] = log M_b − log10(f_ret f_b) + log10 h.
- h = 0.674, CFG416's own conversion value (cfg416_pm.py line 277), so the shift is −0.17134 dex.
- R2 moves CFG804's internal K1 target by the same shift. R3 redirects the outputs into this lane.

Everything else is CFG804 verbatim: data, covariance, profiling, NGRID and classes.
Criteria: `FROZEN_CRITERIA.md` (b35efa722, committed alone before any script).

## Before / after (CFG804's classes: SUFFICES if Δχ²(D_der − B) ≤ 4)

| footing | radii | χ²_B | Δχ² CFG804 (Msun) | Δχ² declared (Msun/h) | change | class before → after | changed? |
|---|---|---|---|---|---|---|---|
| canonical | primary R ≤ 0.31 Mpc | 83.9 | −0.23 | **+0.84** | +1.07 | SUFFICES → **SUFFICES** | no |
| canonical | all radii | 163.1 | +148.69 | **+100.10** | −48.59 | FALLS SHORT → **FALLS SHORT** | no |
| alt | primary R ≤ 0.31 Mpc | 79.7 | −1.51 | **−0.27** | +1.24 | SUFFICES → **SUFFICES** | no |
| alt | all radii | 155.3 | +172.25 | **+123.12** | −49.12 | FALLS SHORT → **FALLS SHORT** | no |

Footings are reported separately and never pooled.

**Derived supply at the new best-fit masses.**
- Canonical: N = 10.0 / 10.0 / 9.4 / 7.1 (primary) and 10.0 / 10.0 / 7.9 / 6.1 (all radii). CFG804 had 10.0 / 8.8 / 7.4 / 5.6
  and 10.0 / 7.7 / 6.4 / 5.2.
- Alt: N = 10.0 / 10.0 / 10.0 / 7.7 (primary) and 10.0 / 10.0 / 9.4 / 6.9 (all radii).
- The edges move from 320–450 kpc (CFG804 canonical; alt 250–420) to **250–570 kpc**: canonical 324–567 kpc, alt 251–509 kpc. Bin 1 sits on
  the f_ret floor in both conventions, so its edge is unchanged.

**At CFG804's own best-fit masses** (the convention effect alone), canonical primary N goes from 10.00 / 8.83 / 7.35 / 5.62
to 10.00 / 10.00 / 9.38 / 6.98. That is +13% / +28% / +24% in bins 2–4, as CFG886 estimated.

## Reading

- **Primary verdict unchanged.** "DERIVED SUPPLY SUFFICES" holds in both footings.
  - Δχ² moves up by about 1 (−0.2 → +0.8 canonical, −1.5 → −0.3 alt). It stays well inside the ≤ 4 threshold.
  - The move is toward slightly worse, even though the supply is larger. Inside 0.31 Mpc the truncated model is not
    monotone in N (presumably because truncation lowers Σ and Σ̄ differently near the edge). CFG804's slightly negative
    Δχ² went with its closer edges. This was not investigated further.
- **All-radii shortfall reduced, class unchanged.** Δχ² falls by about 49 in both footings (+149 → +100, +172 → +123). The
  derived catchment still runs out well short of the 2.6 Mpc reach of the stacked signal.
  - This cannot close by the unit convention alone. The census floor f_ret ≥ 0.10 caps N at 10. CFG803's all-radii demand
    is N_min = 16–24 (quoted in CFG804's criteria).
  - MUTATE confirms this: a deliberately doubled shift still gives +69.4.
- What CFG804 names as next is unchanged: the framework's two-halo term for 0.4–2.6 Mpc.

## Controls (all PASS)

| control | result |
|---|---|
| K1 original convention vs CFG804's committed JSONs (both footings) | every χ², Δχ², p_D and logMb reproduced with max \|Δ\| = 0 (bit-identical); `.out` files byte-identical to `cfg804.out` / `cfg804_alt.out` |
| K2 only D changes | χ²_B identical between orig and declared (\|Δ\| = 0, both footings, both radius sets); CFG804's internal K1/K2 print PASS in all four non-mutate runs |
| K3 declared fixed point | log M_b 10.5 → N 10.000, log M_ta 12.132 Msun/h (target 12.133 ± 0.01); at CFG804's canonical primary masses N 10.00 / 10.00 / 9.38 / 6.98 = CFG886's 10.0 / 10.0 / 9.4 / 7.0 |
| MUTATE (shift 2 log10 0.674 = −0.343 dex, canonical) | (a) at the declared best-fit masses, N rises 10.00/10.00/9.38/7.07 → 10.00/10.00/10.00/8.99 (primary) and 10.00/9.96/7.89/6.13 → 10.00/10.00/10.00/7.69 (all); (b) all-radii Δχ² +100.10 → +69.36 (−30.7 ≥ 1). **Bites.** |
| UNTOUCHED | CFG804 and CFG416 directories unchanged (`git status` clean) |
| R-h (reported only) | h = 0.6736 instead of 0.674 changes N by ≤ 0.004 and no NGRID snap, so the result is unchanged |

Compute: each run took about 2 s on a single core and peaked below 90 MB of memory.

## Scope and caveats

This lane fixes only the unit convention. CFG886's other T5 points are not addressed:
- R from BAO + BBN;
- f_ret provenance: the galaxy floor 0.10 is not traceable in the repo, and the group ramp is UNDETERMINED.

The census f_ret is an observational input carried in the record, not derived by the framework (CFG806).

## Files

- `cfg902_run.py` runs one MODE × footing. `cfg902_summary.py` holds the checks and the before/after table.
- `cfg902_{orig,declared,mutate}[_alt].out` and `cfg902_results_*.json` are CFG804's own outputs, redirected here.
- `cfg902_extras_*.json` holds N under each convention at fixed masses.
- `cfg902_summary.out` and `cfg902_results.json` are the summary.

Rerun from this directory:
- `OMP_NUM_THREADS=1 python3 cfg902_run.py orig canonical`
- repeat the same command with `orig alt`, `declared canonical`, `declared alt` and `mutate canonical`
- `python3 cfg902_summary.py`

κ = ½ FITTED; footings 9.3603e-11 / 1.1312e-10, never pooled; raw KiDS-1000 data, framework-native model; not theory closed.
