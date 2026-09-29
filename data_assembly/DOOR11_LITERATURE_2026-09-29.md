# Door 11 literature: preferred-frame limits, flowing-vacuum and aether MOND, moving dark energy (2026-09-29)

For the gates file `campaign_fresh_gravity/closure_map/DOOR11_FLOWING_VACUUM_GATES_2026-09-29.md`, items 1-9 of the literature request. Read-only work. Nothing was downloaded, nobody was contacted, and no gate is scored here. A separate, independent abstract-level pass exists in `data_assembly/DOOR11_LITERATURE_DATAFRONT_2026-09-29.md`; the cross-check is at the end.

**Tags (every claim carries one).**
- **[FT]** full text read: the arXiv HTML or ar5iv rendering of the whole paper was fetched and queried. The fetch tool returns a model summary of the page, not the raw page, so equations and numbers tagged [FT] are what that summary returned. Where a long page was truncated, this is said.
- **[ABS]** only the arXiv abstract page (or journal abstract page) was read.
- **[SR]** only a search-engine excerpt was seen; the page was not opened. Treat as **UNVERIFIED**.
- **UNVERIFIED** not read at all (named from a secondary citation).
- **[INF]** a calculation or inference made in this file, not a published statement.

---

## Bottom line

1. **G6 numbers.** |α̂₂| < 1.6 × 10⁻⁹ (95% CL) is confirmed from its source. The α̂₁ number is really the 95% interval −3.5 × 10⁻⁵ < α̂₁ < +3.3 × 10⁻⁵, so "3.4 × 10⁻⁵" is a symmetrised rounding: quote the interval, or 3.5 × 10⁻⁵ to be conservative. A tighter bound, |α̂₁| < 2.1 × 10⁻⁵ (95% CL, PSR J1909−3744, 2020), now exists. Both are **strong-field (hatted) pulsar parameters**, and both assume the **CMB frame** as the preferred frame (w ≈ 369 km/s). The weak-field limits are looser: α₁ = (−0.7 ± 1.8) × 10⁻⁴ (95%, lunar laser ranging) and |α₂| < 2.4 × 10⁻⁷ (solar spin alignment; secondary citation only).
2. **No published MOND-like theory with a spatial, one-direction vacuum flow was found.** Every flow or aether MOND construction found uses a **timelike** vector or foliation. The list is generalized Einstein-aether, khronon MOND, MOND-khronometric, AeST, relativistic khronon, and Zhao's vector-for-Λ model. These are all the 11C "flow along time" reading. 11B′ has no published relative.
3. **A pure Λ cannot flow by itself.** T_μν = −ρ_vac g_μν is the only Lorentz-invariant vacuum stress tensor, so a cosmological constant has no rest frame. A flow needs an extra field: an aether, a khronon, a three-form with a potential, or a fluid with w ≠ −1. The momentum density (ρ+p)v of such a fluid vanishes as w → −1.
   - In Henneaux-Teitelboim unimodular gravity, the three-form conjugate to Λ is locally pure gauge. Only the global four-volume ("cosmic time") is physical.
   - In unimodular gravity with energy non-conservation, any energy current into the vacuum must be a gradient (dJ = 0). It therefore appears as a spatial variation of Λ.
4. **Directional a₀ (G8).** The only direct published tests come from one group using SPARC. They **claim** a 25-37% dipole in a₀; the result is unreplicated and the authors themselves call it premature. It cannot serve as an upper bound.
   - A usable proxy exists. The CosmicFlows-4 Tully-Fisher zero-point dipole is 0.063 ± 0.016 mag, and a second team attributes it to local flows or systematics.
   - Converted [INF], this bounds a direction-dependent a₀ to a dipole amplitude ≈ 6% (≲ 9% at ~2σ). The claimed 25-37% a₀ dipole would appear as a 0.25-0.4 mag TF dipole, which CF4 does not show.
5. **G7.** No published test was found of a₀ (or of BTFR/RAR residuals) against a galaxy's speed relative to the CMB or any flow frame. The MOND-khronometric paper leaves the galaxy's motion relative to the foliation undiscussed. This test is open, not closed.

---

## 1. Preferred-frame PPN limits (G6)

| parameter | value (CL) | regime / frame | system | source | read |
|---|---|---|---|---|---|
| α̂₁ | −0.4 (+3.7, −3.1) × 10⁻⁵ (95%), i.e. −3.5 × 10⁻⁵ < α̂₁ < +3.3 × 10⁻⁵ | strong field; CMB frame, binary moving at w ≈ 369 km/s | PSR J1738+0333 (orbital-plane precession about the velocity, via ẋ) | Shao & Wex 2012, CQG 29, 215018, https://arxiv.org/abs/1209.4503 | [ABS] + [FT] https://ar5iv.labs.arxiv.org/html/1209.4503 |
| α̂₁ | < 2.1 × 10⁻⁵ (95%) (the abstract writes "α₁") | strong field | PSR J1909−3744, 15 yr timing | Liu et al. 2020, MNRAS 499, 2276, https://arxiv.org/abs/2009.12544 | [ABS]. A 2025 SKA-era review quotes it as 2.0 × 10⁻⁵ (https://arxiv.org/html/2512.16161v1 [FT]); use the abstract's 2.1 |
| α̂₂ | < 1.8 × 10⁻⁴ (95%) | strong field; CMB frame | PSRs J1012+5307 and J1738+0333 | Shao & Wex 2012 (above) | [ABS] + [FT] |
| α̂₂ | **< 1.6 × 10⁻⁹ (95%)** | strong field; CMB frame, \|w_SSB\| = 369.0 ± 0.9 km/s | solitary MSPs B1937+21 and J1744−1134; ~15 yr of Effelsberg pulse profiles show no spin precession | Shao, Caballero, Kramer, Wex, Champion & Jessner 2013, CQG 30, 165019, https://arxiv.org/abs/1307.2552 | [ABS] + [FT] https://ar5iv.labs.arxiv.org/html/1307.2552 |
| α₁ | (−7 ± 9) × 10⁻⁵ ("realistic" errors) | weak field | lunar laser ranging | Müller, Williams, Turyshev & Shelus 2005, https://arxiv.org/html/gr-qc/0509019v1 | [FT] |
| α₁ | (−0.7 ± 1.8) × 10⁻⁴ (95%) | weak field | LLR | as cited inside Shao & Wex 2012 [FT]; the original Müller et al. 2008 chapter is UNVERIFIED | secondary |
| α₂ | (1.8 ± 2.5) × 10⁻⁵ | weak field | LLR | Müller et al. 2005 (above) | [FT] |
| α₂ | < 2.4 × 10⁻⁷ | weak field | Sun's spin axis vs the planetary angular momentum over ~5 Gyr (Nordtvedt 1987, ApJ 320, 871) | cited inside Shao & Wex 2012 and Shao et al. 2013 [FT]; Nordtvedt 1987 itself UNVERIFIED | secondary |
| α₁, α₂ | ≤ 6 × 10⁻⁶, ≤ 3.5 × 10⁻⁵ | weak field | planetary perihelion precessions | Iorio 2014, IJMPD 23, 1450006, https://arxiv.org/abs/1210.3026 | [ABS]. Single author, and not the value adopted by the analyses read below; treat as contested |

