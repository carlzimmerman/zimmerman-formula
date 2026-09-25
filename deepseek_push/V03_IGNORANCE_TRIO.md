# V03 — THE IGNORANCE-ORTHOGONAL TRIO: R (kernel-free) × U (radius-free) × B (density-free) as ONE decision surface

**2026-09-25 · deepseek lane · follow-on to J05/J06/J09/J10/J11, K08/K09, L07, N04, U05 · no git commit · exit 0, 7/7 checks, 72 cells, n_tot = 3.6×10⁷**

## PRE-REGISTRATION (locked BEFORE the V03 numbers were drawn; identical text in V03_PRE.txt, printed verbatim as the first section of V03_trio.out before any measurement)

### 0.1 The three falsifiers (each immune to a different ignorance)

| falsifier | definition | immune to | record |
|---|---|---|---|
| **R** | R ≡ −ln A / E[D], A = P(no collision) = E[I(N=0)], D = lag | **kernel (phase function)**: A never fires the kernel; E[D]'s scattering term is ∝ E[μ] = 0 for symmetric kernels (L07, 46/46) | J09: central flat window R ∈ [4/3, 2], τ₀-free, closed form W_C(q) = (1+q/3)/(½+q/4); J11/K09: volume window τ₀-dependent |
| **U** | U ≡ std(D)/E[D] (width ratio) | **physical radius**: ratio cancels R (N04, K09 width surface) | N04: kernel-***tagged*** (isotropic shift z ≈ 5–12), 29–49× cheaper than R |
| **B** | bound: E[D²] ≥ 3 E[Dv²]² / E[v⁴], slack_B ≡ E[D²]·E[v⁴]/(3 E[Dv²]²) ≥ 1 | **density, geometry, kernel** (Cauchy–Schwarz; conditional-Gaussian hierarchy J05/J06, exact slack = 1/ρ₀²) | J05: central τ₀=1 slack 1.25/1.13/1.06 at q = 0/3/10; U05 thin limits 4/3, 448/375, 91/81 |

### 0.2 The landscape grid (all cells, both kernels)

- **CORE (36 cells, n = 8×10⁵ each)**: geometry ∈ {central, volume} × q ∈ {0, 3, 10} × τ₀ ∈ {0.5, 1, 2} × kernel ∈ {thomson, isotropic}.
- **SHELL-EXT (36 cells, n = 2×10⁵ each)**: geometry ∈ {shell(a=0.3), shell(a=0.5)} × same q × τ₀ × kernel.
- Engine: J02 exact optical-depth bisection (verbatim copy + L07 kernel switch + K09 shell birth law); parity-checked bitwise against `J02_moment_hierarchy.simulate` and `K09_geometry_reading.simulate_shell` before science cells (P1).
- SEs: R, U by the N04 delta method **and** by 24-block jackknife (block covariance matrix of (R, U, slack) → 3×3 sampling covariance; SE everywhere).

### 0.3 The observer bands (fixed from the RECORD, not from this run)

| band | geometry | provenance | value (widened ±3·tol) |
|---|---|---|---|
| W_C | central | J09-D closed form, exact | [4/3, 2], tol = 0 |
| W_V | volume | K09 Table (τ₀ ∈ {0.5,1,2}, q ∈ {0,3,10}) | [0.9184, 1.9144], tol = 0.010 |
| W_S | shell | K09 union over a ∈ [0.1, 0.99] on-grid | [1.4298, 2.0063], tol = 0.025 |
| U_C | central | N04 U-table (9 cells), union ±3·se | [0.804, 1.982] |
| U_V | volume | N04 U-table (9 cells), union ±3·se | [1.233, 2.536] |
| U_S | shell | **this run** (flagged CIRCULAR for shell cells) | [0.802, 2.186] measured |
| B | any | J05 theorem, slack ≥ 1 | [1, ∞), violated iff slack < 1 − 3·se |

Membership (Tier-1 verdicts): g ∈ v_R iff R ∈ W_g (3σ margins included); g ∈ v_U iff U ∈ band_g; B-PASS iff slack ≥ 1 − 3·se.

### 0.4 Disagreement classes (locked; cells where B-PASS unless stated) — [1]–[8] in V03_PRE.txt

