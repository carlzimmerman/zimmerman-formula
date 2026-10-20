# CFG919 FROZEN CRITERIA: is the baryons' kinematic state (pressure vs rotation support) the selector of the law's excesses?

Block 910–919 (orchestrator reservation, LEDGER row CFG910–919). Frozen 2026-10-20 ~15:15 UTC, committed ALONE before any
script exists and before any number of this lane has been computed. Kind: HYPOTHESIS TEST (pre-registered selector test).
κ = ½ is FITTED. Footings 9.3603e-11 / 1.1312e-10 m/s² are never pooled. Raw data and framework-native quantities only (no
HMcode, BAHAMAS or ΛCDM mass function). Extra mass is cold energy, not a particle. Not "theory closed".

## 1. Question and hypothesis

**H-KIN:** at matched baryonic acceleration g_bar, the excess over the framework's prediction, E = ln(g_obs/g_pred), is set by
ONE dimensionless pressure-support measure of the system's baryons. Rotation-supported systems sit on the law;
pressure-supported systems carry the excess.

## 2. Record check (done before freezing; targeted reads only)

Rows read: LEDGER CFG820–CFG917 (headlines), CFG62, CFG140–175 (pressure-support corrections of KURVS discs: unrelated).
THEORY_CANONICAL_2026-10-18.md (lines 1–60). Relevant prior results:
- CFG828 ("rotation vs dispersion"): where dSphs overlap SPARC (g_bar ≥ 1e-12, N = 8), dwarfs sit with the discs
  (D +0.05 ± 0.07 dex). Out of range, 21 dwarfs average +0.44 dex. This is ONE cell of the present test: dwarfs vs discs.
- CFG849: B21 lenses, colour split +0.571 ± 0.115 and Sérsic split +0.536 ± 0.116 in A, degenerate.
- CFG850: with +0.123 dex on red M*, A_red 1.45 vs A_blue 1.02 (4.0σ; Sérsic 3.8σ).
- CFG851: one spheroidal excess law fitted to red lenses predicts +0.15 dex for satellite dSphs vs +0.44 observed (z +4.4).
- CFG914: no common density ordering. Headline E ranges per sector by density, globulars show no excess.
- CFG912 (not environment), CFG913 (no single local mobility law), CFG915/916 (history-label mobility contradicted /
  lock-and-release underdetermined).
- Canonical v3 addendum (10-19): "the excess tracks gas-poor, pressure-supported systems at g_bar < 1e-12".
- CFG62 used "pressure vs rotation support" as one of four split variables for debris fractions (0/20 splits; a different
  quantity).

**Verdict of the check:** no lane has tested one kinematic measure across all classes with a common form. CFG828 and CFG851 are
pieces of it. **This lane is NOT blind.** From CFG828 and CFG851 a contradiction is a plausible outcome; that is disclosed here
before any number.

**What I saw before freezing (disclosure):**
- the LEDGER headlines above;
- the code (not the outputs) of cfg828.py, cfg829.py, cfg849.py, cfg914.py lines 1–330 and cfg883.py lines 118–130;
- the CFG638 README (the kinetic system);
- column headers of these data files, plus the first data rows printed with them: SPARC_Lelli2016c.mrt; LVD dwarf csv;
  McConnachie 2012; Walker+2023 ReadMe; ATLAS3D table (1 row); Humphrey+2006 (7 rows); Baumgardt GC parameters (47 Tuc:
  ARot 5.00, σ0 11.9; NGC 288: ARot 0.42, σ0 3.1);
- the B21 file list.

I have not opened cfg914_results.json, cfg914's README or .out (except the line "[1 s, 116 MB] inputs loaded"). I have not run
anything.

## 3. Measures (one primary, one alternative; declared before looking)

**Primary f_P = fraction of the baryons' kinetic energy in random motion = 3σ² / (v_rot² + 3σ²)** (σ one-dimensional):
0 = pure rotation, 1 = pure pressure. Assignment per class, with brackets used in variant V3:

