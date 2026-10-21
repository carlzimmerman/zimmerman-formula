# CFG960 AMENDMENT A2 (2026-10-21, POST HOC, after the 128³ validation numbers): V-N1's growth sub-line fails as frozen; diagnosis

Added after every 128³ gate was evaluated (cfg960_validate.out). No grade is changed retroactively. No rerun was made because of this.

**Frozen line.** V-N1 (n = 1) has two parts:
- (a) P_grav / P_VS0 within 3% in the two lowest k shells at z = 1, 0.5 and 0, for VSC and VSA;
- (b) VSC's fundamental-mode P_grav growth from z_i, divided by the native D², within 5% at z = 1, 0.5 and 0 (the CFG654 V-N2 form).

**Result.**
- (a) PASSES on both footings: VSC 0.9960 / 0.9902 (z = 1) to 0.9981 / 0.9922 (z = 0); VSA 0.9965 / 0.9915 to 0.9985 / 0.9931.
- (b) FAILS AS FROZEN: 0.9766 / 0.9659 / 0.9486 at z = 1 / 0.5 / 0. z = 0 misses the line by 0.0014.
- **V-N1 is therefore graded FAIL.**

**Diagnosis (post hoc).** The absolute line measures the engine's own fundamental-mode baseline, not SCT-M:

| run | z = 1 | z = 0.5 | z = 0 |
|---|---|---|---|
| plain-dust control VS0, same box, same ICs, CFG654's own S0 code | 0.9805 | 0.9696 | 0.9504 (inside the line by 0.0004) |
| CFG654's 256³ native S0, VNcs (cfg654_validate.json, a committed number) | 0.9839 | 0.9721 | 0.9517 |
| SCT-M growth relative to plain dust, VSC / VS0 | 0.996 | 0.996 | 0.998 |

The roughly 5% shortfall at z = 0 is present without any SCT sector. It is the single fundamental mode of a 100 Mpc/h box, started with 1LPT at z_i = 49 and integrated by the PM. SCT-M's large-scale growth equals dust growth to ≤ 0.4%, which is the n = 1 property the gate was meant to test (CFG953 (b): bodies are free-falling centres of mass, and the body gas grows as a¹). The 5% line was set without knowing that baseline.

**Consequence for the freeze rule.** FROZEN_CRITERIA.md §2 says all gates must pass before `FROZEN_CRITERIA_1024.md` is frozen. That rule is not met as written.
- The 1024³ pre-registration is frozen anyway, with this failure stated in it. The precedent is CFG654, which froze its 1024³ criteria with its V-N1 failing as frozen and explained.
- Every other gate passes: V-K, V-IC, V-MASS, V-MOM, V-LAW, V-SCORE and V-MEM; V-MUT bites.
- **The orchestrator decides whether this is acceptable before starting any 1024³ job.**

**Also reported (post hoc, no grade): why the 128³ preview is strongly below S0 at k ≥ 0.5.**
- The particle field stays close to S0: VC/VS0 particle P is 0.965 at k = 1, z = 0. The gravitating field falls to 0.673.
- Around the 300 most massive bodies (VC, z = 0), the gravitating mass in a cube of half-width 4 cells matches S0's dust to 1%. In the central cell it is only 0.71 (summed) to 0.80 (median) of S0's.
- The cause: the largest bodies have r_e up to about 7 dx ≈ 5 Mpc/h. They spread the converted cold mass more widely than the resolution-limited dust halos they replace at 128³.
- Why the clusters' bodies are so large (checked with the engine's own `fcond_of` at z = 0, canonical):
  - M2's condensed fraction (the own baryons, U5) sits at the census floor 0.100 for every r_ON from 0.78 to 5.5 Mpc/h (M_ta 2e12–7e14 h⁻¹ M☉), because the cooling factor is about 0;
  - so N = M_c/M_b = (1 − f_b)/(f_b f_d) = 53.7 at every mass;
  - CFG953's census used f_ret instead (N 53.6 → 14.9 → 8.3 at M_b 3e10 → 1e12 → 1e13).
  - With f_ret as the own baryons, a cluster's r_e ∝ N √M_b would be about 3× smaller.
- This is a declared-choice sensitivity (U5 / U13, fixed by the task), not a code fault. It is CFG954's cluster core deficit, seen on the mesh.
- At 1024³ the domain floor drops by a factor of 500 in mass and halo cores are resolved, so the 128³ sign and size predict nothing about SC1x / SC2x. An f_ret own-baryon variant would need its own pre-registration; it is not part of this lane.

κ = ½ FITTED; footings never pooled; not theory closed.
