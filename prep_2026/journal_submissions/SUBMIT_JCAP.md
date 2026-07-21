# JCAP Submission Package

**Target journal:** *Journal of Cosmology and Astroparticle Physics* (JCAP)
**Working title:** *A parameter-free, pre-registered test that the galaxy acceleration scale tracks the dark-energy density: $a_0(z)/a_0(0)=\sqrt{\rho_{\rm DE}(z)/\rho_{\rm DE,0}}$*
**Author:** Carl P. Zimmerman (Briar Creek Tech; independent researcher — no academic affiliation) · carl@briarcreektech.com
**Article type:** Regular article (falsifiable-program + pre-registered test)
**Prepared:** 2026-07-21

> This package contains the five editor-facing components only: (1) cover letter, (2) referee-anticipation memo, (3) novelty statement, (4) calibrated abstract, (5) reformatting/consolidation plan. It does **not** contain the manuscript body — the physics is already written up in the Zenodo source deposits listed in Part 5, which this submission consolidates.

---

## PART 1 — COVER LETTER TO THE EDITOR

Dear Editors of JCAP,

I submit for your consideration a manuscript presenting **a single, parameter-free, falsifiable prediction and a pre-registered protocol to test it**: that the galaxy acceleration scale $a_0$ tracks the dark-energy density across cosmic time,
$$a_0(z)/a_0(0) = \sqrt{\rho_{\rm DE}(z)/\rho_{\rm DE,0}}.$$

**The one result.** In the de Sitter–Unruh *modified-inertia* framework, the low-acceleration scale is sourced by the cosmological horizon, $a_0 = cH_\Lambda/Z$. Promoting this relation adiabatically as the horizon evolves yields the displayed law. The observable I test is the ratio $R\equiv a_0(z)/a_0(0)$, which is **independent of the framework's internal normalization $Z$ and of the absolute value of $a_0$** — both cancel identically in a ratio. $R$ therefore depends only on the measured dark-energy expansion history $w(z)$. This turns an otherwise metaphysical "why is $a_0\approx c\sqrt{\rho_\Lambda}$" coincidence into a quantitative, redshift-dependent prediction that current and forthcoming data can decide.

**Why it fits JCAP.** The claim lives precisely at the cosmology / astroparticle interface that JCAP serves: it connects a galactic-dynamics scale to the dark-energy equation of state, is confronted against DESI DR2 $w_0w_a$ constraints, and is pre-registered against the Rubin/LSST supernova cosmology stream. It is a cosmological test of a dark-sector-adjacent hypothesis, evaluated with standard CPL machinery — the same tooling your readership uses for $w(z)$ inference. The manuscript is a *falsifiable program with a hashed, pre-committed decision procedure*, not a discovery announcement.

**Honest scope, stated up front.** I want to be transparent with the editor about three limitations that the manuscript treats openly rather than burying:

1. The prediction **inherits** $w(z)$: it is a *consequence* of an evolving dark-energy sector, not an independent measurement of one. If $w=-1$, the prediction collapses to constant-$a_0$ MOND and there is no distinctive signal. I frame this as the falsifiable content, not as a weakness to be hidden.
2. The $a_0\propto\sqrt{\rho_{\rm DE}}$ coincidence is **not original to me** — Limbach, Psaltis & Özel (2008) noted it and tested $a_0$–$H_0$ / $a_0$–$\rho_{\rm DE}$ couplings against Tully–Fisher data to $z\simeq1.2$. My addition is the *horizon-sourced dynamical promotion* of that coincidence to a law with a committed test, not the coincidence itself.
3. The value of $a_0$, the normalization $Z$, and the sign of the effect are **posited, not derived**. The kernel $\nu=\sqrt{1+1/y}$ is the identical functional form to Milgrom (1999); the distinctive content is the $cH_\Lambda/Z$ *coefficient* plus the modified-inertia completion.

