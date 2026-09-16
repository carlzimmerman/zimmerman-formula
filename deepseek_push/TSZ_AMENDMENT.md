# G177 — THE TSZ AMENDMENT

**Re-score G129's tSZ proposal with the JOINT (G113 × G122) dust prediction of G141.**

**Filed 2026-09-16. Lane G177.** Builds on G129 (`TSZ_PROPOSAL.md`, the phantom-only
proposal) and G141 (`G141_tsz_dust.py`, the closed coherency's SZ face).
**Deliverable: this file + `G177_tsz_amendment.py` / `.out` / `G177_results.json` (committed and pushed).**

> **THE ONE-SENTENCE AMENDMENT:** G129's falsifiers and SNR forecast were built to test the
> phantom-only slope **−1.44**; G141 showed the framework's joint prediction — phantom
> isotherm × r⁻¹ dust envelope — is **−2.37 at 2 R500** (2-bin [R500,2R500] **−2.54**, amplitude
> **0.30×** the phantom-only at 2 R500), an entirely different target. This amendment re-scores
> the proposal against the joint curve: a new pass window, two re-targeted falsifiers, a two-sector
> Δχ² test, a revised (dimmer) SNR, and a **three-way decision tree** in place of the binary pass/kill.

**Built on (all committed):** G113 `G113_tsz_prediction.py/.out/.json` (the zero-parameter y-profile),
G122 `G122_results.json` (the closed coherency: c_dust = a_c (r/R500)^−0.99, p\* = 0.99, 12/12
amplitudes), G129 `G129_tsz_proposal.py` + `TSZ_PROPOSAL.md` (the 1-sector phantom-only proposal),
G141 `G141_tsz_dust.py/.out/.json` (the joint G113×G122 curve). Every number below is recomputed by
`G177_tsz_amendment.py` by **re-executing G129's and G141's own builds in-process** (identical loaders,
identical recipes) and gated against the committed `G129_results.json` / `G141_results.json`
(9/9 checks PASS). A FAIL would be a finding.

---

## 1. THE CHANGE — what G141 moves, and the two-sector object G129 must test

| quantity | G129 (phantom-only) | G141 (JOINT, G113×G122) | what the amendment does |
|---|---|---|---|
| outer slope at 2 R500 | **−1.44** | **−2.37** (2-bin [R500,2R500] **−2.54**) | re-target the pass window |
| y at 2 R500 vs classic β = 2/3 | 105× | **31×** (0.30× the phantom-only amplitude) | re-quote the signalling |
| predicted per-cluster slope | −(q−1) | −(q−0.01) = −(q−1)−0.99 (the Abel of the r^−0.99 envelope) | re-center the registered band |
| object under test | the phantom-zone pressure profile alone | the **product** n_e k_B T(phantom) × c_dust — two sectors | the falsifiers become directional |
| verdicts | binary pass/kill | **three-way** (joint / phantom-only / neither) | a classification, not a verdict |

The amendment's structural point: G129's pass window (−1.7, −0.9) and falsifiers were built against
−1.44; under the joint prediction a slope of −1.44 is no longer a pass — it is a **falsifier** (the
+0.99 dust steepening is absent → no envelope). And the −1.44 reading G129 wanted to confirm is,
after G141, *the thing that kills the dust*, not the thing that confirms the phantom.

---

## 2. (1) THE REVISED PASS WINDOW + FALSIFIERS

**The revised pass window (the slope the joint model predicts on [R500, 2R500], with the
per-cluster band).** The joint per-cluster 2-bin slope is −(q−0.01); with G129's registered band
half-width 0.4, the **registered joint pass band per cluster is [−(q−0.01)−0.4, −(q−0.01)+0.4]**.
Across the 12 clusters: **12/12** land inside their own band; the sample median 2-bin slope is
**−2.535** (pointwise at 2 R500 **−2.365**), so the **sample pass window is (−2.94, −2.14)** (median
−2.54 ± 0.4), replacing G129's (−1.7, −0.9). A measured slope with per-cluster values inside their
bands at ≤ 2σ and y/y(classic) consistent with ~31× passes.

**F1′ — a measured slope STEEPER than the joint band kills the dust envelope.**
Slope < −(q−0.01)−0.4 at ≥ 3σ. The outer profile then falls faster than phantom + r⁻¹ dust allow —
the envelope's contribution is killed (G129's F1 "steeper than −2" is subsumed; the joint steep edge
is the steeper of the two for q < 4).

**F2′ — a measured slope AT the phantom-only reading kills the dust.**
Slope landing on the [−(q−1)±0.4] band (consistent with −1.44, flatter than the joint band's flat
edge) at ≥ 3σ. The +0.99 steepening is absent → the r⁻¹ envelope contributes nothing → **the dust is
killed, the phantom-only reading stands.**

