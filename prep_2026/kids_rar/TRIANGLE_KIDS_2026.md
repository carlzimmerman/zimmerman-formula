# Three Roads to the Cosmological-Constant Acceleration Scale: Dynamics, Weak-Lensing Geometry, and Expansion — and Why the Lensing Leg Is a Consistency, Not Yet a Free-Fit

**Carl Zimmerman**
*Briar Creek Tech*

---

## Abstract

A single low-acceleration scale $a_0 \sim 1\times10^{-10}\,\mathrm{m\,s^{-2}}$ organizes galaxy rotation curves (the mass-discrepancy–acceleration / radial-acceleration relation), and its numerical coincidence with $c\sqrt{\Lambda}$ has been noted since Milgrom's original papers. In the de Sitter–Unruh modified-inertia framework used here, that coincidence is promoted to an identity, $a_0 = cH_\Lambda / Z$ with $H_\Lambda = c\sqrt{\Lambda/3}$ and $Z=\sqrt{32\pi/3}=5.78881$ *posited*, which inverts to $\Lambda = 32\pi\, a_0^2/c^4$. This note asks whether *three* observational channels with mutually **orthogonal systematics** independently land on the same scale and hence on the same $\Lambda$: (i) **dynamics** — the SPARC rotation-curve $a_0$ (kinematic systematics: stellar $M/L$, inclination, asymmetric drift); (ii) **geometry** — the KiDS-1000 weak-lensing radial-acceleration relation of Brouwer et al. (2021), which reaches $g_{\rm bar}\!\sim\!10^{-15}\,\mathrm{m\,s^{-2}}$, about five decades below $a_0$ and three decades deeper than any rotation curve (shear-calibration and photo-$z$ systematics); and (iii) **expansion** — the $a_0$ demanded by the Type Ia supernova Hubble diagram through the Friedmann dark-energy term (standardization systematics). The three central values span $\approx(0.96\text{–}1.20)\times10^{-10}\,\mathrm{m\,s^{-2}}$ (a $\sim$22% spread; $\sim$30% including the low edge of the SNe range, $0.92\times10^{-10}$), all inside the SPARC systematics box $[0.84,1.36]\times10^{-10}$, and all invert to $\Lambda$ within a factor $\sim$1.6 of the Planck value (KiDS $a_0=1.20\times10^{-10}\Rightarrow\Lambda=1.79\times10^{-52}\,\mathrm{m^{-2}}=1.65\times\Lambda_{\rm Planck}$; Planck sits $0.91\sigma$ from the lensing central value). **We state plainly that this is a consistency + method + forecast note, not a free-fit measurement.** The KiDS leg is a *consistency*: Brouwer adopted $a_0$ (from McGaugh 2016) and tested agreement; a genuine lensing-only free-fit is not yet possible from public data and, from the figure alone, is reading- and scatter-limited to a factor $\sim$2. A tabulated free-fit does not shortcut this: because $a_0\propto g_{\rm obs}^2$ amplifies the per-point scatter, the statistical error alone is $\sim$13–43% ($\sim$43% for the clean reliable sample), comparable to the $\sim$15–25% systematic floor (the $\ge6\sigma$ early/late-type split; the baryonic-mass/deprojection model), so a realistic clean-sample free-fit reaches only $\sim$45% — a modest upgrade on the figure, not a percent-level measurement. Finally, in *modified inertia* the lensing channel does not share the matter metric — it runs through a disformal photon sector — so lensing-$a_0 =$ dynamical-$a_0$ is a *prediction of that completion*, not automatic. The value of $a_0$ and $Z$ are posited, not derived.

---

## 1. Introduction

The radial-acceleration relation (RAR) states that the observed centripetal acceleration in a galaxy, $g_{\rm obs}$, is a tight one-to-one function of the acceleration $g_{\rm bar}$ implied by the baryons alone (Milgrom 1983; McGaugh, Lelli & Schombert 2016; Lelli, McGaugh & Schombert 2016). The relation carries a single scale $a_0\simeq1.2\times10^{-10}\,\mathrm{m\,s^{-2}}$ separating the Newtonian regime $g_{\rm bar}\gg a_0$ from the low-acceleration regime $g_{\rm bar}\ll a_0$ where $g_{\rm obs}\to\sqrt{a_0\,g_{\rm bar}}$. It has been noticed since Milgrom's earliest work that $a_0$ is numerically of order $cH_0$ and of order $c\sqrt{\Lambda}$, i.e. that the dynamical scale coincides with the cosmological-constant scale.

