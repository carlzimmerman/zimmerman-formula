# WG1_cmb_lensing_web_gradient: FROZEN CRITERIA, committed alone before any script or number

**Not blind.** The Planck PR4 lensing bandpowers are already on record (CFG917), and their amplitude matches the standard fit to 2-3 %. One estimate was made in chat before this file: the 2.6′ rms deflection gives a web gradient of about 10⁻² a0. That estimate is not used here.

κ = ½ FITTED. The cold sector stays retired. Nothing here adds a particle or a cold component. Not theory closed. Nothing here says the data favour the framework. No downloads: the PR4 files are already on disk and used by CFG917. No ΛCDM spectrum, transfer function, halofit or ΛCDM background enters any model or verdict. The background is a wide bracket (below).

Owner 2026-11-04: "Yes, run it", for a lane that gives board row D9 (CMB lensing; `N0_board_audit/AUDIT.md`: "no graded number") a verdict for the law alone.

## Step 0: record check
- **CFG363** (a943a437f): phantom plus the conserved cold mass over-lenses CMB lensing 3.3-13.7× (L 40-763). This is the additive reading on a ΛCDM halo population, cold mass included. OLD MODEL.
- **AUDIT_SIGMA8** (10-03): the chassis with Ω_c h² 0.120 grows about 7× too fast and is excluded by CMB lensing. Cold mass included. OLD MODEL.
- **CFG917**: CMB-lensing gate on theory-v2, Part A SAFE. Cold energy mass required. OLD MODEL.
- **PAPER67 v1.0**, gaps section: "a0 is absent from the linear FRW equations, so the law can't act there". Row 11, "act as dust in the CMB": no cold term.
- **N0 board audit D9**: CMB lensing, "no graded number".
- No lane on record does either of these:
  - computes the measured web gradient in units of a0;
  - computes C_L^φφ for the law alone with no cold term.

## Questions
- **Q1.** Where does the potential that CMB lensing measures sit on the law's acceleration scale? That is, what is the rms gradient g_web(z) of that potential at z 0.5-2.33, in units of a0(z)?
- **Q2.** What verdict does D9 get for the law alone?
- **Q3.** Suppose the law acts on that field in its deep limit.
  - How much does C_L^φφ differ between the ρ_DE tie and a0 ∝ H(z)?
  - Can C_L^φφ alone separate that difference from the unknown source amplitude?

## Data
- **Source.** Planck PR4 lensing, CMB-marginalised, conservative L 8-400 (9 bins). Loaded with `cfg917_lib.load_pr4` (imported read only, file paths as in that library). SHA-256 of the bandpowers, covariance and window files is printed in the output.
- **PACKAGE rule:** B = (W + M) X − F, the published likelihood rule. M and F carry the fiducial normalisation, which is Hu 2001's "calibration error" term.
- **PLAIN rule:** B = W X.
- X_L = [L(L+1)]² C_L^φφ / 2π.
- A label holds only if both rules give it.

## Model (no cosmological spectrum)
- **Projection** (Hu 2001 eq. 2, flat sky):
  - φ = −2 ∫ dχ (χ_s − χ)/(χ χ_s) Ψ
  - Limber: C_L = ∫₀^χs dχ q(χ)²/χ² P_Ψ((L+½)/χ, z(χ)), with q = 2(χ_s − χ)/(χ χ_s) and z_s = 1090.
  - Ψ is the dimensionless potential (Φ/c²).
- **Potential spectrum family:** Δ²_Ψ(k, z) = A G(z)² / [1 + (k/k_t)²]^(β/2), with G(z) = (1 + min(z, 5))^p.
- **Free parameters:**
  - A, linear;
  - k_t, scanned over 121 log points from 1e-3 to 1 Mpc⁻¹, then a bounded refinement around the best grid point.
- **Brackets** (every combination, 90 members; no member is preferred):
  - **Background:** flat, H(z)² = H0² [Ω_r(1+z)⁴ + Ω_m(1+z)³ + 1 − Ω_m − Ω_r].
    - Ω_m ∈ {0.05, 0.30, 1.00}: 0.05 is baryons alone, 1.00 is matter only.
    - H0 ∈ {65, 75} km/s/Mpc.
    - Ω_r h² = 4.18e-5.
    - This is a geometry bracket, not an adopted model.
  - **Potential evolution:** p ∈ {−1, −0.5, 0, +0.5, +1}.
  - **High-k slope:** β ∈ {2, 3, 4}.
- **Acceptance:** a member is accepted under a rule if its best χ² (9 bins − 2 parameters = 7 dof) has p ≥ 0.001.

## Quantities
- **Web gradient:** g_web(z) = c² (1+z) σ_∇Ψ(z), with σ_∇Ψ in Mpc⁻¹ converted to m⁻¹.
  - σ²_∇Ψ(z) = ∫ d ln k k² Δ²_Ψ(k, z), taken over the modes the data see at z: 8.5/χ(z) ≤ k ≤ 400.5/χ(z).
- **Conservative envelope** per accepted member:
  - use every k_t with profiled χ² ≤ χ²_min + 4;
  - take A at A_best ± 2σ_A at each such k_t;
  - g_hi is the largest g_web over these points, g_lo the smallest.
