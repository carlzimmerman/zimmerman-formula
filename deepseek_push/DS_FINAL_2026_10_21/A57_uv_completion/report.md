# A57 — THE UV COMPLETION: does one dynamics fix κ AND L★ together?

**Lane:** A57_uv_completion · **Date:** 2026-10-21 · **Base:** `THEORY.md` §§1, 3.4, 7; A33 `MASTER_ACTION.md`;
A15; A28; A20; A2. **Script:** `a57_checks.py` (20/20 PASS, exit 0, 0.6 s) · `a57.out` · `a57_results.json` ·
**Certificate:** `A57_uv_completion.lean` (9 theorems, no `sorry`/`admit`/`axiom`, axioms
`propext, Classical.choice, Quot.sound`) · **Mutations:** `MUTATE.md`, `a57_MUTATE_*.out`.

Notation, fixed once (A37's warning): **κ** = a₀/(c√(Gρ_Λ)); **ℓ₁ = √(8π/Λ) = 15.569 Gpc** the *vacuum cell*;
**L_MOND = c²/a₀ = 31.12 Gpc**; **L★ = √(2γ/K) = 24 pc** the *stiffness* length; **ξ** the medium's *correlation length*
(this lane's "finite ℓ₁" — deliberately not the same glyph); **y = g_N/a₀**; **h(y) ≡ y(ν−1) = u/a₀**;
**y_t = 66.299937**; **F(Y) = ∫₀^∞ h(y)/(1+(y/Y)²)dy**.

## Claim

**No. A medium with a finite number of states per site and a finite correlation length cannot fix both κ and L★, and
the obstruction is exact.** The force law fixes the site capacity to **one occupant per site** (q = 2, capacity =
affinity = a₀; Lean `langmuir_law`, `q3_negative`); the coupling fixes the stiffness, i.e. **L★ and nothing else**,
and *derives* the correlation length (ξ = √(γ/K) = L★/√2 = λ_P), so the "finite ℓ₁" is not an independent handle.
κ never enters the partition function: the energy zero is invariant under H → H + C (Lean `gibbs_shift`), while κ is
a ratio to the absolute vacuum energy. The closure is the one object that could over-determine the system, and it
does not: its convergence comes from the **IR** turn-off y_t = 66.30 (a_t = 6.206×10⁻⁹ m/s² = 11.46 cH_Λ), so a
finite correlation length at any microscopic value changes the integral by 2.4×10⁻⁸. Identifying ξ with the vacuum
cell instead makes the closure **fail by 87.7×**, and the exact truncation bound then forces **κ ≥ 8π = 25.13**,
50.3× the measured ½. The only exact (κ, L★) relation is the identity L★/ℓ₁ = (σ_c/c)²/κ, which *defines* σ_c and so
passes through the measured point by construction; the one closure-derived curve misses it by **7.4 dex**.
**Verdict: two independent UV inputs — the capacity/vacuum-energy zero (κ) and the gradient stiffness (L★); the
completion is a re-parameterisation with one more input than the theory has open numbers.**

## 1. The candidate: q-state lattice, partition function, force law

**1.1** Cubic lattice, spacing a, N sites, q states per site (n_i ∈ {0,…,q−1}), ladder ε(n) = −ε₀n, coupling J:
```
Z(β,μ; q, J) = Σ_{n_i∈{0,…,q−1}} exp[ −β Σ_i ε(n_i) − (βJ/2) Σ_<ij> (n_i−n_j)² + βμ Σ_i n_i ] .             (1)
```

**The two parameters are q (capacity) and J (coupling).** The mean-field saddle (coordination z) gives, with
x ≡ e^{β(μ+ε₀+Jz n̄)},
```
n̄_q(x) = Σ_{k=0}^{q−1} k x^k / Σ_{k=0}^{q−1} x^k .                                                          (2)
```

Following A2's K4 the drive is not a linear Gibbs field: it enters as the **activity** x = g/a₀ (a chemical potential
μ = k_BT ln(g/a₀) − ε₀). Response u ≡ a₀n̄; baryonic field g_N = g − u.

**1.2 The law forces q = 2, exactly.** With capacity C, affinity s (x = g/s, u = C n̄), g_N = g(1 − C/s) + O(g²), so
the deep limit g → √(a₀g_N) requires **C = s exactly, then s = a₀** (A2 K5, symbolic here, K11). With that,
```
q = 2:  n̄ = x/(1+x)  ⇒  g_N = g²/(g+a₀)                                  [exact; Lean `langmuir_law`]      (3)
q = 3:  n̄ = x(1+2x)/(1+x+x²)  ⇒  g_N/a₀ = x²(x−1)/(1+x+x²) < 0, 0 < x < 1  [Lean `q3_identity`,`q3_negative`] (4)
```

For q ≥ 3 the medium **over-responds** (u > g at small g), so g_N < 0: no physical branch. Restoring g_N > 0 needs
C < s, which reintroduces the linear term and destroys MOND. **The exact n = 1 response fixes parameter one: q = 2.**
At x = ½, (4) gives g_N/a₀ = −0.0714 (K10).

**1.3 The stiffness.** (J/2)Σ(n_i−n_j)² → (Jz/4a)∫(∇n)²d³x; with n = u/a₀ and −(γ/2)(D·P)² = −(γ/2K²)(∇u)²,
```
γ = J z K²/(2 a a₀²)   ⇒   L★² = 2γ/K = J z K/(a a₀²)   ⇒   J/a = a₀²L★²/(zK)   (c = 1).                  (5)
```

**The coupling is fixed by L★ and by nothing else** (K12, residual 0). Numerically J = 1.387×10⁶ J at a = ℓ_P
(7.09×10⁻⁴ of ℏc/a) and 8.58×10²⁵ J at a = 1 fm (2.71×10³⁶ of natural): only J/a is physical, so the "UV completion"
is a one-parameter family of continuum limits.

**1.4 The correlation length is not a second parameter.** (5) also fixes the static Green's-function range,
```
ξ = √(γ/K) = L★/√2 = λ_P = 16.97 pc  (L★ = 24 pc),                                                       (6)
```

exactly §3.4's P Compton length. **The medium's finite correlation length *is* the stiffness length.** Of the two
named structures, the finite-state count becomes q = 2 (law) and the finite correlation length becomes L★ (J).
**Neither becomes κ.**

## 2. The closure integral for a finite-capacity medium

**2.1 The integrand is the occupancy.** With ν = g/g_N, h(y) = y(ν−1) = (g_N/a₀)(u/g_N) = **u/a₀ = n̄(g/a₀)**. So h is
not auxiliary: it is the response itself. 0 ≤ h < 1 **is** capacity = a₀ (K3 closed form; Lean `h_lt_one`).

**2.2 Convergence (K4, K20).** A pure finite-capacity medium: ∫₀^∞ h dy **diverges linearly** (F/Y = 0.99989 at
Y = 10⁵). With a finite ξ and no turn-off: Y + ½ − ln(Y+2) + O(1/Y); F(104.70) = 100.531, F(50) = 46.549. With the
turn-off: F(66.299937) = **100.405845** = Λc⁴/a₀² (closed form 100.4495, 4.35×10⁻⁴ high). **A finite-capacity medium
alone has no finite closure integral; a second scale must cut it off — and which scale that is *is* the question.**

**2.3 The truncation bound (exact).** For 0 ≤ h < 1 and any cutoff W ≤ 1 supported below Y, ∫hW ≤ ∫₀^Y h ≤ Y, so
```
F_cut(Y) ≤ Y        [Lean `h_lt_one`; elementary]     and the closure needs F_cut(Y) = 8π/κ²   (7)
⇒   Y ≥ 8π/κ² ,   i.e.   a_max ≥ (8π/κ²) a₀ .                                                            (8)
```

(8) is model-independent: it uses only capacity = a₀ (which the law fixes) and the existence of a cutoff. It converts
any proposed completion into one inequality.

## 3. The sharp question: can a finite ξ satisfy the closure at all?

**3a. If ξ is the vacuum cell: no, exactly.** A medium with correlation length ξ cannot respond above
a_max = c²/ξ (the Rindler surface gravity of a horizon at distance ξ; the factor 2 is immaterial below). With ξ = ℓ₁,
```
Y = a_max/a₀ = c²/(ℓ₁a₀) = L_MOND/ℓ₁ = 1/κ = 2.0                    (κ = ½)                            (9)
F_cut(2) = 1.146733   vs   required 8π/κ² = 100.531      ⇒  87.67× short.                               (10)
```

If the cell length is instead read as the turn-off itself, F = 2.204 — 45.6× short; both readings exclude ξ = ℓ₁.
And (7)+(9) give **κ ≥ 8π = 25.133**, i.e. a₀ ≥ 4.702×10⁻⁹ m/s², **50.23× the measured 9.36×10⁻¹¹** (K5, K6).
Equivalently, a sharp cutoff reaching 8π/κ² needs Y★ = 104.701, i.e. **κ = 0.009551 and a₀ = 1.787×10⁻¹² m/s²,
52.4× low** (K7). No κ near ½ closes the vacuum with a cell-length correlation length. For any
a_max ∈ [c²/(2ξ), 2c²/ξ] the bound is κ ≥ 4π = 12.57 — still 25× above ½, so this is not a convention.

**3b. If ξ is any microscopic length: yes, and the closure is blind to it.** For ξ = λ_P = L★/√2 the cutoff is
Y = 1.834×10⁹ and |F(∞) − F(Y)|/F(∞) = **2.388×10⁻⁸** (K9) — invisible; the convergence is entirely the turn-off's.
In general (8) is satisfied by every **ξ ≤ κℓ₁/(8π) = 309.7 Mpc** at κ = ½ (K8), which any microscopic length
satisfies by more than seven orders.

**3c. Without a turn-off it converges at one tuned value.** F_plain(Y★) = 8π/κ² gives Y★ = 104.701, i.e.
**ξ = 469.4 Mpc = ℓ₁/33.17 = 1.956×10⁷ × L★** (7.29 dex above L★) — a cosmological length, not a UV one.

**Answer.** The closure does **not** require ξ → ∞ or ξ → 0. It requires the cutoff at y_t = 66.30, i.e.
a_t = 6.206×10⁻⁹ m/s² = **11.46 cH_Λ = 9.477 cH₀ ≈ 2Z²a₀** (K16) — an IR scale. A finite correlation length is
compatible with the closure only if it is *not* the vacuum cell; the identification ξ = ℓ₁ is excluded by 87.7× and
by κ ≥ 8π. So a finite-ξ medium can satisfy it, but then ξ is irrelevant and the object that makes it work is a scale
the medium does not own. **No UV completion produces a scale at 11.5 Hubble accelerations**, which is why A28 found
y_t to be κ in disguise: the closure is one equation between two IR numbers.

## 4. Why κ is not a medium property: the shift symmetry

(1) depends on energies only through β(μ+ε₀+Jzn̄) and βJ — energy *differences*. Adding C per site:
```
Z(H+C) = e^{−βNC} Z(H),     every Gibbs weight e^{−βE_i}/Σ_j e^{−βE_j} unchanged   (Lean `gibbs_shift`)    (11)
```

If the vacuum energy is the medium's ground state, ρ_Λc² = ε₀/a³, and ε₀ → ε₀ + Ca³ gives ρ_Λ → ρ_Λ(1+f), f = Ca³/ε₀:
```
κ → κ/√(1+f) ,     while a₀, L★, ξ, h(y) and every response are exactly unchanged.                       (12)
```

K14: f = 1 moves κ from 0.500 to **0.3536** with |Δw| = 0. **κ is therefore not a function of the medium's
parameters**: it is the ratio of the capacity to the *absolute* zero of the energy, and no partition function fixes
an absolute zero. This is A15/k01's J → J + C symmetry lifted to the completion — k01 proved the action class has it;
(11) proves every medium of this class inherits it. The escape is not a better medium but a non-medium principle that
fixes the zero (A15-C1), which is exactly what the theory lacks.

The elastic route fails by a number that *is* the closure: at the saturation strain ∇u = a₀/L★,
u_el = a₀²/(4K) = 2.611×10⁻¹² J/m³ and **ρ_Λc²/u_el = 2Λc⁴/a₀² = 200.81 = 2 × 100.406** (2.303 dex; K15) — the
medium's elastic energy is 201× *below* the vacuum energy, the shortfall being twice the closure number. "The vacuum
energy is the medium's stress" is not an output of (1); it is the identity M1 A15 named as missing.

## 5. The joint prediction: three curves in the (κ, L★) plane

**Curve A — the identity (no content).** κ = ℓ₁/L_MOND and L★ = (σ_c/c)²L_MOND give
```
L★ = (σ_c/c)² ℓ₁ / κ .                                                                                    (14)
```

At κ = ½, σ_c = 8.33 km/s: L★ = **24.040 pc**, on the measured point — but (14) *defines* σ_c = √(a₀L★), so it passes
through the point by construction. Inverting the measurements: σ_c = 8.323 km/s at 24 pc and **16.118 km/s at 90 pc,
1.958× the 10⁴ K width** (K17). After the two measurements (14) has **no freedom left and no predictive power**.

**Curve B — the closure with the medium's own correlation length (a genuine prediction).** ξ = λ_P = L★/√2,
y_t = L_MOND/λ_P = √2ℓ₁/(κL★), so
```
F( √2 ℓ₁/(κ L★) ) = 8π/κ² .                                                                               (15)
```

K18: at κ = ½, (15) gives **L★ = 6.634×10⁸ pc = 663.4 Mpc, 2.76×10⁷ × 24 pc**; at L★ = 24 pc it gives
**κ = 1.744×10⁻⁸, 2.87×10⁷ × below ½**; at L★ = 90 pc the integral is 7.645×10⁶ × the required value. Miss: **7.4 dex**.

**Curve C — the cell identification.** ξ = ℓ₁ gives y_t = 1/κ and no solution below κ = 8π (§3a): empty in the
physical range.

**Answer.** The measured point (0.5, 24–90 pc) lies on Curve A only, and A is an identity that defines σ_c — not a
prediction. The one relation with content, B, misses by 7.4 dex. After the two measurements the relation has **no
freedom left and no content**: the two numbers remain two.

## 6. Parameter count and verdict

| object | status | what fixes it |
|---|---|---|
| site capacity q | **fixed by the law** | q = 2, capacity = affinity = a₀ (§1.2) |
| coupling J | **fixed by L★** | J/a = a₀²L★²/(zK) (§1.3) |
| correlation length ξ | **derived, not independent** | ξ = L★/√2 = λ_P (§1.4) |
| energy zero ε₀ / ρ_Λ | **free, unfixable by (1)** | shift symmetry (11) |

The completion has **two inputs that matter (a₀, J/a) plus the energy zero**, against the theory's **two** open
numbers (κ, L★). The capacity is fixed by the measurement that defines a₀, the coupling by L★, and **κ needs the
third input — precisely the one the partition function cannot see (12).** Count: 3 for 2, one more free parameter
than the theory has open numbers. That is the failure the task asked us to name if it occurred; it occurred.

**Verdict. The theory has two independent UV inputs:**

1. **κ — the vacuum-energy normalisation**, the ratio of the saturation stress a₀²/G to ρ_Λc². In a medium it is the
   absolute zero of the energy functional, unobservable by (11); in the action it is the bare Λ. Not a medium
   parameter, and no finite-state, finite-ξ construction can supply it.
2. **L★ — the gradient stiffness** γ = KL★²/2, equivalently J/a, equivalently the correlation length λ_P. A medium
   *can* supply this one, and §1.3 does.

There is no completion in the tested class that fixes both. The two numbers are two.

## Status

**`NO-GO(obstruction)`** for "one dynamics fixes κ and L★". Sub-results: `DERIVED` — the q = 2 / capacity = affinity
law (§1.2), the stiffness map (5), the bound (7)–(8), the shift invariance (11), all Lean-certified; `NUMERICAL` —
(9)–(10), (13), (14), (15); `NO-GO(exact)` — κ ≥ 8π for ξ = ℓ₁. The missing premise, named exactly: **a principle
that fixes the absolute zero of the medium's energy functional** (A15-C1). It is not a better medium.

## Checks

`a57_checks.py`: 20 checks, deterministic, stdlib + numpy/scipy/sympy, 0.6 s, no network, exit 0 iff all pass.

| id | proves | measured |
|---|---|---|
| K1, K2 | closure reproduces Λc⁴/a₀²; 8π/κ² = 32π = 3Z² | 100.405845 (closed 100.4495); 100.530965 |
| K3 | 0 ≤ h < 1 (response ≤ capacity) | max 0.99999999, exact identity |
| K4 | F_plain(Y) ≤ Y | sup F/Y = 0.98856 |
| K5, K6 | ξ = ℓ₁ ⇒ Y = 1/κ = 2, F = 1.146733; F ≤ Y ⇒ κ ≥ 8π | 87.67× short; 25.1327 (50.265×) |
| K7 | cutoff needed for the closure | Y★ = 104.701, κ = 0.009551, a₀ = 1.787e−12 |
| K8 | ξ ≤ κℓ₁/(8π) | 9.557e24 m = 309.7 Mpc = ℓ₁/50.27 |
| K9 | ξ = λ_P leaves the closure intact | relative change 2.388e−8 |
| K10, K11 | q-ladder over-response; capacity = affinity | g_N/a₀ = −0.0714 at x = ½; 1 − C/s = 0 iff C = s |
| K12, K13 | L★² = JzK/(aa₀²); J contains no κ | exact; ∂J/∂κ = 0 |
| K14 | Gibbs weight invariant under H → H + C | \|Δw\| = 0; κ: 0.500 → 0.3536 |
| K15 | ρ_Λc²/u_el = 2Λc⁴/a₀² | 200.81 (2.303 dex) |
| K16 | turn-off is an IR scale | a_t = 6.206e−9 = 11.460 cH_Λ |
| K17, K18 | identity curve (14); closure curve (15) | 24.040 pc; 663.4 Mpc at κ = ½ (κ = 1.744e−8 at 24 pc) |
| K19 | parameter count | 3 inputs, 2 targets, excess 1 |
| K20 | bare capacity diverges | F(Y)/Y = 0.99989 at Y = 10⁵ |

Mutations (`--mutate`), each exit 1: `kappa1` (K5, K7, K17), `no_turnoff` (K1), `capacity2` (K1, K3, K4, K5, K7, K20),
`q3` (K10), `xi_ell1` (K1). Details in `MUTATE.md`.

## What this does not do

1. **Not a no-go for every completion.** It is a no-go for *finite states per site + finite correlation length*, for
   the exact reason (11): the construction has no access to the absolute zero of energy. A completion that fixes the
   zero non-perturbatively (A15-C1, a global constraint, a topological charge) is outside the class and not excluded.
2. **a_max = c²/ξ is an identification, not a theorem.** It is the Rindler surface gravity at the correlation length,
   and §3a is stable under a factor 2; a medium whose ξ cuts gradients but not accelerations evades §3a and falls into
   §3b, where ξ is irrelevant. Both branches give the same verdict.
3. **The isotherm (2) is mean field, and there is no data fit.** Fluctuations renormalise q = 2 into a crossover but do
   not change the sign of the q = 3 term (4); κ = 0.417 ± 0.095 (CFG493) and L★ ∈ [24, 90] pc (A20) are quoted.
4. **The Lean certificate covers the algebra only** — (3), (4), h < 1, (11), the two length identities, the κ ≥ 8π
   bound. It certifies no integral and no physical premise.

## Next

1. **Attack (11), not the medium.** The one shape that escapes this lane is a functional whose stationarity fixes the
   *absolute* zero of the cold sector's energy against ρ_Λ (A15-C1) — the only object that makes κ a ratio rather
   than a parameter. Everything else in the class is a re-parameterisation.
2. **Turn §3a into a measurement-free theorem.** κ ≥ 8π assumes only capacity = a₀ and a cutoff; if the cutoff is ever
   derived from the medium rather than posited, (8) decides the completion in one line. Empirically, a_t/(cH_Λ) = 11.46
   (13) is a ratio of two IR scales — a few-per-cent RAR determination of the turn-off (A28) measures it, and no UV
   completion can be credited with it.
