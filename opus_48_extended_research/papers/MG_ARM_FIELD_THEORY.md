# The modified-gravity arm: a Bekenstein–Milgrom field theory for $a_{0}=\kappa c\sqrt{G\rho_{\Lambda}}$

**Carl P. Zimmerman**
Briar Creek Tech

*Version 1 (2026-08-08).*

---

## The theory in one box

$$\boxed{\;S=-\!\int\! d^{3}x\left[\frac{a_{0}^{2}}{8\pi G}\,\mathcal{F}(X)+\rho\,\phi\right],
\qquad X=\frac{|\nabla\phi|^{2}}{a_{0}^{2}},
\qquad \nabla\!\cdot\!\big[\mu(x)\nabla\phi\big]=4\pi G\rho\;}$$

with $\mu=\mathcal{F}'(X)$, $x=|\nabla\phi|/a_{0}$, and the acceleration scale **not** a free constant
but

$$\boxed{\;a_{0}=\kappa\,c\sqrt{G\rho_{\Lambda}}=\frac{cH_{\Lambda}}{Z}=9.36\times10^{-11}\ \mathrm{m\,s^{-2}},
\qquad \kappa=\tfrac12,\quad Z=2\sqrt{8\pi/3}\;}$$

The free function is not postulated. For the framework's in-force kernel
$\nu=1/(1-e^{-\sqrt{y}})$ it is **derived in closed parametric form**, and its derivative is exact at
every acceleration:

$$\mathcal{F}'(X)=\mu=1-e^{-\sqrt{y}},\qquad y=x\mu=g_{\rm bar}/a_{0}$$

with limits $\mathcal{F}\to\tfrac23X^{3/2}$ (deep) and
$\mathcal{F}\to X-C_{0}+4e^{-s}(s^{3}+3s^{2}+6s+6)$, $s=X^{1/4}$ (Newtonian), where $C_{0}$ is a pure
constant in the Lagrangian and therefore **unobservable** — only $\mathcal{F}'$ enters the field
equation.

**Seven properties are proved rather than assumed** (§4): convexity of $\mathcal{F}$ — from which
existence, uniqueness, Newton's third law, standard centre-of-mass motion and the exact baryonic
Tully–Fisher relation all follow — plus ellipticity, ghost-freedom, subluminality, positive phantom
density, and a Newtonian residual that is exponentially small *in the action*.

**And it lenses**, because the modification is in the field equation. That is why this is the arm.

**The honest caption.** $\kappa=\tfrac12$ is **fitted**; nothing here derives it. Bekenstein–Milgrom
is not new — it is theirs, from 1984. What is offered is the *coefficient*, the kernel forced by
solar-system ranging, and the closed-form free function with its health proved for that kernel. The
theory is non-relativistic as written (§7). And the cluster shortfall is untouched by the switch (§5.3).

---

## 0. Why this paper exists

This framework has spent most of its life as a **modified-inertia** theory: the metric Newtonian, the
particle's inertia acceleration-dependent. That reading is now excluded, and the exclusion is worth
stating plainly because it is what motivates everything below.

In modified inertia the metric is unmodified and sourced by baryons — that is not an incidental
feature but a requirement, since the whole content is a modified *response* to a Newtonian field. And
photons have no rest mass to modify. So modified inertia predicts $M_{\rm lens}=M_{\rm bar}$, hence
$M_{\rm dyn}/M_{\rm lens}=1/f_{\rm bar}\approx6.4$ in clusters, against an observed $1.0$–$1.3$:
**excluded at $\sim21\sigma$**, and still at $4.2\sigma$ if the systematic on that ratio is inflated
fivefold [1].

