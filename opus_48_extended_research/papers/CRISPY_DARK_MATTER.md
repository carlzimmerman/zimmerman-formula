# Crispy Dark Matter: A Pre-Registered Accommodation Ledger for an Evolving Acceleration Scale

**Carl P. Zimmerman**
Briar Creek Tech, Charlotte, NC, USA · carl@briarcreektech.com

**Version 2026-07-30 (v1)** · License CC-BY-4.0

---

## Abstract

If the acceleration scale $a_0$ of the mass–discrepancy–acceleration relation is set by the
dark-energy density, $a_0=\kappa c\sqrt{G\rho_\Lambda}$ with $\kappa=1/2$, then a measured evolution
of $\rho_\Lambda$ forces a corresponding evolution of $a_0$ with **no additional parameters**.
$\Lambda$CDM contains no $a_0$; its emergent acceleration scale inherits the halo characteristic
density and therefore scales as $H(z)$. These are different functions of redshift, and the difference
is an **absorption function** $A(z)$ that any $\Lambda$CDM account of a measured $a_0(z)$ must supply
through its free sectors — halo concentration evolution and baryonic feedback. We name the resulting
accommodated model **crispy dark matter** and register its required content in advance.

We compute $A(z)$ for four verified DESI DR2 $w_0w_a$CDM fits and give the Occam ledger in bans. We
then report three results that **reduce** the strength of the claim rather than support it. First, most
of the naive absorption requirement ($0.25$ dex at $z=1$) is the pre-existing
constant-$a_0$-versus-rising-$E(z)$ tension that $\Lambda$CDM already accommodates; the genuinely
DESI-dependent part is only $\sim0.01$ dex at $z=1$, changes sign near $z\simeq1$, and reaches
$0.11$–$0.20$ dex only by $z=3$. Second, on the alternative $a_0\propto cH(z)/Z$ footing the
absorption function is **identically zero** for every fit, so the test does not exist there and the
framework must commit to the $\rho_{\rm DE}$ footing to make any claim at all. Third, the input
$(w_0,w_a)$ were themselves inferred assuming standard inertia, so "parameter-free" is conditional on
an unbuilt result. We state the falsification conditions symmetrically and note that a competing
constant-$\Lambda$ reading of the same data is mutually exclusive with this one and is decided by a
$\sim0.05$ dex high-redshift measurement.

**This document is a forecast with a parameter ledger, not a discovery, and not an attribution.**

---

## 1. What this document is, and what it is not

**It is** a prediction, written before the relevant data exist, of *what a $\Lambda$CDM account of an
evolving acceleration scale would have to contain*, and *what that content costs in parameters*.

**It is not** a claim that anyone has proposed such a model. No paper in the literature proposes
crispy dark matter. The name labels a **forecast object**: the model we expect to be constructed if
$a_0(z)$ is measured to evolve. Any resemblance to future work is the entire point of registering it.

**It is not an accusation.** Adjusting halo concentration evolution or feedback strength when new data
arrive is ordinary, correct scientific practice. Those sectors are genuinely uncertain and were never
claimed to be predictions. The single thing this document asks is that such an adjustment be counted
as **parameters spent**, not reported as a prediction fulfilled. That request is symmetric: §7 and §9
apply the same accounting to the framework, which has less freedom and therefore more to lose.

**It is not a claim of novelty for the underlying mechanism.** See §8.

---

## 2. The framework's claim, scoped narrowly

The only claim used here is the reframing of the acceleration scale. The author has publicly retracted
earlier, broader claims, and nothing in this paper depends on them.

The scale is
$$a_0 \;=\; \kappa\, c\,\sqrt{G\rho_\Lambda}\,,\qquad \kappa=\tfrac12 ,$$
equivalently $a_0=cH_\Lambda/Z$ with $Z=\sqrt{32\pi/3}=5.78881$, since

$$
H_\Lambda=\sqrt{\tfrac{8\pi G\rho_\Lambda}{3}}
\;\Longrightarrow\;
\frac{cH_\Lambda}{Z}=c\sqrt{\frac{8\pi G\rho_\Lambda}{3}}\cdot\sqrt{\frac{3}{32\pi}}
=c\sqrt{\frac{G\rho_\Lambda}{4}}=\tfrac12 c\sqrt{G\rho_\Lambda}.
$$

Every $\pi$, the $32$ and the $3$ cancel. Numerically $a_0=9.36\times10^{-11}\,\mathrm{m\,s^{-2}}$ on
the pure-$\Lambda$ footing.

