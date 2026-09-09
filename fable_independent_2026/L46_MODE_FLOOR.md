# L46 — the mode floor: the count is right, two of the speeds are not

2026-09-09. Lane L46 of [CHARTER.md](CHARTER.md).
Script: [L46_mode_floor.py](L46_mode_floor.py) → [L46_mode_floor.out](L46_mode_floor.out).
**59 checks, 59 PASS / 0 FAIL; exit 0.**

Nothing under `closure_2026/` or any other agent's directory was imported, executed or copied. The
quadratic actions, the Dirac algorithm, the constraint algebra and every dispersion relation were built
from scratch in sympy in this file, in exact rational arithmetic. Ten controls guard the machinery.

---

## The verdict, first

**The deposited count of four is right.** An independently built Dirac constraint analysis — one that
computes the constraints instead of being handed them — returns 4 for the assembled action, at every
parameter point tested, including the theory's own exhibited point on the closure locus.

**Four is not the floor. Three is reachable, and three is the floor.** Setting `K₂ = 0` makes the MOND
scalar auxiliary, produces a genuine second-class pair, and returns exactly 3 — with the static MOND
limit, Φ = Ψ, the PPN parameters and the Cassini bound *literally* unchanged, because K₂ occurs in one
entry of one of the three quadratic forms. Three is also the floor implied by the foliation theorem
itself: khronometric theory is the minimal covariant carrier of a preferred foliation and it has 3.
Two is reachable only by the non-covariant A1 construction that L12 already killed.

**But the lane found something bigger than the integer.** The paper's two scalar speeds, σ = 1.679 and
c²_s,mix = (2−K_B)²/(c₁₄|K₂|), are **not the eigenvalues of the coupled scalar sector**. Their *sum* is
the larger eigenvalue. The smaller one is

    c²₋ = (2 − K_B)[2 J_Y − (2 − K_B)] / (4|K₂|)
        = +2.14 × 10⁻⁶ (canonical, J_Y = 3.217)   +1.68 × 10⁻⁶ (alt, J_Y = 2.726)

i.e. a sound speed of **1.46 × 10⁻³ c / 1.30 × 10⁻³ c**, not 1.68 c. Two gate rows the paper marks PASS
are evaluated on a quantity that is not a mode speed, and the sector carries a health condition the gate
table does not contain. Both are reported below. **Neither row's verdict flips at the exhibited point** —
they are right for reasons the paper does not give.

---

## 1. The counter, and why it is not L31's arithmetic

L31's controls C1–C4 evaluate `dof(phase_dim, n_first, n_second)` on **hand-supplied** integers:
`dof(12,4,0) == 2`, `dof(18,4,0) == 5`. That is an assertion about general relativity, not a computation.

Here the algorithm runs. For each theory the quadratic Lagrangian is built from the action about flat
space for one Fourier mode with **k** along z (even-z-index components on cos kz, odd on sin kz, so the
z-average is exact). Then:

1. the velocity Hessian W is computed and its **null vectors are** the primary constraints;
2. the canonical Hamiltonian is built with the Moore–Penrose pseudo-inverse on the primary surface;
3. Dirac's consistency algorithm is iterated to closure — every constraint here is linear in phase
   space, so all mutual brackets are constants and the algorithm is exact linear algebra;
4. first and second class are separated by the **rank of A J Aᵀ**, not by inspection;
5. `N = (2N_q − n_2nd − 2 n_1st)/2`.

### The mandatory controls

