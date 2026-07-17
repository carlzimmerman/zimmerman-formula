# A Passivity Obstruction: Why a Derived $a_0 = cH_\Lambda/Z$ and Single-Metric Weak-Lensing Cannot Coexist in de Sitter–Unruh Modified Inertia

**Carl Zimmerman**
Briar Creek Tech · carl@briarcreektech.com

---

## Abstract

The de Sitter–Unruh modified-inertia (MI) program reproduces galaxy dynamics through a passive vacuum-response kernel $K(\Box_u/a_0^2)$ whose bounded, causal, positive-measure (Herglotz–Nevanlinna) structure ties the MOND acceleration scale to the cosmological horizon, $a_0 = cH_\Lambda/Z$ with $Z=\sqrt{32\pi/3}=5.789$. That structural tie is the program's single most distinctive claim. **What the passive kernel fixes is the *scale* of $a_0$; its numerical value and the sign $s=-1$ of the coupling remain postulates — a one-parameter effective-field-theory reframing, not a first-principles value.** The interpolating $\nu$-kernel law itself is Milgrom's (1999); the framework's distinctive content is the $cH_\Lambda/Z$ coefficient (his was $2cH_\Lambda$) and the covariant MI completion built on the passive frame. Here we ask whether the *same* field theory can also reproduce the weak-lensing MOND relation — the phantom mass $(\nu-1)\rho$ whose gravitational signature makes the observed lensing radial-acceleration relation coincide with the dynamical one, an equality that excludes single-metric pure MI at the $\sim27\sigma$ level (Brouwer et al. 2021, conservative rail, both footings). Conditional on the kernel-passivity premise, it cannot, and we identify the obstruction exactly. Writing $D$ (a$_0$ enters *solely* as the horizon-floored argument of the passive kernel), $S$ (single-metric, $c_\gamma=c_{\rm GW}$), $G$ (ghost-free), $L$ (the theory reproduces $g_{\rm lens}=\nu g_{\rm bar}\to\sqrt{a_0 g_{\rm bar}}$, null geodesics feeling the phantom), the central implication is **$D\wedge S \Rightarrow \lnot L$**. Equivalently $\{D,S,L\}$ is the *unique minimal unsatisfiable subset* of $\{D,S,G,L\}$: each proper subset is realized — $\{D,S\}$ is pure MI, $\{S,L\}$ is the Deffayet–Esposito-Farèse–Woodard / AeST class with $a_0$ a free coupling, and $\{D,L\}$ is a disformal two-cone construction that keeps $a_0$ derived but is excluded observationally by GW170817 (violating $S$). Ghost-freedom $G$ enters no step. The mechanism is a *passivity/amplification dichotomy*: the kernel derives $a_0$'s scale only because it is passive ($\sup K = 1$), and a passive kernel can only *suppress* the source to $\rho/\nu$, whereas MOND-lensing demands *enhancement* to $\nu\rho$, strictly outside the passive cone. We are explicit that the obstruction is conditional on that passivity premise — but the premise is precisely what derives $a_0$, so within the passive class the derivation and $\lnot L$ are consequences of one hypothesis; whether any *non-passive* (pumped) kernel could derive $a_0$ is a separate open question that the banked sign walls shut pump-free. All $a_0$-valued numbers are reported on both footings ($9.36\times10^{-11}\,{\rm m\,s^{-2}}$ canonical and $1.13\times10^{-10}$ alternate); the verdict is footing-independent. This is a conditional obstruction, not a closure of the program.

---

## 1. Introduction

### 1.1 The framework

Modified inertia (MI) treats MOND phenomenology not as a modification of the gravitational field sourced by matter, but as a modification of the inertial response of matter to a field. In the de Sitter–Unruh realization, a passive cosmic rest frame $u^\mu$ — a unit-timelike vector carrying **zero** propagating degrees of freedom, fixed by a Lagrange constraint $(u\cdot u+1)=0$ — mediates a vacuum response whose kernel acts on the frame d'Alembertian $\Box_u$. The worldline equation of motion that emerges is

$$
g_{\rm obs} = \nu(y)\,g_{\rm bar}, \qquad \nu(y)=\sqrt{1+\tfrac{1}{y}}, \qquad y \equiv \frac{g_{\rm bar}}{a_0},
$$

reducing to the deep-MOND law $g_{\rm obs}\to\sqrt{a_0\,g_{\rm bar}}$ as $y\to 0$ and to Newton as $y\to\infty$. This fits the SPARC rotation-curve sample at $0.108$ dex scatter ($\Upsilon=0.70$), competitive with regularized MOND.

The distinguishing structural claim is the identity of the acceleration scale with a horizon quantity,

$$
a_0 = \frac{cH_\Lambda}{Z}, \qquad Z=\sqrt{\tfrac{32\pi}{3}}=5.789 .
$$

Throughout, *footing* denotes the choice of cosmological input to this expression: the **canonical** pure-$\Lambda$ footing ($\rho_{\rm DE}/cH_\Lambda$) gives $a_0 = 9.36\times10^{-11}\,{\rm m\,s^{-2}}$, and the **alternate** footing ($\rho_{\rm total}/cH_0$) gives $1.13\times10^{-10}$. Both are carried at every $a_0$-valued number below.

### 1.2 The kernel and its passivity premise

The tie of $a_0$'s scale to the horizon arises because the vacuum-response kernel is *passive*: it is a bounded, causal, positive-measure response admitting a Herglotz–Nevanlinna spectral representation, normalized so that $\|K\|\le 1$ with a sum rule $\int d\mu/|t| = 1$ (banked MI action, DOI [10.5281/zenodo.21264727](https://doi.org/10.5281/zenodo.21264727); v11 [21284144](https://doi.org/10.5281/zenodo.21284144)). Passivity — a positive spectral measure with unit total weight — is what floors the response amplitude at the horizon scale $cH_\Lambda$; it is the source of the scale-tie. We take this passivity as the **single premise** of the present result and are explicit (Section 7) that the obstruction is conditional on it.

The real-space object that enters the static weak-field problem is the on-shell dressing. In the quasistatic first-moment reduction $K(\Box_u/a_0^2)\to K(X)$ with $X=|a|^2/a_0^2$ and $a^\mu=u^b\nabla_b u^\mu$, the interpolating kernel is

$$
K(X) = \frac{\sqrt{1+4X}-1}{2\sqrt X}, \qquad \nu = 1/K .
$$

