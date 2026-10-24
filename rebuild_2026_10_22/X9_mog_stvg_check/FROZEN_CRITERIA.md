# X9_mog_stvg_check: FROZEN CRITERIA (committed alone, before any script or number of this lane)

Lane `rebuild_2026_10_22/X9_mog_stvg_check/`. Written 2026-10-24. Rules: `rebuild_2026_10_22/BRIEF.md`,
`doors_push_2026_10_22/BRIEF.md`, `BRIEF_E_AUDIT.md`. Inputs and classes: `ASSUMPTION_LEDGER.md`.
For the programme's own law (the reference only): κ = ½ FITTED; footings 9.3603e-11 (canonical) and 1.1312e-10 m s⁻² (alt),
never pooled. No dark-matter particle. Never "theory closed"; never "the data favour the framework".
**No number of this lane exists.** The only numbers read so far are the record's own (P4, F1, X2 JSON) and the literature
values quoted below.

## 0. Question and status of the answer

Does Moffat's MOG/STVG, with its **published universal parameters and nothing fitted in this lane**, pass
(a) the SPARC radial-acceleration tile by P4's own lines and (b) the eRASS1 × KiDS cluster-core lensing stack by X2's
fixed-form pass line? MOG has extra fields (a scalar G, a massive vector φ_μ, a scalar μ) and no dark-matter particle
species. It does not tie a₀ to the dark-energy density (it has no a₀ at all). **This lane is context, not a candidate for
adoption.** The record's only MOG entries are CFG230's C08 cells (memory labels, MAP §1).

## 1. MOG as used here (LITERATURE-INPUT, PROVISIONAL web lookups of the arXiv PDFs; the papers are not on disk)

- **MR13** = Moffat & Rahvar 2013, MNRAS 436, 1439 (arXiv:1306.6383 v3). Read: abstract; §3 Eqs. 21, 28–33; §4 Eq. 34–36;
  Table 1; Fig. 2 caption.
  - Massive test particles, extended source, α and μ constants (Eq. 33):
    a(x) = −G_N ∫ ρ(x′)(x − x′)/|x − x′|³ [1 + α − α e^{−μ|x−x′|}(1 + μ|x − x′|)] d³x′.
    Point mass: a = −G_N M/r² [1 + α − α e^{−μr}(1 + μr)] (also MRT18 Eq. 24). Normalisation: G_eff → G_N as r → 0 and
    → G_N(1 + α) as r → ∞ (G₀ − κ² = G_N, G₀ = G_∞, α = (G_∞ − G_N)/G_N).
  - Discs (Eq. 34): superposition of the point-mass law over the surface density of a razor-thin disc.
  - **Universal set (abstract, §4.1): α = 8.89 ± 0.34, μ = 0.042 ± 0.004 kpc⁻¹**, fixed on 9 THINGS galaxies (combined
    likelihood, Eq. 36) and then used with Υ★ as the only free parameter on Ursa Major. Table 1's per-galaxy fits range
    α 4.3–13.7, μ 0.018–0.12 kpc⁻¹ (the three LSB galaxies sit at α ≈ 13–14, μ ≈ 0.11–0.12): reported, not used.
  - Gas: M_gas = (4/3) M_HI in MR13; this lane keeps SPARC's 1.33 M_HI (inside V_gas, P4's convention).
- **MR14** = Moffat & Rahvar 2014, MNRAS 441, 3724 (arXiv:1309.5077 v4). Read: abstract; §2.1 Eq. 11; §4.3; Fig. 2 caption.
  **Clusters use the same α = 8.89 ± 0.34 and μ = 0.042 kpc⁻¹** (Eq. 11 and Fig. 2). §4.3 states that inside clusters
  (scales ≫ μ⁻¹ ≈ 24 kpc) the Yukawa term is negligible, so g ≈ (1 + α) G_N M(<r)/r² (they compare beyond ~100–300 kpc).
