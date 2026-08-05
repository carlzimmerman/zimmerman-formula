# What Can and Cannot Fix the MOND Acceleration Coefficient: a Relabelling Theorem, Three Failed Derivations, and a Redshift Discriminant

**Carl P. Zimmerman** — Briar Creek Tech

*2026-08-04. All numerical claims are reproduced by public self-checking scripts included in this record; each prints `[OK]`/`[FAIL]` per internal check and exits non-zero if any fails. See §9.*

---

## Abstract

The MOND acceleration scale is numerically close to $cH_\Lambda$, and the proposal that it is *set* by the
cosmological constant dates to Milgrom (1994, 1999). The relation's **form** is established; its dimensionless
$\mathcal{O}(1)$ **coefficient** is not derived by any published argument, and the live proposals differ — Milgrom
(1999) gives $a_0 = 2cH_\Lambda$, Milgrom (2020) gives $\kappa = 1/2\pi$, and one of us has used
$a_0 = \tfrac12 c\sqrt{G\rho_\Lambda}$, i.e. $a_0 = cH_\Lambda/Z$ with $Z = 2\sqrt{8\pi/3}$. That last value is
**fitted, not derived**, and nothing below changes that.

This paper is about what could change it. We prove a **relabelling theorem**: because
$\Lambda = 8\pi G\rho_\Lambda/c^2$ identically, $G\rho_\Lambda$ and $c^2\Lambda$ are the *same* scale up to the
pure number $8\pi$, so any construction that forms a combination of the two returns that scale times a power of
$8\pi$ and cannot select a coefficient. We then audit three constructions of the kind that naturally suggest
themselves, and all three fail — one on dimensions, one because its free parameter is merely relocated, one on a
sign that makes its central quantity imaginary in a homogeneous vacuum. Two of the three additionally commit the
same factor-of-two error, attaching their coefficient to $a_0$ rather than to the **floor** $a_0/2$ that Milgrom's
balance actually contains; we record this as a systematic hazard, having committed it ourselves.

Three results are constructive. **(i)** The relabelling theorem does *not* exclude a single-scale derivation:
$\sqrt{G\rho_\Lambda}$ is $\pi$-free while $\sqrt{8\pi G\rho_\Lambda/3}$ is not, so a construction taking
$\rho_\Lambda$ as its only input is untouched by the theorem and would *automatically* exclude $cH_\Lambda$,
being unable to manufacture the Friedmann $8\pi/3$. **(ii)** No standard local rate supplies the required
factor $\tfrac14$: over seven candidates the closest is $\sqrt{G\rho/4\pi}$ at **12.84%** away, wider than the
7.87% separating the two published coefficients, so there is no near miss to argue into place. **(iii)** The
choice of floor is **observationally decidable and needs no new mechanism**: a local response to the vacuum
*density* gives $a_0 \propto \sqrt{\rho_{\rm DE}}$, exactly constant for $w = -1$ and blind to matter, whereas a
horizon floor tracks $cH(z) = cH_0E(z)$, rising to $1.78$, $3.01$, $4.54$ times its present value at $z = 1, 2, 3$.
The local reading is therefore the **more falsifiable** of the two, because it forbids the rising branch the
horizon reading permits.

We conclude that the coefficient problem should be attacked observationally rather than by further mechanism
search, and we state the methodological reason: $\kappa$ is a fitted number, so searching constructions until one
reproduces it is reverse-engineering a fit.

---

## 1. The problem, and the identification that sharpens it

That $a_0 \sim cH_0$ has been noted since Milgrom (1983). The sharper claim — that the relevant density is the
*dark-energy* density — is also not new: **Milgrom (1994, *Ann. Phys.* 229, 384, §II eq. 3)** writes
$a_\lambda = c^2\sqrt{\Lambda/3}$, and **Milgrom (2020)**, *"The $a_0$–cosmology connection in MOND"*, develops it
directly. The interpolating function $\nu(y) = \sqrt{1+1/y}$, $y \equiv g_{\rm bar}/a_0$, is **Milgrom (1999,
*Phys. Lett. A* 253, 273, eqs. 6–9)**, who fixes its coefficient at $\hat a_0 = 2cH_\Lambda$; the underlying
five-acceleration construction is **Deser & Levin (1997, *CQG* 14, L163)**. The exponential kernel
$\nu = (1-e^{-\sqrt y})^{-1}$ is **McGaugh (2008, *ApJ* 683, 137, eq. 11a)**. None of the *form* is available to
claim; only the coefficient is open.

