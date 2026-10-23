# G1_smooth_cap: is the CFG555 512³ gravitating-power excess a numerical artefact of the settling cap?

Old engine only (CFG424 lineage: settling rule + additive QUMOND phantom). The covariant theory v3 has neither (F3), so
nothing here transfers to v3, and this lane does not re-score CFG596's KiDS Δχ².

## Verdict

**Frozen line (§5): ARTEFACT.** On substance:

- **The 256³ → 512³ growth of the excess is numerical (operator-grid dependence).** The same evolved 512³ state (R3)
  scored with the rule evaluated on coarser grids gives max|P_grav/P_S0 − 1| (k ≤ 1) = **0.040 (128³), 0.077 (256³),
  0.163 (512³, record)**. The source part at k_max is 0.006 / 0.051 / 0.141. The state is fixed; only the grid of the
  cell-wise rule changes. The excess roughly doubles per grid doubling, so neither CFG555's 256³ pass nor its 512³
  fail is a converged property of the rule. A 1024³ run of the same rule would be expected to sit higher still.
- **The proposed cure fails.** The smooth saturation x/(1+x) (harmonic min, no new constant) at the same per-catchment
  normalisation changes the excess at k_max by **+2.6 % (256³) and +26 % (512³ state)**. That is the wrong way.
  The non-differentiability of max(·, 0) is not the cause.
- **A k-space kernel does most of the work.** The engine's own Jeans filter W_MIX(k) on the source cuts the excess at k_max
  by 55 % (256³) and 80 % (512³ state), but opens a deficit near k ≈ 1 (r_grav 0.92 / 0.90). So max|P−1| barely moves:
  0.079 / 0.096 (step + kernel) and 0.045 / 0.059 (smooth + kernel). An L★ kernel is the identity on these grids
  (rms change of the source 2.6e-7).
- **Aliasing proper is part of it, measured where memory allows.** Evaluating the cap on 2× spectrally upsampled
  inputs and truncating back (128³ → 256³ → 128³) changes r_grav − 1 at k_max by 42 % (TA state) and 45 % (R3 state).
  That is about the whole source contribution in that bin at 128³. But max|P−1| moves only 0.040 → 0.034 / 0.040 → 0.045.
  The un-capped product fsw·catch·s_ph aliases by 30 % too, so the binary masks alias as well, not only the cap.
- **The excess is at low k, not near Nyquist.** At 512³ it peaks at k = 0.32–0.41 h/Mpc = 0.04–0.05 k_Ny (26 record
  runs: all k_max/k_Ny < 0.19). Folding aliasing at fixed k should fall as N rises; the record's source excess at
  k = 0.32 rises ×2.7 from 256³ to 512³. Both point to resolution-dependent structure in the cell-wise rule (rectified
  grid-scale phantom power: about 18 % of the baryon field enters s_ph unfiltered), not to pure folding.

**Bottom line.** The 15–19 % excess is not a converged prediction of the old settling rule. It grows with the rule's
grid, and smoothing the cap does not remove it. This does not rescue PAPER45's growth claim: the rule has no converged
answer at these resolutions. It also does not touch v3.

## Numbers (all in `g1_smooth_cap_results.json`)

| check | result |
|---|---|
| K0 reproduction, TA-can 256³ | P_grav vs CFG555 cache 3.3e-7; max\|P−1\| 0.0749 at k 0.347; r_grav 1.0749; 1972 catchments |
| K1 location (26 runs) | max k_max/k_Ny 0.188; 512³ runs 0.039–0.121 |
| K2 scaling (k = 0.32) | source excess 0.0513 (256³) → 0.1402 (512³), ×2.73 |
| K4, 256³, change of excess at k_max | b1 raw +124 %, b1n +2.6 %, b2 −55 %, b3 −53 %, L★ 0.0 % |
| K4 max\|P−1\| (step 0.0749) | b1 0.160, b1n 0.083, b2 0.079, b3 0.045 |
| K5, R3 512³ state on 256³ grid | step 0.0774; b1n 0.0908 (+26 %); b2 0.0962 (−80 % at k_max); b3 0.0586 |
| K3 aliasing share at k_max, 128³ | TA 0.418, R3 0.449; linear round-trip control 4.4e-7 |
| K6 L★ kernel | rms change 2.6e-7 |

Script: `OMP_NUM_THREADS=1 nice -n 15 python3 g1_smooth_cap.py` gives 7/7 PASS, exit 0, 125 s, 0.97 GB peak RSS (main).
Deposit children peak about 0.4 GB and do not overlap the main peak. `G1_MUTATE=1` (no cap) breaks K0 (3.4e-1): 6/7, exit 1.

## Assumption ledger and criteria

See `FROZEN_CRITERIA.md` (committed alone first, 9921a5172a). Amendment A1 is pre-result (K3 control gate, allocator
settings). Amendment A2 is post-result: the K5 clause of the ARTEFACT line is vacuous, so the frozen verdict rests on
S = 0.553 from the kernel variant. The substantive reading above does not depend on it.

## What it does not show

- No 512³-grid smoothing or 512³ dealiasing was run. That needs 512³ fields of about 0.54 GB each, with roughly 15–20
  live in the diag path: about 8–10 GB for K4 at 512³. K3 at 512³ needs 1024³ upsampled grids, about 40 GB. Run it only after CFG960
  finishes. It is not a PM simulation: one `forces(diag=True)` call per variant on the saved state.
- It does not separate folding aliasing from rectification of resolved grid-scale phantom power at 512³.
- It does not say what the gravitating spectrum of a converged settling rule would be, or whether one exists.
- κ = ½ is FITTED; canonical footing only (both re-run states are canonical; alt 512³ read in K1 only). Not
  "theory closed". Nothing here says the data favour the framework.
