# A5 — the 178 Zenodo records, and the 14 clues the canonical documents do not carry

**Claim.** Every deposit under `creators.name:"Zimmerman, Carl"` was fetched from the Zenodo API
(178 reported, 178 retrieved, 8 pages of ≤25 because unauthenticated paging is capped). 177 are
physics records dated 2026-03-19 to 2026-10-21; 1 is a namesake (2010, wildlife genetics) and is
flagged `not_applicable`. Each record's abstract was reduced to its number-bearing claim sentences
(625 verbatim quote blocks, 2,955 numbers, all checked as substrings of the source) and cross-checked
against the repository (161,566 text files, excluding this lane). **The corpus is not un-mined — 59
records have their distinctive numbers in scripts, result files or ledgers, and 21 more exist as
manuscripts. The residue that matters is that the programme's canonical documents contain almost none
of the October layer: of the 29 records dated 2026-10-01 or later, 13 carry distinctive numbers and
not one of those 13 has a single number in `STANDING.md` or `FRAMEWORK_EQUATIONS_2026-10-15.md`
(101 of 121 October numbers absent).** The 14 clues below are the load-bearing part of that residue.
They are not new physics; they are claims already deposited, with numbers the canonical documents
would have to change.

**Status: NUMERICAL** (an audit result, not a derivation). Nothing here closes a question; it fixes
what each open question is currently missing.

## 1. Method, and what "integrated" means here

- **Fetch.** `GET https://zenodo.org/api/records?q=creators.name:"Zimmerman, Carl"&sort=newest`,
  `size=25&page=1..8`. `hits.total = 178` on every page; 178 unique ids after dedupe. Cached to
  `_zenodo/all_records.json` with per-page SHA-256 in `_zenodo/fetch_meta.json`.
- **Quotes.** Abstracts are HTML; text is normalised by stripping tags, decoding named/numeric
  entities (`&nbsp; &times; &sup2; &radic; &pi;` …) and collapsing whitespace. Every quote in the
  ledger is a **substring of that normalised text** — never retyped (K2). Every number listed against
  a quote occurs inside it (K3). This is the anti-drift contract.
- **Repo probe.** Three fixed-string probes per record: the DOI/bare id, two 4-word title shingles,
  and up to six *distinctive* numbers (≥3 significant digits; numbers used by more than two records
  are dropped as common constants). 952 probes over 161,566 files; 497 hit.
- **State rule** (a retrieval verdict, not a quality verdict):
  `integrated` = ≥2 distinctive numbers in **non-paper** repo files (scripts, results, ledgers,
  standing docs); `paper_only` = mapped manuscript carries ≥70 % of the numbers but <2 appear
  outside manuscripts; `catalogued_only` = DOI appears (README table / deposit metadata) and no claim
  number does; `only_zenodo` = neither; `superseded` = earlier deposit of a later record, or a
  retracted class; `out_of_scope` = separate claim class (therapeutics, plant, aroma, other field);
  `not_applicable` = namesake.
- **Result.** integrated 59, paper_only 21, catalogued_only 53, only_zenodo 6, superseded 19,
  out_of_scope 19, not_applicable 1. Bearing on the four questions: (a) κ/a₀ origin 133 records, (b) medium /
  n=1 vs 2 / saturation 105, (c) lensing / GW / PPN / stability 96, (d) 24 pc–1 kpc 21,
  (e) prediction / kill 142.

The count that is *not* a bookkeeping detail: category (d) is thin. Twenty-one records' claims
mention a pc/kpc/Mpc-scale length at all, but only five carry a number inside 24 pc–1 kpc
(21682494 at 80 pc, 21895046 at 105 pc, 22255522 at 1 kpc, 22967954 at 1–4 kpc, 23533323 at
24 pc–1 kpc), and one of those states a range for L*. That band is where the stiffness length lives;
the corpus has far more to say about Mpc scales than about the single decade that decides the medium.

## 2. The 14 clues, with what each changes and the single test

