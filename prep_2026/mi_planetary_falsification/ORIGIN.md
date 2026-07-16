# ORIGIN of the crossover corner omega_c — FORCED or FREE?

**Date:** 2026-07-16. **Framework:** de Sitter–Unruh **MODIFIED INERTIA** (Carl Zimmerman), judged on
its own terms — own interpolation ν(y)=√(1+1/y), μ(x)=(√(1+4x²)−1)/(2x)=K(x²), horizon-derived
a₀=cH_Λ/Z. Published covariant MI action, kernel K(□_u/a₀²), Herglotz–Nevanlinna, sum rule ∫dμ/|t|=1.
**Both footings carried:** canonical a₀=9.36×10⁻¹¹ (ρ_DE, cH_Λ/Z), alt a₀=1.13×10⁻¹⁰ (ρ_tot/cH₀).
s=−1 and a₀'s value remain **POSTULATES**.

**Compute script (exit 0, both footings, no hard-coded verdict booleans):**
`origin_window_scales.py` → `origin_window_scales.out`.

---

## The question

The prior planetary lanes established that the only RAR-preserving solar-system survivor is a **gated
"Reading C"**: MI amplitude × a Lorentzian frequency gate L_c(ω/ω_c) = 1/(1+(ω/ω_c)²), MOND-active for
ω < ω_c (galaxies, ω~10⁻¹⁵), suppressed for ω > ω_c (planets, ω~10⁻⁷). This workflow asks two things,
both reported straight:

1. **Is the joint allowed ω_c window non-empty?** (Recompute from the actual published bounds.)
2. **If non-empty: is ω_c FORCED by a physical scale in the theory, or a FREE add-on (a 5th constant)?**

---

## PART 1 — the joint window is NON-EMPTY on both footings

Recomputed from the actual cited bounds (`origin_window_scales.py` PART 1):

| edge | source (value ± σ) | canonical | alt |
|---|---|---|---|
| **LOWER** (galactic RAR preservation: gate ≥0.90 at the deepest confirmed MOND orbit, y=0.8, v=25 km/s ⇒ ω_c ≥ 3ω_gal) | framework RAR | **8.99×10⁻¹⁵** | **1.08×10⁻¹⁴** |
| **UPPER** (secular-drift ceiling) | **Biskupek & Müller 2021**, Universe 7:34 (arXiv:2012.12032): Ġ/G = (−5.0 ± 9.6)×10⁻¹⁵/yr → 2σ = \|c\|+2σ = **2.42×10⁻¹⁴/yr** | **2.21×10⁻¹⁴** | **1.83×10⁻¹⁴** |
| (looser, not binding) MESSENGER Ġ/G | Genova 2018, Nat. Commun. 9:289: <4×10⁻¹⁴/yr | ≤3.66×10⁻¹⁴ | ≤3.03×10⁻¹⁴ |
| (looser, not binding) per-planet reactive | Fienga & Minazzoli 2024, LRR 27:1 (arXiv:2303.01821), Table 10; binding planet **Saturn** δg 7.0×10⁻¹⁵ | ≤8.27×10⁻¹¹ | ≤7.52×10⁻¹¹ |

**LLR BINDS from above** — ~3.6 dex tighter than the per-planet reactive edge and tighter than
MESSENGER. Transition-region observability adds no edge (only wide binaries/Oort probe ω~ω_c; the gate
keeps ≤6% of the MOND boost at ≤20 kAU — a prediction, not a current exclusion).

**WINDOW:**
- **canonical: ω_c ∈ [9.0×10⁻¹⁵, 2.2×10⁻¹⁴] rad/s = τ 1.43–3.53 Myr** (width ×2.46)
- **alt: ω_c ∈ [1.1×10⁻¹⁴, 1.8×10⁻¹⁴] rad/s = τ 1.73–2.92 Myr** (width ×1.69)

The LLR-drift formula at the Moon (the LLR body, g_N=2.70×10⁻³ m/s²) is d ln r/dt = (a₀/g_N)·ω_c;
it reproduces the ungated universal drift a₀/c = 9.86×10⁻¹²/yr (KERNEL_PLANETS.md:117-124) at the
un-gated limit, and scales linearly with the corner under the gate.

---

## PART 2 — the corner is NOT forced by any physical scale; it is FREE

Each candidate origin tested explicitly (`origin_window_scales.py` PART 2):

| candidate origin | frequency (canon) | in window? | forced theory scale? |
|---|---|---|---|
| **(a)** dS-Unruh bath re-thermalization / KMS Matsubara at T_dS | H_Λ = 1.81×10⁻¹⁸ rad/s | **no** (4.7 dex below) | YES — but it's the **horizon** rate |
| **(b)** density/screening √(4πGρ) ("plasma-like") | ρ_local 2.38×10⁻¹⁵ ; ρ_cosmic 1.51×10⁻¹⁸ | **no** (0.6 dex below at best) | **no** — environmental |
| **(c)** light-crossing/retardation c/r (source) and a₀/c (kernel) | a₀/c = 3.12×10⁻¹⁹ ; c/r 10⁻¹²…10⁻⁴ | **no** | YES/r-dep — but horizon or above |
| **(d)** a second dimensionful scale in the Herglotz measure | a₀/2c = 1.56×10⁻¹⁹ (only one it can build) | **no** (4.8 dex below) | YES — but single-scale a₀ |

