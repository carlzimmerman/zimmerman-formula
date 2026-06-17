---
title: "Dark Energy Sets the Galaxy Acceleration Scale: A Parameter-Free $a_0(z)$ Test $\\Lambda$CDM Cannot Take"
author: "Carl P. Zimmerman · Briar Creek Tech"
date: "June 2026"
---

## Abstract

The de Sitter–MOND framework ties the galactic acceleration scale to the dark-energy density,
$a_0 = c^2\sqrt{\Lambda/32\pi} = \tfrac{c}{2}\sqrt{G\rho_{\rm DE}}$. Promoted across cosmic time this becomes a
**parameter-free shape prediction**, $a_0(z)/a_0(0) = \sqrt{\rho_{\rm DE}(z)/\rho_{\rm DE}(0)}$ — both the coefficient
and the MOND interpolation function cancel in the ratio, so the evolution of $a_0$ is fixed entirely by the dark-energy
equation of state $w(z)$, with no remaining freedom. (The $\sqrt{\rho_{\rm DE}}$ scaling itself is not novel — it appears
in Limbach, Psaltis & Özel 2008 — but the framework promotes it to a *forced* relation and the data now make it sharp.)
DESI DR2's measured time-evolving dark energy ($w_0\simeq-0.75,\ w_a\simeq-0.86$) drives $a_0(z)$ along a distinctive
**non-monotonic** track: a $+6\%$ rise to a peak at $z\approx0.41$ — precisely the phantom-divide crossing where
$w(z)=-1$ — then a decline to $a_0(z{=}3)\approx0.74\,a_0(0)$. The cleanest measurable signature is the **sign** of the
high-$z$ deep-MOND baryonic Tully–Fisher offset: the framework predicts rotation velocities $0.033$ dex ($-7.3\%$)
**below** the local relation at $z=3$, where standard fixed-$a_0$ MOND sits *on* it. We argue this is a near-term
falsification test that $\Lambda$CDM **structurally cannot take** — cold dark matter has no acceleration scale to evolve —
while stating plainly that it is **non-diagnostic today**: the framework is hostage to a DESI result it cannot influence,
dissolves to ordinary MOND if $w\to-1$, and the present $a_0(z)$ data (including MUSE-DARK) are systematics-limited in both
directions. The verdict arrives on two axes — DESI DR3 ($w(z)$, \ensuremath{\sim}2026–27) and high-$z$ resolved kinematics
(ALMA BTFR-sign \ensuremath{\sim}2028–30; ELT/HARMONI clean tracking, early-mid 2030s). We give the kill conditions.

---

## 1. The bet

A spiral galaxy's outer stars orbit faster than the visible matter can hold. The standard answer adds an unseen halo; the
modified-dynamics answer says the mass discrepancy switches on below a universal acceleration $a_0\approx1.2\times10^{-10}\
\mathrm{m\,s^{-2}}$. That number is not arbitrary: to order unity it equals the acceleration set by the dark energy
accelerating the whole universe — the longstanding clue that the galactic scale and the cosmological constant are one
physics.

This paper makes the clue do work. If $a_0$ is genuinely *made of* dark energy, then as the dark-energy density changes
through cosmic history, $a_0$ must change with it — on a track fixed by the cosmology, with nothing to tune. That is a bet
with a theory's neck on the block. We state it precisely, show what DESI's latest data does to it, name exactly what
would settle it and by when — and we are equally explicit about where it is not yet decidable.

## 2. The mechanism (forced in form, hostage in evolution)