Three rescue routes were computed and all three closed. The enhancement cannot sit in *both* the
metric and the inertia — doing both gives $a=\nu^{2}g_{\rm bar}$, wrong by one factor of $\nu$. The
worldline action does have Randers–Finsler form when $\mu$ depends on position, which would give
photons a geometry to follow — but **the resulting null cone degenerates at $\mu=\tfrac12$ and the
signature turns Euclidean below it**, unavoidably, since every interpolation reaching the deep-MOND
limit must cross $\mu=\tfrac12$; on this framework's kernel that happens at $g_{\rm bar}=0.48a_{0}$,
the outer disc of a spiral galaxy [2]. And Bekenstein–Milgrom's own point-particle limit is
*memoryless*, so the modified-inertia action is not that limit either [3].

**Modified inertia and modified gravity are algebraically identical for massive test particles.** That
is precisely why the framework could remain ambiguous about which it was for years. Lensing is the
observation that separates them, and it selects the metric.

**What survives the switch is the part that mattered: $a_{0}=\kappa c\sqrt{G\rho_{\Lambda}}$ is a
statement about the coefficient and is arm-independent.**

---

## 1. The coefficient claim

$a_{0}\sim cH_{0}$ has been noticed for forty years. Writing it with the *asymptotic* de Sitter rate
$H_{\Lambda}=c\sqrt{\Lambda/3}$ instead of the present one makes it a constant for a structural
reason rather than a coincidence of epoch, and turns it into a relation between the **dark-energy
scale** and the **dark-matter-phenomenology scale**:

$$a_{0}=\kappa\,c\sqrt{G\rho_{\Lambda}},\qquad \kappa=\tfrac12\ \Rightarrow\ a_{0}=9.3619\times10^{-11}\ \mathrm{m\,s^{-2}}$$

ΛCDM has no reason to predict such a relation; this framework has no freedom to avoid it. That
asymmetry is the framework's principal asset, and it is **not** evidence that the framework is
correct.

The mechanism behind the numerical coincidence is Milgrom's: an observer with proper acceleration $a$
in de Sitter space sees a temperature $\propto\sqrt{a^{2}+a_{\Lambda}^{2}}$ [4,5], so the bath has a
floor, and the excess $\Delta T=T(a)-T(0)$ has both MOND limits. **The interpolating function that
follows is Eq. (9) of Milgrom (1999), not a variant of it.** That paper fixes $a_{0}=2cH_{\Lambda}$;
$\kappa=\tfrac12$ corresponds to $cH_{\Lambda}/5.79$. The factor of eleven between them is this
framework's distinctive quantitative content, and it is fitted, not derived.

---

## 2. Why the kernel is exponential

MOND's interpolating function is usually treated as free within limits. It is not: **solar-system
ranging constrains its approach to Newtonian behaviour**, and two natural power-law families fail.

- The $1/g$-tailed kernel misses the Earth/Mars bound by a factor $\sim1279$.
- The next one misses the Mars ranging budget by $8.5$–$12.4\times$, and for a subtle reason: its
  slowly-decaying tail binds not at a planet but at **the Sun**, whose acceleration in Jupiter's field
  is itself only $\sim2233\,a_{0}$.

The surviving choice is an **exponential** approach,

$$\nu(y)=\frac{1}{1-e^{-\sqrt{y}}},\qquad \mu=1-e^{-\sqrt{y}}$$

whose Newtonian residual dies as $e^{-\sqrt{y}}$ — utterly negligible at ephemeris accelerations
($\nu-1<10^{-40}$ at $y=10^{4}$). This was arrived at against the author's preference and it retired
two previously published kernel choices [6].

---

## 3. The field theory, and the free function

Bekenstein–Milgrom [7] replaces the Poisson equation with
$\nabla\!\cdot\![\mu(|\nabla\phi|/a_{0})\nabla\phi]=4\pi G\rho$, derivable from the action in the box.
The theory's content is the free function $\mathcal{F}$, and for this kernel it is obtained rather
than assumed.

In spherical symmetry the field equation integrates exactly to $\mu(x)\,x=y$, and
$g_{\rm obs}=\nu(y)g_{\rm bar}$ means $x=\nu(y)y$. Substituting $u=\sqrt{y}$ gives the whole theory in
one clean parametric pair:

$$\mu=1-e^{-u},\qquad x=\frac{u^{2}}{\mu},\qquad u\in(0,\infty)$$

