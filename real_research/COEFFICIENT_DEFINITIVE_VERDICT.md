# Definitive verdict: can Z = √(32π/3) be derived from horizon entropy?

*Two independent ultrathink workflows (11 derivation routes + 5 proof/no-go approaches, 26 agents, every identity
re-derived from scratch in sympy, adversarially verified, cross-checked against 2025–2026 primary literature).
**C. Zimmerman independently re-verified the load-bearing claims.** Both workflows converged.*

## The answer, in one sentence

**No — and provably not.** Horizon thermodynamics **forces** the *form* (`Y^{3/2}`, the deep-MOND √-law) and the
*scale* (`a₀ ∼ c√(Gρ_Λ)`), but the O(1) coefficient `κ` in `a₀ = κ·c√(Gρ_Λ)` is **structurally unfixable** by
equilibrium horizon entropy; the framework's value corresponds **only** to the kinematic choice `κ = ½`, which no
thermodynamic argument can select. This is not "unsolved pending more work" — it is **provably route-dependent**.

## The proof (three independent results, each sufficient, all sympy-verified)

**(a) The "32π = 4 × 8π" framing collapses to a single rational ½.** Substituting Einstein's `ρ_Λ = Λc²/8πG` gives
the exact identity `a₀ = (c/2)√(Gρ_Λ)`, i.e. **κ = ½ exactly** (sympy `solve`, `difference = 0`). The entire disputed
"extra 4" is identically `1/κ² = (1/½)²` — an inverse-square velocity prefactor, a kinematic normalization.

**(b) The de Sitter entropy's one Bekenstein–Hawking ¼ is already spent making Einstein gravity.** From Jacobson's
own result (gr-qc/9504004, `η = 1/4ℏG ⟹ 8πG`, sympy-verified), **`8π = 2π(Unruh) × 4(= 1/[the BH ¼])`**. The single
horizon quarter lives *inside* Einstein's coupling. So `32π = 4 × 8π` demands a **second, independent** factor of 4 —
and the devil's-advocate exhaustion shows **every candidate structure gives the wrong number**:

| candidate "second ¼" structure | resulting Z | vs 5.789 |
|---|---|---|
| two horizons (sum of radii), factor 2 | 2.00 | ✗ |
| squared / Debye entropy `S²`, `a₀∼S^{−½}` | √2 = 1.41 | ✗ |
| **literal second BH ¼ (κ = ¼)** | **11.58** | ✗ (off ~2×) |
| de Sitter surface gravity `c²/2R` | 2.00 (or 12 for `²`) | ✗ |
| active gravitational mass `(ρ+3p) = −2ρ_Λ` | 4.09 | ✗ |
| **free-fall / surface-gravity κ = ½** | **5.789** | ✓ — *the only one* |

A literal second ¼ gives **11.58, not 5.79**. The only thing that lands the framework's value is the rational `κ = ½`
inserted by the free-fall convention.

**(c) Number-field no-go: `√(32π/3) ∉ ℚ(π)` (valuation proof).** Every horizon-thermodynamic constant (Unruh `1/2π`,
BH `¼`, area `4πR²`, equipartition `½`, Friedmann `⅓`, integer dimension counts) lies in `ℚ(π)`. Treating π as
transcendental (`ℚ(π) ≅ ℚ(t)`), the radicand `32t/3` has a **simple zero at t = 0 → valuation 1 (odd)**; every square
in `ℚ(t)` has even valuation everywhere. So `32π/3` is not a square and **`√(32π/3) ∉ ℚ(π)`** — the irreducible `√π`
in `Z` can arise *only* from `√(Gρ_Λ)` (the forced density step, giving `√(8π/3)`), and the leftover prefactor `κ` is
a pure rational that thermodynamics produces in **infinitely many values** (`1/2π, 1/2, 1/4, 1/6, 2, …`) without
selecting one.

## Three realization-independent backstops (why it's route-dependent, not merely route-by-route unsolved)

