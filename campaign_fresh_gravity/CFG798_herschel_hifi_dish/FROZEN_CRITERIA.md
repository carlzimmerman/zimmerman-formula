# CFG798 FROZEN CRITERIA: feasibility of an archival Herschel/HIFI dish-antenna search at 541.7 / 595.5 GHz (committed before any query or script)

**Purpose.** Feasibility only. This lane decides whether public Herschel/HIFI data can serve as an archival version of
the PAPER52 search (DOI 10.5281/zenodo.23402086; CFG797 forecast; ARGON03 kill test). The Herschel 3.5 m primary
mirror plays the dish antenna and HIFI plays the heterodyne receiver, following the JWST approach of arXiv:2402.17140.
No spectra are downloaded or analysed here.

**Targets.** These are the CFG797 lines; the identification is equivalent to κ = ½, which is fitted.
- Canonical: 2.240 meV, ν_c = 541.7 GHz.
- Alt: 2.463 meV, ν_a = 595.5 GHz.

A kinetically mixed vector field puts a narrow line (about 0.3 MHz) at a fixed frequency in the spacecraft frame. The
line is independent of the target and the target's velocity. Only an annual/orbital modulation of about 1e-3 (velocity)
remains.

**Coverage rule.** An observation covers a target if the target lies in either sideband, i.e. 4 ≤ |ν_target − ν_LO| ≤ 8 GHz.
- This IF range applies to HIFI bands 1–5; bands 6–7 use 2.4–4.8 GHz and do not reach these frequencies.
- If the archive gives only a sky-frequency range or a band label, use the LO frequency when available. Otherwise use
  the declared range, and say so.
- Primary count: the exact target frequencies.
- Report only: the ±1% window, because ν ∝ √a₀ and a₀ carries a few-% fitted uncertainty (provisional). A wider
  window is a scan and is out of scope for the feasibility verdict.

**Switching rule.** This is declared before looking. A target-independent signal from the primary mirror is present in
the ON beam and in the sky-reference beam alike, so it cancels in any sky-reference subtraction: position switch, dual
beam switch, and the OFF step of load-chop or frequency-switch "with reference" modes.
- **Tier A** (survives the standard pipeline): frequency-switch or load-chop modes without a sky reference.
- **Tier B** (needs reprocessing of the Level-1 phases without the OFF subtraction): every other mode.

Hours are counted separately per tier.

**Integration time.** The integration time t is 0.5 × the archive duration (overheads; provisional). Hours are counted
separately for 541.7 and 595.5 GHz.

**Signal and noise.** These follow the CFG797 formulas.
- Signal: P = (2/3) ε² ρ c³ A_eff, with ρ = 0.01 M☉ pc⁻³ and A_eff = 9.6 m² / S.
- S is the geometry / mode-matching power suppression. Primary S = 50, the literature value for parabolic dishes
  (provisional). Brackets: S = 10 and 1000.
- Each linear-polarisation mixer receives P/2. H and V are combined, so SNR = (P/2)/σ × √2.
- Radiometer noise: σ = k T_SSB √(B/t). Here T_SSB = 2 T_DSB, with T_DSB = 80–150 K for HIFI band 1 (provisional;
  quoted DSB values). B = max(0.3 MHz line width, 1.1 MHz WBS resolution) = 1.1 MHz (provisional).
- ε_min is the 5σ reach.
- Primary case: S = 50, T_DSB = 150 K, Tier A hours.

**Verdict (frozen).**
- **FEASIBLE (clean):** Tier A has ≥ 10 h integration at either target frequency, and the primary-case ε_min < 4e-9
  (the CFG795 converter window).
- **FEASIBLE-WITH-REPROCESSING:** Tier A fails, but Tier B (or A+B) meets the same hours and reach.
- **NOT FEASIBLE:** neither condition holds.
- **Kill line:** whether the primary case reaches ε_min < 1e-12 (the ARGON03 / PAPER52 kill line) is reported separately.
  It is not required for feasibility.
- Results at S = 10 and S = 1000 are reported as brackets. They do not change the verdict.

**Declared systematics for the write-up.**
- The 557 GHz ortho-H₂O line falls 15.3 GHz from 541.7 and 38.5 GHz from 595.5 GHz. It can appear in the image
  sideband for some LO settings.
- Also covered: LO spurs and purity, HIFI standing waves (about 90–100 MHz), and the spacecraft-frame vs LSR frequency
  scale. Level-2 products are Doppler-corrected and must be put back to the spacecraft frame.

**Controls.**
- K1: at S = 1, A = 10 m², ε = 1e-12, and without the 2/3 factor, the photon rate reproduces ARGON03's 4.4e7 per day
  to 5%.
- MUTATE (separate output): ρ → 0 gives SNR 0.

External numbers (T_DSB, S, B, duty factor, IF ranges) are provisional. κ fitted; not theory closed.
