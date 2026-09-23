# K09 — J10-II: GEOMETRY-AWARE WINDOWS and the robustness of the a₀-radius reading

**2026-09-23 · moment channel → framework core · redo of J10 with central / shell(a) / volume windows · follows J10 (6/6) + J11 (volume atom, V1/V2 → V2 RESOLVED below) · exit 0, 19/19**

## 0. The question

J10 defined the framework-core reading

```
    J10-I  =  −ln A · r_B / (c · d_phys)   =   (r_B/R) · W ,      W ≡ −ln A / E[D]
```

with r_B = √(GM_b/a₀(ρ_B)) (density-local one-boundary radius), the measured pair (A, d_phys) = (zero-lag spike, mean lag), and E[D]·R/c = d_phys (Theorem 1, frozen). J10 used ONE window (central [4/3, 2]); J11 showed the volume window is τ₀-dependent. K09 builds the **J10-II surface** W_g(τ₀, q) for g ∈ {central, shell(a), volume}, answers the robustness question that decides the framework claim, derives the precision needed to resolve central vs volume, and states the per-geometry falsifier. No circular fitting: measurements enter only the tested quantities (J10-I_obs, U_obs); every window is derived (closed form or engine).

## 1. Two corrections to the record (both machine-caught here)

1. **The J11 V2 failures (z = 29.5 / 83.6) were a closed-form bug, not engine noise — the ENGINE was right.** J11's quadrature chord `rμ + √(1−r²(1−μ²))` is not the surface-exit distance for outward-pointing photons (μ>0); the correct root is `−rμ + √(1−r²(1−μ²))` — exactly the engine's `wall = −pd + √(pd²−r²+1)`. With the minus root the closed form agrees with the engine to < 0.5 SE at ALL q (C1: z = 0.40/0.35/0.04 at q=0/3/10; n=5×10⁵). The J11 MC window numbers (1.897/1.710/1.314 at τ₀=1) STAND (reproduced: z_record = 0.7/3.4/3.4 vs the record with the deterministic J11-seed rerun at their n; run-to-run z identical — the residual spread is MC realization at the quoted n, within the 4σ preregistered budget).
2. **The J11 "thin limit ≈ 2.2, crossing the central window from above" was an e₀-scaling artifact.** e₀ = lim E[D]/τ₀ ≈ **0.3876** (measured at τ₀=0.15), not 0.338; the measured thin volume window is ≈ 1.88–1.91 (τ₀ = 0.15–0.5), i.e. **below** the central 2.0. The volume window never crosses the central window from above at q=0. (Also corrected for the record: the J11 verdict table's "central 1.4413 at q=3 AND q=10" — the closed form at q=3 is 1.600, J09's MC: 1.5980. And ⟨chord⟩ for a surface-emission point is **1/2**, not 4/3 — 4/3 is the classical chord-of-a-sphere mean, not the first-flight chord: ⟨ch⟩ = 1.0 central / 0.7503 volume / 1/2 surface, C4.)

## 2. The J10-II surface (derived windows)

**Central** (closed form, τ₀-free, J09-D 27/27): W_cen(τ₀,q) = (1+q/3)/(½+q/4) ∈ **[4/3, 2]**: 2.000 / 1.600 / 1.4444 at q = 0/3/10.

**Volume** (corrected quadrature for A; engine MC for E[D], n = 1.2–3×10⁵, subsample SE):

| τ₀ \ q | 0 | 3 | 10 |
|---|---|---|---|
| 0.15 (thin) | 1.8825 ± 0.022 | 1.8662 ± 0.009 | 1.8210 ± 0.006 |
| 0.5 | 1.9144 ± 0.005 | 1.8208 ± 0.009 | 1.6371 ± 0.008 |
| 1.0 (J11 anchor) | 1.8814 ± 0.010 (rec. 1.897) | 1.7103 ± 0.007 (1.7104) | 1.3288 ± 0.006 (1.3142) |
| 2.0 | 1.8033 ± 0.007 | 1.4228 ± 0.006 | 0.9184 ± 0.003 |
| 3.0 | 1.6981 ± 0.005 | 1.2126 ± 0.007 | 0.7149 ± 0.004 |
| 5.0 (deep) | 1.4712 ± 0.004 | 0.9316 ± 0.005 | **0.5003 ± 0.003** |

