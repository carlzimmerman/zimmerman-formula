# CFG816 FROZEN CRITERIA: scoring the Gaia DR4 R statistic (the CFG800 rule with Amendment 22's σ and scope)

**Status: FROZEN when committed alone (this commit), 2026-10-16, before Gaia DR4 (ESA planned date 2026-12-02, not fixed) and before any DR4 data are read.** After that, never edit it;
any change goes in a new dated file. It implements, as one script, the rule of CFG800 (`CFG800_wb_2026_scoring/FROZEN_CRITERIA.md`, aa71ca510) with the σ and
scope of **Amendment 22** (`prep_2026/gaia_dr4_prep/AMENDMENT22_HASH.txt`, a553a4a66). It changes no frozen number, cut, threshold or sealed file.
It supersedes the dated draft `DR4_R_STATISTIC_CRITERIA_DRAFT_2026-10-15.md` (f1020761b), which is left untouched. κ = ½ is fitted, not derived. The cold mass is still required.
**ID:** the owner asked for CFG810, which was already the H-EX galaxy-scale lensing lane (`CFG810_hex_galaxy_lensing`, criteria 4091eccbc); asked again, the owner chose **CFG816** (2026-10-16).

## 0. Disclosure: what is known about the inputs, and from what
The definitions below were first taken from a fetch-tool summary of arXiv:2602.24035 and are now **checked against the paper's own TeX source**
(`_external_data/cookson2026_arxiv_src/`, untracked; archive `arXiv-2602.24035v1.tar.gz`, SHA-256 `fa27f837f2021c98b3587ca2fd7a892fac573b2c81de844819eb47de8a617f11`,
file `WBQA.tex`, read directly 2026-10-16: the theory, sample-selection, data-analysis, results and discussion sections, lines 255-935). Line numbers below refer to it.
- **Found (confirmed in the TeX):**
  - ṽ = v_sky / √(GM/r_sky) (Eq. 9); v_sky = d_h × (proper-motion difference) plus perspective corrections; both stars at the inverse-variance-weighted common distance; M = the
    pair's total mass from FLAME (about 19% of stars) or M⋆ = 10^{0.0725(M_G,⊙ − M_G)} (Eq. 12); r_M = √(GM/a0) with **a0 = 1.2×10⁻¹⁰ m s⁻²** (Eq. 3), so r_M ≈ 9 kAU for 1.8 M☉
    (my arithmetic); r ≈ r_sky √(3/2) (Eq. 10).
  - Cuts: RUWE < 1.25, parallax uncertainty ≤ 2.5% (C25; 1% in C10), ipd_frac_multi_peak = 0 for both stars, ΔRV < 10 km/s, r_sky ≲ 30 kAU, d_h < 130 pc, ṽ uncertainty < 0.1,
    degrouping, an HR-diagram cut.
  - **The test itself (Results, lines 601-641):** six bins in x = r_sky/r_M, with **bin medians 0.073, 0.153, 0.348, 0.744, 1.419, 3.079** (Table 2, lines 550-566; the edges are not stated); the median ṽ per bin, with uncertainty MAD/√N (measurement errors neglected); a **flat line with free
    normalization** (best fit 0.489) against a MOND curve with a step of about 20% near x ≈ 1 (MLS interpolating function, external field g_N,e = 1.184 a0); χ² with 5 degrees of freedom.
    Table 3: Newton 2.48 vs MOND 15.10 (about 548×) for ṽ ≤ 2.5; about 1501× for the strictest row.
  - **The MOND prediction (lines 255-295):** the median ṽ rises by about 20% (1.7/√2) from x ≪ 1 to x ≳ 1, with any Newtonian normalization ("0.5 → 0.6 as well as 0.7 → 0.84"); a flat trend favours Newton
    "regardless of the particular value". The Newtonian regime is fixed by the first two bins (x = 0.073 and 0.153), "clarifying that the Newtonian normalization must be close to 0.5" (line 605).
  - **Contamination (lines 352-475, 613, 894-931):** undetected close companions and triples raise ṽ (hidden mass lowers the mass estimate; the inner orbit recoils the visible star). The paper
    handles them with cuts, not a fitted fraction, and its main result **assumes that the eccentricity distribution and the incidence of undetected companions do not depend on separation**
    (citing Hartman+2022, Hwang+2022). It says it does not discuss what a suitable forward model for the wide-binary population would be.