The identification that organises everything below is elementary and exact. The relation

$$g_{\rm obs}^2 \;=\; g_{\rm bar}^2 + a_0\,g_{\rm bar}$$

is **identically** $g_{\rm bar} = \sqrt{g_{\rm obs}^2 + (a_0/2)^2} - a_0/2$, i.e. Milgrom's five-acceleration
balance $I(a) = \sqrt{a^2 + k^2} - k$ with the floor $k = a_0/2$. So the entire distinctive content of any
coefficient proposal is **the value of the floor**, and

$$a_0 \;=\; 2k \quad\text{always.}$$

Milgrom (1999) and Deser & Levin take $k = cH_\Lambda$, giving $q \equiv a_0/cH_\Lambda = 2$. The value
$\kappa = \tfrac12$ requires $k = \tfrac14 c\sqrt{G\rho_\Lambda} = 4.6810\times10^{-11}\ \mathrm{m\,s^{-2}}$,
which is $cH_\Lambda/2Z$ with

$$2Z \;=\; 4\sqrt{8\pi/3} \;=\; 8\sqrt{6\pi}/3 \;=\; 11.577620072932.$$

Equivalently $k = (c/4)/t_{\rm dyn}$ with $t_{\rm dyn} = 1/\sqrt{G\rho_\Lambda} = 1.6011\times10^{18}\ \mathrm{s}$:
an acceleration built from $c$ and **one** density, carrying **no** $8\pi$ and **no** $3$. That absence is the
whole discriminant against $cH_\Lambda = c\sqrt{8\pi G\rho_\Lambda/3}$.

Throughout, dimensional quantities are given on the canonical footing
($\rho_{\rm DE}$ with $cH_\Lambda$, $a_0 = 9.3614\times10^{-11}\ \mathrm{m\,s^{-2}}$); the alternative footing
($\rho_{\rm total}$ with $cH_0$) is larger by $1/\sqrt{\Omega_\Lambda} = 1.2082$, giving
$1.13\times10^{-10}\ \mathrm{m\,s^{-2}}$. No conclusion below depends on the choice.

## 2. The relabelling theorem, and its exact boundary

**Theorem.** Let $\omega_\rho^2 = G\rho_\Lambda$ and $\omega_\Lambda^2 = c^2\Lambda$. Since
$\Lambda = 8\pi G\rho_\Lambda/c^2$ identically,

$$\frac{\omega_\rho^2}{\omega_\Lambda^2} \;=\; \frac{1}{8\pi} \qquad\text{exactly,}$$

a pure number. Any homogeneous combination of the two — geometric mean, arithmetic mean, any weighted power — is
therefore *either one of them* multiplied by a power of $8\pi$. Such a construction carries no information capable
of selecting a coefficient, and in particular **cannot exclude** $cH_\Lambda$, which is the same scale times
$\sqrt{8\pi/3}$. (Verified symbolically: the geometric mean is $\omega_\Lambda^2/\sqrt{8\pi}$.)

This is the same structure as a result we reported earlier for the $\kappa$-linear family, where every member is
proportional to $\kappa^n$ and the family therefore relabels rather than constrains.

**The boundary matters, and we state it because we first overstated it.** The theorem excludes *two-scale
combinations*. It does **not** exclude every use of $\rho_\Lambda$. The functions $\sqrt{G\rho_\Lambda}$ and
$\sqrt{8\pi G\rho_\Lambda/3}$ are genuinely different — the first is $\pi$-free, the second is not — so a
derivation whose **only** input is the density $\rho_\Lambda$ has no second scale to average against and no $8\pi$
in which to hide. Such a derivation is untouched by the theorem, and it would automatically exclude $cH_\Lambda$
because it can never produce the Friedmann factor. This is the one structurally open route.

