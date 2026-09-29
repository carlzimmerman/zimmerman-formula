# CFG154 — Referee of CFG122 (door 4, superfluid dark matter): the "mass spread 31.6", re-derived

- **Criteria:** frozen in `../CFG154_FROZEN_CRITERIA.md` (71a12f17d; sha256 7b58a921…a07d60, printed first in every output), before any code. It was written after reading only CFG122's frozen criteria and README, CFG44's README and `Bcommon.py` docstrings, the ten-doors gates file and the cited literature pages.
- **Scripts.** They are self-contained: nothing is imported from the repository.
  - `cfg154_common.py`: two solvers of the static equations, and my own integration of CFG44's target.
  - `cfg154_headline.py`: H1, C1–C3, C5a, R1, R3 and R4. `MUTATE=1` runs the MUTATE.
  - `cfg154_plane.py`: H2, R2, R5, C4, C5b and C6.
  - Post hoc, labelled, written after the frozen runs:
    - `cfg154_plane_POSTHOC.py` asks why C4 and C5b missed.
    - `cfg154_compare_POSTHOC.py` compares with CFG122's code and saved arrays. It reads `../CFG122_door4_superfluid/cfg122_g1_plane_arrays.npz` read-only.
- **Runs.** Each takes seconds to under a minute.
  - Headline, main: 21 of 21 checks pass; exit 0.
  - Headline, MUTATE: H1b fails, as intended; the spread collapses to 1 (to 1.4 × 10⁻¹³); exit 1.
  - Plane: exit 1. C4 and C5b fail as frozen, C6 passes, and H2 agrees with CFG122. By the frozen rule, C4's miss voids H2, R2, R4 and R5.
  - The two post-hoc scripts have no pass lines and exit 0.

## Bottom line

**CFG122's 31.62 is reproduced exactly, and so is its companion 29.87.**
- **The mechanism.** In the gradient-dominated branch (X < 0, |μ − mΦ| ≪ (∇φ)²/2m), Gauss's flux law fixes the condensate density at ρ_DM = 2m²Λ√κ, with κ = αM_b(<r)/(8πM_Pl r²).
  - At fixed x = r/r_M, κ = α a₀ M_Pl/x², so ρ_DM does not depend on M_b. The target's density falls as M_b^(−½).
  - The ratio is therefore ε√(1+x²) for a point mass, with ε = m²r_M/(αM_Pl) = r_M/r_* and r_* = αM_Pl/m².
  - Its mass exponent at fixed x is exactly ½ (with or without the a₀ tie). Over 10⁹–10¹² M☉ the spread is √1000 = 31.6228.
  - My radial solver of the full coupled equations gives 31.6217–31.6228 and an exponent of 0.500000 ± 5 × 10⁻⁶. That holds for the point mass and both self-similar spheres, on both footings.
- **The door fails G1.1a,** as CFG122 found: 31.6 against a 1.10 line.
- **The x-spread at one mass is √(901/1.01) = 29.8677,** matching CFG122's 29.87.
- **The 31.6 is not a P ∝ ρ³ number.** The hydrostatic P ∝ ρ³ branch gives a mass exponent of ¾ and a spread of 177.83 (R1).

**The two questions asked of this referee.**
1. **Does CFG122's G1.1 depend on (m, α) only through ε₀?** Almost, but not quite.
   - **Its model part reduces to ε₀.** That covers the equations, the tie, a per-halo grid in units of mGM/r_M started at 0.1 r_M, and RK4 in ln r.
   - **Its coverage rule does not reduce.** A node counts only if the condensate density n ≥ n_c(m, σ²), a thermal phase boundary with its own m dependence.
   - **So the 60 × 60 plane holds 237 distinct ε₀ values, not 36.** 36 is my own coarse grid's count per footing. The thermal edge then splits some of the 237 groups.
   - **CFG122's own saved arrays confirm this (Q1).** Wherever the edge does not cut the best solution, cells with the same ε₀ have identical best errors. The edge splits 73–79 of the 158–186 verdict-relevant groups per mass. About 18% of cells have their best solution cut by the edge.
   - **So "0 of 3600" is about 237 ε₀ values, partly split by an m-dependent edge.** It is not 3600 independent tests.
   - **The verdict does not depend on the edge.** Scored only over [0.1, 3], the shortest range any edge allows, the best single-mass error is still 0.191 (Q3). So no placement of the edge can make even one mass pass.
