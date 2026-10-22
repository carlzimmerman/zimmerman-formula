# E4_fitted_three: what really fixes κ, L★ and u, and are they independent?

## Verdict: CRISP FINDING

κ = ½ stays FITTED. Z/4π stays a POSTULATE (Milgrom's relation). Nothing here derives any of the three. Not theory closed.

1. **The L★ ≥ 24 pc floor depends on standard-MOND machinery and on one SPS number.** CFG820 builds its prediction with
   the RAR fitting function ν_RAR and the additive EFE recipe y → y + g_ext/a₀ (`cfg820.py:16, :24`). Neither is the
   screened theory's own physics. Our rerun uses the theory's law ν_L, from g_N = g²/(g+a₀), and drops the recipe.
   - The floor rises to **28.85 pc on the canonical footing and 29.12 pc on alt**, against 23.64 / 24.48 pc in CFG820.
     The frozen line reads **L★ FLOOR MOVES**.
   - The rise comes from the EFE treatment, not the kernel. With ν_L and the recipe kept, the floor is 23.87 / 24.66 pc.
   - The action's own external-field response lies somewhere between these two cases. We did not solve it.
   - CFG820 uses one stellar M/L (Υ_V = 1.6) for every cluster. Shifting it by its own 1σ, ±0.15 dex, moves the native
     floor to **20.0–42.3 pc** (canonical) or 20.7–43.5 pc (alt). So the floor is set by this calibration more than by anything else.
   - The thermal value L★ = 23.43 / 19.38 pc is excluded by the native model, at Δχ² = 6.21 and 9.01.
2. **u ≈ 0.47 holds only at κ = ½.** The inversion gives **d ln u / d ln a₀ = +0.55** on both footings.
   - The galaxy gas routes measure a₀ = **7.99×10⁻¹¹ m/s²** (CFG493 with a Planck-free background). At that a₀,
     u_MID = **0.433 ± 0.030** (statistical).
   - The a₀ error alone adds **±0.059** to u. That is more than the statistical error (0.033) and more than all the
     calibration brackets combined (0.044).
   - So u is not an independent "measured fraction". The cluster data fix the combination u·a₀^(−0.55). This is the
     A81 circularity, now expressed as a number.
3. **The three are independent in the action. No relation ties them.**
   - The Jacobian of four observable classes with respect to (ln a₀, ln L★, ln u) has rank 3, with singular values
     1.05, 0.62 and 0.35. It is block-triangular: galaxies fix a₀, globulars then fix L★, and clusters then fix u.
   - Every candidate relation is a posit or a reparametrisation (Part E). No forced relation exists, so there is no
     look-elsewhere probability and no second prediction to give.

Criteria: `FROZEN_CRITERIA.md` was committed alone first (9cc8fcae21). AMENDMENT A1 (9b3dfb1000) was added before any
result. It adds the native-kernel u.

Run: `OMP_NUM_THREADS=1 nice -n 10 python3 e4_fitted_three.py`. It takes 7 s and 91 MB, exits 0, and passes **6/6**.
`--mutate` replaces ν_L with ν_RAR. K5 then fails and the run exits 1 at 5/6. Every number here is in
`e4_fitted_three_results.json`.

## 1. κ: clean value

The cluster channel is circular (A81 §9.4), so it is excluded. The inputs are CFG493's three gas routes and its own
covariance, which is reproduced (K1, K2).

| | a₀ (m/s², footing-free) | κ_Λ (canonical) | κ_crit (alt) |
|---|---|---|---|
| CFG493 record (Planck ρ_Λ; Hubble-flow distances at H₀ = 67.4) | 7.811e-11 ± 0.0985 dex | 0.417 ± 0.095 | 0.345 ± 0.078 |
| **clean: CFG886 BAO + BBN background** (h 0.6856, Ω_m 0.2976) | **7.986e-11** | **0.414 ± 0.094** | **0.347 ± 0.079** |
| variant: SH0ES h with BAO Ω_m | 8.669e-11 | 0.422 ± 0.096 | 0.354 ± 0.080 |

- The background swap shifts κ by −0.03σ (canonical) and +0.02σ (alt). Both read **κ ROBUST**.
- The swap barely moves κ because two effects nearly cancel. The Hubble-flow routes' a₀ scales as h^2.2, while √ρ scales
  as h. The HF-weighted lever is 1.30.
- With the clean background, ½ sits +0.91σ from the canonical value and Z/4π sits +0.50σ.
- Kernel term: CFG493's routes use ν_mono, not ν_L. Switching to ν_L lowers a₀ by 0.0011, 0.0026 and 0.0108 dex at
  y = 0.03, 0.072 and 0.3. Each is ≤ 0.11 of σ.
- What the data actually fix is **a₀**. In this theory κ appears in no z ≈ 0 observable. It is a₀ divided by a background
  input, so "κ fitted" is the same statement as "a₀ fitted". Writing the result as κ adds the claim a₀ ∝ √ρ_Λ, which
  only a₀(z) data or the P5 closure can test.

## 2. L★: the floor (CFG820) and the ceiling (CFG821)

| footing | R0: record machinery (ν_RAR + EFE recipe) | **N1: native (ν_L, no recipe)** | N2: ν_L + recipe | N1 with Υ_V × 10^(∓0.15) | d ln L★₉₅ / d ln a₀ |
|---|---|---|---|---|---|
| canonical | 23.640 pc | **28.853 pc** | 23.867 pc | 20.009 / 42.280 pc | +0.065 |
| alt | 24.476 pc | **29.123 pc** | 24.657 pc | 20.741 / 43.477 pc | +0.075 |

- Pal 14 drives the change. Its recipe field y_ext = 0.019 is larger than its internal y = 0.010. Its boost B is 6.37
  with the recipe and 10.44 without it.
- CFG821's dSph ceiling with ν_L is unchanged at **22.0 pc** on both footings. Its unscreened χ² is 58.4 / 51.8 for 11
  dSphs, so it stays CONDITIONAL.
- CFG821 also assumes no bound cold mass. The screened theory requires bound cold mass for dwarfs, so the ceiling is
  not a valid input to this theory. Read literally, the window [28.9, 22] pc would be closed.

## 3. u: measurement audit (eRASS1 × KiDS, 318 clusters; D6/A21 inversion reproduced, K4)

- **The MID band is a fixed physical radius range, R = 0.461–1.419 Mpc. u_MID uses no r_sp, r200 or NFW quantity.**
- The label "inside splashback" comes from D6's ΛCDM-calibrated r_sp. Its median, 1.403 Mpc, happens to sit at the
  band's outer edge.

| bracket (canonical; alt in the JSON) | class | u_MID | shift / σ |
|---|---|---|---|
| record (ν_mono) | — | 0.4716 ± 0.0325 | — |
| native kernel ν_L (A1) | kernel | 0.4726 | +0.03 |
| a₀ × 1.05 / ÷ 1.05 | footing | 0.4845 / 0.4590 | ±0.40 |
| M_gas × 1.10 | SURVEY-CALIBRATION | 0.4974 | +0.80 |
| R500 × 10^(±0.033) (±0.1 dex in M500) | ΛCDM-PROCESSED | 0.4461 / 0.4984 | −0.78 / +0.83 |
| f_s 0.10 / 0.30 | externally calibrated | 0.4495 / 0.4932 | ∓0.68 |
| Planck → BAO + BBN background (first order) | ΛCDM-PROCESSED | 0.4605 | −0.34 |

- Every ΛCDM-processed bracket stays under 1σ, so the frozen line reads **u CLEAN** on both footings.
- The calibration brackets add up to 0.044 (canonical) and 0.050 (alt) in quadrature. That is larger than the
  statistical error.
- d ln u / d ln M_gas = +0.56.

## 4. Input ledger

| input | used by | class | source |
|---|---|---|---|
| HI rotation curves and HI widths (gas points) | κ | RAW | SPARC, MIGHTEE-HI and WALLABY, through CFG493 |
| HI flux scale and flux tie | κ | SURVEY-CALIBRATION | CFG306 / CFG304 |
| TRGB/Cepheid ladder distances (P1) | κ | SURVEY-CALIBRATION | CFG449 |
| Hubble-flow distances at H₀ = 67.4 (P2, P3) | κ | ΛCDM-PROCESSED (Planck H₀); clean substitute: CFG886 h | CFG493 S_HF |
| stellar M/L (small lever) | κ | SURVEY-CALIBRATION (SPS) | CFG493 S_star |
| ρ_Λ (Planck: h 0.674, Ω_Λ 0.685) | κ only, never a₀ | ΛCDM-PROCESSED; substitute CFG886 BAO + BBN (framework-equivalent background under P3 with β → 0, A46/A78) | CFG493 K1 |
| kernel ν_mono | κ, u | not native (a repair of ν_RAR); bounded ≤ 0.011 dex (κ) and 0.001 (u) | CFG4_common |
| cluster R_req (A18) | κ (A81 joint fit) | circular with u; excluded | A81 §9.4 |
| globular σ, L_V, r_h, R_GC | L★ | RAW | CFG332 table |
| Υ_V = 1.6 (coherent) | L★ | SURVEY-CALIBRATION (SPS); dominant | CFG820 |
| ν_RAR kernel | L★ (CFG820, CFG821) | STANDARD-MOND-MACHINERY; replaced by ν_L | `cfg820.py:16`, `cfg821.py:20` |
| additive EFE recipe with M_MW = 6e10 M☉ point mass | L★ | STANDARD-MOND-MACHINERY; dropped in N1 | `cfg820.py:24` |
| screening table S(s) | L★, Jacobian | FRAMEWORK-NATIVE (CFG691 point-mass solve) | CFG691 |
| dSph σ, M_V, r_h; Υ = 2 | L★ ceiling | RAW; SPS | `lvd_dwarf_mw.csv` |
| KiDS ΔΣ (Σ_crit at a fiducial cosmology) | u | RAW shear; the distances are ΛCDM-PROCESSED (background bracket) | CFG687 npz |
| eRASS1 M_gas | u | SURVEY-CALIBRATION (X-ray) | CFG687 npz |
| eRASS1 R500 (WL-calibrated M500) | u | ΛCDM-PROCESSED (bracket ±0.1 dex) | CFG687 npz |
| β-model shape (r_c = 0.15 R500, to 3 Mpc), f_s = 0.20 | u | externally calibrated | CFG687 |
| r_sp = 1.367 r200c (NFW c = 4.5, r_sp = 0.83 r200m) | the "inside splashback" label only | ΛCDM-PROCESSED | D6/A41 |
| KiDS isolated-lens M* and r200m selection | u_gal (D6, cited) | SPS; ΛCDM-PROCESSED | D6 |
| Ω_c/Ω_b = 5.364 | P4 mass budget, not u_MID | ΛCDM-PROCESSED; Planck-free CFG886 gives 5.272 ± 0.218 | CFG886 T3 |

## 5. Dependency structure and the true count

The Jacobian below is at the canonical footing, L★ = 30 pc and u = 0.4726.

| observable | ∂/∂ln a₀ | ∂/∂ln L★ | ∂/∂ln u |
|---|---|---|---|
| galaxy g (10¹⁰ M☉, 10 kpc) | +0.405 | −1.6e-5 | 0 |
| NGC 2419 σ | +0.063 | −0.138 | 0 |
| Pal 14 σ | +0.020 | −0.606 | 0 |
| cluster MID ΔΣ | +0.497 | −2.6e-9 | −0.902 |

- The rank is 3. Nothing in the action ties the three constants together.
- They are coupled through the measurements, because each later constant is read at a given a₀:
  - L★: d ln L★₉₅ / d ln a₀ = +0.065 (canonical) and +0.075 (alt). This is small.
  - u: d ln u / d ln a₀ = +0.55. This is large.

**The independent fitted constants of the screened theory are:**
- a₀, of which κ is a rewrite that needs ρ_Λ;
- L★, which so far has only a one-sided, calibration-dominated bound;
- u, which is fitted per scale (D6: u_gal ≥ 0.66), so it is a function rather than one number.

Inputs that are free but unobserved:
- η: no observable reaches it (A77).
- y_t: set by κ through the P5 posit (D7).
- β: bounded below 0.028 (A78).

Inputs taken from outside:
- the background quantities ρ_Λ/Λ, H₀ (which sets the distance convention), and Ω_c/Ω_b;
- the law form (n = 1 vs n = 2);
- calibrations: Υ_V and Υ_dSph, the β-model shape and f_s, M_gas and R500.

## 6. Forced relations (Part E): none

| candidate | status | source |
|---|---|---|
| L★ = σ_c²/a₀ | POSIT. No term in the action defines the tethered state, and σ is not one constant. | A76, D8, D8b |
| I(y_t) = 8π/κ² | POSIT (the P5 closure). It relabels κ. | D7 |
| u as a function of a₀ or L★ | NONE in the action. P4 is a posit; the a₀ dependence above is a measurement coupling. | THEORY P4, D6 |
| η = γ | NOT FORCED | A69, A77 |
| screening variable s = (8/3) r_h r_M / L★² | FORCED combination, but only a reparametrisation (d ln L★/d ln a₀ = −¼ at fixed s). It removes no constant and predicts no new number. | γ = KL★²/2, CFG691 |

## Errors and overstatements in the record (read-only; not edited)

- `doors_push_2026_10_22/BRIEF_E_AUDIT.md:8` and `deepseek_push/DS_FINAL_2026_10_21/THEORY.md:125` quote "L★ ≥ 24 pc"
  as the theory's floor. The number comes from ν_RAR plus the additive EFE recipe (`cfg820.py:16, :24`). It also rests
  on a single coherent Υ_V.
  - Native and isolated, the floor is 28.9 pc. With the recipe it is 23.9 pc.
  - Over ±1σ of Υ_V it spans 20–42 pc.
- `deepseek_push/DS_FINAL_2026_10_21/THEORY.md:63-64` says "u ≈ 0.47 inside [splashback] (measured)". Three corrections:
  - The value is measured at fixed radii, 0.46–1.42 Mpc.
  - The splashback label is ΛCDM-calibrated.
  - The value holds at κ = ½. At the galaxy-measured a₀ it is 0.433.
- `THEORY.md:69-70` and the §7 ledger (`"measured fractions: u ≈ 0.47"`) list u as an independent measured input.
  - Its measurement carries a₀ to the power +0.55.
  - The error that a₀ passes to u (0.059) is the largest term in u's error budget.

## What this does not show

- No field solve of the action's own external-field response for the globulars. The native floor lies between N2 and
  N1, 23.9 and 28.9 pc. D7d (screened Cassini) is the lane that is running the solver.
- The u brackets are declared sizes, not measured posteriors. The background swap is first order only (h only).
- CFG493's gas points were not re-reduced with ν_L. Only a bound on that term is given.
- The galaxy row of the Jacobian sets ∂/∂u = 0. That follows the record's construction (A71 fits baryons only), not a
  result proved here.

## Record checked

- BRIEF and BRIEF_E_AUDIT;
- the D5, D6, D7, D8 and D8b READMEs;
- THEORY.md P3–P5 and §7;
- the A81 report (ledger, rank and circularity);
- CFG493 (script and JSON), CFG886 (JSON), CFG820 and CFG821 (scripts and outputs), and the CFG691 table;
- D6's script (inversion and r_sp);
- the memory note on current κ measurements.

Not re-run: D5, D6's solver, D7, D8/D8b, A81 and D7d.
