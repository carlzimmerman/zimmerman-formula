# Does the Galaxy Acceleration Scale Track Cosmic Dark Energy? A Non-Circular Cross-Scale $a_0(z)$ Test of de Sitter–Unruh Modified Inertia — the $z=0$ Tie, the High-$z$ BTFR Forecast, and Why $M_{\rm bar}$ Calibration (Not Rotator Count) Is Decisive

**Carl Zimmerman**
Briar Creek Tech · carl@briarcreektech.com

---

## Abstract

In a de Sitter–Unruh modified-inertia (MI) framework the low-acceleration scale $a_0$ is fixed to the cosmological horizon by $a_0=cH_\Lambda/Z$ with $Z=\sqrt{32\pi/3}=5.78881$, giving the pure–dark-energy-density (canonical) footing $a_0^{\rm canon}=c^2\sqrt{\Lambda/32\pi}=9.355\times10^{-11}\,{\rm m\,s^{-2}}$ or the total-density (ALT) footing $a_0^{\rm ALT}=cH_0/Z=1.1305\times10^{-10}\,{\rm m\,s^{-2}}$, two footings $20.9\%$ apart that are carried on every number here. The framework does **not** rewrite Type Ia supernova standardization and gives **no** new distance formula — its cosmological background is General Relativity. Its distinctive content is that the dark-energy term in the Friedmann equation is not a free fit but the *galaxy* acceleration scale: $H^2(z)=\tfrac{8\pi G}{3}\rho_m(z)+Z^2a_0^2(z)/c^2$, with $a_0(z)$ measurable from galaxy dynamics and $Z$ a single posited constant. This ties a galaxy-kinematic quantity to a cosmic-distance quantity through $a_0(z)=\tfrac{c}{2}\sqrt{G\rho_{\rm DE}(z)}$ (equivalently $a_0=c^2\sqrt{\Lambda_{\rm eff}/32\pi}$ with $\Lambda_{\rm eff}=8\pi G\rho_{\rm DE}/c^2$), i.e. $a_0(z)/a_0(0)=\sqrt{\rho_{\rm DE}(z)/\rho_{\rm DE,0}}$ — a bridge $\Lambda$CDM structurally lacks. It adds no dark-energy parameters beyond the GR background: the same $\rho_{\rm DE}(z)$ that fits cosmic distances must fit the galaxy $a_0(z)$. The equality $a_0\!\leftrightarrow\!\Lambda$ at fixed $z$ is a definition and is circular; the *non-circular* test is the joint $z$-tracking of two independent datasets. We report a method + forecast **non-detection with a live cosmology-side hint**. (i) The $z=0$ tie holds: $\Lambda$-blind SPARC $a_0(0)=1.181\times10^{-10}\,(\pm16\%)$ versus cosmic $(c/2)\sqrt{G\rho_{\rm DE,0}}$ gives ratio $1.26$ ($1.44\sigma$, Planck $H_0$) or $1.17$ ($0.95\sigma$, SH0ES $H_0$). (ii) The DESI DR2 $w_0w_a$ posterior propagated through the framework relation yields $a_0(z{=}3)/a_0(0)\simeq0.74$ (Pantheon+ $0.775$, DESY5 $0.737$, Union3 $0.707$; a $\sim2.2\sigma$ decline) — a consequence of the framework relation plus the DESI $w(z)$, not an independent detection. (iii) On the galaxy side the distinctive $0.60$–$0.75$ decline is neither detected nor excluded: separability $S\simeq0.8\sigma$. The Big Wheel — the cleanest available deep-MOND *candidate* at $z=3.25$, though the v2 dynamical model finds it transitional ($y=g_{\rm bar}/a_0\approx0.7$–$1.3$), not cleanly deep-MOND — gave, on the discovery-paper masses, $a_0(3.25)/a_0(0)=1.31\,(+0.93/-0.52)$, consistent with a constant, unable to separate the decline from flat, and (on those masses) disfavoring the ALT-$cH_0$ $\sim5\times$ *rise* at $\sim2\sigma$. **(v2)** A dedicated 2026 ALMA dynamical model (Quadri et al. 2026), *despite* sharper input kinematics, does **not** tighten the single-object $a_0$ — it *empirically confirms* the central finding: a $0.37$-dex stellar-mass ambiguity the authors flag as unresolved swings the inferred $a_0$ across ratio $\sim0.9$–$3.3$ ($0.4$–$4.7$ across full systematics, $\sim28\%$ of the high-$M_\star$ posterior unphysical). Under the authors' fiducial dynamical mass the object itself sits at a $\sim3\times$ rise (ratio $3.1\,[1.9,4.7]$), so it no longer cleanly excludes the $\sim5\times$ rise either — that $\sim2\sigma$ rise-exclusion held only on the discovery masses. The single rotator cannot pin the decline; $M_{\rm bar}$ calibration, not the object, is decisive. The central finding is methodological: in the baryonic Tully–Fisher (BTFR) estimator $a_0$ is algebraically $1{:}1$ degenerate with baryonic mass ($\Delta\log a_0=-\Delta\log M_{\rm bar}$ at fixed $V$), so the dominant $M_{\rm bar}$ systematic is common-mode and does **not** beat down with rotator count: with a $\gtrsim0.08$-dex correlated $M_{\rm bar}$ floor the test never reaches $3\sigma$ at any $N$. The decisive lever is $M_{\rm bar}$ calibration to $\lesssim0.05$ dex common-mode, not the number of galaxies, and the $a_0$-separable observable that breaks the degeneracy is the full rotation-curve / radial-acceleration transition, not the BTFR zero-point. The value of $a_0$ and the constant $Z$ are posited, not derived; the $a_0$ magnitude inherits $Z$, so only the ratio/tracking is under test.

---

## 1. Introduction

### 1.1 The framework and the horizon scale

Modified inertia proposes that the inertial response of a body to a force weakens below a critical acceleration $a_0$, rather than the gravitational field being modified. In the de Sitter–Unruh realization, an accelerated observer in a universe with a cosmological horizon sees a floor in the vacuum's response set by the horizon temperature, and the transition scale is tied to the horizon:

$$a_0=\frac{cH_\Lambda}{Z}=\frac{c^2\sqrt{\Lambda/3}}{Z},\qquad Z=\sqrt{\tfrac{32\pi}{3}}=5.78881,$$

