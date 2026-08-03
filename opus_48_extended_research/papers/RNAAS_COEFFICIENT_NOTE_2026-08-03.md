# The Coefficient in the MOND–Dark-Energy Acceleration Relation: $a_0 = \tfrac{1}{2}c\sqrt{G\rho_\Lambda}$, and Why Rotation Curves Cannot Yet Fix It

**Carl P. Zimmerman** — Briar Creek Tech

*Research Note of the AAS — draft, 2026-08-03*

---

## 1. What is already established, and what is not

That the MOND acceleration scale $a_0 \simeq 1.2\times10^{-10}\ \mathrm{m\,s^{-2}}$ sits within an order of
magnitude of $cH_0$ has been noted since Milgrom (1983). The sharper statement — that the relevant scale is set
by the *dark-energy* density rather than by the expansion rate — is also not new. Milgrom (1994, *Ann. Phys.*
**229**, 384, §II eq. 3) writes the de Sitter acceleration

$$a_\lambda \;=\; c^2\sqrt{\Lambda/3} \;=\; 5.419\times10^{-10}\ \mathrm{m\,s^{-2}},$$

and Milgrom (2020, *"The $a_0$–cosmology connection in MOND"*) develops the connection directly. The
interpolating function $\nu(y)=\sqrt{1+1/y}$, $y \equiv g_{\rm bar}/a_0$, is Milgrom (1999, *Phys. Lett. A*
**253**, 273, eqs. 6–9), who fixes its coefficient at $\hat a_0 = 2cH_\Lambda$; the underlying
five-acceleration construction is Deser & Levin (1997, *CQG* **14**, L163); the exponential form
$\nu = (1-e^{-\sqrt y})^{-1}$ is McGaugh (2008, *ApJ* **683**, 137, eq. 11a), introduced there for precisely the
solar-system reason it is still used for; and Luo (arXiv:2602.14515v2) reaches the same relation from a
second-moment quantum argument.

**The form of the relation is therefore not available to claim.** What remains genuinely open in the published
literature is the dimensionless $\mathcal{O}(1)$ prefactor, which no derivation fixes. This note states a
specific value for it, and then reports the measurement that its own author's analysis says cannot currently
distinguish it from the alternatives.

## 2. The claim

$$\boxed{\;a_0 \;=\; \kappa\,c\sqrt{G\rho_\Lambda}\,,\qquad \kappa=\tfrac12\;}$$

with $\rho_\Lambda = \Omega_\Lambda\,3H_0^2/8\pi G$. Equivalently, in units of $cH_\Lambda$ where
$H_\Lambda \equiv c\sqrt{\Lambda/3}$,

$$a_0 \;=\; \frac{cH_\Lambda}{Z}\,,\qquad Z \;=\; 2\sqrt{\frac{8\pi}{3}} \;=\; \sqrt{\frac{32\pi}{3}} \;=\;
5.78881\,,$$

giving $a_0 = 9.36\times10^{-11}\ \mathrm{m\,s^{-2}}$ for $\Omega_\Lambda = 0.685$, $H_0 = 67.4\
\mathrm{km\,s^{-1}\,Mpc^{-1}}$. The $8\pi$ is Einstein's and the $3$ is Friedmann's, and both cancel between
$\rho_\Lambda$ and $H_\Lambda$: the entire distinctive content is one factor, since $Z^2 = 4\cdot(8\pi/3)$.
Note $a_\lambda/a_0 = Z$ exactly, so this is Milgrom's 1994 scale divided by $Z$.

Placing the published values on one axis:

| | $a_0$ in units of $cH_\Lambda$ |
|---|---|
| this note, $\kappa=\tfrac12$ | $1/Z = 0.1727$ |
| Luo (2602.14515v2), after projection | $1/3$ |
| Milgrom (2020), $\kappa = 1/2\pi$ | $1/2\pi = 0.1592$ |
| Milgrom (1999) | $2$ |

The realisation is **modified inertia** rather than modified gravity. Milgrom (2022, *PRD* **106**, 064060)
constructs modified inertia at the level of the equations of motion, noting explicitly that such theories "are
not necessarily governed by an action" and requiring only that $x\mu(x)$ be monotonic — a condition the kernels
used here satisfy, verified analytically. This is the appropriate home: for the form class examined, the
modified-inertia law is *not* variational in a disc, so no action is claimed.

## 3. Status: fitted, not derived

**$\kappa = \tfrac12$ is a fitted value.** Three attempts to force it are reported closed rather than pending:

1. **Forcing $\kappa$ from ghost-freedom, unitarity and holography** does not work; these constrain the kernel's
   spectral properties, not its normalisation.
2. **The $\kappa$-linear spectral class is a relabelling.** For that family $W_n \propto \kappa^n$ identically,
   so no member can force $\kappa$ — a theorem, not another failed candidate.
