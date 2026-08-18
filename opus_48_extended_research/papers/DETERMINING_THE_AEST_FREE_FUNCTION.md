# Aether-Scalar-Tensor Gravity Cannot Fit Galaxies and the Solar System Simultaneously

**Carl P. Zimmerman**, Briar Creek Tech
ORCID 0009-0008-3508-7982
2026-08-17

---

## Abstract

Aether-Scalar-Tensor gravity (AeST; Skordis & Złośnik, *Phys. Rev. Lett.* **127**, 161302) is
the only relativistic MOND-class theory reproducing the CMB power spectrum. It contains one
free function, $\mathcal{F}(\mathcal{Y},\mathcal{Q})$, left unspecified by its authors. We show
that requiring $\mathcal{F}$ to be single-valued — equivalently, that the longitudinal scalar
mode not be a gradient ghost — constrains its $\mathcal{Y}$-sector to an infinite-dimensional
class parameterised by a single saturation scale $s$, and that no member of that class is
observationally viable.

The requirement is that the induced anomalous acceleration $U(y)$ be a *monotone increasing*
function of the baryonic one. This is strictly stronger than the corresponding AQUAL
condition, because AeST's free function depends on the scalar's own gradient rather than on
the total potential's, and it immediately excludes the exponential interpolation
$\nu=1/(1-e^{-\sqrt y})$, whose $U$ turns over at $y=2.54$. Every legal member instead
*saturates*, at an anomalous acceleration $s\,a_0$, and $s$ is then fixed twice over by
observation. Planetary perihelion precession requires $s\le1.27\times10^{-5}$; the radial
acceleration relation requires $s\ge0.43$. **These are incompatible by a factor
$\sim1.2$–$3.4\times10^{4}$**, and every correction we have found widens the gap rather than
closing it.

The obstruction is structural rather than a matter of kernel choice: solar-system screening in
this theory is achieved precisely by the non-monotonicity that makes a kernel illegal. One may
have a ghost-free scalar or a screened solar system, not both. We state separately what this
does *not* touch — in particular the empirical normalisation $a_0=\kappa c\sqrt{G\rho_\Lambda}$,
which is independent of AeST — and we report a secondary result, that the RAR's flatness bounds
the theory's charge parameter at $\nu_0\le2.36\times10^{-6}$, nine times below the value
previously adopted.

---

## 1. Setup

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


---

## 2. The legality requirement

Reconstructing the free function from a chosen interpolation gives $J_Y(Y)=y(U)/U$ with
$Y=a_0^2U^2$, invertible **iff $U(y)$ is strictly increasing**. Equivalently, expanding $J$ to
second order about a nontrivial background gives kinetic matrix
$M_{ij}=J_Y\delta_{ij}+2J_{YY}u_iu_j$, whose longitudinal eigenvalue is positive under the same
condition. A non-monotone $U$ therefore means both a multi-valued $\mathcal{F}$ and a
longitudinal gradient ghost.

$$\boxed{\;U(y)\ \text{strictly increasing},\qquad U\to\sqrt y\ (y\to0),\qquad U/y\to0\ (y\to\infty).\;}$$

**Specific to AeST, not inherited from AQUAL.** In AQUAL the free function depends on the
gradient of the *total* potential and stability requires only $dg_{\rm obs}/dg_{\rm bar}>0$,
which the exponential kernel satisfies (minimum $0.968$). AeST's $\mathcal{F}$ depends on
$\mathcal{Y}$, built from the *scalar's* gradient — the stronger condition.

**It excludes the exponential interpolation.** Milgrom & Sanders (2008) Eq. (13) at
$\alpha=\tfrac12$ gives $U=y/(e^{\sqrt y}-1)$, rising to $0.6476$ at $y=2.540$ and then
falling. AeST cannot host it; likewise $\alpha=2$. This is not a statement about exponentials
as a class — $U=\tfrac12(1-e^{-2\sqrt y})$ is monotone and legal.

**The legal class is infinite-dimensional.** A one-parameter family spanning it, everything in
closed form,

$$J_Y(v)=\frac{v}{1-v/s},\qquad
J(Y)=-a_0^2\Big[\tfrac{v^2}{2}+sv+s^2\ln\!\big(1-\tfrac vs\big)\Big],\qquad v\equiv\frac{\sqrt Y}{a_0},$$

is legal for every $s>0$: $d(vJ_Y)/dv=sv(2s-v)/(s-v)^2>0$, longitudinal stiffness
$1+J_Y+2YJ_{YY}>1$, and deep-MOND limit $J\to\tfrac23Y^{3/2}/a_0$ — the form AeST's authors
print — **for every $s$**, so that limit carries no selective power. $s=\tfrac12$ is
$g_{\rm obs}^2=g_{\rm bar}^2+a_0g_{\rm bar}$; $s=1$ is the standard "simple" $\nu$.

