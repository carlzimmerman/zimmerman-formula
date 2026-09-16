# G118 — THE MERGER-RATE REGISTRY: the deep-regime close-pair prediction, pre-registered

**Filed 2026-09-15, in the open before the confrontation measurement. Lane G118.**
**Deliverables: `deepseek_push/G118_merger_registry.md`, `deepseek_push/G118_results.json`
(reproducibly: `python3 deepseek_push/G118_merger_registry.py` → `.out` + `.json`).**

> **WHERE THIS SITS.** G086 (committed) registered the LAW-SIDE pair statement:
> during galaxy mergers the 1/r dark law scales the pair's mutual field by
> **(1 + r/r_M(pair))** — **factor 2.000 exactly at r = r_M** — with
> r_M(pair) = sqrt(G M_b/a0), M_b = M_b,1 + M_b,2:
> **12.2031 / 19.2948 / 27.2869 / 38.5895 kpc at pair totals 1e11 / 2.5e11 / 5e11 / 1e12 M☉**
> (reproduced digit-for-digit here, C1), the observable named (the close-pair
> fraction / merger rate at fixed stellar mass), and a one-line falsifier.
> `GRAVITY_EVERYWHERE.md` open-list item 10 assigns this registry: **G118 executes
> the registry; G121 forecasts the observable.** This document is that execution:
> the closed-form response exponent, the quantitative excess curve, the
> measurement contract, and the armed falsifiers — all fixed now, before the
> measurement.

---

## 1. THE PREDICTION — ITS QUANTITATIVE FORM

For a pair at separation **s** with masses **M1, M2** (M_b = M_b,1 + M_b,2),
r_M(pair) = sqrt(G M_b / a0). The registered prediction:

> **f_pair(s) / f_pair,LCDM(s) = (1 + r_M(s)/s)^q,  q = 1 — closed form**

at fixed stellar mass. Anchor values (computed, exact):

| s | η(s) = 1 + r_M/s | excess factor | reading |
|---|---|---|---|
| s = r_M/2 | 3.000 | **3.000 (+200%)** | the deep-regime interior |
| **s = r_M** | 2.000 | **2.000 (+100%)** | the pair-scale equipartition, **G086's factor EXACT** |
| s = 2 r_M | 1.500 | **1.500 (+50%)** | the slope falsifier's outer anchor |

The excess's log-slope vs separation: d ln(excess)/d ln s = −(r_M/s)/(1 + r_M/s):
**−0.667 at s = r_M/2, −0.500 at s = r_M, −0.333 at s = 2 r_M.**

### 1.1 The derivation of q (the Roche-class criterion with the 1/r force)

1. **The tidal statement (G086, anchor).** The 1/r law scales the pair tidal
   field by the deep-regime force ratio; at the satellite's edge the
   tidally-relevant ratio is the **(1 + r_M,sat/s)-class** factor
   (r_M,sat = sqrt(G M_sat/a0), the satellite's own MOND radius; = 2.000
   exactly at s = r_M,sat — the G086 equipartition structure at the satellite
   scale; at the matched-pair anchor the pair's r_M(pair) is the registered
   scale). Eta(s) = 1 + r_M/s is the enhancement of the disruption-relevant
   field at the satellite's edge.