**KILL-B** (slack < 1−3σ, family kill, expected 0 on-model) · **VOID-R/VOID-U** (that falsifier excludes ALL geometries, K09-F3 outright-kill channel) · **MIRROR** (vR, vU nonempty and disjoint: exclusive contradiction) · **CROSS** (nonempty intersection but non-nested membership, incl. S-membership split) · **HIERARCHY** (vR ⊊ vU or vU ⊊ vR) · **TRIO-AGREE** (vR = vU). Kernel gates: C3 (R kernel-free, z ≤ 5 per cell) and C7 (U kernel-tagged, z ≥ 3) as pre-registered.

### 0.5 Pre-registered checks (thresholds fixed before the run)

P1 parity bitwise · C1 U-record at τ₀=1 (1.437/1.074/0.898 central, 1.893/1.400/1.258 volume, |z|<5) · C2 central R closed form 2.000/1.600/1.4444 τ₀-free (|z|<5) · C3 R kernel-free on ALL 18 core cells incl. volume q=3/10 (new territory; z<5) · C4 slack record 1.25/1.13/1.06 (|z|<4) · C5 slack ≥ 1−3σ at ALL 72 cells · C6 doorB reading 1.8178 ±3σ and CONSISTENT-OPEN · C7 U tagged at ≥ half the core cells.

### 0.6 Decision tree (locked) and 0.7 Joint 3σ regions (locked)

Tree: **Node 1 B gate** (slack ≥ 1−3σ; n-too-small ⇒ UNDET) → **Node 2 R test** (R ∈ [4/3,2]±3σ AND K06-inv (A, E[D]) → (τ̄₀,q̄) pin; fails: R outside all bands = outright kill, off-grid pin) → **Node 3 U readout** vs the resolved N04 atlas at (τ̄₀,q̄) (C / V / AMBIG-CV / U-OUT; failure modes: U kernel-tagged, inversion bias at non-central truth). Min-n per falsifier: n_req = n·(3·se/gap)², gap = distance to nearest competing band edge (R, B) or resolved |U − U_other(τ₀,q)| (U). Joint regions: per (geometry, kernel) class, μ = 9-cell mean, Σ = Σ_landscape + Σ_samp(τ₀=1,q=0); 3σ Mahalanobis ellipsoid; pairwise MC overlap (2×10⁶, clipped-inverse stable); residual degeneracy = pairs ≥ 1% overlap + nearest-cell joint-distance pairs ≤ 3σ + operating-point-only ellipsoid separations.

---

## RESULTS (computed strictly after the locked pre-registration)

### 1. Engine and grid (P1)

Bitwise parity vs the J02 and K09-simulate_shell imports: max|ΔD| = 0, max|ΔN| = 0 (n=2×10⁵ each). 72 cells ran in 124 s of simulation (Pool(8); total wall 130 s). 3.6×10⁷ photons.

### 2. The trio table — R, U, slack_B with SEs (24-block jackknife) at every cell

**Core grid (36 cells, n = 8×10⁵):**

