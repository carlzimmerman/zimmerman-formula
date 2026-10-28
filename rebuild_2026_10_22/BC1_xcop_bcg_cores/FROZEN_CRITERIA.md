# BC1_xcop_bcg_cores: FROZEN CRITERIA (committed alone, before any script or number of this lane)

Written 2026-10-28, at the owner's request: "freeze and run the X-COP lane with an explicit BCG stellar component,
regrading the inner points."

**Why.**
- HO1(a) (91cc5c3bd4) graded the frozen CL2 picture on X-COP's 35 points. The mean was right but the shape wrong:
  - the cores are under-pulled, Δ +0.19 dex at 0.1 R500;
  - the outskirts are over-pulled, −0.12 at 0.7 R500.
- The literature check (2c6b17d683) found the hydrostatic bias small (6–10 %), so the suspect is the core baryons.
- HO1's stars are X-COP's own smoothed stellar profiles (Ghizzardi et al. 2020, `*_mstar.fits`, extension
  MSTAR_SMOOTHED). Whether they fully carry the brightest cluster galaxy (BCG) and its extended light is the question.

**Standing rules.**
- κ = ½ FITTED.
- Footings never pooled; canonical is primary.
- Cold dark energy is not matter and not a particle.
- No ΛCDM number enters a rule.
- Not "theory closed". Nothing here may say the data favour the framework.
- No downloads; on-disk 2MRS (Huchra+12) only.

## 1. BCG component (frozen)

**Identification.** For each X-COP cluster, the BCG is the brightest 2MRS galaxy (smallest Ktmag) satisfying both:
- projected separation from the X-COP header centre (RA, DEC) ≤ 0.1 R500;
- |cz − c z_cl| ≤ 1500 km/s, with z_cl the header REDSHIFT.

Clusters without a match keep HO1's stars, and the count is reported.

**Mass.**
- M★,BCG = Υ_K L_K, with Υ_K = 0.6.
- L_K comes from Ktmag at the luminosity distance used by X-COP's own profiles: d = c z_cl / H0 (1 + z_cl/2),
  H0 = 70.
- **Disclosed:** X-COP's profiles are in its own cosmology (L8, as CS2), so the BCG is put on the same footing.

**Profile.** Hernquist, M(<r) = M★,BCG r² / (r + a)², with a = R_e / 1.8153 and R_e = 20 kpc. Variants are R_e = 10
and 40 kpc.

**Stars in the graded baryons.**
- **PRIMARY (BCG floor):** M★(<r) = max( MSTAR(<r), M_BCG(<r) ). The stars inside r cannot be fewer than the BCG alone.
- **V-ADD:** M★(<r) = MSTAR(<r) + M_BCG(<r). This is the right choice if Ghizzardi's profile excludes the BCG.
- **V-ICL:** V-ADD with M★,BCG × 2. 2MASS total magnitudes are known to miss the BCG's extended envelope and the
  intracluster light; this is a literature-motivated bound.

**Reported per cluster:**
- MSTAR(0.1 R500) / M★,BCG, which tells whether Ghizzardi's profile already carries the BCG;
- the matched 2MRS galaxy and its offset.

## 2. Grade (HO1(a)'s rule and machinery, unchanged otherwise)

The frozen CL2 picture uses HO1's `xcop_cl2` with only the graded baryons' stars replaced. The halo budget is
unchanged (disclosed).

**Graded:**
- **(i)** the full rule: |mean Δ| ≤ 0.05 and rms ≤ 0.10 over the 35 points;
- **(ii)** the inner points (x = 0.1, 0.2; 14 points): mean Δ.

**Verdict (frozen, canonical primary):**

| verdict | condition |
|---|---|
| **BCG FIXES THE X-COP SHAPE** | (i) passes |
| **BCG FIXES THE CORES ONLY** | (i) fails, but the inner mean \|Δ\| ≤ 0.05 |
| **BCG HELPS** | the inner mean Δ falls by at least half (from HO1's +0.19 / +0.03 at x = 0.1 / 0.2, i.e. their mean) |
| **BCG DOES NOT HELP** | otherwise |

## 3. Checks and twin

- **K0 (Step 0).** With the BCG off, the run reproduces HO1(a)'s committed X-COP grade (mean −0.002, rms 0.126, both
  footings) to 1e-6.
- **K1.** For every matched BCG, the Hernquist M(<r) at r = 100 R_e equals M★,BCG to 2 %.
- **K2.** Peak RSS < 1 GB.
- **Rerun.** The results JSON is byte-identical.
- **MUTATE (`BC1_MUTATE=1`, separate outputs).** The BCG mass is subtracted instead of added in V-ADD, and K3 asserts
  that the stars never decrease, so K3 must fail and the run must exit 1.

**Run:** `PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 -I bc1_xcop_bcg_cores.py`
