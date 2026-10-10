# CFG545: does ΛCDM's emergent RAR scale scale with Λ? The d ln a₀/d ln Λ test of "a₀ is set by dark energy". FROZEN before any script exists

Owner chat 10-09. κ = ½ is FITTED. Footings 9.36e-11 / 1.13e-10 are never pooled. Cold energy mass is still required; no dark-matter particle is added. ΛCDM is the comparator. Nothing here may be read as the data favouring the framework.

**Idea under test (owner).** Cold energy clumps first and galaxies form inside it; the acceleration scale is set by dark energy, a₀ = κ c √(G ρ_DE). **Hook:** CFG477 (ΛCDM + DC14 cores on SPARC) produced an emergent a₀ ≈ 9.7e-11 with no tie to Λ.

## Disclosure of what was read before freezing (dated 10-09)
The literature census (task 1) was read before this file was written: arXiv abstracts via the export API (CC0 metadata), plus WebFetch summaries, which are PROVISIONAL. Papers read:
- Keller & Wadsley 2017; Ludlow+17; Navarro+17; Dutton+19; Paranjape & Sheth 2021; Grudić+20; Mayer+23 (Magneticum preprint text).
- Barnes+18 and Salcido+18 (the varied-Λ EAGLE runs).
- Dolag+04 (halo concentrations in dark-energy cosmologies).

Findings already known at freezing:
- (i) No published varied-Λ simulation located measures a rotation curve, the RAR, a characteristic acceleration, halo concentrations or galaxy sizes. Barnes+18 ran Λ = 0 to 300 Λ₀ but measured collapse fractions, accretion and star-formation efficiency (summariser reading).
- (ii) Magneticum's z ≈ 0.1 fitted a₀ is 1.12e-13 km s⁻² (= 1.12e-10 m s⁻²).
- (iii) Grudić+20 explain g† as ⟨ṗ/m★⟩ ~ 0.1 G m_p/σ_T, which contains no cosmological parameter.

No scaling number below had been computed.

## Statistic
**s ≡ d ln a₀,emergent / d ln Λ.** It is evaluated at Λ = Λ₀ as a central log finite difference over λ ≡ Λ/Λ₀ ∈ {0.5, 2}. The full curve a₀(λ) for λ ∈ {0.1, 0.3, 0.5, 1, 2, 3, 10, 30, 100} is reported, along with the span slope over λ ∈ [0.1, 10].

The two predictions:
- **Owner's picture: s = 0.5 exactly** (a₀ ∝ √ρ_DE ∝ √Λ).
- **ΛCDM: s is estimated here.** In its own explanation, the emergent scale is set by galaxy-formation physics and halo structure.

## The ΛCDM estimator (declared)
**Which universe is varied.** As in Barnes+18:
- Physical ω_m = 0.1431, ω_b = 0.02237, n_s = 0.965 and the early-time primordial amplitude are held fixed. σ₈ = 0.811 is set at λ = 1, a = 1.
- Only ρ_Λ = λ ρ_Λ0 is changed, with ρ_Λ0 from h = 0.674, Ω_Λ = 0.685. The background is flat with radiation ignored.

**Observed when:**
- (P) primary: at a = 1, the same CMB temperature and the same physical ρ_m.
- (T) variant: at fixed cosmic age t₀(λ = 1).

**Linear theory.**
- The growth factor is D(a) ∝ H(a) ∫ da/(aH)³, normalised so D → a in the matter era.
- σ(M) is a top-hat over the Eisenstein & Hu 1998 no-wiggle transfer function in physical units (λ-independent), times D_λ(a).

