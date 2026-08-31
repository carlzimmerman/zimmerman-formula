# The Crispy Fried Chicken Theory of Gravity

**A modified-gravity account of the mass–discrepancy–acceleration relation with a horizon-set acceleration scale, and the no-go landscape of its relativistic completion**

Carl P. Zimmerman · Briar Creek Tech, Charlotte, NC, USA · carl@briarcreektech.com

**Version 2.0.0** · 2026-08-30 · License CC-BY-4.0

> **Honest status, stated once and up front.** This paper documents a *candidate* programme, not a finished theory of gravity. Two things in it are solid and reproducible: (i) the non-relativistic phenomenology — an exact exponential interpolation function, the radial-acceleration relation, and the baryonic Tully–Fisher relation, all organised by a single acceleration scale $a_0$; and (ii) a systematic **no-go landscape** for the relativistic completion, in which every reduced-degree-of-freedom single-metric realisation is closed by an explicit obstruction, and the viable completion is forced into the aether-scalar-tensor (AeST) class. What is **not** established, and is labelled as such throughout, is a finished, fully covariant, ghost-free, observationally complete relativistic field theory. The coefficient $\kappa=\tfrac12$ in $a_0=\kappa c\sqrt{G\rho_\Lambda}$ is **fitted, not derived**. The one distinctive, still-standing prediction is $a_0\propto H(z)$.

---

## Abstract

The mass–discrepancy–acceleration relation (MDAR) of galaxies is reproduced with zero fitted shape
parameters by a single acceleration scale $a_0 = 9.36\times10^{-11}\,\mathrm{m\,s^{-2}}$ and the exact
interpolation function $\mu(y) = 1-e^{-y}$, $y = g/a_0$. We take $a_0$ to be set by the horizon /
dark-energy scale, $a_0 = \kappa c\sqrt{G\rho_\Lambda}$ with $\kappa=\tfrac12$; we stress that $\kappa$
is an empirical normalisation, not a derived number. On the Spitzer Photometry and Accurate Rotation
Curves (SPARC) sample the framework reproduces the radial-acceleration relation with $0.108$ dex of
orthogonal scatter at a single stellar mass-to-light ratio, and yields the baryonic Tully–Fisher
relation $v^4 = GMa_0$ analytically. The scale's tie to $\rho_\Lambda$ makes $a_0\propto H(z)$ the
programme's distinctive, falsifiable prediction.

The bulk of this paper concerns the **relativistic completion**: the requirement that the same theory
also bend light correctly, i.e. produce $\Phi=\Psi$ (no gravitational slip) with the MOND-enhanced
source, while propagating a healthy spectrum and respecting Solar-System, gravitational-wave, and
binary-pulsar bounds. We report a systematic result. A single physical metric can carry the MOND
response in exactly two ways — through a *propagating* field or through an *elliptic constraint* — and
both are closed: the propagating branch reintroduces a scalar mode and cannot bend light off the
diffeomorphism-locked ray (slip-lock), while the elliptic-constraint branch is excluded by the
preferred-frame post-Newtonian parameter $\alpha_3 = O(1)$. The two-metric (bimetric) exit is closed
independently: the ghost-free potential sector cannot produce the MOND $1/r$ force, and the
derivative-interaction sector that can, carries a vector-sector Ostrogradsky ghost. The surviving
completion is therefore forced to contain a **preferred-frame vector** — an aether — which places it in
the AeST class of Skordis & Złośnik. We give the honest consequence: a genuinely dark-matter-free
single-metric completion is closed, whereas a viable AeST-class completion exists but carries a dark
*field* (no dark-matter *particle*, but not "dark-matter-free"), and leaves open the finite-wavelength
cosmological dispersion and the preferred-frame parameter $\alpha_2$. We collect these results, the
explicit obstruction certificates, and the remaining open calculations as a research programme.

---

## 1. Introduction

### 1.1 The empirical regularity

Rotationally supported galaxies obey a tight relation between the total (dynamical) centripetal
acceleration $g$ inferred from their rotation curves and the Newtonian acceleration $g_N$ computed from
their *baryonic* mass alone. Below a characteristic scale
$$
a_0 \simeq 1.2\times10^{-10}\,\mathrm{m\,s^{-2}},
$$
the observed acceleration systematically exceeds the baryonic one; above it, the two coincide. This is
the mass–discrepancy–acceleration relation, or in its modern high-precision form the
radial-acceleration relation (RAR). Its scatter is small — of order $0.1$ dex, much of which is
observational — and it holds across galaxies spanning five decades in mass and a wide range of
morphologies. Any successful theory of galactic dynamics must reproduce it.

Two broad interpretations exist. In the particle dark-matter picture the relation is an emergent,
approximate consequence of galaxy-formation physics acting on collisionless halos. In the modified
dynamics picture, initiated by Milgrom, the relation is *fundamental*: it reflects a modification of
gravity or inertia that switches on below $a_0$. This paper works within the second interpretation, and
in particular within its **modified-gravity** arm.

### 1.2 What this paper adds

Three claims are made, in decreasing order of certainty.

1. **A specific closed-form theory of the MDAR.** We adopt the exact interpolation
   $\mu(y)=1-e^{-y}$ and the horizon-tied scale $a_0=\kappa c\sqrt{G\rho_\Lambda}$. Section 2 collects
   the non-relativistic consequences and the SPARC comparison. This part is solid.

2. **A systematic no-go map for the relativistic completion.** Section 5 through Section 7 present a set
   of explicit obstructions — each backed by a symbolic computation — showing that the single-metric and
   two-metric reduced-degree-of-freedom realisations are closed. Section 8 states the resulting
   structural theorem: the viable completion must contain a preferred-frame vector. This is the main new
   content.

3. **An honest identification of the surviving candidate and its price.** Section 9 identifies the
   surviving completion as the AeST class, states what it buys (correct lensing, $c_T=c$, a cosmology)
   and what it costs (a dark field, hence "no dark-matter particle" rather than "dark-matter-free," plus
   open preferred-frame and finite-wavelength gates).

