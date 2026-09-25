# J08 — THE χ²₁ SPINE: SPINE RECORD

**2026-09-25 · record-of-record consolidation · closes K01 finding F6 ("J08 — ABSENT") · NO new physics claims · no git commit**

This file exists because K01 demanded it: *"J08 — ABSENT. … J09's two-component law is attributed to J08 (the χ²₁ spine) but NO J08 files exist; nothing to audit; nothing to promote until the J08 record exists."* (K01_TAUTOLOGY_AUDIT.md:209–213). Nothing here is a new claim; every item is a trace to an existing record on disk, plus the one live re-check the closure allowed (n = 2×10⁶, W-KS in 8 D-bins, one cloud).

---

## 1. Definition (the spine, verbatim)

> **W := v²/(2·ang)  |  (D, ang) ~ χ²₁** — W is INDEPENDENT of the whole path geometry (D, ang).

Kept under its own identity from `J09_two_component_law.py:8–22` (docstring, verbatim; J09's header itself says "Follow-on to J08 (χ²₁ spine)"). Consequences recorded (all in the same docstring):

- **A — hierarchy:** E[D·v^{2m}] = (2m−1)!!·2^m·E[D·ang^m] for every m (tested m = 1..5; 7!! = 105, 9!! = 945).
- **B — per-bin law:** v|D is a scale mixture of Gaussians with scales √(2·ang|D), so **kurt(v|D) = 3·E[ang²|D]/E[ang|D]² ≥ 3** (the docstring's "kurtosis-per-bin = 3" headline was corrected to "≥ 3, mixture law" per K01 F2 — see §4).
- **C — atom + window:** P(D=0, v=0) = A = exp(−τ₀(1 + q/3)) (central source, exact); −ln A / E[D] = (1+q/3)/(½+q/4) ∈ [4/3, 2] for κ = τ₀(1+qr²) (K01 F3 re-scope; generalized to (p+2)/(p+1) in J09P, 21/21).

**Why it is what it is:** v|traj ~ N(0, 2·ang) *is the engine's own kick-generation rule* — J02_moment_hierarchy.py draws a Gaussian kick per scatter (line 112). W|traj ~ χ²₁ for every trajectory is then a two-line tower-property restatement of that model input.

---

## 2. Honest classification — LABEL-ONLY consistency family (per K01)

| item | classification | basis (K01) |
|---|---|---|
| J08 spine / J09-A (W-independence, hierarchy every m) | **LABEL-ONLY (A)** | model input restated; K01_TAUTOLOGY_AUDIT.md:157–169 |
| J09-B (per-bin law) | **LABEL-ONLY (A)** | mixture law is the spine re-expressed per bin; "= 3" headline refuted, K01_TAUTOLOGY_AUDIT.md:171–181 |
| J09-C (atom A = exp(−τ₀(1+q/3))) | **LABEL-ONLY (A)** | sampler's own definitional output; K01_TAUTOLOGY_AUDIT.md:183–190 |
| J09-D (ratio window) | conditional real content | τ₀-cancellation genuine; universality re-scoped (F3); J09P lands it 21/21 |
| **Zero discovery weight** | — | K01 §3: "model-input restatements … must read 'consistency family' in any promotion." (K01_TAUTOLOGY_AUDIT.md:246–248, 258–263) |

**NOT promoted.** The spine stays on record only as the hook on which the channel's real (B)/(C) content hangs (J01-C3, J02-B/C, J05-F2/F3, J07-E — all per K01 §3 GO list).

---

## 3. Where the spine evidence lives (file:line | file:check-name)

### 3.1 The definition and the check machinery
- `deepseek_push/J09_two_component_law.py:8–22` — theorem + consequences (docstring).
- `deepseek_push/J09_two_component_law.py:24–28` — check roster (A1–A5, B1–B3, C1–C3; final run: 27 checks).
- `deepseek_push/J02_moment_hierarchy.py:60–119` — the engine; Gaussian kick at `:112` (the reason K01 classes the spine (A)).
- `deepseek_push/J09c_tail_audit.py:4–7, 39–49` — A4/A5 tail-collapse audit; cites the spine's distributional confirmation ("KS ≤ 0.002 in every D-bin, every cloud") — **see the caveat in §3.2 and OPEN items**.

### 3.2 Per-D-bin χ²₁ KS statistics (the demanded spine evidence) — honest statement
**The original per-D-bin KS p-value table (every D-bin, every cloud) was never recorded on disk** — J08 has no files (K01 F6), and the "KS ≤ 0.002" sentence in J09c is a citation to that absent record, with no backing numbers anywhere in the repo. **This record does not paper over that.** What *is* on disk as per-D-bin spine evidence:

- Per-D-bin kurtosis battery (the recorded form of the per-bin spine check), `J09_two_component_law.py:97–126` → results in `J09_two_component_law.out`:
  - `B_central_q0` (out:158–169): kurt 4.34396 / 3.93587 vs mixture pred 4.34851 / 3.91078, n = 75816/bin — two D-bins.
  - `B_central_q10` (out:170–181): 3.47460 / 3.34770 vs 3.48427 / 3.35690, n = 118431/bin.
  - `B_volume_q0` (out:182–193): 4.33031 / 3.93391 vs 4.27403 / 3.95593, n = 56746/bin.
  - Agreement to < 0.06 in every bin, every cloud — the "≥ 3, mixture law" statement.
- **LIVE re-check (this record's allowed leg)** — W-KS vs χ²₁ in 8 D-bins, n = 2×10⁶, central q=0: `J08_spine_recheck.py`, captured in `J08_spine_recheck.out`, table in `J08_results.json` → **§5**.

### 3.3 Atom-mass check A = exp(−τ₀(1+q/3)) — residual per cloud
`J09_two_component_law.py:128–142` (tolerance |A−predA| < 0.005) → `J09_two_component_law.out:194–214`:

| cloud (τ₀, q) | A measured | pred exp(−τ₀(1+q/3)) | residual (abs / rel) | check |
|---|---|---|---|---|
| (1.0, 0.0) | 0.36825833 | 0.36787944 | **+3.7889e−4 / +0.103 %** | C_atom_1.0_0.0 ✓ |
| (1.0, 10.0) | 0.013205 | 0.01312373 | **+8.1271e−5 / +0.619 %** | C_atom_1.0_10.0 ✓ |
| (2.0, 3.0) | 0.018405 | 0.01831564 | **+8.9361e−5 / +0.488 %** | C_atom_2.0_3.0 ✓ |

Residuals all ≤ 3.8e−4 absolute (worst 0.62% relative at q=10) — inside the pre-registered 0.005 tolerance. Window ratios 2.0022 / 1.4413 / 1.5980 vs exact 2.0 / 1.4444 / 1.6 (all inside [4/3, 2]).

### 3.4 Hierarchy ratios m = 1..5 with their subsample-SE budgets
`J09_two_component_law.py:49–95`: m ≤ 2 strict (|ratio−1| < 0.05); m = 3..5 under a **3 × 10-split subsample-SE budget** (code lines 75–91; measured relative SEs 19 % / 39 % / 75 % at m = 3/4/5, docstring lines 51–52) — the m ≥ 4 tail budgets are exactly what K01's re-run exposed (see §4). Recorded ratios (`J09_two_component_law.out`, n = 6×10⁵):

| m | central q=0 (out:32–73) | central q=10 (out:74–115) | volume q=0 (out:116–157) |
|---|---|---|---|
| 1 | 1.0003 | 0.9967 | 0.9945 |
| 2 | 0.9867 | 0.9967 | 0.9858 |
| 3 | 0.9430 | 0.9787 | 0.9518 |
| 4 | 0.8737 (SE-budget) | 0.9035 (SE-budget) | 0.8618 (SE-budget) |
| 5 | 0.7812 (SE-budget) | 0.7444 (SE-budget) | 0.6992 (SE-budget) |

All 15 A-checks PASS under their stated budgets (27/27 total). The m = 4,5 shortfall is tail-limited sampling, not a law violation — the decisive argument is recorded in `J09c_tail_audit.py:39–49` (pure-χ²₁ at the same n shows the same shortfall; E[W⁵] sample SE ≈ 845 at n = 6×10⁵ vs mean 945, ≈ 89 % relative).

### 3.5 Verdict records
- `K01_TAUTOLOGY_AUDIT.md` — per-claim verdicts J09-A (:157–169), J09-B (:171–181), J09-C (:183–190), J09-D (:192–207), J08-ABSENT (:209–213), findings F1–F6 (:215–234), §3 GO/NO-GO (:236–263), Appendix R re-run (:265–289).
- `K01_J09_RERUN.out` — the 19/20 pre-correction re-run (the m ≥ 4 tail-budget exposure). See §4.
- `J09P_GENERALIZED_P_VERDICT.md` — F3 fix landed: 21/21, window (1+q/(p+1))/(½+q/(p+2)), limit (p+2)/(p+1).

---

## 4. Verification history

1. **J09 original run (2026-09-23, pre-audit).** Docstring-claimed 27/27. Per K01 F1 (K01_TAUTOLOGY_AUDIT.md:150–155) the recorded `.out` was 0 bytes — no captured results existed; every J09 claim was officially **unverified-as-recorded**.
2. **K01 independent re-run** (`K01_J09_RERUN.out`, 16:24) — the pre-correction script: **19/20 — A5_volume FAILS** (0.6992, half-splits [0.746, 0.648] both ≪ 1); m = 3..5 sink below 1 for both sources; per-bin kurtoses 3.35–4.33 (mixture preds 3.36–4.27) refute the "= 3" headline; the script's own tail budget was **miscalibrated** ((2m−3)!!-type products where the (2m−1)!! moment is relevant, Appendix R:274–279). **This run exposed the m ≥ 4 subsample-SE budgets** — the fix that became the final J09.
3. **J09 final corrected run** (`J09_two_component_law.py` 16:44, `.out` 16:45): corrected tail budgets (3 × 10-split subsample SE; measured 19 %/39 %/75 % rel), corrected "≥ 3, mixture law" headline per F2: **27/27 ALL_PASSED, exit 0** — the on-disk capture (`J09_two_component_law.out:216–221`: total_checks 27, passed 27, ALL_PASSED true, "ALL J09 CHECKS PASSED"). K01's "must be re-run, re-scoped, re-recorded" is satisfied; the re-scope of J09-D lives in J09P (21/21).
4. **This record (2026-09-25):** J08_SPINE_RECORD.md + J08_results.json; live re-check executed and captured (`J08_spine_recheck.out`) — §5.

---

## 5. Live re-check (the record-certifying leg, n = 2×10⁶)

**W-KS in 8 D-bins against the χ²₁ CDF, central source, τ₀ = 1, q = 0, seed 20260925** (`J08_spine_recheck.py` → `J08_spine_recheck.out` → `J08_results.json`). Continuous part only (ang > 0; atom spike excluded, same convention as J09's B-check). Null: χ²₁ CDF = erf(√(x/2)); KS p-value via the Kolmogorov asymptotic (implementation validated: p(0.8274/√n) = 0.4999, p(1.358/√n) = 0.0499; simulated-null p-mean 0.525, frac<0.05 = 0.035).

| D-bin | range | n | KS | p | mean W |
|---|---|---|---|---|---|
| 0 | [0.0000, 0.0814) | 158175 | 0.00199 | 0.557 | 0.9967 |
| 1 | [0.0814, 0.2081) | 158175 | 0.00219 | 0.434 | 0.9969 |
| 2 | [0.2081, 0.3723) | 158175 | 0.00301 | 0.113 | 1.0039 |
| 3 | [0.3723, 0.5765) | 158175 | 0.00377 | 0.022 | 0.9930 |
| 4 | [0.5765, 0.8279) | 158175 | 0.00164 | 0.791 | 1.0012 |
| 5 | [0.8279, 1.1519) | 158175 | 0.00234 | 0.350 | 1.0009 |
| 6 | [1.1519, 1.6457) | 158175 | 0.00164 | 0.791 | 1.0030 |
| 7 | [1.6457, ∞) | 158176 | 0.00462 | 0.002 | 1.0136 |

**Overall (continuous part):** KS = 0.000627, p = 0.70; mean W = 1.0011 ± 0.0013; atom fraction A = 0.36730 vs 0.36788 (resid −5.8e−4, ≈ 1.7σ).

**How to read it (honestly):** W|traj ~ χ²₁ is *exact by construction* (Gaussian kicks ⇒ any per-bin departure is Monte Carlo noise, not law signal). At n ≈ 158k/bin the median null KS is 0.868/√n ≈ **0.0022** — the J09c-cited "≤ 0.002" bound sits at the null median, so 3/8 bins meeting it (5/8 above) is binomial-consistent (P(≥5 of 8) ≈ 36 %). The p-value battery is uniform-compatible: 2/8 bins with p < 0.05 (P(≥2 of 8) ≈ 5.7 % under null), min p = 0.0024 (P ≈ 1.9 % under null). Aggregate KS p = 0.70, mean W dead-on. **Verdict: the record is live and the spine re-check is consistent with χ²₁ to null noise.** (Spin-off of the "≤ 0.002 in every bin" phrasing at n = 2×10⁶ should be read as a KS-statistic report, not a p-value bar: 3/8 bins beat it, the aggregate beats it 3×.)

---

## 6. OPEN ITEMS

1. **Per-cloud per-D-bin KS tables (q=10, volume) were never recorded** — the only on-disk per-bin records for those clouds are the J09 B-check kurtoses (out:170–193). J09c's "… every cloud" citation is unbacked as recorded; this record supersedes it for central-q=0 only. A per-cloud KS table would be a future run — not claimed here, not fabricated.
2. **J09c_tail_audit.py's own output was never captured** (no `.out`) — its pure-χ²₁ shortfall table is cited as script content, not recorded numbers.
3. Bin-7 (large-D tail) mean W = 1.0136, the battery's largest fluctuation (+3.8σ slip-SE) — flagged; consistent with noise given exact-by-construction status and 8 independent bins.

Nothing else missing: all J09/A/B/C numbers quoted here were read from the on-disk records listed in §3.

---

## 7. Closure statement

**K01 F6 — CLOSED (2026-09-25).** The J08 spine record exists on disk: this file (definition, honest LABEL-ONLY classification, evidence trace with file:line, verification history, open items), `J08_results.json` (live re-check + trace list), and the reproducible `J08_spine_recheck.py` with its captured `.out`. Every claim is traceable to an existing record. Consistent with K01 §3, the spine is **not promoted** — it remains the label-only consistency family that the channel's real (B)/(C) content hangs on. No git commit (per task).