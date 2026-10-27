# Priority and overlap review: Zimmerman's gravity programme

**Cutoff:** 9 September 2026. **Review conducted:** 9–10 September 2026.
**Repository snapshot:** `25ebacace` plus the existing working tree; pre-existing changes were preserved.

**Scope clarification from Carl during the review:** his exact original normalization \(Z=2\sqrt{8\pi/3}\), its density interpretations, and the project-specific results still in use are the priority targets. Start with [CORE_AND_LIVE_CLAIMS.md](CORE_AND_LIVE_CLAIMS.md). The older-ingredient survey below is context, not a substitute for checking those exact claims.

## Bottom line

**No evidence of copying or appropriation was established in this review. This is not a guarantee that none occurred.** What the evidence does establish is substantial older prior art, several close contemporary research directions, and some narrow project-specific claims whose priority remains unresolved.

The most important correction is to separate three questions:

1. **Did Carl independently develop and record this idea?** The repository often provides useful evidence of that development, including unsuccessful attempts and corrections.
2. **Was the mathematical or physical idea new to the literature?** Several central ingredients demonstrably were not.
3. **Did another author use Carl's work without acknowledgment?** No such causal chain was established. Similarity, chronology, absent citations and download counts do not, individually, settle this question.

This review covers the main claim families identified in the supplied equations and selected repository papers. It is **not a line-by-line plagiarism scan of every file in the enormous repository**, a complete citation census, or a proof of global novelty. A failed theory can still contain an original calculation; an original calculation does not make the encompassing theory correct.

## Claim-by-claim assessment

| Claim family | Finding | Defensible priority status |
|---|---|---|
| \(a_0=\tfrac12c\sqrt{G\rho_\Lambda}\) | No independently authenticated earlier exact fixed-half match located in the reviewed sources. The broad MOND–cosmological-scale connection is much older. | Exact normalization/interpretation remains a bounded open priority question; not a derived universal constant. |
| March density formula | March 17 uses critical density; March 18 already contains the fixed-half dark-energy expression as a future asymptotic floor. June 4 adopts dark-energy tracking for the working interpretation. | Preserve the March occurrence, but do not backdate the later interpretation of today's galaxy scale. |
| \(a_0\propto\sqrt{\rho_{\rm DE}}\), constant for a cosmological constant | Shared scale relation and algebraic consequence; constant-versus-evolving MOND-scale discussion has older antecedents. | Not a uniquely new prediction by itself. |
| Gravitational seesaw \(M_\Lambda^2/(2M_{\rm Planck})\) | Natural-unit rewriting of the normalization, using the unreduced Planck mass. | Not a second independently derived law. |
| \(\mu(x)=1-e^{-x}\) | Explicit in Zhao–Famaey's 2005/2006 work. | Known exact function; cannot support a 2026 first-invention claim. |
| \(\nu(s)=[1-e^{-\sqrt{s}}]^{-1}\) | Milgrom–Sanders 2008, later used for the empirical RAR. | Known exact function, distinct from the preceding row. |
| \(g^2-g_N^2=a_0g_N\) | Closely tied to an older de Sitter thermal-response algebra; newer papers also use that form. | Prior mathematical form exists; applying a thermal analogy to galaxy orbits needs additional justification. |
| Deep-MOND BTFR \(v^4=GMa_0\) | Standard MOND result; substituting Carl's scale fixes its proposed normalization. | The substitution is conditional, not first discovery of the BTFR. |
| Memory/primordial clock motivation | Earlier modified-inertia history dependence and scalar-clock constructions; new independent 2026 memory proposals also exist. | Credit Carl's project-specific motivation without claiming invention of the entire subject. |
| Spatial filtering/elliptic auxiliaries | Carl has June prototypes; Elit has an August author deposit; Carl's later filtered-QUMOND action is not the same nonlinear equation. | Close overlap requiring exact-version comparison; no blanket first-author verdict. |
| Two-tensor constraint architecture | The July Sangtawee–De Felice–Karwan paper supplies a mechanism explicitly acknowledged by this repo. | A cited method applied to a new target, not evidence the authors took Carl's later implementation. |
| Four-form promotion and vacuum-energy integration constants | Older four-form/q-theory antecedents; the repo's particular coupling and normalization exercise are narrower. | Construction-specific novelty unresolved; broad mechanism is not new. |
| Tidal ratio, frequency identity, filtered compact-pair coefficient | No exact external duplicate located in targeted searches. | Candidates for narrow original results; bounded search only, assumptions and independent correctness checks still required. |
| \(GM/(4r)\) correction to \(v^2\) | Already present in the repo's 3 September inverse-exponential series before the 9 September P17 label. | A kernel-dependent mathematical consequence, not a separate discovery of a new field equation. |
| Wide-binary registered numerical bands and cluster tests | Many older and contemporary tests address the same systems; identical observables do not imply identical models or appropriation. | Specific frozen analyses may be original; no complete external dataset/code similarity audit was performed. |
| All-gates relativistic completion | This attribution review does not establish that any cited proposal or repo candidate passes all required physics gates. | Neither academic overlap nor a novelty label certifies closure. |

