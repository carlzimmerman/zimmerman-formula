# Deep-regime a0_eff audit (2026-09-25)

`D01_deep_a0eff_ml_audit.py` (run from the repository root; `MUTATE=1` must fail) audits the "SPARC-deep a0_eff = 0.72 a0" channel
(deepseek_push L06 → N05) that anchors O04b's "joint deep a0_eff = 0.7172 ± 0.0593, 4.77σ below the canonical a0".

**Finding (load-bearing checks D1–D5 pass):** the 0.724 is reproduced exactly from its inputs, and those inputs are the corpus v7
per-galaxy disc mass-to-light ratios (median 1.17, 84th percentile 2.97, up to 15 on gas-rich dwarfs, applied to bulges too) that
multiply SPARC's own 3.6 µm curves. With 3.6 µm population ratios (0.5–0.7) the same statistic on the same rings is 1.39–1.87, and
the α = 1 moment estimator is itself biased 17–26 per cent high for data obeying the in-force kernel. O04b is therefore not a
measurement of a0 against the canonical value; the downstream "a0* ≈ 6.0–6.8e-11" (N01, ZD07–ZD11) inherits it.

**Against interest (D6 FAILED as pre-stated, D7 diagnoses):** fitted with the in-force kernel, the deep band g_bar < 0.1 a0 gives
κ = 0.34–0.44 when every point is weighted equally and 0.43–0.56 with the standard quality cut or error weighting (Υ_disc 0.5–0.7).
The deep band measures κ only to about ±0.1 once point selection is varied — it neither confirms ½ nor supports a 4.77σ deficit.

## D02 — the deepseek chain re-run correctly (2026-09-25)

`D02_deepseek_chain_rerun.py` (run from the repository root, ~30 min; `MUTATE=1` must exit 1) re-runs **25 deepseek_push lanes
with their own code** in a sandbox (`sandbox.py`: copy-on-write clones of every lane file, read-only symlinks for data, nothing
written to the tree) on the committed corpus with only the SPARC `m2l_disk` replaced by 3.6 µm population ratios (Υ_disc
0.5 / 0.6 / 0.7, Υ_bul 0.7, err/V < 10%; a fourth variant without the cut). A baseline sandbox must first reproduce all 21
committed result files to 1e-9 (B1), except the seven G199 fields that change with Python's hash seed alone (its bootstrap
errors and the z-scores built on them), which a two-seed probe measures and the output lists. The only edits to lane code are input **lookups** (`lanes.py`): value-range lookups that
assumed a deficit (O04b, P02), N05's 1 − |Δ|/a₀E mapping, Q02/R03's hard-coded absolute corpus path, G183's hard-coded ring
count, and ZD08/ZD11's hard-coded a₀*. Corrected lane outputs are archived in `D02_rerun_outputs/<variant>/`.

**Root cause (R1):** the corpus `m2l_disk` values correlate at r = 0.92 (log) with the ratio at which Newtonian baryons alone
fit each rotation curve — kinematic fits, so every a₀ measured from them is circular.

**What changes (C1–C10):** the SPARC-deep α = 1 a₀_eff reverses from 0.724 to 1.44–1.87; O04b's own heterogeneity test fires
(χ² 24–52), so the "4.77σ below canonical" joint is not banked; the Q02 anchor rises from 0.83 to 1.42–1.95 and its
CONSTANT-OFFSET verdict becomes Υ-dependent; the MIGHTEE "mirror" dissolves at Υ_disc 0.5–0.6 (z 1.1–2.5 against 7.0);
S01's "sign mirror" reading fails (both surveys above 1); the S02-plane impossibility leg loses its opposite-sign premise
(it survives by magnitude); the SPARC-deep a₀* "wedge" moves from 6.4e-11 to 1.16–1.38e-10, ZD08's "6% agreement" becomes
a factor ~2, and G183's pooled n-free exponent moves from 3.16 to 2.1–2.3.

**What does not change (S1, S2):** G158's slope channel stays at n ≈ 1.2, 12–20 "σ" from n = 2, so the correction leaves
falsifier row 11 where it was (whether row 11 tests the law at all is D04's question); N01's kill of a₀(ρ_local) stands.
Corrections are appended to `deepseek_push/CANDIDATE_LAWS_REGISTER.md` and `deepseek_push/FALSIFIER_MATRIX.md` (append-only).

## D03 — the other three corpus readers (g03d, g03e, G119)

`D03_corpus_side_lanes.py` (seconds; `MUTATE=1` must exit 1) re-runs the three remaining lanes that read the corpus `m2l_disk`.
g03d's bare deep-regime a₀ (the "G03D register", 0.692 a₀_DE) becomes 1.16–1.41 a₀_DE, and g03e's 0.748 becomes 1.15–1.38.
Both lanes fit a₀ on fixed grids: the committed g03e value and g03d's EFE-boosted value (the "0.534" that falsifier row 17
cites) sit exactly on the grid floors, so they are bounds, not fits. G119's algebraic results do not depend on the corpus.

## D04 — does falsifier row 11 test the law? (G158's slope channel, run on the law itself)

`D04_g158_slope_channel.py` (run from the repository root, ~4 min; `MUTATE=1` replaces the law by the task curve β = n/2 and
must fail M1, I1, I2, D1 and A1) feeds G158's own estimator, reproduced to 0.0 on 145 numbers (B1), data that obey the
in-force kernel exactly. Samples are G158's: MIGHTEE-HI, SPARC through G071 (committed and the four corrected corpora) and
the LITTLE THINGS dwarfs.

**Finding:** row 11 measures β = 1, not n = 2. The rule n = 2β gives the canonical footing the Newtonian deep slope, while
the law's deep slope is ½ at both footings (M1). On law-exact data at the canonical footing the row fires in 88% of draws
(per-galaxy reading) and 100% (ring level). With its own mapped null true (β = 1) it fires in 4.5–7.0% / 7.8–14.5%, and its
reading moves only 0.009–0.010 between the two footings (I2). The measured per-galaxy deep slope agrees with the law's own
slope at the same points (D1: pooled z +0.33 to +0.70 over the corrected corpora).

**Against interest, kept:** I1 FAILED its pre-stated 95% bar (88% on the per-galaxy reading) and P1 FAILED its 3σ bar for
a slope of 0.75 (2.2–2.8σ; β = 1 is excluded at 6.0–6.9σ), so the main run exits 1. The deep slope is consistent with the
law, not a sharp confirmation of it. The ring-pooled slope sits 1.5–2.2σ below the law (D2, reported). In the amplitude
channel, where the footing lives, the three deep samples share one amplitude under the in-force kernel (A2: χ² 3.1–8.0,
df 2), jointly n = 1.35–1.52 ± 0.14: 3.3–4.8σ below the canonical n = 2.000 and 1.0–2.3σ below the alternative 1.660. The
lean is carried by MIGHTEE at its fiducial stellar ratios (n = 1.12 ± 0.16, statistical errors only). The survey's own
refit at a SPARC-class Υ_K = 0.6 gives 1.15 a₀_DE, and with MIGHTEE put there the joint becomes n = 1.66–1.83: 1.0–2.0σ
from the canonical footing and 0.0–1.0σ from the alternative (a labelled what-if). Corrected SPARC alone gives 1.61–1.97.
The deep amplitude sits between the two footings and is set by the stellar mass-to-light convention. A diagnosis section, added after the first run and labelled as such, finds that G158's error
bar is the spread of three numbers. Its "12.7σ" is then a t statistic with 2 degrees of freedom (p = 0.009), and that
error swells in the 12% of law-exact draws where the row does not fire.