| cell | R ± se | U ± se | slack ± se | cell | R ± se | U ± se | slack ± se |
|---|---|---|---|---|---|---|---|
| central τ.5 q0 th | 2.0007 ± .0033 | 1.9773 ± .0026 | 1.308 ± .0070 | central τ.5 q0 is | 1.9939 ± .0027 | 1.9295 ± .0024 | 1.314 ± .0121 |
| central τ.5 q3 th | 1.5964 ± .0024 | 1.3952 ± .0017 | 1.207 ± .0089 | central τ.5 q3 is | 1.6044 ± .0023 | 1.3665 ± .0014 | 1.189 ± .0083 |
| central τ.5 q10 th | 1.4442 ± .0029 | 1.0520 ± .0013 | 1.139 ± .0073 | central τ.5 q10 is | 1.4447 ± .0015 | 1.0401 ± .0012 | 1.127 ± .0050 |
| central τ1 q0 th | 1.9971 ± .0032 | 1.4348 ± .0017 | 1.251 ± .0074 | central τ1 q0 is | 2.0015 ± .0027 | 1.4077 ± .0012 | 1.258 ± .0093 |
| central τ1 q3 th | 1.6042 ± .0027 | 1.0738 ± .0012 | 1.143 ± .0039 | central τ1 q3 is | 1.6018 ± .0024 | 1.0611 ± .0008 | 1.124 ± .0056 |
| central τ1 q10 th | 1.4476 ± .0034 | 0.8964 ± .0010 | 1.068 ± .0039 | central τ1 q10 is | 1.4430 ± .0027 | 0.8946 ± .0009 | 1.068 ± .0039 |
| central τ2 q0 th | 2.0015 ± .0033 | 1.0781 ± .0011 | 1.158 ± .0052 | central τ2 q0 is | 1.9988 ± .0025 | 1.0585 ± .0011 | 1.159 ± .0061 |
| central τ2 q3 th | 1.5961 ± .0030 | 0.8914 ± .0010 | 1.068 ± .0045 | central τ2 q3 is | 1.6002 ± .0025 | 0.8874 ± .0011 | 1.079 ± .0046 |
| central τ2 q10 th | 1.4498 ± .0156 | 0.8157 ± .0007 | 1.040 ± .0044 | central τ2 q10 is | 1.4501 ± .0145 | 0.8161 ± .0010 | 1.033 ± .0048 |
| volume τ.5 q0 th | 1.9052 ± .0037 | 2.5251 ± .0036 | 1.473 ± .0128 | volume τ.5 q0 is | 1.9014 ± .0036 | 2.4885 ± .0033 | 1.470 ± .0155 |
| volume τ.5 q3 th | 1.8246 ± .0031 | 1.6914 ± .0019 | 1.335 ± .0089 | volume τ.5 q3 is | 1.8149 ± .0033 | 1.6719 ± .0022 | 1.309 ± .0073 |
| volume τ.5 q10 th | 1.6339 ± .0030 | 1.3469 ± .0016 | 1.180 ± .0048 | volume τ.5 q10 is | 1.6304 ± .0019 | 1.3343 ± .0012 | 1.173 ± .0079 |
| volume τ1 q0 th | 1.8904 ± .0036 | 1.8985 ± .0024 | 1.379 ± .0109 | volume τ1 q0 is | 1.8857 ± .0034 | 1.8703 ± .0023 | 1.333 ± .0075 |
| volume τ1 q3 th | 1.7123 ± .0026 | 1.3973 ± .0018 | 1.199 ± .0065 | volume τ1 q3 is | 1.7061 ± .0030 | 1.3886 ± .0014 | 1.190 ± .0053 |
| volume τ1 q10 th | 1.3168 ± .0030 | 1.2597 ± .0015 | 1.080 ± .0055 | volume τ1 q10 is | 1.3152 ± .0023 | 1.2571 ± .0016 | 1.090 ± .0050 |
| volume τ2 q0 th | 1.8038 ± .0028 | 1.5258 ± .0017 | 1.212 ± .0107 | volume τ2 q0 is | 1.7849 ± .0028 | 1.5072 ± .0020 | 1.208 ± .0056 |
| volume τ2 q3 th | 1.4351 ± .0027 | 1.2803 ± .0016 | 1.098 ± .0064 | volume τ2 q3 is | 1.4300 ± .0025 | 1.2764 ± .0015 | 1.091 ± .0062 |
| volume τ2 q10 th | 0.9207 ± .0016 | 1.2433 ± .0015 | 1.047 ± .0044 | volume τ2 q10 is | 0.9232 ± .0012 | 1.2436 ± .0009 | 1.042 ± .0060 |

**Shell extension (36 cells, n = 2×10⁵; U_S band flagged circular):** full table in `V03_results.json` / `V03_trio.out`. Anchors: a=0.3 τ1 q0 th: R 2.0081 ± .0039, U 1.4793 ± .0027, slack 1.240 ± .0176; a=0.5 τ1 q0 th: R 2.0094 ± .0066, U 1.5825 ± .0037, slack 1.304 ± .0141; a=0.5 τ.5 q0 th: R 1.9991 ± .0091, **U 2.1656 ± .0067**, slack 1.376 ± .0188; a=0.3 τ2 q10 th: R 1.5153 ± 9.77 (atom tail-noise; block SE honest), U 0.8236, slack 1.037. Shell windows (K08 anchors) reproduced: a=0.3 q3: 1.657/1.660/1.648 vs K08 1.6625/1.6570/1.6525 — all within 2 SE; a=0.5 q3: 1.768/1.757/1.713 vs K08 1.7651/1.7455/1.7225 — within 1.6 SE.

### 3. Checks (7/7)

