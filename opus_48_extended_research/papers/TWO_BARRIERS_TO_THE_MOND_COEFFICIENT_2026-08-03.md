# Two Barriers to the MOND Acceleration Coefficient: the de Sitter–Unruh Balance Is Orbital-Invariant at $a_0 = 2cH_\Lambda$, and Rotation-Curve Determinations of $a_0$ Are Definition-Limited at 30%

**Carl P. Zimmerman** — Briar Creek Tech

*Draft, 2026-08-03. All numerical claims are reproduced by public self-checking scripts; see §6.*

---

## Abstract

The MOND acceleration scale $a_0 \simeq 1.2\times10^{-10}\ \mathrm{m\,s^{-2}}$ is numerically close to $cH_\Lambda$,
and several authors have proposed that it is *set* by the cosmological constant. The relation's **form** is
established — Milgrom (1994) writes the de Sitter acceleration $a_\lambda = c^2\sqrt{\Lambda/3}$, and Milgrom
(1999, 2020) develops the connection — but its dimensionless $\mathcal{O}(1)$ **coefficient** is not derived by
any published argument. We report two independent barriers to fixing it, one theoretical and one observational,
and we quantify both.

**First**, we compute the Unruh–DeWitt response for a **circular** worldline in de Sitter space and extract the
MOND crossover coefficient $q$ defined by $a_0 = q\,cH_\Lambda$. Milgrom's (1999) balance uses a *hyperbolic*
worldline and gives $q = 2$; since a circular orbit is never hyperbolic (its Frenet torsion satisfies
$|a|/\tau_1 = v/c$ exactly), that derivation is scope-limited to linear acceleration, while galaxies are orbits.
We find $q = 2$ **exactly** on orbits, for two independent reasons both forced by the single identity
$A^2h^2 - R^2w^2 = 1$: the short-time correlator depends only on $a_5^2 = a^2 + H^2$, which holds for *any*
worldline on the hyperboloid; and the full-response orbital correction is an $a$-**independent** rescaling
(verified to $10^{-16}$ over five decades in $a/H$) which cancels identically in the crossover ratio. The
mechanism therefore returns Milgrom's coefficient and cannot be made to yield a smaller one: the gap to
$q = \sqrt{3/32\pi}\,\cdot 2 = 0.173$ (i.e. $a_0 = \tfrac12 c\sqrt{G\rho_\Lambda}$) is a factor $11.6$, not a
near miss.

**Second**, we show that rotation-curve determinations of $a_0$ are limited not by data quality but by
**definition**. Profiling the SPARC sample (Lelli, McGaugh & Schombert 2016) with the mass-to-light ratio free
per galaxy, the preferred $a_0$ spans **30.6%** across five admissible interpolation shapes — nearly four times
the 7.87% separating the two published coefficient proposals. We identify the mechanism: the likelihood anchors
on a single *deep* acceleration, at boost $\nu \approx 3.97$ ($y \approx 0.06$), where the five kernels agree to
**1.14%**; the knee is emphatically *not* the anchor (correcting at $\nu = \sqrt2$ over-corrects by $3.4\times$).
The 30.6% is a units conversion between kernels, already **diluted $5.5\times$** by SPARC's 1.57 decades of
coverage in $y$ — so additional data at one acceleration cannot reduce it. Crucially, the kernels are *not*
degenerate: after optimal $a_0$ rescaling they still differ by 0.050 dex, 46% of the observed scatter. The
barrier is therefore finite rather than definitional — it is removed by measuring the interpolation **shape**,
not by measuring $a_0$ more precisely.

Both barriers point the same way. Fixing the kernel eliminates the systematic entirely and yields a definite
verdict on the coefficient; we tabulate it for five shapes. The two dominant obstacles to testing
$a_0 = \tfrac12 c\sqrt{G\rho_\Lambda}$ — the kernel choice (30.6%) and the choice of which cosmological density
the horizon term tracks (20.9%) — both **exceed** the 7.87% being measured, and both are settleable by argument
at zero observational cost.

---

## 1. What is established, and what is not

That $a_0 \sim cH_0$ has been noted since Milgrom (1983). The sharper claim — that the relevant density is the
*dark-energy* density — is also not new: **Milgrom (1994, *Ann. Phys.* 229, 384, §II eq. 3)** writes

$$a_\lambda \;=\; c^2\sqrt{\Lambda/3} \;=\; 5.419\times10^{-10}\ \mathrm{m\,s^{-2}},$$