with $H_\Lambda\equiv c\sqrt{\Lambda/3}$ the de Sitter (pure dark-energy) Hubble rate. The Planck 2018 value $\Lambda=1.089\times10^{-52}\,{\rm m^{-2}}$ gives the **canonical footing** $a_0^{\rm canon}=c^2\sqrt{\Lambda/32\pi}=9.355\times10^{-11}\,{\rm m\,s^{-2}}$ (pure $\rho_{\rm DE}$). A second **ALT footing** replaces the pure-$\Lambda$ density by the total present-day critical density, $a_0^{\rm ALT}=cH_0/Z=1.1305\times10^{-10}\,{\rm m\,s^{-2}}$. The two differ by $20.9\%$; both are carried on every dimensional number below. Nothing here derives the value of $a_0$, the constant $Z$, or the sign of the inertial correction: those remain postulates. What the framework ties to the horizon is the *scale* of $a_0$.

### 1.2 The parameter-free replacement of the free-$w$ fit

The framework keeps General Relativity for the cosmological background and therefore has no native supernova formula: the light-curve $\to$ distance standardization is unchanged, and the Friedmann equation is the standard one. Its single distinctive move is that the dark-energy term is not a free fit but the galaxy acceleration scale,

$$H^2(z)=\frac{8\pi G}{3}\,\rho_m(z)+\frac{Z^2a_0^2(z)}{c^2},\qquad \frac{Z^2a_0^2}{c^2}=H_\Lambda^2=\frac{\Lambda c^2}{3}\;\;(z=0),$$

so that, inverting $Z^2a_0^2/c^2=\tfrac{8\pi G}{3}\rho_{\rm DE}$ with $Z^2=32\pi/3$, the dark-energy mass density is $\rho_{\rm DE}(z)=4a_0^2(z)/(Gc^2)$ and

$$\boxed{\;a_0(z)=\tfrac{c}{2}\sqrt{G\,\rho_{\rm DE}(z)}\;=\;c^2\sqrt{\Lambda_{\rm eff}(z)/32\pi}\quad\Longrightarrow\quad \frac{a_0(z)}{a_0(0)}=\sqrt{\frac{\rho_{\rm DE}(z)}{\rho_{\rm DE,0}}}\;}$$

The SI form $\tfrac{c}{2}\sqrt{G\rho_{\rm DE}}$ uses the dark-energy *mass* density $\rho_{\rm DE}$ (kg m$^{-3}$); the equivalent geometric form uses $\Lambda_{\rm eff}\equiv8\pi G\rho_{\rm DE}/c^2$ (units m$^{-2}$). Both give $a_0^{\rm canon}=9.355\times10^{-11}$ at $z=0$ on Planck $\rho_{\rm DE,0}$; the two conventions must not be mixed ($c^2\sqrt{\rho_{\rm DE}/32\pi}$ with a *mass* density is dimensionally inconsistent). The redshift-tracking ratio $a_0(z)/a_0(0)=\sqrt{\rho_{\rm DE}(z)/\rho_{\rm DE,0}}$ is convention-independent.

On the supernova side this adds **no free dark-energy parameter** — against $\Lambda$CDM's $\Omega_\Lambda$ (and, in the evolving-DE extension, $w_0,w_a$). The framework does not, however, produce a parameter-free dark-energy history from nothing: it *consumes* whatever $\rho_{\rm DE}(z)$ the cosmic data prefer (itself the $w_0,w_a$ fit to distances) and requires that the *same* function reproduce the galaxy-side $a_0(z)$. The content is therefore a cross-*dataset* constraint — one $\rho_{\rm DE}(z)$ must simultaneously fit cosmic distances and galaxy kinematics — not a first-principles prediction of $w(z)$. At $z=0$ the framework is identical to $\Lambda$CDM by construction ($Z^2a_0^2/c^2=\Lambda c^2/3$). It differs from $\Lambda$CDM only if $a_0(z)$ evolves — that is, only if the galaxy acceleration scale changes with redshift in lock-step with the cosmic dark-energy density.

### 1.3 The non-circular cross-scale idea

$\Lambda$CDM gives no reason for a galaxy's internal acceleration scale to track cosmic expansion; the framework forces exactly that link. Crucially, the equality of a galaxy $a_0$ and a cosmic $\Lambda$ at a *single* epoch is a definition — one can always convert one into the other, and reading agreement there is circular. The genuine, non-circular test is whether **two independently measured functions of redshift** — $a_0$ from galaxy kinematics and $\rho_{\rm DE}$ from cosmic distances — track each other as $z$ varies. That $z$-tracking is a prediction $\Lambda$CDM cannot make and the framework cannot avoid. The framework *inherits* the dark-energy history $w(z)$ (it does not predict $w(z)$); its content is the tie between the two datasets, so any decline it exhibits is a consequence of the framework relation combined with the measured $w(z)$, not an independent statement about dark energy.

### 1.4 Credit for the kernel, and the status of this paper

The low-acceleration interpolation used to read $a_0$ from rotation curves, $\nu(y)=\sqrt{1+1/y}$ with $y=g_{\rm bar}/a_0$, is Milgrom's (1999, *Phys. Lett. A* **253**, 273, Eq. 9), in the original MOND context of Milgrom (1983). Milgrom's coefficient was $2cH_\Lambda$ rather than $cH_\Lambda/Z$; the deep-MOND limit $V^4=a_0\,GM_{\rm bar}$ that anchors the galaxy-side measurement here is the baryonic Tully–Fisher relation (McGaugh 2005, 2012; Lelli, McGaugh & Schombert 2016). The distinctive content the present framework contributes is the $cH_\Lambda/Z$ coefficient and the $a_0\!\leftrightarrow\!\rho_{\rm DE}(z)$ tie under test. This is a **method + forecast paper reporting a non-detection** with a live cosmology-side hint and a strategic finding; it is not, and does not claim to be, a detection. All load-bearing numbers are produced by committed, exit-0 scripts (Appendix A), and both footings are carried throughout.

---

## 2. The relation and why it is non-circular

