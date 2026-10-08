# CFG403: does any z ~ 1–3 disc have OSIRIS AO inner + deep outer + resolved gas? NONE (metadata only)

Criteria were frozen first (9df62e070). The script is `cfg403_match.py`. It uses metadata only: the Keck archive (KOA) OSIRIS frame list (75,569 spectrograph frames) and ALMA archive rows. No frames or cubes were downloaded; the fetch log and sha256 are in `_external_data/cfg403_work/FETCH_LOG.md`.

**Parents.** 442 unique galaxies at z 1–3: KMOS3D 401, SINS AO 36, NOEMA3D 10.

| gate | galaxies |
|---|---|
| A: OSIRIS ≥ 1 h with Hα or [O III] in band, ≤ 0.1″ scale | 8 |
| B: deep outer (a good KMOS3D fit reaching g_obs ≤ 0.55 a₀) | 3 |
| C: ALMA CO or [C I] at ≤ 0.6″, or NOEMA3D | 101 |
| AB / AC / BC / **ABC** | 0 / 2 / 0 / **0** |

With any AO counted for A (adding SINS AO), A·B·C is still 0.

**Verdict.** NONE. OSIRIS goes on the proposal list. The binding gate is B, the deep outer curve: only 3 of 401 KMOS3D fits reach the deep regime, and none of the 3 has OSIRIS data.

**Near misses (post-freeze reading, not a result).**
- **COS4_05433** (z 2.19) has A (1.2 h, Kn2) and C (ALMA CO(3–2) at 0.57″, 2022.1.01644.S). It misses B at g_out 0.77 a₀ against a cut of 0.55. Its inclination is low (33°) and the KMOS turnover is unresolved (r_t at the grid floor). It is the closest thing to a candidate, and it needs a deeper outer curve.
- **GS4_45068** (z 2.45) has A (5.2 h) and C at 0.065″ (CO(4–3) and [C I], 2016.1.00990.S). Its KMOS fit is unconstrained (V_a at the 800 km/s edge), and it is compact and Newtonian (g_out 33 a₀). The outer is never deep.
- **GS4_40768** (z 2.30) has A (6.8 h). Its KMOS fit is unconstrained (eV_a/V_a ≈ 5). ALMA gas exists only at 1.0–1.8″.
- The four SINS-AO galaxies with OSIRIS (BX455, BX502, BX389, BX513) are in Keck LBG fields. They have no ALMA CO at ≤ 0.6″ and no KMOS3D deep curve.

**Controls.**
- C1: BX442 returns 56 frames and 27,000 s in band.
- C2: the GOODS-ALMA positive/negative pair passes.
- C3: CO(3–2) at z 2.2 maps to 108.06 GHz.
- C4: all 442 galaxies were evaluated.
- MUTATE (+60″ in Dec) takes A from 8 to 0, which meets the premise.

**Disclosed.**
- The first draft treated ALMA `s_resolution` as degrees. The archive gives arcsec (checked against the CFG-era footprint rows); this was fixed before the first run.
- ALMA cannot reach EGS or GOODS-N (Dec +53/+62). Those fields return 0 ALMA rows, and only NOEMA3D supplies their gas.
- The footprint test uses the distance to the pointing centre ≤ s_fov/2, which approximates mosaics.

**Not claimed.** No a₀ is measured. "Covers a line" is not a detection.
