# A causal variational worldline action for modified inertia: the rapidity gap

**Carl P. Zimmerman**
Briar Creek Tech

---

## Abstract

Modified-inertia (MI) realisations of the MOND phenomenology require an inertial mass that depends
on the magnitude of the proper acceleration, |a| — a non-analytic function of the acceleration
squared. No polynomial-in-velocity worldline self-interaction can produce it. We prove this as a
parity theorem: because Minkowski space admits only the rank-2 metric and the rank-4 Levi-Civita
tensor as invariants, every polynomial scalar built from four-velocities at several proper times has
even degree in u and therefore contributes only even powers of the orbital speed, whereas the deep
MOND limit requires the first power. We then exhibit the unique escape class. The square root of the
velocity bilinear is exactly the **rapidity gap** between the velocities at two proper times,
√(−u·u′/c² − 1) = √2 sinh(θ/2) with cosh θ = −u·u′/c², and it is linear in the speed; its
short-separation limit is θ(s) → |a|s/c, because proper acceleration is the rate at which rapidity
accumulates. A retarded kernel smearing of θ therefore delivers |a| with no (v/c) suppression.

With the minimal causal kernel K(s) = (N/λ)e^(−s/λ) the model reduces, on circular worldlines, to the
closed form Θ = (4Nv/c)·x·coth(π/x)/(4+x²) with x = λΩ, and the circular-orbit equation of motion is
g_bar = μ(g_obs/a₀)·g_obs — Milgrom's modified-inertia relation exactly, with μ = 1 + F. Demanding
the interpolation exponent that solar-system ephemerides require (α ≥ 1.4; α = 1 is excluded) gives
F in closed form. The construction is causal, variational in the in-in sense, free of Ostrogradsky
instability, and Lorentz-invariant up to the preferred frame that MI already presupposes.

We identify and repair its worst defect. In a single-factor worldline action the same function
multiplies the rest energy and the inertia, so μ → 0 in the deep limit forces the rest energy to
vanish. We prove this is structural — every ∫dτ W(Θ) term locks the two at a ratio independent of W
— and repair it with a two-function form built on the preferred-frame four-velocity, in two variants
with explicitly different costs. Both give rest energy exactly mc² and inertia exactly mμ. Both
predict that the associated preferred-frame coupling scales as g⁻², so the Lorentz violation is
largest in the lowest-acceleration environments and ~10⁻²³ in a terrestrial laboratory.

We are explicit about what is not achieved: the acceleration scale is not derived. The kernel's first
moment must satisfy M₁ = c/a₀, and in the short-memory limit only that moment survives — verified
across three kernel shapes — so one number is traded for one number. **The coefficient of a₀ remains
fitted, not derived.**

---

## 1. Introduction and prior art

MOND phenomenology is organised by a single acceleration scale a₀ ≈ 1.2 × 10⁻¹⁰ m s⁻² and an
interpolating function between the Newtonian and deep regimes. Two realisations are distinguished:
modified gravity (MG), in which the field equations change, and modified inertia (MI), in which the
particle's inertial response changes. This paper is about MI.

**Credit, stated up front and without hedging.** The interpolating kernel used throughout,
ν(y) = √(1 + 1/y) with y = g_bar/a₀, is *identically* Milgrom's kernel — M. Milgrom, *Phys. Lett. A*
**253** (1999) 273, equations 6–9 — obtained there from a de Sitter–Unruh temperature balance
T = √(a² + Λc²/3)/2π, with the coefficient fixed to â₀ = 2cH_Λ. His equations 10–11 give a second
coefficient, and Milgrom 2008 §7.3.1 records that the mismatch between them "isn't necessarily
meaningful." The scale a_λ = c²√(Λ/3) is Milgrom, *Ann. Phys.* **229** (1994) 384. The temperature
√(a² + Λ/3)/2π is Narnhofer, Peter and Thirring, *IJMPB* **10** (1996) 1507. Nothing in the kernel
is new here.

