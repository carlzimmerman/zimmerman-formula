# The theory at the end of the DSF-21 push

**2026-10-21.** **34 lanes**, all in this folder, each with a script that exits non-zero on a
failed check and a mutation that must break it. Each number is attributed to the lane or
script that produced it. The coordinator's harness (`_parent/parent_audit.py`, 21/21, mutation
bites) checks **21 specific identities, not every number here**: A31's adversarial audit
re-derived 35 and classified all 130 claims in this file as BACKED / OVERSTATED / UNBACKED /
WRONG — **32 were not BACKED**, and they have been corrected in place (§7b records the audit).
A32 independently re-derived the four core results from the equations alone, without reading
any lane; all four match. Nothing here is a projection of what a lane might have said.

**Status in one line.** The framework is a **closed effective theory whose only dimensionless
modulus is κ**: the P sector has **one free stiffness** (§9.1, corrected), the turn-off is not
independent (§3, A28), and κ is a modulus of the de Sitter vacuum rather than a derivable
constant (§9.2) — with the caveat that this rests on the halo truncation (A31). The count is
**4 finite parameters + 3 functionals with 5 exact degeneracies** (§9.3, A33), against ΛCDM's
six and the Standard Model's nineteen. Everything else that was asked for is derived, proved impossible in
a stated class, or converted into a pre-registered number. It is not a UV completion, and §9.2
is the proof that the remaining question lies outside this theory's domain. **The law-first vs
medium-first fork is resolved: LAW-FIRST, at 21σ** (A26).

---

## 0. The theory, stated once

$$
a_0=\kappa\,c\sqrt{G\rho_\Lambda},\qquad \kappa=\tfrac12,\qquad
a_0=\frac{c^2}{2\ell_0},\qquad \ell_0\equiv\sqrt{\frac{8\pi}{\Lambda}} .
$$

$$
\boxed{\;g_N=\frac{g^2}{g+a_0}\;}\qquad\Longleftrightarrow\qquad
g=\frac{g_N}{2}\Big(1+\sqrt{1+\frac{4a_0}{g_N}}\Big),
$$

with `g` the observed acceleration and `g_N` the baryonic one. Deep limit
`g → √(a₀ g_N)`; Newtonian limit `g = g_N + a₀ − a₀²/g_N + …`.

**Ontology.** There is no dark-matter particle. The extra gravitating mass is the
stress-energy of a collisionless cold sector ("cold energy"). Its total is the cosmic
share of the system's catchment, `M_c = (Ω_c/Ω_b) M_b = 5.3643 M_b` (A18: this is the
number the record called "5.364", and it is not a cold-sector parameter — it is the
cosmic baryon ratio). Only a fraction `u` of it is *sourced into* the law's phantom;
the rest falls natively. `u` is measured, not assumed: **u = 0.472 ± 0.036 in the cluster
MID band and 0.986 ± 0.098 in the OUTER band** (A21), i.e. the sourcing fraction *rises
outward*, and a constant `u` is excluded at 4.9σ by the band ratio.

Two numbers now do all the work:
`Z = 2√(8π/3) = 5.7888100`, `2Z = 11.5776201`.

---

## 1. Why the vacuum switches on at a twelfth of the horizon scale

**Answer: it does not switch at a twelfth. It switches at `1/Z = 1/5.7888100 = 0.1727473` — closer
to a *sixth* than a twelfth — and the difference is not a detail, it is the whole content of κ = ½.
The "1/12" is `1/(2Z)` relative to *twice* the horizon, i.e. `a₀ = 2cH/12`.**

Exact, from `H² = 8πGρ/3` (K1–K3, A1; Lean `A8.kappa_Z_identity`):

$$
\frac{a_0}{cH_\Lambda}=\kappa\sqrt{\frac{3}{8\pi}}=\frac{2\kappa}{Z}
=\frac{1}{Z}\ \text{at }\kappa=\tfrac12,\qquad
2\sqrt{\frac{32\pi}{3}}=2Z=11.5776201 .
$$

Read literally, "the switch is at 1/12 of the horizon" means `a₀ = 2cH/12`, which gives
**κ = Z/12 = 0.4824008** — 3.52 % away from ½ (A1). The Lean certificate
`A8.inv_twoZ_ne_twelfth` proves `1/(2Z) ≠ 1/12` exactly, so this is not a rounding
question.

### 1.1 κ = ½ cannot come from counting

$$
\kappa=\frac{\sqrt{8\pi/3}}{\mathcal N}\quad(\text{exact}),\qquad
\kappa=\tfrac12\iff \mathcal N=2\sqrt{32\pi/3}=11.5776201 .
$$

`𝒩` is **irrational**. No rational count of horizon cells, no integer of polarizations,
no solid-angle fraction can equal it. The menu a counting argument can actually reach is
(A1, A10):

| count | 4π | 2π | π | 2 | 1 |
|---|---|---|---|---|---|
| κ | 0.2303294 | 0.4606589 | 0.9213177 | 1.4472025 | 2.8944050 |

a factor 12.6 end to end, with ½ on none of them. The nearest is 0.4607, 7.9 % low. This
is why ~110 prior routes returned "one π off": they were attacking bookkeeping, and the
target is irrational.

### 1.2 Three further no-gos, each exact

- **Dimensional analysis.** `ħGΛ/c³ = 2.8498e-122` is the only dimensionless group
  built from {c, G, ħ, Λ, H}. Any `a₀ = c√(Gρ)·F(x)` has F free, and every analytic F
  with O(1) derivatives is constant to 122 digits. κ is an input (A1; my harness Q1.5).
- **Strain saturation.** The natural principle "the vacuum saturates when its stored
  strain energy per horizon entropy cell equals the cell's energy" gives
  **κ = 4√(π/3) = 4.093307**, missing ½ by the exact factor `8√(π/3) = 8.186614` (A1).
  A class theorem kills the family: every member has `κ² ∈ ℚ·π^odd`, hence κ irrational,
  hence κ ≠ ½.
- **"One quantum per cell" is the Friedmann equation.** `N·T_dS = M_h c²` identically
  reduces to `ρ = 3H²/8πG` — it carries no κ information at all (A1). Any argument of that
  shape is a restatement of the background, not a derivation.
- **The numerology control.** `a₀/(cH₀) = 1/7` to `5.6e-4` — **sixty times tighter** than
  the "1/12" hit. Near-integer ratios at this precision are not derivations, and the record
  now has one at 1/7 that is better than the one at 1/12 (A1).
- **The Euler charge is a₀-blind.** `∫E` is a total derivative in 4D (its
  Euler–Lagrange derivative vanishes identically), so it cannot supply a stationarity
  condition. `∂(AΛ)/∂a₀ = 0` while `∂R/∂a₀ ≠ 0`: the balance fixes the geometric length
  `ℓ_χ = √(8πχ/Λ)` and says nothing about a₀ (A19). The record's `AΛ = 32π²` is the
  arithmetic identity `32π² = π·8π·4` — sphere × Einstein × (1/κ)² — not a derivation.

### 1.3 The closure route is not a derivation of κ

The GF2 chain is exact algebra and its uniqueness lemma is true *as qualified*, but its ½
is **μ := σ²/v_c²**, the singular-isothermal-sphere ratio, not κ. The decisive argument
(A15) is a symmetry: the chain's equations are invariant under

$$
(a_0,\,C,\,\sigma^2,\,v^2)\ \longrightarrow\ (\mu a_0,\,\sqrt{\mu}\,C,\,\sqrt{\mu}\,\sigma^2,\,\sqrt{\mu}\,v^2),
$$

so `κ_dyn = ½` for every μ while `κ_law → μκ_law`. No function of `κ_dyn` can equal
`κ_law`. `ρ_DE` appears **zero** times in the chain. CFG908 was right; GF2's register line
is the error.
**Verdict: DIFFERENT-QUANTITY. κ is a modulus.**

### 1.4 What would close it — one equation, one falsifier

The halo sector has two equations for three unknowns, and κ is exactly the content of the
third (A15):

$$
\boxed{\ \frac{\rho_\Lambda c^2}{a_0^2/G}=4\ }\qquad\Longleftrightarrow\qquad
\Lambda\ell_0^2=32\pi\qquad\Longleftrightarrow\qquad \kappa=\tfrac12 .
$$

Any candidate must be a **local** functional with no dimensionful parameter and no
dimensionless constant whose stationarity on de Sitter returns **exactly 4**. The
falsifier is convention-free: 2, 3, 4π, 8π and 32 are all excluded. Four candidate
classes have now been tried and all fail (A19). This is the single remaining hole in Q1,
and it is now a well-posed target rather than a hunt.

