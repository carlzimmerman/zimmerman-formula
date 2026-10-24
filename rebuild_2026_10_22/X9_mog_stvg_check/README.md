# X9_mog_stvg_check: MOG/STVG with its published universal parameters on SPARC and on the eRASS1 × KiDS cluster stack

Criteria: `FROZEN_CRITERIA.md` (committed alone, 8c548f725d; amendments A1–A3 below). Inputs and classes:
`ASSUMPTION_LEDGER.md`. MOG is context here, not a candidate for adoption: it has no a₀ and does not tie anything to the
dark-energy density. For the programme's law (reference rows only): κ = ½ FITTED; footings never pooled. No dark-matter
particle. Not "theory closed". Nothing here says the data favour the framework.

## Verdict (frozen classes): MOG UNIVERSAL SET FAILS (BOTH)

| dataset | class | why | JSON |
|---|---|---|---|
| (a) SPARC RAR, P4's line | **FAIL (ROBUST)**; χ² line FAIL | rms **0.136 dex** (line 0.110) and median per-galaxy Υ **1.20** (window 0.50–0.80; 57 % of galaxies pinned at the 1.20 bound). Dwarfs sit **+0.39 ± 0.03 dex** above MOG at their best Υ | `sparc.primary`, `sparc_class` |
| (b) cluster stack, X2's fixed-form line | **FAIL** (no qualifier) | the outskirts are over-predicted: A_OUTER **0.65–0.66** (Z −5.8 / −6.1 at C0; −4.4 at C\*). The core is not the problem: A_MID **0.86 / 0.90** (C0) and **0.84 / 0.87** (C\*) | `clusters.PH`, `cluster_class` |

- **Parameters used.** One published set, nothing fitted: α = 8.89, μ = 0.042 kpc⁻¹ (Moffat & Rahvar 2013, MNRAS 436, 1439;
  arXiv:1306.6383). Moffat & Rahvar 2014 (MNRAS 441, 3724; arXiv:1309.5077) reuse exactly this set for 11 Chandra clusters.
  These are web lookups of the arXiv PDFs and are PROVISIONAL.
- **Does MOG need different cluster parameters?** In the literature, yes, twice.
  - Brownstein & Moffat 2006 (the MSTG predecessor) fit clusters with M₀ ≈ 5.9e15 (M_gas/1e14)^0.39 M☉ and r₀ = 139 kpc. Their
    galaxy fit used M₀ = 9.6e11 M☉ and r₀ = 13.9 kpc.
  - The "parameter-free" α(M) (Moffat & Toth 2009, used by Moffat, Rahvar & Toth 2018) gives **α ≈ 18.9** for these
    clusters, not 8.89.

  Here, both cluster sets fail worse than U (side readings S1, S2). U fails too. So no published MOG set passes this stack.
- **Lensing in MOG is not the dynamical G_eff.** Light does not feel MOG's Yukawa vector force (Moffat, Rahvar & Toth 2018,
  Galaxies 6, 43, Eqs. 30–32; MR13 Eq. 21). The lensing mass is therefore (1 + α) M_baryons at every radius. That is the
  primary here (P-PH). The brief's reading, that lensing follows the dynamical G_eff, is variant V-DYN. Inside clusters the two
  agree to 0.1 % (median V-DYN/P-PH 0.9986, range 0.987–1.000; `clusters.VDYN_over_PH_bins3to7`). This confirms MR14 §4.3,
  and it does not change the class.

## Step 0: the record's own numbers, same data, same code

- **R1:** P4's SPARC loader (exec'd from its source) equals `CFG4_common.load_sparc` bit for bit. CFG695 S2 is reproduced:
  0.1009 at Υ 0.60 and 0.0994 at 0.55, |Δ| = 0.
- **R2:** P4's isolated law with one Υ per galaxy is reproduced on both footings: rms **0.05409 / 0.05372**, median Υ
  0.52 / 0.44, |Δ| = 0. P4's full v3 at L★ = 24 pc is 0.0540 / 0.0535 (`sparc_law_reference`).
- **R3:** X2's C0 (F1 PRIMARY) law is reproduced in all 4 cells with |ΔA|, |Δσ|, |Δχ²| = 0. A_MID is 1.676 / 1.720 (canonical,
  h 0.672 / 0.686) and 1.540 / 1.580 (alt). A_OUTER is 0.950 / 0.949 / 0.870 / 0.869. χ² is 33.4 / 41.8 / 27.3 / 34.9
  (`clusters_reference.law_C0`).