**What I am asking JCAP to referee** is therefore not "is the framework correct" but "is this a well-posed, honestly-bounded, pre-registered cosmological test of a specific falsifiable prediction, worth having on the record before the Rubin calibrated sample lands (~2027+)." I believe it is, and that the pre-registration discipline — the estimator, thresholds, and data hierarchy are SHA-256-hashed and Zenodo-timestamped *before* the deciding data exist — is exactly what this class of claim needs to be taken seriously.

I am an independent researcher without academic affiliation. I am aware that modified-gravity/inertia attracts a high volume of under-calibrated submissions, and I have tried to write this manuscript to the opposite standard: every quantitative figure is produced by a committed, runnable script; every claim is bounded both ways; and I state plainly where the honest answer is "this is a real limitation." I publicly retracted earlier over-broad "theory of everything" claims in 2026; my position here is strictly the $a_0(z)$ reframing and its test.

The work has not been submitted elsewhere and is not under consideration by another journal. The Zenodo deposits it consolidates are raw preprints/pre-registrations by the same author (listed in the manuscript), released for reproducibility and timestamping; this manuscript is their consolidated, peer-review-facing version. I have no competing interests to declare and no funding to report.

Thank you for your consideration.

Carl P. Zimmerman
Briar Creek Tech
carl@briarcreektech.com

---

## PART 2 — REFEREE-ANTICIPATION MEMO

*The hardest attacks a JCAP referee will make, and the honest answer to each. Where the honest answer is "yes, that is a real limitation," it says so.*

### Attack 1 — "This is not a prediction, it is a re-labelling of $w(z)$. The framework simply inherits the dark-energy history; you have measured nothing about galaxies."
**Honest answer: substantially correct, and the manuscript says so in the abstract and scope section.** The cosmology-side gate ($R$ from a supernova/BAO $w_0w_a$ posterior) *is* a consequence of $w(z)$, not an independent measurement. Its value is threefold and no more: (i) it makes the framework **falsifiable** — a measured *rise* in $a_0$ with $z$ at $\ge3\sigma$ kills the $\sqrt{\rho_{\rm DE}}$ footing, and $w\to-1$ dissolves the distinctive claim; (ii) it fixes the *sign and amplitude* the genuinely independent galaxy-side test must find; (iii) it is pre-registered, so the mapping from $w(z)$ to $R$ cannot be tuned after the fact. The **independent** content lives entirely on the galaxy side (Attack 4). We do not claim the cosmology gate is independent evidence; we claim it is a necessary, pre-committed consistency condition. GATE OPEN means "survives to face the galaxy-side test," explicitly not "confirmed."

### Attack 2 — "$a_0\sim c\sqrt{\rho_{\rm DE}}$ is Limbach–Psaltis–Özel (2008). What is new?"
**Honest answer: the coincidence is theirs; the dynamical promotion and the pre-registered cross-scale test are the new content.** LPO (2008) noted the numerical coincidence and tested $a_0$ coupled to $H_0$ *or* to $\rho_{\rm DE}$ against Tully–Fisher data to $z\simeq1.2$, treating it as one candidate scaling among several. The framework's addition is to *derive* the $\sqrt{\rho_{\rm DE}}$ scaling as the adiabatic consequence of a horizon-sourced $a_0=cH_\Lambda/Z$ (so the coupling is not a free choice between $H_0$ and $\rho_{\rm DE}$ — it is fixed to $\rho_{\rm DE}$ by the construction), and to commit a hashed decision procedure against the Rubin era. We credit LPO explicitly and prominently. We do **not** claim to have discovered the scaling. If the referee judges the incremental step (coincidence → posited law → pre-registered test) insufficiently novel for a full article, that is a fair editorial call; our answer is that a *committed, falsifiable* version of a previously-loose coincidence, with a live near-term test, is a publishable contribution.

