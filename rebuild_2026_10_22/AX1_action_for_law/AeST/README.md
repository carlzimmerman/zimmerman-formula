# AX1 / AeST: FAIL on both footings. With the AQUAL static limit no candidate passes Cassini Q2 at all four fields (law 2.44–5.15×; β ≥ 2.5 fail E0 at 1.01–1.12× canonical, 1.42–1.47× alt), and the preferred-frame record (AS3) fails G2c on either branch

Criteria `FROZEN_CRITERIA.md` (alone, before this run) + `../common/FROZEN_CRITERIA.md` (fd417eea04). Engine `../common/ax1_engine.py`. Outputs `ax1_AeST.{json,out}`, byte-identical rerun `ax1_AeST_RERUN.json` (SHA-256 33bdb47c…), twin `ax1_AeST_MUTATE.*` (K1, K2 fail, all QUMOND Q2 = 0, exit 1). Seconds, one thread, no download. **Not blind**; the by-hand expectation in the criteria came true. κ = ½ FITTED. Footings never pooled. Not theory closed. Nothing here says the data favour the framework. The cold sector stays retired. CMB and clusters out of scope, open.

## Result

| candidate | G1 | G2a Q2/Hees E0–E3, AQUAL (E2) canonical | alt | G2b Saturn | G2c |
|---|---|---|---|---|---|
| law | identity | 2.44, 3.48, 3.95, 4.55 **F** | 2.85–5.15 **F** | 1.34e4 / 1.62e4 **F** | **F** |
| law + turn-off | identity | 2.45–4.59 **F** | 2.86–5.18 **F** | P | **F** |
| β = 2.5 … 6 | P (z vs law −0.39 to +1.17) | **E0 1.01–1.12 F**, others ≤ 0.81 | **E0 1.42–1.47 F** | P | **F** |

- **G2c F** (record AS3, 9581518967 / 6770f2d8ad): with a sound speed the static branch is real and α1 = −22/5, α2 = 11/2, off the bounds by 4e4 and 2e7. With no sound speed a moving source returns GR (α1 = α2 = 0) and loses the law.
- How far that second branch reaches, reported only: AS3's capture radius GM/w² is (v_flat/w)² of the MOND radius, 0.02–0.44 for v_flat 50–200 km/s and w 300–370 km/s. So a galaxy moving through the aether at a CMB-like speed would have its MOND region outside capture. This is an argument from AS3's linear result, not a solve, and the aether's rest frame is not fixed.
- The AeST mass term does not screen the Sun: (μ_K r_M)² = 1.5e-17 at μ_K = 0.1 Mpc⁻¹ and 1.5e-15 at 1 Mpc⁻¹.
- G3 P [PROVISIONAL]. G4 O: c_T = c by construction [PROVISIONAL]; X6's health line is not re-read. G5: a0 by hand.
- **Label: FAIL [G2a, G2c for every candidate; G2b for the law] on both footings.** It fails on G2a alone, before G2c.

## Reading
The AQUAL form makes the β escape BIMOND has on canonical fail: AQUAL raises the E0 cell by 1.03–1.22 (E2), which pushes β members over the line. A screened AeST needs a new length; that is the v3s construction, graded in `../v3s/`.
