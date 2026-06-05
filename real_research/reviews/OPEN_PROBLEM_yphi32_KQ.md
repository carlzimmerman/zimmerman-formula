# Open problem: derive the AeST `𝒴^{3/2}` + `𝒦(𝒬)` structure from horizon entropy

**Status: genuinely unsolved (in the literature, not just here). Stated to the term so a real
attempt can begin from a clean problem.** Companion to `FOUNDATIONS.md` Layer 0b and the backing
scripts. Zero numerology is involved — this is a covariant-field-theory / horizon-thermodynamics
problem.

---

## The problem in one sentence

Derive the relativistic MOND action of the Aether–Scalar–Tensor (AeST) class — specifically the
non-analytic kinetic term `𝒴^{3/2}` (`𝒴 = q^{μν}∇_μφ∇_νφ`, `q = g + A⊗A`) **and** the cosmological
function `𝒦(𝒬)` — from the thermodynamics/entropy of cosmological horizons, with the acceleration
scale fixed by the de Sitter temperature `a₀ ∼ cH`, rather than postulating the action and tuning it
to fit (as Skordis–Złošnik 2021 do).

---

## What is already established (do not re-derive)

1. **Field content is forced.** Geometry (Jacobson 1995) ⇒ a metric; the de Sitter–Unruh
   temperature is defined in the cosmic rest frame ⇒ a **unit timelike vector** `A_μ` (∇·A=3H on
   FRW, verified); a long-range low-acceleration force ⇒ a **scalar** `φ`. → `clean_slate_field_theory.py`.
