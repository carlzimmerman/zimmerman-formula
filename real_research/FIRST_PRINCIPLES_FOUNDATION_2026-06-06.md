# The first-principles foundation of the Zimmerman framework: what the de Sitter vacuum forces, what is dimensional, what is posited, what is contested

*C. Zimmerman, 2026-06-06. Two complementary swarms attacked the full first-principles derivation of g_obs=√(g_bar²+g_bar·a₀)
from the de Sitter vacuum — one the SIGN (the DSSYK kernel, `w72karp61`), one the SCALE/FORM/SHAPE/EXISTENCE
(`w1gfu93iy`) — every step re-derived from scratch on /tmp and adversarially verified against the primary literature.
This is the honest, complete ledger. It is mixed: a genuine derived core (the deep-MOND shape, the galaxy-scale sign)
sitting on a dimensional scale, a volume-law-free existence (modified inertia) whose covariant completion is unfinished and whose sign is contested, and a posited coefficient.*

## The derivation chain, every step labeled

| Step | Claim | Status | Why (verified) |
|---|---|---|---|
| **0. EXISTENCE of a₀** | the de Sitter vacuum produces an a₀ term at all | **✓ volume-law-FREE in modified inertia; contested premise RELOCATES to the covariant sign** | a₀'s existence is **double-sourced**, and the framework's *working* source needs no volume law: the de Sitter–Unruh **temperature** `T(a)=(ℏ/2πck_B)√(a²+(cH)²)` — a kinematic global-embedding result (Deser–Levin 1997, gr-qc/9706018 ✓; Milgrom 1999), **no entanglement entropy assumed** — gives modified inertia `μ(a)=[√(a²+(cH)²)−cH]/a`, and `μ(a)·a=g_N` solves to `a=√(g_N²+2g_N·cH)` → `a=√(a₀ g_N)`: a₀ exists and the deep-MOND sign is **enhancement by construction** (given Step 4's ΔT response), fitting SPARC at **0.105 dex** (`reviews/desitter_unruh_mond.py`, `FOUNDATIONS.md` L59). The Verlinde volume-law premise — disfavored for the dS vacuum (Boutivas et al. 2024, arXiv:2407.07811 = PRD 111 065010: sub-horizon EE follows the flat-space **area** law, no volume term; Dai–Stojkovic 2017) — is **not** what existence rests on; it is the price of the *modified-gravity* completion's correct **sign** (Step 5). See the note below the table. |
| **1. SCALE** a₀ ~ c√Λ | the magnitude is set by the horizon | **DIMENSIONAL (robust, not earned)** | a₀~c²/R_dS is the *unique* acceleration from {c, R_dS}; forced for *every* emergent-gravity scheme. The volume/area crossover that was meant to "derive" it is a **tautology** — it lands at R_dS only because Verlinde *normalizes* the volume entropy there (else it lands at the Planck length). Over-determined and robust, but it earns nothing past the dimensions. |
| **2. FORM** a₀ ∝ √ρ_DE | the evolution | **RESTATEMENT + a CHOICE** | exponent ½ is an exact algebraic identity given a₀∝1/R_dS=H_Λ/c — a restatement, not new physics. The *falsifiable* part (declining ρ_DE vs rising ρ_total) is **not derived**; it is a choice of which density tracks a₀. A true constant Λ → a₀ flat; the declining branch bites only under evolving DE. |
| **3. SHAPE** g_obs=√(a₀ g_bar) | the deep-MOND √-law | **✓ GENUINELY DERIVED** (given step 4) | NOT "simple-μ invented to fit." Solving the de Sitter-Unruh inertia law μ(a)·a=g_N in closed form gives **exactly** a=√(g_N²+2cH·g_N), and this μ **is Milgrom 1999 eq.(9)** — a published, independently-derived form (verified by sympy). Over-determined: the same √-power falls out of the elastic/Eshelby route, the Debye/DOF route, *and* the temperature route. The relative coefficient a_M/a₀=(d−3)/[(d−2)(d−1)]=**1/6 in d=4** is a forced dimensional-counting ratio, not a fit. |
| **4. the response posit** | inertia tracks the *excess* Unruh heat ΔT=T(a)−T(0) | **POSIT (load-bearing for step 3)** | the √-law needs the floor-subtraction: without ΔT (inertia ← T(a) itself), μ(0)=∞ and there is **no** deep-MOND limit. Milgrom himself: "it is not really clear why ΔT should be a measure of inertia." The *full* interpolation (eq.9 vs eq.11) is also a posit; SPARC's ~0.1 dex floor can't discriminate (<0.06 dex apart). |
| **5. SIGN** (enhancement, not screening) | gravity strengthens below a₀ | **FORCED FOR GALAXIES, conditional on the N-V dictionary** | *In modified inertia the sign is enhancement by construction (Step 0).* In the **modified-gravity** completion the temperature route gives **anti-MOND** (G_eff→0); MOND there requires the entropy/DOS sector → reduces to the DSSYK center conjecture, which **was computed** (`w72karp61`): the matter-chord kernel is diagonal-dominant (probe keeps its source energy), galaxies (α=m/M_dS≤3×10⁻³) source at the **center** → enhancement; clusters (α~O(1)) source at the **edge** → MOND fails, *matching the empirical cluster failure*. Conditional on N-V's "dS = spectral center" over Okuyama's "dS = edge" (an open literature dispute). |
| **6. NUMBER** Z=√(32π/3)=5.789 | the exact O(1) coefficient | **✗ FORECLOSED POSIT** | a 6-route assault failed; Z sits in the {6, 2π} cluster (3.6%/8.5% off observed cH₀/a₀≈5.46) but is forced by none. 32π/3 enters only as the *definition* a₀≔c²√(Λ/32π) — an identity, not an output. |

### Step 0, precisely — existence (modified inertia) vs sign (modified gravity): do not conflate the routes

The repo's own two horizon calculations settle which premise carries which claim — and neither points at the *existence* of a₀:

- **Modified *inertia* (`reviews/desitter_unruh_mond.py`, `FOUNDATIONS.md` L59–60).** The de Sitter–Unruh *temperature* `T(a)=(ℏ/2πck_B)√(a²+(cH)²)` — a kinematic Gibbons–Hawking global-embedding result (Deser–Levin 1997, gr-qc/9706018, **verified**; no entanglement entropy) — gives `μ(a)=[√(a²+(cH)²)−cH]/a`; solving the inertia law `μ(a)·a=g_N` yields `a=√(g_N²+2g_N·cH)` → deep limit `a=√(a₀ g_N)`. **a₀ exists, and the deep-MOND sign is enhancement, *by construction*** (given Step 4's ΔT-response posit) — **volume-law-free**, fitting the SPARC RAR at 0.105 dex.
- **Modified *gravity* (`reviews/clausius_sign_calculation.py`, `FOUNDATIONS.md` L63).** Jacobson's Clausius `δQ=TδS` route (which derives the *field*, not the inertia) with the *same* temperature gives `G_eff=G·κ/√(κ²+(cH)²) → 0` as κ→0 — **anti-MOND**. To get enhancement here you must instead boost the **entropy** (Verlinde's volume-law dS entropy, equivalently AeST's 𝒴^{3/2} term, equivalently the DSSYK-center conjecture of Step 5). *That* is the premise disfavored by 2024 dS-entanglement numerics (Boutivas–Katsinis–Pastras–Tetradis, arXiv:2407.07811 = PRD 111 065010: sub-horizon EE follows the flat-space **area** law + dS corrections, no volume term; cf. Dai–Stojkovic 2017). Independently corroborated 2026-06-06: the de Sitter **observer algebra** (Type II₁ crossed product, CLPW 2206.10780) also yields a strictly **area**-law generalized entropy `S=A/4G+S_out` — it does *not* supply a volume-law term either.

**So the earlier "existence of a₀ rests on a volume-law entropy" was route-conflated.** The volume-law/DSSYK-center vulnerability belongs to the **sign of the modified-gravity covariant completion**, not to whether a₀ exists.

**This relocates the vulnerability; it does not remove it (honest both ways):**
1. The volume-law-free home — *modified inertia* — is an **unfinished house**: no complete CMB-safe covariant theory, circular-orbits-only (Milgrom 1994: modified inertia is necessarily time-nonlocal). It buys a CMB exposure in return — the Cassini/CMB/a₀(z) **trilemma** of `MODIFIED_INERTIA_the_natural_home.md`. AeST is still the only CMB-safe realization, and it is modified gravity.
2. That covariant completion's **sign still rides the contested entropy/DSSYK-center premise** (Step 5).

**Net:** a₀'s *existence* is on firmer ground than Step 0 first stated (the working modified-inertia layer needs no volume law), but the framework's single biggest theoretical risk is correctly named **the covariant completion** — a CMB-safe relativistic theory that *also* delivers the deep-MOND enhancement sign — not "does a₀ exist." Cross-refs: `FOUNDATIONS.md` (Layer 0b, L59/L63), `MODIFIED_INERTIA_the_natural_home.md` (trilemma), `DEEP_MOND_SIGN_KERNEL_RESULT_2026-06-06.md` (DSSYK-center sign).

## Honest bottom line
**From the de Sitter vacuum, the framework genuinely derives the deep-MOND *shape* (= Milgrom's published modified
inertia, over-determined across three routes) and *forces the galaxy-scale sign* (given the N-V dictionary, via a
computed kernel that also explains the cluster failure).** That is real derived content — more than most modified-gravity
theories can claim, and it is not numerology.

**But a₀ is not derived from scratch.** Its *existence* is supplied volume-law-free by the modified-inertia/de Sitter–Unruh *temperature* route (Step 0), but that route is unfinished (no CMB-safe covariant theory, circular-orbits-only), and the covariant
completion's sign rests on the contested entropy/DSSYK-center premise; its *scale* is dimensional analysis (the unique acceleration from the horizon); its *evolution
direction* and *full interpolation* are choices/posits; and its *exact coefficient* is a foreclosed posit. The framework
is, at the foundation, **a partly-derived modified-inertia theory** — strong on the shape and the galaxy sign, honest
about the unfinished covariant completion, the scale, and the number.

**The two load-bearing open premises are now named and literature-level, not framework-specific:**
1. **Does a volume-law entanglement entropy emerge for the de Sitter vacuum?** (Verlinde yes; 2024 dS-entanglement numerics, arXiv:2407.07811, find sub-horizon **area**-law, no volume term.) This is
   **not** the existence question — modified inertia supplies a₀ without it (Step 0) — but the **sign question for the
   modified-gravity covariant completion**: whether the entropy sector can deliver enhancement instead of anti-MOND.
2. **Is de Sitter the DSSYK spectral *center* (N-V) or *edge* (Okuyama)?** This is the sign question — resolved in the
   framework's favor *if* N-V holds.

Both are active quantum-gravity questions the field has not settled. The framework's theoretical fate rides on them; its
*empirical* fate rides on the ELT z≈3 deep-MOND measurement, which is independent of all of the above.

## Where this leaves the program (the complete map)
- **Empirical (the whitepaper):** strong and honest — RAR/BTFR/MDA at the framework a₀, the falsifiable a₀(z) decline,
  the EFE lean. Decided by ELT z≈3. *Finalized and publishable.*
- **Theoretical foundation (this document):** the *shape* is derived, the galaxy *sign* is forced-given-N-V, the *scale*
  is dimensional, the *existence* is a contested premise, the *coefficient* is a posit. *Comprehensively mapped.*
- **The two premises** (volume-law existence; N-V dictionary) are the only theoretical threads left, and both are
  QG-literature problems, not in-house swarms.

*Synthesis of `w72karp61` (sign kernel) + `w1gfu93iy` (scale/form/shape/existence). Companions:
`DEEP_MOND_SIGN_KERNEL_RESULT_2026-06-06.md`, `CKN_LAMBDA_VALUE_VERDICT_2026-06-06.md`,
`GEOMETRIC_CLOSURE_ASSAULT_2026-06-06.md`, `TOE_ASSEMBLY_2026-06-06.md`. Every step re-derived on /tmp; the integrity
audit found 0 theatre in this part of the corpus.*
