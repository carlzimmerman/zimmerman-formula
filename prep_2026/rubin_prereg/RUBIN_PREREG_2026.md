# A Pre-Registered $a_0(z)$ Gate for the Rubin/LSST Supernova Stream: Committing the Test Before the Data

**Carl P. Zimmerman**
Briar Creek Tech — carl@briarcreektech.com
Frozen 2026-07-21

---

## Abstract

**This is a pre-registration, not a result.** It commits — in advance, timestamped, and SHA-256-hashed — the complete analysis procedure by which one distinctive prediction of the de Sitter–Unruh *modified-inertia* framework will be judged against the forthcoming Rubin Observatory / LSST supernova cosmology stream. The framework ties the galaxy acceleration scale $a_0$ to the cosmological horizon and, under an adiabatic-horizon ansatz, predicts that $a_0$ tracks the square root of the dark-energy density: $a_0(z)/a_0(0)=\sqrt{\rho_{\rm DE}(z)/\rho_{\rm DE,0}}$. The observable is the ratio $R\equiv a_0(z{=}3)/a_0(0)$, which is *independent of the normalization* $Z$ and of the absolute value of $a_0$ — both footings of the framework collapse onto the same $R$. The distinctive claim is that $R$ declines to $\approx 0.60$–$0.75$ **if and only if** dark energy evolves; if $w=-1$, then $R=1$ and the framework degenerates to constant-$a_0$ MOND. We freeze the estimator, the decision thresholds, and the data hierarchy *before* any calibrated Rubin supernova cosmology exists — LSST began operations on 2026-06-30, and the LSST-DESC calibrated Type-Ia sample is not expected before ~2027. The credibility move is precisely that the test is written before the data can shape it. At the freeze the best available input (DESI DR2 2025) gives $R=0.775\,[0.68,0.88]$, a $2.0\sigma$ decline — below the committed $3\sigma$ bar, hence **UNDECIDED**. A committed forecast projects that Rubin sharpens this to $\sim 3.3\sigma$ (supernovae alone) up to $\sim 4.7\sigma$ (supernovae combined with CMB/BAO) if dark energy evolves at the DESI-central rate. We state explicitly the *unsound path we refuse*: no do-it-yourself Hubble diagram from public broker light curves. Every number here comes from a committed, hash-locked script; the Zenodo DOI and timestamp are the public lock-in.

---

## 1. Introduction

### 1.1 The prediction under test

The de Sitter–Unruh modified-inertia framework is built on a horizon-derived acceleration scale $a_0 = cH_\Lambda/Z$, with the canonical footing giving $a_0 = 9.36\times10^{-11}\,{\rm m\,s^{-2}}$ and an alternate footing giving $1.13\times10^{-10}\,{\rm m\,s^{-2}}$. The low-acceleration kernel it uses, $\nu = \sqrt{1+1/y}$, is the identical functional form to Milgrom's 1999 interpolation (Milgrom 1983, 1999); the framework's distinctive content is the *coefficient* — the tie of the scale to $cH_\Lambda/Z$ rather than to a free constant — together with a modified-inertia (rather than modified-gravity) completion.

If the acceleration scale is sourced by the cosmological horizon, then when the horizon evolves, so should $a_0$. Under the adiabatic-horizon ansatz the scale tracks the dark-energy density:
$$
a_0(z)/a_0(0) = \sqrt{\rho_{\rm DE}(z)/\rho_{\rm DE,0}}, \qquad
\frac{\rho_{\rm DE}(z)}{\rho_{\rm DE,0}} = (1+z)^{3(1+w_0+w_a)}\, e^{-3 w_a z/(1+z)},
$$
where the second equality is the standard CPL (Chevallier–Polarski–Linder) parameterization of an evolving equation of state $w(a)=w_0+w_a(1-a)$. The single scalar observable is
$$
R \equiv a_0(z{=}3)/a_0(0).
$$
That $a_0$ should scale as $\sqrt{\rho_{\rm DE}}$ is not original to this framework — Limbach, Psaltis & Özel (2008) noted the numerical coincidence $a_0\sim c\sqrt{\rho_{\rm DE}}$ well before it. What the framework adds is the *promotion* of that coincidence to a horizon-sourced dynamical law, which is why it makes a falsifiable redshift prediction rather than a static numerical match.