- **NOT found, and relevant:**
  1. **A calibrated triple (close-binary) fraction as an input.** CFG800 says to use "a calibrated triple fraction, both as published". Cookson et al. use none: the test is a
     **shape** test (flat against a step) with a free normalization, so contamination that does not depend on separation cancels. The ≈ 50% they cite comes from other work
     (Appendix A.4, A.5). CFG800's clause therefore rests on a misreading of the method and **cannot be executed as worded**; section 3 states what is done instead.
  2. The six bin edges (only the medians are given) and the pairs per bin (they are labelled on Figure 8, a PDF).
  3. (Resolved by the TeX) the earlier worry about unread sections: the discussion of distance and ipd is at lines 894-931.
- **What the source adds that matters here:** contamination by undetected close binaries **does depend on distance**, because companions are harder to detect further out. Cookson et al. show that
  extending the sample from 130 to 150 pc without the ipd cut produces a **fake MOND signal** (MOND 12× preferred), and that adding ipd_frac_multi_peak = 0 turns it into Newton 88× (150 pc) and
  1500× (130 pc) (lines 894-931). That is the separation- or distance-dependent contamination that R can be fooled by, and the reason the ipd cut is in the primary here.

## 1. What is scored, and why R is the right statistic
Cookson's test asks whether the median ṽ stays flat with separation (Newton) or steps up by about 20% beyond r_M (MOND with the external field). **R is that step, as one number.** Any bias
that does not depend on separation (an underestimated mass, a recoil from an undetected companion, a normalization of 0.489 instead of 1) multiplies the inner and outer medians alike and
**cancels in R**. What does not cancel, and what a boost would have to be distinguished from, is contamination that grows with separation (flybys, chance alignments, companions that are harder
to detect at large separation). That is the one place a false R > 1 can come from, and sections 3 and 5 test it directly.

