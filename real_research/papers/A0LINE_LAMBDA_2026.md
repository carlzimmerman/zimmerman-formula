# Reading the Cosmological Constant from Dwarf-Galaxy Rotation Curves: The $a_0$-Line, Its Systematic Floor, and the de Sitter–Modified-Inertia Inversion

**Carl Zimmerman**
Briar Creek Tech · carl@briarcreektech.com

---

## Abstract

Gas-rich dwarf-galaxy rotation curves invert, through a single fixed dimensionless constant, to a value of the cosmological constant that agrees with the Planck measurement to within a factor of $\sim2$ — a striking coincidence, given that the galactic-side determination uses *no cosmological input whatsoever* — but the measured low-acceleration scale $\hat a_0=(0.84$–$1.36)\times10^{-10}\ {\rm m\,s^{-2}}$ is a systematics-limited box that straddles both footings on which the framework's horizon term can be defined, and the $\sim21\%$ distinction between them cannot be decided on current data. That is the central result of this paper, and each of its clauses is load-bearing.

In a de Sitter–Unruh modified-inertia (MI) framework, the low-acceleration scale is tied to the cosmological horizon by $a_0=cH_\Lambda/Z$ with $Z=\sqrt{32\pi/3}=5.78881$, giving $a_0^{\rm canon}=c^2\sqrt{\Lambda/32\pi}=9.355\times10^{-11}\ {\rm m\,s^{-2}}$ on the pure-$\Lambda$ (dark-energy-density) *canonical footing*, or $a_0^{\rm ALT}=cH_0/Z=1.1305\times10^{-10}$ on a total-density ($cH_0$) *ALT footing* — two footings $20.9\%$ apart, carried on every dimensional number below. Squaring the framework's interpolation $g_{\rm obs}=\sqrt{g_{\rm bar}^2+a_0 g_{\rm bar}}$ yields the exact identity $E\equiv g_{\rm obs}^2-g_{\rm bar}^2=a_0\,g_{\rm bar}$: the "missing-gravity" excess is a straight line through the origin with slope $a_0$ at *every* acceleration. The interpolation kernel $\nu=\sqrt{1+1/y}$ is Milgrom's (1999); the identity follows from squaring it, and the distinctive empirical content is (a) the exact constancy $\varepsilon\equiv E/(a_0 g_{\rm bar})=1$ at all $g_{\rm bar}$ — a fingerprint whose *constancy* rival kernels violate — (b) the $cH_\Lambda/Z$ coefficient, and (c) the $\Lambda$-inversion.

Fitting the slope on the gas-dominated SPARC subsample (Lelli, McGaugh & Schombert 2016), where the absolute stellar mass-to-light ($\Upsilon$) swing is cut $\sim71\%$ (from $7.90$ to $2.29\times10^{-11}$), gives the box above. We map the two dominant systematics with independent, committed, exit-0 verification: TRGB-class distances collapse the estimator-choice systematic but distance is *not* the binding wall, and an external-$\Upsilon$ lever tightens $a_0$ by $2$–$12\%$ through partial self-calibration ($\rho\approx-0.7$ to $-0.8$) yet leaves the footings undecided even in the perfect-M/L limit — the true floor is gas-mass calibration. Inverting the slope through $\Lambda=3Z^2\hat a_0^2/c^4$ recovers Planck's $\Lambda$ to a factor $\sim2$ (full-gas GLS central $1.59\times$, $+1.45\sigma$; median/independent-machinery central $1.08\times$, $+0.24\sigma$, which is the better-supported and *closer* estimate). The cleaner the distances, the more the central *overshoots* Planck: the TRGB-tightened central inverts to $2.03\times$ ($+2.76\sigma$), so the sharpest data mildly *disfavour* the Planck-anchored canonical footing rather than confirm it — and that overshoot is itself partly an unmodeled $g_{\rm bar}$-correlated systematic (§3.3), so its interpretation is uncertain. A log-flat Occam comparison favours the zero-parameter horizon prediction by $+0.60$ bans (canonical) / $+1.04$ bans (ALT) — substantial, not decisive, and prior-fragile. The factor-2-in-$\Lambda$ is the factor-$\sim1.4$-in-$a_0$ *squared*: the same single comparison, "does the rotation-measured $a_0$ equal $cH_\Lambda/Z$," re-expressed — not independent confirmation across many decades, and not a test of the postulated normalization $Z$, which appears on both sides. The value of $a_0$ and the sign $s=-1$ remain postulates throughout; what is tied to the horizon is the *scale*.

---

## 1. Introduction

### 1.1 The framework, the horizon scale, and the two footings

Modified inertia (MI) proposes that the inertial response of a body to a force is altered at accelerations below a critical scale $a_0$, rather than the gravitational field being modified. In the de Sitter–Unruh realization considered here, an accelerated observer in a universe with a cosmological horizon experiences a floor in the vacuum's response set by the horizon temperature, and the transition scale is fixed to the horizon:

$$a_0 = \frac{cH_\Lambda}{Z} = \frac{c^2\sqrt{\Lambda/3}}{Z},\qquad Z=\sqrt{\tfrac{32\pi}{3}}=5.78881,$$

where $H_\Lambda\equiv c\sqrt{\Lambda/3}$ is the de Sitter (pure dark-energy) Hubble rate. With the Planck 2018 value $\Lambda=1.089\times10^{-52}\ {\rm m^{-2}}$ (Planck Collaboration 2018) this gives the **canonical footing**

$$a_0^{\rm canon}=c^2\sqrt{\Lambda/32\pi}=9.355\times10^{-11}\ {\rm m\,s^{-2}}\quad(\text{Planck-anchored, }\pm1\%).$$

A second, distinct **ALT footing** replaces the pure-$\Lambda$ density by the total present-day critical density, $a_0^{\rm ALT}=cH_0/Z=1.1305\times10^{-10}\ {\rm m\,s^{-2}}$. A *footing*, in the sense used throughout this paper, is a choice of which cosmological density the horizon term tracks — pure dark energy ($\rho_{\rm DE}$, giving $cH_\Lambda$) versus the total present-day density (giving $cH_0$). It is a physics choice about the framework, not a fitting freedom. The two footings differ by $20.9\%$; deciding which one nature uses is one of the two questions this paper confronts, and **both footings are carried on every dimensional number below.** Nothing that follows derives the value of $a_0$ or the sign of the inertial correction $s=-1$: those remain postulates. What the framework ties to the cosmological horizon is the *scale* of $a_0$, and it is that tie — the $\Lambda\leftrightarrow a_0$ relation — that is under measurement.

