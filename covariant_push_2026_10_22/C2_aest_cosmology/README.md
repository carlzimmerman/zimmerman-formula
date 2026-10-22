# C2_aest_cosmology: what an AeST-type completion predicts for cosmology, and what a native CMB / P(k) test needs

## Verdict

**COMPUTED** for the background, the dust abundance and the native H₀.
**DATA-GATED** for a native CMB / P(k) confrontation. The gap list is in §4.

Plain answers:

1. **Ω_c is a fitted number in an AeST-type completion.** The cold share Ω_c/Ω_b = 5.36 stays an import.
   - The dust density is Q₀·I₀/(8πG̃).
   - I₀ is the conserved shift charge, an initial datum. Nothing in the action fixes it.
   - The derivative of the dust density with respect to a₀ is exactly 0, and so is the derivative with respect to Λ (K2).
2. **a₀ cannot enter the background or the linear equations.** The invariant that carries a₀ is
   Y = q^{μν}∂φ∂φ. It vanishes on FRW at order ε⁰ and ε¹, with a general metric and aether perturbation
   included (K1). So the linear CMB and P(k) of such a completion are blind to a₀ and to the screened law.
3. **The 15.5–18σ native-H₀ flag in E1 rests on a background that A78 already excludes.**
   - The lever is G_cosmo/G_N ≡ g. Any background that is GR with G_cosmo = g·G_N leaves the BAO ratios exactly
     unchanged (residual 6×10⁻¹⁶) and gives H₀ = √g·H₀,GR (K4).
   - The record's native branch, β = (2/3)Ω_m, has g = 0.6845 and H₀ = 56.7. A78's BBN line puts it at
     ΔN_eff = −3.4, more than 10× the 0.30 bound.
   - With A78's bound g > 0.9611 and CFG886's GR fit (BAO + BBN, no CMB), the **native H₀ is 67.2–68.6**.
   - Against the ladder 73.0 ± 1.0 that is **4.4–5.8σ** with the ladder error only (E1's convention), or
     **3.9–5.2σ** with the native error added (K5). So the native tension is the ordinary Hubble tension, not 15–18σ.
4. **AeST does not move H₀ toward 73.**
   - Its lever is G̃ = (1 − K_B/2)·Ĝ_qs (external input E-AeST). With 0 < K_B < 2 this can only lower g, and so lower H₀.
   - If G_N = Ĝ_qs, the same BBN line gives **K_B < 0.078** (K6). Whether G_N equals Ĝ_qs (the λ_s factor) is OPEN; it is not on disk.
5. **Linear growth is GR growth on a ΛCDM-shaped background: γ = 0.555, f(0) = 0.510** at CFG886's Ω_m (K7).
   - The same solver gives f(0) = 0.4522 on A46's β branch, which reproduces A45's 0.452.
   - OPEN premise: if sub-horizon growth feels G_N while the background feels G_cosmo, then at g = 0.9611
     σ₈ rises **16 %** (f(0) = 0.523). That is a lever the data could see. It is not a claim of this lane.
   - The record's settling picture is a nonlinear redistribution. On the gravitating field it is excluded on the
     canonical footing by raw KiDS (CFG596, Δχ² +68.7). An AeST-type dust sector does not touch that verdict at
     linear order (K1), so it neither rescues it nor adds to it.

## 1. The numbers (all in `c2_aest_cosmology_results.json`)

| check | what | result |
|---|---|---|
| K1 DERIVED | Y on FRW + general linear perturbation | Y⁽⁰⁾ = 0, Y⁽¹⁾ = 0 (sympy, exact) |
| K2 DERIVED | φ-equation, ρ = QK′ − K, Higgs-phase K | 8πG̃ρ = 2Λ + Q₀I₀/a³ + I₀²/(4K₂a⁶); ∂/∂I₀ = Q₀, ∂/∂a₀ = ∂/∂Λ = 0 |
| K3 COMPUTED | cosh K (record L137 form, Z₀/Q₀ = 10⁻³) | ρa³ drifts +2.09 % from z = 0 to 1090 (analytic 2.10 %); w ≈ 10⁻³; dE/E ≤ 0.9 % |
| K4 DERIVED+COMPUTED | GR with G_cosmo = g·G_N | D_M/r_d and D_H/r_d unchanged to 6×10⁻¹⁶; H₀ = √g·H₀,GR |
| K5 COMPUTED | native H₀ under A78 | 67.22–68.56; 4.44–5.78σ (ladder σ) / 3.93–5.15σ (combined) |
| K6 COMPUTED | AeST K_B under the same BBN line | K_B < 0.0778 (if G_N = Ĝ_qs; OPEN) |
| K7 COMPUTED | growth | γ = 0.5548, f(0) = 0.5105; A46 branch 0.4522 (A45: 0.452) |
| K8b COMPUTED | CLASS 3.3.4 r_d vs quadrature | 148.076 vs 148.087 Mpc (+0.007 %) |
| K9b INVENTORY | tools and data on disk | §3 |

K3 adds one free parameter of K, Z₀/Q₀, at the record's own value. It is counted as POSTULATED.
At that value, ω_c at recombination is about 21·(Z₀/Q₀) larger than today's. The CMB and lensing could see
that, but a fit fixes Z₀/Q₀, not the action.

## 2. What was checked in the record

These were read before any number was produced:
- `real_research/bridge1_aest_equations.md`: AeST equations transcribed from the arXiv LaTeX source, 2026-08-14. This is external input E-AeST.
- `fable_independent_2026/L137_aest_dust_stiff_correction.out`: the quadratic K carries a stiff a⁻⁶ partner; cosh/exp K do not.
- `real_research/AEST_MASS_SCALE_two_doors.md`, `THE_NEXT_CALCULATION_aest_quasistatic.md`.
- `hy4_push/H001*`, `H002*`, which found the CMB peaks to be a null test.
- `campaign_fresh_gravity/CFG242_FROZEN_CRITERIA.md`, CFG886, CFG555/CFG596 (memory note).
- DSF-21 A42, A45, A46, A78, `THEORY.md` §3.6c.
- `doors_push_2026_10_22/E1_input_audit/`.

**Record error (reported, not edited).** `doors_push_2026_10_22/E1_input_audit/README.md` L29–35 and L43
(code `e1_input_audit.py` L95–107) take the native H₀ band 55.0–57.5 and its "15.5–18σ below the ladder" from
A46's β = (2/3)Ω_m background. A78 (commit dc7cc7e409, earlier the same day) excludes that background by BBN.

- The BBN-allowed native H₀ is 67.2–68.6 (K5).
- E1's other uses of that band should be re-read under it.
  - The canonical a₀ value does not change: cH₀√Ω_Λ/Z = κc√(Gρ_Λ) is the same number on either background.
  - What goes away is the reading "a₀ = cH₀/Z with H₀ the native H₀". This lane does not redo E1's other rows.

## 3. Tools and data on disk (K9b)

**Present:**
- Tools:
  - CLASS (`classy` 3.3.4) and CAMB 1.6.6, both vanilla;
  - healpy 1.19.0;
  - pyccl, in the cfg592 venv.
- Data:
  - KiDS-1000 ξ± with covariance and n(z);
  - DES Y3 2pt;
  - Planck PR4 lensing bandpowers and covariance. Its likelihood carries an FFP10 ΛCDM "fiducial correction", which counts as ΛCDM-PROCESSED.
  - Pantheon+;
  - the Planck 2018 parameters paper source (1807.06209);
  - DESI DR2 chains. These are ΛCDM-processed and are not data.
- **Planck PR3 TT unbinned D_ℓ**, ℓ = 2–2508, inside the PR4 lensing package (`.../iswliks/COM_PowerSpect_CMB-TT-full_R3.01.txt`).
  It has diagonal errors only: no covariance, no foreground or calibration model, no TE/EE.
- DESI DR2 BAO is used as a compressed table hard-coded in A46 (arXiv:2503.14738, Table 1). That is a survey compression.

**Absent:** hi_class; any AeST-modified Boltzmann code; `clik`; `cobaya`; any Planck plik / CamSpec / HiLLiPoP
likelihood file; Planck TE/EE spectra; the AeST paper source.

The frozen K9 claimed that no Planck TT spectrum was on disk. It failed: the TT file above exists. AMENDMENT A1 (post-result) corrects this.

## 4. What a native confrontation needs (owner approval; nothing fetched)

A native test only means something once the AeST-specific terms are in a Boltzmann code. The dust limit in
vanilla CLASS *is* ΛCDM, so running it now would test ΛCDM, not the framework. Needed, in order:

1. **An AeST Boltzmann module.** Two routes:
   - (a) the AeST authors' modified CLASS, if it is obtainable (availability unverified);
   - (b) the CLASS 3.3.4 source (`github.com/lesgourg/class_public`, tag v3.3.4), patched with the background
     and the δ/θ/E/α equations of `bridge1_aest_equations.md` (the record's scaffold
     `real_research/bridge1_aest_boltzmann_scaffold.py` is a stub).
   Both are a download plus a C build.
2. **The AeST paper sources** arXiv:2007.00082 (to re-verify E-AeST) and arXiv:2304.05134 (to settle G_N vs Ĝ_qs,
   the OPEN item in K6).
3. **A Planck primary likelihood.** Either:
   - `clik` with the Planck 2018 baseline likelihood bundle (PLA, `COM_Likelihood_Data-baseline_R3.00`; name from memory, to verify), or
   - `pip install cobaya` plus its plik-lite install.
   Plus `COM_PowerSpect_CMB-TE-full_R3.01.txt` and `COM_PowerSpect_CMB-EE-full_R3.01.txt` from the same PLA family as the TT file on disk.
   Without a covariance, the TT file on disk supports only a diagonal, foreground-blind comparison. That is not a verdict.
4. KiDS ξ± and DES Y3 are already on disk. The P(k) side needs the AeST module of item 1. The nonlinear side
   (μ⁻¹ ~ Mpc) needs AeST N-body, and the record has only a prototype (`real_research/aest_3d_nbody/`).

## 5. What this does not show

- It does not show that AeST (or this completion) fits the CMB. That is the paper's claim, and it is not reproduced here.
- It does not derive Ω_c, Z₀/Q₀, K_B or λ_s. Each one is a fitted or postulated number.
- K4 holds z_drag at its microphysical value. The small change in the drag rate relative to H that comes with g is neglected.
- The growth variant rests on an OPEN premise.
- κ = ½ is FITTED. Footings are not pooled; neither footing's a₀ enters K1–K9. Nothing here favours the framework over ΛCDM.

## Files and rules

- `FROZEN_CRITERIA.md`, committed alone first (ac4b30ff62), with AMENDMENT A1 (post-result).
- `c2_aest_cosmology.py` → `.out` and `_results.json`; 9/9 PASS, exit 0.
  - The frozen K8 and K9 lines still print as `K8-orig FAIL` and `K9-orig FAIL`.
  - The first scored run's output is kept as `c2_aest_cosmology_RUN1_prefix.out` (7/9).
- `C2_MUTATE=1` puts the full metric in place of the projector and drops the √ in the H₀ map. K1 and K4 fail and the run exits 1 (`*_MUTATE.*`).
- Run: `OMP_NUM_THREADS=1 nice -n 10 python3 c2_aest_cosmology.py`. It takes about 9 s on one thread with 0.22 GB peak RSS. Nothing was downloaded or installed.

---

## 6. Wave 2 (owner-approved fetches): the papers on disk, G_N vs Ĝ, and a vanilla-CLASS emulation vs plik-lite

**Verdict update.**
- **COMPUTED:** the background ratio g, from the AeST source (P1–P3).
- **DATA-GATED → TOOL-GATED:** the full AeST CMB prediction. The data are now on disk. The AeST Boltzmann code is not.

The run is `c2b_native_cmb.py` under AMENDMENT A2 (pre-result, bfd11598d9). It passes **5/5**. `C2B_MUTATE=1` breaks
P2 and P4 (3/5, exit 1). It made 124 CLASS runs in 202 s on one thread. Peak footprint was 0.23 GB; macOS reports a
max RSS of 1.02e9 B (0.95 GiB), right at the 1 GB line. Provenance is in `PROVENANCE.md`. No downloaded code was executed for any number.

**P1. Source check: 15/15 load-bearing items match.** The two sources are `newRMONDLett.tex` and `main.tex`.
- The record's transcription (`real_research/bridge1_aest_equations.md`) is right on every item checked. It omits
  J_μ = A^α∇_αA_μ and K(Q̄) = −½F(0, Q̄).
- `real_research/THE_NEXT_CALCULATION_aest_quasistatic.md` writes F = −K + …. The source has F(0, Q) = −2K.
- **C1 has a factor-2 slip** in the mass term (C1 README, point 1).
  - C1 uses m² = K₂Q₀²/(2−K_B). The source's Eq. 6 has μ² = 2K₂Q₀²/(2−K_B).
  - This is fixed by K = −F/2, so it is not a convention.
  - It touches only the Mpc-scale term, not C1's verdict.

**P2. Newton's constant in AeST is G_N = (1 + 1/λ_s)·Ĝ.** This is PRL L254; VSZ's Ĝ = G_N/(1+β₀) with λ_s = 1/β₀ says the same.
- Hence **g = G_cosmo/G_N = (1 − K_B/2)·λ_s/(1+λ_s) ≤ 1**. AeST can only lower the native H₀.
- The A78 BBN line (g > 0.9611) needs **both K_B < 0.0778 and λ_s > 24.7**.
- VSZ's plotted λ_s = 1, 2 and 10 would give ΔN_eff = −3.7, −2.5 and −0.68. All three fail the |ΔN_eff| < 0.30 line, if cosmological G is G̃.
- SZ's CMB "MOND models" use λ_s = ∞, where g = 1 − K_B/2. **K6's OPEN item is settled: the bound is K_B < 0.078 at λ_s = ∞.**

**P3. Linear growth feels G̃ = G_cosmo.** The source normalises δ with G̃ and states the Einstein equations in GR form.
- So K7 stands: γ = 0.555.
- **The K7 "G_N variant" (+16 % σ₈) is withdrawn.** It is not AeST's linear behaviour.

**P4/P5. Vanilla-CLASS emulation of g. This is NOT the AeST prediction.**
- **How it works.** Baryons stay physical, so the microphysics is right. The extra gravity is removed through the CDM and N_ur densities.
  - The background and recombination are exact for H² = (8πgG_N/3)ρ.
  - The per-species Poisson weights and the neutrino shear are off by O(1−g): about 6 % of the ν shear at g = 0.961 and about 45 % at g = 0.6845.
- **Likelihoods.** plik-lite TTTEEE (613 bins), low-ℓ TT and low-ℓ EE, reimplemented from the data files.
  - They are not validated against cobaya's own output.
  - Sanity: the ΛCDM refit gives χ²_plik = 582.3 for 613 bins.
- **Results:**

| quantity | value |
|---|---|
| acoustic scale at fixed physical densities, g = 0.9611 | Δθ_s/θ_s = 4.1e-4 (almost blind; absorbed in a refit) |
| low-ℓ τ (native scan) | 0.0510 ± 0.0085 |
| ΛCDM refit (g = 1) | ω_b 0.02231, ω_c 0.1206, 100θ_s 1.0418, n_s 0.962, τ 0.056; H₀ 67.6 |
| Fisher σ(g), marginalised (plik-lite + τ + A priors) | **0.027** (0.0036 with the others fixed) |
| profile at g = 0.9611 (BBN edge) | Δχ² = **+0.03**, H₀ = 65.6 (n_s 0.950, ω_b 0.0221) |
| profile at g = 0.6845 (record's β = (2/3)Ω_m branch) | Δχ² = **+190**, H₀ = 51.1 (emulation crude here) |

- **Reading.**
  - The CMB alone measures g to about 2.7 %, about as well as BBN (3.9 %). The BBN-allowed band cannot be told apart from g = 1.
  - The record's β = (2/3)Ω_m branch is disfavoured by Planck too in this emulation, independently of A78's BBN exclusion.
  - The CMB-preferred H₀ falls with g, never toward 73.
- **Mutation check.** With N_ur left unscaled, the CMB absorbs g entirely into ω_c (Δχ² ≈ 0 even at 0.6845). So the CMB's handle on g is the radiation-era expansion rate.

**A native AeST CMB run: what it needs.**
- The papers give the closed linear system. Besides the background Q(a) from K′(Q) = I₀/a³, there are four extra ODEs per k:
  - δ and θ (Eqs. 8–9);
  - E (the E equation after Fig. 1);
  - α (from E = α̇ + Ψ), with Π (Eq. 10) and χ = φ + φ̄̇α closing it.
- This fits a CLASS patch of roughly 300–500 lines of C in background/perturbations/input, in the Newtonian gauge. Estimated work: about 1–2 weeks including validation.
- Two gaps:
  - (i) **The adiabatic initial conditions are not in either paper.** SZ cite "in preparation". They would have to be derived (super-horizon expansion).
  - (ii) **The CLASS C source (class_public v3.3.4) is not on disk.** Only the binary wheel is. Fetching it was not part of this approval.
- Validation could only be against SZ's Fig. 1 curves; no table exists.
- Not built, as instructed.

**C1's open items, from the source (report only).**
- **Stability conditions.** 0 < K_B < 2 and λ_s > −1 (vectors); K₂ > 0 (scalar); λ_s > 0 (the ω = 0 mode at low k, also in VSZ); μ² > 0.
- **Mode count on Minkowski.** Tensor as in GR (2); a massive transverse vector, M² = (2−K_B)(1+λ_s)Q₀²/K_B (2); and two scalar normal modes, ω² = 0 and ω² = (2−K_B)(1+K_Bλ_s/2)k²/(K₂K_B) + M².
  - That is 5 modes with ω ≠ 0 plus one zero-frequency scalar, matching A68's count of 5. The kinetic structure differs, as C1 said.
- **C1's capped F sits at λ_s → ∞.** This is SZ's own "screening" limit, and SZ's cosmology uses it. But the scalar's
  speed² ∝ (1 + K_Bλ_s/2) and the vector mass M² ∝ (1+λ_s) both diverge there.
  - If one extrapolates the Minkowski result to the cap, where the local 𝒥′ → ∞, the scalar propagates without bound.
  - Whether the capped F is healthy is still **OPEN**. It is flagged, not settled.
