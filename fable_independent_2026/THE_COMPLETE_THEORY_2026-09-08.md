# The theory, written down

**2026-09-08.** Script: [`L43_assemble_theory.py`](L43_assemble_theory.py) → [`L43_assemble_theory.out`](L43_assemble_theory.out)
(exit 0; 4 non-control FAIL lines, every one of them a result). Written to be read by a physicist who has
not seen this repository.

---

## 0. The headline, first

**The parameter space is non-empty.** After eighteen months in which no single point satisfied every
constraint at once, there is now a region, and an explicit point inside it that passes eleven independent
gates on both of the framework's acceleration footings. The point is exhibited in §5 and every gate is
tabulated in §6.

**What that region buys is a complete relativistic theory of gravity for the Solar System and for
galaxies, and nothing above a galaxy.** Cassini, the Saturn phantom-mass bound, the sunward-acceleration
bound, α₁, α₂, α₃, γ, the tensor speed, the mode count and its health, Hadamard well-posedness, causality,
black holes, rotation curves and the lensing/dynamics slip — all pass, at one point, on both footings.
Clusters, ultra-diffuse galaxies, binary galaxies, the CMB and S₈ all fail, and they fail for one reason:
the price of curing the theory's single fatal instability was deleting its only dark component.

Stated the way it should be quoted:

> **A complete theory of gravity that works everywhere except above a galaxy, where it is short by a
> factor of 1.49–1.99 in mass at R₅₀₀ — in lensing and in dynamics alike — with a 9σ error in the shape
> of ΔΣ, and where its own hard acceleration ceiling is exceeded by 5.2× at 40 kpc in cluster cores.**

Nothing here is closed. κ = ½ is **fitted**, not derived, and this document never says otherwise.

---

## 1. The structural decision, and the theorem behind it

For a long time the extra propagating scalar in this class of theories was treated as a defect to be
engineered away. Two results say it cannot be, and the theory is therefore built **on** a preferred
foliation with a healthy clock mode, stated as a consequence rather than apologised for.

**Theorem (Lorentz invariance XOR two modes).** Under four hypotheses — (i) the static weak-field limit is
Milgrom's equation, (ii) one metric, minimally coupled to matter, (iii) exactly two propagating
gravitational modes, (iv) **locality** — a distinguished timelike vector field u is forced; adding the
elliptic boundary-value posing of Milgrom's equation, Frobenius makes it hypersurface-orthogonal, i.e. a
foliation. Verified against a seventeen-theory control table (GR, Brans–Dicke, f(R), TeVeS, Einstein-aether,
khronometric, Hořava, AeST, …): **no row has both Lorentz invariance and exactly two modes**, and no
counterexample was found. Controls return the right mode counts 2/3/3/5 for GR, GR+scalar, khronometric and
Einstein-aether. 53/53 checks pass. `L31_foliation_nogo.py`.

**Companion theorem.** No foliation-independent scalar can replace the slice-built field, on four
independent counts. Fourteen candidates were tested on a *three-member* slicing family of vacuum
Schwarzschild (static / tilted / Painlevé–Gullstrand) — a two-slicing test would have passed two of the
losers by coincidence. Seven candidates die on slice-dependence alone. The decisive count (T3) is
field-independent: on a homogeneous slice every spatial scalar is constant, so μ(0) = 0 forces ρ = 0
against the measured 2.688 × 10⁻²⁷ kg m⁻³. That kills the *structure*, not a choice within it.
`L27_foliation_scalar.py`.

**The one escape, named and left open.** Hypothesis (iv), locality, is not proved. Temporal nonlocality is a
genuine escape: holding the external field fixed and pushing the source 1000× further away drops every local
curvature invariant by 1000× while |∇(□⁻¹R)| is exactly constant. Deciding it requires a definitive
Hamiltonian mode count for retarded-nonlocal gravity, which is being done elsewhere and is **not** claimed
here. **If that escape opens, the foliation below is a choice, not a theorem.** Everything else in this
document is unaffected.

Consequence: the theory has **four** propagating modes — two tensor, one clock, one MOND scalar — not two.
All four are healthy. That is recorded as a cost against the programme's own "N_grav = 2" requirement in
§6, not hidden.

---

## 2. The action

Fields: a metric g_μν; a clock scalar τ, with unit normal n_μ = −∂_μτ/√(−g^{αβ}∂_ατ∂_βτ) and spatial
projector q_μν = g_μν + n_μn_ν; a MOND scalar φ, with Q = n^μ∂_μφ, V_μ = q_μ^ν∂_νφ, Y = V·V. Matter is
**minimally coupled to g_μν** — one metric, no disformal or conformal factor on the matter sector.

    S = ∫d⁴x √−g {  (1/16πG)[R − 2Λ]
                  − c₁(∇_μn_ν)(∇^μn^ν) − c₂(∇·n)² − c₃(∇_μn_ν)(∇^νn^μ) + c₄(n·∇n)²
                  + 2(2 − K_B) J^μ ∂_μφ
                  − K(Q)
                  − (2 − K_B) J( Y + ξ² q^{λσ}q^{μν} ∇_λV_μ ∇_σV_ν )  }
        + S_m[g, ψ_m],          J^μ ≡ n^ν∇_νn^μ

Line by line:

