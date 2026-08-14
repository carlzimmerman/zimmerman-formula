# Bridge 1: the AeST equations, sourced from the paper, with the θ-coupling spelled out

**2026-06-01.** To finish Bridge 1 honestly we need the *actual* Skordis–Złośnik equations, not
a reconstruction. These are transcribed from **Skordis & Złośnik, PRL 127, 161302 (2021),
arXiv:2007.00082** (ar5iv HTML). **Fidelity caveat:** these came through a web fetch that
*summarizes* LaTeX, so the **exact numerical coefficients must be checked against the PDF**
before coding (one example flagged below). The *structure* — which is what the Bridge-1 argument
turns on — is clear and consistent across two independent fetches.

**UPDATE 2026-08-14: the caveat above is DISCHARGED.** The perturbation section below is now
completed **verbatim from the arXiv LaTeX source** (`arxiv.org/e-print/2007.00082` →
`newRMONDLett.tex`), closing the four load-bearing omissions that stage 57 identified as the root
cause of the stage-55 withdrawal, and resolving the flagged coefficient (the factor 3 is present).

---

## The action (Eq. 5)

$$S = \int d^4x\,\frac{\sqrt{-g}}{16\pi\tilde G}\Big[R - \tfrac{K_B}{2}F^{\mu\nu}F_{\mu\nu}
+ 2(2-K_B)J^\mu\nabla_\mu\phi - (2-K_B)\mathcal Y - \mathcal F(\mathcal Y,\mathcal Q)
- \lambda(A^\mu A_\mu + 1)\Big] + S_m[g]$$

| symbol | definition | role |
|---|---|---|
| $A_\mu$ | unit-timelike vector (aether), $A^\mu A_\mu=-1$ via $\lambda$ | carries the cosmic frame; **its expansion θ=∇·A = 3H** is our coupling handle |
| $F_{\mu\nu}=2\nabla_{[\mu}A_{\nu]}$, coeff $K_B$ | vector kinetic term | keeps $c_{\rm GW}=c$ |
| $\phi$ | scalar | sources MOND (gradient) + dark matter (temporal) |
| $\mathcal Y = q^{\mu\nu}\nabla_\mu\phi\nabla_\nu\phi$, $q_{\mu\nu}=g_{\mu\nu}+A_\mu A_\nu$ | **spatial** gradient of φ | **the MOND / galaxy sector — where a₀ lives** |
| $\mathcal Q = A^\mu\nabla_\mu\phi$ | **temporal** part (≈ $\dot{\bar\phi}/N$) | **the cosmological / dust sector — a₀-free** |
| $\mathcal F(\mathcal Y,\mathcal Q)$ | the free function | contains both sectors |

---

## Where a₀ enters — and why scaling it is CMB-safe (now sourced)

**MOND limit (spatial, galaxies):** as $\nabla\phi\to0$,
$$\mathcal J \;\to\; \frac{2\lambda_s}{3(1+\lambda_s)\,a_0}\,\mathcal Y^{3/2},\qquad \mathcal J(\mathcal Y)\equiv\frac{\mathcal F(\mathcal Y,\mathcal Q_0)}{2-K_B}.$$
*(Coefficient RESOLVED 2026-08-14 against the arXiv LaTeX source (`arxiv.org/e-print/2007.00082`,
`newRMONDLett.tex`): the factor 3 IS present, and the limit is stated for
$\mathcal J = \mathcal F/(2-K_B)$, not bare $\mathcal F$. **a₀ is the coefficient of the
$\mathcal Y^{3/2}$ spatial term** — unambiguous either way.)*

**Cosmological dust (temporal, CMB):** the $\mathcal Q$-dependence,
$$\mathcal K(\mathcal Q) = -2\Lambda + \mathcal K_2(\mathcal Q-\mathcal Q_0)^2 + \dots,$$
a shift-symmetric k-essence with a minimum at $\mathcal Q_0\neq0$. **This is what makes the
scalar's energy density behave like dust (below) and fit the CMB — and it contains no a₀.**

> **The Bridge-1 result, sourced:** a₀ sits in $\mathcal F(\mathcal Y)$ (spatial); the CMB-fitting
> dust-mode sits in $\mathcal K(\mathcal Q)$ (temporal). They are *different arguments of the free
> function*. Promoting $a_0\to a_0(z)$ modifies the galaxy (𝒴) sector and leaves $\mathcal K(\mathcal Q)$
> — hence the dust mode and the CMB fit — **structurally untouched.** This upgrades
> `bridge1_aest_qsa_scoping.py`'s plausibility argument from "structural" to "in the action."

