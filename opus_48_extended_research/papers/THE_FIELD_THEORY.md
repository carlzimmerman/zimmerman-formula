# The Field Theory: One Action, One Normalisation, Three Outputs

**Carl P. Zimmerman**, Briar Creek Tech
ORCID 0009-0008-3508-7982
v2, 2026-08-17

> **What this document is.** A single self-contained statement of the field theory: the
> action, the one normalisation condition it needs, the three things it then predicts, the
> complete list of what is fitted and what is free, and every open liability with its
> current status. It supersedes nothing — THE_COMPLETION v9 (DOI 10.5281/zenodo.21895046)
> remains the detailed record — but where the two disagree, **this document is newer**.
>
> **What changed to make it writable.** Two structural liabilities that had been open since
> the theory was assembled were closed on 2026-08-16/17: the perturbation health matrix on a
> tilted, nonlinearly-excited background (stage68) and the post-recombination growth history
> with an evolving sound speed (stage69, run against real CLASS).
>
> **What v2 changed, and it is mostly against the theory.** Six adversarial reviews ran in
> parallel on 2026-08-17. The v1 headline — that the PPN parameter α₁ = −4K_B gives a bound
> four orders tighter than anything the corpus carried — **did not survive**: an independent
> from-scratch derivation gets α₁ = α₂ = 0 for the same sector, the two disagree because the
> theory sits on a degenerate locus where the literature's premises fail, and §3.3 now
> reports a fork rather than a result. The Lyman-α forest tightened the sound-speed bound by
> a further factor of 672, leaving 1.08 of 3.65 decades of the theory's own window. The
> distance-free κ turns out to carry an unpriced ~7% H₀ systematic. Two candidate mechanisms
> — the curl-sector route to clusters and the whole second-field escape for the dust problem
> — were priced and died. Nothing in this round touched a₀ = κc√(Gρ_Λ), the RAR, lensing, or
> the frozen Gaia DR4 band; the risk that surfaced is in the **adopted relativistic home**,
> not in the normalisation claim.

---

## 0. The theory in one equation

$$\boxed{\;
S=\int\! d^4x\sqrt{-g}\left\{\frac{R-\tfrac{K_B}{2}F^{\mu\nu}F_{\mu\nu}
+2(2-K_B)J^\mu\nabla_\mu\varphi-(2-K_B)Y}{16\pi G}
\;+\;\frac{\kappa^2\mathcal{P}}{8\pi}\,\mathcal{F}_Y\!\!\left(\frac{Y}{\kappa^2G\,\mathcal{P}}\right)
\;-\;\mathcal{P}\right\}+S_{\rm m}[g,\psi]\;}$$

$$\mathcal{P}(Q)\;=\;M^4\sqrt{1-\frac{(Q-Q_0)^2}{\Lambda_D^2}}\,,\qquad
Q\equiv A^\mu\nabla_\mu\varphi,\qquad
Y\equiv(g^{\mu\nu}+A^\mu A^\nu)\nabla_\mu\varphi\nabla_\nu\varphi,$$

$$A^\mu A_\mu=-1,\qquad \frac{d\mathcal{F}_Y}{dz}=1-e^{-\sqrt z},\qquad
M^4=\rho_\Lambda c^2,\qquad \kappa=\tfrac12\ \text{(fitted)}.$$

**How to read it, in four lines.**

1. The numerator of the first term is **Aether-Scalar-Tensor gravity** (Skordis & Złośnik
   2021): general relativity, plus a unit-timelike vector $A^\mu$ that carries a cosmic
   frame, plus a scalar $\varphi$. Matter couples to $g_{\mu\nu}$ alone — which is why
   lensing and dynamics agree with no dark halo ($\Phi=\Psi$, $\gamma_{\rm PPN}=1$).
