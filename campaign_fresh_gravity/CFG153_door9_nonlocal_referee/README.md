# CFG153 — Referee of CFG123 (Door 9): the RR model's weak-field effective density against CFG44's target

- **Criteria:** frozen in `../CFG153_FROZEN_CRITERIA.md` (c5c58cc22, sha256 `bf50fa3f…aeaf29`), before any code of this lane. Every output prints that hash first.
- **Script:** `cfg153_rr_weak_field.py`, one file, my own code. It imports nothing from CFG123 or CFG44. The main run takes about 10 s and the MUTATE run about 11 s.
- **Post hoc:** `POSTHOC_1_start_time.py` was written after the frozen runs and after reading CFG123's outputs. It is not evidence.
- **Runs:**
  - The main run passes H1 and C1–C4 and C6. It exits 1, because one sub-line of the control C5 fails as frozen (see Controls).
  - The MUTATE run fails H1 by 6.0 dex, with the predicted shift, and exits 1 as required.
  - The post-hoc script exits 0.

## Bottom line

**Yes. CFG123's headline reproduces in its own setting.** With my own algebra and code, the Maggiore–Mancarella RR model's static weak-field response on a flat background falls short of CFG44's target by about ten orders of magnitude.

- **The headline number.** At M_b = 10¹² M☉ and x = 30 (r = 1.16 Mpc), on the canonical footing, |R_A| = |ρ_eff/ρ_target| = 6.057 × 10⁻¹¹.
  - That is a shortfall of 1.651 × 10¹⁰ (10.22 dex), against CFG123's 6.1 × 10⁻¹¹ and 1.65 × 10¹⁰.
  - All four pinned values agree within 0.006 dex; the H1 line is 0.5 dex. All four round to CFG123's printed two figures.
- **The ingredients reproduce exactly.**
  - ρ_eff = −m²M cos(mr)/(12πr), so c1 = −1/3 by two independent routes. The sign is negative at every grid point: gravity is weakened, not boosted.
  - My own background gives m/H0 = 0.283768.
- **The one numerical difference is diagnosed (post hoc).** CFG123's m/H0 = 0.283934 is 5.8 × 10⁻⁴ higher than mine, which moves R_A by 0.1% (0.0005 dex).
  - CFG123 starts its background at a = 10⁻⁶; I start at x = ln a = −18.
  - Started at a = 10⁻⁶, my own equations give 0.283934 and CFG123's range [2.030 × 10⁻¹⁵, 6.064 × 10⁻¹¹] to every printed digit.
  - My value is converged: a start at −21 agrees with it to 9 × 10⁻⁶, and starts at −21 and −24 agree to 4 × 10⁻⁷.
- **Scope.** The agreement holds inside CFG123's flat-background setting only.
  - Row E1 sizes the coupling of the cosmological background field Ū to the local mass: Ū(0)/2 = 8.02 times the flat-space term in the 00 equation.
  - CFG123's own perturbation equations contain that term (see the comparison notes). Neither lane evaluates it at the order of the headline.
  - My hand estimate is that it could move the number by one to two dex. That would not threaten "about ten orders too small", but it does limit what the 0.5-dex agreement means.

## Comparison with CFG123

My value is from `cfg153_rr_weak_field.out`. CFG123's printed value is from its README, with its three-figure value from `A2_static_linear_response.out` in brackets.

