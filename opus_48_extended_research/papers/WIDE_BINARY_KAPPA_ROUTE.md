# Measuring the MOND coefficient with wide binaries and a directly-measured Galactic acceleration

## An error budget, a requirement sheet, and the case for a second independent route

**Carl P. Zimmerman**
Briar Creek Tech

*Version 1 (2026-08-09).*

---

## Abstract

The framework's central claim is $a_0 = \kappa\,c\sqrt{G\rho_\Lambda}$ with $\kappa$ a pure number.
Every attempt to *derive* $\kappa$ reduces to a relabelling, so $\kappa$ must be *measured*. The
sharpest existing measurement, from the SPARC baryonic Tully–Fisher intercept, gives
$\kappa = 0.465\pm0.076$ and carries a hard floor at $3.9\%$ in $a_0$ set by the helium correction,
HI self-absorption and CO-dark molecular gas — independent of sample size, distances or stellar
populations. That floor caps the discrimination of $\kappa=\tfrac12$ from the nearest rival simple
value $1/\sqrt3$ at $\approx4\sigma$.

This paper prices a second route: the wide-binary velocity boost $\gamma_v$ combined with a
**directly-measured** Galactic acceleration $g_{\rm ext}$ from pulsar timing. Three results.

**(i)** An earlier claim of the author's — that this route is free of any mass-to-light ratio — is
**retracted**. $\gamma_v$ is defined against $v_{\rm Newt}=\sqrt{GM_{\rm tot}/s}$, so
$\gamma_v\propto M_{\rm tot}^{-1/2}$ exactly and a stellar mass enters. What survives is a claim about
the *kind* of calibration: the main-sequence mass–luminosity zero point is fixed **dynamically**, on
eclipsing binaries in the unambiguously Newtonian regime, so it is MOND-independent and tighter than
population synthesis.

**(ii)** The central obstacle is arithmetic. $\gamma_v = \sqrt{\nu(g_{\rm ext}/a_0)}$ is a *weak*
function of $a_0$: $d\ln\gamma_v/d\ln a_0 = 0.1155$ at the solar-neighbourhood field, so
$\sigma(a_0)/a_0 = 8.66\,\sigma(\gamma_v)/\gamma_v$. **Every $\gamma_v$ error is amplified $8.7\times$.**
But an asymmetry runs the other way: because $\gamma_v$ depends only on the *ratio*
$y=g_{\rm ext}/a_0$, an error in $g_{\rm ext}$ propagates **1:1 and is not amplified** — so pulsar
timing at a few percent suffices, with no Milky Way mass model.

**(iii)** What binds today is neither the masses nor $g_{\rm ext}$: the frozen pre-registration's own
$\sigma_{\rm sys}=0.0206$ already caps $a_0$ at $14.7\%$, and DR4 as frozen gives $20\%$ — worse than
SPARC. **DR4 tests which arm the framework is in; it does not measure the coefficient.**

The case for building the route is **independence, not superiority.** Its floor terms — the
mass–luminosity zero point and Gaia systematics — share nothing with SPARC's. Two independent $\approx4\%$
measurements combine to $2.79\%$ in $a_0$, i.e. $\sigma(\kappa)=0.014$, separating $\tfrac12$ from
$1/\sqrt3$ at $\mathbf{5.5\sigma}$. **Neither route reaches $5\sigma$ alone** ($3.97\sigma$ and
$3.87\sigma$). That is the entire argument.

Every number is produced by `mi_wb_gext_kappa_route_2026.py` (15/15 checks, exits non-zero on failure,
negative controls included).

---

## 1. Why the coefficient has to be measured

The framework fixes the *form* of the MOND scale. The uniqueness theorem is short: the only
acceleration constructible from $(G,c,\rho)$ is $\xi\,c\sqrt{G\rho}$, because the exponent matrix is
nonsingular with determinant 2. Admitting $\hbar$ destroys uniqueness, so the theorem constrains the
input set rather than being a triviality of dimensional analysis.

The *number* is another matter. Every route that ties $a_0$ to $\Lambda$ using only $\Lambda$, $G$ and
$c$ produces the same algebra with a convention-dependent residue: $a_0 = m_{\rm cond}/(4\sqrt{\pi})$
is algebraically identical to $\tfrac12\sqrt{G\rho_\Lambda}$ and to $Z=2\sqrt{8\pi/3}$, and the residue
changes between the reduced and non-reduced Planck mass. That is a relabelling, not a derivation.