| class | f_P primary | basis | V3a (less pressure) | V3b (more extreme) |
|---|---|---|---|---|
| DW: 83 LVD dwarfs (CFG880 sample) | 1.0 (v/σ ≈ 0) | class value; no rotation data on disk (Walker+23 per-star velocities have no membership column) | 0.923 (v/σ = 0.5); 0.75 (v/σ = 1) for the HI-bearing dwarfs (LVD mass_HI > 0) | 1.0 |
| SS/SL: SPARC rotators (CFG828/914 selection; Mb ≤ / > 3e9) | per galaxy, σ = 10 km/s, v = V_flat (Table 1); if V_flat = 0, the largest quality-cut V_obs | measured v; σ declared | σ = 20 km/s | σ = 6 km/s |
| LD: B21 disc lenses (Sérsic n < 2) | 0.20 (v/σ ≈ 3.5) | PROXY: lensing has no kinematics; n is a structural proxy for the central galaxy's support | 0.43 (v/σ = 2) | 0.10 (v/σ = 5) |
| LS: B21 spheroid lenses (n > 2) | 0.80 (v/σ ≈ 0.87) | PROXY, as above | 0.57 (v/σ = 1.5) | 0.97 (v/σ = 0.3) |
| CL: eRASS1 clusters (CFG687 shear stack) | 1.0 | ICM is hydrostatic gas: its kinetic energy is thermal (random) | 0.90 | 1.0 |
| GC: 31 tidally safe globulars (CFG883) | per GC from Baumgardt: v/σ = ARot/sigma0 | measured; missing → class median | σ_global = 0.7·sigma0 | as primary |

**Alternative f_sph = fraction of the baryonic mass in pressure-supported components:**
- DW: (M*/2) / (M*/2 + M_gas,in), with CFG880's gas_in; gas is counted as rotation-supported (conservative).
- SPARC, per point: 0.7·Vb|Vb| / (Vg|Vg| + 0.5·Vd|Vd| + 0.7·Vb|Vb|), clipped to [0, 1]. Galaxy value = mean over its points.
- LD 0.15 and LS 0.70: B/T proxies.
- CL 1.0. GC 1.0.

Limitation stated up front: lensing measures g_obs at 30–300 kpc, while the kinematic state is that of the central galaxy.

## 4. Classes, inputs and E

