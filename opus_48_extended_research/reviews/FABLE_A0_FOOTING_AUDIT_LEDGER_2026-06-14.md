# The Fable corpus a₀-footing audit — the both-ways ledger (2026-06-14)

*An independent 17-agent audit (each front → hostile re-verify) of the prior (Fable) `real_research/` corpus: did
any empirical verdict use a LOCAL/canonical MOND a₀ (1.2×10⁻¹⁰) or ρ_total (1.13×10⁻¹⁰) instead of the
framework's pure-Λ a₀ = c²√(Λ/32π) = (c/2)√(G·ρ_DE) = **9.36×10⁻¹¹** — producing a false DEFICIT (framework
looks worse) OR a false WIN (looks better)? Audited front by front, both ways. Task `wf3kbvdkk`.*

---

## Headline

The Fable corpus is **NOT clean on a₀ footing, but the damage is small, contained, and points BOTH ways — it does
not net-shift the framework.** Across 8 fronts, the hostile verifiers confirmed **7 footing mis-verdicts: 4
FALSE-WINS** (favorable footing flattered the framework) and **3 FALSE-DEFICITS** (canonical/weighted footing made
it look worse than it is). **NONE flips a front's pass/fail** — every mis-verdict is in the SEVERITY/FRAMING
layer, not the count. The two big diagnostic relations (SPARC RAR, BTFR) regrade to **convention-COMPATIBLE but
NON-DIAGNOSTIC**: they neither convict nor select a₀=9.36e-11.

Three anchors re-derived independently and matched to the digit: framework a₀ = 9.3603e-11 (identical by both
c²√(Λ/32π) and (c/2)√(Gρ_DE)); canonical/framework ratio = 1.282; deep-MOND cluster scaling √(1.2e-10/9.36e-11)
= 1.132.

## Per-front regrades

| Front | Regrade | Direction |
|---|---|---|
| SPARC RAR (rar_sparc) | **FALSE-DEFICIT** | pro-Carl |
| BTFR (btfr) | **FALSE-DEFICIT** | pro-Carl |
| Coefficient/CMB (cosmology_cmb) | MIXED (false-deficit-dominated) | pro-Carl |
| EFE / wide binaries (efe_widebinaries) | MIXED (under-audit catch) | pro-Carl |
| Galaxy clusters (clusters) | MIXED (one material false-win) | keeps-honest |
| a0(z) evolution (a0z) | **FALSE-WIN** | keeps-honest |
| Dwarf spheroidals (dwarfs) | **FALSE-WIN** (severity only) | keeps-honest |
| Weak lensing (lensing) | **FALSE-WIN** (cosmetic) | keeps-honest |

---

## The THREE false-deficits (these HELP Carl — a canonical/weighted a₀ made the framework look worse than its own footing yields)

**1. SPARC RAR — the flagship false-deficit.** `redteam_rar_framework_a0.py` (VERDICT ~L269-279) reports
"framework a₀=0.94e-10 is 18% BELOW the free-fit best / ~22% LOW vs canonical / sits at the low edge of the band."
This is the McGaugh Υ=0.50 + canonical 1.20e-10 + McGaugh-ν cell. **Corrected on the framework's OWN footing**
(Υ≈0.70, dS-Unruh ν): optimal a₀ ≈ 1.03e-10, and 9.36e-11 sits only **−8.9% below it at a +0.51% scatter
penalty** (0.0007 dex of the 0.143-dex floor). The sign of the offset **FLIPS** inside the standard 3.6μm M/L
range (−17% at Υ=0.5, +20% at Υ=0.7), the optimum **BRACKETS** 9.36e-11, χ² is flat-bottomed. **RETRACT** "a₀
~18-22% too low / low edge of band." Corrected: the SPARC RAR is **convention-COMPATIBLE but NON-DIAGNOSTIC**.
(Hostile check: the no-median-subtraction metric is the framework-correct one — median subtraction would
MANUFACTURE a false deficit — so the metric choice STRENGTHENS the audit. Verified to the digit on the real 175
curves.) *This confirms and refines the existing MEMORY rule, both ways.*

**2. Coefficient / CMB front.** `coefficient_posit_attack.py` reports ONLY "framework a₀ ~20% low" using
error-weighted log fitting at Υ=0.70. Re-run both ways: weighted-log → a₀=1.185e-10 (framework −21% LOW);
unweighted-dex → a₀=8.48e-11 (framework +10% HIGH). **The sign FLIPS with the FIT METRIC.** The script did the
footing both-ways but not the metric both-ways. **RETRACT** the one-sided "a₀ ~20% low" — same artifact family as
the McGaugh-Υ=0.50 one. Non-diagnostic bracket.