| theory | N_q | primary | secondary | 1st class | 2nd class | **DOF** |
|---|---|---|---|---|---|---|
| ADM general relativity | 10 | 4 | 4 | 8 | 0 | **2** ✓ |
| GR + one minimally coupled scalar | 11 | 4 | 4 | 8 | 0 | **3** ✓ |
| Einstein-aether (c₁…c₄ = 1/5, 1/7, 1/11, 1/13) | 13 | 4 | 4 | 8 | 0 | **5** ✓ |
| khronometric (same c's, u hypersurface-orthogonal) | 11 | 4 | 4 | 8 | 0 | **3** ✓ |

k-independent (checked at k = 1, 2, 3). The machinery *sees* why khronometric loses two modes relative to
Einstein-aether: its vector sector carries no mode at all (C10), because u_i is a gradient.

### A second control layer: the speeds

A degeneracy count can be right while the coefficients are wrong, so the same Lagrangians are made to
reproduce the published closed-form speeds, at three random rational parameter points each. Dispersion
relations are extracted **without gauge fixing** — gauge invariance makes det D vanish identically, so
the physical relation is taken as the gcd of the r × r minors at the generic rank r. This matters: the
usual shortcut of setting a variable to zero by gauge silently discards a Lagrange multiplier's
constraint, and that is exactly where a mode count goes wrong.

| control | result |
|---|---|
| tensor | c²_T = 1/(1 − c₁₃) — Jacobson ✓ |
| spin-1 | [c₁ − (c₁²−c₃²)/2]/[c₁₄(1−c₁₃)] — Jacobson ✓ |
| spin-0 (æther) | c₁₂₃(2−c₁₄)/[c₁₄(1−c₁₃)(2+c₁₃+3c₂)] — Jacobson ✓ |
| spin-0 (khronometric) | (2−α)(β+λ)/[α(1−β)(2+β+3λ)] — Blas–Pujolas–Sibiryakov ✓ |

The last one settles a caveat the paper leaves open. §3.1 says the identification
σ = (2−c₁₄)c₂/[c₁₄(2+3c₂)] between the construction's design parameter and the khronometric sound speed
is "**stated, not proved**". As khronometric physics it is now derived here, and the assembled action
reproduces σ* = 1.679312732 exactly once φ is switched off (M2b).

---

## 2. The count: four, confirmed

    ASSEMBLED ACTION: N_q = 12, rank(Hessian) = 8, primaries = 4, secondaries = 4,
                      first class = 8, second class = 0  →  DOF = 4

The constraint structure is *identical* to the controls': four first-class primaries (lapse and shift
momenta), four first-class secondaries (the Hamiltonian and momentum constraints), no second-class pair
anywhere. **The extra modes are extra fields, not extra constraints**, and 12 − 8 = 4. Confirmed at 12
parameter points, both signs of K₂, k = 1 and 2, and at the exhibited point
(K_B = 0.2, c₁₄ = 1.978 × 10⁻⁶, c₂ = 3.3217 × 10⁻⁶, |K₂| = 9.754 × 10⁵) on the closure locus — the
closure locus does **not** degenerate the kinetic matrix.

---

## 3. The four modes, named

| # | mode | kinetic normalisation | speed² | couples to |
|---|---|---|---|---|
| 1–2 | **tensor**, two graviton polarisations | the Einstein term | **exactly 1**, as an identity in K_B (c₁ = −c₃ ⇒ c₁₃ ≡ 0) | T_μν |
| 3 | **fast scalar** — mostly the clock (khronon) | c₁₄ k², suppressed 5.1 × 10⁵ vs the graviton | **3.3586** = σ + c²_s,mix | matter only through the metric, at O(c₁₄) |
| 4 | **slow scalar** — mostly the MOND scalar φ | \|K₂\| per Fourier mode; **k-, c₁₄- and ξ-independent** | **+2.14e−6 / +1.68e−6** (canonical/alt) | matter through the AeST coupling 2(2−K_B) a^μ∂_μφ |

Mode 4's kinetic normalisation carries no ξ, which is the reason the coherence operator
ξ²q^{λσ}q^{μν}∇_λV_μ∇_σV_ν is safe: it is purely spatial, so it adds no time derivative and therefore no
Ostrogradsky mode.

The mixing between 3 and 4 is a **velocity–coordinate** (B-matrix) mixing, not a kinetic one. It does not
degenerate the kinetic matrix — hence the count stays 4 — but it rotates the two scalars into each other.

---

## 4. THE CORRECTION — the scalar eigen-speeds, and two gate rows

This is a correction to a paper deposited on 2026-09-08 (DOI 10.5281/zenodo.22667688), reported plainly.

A closed form for the two scalar eigenvalues is obtained by a **second, independent** reduction — unitary
gauge for the khronon (χ = 0) plus h_zz = 0, with the two genuine Lagrange multipliers n and ν_z removed
by a Schur complement — and checked against the gauge-free minor-gcd machinery of PART 0. The two agree
to 9 decimals (S1).