| term | what it is | what it does |
|---|---|---|
| (1/16πG)(R − 2Λ) | Einstein–Hilbert with a cosmological constant | the metric sector is **exactly Einstein** on the operative branch (DeWitt λ = 1 identically, first-class Hamiltonian constraint) |
| c₁…c₄ | the aether/khronometric kinetic sector, with **c₁ = −c₃ = K_B** so c₁₃ = 0 identically | c₁₃ = 0 makes c_T = c *exactly*, at every K_B — GW170817 is satisfied structurally, not by tuning |
| 2(2 − K_B) J^μ∂_μφ | the AeST coupling of the scalar gradient to the clock's 4-acceleration | **this is what sources the MOND scalar with matter**: statically ∇·J = ∇²Ψ |
| K(Q) | the clock-direction kinetic function of the MOND scalar, K(Q) = K₂Q² | sets the scalar's time-kinetic stiffness. **Q₀ = 0: there is no condensate** (§3) |
| J(Y + ξ²\|∇⊥V\|²) | the MOND function of the *spatial* gradient, plus the coherence (healing-length) operator | J gives Milgrom's law; ξ screens the Solar System. Both are forced, neither is chosen (§4) |

With c₁₃ = 0 and hypersurface-orthogonal n, the clock sector **is** khronometric theory with α = c₁₄,
λ = c₂, β = 0.

**The static weak-field limit is Milgrom's equation at the action's own a₀, with coefficient exactly
1.000000 and no slip.** Independently re-derived: the clock's auxiliary equation
d/dc[(1−c)a² − a₀²U(c)] = 0 with U′(c) = −ln²(1−c) solves to u² = 1 − e^{−|a|/a₀} *exactly* on the static
branch (not as a weak-field approximation), giving

    ∇·[ μ(|∇Φ|/a₀) ∇Φ ] = 4πG_N ρ_b,     Φ = Ψ,     G_dyn = G_lens = G_tensor.

Φ = Ψ to better than 10⁻⁴ out to 1 Mpc, so lensing and dynamics share one potential — the framework's
lensing requirement, met structurally rather than fitted. `L11_galactic_limit.py`; re-derived from scratch
in `L43_assemble_theory.py` checks K4/K4b.

---

## 3. The parameters, with the constraint that fixes each

Both footings are carried on every dimensional number: **a₀ = 9.3619 × 10⁻¹¹ m s⁻² (canonical) and
1.1279 × 10⁻¹⁰ m s⁻² (alt)**.

| parameter | admissible window | what fixes it | script |
|---|---|---|---|
| K_B (= c₁ = −c₃) | 0 < K_B ≤ 0.25 | BBN on the cosmological Newton constant | `route2`, `g03e` B1 |
| c₁₃ = c₁ + c₃ | **0 exactly** | c_T = c (GW170817). Identically zero by K_B − K_B | structural |
| c₁₄ = c₁ + c₄ | **≤ 1.98 × 10⁻⁶** | see the tightening below | `L13`, `L26`, this script |
| c₂ (khronometric λ) | fixed by σ: c₂ = 2σc₁₄/(2 − c₁₄ − 3σc₁₄) ≈ σc₁₄ | the clock's own speed | `L26`, this script |
| σ = clock speed² | **[1.6793, 1.7716)**, with σ\* = 1.679312732 | see below | `L26_sigma_above_one.py` |
| \|K₂\| | on the closure locus c₂\|K₂\| = (2 − K_B)² | linear growth ∧ Cherenkov | `g03t` D5/D7, `g03v` |
| ξ (coherence length) | **≥ 0.10 pc canonical / 0.15 pc alt — theorem-forced** | §4 | `L34`, `g03d`, `g03z` |
| p (saturation exponent) | **0 < p ≤ 1.754** | perturbativity of the cubic action at a planet | `L34_boost_vs_cubic.py` |
| Q₀ (condensate rate) | **0 — the condensate is removed** | see below | `L14`, this script |
| a₀ | 9.3619e-11 / 1.1279e-10 | measurement, two footings | — |
| κ in a₀ = κc√(Gρ_Λ) | **0.4998 canonical / 0.6023 alt — FITTED** | nothing. See §7 H-C | `L32_kappa_necessary.py` |

### 3.1 σ, and why it is above 1

The construction that generates the clock sector carries a design parameter σ — the clock mode's squared
speed — declared over (0, 1] in its own documentation. That declaration turns out to be an **undefended
convention**: it appears once in prose, is copied ten more times, and no `assert`, `if`, `while` or `raise`
anywhere in the construction mentions σ. The only executable restriction is σ > 0.

There is exactly one value of σ at which the construction's quartic obstruction — which otherwise produces
a Hadamard-ill-posed growth rate rising like k² — has its leading order vanish:

    σ* = 4T/(4T − 27) = 3/a*,   T = −27/16 + 54/(5 ln(9/5)) = 16.6865133026,   a* = 3 − 81/(4T)
    σ* = 1.679312732187113        (a clock 29.6% superluminal)

At σ\* the obstruction's leading order is zero *and the sign of the residual reverses on all 59 tested
branch points*, so the real growth rate becomes a bounded oscillation: **the ill-posedness is removed, not
reduced**. All fourteen of the construction's own health conditions hold there — no ghost (the coefficient
is exactly σ-free), positive mode energy, A₀ = 0.4615 > 0, c_T² = 1 as a σ-identity, hyperbolicity, an
unmoved constraint fold, an unchanged det M\*. The **only** internal ceiling anywhere in the family is
J_T > 0, which is exactly affine in σ and vanishes at σ = 1.7716; σ\* sits 5.49% below it. So the
admissible set is a *window*, [1.6793, 1.7716), not a tuned point.