**$R$ is $Z$-independent.** Because $R$ is a *ratio* of $a_0$ at two redshifts, the normalization $Z$ and the absolute value of $a_0$ cancel identically. Both *value* footings — canonical $9.36\times10^{-11}$ and alternate $1.13\times10^{-10}$ — collapse onto the same $R(w_0,w_a)$. This is what makes the gate a clean cosmology-side test: it depends on the dark-energy expansion history alone, not on any posited normalization internal to the framework. One clarification is owed here, because the framework's internal audit distinguishes two separate footing forks. The one that cancels is the *value* fork (which absolute $a_0$ today). A *second*, logically independent fork concerns the *evolution law itself* — the adiabatic-horizon $a_0\propto\sqrt{\rho_{\rm DE}}$ (which declines under evolving DE) versus a rival $a_0\propto cH(z)=cH_0E(z)$ (which *rises* with $z$). **This pre-registration commits to the $\sqrt{\rho_{\rm DE}}$ footing as the prediction under test.** The rival rising-$cH E(z)$ footing is not adopted here; if the data instead showed a rise, that registers as Verdict C below. So "both footings collapse to $R$" is a statement about the value normalization only — it is not a claim that the evolution law is unique.

The distinctive claim is:

> $R$ declines to $\approx 0.60$–$0.75$ **if and only if** dark energy evolves. If $w=-1$ (a true cosmological constant), then $R=1$ exactly and the framework reduces to ordinary constant-$a_0$ MOND.

**Two facts about the shape of $a_0(z)$ must be stated up front, because the gate summarizes a whole curve by a single point.** First, under an evolving CPL history $a_0(z)$ is *not monotonic*: at the DESI-central rate it rises to a small **bump** — $R$ peaks at $\approx1.036$ near $z\approx0.35$ and only crosses back below unity at $z\approx0.9$ — and *declines* only at higher redshift. This is the framework's own committed "bump-then-decline" behavior, which the estimator's $\sqrt{\rho_{\rm DE}}$ form reproduces identically. Second, the gate is evaluated at a **frozen reference redshift $z=3$**, deliberately beyond the range the feeding supernovae actually cover ($z\lesssim1.2$ for the LSST photometric sample). $R=a_0(3)/a_0(0)$ is therefore a *CPL extrapolation*: the headline decline is a lever-arm statement, not a directly measured $z=3$ quantity. Operationally, the significance the gate reports is the significance with which the supernova-constrained $(w_0,w_a)$ posterior excludes the non-evolving point $(w_0,w_a)=(-1,0)$, read along the CPL curve at $z=3$. Both facts are quantified and their consequences drawn out in §6.1.

### 1.2 Why pre-register now, before Rubin data exist

The Vera C. Rubin Observatory began its Legacy Survey of Space and Time on 2026-06-30. No calibrated Rubin supernova cosmology sample yet exists; the LSST-DESC systematics-controlled Type-Ia sample is not expected before roughly 2027. This is exactly the window in which a pre-registration has value. Committing the estimator and the decision thresholds *before* the data land removes any later freedom to tune the analysis to whatever the data happen to show — the single largest source of after-the-fact "detections" in cosmology-adjacent model testing.

This follows the same discipline as the author's Gaia-DR4 pre-registration precedent (frozen wide-binary $\gamma$ targets and cut tables, filed before DR4), now applied to Rubin. The move is deliberately modest: we are not announcing a finding, we are locking the referee-grade procedure so that when the data arrive there is nothing left to negotiate but the input $(w_0,w_a)$ posterior.

### 1.3 What this pre-registration does and does not settle

This gate settles the **cosmology-side** question — *does $a_0$ evolve at all* — which the framework *inherits* from the dark-energy history $w(z)$. It is important to state at the outset, and it is frozen into the protocol below, that a favorable verdict means the distinctive prediction **survives**, not that the framework is established. The independent, corroborating test is the **galaxy-side** measurement of $a_0(z)$ from resolved rotation-curve dynamics across redshift (the cross-scale program, DOI 10.5281/zenodo.21440407). The value of $a_0$, the normalization $Z$, and the adiabatic-horizon promotion of $a_0(z)\propto\sqrt{\rho_{\rm DE}}$ are all **posited**, not derived. This scope statement is non-negotiable and appears again, verbatim, in the frozen estimator's docstring.

