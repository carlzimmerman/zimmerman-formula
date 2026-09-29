<!-- Claims audit. A NEW documentary file; no paper was edited and nothing was deposited. Quotes and line numbers were checked by the compiler against the files at HEAD. -->
# Claims audit of the program's papers against the lanes of 2026-09-28/29

**Scope.** Every load-bearing claim in PAPER33–PAPER37 and the MNRAS manuscript v2 that the new committed results weaken, contradict or leave unsupported. Also included are the headline claims that a new result tests and that survive. The new results are CFG40–CFG67, the CFG48 and CFG49 referee notes, and `GATES_STATUS_2026-09-29.md`.

**Classes.**
- **REQUIRES-CORRECTION:** the paper states as fact something a later committed result contradicts, or quotes a superseded number that changes the conclusion.
- **SOFTEN:** not contradicted, but overstated given the new results.
- **STILL-STANDS:** a later result tests the claim and it survives.

**Method.**
- Three read-only readers each read two documents in full. Each was given the same evidence list (below).
- The compiler then checked every quoted line against the file at HEAD (`grep -n`) before including it.
- Deposited papers are marked; a REQUIRES-CORRECTION item in a deposited paper needs a Zenodo new version or erratum, which is the owner's call.
- **Nothing was edited or deposited.**

## The evidence (committed; cited by lane and commit)

