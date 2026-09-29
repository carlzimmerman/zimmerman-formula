# CFG156 — referee re-derivation of CFG131's sound-speed headline (door 8, interacting vacuum)

- **Criteria.** Frozen in `../CFG156_FROZEN_CRITERIA.md` before any script or number. The reviewing (calculation) chat committed it unchanged as c3b321f99 (sha256 55e58db8…), and every output prints that hash first.
- **Target lane.** `../CFG131_door8_interacting_vacuum/`. Before my frozen runs I read only its FROZEN_QUESTION.md and README.md.
- **Scripts:**
  - `cfg156_referee.py`: one file of my own code. It imports nothing from the repository and runs in about 4 s.
  - `cfg156_posthoc_compare.py`: a diagnostic written after both frozen runs and after reading CFG131's code. It imports only `cfg156_referee.py` and has no pass line.
- **Runs:**
  - The main run passes 23 of 24 load-bearing checks and exits 1. The one failure is the control CM3, as frozen (see Controls). The headline lines H1–H3 all pass.
  - The MUTATE run fails CM3, H1 and H3 and exits 1. Its bound is exactly 1e5 times the main run's.
  - The two runs differ on H1 and H3, so the MUTATE control is informative.
  - The first run is kept as `cfg156_referee_firstrun.out` and `cfg156_referee_firstrun_results.json`. It also failed CB1 steps 1–2, on a sympy simplification (Disclosed departures, item 1). Every physics number is identical between the first and the final run.

## Bottom line

**CFG131's headline reproduces from independent code.**
- **Model side.** Under CFG131's hypotheses H1–H4 and its growth conventions, the largest sound speed the interacting vacuum can give the cold fluid, while keeping growth within 5% of ΛCDM to k = 30/Mpc, is c_s² = 4.608 × 10⁻¹². CFG131 gives 4.6e-12.
- **Target side.** The target's hydrostatic support needs at least 1.963 × 10⁻⁸ at 10⁹ M☉ and 6.207 × 10⁻⁷ at 10¹² M☉. CFG131 gives 2e-8 and 6e-7.
- **Ordering.** The requirement is 4.26 × 10³ times the bound. CFG131 gives 4.3e3.