**Inputs: identical to CFG914, its input section exec'd read-only** (dwarfs, SPARC, B21 lenses, eRASS1 clusters, globulars):
- E = ln(g_obs/g_law). For dwarfs E = 2 ln(σ/σ_law).
- Globulars: E against the framework's screened (Newtonian) baseline, as in CFG914. The law+EFE baseline is variant V4.
- Lenses: the B21 Sérsic bins are the primary lens classes, with +0.123 dex on the n > 2 lenses' M* (the CFG850 correction).
  Lens window 1e-13.3 ≤ g_bar < 1e-10.9 (CFG914's LWIN).
- Clusters: CFG687 radial bands MID+OUTER (jsel 3–7), with CFG687's own FP0 a0 as in CFG914.

**Classes NOT TESTED** (declared):
- **Early-type galaxies with dynamics.** ATLAS3D on disk has JAM M/L but no kinematic-state column (no λ_R or V/σ) and only
  IMF-dependent stellar M/L. The PN tables cover about 6 galaxies and would need new Jeans modelling with free anisotropy.
  No committed framework-native per-object E exists. The n > 2 lenses stand in for early types.
- **Within-class kinematics of dSphs and clusters:** no data.

## 5. Cells (matched g_bar)

**Windows:** fixed 0.5-dex edges in log10 g_bar, the CFG914 GRID (…, −13.0, −12.5, …). One cell per class per window.

**Estimators** (CFG914 conventions):
- DW and GC: per-system mean, se = max(std/√n, √Σσ²/n), n ≥ 3.
- SPARC: mean of galaxy means, ≥ 5 galaxies, 1000-draw galaxy bootstrap covariance across windows.
- Lenses: GLS amplitude A per window with the B21 covariance. E = ln A, kept if A > 0 and sA/A ≤ 1. Covariance propagated
  across windows.
- Clusters: stacked amplitude per window, ≥ 20 distinct clusters, 30-patch RA jackknife covariance.

**Per-cell values:**
- Cell f = mean member f; for SPARC, the mean over contributing galaxies.
- Systematic floor 0.05 dex in g (0.1151 in E), added in quadrature to every cell's diagonal: σ_tot.

## 6. Tests (per footing; all thresholds frozen)

Labels:
- "rotating": cell f ≤ 0.3.
- "pressure": cell f ≥ 0.7.
- GC-based elements are labelled **STIFFNESS-CONDITIONAL** and carry **no class weight**. Reason: the canonical stiffness
  (L* ≥ 24 pc, CFG820) would screen any cold-energy effect at globular radii.

**C1, a rotating system with the excess.** A rotating cell with E/σ_tot ≥ 3 that also either:
- if the window holds non-GC pressure cells: has E ≥ Ē_P − 2√(σ_tot² + σ_P²), where Ē_P is their inverse-variance mean;
- otherwise: has E ≥ 0.345 (0.15 dex).

**C2, a pressure-supported system on the law at the same g_bar.** A pressure cell i with E_i < 2σ_tot,i, such that some cell j
in the same window has f_j ≤ f_i and (E_j − E_i)/√(σ_tot,i² + σ_tot,j²) ≥ 3.

**Within-class ordering** (a violation is significant anti-ordering only):
- W1, lenses: in the combined lens window, (E_LS − E_LD)/σ ≤ −2 is a violation.
- W2, SPARC (SS ∪ SL): take each galaxy's residual ε_g = mean over its points of [E_p − median SPARC E in the same 0.25-dex g_bar
  bin]. Spearman(f_P,g, ε_g) with ρ < 0 and p < 0.01 is a violation. Caveat: f_P is monotone in V_flat, so this is
  confounded with mass.
- W3, GC: Spearman(f_P,i, E_i) with ρ < 0 and p < 0.01 is a violation (STIFFNESS-CONDITIONAL).

**Common forms**, one free parameter A each, GLS over all non-GC cells with block covariance plus floor:
- **F1 (smooth):** E = A·f.
- **F2 (step):** E = A·Θ(f − 0.5). The threshold f = 0.5 ⇔ v/σ = √3 is fixed.

A form's grading:
- **PASS:** χ² p ≥ 0.05 (dof = N_cells − 1) and max class |z_c| ≤ 3. Here z_c = GLS mean residual of the class's cells over its
  standard error.
- **FAIL:** p < 0.01 or max |z_c| > 3.
- **MARGINAL:** otherwise.

**Secondary diagnostics (no class weight):**
- F3: E = A·f·Θ(g_bar < 1e-12), the canonical's dwarf onset. This asks whether kinematics plus an acceleration gate (two
  posits) could work.
- F1/F2 refits with the GC cells included.

**Ordering statistic** (used for MUTATE): T = mean over eligible same-window pairs (|Δf| > 0.1, non-GC) of
sign(f_i − f_j)·tanh((E_i − E_j)/σ_ij), with σ_ij = √(σ_tot,i² + σ_tot,j²).

## 7. Classes

**Coverage** requires ≥ 4 non-GC classes with cells, including ≥ 1 rotating class and ≥ 2 pressure classes. Otherwise the
class is NOT DIAGNOSTIC.

**Per footing (V0 primary):**
- **SELECTOR CONTRADICTED:** C1, or a non-GC C2, or a non-GC W violation, or F1 FAIL and F2 FAIL.
- **SELECTOR SUPPORTED:** none of the above, and F1 or F2 PASSes with A/σ_A ≥ 3.
- **NOT DIAGNOSTIC:** otherwise.

**Overall:**
- CONTRADICTED only if CONTRADICTED on both footings; SUPPORTED only if SUPPORTED on both.
- Otherwise SPLIT BY FOOTING → NOT DIAGNOSTIC, with both reported.

