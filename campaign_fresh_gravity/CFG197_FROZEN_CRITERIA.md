# CFG197 — a gas-independent ("gas-floor") bound on a₀(z) from z > 3.5 discs: FROZEN CRITERIA

Written 2026-09-29, before any dynamical-mass, rotation-velocity or dispersion column is used in a computation, and before the pre-flight (`CFG197_gas_floor_highz/CFG197_preflight.py`) was run. The lemma script (`CFG197_bound.py`) is pure mathematics and ran first. Nothing below may change after a phase-2 number is seen. Any later deviation goes in the README as a disclosed departure. Status: phase 1; the orchestrator reviews and commits this file before phase 2.

## The idea, and the lemma it rests on

- Take any algebraic law g_obs = ν(g_bar/a₀) g_bar. At radius r, set:
  - x = g★(r)/a₀;
  - μ = g_gas(r)/g★(r) ≥ 0.
- The predicted ratio of dynamical to stellar acceleration (M_dyn(<r)/M★(<r) in spherical-equivalent units) is:
  - F(μ; x) = (1 + μ) ν((1 + μ)x) = Φ((1 + μ)x)/x,
  - where Φ(y) = y ν(y).
- `CFG197_bound.py` proves the lemma:
  - dF/dμ = Φ′((1 + μ)x), so F ≥ ν(x) for any gas amount if and only if Φ is non-decreasing.
  - P2: Φ = √(y² + y), with Φ′ > 1.
  - ν_mono: Φ′ ≥ 1 + 0.05 H_P/(y + Y_P) > 1, checked on the committed table.
  - Both pass the record's own C_L = Φ′ − 1 > 0 health condition (FP1 B4). That also gives the stronger F ≥ ν(x) + μ.
  - A switch law with a decreasing stretch of Φ breaks the bound (L5). The floor must not be applied to such a law.
- **The required stellar-mass rescaling.** If M★ is multiplied by s, the law survives with some μ ≥ 0 only if s ≤ s_req = Φ⁻¹(x R_obs)/x, where R_obs is the observed ratio.
  - log s_req < 0 means M★ must be overestimated for the law to survive.
  - Newton: s_req = R_obs.
  - P2: s_req = (√(1 + 4x²R_obs²) − 1)/(2x).
- **A structural asymmetry, stated up front (L4).** s_req rises with x. The rival's x is x_flat/E(z).
  - So the rival ALWAYS needs a smaller s_req than the flat law on the same data.
  - The floor can single out the rival. It can never single out the flat law.
  - The flat law can lose only together with the rival, or to Newton.
  - ΛCDM (Newton plus unseen mass) has the lowest floor, 1, and is always at least as consistent as the flat law here.
  - So a CONSISTENT flat law is the survival of a one-sided bound. It is never evidence for the framework.

## Premises (declared, not derived)

1. The algebraic relation holds locally at r: no external field, no non-local phantom correction.
   - An external field e (in units of a₀) lowers the effective floor to about ν(x + e).
   - For any DISFAVOURED bin, phase 2 reports the e that would restore consistency. This is reported only and changes no verdict.
2. g_gas(r) ≥ 0.
   - This is exact in spherical symmetry.
   - For a disc it fails only for gas with a central depression, such as a ring outside r.
3. The circular speed the paper reports measures g_obs at the stated radius: V_circ²/r. The kinematics trace the potential, not outflows or mergers.
4. M★ is the catalogue's SED value. Its error is the tabulated one.

## Laws, kernels, footings

- **Flat:** a₀(z) = a₀.
- **Rival:** a₀(z) = a₀ E(z), with E = √(Ω_m(1 + z)³ + 1 − Ω_m) and Ω_m = 0.3153 (Planck 2018; `CFG7_common.OM_PL`).
- **Newton** (ν = 1) is the reference floor, 1.
- **a₀ footings:** 9.3603e-11 and 1.1312e-10 m s⁻² (via `CFG4_common`). Both are always reported. κ = ½ is FITTED.
- **Kernels:** P2 = √(1 + 1/y) is primary. ν_mono (the committed FP1 table) is reported.

## Samples, bins and in/out rules (catalogue flags only)

All files are in `data_assembly/arxiv_tables/`. Nothing is fetched.

**Primary bin, z > 3.5.** One verdict per law for the pooled bin. The two sub-bins are also reported.