Details:
- All three headline lines pass on the canonical footing. So do all five secondary bound rows, and the pressure-spread row (32.2–271.7, against CFG131's 32–272).
- **The bound comes from G2, not from the coupling itself.** The power-law Q gives a constant c_s² = n(1+w) for any n, and G2 caps n. The same n then sets the halo's sound speed (CB1 step 5).
- **Conventions matter at the 1% level only.** CFG131 adds radiation, Ω_r = 9.1e-5; my main reading has none. That explains the residual 0.9–1.05% at z = 10. The post-hoc check shows 0.16% once CFG131's own background is used.
- **One declared control failed, and it is why the main run exits 1.** CM3's closed form, as I declared it, left out the start-up term of the δ = a initial condition. The solver is right: the post-hoc CM3′ agrees to 1e-5.
- **Scope.** This re-derives numbers under CFG131's hypotheses; it does not test those hypotheses.
- **Two harder readings.** Giving the fluid the smallest required c_s² (R-req), or a density-dependent c_s² (R-dens), leaves the growth ratio at k = 30 at 0.006 and −0.010.

## Comparison

| quantity | CFG156 | CFG131 README | CFG131 output | CFG156 / CFG131 output |
|---|---|---|---|---|
| **bound, k = 30/Mpc, z = 0 (H1)** | **4.608e-12** | 4.6e-12 | 4.61e-12 (D3) | 0.9995 |
| bound, k = 10, z = 0 | 4.147e-11 | 4.2e-11 | 4.15e-11 | 0.9992 |
| bound, k = 2, z = 0 | 1.037e-9 | 1.0e-9 | 1.04e-9 | 0.9968 |
| bound, k = 0.5, z = 0 | 1.659e-8 | 1.7e-8 | 1.66e-8 | 0.9992 |
| bound, k = 30, z = 10 | 4.205e-11 | 4.3e-11 | 4.25e-11 | 0.9895 |
| bound, k = 10, z = 10 | 3.785e-10 | — | 3.82e-10 | 0.9908 |
| bound, k = 2, z = 10 | 9.462e-9 | — | 9.56e-9 | 0.9897 |
| bound, k = 0.5, z = 10 | 1.514e-7 | 1.5e-7 | 1.53e-7 | 0.9895 |
| **required c_s², 10⁹ M☉ (H2; smallest over x, at x = 30)** | **1.963e-8** | 2e-8 | 1.96e-8 (D3) | 1.00 |
| **required c_s², 10¹² M☉ (H2)** | **6.207e-7** | 6e-7 | not printed | — |
| **requirement / bound at k = 30 (H3)** | **4.260e3** | 4.3e3 | 4.3e3 (1.96e-8 / 4.61e-12) | 1.00 |
| P_req(10¹²)/P_req(10⁹) at matched ρ_c (S2) | 32.17 to 271.71 | 32 to 272 | 32.2 to 272 (D1, seven density keys) | 1.00 |

- **k-scaling.** Every bound scales as k⁻² in both lanes, to printed precision. In CFG156, c_s,max² k² = 4.147e-9 /Mpc² at z = 0 and 3.785e-8 at z = 10.
- **The required c_s² is dP/dρ from hydrostatics**, and it needs no boundary condition.
  - I derived the closed form V_f²(1+x²)^(3/2)/(x(1+2x²)) in the spec. It turned out to be CFG131's own definition (`cs2_req` in D3).
  - Its minimum over x in [0.1, 30] is at x = 30, where it equals 1.0011 × V_f²/2c². The README's "V_f²/2c²" is the x → ∞ limit.
  - With P(∞) = 0, P/ρ tends to the same value.
- **Post hoc, after reading CFG131's Dcommon.py.** On CFG131's background (Ω_r = 9.1e-5 added, Ω_Λ kept at 0.685), my solver gives all eight D3 bounds to within 0.16%. That is D3's 3-figure rounding. So the ~1% at z = 10 in the table is the radiation convention (`cfg156_posthoc_compare.out`).

## Controls

- **CB1 PASS (final run).** Sympy, on ds² = −N²dt² + A²dr² + B²dΩ² with N, A and B general functions of (t, r) and the cold fluid comoving, gives each step of the chain:
  - ∇_μ(−ρ_L g^{μν}) = −∂^ν ρ_L;
  - the exchange then gives ∂_r ρ_L = 0 and N = −∂_t ρ_L/Q;
  - the fluid's acceleration is ∂_r ln N;
  - the Euler equation has no Q term, and the energy equation carries Q;
  - so ∂_r p = (ρ+p)(Q_ρ/Q) ∂_r ρ. This holds for a general Q(L, R), for the power law, and for a non-power form.
  - For the power law, p = nρ/(1−n) + Cρⁿ and c_s² = n(1+w).
  - Reported: the static limit forces Q = 0 (CFG131's A5).
  - In the first run, steps 1–2 FAILED (Disclosed departures, item 1).
- **CT1 PASS: the target reproduces its own identity.** Over 4 masses × 2 footings × 2001 points:
  - C(r) = a₀M_b/4π to 7.8e-16;
  - M_c(<r) by quadrature to 2.7e-14;
  - g from the enclosed mass equals the P2 law to 1.3e-15.
- **CT2 PASS: the singular isothermal sphere.** The solver returns P/ρ = σ² to 6.7e-16 and dP/dρ = σ² to 6.9e-14.
- **CT3 PASS.** The numeric P equals a₀M_b/(8πr²) to 8.9e-16. The numeric dP/dρ equals the closed form to 4.5e-6 (line 1e-5).
- **CM1 PASS.** ΛCDM growth matches the growth integral D(a) to 4.5e-10.
- **CM2 PASS.**
  - Sympy shows that a^(−1/4) J_(5/2)(2√(βa)) solves the Einstein–de Sitter Jeans equation (a symbolic zero).
  - The solver matches it at a = 1 to ≤ 2.5e-11 for β = 0.2, 1 and 5. Those runs keep 0.944, 0.744 and 0.165 of the pressureless growth.
- **CM3 FAIL as frozen, kept load-bearing.** The two-fluid first-order coefficient (1 − ratio)/β is 0.240024, against the declared 2f_c/7 = 0.240363. That is 1.41e-3, over the 1e-3 line.
  - **The error is in my declared expectation, not in the solver.**
    - Starting at δ = a at z = 1000 is the zeroth-order growing mode, not the first-order one.
    - The mismatch at a_i adds a homogeneous growing mode, −1.4 S a_i a, where S = −2f_cβ/7.
    - So the exact first-order answer is (2f_c/7)(1 − 1.4a_i + 0.4a_i^(7/2)) = 0.240027.
    - The post-hoc row CM3′ matches the solver to 1.06e-5, which is the size of the O(β) term.
  - CM3 stays a failed, disclosed control, and it is why the main run exits 1.
  - It does not bear on the headline. The bound search uses the same δ = a start as CFG131, and CM1, CM2 and CM4 test the solver directly.
- **CM4 PASS.** The k = 30 bound moves by 8.5e-11 between rtol 1e-10 and 1e-12.
- **MUTATE: the pressure term × 1e-5, inside the bound searches only.**
  - The bound rises by exactly 1e5, to 4.608e-7. That is above the requirement at 10⁹, 10¹⁰ and 10¹¹ M☉.
  - H1 and H3 fail (the factor becomes 0.043). H2 and every control are unchanged.

## Reported rows (declared in the spec)

- **R-alt.** On the alt footing (a₀ = 1.1312e-10), the smallest requirement is 2.158e-8 at 10⁹ M☉ (1.079 × 2e-8) and 6.824e-7 at 10¹² M☉ (1.137 × 6e-7, outside 10%). So CFG131's numbers are canonical, which its Dcommon.py confirms. The factor is 4.68e3.
- **Conventions at k = 30** (the bound relative to the main reading):
  - k read in h/Mpc: ×2.20 (1.014e-11). This reading would have failed H1. CFG131's code uses k in Mpc⁻¹, like my main reading.
  - H₀ = 70: ×1.079.
  - flat, with radiation (Ω_r = 9.2e-5): ×1.0015.
  - the full constant-w fluid (w = c_s²): a relative change of 1.2e-9.
- **R-req.** Set c_s² to the smallest requirement, 1.963e-8. The growth ratio at z = 0 is then 0.941, 0.360, 0.020 and 0.0059 at k = 0.5, 2, 10 and 30/Mpc.
  - So even the least demanding halo point fails G2, already at k = 0.5.
  - A single k-independent growth factor would have to raise k = 30 about 160-fold while staying within 5% at k = 0.5, which cannot be done. This is an argument about a multiplicative factor, not a computed Γ ≠ 0 row.
- **R-dens.** Here c_s² is a function of density.
  - At each density it takes the smallest requirement among the four masses that reach that density. Outside the union of their ranges it is zero.
  - It is applied at the cosmic mean density ρ̄_c(z), which passes through the halo densities for z between 2.6 and 234.
  - The growth ratio at z = 0 is 0.67, −0.23, 0.012 and −0.010 at k = 0.5, 2, 10 and 30. Negative values are Jeans oscillations.
  - **Correction to the spec's label.** The spec called this row "beyond CFG131", which was wrong. CFG131's README row R4, which I had read, already applies the target's own density-dependent equation of state, one mass at a time. Its R4b does so on each mass's own density range and gets z = 0 ratios of at most 0.0855 at k = 30 (D3). My construction differs: it takes the minimum over masses on the union of ranges. Both fail G2 at k = 30.
- **R-sub.** The smallest k/(aH/c) at k = 0.5 is 125, at z = 1000, so the sub-horizon equations hold.
- **R-prof.** For every mass, dP/dρ falls monotonically across the range: 19.9 V_f²/2 at x = 0.1 and 1.0011 V_f²/2 at x = 30. P/ρ falls from 10.05 to 1.0006 V_f²/2.

## Independence

**What is mine:**
- Every line of `cfg156_referee.py`, written from the frozen spec before any CFG131 code or output was opened.
- The target, built from CFG44's README formulas and Bcommon.py docstrings, not from its code.
- A numerical hydrostatic solver: quadrature from r = ∞, then centred differences. CFG131 used the closed form.
- The growth solver (DOP853, rtol 1e-10) and a first-crossing bound search (a 0.1-dex scan, then brentq). CFG131 used LSODA at rtol 1e-9, and a 0.5-dex scan that takes the last grid point above the line.
- The covariant chain, on a spherical comoving chart (N, A, B of t, r). CFG131's D1 used a conformally flat chart with N and A functions of (t, x, y, z).
- The closed-form controls: the Bessel Jeans solution, the two-fluid first order, the growth integral, and the isothermal sphere.

**Where independence stops:**
1. **Targets were read first.** I read CFG131's numbers in its README before writing code, so they are targets, not blind predictions.
2. **Shared target.** Both lanes use CFG44's point-mass formulas, so a flaw in the target would be common to both.
3. **Shared framing.** H1–H4 and the chain of reasoning are CFG131's: vacuum gradient, lapse, Euler equation, c_s² = (ρ+p)Q_ρ/Q, then a cosmological growth bound that also caps the halo's sound speed. I re-derived each step. I did not look for escapes outside H1–H4.
4. **Shared conventions.** The growth set-up is CFG131's frozen one. Where it said nothing, my readings turned out to match CFG131's code: H₀ = 67.4, k in Mpc⁻¹, and Γ = 0 in R2. Radiation did not match; it moves the bounds by ≤ 1.05%.
5. **Shared reading of the target's c_s².** My dP/dρ reading is CFG131's own definition.
6. **Not re-derived.** CFG131's linear Newtonian-gauge identity (D1-B).
   - My pressure term rests instead on the slice relation of CB1 step 5. It holds on every fluid-orthogonal slice, so δp = c_s² δρ in the fluid's rest frame.
   - Neither lane's chart is the general comoving chart.
7. **Post hoc.** The comparison script and the table's last column were produced after reading CFG131's code and outputs.

## Disclosed departures

1. **CB1 zero test, amended after the first run.**
   - The first run tested `simplify(e) == 0`. That left the θ-component of steps 1–2 as (sin2θ tanθ + cos2θ − 1)ρ_L/(…), which is identically zero, so those steps failed.
   - The test is now `is_zero`: simplify, then trigsimp(expand_trig(·)).
   - A post-hoc self-check (CB1′) shows it still returns False once ρ_L cosθ/B² is added.
   - No pass line, tolerance or physics input changed, and every number is identical.
2. **CM3′ is a post-hoc row.** CM3 keeps its frozen line and its FAIL.
3. **Ghost points.** Centred differences at the grid ends need one extra point at each end, x = 0.1 e^(−Δ) and 30 e^(Δ). All 2001 declared points get centred differences.
4. **P(∞) = 0** is taken by quadrature in s = ln(r′/r) over [0, 80]; the remainder is below e^(−160).
5. **The bound scan** runs up from 1e-16 to at most c_s² = 1. The frozen file set no upper end.
6. **CB1 step 6** runs dsolve at the concrete n = 3/10, alongside the symbolic-n substitution and the homogeneous solution ρⁿ. This avoids sympy's n = 1 branch; it was written before the first run.
7. **Constants:** GM☉ = 1.32712440018e20 m³/s² (IAU), G = 6.67430e-11 (CODATA 2018), a₀ = 9.3603e-11 and 1.1312e-10 m/s², H₀ = 67.4.
8. **The R-dens label is corrected** (see Reported rows).

## Untested

Declared in the frozen file:
- a nonzero exchange rate Γ together with c_s², i.e. the dilution term and the background shift at once. R-req shows what a k-independent change of growth would have to supply;
- Q forms beyond the power law, apart from R-dens;
- horizon-scale GR terms, neutrinos and baryon–photon coupling;
- nonlinear growth: k = 30/Mpc at z = 0 is nonlinear, and the linear ratio is the gate's convention;
- the CMB clause of G2;
- the exponential sphere and other baryon profiles for the required c_s²;
- relativistic corrections to the target's hydrostatics;
- CFG131's other rows: G1 on the exponential sphere, D2, D3's R1 and R3, D4, and the epoch channel.

Also untested here:
- H1–H4 themselves: a vacuum stress that is not Lorentz invariant, a Q^μ with a spatial part, or a collisionless cold component;
- the covariant chain on the general comoving chart.

κ = ½ and Ω_c h² stay fitted. Nothing here says the data favour either model, or that the theory is closed.