### Attack 3 — "The evolution law $a_0\propto\sqrt{\rho_{\rm DE}}$ is itself posited ('adiabatic-horizon ansatz'), and a rival footing $a_0\propto cH(z)$ gives the opposite sign. You have chosen the footing that fits."
**Honest answer: the two footings are a real, acknowledged fork, and we commit to one *in advance* rather than choosing post hoc.** There genuinely are two logically distinct footings: $a_0\propto\sqrt{\rho_{\rm DE}}$ (declines at high $z$ under evolving DE) versus $a_0\propto cH(z)=cH_0E(z)$ (rises with $z$). The manuscript states this openly and **pre-registers the $\sqrt{\rho_{\rm DE}}$ footing as the prediction under test**. Crucially, this is not fitting: a measured rise does not get re-interpreted as the rival footing succeeding — it registers as **Verdict C (framework strained/falsified)** in the frozen protocol. The adiabatic promotion is posited, not derived; we say so. The defense is procedural (commit before data), not a claim that the law is uniquely forced.

### Attack 4 — "The galaxy-side test — your only independent content — is underpowered and hostage to $M_{\rm bar}$."
**Honest answer: yes, at present it is underpowered and $M_{\rm bar}$-dominated; it is neither passed nor failed.** This is stated as the central limitation of the independent lane. The galaxy-side observable is the deep-MOND BTFR zero-point, $a_0(z)/a_0(0)=(V_z/V_0)^4/(M_{{\rm bar},z}/M_{{\rm bar},0})$, which reads $a_0$ *only* for clean deep-MOND objects (fitted slope exactly 4). At present: $z=0$ is solid (SPARC, $N=175$, anchored to 1.00); $z=3.25$ is a single clean object (the "Big Wheel," $R\approx1.0$–$1.3$, consistent with flat, ~2σ against the rival *rising* footing, cannot see the predicted decline). The intermediate-$z$ ($z\sim1$–$2.3$) rotators sit at $g\gtrsim a_0$ (not deep-MOND), their fitted slopes are $3.0$–$3.85$ not $4$, and the inferred "$a_0$ evolution" is **sign-contested** — Übler+2017 (fixed slope) reads it rising, Sharma+2024 (free shallow slope) the opposite, Di Teodoro+2016 / Tiley+2019 read null. $M_{\rm bar}$ (IMF, $\alpha_{\rm CO}$, SED stellar masses, dust) is the dominant systematic and on the Big Wheel alone contributes a factor ~2. **The honest verdict: the galaxy-side test is currently underpowered — not passed, not failed.** We forecast that $N\approx20$–$40$ clean deep-MOND $z\sim2$–$3$ disks with $M_{\rm bar}$ to ~0.1 dex (feasible with JWST/ALMA + ELT/HARMONI) reach $3\sigma$ on the declining track. We present this as a program, not a result.

### Attack 5 — "The headline $R=a_0(3)/a_0(0)$ is a CPL extrapolation to $z=3$, well beyond where the supernovae live ($z\lesssim1.2$). The number is a lever arm, not a measurement."
**Honest answer: correct, and it is documented as limitation #1 in the frozen protocol.** The LSST photometric SN sample constrains $w(z)$ mainly at $z\lesssim1.2$; the gate is read at $z=3$. Propagating the *same* DESI DR2 posterior to different reference redshifts gives decline significance $0.34\sigma$ at $z=1$ ($R=0.99$, effectively flat), $1.7\sigma$ at $z=2$, $2.0\sigma$ at $z=3$, $2.4\sigma$ at $z=10$. So the headline depends on the frozen choice $z=3$. What the gate *genuinely* tests is whether the SN-constrained $(w_0,w_a)$ posterior excludes the non-evolving point $(-1,0)$; the $z=3$ evaluation converts that into an $a_0$-ratio but adds no independent $z=3$ information. The manuscript states explicitly that $R(z{=}3)=0.775$ must **not** be read as a measured $z=3$ acceleration scale. We chose $z=3$ (frozen, hashed) as a fixed lever arm before seeing data; the significance is honestly a $(w_0,w_a)$-exclusion significance re-expressed as a ratio.

