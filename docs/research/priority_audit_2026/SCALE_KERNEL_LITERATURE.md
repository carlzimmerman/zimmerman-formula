# Scale and kernel literature overlap audit

Checked September 9–10, 2026 (local request cutoff September 9). Target interval: March 9–September 9, 2026, with backward searches for actual priority. This is a bounded attribution/normalization audit, not an assessment of copying, a proof of global novelty, or an endorsement of any proposed gravity theory.

## Bottom line

- The square-root vacuum-density scaling is an algebraic rewriting of the long-established MOND–cosmological-constant connection. An exact, independently derived coefficient **1/2** was **not verified** in the primary literature searched here. That is a limited negative search result, not a novelty certificate.
- All three kernel families examined below have pre-2026 antecedents, but they are **not interchangeable**. The exponential μ and exponential RAR ν are particularly easy to conflate.
- The strongest newly found in-window density-scale comparison is Christodoulou–Kazanas–Laycock: their June 22, 2026 v1 gives coefficient **1/√3**, not 1/2. Its September 8 v2 metadata/abstract were accessible; the v2 mathematical text was not verified.
- An August 2026 quantum-gravity upload reproduces the exact algebraic a0-line kernel while crediting older literature. Its own history points back to December 2024, with an independently accessible November 2025 precursor. An August upload is not automatically an August discovery.
- No evidence establishing use of Carl Zimmerman's work was found in this sub-audit. Overlap and a missing name in a bibliography do not establish either copying or independence.

## Normalization contract and exact mathematical distinctions

Here `rho_Lambda` means **mass density**, not energy density:

\[
\rho_\Lambda=\frac{\Lambda c^2}{8\pi G},\qquad
H_\Lambda=c\sqrt{\Lambda/3},\qquad
a_0=\kappa c\sqrt{G\rho_\Lambda}.
\]

Thus, by direct substitution,

\[
\frac{a_0}{cH_\Lambda}=\kappa\sqrt{\frac{3}{8\pi}}.
\]

| Convention | Equivalent κ in the density convention |
|---|---:|
| Project `a0=(1/2)c sqrt(G rho_Lambda)` | `1/2` |
| `a0=cH_Lambda/(2π)` | `sqrt(2/(3π))` |
| Thermal-subtraction `a0=2cH_Lambda` | `2sqrt(8π/3)` |
| Quantum-spin-connection `a0=c²sqrt(2Λ/λ)` | `sqrt(16π/λ)` |
| CKL v1 `〈u0〉=3a0²/G`, with `〈rho0〉=〈u0〉/c²` | `1/sqrt(3)` |

The familiar `cH0/(2π)` and `cH_Lambda/(2π)` are different outside pure de Sitter space. Also, the thermal subtraction coefficient 2 is **not κ=2** under the project's density convention.

For dimensionless accelerations `x=gobs/a0` and `y=gbar/a0`:

| Proposed relation | Exact equation in common variables | Prior source below |
|---|---|---|
| Exponential μ | `y=x(1-exp(-x))` | Zhao–Famaey |
| Exponential RAR ν | `x=y/(1-exp(-sqrt(y)))` | Milgrom–Sanders; McGaugh et al. |
| Algebraic a0-line | `x²=y²+y` | Thermal-subtraction literature |

The last row has

\[
\nu_{\rm line}(y)=\sqrt{1+1/y},\qquad
\mu_{\rm line}(x)=\frac{\sqrt{1+4x^2}-1}{2x}.
\]

In general `μ(x)ν(y)=1` only when `y=xμ(x)` and `x=yν(y)`: one cannot replace μ by the reciprocal ν at the same argument. All three share the leading deep-MOND square-root limit; that does not make their transition regions or high-acceleration residuals equal. In particular, the line has `gobs-gbar → a0/2`; the two exponential forms have vanishing residuals. Any purported common fit or derivation must identify which exact equation was used.

In units `c=ℏ=1`, defining the **unreduced** Planck mass `M_Pl=G^(-1/2)` and `M_Lambda=rho_Lambda^(1/4)` turns the project relation into `a0=M_Lambda²/(2M_Pl)`. This is an algebraic restatement, not an additional mechanism. With the reduced Planck mass `Mbar_Pl=(8πG)^(-1/2)`, its denominator is instead `2sqrt(8π) Mbar_Pl`. Searches for “gravitational seesaw” did not authenticate the exact half-coefficient as a separately derived MOND result.

## Primary-source records: established overlaps

### S1 — Milgrom: thermal-subtraction kernel