The de Sitter–Unruh construction does better than that — it **derives the interpolation function
exactly**, $\nu=\sqrt{1+1/y}$, which is Milgrom (1999) eq. 9 — but it simultaneously forces
$a_0=2cH_\Lambda$, which SPARC excludes at $15.6\sigma$, and the construction is rigid at every step
(the power is forced to $n=1$ by the two MOND limits, the baseline to the ambient de Sitter
temperature, the normalisation to unity by the Newtonian limit). **So the heuristic cannot be cited as
support for $\kappa=\tfrac12$.**

A graviton-bath calculation gives the right *form* — the de Sitter horizon entropy cancels the Planck
suppression exactly, $S_{\rm dS}GH^2=\pi$ identically, leaving $\kappa^2=8\pi\epsilon_{\rm tot}$ with
$\epsilon_{\rm tot}$ a pure number — but not the number: five defensible readings span
$\kappa=0.013$–$2.047$, and the one landing on $\tfrac12$ is structurally invalid, since
$X=h_{\mu\nu}u^\mu u^\nu=h_{00}$ vanishes in TT gauge for a static worldline.

**Hence: measure it.**

---

## 2. The estimator, and what enters it

For a wide binary of total mass $M_{\rm tot}$ and separation $s$, define

$$\gamma_v \;\equiv\; \frac{v_{\rm obs}}{v_{\rm Newt}}, \qquad v_{\rm Newt}=\sqrt{\frac{GM_{\rm tot}}{s}} .$$

In an AQUAL-type external-field effect the boost is isotropic, so

$$\gamma_v \;=\; \sqrt{\nu\!\left(y_{\rm ext}\right)}, \qquad y_{\rm ext}=\frac{g_{\rm ext}}{a_0},$$

with $\nu$ the framework's in-force Route A kernel $\nu(y)=1/(1-e^{-\sqrt{y}})$ (Amendments 8/9). At
$g_{\rm ext}=1.8\times10^{-10}\,$m s$^{-2}$ this gives $y_{\rm ext}=1.923$ and $\gamma_v=1.155$; the
registered target on the full nonlinear treatment is $\gamma_v=1.2139$ (canonical footing) / $1.2592$
(alt), registered as *provisional* pending the full AQUAL-EFE solve.

**Inverting for $a_0$ needs two inputs: $\gamma_v$ and $g_{\rm ext}$.** They behave very differently,
and §4 is about that.

### 2.1 A retraction

The author previously described this route as having *"no mass-to-light ratio anywhere in the chain."*
**That is false.** From the definition, $\gamma_v \propto M_{\rm tot}^{-1/2}$ exactly — doubling the
assumed mass changes $\gamma_v$ by $1/\sqrt2$, verified symbolically — and for Gaia pairs
$M_{\rm tot}$ is photometric. A stellar mass scale enters, and it enters at half strength in the log.

What survives is weaker and still worth having:

| | mass calibration | character |
|---|---|---|
| SPARC galaxies | $\Upsilon$ from population synthesis | a **model**; $\approx17\%$ systematic |
| wide binaries | main-sequence mass–luminosity relation | zero point fixed **dynamically** on eclipsing binaries in the unambiguously Newtonian regime — **MOND-independent**, and tighter |

The distinction is not cosmetic. A population-synthesis $\Upsilon$ depends on an assumed IMF, star
formation history, metallicity and dust treatment. An eclipsing-binary mass is Kepler's third law
applied at $g\sim10^{5}\,a_0$, where no one disputes the dynamics — so the calibration cannot be
contaminated by the effect being tested.

---

## 3. The central obstacle: $\gamma_v$ is a weak function of $a_0$

Differentiating,

$$\frac{d\ln\gamma_v}{d\ln a_0}\Big|_{y_{\rm ext}=1.92} \;=\; 0.1155 \qquad\Longrightarrow\qquad
\boxed{\;\frac{\sigma(a_0)}{a_0} \;=\; 8.66\,\frac{\sigma(\gamma_v)}{\gamma_v}\;}$$

The amplification is robust: $8.25\times$ to $9.68\times$ across $g_{\rm ext}=1.6$–$2.3\times10^{-10}$.
It is pure arithmetic — a property of the kernel's shape at the solar-neighbourhood field — and no
observational improvement removes it.

Propagating the mass term, with $\sigma(\gamma_v)/\gamma_v = \tfrac12\,\sigma_M/M$:

| $\sigma_M/M$ | $\sigma(\gamma_v)/\gamma_v$ | $\sigma(a_0)/a_0$ |
|---|---|---|
| 5% | 2.50% | **21.6%** |
| 2% | 1.00% | 8.7% |
| 1% | 0.50% | 4.3% |
| 0.5% | 0.25% | 2.2% |