**Terminology.** *Footing* — the choice of density that sets the $a_0$ *magnitude*: canonical (pure $\rho_{\rm DE}$, $9.36\times10^{-11}$) or ALT (total present-day density, $1.13\times10^{-10}$); the two are $20.9\%$ apart and cancel in any ratio. *Deep-MOND* — the low-acceleration regime $g\ll a_0$, where $\nu\to\sqrt{a_0/g}$ and $V^4=a_0GM_{\rm bar}$ holds with fitted slope exactly $4$. *BTFR zero-point* — the normalization of $V^4=a_0GM_{\rm bar}$; in the deep-MOND limit that zero-point *is* $a_0$, so reading $a_0(z)$ and reading the BTFR zero-point are the same operation. *Common-mode* — a systematic applied identically across a sample (one $\alpha_{\rm CO}$/IMF/dust prescription), which does not average down with sample size $N$.

### 2.1 The two-dataset bridge

Write the framework tie as a bridge between measurements made on wholly different physical scales:

$$\underbrace{a_0(z)}_{\text{galaxy kinematics: BTFR zero-point}}\;=\;\tfrac{c}{2}\sqrt{G\,\rho_{\rm DE}(z)}\;=\;\underbrace{\tfrac{c}{2}\sqrt{G\,\rho_{\rm DE}(z)}}_{\text{cosmic distances: SNe / DESI }\rho_{\rm DE}(z)}.$$

The left side is read from the internal dynamics of individual galaxies (parsec–kiloparsec scales); the right side is read from the expansion history (gigaparsec scales). $\Lambda$CDM contains no relation forcing these to agree at all, let alone to co-evolve. The framework forces both their $z=0$ equality and their joint $z$-dependence.

### 2.2 Definition versus test

The $z=0$ equality $a_0(0)=(c/2)\sqrt{G\rho_{\rm DE,0}}$ is definitional: given a cosmic $\rho_{\rm DE,0}$ one *defines* the horizon $a_0$, so a $z=0$ match is a consistency knot, not an independent success. Its value is as the anchor the bridge extends from — if it failed badly the whole construction would be dead on arrival — but it carries no evidential weight beyond internal consistency. The non-circular content is entirely in the *slope*: does galaxy-measured $a_0(z)$ decline (or stay flat, or rise) in the same way the independently measured cosmic $\rho_{\rm DE}(z)$ does? Because the two datasets never share inputs, a wrong background assumption shifts both together and cannot manufacture a spurious co-evolution (quantified in §4.4).

### 2.3 What the framework predicts, and what it inherits

At fixed $z$ the framework prediction is fully specified once $\rho_{\rm DE}(z)$ is chosen. Two reference cosmic tracks bracket the question:

| track | $(w_0,w_a)$ | $a_0(3)/a_0(0)$ | $a_0(3.25)/a_0(0)$ |
|---|---|---|---|
| flat-$\Lambda$ ($w=-1$) | $(-1.00,\,0.00)$ | $1.000$ (flat) | $1.000$ |
| DESI-DR2 evolving | $(-0.75,\,-0.90)$ | $0.712$ (declining) | $0.685$ |
| *(ALT $cH(z)$ evolution model, for contrast)* | $a_0\propto cH(z)=cH_0E(z)$ | $4.57$ (rising) | $4.99$ |

with CPL history $\rho_{\rm DE}(z)/\rho_{\rm DE,0}=(1+z)^{3(1+w_0+w_a)}\exp[-3w_az/(1+z)]$. The framework's distinctive canonical-footing prediction is a **mild decline**, $a_0(3)/a_0(0)\approx0.60$–$0.75$, if the DESI-preferred evolving dark energy is real. If instead $w\to-1$ (flat), the framework reduces to $\Lambda$CDM at all $z$ and the distinctive signal vanishes, leaving only the $z=0$ tie. The third row is **not** the ALT $z=0$ normalization ($a_0^{\rm ALT}=1.131\times10^{-10}$) but a distinct *evolution model* in which $a_0$ tracks the total-density Hubble rate $cH(z)$ and therefore *rises* steeply — the opposite sign — and it is the one branch the current galaxy data can already address (§4.3). The ALT $z=0$ normalization itself, if it instead tracked $\rho_{\rm DE}(z)$, would decline like the canonical footing and is *not* excluded; only the rising $cH(z)$ evolution is even approached by the current galaxy data — and, as §4.2 (v2) shows, only on the discovery-paper masses. The flat–DESI separation is only $0.147$ dex at $z=3$ ($0.164$ dex at $z=3.25$); that small gap is what the galaxy data must resolve.

A theory-side caveat bounds the whole construction. The horizon relation $a_0=cH_\Lambda/Z$ is derived for a *static* de Sitter horizon (constant $\Lambda$). Promoting it to $a_0(z)=\tfrac{c}{2}\sqrt{G\rho_{\rm DE}(z)}$ for an evolving equation of state ($w\ne-1$) is an **adiabatic / instantaneous-horizon ansatz** — the assumption that the inertia scale tracks the instantaneous dark-energy density — not a result derived from the de Sitter–Unruh construction, whose horizon is that of a constant-$\Lambda$ background. The $z$-tracking under test is therefore a test of this ansatz combined with the measured $w(z)$; a null would disfavour the ansatz, not the static-horizon relation it reduces to at $z=0$.

---

## 3. The $z=0$ tie and the cosmology side

### 3.1 The $z=0$ tie

The $\Lambda$-blind galaxy $a_0(0)$ is taken from the gas-dominated SPARC BTFR zero-point measured without any cosmological-$\Lambda$ input (the companion $a_0$-line/$\Lambda$ paper, Zimmerman 2026, DOI 10.5281/zenodo.21419735): $a_0(0)=1.181\times10^{-10}\,{\rm m\,s^{-2}}\,(\pm16\%)$. The cosmic-side prediction is $a_0(0)=(c/2)\sqrt{G\rho_{\rm DE,0}}$ with $\rho_{\rm DE,0}=\Omega_{\rm DE}\,3H_0^2/(8\pi G)$:

| footing | cosmic $a_0(0)$ | $a_{0,\rm SPARC}/a_{0,\rm cosmic}$ | tension |
|---|---|---|---|
| Planck ($\Omega_{\rm DE}=0.685,\,H_0=67.4$) | $9.36\times10^{-11}$ | $1.26$ | $1.44\sigma$ |
| SH0ES-$H_0$ ($\Omega_{\rm DE}=0.685,\,H_0=73.0$) | $1.01\times10^{-10}$ | $1.17$ | $0.95\sigma$ |