Superluminality is not a problem here and this is worth stating clearly, because it is usually assumed to
be one:

- **Causality.** The clock mode's acoustic metric is G^{μν} = g^{μν} + (1 − 1/σ)n^μn^ν, so
  G^{μν}n_μn_ν = −1/σ < 0 for every σ > 0. The clock's own leaves are spacelike for **both** cones, so τ is
  a global time function for both and no closed causal curve can be built. This is available to *this*
  theory specifically, because the acoustic metric is built from the same foliation the theory already
  varies.
- **Gravitational Cherenkov.** The 2 × 10⁻¹⁵ bound is a **lower** bound: it constrains modes *slower* than
  an ultra-high-energy cosmic ray, because that is what a ray can radiate into. A 29.6% superluminal mode
  switches the channel off. (Independently, the bound's applicability to a conformally coupled k-essence
  clock loosens by 7.2 × 10⁵× even for subluminal modes, and vanishes entirely once the high-acceleration
  limit is applied in the cosmic ray's own near field.)
- **Black holes.** The universal horizon at r = 3M/2 is reproduced; even an infinite-speed mode is trapped.

**A new consequence, derived in the assembly.** Tying c₂ to c₁₄ through σ makes the preferred-frame PPN
parameter

    α₂ ≈ (c₁₄/2)(1/σ − 1) = −0.2023 c₁₄  at σ = σ*

so the Solar-System bound |α₂| < 4 × 10⁻⁷ forces **c₁₄ ≤ 1.978 × 10⁻⁶** — twelve times tighter than the
bound α₁ = −4c₁₄ imposes on its own (2.5 × 10⁻⁵), and six times tighter than a previous global grid scan
found (1.18 × 10⁻⁵). The three bounds are **nested, not in conflict**: three lanes, different machinery,
same corner.

*Caveat, stated:* the identification σ = (2 − c₁₄)c₂/[c₁₄(2 + 3c₂)] between the construction's design
parameter and the khronometric sound speed is **stated, not proved** — the mapping from the construction's
variables to (c₁₄, c₂, |K₂|) is not determined by its published files. The non-emptiness of the parameter
region does **not** depend on it (§5); only the *sharpness* of the c₁₄ bound does.

### 3.2 Q₀ = 0: the condensate is removed, and why that is the right move

A previous global sweep over 1.2 × 10⁸ grid points per footing, with ten gates each reproducing its own
source script's published verdict as a control, found **no admissible point at all**. The obstruction was
exactly two gates deep, and *every* minimal incompatible subset contained the same gate: the clock tachyon.
The condensate's background contributes a positive gradient term for the clock's time shift, giving a
k-independent instability with rate² = |K₂|Q₀²ε₀a⁻³/c₁₄ — about 280 H₀ today, 2.8 × 10⁵ H₀ at z = 100.
Stability needs c₁₄ ≥ 3Ω_d/Ω_m = 2.533; PPN needs c₁₄ ≤ 2.5 × 10⁻⁵. A 10⁵× gap.

The escape is not parametric, it is structural, and it is free: **the condensate cannot be the dark sector
anyway.** Freeing its amplitude to cure the tachyon caps its dark fraction at 2.6 × 10⁻⁶ against
Ω_d = 0.266 — short by a factor 10⁵. So the object whose background creates the fatal instability is an
object that was never going to do the job it was introduced for. Setting Q₀ = 0 removes it, and the
tachyon gate is then satisfied **identically**.

**The price is the whole of §7 H-A and H-B.** This is the trade the theory makes, and it should be read as
a trade, not as a repair.

---

## 4. The kernel, and the repair the theorem forces

### 4.1 The bounded-boost theorem

Write the acceleration excess as Δ ≡ (g_obs − g_bar)/a₀. Because the MOND scalar is *sourced by matter*,
Gauss's law on a sphere gives J_Y(g_φ)·g_φ = g_N exactly, with no expansion, so g_φ must be a
single-valued monotone function of g_N. Writing g_φ = a₀Δ(s), s = g_N/a₀, the longitudinal stiffness is
exactly Σ_∥ = 1/Δ′(s) — an identity, verified symbolically for arbitrary Δ.

Since Δ is bounded for every kernel of the class, **there is a hard ceiling on the acceleration excess,
with no free parameter**:

| kernel | ceiling C = sup Δ |
|---|---|
| deep-MOND √ | 0.250 |
| standard μ | 0.300 |
| exponential carrier, y e^{−y} | 1/e = 0.367879 |
| **ν_RAR (the operative kernel)** | **0.647610**, at s = 2.5396 |
| simple μ | 1.000 |

ΛCDM structurally cannot make this prediction: a halo contributes g_obs − g_bar = g_halo, set by M₂₀₀ and
concentration, which span decades and are not tied to a₀. **One system above the ceiling, with a
trustworthy baryon model, falsifies the kernel with no fitting freedom.** Currently 99.23% of 2352 SPARC
points beyond 2 kpc obey the widest bound at both footings; the eighteen >3σ exceptions lie in five named
galaxies, thirteen of them in NGC 5985 alone, and are kept and reported rather than cut.

### 4.2 The corollary that forces ξ, and the repair that fixes the published kernel

Monotonicity makes sup Δ = lim Δ, so **the Solar-System residual is at least as large as the galactic
boost.** Against the binding Solar-System gate — the Pitjev–Pitjeva bound of 6.7 × 10⁻¹¹ M_⊙ of phantom
mass inside Saturn's orbit, i.e. 4.329 × 10⁻¹⁵ m s⁻² — the bare kernel is over by

    1.4005 × 10⁴×  (canonical)      1.6873 × 10⁴×  (alt)

and never by less than 6.49 × 10³× for *any* kernel in the class. **No kernel of the class can screen the
Solar System.** The coherence length ξ is therefore a theorem, not a design choice. At ξ = 0.10 pc the
operator's gradient-scale suppression (ξ/R_Sat)² = 4.6 × 10⁶ brings the residual to 3.0 × 10⁻³ of the
bound; at ξ = 0.15 pc (alt) to 1.6 × 10⁻³.

Two further corrections, both made here:

1. **An attained supremum is inadmissible.** The published kernel is ν_RAR up to s = 2.540 and then held
   *flat*. A flat branch has Δ′ = 0, hence Σ_∥ = ∞, hence J(Y) of infinite slope and **no cubic action** at
   any Solar-System background. The supremum must be **approached and never attained**. Of the five kernels
   above, only the simple μ is admissible as printed.
2. **The approach rate is capped.** Perturbativity at a planetary source, with ξ at its floor, caps the
   saturation exponent at **p_max = 1.754** (both footings; robust to ±0.35 over two decades of the O(1)
   strong-coupling convention, and independent of the radius at which the field is evaluated). Exponential
   approach is excluded. This constrains the *rate*, never the ceiling — so there is **no** pincer between
   the bounded boost and the cubic action.

### 4.3 The kernel the theory actually carries

    Δ(s) = C [ 1 − W(u)^{−p} ],      u = √s,      W(u) = 1 + a₁u + a₂u²,      a₁ = 1/(Cp)

with, fitted to the published carried kernel at its own ceiling:

    C = 0.647610   p = 1.7538   a₂ = 0.9335      →  max |Δ log₁₀ g| = 0.0111 dex over s ∈ [10⁻⁴, 10⁴]

Properties, each checked:

- **exact deep-MOND coefficient 1** — Cpa₁ = 1 by construction, so Δ → √s and g → √(g_N a₀) with no stray
  2, ½ or 2π;
- **Δ′ > 0 at every finite s** (minimum 1.15 × 10⁻³³ over twenty decades), so Σ_∥ is finite everywhere and
  the cubic action exists — the property the published kernel fails;
- **the ceiling is approached, never attained**: at 60 digits, C − Δ(10¹⁴) = 2.04 × 10⁻²⁵ > 0, while
  Δ(10¹⁴)/C − 1 is zero to double precision. The bounded-boost prediction and its SPARC test are unchanged;
- **p = 1.7538 ≤ 1.754**, at the cap and not beyond it;
- at Saturn's orbit Σ_∥ = 9.4 × 10¹⁵ (canonical) / 5.6 × 10¹⁵ (alt) — **finite**, where the published
  kernel gives ∞. Large, and the corresponding longitudinal cone is ~10¹⁰c; that is admissible (the clock's
  leaves stay spacelike at any *finite* speed, by the identity above) but it is a real oddity of the class
  and is recorded as one.

The same family fitted to the exponential kernel instead gives C = 1/e, p = 0.844, a₂ = 13.31 and
0.0299 dex.

### 4.4 A fork that is a measurement, not a convention

Two structures are in play and they are **not** the same theory:

- the **carrier** structure of the action above, where the MOND scalar is sourced by matter, Δ(s) is
  monotone, and the boost saturates at C·a₀;
- the **AQUAL** structure of the construction's own static limit, where μ(y) = 1 − e^{−y} acts on the total
  potential and Δ(s) = y e^{−y} *decreases* past s = 0.63.

They agree below s = 0.63 and diverge above it, because a matter-sourced scalar cannot carry a decreasing
Δ. At s = 3 the carrier predicts Δ = 0.648 and AQUAL predicts Δ = 0.136 — **0.066 dex in g**, with a
maximum separation of **0.073 dex** over s ∈ [10⁻⁴, 10⁴], against SPARC's own 0.11–0.13 dex scatter.
Detectable in the aggregate, not point by point. And only the carrier arm needs a coherence length at all:
the AQUAL arm screens the Solar System by itself.

**This fork is unresolved and it is the user's call.** It is also a live documentation conflict: the
programme's frozen recipe names μ(y) = 1 − e^{−y} as *the* kernel while the action document carries ν_RAR.
Until one is amended, any comparison that crosses the two documents is ill-defined.

---

## 5. Is the parameter space non-empty? Yes.

Six free parameters (K_B, c₂, c₁₄, |K₂|, ξ, p), with σ derived and gated. Eleven gates, each taken verbatim
from its source script. 666,082,872 grid points per footing, plus the α₂ = 0 and σ-window loci added
explicitly to the c₂ axis so that no narrow band can be stepped over.

| gate | admitted fraction (canonical / alt) |
|---|---|
| H1 PPN α₁ | 0.387 / 0.387 |
| H2 PPN α₂ | 0.319 / 0.319 |
| H3 tensor c_T = 1 and G_N > 0 | 0.936 / 0.936 |
| H4 BBN | 0.691 / 0.691 |
| H5 Solar-System ξ | 0.571 / 0.429 |
| H6 saturation p ≤ 1.754 | 0.556 / 0.556 |
| H7 clock window σ ∈ [1.6793, 1.7716) | 0.0120 / 0.0120 |
| H8 Cherenkov (no subluminal mode) | 0.410 / 0.410 |
| H9 linear growth | 0.402 / 0.402 |
| H10 scalar kinetic health | 1 / 1 (sign convention) |
| H11 clock tachyon | **1 / 1 — satisfied identically, because Q₀ = 0** |
| **INTERSECTION (all eleven)** | **76,240 / 57,180 points** |

**No subset of the eleven gates up to size four is empty**, on either footing. Compare the previous
answer, reproduced here as a control: with the condensate present, the intersection was **0 points** on
both footings and every minimal incompatible subset contained the clock tachyon.

### The explicit point

    K_B  = 0.2
    c₁₄  = 1.0000 × 10⁻⁶
    σ    = σ* = 1.679312732           (a design choice inside the window, at its lower edge)
    c₂   = 1.679318 × 10⁻⁶            = 2σc₁₄/(2 − c₁₄ − 3σc₁₄), determined by σ
    |K₂| = 1.9294 × 10⁶               = (2 − K_B)²/c₂, exactly on the closure locus
    ξ    = 0.10 pc (canonical) / 0.15 pc (alt)      — at the theorem-forced floor
    p    = 1.7538                     — at the cap
    Q₀   = 0                          — no condensate

    derived:  α₁ = −4.48 × 10⁻⁶ (canonical) / −4.25 × 10⁻⁶ (alt)      bound 10⁻⁴
              α₂ = −2.02 × 10⁻⁷ (both)                                bound 4 × 10⁻⁷ (margin 1.98×)
              α₃ = 0,  γ = 1,  c_T = c exactly
              c_s,mix² = 1.679318,  S_eff = 0.000000
              G_cos/G_N = 0.999997481,   G_N/G = 1.000000500

This point is **derived**, not read off the grid, and then confirmed admitted by all eleven gates on both
footings.

### Two structural results that fell out of the assembly

**(a) The "closure locus" has a meaning.** The relation c₂|K₂| = (2 − K_B)², previously reported as a
tuning that must hold to between 4% and 38%, is *exactly* the locus on which the mixed clock–scalar mode
travels at the clock's own speed: S_eff = 1 − c_s,mix²/σ to leading order in c₁₄ and c₂ (verified to
3 × 10⁻⁶ relative at the exhibited point). It is still a relation between two otherwise-free parameters and
is still reported as a tuning — but it is a *speed-matching* condition, not an arbitrary one.