**A 5% mass zero point alone caps $a_0$ at $22\%$.** This route needs its mass scale at the *percent*
level — which eclipsing-binary calibration can plausibly reach and population synthesis cannot. Note
that the *scatter* of the mass–luminosity relation averages down as $N^{-1/2}$ and is negligible at any
realistic $N$; it is the **zero point** that matters, and zero points do not average.

---

## 4. The asymmetry, and it runs in our favour

Because $\gamma_v$ depends only on the ratio $y=g_{\rm ext}/a_0$, a fractional error $\delta$ in
$g_{\rm ext}$ is *exactly* equivalent to a fractional error $-\delta$ in $a_0$. Verified: a $+3\%$
shift in $g_{\rm ext}$ and a $-3\%$ shift in $a_0$ give identical $\gamma_v$ to machine precision.
Therefore

$$\frac{\sigma(a_0)}{a_0}\bigg|_{g_{\rm ext}} = \frac{\sigma(g_{\rm ext})}{g_{\rm ext}} \qquad
\textbf{1:1, not amplified.}$$

Quantitatively: a $4\%$ error in $g_{\rm ext}$ costs $4\%$ in $a_0$, while a $4\%$ error in $\gamma_v$
costs $35\%$ — a factor $8.7$ asymmetry. A negative control confirms this is a property of the ratio
structure and not a triviality: a mass error does *not* map onto an $a_0$ error the same way.

**This is the structural advantage of the route.** A directly-measured Galactic acceleration — pulsar
timing, with no Milky Way baryonic mass model anywhere — needs only to *match* the target precision,
not beat it by $8.7\times$. The solar-neighbourhood Galactic field is
$\approx2\times10^{-10}\,$m s$^{-2}$, i.e. $\approx2\,a_0$: squarely in the transition region, which is
exactly where a MOND-scale measurement wants to sit.

---

## 5. What binds today, and it is not the masses

The frozen pre-registration carries $\sigma_{\rm fit}=0.019$ and $\sigma_{\rm tot}=0.028$ at
$N=30{,}000$, implying $\sigma_{\rm sys}=0.0206$. Amplified at $8.66\times$ against
$\gamma_v=1.2139$:

| term | $\sigma(\gamma_v)/\gamma_v$ | $\sigma(a_0)/a_0$ |
|---|---|---|
| statistical | 1.57% | 13.6% |
| **systematic** | 1.69% | **14.7%** |
| total | 2.31% | **20.0%** |

**The registration's own systematic budget already caps $a_0$ at $14.7\%$, before any mass
consideration** — and DR4 as frozen gives $20\%$, *worse* than SPARC's $16.2\%$.

This is worth stating without hedging: **DR4 tests the arm, not the coefficient.** Its power is in
discriminating a Newtonian result from the framework's (evidence against at $4.7$–$7.1\sigma$ if
$\gamma_v=1$) and, since Amendment 9, in distinguishing modified inertia from modified gravity — the
two targets are disjoint at $2.68\sigma$. Neither of those is a measurement of $\kappa$.

---

## 6. Requirement sheet for $a_0$ to 4%

Choosing $4\%$ because it is SPARC-comparable, hence combinable:

| requirement | value | comment |
|---|---|---|
| $\sigma(\gamma_v)/\gamma_v$ | $\le 0.462\%$ | i.e. $\sigma(\gamma_v)\le0.0056$ |
| mass–luminosity **zero point** | $\le 0.92\%$ | eclipsing-binary calibrated |
| clean pairs $N$ | $\ge 344{,}000$ | $11.5\times$ the frozen 30,000 — **DR5-and-beyond** |
| $g_{\rm ext}$ (pulsar timing) | $\le 4\%$ | 1:1, so a few percent **suffices** |
| residual $\gamma_v$ systematics | $\le 0.0056$ | **the hard one — currently $0.0206$** |

**The binding item is the systematic, by a factor 3.7.** No number of pairs fixes it: it is the
estimator's shape bias, the contamination budget and the projection treatment that must come down. The
statistical requirement is a telescope problem; the systematic requirement is an analysis problem, and
it is the one that decides whether this route is worth building.

---

## 7. The payoff: orthogonal systematics cross $5\sigma$

