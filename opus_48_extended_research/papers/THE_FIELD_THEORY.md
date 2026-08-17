# The Field Theory: One Action, One Normalisation, Three Outputs

**Carl P. Zimmerman**, Briar Creek Tech
ORCID 0009-0008-3508-7982
v1, 2026-08-17

> **What this document is.** A single self-contained statement of the field theory: the
> action, the one normalisation condition it needs, the three things it then predicts, the
> complete list of what is fitted and what is free, and every open liability with its
> current status. It supersedes nothing — THE_COMPLETION v9 (DOI 10.5281/zenodo.21895046)
> remains the detailed record — but where the two disagree, **this document is newer**.
>
> **What changed to make it writable.** Two structural liabilities that had been open since
> the theory was assembled were closed on 2026-08-16/17: the perturbation health matrix on a
> tilted, nonlinearly-excited background (stage68) and the post-recombination growth history
> with an evolving sound speed (stage69, run against real CLASS). A third, the PPN
> preferred-frame parameter α₁, was computed for the first time (stage70) and returned a
> constraint four orders of magnitude tighter than anything the corpus carried.

---

## 1. The action

$$S=\int d^4x\sqrt{-g}\left\{\frac{R-2\Lambda_{\rm bare}}{16\pi G}
+\mathcal{L}^{\rm AeST}_{\rm aether}[A,g]
+\frac{\mathcal{A}(Q)}{8\pi G}\,\mathcal{F}_Y\!\!\left(\frac{Y}{\mathcal{A}(Q)}\right)
+K(Q)\right\}+S_{\rm m}[g,\psi]$$

with

$$Q\equiv A^\mu\nabla_\mu\varphi,\qquad
Y\equiv(g^{\mu\nu}+A^\mu A^\nu)\nabla_\mu\varphi\nabla_\nu\varphi,\qquad
A^\mu A_\mu=-1,$$

$$\mathcal{L}^{\rm AeST}_{\rm aether}=-\frac{K_B}{2}F^{\mu\nu}F_{\mu\nu}
+2(2-K_B)J^\mu\nabla_\mu\varphi-(2-K_B)Y,
\qquad F_{\mu\nu}=2\nabla_{[\mu}A_{\nu]},\quad J_\mu=A^\alpha\nabla_\alpha A_\mu,$$

and the two functions

$$\boxed{\;K(Q)=-M^4+\mu^2\Lambda_D^2\!\left[1-\sqrt{1-\frac{(Q-Q_0)^2}{\Lambda_D^2}}}\;\right],
\qquad
\boxed{\;\mathcal{A}(Q)\equiv a_0^2(Q)=\kappa^2\,G\,\bigl(-K(Q)\bigr)\;}$$

$\mathcal{F}_Y$ is the interpolation in AQUAL form, $d\mathcal{F}_Y/dz=1-e^{-\sqrt z}$
(Milgrom & Sanders 2008, ApJ **678** 131, Eq. 13 at α = ½; adopted by McGaugh, Lelli &
Schombert 2016). The aether sector is Skordis & Złośnik's (PRL **127** 161302); the
scaffold is theirs and is credited throughout.

**The programme's contribution is exactly two lines:** the promotion
$\mathcal{A}(Q)=\kappa^2G(-K(Q))$ — *the MOND scale is the dark sector's pressure* — and
the offset-DBI $K$ with $\beta\equiv\mu^2\Lambda_D^2/M^4=1$.

### 1.1 One normalisation condition

$K$ has an offset, so at its minimum $-K=M^4$ and $p_Q=K=-M^4$ exactly: $w=-1$, a
cosmological constant, with $M^4=\rho_\Lambda$. Feeding that into the promotion:

$$a_0=\kappa\,c\sqrt{G\rho_\Lambda}=c^2\sqrt{\frac{\Lambda}{32\pi}}
=9.3619\times10^{-11}\ \mathrm{m\,s^{-2}}\quad(\kappa=\tfrac12).$$

This is the theory's **only** normalisation input, and κ is **fitted, not derived** (§4).
Alternative footing (ρ_total, cH₀): $a_0=1.1279\times10^{-10}$; every dimensional number
below is carried on both.

## 2. The three outputs

Nothing further is put in. What comes out:

**(a) Dark energy, exactly.** At the minimum $w=-1$ identically — the vacuum never rolls.
Not fitted; a property of the offset.

**(b) Dark matter, as dust.** For small displacements $u=Q-Q_0$: $K\to\mu^2u^2/2$ is the
pressure while $\rho_{\rm exc}=Q_0\mu^2u$ is *linear* in $u$, so $w=u/2Q_0\to0$. A
pressureless, clustering component — what the CMB requires. The amount is an integration
constant ($\rho=Q_0n$), so it is not predicted; §4.

**(c) The MOND scale, and its redshift law.** Since $p=K$ identically and
$\mathcal{A}\propto-K$,

$$\frac{a_0^2(z)}{a_0^2(0)}=\frac{\sqrt{1+\nu_0^2}}{\sqrt{1+\nu_0^2(1+z)^6}},
\qquad z_t=\nu_0^{-1/3}-1\in[17,35],\qquad \nu_0\in[2.14\times10^{-5},1.77\times10^{-4}]$$

— constant to <1% wherever MOND is tested ($z\lesssim5$), and **off at recombination**
($a_0(1090)/a_0(0)\approx0.002$–$0.006$) as an *output*. So the CMB's dust-like clustering
is a prediction, not an accommodation, and the observed absence of Tully–Fisher zero-point
evolution at $1<z<5$ is a pass (<2×10⁻⁴ dex).

## 3. What is verified

| # | result | status |
|---|---|---|
| 1 | **Lensing** — Φ = Ψ ⟹ γ_PPN = 1, M_dyn/M_lens = 1. The 21.2σ exclusion that killed modified inertia clears at **0.601σ** | committed |
| 2 | **Gravitational waves** — c_T = 1 *exactly* (algebraic in the metric; GW170817-safe). Equivalent to c₁ + c₃ = 0 | committed; re-derived independently (stage71) |
| 3 | **CMB** — full CLASS pass; re-run with the derived a₀(z) agrees to 0.01σ vs cosmic variance | committed |
| 4 | **RAR** — 0.108 dex on 175 SPARC galaxies at Υ = 0.70, with the anchored a₀ | committed |
| 5 | **Weak-lensing RAR, 40 kpc–2.2 Mpc** — pure framework, no dark component: χ²/dof = 2.03 canonical / 0.94 alt on real KiDS data; the same fit *rejects* adding one | committed |
| 6 | **Solar system** — Newtonian residual $e^{-\sqrt y}\approx10^{-3457}$ at Earth's orbit | committed |
| 7 | **No ghost, no gradient instability** — over the whole field range, *including* on a tilted, nonlinearly-excited collapse background | **stage68 (new)** |
| 8 | **Post-recombination growth** — P(k = 0.2) preserved, CLASS-validated integrator | **stage69 (new)** |
| 9 | **PPN preferred frame** — α₁ = −4K_B computed | **stage70 (new)** |
| 10 | **Wide binaries** — hash-frozen pre-registration, 10 amendments, γ_v = 1.1614–1.1814 / 1.1917–1.2267, decided by Gaia DR4 (~Dec 2026) | frozen before data |

### 3.1 The health matrix (stage68) — why it closes structurally

On FRW with no tilt, $Y=O(\delta\varphi^2)$, so the galaxy sector cannot appear in linear
perturbations at all. On a *collapse* background with a tilted aether both invariants are
excited at first order and the (Q, Y) sectors mix — the regime the corpus used and never
proved healthy. It is healthy, and for a reason internal to the promotion: because
$\mathcal{A}=\kappa^2G(-K)$, one has $\mathcal{A}''=-\kappa^2GK''$, so the mixing enters
the Hessian as a **multiplicative factor on** $K''$,