from which $\mathcal{F}$, its convexity, the ellipticity eigenvalues, the scalar sound speed and the
phantom density all follow analytically. **The map is a bijection and the inversion round-trips**, so
the parametrisation is not a reparametrisation trick.

The two asymptotic forms are exact and quotable:

$$\mathcal{F}(X)\to\tfrac23X^{3/2}\quad\text{(deep MOND)},\qquad
\mathcal{F}(X)\to X-C_{0}+4e^{-s}\big(s^{3}+3s^{2}+6s+6\big),\quad s=X^{1/4}\quad\text{(Newtonian)}$$

**A trap worth flagging, because the accompanying script caught itself falling into it.** $X=x^{2}$,
so $\sqrt{X}=x$, and $x=y/\mu\sim u^{2}$ while $u=\sqrt{y}$. The Newtonian residual is therefore
exponential in $X^{1/4}=\sqrt{x}=\sqrt{y}$, **not** in $\sqrt{X}$. The clean physical statement is
that $\mathcal{F}'$ approaches unity like $e^{-\sqrt{g_{\rm bar}/a_{0}}}$ — Route A's kernel restated
variationally.

**And that is the field-theoretic point of the whole construction: the ephemeris relief is a property
of the Lagrangian, not of an algebraic force law bolted on afterwards.**

---

## 4. What is proved

Seven properties, established rather than assumed [8]:

| | |
|---|---|
| **convexity of $\mathcal{F}$** | and from it: existence, uniqueness, Newton's third law, standard centre-of-mass motion, **exact BTFR** |
| **ellipticity** | both eigenvalues of the field operator computed |
| **ghost-freedom** | |
| **subluminality** | the scalar sound speed computed |
| **positive phantom density** | |
| **exact BTFR** | with the coefficient obtained *from the action* |
| **exponentially small Newtonian residual** | in the action, evaluated at the Sun |

Every standard theorem of the Bekenstein–Milgrom class follows from the first line. That is the
structural reason this arm is on firmer ground than the one it replaces: the health is a *consequence*
of a single proved property rather than a list of separately-checked conditions.

---

## 5. Observational standing

### 5.1 Galaxy scales: works, and non-diagnostic of the coefficient

The radial acceleration relation is reproduced with $0.108$ dex scatter at $\Upsilon_{3.6}=0.70$,
*better* than regularised MOND's $0.122$ on the same data. But **the penalty for moving $a_{0}$ by 20%
is under half a per cent in that scatter.** The RAR is compatible with this framework and
non-diagnostic of its coefficient; claims in either direction are interpolation-shape and
mass-to-light artefacts, and two such claims in the author's own corpus were withdrawn for exactly
this reason.

The same caution applies to the BTFR intercept, which is $\Upsilon$-degenerate. The sharpest
$\Upsilon$-free handle — the gas-dominated slope — gives a box $[0.84,1.36]\times10^{-10}$ that
contains both $9.36\times10^{-11}$ and $1.2\times10^{-10}$ and does not discriminate.

### 5.2 Lensing: this is what the switch buys

The metric is modified, so light feels the enhancement. The $21\sigma$ exclusion of §0 does not apply.
**This is the entire reason for the paper.** The lensing *amplitude* is a prediction of the
relativistic completion, not of the non-relativistic theory written here — see §7.

### 5.3 Clusters: unchanged, and still the sharpest problem

**The switch buys nothing here, and that must be said.** The cluster shortfall is a property of the
*kernel*, not of which sector is modified. On this framework's own kernel the required boost at
$R_{500}$ has median $\eta=2.334$ ($0.368$ dex), at $2.0$–$4.1\sigma$.

A full audit of the measurements [9] finds they largely hold up. There *is* one real, published,
unresolved error in the X-ray mass scale — Chandra hydrostatic masses are $14\pm2\%$ higher than
XMM's on 64 clusters observed by both — and it points the framework's way. **It is 14% against a
needed 133%.** The better-established systematic (hydrostatic bias from uncounted non-thermal
pressure) points the *other* way, and the two substantially cancel.

