# GD2_route_e_mw_x5_box — RESULT: FEASIBLE (WIDE PRIORS ONLY), both footings. A short disc lets the flagship pass the Milky Way; published-prior discs do not

Frozen criteria **78f30f7368** (committed alone; no amendment). κ = ½ FITTED. Footings graded separately, never pooled.
Route E: Newtonian baryons plus the OS1-cored cold dark energy halo (Σ = Σ_a₀(σ/σ_ref)^q_f, σ = V_last/√2). Cold dark
energy, not matter. No dark-matter particle. Nothing here says the data favour the framework or ΛCDM. Not "theory closed".
Runtime 5 s, peak RSS 0.37 GB, one thread, nice 15.

**Provenance.** A print-only fix was made before commit: the per-cell table showed the PRIMARY row twice instead of
PRIMARY and VARIANT. The classes, counts and JSON come from `classify()` and were the same on both runs.

## Question

GD1 A1 found the flagship misses V_c(R₀) on McMillan 2017 baryons (z −6.2 to −4.0). GD1b and IJ1 found no native core rule
that lifts the halo. Does any baryon model in X5's frozen published-prior box (175 cells) pass V_c(R₀), K_z and the Ou+24
curve together under the flagship?

## Verdict (frozen classes; PRIMARY = V_last 172.98, background A)

| | canonical | alt |
|---|---|---|
| **class** | **FEASIBLE (WIDE PRIORS ONLY)** | **FEASIBLE (WIDE PRIORS ONLY)** |
| cells passing all four lines | **1** of 175 | **7** |
| cells passing L1 / L2a / L2b / L3 | 16 / 32 / 32 / 9 | 19 / 32 / 37 / 11 |
| VARIANT (V_last 229.05), same rules | FEASIBLE (WIDE PRIORS ONLY), 14 cells | same, 13 cells |
| background B (reported) | same class, 1 cell | same class, 7 cells |

**The canonical passing cell:**
- inputs: Σ_b 47.1 M☉ pc⁻², M_bb 2.12e10 M☉ (the box's top edge), R_d 1.933 kpc, M★ 7.56e10.
- results: V_c(R₀) 232.4 km/s, K_z(R₀) 68.5, χ²_Kz 29.4 / 67.5, χ²_Ou 56.9 / 59.9 (marginal).
- halo: lgM200 12.03, r₀ 16.0 kpc.

**Alt's seven cells:** six at R_d 1.933 with Σ_b 43.7–47.1, and one at R_d 2.267 (Σ_b 53.9). χ²_Ou is 42–57.

**Why "wide priors only".**
- Every passing cell has R_d = 1.93 or 2.27 kpc, outside Licquia & Newman 2016 (2.64 ± 0.13, tag 2.38–2.90). These
  values sit inside BH&G16 (2.6 ± 0.5) at −1.3σ and −0.7σ.
- All passing cells have M★ inside Licquia & Newman 2015's ±2σ.
- The best cell that satisfies both tags (Σ_b 53.9, M_bb 2.12e10, R_d 2.6) gives V_c(R₀) 208.8 / 211.9: z **−4.4 / −3.7**,
  and χ²_Ou 264 / 174. Its K_z is fine (65.4 / 66.2).

## Reading

- **The Milky Way miss is a baryon-scale question, not a halo failure.** With a short disc, about 1.9 kpc, the flagship
  passes all four lines on both footings with no parameter changed.
  - It has the Sun's orbital speed.
  - It has the local vertical pull: both the 43-MAP χ² and Bovy & Rix's summary 66.4 ± 2.2.
  - It has Ou+24's curve to 27 kpc.
- **The law does worse on the same box (X5, context).** The law (v3 AQUAL) also needs the short disc. Its passing cells
  miss Bovy & Rix's summary K_z by +4.7 to +6.6σ (K_z(R₀) 76.7–80.9). Route E's passing cells sit at 65–71 on that
  summary. So this is the first model in the record to clear V_c(R₀), both K_z tests and the Ou+24 curve together. It
  does so only with a disc shorter than Licquia & Newman allow.
- **The OS1 scaling is load-bearing.** The MUTATE run uses q = 0 (X38 core). It reaches **V+K ONLY** on both footings: 8
  cells pass L1 + L2, and **0 pass L3**. A fixed-Σ_a₀ core cannot follow Ou's curve even on a short disc.
- **What decides it.** The flagship's Milky Way now rests on R_d. A disc scale length near 1.9–2.3 kpc keeps it alive; Licquia
  & Newman's 2.64 ± 0.13 does not. Gaia DR4's disc structure and the inner rotation curve bear directly on this.

## Limits

- One family (X5's: McMillan vertical structure, one R_d for both discs, McMillan bulge shape rescaled). The M_bb axis is
  PROVISIONAL (Portail+17 from memory, as X5). The canonical cell sits on the M_bb box edge.
- The Ou+24 χ² uses S3's error model. The canonical pass is marginal (56.9 against a line of 59.9).
- M200 comes from EM1's SPARC relation using each cell's total baryon mass. The halo is spherical and has no EFE.
- V_last is bracketed (PRIMARY 173 / VARIANT 229) and never pooled.

## Checks (`gd2_x5_box.out`)

| check | result |
|---|---|
| K0 McMillan on this Newtonian path vs GD1/S3 | V_b(R₀) 177.09 (177.23), K_z,b 61.89 (62.02): PASS |
| K1 cell masses vs X5's analytic masses | PASS |
| K2 OS1 Σ factor = GD1 A1 (1.635 / 1.510 / 2.100 / 1.863) | PASS; **MUTATE FAILS** (exit 1) |
| K3 halo raises v_c and K_z in every cell | PASS |
| K4 RSS < 1 GB | PASS (0.37) |

## Reproduce

```
OMP_NUM_THREADS=1 nice -n 15 python3 gd2_x5_box.py            # gd2_x5_box.out, gd2_x5_box_results.json
OMP_NUM_THREADS=1 nice -n 15 python3 gd2_x5_box.py --mutate   # q = 0; *_MUTATE; exit 1 by design
```
