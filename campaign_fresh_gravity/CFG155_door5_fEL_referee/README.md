# CFG155 — Referee of CFG130 (Door 5): Eddington's f(E) for the point-mass target is positive. Reproduced.

- **Criteria:** frozen in `../CFG155_FROZEN_CRITERIA.md` (c702dde54, sha256 edff8228…de52), before any code of this lane. Both runs print the sha256 first. The shared gates are in `../closure_map/TEN_DOORS_GATES_2026-09-29.md`. The menu of doors was written knowing the target, and this referee knew CFG130's verdict from its README.
- **Scripts:**
  - `cfg155_eddington_referee.py`: one file, own code. It imports nothing from the repository. It rebuilds CFG44's target from its definitions.
  - `cfg155_compare_cfg130.py`: the post-hoc comparison (R5). It was written after both frozen runs. It reads CFG130's outputs and does not run or modify them.
- **Runs:**
  - The main run passes H1 and all seven controls and exits 0 (10 s).
  - The MUTATE run fails H1 with certainty and exits 1 (10 s). The controls that do not use the density pass. The failures the spec expected under MUTATE happen as declared.
  - The comparison script exits 0.

## Bottom line

**Yes. For CFG44's point-mass target in its own P2 potential, Eddington's isotropic f(E) is strictly positive at every energy. Every f that CFG130 prints for this headline agrees with independent code within 2 × 10⁻⁵, or within 3 × 10⁻⁶ once CFG130's truncation is matched.**

- **Why it holds.** The result is analytic, and the numerics confirm it.
  - In units G = M_b = a₀ = 1, d²ρ_c/dΦ² = x⁵/(π(1+x²)^(7/2)). This is positive for every x > 0.
  - dρ_c/dΦ = −(1+2x²)/(4π(1+x²)²) tends to 0 as Φ → +∞, so the second form of Eddington's formula has no boundary term.
  - Sympy confirms both forms exactly, and finite differences reproduce them to 2 × 10⁻¹⁰.
  - The integrand is therefore positive, and f/∫|integrand| = 1 exactly.
- **On the grid.** f > 0 with certainty at all 1201 energies from x_E = 10⁻⁶ to 10⁶, that is E from −10⁶ to +13.5. This includes the decade at each end outside CFG130's window, [10⁻⁶, 10⁻⁵] and [10⁵, 10⁶].
  - The three routes agree to 1.8 × 10⁻⁸.
  - The minimum of f is 1.43 × 10⁻¹⁴ at x_E = 10⁶, and 1.43 × 10⁻¹² at x_E = 10⁵, the end of CFG130's window. Units are M_b r_M⁻³ v_M⁻³.
  - The minimum is set by where the grid stops, on the isothermal tail f → e^(−2−2E)/π^(5/2), which f matches to 2.8 × 10⁻¹² there. It is not a physical number.
- **The target's identities, reached through f:**
  - The round trip returns ρ_c to 1.6 × 10⁻¹⁵ at x = 10⁻⁴ … 10⁴.
  - The isotropic dispersion returns CFG44's σ² = V_c²/2 to 1.7 × 10⁻¹⁴.
  - The Kepler-cusp limit (8√2π³)⁻¹(−E)^(−1/2) holds to 3.8 × 10⁻¹³ at x_E = 10⁻⁶.
- **The MUTATE bites.** A cored tracer in the same potential, ρ_mut = 1/(4π√(x² + 0.01)√(1+x²)), is negative with certainty at 515 of 1201 energies, from x_E = 10⁻⁶ to 0.138.
  - Its minimum is f = −2.9 × 10⁻⁴, and min f/∫|integrand| = −0.175.
  - Deep inside, f follows the declared asymptote −ρ₀/(4√2π²)(−E)^(−3/2) to 1.5 × 10⁻³.
- **What this does not change.** A positive f is a necessary condition for a collisionless-fluid mechanism, not a mechanism (CFG130 D6).
  - G1–G3 and G5 are not addressed. G4 is untouched: no constant is introduced.
  - Nothing here derives why C(r) = (a₀/4π) M_b(<r).

## Comparison with CFG130 (R5; CFG130's files opened only after both frozen runs)