**S2 — the sum rule.** Over three decades of |K₂|, the two eigen-speeds **sum** to σ + c²_s,mix to better
than 1 part in 10⁵:

| |K₂| | Σ(computed eigenvalues) | σ + c²_s,mix |
|---|---|---|
| 9.754e5 (locus) | 3.35864143 | 3.35863549 |
| 9.754e6 | 1.84724560 | 1.84724501 |
| 9.754e4 | 18.47259970 | 18.47254034 |

So the paper's two scalar numbers are the **trace of the speed matrix**, split between the modes, not the
modes themselves. On the closure locus c₂|K₂| = (2−K_B)² the two *unmixed* numbers coincide — degenerate
unmixed levels plus a mixing split maximally, which is why the locus produces one mode at their sum and
one at almost nothing. **The locus does not mean "both scalar modes travel at σ".**

**S3 — an exact health condition the gate table does not contain.** The product of the two scalar ω²
factorises exactly:

    ω²₊ ω²₋  ∝  −c₂ k⁴ (K_B − 2) [ (2 − K_B) − J₁(2 − c₁₄)(1 + ξ²k²) ] / [ K₂ c₁₄ (3c₂ + 2) ]

so with K₂ < 0 (the healthy sign) **both scalar modes have ω² > 0 if and only if**

    J_Y (2 − c₁₄)(1 + ξ²k²)  >  (2 − K_B)          [critical J_Y = 0.9000009]

independent of |K₂| and of the *sign* of the AeST coupling (it enters squared). The combination
J_Y(1 + ξ²k²) versus (2 − K_B) is the same one the theory's own α₁ = −4c₁₄ − 4(2−K_B)/[J_Y(1+ξ²k²)+1]
carries — the structural echo is a strong check on the algebra.

**S4 — it passes at the exhibited point.** The theory's own kernel slope at the Galactic external field is
J_Y = 3.217 (canonical) / 2.726 (alt) — both ≥ 3.0× the threshold. **All four modes are healthy, on both
footings. The deposited health claim survives**, for a reason the paper does not state.

**S5 — but the Cherenkov row's premise is false.** The slow eigen-mode has c₋ = 1.462 × 10⁻³ c
(canonical) / 1.298 × 10⁻³ c (alt). The gate table's Gravitational-Cherenkov row passes on
"clock 29.6% superluminal; the bound constrains **slow** modes" together with the gate `c²_s,mix ≥ 1`.
The spectrum *contains* a slow mode. Whether the bound actually bites depends on that mode's coupling to
matter, which this lane does **not** compute — the claim here is only that the row's stated premise does
not hold and the row needs re-running.

**S6 — where the condition would fail.** J_Y = s/Δ(s) decreases as the acceleration falls. With the
theory's own repaired kernel (C = 0.647610, p = 1.7538, a₂ = 0.9335), J_Y drops below 0.9000 at

    s = g_N/a₀ = 0.3985   →   g_N < 3.731e−11 m s⁻² (canonical) / 4.495e−11 m s⁻² (alt)

**What that does and does not establish.** ESTABLISHED: about flat space, with the MOND function analytic
at the background and slope J₁ = J_Y, the condition is exact, appears in two independent reductions, and
passes on both footings at the theory's own external-field J_Y. **NOT ESTABLISHED**: that the theory is
unstable in the deep-MOND regime. Below s = 0.399 the background gradient of φ is not zero, and an
anisotropic background splits the perturbation into longitudinal and transverse pieces with stiffnesses
J′ and J′ + 2Y₀J″. That calculation — the one `fc_kh_terminal` performed for the khronometric arm — is
what would decide it, and **this lane does not do it**. Reported as an open computation with a named
entry point, not as a kill. ξ does not help there: (ξ/R_Sat)² = 4.7 × 10⁶ at Solar-System gradient scales
(which is exactly why α₁ passes) but ξ²k² ~ 10⁻⁸ at galactic scales.

---

## 5. Is the fourth mode forced? Three routes to three

### (a) φ = f(τ) — let the MOND scalar *be* the clock. **Exact kill.**

n_μ ∝ ∂_μτ and q projects orthogonal to n, so `q_μ^ν ∂_ν τ ≡ 0` — the clock has zero gradient on its own
leaves. Verified exactly on a random curved metric with a random non-trivial τ in rational arithmetic.
Hence V_μ ≡ 0, Y ≡ 0, J(Y) = J(0) = const, and the **entire MOND sector disappears**. This is an
identity; no parameter evades it.