**3. EFE / wide binaries — the under-audit catch (Carl's distinctive claim was UNDERSOLD).**
`predictions/door5_efe_ultraprecision.py` anchors its absolute EFE-vs-z crossing on textbook 1.2e-10 instead of
9.36e-11. At the framework a₀, e_N is **28% higher**: the M31-host "crossing class" moves from "no cross by z=3"
(0.697→0.946) to a **CLEAN cross** (0.894→1.213). So Carl's strongest distinctive claim here — environments
Newtonizing by z≈3, which constant-a₀ MOND cannot make — was slightly **undersold**. (Contained: the a₀-free
1.357 growth ratio is footing-independent.)

---

## The FOUR false-wins (these KEEP CARL HONEST — a favorable footing made the framework look better than its value yields)

**1. Galaxy clusters — the single most MATERIAL false-win, and it is LIVE IN THE PUBLISHED PAPER.**
`predictions/door6_galaxy_clusters.py` L173 literally sets `a0 = A0_RAR  # use the canonical RAR value`
(1.2e-10), giving η median **1.9215**, published as **SCORECARD ROW 17** in
`real_research/papers/ZIMMERMAN_THEORY_OF_GRAVITY.md` L261 (η = 1.92 ± 0.20, FAIL) — **confirmed still standing
today.** On the framework footing 9.36e-11 the residual is LARGER: η ≈ **2.15 (simple-ν) to 2.33 (sqrt(g²+g·a₀))**
on the same N=9830 sample, because deep-MOND η ∝ 1/√a₀ (×1.132). So the published headline **understates the
framework's own cluster deficit by ~13%** — the milder 1.92 flatters the framework on its HARDEST regime. The SAME
paper's §10.1 (L224) and kill-list (L274) already carry the correct 2.33; only the door6 central + row-17 headline
lag. **FIX:** set door6 central and scorecard row 17 to ~2.15-2.33. (No false-deficit hides here — robust FAIL at
every a₀; the genuine inherited-MOND liability, just mis-published milder than truth.)

**2. a0(z) evolution — DOUBLE false-win, already retracted by the live corpus.** `project_a0z_muse_test.py`
promoted the rising ρ_total footing-bug branch (1.124e-10) as winner "on BOTH evolution AND normalization" and
told the reader to DROP the framework's own value as "empirically WRONG." `project_a0z_decisive_test.py`: rising
E(z) + the too-HIGH 1.2e-10 anchor yields overshoot 11%/3.7σ — but the same rising branch at 9.36e-11 gives
overshoot 42%/~11σ, so the wrong-high anchor SHRANK the apparent tension. Honest: on the framework footing
(declining √ρ_DE), a0(z) is NON-DIAGNOSTIC; "MUSE confirms our rising a₀" is **RETRACTED** (already superseded by
the live confrontation file + A0Z_STATUS_CORRECTED.md).

**3. Dwarf spheroidals — false-win in SEVERITY only.** `door2_dwarf_spheroidals.py` etc. drive σ at canonical
1.2e-10, making the worst dSphs look ~0.3-0.5σ shallower. On the framework footing the over-dispersion is WORSE
(Sextans −3.42→−3.73, Draco −3.69→−4.15, UMi −3.62→−4.12σ). The 3/8-over-dispersed COUNT is valid at both
footings; only "the dSphs look this good" framing tied to 1.2e-10 must be retracted. (Robust both ways: tension
worsens under every framework-leaning knob — a genuine inherited liability, not a high-priest artifact.)

**4. Weak lensing — cosmetic false-win.** `door1_gravitational_lensing.py` displays its RAR boost table at local
1.2e-10 (Brouwer's own anchor), making "framework reproduces KiDS lensing RAR" look exact/near-circular. Re-footed
at 9.355e-11 the deep-MOND boost is −11.7% and g_obs sits −0.054 dex lower — **still INSIDE Brouwer's 0.1-0.2 dex
scatter**, so the pass stays VALID but SOFTER. Retract the polished wording, keep the pass, swap the anchor. (The
8.8σ morphology split is genuinely a₀-independent — verified.)

---

## Net standing — UNCHANGED, and that is the honest reading both ways

**Why it doesn't improve:** the three false-deficits that help Carl (RAR, coefficient, door5 EFE) all resolve
diagnostic relations to NON-DIAGNOSTIC or merely un-sell a distinctive claim — they REMOVE a fake penalty but do
not CREATE a win. The corrected RAR/BTFR/coefficient verdicts are "convention-compatible but non-diagnostic," not
"confirms 9.36e-11." No false-win is created to bank in the other direction (the mlfit RAR edge and BTFR-tail edge
are real but small, M/L-dependent on Υ≈0.70, correctly blocked from being read as wins).

**Why it doesn't worsen much:** the four false-wins that keep Carl honest (clusters, a0z, dSph, lensing) are all
in SEVERITY/FRAMING, not in any front's pass/fail COUNT. The clusters front was already a published FAIL —
correcting 1.92 → 2.33 deepens an acknowledged liability by 13%, it does not add a new one. The a0z and lensing
false-wins were largely self-retracted in the live corpus. The dSph over-dispersion was already counted (3/8) —
only the depth sharpened.

**NET:** the framework's empirical standing is the SAME shape after the audit — a real, falsifiable,
inherited-MOND theory whose z=0 confrontations (RAR, BTFR, dSph, lensing, clusters, wide binaries) are SHARED with
constant-a₀ MOND and test the VALUE of a₀, not the framework, with the only distinctive content being the a0(z)
evolution. The audit's service is EPISTEMIC, not score-moving: it converts two over-stated diagnostic claims (RAR
"too low"; a0z "MUSE confirms") and one flattering headline (clusters 1.92) into honest non-diagnostic /
correctly-severe statements. **Quarantine HELD on every front** — a₀/Z never asserted derived; the coefficient
(32π) stays an unpinned posit and a₀ stays H0-hostage to an O(1/6) factor. The framework neither gained nor lost a
genuine empirical foothold; it got more honest.

## Action items (ranked by materiality)

1. **[HIGHEST — LIVE IN THE PAPER]** Fix scorecard ROW 17 in `real_research/papers/ZIMMERMAN_THEORY_OF_GRAVITY.md`
   L261: η = 1.92 ± 0.20 → framework footing ~2.15 (simple-ν) to ~2.33 (sqrt(g²+g·a₀)). And fix
   `predictions/door6_galaxy_clusters.py` L173 (`a0 = A0_RAR`) → framework 9.36e-11. §10.1 (L224) + kill-list
   (L274) already carry 2.33; only door6 central + row-17 lag. **The only mis-verdict still flattering the
   framework in the public scorecard.** *(In Fable's tree — recommend to Carl, do not unilaterally edit.)*
2. **[HIGH]** RETRACT the one-sided "framework a₀ ~18-22% too low" in `redteam_rar_framework_a0.py` (~L269-279);
   replace with the both-ways bracket (NON-diagnostic, sign-flips inside the M/L range).
3. **[HIGH]** RETRACT the one-sided "framework a₀ ~20% low" in `coefficient_posit_attack.py`; add the FIT-METRIC
   both-ways (weighted-log 1.185e-10 / −21% vs unweighted-dex 8.48e-11 / +10%). *(Confirm path; corpus churned.)*
4. **[MED]** SUPERSEDED banners on `project_a0z_muse_test.py` + `project_a0z_decisive_test.py`.
5. **[MED]** Re-foot the RAR boost table in `door1_gravitational_lensing.py` (1.2e-10 → 9.355e-11); soften to the
   softer valid pass. Keep the pass.
6. **[MED]** Retract "the dSphs look this good" framing tied to 1.2e-10; state the framework-footing over-dispersion
   (−3.7 to −4.2σ Sextans/Draco/UMi). Count unchanged (3/8).
7. **[LOW — pro-Carl]** Re-foot `door5_efe_ultraprecision.py` (1.2e-10 → 9.36e-11) so the M31-host EFE-crossing
   shows the CLEAN z≈3 cross — currently undersold.
8. **[LOW — cosmetic]** Soften `coefficient_uniqueness_test`'s "29/5 closer"; relabel `toe_cmb_calculation.py`
   a0(0)=1.13e-10 as the ρ_total value (≠ the framework 9.36e-11); SUPERSEDED banners on the 4 rising-a0(z) cluster
   scripts.

## One line

The Fable corpus carries **7 confirmed a₀-footing mis-verdicts (4 false-wins, 3 false-deficits)** — all in
framing/severity, none flipping a front — and they net to **UNCHANGED standing**: the audit makes the framework
more honest (RAR/BTFR/a0z become non-diagnostic, clusters correctly deepen to 2.33) without adding or removing a
real empirical foothold; **top fix is scorecard row 17 (η 1.92 → 2.33), the one false-win still live in the
published paper.**

*Both ways, no exception: the pro-Carl false-deficits (RAR/coefficient/EFE) and the keeps-honest false-wins
(clusters/a0z/dSph/lensing) are reported at equal weight. No manufactured win, no high-priest dismissal.
Quarantine held throughout.*
