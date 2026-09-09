# L60 — the anisotropic scalar health condition: it is a KILL, in deep MOND, on both footings

**The condition L46 found does not survive. Keeping the background gradient does not rescue it, and the
theory carries a gradient instability throughout the deep-MOND regime — the regime it exists to explain —
on both a₀ footings.** For a spherical M_b = 10¹¹ M_⊙ galaxy some direction is unstable at every radius
beyond **19.3 kpc (canonical) / 17.6 kpc (alt)** and every direction is unstable beyond **38.7 / 35.3 kpc**,
with a fastest e-folding time of **7.6 × 10² years** at λ ≈ 0.7 pc and still **0.74 Myr** at λ = 1 kpc.

2026-09-09. Lane L60 of [CHARTER.md](CHARTER.md), answering the open computation named in
[L46_MODE_FLOOR.md](L46_MODE_FLOOR.md) §8 item 1 and listed in `papers_2026/PAPER8_ERRATA_PENDING.md`.
Script: [L60_anisotropic_health.py](L60_anisotropic_health.py) → [L60_anisotropic_health.out](L60_anisotropic_health.out).
**64 checks, 64 PASS / 0 FAIL; exit 0; runtime 4 s.**

Polarity: each check asserts a **statement** and PASS means the statement is true. V1 passing is the kill.

Nothing under `closure_2026/` or any other agent's directory was imported, executed or copied. The ADM
Einstein–Hilbert Lagrangian, the aether sector, the Dirac constraint algorithm and every dispersion
relation were rebuilt here in sympy in exact rational arithmetic, and fourteen control checks (C0–C10)
guard the machinery before any result is claimed.

---

## 1. The controls, first, because nothing below counts without them