### (b) one scalar, MOND carried by the clock's own acceleration a_μ (khronometric MOND). **Closed for the programme's kernel; not closed in general.**

Mode count 2 + 1 = 3. Not blocked by counting — blocked by the longitudinal stiffness, and this lane
reaches that conclusion **twice, independently**:

- Gate 12's own F_M(y) = 2[(1+y)e^{−y} − 1], differentiated here, gives
  f″(y) = 2α + 2(2−α)(1−y)e^{−y}, which is FC-KH's kill function. At the assembled theory's **own**
  c₁₄ = 1.978e−6, f″ < 0 on 1 < y < 16.57, and sign(c²_par) = sign(f″) is β,λ-independent. For
  M_b = 10¹¹ M_⊙ the unstable shell is **3.00–15.35 kpc (canonical, r_M = 12.20 kpc) / 2.73–13.98 kpc
  (alt, r_M = 11.12 kpc)** — the MOND radius of a normal galaxy, on both footings.
- The assembled theory's **own** bounded-boost identity Σ_∥ = 1/Δ′(s) says the same thing from the other
  end: §4.4's AQUAL arm has Δ = y e^{−y}, which turns over at y = 1.000000 exactly, so Σ_∥ < 0 above it.

**Where it is left open, and this lane says so:** a monotone-Δ AQUAL kernel has Σ_∥ > 0 and escapes the
stiffness argument. It then carries an unscreened constant boost C·a₀ at every acceleration, so it needs
the ξ operator, which in a single-field theory becomes ξ²(D_iD_j ln N)² — a four-spatial-derivative lapse
term. **Not evaluated here.**

### (c) K₂ = 0 — the MOND scalar made auxiliary. **This one works as a count.**

    K_2 = 0: N_q = 12, primaries = 5, first class = 8, second class = 2  →  DOF = 3

An exhibited construction, not an argument that one might exist. The mode is removed by a genuine
second-class pair (p_φ ≈ 0 and its consistency condition); the four diffeos are untouched. K₂ is absent
from B and from C entirely and occupies exactly one entry of W, so the static sector is literally
unchanged. This is the repository's own **CDE-L4C** architecture, recorded in
`FRIED_CHICKEN_HANDOFF_BRIEF.md` as **OPEN / NOT CERTIFIED**.

---

## 6. The price of route (c)

Priced against all 21 gates the theory passes.

| gate | verdict | why |
|---|---|---|
| static MOND, Φ = Ψ, Cassini, Saturn, sunward, α₁, α₂, α₃, γ | **UNCHANGED** | K₂ is absent from B and C |
| tensor speed, bounded boost, BBN, black holes | **UNCHANGED** | no K₂ dependence |
| DOF health | improved | one fewer mode to keep healthy |
| causality / no CTC | passes | instantaneous *on the leaves* is not acausal when the leaves are the causal structure |
| S3's health condition | **UNCHANGED** | route (c) inherits the same threshold J_Y > 0.9000 (R-c6) — the condition is a property of the MOND coupling, not of having a fourth mode |
| gravitational Cherenkov | **worse** | the surviving scalar sits at c² = 4.28e−6, slower still |
| **linear growth (H9)** | **BROKEN** | S_eff = 1 − (2−K_B)²/(c₂\|K₂\|) → −∞; the closure locus cannot be satisfied at all |
| **gate 7: no instantaneous channel** | **BROKEN** | the φ propagator becomes ω-independent; the scalar dispersion drops from degree 4 to 2 in λ. This is the gate's explicitly named wall |
| **clock speed σ = σ\*** | **BROKEN** | eliminating a slaved φ shifts c₁₄ → c₁₄ + O((2−K_B)/J_Y) = O(1), so the surviving scalar falls from σ = 1.679 to **4.28 × 10⁻⁶** |
| Hadamard well-posedness | changed, not priced here | the system becomes mixed hyperbolic–elliptic |

Three readings, in order of honesty:

1. The broken growth gate is **vacuous**. With Q₀ = 0 there is no dark component; the paper's own table
   records "PASS as an equation — and nothing to grow". A gate whose subject does not exist cannot be
   the reason to keep a mode.