**Credit where it is due.** The interpolating kernel used by this framework,
$\nu(y)=\sqrt{1+1/y}$, is identical to Milgrom (1999, *Phys. Lett. A* **253**, 273, Eq. 9). The
framework's distinctive content is the **coefficient** $cH_\Lambda/Z$ (Milgrom's was $2cH_\Lambda$)
and the modified-inertia completion. The *value* of $\kappa$ is not derived; ghost-freedom, unitarity
and holography have each been shown insufficient to force it. This is a one-parameter effective
theory, not a zero-parameter derivation.

**The consequence used below.** Because $a_0\propto\sqrt{\rho_\Lambda}$,
$$\boxed{\;\frac{a_0(z)}{a_0(0)}=\sqrt{\frac{\rho_{\rm DE}(z)}{\rho_{\rm DE}(0)}}\;}$$
and for the CPL parametrisation $w(a)=w_0+w_a(1-a)$,
$$\frac{\rho_{\rm DE}(z)}{\rho_{\rm DE}(0)}=(1+z)^{3(1+w_0+w_a)}\exp\!\left(\frac{-3w_a z}{1+z}\right),$$
so
$$\frac{a_0(z)}{a_0(0)}=(1+z)^{\frac32(1+w_0+w_a)}\exp\!\left(\frac{-3w_a z}{2(1+z)}\right).$$

This is a **bump-then-decline**, not a monotone rise. A linearisation that drops $w_a$ produces a
spurious monotone rise; that error has been made and is corrected here explicitly.

---

## 3. The absorption function $A(z)$

$\Lambda$CDM has no $a_0$. The mass-discrepancy-acceleration relation emerges from halo structure plus
baryonic physics, and the characteristic acceleration of a virialised halo inherits the collapse
density, $g_\dagger\sim\sqrt{G\rho_{\rm crit}(z)}\propto H(z)$. Therefore the **unadjusted**
$\Lambda$CDM expectation is
$$\frac{g_\dagger(z)}{g_\dagger(0)}=E(z),\qquad
E(z)=\sqrt{\Omega_m(1+z)^3+(1-\Omega_m)\frac{\rho_{\rm DE}(z)}{\rho_{\rm DE}(0)}}.$$

Define the absorption function as the ratio a $\Lambda$CDM account must supply:
$$\boxed{\;A(z)\;\equiv\;\frac{[a_0(z)/a_0(0)]_{\rm framework}}{E(z)}\;}$$

### 3.1 Verified inputs

DESI DR2 CPL fits, verified against arXiv:2508.10514v7 Table 4 and arXiv:2503.14738
(*Phys. Rev. D* **112**, 083515):

| combination | $w_0$ | $w_a$ | $w_0{+}w_a$ | significance |
|---|---|---|---|---|
| $\Lambda$CDM (reference) | $-1.000$ | $0.00$ | $-1.000$ | — |
| DR2+CMB+Pantheon+ | $-0.858\pm0.058$ | $-0.58\pm0.24$ | $-1.438$ | $2.8\to3.2\sigma$ |
| DR2+CMB+DES-Dovekie | $-0.821\pm0.059$ | $-0.73^{+0.27}_{-0.24}$ | $-1.551$ | $4.2\to3.4\sigma$ |
| DR2+CMB+Union3 | $-0.662\pm0.091$ | $-1.15\pm0.33$ | $-1.812$ | $3.8\to3.4\sigma$ |
| DR2+CMB (no SN) | $-0.420\pm0.21$ | $-1.75\pm0.58$ | $-2.170$ | $3.1\sigma$ |

The arrows are the post-recalibration significances reported by Nadathur (Moriond 2026) following
Popovic et al. (2025) and Hoyt et al. (2026). **They are converging on $\sim3.2$–$3.4\sigma$ and the
$4.2\sigma$ headline is gone.** This framework's cosmological prediction requires the evolving-DE
signal to survive, so a softening trend is a liability, and it is recorded here rather than omitted.

### 3.2 Results, $\log_{10}A(z)$ in dex

Canonical ($\rho_{\rm DE}$) footing, $\Omega_m=0.315$:

| combination | $z{=}0.5$ | $z{=}1$ | $z{=}2$ | $z{=}3$ |
|---|---|---|---|---|
| $\Lambda$CDM (reference) | $-0.121$ | $-0.253$ | $-0.482$ | $-0.660$ |
| DR2+CMB+Pantheon+ | $-0.115$ | $-0.260$ | $-0.539$ | $-0.769$ |
| DR2+CMB+DES-Dovekie | $-0.113$ | $-0.262$ | $-0.554$ | $-0.797$ |
| DR2+CMB+Union3 | $-0.101$ | $-0.247$ | $-0.558$ | $-0.827$ |
| DR2+CMB (no SN) | $-0.081$ | $-0.221$ | $-0.554$ | $-0.857$ |

