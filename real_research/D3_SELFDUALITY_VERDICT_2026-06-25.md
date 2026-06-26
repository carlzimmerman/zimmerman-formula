# d=3 Self-Duality and the MOND Scale — Verdict

**C. Zimmerman, 2026-06-25.** *Does the framework's dS–Unruh MOND mechanism genuinely **select** three spatial
dimensions (the cross-product self-duality dim SO(d)=d being load-bearing), or is Z² = 32π/dim SO(3) a cosmetic
re-labeling of 32π/3? Both-ways adjudication. Numbers:
`reviews/dsunruh_d_dimensional_derivation.py` + the adversarial stress test below; sympy/mpmath dps≥40.*

---

## VERDICT: **(B) PARTIAL**

d=3 is **genuinely load-bearing at exactly one place — flat rotation curves** — and the dS–Unruh route adds real
content there (it *forces* the sqrt-law that makes flatness pick d=3, rather than positing it). But this is a
**standard MOND selection re-expressed**, not a new constraint; it is **decorative** in the scalar
a₀ = c²√(Λ/32π) value, **circular** in the read-the-dimension-back-out inversion, and **convention-dependent**
against the one external benchmark. There is **no from-below derivation of d=3** and **no flavor/TOE bridge**.
Not (A) (the selection is not unique to or forced by the dS–Unruh mechanism beyond β=½), not (C) (the flat-curve
selection is not pure triviality — β=½ is forced, not chosen).

---

## What is forced (re-verified symbolically, dps≥40)

| Fact | Status |
|---|---|
| Z² = 32π/3 exactly (= 4√6·√π/3) | **EXACT** ✓ |
| Z_d = 8√(π/[d(d−1)]); Z₃ = 2√(8π/3) = 5.7888 | **EXACT** ✓ (rel-diff ~1e-41) |
| d(d−1) = 2·dim SO(d) (Friedmann denominator) | **EXACT** ✓ |
| #vectors = #bivectors ⟺ d = d(d−1)/2 ⟺ **d=3 only** | **EXACT** ✓ (checked d=2..6) |
| dim SO(d) = d ⟺ d=3 only | **EXACT** ✓ |
| dS–Unruh excess ΔT = √(a²+(cH)²)−cH ~ a²/2cH (quadratic) | **EXACT** ✓ |
| deep-MOND v² ~ r^((3−d)/2); FLAT ⟺ d=3 | **EXACT** ✓ |
| a₀(Λ,d=3) = c²√(Λ/32π) | **EXACT** ✓ |

All three special conditions — **flatness** (1−(d−1)/2 = 0), **self-duality** (d = d(d−1)/2), and
**dim SO(d)=d** — reduce to the **same single equation (d−1)=2**. That coincidence is real, not engineered.

---

## The one place d=3 is genuinely load-bearing: FLAT ROTATION CURVES

The derivation chain, with the two skeptic-flagged smuggles audited out:

1. **Force law from Gauss in d dims (NOT assumed 1/r²):** flux through the (d−1)-sphere gives g_N ~ G M/r^(d−1).
   The d-dependence of the force law is *independently forced* by flux conservation — not borrowed from AQUAL's
   d-baked Poisson operator. ✓ not smuggled.
2. **Inertia law from dS–Unruh (d-agnostic):** the codim-1 hyperboloid embedding of de Sitter_D in flat
   Minkowski_(D+1) gives T(a) = √(a²+(cH)²) for **any** D (Deser–Levin gr-qc/9706018, web-confirmed; the
   Gibbons–Hawking floor T(0)=ħH/2π is dimension-independent). The quadratic excess ΔT ~ a²/2cH **forces the
   deep-MOND slope β=½** (a = √(a₀ g_N)), with **no reference to d**. ✓ not smuggled, and β=½ is *forced not chosen*.
3. **Circular orbit:** v² = a·r = √(a₀ g_N)·r ~ r^(1−(d−1)/2) = r^((3−d)/2). **Flat ⟺ (3−d)/2 = 0 ⟺ d=3.**

The cancellation that makes the curve flat needs the Gauss codimension (d−1) to equal 1/β = 2. Since **β=½ is
supplied by the temperature physics independently of d**, this is a real selection: "a sqrt-law acceleration scale
gives flat curves" picks **exactly the self-dual dimension**, and (d−1)=2 *is literally* the self-duality equation
#vec=#bivec. This is the framework's genuine, elegant content.

---

## Where it fails to reach (A) — the merciless both-ways audit

**1. The flat-curve selection is a STANDARD MOND result, not unique to dS–Unruh.** Any sqrt-law MOND
(modified-inertia OR AQUAL modified-gravity) gives v² ~ r^((3−d)/2) and flattens at d=3. The dS–Unruh route's
*only* value-add over generic MOND is that it **derives** β=½ from ΔT~a² instead of positing it. Real, but narrow.

**2. Each force law flattens at its OWN d — so "flat⟺d=3" is conditional on the law (TEST A).** Generic
g~g_N^β gives flatness at d = 1+1/β: Newton (β=1) flattens at **d=2**, deep-MOND (β=½) at **d=3**, β=⅓ at d=4.
The selection power lives entirely in *forcing β=½*; given that, (d−1)=2 follows. The dS–Unruh mechanism does
force β=½ (TEST B) — which is why this is (B) and not (C) — but the "selection" is "given the sqrt law, flatness
needs d=3," not "the mechanism, from below, requires space to be 3D."