The tie **holds at $\sim1\sigma$** on the canonical (Planck-$H_0$) footing and slightly better ($0.95\sigma$) at the local $H_0$. This is by construction — the definitional anchor — and holds. It re-states that the framework enters the high-$z$ test on solid $z=0$ footing, and carries no evidential weight beyond that internal consistency.

### 3.2 The cosmology side: DESI DR2 propagated

On the cosmic side there is no free dark-energy parameter to fit — the framework consumes whatever $\rho_{\rm DE}(z)$ the data prefer. We propagate the DESI DR2 (2025, arXiv:2503.14738) $w_0w_a$CDM posterior (BAO + CMB + SNe; representative marginals with $w_0$–$w_a$ correlation $\approx-0.87$; $\Lambda$CDM excluded at $2.8\sigma$/Pantheon+, $4.2\sigma$/DESY5, $3.8\sigma$/Union3) through $a_0(z)/a_0(0)=\sqrt{\rho_{\rm DE}(z)/\rho_{\rm DE,0}}$ (Appendix A, `desi_posterior_a0z.py`):

| SNe combination | $a_0(3)/a_0(0)$ | $[16\%,84\%]$ | $P(a_0\text{ declines})$ | decline signif. | in $0.60$–$0.75$ |
|---|---|---|---|---|---|
| DESI+CMB+Pantheon+ | $0.775$ | $[0.683,\,0.878]$ | $97.9\%$ | $2.0\sigma$ | $38\%$ |
| DESI+CMB+DESY5 | $0.737$ | $[0.651,\,0.833]$ | $99.3\%$ | $2.5\sigma$ | $51\%$ |
| DESI+CMB+Union3 | $0.707$ | $[0.599,\,0.831]$ | $98.3\%$ | $2.1\sigma$ | $48\%$ |

Across the three combinations the median is $a_0(3)/a_0(0)\simeq0.74$ with a $\sim2.2\sigma$ decline, and all three posteriors overlap the framework's $0.60$–$0.75$ band. This is a genuine, *live* cosmology-side hint: **if** the DESI evolving-dark-energy signal is real, the induced $a_0(z)$ decline falls squarely inside the framework's $0.60$–$0.75$ band. It is not, however, an independent test — it is a re-expression of the DESI $w(z)$ result through the framework relation, the *same* DESI information seen twice, and it therefore **cannot be added to the galaxy-side $\chi^2$** as if it were a second measurement. It dissolves entirely if the DESI signal regresses to $w=-1$. It sharpens the *target* for the galaxy side; it does not by itself confront it.

---

## 4. The galaxy-side $a_0(z)$ from the high-$z$ BTFR

### 4.1 The estimator

On the galaxy side, $a_0(z)$ is read from the BTFR zero-point at each redshift. In the deep-MOND regime $V^4=a_0\,GM_{\rm bar}$ is exact (the fitted slope is forced to $4$), so at fixed circular velocity

$$\frac{a_0(z)}{a_0(0)}=\frac{(V_z/V_0)^4}{M_{{\rm bar},z}/M_{{\rm bar},0}},\qquad\text{equivalently}\qquad \Delta\log a_0=-\,\Delta\log M_{\rm bar}\big|_{\text{fixed }V}.$$

Reading $a_0(z)$ is therefore the same operation as reading the BTFR zero-point. The estimator is valid **only** where the fitted slope is genuinely $4$, i.e. for objects deep in the low-acceleration regime $g\ll a_0$.

### 4.2 The one clean high-$z$ datum: the Big Wheel at $z=3.25$

A single clean deep-MOND high-$z$ rotator is currently available — the Big Wheel (Wang et al. 2025, *Nature Astronomy* **9**, 710; $z=3.2514$; arXiv:2409.17956), a large, low-acceleration disk whose outer rotation curve satisfies the deep-MOND condition. Monte-Carlo over its velocity and baryonic-mass systematics ($V_{\rm rot}=280\pm31\,{\rm km\,s^{-1}}$, $\sigma_{\rm int}=61\,{\rm km\,s^{-1}}$ with asymmetric-drift correction; $M_\star=1.7\pm0.7\times10^{11}M_\odot$, dynamically capped; $M_{\rm gas}=1.8\pm0.9\times10^{11}M_\odot$, $\times1.36$ He) gives $a_{0,\rm eff}=1.54\,(+1.10/-0.61)\times10^{-10}\,{\rm m\,s^{-2}}$, i.e.

| footing | $a_0(3.25)/a_0(0)$ |
|---|---|
| SPARC $1.181\times10^{-10}$ | $1.31\,(+0.93/-0.52)$ |
| canonical $0.936\times10^{-10}$ ($\rho_{\rm DE}/cH_\Lambda$) | $1.65\,(+1.17/-0.65)$ |
| ALT $1.131\times10^{-10}$ ($\rho_{\rm tot}/cH_0$) | $1.37\,(+0.97/-0.54)$ |

On **every** footing the discovery-mass ratio is consistent with a constant ($1.0$) and with the DESI decline ($0.68$), while it **disfavors the rising $cH(z)$ evolution model ($\sim5\times$) at $\sim2\sigma$** (banked posterior probability $\sim1$–$3\%$). This was a real, if narrow, result *on the discovery-paper masses* — but it is **not robust to the v2 dynamical model** (Update below): under Quadri et al.'s fiducial stellar mass the object sits at ratio $3.1\,[1.9,4.7]$, itself a $\sim3\times$ rise only $\sim1.2\sigma$ from the $\sim5\times$ track, so the rise-exclusion too is $M_{\rm bar}$-hostage. (The claim that reaching $5\times$ needs $M_{\rm bar}$ wrong by $\sim0.7$ dex assumed the discovery masses; the $0.37$-dex dynamical-vs-SED ambiguity alone already spans most of that.)

