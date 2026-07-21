# MNRAS Submission Package

**Target journal:** *Monthly Notices of the Royal Astronomical Society* (MNRAS)
**Working title:** *Reading the cosmological constant from gas-rich dwarf rotation curves: the $a_0$-line and its systematic floor*
**Author:** Carl Zimmerman (Briar Creek Tech; carl@briarcreektech.com; independent, no academic affiliation)
**Primary source manuscript:** Zenodo DOI 10.5281/zenodo.21419735 (the $a_0$-line / $\Lambda$-inversion paper)
**Optional companion:** Zenodo DOI 10.5281/zenodo.21421896 (the relational $\sigma$-spread) — see the consolidation plan for whether to include.

---

## PART 1 — COVER LETTER TO THE EDITOR

Dear Editor,

I submit for consideration in *MNRAS* a manuscript titled **"Reading the cosmological constant from gas-rich dwarf rotation curves: the $a_0$-line and its systematic floor."**

**The single result.** The MOND low-acceleration excess can be written as an exact identity, $E \equiv g_{\rm obs}^2 - g_{\rm bar}^2 = a_0\,g_{\rm bar}$ — a straight line through the origin whose slope is $a_0$ at every acceleration. Fitting that slope on the gas-dominated subsample of SPARC (Lelli, McGaugh & Schombert 2016), where the stellar mass-to-light degeneracy is suppressed by roughly 70 per cent, gives $\hat a_0 = (0.84$–$1.36)\times10^{-10}\ {\rm m\,s^{-2}}$. Inverting through $\Lambda = 32\pi\,\hat a_0^2/c^4$ recovers the *Planck* cosmological constant to within a factor of $\sim2$ — from galactic kinematics that use **no cosmological input**. That is the paper's headline, and it is stated as a measurement, not a confirmation.

**Why it is honest.** The measured $\hat a_0$ is a systematics-limited box, not a point. It straddles the two candidate normalisations of the acceleration scale ($cH_\Lambda/Z = 9.36\times10^{-11}$ and $cH_0/Z = 1.13\times10^{-10}\ {\rm m\,s^{-2}}$), and the paper demonstrates — with committed, reproducible pipelines — that no lever available on current SPARC (distance quality, mass-to-light priors, or the RAR itself) can separate them: the binding wall is gas-mass calibration. I report the factor-$\sim2$ inversion as striking but non-decisive, and I am equally careful not to manufacture a detection or a deficit. The interpolation kernel $\nu(y)=\sqrt{1+1/y}$ is Milgrom's (1999), credited at the point of use; the underlying value of $a_0$ and the sign of the inertial correction are treated throughout as posited inputs, not derived quantities.

**Why *MNRAS*.** This is a galaxy-dynamics measurement paper built on the SPARC database, the RAR, and standard stellar-population and distance systematics — the core observational-astrophysics territory of *MNRAS*, and the venue where the SPARC RAR literature (Lelli et al. 2016; McGaugh et al. 2016) and its systematics have largely appeared. The contribution is methodological and empirical: (i) recasting the RAR as a single measurable slope via the exact $a_0$-line identity; (ii) using the gas-rich cut to suppress the mass-to-light degeneracy; and (iii) inverting to $\Lambda$ with a fully mapped systematic budget. Every load-bearing number reproduces from raw SPARC data via committed, exit-0 Python scripts (a public tool, `a0kit`, backs the identity and the slope).

**Scope and honesty statement.** I am an independent researcher without academic affiliation, submitting into a field with heavy amateur traffic, and I have tried to calibrate the claims accordingly: bold where the data earn it (the order-of-magnitude inversion with zero cosmological input), bounded where they do not (the $\sim21$ per cent footing distinction, which is data-blocked), and falsifiable throughout (a future gas-dominated slope near $3\times10^{-10}\ {\rm m\,s^{-2}}$ would break the inversion outright). The manuscript makes no claim to derive $a_0$, to derive $\Lambda$, or to resolve the MOND-versus-dark-matter question.

