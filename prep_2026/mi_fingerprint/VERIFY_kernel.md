# VERIFY — Kernel-Theory Frequency-Universality Lane (adversarial verify pass, 2026-07-16)

Independent adversarial verification of the RB-lane compute (`rb1_circular_exactness.py`,
`rb2_frequency_dependence.py`, `rb3_eccentric_offset.py`, `KERNEL_THEORY.md`) for the
Zimmerman de Sitter–Unruh **modified-inertia** action. Verified on the framework's own terms
(a₀ = cH_Λ/Z = 9.36e-11 canonical / 1.13e-10 alt; own ν(y)=√(1+1/y); published kernel
K(z)=(√(1+4z)−1)/(2√z), □_u f = u^a∇_a(u^b∇_b f)). A **win is checked as hard as a deficit**.

## 0. Re-run (exit status + reproduction)

All three scripts re-run to **exit 0**, all internal checks PASS (rb1: 15/15, rb2: 13/13,
rb3: 19/19, no FAIL lines). Banked `.out` files reproduce **byte-identical** to fresh runs
(`diff` = IDENTICAL for all three; the rb3 Monte Carlo is seeded `default_rng(7)`).

## 1. u·□_u u = −|a|² — re-derived independently, curved space, general worldline

**Pen-and-paper.** With proper-time parametrization u·u = −1 (constant) and metric compatibility
∇g = 0, the absolute derivative D/Dτ commutes with index-lowering:
- D/Dτ(u·u) = 2 u·a = 0 ⇒ **u·a = 0**.
- D/Dτ(u·a) = a·a + u·ȧ = 0 ⇒ **u·ȧ = −|a|²**.

Since □_u u^μ = u^a∇_a(u^b∇_b u^μ) = D²u^μ/Dτ² = ȧ^μ, we get u_μ □_u u^μ = u·ȧ = −|a|².
The only inputs are (i) unit norm and (ii) ∇g = 0. **No orbit-shape assumption, no circularity.**

**Independent machine check (NOT the rb1 flat-space trick).** I re-derived it covariantly in a
genuinely curved metric (Schwarzschild t–r block, mass M) on an arbitrary **non-geodesic**
worldline T(τ), R(τ), building Christoffels from scratch, forming a^μ = Du^μ/Dτ and
□_u u^μ = Da^μ/Dτ, then enforcing u·u = −1 by solving for Ṫ. Result: `u.Box_u u + |a|^2 = 0`
identically (sympy). The two kinematic identities `d/dτ(u·u)−2u·a = 0` and
`d/dτ(u·a)−(a·a+u·ȧ) = 0` also hold before the constraint is imposed.

**Verdict (a): UPHELD.** The first-moment identity is exact and worldline-general. The published
reduction K(□_u/a₀²) → μ_fw(|a|/a₀) is genuinely the *exact first spectral moment* in the
u-contraction — a derived statement, not an ansatz. Theorem A (ring exactness, K(x²)=μ_fw(x),
circular balance collapse via 1+4(y²+y)=(2y+1)²) is elementary algebra and holds; ring residual
is machine zero (≤3.4e-13).

## 2. The 2.3e-8 frequency-universality number — reproduced with own arithmetic

Circular orbit at a=a₀ ⇒ ω=a₀/v ⇒ w=ωc/a₀ = **c/v** (footing-independent). Phase law
K(−w²+i0)=exp[i·arcsin(1/2w)]. Independent arithmetic (fresh solver, not the rb2 code):

- 1−cos φ_gal = v²/(8c²) = (150 km/s)²/(8c²) = **3.13e-8** (closed-form hand-check matches).
- Circular balance F(x)cos φ = y, F(x)=(√(1+4x²)−1)/2, ν=x/y:
  **Δν/ν(gal↔wb, a=a₀) = +2.35e-8 at y=1, +1.71e-8 at y=0.1**, galactic side more boosted.
- Identical for both a₀ footings (the split depends only on c/v).

Matches the claimed +2.3e-8 / +1.7e-8. Sensitivity |J|=|dlnν/dln cos φ| ∈ [0.55, 0.75] ⊂ [½,1]
as stated. **Verdict on the number: UPHELD, footing-independent.**