The reader who wants only the physics that is presently *established* should read Sections 2, 5–8, and
the scorecard in Section 12, and treat everything about a finished action as a programme.

### 1.3 Notation and conventions

We use the mostly-plus signature $(-,+,+,+)$, units in which factors of $c$ are shown explicitly, and
$G$ for Newton's constant. Greek indices run over spacetime, Latin over space. $R^{(3)}$ is the Ricci
scalar of the spatial metric $\gamma_{ij}$, $D_i$ its covariant derivative, and $\nabla^2$ the flat-space
Laplacian in the weak field. A prime on an interpolation function denotes $d/dy$. In the weak field we
write the metric in the conformal Newtonian gauge
$$
ds^2 = -\left(1+\frac{2\Phi}{c^2}\right)c^2 dt^2 + \left(1-\frac{2\Psi}{c^2}\right)\delta_{ij}dx^i dx^j,
$$
so that $\Phi$ governs the motion of slow test particles and $\tfrac12(\Phi+\Psi)$ governs the deflection
of light. Equality $\Phi=\Psi$ ("no slip") is the condition for the theory to lens like general
relativity for a given mass distribution.

---

## 2. The non-relativistic theory

### 2.1 The acceleration scale

We take the fundamental acceleration scale to be set by the dark-energy density,
$$
\boxed{\,a_0 = \kappa\, c\sqrt{G\rho_\Lambda}\,}, \qquad \kappa = \tfrac12,
$$
which, with $\rho_\Lambda$ from the measured cosmological constant, evaluates to
$$
a_0 = 9.36\times10^{-11}\,\mathrm{m\,s^{-2}}.
$$
Equivalently $a_0 = cH_\Lambda/Z$ with $H_\Lambda=\sqrt{\Lambda/3}\,c$ the de Sitter rate and $Z\simeq21$
a numerical factor; the two forms are identical, $\kappa=\tfrac12 \Leftrightarrow Z = 2\sqrt{8\pi/3}$.

**Honest labelling.** Neither $\kappa=\tfrac12$ nor $Z\simeq21$ is derived from a deeper principle in this
work. They are fixed empirically. The *content* of the relation is the scaling $a_0\propto\sqrt{\rho_\Lambda}$,
i.e. the tie between the galactic scale and the cosmological one; the coefficient is an input. We flag
this because an earlier phase of the programme over-claimed a derivation of $\kappa$, which was publicly
retracted. The surviving, distinctive statement is the *proportionality*, from which follows the
programme's sharpest prediction:
$$
\boxed{\,a_0(z)\propto \sqrt{\rho_\Lambda(z)}\,\Longrightarrow\, a_0\propto H(z)\ \text{if }\rho_\Lambda\ \text{traces the expansion rate}\,},
$$
a redshift dependence absent from standard cold dark matter, in which any emergent acceleration scale
inherits halo properties and scales differently. This is the empirical crux of the whole programme.

### 2.2 The interpolation function

We adopt the exact exponential interpolation
$$
\boxed{\,\mu(y) = 1 - e^{-y}\,}, \qquad y = \frac{g}{a_0},
$$
relating the true acceleration $g$ to the baryonic one through $g_N = \mu(g/a_0)\,g$, or in AQUAL
(aquadratic-Lagrangian) form
$$
\nabla\cdot\!\big[\mu(|\nabla\Phi|/a_0)\,\nabla\Phi\big] = 4\pi G\rho_b .
$$
The limits are the two MOND axioms:
$$
\mu(y)\to 1\quad(y\gg1)\ \Rightarrow\ \text{Newtonian}, \qquad
\mu(y)\to y\quad(y\ll1)\ \Rightarrow\ g^2 = a_0 g_N .
$$
The complementary "$\nu$" form used in the QUMOND/algebraic presentation,
$$
\nu(y) = \frac{1}{1-e^{-\sqrt{y}}},
$$
is Milgrom & Sanders' one-parameter family (2008, ApJ 678, 131, Eq. 13) evaluated at exponent
$\alpha=\tfrac12$; we credit that work for the functional form. The exponential family is favoured over
the "simple" and "standard" families because it approaches the Newtonian limit exponentially fast,
which is what allows the Solar-System residuals to be astronomically small (Section 10).

### 2.3 The MDAR, RAR, and BTFR

With $\mu(y)=1-e^{-y}$ the deep-MOND limit of an isolated spherical source of baryonic mass $M$ is
$$
\mu(g/a_0)\,g = g_N = \frac{GM}{r^2}\ \xrightarrow{y\ll1}\ \frac{g^2}{a_0} = \frac{GM}{r^2},
$$
so
$$
\boxed{\,g = \frac{\sqrt{GMa_0}}{r}\,},\qquad
\boxed{\,v^4 = GMa_0\,}.
$$
The second is the baryonic Tully–Fisher relation (BTFR): a mass–velocity power law with slope exactly 4
and a normalisation fixed by $a_0$ alone, with no free parameter. On the SPARC sample the framework's
RAR is reproduced with an orthogonal scatter of
$$
\sigma_\perp = 0.108\ \text{dex}
$$
at a single, physically reasonable stellar mass-to-light ratio $\Upsilon_\star = 0.70\,M_\odot/L_\odot$
in the $[3.6]$ band. We emphasise a methodological point established in the accompanying scripts: this
scatter is *convention-compatible* with, and non-diagnostic of, the specific value $9.36\times10^{-11}$;
anchoring $a_0$ to the horizon value rather than fitting it is *cheaper* (one fewer parameter), not a
better fit. We do not claim the horizon $a_0$ "fits the RAR better" than a fitted $a_0$.

### 2.4 Operative arm

Historically the programme explored both a *modified-inertia* arm (the low-acceleration modification
lives in the matter action / dispersion relation) and a *modified-gravity* arm (it lives in the
gravitational field equations). The modified-inertia arm is closed for this framework by lensing: a pure
modified-inertia stress cannot supply the light-bending enhancement the data require (the "$\nu^2$ gap,"
Section 7). The operative arm of this paper is therefore **modified gravity**. This is stated because
the relativistic no-go landscape below is specific to the modified-gravity arm.