### Attack 6 — "Your own $a_0(z)$ is non-monotonic — it bumps *up* at low $z$. So at the redshifts the galaxy-side test can actually reach, the framework predicts a *rise*, not a decline. The two halves of your program contradict each other."
**Honest answer: the non-monotonicity is real, we call it out, and it is a genuine tension between the two lanes' accessible redshifts.** Under the DESI-central CPL history $a_0(z)$ is not monotonic: $R$ peaks at $\approx1.036$ near $z\approx0.35$ and only crosses below unity at $z\approx0.9$; the decline is a high-$z$ phenomenon. The galaxy-side test is most tractable at low $z$ — inside the *bump*. So a GATE-OPEN verdict on the $z=3$ decline does **not** translate into a low-$z$ decline for the galaxy side to corroborate; at $z\lesssim0.5$ the framework predicts a slight *rise* (a few percent), at $z\sim1$ essentially no change. Anyone carrying "the framework predicts $a_0$ declines" to low-$z$ observers would have the sign wrong. We state this plainly: the two lanes probe opposite branches of the same non-monotonic curve, and the amplitude available to the galaxy side ($\sim$few percent at accessible $z$) is far smaller than the $z=3$ headline. This is the single most important caveat for a reader and it is in the abstract-level scope.

### Attack 7 — "This is modified inertia without a covariant field theory. Why should JCAP treat the cosmological law as well-defined when the underlying dynamics are not?"
**Honest answer: the cosmological *test* is deliberately decoupled from the field-theory completion, and we do not lean on the latter.** The observable $R$ requires only the scalar relation $a_0(z)/a_0(0)=\sqrt{\rho_{\rm DE}(z)/\rho_{\rm DE,0}}$ and a $w(z)$ posterior — it does not invoke a Lagrangian. There is a separate modified-inertia field-theory manuscript (Zenodo, cited), but this submission does not depend on its completeness, and we do not present the covariant program as settled. The referee is right that a full covariant modified-inertia theory is not in hand; we scope the paper so that nothing in the test rests on it. This is a limitation of the *framework*, disclosed, but not of the *test*.

### Attack 8 — "The decision band $[0.55,0.85]$ for 'GATE OPEN' looks gerrymandered to contain the DESI value $R=0.775$."
**Honest answer: the band is wider than our own nominal claim and is set by the plausible $(w_0,w_a)$ spread, not by the DESI point — but the referee is right to be suspicious and we show the derivation.** The band is fixed and hashed before the deciding data. Its width comes from the spread of currently-allowed dark-energy histories (holding $w_a=-0.62$: $w_0\approx-0.79\to R=0.85$ mild evolution; $w_0\approx-1.00\to R=0.55$ strong evolution), **not** from the two value footings (which give identical $R$ at fixed $(w_0,w_a)$ and so cannot widen it). We flag two honesty points ourselves: (i) the band $[0.55,0.85]$ is deliberately *wider* than the nominal distinctive claim $R\approx0.60$–$0.75$, and the DESI value $0.775$ sits just *above* the nominal $0.75$ though inside the operational band; (ii) the upper edge $0.85$ is close to flat, so "supported" at that edge is a weak decline — the intended cost of a band broad enough not to be tuned to one posterior.

### Attack 9 — "The current state is a $2.0\sigma$ hint from DESI. That is not evidence for anything, and DESI's own $w_0w_a$ evolution is contested."
**Honest answer: agreed — the current verdict is UNDECIDED, and we neither upgrade nor manufacture it.** At the freeze, DESI DR2 (+CMB+Pantheon+) gives $R=0.775\,[0.68,0.88]$, a $2.0\sigma$ decline — *below* our committed $3\sigma$ bar, hence **UNDECIDED**, an explicit non-detection. We note that DESI's evidence for evolving DE is itself contested and depends on the SN compilation (DESY5/Union3 prefer stronger evolution; the state stays UNDECIDED under all of them). The value of the paper is the *committed forward test*, not the current hint. If DESI's evolution washes out toward $w=-1$, the distinctive prediction dissolves into constant-$a_0$ MOND — the stated safe core.