What is new here is the *action*: a causal, variational worldline functional whose equation of motion
is the MI relation, together with the theorem that identifies which structure can produce it.

**What is not claimed.** This paper does not derive a₀, does not derive its coefficient, and makes no
claim about unification or the Standard Model. Section 8 states precisely which single number is
fitted and why the construction cannot fix it.

---

## 2. The obstruction: a parity theorem

Consider a worldline x^μ(τ) with u^μ = dx^μ/dτ, u·u = −c². A nonlocal self-interaction built from
velocities at several proper times is a candidate for an MI action. Take first the bilinear form.

On an exact circular worldline of speed v and coordinate angular velocity Ω, writing γ = (1−v²/c²)^(−1/2),

> **(1)**  u(τ)·u(τ+s) = −γ²c²[1 − (v²/c²)cos(γΩs)]

which is independent of τ and depends on the trajectory only through v and γΩ. Consequently, smearing
with any kernel K(s) returns a constant plus (v²/c²) × (a function of γΩ). But the quantity MOND needs
is the proper acceleration magnitude,

> **(2)**  |a| = γ²Ωv,

which is **first** order in v. The mismatch is exactly one power of v; in amplitude it is (c/v)², which
for galactic speeds of 50–300 km s⁻¹ is 10⁶–3.6 × 10⁷. This reproduces, from power counting alone, the
suppression factor found by direct computation in the modified-inertia programme.

Higher polynomial order does not help, and this is a theorem rather than a survey:

> **Theorem 1 (parity).** Minkowski space admits exactly two invariant tensors, the metric η (rank 2)
> and the Levi-Civita tensor ε (rank 4), both of **even** rank. Every polynomial scalar constructed
> from four-velocities at any number of proper times therefore has even total degree in u, and on a
> circular worldline contributes only **even** powers of v. No polynomial-in-u worldline
> self-interaction, at any degree, can produce the deep-MOND v¹ scaling.

There is no rank-1 or rank-3 invariant, so an odd-degree scalar self-interaction does not exist to be
attempted. Direct check: the quartic (−u·u′/c² − 1)² has short-separation limit |a|⁴s⁴/4c⁴ — degree
four in v, moving further from the target.

---

## 3. The escape: the rapidity gap

Theorem 1 bans polynomials. It does not ban non-analytic functions of the bilinear, and there is a
canonical one. From (1),

> **(3)**  −u·u′/c² − 1 = 2γ²(v²/c²)sin²(γΩs/2)

so that

> **(4)**  √(−u·u′/c² − 1) = √2 · γ(v/c) · |sin(γΩs/2)|

which is **first** degree in v. Geometrically, since cosh θ = −u·u′/c² defines the hyperbolic angle
(rapidity gap) between two unit timelike vectors, and cosh θ − 1 = 2 sinh²(θ/2),

> **(5)**  √(−u·u′/c² − 1) = √2 sinh(θ/2)     exactly.

θ is a Lorentz scalar. Its short-separation behaviour is the point of the construction:

> **(6)**  θ(s)/s → |a|/c,   √(−u·u′/c² − 1)/s → |a|/(√2 c)   as s → 0.

The first of these is the classical statement that **proper acceleration is the rate at which rapidity
accumulates along a worldline**. So |a| appears linearly, with no (v/c) suppression. The proposed
action is a functional of the accumulated rapidity:

> **(7)**  S = −mc² ∫dτ √(1 − v²/c²) [1 + F(Θ)],   Θ(τ) = ∫₀^∞ ds K(s) θ(τ, τ−s)

with the kernel supported on s > 0 only, so the construction is **causal** by fiat. Only u = dx/dτ
appears, at several proper times: there is no second or third derivative of x anywhere, hence **no
Ostrogradsky instability**. With a retarded kernel this is precisely the nonlocal worldline class for
which the in-in (Schwinger–Keldysh) functional is variational, so (7) is variational in that sense.

---

## 4. A kernel, and the closed form

θ(s) is **periodic** in s with period 2π/(γΩ) and bounded above by twice the rapidity, 2 arctanh(v/c).
It behaves as |a|s only for s ≪ 1/Ω. Which regime obtains is therefore the whole content of the model.