---

## 2. The Frozen Estimator and Pre-Committed Thresholds

The decision procedure is committed in `a0z_gate_estimator.py` (SHA-256 in §8). **Input:** a calibrated $(w_0,w_a)$ posterior — mean, marginal uncertainties, and correlation coefficient. **Method:** the estimator draws $N=4\times10^5$ samples from the input's bivariate Gaussian (via Cholesky factorization of the covariance), maps each draw through the framework relation to $R=a_0(3)/a_0(0)$, and reports the median with its $[16,84]$ percentile interval, the significance of a *decline* ($R<1$) against flat, and the significance of a *rise* ($R>1$). It then applies the following pre-committed thresholds. **No threshold, band, or estimator may change after the freeze; only the input $(w_0,w_a)$ is updated.**

| Verdict | Pre-committed condition |
|---|---|
| **A) GATE OPEN** — distinctive prediction alive and supported | decline detected at $\ge 3\sigma$ **and** $R\in[0.55,0.85]$ (the $\sqrt{\rho_{\rm DE}}$ band across both footings) → $a_0$ evolves as required; warrants the independent galaxy-side confrontation |
| **B) GATE DISSOLVED** — safe core, *not* a falsification | consistent with flat ($R=1$ within $2\sigma$) → framework reduces to constant-$a_0$ MOND; the distinctive prediction is inapplicable. If in addition $R\le0.85$ is excluded at $\ge3\sigma$, the distinctive decline is positively ruled out (still dissolution, not a kill of the MOND-scale core) |
| **C) FRAMEWORK STRAINED** — cosmology-side tension | $R>1$ (a *rise*) at $\ge3\sigma$ → the scale rises with $z$, which $a_0\propto\sqrt{\rho_{\rm DE}}$ does not permit under evolving DE |
| **UNDECIDED** | none of the above met (insufficient significance / out of band) |

The band $[0.55,0.85]$ for Verdict A is the range of $R=a_0(3)/a_0(0)$ produced by the $\sqrt{\rho_{\rm DE}}$ relation across the range of dark-energy histories currently plausible; it is fixed here and does not move. To be precise about what sets it — and to forestall any charge of gerrymandering — the band width comes from the spread of allowed $(w_0,w_a)$, **not** from the two value footings (those give an *identical* $R$ at fixed $(w_0,w_a)$, so they cannot widen a band). Holding $w_a=-0.62$, the edges correspond to $w_0\approx-0.79$ ($R=0.85$, mild evolution) and $w_0\approx-1.00$ ($R=0.55$, strong evolution). Two honesty notes follow. (i) The band $[0.55,0.85]$ is deliberately *wider* than the nominal distinctive claim $R\approx0.60$–$0.75$ quoted in §1.1; the DESI-central value $R=0.775$ in fact sits just *above* the nominal $0.75$ but inside the operational band. (ii) The upper edge $R=0.85$ is close to flat, so a "supported" verdict at that edge is a weak decline; this is the intended cost of choosing a decision band broad enough not to be tuned to any single posterior. The asymmetry between Verdicts A, B, and C is intentional: a decline in-band supports the distinctive claim, flatness dissolves it into the safe MOND core, and a *rise* would strain the framework because the committed $\sqrt{\rho_{\rm DE}}$ footing produces no rising $a_0$ under evolving dark energy. Note the deliberate gap: a decline so steep that $R<0.55$ at $\ge3\sigma$ (steeper than $\sqrt{\rho_{\rm DE}}$ allows) returns **UNDECIDED**, not a verdict — the frozen procedure has no "over-decline strain" branch mirroring Verdict C (see §6.1).

---

## 3. Data Hierarchy and the Refused DIY-Hubble-Diagram Path

The gate is fed by a strict, frozen hierarchy of inputs:

1. **Primary:** the LSST-DESC *calibrated* Type-Ia supernova cosmology sample — systematics-controlled zero-points, photometric-redshift treatment, and a modeled selection function. Expected ~2027 and later. This is the only input that can produce a *supported* verdict.
2. **Interim:** published Rubin $w_0w_a$ constraints as they appear, including externally combined CMB/BAO fits. These update the input posterior but carry the caveats of any early, pre-final calibration.
3. **Readiness tracker only:** a running count of broker-classified Type-Ia candidates from the *public* alert stream (`broker_sn_counter.py`). **This count never feeds the verdict.** It tracks *when* the gate will have enough statistical weight to spring — timing, not cosmology.

### The path we refuse

We do **not** build a do-it-yourself Hubble diagram from public broker light curves. The alerts are public and real-time, but they are discoveries, not calibrated distances. Without the DESC calibration layer — zero-point stability, photometric-redshift systematics, and a modeled selection function — any $w(z)$ extracted from raw broker photometry is systematics-dominated, and a "Rubin supports $a_0(z)$" claim built on it would be a manufactured result. Refusing that path is stated here as a virtue of the protocol, not an omission: the primary input is the calibrated sample, full stop. The readiness tracker exists precisely so that the temptation to jump early has a disciplined, cosmology-free outlet.

---

## 4. Forecast: What Significance Rubin Reaches

The forecast basis is committed in `forecast_rubin_a0z.py` (SHA-256 in §8); it is explicitly a projection, not a measurement. It propagates representative *projected* Rubin $w_0$–$w_a$ covariances through the framework relation and asks at what significance Rubin distinguishes the framework's decline from flat ($w=-1$). Photometric supernova cosmology forecasts for LSST reach a Dark Energy Task Force figure of merit of order 150 (LSST alone) up to ~500 (LSST combined with CMB/BAO), against ~54 for the Dark Energy Survey and the ~$2.0\sigma$ decline currently delivered by DESI DR2. Taking the DESI-central evolving-DE history as the assumed truth ($w_0=-0.838$, $w_a=-0.62$), the committed forecast gives:

| Input scenario | $\sigma(w_0)$ | $\sigma(w_a)$ | $R=a_0(3)/a_0(0)$ | Decline significance |
|---|---|---|---|---|
| DESI DR2 now (baseline) | 0.055 | 0.22 | 0.775 [0.683, 0.878] | $2.0\sigma$ |
| Rubin SN alone (FoM ~150) | 0.040 | 0.15 | 0.775 [0.717, 0.837] | $3.3\sigma$ |
| Rubin SN + CMB/BAO (FoM ~500) | 0.020 | 0.08 | 0.775 [0.742, 0.809] | $4.6$–$4.7\sigma$ |

The forecast also runs the **mirror test** — if the universe is in fact flat ($w=-1$, $a_0$ truly constant), how tightly does Rubin pin $R$ to unity and thereby exclude the framework's $\approx0.74$? Rubin-alone (FoM ~150) gives $R=1.00\pm0.078$, excluding $0.74$ at $3.3\sigma$; Rubin + CMB/BAO (FoM ~500) gives $R=1.00\pm0.043$, excluding it at $6.0\sigma$.

The honest forecast summary is deliberately unheroic: if dark energy evolves at the DESI-central rate, Rubin sharpens the $a_0$-decline detection from DESI-now $\sim2.0\sigma$ to $\sim3.3\sigma$ (supernovae alone) or $\sim4.6$–$4.7\sigma$ (with CMB/BAO) — crossing the committed $3\sigma$ bar, approaching but not alone reaching $5\sigma$ at the modest $0.775$-vs-$1.0$ gap. If dark energy is flat, Rubin pins $R=1$ and excludes the framework's $0.74$ at $\sim3.3$–$6.0\sigma$. Either way the gate is likely settled at the $3$–$6\sigma$ level by roughly 2028–2030 — a real upgrade on DESI-now, not a one-instrument slam dunk.

---

## 5. State at the Freeze (2026-07-21)

Running the frozen estimator on the best current input reproduces the baseline verdict exactly:

- **Cosmology input (DESI DR2 2025, arXiv:2503.14738):** $w_0=-0.838\pm0.055$, $w_a=-0.62\pm0.22$, correlation $-0.86$ → $R=0.775\,[0.683,0.878]$, a decline at $2.0\sigma$. This is **below the committed $3\sigma$ threshold**, so the frozen verdict at the freeze is **UNDECIDED** — a $2.0\sigma$ hint, explicitly not a detection, explicitly not gate-open. Applying the same procedure to the two forecast inputs returns *GATE OPEN* at $3.3\sigma$ and $4.7\sigma$ respectively, showing that the projected Rubin precision is what moves the verdict off UNDECIDED — but those are projections, not data, and cannot produce a real verdict.

- **Broker readiness tracker (live, 2026-07-21):** the ALeRCE light-curve classifier reports **36,836** Type-Ia-classified objects (ZTF legacy plus early LSST). This is past the ~4,400 spectroscopic-quality threshold (**REACHED**) and is **9.21%** of the ~400,000 LSST photometric target. It is a broker-classifier count — unvetted, no redshifts, ZTF-and-early-LSST mixed — and by the frozen hard rule it **never feeds the verdict**. It reports timing only.

The fallback brokers, should the ALeRCE endpoint be unavailable, are Fink, Lasair, ANTARES, and Pitt-Google; the tracker script is ready-to-run against any of them.

---

## 6. Honest Scope, and the Kill / Dissolution Conditions

The scope is frozen in and stated plainly:

- This settles the **cosmology-side gate** — *does $a_0$ evolve at all* — which the framework inherits from $w(z)$. **GATE OPEN means the distinctive prediction survives, not that the framework is established.** The corroborating test remains the *independent galaxy-side* $a_0(z)$ measured from resolved dynamics across redshift (cross-scale, DOI 10.5281/zenodo.21440407). The cosmology-side gate and the galaxy-side test are logically distinct; passing the former is necessary, not sufficient.
- $a_0$'s value, the normalization $Z$, and the adiabatic-horizon promotion of $a_0(z)\propto\sqrt{\rho_{\rm DE}}$ are **posited**, not derived. The Milgrom-form kernel $\nu=\sqrt{1+1/y}$ is credited to Milgrom (1999); the framework's distinctive content is the horizon coefficient and the modified-inertia completion (MI Field Theory, DOI 10.5281/zenodo.21403470).

The pre-committed kill / dissolution conditions, signed 2026-07-21:

- **Distinctive prediction FALSIFIED** if the calibrated Rubin posterior yields **Verdict C** — $a_0$ *rises* with $z$ at $\ge3\sigma$ — which no viable footing of $a_0\propto\sqrt{\rho_{\rm DE}}$ permits under evolving dark energy.
- **Distinctive prediction DISSOLVED** (Verdict B) if $w\to-1$: the framework becomes ordinary constant-$a_0$ MOND. This is the stated safe core — dissolution, not a kill of the MOND-scale reframing. The reframing survives as constant-$a_0$ MOND even if the redshift signature vanishes.
- **Distinctive prediction SUPPORTED** (Verdict A) only if *both* the $\ge3\sigma$ decline *and* the $[0.55,0.85]$ band are met — and even then, "supported" means survives to face the galaxy-side test, nothing more.

Because $R$ is $Z$-independent, none of these outcomes depends on the internal normalization; they depend on the measured dark-energy history alone. This is the cleanest form the test can take, and also the sharpest constraint on what a favorable outcome is allowed to mean.

### 6.1 Known limitations baked into the frozen procedure

Because the estimator and thresholds are hashed and cannot be revised after the freeze, the following limitations are documented rather than fixed. They are stated here so that no future reading can present the gate as tighter than it is.

1. **The signal is a $z=3$ extrapolation beyond the supernova range, and the significance is $z$-dependent.** The LSST photometric SN sample constrains $w(z)$ mainly at $z\lesssim1.2$; the gate is read at $z=3$. Propagating the *same* DESI-DR2 posterior to different reference redshifts gives a decline significance of $0.34\sigma$ at $z=1$ ($R=0.99$, effectively flat), $1.7\sigma$ at $z=2$, $2.0\sigma$ at $z=3$, and $2.4\sigma$ at $z=10$; for the tight SN+CMB/BAO forecast covariance it is $1.1\sigma$ at $z=1$ but $4.7\sigma$ at $z\ge2$. The headline numbers therefore depend on the frozen choice $z=3$, which is a lever arm, not a redshift at which calibrated SNe exist. What the gate genuinely tests is whether the SN-constrained posterior excludes $(w_0,w_a)=(-1,0)$; the $z=3$ evaluation converts that into an $a_0$-ratio but does not add independent $z=3$ information. A reader must not treat $R(z{=}3)=0.775$ as a measured $z=3$ acceleration scale.

