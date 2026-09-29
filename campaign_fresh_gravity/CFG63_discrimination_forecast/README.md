# CFG63 -- which open test separates candidate B from the bare MOND-type law and from LCDM, and how big must it be?

Script: `forecast.py` (about 0.03 s). Question frozen in `FROZEN_QUESTION.md` before the script existed. Outputs: `forecast.out`, `forecast_results.json`, and the MUTATE pair `forecast_MUTATE.out`, `forecast_MUTATE_results.json`. Every input carries a file and line, and the script checks that each cited line contains the cited text (65 citations, C0). Only committed budgets and predictions are used; no new physics, no new constant, no tuning. kappa = 1/2 stays FITTED. The theory is not claimed closed.

**Exit codes.** Main run: **0** (11 of 11 checks pass: citations, JSON agreement, eight reproductions of committed separations, and the headline). MUTATE run (`python3 forecast.py MUTATE`, every systematic floor set to zero): **1**. It fails C2b (the frozen sigma_sys no longer caps the old Arm B at 2.25 / 1.50), C2e (CFG52's 2.3 sigma cap no longer reproduces) and the headline H1 (no test is capped any more; every row would read "DISCRIMINATES"). That is the control working.

## Bottom line

Only Gaia DR4 separates B from anything, and only from the bare MOND-type law (Arm A). It cannot separate B from LCDM or Newton at any N, because both predict gamma-hat = 1.000. Every other test that has a usable sigma is capped below 3 sigma by a systematic floor whatever N. KiDS cannot be forecast from committed budgets.

## The ranked table (canonical footing; caps are sigma at N = infinity)

| rank | test | pair separated | Delta | floor | cap | N for 2 sigma | N for 3 sigma | in hand / expected | class |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Gaia DR4 wide binaries (gamma-hat) | B (1.000) vs bare MOND, Arm A floor (1.1614; alt 1.1917) | 0.1614 | 0.020 | **8.1** (4.9 if Arm A's own +-0.0175 is added) | 1,772 pairs | **4,342 pairs** (alt 2,940) | 30,000 expected; pipeline built; release 2 Dec 2026 | **discriminates**; S = 5.8 at N = 30,000 (4.0 at DR3-like precision) |
| 1b | same | B (1.000) vs LCDM / Newton (1.000) | 0 | 0.020 | 0 | never | never | -- | **identical prediction**: a survival test for B, never a confirmation |
| 1c | same | chain ceiling (1.0725; alt 1.0900) vs Newton / B / LCDM | 0.0725 | 0.020 | 3.6 (alt 4.5) | 11,848 (alt 6,665) | 58,850 (alt 21,660) | only if xi sits near its floor | above 3 sigma only at the floor and only beyond 30,000 pairs (canonical) |
| 2 | ultra-faint dwarfs (median log sigma_obs/sigma_law) | isolated law (bare) vs B's derived cold-mass rule (LCDM-like NFW debris) | 0.383 | 0.154 | **2.5** | **about 5 systems** | **never** | 40 uncleaned, 8 statistically corrected, 2 multi-epoch | capped below 3 sigma |
| 3 | a0 at z about 2.5 (mean log a0 offset) | B flat vs a0 following H(z) | 0.576 | 0.250 | **2.3** | 1 object | never | **0 usable discs** (0 of 51, 0 clean) | capped below 3 sigma |
| 4 | X-ray groups at R500 | B vs closure (an NFW or LCDM halo of free mass) | 0.149 | 0.082 | 1.8 | never | never | 20 groups | capped below 2 sigma; B vs the bare law: Delta = 0.012 dex, not separable |
| 5 | a0 at z about 2.5 | B flat vs LCDM-native (+0.334) | 0.334 | 0.250 | **1.3** (1.7 if the 0.2 dex floor is read directly in a0 units) | never | never | 0 usable discs | capped below 2 sigma |
| -- | KiDS budget (CFG24/CFG27) | B vs standard halos | -- | -- | -- | -- | -- | -- | **not forecastable from committed budgets** |

## Plain-language reading

**Most decisive per unit of effort: Gaia DR4, by a wide margin.** The data arrive on 2 December 2026, the pipeline is built, and B (Arm C, gamma-hat = 1.000) sits 5.8 sigma_tot below the bare law's floor at the frozen N = 30,000. Only about 4,300 pairs are needed for 3 sigma, one seventh of the expected sample, and the frozen sigma_sys = 0.02 leaves a cap of 8 sigma. Even at the DR3 dry run's precision (0.035 at 10,624 pairs) the separation is 4.0 sigma. The measurement kills in both directions among the readings: gamma-hat at or above 1.083 kills B (the pre-registration rounds this to 1.084), and gamma-hat at or below 1.079 kills the bare law. A Newtonian result kills the bare law cleanly, because contamination from hidden triples pushes gamma-hat up, never down. A boost result needs the pre-registered stability checks before it kills B, because contamination is a one-sided bias that sigma_sys does not contain.

**What Gaia cannot do.** It cannot tell B from LCDM, Newton or Arm B. A Newtonian outcome is the survival of a test B could have failed, and nothing more. It also cannot separate the chain's law from Newton unless the filter length sits at its floor: even then 3 sigma needs 58,850 pairs canonical, above the 30,000 expected (alt: 21,660, within reach).

**Capped below 3 sigma by systematics, whatever N:**
- **Ultra-faint dwarfs, cap 2.5 sigma.** The two readings differ by 0.38 dex, and the floors (Upsilon_V 0.077, the rule's collapse-mass floor 0.133) combine to 0.154. About 5 systems reach 2 sigma at today's scatter. Adding the binary-treatment shift (0.104, CFG46) lowers the cap to 2.1 and raises N(2 sigma) to 26. Dispersion precision hardly matters: perfect dispersions save at most a factor 1.46 in N, because the scatter between systems (0.20 dex or more) sets N, not the per-system error (0.05-0.10 dex in CFG51). The data sit midway (binary-cleaned median +0.21, midpoint 0.19), so neither reading is excluded today. If the collapse-mass floor were absent, 6 systems would give 3 sigma, but that floor is a theory uncertainty that data cannot shrink. Only 2 multi-epoch systems exist. B and LCDM are not separable here: any halo mass from 2e8 to 1e12 fits, which contains the rule's value.
- **a0 at z about 2.5, cap 2.3 sigma against H(z) and 1.3 against LCDM-native.** Statistics are not the problem: a single object at 0.13 dex reaches 2.57 sigma against LCDM-native before systematics, and the committed count for 3 sigma against LCDM-native is 1.4 objects. The correlated mass-scale systematic is the limit. To reach 3 sigma the floor must fall from about 0.25 to 0.19 dex (against H(z)) or to 0.11 dex (against LCDM-native). And there is nothing to measure yet: no usable disc is on disk. A flat a0 is also what bare MOND with a constant a0 predicts, so this test cannot separate B from that.
- **X-ray groups, cap 1.8 sigma at R500 (2.6 at R2500).** The 20 groups already give a statistical error of 0.014 dex, so more groups change nothing. The hydrostatic-bias allowance (20%, 0.079 dex) is the limit. Cutting it to about 10% would allow 3 sigma on B's own shortfall at R500. B and the bare law predict nearly the same mass there (1.41 against 1.45 canonical), so this test cannot separate them.

**Not forecastable from committed budgets:**
- **KiDS.** Cost (29.4-49.3 in delta-chi2) and the standard-halo spread (50.2) are both delta-chi2 between fixed models, so both scale with survey area and their ratio (0.59-0.98) does not change with N. It stays below 1 at any size. The B-versus-NFW difference is 5.4, about a tenth of that spread. Only a better standard-halo model could change this.
- **Ultra-faints against bare MOND with the external field.** No committed number.
- **Groups against LCDM as a contrast.** LCDM's halo mass is free, so it fits by construction. The baryon-fraction trend across groups and clusters (rho = -0.96) is a trend test with no per-group sigma committed.
- **Gaia contamination.** Hidden triples are a one-sided bias outside sigma_sys. The alt Arm A top (1.2267) also lands in the 1.23 no-verdict zone in 43-49% of true outcomes (PRE line 987).
- **Whether N = 30,000 is reached** after the frozen cuts. The DR3 dry run had 10,624 pairs, and DR4's error scaling is flagged approximate (PRE line 605).

## What result would kill which reading (headline settings)

| test | result | kills (at 2 sigma unless stated) |
|---|---|---|
| Gaia, N = 30,000, 3 sigma_tot | gamma-hat >= 1.083 (frozen text 1.084) | B, Newton, LCDM; the chain survives to 1.155 (frozen text 1.157) |
| | gamma-hat <= 1.079 (frozen text 1.077) | the bare law (Arm A) |
| | gamma-hat in 1.00-1.079 | kills the bare law; B and Newton survive (B cannot be confirmed over Newton) |
| a0(z), any N, floor 0.25 | mean offset above flat below 0.07 | H(z) tracking (2 sigma, N of 10 or more) |
| | mean offset above 0.5 | flat B |
| | any value | LCDM-native cannot be killed at 2 sigma with this floor |
| dwarfs, N = 8 | median offset above the law greater than 0.35 | the isolated law |
| | median offset below 0.03 | the rule |
| | between 0.03 and 0.35 | neither (the current binary-cleaned value, +0.21, is here) |
| groups, R500 | shortfall above 0.17 dex (2 sigma) | B's cold-share rule as written; today 0.149 |

## What is derived here rather than committed

- **The a0(z) floor bridge.** CFG52 commits "about 2.3 sigma whatever N" for flat against H(z), worked in g_obs (gap 0.23-0.27 dex). CFG6 works in log a0. I converted CFG52's cap into an effective floor of 0.576/2.3 = 0.250 dex in a0 units. Reading the 0.2 dex floor directly in a0 units gives caps of 2.9 and 1.7. Both are in `forecast.out`; the headline keeps the lower.
- **The dwarf scatter.** Per-system scatter is the committed bootstrap error times the square root of N (0.242 on 40 systems, 0.320 on CFG46's 8, 0.201 on the best-measured 13). The last is an upper bound on the intrinsic scatter.
- **The dwarf Delta.** It is the difference between the law's and the rule's committed offsets on the same systems (CFG42). The rule is itself not a passing reading (CFG45: none of four readings passes all seven gates), and its ultra-faint collapse mass is an extrapolation (CFG42 line 36).
- **Normality and independence** of the systems are assumed. Ranking by effort is qualitative, since no committed number prices an observation.

Nothing here says the theory is closed.

## Referee corrections (2026-09-29, README audit relayed from the Opus/Fable chat; appended)

- Check C2e (the a₀(z) floor bridge) is circular by construction: the effective 0.25 dex floor is derived from CFG52's committed 2.3σ cap and then used to reproduce that cap. It shows the bridge is self-consistent, not that the floor is independently right; the alternative reading (the 0.2 dex floor directly) gives caps of 2.9 and 1.7.
- In the DR4 row, "4.9" is S(30,000 pairs) with Arm A's own ±0.0175 included (S = 0.1614/√(0.0276² + 0.0175²) = 4.94), not a cap; the corresponding cap at infinite N is about 6.1 by the referee's calculation (8.1 without Arm A's own error). The 3σ pair counts in the row are the primary numbers.
