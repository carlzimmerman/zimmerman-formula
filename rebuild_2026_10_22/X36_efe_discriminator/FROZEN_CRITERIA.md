# X36_efe_discriminator — FROZEN CRITERIA (committed with ASSUMPTION_LEDGER.md, alone, before any script or number)

κ = ½ FITTED. Footings a₀ = 9.3603e-11 (canonical) / 1.1312e-10 m/s² (alt), never pooled. No dark-matter particle. Not
"theory closed". Nothing here says the data favour the framework. Naming: the cold w ≈ 0 clumping component is **cold dark
energy** (a gravitating field component paired with dark energy; not matter, not a particle). "Dust-like" describes only its
clustering. ΛCDM is the external rival's name. Compute: one thread, `nice -n 15`, < 1 GB RSS, minutes, PYTHONHASHSEED=0, no
downloads, `compute_queue/` untouched. Other lanes are read only.

## 0. The question

X33 (`rebuild_2026_10_22/X33_system_atlas`) found, FDR- and Bonferroni-significant, that large SPARC galaxies' residual against
the isolated law falls with log e_ext (Spearman ρ −0.455 canonical, N 68). Two readings of the galaxy law are live after the
v3s verdict (`covariant_push_2026_10_22/V3S_FINAL_VERDICT_2026-10-24.md` §7–8) and EM1 (`rebuild_2026_10_22/EM1_emergent_dust_law`):

- **(a) law fundamental (v3s):** AQUAL, μ = x/(1+x), with the exact external-field effect (EFE). A galaxy in a stronger external
  field sits below the isolated law at its outer radii.
- **(b) route E (law emergent):** cold dark energy clumps everywhere as dust-like halos; there is no law force and no EFE term;
  the RAR is a halo-response regularity.

**Is X33's e_ext trend reproduced by (a), by (b), by neither, or by a confound? Does it discriminate (a) from (b)?**

## 1. Step 0 (stop rule: any FAIL stops the lane; a dated AMENDMENT is written before anything else is run)

- **S0a EM1 rerun.** A scratch copy of `em1_emergent.py` (path constants patched to absolute repo paths; nothing else changed)
  in `X36_efe_discriminator/step0_em1/` is run in default and `--ups05` modes; outputs stay in that scratch folder. PASS iff
  every number in EM1's committed JSONs that the EM1 README quotes is reproduced: R1 rms (to 1e-4), median Υ (exact), (a, b)
  (exact) on backgrounds A and B; UPS05 dust rms (to 1e-4) on A and B and the law at Υ 0.5 on both footings (to 1e-4); R3 g†
  model (to 1e-3 relative); EM1's own checks all PASS. EM1's directory is not written.
- **S0b X33 trend.** From `x33_atlas.csv` alone: Spearman ρ(resid_dex_f, log e_ext) for SPARC subclass "large" and for all SPARC
  with e_ext, both footings, equals `x33_findings.json` to 1e-9 (ρ) and N exactly.
- **S0c residual identity.** My per-galaxy residual at X33's convention (median along the curve of log g_obs − log g_iso,
  g_bar at CFG695's global Υ U₀ per footing, bulge 1.4 Υ) equals `resid_dex_can/alt` in the atlas for every SPARC row to 1e-9.
- **S0d P4 EFE machinery.** With P4's own functions (copied verbatim from `p4_v3_galaxy_tiles.py`: `sparc_mass_fun`,
  `sparc_solve`, `ratio_solve`, `interp_nodes`, `fit_sample`, `pooled`; solver `p4_solver.py` imported read-only), the L★ = 0
  per-galaxy-Υ pooled rms with the EFE solved (Chae primary e_N) equals P4 `T1.footings.f.L0.rms` to 1e-4 and the median Υ
  exactly, both footings.
- **S0e route-E halos.** My implementation of EM1's NFW + Bullock c(M) + global relation, run by EM1's own grid fit, returns
  EM1's (a, b) exactly for R1 (per-galaxy Υ) and UPS05 (Υ 0.5), backgrounds A and B.