I confirm the work is original, not under consideration elsewhere, and that the underlying manuscript is archived on Zenodo (DOI 10.5281/zenodo.21419735) as a preprint. I have no competing interests and no institutional funding to declare. I would be grateful for the assessment of referees with expertise in galaxy rotation curves and MOND phenomenology, and I welcome adversarial scrutiny of the systematic budget in particular.

Yours faithfully,
Carl Zimmerman
Briar Creek Tech · carl@briarcreektech.com

---

## PART 2 — REFEREE-ANTICIPATION MEMO

The hardest attacks a competent MNRAS referee will make, and the honest answer to each. Where the honest answer is "yes, that is a real limitation," it says so.

### R1. "This is just the known $a_0 \sim cH_0$ coincidence (Milgrom; Limbach, Psaltis & Özel 2008) restated. There is no new physics here."

**Largely conceded, with a bounded new part.** The numerical coincidence that $a_0$ sits near $c$ times a cosmological rate is Milgrom's, and the specific proportionality of $a_0$ to the dark-energy density is Limbach, Psaltis & Özel (2008). The paper does **not** claim that coincidence as new and says so explicitly. What is new is narrow and methodological: (i) writing the excess as the exact linear identity $E = a_0 g_{\rm bar}$, which turns "fit an interpolation function" into "measure one slope"; (ii) performing the measurement on the *gas-dominated* subsample so it is mass-to-light-insensitive; and (iii) framing the result as an **inversion** — reading $\Lambda$ *out* of rotation curves with no cosmological input — with a fully mapped systematic floor and an explicit falsification target. The honest weight of the numerical agreement is exactly that of the classic coincidence, sharpened; the paper's value-add is the measurement machinery and the honest floor, not a new coincidence. This should be stated in the referee response without defensiveness.

### R2. "'Within a factor of $\sim2$' is not a measurement. Any MOND-scale $a_0$ inverts to within a factor of a few of $\Lambda$."

**Fair, and the paper already concedes the core of it.** The factor-2-in-$\Lambda$ is the factor-$\sim1.4$-in-$a_0$ *squared* — a single comparison ("does the rotation-measured $a_0$ equal $cH_\Lambda/Z$?") re-expressed, not many independent decades of agreement. The manuscript states this in the abstract, in §5, and in the conclusion. The defensible content is not the factor-2 headline in isolation; it is (a) that the galactic side uses zero cosmological input, so the agreement is a genuine galactic-versus-cosmological comparison, and (b) that the measurement now carries a two-sided falsification exposure (a slope at $3\times10^{-10}$ breaks it). We do not, and will not, upgrade "factor $\sim2$" to a precision test. If the referee wants the headline demoted from the title, that is a reasonable editorial ask and we would comply.

### R3. "The result is systematics-limited and you admit you cannot separate your two 'footings.' So what has actually been measured?"

**Conceded and central — it is the paper's own thesis, not a weakness discovered by the referee.** What is measured is a slope, $\hat a_0 = (0.84$–$1.36)\times10^{-10}\ {\rm m\,s^{-2}}$ ($\pm16$ per cent, systematics-owned), and the corresponding $\Lambda$ box. What is *not* measured is the $\sim21$ per cent distinction between the canonical ($cH_\Lambda/Z$) and alternative ($cH_0/Z$) normalisations: the coherent gas-calibration + stellar-population floor, ${\rm hypot}(s_{U,\rm coh}, s_G) = 1.04\times10^{-11}$, exceeds the $2\sigma$ splitting threshold $|\Delta|/2 = 9.75\times10^{-12}$ at *any* sample size at the current gas-mass precision. The paper's contribution is precisely to map that wall quantitatively and to show which future data (BIG-SPARC-scale clean-distance samples, $\sigma_{\ln G}\lesssim0.08$, points reaching $y\sim1$) would move it. A measurement of a systematics-limited quantity, with the floor honestly located, is a legitimate MNRAS result; it is not dressed up as more.