2. **Mass spread, radial shape, or both?** Both. Each alone is enough to fail.
   - **The gradient regime (frozen, valid):** the ratio ε√(1+x²) fails across masses (31.6) and across radius (29.87). No choice of ε brings one mass below an error of 0.935 (reached at ε = 0.0645).
   - **The radial shape fails every mass, even in the full solution.** With μ free per galaxy and all three branches, no single mass comes within 10% at any ε. The best is 0.416 at ε ≈ 1.4 (R2), and 0.191 even on [0.1, 3] (Q3).
   - **The mass spread then adds to that.** One common (m, α) raises the best worst-mass error to 0.81 (H2; CFG122 found 0.896).
   - **Frozen status:** R2 and H2 are void, because C4 missed. The post-hoc runs show their numbers do not move by more than 5 × 10⁻¹³ where they decide anything.

**One discrepancy with CFG122, which does not change any verdict.**
- **CFG122's per-mass closest approaches are limited by its per-halo grid.** Those are 0.805–0.818, from a 27-value grid (Y0 = 0, ±10^k mGM/r_M).
- **My solver on the same 27 values gives 0.812 (Q2).** My finer search reaches 0.416, at Y0 = 12.7 mGM/r_M, which falls between CFG122's grid points 10 and 100.
- **The closest-approach rows therefore understate how close one galaxy can get.** They do not change "no cell passes".

## Comparison with CFG122

| item | CFG122 | CFG154 | agree? |
|---|---|---|---|
| ratio in the gradient regime, point mass | R0(M)√(1+x²), R0 = √2 Λ√M √α m²/(4√π M_Pl^{5/2} a₀) (sympy) | the same sympy expression; with the tie, ε√(1+x²) | yes |
| mass exponent at fixed x | ½ | ½ exactly (sympy); 0.500000 ± 5 × 10⁻⁶ (solver, 3 geometries × 2 footings) | yes |
| mass spread, 10⁹–10¹² M☉ | 31.62 | √1000 = 31.6228 (solver: 31.6217–31.6228) | yes |
| x-spread at one mass | 29.87 | √(901/1.01) = 29.8677 (solver: 29.86758–29.86769) | yes |
| universal length | r_* = M_Pl^{3/2}√a₀/(Λ√α m²) | αM_Pl/m², the same under the tie | yes |
| G1.1a door verdict (line 1.10) | FAIL | FAIL | yes |
| N_a in a₀ = N_a α³Λ²/M_Pl | 1 | 1 | yes |
| K in P = Kρ³ | 1/(12 m⁶Λ²) | 1/(12 Λ²m⁶) | yes |
| n = ½ Lane–Emden | M–R exponent 0.20000 (internal check) | ξ₁ = 2.75269805, −ξ₁²θ′(ξ₁) = 3.78865; my solver reproduces θ to 5 × 10⁻⁹; slope 0.20000000 | consistent |
| target identities | S0.5 PASS | C2 PASS (≤ 4 × 10⁻¹² relative) | yes |
| G1.1 plane: cells passing | 0/3600, both footings | 0/117, both footings (void by the frozen C4 rule) | yes |
| best worst-mass error | 0.896 / 0.894 | 0.812 / 0.810 | differ: per-halo grid (Q2) |
| best single-mass error | 0.805–0.818 | 0.416 at ε = 1.41 | differ: per-halo grid (Q2) |
| G1.1 depends on (m, α) only via ε₀ | not stated | no: the thermal coverage rule adds an m dependence (Q1) | new |
| MUTATE | MUTATE=a (target := own gradient density): G1.1 flips to PASS | α ∝ M_b^½ collapses the spread to 1 | both informative |

## The headline (H1)

- **H1a, symbolic: PASS.** I derived these with sympy from the Lagrangian as frozen in CFG122:
  - the Euler–Lagrange equation for φ (both signs of X) and its Gauss first integral;
  - the three roots of s|Y − s| = J². BK 2015 eq. 57 (as read) is the X < 0 root;
  - the gradient limit ρ_DM = 2m²Λ√κ and a_φ = √(a₀g_N), with N_a = 1;
  - the ratio above. d ln R/d ln M_b at fixed x is ½ (tie) and ½ (no tie). The spread is exactly 10√10 and the x-spread exactly 10√91001/101;
  - the same exponent for any self-similar extended profile (R = ε ũ/√f);
  - the reduction to ε (S6).
