# L40 — RIGIDITY: can L32's three survivors fix β/√Z̃ = 0.354 with no freedom left?

`L40_coefficient_rigidity.py` / `.out` — 21 checks, **15 FAIL**. Every FAIL is an obstruction established or a
candidate refuted, not a defect discovered; each check's detail line says which way it points.

**Answer: no. κ remains FITTED.** Two structures are EXCLUDED, two RELOCATE, and none derives anything. The
useful part is *how* each fails, and that two of them fail by being **refuted** — which means they were, for the
first time in this corpus, rigid enough to be wrong.

---

## 0. What L32 handed this lane

Once a₀ is promoted to a dynamical order parameter — L32's T5 shows that is **necessary**, since no curvature
polynomial on de Sitter takes a half-integer power of Λ — the *form* of `a₀ = κ c√(Gρ_Λ)` is structural, the
amplitude cancels, and the whole coefficient problem is one dimensionless coupling:

    kappa = sqrt(2) beta/sqrt(Ztilde)   <=>   beta/sqrt(Ztilde) = kappa/sqrt(2) = 0.354   <=>   lambda = Ztilde/beta^2 = 8

A1 reproduces that independently: `ε = qP_q − P = Z̃q²/2`, `a₀ = β√G q`, so `κ² = a₀²/(Gε) = 2β²/Z̃` with the
amplitude **and G** cancelling identically, and `κ = ½ ⟺ Z̃/β² = 8` exactly (L3's four-form-only ratio is
`Z/β² = 8 − 2b = 7.964`). A2 reproduces the combined measurement **κ = 0.5301 ± 0.0374**, 8.0% total comparison
uncertainty. A3 reproduces L32's numerology guard exactly — **27** simple numbers in the 3σ statistical band, 29
with the H₀ convention — which is what **calibrates the candidate-set counter** used against every structure below.

---

## 1. Two guards that apply before any structure is tested

**A4 — the target integer is footing-dependent.** `λ = 2/κ²` is **8.001 on the canonical footing** and **5.512 on
the alt footing**: 0.001 from an integer on one, **0.488** from the nearest integer on the other, which is as far
from any integer as it is possible to be. "λ = 8" is a canonical-footing statement, exactly the guard L3's Q8 and
L32's A2 raise about "32π". An integer-valued principle would have to select the footing as well as the integer.

**A5 — the evidence ceiling, and it outlives every mechanism.** The 3σ band maps to `λ ∈ [4.62, 12.35]`, which
contains the integers **5, 6, 7, 8, 9, 10, 11, 12**. Under a uniform prior over small integers λ ∈ 1…32, a correct
integer prediction lands in the band with probability 0.25, so **a perfect, zero-freedom integer derivation of
λ = 8 is worth at most 2.0 bits = 1.7σ-equivalent**. This bounds the coefficient as evidence *independently of the
mechanism*, and it is the quantitative form of L32's N6: the derivation is the evidence, never the proximity —
and the registered a₀(z) measurement, not κ, is the discriminating observable.

---

## 2. The three survivors, tested

### S8 — horizon thermodynamics. **Verdict: EXCLUDED as a derivation. Free choices: 1.**

The question the lane was asked to settle — *derivation or identification?* — is settled, and the answer is
**identification**.

- **B1, the identity.** Unruh: `T_U(a) = ħa/(2πck_B)`. Gibbons–Hawking: `T_dS = ħc/(2πk_B L_dS)`. The 2π is
  **the same factor on both sides and cancels** when the temperatures are equated, forcing `a₀ = c²/L_dS`, i.e.
  ζ = 1 exactly, **κ = √(8π/3) = 2.894**. That is 5.79× (canonical) / 4.81× (alt) the framework's a₀ and **56σ**
  from the measurement. **This is a REFUTATION of the zero-freedom form**, not a relocation. (Milgrom 1999's
  ζ = 2 variant is already excluded at 15.6σ in-corpus.)
- **B2, the 2π.** Reaching κ = 0.4607 requires `T_U(a₀) = T_dS/(2π)` — **not an identity, an assignment**. Of
  eight enumerated horizon routes, every identity-forced one gives ζ ∈ {0.5, 1.0} (surface gravity, Brown–York,
  Misner–Sharp, Unruh=GH), **none in the band**; every route that reaches the band has a factor put in by hand.
- **B3, rigidity.** The route's own candidate set for ζ (104 simple rationals and π-forms) puts **7** members in
  the band — including 1/6, Milgrom's original `a₀ ≈ cH₀/6`. One free choice, unfixed by any identity.
