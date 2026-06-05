# Ultra-Precision Predictions Ledger
### Emergent-gravity framework: a₀ = c²√(Λ/32π) = (c/2)√(G ρ_Λ)

*Produced by a 19-agent compute→verify→synthesize workflow (9 channels, all adversarially verified: 9 confirmed, 0
corrected, 0 flawed). **C.Z. independently re-ran the headline numbers** — a₀, Z, κ, the eRASS1 cluster η, and the
forecast floor all reproduce. Per-channel scripts: `predictions/ultra_precision_a0.py`, `door4_ultraprecision.py`,
`door2_dsph_ultraprecision.py`, `door1_lensing_ultra.py`, `btfr_offset_ultra.py`, `door5_efe_ultraprecision.py`,
`door6_galaxy_clusters.py`, `door6_wide_binaries_ultra.py`, `combined_fisher_ultra.py`, master in
`ledger_master_numbers.py`.*

**Constants (held fixed throughout):** c = 299792458 m/s (exact); G = 6.67430×10⁻¹¹ (CODATA 2018); M_sun =
1.98892×10³⁰ kg; 1 Mpc = 3.0857×10²² m. **Cosmology:** Planck 2018 H₀ = 67.36 ± 0.54 km/s/Mpc, Ω_Λ = 0.6847 ±
0.0073, Ω_m = 0.3153 ± 0.0073. **Dark energy:** DESI DR2 CPL w₀ = −0.752 ± 0.057, wₐ = −0.86 ± 0.22, ρ_DE(a) =
a^(−3(1+w₀+wₐ)) exp(−3wₐ(1−a)).

---

## Honest one-paragraph summary

From the cosmological constant alone the framework computes a single acceleration scale **a₀ = 9.355×10⁻¹¹ m/s²
(± 0.96 % statistical, ± ~14 % systematic)** and fixes two pure numbers **Z = cH_Λ/a₀ = 5.789** (= √(32π/3), exact)
and **κ = ½** (exact). That central a₀ matches the simple-μ SPARC fit (9.1×10⁻¹¹) to +2.8 % but sits 22 % *below*
McGaugh's RAR value (1.2×10⁻¹⁰); the gap is absorbed by the ~20 % interpolating-function systematic, so it is
consistency, **not independent confirmation**. The dominant uncertainty on every *absolute* quantity is the MOND
μ-function systematic (~20 %, ~20–30× the cosmological error), **inherited, not solved**. **Crucially, the absolute
a₀, the lensing/wide-binary/dwarf z=0 scorecards, and the cluster failure are all SHARED with ordinary constant-a₀
MOND — they test the *value* of a₀, not the framework.** The one framework-distinct content is the predicted
**evolution a₀(z) = a₀(0)√(ρ_DE(z)/ρ_DE0)**, which constant-a₀ MOND fixes at exactly 1.0; it is everywhere a
**forward** prediction (no z>2 kinematics exist yet) whose decisive form is a high-z baryonic Tully–Fisher offset. Two
liabilities are carried in full: galaxy **clusters** (4.7σ, factor-~1.9 residual) and three **dwarf-spheroidal
outliers** (~2.5–3.3σ). Nothing here is a discovery; the value is a tight *prediction of a₀ from Λ* plus a *single
falsifiable evolution signal*.

## Master table

| # | Channel | Central value | Stat err | Syst err | Status | Distinct? |
|---|---------|---------------|----------|----------|--------|-----------|
| 1 | **a₀ scale + coefficient** | **a₀ = 9.355×10⁻¹¹ m/s²**; Λ = 1.0891×10⁻⁵² m⁻²; ρ_Λ = 5.835×10⁻²⁷ kg/m³; cH_Λ = 5.415×10⁻¹⁰; **Z = 5.7888**; **κ = 0.5000** | ±0.96 % (H₀ 0.80 % ⊕ Ω_Λ 0.53 %); Z,κ **zero** | ±~14 % (μ-shape) | consistent | **MOND-shared** |
| 2 | **MDAR / RAR** (175 SPARC, 3389 pts) | scatter 0.195 dex; D-shift z=2 −7.2 %, z=3 −14.2 % | evol z=3 ±4.9 % | a₀ ±24 % (cancels) | consistent | **distinct** (evolution) |
| 3 | **Dwarf spheroidals + EFE** (8 MW dSph) | median \|log(pred/obs)\| 0.088 dex (5/8 ok); σ(z=3)=0.927 | 8–22 % per-dwarf | μ→~4–7 % (a₀^¼) | consistent (3 outliers) | **MOND-shared** (evolution) |
| 4 | **Lensing** (saturated deflection) | α_∞ = **0.508″**(10¹¹), **5.08″**(10¹³), **16.1″**(10¹⁴); peak +3.0 % at z≈0.41 | α ±0.48 %; evol ±5.0 % | α ±6.9 % | forward | **MOND-shared** (evolution) |
| 5 | **High-z BTFR** ← **decisive** | dlogV: z=2 **−3.7 %**, z=3 **−7.3 %** (−0.033 dex), z=6 −15.7 % | z=3 ±5.6 % (wₐ) | **cancels** | forward | **framework-distinct** |
| 6 | **EFE evolution** | a₀(0)/a₀(3) = **1.357** (+35.7 %); crosses e_N=1 at z≈3.4 | ±11.5 % (DESI) | **zero** (ratio) | forward | **framework-distinct** |
| 7 | **Galaxy clusters** (eRASS1, 9830) | **η = 1.92** (misses ~1.9× at R500); evolving-a₀ buys +0.025 dex to z~0.3 (~28× too small) | ±0.09 (WL) | **±0.17 (μ)** | **tension** (4.7σ) | **MOND-shared** |
| 8 | **Wide binaries** (z=0) | s_t = **9753 AU** (1.5 M_sun); boost +2 % to +11 % | ±0.48 % | band [8611, 9888] AU | consistent (**contested**) | **MOND-shared** |
| 9 | **Combined Fisher (β)** | stat: 30 discs@z3→3.0σ, 60@z3.5→5.3σ; **marginalized floor caps single-z at 1.6–2.0σ ∀N** | σ(β)=0.62@z3 floor | cancels | forward | **framework-distinct** |

