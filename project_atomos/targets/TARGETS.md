# TARGETS — sectors ranked by interlock-likelihood, and which targets are sharp enough to trust

Companion to `pdg_constants.py` (the machine-readable dataset, 71 targets with uncertainties) and the fuller
`SM_PARAMETERS.md`. This file does ONE job: tell the engine **where to aim** and **which targets are sharp enough that a
hit could mean anything** — ranked by the prior probability that a real forced-kernel / Koide-class interlock exists, not
by ease.

**The discipline (the whole project).** A formula that hits a number is worthless until it passes the three-part gate:
(A) FDR-survival vs the search-space size, (B) a forced kernel (a coefficient pinned by symmetry/geometry *before*
fitting), (C) an interlock (the same structure forces ≥2 independent observables, or ties ≥3 constants with one
parameter). Same bar both ways: do not manufacture a win, do not high-priest a real signal.

**Carl's #1 emphasis — uncertainties gate everything.** A 6-digit match to a 2-digit-known constant is noise. Every
target in `pdg_constants.py` carries `(value, sigma, rel_precision, n_digits_known)`; the engine scores **n-sigma
agreement**, and the FDR gate weights surplus bits by the *tolerance*, not the raw digit count. The `n_digits_known`
column is the hard cap on how deep a match can be physics rather than fitting. **Aim the search at PRECISE targets; never
fit a tight formula to a WEAK one and call it a hit.**

---

## Precision tiers (from the loaded dataset — the cap on any claim)

`precise_targets(1e-3)` = **25** targets with rel error < 1e-3 (good search targets).
`weak_targets(1e-3)` = **46** targets (quarantine for tight-fit claims).

**SHARP (rel err ≲ 1e-4 — a deep match is meaningful):**
`a_e` (1.1e-10), `alpha_em_inv_0` (1.5e-10), `m_e` (2.9e-10), `m_p`/`r_p_e` (3e-10/4e-10), `m_n`, `m_mu`/`r_mu_e`
(2.2e-8), `a_mu` (1.9e-7), `G_F` (5e-7), `tau_mu` (1e-6), `v_higgs` (2.4e-6), `koide_theta_lep` (6.5e-6),
`koide_Q_lep` (1e-5), `m_Z` (2.2e-5), `m_tau`/`r_tau_*` (6.8e-5).

**USABLE (1e-4 – 1e-3 — weight by sigma):** `alpha_em_inv_MZ`, `sin2_thetaW_MZ`, `m_W`, `tau_n`, `m_H`, `Gamma_Z`.

**WEAK — DO NOT over-fit (rel err ≳ 1e-2):** all light-quark masses & their ratios (`m_u` 23%, `m_d` 10%, `r_c_u` 23%,
`r_s_d` 10%, `sqrt_md_ms`), every CKM O(1) coefficient (`A`, `rhobar`, `etabar`, `J`, the small angles `theta13`,
`theta23`, `deltaCP`), the whole PMNS angle/splitting set (`sin2_12/23/13` at 2.5–4%, `theta*`, `Dm2_*`,
`r_Dm2_atm_sol`), `koide_Q_up`/`koide_Q_down`, `Gamma_H` (38%).

**BOUNDS, not measurements (engine cannot regress these — log only):** `theta_QCD` (<1e-10), `Sum_m_nu` (<0.12 eV),
`pmns_alpha21/31` (Majorana phases unknown). The NO/IO ordering ambiguity rides on the sign of `Dm2_31_NO` vs
`Dm2_32_IO`; both branches are carried.

> **The asymmetry to internalize.** The sharpest targets (leptons, α, g−2, m_p/m_e) are *single eigenvalues / overall
> scales* — exactly the numbers the honest prior says have **no forced kernel** (free Yukawa eigenvalues; QCD
> transmutation still needs a free y_e). The targets where an interlock is most *likely* (PMNS structure, the mixing
> patterns) are **weakly measured**. That tension — sharp-but-kernel-free vs structured-but-blurry — is the core
> difficulty, and the reason the engine's default hard filter is *interlock/symmetry*, not precision alone.

---

## RANKED HIT-LIST — where an interlock is most likely to be REAL