- **a0 footings:** `a0kit.footings()`, canonical and alt, never pooled.
- **a0(z)/a0(0), three rules** (PAPER67 v1.0 band from CFG689; linear in z between the nodes):
  - **TIE-LOW:** the 68 % lower edges, 1.00, 0.76, 0.71, 0.33 at z 0, 1, 1.5, 2.33.
  - **TIE-MID:** 1, 0.91, 0.94, 0.91.
  - **RIVAL:** H(z)/H0 of the member.
  - TIE values are held at the z 2.33 value beyond z 2.33.
- **Graded z grid:** 0.5, 1, 1.5, 2, 2.33. z 3 is reported as context only.

## Checks (all must PASS before any label is read)
- **K1 Limber engine.**
  - Input: P_Ψ = k⁻⁴, G = 1, on the Ω_m 0.30, H0 65 background.
  - Must return 4χ_s / [3(L+½)⁴] to 1e-3 at L 10, 100 and 1000.
- **K2 gradient integral.**
  - Input: Δ² = 1/[1 + (k/k_t)²]², integrated over all k.
  - Must return k_t²/2 to 1e-3 at k_t 0.01 and 0.05.
- **K3 round trip.**
  - Synthetic PACKAGE-rule bandpowers, no noise, from three members with set (A, k_t).
  - The pipeline must recover g_web(1.5) within 1 %.
- **K4 data.**
  - 9 bins, contiguous L 8-400.
  - Covariance positive definite.
  - Hashes printed.
- **MUTATE.**
  - The lensing kernel loses its factor 2: q → (χ_s − χ)/(χ χ_s).
  - K1 must FAIL under MUTATE. Otherwise K1 has no teeth, and the lane reads NOT EVALUABLE.
  - Outputs carry a `_MUTATE` suffix.

## Labels
**V1 (Q1).** Read per footing and per rule, with TIE-LOW. TIE-LOW is the a0(z) rule that makes g/a0 largest.
- R = the maximum, over accepted members and the graded z grid, of g_hi(z)/a0(z).
- **DEEP** if R < 0.1: the simple form's boost g/g_N = 1 + a0/g exceeds 11 everywhere.
- **TRANSITION** if 0.1 ≤ R < 1.
- **SHALLOW** if R ≥ 1.
- **NOT EVALUABLE** if no member is accepted or any K check fails.
- **SPLIT** if the two rules disagree; both labels are reported.
- Also reported: the minimum over members of g_lo/a0 with RIVAL, the smallest ratio.

**V2 (Q2): D9 for the law alone.** The record has no C_L^φφ prediction for the law without a cold term (Step 0). So whatever V1 reads, D9 is **NOT EVALUABLE FOR THE LAW ALONE**, with the missing inputs named:
- **(a)** The law's rule on the linear web. It is required if V1 reads DEEP or TRANSITION, because then that field lies inside the law's range. If V1 reads SHALLOW, (a) is dropped and the door reduces to (b).
- **(b)** A baryon field at z 0.5-3 on k ≈ 0.003-0.2 Mpc⁻¹ that doesn't use a cold term.
- V2 cannot read PASS or FAIL in this lane.

**V3 (Q3).** Reported, not a pass/fail.
- **Deep-limit scaling:** P_Ψ ∝ a0(z)/a0(0) at fixed source. This is exact for g = √(a0 g_N).
- **Computed for each accepted member at its best fit:** B_b(RIVAL)/B_b(TIE-MID) on the PLAIN rule, bins 1-9.
- **Reported:**
  - the median lever;
  - the shape spread S = max_b / min_b − 1.
- **Reading:**
  - If S < 0.10 in every accepted member, the reading is: "C_L^φφ alone can't separate the two a0(z) rules from the source amplitude; tomography or a fixed source is required."
  - If S ≥ 0.10 in some member, report which members, no label.

**Diagnostics.** Not graded, reported only.
- **D1: law OFF on the web** (Newtonian, baryons only). The baryon contrast the measured potential needs:
  - Δ_δb(k, z) = (2/3) k² Δ_Ψ(k, z) / [ω_b (100 km s⁻¹ Mpc⁻¹ / c)² (1+z)].
  - ω_b ∈ {0.0210, 0.0230}, a bracket meant to cover BBN D/H with either rate set. The values are PROVISIONAL, from memory.
  - Evaluated at k ∈ {k_t, 0.02 Mpc⁻¹} and z ∈ {1, 2}.
- **D2: law ON in the simple form.** D1 × g/(g + a0(z)), with g = g_web(z) at the best fit, TIE-MID, per footing.
  - This is an rms-level mapping; the pointwise √ mapping on a Gaussian field is not exact.
  - It gives the size of input (b) in each reading. It is not compared with any baryon field.

## What this lane can't say
- It is not a test of the law's lensing at galaxy scales (the KiDS 0.09 dex row) or of cluster lensing.
- g_web is the web-scale field (k ≤ 400.5/χ). Local fields near bound systems are larger.
- It assumes lensing sees the dynamical potential (v3 φ = ψ; AX1 G3). In a conformal-scalar class, CMB lensing sees only the Newtonian part.
- The background bracket is not a model. The bare law has no consistent background (PAPER67).
- Nothing here reinstates the cold sector or uses ΛCDM spectra.

## Output
- `wg1.py` writes `wg1_results.json` and `wg1.out`.
- MUTATE writes `wg1_MUTATE_results.json` and `wg1_MUTATE.out`.
- `README.md` carries the labels.
- Runs single-threaded, under 1 GB, in minutes.