**The two-sector test (joint fit vs phantom-only fit on the same outer bins).**
On the same outer bins (Planck 143, 8–40′): Δχ² = χ²(phantom) − χ²(joint) against joint-truth data.
**Δχ² = 2290 shape-only → √ = 47.8σ pooled** (1395 absolute → 37.3σ); ACT f150 6–18′ over the 7
in-band clusters: 3795 → 61.6σ. The outer bins themselves reject the phantom-only fit against the
joint fit at tens of σ.

---

## 3. (2) THE REVISED SNR — the joint profile is dimmer outside

The joint prediction is 0.30× (median) the phantom-only amplitude at 2 R500 (range 0.23–0.40). The
outer bin SNRs scale by the per-bin envelope ratio. **Sample-median per-bin SNR (joint profile; per
channel, no ILC penalty):**

*Planck 143 GHz (all 12):*
| bin (′) | 0–4 | 4–8 | 8–12 | 12–17 | 17–23 | 23–31 | 31–40 |
|---|---|---|---|---|---|---|---|
| phantom median SNR | 22.6 | 15.7 | 10.2 | 9.3 | 7.8 | 6.6 | 5.4 |
| **JOINT median SNR** | 30.1 | 21.7 | 12.2 | 6.9 | 4.1 | **2.6** | **1.4** |
| # clusters SNR > 3 | 12 | 12 | 12 | 12 | 8 | **2** | **1** |

*ACT f150 (7 in-band):* all bins > 3σ under the joint profile (median 13–49) — the 8–18′ branch
survives intact.

**Which bins stay above 3σ, which drop out.** The 8–17′ phantom-zone bins survive on all 12 (median
12.2 / 6.9, min 7.8 / 3.8) and the ACT/SO branch holds every bin on the 7 in-band clusters. The
**23–31′ and 31–40′ bins drop below 3σ in median** (2.6 / 1.4; 2/12 and 1/12 clusters above 3σ) —
held above 3σ at Planck 143 depth only by **A2319** (13.7 / 8.5, the flattest gas envelope, q = 1.95)
and **RXC1825** (23–31′: 3.6, the largest envelope amplitude a_c = 10^+0.062).

**The revised integration.** To hold the dropped median bins at 3σ: the 23–31′ bin needs ×1.4, the
31–40′ bin ×4.4 of the archived depth — impossible for end-of-survey Planck/ACT. The decision falls
to (i) the 2/12 clusters holding 23–31′ > 3σ, (ii) the **sample-stacked median** (pooled slope
error), (iii) the ACT/SO 8–18′ overlap, and (iv) SO deep fields (1.6 μK·arcmin, still integrating),
which hold the whole phantom zone above 3σ. **The revised slope error grows: 0.32 → 0.82 per cluster
(2-bin; 0.53 multi-bin), pooled 0.093 → 0.238 (2-bin) / 0.152 (multi-bin).**

---

## 4. (3) THE DECISION TREE — three verdicts (the amendment's core upgrade)

G129 could only pass/kill the phantom-only curve. The amended measurement returns **three verdicts**
on the **sample-median 2-bin slope** over [R500, 2R500]:

| branch | measured slope | attribution |
|---|---|---|
| **(a) THE JOINT reading** | **−2.05…−2.7** | phantom + r⁻¹ dust envelope both present (the G113×G122 prediction) |
| **(b) PHANTOM-ONLY** | **−1.2…−1.8** | the dust envelope's +0.99 steepening is absent → F2′ fires, dust killed, phantom stands |
| **(c) NEITHER** | **steeper than −2.7** (slope < −2.7) | falls faster than phantom + r⁻¹ dust allow → a different envelope slope (F1′) |