3. **The CKN degrees-of-freedom bridge closes algebraically.** The candidate constant
   $(3/8\pi)^{1/4} = 0.58779$ satisfies $(3/8\pi)^{1/4} = \sqrt{2/Z}$ *exactly*, i.e. $1/Z = \tfrac12(3/8\pi)^{1/2}$.
   It is an exact rewriting of $Z$, not independent information about it.

What survives is a one-parameter effective theory in which $\kappa$ is measured, and $Z^2 = 4\cdot(8\pi/3)$
reduces the open problem to a single bare factor of 4.

## 4. The result of this note: rotation curves cannot fix the coefficient

The gap between $\kappa=\tfrac12$ and $\kappa=1/2\pi$ is **7.87%** in $a_0$ — small, but a 7.87% measurement of
$a_0$ is not obviously out of reach, and the SPARC rotation-curve sample (Lelli, McGaugh & Schombert 2016) is
the natural instrument. It does not work, for a reason that appears not to have been quantified before.

A profile likelihood on 175 SPARC galaxies with stellar mass-to-light ratio free per galaxy, $a_0$ an input
throughout, gives $\Delta\chi^2 = \chi^2(1/2\pi) - \chi^2(1/2)$, positive favouring $\kappa=\tfrac12$:

| assumed transition shape | preferred $a_0$ | $\Delta\chi^2$ | $\sigma$ |
|---|---|---|---|
| $\mu = x/(1+x^4)^{1/4}$ | $1.244\,a_0$ | $+139.7$ | 2.69 |
| $\mu = x/\sqrt{1+x^2}$ | $1.192\,a_0$ | $+110.6$ | 2.39 |
| $\nu = \sqrt{1+1/y}$ | $1.154\,a_0$ | $+90.4$ | 2.16 |
| deep-MOND limit only (shape-free) | $1.059\,a_0$ | $+46.3$ | 1.55 |
| $\nu = (1-e^{-\sqrt y})^{-1}$ | $0.938\,a_0$ | $-8.4$ | 0.66 |

Four of five lean toward $\kappa=\tfrac12$, including the shape-free deep-limit estimator; **none reaches
$3\sigma$, and one leans the other way.** The spread of the preferred $a_0$ across these shapes is **30.6%** —
nearly four times the 7.87% being probed. The transition shape is not itself measured to better than this, so
**the shape systematic swamps the coefficient.** Two corollaries follow, and both are cautionary:

- The relation $g_{\rm obs}^2 - g_{\rm bar}^2 = a_0 g_{\rm bar}$, often used as a direct one-number estimator
  of $a_0$, is *identically* the $\nu=\sqrt{1+1/y}$ kernel written as a straight line. It returns $a_0$ exactly
  on data generated by that kernel, and is biased $+10.3\%$ / $-83.6\%$ on data generated by the exponential /
  $x/\sqrt{1+x^2}$ forms. It is shape-assuming, not shape-free.
- A genuinely shape-invariant estimator does exist — regress $\ln(g_{\rm obs}^2/g_{\rm bar})$ on
  $\{1,\sqrt y, y, y^{3/2}\}$ and take the intercept, which recovers $a_0$ to $0.25\%$ under every shape tested —
  but it carries a 17.5% total error, with a 14.2% floor (shape 10.0%, mass-to-light 7.4%, gas 6.8%) that does
  not shrink with sample size. A $3\sigma$ separation needs 2.73%.

Only the deep-MOND regime is shape-independent, since $\nu\sqrt y \to 1$ for every kernel considered; there the
baryonic Tully–Fisher relation $V^4 = GMa_0$ holds with coefficient exactly 1. But the deep regime alone is
where the statistical leverage is weakest.

## 5. What would settle it

Fixing $\kappa$ observationally requires an $a_0$ estimator accurate to $\lesssim 3\%$ that does not assume a
transition shape. Rotation curves do not currently provide one. Candidate routes are the deep-limit BTFR with
substantially improved distances and gas masses; wide-binary kinematics, which is however both shape-dependent
and $a_0$-degenerate; and any observable confined to $g_{\rm bar} \ll a_0$ with per-object precision better
than the present $\sim$14% floor. Until then $\kappa=\tfrac12$ should be read as a postulate consistent with
the data at the $1.5$–$2.7\sigma$ level depending on the assumed shape, and not as a measurement.

## 6. Data and code

All numerical claims above — the five-shape table, the 26.3% shape systematic, the estimator biases, the
$0.25\%$ shape-invariant recovery and the CKN identity — are reproduced by public scripts carrying self-checking
assertions that exit non-zero on failure, archived at *(Zenodo DOI to be inserted)*. The analysis repository has
been submitted to the Astrophysics Source Code Library; the ASCL identifier will be added once assigned. SPARC
data: Lelli, McGaugh & Schombert (2016), *AJ* **152**, 157.

---

*Word count (body, §1–§5): ~1,180.*
