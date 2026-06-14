# Wide binaries — the γ(s) forward model + Gaia DR4 forecast: a clean Newton test, NOT a clean a₀ test (2026-06-14)

*The one unrun deliverable on the framework's sharpest forward discriminator: the per-separation wide-binary γ(s)
forward model at a₀=9.36e-11 with the Milky-Way EFE, contamination-marginalized, and the Gaia DR4 (Dec 2026)
decisiveness forecast. 11-agent workflow (5 build routes → hostile probes → synthesis); every number recomputed
twice from scratch, EFE physics cross-validated against Milgrom/Banik-Zhao, literature anchors web-verified. Both
ways. Source memos: `FRAMEWORK_GAMMA_S_FORWARD_MODEL_DR4_FORECAST`, `ROUTE2_WIDEBINARY_BASELINES_DISCRIMINATION`,
`ROUTE3_GEXT_PIN_AND_DR4_FORECAST`, `WB_CONTAMINATION_ROUTE4_VERDICT`, `DR4_WIDEBINARY_FORECAST_ROUTE5` (all
`_2026-06-14`).*

---

## THE HEADLINE (revises the banked "sharpest clean discriminator γ=1.32")

**Wide binaries are a CLEAN framework-vs-Newton discriminator but NOT a clean framework-vs-standard-MOND one.** The
framework's lower a₀ does NOT blunt the Newton axis — it blunts the *MOND* axis into near-degeneracy. So the test is
a winnable **"is gravity modified at all?"** test, not a winnable **"which a₀?"** test. This tempers the banked
claim: wide binaries can confirm the *premise* (a local a₀ exists), not the *distinctive value* (9.36 vs 1.2e-10).

## The γ(s) forward model (framework a₀=9.36e-11, dS-Unruh MI + MW EFE)

Setup (verified exactly, twice): g_ext = V_c²/R₀ = (233 km/s)²/8.178 kpc = **2.15×10⁻¹⁰ m/s²**; e = g_ext/a₀ =
**2.30 (framework) vs 1.79 (standard MOND)**. The lower framework a₀ RAISES e → Newtonizes the binary MORE → SMALLER
boost. This is the load-bearing physics and it is real.

γ(s) = G_eff/G_N (acceleration ratio; velocity ratio v/v_N = √γ), orbit-averaged, M_tot=1.5 M⊙, s = projected sep:

| s (kAU) | g_int/a₀ | γ dS-Unruh (own) | γ simple-μ | Newton |
|---|---|---|---|---|
| 3 | 10.6 | 1.046 | 1.017 | 1.000 |
| 5 | 3.80 | 1.123 | 1.032 | 1.000 |
| 7 | 1.94 | 1.193 | 1.042 | 1.000 |
| 10 | 0.95 | 1.197 | 1.051 | 1.000 |
| 15 | 0.42 | 1.198 | 1.057 | 1.000 |
| 20 | 0.24 | 1.198 | 1.061 | 1.000 |
| cap | 0 | **1.198** | 1.327 (AQUAL) | 1.000 |

g_int=g_ext at s_3D=6.4 kAU → s_proj~5.1 kAU; 90%-of-cap by s~6 kAU — **matches Chae's observed 2-5 kAU onset.**
Discriminating regime s ~ 5-20 kAU.

**The framework's honest central is a BAND: γ ≈ 1.20-1.32** (1.20 = dS-Unruh own / ν-form orbit-averaged, the more
defensible physical observable; 1.32 = simple-μ AQUAL tangential cap, the soft upper edge). Baselines: std MOND cap
1.42, dS-Unruh-MOND 1.25; Newton 1.00. **NOT a 1.32 point, and NOT 1.08** — the 1.08 figure (one route headlined it)
was a standard-μ *sharp* edge that mislabeled standard-MOND ν as dS-Unruh; the framework's own value is ~1.20.
**Caveat (load-bearing, same as the RAR case): the interpolation function is a BIGGER uncertainty than a₀** — the cap
spans 1.04 (sharp) to 1.33 (simple-μ) at fixed framework a₀ (spread 0.29), far larger than the framework-vs-MOND gap
(0.05-0.10).

