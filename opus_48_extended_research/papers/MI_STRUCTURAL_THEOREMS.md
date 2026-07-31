# Structural Theorems for de Sitter–Unruh Modified Inertia: What the First-Moment Closure Forbids

**Carl P. Zimmerman**
Briar Creek Tech, Charlotte, NC, USA · carl@briarcreektech.com

**Version 2026-07-30 (v3)** · License CC-BY-4.0

> ### ⚠️ v3 CORRECTION NOTICE — THE KERNEL HAS CHANGED. READ FIRST.
>
> v2 stated every result below for $K_1(z)=(\sqrt{1+4z}-1)/(2\sqrt z)$, whose Newtonian approach is
> $1-K\sim1/(2\sqrt z)$ — the $\alpha=1$ class. **Later on the same day as v2's release, the framework
> adopted an $\alpha\ge2$ kernel**, $K_2(z)=\sqrt{z/(1+z)}$. The reason is quantitative and runs against
> the earlier choice: held to all accelerations, $\alpha=1$ forces a *constant* sunward anomaly $a_0/2$
> that is **1279× the Earth 2σ ephemeris bound** (Sereno & Jetzer 2006, Table 1, through their Eq. 9),
> and it drives the companion disformal lensing construction's own $B<1$ premise past **257×** across
> Mercury→Saturn — while buying **+0.0033 dex** on 175 SPARC galaxies, which is $0.10\,\sigma_{\rm int}$
> and unresolvable.
>
> **$a_0=cH_\Lambda/Z$ is unaffected.** Every premise the coefficient's derivation uses — Herglotz–
> Nevanlinna positivity, passivity $\sup K=1$, the unit sum rule $\int\mathrm d\mu/|t|=K(\infty)-K(0)=1$,
> the horizon floor — holds for $K_2$ as well, and $K_2$ keeps the deep-MOND $\sqrt z$ origin. **What is
> withdrawn is the word *exact*:** the relation $g_{\rm obs}^2=g_{\rm bar}^2+a_0g_{\rm bar}$ is an
> $\alpha=1$ identity and is no longer claimed.
>
> **ALL SEVEN RESULTS SURVIVE.** Three carry new numbers, one falsifier is qualified, and there is one
> new result. Everything is recomputed in `mi_structural_theorems_v3_numbers_2026.py`, which reproduces
> **both** published v2 values first (the Hessian $-11/25+23\sqrt5/125$ and the Prop-7 offset $-0.037$
> dex) as a machinery check, so every change below is attributable to the kernel and not to the author:
>
> | result | v2 ($\alpha=1$) | **v3 ($\alpha=2$)** | status |
> |---|---|---|---|
> | Thm 1 moment identity | $\langle\Box_u\rangle_u=+|a|^2$ | identical | kinematic — unchanged |
> | Thm 2 $\operatorname{Im}K\equiv0$ | cut $z\le-\tfrac14$ | cut $-1<z<0$ | survives; cut now **compact** |
> | Thm 3 Hessian det | $-0.02856$ | $\mathbf{-3\sqrt2/64=-0.06629}$ | survives, simpler |
> | Thm 4 FRW inert / non-analytic | $K\sim\sqrt z$ | identical | kinematic + shared origin |
> | Thm 5 dipole, $e\ll y$ | 4.2–22.3% | **5.4–15.4%** | survives, $1.10\times$ |
> | Thm 5 sign, $e\gg y$ | positive | **negative, $<0.2\%$** | **falsifier qualified** |
> | Prop 6 $h(x)$ | $2x/\sqrt{1+4x^2}$ | $\mathbf{x(x^2+2)/(1+x^2)^{3/2}}$ | deep limit **identical** |
> | Prop 7 offset | $-0.037$ dex | $-0.0369$ dex | unchanged |
> | **new** | — | **spectral measure, one region** | new result, §2.1 |
>
> v2's own correction notice (below) about Proposition 7's retracted forecast **still stands**.

> **v2 CORRECTION NOTICE — retained, still in force.** v1's Proposition 7 attached an observational forecast to
> its two propositions: "~1.2–1.9σ on 40–60 Local Group dwarfs, 3σ at $N\sim150$, both routes
> archival." **That forecast was wrong and is retracted here.** Running the test on the real
> McConnachie (2012) catalogue shows it is **systematics-limited, not sample-limited**: the per-object
> scatter is 0.38–0.48 dex rather than the assumed 0.15–0.20, and the dominant error — the stellar
> mass-to-light ratio — is **coherent** across the sample, so $\sqrt N$ does not reduce it.
> **Propositions 7.1 and 7.2 themselves are unchanged** (a theorem and a calculation); only the
> forecast built on them fails. §9 is rewritten accordingly. No other section is affected.

