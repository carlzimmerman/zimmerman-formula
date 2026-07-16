# VERIFY — adversarial verification of the high-z TFR fork confrontation (Lane C/D)

**2026-07-16, independent pass.** Everything below was re-derived or re-fetched independently of
the reviewed scripts (recomputation script written from scratch; papers fetched from
arXiv/ar5iv/A&A full text). Verifier scratch script: `verify_independent.py` (session scratchpad;
all its checks are assertions of the committed scripts' printed numbers, exit 0).

## 1. Script re-runs

| script | exit | anchors |
|---|---|---|
| `ledger_fork_context.py` | **0** | a0(3)/a0(0)=0.737; dlogV(3) canon −0.033 / ALT +0.164; ΛCDM z=1 −0.346 |
| `fork_confrontation.py` | **0** | same anchors + χ² tables identical to FORK_RESULTS.md |
| `prep_2026/btfr_forecast_audit/btfr_forecast_check.py` (bank) | **0** | bump z=0.405 +6.15%, a0(3)~0.74, dlogV(3)=−0.033 |

## 2. Fork numbers recomputed from scratch (E(z) conventions — the Gemini Task-5 trap)

Recomputed with my own CPL implementation (no shared code): f_DE(3)=0.5434, a0(3)/a0(0)
= √f_DE = **0.7370** → dlogV(z=3) = **−0.0331** (canonical); E(3)=4.531 → **+0.1641** (ALT).
Both match the banked anchors to <0.001. Pure-Λ (w=−1, wa=0) gives a0 ratio ≡ 1 exactly.
**The E(z) footing bug is absent**: canonical uses √(ρ_DE ratio), ALT uses full E(z); the banked
script's Task-5 reproduction block shows the old bug (−log10 E(z) with w0=−0.8, wa=−0.5 sold as
"DESI canonical") is quarantined, not inherited. The a0(z) curves in both fork scripts are
consistent with `btfr_forecast_check.py` (same Om=0.315, w0=−0.752, wa=−0.86).

## 3. Zero-points re-fetched from the papers (all verified verbatim)

- **Übler+17** (ar5iv 1703.04321, full text): Δb_sTFR = **−0.44** (z≈0.9), **−0.42** (z≈2.3);
  Δb_bTFR = **−0.44** (z≈0.9), **−0.27** (z≈2.3); slopes 3.60 (Reyes+11) / 3.75 (Lelli+16);
  N=65/46; v_circ² = v_rot² + 2σ₀²(r/R_d); adopted 0.15 dex (M*) and 0.20 dex (gas), verbatim:
  "These choices **likely underestimate the systematic uncertainties**." Abstract confirms the
  bTFR sign structure (negative to z~0.9, positive bTFR evolution 0.9→2.3). **All ledger rows
  exact.** (Ledger paraphrase "may underestimate" — paper says "likely"; harmless.)
- **Tiley+19** (ar5iv 1810.07202, Table 5/3): sTFR **−0.09±0.06** (disky), **+0.02±0.06**
  (rot-dom v/σ>1); K-band **−0.08±0.09 mag**; quality-degrading SAMI moves the local rot-dom MK
  relation by **−0.50±0.10 mag** with slope −9.0±0.3 → −6.6±0.3; no pressure-support correction
  (beam-smearing + inclination only). **All load-bearing ledger numbers exact.** One cosmetic
  slip: the ledger says slope "−8.3 → −6.6"; the rot-dom row is −9.0 → −6.6 (−8.3 is likely a
  different subsample row) — not load-bearing, flagged for a 1-word ledger fix.
- **Disagreement characterization** verified: Übler evolution vs Tiley+19 matched-null is real;
  Jeanneau+26 full text explicitly quotes Turner+17's reconciliation ("many of these studies can
  be reconciled with a moderate evolution ≃ −0.4 dex in stellar mass at z∼1") — as in the ledger.
- **Jeanneau+26** (arXiv 2603.28856 + A&A full HTML): Δb_sTFR = **−0.42±0.05**, Δb_bTFR =
  **0.00±0.06**, 95 lensed SFGs, M*=10^8.1–10.3, Dalcanton-Stilp pressure correction
  (v⊥² = v_c² − 0.92σ_r²(r/R_d)), molecular gas from Tacconi+20 Tab. 2b, atomic from
  NeutralUniverseMachine with **0.8 dex scatter** in log τ_HI, Lelli+19 slope 3.14±0.08. Verified.