| quantity | CFG130 (D5_A) | CFG155 | agreement |
|---|---|---|---|
| potential and zero point | Φ = asinh r − √(1+r²)/r | the same (fixed from the README's E range) | identical |
| formula | second form in t (QUADPACK); t-integral cut at Φ(10⁷ r_M), no tail, no boundary term | untruncated, to Φ = +∞ (tail bound ≤ 9 × 10⁻¹⁸ f); three routes, including the first form, which never uses ρ″ | the cut lowers f by 1.8 × 10⁻⁵ at r_E = 10⁵ and cannot flip a sign |
| energy grid | 481 points, r_E in [10⁻⁵, 10⁵] | 1201 points, x_E in [10⁻⁶, 10⁶] | CFG130's frozen M1 promised [10⁻⁶, 10⁶]; the extra decades are positive here |
| f at the 11 printed energies | 6 significant digits | full / with the cut matched | worst 2.0 × 10⁻⁵ / 3.1 × 10⁻⁶ (tolerance 10⁻³); print resolution about 5 × 10⁻⁶ |
| min f | 1.4290835966 × 10⁻¹² at r_E = 10⁵ | 1.4291089098 × 10⁻¹² full; 1.4290835966 × 10⁻¹² with the 10⁷ cut | −1.77 × 10⁻⁵ from the cut; 8.9 × 10⁻¹⁶ when matched |
| f/∫\|integrand\| | min = max = 1.000 | 1.0000000000 at all 1201 energies | identical |
| energies with f < 0 | 0 of 481 | 0 of 1201 | identical |
| Kepler limit | 1.0000 at r_E = 10⁻⁴ (5% line; README "4 digits") | 1 + 3.8 × 10⁻⁹ at 10⁻⁴; 3.8 × 10⁻¹¹ at 10⁻⁵; 3.8 × 10⁻¹³ at 10⁻⁶ | consistent |
| round trip | worst 3.6 × 10⁻⁴ at r = 10³ (interpolated f; grid-limited) | ≤ 1.6 × 10⁻¹⁵ at 10⁻⁴ … 10⁴ | README's "4 × 10⁻⁴" is CFG130's interpolation, not f |
| isothermal-sphere control | shape only: f/e^(−E/σ²) constant to 2% at E = −1, 0, 1 | absolute Maxwellian to 6.7 × 10⁻¹⁶ at 41 energies | CFG130's control is weaker; no effect on the verdict |
| d ln f/dE range | [−2.0000, +0.3056] | max +0.3061 at x_E = 0.589; −2.0000 at x_E = 10⁵ | within ±0.05 of the README's "+0.3 to −2.0" |
| d ln f/dE at r_E = 1 | 2.8734 × 10⁻² | 2.9756 × 10⁻² | 3.4% gap: CFG130's `np.gradient` on its grid. Applied to CFG155's f, it returns 2.873441 × 10⁻² and CFG130's range exactly |
| MUTATE | shell bump; f < 0 at r_E in [1.62, 2.61] (11 of 481) | cored tracer; f < 0 at x_E in [10⁻⁶, 0.138] (515 of 1201) | different mutations; both bite |

- **Findings about CFG130, stated plainly.** None changes its headline.
  1. Its frozen M1 names the energy range spanned by r in [10⁻⁶, 10⁶] r_M. The script uses r_E in [10⁻⁵, 10⁵], which the README reports correctly.
  2. The t-integral is cut at Φ(10⁷ r_M) with no tail, which lowers f slightly at the outer end.
  3. Its isothermal control tests the shape of f, not its normalisation.
  4. Its d ln f/dE values carry second-order gradient error on a 48-per-decade grid: 3.4% at r_E = 1, and 0.0005 on the maximum.
  5. Its integrand ρ″ is lambdified from an unsimplified sympy expression, `diff(diff(ρ)/g)/g`, which cancels catastrophically at small r.
     - Below r ≈ 10⁻⁴ it returns 0 or negative noise. Examples: −3.6 × 10⁻²² at r = 10⁻⁵, where the exact value is +3.2 × 10⁻²⁶; −3.7 × 10⁻²⁵ at r = 10⁻⁸. At r = 10⁻³ it is off by 1.3 × 10⁻⁴.
     - The effect on f is below 2.2 × 10⁻¹² relative at r_E = 10⁻⁵, so no printed number moves.
     - But the README's "the integrand is positive at every point" is true analytically (as shown here), not as that code evaluates it below 10⁻⁴.
- **A remark from the printed rows, not a computed claim.** f/f_K − 1 falls as E⁻²: 3.8 × 10⁻⁷, 3.8 × 10⁻¹¹ and 3.8 × 10⁻¹³ at E = −10³, −10⁵ and −10⁶. The first-order correction in 1/|E| is therefore absent for this profile, and CFG130's "4 digits" holds with a wide margin.

## Controls

| check | line | main run | MUTATE run |
|---|---|---|---|
| H1(a) ρ″ > 0 on 16001 points, no boundary term, C5 | pass/fail | PASS (min ρ″ 3.2 × 10⁻⁴¹ at x = 10⁻⁸) | FAIL: ρ_mut″ ≤ 0 for x up to 0.481 (does not count alone) |
| H1(b) f > 10⁻⁶ ∫\|integrand\| at 1201 energies; tail < 10⁻¹⁰ f | pass/fail | PASS (1201/1201; tail 9.3 × 10⁻¹⁸) | **FAIL with certainty (515 negative): the MUTATE bites** |
| H1(c) routes A, C against B | 10⁻⁵ | 2.7 × 10⁻¹⁵, 1.8 × 10⁻⁸ | 6.4 × 10⁻¹¹, 1.8 × 10⁻⁸ |
| Q1 / Q2 / Q3 / Q4 | as frozen | all PASS | Q1–Q3 FAIL (expected), Q4 PASS |
| C1 Hernquist closed form, route B / A / C | 10⁻⁶ / 10⁻⁵ | 1.7 × 10⁻¹³ / 1.7 × 10⁻¹³ / 1.4 × 10⁻¹¹ | the same |
| C1b the recalled Hernquist formula, round trip | 10⁻⁶ | 7.1 × 10⁻¹⁴ | the same |
| C2 isothermal sphere, route B / A / C | 10⁻⁸ / 10⁻⁶ | 6.7 × 10⁻¹⁶ / 5.6 × 10⁻¹⁶ / 5.3 × 10⁻⁹ | the same |
| C3 closure ODE, Poisson, C(r), M_c, Φ, P, dP/dr | 10⁻⁷ … 10⁻¹² | all ≤ 1.2 × 10⁻¹¹ (worst dP/dr; ODE 8.6 × 10⁻¹³) | the same |
| C4 round trip / σ² = V_c²/2 / isothermal limit / Kepler limit | 10⁻⁵ / 10⁻⁵ / 10⁻⁴ / 10⁻⁴ | 1.6 × 10⁻¹⁵ / 1.7 × 10⁻¹⁴ / 2.8 × 10⁻⁶ / 3.8 × 10⁻¹¹ | round trip 6.2 × 10⁻¹⁴ PASS; σ² and Kepler FAIL (expected), so C4 FAIL |
| C5 sympy identities; finite differences | exact; 10⁻⁶ | exact; 1.8 × 10⁻¹⁰, 1.3 × 10⁻¹⁰ | the same |
| C6 both footings, M_b = 10⁹ and 10¹² M☉ | 10⁻⁸ | 2.8 × 10⁻¹⁵ | the same |
| MUTATE deep asymptote | 5% | n/a | 1.5 × 10⁻³ |
| exit code | | **0** | **1** |

- No control failed in the main run, and no declared tolerance was changed.
- **The MUTATE run behaves as declared:**
  - H1 fails through (b), the numerical Eddington result, and not only through (a).
  - The round trip still holds (it is an identity for either sign of f).
  - The Kepler limit, the σ² identity and Q2–Q3 fail, as the spec expected.
  - The negative region, x_E below 0.138 against x_core = 0.1, matches the declared "x_E below roughly x_core".
- **Reported rows (no pass line):**
  - **R1:** f/f_K runs from 0.80 to 1.076 over x_E ≤ 1; f/f_iso runs from 0.14 to 1.000 over x_E ≥ 1.
  - **R3, the outer boundary.** A cut at 10 x_E lowers the second form by 2.4 × 10⁻³ and raises the first form by 2.2 × 10⁻⁴. A cut at 100 x_E changes them by −1.8 × 10⁻⁵ and +8.7 × 10⁻⁷. Both stay positive, as expected.
  - **R4:** every boundary term is zero.
  - **N1** (added diagnostic): the lambdified sympy forms agree with 50-digit mpmath to 5 × 10⁻¹⁶.
  - There were no QUADPACK warnings.

## Independence

- **Read before the spec:**
  - CFG130's FROZEN_QUESTION.md and README.md;
  - TEN_DOORS_GATES_2026-09-29.md;
  - CFG44's README.md and the docstrings of Bcommon.py (function bodies not read);
  - CFG118's frozen criteria, for style.
- **Opened only after both frozen runs:** D5_A_eddington_pointmass.py, D5common.py, and the D5_A `.out` and `.json` (main and MUTATE).
- **Not opened at all:** D5_B_orbit_lp.py and its outputs (out of scope), and CFG44's B1–B4.
- **Where independence stops:**
  - The verdict was known in advance, so this is not blind.
  - The target, its potential and the reading that the fluid orbits in g_tot are CFG44's and CFG130's definitions, used as written. An error in them would be shared.
  - Both lanes use the same textbook inversion, and both derive ρ″ with sympy. What is independent here:
    - the hand derivation;
    - the first form (route C), which never uses ρ″;
    - the untruncated treatment;
    - absolute closed-form controls (Hernquist, Maxwellian);
    - the full grid.
  - Eddington's formula, the Hernquist DF and the cusp and isothermal limits are recalled (Binney & Tremaine 2008; Hernquist 1990), not read in this session. C1b checks the Hernquist formula on its own.
  - The numerical stack (numpy, scipy, sympy) is shared, and both codes were written by the same kind of agent.

## Untested (declared)

- The extended-baryon (exponential-sphere) orbit-superposition LP results V1–V3, any β ≠ 0 case and the D5_B controls.
- The maximum-entropy statements (the isothermal and Fermi–Dirac fits). Only the d ln f/dE range is compared.
- Non-ergodic f(E, L) with β ≡ 0. Only the ergodic f(E), which is unique, is inverted.
- Stability of the equilibrium, whether the DF is reached, non-spherical baryons, ν_mono, and the potential re-solved from f.

## Disclosed departures and open choices

1. **Before the first full run:**
   - The three routes and the moments function were unit-tested on the Hernquist and isothermal controls from a scratch harness; the target was not touched.
   - The sympy forms were printed; for the target they are the closed forms already written in the spec.
   - The first full run of each mode is the one reported. No first-run failure occurred.
2. **Implementation details the spec leaves open:**
   - x(Φ) is found by bracketed Newton.
   - Sympy expressions are simplified before lambdify.
   - The round trip's outer Gauss–Legendre uses 64 nodes per half-decade and stops at x = 10¹². The neglected fraction is at most (x/10¹²)² ≤ 10⁻¹⁶.
   - The tail check is folded into H1(b), since the spec states it as a "must".
3. **Added beyond the spec:** N1, the sympy check dΦ/dx = g for every profile, and the printed E-range row.
4. **C6** builds ρ_c, g_tot and d(dρ/dΦ)/dr in physical units with sympy from the physical definitions. It reuses the dimensionless cancellation-free difference (Φ(r) − Φ(r_E))/(r − r_E), scaled by v_M²/r_M.
5. **Reporting choices:**
   - R2 is skipped under MUTATE because f changes sign.
   - The R3 case x_E = x_out = 10⁵ is reported as degenerate.
6. **R5 is post hoc.**
   - CFG130's actual cut, at x_out = 10⁷, is not one of the frozen R3 rows (10⁵ and 10⁶). The matched cut is computed by the comparison script with the same Route B code.
   - The spec's 10⁻³ tolerance is met with or without the match.
   - The `np.gradient` check on d ln f/dE was added to the comparison script after the r_E = 1 gap was seen.
   - The check of CFG130's integrand (finding 5) was added after reading its code. It rebuilds CFG130's sympy expression as written in D5_A.
7. **Nothing was committed or pushed by this lane.** All files are new; no existing file was edited, and CFG130 was not re-run.

kappa = 1/2 and Omega_c h^2 stay fitted. Nothing here says the data favour either model, or that the theory is closed.
