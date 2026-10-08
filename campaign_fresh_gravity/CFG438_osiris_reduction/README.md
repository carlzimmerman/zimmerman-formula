# CFG438: our own OSIRIS DRP reduction of BX442 and A1689B11.2. The cubes exist; the frozen BX442 validation fails on S/N

**Bottom line.** We ran the official Keck OSIRIS DRP under GDL in Docker. It turned the raw KOA frames into mosaicked data cubes for both galaxies. For BX442 the H-alpha line is clearly detected (summed S/N 12 to 19), and there is a velocity gradient. But at the frozen per-spaxel cut (S/N ≥ 5) only 27 spaxels pass, all on one side of the galaxy. The frozen validation against Law et al. 2012 therefore returns **NOT VALIDATED**. The MUTATE control behaves correctly. A1689B11.2 shows no credible detection in our image-plane cube. No a0 claim is made here.

## Reduction (official DRP, GDL port)
- **DRP version.** The DRP is Keck-DataReductionPipelines/OsirisDRP at commit 0601063 (2023-07-21), compiled in the `osiris-gdl` image (GDL 1.0.1).
- **Modules, BX442.** Each frame went through:
  - Subtract Frame (its A/B nod partner);
  - Adjust Channel Levels;
  - Remove Crosstalk;
  - Glitch Identification;
  - Extract Spectra, using recmat s100714_c006 Kn2_100 (the DRP's C rectification, called through CALL_EXTERNAL);
  - Assemble Data Cube (wavelength solution osiris_wave_coeffs_091005-120103);
  - Correct Dispersion;
  - Save.

  Clean Cosmic Rays was skipped, per Keck advice.
- **Modules, A1689B11.2.** The same chain, with these differences:
  - Subtract Frame uses the sky frame nearest in time;
  - no Glitch Identification (H2RG detector, where the DRP also skips channel/crosstalk);
  - recmat s170529_c009 Kn5_050.
- **Mosaics.** Mosaic Frames (MEANCLIP, TEL offsets) gave:
  - BX442: 40 cubes → 421 × 95 × 53;
  - A1689B11.2: 8 cubes → 465 × 66 × 51. These frames have no dithers.
- **Object and sky assignment, from the headers.**
  - BX442: all 40 × 900 s frames are on source. They alternate between two positions 2.8" apart (an A/B nod inside the field), so each frame minus its partner gives 40 cubes.
  - A1689B11.2: the RA 197.87116 pointing (8 frames) is the object; RA 197.87254 (5 frames, 5" east) is sky.
  - The DRFs are written by `make_drfs.py`.
- **Instrumental sigma.** 46.6 km/s (R ≈ 2730), from 9 isolated OH lines in a DRP cube of one unsubtracted frame. The OH line centres agree with vacuum OH wavelengths to about 0.5 Å, i.e. ≤ 10 km/s.
- **GDL port: infrastructure only.** No reduction algorithm was touched. The patched files, a full diff and the runner are in `gdl_port/`. GDL 1.0.1 differs from IDL in five ways that blocked the backbone:
  1. The `<IDL_DEFAULT>` path token, so GDL's own library was put on `!PATH`.
  2. There is no `BIN_DATE`, so a 10-line shim was added.
  3. `IDLffXMLSAX` passes only one attribute per element to `StartElement`, and does not bind SELF in `StartDocument`/`EndDocument`. A small XML walker (`gdlsax_parse.pro`) now calls the parsers' own callbacks, and the two document callbacks are called explicitly.
  4. GDL enforces object-field privacy (`Backbone.<field>`), so accessor methods were added.
  5. There is no `IDLffXMLDOMDocument`, which assembcube uses only to read `calibrations.xml`. A minimal read-only DOM was added.

  GDL's warning "Assignment to loop variable" was checked: the semantics match IDL.
- The cubes and logs are in ../_external_data/cfg438_work/ (not in git).

## BX442 frozen result (`cfg438_kinematics.py bx442`)
| check | value | frozen tolerance | verdict |
|---|---|---|---|
| V1 line found | 27 spaxels at S/N ≥ 5; summed S/N 11.9 at v = −181 km/s | ≥ 30 spaxels, summed S/N ≥ 10, \|v\| ≤ 300 | **FAIL** (count) |
| V2 kinematic PA | 203° (199–207); the tanh fit sits at its bounds | within 20° of 168° | **FAIL** |
| V3 V_c at R ≥ 6 kpc | not computable: no radius has passing spaxels on both sides | 234 (+49, −29) | not evaluated |
| V4 σ_m (flux-weighted, intrinsic) | 76.7 ± 11.2 km/s | 66 ± 6 → PASS if \|Δ\| ≤ 12.7 | **PASS** |

Lane verdict: **NOT VALIDATED**. The slit profile does show a gradient: −51 to −66 km/s on one side and +73 to +108 km/s on the other, within 0.65". But the passing spaxels are too few and too one-sided to fix the PA or fold a rotation curve.

**MUTATE** (fit at z = 2.200): 1 spaxel passes, against 27 at the true z, so under 10%. The summed-spectrum S/N is 1.6 (< 5). The control fails to find a line, as it must. The S/N machinery is not manufacturing detections.

## Post-freeze diagnostic (`cfg438_diag_postfreeze.py`; NOT part of the verdict)
With the cut relaxed to S/N ≥ 3, roughly Law+12's visual cut, and everything else frozen:
- **Spaxel counts and summed line.** 74 spaxels pass at S/N ≥ 4 and 203 at S/N ≥ 3. 134 of the S/N ≥ 3 spaxels lie within 1" of their flux centre. Their summed H-alpha has S/N 18.7.
- **Restricted to that 1" region:**
  - kinematic PA = 173° (172–174), within 5° of Law's 168°;
  - projected velocities run from −125 to +160 km/s (5–95%), matching Law's "±150 km/s". Half that range over sin 42° is about 213 km/s;
  - σ_m = 86 km/s, median 60.
- **Without the spatial restriction,** the full frozen chain at S/N ≥ 3 picks up noise spaxels across the field. The PA goes to 146° and V3 lands on a spurious point at 17 kpc. So the S/N ≥ 3 agreement depends on a spatial selection that was not frozen. It is a hint, not a validation.
- **Systemic offset.** Every route puts the line about 80–100 km/s blue of Law's z = 2.1765 (the summed fits). Our OH wavelength check rules out a wavelength-scale error larger than about 10 km/s. The origin is unresolved (light-weighting, or the systemic definition). It does not affect V_rot or σ.

## A1689B11.2 (descriptive only)
16 spaxels pass S/N ≥ 5. The summed spectrum has S/N 5.2 with σ = 24 km/s, which is narrower than the instrument and so most likely noise. No H-alpha detection is claimed in our image-plane cube. Possible reasons:
- the cube edges carry strong artefacts;
- no lens model was used;
- the source may not sit where we assumed, though the object/sky assignment follows the headers.

## Caveats
- We used 40 frames, against Law's 52 (their third night is not in this set).
- There was no telluric or flux calibration, and no per-channel sky scaling (Law scaled the subtracted frame per channel). Both lower our S/N relative to theirs.
- Our V(R) would not be PSF-corrected even where measurable.
- The cube orientation is taken from the DRP WCS (Keck II era). Parity was not independently verified.

## Files
- **Scripts:**
  - `make_drfs.py` (DRF queues and mosaic DRFs);
  - `gdl_port/` (GDL patches, diff, runner);
  - `cfg438_kinematics.py` (frozen extraction);
  - `cfg438_diag_postfreeze.py` (labelled diagnostic).
- **Outputs:** `cfg438_<mode>_results.json`, `_maps.png`, `_slit_profile.txt`, `_VR_sigmaR.txt`, `_summed_spectrum.txt`, and the `.out` logs, for these modes:
  - `bx442`;
  - `bx442_MUTATE`;
  - `bx442_DIAG_SN3`;
  - `a1689`.