- **Amvrosiadis+25** (arXiv 2312.08959 full HTML): Δ = **−0.53±0.29** (sTFR), **−0.26±0.19**
  (bTFR), same local refs/slopes as Übler+17 (verbatim "the same values that were used in Übler
  et al. (2017)"), α_CO = 0.92±0.36. Verified; it also cross-quotes Übler's −0.42/−0.27,
  confirming the "one reproduced high-z bTFR number" claim.

## 4. ΛCDM-degeneracy band: CITED, not invented

Jeanneau+26 verbatim (their Eq. 9, sourced to Dutton+11 / Mancera Piña+26):
M*(z)/M*(0) = [H(z)√Δc(z) / H₀√Δc(0)]⁻¹ · [f_M ratio] · [f_V ratio]⁻³ · [v ratio]³, and
"**The first term on the right-hand side of Eq. 9 evolves by −0.34 dex between z=0 and z∼1,
accounting for most of the observed offset.**" The script's −0.346 at z=1.0 (MMW/Bryan-Norman)
reproduces it. Independently recomputed: −0.346 at z=1; max |ALT − ΛCDM-halo| = **0.118 dex**
over z=0.5–5 (script: 0.118). The degeneracy statement stands: ALT's −log10 E(z) is
ΛCDM-halo-shaped at every probed z; the check was run, not skipped.

## 5. Stellar→baryonic conversions and a0-sensitivity attacked

- **No tuned gas fraction anywhere**: the likelihood uses only the four *published* bTFR
  zero-points; the script performs no stellar→baryonic conversion of its own. The Danhaive
  f_gas=0.77 (+0.64 dex) conversion appears only as an excluded-context note. Clean.
- **Per-sample exact predictions recomputed from scratch** (own ν inversion
  g_bar = (−a0+√(a0²+4g_obs²))/2, each footing its own a0): all 12 prediction cells match the
  script to <0.003 dex (e.g. Jeanneau ALT −0.1791, Übler z2.3 ALT −0.2061, Amvro CANS −0.3518).
  Jeanneau regime hand-check: g_obs=5.83e-11, g_bar/a0=0.30, dilution 0.63 — exact.
- **(v,R) typicals stress-tested**: generous variations move the exact ALT predictions by
  ±0.05–0.10 dex (Jeanneau −0.10…−0.21; Übler z2.3 −0.13…−0.31) — always inside the ±0.27–0.35
  honest bands; no verdict motion. The script's caveat (order-of-magnitude typicals) is honest
  and the sensitivity is bounded.
- **Internal inconsistency found (minor, disclosed here)**: the *ledger context table's*
  "ALT diluted" column linearizes with the CANONICAL a0 (9.36e-11) instead of ALT's own 1.13e-10
  → it understates ALT by ~0.03–0.04 dex (Jeanneau −0.144 vs exact −0.179). The confrontation
  script uses the exact own-a0 computation, so **no verdict impact**; the ledger column is
  explicitly flagged approximate. Recommend a one-line ledger footnote if reused.

## 6. Verdict attacked in BOTH directions

- **Manufactured preference?** No. The best-in-hand lean (Jeanneau, canonical, 0.65σ) is
  arithmetic-verified ((0.179/0.277)² = 0.42 → 0.65σ) and stated as sub-1σ sign-lean only. The
  6σ z~1 internal inconsistency (0.44/√(0.04²+0.06²)=6.1) is correctly reported as a literature
  problem, not evidence. The naive 7.76σ is ALT-side and flagged DO-NOT-CLAIM — so no hidden
  canonical win; symmetrically the a0-only 0.99σ ALT lean is not claimed either (correct: it is
  size-artifact-contaminated, and no sample is deep-MOND).
- **Manufactured wash?** No — the wash is *structural*, not band-width-driven. Two independent
  stress tests: (i) **band scaling** — with sys bands at 0.5×, 0.75×, 1×, 1.5× the flip between
  lanes persists at every scaling (a0-only lean ALT 1.82/1.28/0.99/0.68σ vs size-lane lean
  canonical 1.76/1.24/0.95/0.65σ); even at stat-only the flip survives (7.76σ vs 6.11σ opposite
  sides). Narrow bands cannot rescue a preference because the two model lanes bracket the data.
  (ii) **α-scan of the size comparator** — for α ∈ [0.4, 1.0] the size lane stays
  canonical-side (0.72–0.95σ); the caveat's claim ("moves it but not the flip") is verified.
  The size term itself is legitimate framework physics (M = g_bar R²/G at fixed g_obs; deep-MOND
  R-cancellation confirmed in the machinery) anchored to van der Wel+14, and is not
  double-counted (the local reference relations are (M,v) fits with no size axis).
- **Band budgets not narrowed**: Jeanneau ±0.27 = √(0.20²+0.16²+0.06²)=0.263 ✓; Übler ±0.35 is
  the generous end of √(0.15²+0.20²+(0.1–0.2)²)=0.27–0.32 plus the authors' own "likely
  underestimate" caveat — defensible, and per (i) irrelevant to the verdict. One nuance: the
  ±0.16 "local bTFR ZP" term matches Jeanneau's σ⊥,int^bTFR = 0.16; whether that figure is the
  Lelli+19 ZP uncertainty or intrinsic scatter is ambiguous in the source — either reading keeps
  the band 0.22–0.27 and changes nothing.

## 7. Verdicts

- **UPHELD**: z~1 UNDERPOWERED (best-in-hand Jeanneau leans canonical 0.65σ only); z~2.3 WASH by
  degeneracy (lean flips a0-only ALT 0.93σ ↔ canonical+size 0.42σ); COMBINED WASH/UNDERPOWERED
  (0.99σ ALT-side ↔ 0.95σ canonical-side across lanes). Neither footing preferred or excluded.
- **UPHELD**: ΛCDM-degeneracy statement (ALT ≈ ΛCDM halo drift within 0.118 dex, z=0.5–5;
  anchored to Jeanneau+26 Eq. 9's verbatim −0.34).
- **UPHELD**: the fork stays internally decisive as banked (−0.033 vs +0.164 at z=3, velocity
  axis, opposite signs) but no in-hand sample is deep-MOND (g_bar/a0 = 0.3–6.4) — the banked
  0.2-dex separation is genuinely not available in published data; wash-breaker #1 (Jeanneau
  low-acceleration-third refit) is correctly identified and correctly NOT executed/claimed here.
- **CORRECTIONS (minor, none verdict-affecting)**: (a) ledger's Tiley+19 slope "−8.3→−6.6"
  should read −9.0→−6.6 for the rot-dom MK row; (b) ledger "ALT diluted" context column uses the
  canonical a0 in the dilution factor, understating ALT by ≲0.04 dex (exact script unaffected);
  (c) Übler's caveat is "likely underestimate," slightly stronger than the ledger's "may."