Take the minimal causal one-scale kernel K(s) = (N/λ)e^(−s/λ). Using
∫₀^∞ e^(−ps)|sin ks| ds = k(p²+k²)^(−1) coth(πp/2k), the non-relativistic reduction is exact:

> **(8)**  Θ(v, Ω) = (4N v/c) · x coth(π/x) / (4 + x²),   x ≡ λΩ

(verified against numerical quadrature to 20 digits at x = 0.05, 1, 20). Its two limits are qualitatively
different:

- **Short memory, x ≪ 1:** Θ → M₁|a|/c with M₁ ≡ ∫K(s)s ds = Nλ. Setting **M₁ = c/a₀** makes
  Θ = |a|/a₀ *exactly* — the MOND variable itself, with no residual factor.
- **Long memory, x ≫ 1:** Θ → (4N/π)(v/c), a function of **speed**, with Ω absent.

---

## 5. The equation of motion

Non-relativistically (7) expands to L ≃ −mc²[1+F] + ½m[1+F]v² − mΦ, so the inertial mass is
m_eff = m[1 + F(Θ)]. For a circular orbit |a| is constant, so the acceleration dependence contributes
no additional radial force, and the radial balance m_eff g_obs = m g_bar gives

> **(9)**  g_bar = [1 + F(g_obs/a₀)] · g_obs ,   μ ≡ 1 + F,   ν ≡ 1/μ

which is Milgrom's modified-inertia relation exactly.

The long-memory branch is excluded **structurally**, not by data. A kinetic function of speed alone,
L = m f(v) − mΦ, gives circular-orbit balance g_bar = g_obs f′(v)/v; matching the deep limit
g_obs = √(g_bar a₀) then requires f′(v) = v³/(r a₀), which depends on r at fixed v. No such f exists.
The model must therefore live in the short-memory regime, and this is a constraint on λ, not a choice.

**Solving for F.** Solar-system ephemerides bound a constant anomalous radial acceleration. In the
α-family ν_α(y) = (1 + y^(−α))^(1/2α), equivalently g_obs^(2α) = g_bar^(2α) + a₀^α g_bar^α, the
Newtonian-limit anomaly is Δ = a₀^α g_bar^(1−α)/(2α). At α = 1 this is the *constant* Δ = a₀/2, which
exceeds the bound by ~10³; the bound requires α ≥ 1.38 before, and ≥ 1.25 after, the external-field
effect. Taking α = 2 and inverting g_obs⁴ = g_bar⁴ + a₀²g_bar², with Y ≡ g_obs/a₀:

> **(10)**  μ₂(Y) = √( (−1 + √(1 + 4Y⁴)) / 2 ) / Y,   F(Y) = μ₂(Y) − 1

This is monotone, tends to 1 as Y → ∞ (Newtonian recovery, F → 0) and to Y as Y → 0 (deep MOND,
m_eff → m|a|/a₀). At α = 2 the anomaly is Δ = a₀²/4g_bar = 3.7 × 10⁻¹⁹ m s⁻² at Earth, below the bound
by five orders. The reproduction of ν₂ is exact by construction, so (10) is a **consistency** result —
a solution F exists — not a prediction of the shape.

---

## 6. The rest-energy defect, and its repair

Equation (10) has F(0) = −1. In (7) the same factor multiplies rest energy and inertia, so the rest
energy mc²[1+F] **vanishes** at zero acceleration. This is not a bad choice of F:

> **Theorem 2.** Any reparametrisation-invariant worldline term ∫dτ W(Θ) expands to
> ∫dt W(1 − v²/2c²), so its rest-energy and inertia contributions are locked at a ratio **independent
> of W**. No single function can separate them.

The repair requires a second structure that is not of the form ∫dτ × (scalar). MI already supplies
one: inertia in MI is defined relative to a preferred frame — the cosmological / de Sitter rest frame
— with unit timelike four-velocity n, n·n = −c², so u·n = −γc². Two independent structures follow.

