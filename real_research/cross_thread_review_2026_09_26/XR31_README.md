# XR31 — is k04's "stable (F6)" right?

`kappa_closure/k04_four_form_promotion_consistency.py` (2fb80ca12) promotes a₀ to a four-form flux:
a₀ = β√G|q|, with P = Zq²/2. Its F6 records the construction as stable because the flux stiffness
Z_eff = Z + (2 − K_B)β²(sΔ − j)/(8π) is positive everywhere. XR20 (a075ad7f7) challenged this: F6 does not test the
slaved kernel, and under k04's kernel the slaved boost falls above y ≈ 2.4 / 2.3. This lane checks the challenge
independently, from k04's own definitions.

Script: `XR31_k04_f6_stability.py`. It writes its own `.out` and `_results.json`, plus `_MUTATE` versions. Nothing
outside the `XR31_*` files was edited. **κ = ½ stays FITTED.** Zt below is the four-form's coupling ratio, not the
framework's Z = 5.7888. Nothing here derives κ.

## The answer

**F6 is wrong as a stability claim. It is right only in a restricted sense.**

- **What F6 tests.** F6's Z_eff is the secant stiffness Π/q. Since F = sΔ − j = YJ_Y − J ≥ 0 for every kernel
  convex in Y, it satisfies Z_eff = Z(1 + cF) ≥ Z identically, so F6 cannot fail (A3). It holds on the very band where
  the construction is unstable (H3).
- **What stability needs.** The flux has no local mode: Π is constant in space and time, and q follows the scalar
  instantly. The scalar therefore obeys the reduced (Routh) Lagrangian L − Πq. The test is its longitudinal
  coefficient, C_L,eff = dg_N/dg_φ at fixed Π.
- **Under k04's own kernel and couplings the slaved kernel folds.** The slaved scalar force
  g_φ = a0_loc·Δ(g_N/a0_loc) peaks, then falls linearly to zero at the switch-off:

| case | fold y_f = g_N/a₀ | a0_loc/a₀ at the fold | switch-off y_off | C_L,eff on the saturated branch |
|---|---|---|---|---|
| k04, K_B = 0 (Z = 8β²; = XR20 "canonical") | **2.385081513** | 0.98908 | 155.234 | **−238.62** |
| k04, K_B = 0.25 | 2.402858081 | 0.99035 | 177.410 | −272.87 |
| tied alt footing (κ = 0.6043 on ρ_Λ, Zt = 2/κ², K_B = 0; = XR20 "alt") | 2.322851252 | 0.98460 | 106.289 | −163.05 |

- **Three routes agree on the fold to about 1e-12:**
  - A: the Legendre map q → Π at fixed Y degenerates, L_qq|_Y = 0 (40-digit differences of L itself).
  - B: double-precision root-finding of the coupled field equations, then the peak of u(y).
  - C: the dual (flux) Schur complement, 40 digits.
- **Why it folds.** k04's kernel is flat above s_sat = 2.540: the scalar force is bounded. A a0_loc that falls with g_N
  tilts that flat branch downward. On it, du/dy = −cD_sat²/(1 − c j_sat) exactly (A4, symbolic in c, D_sat, j_sat).
  So any kernel whose scalar force saturates folds under this four-form.