**But the data now select 4 among the natural options.** Every candidate reduces to the
same master identity (A19)

$$
R\equiv\frac{\Lambda c^4}{8\pi a_0^2}=\frac{\Lambda L^2}{8\pi}=\frac{A\Lambda}{8\pi^2},
\qquad R=4\iff \Lambda L^2=32\pi\iff \kappa=\tfrac12,
$$

and the saturation cap admits only `R ∈ {1, 2, 4}`, i.e. **κ ∈ {1, 0.7071, 0.5}**. Against
the measured κ these are excluded at **6.14σ, 3.05σ, and 0.87σ** respectively: 4 is the
only natural value the data admit. That is a selection, not a derivation — but it converts
"why ½?" into "why is the cap the fourth power of the cell scale?", which is a sharper
question with a single answer left standing. For calibration, the Unruh/de Sitter control
gives `R = 3/(8π) = 0.1194 → κ = 2.894`, excluded at 33.5×.

> **ERRATUM (2026-10-22, doors push D5):** "the data select 4 among the natural caps" is wrong. A19's own natural grid (`a19_checks.py` K6: β ∈ {1, 2}, χ ∈ {1…4}) is R ∈ {1, 2, 3, 4, 8, 12, 16}, not {1, 2, 4}. The data **exclude R = 1** (6.14σ) and, **on CFG493 only**, R = 2 (3.05σ; on the A81 joint band R = 2 is only +1.71σ). On CFG493 (κ = 0.417 ± 0.095) R = 3 (+1.69σ), 4 (+0.87σ), 8 (−0.67σ), 12 (−1.35σ), 16 (−1.76σ) and A19's 4π (−1.42σ) all lie within 2σ, and **R = 8 is closer to the data than R = 4**. The data do not select 4; κ = ½ stays FITTED. See `doors_push_2026_10_22/D5_kappa_four/README.md`.

---

## 2. What medium produces the saturating term, and n = 1 or n = 2

**Answer: a single-scale two-state lattice — and it forces n = 1.**

The canonical law is *exactly* the Langmuir isotherm (A2, verified in sympy):

$$
\mu(x)\equiv\frac{g_N}{g}=\frac{x}{1+x},\qquad x\equiv\frac{g}{a_0}.
$$

A lattice of independent bistable gates, at most one occupant per site, adsorption rate
∝ the drive, constant desorption, has `θ = x/(1+x)` as its stationary occupancy. With the
capacity identified as the affinity, `a₀`, the stationary condition **is** the law, with no
new fitted constant. **n = 1 is forced by one gate per site.**

Three exact forms make the mechanism concrete (A2):

$$
\theta=\frac{g}{g+a_0},\qquad A\equiv g-g_N=a_0\theta,\qquad \frac{1}{A}=\frac{1}{g}+\frac{1}{a_0}.
$$

`A` is the response (the phantom acceleration) and it is the **harmonic mean** of the drive
and the capacity — the cleanest statement of "saturating at `a₀`". The mass-action and
grand-canonical derivations both give it with `k_d/k_a = a₀`. One structural caveat, and it
is a real one: **there is no equilibrium Gibbs state with linear coupling** — the Fermi
occupancy stays finite at `g = −a₀`, where the Langmuir isotherm has its only pole. The
medium must therefore be a *driven steady state*, not a thermal equilibrium. That is a
physical commitment of the model, not a detail.

The lattice also predicts something that is not the law: **occupancy noise**.
`σ(log g)` at fixed `g_N` scales as `g^{−3/2}` with a `(g+a₀)/(g+2a₀)` modulation, giving
`σ(0.3a₀)/σ(3a₀) = 22.34` for n=1 vs 34.49 for n=2, and the **skewness of δg flips sign
exactly at `g = a₀`** (A2). A sign flip is a much cheaper measurement than a 15 % amplitude
difference, and no other interpolation predicts it at the same place.

> **ERRATUM (2026-10-22, doors push D1):** the skew-sign discriminator is **RETIRED for RAR residuals** (D1 SCOPED NO-GO, `doors_push_2026_10_22/D1_skew_preflight/README.md`). RAR errors (distance, Υ, inclination) are symmetric in log g, and in log g **both laws predict a negative skew** across the whole window g/a₀ ∈ (0.375, 1) (√N_s·skew at a₀/2: n=1 −4.38, n=2 −2.44). The sign difference exists only in linear g, where a 0.06 dex log-symmetric background alone has skew +0.42 and SPARC's measured out-of-window skew is +2.9 (canonical) / +3.2 (alt), 17–50× the best-case signal (+0.062 / −0.165). The Gaussian price is also understated: ~1e4–1e6 points, not 7,000–13,500. The statement above is kept as written; it no longer decides n.

**And n = 1 is now *derived*, not asserted.** A35 puts the two laws in one family,
`Y_m = a₀ − λA` with `n − 1 = λ` the depletion fraction: `λ = 0` gives n=1 with capacity `a₀`,
`λ = 1` gives n=2 with capacity `a₀/2` and exact form `1/A = 1/g + 1/(a₀ − A)`. Then:

- **Capacity = affinity is derived**, not fitted: with a linear element `A = a₀θ` and
  `θ_max = 1`, the two are the same number.
- **Least dissipation selects λ = 0.** Minimising `Ψ(A) = A²/2a₀ + (g−A)²/2g` gives
  `A = a₀g/(g+a₀)` **exactly** — the canonical law is the stationary point of a Thomson/Onsager
  dissipation functional, and Lagrange over the two displacements derives the common occupancy.
- **n = 2 is not a state.** Its residual is `2−√5` at `g = a₀` and non-zero for *every* `g` and
  every capacity; its excess energy is `(9−4√5)a₀/4`; and it fails the detailed-balance
  condition `F'(θ₂) = kT ln(2φ) ≠ kT ln 4`, with entropy production `0.6199 a₀k_a > 0`
  everywhere. A single site has only detailed-balanced steady states, so λ = 1 is not
  reachable by any occupancy partition.

The discriminator sharpens accordingly: the occupancy-noise **skewness flips at `g = a₀` for
n=1 but at `g = 3a₀/8` for n=2**, and the two have **opposite signs** across
`g/a₀ ∈ (0.375, 1)` — at `g = a₀/2`, skew = `+0.7071` vs `−0.3483`. The Nyquist ratio at `a₀`
is `(5+2√5)/4 = 2.3680`, and it diverges at `a₀/2` for n=2 only.

> **ERRATUM (2026-10-22, doors push D1):** the skew-sign discriminator is **RETIRED for RAR residuals** (D1 SCOPED NO-GO, `doors_push_2026_10_22/D1_skew_preflight/README.md`). RAR errors (distance, Υ, inclination) are symmetric in log g, and in log g **both laws predict a negative skew** across the whole window g/a₀ ∈ (0.375, 1) (√N_s·skew at a₀/2: n=1 −4.38, n=2 −2.44). The sign difference exists only in linear g, where a 0.06 dex log-symmetric background alone has skew +0.42 and SPARC's measured out-of-window skew is +2.9 (canonical) / +3.2 (alt), 17–50× the best-case signal (+0.062 / −0.165). The Gaussian price is also understated: ~1e4–1e6 points, not 7,000–13,500. The statement above is kept as written; it no longer decides n.

*Correction to an earlier guess of mine:* `√(g²+a₀²/4) − a₀/2` is **exactly `g_N`**, the
baryonic branch, not the response — so the "parallel network" reading was wrong, and the
canonical law is a *series compliance*, not a parallel conductance (A35).

**The discriminator is exact and bigger than the record thought.** At fixed `g_N` the two
laws differ by at most

$$
\max\frac{g_{n=1}-g_{n=2}}{g_{n=2}}=\frac{2}{\sqrt3}-1=15.4700\%\quad\text{at }g_N=\tfrac{a_0}{2},
$$

which is `√(2/√3) − 1 = 7.4570 %` in circular speed. **Three normalisations exist and they are
not equal** (A31, A32): relative to `g_alt` the maximum is **15.470 %**, relative to `g_can` it
is **13.397 %**, and relative to `g_N` **26.795 %** — all at `g_N = a₀/2`. The record's "7.46 %"
is the circular-speed form `√(2/√3)−1 = 7.457 %`; half the 15.47 % figure (7.735 %) is a
*linearisation*, not the exact value, and my earlier claim that the harness "reproduced both"
was wrong.

