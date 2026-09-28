# AS019 — Deep-law source mass conventions

**Run:** `run_AS019-r1-20260927T2259` · **Worker:** `sa-8-0915d4c9` (Hermes subagent; model `deepseek/deepseek-v4-flash-0731` via openrouter) · **Branch:** CORE scale identities (this result is kernel-agnostic in the deep limit; the finite-field flip tables are quoted per branch — Q, RAR, MU2, EXP, MONO — and labelled)
**Task SHA-256:** `7df4433219f25790668c1b20f7814c66358616538a0e4357a715f303a33006e5`

Sources pinned (all match `SOURCE_MANIFEST.json`): README.md `91a5fac4…6b6ed` ✓ · qwen_claude_field_theory/closure_2026/FRIED_CHICKEN_SPEC.md `98d9149f…8e3f` ✓ · campaign_fresh_gravity_astra/DERIVATIONS.md `8da8176e…b889` ✓ · STANDING.md `660462eb…bf63` (consulted) · opus_48_extended_research/reviews/collective_efe/COLLECTIVE_EFE_CLUMPY_VS_SMOOTH_VERDICT_2026-06-20.md (evidence for the spherical enclosed-mass theorem; not manifest-pinned).

---

## 1. Precise claim, symbol dictionary, boundary conditions, assumptions

**Task claim (audited statement).** In the deep law `v_flat⁴ = G·M_b·a0` and the transition radius `r_M = √(G·M_b/a0)`, the mass that enters is the **enclosed baryonic mass at the evaluation radius**, `M_b(<r)`, under the spherical shell-theorem convention `B(r) = G_N·M_b(<r)/r²`; the *total* mass may be substituted **only outside the baryonic edge**, where `M_b(<r) = M_b^tot` has settled. Flipping the catalog convention `M → λM` (any partial-component quotation: disk-only, disk+bulge, disk+bulge+gas) has exact, quantified consequences: deep speed ratio `λ^(1/4)`, `r_M` ratio `λ^(1/2)`, kernel argument ratio `λ` at fixed radius, inferred-`a0` inflation `λ`, and flat-region degeneracy with a `κ → λκ` renormalisation; a flip that changes the *radial profile* of the enclosed mass is **not** renormalisation-degenerate.

**Symbols** (all parameters positive reals; SI units):
| symbol | meaning |
|---|---|
| `B(r)` | baryonic (Newtonian-equivalent) radial acceleration at radius `r` |
| `M_b(<r)` | enclosed baryonic mass inside radius `r` (spherical convention) |
| `M_b^tot`, `M_d`, `M_bulge`, `M_gas` | total / disk / bulge / gas baryonic masses |
| `ρ_b(r)`, `ρ` | 3-D baryonic density; constant density |
| `G_N` | **measured** Newton coupling (framework matching condition); `G_bare`, `G_cosmo` kept separate symbols |
| `a0` | vacuum acceleration scale, `a0 = κ c √(G_N ρ_Λ)`, `κ = 1/2` **adopted** (not derived here) |
| `r_M(M)` | `√(G_N·M/a0)` |
| `y` | kernel argument `B/a0` |
| `ν_RAR, ν_mono, μ2, μ_EXP, h_RAR, h_mono, δ, y*, y_p` | branch kernels per FRAMEWORK_CONTRACT |

**Boundary conditions / solution class.** Static, spherically symmetric baryonic distribution; circular orbits; all five branches evaluated in the spherical unfiltered reduction for the finite-field tables; the operative filtered-MONO statement is the *deep-limit shared result* plus a labelled open transfer (Sections 7, 10). No observational fit is performed; the galaxy-like model used for the flip tables is a **labelled illustrative sample**, not a catalog row.

**Framework inputs vs conclusions.** Inputs: `κ = ½`, both a0 footings, `G_N`, `M_sun`, `pc`, `c`, the branch kernels. Conclusions established here: identity (2), slope identity (4), flip identities (7)–(11), flatness condition (6), λ–κ degeneracy (12), all Lean-certified (Section 11) and numerically cross-checked (Section 8).

---

## 2. Running circular speed for nonconstant M_b(<r); total-vs-enclosed condition