It is also worth stating what is *not* an option. If the density in $\sqrt{G\rho}$ were the **local baryonic**
density — the detector's own mass, a galactic core — then $a_0$ would be environment-dependent. Solar-neighbourhood
baryons at $\simeq 0.1\,M_\odot\,\mathrm{pc}^{-3}$ are $1.158\times10^{6}$ times $\rho_\Lambda$, making $a_0$
about **1076 times too large** there and varying by orders between galaxies. So "local" can only mean that the
*response* is local while the *source* remains the uniform vacuum density. There is no third option.

## 3. Construction I: zero-point kinematic interference

*Proposal.* Treat $\omega_\rho^2 = G\rho$ and $\omega_\Lambda^2 = c^2\Lambda$ as two distinct fundamental scales;
take their interference as the geometric mean; apply the harmonic-oscillator zero-point half-weight; read off
$\text{Floor} = \tfrac12\sqrt{\omega_\rho^2\omega_\Lambda^2}$. This is claimed to force $\kappa = \tfrac12$ and to
exclude $cH_\Lambda$ on the ground that a real detector *has* a density and therefore couples, whereas
$cH_\Lambda$ assumes a massless test particle in an empty universe.

*The instinct is right.* Whether the floor is a bare-horizon property or a matter-coupled local response is
exactly the open question, and $\sqrt{G\rho}$ *is* the natural local response rate.

*The derivation fails five ways.* **(i) Dimensions.** $G\rho$ and $c^2\Lambda$ are both $\mathrm{s^{-2}}$, so
their geometric mean is $\mathrm{s^{-2}}$ — a frequency *squared*. A floor is an acceleration,
$\mathrm{m\,s^{-2}}$. **(ii)** Taken literally the number is $9.778\times10^{-37}\ \mathrm{s^{-2}}$ against
$a_0 = 9.362\times10^{-11}\ \mathrm{m\,s^{-2}}$, a ratio of $1.04\times10^{-26}$; the apparent match arises from
reading $c\sqrt{G\rho\Lambda}$ as $c\sqrt{G\rho_\Lambda}$, which are different expressions.
**(iii) The charitable repair still misses.** Redone with genuine accelerations,
$a_\rho = c\sqrt{G\rho_\Lambda}$ and $a_\Lambda = c^2\sqrt\Lambda$, the half geometric mean is
$2.0962\times10^{-10} = 2.2390\,a_0$ — and that overshoot is *exactly* $(8\pi)^{1/4}$, pinned to $10^{-6}$.
**(iv)** That the miss is a power of $8\pi$ is the signature of §2: the construction is a relabelling.
**(v)** Its physical story is the falsified one — with $\rho = \rho_{\rm local}$ it is 1076 times off, and with
$\rho = \rho_\Lambda$ it keeps the number but discards the story that was supposed to exclude $cH_\Lambda$.

## 4. Construction II: a temperature functional with $r \neq 1$

Milgrom's balance posits inertia proportional to the excess de Sitter–Unruh temperature above the
Gibbons–Hawking floor. For an arbitrary functional $I = f(T) - f(T_{\rm GH})$ with
$T = \sqrt{a^2+H^2}/2\pi$, we have $T - T_{\rm GH} = a^2/4\pi H$ exactly, so $c_2 = f'(T_{\rm GH})/4\pi H$; and
$T \to a/2\pi$ gives $c_1 = c_1'/2\pi$ with $c_1' \equiv \lim_{T\to\infty}f(T)/T$. Hence

$$q \;=\; \frac{c_1}{c_2} \;=\; \frac{2\,c_1'}{f'(T_{\rm GH})} \;\equiv\; \frac{2}{r},
\qquad r \equiv \frac{f'(T_{\rm GH})}{c_1'},$$

and $q$ is invariant under $f \mapsto \alpha f + b$, so $r$ is the *only* physical content of $f$. Milgrom's
$f = T$ is the $r = 1$ member, returning $q = 2$ with $c_1 = 1/2\pi$, $c_2 = 1/4\pi$.

| | $q$ | required $r = 2/q$ |
|---|---|---|
| Milgrom (1999), $f = T$ | $2$ | $1$ |
| Milgrom (2020) | $1/2\pi = 0.15915494$ | $4\pi = 12.566371$ (**exact**) |
| $\kappa = \tfrac12$ | $1/Z = 0.17274707$ | $2Z = 11.577620$ |