- **R4:** X2's single-change law rows (a1), (d) and (e) are reproduced exactly.
- **R5:** F1's Newtonian baryons are reproduced (h 0.70 record recipe): A_MID 9.824 ± 0.629, A_OUTER 7.388 ± 0.612.
- **Law at C\*** (X2 JSON, including X2's (c1) external field): A_MID 1.64 / 1.68 / 1.51 / 1.55, A_OUTER 0.93 / 0.93 / 0.85 /
  0.85, χ² 21.7 / 13.1 / 20.6 / 14.6 (`clusters_reference.law_Cstar_X2`). **The law also fails X2's fixed-form line**, in its
  core.

## (a) SPARC (`sparc.*`; P4's statistics exec'd read-only; Υ per galaxy on 0.30–1.20)

| reading | rms (dex) | median Υ (16–84 %) | at Υ = 1.20 | χ²/dof | frac p ≥ 1e-3 | small / large mean residual |
|---|---|---|---|---|---|---|
| **MOG U, PRIMARY** (thin-disc superposition, MR13 Eq. 34; bulge spherical) | **0.1360** | **1.20** (0.51–1.20) | 0.57 | 16.3 | 0.383 | +0.392 ± 0.033 / +0.102 ± 0.014 |
| MOG U, G-SPH (P4's spherical approximation) | 0.1322 | 1.20 (0.47–1.20) | 0.57 | 16.8 | 0.400 | +0.384 / +0.090 |
| Newton (same freedom) | 0.2528 | 1.20 (0.86–1.20) | 0.73 | 73.1 | 0.274 | +0.430 / +0.190 |
| the law, isolated, per-galaxy Υ (R2) | 0.0541 / 0.0537 | 0.52 / 0.44 | — | 4.93 / 4.77 | 0.634 / 0.634 | — |
| S1 parameter-free α(M), μ(M) (side, no weight) | 0.0892 | 1.12 (0.55–1.20) | 0.46 | 9.35 | 0.474 | +0.233 / +0.040 |

- **ROBUST.** Every declared variant fails the line:
  - the four (α, μ) ±1σ corners give rms 0.133–0.140, median Υ 1.20;
  - P4's Chae lognormal Υ prior gives 0.136;
  - Q ≤ 2 gives 0.135.
- **Mechanism.** μ⁻¹ = 24 kpc is fixed. Inside a few kpc, G_eff/G_N − 1 ≈ α(μr)²/2 ≈ 0.008 (r/kpc)², so a dwarf at
  r ≈ 3–5 kpc gains only 7–20 %. The heaviest allowed disc does not close the gap, so the small galaxies stay +0.39 dex high.
  Even the large galaxies sit +0.10 dex above MOG at their best Υ. MR13's own Table 1 points the same way: its three LSB
  galaxies prefer α ≈ 13–14 and μ ≈ 0.11–0.22 kpc⁻¹ (A4).
- **No point is lost.** g_MOG > 0 wherever g_bar > 0 (`neg_points`).

## (b) Clusters (`clusters.*`; X2's replay and statistics exec'd read-only; MOG has no a₀, so 2 cells, h 0.672 / 0.686)

The primary is P-PH, Σ = (1 + α) Σ_N(baryons). The line is χ² ≤ 11.07 AND |Z_MID| ≤ 2 AND |Z_OUT| ≤ 2 in both cells.

| reading | setup | A_MID ± σ (Z) | A_OUTER ± σ (Z) | χ² | line |
|---|---|---|---|---|---|
| **P-PH** | C0 | 0.864 ± 0.058 (−2.34) / 0.896 ± 0.057 (−1.84) | 0.653 ± 0.059 (−5.84) / 0.661 ± 0.055 (−6.14) | 37.4 / 37.6 | not met |
| **P-PH** | C\* | 0.839 ± 0.120 (−1.34) / 0.872 ± 0.136 (−0.94) | 0.643 ± 0.081 (−4.43) / 0.651 ± 0.079 (−4.44) | 18.4 / 19.1 | not met |
| clipped boost | C0 / C\* | 0.93–0.97 / 0.91–0.94 | 0.69 / 0.68 (Z −5.0 to −5.3 / −3.8) | 24.6–26.3 / 14.4–15.7 | not met |
| α = 8.55 / 9.23 (±1σ) | C0 | 0.89–0.93 / 0.84–0.87 | 0.68 / 0.63–0.64 | 29–30 / 47 | not met |
| V-DYN | C0 / C\* | 0.866 / 0.899; 0.842 / 0.875 | 0.653 / 0.661; 0.643 / 0.651 | 37.0 / 37.3; 18.3 / 19.1 | not met |
| S1 α(M) ≈ 18.9 (side) | C0 | 0.43 / 0.45 | 0.33 | 419–438 | not met |
| S2 BM06 MSTG (side) | C0 | 0.55 / 0.57 | 0.67 / 0.68 | 169–184 | not met |

- **Class: FAIL**, with no qualifier. The clipped boost, α ± 1σ and V-DYN all leave the line unmet at both setups.
- **INNER band (0.15–0.5 Mpc):** MOG gives 0.87–1.10, against the law's 2.04–2.37.
- **Terciles (C0, P-PH; `clusters.terciles_C0_PH`):**
  - T1: A_MID 0.90 / 0.92, A_OUTER 0.56 / 0.61;
  - T2: A_MID 1.03 / 1.08, A_OUTER 0.58 / 0.60;
  - T3: A_MID 0.75 / 0.77, A_OUTER 0.72 / 0.71.

  The OUTER over-prediction holds in every tercile.
- **Why it fails.** MOG multiplies the baryons by a constant 9.89 at every cluster radius. The data relative to Newtonian
  baryons fall from 8.5–8.9 (MID) to 6.5 (OUTER) (`clusters.newton_C0`). A constant factor can match at most one band.
  - α would have to be ≈ 7.5 for MID and ≈ 5.5 for OUTER. Both are far outside 8.89 ± 0.34.
  - The law has the opposite problem: its boost grows outward, which leaves the core short.

### A3 (POST-RESULT diagnostic, no class weight): the FAIL rests on the gas beyond R500

`clusters.A3_gas_beyond_R500`, `clusters.A3_favourable_G2_clip_a8.55`:

| gas beyond R500 | setup | A_MID (Z) | A_OUTER (Z) | χ² |
|---|---|---|---|---|
| X2 (a3): ρ ∝ r⁻³ from R500 | C0 | 0.84 / 0.87 (−2.8 / −2.3) | 0.76 / 0.77 (−3.5) | 28.7 / 23.2 |
| X2 (a3) | C\* | 0.82 / 0.85 (−1.5 / −1.1) | 0.75 / 0.77 (−2.6 / −2.5) | 8.5 / 8.5 |
| F1 G2: none beyond R500 | C0 | 0.83 / 0.87 (−3.0 / −2.4) | 1.28 / 1.33 (+2.4 / +2.9) | 28.4 / 27.6 |
| F1 G2 | C\* | 0.82 / 0.86 (−1.5 / −1.1) | 1.28 / 1.33 (+1.7 / +2.0) | 13.8 / 24.1 |
| G2 + clipped boost + α 8.55 (most favourable) | C\* | 0.92 / 0.96 | 1.40 / 1.44 (+2.2 / +2.5) | 13.6 / 24.1 |

- With the steepest record bracket (a3), MOG at C\* is under the χ² line (8.5) and misses only Z_OUT, by 0.5–0.6σ.
- With no gas beyond R500, OUTER flips to under-prediction.
- **So between those two extrapolations sits a gas profile for which MOG's universal set would meet X2's line.** The frozen
  FAIL is a failure under the record's gas conventions: β = 2/3 to 3 Mpc, or CFG814's steepening at 2.2 R500. About 74–78 %
  of that gas budget lies beyond R500 and is extrapolated, not measured (X2 §(a)).
- The cluster FAIL is therefore real but **gas-shape conditional**. The SPARC FAIL is not.

## Amendments

- **A1 (PRE-RESULT, implementation; after synthetic engine tests only).** K2 samples the exponential discs to 30 R_d, not 10
  R_d.
  - With 10 R_d sampling, the declared R⁻² extension rule (B6) gives up to 0.6 % in g_MOG and would have failed K2's 0.5 %.
  - That is the extension rule, not the numerics. It is printed as **D-EXT**: 0.52 / 0.72 / 0.61 %, ≲ 0.003 dex, far below
    P4's 0.110 dex line.
  - With 30 R_d sampling, K2 = 4.8e-5.
- **A2 (POST-RESULT for K5 only; numerics).**
  - Run 1 stopped at the RSS guard (0.958 GB) before any MOG number.
  - Run 2 (env-flagged RSS trace) completed with the same classes and K5 FAIL at 1.051 GB. Its `.out` was overwritten and is
    not kept.
  - Smaller vectorised chunks gave run 3: 10/10 PASS at 0.418 GB. The committed run is 0.482 GB.
- **A3 (POST-RESULT diagnostic, no class weight).** The gas-beyond-R500 rows above.
- **A4 (POST-RESULT, text only).** The criteria's transcription of MR13 Table 1 understated the LSB μ range: it is
  0.11–0.22 kpc⁻¹ (DDO 154 0.22), not 0.11–0.12. The table is reported only, so no input or line changes.

## Checks: 10/10 PASS (exit 0, 52 s, one thread, peak RSS 0.482 GB); MUTATE 7/10 (exit 1)

| check | result |
|---|---|
| K1 sph engine vs the point-mass closed form | 4.5e-6 (G_eff at 300 kpc 9.8896) |
| K2 disc engine vs direct 2-D quadrature (exponential discs) | 4.8e-5 |
| K3 FFTLog grid ×2, range ×10 | 1.8e-6 dex |
| K4 shells vs the exact uniform-sphere Yukawa field | 7.4e-8 |
| K5 | 0.482 GB |
| R1–R5 | exact (see Step 0) |

`--mutate` (engines at α = 0) makes K1, K2 and K4 FAIL, as frozen. At α = 0 MOG reproduces Newton: SPARC to 1.8e-15 dex, and
the cluster P-PH model equals the Newtonian model (A_MID 8.541).

## What this does not show

- **Not a test of MOG's full theory.** Only its weak-field limit is tested, with constant α and μ (MR13 / MR14). It says
  nothing on MOG's cosmology, CMB or structure growth, and runs no nonlinear STVG solve. The point-source α(M) and BM06 readings
  are side readings.
- **The SPARC geometry is idealised.**
  - Discs are razor-thin superpositions built from SPARC's Newtonian V_gas and V_disk.
  - The δg kernel is smooth, so thickness enters only at O((μz₀)²).
  - Mass beyond the last point is taken as zero (D-EXT ≤ 0.7 %).
  - G-SPH brackets the geometry, and the class does not depend on it.
- **The cluster FAIL is conditional on the gas beyond R500** (A3). A measured outskirt gas profile could move it. The
  external field is irrelevant for MOG (linear field equations). R500 remains ΛCDM-PROCESSED, as in F1.
- **Lensing prescription.** The primary follows MRT18 (light ignores the vector field). If a future MOG treatment let light
  feel part of the Yukawa term, V-DYN brackets it: no change inside clusters, because the Yukawa term is negligible there.
- **Literature values.** All are PROVISIONAL web lookups of arXiv PDFs; none of the papers is on disk.
  - MR13's α = 8.89 was fixed on 9 THINGS galaxies with B-band Υ★, not on SPARC.
  - P4's Υ window (3.6 μm) is the record's line, not MOG's own convention.
- It does not show that any rule-compatible framework passes the cluster cores. MOG's core (MID) is close, at Z −2.3 to −0.9,
  but its outskirts are not.

## Suggested record fixes (no other file edited)

1. **MAP §1 (alternative frameworks) and CFG230's C08 cells.** Replace "MOG/STVG: never computed" with: "X9: with its published
   universal set (α 8.89, μ 0.042 kpc⁻¹), MOG fails P4's SPARC line (rms 0.136, Υ pinned at 1.20, dwarfs +0.39 dex). It also
   fails X2's cluster line on the outskirts (A_OUTER 0.65), not the core (A_MID 0.84–0.90). The cluster fail is conditional
   on the gas beyond R500."
2. **MAP §1.A "Cluster cores" bullet ("the only published cluster passes are contested (MOG)").** Add: "MOG's universal set
   puts no core excess on this stack. Its constant (1 + α) over-predicts the 1.2–3 Mpc band instead."
3. **Coordinator brief wording.** "Lensing in MOG follows the same G_eff" is not the published assumption. MOG's lensing mass
   is (1 + α)M, because light ignores the vector force (MRT18 Eq. 32). Inside clusters the two coincide to 0.1 %.
4. **X2 / status board context.** The law at C\* also fails X2's fixed-form χ² line (13.1–21.7 > 11.07) through its core.
   Worth stating next to X2's V3 when fixed-form models are compared on that line.

## Files and runs

| file | what |
|---|---|
| `FROZEN_CRITERIA.md`, `ASSUMPTION_LEDGER.md` | criteria (8c548f725d), amendments A1 (a9dd8f7239), A2–A4 |
| `x9_mog_stvg_check.py` → `.out`, `_results.json`; `_MUTATE.out`, `_results_MUTATE.json` | engines, checks, both tiles, verdicts |

```
OMP_NUM_THREADS=1 nice -n 15 python3 rebuild_2026_10_22/X9_mog_stvg_check/x9_mog_stvg_check.py            # ~1 min, exit 0
OMP_NUM_THREADS=1 nice -n 15 python3 rebuild_2026_10_22/X9_mog_stvg_check/x9_mog_stvg_check.py --mutate   # ~40 s, exit 1
```

**Read-only inputs:**
- P4's source (exec'd) and `p4_solver`;
- `CFG4_common`;
- CFG695's JSON;
- P4, F1 and X2 JSONs;
- X2's replay npz and source (exec'd);
- F1's source (exec'd through X2's block).

Source sha256 values are in the JSON. Nothing was downloaded into the repo. The literature PDFs were read through the web tool
only.
