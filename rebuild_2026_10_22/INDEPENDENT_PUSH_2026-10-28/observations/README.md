# CRISP FINDING: four SLUGGS gas temperatures recovered; HG's FAINT arm contains a known group-scale hot halo

Nothing here upgrades the theory's grade. No new group enters a graded sample. κ=1/2 remains fitted. The canonical and alt acceleration footings remain separate; the X-ray hydrostatic diagnostic itself contains no a0, so its result is identical on both.

## What changed

1. The claim that no SLUGGS kT is available is now obsolete as a data-availability statement. All four measured spectral temperatures, their source apertures, gas-density beta slopes and core radii are recovered in `sluggs_xray_inputs.csv`.
2. NGC4261 is an actual physical-interpretation counterexample for HG1/HG2's FAINT flag: it has a measured group-scale atmosphere but is stored as FAINT, with zero gas. It contributes to a shared sigma bin.
3. A newer stellar-tracer inclination estimate for IC1613 is recovered and its assumptions distinguished from a direct geometric measurement. It weakens the fixed-inclination precision claim; it does not demonstrate a successful gravity fit.

## SLUGGS: genuine measurements, a conditional diagnostic

Primary source: [Babyk et al.2018, accepted arXiv1803.00020v1](https://arxiv.org/abs/1803.00020v1), Tables1–3. The journal DOI is10.3847/1538-4357/aab3c9. The retrieved file is the exact accepted preprint, not the inaccessible journal PDF. Temperatures are measured from Chandra spectra within5 optical effective radii; they are not converted from stellar dispersion. Source distances differ and are retained.

| Object | kT,keV (formal1sigma) | gas beta | source aperture,kpc | aperture at SLUGGS distance,kpc | mean log10(sigmaGC/sigmaX) | GC projected bins inside aperture |
|---|---:|---:|---:|---:|---:|---:|
| M87 |1.850±.002|.50|35±4|32.1|−.132|4/6|
| NGC4365 |.440±.020|.36|28±2|36.7|+.146|4/5|
| NGC4374 |.810±.005|.48|32.51±3|36.5|−.086|1/1|
| NGC5846 |.790±.003|.38|34±6|39.4|+.035|3/5|

The new diagnostic uses the measured beta/core parameters and the isothermal hydrostatic **total** acceleration

    g_X(r)=3 beta [kT/(mu m_p)] r/(r^2+rc^2), mu=.62.

It independently integrates spherical Jeans and projects through the existing measured GC tracer-density functions. M87/NGC5846 retain the older literature model-derived GC anisotropy functions; NGC4365/4374 retain assumed isotropy. No GC fit was performed. Stellar gravity is not added to this already-total hydrostatic force. This differs from GT1's fixed beta=2/3,rc=.15R500 and is not an unchanged-GT1 test.

The opposing offsets do not establish a cure. At NGC4374's sole outer GC bin,70% of the predicted variance comes from force outside the spectral aperture, under the assumed continuation. Several other outer bins are entirely outside. Global spectral apertures also do not guarantee gas detection at their edge; the source explicitly extrapolates some mass profiles. M87's single-temperature spectral statistic/dof=4.3, and three beta fits have chi2/dof near3, so tiny formal kT errors are insufficient model errors.

An independent [CGA2019 Table5](https://cxc.cfa.harvard.edu/GalaxyAtlas/Common_Fig/Table5.html) recovery gives reliable measured-gas Rmax=24.9kpc for NGC4374 and50.7kpc for NGC5846 at its own distances (25.0/49.3kpc after matching SLUGGS distances). The respective emission-weighted temperatures to Rmax are.92 and.82keV. Rounded zero errors are not exact uncertainties. Small radial-profile PDFs are retained; numeric radial profiles and covariance remain missing. This is a recovered input set and an aperture-sensitive shared-potential diagnostic, not a four-object PASS/FAIL.

## Groups: a real FAINT-label counterexample, not an expanded sample

[O'Sullivan et al.2017 arXiv1708.03555v2](https://arxiv.org/abs/1708.03555v2), Tables1/3/4, supplies26 high-richness CLoGS positions and14 group-scale gas halos. Exact BGE-to-KT2017 optical-member association (<1arcmin and <500km/s), the original HG footprint, and existing GA BRIGHT identities leave one additional candidate:NGC4261, principalPGC39659,129 members,sigma382km/s. Northern coverage and the optical velocity limit prevent treating all14 as additions.

NGC4261 has measured gas kT=1.36(−.02,+.03)keV and group-scale emission detected to85kpc. Existing HG1 and HG2 JSON rows label that same optical group FAINT,erass=null,mgas=0. HG2's stored delta is+.601569dex. It belongs to shared sigma bin25, with2 BRIGHT and5 FAINT objects. This establishes that **no selected eRASS match is not physical absence of a hot atmosphere**. It does not establish a software error in the stated matching rule.

The HG evaluation radius is 619.225 kpc. The 85 kpc detection radius at CLoGS's 32 Mpc becomes 87.81 kpc at HG's 33.058 Mpc, leaving a factor of 7.052 in radius. CLoGS's R500/M500 values are scaling-derived and were excluded. A physical reanalysis still needs a measured gas normalization/profile with uncertainty at the HG radius, unique association checks and sensitivity-matched X-ray non-detections for the controls. No label was flipped and D was not recomputed. Full overlap and eligibility rows are in the results JSON, not merely a candidate bibliography.

## IC1613: independent tracers, conditional geometry

[Taibi et al.2024,A&A689A88](https://doi.org/10.1051/0004-6361/202449468), section6.2,p17, derives i=32±11degrees (simpler model36±11) by equating asymmetric-drift-corrected circular velocities of red giants and main-sequence stars. This is independent of the adopted HI inclination, but conditional on shared geometry/potential and profile assumptions; its general method uses an HI-derived core radius. Thin-disk photometry gives about37degrees and presumes intrinsic shape.

Optimistically scaling all of RT1's speed by sin48/sin32 gives23.70km/s and acceleration residual−.299dex canonical/−.338alt. Zero-residual angles would be22.06/21.05degrees under that heuristic. **Oh2015's speed is already pressure-support corrected**, so these are upper bounds on the correction when the positive pressure term is held fixed, not a new gas fit. The delta-method angle uncertainty is.267dex and is not a new significance grade.

The newer stellar result vcirc(rhalf)=15±2km/s gives Mdyn=1.1±.3e8Msun, compared with its same-radius Wolf estimate1.0±.2e8. It detects rotation and cautions that the dispersion estimator's symmetry, nonrotation and flat-dispersion assumptions are violated to some extent. The similar masses retain the tension; the data do not justify calling it eliminated.

## Reproduce and audit

From repository root:

    python3 rebuild_2026_10_22/INDEPENDENT_PUSH_2026-10-28/observations/extract_published_tables.py
    PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n15 python3 -B rebuild_2026_10_22/INDEPENDENT_PUSH_2026-10-28/observations/recover_observations.py
    PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n15 python3 -B rebuild_2026_10_22/INDEPENDENT_PUSH_2026-10-28/observations/recover_observations.py --mutate

Normal run 8/8 checks; mutation breaks the analytic oracle and exits1,as designed. Independent Jeans baseline reproduces CFG528b to1.58e-6dex; analytic isothermal result to6.68e-6relative. Runs take about 7 seconds and 0.24 GB, one thread. The sandbox denies the requested nice priority; no elevated-priority retry was made. Python 3.9.6, numpy 1.26.2, scipy 1.11.4. The code audits every repository-local file read and records before/after hashes. Full downloaded papers live only in gitignored `sources/`; small derived tables and provenance records remain reviewable. Frozen criteria were files only by coordinator instruction because .git is read-only; no commit or old-lane edit was made.