1. **ℏ⁰ fingerprint.** `a₀ = c²√(Λ/32π)` carries **ℏ⁰** (classical); every thermal/saddle quantity (`T_GH`, `S_dS`,
   `I_E`) carries ℏ. The "thermal ratio" `T_dS/T_Unruh(a₀) = 5.789` is just `cH_Λ/a₀ = Z` **restated — a tautology**,
   not a derivation.
2. **AeST saddle blindness (the structural heart).** `a₀` enters AeST *only* as the normalization of `|Y|^{3/2}`, and
   `Y = q^{μν}∂_μφ∂_νφ` **vanishes identically on any FRW/de Sitter background** (`q⁰⁰ = g⁰⁰ + (A⁰)² = −1+1 = 0`). The
   Gibbons–Hawking partition function depends only on Λ — **the MOND normalization is literally absent from the
   on-shell action**, and `Y^{3/2}` is non-analytic at `Y=0` so one-loop fluctuations don't resurrect it. *The horizon
   knows Λ; it cannot see a₀.* This is the **same `Ȳ=0` fact that makes the framework CMB-safe** — the property that
   protects the CMB is the property that hides the coefficient.
3. **Scale-invariance.** Milgrom's deep-MOND limit is invariant under `(t,r) → (λt,λr)` (rescaling `a → a/λ`) — *the
   symmetry that defines the MOND limit cannot fix the scale that breaks it.*

## The meta-pattern (every route's Z) — and the company you're in

The principled routes split into two clusters; **5.789 sits at the bottom of the upper one, reachable only by
inserting the free-fall ½:** Milgrom `½` · naive horizon `1` · surface gravity `2` · vacuum free-fall `√(8π/3)=2.89` ·
**framework `√(32π/3)=5.79`** · Verlinde `6` · thermal `2π=6.28`. The data band `Z ∈ [4.2, 6.0]` admits 5.79, 6.0, and
2π **simultaneously** — it pins nothing. And the **entire 2025–2026 literature agrees**: Milgrom himself ("de Sitter
*does not tell us which* acceleration parameter is a₀… not backed by a concrete mechanism"), Verlinde (matched, not
derived), Skordis–Złośnik (a₀ = free normalization of `|Y|^{3/2}`), Singh 2026 (`a₀ = c²/(ξℓ_dS)`, ξ "O(1) fixed by
matching"). **Nobody derives the coefficient. Everybody matches it. The framework is at the frontier, not behind it.**

## Disposition

- **Own 32π as a well-motivated, data-selected convention.** The scale (`a₀ ∼ c²√Λ`) and the ballpark (`Z ∼ 5–6`,
  excluding the naive 1–3) are **forced and data-selected** — *not numerology*. The last factor (`κ = ½`, the extra 4,
  the 32π-vs-2π) is a **free-fall / surface-gravity kinematic convention**, a posit at the ~8% level (below the
  ~20–30% interpolating-function systematic), **not** a forced second Bekenstein–Hawking ¼.
- **Moot for the empirical program.** The coefficient-free bridge `a₀(z)/a₀(0) = √(ρ_DE(z)/ρ_DE0)` **cancels Z
  entirely** — the z~3 evolution (β) test does not depend on whether the residual is 32π/3 or 2π.
- **`OPEN_PROBLEM_yphi32_KQ.md` item D is closed as a rigorous null.** Items A/B/C (the form, the inertia↔gravity
  equivalence, the 𝒦(𝒬) cosmology) remain genuinely open; the coefficient is **structurally unfixable** by equilibrium
  horizon thermodynamics.
- **The one bounded thing that could still close it** (outside the homogeneous saddle, which is *why* the homogeneous
  entropy can't): a covariant `O(ε³)` on-shell free-energy computation of the `C(𝒬)Y^{3/2}` vertex on a **strained
  (inhomogeneous) de Sitter horizon**, checking whether the strain trace leaves the sphere-volume `4/3` uncancelled
  and pins `κ=½`. Until that exists, the coefficient is a convention.

**Bottom line:** this is a rigorous, satisfying null. The coefficient is not derivable from horizon entropy — by
anyone, by a structural obstruction (the `Ȳ=0` saddle-blindness + the number-field no-go), not by lack of effort — and
it costs the framework nothing, because every falsifiable test is coefficient-free.
