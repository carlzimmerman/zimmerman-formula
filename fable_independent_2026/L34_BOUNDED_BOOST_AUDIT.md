# L34 — the bounded-boost theorem audited against perturbative well-definedness

2026-09-08. Lane L34 of [CHARTER.md](CHARTER.md).
Script: [L34_boost_vs_cubic.py](L34_boost_vs_cubic.py) → [L34_boost_vs_cubic.out](L34_boost_vs_cubic.out).
**21 PASS, 11 FAIL. All 17 controls PASS**; every FAIL is a substantive finding, none a machinery failure.

Target: **PAPER5_bounded_boost_2026.tex**, DOI 10.5281/zenodo.22548669, already deposited.
Trigger: L13's P9 scope note — beyond `s_sat` the carried kernel has `Δ' = 0` exactly, so `Σ_∥ = 1/Δ'` is
infinite and the MOND scalar's cubic action at the Solar-System background cannot be written.

## Verdict in one line

**No tension inside the theorem. Two repairs to the paper.** The theorem's hypotheses do admit a
twice-differentiable kernel, so the deposited *theorem* is sound; what is wrong is (a) its printed
conclusion that the bound is *attained* on a plateau — an attained supremum has no cubic action — and
(b) its silence about a corollary its own hypotheses force: **no kernel of the class can screen the
Solar System at all**, so the coherence length ξ is mandatory rather than a design choice. The second
is a strengthening of the paper, not a refutation of it.

---

## 1. The theorem's hypotheses, and which one forces saturation

PAPER5 §7, restated exactly. A matter-sourced scalar obeys `∇·[J_Y ∇φ] = 4πGρ`. The paper's three
load-bearing steps, each reproduced here independently rather than quoted:

| step | statement | control |
|---|---|---|
| H1 | Gauss on a sphere ⇒ `J_Y(g_φ) g_φ = g_N`, so `g_φ` is single-valued in `g_N` | **A3** (sympy, exact) |
| H2 | the longitudinal stiffness `dg_N/dg_φ` must be positive or the static problem is ill posed | assumption |
| H3 | writing `g_φ = a₀Δ(s)`, `s = g_N/a₀`, that stiffness is `Σ_∥ = J + 2Y dJ/dY = 1/Δ'(s)` | **A4** (sympy, identity for arbitrary Δ) |

`Σ_∥ = 1/Δ'` was verified as an *exact identity in an arbitrary `Δ`*, not sampled:

```
Sigma_par = J + 2Y dJ/dY = 1/Derivative(Delta(s), s)
```

**H2 is the hypothesis that forces saturation.** H1 and H3 are kinematics; H2 is the physics input
(well-posedness of the static BVP, equivalently no longitudinal ghost / gradient instability in the
covariant completion). It forces `Δ' > 0`, hence `Δ` strictly increasing, hence — with boundedness —
a finite limit `C`. Everything below is a consequence of H2 alone.

**Controls reproducing the paper (all PASS).** `Δ_exp = y e^{-y}`, unique critical point `y = 1`,
`Δ_max = 1/e`, `Δ'' = -1/e < 0` (A1). Carried kernel `ν_RAR`: `s_sat = 2.5396`, `C = 0.64761`
against the paper's 2.540 / 0.6476 (A2). All five suprema of the paper's Table 1 (A5). The stiffness
sign change at `0.6321 a₀` and `2.5396 a₀`, "exactly at the two maxima" (A6). The g03d gates (A7).

---

## 2. The three requirements, and the pincer

As conditions on `Δ` on `[0, ∞)`:

- **(i) bounded** — `Δ ≤ C`. The theorem's own conclusion.
- **(ii) positive stiffness** — `Δ'(s) > 0` at every finite `s`, so `Σ_∥` is finite and the cubic action exists.
- **(iii) the Solar System screens** — `a₀Δ(s)` below the ephemeris gates at `s ~ 10⁵–10⁸`.

Gates verbatim from `g03d_exact_fourth_order_solar.py`. The **binding** one is not the sunward gate
but the Pitjev–Pitjeva phantom mass inside Saturn, converted to an acceleration:

| gate | value | in units of a₀ (canonical / alt) |
|---|---|---|
| sunward ephemeris | 3.662e-14 m/s² | 3.912e-4 / 3.247e-4 |
| **phantom mass inside Saturn**, 6.7e-11 M☉ | **4.330e-15 m/s²** | **4.625e-5 / 3.839e-5** |

### The lemma

(ii) ⇒ `Δ` strictly increasing ⇒ `sup Δ = lim_{s→∞} Δ = C`, and `Δ(s_gal) < Δ(s_⊙)` for **every**
galactic `s_gal` below every Solar-System `s_⊙`. So (iii), which caps `Δ(s_⊙)` at `B`, caps `Δ` **in
galaxies** at the same `B`. That is the whole argument; it needs no computation.

