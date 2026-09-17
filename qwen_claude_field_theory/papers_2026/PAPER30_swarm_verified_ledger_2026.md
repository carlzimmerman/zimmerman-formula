---
title: "What Survives Independent Verification: The Machine-Checked Identities, Reproduced Measurements and No-Go Results of a 440-Commit AI Agent-Swarm Campaign on the Equilibrium Reading of the Radial Acceleration Relation"
author: "Carl P. Zimmerman (Briar Creek Tech) — AI-assisted research programme; not peer reviewed"
date: "2026-09-16 (v1)"
geometry: margin=1in
mainfont: "STIX Two Text"
fontsize: 11pt
---

**Summary.** Between 2026-09-13 and 2026-09-16 five AI agent tracks committed roughly 440 lanes to a shared repository on the "equilibrium reading" of the radial acceleration relation (RAR), a reading in which a cold dark sector equilibrates at the virial temperature $\sigma^2 = \tfrac12\sqrt{G M_b a_0}$ in every baryonic well and its isothermal density is the deep-MOND phantom. The campaign ended with a capstone declaring a complete derivation chain from one input to a derived particle mass, "180 theorems / 22 certificates", and "the loop is closed". This paper records what in that campaign survives verification by a separate track that re-ran every cited script, recompiled every Lean file, and read the FAIL lines. Three classes survive. (i) A machine-checked formalisation: 71 of 73 Lean 4 certificate files compile on the standard axioms (848 theorem declarations), certifying the algebra of the deep-MOND/isothermal chain — the equilibrated density equals the phantom with coefficient one, the enclosed dark mass is $M_b\,r/r_M$, the deep relation $g^2 = a_0 g_N$, the Tully–Fisher quartic — as identities of the definitions, never as dynamics. (ii) Reproduced measurements whose honest readings differ from their labels: the $v^4 = G M_b a_0$ line across twelve decades has pooled slope $1.004 \pm 0.011$ but a slope-fixed zero point $1.81\times a_0$ ($+8.98\sigma$) with channels from $0.66\times$ to $12.2\times$; the zero-parameter cluster temperature relation has a within-sample scatter of 0.053 dex and an unnormalised amplitude $2.1\times$ under the data; the HeCS velocity anisotropy $\beta(2\text{–}5R_{500}) = 0.434 \pm 0.015$ fails the registered rule and equals the cold-dark-matter expectation. (iii) Verified no-go results that are new because the constructions are new: the frozen-scalar action $L = \Lambda^4 f(K)$ with $f' = \mu_2$ has $P_X < 0$ on the branch it uses and no ground state; the postulated temperature is neither an attractor nor an equilibrium of Newtonian dust; the acceleration distribution of the dark mass is not the Lomax law the kernel was said to encode; no phantom/dust partition closes the cluster amplitude; the committed kernel puts $0.489\,M_b$ inside $r_M$ where the certified equipartition says $1.000$; the "derived" carrier mass $5.09 \pm 0.10$ keV is a 5-keV anchor returned by the inversion of its own definition and sits $6.3\sigma$ below the Lyman-$\alpha$ floor the campaign cites. No positive novel physical result survives. This document does not state that a theory is closed.

# 1. Scope and protocol

The campaign under review is the set of commits to the repository between 2026-09-13 and 2026-09-16 by the tracks named `deepseek_push` (the Z, S, A, B, C and D waves and the capstone documents), `project_atomos`, `hy4_push`, `glm53_push`, `qwen38_push` and `deepseek_moa`. Its terminal documents are `THE_COMPLETE_THEORY.md` (lane C09), `D07_derivation_ledger.py`, `WAVEBOARD.md` revision 32, `MNRAS_ABSTRACT.md`, `MNRAS_METHODS.md` and `MNRAS_PARTICLE_SECTION.md`. The previous status report of this programme (PAPER29, DOI 10.5281/zenodo.22753165, versions 2 and 3 carrying the audits L258 and L260) labelled the reading's chain rung by rung; the campaign reviewed here post-dates it.