**Halo structure versus λ.** Three declared concentration models:
- **L16-crit** (primary): Ludlow+16 collapsed-mass model. ⟨ρ₋₂⟩ = 650 ρ_crit,λ(z₋₂), where z₋₂ solves M_coll(z₋₂) = M₋₂ = M m(1)/m(c), with M_coll(z) = M erfc{[δ_c/D(z) − δ_c/D(z_obs)]/√(2[σ²(0.02 M) − σ²(M)])} and δ_c = 1.686. ρ_crit,λ includes the Λ term.
- **L16-m**: the same, with ρ_crit,λ(z₋₂) replaced by the matter-only background, ρ_m(z₋₂)/Ω_m,λ=1(0). This is the same normalisation at λ = 1, with no explicit Λ term.
- **D04**: Dolag+04 growth scaling. c → c × D_λ(a_coll)/D_1(a_coll) at the collapse epoch, with a_coll from L16-crit at λ = 1.

All halos use a fixed physical aperture: M at 200 × ρ_ref, with ρ_ref the CFG476 convention (h = 0.7), unchanged with λ. Each model gives the ratio c_λ(M)/c_1(M). That ratio multiplies the Dutton–Macciò c(M) in CFG477's machinery.

**Held fixed with λ (declared assumption):** the SHMR (Moster+13), the DC14 core response, the galaxy sizes, the SPARC baryon curves and the noise. Basis: Barnes+18 and Salcido+18 report star-formation efficiency changing little for λ ≲ 10 (summariser reading, provisional). This is a limitation, not a result.

**Emergent a₀.** CFG477's code path, exec'd from source unedited: 200 realisations, seed 77 for every λ (common random numbers), and the same statistic (a₀ free, ν_mono).

**Also reported (analytic proxy):** g₋₂ = G M₋₂/r₋₂² at M = 10¹¹ and 10¹² M_⊙ (the halo's own acceleration scale, Navarro+17's mechanism), with its slope s_proxy.

## Verdict rule
Six estimator variants: {L16-crit, L16-m, D04} × {P, T}. s is taken from each variant's median a₀.

The ΛCDM classification:
- **COINCIDENCE-LIKE** if max |s| over variants ≤ 0.15. ΛCDM's scale does not track Λ, so a₀ ≈ c√(Gρ_Λ) would be a coincidence in ΛCDM.
- **TRACKS-Λ** if the primary variant has s ≥ 0.35 (ΛCDM would mimic the owner).
- **NOT DIAGNOSTIC** otherwise, including any case where the variants straddle 0.15–0.35.

The overall lane verdict:
- **TEST AVAILABLE** only if a published simulation with varied Λ measured a characteristic acceleration or rotation curves from which s can be read. The label above then attaches to that measurement.
- Otherwise **TEST NEEDS NEW SIMULATIONS**, with the analytic classification attached as provisional and a spec of the runs.
- **NONE** if neither the estimate nor a feasible simulation spec can separate the two predictions.

**Precision needed (to be reported):** the ln a₀ error per run that would separate s = 0.5 from the ΛCDM estimate at 3σ, using two runs at λ = 1 and λ = 10.

**Time domain (task 3), no new computation.** The observable version is a₀(z) at fixed Λ:
- The owner's picture predicts flat for w = −1 (√ρ_DE(z) for evolving DE).
- ΛCDM-feedback's drift is quoted from committed CFG565 (JSON) and from Mayer+23 (×≈3 by z = 2), with CFG566's caveat that existing high-z estimators do not reach the discriminating regime.

## Controls
- **K1:** at λ = 1 the machinery reproduces CFG477's median a₀ 9.686e-11 within 1% (same seed and code path).
- **K2:** D(a) for λ = 0 equals a (EdS) to 1e-4.
- **K3:** the concentration ratio is exactly 1 at λ = 1 for every model.
- **K4:** L16-crit at λ = 1 gives c(10¹² M_⊙) within a factor 1.5 of Dutton–Macciò (sanity of the σ(M) and normalisation).
- **K-null:** with λ held at 1 on every grid point, the estimator returns |s| < 1e-6.

## MUTATE (`--mutate`, separate outputs)
Replace the ΛCDM halo with the owner's law in the same mock: g_obs = ν_mono(g_bar/a₀(λ)) g_bar with a₀(λ) = 9.36e-11 √λ. The estimator must recover s within 0.45–0.55. It exits 1 when it does (bite detected).

This file is committed alone, before any script.
