# CFG46 — the ultra-faint failure against binary-corrected dispersions (Arroyo-Polonio+2026)

Script: `CFG46_ufd_binary_corrected.py`, about 5 s. Outputs: `.out`, `_results.json`, and the MUTATE pair (dispersions × 0.5). The main run exits 1: **H1 and H2 failed as declared**, for a reason explained below. The mutation run fails H1 as required.

## Question

CFG28–CFG29 refereed B's largest data failure (the Milky Way ultra-faints' dispersions +0.30–0.33 dex above the isolated law, 3.5–3.8σ) and found that binaries could not explain it under published bounds. One escape remained: a statistical correction applied to the data. Arroyo-Polonio, Battaglia & Thomas 2026 (arXiv:2603.03129, Table 1) do exactly that for 12 ultra-faints: a mixture model with the solar-neighbourhood binary velocity distribution, on single-epoch data, with the binary fraction f free (flat prior) or fixed at 0.7.

## Data

`real_research/data/arroyopolonio2026_ufd_binary_corrected.tsv` (12 rows, transcribed by script from the arXiv LaTeX source; e-print 4,376,586 bytes; fetched with the owner's approval). Columns: the literature dispersion, the paper's f = 0, f-free and f = 0.7 posterior medians with 1σ errors. Nine of the twelve are in the repo's Milky Way table; FG001's brightness cut removes Crater II, so **eight are scored** (Boo I, Car II, Hyd I, Leo IV, Leo V, Ret II, Seg 1, Wil 1). Eri III, Sag II and UNIONS 1 are absent from the repo's table.

## Method (declared before the first run)

FG001's estimator and inputs (as CFG28 and CFG42); the statistic is the median over the eight of log(σ/σ_law); the error is a bootstrap plus the measurement error (from the paper's asymmetric errors) plus CFG28's systematic floor. **H1:** the bare law's offset with the f-free dispersions stays positive at > 2σ. **H2:** with f = 0.7, > 1σ. **H3:** the rule (CFG42's sum) with the corrected dispersions is within 2σ of zero.

## Results

| dispersions | law, canonical | σ |
|---|---|---|
| paper, f = 0 (the control) | +0.295 ± 0.163 | +1.81 |
| **f free (H1)** | **+0.206 ± 0.164** | +1.26 |
| **f = 0.7 (H2)** | **+0.171 ± 0.172** | +0.99 |
| rule, f free (H3) | −0.151 ± 0.129 | −1.17 (passes) |

(Alt footing: +0.275, +0.186, +0.150.) Controls: C1 passes (12 rows; the paper's f-free dispersion is below its f = 0 value for all 12); C2 passes (the paper's f = 0 re-analysis agrees with the repo table to 0.013 dex: +0.295 against +0.308).

**H1 and H2 failed, and the reason matters.** On these eight systems even the *uncorrected* offset is only 1.8σ, because eight systems carry far less power than the 40 (31 resolved plus 9 limits) in CFG28, and the per-system offsets range from −0.03 to +0.65. So the failures are largely lost power, not evidence that binaries remove the offset. I declared H1's 2σ threshold without checking that eight systems can reach it at f = 0. That is recorded in the docstring.

**The effect of the correction itself is measured pairwise and does not depend on power** (post-hoc R2, added after the main run): the correction lowers each dispersion by a median of **−0.068 dex** (f free; range −0.17 to −0.02) or **−0.104 dex** (f = 0.7). That removes roughly a quarter to a third of the +0.30 offset. **Seven of the eight offsets stay positive** at f free and at f = 0.7 (all eight at f = 0). Crater II, excluded by the brightness cut, drops by 0.25 dex.

## Standing

**The statistical binary correction lowers B's ultra-faint offset by about 0.07–0.10 dex, from +0.30 to +0.17–0.21 dex, and cannot be said to remove or to confirm it on this sample.** The eight-system test has 1.0–1.3σ, against CFG28's 3.5–3.8σ on 40. The failure is not established by this data, and neither is its absence. The multi-epoch, per-star dispersions (Walker+2023's 3,720 sources with up to 15 epochs; Ou+2026's forward-modelling code) remain the decisive test, and they need per-star reduction.

**Together with CFG42:** the rule with the corrected dispersions sits at −0.15 (−1.2σ), so the rule over-predicts the ultra-faints slightly once the binary correction is applied. Its earlier ultra-faint "closure" (−0.06) was against the uncorrected dispersions.

Nothing here says the theory is closed.