2. Gate 7 is the real price — and gate 7's usual consequence is the repository's own **conjecture**:
   "Any claimed universal `N_grav=2 ⇒ α₃=O(1)` pincer is a conjectured obstruction, not a theorem."
3. **The decisive price is σ.** σ* = 1.679312732 is the *single* value at which §3.1's quartic Hadamard
   obstruction has its leading order vanish. Route (c) destroys it. The reduction buys one integer and
   spends the theory's own well-posedness repair.

---

## 7. Requirement or theory — which should give

**The requirement, verbatim** (`hunt_2026/FRIED_CHICKEN_HANDOFF_BRIEF.md`, gate 2):

> Degrees of freedom: N_grav = 2 tensor (+ at most one healthy clock scalar). HONEST FORM (gate 2′):
> every DOF explicit, counted by a Dirac/Hamiltonian analysis, and healthy (no ghost, no gradient
> instability, no tachyon).

and, in the same kill list: *"Clock + second scalar → N = 2+2 (gate 2)."*

**Correction to the gate table (V1).** THE_COMPLETE_THEORY's DOF row reads "Passes the requirement as
written (separately counted and healthy); fails it read as a total". The requirement *as written* allows
2 tensor + **at most one** clock scalar = 3, and names "clock + second scalar" as a kill. The theory
therefore **fails gate 2 as written as well**. It passes **gate 2′**, and the parenthetical should say so.
A description error of the kind L36 catalogued, not a computation error.

**The case for amending the requirement.** The integer exists to exclude ghosts, extra radiation and
Solar-System violation. All four modes here are healthy; c_T = c exactly and structurally; α₁, α₂, α₃, γ
pass. Three, not two, is the floor a covariant realisation of the forced foliation can reach, because a
non-propagating foliation is either background structure or an instantaneous constraint. The only 2-mode
MOND construction in the record (A1) reaches 2 by going non-covariant and L12 killed it — C_M demands
ρ = −1.6 × 10³ kg m⁻³ at 1 AU in *empty* space.

**The case against.** The fourth mode is not decorative and it is not benign. It is what buys Δ′ > 0: a
matter-sourced carrier obeys J_Y(g_φ)g_φ = g_N by Gauss's law, which forces Δ monotone, where the
single-field AQUAL arm turns over at y = 1. It is also where the theory's worst behaviour lives —
Σ_∥ = 9.4 × 10¹⁵ (canonical) / 5.6 × 10¹⁵ (alt) at Saturn, a ~10¹⁰ c longitudinal cone, a strong-coupling
cap p ≤ 1.754, a sound speed of 1.5 × 10⁻³ c, and the unlisted health condition of §4. That is exactly
the kind of object "N_grav = 2" was written to exclude.

**Recommendation.** Amend the requirement to gate 2′, and name the price. Amending costs nothing the
physics gates do not already test; keeping the raw integer would force route (c), which trades a clean
spectrum for an instantaneous channel, an OPEN uncertified architecture, and σ*. The honest cost of the
amendment is that gate 2 stops doing independent work — every reason to want it is already a separate
gate. **PART 2B is the evidence for that: the integer was right and two of the physics rows were not.**

---

## 8. What is open, named

1. **The anisotropic scalar analysis.** Whether S3's condition survives a background with ∇φ ≠ 0, i.e.
   the deep-MOND regime. Entry point: the longitudinal/transverse split with stiffnesses J′ and
   J′ + 2Y₀J″, the calculation `fc_kh_terminal` ran for the khronometric arm. **This decides whether §4
   is a footnote or a kill.**
2. **The slow mode's coupling to matter**, which decides whether the gravitational-Cherenkov bound bites
   at c₋ = 1.5 × 10⁻³ c / 1.3 × 10⁻³ c.
3. **Route (b)'s monotone-Δ escape**: a single-field AQUAL kernel with Σ_∥ > 0, screened by
   ξ²(D_iD_j ln N)². Not evaluated here.
4. **Gate 7's actual consequence.** The `N_grav=2 ⇒ α₃=O(1)` pincer is recorded as conjectured. Until it
   is a theorem, route (c)'s price is a gate violation, not a physical exclusion.

Nothing here is closed. κ = ½ remains fitted, and this file never says otherwise.