### Attack 10 — "An unaffiliated author with a home-grown 'framework' in modified gravity. Why should this clear the bar?"
**Honest answer: judge the test, not the author.** The manuscript is written so that affiliation is irrelevant to its evaluation: (i) every quantitative figure is produced by a committed, runnable, exit-0 script, released for reproduction; (ii) the estimator, thresholds, and data hierarchy are SHA-256-hashed and Zenodo-timestamped *before* the deciding data exist, removing after-the-fact tuning; (iii) the scope is bounded both ways, with limitations stated as limitations; (iv) prior credit (Milgrom, AeST/Skordis–Zlosnik, LPO 2008) is given explicitly and the author's earlier over-claims were publicly retracted. The paper asks only that a well-posed, pre-registered, falsifiable cosmological test be evaluated on its merits. If it is judged not novel enough or not yet decisive enough, those are legitimate grounds — but they are grounds about the test, which is the intended standard.

---

## PART 3 — NOVELTY STATEMENT (vs Milgrom 1983/1999, AeST/Skordis–Zlosnik, LPO 2008)

The low-acceleration kernel $\nu=\sqrt{1+1/y}$ is the identical functional form to Milgrom's 1999 interpolation, and the covariant modified-gravity realization of a MOND-scale is AeST (Skordis & Zlosnik 2021); this work adopts both and claims neither. The redshift scaling $a_0\propto\sqrt{\rho_{\rm DE}}$ is likewise not new — Limbach, Psaltis & Özel (2008) identified the $a_0\sim c\sqrt{\rho_{\rm DE}}$ coincidence and tested candidate $a_0$–$H_0$/$a_0$–$\rho_{\rm DE}$ couplings against Tully–Fisher data to $z\simeq1.2$. **What is new here is (i) fixing that coupling to $\rho_{\rm DE}$ specifically, as the adiabatic consequence of a horizon-sourced $a_0=cH_\Lambda/Z$ rather than as one free scaling among several, yielding the parameter-free, $Z$-independent ratio $R\equiv a_0(z)/a_0(0)=\sqrt{\rho_{\rm DE}(z)/\rho_{\rm DE,0}}$; and (ii) committing this as a hashed, pre-registered cross-scale test — a cosmology-side gate (DESI/Rubin $w_0w_a$) that fixes the sign and amplitude, plus an independent galaxy-side deep-MOND BTFR-zero-point measurement — filed before the deciding Rubin/LSST calibrated supernova sample exists.** The value of $a_0$, the normalization $Z$, and the sign of the effect remain posited, not derived.

---

## PART 4 — CALIBRATED ABSTRACT

> The galaxy acceleration scale $a_0\approx1.2\times10^{-10}\,{\rm m\,s^{-2}}$ that sets the onset of the mass-discrepancy/MOND regime coincides numerically with $c\sqrt{\rho_\Lambda}$ — a fact noted by Limbach, Psaltis & Özel (2008). In the de Sitter–Unruh modified-inertia framework this scale is sourced by the cosmological horizon, $a_0=cH_\Lambda/Z$; promoting it adiabatically as the horizon evolves fixes the coupling to the dark-energy density and yields a parameter-free redshift law, $a_0(z)/a_0(0)=\sqrt{\rho_{\rm DE}(z)/\rho_{\rm DE,0}}$. We study the ratio $R\equiv a_0(z)/a_0(0)$, which is independent of the framework's internal normalization $Z$ and of the present-day value of $a_0$ (both cancel), so that it depends only on the measured dark-energy equation of state $w(z)$. We show this makes the framework falsifiable: under a CPL history $R$ declines with redshift if and only if dark energy evolves, and reduces to constant-$a_0$ MOND if $w=-1$. We confront the prediction non-circularly across two scales — a cosmology-side gate driven by DESI DR2 $w_0w_a$ constraints, which fixes the required sign and amplitude, and an independent galaxy-side measurement of $a_0(z)$ from the deep-MOND baryonic Tully–Fisher zero point. We state the limitations plainly: the cosmology gate inherits $w(z)$ and is a consistency condition rather than independent evidence; the reference ratio at $z=3$ is a CPL extrapolation beyond the supernova range; the predicted $a_0(z)$ is non-monotonic (a few-percent rise at $z\lesssim0.5$ before declining at high $z$), so the two scales probe opposite branches of the same curve; and the galaxy-side test is at present $M_{\rm bar}$-dominated and underpowered (neither passed nor failed). At present DESI DR2 gives $R=0.775\,[0.68,0.88]$, a $2.0\sigma$ hint below our committed $3\sigma$ bar — undecided. We therefore pre-register — with a hashed, timestamped estimator, decision thresholds, and data hierarchy fixed before the data exist — the test against the forthcoming Rubin/LSST calibrated supernova cosmology sample (expected $\gtrsim2027$), which forecasts project to settle the gate at the $3$–$6\sigma$ level by $\sim$2028–2030. The value of $a_0$, the normalization $Z$, and the sign of the effect are posited, not derived; the kernel $\nu=\sqrt{1+1/y}$ is Milgrom's (1999) and the covariant MOND-scale realization is AeST (Skordis & Zlosnik 2021). The contribution is a bounded, falsifiable, pre-registered program, not a detection.

