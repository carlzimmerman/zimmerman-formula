# The theory, complete

**A self-contained statement: five postulates, everything that follows, and the exact residue.**
Every derived item cites the lane that proves it and the script that checks it. Where a number
was corrected by the adversarial audit (A31) or the clean room (A32), the corrected value is
given. Nothing here is aspirational.

---

## 1. The postulates

**P1 — Geometry.** Gravity is a metric theory with Einstein–Hilbert term `(R − 2Λ_bare)/(4K)`,
`K = 4πG`, on a manifold carrying a preferred foliation (unitary clock gauge `N`, `N^i`).

**P2 — The sector.** A spatial covector `P_i`, with

$$
u=K|P|<a_0,\qquad
W(u)=\frac{a_0^2}{K}\Big[-\frac{u}{a_0}-\ln\Big(1-\frac{u}{a_0}\Big)\Big],
$$

coupled by the clock term `P^i D_i ln N` with coefficient **exactly 1** (any other coefficient
deforms the law: at coefficient 2 the law is off by `0.55 a₀` at `g = a₀/3`), by two gradient
terms `(η/2)E_iE^i` and `−(γ/2)(D_iP^i)² − (γ/4)F_ijF^ij`, and by nothing else — in particular
**no P–curvature coupling**.

**P3 — The vacuum.** `a₀ = κ c √(G ρ_Λ)` on the observed-vacuum footing, with `β` small
(`β < 0.027`, BBN, A78) so that `Λ_bare/Λ_obs ∈ (1, 1.061)`. **κ is an input, not a theorem.** It is
fixed in one of two ways, and the theory does not choose between them:
- **fitted:** `κ = ½`, the record's canonical value (`a₀ = 9.354×10⁻¹¹`);
- **postulated (P-therm, §3.6):** `a₀ ≡ cH_Λ/2π`, which gives `κ = Z/4π = 0.460659` (`a₀ = 8.626×10⁻¹¹`).
  A75 proves P-therm is independent of the action. The relation `2πa₀ ≈ c²(Λ/3)^{1/2}` is Milgrom's
  (arXiv:1605.07458, eq. 5), and the de Sitter Unruh-temperature mechanism behind it is Milgrom 1999
  (astro-ph/9805346).

The data separate the two at 1.35σ (A81, bootstrap error model). See §3.6.

> **Correction (2026-10-22).** Until this date P3 read as below. It needs `β = (2/3)Ω_m = 0.21`,
> which A78's BBN bound `β < 0.027` excludes (≈8σ, §7). It is kept for the record of the footing
> discussion only; it is **not** the theory's postulate.
>
> *Superseded P3:* `a₀ = κ c √(G ρ_bare)` with `κ = ½`, and `Λ_bare = 3H₀²/c²` with
`β = (2/3)Ω_m`. That pair is **not chosen**: it is the unique closure satisfying both
`ρ_bare = ρ_crit` (so `a₀ = 1.1312×10⁻¹⁰ m/s²`) and the clock's own stress identity
`ρ_β = −9βH²/(4K) = −Ω_m ρ_crit` (A42, residual 1.8×10⁻¹⁵). It follows that
`Λ_bare/Λ_obs = 1/(1−Ω_m) = 1.4624` **exactly** — the "footing ratio" 1.4626 is the matter
fraction, not a fine-tuning. **`a₀ = 1.132×10⁻¹⁰ m/s²`** at `H₀ = 67.40` is the theory's own value, not fitted to galaxies —
and **A46 has now run the honest background fit, with a two-sided answer.** (i) The model is an
*exact reparametrisation* of flat ΛCDM in the distance ratios,
`E_model(z;Ω_m,h) = E_ΛCDM(z;Ω_m/(1+Ω_m), h√(1−Ω_m))`, so `D_M/r_d`, `D_H/r_d`, `R`, `ℓ_A` and the
whole SNe diagram are invariant; on BAO+SNe+CMB (13+1580+3 points) **Δχ² = −0.58, ΔAIC = −0.58**.
**The cosmology is not excluded**, and A42's "10.3σ" compared an expansion coefficient to a
density — withdrawn. (ii) The degeneracy forces `H₀ = 56.8 km/s/Mpc` and hence `a₀ = 9.53×10⁻¹¹`;
fixing `H₀ = 67.40` to keep `a₀ = 1.132×10⁻¹⁰` costs **Δχ² = +58.8 (7.7σ)** without the baryon
prior and +749 (27.4σ) with it, and the failure is the **ruler** (`r_d = 169.8` vs 147.09 Mpc,
+15.5 %), not `H(z)`. So the footing question is now **data-separated**: the observed-vacuum
footing fits the background and the bare one costs 7.7σ. Which is the theory's own depends on
whether `H₀` is predicted or measured — and A62 resolves that, because `a₀/(cH₀) = 2κ/Z` ties the
two, so `κ = ½` fixes the ratio and `H₀` fixes the scale.

**P4 — The cold sector.** A collisionless medium, not a particle, carrying the cosmic share of
each system's catchment, `M_c = (Ω_c/Ω_b) M_b = 5.3643 M_b`, of which a fraction `u(r)` sources
the law's phantom and the remainder falls natively. `u(r)` is a **step** at the splashback
radius: `u = 1` outside it (single stream), `u ≈ 0.47` inside (measured; mechanism open).

**P5 — The strong-field turn-off.** `ν_fix = 1 + (ν−1)/(1+(y/y_t)²)` with `y_t` tied to the
observed `Λc⁴/a₀²`. This is a **posit**: `y_t = 66.30` is fitted once `Λ` is taken from data.

That is the whole theory. Its other inputs are measured, not derived: κ (fitted, or set by P-therm),
`u ≈ 0.47`, `Ω_c/Ω_b`, and the background `Λ` and `H₀`. The full count is in §7.

---

## 2. The action

In unitary clock gauge, with `u = K|P|`, `E_i = (Ṗ_i − Lie_N P_i)/N`, `F_ij = ∂_iP_j − ∂_jP_i`:

$$
\frac{L}{N\sqrt h}=\frac{{}^{(3)}R+K_{ij}K^{ij}-(1+\beta)\theta^2-2\Lambda_{\rm bare}}{4K}
+P^iD_i\ln N-W(u)+\frac{\eta}{2}E_iE^i-\frac{\gamma}{2}(D_iP^i)^2-\frac{\gamma}{4}F_{ij}F^{ij}
+\mathcal L_{\rm cold}+\mathcal L_m .
$$

Everything is in this line. The coefficient table (A33, `A33_master_action/MASTER_ACTION.md`):

| term | coefficient | fixed by |
|---|---|---|
| EH + Λ | `1/(4K)`, `Λ_bare` | derived normalisation; `Λ_bare ≥ 1.462 Λ_obs` |
| `θ²` | `β` | **free, bounded** `β > 2ηa₀²/K`; invisible to α₁, α₂, β_PPN |
| clock | **1** | derived: the only O(ε) lapse source |
| `W(u)` | the log form above | derived: one gate per site (A2), least dissipation (A35) |
| `E²` | `η` | free, bounded `η ≥ γ` |
| `(D·P)²`, `F²` | `γ = KL_*²/2` | **defines** `L_*`; measured through it |

---

## 3. What follows, with provenance

**3.1 The law.** In the static spherical limit the P equation and the lapse equation give

$$
\boxed{\,g_N=\frac{g^2}{g+a_0}\,}
\qquad\Longleftrightarrow\qquad
g=\frac{g_N}{2}\Big(1+\sqrt{1+\frac{4a_0}{g_N}}\Big),
$$

with residual exactly 0 (A12, A33 K3; Lean `A8.gCanon_root`, `A8.gCanon_root_unique`). Deep
limit `g → √(a₀g_N)` with coefficient exactly 1; strong-field limit `g = g_N + a₀ − a₀²/g_N + …`.

**3.2 The medium.** The law is the **Langmuir isotherm**: `μ(x) = x/(1+x)`, `x = g/a₀`;
equivalently `1/(g−g_N) = 1/g + 1/a₀`, a harmonic (series) sum of drive and capacity. Capacity
`= ` affinity follows from `θ_max = 1` with a linear element, and **n = 1 is the stationary
point of the Thomson/Onsager functional** `Ψ(A) = A²/2a₀ + (g−A)²/2g` (A35). The rival n = 2 law
is **not a state**: residual `2−√5` at `g = a₀`, excess energy `(9−4√5)a₀/4`, entropy production
`0.62 a₀k_a > 0`, failing detailed balance (A35). `A2`'s exact two-law separation is
`2/√3 − 1 = 15.470 %` relative to the smaller, `13.397 %` relative to the larger, at
`g_N = a₀/2`.

**3.3 The three lengths — do not conflate them.**

| symbol | definition | value | role |
|---|---|---|---|
| `L_MOND` | `c²/a₀` | `9.602×10²⁶ m = 31.1 Gpc` | the MOND length |
| `ℓ₁` | `√(8π/Λ)` | `4.80×10²⁶ m = 15.6 Gpc` | the cell length |
| `L_*` | `√(2γ/K)` | `24 pc` | the stiffness length |

`L_MOND = 2ℓ₁` is **exactly equivalent** to `κ = ½` and to `R = 4` (A19, A27; Lean
`A8.kappa_half_sq`). And `L_*/L_MOND = σ_c²/c²` exactly — the stiffness length sits nine decades
below the MOND length **because the cold medium is non-relativistic** (`σ_c = 8.33 km/s` gives
`7.7×10⁻¹⁰`). That ratio is a statement about the medium, not a mystery.

**3.4 The P sector has one coupling.** `η = γ` (one stiffness) gives `c_s² = γ/η = 1`
**exactly**, `λ_P = √(η/K) = L_*/√2 = 16.971 pc`, `m/H₀ = 2.620985×10⁸` — to fifteen digits the
value A22 reports (coordinator, `closure_theorem.py`). So `(β, η, γ)` collapse to one scale plus
a bounded `β`. Do **not** read `γ = KL_*²/2` as a derivation of `L_*`: it is the definition.

**The K question, settled by A61 (19/19).** `K = 4πG` **uniquely**: the Einstein–Hilbert
normalisation is `1/(4K) = 1/(16πG)`, Poisson is `∇²Φ = Kρ`, and Friedmann's `8πG` is `2K` — so
BRIEF's `K = 8πG` is the same symbol carrying a factor 2, not a second convention. Consequences:
`L_* = 24.025 pc`, `λ_P = 16.988 pc`, `R_core = π√(γ/4πG) = 53.370 pc`, `r_switch = 3.73 pc` (MW) /
`18.43 pc` (dwarf), `λ_J = 106.74 pc`. **A20's window is unchanged** at `[24.03, 90.03] pc` — `8πG` is
never used in any lane's arithmetic. The "coincidence" `L*(4πG) = λ_P(8πG)` is an **exact identity**,
`L*(2K) ≡ λ_P(K) = √(γ/K)` with residual 0 for all `γ, K` — and the *direction* is corrected: it is
`L*(8πG) = λ_P(4πG)`; `λ_P(8πG) = 12.013 pc` and `L*(4πG) = 2λ_P(8πG)`. The identity needs `η = γ`,
else `L*(2K) = c_s λ_P(K)`. Two defects A61 found in A33 and this document: A33's extrinsic-curvature
term has the **opposite sign** to its own lapse equation (R3 coefficient unaffected), and its
coefficient table tags `γ, η` as `[L²]` when in SI they are `m⁵ kg⁻¹ s⁻²`. No number moves.

**3.5 The four gates.**