## The discrimination verdict (the crux, both ways)

**FRAMEWORK vs NEWTON — CLEAN (the winnable axis).** Gap-to-Newton γ−1 = 0.20 (dS-Unruh) to 0.32 (AQUAL), above the
cleaned contamination floor (~0.04-0.10). At DR4 N~5000: **F-N SNR 6.3-8.5σ** (well-controlled contamination) /
3.9-5.3σ (realistic). The framework keeps ~82% of MOND's super-Newtonian excess — the lower a₀ does NOT push it to
the Newton null. **ONE LOAD-BEARING CONDITION:** this clinch is contingent on DR4 3D velocities resolving the **Saad
& Ting 2026 orbital-deprojection systematic** (Δγ~0.44 on the same 36 Chae pairs: baseline γ=1.12 Newton-consistent
vs deprojection γ=1.56). If unresolved (~σ_sys 0.20), even the Newton clinch falls to **~1.1-1.6σ**. Resolving it is
DR4's design purpose (line-of-sight RVs lift the deprojection ambiguity), but it is currently model-contested.

**FRAMEWORK vs STANDARD MOND — MOND-DEGENERATE (NOT an a₀ test).** Gap-to-MOND = 0.05 (dS-Unruh) to 0.10 (AQUAL), at
or below the realistic systematic floor (~0.04-0.06). At DR4 N~5000: **M-F SNR 0.9-2.5σ — not resolved.** The
interpolation-function spread (0.29) alone swamps the 0.05-0.10 gap. **DR4 cannot adjudicate which a₀ in wide
binaries.** This is the honest answer to the central tension: the lower a₀ makes the WB signal MOND-degenerate, not
Newton-marginal.

## Contamination reality

