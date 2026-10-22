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

**P3 — The vacuum.** `a₀ = κ c √(G ρ_bare)` with `κ = ½`, and `Λ_bare ≥ 3H₀²/c²` (forced by
`β > 0`, §4.4). Since `ρ_bare = ρ_DE/Ω_Λ`, this gives **`a₀ = 1.132×10⁻¹⁰ m/s²`** — the theory's
own value, not fitted to galaxies.

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

**3.5 The four gates.**

| gate | result | provenance |
|---|---|---|
| lensing = dynamics | `Φ = Ψ` at O(ε); `(Φ−Ψ)/Ψ = O(Ψ) = 2.63×10⁻⁷`; first slip is second order. The sector is a **charge** sector: exactly one O(ε) lapse source, so the stress is dust at leading order | A12, A3, A32 (clean room) |
| GW speed | `c_T² = 1` **exactly** for the speed. Off the `P̄=0` background the mode also acquires a **mass** — a mass, not a speed | A3, A31 (check 28) |
| Solar System | α₁ = α₂ = 0, β = 1 **for `r ≪ λ = 17 pc`**; the galactic-regime α₁ is **not computed** (A36). Kernel anomaly `a₀ = 2557 B_E` uncured; `y_t = 66.30` closes Λ and lets all planets pass with 9.14× margin; P adds `a_P = GM/L_*² = 6.61×10⁻³ B_E`, unobservable (0.17σ) | A22, A4, A30 |
| stability | `dg/dg_N ∈ [1,∞)` at every acceleration; `c_s² = 1`; principal positivity `β > 2ηa₀²/K` | A4, A3, §3.4 |

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

**Open, precisely**: (1) the one equation for κ; (2) the galactic-regime α₁; (3) the inner
`u = 0.47`; (4) `L_*`'s microscopic value (24–90 pc under `f_c→1`, up to 180 pc at `f_c=0.25`);
(5) a UV completion.

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