What it cannot do is separate the $0.70$ decline from flat. The $M_{\rm bar}$ systematic on a single object ($\approx0.3$ dex in $M_{\rm bar}$, propagating to $\approx0.23$ dex in the combined $a_0$ error) is itself larger than the $0.164$-dex flat-vs-decline signal at $z=3.25$. Worse, that $0.226$-dex error is a *floor*: it holds the asymmetric-drift coefficient fixed at $\alpha=3.4$ rather than Monte-Carloing it, whereas varying $\alpha$ moves the ratio from $0.95$ ($\alpha=0$) to $1.27$ ($\alpha=3.4$) — a further $\sim0.1$–$0.15$ dex — so the true error is somewhat larger and the datum even less constraining (the omitted term also pushes $a_0$ *up*, i.e. anti-framework, so it does not rescue a "win"). We use the anti-framework choices at every fork: the dynamically capped stellar mass, which pushes the ratio *up* (the Monte-Carlo median is $1.31$; the capped-mass point value alone is $1.27$; the full-SED stellar mass would instead place it at $0.86$, right on the DESI decline), and a high asymmetric-drift correction — and the datum still lands consistent with both tracks.

One further systematic works in the framework's favour and is *not* applied to the central value, so the quoted ratio is conservative. The estimator $a_{0,\rm eff}\equiv V^4/(GM_{\rm bar})$ equals $a_0$ *only* in the deep-MOND limit $g_{\rm bar}\ll a_0$. On the framework's own interpolation $g_{\rm obs}^2=g_{\rm bar}^2+g_{\rm bar}a_0$ one has exactly $a_{0,\rm eff}=g_{\rm obs}^2/g_{\rm bar}=g_{\rm bar}+a_0$, so the estimator *overstates* $a_0$ by $g_{\rm bar}$ whenever the rotation-curve point is not deeply in the MOND regime. For the Big Wheel ($M_{\rm bar}\approx4.1\times10^{11}M_\odot$, outer point at $R\sim30$–$45$ kpc) $g_{\rm bar}\approx0.3$–$0.5\,a_0$, so $a_{0,\rm eff}$ is biased high by $\sim30$–$50\%$: subtracting $g_{\rm bar}$ moves the datum from $a_{0,\rm eff}=1.54\times10^{-10}$ (ratio $1.31$) toward $a_0\approx1.1$–$1.2\times10^{-10}$ (ratio $\approx1.0$), i.e. *closer* to flat and to the decline, and *further* from the rise. The "clean deep-MOND" label is therefore optimistic for this single transitional object — the correct treatment uses the full $\nu$-kernel at the measured $g_{\rm bar}/a_0$, not the deep-MOND asymptote — but the direction of the correction only reinforces the "consistent-with-both" reading, and the actual outer-RC radius (hence $g_{\rm bar}/a_0$) should be pinned before this datum is used quantitatively (the rise-exclusion, and the radius, are both revisited in the Update below, which supersedes this estimate).

**Update (v2): the 2026 ALMA dynamical model.** A dedicated dynamical model of the Big Wheel from deep ALMA CO kinematics (Quadri et al. 2026, *A&A*, arXiv:2605.04144; W. Wang among the authors) now supersedes the discovery-paper inputs: a mildly *rising* rotation curve reaching $V_{\rm rot}\approx314\,{\rm km\,s^{-1}}$ at the outermost **measured** radius $\approx16.5$ kpc (the $20$ and $35$ kpc values are angular-momentum *extrapolations*, not measured RC points), $M_{\rm gas}=10^{10.76}M_\odot$, and — critically — a stellar mass ambiguous by $0.37$ dex: the dynamical-model fiducial $M_\star=10^{11.00}M_\odot$ versus a higher SED/half-mass value $M_\star=10^{11.37}M_\odot$ that the authors flag as *in tension* with the dynamics. Applying the framework's exact $a_0$-line kernel $a_0=(g_{\rm obs}^2-g_{\rm bar}^2)/g_{\rm bar}$ at the measured $16.5$ kpc point (the $\nu$-kernel correction advocated above), the inferred $a_0$ swings from ratio $0.86$ (SED $M_\star$, $a_0\simeq1.0\times10^{-10}$) to $3.25$ (dynamical $M_\star$, $a_0\simeq3.8\times10^{-10}$) at central values — Monte-Carlo medians $1.28\,[0.41,2.60]$ and $3.11\,[1.89,4.71]$ respectively, with $\sim28\%$ of the SED-$M_\star$ posterior unphysical ($g_{\rm bar}>g_{\rm obs}$: baryons over-predicting the rotation). The object sits at $y=g_{\rm bar}/a_0\approx0.7$–$1.3$ — transitional, *not* deep-MOND — so $a_0$ is hyper-sensitive to $M_{\rm bar}$, and the $0.37$-dex stellar-mass ambiguity *alone* spans a factor $\sim3.8$ in $a_0$. This does **not** tighten the datum. It *empirically confirms* the paper's central finding (§5) on the very object one would reach for: with new, dedicated dynamical data the single Big Wheel $a_0$ remains $M_{\rm bar}$-hostage and cannot separate the framework's $\sim0.68$ decline at $z=3.25$ (§2.3) from a strong rise. It is an honest downgrade of the one in-hand galaxy-side value — the discovery-based Monte-Carlo had placed it at $1.31$, which sits inside but no longer characterizes the now much wider range — and it supersedes the $g_{\rm bar}$-subtraction estimate above (which assumed the higher discovery-paper $M_{\rm bar}\approx4.1\times10^{11}M_\odot$; with the lower dynamical $M_{\rm bar}$ the correction can move $a_0$ either way, dominated by the $M_\star$ choice). Backed by `bigwheel_update.py` (Appendix A).

### 4.3 Why intermediate-$z$ is not a clean $a_0$ probe

The temptation is to add the many $z\sim0.5$–$2.3$ rotating disks (e.g. KMOS$^{3\rm D}$). They do not help, for a physical reason: these massive rotators sit at $g\gtrsim a_0$, **not** deep-MOND, so their fitted BTFR slopes are $3.0$–$3.85$, not $4$, and the zero-point is then degenerate with the slope, the pivot, and baryon/dark-matter-fraction evolution. The inferred "$a_0$ evolution" *flips sign with the analysis choice*:

- Übler et al. (2017, KMOS$^{3\rm D}$, fixed local slope $3.75$) $\to$ zero-point $\sim0.3$–$0.4$ dex below local $\to$ naive map reads $a_0$ **rising** $\sim2$–$3\times$;
- Sharma et al. (2024, free slope $3.21$) $\to$ zero-point above local at their pivot $\to$ **opposite** sign;
- Di Teodoro et al. (2016) and Tiley et al. (2019, $V/\sigma>3$) $\to$ **null**, no significant zero-point evolution.