### 1.2 What is established, and the question this paper answers

The *forward* statement of the tie — given $\Lambda$, predict $a_0$ — was reported in *The Zimmerman Theory of Gravity* and formalized in the MI field-theory results (Zimmerman 2026a, DOI 10.5281/zenodo.21403470), with the lensing sector constrained separately (Zimmerman 2026b, DOI 10.5281/zenodo.21418816). Independently, the standard MOND phenomenology on the SPARC rotation-curve database is well established: the radial-acceleration relation (McGaugh, Lelli & Schombert 2016) exhibits a characteristic scale $g^\dagger=1.2\times10^{-10}\ {\rm m\,s^{-2}}$, and the SPARC sample itself (Lelli, McGaugh & Schombert 2016) provides the baryonic decompositions used here.

This paper asks the **inverse** question. If $a_0$ is genuinely a horizon-scale quantity, then galaxy rotation curves — sensitive to $a_0$ in their low-acceleration outskirts — should let one *read the cosmological constant back out*, via $\Lambda=3Z^2 a_0^2/c^4$. Can they? And can the measured $a_0$ tell the two footings apart? The answer developed below is the crispest single statement of the result: **the order-of-magnitude inversion is real and striking (rotation curves recover $\Lambda$ to a factor $\sim2$ with no cosmological input on the galactic side), but the $21\%$ footing distinction is blocked by an irreducible systematic floor.** We report this as a *measurement* — striking but non-decisive — and we are equally careful not to manufacture a canonical detection nor a deficit: the best current $a_0$ estimate is a box that straddles *both* footings.

### 1.3 Credit for the kernel

The interpolation function underlying the identity of Section 2,

$$\nu(y)=\sqrt{1+1/y},\qquad y\equiv g_{\rm bar}/a_0,$$

is **not new to this framework**. It is exactly the kernel written by Milgrom (1999, *Phys. Lett. A* **253**, 273, Eq. 9; astro-ph/9805346), in the same functional form, in the original MOND context of Milgrom (1983, *ApJ* **270**, 365). Milgrom's coefficient was $2cH_\Lambda$ rather than $cH_\Lambda/Z$. The identity of Section 2 follows from *squaring* that kernel and is therefore a re-expression of a known law; what the present framework contributes, and what this paper measures, is (a) the exact-constancy fingerprint $\varepsilon=1$, (b) the specific $cH_\Lambda/Z$ coefficient, and (c) the $\Lambda$-inversion. We credit the kernel at the point of use and claim only the distinctive content.

---

## 2. The $a_0$-line identity

### 2.1 The exact identity

The framework's interpolation (Milgrom's kernel, §1.3) $g_{\rm obs}=\sqrt{g_{\rm bar}^2+a_0 g_{\rm bar}}$, i.e. $g_{\rm obs}=g_{\rm bar}\,\nu(y)$ with $\nu=\sqrt{1+1/y}$, squares to

$$\boxed{\;E\equiv g_{\rm obs}^2-g_{\rm bar}^2 = a_0\,g_{\rm bar}\;}\qquad\text{exactly, at every }y.$$

The excess $E$ — the squared difference between observed and baryonic gravity, i.e. the "missing gravity" in acceleration-squared units — is a **straight line through the origin with slope $a_0$**, valid at all accelerations. There is no deep-MOND selection, no interpolation fit, no small- or large-$y$ approximation: the relation is algebraic and exact (verified symbolically in `identity_uniqueness.py`, §A). This converts the usual task — *fit an interpolation function* — into a simpler one: *measure one slope*.

### 2.2 Uniqueness, honestly characterized

Demanding an exactly linear excess, $y^2(\nu^2-1)=\alpha y+\beta$ for all $y>0$, gives $\nu^2=1+\alpha/y+\beta/y^2$. The $\beta$ term produces a nonzero floor, $g_{\rm obs}^2\to\beta a_0^2$ as $g_{\rm bar}\to0$, so requiring $g_{\rm obs}\to0$ forces $\beta=0$; the surviving family $\nu=\sqrt{1+\alpha/y}$ is pure $a_0$-rescaling, and the standard deep-MOND normalization $g_{\rm obs}\to\sqrt{a_0 g_{\rm bar}}$ fixes $\alpha=1$. So $\nu=\sqrt{1+1/y}$ is the **unique interpolation with an exactly linear excess**, up to the definition of $a_0$ itself (verified in `identity_uniqueness.py`, §B; re-derived one generalization further in `verify_independent.py`). We state this honestly: the claim is definitionally tight — "excess exactly linear through the origin" *is* the framework law restated. Its value is methodological, not a new physical fact by itself.

### 2.3 The $\varepsilon=1$ fingerprint versus rival kernels

Define the dimensionless excess ratio $\varepsilon(y)\equiv E/(a_0 g_{\rm bar})=y(\nu^2-1)$. For the framework, $\varepsilon\equiv1$ exactly at all $y$. Rival kernels do not share this:

| $\nu(y)$ | $\varepsilon(y)$ | $y\to0$ | $y\to\infty$ |
|---|---|---|---|
| **framework** $\sqrt{1+1/y}$ | $1$ (exact constant) | $1$ | $1$ |
| **McGaugh/RAR-fit** $\left[1-e^{-\sqrt y}\right]^{-1}$ | $y(\nu^2-1)$ | $1$ | $\sim2y\,e^{-\sqrt y}\to0$ (superexponential death) |
| **simple** $\tfrac12+\sqrt{\tfrac14+1/y}$ | $1-\tfrac y2+\tfrac y2\sqrt{1+4/y}$ | $1$ | $2$ (persistent, slope $2a_0$) |

