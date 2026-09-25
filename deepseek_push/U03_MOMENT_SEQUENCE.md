# U03 — CLOSURE OF THE HIGHER-MOMENT SEQUENCE: THE EXACT GENERATED LAW

**2026-09-25 · volume window · first-flight geometric moments · CLOSED**
Files: `U03_moments.py` · `U03_moments.out` (exit 0 · **52/52 checks PASS** at
`ALL_PASSED: true`) · `U03_results.json` (every fraction + 4 quadratures +
residual + pslq witness). Two **independent quadrature parametrizations**
(A: source grid (r₀, μ); B: line coordinates (ρ, s), E[g] = (3/2)∫ρdρ∫ds),
each at **ng = 1024 and ng = 2048** — every reported fraction is certified by
all four evaluations to < 1e-10 (typically 1e-13) residual. No git commit
(lane rule).

---

## 1. The interior chord law (P1/P4) — CLOSED

For a volume-uniform isotropic source in the unit ball, the **first-flight
chord length has the exact quadratic density**

```
f(ch) = (3/4)(1 − ch²/4),   ch ∈ [0, 2]
⇔  E[chᵐ] = 3·2ᵐ / ((m+1)(m+3))
⇔  F(L) = P(ch ≤ L) = 3L/4 − L³/16
```

| m | E[chᵐ] reconstructed | exact | resid |
|---|---|---|---|
| 1 | 3/4 | 3/4 | 8.9e-14 |
| 2 | 4/5 | 4/5 | 1.3e-13 |
| 3 | 1 | 1 | 3.3e-13 |
| 4 | 48/35 | 48/35 | 6.9e-13 |
| 5 | **2** | 2 | 1.4e-12 |
| 6 | **64/21** | 64/21 | 2.7e-12 |
| 7 | 24/5 | 24/5 | 5.1e-12 |
| 8 | 256/33 | 256/33 | 9.7e-12 |

**E[ch⁵] = 2 and E[ch⁶] = 64/21 are new closed forms** (the pattern
3/4, 4/5, 1, 48/35 predicted by N02 continues exactly). The CDF check
remains a proof: the geometric survival integral evaluated piecewise-smooth
(mpmath, 50 dps) agrees with 3L/4 − L³/16 to **2.2e-16**; a 20M-sample MC
witnesses the CDF at L = 0.25/0.75/1.25/1.75 with |z| ≤ 1.

**Generating function** (sympy series verified to order t⁸):

Σₘ E[chᵐ] tᵐ = 3/(16t³) · [(1−4t²) ln(1−2t) + 2t + 2t²]