### The numbers

| footing | binding B/a₀ | carried kernel C | measured in galaxies (Table 2) | shortfall |
|---|---|---|---|---|
| canonical | 4.625e-5 | 0.6476 | 1.190 | **1.400e4×** (2.573e4× vs measured) |
| alt | 3.839e-5 | 0.6476 | 1.190 | **1.687e4×** (3.100e4× vs measured) |

In physical units: the irreducible residual `C a₀ = 6.063e-11 m/s²` is 1.4e4× the Saturn phantom-mass
gate, 1.66e3× the sunward gate, and corresponds to **9.38e-7 M☉ inside Saturn against a 6.7e-11 M☉
bound**. Even the narrowest kernel in the paper's own Table 1 (standard μ, `C = 0.3003`) is 6.5e3× over.

**(i), (ii) and (iii) are mutually exclusive for the kernel alone.** [FAIL B1]

A 40 000-member randomized scan over bounded strictly-increasing kernels
(`Δ = Σᵢ wᵢ[1 − (1 + s/sᵢ)^{−pᵢ}]`, 1–3 terms, `sᵢ ∈ [10⁻², 10⁸]`, `pᵢ ∈ [10⁻², 10]`) confirms it:
9162 boost galaxies, **0** screen the Solar System, intersection empty. [FAIL B3]

**The scan is not rigged** [PASS B4]: PAPER5's own "exponential inverse partner (unsaturated)",
`Δ = s/(e^s − 1)`, screens the Solar System *perfectly* (`Δ` underflows to zero at Neptune) and boosts
galaxies to 0.49 — it satisfies (i) and (iii) and fails **only** (ii), with `Δ'(2) = −0.206 < 0`, i.e.
`Σ_∥ < 0`. That is exactly the object the theorem forbids, and it is exactly the object that screens.
The pincer is the theorem's own content, seen from the Solar-System side.

---

## 3. Is the asymptotic divergence of `Σ_∥` harmful?

**`Δ' → 0` is unavoidable** [FAIL C1, meaning: it cannot be avoided]. If `Δ' ≥ h > 0` everywhere then
`Δ(S) ≥ hS → ∞`, contradicting boundedness. So `inf Δ' = 0` and `sup Σ_∥ = +∞` for **every** member of
the class. Only its harmfulness is in question.

### The cubic action

Expanding `L = −W(Y)`, `Y = |∇φ|²`, in a longitudinal fluctuation `h = ∂_∥ψ` about a background `ḡ`:

```
L2 coefficient   Sigma_par = W' + 2 g^2 W''
L3 coefficient   kappa3    = 2 g W'' + (4/3) g^3 W'''  ==  (1/3) d Sigma_par / d g_phi   [exact]
```

the last an exact polynomial identity (C2, PASS). Hence the strong-coupling **amplitude**

```
g_*(s) = 3 Sigma_par / |d Sigma_par/d g_phi| = 3 a0 Delta'(s)^2 / |Delta''(s)|
```

(C3, sympy, exact for arbitrary `Δ`; C7, reconstructed from `W'(Y) = J/2` at 60-digit precision and
agreeing to 1e-18).

- **The published kernel has no cubic action at any Solar-System background** [FAIL C4]. `Δ' = 0`
  identically for `s > 2.540`, so `Σ_∥ = ∞` at `s =` 7.0e4 (Neptune), 6.9e5 (Saturn), 6.3e7 (Earth),
  1.1e12 (Cassini conjunction). Independent confirmation of L13's P9.
- **An asymptotically-saturating kernel does** [PASS C5]: `Δ = C[1 − (1 + s/s₀)^{−p}]` has finite
  positive `Σ_∥` at every finite `s` (2.98e9 at Neptune, 2.44e15 at Earth, 7.96e23 at Cassini for `p = 1`).

### How fast the perturbative window closes

For a power-law approach, exactly [PASS C6]:

```
g_*(s) = [3p/(p+1)] * (C a0 - g_phi(s))
```

**the strong-coupling amplitude is proportional to the remaining gap to saturation.** Hard saturation
(gap ≡ 0) gives `g_* = 0` — the L13 pathology as a limit of this formula.

---

## 4. The sharp version

The Solar-System fluctuation the expansion must control: a planet's own scalar field,
`δg = G M_p/(Σ_∥,eff R_p²)`. Perturbativity needs `δg < g_*`. Both shrink as `Δ' → 0`; the ratio decides.

### Kernel alone — strongly coupled for *every* member of the class [FAIL D2]

```
delta_g / g_* = [(p+1)/3] (M_p/M_sun) (r_p/R_p)^2
```

