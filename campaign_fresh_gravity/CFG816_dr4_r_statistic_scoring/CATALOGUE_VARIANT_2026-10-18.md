# The R-analysis catalogue variant (CFG825), declared 2026-10-18 before DR4

**What it is.** The registered stage G (`catalog_builder/build_catalog.py`, run through `dr4_ready_1/dry_run_driver.py`) with exactly two cuts changed: the **NSS screen (cut 12) is removed** and
**"2 < s < 30 kAU" becomes "2 < s < 50 kAU"**. It exists only as the input of the R statistic (`cfg816_r.py`); the registered γ̂ pipeline and its prereg catalogue are untouched. Builder: `build_variant_catalogue.py`
(a new file; the variant function is made from the registered function's own source text with two asserted string replacements and swapped in only for the call). Not an amendment: the owner decides whether to file it as one.
κ = ½ is fitted; nothing here says the data favour the framework.

**Why.** The frozen criteria (CFG825 `FROZEN_CRITERIA.md`) define the primary as not NSS-screened and the numerator as s ≤ 50 kAU, with an NSS-screened branch. The registered catalogue already applies the NSS cut and stops at 30 kAU, so on it
the NSS-screened branch equals the primary and the cap is moot (README, converter findings).

**Unchanged on purpose.** All other cuts, R_chance < 0.01, the correlation caches, the seeds and the driver's copied stage G. **The triple search keeps its registered 30 kAU radius**, so a pair at 30-37 kAU is not tested for a third star
beyond 30 kAU of a component; that can only leave contaminants in and push ṽ up, which makes a false KILLED more likely, not less. The R rule's own contamination checks (NSS-screened branch, f_tail) are the guard.

**Validation on DR3 (offline, a code-path test, never a result; `build_variant_selftest.json`, 10 checks, all pass).**
- V1: with both switches off the build reproduces the registered DR3 catalogue **byte for byte** (6,210 pairs, sha256 `6fff64d964ebaa72`), so the mechanism changes nothing else.
- V2 (baseline): reseeding the registered build alone flips **2.2-2.4% of pairs out and 2.1-2.3% in**, adding no NSS-flagged and no wide pair. This is the registered stage G's Monte-Carlo velocity-error cut (Amendment 18's measured sensitivity): any change of the
  pair array shifts the random stream. A first version of the self-test expected an exact superset of the registered catalogue; that expectation was wrong and is replaced by checks against this baseline.
- Variant (both switches): 6,308 pairs (sha256 `80c1292457b50104d3408d672eb45f4fbe48e6774ee0a3e8601c2a3ad5050612`); intended additions **+100 NSS-flagged pairs (1.59%)** and **+6 pairs wider than 30 kAU (30.2-36.9 kAU)**; the remaining changes (lost 2.29%, other-added 2.16%)
  equal the reseed baseline.

**What it does to the DR3 R inputs (counts only; no R computed from the variant).** Primary sample 1,315 pairs, outer (x > 1) 170, inner (x < 0.3) 175 (the registered table had 175 / 173; the difference is flip noise). **NSS-screened: 1,303 pairs, 168 / 173**: it now differs from the
primary, by 12 pairs (0.9%). **The cap extension adds nothing to the primary's numerator** (the "r_sky ≤ 30 kAU" branch is identical to the primary, 170 / 175): the six wide pairs do not pass the primary's other cuts. The stage-F chance-alignment screen leaves almost no pair beyond about 37 kAU, so the 50 kAU
cap is, in practice, a 37 kAU cap. **On DR3 the variant therefore barely changes R's inputs.** DR4's non-single-star tables may flag far more, which is the reason to declare it now.

**DR4 use.** `python3 build_variant_catalogue.py --release dr4 --manifest M.json --allow-network --out PATH.csv` (the driver's own options pass through; **untested**, DR4 does not exist). The per-star file given to `make_pair_table.py` must carry the cut-12 union flag as `non_single_star`.

**Status of the DR3 check.** The once-only official DR3 run (C4) was made 2026-10-18 21:37 on `pairs_dr3.csv` (the registered-catalogue table; the owner chat's run beside T2x): R = 0.9728, σ_R = 0.1775, N = 348, UNDECIDED, C4 PASS ((R−1)/σ_R = −0.15; (1.20−R)/σ_R = +1.28). A DR3 run on `pairs_dr3_variant.csv` would be a second, different-input code-path run
and needs the once-only guard relaxed with a tag; it has not been made.