Volume window over the grid: **[0.5003, 1.9144]** (τ₀ ∈ [0.15, 5], q ∈ {0,3,10}; thin edge ≈ 1.88–1.94, deep-steep edge ≤ 0.50). Note how far the deep q=10 corner sits below 4/3 — the volume window is NOT [1.3, 1.9] globally.

**Shell(a)** (quadrature atom; shell-birth engine for E[D], n=10⁵): W_shell(a) interpolates central→surface: at a = 0.1: ~2.00 (τ₀-flat, q=0); a = 0.5: ~1.99→1.57 (q=0→10, τ₀=1); a = 0.9–0.99: ~1.6–1.9. Union over a ∈ [0.1, 0.99], τ₀ ∈ {0.5,1,2}, q ∈ {0,3,10}: **[1.4298, 2.0063]**.

**Width surface** U_g = std(D)/E[D] (R-free, the third observable), τ₀=1: central 1.437 / 1.076 / 0.897 vs volume 1.893 / 1.402 / 1.260 at q = 0/3/10.

## 3. The robustness question — verdict

Observed pair (doorB A2744-QSO1): **R = 45 ld, r_B = 40.9 ld (×1.10)**. Reading under geometry g: J10-I_g(τ₀,q) = (r_B/R)·W_g(τ₀,q) = 0.90889·W_g.

| reading at q=0/3/10 (τ₀=1) | q=0 | q=3 | q=10 |
|---|---|---|---|
| central | 1.8178 ∈ [4/3, 2] ✓ | 1.4542 ∈ ✓ | 1.3128 < 4/3 ✗ (exit) |
| volume | 1.7281 ∈ [0.50, 1.91] ✓ | 1.5421 ∈ ✓ | 1.2093 ∈ ✓ |
| shell(a) | [1.485, 1.823] ∈ [1.43, 2.01] ✓ | ∈ ✓ | [1.311, 1.582]: small-a exits ✗ |

**Single-point (τ₀=1, q=0) — the J10/J11 echo: every geometry keeps the pair inside its window** (central 1.818 ∈ [4/3,2]; volume 1.728 ∈ volume range; shell ✓). The framework radius assignment survives geometry ignorance at the physical corner — CONSISTENT-OPEN is preserved under all three geometries.