*(~300 words; JCAP places no hard abstract limit but favours a single self-contained paragraph. Trim to ~200 words if the editor requests, by cutting the limitations sentence to a clause and dropping the credit sentence to the acknowledgements.)*

---

## PART 5 — REFORMATTING / CONSOLIDATION PLAN

### 5.1 Source deposits to consolidate (three → one)

| # | Zenodo source | Role in the JCAP manuscript |
|---|---|---|
| 1 | **Parameter-free $a_0(z)$ test** — DOI 10.5281/zenodo.20737162 | Core: the law $a_0(z)/a_0(0)=\sqrt{\rho_{\rm DE}/\rho_{\rm DE,0}}$, its derivation from $a_0=cH_\Lambda/Z$, $Z$-independence of $R$, CPL form, and the DESI-driven current state. Becomes §2–§3. |
| 2 | **Non-circular cross-scale test** — concept DOI 10.5281/zenodo.21440407 | The two-scale confrontation: cosmology-side gate + independent galaxy-side BTFR-zero-point $a_0(z)$; the non-circularity argument; the galaxy-side data ladder (SPARC anchor, Big Wheel, contested intermediate-$z$). Becomes §4 (galaxy side) + the non-circularity subsection of §3. |
| 3 | **Rubin/LSST pre-registration** — DOI 10.5281/zenodo.21478568 | The frozen estimator, decision thresholds, data hierarchy, refused DIY-Hubble path, forecast table, hashes. Becomes §5 (pre-registration) + §6 (forecast) + Appendix A (freeze hashes). |

The MI field-theory deposit (DOI 10.5281/zenodo.21403470) and the Gaia-DR4 pre-registration precedent are **cited, not consolidated** — the test must not depend on the covariant completion.

### 5.2 Proposed section structure (single consolidated article)

1. **Introduction** — the $a_0\approx c\sqrt{\rho_\Lambda}$ coincidence; LPO 2008; what promoting it to a law buys; the falsifiable claim; explicit scope box.
2. **The prediction** — $a_0=cH_\Lambda/Z$; adiabatic-horizon promotion; $R\equiv a_0(z)/a_0(0)=\sqrt{\rho_{\rm DE}/\rho_{\rm DE,0}}$; $Z$-independence; the value-footing vs evolution-law-footing distinction; CPL mapping; non-monotonic bump-then-decline.
3. **Non-circular cross-scale strategy** — why the cosmology gate is a *consistency condition* (inherits $w(z)$) and the galaxy side is the *independent* content; how a wrong background shifts all points together rather than manufacturing a decline.
4. **Galaxy-side $a_0(z)$** — deep-MOND BTFR zero-point estimator; SPARC $z=0$ anchor; Big Wheel $z=3.25$; the sign-contested intermediate-$z$ rotators; $M_{\rm bar}$ systematics; "underpowered, not passed/failed"; forecast sample size for $3\sigma$.
5. **Cosmology-side gate + pre-registration** — frozen estimator, thresholds (Verdicts A/B/C/UNDECIDED), data hierarchy, refused DIY-Hubble path, current DESI state (UNDECIDED, $2.0\sigma$).
6. **Forecast against Rubin/LSST** — projected FoM → decline significance; mirror test (flat-universe exclusion); "3–6σ by ~2028–2030, not a slam dunk."
7. **Limitations** (own section, not buried) — the six frozen limitations from the pre-registration, plus $M_{\rm bar}$ and the covariant-completion caveats.
8. **Conclusion** — bounded restatement: falsifiable program, pre-registered, awaiting calibrated data.
- **Appendix A** — freeze hashes (SHA-256), script inventory, reproduction instructions.

