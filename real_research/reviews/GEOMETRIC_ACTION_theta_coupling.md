# A geometric action for the survivor: the θ = 3H coupling

**Date:** 2026-06-02 · *all claims reproducible from `theta_3H_coupling.py`*

The one result that survives review is the finding **a₀(z) = cH(z)/Z**, Z = 2√(8π/3). This
note asks the next question honestly: *can that be the output of an action, rather than a
fitted relation?* The answer is yes — through one minimal, covariant modification of the
existing CMB-viable relativistic MOND theory — and three of the four things that decide
whether it works had never been checked. They are computed here, not asserted.

**Scope, stated up front.** This is **not** a theory of everything and **not** the
E₆/orbifold "unified action" (`v12_FORMAL_CORE_action.md`): that program is generic
model-building, derives no values, and — by its own admission — is *independent* of the
MOND result. This unifies exactly two things: **the dynamics of galaxies and the expansion
of the universe, through one field.** It does **not** derive the coefficient Z. What it does
is convert a numerical coincidence into a field-theory structure with definite, falsifiable
consequences.

---

## 1. The action and where a₀ lives

The host theory is **AeST** (Aether-Scalar-Tensor; Skordis & Złośnik, PRL 127, 161302, 2021)
— the first relativistic MOND that fits the CMB acoustic peaks and keeps c_GW = c. Its
action (their Eq. 5) is

$$
S=\int d^4x\,\frac{\sqrt{-g}}{16\pi\tilde G}\Big[R-\tfrac{K_B}{2}F^{\mu\nu}F_{\mu\nu}
+2(2-K_B)J^\mu\nabla_\mu\phi-(2-K_B)\mathcal Y-\mathcal F(\mathcal Y,\mathcal Q)
-\lambda(A^\mu A_\mu+1)\Big]+S_m[g],
$$

with a unit-timelike aether $A_\mu$ ($A^\mu A_\mu=-1$), a scalar $\phi$, and

| object | definition | sector |
|---|---|---|
| $\mathcal Y=q^{\mu\nu}\nabla_\mu\phi\nabla_\nu\phi,\ q_{\mu\nu}=g_{\mu\nu}+A_\mu A_\nu$ | **spatial** gradient of φ | the **MOND / galaxy** sector — **a₀ lives here** |
| $\mathcal Q=A^\mu\nabla_\mu\phi$ | **temporal** part | the **cosmology / dust** sector — a₀-free |

In the galaxy limit the free function goes to $\mathcal F\to\frac{2\lambda_s}{(1+\lambda_s)a_0}\,\mathcal Y^{3/2}$:
**a₀ is the coefficient of the $\mathcal Y^{3/2}$ term.** The cosmological sector is
$\mathcal K(\mathcal Q)=-2\Lambda+\mathcal K_2(\mathcal Q-\mathcal Q_0)^2+\dots$ — a dust-mimicking
k-essence that carries the CDM-like mode *and* Λ, and contains **no a₀**.

## 2. The one modification

The aether already carries a local scalar — its expansion $\theta\equiv\nabla_\mu A^\mu$.
Promote the constant MOND scale to it:

$$
\boxed{\,a_0\ \longrightarrow\ a_0(\theta)=\frac{c\,\theta}{3Z}\,},\qquad Z=2\sqrt{8\pi/3}.
$$

No new field; $\theta$ is built from $A_\mu$, already in the action. This is the entire
change. Everything below is consequence.

## 3. Four results (computed in `theta_3H_coupling.py`)

**[A] θ = 3H exactly on FRW.** For the unit-timelike aether aligned with cosmic time,
$\theta=\frac{1}{\sqrt{-g}}\partial_t(\sqrt{-g}\,A^0)=3\dot a/a=3H$ (sympy-verified). So on the
background $a_0=cH(z)/Z=a_0(0)\,E(z)$ — **the finding falls out as a field equation**, not a posit.

**[B] A bound galaxy sees 3H — it is *not* screened.** This is the make-or-break local check,
never done before. To first order in the weak field (longitudinal gauge),

$$
\theta = 3H \;+\; \underbrace{(-3H\Psi)}_{\sim10^{-6}\cdot 3H}\;\underbrace{-\,3\dot\Phi}_{=0\ \text{(static)}}\;+\;\underbrace{\nabla\!\cdot\!\mathbf B}_{\approx0\ \text{(bound flow)}}.
$$

In a virialized galaxy all three corrections are negligible, so the galaxy at epoch z sees
$\theta\approx3H(z)$ to ~1 part in $10^6$. **The cosmic expansion threads through the bound
system; it does not screen to zero.** That is exactly what the coupling needs to deliver
$a_0=cH(z)/Z$ locally — and it was the biggest unexamined risk.