The framework's acceleration scale is
$$a_0 = c^2\sqrt{\frac{\Lambda}{32\pi}} = \frac{c}{2}\sqrt{G\rho_{\rm DE}}, \qquad \rho_{\rm DE}=\frac{\Lambda c^2}{8\pi G},$$
with the kernel $\sqrt{8\pi/3}$ fixed by gravity — Einstein's $8\pi$ times the Friedmann/de Sitter $3$ — not fit to data.
Promoting $\rho_{\rm DE}$ to its evolution gives the central object:
$$\boxed{\ \frac{a_0(z)}{a_0(0)}=\sqrt{\frac{\rho_{\rm DE}(z)}{\rho_{\rm DE}(0)}}\ }$$
This is **parameter-free**: the coefficient $a_0(0)$ *and* the MOND interpolation function both cancel in the ratio, so
only $w(z)$ enters. For a CPL law $w(a)=w_0+w_a(1-a)$,
$$\frac{\rho_{\rm DE}(z)}{\rho_{\rm DE}(0)}=(1+z)^{3(1+w_0+w_a)}\exp\!\left(\frac{-3w_a z}{1+z}\right).$$
Two honesty markers up front. The *value* $a_0(0)$ is **not** derived — it carries the framework's one free normalization
($\kappa=\tfrac12$); only the **shape** is the prediction. And the *evolution* is **hostage** to $w(z)$: the framework
does not predict $w(z)$, it inherits it.

## 3. Three fates, and the sharpest discriminator

Three readings of the dark sector give three different $a_0(z)$ (Figure 1):

| $z$ | constant ($\Lambda$CDM / pure $\Lambda$) | **framework** (DESI $w_0w_a$) | rising $\sqrt{\rho_{\rm tot}}$ |
|---:|:---:|:---:|:---:|
| 0.0 | 1.000 | 1.000 | 1.21 |
| 0.41 | 1.000 | **1.062** (peak) | 1.52 |
| 1.0 | 1.000 | 1.009 | 2.16 |
| 2.0 | 1.000 | 0.862 | 3.67 |
| 3.0 | 1.000 | **0.737** | 5.52 |

*(Framework: DESI+CMB+DESY5 central $w_0=-0.752,\ w_a=-0.86$; the DESI SNe-combination band spans
$a_0(z{=}3)/a_0(0)\in[0.71,0.78]$. Curves verified against the first-principles density integral to $10^{-32}$.)*

The framework curve is **non-monotonic**: it rises $+6\%$ to a peak at $z\approx0.41$ — the exact redshift where DESI's
$w(z)$ crosses the phantom divide $w=-1$ — then declines to $\approx0.74$ by $z=3$. The rising $\sqrt{\rho_{\rm tot}}$
reading (which sets $a_0\propto cH/E(z)$) climbs to $\sim5.5$; it is shown for contrast but is **already disfavored** by
existing dynamics (Milgrom 2017; RC100; cluster offsets), so the live contest is *declining* (framework) versus *flat*
($\Lambda$CDM/standard MOND).

**The cleanest measurable test is a sign, not an amplitude.** The deep-MOND baryonic Tully–Fisher relation is
$V^4=GMa_0$, so $V\propto a_0^{1/4}$ and $\mathrm{d}\log V=\tfrac18\,\mathrm{d}\log\rho_{\rm DE}$. At $z=3$ the framework
therefore predicts high-$z$ discs lying $0.033$ dex ($-7.3\%$ in $V$) **below** the local BTFR; standard fixed-$a_0$ MOND
sits *on* it ($0$); the rising rival sits $+0.166$ dex *above*. That sign is far more robust to amplitude systematics than
the $a_0$ value itself.

![**Figure 1.** Three falsifiable fates of $a_0(z)$. Constant (gray) is the $\Lambda$CDM/pure-$\Lambda$ expectation. The
framework (blue, with the DESI DR2 $w_0w_a$ band) traces $\sqrt{\rho_{\rm DE}(z)}$: a $+6\%$ rise to the phantom-divide
crossing at $z\approx0.41$, then a decline to $\sim0.74$ at $z=3$. The rising $\sqrt{\rho_{\rm tot}}$ reading (red) climbs
to $\sim5.5$ but is already disfavored. The factor-\ensuremath{\sim}7.5 split by $z=3$ is the
discriminator.](a0z_desi_figure.png)

## 4. DESI DR2 supplies the input the prediction needs