The framework used here takes that coincidence literally. It is a **modified-inertia** theory in which the de Sitter–Unruh temperature of the cosmic horizon sets an inertial floor, giving

$$
a_0 \;=\; \frac{cH_\Lambda}{Z}, \qquad H_\Lambda \equiv c\sqrt{\tfrac{\Lambda}{3}}, \qquad Z=\sqrt{\tfrac{32\pi}{3}} = 5.78881 \ \ (\text{posited}),
$$

with the low-acceleration kernel

$$
g_{\rm obs} \;=\; \sqrt{g_{\rm bar}^2 + g_{\rm bar}\,a_0}\,,
$$

which is algebraically Milgrom's (1999, PLA **253**, 273) $\nu$-kernel $\nu(y)=\sqrt{1+1/y}$; the framework's distinctive content is the coefficient $cH_\Lambda/Z$ (Milgrom's coincidence used $\sim 2cH_0$) together with the modified-inertia completion. Eliminating $H_\Lambda$ gives the inversion used throughout this note,

$$
\boxed{\;\Lambda \;=\; \frac{32\pi\,a_0^2}{c^4}\;}
$$

Because $\Lambda$ scales as $a_0^2$, a factor-$f$ uncertainty on $a_0$ becomes a factor-$f^2$ uncertainty on $\Lambda$; conversely a modest $\sim$30% spread in $a_0$ is a factor $\sim$1.6 in $\Lambda$. We stress at the outset that neither $Z$ nor the *value* of $a_0$ is derived here — both are posited — so what follows tests the *universality of the scale and its inversion to $\Lambda$*, not the origin of the number.

The idea of this paper is simple. If $a_0$ is a genuine constant of nature tied to $\Lambda$, then observables whose systematic errors are unrelated should agree on it. We assemble **three channels**:

- **Dynamics** — rotation-curve kinematics (SPARC).
- **Geometry** — weak gravitational lensing (KiDS-1000).
- **Expansion** — the supernova Hubble diagram.

These three have essentially orthogonal error budgets. Agreement among them is a *cross-check that $\Lambda$CDM does not automatically supply*, because in $\Lambda$CDM the galactic $a_0$ is an emergent feature of feedback-regulated halo assembly with no a-priori link to the value of $\Lambda$ in the Friedmann equation. **This is a consistency + method + forecast note.** We show the triangle closes at the $\sim$30% / factor-1.6 level today, we explain honestly why the lensing leg is presently a *consistency* rather than a free-fit, and we forecast what a proper tabulated free-fit would deliver. Every dimensional number below is reproduced by the committed script `kids_rar_lambda.py` (exit 0) and is quoted for both $a_0$ footings.

Two footings for $a_0$ are carried throughout, as the framework requires: the **canonical** footing $a_0 = cH_\Lambda/Z = 9.355\times10^{-11}\,\mathrm{m\,s^{-2}}$ (in which $\Lambda$ equals the Planck value by construction), and the **alternative** footing $a_0 = 1.1305\times10^{-10}$ (built from $\rho_{\rm total}$ and $cH_0$ rather than $\rho_{\rm DE}$ and $cH_\Lambda$). The measured channels are quoted as measured and then inverted; the footings bracket where the theory *expects* $a_0$ to sit.

---

## 2. The three channels and their orthogonal systematics

### 2.1 Dynamics — the SPARC rotation-curve $a_0$

The sharpest single-number extraction of $a_0$ from rotation curves in this program is the "$a_0$-line" estimator (Zimmerman, DOI 10.5281/zenodo.21419735), which uses the identity

$$
g_{\rm obs}^2 - g_{\rm bar}^2 = a_0\,g_{\rm bar}
$$

(exact for the framework kernel) and reads $a_0$ off the gas-dominated slope, where the stellar $M/L$, distance, and inclination dependences largely cancel in the pairwise estimator. The result is

$$
a_0^{\rm dyn} = 1.181\times10^{-10}\,\mathrm{m\,s^{-2}}, \qquad \text{systematics box } [0.84,\,1.36]\times10^{-10}.
$$

The box is dominated by *kinematic* systematics: the stellar mass-to-light ratio $\Upsilon_*$, disk inclination, and asymmetric-drift / pressure-support corrections. This is the dynamics leg.

### 2.2 Geometry — the KiDS-1000 weak-lensing RAR

Brouwer et al. (2021, A&A **650**, A113; arXiv:2106.11677) constructed the RAR from *weak gravitational lensing* around isolated galaxies in the KiDS-1000 survey, cross-matched with GAMA and with photometric ("KiDS-bright") lens samples. Excess-surface-density profiles convert to $g_{\rm obs}(R)$ out to $\sim$Mpc scales, so the lensing RAR spans

$$
10^{-15}\ \lesssim\ g_{\rm bar}\ \lesssim\ 5\times10^{-12}\ \mathrm{m\,s^{-2}},
$$

roughly **five decades below $a_0$** and about **three decades deeper than the deepest rotation curve**. In 15 logarithmic bins Brouwer show that the *reliable* (spectroscopic GAMA) lensing RAR agrees with the MOND/modified-gravity prediction at the adopted $g_\dagger = a_0 = (1.20\pm0.26)\times10^{-10}$ (McGaugh 2016). The systematics — shear calibration, photometric-redshift errors, source blending, boost/contamination corrections — are *orthogonal* to the kinematic systematics of the dynamics leg. This is the geometry leg, and its numerical value used below is the Brouwer-adopted $a_0=(1.20\pm0.26)\times10^{-10}$.

### 2.3 Expansion — the SNe-demanded $a_0$

In the same framework the Friedmann dark-energy term carries $a_0$ through $Z^2 a_0^2/c^2 = $ (dark-energy density scale), so the Type Ia supernova Hubble diagram *demands* an $a_0$ once $H_0$ is fixed. From the cross-scale $a_0(z)$ analysis (Zimmerman, DOI 10.5281/zenodo.21440407; the `side_by_side` construction), the Pantheon+ diagram over the plausible range $H_0 = 67.4\to73\,\mathrm{km\,s^{-1}\,Mpc^{-1}}$ demands

$$
a_0^{\rm exp}(z{=}0) = (9.17\text{–}9.93)\times10^{-11}\ \mathrm{m\,s^{-2}}\ =\ (0.92\text{–}0.99)\times10^{-10}.
$$

The dominant systematics here are supernova standardization, calibration of the distance ladder, and the choice of $H_0$ — again orthogonal to both other legs. This is the expansion leg.

### 2.4 The triangle and the $\Lambda$ inversions

Collecting the three central values (in units of $10^{-10}\,\mathrm{m\,s^{-2}}$):

| Channel | $a_0$ | Systematics |
|---|---|---|
| Dynamics (SPARC $a_0$-line) | $1.18$, box $[0.84,1.36]$ | $\Upsilon_*$, inclination, asymmetric drift |
| Geometry (KiDS lensing) | $1.20\pm0.26$ | shear calibration, photo-$z$ |
| Expansion (SNe-demanded) | $0.92$–$0.99$ | SNe standardization, $H_0$ |
| *framework canonical* | $0.94$ | $\Lambda=\Lambda_{\rm Planck}$ by construction |

The three measured central values span $\approx(0.96\text{–}1.20)\times10^{-10}$ (a $\sim$22% spread on centrals); including the low edge of the SNe range the full span is $\approx(0.92\text{–}1.20)\times10^{-10}$, i.e. $\sim$22–30% wide. **All three lie inside the SPARC systematics box** $[0.84,1.36]$, and all invert to $\Lambda$ within a factor $\sim$1.6 of the Planck value.

Working the geometry leg explicitly through $\Lambda = 32\pi a_0^2/c^4$:

$$
a_0^{\rm geo} = 1.20\times10^{-10} \Rightarrow \Lambda_{\rm lens} = 1.792\times10^{-52}\,\mathrm{m^{-2}}, \quad \text{range } [1.100,\,2.653]\times10^{-52},
$$

against $\Lambda_{\rm Planck} = 1.089\times10^{-52}\,\mathrm{m^{-2}}$. The ratio is $\Lambda_{\rm lens}/\Lambda_{\rm Planck} = 1.65$ (range $[1.01,2.44]$), and the Planck value sits $0.91\sigma$ from the lensing central value — **consistent**, and on the same "high side of the box" as the SPARC dynamics leg. (This $0.91\sigma$ is computed in $\Lambda$-space with a linearized half-width; the equivalent comparison in $a_0$-space — Planck-equivalent $a_0 = 9.354\times10^{-11}$ against $1.20\pm0.26$ — is $1.02\sigma$. Both are well within $2\sigma$; we quote both frames so the $\Lambda$-space number is not read as the whole story.) In the canonical footing $a_0=9.355\times10^{-11}$ reproduces $\Lambda_{\rm Planck}$ exactly by construction; in the alternative footing $a_0=1.1305\times10^{-10}$ gives $\Lambda=1.59\times10^{-52} = 1.46\times\Lambda_{\rm Planck}$. Three observables with orthogonal systematics agreeing on $a_0$ to $\sim$30% is not a precision match — but it is a genuinely independent third leg on the statement "the scale is universal at $\sim\!\sqrt\Lambda$."

---

## 3. The lensing leg in depth

### 3.1 What Brouwer measured, and the five-decade reach

The lensing RAR is qualitatively different from the kinematic RAR in *where it lives*. Rotation curves probe $g_{\rm bar}$ from $\sim$few$\times10^{-9}$ down to at best $\sim10^{-12}\,\mathrm{m\,s^{-2}}$ in the most extended H\,{\sc i} disks — i.e. barely one to two decades below $a_0$. The KiDS lensing profiles, by stacking excess surface density out to Mpc radii, push $g_{\rm bar}$ down to $\sim10^{-15}\,\mathrm{m\,s^{-2}}$, roughly five decades below $a_0$. This matters for the acceleration-scale program because the *deep* regime is where the interpolation-function ambiguity disappears.

### 3.2 Interpolation-freeness of the deep-regime extraction

Every lensing bin sits deep in the low-acceleration regime ($g_{\rm bar}\ll a_0$), where all viable interpolation kernels collapse onto the same asymptote $g_{\rm obs}\to\sqrt{a_0 g_{\rm bar}}$, so $a_0 = g_{\rm obs}^2/g_{\rm bar}$ independent of kernel choice. Evaluated at $g_{\rm bar}=10^{-15}\,\mathrm{m\,s^{-2}}$ ($y\equiv g_{\rm bar}/a_0 = 8.3\times10^{-6}$):

| Kernel | $g_{\rm obs}$ (m s$^{-2}$) |
|---|---|
| framework $\nu$-kernel $\sqrt{g_{\rm bar}^2+g_{\rm bar}a_0}$ | $3.464116\times10^{-13}$ |
| Brouwer "third-family" $g_{\rm bar}/(1-e^{-\sqrt{y}})$ | $3.469104\times10^{-13}$ |
| pure deep-MOND $\sqrt{a_0 g_{\rm bar}}$ | $3.464102\times10^{-13}$ |

The maximum fractional spread across kernels is $1.44\times10^{-3}$ — about **0.14%**. Five decades deep, the extraction $a_0 = g_{\rm obs}^2/g_{\rm bar}$ is interpolation-free to well below any observational error, and it recovers $1.200\times10^{-10}$ exactly. This is the geometry channel's structural edge over rotation curves, which live near $y\sim1$ where the kernel choice is a real ($\sim$10–20%) systematic. No baryonic effect can mimic $a_0$ this far into the deep regime either — the baryons are $\sim$five decades subdominant.

### 3.3 Why a figure free-fit is reading- and scatter-limited (honest scope)

It is tempting to digitize Brouwer's Fig. 4 and free-fit $a_0$ ourselves. We do **not** present such a number as a measurement, for concrete reasons. Fig. 4 is deep-MOND throughout, so the data lie along a slope-$\tfrac12$ line and $a_0 = g_{\rm obs}^2/g_{\rm bar}$; a small vertical reading error propagates as $\log a_0 = 2\log g_{\rm obs} - \log g_{\rm bar}$, i.e. **doubled**. Two further problems compound this:

- **The KiDS-bright (photometric) sample is selection-biased high.** That the photometric KiDS-bright lens sample carries a photo-$z$ selection bias is Brouwer's own caveat (their §-level discussion of the bright-sample selection, arXiv:2106.11677); the specific number is *our* reading, not theirs. By-eye digitization of that sample gives $a_0\sim1$–$3\times10^{-10}$ (centered near $\sim2\times10^{-10}$), which we attribute to that selection bias plus $\sim$0.1-dex reading error — an artifact, not a measurement.
- **The reliable spectroscopic GAMA sample has large intrinsic scatter.** It tracks MOND at $a_0\sim1.2\times10^{-10}$, but with $\sim$0.2–0.4 dex per point of intrinsic scatter, so even with *perfect* reading a figure free-fit constrains $a_0$ only to a **factor $\sim$2**.

This is precisely why Brouwer **fixed** $a_0$ (adopting McGaugh's value) and tested *consistency* rather than free-fitting it. Our KiDS leg inherits that status: it is a consistency check, not an independent free-fit, and we present it as such.

---

## 4. The forecast: what a tabulated free-fit would deliver

A genuine lensing-only free-fit needs the **per-point tabulated** $(g_{\rm bar}, g_{\rm obs}, \sigma)$ data, not the figure. That table is not cleanly public: there is no VizieR entry, and the KiDS data portal exposes only raw excess-surface-density profiles that require a full lensing-inversion pipeline to turn into $(g_{\rm bar}, g_{\rm obs})$ points. With the table in hand, consider the *statistical* precision from a slope-$\tfrac12$ intercept over $N=15$ bins. In the deep regime $\log g_{\rm obs} = \tfrac12(\log a_0 + \log g_{\rm bar})$, so the intercept has sensitivity $\partial\log g_{\rm obs}/\partial\log a_0 = \tfrac12$ and $a_0 = g_{\rm obs}^2/g_{\rm bar}$ **amplifies** the per-point error by a factor 2:

$$
\sigma_{\log a_0}^{\rm stat} \approx \frac{2\,\sigma_{\rm point}}{\sqrt{N}}\ \Rightarrow\
\begin{cases}
\text{KiDS-bright, } \sigma_{\rm point}=0.10\ \text{dex}: & 0.052\ \text{dex} \approx 13\%\\[4pt]
\text{GAMA reliable, } \sigma_{\rm point}=0.30\ \text{dex}: & 0.155\ \text{dex} \approx 43\%
\end{cases}
$$

So statistical alone is $\sim$13% for the (photo-$z$ biased-high) bright sample and $\sim$43% for the reliable GAMA sample — the factor $a_0\propto g_{\rm obs}^2$ amplifies rather than suppresses the scatter, and the real fitter `fit_kids_rar.py` on synthetic $\sim$0.08-dex data confirms this order (tens of percent, not a few percent). Two systematics sit on top:

- the $\ge6\sigma$ early/late-type RAR split (Section 5) means a single universal $a_0$ is a model choice, not a datum;
- the baryonic-mass estimate and the deprojection / halo-model used to turn stacked $\Delta\Sigma$ into $g_{\rm obs}$ carry their own multiplicative uncertainty.

Taking the systematic floor at $\sim$15–25% and adding in quadrature, statistical and systematic are **comparable — neither dominates**. A realistic tabulated free-fit reaches $a_0$ to $\sim$20–28% for the biased bright sample and $\sim$45–50% for the *clean* late-type/reliable sample. The forecast is therefore honestly mixed: the tabulated data does upgrade the figure — chiefly by removing the reading error and enabling a clean late-type selection — but the gain over the figure's factor-$\sim$2 is **modest for the clean case** ($\sim$45%), not the naive $\sim$20%. It is worth doing when the per-point table becomes public, but it is not a fast route to a percent-level $a_0$. **This paper books the method and the triangle now**; the free-fit is deferred to data availability.

---

## 5. The $\ge6\sigma$ early/late-type split

Brouwer find that early- and late-type galaxies follow RARs that differ by $\ge6\sigma$ at fixed stellar mass $M_*$: at a given $M_*$ the early-types show *excess* $g_{\rm obs}$. Brouwer's own reading is that early-types carry additional unseen baryons — circumgalactic gas with $M_{\rm gas}\sim M_*$ — so that the baryonic $g_{\rm bar}$ is underestimated for them and the "excess" is a missing-baryon artifact rather than a violation of a universal $a_0$.

Either way, this is a **real systematic that must be carried, not footnoted**. If a single $a_0$ is fit across both populations, the split biases and broadens the inferred value; if the excess is truly circumgalactic gas, then the *clean* case for the acceleration-scale program is the **late-type disk sample**, where the baryon census is most complete and the deep-regime lensing points are least contaminated. Our recommended free-fit target (Section 4) is therefore the late-type / disk-selected reliable sample, and the $\sim$15–25% systematic floor already reflects the cost of this split. We do not claim the split is resolved; we claim it is bounded and that the late-type case is the defensible one.

---

## 6. The disformal wrinkle: the honest limit on independence

There is a framework-specific subtlety that sets the *honest ceiling* on how "independent" the geometry leg can be. In ordinary single-metric modified gravity (e.g. an AeST/relativistic-MOND realization), photons and matter share one metric, so a lensing RAR and a dynamical RAR test the *same* function and lensing-$a_0 = $ dynamical-$a_0$ is essentially trivial. In **modified inertia**, this is not the case.

Here the modification lives in the inertial sector — the response of test bodies — not in a single spacetime metric. Light does *not* automatically feel the same effective geometry as slow matter. In this program the photon sector is a published **disformal** completion,

$$
\tilde g_{\mu\nu} = g_{\mu\nu} + B\,u_\mu u_\nu,
$$

with $B$ fixed by the same kernel $K(\Box_u)$ that controls the inertial response (the lensing no-go, DOI 10.5281/zenodo.21418816, and the disformal completion; the MI field-theory results, DOI 10.5281/zenodo.21403470). Consequently, **lensing-$a_0 =$ dynamical-$a_0$ is a *prediction* of that disformal construction, not an automatic consequence of the low-acceleration kernel.** This has two honest implications, in both directions:

1. **Bonus test.** The KiDS agreement is a *consistency test of the disformal photon sector*: it is a non-trivial check that lensing and dynamics share the same scale, which the modified-inertia completion has to arrange and could in principle have failed. That is a genuine feather in the completion's cap.
2. **Not an independent derivation.** Precisely because the equality is engineered by the disformal sector, the KiDS leg is **not an independent derivation of "$\Lambda$ sets $a_0$."** It is consistent *with* that statement *given* the disformal completion; it does not establish it from lensing alone. The geometry leg is therefore "independent" in its *systematics* (shear/photo-$z$ vs. kinematics) but *conditional* in its *theory* (it presumes the disformal sector).

Stating this plainly is the point: the triangle is a strong consistency web, and the value of $a_0$ together with $Z$ remain **posited**, not derived. The three legs test the *universality of the scale and its inversion to $\Lambda$*, not the origin of the number.

---

## 7. Discussion

**What the triangle buys.** Three channels — kinematics, lensing geometry, expansion — with orthogonal systematic budgets agree on $a_0$ to $\sim$22–30%, and all invert to $\Lambda$ within a factor $\sim$1.6 of the Planck value, with Planck sitting $0.91\sigma$ from the lensing central. Notably, the dynamics and geometry legs land on the *same high side* of the box ($1.18$ and $1.20$), while the expansion leg and the canonical footing land low ($0.92$–$0.99$ and $0.94$). This is a self-consistent picture: a modest $\sim$20% upward shift in the measured galactic/lensing $a_0$ relative to the pure-$\Lambda$ canonical value maps, through $\Lambda\propto a_0^2$, to the factor-$\sim$1.6 excess in the inferred $\Lambda$ — the same "high-side" behavior in both the dynamics and the geometry legs, and comfortably within their systematics.

**A link $\Lambda$CDM does not supply.** In $\Lambda$CDM the galactic $a_0$ emerges from baryonic-feedback-regulated halo structure and has no built-in numerical tie to the Friedmann $\Lambda$; the coincidence $a_0\sim c\sqrt\Lambda$ is, within that model, a coincidence. The framework here makes the tie structural via $\Lambda = 32\pi a_0^2/c^4$, and the triangle is the observational face of that tie. We claim this as a *motivating consistency*, not as evidence that the framework is correct — the value of $a_0$ and $Z$ are posited.

**What sharpens it.** In order of leverage: (1) the tabulated KiDS per-point data, enabling a clean late-type free-fit — a modest upgrade to $\sim$45% given the scatter amplification, Section 4, chiefly valuable for removing reading error and enabling the late-type cut; (2) reduction of the SPARC box below $\sim$20% via better $\Upsilon_*$ and inclination control, which the pairwise $a_0$-line estimator is designed to exploit; (3) tightening the SNe/expansion leg through the $H_0$ range, which currently drives most of the $0.92$–$0.99$ spread; and (4) an internal test of the disformal sector that would convert the geometry leg from "conditional on the completion" toward "independent." Any one of these narrows the triangle. We flag honestly that the reach toward a $\sim$10% cross-check would be carried almost entirely by the **SPARC-box (2) and SNe/expansion (3) legs**: with the lensing free-fit now capped at $\sim$45% for the clean late-type sample (Section 4), the geometry leg no longer contributes to reaching $\sim$10% — its value is as a *systematics-orthogonal* and *deep-regime, interpolation-free* cross-check, not as a precision anchor. So "$\sim$10%" is aspirational for the dynamics+expansion pair, with lensing supplying independence rather than tightness.

**Caveats restated.** The KiDS leg is a *consistency*, not a free-fit (Brouwer adopted $a_0$); a figure free-fit is reading/scatter-limited to a factor $\sim$2; the $\ge6\sigma$ early/late split strains a single universal $a_0$ and confines the clean case to late-type disks; and the disformal wrinkle caps the geometry leg's independence. None of these is fatal, and none is hidden.

---

## 8. Conclusion

Three observational roads to the low-acceleration scale — rotation-curve **dynamics**, weak-lensing **geometry**, and the **expansion** history — meet at $a_0\approx(0.92\text{–}1.20)\times10^{-10}\,\mathrm{m\,s^{-2}}$, a $\sim$22–30% spread that lies entirely inside the SPARC systematics box and inverts, through $\Lambda = 32\pi a_0^2/c^4$, to a cosmological constant within a factor $\sim$1.6 of the Planck value ($\Lambda_{\rm Planck}$ at $0.91\sigma$ from the lensing central). Because the three legs' systematics are mutually orthogonal, their agreement is a non-trivial consistency web on the statement that the acceleration scale is universal and set by $\sqrt\Lambda$.

We have been deliberate about scope. This is a **consistency + method + forecast note, not a free-fit measurement.** The lensing leg is a *consistency* — Brouwer adopted $a_0$ and tested agreement — and a genuine lensing free-fit awaits per-point data (forecast: $\sim$45% for the clean late-type sample, since the $a_0\propto g_{\rm obs}^2$ scatter amplification leaves statistical and systematic errors comparable). The $\ge6\sigma$ early/late-type split is a real strain that makes late-type disks the clean case. And in modified inertia the lensing–dynamics equality is a *prediction of the disformal photon sector*, not automatic, so the geometry leg is independent in its systematics but conditional in its theory. The value of $a_0$ and the constant $Z=\sqrt{32\pi/3}$ are **posited, not derived**; the triangle tests universality and scale, not the origin of the number. What the note books is the method and the current state of the three-channel agreement, so that the sharpening steps — chiefly the tabulated KiDS free-fit — have a clear target.

---

## References

- Brouwer, M. M., et al. 2021, *The weak lensing radial acceleration relation: Constraining modified gravity and cold dark matter theories with KiDS-1000*, A&A **650**, A113 (arXiv:2106.11677).
- Lelli, F., McGaugh, S. S., & Schombert, J. M. 2016, *SPARC: Mass Models for 175 Disk Galaxies with Spitzer Photometry and Accurate Rotation Curves*, AJ **152**, 157.
- McGaugh, S. S., Lelli, F., & Schombert, J. M. 2016, *The Radial Acceleration Relation in Rotationally Supported Galaxies*, PRL **117**, 201101.
- Milgrom, M. 1983, *A modification of the Newtonian dynamics as a possible alternative to the hidden mass hypothesis*, ApJ **270**, 365.
- Milgrom, M. 1999, *The modified dynamics as a vacuum effect*, Physics Letters A **253**, 273 (the $\nu$-kernel wellhead).
- Planck Collaboration 2020, *Planck 2018 results. VI. Cosmological parameters*, A&A **641**, A6.
- Zimmerman, C. 2026, *The $a_0$-line: a slope estimator for the cosmological acceleration scale from SPARC, and its inversion to $\Lambda$*, Zenodo, DOI 10.5281/zenodo.21419735.
- Zimmerman, C. 2026, *Cross-scale $a_0(z)$: the supernova-demanded acceleration scale and its expansion-history footing*, Zenodo, DOI 10.5281/zenodo.21440407.
- Zimmerman, C. 2026, *Modified-inertia field-theory results*, Zenodo, DOI 10.5281/zenodo.21403470.
- Zimmerman, C. 2026, *A lensing no-go and the disformal photon completion*, Zenodo, DOI 10.5281/zenodo.21418816.

---

*Reproducibility: every dimensional quantity in this note is emitted by the committed script `kids_rar_lambda.py` (exit 0). $a_0$ is carried on both footings (canonical $a_0=cH_\Lambda/Z=9.355\times10^{-11}$; alternative $a_0=1.1305\times10^{-10}$). No claim of derivation is made for $a_0$ or $Z$.*