## 2. Sample and the residual frames

- **Primary sample S_L:** SPARC subclass "large" (X33: M_b > 3e9 M☉ at canonical U₀) with a Chae+21 environment (N 68).
  **Secondary S_A:** all SPARC with an environment (N 109). Reported both; the verdict uses S_L.
- **e_ext axis:** X33's column (Chae+21 log e_N = mean of the max- and no-clustering brackets, converted to the field by the
  v3 law at the canonical a₀, in units of canonical a₀). Footing-own axis reported.
- **Υ conventions** (each evaluated self-consistently: measured and predicted residuals at the same Υ_i):
  - **C_U0** (primary; X33's frame): Υ = CFG695 U₀ per footing.
  - **C_05:** Υ = 0.50 for every galaxy (EM1 A1's pinned convention).
  - **C_EM1:** each galaxy at its EM1 R1 Υ (route E's own per-galaxy fit, background A). Route E only; the law's prediction at
    the same Υ_i is reported.
- **Measured residual** r_obs,i = median over the curve's valid points of log₁₀ g_obs − log₁₀ g_iso(g_bar(Υ_i)), g_iso = ν₁ g_bar.
- **Model residuals** r_M,i = median over the same points of log₁₀ g_M − log₁₀ g_iso. Also reported: the remaining residual
  against the model, median of log₁₀ g_obs − log₁₀ g_M.

## 3. Models (no new constants are fitted)

**(a) Law with the exact AQUAL EFE.** g_a = P4's `sparc_solve` at L★ = 0 ("mono" = sphere-averaged internal radial field;
the record's primary), at Υ_i exactly (not node-interpolated), external field g_e = law(e_N) per footing from Chae's primary
e_N. Reported variants: Chae max-clustering and no-clustering brackets; "ring" (equatorial) orientation; L★ = 24 pc (v3s
stiffness). Galaxies without an environment: none in S_L/S_A by construction.

**(b) Route E (EM1's model, background A primary, B reported).** g_b = g_bar(Υ_i) + g_NFW(r), M200c from EM1's global relation
log M200 = a + b(log M_b,ref − 10), Bullock+01 c(M) on EM1's CLASS background, no EFE term, no environment term. (a, b) per
convention: C_EM1 → EM1's R1 relation and R1 per-galaxy Υ; C_05 → EM1's UPS05 relation; C_U0 → EM1's grid fit (same grids,
same pooled-rms objective) at Υ fixed to U₀ per footing (EM1's own procedure at a different fixed Υ; declared, like κ).

## 4. Statistics

- ρ = Spearman(r, log e_ext); s = OLS slope of r on log₁₀ e_ext (dex per dex).
- Bootstrap: B = 2000 resamples of galaxies (seed 3601), the SAME indices for measured and model slopes (paired).
- Per model M and convention: s_M; Δ_M = s_obs − s_M; σ_Δ = bootstrap sd of Δ_M; z_M = Δ_M / σ_Δ.
  **M reproduces** iff |z_M| < 2; **M fails** iff |z_M| ≥ 3; 2–3 is tension.
- **Power** P = |s_a − s_b| / σ(s_obs) at the same convention (σ(s_obs) = bootstrap sd of the measured slope).
- Footings never pooled. Route E is judged at its best convention (smallest |z_b| over C_U0, C_05, C_EM1; generous to route E).
  The law is judged at C_U0 (primary); C_05 reported.

## 5. Confound controls (on S_L, convention C_U0, both footings)

- Controls: log D, inclination, Q, T, log Σ₀ (X33's column), log L36, log M_b, distance method (fD: 1 Hubble flow vs other),
  UMa membership. Reported only, NOT in the gate (mechanism-adjacent: the EFE acts through them): log R_last, log x_char.
- Partial Spearman: rank-transform, regress the controls out of both ranks (OLS with intercept), Pearson of the residual ranks;
  p from the t distribution with N − 2 − k dof. Each control singly, and all gated controls jointly.
- Also reported: Spearman of log e_ext with each control; residual slope by fD class; e_ext construction (how X33 / P4 built it).
- **Confound gate:** the trend is CONFOUND-DRIVEN iff the joint partial has p ≥ 0.05 AND |ρ_partial| ≤ 0.5 |ρ_raw| on both
  footings. The named confound is the single control with the largest drop in |ρ|, provided its own Spearman with log e_ext
  has p < 0.01; if none qualifies, the name is "joint (no single control)".

## 6. Verdict (per footing; the lane's verdict needs the same class on both footings, else UNDECIDED (footing split))

Precedence, first match wins:
1. **CONFOUND-DRIVEN (name it):** the gate of §5 fires.
2. **NOT DIAGNOSTIC:** P < 2 (power too low; at C_U0) OR both models reproduce (|z_a| < 2 and best |z_b| < 2).
3. **EFE DISCRIMINATES: LAW:** |z_a| < 2 at C_U0, route E fails (|z_b| ≥ 3) at EVERY convention, and P ≥ 3.
4. **EFE DISCRIMINATES: ROUTE E:** best |z_b| < 2, |z_a| ≥ 3 at C_U0, and P ≥ 3.
5. **UNDECIDED** otherwise; sub-reading named: "NEITHER" if |z_a| ≥ 3 and every |z_b| ≥ 3; "TENSION" otherwise.

Wording if class 3: "this test prefers the fundamental-law reading over route E", nothing broader.

## 7. Reported (not graded)

- S_A (all SPARC with an environment) and every variant of §3.
- Background B for route E.
- Tidal bound for route E halos: r_t = (G M200 / (2 g_ext / d))^{1/3} at declared host distances d = 1 and 3 Mpc, as r_t / R_last.
- **Gaia DR4 wide binaries for the same EFE question:** the MW field e at R₀ from the sealed v3 file (`S3_v3_mw_seals/
  SEALED_V3_MW_DR4.json`, read only), its lever arm over a 200 pc DR4 volume, and v3s's screened γ_v − 1 from
  `covariant_push_2026_10_22/C6_literal_cassini` (read only); route E predicts Newton. The CFG800 / Amendment 22 rule
  (`campaign_fresh_gravity/DR4_OUTCOME_MAP_2026-10-15.md`) is quoted, not edited. Sealed files are never written.
- Directional-EFE record: the n = 16 Â = +2.95 is always quoted beside WALLABY's Â = −1.70 ± 2.12 (n = 25; an amplitude, not a σ).

## 8. Checks (`x36_efe.py` prints `K* PASS/FAIL`; exit 0 iff all pass) and MUTATE

- **S0a–S0e** (§1).
- **K_efe:** model (a) is an EFE: every galaxy's r_a ≤ +1e-6 at C_U0 and max |r_a| > 1e-3 dex (both footings).
- **K_repro:** the measured ρ on S_L at C_U0 equals X33's to 1e-9 (both footings).
- **K_plant (positive control):** r_obs + (−0.10)·(log e − mean) recovers a slope shift of −0.10 ± 2σ(s_obs).
- **K_rss:** RSS < 1 GB.
- **MUTATE** (`X36_MUTATE=1`, outputs `_MUTATE`): log e_ext shuffled within morphology bins (T 0–3, 4–6, 7–8, 9–11; seed 3602)
  AND the EFE switched off in model (a) (g_e = 0). **K_repro and K_efe must FAIL** (exit 1); K_plant must still PASS.

## 9. Outputs and stop rule

`x36_efe.py` → `x36_efe.out`, `x36_efe_results.json`, `x36_per_galaxy.csv` (and `_MUTATE`). No scans beyond the declared
grids. Post-result changes go in a dated AMENDMENT; the classes above are never changed after a number exists.
