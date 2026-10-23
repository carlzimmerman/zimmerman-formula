# U1_v3_dust_content — AMENDMENT A4 (POST-RESULT, 2026-10-23; numbers disclosed; no threshold, check or reading changed)

Fix-forward to A2's F5 (Ursa Major members), after the A2 result (54ee83e54e) was committed.

1. **The script's count differs from the frozen F5 wording.** The frozen text (A2, 616ad70e96) says "their points beyond
   r_f". Read literally, r_f is the last radius where V_hold = √2·V_bar ≥ V_rel (0 if there is none), and the points are
   those at R > r_f. The committed script instead selected member points with V_hold < V_rel at **any** radius. That
   includes inner points where V_bar is still rising, and its output line labels them "beyond r_f". The README's "81 %"
   is this any-radius count.
2. **Change (reported only).** `u1_a2_field_frame.py` now prints both readings, each with per-point and per-galaxy
   statistics. The per-galaxy statistic first takes each member galaxy's mean matched-bin offset, then reports the mean
   and sd/√N over galaxies; points within one galaxy are correlated. The original count, its numbers and its output line
   are unchanged: the any-radius per-point mean is reproduced to 7e-18. No check line changed (A2 6/6; mutate F1, F2 FAIL
   as before).
3. **Numbers** (V_rel = √3 × σ_LOS = √3 × 115 = 199 km/s; 28 members, 27 with matched points; canonical / alt):

   | reading | points (fraction) | per point (dex) | Newton | per-point distance | per galaxy (dex) | Newton | per-galaxy distance |
   |---|---|---|---|---|---|---|---|
   | any radius (committed) | 285 (0.814) | −0.042 ± 0.009 / −0.038 ± 0.010 | −0.440 / −0.472 | 42.5 / 44.6 se | −0.063 ± 0.027 / −0.060 ± 0.028 | −0.408 / −0.438 | 12.6 / 13.4 se |
   | beyond r_f (literal) | 262 (0.749) | −0.037 ± 0.009 / −0.033 ± 0.010 | −0.463 / −0.495 | 46.8 / 48.6 se | −0.060 ± 0.027 / −0.057 ± 0.028 | −0.423 / −0.454 | 13.6 / 14.4 se |

   "Newton" is where a dust-free member would sit. The per-galaxy Newton value is averaged over galaxies, so it differs
   from the per-point value.
4. **The README's "~40σ" is a per-point figure.** Within-galaxy correlation makes it overstate the significance. Per
   galaxy the separation from the dust-free (held-group) branch is **≈ 13–14σ** (12.6–14.4 se across readings and
   footings).
5. **No verdict changes.** Under both readings a majority of member points (0.81 / 0.75) are not held, so the class is
   LOST if the group's dust is held. The data sit ≈ 0.04–0.06 dex below the field RAR, far from the dust-free
   −0.41 to −0.50 dex, on both footings. The reading stays **DEPENDS ON whether a loose group's khronon is held**. v3 does
   not establish that, and the favourable alternative is not assumed. κ = ½ FITTED; footings never pooled.

Run: `OMP_NUM_THREADS=1 nice -n 15 python3 rebuild_2026_10_22/U1_v3_dust_content/u1_a2_field_frame.py` (2 s, exit 0) and
the same with `U1_MUTATE=1` (exit 1; F1, F2 FAIL). The regenerated outputs differ from 54ee83e54e only by the added A4
keys and lines, plus runtime and RSS.