**Premise (spherical enclosed-mass theorem).** For any spherically symmetric baryon distribution, the shell theorem gives exactly

```
B(r) = G_N · M_b(<r) / r² ,   M_b(<r) = 4π ∫₀^r ρ_b(x) x² dx .      (1)
```

This is the convention used by DERIVATIONS.md §3 (`B = G_N M_b(<r)/r²` in the X-COP/SPARC-style inversions) and by the collective-EFE enclosed-mass review; it is the premise to be audited and its flip consequences quantified.

**Deep-limit derivation.** Every branch shares the deep limit `g = √(a0·B)` (Section 6), hence for a circular orbit (`v² = r·g`):

```
v⁴(r) = r²·g² = r²·a0·B(r) = G_N·a0·M_b(<r) .                    (2)
```

**Logarithmic slope.** Differentiating `v = (G_N a0 M_b(<r))^(1/4)`:

```
d ln v / d ln r = (1/4) · (r/M)·(d M/d r) = (1/4) · 4π r³ ρ_b(r) / M_b(<r) .   (4)
```

(same-theory note: (2) and (4) hold on any of Q/RAR/MU2/EXP/MONO in the deep bin, because all five reduce to `g² = a0·B` there — a shared deep limit does not make them the same finite law, per the branch discipline.)

**Condition for using the total mass.** With `M_b(<r) = M_b^tot` for `r ≥ r_edge` (radius enclosing all baryons), the flat law `v_flat⁴ = G_N·a0·M_b^tot` is the correct reading of (2) iff the evaluation radius is in the settled region; quantitively, combining (2) with the total law gives the **exact** ratio

```
( v(r) / v_flat )⁴ = M_b(<r) / M_b^tot ,                          (6)
```

so to keep the flat law within a relative speed tolerance `±ε` one needs `(1−ε)⁴ ≤ M_b(<r)/M_b^tot ≤ (1+ε)⁴`; e.g. `ε = 1%` requires `M_b(<r) ≥ 0.9606·M_b^tot`. A useful scale: this is attained for `r ≳` a few half-mass radii; the *slope* criterion `|d ln M_b(<r)/d ln r| ≪ 1` over the sampled annulus is the local version.

**r_M bookkeeping.** `r_M(M) = √(G_N·M/a0)` is the radius where `B = a0` for a *settled* mass `M`; inside a distribution it is the radius where `M_b(<r)` reaches `a0 r²/G_N`. Under a convention flip `M → λM`:

```
r_M(λM)² = λ·r_M(M)² .                                          (11)
```

---

## 3. Convention-flip taxonomy and exact consequences

**Catalog conventions.** `D` (disk, stellar only), `DB` (disk+bulge), `DBG` (disk+bulge+gas = full baryonic total). Define component ratios

```
μ_b = M_bulge/M_d ,  μ_g = M_gas/M_d ,  λ = (1 + μ_b + μ_g) = M_DBG/M_D .     (7)
```

**Flip consequences (exact, λ > 0):**

```
v_flat(λM)/v_flat(M)  = λ^(1/4)                      (8)   [deep speed]
r_M(λM)/r_M(M)        = λ^(1/2)                      (9)   [transition radius]
y(λM; r)/y(M; r)      = λ        (fixed r, fixed geometry)  [kernel argument]
a0_est(λM)            = λ·a0     (if a0 is *inferred* from v⁴/(G·M_cat))   (10)
```

(8) follows from `v⁴ = G·a0·M`; (10) from `a0_est = v_flat⁴/(G·M_cat)` with `M_cat = M_true/λ`.

**Degeneracy with κ.** In the settled flat region `v_flat⁴ = G·(a0·M)` fixes only the product: `M → λM` at fixed a0 produces **the identical flat curve** as `a0 → λa0` (i.e. `κ → λκ`) at fixed M. Since κ is a fitted input in this framework, **flat-region data alone cannot separate the mass convention from a κ error.** Two consequences:
- *calibration:* under-reporting baryons by λ inflates an inferred a0 by λ (10);
- *profiles break the degeneracy:* because a0 is a scalar, an a0-rescale renormalises the *argument profile* `y(r) = G_N·M(<r)/(a0 r²)` by a constant factor; a convention flip that changes the **radial profile** of `M(<r)` (e.g. bulge stripped, DM excluded, a component edge mis-located) yields a `y(r)`-profile ratio that *varies* with `r`, which no constant λ-rescale can mimic. Numerically (Section 8.4): for the illustrative bulge-stripped flip, the best constant rescale leaves a max log-residual 5.57 (i.e. >10² in y) over `[1.01 r₁, 0.9 R₂]` — the profile flip is **not** degenerate.