- **Hα sub-bin: Danhaive+2025 gold** (`danhaive2025_gold.csv`, 41 galaxies, z 3.80–5.82).
  - All 41 are in. `logMstar_lim`, `re_kpc_lim`, `logMdyn_lim` and `v_over_sigma0_lim` are empty for every row.
  - 17 rows carry σ₀ "<" (an upper limit). They are in the primary. The declared variant **V-lim** excludes them.
- **[CII] sub-bin: ALMA-CRISTAL** (`cristal2025_dynamics.csv` joined to `cristal2025_sample.csv`; ID "09" is "09a").
  - The 14 dynamically modelled discs, minus those with no SED M★ in the sample table (10a-E and 23c; their paper sets M★ = M_dyn − M_gas, which is circular).
  - That leaves 12.
  - Rows whose R_e,disk is fixed (no error: 12 and 15) are in and flagged.
  - Non-disc and unmodelled rows are out.
- **Pooling rule.** If the two sub-bins give opposite verdicts for a law (one DISFAVOURED, the other CONSISTENT), that law's z > 3.5 headline is NON-DIAGNOSTIC.

**Comparison bins.** Each survey is its own bin; they are never pooled.

- **MSA-3D** (`msa3d_galaxies.csv` + `msa3d_kinematics.csv`, 30 galaxies, z 0.58–1.68).
  - All 30 are in.
  - Flagged: footnote a (the kinematic tracer is [OIII], not Hα), footnote b (an HST radius), and the one σ₀ row marked "dagger".
  - Variant: the 23 golden only.
- **KURVS-CDFS** (`kurvs2023_*.csv`, z 1.22–1.62).
  - Primary: the 10 rotation-supported discs that have the paper's f_DM(<R_eff) (the rows of `kurvs2023_fdm.csv`).
  - The `flag_star` row is flagged.

**Measured-gas subset: Roman-Oliveira+2023** (z 4.26–4.43), for the gas-side test below.

- Four sources have kinematics: BRI1335-0417, J081740, SGP38326-1, SGP38326-2.
- AzTEC1 has none. The paper classes it as a likely merger.

**Not binned (context only).**

- **Lelli+2023** (z 1.47, 2.24): no SED M★ or stellar radius in the tables, and the paper states V²/R > 3–4 a₀.
- **ALPAKA-JWST** (z 0.56–2.10): M★ there is a dynamical-fit quantity with a free gas normalisation, and no r_e is tabulated.
- Both are at z < 3.5.

## The radius, M★(<r) and the geometry of g★

**The radius r** is where each paper evaluates its velocity:

| sample | r | note |
|---|---|---|
| Danhaive | Hα r_e from geko | its prior is the UV size × 1.58 |
| CRISTAL | R_e,disk from DysmalPy | Gaussian prior on the [CII] size. It is a kinematic-fit output, which is disclosed; it is not a stellar-light radius |
| MSA-3D | R_e,disk from DysmalPy | the disc's half-mass radius in the dynamical model |
| KURVS | R_eff | HST near-IR; the radius of the paper's f_DM |

**The stellar mass inside r:**