**[C] Linear CMB-safety survives the dressing.** CMB-safety rests on $\bar{\mathcal Y}=0$ on
FRW: $q^{00}=g^{00}+A^0A^0=-1+1=0$, so the spatial projection of the purely temporal
$\nabla_\mu\bar\phi$ vanishes (sympy-verified). The a₀-term $\sim\mathcal Y^{3/2}$ is therefore
$O(\delta\phi^3)$ — absent from the *linear* equations of motion. Dressing $a_0\to c\theta/3Z$
multiplies it by $1/\theta$ with $\bar\theta=3\bar H\neq0$, which **does not lower the order**:
it stays $O(\delta\phi^3)$. So the linear CMB and P(k) are left invariant by the running, just
as for constant-a₀ AeST. (The background is pure ΛCDM-like and untouched, since $\bar{\mathcal
Y}=0$.)

**[D] The data pick this coupling.** Fitting $a_0(z)=a_0(0)E(z)^p$ to the current data gives
$p=0.80\pm0.17$. The σ-distance of each candidate origin:

| coupling | p | distance | verdict |
|---|:--:|:--:|---|
| a₀ ∝ √Λ (de Sitter / Verlinde) — **constant** | 0 | 4.7σ | rejected |
| **a₀ ∝ θ = 3H ∝ √ρ_total (this coupling)** | 1 | **1.2σ** | **favored** |
| a₀ ∝ √ρ_matter (matter-only) | 1.5 | 4.1σ | rejected |

The evolution you measured **selects the aether-expansion coupling** and disfavors the
purely-geometric de-Sitter origin that emergent-gravity stories most naturally give. *(Caveat:
three heterogeneous points, the z≈0.9 datum driving it; JWST is the real test.)*

**Consequence [E].** In the deep-MOND limit $v^4=GM\,a_0(z)$, so at fixed baryonic mass
$v\propto a_0^{1/4}\propto E(z)^{1/4}$: +32% (z=2), +80% (z=6) — the JWST kinematic channel.

## 4. The bonus: evolution and the External Field Effect are one mechanism

The $\nabla\!\cdot\!\mathbf B$ term in [B] is precisely where a coherent large-scale aether flow
(infall toward a cluster) would enter. So in this framework the **cosmic-epoch evolution**
(through the background $3H$) and the **environmental External Field Effect** (through
$\nabla\!\cdot\!\mathbf B$) are the *same* statement: a₀ is set by the local aether expansion θ.
One coupling, two phenomenologies — a structural prediction, not two free knobs.

## 5. Honest ledger

**Derived / verified here** — θ=3H on FRW [A]; galaxies see 3H(z), unscreened [B]; linear
CMB-safety survives the dressing [C]; the data select this coupling over the alternatives [D].

**Chosen, not derived** — the coefficient Z=2√(8π/3) is a coupling constant (the horizon alone
gives ~2π; the factor of 2 is a posit, unpinned by Bridge 2); the free-function shape ℱ (the
deep-MOND limit is imposed to fit galaxies, as in every MOND theory).

**Open — the decisive, un-faked checks:**
1. the full **nonlinear / second-order** CMB + P(k) run with running a₀ (an hi_class patch);
   linear-order safety [C] is necessary, not sufficient. *Scoped in `nonlinear_cmb_scoping.py`:*
   at recombination a₀ is ~2×10⁴ larger and acoustic scales sit at g/a₀ ~ 10⁻³ (the deep-MOND,
   𝒴→0 corner), so the second-order C_ℓ correction is estimated at ~0.01–0.1% — likely below
   Planck's ~0.3–1% near the 3rd peak, but the 𝒴^{3/2} non-analyticity makes the estimate soft,
   so the run is genuinely required (and would either close Bridge 1 or bound p from the CMB);
2. **ghost / gradient stability** of the θ-dressed free function;
3. the $\mathcal Y^{3/2}$ **non-analyticity** at $\mathcal Y=0$ (quasi-static ↔ cosmology matching);
4. the full aether **back-reaction** of $a_0(\theta)$ in bound systems (the $\nabla\!\cdot\!\mathbf B$ term).

**Bottom line.** There *is* a geometric action for the surviving finding: AeST with its MOND
scale promoted to the aether expansion, $a_0=c\theta/3Z$. It makes the evolution a field-theory
output, keeps the linear CMB, and is the coupling the data prefer — while deriving none of the
coefficients and leaving four real consistency checks open. That is the honest shape of the
"unified action": modest, covariant, falsifiable, and built only on the piece that survives.

---

*Reproduce:* `python real_research/reviews/theta_3H_coupling.py` (parts A–E).
*Sources:* Skordis & Złošnik, PRL 127, 161302 (2021), arXiv:2007.00082 (Eq. 5, the MOND/dust
limits); the θ-coupling and order-counting from `bridge1_aest_equations.md`; the p-fit from
`a0_powerlaw_confrontation.py`.