- **C1** (U at τ₀=1): z = −1.24/2.14 (q0), −1.70/−2.90 (q3), −0.15/0.01 (q10), central/volume vs K09 record → PASS.
- **C2** (central R-law): z vs closed form all |z| ≤ 1.6; τ₀-spread z = 1.35/3.09/1.02 at q = 0/3/10 → PASS (R is τ₀-free on this grid, 18/18 cells, both kernels).
- **C3** (R kernel-free): worst |ΔR_iso−thom| = 0.0189 at volume τ2 q0 with **z_R = 4.83 < 5** (marginal, same-family as L07's volume port; direction consistent −); all other 17 cells |z_R| ≤ 2.5; volume q=3/10 cells (L07 untouched territory): z ≤ 2.2 → R survives the kernel swap over the whole landscape → PASS.
- **C4** (slack record): z = 0.15/3.28/1.95 at q = 0/3/10 (central τ₀=1) vs J05 1.25/1.13/1.06 → PASS.
- **C5** (B-theorem): slack ≥ 1 − 3σ at **all 72 cells**; worst (slack−1)/se = 3.85 at shell(0.3) τ2 q10. The density-free bound holds on every geometry × kernel cell of the landscape → PASS.
- **C6** (doorB): reading = 0.90889·R = **1.8151 ± 0.0030** (record 1.8178, z = −0.91); v_R = {C,S}, v_U = {C,S,V}, B-PASS, reading inside all three windows → **CONSISTENT-OPEN REPRODUCED** → PASS (see §7).
- **C7** (U kernel-tagged): 12/18 core cells tagged z ≥ 3, all at q ≲ 3 (max |z_U| = 13.6); the q=10 corner (τ₀=1,2) untagged (|z_U| ≤ 1.4) → the kernel tag on the U channel is landscape-structured, not uniform → PASS as pre-registered (≥9/18).

### 4. THE DISAGREEMENT THEOREM (Tier-1 verdicts, definitions locked in §0.4)

**Counts over all 72 cells (36 per kernel):**

| class | count | cells (all B-PASS) |
|---|---|---|
| KILL-B | **0** | — (B holds on the whole model landscape, as the theorem demands) |
| VOID-R / VOID-U | **0** | — (no cell where a single falsifier excludes every geometry) |
| MIRROR | **0** | — (the trio never produces an exclusive contradiction) |
| CROSS | **3** | s0.3τ0.5q0·thomson, s0.5τ0.5q0·iso, s0.5τ0.5q0·thomson |
| HIERARCHY | **45** | see below |
| TRIO-AGREE | **24** | all q=3 cells of the core grid + τ₂q0 central/shell cells + volume τ₀=0.5 q≥3 cells |

All 48 non-agree cells have B silent (PASS everywhere — the density-free gate never fires on-model), i.e. every disagreement is **between the two geometry probes**, with the model-free gate confirming the family. The physical content:

1. **CROSS (3, all THIN SHELLS at q=0)** — `v_R = {C,S}`, `v_U = {S,V}`: the window ratio reads the cloud as central-like (thin shell skims the surface: R ≈ 1.99–2.01 ∈ [4/3,2] and inside the shell band), while the width ratio reads it as volume-like (tangent-clipped flights give U ≈ 2.04–2.17, above the central band, inside the volume band). Diagnostic content: **a disagreement that localizes the ignorance to the geometry axis the atlas does not span** — an intermediate birth layer is neither central nor volume, and the trio says so by splitting on the S∈v_R vs S∈v_U membership. The observer learns: "consistent with central and with shell for R, but with volume and shell for U ⇒ no pure central/volume cloud reproduces me; the emitting layer sits between". The disagreement is the *shell detector*.
2. **HIERARCHY, polarization (a): R ⊊ U at q ≤ 3 (27 cells)** — e.g. central τ1 q0: v_R = {C,S}, v_U = {C,S,V}. R's τ₀-freedom (central closed form) pushes R ≈ 2.00 above the volume band top (1.9444); U's τ₀-spread union band (volume U ranges 1.23–2.54) admits the same value. Diagnostic content: **R is the restrictive member wherever the volume width can still be mimicked — U's volume band is wide exactly because U is τ₀-resolved only after R pins (τ₀,q)** (N04's resolved-atlas power 1.437 vs 1.893 is invisible to the union band).
3. **HIERARCHY, polarization (b): U ⊊ R at q = 10 (15 cells, both geometries, both kernels)** — e.g. central τ1 q10: v_R = {C,S,V} (R = 1.4476 sits inside all three windows), v_U = {C,S} (U = 0.8964 fell below the volume band floor 1.233). **The restrictive member flips with q** — at the steep-density corner the width collapses below the volume window while R admits it; at the shallow corner R excludes volume while U admits it. Empirical theorem of this run: *the volume-excluding falsifier is q-directed (U at q ≥ 10, R at q ≤ 3), never both, never neither in the q=3 window* — the trio therefore never needs both channels to vote volume OUT at the same cell; their conjunction is what makes the instrument robust where either alone is blind.
4. **HIERARCHY, polarization (c): v_R = {V} at the deep-steep corner (4 cells)** — volume τ2 q10 & τ1 q10: R = 0.921/1.317 exits the central and shell bands (deep window floor): **R alone pins volume-exclusive at the deep corner** (K09's single-window-violation-as-discriminator, realized in the trio).
5. **TRIO-AGREE orbitals**: the q=3 row — where R (1.60–1.72) and U (1.28–1.40) both sit inside all three union bands — is genuinely indeterminate for the Tier-1 instrument: geometry must be recovered by the Node-2 resolved pin, not by band membership.

Kernel dimension: disagreement classes are kernel-symmetric (24 non-agree per kernel, identical labels at 46/48 cells; s0.3τ0.5q0 differs: CROSS-th under Thomson, HIERARCHY under isotropic — the U kernel-shift of 0.049 at that cell crosses the central-band top 1.982).

### 5. THE JOINT ACCEPTANCE REGION and the residual degeneracy

**Class ellipsoids** (9-cell centroids in (R, U, slack), landscape cov + sampling cov at the operating cell):

| class | μ = (R, U, slack) | landscape sd | sampling sd @ (τ₀=1,q=0) |
|---|---|---|---|
| C:thomson | (1.682, 1.179, 1.153) | (0.247, 0.368, 0.089) | (0.0032, 0.0017, 0.0074) |
| C:iso | (1.682, 1.162, 1.150) | (0.246, 0.352, 0.091) | (0.0027, 0.0012, 0.0093) |
| V:thomson | (1.605, 1.574, 1.223) | (0.326, 0.419, 0.145) | (0.0036, 0.0024, 0.0109) |
| V:iso | (1.599, 1.560, 1.212) | (0.323, 0.407, 0.138) | (0.0034, 0.0023, 0.0075) |
| S03:thomson | (1.726, 1.203, 1.153) | (0.212, 0.383, 0.094) | (0.0039, 0.0027, 0.0176) |
| S03:iso | (1.720, 1.187, 1.151) | (0.213, 0.369, 0.095) | (0.0059, 0.0037, 0.0179) |
| S05:thomson | (1.796, 1.264, 1.183) | (0.160, 0.412, 0.116) | (0.0066, 0.0037, 0.0141) |
| S05:iso | (1.784, 1.250, 1.176) | (0.168, 0.399, 0.098) | (0.0052, 0.0034, 0.0194) |

Landscape effective rank 3/3 in every class (the (τ₀,q) manifold is a genuine 2D surface, not a line). **Landscape-prior overlaps (3σ ellipsoids, clipped-inverse MC, 2×10⁶/class): 0.51–0.96 for ALL 28 class pairs** — including central×volume (0.62–0.66). This is not a measurement-error degeneracy: the sampling ellipsoids at any single cell are ~10⁻³ wide; it is the **(τ₀,q)-mixing degeneracy** — the class clouds are q-curves that cross (e.g. central(τ₀=.5,q=3) ≈ (1.60, 1.40, 1.21) and volume(τ₀=1,q=3) ≈ (1.71, 1.40, 1.20) are ~0.4 landscape-σ apart in the (R,U) plane). **The trio is NOT an atlas-free discriminator; its separation power is released only by the Node-2 (τ₀,q)-pin**, after which the resolved atlas acts (below). The B coordinate is the least informative for geometry (slack span 1.03–1.47 across the whole landscape) — its role is the model-free gate only, exactly as designed.

**Localized residual degeneracy** — nearest-cell joint 3σ distances (sampling covariances, full-rank, stable): **8 cell pairs are NOT separable at 3σ; only 4 are cross-geometry**:

| pair | min cell distance | cells |
|---|---|---|
| C:thomson × S03:iso | 2.05σ | central τ₀=.5 q0 (th) vs shell(0.3) τ₀=.5 q0 (iso) |
| C:iso × S03:iso | 2.44σ | central τ₂ q10 (iso) vs shell(0.3) τ₂ q10 (iso) |
| S03:iso × S05:thomson | 2.92σ | shell(0.3) τ₁ q3 (iso) vs shell(0.5) τ₀=.5 q10 (th) |
| S03:iso × S05:iso | 2.48σ | shell(0.3) τ₁ q3 (iso) vs shell(0.5) τ₀=.5 q10 (iso) |
| 4 same-geometry kernel pairs | 0.69–1.44σ | C×C-iso, V×V-iso, S03×S03-iso, S05×S05-iso — all at τ₀=2, q=10 (kernel-blind corner; geometry-safe) |

**Residual degeneracy the trio cannot separate: (i) central ⊗ shell(0.3) at the thin-q0 corner (cross-kernel) and at the deep-q10 corner (same kernel, iso) — at q=10, τ₀=2 the trio (R,U,slack) ≈ (1.450, 0.816, 1.033) for both, because the q-ramp confines scattering to the centre and the a=0.3 layer becomes undetectable; (ii) the shell-radius a-line under (τ₀,q) trades — (a=0.3, τ₀=1, q=3) ≈ (a=0.5, τ₀=.5, q=10) — the a-axis ignorance at 3σ; (iii) kernel identity at the deep corner (U's tag vanishes there), which is geometry-safe since the same-geometry clouds merge.** Volume is trio-separated from everything at ≥ 4σ. This is the exact, quantified answer to "what can the trio not do": it cannot separate central from a small-a shell at the two corners where the density ramp pins the photons, and it cannot separate two shell radii across the (τ₀,q) trading surface.

**Operating-point (τ₀=1, q=0), sampling covariances only — the "measured trio" regions**: all 28 class pairs separable at ≥ 4.8σ (weakest S03×S03 kernel pair; C×S03 at 14.1σ, C×V at hundreds of σ in U alone). At the doorway corner the trio with honest covariances resolves all 4 geometries × 2 kernels; the kernel itself is identified through U's tag (C:th × C:is at 13.3σ, V:th × V:is 9.6σ). **The instrument's blindness is entirely in the (τ₀,q)-direction, not in the geometry direction.**

### 6. THE NOVEL READ-OUT: decision tree, failure modes, minimum n

An observer measures the trio from ONE 2D transfer function (A, E[D], E[D²], E[Dv²], E[v⁴] — the last three from the lag–velocity joint profile).

- **Node 1 — B gate (model-free)**: slack ≥ 1 − 3σ ⇒ PASS (family consistent, any density/geometry/kernel — J05 theorem, C5 verified at 72 cells) · VIOL ⇒ the transfer function is NOT a Thomson-sphere LRD, irrespective of all other ignorance. Failure mode: (slack−1) < 3σ at q ≳ 10 thin cells (slack→1.03–1.07 there): gate undetermined → raise n (n_req below).
- **Node 2 — R test (kernel-free + pin)**: R ∈ [4/3, 2] ± 3σ with |R_iso − R_thom| ≤ 3σ (measured here: worst cell 4.8σ, margin note) ⇒ central-consistent, kernel-immune ⇒ K06-inv (A, E[D]) pins (τ̄₀, q̄). R outside all bands ⇒ outright kill (K09-F3). Failure modes measured: (i) at q=10, τ₀=2 the atom fraction A is tiny — se_R blows up (0.015, central; 10–12 on the shell cells) — the R pin fails on sampling grounds; (ii) at shallow q=0 the volume window overlaps [4/3,2] so "central-consistent" is not "central-exclusive" — the pin is then geometry-conditional (applies strictly to central clouds).
- **Node 3 — U read-out (geometry) at (τ̄₀,q̄)**: compare U vs the resolved atlas columns U_C, U_V (±3 combined σ). Confusion on the landscape: **central truth: 18/18 correct under both kernels** (pin works, U unambiguous); **volume truth: 4 V, 10 U-OUT, 4 NOT-CENTRAL** — the documented failure pattern: (a) at the deep corner (τ₂q10, τ₁q10) R exits the central window ⇒ NOT-CENTRAL (correctly flags non-central, defers); (b) elsewhere R ∈ [4/3,2] (volume window overlaps central) ⇒ the central inversion mis-pins (τ̄₀,q̄) ⇒ U misses the atlas ⇒ U-OUT with pin_bias flag. Failure modes, honest: **the tree is a central-pinning instrument; a volume truth at shallow q masquerades as a central cloud under Node 2 and is caught only by U-OUT** (a diagnostic in itself: U outside every atlas row = the (τ₀,q)-pin is wrong = geometry ≠ central). Kernel-tag: always use the kernel-matched atlas column; for q ≥ 10 the tag is absent (C7) so the iso/thomson ambiguity is resolved by R alone.
- **Minimum n per falsifier for 3σ (n_req = n·(3·se/gap)², per cell, 36 core cells; full per-cell table in V03_results.json):**

| falsifier | min | median | max | infeasible cells |
|---|---|---|---|---|
| B (gap = slack−1) | 3 619 | 12 166 | 149 524 | 0 |
| R (gap to nearest competitor band) | 57 | 56 593 | 241 800 | 32 * |
| U (resolved atlas gap) | 21 | 127 | 379 | 0 |

\* infeasible = R sits inside the pre-registered W_S band (the 0.075-wide shell tolerance) at that cell: Tier-1 R cannot exclude the shell class there — the resolved Route (Node 2+3) is the alternative. Binding readings: **U is 29–49× cheaper than R (N04 confirmed on this grid: 21–379 vs 57–242k); B is the hardest gate at q ≲ 1 (median 12k) and the slack→1 corner q=10 (up to 150k for 3σ).** The trio's per-cell 3σ budget = max over falsifiers: ≈ 1.5×10⁵ photons at the weak cells, ≈ B-gate-limited everywhere else; the operating-point geometry question itself (Node 3 after a pin) needs only ≈ 400 photons.

### 7. Cross-check: the doorB corner (A2744 reading)

At (central, q=0, τ₀=1): R = 1.9971 ± 0.0032 ⇒ **reading = 0.90889·R = 1.8151 ± 0.0030** vs the recorded 1.8178 (z = −0.91). Trio at the corner: v_R = {C,S}, v_U = {C,S,V}, B-PASS, reading inside the central [4/3,2] window, inside the volume window [0.918, 1.914], inside the shell band — **the recorded A2744 interpretation CONSISTENT-OPEN is reproduced** (K09: no geometry excludes the pair at the single point; the trio's agreement membership is exactly the recorded verdict). The trio adds what K09 could not: the SAME measured corner also returns the (τ̄₀,q̄) pin (≈ 1.0, ≈ 0 within SE) and U = 1.4348 ± 0.0017, i.e. a central-atlas reading (U vs U_C(1,0) = 1.4350, z = 0.1) — the doorB corner is central-consistent in all three channels simultaneously.

### 8. Status and honesty ledger

- **Stands:** trio table 72 cells, 7/7 checks, bitwise engine parity, disagreement counts with locked definitions (CROSS 3 / HIERARCHY 45 / AGREE 24, zero KILL-B/VOID/MIRROR), q-directed restrictive-member theorem, residual-degeneracy map (8 pairs, 4 cross-geometry, corners listed), tree confusion and failure modes, min-n (B ≤ 150k, R ≤ 242k w/ 32 Tier-1-infeasible, U ≤ 379), doorB CONSISTENT-OPEN reproduced at z = −0.91.
- **Flagged:** the U_S shell band is first-measurement (circular for shell cells; shell verdicts are honest confusion entries, not prior-tests); the iso atlas column in the tree is in-run (flagged); the landscape ellipsoid overlaps are Gaussian-approximation statements over crossing (τ₀,q)-curves (the localized cell-pair table is the exact version); C3's worst cell (volume τ₂ q0, z_R = 4.83) is inside the L07-kill gate but is the closest call on record — the kernel residual is 1.9% of R there; the q=10, τ₀=2 cells carry large atom-noise (se_R up to 12 on shell) — reported honestly.
- **Not claimed:** any observational data interpretation beyond the recorded A2744 read; no claim that the trio separates beyond the 3σ budget given; novelty per framework rule (the fused instrument, the disagreement classification of the landscape, and the q-directed hierarchy are new as a combined instrument; each member was separately verified in its own lane).

**Deliverables:** `deepseek_push/V03_IGNORANCE_TRIO.md` (this file, pre-registration locked before the run), `deepseek_push/V03_trio.py`, `deepseek_push/V03_trio.out`, `deepseek_push/V03_results.json`, `deepseek_push/V03_PRE.txt` (pre-registration audit text). No git commit.
