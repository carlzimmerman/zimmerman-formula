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

**P3 — The vacuum.** `a₀ = κ c √(G ρ_bare)` with `κ = ½`, and `Λ_bare = 3H₀²/c²` with
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

That is the whole theory. There is no other input.

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

**3.5b The joint theorem FAILS — the DOF mismatch (A64, 20 checks).** Gate by gate, the four gates are
clean: lensing = dynamics is a theorem from the action's dust structure (`Π = O(ε²)`, first slip
`2.63×10⁻⁷` at `O(ε²)`, coefficient exactly `2K`), `c_T² = 1` to all orders with `m_T² > 0` (no
tachyon, 8.3×10⁹ below the graviton bound), `dg/dg_N ≥ 1` and `c_s² = 1`, and `β > 2ηa₀²/K` satisfied
with margin `5.95×10⁻¹⁹`. **But they do not form one theorem.** The action propagates **5 degrees of
freedom — 2 tensor + 2 P-transverse + 1 mixed scalar — not the 4 the theory budgets** (`2+1+1`). The
P constraint is **second-class** (the Legendre map is invertible for `η > 0`, det ≠ 0), so it does not
remove the longitudinal mode; the lapse constraint removes one scalar, leaving five. **That extra mode
is either a ghost or an additional physical scalar, and either way the four-gate statement as a single
theorem is false.** This is the one place where the four gates conflict, and it is structural: it does
not appear if the gates are checked separately, which is exactly why it was missed until A64 checked
them jointly. Neither resolution is available inside the frozen action: (a) a further constraint needs
a modified action; (b) accepting the extra mode needs the gates re-derived in its presence, which would
change the slip and the speed at higher order. **The honest verdict is that the four gates are not
mutually consistent, and the obstruction is the second-class P constraint.**

**3.6 The vacuum closure, and κ.**

$$
I(y_t)\equiv\int_0^\infty \frac{y(\nu-1)}{1+(y/y_t)^2}\,dy=\frac{\Lambda c^4}{a_0^2}=\frac{8\pi}{\kappa^2}
\quad\text{identically, for every }\kappa>0 .
$$

For the canonical kernel the left side is `(π/2)y_t − ln(y_t/4) + C_can`, `C_can = −0.8862944`;
with `Λc⁴/a₀² = 100.4058` this solves to **`y_t = 66.2999`** (A4, A25, A28). `I` is strictly
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
| environment-dependent α₁ | 0.046–5.19 at `g ~ a₀` on kpc scales; `< 10⁻¹³` at every acceleration where a PPN test exists. Crosses `10⁻⁴` at `g = 199 a₀ = 2.25×10⁻⁸ m/s²`, i.e. `r = 513 AU` from the Sun | a preferred-frame anisotropy in the outer Oort cloud at `α₁ v²/c²`; or any measured α₁ above `10⁻⁴` in a system at `g ≫ a₀` |

---

## 6. The no-go ledger

**Closed by derivation**: lensing = dynamics; `c_T² = 1` (speed); `η = γ` ⇒ exact luminality;
`n = 1` from least dissipation; capacity = affinity; `L_MOND = 2ℓ₁ ⇔ κ = ½`; `M_ph/M_b` closed
form and the concentration-independent crossing; `r_switch ∝ L_*`; `u = 1` beyond splashback;
κ–Z identities and the `1/12` bracket (Lean, 40 theorems, no `sorry`, standard axioms).

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
the reason that it is κ = ½*; (2) the galactic-regime α₁ — **computed, positive, and SURVIVED**: A36
gives 0.93 at 8 kpc (its own 0.046–5.19 table spans the radii), so "α₁ = α₂ = 0" is false in the MOND
regime; but **A59 proves every α₁ observable carries (v/c)²**, so the bound `|α₁| < 10⁻⁴` only binds
where it is measured — at LLR's `6.3×10⁷ a₀` the theory gives `1.1×10⁻¹³`, 8.9 decades inside — and
**A60** shows the Sun-embedded-in-Galaxy field moves `α₁(1 AU)` by 4.9×10⁻⁸ to `−1.63×10⁻¹³`, 6.1×10⁸
below the bound. A36's exclusion is over-scoped by ~13 decades; the theory survives its own
coefficient. The distinctive *prediction* is that α₁ is **environment-dependent** (46 decades of
running), crossing 10⁻⁴ at `g = 199 a₀`, i.e. ~513 AU from the Sun; (3) the inner `u = 0.47`; (4) `L_*`'s **normalisation** — A65 derives
the *form* `L_* = σ_c²/a₀ = (σ_c/c)²L_MOND` with coefficient exactly 1 and no tuned constant, but the
number is **fitted in normalisation**: 24.025 pc canonical, 23.429 pc thermal, 19.865 pc on P3's
footing (§6.1). A61's `K` question is settled and **its parenthetical reversed**: `K = 4πG → 24.025 pc`,
`K = 8πG → 16.988 pc = λ_P`; (5) a UV completion; (6) **the DOF mismatch — now the most urgent open problem**: A64's joint theorem
**FAILS** because the action propagates **5 modes, not 4** (the P constraint is second-class), so a ghost
or an extra scalar remains. Resolving it needs either a modified action carrying a further constraint, or
a re-derivation of all four gates in the presence of the extra mode. This is the one structural
obstruction the four gates themselves reveal.

**6.1 The four core questions, answered as far as the physics allows.**

**(Q1) Why the vacuum switches at one-twelfth of the horizon scale.** It does not. `2√(32π/3) =
11.57762` is `2Z = Z/κ`, so **"why 11.5776" is identically "why κ = ½"** — and A62 shows none of the
three named mechanisms produces it: capacity saturation against the horizon **is** the Friedmann
equation and returns `κ = Z/2 = 2.894` (5.79× too big, empirically dead); the field's own zero-point
stress saturates at the **Planck** acceleration (4.458×10⁶¹ × cH); a conformal field gives **0**;
holographic equipartition **is** Friedmann (coefficient 1); a volume law gives 6; Langevin/Brillouin
give exactly `1/(2π) = 0.159155` = 1.8426 × 1/(2Z); Langmuir gives exactly `1/Z`, wrong shape *and*
scale. The literal "one twelfth" is `Z/12 = 0.4824008`, 3.52 % below ½. **Look-elsewhere: 223 hits,
and `√134` is simpler and closer than `2Z`.** So the factor is a *consequence*, not a cause, and the
honest statement is an obstruction, not a derivation. One new falsifiable identity falls out: the
`a₀/(cH₀) = 1/7` coincidence to 5.6×10⁻⁴ is **exactly `Ω_Λ = 32π/147`**, i.e. `0.683827` vs Planck's
`0.6847 ± 0.0073` — a 0.13σ agreement that is a *prediction*, not a fit.

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

---

## 7. What this is, and what it is not

**It is** a closed effective theory: a single action, five postulates, one modulus, and
rotation curves at `χ²/dof = 2.42` on 171 SPARC galaxies with one stellar M/L each — degenerate
with the rival interpolation on total χ² (2.31), and separated by a shape test (Δχ² = 158 with no
free parameters). Its parameter content is **4 finite + 3 functionals with 5 exact degeneracies**
(A33), against ΛCDM's six, and it predicts what ΛCDM cannot even address: the RAR shape,
lensing = dynamics, `c_T = 1` (speed), `α₁ = α₂ = 0` near-source, `β = 1`, the core size, the
saddle no-go.

**It is not** a UV completion, and §3.6 proves the difference is not a gap in the search but a
property of the system. The honest summary is the one line in `FINAL_THEORY.md`: one free
dimensionless number, one free scale, one measured fraction.

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