**(b) A derived ceiling on the theory's own cosmology.** Cherenkov safety (c_s,mix² ≥ 1) together with the
clock window (σ < 1.7716) cap the surviving linear cosmological MOND source at

    S_eff ≤ 1 − 1/σ = 0.4355

so **the action can never deliver more than 44% of its own naive linear source**, whatever the parameters.
This was an input to nothing; it is a consequence.

### Robustness

Two of the eleven gates are conditional. Dropping either only enlarges the region:

| gate set | canonical | alt |
|---|---|---|
| all eleven | 76,240 | 57,180 |
| without H7 (the σ identification, conditional on the unpublished variable map) | 7,567,560 | 5,675,670 |
| without H8 (Cherenkov, which may not apply at all to a conformally coupled clock) | 309,400 | 232,050 |

**The non-emptiness does not rest on either conditional.**

---

## 6. The gate table

Verdicts at the exhibited point, both footings. Full table with sources in
[`L43_assemble_theory.out`](L43_assemble_theory.out) Part V. Tally over both footings: **42 PASS, 18 FAIL,
8 other** (pending / diagnostic / not a discriminant).

| gate | canonical | alt | number |
|---|---|---|---|
| Cassini quadrupole | PASS | PASS | ξ is 3.3× / 3.0× the exact fourth-order solve's own floor |
| Saturn phantom mass | PASS | PASS | bare kernel 1.40e4× / 1.69e4× over; screened to 3.0e-3× / 1.6e-3× |
| Sunward anomaly | PASS | PASS | 1.3e-17 / 7.0e-18 vs bound 3.66e-14 m s⁻² |
| PPN α₁ | PASS | PASS | −4.48e-6 / −4.25e-6 vs 1e-4 |
| PPN α₂ | PASS | PASS | −2.02e-7 vs 4e-7 (margin 1.98×) |
| PPN α₃ | PASS | PASS | 0 exactly |
| PPN γ | PASS | PASS | 1 exactly |
| Tensor speed (GW170817) | PASS | PASS | c₁₃ ≡ 0 ⇒ c_T = c exactly at every K_B |
| Newton constant positivity | PASS | PASS | G_N/G = 1.0000005 |
| **DOF count** | **FAIL vs "N_grav = 2" as a total count** | same | **4** = 2 tensor + 1 clock + 1 scalar. Passes the requirement as written (separately counted and healthy); fails it read as a total |
| DOF health | PASS | PASS | clock A₀ = 0.4615 > 0, positive mode energy, hyperbolic at σ\*; scalar Bogoliubov ω² = c_s²k²(1+ξ²k²) > 0 |
| Hadamard well-posedness | PASS | PASS | S₄ > 0 at 59/59 branch points at σ\*; growth → bounded oscillation |
| Galactic rotation curves | PASS | PASS | MOND at the action's own a₀, coefficient exactly 1.000000 |
| Lensing/dynamics slip (galaxies) | PASS | PASS | Φ = Ψ to <1e-4 out to 1 Mpc |
| Bounded-boost ceiling on SPARC | PASS | PASS | 99.23% of 2352 points; 18 exceptions in 5 named galaxies |
| Kernel tightness vs a fitted halo | **NOT A DISCRIMINANT** | same | 0.142 vs 0.171 dex at zero parameters, but a prior-shrunk NFW reaches 0.085 |
| Gaia DR4 wide binaries | PENDING | PENDING | γ_v ceiling 1.0450 / 1.0300, registered; Arm A band 1.16–1.23 |
| **Clusters: mass at R₅₀₀** | **FAIL** | **FAIL** | required/delivered 1.618 ± 0.022 / 1.493 ± 0.020 (dynamics); 1.987 ± 0.246 / 1.834 ± 0.227 (lensing) |
| **Clusters: bounded-boost ceiling** | **FAIL** | **FAIL** | excess 3.37 a₀ at 40 kpc = 5.2× the ceiling |
| **Clusters: lensing SHAPE** | **FAIL** | **FAIL** | ΔΣ short 2.5–2.7×; log-slope +0.53 ± 0.06 shallower = **9σ** |
| Cluster residual = cosmic share | DIAGNOSTIC | DIAGNOSTIC | required 5.73 ± 0.68 vs Ω_dm/Ω_b = 5.43, universal to 12% |
| **Coma ultra-diffuse galaxies** | **FAIL** | **FAIL** | +1.196 dex (factor 14) at **4.9σ** against the coherent systematic floor |
| **Binary galaxies (2MRS)** | **FAIL alone** | **FAIL alone** | isolated deep-MOND amplitude 1.802 ± 0.041 (19.6σ); 1.141 ± 0.028 with a cosmic share |
| BBN | PASS | PASS | K_B = 0.2 ≤ 0.25; G_cos/G_N − 1 = −2.5e-6 vs 0.13 |
| **CMB acoustic peaks** | **FAIL** | **FAIL** | no dark component in the action once Q₀ = 0 |
| Linear growth | PASS as an equation | same | S_eff = 0 exactly on the closure locus — and nothing to grow |
| **σ₈ / S₈** | **FAIL** (for the late-roll route) | **FAIL** | S₈,eff = 1.06–1.20, +9σ to +34σ |
| Gravitational Cherenkov | PASS | PASS | clock 29.6% superluminal; the bound constrains slow modes |
| Causality / no CTC | PASS | PASS | G^{μν}n_μn_ν = −1/σ < 0 for every σ > 0 |
| Black holes | PASS | PASS | universal horizon r = 3M/2; even an infinite-speed mode trapped |
| Longitudinal cone at Saturn | PASS (repaired) | PASS (repaired) | Σ_∥ = 9.4e15 / 5.6e15 — finite, where the published kernel gives ∞ |
| Strong coupling at a planet | PASS at p ≤ 1.754 | same | δg/g\* = 1520 for Earth without ξ; perturbative with ξ at its floor |
| a₀–Λ tie | **FITTED** | **FITTED** | κ = 0.4998 / 0.6023 |
| **a₀ universality** | **FAIL** | **FAIL** | the ladder spans 0.78 dex across system classes |