Negative values mean crispy dark matter must **suppress** its natural acceleration scale relative to
the $E(z)$ expectation.

---

## 4. The minimal knob

**Stated plainly: this is our construction, not anyone's proposal.** We ask what the *cheapest*
modification is that delivers $A(z)$, so that the parameter cost is a lower bound rather than a straw
figure.

Crispy dark matter $=\Lambda$CDM $+$ a monotone suppression $A(z)$ of the emergent acceleration scale,
delivered through:

1. **Concentration evolution.** For an NFW halo the characteristic acceleration scales as
   $g_\dagger\propto c^{\alpha}$ with $\alpha\simeq1$–$2$ depending on the radius at which the
   relation is evaluated. A required $\Delta\log_{10}g_\dagger$ is then supplied by
   $\Delta\log_{10}c=\Delta\log_{10}A/\alpha$. At $z=1$, $A=-0.262$ dex needs
   $\Delta\log_{10}c\simeq-0.131$ to $-0.262$, i.e. concentrations lower by $26\%$–$45\%$ beyond the
   standard fit. *The exponent $\alpha$ is indicative; a defensible value requires a halo-model
   derivation of the relation's normalisation, which we do not attempt here.*
2. **Feedback strength as a function of $z$**, adjusting the baryon distribution so the relation's
   normalisation moves with redshift.

**Minimal parametrisation.** A monotone $A(z)$ over $0<z<3$ requires at least two parameters, e.g.
$$A(z)=1+\epsilon_1\frac{z}{1+z}+\epsilon_2\left(\frac{z}{1+z}\right)^2 ,$$
which fits the DES-Dovekie row with $\epsilon_1=-0.394$, $\epsilon_2=-1.010$ (max residual $0.023$ in $A$). That residual is $\simeq0.06$ dex at $z=3$ — **comparable to the
signal itself** — so two parameters is a genuine floor and not an adequate fit. A realistic
accommodation needs three or more, which makes the ledger of §5 *conservative*: we charge crispy dark
matter one ban when the honest charge is larger. Realistically a
free function is used, but **two** is the honest floor and is what we charge below.

The framework's count is **zero** new parameters: $a_0(z)$ follows from $(w_0,w_a)$, subject to the
conditionality in §6.3.

---

## 5. The Occam ledger

Both models will fit. The comparison is therefore not about fit quality but about parameter cost. For
$N$ measurements of the relation's normalisation at per-point precision $\sigma$ dex and signal $s$
dex, the evidence ratio in bans (powers of ten) is approximately
$$\mathcal{B}\;\simeq\;\frac{1}{2\ln 10}\,N\left(\frac{s}{\sigma}\right)^{2}\;-\;n_{\rm extra} ,$$
with $n_{\rm extra}\simeq1$ ban charged for crispy dark matter's two additional parameters.

Scored on the **DESI-dependent** signal, $s=0.141$ dex at $z=3$ (see §6.1 — scoring on the $0.25$ dex
figure would double-count an accommodation already made):

| $N$ | $\sigma$ (dex) | bans favouring the framework |
|---|---|---|
| 5 | 0.10 | 1.2 |
| 5 | 0.05 | 7.6 |
| 20 | 0.10 | 7.6 |
| 20 | 0.05 | 33.5 |
| 50 | 0.10 | 20.6 |
| 50 | 0.05 | 85.3 |

**Symmetric statement.** The same arithmetic runs *against* the framework, and harder, if the measured
$a_0(z)$ lands off the parameter-free curve — precisely because the framework cannot move.

---

## 6. Three results that reduce the claim

### 6.1 Most of the requirement is not DESI-dependent

Compare the $\Lambda$CDM reference row of §3.2 ($-0.253$ dex at $z=1$, with $a_0$ **constant**) against
DES-Dovekie ($-0.262$ dex). Nearly identical. The bulk of the absorption requirement is the long-known
constant-$a_0$-versus-rising-$E(z)$ tension, which $\Lambda$CDM already accommodates and largely
successfully. The genuinely new content is the departure of $a_0(z)$ from constant:

| combination | $z{=}0.5$ | $z{=}1$ | $z{=}2$ | $z{=}3$ |
|---|---|---|---|---|
| DR2+CMB+Pantheon+ | $+0.010$ | $-0.009$ | $-0.062$ | $-0.112$ |
| DR2+CMB+DES-Dovekie | $+0.013$ | $-0.011$ | $-0.077$ | $-0.141$ |
| DR2+CMB+Union3 | $+0.035$ | $+0.008$ | $-0.082$ | $-0.171$ |
| DR2+CMB (no SN) | $+0.071$ | $+0.042$ | $-0.077$ | $-0.202$ |

All four combinations agree on three structural facts, so these are robust to which supernova sample
prevails: the signal is $\sim0.01$ dex at $z=1$ (negligible), it **changes sign** near $z\simeq1$, and
it reaches only $0.11$–$0.20$ dex by $z=3$.

**Consequence: this is a $z\gtrsim2$ test.** Redshift $\simeq1$, where most resolved high-redshift
kinematics exists, has almost no discriminating power for the DESI-dependent part.

### 6.2 On the alternative footing the prediction is empty

The framework admits a second footing, $a_0=cH(z)/Z$ with the total density. There
$a_0(z)/a_0(0)=E(z)$ **identically**, so
$$A(z)=\frac{E(z)}{E(z)}=1 \quad\text{exactly, for every }z\text{ and every }(w_0,w_a).$$
Verified as exactly zero in dex for all four fits. The framework and $\Lambda$CDM then predict the
same redshift scaling, are indistinguishable in this channel, and crispy dark matter never needs to
exist.

**The footing choice is not a detail in this test; it is the experiment.** The framework must commit
to the $\rho_{\rm DE}$ footing to have a claim here, and that commitment is itself falsifiable.

### 6.3 The input is not independent of the framework

The $(w_0,w_a)$ used above were inferred by fitting supernova and BAO distances **assuming standard
inertia and standard growth** — the assumption this framework denies. The input is independent only if
modified inertia does not affect the distance–redshift relation. That is nowhere established, and
since
$$\frac{cH_0}{a_0}=7.00 ,$$
cosmological dynamics sits at the same order as $a_0$ and cannot be assumed to be in the Newtonian
regime without a calculation.

**Therefore "parameter-free" in §4 is conditional on an unbuilt result.** The structural findings of
§6.1 and §6.2 are shape statements and are unaffected.

---

## 7. A mutually exclusive reading of the same data, and how to decide it

Dodelson (2026) notes that in the DESI-favoured region "the energy density of dark energy is actually
increasing as the universe expands," and that most workers are unwilling to cross that line. We
confirm this from the fitted values: every supernova-inclusive fit has $w_0+w_a<-1$, crossing
$w=-1$ at $z_{\rm cross}=0.32$–$0.50$, with $\rho_{\rm DE}(3)/\rho_{\rm DE}(0)=0.60$ down to $0.40$.

Because $a_0\propto\sqrt{\rho_\Lambda}$, **this paper's prediction is a rider on the disputed
feature.** If the field retreats from phantom behaviour, $(w_0,w_a)\to(-1,0)$ and the signal of §6.1
goes to zero. Two readings are therefore available:

- **Branch A (this paper).** $\Lambda$ evolves $\Rightarrow a_0$ evolves $\Rightarrow$ crispy dark
  matter owes $A(z)$.
- **Branch B.** $\Lambda$ is constant, the apparent evolution is an artifact of standard-inertia
  distance fitting, and $a_0$ is **constant**.

**They cannot both hold**, and this paper does not assert Branch A over Branch B. They separate by
$0.077$ dex at $z=2$ and $0.141$ dex at $z=3$, so a high-redshift normalisation measurement at
$\sim0.05$ dex decides between them. The contradiction is an experiment.

We note the author's current preference is **Branch B**, on the grounds that it keeps $a_0$ constant
(independently favoured by the low-redshift relation), removes §6.3's circularity, and does not
require the growing-$\rho_{\rm DE}$ behaviour the field disputes. This paper is published as the
**conditional** statement of Branch A: *if* $\Lambda$ evolves, here is what $\Lambda$CDM owes.

---

## 8. Prior art, and what is not claimed

The mechanism class invoked by Branch B — modified gravity producing effective phantom behaviour
without a fundamental phantom field — is **long established**: f(R) (arXiv:0909.0351), scalar–tensor
(arXiv:1204.0369), running vacuum "mirage" phantom (*MNRAS* **437**, 3331), and a 2026 review devoted
to the point (arXiv:2605.27301). The MOND-specific route is separately occupied: dark energy as a
Friedmann modification (arXiv:astro-ph/0301510), Cardassian expansion, Modified Friedmann Dynamics
(arXiv:0712.4232), and extended Friedmann equations *introducing Milgrom's acceleration constant* to
obtain accelerated expansion without dark energy (arXiv:2012.03446). **No novelty is claimed for
Branch B's mechanism.**