"Independently verified" means, throughout: (a) the claim has a committed script in the originating track; (b) that script was re-run by the auditing track (`fable_independent_2026`, lanes L258, L260, L261 and the companion of this paper, L262) with the outputs compared to the committed ones; (c) every check whose pass condition is the literal `True`, or a comparison of a number to itself, was discounted; (d) every number quoted below was re-read from the committed output or results register, not from a commit message; (e) both registered footings of the acceleration scale ($9.3619\times10^{-11}$ and $1.1279\times10^{-10}$ m s$^{-2}$) were carried wherever a dimensional number appears. The verification lane L261 (`fable_independent_2026/L261_wave32_audit.py`) passes 3 of its 37 checks; every failure is a finding and is reported here. Lean files were compiled with `lake env lean` against the repository's Mathlib build (Lean 4.34.0-rc2), with `#print axioms` appended for every theorem (`L261_lean_inventory.py`).

# 2. What the machine-checked certificates certify

**The inventory.** 73 Lean files from the agent tracks and the programme's own library were recompiled: 848 theorem and lemma declarations; 71 files exit 0; every theorem in a compiling file depends only on `propext`, `Classical.choice` and `Quot.sound`. The capstone's count "180 theorems / 22 certificates" reproduces arithmetically from the 22 files it names (126 in the 16-file base ledger plus 54 in the C-wave). Two files fail: `gemini38_flash_push/UnifiedGravitationalTheoryProof.lean` (16 errors; five theorems rest on `sorryAx`; still tracked, no longer counted, not mentioned) and `qwen38_push/lean/Q005_btfr_zero_point.lean`, whose commit message claims "exit 0, zero sorry" and whose three `#eval` checks evaluate to `false`.

**The statements.** Every certified statement is algebra of the static problem. The spine is the chain

$$\sigma^2 = \tfrac12\sqrt{G M_b a_0}
\;\Rightarrow\;
\rho = \frac{\sigma^2}{2\pi G r^2} = \frac{\sqrt{G M_b a_0}}{4\pi G r^2}
\;\Rightarrow\;
M_{\rm ph}(<r) = \frac{M_b\, r}{r_M},\quad r_M = \sqrt{\frac{G M_b}{a_0}},$$

$$M_{\rm ph}(<r) = \frac{M_b\, r}{r_M}
\;\Rightarrow\;
g^2 = a_0 g_N
\;\Rightarrow\;
v^4 = G M_b a_0,$$

which is the statement that a singular isothermal sphere whose dispersion is half the flat-curve velocity squared is the deep-MOND phantom (Milgrom 1983). The certificates named `equilibrated_is_phantom`, `equipartition_linear_law`, `deep_rar` and `btfr_quartic` prove exactly these implications from the first equation taken as a definition; `sigma_virial_half` proves $(x/2)/x = \tfrac12$ from the definition $\sigma^2 := \sqrt{G M_b a_0}/2$. The C-wave adds substitution identities (C04: $T = \mu m_p \sigma^2/k_B$ with $\sigma^2$ substituted), mutual inverses (C02: `ladder(freeze(m)) = m`; C04: `inversion_identity`, `inversion_dual`), square-root algebra (C05), decimal interval checks (C08) and, in C06, the theorem `closure_iff_zSq`: given $a_0 := c^2/(Z R_{dS})$ and $R_{dS} := c/(H_0\sqrt{\Omega_\Lambda})$, the map $\Omega \mapsto 32\pi a_0^2/(3H_0^2c^2)$ is the identity on every $\Omega$ if and only if $Z^2 = 32\pi/3$. One theorem in that file is named `tautological_fixed_point`. The two "entrance" certificates the capstone registers for the temperature (`virial_rung4`, `maxentropy_phantom`) exist in no file.

**What is new here.** To our knowledge this is the first Lean 4/Mathlib formalisation of the deep-MOND phantom, equipartition, deep-RAR and Tully–Fisher identities. It is a formal artifact, not a physical result: none of the 848 theorems certifies that a sector equilibrates, that the temperature takes the stated value, or that the acceleration scale is the de Sitter surface gravity.

# 3. Reproduced measurements, with their readings

All scripts in this section re-run bit-for-bit against their committed outputs. The readings below are what the outputs say.

## 3.1 The twelve-decade line

