# EUC21R (BLIND RE-GRADE OF EUC21: THE GAS LANE ESZ1 ON THE MASK-APERTURE STELLAR MASS): RESULT

Written before EUC21's own result was opened. Labels per row and footing (canonical / alt):

| Row | Word under the corrected mass | Against the committed word | Brackets F1a / F1b |
|---|---|---|---|
| **Y1** Part G lane word | **ONLY A CUSP IS LEFT / ONLY A CUSP IS LEFT**, no tag (all five of ESZ1's brackets give the same word) | **UNCHANGED / UNCHANGED** | **ROBUST / ROBUST** |
| **Y2** Part C word | **WIDE LENSES HOLD MORE GAS PRESSURE**, no tag (the CIB-deprojected map gives the same word); the same on both footings, since Part C uses no a₀ | **CHANGED / CHANGED** (committed: NO EXCESS DETECTED [BRACKET-DEPENDENT: CIB-deprojected map]) | **ROBUST / ROBUST** |

All frozen checks pass (R0 rule self-test, H0 harness byte for byte, H1 on all five runs, H2, H3, H4) and the twin
bites. No amendment was needed. Neither row is a pass, and Y2 says nothing about law S: it compares the gas
pressure of wide lenses with that of matched small lenses.

**In one paragraph.** Correcting the catalogue's stellar mass to the whole Sérsic body makes the wide lenses heavier
(median +0.148 dex) and roughly halves the hot gas law S would need from an extended body. The two cored bodies
are still excluded by their own pressure, now at 10 to 64 σ instead of 19 to 114 σ, so Part G does not move. The
Part C word moves because the controls are matched on stellar mass. The corrected masses pick a different set of
controls (only 15 of the 237 wide lenses keep their control), and that set's stack is lower: −2.14 against −0.34.
The wide lenses' own stack does not change. The committed word sat at the line (lower bound −0.20), and every mass
reading run here, the twin included, puts that bound above zero.

2026-11-14. Reading note `4265063117` (committed alone, before any code or number); code, runs and this result in the
following local commit. kappa = 1/2 FITTED. Footings graded separately, never pooled. Adopts nothing; not pushed.

## Numbers

Units: 10⁻⁶ arcmin² of integrated Compton-y in ESZ1's 2′ compensated aperture. Corrected (committed).

| | canonical | alt |
|---|---|---|
| Wide lenses stacked | 237 (237) | same |
| Measured stack | +3.825 ± 1.471 (identical to the committed value; H4) | same |
| B30 least predicted stack | 21.59 (37.18): 12.1 σ (22.7) above, f_T 0.31 (0.18) → EXCLUDED | 18.56 (32.41): 10.0 σ (19.4), f_T 0.36 (0.21) → EXCLUDED |
| B100 least predicted stack | 98.22 (171.30): 64.2 σ (113.8), f_T 0.069 (0.040) → EXCLUDED | 82.18 (144.60): 53.3 σ (95.7), f_T 0.082 (0.047) → EXCLUDED |
| G2 least predicted stack | 1.21 (2.03), below 3σ = 4.41 → NO POWER | 1.07 (1.86) → NO POWER |
| Wide lenses that need no gas at all (least setting) | 27.4 % (4.6 %) | 31.6 % (8.0 %) |

"Least" is ESZ1's least demanding setting: far source, stars 0.10 dex above Salpeter, zero pressure at the gas edge.

- **Median gas law S needs (least setting):** B30 8.3 / 5.6 × 10¹² M☉ at 0.72 / 0.71 keV (was 2.2 / 1.8 × 10¹³);
  B100 1.9 / 1.2 × 10¹³ M☉ at 1.12 / 1.07 keV (was 5.4 / 4.4 × 10¹³); G2 1.4 / 0.9 × 10¹² M☉ at 0.38 keV (was
  3.2 / 2.8 × 10¹²).
- **Salpeter stars (far, b★ = 0):** B30 30.9 / 26.7 (48.6 / 42.8); B100 141 / 118 (227 / 194); G2 1.71 / 1.54
  (2.54 / 2.36).
- **Central source (z_s = max(2, z_l + 0.5)), b★ from +0.10 to −0.10:** B30 65 to 106 / 58 to 96 (97 to 134 /
  88 to 124); B100 307 to 516 / 266 to 454 (470 to 672 / 412 to 599); G2 4.2 to 6.0 / 4.0 to 5.8.
- **ESZ1's five brackets on the corrected mass** (lane word recomputed by ESZ1's rule; the same on both footings in
  each): CIB-deprojected map +4.36 ± 1.91, B30 / B100 / G2 canonical 21.6 / 98.2 / 1.21; θ_d 1.5′ +1.49 ± 1.02,
  14.4 / 61.7 / 0.96; θ_d 3.0′ +7.19 ± 2.95, 27.4 / 132.9 / 1.28; grade A only (141) +4.52 ± 1.88,
  13.5 / 56.7 / 0.99; z_l ≤ 0.6 only (154) +1.27 ± 2.03, 30.5 / 140.7 / 1.53. All read ONLY A CUSP IS LEFT.