| | floor on $a_0$ | dominant terms |
|---|---|---|
| SPARC BTFR intercept | **3.9%** | helium correction, HI self-absorption, CO-dark H$_2$ |
| wide binary $+\,g_{\rm ext}$ | **$\approx4\%$** | mass–luminosity zero point, Gaia systematics |

**The two term-lists share nothing.** Combined in quadrature: $2.79\%$ on $a_0$, i.e.
$\sigma(\kappa)=0.014$. Against the gap $|\tfrac12-1/\sqrt3|=0.0774$:

| | separation of $\tfrac12$ from $1/\sqrt3$ |
|---|---|
| SPARC alone | $3.97\sigma$ |
| wide binary alone | $3.87\sigma$ |
| **combined** | $\mathbf{5.54\sigma}$ |

**Neither route reaches $5\sigma$ alone. Together they do.** That is the entire case for building this
one — not that it is better, but that it is *independent*.

Both footings are carried, as the framework's standing rule requires: the route measures $a_0$, and
which $\kappa$ that implies depends on the footing ($\kappa_{\rm canonical}=0.500$,
$\kappa_{\rm alt}=0.603$ against the canonical denominator).

---

## 8. What is not claimed

1. **Not** *"no mass-to-light ratio anywhere in the chain"* — retracted in §2.1.
   $\gamma_v\propto M_{\rm tot}^{-1/2}$ exactly.
2. **Not a measurement.** No wide-binary data is analysed here. This is an error budget and a
   requirement sheet.
3. **Not achievable with DR4.** The statistical term alone needs $11.5\times$ the frozen $N$, and the
   systematic needs a factor 3.7 improvement.
4. **Not limited by masses today.** The registration's own $\sigma_{\rm sys}$ binds first.
5. **Not** a claim that pulsar-timing $g_{\rm ext}$ is currently good enough — only that it need not be
   *better* than the target, which is the non-obvious part.
6. **Not** a reason to move any registered number. Amendment 9's target stands, provisional as filed.
7. **Not** a claim that $\kappa\ne\tfrac12$. The best current measurement is consistent with it, and
   with $1/\sqrt3$.

---

## 9. Reproducibility

`real_research/reviews/mi_wb_gext_kappa_route_2026.py` — 15/15 checks, exits non-zero on failure,
negative controls included. It reproduces every table above: the $M_{\rm tot}^{-1/2}$ retraction, the
amplification and its robustness, the exact 1:1 $g_{\rm ext}$ mapping with its control, the
registration's implied $\sigma_{\rm sys}$, the requirement sheet, and the combination arithmetic.

Supporting, previously committed: `mi_kappa_error_budget_unlock_2026.py` (SPARC floor, 15/15);
`mi_btfr_intercept_kappa_door_2026.py` ($\kappa=0.465\pm0.076$, 20/20);
`mi_distance_free_gbar_estimator_sparc_2026.py` (distance-free estimator on raw SPARC, 14/14);
`mi_deser_levin_interpolation_2026.py` (the derived interpolation and the $15.6\sigma$ exclusion,
24/24); `mi_graviton_bath_ctp_2026.py` (15/15);
`mi_eps_tot_mode_counting_verdict_2026.py` (13/13).

---

## References

Milgrom, M. 1983, *ApJ* **270**, 365 — MOND.
Milgrom, M. 1999, *Phys. Lett. A* **253**, 273, eq. 9 — $\nu=\sqrt{1+1/y}$ and the de Sitter–Unruh
construction. **The interpolation function used throughout is his.**
Bekenstein, J. & Milgrom, M. 1984, *ApJ* **286**, 7 — AQUAL, hence the isotropic external-field boost.
Deser, S. & Levin, O. 1997, *CQG* **14**, L163 — the accelerated-observer temperature in de Sitter.
Skordis, C. & Złośnik, T. 2021, *PRL* **127**, 161302 — AeST, the relativistic completion.
Lelli, F., McGaugh, S. & Schombert, J. 2016, *AJ* **152**, 157 — SPARC.
Desmond, H. 2023 — RAR intrinsic scatter, 0.034 dex.
Chakrabarti, S. et al. 2021 — direct measurement of the Galactic acceleration from pulsar timing.
Kopp, M., Skordis, C., Thomas, D. & Ilić, S. 2018, *PRL* **120**, 221102 — the GDM bound.

*The distinctive content of this paper is the error budget: the $8.66\times$ amplification, the exact
1:1 $g_{\rm ext}$ mapping, the identification of the registration's own systematic as today's binding
term, the retraction in §2.1, and the orthogonality argument of §7. The estimator, the kernel and the
interpolation function are cited above and are not mine.*