- **B4, the convention.** ½ and 0.4607 are 8.5% apart = **1.11 × the full Planck→SH0ES span**. `a₀(½, Planck)` and
  `a₀(0.4607, SH0ES)` agree to **0.21%**. A coefficient a change of cosmological convention absorbs carries
  essentially no information. (k03's P2, reproduced independently here.)

### S9 — dimensional transmutation, two condensates in one strongly coupled sector. **Verdict: RELOCATES, into a CONTINUUM. Free choices: 4 discrete + ≥2 continuous.**

- **C1 — credit where it is due, and it is real.** With `Λ_c = μ exp(−8π²/(b₀g²))`, `X = c_X Λ_c²`,
  `ρ_vac = c₂Λ_c⁴`, the result is `κ = β c_X/√c₂`: **the coupling g, the matching scale μ and the beta-function
  coefficient b₀ all cancel identically**. The LOCK (N3) is automatic. S9 genuinely satisfies N1–N3.
- **C2 — and then it fails N4 on the only number left.** Tested on the one strongly coupled sector whose
  condensates are *measured*: `⟨q̄q⟩^{2/3}/√⟨(α_s/π)G²⟩`, with Λ_c cancelling between them. Across the quoted
  ranges (⟨q̄q⟩ at μ = 1/2/3 GeV in MS-bar; ⟨G²⟩ over 0.005–0.024 GeV⁴) the prediction runs **0.391 → 1.149**, a
  factor 2.9, with **3 of 9 combinations in the band and 6 outside**. The number moves from inside to outside the
  band **with the renormalisation scheme alone**.
- **C3 — the deeper reason.** The symbols surviving into κ are `beta, c_2, c_X` — **all continuous**; the only
  integer-valued datum of the sector, b₀, cancels *together with* the coupling. The candidate set contains an
  interval, i.e. has positive measure, and a set of positive measure supplies **zero** evidence whichever member
  is realised. That is strictly worse than the 27-member numerology baseline, not better.
- **C4 — and β.** β survives explicitly. Either the MOND sector is external (β is a Wilson coefficient, continuous)
  or internal (β is an uncomputable non-perturbative O(1)). This is **T2's split degeneracy reappearing in a new
  sector**: the strong dynamics sets Z̃ but never the split between Z̃ and β.

### S10 — nonlinear realisation / coset. **Verdict: RELOCATES. Free choices: 5.**

L32 flagged this as the only structure that could supply RIGIDITY. It turns out to be **rigid about the wrong
number**, and the freedom it needs to reach 0.354 destroys the rigidity.

- **D1 — the zero-freedom form, and its refutation.** A coset G/H whose isotropy representation is **irreducible**
  has a G-invariant metric unique up to overall scale (all irreducible symmetric spaces are of this type). One
  invariant metric ⇒ one normalisation F² ⇒ the order parameter's stiffness and its coupling to the second sector
  are **the same invariant** ⇒ `β/√Z̃ = 1` exactly ⇒ **κ = √2 = 1.414**, i.e. λ = 1. That is **21σ** from the
  measurement. **REFUTED.**
- **D2 — the candidate set.** Built from standard Lie-algebra tables (33 simple algebras, 19 maximal-subgroup
  chains) in six structurally motivated families — √(T(F)/T(adj)), the WZW/GKO level √(k/(k+h^∨)),
  √(C₂(F)/C₂(adj)), coset dimension ratios, 1/√(index), √(rank/dim) — giving **557** candidate values for β/√Z̃.
  **97 lie inside the band** against the calibrated numerology baseline of **27**. Group theory is not scarce: the
  route supplies *more* ways to land in the band, not fewer.
- **D3 — the exact hits, reported in full and NOT adopted.** `β/√Z̃ = 1/√8 = 0.353553` is hit **exactly** by
  **9** members of the set, from structurally different constructions:

  | construction | value |
  |---|---|
  | √(T(F)/T(adj)) for **SU(4)**, **SO(10)**, **Sp(6)** | 1/√8 |
  | √(k/(k+h^∨)) for **SU(7)₁**, **SO(9)₁**, **Sp(12)₁**, **SO(16)₂** | 1/√8 |
  | 1/√m at **m = 8** | 1/√8 |
  | √(rank/dim) for **SU(7)** | 1/√8 |

  Each would read as a derivation of κ = ½ if quoted alone. **That they disagree about which group and which
  level is the proof that none of them derives anything.** They coincide because λ = 8 is a small integer and
  small integers are what all such structures produce — 8 is also dim(adj SU(3)), h^∨(SU(8)), and 2³.
- **D4 — the dichotomy with no interior.** Five free choices (G; H/embedding; representation; level; which
  invariant carries the stiffness vs the coupling). Irreducible isotropy removes the last one and forces κ = √2
  (refuted). Reducible isotropy gives one independent invariant metric per irreducible summand, each with its own
  free normalisation — so the coefficient is a **continuous** ratio again, not a group-theoretic one. **There is
  no coset that is rigid AND lands in the band.**

---

## 3. THEOREM T7 — L3's surviving membrane door, closed

L3's Q5 left one door: make the membrane charge `e` or tension `T` depend on β at fixed Z̃. E1 first notes that
the flux amplitude **cancels identically** from `κ² = 2β²/Z̃`, so `e(β)` cannot act through the amplitude — it can
only act through whatever equation determines Z̃. Both such equations are tested, with `e = e₀β^p`, `T = T₀β^s`:

| branch | Z̃ fixed by | rigidity requires | consequence |
|---|---|---|---|
| **1** | matching the flux energy to the observed vacuum energy, `n²e²/(2Z̃) = ε_obs` | p = 1 | then `κ² = 4ε_obs/(n²e₀²)` — a function of the *observed* Λ, not a pure number — and `a₀ = 2√G ε_obs/(ne₀)` gives **d ln a₀/d ln Λ = 1, not ½: the LOCK fails** |
| **2** | the terminal nucleation condition `Δε = 6πGT²` | p − s = 1 | LOCK holds along β (exponent ½) but `κ² = 24πGT₀²/(e₀²(2n−1))` is **continuous in T₀/e₀**; and along T₀ the LOCK exponent is **1**, while along e₀ **a₀ moves at fixed Λ** (`d ln ε = 0`, `d ln a₀ = −1`) |

**T7: an a₀-dependent membrane charge or tension is a pincer with no interior — either the LOCK (N3) breaks or the
coefficient (N4) stays continuous.** This closes the door L3 and L32 both left open. Verdict: **EXCLUDED.**

---

## 4. The verdict table

| structure | free choices | candidate set | in band | verdict |
|---|---|---|---|---|
| **S8** horizon thermodynamics | **1** | 104 | 7 | **EXCLUDED** — zero-choice form refuted at κ = 2.894 (56σ); the 1/(2π) is inserted, not derived; absorbed by the H₀ convention |
| **S9** two-condensate transmutation | **6** (4 discrete + ≥2 continuous) | continuum | continuum | **RELOCATES** — LOCK automatic (real credit); the surviving number is a scheme-dependent non-perturbative O(1), 0.39–1.15 on QCD's own condensates |
| **S10** coset / nonlinear realisation | **5** | 557 | 97 | **RELOCATES** — zero-choice form refuted at κ = √2 (21σ); 9 exact hits on 1/√8 from different groups |
| **L3** a₀-dependent membrane | **3** | — | — | **EXCLUDED** by T7 |

**Refutation ledger** (zero-freedom forms whose forced value lands outside the band — results, not failures of the
search; both excluded on both a₀ footings, adopted κ = 0.500 canonical / 0.602 alt):

| structure | forces | significance |
|---|---|---|
| S8, Unruh = Gibbons–Hawking | κ = 2.8944 | 56σ |
| S10, isotropy-irreducible coset | κ = 1.4142 | 21σ |

**None DERIVES.** With T1–T6 (L32) plus T7 (here), **eight of the ten enumerated structures are closed by theorem**,
and the two that survive as structures relocate the fit — into a discrete choice with 97 in-band members against a
27-member numerology baseline, or into a continuum.

---

## 5. Verdict

None of L32's three survivors derives κ, and the coefficient problem is now closed in general form rather than for
one action: horizon thermodynamics is settled as an **identification** — the 2π of the Unruh formula and the 2π of
the Gibbons–Hawking formula are the *same* 2π and cancel when the temperatures are equated, so the only
identity-forced statement is a₀ = cH_Λ, refuted at 56σ, and reaching 0.4607 means putting the 2π back by hand into
a coefficient the H₀ convention absorbs anyway. Two-condensate transmutation earns its LOCK honestly and then loses
every discrete datum along with the coupling, leaving a scheme-dependent prefactor that crosses the band boundary
under a change of renormalisation scale; and the coset route, the one L32 hoped could supply rigidity, is rigid
only about κ = √2 (21σ out) and needs five choices to reach 0.354 — which it then reaches **nine different ways**.

Two limits on all of it, stated. This closes the *enumerated* structures, not the search: L32's N3 is a condition a
theory must meet, not a fact about nature, so "a₀ and Λ are independent constants that coincide" remains live, and a
structure nobody has enumerated remains possible. And even a perfect derivation would be nearly worthless as
evidence: the 3σ band contains 8 integers in λ, capping any integer-valued derivation at 1.7σ-equivalent, and
λ = 8 is a canonical-footing statement (5.51, and maximally non-integer, on the alt footing).

**κ = ½ remains FITTED. Nothing here derives it, and nothing here makes ½ preferred over 0.461.**