Every member **saturates**, $U\to s$. That is forced by monotonicity plus $U/y\to0$, and it is
the crux of what follows.

---

## 3. The two constraints on $s$

### 3.1 Solar system

Saturation means a *constant* sunward anomalous acceleration $u_\infty=s\,a_0$ at every
planetary distance. By the Gauss planetary equations a constant radial perturbation gives a
secular apsidal advance $\dot\varpi=u_\infty\sqrt{1-e^2}/(na)$. At $s=\tfrac12$, against
anomalous-precession limits of EPM/INPOP class:

| planet | $\dot\varpi$ predicted (″/cy) | limit (″/cy) | ratio | after EFE (119–189×) |
|---|---|---|---|---|
| Mercury | 0.62 | $3\times10^{-3}$ | 208 | 1.1–1.7 |
| Earth | 1.02 | $1.9\times10^{-4}$ | 5 383 | 28–45 |
| Mars | 1.26 | $3.7\times10^{-5}$ | 33 978 | 180–286 |
| Saturn | 3.15 | $8\times10^{-5}$ | 39 424 | 209–331 |

This is substantially more constraining than the flat bound on a constant anomalous
acceleration usually quoted ($u_\infty/3.66\times10^{-14}=1279$).

**There is no external-field relief.** An earlier version divided by a committed EFE
reduction of 119–189×. That factor is an artefact. Deriving the external-field response *for
this family* rather than importing it — by two independent routes, an $\ell=1$ penetration ODE
and a flux bound needing no perturbation theory — gives a relief of **1.000000×** on the
*saturated* anomaly. The external field screens *itself*, not the anomaly: whatever it does,
somewhere on the 1 AU sphere the anomaly is at least $s\,a_0(1-4\times10^{-9})$. Since
$\dot\varpi\propto s$ and $u_\infty=s\,a_0$ is an absolute acceleration (so the ceiling scales
as $1/a_0$), the worst planet gives

$$s\le1.27\times10^{-5}\ \text{(canonical)},\qquad 1.05\times10^{-5}\ \text{(alt)}.

### 3.2 Galaxies

The RAR requires an anomaly $\approx0.4\,a_0$ at $y\sim2$. Applied to **this paper's own
family** $J_Y=v/(1-v/s)$ that gives $s\ge0.8/1.84=0.4348$. (An earlier version quoted
$s\ge0.558$, obtained from a *different* kernel; withdrawn.) Relaxing from a pointwise to a
global criterion — rms $\le0.15$ dex on 3389 SPARC points with $\Upsilon$ in the Spitzer band —
lowers it to $0.294$ canonical / $0.229$ alt at frozen $\Upsilon=0.70$, and to $0.157$ /
$0.126$ with per-galaxy $M/L$, the most generous defensible treatment. Refitting $\Upsilon$
itself buys only $1.34\times$. Fits to 175 SPARC galaxies at the anchored $a_0$ give 0.1083 dex at $s=\tfrac12$,
0.1009 at $s=1$, 0.0998 at $s=2$: the data mildly **prefer larger $s$**, moving away from the
solar-system requirement.

### 3.3 The incompatibility

$$\boxed{\;s\le1.27\times10^{-5}\ (\text{ephemerides})\qquad\text{versus}\qquad
s\ge0.435\ (\text{RAR}),\qquad\textbf{a factor }3.4\times10^{4}.\;}$$

On the most generous defensible reading of every fork at once — per-galaxy $M/L$ and the alt
footing — the gap is still $1.2\times10^{4}$. A non-spherical (disc) treatment of the local
law, which might have been expected to help, instead multiplies the floor by 1.07–1.10 and
widens it further.

No member of the legal class satisfies both. The obstruction is structural: legality forces
saturation, and the saturation scale is simultaneously the galactic MOND amplitude and the
solar-system anomaly. The one interpolation evading the solar-system constraint — the
exponential, whose $U$ *decays* — evades it precisely by being non-monotone, which is what
makes it illegal. **Within AeST one may have a ghost-free scalar or a screened solar system,
not both.**

---

## 4. Why a local $a_0$ does not rescue it

The $\mathcal{Q}$-sector can make $a_0$ environment-dependent:
$a_0^2(Q)=\kappa^2G(-K(Q))$ with $K$ an offset Dirac–Born–Infeld brane of tension
$M^4=\rho_\Lambda c^2$ — which yields $a_0=\kappa c\sqrt{G\rho_\Lambda}$, $w=-1$ exactly at the
minimum, and pressureless dust for small excitations — giving
$a_0(\nu)/a_0(0)=[(1+\nu_0^2)/(1+\nu^2)]^{1/4}$, $\nu=\nu_0\rho/\rho_0$. At solar-circle dark
density this suppresses the anomaly, weakening §3.1.