| gate | result | provenance |
|---|---|---|
| lensing = dynamics | `Φ = Ψ` at O(ε); `(Φ−Ψ)/Ψ = O(Ψ) = 2.63×10⁻⁷`; first slip is second order. The sector is a **charge** sector: exactly one O(ε) lapse source, so the stress is dust at leading order | A12, A3, A32 (clean room) |
| GW speed | `c_T² = 1` **exactly** for the speed. Off the `P̄=0` background the mode also acquires a **mass** — a mass, not a speed | A3, A31 (check 28) |
| Solar System | **`α₁ = α₂ = 0` is false in the MOND regime and the theory SURVIVES anyway.** A59's bilinearity theorem: `α₁` enters the Lagrangian bilinearly in velocities, so **every observable is `O = α₁ × (v/c)² × (dynamical quantity)`** — there is no velocity-independent term. The bound `|α₁| < 10⁻⁴` is a bound on the coefficient *as measured in that environment*, and this theory's `α₁(g,r_s) = 4u′/(D−u′)` spans **46 decades**. At LLR's `g = 6.3×10⁷ a₀` it gives `1.1×10⁻¹³` (**8.9 decades inside** the bound); at binary pulsars' `10⁹–10¹² a₀`, `8.4×10⁻²⁴` (**18.6 decades inside**). The galactic value 0.93 at 8 kpc is real but **no PPN test reaches it** — so A36's exclusion is **over-scoped by ~13 decades**. A60 then solved the Sun *embedded* in the Galaxy (A22 had solved it isolated): the galactic/solar field ratio is **4.57×10⁻⁶** — A36's "2.19×10⁵ mismatch" was its inverse — and the embedding shifts `α₁(1 AU)` by only 4.9×10⁻⁸, giving **−1.63×10⁻¹³, 6.1×10⁸ below the bound** (A36's K11 understated by 3×, prefactor 2 vs 4). Pioneer: preferred-frame signal 5.5×10⁻¹² to 1.8×10⁻¹¹ of the thermal residual — invisible. Kernel anomaly `a₀ = 2557 B_E` uncured; `y_t = 66.30` closes Λ and planets pass 9.14×; `a_P = GM/L_*² = 6.61×10⁻³ B_E`, unobservable (0.17σ) | A22, A4, A30, A36, **A59, A60** |
| stability | `dg/dg_N ∈ [1,∞)` at every acceleration; `c_s² = 1`; principal positivity `β > 2ηa₀²/K` | A4, A3, §3.4 |

**3.5b The DOF count: 5 modes — computed, not budgeted (A64 → A54 → A68).** *Resolution (2026-10-22,
A68's bracket algebra, 39/39 checks, 9 mutations each breaking a named check).* The 5-vs-4 "mismatch" is
**closed in favour of 5, and there was never a repair to make.** Three computed facts decide it:

1. **There is no `φ_P`.** The P Legendre map is invertible — `det ∂²L/∂Ṗ∂Ṗ = η³h^{3/2}/N³ ≠ 0` (2.476491,
   closed form matching to residual 0) — so `π_P = 0` is not a primary constraint, and the P equation is
   second order. A66's "P momentum constraint" does not exist in this action.
2. **A66's mechanism is absent, not merely small.** The exact `O(P²)` content of the shift constraint is
   `H_i^(P) = π_P^k F_ik − (D·π_P) P_i`; the coefficient of `P_i D_j P^j` is **exactly 0**, and the whole
   object is linear in `π_P`.
3. **The bracket is degenerate on the only surface that matters:**
   `{H_i(x), π_P^j(y)} = [π_P^j δ_i^k − δ_i^j π_P^k] ∂_k δ − δ_i^j (D·π_P) δ`. It is linear in `π_P`,
   contains no `P` at all, and is the **zero matrix at `π_P = 0`** (rank 0 at five configurations, max
   entry 0.0; off-surface rank 3, or 2 when `D·π_P = 0`). Since the bracket is linear in `π_P` with no other
   field dependence, "rank 0 on `π_P = 0`" is an identity at every configuration — not an order-counting
   artefact.

So `SC = 0`, and `(26 − 2·8 − 0)/2 = 5`, agreeing with A54 with **none** of its eight first-class
constraints reclassified. Route C's 4 needed `SC = 2` that the action does not supply. *The design budget of
4 was the error, not the action.*

**The fifth mode, derived rather than dialled.** `Z = K(2+3β)/β + ηp²`, positive iff `β > 0` on the branch
where the θ Legendre map is invertible (`2+3β > 0`); the potential is `αp⁴` with the longitudinal P's `K/2`
mass exactly cancelled by the conformal gradient, so **`m² = 0` and `c_s² = αp²/Z → 0`** — a **gapless `k⁴`
mode**, healthy for `β > 0`, `η > 0`, `α = γ > 0` (36/36 grid points). It is the mixed conformal /
P-longitudinal scalar. **A67's `m² = 2/L★²` is retracted**: it is `K/η` with `η = KL★²/2` substituted — an
input echo — and it belongs to the two **transverse** P modes, whose Compton wavelength is `√(η/K)`, equal to
16.9706 pc *only* under that assumption and 24 pc or 29.39 pc under others. **The action forces `α = γ` — the single-stiffness condition — but not `η = γ`** (Jacobian `1/η ≠ 0`);
so exact luminality of the P sector is a choice, not a theorem. (Precision from A83: `α = γ` is **not** a
second-class condition — A68's Dirac matrix carries no `α` or `γ`. What is actually proved: single
stiffness ⟺ `α = γ`; kinetic degeneracy ⟺ `β = −2/3`; stiffness block non-degenerate ⟺ `αγp ≠ 0`.) The graviton's `c_T² = 1` is a separate result (the TT action) and is unaffected — A68's `c_T²` is
the transverse *P-mode* sound speed, an overloaded symbol worth watching.

Two inherited gaps, stated: the full nonlinear `{H_⊥, H_⊥}` closure at `β ≠ 0` is A54's, not re-derived
(it can only move the count to 6 or 5, never 4); and the transverse/scalar decoupling at quadratic order is
round-2 §3's. Both are flagged in A68 §6.

**The count itself.** A64 counted **5 degrees of
freedom — 2 tensor + 2 P-transverse + 1 mixed scalar — against a design budget of 4** and graded that a
FAIL. A54 then did the full canonical analysis (34/34 checks, 13 Lean theorems) and found the count is
**correct and benign**: 26 phase-space dimensions, 8 first-class constraints, `(26−16)/2 = 5`; the
scalar's kinetic coefficient is `Q₀ = (2+3β)/(Kβ) + ηk²/K²`, **positive iff `β > 0`**, with the
record's principal-positivity bound `β > 2ηa₀²/K` *being* the ghost-freedom condition to one part in
10¹⁸. **The "fifth mode" is not extra** — it is the P longitudinal, already among `P_i`'s three
components; the lapse fixes `π_P^L`, not `ψ`. The design budget of 4 was the error, not the action. So
the four gates **do** descend from one premise: the charge `D·P` with unit coefficient in `H_⊥`, no
`O(ε)` P term in `H_i`, and no P-curvature coupling — from which `Φ = Ψ` at `O(ε)`, `c_T² = 1` exactly,
`α₁ = α₂ = 0` with `β_PPN = 1` wherever `kL_* ≫ 1`, and `dg/dg_N = 1 + a₀²/(g²+2a₀g) ≥ 1` all follow.
**The galactic-regime α₁ is computed, and it is not a dipole (A82, 27/27, 12 mutations).** The naive PPN
coefficient `0.073–5.194` at 1–30 kpc is reproduced exactly (A36's value, max deviation `5.0×10⁻³`), but the
exact nonlinear BVP shows the induced acceleration is a **bounded radial monopole**,
`δa = −2w²a₀²/(g+2a₀)` with `δa ≤ w²a₀ = 1.424×10⁻¹⁶ m/s²`, and the **dipole is identically zero** — every
`O(w²)` source is even in `cosθ` (`l=1` projections `≤3.3×10⁻¹⁶`, dipole moment `7.1×10⁻¹⁴`), with a
quadrupole of `2/13`. The expansion fails at *both* ends of the interval: the ordering `w² ≪ ε` is violated
everywhere (`w²/(Φ/c²) = 5.83` at 8 kpc) and the response denominator `1−u′ > 1/2` beyond `24.14 kpc`, so no
controlled window spans 1–30 kpc (break radii `6.95` and `24.14 kpc`). The pulsar prediction is
`α̂₁ = 3.0×10⁻²⁴`, **19.07 decades inside** Shao–Wex's `3.5×10⁻⁵`; suppression is kinematic
(`g_int = 1.15×10¹²a₀`), not EFE. Caveats: the `h^{ij}` `l=0` term is enumerated but not integrated (quoted
`α₁` are `12/13` of the full first-order value) and the `l=2` radial BVP is not solved (`2/13` is an upper
bound). **A55's SLACS shortfall, re-audited by
A70, is not a falsification.** A55's 11.5 % / 4.9σ used `1/median²` for the mass boost — assuming
`M₂D ∝ R²` — giving `M_*/L = 1.283×` Salpeter. The model's actual response is `dlnR/dlnB = 0.7775`
(computed by finite-differencing the lens-equation solver), and root-finding gives **`B = 1.174 ± 0.039`**
(response route 1.1737, agreement 10⁻⁴). At 1.174 the required IMF normalisation is **1.80σ** from the same
survey's dynamical calibration (`1.00 ± 0.036` dex) and inside its 95 % bound `[0.850, 1.177]` by 0.25 %;
at A55's 1.283 it would have been **outside at ~3σ**. So the lensing gate passes **only with a heavy
IMF — at the 95 % edge, not comfortably** — and A55's 4.9σ was an IMF-prior artifact compounded by an
arithmetic error. What survives: per-lens scatter `0.0927` dex against `0.0446` propagated (real
astrophysical scatter no normalisation removes), and one shape term — `R_E/R_e` at `+0.172 ± 0.060`
(**2.9σ**), inner lenses `0.216` dex low. **A80 has now tested it, and it is not robust**: the residual dies
at `n = 6.09` (`Δ(−2lnL) = 47`) if the catalogue's `f*` is read as a Sérsic enclosed fraction — which its
own scaling supports (`f* M_E/M*_tot = 0.0240 + 1.0223 f₂(x; n=4)`, `R² = 0.8967`) — and survives at **2.3σ
for every `n ≤ 20`** if `f*` is read as a fixed mass. The free-`n` likelihood overshoots to `n₀ = 14.14` with
the slope reversed to `−0.148` (−3.3σ), which is unphysical, so neither reading is decisive. **The residual
is a statement about how `f*` was defined, not about the theory.** Lensing does **not** measure `a₀`: with the IMF free, `Δχ² = 0.26` over `κ ∈ [0.20, 0.80]`
(`dlnR/dlnκ = 0.1205` vs `dlnR/dlnB = 0.7775`). The slip is unobservable (`2.8×10⁻⁶` arcsec, 8600× below
the error) and A55 corrects A12's coefficient: the trace-free identity gives `3K`, not `2K`.

**3.5c The P-sector sound speed: free, unconstrained, and harmless (A69).** A68 showed the action forces
`α = γ` but not `η = γ`. A69 asked what does fix it, in four channels, each with a computed obstruction
rather than an assertion (56/56 checks, 9 mutations each breaking a named check):

- **Foliation-preserving diffeos do not.** The P action is invariant for *arbitrary* `(η, γ)` —
  `|ΔS|/S ≤ 9.698×10⁻⁵` at `λ = 0.02`, with clean `λ²` scaling (ratio 3.996) and **no growth of the residual
  when `η ≠ γ`** (1.109). The reason is structural: `E_i` is a covector and both gradient operators are
  scalar densities, so the variation is `η·0 + γ·0`.
- **There is no shift symmetry.** `W` gives `δS = −a₀|c| = −2.055×10⁻³⁴` per unit volume, i.e. a mass
  `d²W/dP² = K`. `P → P + c` is not a symmetry.
- **Weyl invariance is not a symmetry at all** — the three derivative operators carry weight `2w`, the clock
  term `w+2`, `min_w max|exponent| = 2` — and could not fix a ratio anyway, since all three share one weight.
- **Conservation does not tie them.** `∂_tT⁰⁰ + ∂_iT⁰ⁱ = Ṗ·EOM` is the Noether identity, satisfied to
  `7.52×10⁻¹⁷` for every `(η, γ)`.

So the only handle is `c_T² = γ/η = m_T²L★²/2`, **with `γ` pinned by the fitted `L★` and `η` free**: the
sound speed is measured by the range of the P-mediated force and by nothing else.

**Observationally UNCONSTRAINED, and the reason matters.** The P sector's `O(ε)` stress is *dust*
(`w ∝ ε`, a factor 10 per decade), and its pressure is the **elastic** one, `√(γρ_c) = 0.7204 m/s`
(A16/A20's 0.72, to 5.0×10⁻⁴) — **not** `√(γ/η)`, which would be `10⁸ m/s` at `η = γ` (ratio² 1.73×10¹⁷).
Growth, clusters, CMB and GW therefore see nothing: there is no P–baryon coupling, and the graviton TT speed
is exactly 1 (a P background contributes only a `3.249×10⁻³⁴ eV` mass; the loop correction to `δc_T²` is
`6.7×10⁻¹⁴⁴`). **If** one nonetheless posits the medium's pressure to be `c_T²ρ`, linear growth gives
`γ/η < 1.916×10⁻⁷` at 95 % CL (`3.066×10⁻⁸` at `k = 0.5 h Mpc⁻¹`), hence a P-mode Compton wavelength
`> 38.77 kpc` instead of 16.971 pc. That is the one number that would decide it, and no existing dataset
supplies it.

**All four gates survive `γ/η ≠ 1`, and none of them fixes it:** (i) lensing = dynamics is exact at `O(ε)`,
with `γ` entering only at `O(ε²)` through the measured `L★` (`Π_γ/Π_W = 0.5000` at `r = L★`) and `η` not at
all; (ii) `c_T² = 1` is exact for every `γ/η`; (iii) `α₁ = 8.161×10⁻¹⁴` at 1 AU is `η`-independent, and
`α₂ = 0` because `j_P(E=0) = 0`; (iv) the Hamiltonian is bounded for `β > 0, γ > 0, η > 0`, i.e. `γ/η > 0`,
with the principal-positivity bound translating to the vacuous `γ/η > 5.948×10⁻¹⁹` (24/24 grid points
healthy). A54 is refined, not contradicted: its G4 lists only the `W`-quadrupole, and the `γ`-sector one is
the same order at `r ~ L★`.

**The gapless `k⁴` mode is weakly coupled everywhere — and it is not the MOND mediator.** Its strong-coupling
momentum is `p_sc = K²/(8.485π a₀ α^{3/2}) = 2.836×10⁻⁶⁹ eV` — `1.90×10⁻³⁶ H₀`, `1.38×10⁻³⁵ a₀`,
`1.06×10⁻⁴⁴` of `1/L★` — with the largest loop factor over CMB/LSS/galactic scales `1.904×10⁻⁷⁰`. The EFT
needs no cutoff below the horizon. But its static Green's function is `−r/(8πα)`: a **linear potential and a
constant force**, the `μr/L★²` term of A22's exact solution — not the law. **MOND is the nonlinear
`W(u)`/charge structure, not a propagating mode**, which is consistent with MOND being intrinsically
nonlinear.

**3.6 The vacuum closure, and κ — the thermal POSTULATE gives `Z/4π`; ½ remains the fitted value.**

> **Correction (2026-10-22, after A75/A81).** This section was first titled "κ — now DERIVED". A75 proves
> the thermal identification below is a **postulate** that the action does not supply. A81's ledger
> classes `a₀` as "fixed by the P-therm postulate". So κ is not derived. It is either fitted (½) or set
> by this postulate (`Z/4π`), and the data separate the two at **1.35σ** (A81, bootstrap errors). On the
> raw SPARC χ² the gap would be 7.2σ, so the error model, not the data, sets the size of the preference.
>
> **Prior art.** `a₀ = cH_Λ/2π` is Milgrom's relation `2πa₀ ≈ cH₀ ≈ c²(Λ/3)^{1/2}` (Milgrom, Fortschr.
> Phys. 2017, arXiv:1605.07458, eq. 5). His 1999 paper (astro-ph/9805346) gives the de Sitter mechanism:
> an accelerated observer sees Unruh radiation at `T = (1/2π)(a² + Λ/3)^{1/2}`. The DSF-21 value is that
> relation on the `H_Λ` footing; it is not new to this work. Argon's AG6A also lists `√(2/(3π)) = 0.461`
> as one entry of a horizon-based menu (`κ² = rational × π^{±1}`), "in the data band but not ½".
>
> **Update (2026-10-22, A72/A73), as first written; read "derived" as "set by the P-therm postulate".**
> The coefficient `a₀/(cH)` has exactly
> one derivation in a 260,129-expression census: the thermal wavelength at the Gibbons–Hawking
> temperature, `λ_T(T_dS) = 2πR_Λ`, so **`a₀ = c²/λ_T = cH_Λ/(2π) = 8.6257×10⁻¹¹ m/s²`**, mass-independent
> to 10⁻¹². **Convention audit (2026-10-22, A79): the reduced thermal wavelength is the one the data
> select.** `λ = ħc/(k_BT_dS)` gives `2πR_Λ` and `a₀ = cH_Λ/2π = 8.62×10⁻¹¹` (`0.03σ` from A71); the full
> `hc/(k_BT_dS) = 2πħc/(k_BT_dS)` gives `4π²R_Λ` and `a₀ = cH_Λ/4π² = 1.3725×10⁻¹¹`, **2.63σ** from A71.
> So the ħ-versus-h choice is made by the fit, which is one more bit of fitting, not a derivation. That `a₀` gives
> **`κ_DE = a₀/(c√(Gρ_DE)) = √(2/(3π)) = Z/(4π) = 0.460659`**, `κ_P3 ≈ 0.381`, and
> **`2cH_Λ/a₀ = 4π = 12.566`** — so the "twelfth" is really **`4π`, the solid angle**, not `2Z = 11.578`.
> Against A71's joint fit (`κ_P3 = 0.3777 ± 0.1207`, `a₀ = 8.544×10⁻¹¹`), the thermal point sits
> **0.030σ** away in κ and **0.030σ** in `a₀`; `κ = ½` sits 0.299σ away. The data mildly prefer the
> thermal value (2.6 : 1 on statistical errors alone; LR 1.045), and **only a 2.9 % `a₀` measurement
> decides** — wide binaries at 18–22 kAU with ≈4×10⁵ pairs. Downstream at the thermal point:
> `y_t = 77.85` (inside [60,140]), `L★ = σ_c²/a₀ = 26.1 pc` (inside 24–90), `R_core = 57.9 pc`.
>
> **The competing *derivation* of ½ is dead; ½ itself survives as the fitted value (1.35σ, A81).** `1/7` (⟺ `Ω_Λ = 32π/147`) is a *match*, not a derivation: `147 =
> 3(cH₀/a₀)²` is defined by the measured ratio, the number is irrational so no cell count produces it,
> and in a 260k-form pool **65 expressions land within 0.11σ of 0.6847** with `√3 − π/3` **5.32× closer**.
> Worse, the repo's own DESI 3-pt fit gives `Ω_Λ = 0.69797 ± 0.00368` — **3.82σ** from 32π/147 (A73).
> The Planck 0.11σ agreement is number-vs-one-dataset, not a test.
>
> **What remains a premise, not a theorem:** that the acceleration scale is the one at which a carrier's
> Compton wavelength equals its thermal wavelength at `T_dS`. A72 shows that premise derives the *scale*
> with zero free parameters and a mass-independent cancellation, but its response is analytic (slope 1),
> so it does **not** derive MOND's shape — the law still comes from the Langmuir gate (§3.5). One premise
> for the scale, one for the shape.

**3.6a Confidence ledger on the thermal postulate for κ — what is certain, what is premise, what is marginal.**

- **CERTAIN (algebra, reproducible in one line).** `a₀ = cH_Λ/(2π)` ⟹ `κ_DE = a₀/(c√(Gρ_DE)) =
  √(2/(3π)) = Z/(4π) = 0.460659` identically; `2cH_Λ/a₀ = 4π`; and `a₀ = cH₀/7 ⟺ a₀ = cH_Λ/Z ⟺ κ = ½`,
  so "1/7" and "1/Z" are the same statement in two frames. These are checked numerically and do not depend
  on any lane's code.
- **COMPUTED (22/22 and 26/26, mutation-tested).** In a 260,129-expression census the thermal coefficient
  `1/(2π)` is the only one with a derivation (`0/540` of the `1/7` hits are derivable); the cancellation is
  mass-independent to 10⁻¹²; and `Ω_Λ = 32π/147` has 65 rivals inside 0.11σ with `√3 − π/3` 5.32× closer.
- **PREMISE — not a theorem.** That the acceleration scale is the one at which a carrier's Compton
  wavelength equals its thermal wavelength at `T_dS`. **Nothing in the action forces this.** It derives the
  *scale* and not MOND's shape (the response is analytic, slope 1). If the premise is wrong, `a₀` is not
  predicted and κ returns to being a fit. One more honest wrinkle: the P mass is ~10⁸ × `T_dS`, so this is
  a statement about the *horizon's* thermal wavelength, not about a thermal population of P particles —
  the mass-independence is what makes that distinction possible, and it is also the weakest link.
- **MARGINAL (data).** `0.030σ` vs `0.299σ` is a **2.6 : 1 preference, not a detection**. The measurement's
  total error is 32 %, so a 1 % agreement of central values is suggestive, not decisive; and choosing
  between two candidate coefficients adds a factor-2 look-elsewhere. **κ = ½ is not excluded** — it sits
  0.27σ from the thermal value and both are inside the joint 95 % region.
- **DEAD (computed).** `1/7` as a derivation, `Ω_Λ = 32π/147` as a prediction: both killed by A73.
- **THE HONEST ONE-LINER.** *κ = Z/4π follows from one postulate (Milgrom's `2πa₀ ≈ c²(Λ/3)^{1/2}` on the
  `H_Λ` footing) that the action does not supply (A75); κ = ½ is the fitted value. The data separate them at
  1.35σ on the declared error model (A81). A 2.9 % `a₀` measurement decides. Neither value is derived.*

**3.6b What changes if you take the thermal point — the algebra does not break, two coincidences die.**
The spine is untouched: the law `g_N = g²/(g+a₀)`, the closure identity (true for every κ), `c_T² = 1`,
the 5-mode count, the four gates, `α₁/α₂`, and all 87 Lean theorems (A8's 40 + A83's 47) — those are conditional algebra about
the κ = ½ branch and remain true; only their labelling as "the theory's value" changes. What shifts:

| quantity | κ = ½ | κ = Z/4π | band / verdict |
|---|---|---|---|
| `a₀` | 9.354e-11 | **8.618e-11** | 0.30σ / **0.03σ** from A71 |
| `y_t` | 66.35 | **77.85** | both inside [60,140] |
| `L★ = σ_c²/a₀` | 24.04 pc | **26.09 pc** | both inside [24,90] |
| `R_core = (π/√2)L★` | 53.4 pc | **58.0 pc** | — |
| `m_P = ħ/(cL★)` | 2.66e-25 eV | **2.45e-25 eV** | — |
| `R ≡ Λc⁴/(8πa₀²)` | 4 | **3π/2 = 4.712389** | — |
| `Λc⁴/a₀² = 8π/κ²` | 32π = 100.531 | **12π² = 118.435** | — |
| `a₀/(cH₀)` | 1/7 | **1/5.20** | — |
| `L_MOND/ℓ₁` | 2 exactly | **2.171** | — |

**Neither apparent casualty is one, on inspection.** (i) A19's saturation cap was already principle-free by
its own words — *"Nothing in the class picks one; the data pick the quarter, but the data measure κ itself"* —
and `R = 1/κ²` is a tautology at every κ, so `{1,2,4}` were three hand-chosen integers, not a derivation.
At the thermal point `R = 3π/2` simply leaves a set that never had a principle; nothing is lost because
nothing was there. (ii) `L_MOND/ℓ₁ = 2` becomes **`4π/Z = 2π√(3/(8π)) = 2.170803764` exactly** — the
"twice the cell" reading is replaced by an equally exact closed form. Nothing else fails: the falsifier band
`κ ∈ [0.3415, 0.5265]` contains both (κ_P3 = 0.381 at the thermal point), the `L★` window and the `y_t` band
pass on both, and the IMF tension is 1.97σ in the `R_E`-only fit because A71 already fit at `8.544e-11` —
essentially the thermal point (it rises to **2.27σ** when the `σ_ap` channel is added; A85). **`3π/2` and `12π²` are no less clean than `4` and `32π`; they are simply different.**
The data do not force the choice (0.27σ apart), so the branch is a declared choice, not a derivation.

**3.6c β is measured — and it settles the footing war (A78, 30/30).** β is not a field-redefinition
redundancy: the three rescalings that could absorb it (`h → Ω²h`, `N → χN`, `P → λP`) are pinned by three
measured normalisations (static `G`, `c_T² = 1`, the unit clock charge that fixes the law's shape), a 3×3
system with **det = 4** and unique solution `(1,1,1)`; and the scalar pole shifts by **15/11** between β = 1
and β = 3 while being invariant under every field rescaling. It *looked* invisible because `θ ≡ 0` on every
static configuration, so `∂S_static/∂β ≡ 0` exactly — β is absent from the law, AQUAL, `α₁/α₂/β_PPN` and the
TT sector. The one observable is the cosmological/Newtonian `G` ratio:

$$3(2+3β)H^2 = 2Λ_{bare}c^2 + 4Kρ \quad\Longrightarrow\quad \frac{G_{cosmo}}{G_N} = \frac{2}{2+3β}$$

which is 0.961 at β = 0.027 and 0.400 at β = 1. BBN's `|ΔN_eff| < 0.30` with `ΔN_eff = −11.1738β` gives
**β < 0.027** (i.e. `G_cosmo/G_N > 0.961`). **β is measured, not free**, and it leaves A33's free list.

**It also kills a footing.** A33's `β(Λ_bare = Λ_obs) = −0.211` and `Λ_bare ≥ 1.462Λ_obs` came from applying
the *vacuum* Friedmann equation at `H₀` with `ρ_m` dropped. With matter included, β = 0 sits **exactly** at
`Λ_bare = Λ_obs` (checked to 10⁻¹⁰). So `Λ_bare = Λ_obs(1 + 2.194β)`, and with **β < 0.02798**,
**`Λ_bare/Λ_obs ∈ (1.000, 1.0613)`**. The old "P3" footing (`ρ_bare = ρ_crit`, `a₀ = 1.132×10⁻¹⁰`) requires
β = 0.210, hence `ΔN_eff = −2.34` — **8× the BBN bound, ≈8σ excluded.** The three-footing conflict of §6.2
therefore collapses: **`a₀` survives only in `8.63–8.89×10⁻¹¹`**, with the thermal `8.62×10⁻¹¹` at its lower
edge and the canonical `9.35×10⁻¹¹` just above.

**It fixes the `L★` guard.** At the thermal `a₀`, `L★ = σ_c²/a₀ = 25.44 pc` — **6.0 % above the 24 pc floor**,
so A65's 2.38 % failure was an artifact of the *canonical* `a₀` (23.43 pc), not of the theory. A76 (35/35)
also shows the "floor" itself is A65's rounding of 23.4289 pc upward, and that **no σ_c measurement exists on
disk**: the best independent value is the computed 10⁴ K thermal width, 8.226 km/s (+3.5/−0.55 over
`μ ∈ [1.4, 0.6]`, ±10 % in T), which puts `L★` anywhere in **20.4–47.6 pc** as μ varies. So `L★` remains
*fitted* in the honest sense — derived in form, computed from a thermal width, with a factor-2.3
composition uncertainty and no direct measurement.

**`η/γ` is the one hole that did not close (A77, 40/40).** The equipartition candidate is false twice over:
(i) `c_T² = γ/η` is a stiffness/inertia ratio, not `dP/dρ` — the two coincide only if `ηρ_c = 1`, and the
closure needs `ηρ_c = 7.5×10⁻⁹`, an inertia `1.34×10⁸` below the medium's density; (ii) equipartition itself
gives `3k_BT_dS/m_P = 2.764σ_c²` → 13.84 km/s, not 8.33, which would predict `κ = 1.144` — **6.5σ excluded** —
and `m_P/T_dS = 1.4×10⁹`, so the medium is not in thermal equilibrium at all. The missing principle is named:
a **Kubo/transport matching** for the kinetic coefficient, `η⁻¹ = lim_{ω→0}(1/ω)∫dt⟨[P_i(t),P_j(0)]⟩`, whose
hydrodynamic limit `η = 1/ρ_c` would give `γ/η = 5.77×10⁻¹⁸` and `c_T = 0.72 m/s`.

**3.6d The premise is a postulate — proved, not conceded (A75, 24/24; A74, 29/29).** A75 tested whether the
action forces the thermal identification and returned a clean **no-go**, with four computed obstructions:

1. **The action is classical** — `G, Λ, a₀, η, γ, β` and no `ħ`, no `k_B`. A statement containing both
   cannot be a functional of variables that carry neither.
2. **The gate is athermal at fixed drive.** `θ = g/(g+a₀)` exactly, `dθ/dT|_g = 0`, heat capacity
   **`C_g = 0`**. A system with zero heat capacity cannot generate a thermal-wavelength condition. The one
   temperature-sensitive gate (linear/energetic coupling) has `A(0) = a₀/2 ≠ 0` and is excluded by A63 K16.
3. **The action's own carrier fails the literal condition by ×1.99×10⁹** — `λ_C = L★/√2 = 16.99 pc` against
   `λ_T = 2πc/H_Λ = 33.80 Gpc`; equality would need `L★ = 47.8 Gpc`. (The identification `λ_C = L★/√2`
   is itself conditional on `η = γ`, which A68 does not force: A68's transverse mass is `√(K/η)`, while
   `√(γ/K)` is a *length*, not a mass.)
4. **A72's formula never uses the carrier.** `a_sat = k_BT/(mλ_C) = k_BTc/ħ`: the mass cancels identically
   (spread 0 over four masses), so no `η, γ, K` enters. It is the Gibbons–Hawking temperature rewritten as
   an acceleration, `a_Unruh(T_dS) = cH_Λ = 5.414953×10⁻¹⁰`, divided by `2π` — which A72's own census labels
   **RESTATEMENT**.

**What even the thermal story does not give for free.** The natural Unruh–DeWitt coupling gives
`a₀ = cH_Λ` — **2π too large, excluded at 16.7σ** — so the `1/2π` needs the extra "one thermal
wavelength per horizon circumference" assumption on top of quantization. And adopting the premise forces
`R = 3π/2 = 4.712389 ∉ {1,2,4}` (A19's hand-picked set), which puts the `R = 4` closure **15.1 % away in
Λ**: `Λ_pred/Λ = 8/(3π) = 0.848826` (A75). **The premise and the closure are rival normalisations of the
same parameter, not independent confirmations** — you cannot have both `κ = Z/4π` and `R = 4`.

So the premise is exactly what it looks like: one identification, `a₀ ≡ cH_Λ/2π`, which supplies
`κ = Z/4π`. **Forced by the action:** the isotherm, the law `g_N = g²/(g+a₀)`, `λ_C = √(η/K)`,
`m_T² = K/η`, `L★ = √(2γ/K)`, and the gapless `k⁴` fifth mode. **Not forced:** any relation between
`λ_C` and `1/T_dS`.

**What the identification costs (A74, 29/29).** Fixing `a₀` at the thermal point costs `Δχ² = +0.0169`
(**0.13σ**) against the free fit; the `κ = ½` point costs `+1.8808` (**1.37σ**). Head-to-head,
**`Δχ² = 1.8639 → 1.365σ`, a likelihood ratio of 2.54 : 1** for the thermal point — A72's 2.6 : 1 survives
the full refit intact. SPARC drives `+2.309` of it, SLACS + the IMF prior gives back `0.569`, clusters cost
`0.124`. **Neither point is rejected**, the largest pull anywhere is the IMF at `1.955σ`, and the falsifier
is clean at the thermal point: `y_t = 77.944 ∈ [60,140]`, `L★ = 26.087 pc ∈ [24,90]`, `R_core = 57.95 pc`.
The 2.5 : 1 lean rests on a 9.4 % block-bootstrap error that is **8.3×** the formal `Δχ² = 1` error — worth
exactly what a 1.4σ lean is worth, which is nothing yet.

The closure relation itself is unchanged and holds for every κ:

$$
I(y_t)\equiv\int_0^\infty \frac{y(\nu-1)}{1+(y/y_t)^2}\,dy=\frac{\Lambda c^4}{a_0^2}=\frac{8\pi}{\kappa^2}
\quad\text{identically, for every }\kappa>0 .
$$

For the canonical kernel the left side is `(π/2)y_t − ln(y_t/4) + C_can`, `C_can = −0.8862944`;
at the **thermal (postulated)** point `Λc⁴/a₀² = 118.6` and **`y_t = 77.85`**; at the old `κ = ½` footing
`Λc⁴/a₀² = 100.4058` and **`y_t = 66.2999`** (A4, A25, A28) — the numbers below are the κ = ½ ones. `I` is strictly
increasing, hence invertible: **one de Sitter member per κ, and no internal relation selects
one.** `y_t(κ) = 180.8, 102.7, 66.38, 34.6, 17.6` at `κ = 0.3, 0.4, 0.5, 0.7, 1.0`.

The scope, honestly: this is a modulus of the **two-equation halo truncation** (A15), and every
route to fixing it inside that system is closed — counting (A1, A10: the required count
`𝒩 = 2√(32π/3) = 11.5776` is irrational), dimensional analysis (A1: one free function,
`ħGΛ/c³ = 2.85×10⁻¹²²`), strain saturation (A1: `4√(π/3)`, off by 8.19), Euler charge (A19: a₀-blind,
a total derivative), channel counting (A19: basis-dependent), the cap's natural values (A19: data
pick 4, nothing forces it), the factor 2 (A27: `κ = ½` is a **curve** `β√χ = 2`, so
(2,1) and (1,4) both work), the turn-off (A28: `y_t` is κ in disguise), and the dimension route
(A34: κ = 1/n is a tautology; the codimension of a point in 4D is 3, not 2; D=5 is not even
excluded). **Deriving κ is a UV problem, not an EFT problem, and that is a proved statement
about this system.**

**What the data say about κ — measured, and not decisive.** A51 ran the first joint fit with a
real error bar on κ itself (171 SPARC curves, the cluster amplitude, KiDS lensing, BAO+SNe+CMB):
**`κ = 0.371 ± 0.026 (stat) ± 0.116 (syst) = 0.371 ± 0.119`** in the P3 convention. So ½ sits
**1.09σ away in total error** — admitted, not confirmed — but **4.9σ away statistically**; the whole
distance between "excluded" and "admitted" is the error model, not the data. The fit is dominated by
SPARC (±9.4 %); the cluster adds 11.0 % but only by marginalising `u`, which was derived from the same
amplitudes; KiDS carries **exactly zero** information (an exact `(M_b,a₀)` degeneracy — χ² constant to
6 digits over a factor 2.9 in `a₀`); and BAO+SNe+CMB is **κ-blind**, because κ does not enter `E(z)` at
all. Seven defensible weightings of the same 3375 points give κ from **0.325 to 0.495** (20.8 % half-span,
6× the bootstrap error) — the systematic is analysis choice, not a prior. At `N = 1000` the gap to
0.4824 is **1.2σ statistically, 0.15σ with the coherent floor**; three sigma needs **6,023 galaxies**,
and no `N` reaches it while the floor stands. **κ = ½ is therefore not empirically decidable; only a
derivation settles it** — which is exactly what A62 attempts.

**3.7 The cold sector.** `M_c = 5.3643 M_b` is `Ω_c/Ω_b`, not a cold-sector parameter (A9, A11).
The law's phantom-to-baryon ratio at the virial radius is **25.90** (MW-like) and **3.77**
(cluster-like), 6.87× apart, crossing 5.3643 at `M_v = 1.758×10¹⁴ M⊙` independently of
concentration (A18, corrected by A31). "Cold = the law's phantom" is excluded at **7.7σ**
(`A_MID = 1.9102 ± 0.1186` against 1.000 phantom / 1.852 cosmic share). The sourcing fraction is
a step at `r_sp = 1.367 r200c = 1.414 Mpc`, 0.3 % from the caustic: `u = 1` outside (derived),
`u = 0.47` inside (measured, mechanism open) (A29). And the exact two-body solution requires
**negative** cold density in a pancake through a null point (−89.3× the mean at `R = 0.2d`),
which no positive-mass medium can do (A6, A13).

---

## 4. The theory's rotation-curve prediction — and its honest size

Fix `a₀` from P1 and P3 (`1.132×10⁻¹⁰`) and compute `V(r) = √(g r)` with `g` from the law. On
**all 171 SPARC galaxies** (3375 points, `σ² = errV² + (0.05 V_obs)²`):

| stellar M/L | canonical χ²/dof | n=2 χ²/dof |
|---|---|---|
| **fixed `Υ_* = 0.5` (zero theory parameters)** | **6.87** | **7.06** |
| one `Υ_*` per galaxy | **2.42** | 2.31 |
| same, observed-vacuum footing `a₀ = 9.36e-11` | 2.21 | 2.28 |

**Three honest conclusions, and one correction to my own earlier draft.**

1. **The zero-parameter prediction fails.** At fixed `Υ_* = 0.5` the χ²/dof is 6.87. The theory
   does not predict rotation curves without a stellar M/L, because it does not predict `Υ_*`.
   A five-galaxy subset (NGC 3198, 2403, UGC 02885, 7331, UGC 01281) gives 1.66 — but that is a
   **biased selection of well-sampled rotators**, not a theory result, and it must not be quoted
   as one. I caught this one step after writing it; `_parent/SPARC_FULL.md` records the
   correction.
2. **With one `Υ_*` per galaxy the two laws are degenerate** — 2.42 vs 2.31 — exactly as A7 found
   independently (χ²/dof 2.27, bootstrap z = 0.75, the Δχ² flips sign between footings). The
   footing barely matters on the total χ² either.
3. **Neither law fits well at 2.3/dof**, so with a 5 % floor SPARC is systematics-dominated for
   this error model. The discriminating power lives in the **shape**: A7's per-galaxy Δχ²
   distribution, and A25's RAR-knee test with **Δχ²(Q−L) = +157.96 and no free parameters**
   (pre-registered at ±25).

So the theory's claim on SPARC is not "we predict the curves". It is: **one M/L per galaxy, a
χ²/dof of 2.4 that matches the rival law's, and discrimination in the transition-region shape.**
That is a weaker claim than my first draft made, and it is the true one.

**4.1 The background, honestly fitted.** A46's result is in P3's caveat: an exact ΛCDM
reparametrisation, `Δχ² = −0.58`, **not excluded** — but the same degeneracy moves `H₀` to 56.8
and `a₀` to `9.53×10⁻¹¹`. The theory's background is therefore **viable and degenerate with
ΛCDM**. That is the honest status: it predicts nothing the background can distinguish except
through `a₀`'s footing. Fixing `H₀ = 67.40` costs 7.7σ in the ruler; the observed-vacuum footing
is the one the data allow.

**4.2 Growth — and why the theory is inert at linear order.** A45 went back to the P equation and
found why A40's two branches both failed: `u = K|P|` makes the law *quadratic* in the P field
with a square-root inverse, so **there is no linear term to perturb.** At linear order
`δP_i = K⁻¹∇δΦ/(1+(kλ_P)²)` with `(kλ_P)² = 1.3×10⁻¹²` at `0.1 h/Mpc`; eliminating the charge
gives `G_eff/G = 1 + 1/(kλ_P)² = 7.6×10¹¹` — a `k⁻⁴` runaway with **no finite linear solution**.
The modification is **inert on linear scales**; its first nonzero effect is `O(g_N/a₀) = 0.21 %`
at `8 h⁻¹Mpc`, i.e. second order in `δ`. *Why* it is inert, in one number: the smoothing radius at
which the local acceleration reaches `a₀` is `R(a₀) = 2σ²/a₀ = 1.4–52 kpc`, i.e. `k(a₀) = 29–1037
h/Mpc` — **two to four decades above every linear scale**, so on linear scales the law's argument
never reaches `a₀` and the modification cannot switch on. Stated plainly: `σ₈ = 0.7602` (6.3 % below
Planck's 0.832, *toward* the lensing surveys — KiDS-1000 gives 0.759 ± 0.021) and
`χ²(fσ₈) = 14.78/8` vs ΛCDM's 7.34/8, so growth is **~2σ disfavoured** and *not* a distinctive
prediction. The distinctive signature is the **background rate**: `f(0) = 0.452` vs ΛCDM's 0.528,
a 14 % difference, which an `fσ₈` survey at `z ≲ 0.5` should see. Branch (b)
(`G_eff(0.05)/G_eff(0.2) = 0.630`, blue) and the inert reading (exactly scale-free) are separated
by **scale dependence** — that is the discriminator A45 names.

---

## 5. Predictions, each with a number and a falsifier

| prediction | number | falsifier |
|---|---|---|
| no saddle dip between lens pairs | depth 3.529 M⊙/pc² (MW); test needs `e ≤ 0.22`, void is 0.68 — **not runnable** | a dip at any accessible `e` |
| cluster band ratio | MID/OUTER = 0.966 ± 0.102 (native) vs 1.888 ± 0.203 (phantom) | > 1.3 kills the native-cold reading |
| sourcing step at splashback | `1.37 r200c(M,z)` → 1.10/1.39/2.00/2.99 Mpc | a step that does not scale with mass |
| third-band u | 1.000 (step) vs 0.806 (phase space), 3σ at `σ_u ≤ 0.0648` | a value between them at 3σ |
| pressure core | `R_core = 53.31 pc`; 21 % dip at 30 pc, 11 % at 40 pc | a core scaling with galaxy mass at fixed `L_*` |
| wide binaries (EFE **present**) | `γ_v = 1.18` at 20 kAU (1.1771–1.1933), 1.10 at 10 kAU | `γ_v ≤ 1.05`; note 1.51 is in the theory's own no-verdict zone |
| RAR knee | Δχ²(Q−L) = +157.96, no free parameters; ±25 pre-registered | < −25 |
| turn-off scale | `y_t = 66.30` (n=1) vs 128.76 (n=2) | outside [60,140] |
| occupancy-noise skew | flips sign at `g = a₀` (n=1) vs `3a₀/8` (n=2), **opposite signs** on (0.375,1)a₀ | no flip, or a flip elsewhere |
| Jeans mass | `d ln M_J/d ln ρ = +1` (denser → bigger clumps) | the standard −½ |
| laboratory | `|δG/G| < 10⁻⁶` vs 340 ppm source-boost | +340 ppm |
| galactic α₁ | coefficient runs `0.046–5.19` at `g ~ a₀`, but the induced acceleration is a **monopole with identically zero dipole** (A82), bounded by `w²a₀ = 1.42×10⁻¹⁶ m/s²`; `α̂₁ = 3.0×10⁻²⁴` in a Galactic-field pulsar | not a falsifier as stated — **retired** (A82). A measured preferred-frame *dipole* in a system at `g ≪ a₀` would kill it, but no such measurement exists |

**ERRATUM (2026-10-22, doors push D1):** the skew-sign discriminator is **RETIRED for RAR residuals** (D1 SCOPED NO-GO, `doors_push_2026_10_22/D1_skew_preflight/README.md`). RAR errors (distance, Υ, inclination) are symmetric in log g, and in log g **both laws predict a negative skew** across the whole window g/a₀ ∈ (0.375, 1) (√N_s·skew at a₀/2: n=1 −4.38, n=2 −2.44). The sign difference exists only in linear g, where a 0.06 dex log-symmetric background alone has skew +0.42 and SPARC's measured out-of-window skew is +2.9 (canonical) / +3.2 (alt), 17–50× the best-case signal (+0.062 / −0.165). The Gaussian price is also understated: ~1e4–1e6 points, not 7,000–13,500. The statement above is kept as written; it no longer decides n.

---

## 6. The no-go ledger

**Closed by derivation**: lensing = dynamics; `c_T² = 1` (speed); `η = γ` ⇒ exact luminality;
`n = 1` from least dissipation; capacity = affinity; `L_MOND = 2ℓ₁ ⇔ κ = ½`; `M_ph/M_b` closed
form and the concentration-independent crossing; `r_switch ∝ L_*`; `u = 1` beyond splashback;
κ–Z identities, the `1/12` bracket, the Langmuir slopes, the mass cancellation and the matter-inclusive
β window (**Lean: 87 theorems — A8's 40 plus 47 new in A83 — zero `sorry`, every footprint exactly
`{propext, Classical.choice, Quot.sound}`, A8 sources byte-identical, `lake build A83` green**).

**Closed by no-go**: κ from counting (irrational `𝒩`); from dimensional analysis (free
function); from strain saturation (8.19×); from the Euler charge (a₀-blind); from channel
counting (basis-dependent); from the factor 2 (a curve, not a point); from the turn-off (κ in
disguise); from the dimension route (tautology); n=2 from any occupancy partition (not a state);
u = ½ as an identity (`u = 1+3⟨w⟩` needs `w = −1/6`); a positive-mass medium realising the law at
nulls; "cold = the law's phantom" (7.7σ).

**Closed by data**: medium-first (21σ, A26 — the law holds below `M_crit`).

**Corrected by A47 and A48** — two headline claims that do not survive their own audit:

1. **The `f_ret` collision dissolves.** CFG416's `f_ret = 0.10` is a retained **baryon** fraction,
   `M_b/(f_b M_ta)`, i.e. 10 % of the catchment's baryons. `N = R_cosmic/f_ret = 53.64` is *derived*
   from it, not a second `f_ret`. A43's "`f_ret = 2.195`" is a different object, `f_s =` cold mass
   over the *system's* cosmic share, and its ceiling of 1 is a denominator, not a physical cap (A47).
   The budget is **available**: 44.1 `M_b` at `10¹¹ M⊙` (82 % of the requirement),
   `N_avail/N_req = 2.38`, so the no-edge tension does not return on the primary range.

2. **A33 §5's first integral is an identity, not a constraint.** It defines `g_N = g − u`; it does
   **not** force `M_src = M_b + M_c`. A33's own partition gives `M_src = M_b + (1−ς)M_c` and §7.3
   forces `ς = 1`, so **`M_src = M_b`** — which is what every SPARC fit assumed. The data select
   baryons-only by **Δχ² = 7.5×10⁴** at the theory's `a₀`. A40's "2.523× defect" claim falls
   (its ratio is really 6.3643, the total-to-baryon mass ratio), and so does A33 §5's sentence.

**Open, precisely**: (1) the one equation for κ — **measured, not decidable, and now obstructed**:
A51's joint fit gives `κ = 0.371 ± 0.119` (total), with ½ at **1.09σ in total error** but **4.9σ
statistically**; 0.4824 and 0.4979 are **undecidable even at N = 1000** (0.15σ / 0.02σ with the
coherent floor; three sigma on 0.4824 needs 6,023 galaxies). And **A62 has closed the three named
derivation routes with exact numbers** — §6.1 below. No route works, so the number stays open *for
the reason that it is κ = ½*; (2) the galactic-regime α₁ — **CLOSED by A82, and the earlier "SURVIVED"
reading is withdrawn**: A36's coefficient does run `0.046–5.19` as computed, but the exact nonlinear BVP
shows the induced acceleration is a radial **monopole**, with the **dipole identically zero** and
`δa ≤ w²a₀ = 1.42×10⁻¹⁶ m/s²`. There is no preferred-frame *observable* at galactic accelerations, so
"α₁ = α₂ = 0" was never false there in a measurable sense; the pulsar prediction `α̂₁ = 3.0×10⁻²⁴` is
19.07 decades inside Shao–Wex. The `513 AU` crossing belonged to the coefficient, not to a measurable
dipole, and is withdrawn with it; (3) the inner `u = 0.47`; (4) `L_*`'s **normalisation** — A65 derives
the *form* `L_* = σ_c²/a₀ = (σ_c/c)²L_MOND` with coefficient exactly 1 and no tuned constant, but the
number is **fitted in normalisation**: 24.025 pc canonical, 23.429 pc thermal, 19.865 pc on P3's
footing (§6.1). A61's `K` question is settled and **its parenthetical reversed**: `K = 4πG → 24.025 pc`,
`K = 8πG → 16.988 pc = λ_P`; (5) a UV completion; (6) **the DOF question is closed, and the answer is benign**: A64 counted 5 modes
against a budget of 4 and graded that a failure; A54's canonical analysis shows 26 dimensions and 8
first-class constraints give **5 DOF**, with the scalar's kinetic coefficient `Q₀ = (2+3β)/(Kβ) + ηk²/K²`
positive **iff `β > 0`** — so all five modes are healthy and the "fifth" is the P longitudinal already
counted among `P_i`'s three components. The budget of 4 was wrong, not the action. **What remains open is
observational, not structural**: the galactic-regime `α₁` is now computed rather than assumed — A82
reproduces the coefficient `0.073–5.194` but finds a **zero dipole** and a monopole bounded by `w²a₀` —
and A55's SLACS shortfall — re-audited by A70 — requires
`M_*/L = 1.174 ± 0.039×` Salpeter, which sits **1.80σ** from the same survey's dynamical IMF calibration
and **inside its 95 % bound by 0.25 %**. So the relativistic sector is internally consistent and
observationally at the edge of one IMF calibration, which is a much sharper statement than a ghost hunt.

**6.1 The four core questions, answered as far as the physics allows.**

**(Q1) Why the vacuum switches at one-twelfth of the horizon scale — RESOLVED: it switches at `1/(2π)` of the de Sitter horizon, and the "twelfth" is `4π = 12.566`.** *Update (A72/A73, 2026-10-22): the coefficient is not `1/Z`. The only derivation in a 260,129-expression census is the thermal wavelength at `T_dS`, `a₀ = c²/λ_T = cH_Λ/(2π)` (mass-independent to 10⁻¹²), which gives `κ_DE = √(2/(3π)) = Z/(4π) = 0.460659` and `2cH_Λ/a₀ = 4π`. The measured `κ_P3 = 0.3777 ± 0.1207` is **0.030σ** from it and 0.299σ from ½; a 2.9 % `a₀` measurement decides. See §3.6.* The text below records why every route to `κ = ½` failed — which is now the point: **½ was the wrong target.** The exact chain is
`a₀/(cH_L) = 2κ/Z` with `Z = 2√(8π/3) = 5.788810`, so **`κ = ½` ⟺ `a₀/(cH_L) = 1/Z = 0.1727473`** —
a fifth of the horizon, not a twelfth. The "twelfth" is `1/(2Z) = 0.0863735 = a₀/(2cH_L)`, i.e. the
ratio to **twice** the horizon scale. And `2Z = 12` **iff `π = 27/8`**, which it is not: the exact gap is
`1/(2Z) − 1/12 = (6−Z)/(12Z) = 3.0402×10⁻³`, and the literal twelfth in κ is `Z/12 = 0.4824008`, 3.52 %
below ½. So `2√(32π/3) = 2Z = Z/κ` is a **rewriting of κ = ½**, not a derivation of it, and A62 shows no
named mechanism produces it: capacity saturation against the horizon **is** the Friedmann equation and
returns `κ = Z/2 = 2.894405` (5.79× dead); the field's own zero-point stress saturates at the **Planck**
acceleration (`4.458×10⁶¹ cH`); a conformal field gives **0** and the trace anomaly `1.672×10⁻⁶³`;
holographic equipartition **is** Friedmann (deficit 0 in dS, `0.4743 cH₀` at `Ω_m = 0.3162`); the
Verlinde volume law gives `κ = 0.583369`; Langevin/Brillouin give exactly `1/(2π) = 0.159155`; Langmuir
exactly `1/Z`, wrong shape *and* scale. **Look-elsewhere, done properly this time: a 156,210-value pool
contains 223 closed forms within 1 % of 2Z, the simplest being `√134` at `1.54×10⁻⁴` (`z = −1.06`) — so
a match is not evidence.** The honest statement is an obstruction. One new falsifiable identity still
falls out: `a₀/(cH₀) = √Ω_Λ/Z` **exactly**, so the `1/7` coincidence to 5.6×10⁻⁴ is **`Ω_Λ = 32π/147 =
0.683827`** against Planck's `0.6847 ± 0.0073` — a 0.13σ agreement that is a *prediction*, not a fit.

**(Q2) What medium produces the saturating term, and does nature pick n = 1 or n = 2.** A63's
admissibility theorem: the medium must supply **rectification**, not saturation — the isotherm needs
`f″(0) ≠ 0` so that `A = g − g²/a₀ + …`. Every **centrosymmetric** saturator (`tanh`, Langevin) is
odd, has `f″(0) = 0`, and gives `g_N ∝ g³` — exponent 3, **no MOND at all**. **Born–Infeld** caps the
*drive* instead of the *response* and anti-screens everywhere. The only serious dielectric rival, a
**biased** non-centrosymmetric `tanh`, matches the deep limit exactly but its capacity is bounded by
`a₀/2` — it cannot reach the observed anomaly. The unique admissible medium is a **one-sided,
hard-core, single-occupancy lattice driven by an activity: the Langmuir gate**, with capacity per
site `q = a₀/N_s` and affinity `a₀`. Given a lattice, **n = 1 is forced twice over** — by `c₂ = −1`
with `C = s = a₀`, and by least dissipation (n = 2 is not a stationary state, A35). The discriminator
is a **sign**, needing no calibration: the occupancy-noise skew at fixed `g_N` is **+0.7071 (n=1) vs
−0.3483 (n=2)** at `g = a₀/2`, zero at `a₀` vs `3a₀/8`, opposite signs on `(0.375,1)a₀`; N ≈
7,000–13,500 points in the window decides it. **Status: DERIVED (medium), UNDECIDED (data).**

> **ERRATUM (2026-10-22, doors push D1):** the skew-sign discriminator is **RETIRED for RAR residuals** (D1 SCOPED NO-GO, `doors_push_2026_10_22/D1_skew_preflight/README.md`). RAR errors (distance, Υ, inclination) are symmetric in log g, and in log g **both laws predict a negative skew** across the whole window g/a₀ ∈ (0.375, 1) (√N_s·skew at a₀/2: n=1 −4.38, n=2 −2.44). The sign difference exists only in linear g, where a 0.06 dex log-symmetric background alone has skew +0.42 and SPARC's measured out-of-window skew is +2.9 (canonical) / +3.2 (alt), 17–50× the best-case signal (+0.062 / −0.165). The Gaussian price is also understated: ~1e4–1e6 points, not 7,000–13,500. The statement above is kept as written; it no longer decides n.

**(Q3) A relativistic version that predicts lensing — the four gates.** Structurally **closed, and the
answer is the opposite of A64's first reading**: A54's canonical analysis gives 26 phase-space dimensions
and 8 first-class constraints, hence **5 propagating modes** — 2 tensor, 2 P-transverse, 1 mixed scalar —
and the scalar's kinetic coefficient `Q₀ = (2+3β)/(Kβ) + ηk²/K²` is **positive iff `β > 0`**, so all five
are healthy. The "fifth" is not extra; it is the P longitudinal already among `P_i`'s three components.
From one premise — the charge `D·P` with unit coefficient in `H_⊥`, no `O(ε)` P term in `H_i`, no
P-curvature coupling — all four gates follow as corollaries: `Φ = Ψ` at `O(ε)` (**lensing = dynamics, a
theorem not an assumption**), `c_T² = 1` to all orders with `m_T² > 0` (**GWs at light speed**, no
tachyon), `dg/dg_N = 1 + a₀²/(g²+2a₀g) ≥ 1` and `c_s² = 1` (**Newtonian Solar System**), and the principal
positivity `β > 2ηa₀²/K` satisfied to one part in 10¹⁸ (**stable at every acceleration**). **Two honest
qualifiers.** First, the galactic-regime `α₁`: A54 did not imply it, and A82 has now computed it — the
coefficient runs to `5.194`, but the induced acceleration is a monopole with **zero dipole**, bounded by
`w²a₀ = 1.42×10⁻¹⁶ m/s²`, so the expansion's failure is harmless. Second, **A55's observational check is an IMF statement, not a falsification** (A70): the required
`M_*/L = 1.174 ± 0.039×` Salpeter sits **1.80σ** from the same survey's dynamical calibration
(`1.00 ± 0.036` dex, 95 % `[0.850, 1.177]`), inside by 0.25 %. A55's 4.9σ came from `1/median²`
(`M₂D ∝ R²`) instead of the model's `dlnR/dlnB = 0.7775`, which overstates the boost by 8 % — the
difference between "excluded at 95 %" and "at the 95 % edge". The theory therefore **passes the four gates
as an internal theorem and needs a heavy IMF for lensing**, with the `R_E/R_e` shape term shown by A80 to be
an `f*`-definition ambiguity rather than a theory failure. **Status: DERIVED (gates), LENSING AT THE IMF
EDGE (1.8σ in the `R_E` channel, 2.3σ with `σ_ap`).**

**(Q4) Where the stiffness length comes from.** `L_* = σ_c²/a₀` — the distance the cold medium
travels at `σ_c` during `t_acc = σ_c/a₀`, the time in which the theory's only acceleration changes the
velocity by one `σ_c`. Equivalently `L_* = (σ_c/c)²L_MOND`, which **explains the nine-decade
hierarchy** rather than fitting it. The guard against constant-juggling was pre-registered (four
criteria C1–C4, written before any number was computed) and **A65 fails its own zero-parameter
standard honestly**: the form is derived with coefficient 1, the number is a one-parameter fit to the
24 pc anchor (`σ_c = 8.33 km/s`), and the independent thermal width gives 23.429 pc — 2.38 % below the
window floor. Label: `FITTED(σ_c) / CONDITIONAL(footing)`. The measurement that would convert it to a
derivation: a **core-independent `σ_c` to ~1 %** at 30–100 pc in a face-on low-mass dwarf.

**What A36's `k` is — and what the hedgehog zero actually covers.** A36 evaluates the gradient
term with the **perturbation's** wavenumber `k = 1/r`, so `(kL_*)²u′/2 ≤ 5.2×10⁻⁶` and `D ≈ 1`
at every galactic radius; its route-(a) numbers *are* the full formula, not a limit of it. The
`α₁ → 8/(kL_*)²` hedgehog zero A22 found is the **other** limit, `kL_* → ∞` at sub-AU scales — a
formal statement about the hedgehog, not a statement about the Solar System's acceleration. The
suppression that actually protects the PPN bound is therefore **one** mechanism, not two:
`u′ = a₀²/(g+a₀)² → 0` when `g ≫ a₀`, which is exactly where every precision test sits. The
O(0.1–5) value needs `g ~ a₀`, and only there does it appear. So A36's headline formula and its
numbers are consistent, and no correction to its coefficient is required — but the paper must say
`k = 1/r` explicitly, because with the P-mass `k = 2π/λ_P` the same expression would give ≈0.10
and the distinction matters for the observable, not for the verdict.

**6.2 The referee's audit — four grades, five conflicts, and one falsifier that fires only on an excluded
footing.** A58 audited the
four answers before they reached this document. The four answers compute cleanly — **34 of 50 ledger
claims are BACKED**, and every re-derivable number agrees with its lane — but they **fail as closure**:
three are status upgrades of a result their own lane did not establish. The document-wide upgrade rate is
24.6 %; the four answers are where upgrade pressure concentrates.

| # | answer | grade | defects | verdict | deciding number |
|---|---|---|---|---|---|
| Q1 | κ = ½ from the horizon | **C** | 3/13 | **WRONG** as derivation | `g(κ=½) = Z = 5.788810` vs `2π = 6.283185`, gap **0.4944** |
| Q2 | the medium and its discriminator | **C** | 5/14 | **OVERSTATED** | Δχ² collapses to **17.05 < 25** when `(A, a₀)` are profiled |
| Q3 | the four gates | **B−** | 4/12 | **OVERSTATED** | **2 premises / 4 gates**; 0/4 testable at present sensitivity |
| Q4 | the origin of `L_*` | **C** | 4/11 | **OVERSTATED** | **6.84 dex** joint miss; `μ = 1.22` vs 1.00 |

Only Q1 is outright **WRONG**: the claim that `a₀/(cH_Λ) = 1/Z` is "a horizon fact that fixes κ" fails
because the horizon's own count gives `g = 5.788810` where `2π = 6.283185` is needed — a gap of 0.4944,
i.e. **7.87 %**, and no matching of the temperature normalisation closes it (A50: the unmatched `λ`
forces either `κ = Z/2 = 2.894405`, 5.79× dead, or `κ = √(3/8π)`, which is not ½). Q2–Q4 are **not wrong
numbers**, they are **overstated closures**: Q2's discriminator needs 7,000–13,500 points and the profiled
Δχ² falls below the pre-registered 25 threshold; Q3's four "independent" gates are two premises and four
corollaries, none testable at present sensitivity; Q4's `σ_c = 8.33 km/s` does not come from the medium at
all, and the joint fit misses by 6.84 dex.

**The four cross-lane conflicts, recorded rather than repaired:**

| conflict | magnitude | consequence |
|---|---|---|
| A51's measured `κ = 0.371` fed into A54's gates | **not a conflict** — `y_t = 118.97`, **INSIDE** [60,140] | the band [60,140] on `y_t` is exactly `κ ∈ [0.3415, 0.5265]`; measured κ sits inside, near the upper edge |
| the `Ω_Λ = 1` footing (`a₀ = 1.132×10⁻¹⁰`) → `κ = 0.605` | **30.6 %** (`y_t` 66.35 → 45.82) | **the falsifier fires only here** — and A51's measurement disfavours this footing at 1.97σ |
| A51's `κ` fed into A56's `L_*` | **17.2 %** (24.03 → 19.90 pc) | still inside A20's 24–90 pc window, but the edge is closer than quoted |
| A50's horizon derivation vs A51's measurement | **circular + blind** | A50's route assumes what A51 measures; no independent check |
| A53's medium vs A56's `σ_c` | **6.84 dex** | the medium supplies no velocity scale; `σ_c` is imported, not produced |

**Correction to the first row, and it matters in the theory's favour.** The "`y_t` 66.30 → 46.01" figure is
**not** what A51's `κ = 0.371` produces. Solving `I(y_t) = 8π/κ²` at each κ gives: κ = 0.5 → `y_t = 66.35`;
κ = 0.371 → **`y_t = 118.97`**; κ = 0.605 → `y_t = 45.82`. So `46.01` belongs to **κ = 0.604**, which is A4's
*alternative* footing, and A58's conflict row conflated "A51's measured κ" with "the Ω_Λ = 1 footing's κ".
The falsifier band [60,140] on `y_t` maps exactly to **`κ ∈ [0.3415, 0.5265]`**. A51's measurement sits
**inside** it: the central value 0.371 gives `y_t = 118.97` (near the 140 edge but inside), and κ = ½ gives
66.35 dead centre. **The falsifier does not fire on the measurement.** It fires only on the `Ω_Λ = 1`
footing, where κ = 0.605 → `y_t = 45.82`. That footing is the one A51's own fit disfavours — 1.97σ high —
so the firing is a property of a footing the data already pushes against, not a verdict on the measured
value. The residual tension is narrower and honest: A51's **lower 1σ edge**, κ = 0.252, gives `y_t = 255`
and does fall outside the band above 140. So the measurement's tail straddles the upper edge while its
centre is inside. §6.1's Q1 verdict remains an obstruction — but as a derivation question about κ, not
because the theory's own prediction is excluded.

**The fifth conflict — three footings for `a₀`, and κ scales linearly with it. The measurement breaks the
tie.** A51's own scripts carry `A0_QUOTED = 1.132e-10` (P3, three-digit) and `A0_THEORY = 0.5 ×
cH₀√(8π/3) = 1.131204e-10`; A54 uses `A0 = 9.36e-11`; A62's "canonical" exact value is `c²√(Λ/32π) =
9.354173e-11`; and A51's SPARC best fit lands at **`8.0815e-11`** — 28.6 % below P3's footing. The reason
is the Λ that enters: `Λ_bare = 3H₀²/c²` gives `a₀ = 1.132×10⁻¹⁰`, while `Λ_obs = 3Ω_ΛH₀²/c²` gives
`9.354×10⁻¹¹`, and the two differ by `√Ω_Λ = 0.8275`. Computing κ on each footing through
`κ = Z a₀/(2cH_Λ)`: the `Ω_Λ = 1` footing gives **κ = 0.6051**, the canonical/`Λ_obs` footing gives
**κ = 0.5000** exactly (by construction — the canonical `a₀` *is* the κ = ½ point), and the SPARC fit's own
minimum gives **κ = 0.4320** (matching A51's `κ_DE = 0.4317`, its `κ_P3 = 0.3572` being the same fit in
the other convention).

**This is not an undetermined ambiguity — the data picks an end.** A51's measured band is
`κ = 0.371 ± 0.119`, i.e. `[0.252, 0.490]`. That band **contains** the canonical κ = 0.500 (marginally, at
the upper edge) and the fit's own κ = 0.432, but it **excludes** the `Ω_Λ = 1` footing's κ = 0.605 at
**1.97σ**. So the measurement already discriminates: the footing that fires the falsifier is the footing the
data disfavours. What remains genuinely ambiguous is only the 0.432–0.500 range, and that span
(`y_t` 88.3 → 66.4) is comfortably inside [60,140] throughout. The spread of all three footings, factor
1.40, is *comparable to but contained within* A51's own 32 % relative error bar — so it is not an
additional independent systematic above A51's, it is a component of the same uncertainty. The honest
statement: the theory's `a₀` is only defined once you choose `Λ_bare` vs `Λ_obs`, and A51's κ measurement
prefers `Λ_obs` at 2σ — which is exactly the choice under which the falsifier does not fire.

**RESOLVED (2026-10-22, A78): the footing war is over, and BBN won it.** With matter included, β = 0 sits
exactly at `Λ_bare = Λ_obs` (not `1.462Λ_obs` — A33's number came from dropping `ρ_m`); and
`Λ_bare = Λ_obs(1 + 2.194β)` with the BBN bound **β < 0.027** gives **`Λ_bare/Λ_obs ∈ (1.000, 1.061)`**.
The P3 footing (`ρ_bare = ρ_crit`, `a₀ = 1.132×10⁻¹⁰`) needs β = 0.210, i.e. `ΔN_eff = −2.34` — **≈8σ
excluded**. So `a₀` survives only in **`8.63–8.89×10⁻¹¹`**, and the thermal value `8.62×10⁻¹¹` sits at its
lower edge. The "factor 1.40 spread" recorded above is history, not an open conflict.

---

**6.3 The global consistency test — one parameter set, three channels, and a convention trap (A71).**
The capstone fit: SPARC (171 galaxies / 3375 points), the corrected SLACS sample (70 lenses with A70's
model and Treu's IMF prior), and A18's clusters, sharing `κ`, the IMF normalisation `B`, and `u`, with one
`Υ` per galaxy profiled (28/28 checks, 16 mutations each exit 1).

**Joint result.** `κ_P3 = 0.3777 ± 0.0258 (stat) ± 0.1179 (syst)`, i.e. `a₀ = 8.544×10⁻¹¹`;
`B = 1.1916 ± 0.0364` (**+1.97σ** above Treu's mean); `u = 0.4427`. Per-channel `χ²/dof`: SPARC
`7136.35/3204 = 2.227`, SLACS `61.75/68 = 0.908`, clusters `0.08/1`. **One parameter set fits at
1.89σ (`p = 0.058`) — but 4.47 of the 5.69 tension is the IMF prior alone; data-only `T = 1.21` (0.6σ).**
Pulls: SPARC `−0.61σ`, clusters `+0.37σ`, SLACS `κ +1.97σ`, `B +1.97σ`.

**The convention trap, and it matters more than the fit.** "κ = ½" means different `a₀` depending on which
density enters `a₀ = κc√(Gρ)`. The two differ by `√Ω_Λ = 0.8276`:

| convention | `a₀` at κ = ½ | `κ` at `a₀ = 9.36×10⁻¹¹` | `κ` at `a₀ = 1.1312×10⁻¹⁰` |
|---|---|---|---|
| `ρ_DE` (observed Λ) | **9.36×10⁻¹¹** | 0.500 | 0.604 |
| `ρ_crit` (bare, P3) | **1.1312×10⁻¹⁰** | 0.414 | 0.500 |

The joint fit is **1.40σ (stat) / 0.30σ (total)** from the canonical `a₀ = 9.36×10⁻¹¹` and
**4.74σ / 1.01σ** from the P3 `a₀ = 1.1312×10⁻¹⁰`. Both sit inside the *total* 95 % region; only the
canonical one is inside statistically. The two footings are **3.35σ apart** at joint precision, so the data
do discriminate — **in favour of `a₀` from the observed Λ**. This is consistent with A33's independent
constraint that the action's *bare* `Λ` must be `≥ 1.462 Λ_obs` for `β > 0`: the bare `Λ` and the `Λ` in
`a₀` need not be the same quantity, and the data side with the observed one. The fit cannot *prove* that
identification — only show which one the data prefer.

**A71 vs A70, explicitly — and A80 has settled it.** A70's "`Δχ² = 0.26` over `κ ∈ [0.20, 0.80]`" is a
*mean-only* statement. A71's **`Δχ² = 6.35`** was reported as scatter/shape information "unusable without
per-lens Sérsic `n`". **A80 shows that was the wrong diagnosis**: A71's `SD_TAB` is built at `boost = 1.0`,
i.e. with `B` *not* actually profiled. Reproducing A71's table exactly (63.29 → 56.94) and then profiling
`B` gives **54.53 → 54.50, `Δχ² = 0.29`** over the same band. **The 6.35 was an unprofiled-`B` artifact, not
a Sérsic degeneracy, and SLACS carries essentially no κ information.** With `(B, n)` jointly profiled the
residual rises to 3.53 (free `n`) / 2.80 (`n = 5.2 ± 0.8`), minimised at the `κ = 0.80` edge where `B` is
`−2.93σ` from Treu — a prior-dominated fit, not a measurement. A70's *verdict* stands at `κ = 0.5`; its
*number* does not transfer.

**The IMF tension gets slightly worse, not better.** At the joint `κ = 0.3777`, SLACS demands
`B = 1.2248`, while the posterior compromise is `1.1916` — **outside Treu's 95 % bound `1.1767`**
(1.97σ, up from A70's 1.80σ). Relieving it needs `κ = 0.4928`, a +4.5σ shift.

**The `σ_ap` channel does not rescue it (A85, 32/32, 8 mutations).** Adding the on-disk SDSS aperture
dispersions — the test that should break the `B`–`κ` degeneracy — does not:

- **Route 1 (zero free normalisation).** With each lens's `B_i` fixed by `R_E` alone, the spherical Jeans
  solver predicts `σ_ap` **2.33 % low** (`−0.0103 ± 0.0065` dex, **1.58σ**) with **13.3 %** per-lens scatter.
  Lensing mass = dynamical mass at the few-% level with no dark particle — but the 2.3 % is fully absorbed
  by `n₀ = 4.74` **or** `β_ani = +0.223`, neither measured, so it is not evidence either way. **The 13 %
  scatter is.**
- **Route 2 (shared `B`).** `B = 1.2269 ± 0.0043 (formal) ± 0.0106 (scaled)`, **2.27σ** above Treu —
  *worse* than the 1.97σ of the `R_E`-only fit, because dynamics pushes `B` up while lensing alone does not.
- **The degeneracy is not broken.** `dlnσ/dlnκ = 0.0345` vs `dlnσ/dlnB = 0.4706`, ratio **0.0732** —
  *smaller* than the lensing ratio 0.1550, so the two constraints are nearly **parallel** (3.08° apart,
  Fisher condition number **746**). `σ(κ)` improves `0.629 → 0.268`, still **10× A71's statistical error**.
  The exact profile prefers `κ = 1.10` at `Δχ² = −28.4`, but that channel sits at `χ²/dof = 8.13`; rescaled
  to 1 it is `Δχ² = 2.96`, under 3σ. **It neither confirms nor kills A71's 6.35** — SLACS stays κ-blind
  without per-lens Sérsic `n` and better `σ` errors.

**The final joint fit confirms rather than moves it (A81, 27/27).** Re-running all three channels with
**every** parameter profiled at every grid point — the defect A71 had — gives `κ_P3 = 0.3781 ± 0.0258 (stat)
± 0.1180 (syst)`, `a₀ = 8.554×10⁻¹¹`, `B = 1.1996`, `u = 0.4429`, global tension **1.854σ**, of which the
IMF prior supplies `4.97` and the data only `0.53` (**0.298σ**). Head-to-head, the thermal point beats
`κ = ½` by `Δχ² = 1.8245` → **1.351σ, LR 2.49 : 1**. Removing SLACS from the fit moves κ by `+0.0066`
(0.26σ of the joint error) and SLACS alone gives `κ = 0.979 ± 0.312` — it runs to the edge, as a κ-blind
channel should. The three independent lensing solvers now agree on the shared IMF at
`B = 1.2280 / 1.2269 / 1.2365` (A80/A85/A81, spread 0.8%), and the ledger resolves to **2 independent free
parameters** — one P-sector scale plus `η` — with `a₀` on the postulate and `β` BBN-bounded.

**What would settle it:** a wide-binary `γ_v` measurement at 18–22 kAU — A24's 4.5σ EFE test — cuts the
joint κ error from **0.1207 to 0.0605**, 3.7× the reduction of SPARC at `N = 1000` (which buys only 2 %).
Two honest gaps: the SLACS shape channel carries **no** usable κ information — A80 shows its 6.35 was an
unprofiled-`B` artifact (`Δχ² = 0.29` with `B` profiled) and the `R_E/R_e` residual is an `f*`-definition
ambiguity rather than a theory failure; and the wide-binary forecast is a rescaling of A24's σ's, not a
re-solve.

---

## 7. What this is, and what it is not

**It is** a closed effective theory: a single action, five postulates, and a **computed** five-mode
spectrum — 26 phase-space dimensions, 8 first-class constraints, **0 second-class**, `(26−16)/2 = 5`
(A68, 39/39 checks with the bracket computed rather than asserted). The fifth mode is the mixed
conformal/P-longitudinal scalar, **gapless** (`m² = 0`, `c_s² = αp²/Z → 0`, a `k⁴` mode) and healthy
for `β > 0, η > 0, α = γ > 0`; its strong-coupling scale is `2.836×10⁻⁶⁹ eV = 1.9×10⁻³⁶ H₀` — a
**deep-infrared** scale, so every mode inside the horizon is weakly coupled, and no UV statement follows
either way (A57: this is not a UV completion). Rotation curves: `χ²/dof = 2.227` on 171 SPARC galaxies with
one stellar M/L each (A71), degenerate with the rival interpolation on total `χ²` and separated from the
quadrature kernel by a shape test at **`Δχ² = 158.0` (canonical footing) / `75.3` (alt)** with no free
parameters (**A25**, not A63 — the footing dependence is A25's). The four gates are an internal theorem: `Φ = Ψ` at `O(ε)`,
`c_T² = 1` exactly, `α₁ = α₂ = 0` with `β_PPN = 1` wherever `kL★ ≫ 1`, `dg/dg_N ≥ 1` at every
acceleration (A54, A68, A69).

**The joint fit says one parameter set is enough.** SPARC + corrected SLACS + clusters, sharing κ,
the IMF normalisation and `u`: **`κ_P3 = 0.3777 ± 0.1207`, `B = 1.1916 ± 0.0364`**, global tension
**1.89σ** — of which **4.47 of 5.69 is the IMF prior alone**; data-only `T = 1.21` (0.6σ). **A81's re-fit
with every parameter genuinely profiled reproduces it: `κ_P3 = 0.3781 ± 0.0258 ± 0.1180`, tension
1.854σ, data-only 0.298σ, `Δχ²`(thermal − ½) = 1.8245 → 1.351σ.** The
lensing "4.9σ failure" is gone: it was `1/median²` instead of the model's `dlnR/dlnB = 0.7775`,
corrected to **1.8σ at the 95 % edge** of the same survey's dynamical IMF calibration (A70).
**That statement is about the `R_E` channel, and only it.** Adding the on-disk `σ_ap` dispersions (A85)
does not break the `B`–`κ` degeneracy — the two constraints are 3.08° apart — and pushes the best-fit IMF
to `B = 1.2269`, **2.27σ** above Treu. So "one parameter set" covers `R_E` + SPARC + clusters; the
dynamics channel is a **2.3σ pull, not a confirmation**, and the 1.89σ global number does not include it.

**Parameter content (corrected 2026-10-22, following A81's ledger).** An earlier version of this
paragraph said "κ is derived" and counted "0 free dimensionless numbers, 2 free scales, 1 measured
fraction, 1 premise, against ΛCDM's six parameters". That overstated it. The honest count:

| class | items | source |
|---|---|---|
| **one dimensionless coefficient, not derived** | κ: fitted (`½`), or set by the P-therm postulate `a₀ ≡ cH_Λ/2π` (`Z/4π = 0.460659`, Milgrom's relation — §3.6). A75 proves P-therm independent of the action; A81 separates the two values at 1.35σ (bootstrap errors) | A72, A75, A81 |
| **two free parameters** | `η`, and one P-sector scale shared by `γ = KL★²/2`, `L★` and `σ_c` (one degree of freedom, A81 rank test). `L★` has the form `σ_c²/a₀` but no measured `σ_c` (A76); `η/γ` has no matching principle (A77) | A76, A77, A81 |
| **bounded** | `β < 0.027` (BBN), hence `Λ_bare/Λ_obs < 1.061`. This also excludes the old P3 footing (`β = 0.21`) at ≈8σ | A78 |
| **measured fractions** | `u ≈ 0.47` inside splashback (mechanism open), the cold share `Ω_c/Ω_b` | P4 |
| **background inputs** | `Λ`, `H₀` and the rest of the cosmological background, taken from data | P3, A46 |
| **posited forms** | the strong-field turn-off (P5). `y_t` then follows from κ and the observed `Λ` through the closure `I(y_t) = 8π/κ²` | P5, §3.6 |

So the comparison with ΛCDM is not "a handful against six": this theory **uses** the ΛCDM background
parameters and adds κ, two free scales and the measured fractions on top of them, in exchange for galaxy-scale
predictions that ΛCDM does not make: the RAR shape, lensing = dynamics,
`c_T = 1` (speed), `α₁ = α₂ = 0` near-source, `β = 1`, the core size, the saddle no-go.

**It is not** a UV completion, and §3.6 proves the difference is not a gap in the search but a
property of the system: `L★` and `η/γ` are **two independent UV inputs**, and A69 shows nothing in
the action ties `η` to `γ`. The honest summary is: **one dimensionless coefficient (κ: fitted at ½, or
`Z/4π` by a postulate), two free parameters (`η` and one P-sector scale), one bounded (`β`), measured
fractions (`u`, `Ω_c/Ω_b`) and the ΛCDM background.** κ = ½ and the thermal `Z/4π` differ by 7.9 % and the
data separate them at only 0.27σ in A71 (0.030σ vs 0.299σ) and 1.35σ in A81, so **a 2.9 % `a₀`
measurement lands on `8.626×10⁻¹¹` (P-therm) or `9.355×10⁻¹¹` (κ = ½)** — that is the falsifier. What would: a wide-binary `γ_v` measurement at 18–22 kAU, which cuts the joint κ
error from 0.1207 to 0.0605 (A71), and a homogeneous spectroscopic IMF for the 70 SLACS lenses at
`R_E/2–R_E` to ≤ 0.03 dex.

**And the audit is part of the result.** A31 found **32 defects in 130 claims** in the document
this replaces, and A32 independently re-derived four core results from the equations alone — all
four matched. The corrected numbers are the ones used here.

---

## 8. Reproduce

```bash
cd deepseek_push/DS_FINAL_2026_10_21
python3 _parent/parent_audit.py            # 21/21, independent
python3 _parent/closure_theorem.py         # 8/8, P-sector closure + kappa modulus
python3 _parent/a3_gw_certificate.py       # 6/6, c_T^2 = 1
python3 _parent/a22_no_cosmic_aether.py    # 4/4, no cosmic aether
python3 _parent/theory_prediction.py       # 4/4, zero-parameter galaxy prediction
for d in A*/; do (cd "$d" && python3 *_checks.py); done
cd A8_lean && for f in A8_C*.lean; do lake env lean "$f"; done
```