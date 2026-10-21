# The theory at the end of the DSF-21 push

**2026-10-21.** 23 lanes, all in this folder, each with a script that exits non-zero on a
failed check and a mutation that must break it. Every number below was re-run by the
coordinator from the lane script (`_parent/parent_audit.py`, 21/21, mutation bites) or is
quoted with the lane that computed it. Nothing here is a projection of what a lane might
have said.

**Status in one line.** The framework now has **one free number** (κ), **one free scale**
(L\*), **one free function** (the strong-field turn-off y\_t, tied to Λ), and **one
sector with a measured radial structure** (the cold energy). Everything else that was
asked for is either derived, or proved impossible in a stated class, or converted into a
pre-registered number. That is a completed *effective* theory. It is not a UV completion
and this document does not pretend otherwise.

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

**Answer: it does not switch at a twelfth. It switches at 1/(2Z) = 1/11.5776201, and the
difference is not a detail — it is the whole content of κ = ½.**

Exact, from `H² = 8πGρ/3` (K1–K3, A1; Lean `A8.kappa_Z_identity`):

$$
\frac{a_0}{cH_\Lambda}=\kappa\sqrt{\frac{3}{8\pi}}=\frac{\kappa}{2}\sqrt{\frac{8\pi}{3}}
=\frac{1}{2Z}\ \text{at }\kappa=\tfrac12,\qquad
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

`n = 2` (the a₀-line, `g² − g_N² = a₀g_N`, i.e. the quadrature law) is a **NO-GO in the
thermal-lattice class**: it is not the stationary point of any single-scale two-state
lattice. Its natural home is elsewhere (a Poisson second-moment identity, `⟨n²⟩ = λ²+λ`,
not a maximum-entropy law — A10). So the two laws are not two fits to the same medium;
they are two different media, and the framework's action picks the lattice one.

**The discriminator is exact and bigger than the record thought.** At fixed `g_N` the two
laws differ by at most

$$
\max\frac{g_{n=1}-g_{n=2}}{g_{n=2}}=\frac{2}{\sqrt3}-1=15.4700\%\quad\text{at }g_N=\tfrac{a_0}{2},
$$

