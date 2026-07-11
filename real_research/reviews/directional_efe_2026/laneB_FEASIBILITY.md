# LANE B feasibility verdict -- directional EFE data (2026-07-11)

## What is public (all fetched, in laneB_data/)
- g_ext AMPLITUDE: Chae+2021 (ApJ 921,104) Table 3 = log10(e_N,env) for 109 SPARC galaxies (SDSS footprint), max/no-clustering bracketing; Table 2 = RC-FITTED etilde for 162 galaxies. NOT on VizieR; recovered from the arXiv LaTeX source. Mirrors: home.sejong.ac.kr/~chae + astroweb.cwru.edu/SPARC (neither currently serves the files).
- g_ext DIRECTION: **NOT PUBLISHED ANYWHERE.** Chae's vector sum over 2M++/MCXC/NSA is internal; only |g| released. Reconstructable: the source catalogs (2M++, MCXC, NSA) are public and the method is fully specified in the paper (sec. 3), so the per-galaxy g_ext DIRECTION can be recomputed -- a real but self-contained pipeline (est. days, not months; the dominant-attractor direction converges at the ~10-20 deg level for the strong-field galaxies).
- Per-side velocities, SIGNED + sky direction: van Eymeren+2011a (A&A 530, A29) Table 3 = v_rec, v_appr, v_c, PA(receding), i for 70 WHISP galaxies. SPARC overlap: 26 galaxies. This is the ONLY public machine-recoverable SIGNED per-side catalog found.
- Per-side, UNSIGNED: Ponomareva+2016 Table 4 (tbl_rot): |v_rec-v_appr| (as the V_max 'error') + PA(receding) for 32 galaxies; 11 additional SPARC matches.
- THINGS (de Blok+2008), LITTLE THINGS (Oh+2015), Swaters+2009: per-side curves exist only as FIGURES/private files; VizieR tables carry no approaching/receding split (checked J/AJ/149/180 ReadMe; J/AJ/136/2648 not in VizieR). Velocity FIELDS are public (things.mpia.de etc.), so per-side re-derivation is possible but is a reduction project, not a fetch.

## Overlap (the number that matters)
- Galaxies with BOTH a signed per-side asymmetry AND a published g_ext amplitude: **N = 16** (van Eymeren x Chae T3).
- Adding unsigned Ponomareva matches with g_ext: N = 18 total.
- With RC-fitted etilde instead of environmental e_N: N = 34.
- Galaxies with per-side + g_ext amplitude + g_ext DIRECTION: **N = 0** (direction not public).

## Verdict: PARTIAL
- CONFRONTABLE NOW: only the isotropic |asymmetry| vs |e_N| correlation (N=16 signed + 2 unsigned = 18) -- NOT the pre-registered directional aligned/anti-aligned test, which needs the g_ext VECTOR.
- The missing piece (g_ext direction) exists non-publicly inside Chae+2021's pipeline and IS reconstructable from public catalogs (2M++, MCXC, NSA + galaxy RA/Dec/D).
- No one has published the disk directional-EFE test (searched 2021-2026: Chae, Banik, Kroupa, Haghi, lopsidedness+EFE). Closest: Kroupa+2022 asymmetric tidal tails (star clusters); Chae & Milgrom 2022 computed the azimuthal scatter numerically but confronted no per-side data. The test is OPEN.

## Honest power analysis (from the assembled numbers themselves)
- Measured signed asymmetry scatter (70 WHISP): rms(A) = 0.092 (A=(v_rec-v_appr)/2v_c). This scatter is dominated by ordinary (tidal/accretion) lopsidedness, which is random w.r.t. g_ext and so acts as NOISE for the directional signal.
- Measurement floor (median eps_kin of the 13 Type-1 'symmetric' galaxies): ~0.007.
- N(3-sigma) for a mean aligned asymmetry s (geometric dilution 0.5):
    - AQUAL-class 4%: N ~ 192
    - AQUAL-class 2%: N ~ 765
    - AQUAL-class 1%: N ~ 3057
    - Branch-B w=0.24 x 2% = 0.48%: N ~ 13265
    - Branch-B natural beta=2/7 (~0.28 x 2%) = 0.56%: N ~ 9746
- So: at AQUAL amplitude (1-4%), N ~ 192-3057 galaxies with per-side + g_ext-vector data are needed; the 16 in hand cannot decide even the AQUAL case, and the Branch-B suppressed case needs thousands. A detection/null with N=16 is out of reach at 3 sigma unless the per-galaxy noise is beaten down (stacking by |e_N|, using only strong-field golden galaxies, or per-side errors << the lopsidedness scatter).

## Caveats
- van Eymeren publish NO per-galaxy uncertainty on v_rec/v_appr; sigma_A is honestly unavailable (Type-1 floor above is the proxy).
- eps_kin in [S2] is printed UNSIGNED; the sign here is recomputed from their own v_rec-v_appr columns (verified against printed eps_kin for all 70 rows).
- Chae's e_N,env spans max/no-clustering = a factor ~8 systematic; carry both.
- WHISP eps_kin is measured at the plateau/outermost radii -- roughly the right regime for the EFE, but a real confrontation must match radii to where g_bar ~ e_N a0.
