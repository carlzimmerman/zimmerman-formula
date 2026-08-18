# Determining the Free Function of Aether-Scalar-Tensor Gravity

**Carl P. Zimmerman**, Briar Creek Tech
ORCID 0009-0008-3508-7982
2026-08-17

---

## Abstract

Aether-Scalar-Tensor gravity (AeST; Skordis & Złośnik, *Phys. Rev. Lett.* **127**, 161302)
is the only relativistic MOND-class theory that reproduces the CMB power spectrum. It
contains one free function, $\mathcal{F}(\mathcal{Y},\mathcal{Q})$, which its authors leave
unspecified. We determine it in two independent steps. Its $\mathcal{Q}$-sector is fixed by
the identification $a_0^2(Q)=\kappa^2G\bigl(-K(Q)\bigr)$ — the MOND acceleration scale *is*
the dark sector's pressure — with $K$ an offset Dirac–Born–Infeld brane of tension
$M^4=\rho_\Lambda c^2$, giving $a_0=\kappa c\sqrt{G\rho_\Lambda}$. Its $\mathcal{Y}$-sector
is constrained by a legality requirement specific to AeST: because $\mathcal{F}$ depends on
the *scalar's own* gradient rather than on the total potential's, single-valuedness of the
free function — equivalently, absence of a longitudinal gradient ghost — requires the
anomalous acceleration to be a monotone increasing function of the baryonic one. This is
strictly stronger than the corresponding AQUAL condition.

That requirement has three consequences. First, it **excludes** the exponential interpolation
$\nu(y)=1/(1-e^{-\sqrt y})$ (Milgrom & Sanders 2008 at $\alpha=\tfrac12$): the induced
anomalous acceleration is non-injective, peaking at $0.6476\,a_0$ near $y=2.54$ and falling
thereafter, so no single-valued $\mathcal{F}$ reproduces it. Second, it **admits** the
relation $g_{\rm obs}^2=g_{\rm bar}^2+a_0g_{\rm bar}$, which is also the best-fitting legal
kernel on 3389 SPARC points at the anchored $a_0$. We explicitly do **not** claim uniqueness:
the legal class is infinite-dimensional and we exhibit closed-form alternatives. Third, and
most consequentially, **every** legal kernel saturates at an anomalous acceleration
$\approx a_0/2$, so a constant sunward anomaly of that size is structural to AeST under the
no-ghost condition. Against planetary ephemerides this is $\sim10^3$ times too large. We
state this as the theory's central open problem rather than resolving it.

---

## 1. The theory

AeST's action, verified verbatim against the authors' LaTeX
(arXiv:2007.00082 Eq. 5; restated independently as arXiv:2109.13287 Eq. 1):

$$S=\int d^4x\,\frac{\sqrt{-g}}{16\pi\tilde G}\Big[R-2\Lambda-\frac{K_B}{2}F^{\mu\nu}F_{\mu\nu}
+2(2-K_B)J^\mu\nabla_\mu\varphi-(2-K_B)\mathcal{Y}-\mathcal{F}(\mathcal{Y},\mathcal{Q})
-\lambda(A^\mu A_\mu+1)\Big]+S_{\rm m}[g]$$

with $\mathcal{Q}\equiv A^\mu\nabla_\mu\varphi$,
$\mathcal{Y}\equiv(g^{\mu\nu}+A^\mu A^\nu)\nabla_\mu\varphi\nabla_\nu\varphi$,
$F_{\mu\nu}=2\nabla_{[\mu}A_{\nu]}$, $J^\mu=A^\nu\nabla_\nu A^\mu$. Matter couples to
$g_{\mu\nu}$ alone, so lensing and dynamics agree with no dark halo.

### 1.1 The $\mathcal{Q}$-sector

We take

$$K(Q)=-M^4\sqrt{1-\frac{(Q-Q_0)^2}{\Lambda_D^2}},\qquad
\boxed{\;a_0^2(Q)=\kappa^2G\bigl(-K(Q)\bigr)\;}$$

