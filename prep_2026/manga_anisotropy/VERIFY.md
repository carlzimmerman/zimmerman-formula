# VERIFY — adversarial verification of the Stage-1 MaNGA anisotropy firing

**Date:** 2026-07-17 (UTC). **Verifier:** independent re-run + independent code
(`verify_independent.py` → `verify_independent.out`, exit 0; own sklearn-Huber, own
bootstrap seed 424242, scipy ranks, own δ recomputation straight from the FITS —
none of the lane's regression code reused).

**VERDICT: UPHELD** — the honest state "UNINFORMATIVE on MI-vs-MG; baseline created;
the discriminator's natural home is low-y dispersion systems" is correct and, if
anything, understated: my checks push the fixed-IMF "MI-signed" cell even further
toward pure systematics. Every load-bearing number reproduces. Two sharpenings and
one thin-margin integrity note below.

---

## 1. Re-run (exit-0, drift, determinism)

- `stage1_catalog.py`, `extract_resolved_proxies.py`, `fire_anisotropy.py` all re-ran
  **exit 0**; `resolved_proxies.csv` and `maps_subsample.csv` **bit-identical** to the
  staged files; `stage_catalog.csv` deterministic across runs; `fire_anisotropy.out`
  regenerated **bit-identical** (fixed seed) — every number in FIRING.md matches the log.
- **No hard-coded checks found**: the verdict block, zero-inside flags, decomposition
  read-offs and power table are all computed from `results`/data at runtime; the only
  literals are the frozen constants. (Cosmetic dead line `fire_anisotropy.py:151`.)
- **Freeze-vs-code drift: none material.** All frozen constants/cuts/definitions
  (a₀ both footings, K_v=5.0, H0/Ωm/h, SNR_MED g-band ≥10, σ floor 70, (V/σ)_glob
  definition, dedupe rule, IMF A ×1.55 / B 0.30@130, g_bar=G(M/2)/R_e², P1 wedges
  0.87/0.5 + ≥8 spaxels, P2 window 0.5–1.5 Re + ≥20 spaxels unweighted log-log OLS,
  sigmacorr quadrature, tercile-top-16 subsample rule, Huber+partial-Spearman+10k
  bootstrap, C3 controls + logσ in bracket B) match the code exactly. Two trivia:
  extract adds a σ_c>1 km/s positivity guard (not frozen, harmless); FROZEN.md §2 has
  an ambiguous sentence ("the primary regression controls on log σ_e / log M*") that
  conflicts with the operative §4 spec (logσ_e only in bracket B) — the firing followed
  §4; had §2's reading been used, every cell would have been null by the §5 identity
  below, so the ambiguity was resolved in the only direction that lets the fixed-IMF
  cell exist at all. Flagged; immaterial because that cell was reported as uninformative.
- **Freeze-before-data (mtime check):** FROZEN.md last write 00:23:05Z; dapall download
  completed 00:23:22Z; drpall 00:23:29Z; MAPS 00:26Z. Consistent with freeze-first, but
  the margin is **17 s** — a 146 MB download completing at 00:23:22 plausibly *began*
  before FROZEN.md's final save, and the claimed stamp (00:21:52Z) precedes the file's
  own mtime by 73 s (edited after stamping). "Before the first byte" is therefore
  **not strictly verifiable**; there is no evidence of post-data spec change (the firing
  matches the frozen spec verbatim), but future freezes should be hash-stamped the way
  the Gaia DR4 prereg was.

## 2. Independent recomputation (own code)

- **δ from raw FITS**: max |δ_mine − δ_catalog| over the 48 = **2.4e-6 dex**; cut
  cascade independently reproduced **exactly** (10782/10735/9027/8771/8766/3159/2442;
  382 primary / 671 variant / 2407 parent).
- **Frozen cells** (sklearn Huber, different bootstrap seed):
  P2|canon|fixedIMF **−0.632 [−1.164, −0.261], p=0.015** (lane −0.6355 [−1.141, −0.200],
  p=0.019) ✓; alt −0.632 ✓ footing-inert; bracket-B **+0.0021 zero-inside** ✓; P1
  −1.065 zero-inside ✓; OLS estimator swap −0.688, p=0.039 (sign stable) ✓.
- **Cross-checks**: resolved-vs-DAPall σ_e corr 0.9999 / ratio 0.9993 ✓; all 15 P1
  dropouts are 19- or 37-fibre bundles ✓; all 48 have (V/σ)_glob<0.4 ✓; power table
  reproduced within rounding (b=0.05 → N≈5,133/6,039/12,405 vs lane 5,154/6,064/12,457) ✓;
  y-budget: y median 7.9, log ν median 0.026 dex, trend amplitude 0.172 dex = **11×**
  the 16–84% log ν spread and **6.7×** the median boost ✓ (and this compares against the
  *entire* ν boost, of which any anisotropy modulation is only a fraction — the
  over-budget claim is conservative).

## 3. Rotation/inclination contamination — the strictest slow-rotator subsets

The audit's key question: does the fixed-IMF slope survive the most pressure-supported
subset? **No, as a detection:**

| subset | N | slope | 95% CI | partial ρ |
|---|---|---|---|---|
| (V/σ)_glob < 0.30 | 30 | −0.45 | [−0.79, **+0.97**] zero-IN | **+0.02** |
| (V/σ)_glob < 0.25 | 21 | −0.50 | [−0.93, **+1.19**] zero-IN | −0.22 |
| (V/σ)_glob < 0.20 | 14 | −0.49 | zero-IN | −0.29 |
| resolved V/σ < 0.10 | 23 | **+0.16** | zero-IN | +0.10 |

Point estimates keep the sign in 3/4 cells, but every strict cell is zero-inside and
the rank statistic collapses (even flips). Moreover **corr(P2, resolved V/σ) = −0.77**:
in this sample the "anisotropy" proxy is to first order a *residual-rotation* proxy.
Adding b/a as an inclination control leaves the full-48 slope intact (−0.68, zero-out),
so it is rotation/structure, not inclination per se. This *strengthens* the lane's own
hotter-half flag: the fixed-IMF signal is carried by the more-rotating members.

## 4. The IMF trap, run the other way (how much slope can an IMF gradient FAKE?)

Imposing dlog(M*/L)/dlogσ = γ (literature: Treu+2010 ApJ 709,1195 ≈0.31; Cappellari+
2012 Nature 484,485 / Cappellari+2013 MNRAS 432,1862 ≈0.3–0.4; Li+2017 ApJ 838,77
(MaNGA) ≈0.3; La Barbera+2013 MNRAS 433,3017 up to ≈0.5–0.6) and re-fitting with the
frozen C3 controls:

| γ [dex/dex] | faked slope | % of observed −0.632 |
|---|---|---|
| 0.20 | −0.061 | 10% |
| 0.30 | −0.091 | 14% |
| 0.40 | −0.122 | 19% |
| 0.60 | −0.183 | 29% |

The observed slope **exceeds the literature-amplitude IMF fake by 3.5–7×**; cancelling
it via the mass term alone needs γ ≈ **2.08 dex/dex** (≈7× literature) — the lane's
14%-at-0.30 and "~2.0 dex/dex" claims verified independently. So the IMF gradient
*by itself* neither creates nor kills this slope; what kills it is the σ_e control,
which is §5.

## 5. Manufactured-positive AND manufactured-null hunt (both, equally)

- **Manufactured positive (the MI-signed cell):** (a) the Huber slope of **2·logσ_e**
  on P2|C3 is **−0.6322** vs the δ slope **−0.6317** — the entire fixed-IMF "signal"
  *is* the σ_e–P2 structural relation; ν contributes ~nothing (as the y-budget demands).
  (b) **Placebo test:** 400 synthetic proxies = pure noise correlated with logσ_e at the
  observed r=−0.62 (zero anisotropy content by construction) yield median slope −0.43
  and **fire "MI-like, zero-outside" 78% of the time**. A ~2.3σ MI-signed slope was
  therefore close to guaranteed for *any* σ-correlated proxy; the P2 cell demonstrates
  no anisotropy-specific information. The lane's own over-budget check + UNINFORMATIVE
  verdict already blocked the MI reading — correctly; this quantifies *how* blocked.
- **Manufactured null (the bracket-B cell):** δ is an exact function
  2logσ_e + logR_e − logM* − logν(M*,R_e) + const, so with (logM*, logR_e, z, logσ_e)
  all controlled its free variation collapses from 0.181 dex to **0.014–0.017 dex rms**
  (91% gone by algebra; the Huber core scale 0.001). The bracket-B "zero" and hence the
  frozen **NOT-ROBUST verdict were design-guaranteed before any data existed** — a
  structural null, not an empirical finding. The lane *disclosed* this ("over-conservative
  by construction", "structural degeneracy") and did not let MG claim it; verified and
  endorsed, with the sharper statement: at Stage 1, with δ built solely from
  (σ_e, R_e, M*), the frozen design could never have produced a robust MI result NOR a
  meaningful MG result. UNINFORMATIVE was the only reachable honest endpoint —
  the run's real products are the baseline scatter (0.18 dex), the y-regime statement,
  and the Stage-2 power table, all verified.
- **Selection tuning:** cuts frozen pre-data and the cascade landed inside the
  pre-stated expectation; within the 48, scanning the σ floor (80/90/100/120), z
  (<0.06/<0.04), dropping the top-σ quartile, and jackknife (all 48 leave-one-out
  slopes negative, −0.98..−0.58) keep the sign with graceful significance loss —
  no single-point or cut-edge artifact. P2 window re-extractions from the MAPS
  (0.5–1.0 / 0.75–1.5 / 0.3–1.2 Re) keep the sign (−0.43..−1.35); magnitude is
  window-dependent (a proxy, not a physical slope — consistent with its stated status).
  No sign of tuning; also no incentive, since the fired conclusion is a non-claim.

## 6. Firewall + rails audit

- Firewall/"proxy is NOT β" language present in **all seven** artifacts (FROZEN.md,
  STAGE.md, FIRING.md, all three drivers' docstrings, fire_anisotropy.out) and on both
  figures; the FIRING verdict block restricts its language to "THIS PROXY only". ✓
- Both footings in every cell (canon/alt identical to 3 decimals — verified, and
  expected since footings enter only through log ν ≈ 0.026/0.031 dex at y≈5–11). ✓
- Nulls and MI-signed cells reported at equal prominence; MG explicitly NOT credited
  with the bracket-B zero. ✓
- Stated-empty cells (0.6-variant identity, no catalog-level proxy) are genuinely
  empty-by-freeze, verified against FROZEN.md §3. Environment control omitted AND
  stated, as §4 permits. ✓
- Frozen zimmerman-formula repo untouched; `~/new_physics` (and prep_2026) confirmed
  outside any git repo — big FITS carry no commit risk. ✓

## 7. Corrections / sharpenings to carry forward

1. **FIRING.md's rotation flag is too mild**: with corr(P2, resolved V/σ)=−0.77 and all
   strict slow-rotator subsets zero-inside, the fixed-IMF cell should be described as a
   *rotation/structure systematics measurement*, full stop — Stage 2 must not reuse P2
   as a β carrier even as a "cross-check" without a rotation control.
2. **The bracket-B standard is vacuous at Stage 1** (predetermined null); a future
   freeze should replace "dies under bracket B" with a control that is not an algebraic
   function of the δ estimator (e.g., IMF-corrected δ *without* σ control, which here
   stays zero-outside at −0.55; or Stage-2 β itself).
3. Freeze timestamps should be hash-stamped (17-s mtime margin this time).

**Bottom line:** all numbers reproduce; the anti-overclaim rails held on both sides
(no manufactured MI win — the run itself proves its MI-signed cell is σ-channel
systematics; no manufactured MG null credited — the structural zero is labelled as
such); the exploratory-firewall language is everywhere; the regime conclusion (the
discriminator's home is deep-MOND, low-y pressure-supported systems with real Jeans β,
not massive ETGs at y≈5–11) is arithmetically forced by the verified budget. **UPHELD.**