| quantity | CFG153 (mine) | CFG123 | agreement |
|---|---|---|---|
| c1 in ρ_eff = c1 m²M/(4πr) | −1/3 (routes A and B); exact factor cos(mr) | −1/3 (leading order in m²) | exact; cos(mr) − 1 ≤ 2.7 × 10⁻⁹ on the grid |
| sign of ρ_eff | negative at all 88 grid points | negative everywhere | same |
| m/H0 | 0.283768 (x_i = −18) | 0.2839 (0.283934, a_i = 10⁻⁶) | −5.8 × 10⁻⁴; the start time (post hoc) |
| \|R_A\| canonical, 10⁹ M☉, x = 0.1 | 2.028 × 10⁻¹⁵ | 2.0 × 10⁻¹⁵ (2.030) | 0.006 dex |
| \|R_A\| canonical, 10¹² M☉, x = 30 | 6.057 × 10⁻¹¹ | 6.1 × 10⁻¹¹ (6.064) | 0.003 dex |
| \|R_A\| alt, 10⁹ M☉, x = 0.1 | 1.678 × 10⁻¹⁵ | 1.7 × 10⁻¹⁵ (1.680) | 0.006 dex |
| \|R_A\| alt, 10¹² M☉, x = 30 | 5.012 × 10⁻¹¹ | 5.0 × 10⁻¹¹ (5.018) | 0.001 dex |
| shortfall, canonical best point | 1.651 × 10¹⁰ (10.22 dex) | 1.65 × 10¹⁰ | same |
| G1-S spread over x | 29.868 | 29.87 | same |
| G1-M spread over M_b | 1000.0 | 1000 | same |
| m_req at x = 0.1, × H0/c | 6.301 × 10⁶ … 1.993 × 10⁵ (leading order); 6.35 × 10⁶ … 2.008 × 10⁵ (exact linear) | 6.3 × 10⁶ … 2.0 × 10⁵ | leading order same; the exact form is 0.8% higher |
| 1/m_req | 0.5788 r_M (leading order); 0.5744 r_M (exact linear) | 0.5788 r_M | leading order same |
| sphere h = 2 kpc, \|R_X\| canonical | [6.152 × 10⁻¹⁷, 2.018 × 10⁻¹²] | [6 × 10⁻¹⁷, 2.0 × 10⁻¹²] ([6.16, 2.02]) | 0.011 and 0.004 dex |
| Ū(0) | 16.045 | 16.0 (16.035) | the start time |
| H0²S̄(0) | 2.0655 | 2.06 (2.064) | the start time |
| w_DE(0) | −1.1457 | −1.146 (−1.1457) | same; the literature's w0 = −1.144 |
| E1 = Ū(0)/2 | 8.02 | not computed | beyond CFG123's scope |

- The maximum |R_X| of the sphere sits at x = 2 for 10¹² M☉, not at x = 30. Beyond a few h the sphere acts as a point mass, so |R_X| is flat to 10⁻⁸, and the cos(mr) factor lowers it by about 10⁻⁹ outward. The compared value is the same.
- The literature sanity rows hold. My m/H0 is 0.27% above Maggiore–Mancarella's m ≃ 0.283 H0 (γ ≃ 0.00891, for Ω_DE ≃ 0.68; the inputs differ). w_DE(0) = −1.146 against their w0 = −1.144.

## Method, briefly

- **Localisation.** I use one multiplier: L = √−g [(1 − λ)R − (m²/6)U² + ∇λ·∇U]/16πG, with λ = (m²/3)S on shell. CFG123 uses two (U, S, ξ1, ξ2).
- **Route A: the nonlocal action at quadratic order.**
  - sympy expands √−g R for −(1+2Φ)dt² + (1−2Ψ)dx² and finds R⁽¹⁾ = ∇²(4Ψ − 2Φ). So the static R□⁻²R becomes (4Ψ − 2Φ)².
  - The Euler–Lagrange equations are solved in Fourier space: Φ̂/ρ̂ = −4πG(3k² − 4m²)/[3k²(k² − m²)].
  - Partial fractions and the Green's functions 1/(4πr) and cos(mr)/(4πr) give Φ = −(GM/r)[1 + (1 − cos mr)/3], exact in mr. The second Green's function is the standing-wave one (declared).
- **Route B: the localised action, Weyl-reduced.**
  - The reduction is on −A dt² + B dr² + C r² dΩ². sympy varies A, B, C, U and λ, sets C = 1 and linearises.
  - A first integral of the U-constraint fixes U's normalisation.
  - An ansatz with unknown coefficients through O(m²) gives a₂ = −m² r_S r/6, so c1 = −1/3. The answer was not typed in.
- **Background.** This is the minisuperspace of the same one-multiplier action. Varying N gives the constraint and varying a the acceleration equation.
  - U and λ are integrated from x = −18 with zero data (DOP853, rtol 10⁻¹¹).
  - m/H0 is root-found so that h(0) = 1, with H0 = 67.36, Ω_m = 0.3153, Ω_r h² = 4.15 × 10⁻⁵ and no Λ.
- **Grid values.** They come from the derived closed form at 50 digits (mpmath).
  - CFG123's definition of ρ_eff was also applied numerically, from g_tt at 50 digits, and matches the closed form to 2 × 10⁻²⁵.
  - The sphere uses route A's general-source solution, Φ = c0 I₀ + cm I_m with c0 = −16πG/3 and cm = 4πG/3, and an exact radial convolution.

## Controls