- **The restricted sense in which F6 is right.** The flux equation is well-posed (A5, H3):
  - it has exactly one root, 0 < a0_loc ≤ a₀, at every g_N, because 1 + c(F − sF') ≥ 0.993 in every case;
  - the flux stiffness at fixed matter flux stays positive (≥ 7.964 for Zt = 8);
  - q never reverses sign.

  That is all F6 establishes. The static solution exists and is unique; it is not stable in the band.

### Stability numbers (on the band y_f < y < y_off)

- **Static.** C_L,eff < 0 and C_T,eff > 0 at every band point. C_L,eff is −446.2 at y = 2.45 (the unsaturated slice)
  and −238.62 on the saturated branch (K_B = 0). Route B and route C agree to 2.5e-11, and route A's primal Schur
  complement agrees to 1e-9. The static scalar equation is therefore not elliptic, and a static solution in the band is
  a saddle of its energy.
- **Dynamical, the scalar's own sector.** ω²(k ∥ ∇φ)/ω²(k ⊥ ∇φ) = C_L,eff/C_T,eff. It is −6.76 at y = 20 and −116.6 at
  y = 2.45. For either sign of the inertia one channel grows, at a rate ∝ k (Hadamard).
- **Dynamical, in the chain root's committed quadratic form** (FP7 C1's T, V; α_c = 3.2e-9, c₂ = 7.29e-3, σ = 1),
  with C_φ = C_L,eff. There is exactly one negative root, and ω² ∝ k² to 2e-16:

| case | ω²/(ck)², λ = 1 | λ = 277 | λ = 1.07e7 | FP14 λ = 0: c₂ / c₂ → ∞ | e-fold at k = 1/kpc (λ = 1 / 1.07e7) |
|---|---|---|---|---|---|
| K_B = 0, saturated branch | **−0.857** | −0.430 | −2.23e-5 | −0.860 / −79.5 | 3.5e3 / 6.9e5 yr |
| K_B = 0, y = 2.45 | −1.60 | −0.805 | −4.17e-5 | −1.61 / −149 | 2.6e3 / 5.1e5 yr |
| K_B = 0.25, saturated | −0.980 | −0.492 | −2.55e-5 | −0.984 / −91.0 | 3.3e3 / 6.5e5 yr |
| tied alt, saturated | −0.586 | −0.294 | −1.52e-5 | −0.588 / −54.3 | 4.3e3 / 8.4e5 yr |

  - Controls at fixed a₀ (no four-form) have both roots positive, at y = 1 and in the saturated wall's limit.
  - For comparison, XR20's −1.67 (ck)² at y = 20 is for the root's own kernel J_P2, where C_L,eff = −466.
  - The rate depends on the inertia and on the khronon mixing; the sign does not.
- **The RAR itself stays monotone.** dg_obs/dg_N = 1 + du/dy ≥ 0.9958 (0.9939 tied alt). The fold is in the scalar's
  own force (the phantom), which is what the record's health condition reads (FP7 C1, FP14 X5). It does not show in
  g_obs.

### Where the band sits (FP0 footings a₀ = 9.3603e-11 / 1.1312e-10 m s⁻²; g_N at the fold 2.23e-10 / 2.70e-10)