- **The correction itself:** −log₁₀ f has a median of 0.148 over the 237 wide lenses (16–84 %: 0.072 to 0.265) and
  0.063 over all 6,173 lenses of S (0.007 to 0.168).

### Part C (Y2)

| Run | Primary map: mean difference, wide minus control [95 %] | CIB-deprojected map | Word |
|---|---|---|---|
| committed | +4.17 [−0.20, +8.67] | +7.12 [+2.12, +12.16] | NO EXCESS DETECTED [BRACKET-DEPENDENT: CIB-deprojected map] |
| **corrected** | **+5.97 [+1.43, +10.29]** | +6.91 [+1.54, +12.16] | **WIDE LENSES HOLD MORE GAS PRESSURE** |
| F1a (R_e × 0.80 in f) | +4.59 [+0.60, +8.89] | +6.04 [+0.96, +11.20] | same |
| F1b (R_e × 1.25 in f) | +5.92 [+1.58, +10.28] | +7.30 [+1.80, +12.77] | same |
| twin `invert` (lm + log₁₀ f; not graded) | +5.30 [+1.15, +9.47] | +5.77 [+0.47, +10.62] | same |

Controls under the correction: 237 pairs, median |Δz| 0.020 (0.010), median |Δ log M★| 0.076 (0.069); wide-lens
median log M★ 11.90 (11.72), control median 11.72 (11.59). Control stack −2.14 ± 1.64 (−0.34 ± 1.64); on the
CIB-deprojected map −2.55 ± 2.00 (−2.76 ± 1.89).

### Part D (reported, no word; as the corrected run's code prints it)

The wide-lens row is the measurement and does not move: +3.83 ± 1.47, gas 5.2 × 10¹² M☉ at 1 keV, 2σ limit
8.3 × 10¹² M☉. The limit is now 10.0 mean stellar masses (was 15.8), because the mean stellar mass is larger.
Controls −2.14 ± 1.64 (2σ limit 1.2 × 10¹² M☉, 2.0 M★). The other classes' stacks do not change (their limits in mean stellar masses fall): 1.3–1.7″ +0.42 ± 1.21;
1.0–1.3″ +0.60 ± 0.95; below 1.0″ +0.61 ± 0.44; all valid S +0.76 ± 0.38; L +27.5 ± 4.0.
**Cold-share reading:** median r⁻² component 2.6 / 2.2 × 10¹² M☉. Baryons required at 5.41: 4.8 / 4.0 × 10¹¹ M☉.
That is gas 0 at the median: 67 / 71 % of lenses need none (was 30 / 35 %). Predicted stack 0.145 / 0.128 against
σ = 1.47. The measured stack is above it by 2.5 σ (was 2.4 σ); stated as the criteria ask, not a test of the share.
The full block is in `euc21r_collect.out`.

## Checks (frozen; all pass)

- **R0 rule self-test.** On ESZ1's committed results file my rules return its committed words: Part G ONLY A CUSP IS
  LEFT / ONLY A CUSP IS LEFT, Part C NO EXCESS DETECTED [BRACKET-DEPENDENT: CIB-deprojected map]. The family words
  recomputed from pred_min, measured value and σ agree with the stored ones, in every run.
- **H0 harness** (f = 1, substitution in place): results file and per-lens file byte for byte identical to ESZ1's
  committed files, `.out` identical on every line (no line carried an elapsed time), source exit 0.
- **H1** after each of the five runs: `git status --porcelain --untracked-files=all --ignored` on ESZ1's, EUC1's,
  EUC4's, EUC5's and EUC8's folders and the two mask tables identical before and after; sha256 of every file in ESZ1's
  folder unchanged. A final `git status` on those folders after all runs is empty.