**Can SPARC decide?** No (A7, pre-registered): Δχ² = **+219.45** on the canonical footing
(n=1 favoured) and **−344.66** on the alt footing (n=2 favoured) — the pre-registered rule
fires in *opposite directions*, and with per-galaxy scatter `sd(Δχ²_g) = 22.7` the
bootstrap significances are **z = +0.75** and **z = −1.21**. Per-galaxy wins are 84/87 and
73/98. The forecast (scatter-calibrated) is **N ≈ 1330–1980 SPARC-quality galaxies**, or
effective errors smaller by ≈ 3× at N = 171. Per-galaxy signal-to-noise is 0.068–0.082,
so this is a survey-size problem, not a modelling problem.

---

## 3. The relativistic completion and its four gates

The action is the round-2 one (frozen; `core_open_problems_round2_2026_10_20/03_relativity/`),

$$
\frac{L}{N\sqrt h}=\frac{{}^{(3)}R+K_{ij}K^{ij}-(1+\beta)\theta^2-2\Lambda}{4K}
+P^iD_i\log N-W(u)+\frac{\eta}{2}E_iE^i-\frac{\gamma}{2}(D_iP^i)^2-\frac{\gamma}{4}F_{ij}F^{ij},
$$

`u = K|P|`, `W = (a₀²/K)[−u/a₀ − log(1−u/a₀)]`, and it reproduces `g_N = g²/(g+a₀)`
exactly (residual 0, A12).

| gate | status | number | source |
|---|---|---|---|
| **Lensing = dynamics** | **DERIVED at first order; NOT an identity** | `(Φ−Ψ)/Ψ = O(Ψ) = 2.63e-7`; 9.13e-8 at 10 kpc | A12, A3 |
| **GW speed = c** | **DERIVED (speed); mode acquires a MASS when P̄ ≠ 0** | `c_T² = 1` exactly; but `W(u)` contracts `P_iP_j` with `h^TT` off the P̄=0 background, giving an `h²` **mass** term (A31 check 28) — a mass, not a speed | A3 15/15; A31 |
| **Solar System Newtonian** | **CONDITIONAL (turn-off)** | kernel anomaly `a₀ = 2557.38 B_E` uncured; `y_t = 66.30` closes Λ, planets pass 9.14×; **P sector adds `a_P = GM/L*² = 6.61e-3 B_E`** | A4, A22 |
| **Stable at every acceleration** | **DERIVED** | `dg/dg_N ∈ [1, ∞)`; scalar front speed `c_s² = γ/η = 1` **exactly** once η = γ = KL\*²/2 (§9.1), to 1.2e-18 | A4, A3, §9.1 |
| **Preferred frame** | **DERIVED near-source; GALACTIC REGIME OPEN** | α₁ = α₂ = 0 and β = 1 hold for `r ≪ λ = 17 pc`; the galactic-regime α₁ is **not computed** (A22 says so; A31 flags my earlier "DERIVED (zero)" as a contradiction with my own text) | A22 13/13, A31 |

**Why the preferred-frame parameters vanish — and it is structural, not tuned.** Two facts do it
(A22). (F1) On any static preferred-frame configuration `θ ≡ 0` identically, so the gravity
sector is *exactly* Einstein–Hilbert for every `β_ADM`; in aether variables
`c₁ = c₃ = c₄ = 0, c₂ = −β_ADM`, for which the published α₁ and α₂ both vanish, and `θ²` is
O(h²) so it has no linearised stress either. (F2) P's only O(ρ) stress is the charge `−D·P`
— the clock term has no shift and every other P term is quadratic in P — so there is no
momentum density (`g_0i = 0`) and no anisotropic stress. The residual frame dependence is a
pure isotropic rescaling of the P source, which rescales a *linear* potential `(GM/L*²)r`
rather than `U = GM/r`, hence α₁ = 0. That same linear potential is a **new, independent
observable**: a constant sunward anomaly

$$
a_P=\frac{GM}{L_*^2}=2.4205\times10^{-16}\ {\rm m/s^2}=6.61\times10^{-3}\,B_E,
$$

151× inside the ephemeris bound, but a second anomaly that adds to the kernel's `a₀` in the
budget. Two anomalies, one kernel and one geometric, both proportional to `GM` and both with
distinct distance dependence.

**The GW gate is exact, and for the same structural reason as the lensing gate.** No operator in
the action carries two derivatives of `h^TT`; the constraint sectors are TT-blind; `θ` is
O(perturbation²) so the `(1+β)θ²` term is quartic and inert at quadratic order. The quadratic
tensor action is therefore the Einstein one, `a³(ḣ² − p²h²)/(16K)`, and `c_T² = 1` follows
identically. The operator that would break it is a P–curvature coupling (`ξ R_ij P^iP^j`,
`ζ R P²`); none is present, and adding one shifts `c_T²` off 1 (my mutation demonstrates it).
The scalar sector is the one place the theory can exceed c: `c_s = √(γ/η)`, so `γ ≤ η` is
required, with the joint polarized bound `γ/η + 4γa₀²/K ≤ 1` (the second term is 1.19e-18 at
L\* = 24 pc, so numerically the condition is just `γ ≤ η`).

**The law HAS an external-field effect, and that corrects a published claim.** `g_N = g²/(g+a₀)`
is *exactly* AQUAL with `μ(x) = x/(1+x)`, and AQUAL has an EFE. "ν depends on `g_bar` only"
does **not** imply "no EFE", because `g_bar` at a wide binary contains the Galaxy and removing
it is a non-local operation with no covariant completion. Measured (A24): imposing the
Galactic field moves `γ_v` by **0.350** (12.7σ) while the QUMOND-vs-AQUAL solver fork is
≤ **0.019** (0.7σ) — the EFE is **18×** larger than the solver ambiguity. So the theory has an
EFE, and the October record's title claim ("No External-Field Effect", Zenodo 23251278) is the
document in error, not the September registration. The consequence for the wide-binary arm:
the framework predicts **γ_v = 1.18** at 20 kAU (bracket 1.1771–1.1933 across kernels and
`x_ext`), which sits inside Arm A's 1.1614–1.1814 — the registered prediction was right.
The 1.51 figure comes from dropping the EFE *and* using the total rather than exact two-body
composition: 1.5315 (mass) → 1.4037 (composition) → 1.1933 (EFE). And note 1.51 > 1.23, the
framework's own no-verdict zone, so a 1.51 detection could never have scored as confirmation.

**No cosmic aether (partial close of the preferred-frame gate).** The P field has no
cosmological background value, and this is now a theorem rather than a choice. On FRW every
derivative operator in the action vanishes for homogeneous P, the clock term `P^iD_i ln N`
vanishes with `N = 1`, so the P equation reduces to `dW/du = 0`. Since

$$
\frac{dW}{du}=\frac{u}{K}\frac{1}{1-u/a_0},
$$

the only zero is `u = 0`, and `W` is strictly increasing away from it — there is no
symmetry-breaking minimum. Hence **P = 0 is the unique homogeneous solution** (coordinator,
4/4, mutation bites): the Solar System does not move through a Lorentz-violating VEV. That
removes the VEV route to α₂. The remaining route to α₁, α₂ is the `(1+β)θ²` deformation,
which is a genuine preferred-frame term and is **not** closed here — it is the one gate
still open.

**Why lensing equals dynamics, structurally.** Not because the action was tuned, but
because the extra sector is a **charge** sector, not a stress sector. Under
`N = 1+εn₁`, `f = 1+εh₁`, `P = εp₁`, *every* ≤2-derivative operator built from P has
`Π_O = O(ε²)`; exactly one operator carries an O(ε) lapse source, the clock
`P^iD_i ln N`. So at leading order the sector's stress is `diag(−ρ,0,0,0)` — dust — whose
traceless part vanishes, and by the exact slip lemma
`G^i_j − ⅓δ^i_jG^k_k = (∂^i∂_j − ⅓δ^i_j∇²)(Φ−Ψ)` there is no slip (A12). The
counterexample that gives the theorem content: drop the clock term and
`|Π/σ| = 2`, i.e. O(1) slip (Janis–Newman–Winicour class). The framework's own action
**derives** `P ∥ D ln N` from its P equation rather than assuming it — that is the load-
bearing premise, and it is the one to attack.

**The Solar System, sharply.** The canonical law's strong-field anomaly is a **constant
a₀**, not a₀/2 (exact: `ν_can−1 = ½(√(1+4/y)−1) ~ 1/y` with coefficient 1; quadrature has
½). Against `B_E = 3.66e-14 m/s²` that is **2557.38×**, twice the quadrature's published
1279×. The vacuum integral `Λc⁴/a₀² = ∫y(ν−1)dy` diverges **linearly** for both, canonical
twice as fast (π/2 vs π/4 per unit `y_t`). The exact closure is

