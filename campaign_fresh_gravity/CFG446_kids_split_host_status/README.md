# CFG446: is the KiDS early/late split carried by early types that are group centrals? FAILS (E2 companions; E1 non-discriminating)

- **Criteria:** `FROZEN_CRITERIA.md` (f0232a4c1), committed before the script and before any environment or subset number.
- **Script:** `cfg446_host_split.py`, about 45 s, no new data. Main run: 7 of 9 checks pass, 0 load-bearing failures, exit 0.
  MUTATE run: M1 fails as required, exit 1.
- κ = ½ is fitted. B's law predicts the zero early-minus-late difference in K1 under both footings (projected CFG61 stacks:
  +0.0002 in amplitude units, canonical and alt). No dark-matter particle; the cold mass is still required.

## Bottom line

**FAILS by the frozen map (headline measure E2).** Early types with the fewest companions carry the full early/late split:
matched A_poor = 0.95 ± 0.20 (4.9σ), against A_rich = 1.05 ± 0.13 (8.1σ); rich minus poor +0.10 ± 0.28. The split does not
sit in group centrals. This removes the two-regime (host-status) explanation of B's KiDS failure, at the reach of a
photo-z companion count. It does not touch the reading in the other direction: ΛCDM also predicts richer centrals lens more, so
a SUPPORTED verdict would not have discriminated the framework from ΛCDM either.

**E2 does trace environment.** In the outer bins 0–7 (the 2-halo range) the rich tercile lenses +0.49 ± 0.06 dex (7.7σ)
more than the poor tercile, and that contrast vanishes when X is shuffled (+0.03 ± 0.05). So the companion count picks out
denser environments, and the 1-halo split is the same in them. That row was added after the first run (post hoc, reported only).

| measure | gate G (≥ 0.5) | A_poor (matched) | A_rich (matched) | ΔA | verdict (matched; unmatched the same) | power 1/σ_A(poor) |
|---|---|---|---|---|---|---|
| **E1** (< 10% lens mass; the task's measure) | 0.31, FAIL | 1.06 ± 0.15 (7.0σ) | 0.99 ± 0.18 (5.6σ) | −0.08 ± 0.29 | **NON-DISCRIMINATING** (forced by the gate) | 6.6 |
| **E2** (< lens mass; departure) | 1.91, pass | 0.95 ± 0.20 (4.9σ) | 1.05 ± 0.13 (8.1σ) | +0.10 ± 0.28 | **FAILS** (headline by the frozen rule) | 5.1 |

A = the subsample's early-minus-late difference in K1 projected on CFG88's full-sample split (A = 1 is the full split),
against the same all-late reference; errors from the 50-patch jackknife. Unmatched: E2 A_poor 0.88 ± 0.17, A_rich 0.92 ± 0.12.

- **E1 is empty of companions.** Only 6.3% of early lenses have even one pool galaxy 1 dex below them in the aperture
  (rich tercile 18.5%, poor 0.3%), because the bright sample's r < 20 limit sits above that mass at z ≳ 0.2. Read without the
  gate, E1's numbers point the same way (A_poor 1.06 ± 0.15).
- **Power:** both measures can fail. A_poor = 1 would give FAIL with probability ≈ 0.98 (E2), and A_poor = 0 would sit within
  2σ of zero; the observed A_poor is 4.9σ from zero and 0.2σ from one.
- **Late-type check (reported):** late rich minus late poor −0.14 ± 0.46 (E2, matched), +0.56 ± 0.40 (E1).

## Controls

- **C1:** the per-lens sums reproduce CFG88's K1 split to 5 × 10⁻¹⁴ and its zero-model χ² 35.0418/7 exactly.
- **C2:** all 181,477 lenses match the bright sample by exact position; u − r > 2 reproduces the classes; masses, redshifts
  and pool membership agree.
- **C3:** at independent random positions the background-subtracted count is zero: E1 −0.74 SE, E2 +0.46 SE.
- **C4:** the terciles partition each class.
- **C5:** 100 random equal thirds give std(ΔA/σ) = 0.81 (in [0.7, 1.3]). So the jackknife σ of ΔA is about 20% conservative.
- **MUTATE (X shuffled among early types):** M1 fails as required (exit 1). E1's shuffled contrast is 0.36σ. **E2's shuffled
  contrast is 1.81σ**, above the 1σ line. That is one draw from the null distribution that C5 measures (21% of nulls pass 1σ),
  so the E2 half of the control did not bite on this seed. It is kept as it fell. The R-TRACE row is the sharper control: the
  outer-bin contrast falls from 7.7σ to 0.6σ under the shuffle.

## Caveats

- **The companion count is a photo-z proxy.** The window is ±2σ_z (about ±250 Mpc comoving), so the background is about two
  thirds of the raw count (early: raw 0.67, background 0.43). Terciles are noisy in true host status, and the poor tercile still
  holds some centrals. Dilution alone cannot make A_poor equal to A_rich, though. Since R-TRACE shows the ranking separates
  environments strongly, a split carried only by group centrals would have pulled A_poor well below A_rich.
- **σ_z = 0.018 (1 + z) is the published ANNz2 scatter** (Bilicki et al. 2021), quoted, not re-derived. The catalogue has no
  per-object error.
- **"Central" is defined only by mass rank among photo-z companions.** The lens is the most massive galaxy in the aperture
  only within the June |Δχ| < 10 Mpc isolation; E2 permits companions above 0.1 M_lens outside that slice.
- **Shared limits.** The jackknife has no photo-z, intrinsic-alignment or satellite-term covariance (CFG107: ×1.8).
- 46 lenses outside log M* 8.5–11.0 were clipped to the edge matching bins (not specified in the frozen file).

## Disclosures

- E2, gate G and the matched-headline rule were frozen before any result. They were motivated only by a catalogue-only
  completeness table printed before freezing.
- R-TRACE (the outer-bin tracer row) was added after the first run, reported only. No other line changed between runs.
- No derived data are written; the environment counts are recomputed in each run.

## Owner items

- None needed. A spectroscopic group catalogue (GAMA G3C overlaps KiDS-N) would turn host status from a photo-z proxy into
  a membership label. It would need a download (owner's go).

Nothing here says the data favour the framework or ΛCDM, or that the theory is closed.