---

## Abstract

The modified-inertia action

$$S = \frac{c^4}{16\pi G}\int\!\sqrt{-g}\,R \;+\;\dots\;-\;\frac12\int\!\sqrt{-g}\,\rho_m\Big[s\,u^\mu K(\Box_u/a_0^2)u_\mu\Big],
\qquad K(z)=\sqrt{\frac{z}{1+z}},$$

with $\Box_u f = u^a\nabla_a(u^b\nabla_b f)$ and acceleration scale $a_0=\tfrac12 c\sqrt{G\rho_\Lambda}$,
is evaluated in practice through its **first-moment closure**, $K(\Box_u/a_0^2)\to K(|a|^2/a_0^2)=\mu(|a|/a_0)$.
We prove seven structural results about that closure. Five are prohibitions and two are predictions.
The kernel is $\alpha=2$; **v3 changed it from $\alpha=1$, and §0's notice states why and what moved.**

**(1)** The first-moment identity $u_\mu\Box_u u^\mu=-|a|^2$ holds **pointwise on every timelike
worldline**, following from $u\!\cdot\!u=-1$ alone — not merely on the circular and helical cases
previously verified. **(2)** The closure's argument is therefore $|a|^2\ge 0$, while $K$'s branch cut
requires $z\le-\tfrac14$; hence $\operatorname{Im}K\equiv 0$ **identically**, for the mean motion and
for every perturbation at every order. The MOND amplitude and any dissipative channel are therefore
**mutually exclusive**, and the sign postulate $s$ is demoted from a parameter awaiting data to a label
on a branch the working theory never evaluates. **(3)** The law $\mu(|a|/a_0)\,a=g_{\rm bar}$
is second order, whereas the Euler–Lagrange equation of any $L(x,\dot x,\ddot x)$ is fourth order, and
the degeneracy escape is closed because the acceleration Hessian of $\mu$ is non-singular.
**No local higher-derivative action reproduces the law**: the nonlocal form is required, not stylistic.
**(4)** Comoving FRW makes $u$ an exact zero mode of $\Box_u$, and $K(0^+)=0$, so the matter term
**vanishes identically on the cosmological background**; since $K\sim\sqrt z$ there, no perturbative
modified Friedmann equation exists. Modified inertia cannot alter the expansion history.
**(5)** The external-field effect is forced to be **quadrature with a vector cross term**, so the
customary linear ansatz $A=a_{\rm in}+a_{\rm ex}\theta$ is unavailable; the resulting prediction is a
**dipole** rotation-curve asymmetry, attractor-faster, and **independent of the $a_0$ footing**.
**(6)** The linear-response inertia is $h(x)=\mathrm{d}(x\mu)/\mathrm{d}x=x(x^2+2)/(1+x^2)^{3/2}$,
not $\mu$. **(7)** Dispersion-supported systems discriminate the residual closure freedom:
the ultralocal member places them **exactly** on the rotation relation, an orbit-averaged member offsets
them by $-0.0369$ dex, and on the real McConnachie (2012) catalogue the test proves **systematics-limited** rather than sample-limited (§9.1).

Every result is machine-verified by committed scripts that exit non-zero on any failed internal check.

---

## 1. Scope, and what is not claimed

This paper concerns the **internal structure** of one modified-inertia action. It does not claim to
derive the value of $a_0$, to solve the dark-matter problem, or to establish the framework against
alternatives. The author has publicly retracted earlier and broader claims, and nothing here depends on
them.