It does not help, because the same suppression must appear *across galaxies*. Requiring the
induced variation to stay inside the RAR's 0.108 dex over $\rho=0.01$–$1.5\ \mathrm{GeV\,cm^{-3}}$
bounds

$$\nu_0\le2.36\times10^{-6},$$

at which the solar-circle suppression is a few per cent, not the factor $\sim7$ needed. **The
RAR's flatness is simultaneously a measurement of $\nu_0$ and the reason local $a_0$ cannot
resolve §3.3.**

We report that bound independently, as it corrects a parameter: it lies a factor 9 below the
window $[2.14\times10^{-5},1.77\times10^{-4}]$ previously adopted from an $a_0(z)$ off-switch
at recombination. That off-switch is not the binding requirement — a CLASS computation of the
metric potential at $z=1089.9$ over $k=0.01$–$3\ \mathrm{Mpc^{-1}}$ gives
$g\ge1.22\times10^{-10}\ \mathrm{m\,s^{-2}}$, already exceeding $a_0$, so $y>1$ at recombination
*with no suppression at all*. At the RAR ceiling, $a_0(z_{\rm rec})/a_0=0.018$ and $y\ge72$.

---

## 5. What this does and does not affect

**Not affected.** The empirical normalisation
$a_0=\kappa c\sqrt{G\rho_\Lambda}=c^2\sqrt{\Lambda/32\pi}$ is independent of AeST. $\kappa$ is
fitted, not derived: $0.551\pm0.043$ (distance-free), $0.465\pm0.076$ (BTFR),
$0.537\pm0.071$ (gas-dominated, TRGB), combining to $0.529\pm0.034$, and it must be quoted with
its $H_0$ — the distance-free value carries an unpriced $\sim7\%$ systematic. Also unaffected:
the RAR at 0.108 dex, weak lensing 40 kpc–2.2 Mpc with no dark component, the BTFR, and — within
AeST — $\gamma_{\rm PPN}=1$, $c_T=1$ exactly, and the CMB fit.

**Affected.** AeST as a relativistic completion for MOND phenomenology, in its ghost-free sector.

**Caveats, stated rather than buried.** The local algebraic law of §1 is exact in spherical
symmetry; discs are not. We solved the non-spherical problem rather than estimating it, and it
runs the wrong way: a Miyamoto–Nagai disc gives $u_{\rm disc}/u_{\rm alg}=0.67$ at 3 kpc,
$0.92$ at 8 kpc and $0.98$ at 20 kpc, so the required floor rises by 1.07–1.10 and the gap
widens. The anomalous-precession limits are order-of-magnitude EPM/INPOP-class values rather
than a refit with this signal in the model — that refit remains the one measurement that could
soften §3.1, and it would have to soften it by four orders of magnitude.

We also record what does **not** work, since each was tried. **A local $a_0$ hurts rather than
helps**: with a suppression factor $f$, the ephemeris-constrained product is $s\,f$, and
solving $f\,U_s(2/f)=0.4$ gives $s\,f=0.435$ at $f=1$ but $2.00$ at $f=0.1$ — unsatisfiable
below $f=0.080$, because $U\le\sqrt y$ caps the family. **Refitting $\Upsilon$** buys $1.34\times$,
not the $2.5\times$ a naive comparison suggests, because the larger figure silently swaps a
pointwise criterion for a global one. **The external-field effect** contributes nothing at all
(above).

**What a viable completion must supply.** A screening mechanism that is *not* a non-monotone
interpolation. That is a sharper target than "a relativistic MOND theory," and it is the
constructive content of this negative result.

---

**Reproducibility.** Every number is produced by a committed script at
<https://github.com/carlzimmerman/zimmerman-formula>:
`nbody_2026/stage75_the_closed_theory_2026.py`,
`nbody_2026/stage76_nu0_recombination_pin_2026.py` (the $\nu_0$ bound, with CLASS),
`real_research/reviews/typeII_*_2026.py` (the quasi-static reduction, the legality analysis and
the legal family), `real_research/reviews/a0_local_ephemeris_2026.py`, and
`real_research/rar_framework_a0_mlfit.py`. Withdrawn claims are recorded, dated, in
`RETRACTIONS.md`.

**Attribution.** AeST: Skordis & Złośnik, *Phys. Rev. Lett.* **127**, 161302 (2021),
arXiv:2007.00082, and arXiv:2109.13287. Interpolation family: Milgrom & Sanders, *ApJ*
**678**, 131 (2008). PPN aether results: Foster & Jacobson, *Phys. Rev. D* **73**, 064015
(2006). Ephemeris bound: Sereno & Jetzer (2006). The $a_0$–$\Lambda$ coincidence has prior
art in Milgrom (1999), Blanchet & Le Tiec (2009), Pikhitsa (2010) and Klinkhamer & Kopp (2011).
