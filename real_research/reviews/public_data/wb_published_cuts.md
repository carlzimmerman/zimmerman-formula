# Transcribed published cuts + mass pipelines (WB-R1 Step 1)

*From the papers via ar5iv. Citations to section/eq/table. ASYMMETRIC = present in one pipeline, not the other (fork candidates). TRANSCRIPTION-GAP = detail not recoverable from the fetch; substitute logged.*

## Chae 2023 (arXiv:2305.04613, ApJ 952 128)
**Cuts:** d<200 pc (main; 80 pc benchmark) [§2.1]; **4<M_G<14** both ("clean"; 12 "strict") [§2.1]; **relative PM errors <0.01** (or 0.005) per component, parallax rel. err <1% [§2.1]; **separation 0.2<s<30 kAU** [§2.1]; **|d_A−d_B|<3σ** [§2.1]; **chance-align ℛ<0.01** [§2.1]; MSMS. **Sample: 200 pc main = 26,615 pairs.**
**Mass:** Gaia G-band M_G + extinction (dustmaps, A_V=3.1E(B−V)); **Pecaut & Mamajek 2013** → G-band polynomial log₁₀(M/M☉)=Σaᵢ(M_G)ⁱ [Table 1, §2.2]. Hidden companions modelled probabilistically (self-calibrated f_multi) [§3.2]. *(TRANSCRIPTION-GAP: the Table-1 polynomial coefficients are not in the fetch → substitute a Pecaut–Mamajek-calibrated M_G→M; logged.)*
**v_N:** g=v²/r with **3D-DEPROJECTED** v (MC over inclination/phase/eccentricity, Hwang+2022) [§3.1, eq.8-9, 15]; g_N=GM_tot/r².

## Banik et al. 2024 (arXiv:2311.03436, MNRAS 527 4573)
**Cuts:** **|b|>15°**, **m_G<17**, **ϖ>4 mas (d<250 pc)** [§2.1]; astrometric χ²/ν≤1.2·max(1,exp[−0.2(m_G−19.5)]) [eq.4] *(GAP: needs astrometric_chi2; substitute RUWE<1.4)*; **separation 2<r_sky<30 kAU**; **v_sky<3 km/s** initially, **ṽ≤5** final [§2.4]; **|d_A−d_B|≤min(4σ_d,8 pc)** [§2.1]; **faint-companion/triple search to m_G<20**; **RV screen: ≥1 RV known, reject Δ(RV)>3σ or 3·v_c** (~3.5% loss) [§2.4.5]; **A_V<0.5** [§2.4.1]; MS only, no WDs; **ipd_frac_multi_peak≤2** [§2.4.3]; Error(ṽ)≤0.1·max(1,ṽ/2) [eq.10]; **total mass 0.464–4.31 M☉**. **Sample: 8,611 pairs** [§2.5].
**Mass:** G-band M_G; Pecaut & Mamajek → Gaia (Riello+2021); **cubic M_G=4.887−5.693x+0.4164x²+0.9611x³, x≡ln(M/M☉)**, 0.6<M_G<11.1 [eq.6]; FLAME correction; mass err 5.5% [§2.3.3].
**v_N:** **ṽ≡v_rel/√(GM/r_sky), SKY-PROJECTED only** (no 3D deprojection) [eq.3, §1.1]; systemic-RV perspective correction [§2.3.1].

## ASYMMETRIC cuts (the forks)
- **DEPROJECTION (F3, the big one):** Chae deprojects to 3D; Banik uses sky-projected ṽ. *Different observable.*
- **ṽ cap:** Banik caps ṽ≤5 (removes the extreme super-escape tail by construction); Chae has no such cap (models the tail).
- **Triple handling:** Banik *rejects* (faint-companion search + RV screen); Chae *models* hidden companions probabilistically.
- **Chance-align:** Chae ℛ<0.01; Banik uses χ²/ν + faint-companion search.
- **Mass relation:** different polynomials; different unresolved-binary handling.