This $K(X)$ is a **bounded, increasing (Bernstein-type) function**: $K(0^+)=0$ at the deep-MOND end and $\sup_{X\ge0}K(X)=1$ saturated as $X\to\infty$ (Newton), with $\nu=1/K$ running from $\infty$ (deep-MOND) down to $1$ (Newton). (It is *not* completely monotone — completely-monotone functions decrease; here $K$ increases and $K'$ is completely monotone, the Bernstein/Stieltjes dual. The banked Herglotz–Nevanlinna, $\|K\|\le1$ and sum-rule properties attach to the *frequency-domain response kernel* $K(\Box_u)$; the static $K(X)$ is the corresponding real-space dressing.) The single fact the obstruction actually uses is the uniform bound

$$
\boxed{\ \sup_{X\ge0} K(X) = 1\ }\qquad(\text{Newtonian saturation; } K\to0\text{ deep-MOND}),
$$

i.e. the passive kernel can only ever *suppress* a source to $\rho K \le \rho$.

### 1.3 Honest scope of the claim

We are precise about what is and is not derived. What the framework establishes is the **structural tie of the scale of $a_0$** to the passive kernel and the de Sitter horizon. The **numerical value** of $a_0$ and the **sign** $s=-1$ of the coupling remain **postulates** — the program is a one-parameter effective-field-theory *reframing*, not a first-principles computation. Moreover, the $\nu$-kernel law itself is not original: it is Milgrom (1999, *Phys. Lett. A* **253**, 273; astro-ph/9805346, Eq. 9), whose modified-inertia formulation uses an identical interpolating kernel (his coefficient was $2cH_\Lambda$). The framework's distinctive content is precisely (i) the $cH_\Lambda/Z$ coefficient and (ii) the covariant MI completion built on the passive frame. We credit Milgrom's original MOND (1983) and his 1999 modified-inertia formulation explicitly, and we do not re-assert any earlier, retracted claims of a derived value of $a_0$, a Standard-Model bridge, or a final all-physics theory. The defensible position is the $a_0$ reframing, and nothing more.

### 1.4 The lensing question

Galaxy dynamics is a worldline phenomenon; weak lensing is not. Lensing probes the deflection of null geodesics, fixed by the gravitating stress tensor $T_{\mu\nu}$ that the field equations actually see. A prior calculation (the single-metric lensing decider; SOLVE.md in the banked `mi_lensing_final/` folder, folded into MI Field Theory Results 2026, DOI [10.5281/zenodo.21403470](https://doi.org/10.5281/zenodo.21403470), erratum [21415677](https://doi.org/10.5281/zenodo.21415677)) assembled the **total** gravitating stress tensor of the MI action — matter legs and frame-constraint legs together — and found that it sources a *suppressed* effective density $\rho_{\rm eff}=\rho K = \rho/\nu$. The single metric therefore under-lenses: the lensing ratio

$$
F(y) \equiv \frac{g_{\rm lens}}{\nu(y)\,g_{\rm bar}} < \frac{1}{\nu(y)} < 1 \quad \text{everywhere}.
$$

The observed relation is different. The measured weak-lensing radial-acceleration relation (RAR) of Brouwer et al. (2021, KiDS-1000 isolated galaxies) coincides with the *dynamical* RAR: null geodesics feel an effective lensing mass enhanced to $\nu\rho$, not suppressed to $\rho/\nu$. Single-metric pure MI is excluded relative to that lensing-RAR $=$ dynamical-RAR equality at $\sim27\sigma$ (conservative rail, footing-independent). The gap between what is sourced ($\rho/\nu$) and what the equality requires ($\nu\rho$) is a factor $\nu^2$.

### 1.5 Statement of the result

The natural follow-up is a completion question: can the $\nu^2$ wedge be closed by adding structure to the action, while retaining everything that makes the program distinctive? We formalize "everything distinctive" as four desiderata (Section 3) and show that, **conditional on kernel passivity**, the target is unsatisfiable. The result is an **obstruction theorem**:

> Assume kernel passivity. Then $D\wedge S \Rightarrow \lnot L$: no field theory extending the MI action keeps $a_0$ tied to the passive kernel ($D$), propagates photons and gravitons on one metric ($S$), and reproduces the single-metric MOND-lensing phantom $(\nu-1)\rho$ ($L$). Equivalently $\{D,S,L\}$ is the unique minimal unsatisfiable subset of $\{D,S,G,L\}$; ghost-freedom $G$ enters no step.

The physical crux is a passivity/amplification dichotomy (Section 6): the property that derives $a_0$'s scale (passivity, $\sup K=1$) is the very property that forbids the lensing enhancement (which needs $\nu>1$, outside the passive cone). A completion *does* exist — but only as modified *gravity*, at the cost of $a_0$ becoming a free coupling. We frame this as neither a triumph nor a funeral: it is an exact obstruction, conditional on passivity, that shows the $a_0$ reframing is load-bearing, and it redirects the search for an MI-versus-MG discriminant away from lensing (now a shared observable) and back to the relational velocity-dispersion spread.

---

## 2. Setup

### 2.1 The action and its kernel

The covariant MI action is (signature $-{+}{+}{+}$)

$$
S = S_{\rm EH}[g] + S_u[g,u,\lambda] + S_{\rm matter}[g,u,\psi;K],
$$

with $S_{\rm EH}$ the Einstein–Hilbert term, $S_u = -\int\sqrt{-g}\,\tfrac{\lambda}{2}(u\cdot u+1)$ the passive frame with its Lagrange multiplier (zero propagating dof), and a matter sector dressed by the kernel,

$$
S_{\rm matter} \supset -\tfrac12\int\sqrt{-g}\,\rho_m\,s\,(u\cdot u)\,K(\Box_u/a_0^2), \qquad s=-1.
$$

The passivity premise (Section 1.2) attaches to $K(\Box_u)$: bounded, causal, positive spectral measure, $\|K\|\le1$, sum rule $\int d\mu/|t|=1$ (banked v4, v11). These properties underwrite two things at once — the causal-retarded well-posedness of the theory, and the identification $a_0 = cH_\Lambda/Z$ (the amplitude of a passive vacuum response is floored at the horizon scale). The static real-space dressing $K(X)$ of Section 1.2 is the object that enters the weak-field computation; the load-bearing fact we use downstream is only $\sup K = 1$.

### 2.2 The worldline law

On the rotation-curve shell the kernel argument collapses. With $X=|a|^2/a_0^2$ and the on-shell condition $|a|=g_{\rm obs}=\nu g_{\rm bar}$ (so $|a|/a_0=\nu y = \sqrt{y^2+y}$, hence $X=y^2+y$), one has $1+4X=1+4(y^2+y)=(2y+1)^2$, and the radical collapses:

$$
K\big|_{\rm on\text{-}shell} = \frac{(2y+1)-1}{2\sqrt{y^2+y}} = \frac{1}{\nu(y)}\ \text{exactly}, \qquad \frac{2K'X}{K}\bigg|_{\rm on\text{-}shell} = \frac{1}{2y+1}\le 1 .
$$

The on-shell dressing is the *suppression* $1/\nu\le1$, and the anisotropic slip factor $2K'X/K=1/(2y+1)$ is bounded and tension-signed.

### 2.3 The assembled stress tensor and the $\nu^2$ wedge

Assembling matter and frame legs in the only Newton-consistent bookkeeping (the composite frame $u=J^\mu/|J|$ for which $u\cdot u=-1$ identically, so the frame-constraint leg $S_u\equiv0$ and its stress $T^u\equiv0$; the $1/\nu$ dressing therefore comes entirely from the **matter** leg $\rho K$, not from a frame leg) yields

$$
\hat T_{\mu\nu} = \rho\,K(X)\,u_\mu u_\nu - 2\,\frac{\rho\,K'(X)}{a_0^2}\,a_\mu a_\nu .
$$

On the RAR shell this sources $\rho_{\rm eff}=\rho K=\rho/\nu$ (a *suppression*) plus an anisotropic radial tension $\Pi = -\rho_{\rm eff}/(2y+1)$ carrying the bounded, tension-signed slip factor — it *reduces* lensing rather than enhancing it. Linearizing Einstein on the single metric ($ds^2 = -(1+2\Phi)dt^2+(1-2\Psi)d\vec x^2$),

$$
\nabla^2\Psi = 4\pi G\,\rho_{\rm eff}, \qquad \Phi'-\Psi' = 4\pi G\,r\,\Pi, \qquad g_{\rm lens}=\tfrac12(\Phi'+\Psi'),
$$

every source term is $O(K)\le1$. There is **no $O(\nu)$ structure anywhere** in the assembled tensor.

The **wedge** is the gap between what lensing needs and what MI sources. The observed lensing-RAR $=$ dynamical-RAR equality needs effective mass $\nu\rho$ (enhanced *up*), while MI supplies $\rho/\nu$ (suppressed *down*):

$$
\underbrace{\nu\,\rho}_{\text{needed}} \quad\text{vs}\quad \underbrace{\rho/\nu}_{\text{sourced}} \qquad\Longrightarrow\qquad \text{factor } \nu^2 = 1+\frac{1}{y}.
$$

The missing piece is the **phantom mass** $M_{\rm ph}=(\nu-1)M_{\rm bar}$, exactly the density that QUMOND/AeST source gravitationally and MI does not. The whole completion problem is: *can the phantom be sourced without giving up the derivation of $a_0$'s scale?*

---

## 3. The completion problem

### 3.1 The desiderata

A satisfying MI completion of lensing would keep all of the following. We state each narrowly, so the theorem rests on definitions rather than on plausibility steps.

- **$D$ ($a_0$-derived).** $a_0$ enters the theory *solely* as the horizon-floored argument of the passive kernel $K(\Box_u/a_0^2)$ — **not** as an independent Lagrangian coupling. ($D$ is the *scale-tie*; the value and sign remain postulates, Section 1.3.)
- **$S$ (single-metric).** Photons and gravitons propagate on one metric, $c_\gamma=c_{\rm GW}$.
- **$G$ (ghost-free).** No Ostrogradsky mode, no negative-norm state.
- **$L$ (MOND-lensing).** The theory reproduces $g_{\rm lens}=\nu(y)\,g_{\rm bar}\to\sqrt{a_0 g_{\rm bar}}$ ($F\to1$): null geodesics feel the phantom $(\nu-1)\rho$. *We state $L$ without reference to the number of metrics* — this is what makes $S$ a non-redundant, essential hypothesis (Section 5).

with two secondary constraints — **Cassini** (Solar-System PPN safety, $\nu-1\sim 1/(2y)\to0$ at $y\sim10^6$) and **cosmology-preservation** (the growing mode $\nu_{\rm cosmo}\in[1,1.09]$, $\sigma_8$ $+2$–$3\%$, from the horizon-floored argument).

### 3.2 Two lemmas

The theorem is carried by two universal lemmas; the candidate constructions of Section 4 are existence-witnesses for the surviving corners, not the argument itself.

**Lemma 1 (nonlocality — uses $S$).** Under $S$, the lensing deflection is set by the single metric's stress tensor, so $L$ requires the phantom $(\nu-1)\rho$ to be **real gravitating stress-energy**. For a point mass $M$ ($g_{\rm bar}=GM/r^2$, $y=GM/(a_0r^2)$) the enclosed phantom that makes $g_{\rm lens}=\nu g_{\rm bar}$ is $M_{\rm ph}(r)=(\nu(y)-1)M$, and (sympy-exact)

$$
\frac{M_{\rm ph}(r)}{r}\;\xrightarrow{r\to\infty}\;\sqrt{\frac{a_0 M}{G}}\neq 0 ,
$$

an **unbounded halo** whose enclosed mass keeps growing where $\rho=0$. Now the precise content: a *local* functional of $\rho$ and the passive frame produces a phantom whose radial profile is fixed by the local acceleration invariant $|a|(r)$ **alone**, so its amplitude cannot carry the source mass $M$ that $(\nu-1)M$ requires — the same functional applied to two different masses gets the profile wrong for at least one (this is the mass-blindness that kills C1, §4.1). Matching the *mass-correct, universal* phantom for **all** sources is therefore what requires a nonlocal carrier — a term whose variation yields the elliptic equation $\nabla\cdot[\cdots]=\rho$ (the inverse-Laplacian of AQUAL/QUMOND). (A local term can produce *a* nonzero off-source phantom; what it cannot produce is the mass-correct one for every body.)

**Lemma 2 (boundedness — uses passivity).** By $\sup K = 1$, the passive kernel delivers only $O(K)\le1$ dressing. On the RAR shell it gives the $uu$-coefficient $K=1/\nu$ (suppression) and slip $2K'X/K=1/(2y+1)$ (bounded, tension). The phantom instead needs $uu$-coefficient $\nu-1/\nu = 1/\sqrt{y(y+1)}$ (deep-MOND $\sim1/\sqrt y$, unbounded); the shortfall

$$
\frac{\text{needed}}{\text{supplied}} = \frac{\nu-1/\nu}{1/\nu} = \nu^2-1 = \frac{1}{y}
$$

**diverges** as $y\to0$. No normalized passive kernel reaches $\nu$ on the RAR shell (a direct counterexample search finds the passive cap $1.0$ against a deep-MOND target $\approx31.6$; the value the frame actually realizes, $1/\nu$, is the *farthest* point from $\nu$).

**Both footings:** the halo amplitude $\sqrt{a_0 M/G}$ carries $a_0$, but the *nonlocality* (the nonzero limit) and the shortfall $1/y$ are footing-independent — they hold for $9.36\times10^{-11}$ and $1.13\times10^{-10}$ identically.

---

## 4. Candidate mechanisms

We computed three explicit completions. Each is a genuine attempt to close the wedge; each is an existence-witness landing on a different corner of the obstruction. All scripts exit 0 on both footings.

### 4.1 C1 — nonminimal frame-curvature: keeps $D$, fails $L$ by mass-blindness

Add a frame-kernel–curvature coupling with **no new dimensionful constant**,

$$
\Delta S = \frac{c^4}{16\pi G}\int\sqrt{-g}\; F\!\big(K(\Box_u/a_0^2)\big)\, Q, \qquad Q\in\{R,\ u^\mu u^\nu R_{\mu\nu}\}.
$$

Because $a_0$ enters only through $X$ inside $K$ and the prefactor is the bare $c^4/16\pi G$, this is a **clean $D$-side witness**: the coupling is dimensionless in $F$, and $a_0$ appears nowhere except as the horizon-floored kernel argument. (A separate dissatisfaction — that the *shape* of the free function $F$ is not itself fixed by the vacuum — is not an $a_0$-scale freedom and, as we now show, is not what defeats the candidate; $L$ fails first, on mass-blindness.)

Scalar–Ricci variation gives the standard scalar-tensor form; the new gravitating source is $-(g_{\mu\nu}\Box-\nabla_\mu\nabla_\nu)F(K)$, whose static $00$-projection is a Laplacian of a local scalar. By Gauss the enclosed phantom is a pure surface flux, $M_{\rm ph}(r)=(c^2/G)\,\kappa\,r^2 F'(r)$ — nonzero off-source, so a local term *does* source *a* phantom. But imposing lensing closure $M_{\rm ph}=(\nu-1)M_{\rm bar}$ on a point mass yields (sympy-exact)

$$
F'(y) = -\frac{\nu(y)-1}{2\kappa\sqrt y}\,\frac{\sqrt{GMa_0}}{c^2} \;\propto\; \sqrt{M}.
$$

The required shape **carries the source mass**: $F'_{\rm req}(y;M_2)/F'_{\rm req}(y;M_1)=\sqrt{M_2/M_1}$, independent of $y$. A local $F(K)$ sees only $|a|$ — it is *blind to the source mass* — so no single universal $F$ sources the phantom for more than one object (Lemma 1). Fixing $F$ on a $6\times10^{10}M_\odot$ galaxy and applying it to a $10^{14}M_\odot$ cluster, the cluster receives phantom fraction

$$
\sqrt{\frac{6\times10^{10}}{10^{14}}} \approx 0.024,
$$

i.e. $\sim 2.4\%$ of the needed phantom — under-lensed by a factor $1/0.0245\approx 41$. By the $\sqrt{}$ symmetry the reverse tuning (fix on the cluster, apply to the galaxy) over-lenses by the same $\approx41\times$. The miss is footing-independent ($a_0$ cancels in the ratio). Separately, under honest metric variation $X=|a|^2/a_0^2$ is a function of first metric derivatives, so $\Box F(K)$ contains third metric derivatives ($\Phi'''$) — a genuine Ostrogradsky ghost, unless one *freezes* $X$ and prescribes the scalar by hand (which is no longer MI). Crucially, **C1 fails $L$ by mass-blindness regardless of its ghost**, so it is a clean $D=1$ witness for the "$G$ is not the lever" step. Verdict: **fails-lensing, $D$ kept**.

### 4.2 C2 — nonlocal-in-matter (Deffayet–Esposito-Farèse–Woodard class): closes $L$, loses $D$

Take a purely-metric, single-metric, nonlocal-in-matter distortion of Einstein–Hilbert,

$$
S = \frac{1}{16\pi G}\int\sqrt{-g}\,R\big[1+f(\Box^{-1}R)\big] + S_{\rm matter}[g,\psi],
$$

with $\Box^{-1}$ a *retarded* Green function (so the distortion is a functional of matter history) and $f$ chosen so the weak-field limit is the QUMOND/AQUAL modified-Poisson equation $\nabla\cdot[\nu(|\nabla\Phi_N|/a_0)\nabla\Phi_N]=4\pi G\rho$. This is the nonlocal-metric MOND realization of Deffayet, Esposito-Farèse & Woodard (2011).

It works. The nonlocal term sources the phantom mass $\nu\rho$ on the single metric as a genuine scalar energy density, with **zero** anisotropic stress; the no-slip theorem then gives $\Phi=\Psi$, so $g_{\rm lens}=\nu g_{\rm bar}$ and the deep slope $\to\sqrt{a_0 g_{\rm bar}}$ ($F\to1$, machine-checked). It is purely metric, so $c_\gamma=c_{\rm GW}$ (GW170817-safe), and Cassini-safe by construction ($\nu-1=5\times10^{-7}$ at $y=10^6$).

But $a_0$ is now **free**, and the load-bearing reason is *structural*, not merely a fit degeneracy: there is **no passive frame, no kernel $K(\Box_u)$, no $Z=\sqrt{32\pi/3}$** — the nonlocal operator acts on $R$ (matter curvature), not on a vacuum frame, so nothing ties $a_0$ to $cH_\Lambda$. It enters as an independent coupling inside $f$, i.e. $\lnot D$ by definition. (Corroborating, but weaker: the MOND relation $g_{\rm obs}=\sqrt{g_{\rm bar}^2+a_0 g_{\rm bar}}$ is form-invariant under $(a_0,g_{\rm bar})\to\lambda(a_0,g_{\rm bar})$, so both footings fit equally. This footing-non-diagnosticity is a property of the RAR *relation itself* and is **shared by $a_0$-derived pure MI** — the SPARC RAR is likewise convention-compatible and non-diagnostic of $9.36\times10^{-11}$ — so it does not by itself mark C2 as MG; the structural absence of the kernel does.) The one residual partial: $\Box^{-1}$ carries a horizon IR scale, so $a_0\sim cH_\Lambda$ is *natural* parametrically — but natural is not derived, and $Z$ (hence the exact value) is not sourced. Secondary costs: a localized would-be ghost (kinetic eigenvalues $\pm\tfrac12$) tamed only by the *contested* retarded prescription, and a separate cosmology fit of $f$. Verdict: **closes $L$, $a_0$ free ($=$ MG)**.

### 4.3 C3 — frame/scalar carrier: closes $L$, loses $D$, plus one new dof

Ask whether the frame's dressed momentum can source curvature. Sub-candidate **C3a** (passive frame only, $a_0$ kept derived, 0 new dof): the matter leg's $uu$ coefficient is $O(K)=1/\nu$ and the frame-constraint leg vanishes identically ($u\cdot u=-1$), so the assembled source delivers the suppression $1/\nu$, short of the needed $\nu$ by $\nu^2-1=1/y$, diverging deep-MOND. **Fails lensing**, reproducing the SOLVE.md result exactly. Sub-candidate **C3b** (promote the carrier to a nonlocal scalar): the only local $h(X)$ reaching the deep phantom is $h\sim a_0/|a|$ — the AQUAL term — which makes the potential equation nonlinear and the phantom nonlocal (the same unbounded halo $M_{\rm ph}/r\to\sqrt{a_0M/G}$). A spatial-kinetic carrier is then mandatory, so it **propagates**: one new scalar dof, its acceleration scale a free coupling. Lensing closes ($F\to1$), $c_\gamma=c_{\rm GW}$ holds (the scalar sources via its own $T_{\mu\nu}$, no disformal photon coupling), ghost-free holds ($f'>0$), Cassini-safe — but $a_0$ is **free** and cosmology is forfeited to the new scalar. Verdict: **closes $L$, $a_0$ free ($=$ MG), $+1$ scalar dof**.

### 4.4 Scorecard

| lane | candidate $\Delta S$ | $L$ (lensing) | $S$ ($c_\gamma=c_{\rm GW}$) | $G$ (ghost) | Cassini | cosmology | $a_0$ | verdict |
|---|---|---|---|---|---|---|---|---|
| **C1** | $\int\!\sqrt{-g}\,F(K(\Box_u/a_0^2))\{R,\,uuR_{\mu\nu}\}$ | **FAIL** (mass-blind $\sqrt M$; $2.4\%$ / $41\times$) | OK (scalar-$R$) / risk ($uuR_{\mu\nu}$) | **FAIL** (honest-var Ostrogradsky $\Phi'''$) | OK* | plausible | **kept-derived** | **fails-lensing** |
| **C2** | $\int\!\sqrt{-g}\,R[1+f(\Box^{-1}R)]$, retarded | **PASS** ($F\to1$, $\sqrt{}$ slope) | **PASS** (purely metric) | cost ($\pm\tfrac12$; prescription-dependent) | PASS* (inherits $Q_2$) | tune (separate fit) | **FREE** | **closes, $a_0$ free** |
| **C3a** | passive $-\tfrac12\rho\,h(X)(u\cdot u)$ | **FAIL** (delivers $1/\nu$, short $1/y$) | PASS | PASS (0 dof) | PASS | PASS | **kept-derived** | fails-lensing |
| **C3b** | freed nonlocal carrier ($a_0/|a|$) | **PASS** ($F\to1$, $\sqrt{}$ slope) | PASS (own $T_{\mu\nu}$) | PASS ($f'>0$) | PASS | **forfeited** | **FREE** ($+1$ scalar dof) | **closes, $a_0$ free** |

The pattern is exact: every lane that keeps $D$ (C1, C3a) fails $L$; every lane that achieves $L$ (C2, C3b) loses $D$. No lane holds both. Note C2's $G$-bit is *prescription-dependent* (whether the $\pm\tfrac12$ block is a genuine ghost or merely non-propagating hinges on the contested retarded prescription); C3b is the clean ghost-free $L$-side witness. Either way C2 lands on $\lnot D$ independent of its $G$-bit. These are witnesses; the rigor of the result lives in Lemmas 1–2 (Section 5), not in the enumeration.

---

## 5. The obstruction theorem

### 5.1 Statement

**Theorem (conditional on kernel passivity).** *Assume the passivity premise (Section 1.2). Then $D\wedge S\Rightarrow\lnot L$: no field theory extending the MI action keeps $a_0$ as the passive-kernel argument ($D$), propagates on one metric ($S$), and reproduces the MOND-lensing phantom $(\nu-1)\rho$ ($L$). Equivalently, $\{D,S,L\}$ is the **unique minimal unsatisfiable subset** of $\{D,S,G,L\}$: each proper subset is realized —*

- *$\{D,S\}$ = pure MI (the current theory; $L$ off);*
- *$\{S,L\}$ = Deffayet–Esposito-Farèse–Woodard / AeST with $a_0$ a **free** coupling ($D$ off);*
- *$\{D,L\}$ = a disformal two-cone construction $\tilde g=g+B(\Box_u)\,u_\mu u_\nu$ with $B$ in the passive kernel, which keeps $a_0$ derived but carries a second photon cone excluded observationally by GW170817 ($S$ off).*

*Ghost-freedom $G$ enters no step.*

The connective is **"cannot coexist," $\lnot(D\wedge L)$ under $S$** — not exclusive-or: the pure-GR corner has *neither* $D$ nor $L$, which an XOR would misclassify. Earlier notes that wrote "$D\oplus L$ / XOR" are corrected here.

### 5.2 Why $S$ is essential (and the theorem non-redundant)

Because $L$ is stated metric-agnostically (Section 3.1), $S$ is a genuine, independent hypothesis with a precise role: **under $S$, lensing is fixed by the one metric's $T_{\mu\nu}$, so $L$ forces the phantom to be real gravitating stress-energy**, and Lemma 1 then bites. Drop $S$ — allow a disformal second cone $\tilde g=g+B\,u u$ — and photons see a *different* metric: the phantom becomes **pure geometry with no new stress-energy**, Lemma 1 is evaded, $a_0$ stays inside the passive kernel $B(\Box_u)$, and $L$ is achieved with $D$ kept. That $\{D,L,\lnot S\}$ construction is logically satisfiable as a field theory; it is killed only *observationally*, by GW170817: a disformal coupling large enough to carry the $O(\nu)$ lensing deflection splits the photon and graviton cones far above the bound $|c_\gamma/c_{\rm GW}-1|\lesssim10^{-15}$ (Abbott et al. 2017), while the GW-safe small-$B$ regime cannot source an $O(\nu)$ deflection — the same passivity/amplification wedge, now on the disformal axis. (A merely *conformal* bimetric $\tilde g=A(\phi)g$ preserves the null cone, $c_\gamma=c_{\rm GW}$, but cannot bend light beyond its baryonic content at all — the historical reason TeVeS (Bekenstein 2004) needed a disformal/vector part; conformal rescaling is a distinct non-escape.) This is exactly why $S$ belongs in the minimal unsatisfiable subset: the $\{D,L\}$ witness exists, and $S$ is what excludes it.

### 5.3 The mechanism as lemmas, and the enumeration as bookkeeping

The theorem's content is the single implication $D\wedge S\Rightarrow\lnot L$, carried by:

- **Lemma 1 (nonlocality, §3.2, uses $S$):** a mass-correct universal single-metric $L$ requires a nonlocal $(\nu-1)\rho$ carrier.
- **Corollary (propagation $\Rightarrow\lnot D$):** a nonlocal carrier reproducing the elliptic phantom has a spatial-kinetic term, so it propagates (a new dof) or its shape is a free function put in by hand; either way its acceleration scale is an independent Lagrangian coupling, i.e. **not** the passive-kernel argument — $\lnot D$ **by the definition of $D$** (this is where narrow-$D$ makes the step a near-tautology rather than a plausibility claim). [witnesses: C2, C3b]
- **Lemma 2 (boundedness, §3.2, uses passivity):** keeping $D$ confines the modification to the passive kernel $\sup K=1$ ($O(K)$ dressing, $T_{00}=0$ off $\mathrm{supp}\,\rho$), which cannot source the $O(\nu)$ unbounded phantom — $\lnot L$. [witnesses: C1, C3a]

A finite truth table over the 16 assignments of $\{D,S,G,L\}$ (script `nogo.py`, exit 0) then reads off that the target $D=S=L=1$ is absent, that $\{D,S,L\}$ is the unique minimal unsatisfiable subset, and that the $\{D,L\}$ witness survives the mechanism but is GW-excluded. **We emphasize the table is bookkeeping**: it is modus ponens over Lemmas 1–2, and the entire physics content lives in those two lemmas over the examined term classes (frame-curvature, nonlocal-in-matter, frame carrier). It is not an exhaustion over all possible Lagrangians, and the result's strength is exactly the strength of Lemmas 1–2 as physics statements over those classes.

The observationally-viable single-metric corners are:

| $D$ | $S$ | $G$ | $L$ | identity |
|:-:|:-:|:-:|:-:|---|
| 1 | 1 | 1 | 0 | **pure MI / C3a** — $a_0$ derived, ghost-free, under-lenses ($F<1/\nu$; the current theory) |
| 1 | 1 | 0 | 0 | **C1** — local ghostly frame term; still fails $L$ (mass-blind) even with a ghost |
| 0 | 1 | 1 | 1 | **C2, C3b** — closes $L$, single-metric, ghost-free, but $a_0$ **free** ($=$ MG) |
| 0 | 1 | 0 | 1 | nonlocal with untamed ghost — closes $L$, $a_0$ free, ghost (contested) |
| 0 | 1 | 1 | 0 | GR / trivial |
| 0 | 1 | 0 | 0 | GR $+$ ghost (vacuous) |

The target $D=S=G=L=1$ is **absent**, and so is its ghost-relaxed sibling $D=S=1,G=0,L=1$: relaxing ghost-freedom does not rescue $\{D,S,L\}$, because C1 fails $L$ by mass-blindness regardless of its ghost. This is why $G$ is not the lever.

### 5.4 Footing independence

The wedge is $a_0$-free. The shortfall $\nu^2-1=1/y$ and the mass-blindness ratio $\sqrt{M_2/M_1}$ are dimensionless in $y=g_{\rm bar}/a_0$, and $\nu$ is form-invariant under $(a_0,g_{\rm bar})\to\lambda(a_0,g_{\rm bar})$. Both footings ($9.36\times10^{-11}$ / $1.13\times10^{-10}$) give the identical dimensionless verdict.

---

## 6. The passivity/amplification dichotomy

Here is the physical crux, the intended central idea of the paper.

$a_0=cH_\Lambda/Z$ is derivable **only because** the MI modification is a passive, causal vacuum-response kernel with a normalized positive measure. Passivity floors the response amplitude at the horizon scale — it is the source of the scale-tie. But passivity has a mathematical consequence: $\sup K = 1$. A passive kernel can only **suppress**. On the RAR shell it delivers exactly $\rho/\nu$; deep-MOND $K\to0$, the source dressed all the way down.

MOND-lensing demands the opposite. The phantom $(\nu-1)\rho$ is an **enhancement** to $\nu\rho$, with $\nu>1$ — strictly *outside* the passive cone whose supremum is $1$. The needed $uu$-coefficient is $\nu-1/\nu=1/\sqrt{y(y+1)}$ (unbounded, deep $\sim1/\sqrt y$); the passive kernel supplies $1/\nu$; the shortfall $\nu^2-1=1/y$ **diverges** as $y\to0$.

So the dichotomy is exact and structural, not a failed search:

> **The very property that ties $a_0$'s scale to the vacuum — passivity, $\sup K=1$ — is the property that forbids the lensing phantom.** Enhancement requires an anti-dissipative (pumped) kernel, whose amplitude is a free coupling, so $a_0$ would no longer be $cH_\Lambda/Z$.

The nonlocality lemma closes the loop from the other side: the mass-correct phantom of a point mass is an unbounded halo ($M_{\rm ph}(r)/r\to\sqrt{a_0M/G}$), so sourcing it universally forces a nonlocal carrier with a spatial-kinetic term — a propagating dof whose acceleration scale is a free coupling. Passivity forbids the enhancement; the halo's nonlocality forces propagation; propagation frees $a_0$. The two horns are the same wall seen from two sides.

Two honest guards on this statement. First, boundedness ($\lnot L$) uses **only** $\sup K=1$ — it does not invoke the $a_0$ value-derivation at all. So "$a_0$ derived" and "$\lnot L$" are not one claim chained back on itself; they are two consequences of the **one** passivity premise (a common-premise entailment, not a biconditional — we do not claim, and do not need, the converse "$a_0$-derived $\Rightarrow$ passive"). Second, this is *sufficiency*, not necessity: passivity $\Rightarrow$ ($a_0$-scale-tied $\wedge\ \lnot L$). Whether some **non-passive** kernel could also derive $a_0$ — breaking the lock — is precisely the open pump door of Section 7, so the lock itself is conditional on staying inside the passive class.

---

## 7. Scope and conditionality

We are explicit, both ways, about the strength of this result.

**It is conditional.** The obstruction rests on the single premise of MI-kernel passivity: the response is bounded, causal, positive-measure (Herglotz–Nevanlinna), $\|K\|\le1$, with the sum rule $\int d\mu/|t|=1$, so its real-space dressing obeys $\sup K=1$. This premise is banked and frozen (MI action v4, v11) but it is a *premise*, not a metatheorem. Were the kernel not passive, the argument would not run.

**Within the passive class, $D$ and $\lnot L$ share one origin.** The same passivity premise is what *derives* $a_0$'s scale and what caps $K$ at $1$; $\lnot L$ follows from the cap alone (Section 6). One cannot, inside the passive class, keep the derivation while discarding the boundedness that forbids $L$ — they are two faces of the one hypothesis, which is what makes the obstruction a real dichotomy rather than a coincidence of two separate assumptions. We state this as common-premise entailment, not as a biconditional lock: the claim is passivity $\Rightarrow(D\text{-scale}\wedge\lnot L)$, and whether $D$ could ever hold *without* passivity is the open door below. So the lock is genuine within the passive class and itself conditional on it.

**The one MI escape, and why it is currently shut.** The only way out that keeps $a_0$ tied to $cH_\Lambda$ with a *derived* amplitude is a causal **enhancing** kernel ($\nu>1$) — an anti-dissipative / pumped vacuum response, i.e. a *non-passive* kernel that nonetheless derives $a_0$. The banked sign walls (v4, v11) find no such channel pump-free: passive, reactive, and 4-point/dS-positivity edges are all sign-blind or anti-MOND-locked, and the enhancement reopens only under a *new forced pump mechanism* that has not been exhibited. Absent that, the no-go stands as effectively final for the passive class. **We do not claim the theory is closed.** The door labeled "forced pump" remains open in principle; what the banked results establish is that it is not open by any pump-free route so far identified — and, since a non-passive $a_0$-deriving kernel is exactly what would break the $D$/boundedness lock, that same door is the one place the lock could fail.

**We do not overclaim in either direction.** The obstruction is not more final than "conditional-on-passivity"; nor is it softened — within the passive class it is exact and realized three independent ways. There is no manufactured no-go and no manufactured completion.

---

## 8. Consequences

**(i) A completion exists — as modified gravity, at the cost of the $a_0$ derivation.** C2 and C3b constructively demonstrate a single-metric, ghost-free (C3b) or ghost-cost (C2), GW170817-safe field theory that reproduces MOND dynamics *and* MOND lensing, with the correct deep slope. This is real, honest content. But it is modified *gravity* in the Deffayet–Esposito-Farèse–Woodard / AeST (Skordis & Zlosnik 2021) class, not modified inertia: it forfeits the vacuum-derived $a_0=cH_\Lambda/Z$, demoting $a_0$ to a free Lagrangian coupling, plus (C2) a separate cosmology fit and a contested would-be ghost, or (C3b) one new propagating scalar and a forfeited cosmology. The cost is precisely the program's single most distinctive claim.

**(ii) Lensing becomes a shared-MG observable.** Because the only completions that reproduce the lensing phantom are MG (C2, C3b degenerate there with AeST), weak lensing can no longer discriminate MI from MG — both predict the same $F\to1$ MOND-lensing relation. The clean modified-gravity-*impossible* discriminant reverts to the non-adiabatic **relational velocity-dispersion spread**: MI predicts a $6$–$13\%$ spread in member dispersions from the relational (frame-history-dependent) inertia, while MG predicts *exactly* zero. That observable — currently underpowered — is the one place MI $\neq$ MG survives, and it is where discrimination effort should now go. (Any MG completion also inherits the AeST $Q_2$-quadrupole Solar-System caveat of Desmond, Hees & Famaey 2024 and Park et al. 2026 — a shared-MG cost, honestly stated.)

**(iii) The obstruction shows the $a_0$ reframing is load-bearing.** If $a_0=cH_\Lambda/Z$ were a trivial or cosmetic relabeling, one could keep it while adding any lensing structure. That it is *incompatible* — within the passive class — with single-metric MOND-lensing shows it is a genuine, restrictive, physical commitment: the passivity that derives its scale is a real constraint on the theory space. The reframing's distinctive content is exactly what is forbidden on the MG-lensing side. Far from a funeral, this is evidence the reframing is doing work.

---

## 9. Conclusion

We have identified, and machine-verified on both footings, an obstruction — conditional on kernel passivity — in the de Sitter–Unruh modified-inertia program: **a passive-kernel-derived $a_0$ and single-metric MOND weak-lensing cannot coexist.** The central implication is $D\wedge S\Rightarrow\lnot L$; equivalently $\{D,S,L\}$ is the unique minimal unsatisfiable subset of $\{D,S,G,L\}$, with $\{D,S\}$ = pure MI, $\{S,L\}$ = Deffayet–Esposito-Farèse–Woodard / AeST ($a_0$ free), and $\{D,L\}$ = a disformal two-cone construction ($a_0$ derived) killed observationally by GW170817. Ghost-freedom is not the lever. The mechanism is a passivity/amplification dichotomy — the passive kernel that floors $a_0$'s scale at the horizon can only suppress the source to $\rho/\nu$, whereas lensing needs enhancement to $\nu\rho$, outside the passive cone — reinforced by a nonlocality lemma that turns any mass-correct lensing carrier into a propagating degree of freedom whose acceleration scale is a free coupling. Three explicit candidates witness the surviving corners: C1 fails lensing by mass-blindness ($\sim2.4\%$ of the phantom on a cluster fixed to a galaxy, $\sim41\times$ under-lensed), while C2 and C3b close lensing exactly but only as modified gravity with $a_0$ free.

The result is conditional on kernel passivity — but that premise is the very thing that derives $a_0$'s scale, so within the passive class the derivation and the obstruction are two faces of one hypothesis. The only MI escape, a causal enhancing kernel, is shut by the banked sign walls pump-free and reopens only under a new forced pump mechanism not yet exhibited; we therefore do not claim the theory is closed. The honest map: the MI program is complete for dynamics ($0.108$ dex on SPARC) and viable in cosmology, and its lensing sector completes only by crossing into modified gravity at the cost of the $a_0$ reframing. Lensing is now a shared observable; the clean discriminant is the relational $\sigma$-spread. And the obstruction itself is the strongest evidence that the $a_0=cH_\Lambda/Z$ reframing is load-bearing physics rather than a relabeling.

---

## Appendix A. Verification scripts

All scripts are committed in `prep_2026/mi_lensing_completion/`, run against a frozen read-only repository, and exit 0 on both footings ($a_0=9.36\times10^{-11}$ canonical $=cH_\Lambda/Z$, and $1.13\times10^{-10}$ alternate). They use sympy for exact symbolic checks and numeric grids where a radical will not auto-collapse. No candidate passes all checks, so none is asserted as a full completion.

- **`c1_frame_curvature.py`** (11/11, exit 0). The frame-curvature variation gives $M_{\rm ph}(r)=(c^2/G)\kappa r^2 F'(r)$; lensing closure forces $F'(y)\propto\sqrt M$ (sympy-exact); the two-mass ratio $\sqrt{M_2/M_1}$ is $y$-independent (mass-blindness); the cluster phantom fraction $\sqrt{6\times10^{10}/10^{14}}\approx0.024$ ($\sim41\times$ under-lensing); and the honest-variation Ostrogradsky term ($\Box F(K)$ contains $\Phi'''$).

- **`c2_nonlocal.py`** (18/0, exit 0). The Deffayet–Esposito-Farèse–Woodard nonlocal-in-matter term sources $\nu\rho$ with zero anisotropic stress, no-slip $\Phi=\Psi$, $F\to1$ with the $\sqrt{a_0 g_{\rm bar}}$ slope; $c_\gamma=c_{\rm GW}$ (nonlocal prefactor cancels in the GW dispersion); the $\pm\tfrac12$ would-be-ghost eigenvalues; and form-invariance of $\nu$ under $(a_0,g_{\rm bar})\to\lambda(\cdots)$ ($a_0$ free — noted as *shared* with pure MI, so structural, not the primary marker).

- **`c3_carrier.py`** (exit 0). C3a delivers the $1/\nu$ suppression (shortfall $\nu^2-1=1/y$); C3b's local $h\sim a_0/|a|$ (AQUAL) gives the unbounded halo $M_{\rm ph}/r\to\sqrt{a_0M/G}$, forcing a propagating scalar with $a_0$ free.

- **`nogo.py`** (exit 0). The completeness check: the nonlocality limit; the boundedness shortfall and the tension-signed slip leg $2K'X/K=1/(2y+1)$; the mass-blindness ratio; footing independence of the wedge; and the finite truth table over $\{D,S,G,L\}$ showing $D\wedge S\Rightarrow\lnot L$, that $\{D,S,L\}$ is the unique minimal unsatisfiable subset (each proper subset realized, including the GW-dead $\{D,L\}$ disformal witness), and that the target corner and its ghost-relaxed sibling are both absent, with the surviving corners mapped onto C1/C2/C3. The table is bookkeeping over Lemmas 1–2, not an exhaustion over all Lagrangians.

- **`verify_adversarial.py`** (exit 0). An independent re-derivation (not reusing the candidate assertions) of the wedge $\nu^2$, the passivity/amplification dichotomy, the mass-blindness $\sqrt M$, the frame-lock fork, a direct passive-kernel counterexample search, and a check that C2's $F\to1$ is a genuine (not manufactured) closure that is nonetheless MG with $a_0$ free. Trap sweep both directions: no manufactured completion, no manufactured no-go, no hidden ghost in a "winner," $c_\gamma=c_{\rm GW}$ preserved, Cassini/cosmology honest. Verdict: **UPHELD**.

---

## References

- Abbott, B. P., et al. (LIGO/Virgo, Fermi-GBM, INTEGRAL) (2017). Gravitational Waves and Gamma-Rays from a Binary Neutron Star Merger: GW170817 and GRB 170817A. *ApJ Lett.* **848**, L13. arXiv:1710.05834. [The $|c_\gamma/c_{\rm GW}-1|\lesssim10^{-15}$ bound excluding the disformal second cone.]
- Bekenstein, J. D. (2004). Relativistic gravitation theory for the modified Newtonian dynamics paradigm. *Phys. Rev. D* **70**, 083509. [TeVeS; the two-metric / disformal lensing lineage.]
- Brouwer, M. M., et al. (2021). The weak lensing radial acceleration relation: constraining modified gravity and cold dark matter theories with KiDS-1000. *A&A* **650**, A113. arXiv:2106.11677; DOI 10.1051/0004-6361/202040108. [KiDS-1000 isolated-galaxy lensing RAR; the $\sim27\sigma$ benchmark.]
- Deffayet, C., Esposito-Farèse, G., & Woodard, R. P. (2011). Nonlocal metric formulations of MOND with sufficient lensing. *Phys. Rev. D* **84**, 124054. arXiv:1106.4984. [The C2 nonlocal-in-matter, purely-metric MOND-lensing realization.]
- Desmond, H., Hees, A., & Famaey, B. (2024). On the tension between the radial acceleration relation and Solar System quadrupole in modified gravity MOND. *MNRAS* **530**, 1781.
- Milgrom, M. (1983). A modification of the Newtonian dynamics as a possible alternative to the hidden mass hypothesis. *ApJ* **270**, 365.
- Milgrom, M. (1999). The modified dynamics as a vacuum effect. *Phys. Lett. A* **253**, 273. astro-ph/9805346. [The identical $\nu$-kernel modified-inertia law, Eq. 9; the framework's distinctive content is the $cH_\Lambda/Z$ coefficient, his was $2cH_\Lambda$.]
- Park, M., et al. (2026). Solar-System quadrupole constraints on modified gravity. arXiv:2602.17884.
- Skordis, C., & Zlosnik, T. (2021). New relativistic theory for modified Newtonian dynamics. *Phys. Rev. Lett.* **127**, 161302. arXiv:2007.00082. [AeST; the single-metric MG comparison class.]
- *Background (not the C2 citation):* Deffayet, C., & Woodard, R. P. (2009). Reconstructing the distortion function for nonlocal cosmology. *JCAP* **08**, 023. arXiv:0904.0961.
- **Self-citations.** Zimmerman, C. (2026). MI Field Theory Results 2026, DOI [10.5281/zenodo.21403470](https://doi.org/10.5281/zenodo.21403470) (erratum [21415677](https://doi.org/10.5281/zenodo.21415677)); The MI Action v4, DOI [10.5281/zenodo.21264727](https://doi.org/10.5281/zenodo.21264727), v11 [21284144](https://doi.org/10.5281/zenodo.21284144); the covariant / cluster no-go, DOI [10.5281/zenodo.20779562](https://doi.org/10.5281/zenodo.20779562).

---

*Reproduce:* `python3 {c1_frame_curvature,c2_nonlocal,c3_carrier,nogo,verify_adversarial}.py` in `prep_2026/mi_lensing_completion/` — all exit 0. Both $a_0$ footings carried throughout; the verdict is footing-independent. This is a conditional obstruction result, not a closure of the program.