Exact external equations, dates and primary references supporting these classifications are in [SCALE_KERNEL_LITERATURE.md](SCALE_KERNEL_LITERATURE.md), [RELATIVISTIC_LITERATURE.md](RELATIVISTIC_LITERATURE.md) and [SCREENING_AND_MEMORY.md](SCREENING_AND_MEMORY.md). The source-authentication gaps are part of the findings, not omitted evidence.

## The three interpolation laws must remain separate

Set \(x=g/a_0\) and \(s=g_N/a_0\). The three claims in the project dossier mean:

\[
\begin{array}{ll}
\text{Exact exponential }\mu: & s=x(1-e^{-x}),\\
\text{Empirical RAR }\nu: & x=s/(1-e^{-\sqrt{s}}),\\
\text{The }a_0\text{-line}: & x=\sqrt{s^2+s}.
\end{array}
\]

They share a deep-MOND limit but are not interchangeable at finite acceleration. Consequently, a publication containing one is not an exact match to all three, and a repo timestamp for one does not establish priority for another. Zhao and Famaey explicitly discuss the first function; Milgrom and Sanders provide the second family. [Zhao–Famaey](https://arxiv.org/html/astro-ph/0512425v3), [Milgrom–Sanders](https://arxiv.org/abs/0709.2561).

Similarly, using \(\rho_\Lambda=\Lambda c^2/(8\pi G)\), the fixed-half relation is equivalent to \(a_0=c^2\sqrt{\Lambda/(32\pi)}\). This is a notation translation, not a dynamical derivation. A source with a free coefficient multiplying \(c^2\sqrt\Lambda\) contains a family that includes the numerical choice but does not necessarily propose or predict that particular choice.

## The closest contemporary overlaps

### Spatial filtering: substantial overlap, mixed chronology

The Elit comparison deserves attention because it shares the action/filter/compact-system motivation, not merely the word MOND. However, Carl's June spatial-filter/slip prototypes precede the August external record locally, while the later screened-QUMOND implementation has different field variables and follows it. Historical external PDFs were inaccessible, preventing a complete first-version comparison. See the precise operator comparison and retrieval limits in [SCREENING_AND_MEMORY.md](SCREENING_AND_MEMORY.md) and dated local content in [PROVENANCE.md](PROVENANCE.md).

**Conclusion:** cite the adjacent work when developing this architecture. There is presently no defensible basis to accuse its author, or to assign blanket priority over every filtered construction to either project.

### Constraint methods: acknowledged influence

The repo records its application of the Laplacian-constraint strategy from Sangtawee, De Felice and Karwan. Their first arXiv submission is 28 July 2026; their paper does not construct Carl's specific exponential MOND theory. This is a useful academic input to the programme, not an observed case of reverse appropriation. [Primary paper](https://arxiv.org/abs/2607.26031).

### Acceleration-scale literature: close does not mean exact

The scale review found old and very recent proposals relating MOND to de Sitter/vacuum scales. Importantly, a January 2026 paper by Singh retains an order-one matching factor; describing it as having independently fixed precisely the competing numerical coefficient overstates its result. A June 22 paper by Christodoulou, Kazanas and Laycock gives a closely related density scaling but translates to coefficient \(1/\sqrt3\), not \(1/2\), under its own averaging assumptions. Newly posted papers can also have much older preprints or proceedings ancestors. The scale appendix separates those dates instead of treating a 2026 journal/upload date as the discovery date.

## What is most worth protecting and presenting accurately

The strongest dossier would emphasize **specific equations with hypotheses and reproducible new calculations**, rather than claiming ownership of MOND, gravitational memory, the dark-energy coincidence or constrained auxiliaries generally.

Priority candidates for a carefully scoped record include:

- The precise fixed-half density hypothesis, with the critical-density and dark-energy-density versions separated, and the coefficient explicitly fitted.
- The filtered-action central tidal ratio and its domain: isotropic filtering, the specified kernel, external-field linear response and the stated source/background assumptions.
- Comparable-mass force calculations and any genuinely new numerical counterexamples or error bounds beyond existing MOND two-body results.
- Specific obstruction results, with the exact action and assumptions—not a universal no-go claim broader than the calculation proves.
- Frozen empirical protocols and released code as authored research artifacts, even where the underlying physical ideas have prior art.

No exact duplicate was located for the distinctive tidal/frequency expressions in the targeted search. That means **not located**, not **proven first**. A finite expression derived from an old constitutive function can be a useful original calculation without constituting a new fundamental law.

## Evidence needed to resolve an actual disputed match

For each concern, preserve the exact two texts: Carl's earliest immutable public release containing the equation, and the other author's earliest version containing the same equation. Then compare definitions, coefficients, assumptions, distinctive derivation steps, code and references. A git author/committer date records local history but does not establish when the commit became public. A reserved DOI or a local publish script does not prove successful deposit. Later versions must not be silently backdated.

No private correspondence, author access logs, or authenticated evidence of another researcher's access was supplied or found here. Missing acknowledgment can justify a neutral citation inquiry once an exact earlier result is documented; it is not by itself evidence of misconduct. Download/view ratios cannot identify who downloaded a document or why.

Recommended next deliverable, if desired: a short claim-level priority dossier containing the few strongest exact results, their immutable public versions, and a proper prior-art paragraph for each. This review did not send messages, publish deposits, modify the scientific papers, or commit/push changes.

## Coverage, limitations and audit artifacts

- Three independent workstreams examined repository chronology, scale/kernel literature and relativistic/constraint literature; the lead checked screened actions, memory and the synthesis.
- Discovery used broad web searches, exact equations/titles and SciSpace semantic searches. Conclusions were promoted only to the extent supported by primary papers or author/deposit records.
- Primary arXiv abstracts/version histories, HTML/PDFs, journal pages, author manuscripts and deposit metadata were checked where accessible. SciSpace metadata alone was not treated as a verified theorem or date.
- Some Zenodo/SSRN/PhilArchive requests failed. These failures limit priority conclusions, particularly Carl's independently timestamped public releases and the first versions of the closest filtered manuscript.
- No numerical physics scripts were changed or rerun: this task was a literature/provenance review, not a fresh certification of the field theory. No claim that all closure tests passed is made.
- Mathematical proofreading was limited to the new audit documents; older inconsistent notation and claims were left unchanged and flagged here.

Files: [CORE_AND_LIVE_CLAIMS.md](CORE_AND_LIVE_CLAIMS.md); this report; [PROVENANCE.md](PROVENANCE.md); [LIVE_TIDAL.md](LIVE_TIDAL.md); [LIVE_SCALE.md](LIVE_SCALE.md); [LIVE_Q0.md](LIVE_Q0.md); [SCALE_KERNEL_LITERATURE.md](SCALE_KERNEL_LITERATURE.md); [RELATIVISTIC_LITERATURE.md](RELATIVISTIC_LITERATURE.md); [SCREENING_AND_MEMORY.md](SCREENING_AND_MEMORY.md); [SEARCH_LOG.md](SEARCH_LOG.md).

**Final assessment:** no substantiated appropriation finding; confirmed prior art for several central ingredients; contemporary overlaps worth citing; narrowly defined originality and public-priority questions still open. This preserves Carl's actual contribution without attributing unsupported motives to other researchers.
