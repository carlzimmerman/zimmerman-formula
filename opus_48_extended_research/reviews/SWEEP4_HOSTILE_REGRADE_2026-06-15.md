# Sweep 4 (global intersection / fine-tuning) — HOSTILE REGRADE (Opus 4.8 [1m], 2026-06-15)

*Independent re-run of both grids + cross-check of every load-bearing claim against the banked same-day ledgers
(Sweep 1 box, Frontier-3 hostile regrade, Skordis CMB-cluster deep-dive) and the Mistele 2023 paper (web).
Both ways. Quarantine held: a0/Z never asserted derived.*

## NET: the headline verdict (the MIDDLE one) SURVIVES, but three load-bearing supports are corrected.

The Sweep 4 bottom line — **"jointly viable + LCDM-natural for 8 of 9 fronts (a0=Λ band contains 9.36e-11);
the 9th (clusters) uncured-within-constraints but soft/shared, not a hard kill; box factorizes into A=(a0,Υ,ν)
and B=(μ,I0,cs²)"** — is CORRECT and robust. The factorization (a0 absent from linear cosmology) is real, the
+2 cost (I0, μ) is the right count, the cluster loss is genuinely soft/systematic-limited/MOND-shared. But the
*justification* leans on three claims that are wrong or overstated; correcting them changes the cluster-corner
verdict from "narrow-but-survivable window" toward "empty-to-marginal," i.e. the regrade is HARDER on the
cluster cure, not softer.

## CORRECTION 1 — the primary grid is STALE and self-contradicts the headline (a process bug, not a physics error)
`/tmp/global_intersection.py` (the grid the ledger header cites first) STILL prints
`INTERSECTION = [1.00, 1.50]e-10 ; 9.36e-11 inside: False` — it was never updated after the BTFR-floor artifact
was caught. The headline "[0.88,1.14], 9.36 inside" comes ONLY from the second grid `a0_joint_recheck.py`. The two
banked grids disagree with each other and the ledger silently uses the corrected one. The corrected band is the
right one (see Correction 2), but the ledger should not cite a grid that prints the opposite of its headline.

## CORRECTION 2 — the BTFR "9.36 inside" is RIGHT, but `a0_joint_recheck.py`'s ±12% hand-wave is the WEAK form.
The strong, banked argument is `btfr_hostile_recheck.py`: the all-sample "implied a0 runs high (1.24–1.52e-10)" is a
**slope-4-forcing pivot artifact** (implied a0 SLIDES with the V-window). In the actually-valid deep-MOND tail
(V<80, Υ0.70) the per-galaxy median a0 is **8.7–9.5e-11, bracketing 9.36e-11** (N=13–31, ~0.09 dex scatter →
non-diagnostic, no false-win/no false-deficit). So the BTFR genuinely does not exclude the framework value — but via
the pivot-artifact argument, NOT the crude "1.40×0.5/0.7=1.0 then ±12%" in the recheck grid. Conclusion stands;
provenance upgraded. The MEMORY both-ways catch (the Υ=0.50 floor was an artifact) is REAL and correctly flagged.

## CORRECTION 3 (the big one) — the cs²→0 "over-clusters the 30 kpc RAR" claim is OVERSTATED (own sister-regrade already demoted it).
Sweep 4 §B1 and `global_intersection.py` say cs²≈0 ⟹ scale-blind ⟹ the dust clusters at 30 kpc and over-clusters the
galaxy RAR. **Independently recomputed (this regrade): with cs²∝a⁻³ the comoving Jeans length is scale-invariant at
λ_J ≈ 0.11–1.3 Mpc** (depending on the CMB bound cs²₀∈[7.7e-12, 1e-9]) — ALWAYS above the 30 kpc galaxy scale. The
dust is NOT scale-blind and does NOT cluster at 30 kpc. This is exactly what HOSTILE_REGRADE_FRONTIER3 (same day)
already found (λ_J~0.14–0.22 Mpc) and demoted. The robust defeater is the **AMOUNT** (CDM-sized I0≈0.265 over-closes
clusters ~3× where MOND already explains most mass) + **galaxy-OUTSKIRT re-haloing** (~150 kpc, not 30 kpc) — NOT
literal scale-blindness. The +2 verdict survives; the stated reason is wrong and must be the amount/double-count.

## CORRECTION 4 (the crux, the task's question c) — the Mistele μ-window is EMPTY-to-MARGINAL under the literature bounds, not "narrow-but-non-empty ~4×".
The two same-day ledgers use INCONSISTENT Mistele bounds and reach opposite verdicts:
- **Sweep 1 + SKORDIS deep-dive (literature-honest):** galaxy-WL needs m²/f_G < ~1 Mpc⁻²; clusters need > ~2.5 Mpc⁻²
  (for ≥10% at R500). ⇒ 1/μ must be BOTH >1.0 Mpc AND <0.63 Mpc ⇒ **EMPTY / inverted, no overlap.**