### R4. "The whole thing is the stellar mass-to-light ($\Upsilon_\star$) degeneracy. Swing $\Upsilon_\star$ and you can put $a_0$ wherever you like."

**True on the full sample; that is exactly why the gas cut exists.** On the full SPARC sample the $a_0$-line is an exact reframing of the RAR and inherits the RAR's $a_0$–$\Upsilon_\star$ degeneracy in full (swinging $\Upsilon_d$ over $0.5$–$0.8$ moves $\hat a_0$ by 62 per cent). The gas-dominated cut ($V_{\rm gas}^2 > \Upsilon_d V_{\rm disk}^2 + \Upsilon_b V_{\rm bul}^2$) is the whole point: it removes $\sim71$ per cent of the *absolute* $\Upsilon_\star$ swing (from $7.9$ to $2.3\times10^{-11}$), independently reproduced at 15–29 per cent residual. Further, a proper Bayesian nuisance-marginalisation shows the coherent $\Upsilon_\star$ zero-point is only *partially* degenerate with $a_0$ ($\rho \approx -0.65$ to $-0.81$, never $\to1$), because the stellar share genuinely varies with $g_{\rm bar}$; marginalising therefore *tightens* $a_0$ by 2–12 per cent. And — the honest part — even zeroing $\Upsilon_\star$ entirely leaves the footing separation below $2\sigma$, because the binding wall after $\Upsilon_\star$ is **gas-mass calibration**, not stellar $\Upsilon_\star$. So $\Upsilon_\star$ is handled and quantified, but the referee is right that a residual mass systematic dominates — it is just gas mass, not stellar mass, and the paper says so.

### R5. "Your per-point $a_0$ *declines* across the deep regime by a factor $\sim2.6$. That violates your own model's fingerprint ($\varepsilon \equiv 1$). Isn't this fatal?"

**This is the most serious internal tension and the paper flags it as such, in both directions.** The framework's own prediction is $E/g_{\rm bar} = {\rm const} = a_0$ with zero shape to leak; a genuinely declining per-point $a_0$ is a *mild violation* of that fingerprint, not a benign feature — and the manuscript labels it that way rather than hiding it. Two honest points: (i) the rival kernels (McGaugh RAR-fit, "simple") predict the per-point $\varepsilon$ *rising* across the sampled $y$, the *opposite* sign to the observed decline, so the decline matches no candidate kernel and is most plausibly an unmodelled $g_{\rm bar}$-correlated systematic (residual $\Upsilon_\star$ acting through the stellar-share–$g_{\rm bar}$ correlation at fixed fiducial $\Upsilon_d$), which is testable by tilting $\Upsilon_d$; (ii) because SPARC samples $y$ shallowly (median $y=0.31$; one point above $y=100$), the data cannot yet establish a genuine $\varepsilon \ne 1$, so it is booked as a systematic within the estimator-choice line, not relayed as a measured violation. The correct statement — which we make — is that this is a caveat that partly inflates the central $\hat a_0$ and that $y\sim1$ points are needed to resolve it. We will not claim the $\varepsilon\equiv1$ fingerprint is tested by these data; it is not.

### R6. "The 'cleaner the distances, the worse the agreement' — your TRGB subsample overshoots Planck at $+2.76\sigma$. Doesn't the best data *disfavour* your canonical value?"

**Yes, mildly, and the paper states this rather than burying it.** On the TRGB/Cepheid clean-distance subsample the central moves *up* to $\sim1.3\times10^{-10}$, inverting to $2.03\times$ Planck ($+2.76\sigma$) — so the sharpest current data lean mildly *against* the canonical footing, not onto it. This is reported in the abstract, §4.1, and §5. The mitigating (not exculpating) facts: the upward move is partly the same unmodelled $g_{\rm bar}$-correlated systematic of R5 (which inflates the central), and a weight-free OLS on the same set gives $0.89\times10^{-10}$, near canonical — so the "overshoot" is estimator-weighting-dependent and its interpretation is genuinely uncertain. The honest verdict is a straddle with a mild high-side lean, not a canonical detection and not a clean deficit. A referee who reads this as "the data mildly disfavour your preferred number" is reading it correctly, and the paper's two-sided Occam lever ($-2.45$ bans for canonical if a future clean measurement holds the high central) makes that exposure explicit.