An explicit member with $r = 2Z$ exists:
$f(T) = T + \lambda\beta T_{\rm GH}(1 - e^{-(T-T_{\rm GH})/\beta T_{\rm GH}})$ with $\lambda = 2Z-1$ is smooth and
strictly increasing, asymptotically linear with slope exactly $1$, has $f'(T_{\rm GH}) = 2Z$, and delivers
$q = \sqrt6/8\sqrt\pi = 1/Z$ symbolically, independently of $\beta$. **So the mechanism does not fix the
coefficient** — but $r$ is a free dimensionless number, and imposing $r = 2Z$ trades one fitted number for
another. This is a reparametrisation, not a derivation.

*The freedom is not in the response.* One might hope the gap-dependence of the effective temperature on a
*rotating* worldline supplies $r$. We computed it. For the circular de Sitter worldline,
$D(s) = 4A^2\sinh^2(hs/2) - 4R^2\sin^2(ws/2) \geq s^2$ identically, so there is no real-axis pole; splitting off
the flat double pole gives $\mathcal{F}(-E) - \mathcal{F}(E) = E/2\pi$ for any stationary worldline, hence
$T_{\rm eff}(E) = E/\log[1 + E/2\pi\mathcal{F}(E)]$. The construction validates twice: $R \to 0$ returns
$T_{\rm GH} = H/2\pi$ to $5.8\times10^{-15}$, and at $w = 0$ the response is *exactly* thermal at Deser & Levin's
$\sqrt{a^2+H^2}/2\pi$ to $10^{-15}$–$10^{-17}$ across three radii — so the temperature Milgrom's balance *posits*
is here **obtained from a computed detector response**. Rotation does break the KMS condition, but only
quadratically in $v/c$: the gap-spread of $T_{\rm eff}$ is $0.166$ at $v/c = 0.5$ and falls monotonically to
$8.6\times10^{-7}$ at $v/c = 10^{-3}$, with spread$/(v/c)^2$ constant to within a factor $1.34$. At galactic
speeds the available freedom falls short of the required $r - 1 = 10.58$ by $1.2\times10^{7}$. **The response lane
is a null for the coefficient.**

## 5. Construction III: a vacuum scalar condensate

*Proposal.* Keep Einstein–Hilbert untouched; add a dimensionless scalar $\phi$; couple matter through an
effective metric $g^{\rm eff}_{\mu\nu} = g_{\mu\nu} + F(\phi,\nabla\phi)$; observe that the only scalar with units
of acceleration built from $\phi$ is $a_\phi = c^2\sqrt{\nabla_\mu\phi\nabla^\mu\phi}$; impose
$\nabla_\mu\phi\nabla^\mu\phi = G\rho_\Lambda/4c^2$. Since $\Lambda$ never appears, §2 does not bite.

*The dimensions work* — $a_\phi$ is a genuine acceleration and $G\rho_\Lambda/4c^2$ a genuine inverse area — and
the strategy of deriving field equations rather than a coefficient is the right shape. Three defects:

**Sign.** With signature $(-{+}{+}{+})$, any homogeneous $\phi(t)$ has
$\nabla_\mu\phi\nabla^\mu\phi = -\dot\phi^2/c^2 \leq 0$ — timelike and negative — while the proposal imposes a
positive value. A positive invariant requires a *spacelike* gradient, i.e. $\phi$ varying in space, which breaks
isotropy and selects a spatial direction. As written, $a_\phi$ is **imaginary in any homogeneous vacuum.** The
repair, $a_\phi = c^2\sqrt{-\nabla_\mu\phi\nabla^\mu\phi} = c|\dot\phi|$, costs nothing arithmetically:
$|\dot\phi| = \tfrac12/t_{\rm dyn} = 3.1228\times10^{-19}\ \mathrm{s^{-1}}$.

**Factor two.** In the proposal's own inertia law $a_{\rm eff} = \sqrt{a^2+a_\phi^2} - a_\phi$, the quantity
$a_\phi$ *is the floor*, and §1 gives $a_0 = 2k$. So $a_\phi = \tfrac12 c\sqrt{G\rho_\Lambda}$ delivers
$a_0 = c\sqrt{G\rho_\Lambda}$, i.e. $\kappa = 1$, **not** $\kappa = \tfrac12$; that requires
$\nabla_\mu\phi\nabla^\mu\phi = G\rho_\Lambda/16c^2$.

