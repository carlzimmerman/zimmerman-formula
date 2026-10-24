# X15_c1_preferred_frame: literature map (committed with FROZEN_CRITERIA.md, before any script or number)

**Every web look-up here is PROVISIONAL.** It was made on 2026-10-24 through a summarising web-fetch tool that returns a
model summary of the page, not verbatim text. Tags: **[abs]** arXiv abstract page; **[html]** full-text HTML (ar5iv) read
through the same tool; **[mem]** from memory, not looked up; **[rec]** already transcribed in this repository. Nothing was
downloaded.

| # | statement used | source | tag |
|---|---|---|---|
| L1 | Khronometric (healthy non-projectable Hořava) PPN, BPS Sec. 5.4, Eq. 91: α₁ = −4(α − 2β), α₂ = (α − 2β)(α − λ′ − 3β)/(2(λ′ + β)), both vanishing at α = 2β; λ′ = λ − 1 − β (Eq. 85); G_N = 1/(8πM_P′²(1 − α/2)) (Eq. 87); khronon speed c_χ² = (λ′ + β)/α to first non-trivial order (Eq. 86b). α is the a_ia^i coefficient, β enters through the effective metric g̃ = g − βuu (Eq. 79). The expressions are leading order in the small couplings. | Blas, Pujolàs & Sibiryakov 2011, JHEP 1104:018, arXiv:1007.3503 | [abs] + [html] (summary; the PPN section was reached at text offset 100000) |
| L1b | The exact khronometric α₁ = 4(α − 2β)/(β − 1) (as quoted by Bonetti & Barausse 2015); Einstein-aether at c₁₃ = 0: α₁ = −4c₁₄, α₂ = c₁₄(c₁₄ + 2c₂c₁₄ − c₂)/[c₂(2 − c₁₄)] (Oost, Mukohyama & Wang 2018) | `data_assembly/DOOR11_LITERATURE_2026-09-29.md` §1 | [rec] ([FT] there) |
| L2 | Standard PPN metric (Will): g_00 = −1 + 2U − 2βU² − 2ξΦ_W + (2γ + 2 + α₃ + ζ₁ − 2ξ)Φ₁ + … − (ζ₁ − 2ξ)𝒜 − (α₁ − α₂ − α₃)w²U − α₂w^iw^jU_ij + (2α₃ − α₁)w^iV_i; g_0i = −½(4γ + 3 + α₁ − α₂ + ζ₁ − 2ξ)V_i − ½(1 + α₂ − ζ₁ + 2ξ)W_i + (w-terms); g_ij = (1 + 2γU)δ_ij; χ_,0i = V_i − W_i, ∇²χ = −2U. For Lagrangian (semi-conservative) theories α₃ = ζ_i = 0; ξ = 0 for aether/khronon theories. GR: −(7/2)V_i − ½W_i. | Will, Theory and Experiment in Gravitational Physics; Living Rev. Relativ. 17 (2014) 4 | [mem]; validated in-lane by the GR control S0-4 |
| L3 | Bounds: \|α₁\| ≲ 1e-4 (LLR, weak field), \|α₂\| < 2.4e-7 (Nordtvedt 1987, solar spin vs planetary orbits), \|α̂₁\| < 2.1e-5 (Liu et al. 2020), −3.5e-5 < α̂₁ < 3.3e-5 (Shao & Wex 2012), \|α̂₂\| < 1.6e-9 (Shao et al. 2013); all CMB frame | DOOR11 §1 | [rec] |
| L4 | Gaseous dynamical friction for supersonic motion, F = 4π(GM)²ρ lnΛ/V² (Ostriker 1999, ApJ 513, 252); same order as Chandrasekhar's collisionless form in the highly supersonic limit | Ostriker 1999 | [mem], ESTIMATE use only |

**Matching limit for the cross-check.** v3s + C1 screened and linearised is khronometric with α_BPS → η(k) = 2/(M + γ_Lk²/K),
β_BPS = 0 (no K_ijK^ij term), λ′ = λ − 1 = β (the record's C1 coefficient; note the name clash: the record's β is BPS's
λ′, not BPS's β). In that limit L1 reads α₁ = −4η, α₂ = η(η − β)/(2β).
