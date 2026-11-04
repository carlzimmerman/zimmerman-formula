# WG2 Amendment A1: committed with the engine, after K1 failed as frozen and before any production run

**What happened.** The frozen K1 (Newtonian growth, EdS, 64³, k < 0.05 h Mpc⁻¹, tolerance 3 %) failed twice:
- **As written:** 0.736.
- **After adding CIC deconvolution:** 0.939.

A diagnostic run, made before any production run, showed the deficit tracks the mesh scale, not the time step:

| setup | k < 0.05 mean | per bin |
|---|---|---|
| 64³, 120 steps | 0.939 | 0.997 at k 0.005 down to 0.833 at k 0.047 |
| 64³, 480 steps | 0.939 | the same |
| 128³, 120 steps | 0.985 | 1.000 at k 0.005 down to 0.960 at k 0.047 |

**Reading.** This is the known slower linear growth of a particle lattice toward the Nyquist scale. At 64³, k 0.05 is 0.4 k_Ny. It is not a code error: the integrator and Poisson solver converge with resolution, and K2's QUMOND construction passes to 2.5e-7.

## Changes
- **A1a.** The CIC window is deconvolved once for the deposit and once for the interpolation, inside the Nyquist sphere. Modes outside the sphere are zeroed. This is standard PM practice; CFG359 did not do it.
- **A1b.** K1 is evaluated at 128³, the production resolution, with the same 3 % tolerance. At 64³ the frozen K1 FAILS, and that is recorded here.

## Consequence to carry into the reading
At 128³ the engine still under-grows Newtonian modes:
- about 4 % in P at k 0.05 h Mpc⁻¹;
- more toward k_Ny = 0.25 h Mpc⁻¹.

That biases C_L low at high L, mostly at z < 1. The 192³ run (K5) measures how much this moves r. Labels, thresholds and the run matrix are unchanged.

κ = ½ FITTED; not theory closed.