**The wall is the cosmic baryon budget, and no instrument can move it.** Clusters are already at the
cosmic baryon fraction: $f_{\rm gas}(r_{500})=0.163\pm0.032$ against
$\Omega_{b}/\Omega_{m}=0.167\pm0.006$. Headroom for undetected baryons is at most $1.22\times$ against
a required $2.33\times$. Every knob turned favourably at once absorbs $1.39\times$, leaving a residual
factor $1.68$.

**If you are looking for the observation most likely to kill this framework, it is clusters, and it
has been for thirty years.**

### 5.4 Wide binaries: the registered prediction moves

The author maintains a frozen, hash-stamped Gaia DR4 pre-registration. **Its target is the
modified-inertia value, and this arm predicts a different one.** For a point-field AQUAL-type
external-field effect the boost is isotropic and equals $\sqrt{\nu}$ at the external field:

$$\gamma_{v}^{\rm MG}=\sqrt{\nu(y_{\rm ext})}=1.2139\ \text{(canonical)},\quad1.2592\ \text{(alt footing)}$$

against $\gamma_{v}^{\rm MI}=1.1582$, range $1.1311$–$1.1964$. **The ranges are disjoint.** Moving the
registered target is an amendment-grade change and has not been made in this paper.

It cuts both ways: the separation is $2.68\sigma$ at the registered sample size, so **DR4 can
distinguish the two arms** — which the modified-inertia reading could not do. That is a lever, not a
decisive test, and it is stated as one.

### 5.5 The directional external-field test: now a signal, and it already fired

**This is the strongest thing the switch buys, and it required no new observation.** In an aligned
rotation-curve asymmetry relative to the external field direction, **pure modified inertia predicts
exactly zero**; AQUAL-class theories predict $1$–$4\%$ with a definite sign. A first firing of that
test gave $\hat A=+2.95$ at $p=0.029$ **with the AQUAL-class sign.**

So a measurement that was evidence *against* the previous arm is evidence *for* this one. At
$p=0.029$ it is a lever rather than a confirmation; settling it needs $N\sim1157$ galaxies, and the
field direction is reconstructable from existing peculiar-velocity maps.

---

## 6. What the switch cost

Stated first-class, because two of these were the headline results of the arm being abandoned.

- **$a_{0}=\tfrac23c\,m^{2}/g$ is gone.** That reading was the modified-inertia memory kernel's first
  moment. A Bekenstein–Milgrom theory has no kernel and no moment; $a_{0}$ enters $\mathcal{F}$
  directly.
- **And with it the $\zeta$-pole no-go**, which was a theorem about that first moment. Its conclusion —
  that $a_{0}$ has the status of a renormalisation condition — may still hold here, but it would have
  to be **re-derived** and is not inherited.
- **The $g^{-2}$ Lorentz-violation prediction is gone in pure Bekenstein–Milgrom**, which has no
  preferred frame at all. It survives only if the relativistic completion is AeST-type, carrying a
  vector. **Which completion is adopted therefore decides whether the framework keeps that prediction
  — it is not a detail.**
- **The Cassini quadrupole tension is inherited.** The AeST-class realisation carries a $3$–$15\sigma$
  RAR-versus-$Q_{2}$ tension that modified inertia did not. **This is the item a referee will find
  first.**
- The **parity theorem** — that no polynomial-in-$u$ worldline action can produce MOND — remains
  *true* but is no longer load-bearing.

---

## 7. What is owed

1. **A relativistic completion.** The theory as written is non-relativistic. Cosmology, the CMB, and
   the lensing *amplitude* all require AeST or TeVeS [10,11], each with its own constraints. **Until
   that is fixed, "it lenses" is a statement about the sign and the mechanism, not about the
   amplitude.**
2. **The amendment moving $\gamma_{v}$** (§5.4), which is a registration change and deliberately not
   made here.