and **Milgrom (2020)**, *"The $a_0$–cosmology connection in MOND"*, develops it directly. The interpolating
function $\nu(y) = \sqrt{1+1/y}$ with $y \equiv g_{\rm bar}/a_0$ is **Milgrom (1999, *Phys. Lett. A* 253, 273,
eqs. 6–9)**, who fixes its coefficient at $\hat a_0 = 2cH_\Lambda$; the underlying five-acceleration
construction is **Deser & Levin (1997, *CQG* 14, L163)**. The exponential form $\nu = (1-e^{-\sqrt y})^{-1}$,
used here as one of five test shapes, is **McGaugh (2008, *ApJ* 683, 137, eq. 11a)**, introduced there for the
solar-system reason it is still used for. A second-moment route to the same relation is **Luo
(arXiv:2602.14515v2)**; his acceleration composition
$a_{\rm eff}^2 = (a_N + a_{\rm bg})^2 - a_{\rm bg}^2$ is *identically* the $\nu = \sqrt{1+1/y}$ kernel under
$a_0 = 2a_{\rm bg}$.

**So the form of the relation is not available to claim.** What remains open is the dimensionless coefficient,
and the published proposals differ:

| | $a_0$ in units of $cH_\Lambda$ |
|---|---|
| Milgrom (1999), hyperbolic dS–Unruh balance | $2$ |
| Luo (2602.14515v2), after isotropy projection | $1/3$ |
| Milgrom (2020), $\kappa = 1/2\pi$ | $1/2\pi = 0.1592$ |
| this framework, $a_0 = \tfrac12 c\sqrt{G\rho_\Lambda}$ | $1/Z = 0.1727$, $Z = 2\sqrt{8\pi/3}$ |

This paper reports two barriers to deciding among them. It does **not** derive a coefficient; the value
$\kappa = \tfrac12$ used as a reference throughout remains **fitted, not derived**.

## 2. The orbital de Sitter–Unruh coefficient

### 2.1 Setup and the scope problem

Milgrom's (1999) balance posits inertia proportional to the Unruh–de Sitter temperature above the
Gibbons–Hawking floor. On a **hyperbolic** worldline, Deser & Levin's embedding gives
$T \propto \sqrt{a^2 + a_\lambda^2}$, so

$$I(a) \;\propto\; \sqrt{a^2+H^2} - H \;\longrightarrow\; \frac{a^2}{2H}\quad (a \ll H),$$

which is MOND with crossover $a_* = 2H$, i.e. $q = 2$. But a circular orbit is never hyperbolic. Its Frenet
torsion is $\tau_1 = ARhw(h^2+w^2)/a_5 \simeq a/v$, so $|a|/\tau_1 = v/c$ exactly, and rotating detectors are not
thermal (Letaw 1981; Bell & Leinaas 1983). Galaxies are orbits. The coefficient must therefore be recomputed on
the worldline class the phenomenology actually occupies.

### 2.2 The correlator

For $\rho = R$, $\phi = \Omega t$ in the de Sitter static patch, embedded in $M^5$, with
$N^2 = 1 - H^2R^2 - R^2\Omega^2$, $A^2 = H^{-2} - R^2$, $h = H/N$, $w = \Omega/N$, we derive (twice, by
independent routes — a GEMS/embedding calculation and a conformal-chart calculation)

$$(\Delta X)^2(s) \;=\; 4R^2\sin^2\!\tfrac{ws}{2} \;-\; 4A^2\sinh^2\!\tfrac{hs}{2},\qquad
W(s) = \frac{1}{4\pi^2\,(\Delta X)^2(s-i\epsilon)},$$

with the exact identities $A^2h^2 - R^2w^2 = 1$, $a_5^2 = A^2h^4 + R^2w^4$, and $a^2 = a_5^2 - H^2$ (the last
holding for **any** worldline on the hyperboloid, since $X\!\cdot\!X = H^{-2}$ forces the normal component of the
5-acceleration to be exactly $H$). The static limit reduces to a pure hyperbolic worldline with
$\alpha = \sqrt{a^2+H^2}$, reproducing Deser & Levin's temperature; a KMS check confirms exact thermality there
and confirms that **strict thermality fails for every $\Omega \neq 0$**, so an effective temperature for orbits is
necessarily energy-gap dependent.

### 2.3 $q = 2$, exactly

Write the interval as the hyperbolic part times a correction,
$(\Delta X)^2 = -4A^2\sinh^2(hs/2)\,[1-\varepsilon(s)]$, with
$\varepsilon(s) = (R^2/A^2)\sin^2(ws/2)/\sinh^2(hs/2)$. All orbital content sits in $\varepsilon$. Using
$A^2h^2 = 1 + R^2w^2$,

