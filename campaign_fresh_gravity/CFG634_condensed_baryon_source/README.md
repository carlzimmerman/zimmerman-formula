# CFG634: the condensed-baryon source (H-CB). Verdict: NOT DECIDED (reservoir-limited). The static gates cannot tell H-CB from candidate B; the unsettled-reservoir rule decides them, and no single rule passes groups, clusters and the Bullet together

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (1fea20013). Date 2026-10-11.
- **Settings:** κ = ½ is FITTED. Footings are written canonical / alt and never pooled. "Cold energy" throughout. The cold energy's mass is still required. No particle species. Not "theory closed". Nothing here says the data favour the framework.
- **Scripts** (run from the repository root with `OMP_NUM_THREADS=1 nice -n 10`; one process, below 1 GB):
  - `cfg634_static.py` covers T1, T2, T3 and T6 (about 5 s).
  - `cfg634_bullet.py` covers T4 (about 3 s).
  - `cfg634_halo.py` covers T5 (about 10 s).
  - Each writes `.out` and `_results.json`. The MUTATE controls run inside the same pass. **All 16 checks pass.**
- **Data:** read only from disk. Nothing was downloaded.
- **Number sources:** every number below comes from the three JSONs.

## Hypothesis
The law's phantom (settled cold energy) is sourced only by condensed baryons: stars plus HI/H2. Hot X-ray gas gravitates, but it sources no phantom. Cold energy that has not settled stays an ordinary collisionless reservoir, holding the supply minus what has settled. The switch still reads baryons, so MS1 is kept: a gate on ρ_condensed is a baryon state function and is blind to the cold energy. What changes is which baryons source the phantom. The split adds no fitted constant, but it does need a phase label (X-ray gas vs stars + HI/H2) that an action would have to supply. That part is open.

## Prior record (grep done before freezing)
No committed lane has excluded hot gas from the source inside halos. The closest are:
- **CFG372 / 374 / 376.** PM runs on CFG366's engine, with a Jeans-filtered phantom source. CFG376 split the collapsed phase into filtered hot halo gas and unfiltered stars + cold gas. All three carry the k_J bug (5819dd616). CFG372's pass is withdrawn. They give the direction only: less hot gas in the source means less small-scale excess.
- **CFG432.** The unsettled X-COP mass is more concentrated than the gas.
- **CFG543.** Tian+26 M_bar includes about 8% observed X-ray gas.
- **CFG629.** The reservoir closes most of the Bullet main-cluster core.

## Phase split (declared from the data columns, in the criteria, before any number)
- **SPARC:** rotmod Vdisk, Vbul and Vgas, so hot = 0.
- **Tian+26 groups:** hot = 0.08 M_bar, bracketed 0.04–0.16.
- **X-COP:** hot = MGAS. Condensed = MSTAR, or the audit's imputed stars. Condensed is a median 0.062 of the baryons at the headline radius (range 0.035–0.071).
- **Bullet:** hot = ICM + cool core. Condensed = stars.
- **Halo model:** condensed = max(M*, 0.10 f_b M_ta), with 0.10 the census floor (stars + cold gas). Bracket HC-2 uses stars only.
- **KiDS:** Mgal = M*(1 + f_cold) already, so hot = 0.

## Results per gate (canonical / alt)