- **Sweep 4 grid (relaxed):** galaxy-WL mapped to 1/μ>0.3 Mpc (300 kpc) and cluster to (μ·1.3Mpc)²>1 ⇒ m²/f_G>0.59,
  giving overlap [0.3,1.3] Mpc. **Both relaxations are inconsistent with m²/f_G<1 (which is 1/μ>1.0, not >0.3) and
  with the ≥10% cluster bar (>2.5, not >0.59).**
- **Web-verified (Mistele+2023, arXiv:2301.03499):** the WL bound is m²/f_G ≲ 1 Mpc⁻² (Skordis-Złośnik's own), and
  **WL probes radii up to ~1 Mpc** — overlapping cluster scales, not 300 kpc. Mistele's actual result: even AT
  m²/f_G≲1 AeST ALREADY shows MOND-deviations at WL radii that the data do NOT support. So the galaxy-WL side is in
  tension at the boundary BEFORE the cluster side pushes μ up.

⇒ The honest reading is Sweep 1's, not Sweep 4's: the μ-window for a cluster cure is **empty-to-marginal**, and the
galaxy-WL data already disfavor the boundary. "Narrow but non-empty (~4×)" is too generous. The cluster corner is
closed HARDER than Sweep 4 states.

## CORRECTION 5 (both ways — this one cuts FOR the framework) — the morphology split is 6σ, not 8.8–9.2σ.
Sweep 4 cites the a0-independent morphology-split standing loss at "8.8–9.2σ." Two banked cluster ledgers
(CLUSTER_DENSITY_A0_SHAPE_RECONCILED, CLUSTER_MEASUREMENT_PLAYBOOK) explicitly correct this to **6σ (Brouwer 2021)**
and flag 8.8σ as the wrong number. The *direction* (genuinely a0-independent, no box point erases it) is verified;
the magnitude was inflated. Use ~6σ.

## What SURVIVES at full weight (credit, both ways)
- The 6-D box DOES factorize (a0 absent from linear cosmology / δq⁰⁰=0) — sub-box A and sub-box B share no parameter. Real.
- Sub-box A is BROAD and contains 9.36e-11 (the corrected BTFR + RAR + IF-free ratios) — ≤~1.5σ any front, LCDM-like.
  More economical than LCDM at galaxies (a0=Λ replaces ~350 SPARC halo params with one number).
- The +2 count (I0 for CMB, μ for clusters) is right; the CMB fit is at LCDM CMB-parameter-count (+1 measured I0). Natural.
- The cluster loss is genuinely SOFT (true η(R500)~1.3–1.9 after WL-vs-HSE softening), MOND-SHARED, lensing-confirmed (no-slip).

## What is OVERSTATED / WRONG (concede, both ways)
- The primary grid is stale and prints the opposite of the headline (process bug).
- The cs²→0 "over-clusters 30 kpc" argument is quantitatively wrong (Jeans λ~0.1–1.3 Mpc); real defeater is the amount + outskirt halo.
- The Mistele μ-window is empty-to-marginal under the literature bounds (m²/f_G<1 WL vs >2.5 cluster), NOT a survivable ~4× window.
- The morphology-split σ is ~6, not 8.8–9.2 (over-stated AGAINST the framework — corrected in its favor).

## REGRADE VERDICT
The MIDDLE verdict stands and is the honest one: **jointly viable + LCDM-natural for 8 fronts (sub-box A broad,
contains 9.36e-11); the 9th (clusters) uncured-within-constraints but soft/shared/systematic-limited — a
survivable-soft-loss, not a hard kill.** The fine-tuning is honestly split (A broad / B's CMB-slice natural / B's
cluster-cure-slice empty) and NOT hidden. The one substantive change: the cluster-cure corner is closed HARDER than
Sweep 4 implied — under the literature Mistele bounds the μ-window is empty-to-marginal (not a ~4× survivable
window), and the cs²-scale-blindness prop is wrong (use the amount/outskirt-halo defeater). Neither correction
flips the verdict: a0=Λ still does not supply the cluster cure either way, so the 9-front intersection is empty for
a clean cure regardless — the corrections make the EMPTINESS more certain, not less, while leaving sub-box A's
breadth and the soft/shared cluster loss intact. No manufactured viable corner (the ~4× window was the only
near-manufactured element, now corrected to empty-to-marginal); no high-priest dismissal (sub-box A is genuinely
broad and credited). Quarantine held.