## 3. Honesty crux — "measure is NOT free": real, but it is not the *whole* of the headline

**The measure-uniqueness claim is REAL and correctly proven.** K is Herglotz/Nevanlinna
(I confirmed Im K(t+i0) ≥ 0 at all cut samples → positive spectral density → valid representation);
the RAR calibration fixes K(z)=μ_fw(√z) on a positive-real interval (z=a²/a₀² ∈ ~[1e-4,1e8]);
the positive real axis lies inside the analyticity domain (cut on negatives). By the identity
theorem the analytic continuation — hence the cut boundary values, hence the measure — is **unique**.
Region-B sum-rule contribution ∫dμ/|t| = **2/π exactly** (independent sympy integration), total = 1.
So the **frequency response of the operator K is forced**: there is no measure freedom.

**But this is logically distinct from "the orbit RAR is frequency-universal to 3e-8," and the
distinction must be kept.** Measure-uniqueness pins K *as a function*. Turning K(□_u) into an orbit
law requires the **closure map**, which is genuinely O(1) FREE (the nonlinear operator's ordering on
a worldline; u·K(□_u)u ≠ K(⟨□_u⟩) beyond first moment — rb1[3] shows the literal helix gives
γ²v²K(−(ω/a₀)²), differing at O(1), moment expansion uncontrolled at (c/v)² per order). The 2.3e-8
uses the *minimal* first-moment-amplitude × reactive-phase closure.