**Form I (quadratic in u·n, CPT-even).**

> **(11)**  S = −mc² ∫dτ A(Θ) + (m/c²) ∫dτ B(Θ) (u·n)²

gives rest energy mc²(A − B) and inertial mass m(A + B) — two independent combinations. Imposing
unmodified rest energy and MI inertia,

> **(12)**  A = (1 + μ)/2,   B = (μ − 1)/2

so the rest energy is exactly mc² for every Θ while the inertia is exactly mμ(Θ). B → 0 as μ → 1: the
added structure switches itself off in the Newtonian limit. The exact energy is
E = mc²[Aγ + B(2v²/c² − 1)γ³], which becomes negative above

> **(13)**  v_crit² = 2c²/(3 − μ)

i.e. 0.8165 c in the deep limit, rising to c as μ → 1, so the instability exists only in the MOND
regime. The fastest systems to which MOND is applied (clusters, ~10³ km s⁻¹) lie a factor 240 below
this threshold. It is a relativistic/UV defect, quantified, not a galactic one.

**Form II (linear in u·n).**

> **(14)**  S = −mc² ∫dτ μ(Θ) − ∫dτ (u·n)[μ(Θ) − 1]

also gives rest energy exactly mc² and inertia exactly mμ, with exact energy

> **(15)**  E = mc²[1 + μ(γ − 1)]

which is monotone in γ and bounded below by mc² at every speed: no instability anywhere. Its cost is
different: a term linear in u contracted with a background vector is an SME a^μ-type structure, hence
**CPT-odd**. A full Standard-Model-Extension analysis of (14) is owed and is not attempted here; §7
records its magnitude so that (14) cannot be quoted as clean. (Consistency note: Theorem 1 implies an
odd-degree-in-u scalar requires an external vector, which is exactly what (14) uses.)

---

## 7. A prediction: g⁻² preferred-frame coupling

For the α = 2 kernel, μ₂ = 1 − a₀²/4g² + O(g⁻⁴), so the strength of the preferred-frame term in
either form is

> **(16)**  |B| = (1 − μ)/2 ≃ a₀²/(8g²)

Evaluated with a₀ = 9.36 × 10⁻¹¹ m s⁻²: 1.1 × 10⁻²³ in a terrestrial laboratory (g = 9.81),
3.1 × 10⁻¹⁷ at Earth's orbital acceleration, 2.6 × 10⁻¹³ at Saturn's, and of order unity only in the
outer disc of a galaxy. The g⁻² scaling is exact to numerical precision.

This is a falsifiable statement, and a distinctive one: it is the **opposite** of a constant SME
background. The violation is largest where no Lorentz test exists and smallest where the tests are
tightest. A search that bins Lorentz-violation limits by the local gravitational acceleration would
test it directly. It is not confronted with data here.

---

## 8. What is not derived

The kernel's first moment must satisfy M₁ = c/a₀. Numerically this is M₁ = 3.20 × 10¹⁸ s ≈ 101 Gyr,
which on the pure-Λ footing equals Z/H_Λ with Z = 2√(8π/3), because a₀ = cH_Λ/Z on that footing.

In the short-memory limit **only** M₁ survives: three different kernel shapes (exponential, gamma-2,
box) normalised to the same first moment give the same Θ to eight digits. The shape is invisible; one
number has been traded for one number. This is the same reparametrisation already known to afflict the
temperature-functional class, in which the crossover is a₀/(cH_Λ) = 2/r with r a free ratio of two
slopes of the generating function.

Additionally, the short-memory condition x = λΩ ≪ 1 must hold wherever the acceleration-dependent
relation is applied. The tightest such system is Mercury: x ≤ 0.1 forces **λ ≤ 1.2 × 10⁵ s ≈ 1.4 days**
and hence a kernel weight N = (c/a₀)/λ ≥ 2.6 × 10¹³. A galaxy-scale λ is excluded outright: at
λ = 35 Myr, Earth falls in the long-memory branch with Θ = 0.37, a tens-of-percent inertia shift. So λ
is a new constant of the construction with a hard upper bound, not a free dial.