- **MRT18** = Moffat, Rahvar & Toth 2018, Galaxies 6, 43 (arXiv:1204.2985 v2). Read: §2 Eqs. 5–33; §4.1–4.3; §5.
  - **Light (the published lensing assumption):** for ultrarelativistic particles the vector term αqφ_t is negligible
    (§2.4: ~1e-4 for a 1e12 M☉ lens at 10 kpc), so light bending is the GR formula with G = G₀ = (1 + α) G_N
    (Eqs. 30–31); "lensing mass" M_L = (1 + α) M (Eq. 32). The same follows from MR13 Eq. 21 (½∇²h₀₀ = −4πG₀ρ).
    **So in MOG the repulsive Yukawa term does not act on light: lensing does NOT follow the dynamical G_eff(r).**
    The coordinator's brief said "lensing follows the same G_eff"; that reading is computed as variant **V-DYN** (§3.3).
  - Parameter-free version (Moffat & Toth 2009, CQG 26, 085002, cited as MRT18 ref. [6]; values from MRT18 Eqs. 8–9,
    11–14, 18): α(M) = (G_∞/G_N − 1) M/(√M + E)², μ(M) = D/√M, G_∞ ≈ 20 G_N, D ≈ 6250 M☉^{1/2} kpc⁻¹,
    E ≈ 25 000 M☉^{1/2}. MRT18 §4.1 calls the point-source α "an upper limit" for extended objects; for the Bullet
    Cluster they find observed α 4.3–22 against α(M_L) 17.5–18.6 (Table 2).
- **BM06** = Brownstein & Moffat 2006, MNRAS 367, 527 (arXiv:astro-ph/0507222; MSTG, the predecessor whose weak-field law
  STVG reproduces). Read: abstract; §3 Eqs. 20–25; §4 Eqs. 31–33. Galaxies: M₀ = 9.60e11 M☉, r₀ = 13.92 kpc (Eq. 31).
  Clusters: M₀ = 58.8e14 M☉ (M_gas/1e14 M☉)^0.39, r₀ = r_out/10 for r_out ≤ 650 kpc, else 139.2 kpc (Eq. 33),
  G(r) = G_N{1 + √(M₀/M(r))[1 − e^{−r/r₀}(1 + r/r₀)]} (Eq. 23). **A published cluster parameter set different from the
  galaxy one exists (BM06); MR14 instead reuses the galaxy set.**
- MOG's weak-field equations are linear (Poisson + Yukawa, MR13 Eqs. 21–24): **no external-field effect**. X2's (c1)
  external-field change does not apply to MOG (stated, not computed).

## 2. The one pre-declared parameter set (verdict) and the side readings (no verdict weight)

- **U (verdict):** α = 8.89, μ = 0.042 kpc⁻¹ (MR13), for galaxies AND clusters (as MR14). Bracket for the FRAGILE /
  PARAMETER-FRAGILE qualifiers only: the four corners α ∈ {8.55, 9.23} × μ ∈ {0.038, 0.046} kpc⁻¹ (clusters: α ∈ {8.55, 9.23}).
  No other value of α or μ is evaluated for the verdict; no scan.
- **S1 (side reading):** the parameter-free α(M), μ(M) above. SPARC: M = 1.33 M_HI + Υ L[3.6] (SPARC Table 1) at each
  trial Υ. Clusters: M = the model's baryons inside 3 Mpc (1.2 × gas, C0).
- **S2 (side reading, clusters only):** BM06's cluster prescription, Eq. 23 with Eq. 33: M(r) = enclosed baryons;
  M_gas = gas inside r_out; r_out = radius where the model gas density falls to 1e-28 g cm⁻³ (BM06 Eq. 15), capped at
  3 Mpc. BM06 gives dynamics only; lensing is taken as the dynamical mass M_L(<r) = [G(r)/G_N] M(<r) (an assumption,
  labelled).

## 3. Implementation (this lane's own code; record code exec'd read-only for data and statistics)

### 3.1 Engines
- **Spherical shells (sph):** for a shell of mass m at radius s, exact Newton and Yukawa fields
  (Yukawa: r > s: G m [sinh(μs)/(μs)] e^{−μr}(1 + μr)/r²; r < s: −G m e^{−μs}[μr cosh(μr) − sinh(μr)]/(μ s r²), written
  with combined exponents to avoid overflow); g_MOG = (1 + α) g_N − α g_Y, summed over shells of the source's dM.