2. **The framework's own $a_0(z)$ bumps *up* at low redshift, which is where the galaxy-side corroborating test lives.** At the DESI-central history $a_0(z)$ rises to $R\approx1.036$ near $z\approx0.35$ and only falls below $1$ beyond $z\approx0.9$. The independent galaxy-side $a_0(z)$ program (resolved rotation-curve dynamics, DOI 10.5281/zenodo.21440407) is accessible only at low redshift — squarely inside this *bump*. So a GATE-OPEN verdict on the $z=3$ *decline* does not translate into a low-$z$ decline for the galaxy-side to corroborate; at $z\lesssim0.5$ the framework predicts a slight **rise** (a few percent), and at $z\sim1$ essentially no change. Anyone carrying "the framework predicts $a_0$ declines" to galaxy-side observers at accessible redshifts would have the sign wrong. The two halves of the program probe opposite branches of the same non-monotonic curve, and the amplitude available to the galaxy side ($\sim$few percent) is far smaller than the $z=3$ headline.

3. **Verdict C ("rise ⇒ strained") is well-posed only at the frozen $z=3$.** Because $a_0(z)$ genuinely rises for $z\lesssim0.9$, a measured rise is a contradiction of the $\sqrt{\rho_{\rm DE}}$ footing *only* when read at high $z$; the frozen $z=3$ evaluation is what makes the rule self-consistent. This is a reason the reference redshift is fixed, but it also means Verdict C should never be applied to a low-$z$ input.

4. **Doc-vs-code items.** (a) The Verdict-B sub-clause described in §2 and §6 — "if $R\le0.85$ is additionally excluded at $\ge3\sigma$, the decline is positively ruled out" — is *narrative only*; the frozen `a0z_gate_estimator.py` computes Verdict B purely as consistency with $R=1$ within $2\sigma$ and does not evaluate that exclusion. (b) The over-decline gap of §2 ($R<0.55$ significant $\to$ UNDECIDED) is a real asymmetry with Verdict C. (c) The frozen estimator prints "GATE OPEN" for the two *forecast* covariances; those are fabricated inputs shown for illustration and, by the data hierarchy of §3, can never constitute a verdict — only a calibrated posterior can.

5. **Significance is a Bayesian posterior tail, and the two frozen scripts differ at the $0.1\sigma$ level.** The reported "$N\sigma$" is the posterior credibility that $R<1$ (the fraction of samples with $R\ge1$ mapped to a Gaussian sigma), not a frequentist likelihood-ratio detection. The estimator ($N=4\times10^5$) and the forecast script ($N=3\times10^5$) return $4.7\sigma$ and $4.6\sigma$ respectively for the identical SN+CMB/BAO scenario — a Monte-Carlo difference, reported here as the range $4.6$–$4.7\sigma$.

6. **DESI input provenance.** The baseline $(w_0,w_a)=(-0.838,-0.62)$, $\sigma=(0.055,0.22)$, $\rho=-0.86$ is the DESI DR2 + CMB + Pantheon+ combination (the mildest of the DESI DR2 SN combinations; DESY5 and Union3 prefer stronger evolution and a lower $R$). The verdict at the freeze is UNDECIDED under this input and remains UNDECIDED under the stronger combinations, so the choice does not change the frozen state — but the input row is named explicitly so the update path is unambiguous.

---

## 7. Conclusion

