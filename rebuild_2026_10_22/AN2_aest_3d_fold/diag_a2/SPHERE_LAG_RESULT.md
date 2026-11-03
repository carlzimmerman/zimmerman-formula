# AN2 diagnostic SL, result: the 3D sphere's lag behind AN1 is grid resolution. Diagnostic only; AN2 stays NO VERDICT, no label changes.

Note `SPHERE_LAG_NOTE.md` (6d62f74836), frozen before any run. Data `sphere_lag.jsonl`. e = 0, eta 0.05, L = 8 q_t, canonical. Not blind.

## Runs (t_q in Gyr; dust reference with the box mean taken out: 4.702)
| Id | Change | N | 1e12 | 1e15 |
|---|---|---|---|---|
| D0 | pure dust, no baryon stop | 64 | 6.561 | 6.561 |
| D0 | | 128 | 5.435 | 5.435 |
| D1 | dust, baryon stop | 128 | 5.435 | 5.435 |
| D2 | hold on, no baryon stop | 128 | 6.216 | 5.443 |
| D3 | as D0, CIC kernel | 128 | 5.596 | 5.596 |
| D4 | as the rows | 160 | 6.042 | 5.266 |
| rows | (AN2 S1, e = 0) | 128 | 6.216 | 5.443 |
| AN1 v3 t_ref | 1D | | 5.277 | 4.701 |

## Read by the frozen rule
- **D0 at 128 is +15.6 % after exact dust** (+39.5 % at 64). Outside 3 %, so the grid and kernel are the cause in pure dust. My expectation (D0 within a few percent) was wrong.
- **Baryon stop (D1 against D0): 0.0 %.** Not a cause. My expectation that it carried most of the gap was wrong.
- **Hold term (D2 against D0): +0.15 % at 1e15, +14.4 % at 1e12.** A cause at 1e12 only. In 1D, AN1 has the same term at +12.2 % over dust, so this is the physics AN1 already holds, 2.1 points larger in 3D. It delays, not hastens, the fold at 1e12; my expectation said the opposite.
- **Kernel (D3 against D0): CIC +2.95 %, later than TSC.** Under 3 %, and in the wrong direction to explain the rows. Not a cause.
- **D4, 128 to 160: −3.2 % at 1e15 (not settled), −2.8 % at 1e12 (settled at 160, as a read).**
- **The gap adds up.** At 1e15, rows over AN1 +15.8 % = dust grid error +15.6 %, hold +0.15 %. At 1e12, +17.8 % = 1.156 (grid) × 1.144 (3D hold) / 1.122 (AN1's 1D hold). Nothing unexplained beyond 3 % of t.

## Extrapolation, a read, not graded
D0's error falls by a factor 2.54 from 64 to 128 (order ~1.34). That order predicts dust at 160 at 5.245 Gyr; the rows' 1e15 sphere at 160 is 5.266, with hold adding 0.15 %, so the trend holds. Taking the dust grid error off the rows' spheres gives about 4.71 Gyr at 1e15 (AN1 4.701) and about 5.38 at 1e12 (AN1 5.277, +1.9 %). So in the limit, the 3D sphere folds with AN1, within 2 %.

## What it means for AN2
- The 16-18 % lag in KE is the engine's resolution on a spherical point focus, not missing physics and not an early AN1 reference. 128^3 is too coarse for a 3 % sphere.
- The shape shifts in AN2 section S1 are measured against the engine's own sphere at the same N, so they partly cancel this error. They aren't re-graded here. A shape's fold (filament, sheet) is less focused than a point, so its grid error is probably smaller than the sphere's, which would make the shifts look larger than they are. Not tested.
- The rule for a rerun: KE needs N with dust error under 3 %, about N 440 at order 1.34 (out of reach on this Mac at 1 GB targets), or a convergence correction fixed before the run.

## Compute
12 runs, nice 15, one thread, two at a time. 128^3 1200-1370 CPU s, 1.3-1.5 GB; 160^3 2970-3180 CPU s, 2.65 GB, over the 1 GB target, under the 67.5 min cap.

kappa = 1/2 FITTED. Canonical only, footings not pooled. A gravitating field, never a particle. The cold sector stays retired. No LCDM input. Not theory closed. Nothing here says the data favour the framework.