Mordehai Milgrom, *The modified dynamics as a vacuum effect*. [arXiv record](https://arxiv.org/abs/astro-ph/9805346): first May 28, 1998; checked v2 January 26, 1999. Journal: *Physics Letters A* **253**, 273–279 (1999), [DOI](https://doi.org/10.1016/S0375-9601(99)00077-8). [Full primary text](https://arxiv.org/html/astro-ph/9805346v2), §IV, equations (6)–(9).

For uniform linear acceleration in de Sitter space, the proposed excess-temperature identification gives `gN=sqrt(g²+d²)-d`, where `d=c²sqrt(Λ/3)`. Squaring gives `g²=gN²+2d gN`: the a0-line with `a0=2d`. The corresponding μ is exactly `μ_line` above.

**Classification:** known after translation of notation; algebraic line is a formal corollary. **Caveat:** the paper motivates, rather than establishes, a general dynamical mechanism. It explicitly leaves the physical identification and extension to arbitrary/circular motion unresolved; another temperature construction in the same section gives another μ. The dimensional cosmological connection does not fix the project's coefficient.

### S2 — Pikhitsa: same thermal kernel

Peter V. Pikhitsa, *MOND reveals the thermodynamics of gravity*. [arXiv record](https://arxiv.org/abs/1010.0318): first October 2, 2010; checked v3 October 21, 2010. No journal publication verified. [Full PDF](https://arxiv.org/pdf/1010.0318), equations (4)–(8), (12).

The thermal balance contains `sqrt(g²+H²)-H` in natural units, hence `a0=2H` and the same line after inversion. Its μ is written using `x=g/H`, which must be rescaled to the common `g/a0` convention. The author explicitly relates the result to Milgrom's earlier function.

**Classification:** known after translation, different proposed physical rationale; not the exact half-density coefficient.

### S3 — Klinkhamer and Kopp: minimum temperature

F.R. Klinkhamer and M. Kopp, *Entropic gravity, minimum temperature, and modified Newtonian dynamics*. [arXiv record](https://arxiv.org/abs/1104.2022): first April 11, 2011; checked v6 November 24, 2011. *Modern Physics Letters A* **26**, 2783–2791 (2011), [DOI](https://doi.org/10.1142/S021773231103711X). [Full primary text](https://arxiv.org/html/1104.2022v6), equations (4), (7a), (7b).

The scale `4πckB Tmin/ℏ`, together with the de Sitter temperature, becomes `2cH_dS`. Equation (7b) is `μ_line`. The construction is explicitly heuristic and builds on earlier equations.

**Classification:** known after translation. The numerical coefficient is different from the project's once the Planck/density/curvature conventions are aligned.

### S4 — Zhao and Famaey: exact exponential μ

HongSheng Zhao and Benoit Famaey, *Refining MOND interpolating function and TeVeS Lagrangian*. [arXiv record](https://arxiv.org/abs/astro-ph/0512425): first December 16, 2005; checked v3 January 5, 2006. *Astrophysical Journal* **638**, L9–L12 (2006), [DOI](https://doi.org/10.1086/500805). [Full primary text](https://arxiv.org/html/astro-ph/0512425v3), equation (1) and §III after equation (11).

The source explicitly discusses `μtilde(x)=1-exp(-x)`, with `x=g/a0` and `μtilde(g/a0)g=gN`. It therefore matches the project's exponential μ, not merely a similar exponential ν. The text also discusses multivalued scalar-force mappings for sharply changing functions in its TeVeS setting; this is not automatically a universal objection to every modified-gravity realization.

**Classification:** known verbatim in the checked January 2006 version. Presence in the first December 2005 version was not separately verified.

### S5 — Milgrom and Sanders: exact RAR ν as a family member

Mordehai Milgrom and Robert H. Sanders, *Rings and shells of “dark matter” as MOND artifacts*. [arXiv record](https://arxiv.org/abs/0709.2561): first September 17, 2007; checked v2 March 10, 2008. *Astrophysical Journal* **678**, 131–143 (2008), [DOI](https://doi.org/10.1086/529119). [Full PDF](https://arxiv.org/pdf/0709.2561), §2.1, equation (13).

Their family is

`νbar_α(y)=(1-exp(-y^α))^(-1/(2α))+(1-1/(2α))exp(-y^α)`.

At `α=1/2`, the second term vanishes and this is exactly `1/(1-exp(-sqrt(y)))`. They treat these as interpolation choices, not first-principles derivations.

**Classification:** known after parameter specialization. The checked version proves availability by March 2008; presence of this precise formula in v1 was not separately authenticated.

### S6 — McGaugh, Lelli, Schombert: empirical exponential RAR

Stacy McGaugh, Federico Lelli, Jim Schombert, *The Radial Acceleration Relation in Rotationally Supported Galaxies*. [arXiv record](https://arxiv.org/abs/1609.05917): September 19, 2016, v1. *Physical Review Letters* **117**, 201101 (2016), [DOI](https://doi.org/10.1103/PhysRevLett.117.201101). [Full primary text](https://arxiv.org/html/1609.05917v1), equation (4).

The fitted relation is `gobs=gbar/(1-exp(-sqrt(gbar/gdagger)))`. Identifying `gdagger=a0` gives the RAR ν above, not `μ(x)=1-exp(-x)`.

**Classification:** known verbatim; empirical use of an existing functional form. Neither the fitted value of its acceleration parameter nor the galaxy correlation establishes the project's density normalization.

### S7 — Milgrom: constant Λ versus evolving H

Mordehai Milgrom, *The a0–cosmology connection in MOND*. [arXiv record](https://arxiv.org/abs/2001.09729): January 27, 2020, v1, based on a September 2019 talk; no journal publication date verified. [Full primary text](https://arxiv.org/html/2001.09729v1), equations (2)–(3), §III.

This author's review distinguishes `aH=cH0`, `aΛ=c²sqrt(Λ/3)` and the approximate coincidence `2πa0≈aH≈aΛ`. The changing Hubble rate need not track a constant Λ. The discussion of common scales in underlying actions motivates a link without determining a universal coefficient.

**Classification:** established conceptual connection, not a derivation of κ=1/2. A time-independent acceleration versus an evolving cosmological quantity is not by itself a new 2026 distinction. A proposed specific coupling to dynamical dark energy still requires its own equation and assumptions.

## Recent candidates and their earlier source chains

### R1 — Christodoulou, Kazanas, Laycock: closest new density formula

Dimitris M. Christodoulou, Demosthenes Kazanas, Silas G.T. Laycock, *Plausible Sources of the Cosmological Constant and Associated Vacuum Properties…*. [Full primary v1 PDF](https://www.preprints.org/frontend/manuscript/6d93739261be0e369fb0b69d8cf228e9/download_pub), posted **June 22, 2026**, DOI `10.20944/preprints202606.1623.v1`. The [latest record](https://www.preprints.org/manuscript/202606.1623) changes the title to *Plausible Sources of Dark Energy…*: v2 submitted September 6, posted **September 8, 2026**, explicitly not peer reviewed.

In v1, equation (3) assumes `u0(r)=(a0²/G0)(r0/r)²`, `r0=c²/a0`. Equation (4) averages it to `〈u0〉=3a0²/G0`. Therefore `a0=c sqrt(G0〈rho0〉/3)`: coefficient **1/√3**, not 1/2. This is an assumed varying-G source profile and averaging prescription; it is not a deduction from homogeneous Λ alone. Pages 5 and 10 discuss a0 as a separate vacuum invariant.

**Classification:** partial/adjacent result with the same dimensional scaling and a distinct coefficient/mechanism. No Zimmerman text match in v1. **Limit:** only v2 metadata and abstract authenticated; do not silently apply v1 equation numbering or coefficients to v2.

### R2 — Singh: matching coefficient left free, before the window

Tejinder P. Singh, *A Relativistic MOND*. [arXiv record](https://arxiv.org/abs/2601.04290): January 7, 2026, v1, proceedings of an August 2025 conference; no journal publication date verified. [Full primary text](https://arxiv.org/html/2601.04290v1), equations (5), (13), §6–7.

Equation (5) is `a0=c²/(ξ l_dS)` with order-unity ξ fixed by matching, not derived. The discussion calls ξ numerically comparable to `2π`; it does not set an exact coefficient. Equation (13) uses `μ=x/(1+x)`, different from all three kernels audited above. The covariant completion is explicitly unfinished.

**Classification:** partial/adjacent result; the usual de Sitter scaling after translation, **not** verified agreement with κ=1/2. Calling its prediction a precise coefficient “8% away” overstates what it computes. No Zimmerman reference found in the checked bibliography.

### R3 — Kanatchikov and Kholodnyi: August upload, older kernel

Igor V. Kanatchikov and Valery A. Kholodnyi, *Effects of Quantum Spin-Connection Foam in the Solar System, Galaxies, and the Universe*. [arXiv record](https://arxiv.org/abs/2608.12404): August 11, 2026, v1. [Full primary text](https://arxiv.org/html/2608.12404v1), equations (22)–(23), (43)–(46), §6 and final publication-history note.

The transformed acceleration obeys `gN=sqrt(g²+abar²)-abar`, `g0=2abar`, yielding the exact a0-line and `μ_line`. The authors explicitly credit Milgrom, Pikhitsa and Klinkhamer for the same function. Their scale is `g0=c²sqrt(2Λ/λ)`; Weyl ordering gives `λ=3`, not the half-density coefficient. Their absolute estimate has multiple-orders-of-magnitude uncertainty before empirical calibration.

**Classification:** known after translation, in another proposed theoretical route. The paper says it was submitted as proceedings in **December 2024**, then developed in 2025 publications. That statement is an author history, not independently verified public availability in December. No Zimmerman full-text match found.

### R4 — The same authors' 2023 scale precedent

Igor V. Kanatchikov and Valery A. Kholodnyi, *The Milgromian acceleration and the cosmological constant from precanonical quantum gravity*. [arXiv record](https://arxiv.org/abs/2311.05525): **November 9, 2023**, v1. Published in *Geometric Methods in Physics XL* (Springer, 2024), pp. 393–401, as cited in the authors' later paper. [Full primary text](https://arxiv.org/html/2311.05525v1), equations (21)–(23), (32).

Equation (32) already gives `a0=2abar=sqrt(2Λ/λ)` in natural units, with `λ=3` from the stated ordering choice. The discussion acknowledges that approximation refinements may change the coefficient.

**Classification:** exact earlier precedent for this quantum-spin-connection scale relation, but only adjacent to the project's half coefficient. The verified public arXiv date precedes the requested six months by years.

### R5 — Higher moments: independently accessible November 2025 precursor

Monika E. Pietrzyk, Valery A. Kholodnyi, Igor V. Kanattšikov, Janek Kozicki, *Modifications of Newtonian dynamics from higher moments of quantum spin connection in precanonical quantum gravity*. [arXiv record](https://arxiv.org/abs/2511.15025): **November 19, 2025**, v1. [Full primary text](https://arxiv.org/html/2511.15025v1), equations (41), (56), (58). The related 2026 journal item is cited as *Modern Physics Letters A* **41**, 2541012 in R3; exact publication day was not verified here.

Equation (41) again has `μ_line`; fourth moments produce a different, more complicated kernel and acceleration normalization. Its bibliography already points to a December 2024 version of R3, and acknowledgments mention an April 2025 presentation.

**Classification:** known after translation. This accessible 2025 preprint independently prevents treating the August 2026 kernel upload as first public disclosure.

### R6 — Nash: different meanings for a0 and A0

Gary Nash, *On the physical origin of the radial acceleration relation*. [arXiv record](https://arxiv.org/abs/2608.19245): first August 14, 2026; checked v2 August 21. No journal publication verified. [Full primary text](https://arxiv.org/html/2608.19245v2), equations (1), (69), (92).

Equation (1) quotes the established exponential RAR. Crucially, this paper's `a0` is an **inverse-length metric coefficient**, while its MOND acceleration is `A0=c² a0 γ`, with γ phenomenological. A term `a0 mc²/2` in the force does not mean `A0=(1/2)c sqrt(G rho_Lambda)`. Its local gravitational energy density is also not automatically homogeneous dark-energy density.

**Classification:** partial/adjacent dark-sector and RAR proposal, not an exact scale match. No Zimmerman full-text match found.

### R7 — Hartmann, Silva, Nunes: cosmological ansatz

Gabriel Hartmann, Emanuelly Silva, Rafael C. Nunes, *Testing MOND-like modifications to gravity using growth-rate measurements and one-loop corrections to the matter power spectrum*. [arXiv record](https://arxiv.org/abs/2608.18229): August 18, 2026, v1. No journal publication verified. [Full primary text](https://arxiv.org/html/2608.18229v1), equations (35)–(36) and surrounding construction.

The study employs a power-law generalized Poisson response and phenomenological external scale `g0(z)=cH(z)`, then parametrizes `a0/g0(z)` by `(H0/H(z))^m`. This is a stated modeling ansatz for cosmological perturbations, not a computed half-density coefficient or one of the three exact kernels here.

**Classification:** partial/adjacent cosmological MOND phenomenology. Equations involving an evolving Hubble background should not be reported as identical to a fixed-Λ hypothesis.

### R8 — Scholz: a 2026 journal date, 2025 first preprint

Erhard Scholz, *Bridging the gap between dark matter and MOND by a relativistc scalar field approach*. [Publisher full text](https://link.springer.com/article/10.1140/epjc/s10052-026-16091-3), *European Physical Journal C* **86**, 857 (2026): received January 21, accepted July 4, **published July 23, 2026**. [arXiv record](https://arxiv.org/abs/2510.17704): first **October 20, 2025**, later v3 June 23, 2026; [v1 full text](https://arxiv.org/html/2510.17704v1) has a different title.

The publisher text chooses a scalar scale at the geometric mean of a Milgrom energy and a reduced Planck energy, discussing normalization freedom. This is a relevant seesaw-like scale hierarchy, but not verification of the project's exact coefficient or vacuum-density identity.

**Classification:** partial/adjacent within this sub-audit. Detailed action/phenomenology comparison is delegated to the broader audit. The journal publication is July, not August, and the first preprint is outside the six-month window.

## Corrections suggested by the source check (no physics files changed)

1. Qualify the local README's description of Milgrom (1999): exact kernel overlap is established, but the source does not complete a general physical derivation for galaxy orbits.
2. Express every scale coefficient in one common density convention. In particular, `a0=2cH_Lambda` does not have κ=2.
3. Do not describe Singh (2026) as computing a fixed coefficient about 8% different: ξ remains a matching parameter. The precise `1/(2π)` comparison is a separate conventional benchmark.
4. Keep μ-exponential, ν-exponential RAR, and the a0-line as three separately named hypotheses when documenting derivations and fits.
5. Treat a fitted κ near one half as a numerical/model-comparison result until an independent derivation and its assumptions are supplied. Merely rewriting it with Λ or Planck masses does not add independent evidence.

## Search scope, provenance and open limits

The literature-check skill governed primary-source authentication, common-normalization translation, and bounded overlap labels. Local README was inspected for the project's contracts. Remote primary HTML/PDF was read for the records above; no licensed/private material was uploaded. No source copies were retained locally, so cache SHA-256 and cached extraction are **not requested/not available**; stable primary locators and checked versions are recorded instead. Only this audit report was written.

Discovery used the web search index, followed by arXiv/publisher/preprint primary texts. The parent conducted a second, independent search, including a SciSpace index and additional literature domains; this sub-audit alone is not a fully independent second-index survey. Searches were English, principally astrophysics/gravity, through the request cutoff. Representative literal queries:

- `MOND 2026 dark energy acceleration`, with `site:arxiv.org/abs` variants;
- `"MOND" "32π"`, `"MOND" "32 pi"`, `"a_0" "sqrt" "32" "Lambda" MOND`;
- `"MOND" "gravitational seesaw"`, `"MOND" "seesaw" scale dark energy`;
- `"MOND" "1-exp(-x)"`, `"MOND" "exp(-x)" interpolating`;
- `"MOND" "vacuum density"`, `"MOND" "sqrt" "rho" "1/2"`, `"sqrt(G" "rho" "MOND" "0.5"`;
- `"Zimmerman" "acceleration" cosmological constant`, `"Zimmerman" "MOND" -site:github.com -site:reddit.com`, `"Carl Zimmerman" physics -site:github.com`.

Backward chains followed: 2026 spin-connection paper → 2023/2025 predecessors and Milgrom/Pikhitsa/Klinkhamer; RAR → Milgrom–Sanders family; exponential μ → Zhao–Famaey; cosmological connection → Milgrom's own historical discussion. Forward coverage was search-index driven, not a complete citation-database export. Full-text name searches were negative in Singh's checked bibliography and in Nash, the August spin-connection paper and CKL v1; these are bounded text-search results, not proof that no source was consulted.

Additional discovery-only leads not used to establish exact overlap: Michael Aaron Cody, *Cosmological Origin of MOND Acceleration Scale*, Zenodo 18343518 (January 2026 metadata); Markus Stone, *The Modal-Horizon Framework I*, [Zenodo 20351633](https://zenodo.org/records/20351633) (May 2026 version, inaccessible PDF in this pass); Remi Cornwall, *A Gravitating Dark-Energy Hypothesis to Replace MOND*, [March 2026 preprint](https://www.preprints.org/manuscript/202603.0800). These do not supply a verified half coefficient here.

Important gaps: CKL v2 equations; exact first-version content of the 2005/2007 kernel preprints; exhaustive 2026 coverage, especially late-August/September indexing delays; non-English and non-indexed work; inaccessible source files; independent verification of privately submitted proceedings; and Carl's own public-disclosure dates, which require separate timestamp evidence. No allegation about appropriation is supported by this report.