Ranked by: (a) is there an *already-FDR-surviving parameter-free* relation? (b) is the structure *symmetry-forced*
(discrete group / GUT embedding) rather than a free eigenvalue? (c) does it *interlock* across ≥2 observables/sectors?
Precision noted because it caps the achievable claim.

| # | Sector / target | Why high (mechanism hook) | Sharpness | Gate status |
|---|---|---|---|---|
| **1** | **Koide Q=2/3 (charged leptons)** `koide_Q_lep`, `koide_theta_lep` | The ONE proven, FDR-surviving, parameter-free interlock in the whole SM (~1-in-44k random-triple null; 45-yr puzzle). Ties 3 masses, 0 free params; √-mass vector at 45° to (1,1,1). | **SHARP** (Q rel 1e-5; tau-limited, Q−2/3 ≈ 0.9σ) | **Calibration positive.** Must re-find + re-certify (A via triple-null, C2). Open knob: can a flavor symmetry force r=√2 where the gravity spine provably cannot? B-gap honestly flagged. |
| **2** | **PMNS structure: TBM + A₄/S₄/Δ(27), θ₁₃≈8.5° as breaking** `pmns_sin2_12/23/13` | Most symmetry-forced sector. `sin²θ₁₂≈1/3` and `θ₂₃≈45°` are forced-pattern values; θ₁₃ is the structured breaking. Discrete-group/geometric hypotheses are tailor-made here (the charter's "probably geometric" instinct). | WEAK (2.5–4% rel) | **Highest prior among unsolved.** Engine's GROUP_INVARIANTS pool (A4/S4/Δ27) is the hard filter; sharpness caps claims — a "1/3" hit must clear the FDR null at the 4% tolerance. |
| **3** | **GST mass-mixing: √(m_d/m_s) ≈ \|V_us\|** `sqrt_md_ms` vs `ckm_lambda` | Clean mass↔mixing interlock, no free parameter — the quark-sector analogue of Koide. (Dataset: √(m_d/m_s)=0.224 vs λ=0.225.) | WEAK (light-quark 5% on √-ratio) | **Testable now.** Tantalizing central agreement but the m_d/m_s error is the killer — gate must report whether 0.224≈0.225 survives the FDR null *at the 5% tolerance* (likely "consistent, low-bits"). |
| **4** | **Cross-sector: θ_C+θ₁₂^PMNS≈45° AND θ₁₃^PMNS≈θ_C/√2** `qlc_sum`, `pmns_sin_t13` | Cross-sector interlocks (the gate's strongest class): tie CKM↔PMNS ⇒ a GUT-scale forced kernel. (Dataset: sum=46.4°±0.8; sinθ₁₃=0.148 vs λ/√2=0.159, ~7%.) | WEAK (PMNS-limited) | **Worth extra budget** (cross-sector is hardest to fake). 46.4° is ~1.9σ from 45°; the θ₁₃ coincidence is ~7% off — gate decides coincidence vs structure. |
| **5** | **Gauge unification + sin²θ_W=3/8 (GUT)** `sin2_thetaW_MZ`, `alpha_em_inv_MZ`, `alpha_s_MZ` | 3 couplings nearly meet at high scale ⇒ not independent; SU(5) tree `sin²θ_W=3/8` is genuinely *forced by the embedding* (runs down to 0.231). Forced-kernel-via-β-function class. | sin²θ_W SHARP-ish (1.3e-4); α_s WEAK (8e-3) | **Real forced kernel at the GUT scale**, but the interlock lives in the *running* (needs the β-functions, not a static number-match). The static `3/13` fit is FDR-dead — do not resurrect. |
| **6** | **Georgi-Jarlskog GUT mass relations** (m_b=m_τ; m_μ≈3m_s; m_e≈m_d/3 at GUT) `r_b_tau` | Group-theory-*forced* Yukawa textures that *work* to 10–20% after running — a real forced-kernel candidate in the otherwise kernel-free mass sector. (Dataset: m_b/m_τ=2.35 at low scale → ≈1 at GUT.) | `r_b_tau` MEDIUM; m_μ/m_s, m_e/m_d light-quark-WEAK | **Real candidate**, but the test requires RGE running to the GUT scale (not a low-scale number-match) — the gate's forced-kernel provenance must cite the SU(5)/SO(10) Clebsch, not a fitted integer. |
| **7** | **Wolfenstein/CKM hierarchy as powers of λ** `ckm_lambda`, `ckm_A`, `ckm_rhobar`, `ckm_etabar` | `\|V_ij\|` ≈ powers of λ≈0.225 (V_us~λ, V_cb~λ², V_ub~λ³) is structured — Froggatt-Nielsen signature. But the O(1) coefficients A, ρ̄, η̄ look fitted, and FN charges are themselves free. | λ SHARP (3e-3); A/ρ̄/η̄ WEAK | **Medium prior.** The power-law *structure* is real; the *numbers* on top are FDR-suspect. Gate likely: structure survives, coefficients baked. |
| **8** | **Charged-lepton & quark mass hierarchies (raw Yukawa eigenvalues)** `r_mu_e`, `r_tau_mu`, `r_t_b`, … | The proven-hard sector: free Yukawa eigenvalues, **no forced kernel** (164 FDR-dead re-labelings: 4Z²+3, 64π+Z, 6π⁵…). | r_mu_e, r_p_e SHARP | **Calibration NEGATIVE.** Engine MUST report these FDR-dead honestly (the m_μ/m_e, m_τ/m_μ pool comes back BAKED-dense). Sharpness here is a *trap* — a deep match means nothing without a kernel. |
| **9** | **Higgs v, m_H, λ (single scales)** `v_higgs`, `m_H`, `higgs_lambda` | Scales not ratios; weak interlock prior unless tied to Λ (already owned by a₀). λ≈0.129 has near-criticality arguments but that's a dynamical hint, not a forced number. | SHARP (v 2.4e-6; λ 1.8e-3) | **Low prior.** A kernel on a single dimensionful scale is weak; the *ratios* (which v divides out) are where any physics lives, and those are sectors 1–8. |
| **10** | **θ_QCD ≈ 0** `theta_QCD` | The puzzle is *why ~0* (PQ/axion, Nelson-Barr) — a symmetry-selection target, not a number to regress. | BOUND (<1e-10) | **Outside the search engine's reach.** Logged; a "kernel forcing exactly 0" is the cleanest possible forced kernel but it's a symmetry argument, not a number-match. Deprioritized for the engine. |

---

## Operating rules for the engine/gate (carried from SM_PARAMETERS.md + ENGINE_REVERSE_ENGINEERING.md)

1. **Anonymize before search.** Feed the engine the *dimensionless* targets (the 33-entry `dimensionless()` pool —
   ratios, couplings, sin² values, Q, J) with names stripped, exactly as a₀ was found over anonymized cosmological
   constants. Use `PDGDataset.dimensionless()`.
2. **Within-sector ratios first.** The overall scale (v, or any one mass) is a free dial; the *ratios* are the physics.
   Hunt `r_*`, the Koide invariants, the PMNS `sin²`, the CKM angles — never dimensionful masses directly.
3. **Score by n-sigma, not digits.** `Target.within(candidate, k)` and `Target.n_sigma_of(candidate)` are the hit
   predicates. The FDR gate's tolerance for each target = its `rel_precision` (a hit must land inside the error bar; a
   6-digit landing on a 2-digit target is logged as fitting, not a match).
4. **Calibration must pass first.** Re-find a₀'s √(8π/3) and Koide Q=2/3; reject the 164 FDR-dead re-labelings and the
   raw mass-ratio pool (BAKED-dense). No new lead is trusted until the machine reproduces the one real positive and
   rejects the known negatives.
5. **Cross-sector interlocks are the jackpot** (#3, #4) — an interlock spanning two sectors is the hardest thing to fake
   and the strongest possible certificate. Extra search budget there.
6. **Width gates the claim.** For every WEAK target (light quarks, PMNS, CKM coefficients), the strength of any reported
   hit is capped by `n_digits_known`. The gate must refuse to certify a relation whose precision exceeds the target's.

*Provenance: PDG-2024 / CODATA-2018-22 / NuFIT-5.2-class values (assistant cutoff Jan 2026); discipline from
zimmerman-formula real_research/reviews + opus_48_extended_research/reviews/koide_dsunruh. Same bar both ways.*