### R7. "Squaring the velocities to form $E = g_{\rm obs}^2 - g_{\rm bar}^2$ introduces a positive noise bias. Your slope is biased high by construction."

**Acknowledged and quantified; it is small and sign-known.** $\mathbb{E}[g_{\rm obs}^2] = g_{\rm obs,true}^2 + {\rm Var}(g_{\rm obs})$, so the response $E$ carries an uncorrected positive bias of order (fractional velocity error)$^2 \approx 1$–4 per cent. The committed model-based GLS weighting cures the *weight*–noise correlation (an otherwise $\times3$ artifact) but not the *response* bias, which is carried explicitly. Its sign matters for the paper's honesty: it pushes the central *up*, i.e. it means the canonical footing is treated *conservatively* (the true $a_0$ is slightly lower, slightly closer to canonical). A future $E$-debiased or forward-modelled estimator removes it. This is a real but sub-dominant line in the budget, and it does not change the straddle verdict.

### R8. "You never test the normalisation $Z = \sqrt{32\pi/3}$. It appears on both sides of your inversion. So the 'agreement with Planck' is partly built in."

**Correct — and stated as a load-bearing caveat in §5.** Because $a_0^{\rm canon} \equiv c^2\sqrt{\Lambda_{\rm Planck}/32\pi}$ is *defined* from Planck's $\Lambda$, the predicted ratio is identically $(\hat a_0/a_0^{\rm canon})^2$; the inversion tests whether the rotation-measured $a_0$ equals the horizon value, and does **not** test $Z$, which is assumed on both sides. The paper flags this explicitly so the coincidence is not over-read, and also flags that the "large exponent" of $\Lambda$ ($\sim10^{-52}\ {\rm m}^{-2}$) is a unit-dependent dimensional statement, not a measured dynamic range. The genuinely non-trivial, non-built-in fact is only that the galactic-side $\hat a_0$ uses zero cosmological input. We claim nothing beyond that.

### R9. "Your 'Occam' Bayes factor ($+0.60$ to $+1.04$ bans) depends entirely on an arbitrary log-flat prior width. This is not evidence."

**Half-conceded; it is prior-fragile and labelled 'substantial, not decisive.'** The Occam comparison formalises *predicted-not-fitted* — that $a_0$ was fixed from $c$, $H_\Lambda$, $Z$ before the fit — rather than new data, and the paper reports the full prior/estimator envelope ($+0.30$ to $+1.38$ bans) and states plainly that a literature-informed prior conditioned on the MOND scale can drive the canonical bans toward $\sim0$. It is offered as a modest, honest bookkeeping of the zero-free-parameter nature of the prediction, on Jeffreys' "substantial" rung, explicitly *not* decisive. If the referee prefers it removed or relegated to an appendix, that is a defensible editorial call and we would not resist it; the paper does not rest on the Bayes factor.

### R10. "Independent researcher, no affiliation, MOND-adjacent framework. Why should I trust the pipeline?"

**Answered by reproducibility, not by authority.** Every load-bearing number reproduces from the frozen, read-only SPARC database via committed, exit-0 Python scripts, each carrying both footings and each re-derived by an independent verification pass with its own parser, cuts, and estimators. Three internal artifacts — an observed-weight $\times3$ fake deficit, a cross-$\Upsilon$ covariance fake $\Delta\chi^2$, and a loose error-reduction "win" forecast — were caught *in-script* and corrected rather than relayed, and are documented as such. The public `a0kit` tool reproduces the identity and the slope. The correct response to the affiliation concern is to invite the referee to run the scripts; the claims are engineered to be checkable line-by-line, and the framework's speculative superstructure (the derivation of $a_0$, the sign, a TOE) is explicitly *disclaimed* in this paper, which restricts itself to the measurement.