The scatter across analyses (a factor $\sim2$–$3$, in *either* direction) dwarfs the $0.70$-vs-$1.0$ signal. These points are not valid $a_0$ readouts; where we include the $z\approx2.3$ point in the joint fit we place it at its fixed-slope value $1.86$ (rising — the *wrong* sign for the framework decline), so it counts against, not for, the framework.

### 4.4 The $a_0=M_{\rm bar}$ degeneracy and the mild distance dependence

Because $\Delta\log a_0=-\Delta\log M_{\rm bar}$ at fixed $V$, a mis-estimate of the baryonic mass propagates $1{:}1$ into $a_0$: the two are algebraically degenerate for this estimator. Rising molecular-gas fractions ($\sim10\%$ at $z=0$ to $\sim50\%$ at $z=2$), the CO-to-H$_2$ conversion $\alpha_{\rm CO}$, dust, and IMF evolution all move the BTFR zero-point and are indistinguishable from an $a_0$ shift with the BTFR / point-mass method. This is the crux limitation of §5. The mild distance–cosmology dependence is separate and quantified: $M_{\rm bar}\propto D^2$, and the ratio $D(\text{DESI})/D(\text{flat})$ shifts $M_{\rm bar}$ by $\le0.015$ dex at $z=1$ (smaller at higher $z$) — roughly $10\times$ below the signal and $15\times$ below the Big-Wheel error. A wrong background moves all points together and cannot manufacture a decline, so the test is **not circular in the fatal sense**: testing whether $a_0$ tracks $\rho_{\rm DE}$ is not the same as assuming the DE evolution.

### 4.5 Does the galaxy data show the decline?

No — neither way. Assembling the honest galaxy points (Appendix A, `confront.py`):

| set | $\chi^2(\text{flat})$ | $\chi^2(\text{DESI-decl})$ | $\Delta\chi^2$ | lean |
|---|---|---|---|---|
| all 4 points | $1.08$ | $3.05$ | $-1.97$ | flat, weak |
| deep-MOND candidate only ($z=0$ + Big Wheel, discovery masses; transitional per §4.2/v2) | $0.27$ | $1.55$ | $-1.28$ | flat, weak |

The clean-only row ($z=0$ + Big Wheel) is the sole formally meaningful statistic; the "all 4 points" row is **illustrative only**, because the intermediate-$z$ points are declared invalid $a_0$ readouts (§4.3, slope $\ne4$, sign-contested) and the $z=1$ entry is itself the median of a hand-picked literature straddle — quantities that cannot legitimately enter a likelihood. Both rows agree in direction: the data mildly prefer flat, $|\Delta\chi^2|\approx1.3$–$2.0$ — not significant, and what lean exists in the intermediate-$z$ points is toward *rising*, the wrong sign for the framework decline. The distinctive $0.60$–$0.75$ decline is not detected; the data are consistent with both flat and the decline. The one branch the data disfavor is the rising $cH(z)$ evolution model ($\sim2\sigma$, via the Big Wheel *on the discovery-paper masses* — a result the v2 dynamical model itself weakens, since under the fiducial dynamical mass the Big Wheel sits at a $\sim3\times$ rise; §4.2).

---

## 5. The key finding: $M_{\rm bar}$ calibration, not rotator count, is decisive

The decisive question for any future test is how the significance scales. The separability statistic — the maximum sigma at which the *current* errors could ever tell flat from the DESI decline — is

$$S=\sqrt{\sum_i\left[\frac{\log a_0^{\rm flat}(z_i)-\log a_0^{\rm DESI}(z_i)}{\sigma_i}\right]^2}.$$

The current data give $S=0.73\sigma$ (Big Wheel alone), $0.73\sigma$ (clean pair $z=0+3.25$), and $0.80\sigma$ (all four points): **underpowered**, consistent with both tracks. Every galaxy point sits $\le1.2\sigma$ from *both* the flat and the declining track. This is no longer only a forecast: the 2026 ALMA dynamical re-analysis of the Big Wheel (§4.2, Quadri et al. 2026) demonstrates it directly — a $0.37$-dex stellar-mass ambiguity on a single *dedicated-data* object swings its $a_0$ by a factor $\sim3.8$, exactly the $M_{\rm bar}$-hostage behaviour this section predicts, and precisely why more objects at fixed $M_{\rm bar}$ calibration would not help. So more data are needed — but the crucial point is *what kind*.

The naive forecast assumes independent per-object errors that beat down as $1/\sqrt{N}$. The target signal is $-\log_{10}(0.70)=0.155$ dex, requiring $\sigma_{\rm mean}=0.052$ dex for $3\sigma$, hence $N\approx4$ rotators at SPARC-like precision ($0.10$ dex) or $N\approx24$ at realistic high-$z$ per-object precision ($0.25$ dex). **This is wrong**, because the dominant $M_{\rm bar}$ error — $\alpha_{\rm CO}$, IMF, and dust prescriptions applied *identically* to a sample — is largely common-mode, not independent, and a common-mode error does not average down with $N$. With $\sigma_{\rm mean}^2=\sigma_{\rm ind}^2/N+\sigma_{\rm cm}^2$ and a correlated $M_{\rm bar}$ floor $\sigma_{\rm cm}$:

| $M_{\rm bar}$ common-mode floor | $N$ for $3\sigma$ |
|---|---|
| $0.00$ dex | $24$ |
| $0.05$ dex | $\sim377$ |
| $\ge0.08$ dex | **never reaches $3\sigma$ at any $N$** |

Because realistic high-$z$ $M_{\rm bar}$ calibration floors are $\sim0.08$–$0.15$ dex ($\alpha_{\rm CO}$ alone is a $0.1$–$0.2$ dex systematic), the test is decisive **only if the common-mode $M_{\rm bar}$ systematic can be driven below $\sim0.05$ dex** — a calibration problem, not a counting problem. This is the paper's core methodological contribution: **the decisive observational lever is a uniformly calibrated $M_{\rm bar}$ ladder to $\lesssim0.05$ dex common-mode, not the number of rotators.** A uniformly calibrated $M_{\rm bar}$ scale is worth more than dozens of noisy objects. (Both footings enter this identically — the forecast is expressed in ratios and dex, so the $20.9\%$ footing choice cancels; it re-enters only the Big-Wheel absolute of §4.2.)

---

## 6. Forecast and the $a_0$-separable observable