- **SPARC** (FP1's cuts, 3389 points):

  | | Υ = 0.5 | Υ = 0.7 | Υ = 0.9 |
  |---|---|---|---|
  | canonical: share of points in the band | 13.5% | 17.0% | 20.4% |
  | canonical: galaxies with a band point | 38 | 48 | 55 |
  | alt: share of points in the band | 11.9% | 15.1% | 17.9% |
  | alt: galaxies with a band point | 35 | 42 | 50 |
  | tied alt: share of points in the band | 12.2% | 15.3% | 18.2% |

  One point (tied alt, Υ = 0.9) lies past the switch-off.
- **A solar-mass star.** The scalar is off inside 639 AU (canonical) / 581 AU (alt). An unstable shell runs out to
  5154 / 4689 AU in isolation.
  - With the Galactic field g_ext = 2.32e-10 (FP7 A4; y_ext = 1.845 / 1.433), the outer edge is 3871 AU
    anti-aligned, 6474 AU perpendicular and 10827 AU aligned (canonical).
  - All planets lie in the switched-off core, at y ≥ 5.8e4.
- **Wide binaries, 1.5 M☉:**

  | separation | canonical y | canonical: in the band? | alt y | alt: in the band? |
  |---|---|---|---|---|
  | 2 kAU | 23.76 | every orientation | 19.66 | every orientation |
  | 3 kAU | 10.56 | every orientation | 8.74 | every orientation |
  | 5 kAU | 3.80 | all but anti-aligned | 3.15 | all but anti-aligned |
  | 10 kAU | 0.95 | aligned side only | 0.79 | no |
  | 20 kAU | 0.24 | no | 0.20 | no |

### k04's other headline claims

| claim | depends on F6? | standing |
|---|---|---|
| F1 sign, F2 coefficient | no | Both live on the Y = 0 background (r = 1, outside the band): untouched. F2 stays k04's own FAIL. |
| F3 "RAR moves < 0.002 dex" | partly | The rows s = 0.01, 0.1, 1 lie below the fold and stand. The rows s = 2.54, 10, 100 lie in the band: they are numbers of an unstable static solution. Over SPARC the shift is ≤ 0.0010 dex below the fold and ≤ 0.0018 dex in the band. |
| F4 monopole screening | no, as a static statement | The planets sit in the switched-off core. The core is wrapped in the unstable shell, so the claim needs a stable exterior the construction lacks. **Side finding:** k04's text says the scalar is off "inside 205 AU"; g_N = 155.2 a₀ around 1 M☉ is at **639 AU** with k04's own a₀. This is a hard-coded slip; the verdict does not change. |
| F5 DR4 2 kAU bin (δγ_v = −0.019 / −0.015) | yes | The bin lies in the band on both footings. It is a number of an unstable solution, not a prediction. |

## Proposed correction note (for the coordinator; k04's files were not edited)

> **k04 F6 (correction proposed by XR31).**
>
> - F6's Z_eff = Z + (2 − K_B)β²(sΔ − j)/(8π) is the flux's secant stiffness Π/q. It is ≥ Z for every kernel
>   convex in Y (F = sΔ − j = YJ_Y − J ≥ 0) and cannot fail, so it does not test stability.
> - The test is the slaved scalar's longitudinal coefficient C_L,eff = dg_N/dg_φ at fixed Π.
> - On k04's own kernel and couplings (F3's Z = 8β²), the slaved force g_φ = a0_loc·Δ(g_N/a0_loc) peaks at
>   g_N = 2.385 a₀ (K_B = 0). The peak is at 2.403 a₀ for K_B = 0.25 and 2.323 a₀ with κ tied on the alt footing.
>   It then falls linearly to zero at 155.2 a₀ (177.4 and 106.3 respectively).
> - So C_L,eff < 0 on the whole band: −238.6 at 20 a₀. The static scalar equation is not elliptic there, and
>   longitudinal perturbations grow at a rate ∝ k. In the chain root's quadratic form, ω² = −0.86 (ck)² at λ = 1.
> - The band holds 17% / 15% of SPARC points (Υ = 0.7, canonical / alt). It also holds a shell from 639 to 5154 AU
>   around every solar-mass star, and wide binaries at 2–5 kAU.
> - "stable (F6)" should read: **"UNSTABLE for 2.39 < g_N/a₀ < 155: the four-form's feedback tilts the saturated
>   kernel's flat branch downward."**
> - F1–F2 are unaffected. F3's RAR shift stands below 2.39 a₀. F4's planets sit in the switched-off core, and "205 AU"
>   should read ≈ 639 AU. F5's 2 kAU number is computed on an unstable solution.
> - What F6 does establish: the flux equation has exactly one root, 0 < a0_loc ≤ a₀, at every g_N.

The same text is printed at the end of `XR31_k04_f6_stability.out` and stored as `correction_note` in the results
JSON.

## Relation to XR20

- **XR20's T2f is confirmed.** XR20's own script reproduces its committed T2f line verbatim (C1). It was run
  byte-identical from a scratch mirror with its inputs copied, and nothing in the repository was written.
- **The printed numbers are grid values.** XR20's 2.40 / 2.31 are argmaxes on its 400-point log grid, with steps of
  0.045 / 0.042. This lane's solver on that grid returns the same argmaxes (C1b). The precise folds are 2.3851 and 2.3229.