---

## PART 3 — SHARPENED NOVELTY STATEMENT

The interpolation kernel $\nu(y)=\sqrt{1+1/y}$ and the coincidence $a_0 \sim c\sqrt{\Lambda}$ are **not new**: the kernel is Milgrom's (1999, *Phys. Lett. A* **253**, 273, Eq. 9; original MOND, Milgrom 1983), and the proportionality of $a_0$ to the dark-energy density is Limbach, Psaltis & Özel (2008); the relativistic completion of MOND as a field theory is the domain of AeST (Skordis & Złośnik 2021), which is modified *gravity*, not the modified-*inertia* reading adopted here. What is new is (i) recasting the MOND excess as the **exact algebraic identity** $g_{\rm obs}^2 - g_{\rm bar}^2 = a_0\,g_{\rm bar}$, converting interpolation-function fitting into the measurement of a single slope; (ii) executing that slope measurement on the **gas-dominated (mass-to-light-insensitive) SPARC subsample** with a fully mapped distance/$\Upsilon_\star$/gas-calibration budget; and (iii) framing it as a **$\Lambda$-inversion** — reading the cosmological constant out of dwarf rotation curves with zero cosmological input on the galactic side, to within a factor $\sim2$ of Planck, together with an explicit systematic floor and a two-sided falsification target. The value of $a_0$, the normalisation $Z$, and the sign of the inertial correction are posited inputs, not derived; the novelty is the measurement framing and its honest floor, not the coincidence.

---

## PART 4 — CALIBRATED ABSTRACT (MNRAS-appropriate)

> The radial-acceleration relation of disc galaxies can be written as an exact identity, $E \equiv g_{\rm obs}^2 - g_{\rm bar}^2 = a_0\,g_{\rm bar}$: the "missing-gravity" excess is a straight line through the origin whose slope is the low-acceleration scale $a_0$, valid at every acceleration and following algebraically from the MOND interpolation function $\nu(y)=\sqrt{1+1/y}$ (Milgrom 1999). This converts the usual task of fitting an interpolation function into the measurement of a single slope. We measure that slope on the gas-dominated subsample of the SPARC database (Lelli, McGaugh & Schombert 2016), where the atomic-gas mass dominates the baryonic gravity and the stellar mass-to-light ($\Upsilon_\star$) degeneracy is suppressed by $\sim71$ per cent, obtaining $\hat a_0 = (0.84$–$1.36)\times10^{-10}\ {\rm m\,s^{-2}}$ ($\pm16$ per cent, systematics-limited). Inverting through $\Lambda = 32\pi\,\hat a_0^2/c^4$ recovers the *Planck* cosmological constant to within a factor of $\sim2$ (central estimates $1.08$–$2.03\times$ Planck), from galactic kinematics that carry no cosmological input — a sharpened statement of the classic $a_0 \sim c\sqrt{\Lambda}$ coincidence (Limbach, Psaltis & Özel 2008), now cast as an inversion with a mapped systematic floor. We map the two dominant systematics with reproducible pipelines: tip-of-the-red-giant-branch distances collapse the estimator-choice systematic but are not the binding wall, and external $\Upsilon_\star$ priors tighten $a_0$ by 2–12 per cent through partial self-calibration yet leave the result systematics-limited even in the perfect-$\Upsilon_\star$ limit. The true floor is gas-mass calibration, which does not average down: consequently the measured $a_0$ is a box that cannot separate two candidate normalisations of the scale ($cH_\Lambda/Z = 9.36\times10^{-11}$ versus $cH_0/Z = 1.13\times10^{-10}\ {\rm m\,s^{-2}}$, with $Z=\sqrt{32\pi/3}$) at $2\sigma$ on current data. We identify the future data that would (BIG-SPARC-scale clean-distance samples, an independent gas-mass calibration to $\sigma_{\ln G}\lesssim0.08$, and points reaching $y\sim1$), and note that a future gas-dominated slope near $3\times10^{-10}\ {\rm m\,s^{-2}}$ would break the inversion. The order-of-magnitude $\Lambda$-inversion is robust; the $\sim21$ per cent normalisation distinction is data-blocked. We treat the value of $a_0$ and the sign of the correction as posited inputs throughout.