$$\Xi(z)=1-\frac{\kappa^2}{8\pi}\bigl(\mathcal{F}_Y-z\mathcal{F}_Y'\bigr),
\qquad \mathcal{F}_Y-z\mathcal{F}_Y'\in(-2,0]\ \Rightarrow\ \Xi\ge1 .$$

The promotion makes the theory *more* stable than the bare DBI (max Ξ = 1.0199, in the
Newtonian limit; exactly 1 in deep MOND), and the $\mathcal{A}'^2$ terms leave a strictly
positive residue in the determinant. All four Sylvester conditions hold for **every** tilt
and **every** excitation, with no tuning of $K_B,\mathcal{K}_2,\lambda_s,Q_0$. Every
collapse result that previously assumed health now inherits a proof.

### 3.2 The growth history (stage69) — and the bound it produced

The sound speed is not free: $c_s^2=R\,s(1-s^2)/(1+Rs)$ with $R\equiv\Lambda_D/Q_0$ and
$s(a)$ set by $\nu=\nu_0a^{-3}$. It is a genuine transient — zero at the DBI wall (early),
zero as the excitation drains (late), peaked between. CLASS confirms the danger is real: a
*constant* $c_s^2=10^{-4}$ suppresses P(k = 0.2) to **1.6%** of ΛCDM. Requiring the total
matter power within 3% gives

$$\boxed{\;\Lambda_D/Q_0\le1.5\text{–}3.1\times10^{-6}\quad\Rightarrow\quad
c_{s,\rm peak}^2\le1.2\times10^{-6}\;}$$

a constraint the theory had never carried. The corpus's separately quoted
$c_s^2\approx1.1\times10^{-8}$ sits ~100× inside it, so the theory passes — but the
"natural" choice $\Lambda_D=Q_0$ is **excluded by six orders**.

### 3.3 The preferred frame (stage70/71) — the tightest constraint on the theory

The aether term maps *exactly* onto the Einstein-aether class with
$c_1=K_B,\ c_2=0,\ c_3=-K_B,\ c_4=0$ (verified by coefficient matching; and $c_1+c_3=0$
independently reproduces result 2 above, which validates the identification). Then

$$\alpha_1=-\frac{8(c_3^2+c_1c_4)}{2c_1-c_1^2+c_3^2}=-4K_B
\qquad\Longrightarrow\qquad \boxed{\;K_B<2.5\times10^{-5}\;}$$

from lunar laser ranging — **four orders tighter than the corpus's BBN cap**, and it
excludes all three of Skordis & Złośnik's own published $K_B$ fits (0.5, 0.3, 0.1). The
theory survives because its quasi-static phenomenology is $K_B$-blind
($\tilde G=(1-K_B/2)\hat G_{qs}$; $K_B$ appears zero times in the QS equations), so results
4–6 and 10 are untouched — **but it survives by blindness, not by margin.** Two riders,
both honest: the PPN formula is literature-inherited (Foster & Jacobson 2006), and the
deciding calculation — the PPN expansion retaining AeST's $J^\mu\nabla_\mu\varphi$ coupling
— is owed. And $\alpha_2$, whose bound is 1000× tighter, cannot be inherited at all: the
theory sits on the $c_{123}=0$ locus where the spin-0 aether mode does not propagate, *and
it sits there because it is gravitational-wave safe* — $c_{13}=0$ and $c_{123}=0$ are the
same algebraic fact.

## 4. The complete parameter ledger

| symbol | role | status |
|---|---|---|
| **κ** | the acceleration-scale coefficient | **FITTED**, ½ adopted; measured 0.551 ± 0.043 (distance-free), 0.465 ± 0.076 (BTFR), 0.537 ± 0.071 (gas-dominated, TRGB distances); combined 0.53–0.55. **Not derived** — six derivation classes closed (§5) |
| **β** = μ²Λ_D²/M⁴ | fixes the DBI wall | **SELECTED** = 1 (the Lagrangian vanishes at the wall), not derived |
| **M⁴** | vacuum scale | = ρ_Λ by the normalisation condition |
| **ν₀** | dimensionless charge today | window [2.14×10⁻⁵, 1.77×10⁻⁴], cut from below by the CMB off-switch and above by the RAR |
| **Q₀** | background scalar rate | **PINNED** 0.0024–0.0146 Mpc⁻¹ from galaxy phenomenology (DOI 10.5281/zenodo.21937958) — CANDIDATE-grade value, derivation-grade identification |
| **Λ_D/Q₀** | wall height / rate | **≤ 1.5–3.1×10⁻⁶** (§3.2, new) |
| **K_B** | aether kinetic coefficient | **< 2.5×10⁻⁵** (§3.3, new; was ≤ 0.25 from BBN) |
| **𝓚₂, λ_s** | free | 𝓚₂ pinned to ~3 decades; λ_s free |
| **I₀** | the dark-matter *amount* | an integration constant — **not predicted**, exactly as AeST's authors state |

Five dark-sector parameters against ΛCDM's two. Three of the five now carry
quantitative bounds that did not exist a week ago.

## 5. What is not claimed

1. **κ = ½ is not derived.** Six classes of derivation are now closed by explicit
   calculation: published dS-thermodynamic routes (0 of 4 forced coefficients in the
   measured window), GHY-to-bulk action ratios (0 of 3), linear-response functions in the
   dS-Unruh balance, first-law smearings (choice-dependent, spread 0.36), the q-deformed
   Deser–Levin mirror, and the ε_tot = 1/(32π) enumeration (3 matches vs 2.23 expected by
   chance). A small obstruction theorem holds: every non-trivial dimensionless π-free
   *monomial* in the horizon generators carries a free geometric parameter, so the only
   parameter-free survivor is the trivial 1. **Three routes remain open**: non-monomial
   combinations, a theory-fixed radius ratio, and a combinatorial factor of 2.
   And the honest evidential status: the π-cancellation is *logically identical* to κ = ½
   (not independent support); at ±7.8% every natural parameterisation of the dS scale
   admits a simple rational; under a 1/q² simplicity prior ½ leads by ~6:1. **κ must reach
   ±3.7% for ½ to be the unique simple rational at 3σ** — a 2.1× improvement, and the test
   is two-sided.
2. **Dark matter exists at full Ω_dm.** The only slogan is "no dark-matter *particle*."
   Whether galaxies *keep* their captured charge is the framework's central open problem
   (§6).
3. **This is not a theory of everything** and no part of it addresses the Standard Model.
   The 2026-06-23 retraction stands.
4. **Cassini Q₂ is inherited** (3–15σ) and is not relieved by anything here.
5. **α₂ is uncomputed** and its bound is the tightest in the PPN table (§3.3).

## 6. The open problem, stated as such

The dark sector is a shift-symmetric condensate with a conserved charge. That single
property gives $w=-1$ exactly, makes the excitation dust, and is what the CMB measures —
and it is also what forbids the excitation from behaving differently inside galaxies:
$\rho=Q_0n$ locks the dust mass to the conserved charge; dynamics sees $\rho+3p$ while
lensing sees $\rho+p$, so no equation of state hides energy from both; and
$c_s^2\propto a^{-3}$ for every ghost-free $K$, so it cannot be kept warm. **The
dark-energy triumph and the galaxy-scale problem are the same property of the same field.**

Mechanisms tried and closed: Route A′ (empty γ range), the Cell-3 pressure reading (dead
three ways), the Cell-3 transport reading (conditional-dead by a fixed-point argument
against the theory's own Q₀ pin). Live: Cell 1 at (2,0) marginal under flow pricing, and a
genuine second sector carrying the pressure — a structural change, not a new free function.

## 7. Reproducibility

Every number is produced by a committed script at
<https://github.com/carlzimmerman/zimmerman-formula>. The new results in this document:
`nbody_2026/stage68_health_matrix_tilted_2026.py` (health matrix, 13/13),
`stage69_cs2_growth_class_2026.py` (growth + CLASS, 14/14),
`stage70_ppn_preferred_frame_2026.py` (α₁, 11/11),
`stage71_ppn_alpha2_degeneracy_2026.py` (the α₂ degeneracy, 13/13),
`stage65/66/67` (the κ programme, its evidential audit, and the precision path),
`real_research/kappa_gas_dominated_2026.py` (the gas-dominated κ, 18/18).
Withdrawn claims are recorded, dated, in `RETRACTIONS.md`.

**Attribution.** AeST is Skordis & Złośnik (PRL **127** 161302, arXiv:2007.00082). The
interpolation is Milgrom & Sanders 2008, Eq. (13) at α = ½. The a₀–Λ tie has prior art in
Milgrom (1999), Pikhitsa (2010), Klinkhamer & Kopp (2011), Blanchet & Le Tiec (2009) and
Singh (2026). PPN aether formulas are Foster & Jacobson (2006). This programme contributes
the normalisation, the pressure promotion, the derived a₀(z), the Q₀ pin, and the bounds of
§3.2–3.3.
