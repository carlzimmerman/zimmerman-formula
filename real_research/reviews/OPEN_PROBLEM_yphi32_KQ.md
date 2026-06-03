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
3. **The deep-MOND power is fixed.** The √-law `a=√(g_N a₀)` ⇒ kinetic power `n=3/2`. → same script.
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
that yields the `𝒴^{3/2}` term *covariantly* without the elastic-medium heuristic.

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
2016; Skordis–Złošnik 2021), and the problem above is now bounded to four concrete items.