- **Conventions differ on the alt footing.** k04 kept Z/β² = 8 on both footings, so its fold is footing-free in y.
  XR20's "alt" ties κ = 0.6043 to the observed ρ_Λ, which is this lane's "tied alt" case.
- **Independence.** The derivation here (Routh reduction, Legendre map, dual Schur complement, saturated closed forms)
  was written from k04's code. XR20's code was only run as the cross-check.

## Checks

| run | result |
|---|---|
| main | 26/28 pass; 0 load-bearing failures; **rc = 0**. The two failures are pre-declared EXPECT FALSE reported checks: MONO (the slaved force is not monotone) and H7d (k04's 205 AU). |
| MUTATE | 17/28 pass; **rc = 1**. Route B's slaved law is replaced by its running maximum, a kernel made monotone by hand. MONO then passes, and every fold-requiring check fails: H1 ×3, H4, H5, H6c, H7b, H7c, H7e. Controls, algebra, H2, H3 and H5c still pass. |

Controls:
- **C0:** k04's own script reproduces its committed `.out` verbatim (27 lines, rc = 0).
- **C0b:** route B reproduces k04's F3 rows (K_B = 0, 0.25) and F5 rows (both footings) to the printed digits.
- **C1 / C1b:** XR20's T2f line, as above.
- **C2:** 175 galaxies, and FP7's 3391 points under FP7's own selection.
- **C3:** s_sat = 2.539638, Δ_sat = 0.647610 and j_sat = 0.452525 match k01 / k04.

## Pre-declaration, disclosures, scope

- **Hypotheses.** H0–H7, MONO and the MUTATE design were written into the docstring before any code of the lane ran.
  They came from pencil algebra, informed by XR20's reported 2.40 / 2.31.
- **Run 1** (MUTATE, debug) completed with rc = 1 but exposed three problems:
  - **C2 was mis-specified.** FP7's 3391 counts V_obs > 0 and errV > 0, with no g_bar > 0 cut. FP1's RAR cuts leave 3389
    points at Υ = 0.7. C2 was re-specified to reproduce FP7's own selection, and 3389 is printed beside it.
  - **The envelope cap was misplaced.** A bounded minimiser put it 4.5e-4 past the true peak (K0), leaving a sliver of
    non-monotone law. The cap now sits 1e-6 below the bracketed peak.
  - **The stencil did not cancel.** The 4-point stencil did not cancel exactly on flat stretches (rounding of 7u − 8u).
    It is now written in differences.

  No hypothesis text or threshold changed.
- **Run 2** was a complete pair: MUTATE rc = 1, then main rc = 0.
- **Run 3** is the kept pair, run in the order MUTATE then main. Before it, the note's wording "(Z_eff/β² = 8)" was
  corrected to "(F3's Z = 8β²)", and H5 gained an explicit test of the k² scaling behind its pre-declared "rate ∝ k"
  wording. Every number is identical to run 2; the run-3 main `.out` differs from run 2's only in those two lines.
- **Scope.**
  - k04 does not write its candidate action's perturbation dynamics. The sign of the instability is kernel-generic:
    the scalar-sector ratio above, and FP7 C1's theorem that health requires C_φ > 0 in each channel.
  - The rates are quoted in the chain root's committed quadratic form (FP7 C1, FP14 L2).
  - The nonlinear fate of the band (what state replaces the saddle) is not computed.
  - Discs are not re-solved; the RAR numbers are spherical.

## Reproduction

From the repository root (a few seconds each; one thread):
```
MUTATE=1 python3 real_research/cross_thread_review_2026_09_26/XR31_k04_f6_stability.py
python3 real_research/cross_thread_review_2026_09_26/XR31_k04_f6_stability.py
```
The XR20 cross-check writes only into `XR31_SCRATCH` if that is set, and otherwise into a system temporary directory.
