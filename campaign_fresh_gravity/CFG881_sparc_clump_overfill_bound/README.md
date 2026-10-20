# CFG881 — how much clump-like extra mass can SPARC galaxies hide?

Criteria: `FROZEN_CRITERIA.md` (f417bc25a, committed alone before any script; owner block 880–889). Run: `python3 cfg881.py`
(`CFG881_MUTATE=full|tenth` → separate outputs). Seconds, numpy only. κ = ½ fitted; ν_e; footings never pooled. Not theory closed.
Post-hoc descriptive mass bins: `python3 cfg881_massbins.py` (written after the frozen run; does not change the class).

## Question
CFG878 (post-hoc route 2): each first atomic-cooling block (σ ≈ 7.4–8.2 km/s, baryonic mass M_block ≈ 81σ⁴/(4Ga0) ≈ M_cl) makes one
cold-energy clump of M_cl = 5.25e6 M_⊙ canonical / 4.24e6 alt, which is retained. A galaxy built from N_blocks = M_b/M_block blocks
that kept a fraction F_ret of its clumps carries ≈ F_ret · M_b of extra mass. SPARC sits on the law, so it bounds F_ret.

## Method (as frozen)
- 147 SPARC galaxies (Q ≤ 2, inc ≥ 30°, eV/V < 0.1, g_bar > 0; CFG870's cuts and Υ 0.5/0.7); class on the 122 with M_b ≥ 1e9 M_⊙.
- Per galaxy and window: δ_W = median log10(g_obs/g_law), σ_W = √(σ_med² + 0.10²) (0.10 dex systematic floor per galaxy),
  upper limit δ_up = max(δ_W, 0) + 2σ_W. M_max = the extra mass whose pull, added on top of the law (convention A, as CFG870/877
  used M_x), raises the window median to δ_up.
- Four retained-mass shapes: **CORE1** (clumps sunk inside 1 kpc; points R ≤ 3 kpc), **CORE3** (inside 3 kpc; R ≤ 6 kpc),
  **BARYON** (spread like the stars and gas, g_x = F g_bar; all points), **FLAT** (M ∝ R to the last point; all points).
- F_max = M_max/(N_blocks M_cl) = M_max/M_b (M_block = M_cl), N_max = M_max/M_cl.

## Result — CLASS: **PARTIAL** (both footings agree)
Per shape: CORE1 PARTIAL, CORE3 PARTIAL, BARYON ALLOWED, FLAT ALLOWED.

Massive galaxies (M_b ≥ 1e9), primary (floor 0.10 dex, convention A):
| shape | N | canonical F_max median [16–84%] | N_max median (clumps) | alt F_max median [16–84%] | floor 0.20 (can.) | convention B (can.) |
|---|---|---|---|---|---|---|
| CORE1 (≤1 kpc) | 48 | **0.269** [0.148–0.586] | 527 | **0.258** [0.145–0.616] | 0.632 | 0.196 |
| CORE3 (≤3 kpc) | 95 | **0.917** [0.402–1.932] | 1790 | **0.896** [0.400–1.901] | 2.036 | 0.737 |
| BARYON | 121 | **2.07** [1.07–4.02] | 5800 | **2.08** [1.13–3.79] | 4.88 | 1.32 |
| FLAT | 121 | **3.17** [1.90–5.68] | 9280 | **3.20** [1.99–5.68] | 7.67 | 2.12 |
- Only 10% of CORE1 galaxies (1% of CORE3, none of BARYON/FLAT) reach F_max ≤ 0.1.
- σ_b variants (block σ 7.36 / 8.22 km/s → F × 0.91 / × 1.42): CORE1 0.245 / 0.381, CORE3 0.84 / 1.30; the class does not change.
- Convention B (extra mass as a source through the law) tightens every bound but leaves the same per-shape pattern.
- Dwarfs (M_b < 1e9, 16–20 galaxies): F_max medians 1.4 (CORE1) to 5.2 (CORE3), N_max ≈ 120–410 clumps. CFG877's one clump per
  SPARC dwarf sits far below this.

Post-hoc descriptive, by M_b (canonical; `cfg881_massbins.out`):
| shape | 1e9–1e10 | 1e10–5e10 | ≥ 5e10 | slope dlogF/dlogM_b |
|---|---|---|---|---|
| CORE1 | 0.39 (26) | 0.20 (9) | **0.13** (13) | −0.40 |
| CORE3 | 1.50 (50) | 0.63 (22) | 0.40 (23) | −0.43 |
| BARYON | 3.26 (57) | 1.57 (28) | 1.26 (36) | −0.25 |
| FLAT | 3.23 (57) | 3.17 (28) | 3.00 (36) | −0.04 |
Even in the most massive galaxies the central bound stays just above 0.1, so the frozen EXCLUDED line is not reached anywhere.

## Reading
- **SPARC does not exclude retained first-cooling clumps.** If clumps sank into the central kpc, at most about a quarter of the
  full-assembly clump mass can remain (median; about an eighth in the most massive galaxies). That is up to ~500 clumps, or
  ~3e9 M_⊙, inside 1 kpc. Clumps sunk only to ~3 kpc are allowed at nearly full retention.
- **Spread clump material is not bounded at all at F ~ 1.** Mass that traces the baryons is degenerate with Υ and distance. A
  0.10 dex systematic floor already allows 2–3 M_b. A FLAT (M ∝ R) spread hides even more, because the law's boosted pull
  dominates the outer curve.
- **The bound is limited by systematics, not by statistics.** σ_W ≈ 0.10 dex for almost every galaxy, so the limit is about
  0.2 dex above the law, and doubling the floor more than doubles F_max (×2.3–2.4). SPARC rotation curves are therefore not the decisive probe
  of CFG878's overfill. A probe that does not trade off against Υ would be needed.
- **What F_max bounds is the product φ·F_ret.** Here φ is the fraction of a galaxy's baryons assembled through first-cooling
  blocks. With φ < 1 the retention bound loosens as 1/φ. Nothing in the record fixes φ, so no smaller-φ variant is quoted.
- **Not a detection.** 17% of CORE1 galaxies (7% of BARYON/FLAT) sit more than 2σ_W above the law in their window. That is
  what bulge/disc Υ, beam smearing and non-circular motions produce. It is not evidence for clumps.

## Controls
- **K1 PASS:** the script reproduces CFG877's canonical SPARC D and CFG870's canonical T1 D exactly (|diff| 0.0, N 56 each).
- **K2 PASS:** solver round trip (g_obs := g_law + g_x(0.3 M_b), no noise, no floor) recovers M_test to 8.9e-15 (CORE1 and FLAT,
  every massive galaxy).
- **MUTATE full (F_inj = 1 injected with each shape):** every shape's median F_max ≥ 1, giving RETENTION ALLOWED on both footings,
  as required (CORE1 2.22, CORE3 2.47, BARYON 3.32, FLAT 4.58). Individual detection rises from 17%→94% (CORE1) and 12%→78%
  (CORE3), but only 7%→38% (BARYON) and 7%→20% (FLAT). Per galaxy, the test has power for sunk clumps and little for spread ones.
- **MUTATE tenth (F_inj = 0.1):** no shape is EXCLUDED, as required. This control is **uninformative**: the clean bound already
  exceeds 0.1, so it would pass anyway. CORE1 detection still rises from 17% to 38%.

## Disclosures
- **The hand expectation before the run was wrong.** It put CORE1 at ~0.01–0.05, comparing the full M_b inside 1 kpc with
  g_obs. The 0.2 dex allowance at 2σ is larger than that estimate assumed. The result is 0.27 (0.13 at M_b ≥ 5e10).
- The windows were chosen from data-coverage counts only (no residuals) before freezing. CORE1 uses only the 48 massive galaxies
  with ≥ 3 points inside 3 kpc, which leans toward nearer and smaller systems.
- The mass bins are post-hoc and descriptive.
- M_b = 0.5 L[3.6] + 1.33 M_HI (CFG870's definition). It counts bulge light at Υ 0.5 and slightly inflates F_max (conservative).
- Convention A (extra pull added on top of the law) is the looser of the two conventions. B is reported.
- Mass beyond the last measured point is invisible and not bounded. The FLAT shape assumes all retained mass lies inside R_last.
- CFG878's route 2 is itself post-hoc. This lane bounds it and does not test whether first-cooling blocks exist.