i.e. $-K$ is a pure DBI brane of tension $M^4$. This is a *selection*
($\beta\equiv\mu^2\Lambda_D^2/M^4=1$: the dark-sector Lagrangian is exactly a brane volume
element), not a derivation, and we label it as such. Three properties follow without further
input: at the minimum $Q=Q_0$ one has $K=-M^4$ exactly, so $w=-1$ identically; small
excitations have energy density linear in the displacement and pressure quadratic, so they
are pressureless dust — the clustering component the CMB requires; and at the wall the
pressure vanishes, removing any early stiff phase. Normalising $M^4=\rho_\Lambda c^2$,

$$a_0=\kappa c\sqrt{G\rho_\Lambda}=c^2\sqrt{\Lambda/32\pi}
=9.3619\times10^{-11}\ \mathrm{m\,s^{-2}}\quad(\kappa=\tfrac12).$$

$\kappa$ is **fitted, not derived**: three independent determinations give
$0.551\pm0.043$ (distance-free), $0.465\pm0.076$ (baryonic Tully–Fisher) and
$0.537\pm0.071$ (gas-dominated galaxies at TRGB distances), combining to
$0.529\pm0.034$. An alternative footing ($\rho_{\rm total}$, $cH_0$) gives
$a_0=1.1279\times10^{-10}$; every dimensional number below is carried on both.

Because $-K$ was smaller in the past, $a_0(z)$ is derived rather than assumed: it is flat
below $z\approx20$ and switches off before recombination,
$a_0(1090)/a_0(0)\approx6\times10^{-3}$.

### 1.2 The $\mathcal{Y}$-sector, and the legality requirement

In the quasi-static limit the gradient sector diagonalises: with $\Psi=\Psi_N+\chi$ and
$\nabla^2\Psi_N=4\pi\hat G\rho$, the scalar obeys

$$\nabla\!\cdot\!\bigl[J_Y(|\nabla\chi|^2)\,\nabla\chi\bigr]=4\pi\hat G\rho ,$$

where $J$ is the $\mathcal{Y}$-part of $\mathcal{F}$. In spherical symmetry Gauss's theorem
integrates this exactly to the local algebraic law

$$u\,J_Y(u^2)=g_{\rm bar},\qquad u\equiv|\nabla\chi| ,$$

so the scalar's own gradient $u$ *is* the anomalous acceleration,
$u=(\nu(y)-1)\,g_{\rm bar}$ with $y\equiv g_{\rm bar}/a_0$.

Write $U(y)\equiv u/a_0$. Reconstructing the free function from a chosen interpolation gives
$J_Y(Y)=y(U)/U$ with $Y=a_0^2U^2$, which is invertible **iff $U(y)$ is strictly increasing**.
Equivalently: expanding $J$ to second order about a nontrivial background gives kinetic matrix
$M_{ij}=J_Y\delta_{ij}+2J_{YY}u_iu_j$, whose longitudinal eigenvalue is positive iff the same
monotonicity holds. A non-monotone $U$ therefore means both a multi-valued $\mathcal{F}$ and a
longitudinal gradient ghost.

$$\boxed{\;\text{LEGALITY: }\ U(y)\ \text{strictly increasing},\quad U\to\sqrt y\ (y\to0),
\quad U/y\to0\ (y\to\infty).\;}$$

---

## 2. What legality excludes

The operative interpolation of this programme until now — Milgrom & Sanders (2008) Eq. (13)
at $\alpha=\tfrac12$, $\nu(y)=1/(1-e^{-\sqrt y})$ — gives

$$U(y)=\frac{y}{e^{\sqrt y}-1},$$

which rises to $U=0.6476$ at $y=2.540$ and then **falls**, reaching $\sim10^{-3455}$ at 1 AU.
It is not injective, so no single-valued $\mathcal{F}$ reproduces it, and on the Newtonian
branch the longitudinal mode is a ghost of exponentially large magnitude. **AeST cannot host
it.** The same verdict applies at $\alpha=2$.

This is not a statement about exponentials as a class: $U(y)=\tfrac12(1-e^{-2\sqrt y})$ is
monotone and perfectly legal. It is a statement about this particular kernel, whose
screening — the property that made it attractive, since it suppresses solar-system effects by
$e^{-\sqrt y}\sim10^{-3457}$ — is exactly the non-monotonicity that makes it illegal.