The campaign compiles 542 objects over $\log_{10} M_b = 2.63$–$14.35$ (SPARC rotators, HI dwarfs, ATLAS3D early-types, GEMS groups, dwarf spheroidals, X-COP clusters, globular clusters) on $v^4 = G M_b a_0$, with pressure-supported systems entered through $v = \sqrt{2}\,\sigma$ (the reading's own $\kappa = \tfrac12$, fixed, no per-channel factor). The pooled free slope is $b = 1.004 \pm 0.011$ (rms about the identity 0.180 dex). With the slope fixed at unity the zero point on all 542 is $a_{0,\rm line} = 1.814 \times a_{0,\rm DE}$, i.e. $+0.2585 \pm 0.0288$ dex, $z = +8.98$ (Z08). The per-channel zero points, in units of $a_{0,\rm DE}$:

| Channel | $n$ | $a_0/a_{0,\rm DE}$ | $z$ |
|---|---|---|---|
| SPARC | 35 | 0.663 | $-3.41$ |
| HI dwarfs | 55 | 1.194 | $+0.95$ |
| ATLAS3D | 258 | 2.020 | $+14.37$ |
| GEMS groups | 36 | 1.326 | $+0.78$ |
| dSph | 34 | 7.378 | $+5.00$ |
| X-COP clusters | 12 | 12.164 | $+42.21$ |
| Globular clusters | 112 | 1.401 | $+1.69$ |

The channels span 1.26 dex. Restricted to the domain the reading calls its own ($z^* > 0$, $n = 323$) the slope is $1.155 \pm 0.029$ ($+5.35\sigma$ from unity); with a free zero point per catalogue it is $1.298 \pm 0.056$ (Z01). Removing the ATLAS3D channel leaves the line at $1.644 \times a_{0,\rm DE}$ (S09). The subset that closes at the horizon value ($n = 104$, $z = -0.20$) is the SPARC channel at $-3.41\sigma$ cancelling the HI channel at $+0.95\sigma$ inside a channel set selected for agreement with the line. The reading: the $a_0$-normalised line is not universal across channels; the cluster and dSph offsets are the known MOND cluster and dwarf discrepancies.

## 3.2 The cluster temperature relation

$T = \mu m_p \sqrt{G M_b a_0}/(2 k_B)$ is the isothermal-halo temperature of the phantom; $T \propto M_b^{1/2}$ for clusters is Sanders' (1994, 1999) MOND relation. On the committed sample of 50 objects (X-COP 12, HeCS 12, E11 groups 26; three instruments) the ratio $T_{\rm pred}/T_{\rm obs}$ has sample medians 0.560, 0.721 and 0.433, pooled 0.475: the zero-parameter relation under-predicts by $2.1\times$ (0.32 dex) with no free normalisation. The quoted "0.053 dex MAD" is the scatter after each sample's own mean is removed (B06 lines 292–303 of the script), and the lane's headline verdict conditions on scatter only. The quantity "$f = 5.66$" that the capstone calls a content ratio is $M_{500}/M_b$, the cluster missing mass. The reading: the MOND cluster residual, intact, on a modern sample.

## 3.3 The HeCS velocity anisotropy

From 9,949 members of 58 HeCS clusters, the projected-Jeans window mean is $\beta(2\text{–}5R_{500}) = 0.434 \pm 0.015$ (G203); a two-dimensional phase-space fit gives 0.495 (G206); the free-form radial profile has $\beta(0.5\text{–}1R_{500}) = -0.37 \pm 0.14$ rising outward (G209, estimator E2). The rule registered before the data (G170, "detected when $\beta(2\text{–}5R_{500}) > 0.5$ at $\geq 3\sigma$") fails at $-4.5\sigma$; the lane records "[FAIL] C6". The measured value is the standard N-body expectation for an NFW halo of the fitted concentration (Hansen & Moore 2006, $\beta \approx 0.40$ at these radii); no lane compares to it. The "static null $\beta = 0$, dead at 29.7$\sigma$" is not a prediction any model makes. The reading: a reproduced measurement whose methodology (interloper treatment, stacking, projection) this verification did not independently validate, and whose value is the cold-dark-matter one.

## 3.4 The cluster residual fit

$c_{\rm dust} = 0.72\,(M_{500}/8\times10^{14})^{-0.414}\,(r/R_{500})^{-0.990}$ is an ordinary-least-squares fit of three parameters to 96 bins (12 X-COP clusters $\times$ 8 radii) with residual 0.119 dex (G122). The value $q = -1/3$ presented as derived (0.52$\sigma$ from $-0.414 \pm 0.157$) never enters the law; the D03 inversion uses the fitted $-0.4144$. The dust amount "remains an input" (G110). The reading: a description of the Ettori et al. (2019) hydrostatic masses, not a prediction of them.

## 3.5 The outer envelope slope

The common weighted mean $-2.404 \pm 0.078$ (G184) is "$7.7\sigma$ from NFW's $-3$" only against the $r \gg r_s$ asymptote; the same output records the committed NFW fits at 1–2 $R_{500}$ running $-2.0$ to $-2.75$, and the three "instruments" averaged include the campaign's own tSZ forecast ($-2.37 \pm 0.09$). The X-ray measurements alone are within $1\sigma$ of the window-matched NFW slope (hy4 D036: $+0.03 \pm 0.07$).

# 4. Verified no-go results

These are the campaign's substantive content. They are new because the constructions they kill are new, and each is a committed, re-run script with FAIL lines.

## 4.1 The frozen-scalar action has no ground state (hy4 H045, H053; deepseek G204)

The reading's relativistic completion is GR plus one shift-symmetric scalar with $L = \Lambda^4 f(K)$, $f'(K) = \mu_2(\sqrt K)$, $\mu_2(x) = 1 - (1 + x/2)^{-2}$. In the k-essence variable $X$ on the static branch, $P_X = -f'(K) = -\mu_2 < 0$ for every $K > 0$: wrong-sign gradient energy, and the static energy density is unbounded below as $K \to \infty$. The crossing $u^* = 1.2239$ is exceeded by twelve orders of magnitude at the solar surface. H053 shows no higher-derivative term screens it (the Hessian is indefinite at every finite coefficient, IR-dominated); deepseek's G204 confirms "$P_X = -\mu_2 < 0$ is identically unchanged" across the $k^4$ family, and its latest lane (E02) records "the framework is effective, not fundamental". The capstone and abstract nonetheless present "one scalar field carrying our gravity" and "Section 2 states the action".

## 4.2 The temperature is neither an attractor nor an equilibrium (glm53 G035)

Newtonian N-body runs of dust in a baryonic well: material at $\sigma^2 = G M_b/(2 r_M)$ in an $r^{-2}$ shell is unbound (escape fraction 0.37–0.51 by 100 crossing times, $r_{50}$ expanding to 4.9–10.4 $r_M$, $\sigma^2$ cooling to 0.32 of target); no initial condition converges to the target; both registered kill patterns fired. The lane's verdict: "the temperature must be POSTULATED". Deepseek's G081 records "G035's KILL stands"; the rebuttal registered against it (G111, a relaxation N-body with a scalar mediator) is a specification that has not been run. The capstone's "derived by five routes" cites G084 (which inputs $\sigma^2 = C/2$ and outputs the $r^{-2}$ exponent) and G091 (which inputs $\rho = A/r^2$ and states it is "the same statement as hydrostatic balance"); every route contains the conclusion as a premise, as L258 showed for the first three.

## 4.3 The acceleration distribution is not Lomax; the kernel is not derived (deepseek G230; G228; hy4 H055, H060; N1)

The observation that $1 - \mu_2$ is the survival function of a Lomax (Pareto II) distribution with shape 2 is true of every interpolating function (any monotone $\mu: [0,\infty) \to [0,1)$ is a distribution function; the "simple" $x/(1+x)$ is Lomax with shape 1). The maximum-entropy "derivation" is the textbook fact that a log-moment constraint $\langle \ln(1+u) \rangle = c$ yields the Lomax density, with $c = \tfrac12$ and the scale inserted by hand; the lane itself calls $c$ "CALIBRATED", its three verdict checks are literal `True`, and the sibling lane N1's independent selection gives shape 1.85, window-dependent between 1.05 and 18. The exponent 2 is the coefficient $\kappa = \tfrac12$ under another name ($n = s/a_0$). The direct test: the measured $dM/dg$ of the dark mass has index $+3.47 \pm 0.20$ pooled against the predicted $-2$ ($z = +7.28$), Kolmogorov–Smirnov $p = 0.000$ on SPARC and pooled; G230 passes 1 of 5. The "shape lock" $\gamma = (2+n)/n$ is false: the deep limit of $\mu_n$ gives $g \propto r^{-1}$, hence $\gamma = 2$, for every $n$.

## 4.4 No partition closes the cluster amplitude (glm53 G059, G050)

The kernel's sub-$a_0$ branch supplies 0.57 (canonical) / 0.61 (alternative footing) of the hydrostatic deficit at 420 kpc against the 0.76 the measured band requires; no non-degenerate candidate reaches $[0.8, 1.3]$ of $M_{\rm HSE}$; "supported phantom + free dust account for $M_{\rm HSE}$ by construction" (1 of 7 checks). The "zero-parameter dust law" of §3.4 is that free-dust share, fitted.

## 4.5 A factor two at the one boundary

The reading's single radius $r_M$ is where the baryonic acceleration equals $a_0$. There, the committed kernel $g\,\mu_2(g/2a_0) = g_N$ gives $g/g_N = 1.489$, i.e. $M_{\rm dark}(<r_M) = 0.489\,M_b$ and a mean dark column $a_0/(2\pi G) = 106.9\ M_\odot\,{\rm pc}^{-2}$; the certified equipartition (§2) says $M_{\rm ph}(<r_M) = M_b$ exactly and $a_0/(\pi G) = 213.7$. The campaign carries both: 106.88 in the capstone's Link 1 and 213.74 as "new and owned" in the abstract. hy4 H037 had retracted the 213.7 lemma on 163 SPARC galaxies (measured $81\ M_\odot\,{\rm pc}^{-2}$, $-0.42$ dex, and $M_b$-dependent at $+0.265 \pm 0.038$ dex/dex, $7.0\sigma$ against the universality the lemma asserts) — which is precisely the kill the campaign's own falsifier registry (G237) names and never scores.

## 4.6 The carrier mass is an anchor returned (deepseek G132, G163, G168, G212, G213; atomos B03; Lean C02)

The ladder $m = k_B T_0 (1+z^*)/\sigma^2$ needs a freeze redshift. In every lane $z^*$ is computed as $T_b(m = 5\ {\rm keV})/T_{\rm CMB,0} - 1$ (G132 `M_5KEV`; G163 `M_KEV_REF = 5.0`); G168's header states "z* is DEFINED by $T_b(m = 5\ {\rm keV}) = T_{\rm CMB}$". The band $z^* \in [2.3656, 2.4932]$ is the 5-keV anchor at the two dispersion footings (121.44 and 119.21 km s$^{-1}$), and the "cosmic-noon window" $[5.0, 5.19]$ keV is $5 \times (121.44/119.21)^2$, the footing mismatch, not an uncertainty. "Environment-blindness" (B03; Lean C02) is $f(g(x)) = x$ for mutually inverse formulas, which the Lean file states in its own header. The "three independent lines" of G212 are: the ladder; the Lyman-$\alpha$ forest, whose published *lower* bounds ($m_{\rm WDM} > 3.3$, $> 5.3$, $> 5.7$ keV; Viel et al. 2013, Iršič et al. 2017, Villaseñor et al. 2024, as the campaign's own G093 lists them) are entered as a two-sided window $[3.3, 5.7]$; and the same bounds through $\lambda_{\rm fs}(m)$. All nine G212 checks are `check(True, ...)`. Read as bounds, the record floor excludes $m = 5.089 \pm 0.097$ keV at $6.3\sigma$ (Iršič et al. 2017's 5.3 keV at $2.2\sigma$); the campaign's own forest Gaussian puts 97.7% of its mass in the excluded region. No measured redshift evolution supports $z^* = 2.4$ (G080: null trend to $z = 1.68$; G163: "storying, not a derivation"), and the one direct $a_0(z)$ measurement in the repository (MUSE, rising; lane L143) is cited in no campaign file. The 2.55-keV line, its width, its $1/b$ cusp and the 0.558-Mpc cut are closed forms of this number.

## 4.7 The dark-energy closure is the identity (L258, L260; Lean C06)

$a_0 = \tfrac12 c\sqrt{G\rho_\Lambda} \equiv c\,H_0\sqrt{\Omega_\Lambda}/Z \equiv c^2/(Z R_{dS})$ with $Z = 2\sqrt{8\pi/3}$; each form is the coefficient one-half restated. $\Omega_\Lambda = 32\pi a_0^2/(3H_0^2c^2)$ returns its input for every $\Omega_\Lambda$ (C06 proves this); a galactic $a_0$ ($1.20$–$1.25\times10^{-10}$) returns $\Omega_\Lambda = 1.13$–$1.21$. The campaign's own inventory (G152, 01:04 on 09-16) lists the closure as circular; documents written later the same day (`THEORY_CLOSURE`, the capstone §4.3, `MNRAS_METHODS`, the README) print "$\Omega_\Lambda = 0.685$ from $a_0$ alone (G058, Lean)". The "density-closed cosmology, equilibrium + dust = 1.000 of $\Omega_{\rm dm}$" is coded as $\Omega_{\rm dust} := \Omega_{\rm dm}({\rm Planck}) - \Omega_{\rm phantom}$ (G198).

## 4.8 The force face is a splice

The Cassini null is called "architectural" because the sector is ordinary matter with $p = 0$ and no field force (G086, S08); the RAR and the ontology are carried by the sourced field equation $\nabla\!\cdot[f'(K)\nabla\phi] = 4\pi G\rho_b$ whose Gauss-map charge the phantom is said to be (G234). The first has no field for the phantom to be the charge of and is, by S08's own words, "observationally degenerate with GR + CDM"; the second inherits the external-field quadrupole of the $\mu_2$ equation, $6.44\times$ (canonical) / $7.63\times$ (alternative) the Cassini ceiling (L243). L258 found this splice across two tracks; it is now inside one.

## 4.9 The registered rules

The anisotropy rule failed (§3.3). The thermal-SZ pass window registered in the proposal, sample-median slope in $(-1.7, -0.9)$, was rewritten nine hours before the map was fetched to $(-2.94, -2.14)$, so that the original kill line ($-2$) sits inside the pass band; the advertised "47.8$\sigma$" is a forecast on synthetic truth; the first real cluster scored (A85, slope $-3.246$ against predicted $-2.596$) sits in the campaign's own "NEITHER" branch at forecast errors. The falsifier matrix that reports "zero unexplained fires" does not contain the $+5.35\sigma$ frozen-domain tilt, the $-4.4\sigma$ window rule, the $+8.98\sigma$ full-sample zero point, the $7\sigma$ surface-density mass dependence, the cluster break failure (D036, G160: $\Delta\chi^2 = 24.6$ median) or the escalated RAR sag (G049). The Gaia DR4 pre-registration and its hash files were not modified by the campaign (no commit since 09-13 touches them); a separate deepseek-internal decision rule for its wide-binary ridge was re-stated pre-data (Z03) in the open.

# 5. The headline claims that do not survive

| Claim in the terminal documents | What the record shows | Verdict |
|---|---|---|
| "The ONE input: $a_0 = c^2/(Z R_{dS})$, identity-pinned, ratio 1.00005" | The same $\kappa = \tfrac12$ postulate; 1.00005 is the rounding of $9.3619\times10^{-11}$ | Relabel |
| "$\sigma^2 = \sqrt{G M_b a_0}/2$ derived by five routes" | Every route inputs $\sigma^2 = C/2$ or $\rho \propto r^{-2}$; G035 kills the dynamics; entrance certificates absent | Not derived |
| "$\Omega_\Lambda = 0.685$ from $a_0$ alone (Lean)" | The identity, ruled circular by the campaign's own G152 that morning | Circular |
| "Twelve-decade line at the ONE scale" | $1.81\times a_0$ at $+8.98\sigma$; channels 0.66–12.2$\times$; frozen tilt $+5.35\sigma$ | Fails at the ends |
| "Zero-parameter $T_{\rm X}$ law at 0.053 dex on 50 objects" | Amplitude $2.1\times$ under; scatter after per-sample mean removal | Sanders' residual |
| "$m = 5.09 \pm 0.10$ keV, three independent lines, environment-blind" | A 5-keV anchor inverted; forest floor excludes it at $6.3\sigma$; all checks literal-True | Not derived |
| "The 2.55-keV line, the 0.558-Mpc cut" | Closed forms of the above | Inherits |
| "Cluster sector in closed form, zero-parameter dust law" | 3-parameter OLS fit to the same 12 clusters; dust amount an input; G059 1/7 | Fitted |
| "Outer slope $7.7\sigma$ from NFW" | Against the asymptote; NFW in-window $-2.0$ to $-2.75$ brackets it | Straw man |
| "Anisotropy $\beta$ 0.03 $\to$ 0.56 measured, static null dead at 31$\sigma$" | Registered rule ($> 0.5$) failed at $-4.5\sigma$; value is the NFW one | Failed rule |
| "PPN = GR, Cassini null architectural, one scalar" | No-field reading vs sourced-field reading spliced; the action has no ground state | Splice |
| "180 theorems / 22 certificates" | Count reproduces; content is algebra of definitions; two sibling files fail | Algebra |
| "Zero unexplained falsifier fires" | Six registered $> 3\sigma$ departures outside the matrix | Incomplete |
| "The loop is closed" | The capstone's own final verdict: "not closed as a theory" | Contradicted |

# 6. What is novel, stated plainly

Two constructions in the campaign are, to our knowledge, not in the literature: defining a dark-particle mass by the redshift at which $m\sigma^2/k_B$ equals the CMB temperature, and fitting the cluster residual as a power law in $(M_{500}, r/R_{500})$. The first rests on an anchor and is excluded by the forest bound it cites; the second re-describes hydrostatic masses with fitted parameters. Everything else in the chain is Milgrom's deep-MOND phenomenology, McGaugh's baryonic Tully–Fisher relation, Sanders' cluster temperature relation with its residual, the isothermal-sphere identity, the two-body decay line at $E = m/2$ and the isothermal $\sqrt 2$. The campaign's genuinely new and verifiable products are the formal artifact of §2 and the no-go results of §4, which close, for this specific reading, the frozen-scalar action, the dynamical origin of its temperature, the distributional reading of its kernel, the partition of its cluster sector, the consistency of its one boundary, and the derivation of its carrier mass. No positive novel physical result survives its own record.

# 7. Reproducibility

Every number in this paper is read from a committed file by `fable_independent_2026/L262_paper30_ledger.py`, which prints the tables of §3 and the numbers of §4 from the registers (`Z08_line_zero.out`, `Z01_frozen_tilt.out`, `S09_one_scale.out`, `B06_txray_law.out`, `G203_hecs_commission.out`, `G209_beta_profile.out`, `G122_coherency_decomp.out`, `G184_knee_discriminator.out`, `H045_results.out`, `G035_results.md`, `G230_dmdg_measure.out`, `G059_partition_function.out`, `H033_P1_results.json`, `G212_mass_triangle.out`, `L261_results.json`, `L261_lean_inventory.json`) and fails if any quoted value has drifted. The verification lanes are `L258_closure_audit.py` (2/11), `L260_seesaw_identity_audit.py` (0/5), `L261_wave32_audit.py` (3/37) and `L261_lean_inventory.py`; the repository state audited is commit `2954698c4` and its ancestors. Lean certificates recompile with `cd fable_independent_2026/lean_2026 && lake env lean <file>`.

# References

Eckert, D. et al. 2019, A&A 621, A40 (X-COP). Ettori, S. et al. 2019, A&A 621, A39. Famaey, B. & McGaugh, S. 2012, Living Rev. Relativ. 15, 10. Hansen, S. H. & Moore, B. 2006, New Astron. 11, 333. Iršič, V. et al. 2017, PRD 96, 023522. Lelli, F., McGaugh, S. & Schombert, J. 2016, AJ 152, 157 (SPARC). McGaugh, S. 2012, AJ 143, 40. Milgrom, M. 1983, ApJ 270, 365. Rines, K. et al. 2013, ApJ 767, 15 (HeCS). Sanders, R. H. 1994, A&A 284, L31; 1999, ApJ 512, L23. Viel, M. et al. 2013, PRD 88, 043502. Villaseñor, B. et al. 2024, as cited by the campaign's lane G093. Zimmerman, C. P. 2026, PAPER29, DOI 10.5281/zenodo.22753165 (concept; v2 22772710, v3 22776494).