**Literature identity.** The measure is Kellerer's *interior-radiator
randomness* (i-randomness): point uniform in K, direction isotropic —
A. M. Kellerer, "Considerations on the Random Traversal of Convex Bodies and
Solutions for General Cylinders", *Radiation Research* **47**, 359–376 (1971).
Kellerer's relation for the interior chord density f_I(l) = S_μ(l)/l̄_μ,
with S_μ the μ-randomness (random-line) chord survival and l̄_μ = 4V/S
(Cauchy's mean chord), applied to the unit ball — S_μ(l) = 1 − l²/4,
l̄_μ = 4/3 — gives exactly f_I(l) = (3/4)(1 − l²/4), and
E_I[chᵐ] = ∫₀² lᵐ·(3/4)(1−l²/4) dl = 3·2ᵐ/((m+1)(m+3)).
The identity is verified numerically: 8 moments, CDF to 2e-16, MC, and the
GF coefficients all match the Kellerer integral. (Independently re-derived
here from the line-coordinate measure, Santaló-style.)

## 2. The path integrals E[∫₀^ch r(s)^{2k} ds] — CLOSED (P2/P5)

```
E[I_k] = (3/2) · k!/(k+2)! · S_k,   S_k = Σ_{j=0}^k (j+1)/(2j+1)
```

Exact values, k = 1..6 (all four quadratures agree to ≤ 3.6e-13):

| k | E[∫ r^{2k} ds] | exact | resid | status |
|---|---|---|---|---|
| 1 | 5/12 | 5/12 | 1.2e-13 | M05 re-verified |
| 2 | **17/60** | 17/60 | 1.1e-13 | **M05 correction (see §4)** |
| 3 | **149/700** | 149/700 | 1.0e-13 | **M05 candidate CERTIFIED** |
| 4 | 1069/6300 | 1069/6300 | 1.0e-13 | new |
| 5 | 13649/97020 | 13649/97020 | 1.0e-13 | new |
| 6 | **50423/420420** | 50423/420420 | 9.9e-14 | **E[∫r¹²ds] CLOSED** |

**The E[∫r⁶ds] closure (task item 4):** E[∫r⁶ds] = **149/700** exactly —
the candidate that M05 could not certify at 256-pt now holds at residual
1.0e-13 across A@1024, B@1024, A@2048, B@2048, and matches the closed form
(3/2)·6!/8!·S₃ = 894/4200 = 149/700. **E[∫r¹²ds] = 50423/420420** (q = 420420
> 10⁵ — the reconstruction budget had to be raised to 10⁶; irreducible,
50423 prime-factored against 2²·3·5·7²·11·13) — certified the same way
(resid 9.9e-14) and by direct PSLQ on its 30-digit decimal.  It is **not**
an irrational/MC-only number.

## 3. The complete cross lattice E[r0^{2a}·ch^b], a+b ≤ 6 — CLOSED (P3)

All rational (μ = 0 plane; a ≥ 1, b ≥ 1 rows certified at 2048 both ways):

| a\b | b=1 | b=2 | b=3 | b=4 | b=5 |
|---|---|---|---|---|---|
| a=1 (r0²) | 5/12 | 16/35 | 3/5 | 272/315 | 46/35 |
| a=2 (r0⁴) | 17/60 | 20/63 | 3/7 | 2192/3465 | — |
| a=3 (r0⁶) | 149/700 | 8/33 | 1/3 | — | — |
| a=4 (r0⁸) | 1069/6300 | 28/143 | — | — | — |
| a=5 (r0¹⁰) | 13649/97020 | — | — | — | — |

(Pure radial: E[r0^{2a}] = 3/(2a+3): 3/5, 3/7, 1/3, 3/11, 3/13, 1/5 — checked.)
N02's E[r0²ch²] = 16/35 re-verified; E[r0²ch³] = 3/5 is new.

**Nice identity in the data:** E[r0^{2k}·ch] = E[I_k] for every k = 1..5
(5/12, 17/60, 149/700, 1069/6300, 13649/97020) — the chord-weighted radial
moment equals the line-integral moment; the μ-odd piece ∫s·(ρ²+s²)^k ds
vanishes by symmetry in line coordinates, so the equality is exact.

**μ-lattice snapshot** (E[r0^{2a}μ^bch^c], 308 entries recorded; 299 recon to
small rationals at < 1e-10, the 9 excesses are the highest-power chord rows
with ng=1024 A-errors ~1–2e-10, record only): E[r0²μch] = −1/6,
E[r0⁴μch] = −1/8, E[r0²μch³] = −17/40, E[r0²μch⁴] = −2/3, E[r0²μ²ch²] = 8/35,
E[r0⁴μ²ch²] = 52/315.  N02's E[(p·u)ch³] = E[r0μch³] = −18/35 (r0¹-family,
outside the even lattice) is re-derived by the line-coordinate identity
∫s(h−s)³ds = −(12/5)h⁵ ⇒ −(18/5)·(1/7) = −18/35; E[r0μch⁴] = −4/5 is
MC-witnessed at 2e7 (E = −0.80026, z = −0.6).  Elements with odd μ and 2a < b carry
sqrt/log terms and are NOT small-denominator rationals (e.g.
E[r0²μch²] ≈ −0.2746773, E[μch²] ≈ −0.42274): the lattice is rational on the
μ=0 plane and on 2a ≥ b, algebraic beyond.

## 4. M05 ERRATUM — E[∫r⁴ds] is 17/60, not 1/4

M05's `I2` integrand has two coefficient bugs:
`R·μ·ch⁴/2` should be `R·μ·ch⁴`, and `(2R²μ²+R²)ch³/3` should be
`(4R²μ²+2R²)ch³/3`.  M05's ladder value 0.2500000000000 is the buggy
expression's own limit — reproduced here exactly (0.2500000000003 at
ng=1024) — while the corrected integrand gives 17/60 (all four quadratures,
resid 1.1e-13; also by the closed form (3/2)(2!/4!)(34/15) = 17/60).
**M05's E[∫r²ds] = 5/12, E[ch] = 3/4 rows are unaffected (formulas correct);
only the E[∫r⁴ds] = 1/4 row is superseded.**  N02's geometric constants and
E[∫s·r²ds] = 8/35 formulas are correct (re-verified here).

## 5. Verdict

The first-flight geometric-moment sequence is **closed by two exact laws**:
the quadratic interior-chord density (Kellerer 1971; all E[chᵐ] = 3·2ᵐ/((m+1)(m+3)))
and the harmonic-weighted path-integral law E[I_k] = (3/2)k!/(k+2)!·S_k
(closing 149/700 and 50423/420420), with a complete rational cross lattice
on the μ=0 plane.  Every fraction: two quadratures × two grid levels +
reconstruction residual < 1e-10 + pslq witness + closed-form identity.
The M05 E[∫r⁴ds] = 1/4 entry is corrected to 17/60 (bug reproduced).

— U03_moments.py/.out/U03_results.json/U03_MOMENT_SEQUENCE.md · 52/52 PASS ·
ALL_PASSED true · no git commit