- **Primary: mass follows light.** M★(<r) = M★/2.
- **Declared alternative, "compact stars".** The stellar half-mass radius is r/1.58 (Danhaive's UV-to-Hα size factor, inverted). For an exponential disc this gives M★(<r) = 0.7425 M★.
  - This alternative is adverse to every law, Newton included.
  - It is justified by emission-line and light-weighted sizes exceeding mass-weighted ones. That choice is not taken from these data.

**The geometry of g★(r) = f_geo G M★(<r)/r²** (a sensitivity):

- f_geo = 1: the sphere (primary).
- f_geo = 2/1.8 = 1.111: the q₀ = 0.2 thick disc implied by Price+2022's k_tot = 1.8, which Danhaive use.
- The exact razor-thin exponential disc (Freeman). At R_e this is 1.2503; the compact-stars thin disc gives g★R²/(GM★) = 0.9966.

**The KURVS 3 R_D sensitivity:** M★(<3R_D) = 0.8009 M★, with R_D = R_eff/1.68. The seeing convolution of R′ is ignored (declared).

## The observed ratio R_obs = g_obs(r)/g★(r) (phase 2 only)

- **Danhaive primary (the paper's own M_dyn).**
  - M_dyn = k_tot r_e v_circ²/G, with k_tot = 1.8 and v_circ² = v_rot² + 3.36 σ₀².
  - So g_obs = G M_dyn/(1.8 r_e²), and R_obs = [2/(1.8 f_geo)] × 10^(logMdyn − logMstar).
  - With f_geo = 1.111 this is the paper's own ratio exactly.
- **Danhaive sensitivity (recomputed).**
  - v_rot = (v/σ₀) σ₀ and v_circ² = v_rot² + α σ₀².
  - α ∈ {3.36 (Burkert 2010, the paper's), 1.68 (the surface-density-gradient term R/R_d alone, without Burkert's scale-height term)}.
  - This is done only for the 24 rows with a detected σ₀. For the 17 limit rows, v/σ₀ and σ₀ are limits, so no recomputation is made.
- **CRISTAL:** v_circ² = V_rot(R_e)² + α σ₀², with α ∈ {3.36 (the paper's Burkert equation, primary), 1.68}. Then g_obs = v_circ²/R_e.
- **MSA-3D:** the same rule, with its V_rot(R_e), σ₀ and R_e,disk.
- **KURVS primary (the paper's own f_DM with its own baryon model).**
  - The baryon model is a Freeman thin disc with M_bar = M★/(1 − 0.4).
  - So g_obs = [1/(1 − f_DM)] × (1/0.6) × g★_thin(R_eff).
  - For another geometry, R_obs = g_obs/g★_variant.
- **KURVS sensitivity.**
  - The model velocity at R′_3D = 3R_D (the paper's Freeman-model value).
  - v_circ² = V² + α σ₀², with α ∈ {6.0 (Burkert at 3R_D = 3.36 × 1.787), 3.0}.
  - M★(<3R_D) = 0.8009 M★.
- **Per-galaxy log error.** The tabulated asymmetric errors are symmetrised (mean of the two sides) and added in quadrature with the log M★ error.
  - It is used only for per-galaxy flags.
  - Where M★ has no error (CRISTAL), 0.2 dex is assumed.

## The statistic

- **Per galaxy.** log s_req(L, kernel, footing, variant) = log₁₀[Φ⁻¹(x R_obs)/x], with x = g★/a₀_L(z).
  - Newton: log R_obs.
  - ν_mono: Φ is inverted numerically from the committed table.
- **Per-galaxy flag.** A galaxy is BELOW FLOOR if s_req < 1 even with R_obs raised by its 1σ log error.
- **Per bin.** The median of log s_req.
  - Bootstrap over galaxies: 4000 draws, seed 197.
  - The 5th, 16th, 84th and 95th percentiles of the median are reported.
- **Limits are handled as limits.** If any ratio is a limit, the median is bracketed:
  - one end with the limit rows at the tabulated value;
  - the other with them at −∞ (for an upper limit) or +∞ (for a lower limit).
  - A verdict must hold at both ends.
  - For Danhaive, no M_dyn or M★ is tabulated as a limit. The σ₀ limits are handled by the V-lim variant.

## Decision lines (declared before looking)

**Why the lines sit where they do.** They come from known M★ systematics, not from these data:

- SED stellar masses carry about 0.2–0.3 dex of systematic uncertainty.
  - The KURVS table note gives a typical 0.2 dex for its MAGPHYS masses.
  - A Salpeter IMF instead of Chabrier moves M★ by about 0.24 dex.
  - Danhaive's own caveat says outshining can cause an *under*estimate of M★.
- So a required global M★ overestimate larger than 2× (−0.30 dex) lies beyond the typical systematic.
- A shortfall within −0.10 dex is well inside it.

**Per law, per bin, per footing (P2 is the headline kernel; ν_mono is reported):**

- **DISFAVOURED BY THE GAS FLOOR:** median log s_req < −0.30, AND the bootstrap 95th percentile of the median < −0.10.
- **CONSISTENT:** median ≥ −0.10, AND the bootstrap 5th percentile of the median ≥ −0.30.
- **NON-DIAGNOSTIC:** anything else.

**Robustness.** A verdict counts as a headline only if it holds in every declared variant:

- the three geometries: f_geo ∈ {1, 1.111, thin};
- the pressure terms (the paper's and the moderate one);
- the two M★(<r) assumptions (mass follows light, compact stars);
- V-lim (Danhaive);
- both footings.

This rule is symmetric: it applies to a pass exactly as to a fail. A verdict that holds only in the primary is reported as "primary only", and the headline is NON-DIAGNOSTIC. If the footings disagree, both are quoted and the headline is NON-DIAGNOSTIC. If ν_mono's verdict differs from P2's, that is stated.

**ESTIMATOR-LIMITED.** Applies if Newton's bin median (= median log R_obs) is < −0.10.

- Then the bin's M_dyn/M★ scale is off in the direction no law with ν ≥ 1 can absorb, and no a₀ verdict is headlined.
- All numbers are still reported.
- This applies to both laws equally.

**What counts as the floor separating the laws.**

- Only one outcome does: the rival DISFAVOURED and the flat law CONSISTENT, both robust, in both footings, in a bin that is not ESTIMATOR-LIMITED and passed the pre-flight rule below.
- By L4 the reverse outcome is impossible.
- "Both DISFAVOURED" in a bin that is not estimator-limited is a failure of the flat law against Newton/ΛCDM. It is reported as a fail and is not explained away.
- In no case does any sentence say the data favour the framework.

## Pre-flight discriminability rule (frozen before the pre-flight ran)

The pre-flight uses only M★, r and z. For each bin, with P2, each footing and the primary variant:

- **D0** = −median log s_req^rival(R_hyp), with R_hyp = ν_P2(x_flat).
  - This is a gas-free, dark-free population sitting exactly on the flat floor. Its flat s_req is exactly 1.
  - **CAN** discriminate if D0 ≥ 0.30 in both footings.
  - **MARGINAL** if 0.20 ≤ D0 < 0.30 in either footing.
  - **CANNOT** if D0 < 0.20 in either footing.
- **D_μ for μ ∈ {0.5, 1, 2}** is also reported. It uses flat-law populations with gas μ inside r: R_hyp = (1 + μ) ν_P2((1 + μ) x_flat).
  - If D₁ < 0.30, a flat-law population as gas-rich as the CRISTAL paper reports (median f_molgas 0.51, so μ ≈ 1) would NOT put the rival past the line.
  - The pre-flight states this plainly: the test's power then rests on the galaxies being gas-poor inside r.
- Also reported: the floor separation Δlog floor = log ν(x_rival) − log ν(x_flat), against the 0.2–0.3 dex M★ systematic.
- **What a CANNOT bin means.** Only the flat-vs-rival claim becomes NON-DIAGNOSTIC by construction. Phase 2 still computes every bin, because the flat law's absolute verdict against Newton must be read in every bin, whatever the pre-flight says.

## The gas-side test (Roman-Oliveira, measured CO gas)

- **What can be done from disk.** None of the four kinematic sources has a stellar mass on disk.
  - The only M★ in the paper's text is AzTEC1's (about 1e11 M☉, SED), and AzTEC1 has no kinematics.
  - So the two-sided test as briefed is NOT executable from disk.
- **What is frozen instead: the lower (over-prediction) side,** which needs no M★ because stars only add.
  - **The radius is r_ext,** the mean radius of the last two rings, because V_ext and σ_ext are defined as the averages of the last two radial points.
    - Primary: r_ext = (NRADII − 1) × RADSEP × (kpc/″), taking ring centres at (i + ½) RADSEP.
    - Variant: (NRADII − 1.5) × RADSEP, taking ring centres at i × RADSEP. The smaller radius is less favourable to the laws.
    - Phase 2 checks 3DBarolo's ring convention if a source is on disk.
    - The inputs come from the paper's 3DBarolo parameter table (main.tex, Table BBpar):
      - BRI1335-0417: 5 rings, 0.15″;
      - J081740: 4 rings, 0.13″;
      - SGP38326-1: 5 rings, 0.13″;
      - SGP38326-2: 3 rings, 0.12″.
    - *Correction, made before commit and before any velocity was seen:* the first draft used the outermost ring, (NRADII − 0.5) × RADSEP. That does not match V_ext's definition. The change was made after the pre-flight's first run, which used no velocity.
  - **The gas-only predicted floor.** g_floor,L = a₀_L Φ(f_g G M_H2/(r_ext² a₀_L)).
    - Primary: f_g = 0.5.
    - Variant **V-gasLow**: f_g = 0.25, covering a factor-2 lower α_CO or a quarter of the gas enclosed.
  - **The observed side (phase 2).** g_obs = (V_ext² + α σ_ext²)/r_ext, with α ∈ {0 (primary), 2}.
  - **OVER-PREDICTS:** log g_obs < log g_floor,L − 2σ in the primary and in every variant. σ combines the quoted V, σ and M_H2 errors, plus 0.3 dex for α_CO.
  - SGP38326-1/2 have approximate gas masses with no error; 0.3 dex is used.
- **The upper side** (the law under-predicts even with all the measured gas) needs M★. It is deferred until the owner approves a literature look-up for BRI1335-0417, SGP38326-1 and SGP38326-2. RO say J081740 has no stellar mass.
- **Role.** This subset changes no bin verdict. It is a per-object check.

## MUTATE controls

Each control must bite: its load-bearing check fails, and the run exits 1.

- **C1.** E(z) ≡ 1 makes the rival identical to the flat law: max |Δ log s_req| < 1e-12 over all galaxies and variants.
- **C2.** A planted galaxy with R_obs = 1.0 (M_dyn = M★), at each bin's median x:
  - log s_req < 0 for both the flat law and the rival, with both kernels and both footings;
  - Newton's log s_req = 0 exactly.
- **C3.** A planted galaxy exactly at a law's own floor (R_obs = ν(x)): log s_req = 0 to 1e-9 for that law.
- **C4.** A planted flat-law galaxy with gas μ = 1: the flat log s_req > 0.
- **C5.** The rival's s_req ≤ the flat s_req for every real galaxy (L4).
- **Pre-flight MUTATE=1.** E(z) is forced to 1 and the lemma check uses L5's switch law. The "separation > 0 in every z > 0 bin" check and the floor-validity check must then FAIL, and the run exits 1.
- **Phase-2 MUTATE=1.** R_obs is set to 1 for every galaxy. Every bin must then come out DISFAVOURED for both laws (C2 at scale), and the checks that assert the real verdicts must fail.

## Not blind: what the analyst knew before phase 2

- **Published claims read in the papers on disk:**
  - **Danhaive+2025:** "the majority" of the gold sample have M★ < M_dyn. Five systems lie "above or on the one-to-one relation"; the figure caption says six lie on it. The paper suggests underestimated σ₀ uncertainties.
  - **ALMA-CRISTAL:** its discs "tend to be baryon-dominated", with median f_DM(<R_e) ≈ 18% (range about 5–60%) and median f_molgas 0.51.
  - **MSA-3D:** golden median f_DM(R_e) = 0.63; baryon dominance at z ~ 1 is "not ubiquitous".
  - **Roman-Oliveira:** H₂ masses of 7.6e10–1.9e11 M☉, and the data README's V_rot,max range of 198–562 km s⁻¹.
- **The record's prior KURVS a₀(z) work:** CFG140/141/189 lean toward the rival, which is not a detection.
- **Inadvertent exposure during phase 1.** No computation used any of the values below.
  - **Danhaive.** While checking how limits are encoded, a grep printed five raw rows of the table (IDs 191250, 1000989, 1087148, 1015956, 1065488), including their log M_dyn, σ₀ limits and v/σ₀.
  - **CRISTAL.** A grep printed the first columns of ten rows of the dynamics table (log M_tot, R_e, B/T), plus V_rot(R_e) for three rows (10a-E, 12, 15).
- **So the test is NOT blind.** The protection is that every line above is fixed before any ratio is computed.

## Phase 2 deliverables

- `CFG197_phase2.py` → `CFG197_phase2.out`, `_results.json`, and `_MUTATE` counterparts.
- The per-galaxy s_req table, the bin verdicts, the variant grid and the RO over-prediction checks.
- A README update with disclosed departures, if any.

## Orchestrator note before commit (2026-09-29; no rule changed)
The orchestrating session re-ran `CFG197_bound.py` (21/21), `CFG197_preflight.py` (exit 0) and `MUTATE=1` (exit 1) in a scratch copy: every `.out` is identical to the lane's. The pre-flight uses only M★, r_e and z. It puts the flat law's DISFAVOURED line at R_obs 0.73–0.91 (P2; ν_mono 0.82–1.04) in the z > 3.5 bins, within about 0.1 of Newton's ESTIMATOR-LIMITED line 0.79. The rival's DISFAVOURED line is at 1.55–2.19 (P2). So in these bins the test is in practice a test of the rival, and, as L4 says, a CONSISTENT flat law carries no evidential weight. With gas equal to the stars inside r_e, which is about what CRISTAL reports, the rival is not expected to be DISFAVOURED (pre-flight D1 0.07–0.20 dex). A NON-DIAGNOSTIC outcome is the expected one unless the discs are gas-poor.
