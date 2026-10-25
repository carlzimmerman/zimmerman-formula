# HG2_kids_lowg_hot_gas — RESULT: UNDERPOWERED by the frozen rule (power 0.45 < 0.50); the measured D is negative

Frozen criteria 2546ffbd10 (committed alone, before any script or number). Model-free and footing-independent: the graded
statistic uses no a₀ (a₀ enters only K1, the CFG829 reproduction). κ = ½ FITTED; nothing here says the data favour the
framework or ΛCDM; not "theory closed".

**Question.** At matched σ, do KT2017 groups with an eRASS1 hot atmosphere sit further above a low-acceleration reference
than groups without one, once their hot gas is counted? The reference is the KiDS-1000 isolated blue-lens RAR data
(Brouwer+21 colour bin 1), interpolated point to point with no law. It reaches 10^−14.9, which fixes HG1's coverage wall.

## Result

| item | value |
|---|---|
| K1 (CFG829 blue A reproduced) | 1.0165 ± 0.0859 vs 1.016 ± 0.086 ✓ |
| K2 / K3 / K4 / K5 | ✓ / 4.3e-10 ✓ / 190 groups, 14 BRIGHT, 176 FAINT ✓ / 2e-15 ✓ |
| groups inside the reference's g_bar range | **188 of 190** (HG1: 8): 14 BRIGHT, 174 FAINT |
| in shared σ bins | 11 BRIGHT / 105 FAINT (passes the ≥ 6 rule) |
| pre-flight power for D = +0.20 dex | **0.45** (rule needs ≥ 0.50) |
| D (primary) | **−0.294 dex, 95% [−0.511, −0.076]** (10 of 30,000 reference draws floored) |
| **class** | **UNDERPOWERED** (power rule only) |
| MUTATE (a) shuffle | 0.925 not HOT-TRACKS-sized ✓ |
| MUTATE (b) plant +0.30 | D +0.006 → UNDECIDED, not HOT TRACKS ✗ (see below) |

Variants (reported, not graded), all negative: Nm ≥ 10 −0.226; H0 = 73 −0.296; Υ_K 0.5 −0.338, 0.8 −0.223; X-FAINT gas
0.1 M★ −0.248; reference g_bar −0.2 dex −0.190, +0.2 dex −0.379; all-isolated reference (D5) −0.343.

**The class is UNDERPOWERED, and only because of the power rule.** The power came out 0.45 against a 0.50 bar, so the frozen
rule says UNDERPOWERED. The measured interval's upper bound (−0.076) is below +0.10. With adequate power that would be
HOT DOES NOT TRACK. That class is **not** claimed. The sign is opposite to the hypothesis in every variant: X-bright groups
show **less** excess than X-faint groups at matched σ, not more.

**MUTATE (b) failure, as frozen.** The plant adds +0.30 dex to a real D of −0.294. It moved D by exactly +0.300
(−0.294 → +0.006), so the pipeline responds correctly. But a plant on real data only reaches HOT TRACKS when the real D is
near 0. This control design is inherited from HG1. It is reported as a failure, not amended after the fact.

## Why D is negative (post-run diagnostic, NOT frozen, not graded: `hg2_postrun_diagnostic.py`)

- **At matched σ the two arms have about the same g_obs.** Bin by bin, BRIGHT minus FAINT runs from −0.15 to +0.07 dex.
  BRIGHT is lower in the three lowest-σ bins, where its groups are richer and larger.
- **Counting the hot gas lifts BRIGHT g_bar by 0.7–1.35 dex.** The β-model gas inside r is 2–14× the stars. Each BRIGHT
  group therefore moves up the rising reference curve, and its Δ falls.
- **With BRIGHT hot gas removed from g_bar, D = −0.059.** Most of the negative sign comes from the gas count itself.
- **Reading.** A detected hot atmosphere does not come with extra pull at fixed σ. Once the measured hot gas is counted as
  baryons, the X-bright groups move toward the reference, not away from it.
- **Caveat.** Gas-to-star ratios of 8–14 in the σ 80–160 km/s bins are high for groups. A cluster-calibrated eRASS1 Mgas500
  or the β-model may overstate the gas there, which would push D negative. This was not tested.

## Reported only (not graded)

- Unstratified median Δ against blue lenses: FAINT +0.181 (n 174), BRIGHT +0.389 (n 14).
- The FAINT level matches the record's group excess (f22: +0.20 to +0.23). It is not interpretable on its own: lensing at
  30 kpc–3 Mpc and 3σ²/r at the half-mass radius can differ by a level offset (FROZEN §6). That offset cancels in D only.
- The unstratified BRIGHT median is high because the BRIGHT arm includes cluster-σ systems (σ 639–800). Those systems have
  no FAINT partner and fall outside the shared bins.

## What it means

- The hot-atmosphere selector gets **no support** at group scale from this test. No variant has a positive D.
- The frozen class is UNDERPOWERED. "HOT DOES NOT TRACK" is not claimed.
- The selector is **not closed**. A test with more X-bright groups is needed: eRASS1 group-scale catalogues, or a deeper
  X-ray stack. A per-group check of the eRASS1 gas masses is also needed, given the high gas-to-star ratios.
- This is a correlation test, footing-independent, and post-hoc motivated (disclosed in FROZEN §6).

Files: `hg2_kids_lowg_hot_gas.py` (`.out`, `.json`, `_MUTATE.out`, `_MUTATE.json`); `hg2_postrun_diagnostic.py` (`.out`,
`.json`). Run: `python3 hg2_kids_lowg_hot_gas.py`; `MUTATE=1 python3 hg2_kids_lowg_hot_gas.py` (exits 1 only if both
controls behave; here it exits 0, disclosed above); `python3 hg2_postrun_diagnostic.py`. About 30 s each, one thread.