**3. The scalar a₀ = c²√(Λ/32π) value NEVER invokes self-duality — DECORATIVE there (TEST D).** The a₀ chain is
purely scalar: surface gravity κ=c²/2R, Friedmann H²=8πGρ/3, scalar density. **No cross-product, no curl, no
bivector ever appears.** The "3" in 8π/3 is the **assumed FRW spatial-slice dimension** (an input fixing 3+1
spacetime), not something the equation solves for. Z² = 32π/dim SO(3) is a **true re-labeling** of 32π/3:
dim SO(d)=d coincides with d only AT d=3, so substituting "dim SO(3)" for "3" adds **zero** constraint — it cannot
predict or falsify anything 3 cannot already. The framework's own DEEP_GEOMETRY.md "self-duality" is a *different*
object — the UV/IR self-dual **radius** r→r_s R_H/r — unrelated to the d=3 bivector self-duality.

**4. The read-the-dimension-back-out inversion is CIRCULAR (TEST C).** a₀/cH = 0.173 ⟹ d(d−1) = 64π(a₀/cH)² = 6.0
⟹ d=3 is arithmetically exact, but it **inverts the same Z_d algebra it was built from**. It is an internal
consistency check, not an independent measurement of d. (The framework's own GEOMETRY_OF_Z.md already says exactly
this: "a consistency check, not a precision measurement.")

**5. The external benchmark DISAGREES on the value — convention-dependence (web-confirmed).** Varieschi's Newtonian
Fractional-Dimension Gravity (arXiv:2003.05784, Found. Phys. 50, 1608, 2020) places the **deep-MOND / flat-curve
regime at D ≈ 2, NOT D=3** — because it varies the dimension of the **source measure**, not the ambient space.
Varieschi states explicitly he is "unable to derive this dimension function from first principles" — it is fixed
empirically. So "deep-MOND lives at d=3" vs "D≈2" is a **convention about which d is varied** (ambient vs source).
The dimension is a field-wide *input*, never a from-below result. This is the decisive blow against reading the
framework's d=3 as a forced selection.

---

## HONEST CEILING (stated plainly, both ways)

- **This is at most a gravity-side SELECTION/CONSISTENCY insight, NOT a from-below derivation of d=3.** Nothing
  here explains *why* space is three-dimensional. The mechanism (dS–Unruh temperature, μ(a), the sqrt-law) and
  a₀'s **magnitude** (~cH ~ c²√Λ, finite for every d≥2) are genuinely **d-agnostic**; d enters only through
  flat-curve geometry and the numeric coefficient Z_d.
- **No flavor/particle/TOE bridge.** This is purely the gravity-side d-question. (Consistent with the closed
  particle-numerology and TOE-path standing: the cosmology trick does not transfer to the SM.)
- **Not manufacturing a deficit either.** The framework's own documents already state the correct modest claim —
  GEOMETRY_OF_Z.md: "Z is geometrically natural and meaningful... and that is exactly as much as the math
  supports"; DEEP_GEOMETRY.md calls the read-out "a consistency check, not a precision measurement." Those are the
  right level. The verified TRUE content stands: Z_d = 8√(π/[d(d−1)]) is a genuine non-trivial d-dependence (the
  coefficient really *is* the value 3D GR forces once you assume d=3), and the flat-curve ⟺ self-duality identity
  (d−1)=2 is real and elegant.

**Best defensible one-liner:** *"Given the dS–Unruh-forced sqrt-inertia law, a MOND acceleration scale yields flat
rotation curves only in the self-dual dimension (d−1)=2 ⟹ d=3 — a genuine consistency/selection tie between
flatness and the cross-product self-duality; but it re-expresses a standard MOND fact, is decorative in the scalar
a₀ value, is circular in the dimension read-out, and does not derive d=3 from below."*

---

## Ledger

| Claim | Verdict |
|---|---|
| dS–Unruh temperature, μ(a), sqrt-law β=½ forced | **d-AGNOSTIC** (mechanism closes for any d); β=½ forced ✓ |
| a₀ magnitude ~cH ~ c²√Λ | **d-AGNOSTIC** (finite all d≥2) |
| Z_d = 8√(π/[d(d−1)]); coefficient = the value 3D forces | **CONSISTENCY** (true, re-expressible via d=3) |
| Flat rotation curves ⟺ d=3 | **SELECTION** but standard-MOND-shared (real value-add = forced β=½) |
| flatness ⟺ self-duality ⟺ dim SO(d)=d, all (d−1)=2 | **REAL identity**, a-priori-distinct physics coinciding at d=3 |
| Z² = 32π/dim SO(3) in the scalar a₀ chain | **DECORATIVE** (re-label of 32π/3; never invokes bivectors) |
| a₀/cH ⟹ d=3 read-out | **CIRCULAR** (inverts its own algebra) |
| External benchmark (Varieschi NFDG) | **D≈2 under source-measure convention** — dimension is an input |
| From-below derivation of d=3 / flavor bridge | **NONE** |

**NET: PARTIAL.** Real selection at flat curves with a genuine (narrow) dS–Unruh value-add; decorative in the a₀
value; circular in the read-out; convention-dependent against the field; no from-below d=3, no TOE bridge.
