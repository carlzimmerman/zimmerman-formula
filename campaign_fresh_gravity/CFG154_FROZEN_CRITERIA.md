# CFG154 — Referee of CFG122 (door 4, superfluid dark matter): re-deriving the "mass spread 31.6". FROZEN CRITERIA

Written 2026-09-29, before any script or number of this lane. CFG154 re-derives one headline of CFG122 with its own algebra and its own code (the CFG84–86 way). It adds no gate to door 4 and weakens none. A disagreement with CFG122 is a valid result. The ten doors, and CFG122's door, were written knowing CFG44's target. κ = ½ is FITTED. Both a₀ footings are used: 9.3603e-11 and 1.1312e-10 m/s².

## The headline, pinned

CFG122's README, row G1.1a: ρ_DM/ρ_target = R0(M) √(1+x²) with R0 ∝ M^½ (sympy); "mass spread at fixed x 31.62; over x in [0.1, 30] 29.87; line 1.10". Its frozen text: in the gradient-dominated regime the ratio is ∝ r/r_*(m, α) with r_* independent of M_b; the analytic value is (10³)^½ = 31.6.
- ρ_DM is the condensate density on the X < 0 branch where the phonon gradient dominates X, that is |μ − mΦ| ≪ (∇φ)²/2m. There the density is set by Gauss's flux law, not by hydrostatics.
- ρ_target is CFG44's point-mass density ρ_c = a₀/(4πG r √(1+x²)), with x = r/r_M and r_M = √(G M_b/a₀).
- "Mass spread at fixed x" is max/min of the ratio over M_b = 10⁹, 10¹⁰, 10¹¹ and 10¹² M☉, with the same (m, α) and Λ from the a₀ tie.
- "Over x" is max/min of the ratio over x in [0.1, 30] at one mass. I re-derive it too, as a companion.
- A P ∝ ρ³ profile in hydrostatic equilibrium in the combined potential (suggested when this lane was requested) is not where 31.6 lives. It is the opposite limit of the same equations (X > 0, gradient negligible). My solver contains both limits. The P ∝ ρ³ branch is reported apart (R1), because its mass scaling differs.

