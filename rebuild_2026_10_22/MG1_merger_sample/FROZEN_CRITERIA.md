# MG1_merger_sample: FROZEN CRITERIA (committed alone, before any script, table or web number)

Owner's go, 2026-11-02. Question: do lensing peaks follow galaxies in merging clusters generally? **Not blind.** Read before this: UX6's README, criteria and script (all present-gas readings DEAD on the Bullet; N2 only right sign). General background knowledge of the literature, from memory and unchecked: the Bullet offset, A520's contested dark core, and that El Gordo and MACS J0025 are usually described as peaks on galaxies. So I expect most rows GAL. The literature on this is selected toward systems with visible offsets; this is not a fair sample. kappa = 1/2 FITTED. Cold sector stays retired; no result reinstates it. No particle. Footings canonical 9.3603e-11, alt 1.1312e-10, never pooled. Not theory closed. Nothing here says the data favour the framework. No downloads: web reading only, every web number PROVISIONAL.

## Table
One row per subcluster: system, z, separations d(lens, gal), d(lens, gas), d(gal, gas) in kpc, errors, masses (lens, gas, stars) where published, reference URL, method, flags. Offsets from published values, or from published coordinates if no offset is stated. Target list: Bullet (control, not counted), El Gordo, MACS J0025, Abell 520, Abell 2744, Abell 754, MACS J0717, DLSCL J0916, ZwCl 0008, plus others found. A system I can't get numbers for is listed as NO NUMBERS, not dropped silently. Contested systems: every published reading gets a row; counted under the most recent map-level analysis with the other reading run as a stated alternate count.

Errors: published, quadrature of lens, gas and galaxy terms where given. Missing: ASSUMED sigma 50 kpc (space-based lens map) or 100 kpc (ground-only), flagged, with a rerun at x2.

## Observed label, per subcluster (data only, no model, footing independent)
Z_gal = d(lens, gal)/sigma, Z_gas = d(lens, gas)/sigma.
- **GAL:** Z_gal <= 2 and Z_gas > 2.
- **GAS:** Z_gas <= 2 and Z_gal > 2.
- **BETWEEN:** both > 2.
- **UNRESOLVED:** both <= 2. Decides nothing.
- **NOT USABLE:** no quantitative offset can be got.
Qualitative statements ("coincident with galaxies") with no number are NOT USABLE for the count, listed separately as a reported row.
Counts: by subcluster and by system, with Bullet out and in, all rows and only rows with published errors. Rerun at threshold 1 sigma reported.

## Simple model, per subcluster pair: my reading, with limits
UX6's forms on an isolated pair: gas Plummer (M_gas, a_gas) at origin; stars Plummer (M_star, a_star) at distance s = d(gal, gas). Forms LAW (k = 0), L1, L2, N1, N2, as UX6, N1, N2 about the galaxy centre. k: UX3's fit from `ux3_kfit.json` and pi^2. QUMOND-type divergence plus baryons, as UX6, no regulator change. Inputs: published masses; missing M_gas = 0.12 M_lens and M_star = 0.02 M_lens, flagged DEFAULT, a_gas 300 kpc, a_star 200 kpc, fixed now. M_lens missing: 3e14, flagged. Reported rows at gas x 0.5, x 2. Both footings, both k.
Read: delta = d(peak, gas)/s, and dkappa = mean kappa in 100 kpc about galaxy minus about gas. Model predicts galaxy side if dkappa > 0 (and delta > 0.5).
No mass grade: the isolated pair leaves out the partner and the data's masses are in unlike apertures. Position and sign only.

## Verdicts, frozen
Using usable rows with s resolved (s/sigma > 2), Bullet out, canonical and alt stated separately for the model. Observed fractions by subcluster.
- **Local-gas reading (L1, L2, N1):** **DEAD IN GENERAL** if at least 3 systems, and at least 2/3 of resolved subclusters, read GAL with model dkappa <= 0. **NOT GENERALISED** if the Bullet's failure repeats in fewer. **INSUFFICIENT** if fewer than 3 systems are resolved.
- **Carried-memory reading (N2):** predicts GAL everywhere. **SIGN HOLDS** if at least 2/3 of resolved subclusters read GAL and none reads GAS at published error; **SIGN HOLDS WITH EXCEPTIONS** if 2/3 reached and some GAS; **SIGN FAILS** under 2/3. Any of these is sign only: no mass, no named carrier, and a galaxy-following peak is equally what any mass moving with galaxies gives, so this cannot separate memory from that. A pass is a statement about position only.
- Selection stated in the title or first lines. A count isn't a rate.

## Checks
K1 Bullet pair control: L1 dkappa < 0 at both subclusters, N2 > 0, in UX6's direction at each footing and k fit. Pair model differs from UX6's full model; compare, report. K2 concentric reduction: L1, L2, N1, N2 equal law x (1 + k g_gas/a0), 1e-3. K3 label controls: synthetic rows on galaxies, gas, midway, and coincident give GAL, GAS, BETWEEN, UNRESOLVED. K4 every table row carries a URL and PROVISIONAL tag, and each number comes from a page I read. K5 RSS under 4 GB. K6 positive control: extra mass on galaxies gives dkappa > 0; same on gas gives < 0. K7 second read: at least the rows driving the count re-read from a second page or the paper's own text where possible, disagreements stated. A failed K1 (sign), K2, K3 or K6 stops the verdict.
**MUTATE twin, must fail:** gal and gas positions swapped in the K3 controls, L2 sign flipped in K2, K6 control on the wrong side. Outputs separate, exit 1. Rerun byte-identical.

## File list
Exact files for a map-level test: filename, source URL, size in bytes from HEAD (no body fetched) or archive page, for owner approval. Unverified sizes marked so.

## Expectation, mine, on record
Most usable rows GAL: 70 %. Local-gas DEAD IN GENERAL: 60 %, INSUFFICIENT 30 %. N2 SIGN HOLDS or WITH EXCEPTIONS: 75 %. Many rows lack published errors: 85 %. A520 as an exception in some reading: 80 %.

## Limits known now
Published offsets, unlike methods, different aperture and resolution, few with errors. Projection and inclination ignored. Isolated pair, static, no orbit. a0 at z = 0, though some systems are at z ~ 0.9. k from relaxed clusters carried over. WebFetch summaries can be wrong; PROVISIONAL throughout. Not a map-level test.

Compute: one thread, nice 15, under 4 GB.
