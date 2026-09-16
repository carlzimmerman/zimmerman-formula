# G161 — THE PLATEAU OBSERVING REGISTRY: the flat-tail test pre-registered

**The T(r) → 2 T_floor plateau's last untested statement, written down before the observation.**
**Filed 2026-09-16. Lane G161 (wave 13).**
**Deliverables: this file + `deepseek_push/G161_plateau_registry.py` / `.out` / `G161_results.json` (committed and pushed).**

> **STATUS: REGISTERED, READY TO RUN.** The decision rules below are fixed **before** the maps
> are read and the pointings are made. Two of the three channels are executable on **public
> data today** (the G129 tSZ branch — no telescope time; eROSITA as the eRASS:1–8 data release),
> and the third (XRISM) is a GO-cycle program with its precision requirements fixed here.

**Built on (all committed):** G130 `G130_tprofile_test.py/.out/.json` (the first T-profile
confrontation: LEVEL and ENVELOPE pass, flat tail untested, 10/10), G129
`TSZ_PROPOSAL.md`/`G129_tsz_proposal.py/.out/.json` (the tSZ machinery, 5/5), G113
(the phantom-zone T_inf = 2 T_floor statement), G095 (the per-radius virial identity),
G122/G140 (the free-dust normalization a_c, the leak-test input), the X-COP ingests
(`real_research/data/xcop/`), KEPLER_GRADE_CLUSTER_PREDICTIONS.md (P7). Every number in this
file is reproduced by `G161_plateau_registry.py` (gated against the committed G130/G129 JSONs,
5/5 checks PASS).

---

## 1. THE PREDICTION RESTATED — what exactly is registered

**The statement under test (the flat tail):**

> For a cluster at the predicted level, the outer temperature profile is **FLAT** over the
> window r ∈ [1.25, 2] R500 at the level **2 T_floor**:
> **|dT/d log₁₀ r| ≤ 0.30 keV/dex-class over the window** (T_floor = μ m_p σ_floor²/(2 k_B),
> σ_floor = (G M_b a0)^(1/4)/√2, M_b at R500, canonical a0 = 9.3619e-11, μ = 0.6; per-cluster
> 2 T_floor = 2.47–5.25 keV, median 3.63 keV).

**What G130 already established (in hand, not under test):**

- **The LEVEL** — the outer X-COP T(r) (0.79–1.12 R500) stands at median **1.12 × 2 T_floor**
  at the last bin (window-mean 1.43×, entry 1.63×), six clusters already at/below the level,
  NOT at the cluster-specific virial level (exit T > 2σ below kTvir in **11/12**, median
  deficit 7.3σ) and NOT falling through the floor.
- **The APPROACH ENVELOPE** — the data track **T_ph(r) = 2 T_floor (1 + r_M/r)** across the
  measured window: median envelope residual g = 0.90, 12/12 within |log₁₀ g| < 0.3, no window
  trend; the data's own 1/r extrapolation lands on A = 0.94 × 2 T_floor (median).
- **The plateau is NOT yet FLAT in the measured window** — flat within errors 2/12 (strict
  slope test 0/12; median dT/dlog r = −4.43 keV/dex over 0.79–1.12 R500): the data show the
  *converging branch*, not the asymptote.

**The honesty box — the flat claim is STRONGER than the envelope's own continuation.**
The envelope 2 T_floor (1 + r_M/r) is still falling at 1.25–2 R500: its window slope is
**−0.94 to −3.33 keV/dex per cluster, median −1.63 keV/dex = 5.9× the 0.30 keV/dex claim**
(per cluster 3.1–11.1×). So the registered flat tail is NOT the envelope-continuation; it is
the claim that the plateau is *reached* by 1.25–2 R500. The envelope-continuation is registered
below as outcome **E** with its own decision rule — a *framework sub-reading*, not one of the
alternatives, and it fails the flat claim as registered. This is deliberate: the registry
separates "approaching the plateau" (G130, done) from "sitting on it" (G161, under test).

**The decision rule (the core of the registry):**

