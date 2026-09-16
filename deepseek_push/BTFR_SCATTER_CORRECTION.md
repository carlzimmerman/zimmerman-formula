# BTFR SCATTER REGISTER CORRECTION (G117)

**DATE:** 2026-09-15 (EDT, UTC-04:00) — amendment to the committed record, committed on top of G087 (commit `4897308c4`).

---

## 1. THE OLD NUMBER (the registered claim)

`glm53_push/REFEREE_ATTACKS.md` §2.7 (commit `9261f3df9` era register, quoted in the re-audit):

> **2.7 "BTFR scatter."** G033 on real data: median residual **11.5%, 80th percentile 22%** vs SPARC's 10-15% observed scatter for the ZERO-PARAMETER v^4 = GM_b a0. STATUS: ANSWERED.  (lines 93-95)

Per G087's provenance note: this number was registered on G033's *name without a committed pipeline artifact inside 2.7 — `glm53_push/G033_build_fluid_bundle.py` contains no such statistic in committed code — and it predates the committed bundle. It **is NOT reproduced** by the committed pipeline.

---

## 2. THE NEW NUMBER (the committed pipeline re-audit, G087)

`deepseek_push/G087_btfr_scatter.py` / `.out / G087_results.json (commit `4897308c4`), on the full committed bundle (G033's 175 SPARC rotmod curves, G044 corpus v7 bit-identity E1: 175/175, SPARC Table 1 .mrt merged, standing M/L conventions inherited, never re-fit):

| reading | median \|res| | 80th pct | rms (v) |
|---|---|---|---|
| Table-1 Vflat, M/L 0.5/0.7, canonical (n=135) | 5.0% | 9.7% | 0.0899 dex |
| curve-median V, M/L 0.5/0.7, canonical (n=171) — PRIMARY | 5.6% | 11.6% | 0.1031 dex |
| G033 bundle-exact (M/L=1, curve V), canonical (n=171) | 5.1% | 9.4% | 0.1075 dex |
| alt footing a0=1.1279e-10 (n=135 Table-1) | 4.3% | 9.0% | 0.0862 dex |
| alt footing (n=171 curve-median) | 5.0% | 10.7% | 0.1046 dex |

**Corrected statement: observed BTFR scatter = 5.0–5.6% median |res|, 9.4–11.6% 80th pct, rms 0.09–0.11 dex in v (0.36–0.44 dex in M_b), both footings, three readings. G033's own bundle artifact read directly: median 5.04%, 80th 9.17% (canonical).**

**Intrinsic upper bound (the honest caveat):** E1_loocv = 0.0836 dex ≈ **0.084 dex = 21%** (in-sample E1 0.0713 dex = 17.9%; E2 variance-model 0.0144 dex²; errV-only floor 0.0219 dex). The RAR within-galaxy white-noise analogue is 0.045–0.052 dex — the BTFR intrinsic upper bound sits ~2x above it: "zero intrinsic scatter" remains **bounded, not proven."

**Provenance of the old number (why 11.5%):** the EB-E3 register class — the zero-fit baryon-mass predictor register, `prep_2026/equation_book/EQUATION_BOOK.md` E3 line 60 and `predictions_2026/PREDICTIONS_LEDGER_2026-09-02.md` B-2 row: **median M_pred/M_phot = 1.15 canonical / 0.97 alternate** — the "1.15 mass-ratio register class — is the most likely conflated source (1.15 rendered as a percent), stated honestly per G087.

**The G-scatter row that COULD be rechecked:** none of the G051 table rows carried 11.5/22 itself (see §4 V1 hit list); G051's scatter rows are all RAR-family numbers and stand as measured.

---

## 3. FORECAST UNCHANGED

The G087 forecast curve (new prediction, quantitative, falsifiable, and a deliverable of the re-audit): sigma_v(M_acc) = sqrt(intr² + (M_acc/4)²), M_acc = baryonic-mass measurement accuracy in dex.

- SPARC-era observed rms: **0.1031 dex = 26.8%** (self-consistent with the model at the inferred effective M_acc = 0.24 dex)
- At the JWST-resolved-IMF frontier M_acc = 0.05 dex: **0.0846 dex = 21.5%**

**The forecast is UNCHANGED by this correction** (26.8% → 21.5% with JWST masses). The correction only replaces the scatter level that the curve is anchored to; the curve itself and G087's registered bar (V3: sigma_v(0.05) ≤ 0.5·sigma_obs) measures as 21.5% vs the 12.6% bar → V3 still FAILS as registered, and the curve remains the falsifiable statement.

---

## 4. VERDICT V1 — the grep is complete: every committed hit list

Patterns searched repo-wide: `11.5%`, `22 %`, `80th percentile`, `80th pct`, `0.084`, `0.0836`, `26.8`, `21.5%`, `BTFR scatter`, `BTFR` + scatter/11.5/22, and the 0.05-dex-class RAR-floor analogue (`0.045`, `0.052`, `0.05 dex`, `white-noise floor`), in all committed .md/.py/.json/.out/.txt (excluded: .git, node_modules, venv).

### 4a. Every committed place the registered 11.5%/22% appears (the number to amend — 4 file-hits, one register + its re-audit trio):

1. **`glm53_push/REFEREE_ATTACKS.md:93-95`** — §2.7 register: *"G033 on real data: median residual 11.5%, 80th percentile 22% vs SPARC's 10-15% observed scatter for the ZERO-PARAMETER v^4 = GM_b a0. STATUS: ANSWERED."* — **THE REGISTER ROW. The old number lives ONLY here as a live claim**
2. **`deepseek_push/G087_btfr_scatter.out:78`** — *"registered claim (REFEREE_ATTACKS.md 2.7): median residual 11.5%, 80th pct 22%"* (re-audit target line, with the corrected numbers alongside, lines 79-92)
3. **`deepseek_push/G087_btfr_scatter.py`** — Part-1 header registering the same claim as the audit target (mirror of #2)
4. **`deepseek_push/G087_results.json`** — `registered_claim_reaudit: {claimed_median_pct: 11.5, claimed_p80_pct: 22.0, measured_bundle_artifact_pct: {median: 5.04, p80: 9.17}, measured_this_run_pct: {median: 5.59, p80: 11.65}}`

Negative results (checked; no hit): G033's own committed script `glm53_push/G033_build_fluid_bundle.py` contains NO 11.5/22 text — the registered number never had a committed artifact inside G033 (G087's provenance statement says exactly this); hermes_push/STATE.md:32,47 "22%" hits are the C003 clock-frame-kicks ledger (22% ledger reproduction), **not** the BTFR; prep_2026 11.5% hits (a0-line estimator 11.5%, cluster_efe_channel θ(0)=e spread 11.5%, hunt_2026/k07d +11.5% Υ shift) are unrelated subjects.

### 4b. Every committed place the 0.05-dex-class RAR-floor analogue lives (the benchmark family):

5. **`glm53_push/G051_master_table.py:275-277` / `.out:24` / `.json:316-321`** — row "Within-galaxy white-noise floor | 0.045 | 0.052 | 0.045/0.052 dex | G036 V4a (0.0447); G044 V1E (0.0524/0.0538); registered band 0.045-0.052" — **the analogue row the corrected BTFR intrinsic bound is read against**
6. **`glm53_push/G051_master_table.py:267` / `.out:22` / `.json:286`** — row "RAR total scatter, deep-regime pooled rms 0.15/0.174 dex"
7. **`glm53_push/G051_master_table.py:271` / `.out:23` / `.json:300`** — row "RAR scatter floor with per-galaxy M/L freedom 0.064/0.094 dex"
8. **`glm53_push/REFEREE_ATTACKS.md:87-91`** — §2.6 "The RAR scatter floor": G013 0.064 dex with M/L freedom; G036/G044 within-galaxy white-noise floor 0.045-0.052. STATUS: ANSWERED.
8b. **`glm53_push/STATE.md:147`** — G044 white-noise floor 0.0524/0.0538 dex; **`deepseek_push/STATE.md:16`** — M/L floor 0.064 dex board row "did NOT fire; outer half 0.055"
9. **`deepseek_push/G087_btfr_scatter.out:48-49,63-65,146`** (and .py/.json) — V2's registered reading clause benchmarking E1_loocv against the RAR analogue 0.045-0.052 dex

### 4c. BTFR-adjacent committed rows that DO NOT carry 11.5/22 (checked; listed for completeness):

- `glm53_push/G051_master_table.py:123` / `.out:11` — row "v_flat (MW baryons 6.5e10 Msun) 168.589/176.625 km/s", the BTFR amplitude row (PASS +0.24%/+0.21%)
- `deepseek_push/STATE.md:55` and `glm53_push/STATE.md:162,210` — BTFR zero-point z≈2.5 rows: 0.00 vs +0.33 dex, 20:1 (JWST/ALMA instrument rows)
- `deepseek_push/GRAVITY_EVERYWHERE.md:159` — BTFR in the equipartition triad (v_c² = 2σ² = √(GM_b a₀)); `:304 — the high-z zero point (G080) row, H026 NOT ESTABLISHED
- `deepseek_push/PREDICTIONS.md` (E1–E10) — no BTFR scatter row (the E-ledger has no scatter claim); `qwen38_push/PREDICTIONS.md` — no BTFR scatter row; `kimik3_push/predictions/PREDICTIONS.md:87-92` — P7 BTFR zero-point/normalisation rows (within 0.03 dex of the fitted-scale value; no scatter claim)
- `predictions_2026/PREDICTIONS_LEDGER_2026-09-02.md:47` — B-2 row: the EB-E3 register class: median M_pred/M_phot 1.15/0.97 (BTFR as a theorem; zero-fit mass predictor) — **the provenance register that the old 11.5 almost certainly conflated**
- `prep_2026/equation_book/EQUATION_BOOK.md:53-60` — E3 (EB-E3): the zero-fit baryon-mass predictor + velocity a0-line + exact BTFR; line 60 the 1.15/0.97 SPARC fire result
- hunt_2026 BTFR rows (h49, h105, h109, h123/h125, u03, h74, h94) — independent BTFR lanes quoting their own observed scatters (0.06 dex polar-ring, Lelli+ 0.24 dex/0.10 dex, 0.136 dex cluster spirals, ~0.03 dex scatter in h49 control run). None quotes the 11.5/22 register; none is contradicted by 5.0-5.6% (different samples: V_flat vs V200 widths, etc.) — noted, not amended.