## Ultra-precise vs systematics-limited

- **Exact / ≪1 %:** Z = √(32π/3) = 5.788810 and κ = ½ carry *zero* cosmological error (the √Λ cancels); Λ, ρ_Λ, cH_Λ
  fixed to 0.96 % by Planck. **All evolution RATIOS** (dlogV, D(z)/D(0), σ(z)/σ(0), α(z)/α(0), e_N(z)/e_N(0)) are
  coefficient-free — the μ-systematic and absolute-a₀ error cancel, leaving only the DESI w₀/wₐ error (±0.7 % @z=1 to
  ±8.4 % @z=6). These are the cleanest framework-distinct predictions.
- **Systematics-limited (~20 % floor):** the absolute a₀ and everything ∝a₀ at z=0 (lensing α_∞, wide-binary s_t,
  cluster η, dwarf σ). This μ-function systematic is ~20–30× the cosmological error and is **inherited from MOND, not
  reduced** by the framework. (Planck H₀–Ω_Λ are positively correlated; the true stat error is ~1.16 %, still ≪ syst.)

## Honest tensions (called out plainly)

1. **Galaxy clusters — a real, inherited failure (4.7σ).** On 9,830 real eRASS1 clusters (Bulbul+2024), after the
   full MOND boost the framework still misses **η = 1.92 ± 0.20** of the weak-lensing mass at R500, flat in mass and
   temperature — the classic factor-~2 cluster problem, **identical to constant-a₀ MOND**. Evolving a₀ buys only
   +0.025 dex to z~0.3, ~28× too small to close the 0.6–0.8 dex cluster-BTFR offset. *(At the framework's own
   a₀=9.355×10⁻¹¹ rather than the RAR anchor, η rises to 2.15; 1.92 is the conservative choice.)* **An open liability,
   not a win.**
2. **Dwarf-spheroidal outliers (~2.5–3.3σ).** 5/8 classical dSphs reproduced with no DM; **Sextans, Draco, Ursa
   Minor over-dispersed**, and the tensions do *not* wash out across the plausible M/L range. Shared with ordinary
   MOND; likely tidal/binary/non-equilibrium or a wrong EFE coefficient.
3. **Wide binaries — contested data.** Framework predicts s_t = 9753 AU, boost +2–11 %; but Chae (2023–26) reports a
   MOND-like detection while Banik+2024 / Pittordis–Sutherland report a Newtonian null. Neither confirms nor refutes;
   Gaia DR4 is the arbiter. Zero framework-distinct leverage (no z=0 evolution signal).

## The single decisive test: high-z BTFR (Channels 5 & 9)

- **Prediction:** at fixed M_bar, high-z discs fall **below** the z=0 BTFR by dlogV(z) = ⅛·log₁₀[ρ_DE(z)/ρ_DE0] —
  central **−7.3 % in V at z=3** (±5.6 %), −15.7 % at z=6. *Sign subtlety (honest): under DESI thawing DE, ρ_DE peaks
  at z≈0.405 (+12.7 %) and only crosses below today at z≈1.06, so the offset is slightly positive for z≲1 and the
  clean "discs below" regime is z≥2.*
- **The sign is the decisive content.** Constant-a₀ MOND → dlogV = 0 (exactly). The rising √ρ_total reading → the
  *opposite* sign (+16 % @z=1 to +80 % @z=6). One clean BTFR point at z≥3 chooses among the three. Against dark
  matter the evolution is impossible (a ΛCDM halo obeys the SEP).
- **Forecast — corrected, honest.** Statistically ~30 discs@z=3 → 3σ, ~60@z=3.5 → 5σ. **But** the DESI w₀/wₐ
  uncertainty (partly degenerate with β) imposes a **marginalized floor σ(β) ≈ 0.62@z=3 / 0.50@z=5 independent of N**,
  capping single-redshift significance at **1.6–2.0σ for any sample size**. Multi-z (z=3 & z=5) breaks part of the
  degeneracy but still caps at ~4.9σ with today's DESI prior. **The decisive test is DESI-limited above ~30 discs, not
  galaxy-limited** — 5σ needs a ~2× tighter DESI w₀/wₐ prior or multi-z BTFR. *(This corrects the earlier
  `combined_forecast.py`, which omitted the w₀/wₐ floor and over-promised.)*
- **Current data can't test it.** Real Übler+2017 KMOS³D (z~0.6–2.5) matches the *direction* but the predicted
  magnitude (~0.001–0.025 dex) is below the ~0.05 dex per-galaxy scatter. A 3σ mean needs ~30 discs at z=3 or ~4 at
  z=6 — JWST/ALMA-era z≥3 kinematics.

**Honest non-win:** declining a₀ at high z means a *weaker* early MOND boost — it works *against* the JWST
"too-massive-too-early" galaxies, not for them.

---

*Bottom line: one tight, systematics-limited prediction of a₀ from Λ (MOND-shared); two exact pure numbers (Z, κ);
one decisive but forward and DESI-limited evolution signal (high-z BTFR); two carried liabilities (clusters 4.7σ,
dwarf outliers ~3σ). No claim here is a present-day detection of framework-distinct physics.*