**Variants** (reported per footing; if any variant changes either footing's class, the class is labelled **FRAGILE**, but not
changed):
- V1: alternative measure f_sph.
- V2: colour lens bins (blue = LD proxy, red = LS proxy) instead of Sérsic.
- V3a / V3b: the f brackets of section 3.
- V4: GC against law+EFE.
- V5: clusters with the INNER band added.
- V6: floor 0.10 dex.
- V7: no +0.123 M* shift on the n > 2 / red lenses.

## 8. Controls

Any K failure stops the lane: no class is reported.

**K-tests:**
- **K1:** CFG828 reproduced through this lane's own SPARC/dwarf/law code. N_in, mean_D, se_D, sparc_median_all and
  out_of_range_mean_delta for canonical|nu_e and alt|nu_e must match cfg828_results.json to ≤ 1e-9. The bootstrap stream is
  default_rng(828) in CFG828's loop order.
- **K2:** CFG829 reproduced with this lane's own B21 loader and GLS. The window A and sA of the blue and red lenses (canonical|nu_e
  and alt|nu_e) must match to ≤ 1e-9, and the class "LAW HOLDS AT LOW g" must be recovered.
- **K3:** CFG849's Sérsic disc/sph A (both footings) must match to ≤ 1e-9.
- **K4:** every internal input check of CFG914's input section (K1, K1b, K2a, K2b, K3, K3b, K4a, K4b, K5) must PASS when exec'd
  here.
- **K5:** the Baumgardt ARot/sigma0 parse must give 47 Tuc = 5.00 / 11.9 exactly, and every f_P must lie in (0, 1].

**MUTATE (CFG919_MUTATE=shuffle → `cfg919_MUTATE_shuffle.out` / `cfg919_results_MUTATE_shuffle.json`; exit 1 = bites):**
- S1: take one F1-injected cell set (A_inj = 1.0, rng 919). Shuffle the cell f labels 1000 times (rng 9191), with the verdict
  from cell-level criteria only (C1, C2, F1, F2). The shuffled versions must lose the ordering: SUPPORTED in ≤ 10% of shuffles,
  and median T_shuf ≤ ½·T_true.
- S2: on the real cells, report T_true and its permutation p-value (no class weight).

**INJECT (CFG919_MUTATE=inject → `cfg919_MUTATE_inject.out` / `cfg919_results_MUTATE_inject.json`; exit 0 = recovered):**
- Cell E is replaced by the planted signal + ε, with ε ~ N(0, block covariance + floor²): 200 realizations per footing
  (rng 919).
- Member-level W tests get the planted signal A·f_i + N(0, s), where s = member σ (GC) or the sd of the real ε_g (SPARC).
- Required:
  - **I1** (E = 1.0·f): SUPPORTED in ≥ 90% of realizations, and |Â_F1 − 1|/σ_A ≤ 2 in ≥ 90%.
  - **I2** (E = 1.0·Θ(f − 0.5)): SUPPORTED in ≥ 90%.
  - **I0** (E = 0): SUPPORTED in ≤ 10%.

## 9. Theory note (in the README)

State whether CFG638's system can depend on the baryons' kinematic state at fixed g_bar:
- v_s = −α 1_B 1_C τ ∇ψ;
- ∇²ψ = 4πG(ρ_ph − ρ_c);
- τ = (4πGρ_m)^−½;
- bath target σ_J².

If it cannot, say so plainly, and list a kinematic selector as a NEW POSIT.

## 10. Compute and hygiene

- Compute: one core (OMP_NUM_THREADS=1, nice -n 10), < 1 GB, one process at a time. Nothing downloaded. No other lane's files
  edited (CFG914/880/883/828/829/849 exec'd or read only).
- Commits: explicit paths only.
- Any post-hoc change will be a dated, labelled amendment (AMENDMENT_A*.md), committed before the numbers it affects are
  reported.