---

## 3. What legality admits, and what it does not select

The relation

$$g_{\rm obs}^2=g_{\rm bar}^2+a_0\,g_{\rm bar}
\quad\Longleftrightarrow\quad \nu(y)=\sqrt{1+1/y}$$

gives $U(y)=\sqrt{y^2+y}-y$, strictly monotone, saturating at exactly $\tfrac12$. It is legal,
and its free function follows in closed form:

$$J_Y(Y)=\frac{v}{1-2v},\qquad
J(Y)=-a_0^2\Big[\frac{v(1+v)}{2}+\frac{\ln(1-2v)}{4}\Big],\qquad v\equiv\frac{\sqrt Y}{a_0},$$

whose deep-MOND limit is $J\to\tfrac23Y^{3/2}/a_0$ — the asymptotic form AeST's authors print.

**We do not claim this kernel is selected.** The legal class is infinite-dimensional; the
reconstruction above is explicit and invertible for *every* strictly-increasing $U$ with the
stated limits. Three closed-form alternatives share every property used above — monotonicity,
saturation at $\tfrac12$, and the same deep-MOND limit:

$$J_Y=\frac{v}{1-4v^2},\qquad J_Y=\frac{v}{(1-2v)^2},\qquad U=\tfrac12\bigl(1-e^{-2\sqrt y}\bigr).$$

In particular the shared deep-MOND limit is **not** evidence for any one member.

What data say: fitting the anchored $a_0$ (no fitted acceleration scale, no per-galaxy
freedom) to 3389 SPARC rotation-curve points,

| kernel | canonical $a_0$ | alt $a_0$ |
|---|---|---|
| $g_{\rm obs}^2=g_{\rm bar}^2+a_0g_{\rm bar}$ | **0.1980** | 0.2023 |
| $U=\tfrac12(1-e^{-2\sqrt y})$ | 0.1983 | 0.2031 |
| $J_Y=v/(1-2v)^2$ | 0.1998 | **0.1981** |
| $J_Y=v/(1-4v^2)$ | 0.2025 | 0.2114 |
| $\nu=1/(1-e^{-\sqrt y})$ *(illegal)* | 0.2048 | 0.2147 |

(rms residual in dex; this is raw point scatter, **not** the 0.108 dex obtained from the
maximum-likelihood pipeline with per-galaxy $\Upsilon$, and the two should not be compared.)

Two things are worth stating and neither is uniqueness. The excluded kernel is the **worst**
fit of the set on both footings — it fails legality and the data independently. And
$g_{\rm obs}^2=g_{\rm bar}^2+a_0g_{\rm bar}$ is the best legal fit on the framework's own
canonical footing, though it is not separable from the nearest alternative
($\Delta=0.0002$ dex) and loses narrowly on the alternative footing. Points within a galaxy
are correlated, so naive $\sqrt N$ scaling overstates all of these separations.

---

## 4. The central open problem

Legality forces $U$ to increase monotonically; matching the deep-MOND limit $U\to\sqrt y$
fixes its scale. Together these force $U$ to **saturate at a nonzero constant**, and across
the legal class that constant is $\approx\tfrac12$ — exactly $0.5$ for two of our examples,
$0.4975$ for the third. The anomalous acceleration therefore does not decay at large $y$: it
tends to $a_0/2$.

At 1 AU, $y\approx6\times10^7$, so a legal AeST predicts a **constant sunward anomaly of
$\approx a_0/2=4.7\times10^{-11}\,\mathrm{m\,s^{-2}}$** against a planetary-ephemeris bound of
$3.66\times10^{-14}\,\mathrm{m\,s^{-2}}$ (Sereno & Jetzer 2006) — over by a factor $\sim1.3
\times10^3$, or $\sim10^2$ after the external-field effect is included.

We emphasise the structure of this result. It is **not** specific to any kernel choice: it
follows from legality plus the deep-MOND limit, i.e. from the no-ghost condition plus the
existence of $a_0$ itself. The one interpolation that evades it — the exponential kernel,
whose $U\to0$ at large $y$ screens the solar system — evades it *precisely by being
non-monotone*, which is what makes it illegal. Within AeST one may have a ghost-free scalar
or a screened solar system, and this analysis finds no member of the class with both.