- **H1b, numeric: PASS.** At the headline cell, m = 10⁻³ eV and α = 10 (ε = 7.1 × 10⁻⁹ to 2.5 × 10⁻⁷):
  - max |S(x)/√1000 − 1| = 3.3 × 10⁻⁵;
  - max |p(x) − ½| = 4.6 × 10⁻⁶.
  - This holds at all 200 x, for the point mass and the spheres with h = 0.3 r_M and 3 r_M, on both footings.
  - The numeric R(x = 0.1)/√1.01 equals ε to five digits.
- **H1c, numeric: PASS.** The point-mass x-spread is 29.86758–29.86769 at the four masses and both footings, against 29.86770.
- **P1 precondition: PASS.** max |Y|/J = 1.4 × 10⁻⁴, against the 10⁻² line.

## Controls (failed ones kept)

- **C1 Lane–Emden: PASS, all parts.**
  - (a) My RK4 reproduces the n = 0, 1 and 5 closed forms to 1.3 × 10⁻¹⁴.
  - (b) For n = ½, sympy's exact central series (1, −1/6, 1/240, 1/30240, 1/725760, …) continued by mpmath at 30 digits agrees with my RK4 to 1.9 × 10⁻¹⁴ on [0.5, 2.7]. ξ₁ agrees to 4 × 10⁻¹⁴.
  - (c) My physical-unit solver, in its X > 0 branch with the flux off and no baryons, reproduces θ(r/a) to 5.0 × 10⁻⁹ on [0, 0.99 ξ₁]. The homology slope is 0.20000000.
  - (d) K = 1/(12Λ²m⁶).
- **C2 target identities: PASS.**
  - Point mass: M_c, ρ_c and g_tot = √(g_N² + a₀g_N) to 4.0 × 10⁻¹².
  - C(r) = (a₀/4π)M_b(<r) to 5.9 × 10⁻¹⁰, with ρ_c from a spline derivative.
  - The spheres' integrated M_b(<r) to 4.0 × 10⁻¹¹ (target solver) and 2.4 × 10⁻¹⁰ (radial solver).
- **C3 the tie: PASS.** a_φ = √(a₀g_N) to 3.7 × 10⁻⁶.
- **C5a resolution: PASS.** R moves by 1.2 × 10⁻⁸.
- **C6 search positive control: PASS.** E* = 5.9 × 10⁻⁴; ŷ(0.1) was found at 3.7154 against the true 3.6983.
- **C4 the reduction: FAIL as frozen.**
  - The miss is 6.65 × 10⁻⁶ against the 10⁻⁶ line, in one of 23 compared runs: m = 10 eV, α = 0.1, M_b = 10¹² M☉, ε = 2478, B−.
  - The other 22 runs agree to ≤ 1.9 × 10⁻⁷, most to 10⁻⁹–10⁻¹². One B+a run could not be compared, because its fold lies inside 0.111 r_M.
  - By the frozen rule, **H2, R2, R4 and R5 are void**.
  - Post hoc (P1): the gap is RK4 truncation in the dimensionless solver on a runaway solution (R up to 1.2 × 10¹⁵). It falls 6.65 × 10⁻⁶ → 8.1 × 10⁻⁷ → 5.6 × 10⁻⁸ → 3.6 × 10⁻⁹ as the step halves, the 4th-order signature. The physical-unit solver moves by 4 × 10⁻¹⁰ between rtol 10⁻¹⁰ and 10⁻¹².
- **C5b resolution of the search: FAIL as frozen.**
  - max |ΔE| = 2.0 × 10²⁵. It fails at 16 of 433 ε, all with log ε ≥ 7.89, where E* ≥ 3.7 × 10²⁸ (runaway solutions).
  - Post hoc (P2): wherever E* < 2, |ΔE| ≤ 5.2 × 10⁻¹³.
- **MUTATE: the control works.**
  - α(M_b) = 10(M_b/10¹² M☉)^½ collapses S to 1 within 1.4 × 10⁻¹³ and p to 0 within 6 × 10⁻¹⁵. The sympy exponent becomes 0.
  - H1b fails and the run exits 1. H1c does not move. The door's own G1.1a line would then pass (spread 1.000000), while the x-shape (29.87) still fails.

## Reported rows (no pass line)

- **R1, the P ∝ ρ³ branch:** X = Y in the baryonic point-mass potential, μ = 0, self-gravity off.
  - The exponent is exactly ¾ (also with an edge at fixed x), and the spread is 1000^¾ = 177.828.
  - The solver gives 177.82794 and p = 0.7500000.
