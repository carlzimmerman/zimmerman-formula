# CFG846 FROZEN CRITERIA: does the excess over the law track gas-poorness at matched g_bar? (H-EX's own prediction; before any script)

## Hypothesis (from canonical v2 S4 / H-EX, no new constant)
Free cold energy = the cold share (5.364×) of EXPELLED baryons. Systems that kept their gas expelled little and carry little
free cold energy; gas-poor systems expelled more and carry more. Across the record the excess appears in gas-poor systems
(satellite dSphs/UFDs +0.4 dex, red lenses +0.20) and not in gas-rich ones (SPARC dwarfs +0.03, blue lenses ~0). **Prediction:**
at matched g_bar, the residual over the law rises with gas-poorness. The law alone predicts no dependence.

## Test 1 (primary): within SPARC
- SPARC (Q ≤ 2, Inc ≥ 30°, errV/Vobs < 0.10), canonical a0, ν_e, Υ_disk 0.5, Υ_bul 0.7 (CFG828 conventions).
- Gas-poorness per galaxy: s = M★/(M★ + 1.33 M_HI), M★ = 0.5 L[3.6] (SPARC table).
- Points with g_bar < 10^−10.5 m/s² (the low-acceleration half). Per galaxy: Δ_gal = median residual log10(g_obs/g_law) over those
  points, and its median log g_bar.
- Statistic: partial Spearman of Δ_gal with s controlling for log g_bar (residualise both on log g_bar by least squares, then
  Spearman of the residuals); one-sided (H-EX predicts > 0).
- **H-EX PATTERN SEEN** if one-sided p < 0.01 and the top-third-in-s minus bottom-third-in-s difference of Δ (matched by
  residualising on log g_bar) is ≥ +0.05 dex.
- **NO PATTERN** if p ≥ 0.05. **HINT** otherwise. (Υ systematics: the same test with Υ_disk 0.4 and 0.6 is reported; the class
  must hold at both to stand.)

## Test 2 (reported, not classed): the pattern across samples at g_bar < 10⁻¹²
- Mean Δ of gas-free satellite dSphs (CFG828) vs SPARC's lowest-g_bar points; B21 red vs blue lenses (CFG829). Listed side by side
  with each sample's typical s.

## Controls
- K1: SPARC overall median residual within ±0.05 dex (as CFG828).
- MUTATE (separate output): s shuffled across galaxies (seed 846) → must class NO PATTERN or HINT, not PATTERN SEEN.

κ = ½ fitted; cold energy mass required; not theory closed.