---

## 5. What is and is not claimed

1. **The scaffold is not ours.** AeST is Skordis & Złośnik's; the interpolation family is
   Milgrom & Sanders'; no-ghost conditions on free functions of this type are independently
   known. **The requirement is specific to AeST and does not carry over to AQUAL.** In AQUAL
   the free function depends on the gradient of the *total* potential, and stability requires
   only $dg_{\rm obs}/dg_{\rm bar}>0$ — which the exponential kernel satisfies (minimum
   $0.9676$ over $u\in(10^{-4},40)$), so it is perfectly legal there. In AeST
   $\mathcal{F}$ depends on $\mathcal{Y}$, built from the *scalar's own* gradient, and that
   is the stronger condition which excludes it. The exclusion in §2 is therefore a statement
   about AeST specifically, not an inherited AQUAL result. This work contributes the
   normalisation $a_0=\kappa c\sqrt{G\rho_\Lambda}$,
   the pressure promotion $a_0^2=\kappa^2G(-K)$, the derived $a_0(z)$, and the application of
   legality to AeST specifically — including the exclusion in §2 and the structural
   consequence in §4.
2. **$\kappa=\tfrac12$ is fitted, not derived.** Six classes of derivation are closed by
   explicit calculation; three routes remain open. $\kappa$ must be quoted with its $H_0$:
   the distance-free determination carries an unpriced $\sim7\%$ systematic because most of
   its galaxies use Hubble-flow distances at $H_0=73$ while $c\sqrt{G\rho_\Lambda}$ is
   Planck-footed.
3. **Uniqueness is not claimed** (§3), and the shared deep-MOND limit is not evidence.
4. **Dark matter is present at full $\Omega_{\rm dm}$.** The claim is "no dark-matter
   *particle*," nothing stronger. Whether the dust stays bound inside galaxies is unresolved:
   the excitation is pressureless, $\rho=Q_0n$ ties its mass to a conserved charge, dynamics
   sees $\rho+3p$ while lensing sees $\rho+p$, and $c_s^2\propto a^{-3}$ for every ghost-free
   $K$. Four catalogued second-field escapes fail.
5. **The preferred-frame sector is unresolved.** AeST's aether sits on the degenerate locus
   $c_1+c_2+c_3=0$ where the spin-0 mode does not propagate, and where Foster & Jacobson
   explicitly exclude their PPN results. We report no $\alpha_1,\alpha_2$ here.
6. **This is not a theory of everything** and addresses no part of the Standard Model.

**Falsifiability.** A hash-frozen pre-registration predicts the Gaia DR4 wide-binary velocity
boost, decided around December 2026. On the kernel adopted here the point target is
$\gamma_v=1.139$ (canonical) / $1.169$ (alt); the previously registered band was computed on
the now-excluded exponential kernel and requires a dated amendment filed before data.

**Reproducibility.** Every number is produced by a committed script at
<https://github.com/carlzimmerman/zimmerman-formula>: `nbody_2026/stage75_the_closed_theory_2026.py`
(the construction), `real_research/reviews/typeII_*_2026.py` (the quasi-static reduction and
the legality analysis, including the refutation of uniqueness),
`real_research/rar_framework_a0_mlfit.py` (the RAR fit), and
`real_research/reviews/aqual_efe_a0line_kernel_2026.py` (the wide-binary target). Withdrawn
claims are recorded, dated, in `RETRACTIONS.md`.

**Attribution.** AeST: Skordis & Złośnik, *Phys. Rev. Lett.* **127**, 161302 (2021),
arXiv:2007.00082, and arXiv:2109.13287. Interpolation family: Milgrom & Sanders, *ApJ*
**678**, 131 (2008). PPN aether results: Foster & Jacobson, *Phys. Rev. D* **73**, 064015
(2006). Ephemeris bound: Sereno & Jetzer (2006). The $a_0$–$\Lambda$ coincidence has prior
art in Milgrom (1999), Blanchet & Le Tiec (2009), Pikhitsa (2010) and Klinkhamer & Kopp (2011).