| control | required | got |
|---|---|---|
| C1 ADM general relativity | 2 | **2** (4 primary + 4 secondary, all first class — produced by the algorithm) |
| C2 GR + one minimally coupled scalar | 3 | **3** |
| C3 Einstein-aether (c₁…c₄ = 1/5, 1/7, 1/11, 1/13) | 5 | **5** |
| C4 khronometric (same c's, u hypersurface-orthogonal) | 3 | **3** |
| C6 tensor speed | Jacobson 1/(1−c₁₃) | exact, 3 random rational points |
| C7 spin-1 speed | Jacobson | exact, 3 points |
| C8 spin-0 speed (aether) | Jacobson | exact, 3 points |
| C9 spin-0 speed (khronometric) | Blas–Pujolas–Sibiryakov | exact, 3 points |

And L46's own results reproduce, independently:

| L46 result | reproduced here |
|---|---|
| four propagating modes, 4 primary + 4 secondary, all first class | **R1, R1b, R1c** — 12 − 8 = 4, including at the exhibited point on the closure locus |
| tensor: speed exactly c as an identity in K_B | **R2** |
| clock: kinetic normalisation ∝ c₁₄k² and nothing else | **R3** |
| MOND scalar: kinetic normalisation \|K₂\|, k-, c₁₄- and ξ-independent | **R4** |
| the exact factorisation of ω²₊ω²₋ | **R7** |
| critical J_Y = (2−K_B)/(2−c₁₄) = 0.9000009 | **R8** |
| slow-mode speed c²₋ = +2.14 × 10⁻⁶ / +1.68 × 10⁻⁶ | **R9** (computed 2.1379e−6 / 1.6848e−6) |
| the critical acceleration s = 0.3985 | **R10** |

---

## 2. What the calculation is

L46 linearised about **flat space**, so ∇φ̄ = 0, and said so. Below s = 0.3985 the background gradient is
not zero, it picks out a direction, and the perturbation problem is anisotropic. Expanding J(Y) about
V̄ = ∇φ̄ ≠ 0 (A1, derived by series expansion in three dimensions with a general background direction):

    J(Y)⁽²⁾  =  J_Y |∇δφ|²  +  2 J_YY (V̄·∇δφ)²

which for a plane wave at angle θ to V̄ is `k²[Σ_⊥ sin²θ + Σ_∥ cos²θ]` with the repository's **own** pair,
verified symbolically for an arbitrary kernel from Gauss's law alone (A2) and numerically over sixteen
decades on the theory's own repaired kernel (A3):

    Σ_⊥ = J_Y = s/Δ(s)                  Σ_∥ = J_Y + 2 Y J_YY = 1/Δ′(s)

### The step that makes it tractable, and why it is legitimate

In the action's units (16πG = 1) φ is dimensionless like the metric perturbation, so **B ≡ |∇φ̄| = g_φ/c²
is an inverse length** — of order a₀/c² ≈ 10⁻²⁷ m⁻¹, i.e. 1/(30 Gpc). Every term of the aether and AeST
sectors carries exactly two derivatives, so a term with m of them on the background carries B^m k^{2−m}
and is suppressed by (B/k)^m. Over every regime, both footings and every wavelength from 1 pc to 1 kpc,
**B/k never exceeds 4 × 10⁻⁹** (B1).

The one exception is the J(Y) nonlinearity, because J_YY ~ 1/Y supplies the compensating scale: 2Y J_YY =
Σ_∥ − Σ_⊥ is dimensionless and O(1) (B2, = 0.5413 at s = 0.1). **So the anisotropic splitting of the
stiffness is the only O(1) effect of the background gradient, and everything else is a 10⁻⁹ correction.**
The quadratic Lagrangian is therefore L46's with two *independent* stiffnesses — J_eff(θ) on the Y term and
Σ_⊥ on the ξ term, the latter because ξ²q^{λσ}q^{μν}∇_λV_μ∇_σV_ν reduces to (∂_i∂_jδφ)², which is isotropic
and has vanishing background value (B3).

That two-stiffness Lagrangian is then run through the **same** machinery, and the gauge-free minor-gcd and
the unitary-gauge Schur reduction still agree to 10⁻⁹ with the two stiffnesses different (D2).

---

## 3. The answer

    (2 − c₁₄)[ Σ_⊥ sin²θ + Σ_∥ cos²θ + Σ_⊥ ξ²k² ]  >  (2 − K_B)

**Σ_∥ ≥ Σ_⊥ everywhere on the theory's own kernel** — the ratio is Δ/(sΔ′) = 1/(dlnΔ/dlns) and its minimum
over sixteen decades is **2.000** (A4). So the **transverse** branch is the soft one, and in that branch
J_eff = J_Y **exactly** — which is L46's flat-background stiffness.

> **D4. Keeping the background gradient makes the condition BETTER along ∇φ and leaves it EXACTLY
> UNCHANGED across ∇φ. The worst direction is unchanged.**

The flat-background approximation was neither optimistic nor pessimistic. It was **exact on the softest
branch**, and the gradient it dropped only helps a direction that was never the binding one.

| branch | threshold | fails below |
|---|---|---|
| transverse (θ = 90°) | Σ_⊥ = J_Y > 0.9000009 | **s = 0.3985** — L46's number, unchanged |
| longitudinal (θ = 0) | Σ_∥ = 1/Δ′ > 0.9000009 | **s = 0.0994** |

Between the two thresholds only a cone of directions is unstable; below the lower one all of them are
(D5). At s = 0.1 the unstable cone already covers **99.6%** of directions.

### It fails where the theory works and nowhere else

| regime | s | Σ_⊥ | Σ_∥ | transverse | longitudinal |
|---|---|---|---|---|---|
| deep MOND, outer disc | 0.03 | 0.1835 | 0.400 | **FAIL** | **FAIL** |
| deep MOND, outskirts | 0.10 | 0.3628 | 0.904 | **FAIL** | PASS |
| transition edge | 0.40 | 0.9024 | 3.30 | PASS | PASS |
| transition | 1.00 | 1.845 | 11.07 | PASS | PASS |
| Solar System (Saturn) | 7.0e5 / 5.8e5 | 1.08e6 / 8.9e5 | 9.6e15 / 5.8e15 | PASS | PASS |
| saturated branch | 1e8 | 1.54e8 | 8.4e21 | PASS | PASS |

**The saturated branch and the Solar System are the safest places in the theory, not the most dangerous**
(F2, F3). The failure is confined to deep MOND and is total there.

### There is no parameter escape

- **K_B (F4).** The threshold is (2−K_B)/(2−c₁₄), and BBN caps K_B ≤ 0.25, so it cannot be pushed below
  **0.875** anywhere in the admissible window. To within that 12.5%, since J_Y = s/Δ = g_N/g_φ exactly,
  **the condition IS the statement g_φ ≤ g_N — the MOND boost must not exceed the Newtonian field.** The
  theory is healthy only where MOND is not operating.
- **ξ (F6).** ξ enters as Σ_⊥ξ²k² and so stabilises only the short-wavelength end. Lifting even a 10 kpc
  mode over the threshold at s = 0.1 would need ξ ≈ **1.94 kpc**, about 2 × 10⁴ times the theorem-forced
  floor of 0.10 pc and comparable to the galaxy it is supposed to sit inside — and ξ is bounded from
  *above* by the Solar-System gates.
- **The §4.4 fork (F5).** On the theory's own alternative AQUAL kernel Δ = y e^{−y}, Σ_⊥ = e^y ≥ 1 passes
  everywhere but Σ_∥ = 1/[(1−y)e^{−y}] is **negative for every y > 1** — the transition region, the inner
  disc and the whole Solar System (−7.39 at y = 2, −37.1 at y = 5). The carrier arm fails below s = 0.3985
  *across* the gradient; the AQUAL arm fails above y = 1 *along* it. **No acceleration is healthy on both
  branches of both arms.**

---

## 4. Pricing it: not a ghost, not ill-posed — a gradient instability

**Not a ghost (G1).** All three kinetic normalisations are positive and **none of them depends on J at
all**: the graviton's is the Einstein term, the clock's is c₁₄k² = 1.978e−6 k², the MOND scalar's is
\|K₂\| = 9.754e5. No background acceleration can flip one.

**Not a loss of hyperbolicity (G7).** Above k_up the ξ operator restores ω² > 0, so the growth rate is
bounded and the initial-value problem stays well posed. *The theory is well posed and unstable, which is
the worse of the two diagnoses:* an ill-posed problem can be blamed on a missing operator; a well-posed
instability is a prediction.

**It is a gradient (Laplacian) instability**, ω² = c²₋k² with c²₋ < 0, at the rate:

| footing | s | λ (fastest) | e-fold time | e-folds / 10 Gyr |
|---|---|---|---|---|
| canonical | 0.03 | 0.450 pc | **4.06e2 yr** | 2.5e7 |
| canonical | 0.10 | 0.730 pc | **7.62e2 yr** | 1.3e7 |
| alt | 0.03 | 0.674 pc | **6.09e2 yr** | 1.6e7 |
| alt | 0.10 | 1.095 pc | **1.14e3 yr** | 8.8e6 |

**Not a short-wavelength artefact (G4).** At λ = 1 kpc, where kL = 63 for a 10 kpc background and B/k =
1.4 × 10⁻⁹, the e-folding time is still **0.74 Myr** and the mode grows by **1.4 × 10⁴ e-folds over 10 Gyr**,
on both footings. **And the neglected terms cannot save it (G4b):** the Jeans-type mass the WKB reduction
drops is the square of the galactic dynamical frequency, and γ² exceeds it by **4.7 × 10²** even at λ = 1 kpc,
rising to 4.7 × 10⁶ at 10 pc.

### The region, for a real galaxy, both footings

M_b = 10¹¹ M_⊙, spherical — the same model L46 used for its route-(b) shell.

| footing | r_M | some direction unstable | every direction unstable |
|---|---|---|---|
| canonical | 12.20 kpc | **r > 19.33 kpc** | **r > 38.70 kpc** |
| alt | 11.12 kpc | **r > 17.61 kpc** | **r > 35.26 kpc** |

**G6. A finite region does not regulate a wrong-sign gradient term — and here the region is not even
finite.** The unstable wavelength is ~0.7 pc against a region that starts at 19 kpc and never ends:
2.7 × 10⁴ fastest-growing wavelengths fit inside the first 19 kpc of it alone, and the band spans 0.5 pc
upward. L46's route-(b) kill had a bounded 3.00–15.35 kpc shell; **this one does not close.** HI rotation
curves are measured flat well past both radii.

---

## 5. The independent third route, and the disagreement it settles

The dispersion routes share one machinery, so the threshold was re-derived with none of it. Set every
time derivative to zero, take a static configuration (zero shift, χ = 0, h_zz gauged away), and the whole
static scalar sector is a **3 × 3 matrix**:

           n        hT      δφ
    n  [  c₁₄      1/2    2−K_B   ]
    hT [  1/2      1/8      0     ]
    δφ [ 2−K_B      0   −(2−K_B)J ]

- `C[n,hT] = 1/2` — the Hamiltonian constraint: the lapse multiplies the spatial curvature
- `C[n,φ] = 2−K_B` — the AeST coupling 2(2−K_B)a^μ∂_μφ, **through the lapse**
- Eliminating hT, the lapse's own effective stiffness is `c₁₄ − (1/2)²/(1/8) = c₁₄ − 2` — **dominated by
  the −2 the Einstein constraint supplies, not by c₁₄.** That is why the threshold carries a 2 and why
  c₁₄, six orders of magnitude smaller, is irrelevant to it.
- Eliminating the lapse feeds (2−K_B)² back into δφ's stiffness with the wrong sign, giving

      C_eff  =  (2−K_B)[ (2−K_B) − (2−c₁₄)J ] / (2−c₁₄)

**E1: it changes sign at exactly J = (2−K_B)/(2−c₁₄).** Three routes — gauge-free minor-gcd, unitary-gauge
Schur, and a static energy functional that uses no dynamics at all — one number.

Stated narrowly (E2): what is claimed from the static route is the **location** of the sign change and the
**channel** that produces it, not a standalone stability criterion — the static metric trace carries the
usual conformal-factor indefiniteness. Both match the dispersion route exactly.

---

## 6. Reconciliation with the lanes that found the sector healthy

Four results in this repository would have had to see this. None of them could, and each reason is
checked rather than waved away.

1. **The deposited gate table's "DOF health: PASS" (H1).** It evaluates the scalar sector at the theory's
   own external-field slope J_Y = 3.217 / 2.726, which is **s = 1.899** — the solar-neighbourhood
   acceleration, a factor 3.6 above the threshold and a factor 4.8 in acceleration above where the
   condition fails. **The row is right where it is evaluated. It was never evaluated in deep MOND.**
2. **L46 itself.** It found the condition and stated in its own words that the deep-MOND regime was not
   established because the gradient was dropped. This lane keeps the gradient; the threshold survives
   verbatim on the transverse branch.
3. **L13's coupled (khronon, MOND scalar) system found "Σ > 0" and nothing more (E3, H2, H2b).** Its
   hand-written 2×2 model carries the AeST mixing as `2(2−K_B)k²χ̇δφ` — coupling δφ to the **khronon only**.
   Its product of the two ω² is `c₂(2−K_B)Σ/(c₁₄K₂)`, reproduced here symbolically, and it is positive for
   **every** Σ > 0, with no threshold anywhere. The (2−K_B)² subtraction comes from the **lapse** channel,
   which that model does not carry. And its single test point J_Y = 1.0 sits 11% above the threshold
   0.9000, on the healthy side, where the omission cannot show. **The disagreement resolves in L46's
   favour, and the reason is named.**
4. **L30 and L53 found the saturated branch well posed** — a strictly convex variational inequality with a
   unique, Lipschitz-stable solution (H3). That is a statement about the **static** operator
   ∇·[J_Y∇φ] = 4πGρ, whose ellipticity needs only Σ_⊥ > 0 and Σ_∥ > 0. Both **are** positive here; they are
   merely *small*. A static elliptic solve never forms the coupled (metric, khronon, φ) quadratic form and
   cannot see a threshold that lives in the mixing. And the branch they studied is the **saturated** one,
   where J_Y = s/C diverges and the condition passes by four decades and more. **They are right about a
   different operator in a different regime; there is no contradiction to resolve.**

**H4.** The one place this could have been an error in this lane's own setup — an instability contradicting
a passing lane — is closed by the static route, which shares no machinery with the dispersion routes and
makes no dynamical assumption, and lands on the same threshold.

---

## 7. Verdict, in three sentences

**It is a kill, and it is a kill in the regime the theory exists to explain.** Keeping the background
gradient — the calculation L46 named and did not do — improves the longitudinal branch by a factor of four
in acceleration and leaves the transverse branch exactly where the flat-background calculation put it, so
the deposited scalar sector carries a gradient instability at every acceleration below 0.4 a₀, growing in
760 years at 0.7 pc and 0.74 Myr at 1 kpc, throughout an unbounded region beyond 19 kpc in a normal
galaxy, on both a₀ footings, with no escape through K_B, ξ, or the theory's own §4.4 kernel fork. The
erratum item is discharged in the direction that costs the deposited paper most: the condition must be
**listed** and it must be reported as **failing**, and the honest one-line statement of it is that — to
within the 12.5% that K_B can buy — the theory's scalar sector is healthy only where g_φ ≤ g_N, i.e. only
where MOND is not operating.

---

## 8. What is open, named

1. **The nonlinear endpoint.** An unstable linear mode says the background is not the endpoint; it does
   not say what is. Whether the instability saturates into a modified but viable configuration, or
   destroys the MOND phenomenology, is not computed here.
2. **Wavelengths comparable to the background scale.** The WKB reduction is controlled by B/k ≤ 10⁻⁷ and
   by kL ≫ 1; it is not a statement about λ ≳ 10 kpc. The instability does not need those modes — it is
   already catastrophic at 1 kpc — but the claim is bounded.
3. **Whether an operator exists that repairs it.** The subtraction is generated by the AeST coupling
   through the Einstein constraint, which is what *sources* the MOND scalar with matter. Removing the
   subtraction and keeping the sourcing is not obviously possible, but it is not shown here to be
   impossible.
4. **L46's other two open items** — the slow mode's coupling to matter (the Cherenkov row), and route
   (b)'s monotone-Δ escape — are untouched by this lane.

κ = ½ remains fitted, and this file never says otherwise. Nothing here is closed.