- **H2** (corrected run): K6 fails (median log M_gas 13.23 / 13.13 and 13.60 / 13.49 against 13.44 / 13.37 and
  13.84 / 13.77) and K7 fails (0.34 / 0.39 relative); K1–K5, K8 and K9 pass (K3: B30 0.06 %, B100 0.07 %, G2 0.73 %;
  K8 +78.2 ± 1.9, 41 σ; K9 as committed). The same holds in F1a, F1b and the twin.
- **H3:** for all 6,173 lenses of the per-lens file, (corrected − committed log M★) equals −log₁₀ f, with f
  recomputed by the collector's own code from the mask tables and the catalogue; worst difference 9.8 × 10⁻⁵ (the
  file's 4-decimal rounding).
- **H4:** the wide-lens stack on both maps (N, mean, σ) equals the committed one exactly (relative difference 0).
- **Coverage of the correction:** every one of the 6,173 lenses of S has a mask. There are 6,185 table rows with a
  usable mask and 9 without (none in S). No lens differs between the two tables, and every f lies in (0, 1].
- **Twin `invert`:** B100's least predicted stack rises to 255.8 / 220.5 against 171.3 / 144.6; the driver exits 1.
- The code's own lane words in the corrected runs read NOT EVALUABLE and the source exits 3, as the criteria said
  (its final gate also counts K6 and K7). This lane's words come from the family words and the Part C words
  computed before that gate.

## Reading (mine; not part of the labels)

1. **Y1 is unchanged and robust.** A smaller correction (F1a) or a larger one (F1b) still leaves both cored bodies
   excluded by 8.8 σ or more. The criteria's hand estimate ("roughly half, EXCLUDED by several σ, G2 NO POWER, Y1
   unchanged") holds: B30's least stack falls by 42 / 43 % and B100's by 43 %.
2. **Y2's change is a change of controls, not of the wide lenses.** The wide lenses gain more mass from the
   correction (median 0.148 dex) than the small-separation lenses they are matched to (median 0.063 dex over S). So
   the matching now draws heavier small lenses, and 222 of 237 controls are new. The new control set's stack is
   −2.14, which is negative and so is noise, not gas: 1.1 σ below the old −0.34. That is what moved the difference.
   The committed word sat 0.20 below the line. Every alternative mass reading run here puts it above, the twin
   included, even though the twin moves the masses the other way. So the committed NO EXCESS DETECTED was the
   fragile reading, and the Part C word depends on which controls are drawn more than on the mass correction as
   such. ESZ1's CIB bracket already read an excess.
3. **For the framework:** nothing passes and nothing new fails. Smaller gas bodies are still excluded at
   hydrostatic pressure. The excess pressure in wide lenses over matched lenses, if real, is consistent with the
   richer environments ESZ1 and EUC6 noted, and is not a test of law S.

## Limits

Those of ESZ1 (spherical; hydrostatic; y sees pressure, not mass; photometric lens redshifts; no source redshifts;
radio and dust leakage; a 2′ aperture that takes in neighbours), plus EUC17's premise. The catalogue mass is the
in-mask mass on the paper's text and one lens. M★/f extrapolates the fitted Sérsic wings, and the correction grows
with the share of light outside the mask, which is largest for the wide lenses. Only the F1a / F1b brackets were run
here, as the criteria ask; EUC17's other brackets (n = 4, mask centre, no-mask, n > 9.5) were not run. Part C is a
single draw of controls without replacement. Its word is sensitive to that draw, and the criteria give it no
bracket on the matching.

## Disclosures

- Each run took about 46 s, not the 75 s the brief expected, at 4 threads, nice 19, one at a time.
- Python's warning lines in the five `stderr.txt` logs printed the source's absolute path. I stripped the repository
  prefix from those five files after the runs, before committing. Nothing else in any output was edited.
- The shared side-session notes folder was not opened before this result was committed.

## Files

`READING.md`; `euc21r_run.py` (driver: one substitution, loader wrap, write redirect); `euc21r_collect.py` (rules,
checks, labels); `euc21r_results.json`, `euc21r_collect.out`; `runs/<mode>/` for harness, corrected, F1a, F1b and
invert. Each holds the redirected ESZ1 outputs (`esz1.out`, `esz1_results.json`, `esz1_per_lens.csv`), the driver
record `driver.json`, the per-lens `f_table.csv`, and `stdout.txt` / `stderr.txt`. Inputs: the ECLIPSE files under
`_external_data/euclid_dr1_eclipse/`, and the ACT DR6 y maps and eRASS1 table under
`<repo-parent>/_external_data/act_dr6_nilc/` and `<repo-parent>/_external_data/cfg687_inputs/`.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