**No reduction.** $X_{\rm vac}$ is imposed. Free dimensionless numbers before: one. After: one. Evading §2 is
necessary, not sufficient.

*But the repaired construction is a ghost condensate, and that is not a criticism.* A linearly growing $\phi$ with
$\dot\phi = $ const is precisely a ghost condensate. Shift symmetry $\phi \to \phi + $ const **forbids** $V(\phi)$,
which answers the proposal's own question about broken symmetry: shift symmetry remains *unbroken* and protects the
flat potential, while the condensate spontaneously breaks boosts. For $\mathcal{L} = P(X)$ the FRW equation of
motion integrates to $a^3P'(\dot\phi) = $ const, so $P'(\dot\phi) \to 0$ as $a$ grows: $\dot\phi$ is **dynamically
selected by the extremum of $P$**, not imposed. And $u_\mu = \nabla_\mu\phi/\sqrt{-(\nabla\phi)^2}$ satisfies
$u\cdot u = -1$ identically, so the condensate *generates* the preferred unit timelike vector the modified-inertia
programme already carries as background structure. The remaining wall is that the condensate *amount* is free —
which is the leftover number above, under another name.

## 6. A systematic hazard: the $a_0$-versus-floor factor of two

Milgrom's balance contains the **floor** $k = a_0/2$, not $a_0$. Constructions I and III both attach their
derived coefficient to $a_0$, and we made the same error ourselves in an earlier draft, writing $Z$ where $2Z$ was
required — in the direction favouring our own coefficient, by exactly $2$. Three independent occurrences in a
single working day is enough to record it as a hazard rather than an accident: **state explicitly whether a
proposed mechanism delivers $a_0$ or the floor**, since the two differ by a factor that is comparable to the whole
disagreement between published proposals.

## 7. No standard local rate supplies $\tfrac14$

Given §2, the open route needs a mechanism whose only input is $\rho_\Lambda$ and whose output is
$\tfrac14 c\sqrt{G\rho_\Lambda}$. Writing candidate rates as $\kappa_{\rm loc}\sqrt{G\rho}$:

| candidate local rate | $\kappa_{\rm loc}$ | vs required $\tfrac14$ | % off |
|---|---|---|---|
| bare $\sqrt{G\rho}$ | 1.000000 | 4.0000 | 300.00 |
| free-fall $1/t_{\rm ff} = \sqrt{32G\rho/3\pi}$ | 1.842635 | 7.3705 | 637.05 |
| Jeans $\sqrt{4\pi G\rho}$ | 3.544908 | 14.1796 | 1317.96 |
| $\sqrt{G\rho/4\pi}$ | 0.282095 | 1.1284 | **12.84** |
| $\sqrt{G\rho/8\pi}$ | 0.199471 | 0.7979 | 20.21 |
| $\sqrt{3G\rho/8\pi} = 2/Z$ | 0.345494 | 1.3820 | 38.20 |
| $\pi^{-1}\sqrt{G\rho}$ | 0.318310 | 1.2732 | 27.32 |

The closest is **12.84%** away — wider than the **7.87%** separating the two published coefficients. There is no
near miss.

**And a methodological point that is load-bearing.** $\kappa = \tfrac12$ was fitted to rotation curves, not
predicted. Searching constructions until one reproduces $\tfrac14$ is reverse-engineering a fitted number, a
failure mode we have priced elsewhere: in a symbolic-regression audit of ours, chance alone hit 10 of 19 targets.
**Any candidate mechanism must therefore make an independent prediction beyond reproducing $\tfrac14$.**

## 8. The constructive result: $a_0(z)$ decides which floor

The fork of §2 is not aesthetic, and settling it requires no new mechanism. A local response to the vacuum
*density* gives $a_0 \propto \sqrt{\rho_{\rm DE}(z)}$ — for $w = -1$ exactly **constant**, and blind to the matter
content. A horizon floor tracks the actual expansion rate, $cH(z) = cH_0E(z)$ with
$E(z) = \sqrt{\Omega_m(1+z)^3 + \Omega_\Lambda}$, which **rises**:

| $z$ | local floor: $a_0(z)/a_0(0)$ | horizon floor: $a_0(z)/a_0(0)$ |
|---|---|---|
| 0 | 1.000000 | 1.000000 |
| 1 | 1.000000 | 1.782414 |
| 2 | 1.000000 | 3.014299 |
| 3 | 1.000000 | 4.537951 |

The two are degenerate only in a matter-free pure-$\Lambda$ universe. The local reading is therefore the
**more falsifiable** of the two: it forbids the rising branch that the horizon reading permits, and a measured
rise in $a_0$ with redshift would exclude it. This, rather than further mechanism search, is where the coefficient
question is decidable with existing and forthcoming data.

## 9. Conclusions

1. The coefficient problem reduces exactly to the **value of the floor** in Milgrom's balance, since
   $g_{\rm obs}^2 = g_{\rm bar}^2 + a_0g_{\rm bar}$ is identically that balance with $k = a_0/2$ and $a_0 = 2k$.
2. **Relabelling theorem.** $G\rho_\Lambda$ and $c^2\Lambda$ differ by exactly $8\pi$, so no combination of them
   can select a coefficient or exclude $cH_\Lambda$. Its boundary: a **single-scale** derivation taking
   $\rho_\Lambda$ as sole input is *not* excluded, and would exclude $cH_\Lambda$ automatically.
3. Three natural constructions fail — on dimensions and relabelling (§3), because the freedom is merely
   relocated (§4), and on a sign that makes the central invariant imaginary in a homogeneous vacuum (§5). The
   temperature class obeys $q = 2/r$ with $r$ free, and the detector-response route is a **null**, breaking KMS
   only at $\mathcal{O}(v^2/c^2)$ and falling short of the required freedom by $1.2\times10^{7}$.
4. En route, the response calculation **reproduces Deser & Levin's temperature to $10^{-15}$–$10^{-17}$** from a
   computed detector response at $w = 0$, so Milgrom's posited balance is confirmed rather than assumed.
5. The $a_0$-versus-floor **factor of two** is a systematic hazard, committed three times independently.
6. No standard local rate supplies $\tfrac14$; the closest is 12.84% away. Since $\kappa$ is fitted, mechanism
   search that targets $\tfrac14$ alone is reverse-engineering, and any candidate needs an independent prediction.
7. **The fork is observationally decidable.** $a_0 \propto \sqrt{\rho_{\rm DE}}$ is constant for $w = -1$;
   $a_0 \propto cH_0E(z)$ rises $4.54$-fold by $z = 3$. That is the test worth running.

$\kappa = \tfrac12$ remains **fitted, not derived**.

## 10. Data and code

All numerical and symbolic claims are reproduced by the self-checking scripts included in this record:
`mi_crossover_master_formula_2026.py` (14/14, §4), `mi_2Z_is_the_friedmann_root_2026.py` (8/8, §1–2),
`mi_circular_dS_response_2026.py` (8/8, §4), `mi_zeropoint_interference_audit_2026.py` (7/7, §3),
`mi_local_floor_target_2026.py` (6/6, §2, §7, §8),
`mi_scalar_condensate_proposal_audit_2026.py` (8/8, §5). Each exits non-zero on any failed internal check.
Repository: `https://github.com/carlzimmerman/zimmerman-formula`.

**Overlap declaration.** The closed form of §4 and the floor identification of §1 also appear in the companion
record DOI [10.5281/zenodo.21782600](https://doi.org/10.5281/zenodo.21782600), whose §3.3 they were written for,
and three of the six scripts above are shared with it; the material is repeated here only as far as §3, §5, §7 and
§8 require, and those four sections are new. Physical constants: $G = 6.67430\times10^{-11}$,
$c = 2.99792458\times10^{8}$, $\Lambda = 1.0908\times10^{-52}\ \mathrm{m^{-2}}$,
$\Omega_m = 0.311$, $\Omega_\Lambda = 0.689$.

**Provenance of the constructions.** The three constructions audited in §3 and §5 were proposed to the author
independently of this analysis. They are assessed here on their merits, and no credit is claimed for formulating
them; the audits, the theorem of §2, and the results of §4, §7 and §8 are the author's.