- **Razor-thin disc (disc):** g_MOG = g_N + α δg, δg ≡ g_N − g_Y. δg is obtained from the component's in-plane Newtonian
  field by the order-1 Hankel multiplier m(k) = 1 − k/√(k² + μ²) (the in-plane Yukawa / Newton transfer ratio of a thin
  sheet is k/√(k² + μ²)), using `scipy.fft.fht` (FFTLog) on a log grid. g_N is extended ∝ R inside the first data point and
  ∝ R⁻² beyond the last (no mass beyond the last point: P4's convention). δg's kernel [1 − e^{−μd}(1 + μd)]/d² is smooth, so
  the result depends on the mass distribution only on scales ≳ 1 kpc.

### 3.2 SPARC tile (a)
- Data and conventions: P4's (`P4_v3_galaxy_tiles/p4_v3_galaxy_tiles.py`: `load_sparc_own`, `gal_arrays`, `chi2_offset`,
  `fit_sample`, `pooled`, `t1_line`, `chi2_label`, `UPS`, exec'd read-only from its source text). 175 galaxies, CFG695's
  mask; V_bar² = sign(V_gas)V_gas² + Υ V_disk² + 1.4 Υ V_bul².
- **PRIMARY geometry:** gas and stellar disc razor-thin (MR13 Eq. 34), bulge spherical (shells of M_bul(<r) = r V_bul²/G,
  P4's spherical mass function). Prediction g_MOG(Υ) = g_gas + Υ g_disk + 1.4 Υ g_bul (MOG is linear in the source).
- **Variant G-SPH:** P4's spherical approximation for every component (M(<r) = r V_bar²/G; uniform core inside the first
  point; constant mass beyond the last), sph engine.
- **Υ:** one per galaxy on P4's grid 0.30–1.20 (step 0.01), the rms fit with P4's eV-only weights; the χ² line refits Υ with
  P4's covariance (P4's disclosed reading). Nothing else is free. No external field (MOG has none).
- **Line (P4 T1, unchanged):** rms ≤ 0.110 dex AND median per-galaxy Υ ∈ [0.50, 0.80]. χ² line (P4): fraction of galaxies
  with p ≥ 0.001 ≥ 0.90 PASS, 0.75–0.90 MARGINAL, < 0.75 FAIL; reported as a caveat, never changes the class (as in P4).
- Reported, no weight: χ²/dof; the fraction of galaxies pinned at Υ = 1.20 or 0.30; P4's small (M_b ≤ 3e9 M☉, M_b =
  1.33 M_HI + Υ L[3.6]) / large class mean residuals at each galaxy's best Υ; Newton (α = 0) with the same freedom; the law
  reproduced (both footings).

### 3.3 Cluster tile (b)
- Data: X2's committed replay `X2_cluster_outskirts/x2_replay_percluster.npz` (equal to F1's measurement by X2 R1/R2), with
  F1's functions and X2's `gas`, `model`, `redfac`, `stats`, `A_band`, `jk`, projector functions exec'd read-only from their
  source texts (sha256 recorded). 326 clusters, bins 0.15–3 Mpc, MID bins 3–5, OUTER bins 6–7, F1's 30 RA patches.
- **Cells:** h = 0.672 and 0.686 (MOG has no a₀, so no footing split). The law is reproduced in its 4 cells.
- **Setups:**
  - **C0 = F1 PRIMARY:** eRASS1 Mgas500 × q^{5/2}, R500 × q; β = 2/3, r_c = 0.15 R500, cut at 3 Mpc; f* = 0.20; F1's data
    boost; catalogue miscentring; jackknife errors (σ_jk); χ²_stat.
  - **C\* = X2's corrected baseline without (c1):** gas (a1) (CFG814, r⁻³ beyond 2.2 R500); reduced shear (d) forward-modelled
    with MOG's own Σ; systematics (e) (σ_tot, χ²_sys). (c1) is inapplicable (no EFE in MOG).