3. **Clusters** (§5.3). Unchanged by the switch and still the most likely killer.
4. **$\kappa=\tfrac12$.** Sixteen distinct attempts to force it have failed; the residue after tracing
   $\sqrt{6}$ to the Friedmann equation and $\sqrt{\pi}$ to the three-dimensional momentum measure is
   a single bare factor of two.
5. **Whether the $g^{-2}$ prediction survives**, which follows from item 1.

---

## 8. What is not claimed

- **Bekenstein–Milgrom is not new.** It is theirs, 1984. The interpolating function is Milgrom's, 1999.
  What is offered here is the coefficient, the kernel forced by ranging, and the closed-form free
  function with its health proved for that kernel.
- **$\kappa=\tfrac12$ is fitted, not derived.**
- **No claim is made regarding particle physics, the Standard Model, or unification.** The author
  publicly withdrew earlier statements of that kind in June 2026 and does not restate them. The
  relevant obstruction is specific: this framework's characteristic constant carries $\sqrt{\pi}$
  while all flavour observables are algebraic, so the structure is *blind* to the gauge sector.
- **This is modified gravity, and it does not derive $a_{0}$.** The accompanying script says so in its
  own exit message.

---

## 9. Reproducibility

Every quantitative claim is produced by a committed script that exits non-zero if any internal check
fails, and each carries negative controls that must trip.

- `mi_route_a_field_theory_2026.py` — §§3–4, 11/11 checks.
- `mi_route_a_kernel.py` — §2, 6/6 checks.
- `mi_mg_arm_standing_2026.py` — §§5.4–6, 18/18 checks.
- `mi_lensing_axis_2026.py` — §0, 24/24 checks.
- `mi_finsler_null_cone_2026.py` — §0, 23/23 checks.
- `mi_cluster_measurement_audit_2026.py` — §5.3, 27/27 checks.
- `mi_route_a_wb_gamma_v_2026.py` — §5.4, 26/26 checks.

Both $a_{0}$ footings (canonical $\rho_{\rm DE}$ with $cH_{\Lambda}$; alternative $\times1.2048$) are
carried on every dimensionful number.

**AI-assistance disclosure.** Portions of the analysis, numerical verification and drafting were
carried out with the assistance of a large language model (Anthropic Claude). The author directed the
work, specified and reviewed every load-bearing calculation, and takes full responsibility including
for any errors. No AI system satisfies the criteria for authorship and none is listed as an author.
Claims found to be incorrect during this work were withdrawn rather than quietly re-scoped; the
modified-inertia arm's demotion, recorded in §0 and §6, is the largest of them.

---

## References

[1] C. P. Zimmerman, *A local, generally covariant field theory of modified inertia*, Zenodo, concept
DOI 10.5281/zenodo.21854914, §8 (v6).

[2] `mi_finsler_null_cone_2026.py`, this repository — the Randers null-cone degeneracy.

[3] `mi_point_particle_limit_2026.py`, this repository.

[4] M. Milgrom, *The modified dynamics as a vacuum effect*, Phys. Lett. A **253**, 273 (1999).

[5] S. Deser and O. Levin, Class. Quantum Grav. **14**, L163 (1997).

[6] Amendment 8 to the author's frozen Gaia DR4 pre-registration (2026-08-03).

[7] J. Bekenstein and M. Milgrom, *Does the missing mass problem signal the breakdown of Newtonian
gravity?*, Astrophys. J. **286**, 7 (1984).

[8] `mi_route_a_field_theory_2026.py`, this repository.

[9] `mi_cluster_measurement_audit_2026.py`, this repository; G. Schellenberger et al., Astron.
Astrophys. **575**, A30 (2015); A. Mantz et al., MNRAS **433**, 2790 (2013).

[10] J. Bekenstein, *Relativistic gravitation theory for the modified Newtonian dynamics paradigm*,
Phys. Rev. D **70**, 083509 (2004).

[11] C. Skordis and T. Złośnik, Phys. Rev. Lett. **127**, 161302 (2021).

[12] M. Milgrom, *Dynamics with a non-standard inertia–acceleration relation*, Ann. Phys. **229**, 384
(1994).
