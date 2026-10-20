# CFG872 FROZEN CRITERIA: what sets the ~6e6 M_⊙ cold clump? Its scaling with stellar mass discriminates the origin (before any script)

**Why.** CFG871: if the dwarfs' extra cold component is a self-gravitating clump obeying the law, its mass M_cl = 81 σ_x⁴/(4 G a0) sets both
its velocity scale and core (r_c = (9/2) σ_x²/a0); the sample mean is ~6e6 M_⊙. Deriving it = deriving σ_x. Candidate origins predict
different scalings M_cl ∝ M★^s:
- **velocity floor** (a universal primordial cold-energy dispersion; clump = the deep-law Jeans mass of that floor): s = 0;
- **catchment supply** (clump = fixed fraction of the dwarf's free cold supply 5.364 × 0.9 M_b/f_ret, f_ret at the census floor): s = 1;
- intermediate s: neither (a different mechanism).

## Per-dwarf clump masses
- Dwarfs with an excess (CFG828 rows, Δ > 0.05; Υ_SFH; canonical a0, ν_e; alt reported). Per dwarf, with the core self-consistent under
  H-LINK: solve for σ_x such that σ_obs² = σ_law² + f(r_1/2; r_c) (2σ_x²)/3 with r_c = (9/2) σ_x²/a0 and f = r²/(r² + r_c²) (root-find; dwarfs
  with σ_obs ≤ σ_law or no root are listed and skipped). Then M_cl = 81 σ_x⁴/(4 G a0).
- Fit log10 M_cl = A + s log10 M★ by least squares; bootstrap σ_s (2000, seed 872).
## Classes
- **FLOOR-LIKE** if |s| < 2σ_s (consistent with 0) and s inconsistent with 1 at ≥ 3σ.
- **SUPPLY-LIKE** if |s − 1| < 2σ_s and s inconsistent with 0 at ≥ 3σ.
- **INTERMEDIATE** if inconsistent with both 0 and 1 at ≥ 2σ. **UNDECIDED** otherwise.
- Report the scatter of log M_cl (intrinsic universality: rms) and the median M_cl, σ_x, r_c.

## Controls
- K1: the per-dwarf root reproduces the pooled CFG870/871 scale (median σ_x within 20% of 7.9 km/s). MUTATE (separate output): σ_obs
  replaced by σ_law × 1.5 for all dwarfs → s must change (shows the fit responds to the data).

κ = ½ fitted; cold energy mass required; not theory closed.