For the redshift evolution of the Tully–Fisher relation as a modified-gravity test, see Gnedin (2008),
arXiv:0809.2790, which anticipates the general observational strategy.

What this paper claims as new is narrower and methodological: the **explicit absorption function**
$A(z)$ for an $a_0\propto\sqrt{\rho_\Lambda}$ scale, its **parameter ledger in bans**, and the
**pre-registration** of both, including the finding that the alternative footing empties the test.

---

## 9. Pre-registered scoreboard (frozen 2026-07-30)

### 9.1 What would count as accommodation

1. Concentration-evolution fits acquiring a redshift-dependent normalisation matching $A(z)$ within
   errors, introduced to fit high-redshift kinematics rather than derived from N-body simulation.
2. Feedback retuning that lowers the effective acceleration scale at $z\sim1$–$2$ by the dex amounts
   of §3.2, presented as resolving a high-redshift "tension".
3. **The tell:** any new free function of redshift in the halo–galaxy connection whose fitted shape
   tracks $\sqrt{\rho_\Lambda(z)}$ rather than $E(z)$. There is no $\Lambda$CDM reason for halo
   structure to know the dark-energy density.

### 9.2 What would falsify the framework

1. A measured $a_0(z)$ tracking $E(z)$ within errors: the canonical footing is wrong, and by §6.2 the
   alternative footing predicts nothing distinctive here.
2. A measured $a_0(z)$ rising monotonically and steeply: inconsistent with bump-then-decline for any
   $(w_0,w_a)$ DESI allows.
3. DESI DR3+ converging on $w_0=-1$, $w_a=0$: $\rho_\Lambda$ constant, $a_0$ constant, and this
   paper's prediction is deleted. **The test is hostage to DESI, not to $\Lambda$CDM.**

### 9.3 Amplitude caution

The whole supernova-inclusive phantom signal is a distance-modulus tilt of $0.025$–$0.069$ mag,
against $\sim0.15$ mag Type Ia intrinsic scatter. It is comparable in size to calibration systematics
still being revised: the DES-Dovekie recalibration moved that sample by $\sim0.8\sigma$. Neither this
framework nor crispy dark matter should stake a claim on a signal that photometric recalibration is
still moving by the amplitude of the signal itself.

---

## 10. Reproducibility

Every number is produced by committed, runnable scripts that exit non-zero if any internal check
fails. No verdict is hard-coded.

| script | content |
|---|---|
| `mi_crispy_dark_matter_ledger_2026.py` | $A(z)$, footing fork, Occam ledger, scoreboard; Amendment 1 records §6.3 and §7 |
| `mi_phantom_artifact_2026.py` | §7 phantom verification, $cH_0/a_0$, distance-modulus amplitudes |
| `mi_phantom_prior_art_and_exclusivity_2026.py` | §8 prior art, §7 branch separation |
| `mi_kappa_spectral_reduction_2026.py` | §2 $\kappa$ reduction $a_0=\kappa c\sqrt{G\rho_\Lambda}$ |

---

## References

- DESI Collaboration, *DESI DR2 results II*, arXiv:2503.14738; *Phys. Rev. D* **112**, 083515.
- *Evidence for evolving dark energy from DESI DR2 BAO and Pantheon+, DES-Dovekie, and Union3*,
  arXiv:2508.10514v7; *Eur. Phys. J. C* 10.1140/epjc/s10052-026-15806-w.
- DES Collaboration, SN reanalysis with updated Type Ia calibration, *MNRAS* **548**, stag632.
- S. Nadathur, Moriond 2026 (significance update); Popovic et al. 2025; Hoyt et al. 2026.
- S. Dodelson, *Evolving Dark Energy*, Modern Cosmology, 2026-07-23.
- M. Milgrom, *Phys. Lett. A* **253**, 273 (1999) — the $\nu(y)=\sqrt{1+1/y}$ kernel.
- O. Gnedin, arXiv:0809.2790 — Tully–Fisher evolution as a modified-gravity test.
- Effective phantom prior art: arXiv:0909.0351; arXiv:1204.0369; *MNRAS* **437**, 3331;
  arXiv:2605.27301; arXiv:2605.26259.
- MOND/Friedmann prior art: arXiv:astro-ph/0301510; arXiv:0712.4232; arXiv:2012.03446;
  *MNRAS* **356**, 475.
