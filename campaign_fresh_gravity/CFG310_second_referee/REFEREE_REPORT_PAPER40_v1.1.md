# CFG310: second-round referee report on PAPER40 v1.1

**Manuscript:** "A Width-Chain Estimate of the MOND Acceleration Scale from MIGHTEE-HI COSMOS, with its Flux-Scale, Line-Width and Kernel Systematics".
- Files: `qwen_claude_field_theory/papers_2026/PAPER40_meerkat_a0_2026.{tex,pdf,zenodo.json}`.
- Version: v1.1, commit 24fcc8250.
- First round: CFG306 (1 CRITICAL, 5 MAJOR, 12 MINOR, 9 NIT).

**Lane and evidence.** Lane CFG310, 2026-10-03, read-only on the paper. The evidence files are in this folder:
- `cfg310_mirror_reproduction.out`
- `cfg310_referee_checks.py` with its `.out` and `_results.json` (sections P1–P6)
- `number_trace.csv`

**Standing rules applied.** κ = ½ is FITTED. "The data favour the framework" is never said. The cold mass is still required. Both footings are carried.

## Recommendation: MINOR REVISION. Do not deposit until the two MAJOR items are fixed.

Both MAJOR items are text-only. Every number they need is already in the paper's own `PAPER40_figures_numbers.json` or in CFG309's committed JSON.

**Reproduction is exact.**
- `make_paper40_figures.py` in a fresh `git archive` mirror passes 31/31 reproduction gates.
- It writes `PAPER40_figures_numbers.json` and both figure PDFs byte-identical to the committed files.
- `PAPER40_audit.py` reads committed sources through `git show HEAD:` of the live repository, read-only. It reports 375/375 values, 19/19 LIT values and 236/236 PDF-text checks.
- Both mutation modes fail, as they must.
- All 28 traced numbers match (`number_trace.csv`).

**First round.** The critical rest-frame correction (C1) is carried through everywhere: Table 1, the abstract, κ, the figures and the version note. The other first-round items are mostly resolved:
- the all-baryon flux reading is withdrawn;
- CC2 is called baryon-side only;
- kernel, selection, H₂, q₀ and δ = 5 rows are added;
- prior art is corrected (V25 1.69, the V26 kernel and its SPARC-anchored 5σ rise, Lelli+19, Papastergis+16, McGaugh 2012, Desmond 2023, SPARC's ±0.24 systematic);
- the abstract is now 206 words.

**What remains.** The revision states its footing verdict on one convention and truncates the flux range.
- **The flux range.** The single-dish range quoted in the abstract leaves out CFG304's own frozen primary reading (0.90). It also departs from the adopted record (STANDING, CFG309 entry: 0.90–1.06; "about 0.9–1.31 between flux scales").
- **The footing verdict.** "The canonical footing just outside the recipe width" holds only on the catalogue's H₀ = 70 distances. On the value the paper itself calls like-for-like (H₀ = 67.4), the canonical footing is inside.

The paper is otherwise scrupulous about what it does not claim:
- not a footing discriminator;
- not an a₀(z) test;
- κ = ½ fitted;
- the cold mass still required;
- no "data favour" sentence.

**Counts by severity:** 0 CRITICAL, 2 MAJOR, 7 MINOR, 3 NIT.

---

## A. First-round findings: status in v1.1

| CFG306 | status | note |
|---|---|---|
| C1 rest-frame W50 | **resolved** | k = 0 is primary (CFG309, frozen). k = 1 is kept as a disclosed variant; all downstream numbers recomputed |
| M1 flux range | **partly** | (a) the all-baryon reading is withdrawn; (b) the extrapolations are reported; (c) the direction argument is given. The range is truncated at 0.97 and leaves out the frozen primary's 0.90, against the referee's 0.90–1.13 (finding 1). The abstract still leads with the catalogue-scale value |
| M2 CC2 / width side | **partly** | CC2 is now called baryon-side; the width-side test is reported; the non sequitur is deleted. Not done: a W50 → V_flat calibration (Lelli+19 cited only), and δ treated two-sided around an empirical value (finding 7) |
| M3 kernel | resolved | Table 2 kernel rows; the footings are stated to be kernel-free and comparisons conditional on the exponential kernel; "framework-native" is gone |
| M4 selection | resolved in text | The S/N-threshold rows, residual correlations and joint fit are reported. Not in the abstract (finding 4) |
| M5 prior art | resolved | (a)–(f) all addressed; checked against the audit's LIT rows and CFG279 |
| m1, m3, m5–m11 | resolved | |
| m2 bootstrap | resolved as asked | The SD is quoted, but see finding 3: the k = 0 per-galaxy spread grew and the bootstrap SD no longer matches it |
| m4 H₀ convention | **cosmetically** | 1.208 is printed and called "like-for-like", but every verdict still uses 1.311 (finding 2) |
| m12 lane labels | partly | Data availability maps the lanes to folders, which is acceptable for Zenodo (finding 12) |
| n1 abstract length | resolved | 206 tokens |
| n2 byline/creator | owner | Byline "The authors"; Zenodo creator is the owner's name |
| n3 title, n4 figures, n6–n9 | resolved / disclosed | |

---

## B. Findings

### MAJOR

**1. [MAJOR] The single-dish range leaves out CFG304's frozen primary and departs from the adopted record.**

*Where:*
- Abstract: "a₀ falls to 1.07 (0.97–1.13)".
- Section 5, "What the flux scale does" (l.194): "We take 1.07 (0.97–1.13)", and "the honest range is about 1.0 to 1.31".
- Fig. 1 open triangle; Conclusions.

*The evidence:*
- The paper's own `flux_k0` rows (CFG310 P2) give 0.901 (CFG304's frozen primary, 15 code-1 pairs, R = −0.195), 0.968, 1.017, 1.057, 1.069 and 1.132 ×10⁻¹⁰.
- The quoted central value, 1.07, is a post hoc linear extrapolation in SNR_3D over 15 pairs (Spearman p = 0.01).
- The quoted range drops the frozen 0.90.
- CFG306 recommended 0.90–1.06 (or 0.90–1.13).
- STANDING (CFG309) records 0.90–1.06 and "about 0.9–1.31e-10 between flux scales".