- **C1 PASS (GR limit).** At m = 0 both routes give Φ = Ψ = −GM/r and ρ_eff = 0. Route B's O(m⁰) solve gives b = r_S/r.
- **C2 PASS (the model's known static limit).**
  - My solution equals Kehagias–Maggiore's eqs. (4.31)–(4.33) exactly (symbolic residual 0 in A, B and U).
  - Its series gives Maggiore–Mancarella's A ≃ 1 − (r_S/r)(1 + m²r²/6) and B ≃ 1/A. The correction to the potential is of relative order (mr)², with coefficient 1/6 exactly.
- **C3 PASS (two routes).**
  - Route B's O(m²) solve gives α1 = −1/6, β1 = 1/6, μ1 = −1/2 and λ1 = −1/6, with the rest zero or free constants.
  - Route A's exact solution solves all five route-B equations and the first integral.
  - A constant added to λ drops out of every linear equation, as the spec required to be checked.
- **C4 PASS (the published background equations).** My constraint equals Maggiore–Mancarella's h² = Ω_M e^{−3x} + Ω_R e^{−4x} + γY term by term. My λ-equation equals their W-equation times a³μ²/18, and my U-equation equals theirs times a³H²/6.
- **C5 FAIL as frozen, kept load-bearing.**
  - Two sub-lines pass: the ΛCDM limit to 8.9 × 10⁻¹⁶ (line 10⁻⁹), and constraint propagation to 5.9 × 10⁻¹⁶ (line 10⁻⁸).
  - The start-time sub-line fails. Moving x_i from −18 to −15 changes m/H0 by 1.73 × 10⁻⁴, against a line of 10⁻⁴. Moving it to −21 changes it by 8.7 × 10⁻⁶ (post-hoc precision).
  - The cause: a zero-data start at −15 is only seven e-folds before matter–radiation equality, so it misses some early growth of U. From −18 on, the value has converged.
  - The frozen line was too tight for the −15 probe. It changes R_A by 3.5 × 10⁻⁴ (0.00015 dex).
  - The failure stays load-bearing, so the main run exits 1. It was first seen in a development run in a scratch area; nothing frozen was changed.
- **C6 PASS (the target, my implementation).**
  - ρ_c r³ g_P2 = (a₀/4π)M_b to 5 × 10⁻⁵¹.
  - The quadrature of M_c = M_b(√(1+x²) − 1) agrees to 4 × 10⁻⁴⁹, and g_P2 = G(M_b + M_c)/r² to 5 × 10⁻⁵¹.
  - The sphere's M_b(<r) matches quadrature to 2 × 10⁻⁴⁷.
  - Fed the density rebuilt from the cold mass, the comparator returns 1 to 7 × 10⁻⁵¹.
- **MUTATE works.** m_static = 10³ m is planted in the static action before the derivation.
  - log10|R_A| rises by 5.99882 to 6.00000 dex, against the predicted 5.998 to 6.000.
  - H1 fails at all four points by 5.994 to 6.006 dex, and the run exits 1.
- **Checks added beyond the frozen file (all pass).**
  - My Ricci-scalar helper gives 2/a² on a 2-sphere and 6(ä/a + ȧ²/a²) on FRW.
  - The Green's-function table passes (Laplacian, Helmholtz and delta normalisation).
  - The numerical CFG123-definition check matches to 2 × 10⁻²⁵.
  - The largest mr on the grid is 7.38 × 10⁻⁵.

## How CFG123's scripts carry Ū and S̄ (a comparison note, not a re-score)

- **The nonlinear ladder does not carry them.** A3, with `cfg123_nl.py` and `cfg123_static.py`, declares prescription P0: S(0) = 0 ("no cosmological S-bar") and U → 0 at infinity. That means the exact Schwarzschild exterior at λ = 0 and the standing-wave β = 0 at finite λ. So N1–N3 run on a flat exterior with no background U or S.
- **The README's "background values Ū = 16.0 and S̄ = 2.06 as constants" is A2's "embedding scan".** That scan is exploratory and reported, not a gate. It uses today's values (16.035, 2.064) in two ways only:
  - F̄ = 1 − m²S̄/3 = 0.9445, a rescaling of G (μ_eff = 1.0587);
  - a uniform density shift m²c²Ū/(24πG) = 1.2 × 10⁻²⁷ kg/m³.
- **Neither is the term E1 sizes.** CFG123's own A4 perturbation equation δE₀₀ contains −m²Ū u/6 and −m²Ū²φ/6 at order k⁰.
  - Next to them is the flat-space source −k²m²s/(3a²) → −m²u/3.
  - The Ū u term is therefore Ū/2 ≈ 8 times the flat-space term (my E1 = 8.02).
  - A4 classes every k⁰ term as relative order (aH/k)² or m²a²/k². That is right for growth at k ≥ 0.5/Mpc, where it is ≤ 10⁻⁴. But A2's static ρ_eff is itself a term of exactly that order, and neither A2 nor A3 carries the Ū u term.
  - A frozen-constant static version is not consistent: by hand, the Bianchi identity leaves a residual ∝ (m²/3)Ū ∂δU. So this needs the time-dependent embedding, which neither lane builds.
- **No CFG123 verdict changes.** A factor of about 8, of unknown sign, is small against a 10-dex gap.

## Independence statement

- **Mine:**
  - all the code;
  - the one-multiplier localisation;
  - route A (Fourier, exact in mr) and route B (reduced action, unknown-coefficient ansatz);
  - the minisuperspace derivation and the integrator;
  - the target implementation and the constants (GM☉ from IAU, which differs from CFG123's G × M☉ by 3.0 × 10⁻⁵; negligible here).
- **Shared with CFG123 (a shared error would not be caught):**
  - the RR action and its prescription (symmetric variation, retarded zero data);
  - reading R-A;
  - the flat-background static setting and the ρ_eff definition;
  - the grid and the masses;
  - H0, Ω_m, Ω_r h² and the a₀ footings.
- **Not blind.**
  - CFG123's c1, sign, m/H0 and |R_A| range were read before any code, and my pre-run hand algebra was done after that.
  - The literature controls (Kehagias–Maggiore; Maggiore–Mancarella) come from the model's authors. They were read through a summarising fetch of the ar5iv HTML.
  - My code reproduces every quoted literature form exactly, including the garbled Y read as ½ and ¼.
- **Order.** CFG123's scripts and outputs were opened only after both of my runs were saved. The post-hoc script was written after reading them.
- **Correlated-reasoner risk.** The referee is the same kind of model as CFG123's author.
- **Where the methods differ.**
  - CFG123's A1 took the exact linear solution as a candidate, verified it by substitution into its two-multiplier covariant equations, and then took the leading order. A2 hard-codes C1 = −1/3 and uses the leading-order ρ_eff.
  - My route A derives the exact form, and route B finds the O(m²) coefficients from unknowns.
  - CFG123 gets ζ by differentiating the constraint; I get it from the acceleration equation, and constraint propagation checks the two against each other.

## Disclosed departures and open choices

1. **MUTATE background.** The spec says the shooting is "bypassed". In MUTATE mode the background is solved unmutated, to supply the background-fixed m, and the plant enters only the static action. The shift is measured against an unmutated route-A derivation inside the same run.
2. **m_req.** It is reported in two forms: at leading order (CFG123's definition) and in the exact linear form (my R_A's form). They differ by 0.8% because m_req r = 0.17 there.
3. **Where R3 compares.** R3 compares the range ends; for 10¹² M☉ the maximum sits at x = 2 (see the note under the table).
4. **Development.** The script was developed with fragment and full runs in a scratch area. The recorded runs are the first runs of the final file in the lane folder, and nothing frozen was changed.
5. **Background C5 wording.** "The acceleration equation and the x-derivative of the constraint agree" is evaluated at 181 points from x = −18 to 0.
6. **Post-hoc start-time script.** It re-integrates my own derived equations, read from my results `.json`, from x_i = ln 10⁻⁶, −15, −18, −21 and −24.

## Untested (declared)

- CFG123's θ_* headline and the rest of G2; G3, G4 and G5.
- The nonlinear ladder (N1–N3); the Deser–Woodard model; G1-X beyond the h = 2 kpc sphere.
- **The cosmological embedding at the headline's order.** E1 gives its scale (Ū/2 ≈ 8), and my hand estimate puts its effect at one to two dex, sign unknown. Neither lane solves it.
- **The S̄ rescaling of G** (G_eff/G = 1/F̄ ≈ 1.06). It gives nothing at r > 0 for a point mass. Its time variation is what Lunar Laser Ranging tests; the literature reports the RR model excluded on that ground (Belgacem et al. 2019, abstract read).
- **Homogeneous-solution freedom.** Coefficients of natural size enter at relative order mr ≤ 7.4 × 10⁻⁵ (hand argument).
- **The choice of Green's function** (standing wave against retarded) for the growing mode at r ≳ 1/m.
- **Non-spherical baryons.**
- **The start time of the zero data.** It is a model-definition choice; I use the converged limit, x_i → −∞.

κ = ½ and Ω_c h² stay fitted. Nothing here says the data favour either model, or that the theory is closed.