Read the table this way: **every row that lives inside a galaxy or the Solar System passes; every row above
a galaxy fails**, and the failures are not independent.

---

## 7. The holes, with sizes

### H-A The cluster deficit — the big one

The residual behaves like **mass** in dynamics *and* in lensing, so no lensing-sector repair can reach it.
Five X-COP clusters with published weak lensing, at each cluster's own R₅₀₀: required/delivered against
hydrostatic mass **1.618 ± 0.022 (canonical) / 1.493 ± 0.020 (alt)**; against weak lensing
**1.987 ± 0.246 / 1.834 ± 0.227**; and the two probes agree with each other
(S_lens − S_dyn = +0.37 ± 0.24, 1.55σ). Four independent lensing teams give 1.623 ± 0.080 / 1.499 ± 0.074,
1.4σ away.

The information dynamics could not give is **shape**. In raw ΔΣ over 0.5–2 Mpc the framework is short by
**2.5–2.7×** and its ΔΣ log-slope is **+0.53 ± 0.06 shallower — a 9σ error** — because its phantom is a
near-uniform sheet. Machinery validated by pushing the *measured* X-ray profile through it, which
reproduces measured ΔΣ to a median 1.11; analytic NFW Σ/ΔΣ to 1.3 × 10⁻⁶. The NFW-refit shape systematic is
0.43, so the quoted shortfall **understates** the disagreement.