---

## 5. VERDICT V2 — per-claim impact (G051 rows and the other registers): does 5.0% strengthen or weaken each?

Convention: the corrected statement is a TIGHTER observed scatter (5.0–5.6% vs 11.5%) with an honest 21% intrinsic upper bound.

| # | Row / claim | Site | Impact of 5.0-5.6% | Reading |
|---|---|---|---|---|
| G1 | v_flat BTFR amplitude 168.589/176.625 km/s (PASS +0.24/+0.21%) | G051_master_table | **STRENGTHENS** | The zero-point stands; a tighter scatter raises the weight of a zero-point PASS at constant value — less of the residual budget to hide in. |
| G2 | "RAR total scatter, deep-regime pooled rms 0.15/0.174 dex" | G051 row | **UNCHANGED value; context strengthened** | The BTFR rms 0.09-0.11 dex in v is tighter than the per-point RAR 0.15 dex, and G087 shows its dominant carriers are M_b systematics (M/L lens rms 0.19 dex in M_b ≈ half the residual sd) — the same systematic family the RAR row carries. No row value changes. |
| G3 | "RAR scatter floor with per-galaxy M/L freedom 0.064/0.094 dex" | G051 row | **STRENGTHENED narrative** | G087 independently confirms the M/L-systematic mechanism that this row measures: with M/L freed the scatter collapses (0.15 dex → 0.064). The BTFR re-audit shows the identical physics (convention-switch lens = dominant scatter). |
| G4 | "Within-galaxy white-noise floor 0.045/0.052 dex" (registered band) | G051 row | **UNCHANGED value; becomes the honest benchmark (the caveat row)** | The corrected observed BTFR median |res| 5.0-5.6% ≈ 0.021-0.024 dex sits at the errV floor and is consistent with this analogue; but the corrected intrinsic upper bound 0.084 dex = 21% sits ~2x ABOVE this floor — so the 0.05-dex class now explicitly boundaries the claim "no intrinsic BTFR scatter": bounded at 21%, not certified at 5%. |
| G5 | "Population-mean deep sag -0.13 dex/dex" | G051 row | **UNCHANGED** | Orthogonal row (RAR slope residual); untouched by a BTFR scatter correction. |
| R1 | §2.7 "BTFR scatter: 11.5%/22% ... STATUS: ANSWERED" | REFEREE_ATTACKS | **AMENDED — the status keeps "ANSWERED" but on the corrected numbers; STRENGTHENS the law** | The answer to the attack is now: the registered 11.5/22 is not reproduced; the zero-parameter law confronts the data at 5.0-5.6%/9.4-11.6% observed — a ~2x tighter scatter than the register claimed — with the honest 21% intrinsic bound stated. Under-correction would have made the law look worse than it is; the correction makes it better-constrained. |
| R2 | §3.4 / STATE rows z≈2.5 BTFR zero-point: 0.00 vs +0.33 dex at ±0.13, 20:1 (JWST/ALMA) | REFEREE_ATTACKS:115,180; deepseek STATE:55, glm53 STATE:162,210; GRAVITY_EVERYWHERE:304 | 0% impact on the forecast row; the 5.0% background **strengthens its power** | The 20:1 discriminate lives in the zero-point offset, not the scatter; a tighter scatter slightly reduces the noise term of a 2.5-point sample comparison. Forecast unchanged (G080/H026 statuses intact). "Cannot get much stronger by correcting numbers" applies only to scatter claims; the zero-point forecast never used the 11.5/22 claim. |
| R3 | EB-E3 register class: median M_pred/M_phot = 1.15/0.0.97 (the BTFR-as-theorem row, zero-fit mass predictor) | EQUATION_BOOK:60; PREDICTIONS_LEDGER B-2:47 | **UNCHANGED and NOT revoked; clarified as provenance** | This is the register class the old 11.5 likely conflated (1.15 as percent). The 1.15 mass-ratio row itself stands as measured; it is the *conflation source note*, not a second error. Impact: none on its claim; it gains a cross-reference as G117-provenance. |
| R4 | GRAVITY_EVERYWHERE triad claim (v_c²=2σ²=√(GM_b a₀)) | GRAVITY_EVERYWHERE:159 | **STRENGTHENS** | The triad's amplitude claim gains from a tighter BTFR; no number in the triad changes (equipartition exactness is M-independent). |
| R5 | kimik3 P7 "BTFR ... within 0.03 dex of the fitted-scale value" | kimik3 predictions:87 | **UNCHANGED** | Zero-point claim; no scatter sentence used 11.5/22. |