**Therefore: the coefficient relating a₀ to Λ is fitted, not derived.** On the pure-Λ footing the
relation a₀ = ½c√(Gρ_Λ) = c²√(Λ/32π) is an input to this construction, and the rational ½ has no
derivation here. The author has previously and publicly retracted broader claims; none are made here.

---

## 9. Summary and open problems

Established: a parity theorem excluding all polynomial-in-u worldline self-interactions (Theorem 2 in
the text numbering above is the rest-energy theorem; the parity result is Theorem 1); the rapidity gap
as the unique escape class; a closed-form reduction of a causal one-scale kernel; the MI equation of
motion; the α = 2 interpolation in closed form; a structural exclusion of the speed-dependent branch;
and the two-function repair of the rest-energy defect with both costs priced.

Open:

1. **Non-circular orbits.** The reduction of §5 holds |a| constant. General orbits require the full
   in-in treatment and are not solved here.
2. **The SME analysis of Form II.** Its CPT-odd structure must be confronted with matter-sector
   bounds. Form I avoids the issue at the price of (13).
3. **Quantisation.** The |s| in (4) means the action admits no local derivative expansion, so there is
   no effective-field-theory power counting and no controlled quantum completion by that route. This is
   the flip side of the feature: |a| is precisely the non-analytic object MOND requires.
4. **The coefficient.** M₁ = c/a₀ remains an input.

---

## Reproducibility

Every quantitative claim above is generated by a committed, runnable script that exits non-zero on any
failed check and includes negative controls that must trip:

| Script | Checks | Content |
|---|---|---|
| `mi_nonquadratic_u_escape_2026.py` | 30/30 | parity theorem; the rapidity-gap identities (3)–(6) |
| `mi_rapidity_kernel_solved_2026.py` | 35/35 | closed form (8); the EOM (9); F in closed form (10); λ bound |
| `mi_two_function_restmass_fix_2026.py` | 35/35 | Theorem 2; Forms I and II; (12)–(16) |
| `mi_ephemeris_and_action_pincer_2026.py` | 38/38 | the α-family anomaly Δ; the α ≥ 1.4 bound |
| `mi_ctp_variational_2026.py` | 50/50 | the in-in variational property of the retarded class |
| `mi_crossover_master_formula_2026.py` | 14/14 | the a₀/(cH_Λ) = 2/r reparametrisation |

## References

- M. Milgrom, *Phys. Lett. A* **253** (1999) 273 — the kernel ν = √(1+1/y), eqs 6–9; â₀ = 2cH_Λ.
- M. Milgrom, *Ann. Phys.* **229** (1994) 384 — a_λ = c²√(Λ/3).
- M. Milgrom, *Acta Phys. Polon. B* **32** (2001) 3613; and §7.3.1 of the 2008 review — coefficient mismatch.
- H. Narnhofer, I. Peter, W. Thirring, *IJMPB* **10** (1996) 1507 — the temperature √(a²+Λ/3)/2π.
- S. Deser, O. Levin, *Class. Quantum Grav.* **14** (1997) L163 — five-acceleration interpretation.
- J. L. Synge, *Relativity: The Special Theory* — Frenet–Serret for accelerated worldlines; rapidity.
- M. Ostrogradsky (1850) — the higher-derivative instability avoided by (7).
- D. Colladay, V. A. Kostelecký, *Phys. Rev. D* **55** (1997) 6760; **58** (1998) 116002 — the SME.
- V. A. Kostelecký, *Phys. Rev. D* **69** (2004) 105009 — gravitational SME.
- A. Fienga et al. (2011), INPOP10a — supplementary perihelion advances.
- C. Skordis, T. Złośnik, *Phys. Rev. Lett.* **127** (2021) 161302 — AeST, the MG comparison class.

---

*License: CC-BY-4.0. Prepared with computational assistance; all claims are script-backed and the
scripts are included in this deposit.*