The ceiling `C`, the saturation scale `s₀` and `a₀` **all cancel** (D1, PASS, matches the direct
computation to 1%; both footings give the identical number). Values: 552(p+1) for Earth, 5.7e4(p+1)
for Saturn, **3.8e4(p+1) for Jupiter**. The minimum over the whole scan is 580. Perturbativity without
ξ would need `p < −0.998`: no saturating kernel qualifies.

### With ξ at the paper's own floor — a *bounded* rescue [PASS D3, FAIL D4]

ξ enters inside `𝒥`'s argument, so a mode of wavenumber `k` adds `J ξ²k²` to `Σ_∥` **and**
`(Σ_∥ − J)ξ²k²/ḡ` to the cubic coefficient. Both limits were carried in one expression. At
`ξ = 0.10 pc` (canonical) / `0.15 pc` (alt) the theory is perturbative for slow saturation
(`δg/g_* = 1.8e-7` at `p = 1` for Earth) but **not** for fast saturation. Solving `δg = g_*`:

| footing | ξ [pc] | Earth | Jupiter | Saturn |
|---|---|---|---|---|
| canonical | 0.10 | 1.952 | **1.754** | 1.932 |
| alt | 0.15 | 2.024 | 1.841 | 2.031 |

**Binding `p_max = 1.754`.** Robust: two decades of threshold in the `L₃/L₂` criterion move it by 0.35
(D4b, PASS — the ratio runs ~7 decades per unit `p`), and it is independent of the radius at which the
source's field is evaluated, to 7e-8 over a 100× range (D4c, PASS — in the ξ-dominated regime
`Σ_eff → Jξ²/R_p²` so the `R_p²` cancels). An **exponential** approach to saturation is excluded.

### The ceiling is untouched [FAIL D5]

At fixed `p`, `δg/g_*` varies by 1.4e-14 relative across a 30× range of `C` (0.10 → 3.00), and `p_max`
is identical. **Perturbativity constrains the saturation RATE, never the ceiling.** There is no second
pincer: the boost ceiling galaxies require and the cubic action do not conflict.

### Which of the paper's own kernels survive [PASS D6]

| kernel | C | sup attained at | admissible? |
|---|---|---|---|
| deep-MOND √ | 0.2500 | s = 0.250 | NO |
| standard μ | 0.3003 | s = 0.486 | NO |
| exponential carrier | 0.3679 | s = 0.632 | NO |
| ν_RAR (carried) | 0.6476 | s = 2.540 | NO |
| **simple μ** | **1.0000** | **s → ∞** | **yes** |

Exactly one of the five is admissible as written — and it is the *widest* one, the `C = 1.000` bound
against which the paper reports 99.23% SPARC compliance. Its approach is `1 − 1/y`, i.e. `p = 1`,
comfortably below `p_max = 1.75`.

---

## 5. What the theorem should say

**(1) [unchanged]** Gauss's law forces `J(g_φ²) g_φ = g_N`; `Σ_∥ = J + 2Y dJ/dY = 1/Δ'(s)`, identically.

**(2) [unchanged]** Well-posedness requires `Σ_∥ > 0`, hence `Δ' > 0`: `Δ` is strictly increasing.

**(3) [SHARPENED]** `Δ` is bounded iff it has a finite limit `C = lim_{s→∞} Δ = sup Δ`, **and the
supremum is never attained at finite `s`**. A kernel that attains its supremum on a plateau has
`Δ' = 0` there, hence `Σ_∥ = ∞`, an infinite-slope `J(Y)` at `Y = (C a₀)²`, and no cubic action: it is
not an admissible member of the class. Saturation is **asymptotic, not attained**.

**(4) [NEW COROLLARY — the screening corollary]** Because `Δ` is increasing, the residual scalar force
at Solar-System accelerations is **at least the galactic boost**, while the Saturn phantom-mass gate
caps it at `4.63e-5 a₀` / `3.84e-5 a₀`. The shortfall is 1.4e4× / 1.7e4× for the carried kernel and
never below 6.5e3×. **No kernel of the class can screen the Solar System.** Screening must come from an
operator *outside* the class — here the coherence length ξ, which screens by **gradient scale**
(`ξk ≫ 1` in the Solar System, `≪ 1` in galaxies), not by acceleration. The theorem does not merely
permit ξ; it **requires** it, or an equivalent second scale.

**(5) [SCOPE]** With such an operator present, `J(g_φ²) g_φ = g_N` holds only in the long-wavelength
limit `ξk → 0` — exactly the regime of the galaxy and cluster tests, so §§3–6 are untouched.