| gate | H-CB result | record candidate B (same pipeline) | label |
|---|---|---|---|
| **T1 SPARC** | rms 0.1003 / 0.1013 dex | 0.1003 / 0.1013 (Δ = 0) | **PASS**. This is a check: the rotmod has no hot term, so the source is B's |
| **T2 groups, R0 (primary)** | +0.067 (Z 1.86) / +0.050 (Z 1.38) | +0.060 / +0.043 (CFG543 P2) | **PASS** (CLOSES). It is **RESERVOIR-DEPENDENT** and **HOT-FRACTION-DEPENDENT** |
| T2 hot 0.04 / 0.16 | +0.063 / +0.074 (Z **2.06**, ABOVE); alt +0.047 / +0.058 | | 0.16 fails canonical, marginally |
| T2 hot shape β (r_c = Re) / Re k = 1.563 | +0.067 / +0.049; alt +0.051 / +0.032 | | close |
| T2 RN (NFW c = 3–5 reservoir) | −0.165 to −0.182 (Z −4.1 to −4.4), both footings | −0.174 / −0.173 | **FAIL** (BELOW) for H-CB and for B |
| T2 RI | +0.067 / +0.050 | +0.060 / +0.043 | CLOSES. Inside groups the settled phantom exceeds the cosmic share |
| **T3 X-COP, R0** | η = M_HSE/M_model **3.97 ± 0.12 / 3.81 ± 0.11** | 1.82 / 1.68 (CFG624 NCE) | **FAIL**. Stars are only 6% of the baryons |
| T3 RI (identity) | η 1.057 ± 0.031 (both) | 1.057 (identical; CFG4 identity 0.9457) | **PASS** at the headline radius; the inner band 200–420 kpc FAILS (1.535) for both |
| T3 RN c = 4 | η 0.895 / 0.898; inner 0.890 / 0.897 (PASS); b = 0.2: 1.12 | 1.082 / 1.115; inner **1.46 / 1.58 (FAIL)** | **PASS**, with the inner band passing too. c = 3: 0.94, inner 1.02. c = 5: 0.86, inner 0.80 (TENSION) |
| **T4a Bullet, gas-tied share** of settled cold energy inside 250 kpc | **0** (checked: doubling the hot gas leaves it unchanged; B's changes) | 0.66–0.67 (main), 0.48 (sub) | H-CB's settled mass rides with the galaxies at any α |
| T4b aperture Δκ (galaxies − plasma), R0 | main +0.000 (z −3.65), sub −0.017 (z −2.53) | α = 0: +0.021 / +0.001 (z −3.41 / −2.30) | **FAIL** (both) |
| T4b RI | main +0.102 (z −2.45), sub +0.110 (z −0.89) | identical | TENSION (B1); PASS on BASE |
| T4b RN | main +0.277 (z −0.39), sub +0.019 (z −2.06) | α = 0: +0.238 (−0.85) / −0.008 (−2.41) | TENSION (B1). PASS on B2 and B3; on alt, B3 is TENSION |
| T4b B at α = ∞ (proxy: B's gas-sourced phantom moved onto the plasma) | | main −0.027, sub −0.053 | reported only. Lensing is pulled to the gas, as in CFG621 |
| T4c main M(<250 kpc) / Paraficz+16 (PROVISIONAL) | R0 0.20 / 0.21; RI 0.87; RN 0.86 | R0 0.32 / 0.35; RN 0.83 | the sub stays at 0.11–0.28 (input mass, CFG629) |
| **T5 halo model (CONTEXT ONLY)**, primary HC-1, census edge | E −0.001; **R(k = 1) 0.593 / 0.676**; R(0.3) 0.924 / 0.933; σ8 ratio 0.975 / 0.978 | E **+0.715 / +0.883**, R(1) 1.716 / 1.885 | frozen class **REDUCED**. In plain terms, the excess is gone and the sign flips to a 32–41% deficit at k = 1 |
| T5 emergent edge / HC-2 / reservoir spread* | R(1) 0.24 / 0.28; 0.969 / 0.972 (REMOVED); 0.635 / 0.723 | emergent edge: 0.988 / 1.086 | variant-sensitive: R(1) spans 0.24–0.97 (* is a post-freeze bracket with no verdict weight) |
| **T6 KiDS / isolated lenses** | no change: the record's lens source is already stars + cold gas (f_cold 0.11–9.9, median 0.21) | CFG529: the census edge FAILS f30 on both footings | **NO CHANGE**. A hot-gas escape (CFG61 class) keeps only 0.35 / 0.33 of its boost under H-CB. The early-type age signal (CFG585/631) is untouched |

**Mass profiles in the halo model** (M_F/M_ΛCDM at 0.1 / 0.3 r_ta, canonical):

| log M_ta | B | H-CB | H-CB edge (r_e/r_ta) |
|---|---|---|---|
| 13 | 0.75 / 1.59 | 0.53 / 0.96 | 0.51 |
| 14 | 0.76 / 1.75 | 0.41 / 0.81 | 0.75 |
| 15 | 0.57 / 1.25 | 0.40 / 0.67 | 1.00 |
| ≤ 12.5 (galaxies) | identical | identical | — |

H-CB moves cluster halos from too concentrated at 0.2–0.5 r_ta to too diffuse. It removes CFG556's driver, but it overshoots.

## MUTATE and controls (all pass)

**M1: hot gas restored to the source reproduces the record's candidate-B numbers.**

| gate | reproduced | to |
|---|---|---|
| T1 | CFG624 B rms | 1e-9 |
| T2 | CFG543 P2: +0.05961 / +0.04349 | 1e-4 |
| T3 | CFG624 NCE η 1.819602 / 1.678747, and CFG4 identity 0.945725 | 1e-6 |
| T4 | CFG625 static B1 M(<250)/P16, and CFG629's RN 0.84 | 1e-6 |
| T5 | CFG556 E +0.7151 / +0.8829, and its emergent edge +0.0770 / +0.1458 | 1e-3 |

**M2: all baryons removed from the source breaks galaxies.**
- SPARC rms rises to 0.397 on both footings.
- Groups go to +0.81 (ABOVE).

**M3 (teeth):** H-CB moves R(k = 1) by 1.12 / 1.21 relative to B.

**Controls:**
- The audit profile code reproduces the audit's g_baryon to 2e-16.
- The aperture integrator matches an analytic Plummer sphere to 7e-5.

## What depends on the reservoir profile (it is NOT derived)
- **Clusters (T3) and the Bullet (T4) are set by the reservoir, not by the phantom source.**
  - The no-source control (M2) gives the same T3 and T4 answers as H-CB and B under RI and RN. For example, T3 RN η is 0.86 for no source against 0.90 for H-CB, and T4 RN main Δκ is +0.289 against +0.277.
  - Stars are only about 6% of the cluster baryons, so the phantom they source is small next to the reservoir.
  - Whether H-CB "passes" clusters is therefore a statement about the reservoir rule.
- **Groups need the reservoir OUTSIDE the members (R0 or RI). Clusters need it inside, concentrated (RI or RN).**
  - With one NFW rule (RN), groups fail at Z ≈ −4.3.
  - RI (cold energy inside r = max(settled, cosmic share of enclosed baryons)) is the only single rule that passes T2 and the T3 headline. It fails the X-COP inner band (1.535) and is in TENSION on the Bullet main aperture (z −2.45).
  - **Joint gate J: NO SINGLE RESERVOIR RULE** passes T2, T3 and T4b together. This is equally true of candidate B. The record's split convention (R0 for galaxies and groups, RI for clusters) is why both "pass" in the record.
- **T5's sign flip depends on the halo-model reservoir placement and on the edge variant**, with R(1) spanning 0.24–0.97. It is context only either way.
- **What does NOT depend on the reservoir:**
  - T1 and T6 (no change).
  - T4a (gas-tied share 0).
  - The T2 phantom loss of +0.007 dex from dropping the 8% hot gas.

## Reading
- **H-CB passes every gate it cannot affect.**
  - Galaxies are unchanged by construction: SPARC and KiDS sources hold no hot gas.
  - Groups move by +0.007 dex and still close at the stated 8% hot fraction. At 16% they fail canonical marginally (Z 2.06).
- **Where it does act, it does two real things.**
  - **Bullet:** no settled cold energy is tied to gas. That removes, structurally, the mechanism by which α > 0 failed in CFG621–623: at any α the re-settling target is the galaxies. The static aperture numbers, however, equal B at α = 0. The merger-vs-galaxy α tension is dissolved only in principle; it is not scored, and no grid was run.
  - **Growth (halo model, context):** CFG556's +72–89% excess at k = 1 disappears and becomes a 32–41% deficit, which is the S8-low direction. The size is not robust.
- **H-CB does not break groups, and it does not fix clusters.**
  - Clusters, the Bullet core and the shear-side halo shapes are all decided by the unsettled reservoir's radial profile.
  - The record has never derived that profile, and no single bracket passes groups, clusters and the Bullet together. That failure applies to candidate B as much as to H-CB.
  - Honest verdict by the frozen rule: **NOT DECIDED (reservoir-limited)**. It is not a clean fail (T2 and T3 each pass under some bracket) and not a survival (gate J fails).
- **The early-type tensions get no help.**
  - SLUGGS centrals, KiDS inner mass and the age signal are untouched.
  - The hot-gas escape is weakened further, to about ⅓ of its boost.

## The decisive native test (spec only, NOT run: the CFG596 1024³ job occupies the machine)
- **Engine.** `cfg634_pm.py` = `cfg596_pm.py` at its production freeze (6323b630f), with two changes and nothing else:
  1. In `cover_balls(..., want_fret=True)` the per-catchment source weight `tab` becomes the condensed retention `min(fret_of(lM), 0.10)` instead of `fret_of(lM)`. This is the HC-1 rule: the census floor holds stars + cold gas.
  2. In `x_supply` the census edge uses that condensed retention, r_M from f_c f_b M_ta and ln(1 + f_c f_b/(1 − f_b)).
  - Particles, the switch, R5 and the supply are unchanged.
- **Runs.**
  - The same seed and box as CFG596 production (L100 N1024, z = 1, 0.5 and 0 snapshots), canonical first, then alt.
  - S0 is shared with CFG596.
  - The MUTATE run uses `tab = fret_of` and must reproduce CFG596's spectra bit for bit.
  - A no-source run (`tab = 0`) is a control only.
- **Scoring (frozen now, unchanged from CFG596).**
  - `cfg596_native.py` scores the gravitating P(k, z) against the real KiDS-1000 / DES Y3 ξ± on the framework's own pipeline.
  - The statistic is Δχ²(H-CB − S0), with CFG592's class labels.
  - CFG596's T-OWN tooth applies: an injected framework boost must give χ² ≥ 9.
  - Growth gate on the gravitating field (CFG555 rule): max|P/P_S0 − 1| ≤ 0.10 for k ≤ 1.
- **Pass and fail.**
  - **H-CB fails** natively if it is EXCLUDED, or if the gravitating-field growth gate fails in either direction. A deficit beyond 10% counts as a fail, exactly like an excess.
  - It **passes** the shear side only if it is CONSISTENT on a diagnostic survey on both footings.
- **Machine.** Expected memory equals CFG596 production (about 29 GB RSS). It must run alone, after CFG596 finishes.
- **What it cannot settle.** The PM still places the unsettled reservoir by its own dynamics (collisionless particles). It is the first framework-native measurement of that reservoir's profile, which is the quantity every static gate here turned on.

## Inherited inputs (labelled)
- T5 uses the Tinker08 HMF, Tinker10 bias, Duffy08 c(M) and Moster13 stars (ΛCDM context).
- The RN shape is NFW c = 4 (CFG629/CFG432 placeholder, ΛCDM-shaped).
- X-COP hydrostatic masses are a published reconstruction.
- Paraficz+16 masses are recalled (PROVISIONAL).
- The Bullet progenitor M200 values come from a simulation line (CFG629: the sub is input-limited).
- The 8% group hot fraction is the paper's median, not measured per group.
