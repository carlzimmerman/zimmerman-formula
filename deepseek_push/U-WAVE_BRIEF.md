# U-WAVE BRIEF (conductor tick 2026-09-24, spawned from the landed T-wave)

Successor wave to T01/T02/T03. 3 conductor-run lanes (delegate_task absent from
this session's toolchain; Q/R/S/T precedent). Distinct OPEN doors only — no
KILLED door rehashed (consulted register KILLED column: two-moment closure 5sig,
J03, J04, NSE a0-loading, kurtosis-3 — none touched).

## U01 — MIGHTEE deep-band structure test (Q02 analog on the mirror channel)
Door: S02 found the MIGHTEE deep a0_eff/a0 = 2.1638 vs SPARC anchor 0.8314
(z=+6.99, CHANNEL-DEPENDENT). Open question: is the +1.33 offset a CONSTANT
zero-point within the MIGHTEE deep band, or g_bar-dependent (onset-like)?
- Data: data2/mightee2025_rar_digitized_points.csv (80 rings; 72 deep, lg<-0.699).
- Bins pre-registered: two bins split at lg = log10(g_bar/a0) = -1.0; bin1 = lg < -1.0,
  bin2 = -1.0 <= lg < -0.699 (the deep cut edge).
- K1 (power): any bin n < 15 -> NOT-RESOLVED -> UNDECIDABLE, no verdict forced.
- K2 (both-ways, pre-registered): slope of a0_eff/a0 vs bin-centre lg over the two
  bins; slope SE = colour-group bootstrap (B=2000, seed 20260924). |z_slope| >= 3
  -> STRUCTURE-ONSET within MIGHTEE channel; else CONSTANT-WITHIN-CHANNEL.
  Either outcome a result; no re-tuning. Q02 SPARC slope 0.3396+/-0.1204 compared
  informationally (z_diff reported, not gated).
- K3 (machinery): full-sample Delta matches L06 stored (rel 1e-6); deep ratio
  matches N05 stored a0eff_a0 (1e-9). Else lane INVALID.

## U02 — N05 arbitration card refresh under the channel-dependent model
Door: register row "Deep-bar kill test (N05) | OPEN — arbitration program card
registered" — its N-requirements predate the channel-dependence finding
(S02 sharpened z to +6.99/+7.41; T03: offset is DIFFUSE, a population property).
- Pre-registered formulas (fixed BEFORE running, all inputs runtime-read from
  N05_results.json / Q02_results.json / S02_results.json; any missing key ->
  lane INVALID, no invented numbers):
  F1: per-ring noise sigma1 = stored ensemble se_ring * sqrt(N_stored) per channel.
  F2: per-channel 5-sigma attribution N = ceil( (5 * sigma1 / |delta_a0E|)^2 ),
      delta in a0E units (SPARC 0.27588, MIGHTEE 1.16382, stored).
  F3: cross-channel difference resolution, equal new-N n per channel:
      n = ceil( (5 * sqrt(sigma1_mig^2 + sigma1_sparc^2) / |delta_mig - delta_sparc|)^2 ).
  F4: verification — F2-on-SPARC must reproduce N05 stored N_req_ring_level
      (1655.8515) within 1%; else MISMATCH flag (honest).
- K1: all inputs runtime-read (missing -> INVALID).
- K2: F2-vs-N05 recompute within 1% (MISMATCH flag either way).
- K3 (both-ways): refreshed card recorded either way; NO new physics claim; the
  H_A/H_B slope-channel N (N05 stored 11699.22) stands, with the banked Q02/R03
  bootstrap-vs-multinomial finding (presence-based 1.26-1.33x SMALLER) applied as
  a conservative bracket [N, N*1.33^2] recorded as caveat, not a new kill.

## U03 — MIGHTEE digitization robustness audit (evidence re-audit on the named pain)
Door: the z=+6.99 channel verdict rests on 80 DIGITIZED rings from a published
figure. Is the CHANNEL-DEPENDENT verdict robust to figure-digitization error?
- Pre-registered tolerance: ±0.02 dex per axis, iid uniform (stated assumption:
  standard figure-digitization resolution). B=2000, seed 20260924.
- K1 (machinery): unperturbed deep ratio matches N05 stored (1e-9).
- K2 (both-ways, pre-registered): per draw, perturb both axes ±0.02 dex uniform,
  recompute deep ratio and z_vs_q02; fraction of draws with |z| < 3 >= 50% ->
  DIGITIZATION-FRAGILE (channel verdict at risk); else DIGITIZATION-ROBUST.
  y-only axis reported as secondary (informational). sd(ratio) across draws vs
  stored colour-group SE reported. Either outcome a result.
- K3: no group-level or covariate law claimed (n=72 digitized rings).

## House rules 1-10 apply (LOOP_CONDUCTOR.md). Files claimed: U01_*, U02_*, U03_*.
Exit 0 only on real passes; honest FAILs preserved verbatim; no lane commits.