To reach $3\sigma$ on the $0.60$–$0.75$ decline versus flat therefore requires (i) a common-mode $M_{\rm bar}$ calibration $\lesssim0.05$ dex and (ii) a sample of $\sim20$–$40$ clean deep-MOND $z\sim2$–$3$ rotators, Big-Wheel-like, with gas-traced outer rotation curves (JWST/ALMA) or individually resolved deep-MOND curves (ELT/HARMONI). For fixed samples the per-object precision required is $\le0.16$ dex ($N=10$), $\le0.23$ dex ($N=20$), $\le0.33$ dex ($N=40$) — all under the assumption that these errors are independent, which returns the argument to the common-mode floor above. Clean deep-MOND disks like the Big Wheel are rare (the intermediate-$z$ KMOS$^{3\rm D}$ rotators are $g\gtrsim a_0$, §4.3), so assembling $20$–$40$ of them is itself an observational stretch.

The deeper methodological escape is to stop using the BTFR zero-point at all. Because $a_0$ and $M_{\rm bar}$ are $1{:}1$ degenerate in the BTFR, no amount of BTFR data isolates $a_0$ from baryonic-mass evolution. The **$a_0$-separable** observable is the *shape* of the rotation curve — the radial-acceleration-relation transition radius / the full RAR — which depends on $a_0$ at fixed $M_{\rm bar}$ and therefore breaks the degeneracy that the zero-point cannot. A high-$z$ RAR-transition measurement (the acceleration at which the curve departs from the Newtonian-baryonic expectation) reads $a_0$ directly, without hostage to the gas-mass normalization. This is the observable to target: not more BTFR zero-points, but resolved high-$z$ rotation-curve shapes.

---

## 7. Discussion

The cross-scale link is the substance here. $\Lambda$CDM contains no relation forcing a galaxy's internal acceleration scale to equal, or to co-evolve with, the cosmic dark-energy density; the framework forces both. That makes the joint $z$-tracking of galaxy kinematics and cosmic distances a genuine, falsifiable prediction that is not available to $\Lambda$CDM — and it is non-circular precisely because the two datasets never share inputs. The present status is asymmetric between the two scales. On the **cosmology side** the test is live: the DESI DR2 evolving-dark-energy posterior, propagated through the framework relation, produces an $a_0(3)/a_0(0)\simeq0.74$ decline (at $\sim2.2\sigma$) that falls inside the framework's $0.60$–$0.75$ band — but this is a consequence of the framework relation plus the DESI $w(z)$, not an independent measurement, and it stands or falls with the DESI signal. On the **galaxy side** the test is a hostage to $M_{\rm bar}$: the distinctive decline is neither detected nor excluded ($S\simeq0.8\sigma$), the intermediate-$z$ BTFR is systematics-dominated and sign-contested, and the one high-$z$ datum — on the discovery-paper masses — could only disfavor the rising ALT footing, a result the v2 dynamical model itself weakens (§4.2). The honest reading is that the framework's forced bridge is currently underpowered — not passed, not failed — and that the binding constraint is $M_{\rm bar}$ calibration rather than sample size.

Two caveats bound the interpretation. First, the $a_0$ magnitude inherits the posited $Z$; only the ratio/tracking is under test, so a detection of the decline would test the *relation*, not the *value* of $a_0$ or $Z$. Second, the $z=0$ tie is definitional and carries no independent weight; the evidential content is entirely in the slope. The framework is honest both ways: at every fork in the Big-Wheel analysis the anti-framework option is taken, and the datum still lands consistent with both tracks; the adverse rising intermediate-$z$ point is retained in the fit; and the forecast is corrected downward by the common-mode floor.

---

## 8. Conclusion

We have set out a non-circular cross-scale test of de Sitter–Unruh modified inertia: the framework replaces $\Lambda$CDM's free dark-energy fit with the galaxy acceleration scale, $H^2=\tfrac{8\pi G}{3}\rho_m+Z^2a_0^2(z)/c^2$, forcing $a_0(z)/a_0(0)=\sqrt{\rho_{\rm DE}(z)/\rho_{\rm DE,0}}$ — a bridge between galaxy kinematics and cosmic distances that $\Lambda$CDM structurally lacks. The $z=0$ tie holds at $\sim1\sigma$ (SPARC $a_0(0)=1.181\times10^{-10}$ vs cosmic $(c/2)\sqrt{G\rho_{\rm DE,0}}$; ratio $1.26$ Planck-$H_0$, $1.17$ SH0ES-$H_0$), the definitional anchor. The cosmology side is live: the DESI DR2 posterior propagated through the relation yields $a_0(3)/a_0(0)\simeq0.74$ at $\sim2.2\sigma$ — a consequence of the framework tie plus the DESI $w(z)$, not an independent detection, and it dissolves if $w\to-1$. The galaxy side is underpowered: the distinctive $0.60$–$0.75$ decline is neither detected nor excluded ($S\simeq0.8\sigma$); one $z=3.25$ rotator, on the discovery-paper masses, only disfavored the ALT-$cH_0$ rise ($\sim2\sigma$) — and the v2 ALMA dynamical re-analysis (§4.2) shows even that is $M_{\rm bar}$-hostage, with the object at a $\sim3\times$ rise under the fiducial dynamical mass. The central finding is methodological and redirects the observational strategy: in the BTFR estimator $a_0$ is $1{:}1$ degenerate with $M_{\rm bar}$, the dominant systematic is common-mode, and with a $\gtrsim0.08$-dex correlated $M_{\rm bar}$ floor the test never reaches $3\sigma$ at any rotator count. The decisive lever is $M_{\rm bar}$ calibration to $\lesssim0.05$ dex common-mode, and the $a_0$-separable observable is the full rotation-curve / RAR transition, not the BTFR zero-point. The value of $a_0$ and the constant $Z$ are posited, not derived; both footings are carried throughout; and the test is reported honestly as a non-detection with a live cosmology-side hint and a strategic redirection of the future program.

---

## Appendix A: The committed, exit-0 verification scripts

All numbers above are reproduced by three committed scripts (numpy/scipy only, exit 0, both footings), re-run 2026-07-18; the frozen public repository is left read-only and all outputs are written to `prep_2026/a0z_crossscale/`.