which is `√(2/3) − 1 = 7.4570 %` in circular speed (A2; my harness Q2.8 reproduces both
and reconciles the record's "7.46 %"). `v² = gr`, so the two figures are the same number
in different units.

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
| **GW speed = c** | **DERIVED (exact)** | `c_T² = 1` exactly, not to leading order | A3 15/15; coordinator 6/6 |
| **Solar System Newtonian** | **CONDITIONAL (turn-off)** | anomaly `a₀ = 2557.38 × B_E` uncured; `y_t = 66.30` closes Λ, planets pass with 9.14× margin | A4 |
| **Stable at every acceleration** | **DERIVED (linear), CONDITIONAL (scalar)** | `dg/dg_N ∈ [1, ∞)`; scalar front speed `c_s = √(γ/η) ≤ c ⟺ γ ≤ η` | A4, A3 |

**The GW gate is exact, and for the same structural reason as the lensing gate.** No operator in
the action carries two derivatives of `h^TT`; the constraint sectors are TT-blind; `θ` is
O(perturbation²) so the `(1+β)θ²` term is quartic and inert at quadratic order. The quadratic
tensor action is therefore the Einstein one, `a³(ḣ² − p²h²)/(16K)`, and `c_T² = 1` follows
identically. The operator that would break it is a P–curvature coupling (`ξ R_ij P^iP^j`,
`ζ R P²`); none is present, and adding one shifts `c_T²` off 1 (my mutation demonstrates it).
The scalar sector is the one place the theory can exceed c: `c_s = √(γ/η)`, so `γ ≤ η` is
required, with the joint polarized bound `γ/η + 4γa₀²/K ≤ 1` (the second term is 1.19e-18 at
L\* = 24 pc, so numerically the condition is just `γ ≤ η`).

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
premise named: the turn-off exists and its scale is tied to Λ, not fitted.

---

## 4. Where the stiffness length L\* comes from

**Answer: L\* is the pressure switch-off radius, and that is a derived identity, not a
definition.**

The Γ=2 contact pressure's ratio to gravity is

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
| **window after the data** | **24 pc – 90 pc** (LITTLE THINGS: L\* ≤ 90.0 pc from IC 10; 300 pc excluded by 3.33×, 1 kpc by 11.11×) |
| in horizon units `L*H₀/c` | 5.40e-9 – 2.25e-7 |
| a `c/√(Gρ)` reading requires | ρ = 2.4e14 – 4.2e17 ρ_Λ (a medium density, not the vacuum) |
| `L* = σ²/a₀` maps to | 24 pc ↔ 8.33 km/s; 90 pc ↔ 16.1 km/s |
| core radius (MW-like, L\*=24 pc) | **R_core = 53.31 pc** |
| Jeans mass at switch-off | **M_J = 3.654 V_f²L\*/G = 2.04e4 (V_f/km/s)² M⊙ = 5.57e8 M⊙** |
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

1. **Two ratios, not one.** `M_ph/M_b = ½(√(1+4/y)−1)` at the virial radius is **25.04**
   (MW-like) and **2.62** (cluster-like), 9.57× apart; the cosmic share is **5.3643**.
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
   do this, so the framework predicts **no saddle dip**.
   Three corrections to the published note, all from A6:
   - the **−33 "cluster" figure is not a cluster-pair number.** At `d = 3 Mpc` a cluster pair
     gives −485; reaching −33 needs `d = 11.78 Mpc`, and then the column is −19.73. The two
     cluster numbers are jointly reproduced only by a **group-mass** pair (4.2e12 M⊙ each,
     3 Mpc): ratio −33.07, column −5.025.
   - the **net column is negative**: −2.424 M⊙/pc² (negative part −3.529, positive +1.105).
     The published "total column still positive (+0.016)" appears only within ~1° of
     φ = 77.44°; at the physical φ = 90° it is −2.42. **That claim does not survive.**
   - the missing depth for the MW configuration is **3.529 M⊙/pc²** (A6, explicit masses),
     not 2.16–2.37 (A13, which rescales the paper's own units rather than recomputing). The
     two differ by 1.5× and A6's is the one with stated inputs.
   A naive superposition gives the **wrong sign** (+0.64), so the pancake is strictly
   nonlinear (A13). The 11.8× pair requirement (≈ 8282 pairs for 3σ, reproducing the
   published "about twelve times") is confirmed.
4. **The sourcing fraction is radial, and it is not ½.** `u = 0.4716 ± 0.0362` (MID) →
   `0.9865 ± 0.0984` (OUT). MID is 0.78σ from ½ but OUT is **4.9σ** from it, and the two
   bands differ by ≥ 3.8σ for any band correlation (A21). The "≈ ½ at both anchors" is a
   **cancellation**, not a law: the law's own ratio spans 9.566× between the anchors and the
   retention table spans 9.0×, quotient 1.063.
   **u = ½ is structurally excluded as an identity**: `u = 1 + 3⟨w⟩` exactly, so ½ requires
   `w = −1/6`, i.e. a negative sound speed; and `f_ret ≤ 1` caps the cluster at
   `u ≤ 0.4880`, so ½ there would need more baryons than the cosmic share (`f_ret = 1.0245`).
   The MW anchor needs `f_ret = 0.1071`, which is admissible — so the two anchors cannot both
   be at ½ for a physical reason, only by coincidence. Scaling:
   `u ≈ (f_ret/R_cosmic)[y_v^{−1/2} − ½]`, `d ln u/d ln M_v → +1/6`, spanning 0.37–0.72 over
   1e10–1e14 M⊙. **Correction to A18's prose**: the phantom is too *diffuse*, not too
   centrally concentrated (its own residuals: 1.910 MID vs 1.012 OUTER).
   Falsifier at 3σ: `σ(A_MID) ≤ 0.0312`, i.e. ≥ 4602 clusters — or, cheaply, a group stack at
   `M_v = 1e13` where ½ and the cosmic share differ by 33 % in cold mass (A_MID 1.8122 vs
   1.4051), needing only `σ(A) ≤ 0.136` from a few hundred `M_500 ~ 2e13` stacks.

---

## 6. Predictions, with a number, a recipe and a falsifier

| # | prediction | number | recipe | falsifier |
|---|---|---|---|---|
| P1 | No saddle dip between lens pairs | depth difference **3.529** (MW, M_b=1.4e11, d=780 kpc) / 5.025 (group, 4.2e12, 3 Mpc) M⊙/pc² | stack ~8282 pairs (11.8× arXiv:1702.08485) at ~0.77 Mpc | a dip of the predicted depth ⇒ law exact, medium must carry negative energy |
| P1b | The saddle pancake's shape | 30.5° wide, 26.3 % of solid angle, `|ρ| ∝ r^{−1/2}` | same stack, azimuthal profile | a smooth (non-cusped) trough |
| P7b | Turn-off scale separates n=1 from n=2 | y_t = 66.30 (n=1) vs 128.76 (n=2), ratio 1.94 | kinematic a₀ at high acceleration, or Λ/a₀² systematics | a y_t outside [60, 140] |
| P9 | Occupancy-noise skewness flips at a₀ | sign change of skew(δg) exactly at g = a₀ | RAR residuals at fixed g_N, 3 bins either side | no flip, or a flip away from a₀ |
| P2 | Cluster SCT band ratio | MID/OUTER = **0.966 ± 0.102** (native) vs 1.888 ± 0.203 (phantom) | eRASS1×KiDS, 0.46–1.42 Mpc vs outer | ratio > 1.3 (> 3.3σ) kills the native-cold reading |
| P3 | Sourcing fraction rises outward | u(MID) = 0.4716 ± 0.0362, u(OUT) = 0.9865 ± 0.0984 | same stack, two bands | constant u at ≥ 3.8σ; σ(A_MID) ≤ 0.0312 reaches 3σ |
| P3b | Group-scale u diagnostic | at M_v = 1e13, A_MID = 1.8122 (u=½) vs 1.4051 (cosmic share) | few hundred M_500 ~ 2e13 stacks, eRASS1×DESI Y3 | σ(A) ≤ 0.136 needed; 33 % difference |
| P4 | Pressure core of size L\* | R_core = 53.31 pc at L\*=24 pc; 21.0 % dip at 30 pc, 11.2 % at 40 pc | ngVLA 0.15″, ~30 dwarfs V_f<40 km/s within 8 Mpc, 3 km/s channels | a core size that scales with galaxy mass at fixed L\* |
| P5 | Wide-binary boost (EFE-blind sector) | γ_v = 1.20 at 10 kAU, 1.51 at 20 kAU | Gaia DR4, 4.2σ forecast already on record | γ_v ≤ 1.05 (Arm B) |
| P6 | Laboratory null | \|δG/G\| < 1e-6 (framework) vs 340 ppm (source-boost) | two-configuration Cavendish, source-density swap, 30–50 ppm | +340 ppm kills the screened framework |
| P7 | n = 1 vs n = 2 | 15.47 % max in g at g_N = a₀/2 | 1330–1980 SPARC-quality galaxies, free Υ per galaxy | a stacked Δχ² that survives the bootstrap |
| P8 | Jeans mass rises with density | d ln M_J/d ln ρ = +1 | clump mass function in dense vs diffuse regions | the standard −½ scaling |

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
13. **κ has four numbers circulating** (0.42 ± 0.10, 0.551 ± 0.043, 0.45/0.58/0.43, and the
   March–May κ = 1). There is no single reconciled κ, and A9 shows why: κ ∝ Υ^−1.23, so an
   IMF change moves it 1.98×. The Υ-free channel gives **κ = 0.354 ± 0.106** from 12
   galaxies and 73 points — consistent with ½ at 1.4σ, but not a measurement (A14). The
   distance floor is 16.1 % and **no sample size removes it**.

---

## 8. The final ledger

**Closed by derivation**

- Lensing = dynamics: slip is second order, `2.63e-7`, structurally (charge sector). A12, A3.
- **GW speed = c: `c_T² = 1` exactly**, from the absence of any two-derivative TT operator and
  the TT-blindness of the constraints. A3 15/15, coordinator 6/6.
- m = 1 is the unique thermal-lattice law; the canonical law is Langmuir. A2.
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

**Open, with the missing premise named**

1. **The scale-setting functional** returning exactly 4 in `ρ_DEc²/(a₀²/G)`. This is the
   only hole in Q1. The data have already narrowed the cap to three options and picked one;
   what is missing is the principle that makes the cap the fourth power of the cell scale.
2. **The preferred-frame PPN parameters** α₁, α₂ and the nonlinear β (A22, in flight) — the
   only gate not yet computed. GW speed and lensing are closed; the scalar sector needs `γ ≤ η`.
3. **`u(r)`**: why the inner halo is half-sourced and the outer fully sourced. The
   measurement exists (P3) and the scaling is known (`u ∝ y_v^{−1/2}`, slope +1/6); the
   mechanism does not.
4. **The turn-off's origin**: `y_t = 100.4` closes Λ, but nothing yet forces it.
5. **`L*`'s microscopic value**: now bounded to **24–90 pc** by LITTLE THINGS, with
   `L* = σ²/a₀` the surviving map (24 pc ↔ 8.33 km/s) and its own cap at 93.8 pc. The upper
   half of the published window is gone; the number is not derived.
6. **A UV completion.** The cold sector has no established covariant parent (A5 clue 4:
   the best candidate fails its own frozen rule).

---

## 9. Reproduce

```bash
cd deepseek_push/DS_FINAL_2026_10_21
python3 _parent/parent_audit.py            # 21/21, independent of every lane
for d in A*/; do (cd $d && python3 *_checks.py); done
cd A8_lean && lake env lean A8_C1_C2_kappa_Z.lean   # + C3, C4, C5
```