| id | lane (commit) | result |
|---|---|---|
| E1 | CFG55 (791083f7f) | SLUGGS with each galaxy's own JAM-calibrated stellar mass: the law under-predicts the outer GCs by +0.097 ± 0.024 dex (4.0σ; alt 3.65σ), so this is not an IMF artefact. The derived rule, calibrated the same way, leaves +0.046 (2.6σ). With population masses it had been 0.4σ (CFG38). |
| E2 | CFG61 (3c03f9678; criteria d7aecf12b) | KiDS-1000 early/late split. The rule makes no colour-dependent prediction at KiDS masses. The early-minus-late difference rejects the law and B with the rule (identical there) at χ² 28.1/7, p = 2.1e-4 (≈ 3.7σ). This is a **reported χ² row evaluated after the first run**: the frozen amplitude statistic was degenerate and H1/H2 failed as coded. |
| E3 | CFG67 (f1df7889a) | The ΛCDM control for E2. Through the same machinery, standard halos reproduce the split: colour-split halos give χ² 6.5/7, and even colour-blind Moster halos give 6.9/7. E2's failure is specific to B's mass-independent dark mass. |
| E4 | CFG59 (3371b14ac), CFG62 (6a755e5d6) | No universal debris fraction φ, and no split by one variable, reconciles the rule's ten populations. It would take three non-monotonic mass bands, and the X-ray ellipticals need φ ≈ 2.15. |
| E5 | CFG42 (67c170fe7), CFG45 (5518cfcd0), CFG58 (3371b14ac) | The rule closes the ultra-faint failure but fails M31 LVD (−2.67σ) and the LV field dwarfs (−3.47 / −2.70σ). No reading of the rule passes all seven gates. The TDG and DF2/DF4 passes rest on ownership. |
| E6 | CFG46 (e6ecfd6ff), CFG51 (d7e6a6565) | Binary corrections lower the ultra-faint offset by 0.07–0.10 dex but do not remove it. Cleaned Boötes I is +0.22 (2.46σ) and Tucana II +0.47 (3.63σ). |
| E7 | CFG40 (e773982cd), CFG56 (33e1af197) | Super spirals: the nine fastest sit +0.164 dex above the law (2.34σ). A marginal failure at the top of the disk mass function; the rule cannot help. |
| E8 | CFG41 (42c87ead1), CFG53 (6a48c4e2e) | Massive S0/S0a with HI to 97 kpc: the rule is at −0.8σ by amplitude and −1.2σ by shape; the test cannot decide. UGC 2487 is still over-predicted by 0.14 dex. |
| E9 | CFG52 (9ffb95d57), CFG54 (8b6473b7a) | The a₀(z) test at z ≈ 2.5 cannot be run on the data on disk. |
| E10 | CFG43 (e42a98572), CFG44 (513ee4b28), CFG50 (bb2a7b680) | Gap 3 is partly filled (the tie is written into a fluid's stress cap; a barotropic cap is excluded). Gap 2 is a scoped no-go that reduces to Gap 1's enclosed-mass object. |
| E11 | CFG48 (0dba13349) + referee 35eebbe99 | Gap 1 is a scoped no-go (Gauss, history, the exchange's reaction and energy). A nonlocal enclosed-mass gate is second-variation stable (48/48, referee-reproduced). CFG48's r_ta is not the committed convention, so its ball gate's edge sits at 0.11–0.24 r_ta. |
| E12 | CFG49 (b899e204e) + referee c402c10ae | A local gate scalar needs two new untied constants and pays DE13's N1 cost. It has no separate frozen-criteria file. |
| E13 | CFG47 (4dfa7d995) | The Unruh / de Sitter route to κ = ½ is retired; κ stays FITTED. |
| E14 | commit 97f30b36c (reported, not re-run) | Like-for-like on H₀, κ = ½ and 1/2π are indistinguishable. The 2.2σ preference holds only with 1/2π on the dark-energy footing. |
| E15 | GATES_STATUS_2026-09-29.md (17e897cf0) | B's gate record has sharpened, not improved. |
| E16 | CFG57 (78a5a3a0a) | The hot-gas test on SLUGGS is frozen but not run. |

## Bottom line

- **PAPER36 (deposited) needs a correction notice: 3 claims REQUIRE CORRECTION.**
  - Its SLUGGS fit (0.4σ) does not survive dynamical stellar masses: 2.6σ (CFG55).
  - "One galaxy disagrees" is no longer true. The rule also fails SLUGGS with dynamical masses, M31 LVD (−2.67σ) and the LV field dwarfs (−3.47σ), and it cannot make the KiDS colour split.
  - The basis for "stays at 42/48" is contradicted, because the rule flips two harness gates.
  - A Zenodo new version or erratum is the owner's call.
- **PAPER37 (draft) has 6 claims that require correction before any deposit.**
  - It predates CFG61, CFG62 and CFG67.
  - It states gate instability without the locality condition that CFG48 G6 found.
  - It understates the rule's costs.
  - Its one remaining qualitative constraint on the rule is refuted by CFG62.
- **PAPER35 (draft) has 1:** Amendment 15 is now filed.
- **PAPER33 and PAPER34 (deposited) and the MNRAS v2 manuscript need no correction**, only softer wording.
  - PAPER33's closing outlook assumes a completion that Gaps 1 and 2 now rule out.
  - PAPER34's abstract should say "prescribed switch".
  - The MNRAS odds should budget a correlated mass-calibration error.
- **The claims that survive are the negative and scoped ones.** κ fitted, not derived; no committed action produces B; the a₀(z) test cannot yet be run; the ultra-faints are not explained.

| document | status | REQUIRES-CORRECTION | SOFTEN | STILL-STANDS |
|---|---|---|---|---|
| PAPER36 | DEPOSITED, DOI 10.5281/zenodo.23025372 | 3 | 6 | 6 |
| PAPER37 | draft, NOT deposited | 6 | 7 | 6 |
| PAPER35 | draft, NOT deposited | 1 | 6 | 5 |
| PAPER34 | DEPOSITED v2, DOI 10.5281/zenodo.22984587 | 0 | 3 | 2 |
| PAPER33 | DEPOSITED v2, DOI 10.5281/zenodo.22967954 | 0 | 3 | 1 |
| MNRAS manuscript v2 | revised 2026-09-25, NOT submitted | 0 | 1 | 5 |

The line numbers are those of the files at HEAD. Each quote was checked verbatim at its line by script (61 of 61). Quotes are exact LaTeX. Where a claim recurs, the other lines are named in the reason.

## PAPER36 — the cold component keeps its collapse mass

`qwen_claude_field_theory/papers_2026/PAPER36_cold_mass_conservation_2026.tex`: DEPOSITED, DOI 10.5281/zenodo.23025372.

| line | quote (verbatim) | evidence | class | reason |
|---|---|---|---|---|
| 33 | `are fitted at $+0.007\pm0.017$\,dex (0.4$\sigma$).` | E1 (CFG55) | **REQUIRES-CORRECTION** | With each galaxy's own JAM-calibrated stellar mass the rule leaves +0.046 ± 0.018 dex (2.6σ, both footings; 1.9σ under a Hernquist convention; 2.5σ without NGC 7457). On the same 16 galaxies SLUGGS's population masses still give +0.007, so the change comes from the masses, not the subsample. Also lines 84 and 93. |
| 115 | `\textbf{One galaxy disagrees.} UGC 2487 is one massive S0 with a measured rotation curve.` | E1, E5 (CFG42, CFG58), E6 (CFG51), E2 (CFG61) | **REQUIRES-CORRECTION** | The rule now also misses SLUGGS with dynamical masses (2.6σ), M31 LVD (−2.67σ) and the LV field dwarfs (−3.47 / −2.70σ). It over-predicts cleaned Boötes I and Tucana II, and cannot make KiDS's colour split. |
| 107 | `The score therefore stays at 42/48, inferred rather than established` | E5 (CFG42, CFG45), E15 | **REQUIRES-CORRECTION** | The rule flips two harness gates: the MW ultra-faints pass (−0.41σ) and M31 LVD fails (−2.67σ). The 48 gates were never re-scored with the rule, so the count may stay at 42 only by trade (unverified). |
| 104 | `\textbf{KiDS:} the isolated lenses [Bro21] carry no debris.` | E2 (CFG61), E3 (CFG67) | **SOFTEN** | True, and it is why the rule cannot make KiDS's early/late split. The split rejects B with or without the rule at χ² 28.1/7 (a reported χ² row; the frozen amplitude test was degenerate), and ΛCDM reproduces it through the same machinery (6.5/7). |
| 27 | `The fluid first builds the law's phantom, and any leftover stays as collapse debris with the collapse profile.` | E5 (CFG45), E10 (CFG44, CFG50) | **SOFTEN** | The sum is one of four zero-parameter readings, and none passes all seven gates. 'The fluid builds the phantom' has no dynamical origin (Gap 2 is a scoped no-go), so 'derived' in the title overstates. |
| 27 | `No constant is added, but the collapse mass must be \emph{measured}.` | E4 (CFG59, CFG62) | **SOFTEN** | No universal debris fraction works (SLUGGS φ ≥ 0.81, M31 LVD φ ≤ 0.30, X-ray φ ≈ 2.15), and no one-variable split does either. Keeping the rule needs per-population retention. |
| 30 | `\item every star-forming spiral is left on the law;` | E7 (CFG40, CFG56) | **SOFTEN** | f_ex = 0 in all 23 super spirals, but the law under-predicts the nine fastest by +0.164 dex (2.34σ, marginal), and the rule cannot help. |
| 120 | `Massive passive disks ($\log M_*>11.2$) with extended HI or tracer kinematics must rotate faster than the law at large radii` | E8 (CFG41, CFG53) | **SOFTEN** | Now run on four S0/S0a: they sit on the law, −1.25σ against the rule combined; undecided, and the stellar-mass floor caps any shape test at 1.9σ. |
| 120 | `The rule also inherits the programme's standing tests: Gaia DR4 wide binaries (2 December 2026) and $a_0$ at $z\approx2.5$.` | E9 (CFG52, CFG54) | **SOFTEN** | The z ≈ 2.5 test cannot be run on data on disk. It needs 2–4 new JWST IFU plus ALMA discs with mass calibration of about 0.1 dex. |
| 84 | `The law leaves them $+0.080\pm0.024$\,dex short (3.3$\sigma$), worst in the most massive (M87 $+0.28$).` | E1 (CFG55), E16 (CFG57) | **STILL-STANDS** | Strengthened: with dynamical masses the deficit is +0.097 (4.0σ), so it is not the IMF. Hot gas is the one untested escape (CFG57, frozen). |
| 26 | `with $\kappa=\tfrac12$ fitted, not derived [Z26a]` | E13 (CFG47) | **STILL-STANDS** | The Unruh / de Sitter route is retired; κ stays fitted. |
| 49 | `With these it passes 42 of 48 harness gates (lane CFG19).` | E15 | **STILL-STANDS** | No harness row of B (the law) changed; the new failures lie outside the 48. |
| 78 | `the X-ray ellipticals half-close ($+0.125$/$+0.122$\,dex, 1.0$\sigma$);` | E4 | **STILL-STANDS** | Reproduced; full closure would need φ ≈ 2.15 (CFG59). |
| 79 | `UGC 2487, would rotate $+0.14$\,dex faster than observed.` | E8 | **STILL-STANDS** | Still +0.139 dex; four more S0/S0a lean the same way. |
| 112 | `\textbf{The data do not favour the framework over $\Lambda$CDM.}` | E1, E3 | **STILL-STANDS** | Reinforced (CFG55, CFG67, and CFG69 from another session). |

## PAPER37 — the complete-action obstruction map

`qwen_claude_field_theory/papers_2026/PAPER37_complete_action_obstruction_map_2026.tex`: draft, NOT deposited.

| line | quote (verbatim) | evidence | class | reason |
|---|---|---|---|---|
| 22 | `version 1 (brought up to date through CFG65 and the ChainCert Profile module)` | E2 (CFG61), E4 (CFG62), E3 (CFG67) | **REQUIRES-CORRECTION** | CFG61, CFG62 and CFG67 are missing, while the body already cites CFG66. |
| 29 | `is short or marginal on a further list of rows that we give with their committed sizes` | E2, E1, E15 | **REQUIRES-CORRECTION** | The failure list omits the KiDS colour split (28.1/7, a reported χ² row; B-specific per CFG67) and row 1.20 SLUGGS as FAIL (law 4.0σ, rule 2.6σ). |
| 345 | `no scored result is committed` | E2 | **REQUIRES-CORRECTION** | No longer true: CFG61 (3c03f9678) and CFG67 (f1df7889a). |
| 158 | `A gate that is varied as an action term is unstable: its second variation lands on the field it reads (DE12, DE13)` | E11 (CFG48 G6 + referee) | **REQUIRES-CORRECTION** | Stated without condition. A nonlocal enclosed-mass baryon gate is stable on 48/48 (referee 96/96); the real divide is locality (local gates are unstable on 44/48). This also contradicts the paper's own line 164. |
| 256 | `The rule trades B's largest failure for a smaller one in $\sigma$ (1.8--2.7$\sigma$), spread over more objects` | E5 (CFG58), E1 | **REQUIRES-CORRECTION** | The LV field dwarfs are at −3.47σ (the paper's own line 274) and SLUGGS at 2.6σ with JAM masses, so the new cost nearly equals the 3.8σ removed. |
| 277 | `the maps' only constraint is qualitative: a partial debris that vanishes where the phantom supplies the mass and survives where it does not` | E4 (CFG62) | **REQUIRES-CORRECTION** | CFG62 split on exactly this variable at every threshold: 0/20 splits work (0/18 without X-ray); φ is non-monotonic in mass; X-ray needs φ ≈ 2.15. |
| 29 | `calibrated on the galaxies' own inner kinematics it leaves the SLUGGS early types 2.6$\sigma$ short` | E1 | **SOFTEN** | CFG55 also reports 1.9σ under the Hernquist convention and 2.5σ without NGC 7457. |
| 29 | `Gaia DR4 wide binaries (2~December 2026), which can separate B only from the bare MOND law` | E2, E3 | **SOFTEN** | The KiDS colour split already tests B on data in hand (a reported χ² row; CFG67 makes it B-specific). The same issue appears at lines 337 and 345. |
| 113 | `The ultra-faints (1.09) are the failure the programme's own lane README calls B's largest standing one` | E1, E2 | **SOFTEN** | The law on SLUGGS with dynamical masses (4.0σ) now exceeds the ultra-faints (3.8σ), and the KiDS split is ~3.7σ (reported). |
| 161 | `the maximal-ball functional finds the edge with no new constant` | E11 (referee 35eebbe99) | **SOFTEN** | Against B's committed r_ta the ball's edge sits at 0.11–0.24 r_ta, below B's window. |
| 256 | `The debris would have to switch off where the phantom already supplies the observed mass: a design constraint on T5's max rule` | E4, E5 (CFG45) | **SOFTEN** | The max reading passes only 4/7 gates, and no threshold on the phantom/collapse ratio works (CFG62). |
| 259 | `(S) passes 6/7 and fails only the classical satellites (M31 LVD $-2.67\sigma$)` | E1, E5 | **SOFTEN** | With JAM masses SLUGGS also fails (2.6σ), and CFG58 adds the LV field dwarfs (−3.47 / −2.70σ). |
| 287 | `the most massive early types want nearly all of it` | E4, E1 | **SOFTEN** | The X-ray ellipticals need φ ≈ 2.15, φ is non-monotonic, and with JAM masses SLUGGS likely needs φ > 1 (an inference, not recomputed). |
| 164 | `So Gap~1's obstruction is not stability; it is Gauss, history and the exchange's reaction.` | E11, E15 (row 5.02) | **STILL-STANDS** | Matches the referee-reproduced G6 result. |
| 109 | `The one clean pass of B's derived rule (SLUGGS) did not survive dynamical stellar masses` | E1, E15 | **STILL-STANDS** | Matches CFG55. |
| 139 | `\emph{No committed action produces candidate B.}` | E15 (row 5.01) | **STILL-STANDS** | Matches. |
| 103 | `the nine fastest are $+0.164$\,dex ($2.34\sigma$)` | E7 | **STILL-STANDS** | Exact. CFG68 (the ΛCDM control) is in progress. |
| 274 | `The blind, non-exempt versions for NGC1052-DF2/DF4 and the tidal dwarfs fail under both the law and the sum` | E5 | **STILL-STANDS** | Matches CFG58. |
| 339 | `\emph{It cannot be run on the data on disk}` | E9 | **STILL-STANDS** | Matches CFG52 and CFG54. |

## PAPER35 — hierarchical ownership and Gaia DR4

`qwen_claude_field_theory/papers_2026/PAPER35_hierarchical_ownership_dr4_2026.tex`: draft, NOT deposited.

| line | quote (verbatim) | evidence | class | reason |
|---|---|---|---|---|
| 123 | `A draft amendment fixing the mapping of the frozen cuts onto those tables is prepared` | E15 (row 4.06) | **REQUIRES-CORRECTION** | Amendment 15 (the table mapping) was FILED (9f60163d3). Amendment 16 is a draft and not filed. |
| 27 | `The rule adds no constant and removes one, the Solar-System screening length.` | E11 (CFG48), E12 (CFG49) | **SOFTEN** | True only as a prescribed label: history inside an action is acausal; every local gate is ON at the Sun; the ball gate needs a smoothing width and misses B's edge window; a local gate scalar needs two new constants. The effective Cassini pass stands. |
| 28 | `the combined target law passes 42 of 48 harness gates. It fails two:` | E1, E2, E7, E15 | **SOFTEN** | The count stands, but the law now also fails SLUGGS with dynamical masses (4.0σ), the super spirals (2.34σ, marginal) and the KiDS colour split (a reported χ² row). |
| 28 | `the Milky Way's ultra-faint satellites (3.5--3.8$\sigma$ once refereed` | E6 (CFG46, CFG51) | **SOFTEN** | This figure is on uncorrected dispersions. Binary corrections lower each dispersion by 0.07–0.10 dex, but do not remove the offset. |
| 29 | `A local virial theorem explains the phantom's shape` | E10 (CFG44, CFG50) | **SOFTEN** | The identity is reproduced and Lean-certified, but no dynamics produces that state; it survives only by postulating the BTFR or the anisotropy. |
| 103 | `so KiDS does not prefer either model.` | E2 (CFG61), E3 (CFG67) | **SOFTEN** | Holds for the combined stack. On the early/late split, B fails (28.1/7, a reported χ² row) and ΛCDM, through the same machinery, fits (6.5/7). |
| 129 | `It is read as a state of the framework's own field, not a new particle` | E10, E15 (row 5.11) | **SOFTEN** | Gap 2 is a scoped no-go; no action derives this state. |
| 80 | `It is a real failure, smaller than first quoted.` | E6 | **STILL-STANDS** | Seven of eight corrected offsets stay positive; cleaned Boötes I is +0.22 (2.46σ) and Tucana II +0.47 (3.63σ). |
| 36 | `No natural construction on the vacuum gives $\kappa=\tfrac12$ (lane k05).` | E13 | **STILL-STANDS** | The Unruh route is retired. |
| 66 | `NGC\,1052-DF2 / DF4 & $0.0\sigma$ / $0.8\sigma$` | E5 (CFG58) | **STILL-STANDS** | The passes rest on ownership; the blind versions fail. |
| 130 | `The Milky Way's ultra-faint satellites are not explained.` | E5, E6 | **STILL-STANDS** | The rule's closure costs M31 LVD and over-predicts the corrected data. |
| 131 | `The programme's surviving covariant action has an obstructed region gate.` | E11, E12, E15 (row 5.01) | **STILL-STANDS** | Sharpened: no action produces B. |

## PAPER34 — the kernel-blind dark sector

`qwen_claude_field_theory/papers_2026/PAPER34_kernel_blind_dark_sector_2026.tex`: DEPOSITED v2, DOI 10.5281/zenodo.22984587; the on-disk source is v3 (not deposited), and every flagged line is identical at the same line number in v2.

| line | quote (verbatim) | evidence | class | reason |
|---|---|---|---|---|
| 31 | `Two kernels blind to the large-scale field are built from actions.` | E11, E12, E15 (row 5.02) | **SOFTEN** | True only with the switch prescribed. When varied, the V0 region gate fails; a stable varied gate is either nonlocal or needs two untied constants. |
| 156 | `A switch that reads the baryons and their phantom, $U=C\nabla^2(\Phi-v)$, or the baryon density leaks exactly nothing.` | E11 (CFG48 G6) | **SOFTEN** | The no-leak claim is untested, but as a varied local term this reading is DE12's gate, which is unstable on 44/48. The same issue appears at line 264. |
| 31 | `at its own external field it reproduces isolated MOND on KiDS` | E2 (CFG61), E3 | **SOFTEN** | Unsure of scope: CFG61 rejects a colour-blind MOND law on the early/late split. PAPER34's KiDS passes use the combined sample, and its own constructions were not scored on the split. |
| 262 | `each derived from an action, with their field equations checked symbolically for prescribed switches` | E11, E12 | **STILL-STANDS** | Explicitly scoped to prescribed switches. |
| 155 | `The phantom is a divergence, so it is cancelled at each region's edge` | E11 (CFG48 G1) | **STILL-STANDS** | Matches CFG48's Gauss lemma (referee-reproduced). |

## PAPER33 — the khronon route

`qwen_claude_field_theory/papers_2026/PAPER33_khronon_route_2026.tex`: DEPOSITED v2, DOI 10.5281/zenodo.22967954.

| line | quote (verbatim) | evidence | class | reason |
|---|---|---|---|---|
| 135 | `What survives is a completion in which the phantom is generated by the baryons` | E11, E10, E15 (row 5.01) | **SOFTEN** | Gap 1 (a baryon-reading, owned, bound-only switch) is a scoped no-go, and no committed action produces B. That this line refers to candidate B is the reader's interpretation. |
| 135 | `the dark matter is a separate component invisible to the kernel. That route is being built elsewhere in the programme.` | E10 (CFG44), E4 | **SOFTEN** | Gap 2 is a scoped no-go, and the derived cold-mass rule has lost its SLUGGS pass and is not a one-variable law. |
| 126 | `The relation stops being a coincidence between two constants: $a_0$ and the vacuum energy become two coefficients of one function.` | E10 (CFG43), E15 (row 5.13) | **SOFTEN** | The a₀–Λ tie is a declared input; CFG43 writes it into an action only by postulate (tied, not derived). |
| 33 | `makes $a_0=\kappa c\sqrt{G\rho_\Lambda}$ an identity of the action, with $\kappa=2\sqrt{8\pi}/(3\beta)$; this is algebra, and $\kappa$ is not derived.` | E13 | **STILL-STANDS** | κ stays fitted. |

## MNRAS manuscript v2 — the galactic acceleration scale and the cosmological constant

`qwen_claude_field_theory/papers_2026/mnras_submission_2026_v2/mnras_a0_lambda_v2.tex`: revised 2026-09-25, NOT submitted.

| line | quote (verbatim) | evidence | class | reason |
|---|---|---|---|---|
| 613 | `three at 0.13 dex or four at 0.20 dex decide between constancy and the halo-emergent rise at 20:1 once intrinsic and halo-to-halo scatter are included.` | E9 (CFG52) | **SOFTEN** | The 20:1 treats the mass-scale error as independent per galaxy. A shared calibration error does not average down: a correlated 0.2 dex caps the significance near 2.3σ at any N, so the shared calibration must reach about 0.1 dex. Also lines 562 and 583. |
| 30 | `specify the deciding measurement: two to four lensed rotators at $z\simeq2.5$ with baryonic accelerations below $0.3a_0$, each measured to $0.10$--$0.20$ dex.` | E9 | **STILL-STANDS** | CFG52 reaches the same 2–4 discs. |
| 612 | `Existing high-redshift rotation curves decide nothing; directly measured gas masses are the lever.` | E9 | **STILL-STANDS** | Pooled z ≥ 1.5 data are absorbed by a selection mock; PHIBSS gives N = 0. |
| 590 | `\emph{The coefficient is not derived.} We know of no derivation of $\kappa=1/2$.` | E13 | **STILL-STANDS** | The Unruh route is retired. |
| 356 | `The likelihood ratio between $\kappa=1/2$ and $0.461$ from the two together is $e^{-0.02}$: the data do not distinguish them at all.` | E14 (97f30b36c) | **STILL-STANDS** | Like-for-like on H₀ the two coefficients are indistinguishable; keep any '2.2σ' claim out. |
| 609 | `Separating $1/2$ from $0.461$ needs 2.6 per cent.` | E14 | **STILL-STANDS** | Unsure: E14's 2.2σ rests on a clustered statistical error with the gas mass scale held fixed; one sentence would pre-empt a misreading. |

## Notes

- **Provenance of E2's 3.7σ.** It is CFG61's reported χ² row, evaluated after the first run; the frozen amplitude statistic was degenerate, and H1/H2 failed as coded (LEDGER CFG61-note, 9a466c46c). CFG67 shows the failure is specific to B's mass-independent dark mass: ΛCDM fits the split through the same machinery.
- **Readers' uncertainties are marked "Unsure" in the reasons.** PAPER33 line 135 is read as candidate B's completion; PAPER34's KiDS scope; the MNRAS 2.6-per-cent sentence.
- **Out of scope but noted.** `campaign_fresh_gravity/CFG4_galaxy_law.out` has uncommitted working-tree deletions (another session's interrupted re-run). It is not evidence here, but it is the SPARC lane both PAPER35 and PAPER36 cite.
- **Nothing was edited or deposited.** Correcting or depositing any paper is the owner's call.

κ = ½ and Ω_c h² stay fitted. Nothing here says the theory is closed.


## Corrections, 2026-09-29, after a referee sweep and CFG57 (appended; the rows above are unchanged)

- **E4 needs the acceptance level.** "No universal debris fraction φ, and no split by one variable" holds at the frozen 1σ-per-population acceptance.
  - At 2σ, CFG59's ten populations share φ in [0.52, 0.71] (canonical) and [0.33, 0.66] (alt).
  - With CFG71's dynamical SLUGGS, the 2σ intersection is empty only because of SLUGGS (2.6σ at φ = 1).
  - Source: CFG75, e17cf2cf8.
- **PAPER36 line 27** ("No constant is added, but the collapse mass must be measured"). Its reason, "No universal debris fraction works", takes the same qualifier. The class stays SOFTEN: with dynamical SLUGGS masses no common φ exists even at 2σ, and at 1σ the populations pull apart (SLUGGS φ ≥ 0.81, M31 LVD φ ≤ 0.30).
- **E3 (CFG67) is about the difference.** Standard halos reproduce the early-minus-late difference. In the same machinery, ΛCDM's absolute profiles fail too: 29.6 and 27.9/7, and 45.8/15 over all 15 bins (p = 5.7e-5).
- **E16 has run.** CFG57 (9b071a024; data d409c19be) is non-diagnostic by its frozen map.
  - On the seven SLUGGS galaxies with X-ray profiles, the measured hot gas moves the law's mean by 0.010 dex (+0.163 → +0.153 ± 0.028, 5.4σ). That is below the mean's error.
  - The frozen headline "pass" is an extrapolation artefact.
  - In the PAPER36 line-84 row, "Hot gas is the one untested escape" should now read: the measured hot gas is too small to matter; only gas beyond the X-ray fields is untested (above all M87's, whose GCs reach 109 kpc against a 30-kpc field). That row stays STILL-STANDS.


## Addendum after CFG76 (appended 2026-09-29; the rows above are unchanged)

- **E1 and every row that cites it.** The SLUGGS 4.0σ (alt 3.65σ) and 2.6σ are statistical errors at a fixed GC density slope, γ = 3.
  - CFG76 (276c78784, post hoc) finds the law's offset zero at γ ≈ 1.83 and the rule's at γ ≈ 2.45.
  - Without the four group and cluster centrals (N = 12), the law is at +0.055 (2.7σ) and the rule at +0.026 (1.3σ).
  - No class changes. The REQUIRES-CORRECTION items replace a superseded 0.4σ, and that still holds, but any corrected text should carry the γ qualifier.
- **E1's sample.** h50's name-key artefact dropped NGC 720 and NGC 821. With the keys corrected (`CFG55_h50_keyfix.py`), the JAM sample of 17 gives law +0.0996 (4.3σ) and rule +0.0513 (2.9σ).
- **CFG55's README errors** (the kernel, the distance wording and the undefined Salpeter row) are corrected in its appended section. No audit class depends on them.


## Corrections at adoption (appended 2026-09-29; the rows and addenda above are unchanged; this addendum supersedes them where they differ)

- **E3 and the E2 provenance note** ("specific to B's mass-independent dark mass"): the KiDS early/late lensing split is B-SPECIFIC relative to the ΛCDM comparator, for the early-minus-late difference only. It is shared by any model whose predicted difference at fixed g_bar is negligible, NOT by every colour-blind model (a colour-blind Moster halo fits it at 6.9/7, CFG67). It is robust to the repo's own jackknife covariance (4.4σ in the 1-halo bins, CFG88 ef7c1d303) and to a twice-stricter isolation (4.1σ, amplitude 0.97 ± 0.19, CFG96 d2e97eb53); reduced but not removed by B's own stellar-mass calibration (2.8σ released / 3.6σ jackknife, CFG95 7214b5c62); fragile only to systematics a jackknife cannot see. The law's χ² is the zero-model χ² (CFG77).
- **PAPER36 line 103** ("CFG68 … is in progress"). CFG68 is done: ΛCDM also misses the nine fastest (+0.121, 2.26σ), so the row is SHARED. The number stands, but the failure is not specific to B.
- **PAPER36 line 113** ("the ultra-faints … B's largest standing one") is stale.
  - After CFG55 (SLUGGS 4.0σ with JAM masses, 4.3σ key-fixed, at γ = 3) and CFG88 (KiDS 4.4σ with the jackknife covariance), the ultra-faints (3.8σ) are not the largest.
  - The ultra-faint gate is non-discriminating against ΛCDM (CFG69, CFG73, CFG74).
- **E5 and the rows quoting M31 LVD −2.67σ:** it depends on the error recipe, −2.67 / −1.74 / −1.97 / −1.49σ (CFG91 abb698467).
- **E10, "a barotropic cap is excluded":** a scoped, convention-dependent screening result, with a window from about 11× up to 10⁴–10⁵ in mass (CFG43 README).
- **E9 and the a₀(z) rows** (CFG90 0137d584d):
  - PHIBSS's N = 0 is a knife-edge on an assumed velocity radius.
  - CFG52's pooled z ≥ 1.5 result depends on excluding one +1.14-dex object.
- **"Independent" re-derivations** check the arithmetic and the shared inputs, not the model.


## Addendum after CFG110 (appended 2026-09-29; the rows above are unchanged)

- **E2 and E3 (the KiDS split):** Within colour classes the KiDS 1-halo lensing signal shows no detectable dependence on stellar mass. B's mass-independence gives 22.2/14 (p 0.075) and the colour-split ΛCDM 25.2/14; the two are not discriminated (power 8.8, below the declared 9). The colour-blind Moster ΛCDM is rejected (105/14). So, relative to the colour-blind ΛCDM, B and ΛCDM each fail one KiDS test; relative to the colour-split ΛCDM, the colour split stays B-specific. The signal depends on type, not on mass within a type. All of this is at the re-measurement's jackknife errors; satellites and calibration systematics are not covered (CFG110 2f05b5303). The reading that B gets the mass-independence right rests on a non-detection in a power-limited test.


## Addendum after CFG111 (appended 2026-09-29; the rows above are unchanged)

- **E1 and the rows citing it:** With each SLUGGS galaxy's published GC density slope in place of the fixed γ = 3, the law's JAM-calibrated deficit stays at 3.6σ (alt 3.2σ; 2.2σ without the four centrals). The slopes come from Alabi+2017's literature relation, γ 2.49–3.43, verified against its Table 1. The γ that would null the massive centrals is far below their published values: NGC 4365 needs 1.06 against 2.56, and no γ ≥ 1 nulls M87. So the γ caveat does not rescue the law. B's derived rule fits with the same slopes: 1.55σ (alt 1.64σ), and −0.66σ with population masses. Isotropic orbits are assumed (CFG111 6e1b04092).


## Correction after CFG100 (appended 2026-09-29; the rows above are unchanged)

- **E2 and E3 (the CFG110 addendum above):** CFG100 (a51dfe756) is an independent re-derivation of CFG110 and reproduces every headline: B 22.20/14 (p 0.0746), colour-split ΛCDM 25.16, colour-blind Moster 105.04, power 8.77. It corrects the reading in three ways. (1) 'B gets the mass-independence right' is not supported; only a non-rejection is. The 14-dof test has power 0.41 against ΛCDM-size mass dependence and 0.11 against half of it. The sharper 1-dof amplitude is A = 0.33 ± 0.34, so ΛCDM-size dependence is disfavoured at about 2σ (statistical only) and half of it is not excluded. Read: B is not rejected, and ΛCDM-size mass dependence within a class is disfavoured at about 2σ. Likewise 'not on mass within a type' means no detectable dependence at this power. (2) B and the colour-split ΛCDM are not discriminated. B's p ranges from 0.005 to 0.08 across the mass-split edges, and the order flips: B is better at q25/q75, ΛCDM at q40/q60. Dropping late-class bin 9 makes ΛCDM beat B (p 0.88 vs 0.31). The power of 8.8 against the threshold of 9 is razor-thin (10.35 with pair weights). (3) Only the colour-blind Moster rejection is robust: it holds through the bin set and ×1.5 errors. Its size is not robust: χ² 49–230 for M* ± 0.1 dex, and 79 with M200m. It also rests on the Moster mapping as coded. The jackknife has no photo-z, intrinsic-alignment or satellite terms.


## Addendum after CFG112–CFG114 (appended 2026-09-29; the rows above are unchanged)

- **E1 and the rows citing it, SLUGGS, GC orbits and the joint degeneracy (CFG113 1db2d3a69, CFG114 2a83f369e). At the published slopes, any constant GC anisotropy in the measured range (β −0.5 to +0.5) leaves the law's deficit at 3.4σ or more (alt 2.9σ), and no β < 1 nulls it. But with slopes and orbits varied together, it falls below 2σ at the corner where both are favourable: every γ_i − 0.4 with β = +0.5 gives 0.6σ (alt 0.1σ). That corner is more radial than any measured GC system. The deficit exceeds 2σ in 23 of the 25 cells (alt 21). The rule is conditional in the opposite corner: it fits in 13 of 25 cells and fails wherever the slopes are 0.2 or more steeper than published (2.1–3.5σ). So SLUGGS alone cannot make either reading clean. Measured GC slopes and anisotropy for M87, NGC 4365, NGC 4374 and NGC 5846 would decide it.**
- **Claims that the derived rule has, or lacks, SLUGGS support:** CFG111–CFG113 qualify the line 'The derived rule has no clean support left'. With published GC slopes the rule fits SLUGGS on its own (1.55σ with JAM masses, −0.66σ with population masses), and it keeps fitting for isotropic or radial GC orbits (0.56σ at β = +0.5). But one debris fraction still does not fit all ten populations at 2σ: SLUGGS's window [0.77, 1] misses the other nine's [0.23, 0.71] by 0.06 in φ (alt 0.11), with the M31 LVD binding (CFG112 670356510). That NO is fragile. It opens if every γ_i is lowered by 0.2 or with SLUGGS's population masses, and radial orbits were not tested in it. The line's clause 'not with dynamical SLUGGS masses' therefore stands, narrowly. The 1σ NO and the satellite failures do not depend on SLUGGS.


## Addendum after CFG104–CFG106 (appended 2026-09-29; the rows and addenda above are unchanged)

- **SLUGGS (row 1.20 / E1) and the derived rule's support:** (1) **CFG104** (independent re-derivation of CFG112) reproduces it exactly. Its reading: the NO is a boundary, not a conflict. All ten populations share a φ at 2.07σ (alt 2.09σ) against the 2σ line, and at 2.62σ with γ = 3. Only SLUGGS and the M31 LVD are in tension. The result is a knife edge: every γ_i shifted by −0.1 opens the ten-set, and +0.1 empties SLUGGS's window. The other nine populations are CFG71's committed rows. Read 'not with dynamical SLUGGS masses' as 'only at 2.07σ with dynamical masses and the published slopes'.
- (2) **CFG105** (independent re-derivation of CFG113) reproduces it; the only difference is at β = 0.9 (0.036σ, the grid-edge bias R7 bounds). It adds that the constant-β result assumes the power-law tracer extends to infinity. With the tracer cut off at 50 or 20 R_e, radial orbits worsen the deficit: 3.38σ becomes 3.97σ and 4.98σ at β = +0.5. An Osipkov–Merritt profile with r_a = 3 R_e (β → 1 outside) on an infinite tracer removes it (−0.8σ). So the outer tracer slope matters as much as β. The rule's 2.06σ at β = −0.5 is fragile to leave-one-out.
- (3) **CFG106** (independent re-derivation of CFG114) reproduces it: 23/25 and 21/25 law cells above 2σ, 13/25 for the rule, the corner at 0.586σ. It checked against printed targets, not blind. h50's solver truncates the line-of-sight integral at u = 6, which biases σ_pred by up to 0.57% at the corner. The slopes are one relation shifted coherently, so the law's 2σ failure is only as firm as the unknown correlation of the relation's two coefficients. With 1000 draws, the fraction with the law below 2σ is 4.6% (β = 0) and 21% (β = +0.5) at ρ = −0.99, and about 43–47% at ρ = 0. The corner is a mean cancellation on the box boundary: six galaxies are still under-predicted by more than 0.05 dex, and M87 would need γ ≈ 1.6. A 20% error inflation takes 23/25 to about 21/25.
- (4) **The slopes are 3-D.** Alabi+2017 define γ as the slope of the de-projected GC number-density profile, as checked in the paper's arXiv HTML on 2026-09-29. So the Jeans solution's ρ ∝ r^−γ uses it as intended; the case of projected slopes, which would put SLUGGS at +5.6σ at φ = 1, does not arise. The 'published slopes' are one mass relation, γ = clip(−0.63 log M* + 9.81, 2, 4) (2.49–3.43), not per-galaxy measurements.


## Addendum after CFG115 (appended 2026-09-29; the rows and addenda above are unchanged)

- **The KiDS rows (E2/E3; next to gate 3.05):** CFG115 (e469ab0b1; criteria e416f3bea) splits each class into colour tertiles (June LePhare u − r). At fixed g_bar the KiDS colour dependence is not a sharp step at the red/blue valley: the tertiles on either side of u − r = 2.0 are equal (−0.049 each). A step that is constant within each class is rejected (χ² 18.1/4, p 0.001), and a linear colour gradient fits (6.3/4). But the within-class variation sits in the boundary tertiles (outer contrasts p 0.20), which is what colour noise blurring a true step would produce. The power for a gradient of the class-difference size is 4.8, below 9, so by the frozen map the lane is non-discriminating between a blurred step and a gradient. B's null gives 36.3/5 with a free offset. The descriptive models, none of which include colour noise, give: colour-split ΛCDM's sharp class step 21.1/5, colour-blind Moster 12.2/5. The colour dependence remains B's specific failure; this changes its shape, not its existence.


## Addendum after CFG107 (appended 2026-09-29; the rows and addenda above are unchanged)

- **The KiDS colour structure (CFG115):** CFG107 (a027a5fac; the Opus chat's independent re-derivation) reproduces CFG115's numbers. The step-vs-gradient result is weaker than 'step rejected' reads, for four reasons. (1) Fragile to error inflation: the jackknife has no photo-z, intrinsic-alignment or satellite terms. The step rejection reaches p = 0.05 with errors inflated ×1.38, and the gradient-over-step preference with ×1.82. B's null itself (36.3/5 with a free offset) reaches p = 0.05 at ×1.81. (2) A step blurred by at least 0.2 mag of colour noise fits about as well as the gradient (χ² 7.4/4 at σ = 0.20, p 0.12). The boundary equality L3 = E1 is equally a blurred step. (3) Signal versus a colour-dependent systematic is mostly undecidable with the staged product. The gradient survives mass and redshift matching (β_w 0.58 ± 0.18). It is not confined to large radii, and the two redshift halves differ by only 1σ. Mimicking it with mass-to-light alone would need a colour-dependent stellar-mass bias of about 0.9 dex, which is implausible for mass-to-light alone but not for combined mass-to-light, photo-z and satellite systematics. (4) Quote only free-offset χ² for the model rows. The zero-offset rows under the jackknifed reference (the frozen R1 and R5) measure normalisation against a near-null covariance direction, not physics. The power is 4.47 or 4.80 depending on which class-difference reading is used; both are below 9.
- Supplement (CFG107, exact): the colour-split ΛCDM zero-offset row under the jackknifed reference is 22.7 with an all-lens reference and 77.7 with CFG115's class-mix reference. A −0.006 dex normalisation shift spans that range, so no zero-offset row under the jackknifed reference should be quoted. The power row's 4.8 uses the class-level amplitudes, β_true = (A_E − A_L)/(u_E − u_L); the step-fit reading gives 4.465. After mass and redshift matching, the gradient slope is 0.46 ± 0.11 (β_w 0.58 ± 0.18). The LePhare colour errors are not in the staged files, so the blur cannot be measured. CFG107's independence stops at the sum level: the staged product is checked only against the June file, to 3.1e-11. One CFG107 control, K4a (BFGS vs the normal equations, 1.95e-6 against a frozen 1e-8), failed as frozen; it is an optimiser limit.


## Addendum after CFG116 (appended 2026-09-29; the rows and addenda above are unchanged)

- **The KiDS rows (E2/E3; next to gate 3.05):** CFG116 (1ab67b216; criteria e4083bd4f): the KiDS early/late split passes both standard lensing systematics nulls. Cross shear (B-mode): the early−late cross difference over the 1-halo bins is 5.3/7 (p 0.63), and each class's cross profile is consistent with zero. A systematic carrying half of the split would have given χ² ≈ 9, so class-dependent B-mode systematics at about 50% or more are disfavoured. Source separation: near and far background sources give consistent splits (5.4/7, a weak test), and the split persists with far sources alone (23.2/7, p 0.0016). Near-source dilution (~0.1 dex) is similar for both classes. The 'fragile only to systematics a jackknife cannot see' caveat narrows to E-mode-only shape errors, lens photo-z beyond CFG110, satellites beyond CFG96, and unmodelled covariance (CFG107's ×1.8).


## Addendum after CFG108 (appended 2026-09-29; the rows and addenda above are unchanged)

- **The KiDS nulls (CFG116):** CFG108 (6e7cbdec2; the Opus chat's independent re-derivation) reproduces CFG116's numbers. Its independence stops at the staged sums: the near/far assignment and WX's content inside the staging cannot be re-checked there. It makes four corrections. (1) R0's '9' and '2.2' are non-centralities λ, not expected χ²; the expected χ² is 7 + λ (16.0 and 9.25). (2) The power is overstated. The cross null has only 32% power at ε = 0.5 (α = 0.01); 80% power needs ε ≈ 0.74 (omnibus) or 0.57 (shape-matched). The near/far null is essentially blind to near-only systematics: power 0.07 at ε = 0.5, A_nf = +0.03 ± 0.29. So read 'excluded only for ε ≳ 0.6–0.75, and only for E~B-type leakage', not 'disfavoured at 50% or more'. (3) Calibrate p-values by permutation; the χ²₇ tails are anti-conservative (permuted 99th percentile ≈ 20.5, not 18.5). The far-only split's empirical p is 0.0055, not 0.0016. Random 51% lens subsamples of the all-source split reach χ² ≥ 23.2 with probability 0.39, so the far-only value is not merely a smaller-N fluctuation. The near and far splits are dependent, not independent confirmations. (4) The amplitudes use a pooled-ESD ratio per class, log10(Σ_K1 WG / Σ_K1 WW), early over late; a fixed-pair-weight reading misses the far amplitude by 0.007. Passing both nulls does NOT exclude: E-mode-only class-dependent errors (a multiplicative shear bias would need 51%; a class-dependent baryonic-mass or g_bar-assignment offset would need about 0.5 dex, the largest untested avenue); lens photo-z (a 0.24 offset would be needed through Σ_crit; class-dependent outlier fractions are untested); satellites (the isolation flags were not read); and covariance ×1.8 (the all-source split reaches p = 0.05 at ×1.58, and inflating it destroys the nulls' power too). CFG108's own frozen control K8c failed: a mis-specified 90% threshold, observed 64%.


## Addendum after CFG140 (appended 2026-09-29; the rows and addenda above are unchanged)

- **a₀(z), the decisive test:** CFG140 (KURVS-CDFS, z ≈ 1.5; the first on-disk sample in the decisive regime, g_bar/a₀ = 0.06–0.67 at the outermost measured point): NON-DIAGNOSTIC over the declared brackets, because the answer turns on the unmeasured outer pressure support. With the observed rotation velocity, a strict lower bound on the circular speed, a₀ ∝ H(z) over-predicts the outer accelerations in every gas and stellar-mass cell (−3.2σ to −9.6σ, corrected by the SPARC anchor), and flat a₀ is never disfavoured. With the Burkert constant-σ asymmetric-drift correction, flat a₀ under-predicts in 21 of 24 cells and the rival is never disfavoured. A KROSS z ≈ 0.85 same-pipeline control suggests that correction over-corrects at these radii. What settles it: an outer dispersion profile or a pressure-free tracer, and measured gas. With both, the test has 3–5σ statistical power, subject to CFG52's correlated floor of about 2.3σ.


## Correction to the CFG140 addendum (appended 2026-09-29)

- CFG140 correction (logic; the orchestrator's check). The observed velocity is a lower bound on the circular speed, because pressure support only raises V_c. A lower bound can exclude only a model that predicts V_c below V_obs. Under P0 both readings predict at or above the observed accelerations in every cell (the largest P0 Δ′ is −0.035 for flat and −0.196 for the rival), so the bound excludes neither. The P0 rows are the NO-PRESSURE-SUPPORT SCENARIO (V_c = V_obs), not a bound in the excluding direction. 'a₀ ∝ H(z) over-predicts in all 24 cells' holds only if the outer pressure support is zero; it means the rival needs substantial outer pressure support to survive. 'Flat a₀ under-predicts in 21 of 24 cells' holds only in the constant-σ Burkert scenario (P1); it means flat a₀ needs the outer pressure support well below that level. Neither reading is excluded by the data alone. The frozen verdict (NON-DIAGNOSTIC), the anchor, the KROSS control, the power row and the MUTATE are unchanged.


## Addendum after CFG141 (appended 2026-09-29; the rows and addenda above are unchanged)

- **a₀(z), the decisive test:** CFG141 (KURVS with each galaxy's MEASURED outer dispersion, read from the paper's plotted σ(R)): the outer σ does not fall (σ_out/σ₀ median 1.05, range 0.70–1.13), so the constant-σ pressure correction is supported by data. With it (the isothermal self-gravitating layer with the local σ), flat a₀ under-predicts the outer accelerations in 21 of 24 cells, and survives only if these z ≈ 1.5 discs hold about 4× their stellar mass in cold gas, which is unmeasured. At the paper's own 40% molecular fraction it under-predicts by 0.39 ± 0.07 dex. The rival a₀ ∝ H(z) needs nearly as much gas. The frozen reading is NON-DIAGNOSTIC. Its testable content: flat a₀ requires total cold gas of about 4 M* in KURVS-like discs, and a measured μ ≤ 1.5 would disfavour flat a₀ at z ≈ 1.5 under this correction. The fixed-scale-height variant softens this (flat disfavoured in 16 of 24).

## Correction to the CFG141 addendum (appended 2026-09-29)

- CFG141 wording correction (the orchestrator's check). (1) Under P2 BOTH readings under-predict at realistic gas: at the paper's 40% molecular fraction (μ = 0.67) Δ′_flat = +0.39 ± 0.07 and Δ′_H = +0.24 ± 0.06, and both survive only at μ = 4 (flat 3 cells, the rival 6). So the P2 excess is not evidence against flat a₀ in particular: either both readings need about 4 M* of cold gas, far above the paper's and PHIBSS-type molecular fractions (about 0.4–0.6), or the P2 dispersion model over-corrects. The rival sits 0.12–0.16 dex closer in every cell, about half the gas bracket; under P3 at the paper's gas flat is 3.5σ high and the rival 1.3σ. (2) The pressure term dominates V_c at R_max (V_c²/V_obs² 1.5–6.1), so the result rests on the dispersion model at 4–7 R_d (anisotropy, thickness, non-equilibrium untested), where beam smearing and pressure support are debated. (3) σ_out/σ₀ ≈ 1.05 shows σ does not fall; it does not validate the isotropic isothermal layer. (4) 'About 4 M* of cold gas' is a requirement of the P2 model, for either reading, not a prediction of the framework. (5) CFG140's KROSS caution is narrowed, not removed: a falling outer σ is ruled out as its cause, and the P1 differential (+0.27 ± 0.07) is unexplained. The verdict (NON-DIAGNOSTIC) and every number are unchanged.

## Addendum after CFG117 (appended 2026-09-29; the rows and addenda above are unchanged)

- **The ten doors, door 2 (Verlinde):** CFG117 (door 2 of the ten doors, Verlinde's emergent gravity; criteria b09ca1480, gates 5ef77ea09; lane bb504274c): a scoped NO-GO on G1. Verlinde's apparent dark mass, M_D² = (a_V r²/G) d(M_B r)/dr with a_V = cH/6, misses the CFG44 target's shape in all 16 cases (4 masses × point mass or exponential sphere × H₀ or H_Λ), with the target evaluated at a₀ = a_V. For a point mass C_V/C_target = (1 + x)/x exactly: 11 at x = 0.1, 2 at x = 1, 1.10 at x = 10; the spheres give 10–16 at x = 0.1 and 1.8–8.6 at x = 1. The cause is structural: Verlinde's point-mass dark density is r⁻² all the way in (the linear sum g = g_N + √(a_V g_N)), the target's is r⁻¹ inside r_M (the quadrature sum g = √(g_N² + a₀ g_N)). They share only the deep limit and approach it as 1/x, and the total field differs by up to √2 (at x = 1), not only the dark density. The failure lies inside Verlinde's own onset regime (his eq. 1.3). The normalisation is not the problem: κ_V = √(8π/3)/6 = 0.482 with H_Λ (a_V/a₀ = Z/6 = 0.965) and 0.583 with H₀, both within 2σ of both fitted κ windows. Other gates: G2 and G3 UNDEFINED (no perturbation equations, no action); G4 PASS as a count only; G5 FAIL (Hees, Famaey & Bertone 2017: the weak-field formula misses the planets' perihelion advances by seven orders of magnitude). Untested: Hossenfelder's covariant Lagrangian, later formulations, non-spherical systems. MUTATE (the target's own cold mass) passes 16 of 16: informative.

## Corrections after the round-3 documentation audit (appended 2026-09-29; AUDIT-T 64084d046, a00ed3de1; append-only, no result changed)

- **E5, the PAPER36 bullet ('One galaxy disagrees'), and rows 115, 256 and 259 (the LV field dwarfs at −3.47 / −2.70σ):** the −3.47σ (alt −2.70σ) is in S's own shrunken error (a ddof = 0 scatter and a fixed-halo Υ floor). With Υ propagated into the halo it is −1.75 to −2.1σ at the declared Υ_V = 2, −1.37σ at Υ_V = 1 (S = −0.055 dex) and −4.64σ at Υ_V = 4 (S = −0.147 dex). In the law's own error the change is −1.4σ. The size of the S offset is robust only at Υ_V = 2. 'S switches off above M_b ≈ 2.3e7' holds only within a window: for M* = M_b/2, S is off from 2.3e7 to about 2.2e11 M☉ and f_ex turns on again above that (CFG35's massive-spiral failure); for M* = M_b the window is 5.6e7 to 8.4e10 M☉. CFG92 was written with CFG91's code in view (restructured), so its independence is partial. Row 256's 'the new cost nearly equals the 3.8σ removed' holds only in S's own error; the corrections those rows require stand, but the LV significance quoted in them is recipe-dependent.
- **E7 and rows 30 and 28 (super spirals, 2.34σ):** the failing clause, the nine fastest (+0.164, 2.34σ), is selected on v_obs, the offset's own numerator. Under a no-trend null the selected nine exceed the sample mean by +0.071 ± 0.016, against +0.059 observed (P = 0.77; CFG89, post hoc). So the clause adds almost nothing beyond the all-23 mean (1.67σ), and the unselected trend test is the slope clause, 1.80σ. A +0.1 dex stellar-mass shift alone passes H2 (nine fastest at 1.91σ).
- **The addendum after CFG104–CFG106:** 'alt 2.09σ' should read 2.08σ: CFG104's alt value is 2.0846 (canonical 2.0667, i.e. 2.07σ, unchanged).

## Addendum after CFG119 (appended 2026-09-29; the rows and addenda above are unchanged)

- **The ten doors, door 7 (a fuzzy-dark-matter soliton):** CFG119 (door 7 of the ten doors, a fuzzy-dark-matter soliton with the baryons in its potential; criteria b09ca1480, gates 5ef77ea09; lane 435cb43e9): a scoped NO-GO on G1, on both footings. The Schrödinger–Poisson ground state cannot reproduce the target for any boson mass on the grid (10⁻²³ to 10⁻²⁰ eV), even with the soliton mass free per galaxy. The closest single galaxy (m = 10⁻²³ eV, the 10⁹ M☉ exponential sphere) misses by 4.0 dex against a ±0.04 dex band; the best single m, 10⁻²³ eV (best for every mass), misses its worst galaxy by 1.2 × 10⁵ dex. The ground state is cored where the target rises as 1/r, and falls exponentially where the target falls as r⁻²; no core width can pass (an analytic remark; lighter m not run). Other gates: G2 FAIL for every m on the grid (growth within 5% to 30/Mpc needs m ≥ 1.28 × 10⁻²⁰ eV, from Hu, Barkana & Gruzinov's fit); G4 FAIL (m is a new constant); G3 and G5 pass as statements. Control C1 fails as frozen and is kept: the exact ground state departs from Schive's fitting formula by up to 6.3% at 2.7 r_c, the fit's tail accuracy, not the solver's (an independent referee shooting script reproduces the ground state to every printed digit). MUTATE (the target's own density) passes H1: informative. Untested: the excited-state envelope, which is NFW-like in simulations and behaves as cold dark matter (door 6's question).

## Correction after CFG109 (appended 2026-09-29; the rows and addenda above are unchanged)

- **The KiDS split, satellites:** CFG96 (the isolation test), after CFG109 (b7d41c302; the Opus chat's independent re-derivation, which reproduces every printed number): read 'robust to a twice-stricter isolation' and 'satellites, as removed by this isolation, do not drive it' as: the split persists under stricter photo-z isolation (4.1σ, amplitude 0.97 ± 0.19), but it does not differ from the full split within errors (difference of splits 8.75/7, p 0.27, δ = +0.009 ± 0.350), and the test is not powered to exclude a satellite contribution below ε ≈ 0.3–0.45 of the split at complete removal (0.6–0.9 at 75% removal). The removal fraction is undetermined, because the windows are photo-z proxies. The split's significance is fragile to error inflation (W20 reaches p = 0.05 at errors × 1.51). CFG109's independence stops at the staged sums and the isolation flags; four of its controls failed as frozen, one of them (a biased group-permutation null) unresolved.

## Addendum after CFG118 (appended 2026-09-29; the rows and addenda above are unchanged)

- **The ten doors, door 6 (secondary infall):** CFG118 (door 6 of the ten doors, spherical secondary infall of cold matter onto a baryon core with shell crossing; criteria b09ca1480, gates 5ef77ea09; lane d0baef700): a scoped NO-GO on G1, on both footings. In a 1-D shell code (20,000 shells, Planck18 from z = 100, a static core, three angular-momentum brackets), the infall profile's C/C_target falls with radius in all 24 runs: 4–360 at x ≈ 0.1 for the spheres, 0.8–5.6 at x ≈ 1, and 0.05–0.21 at x ≈ 28. Even the best bracket is off by a factor of about 30 somewhere. The cause: too much cold mass inside r_M and too little outside (the cumulative mass is 1.0–4.2× the target's at x ≈ 1 and 0.28–0.66× at x ≈ 28, stable to resolution). The infall's radial scale follows the turnaround (∝ M^0.33) rather than r_M ∝ M^(1/2), so no single set of constants serves every mass. C1 and C2 (Bertschinger's −9/4 slope, −2.238) pass. C3, the resolution check of the local bins, fails and is kept; the cumulative mass converges, and H1 fails at both resolutions. MUTATE (the target's own density) passes H1: informative. G2, G3 and G5 pass as statements (plain CDM and Newtonian gravity). Untested: non-spherical collapse, mergers, a growing core, feedback, other angular-momentum distributions.

## Addendum after CFG142 and CFG160 (appended 2026-09-29; the rows and addenda above are unchanged)

- **a₀(z), the decisive test:** (1) CFG142 (c64865b33; GOODS-ALMA 2.0 1.1-mm dust continuum, criteria frozen before the cross-match): NON-DIAGNOSTIC for the sample. None of the ten KURVS discs is detected, and only KURVS-11 is powered at the survey's depth. It excludes the P2 gas requirement as an approximate point-source limit: dust-traced μ < 0.72 at the nominal calibration, < 1.44 with gas-to-dust × 2. That holds only if its dust is compact against the 0.45″ beam; the rms is the survey average. (2) CFG160 (ff3d9ea7d; the simulation-calibrated pressure-support factor of Kretschmer et al. 2021, VELA at z = 1–5, frozen before any number): at the pre-declared decision cell (μ = 0.67, the paper's molecular estimate; δ = 0; canonical) the rival a₀ ∝ H(z) fits (Δ′_H = −0.006 ± 0.044) and the framework's flat a₀ is 3.3σ high (Δ′_flat = +0.144 ± 0.044). By the frozen map that is a Kretschmer-conditional lean toward the rival, the first in-regime reading in this record whose central value favours it. It is not robust and not a kill. At μ = 1.5 it flips (flat +1.2σ, rival −2.1σ); at the calibration's α × 0.6 (its 40% scatter) and at R_e = 2 R_eff the cell is non-diagnostic; flat is disfavoured in 14 of 24 cells, not all. The KURVS a₀(z) test now turns on two measurable quantities: the outer pressure support at 2–4.5 R_e, and the total cold gas.

## CFG160 governing wording (appended 2026-09-29; the orchestrator's check; it governs the CFG142/CFG160 addendum above)

- Under the simulation-calibrated (Kretschmer+2021) pressure correction, the pre-declared decision cell (μ = 0.67) leans toward a₀ ∝ H(z) at 3.3σ. It is conditional, not robust and not a kill: it flips with gas (at μ = 1.5 flat is +1.2σ and the rival −2.1σ); it moves within the calibration's 40% scatter (α × 0.6 is non-diagnostic); and it rests on ONE published calibration, adopted after CFG141's P2 result was known (a forking-path risk). The GOODS-ALMA limit (μ < 0.72 nominal) is a point-source approximation, and no total gas is measured. The decisive quantities are the outer pressure support at 2–4.5 R_e and the total cold gas. The decision cell was fixed with the CFG141 grid already known. At that cell a confirming result for flat a₀ would have been Δ′_flat within 2σ with Δ′_H below −2σ (for example α × 0.6 gives +1.3σ / −2.0σ); a disconfirming result is Δ′_H within 2σ with Δ′_flat above +2σ, which is what occurred; anything else is non-diagnostic. Nothing here is evidence against flat a₀ beyond this statement. CFG140's and CFG141's rows are not superseded: they stand as the P1 and P2 results. An independent re-derivation (CFG165, the Opus chat) is pending, and this wording holds until it reports.

## CFG160 after CFG165 (appended 2026-09-29; the rows and addenda above are unchanged)

- **Headline: a weak, normalisation-dependent lean; not a detection.** CFG165 (33b446ef3), the Opus chat's independent re-derivation, reproduces CFG160's decision cell (flat +0.147 ± 0.044, rival −0.003 ± 0.045; the 0.003 gap is inc_sfr_deg against inc_star_deg) and every sensitivity row, and corrects how the lean reads. (a) 'The first in-regime reading favouring the rival' does not survive on CFG160's own map: P3 at the same cell already reads lean rival (CFG141's committed values: flat +3.5σ, rival +1.3σ), and P3 is lean rival in 12 of 24 cells against P4's 14 (both counts checked here from the committed JSONs). The accurate statement is that P4's rival central value sits at zero. (b) The lean depends on the normalisation, not the α shape: all 8 alternative shapes with median α within ×[0.75, 1.25] keep lean rival; flat's Δ′ drops below +2σ at s = 0.71, and the class flips to lean flat by R_e/R_eff = 3 (CFG165). (c) Break-even total gas: μ = 2.14 for flat and 0.65 for the rival. The lean holds only below about 1.2 M*, and at the repo's total-gas median (μ ~ 4) both laws over-predict (CFG165). (d) x runs from 1.04 to 3.54, inside the calibration range. The README's 'the three largest residuals (KURVS 13, 17, 21) have the largest x' is wrong: the largest x are KURVS 21, 8 and 17 (checked here), and KURVS-8 has the lowest residual. (e) With gas and α as nuisance parameters the likelihood ratio falls from about 130 to 0.5–1.7, and P(lean rival | flat true) is 0.31–0.45, against a frozen requirement below 0.05: weak evidence, not a detection (CFG165). (f) KROSS through the same P4 pipeline, anchor-corrected at μ = 0.67: flat −0.004, rival −0.082 (−4.1σ), the opposite of KURVS; KURVS − KROSS = +0.151 ± 0.045 (CFG165), reproduced by CFG161 (9ff8e369a: +0.148 ± 0.044, 3.3σ from flat, 1.7σ from the rival; CFG161's outcome was not blind). (g) CFG165's independence stops at CFG4_common, CFG140's set-up choices, and Kretschmer's α(x) as quoted (unverified literature); its MUTATE M6 (σ_out permuted) did not bite and is kept.

## Addendum after CFG161–CFG163 (appended 2026-09-29; the rows and addenda above are unchanged)

- **a₀(z), the decisive test:** The headline is unchanged: a weak lean that depends on the normalisation and the gas; not a detection. (1) CFG161 (9ff8e369a; its criteria are blind, its outcome is not, as disclosed): under P4 the KURVS − KROSS differential lands on the rival by the frozen rule (+0.148 ± 0.044, 3.3σ from flat's 0 and 1.7σ from the rival's +0.072). P4 does not manufacture evolution; P1–P3 do. But at a common gas fraction, flat fits KROSS (z ≈ 0.85; rival −4.1σ) and the rival fits KURVS: neither law fits both, and the gas evolution between the two epochs is the untested lever. This is a consistency statement about P4, not an a₀ verdict. (2) CFG162 (250250ed3): a map, not a verdict. At the decision cell, flat is preferred for outer pressure support below s_mid = 0.67 × Kretschmer's α (bootstrap 0.51–0.85), and the rival above it. Every published prescription (Kretschmer 1.00, Dalcanton & Stilp 1.42, fixed height 1.62, Price n = 1 1.69, self-gravitating 3.00) sits above s_mid at the paper's molecular gas. The crossing moves with gas (1.11 at μ = 1.5, 2.39 at μ = 4). So, given the literature, the test reduces to the total cold gas: flat fits for μ ≈ 2.1–3.7 and the rival for μ ≈ 0.6–1.7. (3) CFG163 (5b7b4517c): KURVS-15 is not detected in the archival 1.32-mm dust continuum. Its dust-traced gas is below 1.90 M* at the nominal calibration (below 3.8 with gas-to-dust × 2). For this one disc that is below flat's P4 break-even at the nominal calibration, and it does not reach the rival's. It is a gas-prior statement, not an a₀ test.

## Addendum after CFG164 (appended 2026-09-29; the rows and addenda above are unchanged)

- **a₀(z), the gas prior:** CFG164 (bf1e27b2e; a measured gas prior from PHIBSS, Tacconi+2013, the 17 z- and M*-matched rows, frozen before any gas value): NON-DIAGNOSTIC at Kretschmer's correction. The molecular-only prior puts the KURVS sample-median μ at 1.01 (0.60–1.69), 68% of it in the rival's window. The decision cell at s = 1 is lean rival 0.55, lean flat 0.21, both 0.24 (below the 68% bar); under the stronger published corrections (s = 1.42–1.69) it is lean rival 0.70–0.81. Not robust: HI equal to the molecular gas turns s = 1 into lean flat 0.59; extrapolating the gas–mass relation to KURVS's lower masses (8 of 10 discs lie below PHIBSS's range) splits it; the α_CO bracket spans it. Across the declared priors P(lean rival | s = 1) runs 0.11–1.00. The measured prior narrows the question but does not settle it; the decisive measurement remains the KURVS discs' own gas at a depth reaching μ ≈ 1, and HI at z ≈ 1.5.

## CFG164 after CFG166 (appended 2026-09-29; the rows and addenda above are unchanged)

- **Wording: the gas prior gives a weak lean toward the rival, uncertain by a factor of about 2 and reversible by HI; read with CFG165, it is weak evidence, not a detection.** CFG166 (ea66f9f17), the Opus chat's independent re-derivation, reproduces CFG164: 57 of 57 pass lines; counts 73/51/17/38; primary median μ 1.025 (0.604–1.719), 68% rival and 7.6% flat; at s = 1, lean flat 0.210, rival 0.540, both 0.245; the HI, mass-scaled (slope −0.219) and ULIRG rows. The largest class gap, 0.018, is Monte Carlo at N = 4000. (a) Extrapolating to lower mass: by the frozen rule the verdict is driven by the extrapolation, but only just (the P(lean rival) span is 0.202 against the 0.20 line). The mass slope is −0.22 ± 0.20 with a permutation p of 0.28, i.e. undetermined (checked here: −0.219 ± 0.196, p = 0.27). Carrying that uncertainty lowers lean rival from 0.54 to 0.34; a per-disc nearest-mass prior gives 0.52–0.55 (CFG166). (b) The redshift exponent implied by the data in the repo is 0.23 ± 0.52 (checked here, with the mass term, on all 51 clean rows), inconsistent with the 2.5 declared in Variant Z. The z ≈ 1.2 and z ≈ 2.2 PHIBSS samples are selected differently, so neither number is a clean evolution measure. The CO-detection bias cannot be tested, because no flagged row has z in the window; a bounding run moves lean rival to 0.43–0.62 (CFG166). (c) Window edges: the frozen stability line fails narrowly (5 of 105 near-frozen windows miss ±0.12, the worst by 0.199, all with z_hi = 2.5). There is no sign of tuning toward a class, and lean rival is the modal class in 97% of 317 windows (CFG166). (d) The marginalisation does not depend on its definition: bootstrap and lognormal draws differ by at most 0.013 (CFG166). CFG166's controls M1 and M3 did not bite, and are kept. Disclosed here: CFG164's HI rows (h = 0.5, 1) are not exact rescalings of the h = 0 draws, because one sequential random stream was used, so each HI row carries its own Monte Carlo noise (~0.01–0.02).

## Addendum after CFG170 (appended 2026-09-29; the rows and addenda above are unchanged)

- **a₀(z), the two-epoch gas ratio:** CFG170 (fdbdcf323; criteria 1caae1adb frozen before any break-even): NON-DIAGNOSTIC. Both laws need the cold-gas fraction to rise about threefold between KROSS (z ≈ 0.85) and KURVS (z ≈ 1.5). At s = 1.42–3.00, flat needs 2.97–3.10 and the rival 2.60–3.57, only 0.01–0.06 dex apart; at s = 1, flat needs 3.3 [2.0, 5.7] and the rival 11.9 [1.6, open]. The in-repo PHIBSS bracket (1.00, 2σ [0.73, 1.39]) disfavours both laws, and the abstract-level literature bracket (2.02 [1.61, 2.42]) disfavours neither. Two epochs do not break CFG162's pressure–gas degeneracy.