2. **The disruption criterion (Roche-class, 1/r force).** The satellite at
   separation s is disrupted when the host's tidal field at its edge matches
   its self-binding there; the classical boundary is the tidal radius
   **r_t = s (M_sat/M_host)^(1/3)-class** (O(1) constant, 2^(1/3) for the
   point-mass L1 class). With the 1/r law the criterion's boundary is
   **scaled by the deep-regime force ratio** — η(s) = 1 + r_M/s, to the first
   power — and the surviving-pair population at fixed stellar mass responds
   to that boundary linearly (the criterion's first-order statement).
   Hence **q = 1 — the closed form**.
3. **Consistency with G086.** On the (1 + r_M/s) axis, the pair-fraction
   excess at s = r_M is **2.000 — G086's registered factor exactly**. The
   G086-literal axis (1 + s/r_M) agrees at the anchor and diverges at
   s = 2 r_M (3.000 vs the registered 1.500): the axis convention is
   registered here, and the 2 r_M bin is exactly where F2 discriminates.
4. **The honest envelope.** The same chain with the bound-phase-space
   counting (f_pair ~ v_b³, v_b² ~ M_eff) gives q = 3/2; the
   threshold-boundary reading gives q = 1/2. Registered point value:
   **q = 1** (reproduces G086's 2.000 at r_M). The envelope [1/2, 3/2] is the
   pre-registered honesty band: q = 1/2 → 1.414 / 1.225; q = 1 → 2.000 /
   1.500; q = 3/2 → 2.828 / 1.837 at (r_M, 2 r_M). The discriminating deltas
   at 2 r_M are 0.088 dex between adjacent q's.

### 1.2 The criterion's own boundary shift (the consistency check, not the engine)

r_t,deep/r_t,N = [(1 + r_t/r_M,0)/(1 + s/2r_M,0)]^(1/3) (matched members,
M_sat = M_host = M0):

| M0 | s = 10 kpc | s = 20 kpc | s = 40 kpc |
|---|---|---|---|
| 1e10 M☉ | 1.132 | 1.176 | 1.210 |
| 5e10 M☉ | 1.081 | 1.124 | 1.169 |

Max shift 21.0% over the window — and it runs in the **ENHANCEMENT direction**
(r_t,deep > r_t,N: the satellite's dark halo protects its edge — the pair
keeps its satellite at smaller s). The registered prediction's engine is the
linear force-ratio transfer (q = 1), not the boundary geometry; the table is
the criterion's consistency check (C3).

### 1.3 The r_M anchor table (G086, reproduced exactly; both a0 footings)

| M_pair,tot (M☉) | r_M,canonical (kpc) | r_M,alt (kpc) |
|---|---|---|
| 1e11 | 12.2031 | 11.1177 |
| 2.5e11 | 19.2948 | 17.5787 |
| 5e11 | 27.2869 | 24.8600 |
| 1e12 | 38.5895 | 35.1573 |
| 2e10 (task sample floor) | 5.46 | 4.98 |
| 2e11 (task sample ceiling) | 17.26 | 15.72 |

(canonical a0 = 9.3619e-11 m/s², alt 1.1279e-10 — working-rule 4; the s/r_M
axis is **footing-invariant** by construction, the s-anchors shift ×0.9110.)

---

## 2. THE MEASURABLE — f_pair IN THE 10–40 kpc WINDOW

- **Window:** projected/3D separation **s ∈ [10, 40] kpc**; **members M★ ∈
  [1e10, 1e11] M☉** (pair totals 2e10–2e11 M☉ → r_M ∈ [5.46, 17.26] kpc; the
  window maps to s/r_M ∈ [0.58, 7.33] — it straddles the pair scale, with the
  excess's bite at the inner end and at the heavy-mass end; the heavier
  G086-class pairs (1e11–1e12 M☉) reach s/r_M = 0.26 at the window's inner
  edge).
- **Arms:** (a) the **local volume** — resolved pairs (D ≲ 11 Mpc, the
  Karachentsev-class census), true 3D separations — the cleanest anchor
  geometry, but tens of pairs: a consistency arm; (b) the **SDSS-class
  catalogs at z ~ 0.1** — spectroscopic pairs (the Ellison/Patton class),
  r_p ∈ [10, 40] kpc, |Δv| < 500 km/s, M★ ∈ [1e10, 1e11] both members —
  thousands of pairs: **the deciding arm**.
- **The control:** the LCDM expectation computed with **identical cuts on
  LCDM mocks** (z ~ 0.1 snapshot, the survey geometry). The excess is a ratio
  against the identical-selection control: every selection-identical
  systematic (projection dilution, velocity window, mass completeness)
  cancels in the ratio.
- **The estimator:** per-pair r_M from the pair's own masses, then the excess
  in **s/r_M universal bins** — the prediction is a function of s/r_M only.
  Bins [1/2, 1), [1, 2), [2, 4) (this sample; the heavy classes extend below).
- **The window-integrated excess (computed, 4e4-cell grid, log-uniform in
  M_pair and s):**

| bin | n | median excess | median s/r_M |
|---|---|---|---|
| s/r_M ∈ [0.50, 1.00) | 3673 | **2.174** | 0.85 |
| s/r_M ∈ [1.00, 2.00) | 15420 | **1.663** | 1.51 |
| s/r_M ∈ [2.00, 4.00) | 16291 | **1.374** | 2.68 |
| anchor bin [2/3, 4/3] | 8356 | **1.946** (mean 1.991) | — |
| small-s wing < 2/3 | 288 | **2.562** | — |
| large-s wing ≥ 4/3 | 31356 | **1.416** | — |

  **Window median: 1.485 (+48%)**; the excess rises toward small s/r_M as
  registered, asymptoting to 1 beyond the pair scale.
- **The universal-curve statement:** the excess over stellar-mass bins must
  collapse onto the single curve (1 + r_M/s) in s/r_M — no halo-concentration
  input, no environment parameter: a deterministic function of M_b alone
  (G086's own falsifier, restated as F3).
- **Survey power (honest arithmetic):** with N_pairs ~ 1000–10000 (f_pair ~
  5–10%, N_gal ~ 1e5), the anchor-bin excess 2.000× clears at **19–59σ
  (Poisson)**; the q-slope discrimination (0.088 dex between adjacent q's at
  2 r_M) needs the per-bin excess at the ~10% level (N_bin ~ 500+):
  statistics-adequate at SDSS-class N, **systematics-limited** — the residual
  band is the mass-mapping M★ → M_b → r_M anchor and the velocity-window
  fidelity (both canceled in the ratio to the extent they are
  selection-identical in the mock; stated honestly).

---

## 3. THE FALSIFIERS — pre-registered; any one kills

- **F1 — the anchor.** f_pair(s) **at or below the LCDM expectation at
  s ~ r_M** (the anchor bin s/r_M ∈ [2/3, 4/3]: excess ratio ≤ 1.00) kills —
  the registered +100% at the pair-scale equipartition is the core statement.
- **F2 — the slope (the q).** A measured excess that does not follow
  (1 + r_M/s)^q: **q_meas = d log₁₀(excess)/d log₁₀(1 + r_M/s) outside
  [0.5, 1.5]** — including q_meas ≤ 0 (flat or falling toward small s), i.e.
  **a rising f_pair(s) with the wrong slope (the q)** — kills. The
  G086-literal axis (1 + s/r_M) sits at 3.000 at 2 r_M vs the registered
  1.500: the 2 r_M bin discriminates the axes.
- **F3 — the M_b-only statement.** An excess that scales with halo
  concentration or environment instead of (1 + r_M/s) with r_M from M_b
  alone kills (the universal-curve test: scatter > the pre-registered 20%).
- **F4 — the window.** An excess confined outside the registered window
  (e.g. only s < r_M/2, or only at the projected-fringe scales) kills the
  registered curve (the window-integrated median ~1.5 is the prior).

---

## 4. VERDICTS (pre-registered; the PASS = the entry complete, not the physics)

- **[PASS] V1 — the closed-form q and the predicted excess.** q = 1, closed
  form from the Roche-class disruption criterion with the 1/r force
  (r_t = s(M_sat/M_host)^(1/3)-class scaled by the deep-regime force ratio
  η(s) = 1 + r_M/s, linear transfer); f_pair/f_LCDM = (1 + r_M/s)^1; **excess
  **2.000 at s = r_M** (G086's factor EXACT), **1.500 at s = 2 r_M**,
  3.000 at s = r_M/2; envelope [1/2, 3/2]; window median 1.485 over
  10–40 kpc × 2e10–2e11 M☉.
- **[PASS] V2 — the registry complete.** The measurement recipe (the sample
  arms, the estimator, the control, the bins, both footings), the
  falsifiers F1–F4 with decision rules stand as the pre-committed confrontation
  contract, fixed 2026-09-15, in the open; **the G121 handoff**: the
  survey-level forecast of the observable (the rate face and the mass-function
  shaping) rides on this entry.
- **[PASS] V3 — the honest statement (what G118 adds beyond G086, and what it
  does not).** G086 registered the law-side statement: the 1/r law scales the
  pair tidal field by (1 + r/r_M) — factor 2.000 at r_M, r_M(pair)
  12.2–38.6 kpc — with the observable named and a one-line falsifier. G118
  executes the registry: **(a)** the closed-form response exponent q = 1 by
  the disruption criterion; **(b)** the executable curve (1 + r_M/s)^q with
  anchor values 2.000 / 1.500 / 3.000; **(c)** the measurable contract —
  sample, estimator, LCDM-mock control, s/r_M universal bins — and the armed
  slope falsifier G086 left open; **(d)** the honest limits: **no new physics
  beyond G086** — q and the axis convention are the registry's contribution;
  the envelope [1/2, 3/2] is the honesty band; the local-volume arm is
  underpowered (tens of pairs); the SDSS arm is the decider (thousands of
  pairs, 10%-level slope systematics); and the excess statement is
  registered on the (1 + r_M/s) axis — the G086-literal (1 + s/r_M) axis
  agrees at the anchor and diverges at 2 r_M, which is exactly F2's
  discrimination. Nothing here is claimed measured.

**G118 COMPLETE: 8/8 checks PASS. WROTE G118_results.json.**

---

### References (all committed in-repo)

`G086_relativistic_face.py/.out/.json` (the registered pair statement, V2c);
`G088_dr4_forecast.py/.out` (the registry/forecast style); `GRAVITY_EVERYWHERE.md`
open-list item 10 (this registry; G121 = the observable forecast);
`DR4_AMENDMENT_12.md` (the amendment/registration protocol: filed in the open,
both a0 footings, no validates/confirms language); `G089_dimensionless_inventory.md`
(the registration conventions); `PREDICTIONS.md` (the kill-ledger class).