**Is the O(1) freedom under-stated? No — the scripts and KERNEL_THEORY are honest about it.**
rb2[6], rb1[3–4] and KERNEL_THEORY §5 all explicitly flag the closure map as FREE/open and label
2.3e-8 as a *bound* from the minimal closure ("the cross terms are the open ordering … the BOUND is
what is rigorous"). The falsifier is stated correctly.

**One framing tension worth flagging (not a manufactured win):** the headline phrases ("there is
nothing left to tune," "forces … to share the same ν to 3 parts in 10⁸") read stronger than the
hedged body. A skeptical reader could mis-hear "measure unique" as *directly* proving "orbit RAR
universal to 3e-8." It does not — the 3e-8 additionally assumes the reactive (O(φ²)) closure. The
caveat is present in the same documents, so this is honest work with a slightly over-strong headline.

**The load-bearing conclusion survives the closure freedom anyway (I checked the worst case).**
Two circular orbits at the same a differ *only* in ω→φ, and φ=arcsin(a₀/2cω) is bounded by
≈2.5e-4 rad at *all* orbital frequencies (branch point at period **1275 Gyr**, reproduced). So:
- reactive closure: split ~ O(φ²) ≈ 3e-8;
- absolute worst case (dissipative part entering the amplitude *linearly*): split ~ O(φ) ≈ 2.5e-4.

Either way **≪ 10%**. So claim (b) — "any O(10%) wide-binary RAR deviation at fixed g_bar cannot be
the kernel's ω-dependence, it must be the EFE channel" — is **robust to the closure freedom**,
because even the linear-in-φ worst case is 2.5e-4 ≪ 0.10. **Verdict (b): UPHELD**, with the
sharpened statement that the robust bound is "≪ 10%" (worst case 2.5e-4), while the "~1e-7" threshold
is the reactive-closure number specifically.

## 4. Dead literal closure (no MOND + secular drift) — correctly derived, no sign error

**No-MOND part is sign-independent and robust.** On the cut K(−w²+i0)=√(1−1/4w²)+i/(2w), |K|=1
exactly for w≥½. Independent evaluation: galactic w=c/v=1999 → K=0.99999997+2.50e-4 i, |K|=1.000000000
(Newtonian, no MOND) vs prescription K(1)=0.618 (MOND). O(1) different, as claimed. |K|=1 regardless
of sign convention, so the "literal closure gives no MOND / fails the RAR outright" finding is solid.

**Secular scale.** ω sin φ = a₀/2c exactly ⇒ τ = 2c/a₀ = **203 Gyr (canonical) / 168 Gyr (alt)**,
reproduced. Earth–Sun order check ṙ ~ r(a₀/2c) ≈ **0.74 m/yr** (my convention); the doc's "~0.4 m/yr"
is the same order (the factor depends on the E∝1/r convention) and is explicitly flagged as an
order-of-magnitude estimate "pending a cited ephemeris confrontation" — appropriately hedged, not
load-bearing.

**Sign.** Im K = +1/2w > 0 (retarded boundary). The doc does **not** assert a physical sign for the
drift — it says the sign "inherits the s=−1 postulate status" (KMS-passive = damping vs Machian =
gain). That is the honest reading; **no sign error** — the sign is correctly left undetermined, and
the sign-independent part (no MOND) carries the "literal closure is dead" conclusion.
**Verdict (c/d): UPHELD.**

## 5. Ancillary numbers (claim d + the MG contrast) — reproduced

- **Epicyclic law:** C = β(2β+1)/2 (sympy); deep-MOND flat-curve limit β→1, dlnμ/dlnx→1 gives
  Δlog₁₀g = −(3/4)ε²/ln10 = **−0.326 ε² dex** (hand-derived, matches). MC cross-check at ε=0.075:
  −0.00023 vs analytic −0.00021.
- **Closure-B dispersion offset (MC, seeded):** canonical mean **−0.0239**, median **−0.0111**,
  16–84% [−0.051, +0.000]; alt −0.022/−0.008; intermediate −0.019/−0.007 → the claimed
  "−0.011 to −0.024 dex" bracket. Honest non-one-signed finding holds: radial-orbit **flip positive**
  (λ=0.3, ε≈0.62 → +0.005 dex), ~13–16% positive tail. Closure A gives exactly 0. Bracket [0,
  −0.02…−0.05 with radial positive tail] is the correct derived statement.
- **QUMOND-same-ν disk contrast (rb1[5]):** spherical Plummer control returns the algebraic law to
  1.3e-5 (solver validated); Miyamoto–Nagai disk shows a signed radius-mixing split **−1.05% (inner,
  y≈11) → 0 → +2.28% (outer)**, vs MI's exact 0 at every ring. Reproduced.

## 6. Overall verdict

- **(a) ring-by-ring RAR exactness is DERIVED (first-moment identity, any worldline): UPHELD** —
  re-derived independently in curved space, no circularity.
- **(b) frequency universality / "10% wide-binary deviation must be EFE": UPHELD and robust** to the
  O(1) closure freedom (worst case 2.5e-4 ≪ 0.10). The specific "3 parts in 10⁸ / ~1e-7" figure is
  the reactive-closure value; the robust, closure-independent statement is "≪ 10%."
- **(c) literal frequency closure is dead (no MOND + secular drift a₀/2c): UPHELD** — no-MOND part
  is sign-independent (|K|=1); drift sign correctly left undetermined; no sign error.
- **(d) dispersion offset −0.011…−0.024 dex, epicyclic −0.326 ε² dex: UPHELD** (reproduced;
  epicyclic hand-derived).
- **"Measure is not free": REAL** (Herglotz + RAR ⇒ identity theorem ⇒ unique measure), correctly
  proven, and the distinct O(1) closure freedom is **NOT under-stated** in the scripts/KERNEL_THEORY.

**No manufactured win, no manufactured deficit found.** One framing tension: the headline
uniqueness phrasing is stronger than the (present, correct) hedged body — a careful reader should
read the 2.3e-8 as a minimal-closure bound, not a corollary of measure-uniqueness alone. The
framework's own open items (closure map beyond first moment; s=−1 sign; a₀ value) remain open and
are labeled as such. Nothing here is grounds to say "theory closed" or to assert a data verdict.

**Reproduce:**
```bash
cd /Users/carlzimmerman/new_physics/prep_2026/mi_fingerprint
python3 rb1_circular_exactness.py && python3 rb2_frequency_dependence.py && python3 rb3_eccentric_offset.py
# independent cross-check (curved-space identity, own arithmetic, worst-case closure bound):
#   scratchpad/independent_verify.py  (exit 0)
```