---

## 3. The exponential constitutive function

The exponential interpolation admits an exact potential ("constitutive") representation that is used
throughout the relativistic constructions. Define
$$
\boxed{\,G(y) = y^2 + 2(1+y)e^{-y} - 2\,}.
$$
Then
$$
G'(y) = 2y - 2y e^{-y} = 2y\big(1-e^{-y}\big) = 2y\,\mu(y),
$$
so that
$$
\frac{G'(y)}{2y} = \mu(y) = 1-e^{-y}.
$$
Equivalently, in a covariant kinetic variable $Z$ with $y=\tfrac12\sqrt{Z}$ one has
$$
F(Z) = 4\Big[\,1-\big(1+\tfrac12\sqrt{Z}\big)e^{-\sqrt{Z}/2}\Big],\qquad
\boxed{\,F'(Z) = \tfrac12 e^{-\sqrt{Z}/2}\,}.
$$
These identities are exact and are verified symbolically (Appendix A). They are the reason the same
exponential MOND law can be attached to several different relativistic scaffolds without approximation:
one only needs a scalar whose kinetic invariant plays the role of $Z$ or $y^2$, and the constitutive
function $G$ (or $F$) reproduces $\mu=1-e^{-y}$ identically.

A small-argument expansion that matters for effective-field-theory estimates is
$$
F(Z) = \frac{Z}{2} - \frac{Z^{3/2}}{6} + \frac{Z^2}{32} + \cdots,
$$
i.e. the leading correction to the quadratic kinetic term is a **non-analytic** $Z^{3/2}$ piece, not a
quartic $Z^2$. Any strong-coupling or cutoff estimate must diagonalise the quadratic sector first and
respect this non-analyticity; a naive quartic-interaction estimate is wrong.

---

## 4. The relativistic completion problem

### 4.1 What "completion" requires

A relativistic completion of the above must simultaneously satisfy a demanding list:

- **(K) Kernel.** Reproduce $\mu(y)=1-e^{-y}$ and hence the RAR/BTFR in the quasi-static weak field.
- **(L) Lensing.** Produce $\Phi=\Psi$ (equivalently $\gamma_{\rm PPN}=1$) with the MOND-enhanced source,
  so that photons and slow matter feel the same enhanced potential:
  $g_{\rm lens}=g_{\rm dyn}=\nu(y)\,g_N$, where $\nu=1/\mu$ is the enhancement.
- **(T) Tensor sector.** Two luminal gravitational-wave polarisations, $c_T=c$ to the
  $|c_T/c-1|\lesssim10^{-15}$ precision of GW170817/GRB170817A.
- **(H) Health.** No ghost, no gradient or tachyonic instability in the physical spectrum.
- **(P) Post-Newtonian.** Solar-System bounds: $|\gamma_{\rm PPN}-1|\lesssim2\times10^{-5}$ (Cassini),
  and preferred-frame bounds $|\alpha_1|\lesssim10^{-4}$, $|\alpha_2|\lesssim10^{-7}$,
  $|\alpha_3|\lesssim4\times10^{-20}$ (binary pulsars).
- **(C) Cosmology.** An acceptable homogeneous background and finite-wavelength perturbation spectrum;
  ideally the CMB and matter power spectrum.

The single hardest tension is between (K) and (L): a modification strong enough to enhance dynamics by
$\nu$ must enhance lensing by the *same* $\nu$, with no gravitational slip.

### 4.2 The slip obstruction in one line

For a single metric with ordinary (diffeomorphism-invariant) dynamics, the linearised Ricci scalar is
$$
R^{(1)} = -2\nabla^2\Phi + 4\nabla^2\Psi ,
$$
so diffeomorphism invariance ties any frame-free scalar's imprint on $(\Phi,\Psi)$ to the ray
$(1,-2)$ in the $(\delta R)$ direction. A frame-free scalar therefore produces a fixed **slip**
$$
\eta \equiv \frac{\Psi}{\Phi} = \frac{4L+m}{8L+m}\neq 1
$$
for any non-trivial coupling $L>0$ (with $m$ a mass term); one recovers $\eta=\tfrac12$ (the $f(R)$
value) as $m\to0$ and $\eta=1$ (general relativity) only as $L\to0$. This is the **slip-lock**: a
frame-free single-metric scalar cannot bend light like its dynamics. It is the linchpin of the no-go
landscape and it recurs, in different disguises, in every branch below. We label it **DC-013**.

---

## 5. The single-metric landscape

A single physical metric can carry the low-acceleration modification in exactly one of two ways: through
a field that *propagates* (has its own initial-data / Cauchy degrees of freedom), or through a *constraint*
(instantaneous, elliptic, no independent Cauchy data). We treat each.

### 5.1 The propagating branch and its residue

If the MOND response is a propagating scalar $\varphi$ (as in a relativistic AQUAL / $k$-essence, or in a
causal non-local construction where $\Phi=\Box_{\rm ret}^{-1}J$ is localised), two obstructions fire.
First, **DC-013** (slip-lock) applies directly if $\varphi$ is frame-free: the scalar cannot produce
$\Phi=\Psi$. Second, in the specific causal non-local construction, localising the retarded inverse
$\Box_{\rm ret}^{-1}$ introduces a genuine extra propagating scalar mode with dispersion
$$
\boxed{\,\omega^2 = \tfrac12 c^2 k^2\,}
$$
(sub-luminal group speed $c/\sqrt2$, non-tachyonic; the residue sign, i.e. ghost-or-healthy, is a
separate question). The linear spectrum of that construction is therefore **2 tensors + 1 scalar = 3
degrees of freedom**, not 2. This is not a defect that nonlinear terms remove; it is the physical content
of a retarded curvature response. Moreover, a retarded operator is not the Euler–Lagrange derivative of
an ordinary single-copy action ($G_{\rm ret}(x,y)\neq G_{\rm ret}(y,x)$; the transpose is advanced), so
such a construction is a causal *equation ansatz* rather than an action-based field theory unless
formulated in a doubled in-in (Schwinger–Keldysh) framework — and that framework reveals, rather than
removes, the extra mode: the retarded kernel is either genuinely dissipative (an open system with an
integrated-out sector) or the propagator of a local field (the extra scalar). Either way the "single
metric, no extra field, two degrees of freedom" reading is not available on the propagating branch.

### 5.2 The constraint branch and $\alpha_3$

If the MOND response is instead an **elliptic constraint** — the constraint-first "minimal modified
gravity" (MMG) family — the slip can be *repaired*. One writes the log-lapse $\phi=\ln N$, the spatial
volume scalar $q=\tfrac16\ln\det\gamma$, and takes the MOND constraint on a scalar combination together
with a second-class partner. A well-chosen partner makes the space-space (slip) sector give $\Phi=\Psi$,
hence $\gamma_{\rm PPN}=1$. Explicit realisations include (i) the rotated pair $u=\phi-q$ (MOND carrier)
with the auxiliary $D^2r=0$, $r=\phi+q$ (slip removal); and (ii) the curvature-locked variant with the
covariant lock $D^2\phi=\tfrac14R^{(3)}$, equivalently $N=\exp[\tfrac14 D^{-2}R^{(3)}]$. All of these
share a $4\times4$ scalar Dirac block that is generically rank-4 (two gravitational degrees of freedom),
a strictly elliptic MOND operator ($\lambda_\perp=\mu>0$, $\lambda_\parallel=\mu+y\mu'>0$ for $y>0$), and
a luminal tensor sector.

They also share a fatal weak-field structure. On the $\Phi=\Psi$ branch all of them reduce to
$$
N = e^{\Psi/c^2},\qquad g_{00} = -\,c^2 e^{2\Psi/c^2},
$$
with $\Psi$ solving the *instantaneous* elliptic MOND equation. This is the same $g_{00}$ sector across
the whole family (the curvature-lock $N=\exp[\tfrac14D^{-2}R^{(3)}]$ reduces, using
$R^{(3)}=(4/c^2)\nabla^2\Psi$, to exactly $N=e^{\Psi/c^2}$). Because the lapse responds *instantaneously*
to the source — including to its kinetic energy $T_{00}\sim\rho v^2$ — with coefficient $1$ rather than
general relativity's retardation-consistent coefficient $4$, the post-Newtonian expansion gives
$$
\gamma_{\rm PPN}=1,\quad \beta_{\rm PPN}=1,\quad \alpha_1=0,\quad \alpha_2=0,\quad
\boxed{\,\alpha_3 = -3\,}.
$$
(In the un-repaired $D^2q=0$ chassis one finds instead $\gamma_{\rm PPN}=0$, $\alpha_1=4$,
$\alpha_3=-1$, excluded by Cassini at $>4\times10^4\sigma$; repairing the slip fixes $\gamma$ and
$\alpha_1$ but drives $\alpha_3$ to $-3$.) The binary-pulsar bound is $|\alpha_3|\lesssim4\times10^{-20}$;
$\alpha_3=-3$ violates it by $\sim7.5\times10^{19}$. Physically, $\alpha_3\neq0$ is momentum
non-conservation — self-accelerating binaries — and it is *structural* to an instantaneous elliptic
constraint. A spatial-sector lock (any choice of the slip-removal partner) fixes the space-space sector
but cannot reach the time-sector coefficient that sets $\alpha_3$. We label this **DC-019**.

The two branches are exhaustive and mutually exclusive: $\alpha_3=0$ requires a retarded (hyperbolic)
response, which is a propagating field, which is the branch of Section 5.1. Hence:

> **Single-metric pincer.** No single physical metric produces MOND dynamics *and* $\Phi=\Psi$ lensing
> *and* exactly two propagating degrees of freedom *and* $\alpha_3=0$. The propagating branch carries an
> extra scalar and (frame-free) the slip; the elliptic-constraint branch carries $\alpha_3=O(1)$.

---

## 6. The two-metric landscape

The natural escape from the single-metric pincer is a second spin-2 field, which can source the
space-space potential $\Psi$ at linear order and so, in principle, decouple lensing from dynamics. We
examined the ghost-free bimetric (Hassan–Rosen) class and its extensions.

### 6.1 Non-derivative interactions cannot produce MOND $1/r$

The ghost-free bimetric potential is algebraic in the matrix square root $\sqrt{g^{-1}f}$, and its
helicity-0 sector reorganises into the finite Galileon tower. For a static spherical source the
$n$-th Galileon term gives an exterior field $\pi' \propto r^{\,1-3/n}$, so the integer orders
$n\in\{1,2,3,4\}$ give
$$
\pi' \propto \{\,r^{-2},\ r^{-1/2},\ r^{0},\ r^{1/4}\,\},
$$
and the MOND requirement $\pi'\propto r^{-1}$ needs $n=3/2$, which is **not** an integer Galileon
operator. The linear branch is a Yukawa (fixed length scale, anti-MOND). Hence the standard ghost-free
bimetric potential sector cannot produce the MOND $1/r$ vacuum force. We label this **DC-018**. (An
earlier "nonlinear helicity-0 rescue," $r^2(\pi')^2\sim GM\Rightarrow\pi'\sim1/r$, was in error — the
correct spherical balance is $r(\pi')^2/\Lambda_3^3\sim GM\Rightarrow\pi'\sim r^{-1/2}$ — and is
retracted here.)

### 6.2 Derivative interactions produce MOND but carry a vector ghost

A *derivative* (connection-difference) interaction, built from $C^\lambda{}_{\mu\nu}=\Gamma^\lambda{}_{\mu\nu}(g)-\Gamma^\lambda{}_{\mu\nu}(\hat g)$,
*can* produce the MOND $1/r$: a non-analytic $X^{3/2}$-type relative kinetic operator gives, in vacuum,
$r^2(\phi')^2\sim GM\Rightarrow\phi'\sim\sqrt{GM}/r$, and is ghost-free as an isolated scalar
($c_s^2=\tfrac12$). Working with the five independent quadratic invariants of $C$, there is a
two-parameter "ghost-free tuned" subspace (lapse-velocity-free, $\sum c_i=0$) that contains
MOND-producing directions off the constrained-$f(Q)$ line. On that subspace the helicity-0 (Boulware–Deser)
ghost is *absent* (the Stückelberg $\pi$ is non-dynamical) and the tensor speed is exactly $c_T=c$; and,
notably, $\alpha_3=0$ — the one thing the genuinely-bimetric route gets right.

However, the **vector (helicity-1) sector carries a higher-derivative Ostrogradsky ghost**. The
Stückelberg transverse operator is $-\lambda(2u_0+u_1)(\omega^2-\kappa^2)^2/2$ — a $\Box^2$
(four-derivative) double pole — and the physical time-kinetic matrix has signature $(-,+)$
($\det = -9$), one wrong-sign mode. Crucially the MOND acceleration coefficient is $a=-2(2u_0+u_1)$, so
$a\neq0\Leftrightarrow(2u_0+u_1)\neq0\Leftrightarrow$ the $\Box^2$ vector operator is present:
**MOND-aliveness forces the vector ghost**, across the entire tuned subspace, sign-independently, with
the control cases (pure Einstein–Hilbert, Fierz–Pauli mass) coming out clean. The root cause is that the
MOND-producing interaction is intrinsically two-derivative ($C^2$), so breaking the relative
diffeomorphism to obtain $a\neq0$ necessarily deposits a $\Box^2$ ghost in the vector sector; Fierz–Pauli
evades this only because its mass term is zero-derivative. We label this **DC-020**. The escape route —
enlarging to the four-parameter $\sum c_i=0$ space with lapse-velocity terms restored — reintroduces
preferred-frame (khronometric) terms and collapses to the AeST/khronometric family already discussed.

### 6.3 The phantom-density and optical-metric constructions

Two further single-metric ideas are worth recording because they converge on the same conclusion.

**Phantom density.** Adding a gravitating density that tracks the enhancement, $\rho_{\rm ph}=(\nu-1)\rho_b$,
so that the Einstein source becomes $\nu\rho_b$, appears to give lensing without slip. But a single-metric
sector whose gravitating density $f(y)$ depends on the local acceleration $y=|\nabla\Phi|/a_0$ has a
traceless (anisotropic) stress $T_{xx}-T_{yy} = -y\,f'(y)$ (Appendix B). For the RAR-tracking choice
$f=(\nu-1)\rho_b$ one has $f'=\rho_b\,\nu'\neq0$ throughout the MOND transition, so the anisotropic stress
is non-zero and $\Phi\neq\Psi$: this is DC-013 in density costume. The only way to kill the anisotropy is
$f'=0$, i.e. $\nu=$ const, i.e. no MOND. A genuinely independent dust field ($f$ independent of $y$) has
$\Phi=\Psi$ but is not tied to $(\nu-1)\rho_b$ — it is simply dark matter, with no RAR correlation.
Tying free dust to the correlation *dynamically* is precisely AeST's pressureless-scalar sector.

**Optical / disformal metric.** Letting matter and light see a disformally modified metric
$\tilde g_{\mu\nu} = g_{\mu\nu} - 2F(\chi)\,(g_{\mu\nu}+2u_\mu u_\nu)$ with $\chi$ elliptic shifts both
potentials *equally*, $\tilde\Phi=\Phi+\chi$, $\tilde\Psi=\Psi+\chi$, so $\tilde\Phi-\tilde\Psi=\Phi-\Psi$
and general relativity's $\Phi=\Psi$ is inherited: the mechanism *works*. But the object
$E_{\mu\nu}=g_{\mu\nu}+2u_\mu u_\nu$ requires a preferred-frame normal $u_\mu$ — an aether. The
optical-metric construction is therefore the AeST disformal mechanism, and its covariant completion
carries the aether's degrees of freedom.

---

## 7. The modified-inertia obstruction

For completeness we record why the modified-inertia arm is closed for lensing. A passive
low-acceleration kernel that reproduces the dynamics produces a *gravitating* source of order
$\rho_b/\nu$, whereas the observed lensing RAR requires an effective source of order $\nu\rho_b$; the two
differ by a factor $\nu^2$. A passive kernel that both sets the scale $a_0$ *and* supplies the
$\nu\rho_b$ lensing enhancement does not exist within the assumptions of the audit. The resolution is to
separate the two jobs, which is exactly what the modified-gravity completions do.

---

## 8. The structural theorem

Collecting Sections 5 and 6:

> **Completion theorem (as far as established).** Within the classes examined, the relativistic
> completion of the exponential-MOND framework cannot be a reduced-degree-of-freedom single- or
> two-metric theory. The single metric is a closed pincer (DC-013 slip-lock and the propagating extra
> scalar; DC-019 preferred-frame $\alpha_3$). The two-metric exit is closed for non-derivative
> interactions (DC-018) and, on its MOND-producing derivative subspace, by a vector Ostrogradsky ghost
> (DC-020). The one object that legally carries the MOND lensing enhancement — that sources the
> space-space potential off the diffeomorphism-locked $(1,-2)$ ray — is a **preferred-frame vector**.

The theorem is constructive: it tells us the completion must contain an aether (a dynamical or
constrained timelike vector field defining a preferred frame). That places it in the aether-scalar-tensor
(AeST) class of Skordis & Złośnik (2021). The remainder of the paper takes that identification seriously.

Two caveats keep this honest. First, "as far as established" means within the specific classes and at
the order (typically linear around Minkowski, or minisuperspace for the constraint counts) at which the
obstructions were computed; each is backed by a symbolic certificate (Appendix B) but none is a fully
nonlinear all-orders theorem. Second, the derivative-bimetric escape into the four-parameter space with
restored lapse-velocity terms was not exhaustively swept; the argument that it collapses to the
khronometric/AeST family is strong but not a closed proof.

---

## 9. The surviving completion: AeST class

### 9.1 The action

The aether-scalar-tensor theory couples the physical metric $g_{\mu\nu}$ to a unit-timelike vector
$A^\mu$ ($A^\mu A_\mu=-1$, enforced by a Lagrange multiplier $\lambda$) and a scalar $\varphi$, through
invariants
$$
Q = A^\mu\nabla_\mu\varphi,\qquad
Y = (g^{\mu\nu}+A^\mu A^\nu)\nabla_\mu\varphi\,\nabla_\nu\varphi,
$$
with a free function $\mathcal F(Y,Q)$. The exponential MOND kernel is realised by
$$
\mathcal J(Y,Q) = a_0^2(Q)\Big[u^2 + 2(1+u)e^{-u} - 2\Big],\qquad u = \frac{\sqrt{Y}}{a_0(Q)},
$$
so that $\mathcal J_Y = 1-e^{-u}$, reproducing $\mu(y)=1-e^{-y}$ exactly (Section 3). A representative
action is
$$
S = \frac{c^3}{16\pi G_*}\!\int\! d^4x\,\sqrt{-g}\Big[
R - 2\Lambda - \tfrac{K_B}{2}F_{\mu\nu}F^{\mu\nu}
+ 2(2-K_B)J^\mu\nabla_\mu\varphi - (2-K_B)Y - \mathcal F(Y,Q) - \lambda(A^2+1)\Big] + S_m[g,\psi_b],
$$
with $F_{\mu\nu}=\partial_\mu A_\nu-\partial_\nu A_\mu$ and $\mathcal F=(2-K_B)\mathcal J - 2\mathcal K(Q)$.

### 9.2 What it buys

The AeST class delivers what the reduced-degree-of-freedom completions could not:

- **Lensing.** The aether sources the space-space potential off the $(1,-2)$ ray; a quasi-static
  analysis gives $\Phi=\Psi$ and $\gamma_{\rm PPN}=1$. Embedding the exponential kernel and calibrating
  against weak-lensing data brings the framework's lensing discrepancy from a naive $\sim21\sigma$ tension
  (in the modified-inertia arm) down to $\lesssim1\sigma$; a direct comparison to KiDS-based
  galaxy–galaxy lensing gives $\chi^2/\mathrm{dof}\approx0.64$ for the enhanced-source model.
- **Tensor sector.** $c_T=c$ exactly, satisfying GW170817.
- **Degrees of freedom.** The Hamiltonian analysis (Skordis & Złośnik 2023, arXiv:2307.15126) gives
  $4$ first-class $+\,4$ second-class constraints and $N_{\rm grav}=6$ physical degrees of freedom — a
  *healthy* count, not a pathology.
- **Background cosmology.** On the homogeneous background $Y=0$, $Q=\dot\varphi$, and the $Q$-sector
  charge redshifts as $\mathcal K_Q\propto a^{-3}$, i.e. it supplies a pressureless (dust-like)
  homogeneous component; the $k\to0$ de Sitter mode is Hubble-diluted ($\chi\sim e^{-3Ht}$), not a secular
  runaway.

### 9.3 What it costs — stated plainly

The AeST completion is **not dark-matter-free**. Its pressureless scalar sector *is* the CMB's dark
matter; within the completion, dark matter exists at the full $\Omega_{\rm dm}$, because only a
$w=0$ component redshifts as $\rho\propto a^{-3}$ and fits the acoustic peaks. The honest slogan is
therefore **"no dark-matter particle"** — the carrier is a field, not a weakly interacting massive
particle — and *not* "dark-matter-free." This is the sharp dichotomy of the whole programme: a genuinely
dark-matter-free (single-metric) completion is closed by Section 5–6; a viable completion carries a dark
field. There is no third option within the classes examined.

### 9.4 What is open

For the *specific* exponential $\mathcal F(Y,Q)$ (as opposed to generic AeST), the following are not yet
computed and must not be inherited from generic results:

- the finite-wavelength cosmological dispersion in the band $H\ll k<k_\star$ (only $k\to0$ is settled);
- the preferred-frame parameter $\alpha_2$ (the $\alpha_2=0$ result quoted elsewhere belongs to a
  different, two-degree-of-freedom construction and must not be transferred);
- the characteristic speed / causality condition, schematically $c_s^2\sim1/K_B$, requiring $K_B\ge1$ for
  the scalar characteristic to stay inside the light cone — a *conditional* requirement, since no
  in-repo result forces $K_B<1$;
- the full scalar/vector perturbation stability and the CMB/matter-power Boltzmann closure for this
  $\mathcal F$.

The admissible parameter region is therefore presently *conditional*: it has been proved neither empty
nor non-empty. The remaining programme is two well-posed calculations — the finite-$k$ scalar dispersion
$\det\mathcal D_{\rm scalar}(H,k;K_B,\ldots)$ and $\alpha_2(K_B,\ldots)$ — intersected with the $K_B\ge1$
causality condition.

---

## 10. Solar System and inherited liabilities

Because $\mu(y)\to1$ exponentially fast, the fractional deviation of the potential from Newtonian at
Solar-System accelerations is astronomically small — of order $10^{-(10^7)}$ at 1 AU for the exponential
kernel — so the kernel itself is invisible in the inner Solar System. The constraints that bite are
structural, not kernel-dependent:

- **Cassini / $\gamma_{\rm PPN}$.** In the AeST completion $\gamma_{\rm PPN}=1$ at the relevant order,
  passing Cassini. In the elliptic-constraint single-metric family, $\gamma_{\rm PPN}=1$ is achievable
  but at the cost of $\alpha_3=-3$ (Section 5.2), which is the excluding constraint there.
- **External-field effect and quadrupole.** MOND's characteristic external-field effect implies a
  Solar-System anomalous quadratic tidal term; the current audit places the modified-gravity-arm
  quadrupole near or modestly above the Cassini ceiling depending on kernel sharpness, and this remains a
  live constraint rather than a clean pass.
- **Preferred-frame parameters.** A preferred-frame completion generically induces $\alpha_1,\alpha_2$;
  for the specific $\mathcal F$ these are open (Section 9.4). We do **not** claim $\alpha_2=0$.

We also record, without re-deriving, that the exact-law limit of the framework carries an ephemeris
liability: a strictly constant sunward anomaly of order $a_0/2$ would over-produce the Earth–Mars ranging
residual by orders of magnitude, so the "exact law everywhere" reading is disfavoured relative to the
phenomenological kernel — a cost borne by the *exactness* claim, not by the phenomenology.

---

## 11. Local Lorentz invariance and time dilation

Because baryonic matter couples to the single physical metric $g_{\mu\nu}$ (in AeST via a physical/
disformal metric built from $g$, $A^\mu$, $\varphi$, but Lorentzian and unit-normalised for matter), a
freely moving clock measures ordinary metric proper time,
$$
d\tau^2 = -\frac{1}{c^2}g_{\mu\nu}\,dx^\mu dx^\nu \ \xrightarrow{\text{local Minkowski}}\
d\tau = dt\sqrt{1-v^2/c^2}.
$$
A preferred *foliation* is not a preferred *clock law*: the theory has the former (the aether / a
metric-defined time function) but the matter Lagrangian does not introduce a velocity-dependent clock
correction of the form $d\tau = dt\sqrt{1-v^2/c^2}\,F(v_{\rm pref}/c, a/a_0)$. Adding one would be a new
matter coupling and would be constrained precisely by $\alpha_1,\alpha_2$. Consequently ordinary special-
relativistic time dilation, and the standard twin-paradox result, survive intact: a traveller at
$v=0.99c$ for $2$ yr of proper time returns to a $\gamma\approx7.09$, i.e. $\sim14.2$ yr, later epoch,
independently of the low-acceleration modification, because MOND is tied to the gravitational/acceleration
regime and not to relativistic velocity. The invariant statement is that more proper time accumulates
along the stay-at-home worldline; no absolute "everyone else aged faster during the outbound leg" claim
is meaningful.

---

## 12. Scorecard

We tabulate the status of each gate. A tick means established and reproducible in this programme; a
question mark means open; a cross means excluded.

| Gate | Non-relativistic core | Single-metric (elliptic) | Single-metric (propagating) | Derivative bimetric | AeST class |
|---|---|---|---|---|---|
| $\mu=1-e^{-y}$ | ✓ | ✓ | ✓ | ✓ | ✓ |
| RAR ($0.108$ dex) / BTFR | ✓ | ✓ | ✓ | ✓ | ✓ |
| $\Phi=\Psi$ (lensing) | — | ✓ (repaired) | ✗ (slip-lock) | ✓ | ✓ (quasi-static) |
| Two DOF | — | ✓ | ✗ (3 DOF) | — | n/a (6 DOF, healthy) |
| Ghost-free | — | ✓ | ? (residue) | ✗ (vector $\Box^2$) | ✓ (published) |
| $c_T=c$ | — | ✓ | — | ✓ | ✓ |
| $\alpha_3$ | — | ✗ ($-3$) | — | ✓ ($0$) | ? |
| $\alpha_2$ | — | ✓ ($0$) | — | — | ? (open) |
| Cosmology $k\to0$ | — | — | — | — | ✓ (rescued) |
| Cosmology finite-$k$ | — | — | — | — | ? (open) |
| Dark-matter-free | — | (yes, but excluded) | (yes, but slip/3-DOF) | (yes, but ghost) | ✗ (dark field) |
| $a_0(z)\propto H(z)$ | ✓ (prediction) | inherits | inherits | inherits | inherits |

The reading of the table is the thesis of the paper: the non-relativistic core is solid; each
reduced-degree-of-freedom completion is closed by a specific, computed obstruction; and the only column
without an excluding cross is AeST, which pays for it with a dark field and two open gates.

---

## 13. Predictions and falsifiability

Independently of which completion survives, the framework makes concrete predictions inherited from the
non-relativistic core:

1. **BTFR slope exactly 4, normalisation fixed by $a_0$** — no free parameter; falsified by a measured
   slope departing from 4 beyond systematics, or a normalisation inconsistent with $9.36\times10^{-11}$.
2. **RAR with $\lesssim0.11$ dex intrinsic scatter and no second parameter** — falsified by a robust
   residual correlation with a galaxy property other than baryonic acceleration.
3. **$a_0\propto H(z)$** — the distinctive prediction. Standard cold dark matter has no $a_0$ and its
   emergent scale evolves differently. A measurement of the high-redshift acceleration scale (from
   high-$z$ rotation curves or dynamics) that is *constant* in physical units, or that tracks halo
   properties rather than $\sqrt{\rho_\Lambda(z)}$, falsifies the tie. This is the single most decisive
   test and the reason the whole framework is worth completing.
4. **A preferred-frame / lensing signature** at the completion level: the AeST completion predicts
   $\gamma_{\rm PPN}=1$ but non-zero preferred-frame parameters at some level; the sharp target is
   $\alpha_2$ for the specific exponential $\mathcal F$.

---

## 14. Discussion and honest conclusion

The Crispy Fried Chicken Theory of Gravity, in this version, is best described as a **well-specified
research programme with a solid non-relativistic core, a rigorous no-go map for its relativistic
completion, and a single surviving completion class carrying two open gates and a dark field.** We have
deliberately resisted three temptations that earlier phases of the work fell into: deriving $\kappa$
(it is fitted), claiming a dark-matter-free relativistic theory (the viable completion is not), and
declaring a two-degree-of-freedom single-metric completion (it is closed by an explicit
preferred-frame $\alpha_3$).

What survives is genuinely valuable. The exponential kernel is exact and its constitutive algebra is
clean. The MDAR, RAR, and BTFR follow with no shape freedom. The scale's tie to $\rho_\Lambda$ yields a
falsifiable $a_0\propto H(z)$. And the completion analysis is not a collection of failed guesses but a
*structured* result: it identifies, constructively, that the completion must contain a preferred-frame
vector, and it isolates the two calculations — the finite-$k$ cosmological dispersion and $\alpha_2$ for
the exponential $\mathcal F$ — whose outcome decides whether the AeST-class completion is viable.

The honest final label is: **candidate programme; core established; completion conditional.** The next
step is not another architecture. It is those two calculations, performed on the one action that is not
yet excluded.

---

## Appendix A — the constitutive identities

For $\mu(y)=1-e^{-y}$ define $G(y)=y^2+2(1+y)e^{-y}-2$. Then
$$
G'(y) = 2y + 2e^{-y} - 2(1+y)e^{-y} = 2y - 2y e^{-y} = 2y(1-e^{-y}) = 2y\,\mu(y),
$$
so $G'(y)/2y=\mu(y)$. In the covariant variable $Z$ with $y=\tfrac12\sqrt Z$,
$F(Z)=4[1-(1+\tfrac12\sqrt Z)e^{-\sqrt Z/2}]$ gives, with $s=\sqrt Z/2$, $dF/ds=4s e^{-s}$ and
$dZ/ds=8s$, hence $F'(Z)=\tfrac12 e^{-\sqrt Z/2}$. The MOND operator's principal symbol
$A^{ij}=\mu\gamma^{ij}+y\mu'\hat u^i\hat u^j$ has eigenvalues $\lambda_\perp=\mu=1-e^{-y}$ and
$\lambda_\parallel=\mu+y\mu'=1-(1-y)e^{-y}$; both are positive for $y>0$
($\lambda_\parallel\to1$ as $y\to0^+$ and $\to+\infty$ as $y\to\infty$), so the operator is strictly
elliptic on the MOND branch. All identities are verified symbolically in the accompanying scripts.

## Appendix B — obstruction certificates

Each obstruction in Sections 5–7 is backed by a committed symbolic computation. We list the decisive
outputs.

- **DC-013 (slip-lock).** Exact linearised $R^{(1)}=-2\nabla^2\Phi+4\nabla^2\Psi$; a frame-free scalar's
  $(\Phi,\Psi)$ imprint locked to the $(1,-2)$ ray gives $\eta=(4L+m)/(8L+m)\neq1$.
- **DC-018 (bimetric potential).** Spherical helicity-0 scaling $\pi'\propto r^{1-3/n}$; integer
  $n\in\{1,2,3,4\}$ give $\{r^{-2},r^{-1/2},r^0,r^{1/4}\}$; MOND $r^{-1}$ needs $n=3/2$ (non-integer).
- **DC-019 (elliptic $\alpha_3$).** PPN dictionary at $\gamma_{\rm PPN}=1$ with the instantaneous
  $g_{00}$ coefficient held at $1$ gives $\alpha_1=0$, $\alpha_3=-3$; robust to the choice of spatial
  slip-removal lock ($D^2q$, $u=\phi-q$, $D^2\phi=\tfrac14R^{(3)}$, $N=\exp[\tfrac14D^{-2}R^{(3)}]$ all
  reduce to $N=e^{\Psi/c^2}$ in the weak field).
- **DC-020 (vector ghost).** Stückelberg transverse operator $-\lambda(2u_0+u_1)(\omega^2-\kappa^2)^2/2$
  ($\Box^2$ double pole); physical time-kinetic matrix $W=\mathrm{diag}(-2,\tfrac92)$, $\det W=-9$; the
  MOND coefficient $a=-2(2u_0+u_1)$ so $a\neq0\Leftrightarrow$ ghost; controls (Einstein–Hilbert,
  Fierz–Pauli) clean; $c_T=c$ exactly on the whole subspace; helicity-0 non-dynamical (no
  Boulware–Deser scalar).
- **Phantom-density anisotropy.** $L=\sqrt\gamma\,f(y)$, $y=|\nabla\Phi|/a_0$, gives traceless stress
  $T_{xx}-T_{yy}=-y\,f'(y)$; non-zero for $f=(\nu-1)\rho_b$ ($f'=\rho_b\nu'\neq0$ in the MOND transition).

## References (selected)

- M. Milgrom, *A modification of the Newtonian dynamics as a possible alternative to the hidden mass
  hypothesis*, ApJ 270, 365 (1983).
- J. Bekenstein & M. Milgrom, *Does the missing mass problem signal the breakdown of Newtonian gravity?*,
  ApJ 286, 7 (1984) [AQUAL].
- M. Milgrom & R. H. Sanders, ApJ 678, 131 (2008) [the $\nu$-family, Eq. 13].
- M. Milgrom, *Quasi-linear formulation of MOND*, MNRAS 403, 886 (2010) [QUMOND].
- S. McGaugh, F. Lelli & J. Schombert, *Radial Acceleration Relation in Rotationally Supported Galaxies*,
  PRL 117, 201101 (2016) [SPARC RAR].
- C. Skordis & T. Złośnik, *New Relativistic Theory for Modified Newtonian Dynamics*, PRL 127, 161302
  (2021) [AeST].
- C. Skordis & T. Złośnik, *Aether scalar tensor theory: Hamiltonian formalism*, arXiv:2307.15126 (2023)
  [6 DOF].
- S. Hassan & R. Rosen, *Bimetric gravity from ghost-free massive gravity*, JHEP 02 (2012) 126.
- C. Will, *Theory and Experiment in Gravitational Physics* (2nd ed., 2018) [PPN, $\alpha_i$ bounds].
- B. Abbott et al. (LIGO/Virgo), *GW170817 / GRB 170817A*, ApJL 848, L13 (2017) [$c_T=c$].

---

*Provenance note.* This is version 2.0.0: a consolidation of scattered internal results
(`FINAL_CLOSURE`, `THE_COMPLETION`, and the `closure_2026/` obstruction certificates) into a single
flagship document, with the honest-status corrections foregrounded. It supersedes informal earlier
drafts. All load-bearing claims are backed by committed, runnable scripts in the repository; every
"open" label is deliberate.