DESI's Data Release 2 (2025) reports time-evolving dark energy at \ensuremath{\sim}2.8–4$\sigma$ ($w_0>-1$, $w_a<0$) across SNe
compilations. This is the single most consequential *input* the framework could receive: fed through the fixed relation,
DESI's own $\rho_{\rm DE}(z)$ produces the structured curve of Figure 1 with **zero** extra parameters. We are precise
about the logic: DESI measures the *input* $\rho_{\rm DE}(z)$, never the *output* $a_0(z)$ — so this is a **precondition
that arms the prediction**, not a confirmation of it. What is notable is only that the sign of the effect is right: an
*evolving* dark sector is what turns $a_0(z)$ from a flat, indistinct line into a falsifiable curve, and the framework's
$\sqrt{\rho_{\rm DE}}$ relation predates the DR2 measurement.

## 5. Why $\Lambda$CDM cannot take this test

Here is the asymmetry. **In $\Lambda$CDM there is no $a_0$ to evolve.** Cold dark matter has no universal acceleration
scale; the tight radial-acceleration relation is, in the halo picture, an emergent regularity to be explained — not a
fundamental constant with a value and a redshift dependence. Any $a_0(z)$ that $\Lambda$CDM "produces" is a downstream fit
to whatever halo response the simulations are tuned for; it can be made to rise, fall, or stay flat. The framework has no
such freedom: $a_0(z)$ is welded to $\rho_{\rm DE}(z)$, a quantity an entirely independent set of experiments (BAO, SNe,
CMB) measures. One theory stakes a parameter-free curve — and a definite BTFR-offset *sign* — on a number it does not
control; the other has no curve to stake. That is the whole fight.

## 6. The data today — honestly non-diagnostic, both ways

We confront the present $a_0(z)$ data and report plainly that it does not yet decide the question in either direction.

MUSE-DARK (Ciocan et al. 2026) reports $a_0$ *rising* with redshift over an intermediate-$z$ sample — at face value a
large effect (raw significance \ensuremath{\sim}10–30$\sigma$) and the **wrong sign** for the declining branch. It is not a
falsification, for a specific reason: that raw signal de-systematizes to *consistent with zero* once the
$\Lambda$CDM-tied baryon-fraction/mass-modelling degeneracy is included — and that is the **same** degeneracy that makes
*every* current high-$z$ $a_0$ inference non-diagnostic. Applied symmetrically, the systematics that erase MUSE's "rising"
signal also forbid reading it as confirmation of the rising rival. The honest status: the present data neither falsify
the framework nor confirm any competitor; $a_0(z)$ is non-diagnostic at the current systematic floor. We also retract any
earlier suggestion that such measurements *confirm* a rising $a_0$ — the rising branch is a $\rho_{\rm tot}$
footing artifact, overshoots the data, and is $\Lambda$CDM-degenerate. The decisive regime is $z\gtrsim1$, where the
framework declines, $\Lambda$CDM stays flat, and the BTFR-offset sign becomes the clean observable.

## 7. Kill conditions and timeline

The bet is falsifiable on two independent axes, but not instantly.

- **The $w(z)$ axis — DESI DR3 / DESI-final (~2026–27), the gate.** DR3 tightens $w_0,w_a$ by \ensuremath{\sim}1.5–1.8$\times$. If
  evolving DE strengthens (toward \ensuremath{\sim}5–7$\sigma$), the declining $a_0(z)$ becomes a sharp, mandatory prediction and the
  distinctive content is fully live. **If DR3 reverts to $w=-1$, the distinctive content dissolves** — $a_0$ becomes
  constant and the framework degenerates to ordinary fixed-$a_0$ MOND. (This is *dissolution to the safe core, not
  falsification*: constant-$\Lambda$ does not kill the framework, it just removes its one new prediction.) DR3 sets the
  input $\rho_{\rm DE}$; it cannot by itself confirm $a_0(z)$.