2. $\mathcal{P}$ is the **entire dark sector, and it is a brane**: $-\mathcal{P}$ is the
   Dirac–Born–Infeld action $-M^4\sqrt{1-\dot\varphi_{\rm rel}^2}$, with $M^4=\rho_\Lambda c^2$
   its tension. (This is what the selection $\beta\equiv\mu^2\Lambda_D^2/M^4=1$ *means*: the
   dark sector's Lagrangian is exactly a brane volume element, nothing added.) At its
   minimum $Q=Q_0$ it is a cosmological constant with $w=-1$ **exactly**; small excitations
   have energy density linear in the displacement, i.e. **dust** — the dark matter the CMB
   requires; and at the wall $|Q-Q_0|\to\Lambda_D$ the pressure vanishes, killing any early
   stiff phase.
3. The middle term is **MOND**, and its acceleration scale is not a new constant:
   $$a_0^2=\kappa^2G\,\mathcal{P}\qquad\text{— the MOND scale \emph{is} the dark sector's pressure.}$$
   That single identification is the programme's contribution. Evaluated today
   ($Q=Q_0$, $\mathcal{P}=M^4=\rho_\Lambda c^2$) it gives
   $a_0=\kappa c\sqrt{G\rho_\Lambda}=9.36\times10^{-11}\ \mathrm{m\,s^{-2}}$; evaluated in
   the past, where the field has climbed the brane wall and $\mathcal{P}$ is smaller, it
   gives a *derived* $a_0(z)$ that is flat below $z\approx20$ and switches off before
   recombination.
4. $\mathcal{F}_Y$ is the interpolation function (Milgrom & Sanders 2008, $\alpha=\tfrac12$),
   the only thing borrowed from MOND phenomenology.

**Why a physicist should care about the shape of it.** One bounded function $\mathcal{P}$
does three jobs that are normally done by three independent sectors — dark energy, dark
matter, and the MOND scale — and it does them without a single new adjustable function:
the *same* $\mathcal{P}$ that is the vacuum energy today is the dust that clusters at
recombination and the acceleration scale that bends rotation curves. The cost is stated
just as plainly in §4–§6: $\kappa$ is fitted, $\beta=1$ is selected, the dark-matter
*amount* is an integration constant, and whether the dust stays put inside galaxies is
unsolved.

---

## 1. The action, term by term

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
| 8 | **Post-recombination growth** — P(k = 0.2) preserved, CLASS-validated integrator; extended into the Lyman-α forest band, which tightens the bound 672× | **stage69 + forest review (new)** |
| 9 | **PPN preferred frame** — α₁ computed *twice, independently, with disagreeing answers*. This is a **fork, not a result** (§3.3) | **stage70/71/72/73 (new, unresolved)** |
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

$$\Lambda_D/Q_0\le1.5\text{–}3.1\times10^{-6}\quad\Rightarrow\quad
c_{s,\rm peak}^2\le1.2\times10^{-6}$$

a constraint the theory had never carried, and the "natural" choice $\Lambda_D=Q_0$ is
**excluded by six orders**.

**Then the Lyman-α forest tightened it by another factor of 672.** The suppression obeys a
one-parameter scaling theorem — $T^2$ depends on $(k,R)$ only through $x=k^2R$, so the
extrapolation from $k=0.2$ to $k=10\,h\,$Mpc⁻¹ is *exact* rather than heuristic — and the
integrator was re-validated against CLASS *inside* the forest band (≤ 0.0055 absolute,
$k=1$–10, $z=2$–4), using a matched cold-vs-warm fluid ratio so the earlier 2–3% transfer
artifact cancels. Against the 3.1 keV warm-dark-matter yardstick (Iršič et al. 2017;
Villaseñor et al. 2023, 95% CL) the bound becomes

$$\boxed{\;\Lambda_D/Q_0\le2.3\times10^{-9}\;}\qquad
\text{honest bracket }5.7\times10^{-10}\text{–}7.0\times10^{-9}.$$

Two things follow, one each way. **Adverse:** with $Q_0=1$ the committed health window
$\Lambda_D\in(1.9\times10^{-10},8.4\times10^{-7}]$ *is* the $R$ window, and the forest
removes its top 2.56 of 3.65 decades. It survives with **1.08 decades left**, so
"Ly-α-safe *by construction*" is withdrawn — it is safe in the bottom decade of the
theory's own window, on a condition that is new. **Favourable and structural:**
$c_s^2(z=1090)=1.9\times10^{-11}R$, i.e. $2\times10^{-11}$ of its own peak, so there is
**no primordial cutoff at all** — this is not warm dark matter in disguise, and the
suppression is generated entirely *after* the DBI wall.

*Correction filed against this section's own earlier basis:* stage69 argued the theory
passes because the corpus quoted $c_s^2\approx1.1\times10^{-8}$, read as implying
$R\sim3\times10^{-8}$. That number is an **epoch** statement computed at $R=1$ (where
$c_s^2=2w^2$, reproducing $1.1\times10^{-8}$ to 3.1%), and $R=1$ is excluded by stage69's
own bound. The pass is real; the stated basis for it was not. There is no independent
small-$R$ normalisation anywhere in the corpus.

One fork is still open and it flips the verdict: if the excitation *is* the dark matter
($I_0\approx\Omega_{\rm dm}$, the reading this document takes) everything above holds; if
instead the conserved charge is a trace component ($\Omega_{kd}\le4.4\times10^{-7}$) the
forest goes silent — but then Ly-α safety is *inherited from assuming* a cold carrier for
the other 0.265, which concedes the open problem of §6. The two readings are
$1.4\times10^{10}$ apart in $R$; one conserved charge cannot be both.

### 3.3 The preferred frame — an unresolved fork, reported as one

This section previously reported $K_B<2.5\times10^{-5}$ as the tightest constraint on the
theory. **An independent from-scratch derivation disagrees, and the disagreement is
structural.** What follows is the fork, both branches priced.

The aether term maps *exactly* onto the Einstein-aether class with
$c_1=K_B,\ c_2=0,\ c_3=-K_B,\ c_4=0$. This much is settled — three independent derivations
agree (coefficient matching; a symbolic $F^2$ expansion; and `euler_equations` from
scratch). It puts the theory on a **doubly degenerate locus**: $c_1+c_3=0$ (which is why
$c_T=1$ exactly, result 2) *and* $c_{123}=0$, where the spin-0 aether mode has **zero**
propagation speed. These are the same algebraic fact: the theory is gravitational-wave safe
*because* it is degenerate.

**Reading L (literature map).** Foster & Jacobson's generic formula, evaluated on the
dictionary — and its denominator does *not* vanish there, which is why this was banked:

$$\alpha_1=-\frac{8(c_3^2+c_1c_4)}{2c_1-c_1^2+c_3^2}=-4K_B
\qquad\Longrightarrow\qquad K_B<2.5\times10^{-5}\ \text{(lunar laser ranging)}.$$

**Reading D (from scratch, no literature formula, constraints respected).**
$\alpha_1=\alpha_2=0$ identically, for every $K_B$. Two independent routes force
$\lambda\,(w\!\cdot\!\hat k)=0$: antisymmetry of $F^{\mu\nu}$ gives
$\nabla_\nu(\lambda A^\nu)=0$, and $G^{(1)}_{3\nu}\equiv0$ for $z$-only perturbations makes
the four $(3,\nu)$ Einstein equations pure *constraints*. For generic $k$ this forces
$\lambda=0$ and hence the exact GR metric of static dust, with no $w$-dependence anywhere.

**Where they part company, and why neither may be banked.** The literature PPN analysis
assumes every aether mode propagates, so that the static solution is unique and decaying.
At $c_{123}=0$ the spin-0 mode has zero speed, a static source resonantly drives it, and the
solution acquires a non-normalisable wake $v_L\sim U/(ik\,w\!\cdot\!\hat k)$ — a simple pole
with nonzero residue, violating $A\to A_{\rm bg}$ at infinity. So reading L applies a generic
formula off its domain of validity, and reading D buys zero at the price of a pathological
solution. Worse, reading D finds $g_{00}$ has **no Taylor series in $w$** at all: at $w=0$
exactly, $\lambda\ne0$ and $G_N=G/(1-K_B/2)$, so the $w^0$ coefficient itself jumps —
$\alpha_1,\alpha_2$, *defined* as the $O(w^2)$ coefficients, do not exist in the usual
sense. (A third reading, recorded and explicitly not claimed: discarding the constraints and
freezing $\lambda$ at its $w=0$ value gives $\alpha_1=+3K_B/2$, $\alpha_2=+K_B/2$ —
opposite in sign to reading L.) One favourable note on reading D's credibility: its $w=0$
branch independently reproduces $G_N=G/(1-K_B/2)$, i.e. AeST's quasi-static
$\tilde G=(1-K_B/2)\hat G$, a number already on record from an unrelated calculation.

**Why the fork matters beyond PPN: it decides whether the vector sector is internally
consistent.** The corpus has said the quasi-static sector is "$K_B$-blind." That is true of
every *observable* — $\tilde G$, $\mu^2=2\mathcal{K}_2Q_0^2/(2-K_B)$, $r_C$, the RAR, the
a₀-line, lensing, the BTFR, the frozen DR4 band are all regular as $K_B\to0$ — but **false
of the sector**: 5 of 14 $K_B$-carrying quantities diverge, among them the scalar sound
speed and the curl scale, and by a new exact identity they are the *same* divergence,

$$c_s^2=\frac{4m_\times^2}{(2-K_B)\mu^2}\Bigl(1+\tfrac{K_B\lambda_s}{2}\Bigr)
\ \xrightarrow{\,K_B\ \rm small\,}\ 2\Bigl(\frac{m_\times}{\mu}\Bigr)^{2},$$

so the scalar is subluminal **iff** $1/m_\times\ge\sqrt2/\mu$. Since $\mu$ is regular and
CMB-pinned at $\mu^{-1}\gtrsim1$ Mpc, driving $K_B$ down drives the scalar superluminal and
drags the curl scale into the galaxy. Solving $c_s^2=1$ gives a **subluminality floor**
$K_B\ge2/(\mathcal{K}_2+1)$ — a *lower* bound, pointing the opposite way to every PPN bound.
Hence:

| | reading L ($K_B<2.5\times10^{-5}$) | reading D (no ceiling) |
|---|---|---|
| $c_s^2$ at SZ21's own MOND-compatible fits | 8.4–10.7, i.e. $c_s=2.9$–$3.3\,c$ | $2.8\times10^{-4}$–$2.1\times10^{-3}$, subluminal |
| subluminality floor $2/(\mathcal{K}_2+1)$ | $2.1$–$2.7\times10^{-4}$ = **8.4–10.7× above the ceiling ⟹ window empty** | not binding |
| escape | needs $\mathcal{K}_2\ge8\times10^4$, i.e. 8.4× above SZ21's largest fit — which fights the $\mu^{-1}\gtrsim1$ Mpc pin | — |
| $1/m_\times$ on the generic-$\alpha_2$ branch ($K_B<5\times10^{-8}$) | 15–93 kpc: the curl scale would sit **inside galaxies**, and $c_s\sim65$–$73\,c$ | — |

Read instead as a floor $2(Q_0/\mu)^2$ at the theory's *own* pinned $Q_0$, the window is
**open by 2.2× at the low edge and closed by 17× at the high edge** — genuinely knife-edge,
and decided by pinning $Q_0$, which is an owed item rather than a new assumption. One more
honesty note: the corpus cannot bank both this and DOORA_PIN's Serra–Trombetta "robust
pass," which requires $c_s^2\ge1$ — that is the *same* inequality read from the other side.

**Verdict.** The PPN door is open in both directions, not closed.
$K_B<2.5\times10^{-5}$ is demoted from a result to one branch of a fork. **The deciding
calculation is the one both derivations independently named as owed: redo the expansion with
the scalar sector retained** — $2(2-K_B)J^\mu\nabla_\mu\varphi$ and $-(2-K_B)Y$ — since that
is what lifts the $c_{123}=0$ degeneracy. Until then no $\alpha_1$ bound on $K_B$ is quoted
here as in force, in either direction. What is *not* affected either way: κ, $a_0$, β, the
kernel and the promotion appear zero times in this analysis. The risk located here is in the
**adopted relativistic home**, and it can neither be traded away by adjusting κ nor blamed
on it.

## 4. The complete parameter ledger

| symbol | role | status |
|---|---|---|
| **κ** | the acceleration-scale coefficient | **FITTED**, ½ adopted; measured 0.551 ± 0.043 (distance-free), 0.465 ± 0.076 (BTFR), 0.537 ± 0.071 (gas-dominated, TRGB distances); combined **0.529 ± 0.034 as published, 0.547 ± 0.034 on a Planck-consistent distance rescale** (0.9σ / 1.4σ from ½). Must be quoted **with its H₀** — see the note below. **Not derived** — six derivation classes closed (§5) |
| **β** = μ²Λ_D²/M⁴ | fixes the DBI wall | **SELECTED** = 1 (the Lagrangian vanishes at the wall), not derived |
| **M⁴** | vacuum scale | = ρ_Λ by the normalisation condition |
| **ν₀** | dimensionless charge today | window [2.14×10⁻⁵, 1.77×10⁻⁴], cut from below by the CMB off-switch and above by the RAR |
| **Q₀** | background scalar rate | **PINNED** 0.0024–0.0146 Mpc⁻¹ from galaxy phenomenology (DOI 10.5281/zenodo.21937958) — CANDIDATE-grade value, derivation-grade identification |
| **Λ_D/Q₀** | wall height / rate | **≤ 2.3×10⁻⁹** (§3.2; bracket 5.7×10⁻¹⁰–7.0×10⁻⁹). Leaves 1.08 of the health window's 3.65 decades |
| **K_B** | aether kinetic coefficient | **UNRESOLVED** (§3.3): ≤ 0.25 from BBN, and either < 2.5×10⁻⁵ (reading L, which then collides with a subluminality floor 8–11× above it) or unbounded by PPN (reading D). Do not quote a single value |
| **𝓚₂, λ_s** | free | 𝓚₂ pinned to ~3 decades — and under reading L it must exceed 8×10⁴ for the K_B window to be non-empty at all; λ_s free, and it *cannot* rescue subluminality (it pushes c_s² up) |
| **I₀** | the dark-matter *amount* | an integration constant — **not predicted**, exactly as AeST's authors state |

Five dark-sector parameters against ΛCDM's two. Two of the five now carry quantitative
bounds that did not exist a week ago; a third (K_B) turned out to be **contested rather than
bounded**, which is a worse position than the one this ledger reported previously.

**On κ and H₀ — an unpriced systematic, stated as such.** κ ∝ h^(2q_eff − p) with
q_eff ≡ ½ dln a₀/dln h, so it is H₀-invariant *iff* q_eff = p/2 = 0.500 (fixed Ω_Λ) or 0.730
(fixed ω_m). Neither estimator sits there. The distance-free number is the more exposed of
the two: 97 of 175 SPARC galaxies sit on Hubble-flow distances at H₀ = 73 while the
denominator c√(Gρ_Λ) is Planck-footed, and a Planck-consistent rescale moves a₀ by +6.5–7.3%
— **4.0× its 1.84% statistical error, against an error budget that charges 0% for distance
scale.** The BTFR is *less* exposed than a naive count suggests (q_eff = +0.202, the distance
*weight* fraction, not the 0.583 count) and its budget already charges 5.06% > the 3.26%
offset, so its width was honest. What this establishes is an **understated error bar, not a
direction**: the self-consistent range for the distance-free number is [0.492, 0.589] and the
committed 0.551 sits inside it, not at an edge.

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
5. **The preferred-frame parameters are contested, not computed.** Two independent
   derivations disagree about α₁ and the theory may not have a well-defined static PPN limit
   at all (§3.3). No K_B bound from PPN is in force in either direction.
6. **Ly-α safety is conditional, not "by construction."** It holds in the bottom 1.08
   decades of the theory's own Λ_D window (§3.2), and only under the reading in which the
   excitation *is* the dark matter.
7. **No cluster mechanism has been found.** The curl-sector route is dead — not on K_B (which
   helps it) but on geometry: an exact pointwise cancellation makes the saturated tilt a pure
   gradient with zero curl, and the divergence theorem makes the monopole effect exactly
   O(ε²). The shortfall is 8.0× at an absolute floor with every generous assumption stacked,
   ~176× centrally. The a₀-bump remains the only live candidate. Two by-products, one each
   way: a real framework-specific *prediction* survives (a merger/ellipticity-gated rider
   η − 1 ∝ ε² at 0.1–10%, with no free amplitude, which no isotropic bump can mimic), and a
   new **adverse** channel is escalated (the longitudinal tilt suppresses Y by T² = 0.07–1.28
   at cluster scales, making the deficit worse — conditional on reading L).

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
against the theory's own Q₀ pin).

**The second-field escape has now been catalogued and all four candidates are dead** — a
second shift-symmetric k-essence (killed by ρ = Q₀n and by its stiffness), an ungated Proca
on the shift current in both the contact and long-range limits (ungating does not evade the
support bound; it *is* the saturating endpoint), a field entering only the promotion (killed
by the promotion's own order counting, with no external leg needed), and a fourth built
specifically to clear all three known legs, which cleared them and then died on a **sign**:
a gate built from |∇φ| *rises* outward wherever the held dust dominates its own field, so any
monotone gate anti-supports 99.27% of the held mass, and the equilibrium truncates at 653 kpc
piling up 55–61% of the theory's own lensing mass inside the range where it is already fitted.
Two reusable theorems came out of it: at Γ = 4/3 — the dynamical-stability boundary itself —
the support violation is **calibration-independent** at 1.16×10³× the cap; and
r_×/R_supp = [M_bar/((π²/3)M_dust)]^(1/3) = 0.194, fixed by the baryon-to-dust ratio alone,
which any future attempt should test *first* because it is free.

So the escape space for this problem is now narrower, not wider. Live: Cell 1 at (2,0),
marginal under flow pricing. The honest summary is that the theory's central open problem
became harder this week, and none of the routes tried closed it.

## 7. Reproducibility

Every number is produced by a committed script at
<https://github.com/carlzimmerman/zimmerman-formula>. The new results in this document:
`nbody_2026/stage68_health_matrix_tilted_2026.py` (health matrix, 13/13),
`stage69_cs2_growth_class_2026.py` (growth + CLASS, 14/14),
`stage70_ppn_preferred_frame_2026.py` (α₁, 11/11),
`stage71_ppn_alpha2_degeneracy_2026.py` (the α₂ degeneracy, 13/13),
`stage73_ppn_kb_confrontation_2026.py` (**the fork of §3.3 and how the six results
interact, 35/35**),
`stage65/66/67` (the κ programme, its evidential audit, and the precision path),
`real_research/kappa_gas_dominated_2026.py` (the gas-dominated κ, 18/18), and the six
adversarial reviews in `real_research/reviews/`:
`ppn_alpha_independent_check_2026.py` (α₁, α₂ from scratch with no literature formula,
26/26 — the derivation that opened the fork),
`kb_small_limit_safety_2026.py` (the K_B → 0 census, 33/33),
`lyman_alpha_dust_ic_2026.py` (the forest bound, 22/22),
`kappa_h0_convention_audit_2026.py` (the H₀ exposure, 24/24),
`curl_sector_cluster_pricing_2026.py` (the dead cluster route, 27/27),
`second_field_catalog_2026.py` (the four dead second-field candidates, 47/47).
Withdrawn claims are recorded, dated, in `RETRACTIONS.md`.

**Attribution.** AeST is Skordis & Złośnik (PRL **127** 161302, arXiv:2007.00082). The
interpolation is Milgrom & Sanders 2008, Eq. (13) at α = ½. The a₀–Λ tie has prior art in
Milgrom (1999), Pikhitsa (2010), Klinkhamer & Kopp (2011), Blanchet & Le Tiec (2009) and
Singh (2026). PPN aether formulas are Foster & Jacobson (2006). This programme contributes
the normalisation, the pressure promotion, the derived a₀(z), the Q₀ pin, and the bounds of
§3.2–3.3.