Net V2 finding per row; nothing weakens. The only "weakening" in the family is honest: the 21% intrinsic bound means the law's scatter claim is *corrected tighter, but certified only to 21% intrinsic*, exactly the caveat the register must carry.

---

## 6. VERDICT V3 — the honest statement (what the corrected scatter does to the law's standing)

**A TIGHTER zero-parameter BTFR is BETTER for the law.** The law predicts v^4 = G M_b a₀ as an identity — zero fitted parameters, zero intrinsic scatter — for every galaxy. The now-registered numbers are the factual base of that claim's confrontation with data:

1. Observed median |res| on the committed bundle, both footings, all three readings: **5.0–5.6%**, and 9.4–11.6% at the 80th percentile — roughly **half the registered 11.5%/22%** that G033 was previously credited with, and inside the floor of the 10-15% band that §2.7 invoked as SPARC's own literature scatter (10-15%). A zero-parameter law living at 5% median residual in v is a tighter empirical law than a 11.5% one — and the registered 11.5% number made the law look weaker than its own committed pipeline shows.

2. The decomposition channel is genuinely informative in direction: galaxies with worse rotation-error/quality metadata scatter MORE (errV ρ=+0.21, p=0.006; Q ρ=+0.20, p=0.009; FDR-survives Q), and the dominant systematics (M/L convention choice alone = rms 0.19 dex in M_b ≈ half the residual sd in v) are population-model systematics invisible to SPARC's photometric proxies — consistent with the scatter being measurement-dominated. V1 V1-bar (LOOCV R²≥0.10) still FAILs (measured 0.03, honestly stated — the multivariate proxy model does not generalize).

