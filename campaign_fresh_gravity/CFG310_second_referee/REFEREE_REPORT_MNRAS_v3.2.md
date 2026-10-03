# CFG310: second-round referee report on MNRAS v3.2

**Manuscript:** "The galactic acceleration scale and the cosmological constant: the coefficient on SPARC, and what it takes to measure its redshift evolution".
- Directory: `qwen_claude_field_theory/papers_2026/mnras_submission_2026_v3/`.
- Version: tag `mnras-v3.2` = d96f177fe. The tag is pushed to origin. The directory is unchanged at 24fcc8250.
- First round: CFG290 (1 CRITICAL, 10 MAJOR, 20 MINOR, 8 NIT). Revision notes: SUBMISSION_CHECKLIST §7e/§7f.

**Lane and evidence.** Lane CFG310, 2026-10-03, read-only on the paper. The evidence files are all in this folder:
- `cfg310_mirror_reproduction.out`
- `cfg310_referee_checks.py` with its `.out` and `_results.json`
- `cfg310_shared_calibration_N.py` with its `.out`
- `cfg310_number_trace.py`, `number_trace.csv` and `cfg310_number_trace.out`

**Standing rules applied.** κ = ½ is FITTED. "The data favour the framework" is never said. The cold mass is still required. Both footings are carried.

## Recommendation: MINOR REVISION, conditional. Not ready to submit until the five MAJOR items are fixed.

All five are text, disclosure or citation fixes. The only new numbers they need are already in committed outputs.

**Reproduction is clean.**
- `reproduce_all.sh` from a fresh `git archive` mirror reports ALL STEPS PASSED. `paper_numbers.py` runs 100 checks with 0 FAIL.
- `paper_numbers.out` and `.json` are byte-identical to the committed files.
- The six figures differ only in their creation date (rendered pages identical by hash). The PDF text is identical.
- All 28 traced numbers match their committed sources (`number_trace.csv`).

**First round.** The CRITICAL and most MAJOR findings are genuinely resolved: the gated decision value, power and P(20:1), the H₀ convention, Limbach+08, Desmond 2023 with a published-values table, no σ quoted against rivals, the RC100 disclosures, a methods appendix, the AI disclosure, and PAPER6 dropped.