---

## The finishing result: a₀ is absent from LINEAR cosmology (order-counting)

CMB-safety is not just sector separation — it is an **order-counting theorem on the action**.

On FRW the scalar is purely temporal, $\bar\phi=\bar\phi(t)$, and $A^\mu$ is the unit timelike
frame. Since $\mathcal Y=q^{\mu\nu}\nabla_\mu\phi\nabla_\nu\phi$ with $q^{\mu\nu}=g^{\mu\nu}+A^\mu A^\nu$
projecting **orthogonal** to $A$:

- **background:** $\bar{\mathcal Y}=q̄^{\mu\nu}\nabla_\mu\bar\phi\,\nabla_\nu\bar\phi = 0$ (the
  spatial projection of a temporal gradient vanishes);
- **linear order:** $\delta\mathcal Y = 2\,q̄^{\mu\nu}\nabla_\mu\bar\phi\,\nabla_\nu\delta\phi = 0$
  (same projection kills the cross term). So $\mathcal Y = q̄^{\mu\nu}\nabla_\mu\delta\phi\,\nabla_\nu\delta\phi+\dots = \mathbf{O(\delta\phi^2)}$.

The a₀-dependent piece is the non-analytic MOND term $\mathcal J\supset\frac{2\lambda_s}{3(1+\lambda_s)a_0}\mathcal Y^{3/2}$ (i.e. $\mathcal F\supset(2-K_B)\,\mathcal J$; coefficient corrected 2026-08-14 to match the resolution above).
With $\mathcal Y=O(\delta\phi^2)$ this is $(\delta\phi^2)^{3/2}=\mathbf{O(\delta\phi^3)}$ — *third*
order. It contributes **nothing to the second-order action**, i.e. nothing to the **linear** EOMs.
The linear perturbations are governed instead by (i) the analytic kinetic term $-(2-K_B)\mathcal Y$
($O(\delta\phi^2)$, coefficient $(2-K_B)$ is **a₀-free**) and (ii) the temporal $\mathcal K(\mathcal Q)$
(dust + Λ, **a₀-free**).

> **Result (from the action):** a₀ appears in neither the FRW background ($\bar{\mathcal Y}=0$) nor
> the linear perturbations (the MOND term is $O(\delta\phi^3)$). So $a_0\to a_0(z)$ leaves the
> **linear CMB and P(k) exactly invariant.** The running enters only at nonlinear / quasi-static
> (galaxy) order — exactly where the high-z RAR data tests it.

This **establishes Bridge 1's CMB-safety analytically.** The Boltzmann run would *confirm* (the
linear $C_\ell$ are a₀-independent); the genuinely new physics of running a₀ is in **nonlinear
structure formation** — the z>2 RAR front.

**Caveat:** the $\mathcal Y^{3/2}$ non-analyticity at $\mathcal Y=0$ makes perturbation theory around
the cosmological background delicate (the quasi-static/screening matching needs care — the AeST
authors treat this). The leading order-counting (a₀ absent from the linear sector) is robust; a
careful second-order/nonlinear treatment is where running a₀ first bites.

## Background (FRW)

- scalar EOM integrates to $\;\dfrac{d\mathcal K}{d\mathcal Q} = \dfrac{I_0}{a^3}\;$ ($I_0$ = integration const);
- energy density $\;8\pi\tilde G\,\bar\rho = \mathcal Q\,\dfrac{d\mathcal K}{d\mathcal Q} - \mathcal K
  \;\Rightarrow\; \bar\rho = \bar\rho_0/a^3 + \dots\;$ — **dust** (∝ a⁻³), the CDM-mimic;
- $\;\bar{\mathcal Q} = \dot{\bar\phi}/N\;$, and $\;\mathcal Q = \mathcal Q_0 + I_0/a^3 + \dots\;$
- the $-2\Lambda$ in $\mathcal K$ supplies the cosmological constant.

So at the background level AeST = ΛCDM-like (baryons + this dust + Λ), exactly the scaffold's
`Background`. **a₀(z)=cH/Z is a derived diagnostic here, not an input to the background.**

---

## Linear perturbations (conformal Newtonian gauge)