- **R2, E*(ε) (void as frozen):** the reading is (i). No ε gives E* ≤ 0.10; the smallest single-mass E* is 0.4160, at ε = 1.41 (B−, ŷ(0.1) = 35.9).
  - Per branch: B− 0.416, B+b 0.807, B+a 0.9998.
  - A post-hoc reading of the two plateaus:
    - at small ε, E* → 0.9998, the minimax error of the shape x√(1+x²) left by a large negative μ − mΦ;
    - at large ε, E* → 0.8190, the minimax of √(1+x²)/x, the shape when μ − mΦ dominates. That is where CFG122's 0.81 sits.
  - Above log ε ≈ 5, E* rises above the plateau because the search grid's edge (ŷ ≤ 10¹¹) binds. Verdicts are unaffected.
- **R3, BK's finite-temperature model (symbolic, as read):**
  - m ∂P/∂μ from BFK eq. 13 reproduces BFK eq. 33, and the phonon current reproduces eq. 35.
  - The gradient-limit density is (1 − β/3) of the zero-temperature one, 1/3 at β = 2. The M_b exponent, and so the 31.6, is unchanged.
- **R4, how far 31.6 holds (void as frozen):** B−, point mass, μ = 0, self-gravity on.

| ε₀ | S(x = 0.1) | S(1) | S(10) | S(30) |
|---|---|---|---|---|
| 10⁻⁸ | 31.6228 | 31.6228 | 31.6227 | 31.6226 |
| 10⁻⁶ | 31.6227 | 31.6223 | 31.6179 | 31.6085 |
| 10⁻⁴ | 31.6179 | 31.5745 | 31.2183 | 32.2754 |
| 10⁻² | 31.1424 | 27.7029 | 498.19 | 6005.9 |
| 1 | 13.060 | 2020.4 | 27071 | 30445 |
| 10² | 5.630 | 44644 | 32062 | 31727 |

  - So 31.6 holds (within 2%) only while the Bernoulli term stays small, ε₀ ≲ 10⁻⁴.
- **R5, the neglected inner cold mass (void as frozen):** with μ(0.1) = 0.01, no cell verdict changes. The largest |ΔE*| (3.6 × 10²³) is in runaway cells only.

## Post hoc (labelled; not frozen; nothing re-pinned)

- **P1 and P2:** see C4 and C5b above.
- **P3:** the lattice search repeated at twice the steps.
  - No cell verdict changes; the best worst-mass errors stay 0.8118 and 0.8102.
  - The R2 minimum is 0.41598 at ε = 1.4125 at both resolutions (|ΔE*| ≤ 5.2 × 10⁻¹³).
- **Q1, CFG122's arrays against ε₀:**
  - There are 237 distinct ε₀ values, 231 of them shared by more than one cell.
  - Among same-ε₀ groups whose best solutions all reach x = 30 (no edge), every group with an error below 2 is identical. The groups that differ all have errors of 10¹⁷–10²⁹ (runaway, rounding-amplified).
  - Every verdict-relevant group that differs also differs in the thermal edge of its best solution.
  - **Example** (canonical, 10⁹ M☉, ε₀ = 6.2):
    - the best error is 0.8134 for every m ≤ 7.3 eV (edge at x = 30);
    - it drops to 0.8086 as the edge moves in to x = 4.2 (m = 23.6 eV);
    - from m ≈ 30 eV that branch's edge falls below 3, and the best becomes 2794 on B+hi.
- **Q2:** CFG122's 27-value per-halo grid, run in my solver without the edge, gives 0.8118 (ε = 6.31, B+b, Y0 = 100 mGM/r_M). CFG122 printed 0.805–0.818.
- **Q3:** the best single-mass error over [0.1, 3] is 0.1914 (ε = 1.26, B−). No ε reaches 0.10. This bounds G1.1 from below for any edge with x_edge ≥ 3.

## Where the pre-run expectations were wrong

- **R4:** I expected S to fall toward 1000^¼ = 5.6 as μ − mΦ takes over. That held only at x = 0.1 (5.63 at ε₀ = 10²).
  - At x ≥ 1 the spread grows to 10³–4.5 × 10⁴ once ε₀ ≳ 10⁻².
  - There the condensate's own gravity drives μ − mΦ negative, and the density grows as √|μ − mΦ|, faster for larger ε. My hand estimate had self-gravity off.
