# IC1_inner_column_cores — RESULT: IC1 INACTIVE on both footings

Frozen criteria: `FROZEN_CRITERIA.md` + `ASSUMPTION_LEDGER.md` (6e0ea16bc2). Amendment A1 is pre-result (899a4356e7).
Amendment A2 is POST-RESULT and touches the borrowed IC2 comparator and the K3 check only. Checks 6/6. MUTATE (w with the
opposite sign) fails K2 (exit 1). Runtime 47 s, peak RSS 0.63 GB, one thread, `nice -n 15`.
κ = ½ FITTED; footings never pooled; cold dark energy, not matter; not theory closed.

## Question

X41 and X42 left an unexplained "core-concentration factor" of about 11–23 (13.6 in X42's H1-EPS fit) between the EPS
collapse column and the cluster cores. For an NFW halo, c²/[3 m(c)] at c = 6–10 gives the same 11–22. Does ordinary
collapse supply that factor with no free amplitude? Rule IC1:

    Σ_core = max(Σ_a₀, Σ_IC)

Σ_IC is the densest inside-out spherical-collapse column. Each inner fraction f collapses at the NFW (1997) median EPS epoch
and keeps the density 18π² ρ_m(z_c). The result is matched to a Burkert core by equal peak self-acceleration.

## Result

| | canonical | alt |
|---|---|---|
| Step 0: X41's Σ_coll table / X38 + X40b baseline | identical (0 / 3.9e-7) | same run |
| SPARC (both backgrounds) | PASS, = X38 (0 of 350 halos active) | PASS, = X38 |
| clusters | 0 of 652 cells active; identical to X38 | identical to X38 |
| failing keys | MID-T2, MID-T3, MID-b, OUT-Mall, OUT-M3 (all UNDER) | MID-T3, MID-b, OUT-Mall, OUT-M3 |
| groups | ABOVE LAW, Z +2.48 | ABOVE LAW, Z +2.29 |
| **verdict** | **IC1 INACTIVE** | **IC1 INACTIVE** |

Σ_IC over 10¹¹–10¹⁵ M☉ (background A): 8.1, 14.4, 25.3, 43.9 and 76.9 M☉/pc², i.e. 0.08–0.72 Σ_a₀ (canonical). The
log slope over 10¹³–10¹⁵ is 0.242, close to X40b's 0.25–0.30, the same as X41's. The crossover Σ_IC = Σ_a₀ falls at log M
= 15.56 (canonical) and 15.88 (alt), above every cluster. Background B agrees within 2 %.

**The native factor is η_IC = Σ_IC / Σ_coll(X41) = 2.11–2.22, not 13.6.** Inside-out shell memory supplies about 2× over the
virial column, and the cores need about 14×. The densest column comes from large inner fractions (f* = 0.18–0.5, z_c
0.3–1.3), not from early small progenitors. In this native picture, early small progenitors are not denser in column. The
c ≈ 7 concentration that would close the gap is therefore not produced by spherical collapse with shell memory. In NFW97 it
is the simulation-calibrated C (inner density ≈ C ρ_crit(z_c), with C of order 10³), not 18π².

## Reported only (no verdict weight)

- **IC2, BORROWED: ΛCDM NFW with Dutton & Macciò c200(M), same matching.** It overshoots everywhere.
  - SPARC: Υ 0.30 on both footings (FLOOR-BREAKING: 96–100 % of galaxies have s > 1).
  - Cluster s ≈ 9–12, with G-IN-all, G-IN-Mall, MID-T1 and MID-T3 failing OVER.
  - The two cells that no earlier core rule moved do move here: G-OUT-M3 Z +1.04, groups CONSISTENT at Z +1.22.
  - So those cells are not strictly rule-invariant. They respond to a much more concentrated halo, but at a price that
    breaks SPARC and the inner cluster keys.
- **Dwarfs:** DWARFS INACTIVE on both footings. Σ_IC is 0.7–2.4 M☉/pc². Draco and Sextans are BOUNDARY because their
  extrapolated M200 ≈ 2×10⁷ M☉ sits near the σ-table edge. The unfloored order is wrong (Fornax > Leo I > Draco > Sextans,
  set by mass alone, as disclosed before the run). This says nothing about the CCT dwarf campaign.

## What this closes, and what it leaves

- **Closed:** "the missing cluster-core factor is just ordinary collapse concentration" fails in its native form. Inside-out
  spherical collapse with shell memory gives η ≈ 2.1, about 6.4× short.
- **Still open:** the concentration a ΛCDM simulation gives (IC2) is *too much* at every scale once matched by peak
  acceleration. It is about 2× too much for SPARC and about 3× too much for cluster cores. The needed rise is between the
  two, and it has no native origin in the record.
- **Not done:** other Burkert matchings (equal column at r₀, equal mass at r₀). These are named, not done. They change Σ_IC
  by an O(1) factor, and a 6× change would be needed.

## Provenance

- `ic1_run_INTERRUPTED_preA2.log`: the first run, stopped during IC2 after a K3 failure. Its 58 IC1 lines are
  byte-identical to the final `ic1_inner_column.out` once timing is stripped; A2 changed no graded line. See
  `AMENDMENT_A2.md`.
- `ic1_inner_column.out` / `_results.json`: the final run.
- `_MUTATE.out` / `_results_MUTATE.json`: the MUTATE run (K2 fails, exit 1; its numbers are never graded).
- `ic1_x30_machinery.log`: X30's machinery log, redirected here.
- Reproduce (repository root): `PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 rebuild_2026_10_22/IC1_inner_column_cores/ic1_inner_column.py`