**Notes on scope.**
- **Strong field vs weak field.** The pulsar (hatted) parameters are the strong-field counterparts of α₁ and α₂. Shao & Wex say the two can differ significantly, for example through scalarization of neutron stars [FT]. Shao et al. 2013 say α₂ and α̂₂ probe different aspects of local Lorentz invariance [FT].
- **Frame.** Both pulsar papers take the CMB frame as the preferred frame [FT].
  - Shao & Wex 2012 also derive limits for a frame at rest in the Galaxy and for frames co-moving with Galactic rotation [ABS]. Those numbers sit in a section the fetch truncated, so they are **UNVERIFIED**.
  - Shao et al. 2013 say the generalisation to other frames is straightforward but do not give it [FT].
- **The α̂₂ bound is probabilistic.** It assumes a uniform unknown spin azimuth and a Gaussian radial velocity (σ = 100 km/s), with 10⁸ Monte Carlo trials [FT].
- **How other analyses map these limits onto theories.**
  - Einstein-aether after GW170817: Oost, Mukohyama & Wang 2018 adopt the weak-field bounds |α₁| ≤ 10⁻⁴ and |α₂| ≤ 10⁻⁷ [FT https://ar5iv.labs.arxiv.org/html/1802.04303]. With c₁₃ ≈ 0, α₁ = −4c₁₄, giving 0 < c₁₄ ≤ 2.5 × 10⁻⁵ and 0 < c₂ ≲ 0.095. α₂ ≈ c₁₄(c₁₄ + 2c₂c₁₄ − c₂)/[c₂(2 − c₁₄)] [FT].
  - MOND-khronometric: Bonetti & Barausse 2015 adopt |α₁| ≲ 10⁻⁴ and |α₂| ≲ 10⁻⁷. The khronometric α₁ = 4(α − 2β)/(β − 1), which forces α ≈ 2β [FT https://ar5iv.labs.arxiv.org/html/1502.05554].
- **2026 pulsar update.** Vaglio et al. (https://arxiv.org/abs/2605.01436) [ABS] use EPTA + NANOGrav timing of J1738+0333 to give the tightest single-system strong-field Einstein-aether bounds so far. Their numbers are not in the abstract.
- **Scale [INF].** (369.82 km/s / c)² = 1.5 × 10⁻⁶ and (600 km/s / c)² = 4.0 × 10⁻⁶.
  - Solar dipole: v = 369.82 ± 0.11 km/s toward (l, b) = (264.021°, 48.253°). Source: Planck 2018 I, [SR] https://www.aanda.org/articles/aa/full_html/2020/09/aa33880-18/aa33880-18.html. The page returned 403, so this is UNVERIFIED beyond the excerpt.
  - Shao et al. 2013 use 369.0 ± 0.9 km/s [FT].

---

## 2. Directional anisotropy of rotation curves, RAR or BTFR (G7, G8)

**The direct tests (one group, one data set).**
- **Zhou, Zhao & Chang 2017**, ApJ 847, 86, https://arxiv.org/abs/1707.00417 [ABS + FT https://arxiv.org/html/1707.00417].
  - Method: hemisphere comparison of the RAR acceleration scale g† across 147 SPARC galaxies (2693 points), fitted by orthogonal-distance regression in each hemisphere.
  - Result: maximum 1.10 × 10⁻¹⁰ m s⁻² toward (l, b) = (175.5°, −6.5°) and minimum 0.76 × 10⁻¹⁰ in the opposite direction. The anisotropy D = 2(g_up − g_down)/(g_up + g_down) = 0.37 ± 0.04.
  - Controls: 100 isotropic mocks gave 0.05 ± 0.02 (largest 0.10 ± 0.03).
  - Caveats the authors state: M/L is fixed across SPARC, the data points cluster in one sky direction, and better sky coverage is needed. Distance and inclination errors are not discussed in the text read.
- **Chang, Lin, Zhao & Zhou 2018**, Chin. Phys. C 42, 115103, https://arxiv.org/abs/1803.08344 [ABS].
  - A monopole + dipole fit to the RAR. The monopole is negligible; the dipole is 0.25 ± 0.04 toward (171.30° ± 7.18°, −15.41° ± 4.87°).
  - The authors say it is premature to claim an anisotropic universe.
- **Geometry [INF].** The Zhou direction is 94° from the CMB dipole (264.0°, 48.3°) and the Chang direction is 103°: roughly perpendicular. Both are ~65° from the CF4 TF dipole below.
- **Replication.** None found. No published test of RAR/BTFR residuals against the CMB-dipole direction, or against galaxy peculiar velocity, was found (searches are listed at the end).

**Proxy bound: the Tully-Fisher zero-point dipole.**
- **Boubel, Colless, Said & Staveley-Smith 2024/25**, https://arxiv.org/abs/2412.14607 [ABS].
  - CF4 TF distances give a dipole of 0.063 ± 0.016 mag toward (142° ± 30°, 52° ± 10°), equivalent to ΔH₀ = 2.10 ± 0.53 km/s/Mpc (3%) at 3.9σ.
  - This model is only marginally preferred over constant H₀ plus a ΛCDM-consistent bulk flow.
  - Forecast: WALLABY + DESI should detect a 1% dipole at 5.8σ.
- **Stiskalek, Desmond & Lavaux 2025/26**, MNRAS, https://arxiv.org/abs/2509.14997 [ABS]. They find a ~4% dipole in the CF4 zero point, but conclude the anisotropic zero-point model picks up local flow features or systematics, not a real bulk flow. No evidence for H₀ anisotropy.
- **Conversion [INF]** (not in either paper).
  - V_flat⁴ = G M_b a₀, so at fixed V, L ∝ 1/a₀.
  - A direction-dependent a₀ = a₀(1 + ε cos θ) therefore shifts the TF distance modulus by Δμ ≈ 2.5 log₁₀(1 + ε) ≈ 1.086 ε mag, constant with distance. That is the same signature as the fitted "H₀ dipole" / anisotropic zero point.
  - Sign: higher a₀ makes galaxies look more distant, so apparent H₀ is lower. Check: ΔH₀/H₀ ≈ 0.46 Δμ, so 0.063 mag gives 2.9%, matching the quoted 3%.
  - Result: ε ≈ 0.060 ± 0.015, or ≲ 0.09 at ~2σ. The Zhou/Chang ε = 0.25-0.37 would be a 0.25-0.4 mag dipole.
  - Caveats: CF4 uses the luminosity TF relation, not the baryonic one; gas-fraction scatter dilutes the mapping; the effect is assumed to sit in V_flat.

**Adjacent tests (not a sky direction).**
- **Environment.** Chae, Lelli, Desmond, McGaugh, Li & Schombert 2020, ApJ 904, 51, https://arxiv.org/abs/2009.11525 [ABS]. The external-field effect is detected at >4σ in 153 SPARC galaxies (8-11σ in the most strongly perturbed ones), with fitted fields in line with environment.
- **Solar-System anisotropic tide.** Hees, Folkner, Jacobson & Park 2014, PRD 89, 102002, https://arxiv.org/abs/1402.6950 [ABS]: Q₂ = (3 ± 3) × 10⁻²⁷ s⁻² from Cassini tracking. [INF] A uniform streaming acceleration is unobservable inside a freely falling system; only its gradient (quadrupole) is, and Q₂ bounds exactly that.
- **Oort cloud.** Vokrouhlický, Nesvorný & Tremaine 2024, ApJ 968, 47, https://arxiv.org/abs/2403.09555 [ABS]. AQUAL MOND fails the long-period-comet binding-energy distribution, and (for gradual transition functions) the detached-disk TNOs. Screened MOND theories are not excluded.
- **Cosmic-dipole context.** Secrest et al. 2021, ApJL 908, L51, https://arxiv.org/abs/2009.14826 [ABS]. The WISE quasar dipole is aligned with the CMB dipole but has twice the kinematic amplitude (4.9σ). This is the best-known published "one direction" anomaly; it is not a gravity test.

---

## 3. The river model and MOND from flowing space

- **Hamilton & Lisle 2008**, Am. J. Phys. 76, 519, https://arxiv.org/abs/gr-qc/0411060 [ABS].
  - Space falls into a spherical black hole at the Newtonian escape velocity and reaches c at the horizon.
  - The picture extends to Kerr-Newman. There the river has no azimuthal swirl, but each point carries a velocity plus a Lorentz "twist" (six numbers).
  - The abstract presents it as a way to conceptualise stationary GR black holes. It is a re-description of GR (Painlevé-Gullstrand-type coordinates/tetrads), not new dynamics.
- **Braeck & Grøn 2013**, Eur. Phys. J. Plus, https://arxiv.org/abs/1204.0419 [ABS]. Space flows toward the singularity in Schwarzschild and outward to infinity in de Sitter.
  - [INF] The Λ-vacuum's own river is therefore an **outflow**, v = r√(Λc²/3). This is consistent with the gates' v² = 2GM/r + Λc²r²/3 for 11A.
- **Cahill's "dynamical 3-space".** This is the closest published "flowing space replaces dark matter" programme. It is outside mainstream journals (the Apeiron volume and Progress in Physics).
  - Sources: May & Cahill 2010, https://arxiv.org/html/1009.5770 [FT]; Cahill 2011, https://arxiv.org/abs/1102.3222 [ABS].
  - Flow law: ∇·(∂_t v + (v·∇)v) + (α/8)[(tr D)² − tr(D²)] = −4πGρ, where D is the strain rate and α ≈ 1/137.
  - Effective dark density: ρ_DM(r) = (α/2) r^(−2−α/2) ∫_r^R s^(1+α/2) ρ(s) ds.
  - It claims an absolute flow of more than 300 km/s, detected through light-speed anisotropy [FT]. The specific 430-490 km/s toward RA ≈ 4-5 h, Dec ≈ −67° to −75° come only from search excerpts of other Cahill papers (UNVERIFIED).
  - [INF] With a dimensionless α, the extra mass is ∝ α × the baryon mass. So v² ∝ M asymptotically (BTFR slope 2, not 4), and there is no acceleration scale. The ten-door result applies: a missing object must carry an acceleration scale.
  - Laboratory light-speed isotropy is Δc/c ~ 1 × 10⁻¹⁷ (Herrmann et al. 2009, PRD 80, 105011, https://arxiv.org/abs/1002.1284 [ABS]). A few-hundred-km/s ether drift would have (v/c)² ~ 10⁻⁶ [INF].
- **Superfluid vacuum.** Zloshchastiev 2023, Pramana 97, 2, https://arxiv.org/abs/2310.06861 [ABS + FT https://arxiv.org/html/2310.06861].
  - A logarithmic superfluid vacuum gives log, linear and quadratic potential terms.
  - 15 THINGS galaxies are fitted with six free parameters each; the linear and quadratic terms are galaxy-specific.
  - No BTFR and no universal a₀. The vacuum is assumed stationary; there is no flow.
- **"Mezzi effect"** (Benaissa; the vacuum as a radially infalling compliant medium). Search excerpt only, UNVERIFIED.
- **Result.** Outside the covariant vector/foliation theories of items 4, 5 and 9, no MOND-from-flowing-space proposal was found that has a universal a₀ tied to Λ and a stated test.

---

## 4. Generalized Einstein-aether MOND (Zlosnik, Ferreira & Starkman 2007) and its later status

**The original theory.** Zlosnik, Ferreira & Starkman 2007, PRD 75, 044017, https://arxiv.org/abs/astro-ph/0607411 [ABS + FT https://ar5iv.labs.arxiv.org/html/astro-ph/0607411].
- The field is a unit timelike vector A, with A·A = −1 imposed by a Lagrange multiplier. The Lagrangian is ∝ M² F(K), with K = M⁻² K^{αβ}_{γσ} ∇_α A^γ ∇_β A^σ (couplings c₁, c₂, c₃).
- The background aether is A^μ = δ^μ₀, aligned with cosmic time.
- Non-relativistic limit: ∇·[(2 + c₁F′)∇Φ] = 8πGρ. This gives MOND for F ≈ αK + βK^{3/2} at small K. The mass scale M is identified with a₀, and a₀ ≈ cH₀ is noted.
- Caveats in the paper itself:
  - K > 0 in quasi-static systems but K < 0 in cosmology, so the two regimes use different branches of F.
  - Perturbations through the Silk-damping era are unclear.
  - Solar-System constraints and nonlinear stability are left open.

**Solar System.** Bonvin, Durrer, Ferreira, Starkman & Zlosnik 2008, PRD 77, 024037, https://arxiv.org/abs/0707.3519 [ABS + FT ar5iv]. A subclass passes the Mercury perihelion and Cassini time-delay tests. Velocity-dependent (preferred-frame) effects were deferred; α₁ and α₂ were not computed.

**Stability.** Carroll, Dulaney, Gresham & Tam 2009, PRD 79, 065011, https://arxiv.org/abs/0812.1049 [ABS].
- A fixed-norm aether with generic kinetic terms has ghosts or tachyons.
- Only the sigma-model term (with the norm fixed by a constraint), the Maxwell term and (∂·A)² are not manifestly unstable.
- The abstract does not treat F(K) generalizations, so its bearing on this theory is UNVERIFIED here.

**Cosmology.**
- Zuntz, Zlosnik, Bourliot, Ferreira & Starkman 2010, PRD 81, 104015, https://arxiv.org/abs/1002.0849 [ABS]. The dark-matter-candidate regime fails CMB + LSS; the dark-energy regime fits.
- Trinh, Pace, Battye & Bolliet 2019, PRD 99, 043515, https://arxiv.org/abs/1811.07805 [ABS]. w = −1 models agree with ΛCDM on Planck; otherwise w_de = −1.06 (+0.08, −0.03) (CMB). The lensing amplitude stays ~2σ high.
- Carroll & Lim 2004, PRD 70, 123525, https://arxiv.org/abs/hep-th/0407149 [ABS]. A timelike aether rescales G by different factors in cosmology and in the Newtonian limit; BBN bounds the vector norm.

**Gravitational waves (GW170817).**
- The bound itself: LVC + Fermi + INTEGRAL 2017, ApJL 848, L13, https://arxiv.org/abs/1710.05834 [ABS]: −3 × 10⁻¹⁵ < (c_GW − c)/c < +7 × 10⁻¹⁶.
- Einstein-aether: Oost et al. 2018, PRD 97, 124023, https://arxiv.org/abs/1802.04303 [ABS + FT] give |c₁₃| ≲ 10⁻¹⁵, with the c₁₄ and c₂ limits in item 1.
- Pulsars: Gupta et al. 2021, CQG 38, 195003, https://arxiv.org/abs/2104.04596 [ABS] tighten the remaining space by about 10×.
- Chesler & Loeb 2017, PRL 119, 031102, https://arxiv.org/abs/1704.05116 [ABS]. They argue generalized Einstein-aether and BIMOND are fatally inconsistent with UHECR and LIGO; the mechanism is not in the abstract.
- Hou & Gong 2018, Universe 4, 84, https://arxiv.org/abs/1806.02564 [ABS]. Einstein-aether has five polarizations and generalized TeVeS six; the GW170817 bound forces a superluminal mode in generalized TeVeS. The Zlosnik-Ferreira-Starkman model is not addressed.
- Boran, Desai, Kahya & Woodard 2018, PRD 97, 041501, https://arxiv.org/abs/1710.06168 [ABS]. Theories where matter and GWs couple to different metrics ("dark matter emulators") predict a ~400-day Shapiro-delay difference against the observed 1.7 s. This hits two-metric (TeVeS-type) theories. Whether it applies to a single-metric aether is not stated.

**Successors.**
- Skordis & Zlosnik 2019, PRD 100, 104013, https://arxiv.org/abs/1905.09465 [ABS]: a TeVeS class with c_T = c exists.
- AeST: Skordis & Zlosnik 2021, PRL 127, 161302, https://arxiv.org/abs/2007.00082 [ABS]. MOND in galaxies, fits the CMB and linear P(k), ghost-free at second order.
- AeST linear stability, PRD 106, 104041, https://arxiv.org/abs/2109.13287 [ABS]. A non-propagating mode has an unbounded Hamiltonian for k < μ, with μ ≲ Mpc⁻¹.
- AeST Hamiltonian analysis, PRD 110, 044015, https://arxiv.org/abs/2307.15126 [SR]: six degrees of freedom.

---

## 5. Directional vacuum/aether flow giving MOND-like gravity, with tests

- **Blanchet & Marsat 2011**, PRD 84, 044056, https://arxiv.org/abs/1107.5264 [ABS]. The "khronon" defines a preferred time foliation, so the aether is hypersurface-orthogonal (the flow is the unit normal to the foliation). The model is heuristic. It recovers MOND in the non-relativistic limit and gives GR lensing with a modified Poisson-type potential.
- **Sanders 2011**, PRD 84, 084024, https://arxiv.org/abs/1105.3910 [ABS]. A modified low-energy limit of non-projectable Hořava gravity hides the preferred frame wherever the Newtonian field gradient exceeds cH₀. MOND appears below that.
- **Bonetti & Barausse 2015**, PRD 91, 084053 (erratum PRD 93, 029901), https://arxiv.org/abs/1502.05554 [ABS + FT ar5iv].
  - MOND-khronometric: MOND comes from terms in the acceleration of the foliation's normal congruence.
  - If the theory is forced to be exactly GR at high acceleration, the post-Newtonian expansion breaks down at low acceleration.
  - A sizeable parameter region stays perturbative, passes Solar-System and pulsar tests, and gives MOND rotation curves. This wording is from the search summary of the abstract, and the full text matches it.
  - There is a strong-coupling threshold on |λ + β|.
  - The galaxy's motion relative to the foliation is not discussed [FT].
- **Blanchet & Skordis 2024**, JCAP 11 (2024) 040, https://arxiv.org/abs/2404.06584 [ABS]. A relativistic khronon theory: MOND for stationary systems, GR + Λ in strong fields, and agreement with the CMB. The Hamiltonian is bounded for k ≳ 10⁻³¹ eV and unbounded below that. A Moriond summary is https://arxiv.org/abs/2507.00912 [ABS].
- **Sanders 2006**, MNRAS 370, 1519, https://arxiv.org/abs/astro-ph/0602161 [ABS]. Multi-field MOND can pass the inner Solar System and show no ether drift, but it then predicts an anomalous non-inverse-square force in the outer Solar System.
- **Zhao 2007** (vector-for-Λ): see item 9.
- **Li & Chang 2013**, CPC, https://arxiv.org/abs/1204.2542 [ABS]. Finslerian MOND with the Tully-Fisher relation and Lorentz violation. arXiv carries an admin note about substantial text overlap.
- **Ghaffarnejad & Dehghani 2019**, EPJC, https://arxiv.org/abs/1906.01052 [SR only, UNVERIFIED]. A timelike vector as the preferred frame's four-velocity in a Brans-Dicke scalar-vector-tensor theory, checked against the BTFR of 12 galaxies.
- **Result.** No published model was found in which a **spacelike**, one-direction vacuum flow produces MOND. All found models use a timelike vector or foliation. Their tests are PPN α₁/α₂, pulsars, GW speed, and CMB/P(k).

---

## 6. Henneaux-Teitelboim unimodular gravity (Λ dual to a four-form; the conjugate three-form)

- **The original paper.** Henneaux & Teitelboim 1989, Phys. Lett. B 222, 195. The journal page returned 403, so it is **UNVERIFIED**. A search excerpt [SR] (https://www.osti.gov/etdeweb/biblio/5893018, https://ui.adsabs.harvard.edu/abs/1989PhLB..222..195H) says Λ appears as a constant of integration.
- **The content, from a full-text secondary source.** Albertini, Barnes & Herczeg 2023, PRD 108, 024031, https://arxiv.org/html/2303.12842 [FT].
  - Action: S_HT = (1/κ)∫Vol(g)[½R(g) − φ + κL_M] + ∫φ dH. Here φ plays Λ and H is a three-form.
  - Varying φ gives Vol(g) = dH. Varying H gives dφ = 0, so Λ is a constant of integration, not a coupling.
  - Gauge: H → H + dΩ for any two-form Ω. **Only the integrated spacetime volume is physical.** That is the global "cosmic (unimodular) time" conjugate to Λ. The equivalent vector-density form is ∂_μT^μ = √−g.
  - Answer to the item's question: the three-form's local configuration is gauge; the global value of Λ and its conjugate four-volume are physical; there are no local degrees of freedom.
  - The dynamical generalization adds −α∫dH∧*dH − β∫dφ∧*dφ. φ then fluctuates, sourced by non-conserved stress-energy, with approximate de Sitter attractors. Perturbative stability is left for future work.
- **Four-form flux.** Bousso & Polchinski 2000, https://arxiv.org/abs/hep-th/0004134 [ABS; journal ref not read]. Four-form fluxes contribute to Λ with Dirac-quantised values. Λ changes only through membrane nucleation (the Brown-Teitelboim mechanism, whose 1987-88 papers are UNVERIFIED).
- **Unimodular gravity with energy non-conservation.** Josset, Perez & Sudarsky 2017, PRL 118, 021102, https://arxiv.org/abs/1604.04183 [ABS] + [FT https://ar5iv.labs.arxiv.org/html/1604.04183].
  - J_a ≡ ∇^b T_ab may be nonzero, but integrability requires dJ = 0, i.e. J_a = ∇_a Q. The effective Λ then accumulates as Λ₀ + ∫J.
  - Only cosmological consequences are treated; galaxies are not addressed.
  - Newest fit: Chavarría, Fromenteau, Sudarsky & Vargas-Magaña 2026, https://arxiv.org/abs/2607.09750 [ABS]. With Planck 2018 + DESI DR2 + DES Y5 they find Δρ_Λ ≈ −0.016 ± 0.035 (consistent with zero) and a transition at a* ≈ 0.39. AIC favours ΛCDM; DIC shows a slight preference for the unimodular models.
- **Status review.** Carballo-Rubio, Garay & García-Moreno 2022, CQG, https://arxiv.org/abs/2207.08499 [ABS]. Unimodular gravity uses transverse diffeomorphisms plus Weyl rescalings. Beyond the treatment of Λ (technically natural there), no significant difference from GR was found.
- **Meaning for door 11 [INF].** Henneaux-Teitelboim gives the vacuum a conjugate "time" but no local velocity field that could be boosted. In unimodular gravity, energy flowing into the vacuum must be curl-free and would show up as a spatial gradient of Λ.

---

## 7. Three-form dark energy

**Equations.** Koivisto & Nunes 2009, PRD 80, 103509, https://arxiv.org/abs/0908.0920 [ABS + FT https://ar5iv.labs.arxiv.org/html/0908.0920]. Sign conventions below are as the summary returned them.
- Action: S = −∫√−g [R/(2κ²) − F²/48 − V(A²)], with F = dA.
- Homogeneous ansatz: A_ijk = a³ ε_ijk χ(t), so A² = 6χ².
- Equation of motion: χ̈ = −3Hχ̇ − V_χ − 3Ḣχ.
- Energy and pressure: ρ = ½(χ̇ + 3Hχ)² + V and p = −½(χ̇ + 3Hχ)² − V + χV_χ.
- Equation of state: **w = −1 + χV_χ/ρ**. It is phantom where χV_χ < 0, and phantom crossing is possible.
- Sound speed: **c_s² = χV_χχ/V_χ**, which equals n − 1 for V ∝ χⁿ. c_s² ≥ 0 is needed to avoid a gradient instability.
- The Friedmann constraint gives |χ| ≤ √(2/3) (κ = 1 units) when χ̇ = 0.

**Background dynamics and stability.**
- Koivisto & Nunes 2010, PLB 685, 105, https://arxiv.org/abs/0907.3883 [ABS]: scaling solutions, possibly transient acceleration, and phantom crossing.
- De Felice, Karwan & Wongjun 2012, PRD 85, 123545, https://arxiv.org/abs/1202.0896 [ABS]. They derive the no-ghost and no-Laplacian conditions. Mexican-hat potentials are generally unstable, but stable classes exist.
- Koivisto, Mota & Pitrou 2009, JHEP 0909:092, https://arxiv.org/abs/0903.4158 [ABS]. Some n-form actions are equivalent to f(R) or scalar models; a two-form with non-minimal coupling is unstable.

**Couplings.**
- Koivisto & Nunes 2013, PRD 88, 123512, https://arxiv.org/abs/1212.2541 [ABS]: a three-form coupled to CDM; LSS severely restricts the coupling.
- Morais et al. 2017, Phys. Dark Univ., https://arxiv.org/abs/1608.01679 [ABS]: which interactions avoid the "little sibling of the big rip".

**Observational status.**
- Bouhmadi-López, Chiang, Boiza & Chen, JCAP (accepted), https://arxiv.org/abs/2512.09991 [ABS]. A Gaussian-potential three-form fitted to Planck PR4 + DESI DR1 + Pantheon+ + Cepheids + DES Y1. H₀ = 68.29 (+0.56, −0.61) against 67.89 ± 0.36 for ΛCDM: phantom-like, a mild improvement.
- Bouhmadi-López et al. 2026, https://arxiv.org/abs/2606.27436 [ABS]. With DESI DR2 BAO etc., the three-form is mildly preferred when Pantheon+ (especially with SH0ES) is included and neutral otherwise. The reconstructed w has a phantom phase at intermediate z and is Λ-like early and late.

**Meaning for door 11 [INF].** The homogeneous three-form is Hodge-dual to a vector along cosmic time. It is the published "vacuum with a time direction", but it is spatially isotropic. No link to galaxy dynamics was found.

---

## 8. Dark energy with velocity or momentum; sound speed, anisotropic stress, bulk flows

**Can the vacuum move?** Carroll 2001, Living Rev. Rel., https://ar5iv.labs.arxiv.org/html/astro-ph/0004075 [FT, §1.3]. T_μν^vac = −ρ_vac g_μν is the only Lorentz-invariant form. [INF] So a w = −1 component has no rest frame; its momentum density (ρ + p)v vanishes.

**Moving dark energy.**
- Maroto 2006, JCAP 0605:015, https://arxiv.org/abs/astro-ph/0512464 [ABS + FT ar5iv].
  - Rest frames of the CMB, matter and dark energy may differ, so an observer at rest in the CMB can still see a dipole.
  - The relative velocity scales as a^(3w−1). For constant w < −0.78 it decays faster than a^(−3.3).
  - Scaling models keep it longer, giving total damping factors ~10⁻³-10⁻⁴.
  - Observable effects need a relative velocity today of ≳ 10² km/s. No observational bound is derived.
- Beltrán Jiménez & Maroto 2007, PRD 76, 023003, https://arxiv.org/abs/astro-ph/0703483 [SR]. Fluids with differing velocities feed the CMB quadrupole. Initially stiff models are unstable to velocity perturbations, while scaling models can contribute non-negligibly.
- Beltrán Jiménez & Maroto 2009, JCAP 0903:015, https://arxiv.org/abs/0811.3606 [ABS]. Large bulk flows could signal dark energy moving at decoupling.
- Orjuela-Quintana & Beltrán Jiménez 2025, JCAP 04(2025)051, https://arxiv.org/abs/2412.12018 [ABS]. Shift-symmetric Horndeski with a spatial field gradient gives Bianchi I backgrounds with a preferred direction. The momentum density evolves universally, with consequences for dark flows and the CMB dipole and quadrupole.

**Sound speed.**
- Yang, Wang, Ren, Saridakis & Cai 2025/26, https://arxiv.org/abs/2511.22478 [ABS]. From DESI DR2 + Planck 2018 + Union3, for a time-varying w: log₁₀ c_s² = −3.00 (+2.9, −0.99). An EFT analysis favours c_s² ~ 0.3-0.4. For constant w, c_s² is unconstrained.
- Mota, Kristiansen, Koivisto & Groeneboom 2007, MNRAS 382, 793, https://arxiv.org/abs/0708.0830 [ABS]. Sound speed and viscosity (anisotropic stress) are hard to pin down with current data.
- Koivisto & Mota 2006, PRD 73, 083502, https://arxiv.org/abs/astro-ph/0512135 [SR].

**Anisotropic dark energy.**
- Koivisto & Mota 2008, JCAP 0806:018, https://arxiv.org/abs/0801.3676 [ABS]. Bianchi I skewness parameters are well constrained, most tightly by the CMB quadrupole, though some models evade that bound.
- Appleby & Linder 2013, PRD 87, 023532, https://arxiv.org/abs/1210.8221 [ABS]. The CMB strongly restricts integrated dynamical anisotropy.

**Bulk flows.**
- Planck Intermediate XIII 2014, A&A 561, A97, https://arxiv.org/abs/1303.5090 [ABS]. From the kSZ effect, the bulk flow is **< 254 km/s (95%) on Gpc scales** and the monopole is 72 ± 60 km/s.
- Watkins et al. 2023, MNRAS 524, 1885, https://arxiv.org/abs/2302.02028 [ABS]. CF4 minimum-variance bulk flows have < 0.03% (150 h⁻¹ Mpc) and < 0.003% (200 h⁻¹ Mpc) probability in ΛCDM.
- Nusser & Tully 2026, https://arxiv.org/abs/2608.14265 [ABS]. CF4 is broadly ΛCDM-consistent (2.29σ dipole), with a localised 3.40σ, ~628 km/s feature at 120-160 Mpc that depends on the survey component. They read it as regional or systematic.
- Whitford et al. 2023, 428 ± 108 km/s at 173 h⁻¹ Mpc: [SR], UNVERIFIED.

---

## 9. Published links between a dark-energy current/flux and galaxy dynamics or MOND

**Vacuum thermodynamics.**
- Milgrom 1999, Phys. Lett. A 253, 273, https://arxiv.org/abs/astro-ph/9805346 [ABS]. For an accelerated observer in de Sitter, the Unruh temperature goes as (a² + a₀²)^{1/2} with a₀ = (Λ/3)^{1/2} (c = 1). The abstract suggests inertia, and hence MOND, may be a vacuum effect, and calls the mechanism speculative. This is the origin of the a₀-Λ link; it does not fix κ.
- Klinkhamer & Kopp 2011, Mod. Phys. Lett. A 26, 2783, https://arxiv.org/abs/1104.2022 [ABS]. Entropic gravity with a minimum temperature gives a MOND-form force; a₀ is tied to the Unruh temperature of the emerging de Sitter space.

**A flowing dark medium.**
- Zhao 2007, ApJL 671, L1, https://arxiv.org/abs/0710.3616 [ABS]. A medium flowing with four-velocity U^μ adds a non-linear pressure (the "vector-for-Λ" model). It is claimed consistent with the Solar System, dwarf spirals, the Bullet cluster, BBN and late-time acceleration.
- Zhao & Li 2010, ApJ 712, 130, https://arxiv.org/abs/0804.1588 [ABS]. A single "dark fluid" vector of variable norm, with its own stress tensor and current. f(R), TeVeS-like, Einstein-aether and νΛ theories are limits. Parameter choices are claimed to pass BBN, PPN and causality.

**Dark energy displaced by matter** (the closest published analogue of "compaction").
- Verlinde 2017, SciPost Phys. 2, 016, https://arxiv.org/abs/1611.02269 [ABS]. Dark energy carries a volume-law entropy. Matter displaces it, and the elastic response is an extra "dark" force with a₀ = cH₀.
- Lelli, McGaugh & Schombert 2017, MNRAS 468, L68, https://arxiv.org/abs/1702.04355 [ABS]. It matches the RAR only with implausibly low M/L, and predicts radius-correlated residuals that are not seen.
- Hees, Famaey & Bertone 2017, PRD 95, 064019, https://arxiv.org/abs/1702.04358 [ABS]. Galaxy fits are marginal, and Solar-System perihelion precessions are off by **seven orders of magnitude**.
- Hossenfelder 2017, PRD 95, 124018, https://arxiv.org/abs/1703.01415 [ABS]. A covariant version: a vector field in de Sitter that "drags" on baryons and also gives dark energy.
- Tuveri & Cadoni 2019, PRD 100, 024029, https://arxiv.org/abs/1904.11835 [ABS]. Baryons break de Sitter scale symmetry and set an IR scale r₀. Three derivations (one uses an anisotropic fluid source) recover the McGaugh et al. RAR.

**Result.** No paper was found that ties a dark-energy **spatial current/flux** (vacuum momentum) to galaxy rotation. The published links go either through a timelike medium or vector (Zhao; Zhao & Li; Hossenfelder) or through de Sitter thermodynamics (Milgrom; Verlinde; Klinkhamer & Kopp; Tuveri & Cadoni). The unimodular "current" J is cosmological only and curl-free (item 6).

---

## What this means for the door-11 gates

### G6, preferred frame
- **Replace the gate line with the sourced numbers** (all 95% CL, CMB frame):
  - α̂₁ ∈ [−3.5, +3.3] × 10⁻⁵ (Shao & Wex 2012), or the tighter |α̂₁| < 2.1 × 10⁻⁵ (Liu et al. 2020).
  - |α̂₂| < 1.6 × 10⁻⁹ (Shao et al. 2013).
  - Weak field: α₁ = (−0.7 ± 1.8) × 10⁻⁴ (LLR) and |α₂| < 2.4 × 10⁻⁷ (solar spin; secondary citation).
- **A variant must compute both kinds.** The weak-field α₁ and α₂ come from its post-Newtonian metric. The strong-field α̂ values need neutron-star sensitivities. If sensitivities cannot be computed, score G6 on the weak-field bounds (as Oost et al. and Bonetti & Barausse do) and mark α̂ UNDEFINED rather than passed.
- **11B′** (flow rest frame = CMB/Hubble frame): the published limits apply directly, with w ≈ 369 km/s for the Solar System.
- **11A** (each system's own rest frame): the relevant w differs. Shao & Wex also give Galaxy-rest-frame limits, but those were not read (UNVERIFIED).
- **11C**: use α₁ = −4c₁₄ (aether with c₁₃ ≈ 0) or α₁ = 4(α − 2β)/(β − 1) (khronometric). Bonetti & Barausse 2015 is the template, including its strong-coupling warning.
- [INF] Because the α̂₂ bound is ~150× stricter than the weak-field α₂ bound, any variant with α₂ of order its couplings needs couplings ≲ 10⁻⁷-10⁻⁹.

### G7, frame dependence of a₀
- **No published test** of a₀, or of BTFR/RAR residuals, against a galaxy's speed relative to the CMB or a flow frame was found. The khronometric MOND literature does not discuss it.
- **BTFR numbers the gate can use.**
  - Intrinsic scatter ~0.1 dex (Lelli, McGaugh & Schombert 2016, https://arxiv.org/abs/1512.04543 [ABS]).
  - ~6% orthogonal intrinsic scatter using V_flat, slope 3.85 ± 0.09 (Lelli et al. 2019, MNRAS 484, 3267, https://arxiv.org/abs/1901.05966 [ABS]).
  - [INF] A 10% change in a₀ is 0.041 dex in M_b at fixed V, or 0.010 dex in V at fixed M_b. That is comparable to the 2019 scatter and below the 2016 one, so **the scatter alone gives only a weak bound**.
  - The decisive measurement would be BTFR/RAR residuals against CMB-frame peculiar speed. It is not in the literature and could be run as a new test.
- [INF] A naive O((v/c)²) effect at 600 km/s is 4 × 10⁻⁶, which is harmless. G7 bites only if a variant amplifies it by ≳ 2 × 10⁴ (the KM1-type mechanism named in the gates).

### G8, anisotropy (11B′)
- **The only direct published measurement is a claimed detection, not a bound.** It is the 25-37% a₀ dipole of Zhou et al. 2017 and Chang et al. 2018: SPARC only, fixed M/L, clustered sky coverage, unreplicated, and roughly perpendicular to the CMB dipole. It must not be used as the G8 bound, and it must not be read as support either.
- **Declarable galaxy-scale bound [INF].** Direction-dependent a₀ dipole ε ≲ 0.06 ± 0.015 (≲ 0.09 at ~2σ), converted from the CF4 TF zero-point dipole of 0.063 ± 0.016 mag (Boubel et al.). Stiskalek et al. attribute that dipole to local flows or systematics, so the bound is conservative.
  - **This conversion is ours, not published.** It assumes the anisotropy sits in V_flat and that luminosity-TF and baryonic-TF behave alike.
  - No published bound on a quadrupolar (axis) dependence was found.
- **Other bounds that bite on a streaming flow.**
  - Q₂ = (3 ± 3) × 10⁻²⁷ s⁻² in the Solar System (Cassini) covers the anisotropic tidal part at high acceleration; the uniform part is unobservable.
  - Laboratory light isotropy, Δc/c ~ 10⁻¹⁷, applies if the flow affects light.
  - The Planck kSZ bulk flow < 254 km/s (95%, Gpc) applies if the flow drags matter or carries momentum.
  - CMB-quadrupole bounds on moving or anisotropic dark energy (Beltrán Jiménez & Maroto; Koivisto & Mota) apply if the flow is a cosmological fluid.
- **A structural point for 11B′** (from items 6, 8 and bottom line 3). A spatial flow cannot be carried by Λ itself, which is Lorentz-invariant. It needs a new field, which makes 11B′ an aether/khronon-type theory with a boosted or spacelike component. G6 then applies at order α₁ (w·v)/c² and α₂ (w·x)²-type terms.

### Other gates touched
- **G2.** The aether rescales G_cosmo relative to G_N (Carroll & Lim), and the dark-matter regime of generalized Einstein-aether fails CMB + LSS while the dark-energy regime passes (Zuntz et al.; Trinh et al.). That is compatible with door 11 keeping CDM.
- **G5.**
  - Generic aether kinetic terms are unstable (Carroll et al.).
  - AeST and the relativistic khronon both have unbounded Hamiltonians at very low k (μ ≲ Mpc⁻¹; k ≲ 10⁻³¹ eV). Low-k instability is a known cost of this class.
  - Emergent-gravity-type "displacement" fails the Solar System by 10⁷ (Hees et al.).

---

## Searches that returned nothing relevant (not the same as "nothing exists")
- RAR or BTFR residuals against the CMB-dipole direction, against galaxy peculiar velocity, or against the CMB frame.
- a₀ dependence on a galaxy's velocity relative to an aether frame.
- Independent replication or rebuttal of Zhou et al. 2017 / Chang et al. 2018.
- A spacelike (one-direction) vacuum or aether flow that produces MOND.
- A dark-energy spatial current or flux tied to rotation curves.
- A published bound on a quadrupolar a₀ anisotropy.

## Cross-check with `DOOR11_LITERATURE_DATAFRONT_2026-09-29.md` (the independent abstract-level pass)
- **Agree.**
  - 1.6 × 10⁻⁹ is a strong-field α̂₂ bound.
  - The α̂₁ bound is ≈ 3.5 × 10⁻⁵ (the interval), not exactly 3.4 × 10⁻⁵.
  - The Zhou and Chang numbers.
  - No directional-flow MOND and no link between a dark-energy flux and galaxies.
  - The river model is a GR re-description.
  - AeST and the khronon theories are the surviving timelike-vector successors.
- **This file adds (from full texts).**
  - The CMB-frame assumption and w = 369 km/s in both pulsar papers.
  - The newer |α̂₁| < 2.1 × 10⁻⁵ bound (Liu et al. 2020).
  - The LLR α₁ values, read directly: (−7 ± 9) × 10⁻⁵ realistic, and (−0.7 ± 1.8) × 10⁻⁴ at 95% as cited by Shao & Wex.
  - The Henneaux-Teitelboim gauge-vs-physical answer (only the four-volume is physical).
  - The three-form w(z), c_s² and stability conditions.
  - The Zlosnik-Ferreira-Starkman action and its caveats.
  - The angle between the CMB dipole and the claimed a₀ dipole.
  - The CF4 conversion to an a₀-dipole bound [INF].
- **Unresolved in both files.**
  - The Shao & Wex Galaxy-frame limits.
  - Nordtvedt 1987 read directly.
  - Whether Carroll et al. 2009 covers F(K) aethers.
  - The datafront's second LLR value, (−8 ± 4) × 10⁻⁵, which this file did not see.
