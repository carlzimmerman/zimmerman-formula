# CFG153 — Referee of CFG123 (Door 9): the weak-field effective density of the Maggiore–Mancarella RR model against CFG44's target. FROZEN CRITERIA

Written 2026-09-29, before any script or number of this lane. This is a referee lane in the CFG84–86 way. It re-derives ONE headline of CFG123 with its own algebra and code, from CFG123's frozen criteria (e8b9fbcdf) and README only, and says where independence stops.
- CFG123's numbers below were read from its README before any code. They are targets, not blind predictions.
- No CFG123 script, `.out`, `.json` or log is opened before this lane's frozen runs are saved.
- The ten-door menu was written knowing the target (CFG123 section (a)). Nothing here changes that.
- Nothing is committed by the writing agent. The sha256 of this file is printed at the top of every output of this lane, so a later edit is visible.

## The headline under test (pinned from CFG123's README)

CFG123's G1 verdict: the RR model's weak-field static response gives an effective density about ten orders of magnitude below the target.
- **Target (CFG44, point mass, P2).** ρ_c = a₀/(4πG r √(1+x²)), with x = r/r_M and r_M = √(G M_b/a₀). The footings are a₀ = 9.3603e-11 (canonical) and 1.1312e-10 m/s² (alt), as in CFG123's frozen criteria.
- **G1-A, point mass, as printed.** |R_A| = |ρ_eff/ρ_target| lies in [2.0e-15, 6.1e-11] (canonical) and [1.7e-15, 5.0e-11] (alt), "a shortfall of at least 1.65e10".
- **Points.** The README gives the range, not the points. Its stated scalings (R_A ∝ M_b exactly; shape exactly √(1+x²)) put the extremes at two grid corners, which I pin:
  - minimum: M_b = 1e9 M☉, x = 0.1 (r ≈ 0.122 kpc canonical, 0.111 kpc alt);
  - maximum: M_b = 1e12 M☉, x = 30 (r ≈ 1.16 Mpc canonical, 1.05 Mpc alt).
- **The headline number.** |R_A| = 6.1e-11 at M_b = 1e12 M☉, x = 30, canonical. That is a shortfall of 1.65e10 (10.2 dex) at the model's best point.
- **Stated ingredients.** δΦ = −m²GMr/6, ρ_eff = −m²M/(12πr), c1 = −1/3 (negative: δg/g_N = −(mr)²/6). m/H0 = 0.2839, shot from H(a=1) = H0 under reading R-A.
- **Printed by-products** (reported rows here, not the headline):
  - G1-S spread 29.87; G1-M spread 1000;
  - m_req = 6.3e6 (1e9 M☉) to 2.0e5 (1e12 M☉) × H0/c, with 1/m_req = 0.5788 r_M;
  - exponential sphere, h = 2 kpc: |R_X| in [6e-17, 2.0e-12];
  - background: Ū = 16.0, S̄ = 2.06, w_DE(0) = −1.146.
- **Out of scope.** CFG123's other headline (θ_* shifted by +3.80 km/s/Mpc against the 0.54 line). It is untested here.

## The model and setting (declared; taken from CFG123, not re-chosen)