And the kernel's own ceiling is violated: the excess is 3.37 a₀ at 40 kpc, **5.2× the operative ceiling**,
so no interpolation function can absorb it. Both escapes are closed quantitatively — non-thermal support
would need σ₁D = 673–1155 km/s against Hitomi/XRISM's 164 ± 10 km/s in Perseus; unseen baryons would need
3.9–5.2× the imaged X-ray gas.

**Every mechanism the programme owns has been closed against it, one at a time:** an interpolation kernel
(clusters need 2.2–5.1× the galaxy boost at the same acceleration, |z| = 13); a fixed-strength finite-range
force (BBN, 41×); a screened force in Φ, ρ or M (100% density overlap at 12.8σ, plus a cosmological
ordering argument); hydrostatic bias (the required b is **negative**, −0.82, against a measured [0, +0.42];
a negative b means σ² < 0 in 12 of 12 clusters); the solenoidal field (real, 14–27% locally inside a merging
pair, but div a_S = 0 forces ⟨a_S·r̂⟩ ≡ 0 at every radius — it closes 3.9% of the gap and runs the wrong
way); a late-time roll of the coupling (gives 0.97 of the required 2.2–5.1 contrast, and cancels exactly
from the growth source in a consistent scalar-tensor model); light thermal relics (Tremaine–Gunn floor
m ≥ 4.67 eV, and an N_eff-vs-RAR pincer with no interior at 27.6 vs 11 eV); wave dark matter (pincer with
no interior, factor 1.4 in mass); four separate condensate constructions; an environment switch.