*(Length: ~300 words. MNRAS permits abstracts up to ~250 words for the printed version; a trimmed ~230-word variant removing the sentence on future data would fit — flagged in the consolidation plan.)*

---

## PART 5 — REFORMATTING / CONSOLIDATION PLAN

### 5.1 Which source paper(s) to submit

**Submit the $a_0$-line / $\Lambda$-inversion paper alone** (Zenodo 10.5281/zenodo.21419735) as the single MNRAS manuscript. It is a self-contained galaxy-dynamics measurement and is the right scope and subject for the journal.

**Do NOT fold in the $\sigma$-spread paper** (10.5281/zenodo.21421896) as a co-equal result. Reasons: (i) it is a *prediction-and-methods* paper for a currently **underpowered, non-detectable** discriminator (public-MaNGA NO-GO at $\sim40$–$77$ carriers), whereas the $a_0$-line paper is a *measurement*; mixing them dilutes the one thing MNRAS wants (a data result). (ii) Its theorem-grade content is a field-theory statement (MG field-sector zero) that reads as modified-gravity theory, a weaker fit for a measurement-focused submission and a magnet for "speculative theory from an unaffiliated author" resistance. (iii) It rests on the covariant MI completion (its kernel/memory-time machinery), which is *posited* superstructure this submission deliberately brackets off.

**Recommended treatment of the companion:** cite it in one sentence in the Discussion as an *optional companion signature* — "an in-principle modified-gravity-impossible discriminator (the relational velocity-dispersion spread) is developed separately (Zimmerman 2026, Zenodo 10.5281/zenodo.21421896), but is not yet detectable with existing data" — and no more. This keeps the submission clean while pointing the interested referee to the forward program. If the editor explicitly invites a theory-plus-forecast companion, it could be offered as a *separate* Letter later, not merged here.

### 5.2 LaTeX class and mechanics

- **Class:** `mnras.cls` (the official MNRAS class, `\documentclass[fleqn,usenatbib]{mnras}`), with `mnras.bst` for the bibliography (Harvard/author-year, which the source already uses). Two-column MNRAS style.
- **Bibliography:** convert the existing author-year reference list to `natbib` `\citep`/`\citet`. All references already carry journal, volume, page.
- **Math:** the source is MathJax-flavoured markdown; convert `$$...$$` display blocks to `equation`/`aligned` environments. The boxed identity, the two-footing definitions, the inversion $\Lambda = 3Z^2\hat a_0^2/c^4$, and the threshold $\sigma_{\rm tot}\le|\Delta|/2$ are the equations to number.
- **Front matter:** `\title`, `\author[C. Zimmerman]{Carl Zimmerman$^{1}$}`, `\affiliation`/`$^1$Briar Creek Tech (independent researcher)`, `\date`, keywords from the MNRAS keyword list: *gravitation — dark matter — dark energy — galaxies: kinematics and dynamics — galaxies: dwarf — methods: data analysis*.

### 5.3 Length target and structure

**Target: 12–14 journal pages** (within the 10–15 pp brief; MNRAS has no hard page limit but rewards concision). Proposed section map (source → manuscript):