- **PRIMARY prediction (P-PH, MRT18 Eq. 32 / MR13 Eq. 21):** Σ_MOG = (1 + α) Σ_N(baryons), ΔΣ_MOG = (1 + α) ΔΣ_N(baryons),
  miscentred as F1 (X2's floored projector).
- **Variant V-DYN (the brief's reading):** lensing from the dynamical field, M_L(<r) = r² g_MOG(r)/G_N with g_MOG from the
  sph engine on the cluster baryons; ρ_eff = (1/4πG_N r²) d(r² g_MOG)/dr projected as F1 / X2.
- **Statistic (X2's `stats`, unchanged):** A_band = Σ W D B / Σ W P; Z_band = (A − 1)/σ; profile χ² over bins 3–7 with the
  jackknife covariance and Hartlap factor (C\*: plus the rank-1 null templates).
- **Line (X2 §3 fixed-form pass line, unchanged):** profile χ² ≤ 11.07 AND |Z_MID| ≤ 2 AND |Z_OUT| ≤ 2, in both h cells.
- Reported, no weight: INNER band; terciles of catalogue Mgas500 at C0 (X2's split); Newtonian baryons; the law at C0 and C\*
  (C\* law values read from X2's JSON, which include its (c1)).

## 4. Frozen verdict classes

**SPARC (a):** **PASS** iff P4's line passes in the PRIMARY geometry and in G-SPH; **FAIL** iff it fails in both;
**UNDECIDED** otherwise (geometry-dependent; named). Qualifier **FRAGILE** if any (α, μ) corner, P4's Chae lognormal Υ prior,
or the Q ≤ 2 subset changes the PRIMARY line outcome; else **ROBUST**. The χ² line label is reported alongside.

**Clusters (b):** **PASS** iff the line is met at C0 AND at C\* (P-PH); **FAIL** iff it is met at neither; **UNDECIDED**
otherwise, named ("MET ONLY WITH (e)", "MET ONLY AT C0", or an h split). Qualifiers: **BOOST-DEPENDENT** (the clipped-boost
convention changes the line outcome at either setup), **PARAMETER-FRAGILE** (α = 8.55 or 9.23 changes it),
**PRESCRIPTION-DEPENDENT** (V-DYN changes it).

**Overall:** **MOG UNIVERSAL SET PASSES BOTH** iff (a) and (b) are PASS; **MOG UNIVERSAL SET FAILS (SPARC | CLUSTERS |
BOTH)** naming each dataset whose class is FAIL; otherwise **MOG UNIVERSAL SET UNDECIDED (which)**. S1 and S2 never enter
a class. **Finding to report either way:** whether the published literature uses a cluster parameter set different from the
galaxy set (BM06 does; MR14 does not; MRT18's α(M) differs from U).

## 5. Checks (script prints `K# PASS|FAIL value threshold`; exit 0 iff all pass)

| id | check | pass line |
|---|---|---|
| R1 | P4's SPARC loader (exec'd) == `CFG4_common.load_sparc` (bit-for-bit); CFG695 S2 reproduced (0.1009 @ 0.60 / 0.0994 @ 0.55) | equal; \|Δrms\| ≤ 1e-4, Υ equal |
| R2 | the law, isolated, per-galaxy Υ (P4 `iso_perUps`) reproduced on both footings: rms, median Υ, fraction p ≥ 0.001 | \|Δrms\| ≤ 1e-6; Υ and fraction equal |
| R3 | X2 C0 (F1 PRIMARY) law reproduced in its 4 cells: A_MID, A_OUTER, σ_jk, χ²_stat vs X2's JSON | ≤ 1e-6 in A, σ; ≤ 1e-3 in χ² |
| R4 | X2's single-change law rows (a1), (d), (e) reproduced in 4 cells (A, σ_tot, χ²) | ≤ 1e-6; ≤ 1e-3 |
| R5 | F1's Newtonian baryons at h 0.70 (record recipe): A_MID 9.824, A_OUTER 7.388 (F1 JSON `newton_h070`) | ≤ 1e-4 |
| K1 | sph engine, compact Plummer (a = 1e-3 kpc): g_MOG(r)/(G_N M/r²) vs the closed form 1 + α − α e^{−μr}(1 + μr) at r = 0.5–300 kpc, **reference with the published α, μ** | max rel ≤ 1e-3 |
| K2 | disc engine vs direct 2-D quadrature of the exact exponential Σ (R_d = 1, 3, 6 kpc; R = 0.25–10 R_d): g_MOG with g_N from Freeman's formula; **reference with the published α, μ** | max rel ≤ 5e-3 |
| K3 | disc engine convergence: log grid ×2 points and range ×10 at both ends, every SPARC galaxy at Υ = 0.5 | max \|Δ log g\| ≤ 1e-3 dex |
| K4 | sph engine vs the exact uniform-sphere Yukawa field (interior + exterior matched solution, solved in-code), r = 0.1–5 a; **reference with the published α, μ** | max rel ≤ 1e-3 |
| K5 | peak RSS | < 1 GB |

**`--mutate`:** the engines use α = 0 (pure Newton) while the K1, K2, K4 references keep the published α, μ: K1, K2, K4
must FAIL (exit 1). It also prints, as information, that MOG(α = 0) reproduces the Newtonian SPARC and cluster numbers.
Writes `x9_mog_stvg_check_MUTATE.out`, `x9_mog_stvg_check_results_MUTATE.json`.

## 6. Rules

`x9_mog_stvg_check.py` → `x9_mog_stvg_check.out`, `x9_mog_stvg_check_results.json`. Runs: `OMP_NUM_THREADS=1 nice -n 15`,
< 1 GB RSS, ≤ 30 min; the live heavy queue is never touched. No downloads; no fitting of α, μ or Υ beyond P4's per-galaxy
convention; no scans. Pathspec commits of this lane only; never push. Any later change: an append-only AMENDMENTS section,
each labelled PRE-RESULT or POST-RESULT.

## AMENDMENTS (append-only)

**A1 (PRE-RESULT, implementation; written after synthetic engine tests only, before any SPARC or cluster number of MOG).**
A development test of the disc engine on Freeman exponential discs sampled at 0.25–10 R_d (40 points) gave a max relative
g_MOG error of 0.42 % / 0.60 % / 0.48 % (R_d = 1 / 3 / 6 kpc) against the direct 2-D quadrature, i.e. K2 as frozen would
fail at R_d = 3 kpc. Sampling to 30 R_d brings the agreement to ≤ 6e-5 in δg. The difference is not numerical: it is the
declared extension rule B6 (g_N ∝ R⁻² beyond the last sample), which for a disc truncated at 10 R_d implies a slightly
different mass distribution near the edge than the true exponential disc (mass beyond 10 R_d: 5e-4 of the total). So K2,
which is meant to test the numerics, samples the exponential discs at 0.05–30 R_d (600 points) and is still evaluated at
R = 0.25–10 R_d with the same 5e-3 line. The truncated-sampling number is printed as diagnostic **D-EXT** (no weight): it
bounds the effect of rule B6 on a disc at ≲ 0.6 % in g (≲ 0.003 dex), far below P4's 0.110 dex line. Nothing else changes.

**A2 (POST-RESULT for K5 only; numerics, no line, threshold or input changed).** Run 1 stopped at the script's RSS guard
(0.958 GB macOS ru_maxrss, after K1–K4, R1, R2, K3; no MOG number printed). Run 2 (same code plus an env-flagged RSS trace in
the log lines) completed with SPARC FAIL (ROBUST), CLUSTERS FAIL and K5 FAIL at 1.051 GB; its `.out` was overwritten by the
next run and is not kept. The cause was the size of vectorised temporaries in the K2 quadrature, the shell sums and the
cluster Yukawa matrix. The chunk sizes were reduced (quadrature 500 → 50 rows; shell sums ≤ 1e5 elements per block; Yukawa
matrix 500 → 40 rows); the arithmetic per element is unchanged. Run 3: 10/10 PASS at 0.418 GB, classes unchanged. The trace
(`X9_RSS_TRACE=1`) is off in the committed runs.

**A3 (POST-RESULT diagnostic, no class weight).** After seeing that the cluster outcome is driven by the OUTER band
(A_OUTER ≈ 0.65 in every graded reading), the script also reports P-PH with the gas beyond R500 reduced: X2's bracket (a3)
(ρ ∝ r⁻³ from R500) and F1's C3c G2 (gas inside R500 only), at both setups, and the corner most favourable to MOG (G2 gas,
clipped boost, α = 8.55). These rows test whether the FAIL rests on the β-model extrapolation of the gas to 3 Mpc. They
never change the frozen class.

**A4 (POST-RESULT, text only).** §1's transcription of MR13 Table 1 understated the per-galaxy μ range. It is 0.018–0.22 kpc⁻¹:
DDO 154 has μ = 0.22 ± 0.03, IC 2574 0.12, NGC 925 0.11. The three LSB galaxies therefore sit at α ≈ 13–14 and
μ ≈ 0.11–0.22 kpc⁻¹. The table is reported only and is never used, so no input, line or class changes.
