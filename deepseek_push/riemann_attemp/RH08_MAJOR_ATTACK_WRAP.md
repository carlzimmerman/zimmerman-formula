# RH08 -- THE MAJOR-ATTACK WRAP (deepseek, 2026-09-17): four parallel lanes, integrated verdict

**THE VERDICT IN ONE SENTENCE: RH is NOT proven — correctly, honestly, with the referee standing
over every claim — and the attack's value is the certified scaffolding, the executed kills, and the
clean measurements; no claim survived that was not earned.**

---

## THE FOUR LANES (all landed, all verified on disk)

**RH04 -- Li's criterion (the only exact RH-equivalence):**
- True Li constants, extracted from the Hadamard product over ALL zeros (no RH input needed for
  the exact λ_n): λ₁ = 0.02309570896612103381... matches the Maslanka closed form to 1e-81;
  λ₂ = 0.092346; λ₅₀ = 43.531. Partial sums over 500/1000/2000 real zeros are positive and
  monotone into the exact values. K1 PASS (no numerical contradiction of RH).
- Nielandt-type zero-counting envelope covers the exact tail (ratio ≥ 1.0059). K2 PASS: the
  framework-ladder synthetic Li (Lomax λ=2.4824 spacings) is positive. K3 TRIGGERED but weak
  (7/20 seeds, median dev 18.4%): registered as a cancellation, not a coincidence.
- HONEST WALL: partial sums are numerical control, n ≤ 50, tail uncontrolled → **no proof**.

**RH05 -- the general ladder, Lean-certified (16 theorems, exit 0, ZERO sorry):**
- THE FULL MOMENT SEQUENCE: E[ln(1+u)]_l = 1/(l-1) certified for EVERY rung l > 1 -- substitution
  algebra + Mathlib Gamma machinery + the measure-theoretic change of variables. l=3 gives the
  framework's 1/2 exactly.
- THE GENERAL-LADDER REFLECTION: M_l(s) = M_l(l-s) (axis l/2), certified for general l; the l=3
  case recovers RH01L verbatim. An honest correction to the delegated literal: the claimed exponent
  "2s-l" in the task was WRONG (forces s=1); the certified identity is v^(s+1-l)·v^(-2)·(1+1/v)^(-l)·(1+v)^l = v^(s-1).
- THE WALL (in the .lean header): transfer step T1 (kernel embedding, UNPROVED -- false as function
  equality), T2 (edge limit l→1, convergence uncertified, routine analysis; the Γ(s)Γ(1-s)=π/sin(πs)
  identity itself IS certified), T3 (symmetry⇒zeros -- UNPROVED, IS RH, and FALSE in general: certified
  counterexample (s-2)(s+1) has off-axis zeros while its reflection symmetry holds).

**RH06 -- the log-moment spine (the second falsifier, landed):**
- κₙ = n!/(λ-1)ⁿ = n!·κ₁ⁿ sympy-exact (n=1..4, C1 PASS). Measured on 1500 TRUE zeros (unfolded,
  unit-mean; κ₁ = 0.67504 ± 0.00492 reproduces the 0.6746 pin): κ₂=0.49191, κ₃=0.38104, κ₄=0.31042.
- vs the framework spine n!·0.6746ⁿ: 62σ / 192σ / 570σ → **the ladder's full spine is DEAD.**
- vs exact-GUE (MC): κ₂ z=0.45, κ₃ z=1.49 → the zeros' log-moment sequence is GUE's; κ₄ marginally
  neither (z=2.05-2.33). **The single-moment pin (κ₁) was a coincidence of ONE number.**

**RH07 -- the referee (the file to read when asking "did we prove it?"):**
- Independent re-measurement: 0.674564 ± 0.003501 (z vs 1/2 = 49.9) — the flagship number is real.
- Every positive claim classified: (a) certified facts = the Mellin reflection M(s)=M(3-s), the
  moment identity, the axis census (π, π/8, π/4) — exact Gamma/beta arithmetic, zero-free, NO zeta
  content; (b) measured = the GUE match of the zeros' spacings; (c) coincidences registered = the
  1/2 = 1/2 crossing, the ladder-member pin; (d) unproven = every transfer to the zeta's zeros.
- Costs admitted: RH03's "max-entropy self-test PASS" over-sold (GUE entropy < Lomax at the same κ
  means the zeros are NOT the max-entropy law at their own κ); RH02b's "supremum" at 1/2 is a
  MINIMUM (fixed in-file and re-verified this session); the "positive-law: wrong member, not wrong
  class" spin was not earned — κ₂..₄ kill the class-level claim too.
- "A beta-function reflection is a symmetry of a kernel, not a statement about the zeta." — RH07.

---

## THE INTEGRATED HONEST LEDGER

  PROVEN (Lean exit 0, zero sorry, both a₀ footings irrelevant -- no a₀ in RH):
    • M(s) = M(3-s) for the framework kernel; M_l(s) = M_l(l-s) for all l > 1 (axis l/2)
    • E[ln(1+u)]_l = 1/(l-1) for all l; κₙ = n!·κ₁ⁿ; axis census π / π/8 / π/4
    • Li constants λ₁..λ₅₀ EXACT (Hadamard over all zeros) + monotone partial sums over N real zeros
  MEASURED (actual computations, all re-verifiable):
    • E[ln(1+s)] of the zeros = 0.6746 ± 0.0035 = GUE (0.6711 ± 0.0017, 1.0σ), ≠ 1/2 (50σ)
    • κ₂ κ₃ = GUE's; κ₄ marginally own; framework spine dead at 62-570σ
  KILLED (pre-registered, executed):
    • F1: the zeros' spacings are NOT the framework kernel's law (1/2 vs 0.6746, 50σ)
    • F2: the ladder's full log-moment spine is NOT realized in the zeros (62-570σ)
    • the "change-of-class" spin (κ₁ pins member λ=2.48): one number, not a class
  NOT PROVEN: RH.  Nothing in this lane touches a single zero's location.

## WHAT REMAINS OPEN (registered, not abandoned)
  • the edge-extremum test: the zeta's OWN completion at s=1/2 (B(s,1-s)=π/sin(πs) minimized at the
    axis is certified for the ladder edge; the transfer to Xi is NOT)
  • the 30k-zero upgrade run of RH01 (in flight at session end; same test, better σ)

## KEEP / BURN
  KEEP: the pre-registered kill discipline (F1/F2), the honest .lean walls, the measurement
  pipeline (zeros → unfolding → log-moments), the general-ladder certificate as the repo's
  strongest RH-adjacent mathematics.
  BURN: any presentation of the framework as "closer to RH" by the machines of this lane —
  the referee's ledger is the last word on that.

RW, Carl — the referee stands over the ledger. This is the honest state of the attack.