# CFG570: ALMA archive metadata survey of the z 1.2–2.0 window (no download)

Criteria 87dd5ed40 (committed alone, first). Run: `python3 cfg570_alma_window.py` (and `--mutate`). Metadata only; nothing downloaded.

## Result
- **Sample:** 198 galaxies at 1.2 ≤ z ≤ 2.0 (KMOS3D catalogue + KURVS). 43 of them carry deep Hα kinematics (RC100 / RC41 / KURVS / KMOS3D highSN). Eight RC100 window discs have no position on disk (EGS, zC, D3a, GK) and were not searched.
- **Tiers (all 198):** A 10, B 8, C 77, D 71, E 32. The CONTAINS check disagreed with the box+s_fov method on 7 of 25 A/B candidates; the CONTAINS result is used.
- **Deep-kinematics discs (43):** A 4, B 1, C 24, D 11, E 3. Usable at the metadata level, five:

| disc | z | ALMA | verdict |
|---|---|---|---|
| KURVS-15 | 1.613 | Molina 2019.1.01238.S CO(2-1) 0.11″, 6.2 ks | already analysed: CO **not detected** (CFG569) |
| GS4_16814 (RC100) | 1.615 | the same Molina pointing, 6.8″ from KURVS-15 | massive (V 227 km/s, logM* 10.9–11.2, f_DM 0.06): near-Newtonian; the record's full-resolution Molina cube was never fetched (28.8 GB) |
| GS4_24110 (RC100, highSN) | 1.997 | **[CI](2-1) 0.09″, 13.9 ks, 2025.1.01377.L "HIDING in the HUDF"** (Boogaard) | **proprietary until 2026-11-28**; also a 178 s Kohno scan (too shallow) |
| KURVS-18 | 1.341 | CO(5-4) 0.15″, 176 s (Kohno 2015.1.00098.S) | too shallow (3.8 mJy/beam) |
| KURVS-14 | 1.389 | [CI](2-1) 0.47″, 242 s (Scholtz) | too shallow |

- **Tier A/B without deep kinematics:** 13 galaxies (list in the .out). Their gas maps could exist, but their Hα curves aren't deep.

## Bottom line
The z 1.2–2.0 window has **no public resolved-gas + deep-kinematics disc that the record hasn't already tried**. The one real lead is GS4_24110 (z 1.997): deep 0.09″ [CI](2-1) from an ALMA large programme, public on **2026-11-28**. One galaxy is a demonstration, not an a0(z) test. Massive discs like this stay near-Newtonian, so the low-V (120–180 km/s) sample still needs new observations.

## Controls (kept as run)
- **C1 FAIL, a criteria-writing error.** The criteria named 2018.1.00164.S (Ibar) as KURVS-15's ≤ 0.25″ CO(2-1) programme. That programme's beam is 2.48″ (tier C); the 0.11″ CO(2-1) is Molina's 2019.1.01238.S, per CFG569's own criteria. Both the box and the CONTAINS method do recover KURVS-15 at tier A from 2019.1.01238.S (see the .out).
- **C2 PASS** (empty field).
- **MUTATE** (+1° Dec): A+B goes from 18 to 0 → detected (exit 1).
- **Departure:** after the first run, data_rights and release date were added to the printout (a display change only; tiers unchanged). Both modes were then re-run.

κ = ½ fitted; the cold mass is still required. No a0 number, no detection claimed.