**(a) dS bath.** The dS thermal bath's only intrinsic response frequency is its nearest Matsubara pole
at **κ = H_Λ** (the horizon), and the off-circular pullback pole is κ_eff = √(H_Λ²+(a/c)²) ≥ H_Λ
(CONSEQUENCES.md:20-27; CLOSURE_MAP.md:58). H_Λ ≈ 1.8×10⁻¹⁸ rad/s — **~4.7 dex below the window**. The
bath has **no intrinsic ~Myr re-thermalization time**; every scale it offers is the horizon. FORCED
scale, wrong location. **Does not supply ω_c.**

**(b) density/screening.** The gravitational dynamical/Jeans frequency √(4πGρ) is the closest
candidate: at the solar-neighborhood dynamical density (0.1 M_⊙/pc³) it is 2.4×10⁻¹⁵ rad/s — only a
factor ~3.8 below the window bottom. **But density is environmental, not a theory constant:** it spans
1.5×10⁻¹⁸ (cosmic mean) to 2.4×10⁻¹⁵ (local stellar) rad/s, ≥3 dex, and planets share the *local*
density with the co-located local galactic orbit — so a density-set corner cannot separate them.
**CHOSEN, not forced** — a near-miss, honestly flagged, that fails as a mechanism.

**(c) retardation.** Source light-crossing c/r is r-dependent (1.2×10⁻¹² at 8.2 kpc, 2.1×10⁻⁴ at
Saturn — above the window and non-universal). The theory's *own* retardation/memory length is c/a₀ (the
Compton length of the massive auxiliary modes, CONSEQUENCES.md:157-159) → ω = a₀/c ≈ 3×10⁻¹⁹ rad/s,
the horizon. **No retardation scale in the theory lands at ~Myr.**

**(d) Herglotz measure.** The measure's only structure is the branch point at t=1/4 — **dimensionless**
in a₀² units (|a|=a₀/2), not a new dimensionful scale; the sum rule ∫dμ/|t|=1 and ‖K‖≤1 fix
normalization only. Every frequency the measure builds is a₀/c-family (~10⁻¹⁹ rad/s). **The measure is
single-scale a₀ by construction; there is no second scale.**

---

## Verdict

**SURVIVES, CONDITIONALLY — ω_c is a FREE add-on, an honest 5th constant.**

- The joint window is **NON-EMPTY on both footings** (LLR-bound from above). The framework passes every
  solar-system bound as a gated Reading-C crossover with a corner in a ~Myr sliver.
- **No forced theory scale lands in the window.** Every genuine scale in the theory — the dS bath H_Λ,
  the kernel retardation a₀/c, the single-scale Herglotz measure — is the **horizon scale ~10⁻¹⁸–10⁻¹⁹
  rad/s, ~4–5 dex below** the required corner. The published action **forces** the memory corner to
  a₀/2c (τ_mem = 203 Gyr canon / 168 Gyr alt), which is **RAR-dead** at galaxies (retained boost
  2.9×10⁻⁸, CONSEQUENCES.md:117); the pullback leaves the reduction weighting η(β) **free**
  (CONSEQUENCES.md:20-30). Neither pins ω_c.
- The one near-miss (local-density √(4πGρ) ~2×10⁻¹⁵) is **environmental, spans 3+ dex, and cannot
  discriminate planets from the co-located galactic orbit** — CHOSEN, not forced.

**Therefore the constant set {s, a₀, Z, η} → {s, a₀, Z, η, ω_c}:** the framework survives the solar
system only by **adding a postulate the published action does not supply.** Not a falsification; not a
clean win.

**Honest ceiling.** At planetary accelerations (10⁴–10⁸ a₀) GR and healthy MOND-family theories both
predict ≈0; every number here discriminates **among the framework's own readings, never vs ΛCDM.**

**Two-sided falsifiable:** a confirmed Chae-type AQUAL-strength wide-binary boost kills the gated
survivor; a ×3 INPOP/EPM secular refit either detects the drift or closes the window from above.

---

*Reproduce:* `cd /Users/carlzimmerman/new_physics/prep_2026/mi_planetary_falsification && python3 origin_window_scales.py` (exit 0). Sources read (frozen read-only repo / prior prep lanes, cited file:line where load-bearing): `planetary_doors/{BOUNDS.md,KERNEL_PLANETS.md,laneR_bounds_compute.py}`, `mi_closure_pin/{CONSEQUENCES.md,rider_c_planetary.py}`, `mi_field_theory/CLOSURE_MAP.md`. Both footings; s=−1 and a₀'s value postulated; c_T=1 (graviton on g) untouched; no completeness/TOE claim.*