| MNRAS section | Source material | Notes |
|---|---|---|
| 1. Introduction | §1 (framework, two footings, the inverse question) + §1.3 (kernel credit) | Trim the framework metaphysics to ~1 paragraph; lead with the measurement question. Credit Milgrom, LPO2008, AeST early. |
| 2. The $a_0$-line identity | §2 (identity, uniqueness, $\varepsilon=1$ fingerprint) | Keep the identity and the rival-kernel table; **demote** the $\varepsilon=1$ fingerprint to "a future-data lever, data-starved today" (it is not tested here). |
| 3. Data and the gas-dominated measurement | §3 (gas cut, the box, the declining-$a_0$ caveat) | Full SPARC cuts, the $71$ per cent degeneracy kill, and §3.3 (the $g_{\rm bar}$-correlated systematic) kept in full — this is the honesty core. |
| 4. Systematic budget | §4 (TRGB lever, $\Upsilon_\star$ lever, the budget table) | Keep the budget table (Table 3 candidate). This is the section MNRAS referees will read hardest. |
| 5. The $\Lambda$-inversion | §5 (inversion, the "what is/isn't tested" box, Occam) | Keep the inversion table; consider moving the Occam Bayes factor to an appendix per R9. |
| 6. Discussion & future data | §6 + §7 | The footing fork, the BIG-SPARC/gas-calibration/$y\sim1$ roadmap, the $a_0(z)$ discriminator. |
| 7. Conclusions | §8 | The five numbered conclusions, trimmed. |
| Appendix A | Appendix A (committed scripts) | Reframe as "Data and software availability" per MNRAS policy; point to `a0kit` and the Zenodo script bundle. |

### 5.4 Figures (target: 4 main + 1 appendix)

1. **The $a_0$-line.** $E = g_{\rm obs}^2 - g_{\rm bar}^2$ vs $g_{\rm bar}$ for the gas-dominated sample, with the fitted slope and both footing lines overplotted. (Source: `fire_slope_fig.png`.) — *the paper's signature figure.*
2. **The rival-kernel fingerprint.** $\varepsilon(y)$ for framework vs McGaugh vs simple kernels, with SPARC's $y$-sampling histogram beneath to show the data-starvation. (Source: `fire_linearity_fig.png`.) — *makes the "future lever, not present test" point visually.*
3. **The systematic budget / footing straddle.** The measured $\hat a_0$ box against the two footing lines, decomposed by systematic line (the §4.3 table as a forest/error-budget plot). — *build from the budget table; shows the straddle honestly.*
4. **The $\Lambda$-inversion.** $\Lambda_{\rm pred}/\Lambda_{\rm Planck}$ for the GLS / median / TRGB estimators against Planck, with the factor-2 band. (Source: `fire_lambda_fig.png`.) — *the headline, shown with its error, not as a point.*
- **Appendix figure (optional):** the per-point $a_0$ decline across $g_{\rm bar}$ terciles (§3.3), to document the caveat visually.

### 5.5 Pre-submission checklist

- [ ] Confirm SPARC data-use acknowledgement and cite Lelli et al. (2016) as the data source.
- [ ] "Data and software availability" section pointing to the frozen SPARC subset, the committed scripts, and `a0kit` (public).
- [ ] Verify no banned-register language ("proves", "solves", "confirms", "definitive", "theory of everything") survives the markdown→LaTeX pass.
- [ ] Trim abstract to $\le250$ words for the print version (variant noted in Part 4).
- [ ] State the posited status of $a_0$, $Z$, and the sign in both the abstract and §1 (already present in source — preserve verbatim).
- [ ] ORCID and a single-line affiliation ("independent researcher, Briar Creek Tech") — no further personal detail.
- [ ] Suggested referees: galaxy-dynamics / SPARC-RAR / MOND-phenomenology specialists; note openly that the systematic budget is the part most in need of scrutiny.

---

*Package prepared for the $a_0$-line / $\Lambda$-inversion result (Zenodo 10.5281/zenodo.21419735), with the relational $\sigma$-spread (10.5281/zenodo.21421896) held back as a one-line companion cite. All numbers, the two footings, and the posited status of $a_0$/$Z$/sign are carried through from the source manuscripts unchanged.*
