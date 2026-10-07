# CFG386: pre-flight. Do any ON-DISK discs individually span the regimes CFG385 needs?

Criteria: `FROZEN_CRITERIA.md`, committed alone first in d5711e013. A pre-flight: candidate counting only; no law scored.

**Verdict: NONE ON DISK** (0 qualifying under every rule: conservative and lenient inner radius, with and without pressure; KMOS3D z 2.0-2.7 and KURVS z ~ 1.5).

**Why (structural):**
- **KMOS3D (192 fits):** seeing-limited curves span only about 2x in radius (median rmax/PSF = 2.15), so about 2-3x in g_obs. The test needs 6.4x (3.5 a0 -> 0.55 a0). 69 discs have a strong inner point (>= 3.5 a0 at the PSF radius) and 50 have a weak outer point (<= 0.55 a0), but NO disc has both: the massive ones never reach the deep regime and the small ones are deep throughout. Only 58 of 192 fits have eVa/Va <= 10%.
- **KURVS (22):** the outer points are deep (down to 0.02 a0), but the listed points start at 3 R_d, so there is no inner Newtonian anchor (best inner 2.2 a0, KURVS 3; only 8 of 22 have all errors <= 10%).
- **SINS/zC-SINF AO (CFG280):** one published radius per galaxy, so 0 by construction.

**What a spanning disc needs:** AO-resolved inner points (about 1 kpc) AND deep outer points (3-5 R_e) for the SAME galaxy.
- On disk: the 5 KMOS3D x SINS overlaps (K20-ID6, K20-ID7, GMASS-2303, GMASS-2363, ZC410041; data_assembly/kmos3d_cubes/k3d_C1_sins_overlap.csv). A combined inner+outer per-radius extraction is possible locally, but 5 < 10, and their SINS data may be seeing-limited rather than AO (to check).
- External (NOT fetched; each needs the owner's go): Genzel et al. 2017 (Nature; six individual deep outer curves at z 0.9-2.4, several with AO); Lang et al. 2017 (stacked to about 4 R_e; usable only if re-stacked in y); newer JWST/NIRSpec IFU and ALMA kinematics with resolved inner discs.

**Disclosed:**
- The first run silently skipped every KURVS row (R_d was looked up in the wrong table). It was fixed (R_d = R_e/1.678, the KMOS3D rule) and C3 now guards against silent skips.
- MUTATE (a0 x 10) does NOT change the count (0 -> 0), so the frozen premise is not met. The zero is structural (span), not threshold-driven.
- Qualification uses fit-model extrapolations to the PSF radius and rmax, not independent per-radius points.

Controls C1 (D_A 8.468 kpc/arcsec at z = 2.2), C2 (the arctan model) and C3 (no silent skips) pass.