We have frozen, before the data exist, a referee-grade decision procedure for the one distinctive prediction the de Sitter–Unruh modified-inertia framework makes on the cosmological side: that the galaxy acceleration scale tracks $\sqrt{\rho_{\rm DE}}$ and therefore *declines* with redshift if and only if dark energy evolves. The observable $R=a_0(3)/a_0(0)$ is normalization-independent; the estimator, the thresholds ($3\sigma$ decline and the $[0.55,0.85]$ band for GATE OPEN), the data hierarchy, and the refusal of the DIY-Hubble-diagram path are all committed and hashed. At the freeze the test stands **UNDECIDED**: DESI DR2 gives a $2.0\sigma$ hint, $R=0.775\,[0.68,0.88]$, below the committed bar. The committed forecast projects Rubin to reach $\sim3.3$–$4.7\sigma$ if dark energy evolves, or to exclude the decline at $\sim3.3$–$6.0\sigma$ if it does not — a decision at the $3$–$6\sigma$ level expected by roughly 2028–2030 from the LSST-DESC calibrated sample. A favorable outcome would mean the distinctive prediction survives to face the independent galaxy-side $a_0(z)$ test; it would not, on its own, establish the framework. The value of this document is entirely in its timing: it is filed before the calibrated data can shape it, and only the $(w_0,w_a)$ input will be updated when they arrive.

---

## 8. Freeze Integrity

The SHA-256 hashes of the frozen artifacts, recorded in `FREEZE_HASHES.txt` and verified 2026-07-21:

```
852ca954431b9239415038dde9f2b2ad9f89fe6325ff7a8ba3e3ebe357366740  a0z_gate_estimator.py
ba24927ddb3263c390646019b1dba1968c4aa3de5ed572bc5de57685afd2b77f  broker_sn_counter.py
bd714c93edd3eadc6c84413dee331e86be7ebaca8f0a5f88c84ec1542f46df0f  PREREGISTRATION.md
530e66beef425bb500d085051c3219669e6d6e31364eec9263ea036bca7a5697  forecast_rubin_a0z.py
```

The Zenodo DOI and its deposit timestamp are the public lock-in of this pre-registration. No threshold, band, or estimator changes after this hash; only the calibrated $(w_0,w_a)$ input is updated when the LSST-DESC sample lands.

---

## References

- DESI Collaboration (2025). *DESI DR2 Results II: Measurements of Baryon Acoustic Oscillations and Cosmological Constraints.* arXiv:2503.14738; Phys. Rev. D 112, 083515. (The $w_0=-0.838,\,w_a=-0.62$ input used here is the DESI+CMB+Pantheon+ combination.)
- Ivezić, Ž., et al. (LSST/Rubin) (2019). *LSST: From Science Drivers to Reference Design and Anticipated Data Products.* ApJ 873, 111.
- LSST Dark Energy Science Collaboration (LSST-DESC). Supernova cosmology forecasts (photometric FoM ~150; +CMB/BAO ~500).
- Möller, A., et al. *Fink*; Smith, K. W., et al. *Lasair*; Matheson, T., et al. *ANTARES*; Förster, F., et al. *ALeRCE* — LSST/ZTF alert brokers.
- Milgrom, M. (1983). *A modification of the Newtonian dynamics as a possible alternative to the hidden mass hypothesis.* ApJ 270, 365.
- Milgrom, M. (1999). *The modified dynamics as a vacuum effect.* Phys. Lett. A 253, 273 — the $\nu=\sqrt{1+1/y}$ kernel.
- Limbach, C., Psaltis, D., Özel, F. (2008). *The Redshift Evolution of the Tully–Fisher Relation as a Test of Modified Gravity.* arXiv:0809.2790 — considered $a_0$ coupled to $H_0$ or to $\rho_{\rm DE}$ (the $a_0\sim c\sqrt{\rho_{\rm DE}}$ coincidence predates this framework) and tested both couplings against Tully–Fisher data to $z\simeq1.2$. Their credit is for the coincidence; the horizon-sourced dynamical promotion is what this framework adds.
- Zimmerman, C. P. *Cross-scale $a_0(z)$ program* (galaxy-side corroborating test). DOI 10.5281/zenodo.21440407.
- Zimmerman, C. P. *Modified-Inertia Field Theory.* DOI 10.5281/zenodo.21403470.
- Zimmerman, C. P. *Gaia-DR4 pre-registration* (frozen-cuts precedent).

---

*Author: Carl P. Zimmerman, Briar Creek Tech (carl@briarcreektech.com). This is a pre-registration filed before the calibrated Rubin supernova cosmology sample exists. It is a committed analysis protocol, not a result. Every quantitative figure herein is produced by a committed, hash-locked script that exits 0.*