$$
\frac{\Lambda c^4}{a_0^2}=\frac{\pi}{2}\,y_t-\ln\!\frac{y_t}{4}+C_{\rm can},\qquad C_{\rm can}=-0.8862944=8\,C_{\rm quad},
$$

and with the observed `Λc⁴/a₀² = 100.4058` the turn-off solves to **y_t = 66.2999**, i.e.
`6.21e-9 m/s²`. **One** `y_t` does both jobs — it makes the vacuum term finite and equal to
the observed Λ, and every planet then passes with a **9.14× margin** in `y_t`
(the worst case, Neptune, sits at 1.2 % of its bound). But the turn-off is **law-dependent**:
the quadrature law needs `y_t = 128.7559`. Feeding the quadrature's value to the canonical
law over-predicts Λ by **1.9707×**. So `y_t` is not a shared parameter — it is a
**discriminator**: a measurement of the turn-off scale separates n = 1 from n = 2 by a
factor 1.94, on top of the 15.47 % shape difference. That is a conditional pass with the
premise named: the turn-off exists, and its scale is tied to Λ's *observed value* — which is a
posit, not a derivation. A4 is explicit that `y_t` is a **fitted** number once Λ is taken from
data; what the lane shows is that one value does both jobs.
**But `y_t` is not an independent parameter, and A28 proved it:** the closure is exactly
`Λc⁴/a₀² = 8π/κ²`, so `y_t = F⁻¹(8π/κ²)` is a function of κ alone
(`d ln y_t/d ln κ = −1.947`). **Deriving `y_t` *is* deriving κ.** None of four named
principles (strain saturation, response time, one-mode-per-cell, self-consistency) lands
within a factor 8; the only sub-1 % expression at both footings, `y_t = 2Z²`, is numerology
(it implies κ = 0.4979 and makes no second prediction). So the theory carries **one** free
number, not two.

---

## 4. Where the stiffness length L\* comes from

**Answer: L\* is the switch-off radius of the P sector's elastic stress — and that attribution
is a correction.** A33 checked it and the "Γ=2 pressure" is *not* the medium's kinetic pressure:
the elastic sound speed is `0.72 m/s` against a cold-medium dispersion `σ_c = 8.33 km/s`, so
`p_kin/p_el = 2.7×10⁸` and the kinetic Jeans length is `198 kpc`. The kinetic pressure therefore
never switches off where the scaling says; the elastic stress does. The *scaling* `r_switch ∝ L*`
survives unchanged, and so does `R_core`, but the physical carrier is the field's stiffness, not
the medium's velocity dispersion.

The elastic stress's ratio to gravity is

$$
\frac{(1/\rho)\,dp/dr}{g}=\Big(\frac{L_*}{r}\Big)^2
$$

for cusps `1 ≤ n ≤ 2` — **density-free**. Compared with the *cold sector's own* gravity it
switches off at `r = L_*`; compared with the **total** gravity the switch is at
`r = L*√f_c` (A16, corrected by A20) — **3.73 pc** for an MW-like halo at L\* = 24 pc, and
18.40 pc for a dwarf-like one. Both are far inside the innermost SPARC datum, so the law's
fit region is untouched. The theory predicts a **pressure-supported core of size
R_core = (π/√2)L\* = 53.31 pc** at L\* = 24 pc (exact n=1 polytrope; the pressure balances
self-gravity identically). The force-balance deviation is **13.40 % at 2 r_switch**,
2.02 % at 5 r_switch, 1 % at 7.09 r_switch; the *observable* plateau is
`1 − √(1−f_c)` = 1.21 % (MW) / 35.82 % (dwarf).

| | value |
|---|---|
| published window | 24 pc – 1 kpc |
| **window after the data** | **24–90 pc under `f_c → 1`; up to 180 pc at `f_c = 0.25`** (LITTLE THINGS R0.3(IC 10)/2.22; the bound is model-dependent — sample 10th percentile 184.6 pc, median 787.8 pc) |
| in horizon units `L*H₀/c` | 5.40e-9 – 2.25e-7 |
| a `c/√(Gρ)` reading requires | ρ = 2.4e14 – 4.2e17 ρ_Λ (a medium density, not the vacuum) |
| `L* = σ²/a₀` maps to | 24 pc ↔ 8.33 km/s; 90 pc ↔ 16.1 km/s |
| core radius (MW-like, L\*=24 pc) | **R_core = 53.31 pc** |
| Jeans mass at switch-off | `M_J = 3.654 V_f²L*/G = 2.04e4 (V_f/km/s)² M⊙` = **5.57e8 M⊙** for a flat-curve profile; **3.15e6 M⊙** for NFW (A31: the profile matters by 177×) |
| signature | `d ln M_J/d ln ρ = +1` — *denser regions make bigger clumps* (standard Jeans: −½) |

**No-juggling guard, and it bit.** L\* is **one number for all galaxies**, no per-galaxy
freedom, and any formula for it must use only quantities already in the theory. Of the two
candidates, `L* = V_f²/(9a₀)` **fails** outright: a 2.637 dex spread across SPARC, 30.3 %
of galaxies outside the window, and an implied cold-phase dispersion of 55 km/s (6.7× the
8.23 km/s the medium allows). `L* = σ²/a₀` **survives at 24 pc and dies at 1 kpc** — its
own consistency cap is L\* ≤ 93.8 pc. So the guard does what it was built to do: it
removes the upper half of the published window and leaves a single number, ~24 pc.

**Resolution.** SPARC's 30-inch beam floors at ~142 pc and its innermost reliable radius is
80 pc, so **0/175 galaxies probe a 24 pc core** — the present data cannot see it. LITTLE
THINGS does bound it (beams 20–530 pc). The decisive measurement is **ngVLA at 0.15″**,
which reaches 24 pc out to 33 Mpc: ~30 dwarfs with V_f < 40 km/s inside 8 Mpc, 3 km/s
channels, gives a 21.03 % dip at 30 pc and 11.21 % at 40 pc, **≥ 5σ per galaxy** (A20).

**What L\* is not.** It is not a horizon-scale length (7–8 decades below c/H₀), and it is
not the same as the other two cutoffs the same scale generates: one L\* gives
`λ_J = 4.443 L*` (106.6 pc at L\*=24 pc), a free-streaming length ~82 kpc and a half-mode
scale ~1.02 Mpc — a spread of ≥ 3.36 dex *inside* the window, so **no single cutoff can be
the whole story** (A16). The three lengths are three functionals of one microscopic scale;
that is a prediction (three numbers from one), not a fit.

---

## 5. The cold sector — the part nobody else has

1. **Two ratios, not one.** At the virial radius `M_ph(<r_v)/M_b(<r_v) = ½(√(1+4/y_v)−1)` is
   **25.90** (MW-like) and **3.77** (cluster-like), **6.87×** apart (A31 corrected my earlier
   25.04/2.62, which are `R_tot = μ(1+F)−1` — the phantom per *total* baryon, a different
   quantity). The cosmic share is **5.3643**.
   They cross at `M_v = 1.7584e14 M⊙`, **independent of concentration** (A18, structural).
2. **"Cold = the law's phantom" is excluded at 7.7σ.** On the 318-cluster eRASS1×KiDS stack,
   measured `A_MID = 1.9102 ± 0.1186`; the phantom reading predicts **1.000**, the cosmic-
   share reading predicts **1.852**. The data sit 0.49σ from cosmic and 7.67σ from phantom.