**How each branch is written in terms of M_b.** With `B(r) = G_N·M_b(<r)/r²` the branches read (spherical reduction; MONO through its defining splice):

| branch | equation | deep limit `g → √(a0 B)`? |
|---|---|---|
| Q | `g² = B² + a0·B` | yes (neglect of `B²` at `B ≪ a0`) |
| RAR | `g = B·ν_RAR(y)`, `ν_RAR(y) = 1/(1−e^{−√y})`, `y = B/a0` | yes: `ν_RAR(y) → 1/√y` |
| MU2 | `μ2(x)·g = B`, `μ2(x) = 1−(1+x/2)^{−2}`, `x = g/a0` | yes: `μ2(x) → x` |
| EXP | `μ_EXP(x)·g = B`, `μ_EXP(x) = 1−e^{−x}` (historical, retired) | yes |
| MONO | `g = B·ν_mono(y)`, `ν_mono = ν_RAR` below `y*`, log-continuation above (Splice numbers recomputed: `y* = 2.3374124…`, `y_p = 2.5396383…`, `h_p = 0.6476102…`, `δ = 0.05` — matching AS006’s certified `y*` and the contract landmarks) | yes |

Because the deep limit is branch-independent, **the mass-convention identities (2), (4), (6), (8)–(11) are branch-independent.** At finite field the flip enters through `y`; the per-branch table (Section 8.5) shows the resulting fractional changes of the observable, which differ by branch.

**G bookkeeping.** The kernel argument uses the *measured* Newton coupling: `y = G_N·M_b(<r)/(a0·r²)`, `r_M = √(G_N·M_b/a0)` (matching-condition usage). `G_bare` and `G_cosmo` remain separate symbols; if the framework identity forces `Λ_eff = 32π·(G_E/G_N)·a0²/c⁴` with `G_E ≠ G_N`, the λ-degeneracy of Section 3 generalises to a joint `(G_N, M, a0)` product degeneracy `G_N·a0·M_b = const` in the flat region — the audit therefore keeps the three couplings symbolically distinct (contract discipline).

---

## 4. Footing-preserving dimensional examples

`G_N = 6.67430e-11`, `c = 299792458`, `M_sun = 1.98847e30`, `pc = 3.085677581491367e16`, `k_B` not used (no temperature). Both footings separate (from `raw_output.json`):

| quantity | canonical `a0 = 9.3619e-11` | alternative `a0 = 1.1279e-10` |
|---|---|---|
| `r_M(1e9 M_sun)` | 1220.2 pc | 1111.7 pc |
| `r_M(1e11 M_sun)` | 12.202 kpc | 11.117 kpc |
| `r_M(1e13 M_sun)` | 122.02 kpc | 111.17 kpc |
| `v_flat(1e9 M_sun)` | 59.37 km/s | 62.20 km/s |
| `v_flat(1e11 M_sun)` | 187.75 km/s | 196.70 km/s |
| `v_flat(1e13 M_sun)` | 593.71 km/s | 622.01 km/s |
| `r_M` flip ratio `√λ` (λ = 23/15) | 1.2383 | 1.2383 (footing-independent) |
| deep-speed flip ratio `λ^(1/4)` | 1.1128 | 1.1128 (footing-independent) |

The dimensionless flip identities apply as stated to **both** footings; every dimensional number above is quoted on both, per the mandate.

---

## 5. Negative control

**Control (mandated): “apply the total mass inside a uniform-density baryon sphere and detect the wrong radial power.”** Uniform sphere `ρ = 10⁻²¹ kg/m³`, `R = 20 pc` (deep across the whole interior: `B(R)/a0 ≤ 1.8e-3`, section 1 of the script asserts deep-regime entry). Three conventions for the running circular speed:

| convention | formula | fitted log-log slope over [0.02R, 0.30R] | expected | residual |
|---|---|---|---|
| enclosed (correct) | `v⁴ = G_N a0 (4π/3)ρ r³` | 0.75000000 (canonical), 0.75000000 (alt) | 3/4 | 1.0e-15 |
| **wrong: total inserted** | `v⁴ = G_N a0 M_tot` (const) | 0.00000000 | 0 | 0 |
| Newtonian (regime check) | `v² = G_N M(<r)/r` | 1.00000000 | 1 | 1.6e-15 |

**The wrong convention is caught by the radial power: 0 ≠ 3/4** (and both differ from the Newtonian solid-body 1). The three powers are all analytically exact and Lean-certified (Section 11, theorems 3–5).

**Second control (limiting regimes).** Deep limit: identity (2) verified numerically at `B/a0` from `1.8e-3` down to `1e-6` (uniform sphere interior) — the log-slope 3/4 is exact at every point of the sampled decade (residuals ≈ 1e-15); Newtonian limit: slope 1, verified to 1.6e-15. These are exact identities checked at finite precision, not finite numerical coincidences (per the controls note: “distinguish an exact identity from a finite numerical consistency check” — Section 8 reports residuals from a second representation).

---

## 6. Deep and Newtonian limits: leading neglected term

The deep-law statement (2) is exact *by construction* `g = √(a0 B)`; the suppression of the neglected term `B²` in Q is `B/(B+a0)`, i.e. relative `O(B/a0)` (**err = B/(B+a0)**, at most `0.18%` at the sphere edge, `~1e-6` at `B/a0 = 1e-6`, where the fit was run). For RAR/MONO the relative correction to `ν·B` at deep `y` is `1 − ν√y ≈ √y·(1 + √y/2)·… = O(y)` (from `ν_RAR(y) = 1/√y + 1/2 + √y/12 + …`) → for MONO the RAR tail dominates to `y* = 2.3374124` and the continuation adds ≤ 0.0104 dex per the contract; the mass-convention identities are unaffected because they are limit statements.

---

## 7. Representation-independence check (step 4): second representation

1. **Shell theorem by quadrature.** `B(r) = G_N·M(<r)/r²` recomputed by direct Simpson quadrature of the density shells (2000-point grid) at `r ∈ {0.05R, 0.13R, 0.27R}`: relative residuals vs the closed form `{9.1e-16, −1.4e-16, 6.8e-16}`, tolerance `1e-10` — **PASS**.
2. **Slope identity (4) for a non-power-law model.** Two-component bulge+disk model (uniform core `ρ₁ = 1e-20 kg/m³`, `r₁ = 2 kpc`; envelope `ρ₂ = 3e-22 kg/m³·(r/r₁)^{−2}`, truncated at 25 kpc): numeric log-slope of `(G_N a0 M(<r))^{1/4}` via symmetric 4-point differences on a 32001-point grid vs the analytic RHS of (4). Max relative residual `3.65e-8` (canonical) / `3.66e-8` (alternative) on the full domain; `3.59e-8` / `3.58e-8` away from the 3% boundary layer at the density kink `r₁`; tolerance `1e-7` — **PASS** (the kink-adjacent deviation is finite-difference truncation across a discontinuous density, not an identity failure; scale check: 4001→16001→32001 points reduce the max residual 2.3e-6 → 1.5e-7 → 3.7e-8, consistent with the O(h⁴) envelope of the 4-point rule).
3. **Flat-region product degeneracy.** `v_flat(a0, λM) − v_flat(λa0, M) = 0.0` exactly (deviation 0.0 km/s, tolerance 1e-9) — **PASS**: the flip is exactly a κ (a0) rescale in the settled region.

---

## 8. Convention-flip numerics (finite field, all five branches; single illustrative galaxy, labelled sample)