3. **THE HONEST CAVEAT, stated with equal force: the intrinsic upper bound is 0.084 dex = 21%** (E1_loocv; in-sample 17.9%). After removing everything the proxies can carry, 21% of v worth of rms remains that the data cannot attribute to systematics. That sits ~2x above the RAR within-galaxy white-noise floor (0.045–0.052 dex). So the correct sentence is exactly G087's:
   - The observed BTFR scatter is tight (5.0–5.6%) and dominated by the systematic axes the proxies can see, but "zero intrinsic scatter" is *bounded at 21%, not proven at 5%*.
   - The RAR's own floor row (0.045–0.052) is where the BTFR intrinsic scatter would need to be to claim equality with the RAR's tightness class; it is not there yet.

4. The falsifiable JWST-era forecast is unchanged: SPARC era 26.8% (self-consistent at the inferred effective M_acc = 0.24 dex) → 21.5% at JWST-resolved masses M_acc = 0.05 dex; the JWST front decided whether the intrinsic bound (21%) collapses toward the errV floor (2%). V3's registered bar (≤0.5·sigma_obs = 12.6%) is still FAILed by 21.5% — honestly, per pre-registration.

5. Register discipline consequences, stated plainly: (a) §2.7's STATUS line is amended-from-11.5-in-spirit and re-pointed at G087 (this correction + G087 supersedes the 11.5/22 quotation wherever it is quoted from here on, without rewriting history, which stays committed and flagged, G087's convention); (b) NOTHING in G051's numeric rows changes — G051 never carried 11.5/22; its four CITED scatter rows are RAR-family measurements and remain untouched-as-measured; (c) the EB-E3 1.15 mass-ratio register is untouched-as-measured and now explicitly recorded as the provenance class of the old number.