The three agree in the deep regime ($\varepsilon\to1$ as $y\to0$) but diverge at high $y$. The McGaugh RAR-fit excess **dies superexponentially** — a death that survives any choice of $g^\dagger$. The simple kernel's excess **persists but at slope $2a_0$**, so $\varepsilon\to2$: tail persistence alone does *not* separate the framework from the simple kernel; only the *exact constancy* $\varepsilon\equiv1$ at *all* $y$ does. This is the framework's genuine fingerprint. The separation from the McGaugh fit reaches a factor $\sim110$ at $y=100$ on a matched scale (a factor $\sim11$–$44$ at the rival's own preferred scale — the tail *death* is scale-robust, the exact multiplier is convention-cosmetic).

Two points on the logic. First, the **constancy** of $\varepsilon$ across $g_{\rm bar}$ is a scale-independent statement (it needs no value of $a_0$); the further claim that the constant *equals* $a_0$ does need $a_0$. It is the constancy, not the value, that is the clean fingerprint. Second, the catch, quantified in Section 3, is that SPARC samples this fingerprint thinly: the median point sits at $y=0.31$, and only one point in the entire quality-cut sample exceeds $y=100$. The constancy test is in-principle orthogonal to the M/L degeneracy but, at SPARC's sampling, delivers less than $1\sigma$ of persistent-versus-dying discrimination today (a global framework-vs-McGaugh shape comparison is a wash, $|\Delta\chi^2|\approx2$, with M/L profiled; `fire_linearity.py`). It is a future-data lever, not a present discriminator.

---

## 3. The gas-dominated measurement

### 3.1 The gas cut and why it matters

The slope $a_0$ is estimated by iterated generalized least squares (GLS) through the origin with model-based errors,

$$\hat a_0=\frac{\sum_i w_i E_i g_i}{\sum_i w_i g_i^2},\qquad {\rm Var}_{\rm stat}=\frac{1}{\sum_i w_i g_i^2},$$

on the SPARC point sample after quality cuts ($Q\le2$, inclination $\ge30^\circ$, $e_V/V<10\%$; frozen read-only database, 175 galaxies). The controlling systematic on the full sample is the stellar mass-to-light ratio $\Upsilon$: swinging $\Upsilon_d$ over its full physical range $0.5\to0.8$ moves the full-sample $\hat a_0$ from $1.89\to1.10\times10^{-10}$, a $62\%$ swing that reproduces the known RAR $a_0$–$\Upsilon$ degeneracy essentially in full. On the full sample the $a_0$-line is a beautiful *exact reframing* of the RAR, but it inherits that degeneracy completely and adds no information.

The genuinely new content comes from the **gas-dominated subsample** — the points where the atomic-gas mass (measured from HI, independent of any stellar M/L) dominates the baryonic gravity, so the dominant M/L nuisance is largely removed. Applying a point-level cut

$$V_{\rm gas}^2 > \Upsilon_d V_{\rm disk}^2 + \Upsilon_b V_{\rm bul}^2,\qquad \Upsilon_b=1.4\,\Upsilon_d,$$

isolates those points. At the fiducial $\Upsilon_d=0.7$ this retains $310$ points in $49$ galaxies (weighted stellar share $\langle\varphi\rangle=0.32$). On this subsample the absolute $\Upsilon$ swing in $\hat a_0$ collapses from $7.90\times10^{-11}$ (full sample) to $2.29\times10^{-11}$ (gas-dominated): **the gas cut removes $\sim71\%$ of the absolute $a_0$–$\Upsilon$ degeneracy** (`fire_slope.py`; equivalently, in fractional terms the swing drops from $62\%$ to $19\%$, a $\sim69\%$ reduction; independently reproduced at $15$–$29\%$ residual swing in `verify_independent.py`). This is the paper's single new measurement lever, and it is standard in spirit — gas-rich galaxies as M/L-insensitive probes date to McGaugh (2011); "new" here means new relative to the framework's own previously established walls.

### 3.2 The estimate and its honest box

The gas-dominated slope is

$$\hat a_0^{\rm gas}=1.181\times10^{-10}\ (\text{GLS})\ /\ 0.973\times10^{-10}\ (\text{median}),$$

with independent-machinery estimators (own parser, own cuts, own estimators) landing at $0.92$–$0.97\times10^{-10}$ — i.e. siding with the median variant. The GLS–median spread is the single largest line in the error budget and is a physics-free degree of freedom; it is charged as a systematic, not hidden. Combining all estimator and cut freedom gives an **honest all-choices box**

$$\hat a_0^{\rm gas}\in(0.84\text{–}1.36)\times10^{-10}\ {\rm m\,s^{-2}}\quad(\pm16\%\ \text{systematics-owned}).$$

Placed against the two footings at the gas slope's honest error, the GLS point estimate sits $+1.29\sigma$ above canonical and $+0.27\sigma$ above ALT; the median variant sits $+0.19\sigma$ above canonical and $-0.83\sigma$ below ALT. Because the independent estimators lean toward the median — the *better-supported* central — and it lands *closer* to canonical, **there is no usable footing lean in either direction**: the $21\%$ fork is not decided. The box straddles both footings.

One estimator bias runs in a known direction. The response $E=g_{\rm obs}^2-g_{\rm bar}^2$ carries an uncorrected positive bias: $\mathbb E[g_{\rm obs}^2]=g_{\rm obs,true}^2+{\rm Var}(g_{\rm obs})>g_{\rm obs,true}^2$, so $\mathbb E[\hat a_0]\approx a_0+\Sigma w\,g\,{\rm Var}(g_{\rm obs})/\Sigma w\,g^2$ — a positive push of order (fractional velocity error)$^2\approx1$–$4\%$. (The committed `gls(biased=False)` weighting cures the *weight*–noise correlation, $\mathbb E[w\epsilon]<0$; it does not debias the *response*.) This residual is small and sub-dominant to the effect of §3.3, but it pushes the central in exactly the "sits above both anchors" direction on which the mild disfavouring of canonical rests. Its sign therefore means the canonical footing is, if anything, treated *conservatively* — the true $a_0$ is slightly lower than the reported central, i.e. slightly closer to canonical, not further from it.

### 3.3 The declining per-point $a_0$: an unmodeled $g_{\rm bar}$-correlated systematic

A load-bearing caveat, exposed under adversarial verification: the per-point quantity $a_{0,\rm pt}=E/g_{\rm bar}$ **declines across the deep regime**. Binning the gas points by $g_{\rm bar}$ (TRGB set, $\Upsilon_d=0.7$) gives per-point $a_0$ of $\sim1.62\to1.24\to0.62\times10^{-10}$ from the deepest to the highest $g_{\rm bar}$ tercile — a factor $\sim2.6$ decline, entirely within $y\in[0.009,0.17]$.

It is important to name this correctly, because it is easy to mislabel. The framework's own fingerprint (§2.3) is $\varepsilon\equiv1$ *exactly at all $y$*, which is precisely the statement $E/g_{\rm bar}={\rm const}=a_0$ with **zero shape to leak**: under the framework there is nothing about the kernel that could make $a_{0,\rm pt}$ decline. Nor do the rivals explain it: at the sampled deep $y\in[0.009,0.17]$, the McGaugh and simple kernels both predict $\varepsilon$ *rising* with $g_{\rm bar}$ ($\approx1.13\to1.32$ and $\approx1.13\to1.34$ respectively) — the *opposite sign* to the observed decline. The decline therefore matches *no* candidate kernel in sign or magnitude. It is not kernel shape; it is **an unmodeled $g_{\rm bar}$-correlated systematic**, most plausibly residual stellar M/L acting through the $\varphi$–$g_{\rm bar}$ correlation at the fixed fiducial $\Upsilon_d=0.7$ (raising or lowering $\Upsilon$ tilts the trend — a testable signature of M/L, not of the interpolation). Two consequences follow. First, a genuinely declining $a_{0,\rm pt}$ is a *mild violation* of the framework's own $\varepsilon\equiv1$ fingerprint, not a benign feature of it; we book it as a systematic within the estimator-choice line $s_{\rm Est}$, not as a measured $\varepsilon\ne1$ (which the data are too shallow in $y$ to establish). Second, because the cause is a fixable estimator/M-L bias rather than irreducible kernel curvature, the estimator-weighted central is a *regime-weighted slope* rather than a clean single $a_0$: median/GLS weight the deep regime ($\to1.3\times10^{-10}$), while a weight-free $g_{\rm bar}^2$-OLS weights the high-$g_{\rm bar}$ tail ($\to0.89\times10^{-10}$, near canonical — though that weighting is wrong for the strongly heteroscedastic $E$). A future $E$-debiased or forward-modeled estimator, or points reaching $y\sim1$, could recover a cleaner single $a_0$. The estimator-choice systematic $s_{\rm Est}=|{\rm GLS}-{\rm median}|/2\approx1.04\times10^{-11}$ books this spread, and on the full-gas sample it alone exceeds the footing-splitting threshold. The honest consequence is that the measured $a_0$ is intrinsically a **box straddling both footings**, not a single-footing detection — and the low $g_{\rm bar}^2$-OLS value is likewise *not* a canonical detection.

---

## 4. The systematic map: distance and mass-to-light

Three independent levers could in principle split the footings on current SPARC — the radial-acceleration relation itself, distance quality, and stellar M/L. The first is convention-compatible and non-diagnostic of $a_0$'s exact value (§3.1); the second and third are mapped and spent below (§4.1, §4.2). All three fail on the same wall, which is why the fork is BIG-SPARC-gated (§6). Each lever below carries a dedicated, committed, exit-0 pipeline and an adversarial verification pass. The threshold that matters throughout is the one needed to split the two footings at $2\sigma$:

$$\Delta=|a_0^{\rm ALT}-a_0^{\rm canon}|=1.951\times10^{-11},\qquad \sigma_{\rm tot}\le|\Delta|/2=9.753\times10^{-12}.$$

### 4.1 The TRGB distance lever

Distances enter the excess through $g_{\rm obs}\propto1/D$ (while, exactly, $g_{\rm bar}\propto D^0$ for gas *and* stars, since baryonic surface density is distance-independent — verified symbolically). SPARC's distance-method flag $f_D$ isolates galaxies with tip-of-the-red-giant-branch (TRGB) or Cepheid distances ($f_D\in\{2,3\}$, distance error $\sim5\%$) from the Hubble-flow majority ($f_D=1$, $\sim25\%$). Restricting the gas-dominated subsample to $f_D\in\{2,3\}$ retains $18$–$20$ galaxies ($147$–$191$ points), roughly half the gas sample and point-balanced against the Hubble-flow set — so this is a *budget* test, not a sample-size test (`scout_split.py`). Crucially, the TRGB and Hubble-flow subsamples occupy the *same* acceleration window ($y$-medians $0.037$ vs $0.041$): the identity $E=a_0 g_{\rm bar}$ holds at every $g_{\rm bar}$ regardless of a galaxy's mass or distance, so the two probe the same segment of the $a_0$-line.

The lever works mechanically (`est_gls.py`, `est_robust.py`; verified `verify_trgb.py`):

- **The distance systematic is cut $\sim2$–$3.5\times$** ($6.5\%\to2.8\%$ fractional at $\Upsilon_d=0.7$).
- **The estimator-choice systematic collapses**: on the clean-distance set the median and GLS estimators agree to $\sim0.2\sigma$ (median $1.273$, GLS $1.333\times10^{-10}$ at $\Upsilon_d=0.7$).
- **A Hubble-flow artifact is caught**: the banked low full-gas median ($0.973\times10^{-10}$) was largely a Hubble-flow-distance artifact; the clean-distance central moves *up* coherently across median, GLS, and bootstrap to $\sim1.27$–$1.35\times10^{-10}$ (Hubble-flow-only median $0.805\times10^{-10}$). This is robust (galaxy-level bootstrap $1.329$ [$16$–$84\%$: $1.173,1.486$]$\times10^{-10}$; max leave-one-out shift $<10\%$) and is a distance-*scale* effect, not a $g_{\rm bar}$-segment selection artifact (range-matching trims zero points).

But the upward move is itself estimator-weighting-dependent (the unmodeled $g_{\rm bar}$-correlated systematic of §3.3: the weight-free OLS gives $0.89\times10^{-10}$), so it is a regime-weighted slope of uncertain origin, not a canonical detection nor a manufactured deficit. And, decisively, **distance is not the binding wall**: once gas-dominated, the total error is floored by the M/L and gas-calibration systematics *above* the $|\Delta|/2$ target on every prior convention. The clean-distance central at $\sim1.3\times10^{-10}$ sits above *both* anchors, leaning mildly *against* canonical ($-2.75\sigma$) rather than detecting it, with ALT weakly favoured ($-1.28\sigma$) but not confirmed — and, per §3.3, that very overshoot is partly the unmodeled systematic rather than a clean signal, so it is not read as a real move against canonical. The footing separation is $\le1.3$ bans (log-flat), $<1$ ban under an adversarial informed prior — below the $2$-ban line on every convention. **Verdict: the TRGB lever tightens the method but is non-diagnostic of the footing; the distance flag is spent.**

### 4.2 The mass-to-light lever

The residual $\Upsilon$ uncertainty ($\sigma_{\ln\Upsilon}=0.0999$ dex) enters the current budget as *one global, fully coherent* number, so it does not average down with galaxy count — it is a floor. The lever (`setup_mlpriors.py`, `est_indep.py`, `est_marg.py`, `est_wall.py`; verified) decomposes it into a **coherent SPS/IMF zero-point floor** (irreducible; external colours cannot touch it) plus a **per-galaxy reducible part** (which external $[3.6]$+colour SPS priors shrink, and which averages $\sim1/\sqrt N$). Two calibration-preserving literature decompositions (quadrature $\approx$ the banked $0.0999$ dex; Schombert, McGaugh & Lelli 2019; Meidt et al. 2014; McGaugh & Schombert 2014; Bell & de Jong 2001) are used, since SPARC ships one fixed $\Upsilon$ per galaxy and no local colour vector:

- balanced: coherent $0.060$ dex + per-galaxy residual $0.040$ dex;
- NIR-realistic: coherent $0.075$ dex + per-galaxy residual $0.035$ dex.

Three findings, each verified both ways:

1. **The real gain is recognizing the split, not the external prior.** Because at $[3.6]$ the M/L is nearly constant, the per-galaxy reducible signal is intrinsically small; the coherent line drops from $9.57\times10^{-12}$ to $\sim5.8\times10^{-12}$ (balanced, $\Upsilon_d=0.7$) mostly by acknowledging that part of the M/L error already averaged over $\sim49$ galaxies, not by new colour data.

2. **The coherent $\Upsilon$ zero-point is only *partially* degenerate with $a_0$.** Treating it as a proper Bayesian nuisance template ($C=\mathrm{diag}(\sigma_i^2)+s^2 UU^\top$, Sherman–Morrison marginalization) gives correlation $\rho(a_0,\alpha)=-0.65$ to $-0.81$, *never* $\to1$, because the stellar share $\varphi$ genuinely varies with $g_{\rm bar}$ so the template $U$ is not proportional to $g$. The data therefore self-calibrate the nuisance, and marginalization **tightens** $a_0$ by $2$–$12\%$ (marg/quad $=0.88$–$0.98$): the quadrature budget was mildly conservative, not anti-conservative.

3. **Even perfect M/L is insufficient.** Zeroing the $\Upsilon$ systematic *entirely* still leaves the best-case total at $\sim12.96\times10^{-12}$ (TRGB, $\Upsilon_d=0.7$; $\sim1.94\sigma$ footing separation) — above $9.753\times10^{-12}$ and under $2\sigma$ everywhere. Beating $\Upsilon$ is *necessary but not sufficient*.

The reason is that **the true wall after $\Upsilon$ is gas-mass calibration** ($s_G$, coherent $\sigma_{\ln G}=0.10$). It does *not* average down and does *not* self-calibrate, because on gas-dominated points $1-\varphi\approx1$, so the gas template is nearly proportional to $g$. The coherent floor

$$\mathrm{hypot}(s_{U,\rm coh},\,s_G)=\mathrm{hypot}(5.75,\,8.63)\times10^{-12}=1.037\times10^{-11}>|\Delta|/2$$

**exceeds the footing-splitting threshold at any $N$** at $\sigma_{\ln G}=0.10$ (coherent terms do not average down). An external swap to colour-based M/L (McGaugh & Schombert 2014) trades the SPS coherent zero-point for a comparable colour-M/L/dust/age–metallicity zero-point ($\sim0.10$–$0.15$ dex) with no net gain (a swept coherent floor never crosses the threshold). **Verdict: the M/L lever tightens $a_0$ but is non-diagnostic of the footing; the wall shifts to gas-mass calibration.**

### 4.3 The systematic budget

Gas-dominated budget at $\Upsilon_d=0.7$ ($310$ points, $49$ galaxies; all $\sigma$ in $10^{-12}\ {\rm m\,s^{-2}}$), before and after the two levers. Each column is a single, internally consistent configuration: full-gas (banked coherent $\Upsilon$), the $\Upsilon$-lever applied to the full-gas set (balanced decomposition), and the $\Upsilon$-lever applied to the TRGB clean-distance set (balanced decomposition).

| Systematic line | full-gas (banked) | full-gas $+\Upsilon$ lever (balanced) | TRGB $+\Upsilon$ lever (balanced) |
|---|---|---|---|
| statistical | $4.67$ | $4.67$ | $6.12$ |
| distance ($s_D$) | $7.63$ | $7.63$ | $3.80$ |
| inclination ($s_i$) | $2.64$ | $2.64$ | $4.22$ |
| stellar M/L ($s_U$) | $9.57$ | $5.79$ | $6.83$ |
| **gas calibration ($s_G$)** | $\mathbf{8.63}$ | $\mathbf{8.63}$ | $\mathbf{9.46}$ |
| estimator / regime-slope ($s_{\rm Est}$) | $10.44$ | $10.44$ | $3.00$ |
| **total $\sigma_{\rm tot}$** | $19.03$ | $17.43$ | $14.65$ |
| ($\%$ of $\hat a_0$) | $16.1\%$ | $14.8\%$ | $11.0\%$ |
| footing separation | $\sim1.2\sigma$ | $\sim1.3\sigma$ | $\sim1.7\sigma$ |

*Footing separation* here is the log-space metric $|\ln(a_0^{\rm ALT}/a_0^{\rm canon})|/(\sigma_{\rm tot}/\hat a_0)=0.1895/\sigma_{\ln,\rm tot}$ — how many log-$\sigma$ separate the two footings — evaluated at each column's central $\hat a_0$ (full-gas $1.181$, TRGB $1.333\times10^{-10}$). It is the relevant "can I split them" number and is not the same as the linear ratio $|\Delta|/\sigma_{\rm tot}$, which is $\approx1.0$ for full-gas; both are below $2$. Threshold to split at $2\sigma$: $\sigma_{\rm tot}\le9.753\times10^{-12}$. **No configuration reaches it** — not the TRGB clean-distance set, not the external-$\Upsilon$ lever, not the two combined, and not even the $s_U\to0$ perfect-M/L limit ($\sim12.96\times10^{-12}$, $1.94\sigma$; §4.2). The binding lines after both levers are gas calibration $s_G\approx8.6$–$9.5$, the estimator/regime-slope spread $s_{\rm Est}$, and the coherent SPS floor — none of which distance or M/L work reduces. (For reference, the banked TRGB set *before* the $\Upsilon$ lever carried $s_U=11.18$ and $\sigma_{\rm tot}=17.1\times10^{-12}$, $12.8\%$ of $\hat a_0$; the lever is what moves the TRGB column to $14.65$.)

---

## 5. The $\Lambda$-inversion

The horizon tie inverts algebraically to the cosmological constant:

$$a_0=\frac{c^2\sqrt{\Lambda/3}}{Z}\;\Longleftrightarrow\;\boxed{\;\Lambda=\frac{3Z^2\hat a_0^2}{c^4}\;}$$

(sympy-inverted, `fire_lambda.py`; re-derived by hand in verification; note $3Z^2=32\pi$, so equivalently $\Lambda=32\pi\hat a_0^2/c^4$).

**What is and is not tested by this inversion — the load-bearing point.** Because the canonical $a_0^{\rm canon}\equiv c^2\sqrt{\Lambda_{\rm Planck}/32\pi}$ is *defined* from Planck's $\Lambda$, the predicted ratio is *identically*

$$\frac{\Lambda_{\rm pred}}{\Lambda_{\rm Planck}}=\left(\frac{\hat a_0}{a_0^{\rm canon}}\right)^2\quad\text{exactly.}$$

The inversion is therefore a *single-number test* — does the rotation-measured $a_0$ equal the horizon value $cH_\Lambda/Z$? — squared and re-expressed, not many independent decades of confirmation. The "factor $\sim2$ in $\Lambda$" is the "factor $\sim1.4$ in $a_0$" squared. What *is* genuinely independent and non-trivial is that the rotation-curve $\hat a_0$ uses *zero* cosmological input (only rotation velocities $V$, radii $R$, and baryonic decompositions), so its agreement with a horizon-derived acceleration is a real galactic-versus-cosmological coincidence — the classic Milgrom $a_0\sim cH$ coincidence, here sharpened. What is *not* tested is (a) the normalization $Z=\sqrt{32\pi/3}$, which appears on *both* sides of the inversion and is assumed throughout, never checked against data; and (b) the "large exponent" of $\Lambda$ ($\sim10^{-52}\ {\rm m^{-2}}$ in SI units), which is a unit-dependent dimensional statement, not a measured dynamic range. We flag both so the coincidence is not over-read.

Feeding the gas-dominated slope through the relation:

| Estimate | $\hat a_0\ (10^{-10})$ | $\Lambda_{\rm pred}\ (10^{-52}\,{\rm m^{-2}})$ | ratio to Planck | tension |
|---|---|---|---|---|
| full-gas GLS | $1.181$ | $1.74$ | $1.59\times$ | $+1.45\sigma$ |
| full-gas median / independent | $0.973$ | $1.18$ | $1.08\times$ | $+0.24\sigma$ |
| TRGB clean-distance | $1.33$ | $2.21$ | $2.03\times$ | $+2.76\sigma$ |

against Planck 2018, $\Lambda=1.089\times10^{-52}\ {\rm m^{-2}}$, at $\sigma_{\ln\Lambda}=2\sigma_{\ln a_0}=0.32$. The clean $\Lambda$ statement is on the canonical (pure-$\Lambda$) footing; the ALT footing ties $a_0$ to $H_0$ (matching the GLS slope at $+0.27\sigma$) and does not itself produce a "$\Lambda$," so the inversion column is canonical-only by construction.

The headline is the coincidence itself: **rotation curves of gas-rich dwarfs recover the cosmological constant to a factor $\sim1.1$–$2.0$ of the value measured from the cosmic microwave background — two determinations separated by the span from galactic to cosmological scales, with no cosmological input on the galactic side.** This is what a horizon-scale $a_0=cH_\Lambda/Z$ predicts, and it is the same information as the previously reported $a_0\sim cH_\Lambda/Z$ coincidence, reframed as an inversion — now with a sharper falsification target: a future gas-dominated slope at $3\times10^{-10}$ would break it outright. Two honest hedges. First, the *better-supported* estimators (median and independent machinery) land *closer* to Planck ($+0.24\sigma$), so the inversion is if anything cleaner than the GLS headline. Second, the *cleaner the distances, the more the central overshoots Planck*: the TRGB-tightened central sits $2.03\times$ high ($+2.76\sigma$), further above rather than onto Planck, so the sharpest current data mildly *disfavour* the canonical footing rather than confirm it — and, per §3.3, that overshoot is itself partly the unmodeled $g_{\rm bar}$-correlated systematic, so its interpretation is uncertain and it is not read as a real deficit either.

**The Occam comparison.** Contrasting the zero-parameter horizon prediction $M_0=\{a_0\equiv cH_\Lambda/Z,\ \text{no free parameters},\ \pm1\%\ \text{anchor}\}$ against a free-$a_0$ model $M_1$ with a log-flat prior of width $W$:

$$B_{01}=\underbrace{\frac{W}{\sqrt{2\pi}\,s}}_{\text{Occam}}\;\underbrace{e^{-t^2/2}}_{\text{fit penalty}},\qquad t=\frac{\ln a_0^*-\ln\hat a_0}{\sqrt{s^2+s_{\rm anchor}^2}},\quad s=0.161.$$

On the default two-decade prior: $B_{01}=+0.60$ bans (canonical) / $+1.04$ bans (ALT), with a prior/estimator envelope $+0.30$ to $+1.38$ (canonical) / $+0.57$ to $+1.34$ (ALT). On Jeffreys' scale this is "substantial" — **positive but modest, explicitly not decisive**. It formalizes *predicted-not-fitted* (that $a_0$ was fixed from $c$, $H_\Lambda$, $Z$ before the fit), not new data, and it is prior-convention-fragile: a literature-informed prior conditioned on the MOND scale can drive the canonical bans toward $\sim0$ (though never negative). Two-sided, the lever is also a genuine falsification exposure: if a future clean measurement holds the GLS central at $3\times$ smaller error, the canonical footing would move to $-2.45$ bans — which is precisely what makes the measurement worth sharpening.

---

## 6. The footing fork and honest scope

The two footings are $20.9\%$ apart:

$$a_0^{\rm canon}=cH_\Lambda/Z=9.355\times10^{-11}\ (\rho_{\rm DE},\ \text{pure-}\Lambda),\qquad a_0^{\rm ALT}=cH_0/Z=1.1305\times10^{-10}\ (\rho_{\rm total},\ cH_0).$$

The measured $a_0$ is a box $(0.84$–$1.36)\times10^{-10}$ that **straddles both footings**. On the estimator-weighted central the canonical footing is mildly *disfavoured* (the central sits above it, $\sim-3\sigma$ high-side across configurations), while ALT is *not confirmed* ($\sim-1.4\sigma$). We manufacture neither a canonical detection nor a deficit: the honest reading is a straddle, and the mild high-side lean is partly the response bias (§3.2) and the unmodeled $g_{\rm bar}$-correlated systematic (§3.3), both of which push the central up.

The fork is **not decidable from current SPARC by any systematic lever**. The RAR is convention-compatible and non-diagnostic of $a_0$'s exact value; the TRGB distance lever is spent (§4.1); the M/L lever is spent, including its perfect-M/L limit (§4.2). The binding wall is the coherent gas-calibration + SPS floor + estimator/regime-slope spread, and $\mathrm{hypot}(s_{U,\rm coh},s_G)=1.037\times10^{-11}$ exceeds $|\Delta|/2=9.753\times10^{-12}$ at *any* $N$ at the current gas-calibration precision.

Deciding the fork therefore requires *all* of:

1. **BIG-SPARC-scale statistics** — a clean-distance gas-dwarf sample of $N\sim300$–$670$ (the what-it-takes map: at $\sigma_{\ln G}=0.08$, $N\sim666$; at $0.06$, $N\sim273$), to pull the statistical floor down and force the estimator-choice systematic into the open;
2. **An independent gas-mass calibration** cutting $\sigma_{\ln G}$ from $0.10$ to $\lesssim0.08$ (interferometric HI + CO, He/metal corrections) — since at $\sigma_{\ln G}=0.10$ no finite $N$ suffices;
3. **Points reaching $y\sim1$** to break the regime-slope magnitude systematic of §3.3 (and, as a bonus, to make the $\varepsilon=1$ constancy fingerprint of §2.3 testable).

What is robust today is the **order-of-magnitude inversion**: $\Lambda$ recovered from dwarf rotation to within a factor $\sim2$ of Planck, with no cosmological input on the galactic side. What is blocked is the **$21\%$ which-dark-energy-quantity distinction** — canonical $\rho_{\rm DE}$ versus total $\rho_{\rm total}$. The first is a striking measurement; the second is data-gated, and we state it as such.

A footing-fork subtlety worth flagging for future epochs: the canonical footing predicts the gas slope tracks $\sqrt{\rho_\Lambda}$ (constant in redshift), while the ALT footing tracks $cH(z)E(z)$ (rising). A multi-epoch $a_0(z)$ measurement (e.g. via DESI-scale samples) would turn the $21\%$ degeneracy into a slope-versus-redshift discriminator — the one route that does not run into the static systematic floor mapped here.

---

## 7. Discussion

The result of this paper is a **measurement**, and it should be read as one. The $a_0$-line identity converts the framework's rotation-curve law into a single measurable slope; the gas-dominated cut on SPARC removes $\sim71\%$ of the stellar M/L degeneracy that otherwise dominates such measurements; and inverting the slope recovers the cosmological constant to a factor $\sim2$ of the Planck value, from galactic-scale kinematics that carry no cosmological input. That coincidence — that the outskirts of nearby gas-rich dwarfs encode, to within a factor of two, the same $\Lambda$ that governs the accelerating expansion of the universe — is the striking positive of the framework's horizon-scale $a_0=cH_\Lambda/Z$ hypothesis, and it is stated here without overclaim. Its honest weight is exactly that of the classic Milgrom $a_0\sim cH$ coincidence, sharpened into an inversion and a falsifiable target — no more, because the inversion is one comparison squared, and it assumes rather than tests the normalization $Z$.

What the measurement does *not* do is equally important. It does not distinguish the two dark-energy footings: the measured $a_0$ is a box straddling both, and every systematic lever available on current SPARC (the RAR, distance, M/L) has been mapped and spent without crossing the $2\sigma$ splitting threshold. The binding wall is gas-mass calibration together with an irreducible coherent SPS floor and an unmodeled $g_{\rm bar}$-correlated systematic that pulls the inferred magnitude down across the deep regime — a mild tension with the framework's own $\varepsilon\equiv1$ fingerprint, not a benign feature of it. None of these is reducible by more distance or M/L work, and even a perfect M/L measurement leaves the footing separation below $2\sigma$. The identity is a re-expression of a kernel due to Milgrom (1999); the distinctive empirical content is the exact-constancy fingerprint (data-starved today), the $cH_\Lambda/Z$ coefficient, and the inversion. And the value of $a_0$ and the sign $s=-1$ are postulates: what is tied to the horizon is the *scale*.

Read as a statement about method, "$a_0$-from-rotation $=$ the dark-energy density scale" is the sharpest available single-number route from galaxy rotation to the cosmological constant, and this paper strengthens the *method* (the gas cut, the distance and M/L maps, the inversion) while being explicit that it does not yet strengthen the *claim* to a footing-level detection. A genuinely striking numerical coincidence has been sharpened into a falsifiable target, and the two-sided Occam lever means the framework now carries real falsification exposure on the canonical footing — which is what makes the next generation of data (BIG-SPARC, an independent gas-mass calibration, and $y\sim1$ points) worth acquiring.

---

## 8. Conclusion

**Central claim.** Gas-rich dwarf-galaxy rotation curves invert, through the fixed constant $Z=\sqrt{32\pi/3}$, to the cosmological constant measured by Planck to within a factor of $\sim2$ — a striking coincidence with no cosmological input on the galactic side — but the measured $a_0=(0.84$–$1.36)\times10^{-10}\ {\rm m\,s^{-2}}$ is a systematics-limited box that straddles both the canonical ($cH_\Lambda/Z=9.36\times10^{-11}$) and ALT ($cH_0/Z=1.13\times10^{-10}$) footings; the $\sim21\%$ distinction between which dark-energy quantity the horizon term tracks is blocked by a gas-mass-calibration floor and cannot be decided on current SPARC.

1. **The identity.** Squaring the framework's interpolation gives $E\equiv g_{\rm obs}^2-g_{\rm bar}^2=a_0 g_{\rm bar}$, exact at every acceleration — the missing-gravity excess is a straight line through the origin with slope $a_0$. The kernel is Milgrom's (1999); the distinctive content is the exact constancy $\varepsilon=1$, the $cH_\Lambda/Z$ coefficient, and the inversion.

2. **The measurement.** On the gas-dominated SPARC subsample the slope is $\hat a_0=(0.84$–$1.36)\times10^{-10}\ {\rm m\,s^{-2}}$ ($\pm16\%$, no usable footing lean), with $\sim71\%$ of the absolute M/L degeneracy removed and an unmodeled $g_{\rm bar}$-correlated systematic (a mild tension with $\varepsilon\equiv1$) carried throughout.

3. **The systematic floor.** The TRGB distance lever collapses the estimator-choice systematic and catches a Hubble-flow artifact but is not the binding wall; the M/L lever tightens $a_0$ by $2$–$12\%$ through partial self-calibration ($\rho\approx-0.7$ to $-0.8$) yet is insufficient even in the perfect-M/L limit. The true wall is gas-mass calibration: $\mathrm{hypot}(s_{U,\rm coh},s_G)=1.037\times10^{-11}$ exceeds $|\Delta|/2=9.753\times10^{-12}$ at any $N$.

4. **The inversion.** $\Lambda=3Z^2\hat a_0^2/c^4$ recovers the cosmological constant to a factor $\sim2$ of Planck (full-gas GLS $1.59\times$, $+1.45\sigma$; median/independent $1.08\times$, $+0.24\sigma$; TRGB $2.03\times$, $+2.76\sigma$ — overshooting) — the striking positive, favoured by $+0.60$ bans (canonical) / $+1.04$ bans (ALT) on a log-flat Occam comparison, substantial but not decisive. It is one comparison, $\hat a_0$ versus $cH_\Lambda/Z$, squared and re-expressed, and it assumes the normalization $Z$.

5. **The scope.** The order-of-magnitude inversion is robust; the $21\%$ canonical-versus-ALT footing distinction is data-blocked, requiring BIG-SPARC-scale clean-distance samples, a sharper gas-mass calibration ($\sigma_{\ln G}\lesssim0.08$), and $y\sim1$ points. The value of $a_0$ and the sign $s=-1$ remain postulates; what is tied to the horizon is the scale.

---

## Appendix A: Committed, exit-0 verification scripts

Every load-bearing number above reproduces from raw SPARC data (frozen, read-only) via a committed Python script; each exits 0, carries both footings, and was re-derived by an independent verifier with its own parser, cuts, and estimators. No hard-coded checks: every assertion is a live sympy simplification or a computed numeric comparison.

**The $a_0$-line core (`prep_2026/a0_line/`).**
- `identity_uniqueness.py` — sympy verification of the identity $E=a_0 g_{\rm bar}$ (§A), the uniqueness family $\nu=\sqrt{1+\alpha/y}$ with $\alpha=1$ forced (§B), the rival excess formulas and $\varepsilon(y)$ table (§C–D), and the SPARC $y$-sampling census (§E: median $y=0.31$, $N(y>100)=1$).
- `estimator_theory.py` — the GLS estimator, the observed-error weighting trap ($\mathbb E[w\epsilon]<0$, a $\times3$ artifact, cured by model-based weights), the residual positive response bias ($1$–$4\%$, §3.2), the exact distance scaling ($g_{\rm bar}\propto D^0$ for gas and stars), the per-point sensitivity arms, and the full budget.
- `bayes_setup.py` — the Occam factor closed form and quadrature, prior sensitivity, footing comparison, and the $\Lambda$-inversion.
- `fire_slope.py` — the gas-dominated GLS slope ($1.181\times10^{-10}$ / median $0.973$), the $71\%$ absolute degeneracy kill, both footings.
- `fire_linearity.py` — the $\varepsilon=1$ fingerprint versus McGaugh and simple kernels, the shape-test wash ($|\Delta\chi^2|\approx2$ with M/L profiled).
- `fire_lambda.py` — $\Lambda=3Z^2\hat a_0^2/c^4$, $1.74\times10^{-52}$ (GLS) / $1.18\times10^{-52}$ (median) vs Planck.
- `fire_occam.py` — $B_{01}=+0.60$ / $+1.04$ bans, the envelope, the two-sided error-reduction lever.
- `fire_common.py`, `verify_independent.py` — shared machinery and the independent-verifier re-derivation.

**The TRGB distance lever (`prep_2026/a0_line_trgb/`).**
- `scout_split.py` — the $f_D$ split ($18$–$20$ TRGB/Cepheid gas galaxies), same-acceleration-window check.
- `est_gls.py`, `est_robust.py` — the clean-distance slope ($1.33\times10^{-10}$, estimator collapse to $0.2\sigma$, Hubble-flow artifact), both footings.
- `est_forecast.py` — the realized error-reduction / Occam-ban forecast.
- `verify_trgb.py` — independent re-derivation; the $g_{\rm bar}^2$-OLS catch of the declining per-point $a_0$ (deep-to-high tercile $1.62\to0.62\times10^{-10}$).

**The M/L lever (`prep_2026/a0_line_mlpriors/`).**
- `setup_mlpriors.py` — the coherent/per-galaxy $\Upsilon$ decomposition, the coherence check (fully-coherent $9.57$ vs fully-independent $1.66\times10^{-12}$).
- `est_indep.py`, `est_wall.py` — the residual-floor and what-it-takes maps; the $s_U\to0$ hard limit ($\sim1.94\sigma$, insufficient); gas-calibration as the binding wall.
- `est_marg.py` — the Bayesian nuisance marginalization ($\rho=-0.65$ to $-0.81$; marginalization tightens $2$–$12\%$).

All three lanes returned the verdict **UPHELD** under adversarial verification, with the honesty rails run in both directions: three artifacts (an observed-weight $\times3$ fake deficit, a cross-$\Upsilon$ covariance fake $\Delta\chi^2$, and a loose error-reduction "win" forecast) were caught in-script and corrected rather than relayed. No configuration manufactures a footing detection or a deficit; the measured $a_0$ is a box straddling both footings.

---

## References

Bell, E. F., & de Jong, R. S. 2001, *ApJ*, **550**, 212.

Lelli, F., McGaugh, S. S., & Schombert, J. M. 2016, *AJ*, **152**, 157 (SPARC).

McGaugh, S. S. 2011, *Phys. Rev. Lett.*, **106**, 121303.

McGaugh, S. S., Lelli, F., & Schombert, J. M. 2016, *Phys. Rev. Lett.*, **117**, 201101 (RAR, $g^\dagger=1.2\times10^{-10}$).

McGaugh, S. S., & Schombert, J. M. 2014, *AJ*, **148**, 77 (colour–M/L relation).

Meidt, S. E., et al. 2014, *ApJ*, **788**, 144 ([3.6] M/L).

Milgrom, M. 1983, *ApJ*, **270**, 365.

Milgrom, M. 1999, *Phys. Lett. A*, **253**, 273 (astro-ph/9805346; the $\nu=\sqrt{1+1/y}$ kernel, Eq. 9).

Planck Collaboration 2018, *A&A*, **641**, A6 ($\Lambda$).

Schombert, J. M., McGaugh, S. S., & Lelli, F. 2019, *MNRAS*, **483**, 1496 (SPS M/L).

Zimmerman, C., *The Zimmerman Theory of Gravity* (Zenodo; the forward $\Lambda\to a_0$ statement).

Zimmerman, C. 2026a, *MI Field Theory Results 2026*, DOI 10.5281/zenodo.21403470.

Zimmerman, C. 2026b, *MI Lensing No-Go*, DOI 10.5281/zenodo.21418816.
