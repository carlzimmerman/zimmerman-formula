# CFG190 — MUSE-DARK II (bTFR at z ≈ 1) against MUSE-DARK III (a₀ rising with z): can one a₀(z) law fit both?

- **Criteria:** frozen in `FROZEN_CRITERIA.md` (8f251a5a9), before any number.
- **Inputs are ABSTRACT-LEVEL:** the data chat's notes (6aa32738c, 44103dfde), read through a page summariser and unverified against the PDFs. No per-galaxy table was read.
- **Script:** `cfg190_muse_dark.py`, under a second.
- **Runs:**
  - The main run passes both controls and exits 0.
  - MUTATE=1 sets II's offset to −0.38 dex, the value III's rise implies in the deep regime. III's own law then fits both, at y = 0 and y = 0.3, so the headline changes, as required; exit 0.

## Bottom line

**No single a₀(z) law fits both MUSE-DARK II and MUSE-DARK III at any declared acceleration regime. The two are mutually inconsistent under any common a₀(z). So a ROBUST rise is not established, and the record's June verdict on III (non-diagnostic, method-split) stands, now within one collaboration.**

- **The two measurements:**
  - III: log a₀(0.87)/a₀(0) = +0.377 ± 0.025 dex.
  - II: bTFR offset along the mass axis at z ≈ 1 = 0.00 ± 0.06 dex.
- **Each law, mapped to II through P2 at fixed g_obs.** The pull is (predicted − measured)/σ. y = g_bar/a₀ at II's 2 R_e is unread, so it is bracketed.

  | law | against III: predicted (pull) | against II: deep | y = 0.3 | y = 1 |
  |---|---|---|---|---|
  | flat | 0.000 (−14.9) | 0.000 (0.0) | 0.000 (0.0) | 0.000 (0.0) |
  | a₀ ∝ E(z) | +0.219 (−6.2) | −0.253 (−4.2) | −0.184 (−3.1) | −0.109 (−1.8) |
  | T = t(z)/t₀ | −0.333 (−28.2) | +0.373 (+6.2) | +0.174 (+2.9) | +0.086 (+1.4) |
  | III's own linear law | +0.377 (0.0) | −0.413 (−6.9) | −0.323 (−5.4) | −0.206 (−3.4) |

  - Flat fits II and misses III.
  - III's own law fits III and misses II, by 3.4–6.9σ depending on how deep in the MOND regime II's galaxies sit at 2 R_e.
  - a₀ ∝ H(z) misses III by 6.2σ.
  - T misses III by 28σ.
- The mapping's sensitivity is d ln g_bar/d ln a₀ = −1/(2y + 1): −1 in the deep regime and −1/3 at y = 1 (control C2). That sensitivity is why II's constraint weakens outside the deep regime.

## Reading

- **At least one of the two MUSE-DARK results is dominated by something other than a common a₀(z).**
- **The obvious candidates differ between the papers:**
  - III fits M* inside the same DC14 disc–halo model as its halo, and fixes the interpolation function;
  - II uses photometric M* and scaling-relation gas;
  - the fields differ (UDF against lensing clusters);
  - the quantities differ: a RAR built from model curves beyond 2 kpc, against a velocity–mass relation at 2 R_e.
  - Both use Dalcanton–Stilp pressure support and fitted-model velocities, the same model-versus-data point found for KURVS (27bcce5a4).
- **The June confrontation's grade stands, strengthened:** the rise is method-localised (RAR fits), while the bTFR arm is flat, now within the same collaboration at the same redshift.
- **The standing rule** ("a ROBUST rise kills flat a₀(z)") is not triggered: a rise that the same team's bTFR does not show is not robust.
- **Nothing here favours flat a₀ over the other laws.** Flat is excluded by III at face value (−14.9σ), and III is the result in question.

## Q2 — circularity: UNDECIDED without tables (declared)

- **The mechanism:** III's a_bar comes from an M* fitted inside the DC14 disc–halo model, so the a₀ it fits with a fixed interpolation function can inherit the halo-profile prior.
- **What would decide it:**
  - III's per-galaxy fitted M* against photometric M*;
  - a₀ across the seven halo families listed on the DARK site;
  - baryon-only fits.
- These need the per-galaxy tables, requested through the data chat if its user agrees. Nothing is downloaded without a go in this chat.

## Declared limits

- abstract-level inputs;
- II's median redshift taken as 1.0;
- the intercept–slope correlation of III's fit ignored in the ratio's error;
- the y bracket (deep, 0.3, 1.0) declared, not measured;
- II's offset read as along the mass axis at fixed V, as its text says (Sect. 7.1, through the summariser).

κ = ½ and Ω_c h² stay fitted. Nothing here says the data favour any model, or that the theory is closed.

## After the MUSE-DARK table extraction (appended 2026-09-29; the text above is unchanged)

- **Two relayed input corrections, checked against the papers' arXiv HTML text** (three reads; reading only, nothing downloaded). Script: `cfg190_posthoc_errors.py` (POST HOC, labelled).
- **(1) VERIFIED: III's errors are 95% confidence intervals, not 1σ.**
  - Sect. 3.1: "with the errors denoting the 95% confidence intervals (CI) from our MCMC fits". Sect. 3.2: "the 95% CI".
  - The frozen run took them as 1σ. With 1σ = the half-width divided by 1.96, σ(log ratio) falls from 0.0252 to 0.0129 dex.
  - The pulls against III roughly double: flat −14.9 → −29.3; a₀ ∝ E(z) −6.2 → −12.2; T −28 → −55.
  - The pulls against II are unchanged. **The headline stands: no law fits both at any declared y.**
- **(2) NOT FOUND: the claim that II adds a ±0.16 dex uncertainty for the local (Lelli+2019) zero point (Sect. 7.3).**
  - In II's text the only 0.16 dex is the bTFR's orthogonal intrinsic scatter (Table 3, Sect. 7.1).
  - Section 7.3 ("Evolution of the bTFR") contains no such statement, and II adds no uncertainty to Δb = 0.00 ± 0.06 dex for the local reference.
  - The frozen II input therefore stands.
- **Sensitivity (reported, not a correction).** II's ±0.06 is a statistical error, and II calls its bTFR "more indirect". Its systematic floor against the local relation is not quantified: different M*, gas and velocity definitions enter at the two epochs.
  - If an unstated ±0.16 dex were added in quadrature (0.17 in total), III's own law would fit both at y ≥ 0.3: pulls against II of −1.9 at y = 0.3 and −1.2 at y = 1, against −2.4 in the deep regime.
  - So **"mutually inconsistent" holds as stated only if II's quoted error is its whole error against the local relation.** If II has an unstated systematic of about 0.16 dex, the inconsistency survives only in the deep regime.
- **Circularity (Q2) stays UNDECIDED.** The extracted tables (7e43e4fdd, `data_assembly/arxiv_tables/musedark_II_III/`) include no per-galaxy table in II or III.
  - The extraction reads III's DC14 fits as parameterised by log(M*/M_halo), with no SED prior, so III's M* is tied to the halo by construction.
  - Paper I's raster figure shows dynamical M* about 0.11 dex below the SED values.
  - III gives a₀ only for DC14 (2.38), the best-evidence halo (2.61) and MOND (2.19). There is no baryon-only fit.
- **Also corrected:** II's bTFR intrinsic scatter is 0.16 dex. The 0.10–0.12 dex in the data chat's timeline note is the sTFR's.