**And the required ratio is not monotone in scale**, which a scale-free kernel forbids: 1900 isolated 2MRS
major pairs need M_dark/M_bar = **30.9 ± 1.6** within the pair separation against 5.73 ± 0.68 at 0.80 R₅₀₀
— 5.7×, 16σ — and the deficit *grows* with mass at 3.9σ.

**What satisfies all four cluster requirements at once — the mass, the phase-space density, near-absence in
galaxies, and a flat-or-falling enclosed ratio — is a cold, baryon-tracing component. The theory does not
contain one.** That is recorded as a real cost to the modified-gravity programme, not as an open question.

### H-B No dark sector at all, hence no CMB and no structure

Removing the condensate is what cures the clock tachyon, and it was the action's only dark component. Size:
the condensate's dark fraction caps at 2.6 × 10⁻⁶ against Ω_d = 0.266 — short by 10⁵×. With it gone the
theory has baryons only; the CMB third peak, S₈, and the matter power spectrum are unaddressed. The MOND
scalar's own causal growth boost does **not** regenerate P(k) at linear order: σ₈ ≤ 0.65 with a 20–2000×
deficit at k = 0.5–1 h/Mpc, at any |K₂|, on both footings. The one untested route is nonlinear top-down
fragmentation, which a per-mode linear calculation cannot represent.

### H-C κ = ½ is fitted

a₀ = κ c √(Gρ_Λ) is dimensionally forced; κ is not. Recomputed here from Planck's Ω_Λ:
c√(Gρ_Λ) = 1.87251 × 10⁻¹⁰ m s⁻², so **κ = 0.4998 (canonical) and 0.6023 (alt)** — the tie does not even
pick a footing.

Six theorems constrain any derivation. The decisive one: in **any** local action whose MOND function
multiplies √(−g) with a field-independent coefficient, F → F + C adds exactly C√(−g) and is exactly
degenerate with Λ. **κ is a zero mode of the whole class** — verified on four structurally different
Lagrangians, independent of the function, the field count and the coefficient. No curvature polynomial
takes a half-integer power of Λ on de Sitter, so a₀ ∝ √Λ *requires* an order parameter of odd mass
dimension whose square is the vacuum energy; any 4-volume average of a gradient sector is driven to zero in
a Λ-dominated future (10⁻⁸ by 10 t₀), closing the global-constraint class; boundary and Brown–York terms see
only J(0), which the zero-mode theorem already makes pure Λ. Deriving κ reduces to fixing one number,
β/√Z̃ = κ/√2 = 0.354. **A binding guard: 27 simple numbers lie inside the measured 3σ band. Landing in the
band is not evidence — only a derivation is.** And κ is not the discriminating observable: total comparison
uncertainty is 8.0% and nothing in [0.40, 0.66] is rejectable at 3σ.

### H-D The foliation's escape is undecided

See §1. If temporal nonlocality survives a Hamiltonian mode count, the preferred foliation is a choice
rather than a theorem. Being decided in a parallel effort; **not** claimed here either way.

### H-E The variable map is unpublished

c₁₄ has three inconsistent readings in the construction's files spanning 0.073–1.333, and c₂ vanishes at
the state where the mode was measured. The σ ↔ (c₁₄, c₂) identification of §3.1 is therefore stated, not
proved. The region is non-empty with or without it; the sharpness of c₁₄ ≤ 2.0 × 10⁻⁶ is what depends on it.

### H-F c₂ sits five orders below the certified healthy range

The scalar sector's linear health was certified for c₂ ∈ [0.01, 0.1]. The exhibited point has
c₂ = 1.7 × 10⁻⁶. Five orders of untested parameter. Not a computed failure — a gate nobody has run.

### H-G Two documentation conflicts are open

(i) the kernel: the frozen recipe names μ = 1 − e^{−y}, the action document carries ν_RAR; they differ by
up to 0.073 dex and the exponential ceiling is exceeded ~5× more often on the bulgeless SPARC control.
(ii) ξ: the action document's parameter table still quotes 0.03/0.05 pc — the *unsaturated* partner's
floors — against 0.10/0.15 pc for the kernel a scalar can actually carry. One document each needs amending.

