# CFG967 AMENDMENT A1: the d-histogram grid (after stage A's first run, before any score)

Committed with the first-run stage-A script as it ran (`cfg967_pairs_run1_K3b_fail.py`) and its outputs, kept unchanged
(`cfg967_pairs_run1_K3b_fail.out`, `.json`, `cfg967_tables_run1_K3b_fail.npz`).

**Status when this was written.** Run 1 printed only the controls, the cluster edges and the pair counts. No two-halo vector, A
value or slope was printed or inspected, and stage B (the score) does not exist yet. Only the d grid changes; everything else in
FROZEN_CRITERIA.md (908091f9b) stands.

## Finding

Run 1's kernel control **K3b FAILED**: a uniform neighbour field gave |ΔΣ_bin|/Σ₀ = **4.6e-3** (tolerance 2e-3) in CFG687's 8 bins.
K0, K2 (CFG903's stored vectors, max |Δ| = 0), K3a and the internal G-route check passed.

**Cause.** CFG903's d histogram (240 log bins, 75 per decade) has B21's edges on bin edges by construction (`cfg903_lib`
asserts it), and its kernel puts each d-bin's point mass at the bin's representative d. CFG687's edges (0.15·20^(k/8) Mpc) fall
inside d bins. The point mass of a straddling d bin is therefore put wholly on one side of an R edge, a first-order error of about
one d-bin width (3%) in the annulus mass. CFG903's own K2c, on aligned edges, gave 5.9e-5.

## Change (the only one)

- **The d grid is aligned on CFG687's edges:** log bins of δ = log10(20)/128 dex (16 per CFG687 bin, about 2.4% wide).
  - Edges are 0.15·10^(jδ) Mpc for j = −167…147, i.e. 0.00301–4.680 Mpc.
  - Bin 0 is [0, 0.00301) Mpc. That makes 315 bins.
  - Each bin's representative d is the geometric centre (bin 0: 0.0015 Mpc), as in CFG903.
- The neighbour cut stays d < 4.61 Mpc.
- CFG903's kernel and exclusion code are still exec'd unchanged. The new grid is substituted in the `L` they see: D_EDGES, ND,
  D_MAX for the edge list, and dbin_of. Exclusion radii lie on the new d-bin edges from 0.05 to 4.68 Mpc.
- K2 (CFG903's stored vectors) still runs on CFG903's own grid and B21 edges.
- **Added check:** every kernel entry is finite. Run 1 showed floating-point warnings from the BLAS matmul in K3b, while the
  values were finite.

## Not changed

The physics, the data, the edges X1/X2/X3/E0, the brackets, the classes and thresholds, every other control, MUTATE, and the
compute limits.

κ = ½ FITTED; footings never pooled; framework-native; not theory closed.