**Source of every number in this table:** the named record's own abstract, quoted verbatim in
`a5_zenodo_ledger.json` (row `id`, field `claims[].quote`); they are external inputs to this lane, not
recomputed here. The headline counts of §1 and §4 are in `a5_results.json.numbers`.

| # | id | what the record says (verbatim numbers) | Q moved | what it changes | the single test |
|---|---|---|---|---|---|
| 1 | 23171085 | the quadrature tail gives "a constant a0/2 anomaly in the Solar System, **1279** times the Earth-Mars ephemeris bound"; cure `nu_fix` with `y_t`; "every planet passes for y_t <= **7.7e5**"; `Lambda/a0^2 ~ (pi/4) y_t`; `y_t = **128.9**` on κ=1/2, 94–103 for measured a0 | Q1, Q2, Q4 | The canonical n=2 law is **not planetary-safe as written**. The cure adds a second constant and the Λ closure then *defines* y_t rather than deriving κ: the "one-parameter" claim is false in this branch. | Earth–Mars ranging: cured kernel ≤1e-14 m/s² at 1 AU, uncured a0/2 = 4.7e-11 m/s². One year decides. |
| 2 | 23251231 | `Lambda c^4/a0^2 = **73.19**` observed; "with the RAR kernel the integral converges to **12.99**, **5.6** times below"; y_t = **94** (74–120, 1σ); "a Lean proof shows it is independent of the other ingredients" | Q1, Q2 | Λ can be the MOND field's vacuum energy **only** for the quadrature kernel + turn-off. The kernel the repo actually fits SPARC with (RAR/ν_mono) misses by 5.6×. This is an unreconciled kernel conflict, not a small correction. | Compute `(1/2)∫(ν−1)d(y²)` for the repo's canonical ν_mono family: if it converges to ≠73.19, the Λ-as-field-energy identity excludes the repo's own kernel. |
| 3 | 23533323 | "**-89** times the mean cold density at R = 0.2 d"; "**-33** for a cluster pair"; "Prediction: no saddle dip"; "missing depth of **1.9 to 2.1** Msun/pc^2"; "about **twelve** times as many pairs"; "L* lies between **24 pc** … and about **1 kpc**" | Q2, Q4 | A positive-mass tether **cannot** reproduce MOND's phantom near field nulls. The framework therefore predicts a *null* (no saddle dip) where QUMOND predicts a dip of 1.9–2.1 M☉/pc² — a direct, self-contained discriminator between the tether and the law it is supposed to realise. | Stacked lensing of luminous-red-galaxy pairs at ~0.77 Mpc separation; ~12× the pairs of arXiv:1702.08485 for 3σ. |
| 4 | 23532894 | "No complete parent survives"; "slip <= **1.54e-5**"; "vacuum offset **15-25** times the slip bound"; eRASS1 outer shear "Z = **-9.3** canonical, **-11.9** alternative"; law off for "**128 of 175** SPARC galaxies" | Q2, Q3 | There is **no established relativistic parent** for the cold sector. Any canonical statement that the medium is a field theory with a covariant limit is ahead of the record: the best candidate fails its own frozen rule and overshoots cluster shear. | eRASS1 outer shear at R > R500 with the 318 clusters: the construction predicts Z = −9.3 (canonical) / −11.9 (alternative); a measured Z near zero excludes it outright. |
| 5 | 23397365 | source-boost model "about **340 ppm**"; framework `|delta|` below **1e-6** (model **1e-20**); "**30-50 ppm** on the difference" | Q1, Q2 | A table-top experiment separates a source-field-boost reading of MOND from the vacuum-tied framework with no astrophysics. It is the only kill line in the corpus that a single laboratory can execute this year. | Two-configuration Cavendish (source-density swap) at 30–50 ppm: +340 ppm kills the screened framework; <1e-6 kills the boost model. |
| 6 | 23251278 | anisotropic EFE: `Q2 = **2.195e-26** s^-2`, "**6.3 sigma** above the measurement"; wide binaries "gamma_v = **1.20** at 10 kAU and **1.51** at 20 kAU" | Q3 | The data ask for an **EFE-blind** sector, and the price is wide binaries boosted as isolated MOND. That prediction lies **outside both Gaia DR4 arms the repo registered** (Arm A 1.1614–1.1814; Arm B ceilings ≤1.045): the September registration predates this October paper and has not been amended. | Gaia DR4 at 10–20 kAU: 1.51 (EFE-blind) vs 1.19 (Arm A) vs ≤1.045 (Arm B), separated at the repo's own 4.2σ. |
| 7 | 23354043 | capacity `Sigma <= a0/(pi G)` = "**214/258** Msun/pc^2"; galaxies median "~**0.3** of it"; Bullet cores "**3.6-4.8** times it"; "sigma/m <= **0.71** cm^2/g vs a required **0.11-0.82**" | Q2 | The tether **saturates**, and the saturation point is where the one-component reading must fail: cores holding 3.6–4.8× capacity require a second free component. This is a quantitative statement of what "cold energy" must be made of, not a fit. | Free central density in relaxed clusters: the tethered component cannot exceed 214/258 M☉/pc², so any core above it is free component — one resolved lensing + X-ray fit decides. |
| 8 | 23420675 | truncation at the cosmic share excluded: "Delta chi^2 **+197** within 0.31 Mpc, **+753** all radii"; infall fits if `N >= **3-4**`; census `N ~ **6-10**` fits at "**-0.2 / -1.5**"; two-halo term narrows deficit "**+149** to **+11**" | Q2, Q4 | The cold halo has **no edge**, and the natural "each galaxy gets its cosmic share" model is excluded at high significance. Combined with clue 7 this fixes the medium's boundary condition: supply-limited, not truncation-limited. | KiDS-1000 isolated lensing at 0.3–1 Mpc: the two-halo term moves the outer deficit from +149 to +11, so the profile *shape* beyond 0.31 Mpc is the discriminator. |
| 9 | 23482936 | law holds to `g_bar ~ **7e-14** m/s^2` (amplitude **1.016 ± 0.086**); spheroidals "**1.45x** above … (**4.0 sigma** split)"; dwarfs "**+0.44 dex**"; ten mechanisms fail | Q2, Q4 | The law is confirmed at the **lowest acceleration ever tested** and fails exactly where mass is pressure-supported. The anomaly is now a number (+0.44 dex, host-independent) rather than a category, and ten framework-native mechanisms are on record failing it. | A kinematic selector separating rotating from pressure-supported systems at fixed g_bar; five candidates already fail, so the test is a new one on the same sample. |
| 10 | 23372002 | original settling rule "**19-25%** too much power at k = 0.3-1 h/Mpc", `Delta chi^2 = **+68.7**`; condensed-only rule `**+2.03**` | Q2, Q3 | The passing cosmic-shear result is **conditional on an un-derived sourcing rule** (condensed baryons only, per-host catchment). Without it the same engine is excluded. This is a hidden premise, and it is the one the canonical documents never state. | The pre-declared primary run with gas expulsion: if +2.03 degrades past the frozen threshold, the pass was post-hoc selection. |
| 11 | 23396865 | FRB amplitude `B = **1.064**` [1.010, 1.122]; baryon-only BH-ΔE conversion excluded at "**7.8 sigma**" (s_b = 0.70) and "**16.6 sigma**" (0.43); cold-dark conversion "**0.9 sigma**" | Q1, Q3 | If black holes source dark energy, the converted mass **cannot be baryons**. Independent of the ε_req-vs-ceiling argument already in the repo, this closes the baryon channel with 114 localised FRBs and leaves only the dark sector. | A ~200-FRB localised sample at the same host marginalisation: the 30 % baryon deficit is either confirmed or B returns to 1. |
| 12 | 23246734 | "**174,890,804** raw candidates, **42,534,139** distinct values, **82,613** in-window hits, ZERO surviving the false-discovery gate"; realised branching "**4.41**", not 30 | Q1 | Every dimensionless quantity constructible to depth 10 from the framework's germs has been enumerated against 19 targets: **zero survivors**. Any future "κ derived from Z" starts from an empty search space, and the published stopping rule was wrong by a factor 6.8. | Procedural, not experimental: a new κ derivation must state depth, candidate count and FDR gate, and pass the gate that returned zero here. |
| 13 | 23169118 | `a0 = **9.36e-11** m/s^2`; κ "measured **0.551 ± 0.043** … fitted, not derived"; promotion `a0^2(Q) = kappa^2 G (-K(Q))` | Q1 | The programme's own identity says the MOND scale is the dark sector's **pressure**, not its energy density — the one place the origin question is posed as an identification. It also states the measured κ that the canonical docs do not quote. | Measure `w` of the dark sector: a0 inherits it, so a 1 % a0(z) at z ≈ 2 (the registered deep-MOND Tully–Fisher zero point) reads w to δw ≈ 0.006. |
| 14 | 23192441 | "three estimators give kappa = **0.45 ± 0.07**, **0.58 ± 0.18** and **0.43 ± 0.08**"; 1/2 consistent; "**2.1-2.2 sigma**" on the critical density | Q1 | The empirical basis for κ=1/2 is **estimator-dependent** at the 2σ level and degenerate with H₀ and the stellar M/L zero point. "κ=1/2 is selected" rests on this spread; the canonical `0.42 ± 0.10` is a fourth, different number. | An independent stellar M/L zero point: with it the three estimators collapse and the 2.1–2.2σ becomes a real tension or disappears. |