**Hand derivation** (unscripted; the script's sympy governs). Write Y = μ − mΦ, s = φ′²/2m, X = Y − s, n = P′(X) = Λ(2m)^{3/2} √|X| and ρ_DM = m n.
- Gauss: n φ′ = mαΛ M_b(<r)/(4π r² M_Pl), so s |Y − s| = J² with J = α M_b(<r)/(16π m r² M_Pl). The X < 0 root is s = [Y + √(Y² + 4J²)]/2 (BK 2015 eq. 57, as read).
- Gradient limit, |Y| ≪ J: |X| = J and ρ_DM = 2m²Λ √κ, with κ = 2mJ = α M_b(<r)/(8π M_Pl r²). The phonon force is a_φ = α(Λ/M_Pl) √κ = √(a₀ g_N), with a₀ = α³Λ²/M_Pl.
- At fixed x, κ = α a₀ M_Pl/x² (natural units). So ρ_DM does not depend on M_b, while ρ_target ∝ 1/r_M ∝ M_b^(−½).
- The ratio therefore grows as M_b^½: exponent ½, spread √1000 = 31.623. With the tie, the ratio is ε √(1+x²), where ε ≡ m² r_M/(α M_Pl) = r_M/r_* and r_* = α M_Pl/m². Without the tie the exponent is still ½.
- Over x at one mass: √901/√1.01 = 29.868. So in this regime one mass alone already fails: the best single-mass error is (b − a)/(b + a) = 0.935, with a = √1.01 and b = √901.
- CFG44's exponential spheres with h a fixed multiple of r_M (CFG122 used h = 0.3 r_M and 3 r_M): the ratio is ε ũ(x)/√f(x), with f = M_b(<r)/M_b and ũ the target's M_tot(<r)/M_b. Same exponent, same 31.623. It would differ for h fixed in kpc.
- Side remark: the gate's 10% band allows a max/min of 1.1/0.9 = 1.222, looser than G1.1a's 1.10. No verdict turns on it.

## What I read, and what I did not

Read, for this file:
- CFG122_FROZEN_CRITERIA.md and CFG122_door4_superfluid/README.md, in full. They hold the model, the answer (31.62, 29.87, R0(M) √(1+x²)) and its hand derivation. The README also told me that CFG122 scans Y0 on 27 values and neglects the cold mass inside 0.1 r_M.
- closure_map/TEN_DOORS_GATES_2026-09-29.md; CFG44_fluid_target/README.md; the docstrings only of CFG44_fluid_target/Bcommon.py (pulled out with Python's ast, so no function body was read); CFG118_FROZEN_CRITERIA.md (style). A file listing and a search for "CFG15x" (no hits) confirmed the lane number was free.
- Literature, as arXiv abstract pages and ar5iv HTML renderings, read through a fetch tool that returns quoted equations. Every transcription below is unverified against the PDFs.
  - L. Berezhiani & J. Khoury, "Theory of dark matter superfluidity", Phys. Rev. D 92, 103510 (2015), arXiv:1507.01019: abstract; eqs. 4, 25, 26, 30, 39, 44, 45, 51, 52, 57, 60, 64, 67, 68, 74–76.
  - L. Berezhiani & J. Khoury, "Dark matter superfluidity and galactic dynamics", Phys. Lett. B (2016), doi:10.1016/j.physletb.2015.12.054, arXiv:1506.07877: abstract only.
  - L. Berezhiani, B. Famaey & J. Khoury, "Phenomenological consequences of superfluid dark matter with baryon-phonon coupling", JCAP 09 (2018) 021, arXiv:1711.05748: abstract; eqs. 3, 13, 33–35, 38, 42, 43.
- What the papers say, as read:
  - CFG122's frozen model is BK's zero-temperature model. These all match it: P(X) = (2Λ(2m)^{3/2}/3) X√|X| (eq. 25); the coupling −αΛθρ_b/M_Pl (26); ∇·(√(2m|X|) ∇φ) = αρ_b/2M_Pl (51) with κ = α M_b(r)/(8π M_Pl r²) (52); the X < 0 root (57); α^{3/2}Λ = √(a₀ M_Pl) (60); P = ρ³/(12Λ²m⁶) (30).
  - BK's MOND-regime density, ρ_DM ≃ 2m²Λ √(β−1) √κ(r) (75, after a finite-temperature substitution Λ → √(β−1)Λ), has the same √M_b(<r)/r form.
  - Their eq. 76 puts the condensate's own pull against the phonon force at ∝ m² r/(α M_Pl), independent of M_b. That is the published form of the universal length r_*.
  - BK's galaxy fits (BFK 2018) use a finite-temperature Lagrangian X√|X − βY| with β = 2 (their eq. 13). Its density (their eq. 33) mixes μ − mΦ and gradient terms. That is not CFG122's model; only one symbolic row (R3) touches it.

Not read: any CFG122 script, .out, .json or .npz (until my own outputs are saved, in stage 2); CFG44's code bodies and outputs; superfluid_2026/, the pricing script, CFG84–86 and every other lane.

## Method

The scripts are self-contained; nothing is imported from the repository. Directory CFG154_door4_superfluid_referee/:
- cfg154_common.py: the two solvers and the target;
- cfg154_headline.py: H1, C1–C3, C5a, R1, R3, R4; MUTATE=1 runs the MUTATE;
- cfg154_plane.py: H2, R2, R5, C4, C5b, C6.
Each writes .out and _results.json next to itself. The MUTATE writes separate _MUTATE files.

**A. Symbolic (sympy, my own).**
- S1: the static radial Euler–Lagrange equation for φ from r²[P(X) − α(Λ/M_Pl) φ ρ_b], and its Gauss first integral.
- S2: the three roots of s|Y − s| = J², and eq. 57 (as read) as the X < 0 root.
- S3: the gradient limit: ρ_DM = 2m²Λ√κ; a_φ = √(a₀ g_N); the factor N_a in a₀ = N_a α³Λ²/M_Pl.
- S4: the ratio with and without the tie; ∂ln R/∂ln M_b at fixed x; the exact spread over 10⁹–10¹²; the exact x-spread; the single-mass minimax.
- S5: the same for a self-similar extended profile, with f(x) and ũ(x) symbolic.
- S6: the reduction used in C. In x, ŷ = Y/J_M and μ = M_DM/M_b (J_M is the point mass's J at r_M), and given the tie, the system depends on (m, α, M_b, a₀) only through ε.
- S7: K = 1/(12Λ²m⁶), and the Lane–Emden n = ½ scale a of the X > 0, gradient-free branch.

**B. Radial solver (physical units).**
- Natural units (eV). CODATA ħ, c, e and G; M_Pl = √(ħc/8πG) from G; M☉ from GM☉ = 1.3271244e20 m³/s² (IAU nominal).
- Along r it carries M_b(<r) (integrated from ρ_b, not taken from its closed form), M_DM(<r) and Y(r).
- At each r, the branch root comes from bracketed root finding (brentq), solved for |X| directly to avoid cancellation. Then ρ_DM = mΛ(2m)^{3/2} √|X|.
- dM_DM/dr = 4πr²ρ_DM and dY/dr = −mG(M_b + M_DM)/r², integrated with solve_ivp (DOP853, rtol 1e-10) in ln r.
- Start at r_in = 10⁻³ r_M with M_DM = 0 and Y = −mΦ_b(r_in), Φ_b(∞) = 0 (μ = 0 against the baryons' potential).
- The target is my own integration of CFG44's closure w′ = a₀ r u_N/u (u = u_N + w, w = G M_c), in SI. Near a sphere's centre, w ≈ √(a₀ G M_b r⁵/(15 h³)).
- Evaluation: 200 log points in x ∈ [0.1, 30]. R(x) = ρ_DM/ρ_target; S(x) = max/min of R over the four masses; p(x) = least-squares slope of ln R on ln M_b.
- **Headline cell (declared):** m = 10⁻³ eV, α = 10, Λ from the tie, the X < 0 branch. Point mass and spheres with h = 0.3 r_M and 3 r_M; both footings. It is chosen so that the gradient dominates everywhere in range (hand estimate: |Y|/J ≤ 2e-4).
- **Precondition P1:** max |Y|/J ≤ 1e-2 over the range at every mass, geometry and footing. If P1 fails, H1b is void and the cell is not re-picked.

**C. Secondary check: G1.1 on a coarse plane (my grid, my search).** It is run because the reduction S6 makes it cheap.
- Point mass only; G1.2's spheres are not searched.
- The dimensionless system: ĵ = 1/x²; dŷ/dx = −2ε(1 + μ)/x²; dμ/dx = ε x² √|x̂|; R = ε x √(1+x²) √|x̂|.
- By S6, for the point mass with the tie the (m, α) plane is one-dimensional in ε₀ ∝ m²/α, if G1.1 has no other dependence on m or α.
- Three branches, with no switching between them. The labels are mine; I do not assume they match CFG122's B−, B+hi and B+lo.
  - B−: x̂ = [ŷ − √(ŷ² + 4ĵ²)]/2 < 0. It always exists.
  - B+a: x̂ = [ŷ + √(ŷ² − 4ĵ²)]/2 > 0 (the P ∝ ρ³-like root).
  - B+b: x̂ = [ŷ − √(ŷ² − 4ĵ²)]/2 > 0.
  - The B+ roots exist only while ŷ ≥ 2ĵ. The first x where that fails is x_edge.
- The per-halo constant is ŷ(0.1), free for each mass (equivalent to μ). Integration starts at x = 0.1 with μ = 0, so the cold mass inside 0.1 r_M is neglected (R5 tests this).
- Vectorised fixed-step RK4 in ln x, 1194 steps; the 200 evaluation points are every sixth node. Stable root forms avoid cancellation.
- Error E = max over [0.1, min(30, x_edge)] of |R − 1|. If x_edge < 3, the solution fails (CFG122's coverage rule).
- The search over ŷ(0.1) has two stages:
  - the grid {0} ∪ {±10^(k/10): k = −40, …, 110} (303 values);
  - around each of the three lowest local minima, 41 points uniform in log|ŷ| (linear around 0) between its two grid neighbours.
  - E*(ε) is the lowest E over both stages and all three branches.
- The plane: m ∈ {10⁻³, 10^−2.5, …, 10³} eV × α ∈ {10⁻², 10^−1.5, …, 10²}, so 13 × 9 = 117 cells per footing. A cell maps to ε₀ = m² r_M(10⁹ M☉)/(α M_Pl), and its four masses to ε₀ × {1, 10^½, 10, 10^{3/2}}. On this grid log ε falls on a 0.5-dex lattice, about 36 values per footing.
- A cell passes iff E* ≤ 0.10 at all four masses. A value within 0.005 of 0.10 is flagged "marginal", not decided.
- Cost: about 430 values of ε × 3 branches × ~430 trajectories, vectorised. Minutes.

## Checks

**Controls.** A failed control is kept and disclosed, and its script exits 1.
- **C1 [Lane–Emden, n = ½].** n = ½ has no elementary closed form (only n = 0, 1 and 5 have one), so the control has four parts.
  - (a) My Lane–Emden integrator (the RK4 routine of C) against θ = 1 − ξ²/6, sin ξ/ξ and (1 + ξ²/3)^(−½): to 1e-8 on [0, min(ξ₁, 10)].
  - (b) n = ½ against an independent reference: sympy's exact central series (to ξ¹⁶) up to ξ = 0.5, continued by mpmath's arbitrary-precision Taylor integrator. Agreement to 1e-8 in θ on [0.5, 2.7], and to 1e-6 in ξ₁.
  - (c) Solver B in its X > 0 branch, with the flux off and no baryons (m = 1 eV, Λ = 1 meV set directly, not from the tie), reproduces θ(r/a) of (b) to 1e-6 on [0, 0.99 ξ₁], with a from S7. The homology slope d ln R/d ln M between Y_c = 10⁻⁷ and 1.6 × 10⁻⁶ eV is 1/5 to 1e-4.
  - (d) S7's K = 1/(12Λ²m⁶) (BK eq. 30, as read).
  - Reported only: ξ₁ and −ξ₁²θ′(ξ₁) beside the recalled table values, about 2.7527 and 3.787 (from memory, unverified).
- **C2 [the target reproduces its own identities].**
  - Point mass: M_c = M_b(√(1+x²) − 1), ρ_c (from the closure at the integrated M_c) and g_tot = √(g_N² + a₀ g_N) match their closed forms to 1e-8.
  - All three geometries: C(r) = ρ_c r³ g_tot equals (a₀/4π) M_b(<r) to 1e-5, with ρ_c taken from a spline derivative of M_c instead.
  - The spheres' numerical M_b(<r) matches M_b[1 − (1 + s + s²/2)e^(−s)] to 1e-9 for x ≥ 0.1. Both footings.
- **C3 [the tie].** At the headline cell, a_φ = α(Λ/M_Pl) φ′ equals √(a₀ g_N) to 1e-4 for the point mass. This checks N_a and the unit conversions.
- **C4 [the reduction].** Solver B (physical units, brentq, solve_ivp) and solver C (closed-form roots, RK4) give the same R(x) to 1e-6 over [0.1, min(30, 0.9 x_edge)].
  - Cells (m, α) = (1 eV, 1), (0.1 eV, 10) and (10 eV, 0.1); four masses.
  - B− with ŷ(0.1) = 1; B+a with ŷ(0.1) = 10³ + 40ε; both start at 0.1 r_M with no inner cold mass.
  - If C4 fails, H2, R2, R4 and R5 are void.
- **C5 [resolution].** (a) H1: rtol 1e-8 instead of 1e-10 changes R by ≤ 1e-6. (b) H2: each ε's best solution, re-run with twice the steps, changes E by ≤ 1e-3.
- **C6 [the search can find a known answer].** Replace the target by solver C's own B− solution at ε = 1 with ŷ(0.1) = 10^0.568 (off the grid). The search must return E* ≤ 0.005.

**H1 [HEADLINE; the MUTATE must change it].**
- H1a (symbolic): ∂ln R/∂ln M_b at fixed x = ½ exactly, with and without the tie. The spread is exactly √1000, and the x-spread exactly √(901/1.01).
- H1b (numeric): at the headline cell, with P1 met, |S(x)/31.623 − 1| ≤ 0.02 and |p(x) − ½| ≤ 0.01 at all 200 points. Point mass and both spheres, both footings.
- H1c (numeric, point mass): max/min of R over x ∈ [0.1, 30] is within 2% of 29.868 at each mass, both footings.
- cfg154_headline.py exits 0 iff H1a–c and its controls pass. The door's own line is then read off: G1.1a needs S ≤ 1.10.

**H2 [SECONDARY].** AGREE with CFG122 iff no cell passes on either footing. It is reported with the best worst-mass error over cells (CFG122 printed 0.896 / 0.894 on its finer plane). cfg154_plane.py exits 1 on DISAGREE or on a failed control, and says which.

## MUTATE

MUTATE=1 lets α scale with the baryon mass as the target would need: α(M_b) = 10 (M_b/10¹² M☉)^½, with m = 10⁻³ eV and Λ from the tie at each mass. α then runs from 0.32 to 10, inside the plane, and ε is the same at every mass.
- The spread must collapse to 1 (to 1e-6) and p to 0. H1b then fails and the script exits 1.
- The same substitution in S4 must give an exponent of 0. H1c (the x-shape) should not move.
- If the spread does not collapse, the control failed. That is disclosed, and H1b is declared uninformative.

## Reported rows (no pass line; never pooled with H1)

- **R1 [the P ∝ ρ³ branch].** X > 0 with the gradient dropped, in the baryonic point-mass potential, μ = 0, self-gravity off: ρ_DM ∝ √(mGM_b/r). Hand value: R ∝ M_b^{3/4} at fixed x, spread 1000^{3/4} = 177.8, the same for any condensate edge placed at a fixed x. Symbolic, and numeric with solver B (headline cell, flux off). With self-gravity this branch becomes BK's Lane–Emden core, with radius ∝ M_DM^{1/5}; that is not evaluated.
- **R2 [is the spread the reason?].** E*(ε) on a 0.05-dex line over log ε ∈ [−9.5, 8.5], per branch and overall. It says whether even one mass can be fitted, at any (m, α).
- **R3 [BK's finite-temperature model, symbolic].** From P = (2Λ(2m)^{3/2}/3) X√|X − βY| with static Y = μ − mΦ (BFK eq. 13, as read), n = ∂P/∂μ should reproduce BFK eq. 33 (as read). Its gradient limit is then (3 − β)/3 of the zero-temperature density, so the M_b exponent does not change. A mismatch would be a transcription question; no verdict uses R3.
- **R4 [how far 31.6 holds].** B−, point mass, μ = 0 (ŷ(0.1) = 20ε), self-gravity on. S at x = 0.1, 1, 10 and 30 for ε₀ = 10⁻⁸, 10⁻⁶, 10⁻⁴, 10⁻², 1 and 10².
- **R5 [H2 sensitivity].** E* at the lattice points with μ(0.1) = 0.01 instead of 0.

## Readings (declared)

- **H1 reproduced:** CFG122's 31.62 and 29.87 stand. In the gradient regime the condensate density at fixed x does not depend on M_b, while the target's falls as M_b^(−½). G1.1a FAILS for the door, as CFG122 found.
- **H1 not reproduced:** my number is reported beside CFG122's. Nothing is re-tuned.
- **H2:** AGREE means consistent with CFG122's 0/3600 on a coarser grid with my own search. DISAGREE means the passing cells are listed and the cause is traced in stage 2 against CFG122's scripts.
- **R2**, read in this order:
  - (i) E* > 0.10 for every ε: no single mass can be fitted at any (m, α). The G1.1 FAIL does not need the mass spread; 31.6 is a second, separate failure.
  - (ii) Some single masses pass, but no ε₀ passes at all four of ε₀ × {1, 10^½, 10, 10^{3/2}}: the mass spread decides.
  - (iii) Some ε₀ passes at all four: that predicts passing cells (compare H2).
- Whatever the numbers: CFG122's own G1.1a row also prints the x-spread 29.87, so in the gradient regime one mass already fails (best error 0.935). There, "no single (m, α) serves all masses" describes the mass direction only.

## Where independence stops

- The model is CFG122's frozen model: P ∝ X^{3/2}, the linear coupling, the static spherical non-relativistic reduction, the tie with N_a derived, a per-halo μ. I did not choose it. I checked it only against BK 2015 and BFK 2018 as read, at the level of transcribed equations.
- I read CFG122's numbers and formula before deriving them, and H1's pass lines are set to reproduce them. This is a reproduction with my own algebra and code, not a blind derivation.
- The target is CFG44's, from its README and docstrings. The implementation is mine.
- The gate conventions are CFG122's and the gates file's: x ∈ [0.1, 30] on 200 log points, the four masses, max|R − 1| against 10%, x_edge ≥ 3, both footings.
- The secondary check's branch set, no-switching rule, per-halo parametrisation, missing thermal edge, inner-mass neglect and search grids are mine. They were set without reading CFG122's code, but knowing its README (a 27-value Y0 grid; the cold mass inside 0.1 r_M neglected). A disagreement may come from these choices.
- The reduction to ε is my own; C4 tests it.
- CFG122's scripts and outputs are opened only in stage 2, after my outputs are saved. A script changed after its first run keeps that output as *_FIRSTRUN.out, and the change is disclosed.

## Untested (declared)

- BK's finite-temperature model as a whole: BFK 2018's fits, β = 2, their eq. 33 density with both terms, their boundary conditions and NFW envelope. Only R3's gradient-limit factor is checked.
- The thermal phase boundary (T = T_c(n)) and any edge other than a lost static root. H2 has no thermal edge, which makes it more permissive.
- G1.2 (the spheres) in the plane search. Spheres with h fixed in kpc, where the spread at fixed x is not exactly √1000.
- CFG122's other gates: G1.3–G1.6, G2–G6 and Branch F. The stability of the X < 0 branch (BK note a wrong-sign kinetic term for X < 0 at zero temperature, in their text after eq. 62; CFG122's G5.1).
- Branch switching at folds, time dependence, a relativistic completion and non-spherical baryons.

## Expected outcome (stated before running; hand estimates, may be wrong)

- H1a–c PASS (~97%). I read the answer before deriving it, and my hand algebra agrees. The risk is a slip in a printed number.
- The MUTATE collapses the spread to 1 (~98%).
- H2: 0 cells on both footings (~85%).
- R2: reading (i) (~65%). Unscripted orientation: on B−, fitting the outer 1/r² part needs ε ≳ 10, to keep μ − mΦ nearly constant against the cold mass's own potential, and the inner part then overshoots by 2–5×. Fitting the inner part (ε ≈ 1) leaves the outer part off, as the 29.87 shows.
- R4: S falls from 31.6 toward ~1000^{1/4} = 5.6 as μ − mΦ takes over the outer region (hand estimate, self-gravity off).
- R3: BFK eq. 33 is reproduced; at β = 2 the factor is 1/3.

κ = ½ and Ω_c h² stay fitted. Nothing here says the data favour either model, or that the theory is closed.
