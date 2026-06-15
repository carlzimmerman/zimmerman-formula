# Front 4 — lensing-RAR + cosmology: interpolation-function (IF) audit, both ways (2026-06-14)

*Does the framework's conceded losses (weak-lensing morphology split, CMB 3rd peak) and its distinctive
prediction (a0(z)) depend on the interpolation function? Recomputed under the framework's OWN dS-Unruh IF
(`g_obs=√(g_N²+g_N·a0)`, `ν(y)=√(1+1/y)`) vs the normal-MOND IFs actually used. Companion to the wide-binary
catch (simple-mu mislabeled "framework" MOVED the EFE cap 1.20-1.32→1.137) and the EFE-clinch check (simple-mu
mislabeled "framework" did NOT move the verdict). Task: FRONT [lensing_cosmology].*

## Headline

**All four Front-4 items are IF-ROBUST. No verdict moves. Two are EXACTLY IF-independent by construction; one is
softened by a known a0-anchor swap (already banked); one is IF-irrelevant linear theory.** The contamination
found elsewhere (door1's simple-mu mislabeled "framework") IS present in the lensing-RAR boost *table*, but that
table is a cosmetic illustration, not the load-bearing pass — and even the corrected boost stays inside Brouwer's
scatter. **No manufactured win** (correcting the boost makes g_obs LOWER, not a better fit) and **no dismissal**
(the simple-mu mislabel is named even though non-load-bearing).

---

## (i) The weak-lensing morphology split (#1 conceded loss, 8.6-9.2σ) — IF-ROBUST (exactly)

**Where:** `real_research/reviews/lensing_rar/lr_battery.py` (baseline 8.8σ, L46/L102),
`agentZ_second_variable.py:55` (9.1σ raw / 6.8σ Hartlap headline), `agentH_perclass_C.py:234` (Sérsic
8.8/5.8 baselines), `agentK_jackknife_stack.py:171` (8.8σ released-profile analog).

**IF used: NONE.** The split is a χ² of the **MEASURED** early-minus-late `g_obs` at matched `g_bar`, where
`g_obs = 4·G·ESD_t` straight from Brouwer+2021's released KiDS ESD profiles (`lr_battery.py:26,42-46`). There
is no `nu()`, no `a0`, no `g_obs=g_bar·ν(...)` anywhere in the computation. The `np.interp` / `sqrt(1-x²)` hits
are log-interpolation along measured curves and NFW projection geometry (`esd_conversion.py`), not the MOND IF;
the `x/(1+x)` is NFW enclosed-mass `ln(1+x)−x/(1+x)`, not simple-mu.

**Why it CANNOT be an IF artifact (verified, not assumed):** a MOND IF would only enter if the split were
`data − MODEL`. Here it is `data_early − data_late` at matched `g_bar`. Any model line `g_bar·ν(g_bar/a0)` is
IDENTICAL for both types at matched `g_bar`, so it cancels exactly in the difference: `resid_E − resid_L =
data_E − data_L` for *every* IF (simple, dS-Unruh, McGaugh — checked). **Verified by re-run:** `lr_battery.py`
reproduces χ²=119.9 → 8.8σ, 15/15 bins early-ABOVE-late, mean +0.261 dex — a fixed-`g_bar` residual offset, IF-
independent by construction.

**Both ways:** if the split had been an IF artifact, correcting it would have HELPED the framework (erased the
#1 loss). It is not — the loss is real and IF-robust. No banked dS-Unruh re-run exists for this front because
none is needed. (The ledger's "false-win #4" for lensing is the door1 boost TABLE cosmetics, not the split; the
split is explicitly flagged "genuinely a0-independent" there too.)

## (ii) The lensing-RAR boost table (door1) — simple-mu MISLABELED "framework"; dS-Unruh SOFTENS but PASSES

**Where:** `real_research/predictions/door1_gravitational_lensing.py`.
**IF used:** `nu_simple(y)=0.5+√(0.25+1/y)` (**simple-mu**, L35-36) — a NORMAL-MOND IF — driving the boost
table L63-66, with the prose labeling it "the framework predicts." **a0 = 1.2e-10 canonical** (L29), NOT the
framework 9.36e-11. So this row is doubly off-footing (normal IF + canonical a0), same contamination family as
the wide-binary cap and the EFE clinch.

**Recompute (framework dS-Unruh ν @ a0=9.36e-11 vs door1's printed simple-mu @ 1.2e-10), Δlog10 g_obs:**

| g_bar [m/s²] | printed (simple,1.2e-10) | dS-Unruh,9.36e-11 | Δ (dex) | regime |
|---|---|---|---|---|
| 1e-9  | 1.11 | 1.05 | −0.025 | Newtonian |
| 1e-10 | 1.70 | 1.39 | −0.088 | transition |
| 1e-11 | 4.00 | 3.22 | −0.094 | deep-MOND |
| 1e-12 | 11.47| 9.73 | −0.071 | deep-MOND |
| 1e-13 | 35.14| 30.61| −0.060 | deepest lensing bin |

**Decomposition (transition bin 1e-10):** IF-only (simple→dS-Unruh, a0 fixed) = **−0.060 dex** (dominant);
a0-only (1.2→9.36, IF fixed) = −0.030 dex. **Deep bin 1e-13:** IF-only = **−0.006 dex** (negligible — both IFs
→ √(g·a0)); a0-only = −0.053 dex = −½·log10(1.282) (dominant). This matches KNOWN PHYSICS: the IF matters in the
transition, vanishes in deep-MOND.

**Verdict movement: NONE.** The worst shift is −0.094 dex (transition); the deep lensing bins (where Brouwer
actually measures, ~1e-13) shift −0.060 dex — all **INSIDE Brouwer's 0.1-0.2 dex RAR scatter**. The KiDS-RAR
pass SURVIVES under the framework's own IF, just softer (the ledger's "cosmetic false-win" reading is correct
and now IF-decomposed). **Both ways:** correcting the IF makes the predicted boost LOWER / g_obs −0.06 dex below
the printed curve — it does NOT improve the fit; it makes the near-circular "reproduces KiDS exactly" wording
softer. Said plainly: the IF correction here makes the number slightly WORSE-looking, not better — reported.

**FIX (cosmetic, non-load-bearing):** relabel `nu_simple` in door1 as "simple-mu (illustration)"; for the
framework prediction use `ν=√(1+1/y)` and a0=9.36e-11. The pass is unchanged.

## (iii) a0(z) distinctive prediction — EXACTLY IF-INDEPENDENT (verified to 6 digits)

**Where:** `door1_gravitational_lensing.py:39-42,88-90`, `predictions/door1_lensing_ultra.py:15,45-47,182,253`,
`reviews/project_a0z_decisive_test.py`, `reviews/project_a0z_MUSE_DARK_III_confrontation.py`,
`a0z_lensing_forecast.py`.

**The observable is a RATIO of acceleration scales:** `a0(z)/a0(0) = √(ρ_DE(z)/ρ_DE0)` (framework declining
branch) — equivalently the RAR-knee ratio, BTFR zero-point ratio, g_dagger ratio. The IF sets how `g_bar→g_obs`
maps at fixed a0; it does NOT touch the a0 *scale ratio*. **Verified numerically:** `a0(z)/a0(0)` is IDENTICAL
to 6 digits whether the absolute anchor is 9.1e-11 (simple-mu), 1.2e-10 (McGaugh-RAR), or 9.36e-11 (framework)
— e.g. z=0.5 → 1.058488 for all three; z=3 → 0.737036 for all three. The α_inf evolution
`α_inf(z)/α_inf(0)=√(a0(z)/a0(0))` is likewise IF-free (deep-MOND √(GMa0), no ν).

`door1_lensing_ultra.py` already encodes this correctly: it labels the IF choice as a **±7% SYSTEMATIC on the
ABSOLUTE a0** (simple-mu 9.1e-11 ↔ McGaugh 1.2e-10, framework 9.35e-11 inside the band) that **"ALL cancel" in
the coefficient-free ratio** (L182). The dominant *absolute* error is the IF systematic (6.9% on α); in the
*ratio* it is exactly zero.

**Both ways:** if a0(z) had secretly depended on the IF, that would HURT the framework (its one distinctive
prediction would be IF-ambiguous, not clean). It does not — the distinctive prediction is IF-robust. (This is
the same cancellation as the a0(z) bridge: ratio/differential quantities kill the IF.) Quarantine note: a0/Z
still not asserted derived; this only concerns IF-independence of the *ratio*.

## (iv) CMB 3rd-peak loss — IF-IRRELEVANT (a0 absent from the linear theory)

**Where:** `real_research/reviews/cmb_third_peak_dm_mimic.py`.
**IF used: NONE. a0: absent from the computation.** This is a real CAMB linear-theory calc: P3/P2 is driven by
`ombh2, omch2, H0, ns, As, tau` and matter-radiation equality z_eq (L26-36). The result — baryon-only
(modified-inertia) universe gives P3/P2 = 0.42-0.54 vs Planck's ~0.92, baryon-only "CANNOT reach Planck by any
reasonable tuning" (L82) — is a statement about whether modified inertia supplies CDM-like clustering at
recombination. That is orthogonal to the IF, which only lives in the low-acceleration quasi-static regime. `a0`
appears ONLY in the prose verdict (L89-94) noting the result is "branch-INDEPENDENT" and a0-moot. **IF choice
does not touch the 3rd-peak loss — confirmed, no recompute needed beyond verifying a0/ν are absent.**

---

## Net (both ways)

| Item | IF actually used | dS-Unruh recompute | Verdict moves? |
|---|---|---|---|
| (i) morphology split 8.6-9.2σ | **NONE** (measured g_obs contrast) | exactly invariant — model line cancels in E−L | **NO** (loss real, IF-robust) |
| (ii) door1 lensing-RAR boost table | **simple-mu @ 1.2e-10**, mislabeled "framework" | g_obs −0.06 to −0.09 dex, INSIDE Brouwer 0.1-0.2 dex | **NO** (pass survives, softer; correction makes it WORSE-looking) |
| (iii) a0(z) ratio / α_inf evolution | ratio → **IF cancels exactly** | identical to 6 digits across all anchors | **NO** (distinctive prediction IF-robust) |
| (iv) CMB 3rd peak | **NONE** (a0 absent, linear theory) | n/a — IF-irrelevant | **NO** (loss real, IF-irrelevant) |

**The framework's two conceded losses on Front 4 (lensing morphology split, CMB 3rd peak) are IF-ROBUST — they
are NOT IF artifacts, so correcting the IF does not erase them (does not help the framework).** Its distinctive
prediction (a0(z) declining, α_inf evolution) is EXACTLY IF-independent — it does NOT secretly depend on the IF
(does not hurt the framework). The only genuine IF contamination is the door1 boost-table cosmetic (simple-mu +
canonical a0 mislabeled "framework"); correcting it to the framework's dS-Unruh ν makes the boost SMALLER (a
worse-looking, more honest fit) but keeps the KiDS-RAR pass inside Brouwer's scatter — **no verdict moves, no
manufactured win, no dismissal.** Quarantine held.

*Verified, not assumed, in both directions: the IF-cancellation claims (i,iii,iv) and the IF-moves-the-number
claim (ii) each carry the explicit recompute. The door1 boost correction is reported even though it makes the
number worse-looking, per the #1 rule.*