### 5.3 JCAP formatting mechanics

- **LaTeX class:** JCAP uses the **`jcappub.sty`** style with the standard `\documentclass[a4paper,11pt]{article}` + `\usepackage{jcappub}` preamble (the SISSA/IOP JCAP author template, downloadable from the JCAP author pages). Title/author/abstract/keywords via the JCAP macros; `\note`/`\keywords`/`\abstract` blocks as per template. Bibliography in the **JHEP/JCAP `.bst`** style (`\bibliographystyle{JHEP}`) with `[label]` numeric citations.
- **Length target:** **15–20 pages** in `jcappub` 11pt — comfortably fits the seven sections + one appendix. Draft to ~16 pp body; the pre-registration text is dense and compresses well from the raw Zenodo version (remove the freeze-ceremony framing that suited a standalone timestamp deposit).
- **Figures (3, all reproducible from committed scripts):**
  1. **$a_0(z)/a_0(0)$ vs $z$** — the $\sqrt{\rho_{\rm DE}}$ curve under the DESI-central CPL history with its $[16,84]$ band, flat ($w=-1$) reference line at 1.0, the low-$z$ bump annotated, and the $z=3$ read-out marked as an extrapolation. (from `a0z_gate_estimator.py` / `extract_a0z.py`)
  2. **Galaxy-side ladder** — $a_0(z)/a_0(0)$ data points: SPARC anchor (1.00), Big Wheel ($z=3.25$), the sign-contested intermediate-$z$ points with error fans, overlaid on the two footings (declining $\sqrt{\rho_{\rm DE}}$ vs rising $cHE(z)$). (from `galaxy_a0z.py`)
  3. **Forecast significance** — decline significance vs DETF FoM (DESI-now → Rubin-alone → Rubin+CMB/BAO) with the $3\sigma$ bar, plus the mirror-test exclusion. (from `forecast_rubin_a0z.py`)
- **Tables (2):** the verdict/threshold table (A/B/C/UNDECIDED) and the forecast table (FoM → $R$ → significance).
- **Data/code availability statement (JCAP encourages this):** all estimators are committed, exit-0 Python (numpy/scipy), released in the public `a0kit` repository and the three Zenodo deposits; freeze hashes in Appendix A.
- **Cover-page metadata:** single author, single affiliation (Briar Creek Tech), corresponding email; ORCID if available; JCAP keywords — suggest *modified gravity, dark energy equation of state, supernova type Ia - standard candles, redshift surveys, rotation curves of galaxies*.
- **Referee-facing framing note (in submission comments, not the paper):** flag explicitly that this is a pre-registered falsifiable-program article with a currently-UNDECIDED verdict, so the editor routes it to a referee who evaluates test design and pre-registration rather than expecting a detection.

### 5.4 What to cut from the raw Zenodo deposits when consolidating

- The standalone "freeze ceremony" prose (the timestamp/hash lock-in narrative) compresses to one paragraph + Appendix A.
- Duplicate scope statements repeated verbatim across the three deposits → state once, in the Introduction scope box, reference thereafter.
- The broker readiness-tracker count (36,836 objects) → one sentence, since it "never feeds the verdict."
- Internal framework audit tangents (κ-closure, SME bridge, cluster fronts) → out of scope; omit entirely.

---

*Package ends. Manuscript body to be assembled from the three Zenodo deposits per §5; not included here by design.*