## 3. Three cross-record tensions the repo has not reconciled

1. **Kernel.** The Λ-vacuum identity (clue 2) requires the quadrature kernel; the SPARC fits and the
   RAR use ν_RAR/ν_mono. Both cannot be the theory's kernel. No repo file states which is canonical.
2. **Wide binaries.** The September DR4 registration fixes Arm A at γ_v = 1.1614–1.1814 and Arm B
   ceilings ≤1.045. The October EFE-blind paper predicts 1.51 at 20 kAU (clue 6). The registration has
   not been amended; on the repo's own 4.2σ forecast the two are distinguishable, so one of them is
   not the framework's prediction.
3. **κ.** Four numbers circulate: 0.42 ± 0.10 (FRAMEWORK_EQUATIONS), 0.551 ± 0.043 (clue 13),
   0.45/0.58/0.43 (clue 14), and κ = 1 in the March–May deposits (a0 = cH/Z with Z = 5.789). The repo
   has a κ ledger and a footing rule; it does not have a single reconciled κ.

## 4. Checks

`a5_checks.py` proves, on the cached snapshot: 178/178 fetched (K1); 625/625 quotes verbatim (K2);
2,955/2,955 numbers in-quote (K3); state counts complete (K4); DOI/date/title match (K5); 13 October
records with zero canonical numbers (K6); all 14 clues carry a test and a fingerprint (K7); 178 unique
DOIs (K8); abstract hashes stable, and with `--network` three records re-fetched from zenodo.org are
byte-identical after normalisation (K9); `--mutate` corrupts 73.19 → 73.91 and K2/K3/K7 fail (K10).

## 5. What this does not do

- It does not decide whether any claim is **true**; it records where each one lives.
- The state rule is lexical: a number can appear in a script without the claim being used, and a claim
  can be absorbed in prose without its numbers. `catalogued_only` is therefore a prompt to look, not a
  verdict.
- Abstracts are not papers. A claim quoted here may be weakened, conditional or withdrawn in the
  record's own body; the ledger quotes only what the deposit asserts publicly.
- The 2010 namesake record is included only so the count is honest.

## 6. Next

1. Amend the Gaia DR4 registration (or withdraw the EFE-blind wide-binary prediction) — tension 2 is
   decidable in December and cannot be left with two answers.
2. State the kernel once, in `FRAMEWORK_EQUATIONS`, with the 12.99-vs-73.19 number attached.
3. Put the 14 rows of §2 into the canonical ledger with their kill lines, so the entry point stops
   being 25 days behind the deposits.