2. **CMB-safety is structural.** Building the MOND term from the frame-orthogonal projector
   `q^{μν}=g^{μν}+A^μA^ν` gives `q⁰⁰=0` on FRW (computed) ⇒ `𝒴=0` on the background ⇒ a₀ absent from
   linear cosmology (Paper II's δq⁰⁰=0). → same script.
3. **The deep-MOND power is fixed — and now, independently, by symmetry.** The √-law `a=√(g_N a₀)`
   ⇒ kinetic power `n=3/2`. → same script. *Strengthened beyond the √-law + Newtonian-matching
   argument:* Singh 2026 (arXiv:2601.04290, "A Relativistic MOND") shows the deep-MOND action is
   conformally invariant under a 10-parameter group isomorphic to the de Sitter group `SO(4,1)`, and
   that this symmetry **forces** the asymptotic free function `F(y) ∼ (2/3) y^{3/2}` as `y→0`. The
   same non-analytic `3/2` power carried by the `𝒴^{3/2}` term is thus fixed by conformal/de Sitter
   symmetry, not only by the √-law. (Singh's route is an independent `E₆×E₆`/IR-metric-deformation
   construction, not AeST — so this is a second, disjoint origin for the same power.)
4. **The full interpolation has a derived, data-consistent form.** The de Sitter–Unruh temperature
   gives `μ(a)=[√(a²+(cH)²)−cH]/a`, i.e. `g_obs=√(g_bar²+g_bar a₀)`, which fits the SPARC RAR at
   **0.105 dex vs 0.101** for the empirical McGaugh function, with no shape freedom. →
   `desitter_unruh_RAR_test.py`. *(This is modified inertia; the covariant analogue is item B below.)*
5. **The scale is entropic.** `a₀∼cH` is the de Sitter entropy/temperature scale; the deep-MOND
   √-law follows from de Sitter entropy *displacement* (Verlinde 2016) — **but** on a *contested*
   volume-law de Sitter entropy. → `yphi32_from_entropy.py`.

So the *form*, the *field content*, *CMB-safety*, the *deep-MOND power*, and a *data-consistent
interpolation* are in hand. The action's **shape** is forced; what is missing is a rigorous,
uncontested, covariant *derivation* of the full kinetic structure and the cosmological sector.

---

## The precise open pieces

**A. Replace the contested entropy premise with a rigorous one.** Verlinde's `𝒴^{3/2}` origin needs
a *volume-law* bulk entropy for de Sitter space; standard derivations give only the *area* law.
Required: either (i) a defensible derivation of the bulk/volume entropy of de Sitter (or its
effective elastic response), or (ii) an alternative horizon-thermodynamic route (e.g. a Clausius
relation `δQ=TδS` with the de Sitter–Unruh `T` on local causal horizons, à la Jacobson/Padmanabhan)
that yields the `𝒴^{3/2}` term *covariantly* without the elastic-medium heuristic. *Note:* Singh
2026's conformal/`SO(4,1)` result (item 3) independently forces the `𝒴^{3/2}` *form*, but by symmetry
rather than horizon thermodynamics, and it leaves the coefficient open — so it sharpens, but does not
discharge, the entropy-derivation sought here.

**B. Show the covariant (modified-gravity) interpolation equals the modified-inertia one.** Item 4
above is a *modified-inertia* result (closed-orbit-limited). AeST is modified *gravity*. Required:
derive the AeST scalar's interpolation function from the same horizon `T(a)` and check it reproduces
the `√(g_bar²+g_bar a₀)` shape that fits SPARC — i.e. that inertia-route and gravity-route agree on
the RAR.

**C. Derive `𝒦(𝒬)`, the cosmological function.** AeST needs a second function of a temporal scalar
`𝒬` whose job is to make the background + linear perturbations behave like CDM (for the CMB and
growth). Conjecture to test: `𝒦(𝒬)` is the de Sitter *bulk* entropy acting as an effective fluid —
unstrained ⇒ `w=−1` (dark energy), strained by structure ⇒ `w≈0` (a pressureless "dust" mode).
Required: derive `𝒦(𝒬)`'s form (or its `w(𝒬)`) from the horizon entropy and show it gives the
observed `r_s`, `ℓ_A`, and growth — not just a₀-safety (already proven) but a *positive* CDM-like
background from the same entropy that gives a₀.

**D. Pin the coefficient (optional, won't change predictions).** The O(1) in `a₀=cH/Z` (Z = 0.5 / 2π
/ 6 / 5.79 depending on route) is data-degenerate and falsifiable predictions are Z-free, so this is
lowest priority — but a derivation that *also* outputs Z would be decisive.

> **THE LAST OPEN ROUTE IS NOW WORKED — STILL A NULL (strained-horizon O(ε³), `project_strained_horizon_cubic_O3.py`).**
> The definitive verdict had left exactly one route un-run: the *off-saddle* covariant `O(ε³)` free
> energy of the `C(𝒬)Y^{3/2}` vertex on a **strained (inhomogeneous)** de Sitter horizon — the
> "Verlinde-4/3-survival fork" (does the genuine 3/2 power leave the sphere-volume 4/3 uncancelled →
> κ=½, or cancelled → Verlinde 6?). Worked in full in sympy, it resolves **AGAINST closure**, and
> reveals *why*: **a power mismatch, not a 4/3 survival.** Verlinde gets a number (6) only because his
> strain energy is **quadratic** (`ε²`) and the horizon entropy/area response is **also** `ε²` (the
> area of a trace-free-strained sphere is `δA=(16π/5)R²ε²`, the `O(ε)` term vanishing — sympy-exact),
> so `ε²` cancels and the sphere 4/3 collapses to the `1/d` ball factor → `d(d−1)=6` (the bare integral
> ratio is `(d−1)²/d`). The **covariant cubic vertex** makes the strain free energy `O(ε³)` while the
> horizon stays `O(ε²)`: **3 ≠ 2**, so `F_MOND = δQ` is not an identity — it fixes the *strain amplitude*
> `ε`, leaving `a₀` (hence κ) carrying an **unfixed `ε`** (a continuous freedom, not ½). Equivalently the
> cubic **on-shell action is logarithmic** (`∫dr/r`, IR-cut at `R_dS`): there is *no* sphere 4/3 to
> survive — the angular `4π` is eaten by the `1/(12π)` leaving a bare `1/3` × an arbitrary
> `ln(R_dS/r_min)`; the action is `M^{3/2}` while the first law `δQ=TδS=−Mc²` (exact, ℏ cancels) is `M¹`.
> **The steel-man** (expand `Y^{3/2}` around a nonzero background gradient to get a finite `O(ε²)` MOND
> term) **fails by the same `Ȳ=0` fact**: `Y^{3/2}=(Ȳ+εb+ε²s)^{3/2}` has `O(ε²)` coefficient
> `3(4Ȳs+b²)/(8√Ȳ)`, which needs `Ȳ≠0` — but the covariant projector `q⁰⁰=0` forces `Ȳ=0` on the
> horizon (the CMB-safety property), where that coefficient **diverges** (`b²/√Ȳ`, the named
> non-analyticity); any self-consistent strained background has `Ȳ~ε²` → `Y^{3/2}~ε³` again. **So the
> off-saddle route hits the SAME obstruction as the homogeneous saddle, in a new guise:** on-saddle
> `Ȳ=0` *hides* a₀; off-saddle the non-analytic 3/2 power forces `ε³≠ε²` and the coefficient *cannot be
> read off*. Forcing a number anyway needs an extra posit (ε=1, or a choice of integration region, or a
> stress-balance ansatz) and **different posits give different rationals, none ½**. The principle the
> task asked for ("what decides survival vs cancellation?") is answered: **the degree of the vertex vs
> the degree of the area functional (3 vs 2)** — and the very 3/2 power the framework needs is precisely
> what breaks Verlinde's cancellation, not in favor of 4/3, but by introducing an unfixed strain scale.
> **κ=½ is NOT forced; the freedom persists.** This is the last route; item D is closed as a rigorous null.

> **RESOLVED AS A RIGOROUS NULL (June 2026 horizon-entropy sweep).** Six independent de Sitter
> horizon-entropy routes were pushed to their limit (Jacobson–Clausius, Padmanabhan–Debye,
> Verlinde volume-law, AeST-action-as-entropy, pure factor-bookkeeping, dS-CFT/Cardy) and
> cross-checked against the *latest* literature (Singh 2026 `2601.04290`; Sheykhi–Liravi
> `2510.14345`; modified-entropic-gravity `2511.05632`; MOND-entropy→EUP `2601.14353`). **No route
> forces `Z = √(32π/3) = 5.789.`** Every route fixes the *form* (`Y^{3/2}` power, FORCED by the
> √-law: `n=3` ⇒ `(∇φ)³`) and the *scale* (`a₀ ∼ √Λ`, FORCED by the Gibbons–Hawking horizon), and
> every route reduces the coefficient to `a₀ = κ·c√(Gρ_Λ)` with **κ un-pinned** — the framework's
> `κ=½` gives `Z=5.789`, Verlinde's elastic closure forces `κ=√(6π)/9 ⇒ Z=6` (rational, π-free, can
> *never* equal the irrational 5.789), thermal/Unruh gives `Z=2π`, a bare horizon gives `Z=1`.
> **Decisive factor-bookkeeping result (sympy-verified):** `Z² = 32π/3 = (extra 4)×(8π Einstein)/(3
> Friedmann)`, with `8π = 2π(Unruh)×4(=1/[BH ¼])` already spent making Newton (the bit count
> `N = A c³/Għ = 4·S_BH`). The **extra factor of 4 beyond Einstein's 8π is the free-fall /
> surface-gravity `(½)²` convention, NOT a forced second Bekenstein–Hawking ¼.** A literal second
> `¼` does *not* reproduce it (sympy: literal `κ=¼ ⇒ Z=11.58`, off by 2×); single-metric AeST has
> only one horizon, whose one entropic ¼ is already consumed in the 8π; and the "second ¼ under the
> deep-MOND √" reads `√(¼)=½`, numerically identical to the free-fall ½ but a *separate posit*, not a
> consequence. Independent corroboration: Singh 2026 writes `a₀=c²/(ξ ℓ_dS)` with ξ **"O(1) fixed by
> matching to the static (AQUAL) limit"** — matched, not derived; his SO(4,1) symmetry forces the
> `(2/3)y^{3/2}` *form* but leaves the prefactor open — exactly this framework's `Z/κ`. The three
> newest entropic-MOND papers all *insert/match* the O(1). **Bottom line: form + scale derived;
> coefficient route-dependent; the freedom enters at the single leading ½ (the C(𝒬) normalization /
> the extra factor of 4), and no equilibrium horizon-entropy argument fixes it.** This matches every
> prior route (DSSYK / bound / surface-gravity / Penrose / spontaneous-radiation gave Z=1 or by-hand
> 2π, never 5.79). The coefficient remains a posit; predictions are Z-free, so this does not touch any
> falsifiable test. See `THE_FACTOR_OF_FOUR.md` and the full verdict in the June-2026 horizon-entropy
> report. *(Cleanup flagged: `THE_FACTOR_OF_FOUR.md`'s "thermal 2π" row uses cH₀ not cH_Λ — the
> pure-Λ value is `κ=√6/(3√π)=0.461 ⇒ Z=2π=6.28`, which strengthens the not-forced conclusion.)*

---

## Success criterion

A single covariant action `S[g,A,φ]` (+ the `𝒬` sector) such that: (1) every term has a stated
horizon-thermodynamic origin (no postulated functions); (2) the quasi-static limit is the SPARC RAR
shape of item 4; (3) the cosmological limit gives a CMB-safe, CDM-like background (item C); (4) GWs
travel at c and the theory is ghost-free. Achieving (1)–(4) *derives* AeST (or a near relative) from
the horizon foundation and closes Layer 0.

---

## Why it is worth doing

If it closes, the entire chain — **cosmic horizon → emergent inertia → MOND with an evolving scale →
a covariant, CMB-safe field theory → the redshift-weakening EFE** — becomes first-principles, and the
coefficient stops being a posit. It would turn a *phenomenological* relativistic MOND (AeST) into a
*derived* one. The relevant literature is real and active (Jacobson 1995; Padmanabhan; Verlinde 2011,
2016; Skordis–Złošnik 2021; Singh 2026), and the problem above is now bounded to four concrete items.