- **Action.** The RR model (Maggiore–Mancarella 2014): S = (1/16πG) ∫ √−g [R − (m²/6) R □⁻² R] + S_m, with one constant m (1/length).
- **Prescription.** □⁻¹ is varied as if symmetric. Retarded zero data are then imposed: U = S = 0, with zero first derivatives, deep in radiation domination.
- **Reading R-A.** The nonlocal term replaces Λ. m is fixed by H(a=1) = H0, with H0 = 67.36 km/s/Mpc, Ω_m = 0.3153, Ω_r h² = 4.15e-5, spatial flatness and no separate Λ.
- **Static limit.** Weak field on a flat background (the Kehagias–Maggiore setting CFG123 declares), linear in the source.
- **Effective density (CFG123's definition).** ρ_eff = (1/4πG r²) d/dr[r²(g_tot − g_N)]. g_tot is the baryons' acceleration from g_tt; g_N uses the same G.
- **Grid.** x in {0.1, 0.2, 0.3, 0.5, 1, 2, 3, 5, 10, 20, 30}; M_b in {1e9, 1e10, 1e11, 1e12} M☉; both footings.
- **My constants (chosen independently).** G = 6.67430e-11 m³ kg⁻¹ s⁻²; GM☉ = 1.32712440018e20 m³ s⁻²; c = 299792458 m/s; kpc = 3.0856775814913673e19 m.

## Method (my own algebra and code)

- **Localisation (a deliberate difference).** CFG123 declares the two-multiplier form (U, S, ξ1, ξ2). I use one multiplier:
  - L = √−g [(1 − λ)R − (m²/6)U² + ∇λ·∇U]/16πG, so □U = −R and □λ = −(m²/3)U;
  - on shell λ = (m²/3)S;
  - it rests on ∫√−g R□⁻²R = ∫√−g U² under the symmetric prescription.
- **Route A (nonlocal action, quadratic order).**
  - sympy expands √−g R to second order for ds² = −(1+2Φ)dt² + (1−2Ψ)dx², with Φ and Ψ static.
  - The static □⁻¹ is ∇⁻², so the R□⁻²R term becomes a local square of the potentials.
  - The Euler–Lagrange equations are solved for a point mass in closed form, to all orders in mr at linear order in M.
- **Route B (localised action, reduced).**
  - sympy builds the Weyl-reduced action on ds² = −A dt² + B dr² + C r² dΩ², with U(r), λ(r) and static dust (L_m = −4πr²ρ√A, with ρ held fixed).
  - It varies A, B, C, U and λ, sets C = 1, and linearises in the source.
  - The point mass is solved order by order in m². No new 1/r term enters beyond GR's mass.
  - A constant in λ (the infrared divergence of S) multiplies the background Einstein tensor, which is zero. This is checked, not assumed.
  - Route A's closed form is also substituted into all five route-B equations (C2).
- **From g_tt to ρ_eff.** Both routes give g_tt, then ρ_eff by CFG123's definition.
  - The coefficient c1 in ρ_eff = c1 m²M/(4πr), and its sign, come out of the code. Nothing is typed in.
  - Any difference g_tot − g_N at galactic parameters is taken in mpmath at 50 digits, since δg/g_N ≤ 1e-9 there.
- **m from the dark-energy density.**
  - sympy derives the minisuperspace equations of the same one-multiplier action on ds² = −N²dt² + a²dx², with dust and radiation. Varying N gives the Friedmann constraint; varying a gives the acceleration equation.
  - U and λ are integrated in x = ln a from x_i = −18, with U = U′ = λ = λ′ = 0 (scipy, rtol 1e-11).
  - m/H0 is root-found so that h(0) = 1.
  - Ū(0), H0²S̄(0) = 3λ̄(0)/(m/H0)² and w_DE(0) come from the same solution, with Ω_DE(x) = h² − Ω_m e^{−3x} − Ω_r e^{−4x} and w_DE = −1 − Ω_DE′/(3Ω_DE).
- **Ratio.** R_A = ρ_eff/ρ_target on the grid. It uses the derived exact linear ρ_eff (with its cos(mr) factor) and the shot m.
- **Target.** My own code, from CFG44's README and the Bcommon docstrings. Nothing is imported from CFG44.
  - The point mass is analytic.
  - The exponential sphere uses M_b(<r) = M[1 − (1 + s + s²/2)e^{−s}], with s = r/h.
- **Compute.** Under a minute; no data files. The script is path-independent and writes beside itself.

## Pre-run hand expectation (kept if wrong)

My hand algebra was done after reading CFG123's README, so it is not blind.
- **Route A by hand.** The static quadratic Lagrangian is (1/8πG)[(∇Ψ)² − 2∇Φ·∇Ψ] − (m²/24πG)(2Ψ − Φ)² − ρΦ. With χ = 2Ψ − Φ, (∇² + m²)χ = 4πGρ, so χ = −GM cos(mr)/r. Then:
  - Φ = −(GM/r)[1 + (1 − cos mr)/3] and Ψ = −(GM/r)[1 − (1 − cos mr)/3];
  - ρ_eff = −m²M cos(mr)/(12πr). So c1 = −1/3 and the sign is negative, as CFG123 says.
- **Background by hand.** My constraint is (1 − λ)H² − Hλ̇ + λ̇U̇/6 − (m²/36)U² = (8πG/3)ρ.
  - With λ = (m²/3)S and W = H²S, it equals Maggiore–Mancarella's h² = Ω_M e^{−3x} + Ω_R e^{−4x} + γY, term by term.
  - I expect m/H0 of 0.283–0.285.
- **Ratio by hand.** |R_A| = ((m/H0)²/3)(H0 r_M/c)² √(1+x²) |cos(mr)|. With m/H0 = 0.2839:
  - canonical: 2.03e-15 at the minimum and 6.06e-11 at the maximum;
  - alt: 1.68e-15 and 5.02e-11;
  - a shortfall of 1.65e10.
  - H1 is expected to PASS, within 0.01 dex.

## Checks

- **C1 CONTROL (GR limit).** At m = 0 both routes give Φ = Ψ = −GM/r and ρ_eff = 0 exactly (symbolic).
- **C2 CONTROL (the model's known static limit).**
  - My linear solution must equal Kehagias–Maggiore's exact linear solution, eqs. (4.31)–(4.33) as quoted by the fetch tool (areal gauge, linear order, symbolic residual 0):
    - A = 1 − (r_S/r)[1 + (1 − cos mr)/3];
    - B = 1 + (r_S/r)[1 − (1 − cos mr)/3 + (mr sin mr)/3];
    - U = (r_S/r) cos mr.
  - Its small-mr series must give Maggiore–Mancarella's RR statement, A ≃ 1 − (r_S/r)(1 + m²r²/6) and B ≃ 1/A for r_S ≪ r ≪ 1/m. That is a correction to the Newtonian potential of relative order (mr)², with coefficient 1/6 exactly.
  - Maggiore–Mancarella say RR's linearisation about flat space gives the same result as the (g□⁻¹R)^T model that Kehagias–Maggiore solved.
- **C3 CONTROL (two routes).** Routes A and B give the same g_tt and g_rr at linear order, after the linear map between isotropic and areal radius (symbolic residual 0).
- **C4 CONTROL (background equations).**
  - My derived constraint equals h² = Ω_M e^{−3x} + Ω_R e^{−4x} + γY (symbolic residual 0).
  - Here Y = ½W′(6 − U′) + W(3 − 6ζ + ζU′) + ¼U², W = H²S, γ = m²/(9H0²) and ζ = h′/h.
  - Also U″ + (3 + ζ)U′ = 6(2 + ζ) and W″ + 3(1 − ζ)W′ − 2(ζ′ + 3ζ − ζ²)W = U.
- **C5 CONTROL (integrator).**
  - With the nonlocal term off and a constant Λ, the same integrator returns ΛCDM's h(x) to 1e-9.
  - Along the RR solution, the acceleration equation and the x-derivative of the constraint agree to 1e-8.
  - m/H0 changes by less than 1e-4 (relative) when x_i moves to −15 or −21.
- **C6 CONTROL (target identity, my implementation).**
  - ρ_c r³ g_P2 = (a₀/4π) M_b to 1e-12, with g_P2 = √(g_N² + a₀ g_N).
  - ∫ 4πr²ρ_c dr = M_b(√(1+x²) − 1) by quadrature, to 1e-8.
  - g_P2 = G(M_b + M_c(<r))/r² to 1e-12.
  - The sphere's M_b(<r) matches quadrature of ρ₀e^{−r/h}, ρ₀ = M/(8πh³), to 1e-10.
  - Fed ρ_c itself, the comparator returns R_A = 1 to 1e-12 (false-negative control).
- **H1 [HEADLINE; MUTATE must change it].** At each of the four pinned points, |log10|R_A|(mine) − log10|R_A|(CFG123)| ≤ 0.5:
  - canonical: 2.0e-15 at (1e9 M☉, x = 0.1) and 6.1e-11 at (1e12 M☉, x = 30);
  - alt: 1.7e-15 and 5.0e-11 at the same points;
  - and my grid extremes must sit at those two corners.
  - H1 PASS means CFG123's "about ten orders too small" reproduces.

## Reported rows (not gates)

- **R1 (digits and by-products).**
  - Whether my four values round to CFG123's printed two figures.
  - c1 (CFG123: −1/3), and the sign of ρ_eff at every grid point (CFG123: negative everywhere).
  - The G1-S spread (29.87) and the G1-M spread (1000).
  - m_req and 1/m_req (6.3e6 and 2.0e5 × H0/c; 0.5788 r_M).
- **R2 (background).**
  - m/H0 against 0.2839, with an agreement line of 0.5%.
  - m/H0 against Maggiore–Mancarella's m ≃ 0.283 H0 (γ ≃ 0.00891 for Ω_DE ≃ 0.68). This is a sanity row only, since the inputs differ.
  - Ū(0) against 16.0, and H0²S̄(0) against 2.06 (I read CFG123's S̄ in units of H0⁻²).
  - w_DE(0) against −1.146. The literature's w0 = −1.144 is a fit parameter, so it is only roughly comparable.
- **R3 (exponential sphere, h = 2 kpc at every mass, canonical).** R_X = C_eff/[(a₀/4π)M_b(<r)], with C_eff = ρ_eff r³ g_tot, against [6e-17, 2.0e-12]. The line is 0.5 dex at both ends; it is not the headline.
- **E1 (the size of what is untested).** Ū(0)/2, from my background.
  - It is the ratio of the background coupling −Ū δU g_μν (from −½g_μν U² in Maggiore–Mancarella's K_μν) to the flat-space term −2δU g_μν, in the 00 equation.
  - Hand expectation: about 8.
  - This is a size, not a correction (see Untested).
- **Post hoc (after the frozen runs; not evidence).** My full grid against CFG123's committed `.json`, point by point. A note on how CFG123's scripts carry Ū and S̄ (a note, not a test).

## MUTATE

MUTATE=1 plants m_static = 10³ × m (the background-fixed m) in the static sector's action, before any derivation. The background shooting is bypassed, since it would undo the plant.
- **Prediction.** log10|R_A| rises by 6 + log10[cos(10³mr)/cos(mr)] at every grid point. That lies in [5.998, 6.000] on the grid; the check line is 6.000 ± 0.01.
- **Headline change.** H1 then fails at all four points, by about 6 dex, and the run exits 1.
- **Why 10³ and not 10⁵.** 10⁵ puts mr up to 7 on the grid, where cos(mr) changes sign and the clean m² prediction is lost.

## Exit codes and outputs

- One script in `CFG153_door9_nonlocal_referee/`. Each mode writes its own `.out` and `_results.json` beside the script; MUTATE outputs carry `_MUTATE`.
- **Main.** Exit 0 if and only if H1 and C1–C6 all pass. Otherwise exit 1, naming the failing lines.
- **MUTATE.** Exit 1 if and only if H1 fails and the shift is within its prediction at every point. Exit 0 (H1 still passes) or exit 2 (the shift misses) is a control failure, kept and disclosed.
- Nothing is tuned after the first number is seen. Failed controls are kept.
- CFG123's scripts and outputs are opened only after both runs are saved.

## What I read, what I did not, and where independence stops

- **Read (repository).**
  - CFG123_FROZEN_CRITERIA.md and CFG123's README.
  - closure_map/TEN_DOORS_GATES_2026-09-29.md.
  - CFG44's README, and only the docstrings of CFG44's `Bcommon.py` (extracted without the function bodies).
  - CFG118_FROZEN_CRITERIA.md, for style; the first lines of the sibling referee specs CFG150, CFG155 and CFG156, for format.
  - The recent commit summaries shown in this session, which state CFG123's verdict in one line.
- **Read (literature, abstract pages).**
  - arXiv:1401.8289 (Kehagias–Maggiore, JHEP 08 (2014) 029).
  - arXiv:1402.0448 (Maggiore–Mancarella, PRD 90, 023005 (2014)).
  - arXiv:0706.2151 (Deser–Woodard, PRL 99, 111301 (2007)).
  - arXiv:1812.11181 (Belgacem, Finke, Frassino, Maggiore, JCAP 02 (2019) 035).
- **Read (literature, HTML).** The ar5iv renderings of 1401.8289 and 1402.0448, through a summarising fetch tool.
  - The quoted equations may therefore carry paraphrase errors.
  - The Y formula came back garbled. I read its coefficients as ½ and ¼ and pre-register that reading, which my hand derivation already matches.
- **Not read.** Any CFG123 script, `.out`, `.json`, `run_all.log` or post-hoc file, or its directory listing. CFG44's scripts and outputs. CFG48's and CFG70's commons (not needed: there is no r_ta here).
- **Independence stops here.**
  - The pass lines and my hand expectation were set after reading CFG123's c1, sign, m/H0 and |R_A| range. The re-derivation is not blind.
  - The model, the flat-background setting, the ρ_eff definition, the grid, the masses, the cosmological inputs and the a₀ footings are CFG123's. A shared definitional error would not be caught.
  - The literature controls come from the model's own authors.
  - The referee is the same kind of model as CFG123's author, so a correlated reasoning error is possible.
  - What is mine: all code, the one-multiplier localisation, both static routes, the background derivation and integrator, the target implementation and the constants.

## Untested (declared)

- CFG123's θ_* headline and the rest of G2; G3, G4 and G5.
- The nonlinear ladder (N1–N3); the Deser–Woodard model; G1-X beyond the h = 2 kpc sphere.
- **The cosmological embedding, at the headline's own order.**
  - Background values and rates (Ū, S̄, U̇, λ̇, H) couple to the local mass at the same relative order, (H0 r)², as the flat-space term.
  - E1 sizes the largest such term at about Ū/2 ≈ 8 times the flat-space one. Its sign is unknown.
  - A frozen-constant static treatment is not consistent. By hand, the Bianchi identity leaves a residual ∝ (m²/3)Ū ∂δU.
  - So the embedding could move the headline by one to two dex, not ten. That is a hand estimate, not a result.
  - The 0.5-dex agreement is therefore a statement inside CFG123's flat-background setting only.
- **The S̄ rescaling of G** (G_eff = G/(1 − m²S̄/3)).
  - It is absorbed into the measured G and gives no density at r > 0 for a point mass.
  - Its time variation is what Lunar Laser Ranging tests. The literature reports the RR model excluded on that ground (Belgacem et al. 2019, abstract read).
  - Not tested here.
- **Homogeneous-solution freedom.** Coefficients of natural size enter ρ_eff only at relative order mr ≤ 7.4e-5 on the grid (hand argument). Larger ones are not tested.
- The static-versus-retarded choice of Green's function for the growing mode at r ≳ 1/m (the grid has mr ≤ 7.4e-5).
- Non-spherical baryons.

## Readings (declared)

- **H1 PASS.** In its own setting, CFG123's headline reproduces. With m fixed by the dark-energy density, the RR model's flat-background weak-field density falls about ten orders short of the target. This checks algebra and arithmetic; it is not new evidence for or against the door.
- **H1 FAIL.** A referee disagreement, kept. R1 and R2 say whether the cause is c1, m, the target or the constants.
- Neither reading says anything about the untested items above.

κ = ½ and Ω_c h² stay fitted. Nothing here says the data favour either model, or that the theory is closed.