**Strict clause — "for ALL (τ₀,q)": NO geometry keeps the pair inside for every (τ₀,q)** (RO, measured): central exits for q beyond q\* ≈ **7.98** (reading < 4/3 for q > q\*; 40 grid cells exit); volume exits at the deep-steep corner (τ₀=5, q=10): 0.455 < 0.500; shell exits at the 9 q=10/small-a cells (e.g. a=0.1: 1.326 < 1.430). **The exits have one common cause, independent of geometry: R_meas > r_B** compresses the reading by 0.90889 and pushes it below the window floor at the W-minimum corner. Formal statement (measured): reading ∈ window for ALL (τ₀,q) **⟺ R_meas ≤ r_B**, for EVERY geometry. With R = r_B the reading = W ∈ window by construction (C8/scale=1 check). The ×1.10 doorB offset is the stringent status: the x1.10 radius systematics, not geometry ignorance, is what the strict clause trips on — and it trips all geometries identically. **No geometry singles itself out as breaking the claim harder than the others at the observed corner; geometry ignorance does not break the claim** (the claim's own sharp kill requires R > r_B·Wmax/Wmin, see §5).

Discriminating power note (J11's rule in action): at (τ₀=1, q=10) the pair is INSIDE the volume window but OUTSIDE the central one — a single-window violation is a **geometry discriminator**, not a framework kill; at (τ₀=1, q=0) no geometry is excluded (J11 kill rule F3 confirmed).

## 4. Precision needed for 3σ central-vs-volume discrimination (fixed q)

At fixed q the volume band over τ₀ is derived; the central value is a point. Two regimes (A_obs = e⁻¹ illustrative; error split equal: se(A)/A = se(d)/d = f, from se(J10-I)/J10-I = f·√(1 + 1/ln²A), lnA = −1):

| q | volume band (τ₀-scan) | central | mode | Δ | required se(A)/A = se(d)/d (3σ) |
|---|---|---|---|---|---|
| 0 | [1.471, 1.914] | 2.000 | **τ₀-free resolvable** (band below central) | 0.0856 | **≤ 1.01 %** each |
| 3 | [0.932, 1.866] | 1.600 (inside band) | spike-pinned (τ₀\*≈0.60) | 0.2208 | ≤ 2.86 % each |
| 10 | [0.500, 1.821] | 1.444 (inside band) | spike-pinned (τ₀\*≈0.24) | 0.3144 | ≤ 4.21 % each |

Error budget (the derivative, se(J10-I)/J10-I = √[(se(A)/(A|lnA|))² + (se(d)/d)²]):
- **q=0 is the binding case: se(A)/A ≤ 1.0 % and se(d)/d ≤ 1.0 %** for 3σ resolution — and it needs NO τ₀ pinning because the corrected thin limit kills J11's old "crossing" ambiguity (the volume band sits wholly below 2.0).
- q=3,10 are EASIER in Δ but demand the spike to pin τ₀ (A_obs ∈ {e⁻¹} pins τ₀\* per geometry); at any precision the τ₀-free bands contain the central point there.
- Independent reserve: the width ratio U = std(D)/E[D] separates central vs volume already at 1.44 vs 1.89 (q=0, τ₀=1) — a ~30σ-class separation at n=2×10⁵ per epoch — and needs no radius at all.

## 5. The falsifier (pre-registered, per geometry)

Given the measured triple (A_obs, d_obs, σ_d) and the derived windows:

- **F1 (window kill):** J10-I_obs = −ln A_obs·r_B/(c·d_obs) outside [Wmin_g, Wmax_g] + 3σ kills the a₀-radius reading under geometry g. Measured-space form: −ln A_obs/d_obs outside [Wmin_g, Wmax_g]·c/r_B. Windows (grid-supported): central **[1.3333, 2.000]**, volume **[0.5003, 1.9144]**, shell **[1.4298, 2.0063]**.
- **F4 (radius kill):** a measured lag-radius R > r_B·Wmax_g/Wmin_g kills under g for EVERY (τ₀,q): central **61.35 ld** (= 1.5·r_B, J10's sharp form), volume **156.5 ld** (the deep volume floor at 0.50 makes the volume reading far harder to kill — the J10 "R > 1.5 r_B" kill is central-only, a substantive geometry dependence), shell **57.39 ld**.
- **F2 (width kill):** if J10-I_obs ∈ window, invert under g with the framework radius (A_g(τ₀,q) = A_obs; E[D]_g(τ₀,q) = c·d_obs/r_B) → predicted width ratio U_g = std(D)/E[D]_g; measured U_obs = σ_d/d_obs deviating > 3σ kills the reading under g (inversion broken). U needs no radius (σ_d/d_obs cancels R).
- **F3 (outright kill):** J10-I_obs outside the windows of ALL geometries kills the transfer reading outright; a single-window violation is a geometry discriminator, not a framework kill (J11 rule, confirmed).
- DoorB-illustrative anchor: (A, d) = (e⁻¹, 22.5 ld) → J10-I = 1.8178 ∈ every window; U_obs ∈ {1.44 (central), 1.89 (volume)}.

## 6. Status ledger

- J10-II surface derived + verified **19/19** (exit 0): C1 corrected atom (z≤0.4), C2 J11 anchors reproduced (z≤3.4 combined), C3 central flat-in-τ₀ + endpoints, C4 chord anchors (1 / 0.7503 / 0.5), C7 readings per geometry, RO exits detected for all three geometries + scale=1 restoration + exit gate q\* = 7.98 + kill radii, error budget, width surface, falsifier records.
- K07 lane (volume τ₀-surface) and K08 lane (shell(a) surface): derived here as the not-landed lanes promised, with the closed forms corrected (chord root) — see §2 tables.
- J11 record changes: V2 closed form corrected (engine was right); thin-e₀ ≈ 0.388 (not 0.338) and thin-window ≈ 1.9 (not ≈ 2.2, no crossing); central table transcription at q=3 fixed (1.600); surface-emission ⟨chord⟩ = 1/2 (not 4/3). None of the J11 MC window numbers at τ₀=1 change materially (≤ 1.2 %).
- No git commit. No circular fitting: measurements enter only J10-I_obs and U_obs; all windows closed-form/derived.

## 7. Novelty (per user rule: novel + framework-core only)

The geometry-aware window surface (central/shell(a)/volume × τ₀ × q) as a **test of the a₀-radius assignment under geometry ignorance**, the sharp conditional "reading ∈ window ∀(τ₀,q) ⟺ R_meas ≤ r_B", the per-geometry kill radii (the ×3 range central→volume), and the R-free width discriminator U are not in STANDING.md, not in the frozen lane, not in posterior RM literature (scattering RM does not use the atom+lag+width inversion).