**`galaxy_a0z.py`** — the $\Lambda$-blind galaxy-side $a_0(z)$ from the high-$z$ BTFR zero-point. Assembles the $z=0$ SPARC anchor ($1.181\times10^{-10}\pm16\%$), the sign-contested intermediate-$z$ compilation (Übler+2017, Sharma+2024, Di Teodoro+2016, Tiley+2019) with the deep-MOND-validity flag, and the $z=3.25$ Big-Wheel Monte-Carlo ($a_{0,\rm eff}=1.54\,(+1.10/-0.61)\times10^{-10}$). Reports ratios so the footing cancels, and re-enters only the Big-Wheel absolute (SPARC/canonical/ALT $=1.31/1.65/1.37$). Prints the forecast $N\approx4$ (clean) / $N\approx24$ (realistic) and writes `galaxy_a0z.png`.

**`bigwheel_update.py`** (v2) — re-extracts the Big Wheel $a_0$ from the Quadri et al. (2026) ALMA dynamical model via the $a_0$-line kernel $a_0=(g_{\rm obs}^2-g_{\rm bar}^2)/g_{\rm bar}$ at the measured $16.5$ kpc point, for both stellar-mass scenarios ($M_\star=10^{11.00}$ dynamical vs $10^{11.37}$ SED), with Monte-Carlo errors; demonstrates the $M_{\rm bar}$-hostage swing (ratio $a_0/a_0^{\rm SPARC}=0.41$–$4.71$, $\sim28\%$ unphysical at high $M_\star$), the empirical confirmation of §5.

**`confront.py`** — confronts the galaxy $a_0(z)$ against the flat-$\Lambda$ and DESI-DR2 evolving cosmic tracks. Produces the joint $\chi^2$ (all-4: $1.08$ vs $3.05$; clean: $0.27$ vs $1.55$), the separability ($S=0.73/0.73/0.80\sigma$), the $z=0$ tie ($1.26/1.44\sigma$ Planck, $1.17/0.95\sigma$ SH0ES), the both-footings Big-Wheel absolute, and the forecast table — the fixed-$N$ precision requirements **and** the common-mode $M_{\rm bar}$ floor of §5 ($\sigma_{\rm cm}=0\to N\!\approx\!24$; $0.05\to N\!\approx\!377$; $\ge0.08\to$ never reaches $3\sigma$ at any $N$). Bottom line: $S(\text{all})=0.80\sigma\Rightarrow$ underpowered, consistent with both.

**`desi_posterior_a0z.py`** — propagates the DESI DR2 $w_0w_a$CDM posterior (three SNe combinations, correlated $w_0$–$w_a$ via a seeded Cholesky draw) through $a_0(z)/a_0(0)=\sqrt{\rho_{\rm DE}(z)/\rho_{\rm DE,0}}$, giving $a_0(3)/a_0(0)=0.775$ (Pantheon+, $2.0\sigma$), $0.737$ (DESY5, $2.5\sigma$), $0.707$ (Union3, $2.1\sigma$); combined median $\simeq0.74$, decline significance $\sim2.2\sigma$, all overlapping the framework $0.60$–$0.75$ band. The ratio is footing-, $H_0$-, and $M_B$-independent (canonical $\rho_{\rm DE}$ footing by construction; $Z$ cancels).

Supporting reconstructions from an independent lane (`prep_2026/a0z_from_sne/`, `crossscale.py`) confirm that Type Ia supernovae **alone** cannot measure $a_0(z=3)$: the dark-energy residual $E^2-\Omega_m(1+z)^3$ is a difference of large numbers, and the model-independent Gaussian-process reconstruction (Seikel, Clarkson & Smith 2012) is sign-pinned only to $z\approx0.40$. The robust SNe deliverable is $a_0(0)$ ($\simeq9.4\times10^{-11}$ at $H_0=67.4$, $\simeq1.01\times10^{-10}$ at $H_0=73.0$), agreeing with SPARC at $\sim1\sigma$; the $z=3$ decline numbers come from the DESI/model references, not a SNe reconstruction — which is exactly why the two-dataset (galaxy $\times$ cosmic-distance) construction, and not SNe alone, is the test.

---

## References

Brout, D., et al. 2022, *ApJ* **938**, 110 (Pantheon+).

DESI Collaboration 2025, arXiv:2503.14738 ($w_0w_a$CDM; $\Lambda$CDM excluded at $2.8/3.8/4.2\sigma$).

Di Teodoro, E. M., Fraternali, F., & Miller, S. H. 2016, *A&A* **594**, A77.

Lelli, F., McGaugh, S. S., & Schombert, J. M. 2016, *AJ* **152**, 157 (SPARC).

McGaugh, S. S. 2005, *ApJ* **632**, 859; McGaugh, S. S. 2012, *AJ* **143**, 40 (BTFR).

Milgrom, M. 1983, *ApJ* **270**, 365; Milgrom, M. 1999, *Phys. Lett. A* **253**, 273 (the $\nu$-kernel, Eq. 9; astro-ph/9805346).

Seikel, M., Clarkson, C., & Smith, M. 2012, *JCAP* **06**, 036 (Gaussian-process $H(z)$).

Sharma, G., Upadhyaya, V., Salucci, P., & Desai, S. 2024, *A&A* **690** (Tully–Fisher at $0.6\le z\le2.5$; free bTFR slope $3.21\pm0.28$; arXiv:2406.08934).

Tiley, A. L., et al. 2019, *MNRAS* **482**, 2166 (KROSS–SAMI Tully–Fisher across 8 Gyr since $z\approx1$).

Übler, H., et al. 2017, *ApJ* **842**, 121 (KMOS$^{3\rm D}$ bTFR).

Wang, W., et al. 2025, *Nature Astronomy* **9**, 710 (the "Big Wheel" giant disk at $z=3.2514$; arXiv:2409.17956).

Quadri, G., Cantalupo, S., Bacchini, C., et al. 2026, *A&A* (in press), arXiv:2605.04144 (the galaxy–halo connection and dynamical model of the Big Wheel giant disc at $z\simeq3.25$; the v2 dynamical-model input).

Zimmerman, C. 2026, *Reading the Cosmological Constant from Dwarf-Galaxy Rotation Curves: The $a_0$-Line* (self-cite), DOI 10.5281/zenodo.21419735.

Zimmerman, C. 2026, *MI Field Theory Results 2026* (self-cite), DOI 10.5281/zenodo.21403470.
</content>
</invoke>