*Why it matters:* Including 0.90 would not change any verdict: the canonical footing is −0.016 dex from it, inside. But dropping the only frozen reading in favour of a post hoc extrapolation is exactly what the frozen-criteria discipline exists to prevent.

*Fix:*
- Quote 0.90–1.13. Either give no single central value, or name the frozen 0.90 and the SNR-extrapolated 1.07 as two readings.
- Change "about 1.0 to 1.31" to "about 0.9 to 1.31".

**2. [MAJOR] The footing verdict depends on the H₀ convention, and the paper itself calls the other convention like-for-like.**

*Where:*
- Abstract: "the canonical footing just outside the recipe width".
- Section 4 "The level" (l.119): "Both footings lie outside the 95% statistical interval".
- Section 4 "The coefficient"; Section 6 bullet 1; Conclusions.
- Section 5 "Distances and H₀" (l.206): "against the footings this is the like-for-like value".

*The evidence* (CFG309's committed H₀ = 67.4 knob, CFG310 P3):
- a₀ = 1.208 ×10⁻¹⁰ (s* = 1.290).
- The canonical footing is +0.111 dex away. That is inside the recipe half-width whether the H₀ knob is kept (0.128) or removed once it has been applied as a correction (0.123).
- The 95% statistical lower edge becomes 1.111 ×10⁻¹⁰, so the alternative footing (1.131) is inside the statistical interval.
- The κ values are 0.645 and 0.534.

*Why it matters:* The paper's two "fail" statements (canonical outside the recipe width; both footings outside the 95% statistical interval) hold only on the catalogue's H₀ = 70 distances. The standing rule is to verify a fail as hard as a win and to give both footings and conventions. A verdict that flips with the convention must be stated on both.

*Fix:*
- In the abstract and Section 6, give both: "canonical footing 0.019 dex outside the recipe width on the catalogue's H₀ = 70 distances, inside it (0.111 dex) on H₀ = 67.4, the convention of ρ_Λ".
- Remove the H₀ knob from the recipe when the H₀ shift is applied as a correction, or say why it is kept.

### MINOR

**3. [MINOR] The statistical error depends on the method, and the alternative-footing statement rests on the narrower one.**

*The evidence* (CFG310 P4):
- The bootstrap SD is 0.034 dex. It is stable across five seeds: 0.031–0.036.
- The paper's own per-galaxy robust SD is 0.261 at k = 0 (it was 0.199 at k = 1). That implies an asymptotic standard error of the median of 0.048 dex.
- The 68% interval is very asymmetric (−0.013 / +0.034 dex). The per-galaxy roots cluster just at and below the median, then jump by 0.02 dex.
- With 0.048 dex, the 95% half-width is 0.093 dex, so the alternative footing (0.064 dex below) is inside.

*Fix:* Quote both error estimates, or a smoothed bootstrap. Do not base "both footings outside the 95% statistical interval" on the bootstrap tail alone.

**4. [MINOR] The selection systematic is missing from the abstract.**
- Removing the frozen SNR_3D ≥ 8 cut gives +0.084 dex. The 23 removed discs alone give 2.23 ×10⁻¹⁰ (+0.23 dex).
- This is as large as the kernel term, which the abstract does list. A 0.23 dex difference between low- and high-S/N discs is larger than any systematic the abstract lists.
- *Fix:* one clause, for example "the S/N cut moves a₀ by up to +0.08 dex".

**5. [MINOR] "Line-width corrections lower a₀ by up to 0.10 dex" sits beside a larger number in the paper's own text.**
- Section 3 says the CC2 recipe with W50/(2 sin i) in place of V_flat returns s* higher by +0.184 dex at δ = 0.
- The "0.10" is the deep-limit 4 × 0.026 dex. The 0.184 is amplified because the SPARC galaxies are not deep.
- *Fix:* say so in one sentence, so that the 0.10 is not read as contradicted by the 0.184.

**6. [MINOR] All three independent data tests of the velocity frame lean the same way, and the paper never says so.**

*The three tests:*
- CFG302: the raw widths agree with the catalogue to −0.022 dex as rest-frame, and to +0.002 as observed-frame.
- CFG304: the ALFALFA width ratio is 0.000. That is the observed-frame prediction; the rest-frame reading predicts −0.012.
- CFG309 T4: busy-function fits give −0.017 for the rest-frame reading. The test is inadmissible because it failed its injection control.

*What the paper says:* It correctly says no data test can decide, and that the catalogue paper's worked examples (5 of 5 to 7 × 10⁻⁴) carry the decision. It reports each lean separately ("does not decide").

*Fix:* Add one sentence saying that all three point weakly to the observed frame, so the k = 1 variant (1.046) stays a live alternative. It is already shown in Table 2 and Fig. 1.

**7. [MINOR] The width side is still uncalibrated for these discs (CFG306 M2 partly resolved).**
- δ enters the recipe as a one-sided 11 km/s knob, plus a post hoc δ = 5 row.
- No empirical W50 → V_flat relation (Lelli+19 or the 22-galaxy SPARC × ALFALFA overlap) is applied as a two-sided term.
- The Conclusions rightly name this as one of the two largest systematics.
- *Fix:* add the Lelli+19 relation as a Table 2 row, or state that it was not applied and why.

**8. [MINOR] The V26 anchored-evolution results are quoted selectively.**
- PAPER40 quotes V26's formal 5.0σ SPARC-anchored *rise* (varying M/L).
- It omits V26's constant-M/L anchored result, −4.80 ± 0.76 ×10⁻¹⁰ per unit z (a 6.3σ *fall*).
- The MNRAS v3.2 manuscript quotes both, and they are in CFG279's committed output.
- *Fix:* quote both. Together they show that the anchored trend is set by the M/L treatment.

**9. [MINOR] The Zenodo metadata are thin.**

*What is there:* The title matches the tex; the version string is "2026-10-03-v1.1"; CC-BY-4.0; 13 keywords; the description's numbers match the abstract.

*What is missing or off:*
- No `related_identifiers`: the GitHub repository and commit, the MM26 catalogue DOI, the SARAO cube DOI and P38 are all absent.
- The description labels this "Version 1.1", but v1.0 was never deposited. It also points readers to internal lane labels (CFG306, CFG309).
- The byline "The authors" differs from the creator field (owner's call, as in round 1).
- The PDF has no Title or Author metadata.

*Fix:*
- Add `related_identifiers`: isSupplementedBy the repository at 24fcc8250; references 10.1093/mnras/stag1091 and 10.48479/jkc0-g916.
- Either call this deposit version 1 with a "revision history" note, or link the v1.0 commit.
- Add hyperref pdfinfo.

### NIT

**10. [NIT] The joint-fit 68% interval is not printed.** The 68% interval of b_z, [−5.18, −0.47] per unit z, excludes zero. Only the 95% interval [−8.0, +1.5] is printed, so "neither is resolved" is true at 95% only. Print the 68% too.

**11. [NIT] The byline and the creator field differ:** "The authors" against the owner's name (owner's call).

**12. [NIT] Lane labels are still the main way sources are cited.** CFG301, CFG302 and so on carry the citations. For Zenodo this is acceptable with the Data availability map. For a journal, each would need a public data or methods statement.

---

## C. Zenodo deposit sanity

| item | status |
|---|---|
| title = tex title | yes |
| version string | "2026-10-03-v1.1"; v1.0 not deposited (finding 9) |
| creators | one creator with affiliation (owner's call against the "The authors" byline) |
| license | cc-by-4.0 |
| description = abstract numbers | yes: 1.31e-10, ±0.034 / ±0.128 dex, κ 0.70/0.58, 1.07 (0.97–1.13), 0.06–0.07 dex, 0.009 dex, 375/375. The 0.97–1.13 inherits finding 1 |
| related identifiers | none (finding 9) |
| PDF | 9 pages, 187 kB, fonts embedded; no title/author metadata |
| personal data | no e-mail or home path in the tex, PDF, figures, JSON or scripts (git grep, strings) |
| AI disclosure | present; names six providers |

## D. Number trace (28 rows, `number_trace.csv`)

All 28 match their committed sources and are printed. Five carry a referee note:
- **P04:** the error method (finding 3).
- **P14:** the truncated range (finding 1).
- **P20:** selection is not in the abstract (finding 4).
- **P22:** the like-for-like verdict flip (finding 2).
- **P27:** the unprinted 68% interval (finding 10).