---

## 7. VERDICT V4 — the history amendment is committed honestly

This document amends the record without editing the superseded commits: G087 (commit `4897308c4`) already contains the full re-audit (data ingest E1 bit-identity, three readings × two footings, ten quality proxies, multivariate+LOOCV, the intrinsic bound, the forecast curve, VERDICTS 0/3 PASS-by-registration with FAILs-as-findings). This G117 correction references, and ends the circulation of, the 11.5%/22% register statement as a live number.

| Field | value |
|---|---|
| old claim (register) | median 11.5% / 80th 22% (REFEREE_ATTACKS §2.7) |
| new (committed re-audit) | median 5.0–5.6%, 80th 9.4–11.6%, rms 0.09–0.11 dex v (bundle artifact canonical 5.04/9.17) |
| intrinsic upper bound | 0.084 dex = 21% (E1_loocv 0.0836 dex; in-sample 0.0713 dex = 17.9%) |
| provenance | EB-E3 register class: median M_pred/M_phot = 1.15 canon / 0.97 alt (EQUATION_BOOK E3:60, PREDICTIONS_LEDGER B-2:47) — the likely conflated source of "11.5" |
| forecast forecast row | unchanged: 26.8% → 21.5% at M_acc = 0.05 dex (JWST masses); V3 bar still FAILs; curve is the falsifiable deliverable |
| impact grid | G051 rows: all unchanged-as-measured; R1 strengthened; R3 clarified-as-provenance; R4 strengthened; R2/R5 zero-point rows untouched, 20:1 arming intact |
| law standing (V3) | tighter zero-parameter BTFR is better for the law; 21% intrinsic upper bound is the honest caveat; JWST decides the bound at 21.5% |

---

*Supersession note:* any future quotation of the BTFR-scatter register MUST cite the corrected numbers (G087 commit `4897308c4` + this G117) and, if quoting the old claim as history, must carry the "NOT REPRODUCED" line per G087 Part 1. The E-ledger (deepseek_push/PREDICTIONS.md) contains no scatter row and needs no change.