- **The $a_0(z)$ axis — high-$z$ kinematics (\ensuremath{\sim}2028 onward).** ALMA CO/[CII] cold-gas outer discs can begin probing
  the $z\gtrsim2$ BTFR-offset **sign** \ensuremath{\sim}2028–30, *if* baryonic-mass systematics drop below $\sim0.04$ dex.
  ELT/HARMONI (telescope first light 2029; science 2030+) is the decisive resolved deep-MOND machine; a clean
  multi-redshift $5\sigma$ test that $a_0(z)$ *tracks* the independently-measured $\rho_{\rm DE}(z)$ lands **early-to-mid
  2030s**. A caveat that cuts against over-eager reading: with DR2-level priors, any *single*-redshift amplitude test is
  capped sub-3$\sigma$ — the power is in the *sign* and the *correlation across redshift*, not one data point.

**Kill conditions.** (i) Under confirmed evolving DE, a clean high-$z$ deep-MOND $a_0(z)$ measured *flat or rising*
(positive BTFR offset) at $z\gtrsim2$ contradicts the mandatory declining-by-sign prediction and kills the distinctive
claim. (ii) $a_0(z)$ flat to high precision while DESI confirms evolving DE breaks the $a_0\!\propto\!\sqrt{\rho_{\rm DE}}$
lock. **Confirmation:** the BTFR offset going negative at $z\gtrsim2$ and $a_0(z)$ tracking $\sqrt{\rho_{\rm DE}(z)}$ —
ideally including the $+6\%$ bump at $z\approx0.41$ — a redshift correlation $\Lambda$CDM and free-function MOND have no
reason to produce.

## 8. Honest caveats

A falsifiable prediction of a gravity/dark-sector effective theory — and **not a theory of everything yet, as
frustrating as it may be.** Stated plainly: (i) the *form* $a_0\propto\sqrt{\rho_{\rm DE}}$ and the kernel $\sqrt{8\pi/3}$
are forced, but the *value* $a_0(0)$ is not derived (one free $\kappa=\tfrac12$); only the shape is predicted, and the
$\sqrt{\rho_{\rm DE}}$ scaling itself predates the framework (Limbach, Psaltis & Özel 2008). (ii) The $w_0w_a$ inputs
carry DESI's uncertainties and vary across SNe compilations (the Figure 1 band); a shift in DESI's central values shifts
the curve, and the framework cannot adjudicate it. (iii) The prediction is **non-diagnostic now** and **hostage** to DESI:
its one distinctive claim can dissolve before it can be cashed. (iv) A relativistic completion delivering Cassini-safe
lensing remains phenomenological, as in all relativistic-MOND theories; this test concerns dynamics, where the prediction
is sharp. None of these blunt the central point: the shape and the BTFR-offset sign are locked, the data axis is
independent, and the verdict is near.

## Closing

For fifty years the galactic acceleration scale and the cosmological constant have looked like the same number wearing two
hats. The framework takes that seriously enough to be killed by it: *the acceleration scale is made of dark energy, so when
dark energy evolves, so must the scale — here is the curve, and the sign of the high-redshift Tully–Fisher offset,
measured against a quantity I do not control, falsifiable within the decade.* Dark matter cannot answer in kind, because
it has no scale to put on the table. That asymmetry — a parameter-free curve on one side, no curve at all on the other —
is the test. It is not yet decided, it could dissolve if dark energy turns out constant, and the present data are
systematics-limited. But the telescopes that settle it are already being built.

---

*Companion to the de Sitter–MOND framework (DOI [10.5281/zenodo.20721540](https://doi.org/10.5281/zenodo.20721540)).
Figure 1 and all curves are reproducible from `a0z_desi_figure.py`. The framework's open questions — the un-derived value
of $a_0$ (one free $\kappa=\tfrac12$), the phenomenological covariant lensing sector, and the absence of a
Standard-Model derivation — are real and stated in the technical record. This is a falsifiable theory of gravity and the
dark sector; it is not a proven replacement for dark matter, and not a theory of everything.*