- **C4 and C5b** were expected to pass. Both missed, on runaway solutions at the largest ε.
- **My spec said H2's missing thermal edge makes it "more permissive".** That is only half right: an edge at x_edge ≥ 3 also shortens the scored range. Q3 bounds this: even the shortest allowed range cannot be passed.
- **R2, orientation:** I expected the best single mass to sit between ε ≈ 1 and ε ≳ 10. It sits at ε = 1.41 with E* = 0.416.
- **R2 and H2 priors held,** though both are void as frozen.
- **The recalled Lane–Emden values:** ξ₁ "about 2.7527" is 2.75269805. −ξ₁²θ′ "about 3.787" is 3.78865, so the recollection was 0.04% off (no pass line).

## Where independence stops

- **The model is CFG122's frozen model,** not my choice: P ∝ X^{3/2}, the linear coupling, the static spherical non-relativistic reduction, the a₀ tie and a per-halo μ.
  - I checked it against Berezhiani & Khoury 2015 (arXiv:1507.01019) and Berezhiani, Famaey & Khoury 2018 (arXiv:1711.05748), as read. I read ar5iv HTML through a fetch tool that returns quoted equations; the transcriptions are unverified against the PDFs.
  - All the checked equations match (eqs. 25, 26, 30, 51, 52, 57, 60). BK's MOND-regime density (eq. 75) has the same √M_b(<r)/r form.
- **I read CFG122's numbers and formula before deriving them.**
  - The H1 pass lines reproduce them. This is a reproduction with my own algebra and code, not a blind derivation.
  - The sympy ratio agrees symbol for symbol because both derivations start from the same frozen formulas. That is agreement of algebra from shared premises, not independent physics.
- **The target is CFG44's,** from its README and docstrings; the implementation is mine. The gate conventions are CFG122's and the gates file's.
- **CFG122's code was opened only after my frozen runs were saved.**
  - It uses the same equations as mine: the flux law with Λ cancelled, the same three roots, Y0 in units of mGM/r_M at 0.1 r_M, M_DM = 0 there, and RK4 in ln r with N = 160.
  - The one difference is its thermal coverage rule n ≥ n_c(m, σ²), which my frozen H2 does not include.
- **Both post-hoc scripts were written after reading CFG122's code;** the comparison script reads CFG122's arrays.

## Disclosed departures

1. **First run of `cfg154_plane.py`.** It crashed in C4 before writing any result.
   - Cause: for Y < 0, the radial solver bracketed |X| on [−Y, −Y + J], and −Y + J rounds to −Y once |Y|/J > 10¹⁶.
   - Fix: it now solves for s on [0, J], with no cancellation (in `cfg154_common.py`, documented there).
   - The crash log is kept as `cfg154_plane_FIRSTRUN.out`, with the absolute repository path in its traceback redacted to `<repo>/` (nothing else changed).
   - The headline was re-run after the fix. Its outputs were identical apart from the elapsed-time line, so its first outputs were not kept.
2. **The comparison script's first Q1** compared absolute within-group spreads, which runaway errors swamp. That output is kept as `cfg154_compare_POSTHOC_FIRSTRUN.out`. Q1 now uses relative spreads in the verdict-relevant region; Q3 was added in the same revision.
3. **Near the n = ½ surface**, both my RK4 and the mpmath reference switch to u = √θ as the independent variable, because θ^½ is singular at ξ₁. The spec did not say this.
4. **C2 is also applied** to the radial solver's integrated M_b (stricter than the spec).
5. **C4 uses the canonical footing only;** the spec did not name one.
6. **Two small additions in the plane script:**
   - It re-derives N_a with sympy, so that it stands alone.
   - It has an "UNDECIDED (marginal)" H2 status, which did not arise.
7. **The MUTATE run skips** C1, C2, C5a, R1, R3 and R4, which the MUTATE does not touch.
8. **R4's values at x = 1 and 10** are cubic-spline interpolations in ln x on the RK4 nodes.

## Untested (declared)

- **BK's finite-temperature model as a whole:** BFK 2018's fits, β = 2, eq. 33 with both terms, its boundary conditions and NFW envelope. Only R3's gradient-limit factor is checked.
- **CFG122's thermal edge as implemented.** It is bounded from below by Q3, not reproduced.
- **G1.2 (the spheres) in the plane search,** and spheres with h fixed in kpc.
- **CFG122's other gates:** G1.3–G1.6, G2–G6 and Branch F. The stability of the X < 0 branch (BK's text after eq. 62; CFG122's G5.1).
- **Other extensions:** branch switching at folds, time dependence, a relativistic completion and non-spherical baryons.

κ = ½ and Ω_c h² stay fitted. Nothing here says the data favour either model, or that the theory is closed.