**(6) [PERTURBATIVE STATUS]** `g_*(s) = 3a₀Δ'²/|Δ''| = [3p/(p+1)](C a₀ − g_φ(s))`. The kernel alone is
strongly coupled at a planet by 5.5e2 (Earth) to 3.8e4 (Jupiter) for **every** member of the class;
perturbative control in the Solar System is a property of ξ, not of the kernel.

**(7) [NEW CONSTRAINT]** ξ buys a bounded amount: `p_max = 1.754` at the paper's own ξ floor. Faster
approaches — exponential in particular — are strongly coupled at a Solar-System body even with the
screening. This constrains the rate, never the ceiling.

---

## 6. What this costs the deposited paper

| item | status |
|---|---|
| the theorem (§7) | **sound.** No erratum to the mathematics [FAIL E5 = no internal contradiction] |
| "the bound is attained on a plateau" (§2), "must saturate at `C a₀` above it" (§7) | **erratum.** Replace "attained" by "approached"; `sup Δ` is the same number either way |
| the carried kernel's implementation (`Delta = 0.6476` for `s > 2.540`, as coded across the repo) | **must be replaced** by a `C²` continuation with `Δ' > 0`. That search is L30's lane, not this one; L34 only fixes the target: bounded, strictly increasing, `p ≲ 1.75` |
| Table 1 | four of five entries need the same wording fix; the simple-μ row is already correct |
| §9's treatment of ξ as an implementation choice | **upgrade to a corollary.** ξ is forced |
| §§3–6 — the ceiling, SPARC, the cluster violation | **stand as published** [PASS E4] |
| §11's gate ladder | untouched: `J_Y`'s saturated slope `1/C` is unchanged by asymptotic rather than attained saturation |

Nothing here weakens the paper's two positive results. The ceiling is still a parameter-free prediction
a halo model cannot make, and clusters still violate it by a margin no interpolation function absorbs.

---

## Controls (17, all PASS)

| control | reproduces |
|---|---|
| A1 | `Δ_exp = y e^{−y}`: unique critical point, `1/e`, `Δ'' < 0`, both endpoint limits (PAPER5 §2) |
| A2 | the carried kernel's `s_sat = 2.5396`, `C = 0.64761` (PAPER5 Table 1, §7) |
| A3 | Gauss's law ⇒ `J g_φ = g_N`, exactly, in sympy |
| A4 | `Σ_∥ = J + 2Y dJ/dY = 1/Δ'` as an identity in an **arbitrary** `Δ` |
| A5 | all five suprema of PAPER5 Table 1 to the quoted digits |
| A6 | the stiffness sign change at 0.6321 and 2.5396 (PAPER5 §7) |
| A7 | the g03d gates from their own constants; Saturn's phantom mass is the binding one |
| B2 | every scanned kernel is in fact strictly increasing (analytic derivative, not float differences) |
| B4 | the anti-rig: PAPER5's own unsaturated partner screens and fails **only** monotonicity |
| C2 | `κ₃ = (1/3) dΣ_∥/dg_φ` as a polynomial identity in a generic `W` |
| C3 | `g_* = 3a₀Δ'²/|Δ''|`, exact, arbitrary `Δ` |
| C6 | `g_* = [3p/(p+1)](C a₀ − g_φ)` for a power-law approach, to 1e-12 |
| C7 | the whole chain rebuilt from `W'(Y) = J/2` at 60 digits, agreeing to 1e-18 |
| D1 | the closed form `[(p+1)/3](M_p/M☉)(r_p/R_p)²` against the direct computation |
| D4b | `p_max` robust to two decades of strong-coupling convention (spread 0.35) |
| D4c | `p_max` independent of the evaluation radius over 100× (spread 7e-8) |
| D6 | exactly one Table 1 kernel is admissible as written, and it is the simple μ |

## Scope — not done here

The strong-coupling amplitude carries the usual O(1) convention ambiguity; only its parametric
dependence and the D4b sensitivity are load-bearing. The ξ operator's contribution is treated at the
level of the argument shift `Y → Y + ξ²(∇V)²` for a single mode of wavenumber `k`, not a solved
Solar-System profile — the same approximation PAPER5 §11 uses for the `α₁` drag. Metric-mediated
scalar self-interactions are omitted (they are `1/M_pl`-suppressed without the `1/Δ'` enhancement, so
the decoupling limit gives the *lowest* `g_*`). The search for an admissible `C²` continuation of the
carried kernel past `s_sat` is **L30's lane** and is deliberately not attempted here. The claim that
`Σ_∥ < 0` is fatal rather than merely awkward is the paper's own hypothesis H2, inherited and not
re-derived; if a covariant completion existed in which the longitudinal mode is healthy at
`dg_N/dg_φ < 0`, the whole pincer of §2 would reopen and PAPER5's own theorem would fall with it.