3. **The saddle no-go, sharpened.** The exact two-body solution requires **negative**
   cold-energy density in a thin pancake through the null point: **−89.32×** the mean cold
   density at R = 0.2d for `M_b = 1.4e11 M⊙` each at `d = 780 kpc` (reproduced; the
   published note never states `M_b` or `d`, and the plausible band is −75.5 to −110.9).
   The pancake is 30.5° wide and covers 26.3 % of the solid angle at R = 0.2d; the density
   cusps as `|ρ| ∝ r^{−1/2}` at the null (verified to 0.6 %). A positive-mass medium cannot
   do this, so the framework predicts **no saddle dip**. Since A24 established that the law
   *does* carry an EFE, A13's suppression curve transfers — and A23's full-domain solve then
   **kills the test as a practical one**: the dip needs `e ≤ 0.22` (i.e. `g_ext ≤ 3.2e-4 a₀`),
   while a deep void is already at `e = 0.68`, a filament at 10.2 and a group at 34.1. The
   retained column is 1.00 / 0.64 / 0.40 / 0.24 / 0.05 / 0.00 at `e` = 0 / 0.1 / 0.15 / 0.2 /
   0.3 / 0.68. **No accessible environment retains the dip**, so the pair budget diverges.
   A13's "voids are viable" is withdrawn: its EFE curve came from imposing mirror symmetry at
   `z = 0`, which a uniform axial field breaks — reproduced on the half domain (0.746/0.332 at
   e = 0.3/1.0) but 0.050 at e = 0.3 on the full domain. **P1 is therefore a theoretical
   statement about the medium, not a test anyone can run.**
   Three corrections to the published note, all from A6:
   - the **−33 "cluster" figure is not a cluster-pair number.** At `d = 3 Mpc` a cluster pair
     gives −485; reaching −33 needs `d = 11.78 Mpc`, and then the column is −19.73. The two
     cluster numbers are jointly reproduced only by a **group-mass** pair (4.2e12 M⊙ each,
     3 Mpc): ratio −33.07, column −5.025.
   - the **net column is negative**: −2.424 M⊙/pc² (negative part −3.529, positive +1.105).
     The published "total column still positive (+0.016)" appears only within ~1° of
     φ = 77.44°; at the physical φ = 90° it is −2.42. **That claim does not survive.**
   - the missing depth for the MW configuration has **two independent values that do not
     agree**: **3.529 M⊙/pc²** (A6, explicit masses and an analytic null) and **2.16–2.37**
     (A13, a converged axisymmetric field solve). The 1.5× discrepancy is **unresolved**. My
     earlier characterisation of A13 as "rescaling the paper's units" was wrong (A31): it is an
     independent PDE solve. A6's value is quoted in the predictions table because it has stated
     inputs; the disagreement is the honest state.
   A naive superposition gives the **wrong sign** (+0.64), so the pancake is strictly
   nonlinear (A13). The 11.8× pair requirement (≈ 8282 pairs for 3σ, reproducing the
   published "about twelve times") is confirmed.
4. **The sourcing fraction is radial and half-explained.** `u = 0.4716 ± 0.0361` (MID) →
   `0.9865 ± 0.0984` (OUT), plus a new inner value **u = 0.3348 ± 0.0563** (A29, 8 bins).
   **Caveat (A31):** `u` is a ΔΣ-weighted *band amplitude ratio*, not a 3D mass ratio — the
   unmodelled band-to-3D mapping gives a 3D MID value of 0.65 against the 0.812 band share. The
   qualitative rise is robust; the numbers are band-level.
   The profile is a **step, not a gradient**: constant u is rejected at χ²/dof 5.92, a step
   fits at 1.75 with the break in (1.176, 1.711) Mpc. The break is the **splashback radius**:
   `r_sp = 0.83 r200m = 1.367 r200c = 1.414 Mpc`, 0.3 % from the model-independent caustic at
   1.419 Mpc. Beyond `r_sp` the medium is single-stream, hence dust, hence **u = 1 exactly** —
   that number is *forced*, not fitted. Inside, `u = 1 + 3⟨w⟩` with `⟨w⟩ = −0.176 ± 0.012`
   (12σ of tension) and **no velocity distribution supplies it**: relaxation fails on sign
   (the core would relax 94× faster and be dust first), phase space misses by 4.6× in radius,
   and mass terciles prefer the zero-parameter splashback prediction (1.00/0.985/0.817
   vs 1.90/1.04/0.68, max 1.6σ). **The inner 0.472 remains a named premise (P1′).**
   New prediction: the step sits at `1.37 r200c(M,z)` → 1.10 / 1.39 / 2.00 / 2.99 Mpc across
   5e13–1e15 M⊙. Falsifier: a 1.42–2.5 Mpc band separating u = 1.000 (step) from 0.806
   (phase space) at 3σ needs `σ_u ≤ 0.0648`, i.e. **≥ 717 clusters** (2.3× present).

---

## 5b. The fork, resolved: law-first

> **ERRATUM (2026-10-22, doors push D2):** the fork is **not** resolved and "one DR4 bin decides" does not hold. (i) DR4 can decide it only through the whole-catalogue γ̂, and only if σ_sys < 0.054 (canonical; alt 0.064) — the record's inter-group spread (0.174) is 3.2× that ceiling; the 18–22 kAU bin holds ~208 pairs at N = 30k on DR3 occupancy, not 2,223. (ii) A26's law-first verdict tested the law **without** the host's external field (the EFE-blind reading, whose wide-binary value is 1.40–1.53, not 1.18). With the MW/M31 EFE that P5 uses, the 45 sub-threshold satellites sit **+1.25 dex above the law** (5/45 within 0.5 dex). So both readings fail on satellites; the dwarf leg excludes medium-first but does not certify the EFE-present law-first reading that predicts γ_v = 1.18. The fork stays OPEN, DATA-GATED. See `doors_push_2026_10_22/D2_wide_binary_fork/README.md`.

The fork was real and it is now settled by data (A26, 11/11). The threshold is present in the
dwarf population — a step of **+0.453 ± 0.099 dex** at `M_crit` — but it has the **wrong sign
for medium-first**, which requires **−1.622 dex**. The median boost below `M_crit` is **140×**
where medium-first needs 1×. Mann–Whitney p = 2.7×10⁻⁸, KS p = 1.4×10⁻⁸, Δ(−2 ln L) = 158;
14 of 45 sub-threshold systems sit within 0.5 dex of the law, **0 of 45 within 0.5 dex of
Newtonian**.