Model: `M_core = 1.58e10 M_sun` bulge (`r₁ = 2 kpc`), envelope to 25 kpc, `M_tot = 2.21e10 M_sun`; point A = transition radius with `y_true = 1.10` (canonical; bisected at `r = 2.62 kpc`), point B = deep disk (`r = 12 kpc`, `y_true = 0.074` canonical / 0.0616 alt). Three convention readings of the same physical field: (a) true, (b) constant-scale flip `B/λ`, (c) bulge-stripped `G_N·M_env(<r)/r²`. Flip ratios `g_reading/g_true` per branch:

| point (footing) | Q | RAR | MU2 | EXP | MONO | deep-limit value |
|---|---|---|---|---|---|---|
| A cons-scale (can.) | 0.7303 | 0.7416 | 0.7433 | 0.7522 | 0.7416 | (√(1/λ)=0.8076) |
| A strip (can.) | 0.1158 | 0.1116 | 0.1163 | 0.1257 | 0.1116 | 0.1654 |
| B cons-scale (can.) | 0.7978 | 0.7875 | 0.7910 | 0.7960 | 0.7875 | 0.8076 |
| B strip (can.) | 0.5436 | 0.5256 | 0.5317 | 0.5386 | 0.5256 | 0.5571 |
| A cons-scale (alt.) | 0.7375 | 0.7463 | 0.7489 | 0.7585 | 0.7463 | 0.8076 |
| B strip (alt.) | 0.5458 | 0.5282 | 0.5337 | 0.5404 | 0.5282 | 0.5571 |

Reading: (i) at the transition point the constant-scale flip under-predicts the observed acceleration by 25–27%, *larger* than the deep-limit 19% — the finite-kernel response is more sensitive at `y ~ 1` than the deep limit; (ii) at the deep point all branches sit within 1–2% of the shared deep-limit ratio, demonstrating the branch-independence of (8) in the deep bin; (iii) MONO = RAR identically at both points (both `y < y*`), as constructed; (iv) the bulge-stripped flip at point A suppresses ~88% of the field (bulge = 97% of enclosed mass at 2.6 kpc) — the profile-changing flip is a first-order effect, invisible to catalog-level total-mass bookkeeping.

---

## 9. What changed, precisely, when the convention flips

1. `v_flat`: ×`λ^(1/4)` (e.g. ×1.1128 for the illustrative λ = 23/15).
2. `r_M`: ×`λ^(1/2)` (e.g. ×1.2383).
3. Kernel argument `y(r) = B/a0` at fixed physical field point: ×λ (constant-profile flip) or ×λ(r) (profile-changing flip).
4. Inferred `a0` from a flat-region fit: ×λ (calibration consequence).
5. Transition-region observable `g` at fixed r: per-branch tables above (finite-field correction larger than the deep-limit value at `y ~ 1`).
6. The profile-flip is **not** renormalisation-degenerate (max log-residual 5.57 after best constant rescale), the constant-profile flip is exactly degenerate with `κ → λκ` (deviation 0.0).

---

## 10. Strongest surviving statement and next implication

**Strongest statement (scope: static spherical enclosed-mass convention, deep and transition bins, all five branches, both footings).** Let `B = G_N·M_b(<r)/r²`. Then in the deep bin every branch satisfies `v⁴(r) = G_N·a0·M_b(<r)` with log slope (1/4)·`(4πr³ρ_b/M_b)`, the total law is admissible iff the enclosed mass has settled to the flatness tolerance (6), and the convention-flip identities (8)–(11) hold exactly, with the λ–κ flat-region degeneracy and the profile-flip non-degeneracy. All identities are Lean-certified (Section 11) with numerical residuals `≤ 3.7e-8`; the wrong-total negative control returns the wrong radial power (0 vs 3/4), as mandated.