**The v3.2 revision added new problems.** It promoted a "native-baryon" RC100 route to primary and rewrote the redshift summary, and in doing so:
- regressed one fixed finding (MUSE-DARK wording, CFG290 #16);
- describes a heavily censored sample as "no rise";
- overstates how far the journal table was checked;
- states design requirements that are not jointly sufficient;
- uses ALESS 122.1 data without citing any of its three sources.

**Standing rules.** No sentence says the data favour the framework. κ = ½ is stated as fitted throughout (Sections 3.9 and 5). The cold mass is stated as still required (Section 5). Both densities are carried in the body. The abstract quotes κ on the ρ_Λ footing only (finding 6).

**Counts by severity:** 0 CRITICAL, 5 MAJOR, 8 MINOR, 4 NIT.

---

## A. First-round findings: status in v3.2

| CFG290 # | status in v3.2 | note |
|---|---|---|
| 1 CRIT decision value | **resolved** | +0.22 at the gate's halo mass. The abstract still headlines N for σ_sys = 0; see finding 5 |
| 2 expected odds vs P(20:1) | resolved | Table 11 gives P₂₀, P_wrong and N₉₀ |
| 3 mixed H₀ | resolved | Table 7 covers four conventions. Fig. 2(b) bars are computed |
| 4 Limbach+08 | resolved | |
| 5 selective κ citations | resolved | Table 8; Desmond at 2.6σ in the abstract |
| 6 RC100 σ vs rivals | resolved | Only drift-table σ are quoted |
| 7 RC100 disclosures | resolved | (a)–(c) all present |
| 8 re-analyses without methods | **partly** | Appendix B is added. The 0.2–0.7 dex gas bracket is still the author's own computation, cited to Zimmerman2026wall (finding 10) |
| 9 PAPER6 | resolved (owner) | Citations dropped; the cover letter declares the posting |
| 10 AI disclosure | resolved (owner) | Six providers named, plus the two model-produced inputs |
| 11 scope | **partly** | Section 4 folded in, Z dropped; the order is kept (finding 13) |
| 12 abstract length | resolved | 239 tokens in the tex, 243 in the paste text (limit 250) |
| 13 DOI | resolved | |
| 14 comparator slopes | resolved | |
| 15 decades | resolved | |
| **16 MUSE-DARK wording** | **REGRESSED** | v3.1 used STANDING's wording. v3.2's abstract says the rise "disappears", and Conclusion (vi) says it "travels with the halo-fitted masses" (finding 1) |
| 17–26, 28, 29, 31–39 | resolved | Spot-checked against the tex and paper_numbers |
| 27 frozen snapshot | resolved | Tag `mnras-v3.2` exists locally and on origin (d96f177fe); no Zenodo snapshot |
| 30 "author ran every script" | owner | Wording made literally true; TODO-RUN open |

---

## B. Findings

### MAJOR

**1. [MAJOR] The abstract and Conclusion (vi) over-claim on MUSE-DARK. This regresses CFG290 #16.**

*Where:*
- Abstract (tex l.40): "the MUSE-DARK rise at z≃1 disappears".
- Conclusion (vi) (l.637): "travels with the halo-fitted masses: on SED masses no route rises".

*Why it is wrong:*
- The body (l.531) correctly says "The data cannot say which masses are biased … The rise is route-dependent: neither it nor constancy is established."
- The abstract and conclusion read as if the rise were shown to be an artefact.
- The gas-inclusive native route, route (ii), is itself inconsistent with constancy. Committed rows, `paper_numbers.json` S7.native.musedark (CFG310 M4):
  - s* = 0.22, 0.27 and no root in the three thirds;
  - FLAT lies outside the 95% interval in 2 of 3 thirds (z = 0.88 excluded, z = 1.20 no root);
  - D < 1 in 13/37, 14/36 and 21/36 galaxies.
- The quoted −0.26 ± 0.28 is route (iii), stars only and no gas.
- The native route's g_obs is still the DC14 halo-fit model velocity (Appendix B; CFG303 header). The main text says only "the model's dynamical acceleration".

*Fix:*
- Abstract: "the MUSE-DARK rise at z ≃ 1 is not recovered with SED stellar masses; with molecular gas added the baryons exceed the model dynamics, and the data cannot say which masses are biased."
- In Section 4.3, report route (ii)'s levels and its FLAT exclusion.
- Replace Conclusion (vi)'s "travels with the halo-fitted masses".

**2. [MAJOR] The primary RC100 native route is a censored sample, and it is described as "show no rise".**

*Where:* Abstract; Section 4.3 (l.516–529); Conclusion (vi); Fig. 6(a).

*What CFG303's per-galaxy table shows* (CFG310 M3):
- 41 of 100 discs sit at the Newtonian floor (g_bar,native ≥ g_obs).
- The floor fraction rises with redshift: 27% (z 0.5–1.0), 33%, 47%, 51% (z 2.0–2.6). Spearman ρ = +0.25, p = 0.013.
- Dropping the floor discs removes the low-a₀ tail preferentially at high z.
- Kept as censored values (ranked lowest), the implied a₀ *falls* with z: Spearman −0.27, p = 0.006. Above z = 2 the median disc is at the floor.
- A fall is inconsistent with all three laws. It is a z-dependent bias of the native baryons (Tacconi gas plus SED M* in a thin disc).
- The paper's own decision rule reads such a result as counting against all the laws, not as support for constancy.

*What the injection does not test:* I5n uses 0.05 noise in f. It does not model 0.2-dex baryon errors or the floor censoring.

*What the paper already says:* "Neither result is a measurement", and it notes the 41 floor discs. It does not report how they depend on redshift.

*Fix:*
- Report the floor fraction by redshift.
- Say that the native route mainly diagnoses the baryon calibration.
- Change the abstract and Conclusion (vi) wording from "show no rise" to, for example: "on halo-free baryons 41 of 100 discs (half of those at z > 2) have baryons exceeding the dynamics, so the route measures the calibration, not a₀".
- Optionally, add a censored-regression (Tobit-type) slope.

**3. [MAJOR] ALESS 122.1 is used without citing any of its data sources. This blocks submission.**

*Where:* Section 4.3 "Native inputs" (l.539); Conclusion (vi); Acknowledgements.

*What is missing:* references.bib has no entry for:
- Dunne et al. 2022 (the gas: CO, dust and their conversions);
- Calistro Rivera et al. 2018 (σ = 129 km/s);
- **Amvrosiadis et al.**, the source of the kinematics and α_CO used by CFG307. Its README parses "the Amvrosiadis and Dunne TeX". This third source was not in the known-open list.

*Fix:* Add all three to the references and to the Acknowledgements table list, or drop ALESS 122.1.

**4. [MAJOR] The journal check is overstated for the column the primary route uses.**

*Where:* Section 4.3 (l.516, "We use the published table … checked cell by cell against the journal and against arXiv:2209.12199v1"); Data Availability (l.646).

*The problem:*
- `rc100_nestorshachar2023_table3_PUBLISHED.csv` carries no SED stellar-mass column (CFG310 M6).
- The native route's M* is CFG303's one-reader transcription of arXiv-v1 column 6, made from the raster.
- Only row 87's M* was compared with the journal (CFG305 README; SUBMISSION_CHECKLIST §7f says so under "Not verified").
- The partial cross-check (CFG303 T3: median 0.000 dex against Price+21 for the 41 RC41 galaxies) is not mentioned.

*Fix:* Either check column 6 against the journal table B1, or state that "the SED stellar masses used by the primary route were transcribed from arXiv v1 and agree with Price et al. (2021) for the 41 galaxies in common".

**5. [MAJOR] The abstract and Conclusion (vii) state design requirements that are not jointly sufficient.**

*Where:*
- Abstract: "about eight lensed discs … measured to 0.20 dex … and a common baryonic-mass calibration good to 0.06 dex".
- Conclusion (vii) (l.638): "All of this assumes a … calibration shared by the sample to 0.06 dex".

*Why it is wrong:*
- N = 8 is computed for a shared calibration error δ_c = 0. The 0.06 dex is the N → ∞ limit "from the sample means".
- `cfg310_shared_calibration_N.py` re-implements the Table 12 KL computation and reproduces it (20.8:1, 6.2:1 and 2.4:1 at δ_c = 0, 0.05 and 0.10). On that computation:
  - eight discs at δ_c = 0.04 give 8.4:1;
  - eight discs at δ_c = 0.06 give 4.8:1;
  - 20:1 needs about 21 discs at δ_c = 0.05 and 36 at 0.06.
- The ΛCDM model systematic (σ_sys = 0.10/0.20 → N₂₀ = 27/48) is also absent from the abstract.

*Fix:* Give N as a function of δ_c, for example: "eight if the shared calibration were exact, about 20–40 at 0.05–0.06 dex, more if the concentration–mass relation is uncertain". Reword Conclusion (vii) the same way.

### MINOR

**6. [MINOR] The abstract quotes κ on one footing.** "The value 1/2 is consistent with all three" holds on ρ_Λ. On ρ_crit, estimators A and C put ½ at 2.1σ and 2.2σ (Table 6, last row; Section 3.9). The standing rule is both footings. *Fix:* add "(on the critical density, 1/2 lies 2.1–2.2σ from A and C)".

**7. [MINOR] A stale number sits in the MUSE-DARK paragraph.** "Restoring the rise on the SED route would need an SED-mass bias of 1.8–2.2 dex per unit redshift" comes from `S7.musedark.tau_star` R198/R199a. Those are the superseded halo-normalised SED routes. The paragraph now discusses the native routes. *Fix:* recompute for route (iii), or label the number as belonging to the earlier routes.

**8. [MINOR] KURVS: magnitudes against interest are omitted.**

*What the committed record shows* (S7.native.kurvs):
- At the native P2 cell, both laws under-predict the outer accelerations: FLAT by +0.375 ± 0.055 dex (6.8σ), the rival by +0.228 ± 0.054 dex (4.3σ).
- The rival is closer.
- Seven native cells lean to the rival and four to constancy.

*Why it matters:* The abstract's "a lean … needs a simulation-calibrated pressure correction" implies that the lean is an artefact of the ΛCDM calibration.

*Fix:* Quote the native P2 residuals, and say that with analytic corrections more cells lean to the rival than to constancy.

**9. [MINOR] ALESS 122.1 and CRISTAL are reported asymmetrically.**
- CRISTAL gets both exclusion fractions.
- For ALESS only the no-root fraction (44%) is given. FLAT is excluded in 27% of 540 cells, always from above; H(z) in 15%; the primary native s* is 8.8.
- "Two points that appeared to exclude a constant a₀" does not say whose analysis made them appear so (the repository's CFG229 chart).

*Fix:* Give the same fractions for both objects, and name the earlier analysis.

**10. [MINOR] The gas bracket is still self-sourced (CFG290 #8 partly resolved).** The 0.2–0.7 dex is the author's metallicity extrapolation of Bertemes+18 against Geesink+26, cited to Zimmerman2026wall. The primary papers are now cited, but the bracket itself is not described. *Fix:* add one sentence of method in Appendix B (the extrapolation choices that give 0.2 and 0.7), pointing to CFG224/CFG238.

**11. [MINOR] "framework-native" is undefined for a journal reader.** It appears three times in the tex (Fig. 6 caption; Appendix C) and in the Fig. 6 alt text. The paper never defines "the framework". *Fix:* use "halo-free baryons" or "SED + scaling-relation baryons".

**12. [MINOR] Two different "41"s appear in the same subsection.** In Section 4.3 one is the 41 floor discs and the other is the 41 RC41 galaxies of Price+21 (CFG217 G2). A reader can take them to be the same set. *Fix:* give the overlap, or rename one.

**13. [MINOR] The scope question from round 1 is still open (CFG290 #11).** At 16 pages, the κ measurement and the a₀(z) design are two papers. The second is the novel one. Desk-rejection risk is lower than in v3 but not gone. This is the editor's judgement; the authors should expect the question.

### NIT

**14. [NIT] The abstract length is at the edge on the checklist's own convention.** Counts: 239 whitespace tokens in the tex, 238 with math spans as single words, 243 in the ScholarOne paste text, and 249 on the checklist's math-as-word convention. Any added clause (findings 1, 2, 5, 6) needs an equal cut.

**15. [NIT] The cover-letter preamble is stale.** COVER_LETTER.md (outside the paste region) still says the AI paragraph "must be finalised by the author (TODO-AI-DISCLOSURE)", which was decided on 10-02.

**16. [NIT] TODO-RUN is still open (owner).** If the owner runs `reproduce_all.sh` once, the stronger reproducibility wording can be restored.

**17. [NIT] The Fig. 6 alt text uses "framework-native route"** (see finding 11).

---

## C. Compliance

| item | status |
|---|---|
| abstract ≤ 250 words | yes: 239 (tex tokens) / 243 (paste text) / 238 (math as one word); 249 on the checklist's convention |
| keywords | 6, all from the MNRAS list (unchanged since round 1) |
| AI disclosure | Acknowledgements and cover letter name Claude (Claude Code), OpenAI, DeepSeek, GLM, Qwen and Gemini, plus the two model-produced inputs |
| Data Availability | present; names tag `mnras-v3.2` (exists, pushed); overstates the journal check (finding 4) |
| figure alt text | 6 of 6 in the git-ignored bundle file 04; consistent with the figures; "framework-native" (finding 17) |
| PDF ≤ 10 MB | 0.40 MB, 16 pages, all fonts embedded, title/author metadata present |
| personal data | no e-mail or home path in tracked files or in the PDF/figure bytes (git grep at 24fcc8250; strings); the e-mail is only in the git-ignored bundle |
| references | 64 bib entries / 63 cited (PAPER6 dropped). Lee2025 matches Crossref (A&A 701, A260, DOI 10.1051/0004-6361/202555362) and arXiv 2507.11600 (the known open item, now checked). ALESS sources missing (finding 3) |

## D. Number trace (28 rows, `number_trace.csv`)

All 28 match. Nine carry a referee note:
- **M15:** the RC100 native slope is a censored sample.
- **M22:** the MUSE-DARK native result omits route (ii).
- **M25:** the ALESS fractions are asymmetric and its sources uncited.
- **M27:** the 1.8–2.2 figure comes from the superseded routes.
- **M09, M20, M23, M24, M26:** context only.