**[SECTION COMPLETED 2026-08-14 from the arXiv LaTeX source itself** — `curl
arxiv.org/e-print/2007.00082` → `newRMONDLett.tex`, transcribed verbatim below. This discharges the
four load-bearing omissions identified by `nbody_2026/stage57_sz21_corrected_refile_2026.py`
PART C (the root cause of the stage-55 withdrawal): E's definition, the aether perturbation
ansatz, the δ-definition Eq (7) (historically mislabelled "Eq 9"), and Eq (12)'s elided source.**]

**The perturbation ansatz (Newtonian gauge, their §"Cosmological observables"):**
$$g_{00}=-(1+2\Psi),\quad g_{0i}=0,\quad g_{ij}=a^2(1-2\Phi)\gamma_{ij},\qquad
\phi=\bar\phi+\varphi,\qquad \hat A_\mu = \{-1-\Psi,\; \vec\nabla_i\alpha\},$$
so the aether carries ONE scalar perturbation α (omission #2, now closed).

**Mixing variables — all three, including E (omission #1, now closed):**
$$\chi \equiv \varphi + \dot{\bar\phi}\,\alpha,\qquad
\gamma \equiv \dot\varphi - \dot{\bar\phi}\,\Psi,\qquad
E \equiv \dot\alpha + \Psi.$$

**Eq (7) — the definition of δ (label `delta_field_relation`; omission #3, now closed) — and θ (Eq 8):**
*(numbering corrected 2026-08-14: under the source tex this is Eq (7), with θ (8), δ̇ (9), θ̇ (10),
Π (11), E-evolution (12).  Stages 55–57 called the δ-definition "Eq (9)" — a mislabel, now on
record; the equation content those stages used is this one.)*
$$\delta \equiv \frac{1+w}{\dot{\bar\phi}\,c_{ad}^2}\,\gamma
+ \frac{1}{8\pi\tilde G a^2\bar\rho}\,\nabla^2\big[K_B E + (2-K_B)\chi\big],
\qquad \theta \equiv \frac{\varphi}{\dot{\bar\phi}}.$$

With these, $\delta G^0{}_0$ and $\delta G^0{}_j$ take the GR form, and the pair obeys standard
fluid equations
$$\dot\delta = 3H(w\delta-\Pi) + (1+w)\Big(3\dot\Phi - \frac{k^2}{a^2}\theta\Big),\qquad
\dot\theta = 3c_{ad}^2 H\theta + \frac{\Pi}{1+w} + \Psi,$$

**with nonstandard pressure contrast — Eq (11) (label `Pi_delta_E_alpha`):**
$$\Pi = c_{ad}^2\,\delta - \frac{c_{ad}^2}{8\pi\tilde G a^2\bar\rho}\,\nabla^2\big[K_B E + (2-K_B)\chi\big].$$

**Eq (12) IN FULL — the E-evolution equation with the previously-elided source (omission #4, now
closed):**
$$K_B\big(\dot E + HE\big) = \frac{d\mathcal K}{d\mathcal Q}\,\chi
- (2-K_B)\left[\frac{\dot{\bar\phi}}{1+w}\,\Pi + \big(H+\dot{\bar\phi}\big)\chi
- 3c_{ad}^2 H\,\dot{\bar\phi}\,\alpha\right].$$

**The identity the old elision hid (stage-57 C2, now verifiable line-by-line from this page):**
Eq (7) and Eq (11) carry the SAME bracket $\nabla^2[K_B E + (2-K_B)\chi]$, so substituting (9)
into (11) cancels it and gives
$$\boxed{\;\Pi = \frac{(1+w)\,\gamma}{\dot{\bar\phi}}\;}$$
**exactly** — the bracket's Laplacian belongs to the definition of δ, NOT to the pressure. Any
quasi-static closure must attach it to δ. (This is the error class that produced the withdrawn
stage 55.)

**Background relations (verbatim from the same source):**
$$8\pi\tilde G\bar\rho = \mathcal Q\frac{d\mathcal K}{d\mathcal Q}-\mathcal K,\qquad
8\pi\tilde G\bar P = \mathcal K,\qquad
\frac{d\mathcal K}{d\mathcal Q}=\frac{I_0}{a^3},\qquad
8\pi\tilde G\bar\rho_0 = \mathcal Q_0 I_0,$$
$$w_0 = \frac{8\pi\tilde G\bar\rho_0}{4\mathcal Q_0^2\mathcal K_2},\qquad w = w_0/a^3+\dots,\qquad
c_{ad}^2 = \frac{d\mathcal K/d\mathcal Q}{\mathcal Q\, d^2\mathcal K/d\mathcal Q^2} = 2w_0/a^3+\dots$$

**Quasi-static sector constants:** $\mu = \sqrt{\tfrac{2\mathcal K_2}{2-K_B}}\,\mathcal Q_0$,
oscillation radius $r_C\sim(r_M\mu^{-2})^{1/3}$, requirement $\mu^{-1}\gtrsim1$ Mpc;
$\tilde G = (1-\tfrac{K_B}{2})\hat G_{qs}$; and in the quasi-static limit
$\mathcal Q = (1-\Psi)\mathcal Q_0$.

**The three published $\mathcal K(\mathcal Q)$ functions (verbatim; $Z=(\mathcal Q-\mathcal Q_0)/\mathcal Z_0$):**
$$\text{Cosh: } \mathcal K = 2\mathcal K_2\mathcal Z_0^2[\cosh Z - 1]\;(K''=2\mathcal K_2);\quad
\text{Exp: } \mathcal K = 2\mathcal K_2\mathcal Z_0^2[e^{Z^2}-1]\;(K''=4\mathcal K_2);$$
$$\text{Higgs-like: } \mathcal K = \frac{\mathcal K_2}{4\mathcal Q_0^2}(\mathcal Q^2-\mathcal Q_0^2)^2.$$
(The Exp function's $K''(\mathcal Q_0)=4\mathcal K_2$ — not $2\mathcal K_2$ — is the factor-2
convention caught by stage 58's corroboration table.)

The pressure perturbation depends on the vector perturbations through E and χ — SZ21's own text:
the system "is not equivalent to a dark fluid: the nonstandard pressure ... depends on the vector
field perturbations." **These equations are dominated by $d\mathcal K/d\mathcal Q$ (the 𝒬 sector);
a₀ enters only through the 𝒴-sector terms of $\mathcal F$** — SZ21 verbatim: a₀ "does not appear
in the linear cosmological regime but will play a role once nonlinear terms from
$\mathcal F(\mathcal Y,\mathcal Q)$ kick in."

---

## The θ-coupling (the one new ingredient) and the implementation spec

**Promotion:** replace the constant $a_0$ in the $\mathcal Y^{3/2}$ term by
$$a_0 \;\to\; a_0(\theta) = \frac{c\,\theta}{3Z},\qquad \theta \equiv \nabla_\mu A^\mu\;\;(=3H\ \text{on FRW}),\quad Z=2\sqrt{8\pi/3}.$$
$\theta$ is a *local* scalar built from the aether already in the action — so this is a minimal,
covariant modification, not a new field. On the background it gives $a_0=cH/Z$ (the premise);
in galaxies $\theta\approx3H_0$ recovers the standard value.

**To finish (in hi_class / a CLASS patch):**
1. add the unit-timelike vector $A_\mu$ + multiplier $\lambda$ (not in vanilla hi_class);
2. implement $\mathcal F(\mathcal Y,\mathcal Q)$ with the $\mathcal Y^{3/2}$ MOND term and the
   $\mathcal K(\mathcal Q)=-2\Lambda+\mathcal K_2(\mathcal Q-\mathcal Q_0)^2$ dust term;
3. make the $\mathcal Y^{3/2}$ coefficient carry $a_0(\theta)=c\theta/(3Z)$;
4. evolve Eqs. (11)–(12) + the scalar EOM + the CLASS photon/neutrino hierarchy;
5. **decisive check:** does the 3rd-peak height (the dust tracer) match Planck *with* the running
   $a_0$? Compare to the *constant*-$a_0$ AeST run — the difference is the whole question.

**Predicted outcome (from the structure):** small change, because the running lives in the
𝒴-sector and the peaks are set by the 𝒬-sector dust mode. If that holds quantitatively, Bridge 1
closes: one Lagrangian for galaxies (evolving MOND) + the CMB.

---

*Source:* arXiv:2007.00082 (Skordis–Złošnik 2021). Original transcription via ar5iv (2026-06-01);
**perturbation + background sections completed and coefficient-verified against the arXiv LaTeX
source itself on 2026-08-14** (referee-checked line-by-line against `newRMONDLett.tex`) — the old
"verify against the published PDF before coding" caveat is DISCHARGED for everything on this page.
*Wires into:* `bridge1_aest_boltzmann_scaffold.py` (Section 3 stubs now point here).