**Next unresolved implication (first missing bridge to the operative MONO target).** The audit proves the convention identities for the *spherical enclosed idealisation* `B = G_N·M_b(<r)/r²`. For the operative filtered system (`∇²u = 4πG ρ_b`, `∇²Φ = 4πG ρ_b + S*·div[(ν_mono(|∇Su|/a0) − 1)∇Su]`, `S = e^{(ξ²/2)Δ}`) with an **extended axisymmetric disk+bulge source**, the mass entering the kernel argument is `|∇S u|` — a *filtered* functional of the full density, not the raw enclosed monopole. The missing bridge: **prove that for the extended source `|∇S u(r)|/a0 = G_N·M_b(<r)/(a0 r²)·(1+ε(r))` with a quantified `|ε|` (filter-scale and flattening corrections), and state the radius beyond which the enclosed-sphere convention (2) reproduces the filtered circular speed to a stated tolerance.** This is the convention audit’s transfer to the operative gate; it is exactly the composition left open by AS006.C01 (point-source exterior — not dispatched) and AS007.C01 (compact-source far field with `r ≫ max(r_M, ξ)` — not dispatched) for the *intermediate* region inside the mass distribution; child `AS019.C01` (written, not dispatched) targets it with the disk+bulge profile.

---

## 11. Lean 4 certificate

File: `AS019_deep_mass_slopes.lean` (in run dir; canonical copy at `fable_independent_2026/lean_2026/`). Verified: `cd fable_independent_2026/lean_2026 && lake env lean <abs path>.lean` — exit 0, **zero `sorry`**, **`#print axioms` = {propext, Classical.choice, Quot.sound} for all seven theorems** (hard bar met).

| theorem | statement |
|---|---|
| `deep_log_slope_identity` | `v⁴ = C·M(r)` (C > 0), `M, v` differentiable, `M(r), v(r) > 0` ⟹ `v'·r/v = (M'·r)/(4·M)` (the slope identity (4)) |
| `uniform_sphere_deep_slope_three_quarters` | `M(r) = k r³` ⟹ slope `3/4` |
| `total_convention_deep_slope_zero` | `M ≡ M_tot` (wrong convention) ⟹ slope `0` — the negative control |
| `uniform_sphere_newtonian_slope_one` | `v² = C·k·r²` ⟹ slope `1` (Newtonian regime check) |
| `flip_speed_fourth_ratio` | `M₂ = λM₁, vᵢ⁴ = C·Mᵢ (C > 0, M₁ > 0)` ⟹ `(v₂/v₁)⁴ = λ` ((8)) |
| `flatness_violation_ratio` | `(v/v_flat)⁴ = M(<r)/M_tot` ((6)) |
| `rM_flip_square_ratio` | `r_M(λM)² = λ·r_M(M)²` ((11)) |

All derivatives are ordinary (HasDerivAt) calculus on ℝ; all powers are natural powers; positivity states the physical domain. No observational statement is Lean-certified (the Lean file certifies the algebra).

---

## 12. Controls that were capable of failing — evidence

| control | mechanism | result |
|---|---|---|
| wrong-total radial power | total-vs-enclosed inside a uniform sphere | **failed as designed**: slope 0 vs 3/4 (0 vs correct), both footings; also vs Newtonian 1 |
| deep/Newtonian limiting regimes | slopes over a decade of r at `B/a0 ≤ 1.8e-3` | exact to 1e-15; leading neglected term `B/(B+a0) = O(B/a0)` stated |
| second representation | Simpson shell quadrature vs closed form | residuals ≤ 9.1e-16, tolerance 1e-10 |
| slope identity on non-power-law profile | 4-point differences vs analytic RHS (4) on 32001 pts | max 3.65e-8, tolerance 1e-7 (boundary-layer documented) |
| flat-region degeneracy | `v_flat(a0, λM) = v_flat(λa0, M)` | deviation 0.0 (exact) |
| profile-flip non-degeneracy | best constant rescale of the stripped y-profile | log-residual 5.57 ≫ 0 — survived as designed |

## 13. Limitations

- The finite-field flip tables use one **labelled illustrative** galaxy model (2-component spherical bulge+disk); they demonstrate the exact per-branch scaling but are not a catalog study — no data, no fit (per the task).
- The audit is restricted to the spherical enclosed convention; disks are treated only through the label (non-spherical Newtonian fields excluded — the child).
- The operative filtered-MONO transfer is not proved here (open implication, Section 10).
- No branch is imported to repair anything; MONO is the operative branch label, Q/RAR/MU2/EXP remain labelled comparisons at finite field, and the deep identities are branch-shared by the shared-limit theorem (AS030 discipline).
- κ = 1/2 remains adopted input; nothing here derives it.