**Credit.** The interpolating kernel used throughout is $\mu(x)=x/\sqrt{1+x^2}$ — the **"standard"
MOND interpolating function of Milgrom (1983,** *ApJ* **270**, 365**)**. It is not original here, and
neither was v2's $\nu(y)=\sqrt{1+1/y}$, which is Milgrom (1999, *Phys. Lett. A* **253**, 273, Eq. 9)
and whose dS–Unruh derivation there also *fixes* the coefficient at $2cH_\Lambda$. The distinctive
content of this framework is the
**coefficient** $a_0=cH_\Lambda/Z$ with $Z=\sqrt{32\pi/3}$ (Milgrom's was $2cH_\Lambda$), and the
modified-inertia completion. The value of $\kappa=\tfrac12$ in $a_0=\kappa c\sqrt{G\rho_\Lambda}$ is
**not derived**; ghost-freedom, unitarity and holography have each been shown insufficient to force it.
This is a one-parameter effective theory.

**What five of these theorems do is subtract.** They remove a postulate, remove a channel, remove a
class of actions, and remove a cosmological sector from the theory's reach. That is the intended
contribution: a framework with fewer places to hide is more testable, and the prohibitions were
available to any referee.

---

## 2. The action, the closure, and the coefficient

The matter sector carries the modification. With signature $(-,+,+,+)$ and $u\!\cdot\!u=-1$,

$$S_{\rm matter} = -\frac12\int\!\sqrt{-g}\;\rho_m\Big[s\,u^\mu K(\Box_u/a_0^2)u_\mu\Big],\qquad
K(z)=\sqrt{\frac{z}{1+z}},\qquad s=-1\ \text{(postulated)} .$$

$K$ is Herglotz–Nevanlinna with a positive measure, $\|K\|\le1$, causal-retarded, with
$K(0^+)=0$, $K(\infty)=1$, and the identity $K(x^2)=\mu(x)$ where

$$\mu(x)=\frac{x}{\sqrt{1+x^2}},\qquad x=\frac{|a|}{a_0}.$$

### 2.1 The spectral measure (new in v3)

$K_2$'s branch cut is where $z/(1+z)<0$, i.e. $-1<z<0$. Setting $z=-s$ with $0<s<1$ gives
$K=i\sqrt{s/(1-s)}$, so Stieltjes inversion yields the measure in closed form,

$$\rho(s)=\frac1\pi\sqrt{\frac{s}{1-s}}\quad\text{on }0<s<1,\qquad
K_2(z)=1-\int_0^1\frac{\rho(s)\,\mathrm ds}{z+s} .$$

The subtracted form is forced: the bare resolvent vanishes as $z\to\infty$ while $K_2(\infty)=1$. The
substitution $s=\sin^2\theta$ removes the endpoint singularity and gives
$\rho\,\mathrm ds=(2/\pi)\sin^2\theta\,\mathrm d\theta$, whence

$$\int_0^1\frac{\rho(s)}{s}\,\mathrm ds=1,\qquad \int_0^1\rho(s)\,\mathrm ds=\tfrac12 .$$

The first is the **unit sum rule** $\int\mathrm d\mu/|t|=K(\infty)-K(0)$ that makes $a_0$ additively
unrenormalised; it is satisfied identically, which is why the coefficient survives the kernel change.
The representation reproduces the closed form to $8\times10^{-15}$ over eight decades in $z$.

**It is strictly simpler than v2's measure.** That one required *two* spectral regions
($\rho_A$ on $-\tfrac14<t<0$, $\rho_B$ on $t<-\tfrac14$) plus an additive constant $a=0.65411$, on
*unbounded* support with *divergent* total mass. Here: one region, compact support $[0,1]$, finite mass
$\tfrac12$, no additive constant. **And the divergence was the problem** — an unbounded measure is
exactly what produces a $1/\sqrt z$ rather than $1/z$ approach to the passivity bound, i.e. the
$\alpha=1$ tail. Removing it removes the planetary anomaly and the exact law together.

**The coefficient.** Since $H_\Lambda=\sqrt{8\pi G\rho_\Lambda/3}$ and $Z=\sqrt{32\pi/3}$,

$$\frac{cH_\Lambda}{Z}=c\sqrt{\frac{8\pi G\rho_\Lambda}{3}}\cdot\sqrt{\frac{3}{32\pi}}
=c\sqrt{\frac{G\rho_\Lambda}{4}}=\tfrac12\,c\sqrt{G\rho_\Lambda},$$

so every $\pi$, the $32$ and the $3$ cancel. Numerically $a_0=9.36\times10^{-11}\,\mathrm{m\,s^{-2}}$
on the pure-$\Lambda$ footing, $1.13\times10^{-10}$ on the $\rho_{\rm total}$ footing. Both are carried
through every dimensional statement below.

---

## 3. Theorem 1 — the first moment is worldline-general

> **Theorem 1.** For every timelike worldline, in curved spacetime, with no assumption on the orbit,
> $$u_\mu\Box_u u^\mu=-|a|^2 \qquad\Longrightarrow\qquad \langle\Box_u\rangle_u\equiv\frac{u\!\cdot\!\Box_u u}{u\!\cdot\!u}=+|a|^2 .$$

*Proof.* $\Box_u u^\mu=\dot a^\mu$ on a worldline. Differentiate the normalisation twice:
$$\frac{\mathrm{d}}{\mathrm{d}\tau}(u\!\cdot\!u)=2\,u\!\cdot\!a=0\ \Rightarrow\ u\!\cdot\!a=0,$$
$$\frac{\mathrm{d}^2}{\mathrm{d}\tau^2}(u\!\cdot\!u)=2\big(a\!\cdot\!a+u\!\cdot\!\dot a\big)=0
\ \Rightarrow\ u\!\cdot\!\dot a=-a\!\cdot\!a .$$
Dividing by $u\!\cdot\!u=-1$ flips the sign, giving $+|a|^2$. $\square$

Both differentiation steps are verified symbolically for a general worldline with four free functions of
proper time. The positivity of the moment — despite the operator's spectrum lying at $-\omega^2$ — comes
from the **Lorentzian normalisation** and nothing else.

**What is new.** The identity was previously checked on circular and exact-helical worldlines. It is in
fact an algebraic consequence of $u\!\cdot\!u=-1$, hence exact for eccentric, plunging, and perturbed
trajectories alike. Everything below uses this generality.

---

## 4. Theorem 2 — non-negativity, and the mutual-exclusivity of MOND and dissipation

> **Theorem 2.** Under the first-moment closure, $\operatorname{Im}K\equiv0$ identically — for the mean
> motion and for every perturbation, at every order in perturbation amplitude.

*Proof.* $a^\mu$ is spacelike ($u\!\cdot\!a=0$ with $u$ timelike), so $a\!\cdot\!a>0$ and by Theorem 1
the closure feeds $K$ the argument
$$z=\frac{|a|^2}{a_0^2}\;\ge\;0 .$$
$K$ is real-analytic on $z>0$ and acquires an imaginary part only on its branch cut, which for the
$\alpha=2$ kernel is the **compact** interval $-1<z<0$ (v2's $\alpha=1$ kernel had $z\le-\tfrac14$). The
two regions are disjoint either way. $\square$

Verified additionally on explicitly perturbed epicyclic worldlines scanned over amplitude
$\epsilon\in[0.01,0.9]$ and frequency ratio $\kappa/\Omega\in[0.2,3]$: the minimum of $|a|^2$ over every
orbit is non-negative, and the argument never enters the cut. Verified numerically for $K_2$:
$\operatorname{Im}K_2>0$ throughout $-1<z<0$ and identically zero for $z>0$.

> **Corollary 2.1 (mutual exclusivity).** The MOND amplitude and any dissipative channel cannot coexist.
>
> - *First-moment closure*: argument $\ge0$, $K$ real, the radial-acceleration relation is reproduced
>   (0.1116 dex on SPARC at $\alpha=2$; 0.1083 at the retired $\alpha=1$), and dissipation is
>   **identically zero**.
> - *Literal spectral closure*: argument $-(\omega c/a_0)^2$ lies on the cut, $K$ is unimodular and
>   complex, dissipation occurs at exactly $a_0/2c$ — but the relation **fails outright**
>   ($K=0.99999997+2.5\times10^{-4}i$ against the required $K(1)=1/\sqrt2=0.7071$ at $a=a_0$; the
>   $\alpha=1$ kernel required $0.618$).
>
> No closure delivers both.

> **Corollary 2.2 (the sign is demoted).** The dissipative rate carries the postulated sign $s$. Since
> that rate is identically zero in the closure that reproduces the relation, $s$ has **no observable
> consequence**: it is not a parameter awaiting better data but a label on a branch the working theory
> never evaluates. Any future claim to have measured it must first exhibit a closure that samples the cut
> *and* reproduces the relation — which Theorem 2 forbids within the first-moment family.

**Independent confirmation from data.** The literal closure's universal drift $a_0/2c$ = $4.93\times10^{-12}\,\mathrm{yr^{-1}}$
($\tau=203$ Gyr canonical, 168 Gyr alternative — only a $1.21\times$ footing spread) is excluded at
**8.5$\sigma$** by the orbital-period agreement of PSR J0737−3039 (Peters back-reaction validated against
the measured $\dot P_b$ of both J0737−3039 and B1913+16 to 0.03% and 0.8% before use). The Hulse–Taylor
system alone reaches only 1.1$\sigma$.

**Scope.** Theorem 2 is proved for the first-moment closure *family*. Within that family the
off-circular time-weighting remains free, but every member's argument is a weighted average of
$|a(\tau)|^2$ and therefore non-negative, so the conclusion is family-wide.

---

## 5. Theorem 3 — the nonlocal action is necessary

> **Theorem 3.** $\mu(|a|/a_0)\,a=g_{\rm bar}$ is not the Euler–Lagrange equation of any
> non-degenerate local Lagrangian $L(x,\dot x,\ddot x)$.

*Proof.* The higher-derivative Euler–Lagrange equation
$$\frac{\partial L}{\partial x}-\frac{\mathrm{d}}{\mathrm{d}t}\frac{\partial L}{\partial\dot x}
+\frac{\mathrm{d}^2}{\mathrm{d}t^2}\frac{\partial L}{\partial\ddot x}=0$$
contains $x^{(4)}$ in general — verified symbolically, highest derivative order 4. The framework's law
contains no derivative above $\ddot x$; it is an implicit **second**-order relation. The only escape is
degeneracy, $\partial^2L/\partial\ddot x^2=0$, i.e. $L$ at most linear in $\ddot x$. But the framework's
dependence enters through $|a|^2=a\!\cdot\!a$ inside the nonlinear $\mu$, and the Hessian with
respect to acceleration components is non-singular:
$$\det\Big[\partial^2\mu/\partial a_i\partial a_j\Big]_{|a|=a_0}=-\frac{3\sqrt2}{64}=-0.06629\neq0 .$$

For $f(|a|)$ in three dimensions the Hessian has eigenvalues $f''$ (once, along $\hat a$) and $f'/|a|$
(twice, transverse), so $\det=f''(f'/|a|)^2$. **v2's published value for the $\alpha=1$ kernel was
$-11/25+23\sqrt5/125=-0.02856$; the v3 script reproduces it exactly before applying the same method to
$K_2$**, so the change is the kernel's and not the method's. The conclusion is unaffected: the Hessian
is non-singular, so the degeneracy escape stays closed.
$\square$

**This is a positive result for the published action.** The nonlocal form is not an aesthetic
preference or a device for evading Ostrogradsky — it is *required*, because no local higher-derivative
theory can produce the framework's own phenomenological law.

**The gap it exposes.** Theorem 1 supplies a **moment identity**: given a worldline, the operator's
u-contracted first moment is $|a|^2$. An Euler–Lagrange equation *selects* the worldline. These are
different objects, and the corpus's structural guarantees (zero frame degrees of freedom via a
no-wave-cone symbol argument, the causal-retarded Herglotz definition, the one-loop sum rule) are
theorems about the **nonlocal** action, while every quantitative success is computed with the **local**
closure. That the two coincide is not established. The gap is invisible where the framework has been
tested: on a circle $|a|$ is constant, so closure members agree to $1.8\times10^{-16}$, and rotation
curves and the baryonic Tully–Fisher relation are circular by construction. (v2 also listed "the
$a_0$-line" here; that identity was an $\alpha=1$ artefact and is withdrawn in v3.) Off
circles the ambiguity grows — 0.07% at $\epsilon=0.05$, 1.0% at 0.2, 6.5% at 0.5 — and the two places
the framework has been pushed off circles are precisely where closure ambiguities appeared.

---

## 6. Theorem 4 — the cosmological background is inert, and non-analytic

> **Theorem 4.** On a comoving FRW background the modified-inertia term vanishes identically, and no
> perturbative expansion of it exists.

*Proof.* For $\mathrm{d}s^2=-\mathrm{d}t^2+a(t)^2\mathrm{d}\mathbf{x}^2$ and comoving
$u^\mu=(1,0,0,0)$, all $\Gamma^\mu_{\ 00}$ vanish, so
$$a^\mu=u^\nu\big(\partial_\nu u^\mu+\Gamma^\mu_{\ \nu\lambda}u^\lambda\big)=0$$
identically, for arbitrary $a(t)$ — comoving matter is geodesic. Hence $|a|^2=0$ and
$\Box_u u^\mu=u^a\nabla_a(a^\mu)=0$: $u$ is an **exact zero mode** of the operator, so by spectral
calculus $K(\Box_u/a_0^2)u_\mu=K(0)u_\mu$. Since $K(0^+)=0$,
$$-\tfrac12\rho_m\,s\,u^\mu K(\Box_u/a_0^2)u_\mu=-\tfrac12\rho_m\,s\,K(0)(u\!\cdot\!u)=0 .$$
Moreover the series at the origin is $K(z)=\sqrt z\,(1-z)+\mathcal{O}(z^{5/2})$ with $K'(0^+)=\infty$:
$K$ has a **square-root branch point exactly where the cosmological background sits**, so no Taylor
expansion in perturbations about it exists. $\square$

**Consequences.** Modified inertia contributes no background modification and no luminosity-distance
tilt — structurally zero, not small. The framework's expansion history therefore comes from its field
content, not from the inertia modification. And the coincidence $cH_0/a_0=7.00$ is a coincidence of
**scales**, not evidence of a **coupling**: nothing in the action makes the expansion rate an argument
of $K$.

The non-analyticity is an obstacle for the perturbation calculation the framework still requires: a
naive "expand $K$ to first order in perturbations" step is unavailable because $K'(0^+)$ diverges.

---

## 7. Theorem 5 — the external-field effect is quadrature, and predicts a dipole

> **Theorem 5.** Theorem 1 forces the external field into the closure through
> $$|a_{\rm in}+a_{\rm ex}|^2=a_{\rm in}^2+a_{\rm ex}^2+2\,a_{\rm in}\!\cdot\!a_{\rm ex},$$
> a **quadrature** sum with a **vector** cross term. No scalar phase function multiplying $a_{\rm ex}$
> can appear.

The customary linear ansatz $A=a_{\rm in}+a_{\rm ex}\theta(\omega_{\rm ex}/\omega_{\rm in})$ is
therefore unavailable in this framework, together with everything derived from it.

**The correct construction.** The equation of motion applies to the total force and total acceleration,
$$\mu\!\left(\frac{|a_{\rm tot}|}{a_0}\right)a_{\rm tot}=g_{\rm bar,in}+g_{\rm ex},$$
the host's centre of mass obeys the same law under $g_{\rm ex}$ alone, and the observable is the
difference $a_{\rm in,obs}=a_{\rm tot}-a_{\rm ex}$, because the host frame accelerates. (Omitting the
host's own acceleration double-counts the external field and inflates the effect several-fold; the
isolated limit of the construction above reproduces the framework's relation to machine precision.)

> **Corollary 5.1 (the dipole).** Around a circular orbit $a_{\rm in}$ rotates while $a_{\rm ex}$ is
> fixed, so the cross term modulates the inertia with azimuth. On the side facing the attractor the
> fields partially cancel, $|a_{\rm tot}|$ falls, $\mu$ falls, and the boost rises: the **near
> side rotates faster**. The prediction is a **dipole**, not a quadrupole, and it is
> **independent of the $a_0$ footing**, because the governing equation is written entirely in units of
> $a_0$ and the amplitude depends only on $e=g_{\rm ex}/a_0$ and $y=g_{\rm bar}/a_0$.

| regime | dipole $(v_{\rm near}-v_{\rm far})/\bar v$, **v3 ($\alpha=2$)** | v2 ($\alpha=1$) |
|---|---|---|
| $e\ll y$ (inner disk, weak external field) | **5.4% – 15.4%** | 4.2% – 22.3% |
| $e\sim y$ (**MOND saddle — treatment invalid**) | — | 4.2% – 41.1% |
| $e\gg y$ (strong external field) | **$-0.15\%$ – $-0.05\%$ (sign flips)** | 0.1% – 1.2% |

The $e\ll y$ amplitude is $1.10\times$ v2's on matched cases, so the comparison against modified
gravity below is unchanged in character.

The $e\sim y$ peak is the known MOND saddle, where $g_{\rm tot}\to0$ on the near side and the
interpolation sits at its singular point. That is real physics but a point-particle balance is not valid
there; a proper field solve is required. The $e\gg y$ limit correctly **erases** the dipole, everything
being Newtonianised — a check on the construction.

**A prior claim is retracted.** It has been stated in this corpus that pure modified inertia predicts
*exactly zero* directional asymmetry. That is **wrong**, and its origin is now clear: a scalar $\theta$
multiplying $a_{\rm ex}$ carries no orientation, so the asymmetry vanishes identically under the
borrowed ansatz. Quadrature has a vector cross term, so orientation survives. Away from the saddle the
framework predicts 5.4%–15.4% at $\alpha=2$ (4.2%–33.6% at the retired $\alpha=1$), *larger* than the
1–4% of aligned-rotation-curve asymmetry expected in
AQUAL-type modified gravity. The observable therefore changes character: from blind to modified inertia,
to **favourable** to it, as an amplitude comparison.

**Falsifier, with a v3 qualification.** A measured rotation-curve dipole of the **opposite** sign (far
side faster) above $\sim1\%$ falsifies the construction. **v2 claimed the sign "is forced by the cross
term and cannot be tuned"; under the $\alpha=2$ kernel that must be narrowed.** In the $e\gg y$ corner
the v3 dipole is *negative* — $-0.15\%$ to $-0.05\%$ — which v2's kernel did not do. The falsifier is
unaffected in practice, because that corner sits an order of magnitude below the $1\%$ threshold and the
$e\gg y$ limit is precisely where everything is Newtonianised anyway. But the sign is now forced only
for $e\lesssim y$, which is where the amplitude is observable. Stated rather than buried.

---

## 8. Proposition 6 — the linear-response inertia

For $F=m\,a\,\mu(a/a_0)$, the response to a small additional force is governed by the
derivative, not the ratio:

$$h(x)\equiv\frac{\mathrm{d}}{\mathrm{d}x}\big[x\,\mu(x)\big]=\frac{x\,(x^2+2)}{(1+x^2)^{3/2}} ,$$

so the amplification of a perturbing response is $1/h(x)$, **not** $1/\mu(x)$. At $x=1$ these are
$1/h=4/(3\sqrt2)=0.9428$ and $1/\mu=\sqrt2=1.4142$ (v2's $\alpha=1$ kernel gave 1.118 and 1.618). Note
the qualitative change: at $x=1$ the $\alpha=2$ response is **suppressed** ($1/h<1$), not amplified.

**The deep limit is identical in both kernels**, $1/h\to1/(2x)$ against $1/\mu\to1/x$ — a factor 2. That
matters beyond this paper: every deep-regime use of Prop 6 (the diffuse-baryon growth chain, the
Lyman-$\alpha$ forest response) is therefore **unaffected** by the kernel change. Conflating $1/h$ with
$1/\mu$ overstates perturbative responses; so does evaluating $h$ at the *Newtonian* rather than the
*observed* acceleration, which is a separate and larger error corrected elsewhere in this corpus.

---

## 9. Proposition 7 — dispersion-supported systems discriminate the residual closure freedom

The off-circular time-weighting of $|a(\tau)|^2$ is free within the first-moment family. Two members:

- **Ultralocal:** $x_A(\tau)=|a(\tau)|/a_0$, applied pointwise.
- **Orbit-averaged:** $x_B=\sqrt{\langle|a|^2\rangle_{\rm orbit}}/a_0$, one number per orbit.

On a circle $|a|$ is constant and they coincide, which is why rotation curves cannot separate them.
Dispersion-supported systems can.

> **Proposition 7.1.** Under the ultralocal member, spherical dispersion-supported systems lie
> **exactly** on the rotation relation, for any orbit shape, because force balance is pointwise
> algebraic. Verified to $1.6\times10^{-15}$ across four decades in $g_{\rm bar}$, both footings.

> **Proposition 7.2.** Under the orbit-averaged member they are offset **below** it. The sign follows
> before computation: $x_B$ is constant along an orbit while $x_A$ varies and is smallest at apocentre,
> where stars spend most of their time; so $\mu(x_A)<\mu(x_B)$, and since
> $\mu(x)a=g_{\rm bar}$ the orbit-averaged closure over-assigns $\mu$ and under-predicts the
> acceleration.

Orbits integrated in the deep-regime logarithmic potential give, by apocentre-to-pericentre ratio $k$:
$-0.015$ dex ($k=2.2$), $-0.034$ ($k=3.7$), $-0.062$ ($k=8.3$), $-0.088$ ($k=20.5$); representative mean
over $k\sim2$–4 is $\mathbf{-0.0369}$ **dex** ($-0.037$ dex under v2's $\alpha=1$ kernel — the offset
is **kernel-insensitive**, and the v3 script reproduces v2's value by v2's own method before swapping).

**This does not yet fix the weighting** — $-0.037$ dex hides inside a 0.15 dex detectability tolerance
and below the framework's own 0.112 dex relation scatter, so the whole family survives.

### 9.1 Confrontation with the real catalogue (**new in v2**)

The test was run on **McConnachie (2012)**, AJ **144**, 4 (VizieR J/AJ/144/4/catalog): 46 of 102 rows
carry a stellar velocity dispersion, a half-light radius and an absolute $V$ magnitude. Using the
Wolf et al. (2010) estimator with $r_{1/2}=\tfrac43R_e$, $g_{\rm obs}=3\sigma^2/r_{1/2}$ and
$g_{\rm bar}=G(\Upsilon_VL_V/2)/r_{1/2}^2$, residuals taken against this framework's own $\nu$:

| quantity | v1 assumption | **real catalogue** |
|---|---|---|
| per-object scatter | 0.15–0.20 dex | **0.38–0.48 dex** |
| dominant error | random per object | **coherent** (stellar $\Upsilon_V$) |
| mean residual, $N=29$ after pre-stated cuts | — | $+0.2945\pm0.0710$ dex (random only) |

**The forecast fails on both counts.** The scatter is 2–3× larger than assumed, and — decisively — the
dominant uncertainty is not random. $\Upsilon_V$ is common to the whole sample, so it displaces every
dwarf identically and $\sqrt N$ leaves it untouched. Varying $\Upsilon_V$ over 1–4 moves the mean
residual from $+0.454$ to $+0.132$: a span of **0.322 dex, 8.7× the 0.037 dex signal**. Matching the
signal would require $\Upsilon_V$ known to 0.074 dex ($19\%$), against a literature spread of
50–100%.

Consequently **"$N\sim150$ for 3σ" and "both routes are archival" are withdrawn.** The measurement is
systematics-limited, and more dwarfs do not help.

### 9.2 The route that survives

A coherent $\Upsilon$ error and a closure offset are degenerate only if they share a $g_{\rm bar}$
dependence. On the real sample they do not: $\partial(\text{residual})/\partial\log\Upsilon$ has a
slope of $-0.067$ per dex against $\log_{10}(g_{\rm bar}/a_0)$, while the closure offset is
approximately flat in the deep regime — over an available **5.28 dex** of dynamic range. So the two are
**partially separable in principle.**

Realising that requires the closure offset computed **across** $g_{\rm bar}$, whereas §9 above
evaluates a single deep-regime orbit family. That is the concrete next step and it is not done here.
The alternative is a sample with independently calibrated stellar masses.

*Scope.* Planar orbits in an idealised logarithmic potential; three representative orbits rather than a
self-consistent distribution function. Sign and order are robust; the precise dex value should be read
as order-of-magnitude, and a proper isotropic and anisotropic distribution function is the next step.

---

## 10. What this changes

| item | before | after |
|---|---|---|
| first-moment identity | verified on circles/helices | **worldline-general** (Thm 1) |
| dissipative channel | open, sign postulated | **identically zero**; sign demoted (Thm 2) |
| choice of nonlocal action | a modelling preference | **required** (Thm 3) |
| cosmological background | "unbuilt" | **structurally inert**, and non-analytic (Thm 4) |
| external-field effect | Milgrom's postulated $\theta$ | **derived quadrature**; footing-free dipole (Thm 5) |
| perturbative response | $1/\mu$ | $1/h$, differing by up to $2\times$ (Prop 6) |
| off-circular weighting | free $O(1)$ choice | **predictions sharpened** (Props 7.1, 7.2); the test is **systematics-limited**, needing $\Upsilon_V$ to 19% or the $g_{\rm bar}$-resolved offset (§9.1–9.2, **v2**) |

Two remain untouched and postulated: the **value** of $\kappa=\tfrac12$, and the coefficient $Z$.

---

## 11. Reproducibility

Every number is produced by a committed script that exits non-zero if any internal check fails. No
verdict is hard-coded.

| script | results |
|---|---|
| `mi_dcac_split_settled_2026.py` | Thms 1, 2; Cors 2.1, 2.2 |
| `mi_sign_from_perturbation_drift_2026.py` | the 8.5$\sigma$ pulsar exclusion; the universal rate |
| `mi_closure_vs_action_gap_2026.py` | Thm 3 and the moment-vs-EL gap |
| `mi_channelA_friedmann_2026.py` | Thm 4 |
| `mi_efe_derived_general_2026.py` | Thm 5, Cor 5.1 |
| `mi_growth_amplification_founded_2026.py` | Prop 6 |
| `mi_closure_fixed_by_rar_universality_2026.py` | Props 7.1, 7.2 |
| `mi_dsph_closure_test_real_data_2026.py` | §9.1–9.2, the real-catalogue confrontation (**v2**) |
| `mi_kappa_spectral_reduction_2026.py` | the $\kappa$ reduction of §2 |
| **`mi_structural_theorems_v3_numbers_2026.py`** | **every v3 number, with both published v2 values reproduced first as a machinery check (14 checks)** |
| `mi_disformal_tail_freedom_2026.py` | that $a_0$'s derivation does not require $\alpha=1$; the disformal $B<1$ cost |
| `mi_alpha2_migration_2026.py` | the $\alpha\ge2$ switch, its triage, and the $\alpha=2$ spectral measure |

---

## References

- M. Milgrom, *Astrophys. J.* **270**, 365 (1983) — the "standard" interpolating function
  $\mu(x)=x/\sqrt{1+x^2}$ used from v3 onward.
- M. Milgrom, *Phys. Lett. A* **253**, 273 (1999) — the $\nu(y)=\sqrt{1+1/y}$ kernel used in v1–v2, and
  its dS–Unruh derivation, which also fixes the coefficient at $2cH_\Lambda$.
- M. Sereno & Ph. Jetzer, *Mon. Not. R. Astron. Soc.* **371**, 626 (2006) — solar-system limits on
  $\alpha$; the Earth/Mars bound that motivates v3's kernel change.
- M. Milgrom, arXiv:2208.07073 — the external-field effect and the $\theta$ ansatz.
- M. Kramer *et al.*, *Phys. Rev. X* **11**, 041050 (2021) — PSR J0737−3039 timing.
- J. Weisberg & Y. Huang, *Astrophys. J.* **829**, 55 (2016) — PSR B1913+16 timing.
- P. C. Peters, *Phys. Rev.* **136**, B1224 (1964) — orbital back-reaction.
- Framework antecedents: Zenodo 10.5281/zenodo.21264727 (action v4),
  10.5281/zenodo.21284144 (one-loop edge), 10.5281/zenodo.21702746 (wide-binary gate law).