$$\sup_s \varepsilon \;=\; \frac{R^2w^2}{1+R^2w^2} \;=\; \frac{\gamma^2v^2}{1+\gamma^2v^2},$$

which is **independent of $a$**. We verify this to one part in $10^{16}$ at $a/H = 10^{-2}, 1, 10^3$. An
$a$-independent factor is a uniform rescaling of $I(a)$, and a uniform rescaling **cancels identically** in the
crossover ratio $a_* = c_1/c_2$. Hence $q$ is orbital-invariant, with residual $2\times10^{-31}$ (the arithmetic
floor). The second-moment reading gives the same answer for an independent reason: it depends only on
$a_5^2 = a^2+H^2$, exact for any worldline.

**Consequence.** The mechanism returns $q = 2$ — a factor $11.6$ from the $q = 1/Z = 0.173$ required by
$a_0 = \tfrac12 c\sqrt{G\rho_\Lambda}$, and $12.6$ from Milgrom (2020)'s $1/2\pi$. This is not a near miss that
better numerics could close, and the closure is uniform: no choice of energy gap, inertia functional, or orbital
speed can move it. We note the irony that the torsion obstruction, which correctly identifies Milgrom's
derivation as scope-limited, turns out to be **harmless for the coefficient** — it matters for whether the law
admits an action, not for $q$.

**Prior art.** The circular-worldline response in de Sitter is partial prior art: **Hari K. & Kothawala
(*PRD* 109, 104073, 2024; arXiv:2307.16413)** treat stationary trajectories with uniform acceleration and
rotation in 4D dS/AdS numerically and perturbatively, stating they could not obtain a closed form; **Bunney &
Louko (arXiv:2406.17643)** treat $2+1$ dS in a small-$\Lambda$ expansion. We searched for and did not find any
prior extraction of a MOND coefficient from an *orbital* detector response.

## 3. Rotation curves are definition-limited, not data-limited

### 3.1 The 30.6%

We profile 175 SPARC galaxies with $\Upsilon_{\rm disk}$ free per galaxy ($\Upsilon_{\rm bulge} = 1.4\,
\Upsilon_{\rm disk}$), $a_0$ an input, and the intrinsic scatter calibrated to $\chi^2/{\rm dof} = 1$, under five
admissible interpolation shapes. The preferred $a_0$, in units of $\tfrac12 c\sqrt{G\rho_\Lambda} = 9.361\times
10^{-11}$:

| shape | preferred $a_0$ | $\nu(1)$ |
|---|---|---|
| $\mu = x/(1+x^4)^{1/4}$ | $1.244$ | $1.128$ |
| $\mu = x/(1+x^3)^{1/3}$ | $1.234$ | $1.174$ |
| $\mu = x/\sqrt{1+x^2}$ | $1.192$ | $1.272$ |
| $\nu = \sqrt{1+1/y}$ | $1.154$ | $1.414$ |
| $\nu = (1-e^{-\sqrt y})^{-1}$ | $0.938$ | $1.582$ |

The spread is **30.6%** and it is perfectly anti-correlated with the knee boost $\nu(1)$ ($r = -0.94$): a broader
knee needs a smaller $a_0$ to produce the same boost where the data sit.

### 3.2 The anchor is deep, not at the knee

If the likelihood constrained a single boost value $\nu_{\rm anchor}$, then $a_0^{\rm pref}\times y_*$ would be
kernel-invariant, where $y_*$ is each kernel's argument at that boost. Testing $\nu_{\rm anchor} = \sqrt2$ (the
knee) **over-corrects by $3.4\times$**, inflating the spread from 32.6% to 111.6%. Scanning
$\nu_{\rm anchor}$, the product is most nearly conserved at

$$\nu_{\rm anchor} = 3.97\qquad (y \approx 0.06,\ \text{deep MOND}),$$

where the residual spread is **1.14%** — a $28.6\times$ compression. The five kernels therefore agree on one
physical acceleration and differ only in what to call it in units of their own $a_0$.

### 3.3 Already diluted, so more data does not help

A single-point anchor would force a **181%** spread in $a_0$; the observed spread is 33%. The
**$5.5\times$ dilution** is SPARC's coverage: 3389 points spanning 1.57 decades in $y$ (16–84%: 0.050–1.862,
median 0.198), over which the likelihood averages the kernel difference. The 30.6% is thus already the
$y$-averaged residual, and additional measurements at one acceleration cannot reduce it.

### 3.4 But the kernels are not degenerate — which is the way out