**R** = median ṽ over pairs with x ≡ r_sky/r_M > 1 and s ≤ 50 kAU, divided by median ṽ over pairs with x < 0.3 (the Newtonian regime). CFG800 defined the numerator region
and left the Newtonian-regime normalization undefined; x < 0.3 is registered here (Cookson's median-x bins start at 0.073).
- **a0 for r_M:** 1.2×10⁻¹⁰ m s⁻² primary (the value used in the MOND test literature, so the sample matches the published one); branches 9.36×10⁻¹¹ and 1.13×10⁻¹⁰
  (the framework's two footings). Never pooled.
- **Masses:** the DR4 pipeline's mass for each pair, as in the registered estimator (prereg section 1); not re-fitted here.

## 2. Error, and the three classes (Amendment 22(c), unchanged)
- **What the error means in practice (derived, not frozen).** σ_tot = √(σ_fit² + 0.02²) with σ_fit = 0.019√(30000/N) gives, for N = 1421 / 5000 / 10000 / 30000 / 100000 pairs, σ_tot = 0.090 / 0.051 / 0.039 / 0.028 / 0.023,
  so KILLED needs R ≥ 1.27 / 1.15 / 1.12 / 1.08 / 1.07. CONSISTENT is unavailable at every N (σ_sys alone is 0.02 > 0.005). Cookson's own N = 1421 data (Δχ² = 12.6 for the 20% step) imply a statistical error on the step of roughly
  0.056, so a Cookson-sized DR4 result with R ≈ 1.00 would be **UNDECIDED**, not consistent. MOND (R ≈ 1.20) would be excluded at 3σ if σ_R ≲ 0.067, which needs about 2500 pairs or more. The structure is therefore: the framework can be
  killed, or survive; it cannot be confirmed over Newton by this rule, as Amendment 12(e) already says.
- **σ_R** = the larger of (i) σ_tot = √(σ_fit² + σ_sys²), σ_fit = 0.019 √(30000/N), σ_sys = 0.02 (irreducible), and (ii) R's own bootstrap error (2000 resamples of
  pairs, seed 20261216 as the prereg). **N** = the number of pairs that pass the R cuts, both regimes together, the same convention as the pipeline's N. The value with N taken
  as the numerator subsample only is printed as a sensitivity.
- **KILLED** (meaning: the stiffness construction of CFG740 is killed; Arms A, B, C and the settling model keep their own rows): R − 1 ≥ 0.01 **and** R − 1 ≥ 3σ_R.
- **CONSISTENT:** |R − 1| < 0.01 **and** 2σ_R ≤ 0.01. Unavailable if σ_R > 0.005. Then UNDECIDED (or KILLED).
- **UNDECIDED** otherwise. "Standard MOND excluded" is scored by z = (R − γ_MOND)/σ_R for γ_MOND in 1.15-1.20 (CFG800's range) and for the registered Arm A floors
  1.1614 (canon) and 1.1917 (alt), reported side by side.

## 3. Quality checklist (primary) and branches (never pooled)
- **Primary:** d_h < 130 pc; parallax uncertainty ≤ 2.5%; RUWE < 1.25 both stars; ipd_frac_multi_peak = 0 both stars; ΔRV < 10 km/s where radial velocities exist;
  ṽ ≤ 2.5 (Cookson's loosest row); ṽ uncertainty < 0.1. The ipd cut is in the primary because CFG800 records that dropping it changes Cookson's own preference
  (Newton 88× with the cut, MOND 12× without, at d < 150 pc).
- **Branches (reported side by side):** ṽ ≤ 2 and ≤ 1.5; parallax ≤ 1%; r_sky ≤ 30 kAU (Cookson's limit) in the numerator; **NSS-screened** (reject any pair with a DR4
  non-single-star solution, the prereg's designed contamination detector); each of the three a0 values.
- **Triple fraction (replacing CFG800's undefined clause).** Cookson et al. calibrate none, and none is applied to R. The assumption they do make (contamination independent of
  separation) is tested instead: (a) the NSS-screened branch above; (b) the tail fraction f_tail = P(ṽ > 2) is printed in both regimes (a contamination diagnostic, not a correction);
  (c) the **contamination rule:** if R − 1 meets the KILLED threshold on the
  primary but **not** on the NSS-screened branch, or f_tail differs between regimes by more than its 2σ, the result is labelled **CONTAMINATION-LIMITED, not KILLED**. This makes
  a kill harder than a literal reading of CFG800, and it is the same one-sided logic as the prereg (contamination only raises ṽ).

## 4. What must be reported, always
Raw R, R − 1, σ_R with its two components, N per regime, f_tail per regime, and the distance of R to every registered number (1.000, 1.1614/1.1917, 1.15-1.20), for the primary and every
branch, and next to the prereg's own γ̂ and its arm rows (the two statistics are never pooled or averaged). Never a single verdict word. No cut, branch or threshold may be added after DR4.

## 5. Controls (a failed control is kept, and makes the run NOT DIAGNOSTIC)
- **C1 injection:** synthetic pairs with ṽ drawn from a fixed Rayleigh-like shape at the Newtonian normalization 0.489 and a known factor R_true ∈ {1.00, 1.05, 1.20} applied to x > 1; N
  matched to the real sample. R is recovered within 2σ_R in at least 95% of 200 repeats.
- **C2 coverage:** for R_true = 1.00 the 1σ interval covers the truth in 68% ± 5% of 1000 repeats; the class KILLED fires in < 1% of null repeats.
- **C3 class table:** a table of (R, σ_R) values reproduces Amendment 22's arithmetic: at σ_R = 0.028 KILLED needs R ≥ 1.084 and CONSISTENT is unavailable.
- **C4 DR3 code-path run (needs the owner's yes for the download):** the same script on the registered DR3 sample; Cookson's own qualitative result (no 20% boost) must be
  reproduced, as a check on the code, not the framework.
- **MUTATE:** multiply ṽ at x > 1 by 1.2. The script must return R ≈ 1.2 and the MOND z-test must detect it (exit 1). The output carries the `_MUTATE` tag.

## 6. Scripts, access, running, departures
- **Scripts and outputs:** `cfg816_r.py` (with `--mutate`), `cfg816_r.out`, `cfg816_r_results.json`. Controls C1-C3 and MUTATE run before any DR4 data are read; the script imports the registered pipeline's
  functions read-only and changes no model.
- The DR4 archive is accessed only on the owner's explicit yes, after the volume is stated (the prereg's "sync range fetch" convention). The script is run **once** on DR4. Anything changed after the
  first R is printed is listed under "Departures", with its reason; sections 2, 3 and 4 may not be changed.

## 7. Decisions recorded at freezing (2026-10-16, owner)
1. **ID:** CFG816 (CFG810 was taken; see the status paragraph).
2. **Newtonian regime x < 0.3 and the N convention of section 2** (all pairs that pass the R cuts, both regimes together): accepted as drafted. The owner said "freeze it" after being told these points were open; they were not discussed separately.
3. **CONTAMINATION-LIMITED** (section 3) is accepted in place of CFG800's undefined triple-fraction clause, on the same basis.
4. The bin edges of Cookson et al.'s six bins are not stated in their TeX; this file does not use them (it uses x < 0.3 and x > 1).

## 8. Not claimed
No measurement. A prediction scored by rules fixed in advance. Nothing here says the data favour the framework.