> **PLATEAU DETECTED** when, on the level-passing cluster set (window-mean within 2σ of
> 2 T_floor per cluster), **all three** hold:
> (i) **|median window slope| ≤ 0.30 keV/dex** (the claim's magnitude — no benefit of the doubt);
> (ii) **|median window slope|/σ ≤ 3** (consistent with 0 at 3σ);
> (iii) **≥ 9/12 clusters** each with |slope| ≤ min(0.30, 3 σ_slope) **and**
> |T_window_mean − 2 T_floor| ≤ 2 σ_level (the level consistent with 2 T_floor at 2σ).

The decision object is the **sample-median window slope** (G130's V2 convention), not a
per-cluster claim; the per-cluster rows support it. The 9/12 supermajority mirrors G130's
counting. A FAIL is a finding.

---

## 2. THE WINDOW — per cluster (computed from the committed G130/G129 rows)

θ_500 from G129's committed targets; window = [1.25, 2] θ_500; T_env = 2 T_floor(1 + r_M/r)
from G130's committed rows; s_G130 = G130's measured window slope (0.79–1.12 R500);
R_A1@2R = what "keeps falling" at the G130 rate predicts for T(2 R500)/2 T_floor;
tSZ_SNR = the Planck-143 annulus SNR over [1.25, 2] θ_500 (G129's per-bin SNRs).

| cluster | θ_500 [′] | window [′] | eRO reach [R500] | T_env(1.25) [keV] | T_env(2.0) [keV] | env slope [keV/dex] | env/claim | s_G130 [keV/dex] | R_A1@2R | tSZ SNR | tSZ slope err |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A1644 | 18.24 | 22.8–36.5 | 1.67 | 2.99 | 2.79 | −0.94 | 3.1 | −3.83 | 0.75 | 7.1 | 0.33 |
| A1795 | 15.45 | 19.3–30.9 | 1.97 | 3.83 | 3.55 | −1.35 | 4.5 | −4.48 | 0.41 | 4.0 | 0.51 |
| A2029 | 15.62 | 19.5–31.2 | 1.95 | 6.09 | 5.58 | −2.54 | 8.5 | −6.19 | 0.64 | 12.0 | 0.20 |
| A2142 | 13.50 | 16.9–27.0 | **2.00** | 6.78 | 6.16 | −3.01 | 10.0 | −8.19 | 0.40 | 13.7 | 0.16 |
| A2255 | 12.59 | 15.7–25.2 | **2.00** | 4.56 | 4.20 | −1.76 | 5.9 | −4.37 | 0.77 | 8.4 | 0.25 |
| A2319 | 19.98 | 25.0–40.0 | 1.53 | 7.06 | 6.38 | −3.33 | 11.1 | −10.56 | 0.46 | 30.9 | 0.08 |
| A3158 | 15.63 | 19.5–31.3 | 1.95 | 3.72 | 3.45 | −1.31 | 4.4 | −1.86 | 1.06 | 4.7 | 0.65 |
| A3266 | 20.15 | 25.2–40.3 | 1.51 | 5.07 | 4.69 | −1.87 | 6.2 | −4.93 | 0.58 | 6.6 | 0.33 |
| A644 | 14.70 | 18.4–29.4 | **2.00** | 4.40 | 4.07 | −1.63 | 5.4 | −10.89 | 0.00 | 0.9 | 5.44 |
| A85 | 18.40 | 23.0–36.8 | 1.66 | 4.64 | 4.28 | −1.78 | 5.9 | −3.93 | 0.75 | 7.4 | 0.32 |
| RXC1825 | 14.21 | 17.8–28.4 | **2.00** | 3.46 | 3.22 | −1.17 | 3.9 | −2.42 | 1.12 | 8.9 | 0.23 |
| ZW1215 | 15.03 | 18.8–30.1 | **2.00** | 4.54 | 4.21 | −1.61 | 5.4 | −2.89 | 1.14 | 4.6 | 0.46 |
| **median** | 15.5 | 19.5–31.2 | — | — | — | **−1.63** | **5.9** | **−4.37** | **0.75** | **7.4** | **0.33** |

*eRO reach* = the 1.25–2 R500 window truncated at the eROSITA 61′ FoV radius (30.5′): full
window for **5/12** (bold); the other 7 clusters reach 1.51–1.97 R500 in the eROSITA channel
(their outer bins come from XRISM and the tSZ branch).

---

## 3. THE INSTRUMENTS — the registry rows

**The precision budget** (the common core of all three rows). The decision object is the
sample-median slope with σ ≤ 0.10 keV/dex → per-cluster σ_slope ≤ 0.35 keV/dex. Slope fits
over the log bins (regression in log₁₀ r) give the per-bin temperature-error requirement:
σ_T ≤ **1.0%** of the window mean for eROSITA's 3 bins (1.25–1.5–1.75–2.0 R500) → ~**8.5e4**
net counts/bin; σ_T ≤ **2.2%** for XRISM's 5 bins (1–2.5 R500) → ~**2.0e4** net counts/bin
(κ_CCD = 3.0, the XMM/X-COP calibration class: eT/T ~ 7–14% at N ~ 1–3e3 → κ ~ 3–4, 3.0 taken).
The per-cluster ceiling (claim certified *per cluster*, σ_slope ≤ 0.10 keV/dex) is σ_T ≤
0.3%/0.6% — registered as the ceiling, **not** the baseline program.

### 3.1 eROSITA — the 12 X-COP T-profiles extended beyond R500 (survey channel)

**Instrument (public specs, Merloni et al. 2024 DR1-class):** 7 Wolter-I modules, 0.2–10 keV
(survey-prime 0.2–2.3 keV), effective area ~1365 cm² at 1 keV, **on-axis PSF HEW ~18″ (average
~30″ across the 61′ FoV)**, PNCCD ΔE ~ 80–150 eV FWHM class, FoV **61′ diameter (30.5′
radius)**, 50 ms frames; eRASS:1–8 all-sky scans, stacked exposure ~2–10 ks per sky position
(ecliptic-latitude dependent) + deeper legacy/pointed fields where available.

| row item | value |
|---|---|
| **window** | r ∈ [1.25, 2] R500 = [1.25, 2] θ_500 → 15.7–40.3′ per cluster (table §2); **full window in-FoV for 5/12**, FoV-truncated to 1.51–1.97 R500 for the other 7 |
| **bins** | 3 log-equal bins, edges 1.25 / 1.5 / 1.75 / 2.0 R500 (bin width ~1.9–6.7′ — ≫ the survey PSF, so PSF-mixing is a bounded correction, not a resolution limit) |
| **precision** | per-bin σ_T ≤ 1.0% (sample-level budget) → N ~ 8.5e4 net ct/bin; per-cluster ceiling σ_T ≤ 0.3% |
| **exposure** | eRASS:1–8 stack at the clusters' positions (public with the data release); legacy/deep fields (30–100 ks class) where granted; **feasibility ladder** (§3.4) |
| **decision rule** | the §1 rule on the sample-median slope + per-cluster level; the level channel (absolute T vs the M_b-computed 2 T_floor) is eROSITA's joint duty with XRISM |

**Coverage caveat (registered):** the 7 large-θ_500 clusters' outer bins (1.5–2 R500) fall
outside the single-exposure FoV radius; their eROSITA weight in the sample-level verdict is
reduced and their flat-tail claim is carried by XRISM + tSZ. Background/vignetting at 20–30′
off-axis is the dominant systematic — the control is the standard off-axis background map +
vignetting correction (stated, not a decision channel).

### 3.2 XRISM — the resolved T(r) at 1–2.5 R500 (the per-cluster channel)

**Instrument (public specs, HEASARC):** **Resolve** microcalorimeter — 1.7–12 keV, 180 cm² at
6 keV, FoV **3.1′ × 3.1′**, **energy resolution < 7 eV at 6 keV (~5 eV in flight)**; **Xtend**
CCD imager — 0.4–12 keV, 360 cm² at 6 keV, FoV **38′ × 38′** (corner reach 26.9′), < 200 eV at
6 keV; mirror HPD < 1.3′. Resolve anchors the spectral/T calibration and the non-thermal
pressure budget (the committed A2029 result: non-thermal 2.6 ± 0.3%, ≤ 2% out to R2500 —
arXiv:2501.05514-class, quoted in the repo's CLASH_XRISM_SHAPE_PROPOSAL.md).

| row item | value |
|---|---|
| **window** | r ∈ [1, 2.5] R500, resolved T(r); the flat-tail test uses [1.25, 2] R500 ⊂ it (the extra inner bins tie to the X-COP overlap for calibration) |
| **bins** | 5 log-equal bins, edges 1.0 / 1.3 / 1.6 / 2.0 / 2.5 R500 |
| **precision** | per-bin σ_T ≤ 2.2% (sample-level) → N ~ 2.0e4 net ct/bin; per-cluster ceiling σ_T ≤ 0.6% → σ_slope ≤ 0.10 keV/dex per cluster |
| **exposure** | 100–250 ks per cluster × **5–8 clusters** (the brightest, FoV-matched subset: A2029, A2142, A2319, A3266, A85, ZW1215 + 1–2 more); 2–4 Xtend pointings mosaicked to cover the 19–27′ annuli, Resolve on the core as the spectral anchor; background low (the microcalorimeter's advantage) |
| **decision rule** | per-cluster: |slope| ≤ min(0.30, 3 σ_slope) and |T̄_win − 2 T_floor| ≤ 2 σ_level; sample-level over the observed subset; **the slope-BREAK test (A1 vs A2) lives here** (§4) |

**Why XRISM closes what eROSITA cannot:** per-cluster σ_slope ~ 0.34–0.55 keV/dex at the
100–250 ks class → the envelope continuation (−0.94…−3.33 keV/dex per cluster) is excluded at
≥ 3σ *per cluster*, and the 5-bin resolved profile is what the A1-vs-A2 slope-break fit needs.

### 3.3 The tSZ cross-check — G129's Planck/ACT machinery on the same window

**Instrument (committed, G129):** Planck HFI 143 GHz (7.2′ beam, 33 μK·arcmin; all 12
clusters) + ACT DR6 f150 (1.4′, 7/12 in band); y → ΔT_CMB = T_CMB y g(x) with the committed
spectral conversion; the ~1.4× ILC penalty stated as assumption; **end-of-survey depth —
the data already exist**.

| row item | value |
|---|---|
| **window** | [1.25, 2] θ_500 ⊂ G129's decision window [θ_500, 2 θ_500] (median 15.5′–31′); Planck annuli 12–17′, 17–23′, 23–31′ (+31–40′ for the big clusters) |
| **bins** | G129's registered Planck 143 annuli (7 bins, 0–40′); the annulus [1.25, 2] θ_500 carries **median combined SNR 7.4** (per cluster 0.9–30.9; A644's outer bins dim — registered G129 caveat) |
| **precision** | slope error **0.327 per cluster (conservative 2-bin) → 0.094 pooled** over the 12 (G129's committed numbers; multi-bin fits reach ~0.15 per cluster) — log-slope units, the F-line convention |
| **exposure** | none requested — archived Planck/ACT maps; 2–4 weeks of analysis per survey |
| **decision rule** | the §1 slope rule translated to log-slope: measured y-log-slope over the annulus within **[−(q−1) − 0.4, −(q−1) + 0.4]** at 3σ (G129's F2/PASS band; q = the committed per-cluster gas-envelope exponent); **F1** (slope < −2 over [θ_500, 2θ_500] at ≥ 3σ, ~6σ pooled) fires for the steepening alternatives; the **amplitude is registered non-decisive** (G129 V1e) — the tSZ channel maps the window and the shape, not the 2 T_floor level |

**What the tSZ channel can and cannot decide (registered):** it decides A1/A2 steepening at
3–6σ pooled and confirms the shape class; it **cannot** split the flat tail P from the
envelope continuation E — both sit inside the ±0.4 band (the envelope shifts the y-slope by
only ~0.07–0.11 log units there). The P-vs-E split is the X-ray slope's job (~1.6 keV/dex
gap, ≥ 3σ per cluster with XRISM, ~3.3σ sample-level at eROSITA survey depth).

### 3.4 The feasibility ladder (the honest exposure statement)

| channel / depth | per-bin σ_T | sample-median σ_slope | what it establishes |
|---|---|---|---|
| eROSITA eRASS:1–8 survey stack | ~6% (N ~ 2.5e3; the X-COP/XMM error class) | ~0.5 keV/dex | flat accepted at 3σ; envelope excluded ~3.3σ; **claim not yet certified** (intermediate verdict, §5) |
| eROSITA legacy/deep (30–100 ks) | ~2% | ~0.16 keV/dex | claim certified ~2σ; envelope excluded ~10σ |
| XRISM 100–250 ks × 5–8 clusters | ~2.5–4% outer bins | 0.13–0.2 keV/dex (observed subset) | per-cluster envelope exclusion ≥ 3σ; claim at 1.5–2.5σ sample-level; the A1-vs-A2 break test |
| tSZ (G129, public) | — | 0.094 pooled (log-slope) | A1/A2 steepening at 3–6σ; P-vs-E not separable |

---

## 4. THE ALTERNATIVE READINGS — each with its own decision rule

**A1 — "keeps falling" (no plateau).** *Status: excluded at 11/12 already, in the current
window.* G130: exit T > 2σ below the cluster-specific virial level in 11/12 (median deficit
7.3σ); the decline is the predicted 1/r approach whose own extrapolation lands on A = 0.94 ×
2 T_floor, not on zero; continuing at the measured rate predicts T(2 R500) = **0.75 ×
2 T_floor (median; 0.00–1.14 per cluster)** — far below the plateau and below the envelope.
*Decision rule (the re-test in the new window):* **A1 fires if the measured window slope is
below the envelope band by ≥ 3σ** (slope < s_env − 3σ_slope, i.e. the fall has NOT leveled
onto the floor) **and/or tSZ F1 fires** (y-log-slope < −2 over [θ_500, 2θ_500] at ≥ 3σ). If
it fires, A1 is *restored for the outer window* — never declared dead beyond the measured
coverage.

**A2 — a steeper-than-predicted outer drop (the cap-fires reading).** The EFE cap (G127/G132:
environmental in placement, first-order in class) truncates the phantom hold-up beyond some
radius; the T-profile breaks away from the envelope and steepens back toward the classic
decline (G129: "the capped reading would steepen the profile back toward the beta family").
*Predicted marker:* the slope breaks at **r_cap ∈ (1.2, 1.5) R500** (registered band) to the
steep class (−2…−5 keV/dex). *Decision rule:* **A2 fires when (X-ray) T(2 R500) <
T_env(2 R500) − 3σ_level AND a slope break is detected (2-slope fit over [1.25, 2] R500,
break-radius free: Δslope > 3σ, break inside (1.2, 1.5) R500)**, with the tSZ arm **F1**
firing in the same window. **A1-vs-A2 split:** A1 = one steep slope throughout (no break);
A2 = envelope slope then break (Δslope > 3σ). This split needs the resolved XRISM bins; the
tSZ bins (2–3 in-window) cannot do it per cluster — registered.

**A3 — a plateau at a cluster-specific level (the free-dust normalization leaks).** The
free-dust normalization (G113 V3's open item; G122's a_c, G140's mass-ordering) leaks into
the temperature level: each cluster reaches *its own* plateau level, scattered around
2 T_floor in a way that tracks the dust amplitude. *Decision rule:* **A3 fires when the slope
test passes (flat tails found) BUT the level test fails in ≥ 5/12 clusters AND the level
residuals |T̄_win − 2 T_floor| are ordered by G122's committed a_c (Spearman ρ ≥ +0.5,
p ≤ 0.05)** — the leak signature. The tSZ channel cannot decide A3 (amplitude non-decisive);
the level is an X-ray measurement (eROSITA + XRISM, cross-calibrated against the X-COP
overlap). If the tails are flat and the levels scatter with **no** a_c ordering, the
normalization is not leaking and A3 is excluded.

**E — the envelope continuation (the framework's own weaker sub-reading).** The data keep
following 2 T_floor (1 + r_M/r) through the window (slope −0.94…−3.33 keV/dex). *Rule:* the
flat claim (i)(ii)(iii) fails, but T(2 R500) is on the envelope line (within 3σ) and the
level at the window mean is above 2 T_floor on the 1/r tail. Reading: "approaching, not yet
reached" — the registered flat-tail claim is falsified at this window *as registered*, and
the test extends outward (r → 2–3 R500, the same three channels).

---

## 5. VERDICTS

**V1 — the registry is complete.** PREDICTION restated (flat tail: |dT/dlog r| ≤ 0.30 keV/dex
over 1.25–2 R500 at the level 2 T_floor; envelope confirmed in-window by G130; the honesty
box: the flat claim is 5.9× stronger than the envelope's own continuation — E registered as a
separate outcome). INSTRUMENTS: eROSITA (3 bins, FoV-truncated window table, precision 1.0%
per-bin → N ~ 8.5e4, exposure classes), XRISM (resolved 1–2.5 R500, 5 bins, 2.2% → N ~ 2.0e4,
100–250 ks × 5–8 clusters, Resolve spectral anchor + A2029-class non-thermal pinning), tSZ
(G129's committed machinery: window SNR 7.4, slope error 0.094 pooled, F1/F2 lines,
amplitude non-decisive). DECISION RULES fixed (slope 0 at 3σ, level 2 T_floor at 2σ,
≥ 9/12, claim-magnitude clause). ALTERNATIVES A1/A2/A3/E each with its own firing rule.
**5/5 checks PASS** (`G161_plateau_registry.py`/`.out`).

**V2 — the claimed discrimination power: which measurement decides which alternative.**

| question | deciding measurement | power (registered) |
|---|---|---|
| flat vs envelope-continuation (P vs E) | **XRISM** per-cluster slope (σ_slope 0.34–0.55 keV/dex); eROSITA sample-median (0.5 survey / 0.16 deep) | the ~1.6 keV/dex gap: ≥ 3σ per cluster (XRISM), ~3.3σ sample (eROSITA survey), ~10σ (deep); tSZ cannot split them |
| flat vs A1 keeps-falling | X-ray slope below envelope band ≥ 3σ **and/or** tSZ F1 (slope < −2, ~6σ pooled) | A1's T(2 R500) = 0.75 × 2 T_floor (median) vs 1.0 — the level test alone separates at ≫ 2σ |
| A2 cap-fires | X-ray T(2 R500) < T_env − 3σ **+ the slope break at r_cap ∈ (1.2, 1.5) R500** (XRISM bins); tSZ F1 as the cross-arm | break Δslope > 3σ (XRISM, 5 bins); A1-vs-A2 split = break vs no break |
| A3 dust-normalization leak | X-ray level residuals vs **G122's a_c** (Spearman ≥ +0.5, p ≤ 0.05) | level = eROSITA+XRISM absolute T; tSZ amplitude registered non-decisive — tSZ cannot decide A3 |
| the 2 T_floor **level** | X-ray absolute T (eROSITA + XRISM, X-COP-overlap cross-calibration) vs the M_b(R500)-computed 2 T_floor | 2σ per cluster, ≥ 9/12; the tSZ amplitude is a consistency test only (G129 V1e) |

**V3 — the honest statement: CONFIRMED on the level, PENDING on the flat tail.**

> **CONFIRMED (G130, in hand):** the plateau LEVEL — median last-bin T = 1.12 × 2 T_floor,
> window-mean 1.43×, on the envelope 2 T_floor (1 + r_M/r) at median residual g = 0.90
> (12/12 within 0.3 dex), the cluster-specific virial level excluded at > 2σ in 11/12.
> **PENDING:** the FLAT TAIL — 2/12 flat within errors in the 0.79–1.12 R500 window (strict
> slope 0/12), and the flat claim (|slope| ≤ 0.30 keV/dex at 1.25–2 R500) is 3–11× stronger
> than the envelope's own continuation there. The plateau's *existence at the predicted
> level* is a measured result; the plateau's *flatness* is an open, registered, falsifiable
> claim.

**What closes it, and who runs it (the run order):**

1. **The tSZ cross-check — TODAY, any SZ analyst, zero telescope time.** G129 files the full
   pipeline on public Planck/ACT maps; the window [θ_500, 2θ_500] carries slope error 0.094
   pooled → A1/A2 steepening decided at 3–6σ; 2–4 weeks per survey. First-available
   cross-check mapping the same window.
2. **eROSITA — the 12 X-COP T-profiles beyond R500, as eRASS:5–8 land** (public with the
   data release; the eROSITA team and the wider community via the released data). Survey
   depth: sample-median slope ~0.5 keV/dex → intermediate verdict (flat at 3σ, envelope
   excluded, claim uncertified); legacy/deep fields (30–100 ks) lift it to claim
   certification (~2σ).
3. **XRISM — the per-cluster closure, via the GO/AO cycles** (any PI through the
   NASA/JAXA/ESA guest-observer program): 5–8 clusters × 100–250 ks, Xtend mosaic +
   Resolve anchor → per-cluster σ_slope ≤ 0.2 keV/dex, the envelope excluded at ≥ 3σ per
   cluster, the A1-vs-A2 slope-break test, and the per-cluster flat-tail certification.

The three channels are complementary by design: **tSZ now** (shape/steepening, sample-level),
**eROSITA next** (the level + sample flatness on the 12), **XRISM to close** the per-cluster
claim and the mechanism split. The decision rules in §1 and §4 are fixed; a FAIL on any of
them is a finding, and the outcome is registered either way.

---

*All numbers from the committed G130/G129 rows, reproduced by `G161_plateau_registry.py`
(gates: 12/12 clusters from G130_results.json with median T_inf = 3.67 keV — G130's 3.63-keV
class; θ_500 and slope errors from G129_results.json; 5/5 checks PASS). Instrument specs:
eROSITA per Merloni et al. 2024 DR1-class (on-axis HEW ~18″, ~1365 cm² at 1 keV, 61′ FoV);
XRISM per the HEASARC mission page (Resolve 180 cm²@6 keV, 3.1′×3.1′, < 7 eV; Xtend
360 cm²@6 keV, 38′×38′, < 200 eV). Exposure classes are requirements + feasibility classes —
the proposers confirm the per-bin count rates with the official exposure calculators at run
time. A FAIL is a finding.*