### H-H Standing liabilities the assembly does not repair

Coma ultra-diffuse galaxies: the amplitude stands at +1.196 ± 0.062 dex (a factor of 14), but the
significance is **4.9σ, not the 19.4σ once quoted** — the 0.062 dex bar is statistics-only on eleven objects
sharing one M/L scale, one estimator and one cluster model, and the coherent systematic floor is 0.227 dex.
Closing it needs M/L × 14.4. The a₀ ladder spans 0.78 dex across system classes. Unequal-mass wide binaries
carry an open numerical item. Non-spherical accretion and the existence theory of the non-spherical
fourth-order law are untouched.

---

## 8. What is distinctive, with numbers, and what would falsify it

1. **The bounded boost.** g_obs − g_bar ≤ C a₀ = 6.06 × 10⁻¹¹ / 7.30 × 10⁻¹¹ m s⁻², *everywhere, in every
   system, with no free parameter*. ΛCDM cannot make this prediction. **Falsified by one system above the
   ceiling with a trustworthy baryon model.**
2. **a₀(z) — the surviving distinctive prediction.** The deep-MOND baryonic Tully–Fisher zero point is flat
   to <1% out to z = 5 on the derived law, against ΛCDM's +0.33 dex by z = 2.5. **Decisive measurement: a
   deep-MOND lensed rotator at z ≈ 2–2.5 to ±0.13 dex.** This, not κ, is the discriminator.
3. **Gaia DR4 wide binaries — and it is a Newton-like answer.** γ_v ≤ **1.0450** (canonical, ξ = 0.10 pc) /
   **1.0300** (alt, ξ = 0.15 pc), falling toward 1 as ξ grows, against a separately registered band of
   1.16–1.23 and Newton's 1.000. These are **ceilings**: DR4 can kill this arm from above, it cannot
   confirm it over Newton. **A measurement inside 1.16–1.23 falsifies the coherence-length structure.**
4. **The saddle null.** No Bekenstein–Magueijo anomaly at any Solar-System field null — the coherence
   operator erases it by 10⁻²⁹. A LISA-Pathfinder-class saddle flyby detecting one falsifies the operator.
5. **The saturation exponent is bounded above.** p ≤ 1.754: the approach to the ceiling is a power law,
   never exponential. Measuring a faster approach falsifies the perturbative existence of the theory's own
   cubic action.
6. **The carrier/AQUAL fork, priced here for the first time.** 0.073 dex maximum separation, 0.066 dex at
   s = 3. BIG-SPARC's transition bins decide which structure the data prefer — and only the carrier arm
   needs a coherence length at all.
7. **A prediction the removed branch would have made, listed to be honest about what removing it costs.**
   If any component with the scalar's stiffness supplied part of the cluster residual, its peak radius would
   be set by H = 0.42 e c²/(|K₂|a₀) alone and would therefore be **the same physical radius in every
   cluster**, where an NFW scale radius grows as M^{1/3}. The assembled theory has no such component.

---

## 9. Verdict, in three sentences

The admissible region is non-empty, and at an explicit point inside it this is a complete, internally
consistent, Solar-System-safe, galaxy-correct relativistic theory of gravity — one metric, matter minimally
coupled, exactly Einstein in the metric sector, c_T = c exactly, four healthy propagating modes, a preferred
foliation forced by a theorem rather than assumed, and Milgrom's law at the framework's own a₀ with
coefficient exactly 1 and no lensing/dynamics slip.

It is **not** a complete theory of the universe: curing its one fatal instability required deleting its only
dark component, so it is short by a factor of 1.49–1.99 in mass at R₅₀₀ in both lensing and dynamics, wrong
by 9σ in the shape of ΔΣ, over its own hard acceleration ceiling by 5.2× in cluster cores, and silent on
the CMB, S₈ and the matter power spectrum.

What is missing is exactly three things and they should be named that plainly: a cold, baryon-tracing
component that every mechanism this action contains has been shown one by one unable to supply; a
derivation of κ, which a zero-mode theorem proves no local action of this class can give; and a decision on
the locality hypothesis that the foliation theorem rests on.

---

## 10. Reproduction

```
python3 fable_independent_2026/L43_assemble_theory.py
```

Exit 0. Nine controls (K1–K9) rebuild six settled numbers from their own algebra and confront them with the
value printed in the source lane's own `.out`; two more reproduce a known PASS and a known FAIL from
existing gate scripts. Seven kernel checks (N1–N7), thirteen gate-fraction checks, and the admissibility
test (T1, T2) follow. Every control passes. The four FAIL lines — T5, T7, T8, V1 — are results, not machine
errors: the documentation conflicts, the failures above a galaxy, the cluster deficit, and the
incompleteness itself.

Supporting lanes, each with its own script and `.out` in this directory: `L4`, `L8` (verification of the
construction), `L11` (the MOND limit), `L13` (α₁ = −4c₁₄), `L14` (the previous, empty sweep), `L19`
(Cherenkov applicability), `L21` (binary galaxies), `L22` (the curl field), `L23` (Coma UDGs), `L24`
(lensing vs dynamics), `L26` (σ > 1), `L27`/`L31` (the foliation theorems), `L28` (tightness), `L29` (S₈),
`L32` (κ), `L33` (the scalar cone), `L34` (the bounded-boost audit).
