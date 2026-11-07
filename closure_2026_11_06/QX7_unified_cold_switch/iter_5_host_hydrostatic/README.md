# QX7 iter_5: today's dust held by its host's gravity. FAIL (no window); clusters do not pass anywhere either

Kappa = 1/2 FITTED; not theory closed. Adopts nothing. Criteria 2afe6bac03, committed and pushed before any number.
Script: qx7_iter5.py (one thread, about 25 min); outputs qx7_iter5.json/.out, qx7_iter5_MUTATE.json/.out, run_main.txt,
run_mutate.txt. Mutation of iter_4 (9a8f2e4778).

**Disclosure (11-07): this is an independent REPRODUCTION, not a new kill.** QX10 iter_2 (criteria c1f0cadb7a, A1 168db297bd)
already put the n = 1 fluid in the host's potential and KILLED iter_4's window on KiDS lensing (G6 -0.24 / -0.27 / -0.15 / -0.25 in
cells C1-C4). iter_5 missed QX10 when it checked the record. It agrees on the full grid (-0.27 at 1.47, -0.25 at 2.15, -0.15 / -0.10 at 8.25).
What is new here is the scan to lambda_0 = 100 Mpc (galaxies pass only at >= 10 Mpc, past the growth window) and the cluster readout.

## Mechanism

iter_4 put each system's captured dust in the ISOLATED n = 1 core. iter_5 solves the n = 1 hydrostatic equation in the host's
own field: d rho/dr = -(mu^2/4 pi G) g_law(G (M_b + M_d)/r^2), mu = 2 pi/lambda_0. That is the same K, with no new constant.
The total mass is f_cap R M_b, and a system keeps nothing if the surface r_s >= r_ta. Growth and forest are carried from iter_4
(the switch is unchanged; R1 recomputes one cell exactly).

## Result: FAIL (no window), both footings

| lambda_0 (Mpc) | G5 SPARC | G6 KiDS lensing shift (line 0.05) | G7 ellipticals | in iter_4's growth window? |
|---|---|---|---|---|
| <= 0.15 | fail | fail | fail | no |
| 0.18-0.26 | fail | fail | pass | no |
| 0.32-8.25 | pass | **fail: -0.27 to -0.10 canonical, -0.27 to -0.15 alt** | pass | 1.47-8.25 yes |
| 10-100 | pass | pass | pass | **no** (growth window ends at 8.25) |

- **Why the galaxies break:** under the a0 law a galaxy's pull falls only as 1/r. Integrated over a Mpc, that is a deep well, so
  the host squeezes the dust well inside its turnaround radius. Isolated lensing galaxies then keep 4.2 M_b of dust within a few
  hundred kpc (r_s 0.19 Mpc for a 1e10 system at lambda_0 2). iter_4's isolated core had let them shed it.
- **The galaxy gates pass only at lambda_0 >= 10 Mpc**, and the CMB-lensing growth window stops at 8.25. There is no overlap,
  so the window is empty.
- A Milky Way-mass system (6e10) keeps no dust at any galaxy-ok lambda_0, so the Solar System is untouched there.

## Clusters (reported, ungraded; this readout was added after the first run and is disclosed here)

Clusters were read across iter_4's whole window, ignoring the galaxy failure, to see whether host gravity fixes them on their own.
It does not:

- **X-COP:** the rms never gets below 0.225 (line 0.10). The mean crosses zero near lambda_0 3.2 (+0.033 canonical, -0.002 alt).
- **Groups:** at most 5 of 20 pass the strict rule (needed: 16).
- **The radial pattern is iter_4's, only smaller.** At lambda_0 3.16, every cluster runs from +0.25 to +0.41 dex at 0.1 R500
  (dust missing in the centre) down to -0.19 to -0.36 at 0.7 R500 (too much outside). Host gravity tilts the profile the right way,
  but a sector whose Jeans length is megaparsecs is too stiff to pile mass up on 100-kpc scales.
- **At lambda_0 >= 10, where galaxies pass,** clusters go back toward the plain law (+0.36 to +0.47 canonical).

Reading: for this n = 1 cold dark energy sector, one Jeans length cannot both keep dust out of isolated galaxies and concentrate
it inside clusters. The galaxy side needs lambda_0 >= 10 Mpc, while the cluster shape would need far below 1 Mpc, and that would
put dust in every galaxy (MUTATE C).

## Controls (all hold)

| Control | Result |
|---|---|
| K1 isolated Newtonian = sinc core | r_s err 3.6e-7, enclosed fraction err 2.8e-6: PASS |
| R1 carried growth cell recomputed | dchi2 3.287197 = stored: PASS |
| MUTATE A host off = iter_4 | X-COP +0.0012/0.2346 vs +0.0014/0.2346 (alt -0.0228/0.2337 vs -0.0227/0.2337): REPRODUCES |
| MUTATE B f_cap 0 = QX2 | +0.4675 / +0.4345: PASS |
| MUTATE C lambda_0 1e-3 | G5, G6, G7 all fail: BITES |
| MUTATE D f_cap x3 | X-COP moves -0.270 / -0.264: BITES |

## Disclosed fixes after the first run

- Two plumbing bugs (a missing argument; providers returning a tuple) crashed the first run before any gate was graded.
- The first graded run hit a numerical bracket failure at lambda_0 >= 6.8 Mpc: the host-held solution needs a central density
  far above the isolated estimate. The bracket now expands adaptively. This changes no physics, and K1 and MUTATE A-D are
  unchanged by it. The rows that errored first are the ones the table now grades.
- The ungraded cluster readout across iter_4's window was added after the first graded run. It is outside the frozen report
  list and does not enter the label.

## What this closes, and what stays open

- **Closed (this class):** an n = 1 cold dark energy sector with one leaf-uniform Jeans length, in hydrostatic equilibrium in its
  host, cannot pass the galaxy gates, CMB-lensing growth and clusters together.
- **Still open:** a sector whose stiffness is not one global constant today (for example, set locally by the host's own state);
  real capture and evaporation dynamics; TT/EE; UDGs. Nothing here is adopted.