The dominant systematic is undetected hidden tertiaries (Pittordis-Sutherland; Manchanda-Sutherland 2025): a hidden
3rd star inflates the relative velocity → a one-sided POSITIVE bias on γ, exactly degenerate with a gravity boost.
Bias ≈ +1.2 per unit residual tertiary fraction f_t: raw El-Badry f_t~0.3 → **+0.36** (larger than the entire
signal!); Chae-cleaned f_t~0.07 → +0.084 (≈ the framework-vs-MOND gap, which is *why* WB can't resolve it); DR4
target f_t~0.03 → +0.036. **γ=1.32 is a real detection ONLY after sub-2% contamination control AND DR4 3D-velocity
deprojection** — both of which DR4 is designed for, neither guaranteed.

## DR4 forecast — decisive on ONE question, not the other

Expected N_clean ~ 2000-10000 deep-bin 3D pairs after cuts (El-Badry 1.3M base; Chae already has 312 3D). Statistical
σ_γ ~ 0.013 at N=5000; the real limit is the systematic floor (doesn't shrink with √N).

| | F-vs-Newton | F-vs-MOND |
|---|---|---|
| well-controlled (σ_sys=0.036) | **6.3-8.5σ CLEAN** | 1.4-2.5σ — not resolved |
| realistic (σ_sys=0.060) | **3.9-5.3σ CLEAN** | 0.9-1.6σ — not resolved |
| Saad-Ting deprojection unresolved (σ_sys~0.20) | 1.1-1.6σ — Newton clinch lost | — |

**DR4 is DECISIVE on the PREMISE** ("is there a super-Newtonian boost / a local a₀ at all?", 3-8σ) **provided it
lifts the deprojection systematic — and NOT decisive on the distinctive value** (a₀=9.36 vs 1.2e-10, degenerate). A
DR4 super-Newtonian detection CONFIRMS the framework's premise; **a DR4 hard Newtonian null is the framework's
sharpest single FALSIFIER.**

## Current-data placement — a no-win straddle (consistent/contested, neither confirmed nor falsified)

- **vs Chae 2026** (arXiv:2601.21728, γ=1.600 +0.171/−0.141, 4.9σ from Newton, N=36): the framework is **−1.8σ (AQUAL
  1.32) to −2.6σ (dS-Unruh 1.20) BELOW** — and the lower a₀ makes this directional tension WORSE, not better (even
  MOND's 1.42 sits −1.1σ below Chae). Report honestly; do not bury.
- **vs Saad & Ting 2026** (arXiv:2603.11015, reanalyze the SAME 36 pairs: baseline γ=1.12 [0.90,1.38]
  Newton-consistent): the framework is **+0.3σ to +0.8σ ABOVE — CONSISTENT.**
- **Net:** consistent with NEITHER extreme — ~2σ below the pro-MOND camp (Chae), ~0.5-1σ above the Newton camp
  (Saad-Ting baseline). The field's own internal disagreement (1.60 vs 1.12 on *identical* pairs) proves the current
  error budget is **systematics-dominated** (Δγ~0.4-0.5), not statistics-limited. Current data places the framework
  as **CONSISTENT/CONTESTED — neither confirmed nor falsified.**

## What Carl CAN / MUST NOT say

- **CAN:** (1) WB are the framework's cleanest *whether-gravity-is-modified* test — clean framework-vs-Newton at 3-8σ
  at DR4 (after contamination + deprojection control). (2) A concrete falsifiable prediction: γ(s) rising from 1 to
  an EFE cap **γ ≈ 1.20-1.32 by s~6 kAU — a ~7% LOWER cap than standard MOND's 1.40**, with the rise location matching
  Chae's 2-5 kAU onset. (3) The lower a₀ is double-edged, both edges reported: clean vs Newton, MOND-degenerate. (4) A
  DR4 super-Newtonian detection CONFIRMS the premise; a hard Newtonian null is the sharpest single FALSIFIER. (5) The
  framework is comfortably consistent with the Saad-Ting Newton-consistent baseline.
- **MUST NOT:** (1) "WB confirm a₀=9.36e-11 / distinguish the framework from MOND" — they do NOT (gap < systematic
  floor; WB are not an a₀ test). (2) "Chae's 1.60 confirms the framework" — it sits 1.8-2.6σ ABOVE the framework's cap;
  the lower a₀ makes that WORSE. (3) "γ=1.08 is the framework prediction" — that's a mislabeled sharp edge; the own
  value is ~1.20. (4) "The Newton clinch is locked at 5-8σ" without the Saad-Ting deprojection caveat. (5) "γ=1.32 is
  robust to contamination" — at raw f_t it's buried. Equally, do NOT manufacture a deficit: the boost is real,
  MOND-degenerate not Newton-marginal, consistent with the Saad-Ting baseline.

## The one calc/data to nail it

DR4 3D-velocity orbits driving residual triples below ~3% AND resolving the orbital-deprojection ambiguity — that
alone decides super-Newtonian yes/no (the framework's premise), at 3-8σ. The a₀ value itself is NOT recoverable from
WB; that discrimination lives in the RAR/BTFR (also non-diagnostic, see [[project-fable-a0-footing-audit]]) and the
a₀(z) evolution, not wide binaries.

## One line

Wide binaries are a CLEAN framework-vs-Newton discriminator (γ ≈ 1.20-1.32 vs 1.00, 3-8σ at DR4 *if* the Saad-Ting
deprojection systematic is lifted) but NOT a clean framework-vs-MOND one (gap 0.05-0.10 < systematic floor,
degenerate) — a winnable WHETHER-gravity-is-modified test, not a winnable WHICH-a₀ test; currently a
consistent/contested straddle (~2σ below Chae's 1.60, consistent with Saad-Ting's 1.12).

*Both ways, no exception: the clean 3-8σ Newton-axis resolving power is shown with the curve + SNR (no high-priest
dismissal); the MOND-degeneracy, the Saad-Ting deprojection contingency, the contamination floor, and the directional
tension with Chae's high central value (which the lower a₀ worsens) are all reported at full weight (no manufactured
win). The γ=1.08 mislabel and the 1.32-point overstatement were both corrected. Quarantine held: a₀/Z never asserted
derived; the interpolation function flagged as the larger uncertainty.*