**Boundary values and grey zones.** The joint centre is −2.54 (2-bin), so the joint branch is
centred near the G141 number with per-cluster bands [−(q−0.01)±0.4]. Grey zones, registered:
(−2.05, −1.8) is intermediate (a partial/transition envelope — a midpoint landing is a >3σ rejection
of *both* registered curves), and flatter than −1.2 is the classic/rising-T regime that kills the
phantom-zone reading as registered (G129's F2 family). **Per-cluster caveat:** the tree is stated
for the sample median; per-cluster bands shift with q — A644's own joint band [−6.89, −6.09] lies
entirely in the "neither" branch, so for it the per-cluster tree is inapplicable (the decision is the
full-curve fit + the sample median, as G129/G141 registered).

**Separation power (honest).** The two axes are **not equal**: F2′ (phantom-vs-joint, the dust-kill)
separates at **4.4σ (2-bin) / 6.9σ (multi-bin) pooled**; F1′ (steeper, the "neither" branch) at only
**1.7σ (2-bin) / 2.6σ (multi-bin) pooled** — a genuinely **sub-3σ weak leg**, because the joint
prediction sits close to the classic −3 line and the dimmed outer bins carry little weight. So the
measurement **confidently separates JOINT from PHANTOM-ONLY, and can only point (not kill) toward "a
different envelope slope."** A (c)-verdict would be a strong hint followed by a dedicated
follow-up, not a kill.

---

## 5. (4) VERDICTS

**V1 — the amended proposal.** PASS WINDOW: sample-median 2-bin in (−2.94, −2.14) with per-cluster
values inside [−(q−0.01)±0.4] at ≤ 2σ; pointwise at 2 R500 consistent with −2.37±0.4; y/y(classic)
~31×. FALSIFIERS: **F1′** = steeper than the joint band (kills the dust envelope); **F2′** = at the
phantom-only −1.44 (kills the dust). TWO-SECTOR TEST: Δχ² over the same outer bins (8–40′) = 2290
shape-only → 47.8σ pooled. SNR: joint profile; Planck median bins 30.1/21.7/12.2/6.9/4.1/2.6/1.4;
23–31′ & 31–40′ drop below 3 in median (2/12, 1/12 clusters > 3); ACT all bins > 3σ on the 7
in-band; slope error 0.82 (2-bin) / 0.53 (multi-bin) per cluster, 0.238 / 0.152 pooled. DECISION
TREE: 3-way as §4.

**V2 — the revised feasibility: which clusters still decide.**
- **Decide their own outer bins (23–31′ > 3σ at Planck depth): 2/12 — A2319 (13.7), RXC1825 (3.6)**;
  only A2319 holds 31–40′ (8.5). These two carry the per-cluster outer-slope statement.
- **Decide the 8–17′ phantom-zone bins: all 12** (median 12.2/6.9; the A2029/A2142/A3266/A85 bright
  set hold 14.6–17.7 at 8–12′, 7.7–9.8 at 12–17′).
- **ACT/SO branch: all 7 in-band clusters** hold every 0–18′ bin > 3σ (median 23–49) — the inner and
  mid-phantom resolution survives the dimming.
- **Pooled/sample-level only (outer bins below their own 3σ): A1644 (23–31′ = 2.9), A2029 (2.8),
  A2142 (2.6), A3266 (2.5), A2255 (2.3), A85 (2.7), ZW1215 (1.4), A3158 (1.4), A1795 (1.1)** — they
  still feed the pooled median and the full-curve χ²; **A644 contributes neither its own outer bins
  (SNR 0.1) nor a meaningful exterior** (its joint band is already "neither").
- The sample-level decision is intact: pooled slope error 0.238/0.152 → F2′ at 4.4–6.9σ, F1′ at
  2.6σ (multi-bin); two-sector Δχ² 47.8σ. **The dimming does NOT remove any cluster from the pooled
  statements.**

**V3 — the honest statement: the amendment's delta.**
> **The tSZ test is upgraded from a 1-SECTOR to a 2-SECTOR discriminator with a 3-WAY decision tree.**
> (1) G129 could only pass/kill the phantom-only −1.44 curve — one hypothesis under test, and the dust
> envelope was invisible to it (its effect was, unbeknownst to the 1-sector design, already inside
> G129's own physics). (2) The amended proposal tests BOTH sectors at once: the joint curve
> (G113×G122, zero new parameters) is the prediction; F1′ (steeper than the joint band → envelope
> killed) and F2′ (at the phantom-only −1.44 → dust killed, phantom stands); and the measurement
> returns THREE verdicts (joint / phantom-only / neither), not a verdict. (3) The cost, honestly
> stated: the joint prediction is dimmer outside (0.30× at 2 R500), the outer bins lose signal, the
> slope error grows (0.32 → 0.82 per cluster 2-bin), and the 23–40′ bins drop below 3σ in median at
> archived Planck depth. (4) The asymmetry: F2′ (dust-kill) is the strong axis (4.4–6.9σ pooled);
> F1′ (the steeper/"neither" branch) is a registered **2.6σ** weak leg — the measurement confidently
> separates JOINT from PHANTOM-ONLY and can only point toward "a different envelope slope," not kill
> for it. Net: the same observation now classifies three readings instead of testing one, at a
> registered SNR cost that keeps the dust-kill decision above 3σ while honestly flagging the
> steeper-than-joint branch as needing further integration (SO deep) or dedicated follow-up.

---

*All numbers from the committed ingests and the committed G113/G122/G129/G141 artifacts, reproduced
by `G177_tsz_amendment.py` through in-process re-execution of G129's and G141's own builds (gates vs
`G129_results.json` / `G141_results.json`: 2/2 PASS) and the revised-SNR/multi-bin/falsifier machine
described above (9/9 checks PASS). A FAIL would be a finding.*