Rescaling $a_0$ does **not** make the shapes equivalent. Fitting each kernel's best $a_0$ to the best-fit
$\nu = (1-e^{-\sqrt y})^{-1}$ curve over SPARC's own $y$-range leaves a worst-case residual of **0.050 dex** —
46% of the 0.108 dex observed scatter, not a tenth of it. The shapes are distinguishable by data. Reducing the
30.6% therefore requires **measuring the interpolation shape**, which needs of order $(0.108/0.050)^2 \approx 5$
times the current effective sample — large but finite, and not a definitional obstruction.

### 3.5 Fix the kernel and the coefficient gets a verdict

With the shape fixed there is no shape systematic. Writing $\Delta\chi^2 = \chi^2(1/2\pi) - \chi^2(1/2)$,
positive favouring $\kappa = \tfrac12$:

| shape fixed | $\Delta\chi^2$ | $\sigma$ | verdict |
|---|---|---|---|
| $x/(1+x^4)^{1/4}$ | $+139.7$ | 2.69 | favours $\kappa=\tfrac12$ |
| $x/(1+x^3)^{1/3}$ | $+133.7$ | 2.63 | favours |
| $x/\sqrt{1+x^2}$ | $+110.6$ | 2.39 | favours |
| $\sqrt{1+1/y}$ | $+90.4$ | 2.16 | favours |
| $(1-e^{-\sqrt y})^{-1}$ | $-8.4$ | 0.66 | disfavours |

Four of five favour $\kappa = \tfrac12$, including the shape-free deep-limit estimator ($+46.3$, 1.55$\sigma$);
none reaches $3\sigma$. **The kernel choice is the coefficient question.**

## 4. Where the barrier actually is

Against the 7.87% separating $\kappa = \tfrac12$ from $1/2\pi$:

- the **kernel** choice contributes 30.6% — $3.9\times$ the gap;
- the **footing** choice (whether the horizon term tracks $\rho_{\rm DE}$ or $\rho_{\rm total}$) contributes
  20.9% — $2.7\times$;
- the best **shape-invariant** estimator we could construct reaches 14.2% (an $N$-independent floor of shape
  10.0%, mass-to-light 7.4%, gas calibration 6.8%) — $1.8\times$.

Both dominant obstacles are theoretical choices, settleable by argument at no observational cost. Two
constraints on the kernel already exist and pull in the same direction: solar-system ephemerides require the
Newtonian approach exponent $p \gtrsim 2.3$ in $\nu - 1 \sim C y^{-p}$, and analyticity of Milgrom's (1994) class-(34)
kinetic function at the Newtonian point requires $p/2 \in \mathbb{Z}_{\geq 2}$, hence $p \geq 4$ — so
**analyticity implies the ephemeris bound**, and $p = 4$ is the minimal fully admissible power-law member. It is
also the most coefficient-favourable shape in Table 3.5. Against that: $p = 4$ drives the wide-binary velocity
ratio sub-Newtonian ($\gamma_v = 0.998$) and worsens a five-constraint Milky Way fit to $4.47\sigma$. That
tension is real and unresolved.

## 5. Conclusions

1. The de Sitter–Unruh balance is **orbital-invariant** and returns $q = 2$ exactly, for two independent reasons
   both traceable to $A^2h^2 - R^2w^2 = 1$. The coefficient $a_0 = \tfrac12 c\sqrt{G\rho_\Lambda}$ is a factor
   11.6 away and is **not derivable from this mechanism**.
2. Rotation-curve determinations of $a_0$ carry a **30.6%** shape systematic, which is a units conversion about a
   *deep* anchor ($\nu \approx 3.97$), already diluted $5.5\times$ by the sample's $y$-coverage, and reducible only
   by measuring the interpolation shape — for which the required leverage is finite ($\sim5\times$ the effective
   sample).
3. Consequently the barrier to fixing the MOND coefficient is presently **theoretical rather than
   observational**, and the largest single lever is deciding the interpolation function on independent grounds.

Nothing here derives a coefficient, and $\kappa = \tfrac12$ remains fitted.

## 6. Data and code

All numerical claims are reproduced by public scripts carrying self-checking assertions that exit non-zero on
failure: `mi_orbital_unruh_gems_2026.py` (38/38), `mi_orbital_unruh_conformal_2026.py` (31/31),
`mi_orbital_unruh_q_2026.py` (6/6), `mi_routeA_a0_estimator_invariance_2026.py` (7/7),
`mi_p4_kernel_pricing_2026.py` (15/15), `mi_shape_systematic_mechanism_2026.py` (6/6),
`mi_routeA_admissibility_audit_2026.py` (31/31). Repository:
`https://github.com/carlzimmerman/zimmerman-formula`. Archive DOI: *(to be inserted.)* SPARC data: Lelli,
McGaugh & Schombert (2016), *AJ* 152, 157.