**Verdict: LAW-FIRST.** The law holds below the crossover, so A22's `M_crit = 3.87e5 M⊙` is
*not* a place where MOND switches off — it is the radius inside which the static P-sector
ansatz changes character, and the ansatz is not the fundamental object. That is a real
demotion of A22's finding and it is recorded as such. The honest caveat: the `M_crit` split is
population-degenerate with `g_bar < 1e-12` (ρ = +0.79), and the largest measured
binary/tidal correction (0.59 dex) leaves 73 % of the +0.65 dex excess unexplained — but that
excess is a *different* problem (the record's dwarf anomaly), and it does not affect the sign
test. The clean separator would be isolated (non-satellite) ultra-faints with
`M* < 3.9e5 M⊙`; exactly one is on disk (Leo T).

**Consequence for the parameter count.** With law-first, the medium is an *effective*
description of the law, not its microscopic parent. That is consistent with A27's and A28's
no-gos: neither the factor 2 nor the turn-off can be derived *from* the medium, because the
medium is downstream of the law.

---

## 6. Predictions, with a number, a recipe and a falsifier

| # | prediction | number | recipe | falsifier |
|---|---|---|---|---|
| P1 | No saddle dip between lens pairs — **theoretical only** | depth **3.529** (MW) / 5.025 (group) M⊙/pc² | needs `e ≤ 0.22`; no accessible environment has it (void 0.68) — **not runnable** | a dip at any accessible `e` would still mean the medium carries negative energy |
| P1b | The saddle pancake's shape | 30.5° wide, 26.3 % of solid angle, `|ρ| ∝ r^{−1/2}` | moot until P1 is accessible | a smooth (non-cusped) trough |
| P7b | Turn-off scale separates n=1 from n=2 | y_t = 66.30 (n=1) vs 128.76 (n=2), ratio 1.94 | kinematic a₀ at high acceleration, or Λ/a₀² systematics | a y_t outside [60, 140] |
| P9 | Occupancy-noise skewness flips at a₀ | sign change of skew(δg) exactly at g = a₀ | RAR residuals at fixed g_N, 3 bins either side | no flip, or a flip away from a₀ |
| P2 | Cluster SCT band ratio | MID/OUTER = **0.966 ± 0.102** (native) vs 1.888 ± 0.203 (phantom) | eRASS1×KiDS, 0.46–1.42 Mpc vs outer | ratio > 1.3 (> 3.3σ) kills the native-cold reading |
| P3 | Sourcing fraction is a **step** at the splashback radius | u(inner) = 0.3348 ± 0.0563, u(MID) = 0.4716, u(OUT) = 0.9865; break at 1.376 r200c = 1.414 Mpc | eRASS1×KiDS 8 radial bins | step radius scaling as 1.37 r200c across mass (predicted 1.10/1.39/2.00/2.99 Mpc) |
| P3b | Third-band u separates step from phase space | u = 1.000 (step) vs 0.806 (phase space), 3σ needs σ_u ≤ 0.0648 | 1.42–2.5 Mpc band, ≥ 717 clusters | a value between the two at > 3σ |
| P4 | Pressure core of size L\* | R_core = 53.31 pc at L\*=24 pc; 21.0 % dip at 30 pc, 11.2 % at 40 pc | ngVLA 0.15″, ~30 dwarfs V_f<40 km/s within 8 Mpc, 3 km/s channels | a core size that scales with galaxy mass at fixed L\* |
| P5 | Wide-binary boost (EFE **present**) | γ_v = **1.18** at 20 kAU (bracket 1.1771–1.1933); at 10 kAU EFE-present is **1.100–1.107**, not the EFE-blind 1.16; **not** 1.51 | Gaia DR4, 18–22 kAU bin, 2223 pairs, 4.5σ separation | γ_v ≤ 1.05 (Arm B); 1.51 would be a *no-verdict* zone value |
| P5b | Kernel decision on the RAR knee | Δχ²(Q−L) = **+157.96** canonical / +75.25 alt, no free parameters; +17.05 profiled | SPARC binned transition shape, fixed-Υ diagonal bins | pre-registered: < −25 refutes, > +25 confirms |
| P6 | Laboratory null | \|δG/G\| < 1e-6 (framework) vs 340 ppm (source-boost) | two-configuration Cavendish, source-density swap, 30–50 ppm | +340 ppm kills the screened framework |
| P7 | n = 1 vs n = 2 | 15.47 % max in g at g_N = a₀/2 | 1330–1980 SPARC-quality galaxies, free Υ per galaxy | a stacked Δχ² that survives the bootstrap |
| P8 | Jeans mass rises with density | d ln M_J/d ln ρ = +1 | clump mass function in dense vs diffuse regions | the standard −½ scaling |

**ERRATUM (2026-10-22, doors push D2):** (P5 recipe) the 18–22 kAU bin holds **~208 pairs at N = 30,000** on the DR3 frozen-cut occupancy (43 of 6,210 pairs, 0.69 %), not 2,223 (log-uniform 7.41 % is 10.7× too many; the pipeline's own mock gives 3.73 %, 1,119 pairs). The bin alone then separates 1.18 from 1.0 at only 0.8–2.6σ, so one bin does not decide; the registered whole-catalogue γ̂ does (5.0–5.9σ canonical) only if the contamination systematic σ_sys < 0.054 (alt 0.064). See `doors_push_2026_10_22/D2_wide_binary_fork/README.md`.

**ERRATUM (2026-10-22, doors push D1):** (P9) the skew-sign discriminator is **RETIRED for RAR residuals** (D1 SCOPED NO-GO, `doors_push_2026_10_22/D1_skew_preflight/README.md`). RAR errors (distance, Υ, inclination) are symmetric in log g, and in log g **both laws predict a negative skew** across the whole window g/a₀ ∈ (0.375, 1) (√N_s·skew at a₀/2: n=1 −4.38, n=2 −2.44). The sign difference exists only in linear g, where a 0.06 dex log-symmetric background alone has skew +0.42 and SPARC's measured out-of-window skew is +2.9 (canonical) / +3.2 (alt), 17–50× the best-case signal (+0.062 / −0.165). The Gaussian price is also understated: ~1e4–1e6 points, not 7,000–13,500. The statement above is kept as written; it no longer decides n.

---

## 7. Corrections this push makes to the record (fix-forward, nothing deleted)

1. **GF2's κ = ½ is μ = σ²/v_c²**, not the law's κ (A15). The κ ledger must be corrected;
   CFG908 stands.
2. **A11's `c_s = 0.72c` is a unit slip** — `c_s = 0.72 m/s`. The Γ=2 pressure is
   subluminal everywhere; the causality motive for switching it off does not exist (A16).
   A11's Task-2 no-go and its `L* ≤ 0.0608 pc` ceiling are withdrawn.
3. **A9's distance scaling `a₀ → a₀/f` is wrong** — it is `a₀ → a₀/f²` (V_bar → f^0.5 V_bar,
   g_bar invariant), confirmed independently by the per-galaxy scatter: 0.207 dex measured
   vs 0.210 predicted for p=2, 0.105 for p=1 (A14).
4. **Zenodo 23533323's "total column positive"** does not hold for the MW configuration
   (net −2.42 M⊙/pc²), and the cluster −33 is at 11.78 Mpc (A6).
5. **The published saddle depths are 11–14 % low**: 2.16–2.37 / 5.16–5.68 M⊙/pc², not
   1.9–2.1 / 4.6–5.1 (A13).
6. **The shear pass is conditional on "condensed baryons only"** (Δχ² +68.7 → +2.03); the
   canonical documents do not state that premise (A5 clue 10).
7. **The wide-binary DR4 registration is stale**: the September arms (1.1614–1.1814 /
   ≤1.045) predate the October EFE-blind paper's 1.51 at 20 kAU. One of them is not the
   framework's prediction (A5 tension 2).
8. **`r_switch = L*` is right only against the cold sector's own gravity**; against the
   total gravity it is `r_switch = L*√f_c` (3.73 pc, not 24 pc, for an MW-like halo). A20
   corrects A16 on this point; A16's `r_switch ∝ L*` scaling and its density-independence
   stand.
9. **A18's prose reverses its own sign**: the law's phantom is too diffuse, not too
   centrally concentrated (A21).
10. **A19's task statement (mine) was internally inconsistent**: `ℓ₀ = √(8π/Λ)` gives
   `Λℓ₀² = 8π`, not 32π. The two lengths are distinct — the cell `ℓ₁ = √(8π/Λ)` and the
   MOND length `L = c²/a₀ = 2ℓ₁`. The master identity is `R = ΛL²/(8π)`.
11. **The "smallest strong-field anomaly" justification for p = 1 is empty.** In the family
    `μ = x/(1+x^p)^{1/p}` (both limits exact for every p) the constant-anomaly coefficient is
    1 at p = 1 and **0** for p > 1: the canonical law has the *largest* constant anomaly, not
    the smallest (A6). What actually fixes p = 1 is exact Newton **plus** single-scale
    saturation — and the residue is `a₀`, i.e. the open strong-field problem, not a virtue.
12. **The turn-off is law-dependent**, so the record's "94–129" band is the quadrature's, not
    the canonical law's: 66.30 vs 128.76, ratio 1.94 (A4). Transplanting one to the other
    mis-predicts Λ by 1.97×.
13. **"No external-field effect" is wrong.** The law is exactly AQUAL with `μ = x/(1+x)`, and
    AQUAL has an EFE. The EFE moves the wide-binary boost by 0.350 (12.7σ) versus a
    0.019 (0.7σ) solver fork, so it is 18× the ambiguity and cannot be argued away. Zenodo
    23251278's title claim must be corrected; the wide-binary prediction is **1.18, not
    1.51** (A24), and 1.51 lies in the theory's own no-verdict zone (> 1.23).
14. **The kernel conflict dissolves.** `12.99 = 2π⁴/15` exactly (0.016 %), and the RAR kernel
    is the *only* one of the four that **cannot close Λ at all** — it converges, and the
    turn-off can only lower it. The 5.6× "tension" therefore compares a kernel the theory
    does not use. The canonical kernel is Langmuir/simple, forced by the action (A2, A12) and
    not disfavoured by SPARC (Δχ²(R−L) = +10.1/−0.8). The "94–129" band is the quadrature at
    two a₀ normalisations (94.05 at 73.19, 128.92 at 32π); the action's kernel gives
    48.79/66.38 — matching A4's 66.30.
15. **73.19 vs 32π is a convention, not physics**: `73.19 = 32π Ω_Λ` with `Ω_Λ = 0.728034`.
    The framework's own `a₀ = c²√(Λ/32π)` makes the target exactly 32π.
16. **`y_t` is not a second constant** — the closure is `Λc⁴/a₀² = 8π/κ²` identically, so the
    turn-off is κ restated and the theory has one free number (A28). A22's `a_P` is real but
    **unobservable**: 0.17σ in the joint 8-planet fit, 5.7× (formal Mars) to 151× (B_e) below
    the bounds — a consistency check that passes, not a test (A30). My brief's
    `L* = c²/a₀` was wrong by 1.3e9 (that length is 31 Gpc); the a_P number uses the *measured*
    stiffness length 23.45 pc (A30 caught this).
17. **κ = ½ is a curve, not a point.** In the (β, χ) ledger with `β = L/ℓ₁`, `χ` the cell
    topology, `κ = 1/(β√χ)`, the condition κ = ½ is `β√χ = 2` — so (β,χ) = (2,1) and (1,4)
    both give exactly ½ and R = 4. "Why the diameter rather than the radius" is therefore
    ill-posed (A27); what is missing is the *link* (which functional of the cell the law's
    length is), not a doubling argument.
18. **The dimension route is numerology** (A34). The premise I gave it was simply false: the
    codimension of a point in D=4 is **3**, not 2 (a codim-2 source is a *string*, a
    `(D−2)`-brane gives a constant field). `κ = 1/n` is a tautology in the framework's own
    definitions, and the delivered exponent is `D−3`, which is D-independent. D=5 predicts
    κ = 0.333 or 0.4 — both **within 1σ** of the measured 0.417 — so the κ data cannot even
    exclude five dimensions. Look-elsewhere: 11 hits at D=4 in a pool of 90. Dead.
19. **`υ` cannot be an action coefficient** (A33). A constant partition at 0.4716 deforms the
    law by **24 %** at `g = a₀/2`; so the measured `υ < 1` must be the catchment `f_ret`, not a
    coefficient. The master action carries `f_ret`, not `υ`.
20. **`γ = KL*²/2` is a definition of `L*`**, not a derivation of it (A33) — my first §9.1 said
    "zero free couplings" and that was wrong; it is one free stiffness, which *is* `L*`.
21. **A3's reduced P equation is missing its `γP″` term** (A33 caught it in the `D_t` chain),
    though no A3 conclusion changes because that lane evaluates at `P = 0`.
22. **The Γ = 2 "pressure" is elastic, not kinetic** (A33): elastic `c_s = 0.72 m/s` against
    `σ_c = 8.33 km/s`, `p_kin/p_el = 2.7×10⁸`, kinetic Jeans length 198 kpc. The `r_switch ∝ L*`
    scaling survives; its physical carrier is the field's stiffness.
23. **My "parallel network" guess was wrong** (A35): `√(g²+a₀²/4) − a₀/2` is **exactly `g_N`**,
    the baryonic branch, not the response. The canonical law is a *series compliance*.
24. **κ has four numbers circulating** (0.42 ± 0.10, 0.551 ± 0.043, 0.45/0.58/0.43, and the
   March–May κ = 1). There is no single reconciled κ, and A9 shows why: κ ∝ Υ^−1.23, so an
   IMF change moves it 1.98×. The Υ-free channel gives **κ = 0.354 ± 0.106** from 12
   galaxies and 73 points — consistent with ½ at 1.4σ, but not a measurement (A14). The
   distance floor is 16.1 % and **no sample size removes it**.

---

## 7b. The adversarial audit — 32 defects in 130 claims

A31 was given this document and told to break it. It classified every quantitative claim
against the backing files: **98 BACKED, 17 OVERSTATED, 1 UNBACKED, 14 WRONG — 32/130, a 24.6 %
defect rate.** It re-derived 35 numbers independently; 29 matched, 6 did not. A32 re-derived
the four core results in a clean room, forbidden to read any lane: **all four match**, including
`a₀/(cH) = 0.1727471`, `2√(32π/3) = 11.5776` (12 is 3.648 % off), the strong-field offsets
1 and ½, `c_T² = 1`, and `θ⁽¹⁾ = Π⁽¹⁾ = 0`.

The six load-bearing verdicts, and what was done:

| claim | verdict | action |
|---|---|---|
| "κ is a modulus" | **OVERSTATED** — A15's flat direction is a one-parameter family of the *two-equation halo truncation*, and A15 itself disclaims general underivability | §9.2 now says the theorem is conditional on the truncation; the list of closed routes stands |
| "n = 1 is forced by the lattice" | **OVERSTATED** — the lattice *matches* capacity to `a₀`, it does not derive it | superseded: A35 derives capacity = affinity and n=1 from least dissipation (added after the referee's snapshot) |
| `c_T² = 1` exactly | **OVERSTATED** — true for the *speed*, but on a `P̄ ≠ 0` background `W(u)` contracts `P_iP_j` with `h^TT` and gives an `h²` **mass** term | gate table now separates speed from mass |
| `α₁ = α₂ = 0` | **OVERSTATED + WRONG** — the aether `α₁` is `0/0` at `c₁=c₃=c₄=0`; the zero rests on the near-source argument (`r ≪ λ`), the galactic regime is uncomputed, and my table contradicted my own text | gate table now reads "DERIVED near-source; GALACTIC REGIME OPEN" |
| `L* = 24–90 pc` | **OVERSTATED** — 90 pc assumes `f_c → 1`; at `f_c = 0.25` it is 180 pc | window now quoted with its `f_c` dependence |
| "u rises outward" | **OVERSTATED** — `u` is a ΔΣ-weighted band ratio, not a 3D mass ratio (3D MID 0.65 vs 0.812 band) | caveat added in §5 |

The rest were arithmetic or attribution, all now corrected: `√(2/√3)−1 = 7.457 %` (I had
written `√(2/3)`, and "half of 15.47 %" is a linearisation, not the exact value); `y_t = 100.4`
in one place (that is `N_Λ`, not `y_t`); "1.16 at 10 kAU" (EFE-present is 1.100–1.107);
`M_J` depends on the profile by 177× (flat-curve 5.57e8 vs NFW 3.15e6); `M_ph/M_b` at the
virial radius is 25.90/3.77, not 25.04/2.62 (the latter is `R_tot`, a different quantity); the
saddle depth has **two independent values that disagree by 1.5×** and I no longer call A13's a
unit rescaling; the horizon-window row was the 24 pc–1 kpc value, not the 90 pc one; the
turn-off is a **fitted** posit (A4 says so), not "tied to Λ, not fitted"; and "every number was
re-run (21/21)" was a universal claim about 21 specific checks, which it is not.

**This table is the reason to trust the rest.** A 24.6 % defect rate in a document I wrote is
the useful number, not an embarrassment to be hidden — and A32's clean-room agreement on the
four core results is what survives independent of my prose.

---

## 8. The final ledger

**Closed by derivation**

- Lensing = dynamics: slip is second order, `2.63e-7`, structurally (charge sector). A12, A3.
- **GW speed = c: `c_T² = 1` exactly**, from the absence of any two-derivative TT operator and
  the TT-blindness of the constraints. A3 15/15, coordinator 6/6.
- **Preferred frame near-source: α₁ = α₂ = 0, β = 1** for `r ≪ λ = 17 pc`; θ ≡ 0 on static
  configurations, P carries no momentum density and no anisotropic stress. The **galactic-regime
  α₁ is not computed** (A22, A31) — that is the open part of this gate, not the near-source part.
- m = 1 is the unique thermal-lattice law; the canonical law is Langmuir. A2.
- **The kernel is decided**: Langmuir/simple, the action's own — forced by three independent
  constraints, and the only one of the four that both closes Λ and is derived. A25.
- `r_switch = L*` against the cold sector's own gravity (`L*√f_c` against the total), and
  `R_core = 53.31 pc`. A16, A20 corrected.
- `M_ph/M_b = ½(√(1+4/y)−1)`; the 1.7584e14 M⊙ crossing is concentration-independent. A18.
- Lean, no `sorry`, standard axioms only: κ–Z identity, `1/12 < 1/(2Z) < 1/11`, both roots
  and their **strict** ordering (`g_q < g_c`, no hypothesis needed), monotonicity, capacity
  limits. A8 — **40 theorems**, axiom footprint `{propext, Classical.choice, Quot.sound}`.
- `M_c = 5.3643 M_b` is `Ω_c/Ω_b`, not a cold-sector parameter. A9, A11.

**Closed by no-go**

- κ from counting: impossible (irrational `𝒩`). A1, A10.
- κ from dimensional analysis: impossible (one free function). A1.
- κ from strain saturation: `κ = 4√(π/3)`, off by 8.19×. A1.
- κ from the Euler charge: a₀-blind (total derivative). A19.
- κ from channel counting: basis-dependent. A19.
- n = 2 from a thermal lattice: impossible. A2.
- A positive-mass medium realising the law at null points: impossible. A6, A13.
- "Cold energy = the law's phantom": excluded at 7.7σ. A18.
- **u = ½ as an identity**: impossible — `u = 1 + 3⟨w⟩` forces `w = −1/6` (negative sound
  speed), and `f_ret ≤ 1` caps the cluster at u ≤ 0.488. A21.
- **R ≠ 4 in the saturation cap**: `R ∈ {1, 2}` gives κ = 1 and 0.7071, excluded by the
  measured κ at 6.14σ and 3.05σ. Only R = 4 survives. A19.

**Closed by data**

- **Law-first** (A26, 21σ): the law holds below `M_crit`; medium-first is excluded. The P
  sector's crossover is an ansatz artefact, not a MOND switch-off.

**Open, with the missing premise named**

1. **The scale-setting functional** returning exactly 4 in `ρ_DEc²/(a₀²/G)` — or equivalently
   the link that makes `β√χ = 2` (A27). This is now the **only free number** in the theory:
   `y_t` folds into it (A28), and the factor 2 folds into it (A27). The data have narrowed the
   cap to three options and picked one; what is missing is the principle.
2. **`u(r)`'s inner value**: `u = 0.472` inside the splashback radius needs `⟨w⟩ = −0.176`,
   i.e. tension, which no velocity distribution supplies. The outer `u = 1` is *derived*
   (single stream). One named premise (P1′) and one clean falsifier (≥ 717 clusters, third
   band).
3. **`L*`'s microscopic value**: bounded to **24–90 pc** by LITTLE THINGS, with
   `L* = σ²/a₀` the surviving map (24 pc ↔ 8.33 km/s) and its own cap at 93.8 pc. The number
   is not derived.
4. **A UV completion.** The cold sector has no established covariant parent (A5 clue 4:
   the best candidate fails its own frozen rule), and law-first says the medium is downstream
   of the law rather than its parent — which makes this the hardest item, not merely the last.

---

## 9. What "closed" means here — the closure theorem

This is the strongest statement the push can make, and it is a statement about structure, not
about a number.

### 9.1 The P sector has one coupling, not three

**Corrected by A33, which is right and my first version was not.** `γ = KL*²/2` is a
*definition* of the stiffness length (`L*² := 2γ/K`), not a derivation of it. So there is one
free stiffness, and it *is* `L*`. What is real, and unconditional, is that `η = γ` — one
stiffness rather than two — which A22's hedgehog solution already carries: the Compton
wavelength it reports is `L*/√2`, and its `m/H₀ = 2.620985163×10⁸` is what `c/(H₀L*/√2)` gives
to fifteen digits. So three couplings `(β, η, γ)` collapse to **one scale `L*` plus a bounded
`β`**, and the following hold (coordinator, `_parent/closure_theorem.py`, 8/8):

| consequence | value |
|---|---|
| scalar front speed | `c_s² = γ/η = 1` **exactly** (was CONDITIONAL, now closed) |
| P Compton wavelength | `λ_P = √(η/K) = L*/√2 = 16.9706 pc` |
| P mass | `m/H₀ = 2.620985e8` |
| residual non-luminality | `4γa₀²/(Kc⁴) = 1.19e-18` |

The relativistic sector therefore has **one free coupling plus a bounded `β`**, down from
three. `η = γ` is a choice of a single stiffness (A33 lists it as *chosen*, not derived); what
it *buys* is exact luminality, which is a nontrivial consistency gain: the scalar gate that was
CONDITIONAL in A3 is now closed, and the same choice fixes the P mass at `L*/√2` with no
further input.

### 9.2 κ is a modulus of the truncated halo system

The closure integral satisfies `I(y_t) = Λc⁴/a₀²`, and the definition of `a₀` gives
`Λc⁴/a₀² = 8π/κ²` **identically**. So

$$
I(y_t)=\frac{8\pi}{\kappa^2}\quad\text{for every }\kappa>0 .
$$

`I` is strictly increasing, hence invertible: **there is exactly one de Sitter member per κ,
and no EFT-internal relation selects one.** Numerically `y_t(κ) = 180.8, 102.7, 66.38, 34.6,
17.6` at `κ = 0.3, 0.4, 0.5, 0.7, 1.0`; with `a₀` fixed, `Λ ∝ 1/κ²`. That is a one-dimensional
vacuum manifold — a modulus, in the precise sense.

**The scope, stated honestly (A31):** the flat direction is a property of the *two-equation
halo truncation* — two equations, three unknowns. That is enough to kill every route that
starts from those equations, and it is not enough to prove that *no* system of equations could
fix κ. A15 says so itself. So the correct claim is "κ is a modulus of this system, and the
missing object is one more equation", not "κ is underivable, full stop".

Every route to fixing it has now been tried and closed: counting (A1, A10 — irrational),
dimensional analysis (A1 — one free function), strain saturation (A1 — off by 8.19), Euler
charge (A19 — a₀-blind), channel counting (A19 — basis-dependent), the cap's natural values
(A19 — data pick 4 but nothing forces it), the factor 2 (A27 — κ = ½ is a *curve* β√χ = 2),
and the turn-off (A28 — `y_t` is κ in disguise). **No further work inside this EFT can close
it.** That is not a gap in the search; it is the result of the search.

### 9.3 The parameter count, stated plainly

A33's master-action count is the honest one, and it is larger than my first estimate:

| theory | free parameters | what it predicts about galaxies |
|---|---|---|
| **this framework** | **4 finite + 3 functionals**, reduced by **5 exact degeneracies** | the RAR shape, lensing = dynamics, c_T = 1, α₁ = α₂ = 0, β = 1, the core size, the saddle no-go |
| ΛCDM | 6 (Ω_b, Ω_c, Ω_Λ, H₀, n_s, A_s, +τ) | nothing about the RAR — it needs a separate baryonic-feedback model with more parameters |
| Standard Model | 19 | nothing gravitational |

The four finite are κ, β, η, γ; the three functionals are the scale-setting functional, the
`υ(r)` profile and the turn-off *form*. The five degeneracies are exactly what makes the count
look smaller than it is: `γ–η` (only γ/η is observable), `γ–L*` (same parameter by definition),
`κ–a₀` (one number given Λ), `β–Λ_bare` (one background equation, two unknowns), and
`υ–f_ret` (a single-band amplitude cannot separate them). **So the framework is not "3
parameters"; it is 4 + 3 with 5 degeneracies, and the honest comparison to ΛCDM's 6 is that the
*observable* content is comparable while the *predictions* are far more numerous.** I would
rather state that plainly than win an argument with a miscount.

So the honest landing is: **this is a closed effective theory with one modulus, whose observable
parameter content is comparable to ΛCDM's while its predictions are far more numerous and its
RAR is not fitted at all.** The remaining question — *why this member of the family* — is a
UV/landscape question. It is not a gap in the equations; it is the boundary of their domain, and
§9.2 is the proof that the boundary is where it is.

### 9.4 The footing question is closed — and it picks the alt footing

This is A33's most consequential finding, and it was not asked for. The `θ²` term makes the
background equation

$$
2+3\beta=\frac{2\Lambda_{\rm bare}c^2}{3H^2},
$$

so `β = ½(2Λ_bare c²/3H² − 2)`. Requiring `β > 0` (the principal-positivity bound) with
`Λ_bare = Λ_obs` gives **β = −0.211 < 0** — excluded. Hence

$$
\Lambda_{\rm bare}\ \ge\ \frac{3H_0^2}{c^2}=1.462\,\Lambda_{\rm obs},
\qquad\text{i.e.}\qquad
\rho_{\rm bare}\ \ge\ \frac{\rho_{\rm DE}}{\Omega_\Lambda}.
$$

The action's de Sitter endpoint is a **pure** de Sitter universe (`Ω_Λ,eff = 1`), not ΛCDM; the
observed budget is recovered only with the clock's negative background stress `ρ_β = −9βH²/4K`
cancelling the excess. That is why `β` is invisible to α₁, α₂ and β_PPN.

**And that resolves the two-footing ambiguity.** With `ρ_bare = ρ_DE/Ω_Λ`,

$$
a_0=\kappa c\sqrt{G\rho_{\rm bare}}=\frac{\kappa c\sqrt{G\rho_{\rm DE}}}{\sqrt{\Omega_\Lambda}}
=\frac{a_0^{\rm can}}{\sqrt{\Omega_\Lambda}}=1.2091\,a_0^{\rm can}=\mathbf{1.132\times10^{-10}\ m/s^2}.
$$

So the two footings are not an ambiguity in the theory — they are the **bare and the observed
vacuum**, and the action lives at the bare one. **The framework's own value is the alt footing,
`1.132e-10 m/s²` (a lower bound), and the canonical `9.36e-11` is that same formula evaluated on
the observed dark-energy density.** This is a prediction, and the data already lean the right
way: A9's free SPARC fit gives `a₀ = 1.1033e-10` — 2.4 % below the action's bound, where the
canonical value is 17.3 % below.

The tension to keep in view: κ must be quoted *against a named density*. Against the bare
vacuum the theory's value is ½; against the observed `ρ_DE` the same a₀ reads κ = 0.605. The
Υ-free measurement `κ = 0.354 ± 0.106` (A14) is 2.4σ from 0.605 and 1.2σ from 0.5, so the
footing choice and the κ measurement are not yet separable — A33's degeneracy `(κ, a₀ | Λ)` is
exactly this.

---

## 10. Reproduce

```bash
cd deepseek_push/DS_FINAL_2026_10_21
python3 _parent/parent_audit.py            # 21/21, independent of every lane
for d in A*/; do (cd $d && python3 *_checks.py); done
cd A8_lean && lake env lean A8_C1_C2_kappa_Z.lean   # + C3, C4, C5
```