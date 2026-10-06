# CFG369: does dissipation (baryon cooling) settle the cold fluid into the phantom? A four-way swing

Criteria: `FROZEN_CRITERIA.md`, committed alone first in 9e7ae79a1. cm12's cooling functions are copied verbatim (C1 reproduces cm12's crossing 10^11.623 exactly).

**Lane verdict: PARTIAL (both footings). Class: NON-adiabatic. The gravity-only adiabatic route is excluded.**

| sub-test | result | numbers (canonical; alt similar) |
|---|---|---|
| **S2 rate pincer** | **PASS** (R1 = the MOND-radius cooling) | Gamma_cool: MW 2-4e3 H_Lambda (needs >= 1.73); cluster 0.35-0.70 H_Lambda (needs <= 1.93, and even <= 1.04 central). A cooling-keyed rate sits in CFG245's window automatically. The R2 cells (200 rho_b radius) fail: everything is too slow. |
| **S3 levels** | **FAIL** | R1: unsettled fraction e = 0.000 (MW, measured 0.13), 0.002-0.047 (group, measured 0.60), 0.66-0.81 (cluster, measured 0.58). The step lands between groups and clusters (~1e13.5-1e14), 0.5-1 dex too high, and the galaxy floor 0.13 is not produced. |
| **S1 energy** | **MARGINAL** | median epsilon_min = 0.09 (generous E1, r_in = 10 r_M) to 1.76 (high E1); 0.63-12 at r_in = r_M. Cooling radiation is enough only for the low end of CFG245's sink, or with near-unit coupling. |
| **S4 shape (gravity-only adiabatic contraction)** | **FAIL** | median log(M_c,f/M_ph) +0.12 to +0.84, rms 0.45-1.05 dex, slope +0.38 to +0.53 vs log g_bar. Contraction piles fluid into the high-acceleration centre, the opposite of the phantom (which vanishes there). |

**What this narrows (the answer to "where does it point").**
1. **Keep:** a settling rate keyed to the host's gas cooling rate at the MOND radius. It is the first rate in the record that resolves CFG245's galaxy/cluster pincer with no new constant.
2. **Excluded:** gravity-only ADIABATIC coupling (contraction) as the organiser. The exchange must be non-adiabatic, as CFG60 said, and it must REMOVE fluid from the high-g_bar centre.
3. **Open, with sharp targets:** (a) the step is 0.5-1 dex too high in mass (groups settle in this model, but the data say they keep 0.60); (b) the universal galaxy floor 0.13 is not explained (this model settles galaxies completely); (c) the energy works only at the generous end.

Controls C1, C2 PASS. MUTATE (cooling x100) moves e(MW) from 0.83 to 0.00 in the R2 cells and flips S2's passing cells, rc 1.

Run: `python3 cfg369_dissipation.py` (seconds).

## Forward fix (appended after CFG370; no frozen number edited)
The copied cm12 cooling function is 10x too low: its unit is 1e-22, not 1e-23 (bremsstrahlung floor check, CFG370 POST-FREEZE 1). With the corrected cooling (CFG370 POST-FREEZE 2):
- S2 passes only in the R2 / f_hot 1 cells (MW 3.2 H_L canonical / 2.5 alt; cluster 0.02 H_L).
- The R1 cells now FAIL (clusters too fast, 3.5-8.8 H_L).
- S3 still FAILS: MW 0.15 / 0.23, groups 0.96 against 0.60.
The headline "the cooling-keyed rate resolves the pincer" holds only in the R2 cells.
